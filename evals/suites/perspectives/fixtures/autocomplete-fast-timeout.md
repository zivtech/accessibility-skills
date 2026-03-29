# Fixture: Address Autocomplete With Fast Timeout and Double-Action Enter

## Component Code

```jsx
import React, { useState, useEffect, useRef } from 'react';

const mockAddresses = [
  '123 Main Street, Philadelphia, PA 19103',
  '456 Market Street, Philadelphia, PA 19104',
  '789 Broad Street, Philadelphia, PA 19107',
  '321 Walnut Street, Philadelphia, PA 19106',
  '654 Chestnut Street, Philadelphia, PA 19103',
  '987 Pine Street, Philadelphia, PA 19107',
];

const AddressAutocomplete = ({ onSubmit }) => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [selectedIdx, setSelectedIdx] = useState(-1);
  const timeoutRef = useRef(null);
  const formRef = useRef(null);

  useEffect(() => {
    if (!query.trim()) { setSuggestions([]); return; }
    setLoading(true);
    const timer = setTimeout(() => {
      const results = mockAddresses.filter(a =>
        a.toLowerCase().includes(query.toLowerCase())
      );
      setSuggestions(results);
      setLoading(false);
      setShowSuggestions(true);
      setSelectedIdx(-1);
    }, 200);
    return () => clearTimeout(timer);
  }, [query]);

  // BUG: Suggestions disappear after 800ms of inactivity — WCAG 2.2.1
  useEffect(() => {
    if (!showSuggestions) return;
    clearTimeout(timeoutRef.current);
    timeoutRef.current = setTimeout(() => {
      setShowSuggestions(false);
    }, 800);
    return () => clearTimeout(timeoutRef.current);
  }, [showSuggestions, selectedIdx]);

  const handleKeyDown = (e) => {
    if (!showSuggestions || suggestions.length === 0) return;

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIdx(i => Math.min(i + 1, suggestions.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIdx(i => Math.max(i - 1, 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (selectedIdx >= 0) {
        // BUG: Enter selects suggestion AND submits the form — WCAG 3.2.2
        setQuery(suggestions[selectedIdx]);
        setShowSuggestions(false);
        formRef.current.submit();
      }
    }
  };

  const handleSelect = (address) => {
    setQuery(address);
    setShowSuggestions(false);
  };

  return (
    <form ref={formRef} onSubmit={(e) => { e.preventDefault(); onSubmit?.(query); }} className="address-form">
      <h2>Shipping Address</h2>

      <div className="autocomplete-wrapper">
        <label htmlFor="address-input">Street address</label>
        <input
          id="address-input"
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          onBlur={() => setTimeout(() => setShowSuggestions(false), 150)}
          aria-describedby="address-hint"
          autoComplete="off"
        />
        <p id="address-hint" className="hint">Start typing to see address suggestions.</p>

        {/* BUG: Loading spinner — CSS only, no aria-busy or text */}
        {loading && <div className="autocomplete-spinner" />}

        {showSuggestions && suggestions.length > 0 && (
          // BUG: No role="listbox" — plain div with no ARIA
          <div className="suggestions-list">
            {suggestions.map((addr, i) => (
              // BUG: No role="option" — plain div
              <div
                key={addr}
                className={`suggestion-item ${i === selectedIdx ? 'highlighted' : ''}`}
                onClick={() => handleSelect(addr)}
              >
                {addr}
              </div>
            ))}
          </div>
        )}

        {showSuggestions && !loading && suggestions.length === 0 && query.trim() && (
          // BUG: "No results" — italic gray, no aria-live
          <p className="no-results">No matching addresses found.</p>
        )}
      </div>

      <button type="submit" className="submit-btn">Continue to payment</button>
    </form>
  );
};

export default AddressAutocomplete;
```

```css
.address-form {
  max-width: 480px;
  margin: 0 auto;
  padding: 24px;
  font-family: system-ui, sans-serif;
}

.address-form h2 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: #111;
}

.autocomplete-wrapper {
  position: relative;
  margin-bottom: 20px;
}

.autocomplete-wrapper label {
  display: block;
  font-weight: 600;
  margin-bottom: 4px;
  color: #222;           /* 14.7:1 */
}

.autocomplete-wrapper input {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid #767676;  /* 4.54:1 — passes AA for UI components */
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

.autocomplete-wrapper input:focus {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}

.hint {
  font-size: 0.85rem;
  color: #555;           /* 7.5:1 */
  margin: 4px 0 0;
}

.autocomplete-spinner {
  position: absolute;
  right: 12px;
  top: 40px;
  width: 16px; height: 16px;
  border: 2px solid #e0e0e0;
  border-top-color: #1565c0;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.suggestions-list {
  position: absolute;
  top: calc(100% - 16px);
  left: 0; right: 0;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 0 0 4px 4px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  z-index: 10;
  max-height: 200px;
  overflow-y: auto;
}

.suggestion-item {
  padding: 10px 12px;
  cursor: pointer;
  font-size: 0.95rem;
  color: #222;
}

.suggestion-item:hover { background: #e3f2fd; }
.suggestion-item.highlighted { background: #bbdefb; }

/* BUG: No focus-visible on suggestion items — they're not focusable */

.no-results {
  font-style: italic;
  color: #888;           /* 3.5:1 — fails AA for text but it's a status message */
  font-size: 0.9rem;
  padding: 8px 12px;
  margin: 0;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background: #1565c0;
  color: #fff;           /* 5.4:1 */
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
}

.submit-btn:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}
```

## Expected Behavior

- Address input with autocomplete suggestions
- Typing filters matching addresses from a mock dataset
- Arrow keys navigate highlighted suggestion
- Enter selects the highlighted suggestion
- Selected address populates the input

## Accessibility Features Present

- `<label>` associated with input via `htmlFor`/`id`
- `aria-describedby` links input to hint text
- Visible focus outline on input and submit button
- Arrow keys navigate suggestion list
- Hint text explains autocomplete behavior
- Submit button is properly labeled

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Suggestions disappear after 800ms of inactivity — WCAG 2.2.1 (Timing Adjustable)**
   `setTimeout` hides suggestions after 800ms with no way to extend or disable. Switch users and motor-impaired users who navigate slowly lose the suggestion list mid-selection.
   - Evidence: Lines 38-42 — setTimeout(800) closes suggestions; resets on each selectedIdx change but base timeout is too short
   - User group: Motor impairment users, switch users, cognitive users
   - Fix: Remove timeout or extend to 5s+ with option to disable; keep suggestions open while input is focused

2. **MAJOR: Enter selects suggestion AND submits the form — WCAG 3.2.2 (On Input)**
   Pressing Enter on a highlighted suggestion calls both `setQuery` and `formRef.current.submit()`. Users expect Enter to select the suggestion and return to the input — not submit the entire form.
   - Evidence: Lines 57-60 — Enter handler selects then immediately submits
   - User group: Keyboard users, cognitive users
   - Fix: Separate selection from submission; Enter should select only, Tab or explicit button click submits

3. **MAJOR: Suggestions list has no role="listbox" — WCAG 4.1.2 (Name, Role, Value)**
   Suggestions container is a plain `<div>` with no ARIA role. Items have no `role="option"`. Screen readers cannot identify this as a list of selectable options.
   - Evidence: Line 91 — `<div className="suggestions-list">` with no role
   - User group: Screen reader users
   - Fix: Add `role="listbox"`, `role="option"` on items, `aria-activedescendant` on input

4. **MINOR: "No results" state shows with no aria-live announcement — WCAG 4.1.3**
   Empty state text appears visually but has no live region. Screen reader users don't learn that no matches were found.
   - Evidence: Lines 101-103 — plain `<p>` with no aria-live
   - User group: Screen reader users
   - Fix: Wrap in `aria-live="polite"` region

5. **MINOR: Loading spinner is CSS-only with no accessible text — WCAG 4.1.3**
   Spinner is purely visual — no `aria-busy`, no sr-only text.
   - Evidence: Line 87 — `<div className="autocomplete-spinner" />` with no ARIA
   - User group: Screen reader users
   - Fix: Add `aria-busy="true"` on wrapper; add sr-only "Loading suggestions" text

## Difficulty Level

**ADVERSARIAL** — Automated tools find no issues (all elements are labeled, contrast passes on main elements). The bugs are in timing behavior and interaction patterns: the 800ms timeout is the key adversarial element — it requires reasoning about motor/cognitive timing needs.

## Frameworks

React 18+, CSS
