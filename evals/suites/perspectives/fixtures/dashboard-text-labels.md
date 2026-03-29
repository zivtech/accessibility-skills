# Fixture: Analytics Dashboard With Text Status Labels (CLEAN)

## Component Code

```jsx
import React from 'react';

const stats = [
  { label: 'Active Users', value: '12,847', change: '+8.2%', status: 'up' },
  { label: 'Revenue', value: '$142.3K', change: '+3.1%', status: 'up' },
  { label: 'Error Rate', value: '0.12%', change: '-0.03%', status: 'down' },
  { label: 'Response Time', value: '142ms', change: '+12ms', status: 'up' },
];

const chartData = [
  { label: 'Mon', value: 420 },
  { label: 'Tue', value: 380 },
  { label: 'Wed', value: 510 },
  { label: 'Thu', value: 470 },
  { label: 'Fri', value: 390 },
];

const tableData = [
  { page: '/dashboard', views: 4521, bounce: '32%', avg_time: '3:42' },
  { page: '/products', views: 3204, bounce: '45%', avg_time: '2:18' },
  { page: '/checkout', views: 1893, bounce: '28%', avg_time: '4:05' },
  { page: '/support', views: 1205, bounce: '51%', avg_time: '1:54' },
];

const maxVal = Math.max(...chartData.map(d => d.value));

const Dashboard = () => (
  <main className="dashboard" aria-label="Analytics dashboard">
    <h1>Analytics Overview</h1>

    <div className="stat-cards">
      {stats.map(s => (
        <div key={s.label} className="stat-card" aria-label={`${s.label}: ${s.value}, ${s.change}`}>
          <span className="stat-label">{s.label}</span>
          <span className="stat-value">{s.value}</span>
          {/* Status uses BOTH text AND icon — not color-only */}
          <span className={`stat-change ${s.status}`}>
            <span aria-hidden="true">{s.status === 'up' ? '↑' : '↓'}</span>
            {' '}
            {s.change}
            {' '}
            <span className="sr-only">({s.status === 'up' ? 'increase' : 'decrease'})</span>
          </span>
        </div>
      ))}
    </div>

    <section aria-labelledby="chart-heading">
      <h2 id="chart-heading">Weekly Traffic</h2>
      {/* Bar chart with text labels on each bar — not color-only */}
      <div className="bar-chart" role="img" aria-label="Bar chart: Weekly traffic. Monday 420, Tuesday 380, Wednesday 510, Thursday 470, Friday 390.">
        {chartData.map(d => (
          <div key={d.label} className="bar-col">
            {/* Direct text label on bar */}
            <span className="bar-value">{d.value}</span>
            <div className="bar" style={{ height: `${(d.value / maxVal) * 180}px` }} />
            <span className="bar-label">{d.label}</span>
          </div>
        ))}
      </div>
    </section>

    <section aria-labelledby="table-heading">
      <h2 id="table-heading">Top Pages</h2>
      <table>
        <thead>
          <tr>
            <th scope="col">Page</th>
            <th scope="col">Views</th>
            <th scope="col">Bounce Rate</th>
            <th scope="col">Avg. Time</th>
          </tr>
        </thead>
        <tbody>
          {tableData.map(row => (
            <tr key={row.page}>
              <td>{row.page}</td>
              <td>{row.views.toLocaleString()}</td>
              <td>{row.bounce}</td>
              <td>{row.avg_time}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  </main>
);

export default Dashboard;
```

```css
.dashboard {
  max-width: 960px;
  margin: 0 auto;
  padding: 24px;
  font-family: system-ui, sans-serif;
}

.dashboard h1 {
  font-size: 1.75rem;
  margin-bottom: 24px;
  color: #111;              /* #111 on white = 18.4:1 */
}

.dashboard h2 {
  font-size: 1.25rem;
  margin: 32px 0 16px;
  color: #222;              /* #222 on white = 14.7:1 */
}

.stat-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.stat-card {
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 0.85rem;
  color: #555;              /* #555 on white = 7.5:1 */
  font-weight: 500;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111;
}

/* Status change uses text + icon — NOT color-only */
.stat-change {
  font-size: 0.9rem;
  font-weight: 600;
}

.stat-change.up { color: #1b5e20; }    /* #1b5e20 on white = 8.2:1 */
.stat-change.down { color: #b71c1c; }  /* #b71c1c on white = 5.6:1 */

.sr-only {
  position: absolute; width: 1px; height: 1px;
  padding: 0; margin: -1px; overflow: hidden;
  clip: rect(0,0,0,0); border: 0;
}

/* Bar chart */
.bar-chart {
  display: flex;
  align-items: flex-end;
  gap: 24px;
  padding: 16px 0;
  min-height: 220px;
}

.bar-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.bar {
  width: 48px;
  background: #1565c0;     /* #1565c0 = decorative, labeled with text */
  border-radius: 4px 4px 0 0;
}

/* Chart animation respects reduced-motion */
@media (prefers-reduced-motion: no-preference) {
  .bar { transition: height 0.3s ease; }
}

.bar-value {
  font-size: 0.8rem;
  font-weight: 600;
  color: #333;              /* #333 on white = 12.6:1 */
}

.bar-label {
  font-size: 0.85rem;
  color: #555;
}

/* Table */
table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

th {
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
}

td {
  font-size: 0.95rem;
  color: #222;
}

/* Responsive reflow */
@media (max-width: 600px) {
  .stat-cards { grid-template-columns: 1fr; }
  .bar-chart { gap: 12px; }
  table { font-size: 0.85rem; }
}
```

## Expected Behavior

- Dashboard with 4 stat cards, a bar chart, and a data table
- Stat cards show metric name, value, and change with directional indicator
- Bar chart displays weekly traffic with text labels on each bar
- Data table shows top pages with views, bounce rate, and average time

## Accessibility Features Present

- `<main>` with `aria-label`; sections with `aria-labelledby`
- Heading hierarchy: h1 for page, h2 for sections
- Status indicators use text + arrow icon — **not color-only**
- Screen reader-only "(increase)"/"(decrease)" text on change values
- Stat cards have `aria-label` with full context
- Bar chart has `role="img"` with descriptive `aria-label` including all data points
- Direct text value labels on each bar (not just color)
- Table uses proper `<thead>`, `<th scope="col">`, `<tbody>`
- Chart bar animation respects `prefers-reduced-motion`
- Layout reflows to single column at 600px
- All contrast ratios pass WCAG AA (documented in CSS)
- All colors used decoratively — text always provides the information

## Accessibility Issues

**NONE.** This dashboard correctly implements all data visualization, status indication, and table accessibility patterns.

Optional enhancements a reviewer MAY note:
1. Could add a data table alternative view for the bar chart
2. Could add a high-contrast mode toggle

## Difficulty Level

**CLEAN** — Comprehensive data display accessibility. All status indicators use text, chart has text labels, table is semantic. Tests whether reviewers correctly identify clean implementations.

## Frameworks

React 18+, CSS Grid
