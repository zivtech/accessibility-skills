# Fixture: Combobox with Autocomplete

## Feature Description

You're planning accessibility for a search input with autocomplete/typeahead functionality. The component:
- User types in an input field
- Filtered results appear in a dropdown list below the input
- Results can be selected with keyboard (Arrow Up/Down, Enter) or mouse
- Selection updates the input value and closes the dropdown
- Can include grouped results (e.g., "People", "Organizations")
- Supports clearing the input and reopening the dropdown

## Context

- **Platform:** React web application with custom component library
- **Existing code:** No, this is a new component built on WAI-ARIA Combobox pattern
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA (Windows), JAWS, VoiceOver (macOS), keyboard-only users
- **Scope:** Reusable combobox component for search, filtering, and selection
- **Constraints:** Must work on desktop and mobile; results can be dynamically fetched from API; Must support async loading

## Requirement

Create a comprehensive accessibility design plan that covers the full APG Combobox pattern including:
- HTML structure for input, listbox, and options
- Complete ARIA implementation (roles, properties, states)
- Keyboard interaction model (typing, Arrow Up/Down, Enter, Escape, Tab)
- Focus management (focus in input, focus on filtered results, announcements)
- Loading state communication (aria-busy, live region)
- Option filtering and list updates
- Screen reader announcements for result count and selection
- Testing strategy with keyboard and screen reader scenarios

## Scope Hints

This is a **MODERATE** difficulty fixture. The APG Combobox pattern is complex with many attributes (aria-expanded, aria-owns/aria-controls, aria-activedescendant, aria-autocomplete). The plan should be 3-4 pages and address:

1. Mapping to APG Combobox pattern with URL
2. Complete ARIA attributes for input, listbox, options (aria-expanded, aria-owns, aria-activedescendant, aria-autocomplete, aria-controls)
3. Keyboard interaction (type, arrow keys, Enter to select, Escape to close, Tab to exit)
4. Focus management between input and filtered results
5. Dynamic updates to result list (aria-live for count, aria-busy for loading)
6. Screen reader announcements (number of results, selected item, loading state)
7. Option grouping and announcement strategy
8. Test cases for API delays, empty results, and keyboard selection

## What Success Looks Like

An excellent plan would:
- ✓ Reference APG Combobox pattern with explicit URL
- ✓ Specify complete ARIA attributes: aria-expanded, aria-owns/aria-controls, aria-activedescendant, aria-autocomplete="list"
- ✓ Document keyboard interactions: typing, Arrow Up/Down to navigate, Enter to select, Escape to close, Tab to exit
- ✓ Include HTML structure stub with input, listbox, and option elements
- ✓ Plan focus management: focus stays in input while user types, no focus movement to list
- ✓ Plan live region announcements for result count and loading state
- ✓ Document ARIA state changes: aria-expanded true/false, aria-activedescendant updates, aria-busy during load
- ✓ Include test cases for keyboard navigation, screen reader announcements, async loading, empty results
- ✓ Cite WCAG 2.1.1 (Keyboard), 4.1.2 (Name Role Value), 4.1.3 (Status Messages)

## What Would Be Below Expectations

- ✗ No APG Combobox pattern reference or generic reference without URL
- ✗ Incomplete ARIA attributes (mentions aria-expanded but not aria-owns or aria-activedescendant)
- ✗ No keyboard interaction documentation
- ✗ Unclear focus management strategy (should focus move to results or stay in input?)
- ✗ No plan for async loading state communication
- ✗ No test cases or testing strategy
- ✗ Vague about screen reader announcements
- ✗ Missing consideration of mobile/touch interactions
