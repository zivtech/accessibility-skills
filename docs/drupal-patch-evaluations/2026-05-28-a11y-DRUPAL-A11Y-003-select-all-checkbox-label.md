# Drupal Accessibility Patch Evaluation Packet: DRUPAL-A11Y-003 Select-All Checkbox Label

> Status: FAILED
> Prepared: 2026-05-28
> Purpose: Local evaluator packet for Mike Gifford's current `a11y-DRUPAL-A11Y-003-select-all-checkbox-label` patch.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-DRUPAL-A11Y-003-select-all-checkbox-label` |
| Status | `FAILED` |
| Project/package | `mgifford/drupal-core` |
| Target commit checked | `3728741f23122018f1f26206fe563cb6c9ad49f8` (`main` on 2026-05-28) |
| Local runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| Evaluation artifact | `docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-003-select-all-checkbox-label-evaluation-codex-runtime-smoke-003.{md,json}` |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Issue Summary

| Field | Value |
|---|---|
| Rule/source | `axe-core label-title-only` |
| WCAG SC | `1.3.1 Info and Relationships (A)` in upstream artifacts |
| Routes | `/admin/content`, `/admin/people`; pattern report also lists `/table` |
| Selector | `input[title="Select all rows in this table"]` |
| Pattern ID | `DRU-987EB788` |
| Runtime state | DDEV project `drupal-core`, Drupal 12.0-dev, admin/admin, fixture modules enabled |

## Local Evaluator Result

Command:

```bash
cd /Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
DRUPAL_BASE_URL=http://drupal-core.ddev.site:33000 \
  A11Y_VARIANT_ID=codex-runtime-smoke-003 \
  node core/tests/playwright/scripts/evaluate-patch.js \
  a11y-DRUPAL-A11Y-003-select-all-checkbox-label
```

Result:

```text
Status: FAIL
Outcome reason: targeted-instances-not-fixed
Case generation mode: pattern-report-derived
Baseline observed instances: 1
Fixed instances after patch: 0
Remaining instances after patch: 1
Introduced new violations: 0
```

The `/admin/content` case was skipped because the target selector was not present. The `/admin/people` case observed the target `label-title-only` issue before patching and still observed it after patching.

Runtime readiness note: `/table` already renders the deterministic `input[title="Select all rows in this table"]` baseline, but the current evaluator run did not directly target `/table`. `/admin/content` needs at least one node before it can expose the content-list select-all checkbox. The current patch also appears to target `default_admin` rendering while the local evaluator sets the admin theme to `claro`, so the active render path should be checked before rerolling.

## Gates

- [x] Baseline target observed before patch on at least one target route.
- [x] Patch applied and reverted.
- [x] Same route and state tested after patch.
- [ ] Target rule absent after patch.
- [x] No new violations introduced.
- [ ] Cleaner deterministic `/table` fixture rerun completed.
- [ ] Manual keyboard/screen-reader name smoke check completed.

## Outcome

`FAILED`

The issue is reproducible on `/admin/people`, and the current patch does not fix the observed target instance. Next action: inspect whether the patch targets the right table/select-all render source for the active theme, then rerun with a deterministic `/table` case or seeded admin list rows.
