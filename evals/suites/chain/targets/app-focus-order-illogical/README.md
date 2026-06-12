# App Layout with Illogical Focus Order

## Description

Web app layout with header, sidebar, main content, and FAB. CSS order property creates visual/DOM tab order mismatch, skip link targets non-focusable element, sidebar focus indicators have insufficient contrast, and positive tabindex on FAB preempts all content.

## Expected Behavior

- Skip link allows keyboard users to bypass header and sidebar navigation, jumping directly to main content
- Tab order follows the visual layout: skip link → header → sidebar → main content → FAB
- Focus indicators are clearly visible on all interactive elements (minimum 3:1 contrast)
- Sidebar navigation appears on the left, main content on the right
- Floating action button is accessible but does not disrupt natural tab order

## Accessibility Features Present

✓ Skip link present with `href="#content"`
✓ Semantic HTML: `<header>`, `<main>`, `<aside>`, `<nav>`, `<section>`
✓ Landmark regions with distinct `aria-label` on each `<nav>`
✓ Heading hierarchy: h1 for page title, h2 for sections and sidebar
✓ Sections use `aria-labelledby` pointing to heading ids
✓ Focus indicators present on all interactive elements
✓ FAB has `aria-label="Create new report"`
✓ Lists use `<ul>`/`<li>` for navigation and content items

---

_This directory contains component files extracted from the a11y eval suite for chain evaluation._
_Run `/a11y-workflow full evals/suites/chain/targets/app-focus-order-illogical/component.jsx` to start the chain._
