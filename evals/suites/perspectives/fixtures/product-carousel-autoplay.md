# Fixture: Product Carousel With Autoplay Animation

## Component Code

```jsx
import React, { useState, useEffect } from 'react';

const products = [
  { id: 1, name: 'Wireless Headphones', price: '$149', badge: 'NEW', image: '/img/headphones.jpg' },
  { id: 2, name: 'Mechanical Keyboard', price: '$89', badge: 'SALE', image: '/img/keyboard.jpg' },
  { id: 3, name: 'USB-C Hub', price: '$49', badge: 'HOT', image: '/img/hub.jpg' },
  { id: 4, name: 'Webcam Pro', price: '$129', badge: 'NEW', image: '/img/webcam.jpg' },
];

const ProductCarousel = () => {
  const [currentIndex, setCurrentIndex] = useState(0);

  // BUG: Auto-advances every 3 seconds with no pause/stop control — WCAG 2.2.2
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % products.length);
    }, 3000);
    return () => clearInterval(timer);
  }, []);

  const goToPrev = () => {
    setCurrentIndex((prev) => (prev - 1 + products.length) % products.length);
  };

  const goToNext = () => {
    setCurrentIndex((prev) => (prev + 1) % products.length);
  };

  const product = products[currentIndex];

  return (
    // BUG: Parallax background with no reduced-motion alternative — WCAG 2.3.1
    <div className="carousel-wrapper" data-parallax="true">
      <div
        className="carousel-track"
        style={{
          // BUG: CSS transform transition ignores prefers-reduced-motion — WCAG 2.3.1
          transform: `translateX(-${currentIndex * 100}%)`,
          transition: 'transform 0.6s ease',
        }}
      >
        {products.map((p) => (
          <div key={p.id} className="carousel-slide">
            <img src={p.image} alt={p.name} />
            {/* BUG: Rapid fade-in/fade-out animation — distracting for cognitive/attention users */}
            <span className="product-badge">{p.badge}</span>
            <h2>{p.name}</h2>
            <p className="price">{p.price}</p>
          </div>
        ))}
      </div>

      {/* Keyboard navigation works correctly — prev/next buttons are focusable and labeled */}
      <button
        className="carousel-btn carousel-prev"
        onClick={goToPrev}
        aria-label="Previous product"
      >
        ‹
      </button>
      <button
        className="carousel-btn carousel-next"
        onClick={goToNext}
        aria-label="Next product"
      >
        ›
      </button>

      {/* BUG: No aria-live region — screen reader users don't hear slide changes */}
      <div className="carousel-dots">
        {products.map((_, i) => (
          <span
            key={i}
            className={`dot ${i === currentIndex ? 'active' : ''}`}
            aria-hidden="true"
          />
        ))}
      </div>
    </div>
  );
};

export default ProductCarousel;
```

```css
/* BUG: No @media (prefers-reduced-motion: reduce) override anywhere in this stylesheet */

.carousel-wrapper {
  position: relative;
  overflow: hidden;
  /* BUG: Parallax background shift — scrolling triggers continuous motion */
  background-attachment: fixed;
  background-image: url('/img/pattern.svg');
}

.carousel-track {
  display: flex;
  /* transition defined inline via React style prop — also no reduced-motion check */
}

.carousel-slide {
  min-width: 100%;
  flex-shrink: 0;
  position: relative;
}

/* BUG: Rapid alternating opacity animation on badges — no reduced-motion guard */
.product-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: #e63946;
  color: #fff;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: bold;
  animation: badgePulse 0.8s ease-in-out infinite alternate;
}

@keyframes badgePulse {
  from { opacity: 1; }
  to   { opacity: 0.3; }
}

.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0,0,0,0.5);
  color: #fff;
  border: none;
  padding: 12px 16px;
  cursor: pointer;
  font-size: 1.5rem;
  border-radius: 4px;
}

.carousel-btn:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}

.carousel-prev { left: 8px; }
.carousel-next { right: 8px; }

.carousel-dots {
  text-align: center;
  padding: 8px 0;
}

.dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #ccc;
  margin: 0 4px;
}

.dot.active {
  background: #333;
}
```

## Expected Behavior

- Carousel shows one product at a time
- Auto-advances every 3 seconds indefinitely
- User can navigate manually with prev/next buttons
- Active dot indicator updates with current slide
- Product badge pulses continuously

## Accessibility Features Present

✓ Prev/next buttons have descriptive `aria-label` attributes
✓ Prev/next buttons are keyboard focusable with visible focus styles (`:focus-visible` outline)
✓ Product images have non-empty `alt` text
✓ Color contrast on text and buttons meets WCAG AA
✓ Semantic heading (`h2`) on product name
✓ Decorative dot indicators are `aria-hidden`

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: No pause/stop control for auto-advancing content — WCAG 2.2.2 (Pause, Stop, Hide)**
   Auto-advance fires every 3 seconds with no mechanism to pause, stop, or hide the motion. WCAG 2.2.2 requires that moving content lasting more than 5 seconds can be paused. Users with vestibular disorders, cognitive disabilities, and attention difficulties are directly harmed by content they cannot stop.
   - Evidence: `product-carousel-autoplay.md:16-20` (`setInterval` with no pause mechanism)
   - User group: Vestibular disorder users, cognitive/attention users, photosensitive users
   - Fix: Add a pause/play button that clears/restarts the interval

2. **MAJOR: CSS transition animation ignores `prefers-reduced-motion` — WCAG 2.3.1 (Three Flashes or Below Threshold)**
   The slide transition (`transform 0.6s ease`) is applied unconditionally via inline style. No `@media (prefers-reduced-motion: reduce)` block exists anywhere in the stylesheet to disable or reduce this motion. Users who have enabled reduced-motion at the OS level receive no accommodation. Large viewport-width slide translations are among the most likely CSS animations to trigger vestibular symptoms.
   - Evidence: `product-carousel-autoplay.md:34-37` (inline transition with no media query guard)
   - User group: Vestibular disorder users (motion sickness, BPPV, migraine)
   - Fix: Wrap the transition in a `useReducedMotion` check; use instant swap or crossfade instead

3. **MAJOR: Parallax background effect with no reduced-motion alternative — WCAG 2.3.1**
   `background-attachment: fixed` on `.carousel-wrapper` creates a parallax scrolling effect as the page scrolls. Parallax motion is strongly associated with vestibular symptoms (nausea, dizziness) and is explicitly called out in WCAG 2.3.3 guidance. No reduced-motion alternative is provided.
   - Evidence: `product-carousel-autoplay.md:CSS:91-93` (`background-attachment: fixed`)
   - User group: Vestibular disorder users
   - Fix: `@media (prefers-reduced-motion: reduce) { .carousel-wrapper { background-attachment: scroll; } }`

4. **MINOR: Rapid badge pulse animation is distracting — cognitive/attention impact**
   `.product-badge` runs a 0.8s infinite alternating opacity animation (`badgePulse`). Constant peripheral animation in a 0.3–1.0 opacity range draws involuntary attention and can be highly disruptive for users with ADHD, autism spectrum conditions, or anxiety. No reduced-motion guard on this keyframe.
   - Evidence: `product-carousel-autoplay.md:CSS:108-115` (`@keyframes badgePulse`, no media query)
   - User group: Cognitive/attention users (ADHD, ASD), vestibular users
   - Fix: `@media (prefers-reduced-motion: reduce) { .product-badge { animation: none; } }`

5. **MINOR: No `aria-live` region announcing slide changes — screen reader experience**
   When the carousel auto-advances or the user navigates manually, the slide change produces no announcement. Screen reader users who are focused elsewhere on the page have no way to know the content has changed. An `aria-live="polite"` region with the current product name would provide non-intrusive announcements.
   - Evidence: `product-carousel-autoplay.md:57-67` (dot indicators are `aria-hidden`, no live region present)
   - User group: Screen reader users
   - Fix: Add `<div aria-live="polite" aria-atomic="true" className="sr-only">{product.name}</div>`

## Difficulty Level

**HAS-BUGS** — Keyboard navigation works correctly. The component's failure mode is entirely in the vestibular/motion and cognitive dimensions. A reviewer focused only on keyboard/ARIA patterns will miss 4 of the 5 issues.

## Frameworks

React 18+, CSS (no CSS-in-JS)
