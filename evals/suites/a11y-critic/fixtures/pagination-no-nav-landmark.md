# Fixture: Pagination Controls Without nav Landmark

## Component Code

```jsx
import React from 'react';

const BuggyPagination = ({ currentPage, totalPages, onPageChange }) => {
  return (
    <div className="pagination-container">
      {/* BUG: No <nav> element — pagination is navigation but uses div */}
      {/* BUG: No aria-label describing pagination purpose */}
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        aria-label={`Previous page`}
      >
        Previous
      </button>

      {/* BUG: Page numbers are displayed without context */}
      <div className="page-numbers">
        {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
          <button
            key={page}
            onClick={() => onPageChange(page)}
            // BUG: No aria-current="page" to identify current page
            // BUG: No indication that these are page numbers
            className={page === currentPage ? 'active' : ''}
            aria-label={`Page ${page}`}
          >
            {page}
          </button>
        ))}
      </div>

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        aria-label={`Next page`}
      >
        Next
      </button>
    </div>
  );
};

export default BuggyPagination;
```

## Expected Behavior

- Previous/Next buttons navigate pages
- Current page is highlighted and announced as current
- Screen reader identifies as pagination navigation
- Page numbers presented with context
- Landmark allows quick navigation to pagination

## Accessibility Features Present

✓ aria-label on Previous/Next buttons
✓ aria-label on page buttons
✓ disabled state on edge buttons

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Missing <nav> landmark** — Pagination is navigation but uses div. Screen reader user cannot identify as pagination landmark. Per HTML semantics, pagination should be wrapped in <nav> with aria-label to create navigation landmark.
   - Evidence: `pagination-no-nav-landmark.md:5-6` (div instead of nav)
   - User group: Screen reader users (critical)
   - Expected: Pagination should be wrapped in <nav>
   - Fix: Replace div with <nav> element

2. **MAJOR: Missing aria-label on nav landmark** — Navigation landmark needed to describe pagination purpose. Screen reader user navigating landmarks hears "navigation" without knowing it's pagination. aria-label="Pagination" would clarify.
   - Evidence: `pagination-no-nav-landmark.md:5-6` (nav has no aria-label)
   - User group: Screen reader users
   - Expected: <nav> should have aria-label="Pagination"
   - Fix: Add aria-label="Pagination" to nav element

3. **MAJOR: Missing aria-current="page" on current page** — Current page button should announce as current using aria-current="page". Without it, screen reader user cannot quickly identify which page is active beyond visual styling.
   - Evidence: `pagination-no-nav-landmark.md:20-26` (no aria-current attribute)
   - User group: Screen reader users
   - Expected: Active page button should have aria-current="page"
   - Fix: Add aria-current={page === currentPage ? "page" : undefined}

## Difficulty Level

**HAS-BUGS** — Missing navigation landmark and state announcement. Pagination works but lacks semantic structure.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Difficulty Rating

A11y-critic should recognize that pagination is a navigation pattern that requires <nav> landmark and proper state management for screen reader users.
