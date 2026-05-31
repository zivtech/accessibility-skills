# Drupal Accessibility Patch Evaluation Packet: DRUPAL-A11Y-002 Submit Button Contrast

> Status: VERIFIED
> Prepared: 2026-05-28
> Last updated: 2026-05-31
> Purpose: Local evaluator packet for the canonical `DRUPAL-A11Y-002` color-contrast source, now resolved upstream as Default Admin orange accent contrast.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-DRUPAL-A11Y-002-submit-button-contrast` |
| Status | `VERIFIED` |
| Project/package | `mgifford/drupal-core` |
| Target commit checked | `9ec853aac0` (`origin/main` on 2026-05-31) |
| Local runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| PR worktree | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-pr-orange-accent-contrast-20260531` |
| Patch artifact | `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-002-submit-button-contrast-codex-orange-accent-contrast.patch` |
| Evidence artifact | `docs/drupal-patch-evaluations/reports/manual-checks/2026-05-31-drupal-a11y-002-orange-accent-contrast.md` |
| Upstream PR | https://github.com/mgifford/drupal-core/pull/20 |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Source Reconciliation

The first local evaluator run was blocked because it followed stale packet state and did not recreate the source report's Default Admin orange accent conditions.

The current pattern report maps canonical `DRUPAL-A11Y-002` to:

- pattern `DRU-F75A07EF`
- axe rule `color-contrast`
- selector `a[hreflang="he"]`
- Default Admin orange accent foreground `#c55228` against generated background `#fefaf8`
- measured contrast `4.38:1`, below WCAG 2.2 SC 1.4.3 AA

The candidate therefore changes the shared Default Admin orange preset from `#c55228` to `#bf4e25` in `Helper::accentColors()`. That source feeds both server-rendered `--accent-base` and the migration JS settings.

## Verification

Runtime state:

```text
system.theme default: default_admin
system.theme admin: default_admin
default_admin.settings preset_accent_color: orange
```

Before the patch, focused axe reproduction on `/action-link` observed the canonical Hebrew language link using `#c55228` and axe reported the `color-contrast` failure.

After the patch:

```text
/action-link: data-gin-accent="orange", --accent-base: #bf4e25;, color-contrast violations: 0
/admin: data-gin-accent="orange", --accent-base: #bf4e25;, color-contrast violations: 0
/admin/content: data-gin-accent="orange", --accent-base: #bf4e25;, color-contrast violations: 0
```

Regression checks:

```text
git diff --check: pass
php -l core/themes/default_admin/src/Helper.php: pass
php -l core/themes/default_admin/tests/src/Functional/AdminTest.php: pass
Drupal PHPCS on changed files: pass
Focused AdminTest::testAccentColorSetting: OK (1 test, 11 assertions)
Full core/themes/default_admin/tests/src/Functional/AdminTest.php: OK (5 tests, 54 assertions)
GitHub AccessLint on PR #20: pass
```

Regression classification: low-to-moderate risk. The change alters one shared Default Admin preset color, so it can affect every surface using orange accent, but it does not change markup structure, interaction behavior, route-specific CSS, or other accent presets. The after-patch axe probes covered the source route and two admin routes under the same orange accent conditions, and the full Default Admin functional test file passed.

## Outcome

`VERIFIED`

PR #20 is open and clean: https://github.com/mgifford/drupal-core/pull/20

This verifies the canonical orange accent source behind `DRUPAL-A11Y-002`. It does not claim that every Default Admin preset has been audited, and it does not validate the stale yellow-accent patch thread that appeared in older local artifacts.
