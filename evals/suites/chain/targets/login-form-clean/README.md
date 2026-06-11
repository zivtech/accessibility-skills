# Login Form With Complete Accessibility (CLEAN)

## Description

React login form with email, password, remember-me, and forgot-password link. All labels matched, aria-describedby on errors, role='alert', aria-invalid, aria-required, autocomplete, visible focus styles.

## Expected Behavior

- Login form with email, password, remember-me checkbox, and submit button
- Client-side validation on submit
- Error summary appears with links to offending fields
- Individual field errors appear below each input
- "Forgot password" and "Create account" links available

## Accessibility Features Present

- `<label>` with matching `htmlFor`/`id` on all fields
- `aria-describedby` links inputs to error messages
- `aria-invalid` toggles on validation failure
- `aria-required="true"` on required fields
- `autoComplete` attributes (`email`, `current-password`)
- Error summary with `role="alert"` for screen reader announcement
- Error summary links navigate to fields via `<a href="#fieldId">`
- All color contrast meets WCAG AA (ratios documented in CSS comments)
- All links are underlined
- Focus-visible outlines on all interactive elements
- `<main>` landmark, `<form>` with `aria-label`
- Heading hierarchy (h1 for page, h2 for error summary)
- Submit button is `type="submit"` for Enter key support

---

_This directory contains component files extracted from the a11y eval suite for chain evaluation._
_Run `/a11y-workflow full evals/suites/chain/targets/login-form-clean/component.jsx` to start the chain._
