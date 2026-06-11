# Modal Dialog With Broken Focus Trap

## Description

React modal dialog with form content. Focus not moved on open, no focus trap, no role="dialog" or aria-modal, close button has no accessible label, Escape doesn't close.

## Expected Behavior

- Clicking "Subscribe Now" opens the modal
- Focus moves automatically into the modal on open (first focusable element or modal heading)
- Tab cycles only among focusable elements inside the modal — background links are unreachable
- Shift+Tab wraps backward within the modal
- Escape closes the modal
- When modal closes, focus returns to the "Subscribe Now" trigger button
- Screen reader announces "Subscribe to Updates, dialog" on open

## Accessibility Features Present

- Trigger button uses `aria-haspopup="dialog"` correctly
- Form inputs have visible labels correctly associated via `htmlFor`/`id`
- `aria-required="true"` on both required inputs
- All interactive controls are real `<button>` or `<input>` elements
- Visible focus indicators on all interactive elements
- Visual backdrop overlay dims background content
- `triggerRef` is attached to the trigger button (though never used for focus restoration)
- Submit and Cancel buttons are real `<button>` elements with correct `type` attributes

---

_This directory contains component files extracted from the a11y eval suite for chain evaluation._
_Run `/a11y-workflow full evals/suites/chain/targets/modal-broken-focus-trap/component.jsx` to start the chain._
