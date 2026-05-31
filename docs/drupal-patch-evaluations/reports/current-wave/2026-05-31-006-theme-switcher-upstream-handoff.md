# Upstream Handoff: DRUPAL-A11Y-006 Theme Switcher Landmark

> Date: 2026-05-31
> Runtime: `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime`
> PR worktree: `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-pr-006-theme-switcher-landmark-20260531`
> Branch: `codex/theme-switcher-form-landmark-20260531`
> Upstream PR: https://github.com/mgifford/drupal-core/pull/14

## Summary

The previous patch wrapped a broad Default Admin form layout in a `nav` landmark, which did not fix the real `.themeswitcher-form__form-item` target and overstated the control as navigation.

The reroll names the actual theme switcher form wrapper with `aria-label="Theme switcher"`, exposing it as a native named form landmark. It also adds functional coverage for the rendered form and select control.

Live PR state checked 2026-05-31:

```text
State: open, not draft
Merge state: CLEAN
Checks: AccessLint SUCCESS
Comments/reviews: none
```

Patch artifact:

```text
docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-006-theme-switcher-landmark-codex-form-landmark-006.patch
```

Evaluation artifact:

```text
docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-006-theme-switcher-landmark-evaluation-codex-form-landmark-006.md
```

## Validation

Code checks:

```bash
php -l modules/contrib/theming_tools/modules/themeswitcher/src/Form/ThemeSwitcherForm.php
php -l modules/contrib/theming_tools/modules/themeswitcher/tests/src/Functional/ThemeSwitcherFormTest.php
git diff --check
ddev exec vendor/bin/phpcs --standard=core/phpcs.xml.dist modules/contrib/theming_tools/modules/themeswitcher/src/Form/ThemeSwitcherForm.php modules/contrib/theming_tools/modules/themeswitcher/tests/src/Functional/ThemeSwitcherFormTest.php
```

Functional test:

```bash
ddev exec env SIMPLETEST_BASE_URL=http://web SIMPLETEST_DB=[local test DB DSN] BROWSERTEST_OUTPUT_DIRECTORY=/var/www/html/sites/simpletest/browser_output vendor/bin/phpunit -c core modules/contrib/theming_tools/modules/themeswitcher/tests/src/Functional/ThemeSwitcherFormTest.php
```

Result:

```text
OK (1 test, 7 assertions)
```

Focused axe scan after patch:

```text
themeSwitcherRegion=0 and aria-label=Theme switcher on /, /admin, /admin/appearance, /admin/config, /admin/config/content/formats, /admin/config/content/formats/manage/restricted_html, /admin/config/system/site-information, and /admin/content.
```

Evaluator:

```text
Baseline observed instances: 3
Fixed instances after patch: 3
Remaining instances after patch: 0
Overall evaluator status: FAIL, because /admin/config exposed a non-patch-owned heading-order finding after status-message state changed.
```

## Critic Gate

The named native form is the defensible semantic choice. The control changes a preference and submits a form; it is not navigation, so wrapping it in `nav` would be fluent but wrong.

The evaluator's overall FAIL should not be smoothed away. It is useful evidence that the runtime still has page-state noise and unrelated heading-order debt. It is not evidence that this patch introduced heading-order markup.

## Non-Claims

This does not claim a full landmark audit of the page-bottom region or all Theming Tools routes.

This does not claim human AT verification. Evidence is axe, rendered DOM, functional test coverage, and GitHub AccessLint.

This does not address the unrelated `heading-order`, `landmark-contentinfo-is-top-level`, `landmark-no-duplicate-contentinfo`, `color-contrast`, or `label-title-only` findings still visible elsewhere.

## Review Ask

- Is a named native form landmark the right semantic treatment for the fixed theme switcher preference control?
- Should the evaluator metadata be corrected separately so the issue is no longer described as a `nav` wrapper?
