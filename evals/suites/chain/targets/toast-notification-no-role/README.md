# Toast Notification Without Alert Role

## Description

Toast notification with auto-dismiss but missing role="alert", aria-live, and manual dismiss option.

## Expected Behavior

- Toast appears and automatically dismisses after 3 seconds
- Screen reader announces toast message immediately
- Message is announced with alert priority
- Keyboard user can dismiss toast if needed
- Visual indicator shows toast type (success, error, etc.)

## Accessibility Features Present

✓ Automatic dismissal timer
✓ Visual styling

---

_This directory contains component files extracted from the a11y eval suite for chain evaluation._
_Run `/a11y-workflow full evals/suites/chain/targets/toast-notification-no-role/component.jsx` to start the chain._
