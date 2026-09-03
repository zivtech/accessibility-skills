# GT-05 — SPA route change: fixture pair, blind draws, acceptance gate (2026-09-03)

Receipts for the clause-6 review of the GT-05 (ledger PT-14) fixture pair in
`evals/suites/a11y-critic/`. Two commits on `learnings/wave2-gt-fixtures`:

| Commit | What it is |
|---|---|
| `5f69e0f` | revision 1 — the pair as first authored |
| `89e06b3` | revision 2 — repairs from the draws and the gate below |

## What was run

Five opus reviewers, all reading a single file and nothing else:

| File | Condition | Fixture | Prompt |
|---|---|---|---|
| `claude-critic-skill-unannounced-opus-rev{1,2}.md` | a11y-critic agent (skill loaded) | BUG | blind |
| `claude-critic-skill-clean-opus-rev{1..4}.md` | a11y-critic agent (skill loaded) | CLEAN | blind |
| `claude-baseline-unannounced-opus-rev{1,2}.md` | general-purpose agent, no skill | BUG | blind |
| `claude-baseline-clean-opus-rev{1..4}.md` | general-purpose agent, no skill | CLEAN | blind |
| `bench-reviewer-gate-opus-rev1.md` | bench-reviewer, full file access | both + rubrics + metadata | not blind (it reviews the instrument) |

Twelve draws in total. `revN` is the fixture revision the draw read, not a
repeat draw of the same text.

Prompts are the harness's own output: `prompts/*.blind.md` is
`run_benchmark.load_fixture()`, which applies `strip_answer_key()`. Reviewer
reports are verbatim, recovered from each agent's session transcript rather
than from the truncated inter-agent messages.

## Revision 1 result

**Every draw found both planted defects in the BUG half** and returned REVISE;
both CLEAN draws returned an ACCEPT-shaped verdict. That is the signal the
fixture is for, and it survived into revision 2 unchanged.

**What the draws also found — five unplanted defects, in both halves:**

| # | Defect | Raised by | Severity given |
|---|---|---|---|
| 1 | Header flex row cannot wrap; ~408px minimum against a 320px threshold (1.4.10 Reflow) | all four | MAJOR against the CLEAN half |
| 2 | Hand-computed `aria-current` overrides `NavLink`'s own with a stricter match | both BUG draws | MAJOR |
| 3 | Links to sub-routes no `<Route>` matched; no index or catch-all, so `/` rendered an empty document | three draws | MAJOR |
| 4 | `<main>` not focusable as the skip-link target | two draws | MAJOR / ENHANCEMENT (contested) |
| 5 | React StrictMode repeats mount effects, so the boolean `isFirstRender` guard was already false on the repeat and focus moved on first load anyway | CLEAN skill draw | MINOR |

Defect 1 is the one that matters most: a CLEAN fixture carrying a legitimately
flaggable defect scores a correct reviewer as a false positive. That is the
`modal-complete-clean` failure mode, and it was found here by the very draw the
fixture was supposed to pass. Defect 5 is worse in kind — it is inside trap 1,
so the fixture did not do what its own rubric said it did.

**What the gate found — three instrument defects the draws could not see:**

- **CRITICAL, scoring.** Both `must_find` descriptions fell through to
  `score_common.fallback_keywords`, which keeps the first four words over three
  characters and marks an item FOUND if ANY of them appears anywhere in the
  review — `['focus','left']` and `['document','title','never']`. The gate
  proved with a synthetic review that a critic finding **neither** planted
  defect and reporting all three traps scored 1/2 = 50% = PASS, credited off
  the sentence "visible focus indicators are present, which is good". The 30%
  calibration on the title item was unachievable, because "title" matches
  everything.
- **MAJOR, blindness.** `ANSWER_KEY_RE` anchors on `## Accessibility Issues`,
  which a CLEAN fixture has no reason to carry, so the whole file reached the
  prompt — including the Difficulty line naming all four traps. **The
  revision-1 CLEAN draws are therefore not evidence that the traps hold: they
  were shown the answer.** Fixed with the `modal-complete-clean` heading
  precedent, and re-drawn.
- **MAJOR, false claim.** "The title half has no skill text at all" is false
  bundle-wide: `perspective-audit/references/perspectives.md:161` and
  `a11y-test/SKILL.md:726-728` both require a route change to update the page
  title, and the PT-14 disposition row already said a11y-test carries SPA
  sections. Verified directly. The claim is now scoped to the a11y-critic
  skill, where the 0-hit result stands against a 3-hit positive control.

The gate's own note on its performance is kept verbatim in its report: four of
the five fixture defects found, one missed outright, two under-rated, and one
(the `<main>` focus target) found and then argued away on house-precedent
grounds. The blind draws beat it on fixture content; it beat them on the
instrument. Neither alone would have been enough.

## Scoreboard — 12 draws across four revisions

| Rev | Fixture | critic-skill | baseline | Both planted defects found (BUG) / traps held (CLEAN) |
|---|---|---|---|---|
| 1 | BUG | REVISE | REVISE | 2/2 both |
| 1 | CLEAN | ACCEPT-with-reservations | ACCEPT | traps held, but the fixture leaked its trap list — **not evidence** |
| 2 | BUG | REVISE | REVISE | 2/2 both |
| 2 | CLEAN | REVISE | REVISE | both traced the redirect defect revision 2 introduced |
| 3 | CLEAN | ACCEPT-with-reservations | REVISE | baseline found the index-route defect revision 3 introduced |
| 4 | CLEAN | **ACCEPT** | **ACCEPT** | 6/6 and 5/5 pre-committed predictions refuted; no CRITICAL, no MAJOR |

The BUG half has been stable since revision 2 and is not re-drawn after it: all
four BUG draws found both planted defects and returned REVISE. The CLEAN half
took four revisions to reach a clean ACCEPT from both conditions.

**What the A/B says.** On the BUG fixture the two conditions agree — both find
both defects, so this pair does not discriminate skill-condition from baseline
on detection. Where they differ is severity discipline and negative space: the
skill-condition draws write pre-commitment predictions, mark confidence, and
state what they checked and found clean, and it was a skill-condition draw that
held MAJOR on the CLEAN half's reflow defect when the baseline rated the same
construct MINOR. One draw per cell is not a calibration.

## The repair spiral, and what it means

Three consecutive repair rounds each introduced a new legitimate defect into
the CLEAN half, and each was caught only by a fresh draw:

| Revision | Repair | Defect it introduced |
|---|---|---|
| 2 | index redirect added to fix the empty-document route gap | the redirect's second render read as a navigation and stole focus on cold entry — the exact harm the fixture's guard exists to prevent |
| 3 | redirect replaced with an index route rendering the accounts view at `/` | `NavLink ... end` is inactive at `/`, so the entry URL showed a section no nav item claimed as current |
| 4 | index route removed; portal mounted at `/accounts` | none found; both draws ACCEPT |

Every one of those was in the route table. The CLEAN half models a whole
application shell — route table, nav active state, entry URL, document head,
responsive CSS — and each of those surfaces generated a legitimate finding. The
sibling CLEAN fixtures are single components, and none of them has needed a
repair round.

**Recommendation, for the user rather than done here:** narrow the CLEAN half to
the route-change mechanism at the scale of its siblings. The current fixture is
defensible as it stands — two ACCEPT verdicts, all six traps held — but its
surface area is why it took four rounds, and the same surface is what a future
maintainer will have to keep clean.

**The rule this lane earned:** a repair round is a new authoring round. A CLEAN
fixture is clean as of its last draw and no earlier, and a repair that is not
re-drawn is a claim, not a result.

## Residual, stated rather than fixed

- **Trailing-slash URLs.** With `end`, `NavLink` compares pathnames literally, so
  `/accounts/` renders the accounts view without marking the nav item current.
  2.4.8 Location at AAA, normally normalised by the host before it reaches the
  router. Closing it means adding another route-table surface — the class of
  change that introduced a defect in each of revisions 2 and 3.
- **Back/forward.** The focus effect keys on `pathname` alone, so a POP is
  treated as a forward navigation: scroll resets and focus moves where the
  browser would have restored both. No SC maps to it. Both revision-4 draws
  reached it, so it is scored as a `nice_to_find` rather than left as unlisted
  surface a reviewer could be penalised for noticing.
- **`.portal-main:focus-visible`** was added in revision 5, after both skill
  draws raised it. It is additive CSS; the two ACCEPT draws are against
  revision 4 and were not re-run for it.

## Reproduce

```
python3 evals/results/gt05-spa-route-change/canaries.py    # exit 0 = CLEAN
python3 scripts/validate_fixtures.py
```

`canaries.py` is the standing proof for the scoring CRITICAL: a trap-only
review scores 0/2, a correct review 2/2, a focus-only review 1/2. The first
four words of each `must_find` description are load-bearing scoring tokens —
rewriting them for readability silently re-opens the defect.

## Known properties, not defects

- Every CLEAN fixture in this suite states its correct decisions in an
  `## Accessibility Features Present` section that **is** part of the prompt;
  traps 1 and 4 are partly pre-empted there. That is the corpus convention, not
  a GT-05 leak, and it applies equally to the sibling CLEAN fixtures.
- The gate reports the same `ANSWER_KEY_RE` exposure in all three GT siblings
  on this branch (GT-07, GT-09, GT-11). Not fixed here — flagged for the user,
  since re-drawing those rows is separate work.

## Not evidence of

These rows are Claude-subagent draws at one temperature on one day. They are
not a local-model row, not a Codex or Gemini row, and not a multi-draw variance
characterisation — the repo's own calibration history says single draws flip
items at this magnitude. They establish that the pair discriminates for one
reviewer family, not that its `expected_to_find` figures are calibrated.
