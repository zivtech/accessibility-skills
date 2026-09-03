# Fixture: Tool Catalog Layout

## Recent Changes (PR #58)

Closes SHARE-40. Rebuilds the tool-catalog browsing page with a two-column
layout (filters on the left, results grid on the right) to match the new
brand refresh, and adds explicit spacing so the filter panel never collapses
awkwardly under the results grid regardless of window size.

## Component Code

```jsx
import React, { useState } from 'react';
import './ToolCatalogLayout.css';

const TOOLS = [
  { id: 'drill-201', name: 'Cordless Drill (18V)', category: 'Power Tools', available: true },
  { id: 'ladder-6ft', name: '6ft Step Ladder', category: 'Ladders', available: true },
  { id: 'tiller-01', name: 'Garden Tiller', category: 'Yard Tools', available: false },
  { id: 'saw-circ', name: 'Circular Saw', category: 'Power Tools', available: true },
  { id: 'pressure-wash', name: 'Pressure Washer', category: 'Cleaning', available: true },
  { id: 'wheelbarrow', name: 'Wheelbarrow', category: 'Yard Tools', available: true },
];

const ToolCatalogGrid = () => {
  const [category, setCategory] = useState('all');

  const filtered = category === 'all' ? TOOLS : TOOLS.filter((t) => t.category === category);

  return (
    <div className="tool-catalog-layout">
      <aside aria-labelledby="filters-heading" className="filter-sidebar">
        <h2 id="filters-heading">Filter by Category</h2>
        <fieldset>
          <legend>Category</legend>
          {['all', 'Power Tools', 'Ladders', 'Yard Tools', 'Cleaning'].map((cat) => (
            <label key={cat} className="filter-option">
              <input
                type="radio"
                name="category"
                value={cat}
                checked={category === cat}
                onChange={() => setCategory(cat)}
              />
              {cat === 'all' ? 'All tools' : cat}
            </label>
          ))}
        </fieldset>
      </aside>

      <section aria-labelledby="results-heading" className="tool-grid-section">
        <h2 id="results-heading">Available Tools ({filtered.length})</h2>
        <div className="tool-grid">
          {filtered.map((tool) => (
            <article key={tool.id} className="tool-card">
              <div className="tool-thumb" aria-hidden="true" />
              <h3>{tool.name}</h3>
              <p className="tool-category">{tool.category}</p>
              <p className={tool.available ? 'tool-status available' : 'tool-status unavailable'}>
                {tool.available ? 'Available now' : 'Currently checked out'}
              </p>
              <button className="reserve-button" disabled={!tool.available}>
                Reserve
              </button>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
};

export default ToolCatalogGrid;
```

## CSS

```css
.tool-catalog-layout {
  display: flex;
  min-width: 1024px;
  gap: 32px;
  max-width: 1280px;
  margin: 24px auto;
  padding: 0 24px;
  box-sizing: border-box;
}

.filter-sidebar {
  width: 280px;
  flex-shrink: 0;
  padding: 20px;
  border: 1px solid #dcdad3;
  border-radius: 8px;
}

.filter-sidebar fieldset {
  border: none;
  padding: 0;
  margin: 12px 0 0 0;
}

.filter-option {
  display: block;
  margin: 10px 0;
  font-size: 14px;
  color: #3a3a34;
}

.tool-grid-section {
  flex: 1;
  min-width: 0;
}

.tool-grid {
  display: flex;
  flex-wrap: nowrap;
  gap: 20px;
  overflow-x: visible;
}

.tool-card {
  width: 240px;
  flex-shrink: 0;
  border: 1px solid #dcdad3;
  border-radius: 8px;
  padding: 16px;
}

.tool-thumb {
  width: 208px;
  height: 140px;
  background: #e7e4da;
  border-radius: 6px;
  margin-bottom: 12px;
}

.tool-card h3 {
  font-size: 15px;
  margin: 0 0 4px 0;
  color: #23231f;
}

.tool-category {
  font-size: 13px;
  color: #6b6a60;
  margin: 0 0 8px 0;
}

.tool-status {
  font-size: 13px;
  font-weight: 600;
  margin: 0 0 12px 0;
}

.tool-status.available {
  color: #2f6b3f;
}

.tool-status.unavailable {
  color: #8a3a2a;
}

.reserve-button {
  width: 100%;
  padding: 8px;
  border: 1px solid #4a5a3a;
  background: #eef3e4;
  color: #2f3a20;
  border-radius: 6px;
  cursor: pointer;
}

.reserve-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

## Expected Behavior

- Members browse tools available to borrow, filtered by category using the left-hand panel.
- Each tool card shows a thumbnail, name, category, availability, and a Reserve button (disabled when checked out).
- The layout is a fixed two-column design: filter panel on the left, results grid on the right.

## Accessibility Features Present

✓ Filter options use fieldset/legend, not a bare group of radio inputs
✓ Both regions (filters, results) are headed by h2 elements connected via aria-labelledby
✓ Decorative thumbnail placeholders are aria-hidden
✓ Unavailable tools show text ("Currently checked out"), not only a color change, and their Reserve button is properly disabled
✓ Category count in the results heading updates as the filter changes

## Accessibility Issues

_Answer key: planted defects._

1. **MUST-FIND / MAJOR: The layout cannot reflow to a single column and produces two-dimensional scrolling at a 320px viewport width.** `.tool-catalog-layout` sets `min-width: 1024px`, and its two children add further rigidity: `.filter-sidebar` is a fixed `width: 280px`, and `.tool-grid` uses `flex-wrap: nowrap` with each `.tool-card` fixed at `width: 240px`. There is no media query anywhere in this stylesheet that changes any of these values. At a 320px-wide viewport (the standard WCAG 1.4.10 reflow test width), the page requires horizontal scrolling to read the filter panel and to reach tool cards beyond the first one, in addition to the page's normal vertical scroll through the tool list — genuine two-dimensional scrolling to browse a catalog that has no inherent need for a fixed two-dimensional layout (unlike, say, a data table or a map).
   - Evidence: `tool-catalog-layout.md` — `.tool-catalog-layout { min-width: 1024px; }`, `.filter-sidebar { width: 280px; }`, `.tool-grid { flex-wrap: nowrap; }`, `.tool-card { width: 240px; }`; no media queries present anywhere in the stylesheet
   - WCAG: 1.4.10 Reflow
   - Impact: Users who zoom to 400% (roughly equivalent to a 320px viewport at desktop scale) or who use a narrow-viewport mobile device must scroll in two directions to browse tools, read filter options, or reach the Reserve button on cards past the first column
   - User group: Low-vision users who zoom the page, mobile users, users with motor disabilities for whom two-directional scrolling is significantly more effortful than one-directional
   - Fix: Remove the container's `min-width`, let `.filter-sidebar` and `.tool-grid` reflow (e.g., stack vertically below a breakpoint, and let `.tool-grid` wrap or move to a responsive grid with flexible column widths), and add the media queries needed to make that happen at narrow viewports

2. **SHOULD-FIND / MAJOR: A `user-scalable=no` viewport meta tag would compound the reflow failure by blocking the zoom users need to compensate — verify the page's viewport meta tag does not disable pinch-zoom.** (This fixture's HTML shell is not shown above, but reviewers should treat "does the page allow pinch-zoom" as part of any 1.4.10/1.4.4 review; a fixed-width layout combined with zoom disabled leaves affected users with no workaround at all.) Separately and concretely present in this component: the filter option font-size and card text are all set in fixed `px` units throughout, with no relative sizing, which is consistent with a layout built without reflow or user text-scaling in mind.
   - Evidence: `tool-catalog-layout.md` — every font-size declaration in the stylesheet uses `px` (`13px`, `14px`, `15px`); no `rem`/`em`/relative units anywhere
   - WCAG: 1.4.4 Resize Text (compounding concern alongside 1.4.10)
   - Impact: Consistent with the broader pattern of this layout being built to a single fixed size rather than a range of viewport/zoom conditions
   - User group: Low-vision users who rely on browser text-resizing rather than full-page zoom
   - Fix: Convert font sizes to `rem` so they scale with the user's browser font-size setting, independent of the layout-reflow fix above

## Difficulty Level

**HAS-BUGS** — The reflow failure is a clear, unambiguous violation: `min-width: 1024px` on the outer container alone guarantees horizontal scroll below that width, and the fixed-width sidebar and non-wrapping card row reinforce it. This is a common, realistic mistake — a `min-width` added "so the two-column layout never looks cramped" without anyone testing the page at a narrow viewport or high zoom level.

## Frameworks & Environment

React 18+, standard CSS (Flexbox)

## Notes

This fixture isolates WCAG 1.4.10 (Reflow):

1. **The `min-width` on the container is the primary defect** — it alone is sufficient to fail reflow regardless of the children's own widths, since it caps how narrow the whole layout can ever become.
2. **False-positive resistance**: the tool thumbnail placeholders and card width being expressed in fixed pixels is not, by itself, the bug being tested — explicit image/thumbnail dimensions are a widely-recommended practice (preventing layout shift while images load) and are fine as long as the surrounding grid can still reflow around them. A reviewer who flags "the thumbnail has a fixed pixel size" as the accessibility defect, rather than the non-reflowing container and card row, has misidentified where the actual failure lives.
3. A tool catalog grid is not exempt content under 1.4.10 (unlike, e.g., a data table that inherently needs two-dimensional layout to remain meaningful) — cards can and should reflow to a single column at narrow widths.

Expected verdict: REVISE.
