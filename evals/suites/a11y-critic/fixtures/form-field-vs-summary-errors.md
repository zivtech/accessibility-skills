# Fixture: Registration Form with Dual Error Announcement Pattern

## Component Code

```jsx
import React, { useState, useRef } from 'react';

const RegistrationForm = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    displayName: '',
  });
  const [errors, setErrors] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const summaryRef = useRef(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (submitted) {
      setErrors((prev) => {
        const next = { ...prev };
        delete next[name];
        return next;
      });
    }
  };

  const validate = () => {
    const errs = {};
    if (!formData.email) {
      errs.email = 'Email address is required.';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      errs.email = 'Enter a valid email address.';
    }
    if (!formData.password) {
      errs.password = 'Password is required.';
    } else if (formData.password.length < 8) {
      errs.password = 'Password must be at least 8 characters.';
    }
    if (!formData.confirmPassword) {
      errs.confirmPassword = 'Please confirm your password.';
    } else if (formData.confirmPassword !== formData.password) {
      errs.confirmPassword = 'Passwords do not match.';
    }
    if (!formData.displayName) {
      errs.displayName = 'Display name is required.';
    } else if (formData.displayName.length < 2) {
      errs.displayName = 'Display name must be at least 2 characters.';
    }
    return errs;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
    const errs = validate();
    setErrors(errs);
    if (Object.keys(errs).length > 0) {
      summaryRef.current?.focus();
    }
  };

  const fieldDefs = [
    { name: 'email', label: 'Email address', type: 'email' },
    { name: 'password', label: 'Password', type: 'password' },
    { name: 'confirmPassword', label: 'Confirm password', type: 'password' },
    { name: 'displayName', label: 'Display name', type: 'text' },
  ];

  const hasErrors = Object.keys(errors).length > 0;

  return (
    <form onSubmit={handleSubmit} className="reg-form" noValidate>
      <h1>Create your account</h1>

      {/* Error summary — role="alert" announces the full summary on submit */}
      {hasErrors && (
        <div
          ref={summaryRef}
          role="alert"
          className="error-summary"
          tabIndex={-1}
        >
          <h2>There are {Object.keys(errors).length} errors in this form</h2>
          <ul>
            {Object.entries(errors).map(([field, msg]) => (
              <li key={field}>
                <a href={`#field-${field}`}>{msg}</a>
              </li>
            ))}
          </ul>
        </div>
      )}

      {fieldDefs.map(({ name, label, type }) => (
        <div key={name} className="form-group">
          <label htmlFor={`field-${name}`}>{label}</label>
          <input
            id={`field-${name}`}
            name={name}
            type={type}
            value={formData[name]}
            onChange={handleChange}
            aria-invalid={errors[name] ? 'true' : undefined}
            aria-describedby={errors[name] ? `error-${name}` : undefined}
          />
          {/* Inline error — aria-live="polite" announces per-field corrections */}
          <div aria-live="polite" className="inline-error-region">
            {errors[name] && (
              <span id={`error-${name}`} className="error-text">
                {errors[name]}
              </span>
            )}
          </div>
        </div>
      ))}

      <button type="submit" className="submit-btn">
        Create account
      </button>
    </form>
  );
};

export default RegistrationForm;
```

## CSS

```css
.reg-form {
  max-width: 480px;
  margin: 40px auto;
  padding: 32px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.reg-form h1 {
  margin: 0 0 24px;
  font-size: 24px;
  color: #111827;
}

.error-summary {
  background: #fef2f2;
  border: 2px solid #dc2626;
  border-radius: 6px;
  padding: 16px;
  margin-bottom: 24px;
}

.error-summary:focus {
  outline: 3px solid #2563eb;
  outline-offset: 2px;
}

.error-summary h2 {
  margin: 0 0 8px;
  font-size: 16px;
  color: #991b1b;
}

.error-summary ul {
  margin: 0;
  padding-left: 20px;
}

.error-summary a {
  color: #dc2626;
  text-decoration: underline;
}

.error-summary a:hover {
  color: #991b1b;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  font-size: 14px;
  color: #374151;
}

.form-group input {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid #d1d5db;
  border-radius: 6px;
  font-size: 16px;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.form-group input[aria-invalid="true"] {
  border-color: #dc2626;
}

.inline-error-region {
  min-height: 20px;
}

.error-text {
  display: block;
  color: #dc2626;
  font-size: 13px;
  margin-top: 4px;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

.submit-btn:hover {
  background: #1d4ed8;
}

.submit-btn:focus {
  outline: 3px solid #2563eb;
  outline-offset: 2px;
}
```

## Expected Behavior

- Form validates all four fields on submit
- If errors exist, an error summary appears at the top and receives focus
- Error summary lists all errors as links that jump to the corresponding field
- Each invalid field shows an inline error message below the input
- Clearing a field's error on edit removes that inline message
- All fields use `aria-invalid` and `aria-describedby` when in error state

## Accessibility Features Present

✓ `role="alert"` on error summary — announced assertively on appearance
✓ Error summary receives focus via `tabIndex={-1}` and `ref.focus()`
✓ Error summary items are links to fields (`<a href="#field-email">`)
✓ `aria-invalid="true"` set on invalid inputs
✓ `aria-describedby` pointing to inline error message `id`
✓ `aria-live="polite"` wrapper around each inline error message
✓ Proper `<label htmlFor>` associations on every field
✓ Visible focus indicators on all interactive elements
✓ `noValidate` on form — custom validation instead of browser defaults
✓ Semantic form structure with heading

## Design Rationale

The developer followed the GOV.UK Design System error pattern, which recommends:

1. An error summary at the top of the form with links to each invalid field
2. Inline error messages at each field, associated via `aria-describedby`

The implementation adds `role="alert"` to the summary (so the full error list is announced when it appears) and `aria-live="polite"` wrappers around inline errors (so individual corrections are announced as the user fixes fields one at a time).

Both patterns are correctly implemented per their respective APG guidance:
- The error summary follows the "Error Message" pattern with `role="alert"`
- The inline errors follow the "Form Validation" pattern with `aria-describedby` and live region announcements

## Accessibility Issues (None Planted — Design Tension)

**No planted bugs.** This is an ADVERSARIAL fixture: the accessibility question is the design tension analyzed below. Everything from this heading down is eval metadata kept below the blind cut line (runners strip this heading and all following sections from model prompts).

## The Ambiguity

This form uses **both** a form-level error summary with `role="alert"` **and** field-level inline errors inside `aria-live="polite"` regions. Each pattern is correctly implemented. The question is whether using both together creates a better or worse experience for assistive technology users.

**Argument for dual announcements (this implementation is correct):**
- The error summary and inline errors serve different purposes at different moments. On submit, the summary gives an overview of everything wrong. During correction, inline errors announce per-field changes.
- WCAG 3.3.1 (Error Identification) requires that errors be identified and described. Providing errors in two locations ensures coverage regardless of where the user's attention is.
- GOV.UK Design System, one of the most accessibility-tested pattern libraries, explicitly recommends this exact dual approach.
- Users who Tab through the form encounter field-level context via `aria-describedby`. Users who read from the top get the summary. Different navigation strategies are served.
- Focus is moved to the summary on submit, giving the user a clear starting point, but `aria-describedby` ensures context is available when they reach each field.

**Argument against dual announcements (this creates problems):**
- On form submission, the `role="alert"` summary fires immediately and a screen reader announces the full error list. But the inline error messages also appear simultaneously inside `aria-live="polite"` regions — queuing additional announcements. The user hears the summary, then hears each error message again individually as the live regions populate.
- For a form with 4 errors, the user may hear 8 separate announcements: 4 from the summary alert, then 4 from the live regions. This is disorienting, especially under time pressure.
- Users with cognitive disabilities may struggle to distinguish summary announcements from field-level announcements, uncertain whether these are the same errors or different ones.
- The `aria-live="polite"` regions are primarily valuable for **real-time correction** (clearing errors one at a time), but they also fire on initial error display, creating the double-announcement on submit.
- A simpler approach — error summary with `role="alert"` only, inline errors associated via `aria-describedby` but without `aria-live` — would eliminate the double announcement while preserving all the field-level context.

**Why this is genuinely hard:**
Both patterns are individually correct. The summary-with-alert is correct. The inline-errors-with-live-region is correct. The question is an interaction effect: when both fire simultaneously on the same validation event, the combined experience may be worse than either alone. But removing either pattern also removes a real benefit. The "simpler approach" (drop `aria-live` from inline errors) trades announcement redundancy for losing real-time correction feedback. There is no costless answer.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Notes

This is an ADVERSARIAL fixture. The "correct" review is NOT to flag either error pattern as broken, but to:

1. Recognize that both the error summary and inline error patterns are correctly implemented individually
2. Articulate the specific tension: dual `role="alert"` + `aria-live="polite"` firing simultaneously causes redundant announcements on submit
3. Explain who benefits from the dual pattern (users correcting fields one at a time) and who is burdened by it (users hearing the initial error blast)
4. Make a recommendation acknowledging the tradeoff — whether to keep both, remove `aria-live` from inline errors, or conditionally suppress live announcements on initial submission
5. Avoid claiming either pattern is "wrong" — the issue is the interaction between two correct patterns

A reviewer that says "remove role='alert' from the summary" is wrong — it is correctly implemented. A reviewer that says "remove aria-live from inline errors" may be right but only if they acknowledge what is lost. A reviewer that says "this is fine" without noting the double-announcement issue is incomplete.
