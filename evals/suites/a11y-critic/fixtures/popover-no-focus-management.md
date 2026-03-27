# Fixture: Popover Without Focus Management

## Component Code

```jsx
import React, { useState, useRef } from 'react';

const BuggyPopover = ({ trigger, content }) => {
  const [isOpen, setIsOpen] = useState(false);
  const triggerRef = useRef(null);

  const openPopover = () => {
    setIsOpen(true);
    // BUG: Focus not moved to popover or trap within it
  };

  const closePopover = () => {
    setIsOpen(false);
    // BUG: Focus not restored to trigger button
  };

  return (
    <div className="popover-wrapper">
      <button ref={triggerRef} onClick={openPopover}>
        {trigger}
      </button>

      {isOpen && (
        <div
          className="popover-content"
          // BUG: No role="dialog" to identify as popover
          // BUG: No aria-modal to indicate modal behavior
          // BUG: No aria-labelledby to label popover
        >
          <button onClick={closePopover}>Close</button>
          {content}
        </div>
      )}
    </div>
  );
};

export default BuggyPopover;
```

## Expected Behavior

- Button opens popover dialog
- Focus moves into popover after opening
- Escape key closes popover and restores focus
- aria-modal announces modal behavior
- Popover labeled by title or aria-labelledby

## Accessibility Features Present

✓ Close button visible
✓ Click handler for opening/closing

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Focus not moved to popover** — When popover opens, focus remains on trigger button. Keyboard user doesn't know popover has opened or where to navigate. Per modal pattern, focus should move to popover after opening.
   - Evidence: `popover-no-focus-management.md:8-10` (openPopover has no focus movement)
   - User group: Keyboard users (critical)
   - Expected: Focus should move to popover content or close button after opening
   - Fix: Add autoFocus on close button or use useEffect to move focus

2. **CRITICAL: Focus not restored to trigger** — When popover closes, focus is not restored to trigger button. Keyboard user loses position and must tab to regain focus. Per modal pattern, focus should return to trigger.
   - Evidence: `popover-no-focus-management.md:12-15` (closePopover has no focus restoration)
   - User group: Keyboard users (critical)
   - Expected: Focus should return to trigger button after close
   - Fix: Add triggerRef.current.focus() in closePopover

3. **CRITICAL: Missing role="dialog"** — Popover is a div without dialog semantics. Screen reader user doesn't identify it as a modal dialog. Per ARIA, popovers should have role="dialog" to mark as modal.
   - Evidence: `popover-no-focus-management.md:25-31` (no role attribute)
   - User group: Screen reader users (critical)
   - Expected: Popover should have role="dialog"
   - Fix: Add role="dialog" to popover div

4. **MAJOR: Missing aria-modal** — Without aria-modal="true", screen reader doesn't announce that interaction is modal (affects focus scope for assistive tech). Per ARIA modal dialog pattern, aria-modal should indicate modal behavior.
   - Evidence: `popover-no-focus-management.md:25-31` (no aria-modal)
   - User group: Screen reader users
   - Expected: Popover should have aria-modal="true"
   - Fix: Add aria-modal="true" to popover div

5. **MAJOR: Missing aria-labelledby** — Popover has no label. Screen reader user doesn't know what dialog is about. Should have aria-labelledby pointing to title or trigger text.
   - Evidence: `popover-no-focus-management.md:25-31` (no aria-labelledby)
   - User group: Screen reader users
   - Expected: Popover should have aria-labelledby pointing to header
   - Fix: Add title and aria-labelledby reference

## Difficulty Level

**HAS-BUGS** — Popover rendered but modal semantics and focus management completely missing.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Difficulty Rating

A11y-critic should identify that popovers are modal dialogs requiring focus management, role="dialog", aria-modal, and proper labeling. This tests understanding of complex modal patterns.
