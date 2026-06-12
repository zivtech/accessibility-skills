# Claude subagent planner lane — raw artifacts (plan 006 Phase D)

- Run date: 2026-06-12; mechanism: Claude Code `Agent(subagent_type="a11y-planner", model="opus")`, one background subagent per fixture (25 total, parallel).
- Shape: runner-compatible response JSONs (`response` + `_benchmark` provenance); score with `python3 ollama/score_planner.py <json> evals/suites/a11y-planner/fixtures/<id>.metadata.yaml`.
- Summary table: `evals/suites/a11y-planner/RESULTS-claude-opus-subagent.md`; published section: `ollama/BENCHMARK.md` → "Claude subagent lane".
