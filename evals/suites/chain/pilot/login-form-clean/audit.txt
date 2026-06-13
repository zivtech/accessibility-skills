# Perspective Audit — login-form-clean (Opus)

(Audit stage output — faithful capture. ✅ INTEGRITY: did NOT read the rubric; honest about confidence.
Audited the 3 escalated perspectives. KEY: OVERTURNED the critic's keyboard escalation as a false
positive after verifying the source.)

Perspectives audited: Screen Reader (MEDIUM), Keyboard & Motor (MEDIUM), Cognitive (MEDIUM).

## Screen Reader & Semantic (MEDIUM)
Many PASS items recorded honestly (landmarks, h1→h2, label/htmlFor association, aria-describedby
mechanism, aria-required, noValidate delegation — all correct).
- MAJOR 1 — Stale aria-invalid="true" persists on a corrected field. aria-invalid={submitted &&
  !!errors.email} (:53/:70); errors only written in handleSubmit (:21-22); onChange (:51/:68) never
  recomputes/clears. After a failed submit, a fixed field still announces "invalid entry". 4.1.2.
- MAJOR 2 — Stale inline error text remains in the a11y tree (id="email-error" still referenced by
  aria-describedby). 3.3.1.
- MINOR 3 — role="alert" goes silent on an IDENTICAL repeat submit (unchanged node text → no
  re-announce). Narrow trigger; first-failure and partial-correction cases announce fine. 4.1.3.

## Keyboard & Motor (MEDIUM) — ESCALATION NOT REPRODUCED (critic false positive)
The critic feared "focus-to-summary on every submit yanks focus." VERIFIED: there is NO focus
management in the source at all — no useRef, no useEffect, no .focus(). The error-summary anchors
(href="#field", :39) are manually-activated skip links, not auto-focus. Keyboard perspective is
CLEAN today (focus indicators 3px outline, logical order, native controls, targets >=24px all PASS).
Converted to a forward-looking implementation CONSTRAINT: when fixing MAJOR 1/2 with onChange
revalidation, a later focus-to-summary must be keyed to a submit counter, NOT [errors], or it would
introduce the very yank the critic feared.

## Cognitive & Neurodivergent (MEDIUM)
Error-message wording is genuinely good (specific suggestions); autocomplete present; no auto-submit.
- MAJOR 5 — Corrected field keeps red border (styles.css:66-68, driven by stale aria-invalid) + error
  text, contradicting the user's action ("I fixed it — why is it still angry?"). Same root cause. 3.3.1.

## Summary
Perspectives audited: 3. CRITICAL: 0. MAJOR: 3 (all ONE root cause: errors never cleared on change;
submitted latches true forever). MINOR: 1. keyboard: false-positive escalation, corrected.
Overall recommendation: REVISE (not a block; no CRITICAL).

⚠️ FIXTURE FINDING: this fixture is labeled CLEAN with expected_audit_verdict: PASS, but it carries a
GENUINE MAJOR stale-error-state defect (verified in source). The chain correctly found it. So login's
non-PASS audit + 3-perspective escalation is the chain catching a real bug the fixture's static
alarm ground truth missed — NOT a chain false-positive (except the keyboard sub-escalation, which WAS
a critic false-positive the audit corrected).
