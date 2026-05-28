# Drupal Accessibility Patch Evaluation Packet: DRUPAL-A11Y-002 Submit Button Contrast

> Status: TEST STATE BLOCKED
> Prepared: 2026-05-28
> Purpose: Local evaluator packet for Mike Gifford's current `a11y-DRUPAL-A11Y-002-submit-button-contrast` patch.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-DRUPAL-A11Y-002-submit-button-contrast` |
| Status | `TEST STATE BLOCKED` |
| Project/package | `mgifford/drupal-core` |
| Target commit checked | `3728741f23122018f1f26206fe563cb6c9ad49f8` (`main` on 2026-05-28) |
| Local runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| Evaluation artifact | `docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-002-submit-button-contrast-evaluation-codex-runtime-smoke-002.{md,json}` |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Local Evaluator Result

Command:

```bash
cd /Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
DRUPAL_BASE_URL=http://drupal-core.ddev.site:33000 \
  A11Y_VARIANT_ID=codex-runtime-smoke-002 \
  node core/tests/playwright/scripts/evaluate-patch.js \
  a11y-DRUPAL-A11Y-002-submit-button-contrast
```

Result:

```text
Status: INCONCLUSIVE
Outcome reason: no-baseline-instances-observed
Case generation mode: fallback-config-testCases
Route: /action-link
Baseline observed instances: 0
```

The route loaded and the configured selectors were present for `a[hreflang="he"]` and `#edit-submit`, but no matching `color-contrast` baseline violation was observed.

## Outcome

`TEST STATE BLOCKED`

The current run does not evaluate the patch. Next action: reproduce the yellow-accent button state from the pattern report on an admin/default_admin route, then rerun with a selector/state that observes the contrast failure before patching.
