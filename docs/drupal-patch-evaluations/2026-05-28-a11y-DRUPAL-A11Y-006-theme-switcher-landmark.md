# Drupal Accessibility Patch Evaluation Packet: DRUPAL-A11Y-006 Theme Switcher Landmark

> Status: VERIFIED with evaluator caveat
> Prepared: 2026-05-28
> Rerolled: 2026-05-31
> Purpose: Local evaluator packet for Mike Gifford's current `a11y-DRUPAL-A11Y-006-theme-switcher-landmark` patch.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-DRUPAL-A11Y-006-theme-switcher-landmark` |
| Status | `VERIFIED` |
| Project/package | `mgifford/drupal-core` |
| Upstream PR | https://github.com/mgifford/drupal-core/pull/14 |
| PR branch | `AlexU-A:codex/theme-switcher-form-landmark-20260531` |
| Local runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| PR worktree | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-pr-006-theme-switcher-landmark-20260531` |
| Patch artifact | `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-006-theme-switcher-landmark-codex-form-landmark-006.patch` |
| Evaluation artifact | `docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-006-theme-switcher-landmark-evaluation-codex-form-landmark-006.md` |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Summary

The original patch wrapped Default Admin's broad `form-two-columns.html.twig` layout in a `nav` landmark. That was the wrong render path and the wrong semantic claim: the theme switcher is a fixed user-preference form, not navigation. It also left the target `.themeswitcher-form__form-item` `region` finding unchanged.

The reroll targets the actual source, `modules/contrib/theming_tools/modules/themeswitcher/src/Form/ThemeSwitcherForm.php`, and gives the native form wrapper an accessible name:

```text
form.themeswitcher-form[aria-label="Theme switcher"]
```

That exposes the control as a named form landmark without inventing navigation semantics. The patch also adds a functional regression test for the rendered form and select control.

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
/ | themeSwitcherRegion=0 | aria-label=Theme switcher
/admin | themeSwitcherRegion=0 | aria-label=Theme switcher
/admin/appearance | themeSwitcherRegion=0 | aria-label=Theme switcher
/admin/config | themeSwitcherRegion=0 | aria-label=Theme switcher
/admin/config/content/formats | themeSwitcherRegion=0 | aria-label=Theme switcher
/admin/config/content/formats/manage/restricted_html | themeSwitcherRegion=0 | aria-label=Theme switcher
/admin/config/system/site-information | themeSwitcherRegion=0 | aria-label=Theme switcher
/admin/content | themeSwitcherRegion=0 | aria-label=Theme switcher
```

GitHub AccessLint on PR #14:

```text
SUCCESS
```

## Evaluator Caveat

The patch evaluator observed and fixed the targeted instances it matched:

```text
Baseline observed instances: 3
Fixed instances after patch: 3
Remaining instances after patch: 0
```

The evaluator still returned overall `FAIL` because `/admin/config` exposed a `heading-order` finding after status-message state changed during the before/after run. This is not patch-owned: the patch only changes `ThemeSwitcherForm` markup and adds a test file. The direct focused scan above confirmed the theme switcher target has zero remaining `region` violations across the relevant routes.

## Gates

- [x] Baseline target observed before patch.
- [x] Patch applied and reverted.
- [x] Same route and state tested after patch for matched target instances.
- [x] Target rule absent after patch for matched target instances.
- [x] Focused post-patch scan across representative routes completed.
- [x] Functional regression test completed.
- [x] AccessLint passed on upstream PR.
- [x] Evaluator overall failure adjudicated as non-patch-owned state noise.

## Non-Claims

This does not claim a full landmark audit for every Theming Tools route.

This does not claim human screen-reader, switch-control, or voice-control verification. The evidence is axe, rendered DOM, functional test coverage, and GitHub AccessLint.

This does not address pre-existing `heading-order`, `landmark-contentinfo-is-top-level`, `landmark-no-duplicate-contentinfo`, `color-contrast`, or `label-title-only` findings on the scanned pages.

## Review Ask

- Is a named native form landmark the right semantic treatment for this fixed preference control?
- Should the evaluator description be updated separately from "Wrap theme switcher form in nav landmark" now that the target fix is a named form, not navigation?
