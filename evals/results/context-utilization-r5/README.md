# Phase 4.3 R5 receipts — `num_ctx` map hygiene (2026-08-27)

Receipts for tasks **R5.1–R5.5** of
`docs/plans/2026-08-27-context-utilization-r5-decision-memo.md`, whose §1 conclusion was: at pack
scale, for local models, **fit is everything and curation buys no accuracy** — so R5 resolves to map
hygiene, i.e. correcting `num_ctx` entries.

| task | what landed | where |
|---|---|---|
| **R5.1** | `num_ctx` recorded on all six scored `_benchmark` dicts, beside `declared_context_length` | `ollama/run_benchmark.py` |
| **R5.2** | `num_predict=1` probes, 3 models × 5 suites × 2 points (30 probes) | `num-ctx-probe-receipts.md`, `num-ctx-probes-2026-08-27.json`, `probe_num_ctx.py` |
| **R5.3** | output-side `eval_count` analysis of all 57 committed local planner rows | `planner-historical-exposure-analysis.md` |
| **R5.4** | 4 `_DEFAULT`s raised + `ollama_a11y.py` per-command `SKILL_NUM_CTX` dict + tag/`show` guard fixes + tests (50 pass) | `ollama/run_benchmark.py`, `ollama/ollama_a11y.py`, `ollama/test_context_guard.py` |
| **R5.5** | dated §5.2 comparability annotation per raised default | `ollama/BENCHMARK.md` |

Supporting: `estimate_pass.py` reproduces the memo §3 guard estimates for every fixture in every
suite (no server needed).

## The raises

| default | old → new |
|---|---|
| `CRITIC_CTX_DEFAULT` | 16,384 → 32,768 |
| `PLANNER_CTX_DEFAULT` | 32,768 → 40,960 |
| `BUGREPORT_CTX_DEFAULT` | 16,384 → 32,768 |
| `PERSPECTIVE_CTX_DEFAULT` | 16,384 → 32,768 |
| `ollama_a11y.py` wrapper | flat 32,768 → `SKILL_NUM_CTX` (planner 40,960, others 32,768) |

`EVALREPORT_CTX_DEFAULT` (32,768) and `ACR_CTX_DEFAULT` (40,960) measured fine and are unchanged, as
are `CRITIC_CTX`'s 10 mapped entries and `PERSPECTIVE_CTX`'s 7.

## What these receipts add beyond the memo

1. **The planner raise's real justification is output-side, not prompt-side.** The memo argued from
   guard refusals (19/28). Measured against real `prompt_eval_count`, only **2 of 57** committed rows
   would truly have overflowed — most refusals are estimator artifacts. The load-bearing evidence is
   R5.3's **3 confirmed output clips**.
2. **`planner-federal` was absent from the memo's §3 table** and refuses **28/28** at the old 32,768.
   At 40,960 it clears by **759 estimated tokens**, and `qwen3:32b`'s declared ceiling *is* 40,960 —
   the closest thing on record to "fit that can't be bought with an integer," though not yet an
   instance of it (R5.2 finding 2).
3. **The estimator under-counts on perspective prompts** (0.978–0.993), contradicting
   `estimate_tokens()`'s "always the safe direction" claim. The 8,192 reserve is what makes it safe
   (R5.2 finding 1).
4. **Protocol growth silently eats output headroom** — `a11y-planner/SKILL.md` +11,132 chars in six
   weeks, so R5.3's 3/57 is a floor for today, not a rate (R5.3 §4.4).
5. **66 committed critic rows on two more unmapped models** ran at 16,384 before the guard existed —
   the same class as the documented qwen3:32b 99-row case, previously unrecorded (R5.5 annotation).
6. **Three defects that stopped models running any lane** — unrelated to `num_ctx` values, found
   while probing and **fixed in the same change**: `/api/show` fallback for models whose `/api/tags`
   entry carries a null `context_length` (unblocked `gemma4:31b`/`:26b`, both `CRITIC_CTX`-mapped),
   implicit-`:latest` resolution in the guard, and `ctx_for()` so the same spelling gap can no longer
   drop a mapped model to the `_DEFAULT` silently (R5.2 finding 3).

## Still open

- **The memo §6 routing block is NOT folded.** That section (P1/P1b/P3 findings + the sizing rule) is
  gated on Phase 4.1 completing, per RESULTS:157–158 and memo §6. Only the §5.2 comparability
  annotation — bookkeeping for a code change made today — landed in `BENCHMARK.md`. Deferring it too
  would have left raised defaults with no record of when or why they changed, which is the exact
  hazard §5 exists to prevent. The §6 verbatim block still awaits Phase 4.2.
- **Issue #28** (`flag_context_pressure` compares against requested `num_ctx`, not the clamped
  ceiling) is unchanged. Raising toward 40,960 keeps `min()` a no-op for both current local models,
  so this neither aggravates nor fixes it.
- **`qwen3.5:latest` (9.7B, 33 committed critic rows) is unmapped in both `CRITIC_CTX` and
  `PERSPECTIVE_CTX`.** Left that way on purpose: the R5.4 defaults give it the right window (32,768)
  and adding an entry without probing that model would be inventing a value. Probe it before mapping
  it.
