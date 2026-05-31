# Upstream Handoff: DRUPAL-A11Y-010 Datetime Wrapper Heading Order

> Date: 2026-05-31
> Upstream PR: https://github.com/mgifford/drupal-core/pull/17
> Patch artifact: `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-010-datetime-wrapper-heading-order-codex-datetime-wrapper-label.patch`

## Summary

I split the datetime wrapper family out of the broader `DRUPAL-A11Y-010` heading-order evidence.

The patch removes `h4` markup from datetime wrapper titles and labels the wrapper as a form control group with `role="group"` and `aria-labelledby`.

## Changed Files

```text
core/lib/Drupal/Core/Datetime/DatePreprocess.php
core/modules/system/templates/datetime-wrapper.html.twig
core/modules/system/tests/src/Functional/Form/ElementsLabelsTest.php
core/profiles/demo_umami/themes/umami/templates/classy/form/datetime-wrapper.html.twig
core/themes/claro/templates/datetime-wrapper.html.twig
core/themes/default_admin/templates/form/datetime-wrapper.html.twig
core/themes/olivero/templates/datetime-wrapper.html.twig
core/themes/stable9/templates/form/datetime-wrapper.html.twig
core/themes/starterkit_theme/templates/form/datetime-wrapper.html.twig
```

## Evidence

Historical reproduction:

```text
/admin/form_style .form-datetime-wrapper > h4
/contact/textform #edit-timestamp-wrapper .form-datetime-wrapper > h4
```

After patch:

```text
/admin/form_style
- status 200
- 2 datetime wrappers
- Datelist and Datetime labels rendered as divs referenced by aria-labelledby
- wrapper h4 count 0
- axe heading-order 0

/contact/textform
- status 200
- 14 datetime wrappers
- titled wrappers rendered with role group and aria-labelledby
- wrapper h4 count 0
- axe heading-order 0
```

## Validation

```text
git diff --check: pass
php -l core/lib/Drupal/Core/Datetime/DatePreprocess.php: pass
php -l core/modules/system/tests/src/Functional/Form/ElementsLabelsTest.php: pass
PHPCS on changed PHP and Twig files: pass
ElementsLabelsTest::testFormElements: OK (1 test, 80 assertions)
Playwright exact-route smoke on /admin/form_style and /contact/textform: pass
AccessLint on PR #17: SUCCESS
```

## Review Ask

The main design question is whether this should stay a narrow ARIA grouping patch or become a broader native `fieldset` and `legend` conversion.

I chose the narrow version because it removes the false heading role and preserves a programmatic group label without changing fieldset layout in every theme override.

## Negative Space

This does not claim human screen reader verification. It also does not claim that native `fieldset` semantics would be wrong in a broader redesign.
