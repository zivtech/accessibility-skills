# Fixture: Image Carousel Without Region and Live Region

## Component Code

```jsx
import React, { useState } from 'react';

const BuggyCarousel = ({ images = [] }) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  const goToPrevious = () => {
    setCurrentIndex((currentIndex - 1 + images.length) % images.length);
  };

  const goToNext = () => {
    setCurrentIndex((currentIndex + 1) % images.length);
  };

  return (
    <div className="carousel">
      {/* BUG: No role="region" to identify as carousel region */}
      {/* BUG: No aria-label to describe carousel purpose */}
      {/* BUG: No aria-live region to announce image changes */}
      <div className="carousel-images">
        <img
          src={images[currentIndex]}
          alt={`Carousel image ${currentIndex + 1}`}
          // BUG: alt text doesn't describe image content
        />
      </div>

      <button onClick={goToPrevious} aria-label="Previous image">
        Previous
      </button>

      <button onClick={goToNext} aria-label="Next image">
        Next
      </button>

      {/* BUG: No live region to announce current position */}
      <div className="carousel-indicators">
        {images.map((_, idx) => (
          <button
            key={idx}
            onClick={() => setCurrentIndex(idx)}
            className={idx === currentIndex ? 'active' : ''}
            // BUG: aria-label doesn't indicate if this is current
            aria-label={`Go to image ${idx + 1}`}
          >
            {idx + 1}
          </button>
        ))}
      </div>
    </div>
  );
};

export default BuggyCarousel;
```

## Expected Behavior

- Carousel displays images with navigation buttons
- Screen reader announces current image and position
- aria-live region announces when image changes
- Indicator buttons show which image is current
- Region labeled for context

## Accessibility Features Present

✓ aria-label on Previous/Next buttons
✓ alt text on images
✓ aria-label on indicator buttons

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Missing role="region" on carousel container** — Carousel is just a div without semantic meaning. Screen reader user does not identify it as a carousel region. Per carousel pattern, container should have role="region" to mark it as important section.
   - Evidence: `image-carousel-no-region.md:16-17` (div has no role)
   - User group: Screen reader users (critical)
   - Expected: Carousel should have role="region"
   - Fix: Add role="region" to carousel div

2. **MAJOR: Missing aria-label on carousel region** — Region lacks descriptive label. Screen reader user navigating regions hears "region" without knowing it's a carousel. aria-label="Carousel" would clarify.
   - Evidence: `image-carousel-no-region.md:16-17` (no aria-label)
   - User group: Screen reader users
   - Expected: Region should have aria-label
   - Fix: Add aria-label="Carousel" or aria-label="Image carousel"

3. **CRITICAL: Missing aria-live region for status updates** — When user clicks Next, image changes but screen reader doesn't announce it. No aria-live region to communicate image position change. Per carousel pattern, aria-live="polite" should announce current image.
   - Evidence: `image-carousel-no-region.md:35-45` (no aria-live element)
   - User group: Screen reader users (critical for awareness)
   - Expected: Live region should announce current image and total count
   - Fix: Add aria-live="polite" region with current position text

4. **MAJOR: Missing aria-current on current indicator** — Current indicator button should announce using aria-current="true". Without it, screen reader user cannot quickly identify which indicator is active beyond visual highlighting.
   - Evidence: `image-carousel-no-region.md:40-46` (no aria-current)
   - User group: Screen reader users
   - Expected: Active indicator should have aria-current="true"
   - Fix: Add aria-current={idx === currentIndex ? "true" : undefined}

## Difficulty Level

**HAS-BUGS** — Missing region semantics and live region announcements. Carousel works visually but lacks screen reader support for state changes.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Difficulty Rating

A11y-critic should identify that carousels are complex interactive patterns requiring role="region", aria-live for announcements, and proper state management.
