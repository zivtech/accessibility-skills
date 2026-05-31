# Drupal Accessibility Patch Evaluation Packet: DRUPAL-A11Y-008 Empty Table Headers

> Status: VERIFIED
> Prepared: 2026-05-28
> Updated: 2026-05-31
> Purpose: Local evaluator packet for Mike Gifford's current `a11y-DRUPAL-A11Y-008-empty-table-headers` patch.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-DRUPAL-A11Y-008-empty-table-headers` |
| Status | `VERIFIED` |
| Project/package | `mgifford/drupal-core` |
| Target commit checked | `9ec853aac0` (`origin/main` on 2026-05-31) |
| Local runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| PR worktree | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-pr-empty-table-headers-20260531` |
| Patch artifact | `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-008-empty-table-headers-codex-field-operations-header.patch` |
| Evaluation artifact | `docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-008-empty-table-headers-evaluation-codex-field-operations-header-008.md` |
| Upstream PR | https://github.com/mgifford/drupal-core/pull/18 |
| AI assistance disclosed? | Yes, in PR body |

## Source Triage

The first runtime smoke on 2026-05-28 was `TEST STATE BLOCKED`: the evaluator selected `/autocomplete`, but the route returned 404 because the theming tools `autocomplete` fixture module was not enabled.

The route was repaired on 2026-05-31 by enabling the fixture:

```bash
ddev drush en autocomplete -y
ddev drush cr
```

After repair, `/autocomplete` returned 200 and rendered one empty table header in the multiple-value field widget table:

```html
<th></th>
```

The empty header comes from `Drupal\Core\Field\FieldPreprocess::preprocessFieldMultipleValueForm()`, where the operations column header was an empty array. The earlier broad candidate patched `core/modules/system/templates/table.html.twig` to label every empty `<th>` as `Column`; the upstream PR intentionally does not use that broad fallback.

## Patch

The upstream patch labels only the known multiple-value field operations column:

```text
core/lib/Drupal/Core/Field/FieldPreprocess.php
core/modules/field/tests/src/Functional/FormTest.php
```

The formerly empty header now renders as:

```html
<th><span class="visually-hidden">Operations</span></th>
```

## Validation

Commands run:

```bash
git diff --check
php -l core/lib/Drupal/Core/Field/FieldPreprocess.php
php -l core/modules/field/tests/src/Functional/FormTest.php
vendor/bin/phpcs --standard=core/phpcs.xml.dist core/lib/Drupal/Core/Field/FieldPreprocess.php core/modules/field/tests/src/Functional/FormTest.php
ddev exec env SIMPLETEST_BASE_URL=http://drupal-core.ddev.site SIMPLETEST_DB=[local DDEV DB] BROWSERTEST_OUTPUT_DIRECTORY=/tmp vendor/bin/phpunit -c core/phpunit.xml.dist --filter testFieldFormUnlimited core/modules/field/tests/src/Functional/FormTest.php
DRUPAL_BASE_URL=http://drupal-core.ddev.site A11Y_VARIANT_ID=codex-field-operations-header-008 node core/tests/playwright/scripts/evaluate-patch.js a11y-DRUPAL-A11Y-008-empty-table-headers
```

Results:

```text
git diff --check: pass
PHP syntax checks: pass
PHPCS: pass
FormTest filtered run: OK (2 tests, 36 assertions)
Evaluator: PASS
AccessLint on PR #18: SUCCESS
```

Evaluator summary:

```text
Route: /autocomplete
HTTP status: 200
Rule: empty-table-header
Axe violation count: 1 -> 0
Total violations: 3 -> 2
New violations introduced: 0
```

## Critic Gate

The meaningful design decision was scope. A generic table-template fallback would make all empty header cells announce as `Column`, even when the table source knows a better label. That would pass axe but flatten semantics.

The upstream patch stays at the field-multiple-value render source and labels the column as `Operations`, which matches Drupal table-header language for action columns and avoids changing unrelated table output.

## Negative Space

This packet does not claim:

- that all empty `<th>` cells in Drupal core are fixed;
- that raw evaluator JSON/HTML artifacts are safe to commit;
- that eight distinct empty headers were rendered in the current runtime. The evaluator reported eight targeted selector instances, but the current `/autocomplete` route rendered one empty header cell;
- that human screen reader verification has been completed.
