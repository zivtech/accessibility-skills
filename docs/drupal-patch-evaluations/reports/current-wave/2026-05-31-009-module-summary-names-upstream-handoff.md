# DRUPAL-A11Y-009 Module Summary Names Upstream Handoff

## Status

`VERIFIED` and upstreamed.

- PR: https://github.com/mgifford/drupal-core/pull/19
- Branch: `AlexU-A:codex/module-summary-names-20260531`
- Commit: `01ffe16648 fix: label empty module summaries`
- PR state checked: open, not draft, merge state `CLEAN`, AccessLint passing on 2026-05-31

## What Changed

The old packet was blocked because `/admin/modules` did not expose the Nyan Cat core test module row. That blocker was repaired in the runtime by enabling test-extension discovery. After that, the evaluator reproduced the `summary-name` violation on:

```text
#edit-modules-nyan-cat-enable-description > .module-list__module-summary
```

The upstream patch adds a narrow fallback:

- `SystemAdminThemePreprocess::preprocessSystemModulesDetails()` derives `module.summary_label` only when the rendered module description is empty plain text.
- Core, Claro, Default Admin, and Stable 9 module-list templates add an `aria-label` only when that fallback exists.
- Existing visible description summaries keep their current accessible name.
- The existing empty-description module-list functional test now covers both the empty and non-empty cases.

## Validation

```text
git diff --check: pass
php -l changed PHP files: pass
Drupal PHPCS on changed PHP/Twig/test files: pass
Evaluator: PASS, summary-name 1 -> 0, no new violations
Focused functional test: OK (1 test, 10 assertions)
Full ModulesListFormWebTest.php: OK (6 tests, 68 assertions)
```

Live DOM smoke after applying the candidate:

```json
{
  "nyanExists": true,
  "nyanText": "",
  "nyanAriaLabel": "Details for Nyan cat",
  "nonEmptyAriaLabel": null,
  "emptySummaryCount": 0
}
```

## Files

- Packet: `docs/drupal-patch-evaluations/2026-05-28-a11y-DRUPAL-A11Y-009-module-summary-names.md`
- Patch artifact: `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-009-module-summary-names-codex-summary-label-fallback.patch`
- Sanitized evaluator summary: `docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-009-module-summary-names-evaluation-codex-summary-label-fallback-009.md`

## Boundaries

This is not an AT smoke result. It is axe/DOM/functional-test evidence for the accessible-name failure. The patch also does not decide whether empty details disclosures should be removed from the module listing; it only ensures the existing disclosure has a discernible accessible name.

## Next Action

Track Mike's review on PR #19. Keep the scope limited to empty module-description details summaries unless review asks for a broader module-list rendering or UX change.
