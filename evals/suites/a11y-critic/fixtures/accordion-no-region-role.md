# Fixture: Accordion Without Region Role on Expanded Content

## Component Code

```jsx
import React, { useState } from 'react';

const BuggyAccordion = ({ items = [] }) => {
  const [expanded, setExpanded] = useState(0);

  const toggleItem = (index) => {
    setExpanded(expanded === index ? -1 : index);
  };

  return (
    <div className="accordion">
      {items.map((item, index) => (
        <div key={index} className="accordion-item">
          <button
            className="accordion-trigger"
            onClick={() => toggleItem(index)}
            aria-expanded={expanded === index}
            aria-controls={`panel-${index}`}
          >
            {item.title}
            <span aria-hidden="true">{expanded === index ? '−' : '+'}</span>
          </button>
          {expanded === index && (
            <div
              id={`panel-${index}`}
              className="accordion-panel"
              // BUG: Missing role="region" — screen reader just reads content
              // no indication that this is a logical panel/region
              // No aria-labelledby to associate panel with button
            >
              {item.content}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default BuggyAccordion;
```

## Expected Behavior

- Each accordion item has expandable button and content panel
- Only one panel open at a time
- Button shows +/- indicator (aria-hidden)
- Content panel should be announced as region
- Panel should be labeled by its trigger button

## Accessibility Features Present

✓ Button with aria-expanded
✓ aria-controls references panel id
✓ Proper id on panel
✓ aria-hidden on decorative icon

## Accessibility Issues (Planted Bugs)

1. **MAJOR: Missing role="region" on accordion panel** — Screen reader user just reads content without context that it's an expandable region. Per ARIA Accordion Pattern, expanded content should have role="region" to mark it as a logical section. Without role="region", screen reader just presents content as part of page flow.
   - Evidence: `accordion-no-region-role.md:29-35` (div has no role attribute)
   - User group: Screen reader users
   - Expected: Expanded panel should have role="region"
   - Fix: Add role="region" to accordion-panel div

2. **MAJOR: Missing aria-labelledby on panel** — Panel region has no label. Screen reader user cannot quickly identify what section is expanded. Per region semantics, aria-labelledby should point to trigger button to establish label relationship.
   - Evidence: `accordion-no-region-role.md:29-35` (no aria-labelledby attribute)
   - User group: Screen reader users
   - Expected: Panel should have aria-labelledby pointing to trigger button
   - Fix: Add aria-labelledby={`trigger-${index}`} and id={`trigger-${index}`} to button

3. **MINOR: Collapsed panels still exist in DOM** — Keyboard user who tabs quickly might focus on hidden button. While aria-expanded announces state, collapsed content still in DOM could be confusing for some AT users. Conditional rendering would improve experience.
   - Evidence: `accordion-no-region-role.md:27-35` (panel only renders when expanded, but button always present)
   - User group: Keyboard users navigating by Tab
   - Expected: All panels in DOM with visible/hidden state, or ensure Tab order skips collapsed buttons
   - Fix: Consider keeping all panels in DOM with display:none for better AT support

## Difficulty Level

**HAS-BUGS** — Accordion interaction works, but screen reader semantics for region identification are incomplete.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Difficulty Rating

This tests whether reviewers understand that role="region" serves a specific purpose (marking expandable sections) beyond just aria-expanded on the button. A11y-critic should identify the pattern incompleteness around region semantics.
