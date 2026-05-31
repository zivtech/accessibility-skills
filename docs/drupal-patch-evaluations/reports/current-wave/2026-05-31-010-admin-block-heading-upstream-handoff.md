# Upstream Handoff: DRUPAL-A11Y-010 Admin Block Heading Order

> Date: 2026-05-31
> Upstream PR: https://github.com/mgifford/drupal-core/pull/15
> Branch: `AlexU-A:codex/admin-block-heading-order-20260531`

## What Changed

The split-out admin block heading-order family now has a scoped patch. It changes active `admin_block` panel titles from `h3.panel__title` to `h2.panel__title` in the core system template and the Default Admin override.

Commit:

```text
1bb53b07e2 fix: correct admin block panel heading level
```

Patch artifact:

```text
docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-010-admin-block-heading-order-codex-admin-block-heading-level.patch
```

Packet:

```text
docs/drupal-patch-evaluations/2026-05-31-a11y-DRUPAL-A11Y-010-admin-block-heading-order.md
```

## Validation

```text
git diff --check: pass
php -l core/modules/system/tests/src/Functional/System/AdminTest.php: pass
php -l core/themes/default_admin/tests/src/Functional/AdminTest.php: pass
ddev exec vendor/bin/phpcs --standard=core/phpcs.xml.dist core/modules/system/tests/src/Functional/System/AdminTest.php core/themes/default_admin/tests/src/Functional/AdminTest.php: pass
ddev exec env SIMPLETEST_BASE_URL=http://web SIMPLETEST_DB=[local DDEV DB] BROWSERTEST_OUTPUT_DIRECTORY=/var/www/html/sites/simpletest/browser_output vendor/bin/phpunit -c core --filter testConfigBlocksDescription core/modules/system/tests/src/Functional/System/AdminTest.php: OK (1 test, 13 assertions)
ddev exec env SIMPLETEST_BASE_URL=http://web SIMPLETEST_DB=[local DDEV DB] BROWSERTEST_OUTPUT_DIRECTORY=/var/www/html/sites/simpletest/browser_output vendor/bin/phpunit -c core --filter testAdminBlockHeadingLevel core/themes/default_admin/tests/src/Functional/AdminTest.php: OK (1 test, 9 assertions)
Playwright exact-route smoke on /cd-navigation/config: h2.panel__title rendered, h3.panel__title absent, axe heading-order returned no violations.
```

Live PR state checked after creation:

```text
PR #15 open, not draft, merge state CLEAN, AccessLint SUCCESS.
```

## Scope Boundary

This PR is not the pager fix from PR #10, and it should not absorb the datetime wrapper or multiple-value field heading families. Those form-label/render-contract questions need separate design review before code changes.

Stable 9 was intentionally left unchanged because it is a deprecated backwards-compatibility markup layer.

## Review Ask

- Is `h2` the right heading level for admin block panel titles under admin overview page `h1` headings?
- Should this remain separate from the existing Content view pager heading PR?
- Is leaving Stable 9 unchanged the right BC boundary for this patch?
