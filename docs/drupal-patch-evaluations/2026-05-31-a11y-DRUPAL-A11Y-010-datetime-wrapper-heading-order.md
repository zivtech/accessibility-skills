# Drupal Accessibility Patch Evaluation Packet: DRUPAL-A11Y-010 Datetime Wrapper Heading Order

> Status: VERIFIED
> Date: 2026-05-31
> Scope: Split-out datetime wrapper label family from `DRUPAL-A11Y-010-heading-order`.

## Summary

The original `DRUPAL-A11Y-010` investigation found several unrelated `heading-order` families. The pager family is PR #10, the admin block family is PR #15, and the multiple-value field family is PR #16.

This packet covers only the datetime wrapper label family reproduced on:

- `/admin/form_style`
- `/contact/textform`

The fix removes `h4` heading markup from titled datetime wrappers and preserves a programmatic group label with:

```text
role="group"
aria-labelledby="[datetime-element-id]--label"
```

It updates the system template and the Claro, Default Admin, Olivero, Stable 9, Starterkit, and Umami overrides.

## Patch

```text
docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-010-datetime-wrapper-heading-order-codex-datetime-wrapper-label.patch
```

Upstream PR:

```text
https://github.com/mgifford/drupal-core/pull/17
```

Branch:

```text
AlexU-A:codex/datetime-wrapper-heading-order-20260531
```

Commit:

```text
60c2bb3b8d fix: remove heading markup from datetime wrapper labels
```

## Evidence

Before patch, route-family reproduction recorded datetime wrapper labels rendered as headings:

```html
<h4 class="form-item__label">Datelist</h4>
<h4 class="form-item__label">Timestamp</h4>
```

After patch, a Playwright route smoke observed:

```text
/admin/form_style: 2 datetime wrappers, role group labels for Datelist and Datetime, wrapper h4 count 0, axe heading-order 0
/contact/textform: 14 datetime wrappers, titled wrappers labelled with role group, wrapper h4 count 0, axe heading-order 0
```

The two untitled wrappers on `/contact/textform` remained unlabelled groups because they did not have wrapper titles to expose. They also rendered no `h4`.

## Validation

```text
git diff --check
php -l core/lib/Drupal/Core/Datetime/DatePreprocess.php
php -l core/modules/system/tests/src/Functional/Form/ElementsLabelsTest.php
vendor/bin/phpcs --standard=core/phpcs.xml.dist [changed PHP and Twig files]
ddev exec env SIMPLETEST_BASE_URL=http://drupal-core.ddev.site SIMPLETEST_DB=[local DDEV DB] BROWSERTEST_OUTPUT_DIRECTORY=/tmp vendor/bin/phpunit -c core/phpunit.xml.dist --filter testFormElements core/modules/system/tests/src/Functional/Form/ElementsLabelsTest.php
Playwright exact-route smoke on /admin/form_style and /contact/textform
AccessLint on PR #17
```

Results:

```text
git diff --check: pass
PHP syntax checks: pass
PHPCS: pass
ElementsLabelsTest::testFormElements: OK (1 test, 80 assertions)
Playwright exact-route smoke: datetime wrapper h4 count 0 and axe heading-order 0 on both reproduced routes
AccessLint on PR #17: SUCCESS
```

## Design Boundary

This patch uses `role="group"` and `aria-labelledby`, not native `fieldset` and `legend`.

That is the intentional narrow boundary: it removes the false heading semantics and gives assistive technology a programmatic group label without changing each theme's fieldset layout, wrappers, and visual treatment. A reviewer may still prefer a broader native-fieldset change. That question is named in the upstream review ask.

## Negative Space

This packet does not claim:

- that human screen reader verification has been completed;
- that all form group semantics in Drupal core have been redesigned;
- that `fieldset` and `legend` would be wrong for a broader follow-up;
- that unrelated `heading-order` findings outside this datetime wrapper family are fixed.

## Review Ask

- Is `role="group"` plus `aria-labelledby` the right narrow semantic boundary for datetime wrapper labels?
- Should this issue instead move all titled datetime wrappers to native `fieldset` and `legend`, accepting the larger theme/layout blast radius?
- Are the theme override changes complete for the datetime wrapper render path?
