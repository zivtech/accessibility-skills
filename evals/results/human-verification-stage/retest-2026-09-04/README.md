# Retest of the #57 rows against the post-#62 instrument (2026-09-04)

PR #62 changed the `acr-reporting` gate text and the fix-closure contract —
both of which an ACR draw reads. Every existing hosted row had been drawn
against the superseded skill, and fixture #8 had never been drawn at all. This
is the re-run: three `acr-reporting` fixtures, opus ×2 each, at `57034be`.

The `a11y-test-operation-evidence` fixtures were **not** re-drawn. #62 did not
touch `a11y-test/SKILL.md`, so the protocol slice those draws consume
(`load_opevidence_system_prompt()`) is byte-identical; re-running them would
have measured nothing.

## Headline

**Fixture #8's first rows are clean, and the only fixture that failed did so
because of the scorer, not the model.** Across six draws and 18 must-tier
checks the instrument reported five must-misses. Every one traced to
`score_acr.py` matching plain-text tokens against Markdown prose. Zero were
model errors, and zero fabrications appeared anywhere.

## Rows (6) — opus ×2, repo root pinned to `57034be`

| Fixture | Draw | Before the fix | After the fix | Fab |
|---|---|---|---|---|
| `county-library-retest` (#6) | 1 | WARN | WARN | 0 |
| `county-library-retest` (#6) | 2 | **PASS** | **PASS** | 0 |
| `utility-billing-retest` (#7) | 1 | FAIL | WARN | 0 |
| `utility-billing-retest` (#7) | 2 | FAIL | FAIL | 0 |
| `court-payments-independence` (#8) | 1 | WARN | WARN | 0 |
| `court-payments-independence` (#8) | 2 | **PASS** | **PASS** | 0 |

### Fixture #8 — the independence canary works

Its first rows ever, and both carry **zero must-misses**. Both draws blocked
all three traps (4.1.3 same-name-same-day, 2.5.3 self-attested with the same
person confirming, 3.3.3 the co-authored pair) and stood both over-refusal
controls (1.1.1 same person on a later day, 2.1.1 self-attested with an
independent confirmer). Draw 2 cites the new field by name in its document
notes — *"second-confirmed by Nkechi Balogun who discloses `authored_fix:
false`"* — so the contract field added in #62 is being read and used, not
ignored in favour of the prose authorship table.

That answers the question the fixture was built to leave open: the field makes
rows 3 and 5 separable in practice, not just in principle.

### `utility-billing-retest` — the scorer has never once scored it correctly

Four draws of this fixture exist across two sessions. All four produced
must-misses; **all four were false.** Three sub-classes, each reproduced:

| Sub-class | What the draw wrote | Token expected |
|---|---|---|
| Inline markup | ``after `report_date` `` | `after report_date` |
| YAML line wrap | `1 random` split across a folded scalar's line break | `1 random` |
| Interpolated specificity | `after the 2026-07-24 report date` | `after the report` |

The third is the model being *more* precise than the token anticipated — it
named the actual date inside the phrase — and the matcher rejected it for it.

## The fix, and what it does not fix

`any_token()` was a plain lowercased substring test. It now normalizes the
prose first: strip the Markdown emphasis and code characters (`` ` `` and
`*`), then collapse every whitespace run to one space. Underscores are
deliberately **not** stripped — `report_date` and `self_attested` are field
names that appear inside tokens.

That closes the markup and line-wrap classes: four of the five false misses.

**It does not close the interpolated-specificity class,** and no attempt was
made to. Fixing that would mean either over-fitting the fixture's token list
to one draw's phrasing, or relaxing the matcher to allow bounded intervening
text — and this scorer already has weak discrimination by its own admission
(fixture #8's metadata records that it keyword-matches the handoff's stated
reason rather than computing independence). Loosening it further to chase one
row would trade a false negative for a false positive. `utility-billing-retest`
draw 2 therefore still reads FAIL, on a miss adjudicated here as the
instrument's, not the model's. Recorded rather than papered over.

## Effect on published rows

Calibration is unchanged: **18/18 CLEAN** before and after, so the fix does
not blunt the instrument's ability to catch a real breaker. Every committed
`acr` row re-scored — see [`rescore-published-rows.md`](rescore-published-rows.md):

| Row | Before | After |
|---|---|---|
| `county-library-retest` d1, d2 (2026-09-03) | PASS | PASS |
| `utility-billing-retest` d1 (phase2) | PASS | PASS |
| `utility-billing-retest` d2 (phase2) | **FAIL** | **WARN** |

The one row that moves is the one whose FAIL was already adjudicated as a
scorer defect in the phase-2 receipts and its PR. The scorer now agrees with
the adjudication that was published beside it.

## Method

Identical to the phase-2 rows, with one correction carried forward: **the
repository root is pinned in the prompt.** The phase-2 opevidence draws left it
implicit and read a checkout three commits behind `main`; that lesson is
applied here, and every draw's Provenance confirms it read from
`/Users/AlexUA_1/claude/accessibility-skills` at `57034be`.

`Agent(subagent_type=general-purpose, model=opus)`, one subagent per draw,
byte-identical prompt within a fixture, fixture staged alone with no metadata
and no rubric, `evals/` and `docs/plans/` and every `*.metadata.yaml` /
`*.rubric.yaml` read-barred, pinned `@openacr/openacr@0.3.8` offered for the
skill's self-validate step, no repo writes, no subagents. Each draw wrote its
final message to an `OUT_PATH` file before sending it; every notification
arrived truncated and every receipt is complete, so the committed `.md` files
are the drafts themselves and each wrapped `-response.json` records its
sha256.

Blindness control: these fixtures' `.md` files carry no answer-key section
(expectations live in the read-barred metadata). Verified with a positive
control — a critic fixture's `## Accessibility Issues` heading matches; all
three staged files score 0.

## What this establishes, and what it does not

The three `acr-reporting` fixtures are followed correctly by opus against the
current instrument, including the contract field #62 added. Fixture #8's
canary fires on all three traps and holds both controls, on both draws.

It says nothing about local detector models on any of the three — none were
drawn, and the plan's routing is hosted-first. It says nothing about the
`a11y-test-operation-evidence` fixtures, which were deliberately not re-run.
And it does not resolve `op-human-signature-only`'s contested OP-OPTION rule
set, which remains the open fixture question from the phase-2 rows.
