# Fixture: Complex Modal with Focus Trap

## Feature Description

You're planning accessibility for a complex modal dialog containing a multi-section form with validation. The component:
- Modal overlay with multiple form sections
- Various input types (text, select, checkbox, radio)
- Form validation on blur and submit
- Focus must be trapped within modal (Tab cycles)
- Focus must return to trigger button when modal closes
- Escape key closes the modal
- Visual focus indicators on all focusable elements

## Context

- **Platform:** React e-commerce application
- **Existing code:** No, new modal component
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** JAWS, NVDA, VoiceOver, keyboard-only users
- **Scope:** Reusable modal component with form
- **Constraints:** Form size variable (10+ fields); Multiple modals can be stacked; Touch support needed

## Requirement

Create a comprehensive accessibility design plan covering:
- APG Dialog pattern mapping
- Focus trap implementation (Tab cycles within modal)
- Focus restoration mechanism
- Modal semantics (role="dialog", aria-modal, aria-labelledby)
- Form structure (fieldset/legend, labels, error association)
- Keyboard interactions (Tab, Shift+Tab, Escape)
- Screen reader experience
- Visual focus indicators
- Testing strategy for focus management

## Scope Hints

This is **COMPLEX** difficulty. Combines multiple patterns (modal + form + focus trap). Plan should be 4-5 pages covering focus trap details, focus restoration, form integration, and test cases.

## What Success Looks Like

An excellent plan would:
- ✓ Reference APG Dialog pattern with explicit URL
- ✓ Document focus trap: Tab cycles forward, Shift+Tab backward
- ✓ Document focus restoration mechanism
- ✓ Plan initial focus strategy
- ✓ Document form structure with fieldset/legend
- ✓ Include HTML structure stub
- ✓ Test cases for tab cycling, focus restoration, nested modals
- ✓ WCAG citations (2.1.1, 4.1.2, 2.4.3)

## What Would Be Below Expectations

- ✗ No APG Dialog pattern reference
- ✗ Focus trap not documented
- ✗ Focus restoration not mentioned
- ✗ Form structure not specified
- ✗ No keyboard interaction documentation
- ✗ No test cases
- ✗ Missing Escape key handling
