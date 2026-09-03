# GT-07, GT-09, GT-11 — first model rows (2026-09-03)

The three GT-wave fixture pairs shipped in `3c29733`, `5d7e6d4` and `5efa15f`
with "no model rows yet". This is that measurement, taken before the wave's PR
rather than after — twelve blind draws, every fixture in all three pairs, under
both conditions.

It was worth taking before shipping. Two defects here would have made the rows
meaningless, and one of them was scoring correct reviewers as wrong.

## Conditions

| Condition | Agent | Prompt |
|---|---|---|
| `critic-skill` | `a11y-critic` (protocol loaded) | blind |
| `baseline` | `general-purpose`, no skill | blind |

Prompts are the harness's own `run_benchmark.load_fixture()` output, in
`prompts/*.blind.md`. Reports are verbatim, recovered from each agent's session
transcript. All twelve draws are opus, one per cell, on 2026-09-03.

## Result — the pairs discriminate

| Pair | Fixture | critic-skill | baseline |
|---|---|---|---|
| GT-07 | `async-retry-error-unannounced` (BUG) | REVISE, both must-finds | REVISE, both must-finds |
| GT-07 | `async-retry-recovery-clean` | ACCEPT | ACCEPT |
| GT-09 | `pseudo-link-map-controls` (BUG) | REVISE, must-find found | REVISE, must-find found |
| GT-09 | `map-controls-clean` | ACCEPT | ACCEPT |
| GT-11 | `row-action-inconsistent-labels` (BUG) | REVISE, must-find found | REVISE, must-find found |
| GT-11 | `paired-id-name-columns-clean` | ACCEPT | ACCEPT |

Six for six in both conditions. The BUG halves are found, the CLEAN halves are
not over-flagged, and no CLEAN half drew a CRITICAL or MAJOR from either
condition.

**The A/B is not a detection difference.** Both conditions find every planted
defect. What separates them is discipline: the skill-condition draws write
pre-commitment predictions before reading and report how many were refuted
(3 of 5, 5 of 6, 4 of 6 across these fixtures), mark confidence, separate
"checked and deliberately not flagged" from silence, and decline to inflate a
citation — the GT-09 draw explicitly refused to file 2.1.1 for a role mismatch
that Tab+Enter still operates. One draw per cell is not a calibration.

## What the draws found in the instrument

**Scoring — the must_find descriptions did not discriminate.** Checked before
the draws, on the same class the GT-05 gate had found. `score_output.py` has no
explicit-keyword field, so a description falls through to
`fallback_keywords`: first four words over three characters, FOUND if ANY
appears anywhere. A trap-only review — one that finds neither planted defect and
reports only that fixture's own declared traps — scored:

| Fixture | Before | Keywords |
|---|---|---|
| `async-retry-error-unannounced` | 1/2 = 50% **PASS** | matched via the live-region branch, which the trap is also about |
| `pseudo-link-map-controls` | 1/1 = 100% **PASS** | `['link', 'role']` |
| `row-action-inconsistent-labels` | 1/1 = 100% **PASS** | `['same', 'action']` |

Fixed in `2dd9a32`; `canaries.py` is the standing proof for all four GT BUG
fixtures, and records the pre-fix numbers so the regression stays legible.

**GT-07's trap 1 penalised a correct finding.** It claimed the loading live
region was fine and flagging it was a false alarm. But `status` initialises to
`'loading'`, so that region mounts with its message already inside — the exact
pattern the CLEAN pair member's own notes call "frequently not spoken at all".
Three draws reached it independently; the BUG skill draw called it "the
surprise I did not predict: the component announces nothing in any state,
ever." Each of them would have been scored −2 for being right. Narrowed to
"reporting it as MISSING is a false alarm", with the mount-timing observation
scored as a `nice_to_find` at 35%.

**GT-07 CLEAN carried an unplanted defect** — `list-style: none` with no
`role="list"` (1.3.1), flagged by both draws. That is the failure a CLEAN half
exists to avoid. Fixed, and the construct is now a trap. Its "persistent live
regions" claim also overreached: the invariant covers every transition except
the first paint.

**GT-09's prose contradicted its own DOM** — line 136 said the controls sit
"above the map"; they render after the canvas. Both draws spent words on it,
and one noted that satisfying the old wording with CSS rather than JSX would
split visual and focus order into a real 1.3.2 defect.

**GT-11 needed no repair.** Both draws ACCEPT with only AAA-level and
robustness observations, now scored as `nice_to_find` so a reviewer who reaches
them is credited: the missing `overflow-x` container, and the correction that
2.4.4 is satisfied by its own normative admission of "a table header cell for
a cell that contains the link" rather than by an assumption about screen-reader
behaviour.

## Open, raised rather than fixed

**The BUG fixtures' titles name their own defect.** "Async Request Failure and
Recovery Are Never Announced" is line 1 of the blind prompt. The GT-07 skill
draw flagged it and deliberately audited past it, finding four issues
independent of the telegraphed one. This is corpus-wide convention across the
HAS-BUGS fixtures rather than a GT-wave regression, so it is not changed
unilaterally — but every BUG row in this suite is measured with a hint in the
prompt, and that belongs in any claim made from these numbers.

**The CLEAN fixtures pre-argue their own defenses.** The
`Accessibility Features Present` section precedes the blind cut line by corpus
convention, so a CLEAN prompt carries the reasoning for its own traps. The
GT-11 baseline draw noticed and said it derived its 3.2.4 and 2.4.4 rulings
before reading that section. Same disposition: convention, not a GT defect,
but it caps what a CLEAN trap row can claim.

## GT-07 narrowed, and the result that justified it

GT-07's CLEAN half took three repair rounds, each turning up a real MAJOR:
missing `role="list"` (1.3.1), then a stale-request race that let a slow failure
interrupt assertively over a successful load, then a Retry press that was
deterministically silent while loading. Only the first was about what the
fixture measures. The other two came from the fixture owning its own fetch.

Narrowed on the user's call (220 -> 135 lines, against map-controls-clean at
164): the component is presentational now, with `status`, `transactions` and
`onRetry` as props, so the race, the repeat-press question and the abort
question belong to the parent and leave the fixture entirely.

| | Before narrowing | After |
|---|---|---|
| critic-skill | ACCEPT-with-reservations, 1 MAJOR | **ACCEPT**, no CRITICAL/MAJOR, 4 of 6 predictions refuted |
| baseline | ACCEPT | **ACCEPT**, no CRITICAL/MAJOR |

Two items came out of the narrowing itself and were fixed: the trimmed CSS had
dropped the row's flex rule, so payee and amount rendered with no separator and
read as one string ("Acme Corp-$42.00"); and the initial-mount caveat now needed
stating as a parent contract, since the component no longer controls when it
first renders. Both draws named the second one, and the skill draw's recommended
fix — "state the parent-side invariant explicitly" — is what the Expected
Behavior list now says.

This is the second fixture in the wave to reach a clean result only after being
narrowed, which is the wave's most transferable finding: a CLEAN fixture that
models a whole subsystem inherits that subsystem's defect surface, and none of
it is what the fixture measures.

## Reproduce

```
python3 evals/results/gt-siblings-rows/canaries.py    # exit 0 = CLEAN
python3 scripts/validate_fixtures.py
```

## Not evidence of

One opus draw per cell on one day. Not a local-model row, not Codex or Gemini,
not a multi-draw variance characterisation — this repo's own history says single
draws flip items at this magnitude. These rows establish that each pair
discriminates for one reviewer family, not that the `expected_to_find` figures
are calibrated.
