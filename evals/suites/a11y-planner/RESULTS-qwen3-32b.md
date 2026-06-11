# Planner benchmark results — qwen3:32b (25 fixtures)

- Date: 2026-06-11
- Model: qwen3:32b (Q4_K_M, 20.2 GB), Ollama 0.24.0, native macOS server, full Metal offload
- Runner: `ollama/run_benchmark.py planner` (num_ctx=32768, temperature=0.3, timeout 1200s)
- Scorer: `ollama/score_planner.py` with rubric-supplied `scoring_keywords` (plan 006 Phase A; pilot audit: `PILOT-SCORING-AUDIT.md`, 23/23 agreement, operator-approved)
- Gate: must-have hit rate >= 0.7 -> PASS
- Fallback-keyword warnings during scoring: 0

| Fixture | Must-have hits | Status | Elapsed (s) | Response (chars) |
|---------|---------------|--------|-------------|------------------|
| aria-combobox-autocomplete | 11/11 | PASS | 459 | 10059 |
| aria-data-table-sorting | 10/10 | PASS | 742 | 9276 |
| aria-disclosure-widget | 9/9 | PASS | 316 | 6191 |
| aria-modal-form-validation | 11/11 | PASS | 430 | 10752 |
| aria-tab-dynamic-content | 10/10 | PASS | 487 | 8369 |
| keyboard-breadcrumb | 5/5 | PASS | 609 | 6418 |
| keyboard-button-bar | 6/6 | PASS | 318 | 6138 |
| keyboard-menu-dropdown | 9/9 | PASS | 450 | 10119 |
| keyboard-modal-focus-trap | 10/10 | PASS | 420 | 8803 |
| keyboard-roving-tabindex | 9/9 | PASS | 383 | 8950 |
| sr-article-page | 8/8 | PASS | 417 | 9092 |
| sr-form-field-help | 13/13 | PASS | 577 | 14734 |
| sr-notification-system | 12/12 | PASS | 417 | 10021 |
| sr-product-listing | 8/10 | PASS | 444 | 12470 |
| sr-search-results-live | 11/11 | PASS | 363 | 8947 |
| test-data-table | 13/13 | PASS | 384 | 10744 |
| test-form | 10/11 | PASS | 359 | 9585 |
| test-modal | 9/11 | PASS | 332 | 8868 |
| test-multi-page-audit | 11/11 | PASS | 303 | 7339 |
| test-simple-button | 7/9 | PASS | 246 | 5890 |
| visual-animated-transition | 7/7 | PASS | 329 | 8551 |
| visual-dark-mode | 6/7 | PASS | 476 | 9145 |
| visual-data-viz | 6/6 | PASS | 608 | 11372 |
| visual-form-validation | 10/10 | PASS | 679 | 13457 |
| visual-status-colors | 6/6 | PASS | 607 | 6273 |
| **Total** | **227/235 (96.6%)** | **25/25 PASS** | | |
