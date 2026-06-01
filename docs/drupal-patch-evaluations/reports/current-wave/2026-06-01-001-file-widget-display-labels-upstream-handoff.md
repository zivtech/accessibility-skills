# DRUPAL-A11Y-001 File Widget Display Labels Upstream Handoff

Date: 2026-06-01

## Status

`UPSTREAM PR OPEN`

There was one more workable queue item: `DRUPAL-A11Y-001-file-widget-display-labels`. The earlier packet was not dead, but it had flattened into an "automated pass" while still carrying two real gaps: no source pattern ID mapping and no role/name or keyboard smoke. Both gaps are now closed.

## Candidate Worktree

- Worktree: `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-pr-001-file-widget-display-labels-20260601`
- Branch: `codex/file-widget-display-labels-20260601`
- Base commit: `9ec853aac0cd55c6ed574343440b5d31e75ce81c`
- Upstream PR: https://github.com/mgifford/drupal-core/pull/21
- Patch artifact: `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-001-file-widget-display-labels-codex-invisible-label.patch`
- Patch SHA-256: `a2e5a5eddbf42e6f09b51d4e3412ac942c9e340f1de6924d2838313ce7e2ec9e`

## Patch Shape

Files changed:

- `core/modules/file/src/Hook/FileThemeHooks.php`
- `core/modules/file/tests/src/Functional/FileFieldDisplayTest.php`

The previous local patch added `aria-label` to the display checkbox render element. This candidate instead preserves the existing `#title` and changes multiple-file widget preprocessing from unsetting that title to rendering it invisibly:

```php
$widget['display']['#title_display'] = 'invisible';
```

That keeps the visible table unchanged while giving each display checkbox a native associated label.

## Evidence

Evaluator:

- Command: `DRUPAL_BASE_URL=http://drupal-core.ddev.site A11Y_VARIANT_ID=codex-invisible-label-001 node core/tests/playwright/scripts/evaluate-patch.js a11y-DRUPAL-A11Y-001-file-widget-display-labels`
- Result: `PASS`
- Outcome reason: `targeted-issues-fixed-without-regressions`
- Target source pattern: `DRU-6CA3D5EB`
- Pattern ID match type: `source-pattern-matched`
- Case generation mode: `pattern-report-derived`
- Route: `/contact/imagefile_file`
- axe `label`: 4 before, 0 after
- New violations: 0

Agent browser smoke on patched runtime:

- 4 target checkboxes matched `[id^="edit-imagefile-file-limited-"][id$="-display"]`.
- Each target checkbox had `label[for]` text `Include file in display`.
- Each target label included `visually-hidden`.
- No target checkbox needed `aria-label`; the name came from the native label.
- axe `label` returned 0 violations.
- Real `Tab` reached `#edit-imagefile-file-limited-0-display`.
- Real `Space` toggled checked `true -> false`; a second `Space` restored `true`.

Focused test and hygiene:

- `php -l core/modules/file/src/Hook/FileThemeHooks.php`: pass
- `php -l core/modules/file/tests/src/Functional/FileFieldDisplayTest.php`: pass
- `git diff --check`: pass
- `vendor/bin/phpcs --standard=core/phpcs.xml.dist <changed files>`: pass
- `ddev exec ... ./vendor/bin/phpunit -c core/phpunit.xml.dist core/modules/file/tests/src/Functional/FileFieldDisplayTest.php --filter testNodeDisplay`: pass, 1 test / 37 assertions

## Boundaries

This verification claims:

- Native programmatic labels exist for the target file display checkboxes.
- The target axe `label` violations are fixed under the same route and conditions.
- The target checkbox is keyboard reachable and Space-operable.

This verification does not claim:

- Human VoiceOver/NVDA testing was performed.
- The repeated label text is uniquely disambiguated by file name outside table context.
- Non-target `color-contrast` or `region` violations on the fixture route are fixed.

## Next Action

Track Mike review on PR #21. Keep scope limited to native invisible labels for multiple file display checkboxes unless reviewer asks for unique per-file label text or broader file-widget semantics.
