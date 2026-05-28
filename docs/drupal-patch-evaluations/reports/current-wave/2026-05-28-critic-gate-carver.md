# Critic Gate: LABEL-IN-NAME-004 and DRUPAL-A11Y-007

> Date: 2026-05-28
> Agent: Carver
> Verdict: `ACCEPT-WITH-RESERVATIONS`

## Status Recommendations

`LABEL-IN-NAME-004` can be marked `VERIFIED` locally. The repaired evaluator report passed with baseline observed, one fixed target, zero remaining targets, and no new violations. The fixed rule was `label-content-name-mismatch`, reduced from 4 failures to 0. Manual axe evidence independently confirmed the accessible-name contract before and after patching.

`DRUPAL-A11Y-007` can be marked `VERIFIED` only as local automated verification of the reroll candidate. It must not be described as verification of the original upstream raw patch, and it must not be described as full assistive-technology verification.

## Reservations

1. The first reroll report showed a client-created warning message rendered as `role="alert"`, while the intended design was `role="status"` for non-error messages.
2. The evaluator pass should not be described as complete historical route coverage. Several generated cases skipped because the baseline target was not observed in this runtime.
3. One NVDA or VoiceOver smoke check is still needed before presenting the role design as user-verified upstream evidence.

## Integration

The warning-role reservation was resolved after the critic gate by expanding the `007` reroll to JavaScript message themers as well as Twig templates. A DOM probe with the final patch applied confirmed:

```text
/admin/appearance: error alert, warning status
/admin/modules: error alert, warning status
JavaScript-created warning: warning status
```

The remaining caveat is assistive-technology smoke testing.
