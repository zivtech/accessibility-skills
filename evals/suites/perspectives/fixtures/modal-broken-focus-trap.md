# Fixture: Modal Dialog With Broken Focus Trap

## Component Code

```jsx
import React, { useState, useRef, useEffect } from 'react';

const SubscribeModal = ({ onClose }) => {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [submitted, setSubmitted] = useState(false);

  // BUG: No ref on the modal container for focus management
  // BUG: No useEffect to move focus into the modal on open
  // BUG: No focus trap logic — Tab exits into background page freely

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  if (submitted) {
    return (
      /*
        BUG: <div> with no role="dialog" or aria-modal — SR treats this as
        normal page content, not a dialog overlay.
        BUG: No aria-labelledby pointing to the heading.
      */
      <div className="modal-backdrop">
        <div className="modal-container">
          <p className="modal-success">Thanks, {name}! You're subscribed.</p>
          {/*
            BUG: Close button uses "×" character with no aria-label.
            SR may announce "times" or "multiplication sign" depending on SR.
          */}
          <button className="modal-close" onClick={onClose}>×</button>
        </div>
      </div>
    );
  }

  return (
    /*
      BUG: No role="dialog" — not identified as a dialog to AT.
      BUG: No aria-modal="true" — background content not hidden to virtual cursor.
      BUG: No aria-labelledby — dialog has no accessible name.
      The backdrop dims visually, which is correct.
    */
    <div className="modal-backdrop">
      <div className="modal-container">

        <div className="modal-header">
          {/* id present for potential aria-labelledby — but dialog never references it */}
          <h2 id="modal-title" className="modal-title">Subscribe to Updates</h2>
          {/*
            BUG: Close button icon "×" has no aria-label.
            Announced as "times button" or similar — not descriptive.
          */}
          <button
            className="modal-close"
            onClick={onClose}
          >
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="modal-form" noValidate>

          {/* Works: label correctly associated with input via htmlFor/id */}
          <div className="form-group">
            <label htmlFor="modal-name">Your name</label>
            <input
              id="modal-name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              aria-required="true"
            />
          </div>

          {/* Works: label correctly associated with input via htmlFor/id */}
          <div className="form-group">
            <label htmlFor="modal-email">Email address</label>
            <input
              id="modal-email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              aria-required="true"
            />
          </div>

          {/* Works: real <button> elements, keyboard-activatable */}
          <div className="modal-actions">
            <button type="button" className="btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn-primary">
              Subscribe
            </button>
          </div>

        </form>
      </div>
    </div>
  );
};

const SubscribePage = () => {
  const [isOpen, setIsOpen] = useState(false);
  const triggerRef = useRef(null);

  // BUG: When modal closes, focus is not returned to the trigger button.
  // triggerRef exists but is never used to restore focus on close.
  const handleClose = () => {
    setIsOpen(false);
    // Missing: triggerRef.current?.focus();
  };

  return (
    <main className="page-main">
      <h1>Newsletter</h1>
      <p>Stay informed about our latest updates and announcements.</p>

      <button
        ref={triggerRef}
        className="btn-open"
        onClick={() => setIsOpen(true)}
        aria-haspopup="dialog"
      >
        Subscribe Now
      </button>

      {/* Background content remains fully interactive while modal is open */}
      <nav className="background-nav">
        <a href="/home">Home</a>
        <a href="/about">About</a>
        <a href="/contact">Contact</a>
      </nav>

      {isOpen && <SubscribeModal onClose={handleClose} />}
    </main>
  );
};

export default SubscribePage;
```

## CSS

```css
.page-main {
  max-width: 640px;
  margin: 40px auto;
  padding: 24px;
  font-family: system-ui, sans-serif;
}

.btn-open {
  padding: 12px 24px;
  background: #1565c0;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

.btn-open:focus {
  outline: 3px solid #1565c0;
  outline-offset: 2px;
}

/* Works: backdrop visually dims background — conveyed non-accessibly */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
}

.modal-container {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  width: 100%;
  max-width: 440px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-title {
  margin: 0;
  font-size: 20px;
  color: #1a1a1a;
}

/* BUG: Close button visually clear but no accessible name for SR */
.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #424242;
  padding: 4px 8px;
  border-radius: 4px;
  line-height: 1;
}

.modal-close:focus {
  outline: 3px solid #1565c0;
  outline-offset: 2px;
}

.modal-form .form-group {
  margin-bottom: 16px;
}

.modal-form label {
  display: block;
  margin-bottom: 4px;
  font-weight: 600;
  font-size: 14px;
}

.modal-form input {
  width: 100%;
  padding: 10px;
  border: 2px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
  box-sizing: border-box;
}

.modal-form input:focus {
  outline: 3px solid #1565c0;
  outline-offset: 2px;
  border-color: #1565c0;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
}

.btn-secondary {
  padding: 10px 20px;
  background: #f5f5f5;
  color: #1a1a1a;
  border: 2px solid #ccc;
  border-radius: 4px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}

.btn-secondary:focus {
  outline: 3px solid #1565c0;
  outline-offset: 2px;
}

.btn-primary {
  padding: 10px 20px;
  background: #1565c0;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}

.btn-primary:focus {
  outline: 3px solid #1565c0;
  outline-offset: 2px;
}

.modal-success {
  font-size: 16px;
  color: #2e7d32;
  font-weight: 600;
  margin: 0 0 16px;
}

.background-nav {
  margin-top: 32px;
  display: flex;
  gap: 16px;
}

.background-nav a {
  color: #1565c0;
  text-decoration: underline;
}

.background-nav a:focus {
  outline: 3px solid #1565c0;
  outline-offset: 2px;
}
```

## Expected Behavior

- Clicking "Subscribe Now" opens the modal
- Focus moves automatically into the modal on open (first focusable element or modal heading)
- Tab cycles only among focusable elements inside the modal — background links are unreachable
- Shift+Tab wraps backward within the modal
- Escape closes the modal
- When modal closes, focus returns to the "Subscribe Now" trigger button
- Screen reader announces "Subscribe to Updates, dialog" on open

## Accessibility Features Present

- Trigger button uses `aria-haspopup="dialog"` correctly
- Form inputs have visible labels correctly associated via `htmlFor`/`id`
- `aria-required="true"` on both required inputs
- All interactive controls are real `<button>` or `<input>` elements
- Visible focus indicators on all interactive elements
- Visual backdrop overlay dims background content
- `triggerRef` is attached to the trigger button (though never used for focus restoration)
- Submit and Cancel buttons are real `<button>` elements with correct `type` attributes

## Accessibility Issues (Planted)

1. **CRITICAL: Focus is not moved to the modal on open** — No `useEffect` runs on mount to move focus inside the modal container. When the modal opens, keyboard focus remains on the "Subscribe Now" trigger, leaving users stranded outside the modal content.
   - Evidence: `SubscribeModal` component has no `useEffect` and no `useRef` for focus management; no `autoFocus` on any element
   - WCAG: 2.4.3 Focus Order
   - User group: Keyboard users, screen reader users
   - Fix: Add `const modalRef = useRef(null)` and `useEffect(() => { modalRef.current?.focus(); }, [])` with `tabIndex={-1}` on the modal container div

2. **CRITICAL: No focus trap — Tab escapes modal into background page** — Nothing prevents Tab from reaching the background `<nav>` links while the modal is open. Users can navigate away from the modal without closing it.
   - Evidence: No `onKeyDown` focus trap handler on modal; `.background-nav` links remain in tab order while modal is open
   - WCAG: 2.4.3 Focus Order
   - User group: Keyboard users, screen reader users
   - Fix: Add a keydown handler that intercepts Tab/Shift+Tab, collects focusable children, and cycles focus within the modal

3. **MAJOR: No `role="dialog"` or `aria-modal`** — The modal container is a plain `<div>`. Screen readers do not identify it as a dialog. Without `aria-modal="true"`, virtual cursor (browse mode) can reach background content even if visual focus is trapped.
   - Evidence: Modal container `<div className="modal-container">` — no `role`, no `aria-modal`
   - WCAG: 4.1.2 Name, Role, Value
   - User group: Screen reader users
   - Fix: Add `role="dialog" aria-modal="true" aria-labelledby="modal-title"` to `modal-container`

4. **MAJOR: Close button has no accessible name** — The close button renders the Unicode character `×` with no `aria-label`. Screen readers will announce it as "times button", "multiplication sign button", or just "button" depending on the reader.
   - Evidence: `<button className="modal-close" onClick={onClose}>×</button>` — no `aria-label`
   - WCAG: 4.1.2 Name, Role, Value
   - User group: Screen reader users
   - Fix: Add `aria-label="Close subscribe dialog"` to the close button; optionally use `aria-hidden="true"` on the `×` character

5. **MINOR: Focus not returned to trigger on modal close** — `handleClose` calls `setIsOpen(false)` but never calls `triggerRef.current?.focus()`. After dismissal, focus is lost (lands on `<body>` or wherever the browser places it).
   - Evidence: `handleClose` function — `setIsOpen(false)` only; `triggerRef` is declared and attached but never used for focus restoration
   - WCAG: 2.4.3 Focus Order
   - User group: Keyboard users, screen reader users
   - Fix: Add `triggerRef.current?.focus()` in `handleClose` after `setIsOpen(false)`

## What Should NOT Be Flagged

- Trigger button's `aria-haspopup="dialog"` is correctly set — do not flag
- Form field labels are correctly associated (`htmlFor`/`id` match on both fields) — do not flag
- `aria-required="true"` is present on required inputs — do not flag
- Submit and Cancel are real `<button>` elements with correct types — do not flag
- Focus indicators (`:focus` outlines) are present on all interactive elements — do not flag
- Visual backdrop overlay communicates modal state visually — not an a11y issue in itself

## Difficulty Level

**HAS-BUGS** — The modal has the visual appearance of an accessible dialog (overlay, header, labeled form fields, proper buttons, focus styles) but fails on the three core modal accessibility requirements: focus management on open, focus trap, and ARIA dialog semantics. These are well-established keyboard and screen reader dimension failures — regression detection territory for both primary dimensions.
