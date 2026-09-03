# Fixture: Client-Side Route Change Leaves Focus and Title Behind

## Component Code

```jsx
import { NavLink, Routes, Route, useLocation } from 'react-router-dom';

const AccountsView = () => (
  <section className="view">
    <h1>Accounts</h1>
    <ul className="account-list">
      <li><a href="/accounts/checking">Everyday Checking &middot; $2,418.06</a></li>
      <li><a href="/accounts/savings">Reserve Savings &middot; $9,120.44</a></li>
    </ul>
  </section>
);

const TransfersView = () => (
  <section className="view">
    <h1>Transfers</h1>
    <p>Move money between your accounts or to someone else.</p>
    <button type="button" className="primary">Start a transfer</button>
  </section>
);

const StatementsView = () => (
  <section className="view">
    <h1>Statements</h1>
    <ul className="statement-list">
      <li><a href="/statements/2026-08">August 2026 (PDF)</a></li>
      <li><a href="/statements/2026-07">July 2026 (PDF)</a></li>
    </ul>
  </section>
);

const SECTIONS = [
  { path: '/accounts', label: 'Accounts', Component: AccountsView },
  { path: '/transfers', label: 'Transfers', Component: TransfersView },
  { path: '/statements', label: 'Statements', Component: StatementsView },
];

const PortalShell = () => {
  const { pathname } = useLocation();

  return (
    <div className="portal">
      <a className="skip-link" href="#main-content">
        Skip to main content
      </a>

      <header className="portal-header">
        <span className="brand">Ridgeline Credit Union</span>
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
        <Routes>
          {SECTIONS.map(({ path, Component }) => (
            <Route key={path} path={path} element={<Component />} />
          ))}
        </Routes>
      </main>
    </div>
  );
};

export default PortalShell;
```

```html
<!-- index.html — the only place a title is set for the whole application -->
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
.primary:focus-visible {
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

.view h1 {
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
- The active section is styled with an underline and marked `aria-current="page"`.
- Each section renders its own `<h1>` inside the shared `<main>` landmark.
- Browser back and forward move between sections, because these are real routes with real URLs.

## Accessibility Issues (Planted)

1. **CRITICAL: Focus is left on the nav link after the view is replaced** — Activating a section link swaps everything inside `<main>`, but nothing moves focus. The browser's own focus reset does not apply: this is a client-side transition, so focus stays exactly where it was, on the link that was just activated. A screen reader user hears the link name and then silence — no title change, no heading, nothing that says a new view arrived; the only way to discover that anything happened is to start reading. A sighted keyboard user is left mid-header and has to Tab through the rest of the nav to reach the content that has already replaced itself on screen. The skip link at `spa-route-change-unannounced.md:47-49` does not rescue them, because it sits **before** the nav in the DOM: from a focused nav link, Tab moves forward past it, so reaching `#main-content` means shift-Tabbing backwards to a link most users do not know is there.
   - Evidence: `spa-route-change-unannounced.md:42-79` — `PortalShell` reads `pathname` for `aria-current` only; there is no ref, no effect keyed on the pathname, and no focus target anywhere in the route views (`:8-34`, no `tabIndex={-1}` on any `<h1>`).
   - WCAG citation: 2.4.3 Focus Order (after a view replacement, the focus position no longer corresponds to the content on screen)
   - User group: Screen reader users; keyboard-only users
   - Expected: After the route commits, focus should move into the new view — conventionally its `<h1>` given `tabIndex={-1}` — so the heading is announced and the next Tab lands inside the new content.
   - Fix: Hold a ref to the view heading, and in an effect keyed on `pathname` call `focus({ preventScroll: true })` on it once the new view has rendered, skipping the initial mount so first page load is left to the browser.

2. **MAJOR: The document title never changes between sections** — `<title>Ridgeline Credit Union</title>` is set once in `index.html` (`:90`) and no route updates it. Every section is therefore "Ridgeline Credit Union": the browser tab, every entry in the back-history menu, and every bookmark are indistinguishable, and a screen reader user who checks where they are — the title is what is announced on window switch, and what NVDA's Insert+T and VoiceOver's VO+F2 report — is told the site name and nothing about the view. The URL changed and the heading changed; the one string assistive technology treats as the page's identity did not.
   - Evidence: `spa-route-change-unannounced.md:85-96` (single static `<title>`); `:42-79` (no `document.title` assignment on route change anywhere in the shell)
   - WCAG citation: 2.4.2 Page Titled (a client-side view change produces a new page for the user and needs a title that describes it)
   - User group: Screen reader users; users with cognitive disabilities relying on history and tab labels; users with multiple tabs open
   - Expected: Each route should set a title naming the section and the site, e.g. "Transfers — Ridgeline Credit Union".
   - Fix: Set `document.title` in the same pathname-keyed effect that moves focus, from the section's own label rather than a second hardcoded list.

## Difficulty Level

**HAS-BUGS** — Everything a scanner and a quick read look for is present and correct: real `<a href>` links, a labelled `<nav>`, `aria-current="page"`, a single `<h1>` per view, a `<main>` landmark, a working skip link, visible focus indicators. Both defects are about what happens *between* renders rather than what is in any one of them, so they are only reachable by asking where focus is and what the title says after the transition, not by inspecting the markup of either view.
