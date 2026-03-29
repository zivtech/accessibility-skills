# Fixture: Navigation Menu With Complete Landmarks (CLEAN)

## Component Code

```jsx
import React from 'react';

const NavMenuPage = () => (
  <div className="page">
    <a href="#main-content" className="skip-link">Skip to main content</a>

    <header className="site-header">
      <a href="/" className="logo" aria-label="Acme Corp home">Acme Corp</a>
      <nav aria-label="Primary navigation">
        <ul>
          <li><a href="/products">Products</a></li>
          <li><a href="/solutions">Solutions</a></li>
          <li><a href="/pricing">Pricing</a></li>
          <li><a href="/docs">Documentation</a></li>
          <li><a href="/contact">Contact us</a></li>
        </ul>
      </nav>
    </header>

    <nav aria-label="Breadcrumb">
      <ol className="breadcrumb">
        <li><a href="/">Home</a></li>
        <li><a href="/products">Products</a></li>
        <li><a href="/products/widget" aria-current="page">Widget Pro</a></li>
      </ol>
    </nav>

    <div className="content-layout">
      <main id="main-content">
        <h1>Widget Pro</h1>
        <p>Our flagship product for enterprise teams. Built for speed, designed for scale.</p>
        <section aria-labelledby="features-heading">
          <h2 id="features-heading">Key Features</h2>
          <ul>
            <li>Real-time collaboration</li>
            <li>Advanced analytics dashboard</li>
            <li>Custom integrations via API</li>
            <li>Role-based access control</li>
          </ul>
        </section>
        <section aria-labelledby="pricing-heading">
          <h2 id="pricing-heading">Pricing</h2>
          <p>Starting at $29/month per seat. <a href="/pricing">See full pricing</a>.</p>
        </section>
      </main>

      <aside aria-label="Related products">
        <h2>Related Products</h2>
        <nav aria-label="Related product links">
          <ul>
            <li><a href="/products/widget-lite">Widget Lite</a></li>
            <li><a href="/products/widget-enterprise">Widget Enterprise</a></li>
            <li><a href="/products/api-toolkit">API Toolkit</a></li>
          </ul>
        </nav>
      </aside>
    </div>

    <footer>
      <nav aria-label="Footer navigation">
        <ul className="footer-links">
          <li><a href="/privacy">Privacy policy</a></li>
          <li><a href="/terms">Terms of service</a></li>
          <li><a href="/accessibility">Accessibility statement</a></li>
        </ul>
      </nav>
      <p className="copyright">&copy; 2026 Acme Corp. All rights reserved.</p>
    </footer>
  </div>
);

export default NavMenuPage;
```

```css
.page {
  font-family: system-ui, sans-serif;
  color: #222;              /* #222 on #fff = 14.7:1 */
}

.skip-link {
  position: absolute;
  left: -10000px;
  top: auto;
  width: 1px;
  height: 1px;
  overflow: hidden;
  padding: 12px 24px;
  background: #1565c0;
  color: #fff;              /* #fff on #1565c0 = 5.4:1 */
  text-decoration: underline;
  font-weight: 600;
  z-index: 100;
}

.skip-link:focus {
  position: static;
  width: auto;
  height: auto;
}

.site-header {
  display: flex;
  align-items: center;
  gap: 32px;
  padding: 16px 24px;
  border-bottom: 1px solid #ccc;
}

.logo {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111;
  text-decoration: none;
}

.logo:focus {
  outline: 3px solid #005fcc;
  outline-offset: 4px;
}

.site-header nav ul {
  display: flex;
  gap: 24px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.site-header nav a {
  color: #1565c0;          /* #1565c0 on white = 5.4:1 */
  text-decoration: underline;
  font-weight: 500;
}

.site-header nav a:focus {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}

.breadcrumb {
  display: flex;
  gap: 8px;
  list-style: none;
  padding: 12px 24px;
  margin: 0;
  font-size: 0.9rem;
}

.breadcrumb li::after { content: '/'; margin-left: 8px; color: #999; }
.breadcrumb li:last-child::after { content: ''; }

.breadcrumb a {
  color: #1565c0;
  text-decoration: underline;
}

.breadcrumb a[aria-current="page"] {
  color: #333;
  font-weight: 600;
  text-decoration: none;
}

.breadcrumb a:focus { outline: 2px solid #005fcc; outline-offset: 2px; }

.content-layout {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 32px;
  padding: 24px;
  max-width: 1080px;
}

@media (max-width: 768px) {
  .content-layout { grid-template-columns: 1fr; }
}

main h1 { font-size: 2rem; margin-bottom: 16px; }
main h2 { font-size: 1.25rem; margin-top: 24px; margin-bottom: 8px; }
main p { line-height: 1.6; }
main a { color: #1565c0; text-decoration: underline; }
main a:focus { outline: 3px solid #005fcc; outline-offset: 2px; }

aside {
  padding: 16px;
  background: #f5f5f5;
  border-radius: 4px;
}

aside h2 { font-size: 1.1rem; margin-bottom: 12px; }
aside ul { list-style: none; padding: 0; }
aside li { margin-bottom: 8px; }
aside a { color: #1565c0; text-decoration: underline; }
aside a:focus { outline: 2px solid #005fcc; outline-offset: 2px; }

footer {
  border-top: 1px solid #ccc;
  padding: 24px;
  margin-top: 32px;
}

.footer-links {
  display: flex;
  gap: 24px;
  list-style: none;
  padding: 0;
  margin: 0 0 8px;
}

.footer-links a {
  color: #1565c0;
  text-decoration: underline;
}

.footer-links a:focus { outline: 2px solid #005fcc; outline-offset: 2px; }

.copyright { font-size: 0.85rem; color: #555; }
```

## Expected Behavior

- Full product page with header, breadcrumb, main content, sidebar, footer
- Primary navigation in header with 5 links
- Breadcrumb trail: Home > Products > Widget Pro
- Main content with product info sections
- Sidebar with related product links
- Footer with legal links

## Accessibility Features Present

- Skip link to main content (visually hidden, appears on focus)
- `<header>`, `<main>`, `<aside>`, `<footer>` landmarks
- 4 `<nav>` elements each with distinct `aria-label` (Primary, Breadcrumb, Related, Footer)
- Breadcrumb uses `<ol>` with `aria-current="page"` on current item
- All links have descriptive text (no "click here")
- All links are underlined (WCAG 1.4.1)
- Heading hierarchy: h1 for page, h2 for sections, with `aria-labelledby`
- Focus-visible outlines on all interactive elements
- Responsive layout (single column below 768px)
- All color contrast passes WCAG AA (ratios in CSS comments)

## Accessibility Issues

**NONE.** This page correctly implements all landmark, navigation, and semantic patterns.

Optional enhancement a reviewer MAY note:
1. Could add `aria-expanded` on a mobile menu toggle (desktop view shown has no hamburger menu)

## Difficulty Level

**CLEAN** — All navigation patterns, landmarks, and semantics are correctly implemented. Tests false-positive rate — a reviewer should produce ACCEPT.

## Frameworks

React 18+, CSS Grid
