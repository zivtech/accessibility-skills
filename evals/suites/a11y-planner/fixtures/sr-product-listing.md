# Fixture: E-Commerce Product Grid with Sort, Filter, and Add-to-Cart

## Feature Description

You're planning accessibility for an e-commerce product listing page on an outdoor gear retailer's site. The page displays a grid of product cards (24 per page), each containing a product image, product name as a link, star rating, price with optional sale price (strikethrough original + red "Sale" badge), availability status ("In Stock" / "Low Stock" / "Out of Stock"), and an "Add to Cart" button. Above the grid: a sort dropdown ("Best Match", "Price: Low to High", "Price: High to Low", "Customer Rating"), a filter panel (collapsible on mobile) with Category, Brand, Price Range (slider), and Color checkboxes. When "Add to Cart" is clicked, the button label changes to "Added ✓" for 3 seconds, the cart badge count in the header increments, and a toast notification appears bottom-right ("Seaborn Down Jacket added to cart. View Cart"). There are 847 products total; pagination uses prev/next buttons plus a page selector. The price range filter uses a two-handle range slider.

## Context

- **Platform:** React/Next.js e-commerce front-end
- **Existing code:** Yes — product cards rendered as `<div>` elements with click handlers; star ratings are Unicode stars (★★★☆☆) with no SR equivalent; sale prices marked up with visual strikethrough only; "Add to Cart" button has no post-action announcement; cart badge count updates silently; price range slider is a custom component with no ARIA
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA (Windows), JAWS (Windows), VoiceOver (macOS), keyboard-only users
- **Scope:** Product grid semantics, sort state, filter state, price range slider, cart action confirmation, cart count update
- **Constraints:** Product cards must work as list items, not table rows; star ratings are font icons that must be replaced with accessible equivalents; price range slider is a third-party component with limited ARIA support; cart toast appears outside the main landmark

## Requirement

Create a comprehensive accessibility design plan that a developer with no accessibility knowledge can use to implement the component correctly on the first attempt.

The plan should cover:
- Semantic structure: product list as `<ul>/<li>` not a grid table; card heading hierarchy
- Sort control: `<select>` with visible `<label>`, current sort communicated via selected `<option>`
- Filter panel: landmark region, collapsible state, checkbox group with `<fieldset>/<legend>`
- Star rating: replace Unicode stars with `<span aria-label="4 out of 5 stars">` pattern; hide decorative stars with `aria-hidden`
- Sale price: strikethrough original price must be announced with context ("Was $149, now $89")
- Price range slider: `role="slider"`, `aria-valuenow`, `aria-valuemin`, `aria-valuemax`, `aria-valuetext` with formatted price
- Add to Cart confirmation: `aria-live="polite"` region for cart action feedback; button label change timing
- Cart badge count: `aria-live="polite"` region for the header cart count; or `aria-label` update on the cart button
- Availability status: color alone does not communicate "Low Stock" — needs text or icon with accessible label
- Pagination: navigation landmark with `aria-label="Product pagination"`, current page `aria-current="page"`
- Testing strategy
- Implementation tasks with a11y-critic checkpoints

## Scope Hints

This is a **MODERATE** difficulty fixture — the challenge is breadth (many component sub-patterns to address) plus two non-obvious decisions: star rating representation and price announcement. Expected plan length: 3-4 pages. Focus on:

1. Product list semantics: `<ul role="list">` with `<li>` cards — each card's product name is a heading (`<h2>` if within a `<section>`, or `<h3>` if the page has section headings)
2. Star rating: Unicode stars in DOM are read as individual characters by some AT — use `<span class="sr-only">4 out of 5 stars</span>` and `aria-hidden="true"` on the visual stars
3. Sale price announcement: `<s aria-hidden="true">$149</s><span class="sr-only">Was $149, now</span> $89` pattern
4. Price range slider: two `role="slider"` elements with coordinated `aria-valuetext` ("Minimum price: $25") — not a generic `<input type="range">`
5. Cart action feedback: a persistent but initially empty `<div aria-live="polite" aria-atomic="true">` in the DOM; write cart confirmation message into it on "Add to Cart" — do NOT use `aria-live` on the toast element (toast appears after DOM insertion, live region must pre-exist)
6. Cart badge: `aria-label="Cart, 3 items"` updated on the cart button/link, not a live region for every increment

## What Success Looks Like

An excellent plan would:
- ✓ Specify `<ul>` product list semantics with product name as a heading element inside each card
- ✓ Document the star rating pattern: `aria-hidden="true"` on visual stars, `<span class="sr-only">` for spoken equivalent
- ✓ Address sale price: both original and sale price readable in sequence with context ("Was $149, now $89") via `<s aria-hidden>` and visible text
- ✓ Plan the price range slider as two `role="slider"` elements with `aria-valuemin`, `aria-valuemax`, `aria-valuenow`, `aria-valuetext`
- ✓ Document the pre-existing live region pattern for cart confirmation (region must exist in DOM before content is written into it)
- ✓ Specify cart badge as `aria-label` update on the cart button rather than a live region announcement per increment
- ✓ Address availability badge: "Low Stock" text must not rely on red color alone — text badge is sufficient without additional ARIA
- ✓ Cite WCAG 1.3.1, 1.4.1, 4.1.2, 4.1.3
- ✓ Include testing approach for cart action announcement and price range keyboard interaction

## What Would Be Below Expectations

- ✗ No star rating accessibility strategy — or only "add aria-label" without specifying the exact pattern
- ✗ Sale price with only `<del>` — `<del>` reads as "deleted" in some AT, not "was"; plan should specify `aria-hidden` on visual element plus SR-only text
- ✗ Price range slider planned as `<input type="range">` without ARIA — third-party component needs explicit ARIA attributes
- ✗ `aria-live` applied to the toast element itself — toast is inserted into DOM after creation, live region must pre-exist
- ✗ Cart badge updated via a live region on every add — chatty; `aria-label` update on the cart button is sufficient
- ✗ No filter panel landmark or `<fieldset>/<legend>` for checkbox groups
- ✗ Availability status relying only on color (red = out of stock) — fails WCAG 1.4.1
- ✗ No WCAG 4.1.3 citation for Add to Cart confirmation
