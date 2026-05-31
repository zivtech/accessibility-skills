# Drupal Accessibility Patch Evaluation Packet: DRUPAL-A11Y-003 Select-All Checkbox Label

> Status: VERIFIED
> Prepared: 2026-05-28
> Purpose: Local evaluator packet for Mike Gifford's current `a11y-DRUPAL-A11Y-003-select-all-checkbox-label` patch.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-DRUPAL-A11Y-003-select-all-checkbox-label` |
| Status | `VERIFIED` |
| Project/package | `mgifford/drupal-core` |
| Target commit checked | `9ec853aac0cd55c6ed574343440b5d31e75ce81c` (`origin/main` on 2026-05-31) |
| Local runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| Evaluation artifact | `docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-003-select-all-checkbox-label-evaluation-codex-select-all-aria-label-003.{md,json,html}` |
| Patch artifact | `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-003-select-all-checkbox-label-codex-select-all-aria-label.patch` |
| Upstream handoff | `docs/drupal-patch-evaluations/reports/current-wave/2026-05-31-003-select-all-checkbox-upstream-handoff.md` |
| Upstream PR | https://github.com/mgifford/drupal-core/pull/13 |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Issue Summary

| Field | Value |
|---|---|
| Rule/source | `axe-core label-title-only` |
| WCAG SC | `1.3.1 Info and Relationships (A)` in upstream artifacts |
| Routes | `/admin/content`, `/admin/people`; deterministic fixture route `/table` |
| Selector | `input[title="Select all rows in this table"]` |
| Pattern ID | `DRU-987EB788` |
| Runtime state | DDEV project `drupal-core`, Drupal 12.0-dev, admin/admin, fixture modules enabled |

## Local Evaluator Result

Command:

```bash
cd /Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
DRUPAL_BASE_URL=http://drupal-core.ddev.site \
  A11Y_VARIANT_ID=codex-select-all-aria-label-003 \
  node core/tests/playwright/scripts/evaluate-patch.js \
  a11y-DRUPAL-A11Y-003-select-all-checkbox-label
```

Result:

```text
Status: PASS
Outcome reason: targeted-issues-fixed-without-regressions
Case generation mode: pattern-report-derived
Baseline observed instances: 1
Fixed instances after patch: 1
Remaining instances after patch: 0
Introduced new violations: 0
```

The rerolled patch applied and reverted cleanly. The `/admin/content` case observed the `label-title-only` baseline before patch application and did not observe it after patch application under the same route and conditions. The `/admin/people` case loaded successfully but was skipped because the target baseline violation was not observed in this runtime.

## Patch-Target Finding

The original local failure was real: targeting only the Default Admin Twig template did not fix the active Claro/core `tableSelect` render path. The deterministic `/table` fixture and the authenticated `/admin/content` route both showed that the select-all checkbox can be inserted by JavaScript from `core/misc/tableselect.js`.

The reroll replaces the title-only label source with `aria-label` in:

```text
core/misc/tableselect.js
core/themes/default_admin/migration/js/tableselect.js
core/themes/default_admin/templates/dataset/table.html.twig
core/themes/default_admin/templates/views/views-view-table.html.twig
```

It also updates the FunctionalJavascript coverage in:

```text
core/modules/system/tests/src/FunctionalJavascript/Form/ElementsTableSelectTest.php
```

The first reroll added `aria-label` while leaving the same text in `title`. A Chrome accessibility-tree probe exposed that as duplicate name/description output, so the final patch removes the `title` attribute and keeps the accessible name on `aria-label`.

## Additional Validation

Code checks:

```bash
node --check core/misc/tableselect.js
node --check core/themes/default_admin/migration/js/tableselect.js
php -l core/modules/system/tests/src/FunctionalJavascript/Form/ElementsTableSelectTest.php
git diff --check
ddev exec vendor/bin/phpcs --standard=core/phpcs.xml.dist core/misc/tableselect.js core/themes/default_admin/migration/js/tableselect.js core/modules/system/tests/src/FunctionalJavascript/Form/ElementsTableSelectTest.php core/themes/default_admin/templates/dataset/table.html.twig core/themes/default_admin/templates/views/views-view-table.html.twig
```

FunctionalJavascript test:

```bash
ddev exec env SIMPLETEST_BASE_URL=http://web SIMPLETEST_DB=[REDACTED_DB_DSN] BROWSERTEST_OUTPUT_DIRECTORY=/var/www/html/sites/simpletest/browser_output MINK_DRIVER_ARGS_WEBDRIVER='["chrome", {"browserName":"chrome", "goog:chromeOptions":{"args":["--headless=new", "--no-sandbox", "--disable-dev-shm-usage"]}}, "http://drupal-core-selenium-003:4444"]' vendor/bin/phpunit -c core core/modules/system/tests/src/FunctionalJavascript/Form/ElementsTableSelectTest.php
```

Result:

```text
OK (2 tests, 23 assertions)
```

Manual browser checks on `/table`:

```text
Rendered checkbox: aria-label present, title absent
axe label-title-only violations: 0
Keyboard Space activation: checked false -> true
Accessible name: "Select all rows in this table" -> "Deselect all rows in this table"
Accessible description: empty before and after
```

Live PR state checked 2026-05-31:

```text
PR: https://github.com/mgifford/drupal-core/pull/13
State: open, not draft
Merge state: CLEAN
Checks: AccessLint SUCCESS
Comments/reviews: none
```

## Gates

- [x] Baseline target observed before patch.
- [x] Patch applied and reverted.
- [x] Same route and state tested after patch.
- [x] Target rule absent after patch.
- [x] No new violations introduced.
- [x] Deterministic `/table` fixture rerun completed.
- [x] Manual keyboard and accessibility-tree name smoke check completed.

## Outcome

`VERIFIED`

The issue is reproducible and the rerolled patch fixes the targeted title-only select-all checkbox label without introducing new evaluator violations. The fix deliberately removes the `title` attribute rather than duplicating the accessible name in both `aria-label` and `title`.

Next action: track Mike review on PR #13 and keep scope limited to the select-all checkbox accessible name unless review asks for broader table-select behavior.
