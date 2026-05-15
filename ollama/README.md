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
| **qwen3:32b** | 18.8 GB | **Yes** | Best value — same detection rate, better WCAG citations, half the size |
| llama3.3:70b | 39.6 GB | For verbose output | Follows all 11 protocol phases, larger responses |
| qwen3.5:latest | 6.6 GB | **Lightweight** | Same accuracy as 32B, 3-6x faster (75-170s vs 300-500s) |
| deepseek-r1:70b | 42.5 GB | Testing | Reasoning model, n=1 preliminary result |
| qwen3.5:27b | 17.4 GB | Testing | Newer Qwen generation, not yet benchmarked |

See [BENCHMARK.md](BENCHMARK.md) for full results.

## Benchmark Results

### a11y-critic (7 fixtures: 3 HAS-BUGS + 4 CLEAN)

| Metric | llama3.3:70b | qwen3:32b |
|--------|-------------|-----------|
| Must-find detection | 6/7 (86%) | 6/7 (86%) |
| False positives on CLEAN | 0/4 (0%) | 0/4 (0%) |
| Verdict accuracy | 7/7 (100%) | 7/7 (100%) |

Both models correctly identify real accessibility bugs (aria-describedby gaps, missing arrow nav, absent live regions) AND correctly accept well-implemented components without manufacturing false findings.

### a11y-planner (2 fixtures: modal dialog + roving tabindex)

| Metric | llama3.3:70b | qwen3:32b |
|--------|-------------|-----------|
| Modal (complex, 15 criteria) | 13/15 (87%) | **15/15 (100%)** |
| Keyboard (focused, 8 criteria) | 8/8 (100%) | **8/8 (100%)** |

Both models produce usable accessibility plans with APG pattern references, focus management strategies, ARIA attribute specs, and HTML stubs. qwen3 adds explicit WCAG criterion numbers.

### What gets detected

Tested against graded fixtures covering:
- Form validation errors not associated via `aria-describedby`
- Missing `aria-live` regions for dynamic content
- Tabs without arrow key navigation
- Toast notifications missing `role`/`aria-live`
- Skip links, dropdowns, modals, search results (CLEAN baselines)

### What gets missed

Both models missed `role="alert"` on a toast fixture while catching the overlapping `aria-live="assertive"`. This appears to be rubric overlap rather than a true blind spot.

## Files

| File | Purpose |
|------|---------|
| `ollama_a11y.py` | Main wrapper — sends skill protocol + input to Ollama |
| `run_benchmark.py` | Benchmark runner — tests models against graded fixtures (critic, planner, perspective) |
| `score_output.py` | Scorer — checks critic/planner output against fixture rubrics |
| `score_perspective.py` | Scorer — checks perspective-audit output (coverage, escalation, ARRM routing) |
| `BENCHMARK.md` | Full benchmark results with per-fixture breakdowns |

## Benchmarking

```bash
# Run CLEAN fixtures (false positive test) on all models
python3 ollama/run_benchmark.py ollama-clean

# Run HAS-BUGS fixtures on all models
python3 ollama/run_benchmark.py ollama-bugs

# Score all critic results
python3 ollama/run_benchmark.py score-all

# Single fixture, single model
python3 ollama/run_benchmark.py single qwen3:32b tabs-missing-arrow-nav

# Perspective-audit: single fixture
python3 ollama/run_benchmark.py perspective qwen3:32b animated-onboarding-flow

# Perspective-audit: pilot set (7 fixtures, one model)
python3 ollama/run_benchmark.py perspective-pilot qwen3:32b

# Score perspective results
python3 ollama/run_benchmark.py score-perspective
```

## Architecture

The wrapper sends the full SKILL.md (minus YAML frontmatter) as the Ollama system prompt and the component/requirements file as the user prompt. No phase-by-phase orchestration — benchmarks proved single-shot works.

For perspective-audit, reference files (perspectives.md, arrm-perspective-mapping.md) are appended to the system prompt automatically. The escalation list (which perspectives are MEDIUM/HIGH) is injected into the user prompt from fixture metadata.

### Tiered Model Routing (Planned)

Route by task difficulty — use the smallest model that produces reliable results:

| Tier | Model | Size | Use For |
|------|-------|------|---------|
| Cloud | Claude Sonnet | API | Adversarial/complex fixtures, baseline comparisons |
| Local L | llama3.3:70b / deepseek-r1:70b | ~42 GB | Subtle bugs, multi-perspective reviews |
| Local M | qwen3:32b / qwen3.5:27b | 17-20 GB | Standard HAS-BUGS, planner tasks |
| Local S | qwen3.5:latest | 6.6 GB | CLEAN false-positive checks, obvious bugs |

### Performance Notes

- **Memory**: Run one model at a time when possible. Loading two large models simultaneously (e.g., 78 GB) on a 128 GB system causes 1.5-2x slowdowns.
- **Speed**: Expect 5-10 minutes per review on 70B models, 3-8 minutes on 32B models, potentially faster on smaller models.
- **Context**: Default 32K token context window. Increase with `--ctx 65536` for very large components.
- **DeepSeek-R1**: Emits `<think>...</think>` reasoning blocks — automatically stripped before scoring.
