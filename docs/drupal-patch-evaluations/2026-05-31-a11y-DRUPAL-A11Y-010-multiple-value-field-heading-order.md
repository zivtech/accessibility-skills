# Drupal Accessibility Patch Evaluation Packet: DRUPAL-A11Y-010 Multiple-Value Field Heading Order

> Status: VERIFIED
> Date: 2026-05-31
> Scope: Split-out multiple-value field label family from `DRUPAL-A11Y-010-heading-order`.

## Summary

The original `DRUPAL-A11Y-010` investigation found several unrelated `heading-order` families. The pager family is PR #10, and the admin block family is PR #15. This packet covers only the multiple-value field label family reproduced on:

- `/contact/field_cardinality_test`
- `/contact/presuf_formatted`
- `/contact/presuf_number`

The fix keeps the label text inside the existing table header cell, but removes the heading element wrapper. It changes the multiple-value field label render element from `h4` to `span` in:

- `core/lib/Drupal/Core/Field/FieldPreprocess.php`
- `core/themes/olivero/src/Hook/OliveroHooks.php`

It also updates the Claro and Default Admin compatibility selectors so fallback `.label` styling still applies to the non-heading label markup.

## Patch

```text
docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-010-multiple-value-field-heading-order-codex-multiple-value-field-label.patch
```

Upstream PR:

```text
https://github.com/mgifford/drupal-core/pull/16
```

Branch:

```text
AlexU-A:codex/multiple-value-field-heading-order-20260531
```

Commit:

```text
e91fbb643f fix: remove heading markup from multiple value field labels
```

## Evidence

Before patch, route-family reproduction recorded multiple-value field labels rendered as headings, for example:

```html
<h4 class="form-item__label form-item__label--multiple-value-form">Multiple, unlimited text</h4>
```

After patch, an exact-route Playwright smoke observed:

```text
/contact/field_cardinality_test: labelTag span, headingCount 0, axe heading-order 0
/contact/presuf_formatted: labelTag span, headingCount 0, axe heading-order 0
/contact/presuf_number: labelTag span, headingCount 0, axe heading-order 0
```

The label remains the text content of the existing table header cell. The patch does not remove the field label, table header, or required-marker styling classes.

## Validation

```text
git diff --check
php -l core/lib/Drupal/Core/Field/FieldPreprocess.php
php -l core/modules/field/tests/src/Functional/MultipleWidgetFormTest.php
php -l core/themes/olivero/src/Hook/OliveroHooks.php
php -l core/themes/olivero/tests/src/Unit/OliveroFieldMultipleValueFormTest.php
vendor/bin/phpcs --standard=core/phpcs.xml.dist core/lib/Drupal/Core/Field/FieldPreprocess.php core/modules/field/tests/src/Functional/MultipleWidgetFormTest.php core/themes/olivero/src/Hook/OliveroHooks.php core/themes/olivero/tests/src/Unit/OliveroFieldMultipleValueFormTest.php
vendor/bin/phpunit -c core/phpunit.xml.dist core/themes/olivero/tests/src/Unit/OliveroFieldMultipleValueFormTest.php
ddev exec env SIMPLETEST_BASE_URL=http://drupal-core.ddev.site SIMPLETEST_DB=[local DDEV DB] BROWSERTEST_OUTPUT_DIRECTORY=/tmp vendor/bin/phpunit -c core/phpunit.xml.dist --filter testLabelOnMultiValueFields core/modules/field/tests/src/Functional/MultipleWidgetFormTest.php
```

Results:

```text
Olivero unit test: OK (1 test, 4 assertions)
Field MultipleWidgetFormTest focused functional: OK (1 test, 16 assertions)
Playwright exact-route smoke on all three reproduced multiple-value routes: span labels rendered, table header heading count 0, axe heading-order 0.
AccessLint on PR #16: SUCCESS
```

## Negative Space

This packet does not claim:

- that datetime wrapper heading labels are fixed;
- that the pager family from PR #10 or admin block family from PR #15 should be broadened;
- that all form table semantics have been redesigned;
- that human screen reader verification has been completed.

## Review Ask

- Is removing the redundant heading wrapper from multiple-value field table labels the right semantic boundary?
- Should the label remain in the existing table header cell, or should field table labeling be redesigned more broadly in a follow-up?
- Are the Claro, Default Admin, and Olivero styling boundaries sufficient for this narrow change?
