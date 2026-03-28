# Fixture: Project Dashboard With Color-Only Status Indicators

## Component Code

```jsx
import React, { useState } from 'react';

const tasks = [
  { id: 1, name: 'API integration', owner: 'JL', due: 'Mar 31', effort: 'L', priority: 'P1', status: 'blocked',     progress: 20, desc: 'Integrate payment gateway API. Blocked on vendor credentials from procurement.' },
  { id: 2, name: 'Auth flow refactor', owner: 'MK', due: 'Apr 3',  effort: 'M', priority: 'P1', status: 'at-risk',   progress: 55, desc: 'Refactor OAuth2 login flow. At risk due to dependency on legacy session module.' },
  { id: 3, name: 'Dashboard UI', owner: 'SP', due: 'Apr 7',  effort: 'M', priority: 'P2', status: 'on-track',  progress: 70, desc: 'Build project dashboard views. On track per latest sprint review.' },
  { id: 4, name: 'Export to CSV', owner: 'JL', due: 'Apr 10', effort: 'S', priority: 'P3', status: 'on-track',  progress: 40, desc: 'Add CSV export for report views. On track, no blockers.' },
  { id: 5, name: 'Email notifications', owner: 'RP', due: 'Apr 14', effort: 'M', priority: 'P2', status: 'not-started', progress: 0,  desc: 'Configure transactional email via SendGrid. Not yet started, queued for next sprint.' },
  { id: 6, name: 'Perf audit', owner: 'MK', due: 'Apr 14', effort: 'S', priority: 'P3', status: 'not-started', progress: 0,  desc: 'Run Lighthouse audit and address P1 findings. Not yet started.' },
  { id: 7, name: 'Accessibility pass', owner: 'SP', due: 'Apr 21', effort: 'L', priority: 'P1', status: 'not-started', progress: 0,  desc: 'Full WCAG 2.1 AA review and remediation across all views.' },
  { id: 8, name: 'Load testing', owner: 'RP', due: 'Apr 28', effort: 'M', priority: 'P2', status: 'on-track',  progress: 10, desc: 'k6 load test suite for API endpoints. Early stages, on track.' },
];

// BUG: Status is communicated solely by dot color — no text, icon, or pattern supplement
// Each dot color passes contrast against white (4.5:1+), so automated tools will not flag this.
// But color is the ONLY differentiator between four distinct states — WCAG 1.4.1 violation.
const STATUS_COLORS = {
  'blocked':     '#d32f2f',  // red   — 5.1:1 contrast against white — passes automated check
  'at-risk':     '#f57c00',  // amber — 4.6:1 contrast against white — passes automated check
  'on-track':    '#2e7d32',  // green — 5.9:1 contrast against white — passes automated check
  'not-started': '#1565c0',  // blue  — 5.4:1 contrast against white — passes automated check
};

const SORT_COLS = ['name', 'owner', 'due', 'effort', 'priority', 'status', 'progress'];

const ProjectDashboard = () => {
  const [sortCol, setSortCol] = useState('priority');
  const [sortDir, setSortDir] = useState('asc');
  // BUG: selectedRow uses only a background color shift to indicate selection — no other indicator
  const [selectedRow, setSelectedRow] = useState(null);

  const handleSort = (col) => {
    if (sortCol === col) {
      setSortDir(d => d === 'asc' ? 'desc' : 'asc');
    } else {
      setSortCol(col);
      setSortDir('asc');
    }
  };

  const sorted = [...tasks].sort((a, b) => {
    const av = a[sortCol] ?? '';
    const bv = b[sortCol] ?? '';
    const cmp = String(av).localeCompare(String(bv), undefined, { numeric: true });
    return sortDir === 'asc' ? cmp : -cmp;
  });

  return (
    <div className="dashboard">
      {/* Good: heading structure — h1 present, correct hierarchy */}
      <h1 className="dashboard-title">Project Dashboard</h1>

      {/* Good: landmark region */}
      <section aria-label="Task overview">
        {/* BUG: Dense layout — 8 columns, small text (11px in cells), abbreviations (L/M/S, P1/P2/P3)
            with no expansion. WCAG 3.1.4 (Abbreviations, AAA) — flagged as ENHANCEMENT by
            Cognitive perspective even though it is technically AAA. */}
        <table className="task-table">
          <thead>
            <tr>
              {SORT_COLS.map(col => (
                <th key={col} scope="col">
                  {/* BUG: Sort button uses a tiny 10x10px arrow icon with no accessible label
                      describing sort direction or target column — WCAG 2.5.8 (target size 24x24px min)
                      The arrow icon provides no context to keyboard or screen reader users either. */}
                  <button
                    className="sort-btn"
                    onClick={() => handleSort(col)}
                    tabIndex={0}
                  >
                    {col.charAt(0).toUpperCase() + col.slice(1)}
                    {/* BUG: 10x10px icon only, no accessible label for sort state */}
                    <span className="sort-icon" aria-hidden="true">
                      {sortCol === col ? (sortDir === 'asc' ? '▲' : '▼') : '⇅'}
                    </span>
                  </button>
                </th>
              ))}
              <th scope="col">Description</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map(task => (
              // BUG: selected state communicated only by background-color change (light blue tint)
              // No aria-selected, no border, no checkmark, no text change — WCAG 1.4.1
              <tr
                key={task.id}
                className={`task-row ${selectedRow === task.id ? 'selected' : ''}`}
                onClick={() => setSelectedRow(task.id)}
                tabIndex={0}
                onKeyDown={e => e.key === 'Enter' && setSelectedRow(task.id)}
              >
                <td className="cell-name">{task.name}</td>
                <td className="cell-owner">{task.owner}</td>
                <td className="cell-due">{task.due}</td>
                {/* BUG: Abbreviation "L/M/S" with no expansion — WCAG 3.1.4 */}
                <td className="cell-effort">{task.effort}</td>
                {/* BUG: Abbreviation "P1/P2/P3" with no expansion — WCAG 3.1.4 */}
                <td className="cell-priority">{task.priority}</td>
                <td className="cell-status">
                  {/* BUG: Colored dot only — no text label, no aria-label, no pattern/icon supplement
                      Screen reader will announce nothing meaningful here.
                      Color-blind users (8% of males) cannot distinguish red/green dots.
                      WCAG 1.4.1: information conveyed by color alone. */}
                  <span
                    className="status-dot"
                    style={{ backgroundColor: STATUS_COLORS[task.status] }}
                  />
                </td>
                <td className="cell-progress">
                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{ width: `${task.progress}%` }}
                    />
                  </div>
                  <span className="progress-label">{task.progress}%</span>
                </td>
                <td className="cell-desc">
                  {/* BUG: Full description only visible on hover via CSS tooltip — no focus equivalent
                      Keyboard-only users and touch users cannot access this content.
                      WCAG 1.4.13 (Content on Hover or Focus), 2.1.1 (Keyboard) */}
                  <span className="desc-trigger" data-tooltip={task.desc}>
                    {task.desc.slice(0, 30)}…
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      {/* Good: summary stats with visible text labels */}
      <section className="summary-bar" aria-label="Status summary">
        <div className="summary-item">
          <span className="summary-count">{tasks.filter(t => t.status === 'blocked').length}</span>
          {/* BUG: Summary also uses color-only dots — no text label on the indicator itself */}
          <span className="status-dot" style={{ backgroundColor: STATUS_COLORS['blocked'] }} />
        </div>
        <div className="summary-item">
          <span className="summary-count">{tasks.filter(t => t.status === 'at-risk').length}</span>
          <span className="status-dot" style={{ backgroundColor: STATUS_COLORS['at-risk'] }} />
        </div>
        <div className="summary-item">
          <span className="summary-count">{tasks.filter(t => t.status === 'on-track').length}</span>
          <span className="status-dot" style={{ backgroundColor: STATUS_COLORS['on-track'] }} />
        </div>
        <div className="summary-item">
          <span className="summary-count">{tasks.filter(t => t.status === 'not-started').length}</span>
          <span className="status-dot" style={{ backgroundColor: STATUS_COLORS['not-started'] }} />
        </div>
      </section>
    </div>
  );
};

export default ProjectDashboard;
```

```css
.dashboard {
  font-family: system-ui, sans-serif;
  padding: 24px;
  background: #ffffff;
}

.dashboard-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 16px;
}

.task-table {
  width: 100%;
  border-collapse: collapse;
  /* BUG: font-size on data cells is 11px — below comfortable reading threshold for low-vision users */
  font-size: 11px;
}

.task-table th {
  text-align: left;
  padding: 6px 8px;
  border-bottom: 2px solid #e0e0e0;
  white-space: nowrap;
}

.task-table td {
  padding: 5px 8px;
  border-bottom: 1px solid #f0f0f0;
  vertical-align: middle;
}

/* BUG: sort-btn has a 10x10px icon — total interactive area is under 24x24px — WCAG 2.5.8 */
.sort-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-weight: 600;
  padding: 0;
  display: inline-flex;
  align-items: center;
  gap: 2px;
}

.sort-btn:focus-visible {
  /* Good: focus indicator is present on sort buttons */
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

/* BUG: sort icon is 10x10px — no padding to expand the touch/click target */
.sort-icon {
  font-size: 10px;
  display: inline-block;
  width: 10px;
  height: 10px;
  line-height: 10px;
}

/* Good: table rows are keyboard focusable */
.task-row:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: -2px;
}

/* BUG: selected state uses only a background tint — no border, checkmark, or other non-color indicator */
.task-row.selected {
  background-color: #e3f2fd;  /* light blue — color is the ONLY selection indicator */
}

/* BUG: status-dot carries meaning through color alone — no shape/pattern/text supplement */
.status-dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.progress-bar {
  display: inline-block;
  width: 60px;
  height: 6px;
  background: #e0e0e0;
  border-radius: 3px;
  vertical-align: middle;
}

.progress-fill {
  height: 100%;
  background: #1565c0;
  border-radius: 3px;
}

.progress-label {
  margin-left: 4px;
  font-size: 10px;
}

.cell-desc {
  max-width: 160px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* BUG: Tooltip appears only on CSS :hover — no :focus equivalent — WCAG 1.4.13, 2.1.1 */
.desc-trigger {
  position: relative;
  cursor: default;
}

.desc-trigger::after {
  content: attr(data-tooltip);
  position: absolute;
  bottom: 100%;
  left: 0;
  background: #333;
  color: #fff;
  padding: 6px 10px;
  border-radius: 4px;
  font-size: 12px;
  white-space: normal;
  width: 220px;
  z-index: 100;
  display: none;
}

/* BUG: only :hover triggers tooltip — keyboard focus does not */
.desc-trigger:hover::after {
  display: block;
}

.summary-bar {
  display: flex;
  gap: 24px;
  margin-top: 16px;
  padding: 12px 0;
  border-top: 1px solid #e0e0e0;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
}
```

## Expected Behavior

- Project dashboard table showing 8 tasks across 8 columns
- Rows are sortable by clicking column headers
- Clicking a row selects it, highlighting it
- Status for each task is shown as a colored dot (red, amber, green, blue)
- Full task descriptions are visible on hover over the truncated text
- A summary bar at the bottom shows counts per status category

## Accessibility Features Present

- Good heading structure (`h1` present, correct semantic level)
- Table uses `<table>`, `<thead>`, `<tbody>`, `scope="col"` on headers
- Landmark region with `aria-label` wrapping the table
- Summary bar has `aria-label`
- All table rows have `tabIndex={0}` and `onKeyDown` for keyboard interaction
- Sort buttons have `:focus-visible` outline styles
- Progress values are shown as visible text percentages alongside the bar
- Color contrast on all dot colors meets WCAG AA against white background (each >= 4.5:1)

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Status communicated by color alone — WCAG 1.4.1 (Use of Color)**
   Four distinct task states (blocked, at-risk, on-track, not-started) are represented solely by dot color. No text label, icon shape, pattern, or other non-color indicator distinguishes the states. The `<span>` has no `aria-label` and renders nothing a screen reader can read. Users with color vision deficiency (affects ~8% of males) cannot distinguish red from green dots. Users on monochrome displays, printed output, or high-contrast mode lose all status information. Note: each dot color passes automated contrast checks (4.5:1+), so axe-core and similar tools will not flag this — the violation is color-as-sole-differentiator, not contrast ratio.
   - Evidence: `color-only-status-indicators.md:77-82` — `<span class="status-dot">` with background color and no text or aria-label
   - User group: Color-blind users, monochrome display users, screen reader users
   - Expected fix: Add visible text label (e.g., "Blocked") or `aria-label` on each dot, plus a non-color shape/icon supplement (e.g., filled circle = on-track, X = blocked, triangle = at-risk)

2. **MAJOR: Hover-only tooltips with no keyboard or focus equivalent — WCAG 1.4.13 (Content on Hover or Focus), 2.1.1 (Keyboard)**
   Full task descriptions are truncated to 30 characters in the table cell and the complete text is only revealed via a CSS `:hover` pseudo-class on `.desc-trigger::after`. No `:focus` rule exists. Keyboard-only users, switch access users, and touch users cannot access the full description. The tooltip content is load-bearing (it is the only place the full description exists).
   - Evidence: `color-only-status-indicators.md:CSS:tooltip section` — `.desc-trigger:hover::after { display: block }` with no `:focus` equivalent
   - User group: Keyboard-only users, switch access users, touch users
   - Expected fix: Add `.desc-trigger:focus::after { display: block }` at minimum; preferred fix is a `<button>` that opens a proper popover with `role="tooltip"` and keyboard dismiss

3. **MAJOR: Sort icon target size below minimum — WCAG 2.5.8 (Target Size, Minimum)**
   The sort icon (`.sort-icon`) renders at 10x10px with zero padding. WCAG 2.5.8 requires a minimum target size of 24x24px for interactive controls, or sufficient spacing from other targets if smaller. The entire sort button is constrained to its text width plus the 10x10 icon, making it difficult to activate precisely, especially for users with motor impairments, tremor, or those using touch.
   - Evidence: `color-only-status-indicators.md:CSS:sort-icon` — `width: 10px; height: 10px; line-height: 10px` with `padding: 0`
   - User group: Motor impairment users, tremor users, touch users
   - Expected fix: Set `.sort-btn { padding: 8px; min-height: 44px; }` to bring the entire button to a comfortable activation area

4. **MAJOR: Dense layout with unexpanded abbreviations — Cognitive accessibility, WCAG 3.1.4 (Abbreviations, AAA)**
   The table uses abbreviations throughout: effort is shown as `L`, `M`, `S` (no expansion for Large, Medium, Small); priority is shown as `P1`, `P2`, `P3` (no expansion). These are never defined anywhere on the page. For users new to the system, users with cognitive disabilities, or users relying on screen readers, these abbreviations carry no inherent meaning. While WCAG 3.1.4 is Level AAA, the Cognitive & Neurodivergent perspective flags unexpanded abbreviations as ENHANCEMENT for any data-dense interface.
   - Evidence: `color-only-status-indicators.md:68-72` — raw `{task.effort}` and `{task.priority}` rendered without `<abbr>` or tooltip expansion
   - User group: Cognitive disability users, users unfamiliar with the system, screen reader users
   - Expected fix: Use `<abbr title="Large">L</abbr>` / `<abbr title="Small">S</abbr>`, or add a legend below the table defining all abbreviations

5. **MINOR: Row selection communicated by background color shift only — WCAG 1.4.1 (Use of Color)**
   When a row is selected, `.task-row.selected` applies `background-color: #e3f2fd` (a light blue tint). No other indicator is present: no border, no checkmark, no `aria-selected` attribute, no text change. In high-contrast mode or for users with color vision deficiency, the selection state is invisible.
   - Evidence: `color-only-status-indicators.md:CSS:task-row.selected` — background tint is the sole indicator
   - User group: Color-blind users, high-contrast mode users, screen reader users
   - Expected fix: Add `aria-selected="true"` to the selected row and a left border or icon indicator (e.g., `border-left: 3px solid #005fcc`) that is not color-dependent

6. **MINOR: No option to reduce information density**
   The dashboard presents 8 columns at 11px font size with no mechanism to hide columns, increase text size, or switch to a simplified view. For users with cognitive disabilities, attention disorders, or low vision who use zoom but need layout adaptation, the fixed-density layout offers no accommodation.
   - Evidence: `color-only-status-indicators.md:35-38` — table hardcodes all 8 columns; no column visibility toggle or density control
   - User group: Cognitive disability users, ADHD users, low-vision users
   - Expected fix: Add a column visibility toggle or a "simplified view" option that shows only name, status (as text), and due date

## Difficulty Level

**ADVERSARIAL** — This component is designed to defeat surface-level review. Automated tools (axe-core, Lighthouse) will report zero errors: all dot colors pass contrast ratio checks, the table has correct semantics, keyboard navigation functions, and focus indicators are present. A reviewer applying only keyboard/ARIA patterns will find nothing critical. The primary failure mode (color-as-sole-status-differentiator) requires understanding that passing contrast ratio does not satisfy WCAG 1.4.1 — these are distinct requirements. The secondary failure mode (cognitive density, abbreviations) requires reasoning from the Cognitive & Neurodivergent perspective to surface what automated scanning cannot detect.

## Frameworks

React 18+, CSS (no CSS-in-JS), HTML5 table element
