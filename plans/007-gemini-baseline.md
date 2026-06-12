# Plan 007: Add the promised Gemini baseline — provider adapter, cost-gated run, committed artifacts

> **AMENDMENT (2026-06-12, operator decision)**: The transport is the `gemini`
> CLI (v0.46.0, already authenticated on this machine), NOT the google-genai
> SDK + GEMINI_API_KEY this plan was written around. The operator directed
> this ("you have gemini as a cli tool... I'm using it so it's already
> working") and it matches the codex lane precedent (`run_codex` shells out to
> `codex exec`). Consequences: step 1 (SDK dep) is dropped from
> requirements.txt; step 2 model enumeration is replaced by CLI `-m` probes;
> the GEMINI_API_KEY startup guard becomes a `gemini`-binary presence guard;
> "paid run" gates become quota/wall-clock gates (CLI auth, no per-token
> billing). Isolation requirements discovered by probe: run from a neutral
> temp cwd with `--skip-trust` (otherwise the CLI loads this repo's own
> `.agents/skills/a11y-*` skill files into context — lane contamination) and
> use `--approval-mode plan` + `-o json`. CLI harness overhead ~18.7K input
> tokens per call, recorded per-fixture via the JSON `stats` block.

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. THIS PLAN HAS TWO HARD COST GATES (steps 5 and 6)
> — never start a paid run without the operator's recorded approval. When
> done, update the status row for this plan in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat de0031f..HEAD -- ollama/run_cloud_benchmark.py ollama/requirements.txt ollama/README.md ollama/BENCHMARK.md`
> Changes from plans 001–003 are EXPECTED and REQUIRED (this plan builds on
> 003's error lanes and atomic writes). If `run_cloud_benchmark.py` does NOT
> show plan 003's changes (`write_json_atomic`, `RESULTS_DIR`, error
> placeholders), STOP — dependency not met.

## Status

- **Priority**: P3
- **Effort**: M (adapter S; runs are wall-clock + approval-bound)
- **Risk**: MED (paid API usage; new provider semantics)
- **Depends on**: plans/002 (scorers), plans/003 (runner robustness — hard), plans/001 (CI)
- **Category**: direction (migration/feature)
- **Planned at**: commit `de0031f`, 2026-06-11

## Why this matters

Four documents promise the same thing in the same hedged words: Gemini rows "when raw result artifacts are present" (`README.md:145`, `ollama/BENCHMARK.md:17`, `EVAL-GAPS-PLAN.md:13`, `ollama/README.md:49`). No Gemini artifact exists. The cross-model story — the repo's positioning — has Claude, OpenAI, and local lanes but is missing the third major hosted family. This plan adds a `gemini` platform to the existing escalation runner, runs the 33-fixture critic suite bottom-up (cheap tier → strong tier), commits the raw artifacts (closing the four-document hedge the honest way), and adds the BENCHMARK.md rows. Spend is explicitly gated: adapter and dry-run are free; nothing paid runs without operator approval.

## Current state

Verified at commit `de0031f` (line numbers pre-003; re-locate by symbol after 003):

- `ollama/run_cloud_benchmark.py` structure to mirror:
  - Tier ladders: `CLAUDE_TIERS` (`:63-92`) and `CODEX_TIERS` (`:94-99`) — list of dicts `{name, model, …, label}`, cheapest first.
  - `get_tier(platform, tier_name)` (`:191-198`) selects from the platform's ladder.
  - `output_path(platform, tier_name, fixture_id, skill)` (`:201-205`) — platform→filename prefix (`cloud` for claude, `codex` for codex); results named `{prefix}-bench[-skill]-{fixture}-{tag}-response.json`.
  - `run_claude(tier, fixture_id, system_prompt, user_prompt, skill)` (`:220-275`) — the adapter shape: build request, time it, collect text, write result JSON with `_benchmark` metadata (platform/model/tier/fixture/skill/elapsed/timestamp) plus `input_tokens`/`output_tokens`.
  - System prompt = critic SKILL.md minus frontmatter (`load_critic_system_prompt`, `:142-144`); user prompt = `CRITIC_PROMPT_PREFIX` + fixture content; `temperature 0.3`, `max_tokens 8192` on non-thinking tiers.
  - Escalation: `run_escalation(platform, skill)` (`:510+`) runs every fixture at the cheapest tier, scores via the score scripts' stdout (`"Status: PASS"`), promotes failures (+errors, post-003 in a separate `errored` lane) to the next tier.
- After plan 003: `write_json_atomic()`, `RESULTS_DIR = os.environ.get("BENCHMARK_RESULTS_DIR", "/tmp")`, error-placeholder JSONs (`"error": ...`), `ANTHROPIC_API_KEY` startup guard pattern to copy.
- `ollama/requirements.txt` (from plan 001): `pyyaml`, `anthropic`.
- No `google-genai` / Gemini code anywhere in the repo (`grep -ri gemini ollama/*.py` → no hits).
- Committed-artifact rule (repo's own): BENCHMARK.md:17 — "Add rows when raw results are committed."

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Compile | `python3 -m py_compile ollama/run_cloud_benchmark.py` | exit 0 |
| SDK present | `python3 -c "from google import genai; print('genai ok')"` | `genai ok` (after step 1) |
| Key guard probe | `env -u GEMINI_API_KEY python3 ollama/run_cloud_benchmark.py gemini <tier> <fixture>` | refusal message, exit 1, no traceback |
| Model listing (free) | step 2 snippet | model ids print |
| Smoke + fixtures | `bash scripts/smoke_scorers.sh && python3 scripts/validate_fixtures.py` | exit 0 |

## Scope

**In scope**:
- `ollama/run_cloud_benchmark.py` (add `GEMINI_TIERS`, `run_gemini()`, dispatch, dry-run command)
- `ollama/requirements.txt` (+ `google-genai`)
- `ollama/README.md` (Gemini setup: `GEMINI_API_KEY`, commands)
- `evals/results/gemini/` (create — committed raw result JSONs, step 6)
- `ollama/BENCHMARK.md` (append-only Gemini section, step 7)
- `README.md` Model Baselines (one bullet, step 7)

**Out of scope** (do NOT touch):
- Perspective/planner Gemini lanes — critic suite only for the first baseline (extend later if the operator wants).
- `run_benchmark.py`, the scorers, fixtures, historical BENCHMARK tables.
- Any retry/quota engineering beyond 003's error placeholders — first pass keeps the runner simple; infra errors land in the `errored` lane and re-run on the next invocation.

## Git workflow

- Branch: `advisor/007-gemini-baseline`
- Conventional commits, e.g. `feat: add gemini platform to cloud benchmark runner`.
- Do NOT push or open a PR unless the operator instructed it.

## Steps

### Step 1: Add the dependency

Append `google-genai>=1.0` to `ollama/requirements.txt`; `pip3 install -r ollama/requirements.txt`.

**Verify**: `python3 -c "from google import genai; print('genai ok')"` → `genai ok`.

### Step 2: Enumerate live models and pick the two-tier ladder (free)

Do NOT hardcode model ids from memory — enumerate, then choose:

```bash
python3 - <<'EOF'
import os
from google import genai
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
for m in client.models.list():
    actions = getattr(m, "supported_actions", None)
    print(m.name, actions or "")
EOF
```

Choose: TIER 1 = the current cheapest general text model of the newest stable family (the "flash" tier); TIER 2 = the strongest stable reasoning model (the "pro" tier). Record both ids and, from https://ai.google.dev/gemini-api/docs/pricing, their per-token prices, in your report. If the family naming is ambiguous (e.g. multiple flash variants), prefer the one Google's docs mark as the default general-purpose model. (As of this plan's knowledge, the families were `gemini-2.5-flash` / `gemini-2.5-pro` — treat that as a hint to validate, not an answer.)

**Verify**: the listing ran (requires `GEMINI_API_KEY` — obtaining the key is the OPERATOR's step; if absent, STOP and request it); two model ids + prices recorded in the work log.

### Step 3: Add the adapter to `run_cloud_benchmark.py`

1. Ladder, mirroring `CODEX_TIERS`' shape:
```python
GEMINI_TIERS = [
    {"name": "flash", "model": "<tier-1 id from step 2>", "max_tokens": 8192, "label": "<human label>"},
    {"name": "pro",   "model": "<tier-2 id from step 2>", "max_tokens": 8192, "label": "<human label>"},
]
```
2. `get_tier`: add `gemini` → `GEMINI_TIERS` (the current claude/codex two-way selection becomes three-way).
3. `output_path`: platform prefix `"gemini"` → files `gemini-bench-{fixture}-{tag}-response.json` under `RESULTS_DIR`.
4. `run_gemini(tier, fixture_id, system_prompt, user_prompt, skill="critic")`, mirroring `run_claude` exactly (timing, prints, `_benchmark` block, `write_json_atomic`, the 003-style try/except writing an `"error"` placeholder on failure):
```python
    from google import genai
    from google.genai import types
    client = genai.Client()   # reads GEMINI_API_KEY
    response = client.models.generate_content(
        model=tier["model"],
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.3,
            max_output_tokens=tier["max_tokens"],
        ),
    )
    response_text = response.text or ""
```
   Record `response.usage_metadata.prompt_token_count` / `candidates_token_count` as `input_tokens`/`output_tokens` when present (guard with `getattr`).
5. Dispatch: `gemini <tier> <fixture>`, `gemini-all <tier>`, `gemini-escalate` — clone the claude command wiring, including the startup guard:
```python
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("GEMINI_API_KEY is not set — refusing to start a paid run.")
```
6. Add a FREE `gemini-dry-run` command: for each of the 33 critic fixtures, build both prompts, print fixture id + system/user prompt char counts and a rough token estimate (chars/4), then a total estimate per tier using step 2 prices. No API calls.
7. Update the module docstring usage block.

**Verify**: `python3 -m py_compile ollama/run_cloud_benchmark.py` → exit 0. `env -u GEMINI_API_KEY python3 ollama/run_cloud_benchmark.py gemini flash button-skip-link-clean; echo exit=$?` → refusal, `exit=1`. `python3 ollama/run_cloud_benchmark.py gemini-dry-run` → 33 lines + cost estimate, exit 0, no network.

### Step 4: Document setup

In `ollama/README.md`, next to the existing Claude/Codex setup (around the `### Claude API (requires ANTHROPIC_API_KEY)` heading at `:137`), add a `### Gemini API (requires GEMINI_API_KEY)` block: where to create the key (Google AI Studio), export line, the three commands, and the dry-run command with a note that escalation runs are cost-gated.

**Verify**: `grep -n "GEMINI_API_KEY" ollama/README.md` → ≥2 hits.

### Step 5: COST GATE 1 — 3-fixture probe (operator approval required)

Present the operator: dry-run cost estimate + step 2 prices + the proposed probe (3 fixtures: `button-skip-link-clean`, `toast-notification-no-role`, `tabbed-nav-vs-tab-pattern` — one CLEAN, one HAS-BUGS, one ADVERSARIAL) at the flash tier. **Do not proceed without recorded approval.** Then:

```bash
export BENCHMARK_RESULTS_DIR=$HOME/a11y-bench-results
python3 ollama/run_cloud_benchmark.py gemini flash button-skip-link-clean   # ×3
python3 ollama/score_output.py "$BENCHMARK_RESULTS_DIR/gemini-bench-toast-notification-no-role-flash-response.json" evals/suites/a11y-critic/fixtures/toast-notification-no-role.metadata.yaml
```

Read all three responses end-to-end yourself: sane critic output (phases, findings, verdict)? Scorer parses them? Token counts recorded?

**Verify**: 3 result JSONs with non-empty `response` and `_benchmark.platform == "gemini"`; scorer produces a `Status:` line on each; actual cost within 2× of the dry-run estimate for those fixtures (else recalibrate the estimate before gate 2).

### Step 6: COST GATE 2 — full escalation run + commit artifacts (operator approval required)

Present the operator the full-run estimate (33 fixtures × flash, plus expected escalations × pro). On approval:

```bash
python3 ollama/run_cloud_benchmark.py gemini-escalate
```

(Resumable: `result_exists` skips completed fixtures; infra errors land in the `errored` lane and re-run on re-invocation.) Then copy the raw artifacts into the repo and commit them:

```bash
mkdir -p evals/results/gemini
cp "$BENCHMARK_RESULTS_DIR"/gemini-bench-*-response.json evals/results/gemini/
```

Add `evals/results/gemini/README.md` (3 lines: run date, model ids, command used). Before committing, scan the JSONs: they must contain NO key material (they don't by construction — response/usage/metadata only — but check one file by eye).

**Verify**: 33+ JSONs in `evals/results/gemini/` (33 flash + any pro escalations); escalation summary printed PASS/FAIL/INFRA-ERROR per tier; `grep -rl "api_key\|AIza" evals/results/gemini/` → no matches.

### Step 7: Publish

Append to `ollama/BENCHMARK.md`: `## Gemini baseline (<date>, post-002 scoring)` — escalation table in the house style (tier, ran, pass, fail, infra-error), must-find aggregate, CLEAN false-positive count, ADVERSARIAL verdicts, pointer to `evals/results/gemini/`. Update the cross-platform summary table ONLY by adding a Gemini column/row (no edits to existing cells). In root `README.md` Model Baselines, add a Gemini bullet and delete the "should be tracked … when raw result artifacts are present" hedge sentence (the promise is now fulfilled). Every number must trace to the committed artifacts.

**Verify**: `git diff ollama/BENCHMARK.md` shows additions only; `grep -n "when raw result artifacts are present" README.md` → 0 hits; each table number reproducible by re-running `score_output.py` over `evals/results/gemini/`.

## Test plan

- Free-path tests: key-guard probe, dry-run determinism (`gemini-dry-run` twice → identical output), compile check, smoke suite untouched.
- The 3-fixture probe (step 5) is the integration test; the operator is the reviewer at both gates.
- CI (plan 001) covers compile + registries; no CI step may call the Gemini API.

## Done criteria

ALL must hold:

- [ ] `gemini`, `gemini-all`, `gemini-escalate`, `gemini-dry-run` commands exist; compile passes
- [ ] No-key invocation refuses with exit 1 before any network call
- [ ] Model ids chosen by live enumeration, recorded with prices (step 2 log)
- [ ] Probe ran with operator approval; responses humanly sane; scorer parses them
- [ ] Full run completed with operator approval; raw artifacts committed under `evals/results/gemini/` with README
- [ ] BENCHMARK.md Gemini section appended; README hedge sentence removed; numbers trace to artifacts
- [ ] `bash scripts/smoke_scorers.sh` and `python3 scripts/validate_fixtures.py` still exit 0
- [ ] `plans/README.md` status row updated

## STOP conditions

Stop and report back (do not improvise) if:

- Plan 003's changes are absent from `run_cloud_benchmark.py` (no `write_json_atomic`/`RESULTS_DIR`).
- No `GEMINI_API_KEY` is available — request it from the operator; never mint, guess, or copy keys, and never write a key value anywhere.
- Step 2 model enumeration shows no clear flash/pro pairing — present the options table to the operator instead of choosing.
- Probe responses are structurally unusable by `score_output.py` (e.g. Gemini refuses the system-prompt length) after one adjustment attempt — report with a sample response.
- Estimated full-run cost at gate 2 exceeds the gate-1-calibrated estimate by >2× — re-present to the operator.
- Any temptation to run perspective/planner Gemini lanes "while we're at it."

## Maintenance notes

- Committed artifacts under `evals/results/gemini/` are the precedent the four-document hedge asked for — future hosted runs (and ideally re-runs of Claude/Codex lanes) should follow it; consider a follow-up that re-runs existing lanes with artifact retention so all published tables become reproducible.
- When Gemini ships a new family, re-run step 2 and add a tier — do not edit old tier entries (old artifacts reference them).
- Reviewer should scrutinize: that no key material or account identifiers landed in committed JSONs, and that README/BENCHMARK numbers match the artifacts.
