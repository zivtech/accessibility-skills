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
