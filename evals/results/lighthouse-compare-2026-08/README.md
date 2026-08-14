# Lighthouse vs baseline-url-scan — EPA head-to-head (2026-08-14)

**Question** (asked by Alex during the [client-a-project] coverage work): does the a11y-test mode #6 baseline scanner (`references/baseline-url-scan.mjs`) catch as much as Lighthouse's accessibility category?

**Method:** 5 pages from the 2026-08-13 EPA public-sites corpus (4 with known violations, 1 clean-proxy — no page in that 40-view corpus was literally axe-clean, disclosed in `lighthouse-compare-summary.json`). Each page: mode #6 at its default dual viewports (1280×800 + 320×800) vs `npx lighthouse@13.4.1 --only-categories=accessibility` in both mobile-default and `--preset=desktop` modes. Both tools resolved **identical axe-core 4.13.0** (verified in the npx cache), ruling out version drift.

**Result: mode #6 was a strict superset on every page.**

- **Lighthouse-only findings: zero** (all 5 pages, both emulations).
- **Ours-only rules: 8 distinct**, every one traced to Lighthouse's design, not to our tool over-firing: 6 rules have no audit in Lighthouse's 66-audit set at all (`region`, `landmark-unique`, `label-title-only`, `meta-viewport-large`, `empty-table-header`, `page-has-heading-one`); 2 exist but are `scoreDisplayMode: informative`, which `_normalizeAuditScore` hardcodes to score 1 — they fired identically in the LHR and structurally cannot fail (`aria-allowed-role`, `empty-heading`).
- **False-clean risk:** Lighthouse scored the clean-proxy page 100 in both modes while mode #6 held 4 real low-severity findings — rules its audit set omits.
- **Reliability:** Lighthouse's mobile emulation failed wholesale on one page (HTTP 500, `ERRORED_DOCUMENT_REQUEST`, reproduced 2/2); mode #6 measured the same URL cleanly at both viewports, including 320×800.

**Boundary consequence:** this adjudicates the Lighthouse question in `docs/baseline-url-scan-adoption-assessment.md` empirically — no detection gain, plus a false-clean hazard if Lighthouse's score were trusted alone. Adopting Lighthouse for its non-a11y categories (perf/SEO) remains a separate, open scope decision.

**Caveats (do not over-generalize):** 5 pages, one day, one version pair (Lighthouse 13.4.1 / axe-core 4.13.0). Revisit if Lighthouse materially changes its audit set or scoring. This is an instrument comparison, not a detection-accuracy benchmark against planted ground truth.

**Contents:** `lighthouse-compare-summary.json` (full comparison data) · `compact-table.md` (per-URL table) · `ours/` (mode #6 raw output) · `lighthouse/` (raw LHR JSONs, both emulations) · `urls.txt` + `run-lighthouse.sh` + `compare.py` + `build_final_summary.py` (reproduction recipe; run mode #6 from a dir whose ancestors carry `playwright` + `@axe-core/playwright`).
