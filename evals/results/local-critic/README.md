# Newer local-model critics + ensemble simulation

**Date:** 2026-09-12. Goal: find a better free/no-Claude local a11y-critic than the
champion `qwen3.6:35b`, and test whether a **local mixture of models** (cross-family
majority vote) beats any single one. Same 33 fixtures as the Gemini benchmarks
(`evals/results/gemini-3.8/`, `evals/results/gemini/`). Blind-cut, retry-on-empty,
scored with `ollama/score_output.py`. Runner: `ollama/run_local_critic.py`;
ensemble: `ollama/simulate_ensemble.py`.

## Single-model results (PASS of 33)

| Model | PASS | CLEAN false-alarms | Note |
|---|---|---|---|
| **qwen3.6:35b** (current champion) | **31/33** | 1/4 | only `interactive-dropdown-clean` (known family blind spot) |
| gemma4:31b | 28/33 | 4/4 | over-flags every clean fixture; ~174s/fixture (dense) |
| gpt-oss:120b | — | — | **OOM at 11/33** — 65 GB won't co-reside with the shared :11434 instance |
| Gemini 3.8 Flash (hosted, ref) | 28/33 | 4/4 | same 4 CLEAN failures as gemma4 |
| Gemini 2.5 Flash (hosted, ref) | 31/33 | — | prior baseline |

**No newer local model beat `qwen3.6:35b`.** gemma4:31b is worse (over-flags clean code);
gpt-oss:120b is not runnable on this hardware. Champion holds.

## Ensemble simulation — qwen3.6:35b + gemma4:31b (2-of-2)

Verdict-level (a model "flags" if verdict is REVISE/REJECT; CLEAN flag = false alarm).

| Rule | CLEAN false-alarms | HAS-BUGS catches |
|---|---|---|
| union (≥1 flags) | 4/4 | 26/26 |
| unanimous (both flag) | **1/4** | 26/26 |
| qwen3.6:35b alone | 1/4 | 26/26 |

**A local ensemble is not worth building.** Requiring agreement lands at exactly the best
single model (1/4) — it never *beats* it. It only helps relative to a weaker model or a
union (union is strictly worse, 4/4, inheriting gemma4's over-flagging). The one residual
false alarm (`interactive-dropdown-clean`) is **shared by both models** — a correlated
blind spot agreement cannot filter. Cross-family diversity did not decorrelate the errors
here (gemma4 and Gemini 3.8 Flash — both Google — plus qwen all over-flag overlapping
clean fixtures).

**Recommendation:** use `qwen3.6:35b` alone as the local detector; do not build N-model
ensemble infrastructure (N× cost + model-churn maintenance for no precision gain over the
champion). The detector-not-verdict rule stands regardless — a human/stronger judge
remains the arbiter.

## Limits

4 CLEAN fixtures (low power); 2 complete models (gpt-oss:120b OOM'd at 11/33);
recall is measured at verdict level, not per-must-find. Directional, not definitive —
but consistent with theory (correlated errors + best-single dominance).

## Files

`<model-slug>/<fixture>.json` per model. Reproduce a model:
`python3 ollama/run_local_critic.py <model>` (dedicated :11435, one model at a time).
Simulate: `python3 ollama/simulate_ensemble.py <slug> <slug> [...]`.
