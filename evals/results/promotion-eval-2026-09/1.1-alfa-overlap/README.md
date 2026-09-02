# Alfa vs axe-core + htmlcs overlap measurement (Phase 1.1)

**Goal:** measure whether the Siteimprove Alfa open-source ACT engine detects WCAG 2.2 A/AA
defect classes that axe-core + HTML_CodeSniffer (via pa11y) miss, on the same 6 public pages.

**Verdict: BELOW THRESHOLD.** Alfa found only **2** distinct A/AA rule classes
(`sia-r14` → SC 2.5.3, `sia-r69` → SC 1.4.3) that neither axe nor htmlcs flagged
on the same page — short of the pre-declared bar of ≥3. Both of the 2 findings
look like genuine, checkable defects (see "Alfa-only findings" below), but the
count bar is not met, and the pre-declared rule is not softened for this result.

Full per-page tables and the verdict computation: `overlap-table.md`.

## Setup

```
cd project && npm init -y
npm install --save-exact \
  @siteimprove/alfa-test-utils@0.84.2 @siteimprove/alfa-playwright@0.84.2 \
  playwright@1.62.1 @axe-core/playwright@4.13.0 pa11y
npx playwright install chromium
```

Full verbatim command log: `commands.sh`.

### Resolved versions

| Package | Requested | Resolved |
|---|---|---|
| `@siteimprove/alfa-test-utils` | 0.84.2 (exact) | 0.84.2 |
| `@siteimprove/alfa-playwright` | 0.84.2 (exact) | 0.84.2 |
| `@siteimprove/alfa-rules` | (transitive) | **0.119.0** |
| `@siteimprove/alfa-wcag` | (transitive) | **0.119.0** |
| `playwright` | 1.62.1 (exact) | 1.62.1 |
| `@axe-core/playwright` | 4.13.0 (exact) | 4.13.0 |
| `axe-core` (transitive of `@axe-core/playwright`) | ~4.13.0 | **4.13.0** |
| `pa11y` | latest | **9.1.1** |
| `@pa11y/html_codesniffer` (bundles HTML_CodeSniffer, transitive of `pa11y`) | ^2.6.0 | **2.6.0** |

Chromium installed via `npx playwright install chromium`: chromium-1205 (matches
playwright 1.62.1's pinned browser build; replaced a stale chromium-1228 cache
entry left from a different playwright version on this machine).

### robots.txt check

- `https://example.com/robots.txt` → HTTP 404 (no robots.txt at all — no restriction).
- `https://www.w3.org/robots.txt` exists and disallows a long list of paths
  (`/WAI/PF/comments/`, `/WAI/events/`, `/WAI/beta/`, `/WAI/ut1-4/`,
  `/WAI/drafts/`, `/WAI/search/`, plus generic CMS/wiki paths). **None of the
  5 target `w3.org` paths used in this measurement** (`/WAI/ARIA/apg/patterns/…`,
  `/WAI/demos/bad/before/*.html`) match any Disallow rule. Clear to proceed.

## Pages scanned

1. https://example.com
2. https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-faq/
3. https://www.w3.org/WAI/demos/bad/before/home.html
4. https://www.w3.org/WAI/demos/bad/before/news.html
5. https://www.w3.org/WAI/demos/bad/before/tickets.html
6. https://www.w3.org/WAI/demos/bad/before/survey.html

Viewport 1280×800, `domcontentloaded` + 3s settle, one run per engine per page.
All three engines ran successfully on all 6 pages — no failed installs or runs.

## Engines

- **axe-core** via `@axe-core/playwright`'s `AxeBuilder`, tags
  `['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']` (no best-practice).
  Note: `AxeBuilder` requires a page created via `browser.newContext().newPage()`
  — a page from a bare `browser.newPage()` throws `"Please use browser.newContext()"`.
  Saved `violations` + `incomplete` per page.
- **htmlcs** via `pa11y({ runners: ['htmlcs'], standard: 'WCAG2AA', includeWarnings: false })`.
  Saved `issues` per page.
- **Alfa** via the documented pattern:
  ```js
  import { Audit } from "@siteimprove/alfa-test-utils";
  import { Playwright as AlfaPlaywright } from "@siteimprove/alfa-playwright";
  const alfaPage = await AlfaPlaywright.toPage(await page.evaluateHandle(() => window.document));
  const audit = await Audit.run(alfaPage);
  const json = audit.toJSON();
  ```
  Ran on the *same* Playwright page/context as the axe-core scan for that page
  (one browser context per page, both engines against it). Saved
  `json.outcomes` + `json.resultAggregates` per page.

  `Audit.run()` with no options runs Alfa's full default rule set — all 89
  "stable"-tagged rules (`@siteimprove/alfa-test-utils` also exports a
  pre-built `Rules.aaFilter` for "WCAG 2.2 A/AA rules only", which was **not**
  used for the run itself so that the A/AA filtering step is done transparently
  in the analysis stage from the same requirements map used for reporting).

  `Audit.toJSON()` confirmed (live probe) to serialize `outcomes` as a flat
  array of `{outcome, rule: {uri}, mode, target, expectations|diagnostic}`
  objects — `rule` is `Rule.MinimalJSON` (uri only, no requirements/tags), so
  the requirements join below is required to get from an outcome back to a
  WCAG SC. `outcome` is one of `inapplicable | passed | failed | cantTell`.
  Alfa's `target` object carries only an internal `serializationId` + node
  `type` (`element`/`text`/`document`/`attribute`), **not** a CSS selector or
  outerHTML — unlike axe (`nodes[].html`) and htmlcs (`.selector`, `.context`),
  Alfa's default JSON gives no serialized markup. The "example target" cells
  in `overlap-table.md` therefore use Alfa's own diagnostic/error message text
  (which is often more informative anyway — e.g. it names computed contrast
  ratios and RGB values directly) rather than a selector.

## Requirements join (uri → WCAG criteria)

Documented exactly, since this is the piece a future reference script needs.

1. `import Rules from "@siteimprove/alfa-rules"` — the package's default
   export is a `Sequence` of all 89 "stable" `Flattened.Rule` objects (the
   same set `Audit.run()` uses by default; there are separate `experimental.js`
   / `deprecated.js` exports for the non-default rule tiers, not used here).
2. For each rule: `rule.uri` (e.g. `https://alfa.siteimprove.com/rules/sia-r1`,
   rule id = the URI's last path segment) and `rule.requirements` — an array
   of `Requirement` objects whose `.type` is one of `criterion | eaa |
   technique | ARIA | best practice`. Only `type === "criterion"` entries are
   actual `@siteimprove/alfa-wcag` `Criterion` instances.
3. Each `Criterion` requirement exposes `.chapter` (WCAG SC number as a string,
   e.g. `"2.4.2"`), `.title` (e.g. `"Page Titled"`), and `.level` — a
   `Branched<Level, Version>` value from `@siteimprove/alfa-branched`. Its
   `.toJSON()` serializes as an array of `[level, [versions...]]` pairs, e.g.
   `[["A",["2.2","2.1","2.0"]]]` or `[["AA",["2.2"]]]` (a criterion's level
   can differ across WCAG versions — 2.5.8 Target Size Minimum, for instance,
   is AA-under-2.2 only and has no 2.0/2.1 entry). We scan this array for the
   pair whose versions list includes `"2.2"` and take that pair's level as
   `level_2_2`. If no pair includes `"2.2"`, the criterion isn't defined under
   2.2 and `level_2_2` is `null` (not observed in this rule set in practice).
4. A single rule can carry more than one criterion requirement — e.g.
   `sia-r11` maps to 2.4.4, 2.4.9, *and* 4.1.2 — so the map value is a list of
   `{criterion, title, level_2_2}`, not a single entry.
5. Rules with zero `"criterion"`-typed requirements (ARIA/technique/best-practice
   only) map to an empty list.
6. Filtering: "keep only outcomes whose mapped level is A or AA under WCAG
   2.2; drop AAA-only rules" is implemented by keeping only
   `level_2_2 === "A" || level_2_2 === "AA"` entries from each rule's mapped
   criteria list, applied per-outcome during analysis (not at audit-run time).

Implementation: `project/build-requirements-map.mjs` → `project/requirements-map.json`.

### Join coverage

- Total Alfa rules: **89**. Rules with ≥1 criterion requirement: **58** (65.2%);
  zero-criterion rules: **31** — these are Alfa's ARIA-technique / best-practice
  / EAA-only rules (e.g. `sia-r48`, `sia-r53`…`sia-r61`; full list in
  `project/requirements-map.json`'s `unmapped` array).
- Of the rule URIs that **actually produced a FAILED outcome somewhere across
  the 6 pages** (22 distinct rule ids): **16 mapped** to ≥1 WCAG criterion,
  **6 did not** → **join coverage 72.7%** on this run's observed outcomes.
- The 6 unmapped-but-FAILED rule ids and what they check (from their
  non-criterion requirement titles):

  | Rule id | Requirement type | What it checks |
  |---|---|---|
  | `sia-r57` | ARIA | WAI-ARIA APG landmark-region general design principles |
  | `sia-r61` | best practice | `document-start-with-level-1-heading` |
  | `sia-r70` | best practice | `no-deprecated-elements` |
  | `sia-r72` | best practice | `paragraph-not-uppercase` |
  | `sia-r85` | best practice | `paragraph-not-italics` |
  | `sia-r87` | technique + best practice | skip-link technique / `first-focusable-is-skip-link` |

  These are all Alfa "best practice" tier checks with no direct WCAG SC
  binding — correctly excluded from the A/AA overlap comparison, not a join
  bug. (Note `sia-r87` shows up here as FAILED on some pages and `cantTell`
  on page 1 — both outcomes are excluded from the A/AA analysis for the same
  reason: no mapped criterion.)

## Analysis

Full per-page tables: `overlap-table.md`. Summary:

- Across the 6 pages, the two "before" WAI-demo pages with the most defects
  (`survey.html`, `news.html`) had 6–8 distinct Alfa A/AA-mapped FAILED rule
  classes each; most of those SCs were also caught by axe and/or htmlcs
  (contrast, image-alt, heading structure, name/role/value, target-size,
  language-of-page all showed up as "≥2 engines" agreement on multiple pages
  — a useful cross-validation signal, not just a gap-finding one).
- `example.com` (page 1) and `disclosure-faq` (page 2, a WAI-ARIA APG
  *reference* example) were near-clean, as expected — page 2 is where Alfa's
  one real gap in the accessible-name area actually surfaced.
- **2 distinct Alfa-only A/AA rule classes** across all 6 pages:

  | Alfa rule | SC | Level | Page | Assessment |
  |---|---|---|---|---|
  | `sia-r14` | 2.5.3 Label in Name | A | 2 (disclosure-faq) | plausible true positive |
  | `sia-r69` | 1.4.3 Contrast (Minimum) | AA | 4 (news.html) | plausible true positive |

  - **`sia-r14`** on the disclosure-faq APG example: Alfa reports the visible
    text content of an element (`"skip to content option0"`) is not included
    in its accessible name (`"skip to content shortcut option 0"`). This is a
    real SC 2.5.3 mismatch pattern — a speech-input user saying the visible
    label wouldn't reliably match. Notable that this shows up on a WAI
    reference implementation page; worth a human look at the live markup to
    rule out a stray templating/duplication artifact in the specific skip-link
    instance, but the reported mismatch itself is a genuine finding class,
    not a parser error.
  - **`sia-r69`** on news.html: Alfa reports a specific *computed* contrast
    ratio (4.02:1) against the AA text threshold (4.5:1), with the actual
    foreground/background sRGB triples it used. This is a falsifiable,
    quantitative claim (not a heuristic guess), and — notably — the *same*
    contrast rule (`sia-r69`) also fires and gets matched by axe's
    `color-contrast` on pages 3, 5, and 6 (shows as "≥2 engines" there), so
    the engine is not systematically miscalibrated; this looks like axe
    missing one specific near-threshold pairing on page 4 that Alfa's
    contrast pairing logic caught.
- Both assessments are **agent-assessed and need human confirmation** — no
  live-page manual verification (e.g. inspecting `news.html`'s actual computed
  styles in a real browser devtools contrast checker) was performed as part
  of this measurement pass.

### Threshold verdict

Pre-declared rule (not softened): Alfa is a "threshold candidate" only if it
fails **≥3 distinct A/AA rule classes** that neither axe nor htmlcs flagged on
the same page, **and** at least one is a plausible true positive on inspection.

- Distinct Alfa-only A/AA rule classes found: **2** (need ≥3) — **count bar not met**.
- At least one plausible true positive among them: **yes** (both, arguably).
- **Verdict: BELOW THRESHOLD.**

This does not mean Alfa found nothing useful — see the "≥2 engines" overlap
rows in `overlap-table.md`, where Alfa cross-validates axe/htmlcs on most of
the real defects on the four "before" demo pages — only that it did not clear
the pre-declared bar for being a *distinct-coverage* addition on this specific
6-page, single-day sample.

## Negative space — what this measurement does NOT show

- **Sample size**: 6 pages, 1 viewport (1280×800), 1 day (2026-09-02). A
  6-page sample with only 2 pages having any real defect density (the other
  4 are either clean or near-clean by design) is not enough to establish a
  stable rate for how often Alfa finds distinct A/AA gaps — the 2-vs-3
  threshold miss could easily flip with a different or larger page sample.
- **Version-specific**: pinned to Alfa 0.84.2 (test-utils/playwright) /
  0.119.0 (rules/wcag), axe-core 4.13.0, HTML_CodeSniffer 2.6.0 as of
  2026-09-02. All three engines update their rule sets independently and
  fairly often; this comparison is not a durable claim about relative rule
  coverage going forward.
- **No keyboard or screen-reader evidence**: all three engines here are
  static/DOM-analysis detectors. None of them execute real keyboard
  interaction or assistive-technology behavior — per this bundle's own
  routing rules, that evidence class comes from a different tool tier
  entirely (Playwright keyboard tests / keyboard-a11y-tester /
  virtual-screen-reader), not from any ACT-rules engine.
- **Detector, not a conformance verdict**: axe-detectable and htmlcs-detectable
  issue classes are themselves a known partial subset of WCAG (axe alone is
  documented elsewhere in this program as roughly 30–40% of issue classes);
  Alfa adds another partial, automatable subset. None of the three, singly or
  combined, constitutes a conformance audit.
- **"Rule availability per version" caveat**: the requirements-join method
  above depends on `@siteimprove/alfa-rules`' `Criterion.level` carrying a
  `"2.2"` branch for the criteria actually exercised in this run. It does,
  for every criterion this run's outcomes touched — but the method has not
  been stress-tested against edge cases like a criterion that exists only
  pre-2.2 (deprecated) or an Alfa rule whose only requirements are `eaa`-typed
  (EU Accessibility Act clauses, not WCAG criteria at all — none of the 89
  rules were eaa-only with zero criterion/other requirements in this set, but
  that's a property of the current 0.119.0 rule set, not a guarantee).
- **SC-level, not defect-instance-level, dedup**: the "flagged by ≥2 engines"
  classification is done at the WCAG-SC granularity per page (any axe
  violation *or* htmlcs error mapped to the same SC counts as "caught"), not
  by matching the *specific DOM element* each engine flagged. Two engines
  agreeing on an SC on a page does not guarantee they found the same instance
  of the defect — nor does an "Alfa-only" SC guarantee axe/htmlcs found
  literally zero instances of anything related; it means neither produced a
  FAILED/error result mapped to that exact SC on that page.
- **Axe tag→SC parsing assumption**: axe-core's `wcagXYZ` tags are parsed as
  principle-digit + guideline-digit + SC-number (unambiguous because WCAG
  guideline numbers never exceed 9), not looked up from an axe-core-shipped
  table. This held for every tag seen in this run's actual violations, but
  wasn't cross-checked against axe-core's full rule metadata for tags that
  didn't appear here.

## Files

- `README.md` — this file.
- `overlap-table.md` — full per-page + cross-page tables and the verdict computation.
- `commands.sh` — verbatim setup/run commands.
- `package.json`, `package-lock.json` — copies of the project's dependency lockfile.
- `raw/page-<1-6>-<axe|htmlcs|alfa>.json` — raw per-page, per-engine output (18 files).
- `project/` — the npm project: `build-requirements-map.mjs`, `run-axe-alfa.mjs`,
  `run-pa11y.mjs`, `analyze.mjs`, `join-coverage.mjs`, `write-overlap-table.mjs`,
  `requirements-map.json`, `join-coverage.json`.

## Reviewer correction (2026-09-02, after the critic pass)

The "Negative space" paragraph above says only 2 of 6 pages had real defect density; the tables in `overlap-table.md` show four defect-dense pages (3–6) and two near-clean ones (1–2). The paragraph is wrong on that count. The sharper limitation it misses: pages 3–6 are four pages of **one authored demo suite** (`/WAI/demos/bad/before/`) with near-identical SC profiles — pages 3, 4, 5 each fail {1.1.1, 1.3.1, 1.4.3, 2.4.4, 2.5.8, 3.1.1, 4.1.2} and page 6 the same set minus 1.4.3. They are one template sampled four times, so the effective number of independent defect-bearing surfaces is about three, not six. That, more than "6 pages, one day", is why a 2-vs-3 result is inside the noise, and the reopen trigger in the dispositions document is stated in independent surfaces rather than page count for this reason. Not measured at all in this run: Alfa's EARL output. Licence, for the record: every `@siteimprove/alfa-*` package resolved here is MIT (see `package-lock.json`).
