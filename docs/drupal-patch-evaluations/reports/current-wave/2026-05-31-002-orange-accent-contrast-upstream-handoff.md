# DRUPAL-A11Y-002 Orange Accent Contrast Upstream Handoff

## Upstream PR

PR: https://github.com/mgifford/drupal-core/pull/20

Branch: `AlexU-A:codex/orange-accent-contrast-20260531`

Commit: `6d6ce230d9 fix: darken default admin orange accent`

Worktree: `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-pr-orange-accent-contrast-20260531`

GitHub state on 2026-05-31:

```text
state: OPEN
draft: false
mergeStateStatus: CLEAN
AccessLint: SUCCESS
```

## What Changed

Default Admin's orange accent preset moved from `#c55228` to `#bf4e25`.

The fix is intentionally at `Helper::accentColors()` because that value feeds both:

- server-rendered `--accent-base` on the root element
- `drupalSettings.gin.accent_colors` consumed by migration JS

The regression test extends `AdminTest::testAccentColorSetting()` to assert the orange preset renders `--accent-base: #bf4e25;`.

## Evidence

Source report baseline:

```text
DRUPAL-A11Y-002 / DRU-F75A07EF
selector: a[hreflang="he"]
foreground: #c55228
background: #fefaf8
ratio: 4.38:1
rule: color-contrast
```

After-patch focused axe checks:

```text
/action-link: 0 color-contrast violations
/admin: 0 color-contrast violations
/admin/content: 0 color-contrast violations
```

Regression checks:

```text
git diff --check: pass
php -l changed files: pass
Drupal PHPCS on changed files: pass
Focused AdminTest::testAccentColorSetting: OK (1 test, 11 assertions)
Full AdminTest.php: OK (5 tests, 54 assertions)
```

Regression classification: low-to-moderate risk because one shared Default Admin preset color changes globally for orange accent. No markup, behavior, route-specific CSS, or non-orange presets changed.

## Boundaries

This PR resolves the canonical orange accent contrast source for `DRUPAL-A11Y-002`.

It does not claim a full Default Admin accent palette audit. It also does not revive the stale `DRUPAL-A11Y-005` yellow/button patch thread; that packet is now marked obsolete unless fresh source evidence appears.
