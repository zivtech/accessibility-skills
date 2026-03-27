# Fixture: Breadcrumb Navigation

## Feature Description

You're planning accessibility for a breadcrumb navigation showing the current page hierarchy:
- Home > Products > Electronics > Laptops (current page)
- Each item except the last is a link
- Last item (current page) is not a link (static text)
- Links navigate to parent pages
- Arrow separators between items (visual only)

## Context

- **Platform:** E-commerce website
- **Existing code:** No, new component
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA, VoiceOver, keyboard-only users
- **Scope:** Reusable breadcrumb component
- **Constraints:** Variable depth (2-5 levels); Current page indicator needed

## Requirement

Plan accessibility covering:
- Semantic nav element and ol/li structure
- aria-current="page" for current item
- Link text clarity ("Laptops" vs "Go to Laptops")
- Tab order (each link focusable)
- Focus indicators
- Visual separator handling (css-only, hidden from SR)
- WCAG citations

## Scope Hints

This is **MODERATE** difficulty. Plan should be 2-3 pages:

1. Semantic nav, ol, li structure
2. aria-current="page" documentation
3. Link text strategy
4. Tab order (left-to-right)
5. Visual separators (css-only)
6. Test cases

## What Success Looks Like

- ✓ Semantic nav element
- ✓ ol list structure documented
- ✓ aria-current="page" for current item
- ✓ Clear link text strategy
- ✓ Tab order documented
- ✓ Visual separators hidden from screen readers
- ✓ WCAG citations
