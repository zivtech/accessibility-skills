# Fixture: Simple Button Navigation

## Feature Description

You're planning accessibility for a simple button bar containing 3 action buttons arranged horizontally:
- "Save" button
- "Cancel" button
- "Delete" button
- Each button has an icon + text label
- Buttons are statically positioned (no dynamic addition/removal)
- Buttons have hover and active states
- Each button has a different action

## Context

- **Platform:** Web application
- **Existing code:** No, new component
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA, keyboard-only users
- **Scope:** Simple 3-button bar (reusable)
- **Constraints:** Icon-only buttons (need accessible labels)

## Requirement

Create a concise accessibility design plan for a simple button bar covering:
- HTML button elements with proper labels
- Tab order (left-to-right)
- Focus indicator contrast (3:1 minimum)
- Icon accessibility (alt text or aria-label)
- Keyboard activation (Enter/Space)
- Visual distinction of action buttons (danger vs normal)
- Testing strategy

## Scope Hints

This is a **TRIVIAL** difficulty fixture. Plan should be 1-2 pages:

1. Button semantics (native HTML button)
2. Icon labels (aria-label or alt)
3. Tab order (natural left-to-right)
4. Focus indicator visibility (3:1 contrast)
5. Keyboard activation (Enter/Space)
6. Visual button styling
7. Test cases (keyboard, focus, screen reader)

## What Success Looks Like

- ✓ Native HTML button elements
- ✓ Icon labels with aria-label or accessible text
- ✓ Focus indicator contrast specified (3:1)
- ✓ WCAG 2.1.1 citation for keyboard support
- ✓ Keyboard interactions documented (Enter/Space)
- ✓ Visual styling plan
- ✓ Simple test cases

## What Would Be Below Expectations

- ✗ Using div instead of button element
- ✗ No labels for icons
- ✗ No focus indicator planning
- ✗ No WCAG citations
- ✗ Vague button styling
