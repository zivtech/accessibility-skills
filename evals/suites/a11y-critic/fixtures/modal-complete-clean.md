# Fixture: Modal Dialog Component (Complete, CLEAN)

## Component Code

```jsx
import React, { useState, useRef, useEffect } from 'react';
import ReactDOM from 'react-dom';

const Modal = ({ isOpen, onClose, title, children }) => {
  const modalRef = useRef(null);
  const previouslyFocusedElement = useRef(null);

  useEffect(() => {
    if (isOpen) {
      // Store the previously focused element
      previouslyFocusedElement.current = document.activeElement;

      // Move focus into the modal (to the close button or first focusable element)
      setTimeout(() => {
        const firstFocusable = modalRef.current?.querySelector('button, [href], input, [tabindex]');
        firstFocusable?.focus();
      }, 0);

      // Disable body scroll
      document.body.style.overflow = 'hidden';

      // Handle Escape key
      const handleEscape = (e) => {
        if (e.key === 'Escape') {
          onClose();
        }
      };

      document.addEventListener('keydown', handleEscape);

      return () => {
        document.removeEventListener('keydown', handleEscape);
        document.body.style.overflow = '';
        // Restore focus when modal closes
        previouslyFocusedElement.current?.focus();
      };
    }
  }, [isOpen, onClose]);

  // Focus trap: keep focus within modal when tabbing
  useEffect(() => {
    if (!isOpen || !modalRef.current) return;

    const handleTabKey = (e) => {
      if (e.key !== 'Tab') return;

      const focusableElements = modalRef.current.querySelectorAll(
        'button, [href], input, [tabindex]'
      );
      const firstElement = focusableElements[0];
      const lastElement = focusableElements[focusableElements.length - 1];
      const activeElement = document.activeElement;

      if (e.shiftKey) {
        // Shift+Tab
        if (activeElement === firstElement) {
          e.preventDefault();
          lastElement?.focus();
        }
      } else {
        // Tab
        if (activeElement === lastElement) {
          e.preventDefault();
          firstElement?.focus();
        }
      }
    };

    document.addEventListener('keydown', handleTabKey);
    return () => document.removeEventListener('keydown', handleTabKey);
  }, [isOpen]);

  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <div className="modal-overlay" onClick={onClose} role="presentation">
      <div
        ref={modalRef}
        className="modal-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
      >
        <div className="modal-header">
          <h2 id="modal-title">{title}</h2>
          <button
            className="modal-close"
            onClick={onClose}
            aria-label="Close dialog"
          >
            ✕
          </button>
        </div>
        <div className="modal-body">{children}</div>
      </div>
    </div>,
    document.body
  );
};

export default Modal;
```

## CSS

```css
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-dialog {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}

.modal-dialog:focus {
  outline: 3px solid #0066cc;
  outline-offset: 2px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  font-size: 20px;
  color: #333;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: 4px 8px;
  color: #666;
  transition: color 0.2s;
}

.modal-close:hover {
  color: #333;
}

.modal-close:focus {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
  border-radius: 4px;
}

.modal-body {
  padding: 20px;
  color: #333;
  line-height: 1.6;
}
```

## Expected Behavior

- Modal displays when isOpen=true, hidden when isOpen=false
- Escape key closes modal
- Focus traps within modal (Tab cycles through focusable elements)
- Focus returns to trigger button when modal closes
- Backdrop (overlay) is not interactive (role="presentation")
- Modal has proper ARIA attributes
- Title is announced by screen reader

## Accessibility Features Implemented

✓ role="dialog" and aria-modal="true"
✓ aria-labelledby links to modal title
✓ Focus trap implemented (Tab/Shift+Tab cycle within modal)
✓ Focus restoration on close (previouslyFocusedElement)
✓ Escape key handler
✓ Backdrop not interactive (role="presentation")
✓ All interactive elements within modal are focusable
✓ Clear close button with aria-label
✓ Heading hierarchy correct (h2 for modal title)
✓ Semantic structure: header > title + close button, body

## Difficulty Level

**CLEAN** — This is a properly implemented WAI-ARIA Modal Dialog pattern. Should receive a clean verdict or ACCEPT. Used as a baseline to verify skill accuracy and false-positive rate.

## Notes

A11y-critic should verify and acknowledge this is properly implemented. Not finding issues here is correct. The component demonstrates:
- Complete WAI-ARIA Modal Dialog pattern
- Proper focus management (trap + restoration)
- Keyboard handling (Escape)
- Semantic structure

May note optional enhancements (e.g., aria-label on overlay, animation on open), but no blocking issues.
