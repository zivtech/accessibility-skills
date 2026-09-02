#!/usr/bin/env python3
"""Rule-based scorer for the a11y-test-operation-evidence eval lane.

Scores a model-produced operation-evidence admissibility review against a
fixture's metadata expectations (evals/suites/a11y-test-operation-evidence/
fixtures/*.metadata.yaml). Rule *selection* (which of the five operation-
evidence rules a package violates) is the model's semantic judgment; the
Structured disposition block the review closes with
(.claude/skills/a11y-test/SKILL.md, "### Structured disposition block") makes
*reporting* that judgment mechanical — the same reporting-is-mechanical split
`ollama/score_acr.py` uses for the ACR YAML block.

Checks:
1. Response truncation (unclosed <think>) -> Status: INCOMPLETE, not scored
2. Structured disposition ```yaml fence present and parseable
3. Required keys: admissibility, dispositions, rules_violated, claim_boundary
4. admissibility is ACCEPT|REJECT and matches expected_admissibility
5. dispositions is a mapping of known values, matching expected_dispositions
6. rules_violated: mapping-or-empty, rule ids from the five stable ids only
   (unknown ids are a fabrication), operations named must exist in
   dispositions, and ACCEPT/REJECT consistency with emptiness
7. must_catch[]: each expected rule fired on its operation (must-tier); its
   hook_present tokens appear in the prose remainder (should-tier).
   hook_absent_in_evidence is documentation-only — NOT checked here; it
   describes what a well-formed rejection's prose should not contain, but
   enforcing it would penalize a correct review for simply not describing
   evidence the package never had. Left for human/model-judge adjudication.
8. rules_violated_must_be_empty_for[]: any rule fired on a listed operation
   is a false fire (must-tier); and, exhaustively, any (operation, rule)
   pair outside must_catch is an unexpected fire (must-tier) — over-flagging
   fails, not just under-flagging (opt out: rules_violated_exhaustive: false)
9. expected_verdict_must_not[]: forbidden phrases, checked against the prose
   remainder after strip_negation_lines (an honest "the run claims 2.1.2
   FAIL but that is not supported" must survive; a bare ratification must
   not) — a hit is a fabrication, same tier as score_evalreport.py's
   assertive-claim scan
10. claim_boundary: non-empty string; should name every operation in
    dispositions

Status: PASS (all musts, no fabrication), WARN (musts pass, should missed),
FAIL (any must missed or fabrication detected).

Usage:
    python3 ollama/score_operation_evidence.py <response.json> <metadata.yaml>
"""

import json
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(__file__))
from score_common import strip_negation_lines, strip_thinking  # noqa: E402

YAML_FENCE_RE = re.compile(r"```ya?ml\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)

STABLE_RULE_IDS = {
    "bounded_diagnostic_not_promoted",
    "setup_action_continuity",
    "natural_only_conditional_state",
    "passive_observation_binding",
    "ancestor_remapping_review",
}
ADMISSIBILITY_VALUES = {"ACCEPT", "REJECT"}
DISPOSITION_VALUES = {"PASS", "FAIL", "UNTESTED", "BLOCKED"}
REQUIRED_KEYS = ("admissibility", "dispositions", "rules_violated", "claim_boundary")


def load_response(path):
    with open(path) as f:
        data = json.load(f)
    text = data["response"] if isinstance(data, dict) else str(data)
    return strip_thinking(text)


def extract_disposition_yaml(text):
    """Return (yaml_text, doc, remainder). Picks the largest fence whose
    parse is a dict containing 'admissibility'; remainder is the response
    minus the chosen fence (prose, including any other fences). When no
    fence parses, doc is None and the second slot carries (body, error) for
    the largest fence that mentions admissibility, so a quoting slip is
    reported as an unparseable block rather than as no block at all."""
    best = None
    broken = None  # largest fence that names admissibility but fails to parse
    for m in YAML_FENCE_RE.finditer(text):
        body = m.group(1)
        try:
            parsed = yaml.safe_load(body)
        except yaml.YAMLError as err:
            if "admissibility" in body and (broken is None or len(body) > len(broken[0])):
                broken = (body, str(err).splitlines()[0])
            continue
        if isinstance(parsed, dict) and "admissibility" in parsed:
            if best is None or len(body) > len(best[0]):
                best = (body, parsed, m.span())
    if best is None:
        return None, broken, text
    start, end = best[2]
    return best[0], best[1], text[:start] + text[end:]


def check_required_keys(doc, must_miss):
    for k in REQUIRED_KEYS:
        if k not in doc:
            must_miss.append(f"missing key: {k}")


def check_admissibility(doc, meta, must_miss):
    val = doc.get("admissibility")
    if val is None:
        return None
    val_s = str(val).strip()
    if val_s not in ADMISSIBILITY_VALUES:
        must_miss.append(f"admissibility: unknown value '{val_s}'")
        return val_s
    expected = meta.get("expected_admissibility")
    if expected and val_s != str(expected):
        must_miss.append(f"admissibility: got '{val_s}', expected '{expected}'")
    return val_s


def check_dispositions(doc, meta, must_miss):
    dispositions = doc.get("dispositions")
    if dispositions is None:
        return {}
    if not isinstance(dispositions, dict):
        must_miss.append("dispositions must be a mapping")
        return {}
    unknown = set()
    for op, val in dispositions.items():
        val_s = str(val).strip()
        if val_s not in DISPOSITION_VALUES:  # case-sensitive: the contract's closed set is uppercase
            must_miss.append(f"unknown disposition value for {op}: '{val}'")
            unknown.add(op)
    expected = meta.get("expected_dispositions") or {}
    for op, want in expected.items():
        if op not in dispositions:
            must_miss.append(f"disposition {op}: missing")
        elif op not in unknown:
            got = str(dispositions[op]).strip()
            if got != str(want):
                must_miss.append(
                    f"disposition {op}: got '{got}', expected '{want}'")
    return dispositions


def normalize_rules_violated(doc, dispositions, must_miss, fabrications):
    """Return {op: [rule_id, ...]} — {}, [], None all normalize to empty.
    Flags fabricated rule ids and operations absent from `dispositions`."""
    raw = doc.get("rules_violated")
    if raw in ({}, [], None):
        return {}
    if not isinstance(raw, dict):
        must_miss.append("rules_violated must be a mapping of operation id to rule ids")
        return None  # shape error: the consistency check has nothing to compare

    rules_map = {}
    for op, rules in raw.items():
        if rules in (None, [], {}):
            rule_list = []
        elif isinstance(rules, list):
            rule_list = [str(r) for r in rules]
        else:
            rule_list = [str(rules)]
        rules_map[op] = rule_list

        if op not in dispositions:
            must_miss.append(
                f"rules_violated names an operation not in dispositions: {op}")
        for rid in rule_list:
            if rid not in STABLE_RULE_IDS:
                fabrications.append(f"unknown rule id in rules_violated: {rid}")
    return rules_map


def check_admissibility_consistency(admissibility, rules_map, must_miss):
    if rules_map is None:
        return
    any_nonempty = any(rules_map.values())
    if admissibility == "ACCEPT" and any_nonempty:
        must_miss.append("admissibility ACCEPT but rules_violated is not empty")
    if admissibility == "REJECT" and not any_nonempty:
        must_miss.append("admissibility REJECT but rules_violated is empty")


def check_must_catch(meta, rules_map, remainder, must_miss, should_miss):
    low_remainder = remainder.lower()
    for entry in meta.get("must_catch") or []:
        rule = entry["id"]
        op = entry.get("operation")
        if op:
            found = rule in (rules_map.get(op) or [])
            if not found:
                must_miss.append(f"rules_violated missing: {rule} under {op}")
        else:
            found = any(rule in v for v in rules_map.values())
            if not found:
                must_miss.append(f"rules_violated missing: {rule}")
        print(f"  {'+' if found else 'X'} {rule}"
              f"{' under ' + op if op else ''}")

        hooks = entry.get("hook_present") or []
        hook_hit = any(h.lower() in low_remainder for h in hooks)
        if hooks and not hook_hit:
            should_miss.append(f"hook not mentioned for {rule}: {hooks}")
        # entry.get("hook_absent_in_evidence") is documentation-only — see
        # module docstring point 7. Deliberately not checked.


def check_must_be_empty_for(meta, rules_map, must_miss):
    for op in meta.get("rules_violated_must_be_empty_for") or []:
        for rid in rules_map.get(op) or []:
            must_miss.append(f"rule fired on admissible operation {op}: {rid}")


def check_no_unexpected_rules(meta, rules_map, must_miss):
    """Over-attribution is a miss too. A fixture's must_catch is the complete
    expected rules_violated map (entries without `operation` are allowed on
    any operation); any other (operation, rule) pair is a false fire. A
    review that fires every rule on every operation must not score PASS —
    that is the flag-everything critic this repo calls dead. Opt out per
    fixture with `rules_violated_exhaustive: false` (none do today)."""
    if meta.get("rules_violated_exhaustive", True) is False:
        return
    allowed_anywhere = {e["id"] for e in meta.get("must_catch") or [] if not e.get("operation")}
    allowed = {}
    for e in meta.get("must_catch") or []:
        if e.get("operation"):
            allowed.setdefault(e["operation"], set()).add(e["id"])
    already = set(meta.get("rules_violated_must_be_empty_for") or [])
    for op, rules in rules_map.items():
        if op in already:
            continue
        for rid in rules:
            if rid in STABLE_RULE_IDS and rid not in allowed.get(op, set()) and rid not in allowed_anywhere:
                must_miss.append(f"unexpected rule fired on {op}: {rid}")


def check_forbidden_phrases(meta, remainder, fabrications):
    survivors = strip_negation_lines(remainder).lower()
    for phrase in meta.get("expected_verdict_must_not") or []:
        if phrase.lower() in survivors:
            fabrications.append(f"forbidden verdict phrase: '{phrase}'")


def check_claim_boundary(doc, dispositions, must_miss, should_miss):
    cb = doc.get("claim_boundary")
    if not isinstance(cb, str) or not cb.strip():
        must_miss.append("claim_boundary missing or empty")
        return
    for op in dispositions:
        if op not in cb:
            should_miss.append(f"claim_boundary does not mention {op}")


def print_nice_to_have(meta, remainder):
    low_remainder = remainder.lower()
    for grp in meta.get("nice_to_have") or []:
        hit = any(t.lower() in low_remainder for t in grp)
        print(f"  {'+' if hit else '-'} nice-to-have: {grp[:3]}")


def run_checks(text, meta):
    """Run every check in order, printing progress. Returns (must_miss,
    should_miss, fabrications)."""
    must_miss, should_miss, fabrications = [], [], []
    print(f"Fixture: {meta['fixture_id']}")
    print(f"Response length: {len(text)} chars")

    yaml_text, doc, remainder = extract_disposition_yaml(text)
    if yaml_text is None:
        if doc is not None:  # (body, error) of an unparseable candidate
            must_miss.append(
                f"disposition block present but not parseable YAML: {doc[1]}")
            print("Structured block: X fence found but YAML does not parse")
        else:
            must_miss.append("no structured disposition block found")
            print("Structured block: X no disposition yaml fence found")
        doc = {}
    else:
        print(f"Structured block: + parsed ({len(yaml_text)} chars)")

    check_required_keys(doc, must_miss)

    admissibility = check_admissibility(doc, meta, must_miss)
    print(f"Admissibility: {admissibility!r} "
          f"(expected {meta.get('expected_admissibility')!r})")

    dispositions = check_dispositions(doc, meta, must_miss)
    print(f"Dispositions: {dispositions}")

    rules_map = normalize_rules_violated(doc, dispositions, must_miss, fabrications)
    check_admissibility_consistency(admissibility, rules_map, must_miss)
    print(f"Rules violated: {rules_map}")
    if rules_map is None:
        rules_map = {}

    print("\nMust-catch:")
    check_must_catch(meta, rules_map, remainder, must_miss, should_miss)
    check_must_be_empty_for(meta, rules_map, must_miss)
    check_no_unexpected_rules(meta, rules_map, must_miss)

    check_forbidden_phrases(meta, remainder, fabrications)
    check_claim_boundary(doc, dispositions, must_miss, should_miss)

    print("\nNice-to-have (informational only):")
    print_nice_to_have(meta, remainder)

    return must_miss, should_miss, fabrications


def print_verdict(must_miss, should_miss, fabrications):
    print(f"\nMust misses: {len(must_miss)}")
    for m in must_miss:
        print(f"  - {m}")
    print(f"Fabrications: {len(fabrications)}")
    for f_ in fabrications:
        print(f"  - {f_}")
    print(f"Should misses: {len(should_miss)}")
    for s in should_miss:
        print(f"  - {s}")

    if must_miss or fabrications:
        status = "FAIL"
    elif should_miss:
        status = "WARN"
    else:
        status = "PASS"
    print(f"\nStatus: {status}")


def main():
    if len(sys.argv) != 3:
        sys.exit(
            "Usage: python3 ollama/score_operation_evidence.py "
            "<response.json> <metadata.yaml>")

    text, truncated = load_response(sys.argv[1])
    with open(sys.argv[2]) as f:
        meta = yaml.safe_load(f)

    if truncated:
        # Same early exit as score_acr.py / score_evalreport.py: a response cut
        # off mid-<think> is not a review, and scoring its remainder would
        # record a FAIL against the model's judgment rather than its output.
        print(f"Fixture: {meta['fixture_id']}")
        print("Truncated: X unclosed <think> block — not scored")
        print("\nStatus: INCOMPLETE")
        return

    must_miss, should_miss, fabrications = run_checks(text, meta)
    print_verdict(must_miss, should_miss, fabrications)


if __name__ == "__main__":
    main()
