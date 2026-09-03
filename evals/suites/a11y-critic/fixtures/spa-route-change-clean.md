# Fixture: Client-Side Route Change With Title and Focus Handled (CLEAN)

## Component Code

```jsx
import { useEffect, useRef } from 'react';
import { NavLink, Routes, Route, useLocation, Outlet } from 'react-router-dom';

const SITE = 'Ridgeline Credit Union';

const SECTIONS = [
  { path: '/accounts', label: 'Accounts' },
  { path: '/transfers', label: 'Transfers' },
  { path: '/statements', label: 'Statements' },
];

// Title and heading come from the view that actually rendered, never from a
// second match against the pathname: React Router ignores trailing slashes and
// matches case-insensitively, so a hand-rolled `pathname === path` lookup
// desyncs on /accounts/ and /Accounts and would title a real page "not found".
const ViewHeading = ({ children }) => {
  useEffect(() => {
    document.title = `${children} — ${SITE}`;
  }, [children]);

  return (
    <h1 tabIndex={-1} className="view-heading">
      {children}
    </h1>
  );
};

const PortalShell = () => {
  const { pathname } = useLocation();
  const mainRef = useRef(null);
  // The previous pathname, not a "have we mounted yet" boolean: React re-runs
  // mount effects in StrictMode dev builds, and a boolean flipped inside the
  // effect is already false on the repeat run, so focus would move on first
  // load after all. Comparing paths is idempotent under that repeat.
  const previousPath = useRef(pathname);

  // Focus follows the view. Skipped while the path is unchanged, which covers
  // the first render: on a full page load the browser has already put focus at
  // the top of the document, and moving it would take the user past content
  // they have not seen.
  useEffect(() => {
    if (previousPath.current === pathname) return;
    previousPath.current = pathname;
    const frame = requestAnimationFrame(() => {
      window.scrollTo({ top: 0 });
      mainRef.current?.querySelector('h1')?.focus({ preventScroll: true });
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
          <ul className="section-nav" role="list">
            {SECTIONS.map(({ path, label }) => (
              <li key={path}>
                <NavLink
                  to={path}
                  end
                  className={({ isActive }) => (isActive ? 'nav-link is-active' : 'nav-link')}
                >
                  {label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
      </header>

      <main id="main-content" tabIndex={-1} ref={mainRef} className="portal-main">
        <Outlet />
      </main>
    </div>
  );
};

const AccountsView = () => (
  <>
    <ViewHeading>Accounts</ViewHeading>
    <ul className="account-list" role="list">
      <li>
        <span className="acct-name">Everyday Checking</span>
        <span className="acct-balance">$2,418.06</span>
      </li>
      <li>
        <span className="acct-name">Reserve Savings</span>
        <span className="acct-balance">$9,120.44</span>
      </li>
    </ul>
  </>
);

const TransfersView = () => (
  <>
    <ViewHeading>Transfers</ViewHeading>
    <p>Move money between your accounts or to someone else.</p>
    <button type="button" className="primary">Start a transfer</button>
  </>
);

const StatementsView = () => (
  <>
    <ViewHeading>Statements</ViewHeading>
    <ul className="statement-list" role="list">
      <li><a href="/files/statement-2026-08.pdf">August 2026 statement (PDF)</a></li>
      <li><a href="/files/statement-2026-07.pdf">July 2026 statement (PDF)</a></li>
    </ul>
  </>
);

const NotFoundView = () => (
  <>
    <ViewHeading>Page not found</ViewHeading>
    <p>Choose a section from the menu above.</p>
  </>
);

const PortalRoutes = () => (
  <Routes>
    <Route element={<PortalShell />}>
      <Route path="/accounts" element={<AccountsView />} />
      <Route path="/transfers" element={<TransfersView />} />
      <Route path="/statements" element={<StatementsView />} />
      <Route path="*" element={<NotFoundView />} />
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
    <meta name="viewport" content="width=device-width, initial-scale=1" />
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
  flex-wrap: wrap;
  align-items: center;
  gap: 12px 32px;
  padding: 12px 24px;
  border-bottom: 1px solid #d0d5dd;
}

.section-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 20px;
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
  display: flex;
  justify-content: space-between;
  gap: 16px;
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
- Each view sets the document title from its own heading text, so the browser tab, the back-history menu, and the screen reader's page-title command all name the view that actually rendered.
- On every client-side navigation *after the first render*, focus moves to the heading of the new view, which announces it and puts the next Tab inside the new content.
- The first page load leaves focus where the browser put it, whichever URL it lands on.
- The portal is mounted at `/accounts`. `/` and any other unmatched URL render the not-found view, which has its own heading and its own title — so no URL produces a view that the nav claims is a different section.
- `NavLink` marks the active section `aria-current="page"`.

## Accessibility Features Present

1. **The title comes from the view that rendered, not from a second match against the URL** (`spa-route-change-clean.md:21-31`) — `ViewHeading` renders the `<h1>` and sets `document.title` from the same string, so the two can never disagree and no route can render under another route's title. Deriving them instead from a hand-rolled `pathname === path` lookup would desync from React Router itself, which ignores trailing slashes and matches case-insensitively: `/accounts/` would render the accounts view under a "Page not found" heading and title.

2. **Focus moves to the heading of the new view, not to the top of the page** (`spa-route-change-clean.md:42-54`) — the `<h1>` carries `tabIndex={-1}` (`:27`) so it can receive programmatic focus without entering the Tab order, and the shell finds it inside its own `<main>` rather than holding a ref that would have to be threaded through every view. The heading text is announced on focus, so a screen reader user learns that a navigation completed and what arrived, and the next Tab lands on the first control inside the new view rather than back in the nav.

3. **The first render is deliberately exempt, and the guard survives StrictMode** (`:40,47-48`) — on a full page load the browser has already positioned focus at the start of the document, and moving it into the heading would skip the skip link and the nav for a user who has not seen either yet. The guard compares the previous pathname rather than flipping a boolean, because React re-runs mount effects in StrictMode development builds: a boolean set to false on the first run would let the repeat run move focus after all. There is no root redirect for the same reason — a redirect fires a second render with a changed pathname, which would read as a navigation and move focus on the most common cold entry of all.

4. **Scroll and focus are handled separately** (`:49-52`) — the app scrolls the window to the top itself, then focuses with `preventScroll: true`. Calling `focus()` without `preventScroll` would let the browser choose the scroll position, which on a long view can leave the heading against the top edge or skip past sticky header chrome. Doing both in a `requestAnimationFrame` callback lets the new route's DOM commit first, so the heading queried from `<main>` is the new view's.

5. **The heading has a visible focus indicator** (`:193-199`) — it is a programmatic focus target rather than a keyboard-reachable one, but the indicator is kept so that a sighted user who navigated by keyboard can see where focus landed.

6. **The route table has no dead ends and no disagreements** (`:129-138`) — every route renders a view that owns its heading and title, and a catch-all covers everything else, so no URL yields an empty document or a stale title. There is deliberately no index route and no root redirect: a redirect fires a second render that reads as a navigation and steals focus on cold entry, and an index route rendering a section at `/` would leave `NavLink ... end` inactive there, putting a section on screen that no nav item claims.

## Accessibility Issues (None Planted — CLEAN Baseline)

None. This fixture is the correct-implementation half of a pair; everything
below this heading is withheld from model prompts by the harness.

## Difficulty Level

**CLEAN** — Baseline for false-positive avoidance on client-side route changes. The `tabIndex={-1}` heading, the first render that deliberately does not move focus, the absence of an `aria-live` route announcer, and `preventScroll` on the focus call are each a correct decision that reads like a defect to a reviewer applying a rule mechanically rather than reasoning about what the user hears and where focus lands.
