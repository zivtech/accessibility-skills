#!/usr/bin/env python3
"""Gate the byte size of the always-on context files (CLAUDE.md, AGENTS.md).

CLAUDE.md and AGENTS.md load into context in every session that touches this
repo, so their byte size is a per-session token tax. CLAUDE.md regrew from a
lean file to 32,986 bytes between 2026-06 and 2026-09 — almost entirely dated
eval results, model-benchmark deltas, and provenance narrative that already
lived in `docs/*-adoption-assessment.md` and `evals/results/*/README.md`. It
was cut back on 2026-09-12 (see `context-audit/03-accessibility-skills-handoff.md`).
This gate exists so that regression is caught early rather than after the file
has silently doubled again.

Two thresholds per file:

  warn  soft limit — printed as a warning, never fails the build. Set just
        above the rules-preserved floor so any regrowth is visible immediately.
  fail  hard limit — `--strict` exits 1. Set with headroom for legitimate
        growth but well below the 33KB regression point.

The CLAUDE.md budget is set just above the *rules-preserved* floor (~16.6KB
after the 2026-09-12 cut): the load-bearing rules (the WCAG-EM / ICT-baseline
scope rules and reading traps, the acr-reporting gates, the browser-automation
routing verdicts) are stated as named-rule + doc pointer, with the mechanics in
each skill's own SKILL.md and in docs. Going much lower means deleting a working
rule, not trimming prose. If a future cut genuinely relocates rule content to
docs, lower these numbers.

Content policy this gate backstops (not machine-checkable, stated for editors):
dated eval results, model-row deltas, and phase-by-phase provenance belong in
`docs/*-adoption-assessment.md` or `evals/results/*/README.md`, cited by a
one-line pointer here — never inline.

`--self-test` runs the classifier against synthetic sizes (a positive control
that must trip `fail`, negative controls that must not) and exits 1 if the
threshold logic misbehaves — a green report is only meaningful if the gate
provably fires. CI runs the self-test before the scan.

Exit 0 on a clean report (or any report without `--strict`); exit 1 under
`--strict` if any budgeted file is at or above its fail threshold.

Run from repo root:
    python3 scripts/check_doc_budget.py --self-test
    python3 scripts/check_doc_budget.py
    python3 scripts/check_doc_budget.py --strict
"""

import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Per-file byte budgets. warn < fail. See module docstring for rationale.
BUDGETS = {
    "CLAUDE.md": {"warn": 18_000, "fail": 21_000},
    "AGENTS.md": {"warn": 5_000, "fail": 8_000},
}


def classify(size, budget):
    """Return 'ok', 'warn', or 'fail' for a byte size against a {warn, fail} budget."""
    if size >= budget["fail"]:
        return "fail"
    if size >= budget["warn"]:
        return "warn"
    return "ok"


def file_size(rel_path):
    """Byte size of a repo-relative file, or None if it does not exist."""
    abs_path = os.path.join(REPO, rel_path)
    try:
        return os.path.getsize(abs_path)
    except OSError:
        return None


def self_test():
    """Classifier controls. Every positive must trip its band; negatives must not."""
    budget = {"warn": 100, "fail": 200}
    cases = [
        (50, "ok"),
        (99, "ok"),
        (100, "warn"),
        (150, "warn"),
        (199, "warn"),
        (200, "fail"),
        (500, "fail"),
    ]
    failures = []
    for size, expected in cases:
        got = classify(size, budget)
        if got != expected:
            failures.append(f"classify({size}) = {got!r}, expected {expected!r}")
    # Explicit positive/negative controls for the fail band (the one that gates CI).
    if classify(budget["fail"], budget) != "fail":
        failures.append("positive control: size at fail threshold did not classify 'fail'")
    if classify(budget["warn"] - 1, budget) == "fail":
        failures.append("negative control: size below warn classified 'fail'")

    if failures:
        print("Doc-budget self-test FAILED:")
        for failure in failures:
            print(f"  {failure}")
        sys.exit(1)
    print(f"Doc-budget self-test passed — {len(cases)} classifier cases + 2 controls.")
    sys.exit(0)


def main():
    if "--self-test" in sys.argv[1:]:
        self_test()

    strict = "--strict" in sys.argv[1:]
    any_fail = False
    any_warn = False
    print("Doc byte budget:")
    for rel_path, budget in BUDGETS.items():
        size = file_size(rel_path)
        if size is None:
            print(f"  MISS {rel_path} (not found — budget skipped)")
            continue
        status = classify(size, budget)
        marker = {"ok": "ok  ", "warn": "WARN", "fail": "FAIL"}[status]
        print(
            f"  {marker} {rel_path}: {size:,} bytes "
            f"(warn {budget['warn']:,} / fail {budget['fail']:,})"
        )
        if status == "fail":
            any_fail = True
        elif status == "warn":
            any_warn = True

    if any_fail:
        print(
            "\nAt least one file is at or above its fail budget. Move dated eval "
            "results / provenance to docs and cite a one-line pointer instead."
        )
        if strict:
            sys.exit(1)
    elif any_warn:
        print("\nWarning band reached — watch for further growth.")

    sys.exit(0)


if __name__ == "__main__":
    main()
