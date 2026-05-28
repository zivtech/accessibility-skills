# Drupal Accessibility Patch Evaluation Packet: LABEL-IN-NAME-004 Filter Format Configure Link

> Status: VERIFIED
> Prepared: 2026-05-28
> Purpose: Local evaluator packet for Mike Gifford's current `a11y-LABEL-IN-NAME-004-filter-format-aria-label` patch.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-LABEL-IN-NAME-004-filter-format-aria-label` |
| Status | `VERIFIED` |
| Project/package | `mgifford/drupal-core` |
| Target commit checked | `3728741f23122018f1f26206fe563cb6c9ad49f8` (`main` on 2026-05-28) |
| Local runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| Evaluation artifact | PASS: `docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-LABEL-IN-NAME-004-filter-format-aria-label-evaluation-codex-selector-hint-label-004.{md,json,html}`; earlier inconclusive run: `docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-LABEL-IN-NAME-004-filter-format-aria-label-evaluation-codex-runtime-smoke-label-004.{md,json}` |
| Manual check | `docs/drupal-patch-evaluations/reports/manual-checks/2026-05-28-label-in-name-004-manual-axe.md` |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Local Evaluator Result

Initial command:

```bash
cd /Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
DRUPAL_BASE_URL=http://drupal-core.ddev.site:33000 \
  A11Y_VARIANT_ID=codex-runtime-smoke-label-004 \
  node core/tests/playwright/scripts/evaluate-patch.js \
  a11y-LABEL-IN-NAME-004-filter-format-aria-label
```

Result:

```text
Status: INCONCLUSIVE
Outcome reason: no-baseline-instances-observed
Case generation mode: fallback-config-testCases
Route: /admin/config/content/formats
Selector count: table a:has-text("Configure") = 4
Baseline observed instances: 0
```

The evaluator report is inconclusive because the configured rule is `label-in-name`, while axe-core 4.11.4 exposes the relevant rule as `label-content-name-mismatch`.

### Rerun After Evaluator Support

I updated the local runtime evaluator so it:

- maps `label-in-name` to axe-core's `label-content-name-mismatch`,
- runs required non-default axe rules explicitly with `runOnly`,
- matches broad Playwright selector hints such as `table a:has-text("Configure")` to axe's concrete failing selectors.

Rerun command:

```bash
cd /Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
DRUPAL_BASE_URL=http://drupal-core.ddev.site:33000 \
  A11Y_VARIANT_ID=codex-selector-hint-label-004 \
  node core/tests/playwright/scripts/evaluate-patch.js \
  a11y-LABEL-IN-NAME-004-filter-format-aria-label
```

Result:

```text
Status: PASS
Outcome reason: targeted-issues-fixed-without-regressions
Case generation mode: fallback-config-testCases
Baseline observed instances: 1
Fixed instances after patch: 1
Remaining instances after patch: 0
Total axe violations: 5 before, 1 after
Fixed rule: label-content-name-mismatch 4 -> 0
Introduced new violations: 0
```

## Manual Rule Check

Manual Playwright plus axe-core check on `/admin/config/content/formats`:

```text
Before patch:
- axe rule label-content-name-mismatch: 4 failing nodes
- visible text: Configure
- aria-label values: Edit Basic HTML, Edit Restricted HTML, Edit Full HTML, Edit Plain text

After patch:
- axe rule label-content-name-mismatch: 0 failing nodes
- aria-label values: Configure Basic HTML, Configure Restricted HTML, Configure Full HTML, Configure Plain text
```

## Outcome

`VERIFIED`

The patch now passes the standard evaluator in the repaired local runtime, and the independent manual axe check confirms the accessible-name contract before and after patching. Optional voice-control smoke testing would strengthen an upstream filing, but the local patch evaluation is no longer blocked by the axe rule ID mismatch.
