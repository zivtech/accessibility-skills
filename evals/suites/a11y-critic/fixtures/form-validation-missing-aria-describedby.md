# Fixture: Form with Validation Errors Not Associated with Fields

## Component Code

```jsx
import React, { useState } from 'react';

const LoginForm = () => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!formData.email.includes('@')) {
      newErrors.email = 'Email must be valid';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      console.log('Form submitted:', formData);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="login-form">
      <h1>Login</h1>

      {/* BUG: Error messages exist but aren't announced as live region */}
      {Object.keys(errors).length > 0 && (
        <div className="error-summary">
          <h2>Please fix the following errors:</h2>
          <ul>
            {Object.entries(errors).map(([field, message]) => (
              <li key={field}>{message}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="form-group">
        <label htmlFor="email">Email Address</label>
        <input
          id="email"
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          className={errors.email ? 'error' : ''}
          aria-invalid={errors.email ? true : false}
          // BUG: No aria-describedby pointing to error message
        />
        {/* Error message exists but not associated to input */}
        {errors.email && <span className="error-text">{errors.email}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          className={errors.password ? 'error' : ''}
          aria-invalid={errors.password ? true : false}
          // BUG: No aria-describedby pointing to error message
        />
        {/* Error message exists but not associated to input */}
        {errors.password && <span className="error-text">{errors.password}</span>}
      </div>

      <button type="submit" className="submit-button">
        Log In
      </button>
    </form>
  );
};

export default LoginForm;
```

## CSS

```css
.login-form {
  max-width: 400px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.login-form h1 {
  margin-top: 0;
  color: #333;
}

.error-summary {
  background-color: #fee;
  border: 2px solid #c33;
  border-radius: 4px;
  padding: 16px;
  margin-bottom: 20px;
}

.error-summary h2 {
  margin: 0 0 8px 0;
  color: #c33;
  font-size: 18px;
}

.error-summary ul {
  margin: 0;
  padding-left: 20px;
  color: #c33;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 2px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #0066cc;
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.form-group input.error {
  border-color: #c33;
}

.error-text {
  display: block;
  color: #c33;
  font-size: 14px;
  margin-top: 4px;
}

.submit-button {
  width: 100%;
  padding: 12px;
  background-color: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-button:hover {
  background-color: #004499;
}

.submit-button:focus {
  outline: 3px solid #0066cc;
  outline-offset: 2px;
}
```

## Expected Behavior

- Form validates on submit
- Errors display in summary at top
- Individual fields show error messages below
- aria-invalid marks invalid fields
- Form is keyboard navigable

## Accessibility Features Present

✓ Label associated via htmlFor
✓ aria-invalid toggles with error state
✓ Error messages displayed (visually)
✓ Focus indicators visible
✓ Semantic form structure

## Accessibility Issues (Planted)

1. **CRITICAL: Error messages not associated with form inputs via aria-describedby** — Although errors are displayed and aria-invalid is set, the input has no aria-describedby attribute pointing to the error message. Screen reader user hears "Email Address, invalid" but doesn't hear what's wrong.
   - Evidence: `form-validation-missing-aria-describedby.md:72-82` (aria-invalid without aria-describedby; error message ID not linked)
   - WCAG citation: 1.3.1 Info and Relationships (error must be associated with field), 4.1.2 Name, Role, Value
   - User group: Screen reader users
   - Expected: Inputs should have aria-describedby="error-email" (or similar) pointing to error message element with matching id
   - Fix: Add id to each error message (id="error-email"), add aria-describedby to input pointing to it

2. **MAJOR: Error messages not announced as live region** — Error summary exists but doesn't have aria-live, so users who have form already loaded don't hear when validation fails. aria-live="polite" needed on error summary.
   - Evidence: `form-validation-missing-aria-describedby.md:19-26` (error-summary div has no aria-live or role="status")
   - WCAG citation: 4.1.3 Status Messages (dynamic content updates should be announced)
   - User group: Screen reader users
   - Expected: Error summary should have role="alert" or aria-live="polite"
   - Fix: Add aria-live="polite" aria-atomic="true" to error summary div

3. **MINOR: Error summary doesn't link to specific fields** — While the summary lists which fields have errors, there's no way to jump from summary to field. Cognitive users might appreciate links from error summary to fields.
   - Evidence: `form-validation-missing-aria-describedby.md:19-26` (list items are plain text, not links)
   - Severity: ENHANCEMENT for most, MINOR for cognitive users
   - Fix: Optional: Make error messages in summary clickable links to fields

## Difficulty Level

**HAS-BUGS** — Clear pattern incompleteness. The form has proper labels and visual error indication, but the programmatic association between errors and fields is missing. This is a very common real-world issue: visual design is correct but accessible name/description relationships are incomplete.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Notes

This fixture tests whether a11y-critic catches the difference between:
- **Visual presentation** (error message shown near field) ✓
- **Programmatic association** (aria-describedby linking error to field) ✗

Baseline might miss this because the error messages are visible. A11y-critic should identify this as a critical gap in the semantic relationship between error and field.
