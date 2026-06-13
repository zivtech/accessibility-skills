# Breadcrumb navigation

A breadcrumb trail showing the user's location within the site hierarchy. Renders an
ordered list of ancestor links ending in the current page.

## Files
- `component.jsx` — `Breadcrumbs` React component. Takes a `trail` array of
  `{ label, href }` and renders the final item as the current page.
- `styles.css` — layout, separators, link and focus styling.

## Expected behavior
- Ancestor items link to their pages; the final item is the current page (not a link).
- Keyboard users tab through the ancestor links in document order.
- The trail communicates the page's position within the overall site structure.
