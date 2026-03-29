# Calibration Fixture C4: Animated Dashboard

## Component Description

React analytics dashboard with live-updating charts, animated counters, a scrolling news ticker, and color-coded severity alerts. Multiple simultaneous visual and interactive concerns.

## Component Code

```jsx
import React, { useState, useEffect, useRef } from 'react';

const AlertSeverity = { critical: '#d32f2f', warning: '#f57c00', info: '#1565c0' };

const AnimatedDashboard = () => {
  const [counters, setCounters] = useState({ users: 0, revenue: 0, errors: 0, uptime: 0 });
  const [tickerPos, setTickerPos] = useState(0);
  const tickerRef = useRef(null);
  const targets = { users: 12847, revenue: 142300, errors: 12, uptime: 99.9 };

  // Animated counter increment
  useEffect(() => {
    const duration = 2000;
    const start = Date.now();
    const animate = () => {
      const progress = Math.min((Date.now() - start) / duration, 1);
      setCounters({
        users: Math.round(targets.users * progress),
        revenue: Math.round(targets.revenue * progress),
        errors: Math.round(targets.errors * progress),
        uptime: +(targets.uptime * progress).toFixed(1),
      });
      if (progress < 1) requestAnimationFrame(animate);
    };
    requestAnimationFrame(animate);
  }, []);

  // Scrolling ticker — continuous horizontal scroll
  useEffect(() => {
    const interval = setInterval(() => {
      setTickerPos(p => p - 1);
    }, 30);
    return () => clearInterval(interval);
  }, []);

  const alerts = [
    { severity: 'critical', text: 'Database CPU at 95% — scale up recommended' },
    { severity: 'warning', text: 'API latency above 200ms threshold' },
    { severity: 'info', text: 'Deploy v3.2.1 completed successfully' },
    { severity: 'critical', text: 'Payment gateway timeout — 3 failed transactions' },
    { severity: 'warning', text: 'Memory usage at 82% on worker-3' },
  ];

  const tickerItems = [
    'Users online: 3,421',
    'Transactions/sec: 847',
    'Cache hit rate: 94.2%',
    'CDN bandwidth: 2.3 TB/day',
    'Queue depth: 142',
  ];

  return (
    <main className="live-dashboard">
      <h1>Operations Dashboard</h1>

      <div className="counter-grid">
        {Object.entries(counters).map(([key, val]) => (
          <div key={key} className="counter-card">
            <span className="counter-label">{key}</span>
            <span className="counter-value">{key === 'revenue' ? `$${val.toLocaleString()}` : val.toLocaleString()}</span>
          </div>
        ))}
      </div>

      <div className="ticker-strip">
        <div className="ticker-track" style={{ transform: `translateX(${tickerPos}px)` }} ref={tickerRef}>
          {[...tickerItems, ...tickerItems].map((item, i) => (
            <span key={i} className="ticker-item">{item}</span>
          ))}
        </div>
      </div>

      <section className="chart-panel" aria-label="Traffic chart">
        <h2>Live Traffic</h2>
        <div className="animated-chart">
          {[65, 80, 45, 92, 73, 88, 60].map((h, i) => (
            <div key={i} className="chart-bar" style={{ height: `${h}%`, animationDelay: `${i * 0.1}s` }} />
          ))}
        </div>
      </section>

      <section className="alerts-panel" aria-label="System alerts">
        <h2>Active Alerts</h2>
        {alerts.map((alert, i) => (
          <div key={i} className="alert-row" style={{ borderLeftColor: AlertSeverity[alert.severity] }}>
            <span className="alert-badge" style={{ backgroundColor: AlertSeverity[alert.severity] }}>
              {alert.severity}
            </span>
            <span className="alert-text">{alert.text}</span>
          </div>
        ))}
      </section>
    </main>
  );
};

export default AnimatedDashboard;
```

```css
.live-dashboard { max-width: 960px; margin: 0 auto; padding: 24px; font-family: system-ui; }
.live-dashboard h1 { font-size: 1.75rem; margin-bottom: 20px; }
.live-dashboard h2 { font-size: 1.25rem; margin-bottom: 12px; }

.counter-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 16px; }
.counter-card { background: #f5f5f5; padding: 16px; border-radius: 8px; text-align: center; }
.counter-label { display: block; font-size: 0.8rem; color: #555; text-transform: capitalize; }
.counter-value { display: block; font-size: 1.5rem; font-weight: 700; color: #111; }

.ticker-strip { overflow: hidden; background: #222; padding: 8px 0; margin-bottom: 16px; }
.ticker-track { display: flex; gap: 48px; white-space: nowrap; }
.ticker-item { color: #ccc; font-size: 0.85rem; }

.chart-panel { margin-bottom: 24px; }
.animated-chart { display: flex; align-items: flex-end; gap: 8px; height: 150px; padding: 8px; background: #fafafa; border-radius: 4px; }
.chart-bar {
  flex: 1; background: #1565c0; border-radius: 4px 4px 0 0; min-width: 20px;
  animation: growBar 1s ease forwards;
  transform-origin: bottom;
}
@keyframes growBar { from { transform: scaleY(0); } to { transform: scaleY(1); } }

.alerts-panel { margin-bottom: 24px; }
.alert-row { display: flex; align-items: center; gap: 12px; padding: 10px 12px; border-left: 4px solid; margin-bottom: 8px; background: #fafafa; border-radius: 0 4px 4px 0; }
.alert-badge { padding: 2px 8px; border-radius: 4px; color: #fff; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }
.alert-text { font-size: 0.9rem; color: #333; }
```

## Why This Is a Calibration Fixture

This dashboard has **many simultaneous accessibility concerns** across multiple perspectives. It is designed to test whether the alarm level escalation mechanism correctly identifies a component with broadly HIGH alarm levels rather than averaging them down.

## Expected Alarm Levels

| Perspective | Expected | Rationale |
|---|---|---|
| Vestibular & Motion | **HIGH** | Scrolling ticker (continuous), counter animations (2s), chart bar grow animations — multiple simultaneous motion sources |
| Environmental Contrast | **HIGH** | Color-coded alert severity (red/orange/blue) — color carries meaning; badge text alone may not suffice |
| Keyboard & Motor | **HIGH** | Chart panel and alert rows are interactive-looking but may lack keyboard access; multiple widget regions |
| Screen Reader & Semantic | **HIGH** | Live counter updates, ticker content, chart with no accessible data alternative, alert severity communicated via color |
| Magnification & Reflow | **MEDIUM** | Dense 4-column counter grid may overflow; chart has fixed heights; ticker clips at zoom |
| Cognitive & Neurodivergent | **MEDIUM** | Information density with multiple simultaneous updating regions; scrolling ticker creates cognitive competition |
| Auditory Access | **LOW** | No audio or media content |

## Frameworks

React 18+, CSS Animations
