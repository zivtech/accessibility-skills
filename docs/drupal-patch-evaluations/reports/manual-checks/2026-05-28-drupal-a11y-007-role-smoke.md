# Role Smoke Check: DRUPAL-A11Y-007 Messages Landmark Role

> Status: DOM/axe role smoke passed; real NVDA/VoiceOver smoke still not run
> Date: 2026-05-28
> Runtime: `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime`
> Base URL: `http://drupal-core.ddev.site:33000`

## Scope

This is not a substitute for a screen reader smoke check. NVDA is unavailable on this macOS runtime, and VoiceOver was not already running. I did not enable VoiceOver because that changes the user's desktop state.

This probe verifies the role semantics that a screen reader would consume:

- server-rendered error messages use `role="alert"`;
- server-rendered warning messages use `role="status"`;
- JavaScript-created warnings use `role="status"`;
- JavaScript-created errors use `role="alert"`;
- target axe landmark rules remain clear after the reroll patch is applied.

## Command

```bash
cd /Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
git apply patches/a11y-DRUPAL-A11Y-007-messages-landmark-role.patch
ddev drush cache-rebuild
node <<'NODE'
// Playwright script applied the patch, logged in through Drush ULI,
// scanned /admin/appearance and /admin/modules for:
// - landmark-contentinfo-is-top-level
// - landmark-no-duplicate-contentinfo
// It also created one Drupal.Message warning and one Drupal.Message error.
NODE
git apply -R patches/a11y-DRUPAL-A11Y-007-messages-landmark-role.patch
ddev drush cache-rebuild
```

## Result

Target axe violation count after the reroll patch:

| Route | Target axe violations |
|---|---:|
| `/admin/appearance` | 0 |
| `/admin/modules` | 0 |

Server-rendered messages after patch:

```text
/admin/appearance error: role=alert
/admin/appearance warning: role=status
/admin/modules error: role=alert
/admin/modules warning: role=status
```

JavaScript-created messages after patch:

```text
/admin/appearance warning: role=status
/admin/appearance error: role=alert
/admin/modules warning: role=status
/admin/modules error: role=alert
```

## Interpretation

The reroll's role design is coherent at the DOM and axe-rule layer. It still needs a short human NVDA or VoiceOver smoke check before being described upstream as assistive-technology verified.
