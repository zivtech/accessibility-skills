# Drupal Accessibility Patch Evaluation Packet: DRUPAL-A11Y-004 Tabindex Buttons Test Form

> Status: VERIFIED
> Prepared: 2026-05-28
> Purpose: Local evaluator packet for Mike Gifford's current `a11y-DRUPAL-A11Y-004-tabindex-buttons-test-form` patch.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-DRUPAL-A11Y-004-tabindex-buttons-test-form` |
| Status | `VERIFIED` |
| Project/package | `mgifford/drupal-core` |
| Target commit checked | `9ec853aac0cd55c6ed574343440b5d31e75ce81c` (`origin/main` on 2026-05-31) |
| Local runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| Evaluation artifact | `docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-004-tabindex-buttons-test-form-evaluation-codex-remove-positive-tabindex-004.{md,json,html}` |
| Patch artifact | `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-004-tabindex-buttons-test-form-codex-remove-positive-tabindex.patch` |
| Upstream handoff | `docs/drupal-patch-evaluations/reports/current-wave/2026-05-31-004-tabindex-buttons-upstream-handoff.md` |
| Upstream PR | https://github.com/mgifford/drupal-core/pull/12 |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Issue Summary

| Field | Value |
|---|---|
| Rule/source | `axe-core tabindex` |
| WCAG SC | `2.1.1 Keyboard (A)` in upstream artifacts |
| Route | `/buttons` |
| Selector(s) | `#edit-submit`, `#edit-danger--N`; rendered controls are `input[tabindex="1"]` |
| Pattern ID | `DRU-CC36FB25` |
| Fixture | `theming_tools:button`, `ButtonTestForm` |
| Runtime state | DDEV project `drupal-core`, Drupal 12.0-dev, admin/admin, fixture modules enabled |

## Local Evaluator Result

Command:

```bash
cd /Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
DRUPAL_BASE_URL=http://drupal-core.ddev.site \
  A11Y_VARIANT_ID=codex-remove-positive-tabindex-004 \
  node core/tests/playwright/scripts/evaluate-patch.js \
  a11y-DRUPAL-A11Y-004-tabindex-buttons-test-form
```

Result:

```text
Status: PASS
Outcome reason: targeted-issues-fixed-without-regressions
Case generation mode: pattern-report-derived
Baseline observed instances: 2
Fixed instances after patch: 2
Remaining instances after patch: 0
Introduced new violations: 0
```

The rerolled patch applied and reverted cleanly. Target `tabindex` violations were observed before patch application and absent after patch application under the same `/buttons` route and conditions.

## Patch-Target Finding

The current patch modifies:

```text
core/modules/system/tests/modules/form_test/src/Form/FormTestClickedButtonForm.php
```

The failing runtime fixture is:

```text
modules/contrib/theming_tools/modules/button/src/Form/ButtonTestForm.php
```

The rendered `/buttons` baseline includes multiple submit inputs with `tabindex="1"`, including `#edit-submit`, `#edit-danger`, `#edit-cancel`, and their small-button variants. The current patch does not touch that source, so the local `FAILED` outcome is expected.

Additional config/design notes:

- The evaluator config selector `button[tabindex]` is too narrow for the live fixture because the failing controls render as `input[type="submit"][tabindex]`.
- The patch adds `tabindex => -1` in a test form. That would remove controls from normal tab order and is not an appropriate keyboard-accessibility fix for actual submit buttons. The likely repair is to remove the explicit positive tabindex from the real `ButtonTestForm` fixture, then verify the natural DOM order.

## Reroll Finding

The reroll removes the explicit positive `tabindex` values from the real `ButtonTestForm` fixture and keeps the native submit/button/link controls in DOM order. It also adds a functional regression test asserting that `/buttons` and `/buttons/disabled` do not render explicit `tabindex` attributes inside `#button-test-form`.

Additional validation:

- `ddev exec vendor/bin/phpcs --standard=core/phpcs.xml.dist modules/contrib/theming_tools/modules/button/src/Form/ButtonTestForm.php modules/contrib/theming_tools/tests/src/Functional/ButtonTestFormTest.php`
- `ddev exec env SIMPLETEST_BASE_URL=http://drupal-core.ddev.site SIMPLETEST_DB=mysql://db:db@db/db BROWSERTEST_OUTPUT_DIRECTORY=/var/www/html/sites/simpletest/browser_output vendor/bin/phpunit -c core modules/contrib/theming_tools/tests/src/Functional/ButtonTestFormTest.php` passed with 1 test and 9 assertions.
- Manual Playwright/axe check found zero explicit `tabindex` attributes and zero axe `tabindex` violations on `/buttons` and `/buttons/disabled`.
- Real Playwright `Tab` presses reached the `/buttons` controls in document order with no explicit `tabindex` on the focused controls.

## Gates

- [x] Baseline target observed before patch.
- [x] Patch applied and reverted.
- [x] Same route and state tested after patch.
- [x] Target rule absent after patch.
- [x] No new violations introduced.
- [x] Manual keyboard check completed.

## Outcome

`VERIFIED`

The issue is reproducible and the rerolled patch fixes the targeted `tabindex` violations on the route used by the evaluator without introducing new violations. Upstream PR #12 is open, mergeable cleanly, and AccessLint passing as of 2026-05-31. Next action: track Mike review and keep the claim limited to the theming tools button fixture.
