# Sanitized Evaluator Summary: DRUPAL-A11Y-001 File Widget Display Labels

Generated from the local runtime run on 2026-06-01 at 13:16Z. This file intentionally omits raw environment dumps and local database connection fields from the generated evaluator artifact.

## Command

```bash
cd /Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
DRUPAL_BASE_URL=http://drupal-core.ddev.site \
  A11Y_VARIANT_ID=codex-invisible-label-001 \
  node core/tests/playwright/scripts/evaluate-patch.js \
  a11y-DRUPAL-A11Y-001-file-widget-display-labels
```

## Summary

- Description: Add invisible labels to file widget display checkboxes.
- WCAG criteria: `1.3.1 (A)`.
- axe rule: `label`.
- Pattern source: `reports/pattern-report-2026-05-06.json`.
- Target pattern ID: `DRU-6CA3D5EB`.
- Pattern ID match type: `source-pattern-matched`.
- Case generation mode: `pattern-report-derived`.
- Route: `/contact/imagefile_file`.
- Elements tested: `#edit-imagefile-file-limited-N-display`.
- Status: `PASS`.
- Outcome reason: `targeted-issues-fixed-without-regressions`.
- Eligible for patch recommendation: yes.

## Before/After

| Metric | Before | After | Change |
|---|---:|---:|---:|
| Total violations | 7 | 3 | -4 |
| `label` violations | 4 | 0 | -4 |
| `color-contrast` violations | 2 | 2 | 0 |
| `region` violations | 1 | 1 | 0 |

The target pattern was observed before patching, fully fixed after patching, and no new violations were introduced.

## Pattern Coverage

| Pattern ID | Rule | Path | Before | After | Status |
|---|---|---|---:|---:|---|
| `DRU-6CA3D5EB` | `label` | `/contact/imagefile_file` | 2 | 0 | fully fixed |

Instance coverage:

- Targeted instance IDs: 1.
- Seen before patch: 1.
- Fixed after patch: 1.
- Remaining after patch: 0.
- Not observed in baseline: 0.

## Patch Shape

The candidate does not add an `aria-label`. It keeps the existing checkbox title and changes the multiple-file table preprocess so the title is rendered as an invisible native label:

```php
$widget['display']['#title_display'] = 'invisible';
```

This preserves the visible table layout while giving each display checkbox a programmatic label.

## Additional Browser Smoke

A separate Playwright smoke check against the patched runtime confirmed:

- 4 target checkboxes matched `[id^="edit-imagefile-file-limited-"][id$="-display"]`.
- Each target checkbox had `label[for]` text `Include file in display`.
- Each target label included `visually-hidden`.
- axe `label` scan returned 0 violations.
- Real `Tab` navigation reached `#edit-imagefile-file-limited-0-display`.
- Real `Space` toggled that checkbox from `true` to `false`, and a second `Space` restored `true`.

This is agent browser role/name and keyboard evidence, not a human screen reader claim.
