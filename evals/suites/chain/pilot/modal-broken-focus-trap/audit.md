# Perspective Audit — modal-broken-focus-trap (Opus)

(Audit stage output. Captured for chain eval. KEY META-OBSERVATION the audit made on its own:
the escalation injected the critic's PLAN-level findings — about proposed fixes — but the skill
Step 4 points the audit at SOURCE files, which contain none of those proposed elements. The audit
re-grounded every finding in the actual source. Recorded as a chain finding in PILOT-REPORT.)

Perspectives audited: 3 (Keyboard & Motor, Screen Reader & Semantic, Magnification/Low Vision) —
exactly the escalated set, no LOW leakage.

## Keyboard & Motor Access (escalated MEDIUM)
1. MAJOR — No focus movement INTO the dialog on open (2.4.3). Evidence: component.jsx:115 renders
   conditionally; no useEffect, no ref, no .focus() in SubscribeModal (lines 3-82). Focus stays on
   the trigger; next Tab lands on background nav. [THIS IS THE TRACER — survived to last stage.]
2. MAJOR — No focus restoration on close (2.4.3). component.jsx:89-92 handleClose has comment
   "// Missing: triggerRef.current?.focus();"; triggerRef wired at :100 never read.
3. MAJOR — Escape does not close the dialog (2.1.2 / dialog convention). No onKeyDown anywhere.
4. MAJOR — No focus containment; Tab leaks to non-inert background (2.1.2). Background nav remains
   in tab order; no trap, no inert.
Critic-claim check: the escalation's "Enter-submit → error-summary tabindex no-op" describes the
PLAN; the SOURCE has no error summary and no validation at all (handleSubmit ignores empty fields).

## Screen Reader & Semantic (escalated MEDIUM)
5. CRITICAL — Dialog has no role="dialog", no aria-modal, no accessible name (4.1.2). component.jsx:27
   is a bare <div className="modal-container">; h2 has id="modal-title" but dialog never references it.
   [Red-flag auto-CRITICAL: custom widget with no ARIA role.]
6. MAJOR — noValidate form with required fields but no error handling/association (3.3.1). handleSubmit
   (:9-12) sets submitted=true regardless; no aria-invalid, no error text, no aria-describedby.
7. MAJOR — Success confirmation not announced (4.1.3). component.jsx:14-23 swaps to <p> with no
   role="status"/aria-live and no focus move. SR user gets silence.
8. MAJOR — Double-announcement risk is real ONLY if BOTH role="status" AND focus-move adopted; source
   currently does NEITHER (zero announcement, not double). Critic's concern is plan-level.

## Magnification / Low Vision (escalated MEDIUM)
9. MAJOR — Focus indicator invisible on the two primary blue buttons (2.4.13 / 1.4.11). Measured:
   outline #1565c0 on .btn-primary fill #1565c0 = 1.0:1; .btn-open same = 1.0:1. outline-offset:2px
   partially rescues against the white page (5.75:1) but the inner edge vanishes against the button.
   Secondary button fine (#1565c0 on #f5f5f5 = 5.27:1). Critic-claim check: the "white box-shadow on
   the wrong side" describes a PROPOSED fix not in source (source uses outline); diagnosis correct,
   mechanism unverifiable against source. Correct geometry: white INNER ring (vs blue button) + dark/
   blue OUTER ring (vs white page).

## Summary
Perspectives audited: 3. CRITICAL: 1. MAJOR: 8. MINOR: 0. Overall recommendation: BLOCK.

### Confirmed vs corrected in the critic's escalation
- Confirmed: focus indicator fails on the two blue buttons (1.0:1 measured); double-announce risk real
  if both techniques adopted; tabindex="-1" mechanism for a programmatically-focused summary is correct.
- Corrected/unverifiable from source: the escalation described a PROPOSED fix (white box-shadow ring,
  error summary, success-heading focus-move + role="status") absent from these files. Source uses
  outline focus styles, has NO error summary, NO validation, and NO success announcement (zero, not
  double). Re-grounded each finding in the actual code.

### Negative space (audit limits)
- No browser run. Reflow/zoom PASS verdicts (1.4.4, 1.4.10, 1.4.12) inferred from CSS source, not
  screenshot-verified. LOW perspectives (vestibular, auditory, cognitive, broad contrast) not audited.

Overall audit verdict: BLOCK.
