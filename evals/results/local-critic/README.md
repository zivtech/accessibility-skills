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
| gpt-oss:120b | 3/33† | — | **runs fine alone** (64 GB resident, ~33 s cold / ~6 s hot); refuses to review — stalls on Phase 0 (see below) |
| Gemini 3.8 Flash (hosted, ref) | 28/33 | 4/4 | same 4 CLEAN failures as gemma4 |
| Gemini 2.5 Flash (hosted, ref) | 31/33 | — | prior baseline |

† **Not real detection.** All 33 gpt-oss:120b responses render `Verdict: NONE` — every
one is a Phase 0 prerequisite question ("Have you run the automated tests first?"), zero
findings emitted. The 3 nominal PASSes are `score_output.py` false-credit: its must-find
check is keyword-substring matching, and the stall preambles happen to name the right ARIA
terms. Effective critic score: **0/33.**

**No newer local model beat `qwen3.6:35b`.** gemma4:31b is worse (over-flags clean code);
gpt-oss:120b **runs on this hardware but is not a functioning critic** — it treats the
skill's Phase 0 gate ("critic reviews design after automated tests pass") as a blocking
question and asks for confirmation instead of investigating (33/33). qwen/gemma push
through the same gate. Champion holds — for a stronger reason than "gpt-oss can't run."

### Correction to the first run (2026-09-12)

The initial gpt-oss:120b attempt was abandoned at 11/33 with an OOM and recorded as "not
runnable on this hardware." That was a **co-residency misdiagnosis**: 65 GB OOM'd only
because claude-smart's ~29 GB model was loaded on `:11434` at the same time (65+29 ≈ 94 GB,
over the ~96 GB default macOS `iogpu.wired_limit_mb` cap). Re-run 2026-09-12 with `:11434`
idle: the full 33 completed with no OOM. Disk footprint is irrelevant to this — models
consume zero RAM until loaded; uninstalling other models would not have prevented it.
The correct lever is runtime isolation (nothing co-resident) or raising the wired cap.

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

4 CLEAN fixtures (low power); recall is measured at verdict level, not per-must-find.
gpt-oss:120b is complete (33/33) but non-scoreable as a critic — it never renders a
verdict. Directional, not definitive — but consistent with theory (correlated errors +
best-single dominance). Secondary finding: `score_output.py`'s keyword-substring must-find
check credits non-answers (3 stalls scored PASS) — an over-credit worth hardening later.

## Files

`<model-slug>/<fixture>.json` per model. Reproduce a model:
`python3 ollama/run_local_critic.py <model>` (dedicated :11435, one model at a time).
Simulate: `python3 ollama/simulate_ensemble.py <slug> <slug> [...]`.
