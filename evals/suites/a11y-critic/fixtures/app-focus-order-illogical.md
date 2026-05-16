# Fixture: App Layout with Illogical Focus Order

## Component Code

```jsx
import React from 'react';
import './AppLayout.css';

const AppLayout = () => {
  return (
    <div className="app-layout">
      <a href="#content" className="skip-link">
        Skip to main content
      </a>

      <header className="app-header">
        <div className="logo">
          <a href="/">Acme Dashboard</a>
        </div>
        <nav aria-label="Header navigation">
          <ul className="header-nav">
            <li><a href="/notifications">Notifications</a></li>
            <li><a href="/settings">Settings</a></li>
            <li><a href="/profile">Profile</a></li>
          </ul>
        </nav>
      </header>

      <div className="app-body">
        {/* BUG: Main content appears BEFORE sidebar in DOM order.
            CSS order: -1 on sidebar visually moves it left,
            but keyboard tab order follows DOM: main → sidebar */}
        <main className="main-content">
          <div id="content">
            {/* BUG: Skip link targets this div, but div is not
                focusable — no tabindex="-1". Skip link does nothing. */}
            <h1>Dashboard</h1>
          </div>

          <section aria-labelledby="recent-heading">
            <h2 id="recent-heading">Recent Activity</h2>
            <ul className="activity-list">
              <li>
                <a href="/reports/q1">Q1 Performance Report</a>
                <span className="activity-date">May 12, 2026</span>
              </li>
              <li>
                <a href="/reports/q2">Q2 Forecast Draft</a>
                <span className="activity-date">May 10, 2026</span>
              </li>
              <li>
                <a href="/reports/audit">Annual Audit Summary</a>
                <span className="activity-date">May 8, 2026</span>
              </li>
            </ul>
          </section>

          <section aria-labelledby="tasks-heading">
            <h2 id="tasks-heading">Open Tasks</h2>
            <ul className="task-list">
              <li>
                <a href="/tasks/142">Review budget proposal</a>
                <span className="task-status">Due May 20</span>
              </li>
              <li>
                <a href="/tasks/143">Approve vendor contract</a>
                <span className="task-status">Due May 22</span>
              </li>
            </ul>
          </section>
        </main>

        <aside className="sidebar">
          <nav aria-label="Sidebar navigation">
            <h2 className="sidebar-heading">Navigation</h2>
            <ul className="sidebar-nav">
              <li><a href="/dashboard">Dashboard</a></li>
              <li><a href="/reports">Reports</a></li>
              <li><a href="/analytics">Analytics</a></li>
              <li><a href="/team">Team</a></li>
              <li><a href="/projects">Projects</a></li>
              <li><a href="/invoices">Invoices</a></li>
            </ul>
          </nav>
        </aside>
      </div>

      {/* BUG: tabIndex={1} forces this to receive focus BEFORE
          skip link and all other content */}
      <button
        className="fab"
        tabIndex={1}
        aria-label="Create new report"
        onClick={() => console.log('create report')}
      >
        +
      </button>
    </div>
  );
};

export default AppLayout;
```

## CSS

```css
/* ---- Skip Link ---- */
.skip-link {
  position: absolute;
  top: -40px;
  left: 16px;
  padding: 8px 16px;
  background: #1e293b;
  color: #ffffff;
  font-size: 14px;
  font-weight: 600;
  z-index: 100;
  border-radius: 0 0 4px 4px;
  text-decoration: none;
}

.skip-link:focus {
  top: 0;
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}

/* ---- Header ---- */
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  background: #1e293b;
  color: #ffffff;
}

.logo a {
  color: #ffffff;
  font-size: 18px;
  font-weight: 700;
  text-decoration: none;
}

.header-nav {
  display: flex;
  list-style: none;
  gap: 16px;
  margin: 0;
  padding: 0;
}

.header-nav a {
  color: #cbd5e1;
  text-decoration: none;
  font-size: 14px;
}

.header-nav a:hover {
  color: #ffffff;
}

.header-nav a:focus {
  outline: 2px solid #60a5fa;
  outline-offset: 2px;
}

/* ---- App Body (Flex Layout) ---- */

/* BUG: DOM order is main → sidebar, but CSS order: -1 on sidebar
   visually places sidebar on the left. Keyboard tab order follows
   DOM, so users tab through all main content before reaching sidebar. */
.app-body {
  display: flex;
  min-height: calc(100vh - 56px);
}

.sidebar {
  order: -1;
  width: 240px;
  flex-shrink: 0;
  background: #f8fafc;
  border-right: 1px solid #e2e8f0;
  padding: 24px 16px;
}

.main-content {
  flex: 1;
  padding: 32px 40px;
}

/* ---- Sidebar Nav ---- */
.sidebar-heading {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
  margin: 0 0 12px 0;
}

.sidebar-nav {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-nav li {
  margin-bottom: 2px;
}

.sidebar-nav a {
  display: block;
  padding: 8px 12px;
  color: #334155;
  text-decoration: none;
  font-size: 14px;
  border-radius: 6px;
}

.sidebar-nav a:hover {
  background: #e2e8f0;
  color: #0f172a;
}

/* BUG: Focus indicator on sidebar links has ~1.5:1 contrast ratio.
   #a8d0f0 (light blue) on #f8fafc (near-white sidebar background)
   fails the 3:1 minimum required by WCAG 2.4.7 / 2.4.13.
   Main content links below have a proper high-contrast indicator. */
.sidebar-nav a:focus {
  outline: 2px solid #a8d0f0;
  outline-offset: 2px;
}

/* ---- Main Content ---- */
.main-content h1 {
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 24px 0;
}

.main-content h2 {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 12px 0;
}

.activity-list,
.task-list {
  list-style: none;
  padding: 0;
  margin: 0 0 32px 0;
}

.activity-list li,
.task-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f1f5f9;
}

.activity-list a,
.task-list a {
  color: #2563eb;
  text-decoration: none;
  font-size: 14px;
}

.activity-list a:hover,
.task-list a:hover {
  text-decoration: underline;
}

/* Good focus indicator on main content links — 
   #2563eb on #ffffff is ~5.2:1, well above 3:1 */
.activity-list a:focus,
.task-list a:focus {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}

.activity-date,
.task-status {
  font-size: 12px;
  color: #64748b;
}

/* ---- Floating Action Button ---- */
.fab {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: none;
  background: #2563eb;
  color: #ffffff;
  font-size: 24px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 50;
}

.fab:hover {
  background: #1d4ed8;
}

.fab:focus {
  outline: 3px solid #1e40af;
  outline-offset: 3px;
}
```

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

## Accessibility Issues (Planted)

1. **MUST-FIND / MAJOR: Tab order does not match visual layout — CSS `order` creates DOM/visual mismatch.** The sidebar renders AFTER `<main>` in DOM order but visually appears on the LEFT via `order: -1` on `.sidebar` inside the flexbox `.app-body`. A keyboard user tabs through the skip link, then the header, then ALL main content links (5 links across 2 sections), and only THEN reaches sidebar navigation. The visual left-to-right reading order (sidebar → main) does not match the DOM tab order (main → sidebar).
   - Evidence: `app-focus-order-illogical.md:30-73` — `<main>` rendered before `<aside>` in JSX; CSS `.sidebar { order: -1 }` (line ~88 of CSS) visually reorders it left
   - WCAG: 2.4.3 Focus Order ("focusable components receive focus in an order that preserves meaning and operability"), 1.3.2 Meaningful Sequence
   - Impact: Keyboard user expecting to tab into sidebar first (matching visual layout) must instead tab through 5+ main content links. Disorienting — the focus appears to jump to the center of the page, skipping the left column entirely
   - User group: Keyboard users (all), screen reader users (tab order confusion)
   - Fix: Move `<aside>` before `<main>` in the DOM (matching visual order), remove `order: -1` from CSS

2. **SHOULD-FIND / MAJOR: Skip link targets a non-focusable element — clicking it does nothing for keyboard users.** The skip link's `href="#content"` points to `<div id="content">`, but a plain `<div>` is not focusable without `tabindex="-1"`. When a keyboard user activates the skip link, the browser may scroll to the element but focus does not move — the next Tab press goes to whatever follows the skip link in DOM order (the header logo), not to the main content area.
   - Evidence: `app-focus-order-illogical.md:33-36` — `<div id="content">` has no tabindex attribute
   - WCAG: 2.4.1 Bypass Blocks (skip link exists but doesn't function), 2.4.3 Focus Order
   - Impact: Skip link is cosmetically present but functionally broken. Keyboard users cannot bypass the header navigation. The feature exists in name only.
   - User group: Keyboard users, screen reader users
   - Fix: Add `tabindex="-1"` to the `<div id="content">` element, or move `id="content"` to the `<main>` element and add `tabindex="-1"` there

3. **SHOULD-FIND / MAJOR: Sidebar navigation focus indicators have insufficient contrast (~1.5:1).** The `.sidebar-nav a:focus` rule uses `outline: 2px solid #a8d0f0` (light blue). Against the sidebar's `#f8fafc` (near-white) background, this produces approximately 1.5:1 contrast ratio — well below the 3:1 minimum required by WCAG 2.4.7 (Focus Visible) and the enhanced 2.4.13 (Focus Appearance). Meanwhile, main content links use `#2563eb` focus outlines on white (~5.2:1), creating an inconsistent experience.
   - Evidence: CSS `.sidebar-nav a:focus { outline: 2px solid #a8d0f0 }` against `.sidebar { background: #f8fafc }` — computed contrast ratio ~1.5:1
   - WCAG: 2.4.7 Focus Visible ("any keyboard operable user interface has a mode of operation where the keyboard focus indicator is visible"), 2.4.13 Focus Appearance (3:1 minimum contrast for focus indicator)
   - Impact: Low-vision users and keyboard users on the sidebar cannot reliably see which link has focus. They can see focus on main content links but lose track when tabbing into the sidebar.
   - User group: Low-vision users, keyboard users
   - Fix: Change sidebar focus outline to a higher-contrast color, e.g., `#2563eb` (matching main content) or `#1e40af` (~8.6:1 on white)

4. **NICE-TO-FIND / MINOR: Positive `tabIndex={1}` on FAB forces it to receive focus before all other content.** The floating action button has `tabIndex={1}`, which places it in the tab order BEFORE every element with `tabIndex={0}` or no explicit tabindex. This means the FAB receives focus before the skip link, header navigation, sidebar, and main content. The "Create new report" button becomes the very first focusable element on the page — a nonsensical focus entry point that also defeats the skip link even if the skip link target were fixed.
   - Evidence: `app-focus-order-illogical.md:89-96` — `tabIndex={1}` on the `<button className="fab">`
   - WCAG: 2.4.3 Focus Order (positive tabindex creates unpredictable order)
   - WAI-ARIA Authoring Practices: "Do not use tabindex values greater than 0" — positive tabindex is an anti-pattern that creates maintenance nightmares and unpredictable focus order
   - Impact: First Tab press on the page goes to a button in the bottom-right corner. User must tab past it to reach the skip link. Compounds with Issue #2: even if the skip link worked, the FAB preempts it.
   - User group: Keyboard users
   - Fix: Remove `tabIndex={1}`, use `tabIndex={0}` or no tabindex (natural DOM order); if FAB should be easily reachable, use a keyboard shortcut or place it logically in the DOM

## Difficulty Level

**FLAWED** — The component uses semantic HTML, has a skip link, includes focus indicators on every interactive element, uses ARIA landmarks and labels correctly. A surface-level audit sees an application layout that "looks accessible." The four bugs require deeper analysis:

1. The CSS order bug requires understanding that `display: flex` + `order: -1` changes visual order but not tab order — you have to mentally map the DOM reading order against the rendered layout.
2. The broken skip link requires testing the target element's focusability, not just checking that `href="#content"` and `id="content"` match.
3. The focus contrast bug requires calculating (or estimating) the contrast ratio of `#a8d0f0` against `#f8fafc` — and noticing the inconsistency with main content focus indicators.
4. The positive tabindex requires knowing that `tabindex="1"` is an anti-pattern and tracing its effect on the entire page's focus sequence.

Each issue alone is individually subtle. Together, they compound into a keyboard experience where: the first Tab press goes to a bottom-right FAB (Issue 4), the skip link does nothing (Issue 2), main content is tabbed through before the visually-left sidebar (Issue 1), and sidebar focus indicators are nearly invisible (Issue 3).

Expected baseline detection: 15-35%. A zero-shot reviewer sees semantic HTML, skip link, ARIA landmarks, focus indicators, and concludes the layout is accessible. Finding the compounding effect requires tracing the actual tab sequence from start to finish.

## Frameworks & Environment

React 18+, standard HTML/CSS (no CSS modules or CSS-in-JS)

## Notes

This fixture tests four distinct reviewer skills:

1. **CSS-DOM interaction awareness** (must_find) — Can the critic identify that CSS visual reordering (`flex` + `order`) creates a mismatch between what sighted users see and what keyboard users experience? This requires reading the CSS alongside the JSX, not just scanning attributes.

2. **Skip link verification** (should_find) — Does the critic check that the skip link actually WORKS, not just that it exists? The `href` and `id` match perfectly — the bug is that the target element isn't focusable. Presence is not function.

3. **Focus indicator measurement** (should_find) — Does the critic evaluate focus indicator QUALITY, not just presence? Every element has a `:focus` rule. The bug is that one set of indicators has insufficient contrast — a distinction that requires color contrast awareness.

4. **Tabindex anti-pattern recognition** (nice_to_find) — Does the critic recognize positive tabindex as harmful and trace its effect on page-level focus order? This is well-known in a11y circles but often missed when the element is otherwise well-labeled.

The compound observation — that Issue 4 defeats Issue 2 even if Issue 2 were fixed — distinguishes thorough reviewers from checklist-followers.
