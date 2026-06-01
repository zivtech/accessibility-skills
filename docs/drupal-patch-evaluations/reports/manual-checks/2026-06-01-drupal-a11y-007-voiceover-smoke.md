# DRUPAL-A11Y-007 VoiceOver Smoke Attempt

> Date: 2026-06-01T02:28Z (`2026-05-31 22:28 -0400`); rerun 2026-06-01T13:31Z (`2026-06-01 09:31 -0400`)
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

## 2026-06-01 Caption-Panel Rerun

The rerun used a dedicated visible Chrome window driven by Playwright while macOS VoiceOver was running with the caption panel visible. The 007 patch was temporarily applied to the disposable runtime and Drupal cache was rebuilt before testing.

Artifacts:

- `docs/drupal-patch-evaluations/reports/manual-checks/artifacts/2026-06-01-007-voiceover-caption/voiceover-007-evidence.json`
- `docs/drupal-patch-evaluations/reports/manual-checks/artifacts/2026-06-01-007-voiceover-caption/voiceover-007-warning-rerun.json`
- `docs/drupal-patch-evaluations/reports/manual-checks/artifacts/2026-06-01-007-voiceover-caption/voiceover-007-direct-announce.json`
- `docs/drupal-patch-evaluations/reports/manual-checks/artifacts/2026-06-01-007-voiceover-caption/04-error-live-region-caption.jpg`
- `docs/drupal-patch-evaluations/reports/manual-checks/artifacts/2026-06-01-007-voiceover-caption/10-warning-after-10s-no-caption.jpg`
- `docs/drupal-patch-evaluations/reports/manual-checks/artifacts/2026-06-01-007-voiceover-caption/16-direct-assertive-caption.jpg`

### Rerun Results

Server-rendered messages on `/admin/appearance`:

- Error message wrapper rendered `role="alert"`.
- Warning message wrapper rendered `role="status"`.

Dynamic `Drupal.Message` probes:

- Injected warning text: `VoiceOver warning priority probe 007 June one`.
- Rendered warning wrapper: `role="status"`.
- Live region priority: `aria-live="polite"`.
- VoiceOver caption result: no screenshot in the timed series captured the warning text. Captures at 1, 3, 6, and 10 seconds continued to show normal navigation/focus output instead.
- Injected error text: `VoiceOver error priority probe 007 June one`.
- Rendered error wrapper: `role="alert"`.
- VoiceOver caption result: the caption panel captured `VoiceOver error priority probe 007 June one`.

Direct `Drupal.announce()` controls:

- Direct polite announce text: `VoiceOver direct polite announce 007`.
- Live region eventually contained the polite text with `aria-live="polite"`.
- VoiceOver caption result: no 1, 4, or 8 second capture showed the polite text.
- Direct assertive announce text: `VoiceOver direct assertive announce 007`.
- VoiceOver caption result: the caption panel captured `VoiceOver direct assertive announce 007`.

Tabledrag warning probe:

- Route: `/admin/structure/menu/manage/main`.
- `Drupal.theme('tableDragChangedWarning')` was available.
- Inserted warning rendered `role="status"` with text `* You have unsaved changes.`
- VoiceOver caption result: no tabledrag warning announcement was captured; the caption panel continued to show navigation/focus output.

## Rerun Verdict

`PARTIAL / STILL INCONCLUSIVE`

This rerun is materially stronger than the earlier page-world-only pass because it captured actual VoiceOver caption-panel output for alert/assertive paths. It supports these narrow claims:

- Error messages are exposed as `role="alert"`.
- VoiceOver did caption the dynamic error message text.
- Direct assertive `Drupal.announce()` output was captioned by VoiceOver.
- Warning/status messages are exposed as `role="status"` and use polite live-region priority.
- Polite warning/status output did not interrupt the current VoiceOver navigation/focus output in this run.

It does not support claiming warning/status announcements were successfully heard or captioned. Across repeated timed captures, VoiceOver did not show the polite warning/status probe text. Treat that as unresolved AT behavior, not as a pass.

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

The smoke attempts now support three narrow claims: this patched Chrome/VoiceOver page did not expose duplicate `contentinfo` landmarks in the rotor during the earlier pass, the actual page-world Drupal message APIs rendered the expected warning/status and error/alert DOM plus live-region priority, and the VoiceOver caption panel captured error/assertive message text.

It still does not prove warning/status messages are announced in VoiceOver. The warning/status text remained visible in the DOM and live region, but no caption-panel capture showed that polite announcement. The missing evidence is a human screen-reader-user pass or a repeatable AT capture showing the intended warning/status behavior.

Keep `DRUPAL-A11Y-007` as `INCONCLUSIVE` until a human VoiceOver or NVDA tester can complete the checklist against warning/status and error announcement behavior.

## Non-Claims

- This is not a human screen-reader-user test.
- This is not VoiceOver + Safari verification.
- This complements, but does not replace, the FunctionalJavascript regression that verifies `Drupal.Message` live-region priority.
- This does not cover all Drupal themes, message states, or dynamic Ajax flows.
