# Baseline URL-list scan Adoption Assessment

**Decision:** promote an in-repo one-off evidence harness into a generalized, reusable reference script — the a11y-test skill's sixth execution mode. This is not an external-tool adoption: nothing is vendored, and no license/provenance gate applies beyond the peer dependencies (`playwright`, `@axe-core/playwright`) the skill already assumes elsewhere (`templates/drupal-a11y-patch-evaluation-template.md` already cites `@axe-core/playwright` as an example tool version).

## What Was Adopted

- **In-repo reference script**: [`.claude/skills/a11y-test/references/baseline-url-scan.mjs`](../.claude/skills/a11y-test/references/baseline-url-scan.mjs), promoted 2026-08-14 from the zivtech/a11y-audits repo (private), `2026-08-13-epa-public-sites/evidence/harness/audit-pages.mjs` — a one-off harness run against 40 views during the 2026-08-13 EPA public-sites engagement. The promotion keeps the source harness's sequential-scan-with-polite-delay shape, its dual-viewport lineage (desktop `1280x800` + narrow `320x800` by default, overridable via `--viewports WxH[,WxH...]`, with results keyed per viewport in the per-URL JSON), and its WCAG 2.2 AA axe tag set (`wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`, `best-practice`), but drops its other engagement-specific extras — full DOM structure inventory, ARIA snapshot, keyboard tab-trace, text-spacing reflow probe, per-node XPath computation — to stay a focused baseline/regression tool that takes a plain-text URL list or CLI args instead of a hand-built `corpus.json`. It records the resolved `axe_core_version` in `summary.json`, since rule availability is per-axe-core-version; consuming projects should exact-pin `@axe-core/playwright` themselves rather than rely on this recording alone.
- **Routing**: sixth `a11y-test` execution mode — a routing-table row, a decision-flowchart branch, and a dedicated quickstart section in `SKILL.md`, mirroring the shape of the existing keyboard-a11y-tester and virtual-screen-reader sections. Mirrored into `.agents/skills/a11y-test/` (Codex surface) byte-for-byte; `scripts/check_mirrors.py --strict` passes.
- **`pa11y-ci` as a routed sitemap-sweep alternative**: `npx pa11y-ci --sitemap <url> --runner axe --runner htmlcs`, documented for sitemap-wide sweeps where a maintained, hosted CI tool fits better than a hand-maintained URL list. Routed, not vendored — same boundary as keyboard-a11y-tester and virtual-screen-reader.

## What Was NOT Adopted, and Why

**Lighthouse was rejected** for the axe-scanning role this mode fills, for two reasons:

1. **No detection gain.** Lighthouse's accessibility category is itself axe-core-derived, so running it alongside this mode would not surface violation classes that raw axe-core scanning already misses — it would duplicate the same detector behind a second wrapper, not extend coverage.
2. **Scope exclusion already on record.** [`docs/vital-core-adoption-assessment.md`](vital-core-adoption-assessment.md) already excludes Lighthouse (with security and sustainability engines) on scope grounds: "web-quality scanner dimensions, not accessibility meta-skill finding-contract requirements." Lighthouse's non-accessibility categories (performance, SEO, best practices) sit outside this repo's finding contract, and importing the Lighthouse engine for one category it doesn't uniquely provide would cross that already-drawn line for no coverage benefit.
3. **Empirically verified, same day (2026-08-14).** Head-to-head on 5 EPA pages from the 2026-08-13 corpus, both tools resolving identical axe-core 4.13.0: **zero Lighthouse-only findings; this mode was a strict superset on every page.** Every ours-only rule traced to Lighthouse's own design — 6 rules absent from its 66-audit set (`region`, `landmark-unique`, `label-title-only`, `meta-viewport-large`, `empty-table-header`, `page-has-heading-one`), 2 present but hardcoded `informative` so they structurally cannot fail (`aria-allowed-role`, `empty-heading`). Two operational asymmetries also surfaced: Lighthouse scored a page 100 that carried 4 real axe findings its set omits (a false-clean hazard if the score is trusted alone), and its mobile emulation failed wholesale (HTTP 500, 2/2) on a page this mode measured cleanly at both viewports. Receipts: [`evals/results/lighthouse-compare-2026-08/`](../evals/results/lighthouse-compare-2026-08/README.md). Caveats: 5 pages, one day, Lighthouse 13.4.1 — revisit if its audit set or scoring materially changes.

This began as a **conscious boundary decision surfaced rather than silently resolved**, and was then **empirically adjudicated the same day** (point 3, at Alex's request). Recorded explicitly in case a future engagement wants Lighthouse's non-accessibility categories for a different purpose; that would be a new scope decision, not a reopening of this one.

Plain `pa11y` (the single-page library, distinct from `pa11y-ci`) was not separately evaluated: `pa11y-ci`'s sitemap crawling is the specific capability gap this mode's URL-list scan doesn't fill, so the search stopped at the tool that closes that gap.

## Detector, Not a Verdict Authority

Same routing rule as every other automated lane in this bundle (Ollama models, keyboard-a11y-tester's deterministic layer, axe-core in `.spec.js` files): this mode's output is **candidate findings for human review, never a conformance verdict**. A clean `summary.json` means axe found nothing in its rule set on the URLs scanned — nothing more. Route it as evidence into a11y-critic Phase 0 or the Optional A11y Evidence Finding Contract, not as a pass/fail gate. Axe-core's own detection ceiling — roughly 30-40% of WCAG 2.2 issue classes — applies exactly as it does in `SKILL.md` §4's in-spec-file scans; this mode changes the *granularity* (many URLs, one run) and *packaging* (per-URL JSON plus a summary, no spec file), not the underlying detector's reach.

## Validation Performed

Smoke-tested 2026-08-14 from a scratch directory (deps installed there only, never in this repo): `npm install playwright@1.62.1 @axe-core/playwright@4.13.0 && npx playwright install chromium`, then the committed script (byte-diff-verified unmodified) run against two public URLs:

```
node baseline-url-scan.mjs --out ./out https://example.com \
  https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-faq/
```

Result (initial, single-viewport version): 2/2 URLs measured, 0 errors, 6 violation nodes across 5 rules (1 serious `frame-title`, 5 moderate — `region`, `heading-order`, `landmark-no-duplicate-contentinfo`, `landmark-one-main` ×2). Per-URL JSON carried rule id, impact, node count, and sample selectors (e.g. `frame-title` → `["iframe"]`); `summary.json` aggregated correctly across both pages.

**Re-validated the same day** after the dual-viewport and axe-version follow-ups landed, against one URL:

```
node baseline-url-scan.mjs --out ./out2 https://example.com
```

Result: both configured viewports (`1280x800`, `320x800`) ran and appear as separate keys in the per-URL JSON, each with its own `violations`/`incomplete`/`axe_core_version`; `summary.json` reports `schema_version: "1.1"`, `axe_core_version: "4.13.0"` at the top level, and `totals.viewport_scans: 2` (1 URL × 2 viewports, both measured, 0 errors). This is a runs-cleanly check, not a detection-accuracy benchmark — no fixture with planted defects and known ground truth was run against this script.

## What This Does Not Claim

- Not a replacement for `.spec.js` codified tests, `agent-browser` reconnaissance, keyboard-a11y-tester journey audits, or virtual-screen-reader component assertions — those remain necessary for the keyboard-operability, screen-reader-announcement, and CI-embedded evidence this mode never produces.
- Not a WCAG-EM sampling methodology by itself — it executes a URL list; deciding *which* URLs go in that list (structured + 10% random + representativeness check) stays a planner/test-skill responsibility.
- Not a vendored dependency: `playwright` and `@axe-core/playwright` are peer dependencies installed in the consuming project, never added to this (nonexistent) repo package.json.
- Not a Lighthouse integration, now or implicitly — see the boundary decision above.
- Not a detection-accuracy benchmark against known ground truth — see Validation Performed above.
- **Not carrying the EPA harness's keyboard tab-trace capability — dropped deliberately, not lost accidentally.** The source harness recorded an `observedTabTrace` per page (30 Tab presses, focus/name/role/style per step); this mode never presses a key. Keyboard evidence routes to `keyboard-a11y-tester` (journey-level) or `npx playwright test` with the APG templates (widget-level) per the routing table above — this mode stays axe-only by design.
