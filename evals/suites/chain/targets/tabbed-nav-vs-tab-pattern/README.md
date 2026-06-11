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

## The Ambiguity

This component uses the WAI-ARIA Tabs pattern for what is effectively **page-level navigation**. Each "tab" triggers a Next.js route change (`router.push()`), loading entirely different page content. The tabs pattern is implemented correctly per the APG spec — but the semantic model may be wrong.

**Argument for Tabs pattern (defender):**
- The visual and interaction design IS tabs. Users see tabs, expect tab behavior, get tab behavior.
- Content is subsections of a single product page — conceptually "panels" even if technically different routes.
- Arrow key navigation is the expected interaction model for this visual pattern.
- Screen readers announce "tab, 2 of 4, selected" which correctly describes the UI.
- The APG doesn't prohibit using tabs for route-based content.

**Argument for Navigation pattern (challenger):**
- Each "tab" loads a different URL. This is navigation, not panel switching.
- Screen reader users navigating by landmark would expect `<nav>` with links, not a tablist.
- The `role="tabpanel"` wraps content that doesn't exist in the same DOM — it's loaded via router.
- Browser back/forward creates a navigation history, which tabs shouldn't.
- Links (`<a href>`) provide built-in behaviors: right-click "open in new tab", cmd+click, URL sharing. Buttons with router.push() lose all of these.
- SEO: links are crawlable, buttons are not.

**Why this is genuinely hard:**
Neither side is clearly wrong. The tabs pattern correctly describes the user's interaction model. The nav pattern correctly describes the underlying technical model. The right answer depends on which model you prioritize — and reasonable accessibility experts disagree.

## Frameworks & Environment

React 18+ with Next.js App Router

## Notes

This is an ADVERSARIAL fixture. The "correct" review is NOT to flag one side as wrong, but to:

1. Recognize that both approaches have legitimate accessibility arguments
2. Articulate the specific tradeoff (interaction model vs semantic model)
3. Explain who is affected by each choice and how
4. Make a recommendation with reasoning, acknowledging the other side
5. Avoid treating this as a clear-cut bug

A reviewer that simply says "this should be nav with links" without acknowledging why tabs were chosen is as incomplete as a reviewer that says "this is fine" without noting the semantic tension.

---

_This directory contains component files extracted from the a11y eval suite for chain evaluation._
_Run `/a11y-workflow full evals/suites/chain/targets/tabbed-nav-vs-tab-pattern/component.jsx` to start the chain._
