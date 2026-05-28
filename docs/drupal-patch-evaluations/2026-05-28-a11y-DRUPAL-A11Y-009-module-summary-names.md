# Drupal Accessibility Patch Evaluation Packet: DRUPAL-A11Y-009 Module Summary Names

> Status: TEST STATE BLOCKED
> Prepared: 2026-05-28
> Purpose: Local evaluator packet for Mike Gifford's current `a11y-DRUPAL-A11Y-009-module-summary-names` patch.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-DRUPAL-A11Y-009-module-summary-names` |
| Status | `TEST STATE BLOCKED` |
| Project/package | `mgifford/drupal-core` |
| Target commit checked | `3728741f23122018f1f26206fe563cb6c9ad49f8` (`main` on 2026-05-28) |
| Local runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| Evaluation artifact | `docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-009-module-summary-names-evaluation-codex-runtime-smoke-009.{md,json}` |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Local Evaluator Result

Command:

```bash
cd /Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
DRUPAL_BASE_URL=http://drupal-core.ddev.site:33000 \
  A11Y_VARIANT_ID=codex-runtime-smoke-009 \
  node core/tests/playwright/scripts/evaluate-patch.js \
  a11y-DRUPAL-A11Y-009-module-summary-names
```

Result:

```text
Status: INCONCLUSIVE
Outcome reason: no-baseline-instances-observed
Case generation mode: pattern-report-derived
Pattern observed before patch attempt: no
Baseline observed instances: 0
```

The evaluator looked for `#edit-modules-nyan-cat-enable-description > .module-list__module-summary`, but that selector was not present in the local runtime. The page loaded successfully, but no `summary-name` baseline instance was observed.

Source note: a newer source artifact may claim a PASS, but this local packet keeps the status blocked until the missing fixture or an equivalent current module row is reproduced under the same conditions.

## Outcome

`TEST STATE BLOCKED`

The current local run does not confirm or disprove the upstream PASS claim. Next action: install or recreate the missing module-summary fixture that exposes the `nyan_cat` selector, or update the evaluator config to target a current module row that still reproduces the `summary-name` issue before patching.
