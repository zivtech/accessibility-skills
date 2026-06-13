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

  const clearFieldError = (field) =>
    setErrors((prev) => {
      if (!prev[field]) return prev;
      const next = { ...prev };
      delete next[field];
      return next;
    });

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
            onChange={(e) => { setEmail(e.target.value); clearFieldError('email'); }}
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
            onChange={(e) => { setPassword(e.target.value); clearFieldError('password'); }}
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
