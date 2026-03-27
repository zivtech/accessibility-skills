# Fixture: Data Table Missing Scope Attributes

## Component Code

```jsx
const SalesDataTable = () => {
  const data = [
    { product: 'Widget A', q1: 12500, q2: 13200, q3: 14100, q4: 15800 },
    { product: 'Widget B', q1: 8900, q2: 9200, q3: 9800, q4: 10200 },
    { product: 'Widget C', q1: 22300, q2: 24100, q3: 26000, q4: 28500 },
  ];

  return (
    <div className="table-container">
      <h2>Q1-Q4 Sales Data by Product</h2>
      {/* BUG: No caption or aria-label describing table */}
      <table className="data-table">
        <thead>
          <tr>
            {/* BUG: Column headers lack scope="col" */}
            <th>Product</th>
            <th>Q1</th>
            <th>Q2</th>
            <th>Q3</th>
            <th>Q4</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              {/* BUG: Row headers (Product column) lack scope="row" */}
              <th>{row.product}</th>
              <td>{row.q1.toLocaleString()}</td>
              <td>{row.q2.toLocaleString()}</td>
              <td>{row.q3.toLocaleString()}</td>
              <td>{row.q4.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default SalesDataTable;
```

## CSS

```css
.table-container {
  margin: 20px 0;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.table-container h2 {
  margin-top: 0;
  color: #333;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.data-table th,
.data-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: right;
}

.data-table th:first-child,
.data-table td:first-child {
  text-align: left;
}

.data-table thead {
  background-color: #f5f5f5;
  font-weight: bold;
}

.data-table tbody tr:nth-child(even) {
  background-color: #fafafa;
}

.data-table tbody tr:hover {
  background-color: #f0f0f0;
}
```

## Expected Behavior

- Table displays sales data with products in rows and quarters in columns
- Column headers (Q1, Q2, etc.) are clearly identified
- Product names are row headers
- Numbers are right-aligned (except product names)
- Table is visible and readable

## Accessibility Features Present

✓ Semantic table structure (<table>, <thead>, <tbody>, <th>, <td>)
✓ Column headers use <th> element
✓ Row headers use <th> element
✓ Heading above table (h2)

## Accessibility Issues (Planted)

1. **MAJOR: Column headers lack scope="col" attribute** — Per WCAG 2.2 criterion 1.3.1, table headers must identify whether they apply to columns or rows. Without scope, screen reader doesn't know if "Q1" is a column header or row header.
   - Evidence: `data-table-missing-scope.md:12-17` (th elements without scope="col")
   - WCAG citation: 1.3.1 Info and Relationships (table header scope must be identified)
   - User group: Screen reader users
   - Expected: Column headers should have scope="col"
   - Fix: Add scope="col" to all column headers in <thead>

2. **MAJOR: Row headers lack scope="row" attribute** — The Product column serves as row headers but lacks scope="row", making the relationship unclear to screen readers.
   - Evidence: `data-table-missing-scope.md:24` (row <th> elements without scope="row")
   - WCAG citation: 1.3.1 Info and Relationships
   - User group: Screen reader users
   - Expected: Product headers in rows should have scope="row"
   - Fix: Add scope="row" to product name <th> elements

3. **MINOR: Table lacks caption or aria-label** — While the heading above the table describes it, the table itself has no <caption> or aria-label. Makes it less clear to screen reader what table is for when encountered in context.
   - Evidence: `data-table-missing-scope.md:10` (table element has no caption or aria-label)
   - WCAG citation: 1.3.1 Info and Relationships (complex tables should have descriptions)
   - User group: Screen reader users
   - Expected: Table should have <caption> or aria-label describing its purpose
   - Fix: Add <caption>Sales Data by Product and Quarter</caption> or aria-label

## Difficulty Level

**HAS-BUGS** — Clear table structure issues. The table is semantically correct (uses <table>, <thead>, <tbody>, proper <th> and <td> elements), but the semantic relationships (scope attributes) are missing. This is a common mistake: developers create proper table structure but forget scope attributes.

## Frameworks & Environment

React, standard HTML/CSS

## Notes

This fixture tests whether a11y-critic can distinguish between:
1. **Proper semantic elements** (using <th>, not divs) ✓
2. **Complete semantic relationships** (scope attributes) ✗

Screen reader users cannot determine table structure without scope attributes. Pressing "table navigation" keys (like in NVDA) doesn't work properly without scope.

Expected baseline: Might miss this if it only checks "is it a <table>? Yes". A11y-critic should specifically audit scope attributes.
