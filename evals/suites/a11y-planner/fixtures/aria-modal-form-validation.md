# Fixture: Modal Dialog with Form Validation

## Feature Description

You're planning accessibility for a modal dialog that contains a form with real-time validation. The component:
- Modal overlay (darkens background)
- Form inside the modal with multiple input fields
- Real-time validation (error messages appear as user types or on blur)
- Submit button that triggers validation (errors if invalid)
- Cancel button to close modal
- Close button (X icon in top right)
- Focus trap (Tab cycles within modal, doesn't escape)
- Focus restoration (focus returns to trigger button when modal closes)
- Error messages appear dynamically below inputs
- Success message after form submission

## Context

- **Platform:** Next.js web application
- **Existing code:** No, new component
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** JAWS, NVDA, VoiceOver, keyboard-only users
- **Scope:** Reusable modal component with flexible form content
- **Constraints:** Form validation can be async; Multiple modals can be stacked (nested); Error recovery needed

## Requirement

Create a comprehensive accessibility design plan covering:
- Modal semantics (role="dialog", aria-modal="true", aria-labelledby)
- Focus trap implementation (Tab key management)
- Focus restoration (focus returns to trigger button)
- Form structure (fieldset, legend for grouped inputs)
- Input and label association
- Error message communication (aria-describedby, aria-invalid)
- Real-time validation announcements (live region)
- Success/submission messaging
- Keyboard interactions (Tab, Escape to close)
- Screen reader experience (modal announcement, error announcements, form guidance)
- Testing strategy for validation, keyboard, focus management

## Scope Hints

This is an **AMBIGUOUS** difficulty fixture. It combines multiple complex patterns (modal + form + validation + focus trap). Plan should be 4-5 pages but complexity is unclear:
- Does validation happen real-time (aria-live) or on submit (aria-describedby)?
- How many form fields? (2 fields vs 10 fields changes complexity)
- Can modals be nested? (adds focus trap complexity)
- What's the error recovery flow?

Scope hints should help you navigate ambiguity:

1. Modal pattern mapping (APG Dialog)
2. Focus trap implementation with Tab key handling
3. Focus restoration mechanism
4. Form pattern (fieldset/legend, labels)
5. Error message association (aria-invalid, aria-describedby)
6. Validation strategy (real-time vs submit)
7. Live region planning for dynamic error messages
8. Test cases for keyboard, focus, validation, screen reader

## What Success Looks Like

An excellent plan would:
- ✓ Reference APG Dialog pattern with URL
- ✓ Document focus trap (Tab cycles, Escape closes)
- ✓ Document focus restoration mechanism
- ✓ Plan form structure with fieldset/legend
- ✓ Document aria-invalid and aria-describedby for error messages
- ✓ Plan real-time validation announcements (live region)
- ✓ Include HTML structure stub
- ✓ Address nested modal scenarios (if applicable)
- ✓ Include test cases for all scenarios

## What Would Be Below Expectations

- ✗ No APG Dialog pattern reference
- ✗ Focus trap not planned or unclear
- ✗ No focus restoration strategy
- ✗ Form structure vague
- ✗ Error messages not associated with fields
- ✗ No validation announcement strategy
- ✗ Ambiguity not addressed (unclear requirements)
- ✗ Missing test cases
