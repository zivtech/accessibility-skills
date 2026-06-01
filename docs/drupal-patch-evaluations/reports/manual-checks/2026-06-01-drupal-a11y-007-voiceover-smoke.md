# DRUPAL-A11Y-007 VoiceOver Smoke Attempt

> Date: 2026-06-01T02:08Z (`2026-05-31 22:08 -0400`)
> Patch: `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-007-messages-landmark-role-codex-reroll-status-alert-007.patch`
> Verdict: `INCONCLUSIVE`

## Environment

| Field | Value |
|---|---|
| Runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| Drupal route | `/admin/appearance` |
| Browser | Google Chrome `148.0.7778.215`; Safari `26.4` attempted |
| OS | macOS `26.4.1` build `25E253` |
| AT | VoiceOver app metadata version `10` |
| Tester | Codex agent observing VoiceOver captions/screenshots |

## What Was Attempted

The final regenerated patch was temporarily applied to the runtime, Drupal cache was rebuilt, Chrome was logged in through a Drush ULI, and `/admin/appearance` was opened with VoiceOver running.

Safari was also attempted, but scripted JavaScript execution failed because Safari's "Allow JavaScript from Apple Events" setting is disabled. I did not change that user preference.

## Observations

- VoiceOver captions were visible and active while Chrome displayed the patched `/admin/appearance` page.
- The page showed the expected rendered error and warning messages.
- VoiceOver's Links rotor listed page links, including two `available updates` links from the visible messages.
- VoiceOver's Landmarks rotor reported `No items in, Landmarks menu`; no duplicate `contentinfo` landmark entries were observed in this browser/AT pass.
- Chrome AppleScript reported `has-message-api=false` for `Drupal.Message` on this loaded page, so dynamic warning/error message announcements were not exercised through VoiceOver.

## Result

This is not enough to mark the packet `VERIFIED`.

The smoke attempt supports the narrow negative claim that this patched Chrome/VoiceOver page did not expose duplicate `contentinfo` landmarks in the rotor. It does not prove warning/status announcements are non-interruptive in VoiceOver, and it does not prove error messages are announced with alert urgency.

Keep `DRUPAL-A11Y-007` as `INCONCLUSIVE` until a human VoiceOver or NVDA tester can complete the checklist against warning/status and error announcement behavior.

## Non-Claims

- This is not a human screen-reader-user test.
- This is not VoiceOver + Safari verification.
- This does not replace the FunctionalJavascript regression that verifies `Drupal.Message` live-region priority.
- This does not cover all Drupal themes, message states, or dynamic Ajax flows.
