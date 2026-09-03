# Fixture: Client-Side Route Change With Title and Focus Handled (CLEAN)

## Component Code

```jsx
import { useEffect, useRef } from 'react';
import { NavLink, Routes, Route, useLocation, Outlet } from 'react-router-dom';

const SITE = 'Ridgeline Credit Union';

const SECTIONS = [
  { path: '/accounts', label: 'Accounts' },
  { path: '/transfers', label: 'Transfers' },
];

// The heading and the title come from the view that rendered, never from a
// second match against the pathname: React Router ignores trailing slashes and
// matches case-insensitively, so a hand-rolled `pathname === path` lookup
// desyncs from it and would title a real view "Page not found".
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

      <nav aria-label="Account sections">
        <ul>
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

      <main id="main-content" tabIndex={-1} ref={mainRef}>
        <Outlet />
      </main>
    </div>
  );
};

const AccountsView = () => (
  <>
    <ViewHeading>Accounts</ViewHeading>
    <p>Everyday Checking &middot; $2,418.06</p>
  </>
);

const TransfersView = () => (
  <>
    <ViewHeading>Transfers</ViewHeading>
    <button type="button">Start a transfer</button>
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
      <Route path="*" element={<NotFoundView />} />
    </Route>
  </Routes>
);

export default PortalRoutes;
```

## CSS

```css
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

.nav-link {
  color: #1d2939;
}

.nav-link.is-active {
  color: #0b4fa8;
  font-weight: 600;
  text-decoration: underline;
}

a:focus-visible,
button:focus-visible,
main:focus-visible,
.view-heading:focus-visible {
  outline: 3px solid #0b4fa8;
  outline-offset: 2px;
}
```

## Expected Behavior

- The nav stays mounted; activating a section link swaps the content inside `<main>` without a full page load.
- Each view sets the document title from its own heading text, so the browser tab, the back-history menu and the screen reader's page-title command all name the view that actually rendered.
- On every client-side navigation *after the first render*, focus moves to the heading of the new view.
- The first page load leaves focus where the browser put it, whichever URL it lands on.
- The portal is mounted at `/accounts`; any unmatched URL, `/` included, renders the not-found view, which has its own heading and its own title.
- `NavLink` marks the active section `aria-current="page"`.

## Accessibility Features Present

1. **The title comes from the view that rendered, not from a second match against the URL** (`spa-route-change-clean.md:20-30`) — `ViewHeading` renders the `<h1>` and sets `document.title` from the same string, so the two cannot disagree and no route can render under another route's title.

2. **Focus moves to the heading of the new view** (`spa-route-change-clean.md:41-53`) — the `<h1>` carries `tabIndex={-1}` (`:26`) so it can take programmatic focus without entering the Tab order, and the shell finds it inside its own `<main>` rather than threading a ref through every view. The heading is announced on focus, and the next Tab lands inside the new content.

3. **The first render is deliberately exempt, and the guard survives StrictMode** (`:39,46-47`) — moving focus on a full page load would take the user past the skip link and the nav before they had seen either. The guard compares the previous pathname rather than flipping a boolean, because React re-runs mount effects in StrictMode development builds. There is no root redirect for the same reason: a redirect fires a second render with a changed pathname, which reads as a navigation.

4. **Scroll and focus are handled separately** (`:48-52`) — the component scrolls to the top itself, then focuses with `preventScroll: true`, so the browser's scroll-into-view heuristic never picks the position. The `requestAnimationFrame` lets the new route's DOM commit first, so the heading queried from `<main>` is the new view's.

5. **Both programmatic focus targets have a visible indicator** (`:144-150`) — neither `<main>` nor the heading is keyboard-reachable, so 2.4.7 does not reach either, but the indicator is kept on both. Without it on `<main>`, a successful skip-link activation would be invisible: `<main>` is already on screen and nothing else changes.
