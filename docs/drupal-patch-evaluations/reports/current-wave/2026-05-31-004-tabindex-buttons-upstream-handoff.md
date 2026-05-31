# Upstream Handoff: DRUPAL-A11Y-004 Tabindex Buttons Test Form

> Date: 2026-05-31
> Runtime: `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime`
> PR worktree: `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-pr-004-tabindex-buttons-20260531`
> Branch: `codex/tabindex-buttons-test-form-20260531`
> Upstream PR: https://github.com/mgifford/drupal-core/pull/12

## Summary

The original patch targeted `FormTestClickedButtonForm` and added `tabindex => -1`, but the observed `/buttons` failure comes from `modules/contrib/theming_tools/modules/button/src/Form/ButtonTestForm.php`, where native submit/button controls rendered with `tabindex="1"`.

The reroll removes the explicit positive `tabindex` attributes from the real fixture source so the controls use native DOM tab order. It also adds a functional regression test for `/buttons` and `/buttons/disabled`.

Live PR state checked 2026-05-31:

```text
State: open, not draft
Merge state: CLEAN
Checks: AccessLint SUCCESS
Comments/reviews: none
```

Patch artifact:

```text
docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-004-tabindex-buttons-test-form-codex-remove-positive-tabindex.patch
```

Evaluation artifact:

```text
docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-004-tabindex-buttons-test-form-evaluation-codex-remove-positive-tabindex-004.md
```

## Validation

Evaluator:

```bash
cd /Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
DRUPAL_BASE_URL=http://drupal-core.ddev.site \
  A11Y_VARIANT_ID=codex-remove-positive-tabindex-004 \
  node core/tests/playwright/scripts/evaluate-patch.js \
  a11y-DRUPAL-A11Y-004-tabindex-buttons-test-form
```

Result:

```text
PASS
Outcome reason: targeted-issues-fixed-without-regressions
Baseline observed instances: 2
Fixed instances after patch: 2
Remaining instances after patch: 0
Introduced new violations: 0
```

Code checks:

```bash
php -l modules/contrib/theming_tools/modules/button/src/Form/ButtonTestForm.php
php -l modules/contrib/theming_tools/tests/src/Functional/ButtonTestFormTest.php
git diff --check
ddev exec vendor/bin/phpcs --standard=core/phpcs.xml.dist modules/contrib/theming_tools/modules/button/src/Form/ButtonTestForm.php modules/contrib/theming_tools/tests/src/Functional/ButtonTestFormTest.php
ddev exec env SIMPLETEST_BASE_URL=http://drupal-core.ddev.site SIMPLETEST_DB=mysql://db:db@db/db BROWSERTEST_OUTPUT_DIRECTORY=/var/www/html/sites/simpletest/browser_output vendor/bin/phpunit -c core modules/contrib/theming_tools/tests/src/Functional/ButtonTestFormTest.php
```

Functional test result:

```text
OK (1 test, 9 assertions)
```

Manual browser check:

```text
/buttons: explicit tabindex count 0; axe tabindex violation count 0
/buttons/disabled: explicit tabindex count 0; axe tabindex violation count 0
```

Real `Tab` presses on `/buttons` reached these fixture controls in order, with no explicit `tabindex` on the focused elements:

```text
edit-submit -> edit-danger -> edit-cancel -> edit-submit--3 -> edit-delete -> edit-cancel--3 -> edit-submit--2 -> edit-danger--2
```

## Critic Gate

This is the right target because the failing page is `ButtonTestForm`, not `FormTestClickedButtonForm`. Removing positive `tabindex` preserves native keyboard reachability; replacing it with `-1` would hide active controls from normal Tab navigation.

The regression test is intentionally markup-level. The measured keyboard evidence lives in this handoff and the evaluator/browser artifacts rather than in a JavaScript test, because the code change is a fixture markup correction and the existing evaluation lane already exercises the live route with Playwright.

## Non-Claims

This does not claim a global Drupal button-system audit.

This does not claim screen-reader, switch-control, or voice-control verification. The evidence is axe `tabindex`, native markup, functional route rendering, and real keyboard Tab order.

This does not address the two remaining `region` violations reported on `/buttons`; they pre-existed and remain outside this scoped `tabindex` patch.

## Review Ask

- Is removing the explicit positive `tabindex` from the theming tools button fixture acceptable, or was it originally intended to demonstrate an anti-pattern?
- Is the functional test scope sufficient, given that the evaluator and manual Playwright check provide the real keyboard evidence?
- Should the remaining `/buttons` `region` violations stay as a separate fixture/layout issue?
