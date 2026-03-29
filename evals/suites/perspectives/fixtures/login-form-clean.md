# Fixture: Login Form With Complete Accessibility (CLEAN)

## Component Code

```jsx
import React, { useState } from 'react';

const LoginForm = ({ onSubmit }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [errors, setErrors] = useState({});
  const [submitted, setSubmitted] = useState(false);

  const validate = () => {
    const errs = {};
    if (!email) errs.email = 'Email address is required.';
    else if (!/\S+@\S+\.\S+/.test(email)) errs.email = 'Please enter a valid email address.';
    if (!password) errs.password = 'Password is required.';
    else if (password.length < 8) errs.password = 'Password must be at least 8 characters.';
    return errs;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const errs = validate();
    setErrors(errs);
    setSubmitted(true);
    if (Object.keys(errs).length === 0) {
      onSubmit?.({ email, password, rememberMe });
    }
  };

  return (
    <main className="login-page">
      <form onSubmit={handleSubmit} aria-label="Sign in" noValidate>
        <h1>Sign In</h1>

        {submitted && Object.keys(errors).length > 0 && (
          <div role="alert" className="error-summary">
            <h2>Please fix the following errors:</h2>
            <ul>
              {Object.entries(errors).map(([field, msg]) => (
                <li key={field}><a href={`#${field}`}>{msg}</a></li>
              ))}
            </ul>
          </div>
        )}

        <div className="form-field">
          <label htmlFor="email">Email address</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            aria-describedby={errors.email ? 'email-error' : undefined}
            aria-invalid={submitted && !!errors.email}
            aria-required="true"
            autoComplete="email"
          />
          {errors.email && (
            <p id="email-error" className="field-error">{errors.email}</p>
          )}
        </div>

        <div className="form-field">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            aria-describedby={errors.password ? 'password-error' : undefined}
            aria-invalid={submitted && !!errors.password}
            aria-required="true"
            autoComplete="current-password"
          />
          {errors.password && (
            <p id="password-error" className="field-error">{errors.password}</p>
          )}
        </div>

        <div className="form-field checkbox-field">
          <input
            id="remember"
            type="checkbox"
            checked={rememberMe}
            onChange={(e) => setRememberMe(e.target.checked)}
          />
          <label htmlFor="remember">Remember me</label>
        </div>

        <button type="submit" className="submit-btn">Sign In</button>

        <p className="help-links">
          <a href="/forgot-password">Forgot password?</a>
          {' | '}
          <a href="/register">Create account</a>
        </p>
      </form>
    </main>
  );
};

export default LoginForm;
```

```css
.login-page {
  max-width: 400px;
  margin: 40px auto;
  padding: 32px;
  font-family: system-ui, sans-serif;
}

.login-page h1 {
  font-size: 1.75rem;
  margin-bottom: 24px;
  color: #111;           /* #111 on white = 18.4:1 */
}

.error-summary {
  border: 2px solid #b71c1c;
  border-radius: 4px;
  padding: 12px 16px;
  background: #fff3f3;
  margin-bottom: 20px;
}

.error-summary h2 {
  font-size: 1rem;
  color: #b71c1c;        /* #b71c1c on #fff3f3 ≈ 6.0:1 */
  margin: 0 0 8px;
}

.error-summary ul { margin: 0; padding-left: 20px; }

.error-summary a {
  color: #b71c1c;
  text-decoration: underline;
}

.error-summary a:focus {
  outline: 3px solid #b71c1c;
  outline-offset: 2px;
}

.form-field {
  margin-bottom: 16px;
}

.form-field label {
  display: block;
  font-weight: 600;
  margin-bottom: 4px;
  color: #222;            /* #222 on white = 14.7:1 */
}

.form-field input[type="email"],
.form-field input[type="password"] {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid #767676;  /* #767676 on white = 4.54:1 — passes AA for UI components */
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

.form-field input:focus {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}

.form-field input[aria-invalid="true"] {
  border-color: #b71c1c;
}

.field-error {
  color: #b71c1c;
  font-size: 0.875rem;
  margin: 4px 0 0;
}

.checkbox-field {
  display: flex;
  align-items: center;
  gap: 8px;
}

.checkbox-field input { width: auto; }

.submit-btn {
  width: 100%;
  padding: 12px;
  background: #1565c0;   /* #1565c0 on white bg, but text is white: #fff on #1565c0 = 5.4:1 */
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 8px;
}

.submit-btn:hover { background: #0d47a1; }
.submit-btn:focus-visible { outline: 3px solid #005fcc; outline-offset: 2px; }

.help-links {
  margin-top: 16px;
  text-align: center;
  font-size: 0.9rem;
}

.help-links a {
  color: #1565c0;        /* #1565c0 on white = 5.4:1 */
  text-decoration: underline;
}

.help-links a:focus {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}
```

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

## Accessibility Issues

**NONE.** This is a clean, well-implemented login form. All accessibility features are correctly implemented.

Optional enhancements a reviewer MAY note (ENHANCEMENT severity only):
1. Could add `aria-live="polite"` to error summary region for more reliable announcement timing
2. Could add a show/hide password toggle for usability

## Difficulty Level

**CLEAN** — This form correctly implements all common accessibility patterns. A competent reviewer should produce ACCEPT or ACCEPT-WITH-RESERVATIONS. Used to measure false-positive rate.

## Frameworks

React 18+, CSS
