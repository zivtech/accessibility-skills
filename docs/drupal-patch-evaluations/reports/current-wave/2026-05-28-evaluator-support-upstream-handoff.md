# Evaluator Support Upstream Handoff

> Date: 2026-05-28
> Scope: Drupal accessibility evaluator infrastructure
> Patch artifact: `docs/drupal-patch-evaluations/patches/evaluator-support/codex-evaluator-support-baseurl-rule-alias-runonly-selector-hints.patch`

## Purpose

This patch makes the local Drupal accessibility evaluator more portable and more faithful to the packets it is asked to verify. It is not a Drupal product accessibility patch. It supports the review workflow around those patches by reducing false negatives caused by local runtime assumptions, axe rule naming drift, and broad target selectors.

## Changes

1. Make the evaluator base URL configurable with `DRUPAL_BASE_URL` or `DRUPAL_TEST_BASE_URL`, while preserving the existing `http://drupal-core.ddev.site` default.
2. Restore `core/tests/playwright/scripts/lib/canonical-patch-map.js` so the evaluator can load the known-safe patch list from the local `patches/` directory.
3. Alias the human-facing `label-in-name` rule label to axe-core's concrete `label-content-name-mismatch` rule ID.
4. Run explicit `runOnly` axe scans for required packet rules, then merge those results with the default axe scan. This catches required rules that axe does not include in its default rule set.
5. Allow selector-hint matching for configured targets such as `table a:has-text("Configure")` when axe reports the concrete failing selector differently.

## Validation

Syntax checks passed in the disposable Drupal runtime:

```bash
node --check core/tests/playwright/scripts/evaluate-patch.js
node --check core/tests/playwright/scripts/evaluate-all-patches.js
node --check core/tests/playwright/scripts/lib/canonical-patch-map.js
```

The evaluator changes were also exercised by current-wave evidence:

- `LABEL-IN-NAME-004-filter-format-aria-label` passed after the `label-in-name` alias, explicit required-rule scan, and selector-hint matching were in place.
- `DRUPAL-A11Y-007-messages-landmark-role` passed after the reroll and cleaned evaluator run, with before/after evidence saved under `docs/drupal-patch-evaluations/reports/evaluator-runs/`.

## Boundaries

This handoff does not claim that every Drupal accessibility patch is verified. It only claims that the evaluator can now run in the current disposable DDEV runtime and can test packet rules that were previously missed or mismatched.

The `canonical-patch-map.js` restoration may be reviewed separately from the rule-resolution and base-URL changes if maintainers prefer a smaller first patch. If the hardcoded DDEV hostname was intentional policy rather than a local assumption, the base-URL environment override should be discussed before upstreaming.

## Recommended Upstream Framing

Frame this as evaluator reliability work:

- It makes local and CI-like evaluator runs less dependent on a single DDEV hostname.
- It aligns packet terminology with axe-core rule IDs without forcing packet authors to use implementation-specific rule names.
- It avoids false negatives when target selectors are intentionally written as human-readable Playwright hints.

The weakest part of the case is that this is currently proven through local runtime evidence, not a committed evaluator test suite. Before filing upstream, add or identify a focused evaluator unit/integration test if the project already has a test harness for these scripts.
