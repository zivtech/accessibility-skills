# Fixture: Mega Menu Without Proper Structure and Navigation

## Component Code

```jsx
import React, { useState } from 'react';

const BuggyMegaMenu = ({ items = [] }) => {
  const [openMenu, setOpenMenu] = useState(null);

  return (
    <div className="megamenu-container">
      {/* BUG: No <nav> to identify as navigation */}
      {/* BUG: Menu items are not a semantic list */}
      <div className="megamenu-items">
        {items.map((item, idx) => (
          <div
            key={idx}
            className="menu-item"
            onClick={() => setOpenMenu(openMenu === idx ? null : idx)}
            // BUG: Click on div, not button
            // BUG: No role="button"
            // BUG: No keyboard support
            // BUG: No aria-expanded
          >
            {item.label}
            {openMenu === idx && (
              <div className="submenu">
                {/* BUG: Submenu is div, not semantic list */}
                {/* BUG: No role="menu" or submenu role */}
                {item.children &&
                  item.children.map((child, cidx) => (
                    <div key={cidx} className="submenu-item">
                      {/* BUG: Submenu items are divs, not links or buttons */}
                      {child}
                    </div>
                  ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default BuggyMegaMenu;
```

## Expected Behavior

- Navigation landmark identifies menu
- Menu items are semantic buttons with keyboard support
- Submenu expands/collapses with aria-expanded
- Submenu items are accessible via keyboard (arrow keys)
- Mouse and keyboard users can navigate full menu

## Accessibility Features Present

✓ Menu structure visible
✓ Expansion mechanic works on click

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Missing <nav> landmark** — Menu is just a div, not a navigation landmark. Screen reader user cannot identify as site navigation. Per HTML, main navigation should use <nav> element.
   - Evidence: `megamenu-no-structure.md:8-9` (div instead of nav)
   - User group: Screen reader users (critical)
   - Expected: Menu should be wrapped in <nav>
   - Fix: Replace div with <nav> element

2. **CRITICAL: Menu items are divs instead of buttons** — Menu triggers are divs with click handlers, not buttons. Keyboard users cannot activate with Space/Enter. Per semantic HTML, interactive elements must be buttons or have proper keyboard handling.
   - Evidence: `megamenu-no-structure.md:13-19` (div with onClick)
   - User group: Keyboard users (critical)
   - Expected: Menu items should be <button> elements
   - Fix: Replace menu-item divs with <button> elements

3. **CRITICAL: Submenu items are divs, not links** — Submenu items are divs with no semantic meaning or keyboard support. Keyboard user cannot navigate submenu items. Per pattern, submenu should contain <a> or <button> elements.
   - Evidence: `megamenu-no-structure.md:27-33` (divs instead of links/buttons)
   - User group: Keyboard users (critical)
   - Expected: Submenu items should be <a> or <button>
   - Fix: Replace submenu divs with semantic links or buttons

4. **MAJOR: No role="menu" on submenu** — Submenu div has no semantic role. Screen reader doesn't identify as menu. Per ARIA, submenus should have role="menu" and items should have role="menuitem".
   - Evidence: `megamenu-no-structure.md:23-33` (submenu div has no role)
   - User group: Screen reader users
   - Expected: Submenu should have role="menu"
   - Fix: Add role="menu" to submenu div and role="menuitem" to items

5. **MAJOR: No arrow key navigation** — Only mouse click works, no arrow key support. Keyboard user navigating by Tab cannot open/navigate submenu with arrow keys. Per ARIA menu pattern, arrow keys should open and navigate submenus.
   - Evidence: `megamenu-no-structure.md:13-19` (only onClick handler, no onKeyDown)
   - User group: Keyboard users
   - Expected: Arrow key handlers should open/navigate menu
   - Fix: Add onKeyDown handlers for ArrowDown/Right to open submenu

6. **MAJOR: Missing aria-expanded on menu items** — Submenu state (open/closed) not announced. Screen reader user doesn't know if menu item is expandable or expanded.
   - Evidence: `megamenu-no-structure.md:13-19` (no aria-expanded)
   - User group: Screen reader users
   - Expected: Menu item should have aria-expanded={isExpanded}
   - Fix: Add aria-expanded attribute to menu items

## Difficulty Level

**HAS-BUGS** — Mega menu rendered but semantic structure and navigation pattern completely missing. Multiple pattern violations.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Difficulty Rating

A11y-critic should identify that mega menus are complex navigation patterns requiring nav landmark, semantic buttons, submenu roles, keyboard navigation, and aria-expanded. This tests understanding of menu patterns and comprehensive keyboard support.
