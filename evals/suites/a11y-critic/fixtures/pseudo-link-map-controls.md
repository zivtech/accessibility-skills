# Fixture: Map Zoom and Reset Controls Are Anchors Posing as Buttons

## Component Code

```jsx
const WatershedMapPanel = () => {
  const handleZoomIn = () => console.log('zoom in');
  const handleZoomOut = () => console.log('zoom out');
  const handleReset = () => console.log('reset view');

  return (
    <section className="map-panel" aria-labelledby="map-heading">
      <h2 id="map-heading">Watershed Boundary Map</h2>

      {/* Third-party map library mounts its canvas here. The same boundary
          data is available to everyone through the table linked below, which
          is the map's text alternative rather than a fallback. */}
      <div className="map-canvas" />

      <p className="map-alt-link">
        <a href="/watershed/boundaries-table">
          View watershed boundaries as a data table
        </a>
      </p>

      <div className="map-controls">
        <a href="javascript:void(0)" className="map-control" onClick={handleZoomIn}>
          Zoom in
        </a>
        <a href="javascript:void(0)" className="map-control" onClick={handleZoomOut}>
          Zoom out
        </a>
        <a href="javascript:void(0)" className="map-control" onClick={handleReset}>
          Reset view
        </a>
      </div>

      <p className="map-report-link">
        <a href="/reports/watershed-2026" target="_blank" rel="noopener noreferrer">
          Open full report
          <span className="visually-hidden"> (opens in a new tab)</span>
        </a>
      </p>
    </section>
  );
};

export default WatershedMapPanel;
```

## CSS

```css
.map-panel {
  max-width: 640px;
  margin: 24px auto;
  border: 1px solid #d0d5dd;
  border-radius: 8px;
  padding: 16px;
}

.map-panel h2 {
  margin: 0 0 12px 0;
  font-size: 1.125rem;
}

.map-canvas {
  height: 280px;
  background: #eaecf0;
  border-radius: 6px;
  margin-bottom: 16px;
}

.map-controls {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.map-control {
  padding: 6px 14px;
  border: 1px solid #0b5fff;
  border-radius: 4px;
  background: #fff;
  color: #0b5fff;
  text-decoration: none;
  cursor: pointer;
}

.map-control:focus-visible {
  outline: 3px solid #0b5fff;
  outline-offset: 2px;
}

.map-alt-link {
  margin: 0 0 12px 0;
}

.map-alt-link a {
  color: #0b5fff;
}

.map-alt-link a:focus-visible {
  outline: 3px solid #0b5fff;
  outline-offset: 2px;
}

.map-report-link {
  margin: 0;
}

.map-report-link a {
  color: #0b5fff;
}

.map-report-link a:focus-visible {
  outline: 3px solid #0b5fff;
  outline-offset: 2px;
}

.visually-hidden {
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
```

## Expected Behavior

- On load, the panel shows the watershed boundary map, followed by three actions below it: **Zoom in**, **Zoom out**, **Reset view**. Visual order matches DOM order; no CSS reorders them.
- Pressing any of the three actions updates the map's zoom/pan state in place; none of them navigates the browser anywhere or changes the URL.
- **Open full report** opens the underlying watershed report PDF in a new tab, leaving the map panel open in the original tab.

## Accessibility Issues (Planted)

1. **CRITICAL: Zoom in / Zoom out / Reset view are anchors used as buttons (F42)** — All three map actions are `<a href="javascript:void(0)" onClick={...}>` elements sharing the identical pseudo-href `javascript:void(0)`. An anchor's default role is `link`, which tells assistive technology "activating this navigates to a destination." None of these three does — they mutate in-page map state and go nowhere. A screen reader user who pulls up the page's links list (a common navigation strategy) hears "Zoom in, link", "Zoom out, link", "Reset view, link" alongside the one real destination on the page, with no way to tell from the role alone that three of the four are not links at all. The role communicates a promise — navigation — that activating the control does not keep.
   - Evidence: `pseudo-link-map-controls.md:26-36` (three `<a>` elements, each `href="javascript:void(0)"`, in `.map-controls`)
   - WCAG citation: 4.1.2 Name, Role, Value (F42: anchor used as a control announces role "link", communicating navigation that does not occur)
   - User group: Screen reader users
   - Expected: An element that performs an in-page action and never navigates should expose role `button`, not `link`.
   - Fix: Replace all three with `<button type="button">`, keeping the existing `onClick` handlers and visible text, and drop the `href` entirely.

2. **MAJOR: The same three anchors respond to Enter but not Space** — Because `Zoom in` / `Zoom out` / `Reset view` are anchors rather than buttons, they inherit the anchor keyboard-activation model: Enter fires the click, Space does not (Space only activates elements with the button role). A user who has learned "this is a button, Space activates it" — because it is styled like one, sits in a control bar with other actions, and performs a momentary action rather than navigating — presses Space and nothing happens. The control is reachable and even operable via Enter, so this is not a keyboard-trap or missing-handler failure; it is the role misrepresenting which interaction model applies.
   - Evidence: `pseudo-link-map-controls.md:26-36` (same three anchors; no `role="button"`, so Space is never wired to `handleZoomIn`/`handleZoomOut`/`handleReset`)
   - WCAG citation: 4.1.2 Name, Role, Value (the control's role communicates the wrong interaction model, not a 2.1.1 Keyboard failure — Enter does operate all three)
   - User group: Keyboard users applying the button interaction model
   - Expected: A control that performs an action rather than navigating should activate on both Enter and Space, matching the interaction model its appearance and behavior imply.
   - Fix: The same fix as the role defect above — converting the three anchors to real `<button type="button">` elements restores native Space activation at no extra cost.

## Difficulty Level

**HAS-BUGS** — The defect is visually invisible: the three controls look and behave like buttons on click, and a reviewer testing only with a mouse or only pressing Enter will never notice anything wrong. Finding it requires reading the markup for the element type rather than the rendered behavior, or testing keyboard activation with Space specifically. The fixture also carries a genuine anchor (`Open full report`) with a real destination, so a reviewer must distinguish "anchor used correctly" from "anchor used as a button" within the same component rather than pattern-matching on "this component uses anchors, therefore anchors are the problem" or "therefore anchors are fine."
