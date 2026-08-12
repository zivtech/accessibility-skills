#!/usr/bin/env python3
"""Synthetic calibration for the acr-reporting Lane B path (integration
plan Phase 3) — run BEFORE any model row, per house practice.

Builds synthetic claims-delta reports in-memory — honest reports derived
from each fixture's metadata (metadata self-consistency under test) plus
verdict-flipping, boundary-breaking, and shoulds-missed mutants — scores
each with the real `ollama/score_acr.py` lane B path, and asserts the
expected status and check lines. Exit 0 = CLEAN. The lane B path needs no
CLI (the deliverable is Markdown, not an OpenACR document).

Usage:
    python3 evals/results/acr-reporting-phase3/calibrate.py [--dump]
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


def load_meta(fixture_id):
    with open(os.path.join(FIXTURES, f"{fixture_id}.metadata.yaml")) as f:
        return yaml.safe_load(f)


def build_honest_delta(meta):
    """Derive the honest claims-delta report from the metadata."""
    expected = {str(k): v for k, v in meta["expected_verdicts"].items()}
    cites = {str(k): v for k, v in
             (meta.get("verdict_citations") or {}).items()}
    hygiene = {str(k): v for k, v in (meta.get("hygiene_must") or {}).items()}
    unver = {str(k): v for k, v in
             (meta.get("unverifiable_reasons") or {}).items()}
    na_note = {str(k): v for k, v in
               (meta.get("na_note_should") or {}).items()}

    rows = ["| SC | Claimed | Observed (this scope) | Verdict | Evidence |",
            "|----|---------|-----------------------|---------|----------|"]
    counts = {}
    for sc, verdict in expected.items():
        counts[verdict] = counts.get(verdict, 0) + 1
        ev = []
        if sc in cites:
            ev.append(", ".join(cites[sc]))
        if sc in hygiene:
            ev.append("claim-hygiene: not-evaluated is reserved for Level "
                      "AAA — an illegal claim on an AA criterion")
        if sc in unver:
            ev.append("SSO sign-in enclave excluded by the commissioner — "
                      "untested at this scope")
        if sc in na_note:
            ev.append("classification note: the claimed content type does "
                      "exist (media exists in the sample); the NA reasoning "
                      "is wrong while the conformance content holds")
        rows.append(f"| {sc} | (claimed term) | (observed would-be term) | "
                    f"{verdict} | {'; '.join(ev) or '—'} |")

    summary = ("\n\nSummary: "
               + ", ".join(f"{n} {v}" for v, n in sorted(counts.items()))
               + " — all verdicts scoped to the verification sample set, "
                 "never a whole-product conclusion.")
    routing = ("\n\nOverstated claims route into bug-reporting for filable "
               "issues." if any(v == "overstated" for v in expected.values())
               else "\n\nNo overstated claims; nothing routes to "
                    "bug-reporting this cycle.")
    handoff = ("\n\n## Handoff\n\na11y-critic adjudicates every "
               "non-confirmed verdict against the evidence before delivery; "
               "the procurement owner reviews and owns every statement made "
               "to the vendor.")
    return "\n".join(rows) + summary + routing + handoff


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


def swap_verdict(text, sc, new):
    out = []
    for l in text.splitlines():
        if l.startswith(f"| {sc} |"):
            for v in ("confirmed", "overstated", "understated",
                      "unverifiable-at-this-scope"):
                l = l.replace(f"| {v} |", f"| {new} |")
        out.append(l)
    return "\n".join(out)


CASES = []


def case(name, fixture_id, expect_status, expect_lines=()):
    def wrap(fn):
        CASES.append((name, fixture_id, expect_status, expect_lines, fn))
        return fn
    return wrap


@case("f4-honest", "shiftline-vendor-acr", "PASS",
      ("Claims-delta verdicts: 56/56",))
def f4_honest(text, meta):
    return text


@case("f4-verdict-flipper", "shiftline-vendor-acr", "FAIL", (
    "verdict: 2.4.7: overstated (expected confirmed)",
    "verdict: 1.4.3: confirmed (expected overstated)",
    "2.1.1 row cites none of ['a11y_grid_cells_keyboard']",
    "trend vocabulary against a foreign ACR: 'persistent'",
    "invented finding_id: a11y_bogus_extra",
))
def f4_flip(text, meta):
    text = swap_verdict(text, "2.4.7", "overstated")   # FP arm
    text = swap_verdict(text, "1.4.3", "confirmed")    # miss arm
    text = text.replace("| 2.1.1 | (claimed term) | (observed would-be term) "
                        "| overstated | a11y_grid_cells_keyboard |",
                        "| 2.1.1 | (claimed term) | (observed would-be term) "
                        "| overstated | keyboard defects observed |")
    return text + ("\n\nThe 1.4.3 contrast defect is persistent since the "
                   "vendor's ACR (see also a11y_bogus_extra).")


@case("f4-honest-rule-quote", "shiftline-vendor-acr", "PASS", (
    "Claims-delta verdicts: 56/56",))
def f4_rule_quote(text, meta):
    # First-local-row adjudication probe: QUOTING the trend boundary rule
    # is compliance, not violation — the negation-aware scan must not fire.
    return text + ("\n\nTrend boundary: foreign ACR — trend vocabulary "
                   "(persistent/worsening/improving/resolved) is out of "
                   "scope for third-party claims without prior "
                   "fingerprint history.")


@case("f4-shoulds-missed", "shiftline-vendor-acr", "WARN", (
    "1.2.3: NA-claim classification note absent",
    "summary misses all of",
))
def f4_warn(text, meta):
    text = text.replace("classification note: the claimed content type does "
                        "exist (media exists in the sample); the NA "
                        "reasoning is wrong while the conformance content "
                        "holds", "—")
    text = re.sub(r"\n\nSummary: .*", "", text)
    return text


@case("f4b-honest", "courseware-vendor-acr-clean", "PASS",
      ("Claims-delta verdicts: 56/56",))
def f4b_honest(text, meta):
    return text


@case("f4b-flagger", "courseware-vendor-acr-clean", "FAIL", (
    "verdict: 1.4.3: overstated (expected confirmed)",
    "invented finding_id: a11y_contrast_ghost",
))
def f4b_flag(text, meta):
    text = swap_verdict(text, "1.4.3", "overstated")
    return text.replace("| 1.4.3 | (claimed term) | (observed would-be term) "
                        "| overstated | — |",
                        "| 1.4.3 | (claimed term) | (observed would-be term) "
                        "| overstated | a11y_contrast_ghost |")


def main():
    dump = "--dump" in sys.argv
    failures = 0
    for name, fixture_id, expect_status, expect_lines, fn in CASES:
        meta = load_meta(fixture_id)
        text = fn(build_honest_delta(meta), meta)
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
