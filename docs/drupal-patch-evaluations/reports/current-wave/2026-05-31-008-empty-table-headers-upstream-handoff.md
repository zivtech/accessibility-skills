# Upstream Handoff: DRUPAL-A11Y-008 Empty Table Headers

> Date: 2026-05-31
> Upstream PR: https://github.com/mgifford/drupal-core/pull/18
> Patch artifact: `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-008-empty-table-headers-codex-field-operations-header.patch`

## Summary

I repaired the blocked `/autocomplete` fixture path by enabling the theming tools `autocomplete` module in the disposable runtime, then rerolled the patch boundary.

The earlier broad candidate labelled every empty table header from `table.html.twig` as `Column`. I did not upstream that version. The PR instead labels the specific multiple-value field operations column at its render source with visually hidden `Operations` text.

## Changed Files

```text
core/lib/Drupal/Core/Field/FieldPreprocess.php
core/modules/field/tests/src/Functional/FormTest.php
```

## Evidence

Before patch on `/autocomplete`:

```text
Header 1: Select some other countries
Header 2: [empty]
Header 3: Order
empty-table-header: 1
```

After patch:

```text
Header 1: Select some other countries
Header 2: Operations (visually hidden)
Header 3: Order
empty-table-header: 0
```

## Validation

```text
git diff --check: pass
php -l core/lib/Drupal/Core/Field/FieldPreprocess.php: pass
php -l core/modules/field/tests/src/Functional/FormTest.php: pass
PHPCS on changed PHP files: pass
FormTest filtered run: OK (2 tests, 36 assertions)
Evaluator on /autocomplete: PASS, empty-table-header 1 -> 0, no new violations
AccessLint on PR #18: SUCCESS
```

## Review Ask

Is `Operations` the right hidden header for the field multiple value action column, or should the column be named more narrowly as remove/reorder-related UI?

## Negative Space

This does not claim that every empty table header in Drupal core is fixed. It also does not claim human screen reader verification; this is rendered DOM, axe, functional test, and AccessLint evidence.
