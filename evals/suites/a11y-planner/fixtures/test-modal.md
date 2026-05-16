# Fixture: Modal Dialog Testing

## Feature Description

You're planning accessibility testing for a confirmation modal dialog used in a project management SaaS application. The modal appears when a user clicks "Delete Project" — it requires the user to type the project name to confirm deletion, then click a destructive "Delete" button or press Escape/click the backdrop to cancel.

The modal:
- Opens on button click; focus moves to the dialog container (the `<div role="dialog">`)
- Has a visible title ("Delete Project: {name}") referenced via `aria-labelledby`
- Has a description paragraph referenced via `aria-describedby`
- Contains a text input (with label), a "Delete" button, and a "Cancel" button
- The "Delete" button is disabled until the text input value matches the project name
- Background content uses `inert` attribute when modal is open
- Pressing Escape or clicking the backdrop closes the modal and returns focus to the "Delete Project" trigger button
- Closing the modal with the "Cancel" button also returns focus to the trigger

## Context

- **Platform:** React web application (TypeScript), using a custom modal hook
- **Existing code:** Yes, component exists — engineering wants a testing plan before the next sprint
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA (Windows), JAWS (Windows), VoiceOver (macOS), keyboard-only users
- **Scope:** Single modal dialog component with confirmation input pattern
- **Constraints:** Must identify any axe-core violations before PR merge; Playwright + axe-core in CI; QA engineer writing tests has used Playwright but not screen readers

## Requirement

Create a comprehensive accessibility testing plan that a QA engineer with basic accessibility knowledge can execute. The plan should be structured enough for consistent execution across team members.

The plan should cover:
- Automated testing setup (axe-core, Playwright)
- Focus trap testing methodology
- Escape key and backdrop close testing
- Focus restoration verification
- Background inert testing
- Screen reader mode announcement (dialog role, title, description)
- Visual regression testing
- Test prioritization and execution order
- Acceptance criteria
- a11y-critic review checkpoints

## Scope Hints

This is a **MODERATE** difficulty fixture — modal dialogs have well-established APG patterns but the testing must cover the focus lifecycle (open → trap → close → restore), not just static state. Expected plan length is 3-4 pages. Focus on:

1. APG Dialog Modal pattern: https://www.w3.org/WAI/ARIA/apg/patterns/dialogmodal/
2. Focus trap: Tab cycles within modal; verify no Tab escape to background
3. Escape key: Modal closes, focus returns to trigger
4. Background inert: Elements outside modal are not reachable by keyboard or SR
5. Opening announcement: NVDA should announce dialog role + `aria-labelledby` title on open
6. Conditional "Delete" button: Test that `aria-disabled="true"` state changes are announced

## What Success Looks Like

An excellent plan would:
- ✓ Reference APG Dialog Modal pattern with explicit URL
- ✓ Provide step-by-step focus trap test: open modal → Tab through all interactive elements → verify Tab cycles back to first, not to background
- ✓ Document Escape key test: press Escape → modal closes → verify focus lands on trigger button
- ✓ Test background inert: verify background elements do not receive keyboard focus when modal is open
- ✓ Document NVDA announcement on open: what the screen reader says when focus moves to dialog (role, title, description)
- ✓ Test the conditional "Delete" button state: type correct text → aria-disabled changes → verify announcement
- ✓ Include Playwright assertions for inert attribute and aria-modal or inert on background container
- ✓ Specify visual regression states: modal-closed, modal-open, input-invalid-state, delete-button-enabled
- ✓ Cover backdrop click test: click outside modal → verify close and focus restoration

## What Would Be Below Expectations

- ✗ No APG dialog pattern reference — the dialog pattern is well-documented and must be the grounding
- ✗ Focus trap test described as "verify focus stays in modal" without step-by-step keyboard script
- ✗ No test for background inert — this is the most commonly missed test for modal dialogs
- ✗ Screen reader test that says "verify modal announced" without specifying what NVDA announces (role, title, description in what order)
- ✗ Missing focus restoration test — the most common modal accessibility failure in production
- ✗ No test for the conditional disabled state of the "Delete" button
- ✗ Prescribing `aria-modal="true"` as a required attribute — it's a workaround for older SRs that don't support `inert`; the plan should test inert as the primary mechanism and note aria-modal as a compatibility fallback
- ✗ Testing only "happy path" (successful deletion) without testing Cancel and Escape exit paths
