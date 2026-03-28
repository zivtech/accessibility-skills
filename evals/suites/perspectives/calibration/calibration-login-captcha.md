# Calibration Fixture C2: Login Form With CAPTCHA

## Component Code

```jsx
import React, { useState } from 'react';

const LoginForm = ({ onSubmit, captchaSiteKey }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState({});
  const [captchaToken, setCaptchaToken] = useState(null);

  const validate = () => {
    const newErrors = {};
    if (!email) newErrors.email = 'Email is required';
    if (!password) newErrors.password = 'Password is required';
    if (password && password.length < 8) newErrors.password = 'Password must be at least 8 characters';
    if (!captchaToken) newErrors.captcha = 'Please complete the CAPTCHA';
    return newErrors;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const newErrors = validate();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    onSubmit({ email, password, captchaToken });
  };

  return (
    <main>
      <form onSubmit={handleSubmit} aria-label="Login" noValidate>
        <h1>Sign In</h1>

        <div className="field">
          <label htmlFor="email">Email address</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            aria-describedby={errors.email ? 'email-error' : undefined}
            aria-invalid={!!errors.email}
            autoComplete="email"
          />
          {errors.email && (
            <p id="email-error" className="error" role="alert">{errors.email}</p>
          )}
        </div>

        <div className="field">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            aria-describedby={errors.password ? 'password-error' : undefined}
            aria-invalid={!!errors.password}
            autoComplete="current-password"
          />
          {errors.password && (
            <p id="password-error" className="error" role="alert">{errors.password}</p>
          )}
        </div>

        {/* Third-party visual CAPTCHA — the accessibility challenge */}
        <div className="captcha-container">
          <div
            id="captcha-widget"
            data-sitekey={captchaSiteKey}
            data-callback="onCaptchaSuccess"
            aria-label="CAPTCHA verification"
          >
            {/* Rendered by third-party CAPTCHA script */}
            {/* Typically an image challenge or checkbox */}
          </div>
          {errors.captcha && (
            <p id="captcha-error" className="error" role="alert">{errors.captcha}</p>
          )}
        </div>

        <button type="submit">Sign In</button>

        <p className="help-text">
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

## Component Description

A login form with email, password, and a third-party visual CAPTCHA widget. The form has proper labels, error handling with aria-describedby, and autocomplete attributes. The CAPTCHA is the primary accessibility concern — it creates barriers for cognitive users (puzzle-solving under time pressure), keyboard users (third-party widget may not be keyboard-operable), and screen reader users (image challenges are not accessible).

## Why This Is a Calibration Fixture

Login forms with CAPTCHA are a well-understood accessibility anti-pattern. The escalation mechanism should correctly identify Cognitive and Keyboard as HIGH (CAPTCHA is a known barrier), Screen Reader as MEDIUM (the form itself is accessible but CAPTCHA widget accessibility depends on the third-party), and other perspectives as LOW (no media, no animation, no color-only information).

## Expected Alarm Levels

| Perspective | Expected Level | Rationale |
|---|---|---|
| Magnification & Reflow | LOW | Simple single-column form, no fixed layout issues |
| Environmental Contrast | LOW | Standard form elements, no color-coded information |
| Vestibular & Motion | LOW | No animation, no auto-playing content |
| Auditory Access | LOW | No audio or video content |
| Keyboard & Motor | HIGH | CAPTCHA may trap keyboard users; third-party widget keyboard support unknown |
| Screen Reader & Semantic | MEDIUM | Form semantics are good but CAPTCHA widget AT support is uncertain |
| Cognitive & Neurodivergent | HIGH | CAPTCHA requires puzzle-solving under time pressure; password complexity rules |
