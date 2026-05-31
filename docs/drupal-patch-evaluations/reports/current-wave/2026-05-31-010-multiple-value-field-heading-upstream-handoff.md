# Upstream Handoff: DRUPAL-A11Y-010 Multiple-Value Field Heading Order

> Date: 2026-05-31
> Upstream PR: https://github.com/mgifford/drupal-core/pull/16
> Branch: `AlexU-A:codex/multiple-value-field-heading-order-20260531`

## What Changed

The split-out multiple-value field heading-order family now has a scoped patch. It keeps field labels in the existing table header cell but changes the redundant heading wrapper from `h4` to `span`.

Commit:

```text
e91fbb643f fix: remove heading markup from multiple value field labels
```

Patch artifact:

```text
docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-010-multiple-value-field-heading-order-codex-multiple-value-field-label.patch
```

Packet:

```text
docs/drupal-patch-evaluations/2026-05-31-a11y-DRUPAL-A11Y-010-multiple-value-field-heading-order.md
```

## Validation

```text
git diff --check: pass
php -l core/lib/Drupal/Core/Field/FieldPreprocess.php: pass
php -l core/modules/field/tests/src/Functional/MultipleWidgetFormTest.php: pass
php -l core/themes/olivero/src/Hook/OliveroHooks.php: pass
php -l core/themes/olivero/tests/src/Unit/OliveroFieldMultipleValueFormTest.php: pass
vendor/bin/phpcs --standard=core/phpcs.xml.dist core/lib/Drupal/Core/Field/FieldPreprocess.php core/modules/field/tests/src/Functional/MultipleWidgetFormTest.php core/themes/olivero/src/Hook/OliveroHooks.php core/themes/olivero/tests/src/Unit/OliveroFieldMultipleValueFormTest.php: pass
vendor/bin/phpunit -c core/phpunit.xml.dist core/themes/olivero/tests/src/Unit/OliveroFieldMultipleValueFormTest.php: OK (1 test, 4 assertions)
ddev exec env SIMPLETEST_BASE_URL=http://drupal-core.ddev.site SIMPLETEST_DB=[local DDEV DB] BROWSERTEST_OUTPUT_DIRECTORY=/tmp vendor/bin/phpunit -c core/phpunit.xml.dist --filter testLabelOnMultiValueFields core/modules/field/tests/src/Functional/MultipleWidgetFormTest.php: OK (1 test, 16 assertions)
Playwright exact-route smoke on /contact/field_cardinality_test, /contact/presuf_formatted, and /contact/presuf_number: span labels rendered, table header heading count 0, axe heading-order 0.
```

Live PR state checked after creation:

```text
PR #16 open, not draft, merge state CLEAN, AccessLint SUCCESS.
```

## Scope Boundary

This PR is not the pager fix from PR #10 or the admin block panel title fix from PR #15. It should not absorb datetime wrapper headings, which still need a form-group semantics decision.

This is not claiming human AT verification. The evidence is render-path tracing, functional and unit tests, and axe `heading-order` validation.

## Review Ask

- Is replacing the nested heading with non-heading text inside the existing table header cell the right semantic treatment?
- Should field table labeling stay scoped here, or does it need a broader follow-up beyond the heading-order violation?
- Are the theme styling updates broad enough for the supported active themes?
