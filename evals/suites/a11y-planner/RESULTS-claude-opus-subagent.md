# Planner benchmark results — Claude Opus subagents (25 fixtures)

- Date: 2026-06-12
- Lane: plan 006 Phase D, Claude lane — Claude Code subagents (the production
  mechanism), `Agent(subagent_type="a11y-planner", model="opus")`, one
  background subagent per fixture, all 25 dispatched in parallel
- Task prompt: verbatim `PLANNER_PROMPT_PREFIX` from `ollama/run_benchmark.py`
  ("Plan the accessible implementation for the following component or feature.
  Execute all phases of the planning protocol."); each agent read its fixture
  file and wrote its complete plan via the Write tool; the orchestrator wrapped
  outputs into runner-shaped response JSONs (committed under
  `evals/results/claude-planner/`)
- Scorer: `ollama/score_planner.py` with rubric-supplied `scoring_keywords`
  (post-002 basis, same instrument as the qwen3:32b run)
- Gate: must-have hit rate >= 0.7 -> PASS
- Fallback-keyword warnings during scoring: 0
- Wall-clock: ~12.5 min for all 25 (parallel); per-fixture agent durations below
- Harness-reported subagent tokens, all 25 runs: ~2.55M total
  (includes the a11y-planner agent system prompt per run)

| Fixture | Must-have hits | Status | Elapsed (s) | Response (bytes) |
|---------|---------------|--------|-------------|------------------|
| aria-combobox-autocomplete | 10/11 | PASS | 298 | 57308 |
| aria-data-table-sorting | 10/10 | PASS | 449 | 64799 |
| aria-disclosure-widget | 9/9 | PASS | 168 | 32077 |
| aria-modal-form-validation | 11/11 | PASS | 249 | 47018 |
| aria-tab-dynamic-content | 10/10 | PASS | 294 | 58740 |
| keyboard-breadcrumb | 5/5 | PASS | 237 | 39491 |
| keyboard-button-bar | 6/6 | PASS | 187 | 29240 |
| keyboard-menu-dropdown | 9/9 | PASS | 282 | 49766 |
| keyboard-modal-focus-trap | 10/10 | PASS | 246 | 50004 |
| keyboard-roving-tabindex | 9/9 | PASS | 247 | 44608 |
| sr-article-page | 8/8 | PASS | 242 | 42675 |
| sr-form-field-help | 13/13 | PASS | 330 | 63023 |
| sr-notification-system | 12/12 | PASS | 342 | 65189 |
| sr-product-listing | 10/10 | PASS | 399 | 68241 |
| sr-search-results-live | 11/11 | PASS | 285 | 54150 |
| test-data-table | 13/13 | PASS | 303 | 58019 |
| test-form | 11/11 | PASS | 286 | 53966 |
| test-modal | 11/11 | PASS | 247 | 47379 |
| test-multi-page-audit | 11/11 | PASS | 267 | 43044 |
| test-simple-button | 9/9 | PASS | 131 | 24455 |
| visual-animated-transition | 7/7 | PASS | 287 | 51643 |
| visual-dark-mode | 7/7 | PASS | 314 | 57358 |
| visual-data-viz | 6/6 | PASS | 289 | 46387 |
| visual-form-validation | 10/10 | PASS | 305 | 58503 |
| visual-status-colors | 6/6 | PASS | 194 | 32385 |
| **Aggregate** | **234/235 (99.6%)** | **25/25 PASS** | mean 275 | mean ~49K |

## The single miss (instrument note)

`aria-combobox-autocomplete` 10/11: criterion "Focus management plan: focus
remains in input during navigation" — keyword set
`['focus remains in input', 'focus stays in input', 'focus in the input']`
did not match. The response covers the criterion substantively ("DOM focus
stays on the `<input>` at all times while the listbox is open", "focus does
NOT move to the list. It stays in the input. Highlight is virtual, via
`aria-activedescendant`") in phrasing outside the keyword set. Reported as
scored — the number traces to the instrument, and the limitation is the
documented section-presence-proxy caveat, not a content gap.

## vs qwen3:32b (same instrument, same fixtures)

| Lane | Aggregate | PASS | Partial-hit fixtures |
|------|-----------|------|----------------------|
| qwen3:32b (local, 2026-06-11) | 227/235 (96.6%) | 25/25 | 5 |
| Claude Opus subagents (2026-06-12) | 234/235 (99.6%) | 25/25 | 1 (keyword-phrasing) |

Claude responses are ~5x longer (mean ~49K vs ~9K chars) and slower per
fixture in isolation (mean 275s vs qwen ~450s on Metal — comparable), but the
25 parallel subagents finished in ~12.5 min wall-clock vs the sequential local
run's multi-hour window.
