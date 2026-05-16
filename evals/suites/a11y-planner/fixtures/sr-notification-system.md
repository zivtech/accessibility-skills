# Fixture: Real-Time Notification Panel with Priority Tiers

## Feature Description

You're planning accessibility for a real-time notification system in a hospital EHR (electronic health records) web application. Notifications arrive via WebSocket and appear in a collapsible notification panel accessible via a bell icon button in the top navigation. Notifications have three priority tiers:

- **Error/Critical** (red): "Critical lab result: Patient Doe, John — Potassium 6.8 mEq/L. Requires immediate review." — must interrupt whatever the clinician is doing
- **Warning** (amber): "Medication order pending countersignature: Lisinopril 10mg, Patient Chen, Sarah" — should announce without interrupting
- **Info** (blue): "Appointment reminder: Team huddle at 14:00" — low-priority, should not interrupt

Each notification is dismissible (×  button). Notifications persist in a "Notification History" drawer accessible from the panel. An unread badge count on the bell icon shows the total unread count (capped at "99+" display). New notifications arrive while the panel is closed — the badge updates in real time. The panel can contain up to 50 visible notifications at a time; older ones are in History. Notifications auto-dismiss after configurable timeouts (Critical: never auto-dismiss; Warning: 30s; Info: 10s).

## Context

- **Platform:** React single-page application (TypeScript)
- **Existing code:** Yes — notification panel exists but all three priority tiers use the same `<div role="alert">` for every notification; badge count updates silently with no AT announcement; dismiss buttons are `<span>` elements with click handlers and no keyboard support; notification history is a `<div>` with no landmark or scroll management; no auto-dismiss countdown communicated to AT
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA (Windows), JAWS (Windows), VoiceOver (macOS), keyboard-only users
- **Scope:** Priority-tiered live regions, badge count announcement, dismiss interaction, notification history navigation, auto-dismiss timing
- **Constraints:** Critical notifications must interrupt (assertive); Warning/Info must not interrupt (polite); role="alert" is assertive by default — current implementation interrupts on ALL tiers; medical context means missed Critical announcements are a patient safety issue; auto-dismiss must allow sufficient time for AT users to read notifications before dismissal (WCAG 2.2.1)

## Requirement

Create a comprehensive accessibility design plan that a developer with no accessibility knowledge can use to implement the component correctly on the first attempt.

The plan should cover:
- Priority-tiered live regions: three separate `aria-live` regions with correct politeness levels (assertive for Critical, polite for Warning and Info)
- Why `role="alert"` alone is wrong: it maps to `aria-live="assertive"` — applying it to all tiers causes Warning/Info to interrupt workflow
- `aria-atomic="true"` decision per tier: Critical announcements should be read completely; Info notifications should announce only the new content added
- Badge count update strategy: when and how the unread count is announced without spamming
- Dismiss button: `<button>` element (not `<span>`), label pattern ("Dismiss: Critical lab result — Patient Doe, John"), keyboard interaction
- Notification history: region landmark, focus management when history drawer opens, scroll to latest
- Auto-dismiss timing: WCAG 2.2.1 requires pause/stop/hide control for auto-updating content; 10-second Info auto-dismiss may not give AT users enough time
- Focus management: where does focus go when the panel opens? When a notification is dismissed? When the last notification is dismissed?
- `role="status"` vs `role="alert"` vs `aria-live` — plan must distinguish these correctly
- Testing strategy with specific AT test cases for each priority tier
- Implementation tasks with a11y-critic checkpoints

## Scope Hints

This is a **COMPLEX** difficulty fixture — the challenge is the priority-tiered live region architecture and the safety-critical context. Expected plan length: 5-7 pages. Focus on:

1. Three dedicated `aria-live` regions (hidden from visual layout, persistent in DOM): `<div aria-live="assertive" aria-atomic="true" class="sr-only" id="critical-announcer">`, `<div aria-live="polite" aria-atomic="true" class="sr-only" id="warning-announcer">`, `<div aria-live="polite" aria-relevant="additions" class="sr-only" id="info-announcer">`
2. Message injection pattern: notifications are NOT added to the live region element — a message string is injected/replaced in the announcer element. New content → clear → inject pattern prevents DOM-add detection race conditions in NVDA/JAWS
3. Badge count: announce only when the panel is closed and a new notification arrives; do NOT announce every increment; use `aria-label="Notifications, 5 unread"` on the bell button rather than a separate live region
4. Auto-dismiss: WCAG 2.2.1 (Timing Adjustable) — 10s Info auto-dismiss needs a "Pause notifications" control; Critical never auto-dismisses (correct); Warning 30s is borderline for AT users
5. Dismiss focus management: when last notification in the panel is dismissed, focus should return to the bell button (the trigger); when a non-last notification is dismissed, focus should move to the next notification's dismiss button
6. Notification history: `<section aria-label="Notification history">` with `aria-live="off"` (history drawer is not a live region); focus moves to first item when drawer opens

## What Success Looks Like

An excellent plan would:
- ✓ Design three separate `aria-live` regions, not `role="alert"` on notification elements
- ✓ Correctly explain `role="alert"` = `aria-live="assertive"` — the existing code is wrong for Warning/Info
- ✓ Document the inject/clear/inject pattern for live region content (vs appending DOM nodes)
- ✓ Address badge count: `aria-label` on bell button rather than a separate live region per increment
- ✓ Specify dismiss button as `<button>` with a label that includes notification content summary
- ✓ Plan focus management for dismiss: next notification's dismiss button, or bell button if last
- ✓ Address WCAG 2.2.1 for auto-dismiss with a "Pause auto-dismiss" control requirement
- ✓ Flag the safety implication: Critical tier must always interrupt; a missed Critical announcement in an EHR is a patient safety failure
- ✓ Plan notification history as a region landmark with `aria-live="off"` (not a live region)
- ✓ Cite WCAG 4.1.3 (Status Messages), 2.2.1 (Timing Adjustable), 2.1.1 (Keyboard), 1.4.3 (Contrast)
- ✓ Include AT-specific test cases: NVDA test for Critical interruption, JAWS test for Info non-interruption

## What Would Be Below Expectations

- ✗ Using `role="alert"` for all three priority tiers — the existing bug, not the fix
- ✗ Single `aria-live` region for all notifications — cannot support mixed politeness levels
- ✗ Appending notification elements to the live region rather than injecting text — unreliable across NVDA/JAWS
- ✗ Badge count announced via a live region on every increment — announces "3", "4", "5" as each arrives
- ✗ No WCAG 2.2.1 analysis for auto-dismiss — the 10-second Info timeout is insufficient for many AT users
- ✗ Dismiss buttons not keyboard accessible — existing `<span>` elements are not in tab order
- ✗ No focus management plan for dismiss action
- ✗ Notification history treated as a live region — history should be `aria-live="off"`
- ✗ No WCAG 4.1.3 citation for the announcement strategy
