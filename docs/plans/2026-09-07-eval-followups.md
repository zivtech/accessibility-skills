# Federal planner parity and attestation regression

The owner selected two unfinished items on 2026-09-07: the cloud runner's
`planner-federal` condition from issue #17, and the missing second-confirmer
authorship fixture from issue #57. Start from `main` at `e85a0e2` in an
isolated worktree; preserve the existing checkout's uncommitted review files.

## Scope

1. Add the crosswalk-supplied condition to the cloud runner's existing Codex
   planner transport. Use the same planner protocol, fixture, and crosswalk
   text as the local condition. Keep the existing plain planner behavior.
2. Add an adversarial ACR fixture for a self-attested closure whose differently
   named second confirmer omits `authored_fix`. The improved term must remain
   a draft gap. A self-attested closure with `authored_fix: false` must stand;
   a non-self-attested closure need not supply that conditional field.

## Acceptance checks

- Federal and plain prompts differ only by the existing crosswalk suffix.
  Fixture inputs remain blind to metadata and rubric expectations.
- Federal and plain runs have distinct result and temporary-message paths,
  cache identity, and scorer selection. New success and error records name
  their condition. Historical plain records without a condition remain usable.
- Scoring the plain lane excludes federal files even though their filenames
  also match the plain lane's glob. Scoring federal results never consumes
  plain results.
- The new fixture has a complete triplet, appears in the runner registry,
  and includes both required-field and valid-control cases with otherwise
  consistent dates, product pins, observations, and confirmer identities.
- Synthetic calibration accepts the honest draft and rejects both admission
  of the incomplete closure and refusal of a valid control. Run the existing
  calibration against the pinned OpenACR CLI as well.
- Deterministic runner tests, fixture validation, scorer smoke tests, skill
  lint, blind-prompt checks, manifest verification, and strict mirror checks
  pass. Independent review examines the plan and resulting diff.

## Boundaries

This adds no Claude API or Gemini planner transport and produces no new model
benchmark rows. It changes no attestation rule and does not promote a skill.
The new fixture contains synthetic evidence, not human confirmations or an
engagement event. Issue #57's real campaign and countersigned roster remain
open. Issue #17's other hosted rows and upstream watch items remain open.

The scorer can check structural placement and reason tokens; it cannot prove
that a model reasoned correctly about authorship. Future model rows still need
their reasons read and adjudicated. Refreshing a current runner hash in a
retained manifest must leave its historical references and hashes unchanged.

## Completion evidence

Implemented the Codex federal single, all-fixture, and scoring commands with
condition-specific output, message, and cache paths. A shared planner-result
reader rejects unfinished, malformed, and mislabeled rows before reuse or
scoring; historical plain rows remain usable. The system prompt matches the
local federal prompt byte for byte.

Added `resident-services-authorship-disclosure` as fixture 9 (the suite's
eighth fixture). Its three complete closure records isolate one missing-field
case and two valid controls. Independent source review corrected abbreviated
closure records and overly broad reason tokens before acceptance. The review
also recomputed all 56 A/AA outcome memberships and the three closure links.

Local validation passed: 13 cloud condition tests, 50 context-guard tests,
22 pinned OpenACR calibration cases (18 existing plus four new cases),
70 scorer smoke cases, and 238 blind prompts. Fixture/registry validation,
manifest integrity and verifier tests, skill lint, client-reference checks,
strict mirror parity and self-tests, Python compilation, and diff checks passed.
CI now runs the cloud tests and the complete synthetic ACR calibration against
`@openacr/openacr@0.3.8`. No model draws were made and historical output and
score files were not changed.
