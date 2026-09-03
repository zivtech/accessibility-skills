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

- The table lists maintenance cases, one row per case, with an **Actions** column added for editing.
- The **Case ID** column links to the case's detail page and is labelled with the case's identifier (e.g. "4471").
- The **Case Name** column links to the same detail page and is labelled with the case's human-readable name (e.g. "Ridgeway Pumping Station").
- The **Actions** column links to the same case's edit page (`/cases/{id}/edit`) on every row — the same function every time — but the link text differs row to row: "Edit", "Modify", "Change details".
- **Status** and **Last updated** are plain text, not interactive.

## Accessibility Issues (Planted)

1. **MAJOR: The same row action is labelled three different ways** — every row's Actions link points at the same per-record edit affordance (`/cases/{id}/edit`), but its accessible name changes row to row: "Edit" (row 1), "Modify" (row 2), "Change details" (row 3). This is a textbook SC 3.2.4 Consistent Identification failure: unlike the Case ID/Case Name pair in the same rows (which are two genuinely different functions sharing a destination — see the false-positive trap below), the Actions link is the *same* function — editing the record — recurring across rows, and 3.2.4 requires that a component with one repeated functionality be identified consistently. A user who learns that "Edit" opens the edit form for one case has no way to know that "Modify" and "Change details" do the same thing on the next two rows; a screen reader user tabbing through action links or browsing a forms/links list hears three unrelated-sounding labels instead of one predictable control.
   - Evidence: `row-action-inconsistent-labels.md:38` (`{c.actionLabel}` renders "Edit" / "Modify" / "Change details" across rows, all inside `<a href={`/cases/${c.id}/edit`}>` at the same line) — contrast with the Case ID link at line 30 and Case Name link at line 33, whose href is likewise per-row but whose *labels* are each correct because they are different functions, not the same one.
   - WCAG citation: 3.2.4 Consistent Identification (components with the same functionality must be identified consistently)
   - User group: Screen reader users; also cognitive/low-vision users who rely on recognizing a control by its label rather than re-reading the row each time
   - Expected: The edit link's accessible name should be the same string on every row (e.g. always "Edit"), optionally with a visually-hidden per-row suffix for disambiguation (e.g. "Edit, Ridgeway Pumping Station") that keeps the visible/base label consistent
   - Fix: Replace `{c.actionLabel}` with a fixed label, e.g. `<a href={`/cases/${c.id}/edit`}>Edit<span className="visually-hidden">, {c.name}</span></a>`, and remove `actionLabel` from the data

## Difficulty Level

**HAS-BUGS** — The fixture deliberately sits right next to the false-alarm shape it must not be confused with: the Case ID/Case Name links in every row already share a destination with different names, and that pairing is correct (same reasoning as the CLEAN sibling `paired-id-name-columns-clean`). The one planted defect is a *different* pair sharing a destination — where the two occurrences really are the same function — so a reviewer has to tell "same destination, different function" (fine, twice in this fixture) apart from "same destination, same function, different label" (the one real violation) rather than pattern-matching on "links to the same place" in either direction.
