# Baseline scanner vs Lighthouse accessibility category -- 5 EPA pages, 2026-08-14

Versions: our scanner axe-core 4.13.0 (Playwright 1.62.1) | Lighthouse 13.4.1 (bundled axe-core 4.13.0 -- IDENTICAL) | manual-only Lighthouse audits excluded from all counts below (10 per run, constant: focusable-controls, interactive-element-affordance, logical-tab-order, visual-order-follows-dom, focus-traps, managed-focus, use-landmarks, offscreen-content-hidden, custom-controls-labels, custom-controls-roles)

| URL | both-fire | ours-only | lighthouse-only |
|---|---|---|---|
| comptox.epa.gov/dashboard/ (C01, signal) | aria-allowed-attr, aria-required-parent, color-contrast, html-has-lang, link-in-text-block, list, listitem, target-size | aria-allowed-role, landmark-unique, region | (none) |
| comptox.epa.gov/dashboard/search-results?...caffeine (C02, signal) | aria-allowed-attr, aria-required-parent, button-name, html-has-lang, image-alt, link-in-text-block, list, listitem, tabindex, target-size | aria-allowed-role, empty-table-header, landmark-unique, page-has-heading-one, region | (none) -- NOTE: mobile Lighthouse pass errored wholesale (HTTP 500), see below |
| fire.airnow.gov/ (A07, signal) | button-name, label, meta-viewport | (none) | (none) |
| gispub.epa.gov/airnow/?monitors=ozonepm (A06, signal) | color-contrast, html-has-lang, meta-viewport | empty-heading, label-title-only, region | (none) |
| airnow.gov/about-airnow/ (A20, false-positive check) | (none) | label-title-only, landmark-unique, meta-viewport-large, region | (none) |

Lighthouse-only total across all 5 pages: **0**. Nothing to investigate in the emulation/axe-version/tag-set/DOM-timing queue.

## ours-only classification (8 distinct rule IDs across 5 pages)

| Rule ID | Bucket | Evidence |
|---|---|---|
| region | no-lighthouse-audit | Absent from Lighthouse's ~66-audit `categories.accessibility.auditRefs` entirely (checked `default-config.js` v13.4.1 directly) |
| landmark-unique | no-lighthouse-audit | Same -- Lighthouse only has `landmark-one-main`, a different rule (exactly-one-`<main>`, not accessible-name-uniqueness) |
| label-title-only | no-lighthouse-audit | Same -- no audit registered |
| meta-viewport-large | no-lighthouse-audit | Same -- Lighthouse only has `meta-viewport` (disables-zoom), not the 500%-zoom variant |
| empty-table-header | no-lighthouse-audit | Same -- no audit registered |
| page-has-heading-one | no-lighthouse-audit | Same -- no audit registered |
| aria-allowed-role | lighthouse-informative-cannot-fail | Lighthouse DOES run this axe check; its own LHR shows the identical violating `<ul role="navigation">` node -- but `scoreDisplayMode: informative` is hardcoded in `aria-allowed-role.js`, and `core/audits/audit.js:_normalizeAuditScore` forces `return 1` for ALL informative-mode audits regardless of findings |
| empty-heading | lighthouse-informative-cannot-fail | Same mechanism -- LHR shows the identical `<h2 class="subtitle">` node, forced score=1 |

Zero ours-only hits were 320px-narrow-viewport-exclusive (checked per-rule viewport provenance across all 15 hit instances). Zero were experimental/hidden-tag rules (`label-content-name-mismatch`, `table-fake-caption`, `td-has-header` never fired). Zero were genuine same-audit detection misses -- every ours-only rule traces to one of the two buckets above.

## Reliability anomaly (independent of rule coverage)

Lighthouse's **mobile-emulation** pass on comptox-search failed wholesale: `runtimeError: ERRORED_DOCUMENT_REQUEST`, HTTP 500, reproduced 2/2 (original run + one immediate retry). Isolated to this URL x mobile-mode combination only -- comptox-search **desktop** succeeded (category score 0.62), and our own scanner succeeded at **both** viewports on the identical URL, including the narrow 320x800 (HTTP 200). Most-likely-cause evidence: Lighthouse mobile's `emulatedUserAgent` is an Android/Mobile Chrome string (`...Android 11; moto g power...Mobile Safari...`) with throttling (`cpuSlowdownMultiplier: 4`, `rttMs: 150`), while desktop Lighthouse and our scanner both use non-mobile UAs with no throttling -- pointing at the mobile UA/throttling fingerprint rather than viewport width (our 320px-wide request succeeded fine with a non-mobile UA). Not provable without EPA server-side logs, but reproducible and isolated to one axis.

## Clean-page (false-positive) check -- airnow.gov/about-airnow/

Caveat first: **no page in the entire 40-page 2026-08-13 corpus was literally axe-clean** at either viewport (checked exhaustively against both raw per-rule summaries). This page is the best available proxy: it trips only the 4 shared-template/best-practice rules present on nearly every airnow.gov content page, zero page-specific critical/serious defects, and yesterday's representativeness check confirmed it added no new rule categories.

- Our tool: 4 hits (region, label-title-only, landmark-unique, meta-viewport-large) -- all in the no-lighthouse-audit bucket above.
- Lighthouse: category score **1.0 / 100** on both mobile and desktop -- zero failing audits.
- Asymmetry: not a hallucinated-violation false positive from either side -- our 4 hits are real axe detections, Lighthouse's 1.0 honestly reflects its own narrower rule set. But it IS a "false clean bill of health" risk: a reader trusting Lighthouse's 100/100 alone would conclude zero issues exist, when 4 real (low-severity) axe-detectable issues do -- purely because those 4 rule IDs have no Lighthouse audit, not because Lighthouse evaluated and passed them.

## Bottom line

On these 5 EPA pages (one day, axe-core 4.13.0 on both sides, Lighthouse 13.4.1), our dual-viewport baseline scanner was a **strict superset** of Lighthouse's accessibility category: zero lighthouse-only hits anywhere. Every ours-only rule traces cleanly to Lighthouse's own curated-set-and-scoring design (6 rules entirely unimplemented, 2 more implemented but hardcoded to never fail), not to viewport tricks or experimental noise on our side. This does not generalize beyond this sample -- 5 pages, one day, one version pair -- and a real reliability gap surfaced independent of coverage: Lighthouse's mobile pass failed outright on one URL where both desktop Lighthouse and our own scanner succeeded.
