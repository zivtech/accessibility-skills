# Drupal Accessibility Patch Evaluation Packet: DRUPAL-A11Y-004 Tabindex Buttons Test Form

> Status: FAILED
> Prepared: 2026-05-28
> Purpose: Local evaluator packet for Mike Gifford's current `a11y-DRUPAL-A11Y-004-tabindex-buttons-test-form` patch.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-DRUPAL-A11Y-004-tabindex-buttons-test-form` |
| Status | `FAILED` |
| Project/package | `mgifford/drupal-core` |
| Target commit checked | `3728741f23122018f1f26206fe563cb6c9ad49f8` (`main` on 2026-05-28) |
| Local runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| Evaluation artifact | `docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-004-tabindex-buttons-test-form-evaluation-codex-runtime-smoke-004.{md,json}` |
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
DRUPAL_BASE_URL=http://drupal-core.ddev.site:33000 \
  A11Y_VARIANT_ID=codex-runtime-smoke-004 \
  node core/tests/playwright/scripts/evaluate-patch.js \
  a11y-DRUPAL-A11Y-004-tabindex-buttons-test-form
```

Result:

```text
Status: FAIL
Outcome reason: targeted-instances-not-fixed
Case generation mode: pattern-report-derived
Baseline observed instances: 2
Fixed instances after patch: 0
Remaining instances after patch: 2
Introduced new violations: 0
```

The patch applied and reverted cleanly, but target `tabindex` violations remained unchanged on `/buttons`.

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

## Gates

- [x] Baseline target observed before patch.
- [x] Patch applied and reverted.
- [x] Same route and state tested after patch.
- [ ] Target rule absent after patch.
- [x] No new violations introduced.
- [ ] Manual keyboard check completed.

## Outcome

`FAILED`

The issue is reproducible and the patch is not effective against the route used by the evaluator. Next action: reroll the patch against `modules/contrib/theming_tools/modules/button/src/Form/ButtonTestForm.php`, remove positive `tabindex` attributes rather than replacing them with `-1`, widen the evaluator selector to include submit inputs, then rerun the same evaluator variant.
