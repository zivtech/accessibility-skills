# Fixture: Modal Dialog Component

## Component Code

```jsx
import React, { useRef, useEffect } from 'react';
import ReactDOM from 'react-dom';

// Standard tabbable elements: native interactive elements that are not
// disabled, plus anything opted into the tab order. Excludes
// tabindex="-1" (programmatically focusable but never Tab-reachable).
const FOCUSABLE_SELECTOR = [
  'a[href]',
  'area[href]',
  'button:not([disabled])',
  'input:not([disabled]):not([type="hidden"])',
  'select:not([disabled])',
  'textarea:not([disabled])',
  'audio[controls]',
  'video[controls]',
  '[contenteditable]:not([contenteditable="false"])',
  '[tabindex]:not([tabindex="-1"])',
].join(', ');

const getFocusableElements = (container) =>
  Array.from(container.querySelectorAll(FOCUSABLE_SELECTOR)).filter(
    // display:none elements produce no client rects and cannot take
    // focus, so they must not become wrap anchors.
    (el) => el.getClientRects().length > 0
  );

const Modal = ({ isOpen, onClose, title, children }) => {
  const modalRef = useRef(null);
  const previouslyFocusedElement = useRef(null);
  const mouseDownTarget = useRef(null);

  useEffect(() => {
    if (isOpen) {
      // Store the previously focused element
      previouslyFocusedElement.current = document.activeElement;

      // Move focus into the modal (to the close button or first focusable element)
      setTimeout(() => {
        if (!modalRef.current) return;
        const firstFocusable = getFocusableElements(modalRef.current)[0];
        firstFocusable?.focus();
      }, 0);

      // Disable body scroll
      document.body.style.overflow = 'hidden';

      return () => {
        document.body.style.overflow = '';
        // Restore focus when modal closes
        previouslyFocusedElement.current?.focus();
      };
    }
  }, [isOpen]);

  // Handle Escape key. Separate effect so an unstable onClose identity
  // (e.g. an inline arrow prop) only re-binds this listener and never
  // disturbs the focus save/restore lifecycle above.
  useEffect(() => {
    if (!isOpen) return;

    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  // Focus trap: keep focus within modal when tabbing
  useEffect(() => {
    if (!isOpen || !modalRef.current) return;

    const handleTabKey = (e) => {
      if (e.key !== 'Tab') return;

      // Recompute on every Tab so children added, removed, or disabled
      // while the modal is open are handled correctly.
      const focusableElements = getFocusableElements(modalRef.current);
      if (focusableElements.length === 0) {
        e.preventDefault();
        return;
      }

      const firstElement = focusableElements[0];
      const lastElement = focusableElements[focusableElements.length - 1];
      const activeElement = document.activeElement;

      // If focus landed outside the dialog (e.g. a click on static text
      // moved it to <body>), pull it back to the boundary instead of
      // letting Tab continue into the page behind the modal.
      if (!modalRef.current.contains(activeElement)) {
        e.preventDefault();
        (e.shiftKey ? lastElement : firstElement).focus();
        return;
      }

      if (e.shiftKey) {
        // Shift+Tab
        if (activeElement === firstElement) {
          e.preventDefault();
          lastElement.focus();
        }
      } else {
        // Tab
        if (activeElement === lastElement) {
          e.preventDefault();
          firstElement.focus();
        }
      }
    };

    document.addEventListener('keydown', handleTabKey);
    return () => document.removeEventListener('keydown', handleTabKey);
  }, [isOpen]);

  if (!isOpen) return null;

  const handleOverlayMouseDown = (e) => {
    mouseDownTarget.current = e.target;
  };

  const handleOverlayClick = (e) => {
    // Close only when the click both started and ended on the backdrop
    // itself. Clicks inside the dialog bubble up to this handler, and a
    // text-selection drag that ends on the backdrop fires a click whose
    // target is the backdrop — neither may dismiss the dialog.
    if (
      e.target === e.currentTarget &&
      mouseDownTarget.current === e.currentTarget
    ) {
      onClose();
    }
  };

  return ReactDOM.createPortal(
    <div
      className="modal-overlay"
      onMouseDown={handleOverlayMouseDown}
      onClick={handleOverlayClick}
      role="presentation"
    >
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
- Focus traps within modal: Tab and Shift+Tab cycle through every tabbable element inside the dialog — links, buttons, inputs, selects, textareas, contenteditable regions, and elements with a non-negative tabindex — skipping disabled controls and tabindex="-1" elements
- Focus returns to trigger button when modal closes
- Clicking the backdrop closes the modal; clicks that start inside the dialog (including text-selection drags that end on the backdrop) never close it
- Backdrop is not exposed to assistive technology (role="presentation") and is not focusable; Escape is the keyboard equivalent of backdrop dismissal
- Modal has proper ARIA attributes
- Title is announced by screen reader

## Accessibility Features Implemented

✓ role="dialog" and aria-modal="true"
✓ aria-labelledby links to modal title
✓ Focus trap covers the full tabbable set (recomputed on each Tab; disabled and tabindex="-1" elements excluded)
✓ Focus trap recovers focus that lands outside the dialog instead of letting Tab escape
✓ Focus restoration on close (previouslyFocusedElement), unaffected by parent re-renders
✓ Escape key handler
✓ Backdrop dismissal guarded: only clicks that start and end on the backdrop close the dialog
✓ Backdrop not exposed to AT (role="presentation")
✓ All interactive elements within modal are focusable
✓ Clear close button with aria-label
✓ Heading hierarchy correct (h2 for modal title)
✓ Semantic structure: header > title + close button, body

## Accessibility Issues (None Planted — CLEAN Baseline)

None. This fixture is a CLEAN baseline: the component is a complete, correct
WAI-ARIA Modal Dialog implementation with no planted defects. Everything from
this heading down is ground-truth material and is stripped from model prompts
by the blind protocol (`ANSWER_KEY_RE` in the runners).

## Difficulty Level

**CLEAN** — This is a properly implemented WAI-ARIA Modal Dialog pattern. Should receive a clean verdict or ACCEPT. Used as a baseline to verify skill accuracy and false-positive rate.

## Notes

A11y-critic should verify and acknowledge this is properly implemented. Not finding issues here is correct. The component demonstrates:
- Complete WAI-ARIA Modal Dialog pattern
- Proper focus management (trap + restoration)
- Keyboard handling (Escape)
- Semantic structure

May note optional enhancements (e.g., aria-label on overlay, animation on open), but no blocking issues.

Revision history: on 2026-07-16 two real, unplanted defects were fixed at
source (incomplete focus-trap selector `'button, [href], input, [tabindex]'`;
unguarded overlay `onClick={onClose}` that closed the dialog on any in-dialog
click). Reviewers that flagged either on earlier runs were correct. The same
revision moved this section and Difficulty Level below the blind-protocol strip
boundary and dropped the "(Complete, CLEAN)" suffix from the h1 title — before
that, every lane saw this fixture's "should receive ACCEPT" prose and tier
label in its prompt. See `ollama/BENCHMARK.md` → Scoring changelog (2026-07-16).
