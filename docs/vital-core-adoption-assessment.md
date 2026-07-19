# Vital-Core Adoption Assessment

**Decision:** adopt Vital-Core's reporting discipline, not its scanner product.

This assessment covers `/Users/AlexUA_1/claude/vital-core` as reviewed on 2026-06-19. It does not copy runtime code, generated report code, vendor code, crawler state, or dashboard assets into `accessibility-skills`.

## V1 Adoption Matrix

| Surface | Decision | Rationale |
|---|---|---|
| Issue-first findings | adopt | `a11y-test`, `a11y-critic`, and `perspective-audit` benefit from findings that lead with user impact, evidence, expected/actual behavior, and fix direction. |
| Stable finding fingerprints | adopt | Stable IDs make repeated benchmark runs comparable without importing Vital-Core's crawl state or URL identity runtime. |
| Trend language | adopt | `new`, `persistent`, `worsening`, `improving`, and `resolved` are useful for reruns and fixture regression language. |
| Generated-output boundaries | adopt | Vital-Core clearly separates source data from generated reports. This repo should be equally explicit that benchmark claims need runnable commands or committed raw artifacts. |
| Reproducible benchmark gates | adopt | The skill repo already has fixture, scorer, smoke, chain, and mirror gates. The new evidence contract plugs into those gates instead of creating a product dashboard. |
| AI diagnostic export shape | adapt | Vital-Core's `ai-findings.json` idea informs a compact, LLM-friendly evidence contract. The v1 adaptation is prompt-and-scorer guidance, not a JSON export format. |
| Section 508 FPC context | adapt | Use Section 508 and FPC fields as context for impact routing. Do not overstate WCAG 2.2-only findings as Section 508 failures. |
| ACT/WCAG mapping discipline | adapt | Useful as future curated reference data, but v1 only requires explicit WCAG/APG citations and keeps mappings human-reviewable. |
| Accessible report/export design | defer | Could inform a later `a11y-monitor` or report skill after the finding contract proves stable. |
| Continuous crawling | defer | Out of scope for a prompt/eval bundle. This belongs in a separate monitor product, if needed. |
| ISO-week dashboards and ledgers | defer | Valuable for site monitoring, but not for the existing planner/test/critic lifecycle. |
| GitHub Pages publishing | defer | This repo publishes docs, but should not become a generated audit-report app in v1. |
| Multi-engine consensus | defer | axe/Alfa consensus is valuable in Vital-Core. This repo should first prove a source-neutral evidence contract. |
| Mutable crawl state | reject for v1 | `accessibility-skills` has no crawler frontier, no target config, and no week-over-week site state. |
| Scanner runtime code | reject for v1 | Direct reuse is blocked by product scope and license/provenance review. |
| Wappalyzer vendor surface | reject for v1 | Technology fingerprinting is not part of the meta-skill lifecycle and introduces GPL-vendored data scope. |
| ParaCharts vendor/runtime | reject for v1 | Generated dashboard chart runtime is outside the skill/eval boundary and introduces AGPL vendor obligations. |
| Lighthouse, security, sustainability engines | reject for v1 | They are web-quality scanner dimensions, not accessibility meta-skill finding-contract requirements. |

## License and Provenance Gate

Direct code reuse remains blocked until a license/provenance decision reconciles:

- `accessibility-skills` repository license: GPL-3.0-or-later.
- Per-skill frontmatter currently declaring Apache-2.0.
- `vital-core` package license: AGPL-3.0-only.
- Vital-Core vendor surfaces including GPL Wappalyzer fingerprints and AGPL ParaCharts runtime.

Until that decision exists, v1 only adopts concepts, vocabulary, and benchmark expectations. It does not copy implementation code.

## Accepted V1 Contract Impact

- `a11y-test` may wrap failing keyboard, axe, static-analysis, visual, or manual findings in an optional A11y Evidence Finding Contract.
- `a11y-critic` may consume the contract as traceable evidence, while still verifying source, behavior, severity, WCAG/APG grounding, and user impact independently.
- `perspective-audit` preserves `finding_id`, `fingerprint`, `source`, trend, perspective alarms, and ARRM routing when a contract triggers deep review.
- Scorer smoke coverage validates required contract fields, stable IDs, trend values, and false-positive resistance.

## Section 508 and WCAG Boundary

Use WCAG 2.2 AA as the current planning and review target for this bundle. Use Section 508 as regulatory context only when the project scope requires it.

Official references:

- [Section508.gov Applicability and Conformance Requirements](https://www.section508.gov/develop/applicability-conformance/) states that the Revised 508 Standards incorporate WCAG 2.0 Level AA for web and non-web electronic content.
- [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) is the current W3C recommendation this bundle uses as its planning and review target.

## What This Does Not Claim

- This is not a full VPAT, ACR, or legal conformance statement.
- This is not a replacement for manual testing with assistive technology or users with disabilities.
- This does not make `accessibility-skills` a site-scale crawler, generated dashboard, or continuous monitoring product.
- This does not authorize copying Vital-Core AGPL runtime code into this repository.
