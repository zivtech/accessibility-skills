# Fixture: Interactive Map With Mouse-Only Navigation

## Component Code

```jsx
import React, { useState, useRef, useCallback } from 'react';

const markers = [
  { id: 1, label: 'HQ Office', lat: 39.95, lng: -75.17, info: 'Main headquarters. 200 employees. Open M-F 8am-6pm.' },
  { id: 2, label: 'Warehouse', lat: 40.01, lng: -75.13, info: 'Distribution center. 50,000 sq ft. 24/7 operations.' },
  { id: 3, label: 'Retail Store', lat: 39.94, lng: -75.16, info: 'Flagship retail location. Open daily 10am-9pm.' },
];

const MapInterface = () => {
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [zoomLevel, setZoomLevel] = useState(1);
  const [activePopup, setActivePopup] = useState(null);
  const [dragging, setDragging] = useState(false);
  const dragStart = useRef(null);
  const mapRef = useRef(null);

  // BUG: Panning relies entirely on mouse drag — no keyboard alternative — WCAG 2.1.1
  const handleMouseDown = (e) => {
    setDragging(true);
    dragStart.current = { x: e.clientX - offset.x, y: e.clientY - offset.y };
  };

  const handleMouseMove = useCallback((e) => {
    if (!dragging) return;
    setOffset({
      x: e.clientX - dragStart.current.x,
      y: e.clientY - dragStart.current.y,
    });
  }, [dragging]);

  const handleMouseUp = () => setDragging(false);

  // BUG: Scroll wheel zoom hijacks page scroll — no escape mechanism
  const handleWheel = (e) => {
    e.preventDefault();
    setZoomLevel(z => Math.max(0.5, Math.min(3, z + (e.deltaY > 0 ? -0.1 : 0.1))));
  };

  return (
    <section className="map-page">
      <h1>Our Locations</h1>

      <div className="map-toolbar">
        <label htmlFor="location-search">Search location</label>
        <input id="location-search" type="text" placeholder="Enter address..." className="search-input" />
      </div>

      <div
        ref={mapRef}
        className="map-container"
        role="application"
        aria-label="Interactive map showing office locations"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onWheel={handleWheel}
      >
        <div
          className="map-canvas"
          style={{
            transform: `translate(${offset.x}px, ${offset.y}px) scale(${zoomLevel})`,
          }}
        >
          <div className="map-tile" />

          {markers.map(m => (
            <div
              key={m.id}
              className="map-marker"
              style={{ left: `${(m.lng + 75.2) * 500}px`, top: `${(40.1 - m.lat) * 500}px` }}
              // BUG: Info popup on hover only — no focus/click alternative — WCAG 1.4.13
              onMouseEnter={() => setActivePopup(m.id)}
              onMouseLeave={() => setActivePopup(null)}
            >
              <div className="marker-pin" aria-label={m.label}>📍</div>

              {activePopup === m.id && (
                <div className="marker-popup">
                  <strong>{m.label}</strong>
                  <p>{m.info}</p>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* BUG: Zoom buttons 18x18px — WCAG 2.5.8 */}
        {/* BUG: At 200% browser zoom, these overlap the map edge — WCAG 1.4.10 */}
        <div className="map-controls">
          <button className="zoom-control" onClick={() => setZoomLevel(z => Math.min(3, z + 0.25))} aria-label="Zoom in">+</button>
          <button className="zoom-control" onClick={() => setZoomLevel(z => Math.max(0.5, z - 0.25))} aria-label="Zoom out">−</button>
        </div>
      </div>
    </section>
  );
};

export default MapInterface;
```

```css
.map-page { font-family: system-ui, sans-serif; padding: 24px; }
.map-page h1 { font-size: 1.5rem; margin-bottom: 16px; }

.map-toolbar { margin-bottom: 12px; }
.map-toolbar label { display: block; font-weight: 600; margin-bottom: 4px; }
.search-input {
  padding: 8px 12px; width: 280px; border: 2px solid #ccc; border-radius: 4px; font-size: 1rem;
}
.search-input:focus { outline: 3px solid #005fcc; outline-offset: 2px; }

.map-container {
  position: relative; width: 100%; height: 400px;
  overflow: hidden; border: 1px solid #ccc; border-radius: 4px;
  cursor: grab; background: #e8eaed;
}

.map-container:active { cursor: grabbing; }

.map-canvas {
  position: absolute; width: 600px; height: 400px;
  transition: none; /* immediate pan response */
}

.map-tile {
  width: 100%; height: 100%;
  background: linear-gradient(135deg, #d4e6f1, #a9cce3);
}

.map-marker { position: absolute; cursor: pointer; }
.marker-pin { font-size: 24px; }

.marker-popup {
  position: absolute; bottom: 100%; left: 50%; transform: translateX(-50%);
  background: #fff; border: 1px solid #ccc; border-radius: 4px;
  padding: 8px 12px; width: 200px; box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  z-index: 10;
}

.marker-popup strong { display: block; margin-bottom: 4px; }
.marker-popup p { font-size: 13px; color: #333; margin: 0; }

/* BUG: Zoom controls 18x18px — below 24x24 minimum */
/* BUG: position: absolute with fixed offsets — overlaps at 200% zoom */
.map-controls {
  position: absolute; top: 8px; right: 8px;
  display: flex; flex-direction: column; gap: 2px;
}

.zoom-control {
  width: 18px; height: 18px; padding: 0;
  background: #fff; border: 1px solid #999;
  font-size: 14px; font-weight: 700; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  border-radius: 2px;
}

.zoom-control:focus-visible { outline: 2px solid #005fcc; outline-offset: 2px; }
```

## Expected Behavior

- Interactive map displays 3 location markers
- Mouse drag pans the map view
- Scroll wheel zooms in/out
- Hovering a marker shows an info popup
- +/- buttons zoom the map
- Search input allows location queries

## Accessibility Features Present

- Map container has `role="application"` and descriptive `aria-label`
- Zoom buttons are real `<button>` elements with `aria-label`
- Search input has associated `<label>`
- Focus-visible outlines on zoom buttons and search input
- Heading structure (h1) present

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Map panning relies on mouse drag only — WCAG 2.1.1 (Keyboard)**
   No arrow key handlers for panning. Keyboard users cannot navigate the map.
   - Evidence: Lines 21-30 — onMouseDown/Move/Up with no onKeyDown for arrows
   - User group: Keyboard users, switch access users
   - Fix: Add onKeyDown handler for Arrow keys to adjust offset

2. **MAJOR: Zoom +/- buttons 18x18px — WCAG 2.5.8 (Target Size)**
   Below the 24x24px minimum target size.
   - Evidence: CSS `.zoom-control { width: 18px; height: 18px }`
   - User group: Motor impairment users, touch users
   - Fix: Increase to 44x44px with padding

3. **MAJOR: At 200% zoom, controls overlap and become unusable — WCAG 1.4.10 (Reflow)**
   Map controls use absolute positioning with fixed px values. At 200% zoom they overlap content.
   - Evidence: CSS `.map-controls { position: absolute; top: 8px; right: 8px }`
   - User group: Magnification users
   - Fix: Use responsive positioning or place controls outside map container

4. **MAJOR: Info popup on marker hover only — WCAG 1.4.13 / 2.1.1**
   Marker popups appear on `onMouseEnter` with no focus or click equivalent.
   - Evidence: Lines 67-68 — onMouseEnter/Leave with no focus/click handler; marker div has no tabIndex
   - User group: Keyboard users, touch users
   - Fix: Add tabIndex={0}, onFocus, and onClick handlers to markers

5. **MINOR: Scroll wheel zoom hijacks page scroll**
   `e.preventDefault()` on wheel event prevents scrolling past the map.
   - Evidence: Line 37 — `e.preventDefault()` in handleWheel
   - User group: All users trying to scroll past the map
   - Fix: Only zoom when Ctrl+wheel or when map is focused

## Difficulty Level

**HAS-BUGS** — New dimensions: Magnification & Reflow + Keyboard. The map has correct role="application", proper zoom button labels, and a labeled search input. The failures are in mouse-only interaction and small targets — requiring magnification and motor perspectives.

## Frameworks

React 18+, CSS
