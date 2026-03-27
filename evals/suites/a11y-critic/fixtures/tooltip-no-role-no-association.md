# Fixture: Tooltip Missing Role and Focus Association

## Component Code

```jsx
import React, { useState } from 'react';

const BuggyTooltip = ({ trigger, content }) => {
  const [showTooltip, setShowTooltip] = useState(false);

  return (
    <div className="tooltip-wrapper">
      <button
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
        // BUG: No aria-describedby to associate tooltip with trigger
        // BUG: No aria-label if button text is unclear
      >
        {trigger}
      </button>
      {showTooltip && (
        <div
          className="tooltip-content"
          role="tooltip"
          // BUG: Role is present but no proper timing or focus management
          // Tooltip appears on hover only, not on focus
          // Keyboard user cannot access tooltip
        >
          {content}
        </div>
      )}
    </div>
  );
};

export default BuggyTooltip;
```

## Expected Behavior

- Tooltip appears on mouse hover
- Tooltip should appear on keyboard focus
- Tooltip content should be associated with trigger via aria-describedby
- Screen reader should announce tooltip when trigger is focused
- Tooltip should be visible for keyboard users

## Accessibility Features Present

✓ role="tooltip" on tooltip div

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Tooltip only appears on hover, not focus** — Keyboard user pressing Tab to trigger button does not see tooltip. Tooltip appears on hover only (JavaScript onMouseEnter), not on focus. Per WCAG 1.4.13 (Content on Hover or Focus), tooltips must appear on focus for keyboard users.
   - Evidence: `tooltip-no-role-no-association.md:11-13` (onMouseEnter only, no onFocus handler)
   - User group: Keyboard-only users (critical)
   - Expected: Tooltip should appear on both hover AND focus
   - Fix: Add onFocus and onBlur handlers to trigger button

2. **CRITICAL: Missing aria-describedby on trigger button** — Screen reader user cannot know that tooltip content describes the button. No association established between button and tooltip. Per ARIA practices, aria-describedby should link button to tooltip.
   - Evidence: `tooltip-no-role-no-association.md:8-13` (button has no aria-describedby)
   - User group: Screen reader users (critical)
   - Expected: Button should have aria-describedby="tooltip-id"
   - Fix: Add aria-describedby pointing to tooltip div id

3. **MAJOR: Tooltip not announced on focus** — Even with role="tooltip", screen reader does not announce content when button is focused. Tooltip content should be automatically announced to screen reader user when trigger receives focus.
   - Evidence: `tooltip-no-role-no-association.md:15-22` (tooltip only renders on hover, not available to AT on focus)
   - User group: Screen reader users
   - Expected: Tooltip should be announced when button is focused
   - Fix: Ensure tooltip renders when trigger has focus, and aria-describedby is present

## Difficulty Level

**HAS-BUGS** — Tooltip pattern is incomplete. Role is present but focus behavior and association are missing.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Difficulty Rating

Many developers add role="tooltip" and think they're done. A11y-critic should identify that tooltips must also handle keyboard focus and establish associations with their trigger elements. This tests understanding of WCAG 1.4.13 and focus management requirements.
