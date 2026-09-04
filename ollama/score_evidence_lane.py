#!/usr/bin/env python3
"""Score a Phase 3 evidence-volume-lane model row (context-utilization plan,
docs/plans/2026-08-24-context-utilization-plan.md §6 Phase 3; lane design:
evals/results/context-utilization-phase3/README.md; gate review:
docs/plans/2026-08-25-context-utilization-phase3-gate-review.md — F1-F8
below cite that doc's findings).

Ingests one model response + fixture metadata + lane-manifest per-item
keyword overrides + the fixture's committed pack completeness audit; emits
per row: must-find recall with adjudication-ready evidence quotes (matching
is EXPLICIT keyword overrides only, from `must_find_keywords` — never
score_output.py's generic cascade, which cannot discriminate 5 of this
lane's 9 must-finds, gate F1; score_output.py stays untouched, no
check_finding import); FP candidates on CLEAN fixtures (F8); a 4-bucket miss
partition — `not-tool-observable` / `raw-set-gap` / `pack-omission` /
`model-miss`, in that priority order (F4, see classify_miss docstring);
`output_clipped` when `done_reason == "length"` (F7); `prompt_eval_count`/
`done_reason` pass-through with an `invalid` flag on Phase 0 guard fires.

Fixtures are never hardcoded here — resolved from `lane_manifest.yaml`
(--manifest + --fixture-id). `aggregate_by_condition` keys by
(model, condition), never condition alone (F5b), with a dilution-eligible
`possible` denominator (F5c). `per_item_rows` flattens to
(model, condition, fixture, item_index) for per-item flip reporting (F5d).

Usage:
    # Real row, resolving paths + keyword overrides from the lane manifest:
    python3 ollama/score_evidence_lane.py response.json \\
        --fixture-id heading-hierarchy-skipped \\
        --condition curated-32k --payload CURATED --draw 1

    # Real row, explicit paths (no manifest) — keywords still required for
    # non-CLEAN fixtures via a standalone keywords file (same
    # must_find_keywords: shape as a manifest fixture entry):
    python3 ollama/score_evidence_lane.py response.json \\
        --metadata evals/suites/a11y-critic/fixtures/X.metadata.yaml \\
        --completeness-audit evals/results/context-utilization-phase3/completeness/X.audit.yaml \\
        --keywords-file X.keywords.yaml \\
        --condition dump-40k --payload DUMP --draw 2

    # Prove the partition/matching logic with synthetic + real-fixture rows:
    python3 ollama/score_evidence_lane.py --selftest

Known limits (same convention as score_output.py / score_evalreport.py):
this is a rule-based CANDIDATE detector, not a semantic adjudicator. A
"found" must-find item is a keyword-match candidate with a quoted response
line attached — every plan decision rule (P1/P1b/P2/P3) requires
content-adjudication of these candidates before counting them (single-draw
deltas are variance; see README §5-§7). Do not feed raw `matched_count`
numbers into a decision rule without that pass. CLEAN-fixture FP counts
specifically need the same pass before trusting them: a correctly-scoped
`nice_to_find` ENHANCEMENT reported as a numbered finding is not an FP
(gate F8) — `print_report` reports CLEAN rows as candidates requiring
adjudication, the same as HAS-BUGS rows, not a bare PASS/FAIL verdict.
"""

import argparse
import json
import os
import re
import sys
import tempfile

import yaml

sys.path.insert(0, os.path.dirname(__file__))
from score_common import normalize_quotes, strip_thinking  # noqa: E402
from score_output import check_verdict, count_false_positives  # noqa: E402

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_MANIFEST = os.path.join(
    REPO_ROOT, "evals", "results", "context-utilization-phase3", "lane_manifest.yaml",
)
DILUTION_EXCLUDED_REASONS = ("not-tool-observable", "raw-set-gap")


class ScorerError(Exception):
    """Lane-specific scoring precondition failure (e.g. a missing
    completeness audit, a malformed audit entry, or an unauthored keyword
    override) — caught in main() and reported cleanly, never a raw
    traceback. Every case this is raised for was previously a silent
    default that biased a registered prediction (gate F1/F5a)."""


# ── I/O ──────────────────────────────────────────────────────────────────

def resolve_repo_path(rel_path):
    """lane_manifest.yaml declares paths repo-relative by convention (see
    its header comment). Resolve them against the repo root — derived from
    this file's own location, never the caller's cwd — so a fixture-id
    lookup behaves the same whether invoked from the repo root, from
    ollama/, or from a subagent with an unrelated cwd. None and already-
    absolute paths pass through unchanged."""
    if rel_path is None or os.path.isabs(rel_path):
        return rel_path
    return os.path.normpath(os.path.join(REPO_ROOT, rel_path))


def load_manifest(path):
    with open(path) as f:
        return yaml.safe_load(f)


def resolve_fixture_config(manifest, fixture_id):
    for entry in manifest.get("fixtures", []):
        if entry["fixture_id"] == fixture_id:
            return entry
    raise ScorerError(f"{fixture_id!r} not found in lane manifest fixtures list")


def load_keyword_overrides(entry_or_doc):
    """Build {item_index: keywords} from a manifest fixture entry OR a
    standalone --keywords-file document — both use the same
    `must_find_keywords: [{item_index, keywords}]` shape (gate F1 fix)."""
    return {kw["item_index"]: kw["keywords"]
            for kw in (entry_or_doc or {}).get("must_find_keywords", [])}


def load_completeness_audit(path):
    """Load a fixture's committed completeness audit (README §10 shape,
    gate F4 revision: {items: [{item_index, tool_observable,
    evidence_in_raw_set, in_curated_pack, raw_handle}]}). Returns None if
    the file doesn't exist yet — real (non-selftest) scoring of a non-CLEAN
    fixture must not silently treat None as "no omissions"; score_row
    raises unless allow_unaudited is explicitly set."""
    if not path or not os.path.exists(path):
        return None
    with open(path) as f:
        data = yaml.safe_load(f)
    return {item["item_index"]: item for item in data.get("items", [])}


# ── must-find matching (gate F1) ────────────────────────────────────────

def flatten_must_find_items(metadata):
    """Flatten expected_findings into a flat, index-stable must_find list.
    Index order matches iteration order elsewhere in this repo's scorers
    (score_output.py's own expected_findings loop) so completeness-audit
    and must_find_keywords item_index values line up with what a human
    authored by hand."""
    items = []
    for cat in metadata.get("expected_findings", []):
        if cat.get("category") != "must_find":
            continue
        items.extend(cat.get("items", []))
    return items


def find_evidence_quote(text, keywords, max_chars=200):
    """First response line containing any keyword, truncated — the
    adjudication-ready quote a human/opus checks against the item
    description. None if no line matches (should not happen when the
    caller already knows result['found'] is True)."""
    for line in text.splitlines():
        norm_line = normalize_quotes(line.lower())
        if any(normalize_quotes(kw.lower()) in norm_line for kw in keywords):
            stripped = line.strip()
            if len(stripped) > max_chars:
                return stripped[:max_chars] + "…"
            return stripped
    return None


def match_must_find_item(text, item, keywords):
    """Match against EXPLICIT keyword overrides only — never
    check_finding's branch cascade (gate F1). Case-insensitive,
    quote-normalized substring search."""
    description = item.get("description", "")
    wcag = item.get("wcag", "")
    norm_text = normalize_quotes(text.lower())
    found = any(normalize_quotes(kw.lower()) in norm_text for kw in keywords)
    wcag_cited = False
    m = re.search(r"(\d+\.\d+\.\d+)", wcag) if wcag else None
    if m:
        wcag_cited = m.group(1) in text
    return {"description": description, "found": found,
            "wcag_cited": wcag_cited, "keywords_checked": keywords}


def score_must_find_items(text, metadata, audit, payload, keyword_overrides):
    """Match every must_find item using its required manifest keyword
    override and partition the misses (gate F1 + F4). Raises ScorerError if
    an item has no override — silently falling back to a generic matcher
    would reintroduce the exact ceiling-effect bug F1 exists to close."""
    items = flatten_must_find_items(metadata)
    matched, misses = [], []
    for idx, item in enumerate(items):
        if idx not in keyword_overrides:
            raise ScorerError(
                f"No must_find_keywords override for item_index={idx} "
                f"({item.get('description', '')[:60]!r}). Every must-find "
                "item needs an explicit lane_manifest.yaml override "
                "(gate F1) — there is no generic-matcher fallback.")
        result = match_must_find_item(text, item, keyword_overrides[idx])
        if result["found"]:
            matched.append({
                "item_index": idx, "description": result["description"],
                "found": True,
                "evidence_quote": find_evidence_quote(text, keyword_overrides[idx]),
                "wcag_cited": result["wcag_cited"],
            })
        else:
            misses.append({
                "item_index": idx, "description": result["description"],
                "found": False, "reason": classify_miss(idx, audit, payload),
            })
    return matched, misses, len(items)


def classify_miss(item_index, audit, payload):
    """Partition one missed must-find item (gate F4/F5a — see module
    docstring for the 4 buckets). Every required audit key must be
    explicitly present; a missing item_index or key raises ScorerError
    rather than silently defaulting True/False, which would bias whichever
    registered prediction reads the partition."""
    if audit is None:
        return "unaudited"
    entry = audit.get(item_index)
    if entry is None:
        raise ScorerError(f"Completeness audit has no entry for item_index={item_index}")
    for key in ("tool_observable", "evidence_in_raw_set"):
        if key not in entry:
            raise ScorerError(f"item_index={item_index}: audit missing required key {key!r}")
    if not entry["tool_observable"]:
        return "not-tool-observable"
    if not entry["evidence_in_raw_set"]:
        return "raw-set-gap"
    if payload != "CURATED":
        return "model-miss"
    if "in_curated_pack" not in entry:
        raise ScorerError(
            f"item_index={item_index}: audit missing required key "
            "'in_curated_pack' (CURATED, evidence_in_raw_set=True)")
    return "pack-omission" if not entry["in_curated_pack"] else "model-miss"


def score_clean(text, verdict):
    """CLEAN-fixture scoring. Gate F8: count_false_positives (score_output.py,
    untouched) counts any numbered `Finding N:` regardless of severity, and
    both CLEAN fixtures carry one legitimate nice_to_find ENHANCEMENT each —
    a model correctly reporting it would count as an FP here. Gate's fix is
    documentation-only (README states P3 needs the same adjudication pass);
    print_report never presents this count as a settled verdict."""
    fp = count_false_positives(text, verdict)
    return {
        "applicable": True,
        "correct_verdict": verdict in ("ACCEPT", "ACCEPT-WITH-RESERVATIONS"),
        "structured_findings": fp["structured_findings"],
        "wrong_verdict": fp["wrong_verdict"],
        "fp_count": fp["structured_findings"],
    }


# ── row scoring ──────────────────────────────────────────────────────────

def _base_result(data, bench, condition, payload, draw):
    result = {
        "fixture_id": bench.get("fixture_id"),
        "model": bench.get("model"),
        "condition": condition,
        "payload": payload,
        "draw": draw,
        "prompt_eval_count": bench.get("prompt_eval_count"),
        "done_reason": bench.get("done_reason"),
        "context_pressure": bench.get("context_pressure"),
        # Gate F7: output-side clipping depresses recall and risk rises with
        # prompt size (DUMP arm) — the direction that would falsely confirm
        # P1. Must be checked before trusting this row's recall.
        "output_clipped": bench.get("done_reason") == "length",
        "invalid": None,
    }
    if data.get("invalid") == "context_overflow":
        result.update({
            "invalid": "context_overflow",
            "estimated_prompt_tokens": data.get("estimated_prompt_tokens"),
            "num_ctx": data.get("num_ctx"),
        })
    return result


def _require_scoring_preconditions(tier, completeness_audit_path, audit,
                                    keyword_overrides, allow_unaudited):
    """Fail loud on either missing precondition rather than defaulting
    (gate F1 / F5a philosophy applied at the entry point, not just inside
    classify_miss)."""
    if audit is None and not allow_unaudited:
        raise ScorerError(
            f"No completeness audit at {completeness_audit_path!r} for a {tier} "
            "fixture. Pack freeze requires one committed before any model row "
            "is scored (README.md §10). Pass allow_unaudited=True only for "
            "pre-freeze dry runs."
        )
    if not keyword_overrides:
        raise ScorerError(
            f"No must_find_keywords for a {tier} fixture (gate F1) — pass "
            "--fixture-id with a manifest that has them authored, or "
            "--keywords-file."
        )


def score_row(response_path, metadata_path, condition, payload, *,
              completeness_audit_path=None, keyword_overrides=None,
              draw=None, allow_unaudited=False):
    """Score one model response against one fixture. `keyword_overrides`
    (dict item_index -> keywords) is required for non-CLEAN tiers — gate
    F1. Raises ScorerError if a non-CLEAN fixture has no committed
    completeness audit and the caller did not explicitly opt into
    allow_unaudited (pre-freeze dry runs / calibration only)."""
    with open(response_path) as f:
        data = json.load(f)
    bench = data.get("_benchmark", {})
    base = _base_result(data, bench, condition, payload, draw)
    if base["invalid"]:
        return base

    text, truncated = strip_thinking(data.get("response", ""))
    if truncated:
        base["invalid"] = "truncated_think_block"
        return base

    with open(metadata_path) as f:
        metadata = yaml.safe_load(f)
    tier = metadata.get("difficulty", "unknown")
    base.update({"tier": tier, "verdict": check_verdict(text)})

    if tier == "CLEAN":
        base["false_positives"] = score_clean(text, base["verdict"])
        base["must_find"] = {"total": 0, "matched": [], "matched_count": 0, "recall": None}
        base["misses"] = []
        return base

    audit = load_completeness_audit(completeness_audit_path)
    _require_scoring_preconditions(tier, completeness_audit_path, audit,
                                    keyword_overrides, allow_unaudited)

    matched, misses, total = score_must_find_items(text, metadata, audit, payload, keyword_overrides)
    base["must_find"] = {
        "total": total,
        "matched": matched,
        "matched_count": len(matched),
        "recall": (len(matched) / total) if total else None,
    }
    base["misses"] = misses
    base["false_positives"] = None
    return base


# ── aggregation feed for P1/P1b/P2/P3 (gate F5) ─────────────────────────

def _dilution_eligible_count(row):
    """Count must-find items eligible for the P1/P1b denominator (gate
    F5c): matched items always count; missed items count unless excluded
    (DILUTION_EXCLUDED_REASONS) — those were never findable under either
    pack condition."""
    mf = row.get("must_find") or {}
    eligible = mf.get("matched_count") or 0
    for miss in row.get("misses") or []:
        if miss.get("reason") not in DILUTION_EXCLUDED_REASONS:
            eligible += 1
    return eligible


def aggregate_by_condition(rows):
    """Fold scored rows into per-(model,condition) candidate totals (gate
    F5). Keys by (model, condition) — never condition alone, which would
    pool qwen3:32b into the mix and destroy the control comparison (F5b).
    INVALID rows count per key, not silently dropped (F5c). Still CANDIDATE
    counts — see module docstring."""
    totals = {}
    for row in rows:
        key = (row.get("model"), row.get("condition"))
        agg = totals.setdefault(key, {
            "matched": 0, "possible": 0, "fp": 0, "rows": 0, "invalid_rows": 0,
        })
        agg["rows"] += 1
        if row.get("invalid"):
            agg["invalid_rows"] += 1
            continue
        mf = row.get("must_find") or {}
        agg["matched"] += mf.get("matched_count") or 0
        agg["possible"] += _dilution_eligible_count(row)
        fp = row.get("false_positives")
        if fp and fp.get("applicable"):
            agg["fp"] += fp.get("fp_count") or 0
    return totals


def per_item_rows(rows):
    """Flatten to one record per (model, condition, fixture, item_index) —
    gate F5d, the granularity the plan's per-item flip reporting needs."""
    out = []
    for row in rows:
        if row.get("invalid"):
            continue
        prefix = (row.get("model"), row.get("condition"), row.get("fixture_id"))
        for m in (row.get("must_find") or {}).get("matched", []):
            out.append({"key": prefix + (m["item_index"],), "found": True,
                        "reason": None, "evidence_quote": m.get("evidence_quote")})
        for miss in row.get("misses") or []:
            out.append({"key": prefix + (miss["item_index"],), "found": False,
                        "reason": miss.get("reason"), "evidence_quote": None})
    return out


# ── reporting ────────────────────────────────────────────────────────────

def print_report(result):
    print(f"Fixture: {result.get('fixture_id')} | Model: {result.get('model')}")
    print(f"Condition: {result.get('condition')} ({result.get('payload')}) | Draw: {result.get('draw')}")
    if result.get("invalid"):
        print(f"INVALID: {result['invalid']}")
        if result["invalid"] == "context_overflow":
            print(f"  estimated_prompt_tokens={result.get('estimated_prompt_tokens')} "
                  f"num_ctx={result.get('num_ctx')}")
        print("Status: INVALID")
        return
    print(f"prompt_eval_count={result.get('prompt_eval_count')} "
          f"done_reason={result.get('done_reason')} "
          f"output_clipped={result.get('output_clipped')} "
          f"context_pressure={result.get('context_pressure')}")
    print(f"Tier: {result.get('tier')} | Verdict: {result.get('verdict')}")

    fp = result.get("false_positives")
    if fp and fp.get("applicable"):
        # Gate F8: CLEAN rows report as candidates requiring the same
        # adjudication pass as HAS-BUGS rows, never a bare PASS/FAIL — a
        # correctly-reported nice_to_find ENHANCEMENT is not an FP, and
        # count_false_positives cannot tell the difference on its own.
        print(f"CLEAN fixture — correct_verdict={fp['correct_verdict']} "
              f"candidate_fp_count={fp['fp_count']} (nice_to_find items may "
              f"inflate this — adjudicate before counting as FP, README §9.5/F8)")
        print("Status: SCORED (candidate — content-adjudication required, README §6/§7)")
        return

    mf = result["must_find"]
    print(f"Must-find candidates: {mf['matched_count']}/{mf['total']}")
    for m in mf["matched"]:
        print(f"  + [{m['item_index']}] {m['description'][:70]} — {m['evidence_quote']!r}")
    for m in result["misses"]:
        print(f"  X [{m['item_index']}] {m['description'][:70]} — reason={m['reason']}")
    print("Status: SCORED (candidate matches — content-adjudication required, README §6/§7)")


# ── selftest ─────────────────────────────────────────────────────────────

SELFTEST_METADATA = {
    "fixture_id": "selftest-fixture",
    "difficulty": "HAS-BUGS",
    "expected_findings": [
        {"category": "must_find", "items": [
            {"description": "Missing aria-describedby on error field",
             "severity": "CRITICAL", "wcag": "4.1.2 Name, Role, Value"},
            {"description": "Missing fieldset to group related radios",
             "severity": "CRITICAL", "wcag": "1.3.1 Info and Relationships"},
        ]},
    ],
}

SELFTEST_CLEAN_METADATA = {
    "fixture_id": "selftest-clean-fixture",
    "difficulty": "CLEAN",
    "expected_findings": [{"category": "must_find", "items": []}],
}

SELFTEST_KEYWORDS = {
    "must_find_keywords": [
        {"item_index": 0, "keywords": ["aria-describedby", "describedby"]},
        {"item_index": 1, "keywords": ["fieldset", "legend"]},
    ],
}

# item 0: tool-observable, in raw set, curated omitted it -> pack-omission
# under CURATED. item 1: not tool-observable at all (source-only defect).
SELFTEST_AUDIT = {
    "items": [
        {"item_index": 0, "tool_observable": True, "evidence_in_raw_set": True,
         "in_curated_pack": False, "raw_handle": "selftest: synthetic axe row"},
        {"item_index": 1, "tool_observable": False, "evidence_in_raw_set": False,
         "raw_handle": "selftest: source-only, no tool could see it"},
    ],
}

# A third, malformed entry for the F5a malformed-audit selftest: present,
# but missing the required evidence_in_raw_set key.
SELFTEST_AUDIT_MALFORMED = {
    "items": [{"item_index": 0, "tool_observable": True,
               "raw_handle": "selftest: missing evidence_in_raw_set"}],
}


def _write_json(dirpath, name, data):
    path = os.path.join(dirpath, name)
    with open(path, "w") as f:
        json.dump(data, f)
    return path


def _write_yaml(dirpath, name, data):
    path = os.path.join(dirpath, name)
    with open(path, "w") as f:
        yaml.safe_dump(data, f)
    return path


def _selftest_response(response_text, done_reason="stop"):
    return {
        "response": response_text,
        "_benchmark": {
            "model": "selftest-model",
            "fixture_id": "selftest-fixture",
            "prompt_eval_count": 12345,
            "done_reason": done_reason,
            "context_pressure": False,
        },
    }


def _check(label, cond):
    print(f"  {'+' if cond else 'X'} {label}")
    return bool(cond)


def _selftest_miss_partition(tmp, metadata_path, audit_path):
    """R1/R2: the same all-missed response scored under CURATED vs DUMP —
    proves pack-omission is CURATED-only and not-tool-observable is
    payload-independent (gate F4's raw-set-gap bucket is exercised
    separately in _selftest_raw_set_gap, below)."""
    miss_both = _write_json(tmp, "miss_both.json", _selftest_response(
        "## Review\n\nNo issues found in this component.\n"))
    r1 = score_row(miss_both, metadata_path, "curated-32k", "CURATED",
                    completeness_audit_path=audit_path,
                    keyword_overrides=load_keyword_overrides(SELFTEST_KEYWORDS), draw=1)
    ok = _check("R1 (CURATED, both missed) item0 -> pack-omission",
                r1["misses"][0]["reason"] == "pack-omission")
    ok &= _check("R1 item1 -> not-tool-observable",
                 r1["misses"][1]["reason"] == "not-tool-observable")

    r2 = score_row(miss_both, metadata_path, "dump-40k", "DUMP",
                    completeness_audit_path=audit_path,
                    keyword_overrides=load_keyword_overrides(SELFTEST_KEYWORDS), draw=1)
    ok &= _check("R2 (DUMP, both missed) item0 -> model-miss (never omission under DUMP)",
                 r2["misses"][0]["reason"] == "model-miss")
    ok &= _check("R2 item1 -> not-tool-observable regardless of payload",
                 r2["misses"][1]["reason"] == "not-tool-observable")
    return ok, r1, r2, miss_both


def _selftest_match_and_clean(tmp, metadata_path, audit_path):
    """R3: a response that actually mentions one item gets a quoted match.
    R4: a genuinely clean response scores fp_count 0 on a CLEAN fixture."""
    found_text = "The input is missing aria-describedby linking it to the visible error text."
    found_resp = _write_json(tmp, "found.json", _selftest_response(found_text))
    r3 = score_row(found_resp, metadata_path, "curated-40k", "CURATED",
                    completeness_audit_path=audit_path,
                    keyword_overrides=load_keyword_overrides(SELFTEST_KEYWORDS), draw=1)
    ok = _check("R3 item0 found with a non-empty evidence quote",
                bool(r3["must_find"]["matched"])
                and bool(r3["must_find"]["matched"][0]["evidence_quote"]))
    ok &= _check("R3 item1 still missed -> not-tool-observable",
                 bool(r3["misses"]) and r3["misses"][0]["reason"] == "not-tool-observable")

    clean_text = "## Review\n\nVerdict: ACCEPT\n\nNo accessibility issues found. Implementation is complete."
    clean_resp = _write_json(tmp, "clean.json", _selftest_response(clean_text))
    r4 = score_row(clean_resp, _write_yaml(tmp, "clean.yaml", SELFTEST_CLEAN_METADATA),
                    "curated-32k", "CURATED", draw=1)
    ok &= _check("R4 CLEAN correct verdict, fp_count 0",
                 r4["false_positives"]["correct_verdict"] and r4["false_positives"]["fp_count"] == 0)
    return ok, r3


def _selftest_invalid_and_guards(tmp, metadata_path, audit_path, miss_both):
    """R5: context_overflow rows pass through unscored. Plus: a missing
    audit fails loud (unless allow_unaudited), and missing keyword
    overrides fails loud (gate F1)."""
    invalid_resp = _write_json(tmp, "invalid.json", {
        "invalid": "context_overflow",
        "estimated_prompt_tokens": 40000,
        "num_ctx": 32768,
        "_benchmark": {"model": "qwen3:32b", "fixture_id": "selftest-fixture"},
    })
    r5 = score_row(invalid_resp, metadata_path, "overflow-32k", "DUMP", draw=1)
    ok = _check("R5 context_overflow row passes through as INVALID, unscored",
                r5["invalid"] == "context_overflow" and "must_find" not in r5)

    unaudited_error = False
    try:
        score_row(miss_both, metadata_path, "curated-32k", "CURATED",
                  keyword_overrides=load_keyword_overrides(SELFTEST_KEYWORDS), draw=1)
    except ScorerError:
        unaudited_error = True
    ok &= _check("Missing completeness audit raises ScorerError (fail loud, not silent)",
                 unaudited_error)

    no_keywords_error = False
    try:
        score_row(miss_both, metadata_path, "curated-32k", "CURATED",
                  completeness_audit_path=audit_path, draw=1)
    except ScorerError:
        no_keywords_error = True
    ok &= _check("Missing must_find_keywords raises ScorerError (gate F1, fail loud)",
                 no_keywords_error)
    return ok


def _selftest_malformed_audit_and_raw_set_gap(tmp, metadata_path):
    """Gate F5a: a real selftest exercise of a malformed audit entry
    (present item_index, missing a required key) -> ScorerError, not a
    silent default. Also proves the raw-set-gap bucket (gate F4) fires
    when evidence_in_raw_set is explicitly False."""
    malformed_path = _write_yaml(tmp, "malformed_audit.yaml", SELFTEST_AUDIT_MALFORMED)
    malformed_error = False
    try:
        classify_miss(0, load_completeness_audit(malformed_path), "CURATED")
    except ScorerError:
        malformed_error = True
    ok = _check("Malformed audit entry (missing evidence_in_raw_set) raises ScorerError",
                malformed_error)

    raw_set_gap_audit = {"items": [
        {"item_index": 0, "tool_observable": True, "evidence_in_raw_set": False,
         "raw_handle": "selftest: tool-observable but never collected for this fixture"},
    ]}
    gap_path = _write_yaml(tmp, "raw_set_gap_audit.yaml", raw_set_gap_audit)
    reason = classify_miss(0, load_completeness_audit(gap_path), "CURATED")
    ok &= _check("evidence_in_raw_set=False -> raw-set-gap (gate F4)", reason == "raw-set-gap")
    return ok


def _selftest_per_model_aggregation():
    """Gate F5b: two rows, same condition, different models, must land in
    two separate (model, condition) buckets — never pooled."""
    row_a = {"model": "qwen3.6:35b", "condition": "curated-32k", "invalid": None,
             "must_find": {"matched_count": 2, "total": 2}, "misses": []}
    row_b = {"model": "qwen3:32b", "condition": "curated-32k", "invalid": None,
             "must_find": {"matched_count": 1, "total": 2},
             "misses": [{"item_index": 1, "reason": "model-miss"}]}
    agg = aggregate_by_condition([row_a, row_b])
    ok = _check("Two models, same condition -> two separate aggregate buckets",
                len(agg) == 2 and ("qwen3.6:35b", "curated-32k") in agg
                and ("qwen3:32b", "curated-32k") in agg)
    ok &= _check("qwen3.6:35b bucket unaffected by qwen3:32b's row",
                 agg[("qwen3.6:35b", "curated-32k")]["matched"] == 2)
    return ok


def _selftest_output_clipped(tmp, metadata_path, audit_path):
    """Gate F7: done_reason == 'length' must set output_clipped True; a
    normal 'stop' completion must not."""
    clipped_resp = _write_json(tmp, "clipped.json",
                                _selftest_response("Partial respo", done_reason="length"))
    r_clipped = score_row(clipped_resp, metadata_path, "dump-40k", "DUMP",
                           completeness_audit_path=audit_path,
                           keyword_overrides=load_keyword_overrides(SELFTEST_KEYWORDS), draw=1)
    ok = _check("done_reason=length -> output_clipped True", r_clipped["output_clipped"] is True)

    clean_resp = _write_json(tmp, "not_clipped.json",
                              _selftest_response("Complete response.", done_reason="stop"))
    r_clean = score_row(clean_resp, metadata_path, "dump-40k", "DUMP",
                         completeness_audit_path=audit_path,
                         keyword_overrides=load_keyword_overrides(SELFTEST_KEYWORDS), draw=1)
    ok &= _check("done_reason=stop -> output_clipped False", r_clean["output_clipped"] is False)
    return ok


# The 4 buggy fixtures' real metadata (gate F1 calibration: null response
# must score all 9 False). Listed for legibility; keywords still come only
# from the manifest, never duplicated here.
REAL_BUGGY_FIXTURE_IDS = [
    "heading-hierarchy-skipped", "file-input-no-labels",
    "tabs-missing-arrow-nav", "interactive-dropdown-focus-bug",
]


def _selftest_real_fixture_calibration():
    """Gate F1 calibration, run against the REAL 9 must-finds and REAL
    lane_manifest.yaml keyword overrides (not synthetic data) — a
    null/no-issues response must score False on every one of them. This is
    the check that would have caught the original ceiling-effect bug."""
    manifest = load_manifest(DEFAULT_MANIFEST)
    null_text = "## Review\n\nVerdict: ACCEPT\n\nNo accessibility issues found in this component.\n"
    total_items, total_false = 0, 0
    for fixture_id in REAL_BUGGY_FIXTURE_IDS:
        entry = resolve_fixture_config(manifest, fixture_id)
        keywords = load_keyword_overrides(entry)
        with open(resolve_repo_path(entry["metadata_path"])) as f:
            metadata = yaml.safe_load(f)
        matched, misses, total = score_must_find_items(null_text, metadata, None, "CURATED", keywords)
        total_items += total
        total_false += len(misses)
        if not _check(f"{fixture_id}: {len(misses)}/{total} score False on null response",
                       len(matched) == 0):
            for m in matched:
                print(f"      FALSE POSITIVE: item {m['item_index']} {m['description'][:60]!r} "
                      f"matched keywords {keywords.get(m['item_index'])}")
    return _check(f"Real-fixture calibration: {total_false}/{total_items} must-finds score False "
                  "on a null response (gate F1)", total_false == total_items and total_items == 9)


def selftest():
    """Prove the matching + partition logic with synthetic rows, then
    calibrate the real per-item keyword overrides against the real 9
    must-finds (gate F1's own calibration requirement). Synthetic data is
    for the partition-logic proof ONLY — real scoring always reads
    committed pack artifacts (README.md 'Pack freeze' protocol forbids
    synthetic evidence in real packs)."""
    print("=== score_evidence_lane.py selftest ===\n")
    with tempfile.TemporaryDirectory() as tmp:
        metadata_path = _write_yaml(tmp, "metadata.yaml", SELFTEST_METADATA)
        audit_path = _write_yaml(tmp, "audit.yaml", SELFTEST_AUDIT)

        ok1, r1, r2, miss_both = _selftest_miss_partition(tmp, metadata_path, audit_path)
        ok2, r3 = _selftest_match_and_clean(tmp, metadata_path, audit_path)
        ok3 = _selftest_invalid_and_guards(tmp, metadata_path, audit_path, miss_both)
        ok4 = _selftest_malformed_audit_and_raw_set_gap(tmp, metadata_path)
        ok5 = _selftest_per_model_aggregation()
        ok6 = _selftest_output_clipped(tmp, metadata_path, audit_path)

        agg = aggregate_by_condition([r1, r2, r3])
        ok7 = _check("aggregate_by_condition groups by (model, condition)",
                     set(agg) == {("selftest-model", "curated-32k"),
                                  ("selftest-model", "dump-40k"),
                                  ("selftest-model", "curated-40k")})

    print()
    ok8 = _selftest_real_fixture_calibration()

    ok = ok1 and ok2 and ok3 and ok4 and ok5 and ok6 and ok7 and ok8
    print(f"\nSelftest: {'ALL PASS' if ok else 'FAILURES ABOVE'}")
    return ok


# ── CLI ──────────────────────────────────────────────────────────────────

def build_arg_parser():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("response", nargs="?", help="Path to the model response JSON")
    p.add_argument("--manifest", default=DEFAULT_MANIFEST)
    p.add_argument("--fixture-id", help="Resolve --metadata/--completeness-audit/keywords from the manifest")
    p.add_argument("--metadata", help="Override/replace the manifest-resolved metadata path")
    p.add_argument("--completeness-audit", help="Override/replace the manifest-resolved audit path")
    p.add_argument("--keywords-file", help="Standalone must_find_keywords YAML (non-manifest usage)")
    p.add_argument("--condition", help="Cell id, e.g. curated-32k (see lane_manifest.yaml)")
    p.add_argument("--payload", choices=["CURATED", "DUMP"])
    p.add_argument("--draw", type=int)
    p.add_argument("--allow-unaudited", action="store_true",
                    help="Score against a fixture with no committed completeness audit "
                         "yet (pre-freeze dry runs only)")
    p.add_argument("--selftest", action="store_true",
                    help="Run the synthetic + real-fixture-calibration proof and exit")
    return p


def _resolve_scoring_inputs(args):
    """Resolve metadata/audit/keyword paths from --fixture-id + manifest,
    falling back to explicit overrides. Returns (metadata_path, audit_path,
    keyword_overrides)."""
    metadata_path, audit_path, keywords = args.metadata, args.completeness_audit, None
    if args.fixture_id:
        entry = resolve_fixture_config(load_manifest(args.manifest), args.fixture_id)
        metadata_path = metadata_path or resolve_repo_path(entry["metadata_path"])
        audit_path = audit_path or resolve_repo_path(entry.get("completeness_audit_path"))
        keywords = load_keyword_overrides(entry)
    if args.keywords_file:
        with open(args.keywords_file) as f:
            keywords = load_keyword_overrides(yaml.safe_load(f))
    return metadata_path, audit_path, keywords


def main():
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.selftest:
        sys.exit(0 if selftest() else 1)

    if not args.response:
        parser.error("response path is required outside --selftest")
    if not args.condition or not args.payload:
        parser.error("--condition and --payload are required outside --selftest")

    metadata_path, audit_path, keywords = _resolve_scoring_inputs(args)
    if not metadata_path:
        parser.error("--metadata or --fixture-id (with --manifest) is required")

    try:
        result = score_row(
            args.response, metadata_path, args.condition, args.payload,
            completeness_audit_path=audit_path, keyword_overrides=keywords,
            draw=args.draw, allow_unaudited=args.allow_unaudited,
        )
    except ScorerError as e:
        sys.exit(f"ERROR: {e}")

    print_report(result)
    print()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
