#!/usr/bin/env python3
"""Would scoring `false_positive_trap` have been worth it?

Issue #63 asks whether to score the `false_positive_trap` rubric dimension or
delete it. This probe answers it from evidence already in the repo — the 110
committed CLEAN draws of the features-section lane — instead of from opinion.
No new draws.

It reports three things:

  1. How much the model over-flags CLEAN fixtures overall (verdict level).
  2. How often the specific constructs the rubrics *predicted* would be
     over-flagged actually appear, using hand-authored patterns.
  3. The matched excerpts, so a reader can check whether a "fire" is really
     an over-flag — or the model affirming the pattern, or offering an
     enhancement. This is the part that decides the question.

Run from the repo root:
    python3 evals/results/fixture-leak-2026-09/trap-probe.py
"""
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DRAWS = os.path.join(HERE, "featurehint")

# Hand-authored patterns for two fixtures' trap items. Deliberately written the
# way a first implementation would be — concrete construct names — because the
# question is whether that approach works, not whether a perfect matcher could.
TRAPS = {
    "async-retry-recovery-clean": {
        "aria-hidden on decorative spinner": [
            r"aria-hidden[^.\n]{0,60}spinner", r"spinner[^.\n]{0,60}aria-hidden"],
        "two politeness levels": [
            r"politeness[^.\n]{0,40}(inconsisten|mismatch|conflict)",
            r"(inconsisten|conflict)[^.\n]{0,40}politeness"],
        "empty persistent containers": [
            r"empty[^.\n]{0,40}(live region|status|alert)",
            r"(live region|status container)[^.\n]{0,30}empty"],
    },
    "modal-complete-clean": {
        "role=presentation on overlay": [
            r"role=[\"']?presentation[\"']?[^.\n]{0,60}(missing|should|add|need)",
            r"overlay[^.\n]{0,50}role"],
        "setTimeout for initial focus": [
            r"setTimeout[^.\n]{0,70}(unreliab|timing|race|fragile|anti-?pattern)"],
    },
}


def load(path):
    with open(path) as f:
        return json.load(f)["response"]


def overall():
    with open(os.path.join(HERE, "score-featurehint.json")) as f:
        rows = [r for r in json.load(f)["rows"] if r["tier"] == "CLEAN"]
    n = len(rows)
    non_accept = sum(1 for r in rows if r["verdict"] != "ACCEPT")
    with_findings = sum(1 for r in rows if r["structured_findings"] > 0)
    print(f"=== Over-flagging overall, {n} committed CLEAN draws")
    print(f"  no clean ACCEPT            {non_accept}/{n} = {non_accept/n:.0%}")
    print(f"  raised >=1 structured find {with_findings}/{n} = {with_findings/n:.0%}")
    return n


def trap_fires():
    print("\n=== Did the *predicted* constructs fire?")
    for fixture, traps in TRAPS.items():
        files = sorted(glob.glob(os.path.join(DRAWS, f"*-{fixture}-*.json")))
        if not files:
            continue
        print(f"\n{fixture}  ({len(files)} draws)")
        for name, pats in traps.items():
            hits = [p for p in files
                    if any(re.search(x, load(p), re.I) for x in pats)]
            print(f"  {name:36s} {len(hits):2d}/{len(files)}  ({len(hits)/len(files):.0%})")
            for p in hits[:4]:
                text = load(p)
                for pat in pats:
                    m = re.search(r"[^.\n]{0,70}" + pat + r"[^.\n]{0,60}", text, re.I)
                    if m:
                        print(f"       … {' '.join(m.group(0).split())[:132]}")
                        break


if __name__ == "__main__":
    overall()
    trap_fires()
    print("""
=== Reading

The predicted constructs fire at 0-40% while the model fails to return a clean
ACCEPT on 93% of the same draws. The rubric authors guessed wrong about what
gets over-flagged: the traps are not where the false positives are.

And the one non-trivial rate is the matcher, not the model. Read the
`role=presentation` excerpts above: the model is affirming the pattern
("safe for AT because the overlay is non-focusable"), or offering a legitimate
enhancement ("use `inert` instead ... more robust"), or merely citing the line.
A naive trap matcher scores those as false positives and would report the
instrument working. That is the same prose-matching brittleness that produced
five false must-misses in `score_acr.py` (see
../human-verification-stage/retest-2026-09-04/), firing here in the flattering
direction.

Conclusion for #63: scoring this dimension costs hand-authored, adversarially
tested tokens for all 50 items plus a recalibration and a disclosure, and buys
an explanation of roughly a tenth of the behaviour. The verdict-level and
structured-finding measures already in this lane capture all of it for free.
""")
