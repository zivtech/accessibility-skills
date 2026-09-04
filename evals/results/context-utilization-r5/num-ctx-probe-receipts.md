# R5.2 — `num_predict=1` probe receipts for the raised `num_ctx` defaults

**Date:** 2026-08-27 · **Server:** ollama, default `:11434` · **Probe `num_ctx`:** 40,960 for every
probe (generous for all five suites, and exactly `qwen3:32b`'s declared ceiling, so no probe was
silently clamped) · **Options:** `{"num_predict": 1, "temperature": 0}`
**Task:** R5 decision memo `docs/plans/2026-08-27-context-utilization-r5-decision-memo.md` §4 row
**R5.2**. **Harness:** `probe_num_ctx.py` (this directory). **Raw:** `num-ctx-probes-2026-08-27.json`.

Prompt assembly is **imported from `ollama/run_benchmark.py`** — `load_system_prompt`,
`load_planner_system_prompt`, `load_planner_federal_system_prompt`, `build_escalation_prompt`,
`load_fixture` (→ `strip_answer_key`), and the `*_PROMPT_PREFIX` constants — never re-implemented.
Each probe sends the exact production `system` + `prompt` pair and reads the server's own
`prompt_eval_count`. Probes deliberately bypass the client-side guard: the point is to measure what
the guard estimates.

## Model set, and why these three

The four raised entries are all `_DEFAULT`s, which exist for models that do not exist yet. Memo §8's
rule: *"size from the current models' probes with the densest measured tokenizer governing."*
Probed: `qwen3.6:35b` (current recommendation), `qwen3:32b` (fallback baseline, and the only local
model with a declared ceiling that bites — 40,960), and `gemma4:31b` (densest-tokenizer candidate).

**`gemma4:31b` is confirmed the densest on all five suites** and therefore governs every default
below. Its margin over `qwen3.6:35b` is 191–588 tokens depending on suite — small, but it is the
model that would have overflowed first, so it is the one the defaults are sized against.

Per memo §8, stated plainly: **for an unknown model the client-side guard, not the default, is the
real protection.** A default is a starting guess.

## Governing measurement — largest fixture per suite

| suite | new `num_ctx` | budget | fixture | model | guard est | **measured** | est/measured | est margin vs budget | true headroom |
|---|---|---|---|---|---|---|---|---|---|
| critic | 32,768 | 24,576 | `multistep-form-error-clearing` | qwen3.6:35b | 19,906 | **17,237** | 1.155 | +4,670 | 15,531 |
| critic | 32,768 | 24,576 | `multistep-form-error-clearing` | qwen3:32b | 19,906 | **16,530** | 1.204 | +4,670 | 16,238 |
| critic | 32,768 | 24,576 | `multistep-form-error-clearing` | gemma4:31b | 19,906 | **17,655** | 1.127 | +4,670 | 15,113 |
| planner | 40,960 | 32,768 | `sr-notification-system` | qwen3.6:35b | 25,709 | **21,182** | 1.214 | +7,059 | 19,778 |
| planner | 40,960 | 32,768 | `sr-notification-system` | qwen3:32b | 25,709 | **20,649** | 1.245 | +7,059 | 20,311 |
| planner | 40,960 | 32,768 | `sr-notification-system` | gemma4:31b | 25,709 | **21,461** | 1.198 | +7,059 | 19,499 |
| planner-federal | 40,960 | 32,768 | `sr-notification-system` | qwen3.6:35b | 32,009 | **26,924** | 1.189 | +759 | 14,036 |
| planner-federal | 40,960 | 32,768 | `sr-notification-system` | qwen3:32b | 32,009 | **26,135** | 1.225 | +759 | 14,825 |
| planner-federal | 40,960 | 32,768 | `sr-notification-system` | gemma4:31b | 32,009 | **27,512** | 1.163 | +759 | 13,448 |
| bugreport | 32,768 | 24,576 | `axe-button-name-federal` | qwen3.6:35b | 9,567 | **9,165** | 1.044 | +15,009 | 23,603 |
| bugreport | 32,768 | 24,576 | `axe-button-name-federal` | qwen3:32b | 9,567 | **8,751** | 1.093 | +15,009 | 24,017 |
| bugreport | 32,768 | 24,576 | `axe-button-name-federal` | gemma4:31b | 9,567 | **9,497** | 1.007 | +15,009 | 23,271 |
| perspective | 32,768 | 24,576 | `article-page-clean` | qwen3.6:35b | 10,106 | **10,175** | 0.993 | +14,470 | 22,593 |
| perspective | 32,768 | 24,576 | `article-page-clean` | qwen3:32b | 10,106 | **9,652** | 1.047 | +14,470 | 23,116 |
| perspective | 32,768 | 24,576 | `article-page-clean` | gemma4:31b | 10,106 | **10,337** | 0.978 | +14,470 | 22,431 |

*budget = `num_ctx` − 8,192 reserve. "est margin vs budget" is what the guard sees (identical across
models — the estimate is char-based). "true headroom" is `num_ctx` − measured, what the model gets.*

## Protocol-alone anchors (system prompt + prefix, no fixture)

### protocol-alone anchors

| suite | qwen3.6:35b | qwen3:32b | gemma4:31b |
|---|---|---|---|
| critic | 14,360 | 13,936 | 14,551 |
| planner | 19,468 | 18,950 | 19,717 |
| planner-federal | 25,210 | 24,436 | 25,768 |
| bugreport | 8,134 | 7,749 | 8,383 |
| perspective | — | — | — |

*Perspective has no separable protocol anchor: `build_escalation_prompt` produces the whole user
prompt, so a system-only probe sends an empty `prompt` and Ollama answers `done_reason=load` with
null counts. Recorded as null in the raw JSON, not as a failure.*

**Supersedes** the `CRITIC_CTX` comment's "gemma4 tokenizer: critic prompt alone measures 16,477
tokens (2026-07-28)" — today's measurement is **14,551**. The difference is `a11y-critic/SKILL.md`
drift between the dates, not tokenizer variance; all three models moved together.

## Finding 1 — the 3.5 chars/token estimator is not uniformly conservative

`estimate_tokens()`'s docstring states 3.5 "stays unchanged, still deliberately below both measured
ratios — the safe direction." **Measured across five suites, that holds for three of them and fails
for one:**

| suite | est/measured (35b, 32b, gemma4) | reading |
|---|---|---|
| critic | 1.155 / 1.204 / 1.127 | conservative, as documented |
| planner | 1.214 / 1.245 / 1.198 | conservative |
| planner-federal | 1.189 / 1.225 / 1.163 | conservative |
| bug-report | 1.044 / 1.093 / **1.007** | barely — gemma4 is 70 tokens from parity |
| perspective | **0.993** / 1.047 / **0.978** | **under-counts on 2 of 3 models** |

The claim was calibrated on critic-protocol text (60K chars of dense prose) and does not generalize
to prompt mixtures with more YAML, tables, and code. Under-counting is the *unsafe* direction: the
guard believes the prompt is smaller than it is.

**No action taken, and the reason matters.** At the raised defaults perspective has ~22.4K tokens of
true headroom, so a 2% under-count is absorbed many times over by the 8,192 reserve. **The reserve is
what makes this safe, not the ratio** — which inverts the docstring's stated safety argument. Changing
the constant would re-baseline every estimate in every committed row's `estimated_prompt_tokens`
field; documenting the boundary is the cheaper correct move. The docstring is annotated in place
(`PERSPECTIVE_CTX_DEFAULT`'s R5.4 comment).

## Finding 2 — `planner-federal` is where the next integer runs out

`planner-federal` (crosswalk YAML appended to the planner system prompt) clears the new 40,960 by
**759 estimated tokens** — max est 32,009 + 8,192 reserve = 40,201. That is ≈ **2,657 chars** of
protocol growth, against a `a11y-planner/SKILL.md` that grew **11,132 chars in the six weeks** to
2026-08-25.

The true tokens are comfortable — 26,135–27,512 measured, ~13.4–14.8K of real headroom. **The squeeze
is entirely on the estimator, and the estimator is what the guard obeys.**

And there is no next raise for one model: **`qwen3:32b`'s declared ceiling *is* 40,960**
(`/api/tags`, confirmed 2026-08-27). Above it the server clamps silently. So when federal growth
crosses the guard line, the remedies for `qwen3:32b` are curate-the-input or drop the model — not a
bigger integer.

**This is not yet the memo §8 reopen condition** ("a declared window smaller than protocol +
fixture"). The window is not too small; the *estimate* is close to the line while the true prompt has
room. Naming it precisely: this is the reopen condition approached from the estimator side, and it
would be reached by protocol growth rather than by a new model. A guard-side tripwire now exists —
`test_every_raised_default_actually_clears_its_suite_today` in `ollama/test_context_guard.py`.

## Finding 3 — three defects that stopped models running any lane (found here, FIXED)

Discovered while probing. None is a `num_ctx` *value* defect — each stopped a model from running at
all — so they are recorded here rather than in the raises table. **All three are fixed** in the same
change (`ollama/run_benchmark.py`, `ollama/ollama_a11y.py`, 8 new tests in
`ollama/test_context_guard.py`).

1. **`gemma4:31b` and `gemma4:26b` were hard-blocked.** `/api/tags` reports no `context_length` in
   their `details`, so `fetch_declared_context_length` raised `GuardConfigError` by design ("never a
   silent default"). Both are mapped in `CRITIC_CTX` at 32,768, so two mapped models could not
   execute a single lane; the probes above reached them only because probes bypass the guard.
   **Fix:** fall back to `/api/show`, whose `model_info["<arch>.context_length"]` carries the GGUF
   value the tags summary omits. This is **not a guessed default** — verified 2026-08-27 that
   `/api/show` agrees *exactly* with `/api/tags` on every model reporting both (`qwen3:32b` 40,960,
   `qwen3.6:35b` 262,144, `llama3.3:70b` 131,072), and supplies 262,144 for gemma4 where tags is
   null. Same number, fuller source. When neither source has a value the guard still raises.
   A test pins the case that matters most: **`/api/show` must never override a real `/api/tags`
   ceiling** — `qwen3:32b` still resolves to its clamped 40,960, not the architecture's 262,144,
   which is the clamp F13 exists to catch.

2. **Untagged model names hard-failed the guard.** `fetch_declared_context_length` matched
   `/api/tags`'s `name` exactly, and `/api/tags` always reports a tag suffix. `laguna-xs-2.1` — the
   exact string with 12 committed critic rows *and* a `CRITIC_CTX` entry — raised
   `GuardConfigError`, while `laguna-xs-2.1:latest` resolved. **Fix:** `_tag_variants()` resolves the
   implicit `:latest` in both directions. Only `:latest` is implied — a real tag is never treated as
   interchangeable, so `qwen3.5:27b` and `qwen3.5:latest` stay distinct.

3. **The `*_CTX` maps had the same spelling gap, silently.** The maps are keyed on the caller's
   string; a bare-name entry missed a tagged invocation and dropped that model to the `_DEFAULT`
   with no warning. **Fix:** all six lanes now look up through `ctx_for(model, MAP, DEFAULT)`, and a
   test fails if any lane reverts to a bare `MAP.get(model, DEFAULT)`.

**Corrected from this document's first draft:** it read `PERSPECTIVE_CTX["qwen3.5:27b"]` as a
mis-keyed entry for the installed `qwen3.5:latest`. It is not — `qwen3.5:latest` is **9.7B** and
`qwen3.5:27b` names a 27B that is not installed, the same category as
`PERSPECTIVE_CTX["deepseek-r1:70b"]`. Neither is a typo and neither was changed. The real gap they
sit next to is that **`qwen3.5:latest` (33 committed critic rows) has no entry in either map** — left
unmapped deliberately: with the R5.4 defaults now correct at 32,768 for both lanes it receives the
right window anyway, and adding a mapped entry without a probe of that model would be inventing a
value.

Live verification after the fix — all 13 installed models resolve, both absent names still fail loud,
and `qwen3:32b` still reports its clamped ceiling:

| model | declared_context_length |
|---|---|
| qwen3:32b | **40,960** (clamped ceiling preserved) |
| gemma4:31b, gemma4:26b | 262,144 *(via `/api/show`; previously `GuardConfigError`)* |
| laguna-xs-2.1 *(bare)* | 262,144 *(previously `GuardConfigError`)* |
| qwen3.6:35b, qwen3.6:27b, laguna-xs-2.1:latest, laguna-s-2.1:q4_k_m, qwen3.5:latest, ornith:35b, qwen3.8:27b | 262,144 |
| llama3.3:70b, gpt-oss:120b | 131,072 |
| qwen3.5:27b, not-a-real-model | `GuardConfigError` *(correct — not installed)* |

## Negative space

- **`_DEFAULT`s only.** `CRITIC_CTX`'s 10 mapped entries and `PERSPECTIVE_CTX`'s 7 are unchanged and
  were not re-probed except where a model appears above.
- **One draw per cell.** `num_predict=1` at `temperature=0` makes `prompt_eval_count` deterministic
  for a fixed prompt and tokenizer; no repeat draws were taken, and none of the output-side
  variability the benchmark lanes see applies to a prompt-token count.
- **Largest fixture only** for the governing table. Smaller fixtures were estimated, not probed.
- **Three models.** `llama3.3:70b`, `qwen3.5:latest`, `qwen3.8:27b`, `ornith:35b`, `gpt-oss:120b`,
  `laguna-*` were not probed; the densest-governs rule was applied to the three above.
- **No `evalreport` / `acr` probes.** Those defaults were not raised.
- **No accuracy claim.** Nothing here measures whether any model answers better at a larger window.
  Fit only.
