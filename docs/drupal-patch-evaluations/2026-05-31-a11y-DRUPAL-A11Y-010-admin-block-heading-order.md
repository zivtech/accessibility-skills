# Drupal Accessibility Patch Evaluation Packet: DRUPAL-A11Y-010 Admin Block Heading Order

> Status: VERIFIED
> Date: 2026-05-31
> Scope: Split-out admin block panel heading family from `DRUPAL-A11Y-010-heading-order`.

## Summary

The original `DRUPAL-A11Y-010` investigation found several unrelated `heading-order` families. The pager family was handled separately in PR #10. This packet covers only the admin block panel title family reproduced on `/cd-navigation/config`.

The fix changes active `admin_block` panel titles from `h3.panel__title` to `h2.panel__title` in:

- `core/modules/system/templates/admin-block.html.twig`
- `core/themes/default_admin/templates/admin/admin-block.html.twig`

The patch intentionally does not change datetime wrapper headings, multiple-value field headings, or the deprecated Stable 9 compatibility template.

## Patch

```text
docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-010-admin-block-heading-order-codex-admin-block-heading-level.patch
```

Upstream PR:

```text
https://github.com/mgifford/drupal-core/pull/15
```

Branch:

```text
AlexU-A:codex/admin-block-heading-order-20260531
```

## Evidence

Before patch, the route-family reproduction recorded `/cd-navigation/config` rendering:

```html
<h3 class="panel__title">People</h3>
```

After patch, an exact-route Playwright smoke on `/cd-navigation/config` observed:

```text
h2.panel__title:
People
Content authoring
Development
Search and metadata
Web services
System
User interface
Media
Region and language

h3.panel__title: none
axe heading-order violations: none
```

Targeted functional tests also assert the rendered heading level for the core system template and Default Admin override.

## Validation

```text
git diff --check
php -l core/modules/system/tests/src/Functional/System/AdminTest.php
php -l core/themes/default_admin/tests/src/Functional/AdminTest.php
ddev exec vendor/bin/phpcs --standard=core/phpcs.xml.dist core/modules/system/tests/src/Functional/System/AdminTest.php core/themes/default_admin/tests/src/Functional/AdminTest.php
ddev exec env SIMPLETEST_BASE_URL=http://web SIMPLETEST_DB=[local DDEV DB] BROWSERTEST_OUTPUT_DIRECTORY=/var/www/html/sites/simpletest/browser_output vendor/bin/phpunit -c core --filter testConfigBlocksDescription core/modules/system/tests/src/Functional/System/AdminTest.php
ddev exec env SIMPLETEST_BASE_URL=http://web SIMPLETEST_DB=[local DDEV DB] BROWSERTEST_OUTPUT_DIRECTORY=/var/www/html/sites/simpletest/browser_output vendor/bin/phpunit -c core --filter testAdminBlockHeadingLevel core/themes/default_admin/tests/src/Functional/AdminTest.php
```

Results:

```text
System AdminTest: OK (1 test, 13 assertions)
Default Admin AdminTest: OK (1 test, 9 assertions)
AccessLint on PR #15: SUCCESS
```

## Negative Space

This packet does not claim:

- that all `DRUPAL-A11Y-010` heading-order families are fixed;
- that datetime wrapper labels or multiple-value field labels should become `h2`;
- that Stable 9 markup should change despite its backwards-compatibility role;
- that the existing pager PR #10 should be broadened.
