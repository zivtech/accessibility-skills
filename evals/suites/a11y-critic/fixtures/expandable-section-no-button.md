# Fixture: Expandable Section Using Div Instead of Button

## Component Code

```jsx
import React, { useState } from 'react';

const BuggyExpandable = ({ title, content }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggle = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className="expandable-section">
      {/* BUG: Click handler on div instead of button */}
      {/* BUG: No role="button" to mark as interactive */}
      {/* BUG: No aria-expanded state */}
      {/* Keyboard user cannot activate with Space/Enter */}
      <div
        className="expandable-trigger"
        onClick={toggle}
        // BUG: No role="button"
        // BUG: No keyboard handler
        // BUG: No aria-expanded
      >
        {/* BUG: No visual indicator that this is clickable */}
        {title}
        {isExpanded ? ' −' : ' +'}
      </div>

      {isExpanded && (
        <div className="expandable-content">
          {content}
        </div>
      )}
    </div>
  );
};

export default BuggyExpandable;
```

## Expected Behavior

- Click title to expand/collapse content
- Keyboard user can use Space/Enter to toggle
- aria-expanded announces state
- Visual styling indicates clickable trigger
- Semantically correct button element

## Accessibility Features Present

✓ Visual indicator (+/−)
✓ onClick handler

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Using <div> instead of <button> for trigger** — Trigger is a div with onClick handler instead of a proper button element. Keyboard user cannot activate using Space or Enter keys. Per HTML semantics, interactive elements must be <button> or have role="button" with proper keyboard handling.
   - Evidence: `expandable-section-no-button.md:14-23` (div used instead of button)
   - User group: Keyboard-only users (critical)
   - Expected: Trigger should be <button> element
   - Fix: Replace div with <button> element

2. **CRITICAL: Missing aria-expanded state announcement** — No aria-expanded attribute to announce expand/collapse state. Screen reader user does not know if section is expanded or can be expanded.
   - Evidence: `expandable-section-no-button.md:14-23` (no aria-expanded)
   - User group: Screen reader users (critical)
   - Expected: Trigger should have aria-expanded={isExpanded}
   - Fix: Add aria-expanded={isExpanded} to trigger

3. **MAJOR: No keyboard support** — div onClick only responds to mouse click. Keyboard user pressing Tab cannot focus the trigger (not a button), and even if focused, Space/Enter will not activate. Per WCAG 2.1.1, all interactive elements must be keyboard accessible.
   - Evidence: `expandable-section-no-button.md:14-23` (div has no keyboard handlers)
   - User group: Keyboard-only users (major)
   - Expected: Interactive element should handle Space/Enter keys
   - Fix: Use <button> element which handles keyboard automatically

4. **MAJOR: Missing role="button"** — If div is used, it needs role="button" and keyboard handling. Without role, screen reader user doesn't know this is a button.
   - Evidence: `expandable-section-no-button.md:14-23` (no role attribute)
   - User group: Screen reader users (major)
   - Expected: Should have role="button" or be replaced with <button>
   - Fix: Use <button> element instead of div with role

## Difficulty Level

**HAS-BUGS** — Semantic button pattern completely missing. Interactive element is div with no keyboard or ARIA support.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Difficulty Rating

A11y-critic should identify this as a fundamental semantic HTML issue. Using div for interactive elements is a common mistake that breaks keyboard accessibility. This is a critical pattern violation.
