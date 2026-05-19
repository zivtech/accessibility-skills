# Ollama Local A11y Skills

Run a11y-critic, a11y-planner, and perspective-audit locally via Ollama — no cloud API required.

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

## Tested Models

| Model | Size | Recommended | Notes |
|-------|------|-------------|-------|
| **qwen3:32b** | 18.8 GB | **Yes — production** | 96% must-find (33 fixtures), 100% perspective-audit, 0% false positives, perfect planner. Reliable on all 3 skills. |
| qwen3.5:27b | 17.4 GB | Detection-critical | 100% must-find (13 HAS-BUGS), found `role="alert"` (only local model to do so). Prone to `/think` stalls on some fixtures — use with retry. NOT tested on perspective-audit. |
| llama3.3:70b | 39.6 GB | Phase-compliant output | 86% must-find (7 fixtures), follows all 11 protocol phases in output. |
| qwen3.5:latest | 6.6 GB | Fast critic-only | 86% must-find (7 fixtures), 3-6x faster. **NOT viable for perspective-audit** (context exhaustion — 50% empty responses). |
| deepseek-r1:70b | 42.5 GB | Preliminary | n=1 fixture only, not fully benchmarked. |

### Cloud Baselines (Claude + OpenAI)

All three platforms benchmarked on 33 critic fixtures with bottom-up escalation:
- **Claude**: Haiku 85% → Sonnet+thinking 100%. Cost: ~$0.65.
- **OpenAI**: GPT-5.2 91% → GPT-5.5-low 100%. Included in Codex subscription.
- **Ollama**: qwen3:32b 100%. Free, local.

All platforms achieve 100% on HAS-BUGS and FLAWED fixtures. Failures are CLEAN (false positives) and ADVERSARIAL (verdict calibration). GPT-5.2 outperforms Haiku on ADVERSARIAL (3/3 vs 0/3).

See [BENCHMARK.md](BENCHMARK.md) for full results.

## Benchmark Results Summary

### a11y-critic

| Model | Fixtures | HAS-BUGS must-find | CLEAN FP | Overall |
|-------|----------|-------------------|----------|---------|
| **GPT-5.2** | **33** | **100%** | 3 CLEAN | **30/33 PASS** |
| Claude Haiku 4.5 | **33** | **100%** | 2 CLEAN | **28/33 PASS** |
| Claude Sonnet 4.6 | 5 (escalated) | n/a | 0% | 4/5 PASS |
| Claude Sonnet 4.6 + think | 1 (escalated) | n/a | 0% | 1/1 PASS |
| GPT-5.2 (low) | 3 (escalated) | n/a | 0% | 1/3 PASS |
| GPT-5.5 | 2 (escalated) | n/a | 0% | 1/2 PASS |
| GPT-5.5 (low) | 1 (escalated) | n/a | 0% | 1/1 PASS |
| qwen3.5:27b | 17* | **100%** | 0%† | 16/17 PASS |
| qwen3:32b | 33 | 96% | 0% | 33/33 PASS |
| llama3.3:70b | 7 | 86% | 0% | 7/7 PASS |
| qwen3.5:latest | 7 | 86% | 0% | 7/7 PASS |

*Run stopped at 17/33 due to `/think` stalls. †1 CLEAN FAIL from context exhaustion (no verdict emitted), not a false positive.*

### a11y-planner (2 of 25 fixtures benchmarked)

| Metric | llama3.3:70b | qwen3:32b |
|--------|-------------|-----------|
| Modal (complex, 15 criteria) | 13/15 (87%) | **15/15 (100%)** |
| Keyboard (focused, 8 criteria) | 8/8 (100%) | **8/8 (100%)** |

### perspective-audit (25 fixtures, qwen3:32b only)

| Tier | Fixtures | PASS | WARN | FAIL | Must-find |
|------|----------|------|------|------|-----------|
| HAS-BUGS | 16 | 16 | 0 | 0 | 100% |
| ADVERSARIAL | 4 | 4 | 0 | 0 | 100% |
| CLEAN | 5 | 0 | 4 | 1* | n/a |

*1 CLEAN FAIL from page-shell scope issue (fixture since fixed).*

### Key Detection Gap

All Ollama models except qwen3.5:27b missed `role="alert"` on the toast fixture (scored 3/4 instead of 4/4). All Claude models found it. This is a real detection gap, not a rubric overlap issue (as initially hypothesized).

## Files

| File | Purpose |
|------|---------|
| `ollama_a11y.py` | Main wrapper — sends skill protocol + input to Ollama |
| `run_benchmark.py` | Benchmark runner — tests Ollama models against graded fixtures |
| `run_cloud_benchmark.py` | Cloud benchmark runner — Claude API + Codex/OpenAI with escalation |
| `codex-benchmark.sh` | Shell entry point for running OpenAI benchmarks from Codex |
| `score_output.py` | Scorer — checks critic output against fixture rubrics |
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

## Benchmarking — Cloud (Claude API + Codex/OpenAI)

Bottom-up escalation: starts with the cheapest tier, runs all fixtures, and only promotes failures to the next tier. Goal: find the minimum viable model per platform.

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

Tiers: `5.2` → `5.2-low` → `5.3` → `5.5` → `5.5-low`

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
