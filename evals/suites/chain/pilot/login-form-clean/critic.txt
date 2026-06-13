# Verdict: ACCEPT-WITH-RESERVATIONS  (a11y-critic, Opus)

(Critic stage output — faithful capture. ✅ INTEGRITY: this critic explicitly stayed blind —
"I'm reviewing a plan, not scoring the fixture, so I'll avoid reading the rubric to keep my
judgment independent." Used a 7-perspective taxonomy with DIFFERENT names again: screen reader,
keyboard, low vision, cognitive, motor, speech/voice, seizure/vestibular — none identical to the
modal critic's 6 lenses or the video critic's 7. Taxonomy instability recorded as instrument finding.)

**Overall**: Strong, evidence-accurate plan (line citations verified). Correctly identifies the
headline risk (role="alert" re-announce failure on a second identical submit) and the focus-move
design. Not ACCEPT because it never engages the component's STALE-ERROR LIFECYCLE.

## Major Findings (real dynamic-behavior bugs the critic found independently)
MAJOR 1 — Stale aria-invalid + stale error text persist while the user fixes the field. Source:
  aria-invalid={submitted && !!errors.email} (:53); errors only written in handleSubmit (:22);
  onChange (:51) never re-validates/clears. After a failed submit, a corrected field still
  announces "invalid entry" + shows red border + old error <p> until next submit. The plan's
  "drive all three off the SAME condition" rec would entrench this unless paired with on-change
  clearing, which the plan omits. WCAG 3.3.1, 4.1.2. Hits SR + cognitive users hardest.
MAJOR 2 — Recommended Option A (focus-to-summary on EVERY failed submit) fights the error-link
  focus-move: Enter-submit from within a field during the correction loop yanks focus back to the
  summary every iteration. Disorienting for keyboard/SR users. Fix: don't steal focus when already
  inside the form's error context; use Option B's re-announce mechanism there.

MINOR: password-hint must be unconditionally in aria-describedby (only error id conditional);
touch-target heights asserted from padding arithmetic not measurement; aria-busy/aria-disabled
button state mentioned 3× without one decision.

## Perspective Alarm Levels (independent — critic stayed blind)
| Perspective | Alarm |
|---|---|
| screen reader | MEDIUM |
| keyboard | MEDIUM |
| low vision | LOW |
| cognitive | MEDIUM |
| motor | LOW |
| speech / voice | LOW |
| seizure / vestibular | LOW |

Escalation: YES — SR + keyboard + cognitive at MEDIUM. The critic escalated on THREE perspectives.
⚠️ Rubric expected NARROW escalation: expected_escalated_perspectives = [cognitive_neurodivergent]
ONLY → per rubric S4 scoring this is SCOPE-INFLATED → S4=0. BUT the critic found genuine dynamic
bugs (MAJOR 1/2) reviewing the PLAN (planner rated it Medium), which the CLEAN fixture's static
alarm profile did not anticipate. Recorded as a CLEAN-probe calibration finding: in the chain, the
critic reviews the PLAN, surfacing more than the source-only perspective ground truth predicts.
Verdict ACCEPT-WITH-RESERVATIONS (not REVISE, so not an outright rubric fail), but the reservations
are MAJOR-level, exceeding the rubric's "enhancement-level only" bar for ACCEPT-WITH-RESERVATIONS.
