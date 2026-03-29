# Fixture: Data Table With Sortable Columns and Broken ARIA Sort

## Component Code

```jsx
import React, { useState } from 'react';

const RAW_DATA = [
  { id: 1, name: 'Alice Nguyen',    dept: 'Engineering', salary: 112000, start: '2019-03-12' },
  { id: 2, name: 'Bob Okafor',      dept: 'Design',      salary: 94000,  start: '2021-07-01' },
  { id: 3, name: 'Carmen Reyes',    dept: 'Engineering', salary: 125000, start: '2017-11-08' },
  { id: 4, name: 'David Kim',       dept: 'Marketing',   salary: 88000,  start: '2022-02-14' },
  { id: 5, name: 'Elena Petrova',   dept: 'Design',      salary: 99000,  start: '2020-09-30' },
  { id: 6, name: 'Felix Andrade',   dept: 'Engineering', salary: 117000, start: '2018-06-20' },
  { id: 7, name: 'Grace Liu',       dept: 'Marketing',   salary: 91000,  start: '2023-01-05' },
  { id: 8, name: 'Hank Morrison',   dept: 'Design',      salary: 103000, start: '2019-12-17' },
  { id: 9, name: 'Isla Fernandez',  dept: 'Engineering', salary: 134000, start: '2016-04-22' },
  { id: 10, name: 'James Obi',      dept: 'Marketing',   salary: 86000,  start: '2022-08-09' },
  { id: 11, name: 'Kira Walsh',     dept: 'Engineering', salary: 108000, start: '2020-05-15' },
  { id: 12, name: 'Leo Tran',       dept: 'Design',      salary: 97000,  start: '2021-03-28' },
];

const PAGE_SIZE = 5;

const COLUMNS = [
  { key: 'name',   label: 'Name' },
  { key: 'dept',   label: 'Department' },
  { key: 'salary', label: 'Salary' },
  { key: 'start',  label: 'Start Date' },
];

const SortableTable = () => {
  const [sortKey, setSortKey]   = useState('name');
  const [sortDir, setSortDir]   = useState('asc');
  const [page, setPage]         = useState(0);

  const sorted = [...RAW_DATA].sort((a, b) => {
    const av = a[sortKey];
    const bv = b[sortKey];
    if (av < bv) return sortDir === 'asc' ? -1 : 1;
    if (av > bv) return sortDir === 'asc' ? 1 : -1;
    return 0;
  });

  const totalPages = Math.ceil(sorted.length / PAGE_SIZE);
  const pageData = sorted.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE);

  const handleSort = (key) => {
    if (key === sortKey) {
      setSortDir(d => d === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortDir('asc');
    }
    setPage(0);
  };

  const formatSalary = (n) => `$${n.toLocaleString()}`;

  return (
    <div className="table-wrapper">

      {/*
        BUG: Entire table built with CSS grid divs — no semantic <table>, <thead>,
        <tbody>, <th>, <tr>, or <td> elements.
        WCAG 1.3.1: tabular structure not programmatically determinable.
        No scope on headers because there are no real <th> elements.
      */}
      <div className="data-table" role="region" aria-label="Employee directory">

        {/* Header row */}
        <div className="table-row table-header-row">
          {COLUMNS.map(col => (
            /*
              BUG: No aria-sort on sort buttons — SR users cannot tell which
              column is sorted or in which direction.
              The button is keyboard-activatable (correct), but sort state is
              communicated visually only via the arrow icon CSS class.
              WCAG 4.1.2: sort state not programmatically exposed.
            */
            <div key={col.key} className="table-cell table-header-cell">
              <button
                className={`sort-btn ${sortKey === col.key ? `sort-${sortDir}` : ''}`}
                onClick={() => handleSort(col.key)}
              >
                {col.label}
                <span className="sort-icon" aria-hidden="true">
                  {sortKey === col.key ? (sortDir === 'asc' ? ' ▲' : ' ▼') : ' ⇅'}
                </span>
              </button>
            </div>
          ))}
        </div>

        {/* Data rows */}
        {pageData.map(row => (
          <div key={row.id} className="table-row">
            <div className="table-cell">{row.name}</div>
            <div className="table-cell">{row.dept}</div>
            <div className="table-cell">{formatSalary(row.salary)}</div>
            <div className="table-cell">{row.start}</div>
          </div>
        ))}

      </div>

      {/*
        Works: "Showing X-Y of Z" text is visible.
        BUG: No aria-live on this region — when sort or page changes, SR
        users don't know the count has updated.
      */}
      <div className="table-meta">
        Showing {page * PAGE_SIZE + 1}–{Math.min((page + 1) * PAGE_SIZE, sorted.length)} of {sorted.length} employees
      </div>

      {/* Pagination */}
      <nav className="pagination" aria-label="Table pagination">
        {/*
          BUG: Pagination uses href="#" plain anchor links.
          No page context announced — SR users don't know "Page 2 of 3".
          Current page link has no aria-current="page".
          href="#" causes scroll-to-top behavior and announces no destination.
        */}
        {Array.from({ length: totalPages }, (_, i) => (
          <a
            key={i}
            href="#"
            className={`page-link ${i === page ? 'current' : ''}`}
            onClick={(e) => { e.preventDefault(); setPage(i); }}
          >
            {i + 1}
          </a>
        ))}
      </nav>

    </div>
  );
};

export default SortableTable;
```

## CSS

```css
.table-wrapper {
  max-width: 760px;
  margin: 32px auto;
  font-family: system-ui, sans-serif;
}

/* BUG: Grid layout mimics table visually but carries no semantic table structure */
.data-table {
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  overflow: hidden;
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 1.5fr 1fr 1fr;
  border-bottom: 1px solid #e0e0e0;
}

.table-row:last-child {
  border-bottom: none;
}

.table-header-row {
  background: #f5f5f5;
}

.table-cell {
  padding: 12px 16px;
  font-size: 14px;
  color: #1a1a1a;
  align-self: center;
}

.table-header-cell {
  padding: 0;
}

/* Works: sort buttons are keyboard-activatable, have visible focus */
.sort-btn {
  width: 100%;
  padding: 12px 16px;
  background: none;
  border: none;
  text-align: left;
  font-size: 14px;
  font-weight: 700;
  color: #1a1a1a;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.sort-btn:focus {
  outline: 3px solid #1565c0;
  outline-offset: -3px;
}

.sort-btn:hover {
  background: #eeeeee;
}

/* BUG: Sort direction communicated via color + icon — not by aria-sort */
.sort-btn.sort-asc  { color: #1565c0; }
.sort-btn.sort-desc { color: #6a1b9a; }

.sort-icon {
  font-size: 12px;
  opacity: 0.7;
}

.table-meta {
  margin-top: 12px;
  font-size: 13px;
  color: #616161;
}

.pagination {
  display: flex;
  gap: 8px;
  margin-top: 16px;
  align-items: center;
}

/* BUG: Current page communicated by color only — no aria-current */
.page-link {
  display: inline-block;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  text-decoration: none;
  font-size: 14px;
  color: #1565c0;
}

.page-link:focus {
  outline: 3px solid #1565c0;
  outline-offset: 2px;
}

.page-link.current {
  background: #1565c0;
  color: #fff;
  border-color: #1565c0;
  font-weight: 700;
}

.page-link:hover:not(.current) {
  background: #e3f2fd;
}
```

## Expected Behavior

- Table displays 5 rows per page with pagination controls
- Clicking a column header sorts the table by that column (asc/desc toggle)
- Sort direction indicated both visually and programmatically
- Screen reader announces sort state when column header is focused or activated
- Pagination announces current page and total pages
- Table structure is navigable by row and column in screen reader table mode

## Accessibility Features Present

- Sort buttons are real `<button>` elements — keyboard-activatable with Enter/Space
- Sort buttons have visible focus indicators (`:focus` outline)
- Sort icon uses `aria-hidden="true"` — correct (decorative)
- Pagination wrapped in `<nav>` with `aria-label="Table pagination"` — correct landmark
- `role="region"` with `aria-label` on the table wrapper — provides landmark
- Visual sort direction indicators (▲ ▼ ⇅) are present
- "Showing X–Y of Z" count is visible

## Accessibility Issues (Planted)

1. **CRITICAL: No `aria-sort` on sort column headers** — Sort state (ascending/descending/none) is conveyed only through CSS color changes and arrow icons. Screen reader users have no programmatic indication of which column is sorted or its direction.
   - Evidence: Sort button `<button className={...}>` — no `aria-sort` attribute; state encoded only in CSS class `sort-asc`/`sort-desc`
   - WCAG: 4.1.2 Name, Role, Value
   - User group: Screen reader users
   - Fix: Add `aria-sort={sortKey === col.key ? (sortDir === 'asc' ? 'ascending' : 'descending') : 'none'}` to each sort button (or to the header cell if using semantic `<th>`)

2. **MAJOR: `div` + CSS grid instead of semantic `<table>` structure** — No `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, or `<td>` elements. Screen reader table navigation (read by row, read by column, announce header context) is unavailable.
   - Evidence: `.data-table` is a `<div>`; rows are `<div className="table-row">`; cells are `<div className="table-cell">` — no semantic table markup
   - WCAG: 1.3.1 Info and Relationships
   - User group: Screen reader users
   - Fix: Replace div grid with `<table>`, `<thead>/<tbody>`, `<tr>`, `<th scope="col">`, `<td>` elements; apply grid styles to `<table>` or use `display: contents` on `<tr>`

3. **MAJOR: Pagination uses `href="#"` links with no page context** — Pagination links are plain anchors with no `aria-current="page"` on the active page and no `aria-label` distinguishing "page 1" from "page 2". Screen readers announce them as generic links.
   - Evidence: `<a href="#" className={...}>` — no `aria-current`, no `aria-label="Page N"`, no "of N pages" context
   - WCAG: 4.1.2 Name, Role, Value; 2.4.6 Headings and Labels
   - User group: Screen reader users, keyboard users
   - Fix: Use `<button>` elements for pagination (no href="#"); add `aria-current="page"` to active page; add `aria-label={`Page ${i + 1} of ${totalPages}`}` to each button

4. **MINOR: "Showing X–Y of Z" count has no `aria-live` region** — When sort or page changes, the visible count updates but screen reader users are not notified. An `aria-live="polite"` region would announce the update automatically.
   - Evidence: `.table-meta` div has no `aria-live`, `role="status"`, or `aria-atomic`
   - WCAG: 4.1.3 Status Messages
   - User group: Screen reader users
   - Fix: Add `aria-live="polite" aria-atomic="true"` to the `.table-meta` div

5. **MINOR: No `scope` attribute on headers** — There are no real `<th>` elements, so `scope` is impossible. This compounds the WCAG 1.3.1 failure but is a separate symptom.
   - Evidence: Absence of `<th scope="col">` — structural consequence of div-based table
   - WCAG: 1.3.1 Info and Relationships
   - User group: Screen reader users
   - Fix: Addressed by converting to semantic `<table>` and adding `scope="col"` to `<th>` elements

## What Should NOT Be Flagged

- Sort buttons are real `<button>` elements — keyboard-activatable with Enter/Space — do not flag as inaccessible to keyboard
- Sort icon has `aria-hidden="true"` — correct usage, do not flag
- Pagination `<nav>` has `aria-label` — correct landmark, do not flag
- Focus indicators on sort buttons and pagination links are visible — do not flag
- `role="region"` + `aria-label` on the table wrapper is a valid landmark pattern — do not flag

## Difficulty Level

**HAS-BUGS** — The table has working keyboard interaction (sort buttons are real buttons, pagination links are focusable), visible focus styles, and landmark structure, but fails on the programmatic semantics that screen reader users depend on: `aria-sort`, semantic table structure, and pagination state. This is a regression detection fixture primarily targeting the Screen Reader dimension with secondary signal in Keyboard.
