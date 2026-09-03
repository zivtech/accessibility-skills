#!/usr/bin/env python3
"""Scorer-discrimination canaries for every GT-wave BUG fixture.

score_output.py has no explicit-keyword field. A must_find description that
matches none of its hardcoded branches falls through to
score_common.fallback_keywords, which keeps the first four words longer than
three characters and marks the item FOUND if ANY of them appears anywhere in
the review. The first four words of each description are therefore scoring
tokens, not prose.

Measured before the 2026-09-03 rewording, with a trap-only review that finds
neither planted defect and reports only that fixture's own declared traps:

    async-retry-error-unannounced   1/2 = 50%  -> PASS   (keywords via the live-region branch)
    pseudo-link-map-controls        1/1 = 100% -> PASS   (['link', 'role'])
    row-action-inconsistent-labels  1/1 = 100% -> PASS   (['same', 'action'])
    spa-route-change-unannounced    1/2 = 50%  -> PASS   (['focus', 'left'])

Run:  python3 evals/results/gt-siblings-rows/canaries.py    (exit 0 = CLEAN)
"""
import importlib.util, os, sys, yaml

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO, "ollama"))
spec = importlib.util.spec_from_file_location("so", os.path.join(REPO, "ollama", "score_output.py"))
so = importlib.util.module_from_spec(spec); spec.loader.exec_module(so)
RUBRICS = os.path.join(REPO, "evals", "suites", "a11y-critic", "rubrics")

# Per fixture: a trap-only review (reports only the fixture's declared traps,
# finds neither planted defect) and a correct review (finds every planted one).
CASES = {
 "async-retry-error-unannounced": (
  """VERDICT: ACCEPT
  The loading state needs a live region so users know the request is in flight,
  and aria-busy is missing on the panel body. The spinner is hidden from screen
  readers by aria-hidden, so the loading message is lost.""",
  """VERDICT: REVISE
  CRITICAL: the error-branch has no alert-container at all — failure-silent.
  MAJOR: the recovery-transition is unspoken; results-mount-silent, so the
  retry-outcome-lost."""),
 "pseudo-link-map-controls": (
  """VERDICT: ACCEPT
  The zoom controls should expose a pressed state. The map canvas has no text
  alternative. The link that opens the full report does not warn that it opens
  in a new tab. Roles look fine otherwise.""",
  """VERDICT: REVISE
  CRITICAL: anchor-as-button — the zoom controls use a pseudo-href, so these
  map-controls promise navigation-that-never-happens (F42)."""),
 "row-action-inconsistent-labels": (
  """VERDICT: ACCEPT
  The Case ID and Case Name columns both point at the same record with
  different names, a consistent identification problem. The table needs a
  caption and the column headers need scope.""",
  """VERDICT: REVISE
  MAJOR: the per-row edit-control has label-varies-by-row —
  Edit/Modify/Change-details for one operation."""),
 "spa-route-change-unannounced": (
  """VERDICT: ACCEPT
  The nav is correct with aria-current on the active link, each view has one
  heading inside the main landmark, and the skip link works. Visible focus
  indicators are present, which is good. The document is titled.""",
  """VERDICT: REVISE
  CRITICAL: no pathname-keyed useEffect, so focus-restoration is
  absent-entirely. MAJOR: document.title is never-updated across-routes —
  one static-index-title serves them all."""),
}

failed = 0
for fid, (trap_only, correct) in CASES.items():
    with open(os.path.join(RUBRICS, f"{fid}.rubric.yaml")) as fh:
        items = next(c for c in yaml.safe_load(fh)["expected_findings"]
                     if c["category"] == "must_find")["items"]
    t = sum(so.check_finding(trap_only, i)["found"] for i in items)
    c = sum(so.check_finding(correct, i)["found"] for i in items)
    ok = (t == 0 and c == len(items))
    failed += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {fid}: trap-only {t}/{len(items)} (want 0), "
          f"correct {c}/{len(items)} (want {len(items)})")
    if not ok:
        for i in items:
            print(f"        keywords: {so.check_finding('', i)['keywords_checked']}")

print("\nCLEAN" if not failed else f"\n{failed} CANARY FAILURE(S)")
sys.exit(1 if failed else 0)
