# Fixture: Toast Notification Without Alert Role

## Component Code

```jsx
import React, { useState, useEffect } from 'react';

const BuggyToast = ({ message, duration = 3000 }) => {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(false);
    }, duration);

    return () => clearTimeout(timer);
  }, [duration]);

  if (!isVisible) {
    return null;
  }

  return (
    <div className="toast-notification">
      {/* BUG: No role="alert" or role="status" */}
      {/* BUG: No aria-live region to announce message */}
      {/* BUG: No aria-label or aria-describedby */}
      {/* Screen reader user may miss toast message entirely */}
      {message}
    </div>
  );
};

export default BuggyToast;
```

## Expected Behavior

- Toast appears and automatically dismisses after 3 seconds
- Screen reader announces toast message immediately
- Message is announced with alert priority
- Keyboard user can dismiss toast if needed
- Visual indicator shows toast type (success, error, etc.)

## Accessibility Features Present

✓ Automatic dismissal timer
✓ Visual styling

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Missing role="alert"** — Toast notification is just a div without alert semantics. Screen reader user may not be immediately notified of message. Per ARIA, toast notifications should have role="alert" to mark as important status message.
   - Evidence: `toast-notification-no-role.md:19-25` (div has no role)
   - User group: Screen reader users (critical)
   - Expected: Toast should have role="alert" or role="status"
   - Fix: Add role="alert" to notification div

2. **CRITICAL: Missing aria-live region** — Even with role="alert", aria-live="assertive" ensures announcement. Without aria-live, message may not be announced to screen reader user, especially if toast appears after page load.
   - Evidence: `toast-notification-no-role.md:19-25` (no aria-live attribute)
   - User group: Screen reader users (critical)
   - Expected: Toast should have aria-live="assertive"
   - Fix: Add aria-live="assertive" to ensure immediate announcement

3. **MAJOR: No way to dismiss for keyboard user** — Toast auto-dismisses but keyboard user cannot manually dismiss if needed. Should provide close button for user control. Per WCAG 2.1.1, user should have control over timed interactions.
   - Evidence: `toast-notification-no-role.md:10-17` (no dismiss mechanism)
   - User group: Keyboard users (major)
   - Expected: Close button should be provided
   - Fix: Add accessible close button that keyboard user can activate

4. **MAJOR: Message not labeled or described** — Toast message has no associated label or description. Screen reader user hears the text but may not understand the message type (success, error, warning).
   - Evidence: `toast-notification-no-role.md:24-25` (no aria-label or context)
   - User group: Screen reader users
   - Expected: Should have aria-label describing message type, or context should be clear
   - Fix: Add aria-label="Success: [message]" or similar

## Difficulty Level

**HAS-BUGS** — Toast notification lacks alert semantics and announcements. Common pattern but accessibility incomplete.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Difficulty Rating

A11y-critic should recognize that toast notifications are status messages that require role="alert" and aria-live for proper AT support. This tests understanding of transient messages and alert announcements.
