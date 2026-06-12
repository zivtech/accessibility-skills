# Plan 003: Make the benchmark runners resumable, error-honest, and reproducible

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat de0031f..HEAD -- ollama/run_benchmark.py ollama/run_cloud_benchmark.py ollama/codex-benchmark.sh`
> If either runner changed since this plan was written, compare the
> "Current state" excerpts against the live code before proceeding; on a
> mismatch, treat it as a STOP condition.

## Status

- **Priority**: P2
- **Effort**: M
- **Risk**: MED (changes output paths/derivations; old `/tmp` artifacts become invisible to resume logic — acceptable, they're ephemeral by design today)
- **Depends on**: plans/001-ci-verification-baseline.md (compile check + registry check in CI)
- **Category**: bug
- **Planned at**: commit `de0031f`, 2026-06-11

## Why this matters

Benchmark runs cost real time (local models: minutes/fixture) and real money (Claude/Codex APIs). Today: (1) a Ctrl-C mid-write leaves a half-written JSON that either crashes the next resume (`result_exists` does an unguarded `json.load`) or silently passes as complete; (2) an API outage or missing key crashes mid-run after burning spend, and fixtures that never ran are escalated to more expensive tiers as if the model had failed them, distorting the "cheapest tier with 100% pass" story; (3) results land in `/tmp`, so published numbers cannot be recomputed after a reboot — the raw artifacts behind BENCHMARK.md are already gone; (4) the perspective/planner paths derive a model tag that drops the size suffix (`qwen3:32b` → `qwen3`), so two same-family models would silently share resume state and skip each other's fixtures.

## Current state

Verified excerpts at commit `de0031f`:

**Non-atomic writes** — `ollama/run_benchmark.py:244-245` (same pattern at `:295-296` planner, and in the perspective path ~`:340-360`); `ollama/run_cloud_benchmark.py:270-271` (Claude), and the codex path writes similarly:
```python
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)
```

**Fragile resume check** — `ollama/run_cloud_benchmark.py:208-214`:
```python
def result_exists(platform, tier_name, fixture_id, skill="critic"):
    path = output_path(platform, tier_name, fixture_id, skill)
    if not os.path.exists(path):
        return False
    with open(path) as f:
        data = json.load(f)          # unguarded — corrupt file crashes the run
    return len(data.get("response", "")) > 100
```

**No API error capture / no key guard** — `ollama/run_cloud_benchmark.py:220-242`: `import anthropic; client = anthropic.Anthropic()` then `client.messages.create(**kwargs)` with no try/except and no startup check that `ANTHROPIC_API_KEY` is set (the docstring at `:8` mentions the env var; nothing enforces it).

**Failure conflation** — `ollama/run_cloud_benchmark.py:500-506` marks a fixture failed when `"Status: PASS" not in proc.stdout` (a scorer crash → empty stdout → "failed"), and `:554-555`:
```python
        # Escalate both failures AND not-run (model didn't exist, API error, etc.)
        remaining = failed + [f for f in not_run if f in remaining]
```
The comment shows escalating not-run is deliberate — but the tier summary (`:542-549`) then reports those as model performance, and an API outage cascades every fixture through every paid tier.

**Inconsistent model tags** — `ollama/run_benchmark.py:205` (critic): `model.replace(":", "-").replace(".", "")` → `qwen3-32b`; vs `:269` (planner) and `:324` (perspective): `model.split(":")[0].replace(".", "").replace("-", "")` → `qwen3` (size suffix lost; `qwen3:32b` and `qwen3:8b` collide). The resume globs at `:434` and `:456-457` use these tags.

**Ephemeral results** — all output paths are f-strings rooted at `/tmp/` (`run_benchmark.py:206,270,325`; `run_cloud_benchmark.py:201-205`), and the scoring globs read `/tmp` (`run_benchmark.py:480-481,512`).

**Unvalidated fixture ids** — both runners take `fixture_id` from `sys.argv` and interpolate it into paths (e.g. `run_cloud_benchmark.py:205` and `load_fixture` at `:157-160`). A typo like `../foo` produces writes outside the results dir. Researcher-only tool, so severity is low — but a 1-line guard prevents accidents.

**Repo conventions**: flat stdlib scripts, no classes; constants UPPER_CASE at module top; conventional commits.

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Compile | `python3 -m py_compile ollama/run_benchmark.py ollama/run_cloud_benchmark.py` | exit 0 |
| Registry check | `python3 scripts/validate_fixtures.py` | exit 0 |
| Smoke (unchanged by this plan) | `bash scripts/smoke_scorers.sh` | exit 0 |
| Help paths | `python3 ollama/run_benchmark.py 2>&1 \| head -30` | usage text prints, no traceback |

No Ollama server and no API key are required to verify this plan — every verification is static or uses the guards' error paths.

## Scope

**In scope**:
- `ollama/run_benchmark.py` (modify)
- `ollama/run_cloud_benchmark.py` (modify)
- `ollama/README.md` (add: `BENCHMARK_RESULTS_DIR` documentation — one short subsection)

**Out of scope** (do NOT touch):
- `ollama/score_*.py`, `ollama/score_common.py` — plan 002. The stdout contract (`Status: PASS`) is consumed here; do not alter the scorers from this side.
- `ollama/codex-benchmark.sh` — thin wrapper, already quotes correctly; the validation lands in the Python it calls.
- `ollama/BENCHMARK.md` historical tables.
- `evals/**`, `.claude/**`, `.agents/**`.

## Git workflow

- Branch: `advisor/003-runner-robustness`
- Conventional commits per step, e.g. `fix: atomic result writes in benchmark runners`.
- Do NOT push or open a PR unless the operator instructed it.

## Steps

### Step 1: Results directory env var

In BOTH runners, near the other module constants, add:

```python
RESULTS_DIR = os.environ.get("BENCHMARK_RESULTS_DIR", "/tmp")
```

Replace every hardcoded `/tmp/` in output-path f-strings and result globs with `{RESULTS_DIR}/` (use `os.path.join(RESULTS_DIR, ...)` where natural). Affected lines — `run_benchmark.py`: 206, 270, 325, 434, 456–457, 480–481, 512 (re-locate by grepping `"/tmp` after the prior edits shift lines); `run_cloud_benchmark.py`: `output_path()` at 201–205 plus any `glob.glob("/tmp/...")` in the score-cloud/summary commands (grep the file). Default stays `/tmp`, so behavior is unchanged unless the var is set.

In `ollama/README.md`, add under the benchmark-running section:

```markdown
### Persistent results

By default raw responses land in `/tmp` (cleared on reboot). To keep artifacts
for reproducible scoring, set `BENCHMARK_RESULTS_DIR`, e.g.:

    export BENCHMARK_RESULTS_DIR="$HOME/a11y-bench-results"
    mkdir -p "$BENCHMARK_RESULTS_DIR"

Published tables in BENCHMARK.md should only cite runs whose artifacts were
kept this way.
```

**Verify**: `grep -n '"/tmp\|f"/tmp' ollama/run_benchmark.py ollama/run_cloud_benchmark.py` → no matches. `BENCHMARK_RESULTS_DIR=/tmp/bench-test python3 -c "import sys,os; sys.path.insert(0,'ollama'); import run_cloud_benchmark as r; p=r.output_path('claude','haiku','x-y'); print(p); assert p.startswith('/tmp/bench-test/')"` → prints the path, no assertion error.

### Step 2: Atomic writes everywhere a result JSON is written

Add to BOTH runners (duplicate the helper in each file — matches the repo's current no-shared-module style for runners; plan 002 only shared scorer helpers):

```python
def write_json_atomic(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)
```

Replace every `with open(out_path, "w") as f: json.dump(data, f, indent=2)` pair with `write_json_atomic(out_path, data)`. Sites: `run_benchmark.py` critic (244–245), planner (295–296), perspective (locate the third occurrence by grepping `json.dump`); `run_cloud_benchmark.py` Claude (270–271) and the codex write (grep `json.dump`).

**Verify**: `grep -n "json.dump" ollama/run_benchmark.py ollama/run_cloud_benchmark.py` → only inside `write_json_atomic` definitions.

### Step 3: Corruption-tolerant `result_exists`

Rewrite `run_cloud_benchmark.py:208-214`:

```python
def result_exists(platform, tier_name, fixture_id, skill="critic"):
    path = output_path(platform, tier_name, fixture_id, skill)
    if not os.path.exists(path):
        return False
    try:
        with open(path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        print(f"WARN: corrupt result file, will re-run: {path}")
        return False
    if data.get("error"):
        return False  # error placeholder from step 4 — re-run, don't skip
    return len(data.get("response", "")) > 100
```

`run_benchmark.py`'s resume paths (`critic-remaining` at ~451–457, `perspective-remaining` at ~429–437) only check file existence via glob — wrap any `json.load` they perform the same way if present (grep first; if they never parse, no change there).

**Verify**: `printf '{"response": "trunca' > /tmp/corrupt-probe.json && python3 -c "import sys; sys.path.insert(0,'ollama'); import run_cloud_benchmark as r, shutil; shutil.copy('/tmp/corrupt-probe.json', r.output_path('claude','haiku','probe-fixture')); print(r.result_exists('claude','haiku','probe-fixture'))"` → prints `WARN: corrupt result file…` then `False`. Clean up both probe files afterwards.

### Step 4: Capture API/infra errors as data, separate them in escalation

1. In `run_cloud_benchmark.py`, at the top of the `claude`, `claude-all`, and `claude-escalate` command paths (find the `sys.argv` dispatch in `main`/bottom of file), add:
```python
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set — refusing to start a paid run.")
```
2. Wrap the API call in `run_claude` (and the subprocess invocation in the codex run function) so an exception writes an error placeholder instead of crashing the whole run:
```python
    try:
        response = client.messages.create(**kwargs)
    except Exception as e:                      # APIError, network, auth
        write_json_atomic(out, {
            "response": "", "done": False,
            "error": f"{type(e).__name__}: {e}",
            "_benchmark": {"platform": "claude", "tier": tier["name"],
                            "fixture_id": fixture_id, "skill": skill,
                            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")},
        })
        print(f"ERROR (infra, not model): {type(e).__name__}: {e}")
        return out
```
3. In `get_failed_fixtures` (`:469-507`), add a third returned list `errored`: before scoring, load the result JSON; if it has a non-empty `"error"`, append to `errored` and `continue` (do not run the scorer on it). Return `(failed, not_run, errored)` and update both call sites.
4. In `run_escalation` (`:510-570`): keep escalating `failed` and `not_run` (current deliberate behavior), and ALSO escalate `errored` — but report them separately so cost analysis is honest. Tier summary lines become:
```
Tier {label}: {passed} PASS / {len(failed)} FAIL / {len(errored)} INFRA-ERROR / {len(not_run)} NOT_RUN
```
and the final `ESCALATION SUMMARY` prints an `infra_errors` count per tier. The `pct` math at `:564` must keep dividing by `passed + failed` only (model performance excludes infra errors).

**Verify**: `python3 -m py_compile ollama/run_cloud_benchmark.py` → exit 0. Then the no-key guard: `env -u ANTHROPIC_API_KEY python3 ollama/run_cloud_benchmark.py claude haiku button-skip-link-clean; echo "exit=$?"` → prints the refusal message, `exit=1`, and NO traceback, NO result file written.

### Step 5: One model-tag derivation

In `run_benchmark.py`, add near the constants:

```python
def make_model_tag(model):
    """qwen3:32b -> qwen3-32b ; deepseek-r1:70b -> deepseek-r1-70b (dots dropped)."""
    return model.replace(":", "-").replace(".", "")
```

Replace the inline derivations at `:205` (critic — already this formula), `:269` (planner), and `:324` (perspective) with `make_model_tag(model)`, and update the resume-glob tag derivations (`perspective-remaining` ~`:432`, `critic-remaining` ~`:453`) to use it too. Consequence to state in the commit message: previously-written planner/perspective files under the OLD short tag (`...-qwen3-response.json`) will no longer be seen by resume logic; with default `/tmp` storage these are ephemeral anyway.

**Verify**: `python3 -c "import sys; sys.path.insert(0,'ollama'); from run_benchmark import make_model_tag as t; assert t('qwen3:32b')=='qwen3-32b'; assert t('qwen3.5:27b')=='qwen35-27b'; assert t('deepseek-r1:70b')=='deepseek-r1-70b'; print('tags ok')"` → `tags ok`. Then `grep -n 'split(":")\[0\]' ollama/run_benchmark.py` → no matches.

### Step 6: Validate fixture ids at the CLI boundary

In BOTH runners, where `fixture_id` comes from `sys.argv` (grep `sys.argv` in each dispatch), guard before first use:

```python
import re as _re
if not _re.fullmatch(r"[a-z0-9][a-z0-9-]*", fixture_id):
    sys.exit(f"Invalid fixture id: {fixture_id!r} (expected kebab-case)")
```

**Verify**: `python3 ollama/run_benchmark.py single qwen3:32b "../evil"; echo "exit=$?"` → prints `Invalid fixture id…`, `exit=1`, no traceback, no file created. (If the `single` subcommand requires the Ollama server before reaching the guard, place the guard before any network/file access — re-order so validation is first.)

## Test plan

- This plan's verifications are its tests (static probes + error-path probes); none require Ollama or API keys.
- `bash scripts/smoke_scorers.sh` must still pass untouched (scorers not modified here).
- `python3 scripts/validate_fixtures.py` must still pass (registries untouched).
- Optional live test if the operator has Ollama running (do NOT block on it): `BENCHMARK_RESULTS_DIR=/tmp/bench-test python3 ollama/run_benchmark.py single qwen3:32b button-skip-link-clean` → file appears under `/tmp/bench-test/`, and no stray `.tmp` file is left behind.

## Done criteria

ALL must hold:

- [ ] `python3 -m py_compile ollama/run_benchmark.py ollama/run_cloud_benchmark.py` exits 0
- [ ] `grep -rn '"/tmp\|f"/tmp' ollama/run_benchmark.py ollama/run_cloud_benchmark.py` → 0 matches
- [ ] `grep -n "json.dump" ollama/*.py` → matches only inside `write_json_atomic` (scorers don't write JSON)
- [ ] No-key run refuses with exit 1 and no traceback
- [ ] Corrupt result file → `result_exists` returns False with a WARN, no crash
- [ ] `make_model_tag('qwen3:32b') == 'qwen3-32b'` and no `split(":")[0]` tag derivation remains
- [ ] Invalid fixture id exits 1 before any file/network access
- [ ] `bash scripts/smoke_scorers.sh` and `python3 scripts/validate_fixtures.py` still exit 0
- [ ] `git status` shows changes only in: `ollama/run_benchmark.py`, `ollama/run_cloud_benchmark.py`, `ollama/README.md`
- [ ] `plans/README.md` status row updated

## STOP conditions

Stop and report back (do not improvise) if:

- The live code at the cited lines doesn't match the excerpts (drift since `de0031f`).
- You cannot find one of the listed write/glob sites by grep — the file may have been refactored; report what you found instead.
- Changing the escalation return shape (`get_failed_fixtures` 3-tuple) breaks a caller you didn't anticipate — list the call sites and stop if there are more than the two in `run_escalation`/summary.
- Any verification requires actually spending API credit — nothing in this plan should; if it seems to, you've taken a wrong turn.

## Maintenance notes

- When a future plan consolidates `load_fixture`/`build_escalation_prompt` duplication between the two runners (deferred — see plans/README.md), `write_json_atomic` and `make_model_tag` should move into that shared module.
- The `errored` lane gives BENCHMARK.md authors an honest cost story; the next benchmark write-up should report infra errors per tier explicitly.
- Reviewer should scrutinize: that `os.replace` is used (atomic on POSIX), not `os.rename`-after-unlink patterns; and that the error placeholder JSON always has `"response": ""` so `result_exists` re-runs it.
- Note for operators: keep treating local Ollama as the default execution lane; cloud escalation runs remain an explicit cost decision (the new startup guard helps enforce that).
