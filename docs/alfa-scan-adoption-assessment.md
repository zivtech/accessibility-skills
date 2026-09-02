# Alfa scan lane — Adoption Assessment (negative result)

**Decision (2026-09-02):** **not adopted** as a seventh `a11y-test` execution mode. This record exists so the measurement, its boundary, the durable technical findings, and the reopen triggers have a home — the repo's established shape for "we evaluated a tool, here is where it stands" — rather than living only in a dispositions table. Nothing is routed, pinned, or vendored by this decision.

## What was evaluated

Candidate PT-06 from the engagement-tooling promotion catalogue (`docs/plans/2026-09-02-engagement-tooling-promotion-handoff.md`; dispositions in `docs/plans/2026-09-02-promotion-candidate-dispositions.md`). The candidate's job-to-be-done named three value propositions: run a second independent ACT-rules engine beside axe so detections can be **cross-checked**, so rule coverage is **widened**, and with **EARL-native output**.

The engine: [Siteimprove Alfa](https://github.com/Siteimprove/alfa), an open-source ACT-rules implementation. Packages resolved in the measurement (all MIT per the npm registry and the committed lockfile): `@siteimprove/alfa-test-utils@0.84.2`, `@siteimprove/alfa-playwright@0.84.2`, core `@siteimprove/alfa-rules@0.119.0` / `@siteimprove/alfa-wcag@0.119.0`. Single commercial vendor; the paid Siteimprove product sits on the same engine.

Provenance of the candidate: one engagement run whose manifest names three output artifacts that exist on no branch of the private repo, with the manifest's own anchor left `PENDING`. That is a provenance note, not a bar failure — the ledger classes generic tools as n/a for reproductions — but it means the scratch run below is the first retrievable receipt.

## What was measured

Receipts: [`evals/results/promotion-eval-2026-09/1.1-alfa-overlap/`](../evals/results/promotion-eval-2026-09/1.1-alfa-overlap/README.md) (setup, resolved versions, robots check, requirements-join method, per-page tables, raw outputs, verbatim commands, pre-run decision rule).

- **Sample:** six public pages — `example.com`, the WAI-ARIA APG disclosure example, and four pages of the W3C WAI "Before and After Demonstration" *before* site. One viewport (1280×800), one day.
- **Engines on every page:** axe-core 4.13.0 (WCAG 2.x A/AA tags, no best-practice), HTML_CodeSniffer 2.6.0 via pa11y 9.1.1 (`WCAG2AA`), Alfa default stable rule set (89 rules).
- **Decision rule, stated before the run** (`PRE-DECLARATION.md`): Alfa is a coverage candidate only if it FAILS ≥3 distinct A/AA rule classes that neither axe nor htmlcs flagged on the same page, with ≥1 plausible true positive on inspection. `cantTell` outcomes never count as failures.
- **Result:** **2** Alfa-only A/AA rule classes — `sia-r14` → 2.5.3 Label in Name (APG disclosure page: visible text not contained in the accessible name) and `sia-r69` → 1.4.3 Contrast (a quantified 4.02:1 against 4.5:1, with the sRGB triples used). Both plausible true positives; both agent-assessed and **not confirmed against the live pages**.
- **Cross-checking:** succeeded. On the defect-dense pages, Alfa agreed with axe and/or htmlcs on 1.1.1, 1.4.3, 2.4.4, 2.5.8, 3.1.1, 4.1.2.
- **EARL output:** not measured.
- **Requirements join:** 16 of the 22 Alfa rule ids that produced a FAILED outcome map to a WCAG criterion (72.7 %); the other six are best-practice rules with no SC binding — correctly excluded, not a join defect. Across the full set, 58 of 89 rules carry ≥1 criterion requirement.
- **Sample honesty:** the four demo pages are one authored template with near-identical SC profiles, so the run had about three independent defect-bearing surfaces. A 2-vs-3 result is inside that noise.

## Why it was not adopted

1. **Below the pre-stated coverage bar**, and the bar tested the one value proposition (widening) that would justify sending readers to a third engine. A single measurement is single-source; bar clause 1 in `maintain-accessibility-skills` caps that at a doc edit — this file.
2. **A second engine is already routed.** `a11y-test` already sends sitemap-wide sweeps to `pa11y-ci --runner axe --runner htmlcs`; HTML_CodeSniffer is an independent rule engine. The question was never "is there a second engine" but "does Alfa add A/AA classes over axe+htmlcs", and on this sample it added two.
3. **Alfa's default JSON carries no selector or markup for targets** — only an internal serialization id, a node type, and diagnostic text. The bundle's evidence-finding contract builds fingerprints from selector + rule + kind; a lane whose raw output cannot supply a selector would need extra serialization work before its findings could enter the contract at all. That cost was not in the candidate's estimate.

## What was learned (durable, whether or not this reopens)

- `Audit.toJSON()` in `@siteimprove/alfa-test-utils` serializes outcomes at minimal verbosity: `outcome.rule` is `{uri}` only. To get from an outcome to a WCAG criterion, join `rule.uri` against the default export of `@siteimprove/alfa-rules` (a Sequence of the 89 stable rules), read each rule's `requirements`, keep `type === "criterion"`, and resolve the version-branched `level` for `"2.2"`. A rule can map to several criteria (`sia-r11` → 2.4.4, 2.4.9, 4.1.2). The engagement script had hand-coded six rules for exactly this reason.
- `Rules.aaFilter` exists in test-utils for an A/AA-only run; the measurement filtered in analysis instead so the join could be checked transparently.
- Alfa's diagnostic text is often richer than axe's for the same class (contrast findings carry the computed ratio and colours).
- `@axe-core/playwright`'s `AxeBuilder` requires a page from `browser.newContext().newPage()`; a bare `browser.newPage()` throws.
- Exact pins and resolved versions are in the receipt's `package.json` / `package-lock.json`.

## Detector, not a verdict authority

Had it been adopted, the same routing rule as every automated lane would apply: candidate findings for human review, never a conformance verdict; no keyboard or screen-reader evidence; an ACT engine's rule set is a partial, version-specific subset of WCAG.

## Reopen triggers (and where they are checked)

Checked when a candidate ledger or this program is next reviewed; recorded here so they are not a side file nobody populates.

- **(a) Coverage:** ≥5 *independent* defect-bearing surfaces (not pages of one demo template) yield ≥3 Alfa-only A/AA rule classes under the same rule, with ≥1 human-confirmed true positive.
- **(b) Rule sets change materially** in Alfa (`alfa-rules` major) or in axe-core such that the overlap picture could differ.
- **(c) An engagement mandates EARL-native output** — measure Alfa's EARL then; it was not measured here.
- **(d) A maker-published skill, MCP server, or integration appears** that would make this a reuse rather than a build (survey pre-check before any routed instrument: skills.sh, GitHub, npm, the maker's site).

## Escape hatch and dependency risk (if ever adopted)

Routed, never vendored; exact-pinned. MIT is irrevocable for released versions, so a pinned version cannot be withdrawn; the residual risk is single-vendor governance (a future major could relicense), mitigated by the pin. Fallback second engine: `pa11y-ci --runner htmlcs`, already routed. Maintainer bus-factor and transitive supply-chain exposure across the `@siteimprove/*` package family are deferred to their own lenses (`security-ownership-mapper`, `security-threat-model-planner`), not assessed here.

## What this does not claim

- Not that Alfa is a weak engine — it cross-validated the other two on most real defects and found two plausible defects they missed.
- Not a durable statement about relative coverage: one day, one version set, ~3 independent surfaces.
- Not a verdict on EARL: unmeasured.
- Not a routing recommendation of any kind: `a11y-test`'s routing table is unchanged by this file.
