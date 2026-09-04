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
record the transcript timestamp). Nothing was edited. `elapsed_seconds` is
first-to-last transcript timestamp; token fields are the transcript's usage
sums (output) and peak (context), not a billing figure.

## Rows (2) — `ollama/score_acr.py` under `OPENACR_CLI_DIR=/tmp/acr-check`

| Row | Draw | Status | Must / Fab / Should | CLI | Elapsed |
|---|---|---|---|---|---|
| opus f6 `county-library-retest` | 1 | **PASS** | 0 / 0 / 0 | `+ Valid!` | 444.1 s |
| opus f6 `county-library-retest` | 2 | **PASS** | 0 / 0 / 0 | `+ Valid!` | 483.1 s |

Scorer receipts: `score-acr-county-library-retest-opus.txt`,
`score-acr-county-library-retest-opus-draw2.txt`. Term mapping 52/52 in both;
A/AA completeness 56/56 present-or-blocked; zero invented `finding_id`s.

## Per-row reading (statuses are detector output; this is the verdict)

The fixture sets five traps. Both draws were read against each, not just scored.

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
