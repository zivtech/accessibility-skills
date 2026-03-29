# Fixture: Mega-Menu Navigation With Hover-Only Submenus

## Component Code

```jsx
import React, { useState } from 'react';

const menuItems = [
  { id: 'products', label: 'Products', href: '/products', children: [
    { label: 'Widget Pro', href: '/products/widget-pro' },
    { label: 'Widget Lite', href: '/products/widget-lite' },
    { label: 'API Toolkit', href: '/products/api-toolkit' },
    { label: 'Enterprise Suite', href: '/products/enterprise' },
  ]},
  { id: 'solutions', label: 'Solutions', href: '/solutions', children: [
    { label: 'For Startups', href: '/solutions/startups' },
    { label: 'For Enterprise', href: '/solutions/enterprise' },
    { label: 'For Education', href: '/solutions/education' },
  ]},
  { id: 'resources', label: 'Resources', href: '/resources', children: [
    { label: 'Documentation', href: '/docs' },
    { label: 'Blog', href: '/blog' },
    { label: 'Community', href: '/community' },
    { label: 'Support', href: '/support' },
  ]},
  { id: 'pricing', label: 'Pricing', href: '/pricing', children: [] },
];

const MegaMenu = () => {
  const [openMenu, setOpenMenu] = useState(null);

  return (
    <div className="page">
      <a href="#main-content" className="skip-link">Skip to main content</a>

      <header className="site-header">
        <a href="/" className="logo">Acme Corp</a>
        <nav aria-label="Main navigation">
          <ul className="nav-list">
            {menuItems.map(item => (
              <li
                key={item.id}
                className="nav-item"
                // BUG: mouseenter only — no keyboard trigger — WCAG 2.1.1
                onMouseEnter={() => setOpenMenu(item.id)}
                // BUG: mouseleave immediately hides — no grace period — WCAG 1.4.13
                onMouseLeave={() => setOpenMenu(null)}
              >
                <a href={item.href} className="nav-link">
                  {item.label}
                </a>

                {item.children.length > 0 && openMenu === item.id && (
                  // BUG: No role="menu" — just nested links in a div
                  <div className="submenu">
                    {item.children.map(child => (
                      <a key={child.href} href={child.href} className="submenu-link">
                        {child.label}
                      </a>
                    ))}
                  </div>
                )}
              </li>
            ))}
          </ul>
        </nav>
      </header>

      <main id="main-content">
        <h1>Welcome to Acme Corp</h1>
        <p>Build something amazing with our tools and platform.</p>
      </main>
    </div>
  );
};

export default MegaMenu;
```

```css
.page { font-family: system-ui, sans-serif; }

.skip-link {
  position: absolute; left: -10000px; top: auto;
  width: 1px; height: 1px; overflow: hidden;
  padding: 12px 24px; background: #1565c0; color: #fff;
  text-decoration: underline; font-weight: 600; z-index: 100;
}
.skip-link:focus { position: static; width: auto; height: auto; }

.site-header {
  display: flex; align-items: center; gap: 32px;
  padding: 12px 24px; border-bottom: 1px solid #ddd; background: #fff;
}

.logo { font-size: 1.25rem; font-weight: 700; color: #111; text-decoration: none; }
.logo:focus { outline: 3px solid #005fcc; outline-offset: 4px; }

.nav-list {
  display: flex; gap: 0; list-style: none; margin: 0; padding: 0;
}

.nav-item { position: relative; }

.nav-link {
  display: block; padding: 12px 16px;
  color: #1565c0;          /* 5.4:1 on white */
  text-decoration: underline;
  font-weight: 500; font-size: 0.95rem;
}

/* Visual focus on top-level items — correct */
.nav-link:focus-visible {
  outline: 3px solid #005fcc; outline-offset: 2px;
}

/* BUG: Submenu appears with slide-down, no prefers-reduced-motion */
.submenu {
  position: absolute; top: 100%; left: 0;
  min-width: 200px; background: #fff;
  border: 1px solid #ddd; border-radius: 0 0 4px 4px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  display: flex; flex-direction: column;
  z-index: 20;
  animation: slideDown 0.2s ease;
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}

/* BUG: No @media (prefers-reduced-motion: reduce) to disable animation */

.submenu-link {
  display: block; padding: 10px 16px;
  color: #333;             /* 12.6:1 */
  text-decoration: underline;
  font-size: 0.9rem;
}

.submenu-link:hover { background: #f5f5f5; }
.submenu-link:focus-visible { outline: 2px solid #005fcc; outline-offset: -2px; background: #e3f2fd; }

main { padding: 32px 24px; max-width: 800px; }
main h1 { font-size: 2rem; margin-bottom: 16px; }
main p { font-size: 1.1rem; color: #333; line-height: 1.6; }
```

## Expected Behavior

- Horizontal navigation bar with 4 top-level links
- Hovering over Products, Solutions, or Resources reveals a submenu
- Submenu contains child links
- Skip link available for keyboard users

## Accessibility Features Present

- Skip link to main content (visible on focus)
- `<nav>` with `aria-label`
- All top-level items are `<a>` elements with descriptive text
- All links are underlined
- Focus-visible outlines on all links
- Submenu links are real `<a>` elements
- `<main>` landmark with heading

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Submenus appear on mouseenter only — no keyboard trigger — WCAG 2.1.1 (Keyboard)**
   Submenus are controlled via `onMouseEnter`/`onMouseLeave`. No `onFocus`, `onKeyDown`, or `aria-expanded` handling. Keyboard users Tab to "Products" but the submenu never opens — they can only reach the top-level href.
   - Evidence: Lines 43-45 — onMouseEnter/Leave only; no focus handlers
   - User group: Keyboard users, switch users
   - Fix: Add onFocus/onBlur handlers, aria-expanded on parent, keyboard Enter/Space/ArrowDown to open

2. **MAJOR: Submenu disappears immediately on mouseleave — WCAG 1.4.13 (Content on Hover or Focus)**
   No hover grace period or delay. Moving the mouse diagonally from the parent to a submenu item causes the submenu to close because the mouse briefly leaves the nav-item bounds.
   - Evidence: Line 45 — `onMouseLeave={() => setOpenMenu(null)}` fires immediately
   - User group: Motor impairment users, magnification users
   - Fix: Add 300ms delay on mouseleave; use a "hover intent" triangle pattern

3. **MAJOR: No Escape key handler to close open submenu — WCAG 1.4.13**
   No keyboard mechanism to dismiss the submenu. WCAG 1.4.13 requires Escape to dismiss hover/focus content.
   - Evidence: No onKeyDown handler in the component
   - User group: Keyboard users
   - Fix: Add onKeyDown for Escape that closes submenu and returns focus to parent

4. **MINOR: Submenu slide-down animation without prefers-reduced-motion — WCAG 2.3.3**
   `.submenu` has `animation: slideDown 0.2s ease` with no `@media (prefers-reduced-motion)` guard.
   - Evidence: CSS @keyframes slideDown with no reduced-motion override
   - User group: Vestibular users
   - Fix: `@media (prefers-reduced-motion: reduce) { .submenu { animation: none; } }`

5. **MINOR: Submenu items not wrapped in role="menu" — WCAG 4.1.2**
   Submenu is a plain `<div>` with child `<a>` elements. No `role="menu"` or `role="menuitem"`. Screen readers don't announce it as a menu.
   - Evidence: Line 55 — `<div className="submenu">` with no ARIA role
   - User group: Screen reader users
   - Fix: Add `role="menu"` on container, `role="menuitem"` on links

## Difficulty Level

**ADVERSARIAL** — Passes axe-core (all links are real anchors, contrast is fine, labels present). The failures are in interaction patterns (hover-only reveal, no keyboard trigger) requiring keyboard/motor perspective reasoning.

## Frameworks

React 18+, CSS
