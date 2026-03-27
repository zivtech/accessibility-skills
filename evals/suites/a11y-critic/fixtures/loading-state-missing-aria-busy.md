# Fixture: Loading State Without aria-busy or Announcement

## Component Code

```jsx
const DataLoader = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [data, setData] = useState(null);

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setData({ content: 'Loaded data' });
      setIsLoading(false);
    }, 2000);
  }, []);

  return (
    <div className="data-container">
      {/* BUG: No aria-busy, no role="status", no aria-live */}
      {isLoading && (
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading data...</p>
        </div>
      )}

      {!isLoading && data && (
        <div className="data-content">
          <h2>Results</h2>
          <p>{data.content}</p>
        </div>
      )}
    </div>
  );
};

export default DataLoader;
```

## CSS

```css
.data-container {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
}

.loading-spinner {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.spinner {
  width: 30px;
  height: 30px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #0066cc;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.data-content {
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.data-content h2 {
  margin-top: 0;
}
```

## Expected Behavior

- Shows loading spinner for 2 seconds
- Displays loaded data after loading completes
- User understands when content is loading vs loaded

## Accessibility Issues (Planted)

1. **CRITICAL: Loading state not communicated to screen readers** — The spinner appears visually but screen reader user has no way to know content is loading. No aria-busy, no aria-live, no role="status". Screen reader announces "Results" content immediately (before it loads), creating confusion.
   - Evidence: `loading-state-missing-aria-busy.md:6-18` (no aria-busy, no live region, no announcement)
   - WCAG citation: 4.1.3 Status Messages (loading state is a status message that must be announced)
   - User group: Screen reader users
   - Expected: Container should have aria-busy="true" while loading, aria-busy="false" when complete
   - Fix: Add aria-busy="true" to data-container while isLoading, change to false when loaded. Consider aria-live="polite" for explicit announcement.

2. **MAJOR: No clear loading state indication** — Visual loading spinner shown, but only as animated element. Screen reader has no way to determine page is in loading state vs fully loaded.
   - Evidence: `loading-state-missing-aria-busy.md:12-18` (isLoading state only controls visibility, not ARIA)
   - WCAG citation: 4.1.3 Status Messages
   - User group: Screen reader users
   - Expected: Use aria-busy or role="status" with aria-live to communicate loading state
   - Fix: Add aria-busy attribute or wrap loading message in role="status" aria-live="polite"

## Difficulty Level

**HAS-BUGS** — A common issue. Visual loading indicators are common but screen reader announcements are forgotten.
