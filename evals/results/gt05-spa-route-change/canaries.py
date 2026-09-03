#!/usr/bin/env python3
"""GT-05 scorer canaries — proof that the two must_find descriptions discriminate.

The gate review of revision 1 proved the opposite with a synthetic review: the
original descriptions ("Focus is left on...", "The document title never...")
fall through to score_common.fallback_keywords, which keeps the first four
words longer than three characters and scores an item FOUND if ANY of them
appears anywhere in the review. That yielded ['focus','left'] and
['document','title','never'], so a review finding NEITHER planted defect scored
1/2 = 50% = PASS off the sentence "visible focus indicators are present".

Run:  python3 evals/results/gt05-spa-route-change/canaries.py   (exit 0 = CLEAN)
"""
import importlib.util, os, sys, yaml

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO, "ollama"))
spec = importlib.util.spec_from_file_location("so", os.path.join(REPO, "ollama", "score_output.py"))
so = importlib.util.module_from_spec(spec); spec.loader.exec_module(so)

RUBRIC = os.path.join(REPO, "evals/suites/a11y-critic/rubrics/spa-route-change-unannounced.rubric.yaml")
with open(RUBRIC) as fh:
    must = next(c for c in yaml.safe_load(fh)["expected_findings"] if c["category"] == "must_find")["items"]

# 1. Trap-only review: finds neither planted defect, reports all three traps as
#    positives, and uses the words the original descriptions leaked on.
TRAP_ONLY = """VERDICT: ACCEPT
The nav is correct: real <a href> links inside a labelled <nav>, with
aria-current='page' on the active link. Each view has one <h1> inside the
<main> landmark. The skip link is present and correctly implemented. Visible
focus indicators are present on every interactive element, which is good. The
document is titled and the heading structure is left intact. Nothing to fix."""

# 2. Correct review: finds both planted defects in the natural vocabulary.
CORRECT = """VERDICT: REVISE
CRITICAL: there is no pathname-keyed useEffect anywhere in the shell, so
focus-restoration never happens after a client-side navigation — focus is left
on the nav link that was activated (2.4.3).
MAJOR: document.title is never-updated; index.html sets one static title that
serves all three routes (2.4.2)."""

# 3. Focus-only review: finds defect 1, misses defect 2.
FOCUS_ONLY = """VERDICT: REVISE
CRITICAL: no pathname-keyed useEffect and no focus-restoration on route change;
focus stays on the activated link (2.4.3). Everything else reads correct."""

def score(text):
    return [so.check_finding(text, item)["found"] for item in must]

CASES = [
    ("trap-only review scores neither must-find", TRAP_ONLY, [False, False]),
    ("correct review scores both must-finds", CORRECT, [True, True]),
    ("focus-only review scores exactly one", FOCUS_ONLY, [True, False]),
]

failed = 0
for name, text, expected in CASES:
    got = score(text)
    ok = got == expected
    failed += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {name}: expected {expected}, got {got}")

print("\nkeywords in force:")
for item in must:
    print("  ", so.check_finding("", item)["keywords_checked"])

print("\nCLEAN" if not failed else f"\n{failed} CANARY FAILURE(S)")
sys.exit(1 if failed else 0)
