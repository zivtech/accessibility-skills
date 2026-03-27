# Fixture: Breadcrumb Navigation Without nav Landmark

## Component Code

```jsx
import React from 'react';

const BuggyBreadcrumb = ({ items = [] }) => {
  return (
    <div className="breadcrumb-container">
      {/* BUG: No <nav> landmark to identify this as navigation */}
      {/* BUG: No aria-label to describe the breadcrumb purpose */}
      {/* Screen reader just sees a list without knowing it's breadcrumb navigation */}
      <ol className="breadcrumb-list">
        {items.map((item, idx) => (
          <li key={idx} className="breadcrumb-item">
            {item.current ? (
              <span aria-current="page">{item.label}</span>
            ) : (
              <a href={item.href}>{item.label}</a>
            )}
            {/* BUG: Using "/" as visual separator, not screen reader accessible */}
            {idx < items.length - 1 && (
              <span className="breadcrumb-separator" aria-hidden="true">/</span>
            )}
          </li>
        ))}
      </ol>
    </div>
  );
};

export default BuggyBreadcrumb;
```

## Expected Behavior

- Breadcrumb shows navigation path (e.g., Home > Products > Shoes)
- Screen reader identifies as navigation landmark
- aria-current="page" marks current page
- Separators are visual-only (aria-hidden)
- Screen reader user can understand location in site structure

## Accessibility Features Present

✓ aria-current="page" on current item
✓ aria-hidden on separators
✓ <ol> semantic list

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Missing <nav> landmark** — Breadcrumb is just a div, not a navigation landmark. Screen reader user does not identify it as site navigation. Per HTML Breadcrumb Pattern, breadcrumbs should be wrapped in <nav> to create a navigation landmark.
   - Evidence: `breadcrumb-navigation-no-nav-landmark.md:5-6` (div instead of nav)
   - User group: Screen reader users (critical for orientation)
   - Expected: Breadcrumb should be wrapped in <nav>
   - Fix: Replace div with <nav> element

2. **MAJOR: Missing aria-label on nav** — Navigation landmark exists but has no descriptive label. Screen reader user navigating by landmarks hears "navigation" but not "breadcrumb". Per landmark semantics, <nav> should have aria-label="Breadcrumb" to distinguish from other nav regions.
   - Evidence: `breadcrumb-navigation-no-nav-landmark.md:5-6` (nav has no aria-label)
   - User group: Screen reader users
   - Expected: <nav> should have aria-label="Breadcrumb"
   - Fix: Add aria-label="Breadcrumb" to nav element

3. **MINOR: Potential confusion with visual separators** — While separators use aria-hidden, the ordered list structure with separators may be confusing. Could be clarified with aria-label on nav or breadcrumb structure documentation.
   - Evidence: `breadcrumb-navigation-no-nav-landmark.md:20-22` (separators are visual only)
   - User group: Screen reader users
   - Expected: List structure clear, but context helpful
   - Fix: Ensure list context clearly communicates breadcrumb purpose

## Difficulty Level

**HAS-BUGS** — Missing navigation landmark. Breadcrumb content is present but not properly marked as navigation.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Difficulty Rating

A11y-critic should recognize that this is a navigation landmark pattern issue. Many developers overlook <nav> because breadcrumbs work visually and function with links. But without <nav>, screen reader users lose navigation context.
