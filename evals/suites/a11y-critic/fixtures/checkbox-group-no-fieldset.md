# Fixture: Checkbox Group Without Fieldset and Legend

## Component Code

```jsx
import React, { useState } from 'react';

const BuggyCheckboxGroup = ({ label, options = [] }) => {
  const [selected, setSelected] = useState([]);

  const handleChange = (option) => {
    if (selected.includes(option)) {
      setSelected(selected.filter((s) => s !== option));
    } else {
      setSelected([...selected, option]);
    }
  };

  return (
    <div className="checkbox-group">
      {/* BUG: No <fieldset> to group related checkboxes */}
      {/* BUG: No <legend> to label the entire group */}
      {/* Screen reader announces each checkbox individually without group context */}
      <div className="group-label">{label}</div>
      {options.map((option) => (
        <label key={option} className="checkbox-label">
          <input
            type="checkbox"
            checked={selected.includes(option)}
            onChange={() => handleChange(option)}
            // BUG: No role="group" or aria-label on individual items to indicate grouping
          />
          {option}
        </label>
      ))}
    </div>
  );
};

export default BuggyCheckboxGroup;
```

## Expected Behavior

- Multiple checkboxes for selecting related options
- Group should be semantically grouped with fieldset/legend
- Screen reader announces group name and individual options
- Visual label matches semantic grouping

## Accessibility Features Present

✓ Label associated with each checkbox
✓ htmlFor properly used

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Missing <fieldset> to group related checkboxes** — Screen reader announces each checkbox as individual element without understanding they're part of a group. Per HTML semantics, related checkboxes should be wrapped in <fieldset> to create programmatic grouping.
   - Evidence: `checkbox-group-no-fieldset.md:18-22` (div wrapper instead of fieldset)
   - User group: Screen reader users (critical)
   - Expected: Checkboxes should be wrapped in <fieldset>
   - Fix: Replace div wrapper with <fieldset> element

2. **CRITICAL: Missing <legend> to label the group** — Group has visual label (div.group-label) but no <legend> element for semantic labeling. Screen reader user cannot identify the group name. Per HTML form semantics, <fieldset> requires <legend> for accessible grouping.
   - Evidence: `checkbox-group-no-fieldset.md:18-22` (group-label is plain div, not legend)
   - User group: Screen reader users (critical)
   - Expected: Visual label should be wrapped in <legend> inside <fieldset>
   - Fix: Wrap label text in <legend> element inside <fieldset>

3. **MAJOR: Group context lost to screen reader** — Even though individual checkboxes have labels, screen reader user navigating by Tab does not hear that checkboxes are part of a group. Each checkbox announced in isolation without group context.
   - Evidence: `checkbox-group-no-fieldset.md:27-36` (each input label only references individual option, not group)
   - User group: Screen reader users
   - Expected: Screen reader announces "Group: [Legend], Option 1 of N, [label]"
   - Fix: Use <fieldset> and <legend> to establish proper grouping structure

## Difficulty Level

**HAS-BUGS** — Basic form pattern incompleteness. Missing fundamental HTML semantics for checkbox groups.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Difficulty Rating

A11y-critic should recognize that this is a basic HTML form pattern that requires <fieldset> and <legend>, not just label elements on individual checkboxes. Many developers miss this pattern.
