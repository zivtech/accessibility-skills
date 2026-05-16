# Fixture: Interactive Bar/Line Chart

## Feature Description

You're planning accessibility for an interactive chart component used on a public analytics dashboard. The component renders either a bar chart or line chart (switchable via a prop) using a custom SVG renderer. The chart has: a legend with colored swatches identifying data series, axis labels (X: months, Y: numeric values), a tooltip that appears on hover/focus and shows the exact data point value, and interactive data points (bars or nodes) that can be hovered. The chart is used to compare 3-5 data series across 12 months. Currently, the chart SVG has no ARIA attributes, the tooltip is hover-only, and there is no keyboard navigation or screen reader alternative.

## Context

- **Platform:** React SPA, custom SVG renderer (not a chart library like recharts or victory)
- **Existing code:** Yes — chart renders correctly visually; no ARIA, no keyboard navigation, no alternative formats
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA (Windows), JAWS (Windows), VoiceOver (macOS), keyboard-only users
- **Scope:** The chart component and its accessibility layer — visual, keyboard, screen reader, and reflow/zoom behaviors; does not include the data pipeline that feeds the chart
- **Constraints:** Custom SVG renderer must remain (no migration to recharts); the visual chart (colors, tooltips, animation) must remain unchanged; a data table fallback is acceptable as an addition; the chart will sometimes be embedded in a responsive container that narrows to 320px on mobile

## Requirement

Create a comprehensive accessibility design plan that a developer with no accessibility knowledge can use to implement the component correctly on the first attempt.

The plan should cover:
- Semantic structure
- ARIA implementation (pattern mapping, attributes)
- Keyboard interaction model
- Focus management
- State communication
- Visual accessibility (color alternatives, contrast, reflow)
- Content accessibility (screen reader alternative, data table)
- Testing strategy
- Implementation tasks with a11y-critic checkpoints

## Scope Hints

This is an **AMBIGUOUS** difficulty fixture — there is no single correct approach to chart accessibility. Multiple valid strategies exist (SVG title/desc, role="img" + aria-label summary, keyboard-navigable data points, ARIA grid for bar groups, full HTML table fallback, or a combination). The plan must choose an approach, justify it, and make it internally coherent. A plan that lists all possible approaches without committing to one will score lower than a plan that commits and explains. The plan length will vary by chosen approach, typically 3-5 pages. Focus on:

1. Chart as a whole: choose between `role="img"` with a summary `aria-label`, or a structured navigation model. Both are valid — justify the choice
2. Color in the legend: 3-5 colored swatches distinguish data series — cite WCAG 1.4.1, add pattern fill or text labels as non-color alternatives
3. Keyboard navigation: if data points are keyboard-navigable, specify the interaction model (Arrow keys to move between data points, focus ring on the focused bar/node); if choosing the table fallback instead, explain why keyboard nav within SVG is deferred
4. Screen reader data access: choose one strategy (long description, visually hidden data table, or aria-describedby to a summary) and implement it — do not list all three
5. Tooltip: hover-only tooltip fails WCAG 1.4.13 (Content on Hover or Focus) — plan keyboard-triggerable tooltip equivalent
6. Reflow at 320px: the chart must not require horizontal scrolling at 320px CSS width; address WCAG 1.4.10 (Reflow)

## What Success Looks Like

An excellent plan would:
- ✓ Choose a specific accessibility architecture (e.g., `role="img"` + summary + hidden data table) and justify the tradeoff explicitly
- ✓ Cite WCAG 1.4.1 (Use of Color) for the legend swatches and specify a concrete alternative (pattern fill, direct label, or text-only legend)
- ✓ Address WCAG 1.4.13 (Content on Hover or Focus) — tooltip must appear on keyboard focus, not only on hover; specify how tooltips render on focus
- ✓ Cite WCAG 1.4.10 (Reflow) and plan a chart behavior at 320px (scrollable container, simplified chart, or data table shown at narrow viewport)
- ✓ Specify the screen reader data access path — e.g., a `<table>` element with `class="sr-only"` containing the chart data in tabular form
- ✓ Document what the chart SVG root element's ARIA attributes will be and what `aria-label` will say
- ✓ If keyboard navigation is planned: specify the key model (Tab to chart, Arrow keys between data points, Enter/Space for tooltip, Escape to exit) and how `aria-activedescendant` or direct focus management works

## What Would Be Below Expectations

- ✗ Listing all possible approaches (SVG desc, ARIA grid, data table) without choosing one
- ✗ Adding a single `alt` string to the SVG root that describes the visual appearance ("A bar chart with blue and red bars") rather than the data
- ✗ Missing the tooltip/hover content problem (1.4.13) — tooltip is hover-only, that's a WCAG failure
- ✗ No plan for the legend color swatch problem (1.4.1 — color alone distinguishes series)
- ✗ WCAG 1.4.10 (Reflow at 320px) not addressed
- ✗ "Provide a data table" without specifying how it is linked to the chart, where it renders, and how it is styled for screen readers vs. sighted users
- ✗ No WCAG citations at all (common in ambiguous fixtures where the evaluator hedges)
- ✗ Over-specifying complex SVG ARIA patterns without considering the simpler, more robust data table alternative
