# Claude Opus subagent lane — perspective suite results (2026-07-13, BLIND)

Mechanism, blind protocol, and adjudication receipts: [evals/results/claude-perspective/README.md](../../results/claude-perspective/README.md).

**Raw scorer: 20 PASS / 1 WARN / 4 FAIL. Content-adjudicated: 25/25** (all deductions are scorer
artifacts — verdict-fallback ladder hits and quote-style keyword misses — receipted against the
committed audits). First lane in this suite run with the fixture answer key withheld; do not compare
1:1 against previously published non-blind rows.

| Fixture | Class | Scorer status | Must-find (scorer) | Adjudicated | Note |
|---|---|---|---|---|---|
| animated-onboarding-flow | HAS-BUGS | PASS | 2/2 | PASS |  |
| article-page-clean | CLEAN | WARN | — | PASS* | findings are ENHANCEMENT/open-question only; 0 CRITICAL/MAJOR — CLEAN bar met |
| autocomplete-fast-timeout | ADVERSARIAL | PASS | 2/2 | PASS |  |
| chat-cognitive-load | HAS-BUGS | PASS | 1/1 | PASS |  |
| checkout-form-broken-errors | HAS-BUGS | PASS | 3/3 | PASS |  |
| color-only-status-indicators | ADVERSARIAL | PASS | 2/2 | PASS |  |
| custom-select-combobox | HAS-BUGS | PASS | 1/2 | PASS† | keyword quote-style miss — role content present verbatim in audit |
| dashboard-text-labels | CLEAN | FAIL | — | PASS* | scorer verdict artifact — fallback ladder matched boilerplate 'BLOCK'; audit concludes PASS with 0 CRITICAL/MAJOR |
| data-table-sortable-columns | HAS-BUGS | PASS | 2/2 | PASS |  |
| data-viz-color-encoding | HAS-BUGS | PASS | 2/2 | PASS |  |
| dense-admin-jargon | HAS-BUGS | PASS | 1/1 | PASS |  |
| hover-reveal-navigation | ADVERSARIAL | PASS | 2/2 | PASS |  |
| image-gallery-small-targets | HAS-BUGS | PASS | 2/2 | PASS |  |
| infinite-scroll-cognitive | ADVERSARIAL | PASS | 2/2 | PASS |  |
| login-form-clean | CLEAN | FAIL | — | PASS* | scorer verdict artifact — fallback ladder matched boilerplate 'BLOCK'; audit concludes PASS with 0 CRITICAL/MAJOR |
| map-interface-zoom | HAS-BUGS | PASS | 2/2 | PASS |  |
| media-player-captions | CLEAN | FAIL | — | PASS* | scorer verdict artifact — fallback ladder matched boilerplate 'BLOCK'; audit concludes PASS with 0 CRITICAL/MAJOR |
| modal-broken-focus-trap | HAS-BUGS | PASS | 2/2 | PASS |  |
| multi-column-pricing | HAS-BUGS | PASS | 1/1 | PASS |  |
| nav-menu-landmarks | CLEAN | FAIL | — | PASS* | scorer verdict artifact — fallback ladder matched boilerplate 'BLOCK'; audit concludes PASS with 0 CRITICAL/MAJOR |
| podcast-audio-only | HAS-BUGS | PASS | 1/1 | PASS |  |
| product-carousel-autoplay | HAS-BUGS | PASS | 2/2 | PASS |  |
| search-results-dynamic-update | HAS-BUGS | PASS | 2/2 | PASS |  |
| tab-panel-arrow-keys | HAS-BUGS | PASS | 1/2 | PASS† | keyword quote-style miss — role content present verbatim in audit |
| video-tutorial-no-captions | HAS-BUGS | PASS | 2/2 | PASS |  |

`*` scorer artifact adjudicated against the audit's literal verdict line. `†` scorer keyword artifact
adjudicated against the audit's findings text. Raw audits: the `response` field of each JSON in
`evals/results/claude-perspective/`.
