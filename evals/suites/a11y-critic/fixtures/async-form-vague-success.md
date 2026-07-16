# Fixture: Async Form with Vague Success Announcement

## Component Code

```jsx
import React, { useState, useRef } from 'react';

const FeedbackForm = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  });
  const [status, setStatus] = useState('idle'); // idle | submitting | success | error
  const [errorMessage, setErrorMessage] = useState('');
  const statusRef = useRef(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('submitting');
    setErrorMessage('');

    try {
      const response = await fetch('/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error('Server error');

      setStatus('clearing');
      setTimeout(() => {
        setStatus('success');
      }, 200);
    } catch (err) {
      setStatus('error');
      setErrorMessage('Something went wrong. Please try again.');
    }
  };

  return (
    <div className="feedback-form-container">
      <h2>Send Us Feedback</h2>

      <div
        ref={statusRef}
        role="status"
        aria-live="polite"
        aria-atomic="true"
        aria-busy={status === 'submitting'}
        className="form-status"
      >
        {status === 'submitting' && (
          <p className="status-message loading">
            <span className="spinner" aria-hidden="true"></span>
            Submitting your feedback...
          </p>
        )}
        {status === 'success' && (
          <p className="status-message success">
            Your submission was successful!
          </p>
        )}
        {status === 'error' && (
          <p className="status-message error" role="alert">
            {errorMessage}
          </p>
        )}
      </div>

      <form onSubmit={handleSubmit} className="feedback-form">
        <div className="form-group">
          <label htmlFor="feedback-name">Full Name</label>
          <input
            id="feedback-name"
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            autoComplete="name"
          />
        </div>

        <div className="form-group">
          <label htmlFor="feedback-email">Email Address</label>
          <input
            id="feedback-email"
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            autoComplete="email"
          />
        </div>

        <div className="form-group">
          <label htmlFor="feedback-message">Your Feedback</label>
          <textarea
            id="feedback-message"
            name="message"
            value={formData.message}
            onChange={handleChange}
            required
            rows={5}
          />
        </div>

        <button
          type="submit"
          className="submit-button"
          disabled={status === 'submitting'}
        >
          {status === 'submitting' ? 'Submitting...' : 'Send Feedback'}
        </button>
      </form>
    </div>
  );
};

export default FeedbackForm;
```

## CSS

```css
.feedback-form-container {
  max-width: 520px;
  margin: 32px auto;
  padding: 24px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-family: system-ui, -apple-system, sans-serif;
}

.feedback-form-container h2 {
  margin: 0 0 20px;
  font-size: 22px;
  color: #1e293b;
}

.form-status {
  min-height: 24px;
  margin-bottom: 16px;
}

.status-message {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
}

.status-message.loading {
  background: #eff6ff;
  color: #1d4ed8;
  border: 1px solid #bfdbfe;
}

.status-message.success {
  background: #f0fdf4;
  color: #15803d;
  border: 1px solid #bbf7d0;
}

.status-message.error {
  background: #fef2f2;
  color: #b91c1c;
  border: 1px solid #fecaca;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid #bfdbfe;
  border-top-color: #1d4ed8;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: 600;
  color: #334155;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid #cbd5e1;
  border-radius: 6px;
  font-size: 15px;
  box-sizing: border-box;
  transition: border-color 0.15s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

.form-group textarea {
  resize: vertical;
}

.submit-button {
  width: 100%;
  padding: 12px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.15s;
}

.submit-button:hover:not(:disabled) {
  background: #1d4ed8;
}

.submit-button:focus {
  outline: 3px solid #3b82f6;
  outline-offset: 2px;
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
```

## Expected Behavior

- User fills in name, email, and feedback message
- On submit, a loading spinner and "Submitting your feedback..." appear in the live region
- aria-busy signals the async operation in progress
- On success, a green confirmation message appears
- On error, a red alert message appears
- Screen reader users hear status updates through the aria-live region

## Accessibility Features Present

- role="status" on the live region container
- aria-live="polite" on the status container
- aria-atomic="true" for complete re-reads
- aria-busy toggles during async request
- aria-hidden="true" on decorative spinner
- Proper label associations via htmlFor
- required attribute on all fields
- autoComplete hints on name and email
- Visible focus indicators on all interactive elements
- Button disabled during submission with visual feedback
- Semantic form structure with fieldset-free layout (appropriate for simple forms)
- Error state uses role="alert" for assertive announcement

## Accessibility Issues (Planted)

1. **MAJOR: Success message is generic — doesn't identify what was submitted** — The live region announces "Your submission was successful!" regardless of form context. A screen reader user who just submitted feedback, a newsletter signup, or a support ticket all hear the same message. Per WCAG 4.1.3 Status Messages, the status message should provide equivalent information to what a sighted user perceives — and a sighted user sees the form title "Send Us Feedback" along with the success message, establishing context. A screen reader user who submitted the form and navigated elsewhere before the announcement arrives hears only the generic "Your submission was successful!" with no way to know WHICH submission succeeded.
   - Evidence: `async-form-vague-success.md:65-67` — hardcoded "Your submission was successful!" with no reference to form purpose or submitted data
   - WCAG citation: 4.1.3 Status Messages (status message must provide equivalent information)
   - User group: Screen reader users — especially those with multiple forms open or who have navigated away from the form
   - Expected: "Your feedback has been sent successfully" or "Feedback from [name] submitted" — message should identify the action that completed
   - Fix: Change success message to include form context: `Your feedback has been sent. We'll respond to ${formData.email} within 2 business days.`

2. **MAJOR: aria-busy cleared 200ms before success content arrives** — The `aria-busy` attribute transitions from `true` to `false` when status changes to `'clearing'`, but the success message text isn't inserted until 200ms later when status becomes `'success'`. During this gap, the live region is: not busy (aria-busy="false"), empty (no status message rendered), and polite (aria-live="polite"). Some screen readers (NVDA, JAWS) check the live region content when aria-busy transitions to false — if the region is empty at that moment, the announcement is skipped entirely. The success message that arrives 200ms later may or may not trigger a second announcement depending on the SR's debounce behavior.
   - Evidence: `async-form-vague-success.md:37-39` — `setStatus('clearing')` removes aria-busy immediately, `setTimeout(() => setStatus('success'), 200)` inserts content later
   - WCAG citation: 4.1.3 Status Messages (announcement timing must ensure AT receives the message)
   - User group: Screen reader users — NVDA and JAWS most affected; VoiceOver somewhat more tolerant of timing gaps
   - Expected: aria-busy should remain true until the success message is ready, then both should update in the same render cycle
   - Fix: Remove the `clearing` intermediate state. Set status directly to `'success'` so aria-busy transitions to false in the same React render that inserts the success text.

3. **MINOR: Form fields remain editable after successful submission** — After the success message appears, all form fields (name, email, message) remain interactive. No `disabled` or `aria-disabled` attribute is set, no visual dimming or "already submitted" state. A screen reader user tabbing through the form after submission encounters fully editable fields with no indication the form was already submitted. They could fill it in again and re-submit.
   - Evidence: `async-form-vague-success.md:76-106` — no conditional disabled/aria-disabled based on success state; form fields always editable
   - WCAG citation: 3.3.4 Error Prevention (for forms that submit data, provide ability to review/correct/confirm — but equally, prevent unintentional duplicate submissions)
   - User group: Screen reader users (no programmatic "done" state), cognitive disability users (may not remember they already submitted), motor impairment users (accidental re-activation)
   - Expected: After success, disable form fields and submit button, or replace form with confirmation content
   - Fix: When `status === 'success'`, set `disabled` on all inputs/textarea and the submit button, or conditionally render a confirmation view instead of the form

4. **ENHANCEMENT: Success confirmation cannot be re-read after navigation** — The success message appears once in the live region. If the user navigates away (e.g., to another part of the page) and returns, the message is still visible but a screen reader won't re-announce it — the content didn't change. There's no mechanism to re-read the confirmation: no focus management to the success message, no heading in the confirmation, and the message isn't a landmark.
   - Evidence: `async-form-vague-success.md:57-70` — status div has no tabindex, no heading, and is not a landmark. Once the live region announcement fires, the content is only discoverable by sequential navigation.
   - WCAG citation: Best practice — persistent status should be discoverable, not just announced once
   - User group: Screen reader users (can't re-find confirmation), cognitive disability users (may need to re-read to confirm)
   - Expected: Either move focus to the success message (with tabindex="-1"), or provide a heading/landmark that screen reader users can navigate to
   - Fix: Add `tabindex="-1"` to success message container and call `statusRef.current.focus()` when status becomes 'success', or add a heading level to the confirmation

## Difficulty Level

**FLAWED** — The live region infrastructure looks correct at first glance: `aria-live="polite"`, `role="status"`, `aria-atomic="true"`, `aria-busy` toggling during the async request, `aria-hidden` on the spinner, `role="alert"` on errors. A surface-level check sees "all the right attributes" and moves on. The bugs are in the QUALITY of announcements (vague message that doesn't identify the submission), TIMING (aria-busy/content desynchronization), and COMPLETENESS (no post-submission state management for the form itself).

Expected baseline detection: 15-35%. A zero-shot reviewer sees the live region with correct attributes, aria-busy toggling, success/error paths — and concludes the pattern is well-implemented. Finding the vague message bug requires thinking about what a screen reader user ACTUALLY HEARS versus what a sighted user sees in context. Finding the timing bug requires tracing the state machine through the `clearing` intermediate state and understanding how SRs respond to aria-busy transitions.

## Frameworks & Environment

React 18+, standard HTML/CSS, async fetch API

## Notes

This fixture tests three distinct reviewer skills:

1. **Message quality analysis** (must_find) — Can the critic evaluate whether a live region announcement provides equivalent information? The message is syntactically correct but semantically insufficient. This requires thinking about user experience, not just attribute correctness.

2. **Timing trace** (should_find) — Can the critic trace the aria-busy lifecycle through the `clearing` intermediate state? The 200ms gap between aria-busy="false" and content insertion is a real-world pattern that causes silent announcement failures in NVDA/JAWS. Finding this requires understanding SR timing behavior, not just checking that aria-busy exists.

3. **Post-action state management** (nice_to_find) — Does the critic check what happens to the form AFTER the async action completes? Most reviewers focus on the status announcement and stop. The form's unchanged editable state after success is a separate dimension that tests completeness of review scope.
