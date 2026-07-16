# Claude Opus subagent lane — perspective suite results (2026-07-13, BLIND)

Mechanism, blind protocol, and adjudication receipts: [evals/results/claude-perspective/README.md](../../results/claude-perspective/README.md).

**Post-003 scorer: 20 PASS / 5 WARN / 0 FAIL; must-find 36/37. Content-adjudicated: 25/25 correct
verdicts, 37/37 must-find coverage, 0 CRITICAL/MAJOR on all 5 CLEAN fixtures.** (Pre-003 the same
artifacts scored 20 PASS / 1 WARN / 4 FAIL with must-find 35/37 — the deltas are the scorer fixes
recorded in ollama/BENCHMARK.md → Scoring changelog, not model changes.) First lane in this suite run
with the fixture answer key withheld; do not compare 1:1 against previously published non-blind rows.

| Fixture | Class | Post-003 status | Must-find | Adjudication note |
|---|---|---|---|---|
| animated-onboarding-flow | HAS-BUGS | PASS | 2/2 |  |
| article-page-clean | CLEAN | WARN | — | CLEAN: correct PASS verdict, 0 CRITICAL/MAJOR — WARN is the severity-blind finding-count flag (findings are ENHANCEMENT/open-question) |
| autocomplete-fast-timeout | ADVERSARIAL | PASS | 2/2 |  |
| chat-cognitive-load | HAS-BUGS | PASS | 1/1 |  |
| checkout-form-broken-errors | HAS-BUGS | PASS | 3/3 |  |
| color-only-status-indicators | ADVERSARIAL | PASS | 2/2 |  |
| custom-select-combobox | HAS-BUGS | PASS | 2/2 |  |
| dashboard-text-labels | CLEAN | WARN | — | CLEAN: correct PASS verdict, 0 CRITICAL/MAJOR — WARN is the severity-blind finding-count flag (findings are ENHANCEMENT/open-question) |
| data-table-sortable-columns | HAS-BUGS | PASS | 2/2 |  |
| data-viz-color-encoding | HAS-BUGS | PASS | 2/2 |  |
| dense-admin-jargon | HAS-BUGS | PASS | 1/1 |  |
| hover-reveal-navigation | ADVERSARIAL | PASS | 2/2 |  |
| image-gallery-small-targets | HAS-BUGS | PASS | 2/2 |  |
| infinite-scroll-cognitive | ADVERSARIAL | PASS | 2/2 |  |
| login-form-clean | CLEAN | WARN | — | CLEAN: correct PASS verdict, 0 CRITICAL/MAJOR — WARN is the severity-blind finding-count flag (findings are ENHANCEMENT/open-question) |
| map-interface-zoom | HAS-BUGS | PASS | 2/2 |  |
| media-player-captions | CLEAN | WARN | — | CLEAN: correct PASS verdict, 0 CRITICAL/MAJOR — WARN is the severity-blind finding-count flag (findings are ENHANCEMENT/open-question) |
| modal-broken-focus-trap | HAS-BUGS | PASS | 2/2 |  |
| multi-column-pricing | HAS-BUGS | PASS | 1/1 |  |
| nav-menu-landmarks | CLEAN | WARN | — | CLEAN: correct PASS verdict, 0 CRITICAL/MAJOR — WARN is the severity-blind finding-count flag (findings are ENHANCEMENT/open-question) |
| podcast-audio-only | HAS-BUGS | PASS | 1/1 |  |
| product-carousel-autoplay | HAS-BUGS | PASS | 2/2 |  |
| search-results-dynamic-update | HAS-BUGS | PASS | 2/2 |  |
| tab-panel-arrow-keys | HAS-BUGS | PASS | 1/2 | rubric artifact: scoring keyword is the compound string role='tablist'/role='tab'/role='tabpanel'; the audit states each missing role explicitly |
| video-tutorial-no-captions | HAS-BUGS | PASS | 2/2 |  |

Raw audits: the `response` field of each JSON in `evals/results/claude-perspective/`; scorer outputs
committed alongside under `scores/`.
