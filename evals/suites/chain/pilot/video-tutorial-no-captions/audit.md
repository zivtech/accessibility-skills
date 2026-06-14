# Perspective Audit — video-tutorial-no-captions (Opus)

<!--OPERATOR
peek: false
reason: |
  INTEGRITY: did NOT read the rubric; reasoned the 1.2.3 question independently. Audited ONLY the
  2 escalated perspectives; LOW perspectives explicitly not reviewed → S5a no-leakage.
OPERATOR-->

Perspectives audited: Auditory Access (HIGH), Screen Reader & Semantic (MEDIUM).

## Auditory Access (HIGH)
- CRITICAL 1 — Video with instructor speech has NO captions. component.jsx:95-100 <video> self-closing,
  no <track> child. README confirms speech. 1.2.2 Level A. [THIS IS THE TRACER — survived to last stage.]
- CRITICAL 2 — Completion status conveyed ONLY by an 880Hz beep, never rendered. hasCompleted (:10)
  set at :23 but never in JSX return. 1.2.1.
- CRITICAL 3 — Error status conveyed ONLY by 220Hz beep, never rendered. hasError (:9) set at :31,
  never rendered. 1.2.1 / 3.3.1.
- MAJOR 4 — No transcript / media alternative. .tutorial-meta (:154-157) has only h2 + duration. 1.2.3.

1.2.3 reasoning (independent, honest-uncertainty): a narration-ONLY transcript does NOT satisfy 1.2.3
(Level A) when the tutorial shows visual-only content (on-screen code). 1.2.3's media-alternative branch
must describe the visual content (for users who can't see it); captions (1.2.2) are separately and
unconditionally required. 1.2.5 (AA) audio description may be naturally discharged if narration already
describes what's on screen — needs human verification.

## Screen Reader & Semantic (MEDIUM)
- MAJOR 5 — Completion not announced (no aria-live region for hasCompleted). 4.1.3.
- MAJOR 6 — Error not announced (no aria-live region for hasError). 4.1.3 / 3.3.1.
- MINOR 7 — <video> accessible name "video player" is generic; use the tutorial title. 1.1.1 / 4.1.2.
- announce-once: hasCompleted/hasError are one-way flags → conditional content enters the live region
  exactly once = announced once (correct). Keep aria-live="off" on the per-frame time display (:126).

Root cause: Findings 2,3,5,6 are ONE bug — hasError/hasCompleted set in state but never rendered. A
single fix (render both flags into a visible region that is also a live region) closes 2 CRITICAL +
2 MAJOR across both perspectives.

## Summary
Perspectives audited: 2. CRITICAL: 3. MAJOR: 3. MINOR: 1. Overall recommendation: BLOCK.
Fixture note (from the audit): the audio-only-status trap is a strong adversarial test — rewards a
reviewer for noticing set-but-never-rendered state that a <track>-grepping checklist would miss.
