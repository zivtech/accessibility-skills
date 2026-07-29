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

## Stage 2 — qwen3.6:35b full lanes (2026-07-28, ollama 0.31.1, receipts in `stage2-qwen36-35b/`)

All four lanes completed with zero incompletions and zero empty responses (guards green). Scorer-level results; per the invariants every scorer **miss** requires content adjudication — the critic lane has none to adjudicate:

| Suite | Result | vs qwen3:32b unassisted rebaseline |
|---|---|---|
| a11y-critic (33) | **68/68 must-find** — first full-suite sweep by any local model. 30 PASS / 1 WARN / **1 FAIL** (interactive-dropdown-clean false REJECT — same fixture as its screening draw: a stable, narrow CLEAN failure, not draw noise). button-skip-link-clean judged **correctly** (the incumbent's known miss). | 65/68; 1 wrong CLEAN verdict + 2 finding-raising WARNs |
| perspective-audit (25) | **36/37 must-find** (tab-panel-arrow-keys 1/2). Zero HAS-BUGS verdict failures. CLEAN: 3/5 correct (media-player-captions and dashboard-text-labels wrong; media-player-captions is wrong in every qwen-family draw ever recorded) | 34/37; first-ever HAS-BUGS FAIL (checkout-form); CLEAN 1/5–4/5 draw-unstable |
| planner (25) | 25/25 PASS, 249/250 must-have (test-modal 10/11) | 25/25 (parity) |
| bug-reporting (6) | **First model rows for this suite:** 1 PASS / 1 WARN / 4 FAIL. Structure perfect (7/7 labels + snippet on every report, correct report counts, N/A fields honored). Failures are **value fidelity**: exact selectors dropped (2 fixtures), recomputed stable IDs 0/N verified everywhere checked, and **2 fabrications** — an invented ACT rule id (manual-sr-finding-prose) and an invented Screen-type on the absent-data trap (sparse-scan-adversarial) | no prior rows (instrument-validated suite) |

**Interim profile:** detection and planning at or above the incumbent across every analysis suite, with severity overshoot (REJECT-where-REVISE on ~6 HAS-BUGS fixtures) and a data-fidelity weakness — qwen3.6:35b paraphrases where exactness is required (also seen at 27b: the 10%→20% parameter flip in the WCAG-EM probe). Do not route bug-report *generation* to it without a value-checking pass. The verdict-authority question (routing-rule change) stays open until Stage 3 ×3-draw stability.

## Stage 3 — verdict-stability characterization (2026-07-28, **ollama 0.32.5**, receipts in `stage3-35b/`)

qwen3.6:35b, 9 CLEAN fixtures ×3 draws + flip-set re-draws + a qwen3:32b control draw. Verdict-correctness per draw (✓ = correct verdict, WARN counts as correct with findings; ✗ = wrong verdict):

| CLEAN fixture | d1 / d2 / d3 | Stable? |
|---|---|---|
| button-skip-link (critic) | ✓ / ✗ / ✓ | no |
| interactive-dropdown (critic) | ✗ / ✗ / ✗ | stably wrong |
| modal-complete (critic) | ✓ / ✓ / ✓ | **stable correct** |
| search-results-dynamic (critic) | ✗ / ✗ / ✗ | stably wrong on 0.32.5 (was correct in both 0.31.1 draws — runtime-shift vs draw-variance not disentangled; disclosed, not claimed) |
| article-page (persp) | ✓ / ✗ / ✗ | no |
| login-form (persp) | ✓ / ✓ / ✗ | no |
| nav-menu-landmarks (persp) | ✓ / ✓ / ✓ | **stable correct** |
| dashboard-text-labels (persp) | ✗ / ✗ / ✗ | stably wrong |
| media-player-captions (persp) | ✗ / ✗ / ✓ | no (wrong in every qwen-family draw before this one) |

**Promotion bar (all-3-draws correct on 4/4 critic + ≥4/5 perspective): FAILED — 1/4 critic, 1/5 perspective.** The control run confirms symmetry: qwen3:32b's fresh 0.32.5 draw got 3/4 critic CLEANs and 2/5 perspective CLEANs wrong. Per the plan's own framing, the null result publishes: **no local verdict authority exists at ≤128 GB as of July 2026** — now established against the strongest local candidate ever measured, with a same-day incumbent control.

Flip-set stability (detection side): accordion 2/2 in all three draws; checkout-form 3/3 in all three (the incumbent's variance-FAIL fixture is stable at 35b); tooltip 3/3 → 2/3 → 2/3 (one item flips — the known pair behavior persists).

**Stage-3-backed routing outcome:** the detector recommendation moves to qwen3.6:35b (best detection ever recorded: 68/68 critic sweep, 36/37 perspective, faster than the incumbent, flip-set no worse); the "detector, not a verdict authority" rule is retained verbatim and now applies to the whole local tier. Data-fidelity caveat from the bugreport lane carries into the routing note.

## Status

- **Done:** Stage 0/1 (27b stop, 35b advance, gemma4:31b stop); Stage 2 full lanes for 35b; Ollama 0.31.1 → 0.32.5 upgrade (unblocked Laguna); laguna-s audit + smoke (full offload at 96 GB, ~7–8 min/fixture, advances); Stage 3 + control (above).
- **Running:** laguna-s Stage 1; laguna-xs audit + smoke.
- **Queued:** gemma4:26b, gpt-oss:120b, ornith:35b screenings; BENCHMARK.md rows + routing-note edits (Stage 3 evidence in hand).
