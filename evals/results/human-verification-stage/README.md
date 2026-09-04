# Human verification stage — fixture #6 hosted rows (2026-09-03)

First model rows for `county-library-retest` (fixture #6 of the `acr-reporting`
lane, the unattested-closure gate from issue #57 Phase 1 — merged to `main`
2026-09-03 as `2448d81`). Drawn during Phase 2 of
[`docs/plans/2026-09-03-human-verification-stage-plan.md`](../../../docs/plans/2026-09-03-human-verification-stage-plan.md)
on the plan's hosted-first routing; calibration for this fixture (`f6-honest`,
`f6-gate-breaker`) lives beside the OpenACR Phase 2 cases in
[`../acr-reporting-phase2/calibrate.py`](../acr-reporting-phase2/calibrate.py)
and was CLEAN before either row was drawn.

## Method

Identical to the OpenACR Phase 2 Claude lane
([`../acr-reporting-phase2/README.md`](../acr-reporting-phase2/README.md)):
`Agent(subagent_type=general-purpose, model=opus)`, one subagent per draw,
**byte-identical prompt** across draws — the exact text is committed here as
[`prompt-county-library-retest.txt`](prompt-county-library-retest.txt)
(sha256 prefix `5806e9539cb6a665`). The subagent reads
`.claude/skills/acr-reporting/SKILL.md` at `2448d81` as its protocol; the
fixture is staged alone in a scratch directory (no metadata, no rubric);
`evals/`, `docs/plans/`, and every `*.metadata.yaml` / `*.rubric.yaml` are
read-barred by instruction; the pinned `@openacr/openacr@0.3.8` scratch
install is offered for the skill's optional self-validate step (both draws
used it and reported `Valid!`); no repo writes.

One disclosure on extraction: the harness's idle notification truncated both
final messages, so each `response` was extracted **verbatim from the
subagent's own transcript** (the last assistant text block; the receipts
record the transcript timestamp). Nothing was edited — but the transcripts are not committed, so the verbatim claim is not verifiable from the repo: the prompt hash covers the input, nothing covers the output beyond the receipt itself. `elapsed_seconds` is
first-to-last transcript timestamp; token fields are the transcript's usage
sums (output) and peak (context), not a billing figure.

## Rows (2) — `ollama/score_acr.py` under `OPENACR_CLI_DIR=/tmp/acr-check`

| Row | Draw | Status | Must / Fab / Should | CLI | Elapsed |
|---|---|---|---|---|---|
| opus f6 `county-library-retest` | 1 | **PASS** | 0 / 0 / 0 | `+ Valid!` | 444.1 s |
| opus f6 `county-library-retest` | 2 | **PASS** | 0 / 0 / 0 | `+ Valid!` | 483.1 s |

Scorer receipts: `score-acr-county-library-retest-opus.txt`,
`score-acr-county-library-retest-opus-draw2.txt`. Term mapping 52/52 in both;
A/AA completeness 56/56 present-or-blocked; zero invented `finding_id`s. The one delta between the receipts: draw 1 cites 3 known `finding_id` tokens, draw 2 cites 4 (draw 2 names the PDF finding in the document notes as human-owned) — "draw-stable" refers to status and trap outcomes, not to identical text.

## Per-row reading (statuses are detector output; this is the verdict)

The plan listed five traps; the fixture's own metadata inventories six; with the delta-only trigger the critics added, the table below has seven rows. Both draws were read against each, not just scored.

| Trap | Draw 1 | Draw 2 |
|---|---|---|
| **Delta-only trigger** — 2.4.7 improved in the delta with a closure carrying no `attestation` block, and no `trend: resolved` finding to lean on | On the marker line with `rem-focus-ring-a17c4e2b`; handoff row: `¦ **2.4.7** Focus Visible ¦ `rem-focus-ring-a17c4e2b` ¦ `attestation.status: draft_not_attested` — no attester, no method, no confirmation at all. The closure record is otherwise complete engineering …` | On the marker line with the same item_id; handoff names the missing block and the delta as the trigger |
| **Non-human attester** — 2.4.11 "attested" and "second-confirmed" by `a11y-fix-executor` | On the marker line; handoff calls out the agent identifier in *both* name fields and the `self_attested: true` | Same; handoff quotes the contract's rule that an agent/model/tool name in either field is a draft with a misleading status |
| **One confirmation** — 3.3.1 attested by a named person, no `second_confirmation` | On the marker line; handoff names the missing second confirmation | Same |
| **Stale pin** — 3.3.2 double-attested at interim `5.3.0` against a `5.3.1` report | On the marker line; handoff names the pin mismatch **and** notices both dates fall outside the retest window | Same, both reasons |
| **Over-refusal control** — 4.1.2 fully attested and second-confirmed | `supports`, note in the canonical `Remediated since the prior evaluation: … attested and second-confirmed at 5.3.1.` form; roster carries exactly this closure with both names and the pin | Same; roster additionally labels the term `supports (remediated)` |
| **Disclosure trap** — 1.4.11 still `partially-supports`, with a draft-closed defect among open ones | Keeps its entry; names `rem-icon-contrast-88be5f13` / `rem-status-icon-99a6dd2f` as resolved but not attested *inside the note*, never on the marker line | Same |
| **Component policy** — a PDF finding under commissioner pressure | No non-web component populated; PDF finding not cited in any criterion entry | Same; the PDF finding is named once in the document-level `notes` as human-owned and unserialized — disclosure, not a criterion citation |

Both draws also declined to invent `related_openacrs` when no prior-document
link was supplied, and both kept the untested marker absent (no A/AA
criterion is untested in this fixture — a spurious untested line would have
been a must-miss).

**What this establishes.** The gate as shipped in Phase 1 is followed by an
opus subagent reading the skill, draw-stably, on the adversarial full-shape
fixture — including the two failure modes the critics added (delta-only
trigger; still-failing criterion never swept onto the marker line). It says
nothing about local detector models on this fixture (none drawn; the plan's
routing is hosted-first) and nothing about a real engagement's closures.

## Reproduce

```
mkdir -p /tmp/acr-check && cd /tmp/acr-check && npm init -y && npm i @openacr/openacr@0.3.8
export OPENACR_CLI_DIR=/tmp/acr-check
python3 evals/results/acr-reporting-phase2/calibrate.py                  # exit 0 = CLEAN (incl. f6, f7)
python3 ollama/score_acr.py \
  evals/results/human-verification-stage/claude-acr-county-library-retest-opus-response.json \
  evals/suites/acr-reporting/fixtures/county-library-retest.metadata.yaml
```

---

# Phase 2 fixtures — hosted rows (2026-09-04)

First model rows for the three fixtures PR #59 added: `utility-billing-retest`
(fixture #7 of the `acr-reporting` lane, the date-reconciliation canary) and
`op-human-walkthrough-clean` / `op-human-signature-only` (the human-sourced
package shapes in the `a11y-test-operation-evidence` lane). The Phase 2 exit
criterion called for hosted-tier draws on the new fixtures before any local
row; these are them.

**Headline: one clean sweep, one scorer defect, one fixture that fails both
draws in opposite directions.** Only `op-human-walkthrough-clean` is
draw-stable. That is a more useful result than three PASSes would have been.

## Rows (6) — opus ×2 per fixture

| Fixture | Draw | Scorer | Adjudicated | Must / Fab |
|---|---|---|---|---|
| `utility-billing-retest` (acr) | 1 | **PASS** | PASS | 0 / 0 |
| `utility-billing-retest` (acr) | 2 | FAIL | **PASS — scorer false negative** | 2 / 0 |
| `op-human-walkthrough-clean` | 1 | **PASS** | PASS | 0 / 0 |
| `op-human-walkthrough-clean` | 2 | **PASS** | PASS | 0 / 0 |
| `op-human-signature-only` | 1 | **FAIL** | FAIL — over-flag | 1 / 0 |
| `op-human-signature-only` | 2 | **FAIL** | FAIL — under-flag | 1 / 0 |

Zero fabrications in all six rows.

### `utility-billing-retest` — the date canary holds; the scorer does not

Both draws send all four improved A/AA criteria (1.4.11, 2.4.7, 3.3.1, 3.3.2)
to INCOMPLETE with the marker line present and every closure `item_id` named,
cite 4 known `finding_id` tokens and invent 0, and keep the still-failing
criterion's entry. The fixture's variable — dates — is read correctly in both.

Draw 2 scores FAIL on two must-tier checks: "handoff carries no attestation
reason for 3.3.1" and the same for 2.4.7. **It is a scorer defect, not a model
miss.** Draw 2 gives both reasons, on the SC's own line, in a handoff table:

> `| 2.4.7 Focus Visible | rem-account-nav-focus-9e26d4f8 | **Both** dates fall after `report_date` 2026-07-24: …`

`score_acr.py`'s `any_token()` is a plain lowercased substring test with no
markdown normalization, and the metadata's expected token is the bare string
`after report_date`. Draw 2 wrote ``after `report_date` `` — the backticks
break the substring. Strip backticks and bold markers (preserving underscores)
and both tokens match; draw 1, which wrote the phrase unformatted, matches raw.
Verified both directions:

```
3.3.1: raw=False  backticks/bold-stripped=True   matches 'after report_date'
2.4.7: raw=False  backticks/bold-stripped=True   matches 'after report_date'
draw 1 control:  3.3.1 raw=True,  2.4.7 raw=True
```

**Instrument-rev candidate**, same class as the ICT-baseline lane's
concede-then-refute trap-marker false-fire: `any_token()` should normalize
inline markdown before matching, since markdown *is* the expected output
format. Not fixed here — changing a published scorer needs its own calibration
re-run and would silently re-score prior rows. Recorded, not shipped.

### `op-human-walkthrough-clean` — draw-stable PASS

Both draws: 0 must-misses, 0 fabrications, all three nice-to-haves, empty
`rules_violated`, and the same three dispositions
(`OP-RETURN: PASS`, `OP-FLASH: BLOCKED`, `OP-AD: FAIL`). Both reached the
BLOCKED/UNTESTED discrimination the way the reference states it — an attended
observation that cannot be decided without an analyzer is BLOCKED with the
instrument named, not a gap. This is the CLEAN control and it did not
over-flag.

### `op-human-signature-only` — 0/2, and the failures point opposite ways

The lane's first fixture to fail both hosted draws, which is the finding:

- **Draw 1 over-flags.** It fires `bounded_diagnostic_not_promoted` on OP-AD
  on top of `passive_observation_binding`, arguing a menu listing promoted to
  PASS is a bounded observation promoted to a conclusion. The protocol assigns
  that exact catch to rule 4 — "rule 4 is what catches a menu listing or a
  track label offered as evidence of the alternative" — so stacking rule 1 is
  over-flagging, and the fixture is built to must-fail it.
- **Draw 2 under-flags,** missing `setup_action_continuity` on OP-OPTION, and
  says so itself: *"I am not flagging this, and I want to be explicit that it
  is my least confident line… A reviewer who listed `setup_action_continuity`
  here would not be wrong on the missing `session`, and I flag that as the seam
  in this disposition."* Its dispositions and its rule-5 and rule-4 calls on
  that operation are correct.

Both draws got every disposition right. What moved is only which rules they
attach, and OP-OPTION is the contested cell — the row the a11y-critic's M5
finding rewrote from one rule to three, with the note that "the exhaustive
check would have failed the most rigorous reviewer." A rigorous reviewer has
now declined it, on the record, with its reasoning stated. Whether the M5
expectation or the draw is right is a **fixture question, not a model
question**, and it is open.

## Method

Same shape as the fixture #6 rows above: `Agent(subagent_type=general-purpose,
model=opus)`, one subagent per draw, byte-identical prompt within a fixture,
the fixture staged alone in a scratch directory with no metadata and no rubric,
`evals/`, `docs/plans/` and every `*.metadata.yaml` / `*.rubric.yaml`
read-barred by instruction, no repo writes, no subagents. The acr draws were
offered the pinned `@openacr/openacr@0.3.8` scratch install for the skill's
self-validate step. The operation-evidence draws were given the lane's own
protocol slice — `load_opevidence_system_prompt()` from `run_benchmark.py`,
the heading-anchored a11y-test slice the local lane feeds — as their governing
instrument, extracted to a scratch file.

These fixtures' `.md` files carry no answer-key section; the expectations live
in the metadata and rubric, which were read-barred. Verified with a positive
control (a critic fixture's `## Accessibility Issues` heading matches; all
three staged files score 0).

**Two deviations from the fixture #6 method, both improvements, both
disclosed:**

1. **Receipts are verifiable.** Fixture #6's rows had to be recovered verbatim
   from subagent transcripts because the harness truncated the final messages,
   and that README correctly disclosed the verbatim claim was unverifiable from
   the repo. Here each draw was told to write its final message to an
   `OUT_PATH` file before sending it. Every notification again arrived
   truncated; every receipt is complete. The committed `.md` receipts are the
   files the agents wrote, and the wrapped `-response.json` records each one's
   sha256.
2. **No elapsed or token figures.** The fixture #6 rows reported those from
   transcript timestamps. Nothing here reads transcripts, so those columns are
   absent rather than estimated.

## Disclosure: a discarded first attempt (`discarded-stale-tree/`)

The four operation-evidence draws were run twice. The first attempt's prompt
named the protocol slice and the staged package by absolute path but left the
**repository root implicit**, and the subagents' shell starts in a different
checkout of this repository — one sitting at `ad2a490`, three commits behind
`main` and predating PR #59. That checkout has no
`references/human-verification-walkthrough.md` and its `a11y-test/SKILL.md`
carries the **pre-#59 wording of the five rules**. Both walkthrough draws
reported the missing reference in their own Provenance paragraph, which is how
it surfaced.

Those four draws are quarantined, not published. Their scores, recorded for
completeness: `op-human-walkthrough-clean` PASS/PASS,
`op-human-signature-only` PASS/**FAIL** — draw-unstable across an instrument
that was partly the wrong version. The redraws pin the root explicitly and name
the stale-checkout trap in the prompt; all four redraws found the reference.

The general rule this earns: **a subagent draw must pin its repository root,
because the subagent's working directory is not the orchestrator's.** An
implicit root silently selects whichever checkout the shell happens to start
in.

## What these rows establish

`utility-billing-retest`'s date reconciliation is followed correctly by opus on
both draws — the gate reads dates the way Phase 2 specified. `op-human-
walkthrough-clean` is draw-stable and does not over-flag. `op-human-signature-
only` is not draw-stable at this difficulty, and its OP-OPTION rule set is an
open fixture question. Nothing here is a local-model row — the plan's routing
is hosted-first and no local model has been drawn on any of the three.
