# Fixture: Image Gallery With Undersized Touch Targets

## Component Code

```jsx
import React, { useState, useEffect, useRef } from 'react';

const images = [
  { id: 1, src: '/img/sunset.jpg', alt: 'Sunset over Pacific coastline' },
  { id: 2, src: '/img/forest.jpg', alt: 'Redwood forest trail in morning fog' },
  { id: 3, src: '/img/city.jpg', alt: 'Downtown skyline at dusk' },
  { id: 4, src: '/img/mountain.jpg', alt: 'Snow-capped peak above treeline' },
  { id: 5, src: '/img/ocean.jpg', alt: 'Waves breaking on rocky shore' },
  { id: 6, src: '/img/desert.jpg', alt: 'Sand dunes under clear sky' },
  { id: 7, src: '/img/lake.jpg', alt: 'Still lake reflecting autumn colors' },
  { id: 8, src: '/img/garden.jpg', alt: 'Japanese garden with stone bridge' },
  { id: 9, src: '/img/canyon.jpg', alt: 'Red rock canyon from overlook' },
];

const ImageGallery = () => {
  const [lightbox, setLightbox] = useState(null);
  const [zoom, setZoom] = useState(1);
  const closeBtnRef = useRef(null);
  const lastFocused = useRef(null);

  const openLightbox = (img) => {
    lastFocused.current = document.activeElement;
    setLightbox(img);
    setZoom(1);
  };

  const closeLightbox = () => {
    setLightbox(null);
    lastFocused.current?.focus();
  };

  // Focus trap and Escape handling — correctly implemented
  useEffect(() => {
    if (!lightbox) return;
    closeBtnRef.current?.focus();
    const handleKey = (e) => {
      if (e.key === 'Escape') closeLightbox();
    };
    document.addEventListener('keydown', handleKey);
    return () => document.removeEventListener('keydown', handleKey);
  }, [lightbox]);

  const currentIdx = lightbox ? images.findIndex(i => i.id === lightbox.id) : -1;
  const goPrev = () => currentIdx > 0 && setLightbox(images[currentIdx - 1]);
  const goNext = () => currentIdx < images.length - 1 && setLightbox(images[currentIdx + 1]);

  return (
    <section className="gallery" aria-label="Photo gallery">
      <h2>Nature Photography</h2>

      {/* BUG: Thumbnails are 32x32px with 2px gap — WCAG 2.5.8 minimum is 24x24 but
          with only 2px spacing, adjacent targets overlap effective hit area */}
      <div className="thumb-grid">
        {images.map(img => (
          <button
            key={img.id}
            className="thumb-btn"
            onClick={() => openLightbox(img)}
            aria-label={`View ${img.alt}`}
          >
            <img src={img.src} alt="" className="thumb-img" />
          </button>
        ))}
      </div>

      {lightbox && (
        <div className="lightbox-overlay" role="dialog" aria-modal="true" aria-label={lightbox.alt}>
          <div className="lightbox-content">
            <img src={lightbox.src} alt={lightbox.alt} style={{ transform: `scale(${zoom})` }} />

            {/* BUG: Close button is 16x16px — WCAG 2.5.8 */}
            <button
              ref={closeBtnRef}
              className="lightbox-close"
              onClick={closeLightbox}
              aria-label="Close lightbox"
            >
              ×
            </button>

            <button className="lightbox-prev" onClick={goPrev} aria-label="Previous image" disabled={currentIdx === 0}>‹</button>
            <button className="lightbox-next" onClick={goNext} aria-label="Next image" disabled={currentIdx === images.length - 1}>›</button>

            {/* BUG: Zoom buttons are 20x20px — WCAG 2.5.8 */}
            <div className="zoom-controls">
              <button className="zoom-btn" onClick={() => setZoom(z => Math.min(z + 0.25, 3))} aria-label="Zoom in">+</button>
              <button className="zoom-btn" onClick={() => setZoom(z => Math.max(z - 0.25, 0.5))} aria-label="Zoom out">−</button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
};

export default ImageGallery;
```

```css
.gallery { padding: 24px; font-family: system-ui, sans-serif; }
.gallery h2 { font-size: 1.5rem; margin-bottom: 16px; }

/* BUG: 32x32px thumbnails with 2px gap — too small, too close */
.thumb-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, 32px);
  gap: 2px;
}

.thumb-btn {
  width: 32px; height: 32px;
  padding: 0; border: none; cursor: pointer;
  background: none;
}

.thumb-btn:focus-visible { outline: 3px solid #005fcc; outline-offset: 2px; }
.thumb-img { width: 100%; height: 100%; object-fit: cover; display: block; }

/* BUG: At 200% zoom, grid overflows horizontally — WCAG 1.4.10 */
/* No flex-wrap or responsive breakpoint */

.lightbox-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.9); display: flex; align-items: center; justify-content: center;
  z-index: 1000;
}

.lightbox-content { position: relative; max-width: 90vw; max-height: 90vh; }
.lightbox-content img { max-width: 100%; max-height: 80vh; transition: transform 0.2s; }

/* BUG: Close button 16x16px — far below 24x24 minimum */
.lightbox-close {
  position: absolute; top: 4px; right: 4px;
  width: 16px; height: 16px;
  background: rgba(255,255,255,0.8); border: none;
  font-size: 14px; line-height: 16px; cursor: pointer;
  border-radius: 2px; padding: 0;
}

.lightbox-close:focus-visible { outline: 2px solid #fff; outline-offset: 2px; }

.lightbox-prev, .lightbox-next {
  position: absolute; top: 50%; transform: translateY(-50%);
  background: rgba(255,255,255,0.8); border: none;
  padding: 12px 16px; font-size: 1.5rem; cursor: pointer; border-radius: 4px;
}

.lightbox-prev { left: -48px; }
.lightbox-next { right: -48px; }
.lightbox-prev:focus-visible, .lightbox-next:focus-visible { outline: 2px solid #fff; }

/* BUG: Zoom buttons 20x20px — below minimum */
.zoom-controls {
  position: absolute; bottom: 8px; right: 8px;
  display: flex; gap: 4px;
}

.zoom-btn {
  width: 20px; height: 20px; padding: 0;
  background: rgba(255,255,255,0.8); border: none;
  font-size: 14px; cursor: pointer; border-radius: 2px;
}

.zoom-btn:focus-visible { outline: 2px solid #fff; }

/* BUG: lightbox-prev/next positioned at viewport edge — clipped at zoom */
```

## Expected Behavior

- Grid of thumbnail images opens lightbox on click
- Lightbox shows full image with prev/next navigation
- Zoom in/out controls adjust image scale
- Close button or Escape key dismisses lightbox

## Accessibility Features Present

- All buttons are real `<button>` elements
- Images have descriptive alt text
- Lightbox has `role="dialog"` and `aria-modal="true"`
- Focus moves to close button on open; returns to trigger on close
- Escape key closes lightbox
- Focus-visible outlines on all interactive elements
- Prev/next buttons properly labeled and disabled at boundaries

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Thumbnails 32x32px with 2px gap — WCAG 2.5.8 (Target Size, Minimum)**
   Each thumbnail button is 32x32px with only 2px gap between adjacent targets. While 32px exceeds the 24px minimum, the 2px spacing means effective hit areas overlap for users with motor impairments.
   - Evidence: CSS `.thumb-grid { gap: 2px }` and `.thumb-btn { width: 32px; height: 32px }`
   - User group: Motor impairment users, tremor users, touch users
   - Fix: Increase to 44x44px with 8px gap

2. **MAJOR: Lightbox close button 16x16px — WCAG 2.5.8**
   Close button renders at 16x16px with no padding — well below the 24x24px minimum.
   - Evidence: CSS `.lightbox-close { width: 16px; height: 16px; padding: 0 }`
   - User group: Motor impairment users
   - Fix: Increase to 44x44px minimum with adequate padding

3. **MAJOR: Zoom in/out buttons 20x20px — WCAG 2.5.8**
   Zoom controls render at 20x20px with no padding.
   - Evidence: CSS `.zoom-btn { width: 20px; height: 20px; padding: 0 }`
   - User group: Motor users, touch users
   - Fix: Increase to 44x44px with adequate padding

4. **MINOR: At 200% zoom, thumbnail grid overflows horizontally — WCAG 1.4.10 (Reflow)**
   Grid uses fixed 32px columns with no responsive breakpoint. At 200% browser zoom, content overflows creating a horizontal scrollbar.
   - Evidence: CSS `.thumb-grid` uses fixed grid-template-columns with no media query
   - User group: Magnification users
   - Fix: Use flexible grid or reduce columns at narrow widths

5. **MINOR: Lightbox nav arrows positioned at viewport edge, clipped at zoom**
   Prev/next buttons use absolute positioning that goes off-screen at zoom levels.
   - Evidence: CSS `.lightbox-prev { left: -48px }` — negative offset clips at zoom
   - User group: Magnification users
   - Fix: Position inside lightbox content bounds

## Difficulty Level

**HAS-BUGS** — New dimension: Magnification & Reflow. The lightbox correctly traps focus, has ARIA roles, and Escape works — keyboard/SR dimensions are intentionally correct. The bugs are all in target size and reflow, requiring a magnification perspective to surface.

## Frameworks

React 18+, CSS Grid
