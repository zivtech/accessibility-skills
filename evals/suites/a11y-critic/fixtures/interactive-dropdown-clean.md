# Fixture: Interactive Dropdown Component (CLEAN)

## Component Code

```jsx
import React, { useState, useRef, useEffect } from 'react';

const DropdownSelect = ({ label, options, onSelect }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const buttonRef = useRef(null);
  const listRef = useRef(null);

  const handleToggle = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      setTimeout(() => {
        listRef.current?.focus();
      }, 0);
    }
  };

  const handleSelect = (index) => {
    setSelectedIndex(index);
    onSelect(options[index]);
    setIsOpen(false);
    // Restore focus to trigger button
    buttonRef.current?.focus();
  };

  const handleKeyDown = (e) => {
    if (!isOpen) {
      if (e.key === 'Enter' || e.key === ' ' || e.key === 'ArrowDown') {
        e.preventDefault();
        setIsOpen(true);
        setTimeout(() => {
          listRef.current?.focus();
        }, 0);
      }
      return;
    }

    // Dropdown is open
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      const nextIndex = selectedIndex < options.length - 1 ? selectedIndex + 1 : 0;
      setSelectedIndex(nextIndex);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      const prevIndex = selectedIndex > 0 ? selectedIndex - 1 : options.length - 1;
      setSelectedIndex(prevIndex);
    } else if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleSelect(selectedIndex);
    } else if (e.key === 'Escape') {
      e.preventDefault();
      setIsOpen(false);
      // CRITICAL: Restore focus to trigger button
      buttonRef.current?.focus();
    }
  };

  return (
    <div className="dropdown-wrapper">
      <label htmlFor="dropdown-button">{label}</label>
      <button
        ref={buttonRef}
        id="dropdown-button"
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        aria-controls="dropdown-listbox"
        onClick={handleToggle}
        onKeyDown={handleKeyDown}
        className="dropdown-trigger"
      >
        {options[selectedIndex]}
        <span aria-hidden="true">▼</span>
      </button>
      {isOpen && (
        <ul
          ref={listRef}
          id="dropdown-listbox"
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
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  handleSelect(index);
                }
              }}
              className={`dropdown-item ${index === selectedIndex ? 'selected' : ''}`}
            >
              {option}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default DropdownSelect;
```

## CSS Styles

```css
.dropdown-wrapper {
  position: relative;
  display: inline-block;
  width: 200px;
}

.dropdown-wrapper label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #333;
}

.dropdown-trigger {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid #0066cc;
  border-radius: 4px;
  background: white;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: border-color 0.2s;
}

.dropdown-trigger:hover {
  border-color: #004499;
  background: #f9f9f9;
}

.dropdown-trigger:focus {
  outline: 3px solid #0066cc;
  outline-offset: 2px;
  border-color: #0066cc;
}

.dropdown-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin: 4px 0 0 0;
  padding: 0;
  border: 1px solid #ccc;
  border-radius: 4px;
  background: white;
  list-style: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 10;
  max-height: 200px;
  overflow-y: auto;
}

.dropdown-list:focus {
  outline: 3px solid #0066cc;
  outline-offset: -1px;
}

.dropdown-item {
  padding: 12px;
  cursor: pointer;
  border-bottom: 1px solid #eee;
  transition: background-color 0.15s;
}

.dropdown-item:last-child {
  border-bottom: none;
}

.dropdown-item:hover,
.dropdown-item[aria-selected="true"] {
  background-color: #e6f2ff;
  color: #0066cc;
  font-weight: 600;
}

.dropdown-item:focus {
  outline: 2px solid #0066cc;
  outline-offset: -1px;
  background-color: #e6f2ff;
}
```

## Expected Behavior

- Clicking the trigger button opens the dropdown list
- Arrow Down/Up keys navigate options (wrapping at ends)
- Enter or Space selects highlighted option
- Escape key closes dropdown and restores focus to trigger button
- Selected option is visually highlighted and aria-selected="true"
- aria-expanded accurately reflects open/closed state
- aria-controls links button to listbox
- aria-haspopup="listbox" informs AT of popup type

## Accessibility Features Implemented

✓ Native button element for trigger (proper semantics)
✓ Label associated via htmlFor (proper form semantics)
✓ aria-haspopup="listbox" on trigger (role announcement)
✓ aria-expanded toggles with state (state communication)
✓ aria-controls links trigger to list (relationship communication)
✓ role="listbox" on list container
✓ role="option" on items with aria-selected
✓ Arrow key navigation fully implemented
✓ Escape key closes and restores focus to trigger
✓ Focus indicators visible (outline on button and list)
✓ Click handler for mouse users
✓ Roving tabindex: listbox gets tabindex="0", items not individually focusable

## Frameworks & Environment

- React 18+
- No external libraries (vanilla focus management)
- CSS-in-JS compatible or stylesheet compatible
- Works with any screen reader (NVDA, JAWS, VoiceOver)

## Difficulty Level

**CLEAN** — This is a properly implemented custom dropdown that should serve as a baseline for skill accuracy. A11y-critic should verify:
1. All ARIA attributes present and correct
2. Focus management works (Escape restores focus)
3. Arrow key navigation complete
4. Semantic structure correct (button + listbox pattern)
5. No false positives (this is genuinely accessible)

The fixture should receive a clean verdict with possible minor suggestions (e.g., aria-label on list could be more descriptive if there are multiple dropdowns on page).
