# Fixture: Row Action Link Labelled Differently on Every Row

## Component Code

```jsx
const MaintenanceCasesTable = () => {
  const cases = [
    { id: 4471, name: 'Ridgeway Pumping Station', status: 'Open', lastUpdated: 'Aug 14, 2026', actionLabel: 'Edit' },
    { id: 4488, name: 'Northgate Reservoir', status: 'Closed', lastUpdated: 'Jul 30, 2026', actionLabel: 'Modify' },
    { id: 4502, name: 'Elm Street Lift Station', status: 'In Progress', lastUpdated: 'Aug 21, 2026', actionLabel: 'Change details' },
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
            <th scope="col">Actions</th>
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
              <td>
                <a href={`/cases/${c.id}/edit`}>{c.actionLabel}</a>
              </td>
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
  background-color: #f5f5f5;  /* #f0f0f0 puts the link colour at 4.4998:1, under the 4.5 floor */
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

- The table lists maintenance cases, one row per case, with an **Actions** column added for editing.
- The **Case ID** column links to the case's detail page and is labelled with the case's identifier (e.g. "4471").
- The **Case Name** column links to the same detail page and is labelled with the case's human-readable name (e.g. "Ridgeway Pumping Station").
- The **Actions** column links to the same case's edit page (`/cases/{id}/edit`) on every row — the same function every time — but the link text differs row to row: "Edit", "Modify", "Change details".
- **Status** and **Last updated** are plain text, not interactive.
