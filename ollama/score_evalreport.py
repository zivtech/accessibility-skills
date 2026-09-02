#!/usr/bin/env python3
"""Rule-based scorer for the evaluation-report lane (adoption plan step 11b).

Scores a model-produced Accessibility Evaluation Report (the aggregation of
a finished audit's evidence, shaped by docs/a11y-evaluation-report-contract.md)
against a fixture's metadata expectations
(evals/suites/evaluation-report/fixtures/*.metadata.yaml):

1. Required contract sections present (heading scan, label fallback)
2. finding_id integrity, both directions — all expected ids present, and no
   invented id matching finding_id_pattern (fabrication)
3. Severity preservation near each named finding_id (orthogonality probe)
4. Per-criterion outcomes — failed/passed/inapplicable as evidenced, and the
   never-evaluated criterion reported untested, never passed (fabrication)
5. must_contain / boundary_must_contain any-of groups (representativeness
   result, baseline echo, identity, coverage boundary)
6. Statement discipline — no assertive product-wide conformance claim after
   negation-stripping (honest refusals quoting the claim survive)
7. fabricated_tokens — environment data no input stream contains (hard FAIL)

Status: PASS (all musts, no fabrication), WARN (musts pass, should/nice
missed), FAIL (any must missed or fabrication detected).

Known limits (also in fixture notes): any-token line checks undercount
paraphrase; the negation strip is a heuristic; adjudicate misses by reading
before counting them.

Usage:
    python3 ollama/score_evalreport.py <response.json> <metadata.yaml>
"""

import json
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(__file__))
from score_common import strip_negation_lines, strip_thinking  # noqa: E402

HEADING_RE = re.compile(r"(?im)^#{1,6}\s+(.+?)\s*$")

OUTCOME_TOKENS = {
    "fail": ["fail"],
    "pass": ["pass"],
    "inapplicable": ["inapplicable", "not applicable"],
    "untested": ["untested", "not evaluated", "not tested", "cantTell",
                 "cannot tell", "cant tell"],
}


def load_response(path):
    with open(path) as f:
        data = json.load(f)
    text = data["response"] if isinstance(data, dict) else str(data)
    cleaned, truncated = strip_thinking(text)
    return cleaned, truncated


def find_sections(text):
    """Return [(title, content_start, content_end)] for markdown headings."""
    matches = list(HEADING_RE.finditer(text))
    sections = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections.append((m.group(1), m.end(), end))
    return sections


def section_span(sections, patterns, text):
    """Span of the first heading matching any pattern; whole doc if none."""
    for title, start, end in sections:
        low = title.lower()
        if any(p.lower() in low for p in patterns):
            return text[start:end], True
    return text, False


def any_token(text_lower, tokens):
    return any(t.lower() in text_lower for t in tokens)


def check_outcomes(span, checks, tier, must_miss, fabrications):
    """Line-scoped outcome checks; returns list of (desc, hit) for printing."""
    results = []
    lines = span.splitlines()
    for chk in checks or []:
        pats, expect = chk["sc_patterns"], chk["expect"]
        sc_lines = [l for l in lines if any(p.lower() in l.lower() for p in pats)]
        desc = f"{pats[0]} → {expect}"
        if not sc_lines:
            results.append((desc, False))
            if tier == "must":
                must_miss.append(f"outcome: no line names {pats[0]}")
            continue
        joined = "\n".join(sc_lines).lower()
        hit = any_token(joined, OUTCOME_TOKENS[expect])
        if expect == "untested":
            survivors = strip_negation_lines("\n".join(sc_lines)).lower()
            if "pass" in survivors:
                fabrications.append(
                    f"{pats[0]} marked passed but nothing evaluated it")
        results.append((desc, hit))
        if not hit and tier == "must":
            must_miss.append(f"outcome: {pats[0]} not reported {expect}")
    return results


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: ollama/score_evalreport.py <response.json> <metadata.yaml>")

    text, truncated = load_response(sys.argv[1])
    if truncated:
        print("Response truncated mid-<think> block — not scoring")
        print("Status: INCOMPLETE — truncated response")
        return
    with open(sys.argv[2]) as f:
        meta = yaml.safe_load(f)

    text_lower = text.lower()
    sections = find_sections(text)
    must_miss, should_miss, fabrications = [], [], []

    print(f"Fixture: {meta['fixture_id']}")
    print(f"Response length: {len(text)} chars\n")

    # 1. required sections
    print("Required sections:")
    for spec in meta.get("required_sections", []):
        present = (
            section_span(sections, spec["patterns"], text)[1]
            or any_token(text_lower, spec["patterns"])
        )
        print(f"  {'+' if present else 'X'} {spec['name']}")
        if not present:
            must_miss.append(f"section missing: {spec['name']}")

    # 2. finding ids, both directions
    expected_ids = meta.get("expected_finding_ids", [])
    found_tokens = set(re.findall(meta["finding_id_pattern"], text))
    missing_ids = [i for i in expected_ids if i not in found_tokens]
    invented = sorted(found_tokens - set(expected_ids))
    print(f"\nFinding ids: {len(expected_ids) - len(missing_ids)}/"
          f"{len(expected_ids)} present, {len(invented)} invented")
    for i in missing_ids:
        must_miss.append(f"finding_id missing: {i}")
        print(f"  X missing: {i}")
    for i in invented:
        fabrications.append(f"invented finding_id: {i}")
        print(f"  X invented: {i}")

    # 3. severity preservation near ids. The span is truncated at the next
    #    finding-id token so a list neighbor's severity can never satisfy this
    #    finding's check (calibration 2026-08-01: an untruncated window masked
    #    both planted re-ranks). Any occurrence may carry the severity —
    #    reports legitimately cross-reference ids in outcome evidence rows
    #    before stating severity in the findings section.
    window = meta.get("severity_window", 400)
    id_re = re.compile(meta["finding_id_pattern"])
    print("\nSeverity preservation:")
    for fid, sev in (meta.get("severity_pairs") or {}).items():
        ok = False
        for m in re.finditer(re.escape(fid), text):
            end = m.end() + window
            nxt = id_re.search(text, m.end())
            if nxt and nxt.start() < end:
                end = nxt.start()
            if sev.lower() in text[m.end():end].lower():
                ok = True
                break
        print(f"  {'+' if ok else 'X'} {fid} stays {sev}")
        if not ok:
            must_miss.append(f"severity: {fid} not reported {sev}")

    # 4. outcomes (scoped to the outcomes section when found)
    outcome_spec = next(
        (s for s in meta.get("required_sections", []) if s["name"] == "outcomes"),
        {"patterns": ["outcome"]},
    )
    span, scoped = section_span(sections, outcome_spec["patterns"], text)
    checks = meta.get("outcome_checks", {})
    print(f"\nOutcomes ({'section-scoped' if scoped else 'whole-document'}):")
    for desc, hit in check_outcomes(span, checks.get("must"), "must",
                                    must_miss, fabrications):
        print(f"  {'+' if hit else 'X'} {desc}")
    for desc, hit in check_outcomes(span, checks.get("should"), "should",
                                    [], fabrications):
        print(f"  {'+' if hit else 'x'} {desc} (should)")
        if not hit:
            should_miss.append(f"outcome: {desc}")

    # 5. must_contain groups + boundary-scoped groups
    print("\nKey values:")
    for group in meta.get("must_contain", []):
        hit = any_token(text_lower, group)
        print(f"  {'+' if hit else 'X'} any of {group[:3]}")
        if not hit:
            must_miss.append(f"missing all of: {group}")
    bspan, bscoped = section_span(
        sections, ["coverage boundary", "boundary"], text)
    for group in meta.get("boundary_must_contain", []):
        hit = any_token(bspan.lower(), group)
        print(f"  {'+' if hit else 'X'} boundary"
              f"{' (scoped)' if bscoped else ''}: any of {group[:3]}")
        if not hit:
            must_miss.append(f"boundary missing all of: {group}")

    # 6. statement discipline
    survivors = strip_negation_lines(text).lower()
    for phrase in meta.get("assertive_claim_must_not", []):
        if phrase.lower() in survivors:
            fabrications.append(f"assertive conformance claim: '{phrase}'")
    withhold = any_token(text_lower, meta.get("statement_withholding_should", []))
    if not withhold:
        should_miss.append("no explicit statement-withholding language")
    print(f"\nStatement: {'no assertive claim' if not any('claim' in f for f in fabrications) else 'ASSERTIVE CLAIM FOUND'}; "
          f"withholding language {'present' if withhold else 'absent (should)'}")

    # 7. fabricated environment tokens (word-boundary)
    for tok in meta.get("fabricated_tokens", []):
        if re.search(rf"(?i)\b{re.escape(tok)}\b", text):
            fabrications.append(f"environment token never in input: {tok}")

    nice_hit = any_token(text_lower, meta.get("nice_to_have_tokens", []))
    if not nice_hit:
        should_miss.append("no orthogonality language (nice)")

    print(f"\nMust misses: {len(must_miss)}")
    for m in must_miss:
        print(f"  - {m}")
    print(f"Fabrications: {len(fabrications)}")
    for f_ in fabrications:
        print(f"  - {f_}")
    print(f"Should/nice misses: {len(should_miss)}")
    for s in should_miss:
        print(f"  - {s}")

    if must_miss or fabrications:
        status = "FAIL"
    elif should_miss:
        status = "WARN"
    else:
        status = "PASS"
    print(f"\nStatus: {status}")


if __name__ == "__main__":
    main()
