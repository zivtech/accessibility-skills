# Fixture: Custom Dropdown with Focus Restoration Bug

## Component Code

```jsx
import React, { useState, useRef } from 'react';

const BuggyDropdown = ({ label, options, onSelect }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const listRef = useRef(null);

  const handleToggle = () => {
    setIsOpen(!isOpen);
    if (!isOpen && listRef.current) {
      listRef.current.focus();
    }
  };

  const handleSelect = (index) => {
    setSelectedIndex(index);
    onSelect(options[index]);
    setIsOpen(false);
    // BUG: Focus is NOT restored to trigger button
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      e.preventDefault();
      setIsOpen(false);
      // BUG: Focus not restored here either
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      const nextIndex = selectedIndex < options.length - 1 ? selectedIndex + 1 : 0;
      setSelectedIndex(nextIndex);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      const prevIndex = selectedIndex > 0 ? selectedIndex - 1 : options.length - 1;
      setSelectedIndex(prevIndex);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      handleSelect(selectedIndex);
    }
  };

  return (
    <div className="dropdown-wrapper">
      <label htmlFor="dropdown-btn">{label}</label>
      <button
        id="dropdown-btn"
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        aria-controls="dropdown-list"
        onClick={handleToggle}
      >
        {options[selectedIndex]}
        <span aria-hidden="true">▼</span>
      </button>
      {isOpen && (
        <ul
          ref={listRef}
          id="dropdown-list"
          role="listbox"
          onKeyDown={handleKeyDown}
          tabIndex="0"
          className="dropdown-list"
        >
          {options.map((option, index) => (
            <li
              key={index}
              role="option"
              aria-selected={index === selectedIndex}
              onClick={() => handleSelect(index)}
              className={index === selectedIndex ? 'selected' : ''}
            >
              {option}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default BuggyDropdown;
```

## Expected Behavior

- Opens on button click, list receives focus
- Arrow Down/Up navigate options
- Enter or click selects option
- Escape should close dropdown AND restore focus to button (BUG: doesn't)
- Selection should restore focus to button (BUG: doesn't)

## Accessibility Features Present

✓ aria-haspopup="listbox"
✓ aria-expanded toggles
✓ aria-controls references list
✓ role="listbox" and role="option"
✓ aria-selected on items
✓ Arrow key navigation
✓ Label association via htmlFor

## Accessibility Issues (Planted Bugs)

1. **MAJOR: Focus not restored after selection** — When user selects an option by clicking or pressing Enter, focus is lost (goes to document body). Keyboard user has no clear reference point to continue navigation. Per WAI-ARIA Listbox Pattern, focus should return to trigger button.
   - Evidence: `interactive-dropdown-focus-bug.md:41-45` (handleSelect function has no focus restoration)
   - User group: Keyboard-only (critical)
   - Expected: After selection, focus returns to trigger button
   - Fix: Add `buttonRef.current?.focus()` after `setIsOpen(false)` in handleSelect

2. **MAJOR: Focus not restored on Escape** — When user presses Escape to close dropdown, focus is not restored to trigger button. Keyboard user loses position. Per WCAG 2.1.2 (No Keyboard Trap) and WAI-ARIA Listbox Pattern, focus must be managed explicitly.
   - Evidence: `interactive-dropdown-focus-bug.md:17-20` (handleKeyDown Escape handler missing focus management)
   - User group: Keyboard-only (critical to keyboard navigation flow)
   - Expected: Escape closes dropdown AND returns focus to trigger button
   - Fix: Store buttonRef and restore focus in Escape handler

## Difficulty Level

**HAS-BUGS** — Clear keyboard focus management failures. The ARIA pattern is mostly correct (aria-expanded, aria-selected present), but the focus management design is incomplete. This is a common real-world bug in custom dropdowns.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Difficulty Rating

Baseline (generic a11y prompt) will likely catch the missing focus restoration because it's obvious once you test with keyboard. A11y-critic should:
1. Identify both focus restoration gaps as MAJOR
2. Cite WAI-ARIA Listbox Pattern and focus management requirements
3. Note this breaks keyboard-only user experience
4. Suggest concrete fix (adding focus restoration)
5. Distinguish from CRITICAL because ARIA structure is correct (just focus management incomplete)
