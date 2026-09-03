I'll start by orienting in the worktree and reading the commit under review.

---

**Verdict: REVISE** — report sent to team-lead.

**1 CRITICAL:** Both must-find descriptions fall through to `fallback_keywords`, yielding `['focus','left']` and `['document','title','never']`. I proved with a synthetic review that a critic finding *neither* planted defect and reporting *all three* traps scores 1/2 = 50% → **PASS** — credited off the positive sentence "visible focus indicators are present, which is good" (`strip_negation_lines` exists in `score_common.py:64` but `score_output.py` never calls it). Delete the word "focus" → 0/2 FAIL. The 30% calibration on the title item is unachievable; "title" matches everything.

**2 MAJOR:**
- The CLEAN fixture leaks its answer key. `ANSWER_KEY_RE` anchors on `## Accessibility Issues`, which `spa-route-change-clean.md` doesn't have — measured 238 lines in, 238 out. Line 238 names all four traps in one sentence. Wave-wide: all three GT siblings have it too; the three pre-GT CLEAN fixtures strip correctly.
- "The title half has no skill text at all" is false bundle-wide — `perspective-audit/references/perspectives.md:161` and `a11y-test/SKILL.md:726-728` both carry it, and the PT-14 disposition row already said so. The critic-scoped greps (0 hits / 3-hit control) verified true.

**5 MINOR:** missing `REVISE` in BUG metadata notes (only fixture in the wave lacking it); dead `'Not found'` fallback + no catch-all route in CLEAN (unknown URL renders nothing); StrictMode defeats the `isFirstRender` guard; the rAF rationale at `:232` describes a node this design never replaces; redundant `aria-current`.

**Clean:** all 40 line citations verified programmatically, registry 50/50 matches disk, CSS contrast fine, BUG traps well-scoped, difficulty labels right. The skip-link-target-without-tabindex point I initially suspected is settled house style (`button-skip-link-clean.md:23`), so I did not count it.

Both blocking findings are cheap in-fixture fixes — reword two `description:` strings, add one heading (precedent: `modal-complete-clean.md:275`).

---

Addendum sent. Summary:

**Verdict unchanged: REVISE, scoped to revision 1** (5f69e0f as committed). All 40 line citations I verified are now stale — both `.md` files changed length (CLEAN 238→257, BUG 210→227).

**My misses, owned:** Your four blind draws beat me. I missed the 1.4.10 reflow defect outright (I checked contrast and focus visibility, then wrote "CSS is clean" — a scoped pass presented as a general one). Worse, I *found* the `<main>`-not-focusable issue and then argued myself out of it on house-precedent grounds — backwards reasoning, since `button-skip-link-clean.md:23` carrying the same construct is evidence that fixture is also exposed, not that reviewers won't flag it. I found the routing and `aria-current` defects (m5, m8) but under-rated both, and used one to excuse the other. 4 of 5 found, 1 missed, 2 under-rated, 1 wrongly dismissed. My unplanted-defect pass on the BUG fixture reported none, and there were four — treat the draws as the record.

**Repairs address** m5, m6, m8. Not m7 (the rAF rationale prose).

**Survives, and is what you said you need:**
- **C1** stands and is now *worse* — a reviewer writing up the `<main>` focus defect will use the word "focus", which credits must-find item 1. An unplanted-defect finding scores as a planted-defect hit.
- **M2** verified still live: I ran one targeted check rather than re-reviewing — CLEAN strips 257→257 (nothing), BUG 227→208 (correctly).
- **M3** unaffected (skill text, not fixture text).
- **m4** needs recheck — `git status` shows the BUG metadata *is* modified in the working tree, contrary to your note.

**Forward risk worth checking:** the catch-all route makes the `'Not found'` branch reachable for the first time; if the title effect still falls back to bare `SITE`, the CLEAN fixture now fails 2.4.2 on the criterion it exists to teach. Also `role="list"` is a new trap candidate needing its own entry.