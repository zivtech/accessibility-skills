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
  /* #f0f0f0 puts the link colour at 4.4995:1 against this background — under
     the 4.5:1 floor by a rounding artifact that every checker reports as a
     pass. Lightened so the margin is real rather than nominal. */
  background-color: #f5f5f5;
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
2. **Two links to the same destination are not a Consistent Identification failure** — and the load-bearing reason is scope, not functionality. SC 3.2.4 applies to "components that have the same functionality **within a set of Web pages**", and its failure technique F31 is about the same function carrying different labels *across* pages. Two links inside one row of one page are outside the criterion's scope entirely, which is an argument a skeptic cannot dispute. The secondary reading — that an id-lookup affordance and a name-lookup affordance are different functionalities that happen to resolve to the same page — is defensible but contestable, since both can fairly be described as "open case 4471". Do not rest the verdict on it.
3. **The Case ID link's accessible name is short but satisfies the AA criterion** — its accessible name is just "4471". SC 2.4.4 Link Purpose (In Context) is met on normative grounds rather than behavioural ones: the SC's own definition of *programmatically determined link context* explicitly admits "a table header cell for a cell that contains the link", and the header association here is real (`scope="col"` plus `scope="row"`). Stated precisely, because the weaker version of this claim is wrong: a user reading in table-navigation mode or linearly does hear the header with the number, but a links list (NVDA Elements List, VoiceOver rotor) strips table context and presents "4471" alone. That gap is exactly what SC 2.4.9 Link Purpose (Link Only) covers, and 2.4.9 is AAA. This fixture targets AA, where the criterion is satisfied.
4. **Focus is visible** — `.cases-table a:focus-visible` gives every link, including both links in a row, a visible outline on keyboard focus.
5. **Two links per row are two intents, not duplication** — the ID link serves a user scanning by case number; the Name link serves a user scanning by site name. Neither is redundant with the other, so collapsing them into a single link would remove a legitimate way of finding the row.
