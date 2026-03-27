# Fixture: Navigation with Skip Link (CLEAN)

## Component Code

```jsx
const MainLayout = ({ children }) => {
  return (
    <div className="layout">
      {/* Skip link allows keyboard users to bypass navigation */}
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>

      <nav className="main-nav" aria-label="Main navigation">
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/about">About</a></li>
          <li><a href="/services">Services</a></li>
          <li><a href="/contact">Contact</a></li>
        </ul>
      </nav>

      <main id="main-content">
        {children}
      </main>

      <footer>
        <p>&copy; 2024 Example Company</p>
      </footer>
    </div>
  );
};

export default MainLayout;
```

## CSS

```css
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #0066cc;
  color: white;
  padding: 8px 16px;
  text-decoration: none;
  z-index: 100;
}

.skip-link:focus {
  top: 0; /* Reveals on focus */
}

.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-nav {
  background: #333;
  padding: 0;
}

.main-nav ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  gap: 20px;
}

.main-nav a {
  display: block;
  color: white;
  text-decoration: none;
  padding: 16px;
}

.main-nav a:focus {
  outline: 3px solid #0066cc;
  outline-offset: -3px;
}

main {
  flex: 1;
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

footer {
  background: #f5f5f5;
  padding: 20px;
  text-align: center;
  color: #666;
}
```

## Expected Behavior

- Skip link is hidden by default
- Skip link appears on keyboard focus (visible)
- Clicking skip link focuses main content
- Navigation clearly marked with aria-label
- Footer is semantic footer element
- Main content in semantic main element

## Accessibility Features Implemented

✓ Skip link hidden off-screen, revealed on focus
✓ Skip link functional (href="#main-content")
✓ Navigation with proper aria-label
✓ Semantic landmarks: nav, main, footer
✓ Proper heading hierarchy (if headings used in main)
✓ Clear link text
✓ Focus indicators visible on nav links
✓ List semantics for navigation

## Difficulty Level

**CLEAN** — Proper implementation of skip links and landmark navigation. Should receive clean verdict.

## Notes

A11y-critic should verify:
1. Skip link is present and functional
2. Hidden by default, revealed on focus
3. Landmark regions used (nav, main, footer)
4. Navigation list semantics correct
5. Focus indicators visible

No critical issues. May note enhancement (aria-current on current page in nav), but overall clean.
