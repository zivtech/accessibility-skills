# DRUPAL-A11Y-002 Orange Accent Contrast Focused Verification

## Summary

Canonical source: `DRUPAL-A11Y-002`, pattern `DRU-F75A07EF`, axe `color-contrast`.

The source report failure is a Default Admin orange accent contrast problem, not a route-specific language-switcher bug and not the stale yellow-accent patch thread from older local artifacts.

## Baseline Evidence

Source report baseline:

```text
Selector: a[hreflang="he"]
Foreground: #c55228
Background: #fefaf8
Measured ratio: 4.38:1
Expected: 4.5:1
Affected route used for reproduction: /action-link
```

Focused runtime reproduction before the patch confirmed the same selector, accent color, generated light accent background, and axe `color-contrast` failure.

## Patch

Upstream PR: https://github.com/mgifford/drupal-core/pull/20

Patch surface:

```text
core/themes/default_admin/src/Helper.php
core/themes/default_admin/tests/src/Functional/AdminTest.php
```

Change:

```text
Default Admin orange preset: #c55228 -> #bf4e25
```

`Helper::accentColors()` is the shared source for server-rendered `--accent-base` and the migration JS color settings, so no route-specific CSS was needed.

## After-Patch Evidence

Runtime state:

```text
system.theme default: default_admin
system.theme admin: default_admin
default_admin.settings preset_accent_color: orange
```

Focused axe `color-contrast` probes after the patch:

| Route | Rendered accent | Violations |
|---|---|---:|
| `/action-link` | `--accent-base: #bf4e25;` | 0 |
| `/admin` | `--accent-base: #bf4e25;` | 0 |
| `/admin/content` | `--accent-base: #bf4e25;` | 0 |

Observed sample after patch:

```text
a[hreflang="he"] color: rgb(191, 78, 37)
#edit-submit color: rgb(255, 255, 255)
#edit-submit background: rgb(191, 78, 37)
```

## Regression Checks

```text
git diff --check: pass
php -l core/themes/default_admin/src/Helper.php: pass
php -l core/themes/default_admin/tests/src/Functional/AdminTest.php: pass
Drupal PHPCS on changed files: pass
Focused AdminTest::testAccentColorSetting: OK (1 test, 11 assertions)
Full core/themes/default_admin/tests/src/Functional/AdminTest.php: OK (5 tests, 54 assertions)
GitHub AccessLint on PR #20: pass
```

Regression classification: low-to-moderate risk. The patch changes one shared Default Admin preset color, so all orange-accent surfaces inherit the darker value. It does not change markup, keyboard behavior, route-specific language-link CSS, or other accent presets.

## Boundaries

This verifies the canonical orange accent contrast failure from the pattern report.

This does not claim that every Default Admin accent preset has been audited. It also does not validate the stale yellow-accent patch thread that appeared in older local artifacts.
