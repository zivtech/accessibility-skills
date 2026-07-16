# Fixture: Analytics Dashboard with Structural Inconsistencies

## Component Code

```jsx
import React from 'react';

const AnalyticsDashboard = () => {
  return (
    <div className="dashboard">
      <div className="sidebar">
        <ul aria-label="Main navigation">
          <li><a href="/dashboard" className="nav-link active">Overview</a></li>
          <li><a href="/analytics" className="nav-link">Analytics</a></li>
          <li><a href="/reports" className="nav-link">Reports</a></li>
          <li><a href="/settings" className="nav-link">Settings</a></li>
        </ul>
      </div>

      <div className="content">
        <h1>Analytics Overview</h1>

        <div className="metrics-grid">
          <div className="metric-card">
            <h3>Total Users</h3>
            <div className="metric-value">24,521</div>
            <div className="metric-label">+12.3% from last month</div>
          </div>

          <div className="metric-card">
            <h2>Active Sessions</h2>
            <div className="metric-value">1,847</div>
            <div className="metric-label">Live right now</div>
          </div>

          <div className="metric-card">
            <h3>Bounce Rate</h3>
            <div className="metric-value">34.2%</div>
            <div className="metric-label">-2.1% from last month</div>
          </div>

          <div className="metric-card">
            <h2>Avg. Session Duration</h2>
            <div className="metric-value">4m 32s</div>
            <div className="metric-label">+18s from last month</div>
          </div>
        </div>

        <div className="tables-section">
          <div className="table-card">
            <h3>Traffic by Source</h3>
            <table className="data-table">
              <caption>Visitors grouped by traffic source for the current month</caption>
              <thead>
                <tr>
                  <th>Source</th>
                  <th>Visitors</th>
                  <th>Bounce Rate</th>
                  <th>Avg. Duration</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th>Organic Search</th>
                  <td>12,840</td>
                  <td>31.2%</td>
                  <td>5m 12s</td>
                </tr>
                <tr>
                  <th>Direct</th>
                  <td>6,230</td>
                  <td>28.5%</td>
                  <td>6m 45s</td>
                </tr>
                <tr>
                  <th>Social Media</th>
                  <td>3,890</td>
                  <td>42.1%</td>
                  <td>2m 58s</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="table-card">
            <h2>Top Pages</h2>
            <table className="data-table">
              <caption>Most visited pages ranked by pageviews this month</caption>
              <thead>
                <tr>
                  <th>Page</th>
                  <th>Pageviews</th>
                  <th>Unique Visitors</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th>/home</th>
                  <td>8,420</td>
                  <td>6,105</td>
                </tr>
                <tr>
                  <th>/pricing</th>
                  <td>4,210</td>
                  <td>3,890</td>
                </tr>
                <tr>
                  <th>/docs/getting-started</th>
                  <td>3,780</td>
                  <td>2,640</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;
```

## CSS

```css
.dashboard {
  display: flex;
  min-height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  color: #1e293b;
}

.sidebar {
  width: 240px;
  background: #0f172a;
  padding: 24px 0;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-link {
  display: block;
  padding: 12px 24px;
  color: #94a3b8;
  text-decoration: none;
  font-size: 14px;
}

.nav-link:hover,
.nav-link.active {
  color: #f8fafc;
  background: #1e293b;
}

.content {
  flex: 1;
  padding: 32px;
  background: #f8fafc;
}

.content h1 {
  font-size: 28px;
  margin: 0 0 24px;
}

.metric-card h2,
.metric-card h3,
.table-card h2,
.table-card h3 {
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0 0 8px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.metric-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.metric-value {
  font-size: 32px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 4px;
}

.metric-label {
  font-size: 13px;
  color: #94a3b8;
}

.tables-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.table-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 12px;
}

.data-table th,
.data-table td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
  font-size: 14px;
}

.data-table thead th {
  font-weight: 600;
  color: #475569;
  background: #f8fafc;
}

.data-table tbody th {
  font-weight: 500;
  color: #334155;
}

.data-table tbody td {
  color: #64748b;
}
```

## Expected Behavior

- Dashboard displays sidebar navigation, metric cards, and data tables
- Content sections are visually organized with consistent card styling
- Headings identify each section and card
- Tables show structured data with row and column relationships
- Screen reader users can navigate the dashboard by landmarks and headings

## Accessibility Features Present

✓ Semantic heading elements (h1, h2, h3) used for titles
✓ `aria-label` on sidebar navigation list
✓ `<table>` with `<thead>`, `<tbody>`, `<th>`, `<td>` structure
✓ `<caption>` on both data tables describing their purpose
✓ `<th>` used for both column headers and row headers in tables
✓ Ordered list for navigation links

## Accessibility Issues (Planted)

1. **MAJOR: Heading hierarchy inconsistent — h1 → h3 (skipping h2) in some cards, h2 in others** — The page has an `<h1>` for the dashboard title. Two metric cards use `<h3>` (Total Users, Bounce Rate), skipping h2. Two other metric cards use `<h2>` (Active Sessions, Avg. Session Duration). One table card uses `<h3>` (Traffic by Source), the other uses `<h2>` (Top Pages). The CSS styles h2 and h3 identically (same font-size, weight, color, text-transform), so visually they look consistent — but the heading tree is broken.
   - Evidence: `dashboard-heading-inconsistency.md:25` (h3 "Total Users"), `dashboard-heading-inconsistency.md:31` (h2 "Active Sessions"), `dashboard-heading-inconsistency.md:37` (h3 "Bounce Rate"), `dashboard-heading-inconsistency.md:43` (h2 "Avg. Session Duration"), `dashboard-heading-inconsistency.md:51` (h3 "Traffic by Source"), `dashboard-heading-inconsistency.md:86` (h2 "Top Pages")
   - WCAG: 1.3.1 Info and Relationships — heading hierarchy must be logical and consistent
   - User group: Screen reader users navigating by heading level (pressing `2` for h2, `3` for h3)
   - Impact: Screen reader user pressing `2` finds only half the cards. Pressing `3` finds the other half. The heading tree shows a jumbled structure with no logic to which cards are h2 vs h3. Users can't build a mental model of the page from headings alone.
   - Fix: All card headings should be `<h2>` (direct children of the h1 page title)

2. **MAJOR: Data table headers missing scope attributes** — Both tables use `<th>` for column headers (in `<thead>`) and row headers (first cell in each `<tbody>` row), but none have `scope="col"` or `scope="row"`. Tables have captions, so a surface check sees "table has caption and th elements — looks good." But without scope, a screen reader navigating by cell cannot associate data cells with their headers.
   - Evidence: `dashboard-heading-inconsistency.md:56-59` (Traffic table: column `<th>` without scope), `dashboard-heading-inconsistency.md:64,70,76` (Traffic table: row `<th>` without scope), `dashboard-heading-inconsistency.md:91-93` (Top Pages table: column `<th>` without scope), `dashboard-heading-inconsistency.md:98,103,108` (Top Pages table: row `<th>` without scope)
   - WCAG: 1.3.1 Info and Relationships — table headers must identify their scope
   - User group: Screen reader users navigating tables with Ctrl+Alt+arrow keys
   - Impact: When a screen reader user moves to a data cell, they hear the value but not which column or row it belongs to. In the Traffic table, hearing "31.2%" without knowing it's the Bounce Rate for Organic Search is meaningless.
   - Fix: Add `scope="col"` to all `<th>` in `<thead>`, add `scope="row"` to all `<th>` in `<tbody>`

3. **MINOR: Metric cards use divs for key-value pairs instead of semantic structure** — Each metric card presents a label-value relationship ("Total Users" → "24,521" → "+12.3% from last month") using plain divs with class names. Screen reader users hear a flat sequence of text with no semantic relationship between the heading, value, and change description. A `<dl>/<dt>/<dd>` or table structure would convey the label-value pairing programmatically.
   - Evidence: `dashboard-heading-inconsistency.md:26-27` (div.metric-value + div.metric-label, no semantic pairing)
   - WCAG: 1.3.1 Info and Relationships — information conveyed through presentation must be programmatically determinable
   - User group: Screen reader users
   - Impact: Low-to-moderate. Users can infer meaning from reading order, but the relationship between "24,521" and "Total Users" is visual, not semantic. With 4 cards in sequence, a screen reader user hears a stream of headings, numbers, and percentages with no structure separating one metric from another.
   - Fix: Use `<dl>` with `<dt>` for the metric name and `<dd>` for the value, or use a compact table structure

4. **MINOR: No landmark regions — missing `<main>`, `<nav>`, `<section>` labels** — The dashboard has no landmark regions at all. The sidebar is a `<div>` (not `<nav>`), the content area is a `<div>` (not `<main>`), and neither the metric grid nor the table sections use `<section>` with accessible names. Screen reader users pressing `D` (NVDA) or using the Rotor (VoiceOver) to navigate by landmark find nothing.
   - Evidence: `dashboard-heading-inconsistency.md:11` (sidebar: `<div>` not `<nav>`), `dashboard-heading-inconsistency.md:20` (content: `<div>` not `<main>`)
   - WCAG: 1.3.1 Info and Relationships, 2.4.1 Bypass Blocks
   - User group: Screen reader users, keyboard-only users
   - Impact: On a page with a sidebar and multiple content sections, landmarks are the primary way screen reader users orient themselves. Without them, the user must read linearly to understand page layout.
   - Fix: Wrap sidebar in `<nav aria-label="Main navigation">`, wrap content in `<main>`, optionally add `<section aria-label="...">` around the metrics grid and tables section

5. **ENHANCEMENT: No skip link to bypass sidebar navigation** — The dashboard has a sidebar with navigation links before the main content. Keyboard users must tab through all navigation links before reaching dashboard content. There is no skip link to jump directly to the main content area.
   - Evidence: `dashboard-heading-inconsistency.md:11-17` (sidebar comes first in DOM with 4 links, no skip mechanism)
   - WCAG: 2.4.1 Bypass Blocks
   - User group: Keyboard-only users, screen reader users
   - Impact: With only 4 links, the impact is moderate. On a real dashboard with more nav items, sub-menus, or filters, the impact compounds.
   - Fix: Add a visually-hidden skip link as the first focusable element: `<a href="#main-content" className="skip-link">Skip to dashboard content</a>` with `id="main-content"` on the content container

## Difficulty Level

**FLAWED** — The dashboard looks professional and "accessible enough" at first glance. It uses semantic headings, proper table elements with captions, aria-label on the sidebar list, and `<th>` for header cells. A surface-level audit checks off the obvious boxes and moves on.

The bugs are structural, not surface-level: heading hierarchy that's broken but visually hidden by identical CSS styling, scope attributes omitted from tables that already have captions, div-based metric layouts that look structured but aren't semantic, and missing landmarks on a page that has clear visual regions.

Expected baseline detection: 15-35%. A zero-shot reviewer sees headings (check), tables with captions and th elements (check), aria-label on the sidebar list (check) — and concludes the component passes. Finding the heading inconsistency requires comparing heading levels across cards. Finding the scope gap requires looking past the caption. Finding the div-based metrics requires understanding what semantic structure a screen reader needs to parse key-value pairs.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Notes

This fixture tests five distinct structural analysis skills:

1. **Heading tree analysis** (must_find) — Can the critic build the actual heading tree and detect that h2 and h3 are used inconsistently for peer-level content? The CSS deliberately styles them identically to remove visual cues.

2. **Table completeness beyond surface checks** (should_find) — Can the critic look past the caption and th elements to check scope attributes? Tables that "look structured" often get a pass.

3. **Semantic structure for data presentation** (should_find) — Can the critic identify that div-based key-value pairs in metric cards need semantic markup like `<dl>/<dt>/<dd>`?

4. **Landmark awareness** (nice_to_find) — Does the critic check for `<nav>`, `<main>`, and labeled `<section>` elements on a multi-region page?

5. **Bypass mechanism** (nice_to_find) — Does the critic check for skip links when sidebar navigation precedes main content?

The compounding effect matters: each issue alone is moderate, but together they mean a screen reader user encountering this dashboard has no landmarks, a broken heading tree, no semantic structure in the metric cards, and no column/row associations in the tables. The page is essentially unstructured to assistive technology despite looking well-organized visually.
