# Fixture: Search Results with Live Region (CLEAN)

## Component Code

```jsx
import React, { useState } from 'react';

const SearchResults = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    setResults([]);

    // Simulate API call
    setTimeout(() => {
      const mockResults = [
        { id: 1, title: 'Result 1', description: 'Description for result 1' },
        { id: 2, title: 'Result 2', description: 'Description for result 2' },
        { id: 3, title: 'Result 3', description: 'Description for result 3' },
      ];
      setResults(mockResults);
      setIsLoading(false);
    }, 500);
  };

  return (
    <div className="search-container">
      <form onSubmit={handleSearch}>
        <label htmlFor="search-input">Search</label>
        <input
          id="search-input"
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for..."
          aria-label="Search query"
        />
        <button type="submit">Search</button>
      </form>

      {/* Live region announces search status */}
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      >
        {isLoading && 'Searching...'}
        {!isLoading && results.length > 0 && `Found ${results.length} results`}
        {!isLoading && results.length === 0 && query && 'No results found'}
      </div>

      {isLoading && <p className="loading">Searching...</p>}

      {results.length > 0 && (
        <div className="results-container">
          <h2>Search Results</h2>
          <ul className="results-list">
            {results.map((result) => (
              <li key={result.id}>
                <h3>{result.title}</h3>
                <p>{result.description}</p>
              </li>
            ))}
          </ul>
        </div>
      )}

      {!isLoading && results.length === 0 && query && (
        <p className="no-results">No results found for "{query}"</p>
      )}
    </div>
  );
};

export default SearchResults;
```

## CSS

```css
.search-container {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
}

.search-container form {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.search-container label {
  display: none; /* Hidden but accessible */
}

.search-container input {
  flex: 1;
  padding: 10px;
  border: 2px solid #0066cc;
  border-radius: 4px;
  font-size: 16px;
}

.search-container button {
  padding: 10px 20px;
  background-color: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
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

.loading {
  color: #0066cc;
  font-style: italic;
}

.results-container {
  margin-top: 20px;
}

.results-container h2 {
  font-size: 18px;
  color: #333;
  margin-bottom: 16px;
}

.results-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.results-list li {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 16px;
  margin-bottom: 12px;
}

.results-list h3 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #0066cc;
}

.results-list p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.no-results {
  color: #666;
  font-style: italic;
  padding: 20px;
  text-align: center;
}
```

## Expected Behavior

- Form has input and button
- Entering query and submitting shows loading message
- After delay, displays search results
- Live region announces "Searching..." and "Found X results"
- Screen reader announces dynamic content updates

## Accessibility Features Implemented

✓ role="status" on live region (announces updates)
✓ aria-live="polite" (non-intrusive announcements)
✓ aria-atomic="true" (entire message announced)
✓ Label associated with input (htmlFor)
✓ Clear heading for results section
✓ Results in semantic list structure
✓ Loading message both visual and announced
✓ No results message announced

## Difficulty Level

**CLEAN** — Proper implementation of live regions and dynamic content announcement. Should receive clean verdict.

## Notes

A11y-critic should verify role="status", aria-live, and aria-atomic are all present and correct. Loading state is communicated both visually and programmatically. Results are announced. No critical gaps.
