# Tabbed Navigation Using Tab Pattern for Page-Level Routes

## Description

Next.js component using complete WAI-ARIA Tabs pattern for page-level route navigation. Technically correct tab implementation but semantic model arguably wrong — tabs vs nav is genuinely debatable.

## Expected Behavior

- Clicking a tab navigates to that product section (different URL/route)
- Arrow Left/Right cycles through tabs, triggering route navigation
- Active tab reflects the current URL
- Each section is a distinct page with its own content
- Browser back/forward works (each tab is a route change)

## Accessibility Features Present

✓ role="tablist" with aria-label
✓ role="tab" on each button
✓ aria-selected reflects current route
✓ aria-controls links tab to content panel
✓ role="tabpanel" wrapping page content
✓ aria-labelledby on tabpanel linking to tab
✓ Roving tabindex
✓ Arrow key navigation (Left, Right, Home, End)
✓ Visible focus indicator
✓ Complete WAI-ARIA Tabs pattern implementation

## Design Rationale (Why Tabs)

The designer chose the tabs pattern because:
1. The UI looks and behaves exactly like tabs — horizontal bar, one active, panel below
2. Users interact with it as tabs — arrow keys to navigate, one section visible at a time
3. The content areas are thematically grouped subsections of a single product
4. The tab metaphor is immediately understandable to users

---

_This directory contains component files extracted from the a11y eval suite for chain evaluation._
_Run `/a11y-workflow full evals/suites/chain/targets/tabbed-nav-vs-tab-pattern/component.jsx` to start the chain._
