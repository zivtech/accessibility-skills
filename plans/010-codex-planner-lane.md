# Plan 010: Codex planner lane — add a planner path to the cloud benchmark runner

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving on. If
> anything in "STOP conditions" occurs, stop and report — do not improvise.
> THIS PLAN HAS ONE COST GATE (step 5) — the full 25-fixture run consumes
> ChatGPT/Codex plan quota and 30–75 min of wall-clock; never start it
> without the operator's (Alex's) recorded approval. When done, update this
> plan's status row in `plans/README.md`.
>
> **Drift check (run first)**:
> `git log --oneline -1 -- ollama/run_cloud_benchmark.py` and confirm the file
> contains `run_codex(`, `output_path("codex"...` with a `skill` parameter,
> `write_json_atomic`, and `RESULTS_DIR` (plans 002/003 landed on main at
> `80a40e6`). If the `skill` parameter or atomic writes are absent, STOP —
> dependency not met.

## Status

- **Priority**: P3
- **Effort**: S–M (adapter S; run is wall-clock-bound)
- **Risk**: LOW-MED (no API key spend — codex CLI uses ChatGPT auth; risk is
  quota burn and CLI flakiness)
- **Depends on**: plans 002/003/006 (all merged to main at `80a40e6`)
- **Origin**: plan 006 Phase D scoped the codex planner lane OUT; operator
  requested this follow-up on 2026-06-12.
- **Planned at**: commit `80a40e6`, 2026-06-12

## Why this matters

Plan 006 Phase D defined two hosted planner lanes. The Claude lane runs via
Claude Code subagents (the production mechanism — see BENCHMARK.md). The
Codex lane could not run because `run_cloud_benchmark.py` has critic and
perspective paths for codex but no planner path. This plan adds it, so the
planner benchmark gains a second hosted family and the cross-model planner
table stops being single-hosted-lane.

## Current state (verified at `80a40e6`)

- `ollama/run_cloud_benchmark.py`:
  - `CODEX_TIERS` (`:95-100`): `5.2`, `5.2-low`, `5.5`, `5.5-low` —
    `{name, model, effort, label}`.
  - `run_codex(tier, fixture_id, system_prompt, user_prompt, skill="critic")`
    (`:337`): shells out to `codex exec -m <model> --sandbox read-only
    --ephemeral --ignore-rules --ignore-user-config --skip-git-repo-check`,
    full prompt on stdin, 300s timeout, atomic JSON result write. **The
    preamble is critic-specific** ("You are an accessibility design
    reviewer…") — hardcoded inside `run_codex`.
  - Skill wrappers to mirror: `run_codex_critic` (`:447`),
    `run_codex_perspective` (`:454`) — each builds skill-specific
    system/user prompts then delegates to `run_codex`.
  - `output_path(platform, tier_name, fixture_id, skill)` (`:219`) and
    `result_exists(...)` (`:226`) already take `skill` — planner files will
    name as `codex-bench-planner-{fixture}-{tier}-response.json` (verify the
    exact pattern in `output_path` before relying on it).
  - `score_codex_results(skill="critic")` (`:508`) — verify whether it
    dispatches to `score_planner.py` for `skill="planner"`; wire if not.
- `ollama/run_benchmark.py` has the planner constants to mirror:
  `PLANNER_PROMPT_PREFIX` (`:38`), `PLANNER_FIXTURES` (25 ids, `:40-66`),
  `PLANNER_FIXTURES_DIR` (`:34`).
- `ollama/score_planner.py` scores any JSON with a `response` key against
  the fixture metadata; prints `Score: N/M` + `Status: PASS|NEEDS REVIEW`.
- Known deferred item (plans/README.md): runner code duplication. Mirror the
  three planner constants into `run_cloud_benchmark.py` with a
  `# KEEP IN SYNC with run_benchmark.py` comment rather than importing —
  consistent with the file's current style; consolidation is the separate
  deferred refactor.

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Compile | `python3 -m py_compile ollama/run_cloud_benchmark.py` | exit 0 |
| Codex CLI present | `codex --version` | version string |
| Smoke + fixtures | `bash scripts/smoke_scorers.sh && python3 scripts/validate_fixtures.py` | exit 0 |
| Single planner run | `python3 ollama/run_cloud_benchmark.py codex-planner 5.2-low keyboard-breadcrumb` | result JSON written |
| Score one | `python3 ollama/score_planner.py "$BENCHMARK_RESULTS_DIR/codex-bench-planner-keyboard-breadcrumb-5.2-low-response.json" evals/suites/a11y-planner/fixtures/keyboard-breadcrumb.metadata.yaml` | `Score:` + `Status:` lines |

## Scope

**In scope**:
- `ollama/run_cloud_benchmark.py`: planner constants, `load_planner_system_prompt()`,
  skill-aware preamble, `run_codex_planner()`, dispatch commands, scoring dispatch
- `ollama/README.md`: codex planner commands
- `evals/results/codex-planner/` (created at step 5 — committed raw JSONs)
- `ollama/BENCHMARK.md`: append-only codex planner section (step 6)

**Out of scope** (do NOT touch):
- Claude planner lane (already run via subagents — different mechanism by design)
- Gemini anything (plan 007), scorers, fixtures, existing BENCHMARK tables
- Runner deduplication refactor (separate deferred item)
- Parallel codex execution — see sequential note in step 5

## Git workflow

This work commits directly to `main` of the **a11y-meta-skills repo** (the
advisor/* branch pattern ended when plans 001–009 merged). Conventional
commits, e.g. `feat: add codex planner lane to cloud benchmark runner`.
Push only after step-4 verification passes.

## Steps

### Step 1: Mirror the planner constants (~10 min)

In `run_cloud_benchmark.py`, near `CRITIC_PROMPT_PREFIX`, add (verbatim from
`run_benchmark.py:34-66`, with sync comment):

```python
# KEEP IN SYNC with run_benchmark.py (planner constants)
PLANNER_FIXTURES_DIR = os.path.join(BASE_DIR, "..", "evals", "suites", "a11y-planner", "fixtures")
PLANNER_PROMPT_PREFIX = "Plan the accessible implementation for the following component or feature. Execute all phases of the planning protocol.\n\n"
PLANNER_FIXTURES = [ ... 25 ids, copied exactly ... ]
```

Add `load_planner_system_prompt()` mirroring `load_critic_system_prompt()`
(`:160`) but reading `.claude/skills/a11y-planner/SKILL.md`, stripping
frontmatter identically.

**Verify**: `python3 -m py_compile ollama/run_cloud_benchmark.py` → exit 0;
`python3 -c "import importlib.util,sys; spec=importlib.util.spec_from_file_location('r','ollama/run_cloud_benchmark.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); print(len(m.PLANNER_FIXTURES))"`
→ `25`.

### Step 2: Skill-aware preamble + planner wrapper (~15 min)

1. In `run_codex`, replace the hardcoded reviewer preamble with a
   skill-keyed dict; planner preamble (verbatim):

```python
PREAMBLES = {
    "critic": "You are an accessibility design reviewer. Analyze ONLY the component provided below — do not read files, run commands, or use any tools. Output your complete review as text.",
    "perspective": <existing text, unchanged>,
    "planner": "You are an accessibility design planner. Plan ONLY from the requirements provided below — do not read files, run commands, or use any tools. Output your complete plan document as text.",
}
```

   Critic and perspective outputs must be byte-identical to before the
   refactor for the same inputs (the preamble text itself must not change).

2. Add the wrapper, mirroring `run_codex_perspective`:

```python
def run_codex_planner(tier, fixture_id):
    system_prompt = load_planner_system_prompt()
    fixture_content = load_fixture(fixture_id, PLANNER_FIXTURES_DIR)
    user_prompt = PLANNER_PROMPT_PREFIX + fixture_content
    return run_codex(tier, fixture_id, system_prompt, user_prompt, "planner")
```

   (Check `load_fixture`'s signature in THIS file first — if it has no
   directory parameter, extend it with an optional one defaulting to the
   critic dir, keeping existing call sites unchanged.)

**Verify**: compile passes; `git diff` shows critic/perspective preamble
strings unchanged.

### Step 3: Dispatch + scoring (~15 min)

1. Commands (clone the perspective wiring): `codex-planner <tier> <fixture>`,
   `codex-planner-all <tier>` (loops `PLANNER_FIXTURES`, skipping
   `result_exists` hits — resumable), and update the module docstring.
2. Scoring: ensure `score_codex_results("planner")` invokes
   `score_planner.py` with the planner metadata path
   (`evals/suites/a11y-planner/fixtures/{id}.metadata.yaml`). Add the
   planner branch if missing.
3. No escalation command in this plan — single-tier runs only; the planner
   PASS gate is `PLANNER_SECTION_PASS_THRESHOLD` via the scorer. (Escalation
   for planner is a possible follow-up once single-tier numbers exist.)

**Verify**: `python3 ollama/run_cloud_benchmark.py` (no args) prints usage
including the two new commands; compile passes;
`bash scripts/smoke_scorers.sh && python3 scripts/validate_fixtures.py` → exit 0.

### Step 4: Free smoke — no quota beyond one fixture (~10 min)

```bash
export BENCHMARK_RESULTS_DIR=$HOME/a11y-bench-results
python3 ollama/run_cloud_benchmark.py codex-planner 5.2-low keyboard-breadcrumb
python3 ollama/score_planner.py "$BENCHMARK_RESULTS_DIR/codex-bench-planner-keyboard-breadcrumb-5.2-low-response.json" evals/suites/a11y-planner/fixtures/keyboard-breadcrumb.metadata.yaml
```

The operator (Alex) reads the response end-to-end: is it a real plan
(phases, APG references, code stubs), and does the scorer parse it?
(One fixture ≈ one ChatGPT-plan request — treated as free for gating
purposes.)

**Verify**: result JSON exists with non-empty `response` and
`_benchmark.platform == "codex"`, `_benchmark.skill == "planner"`; scorer
prints a `Status:` line. Commit the code at this point.

### Step 5: COST GATE — full 25-fixture run (operator approval required)

Present the operator (Alex): the smoke fixture's score, the tier you intend
(default `5.2-low` to match the critic lane's full-pass tier; flag if you
propose otherwise), and the quota/wall-clock estimate (25 sequential codex
CLI invocations × 1–3 min ≈ 30–75 min). **Do not start without recorded
approval.**

**Sequential execution note**: codex CLI invocations share the local codex
session/auth — run the 25 fixtures STRICTLY sequentially (the `-all` loop
already does); never parallelize with a second codex process, and do not run
this while another codex CLI task is active on the machine.

```bash
python3 ollama/run_cloud_benchmark.py codex-planner-all 5.2-low
mkdir -p evals/results/codex-planner
cp "$BENCHMARK_RESULTS_DIR"/codex-bench-planner-*-response.json evals/results/codex-planner/
```

Add `evals/results/codex-planner/README.md` (3 lines: run date, codex CLI
version + model/tier, command used). Scan one JSON by eye for key material
(none expected — codex CLI auth never enters the result payload).

**Verify**: 25 JSONs in `evals/results/codex-planner/`; zero
`WARN: fallback keywords` lines when scoring;
`grep -rl "api_key\|sk-" evals/results/codex-planner/` → no matches.

### Step 6: Publish (~15 min)

Score all 25; build the per-fixture table; append to `ollama/BENCHMARK.md`
under the planner benchmark section: `### Codex planner lane (<date>,
post-002 scoring)` — per-fixture Score/Status, aggregate section-hit rate,
caveats (single tier; section-presence is a structural proxy), pointer to
`evals/results/codex-planner/`. Update the planner cross-lane summary by
ADDING a codex row only. Update `plans/README.md` row 010. Commit + push.

**Verify**: `git diff ollama/BENCHMARK.md` is append-only (plus the one
summary-row addition); every number traces to the committed JSONs via
`score_planner.py`.

## Time estimate (by phase)

- Steps 1–3 (code): 40 min
- Step 4 (smoke + operator read): 10–15 min
- Step 5 (gated full run): 30–75 min wall-clock, unattended, resumable
- Step 6 (publish): 15 min
- Total: ~1.5–2.5 h, of which ≤1 h is hands-on

## Test plan

- Free-path: compile, usage text, smoke suite, validate_fixtures — all exit 0.
- Step 4's single fixture is the integration test; the operator (Alex) is
  the reviewer there and at the step-5 gate.
- CI never invokes the codex CLI (it isn't installed there); CI coverage is
  compile + registries only.

## Done criteria

ALL must hold:

- [ ] `codex-planner` and `codex-planner-all` commands exist; compile passes
- [ ] Critic/perspective preambles byte-identical to pre-change
- [ ] Smoke fixture run + scored; operator read it
- [ ] Full run completed with recorded operator approval; 25 raw JSONs
      committed under `evals/results/codex-planner/` with README
- [ ] BENCHMARK.md codex planner section appended; numbers trace to artifacts
- [ ] `bash scripts/smoke_scorers.sh` and `python3 scripts/validate_fixtures.py` exit 0
- [ ] `plans/README.md` status row updated

## STOP conditions

Stop and report back (do not improvise) if:

- `run_codex`'s `skill` parameter or `write_json_atomic` are absent (deps not merged).
- `codex --version` fails or `codex exec` errors on auth — the operator must
  fix codex CLI login first.
- The smoke response is structurally unusable by `score_planner.py` after
  one preamble adjustment attempt — report with the sample response.
- More than 3 of the 25 full-run fixtures hit the 300s timeout — stop the
  loop, report; do not silently retry-spin quota.
- Any temptation to add critic/perspective changes "while in the file".

## Maintenance notes

- When CODEX_TIERS gains a new family, planner lane inherits it for free
  (tier is a parameter).
- The mirrored planner constants carry a KEEP IN SYNC comment; the real fix
  is the deferred runner consolidation — do not half-do it here.
- Reviewer should scrutinize: the preamble refactor not perturbing existing
  lanes, and that published numbers re-derive from the committed JSONs.
