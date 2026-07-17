# A11y Model Benchmarks and Local Skills

Run a11y-critic, a11y-planner, and perspective-audit locally via Ollama, then compare those runs against hosted baselines. The benchmark suite is cross-model: Claude, Codex/OpenAI, Gemini, and local models share the same results story, with raw hosted-run artifacts committed under `evals/results/`.

## Prerequisites

- Python 3.10+
- Python packages: `pip3 install -r ollama/requirements.txt` (PyYAML for all
  scorers; `anthropic` only needed for Claude API runs)
- [Ollama](https://ollama.com) installed and serving (`ollama serve`), with at
  least one supported model pulled (see Quick Start)
- For hosted runs only: `ANTHROPIC_API_KEY` exported (Claude), Codex CLI
  authenticated (OpenAI), or gemini CLI authenticated (Gemini) — see
  "Cross-platform baselines" below

## Quick Start

```bash
# Ensure Ollama is running with a supported model
ollama serve  # in another terminal
ollama pull qwen3:32b      # Recommended (18.8 GB, best accuracy-to-size ratio)
ollama pull llama3.3:70b   # Alternative (39.6 GB, follows all protocol phases)

# Review a component for accessibility issues
python3 ollama/ollama_a11y.py critic path/to/component.jsx

# Plan accessibility for a feature before building it
python3 ollama/ollama_a11y.py planner path/to/requirements.md

# Run perspective audit on escalated perspectives
python3 ollama/ollama_a11y.py perspective path/to/component.jsx

# Use a specific model
python3 ollama/ollama_a11y.py critic path/to/component.jsx --model qwen3:32b

# Pipe from stdin
cat component.jsx | python3 ollama/ollama_a11y.py critic -

# JSON output with metadata
python3 ollama/ollama_a11y.py critic component.jsx --json
```

## Tested Local Models

| Model | Size | Recommended | Notes |
|-------|------|-------------|-------|
| **qwen3:32b** | 18.8 GB | **Yes — production** | Blind re-run 2026-07-13: critic 33/33 PASS, 97% must-find, 0 false positives (blind-confirmed); perspective detection 20/20 + 36/37 must-find, **but 4/5 CLEAN fixtures draw false REVISE/BLOCK verdicts blind** (historical "100% perspective, 0% FP" was answer-key-assisted on CLEAN). Perfect planner. |
| qwen3.5:27b | 17.4 GB | Detection-critical | 100% must-find (13 HAS-BUGS), found `role="alert"` (only local model to do so). Prone to `/think` stalls on some fixtures — use with retry. NOT tested on perspective-audit. |
| llama3.3:70b | 39.6 GB | Phase-compliant output | Blind full-suite 2026-07-13: 33/33 PASS, 92.6% must-find scorer / 97.1% adjudicated, zero truncations. Follows all 11 protocol phases in output. |
| qwen3.5:latest | 6.6 GB | Fast critic-only | Blind full-suite 2026-07-13: 33/33 PASS, 98.5% must-find, ~34 s/fixture (fastest lane). **Needs ≥32K num_ctx on long critic fixtures** (4/33 prompts exceed 16K tokens on its tokenizer — empty/truncated otherwise). **NOT viable for perspective-audit** (same context-exhaustion mechanism, 50% empty responses). |
| deepseek-r1:70b | 42.5 GB | Preliminary | n=1 fixture only, not fully benchmarked. |

### Cross-Platform Baselines

Committed result tables currently cover four platform families on 33 critic fixtures with bottom-up escalation:
- **Claude**: Haiku 85% → Sonnet+thinking 100%. Cost: ~$0.65.
- **OpenAI**: GPT-5.2 91% → GPT-5.5-low 100%. Included in Codex subscription.
- **Gemini**: 2.5 Flash 94% (31/33; pro escalation pending account quota). Included in gemini CLI auth; raw artifacts in `evals/results/gemini/`.
- **Ollama**: qwen3:32b 100%. Free, local.

New hosted providers join as peer rows when their runner output is committed; do not collapse the benchmark narrative back to single-provider wording.

Benchmark artifacts are evidence records for the skills. They are not a launch surface for a generated dashboard, crawler runtime, or Vital-Core-derived reporting app.

All platforms achieve 100% on HAS-BUGS and FLAWED fixtures. Failures are CLEAN (false positives) and ADVERSARIAL (verdict calibration). GPT-5.2 outperforms Haiku on ADVERSARIAL (3/3 vs 0/3).

See [BENCHMARK.md](BENCHMARK.md) for full results.

### Persistent results

By default raw responses land in `/tmp` (cleared on reboot). To keep artifacts
for reproducible scoring, set `BENCHMARK_RESULTS_DIR`, e.g.:

    export BENCHMARK_RESULTS_DIR="$HOME/a11y-bench-results"
    mkdir -p "$BENCHMARK_RESULTS_DIR"

Published tables in BENCHMARK.md should only cite runs whose artifacts were
kept this way.

## Benchmark Results Summary

### a11y-critic

| Model | Fixtures | HAS-BUGS must-find | CLEAN FP | Overall |
|-------|----------|-------------------|----------|---------|
| **Codex/OpenAI escalation** | **33** | **100%** | 0 remaining | **33/33 PASS** |
| **Claude API escalation** | **33** | **100%** | 0 remaining | **33/33 PASS** |
| **GPT-5.2** | **33** | **100%** | 3 CLEAN | **30/33 PASS** |
| Claude Haiku 4.5 | **33** | **100%** | 2 CLEAN | **28/33 PASS** |
| Claude Sonnet 4.6 | 5 (escalated) | n/a | 0% | 4/5 PASS |
| Claude Sonnet 4.6 + think | 1 (escalated) | n/a | 0% | 1/1 PASS |
| GPT-5.2 (low) | 3 (escalated) | n/a | 0% | 1/3 PASS |
| GPT-5.5 | 2 (escalated) | n/a | 0% | 1/2 PASS |
| GPT-5.5 (low) | 1 (escalated) | n/a | 0% | 1/1 PASS |
| qwen3.5:27b | 17* | **100%** | 0%† | 16/17 PASS |
| **qwen3:32b BLIND (2026-07-13)** | **33** | **97%** | **0%** | **33/33 PASS** |
| **qwen3.5:latest BLIND (2026-07-13)** | **33** | **98.5%** | **0%** | **33/33 PASS*** |
| **llama3.3:70b BLIND (2026-07-13)** | **33** | **92.6%** (97.1% adjudicated) | **0%** | **33/33 PASS** |
| qwen3:32b (non-blind) | 33 | 96% | 0% | 33/33 PASS |
| llama3.3:70b (non-blind) | 7 | 86% | 0% | 7/7 PASS |
| qwen3.5:latest (non-blind) | 7 | 86% | 0% | 7/7 PASS |

*qwen3.5:latest requires ≥32K `num_ctx` on 4 long fixtures whose prompts tokenize to 15.8K–16.9K
tokens on this model — at the lane-standard 16K they truncate mechanically (`done_reason=length`).
Override re-runs carry explicit provenance; receipts in BENCHMARK.md → "Blind lanes for the
other historical local models".

*Run stopped at 17/33 due to `/think` stalls. †1 CLEAN FAIL from context exhaustion (no verdict emitted), not a false positive.*

Rows dated before 2026-07-13 ran non-blind (fixture answer keys were in the prompts — see the
disclosure in BENCHMARK.md). The blind qwen3:32b row is the corrected basis; raw artifacts:
`evals/results/ollama-blind/`. A second caveat applies to **every** row above, blind lanes
included: until 2026-07-16 the fixture code blocks carried inline `// BUG:` hint comments that
survived answer-key stripping (24/33 critic, 20/25 perspective fixtures), so must-find/detection
numbers are hint-assisted upper bounds — see the hint-comment disclosure in BENCHMARK.md. The
first de-hinted re-run (qwen3:32b, 2026-07-16, `evals/results/ollama-dehinted/`) measures that
bound for this model: **nil on critic** (67/68 content-adjudicated in both lanes, CLEAN 4/4
with zero findings) and **−1 must-find item on perspective** (the hint-carried
`map-interface-zoom` target-size defect; 36/37 vs 37/37). It also re-characterizes the blind
lane's perspective CLEAN weakness (4/5 wrong verdicts) as run-unstable: the re-run drew 1/5
wrong on byte-identical CLEAN prompts. CLEAN false-positive rows are unaffected by hints (CLEAN
fixtures carried none); cross-model comparisons within a lane are unaffected (identical
prompts).

### a11y-planner (25 of 25 fixtures, two lanes)

| Lane | PASS | Must-have criteria | Raw results |
|------|------|--------------------|-------------|
| qwen3:32b (local, 2026-06-11) | 25/25 | 227/235 (96.6%) | `evals/suites/a11y-planner/RESULTS-qwen3-32b.md` |
| Claude Opus subagents (2026-06-12) | 25/25 | 234/235 (99.6%) | `evals/suites/a11y-planner/RESULTS-claude-opus-subagent.md` + `evals/results/claude-planner/` |

Original 2-fixture deep-dive (pre-instrument, retained for history):

| Metric | llama3.3:70b | qwen3:32b |
|--------|-------------|-----------|
| Modal (complex, 15 criteria) | 13/15 (87%) | **15/15 (100%)** |
| Keyboard (focused, 8 criteria) | 8/8 (100%) | **8/8 (100%)** |

### perspective-audit (25 fixtures, qwen3:32b only)

Blind re-run (2026-07-13, post-003 scorers — the corrected basis):

| Tier | Fixtures | PASS | WARN | FAIL | Must-find |
|------|----------|------|------|------|-----------|
| HAS-BUGS | 16 | 16 | 0 | 0 | 36/37 scorer, 37/37 adjudicated |
| ADVERSARIAL | 4 | 4 | 0 | 0 | 100% |
| CLEAN | 5 | 0 | 1 | **4*** | n/a |

*The 4 CLEAN FAILs are genuine blind false positives (REVISE/BLOCK verdicts on clean
components — page-shell over-flagging and verdict inflation; receipts in
`evals/results/ollama-blind/README.md`). Detection is unaffected by blinding; CLEAN
false-positive resistance is not.*

Historical non-blind run (answer keys in prompts; CLEAN row overstated resistance):

| Tier | Fixtures | PASS | WARN | FAIL | Must-find |
|------|----------|------|------|------|-----------|
| HAS-BUGS | 16 | 16 | 0 | 0 | 100% |
| ADVERSARIAL | 4 | 4 | 0 | 0 | 100% |
| CLEAN | 5 | 0 | 4 | 1* | n/a |

*1 CLEAN FAIL from page-shell scope issue (fixture since fixed).*

### Key Detection Gap (revised 2026-07-13)

Ollama qwen3:32b, llama3.3:70b, and qwen3.5:latest missed `role="alert"` on the toast fixture in the historical runs (3/4 instead of 4/4), while Claude models, GPT-5.2, and qwen3.5:27b found it. The blind qwen3:32b re-run **found all 4/4 including `role="alert"`** — so this is run-to-run variance at temperature 0.3, not a stable model-specific gap (and not the rubric overlap initially hypothesized either).

## Files

| File | Purpose |
|------|---------|
| `ollama_a11y.py` | Main wrapper — sends skill protocol + input to Ollama |
| `run_benchmark.py` | Benchmark runner — tests Ollama models against graded fixtures |
| `run_cloud_benchmark.py` | Hosted benchmark runner — Claude API + Codex/OpenAI with escalation; extend with Gemini/other adapters as result sets are added |
| `codex-benchmark.sh` | Shell entry point for running OpenAI benchmarks from Codex |
| `score_output.py` | Scorer — checks critic output against fixture rubrics |
| `test_score_output_contracts.py` | Focused checks for evidence-contract parsing and false-positive bait |
| `score_planner.py` | Scorer — checks planner output against fixture rubrics |
| `score_perspective.py` | Scorer — checks perspective-audit output (coverage, escalation, ARRM routing) |
| `BENCHMARK.md` | Full benchmark results with per-fixture breakdowns |

## Benchmarking — Ollama (Local)

```bash
# Run remaining critic fixtures for a model (skips already-done fixtures)
python3 ollama/run_benchmark.py critic-remaining qwen3:32b

# Run remaining perspective fixtures for a model
python3 ollama/run_benchmark.py perspective-remaining qwen3:32b

# Score all critic results
python3 ollama/run_benchmark.py score-all

# Score all perspective results
python3 ollama/run_benchmark.py score-perspective

# Single fixture, single model
python3 ollama/run_benchmark.py single qwen3:32b tabs-missing-arrow-nav

# Perspective-audit: pilot set (7 fixtures)
python3 ollama/run_benchmark.py perspective-pilot qwen3:32b
```

## Benchmarking — Hosted (Claude API + Codex/OpenAI)

Bottom-up escalation: starts with the cheapest tier, runs all fixtures, and only promotes failures to the next tier. Goal: find the minimum viable model per platform. Add Gemini or other hosted model commands here as adapters land; use the same fixtures, rubrics, and scoring scripts.

### Claude API (requires ANTHROPIC_API_KEY)

Tiers: `haiku` → `sonnet` → `sonnet-think` → `opus`

```bash
# Escalation: starts at Haiku, promotes failures up
python3 ollama/run_cloud_benchmark.py claude-escalate

# Single fixture, specific tier
python3 ollama/run_cloud_benchmark.py claude haiku tabs-missing-arrow-nav

# All fixtures, one tier
python3 ollama/run_cloud_benchmark.py claude-all haiku

# Perspective-audit escalation
python3 ollama/run_cloud_benchmark.py claude-escalate --skill perspective

# Score all Claude results
python3 ollama/run_cloud_benchmark.py score-cloud
```

### Codex/OpenAI (requires Codex CLI auth)

Tiers: `5.2` → `5.2-low` → `5.5` → `5.5-low`

`5.3` is intentionally omitted: the Codex CLI does not expose a GPT-5.3 tier.

Availability note (2026-06-12): ChatGPT-account codex CLI auth now rejects
`gpt-5.2` ("model is not supported when using Codex with a ChatGPT account");
`gpt-5.5` works. The `5.2` tiers remain listed for the historical critic-lane
results — new runs should use `5.5` / `5.5-low`.

```bash
# From Codex: run the escalation benchmark
bash ollama/codex-benchmark.sh

# Or individual commands:
bash ollama/codex-benchmark.sh single 5.2 tabs-missing-arrow-nav
bash ollama/codex-benchmark.sh all 5.2
bash ollama/codex-benchmark.sh score
bash ollama/codex-benchmark.sh perspective

# Or via Python directly:
python3 ollama/run_cloud_benchmark.py codex-escalate
python3 ollama/run_cloud_benchmark.py codex 5.2 tabs-missing-arrow-nav

# Planner lane (plan 010): single fixture, full 25-fixture run, scoring
python3 ollama/run_cloud_benchmark.py codex-planner 5.5-low keyboard-breadcrumb
python3 ollama/run_cloud_benchmark.py codex-planner-all 5.5-low
python3 ollama/run_cloud_benchmark.py score-codex-planner
```

### Gemini (requires gemini CLI auth)

Tiers: `flash` → `pro`. Critic suite only (plan 007 scope). Transport is the
authenticated `gemini` CLI (plan 007 amendment), not an API key. The runner
isolates every call: neutral temp cwd + `--skip-trust` so the CLI cannot load
this repo's own `.agents` skills or workspace context into the model prompt,
`--approval-mode default`, and a headless preamble that forbids file writes
(the CLI agent otherwise tries to "save" the review instead of returning it).
The CLI harness adds ~18.7K input tokens per call; exact per-call token counts
are recorded in each result's `_benchmark` block. Quota note: a pro-tier
capacity exhaustion lands fixtures in the resumable `errored` lane — re-run
`gemini-escalate` after quota reset.

```bash
# FREE: per-fixture prompt sizes + total token estimate, no network
python3 ollama/run_cloud_benchmark.py gemini-dry-run

# Escalation: starts at flash, promotes failures to pro
python3 ollama/run_cloud_benchmark.py gemini-escalate

# Single fixture, specific tier
python3 ollama/run_cloud_benchmark.py gemini flash tabs-missing-arrow-nav

# All fixtures, one tier
python3 ollama/run_cloud_benchmark.py gemini-all flash

# Score all Gemini results
python3 ollama/run_cloud_benchmark.py score-gemini
```

### Cross-Platform Summary

```bash
python3 ollama/run_cloud_benchmark.py summary
```

## Architecture

The wrapper sends the full SKILL.md (minus YAML frontmatter) as the Ollama system prompt and the component/requirements file as the user prompt. No phase-by-phase orchestration — benchmarks proved single-shot works.

For perspective-audit, reference files (perspectives.md, arrm-perspective-mapping.md) are appended to the system prompt automatically. The escalation list (which perspectives are MEDIUM/HIGH) is injected into the user prompt from fixture metadata.

All Ollama API calls use streaming mode to prevent HTTP timeouts during long `/think` reasoning sessions.

### Model Routing

| Skill | Minimum model | Recommended |
|-------|--------------|-------------|
| a11y-critic | qwen3.5:latest (6.6 GB) | qwen3:32b (20 GB) |
| a11y-planner | qwen3.5:latest (6.6 GB) | qwen3:32b (20 GB) |
| perspective-audit | qwen3:32b (20 GB) | qwen3:32b (20 GB) |

### Performance Notes

- **Memory**: Run one model at a time when possible. Loading two large models simultaneously on a 128 GB system causes 1.5-2x slowdowns.
- **Speed**: qwen3:32b averages ~4 min/fixture (critic), ~3 min/fixture (perspective). qwen3.5:latest averages ~2 min (critic only). 70B models average ~6-8 min.
- **Context**: Default 16K token context for critic/planner, 32K for perspective-audit (configurable per model in `run_benchmark.py`).
- **`/think` models**: qwen3 and qwen3.5 use extended reasoning by default. This is what enables high accuracy but can cause context exhaustion on smaller models with complex prompts.
