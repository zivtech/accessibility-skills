# New Local Model Benchmark Plan (2026-07-28)

**Status**: PROPOSED — no runs executed.
**Hardware**: MacBook Pro M5 Max, 128 GB unified memory, ~324 GB free disk.
**Scope**: analysis-only skills (critic, planner, perspective-audit, bug-reporting) via the
`ollama/` wrapper. a11y-test is out of scope (not portable by design).

## Why now

1. Every benchmarked local model was pulled by late May 2026. Since then a full model
   generation shipped: Qwen 3.6 (Apr 2026), Gemma 4 mid/large tags (Apr 2026), Ornith 1.0
   (Jun 2026), Poolside Laguna 2.1 (Jul 2026).
2. Only **one** local row exists on the fully corrected (post-PR-4, unassisted) corpus:
   qwen3:32b, single draw, 2026-07-17→19 (`evals/results/ollama-rebaseline/`). Every other
   local row is hint- and/or verdict-assisted and cannot be compared against new runs.
3. The routing rule ("qwen3:32b is a detector, not a verdict authority") is an open
   challenge: **is there now a local model that combines ≥ qwen3:32b detection with stable
   CLEAN verdicts across draws?** That is the headline question this plan answers.

## Baseline for all comparisons

The **only** valid reference numbers are the post-PR-4 unassisted lane (qwen3:32b):

| Suite | Result | Must-find |
|---|---|---|
| a11y-critic (33) | 30 PASS / 2 WARN / 1 FAIL (wrong REVISE on button-skip-link-clean) | 65/68 content-adjudicated |
| perspective-audit (25) | 19 PASS / 1 WARN / 5 FAIL (first HAS-BUGS FAIL: checkout-form 1/3) | 34/37 content |

Known variance at temperature 0.3: byte-identical prompts flip ±2–3 must-find items and
flip CLEAN verdicts between draws. **No single-draw delta smaller than that may be read as
a model difference.** The reference envelope is n=1 on this corpus, so the plan includes
one additional qwen3:32b CLEAN-lane draw (both suites) as a control.

## Candidates

Verified against ollama.com library pages 2026-07-28 unless marked otherwise.

### Priority 1 — full funnel

| Model | Tag | Size | Arch | Why |
|---|---|---|---|---|
| Qwen 3.6 27B | `qwen3.6:27b` | 17 GB | dense, 256K ctx, thinks by default | Lineage successor to the champion. qwen3.5:27b had the best local detection ever recorded (100% must-find incl. toast `role="alert"`) but failed on `/think` stalls; 3.6's controllable thinking may keep the detection and fix the reliability. |
| Qwen 3.6 35B | `qwen3.6:35b` | 24 GB | dense, 256K ctx | Bigger sibling, same hypothesis, closest size-class to qwen3:32b. |
| Gemma 4 31B | `gemma4:31b` | 20 GB | dense, 256K ctx | First serious non-Qwen candidate since llama3.3. New family diversity matters: Qwen-family blind spots (page-shell over-flagging, checkout label-association) may not transfer. |
| Laguna S 2.1 | `laguna-s-2.1:q4_k_m` | 75 GB | 118B-A8B MoE, 256K ctx, thinking | Capability-ceiling test for this hardware. Built for "extended reasoning"; 8B active params ≈ fast decode despite bulk. OpenMDW-1.1 license. |

### Priority 2 — screen, promote only if Stage 1 clears

| Model | Tag | Size | Arch | Why |
|---|---|---|---|---|
| Gemma 4 26B MoE | `gemma4:26b` | 18 GB | 25.2B-A3.8B MoE | Speed play: ~4B-active throughput would cut full-suite runtimes several-fold if detection holds. |
| gpt-oss 120B | `gpt-oss:120b` | ~65 GB | 117B-A5.1B MoE, adjustable reasoning effort | Not new (Aug 2025) but a coverage gap: the only major open reasoning family with zero rows in BENCHMARK.md. |
| Ornith 35B | `ornith:35b` | ~20 GB (verify at pull) | MoE, MIT | DeepReinforce agentic-coding family (Jun 2026). Coding-specialized, but the critic task *is* code-reading + structured findings. |
| Laguna XS 2.1 | `laguna-xs-2.1` | ~19 GB (verify at pull) | 33B-A3B MoE | Small/fast sibling; candidate for the qwen3.5:latest niche (cheap critic lane). |

Already installed, never benchmarked, **low priority**: `qwen3-coder-next:q8_0` (84 GB) and
`qwen2.5-coder:32b-instruct-q8_0` — coder-tuned and superseded; screen only if idle.
`gemma4:latest` is the e4b edge variant (4.5B effective) — below the viability line
qwen3.5:latest established on perspective-audit; skip.

### Excluded (verified 2026-07-28)

- **Kimi K3** — Ollama cloud-only; no local weights that fit 128 GB.
- **MiniMax M3** — 428B-A23B; ≥192 GB class even quantized.
- **DeepSeek V4-Flash** — 284B MoE; ~90–103 GB only at IQ3/INT4 community quants, leaving
  no KV-cache headroom at 32K ctx on 128 GB. Revisit if an official small variant ships.
- **DeepSeek R3, GLM-5.2** — server-class only.
- **Qwen 3.7** — API-only, closed weights as of 2026-07-28. Watch: Alibaba's pattern is
  open weights 3–4 weeks post-API, already overdue.
- **Mistral Medium 3.5** — appeared in one ≤128 GB roundup; open-weights status
  **unverified**. Watch list, do not pull until confirmed.
- **North Mini Code 1.0** (Cohere 30B-A3B) — coding-only positioning, no evidence edge over
  Ornith/Laguna. Watch list.

## Protocol invariants (carried from the July lanes, non-negotiable)

- Corpus: current `main`; preflight `python3 ollama/test_blind_prompts.py` must print the
  166-prompt OK line before any run.
- Transport: dedicated Metal server on `127.0.0.1:11435`, Ollama.app quit for the whole
  window, `caffeinate -is` wrapping every batch, full offload verified via `/api/ps`
  (`size == size_vram`).
- Runner: `OLLAMA_URL=http://127.0.0.1:11435/api/generate`, `BENCHMARK_RESULTS_DIR` →
  per-lane dir under `evals/results/`; temperature 0.3; num_ctx 16384 critic / 32768
  perspective; scorers (`score_output.py`, `score_perspective.py`, `score_planner.py`,
  `score_bugreport.py`) unmodified.
- Every scorer miss content-adjudicated against response text before it is reported.
- Each lane gets a README following the `evals/results/ollama-rebaseline/` pattern
  (receipts, interruptions, deviations disclosed).

## Pre-run engineering (once, before Stage 0)

1. **Thinking-token audit.** qwen3.6 thinks by default; gemma4, laguna, and gpt-oss expose
   thinking/reasoning. `run_benchmark.py` posts raw `/api/generate`; newer Ollama versions
   can return reasoning in a separate `thinking` field or inline `<think>` blocks depending
   on model/version. Verify per model where reasoning lands and that scorers strip it —
   the existing `<think>` strip logic was never exercised (deepseek-r1 probe emitted none).
   Extend `score_common.py` stripping if a new format appears.
2. **Per-model context.** The `PERSPECTIVE_CTX` map exists for overrides. Thinking models
   may need 32K on the critic suite too (qwen3.5's context-exhaustion stalls were exactly
   this failure). Decide per model at smoke stage; disclose any override in the lane README.
3. **Optional `think:false` escape hatch** for qwen3.6 if stalls appear — mirror of the
   qwen3.5 lesson. Only if needed; a disabled-thinking run is a different condition and
   must be labeled as such.

## Funnel

### Stage 0 — smoke (~15 min/model)

`single <model> form-validation-missing-aria-describedby` + `single <model>
button-skip-link-clean`. Kill criteria: stall >30 min, `done_reason != stop`, unparseable
verdict, reasoning tokens leaking into scored text. Models die here cheaply or not at all.

### Stage 1 — screening (~1 h/model, 10 fixtures)

Critic-suite subset chosen for discrimination, not representativeness:

- 5 HAS-BUGS: `form-validation-missing-aria-describedby` (sanity),
  `toast-notification-no-role` (the `role="alert"` model-differentiator),
  `infinite-scroll-no-announcement` (discoverability item — missed by **every** local model
  in every lane), `accordion-no-region-role` + `tooltip-no-role-no-association` (the
  flip-prone variance pair).
- All 4 CLEAN (`button-skip-link`, `interactive-dropdown`, `modal-complete`,
  `search-results-dynamic`) — the unassisted-verdict test qwen3:32b now fails on 1–3 of.
- 1 ADVERSARIAL: `tabbed-nav-vs-tab-pattern`.

**Gates to advance**: within 2 must-find items of qwen3:32b's unassisted score on the same
subset; ≤1 wrong CLEAN verdict; zero incompletions. Models that fail get a one-paragraph
note in BENCHMARK.md and stop here.

### Stage 2 — full lanes (survivors; ~4–6 h/model dense, less for MoE)

`critic-remaining` (33) → `perspective-remaining` (25) → planner (25) →
`bugreport-remaining` (6). The bug-reporting lane has a validated instrument and **zero
model rows** — the first rows in the suite's history land here for free.

### Stage 3 — verdict-stability characterization (top 1–2 models + qwen3:32b control)

- CLEAN lanes ×3 draws, both suites, plus re-draws of the known flip set (accordion,
  tooltip, checkout-form, modal findings).
- All misses and all CLEAN findings content-adjudicated.
- **Promotion bar for "verdict authority"** (would change the routing rule in CLAUDE.md and
  README): correct CLEAN verdicts in all 3 draws on ≥4/5 perspective CLEAN fixtures and 4/4
  critic CLEAN fixtures (enhancement-level findings tolerated), with must-find inside the
  qwen3:32b variance envelope. If nothing clears, the routing rule stands and the results
  publish anyway — a confirmed "no local verdict authority exists at ≤128 GB, July 2026" is
  a finding.

## Order, time, disk

Run order (value-first): `qwen3.6:27b` → `gemma4:31b` → `gemma4:26b` → `laguna-s-2.1` →
`qwen3.6:35b` → `gpt-oss:120b` → `ornith:35b` → `laguna-xs-2.1`.

- Screening all 8 ≈ 1.5 elapsed days including pulls. Stage 2 for a realistic 3–4
  survivors ≈ 3–5 caffeinated days (sequential residency — one model loaded at a time;
  128 GB cannot co-load laguna-s with anything).
- Disk: all P1+P2 pulls ≈ 240 GB worst case against ~324 GB free. If tight, the pruning
  candidates are `deepseek-r1:70b` (42 GB, n=1 probe, superseded) and `qwen2.5:latest`
  (4.7 GB) — confirm before deleting.

## Reporting

Lane READMEs → BENCHMARK.md rows (bench-reporter conventions) → routing-rule edits in
CLAUDE.md/README **only** on Stage 3 evidence.

## Negative space

- Nothing here re-measures hosted families on the corrected corpus; Claude/GPT/Gemini rows
  remain assisted-era upper bounds until separately re-run.
- HAS-BUGS/FLAWED titles still name their planted defects (open axis from the July
  disclosures) — detection stays title-assisted to that extent, equally for every model.
- Stage 1 gates de-risk time, not conclusions: only full-lane, adjudicated numbers are
  publishable rows.
- Model specs sourced from ollama.com library pages and release coverage on 2026-07-28;
  anything marked "verify at pull" or "unverified" is exactly that.
