# Fixture: Form Testing Strategy

## Feature Description

You're planning accessibility testing for a user registration form used at the entry point of a healthcare patient portal. The form has 8 fields across two sections: Personal Information (first name, last name, date of birth, phone) and Account Setup (email, password, confirm password, terms acceptance checkbox). Validation fires on blur for individual fields and on submit for the full form.

The form:
- Shows inline error messages below each invalid field on blur (not on keyup)
- Associates errors with fields via `aria-describedby`
- Marks invalid fields with `aria-invalid="true"` and a red border
- Shows a summary error banner at the top of the form on failed submit
- Marks required fields with a red asterisk (*) and `aria-required="true"`
- Has a "Show password" toggle button that converts the password input type

## Context

- **Platform:** React web application with React Hook Form
- **Existing code:** Yes, component exists and is going to production in 3 weeks
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA (Windows), JAWS (Windows), VoiceOver (macOS), keyboard-only users
- **Scope:** Single multi-section registration form (8 fields)
- **Constraints:** QA team has no screen reader experience; must produce step-by-step runbooks; Playwright + axe-core already in CI; deadline is 3 weeks

## Requirement

Create a comprehensive accessibility testing plan that a QA engineer with basic accessibility knowledge can execute. The plan should be structured enough for consistent execution across team members.

The plan should cover:
- Automated testing setup (axe-core, Playwright)
- Keyboard navigation order
- Error announcement testing
- Screen reader form mode
- Visual regression for focus indicators and error states
- Focus management verification
- ARIA state testing
- Test prioritization and execution order
- Acceptance criteria
- a11y-critic review checkpoints

## Scope Hints

This is a **MODERATE** difficulty fixture — multiple interacting concerns (form semantics, error announcement, screen reader form mode, keyboard order, visual error states). Expected plan length is 3-4 pages. Focus on:

1. Axe-core rules for forms: `label`, `label-content-name-mismatch`, `aria-required-attr`, `color-contrast`, `autocomplete-valid`
2. Keyboard test: Tab order matches visual order, focus reaches all 8 fields plus submit button
3. Error announcement: blur validation announces via aria-describedby + aria-invalid; submit summary banner uses role="alert"
4. Screen reader form mode: In NVDA forms mode (F), labels are read with each field; errors are associated correctly
5. "Show password" toggle: Focus should remain in the password field context after activation, not jump to top
6. Visual regression: Capture error state screenshots for each invalid field and the summary banner

## What Success Looks Like

An excellent plan would:
- ✓ Name specific axe-core rule IDs relevant to forms, not just "run axe"
- ✓ Document the exact keyboard Tab order (field 1 → 2 → ... → 8 → submit) and verify against visual layout
- ✓ Provide step-by-step error announcement testing (trigger blur on empty required field → verify NVDA announces error)
- ✓ Document NVDA Forms Mode explicitly (F to enter, Tab through fields, errors read in context)
- ✓ Test the "show password" toggle: focus stays in password area, toggle role="button" announced
- ✓ Include measurable acceptance criteria (e.g., "error message text matches aria-describedby value of input")
- ✓ Cover the submit-time error summary banner: role="alert", focus moves to banner, all errors listed
- ✓ Specify Playwright assertions for aria-invalid and aria-describedby
- ✓ Include visual regression test list: field-default, field-focused, field-error, form-submit-error-banner states

## What Would Be Below Expectations

- ✗ "Verify all fields have labels" without specifying which axe rule catches unlabeled inputs
- ✗ No mention of NVDA Forms Mode — a plan that misses this will produce incorrect screen reader test results
- ✗ Keyboard test described as "tab through the form" without specifying the expected focus order
- ✗ Error announcement test that says "verify error is announced" without specifying which mechanism (aria-describedby vs aria-live)
- ✗ No test for the "show password" toggle accessibility (focus management, role, state)
- ✗ Acceptance criteria that are not measurable ("errors should be clear to users")
- ✗ Missing the submit-time error summary banner entirely
- ✗ Prescribing that each field should have `aria-label` — native `<label for>` association is preferred; over-prescribing aria-label is a planning smell
