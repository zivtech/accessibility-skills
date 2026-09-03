# Fixture: Client-Side Route Change Leaves Focus and Title Behind

## Component Code

```jsx
import { NavLink, Navigate, Routes, Route } from 'react-router-dom';

const AccountsView = () => (
  <section className="view">
    <h1>Accounts</h1>
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
    <ul className="statement-list" role="list">
      <li><a href="/files/statement-2026-08.pdf">August 2026 statement (PDF)</a></li>
      <li><a href="/files/statement-2026-07.pdf">July 2026 statement (PDF)</a></li>
    </ul>
  </section>
);

const NotFoundView = () => (
  <section className="view">
    <h1>Page not found</h1>
    <p>Choose a section from the menu above.</p>
  </section>
);

const SECTIONS = [
  { path: '/accounts', label: 'Accounts', Component: AccountsView },
  { path: '/transfers', label: 'Transfers', Component: TransfersView },
  { path: '/statements', label: 'Statements', Component: StatementsView },
];

const PortalShell = () => (
  <div className="portal">
    <a className="skip-link" href="#main-content">
      Skip to main content
    </a>

    <header className="portal-header">
      <span className="brand">Ridgeline Credit Union</span>
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

    <main id="main-content" tabIndex={-1} className="portal-main">
      <Routes>
        <Route path="/" element={<Navigate to="/accounts" replace />} />
        {SECTIONS.map(({ path, Component }) => (
          <Route key={path} path={path} element={<Component />} />
        ))}
        <Route path="*" element={<NotFoundView />} />
      </Routes>
    </main>
  </div>
);

export default PortalShell;
```

```html
<!-- index.html — the only place a title is set for the whole application -->
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
- The active section is styled with an underline, and `NavLink` marks it `aria-current="page"`.
- Each section renders its own `<h1>` inside the shared `<main>` landmark.
- The application root redirects to `/accounts`, and any unmatched URL renders the not-found view rather than an empty shell.
- Browser back and forward move between sections, because these are real routes with real URLs.

## Accessibility Issues (Planted)

1. **CRITICAL: Focus is left on the nav link after the view is replaced** — Activating a section link swaps everything inside `<main>`, but nothing moves focus. The browser's own focus reset does not apply: this is a client-side transition, so focus stays exactly where it was, on the link that was just activated. A screen reader user hears the link name and then silence — no title change, no heading, nothing that says a new view arrived; the only way to discover that anything happened is to start reading. A sighted keyboard user is left mid-header and has to Tab through the rest of the nav to reach the content that has already replaced itself on screen. The skip link at `spa-route-change-unannounced.md:57-59` does not rescue them, because it sits **before** the nav in the DOM: from a focused nav link, Tab moves forward past it, so reaching `#main-content` means shift-Tabbing backwards to a link most users do not know is there.
   - Evidence: `spa-route-change-unannounced.md:55-90` — `PortalShell` does not observe the route at all: no `useLocation`, no ref, no effect, no focus call. `<main>` at `:80` carries `tabIndex={-1}`, so a focus target exists and nothing ever uses it; none of the four views (`:8-47`) is a focus target either.
   - WCAG citation: 2.4.3 Focus Order — the conventional home for this defect. It is not a bright-line failure the way 2.4.2 below is: 2.4.3 does not literally forbid leaving focus in place, and 4.1.3 Status Messages is written for changes the user did not initiate. The substantive authority is WAI's SPA guidance; the criterion is where auditors file it.
   - User group: Screen reader users; keyboard-only users
   - Expected: After the route commits, focus should move into the new view — conventionally its `<h1>` given `tabIndex={-1}`, or the `<main>` element that already has one — so the new content is announced and the next Tab lands inside it.
   - Fix: Observe `pathname`, and once the new view has rendered call `focus({ preventScroll: true })` on the view heading, skipping the initial render so first page load is left to the browser.

2. **MAJOR: The document title never changes between sections** — `<title>Ridgeline Credit Union</title>` is set once in `index.html` (`:101`) and no route updates it. Every section is therefore "Ridgeline Credit Union": the browser tab, every entry in the back-history menu, and every bookmark are indistinguishable, and a screen reader user who checks where they are — the title is what is announced on window switch, and what NVDA's Insert+T and VoiceOver's VO+F2 report — is told the site name and nothing about the view. The URL changed and the heading changed; the one string assistive technology treats as the page's identity did not.
   - Evidence: `spa-route-change-unannounced.md:96-107` (single static `<title>`); `:55-90` (no `document.title` assignment on route change anywhere in the shell)
   - WCAG citation: 2.4.2 Page Titled — uncontested here, because these are real URLs producing real history entries
   - User group: Screen reader users; users with cognitive disabilities relying on history and tab labels; users with multiple tabs open
   - Expected: Each route should set a title naming the section and the site, e.g. "Transfers — Ridgeline Credit Union".
   - Fix: Set `document.title` in the same pathname-keyed effect that moves focus, from the `SECTIONS` list rather than a second hardcoded string.

## Difficulty Level

**HAS-BUGS** — Everything a scanner and a quick read look for is present and correct: real `<a href>` links, a labelled `<nav>`, `aria-current="page"` from `NavLink`, a single `<h1>` per view, a `<main>` landmark that is itself a focus target, a working skip link, an index redirect and a catch-all route, visible focus indicators, and a header that wraps. Both defects are about what happens *between* renders rather than what is in any one of them, so they are only reachable by asking where focus is and what the title says after the transition, not by inspecting the markup of either view.
