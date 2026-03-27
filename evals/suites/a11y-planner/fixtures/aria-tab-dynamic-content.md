# Fixture: Tab Panel with Dynamic Content

## Feature Description

You're planning accessibility for a tab interface where tab panel content loads asynchronously when tabs are selected. The component:
- Multiple tabs in a tab list (role="tablist")
- Each tab can be selected (via click or keyboard)
- When a tab is selected, its associated panel loads content (could be a delay while fetching from API)
- Tab shows loading state during fetch (spinner, "Loading..." text)
- Only one tab's panel is visible at a time
- Focus management when switching tabs
- Optional: some tabs may be disabled

## Context

- **Platform:** Vue.js web application
- **Existing code:** No, this is a new component
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** JAWS, NVDA, VoiceOver, keyboard-only users
- **Scope:** Reusable tab component with async content loading
- **Constraints:** Content can take 1-3 seconds to load; Must support mobile; Error states possible (load failure)

## Requirement

Create a comprehensive accessibility design plan covering:
- HTML structure (tablist, tab, tabpanel)
- ARIA attributes (role, aria-selected, aria-controls, aria-labelledby, aria-disabled)
- Keyboard interaction (Left/Right arrows to switch tabs, Home/End to jump to first/last)
- Focus management (focus moves to selected tab or first focusable element in panel?)
- Loading state communication (aria-busy, live region announcements)
- Error state handling (failed load, retry button)
- Screen reader announcements (selected tab, loading state, completion, error)
- Testing strategy for keyboard, async, and error scenarios

## Scope Hints

This is a **MODERATE** difficulty fixture. The APG Tab pattern is well-documented but async loading adds complexity. Plan should be 3-4 pages:

1. Mapping to APG Tab pattern with URL
2. Complete ARIA attributes for tablist, tab, tabpanel
3. Keyboard interaction (Left/Right, Home/End, Tab)
4. Focus management strategy for tab switching
5. aria-busy and live region for loading state
6. Error handling and retry communication
7. Disabled tab handling
8. Test cases for async, errors, keyboard, and screen reader

## What Success Looks Like

An excellent plan would:
- ✓ Reference APG Tab pattern with explicit URL
- ✓ Specify aria-selected, aria-controls, aria-labelledby with WCAG citations
- ✓ Document keyboard interactions: Left/Right arrows, Home, End, Tab exits
- ✓ Include HTML structure stub with tablist, tab, tabpanel
- ✓ Plan focus management: clarify if focus moves to panel or stays on tab
- ✓ Plan aria-busy during loading with live region announcements
- ✓ Document error state: aria-describedby linking tab to error message
- ✓ Plan disabled tabs: aria-disabled="true" with explanation
- ✓ Include test cases for loading, errors, keyboard, screen reader

## What Would Be Below Expectations

- ✗ No APG Tab pattern reference
- ✗ Missing aria-controls (linking tabs to panels)
- ✗ No keyboard interaction documentation
- ✗ No plan for loading state communication
- ✗ No error handling strategy
- ✗ Unclear focus management
- ✗ No test cases for async scenarios
- ✗ Missing consideration of disabled tabs
