# Product Carousel With Autoplay Animation

## Description

React product carousel that auto-advances every 3 seconds with sliding CSS transitions, a parallax background, and a pulsing badge animation — none guarded by prefers-reduced-motion. No pause/stop control exists. Keyboard navigation (prev/next buttons) works correctly. Tests whether reviewers surface vestibular and cognitive concerns, not just ARIA/keyboard gaps.

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

---

_This directory contains component files extracted from the a11y eval suite for chain evaluation._
_Run `/a11y-workflow full evals/suites/chain/targets/product-carousel-autoplay/component.jsx` to start the chain._
