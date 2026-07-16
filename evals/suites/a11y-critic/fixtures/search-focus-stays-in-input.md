# Fixture: Search with Focus Retained in Input During Live Results

## Component Code

```jsx
import React, { useState, useRef, useCallback, useEffect } from 'react';

const LiveSearch = ({ onSearch }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [resultCount, setResultCount] = useState(null);
  const inputRef = useRef(null);
  const listRef = useRef(null);
  const debounceRef = useRef(null);

  const performSearch = useCallback(async (searchTerm) => {
    if (!searchTerm.trim()) {
      setResults([]);
      setResultCount(null);
      return;
    }
    // Simulate API search
    const mockResults = [
      { id: 'r1', title: 'Getting started guide', url: '/docs/getting-started' },
      { id: 'r2', title: 'API reference', url: '/docs/api' },
      { id: 'r3', title: 'Configuration options', url: '/docs/config' },
      { id: 'r4', title: 'Troubleshooting common errors', url: '/docs/troubleshooting' },
    ].filter(r => r.title.toLowerCase().includes(searchTerm.toLowerCase()));
    setResults(mockResults);
    setResultCount(mockResults.length);
  }, []);

  const handleInputChange = (e) => {
    const value = e.target.value;
    setQuery(value);

    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => {
      performSearch(value);
    }, 300);
  };

  const handleKeyDown = (e) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        if (results.length > 0 && listRef.current) {
          const firstLink = listRef.current.querySelector('a');
          if (firstLink) firstLink.focus();
        }
        break;
      case 'Escape':
        e.preventDefault();
        setQuery('');
        setResults([]);
        setResultCount(null);
        inputRef.current?.focus();
        break;
      default:
        break;
    }
  };

  const handleResultKeyDown = (e, index) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        const nextLink = listRef.current?.querySelectorAll('a')[index + 1];
        if (nextLink) nextLink.focus();
        break;
      case 'ArrowUp':
        e.preventDefault();
        if (index === 0) {
          inputRef.current?.focus();
        } else {
          const prevLink = listRef.current?.querySelectorAll('a')[index - 1];
          if (prevLink) prevLink.focus();
        }
        break;
      case 'Escape':
        e.preventDefault();
        setQuery('');
        setResults([]);
        setResultCount(null);
        inputRef.current?.focus();
        break;
      default:
        break;
    }
  };

  useEffect(() => {
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, []);

  return (
    <div className="live-search">
      <label htmlFor="site-search" className="search-label">
        Search documentation
      </label>
      <input
        ref={inputRef}
        id="site-search"
        type="search"
        value={query}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
        placeholder="Type to search..."
        aria-autocomplete="list"
        aria-controls="search-results-list"
        aria-expanded={results.length > 0}
        autoComplete="off"
      />

      <div
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
        role="status"
      >
        {resultCount !== null && (
          resultCount === 0
            ? 'No results found'
            : `${resultCount} result${resultCount !== 1 ? 's' : ''} found`
        )}
      </div>

      {results.length > 0 && (
        <ul
          ref={listRef}
          id="search-results-list"
          role="listbox"
          aria-label={`Search results: ${resultCount} items`}
        >
          {results.map((result, index) => (
            <li key={result.id} role="option">
              <a
                href={result.url}
                onKeyDown={(e) => handleResultKeyDown(e, index)}
              >
                {result.title}
              </a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default LiveSearch;
```

## CSS

```css
.live-search {
  position: relative;
  max-width: 480px;
  margin: 0 auto;
}

.search-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 6px;
}

.live-search input[type="search"] {
  width: 100%;
  padding: 10px 14px;
  font-size: 16px;
  border: 2px solid #9ca3af;
  border-radius: 6px;
  background: #fff;
  color: #111827;
  box-sizing: border-box;
}

.live-search input[type="search"]:focus {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
  border-color: #2563eb;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

ul[role="listbox"] {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin: 4px 0 0;
  padding: 4px 0;
  list-style: none;
  background: #fff;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 100;
  max-height: 320px;
  overflow-y: auto;
}

ul[role="listbox"] li {
  margin: 0;
  padding: 0;
}

ul[role="listbox"] a {
  display: block;
  padding: 10px 14px;
  color: #1f2937;
  text-decoration: none;
  font-size: 15px;
}

ul[role="listbox"] a:hover,
ul[role="listbox"] a:focus {
  background: #eff6ff;
  color: #1d4ed8;
  outline: none;
}
```

## Expected Behavior

- Typing in the search input filters results after a 300ms debounce
- Results appear in a dropdown list below the input
- **Focus stays in the search input as results update** — user can keep typing
- `aria-live="polite"` region announces the result count ("4 results found")
- Pressing Down Arrow from the input moves focus to the first result link
- Pressing Up Arrow from the first result returns focus to the input
- Arrow Down/Up navigates through results
- Pressing Escape clears the search query and results, returns focus to input
- Tab from the input moves focus to the first result link (standard tab order)

## Accessibility Features Present

- Visible `<label>` associated with the search input via `htmlFor`
- `type="search"` provides native search semantics
- `aria-autocomplete="list"` communicates that results will appear as user types
- `aria-controls` links input to the results list
- `aria-expanded` reflects whether results are showing
- `role="status"` with `aria-live="polite"` and `aria-atomic="true"` announces result count
- `role="listbox"` on the results container with descriptive `aria-label`
- `role="option"` on each result item
- Arrow key navigation between input and results
- Escape clears and returns focus to input
- Visible focus indicators on both input and result links
- Debounced search prevents excessive announcements

## Design Rationale

The developer chose to keep focus in the search input because:

1. **Users are typing** — moving focus away from the input on every keystroke (or after debounce) would interrupt the typing flow and be disorienting
2. **Industry precedent** — Google Search, Algolia DocSearch, Spotlight, VS Code Command Palette all keep focus in the input while results update
3. **The aria-live region announces results** — screen reader users hear "4 results found" without needing focus to move
4. **Down Arrow is the explicit gesture** — when the user is ready to browse results, they press Down Arrow. This separates "still typing" from "ready to browse"
5. **Escape provides a clear exit** — the user can dismiss results and stay in the input at any time

## Accessibility Issues (None Planted — Design Tension)

**No planted bugs.** This is an ADVERSARIAL fixture: the accessibility question is the design tension analyzed below. Everything from this heading down is eval metadata kept below the blind cut line (runners strip this heading and all following sections from model prompts).

## The Ambiguity

Focus stays in the search input while results update dynamically below. The `aria-live="polite"` region announces how many results were found. The user must press Down Arrow (or Tab) to move into the results. This is a deliberate design decision, not an oversight — but it creates a real tension.

**Argument for keeping focus in input (defender — implemented approach):**
- Moving focus away from the input while the user is typing would be disorienting, potentially causing typed characters to be lost or interpreted as shortcuts
- The `aria-live` region announces the result count, so screen reader users know results appeared without focus moving
- Down Arrow is an explicit, intentional gesture that means "I'm done typing, show me what you found" — it respects user agency
- Every major search UI (Google, Algolia, macOS Spotlight, VS Code) uses this pattern; users have strong muscle memory for it
- The `aria-autocomplete="list"` attribute tells assistive technology that results will appear, priming SR users to expect the Down Arrow interaction

**Argument for moving focus to results (challenger):**
- `aria-live="polite"` announcements can be missed — screen readers suppress polite announcements when the user is actively interacting (typing generates speech output that may override the polite announcement)
- The live region says "4 results found" but does NOT describe what the results are — the user knows results exist but not their content
- Keyboard-only users must know the Down Arrow convention. There is no visible affordance or instruction telling them to press Down Arrow to reach results
- If the user presses Tab (the most universal keyboard navigation key), focus moves to the first result — but the `role="listbox"` pattern conventionally uses Arrow keys, not Tab. This creates a mixed interaction model
- Sighted users can visually scan results while typing; screen reader users cannot. The pattern optimizes for sighted users' workflow while requiring extra steps from SR users
- After the user stops typing and waits, there is no automatic announcement of what the results are — the user must take action to discover result content

**Why this is genuinely hard:**
The focus-stays-in-input pattern is an industry standard backed by strong UX rationale. But the screen reader experience is measurably different from the sighted experience: sighted users see results updating in real time while they type, while SR users hear only a count and must take explicit action to discover what was found. Whether that gap constitutes an accessibility problem or an acceptable tradeoff depends on how you weight user agency (letting the user choose when to browse) against information equivalence (sighted users get more information passively).

## Frameworks & Environment

React 18+, no specific framework beyond React

## Notes

This is an ADVERSARIAL fixture. The "correct" review is NOT to flag the focus behavior as a bug, but to:

1. Recognize the tension between keeping focus in the input (respecting user agency, industry convention) and moving focus to results (information equivalence for SR users)
2. Articulate both sides with specific reasoning about who is affected
3. Acknowledge the aria-live region as a genuine mitigation — then examine its limitations (polite announcements can be missed, count-only vs content description)
4. Make a recommendation with reasoning, while acknowledging the other approach is defensible
5. NOT treat this as a clear-cut accessibility violation — it is a design tradeoff

A reviewer that says "focus should move to results after search" without acknowledging why it stays in the input is as incomplete as a reviewer that says "this is fine, there's an aria-live region" without examining its limitations for SR users.
