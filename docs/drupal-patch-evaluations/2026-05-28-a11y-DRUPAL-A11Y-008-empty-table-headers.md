# Drupal Accessibility Patch Evaluation Packet: DRUPAL-A11Y-008 Empty Table Headers

> Status: TEST STATE BLOCKED
> Prepared: 2026-05-28
> Purpose: Local evaluator packet for Mike Gifford's current `a11y-DRUPAL-A11Y-008-empty-table-headers` patch.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-DRUPAL-A11Y-008-empty-table-headers` |
| Status | `TEST STATE BLOCKED` |
| Project/package | `mgifford/drupal-core` |
| Target commit checked | `3728741f23122018f1f26206fe563cb6c9ad49f8` (`main` on 2026-05-28) |
| Local runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| Evaluation artifact | `docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-008-empty-table-headers-evaluation-codex-runtime-smoke-008.{md,json}` |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Local Evaluator Result

Command:

```bash
cd /Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
DRUPAL_BASE_URL=http://drupal-core.ddev.site:33000 \
  A11Y_VARIANT_ID=codex-runtime-smoke-008 \
  node core/tests/playwright/scripts/evaluate-patch.js \
  a11y-DRUPAL-A11Y-008-empty-table-headers
```

Result:

```text
Status: INCONCLUSIVE
Outcome reason: baseline-not-observed-due-to-route-unavailable
Case generation mode: pattern-report-derived
Target route: /autocomplete
Baseline HTTP status: 404
Baseline observed instances: 0
```

The evaluator selected `/autocomplete` from the pattern report, but that route was unavailable in the current runtime. No empty-table-header baseline was observed.

## Outcome

`TEST STATE BLOCKED`

The current run does not evaluate the patch. Next action: enable or repair the `autocomplete` fixture route, or retarget the evaluator to a current route that renders the same empty second header cell before patching.
