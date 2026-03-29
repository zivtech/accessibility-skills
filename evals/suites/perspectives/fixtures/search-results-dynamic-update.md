# Fixture: Search Results With No Live Region Announcements

## Component Code

```jsx
import React, { useState, useEffect } from 'react';

const mockResults = [
  { id: 1, title: 'Getting Started with React', desc: 'A beginner guide to React components and hooks.', url: '/docs/react-intro' },
  { id: 2, title: 'React Performance Tips', desc: 'Optimize re-renders, memoize callbacks, and profile components.', url: '/docs/react-perf' },
  { id: 3, title: 'React Testing Library', desc: 'Write reliable tests with user-centric queries.', url: '/docs/react-testing' },
  { id: 4, title: 'State Management Patterns', desc: 'Context, reducers, and external stores compared.', url: '/docs/state-mgmt' },
  { id: 5, title: 'Server Components', desc: 'RSC architecture and when to use client vs server.', url: '/docs/rsc' },
  { id: 6, title: 'Accessibility in React', desc: 'ARIA patterns, focus management, and keyboard navigation.', url: '/docs/a11y' },
];

const SearchPage = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!query.trim()) { setResults([]); return; }
    setLoading(true);
    const timer = setTimeout(() => {
      const filtered = mockResults.filter(r =>
        r.title.toLowerCase().includes(query.toLowerCase()) ||
        r.desc.toLowerCase().includes(query.toLowerCase())
      );
      setResults(filtered);
      setLoading(false);
    }, 300);
    return () => clearTimeout(timer);
  }, [query]);

  return (
    <main className="search-page">
      <h1>Documentation Search</h1>

      <div className="search-bar">
        {/* BUG: input type="text" not type="search" — semantic issue */}
        <label htmlFor="search-input">Search documentation</label>
        <div className="input-wrapper">
          <input
            id="search-input"
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search..."
          />
          {query && (
            // BUG: Clear button has no aria-label — just "×" text
            <button className="clear-btn" onClick={() => setQuery('')}>×</button>
          )}
        </div>
      </div>

      {/* BUG: No aria-live on results container — SR users unaware results changed */}
      <section className="results-section" aria-label="Search results">
        {/* BUG: Count updates visually but no live region announces it */}
        <p className="results-count">
          {query ? `${results.length} results for "${query}"` : 'Enter a search term'}
        </p>

        {/* BUG: Loading spinner is CSS-only — no aria-busy, no SR text */}
        {loading && <div className="spinner" />}

        {!loading && results.map(r => (
          <article key={r.id} className="result-card">
            <h2><a href={r.url}>{r.title}</a></h2>
            <p>{r.desc}</p>
          </article>
        ))}

        {!loading && query && results.length === 0 && (
          <p className="no-results">No results found. Try different keywords.</p>
        )}
      </section>
    </main>
  );
};

export default SearchPage;
```

```css
.search-page {
  max-width: 680px;
  margin: 0 auto;
  padding: 32px 24px;
  font-family: system-ui, sans-serif;
}

.search-page h1 { font-size: 1.75rem; margin-bottom: 24px; }

.search-bar label { display: block; font-weight: 600; margin-bottom: 4px; }

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper input {
  width: 100%;
  padding: 10px 40px 10px 12px;
  border: 2px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

.input-wrapper input:focus {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}

/* BUG: Clear button — no aria-label, just × */
.clear-btn {
  position: absolute;
  right: 8px;
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  color: #666;
  padding: 4px 8px;
}

.clear-btn:focus-visible {
  outline: 2px solid #005fcc;
}

.results-count {
  font-size: 0.9rem;
  color: #555;
  margin: 16px 0 12px;
}

/* BUG: CSS-only spinner — no accessible text */
.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid #e0e0e0;
  border-top-color: #1565c0;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 16px auto;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.result-card {
  border-bottom: 1px solid #eee;
  padding: 12px 0;
}

.result-card h2 {
  font-size: 1.1rem;
  margin: 0 0 4px;
}

.result-card h2 a {
  color: #1565c0;
  text-decoration: underline;
}

.result-card h2 a:focus {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}

.result-card p {
  font-size: 0.9rem;
  color: #333;
  margin: 0;
}

.no-results {
  color: #666;
  font-style: italic;
  margin: 16px 0;
}
```

## Expected Behavior

- Search input filters results in real-time as user types
- Results count updates ("N results for 'query'")
- Loading spinner shows during fetch delay
- Clear button resets search
- Each result is a card with heading link and description

## Accessibility Features Present

- `<label>` associated with search input
- Results in `<section>` landmark with `aria-label`
- Each result is `<article>` with `<h2>` heading
- Links have descriptive text (article titles)
- Focus-visible on input, clear button, and result links
- Keyboard navigation between results works (Tab through links)
- `<main>` landmark wrapping the page

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: No aria-live on results container — WCAG 4.1.3 (Status Messages)**
   Results update dynamically as the user types, but the results section has no `aria-live` attribute. Screen reader users focused on the input are unaware that results changed below.
   - Evidence: Line 56 — `<section>` with `aria-label` but no `aria-live`
   - User group: Screen reader users
   - Fix: Add `aria-live="polite" aria-atomic="true"` to the results section or a dedicated status div

2. **MAJOR: "N results found" count updates visually but no live announcement**
   The count text at `<p className="results-count">` updates on each render but has no `aria-live` wrapper.
   - Evidence: Lines 58-60 — text updates dynamically with no live region
   - User group: Screen reader users
   - Fix: Wrap in `<div aria-live="polite">` or add a separate `sr-only` live region

3. **MAJOR: Loading spinner CSS-only — no aria-busy, no accessible text**
   `.spinner` is a CSS animation with no text content, no `aria-label`, and no `aria-busy` on the container.
   - Evidence: Lines 63-64 — `<div className="spinner" />` with no ARIA
   - User group: Screen reader users
   - Fix: Add `aria-busy="true"` to results section during load; add visually-hidden "Loading results" text

4. **MINOR: Search input type="text" not type="search"**
   Input uses `type="text"` instead of `type="search"`. The `search` type provides semantic meaning and often a native clear button.
   - Evidence: Line 41 — `type="text"`
   - User group: Screen reader users (semantic role)
   - Fix: Change to `type="search"`

5. **MINOR: Clear search button "×" has no aria-label**
   Button contains only "×" character with no `aria-label`. Screen readers announce "times" or the character name.
   - Evidence: Line 49 — `<button className="clear-btn">×</button>`
   - User group: Screen reader users
   - Fix: Add `aria-label="Clear search"`

## Difficulty Level

**HAS-BUGS** — Existing dimension: Screen Reader. The UI is visually correct and keyboard-navigable. The failures are all in dynamic announcement patterns (live regions, status messages) — classic screen reader issues the current skills should catch.

## Frameworks

React 18+, CSS
