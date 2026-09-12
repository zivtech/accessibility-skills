# Design: qwen detector-step pipeline (Stream 2)

**Date:** 2026-09-12 · **Status:** DESIGN — Stage-A harness built (this PR); paid hosted eval gated on explicit approval. Folds an Opus proposal-critic ADVERSARIAL REVISE (2 CRITICAL + 4 MAJOR).
**Goal:** Leverage qwen for the *detection* half of the critic workflow (recall is excellent: must-find 68/68), keeping *judgment* and *value fidelity* hosted — IF a cheap up-front test shows qwen's candidates let the hosted judge do **less real work at equal detection**. Does not move the detector-not-verdict ceiling. ROI gate cleared: hosted-from-scratch critic is run frequently, so there is real spend to save against.

## Pipeline

**qwen PRE-SORT (local, free)** emits `candidates.json` = leads only (`location_hint`, `suspected_class`, `why`, `confidence`) — no verdicts, no exact IDs/selectors → **hosted ADJUDICATE (Claude, paid)**.

## The structural tension — named (critic CRITICAL #2)

M2 (no detection loss) and M3 (no anchoring) push the hosted judge toward independent investigation — the very work the saving needs it to skip. You cannot both distrust qwen enough to protect detector-not-verdict AND trust it enough to let the judge stop investigating. The eval must resolve this, not assume it away.

## "Bounded independent sweep" — PINNED (was the load-bearing ambiguity)

Two candidate pipeline shapes; we pin **Design 1** because it is the one that can save cost, and design the eval to falsify it:

- **Design 1 (cost-saving — the shipped shape under test):** the hosted judge, given the candidate appendix, **adjudicates each candidate (confirm/reject with its own verification) plus runs one structural sweep for the high-severity classes qwen is known to miss** — it does NOT run the full 11-phase from-scratch investigation. The saving = full-protocol generation replaced by adjudicate-plus-bounded-sweep. M2 tests whether this bounded pass loses any must-find vs. the full-protocol baseline; M3 tests over-confirmation. **If M2 shows any detection loss, the bounded sweep is insufficient → Design 1 cannot save safely → kill (or fall back to Design 2).**
- **Design 2 (recall net — fallback only):** judge runs the full protocol; candidates are a post-hoc cross-check. No cost saving; value only if qwen surfaces must-finds the judge missed. Recorded as the fallback if Design 1 fails M2.

This makes detector-not-verdict safe under BOTH: qwen never authors a verdict; the judge always verifies before confirming.

## Stage A — cheap gate, run FIRST (this PR builds the harness; runs are gated)

- **M0 — qwen value-add.** Run the hosted judge in two arms on the same fixtures — **with candidates** (Design 1 bounded pass) vs **blind** (full protocol, no list) — and diff confirmed findings. Value-add = must-finds the with-candidates arm catches that the blind arm's bounded-equivalent would miss, minus any it now misses. If ≈ 0 AND no cost saving, **kill regardless of M1**.
- **M1 — dollar-weighted, caching-aware cost.** Not a token sum. `cost = in×in_price + cache_write×cw_price + cache_read×cr_price + out×out_price` at the tier's published rate, input/output/cache reported separately. Measure **cached and uncached** (production caches the ~fixed critic system prompt; the candidate list is then the marginal cache-miss input). Requires cache-token accounting in `run_cloud_benchmark.py` (records raw input/output only today).

**Stage A decision rule:** proceed to Stage B only if M0 > 0 beyond draw variance AND dollar-weighted M1 (in production's caching mode) shows real saving. Else stop, ~$0 spent.

## Stage B — full safety eval (only if A passes)

Corrected corpus (verified in `evals/suites/a11y-critic/fixtures/`, 50 metadata): **34 HAS-BUGS** (32 REVISE + 2 REJECT), **~11–13 CLEAN**, **7 ACCEPT-WITH-RESERVATIONS** (own class — over-sampled in M3; where anchoring is most dangerous).

- **M2 — no detection loss:** pipeline recall ≥ full-protocol recall on the 34 HAS-BUGS, N ≥ 3 draws/fixture/condition, per-draw + cross-draw adjudication (temp 0.3 flips 2–3 items).
- **M3 — no anchoring, per-item + 3-arm:** paired per-item (P(confirm non-bug | qwen flagged that location) vs base FP rate on that fixture), arms = no-list / list-with-provenance / list-blind-provenance. Bounded against variance (~12 CLEAN + documented 4/5→1/5→4/5 CLEAN instability → a 1–2 item flip is noise).

## ROI (critic MAJOR #6)

Gate cleared (hosted critic used frequently). Second-lane maintenance cost (candidates.json schema, keep monolithic lane, second scoring path, mirror parity, model-churn re-eval tax as qwen versions bump) is real but acceptable given usage. State $/month once Stage A yields per-run numbers.

## Negative space / costs

Not a verdict-authority change (M3 guards). Not a main-session play (Stream 1). Not necessarily a total-token reduction — trades local wall-clock for hosted dollars. Model-churn re-opens M0/M1/M2/M3 per qwen bump. Local pre-sort is serialized before the hosted pass (minutes/fixture on 35b) — real latency. "Local free" is imprecise (contended GPU → the :11435 rule).

## Guardrails

`candidates.json` additive; monolithic qwen lane stays until the gate passes. Any skill-text landing follows the promotion bar.

## Stage-A harness (this PR — free/local only)

1. `ollama/presort-prompt.md` — the detection-only pre-sort system prompt (leads not verdicts; no exact IDs).
2. `ollama/presort_candidates.py` — runs qwen on a fixture, emits schema-valid `candidates.json`; dedicated port (`:11435`).
3. `run_cloud_benchmark.py` — dollar + cache-token accounting (`cache_creation_input_tokens`, `cache_read_input_tokens`, a `PRICES` table, `cost_usd()`), plus a self-test that does not call the API.
4. Local proof: pre-sort run on ≥1 fixture, schema-validated. **No hosted spend in this PR.**
