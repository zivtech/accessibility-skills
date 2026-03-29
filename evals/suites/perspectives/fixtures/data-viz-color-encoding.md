# Fixture: Data Visualization With Color-Only Series Encoding

## Component Code

```jsx
import React, { useState } from 'react';

const REGIONS = [
  { name: 'North America', value: 420, fill: '#1565c0' },
  { name: 'Europe',        value: 380, fill: '#2e7d32' },
  { name: 'Asia Pacific',  value: 310, fill: '#e65100' },
  { name: 'Latin America', value: 180, fill: '#6a1b9a' },
  { name: 'Africa & ME',   value: 95,  fill: '#c62828' },
];

const CHART_W = 600, CHART_H = 300, PAD = 50;
const maxVal = Math.max(...REGIONS.map(r => r.value));

const RevenueChart = () => {
  const [tooltip, setTooltip] = useState(null);

  const barW = (CHART_W - PAD * 2) / REGIONS.length - 12;

  return (
    <section className="chart-section">
      <h2>Q1 2026 Revenue by Region</h2>

      {/* BUG: SVG has no role="img" or aria-label — inaccessible to screen readers */}
      <svg
        width={CHART_W}
        height={CHART_H + 60}
        className="revenue-chart"
      >
        {/* BUG: Y-axis labels at 10px — below comfortable reading size */}
        {[0, 100, 200, 300, 400, 500].map(tick => (
          <text
            key={tick}
            x={PAD - 8}
            y={CHART_H - (tick / maxVal) * (CHART_H - PAD) + 4}
            textAnchor="end"
            fontSize="10"
            fill="#666"
          >
            ${tick}M
          </text>
        ))}

        {REGIONS.map((region, i) => {
          const barH = (region.value / maxVal) * (CHART_H - PAD);
          const x = PAD + i * (barW + 12);
          const y = CHART_H - barH;

          return (
            <g key={region.name}>
              {/* BUG: Bars use fill color as sole series differentiator —
                  no pattern fills, no direct value labels on bars — WCAG 1.4.1 */}
              {/* BUG: onMouseEnter shows tooltip but no onFocus — keyboard users
                  cannot access values — WCAG 2.1.1, 1.4.13 */}
              <rect
                x={x}
                y={y}
                width={barW}
                height={barH}
                fill={region.fill}
                onMouseEnter={() => setTooltip({ x: x + barW / 2, y: y - 10, text: `${region.name}: $${region.value}M` })}
                onMouseLeave={() => setTooltip(null)}
              />
              <text
                x={x + barW / 2}
                y={CHART_H + 16}
                textAnchor="middle"
                fontSize="11"
                fill="#333"
              >
                {region.name}
              </text>
            </g>
          );
        })}

        {tooltip && (
          <g>
            <rect x={tooltip.x - 60} y={tooltip.y - 22} width={120} height={24} rx={4} fill="#333" />
            <text x={tooltip.x} y={tooltip.y - 6} textAnchor="middle" fontSize="12" fill="#fff">
              {tooltip.text}
            </text>
          </g>
        )}
      </svg>

      {/* BUG: Legend uses small colored squares only — no shape/pattern mapping */}
      <div className="legend">
        {REGIONS.map(r => (
          <div key={r.name} className="legend-item">
            <span className="legend-swatch" style={{ backgroundColor: r.fill }} />
            <span className="legend-label">{r.name}</span>
          </div>
        ))}
      </div>
    </section>
  );
};

export default RevenueChart;
```

```css
.chart-section {
  max-width: 680px;
  margin: 0 auto;
  font-family: system-ui, sans-serif;
}

.chart-section h2 {
  font-size: 1.25rem;
  margin-bottom: 12px;
}

/* All fill colors pass contrast against white — automated tools won't flag */
/* #1565c0 = 5.4:1, #2e7d32 = 5.9:1, #e65100 = 4.6:1, #6a1b9a = 7.2:1, #c62828 = 5.6:1 */

.legend {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin-top: 12px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
}

/* BUG: Swatch is color-only — no shape, no pattern fill, no icon */
.legend-swatch {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 2px;
}
```

## Expected Behavior

- Bar chart displays revenue for 5 regions with labeled X-axis
- Hovering a bar shows a tooltip with region name and revenue figure
- Legend maps colors to region names
- Y-axis shows dollar amounts in millions

## Accessibility Features Present

- Heading structure (h2 for chart title)
- Region names on X-axis as text labels
- Legend includes text names alongside color swatches
- Page-level landmarks are correct

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: 5 data series distinguished only by fill color — WCAG 1.4.1 (Use of Color)**
   Bars use fill color as the sole differentiator between regions. No pattern fills, no direct value labels on bars, no shape variation. Color-blind users (protanopia, deuteranopia) cannot distinguish blue from purple, or red from green/orange. All colors pass contrast ratio checks — automated tools will not flag this.
   - Evidence: Lines 50-58 — `<rect fill={region.fill}>` with no pattern or label overlay
   - User group: Color-blind users, monochrome display users
   - Fix: Add direct value labels on each bar, or use pattern fills (hatching, dots) alongside color

2. **MAJOR: Hover tooltips on SVG bars with no keyboard/focus equivalent — WCAG 2.1.1 (Keyboard), 1.4.13 (Content on Hover)**
   Bar values are only accessible via mouse hover (`onMouseEnter`). SVG rect elements have no tabIndex, no onFocus handler. Keyboard users cannot access individual bar values.
   - Evidence: Lines 53-55 — `onMouseEnter` handler with no focus equivalent; rect has no tabIndex
   - User group: Keyboard users, screen reader users
   - Fix: Add `tabIndex={0}` and `onFocus` handler to each rect; add `role="img"` and `aria-label` per bar

3. **MAJOR: Legend uses colored squares only — no text-shape mapping — WCAG 1.4.1**
   Legend items pair a colored square with a region name, but color is the sole visual mapping between legend and chart bars. No shape, pattern, or numbering connects legend to bars.
   - Evidence: CSS `.legend-swatch` — 12x12px colored square with no pattern
   - User group: Color-blind users
   - Fix: Use distinct shapes (circle, square, triangle, diamond, cross) or pattern fills matching the bars

4. **MINOR: SVG element has no accessible name — WCAG 1.1.1 (Non-text Content)**
   The `<svg>` element has no `role="img"` and no `aria-label`. Screen readers may skip or announce it generically.
   - Evidence: Line 28 — `<svg>` with only width/height/className
   - User group: Screen reader users
   - Fix: Add `role="img" aria-label="Bar chart: Q1 2026 Revenue by Region"`

5. **MINOR: Y-axis labels at 10px font size — WCAG 1.4.4 (Resize Text)**
   Y-axis tick labels are rendered at `fontSize="10"` in SVG. At this size they are difficult to read for low-vision users and don't scale with browser zoom (SVG text doesn't respond to `rem`/`em`).
   - Evidence: Line 37 — `fontSize="10"` on Y-axis text elements
   - User group: Low-vision users, magnification users
   - Fix: Increase to at least 12px; consider rendering Y-axis labels as HTML overlays

## Difficulty Level

**HAS-BUGS** — New dimension: Environmental Contrast. All chart colors pass automated contrast checks. The failure is color-as-sole-differentiator (WCAG 1.4.1), which requires reasoning beyond contrast ratio analysis. A reviewer focused only on ARIA patterns will note the missing SVG accessible name but miss the core color-only encoding issue.

## Frameworks

React 18+, SVG, CSS
