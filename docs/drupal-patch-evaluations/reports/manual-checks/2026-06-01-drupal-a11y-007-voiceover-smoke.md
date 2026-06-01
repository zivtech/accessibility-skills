# DRUPAL-A11Y-007 VoiceOver Smoke Attempt

> Date: 2026-06-01T02:28Z (`2026-05-31 22:28 -0400`)
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

A follow-up Chrome pass used `/admin/appearance` again. Direct Chrome AppleScript checks for `Drupal` were misleading because they run outside the page's JavaScript world, so I injected a page-world script that wrote probe results back to DOM attributes and then read those attributes from AppleScript.

## Observations

- VoiceOver captions were visible and active while Chrome displayed the patched `/admin/appearance` page.
- The page showed the expected rendered error and warning messages.
- VoiceOver's Links rotor listed page links, including two `available updates` links from the visible messages.
- VoiceOver's Landmarks rotor reported `No items in, Landmarks menu`; no duplicate `contentinfo` landmark entries were observed in this browser/AT pass.
- The follow-up page-world probe confirmed `Drupal.Message` and `Drupal.announce` were available on `/admin/appearance`.
- Injected warning message: rendered `role="status"`; `#drupal-live-announce` had `aria-live="polite"` and text `VoiceOver warning priority probe`.
- Injected error message: rendered `role="alert"`; `#drupal-live-announce` had `aria-live="assertive"` and text `VoiceOver error priority probe`.
- Screenshots showed both injected messages visible while VoiceOver was running.
- The screenshots did not capture a readable VoiceOver caption containing either live-region probe text.

## Result

This is not enough to mark the packet `VERIFIED`.

The smoke attempt supports two narrow claims: this patched Chrome/VoiceOver page did not expose duplicate `contentinfo` landmarks in the rotor, and the actual page-world Drupal message APIs rendered the expected warning/status and error/alert DOM plus live-region priority.

It still does not prove warning/status announcements are non-interruptive in VoiceOver, and it does not prove error messages are announced with alert urgency. The missing evidence is the actual VoiceOver caption/audio announcement, ideally observed by a human screen-reader user.

Keep `DRUPAL-A11Y-007` as `INCONCLUSIVE` until a human VoiceOver or NVDA tester can complete the checklist against warning/status and error announcement behavior.

## Non-Claims

- This is not a human screen-reader-user test.
- This is not VoiceOver + Safari verification.
- This complements, but does not replace, the FunctionalJavascript regression that verifies `Drupal.Message` live-region priority.
- This does not cover all Drupal themes, message states, or dynamic Ajax flows.
