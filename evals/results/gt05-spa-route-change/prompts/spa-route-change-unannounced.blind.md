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
