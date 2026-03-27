# Fixture: Custom Disclosure Widget

## Feature Description

You're planning accessibility for a custom disclosure/accordion widget that allows users to expand and collapse content sections. The widget:
- Has multiple disclosure items (e.g., FAQ sections)
- Each item has a button trigger that shows/hides associated content
- Multiple sections can be open simultaneously (not exclusive)
- When a button is clicked or Space/Enter is pressed, the associated content panel toggles visible/hidden

## Context

- **Platform:** React web application
- **Existing code:** No, this is a new component
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA (Windows), VoiceOver (macOS), keyboard-only users
- **Scope:** Single disclosure component (reusable)
- **Constraints:** Must work in a design system; must support mobile (touch)

## Requirement

Create a comprehensive accessibility design plan that a developer with no accessibility knowledge can use to implement the component correctly on the first attempt.

The plan should cover:
- Semantic structure
- ARIA implementation (pattern mapping, attributes)
- Keyboard interaction model
- Focus management
- State communication
- Visual accessibility
- Content accessibility
- Testing strategy
- Implementation tasks with a11y-critic checkpoints

## Scope Hints

This is a **TRIVIAL** difficulty fixture — a well-documented pattern with straightforward interactions. The plan should be concise (1-2 pages) but complete. Focus on:

1. Mapping to the APG Disclosure pattern with URL citation
2. Specifying the exact ARIA attributes (aria-expanded, aria-controls) and their WCAG citations
3. Documenting keyboard interactions (Tab focuses button, Space/Enter toggles)
4. Planning basic focus management (no focus trap needed)
5. Ensuring state is communicated both visually and programmatically
6. Specifying test cases

## What Success Looks Like

An excellent plan would:
- ✓ Reference APG Disclosure pattern with explicit URL
- ✓ Specify aria-expanded and aria-controls with WCAG citations
- ✓ Document keyboard interactions (Tab, Space, Enter)
- ✓ Include HTML structure stub with semantic elements
- ✓ Plan focus indicator visibility and contrast
- ✓ Document state communication (aria-expanded true/false)
- ✓ Include test cases (keyboard, screen reader, visual)
- ✓ Be concise (1-2 pages, no scope creep)

## What Would Be Below Expectations

- ✗ No APG pattern reference or generic reference without URL
- ✗ ARIA attributes mentioned but not cited to WCAG
- ✗ No keyboard interaction documentation
- ✗ No focus management planning (even trivial components need it)
- ✗ No test cases or testing strategy
- ✗ Vague implementation guidance ("use aria-expanded" without specifics)
- ✗ Missing consideration of screen reader announcements

