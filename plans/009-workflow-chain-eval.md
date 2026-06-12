# Plan 009: Design the end-to-end chain eval for /a11y-workflow (design + 3-fixture pilot, gated)

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. This is a DESIGN/SPIKE plan: the deliverable is
> the eval protocol, chain rubrics, extracted targets, and a 3-fixture pilot
> — NOT a full benchmark run. The full run is a separate, operator-approved
> follow-up. When done, update the status row for this plan in
> `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat de0031f..HEAD -- .claude/skills/a11y-workflow/SKILL.md .claude/teams/a11y-workflow.md evals/suites/`
> If the workflow skill or team file changed since `de0031f`, re-read them
> and adjust the stage boundaries below before designing; on structural
> change (steps added/removed), STOP and report.

## Status

- **Priority**: P3
- **Effort**: M (design + extraction S–M; pilot is 3 operator-approved Opus-chain sessions)
- **Risk**: LOW (new eval assets only; one scorer-adjacent helper script)
- **Depends on**: none hard (soft: plan 001's `validate_fixtures.py` exists and must IGNORE the new `evals/suites/chain/` — confirm, don't assume)
- **Category**: direction (tests)
- **Planned at**: commit `de0031f`, 2026-06-11

## Why this matters

Every individual agent in the a11y-workflow team is benchmarked (33-fixture critic, 25-fixture perspective, planner per plan 006) — but the PRODUCT is the chain, and the chain's record is thin: Phase 7B validated scout→critic on 3 fixtures (`ollama/BENCHMARK.md:865`, "3/3 PASS"); the full scout→planner→critic→[audit] path has no fixture-based pass/fail record at all. The risk concentrates at the integration points the single-agent benchmarks cannot see: does the critic's alarm output actually trigger the audit when it should (and NOT when it shouldn't)? Does the planner's file-based handoff survive? Does context compression between stages drop the load-bearing findings? This plan designs the measurement: stage-boundary rubrics grounded in ground truth the suites already contain, runnable through the REAL mechanism (Claude Code subagents in a live session — the production path), with a 3-fixture pilot to validate the instrument before anyone pays for a full run.

## Current state

Verified at commit `de0031f`:

- `.claude/skills/a11y-workflow/SKILL.md` — the chain under test (Mode 1, steps 1–5 are the pre-implementation chain this eval covers):
  - Step 1 Scout (haiku): returns recon ≤1500 chars — file paths, component type, ARIA inventory, complexity.
  - Step 2 Planner (opus): consumes scout output verbatim; writes plan to `docs/a11y-plans/YYYY-MM-DD-<feature>-a11y-plan.md`.
  - Step 3 Critic (opus): reads plan file + source paths; must "Flag perspective alarm levels (LOW/MEDIUM/HIGH) for each of the 7 perspectives".
  - Step 4 Perspective audit: CONDITIONAL — "Only if the critic flags any perspective at MEDIUM or HIGH alarm"; receives only extracted alarm levels + findings (≤1500 chars).
  - Context rule: output >2K chars → file handoff; ≤2K → prompt injection (SKILL.md "Size budget rule").
  - Steps 6–9 (test → implementation critique) need an implementation to exist — OUT of this eval's scope (fixtures are specs/components, not deployed apps).
- `.claude/teams/a11y-workflow.md` — escalation signals table (CLEAN verdict → Opus re-run; perspective alarm MEDIUM/HIGH → invoke audit, always Opus).
- Ground truth already in the suites:
  - `evals/suites/perspectives/fixtures/*.metadata.yaml` carry `expected_alarm_levels` per perspective (the scorer reads them at `score_perspective.py:49-58`) — this makes the **escalation decision** (the chain's most important branch) directly checkable.
  - `evals/suites/a11y-critic/fixtures/*` carry must-find/CLEAN/ADVERSARIAL ground truth for the critic stage.
  - Perspective fixture `.md` files embed component code with `// BUG:` hint comments; `evals/suites/perspectives/strip_bug_comments.py` already strips them for blind runs (pattern at `strip_bug_comments.py:18-65`) — reuse the pattern, do NOT hand the workflow a fixture file with bug hints in it.
- The workflow takes a FILE/COMPONENT TARGET (e.g. `src/components/Modal.tsx`), not a fixture markdown — chain targets must be extracted from fixtures into real component files.
- Scoring tools that can be reused per-stage: `score_perspective.py`'s alarm/coverage logic concepts; calibration scoring convention from root `README.md:243`: alarm exact match = 1.0, ±1 level = 0.5, off-by-2 = 0.0.
- Cost reality: one full chain ≈ 1 Haiku + 2 Opus calls (+1 Opus if audit triggers). Pilot of 3 ≈ ~8–10 Opus-tier subagent calls. Operator approval required (Opus spend).

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Extract targets | `python3 evals/suites/chain/extract_targets.py` (created in step 2) | targets written, BUG-comment-free |
| No bug hints leaked | `grep -rn "BUG:" evals/suites/chain/targets/` | no matches |
| YAML parse | `python3 -c "import yaml,glob; [yaml.safe_load(open(p)) for p in glob.glob('evals/suites/chain/rubrics/*.yaml')]; print('ok')"` | `ok` |
| Suite checker unaffected | `python3 scripts/validate_fixtures.py` (if plan 001 ran) | exit 0 |

## Scope

**In scope**:
- `evals/suites/chain/` (create): `CHAIN-EVAL-PROTOCOL.md`, `extract_targets.py`, `targets/<fixture-id>/` (extracted component files), `rubrics/<fixture-id>.chain.yaml` (8 files), `RESULTS-TEMPLATE.md`
- Pilot artifacts: `evals/suites/chain/pilot/` (3 session records, scored)

**Out of scope** (do NOT touch):
- `.claude/skills/a11y-workflow/SKILL.md`, agents, team file — the chain is measured AS-IS; if the eval reveals defects, those become findings, not in-flight edits.
- Existing suites' fixtures/metadata/rubrics — chain rubrics REFERENCE them, never modify them.
- The full 8-fixture run — pilot (3) only, then STOP for operator review.
- Steps 6–9 of the workflow (implementation/test phases) — pre-implementation chain only.

## Git workflow

- Branch: `advisor/009-workflow-chain-eval`
- Conventional commits, e.g. `test: add chain eval protocol and rubrics`.
- Do NOT push or open a PR unless the operator instructed it.

## Steps

### Step 1: Select the 8 chain fixtures and write the protocol

Selection (rationale: every chain branch gets coverage, ground truth already exists):

| Chain fixture | Source suite / id | Why |
|---|---|---|
| 1 | perspectives / `modal-broken-focus-trap` | HAS-BUGS, keyboard+SR alarms expected → audit MUST trigger |
| 2 | perspectives / `product-carousel-autoplay` | vestibular HIGH expected → audit MUST trigger on a non-keyboard perspective |
| 3 | perspectives / `video-tutorial-no-captions` | auditory HIGH → tests a perspective the critic historically under-weights |
| 4 | perspectives / `login-form-clean` | CLEAN → audit must NOT trigger; false-escalation probe |
| 5 | perspectives / `article-page-clean` | CLEAN #2 → second false-escalation probe |
| 6 | a11y-critic / `tabbed-nav-vs-tab-pattern` | ADVERSARIAL → verdict calibration through the chain |
| 7 | a11y-critic / `app-focus-order-illogical` | FLAWED → plan-level reasoning, not attribute-spotting |
| 8 | a11y-critic / `toast-notification-no-role` | HAS-BUGS with the known `role="alert"` discriminator item |

(If any id is absent on disk, pick the nearest same-category fixture and record the substitution — ids verified present in the registry lists at `run_benchmark.py:54-127` at planning time.)

Write `evals/suites/chain/CHAIN-EVAL-PROTOCOL.md` defining the FIVE measured boundaries, each with its scoring dimensions:

- **S1 Scout output**: ≤1500 chars (hard); names ≥80% of target files; component type correct vs fixture metadata. Score 0–2.
- **S2 Planner handoff**: plan file exists at the documented path pattern; contains the planner's 9 phase sections; addresses the component the scout described (not a hallucinated one). Score 0–2.
- **S3 Critic alarm accuracy**: per-perspective alarm vs the perspective fixture's `expected_alarm_levels` using the calibration convention (exact 1.0 / ±1 0.5 / else 0). For critic-suite fixtures (6–8) where no `expected_alarm_levels` exist: score S3 on must-find detection against the fixture's `must_find` list instead, and say so in the rubric. Score = mean.
- **S4 Escalation decision**: audit invoked ⟺ any expected alarm is MEDIUM/HIGH. Binary 0/1 — this is the headline number.
- **S5 Audit scope adherence** (only when audit runs): audited perspectives ⊆ escalated perspectives (no LOW leakage — same concept as `score_perspective.py:102-114`); must-find items for escalated perspectives detected. Score 0–2.
- **Chain-survival check**: for fixtures 1–3 and 8, ONE named "tracer finding" (the fixture's most important must-find item, copied verbatim into the rubric) must still be present in the LAST stage's output — measuring whether compression between stages dropped the load-bearing finding. Binary.
- Per-fixture PASS = S4 correct AND no stage scored 0 AND tracer survives (where defined).

**Verify**: protocol file exists; every dimension above appears; the 8-row fixture table with rationale is in it.

### Step 2: Extract chain targets from fixtures

Write `evals/suites/chain/extract_targets.py` (stdlib only, modeled on `strip_bug_comments.py:18-65`): for each of the 8 fixtures, read the source fixture `.md`, extract fenced code blocks, strip `// BUG:` and `/* BUG: */` comments using the exact patterns from `strip_bug_comments.py`, and write real component files to `evals/suites/chain/targets/<fixture-id>/` (one file per code block; name from the block's language — `component.jsx`, `styles.css`, `index.html` — plus a `README.md` carrying the fixture's expected-behavior prose so the scout has context a real repo would have). Deterministic: re-running overwrites identically.

**Verify**: `python3 evals/suites/chain/extract_targets.py` → exit 0, prints per-fixture file counts; `grep -rn "BUG:" evals/suites/chain/targets/` → no matches; run it twice → `git status` shows no changes after the second run.

### Step 3: Author the 8 chain rubrics

`evals/suites/chain/rubrics/<fixture-id>.chain.yaml`, schema (documented at the top of the protocol file):

```yaml
chain_fixture: modal-broken-focus-trap
source_suite: perspectives
source_metadata: evals/suites/perspectives/fixtures/modal-broken-focus-trap.metadata.yaml
target_dir: evals/suites/chain/targets/modal-broken-focus-trap/
expected_escalation: true            # derived from source expected_alarm_levels
expected_alarm_levels: {}            # COPY from source metadata (duplicated for self-containment, with source path above as the authority)
tracer_finding: "<verbatim most-important must_find description from source metadata>"
component_type: "modal dialog"       # for S1 scoring
stage_notes: |
  Anything fixture-specific a scorer needs (e.g. fixture 6 is ADVERSARIAL —
  acceptable critic verdicts are ACCEPT-WITH-RESERVATIONS or REVISE).
```

Populate from the source metadata files — every copied value must match its source (spot-check command below).

**Verify**: all 8 parse (command table); for two of them, manually diff `expected_alarm_levels` against the source metadata → identical. If plan 001's `validate_fixtures.py` exists, run it → still exit 0 (chain/ must not trip the triplet checker; if it does, the checker's suite list needs the chain dir excluded — that is a one-line fix WITHIN validate_fixtures.py explicitly permitted here).

### Step 4: Results template + scoring helper

1. `evals/suites/chain/RESULTS-TEMPLATE.md`: per-fixture table (S1–S5, tracer, PASS/FAIL, session pointer, model tiers used, wall-clock), plus an aggregate block (S4 escalation accuracy n/8 headline, mean stage scores, tracer survival rate).
2. OPTIONAL helper (only if cheap): `evals/suites/chain/score_chain.py` that takes a filled-in session record (the operator saves scout/planner/critic/audit outputs as four text files per fixture) and computes S3–S5 mechanically using the rubric YAML; S1–S2 stay human-scored. If this exceeds ~150 lines, skip it — manual scoring of 8 fixtures is cheaper than maintaining a scorer; record the decision.

**Verify**: template exists; if the helper was built, run it against a hand-made dummy session record → plausible scores; if skipped, the protocol file says scoring is manual and why.

### Step 5: PILOT — 3 fixtures through the real chain (OPERATOR GATE)

STOP and get operator approval first (Opus spend, ~3 chains). Pilot set: fixture 1 (`modal-broken-focus-trap`, must-escalate), fixture 4 (`login-form-clean`, must-NOT-escalate), fixture 6 (`tabbed-nav-vs-tab-pattern`, ADVERSARIAL verdict).

Per fixture, in a live Claude Code session (the production mechanism — no API-side simulation):
1. `/a11y-workflow full evals/suites/chain/targets/<fixture-id>/` (the extracted target dir).
2. Save each stage's raw output to `evals/suites/chain/pilot/<fixture-id>/{scout,planner-plan-path,critic,audit}.md` (audit file only if invoked; for the planner, record the path of the plan file it wrote and copy that file in).
3. Score against the rubric; fill a RESULTS-TEMPLATE row.

Then write `evals/suites/chain/pilot/PILOT-REPORT.md`: scores, **instrument findings** (was anything unscoreable? did a dimension fail to discriminate? did the protocol miss a boundary that mattered in practice?), and chain findings if any (e.g. escalation fired wrong) — clearly separated, because instrument defects get fixed in this plan's files, chain defects get REPORTED, not fixed (the workflow is out of scope).

**Verify**: 3 scored rows; pilot report present; every score traceable to a saved stage output; both escalation probes conclusive (fixture 1 escalated, fixture 4 did not — if either went the other way, that IS the result: record it as a chain finding, do not re-run hoping for different).

### Step 6: Handoff for the full run

Update `CHAIN-EVAL-PROTOCOL.md` with any instrument revisions from the pilot, then add a final section "Full run (pending)": the remaining 5 fixtures, expected cost, and the rule that results publish to BENCHMARK.md append-only as `## Chain eval (a11y-workflow, 8 fixtures)` only after all 8 are scored. The full run itself is OUTSIDE this plan — mark this plan DONE at this point.

**Verify**: protocol's revision log lists pilot-driven changes (or states "none"); plans/README.md row updated.

## Test plan

- `extract_targets.py` determinism check (step 2) and the BUG-leak grep are the automated tests.
- The pilot IS the instrument's validation — 3 fixtures chosen to hit both escalation branches and the verdict-calibration case.
- Rubric-to-source consistency spot-checks (step 3) guard the duplicated ground truth.

## Done criteria

ALL must hold:

- [ ] `CHAIN-EVAL-PROTOCOL.md` defines S1–S5 + tracer + per-fixture PASS rule and the 8-fixture table
- [ ] `extract_targets.py` runs deterministically; targets contain zero `BUG:` strings
- [ ] 8 chain rubrics parse; spot-checked values match source metadata
- [ ] Results template exists; scoring helper built (≤150 lines) or explicitly waived in the protocol
- [ ] Pilot ran with operator approval; 3 scored rows + pilot report committed; escalation probes recorded as-is
- [ ] No file under `.claude/` was modified; existing suites untouched (`git status` check)
- [ ] `python3 scripts/validate_fixtures.py` (if present) exits 0
- [ ] `plans/README.md` status row updated

## STOP conditions

Stop and report back (do not improvise) if:

- The workflow skill's Mode 1 steps changed structurally since `de0031f` (stage list differs from "Current state").
- Any selected fixture id is missing AND no same-category substitute exists.
- The pilot reveals the workflow cannot consume a directory target at all (e.g. scout requires a git repo context the targets lack) — that is a design finding about the eval OR the workflow; present both interpretations to the operator rather than patching either side.
- Anyone (including you) proposes editing the a11y-workflow skill mid-eval to make a pilot pass — measurement first, fixes as separate follow-ups.
- Operator approval for the pilot is not obtainable — deliver steps 1–4 as the design artifact and mark the plan DONE-DESIGN-ONLY in the index.

## Maintenance notes

- The chain rubrics duplicate `expected_alarm_levels` from source metadata for self-containment; the `source_metadata` path is the authority — if a source fixture's ground truth changes, regenerate the chain rubric (a future `validate_fixtures.py` extension could diff them; note it as a candidate check).
- S4 (escalation accuracy) is the number to watch over time — it is the chain's reason to exist. If a future workflow change (e.g. new escalation signals in the team file) lands, re-run at least fixtures 1 and 4 before trusting the chain again.
- The full 8-fixture run + BENCHMARK.md publication is the natural follow-up plan; its cost is known after the pilot.
- Reviewer should scrutinize: tracer-finding choices (must be the fixture's genuinely load-bearing item, not an easy keyword) and that CLEAN probes weren't given any hint of their cleanliness in the extracted targets.
