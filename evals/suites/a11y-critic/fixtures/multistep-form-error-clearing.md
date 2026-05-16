# Fixture: Multi-Step Form Wizard with Error Clearing Gaps

## Component Code

```jsx
import React, { useState, useRef } from 'react';

const STEPS = ['Personal Info', 'Address', 'Confirm'];

const MultiStepForm = () => {
  const [step, setStep] = useState(0);
  const [data, setData] = useState({ name: '', email: '', street: '', zip: '' });
  const [errors, setErrors] = useState({});
  const liveRef = useRef(null);

  const update = (e) => {
    const { name, value } = e.target;
    setData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      const next = { ...errors };
      delete next[name];
      setErrors(next);
    }
  };

  const validate = () => {
    const errs = {};
    if (step === 0) {
      if (!data.name.trim()) errs.name = 'Full name is required.';
      if (!data.email.includes('@')) errs.email = 'Enter a valid email address.';
    } else if (step === 1) {
      if (!data.street.trim()) errs.street = 'Street address is required.';
      if (!/^\d{5}$/.test(data.zip)) errs.zip = 'ZIP code must be 5 digits.';
    }
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };
  const next = () => { if (validate()) setStep(s => Math.min(s + 1, 2)); };
  const back = () => { setErrors({}); setStep(s => Math.max(s - 1, 0)); };
  const hasErrors = Object.keys(errors).length > 0;
  return (
    <form onSubmit={e => { e.preventDefault(); }} className="wizard-form" noValidate>
      <div className="step-indicator" role="group" aria-label="Form progress">
        {STEPS.map((label, i) => (
          <span key={label}
            className={`step-dot ${i === step ? 'active' : ''} ${i < step ? 'done' : ''}`}>
            {label} ({i + 1} of {STEPS.length})
          </span>
        ))}
      </div>
      <div ref={liveRef} aria-live="polite" className="error-region">
        {hasErrors && (
          <ul className="error-list">
            {Object.entries(errors).map(([k, msg]) => <li key={k}>{msg}</li>)}
          </ul>
        )}
      </div>
      <div className={step === 0 ? 'step-panel' : 'step-hidden'}
           aria-hidden={step !== 0 ? 'true' : undefined}>
        <h2>Personal Information</h2>
        <div className="field-group">
          <label htmlFor="name">Full Name</label>
          <input id="name" name="name" type="text" value={data.name}
            onChange={update} aria-invalid={!!errors.name}
            aria-describedby={errors.name ? 'err-name' : undefined} />
          {errors.name && <span id="err-name" className="field-error">{errors.name}</span>}
        </div>
        <div className="field-group">
          <label htmlFor="email">Email Address</label>
          <input id="email" name="email" type="email" value={data.email}
            onChange={update} aria-invalid={!!errors.email}
            aria-describedby={errors.email ? 'err-email' : undefined} />
          {errors.email && <span id="err-email" className="field-error">{errors.email}</span>}
        </div>
      </div>
      <div className={step === 1 ? 'step-panel' : 'step-hidden'}
           aria-hidden={step !== 1 ? 'true' : undefined}>
        <h2>Address</h2>
        <div className="field-group">
          <label htmlFor="street">Street Address</label>
          <input id="street" name="street" type="text" value={data.street}
            onChange={update} aria-invalid={!!errors.street}
            aria-describedby={errors.street ? 'err-street' : undefined} />
          {errors.street && <span id="err-street" className="field-error">{errors.street}</span>}
        </div>
        <div className="field-group">
          <label htmlFor="zip">ZIP Code</label>
          <input id="zip" name="zip" type="text" inputMode="numeric" value={data.zip}
            onChange={update} aria-invalid={!!errors.zip}
            aria-describedby={errors.zip ? 'err-zip' : undefined} />
          {errors.zip && <span id="err-zip" className="field-error">{errors.zip}</span>}
        </div>
      </div>
      {step === 2 && (
        <div className="step-panel">
          <h2>Confirm Your Information</h2>
          <dl className="review-list">
            <dt>Name</dt><dd>{data.name}</dd>
            <dt>Email</dt><dd>{data.email}</dd>
            <dt>Address</dt><dd>{data.street}, {data.zip}</dd>
          </dl>
        </div>
      )}
      <div className="button-bar">
        {step > 0 && (
          <button type="button" className="btn-back" onClick={back}>Back</button>
        )}
        {step < 2 ? (
          <button type="button" className="btn-next" disabled={hasErrors}
            onClick={next}>Next</button>
        ) : (
          <button type="submit" className="btn-submit">Submit</button>
        )}
      </div>
    </form>
  );
};

export default MultiStepForm;
```

## CSS

```css
.wizard-form {
  max-width: 560px;
  margin: 32px auto;
  padding: 24px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.step-indicator {
  display: flex;
  justify-content: space-between;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e2e8f0;
}

.step-dot {
  font-size: 13px;
  color: #94a3b8;
  padding: 4px 12px;
  border-radius: 16px;
  background: #f8fafc;
}

.step-dot.active {
  color: #1e40af;
  background: #dbeafe;
  font-weight: 600;
}

.step-dot.completed {
  color: #059669;
  background: #d1fae5;
}

.error-region {
  min-height: 0;
}

.error-list {
  background: #fef2f2;
  border: 2px solid #dc2626;
  border-radius: 6px;
  padding: 12px 12px 12px 32px;
  margin: 0 0 16px 0;
  color: #991b1b;
  font-size: 14px;
}

.error-list li {
  margin-bottom: 4px;
}

.step-panel {
  margin-bottom: 24px;
}

.step-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
}

.step-panel h2,
.step-hidden h2 {
  font-size: 20px;
  margin: 0 0 16px;
  color: #1e293b;
}

.field-group {
  margin-bottom: 16px;
}

.field-group label {
  display: block;
  margin-bottom: 4px;
  font-weight: 600;
  font-size: 14px;
  color: #334155;
}

.field-group input[type="text"],
.field-group input[type="email"],
.field-group input[type="tel"] {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid #cbd5e1;
  border-radius: 6px;
  font-size: 16px;
  box-sizing: border-box;
}

.field-group input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

.field-group input[aria-invalid="true"] {
  border-color: #dc2626;
}

.field-error {
  display: block;
  color: #dc2626;
  font-size: 13px;
  margin-top: 4px;
}

.review-list {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 8px 16px;
  font-size: 15px;
}

.review-list dt {
  font-weight: 600;
  color: #475569;
}

.review-list dd {
  margin: 0;
  color: #1e293b;
}

.button-bar {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.btn-back {
  padding: 10px 20px;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 15px;
  cursor: pointer;
  color: #475569;
}

.btn-back:hover {
  background: #e2e8f0;
}

.btn-back:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

.btn-next,
.btn-submit {
  padding: 10px 24px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  margin-left: auto;
}

.btn-next:hover,
.btn-submit:hover {
  background: #1d4ed8;
}

.btn-next:focus,
.btn-submit:focus {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}

.btn-next:disabled {
  background: #94a3b8;
  cursor: not-allowed;
  opacity: 0.6;
}
```

## Expected Behavior

- User fills out fields on each step and clicks "Next" to advance
- Validation runs on "Next" click; errors appear in a live region and inline
- When the user fixes a field, inline error disappears and the error summary updates
- Screen reader users are informed of both errors appearing AND errors resolving
- "Next" button remains discoverable and explains why progression is blocked
- Step indicator communicates current position to all users
- Inactive steps are fully hidden from assistive technology

## Accessibility Features Present

These features are correctly implemented and should NOT be flagged:

- Labels associated via htmlFor on every input
- aria-invalid toggles with error state on each field
- aria-describedby links each input to its inline error span when the error exists
- aria-live="polite" region wraps the error summary list
- Error messages are specific ("Full name is required" not just "Error")
- Visible focus indicators on all interactive elements (2px solid blue)
- Semantic form structure with headings per step
- noValidate on form to prevent browser-native validation conflicts
- Back button available on steps 2 and 3

## Accessibility Issues (Planted)

1. **MUST-FIND / MAJOR: Error clearance is silent to screen readers** — The error summary lives inside an `aria-live="polite"` region. When validation fails, error text is injected and screen readers announce it. When the user fixes a field, `handleChange` removes that error from state, the error `<li>` is removed from the DOM, and the live region's text content shrinks or empties. Screen readers do NOT announce text removal from live regions — they only announce text additions. The user gets no auditory confirmation that their fix worked. They must either re-navigate to the error region to discover it's empty, or press "Next" again and hope for the best.
   - Evidence: `multistep-form-error-clearing.md` lines 19-23: `update` handler deletes the error from state. Lines 51-57: the live region conditionally renders error items — when errors clear, the content simply disappears.
   - WCAG: 4.1.3 Status Messages (status changes, including resolution, must be communicated to AT)
   - APG: Forms Pattern — "Provide feedback when errors are corrected"
   - User group: Screen reader users (critical — no feedback loop on error resolution)
   - Impact: User cannot determine whether their correction was successful without re-navigating or re-submitting. On a multi-field step with several errors, this creates a "fix and guess" loop.
   - Fix: When an error clears, inject a brief confirmation message into the live region (e.g., "Email error resolved") before removing the error text, or maintain a persistent status like "No errors" / "All errors resolved" that replaces the error list.

2. **SHOULD-FIND / MAJOR: "Next" button uses `disabled` attribute, removing it from tab order** — When validation errors exist, the Next button gets `disabled={hasErrors}`, which applies the HTML `disabled` attribute. Disabled elements are removed from the tab order and are not focusable. A screen reader user who tabs through the form will skip directly from the last field to the Back button (or out of the form). The Next button is invisible to them. They cannot discover WHY they are stuck — the button that should explain the block is unreachable.
   - Evidence: `multistep-form-error-clearing.md` lines 109-110: `disabled={hasErrors}` on the Next button.
   - WCAG: 4.1.2 Name, Role, Value (interactive element state must be perceivable); 3.3.3 Error Suggestion (user should understand how to fix errors)
   - APG: "Use `aria-disabled='true'` instead of the HTML `disabled` attribute when the disabled state needs to remain discoverable"
   - User group: Screen reader users, keyboard-only users (cannot discover the blocked button)
   - Impact: Users who rely on tab order to discover interface state will not know the Next button exists while errors are present. Combined with bug #1 (silent error clearing), this creates a dead end — the user fixes errors but gets no confirmation, and the button they need is missing from the tab order.
   - Fix: Replace `disabled={hasErrors}` with `aria-disabled={hasErrors ? 'true' : undefined}`. Keep the button focusable. Add an `aria-describedby` pointing to the error summary or a hidden message like "Fix errors above to continue." Prevent the click handler from firing when `aria-disabled` is true.

3. **NICE-TO-FIND / MINOR: Step indicator does not communicate current step to screen readers** — The step indicator shows "Personal Info (1 of 3)" for each step, and the active step gets a visual `.active` class (blue background). But no `aria-current="step"` is set on the active indicator. Screen reader users navigating the step indicator hear all three labels identically — they cannot determine which step is current without reading the visual styling.
   - Evidence: `multistep-form-error-clearing.md` lines 43-50: step dots use className for visual state but no aria-current attribute.
   - WCAG: 1.3.1 Info and Relationships (visual state must be conveyed programmatically)
   - User group: Screen reader users (low-friction — they can infer from heading, but indicator itself is ambiguous)
   - Impact: Minor. The step heading ("Personal Information", "Address") provides context. But the progress indicator, which sighted users rely on for orientation, conveys nothing to SR users beyond the text labels.
   - Fix: Add `aria-current={i === step ? 'step' : undefined}` to the active step span.

4. **NICE-TO-FIND / MINOR: Inactive step panels are visually hidden but inputs remain keyboard-focusable** — Inactive steps use `aria-hidden="true"` combined with a CSS clip pattern (`.step-hidden`) to move them off-screen. However, `aria-hidden` does not affect tab order. The inputs inside hidden panels retain their default tabindex and are still focusable via Tab. A keyboard user tabbing through the active step will tab past the last visible field and into invisible inputs on a hidden step — they can type into fields they cannot see. Screen readers in browse/forms mode may also navigate into `aria-hidden` subtrees on some browser/AT combinations.
   - Evidence: `multistep-form-error-clearing.md` lines 58-93: inactive panels get `aria-hidden="true"` and `.step-hidden` class (off-screen clip), but child inputs retain their default tabindex. No `disabled`, `tabindex="-1"`, or `inert` attribute prevents keyboard access.
   - WCAG: 2.4.3 Focus Order (focusable elements should follow visible content sequence); 1.3.2 Meaningful Sequence
   - User group: Keyboard-only users (tab into invisible fields), screen reader users (AT may expose aria-hidden subtrees)
   - Impact: Low in practice because the number of hidden fields is small, but the failure mode is real: focus disappears into off-screen inputs. The `inert` attribute (now well-supported) is the robust fix — it prevents both AT exposure and keyboard focus.
   - Fix: Add `inert` attribute to inactive step panels: `inert={step !== 0 ? true : undefined}`. Or use `display: none` if the off-screen positioning pattern is not required for animation.

## Difficulty Level

**FLAWED** — The surface looks competent: labeled inputs, aria-invalid, aria-describedby, a live region for errors, arrow key support implicit in browser form navigation, semantic headings. A reviewer who checks for the "usual suspects" (missing labels, missing live region, missing aria-invalid) will find everything in order. The bugs are in what happens AFTER the obvious: what occurs when an error is resolved (silence), what happens to the Next button when errors exist (vanishes from tab order), and whether the step indicator conveys its visual state.

Expected baseline detection: 15-35%. Zero-shot reviewers will see the aria-live region, see errors being announced, and move on. They won't trace what happens when the error text is REMOVED from the live region. The disabled-button issue requires understanding the difference between `disabled` and `aria-disabled` — a distinction many developers (and reviewers) conflate.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Notes

This fixture tests four distinct reviewer capabilities:

1. **Temporal interaction tracing** (must_find) — Can the critic trace the FULL lifecycle of an error, including what happens when it resolves? Most reviewers stop at "errors are announced" without checking "error resolution is announced."

2. **Disabled vs. aria-disabled distinction** (should_find) — Can the critic distinguish between an element being disabled (removed from interaction entirely) and an element being aria-disabled (still discoverable but inoperable)? This is a nuanced but consequential difference for screen reader discoverability.

3. **Progressive indicator semantics** (nice_to_find) — Does the critic check that visual progress indicators have programmatic equivalents? `aria-current="step"` is not widely known.

4. **Hiding mechanism analysis** (nice_to_find) — Does the critic recognize that `aria-hidden` does not affect keyboard tab order? The hidden panels are off-screen but their inputs remain focusable — keyboard users can tab into invisible fields. The `inert` attribute or `display: none` would prevent this.

The compound effect of bugs #1 and #2 is the real test: a screen reader user who hits errors cannot tell when they have fixed them (bug #1), and the button they need to proceed has vanished (bug #2). Together, these create a dead end that neither bug alone would produce.
