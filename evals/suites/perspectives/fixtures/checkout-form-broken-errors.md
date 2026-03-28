# Fixture: Multi-Step Checkout Form With Broken Error Association

## Component Code

```jsx
import React, { useState } from 'react';

const STEPS = ['Shipping', 'Payment', 'Review'];

const CheckoutForm = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [errors, setErrors] = useState({});
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    address: '',
    city: '',
    cardNumber: '',
    cardExpiry: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const validateStep = (step) => {
    const newErrors = {};
    if (step === 0) {
      if (!formData.firstName) newErrors.firstName = 'First name is required';
      if (!formData.lastName) newErrors.lastName = 'Last name is required';
      if (!formData.address) newErrors.address = 'Address is required';
      if (!formData.city) newErrors.city = 'City is required';
    }
    if (step === 1) {
      if (!formData.cardNumber) newErrors.cardNumber = 'Card number is required';
      if (!formData.cardExpiry) newErrors.cardExpiry = 'Expiry date is required';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleNext = () => {
    if (validateStep(currentStep)) {
      setCurrentStep(prev => prev + 1);
      setErrors({});
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateStep(currentStep)) {
      alert('Order placed!');
    }
  };

  return (
    <div className="checkout-wrapper">

      {/* BUG: Step indicator uses color only — no text or icon supplement */}
      <ol className="step-indicator" aria-label="Checkout steps">
        {STEPS.map((step, idx) => (
          <li
            key={step}
            className={idx < currentStep ? 'complete' : idx === currentStep ? 'active' : 'upcoming'}
          >
            {step}
          </li>
        ))}
      </ol>

      {/* BUG: Error summary exists but list items have no href — cannot navigate to fields */}
      {Object.keys(errors).length > 0 && (
        <div className="error-summary">
          <h2 id="error-summary-heading">Please fix the following errors:</h2>
          <ul aria-labelledby="error-summary-heading">
            {Object.entries(errors).map(([field, message]) => (
              // BUG: plain <li> instead of <li><a href="#field-id">...</a></li>
              <li key={field}>{message}</li>
            ))}
          </ul>
        </div>
        // BUG: no aria-live on this region — won't announce to screen reader
      )}

      <form onSubmit={handleSubmit} noValidate>

        {currentStep === 0 && (
          <fieldset>
            <legend>Shipping Information</legend>

            <div className="form-group">
              {/* BUG: htmlFor="first-name" but input id="firstName" — mismatch */}
              <label htmlFor="first-name">First Name</label>
              <input
                id="firstName"
                name="firstName"
                type="text"
                value={formData.firstName}
                onChange={handleChange}
                aria-invalid={!!errors.firstName}
                aria-required="true"
                // BUG: no aria-describedby pointing to error message
              />
              {errors.firstName && (
                <span className="error-text">{errors.firstName}</span>
                // BUG: no id on this span — cannot be referenced by aria-describedby
              )}
            </div>

            <div className="form-group">
              <label htmlFor="lastName">Last Name</label>
              <input
                id="lastName"
                name="lastName"
                type="text"
                value={formData.lastName}
                onChange={handleChange}
                aria-invalid={!!errors.lastName}
                aria-required="true"
                // BUG: no aria-describedby pointing to error message
              />
              {errors.lastName && (
                <span className="error-text">{errors.lastName}</span>
              )}
            </div>

            <div className="form-group">
              {/* BUG: htmlFor="street-address" but input id="address" — mismatch */}
              <label htmlFor="street-address">Street Address</label>
              <input
                id="address"
                name="address"
                type="text"
                value={formData.address}
                onChange={handleChange}
                aria-invalid={!!errors.address}
                aria-required="true"
              />
              {errors.address && (
                <span className="error-text">{errors.address}</span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="city">City</label>
              <input
                id="city"
                name="city"
                type="text"
                value={formData.city}
                onChange={handleChange}
                aria-invalid={!!errors.city}
                aria-required="true"
              />
              {errors.city && (
                <span className="error-text">{errors.city}</span>
              )}
            </div>
          </fieldset>
        )}

        {currentStep === 1 && (
          <fieldset>
            <legend>Payment Details</legend>

            <div className="form-group">
              <label htmlFor="cardNumber">Card Number</label>
              <input
                id="cardNumber"
                name="cardNumber"
                type="text"
                inputMode="numeric"
                value={formData.cardNumber}
                onChange={handleChange}
                aria-invalid={!!errors.cardNumber}
                aria-required="true"
              />
              {errors.cardNumber && (
                <span className="error-text">{errors.cardNumber}</span>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="cardExpiry">Expiry Date (MM/YY)</label>
              <input
                id="cardExpiry"
                name="cardExpiry"
                type="text"
                value={formData.cardExpiry}
                onChange={handleChange}
                aria-invalid={!!errors.cardExpiry}
                aria-required="true"
              />
              {errors.cardExpiry && (
                <span className="error-text">{errors.cardExpiry}</span>
              )}
            </div>
          </fieldset>
        )}

        {currentStep === 2 && (
          <section aria-labelledby="review-heading">
            <h2 id="review-heading">Review Your Order</h2>
            <p><strong>Name:</strong> {formData.firstName} {formData.lastName}</p>
            <p><strong>Address:</strong> {formData.address}, {formData.city}</p>
            <p><strong>Card ending:</strong> {formData.cardNumber.slice(-4) || '—'}</p>
          </section>
        )}

        <div className="form-actions">
          {currentStep < STEPS.length - 1 ? (
            <button type="button" onClick={handleNext}>
              Next: {STEPS[currentStep + 1]}
            </button>
          ) : (
            <button type="submit">Place Order</button>
          )}
        </div>

      </form>
    </div>
  );
};

export default CheckoutForm;
```

## CSS

```css
.checkout-wrapper {
  max-width: 560px;
  margin: 32px auto;
  padding: 24px;
  font-family: system-ui, sans-serif;
}

/* BUG: complete/upcoming states communicated by color alone */
.step-indicator {
  display: flex;
  gap: 8px;
  list-style: none;
  padding: 0;
  margin: 0 0 24px;
}

.step-indicator li {
  flex: 1;
  text-align: center;
  padding: 8px;
  border-radius: 4px;
  font-weight: 600;
  font-size: 14px;
}

.step-indicator li.complete  { background: #2e7d32; color: #fff; }
.step-indicator li.active    { background: #1565c0; color: #fff; }
.step-indicator li.upcoming  { background: #e0e0e0; color: #555; }

.error-summary {
  border: 2px solid #b71c1c;
  border-radius: 4px;
  padding: 16px;
  margin-bottom: 20px;
  background: #fff3f3;
}

.error-summary h2 {
  margin: 0 0 8px;
  font-size: 16px;
  color: #b71c1c;
}

.error-summary ul {
  margin: 0;
  padding-left: 20px;
  color: #b71c1c;
}

fieldset {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 16px;
  margin-bottom: 16px;
}

legend {
  font-weight: 700;
  padding: 0 8px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 4px;
  font-weight: 600;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 2px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
  box-sizing: border-box;
}

.form-group input[aria-invalid="true"] {
  border-color: #b71c1c;
}

.form-group input:focus {
  outline: 3px solid #1565c0;
  outline-offset: 2px;
}

.error-text {
  display: block;
  color: #b71c1c;
  font-size: 14px;
  margin-top: 4px;
}

.form-actions {
  margin-top: 24px;
  text-align: right;
}

.form-actions button {
  padding: 12px 24px;
  background: #1565c0;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

.form-actions button:focus {
  outline: 3px solid #1565c0;
  outline-offset: 2px;
}

.form-actions button:hover {
  background: #0d47a1;
}
```

## Expected Behavior

- Three-step checkout: Shipping → Payment → Review
- Validation runs on "Next" and on final submit
- Error summary appears above the form when validation fails
- Individual field errors render below each input
- Tab order follows DOM order through all fields
- "Next" and "Place Order" buttons respond to Enter key

## Accessibility Features Present

- Labels present on all fields (visually and in DOM)
- `fieldset` + `legend` groups fields within each step
- `aria-invalid` toggles on fields with errors
- `aria-required="true"` on all required inputs
- `aria-label` on step indicator list
- Submit and navigation controls are real `<button>` elements
- Focus indicators visible on inputs and buttons
- Keyboard navigation between fields works correctly (Tab/Shift+Tab)
- Review section uses `aria-labelledby`

## Accessibility Issues (Planted)

1. **CRITICAL: `htmlFor` mismatch on First Name field** — `<label htmlFor="first-name">` but `<input id="firstName">`. Screen reader announces "First Name" for an unrelated element (or announces nothing). The input itself is unlabeled from the browser's perspective.
   - Evidence: Lines 72–73 (`htmlFor="first-name"` vs `id="firstName"`)
   - WCAG: 1.3.1 Info and Relationships, 4.1.2 Name, Role, Value
   - User group: Screen reader users
   - Fix: Align `htmlFor` and `id` — use `htmlFor="firstName"` or `id="first-name"` consistently

2. **CRITICAL: `htmlFor` mismatch on Street Address field** — `<label htmlFor="street-address">` but `<input id="address">`. Same failure mode as First Name.
   - Evidence: Lines 95–96 (`htmlFor="street-address"` vs `id="address"`)
   - WCAG: 1.3.1 Info and Relationships, 4.1.2 Name, Role, Value
   - User group: Screen reader users
   - Fix: Align `htmlFor` and `id` — use `htmlFor="address"` or `id="street-address"` consistently

3. **MAJOR: Error messages not associated with fields via `aria-describedby`** — Error `<span>` elements have no `id`, and no input has `aria-describedby` pointing to its error. Screen reader announces `aria-invalid="true"` but never reads the error text.
   - Evidence: All form groups (e.g., lines 80–84, 103–107) — `aria-invalid` set but `aria-describedby` absent; error spans have no `id`
   - WCAG: 3.3.1 Error Identification, 3.3.2 Labels or Instructions
   - User group: Screen reader users
   - Fix: Add `id="error-firstName"` to error span; add `aria-describedby="error-firstName"` to corresponding input

4. **MAJOR: Error summary links do not navigate to fields** — Error summary `<li>` elements are plain text, not anchor links. A user cannot activate a link to jump focus to the offending field.
   - Evidence: Lines 67–70 — `<li key={field}>{message}</li>` with no `<a href="#fieldId">`
   - WCAG: 3.3.1 Error Identification (users should be able to locate and correct errors)
   - User group: Keyboard users, screen reader users, cognitive users
   - Fix: Replace `<li>{message}</li>` with `<li><a href="#fieldId">{message}</a></li>` where `fieldId` matches the input's `id`

5. **MAJOR: Step indicator communicates state via color alone** — Complete steps are green, upcoming steps are gray. No text supplement ("Complete", "Upcoming"), no icon, no `aria-current`, no visually-hidden label distinguishing states.
   - Evidence: CSS lines 15–17 — `.complete`, `.active`, `.upcoming` differ only in background color; JSX renders only step name text
   - WCAG: 1.4.1 Use of Color
   - User group: Color-blind users, low-vision users
   - Fix: Add visually-hidden text or `aria-label` suffix per step (e.g., "Shipping — complete"); or add an icon (checkmark) with `aria-hidden="false"` alt text

6. **MINOR: Error summary region has no `aria-live`** — When validation fails and the error summary mounts, screen reader users who are focused elsewhere will not be alerted. No `aria-live`, `role="alert"`, or `role="status"` on the summary container.
   - Evidence: Lines 64–71 — error summary `<div>` has no live region attribute
   - WCAG: 4.1.3 Status Messages
   - User group: Screen reader users
   - Fix: Add `role="alert"` (or `aria-live="polite"` + `aria-atomic="true"`) to the error summary `<div>`

## What Should NOT Be Flagged

- Keyboard navigation between fields is fully functional — Tab and Shift+Tab traverse all inputs in DOM order
- Tab order is logical and matches visual flow
- "Next" and "Place Order" are real `<button>` elements — keyboard-activatable with Enter/Space
- `fieldset` + `legend` grouping is correct
- `aria-required` is present on required fields

## Difficulty Level

**HAS-BUGS** — The form has the surface appearance of accessible design (labels, fieldsets, aria-invalid, focus styles) but contains specific, realistic failures in programmatic associations. Two `htmlFor` mismatches mean two fields are effectively unlabeled to screen readers despite having visible labels. Error handling is visually correct but semantically incomplete. This is a regression detection fixture — these are existing-dimension issues (screen reader, keyboard) that the current skills are already trained to find.
