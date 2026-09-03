# Fixture: Cases Table with ID and Name Columns

## Component Code

```jsx
const MaintenanceCasesTable = () => {
  const cases = [
    { id: 4471, name: 'Ridgeway Pumping Station', status: 'Open', lastUpdated: 'Aug 14, 2026' },
    { id: 4488, name: 'Northgate Reservoir', status: 'Closed', lastUpdated: 'Jul 30, 2026' },
    { id: 4502, name: 'Elm Street Lift Station', status: 'In Progress', lastUpdated: 'Aug 21, 2026' },
  ];

  return (
    <div className="cases-table-container">
      <table className="cases-table">
        <caption>Open and recently closed maintenance cases</caption>
        <thead>
          <tr>
            <th scope="col">Case ID</th>
            <th scope="col">Case Name</th>
            <th scope="col">Status</th>
            <th scope="col">Last updated</th>
          </tr>
        </thead>
        <tbody>
          {cases.map((c) => (
            <tr key={c.id}>
              <th scope="row">
                <a href={`/cases/${c.id}`}>{c.id}</a>
              </th>
              <td>
                <a href={`/cases/${c.id}`}>{c.name}</a>
              </td>
              <td>{c.status}</td>
              <td>{c.lastUpdated}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default MaintenanceCasesTable;
```

## CSS

```css
.cases-table-container {
  margin: 20px 0;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.cases-table {
  width: 100%;
  border-collapse: collapse;
}

.cases-table caption {
  text-align: left;
  font-weight: 600;
  margin-bottom: 12px;
  color: #333;
}

.cases-table th,
.cases-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

.cases-table thead {
  background-color: #f5f5f5;
  font-weight: bold;
}

.cases-table tbody tr:nth-child(even) {
  background-color: #fafafa;
}

.cases-table tbody tr:hover {
  background-color: #f0f0f0;
}

.cases-table a {
  color: #0b5fff;
  text-decoration: underline;
}

.cases-table a:focus-visible {
  outline: 3px solid #0b5fff;
  outline-offset: 2px;
}
```

## Expected Behavior

- The table lists maintenance cases, one row per case.
- The **Case ID** column links to the case's detail page and is labelled with the case's identifier (e.g. "4471").
- The **Case Name** column links to the same detail page and is labelled with the case's human-readable name (e.g. "Ridgeway Pumping Station").
- **Status** and **Last updated** are plain text, not interactive.
- A user scanning the list by case number uses the ID link; a user scanning by site name uses the Name link — both land on the same case.

## Accessibility Features Present

1. **Proper table semantics** — a real `<table>` with a `<caption>`, `<thead>`/`<tbody>`, `scope="col"` on every column header, and `scope="row"` on the Case ID header cell in each row. A screen reader in table-navigation mode announces the column header and the row header together with every cell.
2. **Two links to the same destination are not a Consistent Identification failure** — the Case ID link and the Case Name link in a row both resolve to `/cases/4471`, but they do not share a function. The ID link is the record's identifier; the Name link is its human-readable label. WCAG's Understanding page for SC 3.2.4 Consistent Identification scopes the criterion to "components that have the same functionality" — an id-lookup affordance and a name-lookup affordance are different functionalities that happen to resolve to the same page, the way a search result's title and its "View" button both open the same document without being the same control.
3. **The Case ID link's accessible name is short but not ambiguous** — its accessible name is just "4471", but SC 2.4.4 Link Purpose (In Context) is satisfied by context: the link sits in a cell under the "Case ID" column header, and table-navigation mode reads the header and the cell together, so a screen reader user hears the header and the number as one unit, never a bare, unexplained digit string.
4. **Focus is visible** — `.cases-table a:focus-visible` gives every link, including both links in a row, a visible outline on keyboard focus.
5. **Two links per row are two intents, not duplication** — the ID link serves a user scanning by case number; the Name link serves a user scanning by site name. Neither is redundant with the other, so collapsing them into a single link would remove a legitimate way of finding the row.
