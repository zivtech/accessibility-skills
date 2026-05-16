# Fixture: Data Table Testing

## Feature Description

You're planning accessibility testing for a sortable, paginated data table used in a financial reporting dashboard. The table displays 50 rows per page of transaction records with 7 columns: Date, Description, Category, Amount, Status, Account, and Actions. The "Actions" column contains a dropdown menu button per row.

The table:
- Uses semantic `<table>` with `<thead>`, `<tbody>`, `<th scope="col">` for column headers
- Column headers for Date, Amount, and Status are sortable — clicking them toggles sort ascending/descending/none; current sort direction shown via `aria-sort` attribute
- Sort state changes trigger an `aria-live="polite"` region announcing the new sort (e.g., "Sorted by Date, ascending")
- Pagination: Previous/Next buttons and a page indicator ("Page 2 of 15"); focus stays on the Previous/Next button after page change
- Row actions: Each row's Actions column has a `<button>` that opens an inline dropdown menu (Edit, Delete, View Details) via the APG menu button pattern
- Table is horizontally scrollable on smaller viewports
- Caption reads "Transaction Records — 742 results"

## Context

- **Platform:** React web application using a custom DataTable component
- **Existing code:** Yes, component exists — engineering team has flagged it as a known accessibility risk
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA (Windows), JAWS (Windows), VoiceOver (macOS), keyboard-only users
- **Scope:** DataTable component including pagination, sort controls, and per-row action menus
- **Constraints:** Table has complex interaction model (sort + pagination + per-row menus); team has limited axe-core experience; tests must be maintained by a QA team that rotates; NVDA + Chrome is the primary test combination

## Requirement

Create a comprehensive accessibility testing plan that a QA engineer with basic accessibility knowledge can execute. The plan should be structured enough for consistent execution across team members.

The plan should cover:
- Automated testing setup (axe-core, Playwright)
- Table semantics testing (scope, caption, header association)
- Sort state testing (aria-sort transitions, announcement)
- Keyboard navigation of cells and sortable headers
- Screen reader table mode navigation
- Pagination keyboard and screen reader behavior
- Per-row dropdown menu accessibility
- Responsive behavior testing
- Test prioritization and execution order
- Acceptance criteria
- a11y-critic review checkpoints

## Scope Hints

This is a **COMPLEX** difficulty fixture — multiple independently complex subsystems (table semantics, sort state, pagination, per-row menus) that all interact with screen reader table mode and keyboard navigation. Expected plan length is 5-7 pages. Focus on:

1. Table semantics: axe-core rules `td-headers-attr`, `th-has-data-cells`, `scope-attr-valid`; verify header scope attributes
2. Sort state: aria-sort transitions (none → ascending → descending → none); announce each transition via aria-live
3. Screen reader table mode: NVDA in Browse Mode (B key for table), cell navigation (Ctrl+Alt+Arrow), header announcement per cell
4. Pagination: keyboard test of Previous/Next buttons; screen reader announcement of page change; focus management after page load
5. Per-row menus: APG Menu Button pattern; Arrow key navigation within menu; Escape closes menu and restores focus to trigger button
6. Responsive behavior: Horizontal scroll works with keyboard; 200% zoom does not lose column headers; no horizontal scroll of the full page

## What Success Looks Like

An excellent plan would:
- ✓ Name specific axe-core rules for tables (`td-headers-attr`, `th-has-data-cells`, `scope-attr-valid`, `table-duplicate-name`)
- ✓ Script the sort state transition test: click Date header → verify aria-sort="ascending" → verify aria-live announcement
- ✓ Document NVDA table mode navigation: Ctrl+Alt+Right/Left/Up/Down to navigate cells; column header announced per cell
- ✓ Provide acceptance criteria for each sort state: "aria-sort attribute cycles none→ascending→descending→none with each click"
- ✓ Test pagination focus management: Previous button click → focus stays on Previous button (or moves appropriately if disabled)
- ✓ Test the per-row dropdown via APG Menu Button pattern with Arrow key navigation
- ✓ Specify Playwright assertions for aria-sort and aria-live region content
- ✓ Cover responsive test: table scrolls horizontally with keyboard; headers remain visible
- ✓ Distinguish the two table navigation modes (Table mode vs Browse mode in NVDA)

## What Would Be Below Expectations

- ✗ "Verify table has proper headings" without naming which axe rules or scope attributes
- ✗ Sort test described as "verify sort works" without testing aria-sort attribute values and aria-live announcement
- ✗ No documentation of NVDA table mode (Ctrl+Alt+Arrow navigation) — a critical gap for table testing
- ✗ Pagination testing limited to "verify buttons work" without covering focus management after page change
- ✗ No test for the per-row dropdown menus
- ✗ Responsive testing absent or described as "verify on mobile" without specifying keyboard scrolling behavior
- ✗ Acceptance criteria that can't be measured ("the table should be navigable by keyboard")
- ✗ Prescribing headers attribute (`headers="..."`) on all TD cells — scope attribute is sufficient for single-level column headers and headers is only needed for complex multi-level tables; over-prescribing headers is a planning smell for a 7-column flat table
