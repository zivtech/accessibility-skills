# Fixture: Client-Side Route Change With Title and Focus Handled (CLEAN)

## Component Code

```jsx
import { useEffect, useRef } from 'react';
import { NavLink, Routes, Route, useLocation, Outlet } from 'react-router-dom';

const SITE = 'Ridgeline Credit Union';

const SECTIONS = [
  { path: '/accounts', label: 'Accounts', title: 'Accounts' },
  { path: '/transfers', label: 'Transfers', title: 'Transfers' },
  { path: '/statements', label: 'Statements', title: 'Statements' },
];

const PortalShell = () => {
  const { pathname } = useLocation();
  const headingRef = useRef(null);
  const isFirstRender = useRef(true);

  const section = SECTIONS.find(s => s.path === pathname);

  // The title is the only string assistive technology treats as the page's
  // identity, so it is derived from the same list that renders the nav.
  useEffect(() => {
    document.title = section ? `${section.title} — ${SITE}` : SITE;
  }, [section]);

  // Focus follows the view. Skipped on first render: on a full page load the
  // browser has already put focus at the top of the document, and moving it
  // would take the user past content they have not seen.
  useEffect(() => {
    if (isFirstRender.current) {
      isFirstRender.current = false;
      return;
    }
    const frame = requestAnimationFrame(() => {
      window.scrollTo({ top: 0 });
      headingRef.current?.focus({ preventScroll: true });
    });
    return () => cancelAnimationFrame(frame);
  }, [pathname]);

  return (
    <div className="portal">
      <a className="skip-link" href="#main-content">
        Skip to main content
      </a>

      <header className="portal-header">
        <span className="brand">{SITE}</span>
        <nav aria-label="Account sections">
          <ul className="section-nav">
            {SECTIONS.map(({ path, label }) => (
              <li key={path}>
                <NavLink
                  to={path}
                  className={({ isActive }) => (isActive ? 'nav-link is-active' : 'nav-link')}
                  aria-current={pathname === path ? 'page' : undefined}
                >
                  {label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
      </header>

      <main id="main-content" className="portal-main">
        <h1 ref={headingRef} tabIndex={-1} className="view-heading">
          {section ? section.title : 'Not found'}
        </h1>
        <Outlet />
      </main>
    </div>
  );
};

const AccountsView = () => (
  <ul className="account-list">
    <li><a href="/accounts/checking">Everyday Checking &middot; $2,418.06</a></li>
    <li><a href="/accounts/savings">Reserve Savings &middot; $9,120.44</a></li>
  </ul>
);

const TransfersView = () => (
  <>
    <p>Move money between your accounts or to someone else.</p>
    <button type="button" className="primary">Start a transfer</button>
  </>
);

const StatementsView = () => (
  <ul className="statement-list">
    <li><a href="/statements/2026-08">August 2026 (PDF)</a></li>
    <li><a href="/statements/2026-07">July 2026 (PDF)</a></li>
  </ul>
);

const PortalRoutes = () => (
  <Routes>
    <Route element={<PortalShell />}>
      <Route path="/accounts" element={<AccountsView />} />
      <Route path="/transfers" element={<TransfersView />} />
      <Route path="/statements" element={<StatementsView />} />
    </Route>
  </Routes>
);

export default PortalRoutes;
```

```html
<!-- index.html — the initial title; every route replaces it via the effect above -->
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Ridgeline Credit Union</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

## CSS

```css
.portal-header {
  display: flex;
  align-items: center;
  gap: 32px;
  padding: 12px 24px;
  border-bottom: 1px solid #d0d5dd;
}

.section-nav {
  display: flex;
  gap: 20px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-link {
  color: #1d2939;
  text-decoration: none;
  padding: 6px 2px;
  border-bottom: 2px solid transparent;
}

.nav-link.is-active {
  color: #0b4fa8;
  border-bottom-color: #0b4fa8;
  font-weight: 600;
}

.nav-link:focus-visible,
.skip-link:focus-visible,
.primary:focus-visible,
.view-heading:focus-visible {
  outline: 3px solid #0b4fa8;
  outline-offset: 2px;
}

.skip-link {
  position: absolute;
  left: -9999px;
}

.skip-link:focus {
  left: 8px;
  top: 8px;
  padding: 8px 12px;
  background: #fff;
  border: 2px solid #0b4fa8;
}

.portal-main {
  max-width: 760px;
  margin: 24px auto;
  padding: 0 16px;
}

.view-heading {
  font-size: 1.5rem;
  margin: 0 0 12px;
}

.account-list,
.statement-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.account-list li,
.statement-list li {
  padding: 10px 0;
  border-bottom: 1px solid #eaecf0;
}

.primary {
  padding: 8px 16px;
  border: 1px solid #0b4fa8;
  border-radius: 4px;
  background: #0b4fa8;
  color: #fff;
  cursor: pointer;
}
```

## Expected Behavior

- The header nav stays mounted; activating a section link swaps the content inside `<main>` without a full page load.
- On every client-side navigation the document title becomes "<Section> — Ridgeline Credit Union", so the browser tab, the back-history menu, and the screen reader's page-title command all name the current view.
- On every client-side navigation *after the first render*, focus moves to the view heading, which announces the new view and puts the next Tab inside the new content.
- The first page load leaves focus where the browser put it.
- The active section is marked `aria-current="page"`.

## Accessibility Features Present

1. **The title identifies the view, and comes from the same source as the nav** (`spa-route-change-clean.md:24-28`) — one `SECTIONS` list drives the nav label, the route, and the title, so a new section cannot ship with a stale title. The format puts the section first, which is what a screen reader user hears first when they check where they are and what a user with many tabs open can read in a narrow tab.

2. **Focus moves to the heading of the new view, not to the top of the page** (`spa-route-change-clean.md:33-43`) — the `<h1>` carries `tabIndex={-1}` (`:71-73`) so it can receive programmatic focus without entering the Tab order. The heading text is announced on focus, which tells a screen reader user that a navigation completed and what arrived, and the next Tab lands on the first control inside the new view rather than back in the nav.

3. **The first render is deliberately exempt** (`:34-37`) — on a full page load the browser has already positioned focus at the start of the document, and moving it into the heading would skip the skip link and the nav for a user who has not seen either yet. The `isFirstRender` guard makes route-driven focus apply only to route *changes*.

4. **Scroll and focus are handled separately** (`:38-42`) — the app scrolls the window to the top itself, then focuses with `preventScroll: true`. Calling `focus()` without `preventScroll` would let the browser choose the scroll position, which on a long view can leave the heading against the top edge or skip past sticky header chrome. Doing both in a `requestAnimationFrame` callback lets the new route's DOM commit first; focusing a node that React is about to replace silently does nothing.

5. **The heading has a visible focus indicator** (`:161-167`) — it is a programmatic focus target rather than a keyboard-reachable one, but the indicator is kept so that a sighted user who navigated by keyboard can see where focus landed.

## Difficulty Level

**CLEAN** — Baseline for false-positive avoidance on client-side route changes. The `tabIndex={-1}` heading, the first render that deliberately does not move focus, the absence of an `aria-live` route announcer, and `preventScroll` on the focus call are each a correct decision that reads like a defect to a reviewer applying a rule mechanically rather than reasoning about what the user hears and where focus lands.
