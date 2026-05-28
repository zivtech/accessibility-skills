# DRUPAL-A11Y-007 AT Smoke Checklist

> Date: 2026-05-28
> Patch: `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-007-messages-landmark-role-codex-reroll-status-alert-007.patch`
> Purpose: Fill the human assistive-technology evidence gap before upstream filing.

## Setup

Use the patched Drupal runtime or an equivalent Drupal core checkout with the reroll patch applied.

Recommended target routes:

```text
/admin/appearance
/admin/modules
```

The local DOM/axe role smoke already confirmed:

- server-rendered warnings use `role="status"`;
- JavaScript-created warnings use `role="status"`;
- errors use `role="alert"`;
- the old `role="contentinfo"` wrapper is removed from the tested message elements.

This checklist is only for human AT behavior.

## VoiceOver Smoke

1. Enable VoiceOver.
2. Open `/admin/appearance` with a visible warning or status message.
3. Confirm the message is discoverable without being exposed as a page `contentinfo` landmark.
4. Confirm a warning/status message does not interrupt like an error alert.
5. Trigger or load an error message if available.
6. Confirm the error is announced with alert urgency.
7. Repeat the same checks on `/admin/modules`.

## NVDA Smoke

1. Open the patched site in a Windows/NVDA environment.
2. Open `/admin/appearance` with a visible warning or status message.
3. Confirm the message is discoverable without appearing as a duplicate contentinfo landmark.
4. Confirm a warning/status message does not interrupt like an error alert.
5. Trigger or load an error message if available.
6. Confirm the error is announced with alert urgency.
7. Repeat the same checks on `/admin/modules`.

## Pass Criteria

Record a pass only if:

- warning/status messages are announced or discoverable with non-interruptive status behavior;
- error messages use alert-like urgency;
- tested message elements no longer create duplicate `contentinfo` landmark navigation noise;
- the tester records browser, AT, OS, and route details.

## Result Template

```text
Tester:
Date:
Browser:
OS:
AT/version:
Drupal route(s):
Patch artifact:

Warning/status behavior:
Error behavior:
Landmark navigation result:

Verdict: PASS | FAIL | INCONCLUSIVE
Notes:
```

## Non-Claims

This smoke check does not prove full screen reader support across all Drupal message states, themes, and browsers. It only closes the narrow AT-behavior gap for the rerolled status/error role semantics on the tested routes.
