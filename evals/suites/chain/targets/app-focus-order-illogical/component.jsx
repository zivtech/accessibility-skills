import React from 'react';
import './AppLayout.css';

const AppLayout = () => {
  return (
    <div className="app-layout">
      <a href="#content" className="skip-link">
        Skip to main content
      </a>

      <header className="app-header">
        <div className="logo">
          <a href="/">Acme Dashboard</a>
        </div>
        <nav aria-label="Header navigation">
          <ul className="header-nav">
            <li><a href="/notifications">Notifications</a></li>
            <li><a href="/settings">Settings</a></li>
            <li><a href="/profile">Profile</a></li>
          </ul>
        </nav>
      </header>

      <div className="app-body">
        <main className="main-content">
          <div id="content">
            <h1>Dashboard</h1>
          </div>

          <section aria-labelledby="recent-heading">
            <h2 id="recent-heading">Recent Activity</h2>
            <ul className="activity-list">
              <li>
                <a href="/reports/q1">Q1 Performance Report</a>
                <span className="activity-date">May 12, 2026</span>
              </li>
              <li>
                <a href="/reports/q2">Q2 Forecast Draft</a>
                <span className="activity-date">May 10, 2026</span>
              </li>
              <li>
                <a href="/reports/audit">Annual Audit Summary</a>
                <span className="activity-date">May 8, 2026</span>
              </li>
            </ul>
          </section>

          <section aria-labelledby="tasks-heading">
            <h2 id="tasks-heading">Open Tasks</h2>
            <ul className="task-list">
              <li>
                <a href="/tasks/142">Review budget proposal</a>
                <span className="task-status">Due May 20</span>
              </li>
              <li>
                <a href="/tasks/143">Approve vendor contract</a>
                <span className="task-status">Due May 22</span>
              </li>
            </ul>
          </section>
        </main>

        <aside className="sidebar">
          <nav aria-label="Sidebar navigation">
            <h2 className="sidebar-heading">Navigation</h2>
            <ul className="sidebar-nav">
              <li><a href="/dashboard">Dashboard</a></li>
              <li><a href="/reports">Reports</a></li>
              <li><a href="/analytics">Analytics</a></li>
              <li><a href="/team">Team</a></li>
              <li><a href="/projects">Projects</a></li>
              <li><a href="/invoices">Invoices</a></li>
            </ul>
          </nav>
        </aside>
      </div>

      <button
        className="fab"
        tabIndex={1}
        aria-label="Create new report"
        onClick={() => console.log('create report')}
      >
        +
      </button>
    </div>
  );
};

export default AppLayout;
