# Fixture: Watershed Map Panel with Zoom Controls

## Component Code

```jsx
import { ZoomInIcon, ZoomOutIcon, ResetViewIcon } from '../icons';

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
        <button type="button" className="map-control" onClick={handleZoomIn}>
          <ZoomInIcon aria-hidden="true" />
          Zoom in
        </button>
        <button type="button" className="map-control" onClick={handleZoomOut}>
          <ZoomOutIcon aria-hidden="true" />
          Zoom out
        </button>
        <button type="button" className="map-control" onClick={handleReset}>
          <ResetViewIcon aria-hidden="true" />
          Reset view
        </button>
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
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border: 1px solid #0b5fff;
  border-radius: 4px;
  background: #fff;
  color: #0b5fff;
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
- Pressing any of the three actions — by mouse click, Enter, or Space — updates the map's zoom/pan state in place; none of them navigates the browser anywhere or changes the URL.
- **Open full report** opens the underlying watershed report PDF in a new tab, leaving the map panel open in the original tab.

## Accessibility Features Present

1. **Real buttons for in-page actions** — `Zoom in`, `Zoom out`, and `Reset view` are `<button type="button">` elements. Their role is correctly `button`, so assistive technology never implies a navigation destination that doesn't exist, and they activate on both Enter and Space.
2. **Icons are decorative, text carries the name** — `ZoomInIcon` / `ZoomOutIcon` / `ResetViewIcon` are `aria-hidden="true"`; each button's accessible name comes from its own visible text ("Zoom in", "Zoom out", "Reset view"), so there is no risk of an `aria-label` silently diverging from what's on screen.
3. **No `aria-pressed` on the three buttons** — Zoom in, Zoom out, and Reset view are momentary actions, not toggles: they don't have an on/off state to reflect, so they are correctly plain buttons rather than toggle buttons.
4. **The map has a text alternative** — the boundary data the canvas renders visually is reachable by everyone through the "View watershed boundaries as a data table" link, a peer route to the same information rather than a fallback for people who cannot use the map.
5. **Genuine anchor implemented correctly** — `Open full report` is a real `<a href="/reports/watershed-2026">` with a real destination, `target="_blank"`, `rel="noopener noreferrer"`, and a visually-hidden "(opens in a new tab)" disclosure so the new-tab behavior is announced rather than silently sprung on the user.
6. **Visible focus indicators** — every interactive element (`.map-control`, the data-table link, and the report anchor) has a `:focus-visible` outline.

## Accessibility Issues

_Answer key: none planted (CLEAN baseline)._

None. This fixture is a CLEAN baseline with no planted defects. Everything from
this heading down is ground-truth material and is stripped from model prompts by
the blind protocol (`ANSWER_KEY_RE` in the runners).

## Difficulty Level

**CLEAN** — Baseline for false-positive avoidance on the "control vs. link" distinction. Three constructs here read like defects to a reviewer applying a rule mechanically rather than reasoning about what each control actually does: the absence of `aria-pressed` on three prominent buttons, and the presence of three same-group buttons with distinct labels that a reviewer primed by a companion BUG fixture might still reflexively check against SC 3.2.4.
