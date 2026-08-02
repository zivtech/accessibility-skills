#!/usr/bin/env python3
"""De-hint checker for planner fixtures (adoption plan step 11a).

The step-10 A/B (evals/results/wcag-em-phase3/) proved that a fixture whose
text names its own rubric keywords saturates the mechanical gate for every
model and condition. A de-hinted fixture makes the opposite promise: none of
its scoring keywords (nor any cue-adjacent term in `dehint_forbidden`) appear
in the fixture text, so a gate hit can only come from knowledge the plan
brought itself.

This script enforces that promise, plus the key-alignment property the gate
silently depends on:

1. ALIGNMENT — every expected_findings.must_have item has an exact-match key
   in scoring_keywords. A mismatched key sends score_planner.py to weak
   fallback keywords without failing, quietly degrading the gate.
2. DE-HINT — no keyword from any scoring_keywords list, and no term from
   dehint_forbidden, occurs case-insensitively in the fixture text (the same
   substring test score_planner.py applies to plans).

Exit codes: 0 clean; 1 any check failed (fixtures without `dehinted: true`
run in advisory mode — findings are printed but exit is 0, so the checker
can also audit hinted fixtures without gating them).

Usage:
    python3 evals/suites/a11y-planner/check_dehinted.py \
        fixtures/<id>.md fixtures/<id>.metadata.yaml

Run it after ANY edit to a de-hinted fixture's .md or metadata.
"""

import sys

import yaml


def collect_keywords(meta: dict) -> list[tuple[str, str]]:
    """Return (source_label, keyword) pairs from scoring_keywords + dehint_forbidden."""
    pairs = []
    for item, kws in (meta.get("scoring_keywords") or {}).items():
        for kw in kws or []:
            pairs.append((f"scoring_keywords[{item[:50]}…]", kw))
    for kw in meta.get("dehint_forbidden") or []:
        pairs.append(("dehint_forbidden", kw))
    return pairs


def main() -> int:
    if len(sys.argv) != 3:
        sys.exit(f"Usage: {sys.argv[0]} <fixture.md> <metadata.yaml>")

    with open(sys.argv[1]) as f:
        fixture_text = f.read()
    with open(sys.argv[2]) as f:
        meta = yaml.safe_load(f)

    dehinted = bool(meta.get("dehinted", False))
    fixture_lower = fixture_text.lower()
    failures = 0

    print(f"Fixture: {meta.get('fixture_id', sys.argv[1])}")
    print(f"Declared de-hinted: {dehinted}")

    # 1. alignment: every must_have item resolves to explicit keywords
    expected = meta.get("expected_findings") or {}
    must_have = expected.get("must_have") or []
    keys = set((meta.get("scoring_keywords") or {}).keys())
    unaligned = [item for item in must_have if item not in keys]
    print(f"\nAlignment: {len(must_have) - len(unaligned)}/{len(must_have)} "
          f"must_have items have exact scoring_keywords keys")
    for item in unaligned:
        failures += 1
        print(f"  X no exact key (scorer would fall back): {item[:90]}")

    # 2. de-hint: no keyword substring appears in the fixture text
    collisions = []
    seen = set()
    for source, kw in collect_keywords(meta):
        if kw.lower() in fixture_lower and (kw.lower(), source) not in seen:
            seen.add((kw.lower(), source))
            collisions.append((source, kw))
    print(f"\nDe-hint: {len(collisions)} keyword collision(s) in fixture text")
    for source, kw in collisions:
        failures += 1
        line_no = next(
            (i + 1 for i, line in enumerate(fixture_text.splitlines())
             if kw.lower() in line.lower()), "?",
        )
        print(f"  X '{kw}' (from {source}) — first hit at fixture line {line_no}")

    ok = failures == 0
    print(f"\nStatus: {'CLEAN' if ok else f'{failures} FAILURE(S)'}")
    if not ok and not dehinted:
        print("(advisory mode — fixture is not declared dehinted; exit 0)")
        return 0
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
