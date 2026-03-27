# Fixture: Radio Button Group Without Semantic Grouping

## Component Code

```jsx
import React, { useState } from 'react';

const BuggyRadioGroup = ({ label, options = [] }) => {
  const [selected, setSelected] = useState(options[0]);

  return (
    <div className="radio-group">
      {/* BUG: No <fieldset> to group related radios */}
      {/* BUG: No <legend> to label the radio group */}
      {/* Visual label is just a div, not semantic */}
      <div className="group-label">{label}</div>
      {options.map((option) => (
        <label key={option} className="radio-label">
          <input
            type="radio"
            name="options"
            value={option}
            checked={selected === option}
            onChange={(e) => setSelected(e.target.value)}
            // BUG: name="options" groups them in form submission but not semantically
            // Screen reader doesn't announce group name
          />
          {option}
        </label>
      ))}
    </div>
  );
};

export default BuggyRadioGroup;
```

## Expected Behavior

- Multiple radio buttons for selecting one option
- Group should be semantically grouped with fieldset/legend
- Screen reader announces group name before presenting options
- Name attribute groups radios for form submission

## Accessibility Features Present

✓ name attribute groups radios
✓ Label associated with each radio
✓ htmlFor properly used

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Missing <fieldset> to group related radio buttons** — Screen reader announces each radio as individual element. The name attribute groups them for form submission but not semantically. Per HTML semantics, radio groups should use <fieldset> for programmatic grouping.
   - Evidence: `radio-button-group-no-grouping.md:9-13` (div wrapper, not fieldset)
   - User group: Screen reader users (critical)
   - Expected: Radio buttons should be wrapped in <fieldset>
   - Fix: Replace div with <fieldset> element

2. **CRITICAL: Missing <legend> to label the group** — Visual label (div.group-label) exists but <legend> is missing. Screen reader user does not hear the group label when navigating radios. Per HTML, <fieldset> requires <legend>.
   - Evidence: `radio-button-group-no-grouping.md:11` (group-label is div, not legend)
   - User group: Screen reader users (critical)
   - Expected: Label should be wrapped in <legend>
   - Fix: Replace group-label div with <legend> inside <fieldset>

3. **MAJOR: name attribute alone is insufficient for AT** — While name="options" groups radios for form submission, it does not communicate group relationship to screen reader. Screen reader user navigating by Tab hears radios as isolated elements.
   - Evidence: `radio-button-group-no-grouping.md:14-24` (name attribute present but no fieldset/legend)
   - User group: Screen reader users
   - Expected: Radio group should announce as group with legend label
   - Fix: Use <fieldset> and <legend> alongside name attribute

## Difficulty Level

**HAS-BUGS** — Missing fundamental HTML semantics for radio button groups. Similar to checkbox groups but for mutually exclusive options.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Difficulty Rating

A11y-critic should recognize that radio button groups follow the same semantic pattern as checkbox groups: they need <fieldset> and <legend>. This is a common pattern omission.
