# Fixture: Combobox with Missing Listbox Role

## Component Code

```jsx
import React, { useState, useRef } from 'react';

const BuggyCombobox = ({ label, options = [] }) => {
  const [input, setInput] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const inputRef = useRef(null);

  const filtered = input
    ? options.filter((opt) =>
        opt.toLowerCase().includes(input.toLowerCase())
      )
    : options;

  const handleInputChange = (e) => {
    setInput(e.target.value);
    setIsOpen(true);
    setSelectedIndex(-1);
  };

  const handleSelect = (value) => {
    setInput(value);
    setIsOpen(false);
    setSelectedIndex(-1);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (!isOpen) {
        setIsOpen(true);
      } else {
        const nextIdx = selectedIndex < filtered.length - 1 ? selectedIndex + 1 : 0;
        setSelectedIndex(nextIdx);
      }
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      const prevIdx = selectedIndex > 0 ? selectedIndex - 1 : filtered.length - 1;
      setSelectedIndex(prevIdx);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (selectedIndex >= 0) {
        handleSelect(filtered[selectedIndex]);
      }
    } else if (e.key === 'Escape') {
      e.preventDefault();
      setIsOpen(false);
    }
  };

  return (
    <div className="combobox-wrapper">
      <label htmlFor="combobox-input">{label}</label>
      <div className="combobox-control">
        <input
          ref={inputRef}
          id="combobox-input"
          type="text"
          value={input}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          aria-autocomplete="list"
          aria-expanded={isOpen}
          role="combobox"
          // BUG: No aria-owns or aria-controls pointing to suggestions list
        />
      </div>
      {isOpen && filtered.length > 0 && (
        <div
          // BUG: Missing role="listbox" — just a div with no semantic meaning
          // Screen reader user has no idea this is a list of suggestions
          className="suggestions-list"
          id="suggestions-popup"
        >
          {filtered.map((option, idx) => (
            <div
              key={idx}
              // BUG: No role="option" on items
              onClick={() => handleSelect(option)}
              className={selectedIndex === idx ? 'suggestion-item selected' : 'suggestion-item'}
              // BUG: No aria-selected to announce selection state
            >
              {option}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default BuggyCombobox;
```

## Expected Behavior

- User types in input to filter suggestions
- Arrow Down opens list and navigates items
- Arrow Up navigates backward
- Enter selects highlighted item
- Escape closes list
- Screen reader announces suggestions list and item selection state

## Accessibility Features Present

✓ input has role="combobox"
✓ aria-autocomplete="list"
✓ aria-expanded toggles
✓ Arrow key navigation implemented
✓ Label association via htmlFor

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Missing role="listbox" on suggestions container** — Screen reader user has no indication that the popup is a selectable list. The div is announced as a generic container, not a listbox. Per WAI-ARIA Combobox (with Listbox Popup) Pattern, aria-owns or aria-controls must establish the relationship.
   - Evidence: `combobox-autocomplete-no-listbox-role.md:64-72` (suggestions div has no role attribute)
   - User group: Screen reader users (critical; cannot identify popup as list)
   - Expected: Popup container should have role="listbox"
   - Fix: Add role="listbox" to suggestions-list div

2. **CRITICAL: Suggestion items missing role="option"** — Screen reader user cannot navigate items as options. Items announced as plain divs, not list items. Per combobox pattern, each item must have role="option" and aria-selected.
   - Evidence: `combobox-autocomplete-no-listbox-role.md:73-82` (items are divs with no role)
   - User group: Screen reader users (critical; cannot navigate as list items)
   - Expected: Items should have role="option"
   - Fix: Add role="option" and aria-selected={selectedIndex === idx} to item divs

3. **MAJOR: Missing aria-owns or aria-controls** — Input does not declare relationship to suggestions container. Screen reader user must guess that popup is related to input. Per APG Combobox Pattern, aria-controls should link input to listbox.
   - Evidence: `combobox-autocomplete-no-listbox-role.md:60-61` (no aria-controls attribute)
   - User group: Screen reader users
   - Expected: Input should have aria-controls="suggestions-popup"
   - Fix: Add aria-controls="suggestions-popup" to input element

4. **MAJOR: Missing aria-selected on items** — No state announcement for item selection. Screen reader user cannot determine which item is highlighted during keyboard navigation.
   - Evidence: `combobox-autocomplete-no-listbox-role.md:73-82` (no aria-selected)
   - User group: Screen reader users
   - Expected: Selected item should announce aria-selected="true"
   - Fix: Add aria-selected={selectedIndex === idx} to each item

## Difficulty Level

**HAS-BUGS** — Missing fundamental ARIA semantics for combobox with listbox popup. The interaction pattern (arrow keys, selection) works, but screen reader experience is broken.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Difficulty Rating

A generic accessibility review might flag the missing roles as "missing ARIA" without understanding the specific combobox pattern. A11y-critic should:
1. Identify role="listbox" and role="option" as CRITICAL — not optional enhancements
2. Cite WAI-ARIA Combobox (with Listbox Popup) Pattern specifically
3. Note this breaks screen reader user experience for navigation
4. Explain aria-owns or aria-controls requirement
5. Recognize this as a pattern structure bug (major), not just a missing attribute
