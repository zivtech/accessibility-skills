# Fixture: Custom Select Combobox Without Keyboard Navigation

## Component Code

```jsx
import React, { useState, useRef, useEffect } from 'react';

const options = [
  { value: 'us', label: 'United States' },
  { value: 'ca', label: 'Canada' },
  { value: 'mx', label: 'Mexico' },
  { value: 'uk', label: 'United Kingdom' },
  { value: 'de', label: 'Germany' },
  { value: 'fr', label: 'France' },
  { value: 'jp', label: 'Japan' },
  { value: 'au', label: 'Australia' },
];

const CustomSelect = ({ label, onChange }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selected, setSelected] = useState(null);
  const [filter, setFilter] = useState('');
  const inputRef = useRef(null);

  const filtered = options.filter(o =>
    o.label.toLowerCase().includes(filter.toLowerCase())
  );

  const handleSelect = (option) => {
    setSelected(option);
    setFilter(option.label);
    setIsOpen(false);
    onChange?.(option.value);
  };

  // BUG: No ArrowUp/ArrowDown handling — only Tab navigates options
  // BUG: No Escape to close dropdown
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && filtered.length === 1) {
      handleSelect(filtered[0]);
    }
  };

  return (
    <div className="custom-select">
      <label htmlFor="country-input">{label}</label>
      {/* BUG: No role="combobox" on input — WCAG 4.1.2 */}
      <input
        id="country-input"
        ref={inputRef}
        type="text"
        value={filter}
        onChange={(e) => { setFilter(e.target.value); setIsOpen(true); }}
        onFocus={() => setIsOpen(true)}
        onKeyDown={handleKeyDown}
        placeholder="Type to search..."
        autoComplete="off"
        // BUG: Missing aria-expanded, aria-controls, aria-activedescendant
      />

      {isOpen && filtered.length > 0 && (
        // BUG: No role="listbox" — this is a plain div
        <div className="select-dropdown">
          {filtered.map((option, i) => (
            // BUG: No role="option", no aria-selected
            <div
              key={option.value}
              className={`select-option ${selected?.value === option.value ? 'selected' : ''}`}
              onClick={() => handleSelect(option)}
              tabIndex={0}
            >
              {option.label}
            </div>
          ))}
        </div>
      )}

      {/* BUG: No live region announcing filtered count */}
    </div>
  );
};

export default CustomSelect;
```

```css
.custom-select {
  position: relative;
  width: 280px;
  font-family: system-ui, sans-serif;
}

.custom-select label {
  display: block;
  font-weight: 600;
  margin-bottom: 4px;
}

.custom-select input {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

.custom-select input:focus {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}

.select-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  max-height: 200px;
  overflow-y: auto;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 0 0 4px 4px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  z-index: 10;
}

.select-option {
  padding: 8px 12px;
  cursor: pointer;
  font-size: 0.95rem;
}

.select-option:hover {
  background: #e3f2fd;
}

/* Visual focus indicator on options — correct */
.select-option:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: -2px;
  background: #e3f2fd;
}

.select-option.selected {
  background: #bbdefb;
  font-weight: 600;
}
```

## Expected Behavior

- Text input filters options as user types
- Dropdown appears on focus with matching options
- Clicking an option selects it and closes the dropdown
- Arrow keys should navigate options (but don't)
- Escape should close dropdown (but doesn't)

## Accessibility Features Present

- `<label>` associated with input via `htmlFor`/`id`
- Visual focus indicator on input (`:focus` outline)
- Visual focus indicator on options (`:focus-visible`)
- Options are focusable via `tabIndex={0}`
- Visual selected state (bold + background color)

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Arrow keys don't navigate options — WCAG 2.1.1 (Keyboard) + APG Combobox**
   Only Tab moves between options. ArrowUp/ArrowDown are not handled in `onKeyDown`. This violates both the WCAG keyboard requirement and the APG combobox interaction pattern.
   - Evidence: Lines 34-38 — `handleKeyDown` only checks Enter, not Arrow keys
   - User group: Keyboard users, switch access users
   - Fix: Add ArrowUp/ArrowDown handlers to move visual focus through options using an `activeIndex` state

2. **CRITICAL: No role="combobox" or role="listbox" — WCAG 4.1.2 (Name, Role, Value)**
   The input has no `role="combobox"` and the dropdown div has no `role="listbox"`. Screen readers cannot identify this as a combobox widget.
   - Evidence: Lines 48-49 — plain `<input>` with no ARIA role; Line 62 — dropdown is plain `<div>`
   - User group: Screen reader users
   - Fix: Add `role="combobox"` on input, `role="listbox"` on dropdown, `role="option"` on each item

3. **MAJOR: Selected option not announced — no aria-selected or aria-activedescendant**
   Options have no `aria-selected` attribute. Input has no `aria-activedescendant`. Screen readers cannot communicate which option is current or selected.
   - Evidence: Lines 65-70 — options use CSS class `.selected` but no `aria-selected`; input has no `aria-activedescendant`
   - User group: Screen reader users
   - Fix: Add `aria-selected={selected?.value === option.value}` on options; add `aria-activedescendant` on input pointing to focused option ID

4. **MINOR: Escape doesn't close dropdown — APG Combobox pattern**
   No Escape key handling in `onKeyDown`. Users cannot dismiss the dropdown via keyboard.
   - Evidence: Lines 34-38 — no `e.key === 'Escape'` check
   - User group: Keyboard users
   - Fix: Add `if (e.key === 'Escape') { setIsOpen(false); }`

5. **MINOR: No live region announces filtered count — WCAG 4.1.3**
   When the user types and options filter, the count changes visually but no aria-live region announces "3 results available."
   - Evidence: No `aria-live` element in the component
   - User group: Screen reader users
   - Fix: Add `<div aria-live="polite" className="sr-only">{filtered.length} results available</div>`

## Difficulty Level

**HAS-BUGS** — Existing dimension: Keyboard & Screen Reader. These are classic ARIA/keyboard pattern failures the current skills should already catch. This is a regression detection fixture — all three conditions should score 70%+.

## Frameworks

React 18+, CSS
