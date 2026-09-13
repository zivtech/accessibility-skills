#!/usr/bin/env python3
"""Simulate a cross-family LOCAL-model ensemble from already-collected per-model
critic responses — NO new inference. Answers the ensemble hypothesis: does 2-of-3
AGREEMENT cut CLEAN over-flagging (the ceiling) while holding HAS-BUGS catches?

Verdict-level analysis (a model "flags" a component if its verdict is REVISE or
REJECT). For CLEAN fixtures a flag is a FALSE ALARM; for HAS-BUGS a flag is a
correct catch. Union = >=1 model flags; Majority = >=2; Unanimous = 3.

Usage: python3 ollama/simulate_ensemble.py <model-slug> <model-slug> <model-slug> ...
  reads evals/results/local-critic/<slug>/<fixture>.json
"""
import sys, os
BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BASE)
FIX = os.path.join(REPO, "evals/suites/a11y-critic/fixtures")
LC = os.path.join(REPO, "evals/results/local-critic")
sys.path.insert(0, BASE)
import score_output as so  # noqa: E402
from run_gemini_agy_critic import BASELINE_33  # noqa: E402

FLAG = {"REVISE", "REJECT"}


def verdict_for(slug, fixture):
    p = os.path.join(LC, slug, fixture + ".json")
    if not os.path.exists(p):
        return None
    text, trunc = so.load_response(p)
    if trunc or not text.strip():
        return None
    return so.check_verdict(text)


def difficulty(fixture):
    return so.load_rubric(os.path.join(FIX, fixture + ".md".replace(".md", ".metadata.yaml"))).get("difficulty", "unknown") \
        if os.path.exists(os.path.join(FIX, fixture + ".metadata.yaml")) else "unknown"


def main():
    slugs = sys.argv[1:]
    if len(slugs) < 2:
        sys.exit("give >=2 model slugs")
    clean = [f for f in BASELINE_33 if difficulty(f) == "CLEAN"]
    hasbugs = [f for f in BASELINE_33 if difficulty(f) in ("REVISE", "REJECT") or difficulty(f) not in ("CLEAN", "ADVERSARIAL", "unknown")]
    # Fallback: treat non-CLEAN, non-ADVERSARIAL as has-bugs by rubric verdict.
    print(f"Models: {', '.join(slugs)}")
    print(f"CLEAN fixtures: {len(clean)} | HAS-BUGS fixtures: {len(hasbugs)}\n")

    def flags(slug, fx):
        v = verdict_for(slug, fx)
        return None if v is None else (v in FLAG)

    # Per-model false alarms (CLEAN) and catches (HAS-BUGS)
    print(f"{'model':22} {'CLEAN false-alarms':20} {'HAS-BUGS catches'}")
    for s in slugs:
        fa = sum(1 for f in clean if flags(s, f))
        ca = sum(1 for f in hasbugs if flags(s, f))
        print(f"{s:22} {fa}/{len(clean):<18} {ca}/{len(hasbugs)}")
    print()

    def ensemble(fixtures, threshold):
        hits = 0
        for f in fixtures:
            votes = [flags(s, f) for s in slugs]
            votes = [v for v in votes if v is not None]
            if votes and sum(votes) >= threshold:
                hits += 1
        return hits

    n = len(slugs)
    print(f"{'ensemble rule':22} {'CLEAN false-alarms':20} {'HAS-BUGS catches'}")
    print(f"{'union (>=1)':22} {ensemble(clean,1)}/{len(clean):<18} {ensemble(hasbugs,1)}/{len(hasbugs)}")
    print(f"{'majority (>=2)':22} {ensemble(clean,2)}/{len(clean):<18} {ensemble(hasbugs,2)}/{len(hasbugs)}")
    print(f"{'unanimous (>={n})':22} {ensemble(clean,n)}/{len(clean):<18} {ensemble(hasbugs,n)}/{len(hasbugs)}")
    print("\nRead: lower CLEAN false-alarms = better precision; higher HAS-BUGS catches = better recall.")
    print("The ensemble helps only if majority/unanimous cuts CLEAN false-alarms while holding HAS-BUGS catches.")


if __name__ == "__main__":
    main()
