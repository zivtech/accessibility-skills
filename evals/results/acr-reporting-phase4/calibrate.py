#!/usr/bin/env python3
"""Synthetic calibration for the acr-reporting Lane C path (integration
plan Phase 4, docs/plans/2026-08-12-openacr-phase4-handoff.md Part 1) —
run BEFORE any model row, per house practice.

Builds synthetic drift reports in-memory — honest reports derived from each
fixture's metadata (so metadata self-consistency is itself under
calibration) plus trend-flipping, boundary-breaking, dramatizing and
shoulds-missed mutants — scores each with the real `ollama/score_acr.py`
lane C path, and asserts the expected status and check lines. Exit 0 =
CLEAN. Like lane B, this path needs no CLI: the deliverable is a Markdown
drift report, not an OpenACR document.

Usage:
    python3 evals/results/acr-reporting-phase4/calibrate.py [--dump]
"""

import json
import os
import re
import subprocess
import sys
import tempfile

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FIXTURES = os.path.join(REPO, "evals", "suites", "acr-reporting", "fixtures")
SCORER = os.path.join(REPO, "ollama", "score_acr.py")

SELF_FIXTURE = "transit-portal-drift-self"
FOREIGN_FIXTURE = "shiftline-drift-foreign"


def load_meta(fixture_id):
    with open(os.path.join(FIXTURES, f"{fixture_id}.metadata.yaml")) as f:
        return yaml.safe_load(f)


# ── honest reports, derived from metadata ────────────────────────────────

DELTA_HEAD = ["| SC | Prior term | Current term | Delta | Comparable? | "
              "Evidence |",
              "|----|-----------|--------------|-------|-------------|"
              "----------|"]


def build_honest_self(meta):
    deltas = {str(k): v for k, v in meta["expected_sc_deltas"].items()}
    trends = meta["expected_trends"]
    fps = meta["trend_fingerprints"]
    scs = meta["trend_scs"]
    noncomp = {str(k): v for k, v in (meta.get("noncomparable_scs")
                                      or {}).items()}
    by_sc = {str(v): k for k, v in scs.items()}

    out = ["# Drift report — RiverCity Metro Rider Portal, rcm-2026q3 → "
           "rcm-2027q1", "",
           "## Comparability (WCAG-EM re-evaluation)", "",
           "Carried over from the prior cycle and common to both: S01, S02, "
           "S03, S06, S07, S08, S11, and both complete processes. Retired: "
           "S04, S05, S09, S10, R01. Added this cycle: S12, S13, S14, S15, "
           "R02. A delta resting only on an added sample is a coverage "
           "change, not movement, and is marked below.", "",
           "## SC-level deltas", ""] + list(DELTA_HEAD)

    for sc, spec in deltas.items():
        fid = by_sc.get(sc, "")
        if sc in noncomp:
            comp = ("no — S14 station detail is a new template with no "
                    "prior counterpart")
        else:
            comp = "yes — the failing sample is carried over"
        direction = ("newly passing" if spec["current"] == "supports"
                     else "newly failing" if spec["prior"] == "supports"
                     else "still failing, term moved")
        out.append(f"| {sc} | {spec['prior']} | {spec['current']} | "
                   f"{direction} | {comp} | {fid} |")

    unchanged = meta.get("unchanged_scs") or []
    out += ["",
            f"Unchanged: 50 criteria carry identical terms in both "
            f"documents, among them {', '.join(unchanged)}. They are "
            f"reported here as unchanged and nowhere else.", "",
            "## Finding-level trend", "",
            "| finding_id | fingerprint | SC | Prior | Current | Trend | "
            "Evidence |",
            "|---|---|---|---|---|---|---|"]

    ev = {
        "resolved": "verified absent in the current cycle's re-check",
        "persistent": "still present, materially unchanged in scope and "
                      "severity",
        "improving": "still present on a smaller surface; the fingerprint "
                     "is still on the ledger, so this is not a retirement",
        "worsening": "still present on a larger surface, severity raised",
        "new": "first observed this cycle, on a template with no prior "
               "counterpart",
    }
    for fid, trend in trends.items():
        sc = scs[fid]
        spec = deltas.get(sc)
        prior = spec["prior"] if spec else "partially-supports"
        cur = spec["current"] if spec else "partially-supports"
        out.append(f"| {fid} | {fps[fid]} | {sc} | {prior} | {cur} | "
                   f"{trend} | {ev[trend]} |")

    counts = {}
    for t in trends.values():
        counts[t] = counts.get(t, 0) + 1
    out += ["", "## Summary", "",
            ", ".join(f"{n} {t}" for t, n in sorted(counts.items()))
            + ". Every delta above is sample-scoped: the two documents rest "
              "on two sample sets drawn one release apart, and this report "
              "describes movement on the sampled surface, never a "
              "whole-product conformance claim.", "",
            "## Handoff", "",
            "a11y-critic adjudicates every resolved row against the current "
            "cycle's verified-absent evidence before delivery. The "
            "Authority's engagement owner reviews the report and owns any "
            "decision to publish a revised ACR."]
    return "\n".join(out)


def build_honest_foreign(meta):
    deltas = {str(k): v for k, v in meta["expected_sc_deltas"].items()}
    absent = {str(k): v for k, v in (meta.get("absent_rows") or {}).items()}
    unchanged = meta.get("unchanged_scs") or []

    out = ["# Drift report — ShiftLine Workforce Scheduling, vendor ACR 9.3 "
           "→ 9.6", "",
           "Both documents were written by the vendor. No evaluation of "
           "v9.6 has been commissioned: nothing below was verified, and a "
           "rewritten term is a claim the vendor makes, not measured "
           "evidence.", "",
           "## Term-level deltas", "",
           "| SC | v9.3 claim | v9.6 claim | Delta | Evidence |",
           "|----|-----------|-----------|-------|----------|"]

    labels = {("supports", "partially-supports"): "claim weakened",
              ("partially-supports", "supports"): "claim strengthened",
              ("not-evaluated", "supports"): "claim replaced"}
    for sc, spec in deltas.items():
        note = "unverified at this engagement"
        if sc == "3.1.2":
            note = ("unverified; the v9.3 term was not-evaluated, which the "
                    "catalog reserves for Level AAA criteria — an illegal "
                    "claim on a Level AA row")
        out.append(f"| {sc} | {spec['prior']} | {spec['current']} | "
                   f"{labels.get((spec['prior'], spec['current']), 'changed')}"
                   f" | {note} |")
    for sc in absent:
        out.append(f"| {sc} | not-applicable | (no row) | claim withdrawn — "
                   f"the criterion is absent from the v9.6 document | "
                   f"unverified |")

    out += ["",
            f"Unchanged: 51 criteria carry identical terms in both "
            f"documents, among them {', '.join(unchanged)}. 2.1.1 had its "
            f"note text edited while its term stayed put; a note edit is "
            f"not a term delta.", "",
            "## What this report is not", "",
            "This pair is foreign: the city holds no fingerprints for "
            "either document, so no comparison history exists and the "
            "evidence contract's trend vocabulary is out of scope here. "
            "Term-level deltas are the whole of what two vendor documents "
            "can support.", "",
            "## Routing", "",
            "Turning any claim change above into evidence takes a "
            "verification engagement — Lane B claims verification against a "
            "WCAG-EM sample of v9.6. Nothing routes to bug-reporting: "
            "nothing was verified, so there is nothing to file.", "",
            "## Summary", "",
            "Four criteria changed term and one claim was withdrawn; 51 are "
            "unchanged.", "",
            "## Handoff", "",
            "The procurement owner owns the renewal decision and every "
            "statement made to the vendor; this is a document diff for "
            "human review."]
    return "\n".join(out)


def score(response_text, fixture_id):
    with tempfile.NamedTemporaryFile("w", suffix=".json",
                                     delete=False) as tf:
        json.dump({"response": response_text}, tf)
        path = tf.name
    try:
        proc = subprocess.run(
            [sys.executable, SCORER, path,
             os.path.join(FIXTURES, f"{fixture_id}.metadata.yaml")],
            capture_output=True, text=True, timeout=120)
        return proc.stdout + proc.stderr
    finally:
        os.unlink(path)


def swap_cell(text, key, old, new):
    """Replace a cell value on the table row naming `key`."""
    out = []
    for l in text.splitlines():
        if l.startswith(f"| {key} |") and f"| {old} |" in l:
            l = l.replace(f"| {old} |", f"| {new} |")
        out.append(l)
    return "\n".join(out)


CASES = []


def case(name, fixture_id, expect_status, expect_lines=()):
    def wrap(fn):
        CASES.append((name, fixture_id, expect_status, expect_lines, fn))
        return fn
    return wrap


# ── fixture 6 (self-produced pair) ───────────────────────────────────────

@case("f6-honest", SELF_FIXTURE, "PASS", (
    "SC deltas: 6/6", "Finding trend: 8/8", "0 dramatized"))
def f6_honest(text, meta):
    return text


@case("f6-trap-taker", SELF_FIXTURE, "FAIL", (
    "trend: a11y_form_autocomplete_missing: resolved (expected improving)",
    "trend: a11y_legacy_skiplink_anchor: new (expected worsening)",
    "a11y_route_badge_contrast trend row does not cite its fingerprint",
    "invented finding_id: a11y_phantom_regression",
    "invented fingerprint: aa11bb22",
))
def f6_trap(text, meta):
    # Both discrimination traps taken the tempting way: a term that moved
    # up read as a retirement, a term that moved down read as a fresh find.
    text = swap_cell(text, "a11y_form_autocomplete_missing", "improving",
                     "resolved")
    text = swap_cell(text, "a11y_legacy_skiplink_anchor", "worsening", "new")
    text = swap_cell(text, "a11y_route_badge_contrast", "2ab9d871", "n/a")
    return text + ("\n\n| a11y_phantom_regression | aa11bb22 | 2.4.5 | "
                   "supports | partially-supports | new | inferred |")


@case("f6-dramatizer", SELF_FIXTURE, "FAIL", (
    "criterion identical in both documents tabled as a term change — 2.4.7",
    "whole-product improvement claim",
))
def f6_dramatize(text, meta):
    text = text.replace(
        "## Summary",
        "| 2.4.7 | supports | partially-supports | newly failing | yes | "
        "focus indicator drift |\n\n## Summary")
    return text.replace(
        "Every delta above is sample-scoped",
        "Overall accessibility improved this cycle. Every delta above is "
        "sample-scoped")


@case("f6-comparability-dropper", SELF_FIXTURE, "FAIL", (
    "2.4.11: delta resting on a sample with no prior-cycle counterpart",
    "comparability statement misses all of",
))
def f6_comp(text, meta):
    # The caveat must go from EVERY line naming the criterion — the check is
    # line-scoped over all of them, so a caveat carried on the trend row is
    # still a caveat (calibration finding, 2026-08-13).
    text = text.replace(
        "no — S14 station detail is a new template with no prior counterpart",
        "yes")
    text = text.replace("first observed this cycle, on a template with no "
                        "prior counterpart", "first observed this cycle")
    start = text.index("## Comparability")
    end = text.index("## SC-level deltas")
    return text[:start] + text[end:]


@case("f6-shoulds-missed", SELF_FIXTURE, "WARN", (
    "summary misses all of", "handoff misses all of"))
def f6_warn(text, meta):
    # Drops the per-verdict counts and the handoff while KEEPING the
    # sample-scope sentence — a should-tier miss must not take a must with it.
    text = text.replace("3 resolved", "several resolved")
    text = text.replace("1 worsening", "a worsening")
    return text[:text.index("## Handoff")]


# ── fixture 6b (foreign pair) ────────────────────────────────────────────

@case("f6b-honest", FOREIGN_FIXTURE, "PASS", (
    "SC deltas: 4/4", "0 dramatized", "0 invented"))
def f6b_honest(text, meta):
    return text


@case("f6b-honest-rule-quote", FOREIGN_FIXTURE, "PASS", ("SC deltas: 4/4",))
def f6b_rule_quote(text, meta):
    # Lane B precedent probe carried into lane C: QUOTING the boundary rule
    # is compliance, and the negation-aware scan must not fire on it.
    return text + ("\n\nBoundary: trend vocabulary "
                   "(persistent/worsening/improving/resolved) requires our "
                   "own prior fingerprints and is forbidden against a "
                   "foreign pair.")


@case("f6b-trend-leaker", FOREIGN_FIXTURE, "FAIL", (
    "trend vocabulary against a foreign pair: 'resolved'",
    "no claim-change framing",
))
def f6b_leak(text, meta):
    # Reads the vendor's own document as evidence: the claim-not-verified
    # framing goes from the intro, from the boundary section, AND from the
    # per-row evidence cells — leaving it on the rows is still framing
    # (calibration finding, 2026-08-13).
    start = text.index("## What this report is not")
    end = text.index("## Routing")
    text = text[:start] + text[end:]
    text = text.replace(
        "Both documents were written by the vendor. No evaluation of v9.6 "
        "has been commissioned: nothing below was verified, and a "
        "rewritten term is a claim the vendor makes, not measured "
        "evidence.", "The vendor shipped fixes across three releases.")
    text = text.replace("unverified", "n/a")
    return text + ("\n\nThe schedule-grid focus indicator defect disclosed "
                   "in 9.3 is resolved as of 9.5.")


@case("f6b-absence-misser", FOREIGN_FIXTURE, "FAIL", (
    "1.2.2: claim present in the prior document and absent",
    "invented finding_id: a11y_dashboard_contrast",
))
def f6b_absence(text, meta):
    text = "\n".join(l for l in text.splitlines()
                     if not l.startswith("| 1.2.2 |"))
    text = text.replace("the criterion is absent from the v9.6 document", "")
    return text.replace("| unverified at this engagement |",
                        "| a11y_dashboard_contrast |", 1)


@case("f6b-shoulds-missed", FOREIGN_FIXTURE, "WARN", (
    "3.1.2: prior-document claim-hygiene note absent",
    "summary misses all of",
))
def f6b_warn(text, meta):
    text = text.replace(
        "unverified; the v9.3 term was not-evaluated, which the catalog "
        "reserves for Level AAA criteria — an illegal claim on a Level AA "
        "row", "unverified at this engagement")
    return text.replace("Four criteria changed term and one claim was "
                        "withdrawn; 51 are unchanged.",
                        "Several rows moved.")


BUILDERS = {SELF_FIXTURE: build_honest_self,
            FOREIGN_FIXTURE: build_honest_foreign}


def main():
    dump = "--dump" in sys.argv
    failures = 0
    for name, fixture_id, expect_status, expect_lines, fn in CASES:
        meta = load_meta(fixture_id)
        text = fn(BUILDERS[fixture_id](meta), meta)
        out = score(text, fixture_id)
        m = re.search(r"Status: (\w+)", out)
        status = m.group(1) if m else "NONE"
        ok = status == expect_status
        missing = [l for l in expect_lines if l not in out]
        if missing:
            ok = False
        if dump:
            with open(os.path.join(HERE, f"score-cal-{name}.txt"), "w") as f:
                f.write(out)
        print(f"{'CLEAN' if ok else 'DEFECT'}  {name}: {status} "
              f"(expected {expect_status})"
              + (f" — missing lines: {missing}" if missing else ""))
        if not ok:
            failures += 1
            print("---- scorer output ----")
            print(out)
            print("-----------------------")
    print(f"\n{len(CASES) - failures}/{len(CASES)} calibration cases CLEAN")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
