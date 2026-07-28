# New Local Model Benchmark — July 2026 (screening receipts, in progress)

Executes [docs/plans/2026-07-28-new-local-model-benchmark-plan.md](../../../docs/plans/2026-07-28-new-local-model-benchmark-plan.md). This README is the live receipts record; BENCHMARK.md rows land only for full, adjudicated lanes. Baseline for every comparison: the post-PR-4 unassisted qwen3:32b lane (`evals/results/ollama-rebaseline/`).

## Environment (protocol invariants, as run)

- Dedicated Metal server `127.0.0.1:11435`, **ollama 0.31.1**, Ollama.app quit for the window (it self-relaunched once mid-window — an outdated 0.23.0 in-memory process — and was re-quit; the persistent `:11434` responder is the CPU-only OrbStack container, no GPU contention, left alone). `caffeinate -is` wraps every batch; full offload verified per model via `/api/ps`.
- Corpus: benchmark branch `claude/local-model-benchmarks-testing-e1e008` (= main `841903a` + plan + runner fixes below). Preflight `test_blind_prompts.py`: **OK, 166 prompts** (2026-07-28).
- Scorers unmodified. Runner changes on this branch, each measured before scored runs: `CRITIC_CTX` per-model map (`6d3318b`), gemma4 entry, qwen3.6 `PERSPECTIVE_CTX` entries.
- One session restart mid-window (Claude Code process exit): the detached `:11435` server survived; interrupted pull resumed; smoke artifacts verified complete before scoring. The repo directory was renamed `a11y-meta-skills` → `accessibility-skills` mid-window (worktrees repaired; no artifact loss).

## Pre-run engineering findings (apply to all future lanes)

1. **The critic prompt sits at the 16K boundary for current-gen tokenizers**: qwen3.6 tokenizes it at 16,157, gemma4 at 16,477 — at the old 16384 default, generation clips (qwen3.6: `done_reason=length` inside the thinking stream → **silent empty response**) or the prompt itself exceeds the window (gemma4). New models get 32768 via `CRITIC_CTX`. Legacy rebaseline rows stand as-run.
2. **Thinking-token audit per model** (trivial + `num_predict=1` probes): qwen3.6 (both sizes) put reasoning in a separate `thinking` field — scored `response` text is clean by construction; stalls surface as `done_reason != stop`, not `<think>` truncation. gemma4:31b emits no reasoning channel at all. The runner saves neither `done_reason` nor `thinking` — recorded as a hardening item; the first 27b smoke produced silent 0-char artifacts because of it (kept: `stage0/*-ctx16384-FAILED.json`).
3. **laguna-s-2.1:q4_k_m is runtime-incompatible with ollama 0.31.1**: `missing tensor 'blk.0.attn_g.weight'` at load — llama.cpp predates the architecture. Also 96 GB actual vs 75 GB planned. Parked pending an ollama upgrade decision (an upgrade mid-window would change the runtime under comparison and must be its own disclosed condition). laguna-xs expected to share the block.

## Stage 0/1 results (screening subset: 5 HAS-BUGS + 4 CLEAN + 1 ADVERSARIAL)

| Model | Detection (must-find) | CLEAN verdicts wrong (gate ≤1) | Incompletions | Gate verdict |
|---|---|---|---|---|
| qwen3.6:27b | **15/15** — incl. infinite-scroll (missed by every local model in every prior lane) and toast `role="alert"` | **3/4** (false REVISE ×3; search-results correct) | 0 | **STOP** — detector profile, not verdict authority; family trait sharper than qwen3.5 |
| qwen3.6:35b | **15/15** — same perfect subset | **1/4** (interactive-dropdown REJECT; modal-complete correct-with-findings WARN; other two correct) | 0 | **ADVANCE → Stage 2** (full lanes in progress) |
| gemma4:31b | 14/15 (tooltip 2/3) | **4/4** + over-severe REJECT on the ADVERSARIAL fixture | 0 | **STOP** — flags everything; family-diversity hypothesis fails at the verdict layer |
| laguna-s-2.1 | — | — | — | **BLOCKED** (runtime incompatibility above) |

Verdict-severity note (all three scored models): REJECT drawn where REVISE expected on 1–3 HAS-BUGS fixtures each — detection-PASS by the scorer, but severity overshoot is a shared new-generation trait worth watching at Stage 3.

Baseline context for the CLEAN gate: qwen3:32b's own unassisted draw had 1 wrong CLEAN verdict + 2 finding-raising WARNs on this subset, and its CLEAN verdicts are draw-unstable (1/5↔4/5 wrong across perspective draws). 35b's 1-wrong + 1-WARN screening result is at or better than the incumbent — the Stage 3 ×3-draw protocol decides the verdict-authority question, not this single draw.

## Status

- **Stage 2 (qwen3.6:35b): running** — critic-remaining → perspective-remaining → planner-all → bugreport-remaining, with an empty-response guard between lanes (the `-remaining` modes treat any existing artifact as done, so silent empties would otherwise become permanent gaps).
- **P2 pulls**: gemma4:26b, gpt-oss:120b, ornith:35b, laguna-xs-2.1 downloading; each gets audit → ctx decision → smoke → Stage 1 before any full lane.
- Not yet run: qwen3:32b control draw (planned), Stage 3 stability draws.
