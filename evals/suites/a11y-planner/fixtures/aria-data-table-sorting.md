# Fixture: Custom Data Table with Sorting

## Feature Description

You're planning accessibility for a data table with sortable column headers. The component:
- Semantic HTML table (thead, tbody, tr, td)
- Column headers that are clickable to sort
- Sorting indicator (icon or text showing ascending/descending/none)
- Multiple columns sortable (one at a time or multiple?)
- Visual sorting indicator (arrow icon, background color)
- Keyboard navigation within table (Tab moves to next cell, arrow keys optional)
- Screen reader announces sort order
- Potentially large table (100+ rows, pagination possible)

## Context

- **Platform:** React data visualization library
- **Existing code:** No, new component
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** JAWS, NVDA, VoiceOver, keyboard-only users
- **Scope:** Reusable data table with flexible columns
- **Constraints:** Can be very large (pagination needed); Column headers must be keyboard accessible; Multiple tables on one page possible

## Requirement

Create a comprehensive accessibility design plan for a sortable data table covering:
- Semantic HTML structure (table, thead, tbody, tfoot, tr, th, td)
- Column scope attributes (scope="col")
- Sorting indicator implementation (aria-sort with WCAG citations)
- Keyboard navigation (Tab order, arrow keys for navigation)
- Focus management (focus visible on headers and cells)
- Sort state communication (aria-sort values: none/ascending/descending)
- Screen reader experience (header announcements, sort order, current cell position)
- Pagination strategy (if applicable)
- Testing strategy for keyboard, screen reader, and large data sets

## Scope Hints

This is a **COMPLEX** difficulty fixture. Tables are semantically straightforward but accessibility interactions are nuanced. Plan should be 4-5 pages:

1. Complete semantic HTML structure with thead, tbody, scope attributes
2. Mapping to table semantics (not ARIA roles)
3. aria-sort implementation with states and WCAG citations
4. Keyboard navigation strategy (Tab order within table)
5. Focus management for interactive headers
6. Large data set considerations (pagination, row count announcements)
7. Screen reader experience planning
8. Test cases for keyboard navigation, sort verification, visual sort indicator

## What Success Looks Like

An excellent plan would:
- ✓ Document complete HTML table semantics (thead, tbody, scope="col")
- ✓ Explain table header role and announcement strategy
- ✓ Document aria-sort values with WCAG 2.2 citations
- ✓ Specify keyboard navigation (Tab order, arrow navigation optional)
- ✓ Plan focus indicator for headers and focusable cells
- ✓ Document sort state communication to screen readers
- ✓ Address large data set handling (pagination)
- ✓ Include HTML structure stub showing table markup
- ✓ Plan visual sort indicator with non-color alternative

## What Would Be Below Expectations

- ✗ Missing semantic table elements (scope attributes)
- ✗ Using ARIA roles instead of semantic HTML
- ✗ No aria-sort documentation
- ✗ Unclear keyboard navigation strategy
- ✗ No consideration of large data sets
- ✗ Missing screen reader announcement strategy
- ✗ Vague about visual sort indicator
- ✗ No test cases
