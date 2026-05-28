# Drupal Accessibility Patch Evaluation Packet: DRUPAL-A11Y-001 File Widget Display Labels

> Status: INCONCLUSIVE
> Prepared: 2026-05-28
> Purpose: Local evaluator packet for Mike Gifford's current `a11y-DRUPAL-A11Y-001-file-widget-display-labels` patch.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-DRUPAL-A11Y-001-file-widget-display-labels` |
| Status | `INCONCLUSIVE` |
| Project/package | `mgifford/drupal-core` |
| Target commit checked | `3728741f23122018f1f26206fe563cb6c9ad49f8` (`main` on 2026-05-28) |
| Local runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| Evaluation artifact | `docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-001-file-widget-display-labels-evaluation-codex-runtime-smoke-001.{md,json}` |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Issue Summary

| Field | Value |
|---|---|
| Rule/source | `axe-core label` |
| WCAG SC | `1.3.1 Info and Relationships (A)` in upstream artifacts |
| Route | `/contact/imagefile_file` |
| Selector | `[id^="edit-imagefile-file-limited-"][id$="-display"]` |
| Fixture | `theming_tools:imagefile` |
| Runtime state | DDEV project `drupal-core`, Drupal 12.0-dev, admin/admin, fixture modules enabled |

## Local Evaluator Result

Command:

```bash
cd /Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
DRUPAL_BASE_URL=http://drupal-core.ddev.site:33000 \
  A11Y_VARIANT_ID=codex-runtime-smoke-001 \
  node core/tests/playwright/scripts/evaluate-patch.js \
  a11y-DRUPAL-A11Y-001-file-widget-display-labels
```

Result:

```text
Status: PASS
Outcome reason: targeted-issues-fixed-without-regressions
Case generation mode: fallback-config-testCases
Baseline observed instances: 1
Fixed instances after patch: 1
Remaining instances after patch: 0
Introduced new violations: 0
```

The evaluator observed four `label` violations before patching and zero `label` violations after patching on `/contact/imagefile_file`. Remaining non-target violations were `color-contrast` and `region`.

## Gates

- [x] Baseline target observed before patch.
- [x] Patch applied and reverted.
- [x] Same route and state tested after patch.
- [x] Target rule absent after patch.
- [x] No new violations introduced.
- [ ] Pattern report ID mapping reconciled; this run used fallback config cases because no configured pattern IDs were present.
- [ ] Manual screen reader/name smoke check completed.

## Outcome

`INCONCLUSIVE`

Automated evidence supports the patch fixing the targeted label failures in the repaired local runtime. Keep the local packet `INCONCLUSIVE`, not `VERIFIED`, until the pattern ID mapping and required manual accessible-name smoke checks are complete.

Next action: reconcile the configured pattern IDs for this patch so the standard evaluator no longer falls back to config-only test cases.
