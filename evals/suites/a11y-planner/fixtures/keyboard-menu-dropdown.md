# Fixture: Menu Button with Dropdown

## Feature Description

A menu button that opens a dropdown list with selectable items. The component:
- Button labeled "Menu" or "Actions"
- Clicking button opens/closes dropdown list below
- Dropdown contains 5-8 menu items
- User can select items via click or keyboard
- Escape key closes the menu
- Focus management: where should focus go when menu opens?
- Visual focus indicator on menu items

## Context

- **Platform:** React application
- **Existing code:** No, new component
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** JAWS, NVDA, keyboard-only users
- **Scope:** Reusable menu button component
- **Constraints:** Some items may be disabled; Nested submenus (optional)

## Requirement

Plan accessibility covering:
- APG Menu Button pattern mapping
- Button role and aria-expanded
- Menu/menuitem roles and aria-disabled
- Keyboard navigation (Arrow Up/Down within menu)
- Focus movement on menu open (to first or button?)
- Escape key to close menu
- Focus restoration to button
- Screen reader announcements
- Visual focus indicators

## Scope Hints

This is **MODERATE** difficulty. Plan should be 3 pages:

1. APG Menu Button pattern reference
2. ARIA attributes (aria-expanded, roles, aria-disabled)
3. Keyboard model (Arrow Up/Down, Enter, Escape, Tab)
4. Focus trap vs focus movement strategy
5. Screen reader experience
6. Test cases for keyboard and screen reader

## What Success Looks Like

- ✓ APG Menu Button pattern with URL
- ✓ Button role with aria-expanded
- ✓ Menu and menuitem roles documented
- ✓ Keyboard interaction documented
- ✓ Focus management clarified
- ✓ WCAG citations
