# Fixture: Tab Panel Without Arrow Key Navigation

## Component Code

```jsx
import React, { useState } from 'react';

const tabs = [
  { id: 'overview', label: 'Overview', content: 'Product overview with key features, specifications, and use cases. This section covers the main value proposition and target audience.' },
  { id: 'specs', label: 'Specifications', content: 'Detailed technical specifications: dimensions, weight, materials, power requirements, connectivity options, and certifications.' },
  { id: 'reviews', label: 'Reviews', content: 'Customer reviews and ratings. Average 4.3/5 from 1,247 reviews. Common praise: build quality. Common critique: battery life.' },
  { id: 'support', label: 'Support', content: 'Warranty information, troubleshooting guides, firmware updates, and contact support options.' },
];

const TabPanel = () => {
  const [activeTab, setActiveTab] = useState('overview');

  // BUG: No Arrow key handling — only Tab/click switches panels
  // APG tabs pattern requires ArrowLeft/Right between tabs
  const handleTabClick = (tabId) => {
    setActiveTab(tabId);
  };

  return (
    <section className="tabs-component">
      <h2>Product Details</h2>

      {/* BUG: No role="tablist" — this is a plain div */}
      <div className="tab-bar">
        {tabs.map(tab => (
          // BUG: No role="tab", no aria-selected, no aria-controls
          <button
            key={tab.id}
            className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => handleTabClick(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {tabs.map(tab => (
        // BUG: No role="tabpanel", no aria-labelledby
        <div
          key={tab.id}
          className="tab-panel"
          style={{ display: activeTab === tab.id ? 'block' : 'none' }}
        >
          <p>{tab.content}</p>
        </div>
      ))}
    </section>
  );
};

export default TabPanel;
```

```css
.tabs-component {
  max-width: 640px;
  margin: 0 auto;
  padding: 24px;
  font-family: system-ui, sans-serif;
}

.tabs-component h2 {
  font-size: 1.5rem;
  margin-bottom: 16px;
}

.tab-bar {
  display: flex;
  border-bottom: 2px solid #e0e0e0;
  gap: 0;
}

.tab-btn {
  padding: 10px 20px;
  border: none;
  background: none;
  font-size: 0.95rem;
  font-weight: 600;
  color: #555;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
}

/* Visual active indicator — correct appearance but no ARIA */
.tab-btn.active {
  color: #1565c0;
  border-bottom-color: #1565c0;
}

.tab-btn:hover {
  color: #1565c0;
  background: #f5f5f5;
}

.tab-btn:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}

.tab-panel {
  padding: 16px 0;
}

.tab-panel p {
  font-size: 1rem;
  line-height: 1.6;
  color: #222;
}
```

## Expected Behavior

- Four tabs: Overview, Specifications, Reviews, Support
- Clicking a tab shows its panel content
- Active tab has visual underline indicator
- Arrow Left/Right should navigate between tabs (but don't)
- Only one panel visible at a time

## Accessibility Features Present

- Buttons are real `<button>` elements (keyboard activatable with Enter/Space)
- Visual active tab indicator (blue underline)
- Focus-visible outlines on tab buttons
- Heading structure (h2 for section title)
- Content shows/hides correctly on tab change

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: No Arrow Left/Right navigation — WCAG 2.1.1 (Keyboard) + APG Tabs Pattern**
   Only Tab key and click switch panels. The APG tabs pattern requires ArrowLeft/ArrowRight to move focus between tabs within the tablist, with Tab moving into the panel content.
   - Evidence: Lines 18-20 — `handleTabClick` with no keyboard handler; no `onKeyDown` on buttons
   - User group: Keyboard users, screen reader users
   - Fix: Add onKeyDown handler for ArrowLeft/Right/Home/End on the tab bar

2. **MAJOR: No role="tablist", role="tab", role="tabpanel" — WCAG 4.1.2 (Name, Role, Value)**
   Tab bar is a plain `<div>`, tabs are plain `<button>`, panels are plain `<div>`. Screen readers cannot identify the widget as a tab interface.
   - Evidence: Line 28 — `<div className="tab-bar">` with no role; Lines 30-36 — buttons with no `role="tab"`; Lines 40-46 — panels with no `role="tabpanel"`
   - User group: Screen reader users
   - Fix: Add `role="tablist"` on bar, `role="tab"` on buttons, `role="tabpanel"` on panels

3. **MAJOR: No aria-selected on active tab, no aria-controls linking tab to panel**
   Active tab is distinguished only by CSS class `.active`. No `aria-selected="true"` communicates the state. No `aria-controls` links tabs to their panels.
   - Evidence: Line 33 — CSS class only, no aria-selected; no aria-controls attribute
   - User group: Screen reader users
   - Fix: Add `aria-selected={activeTab === tab.id}` on each button; add `aria-controls={`panel-${tab.id}`}` and matching `id` on panels

4. **MINOR: Home/End keys don't jump to first/last tab — APG Tabs Pattern**
   No Home/End key handlers for quick navigation to boundary tabs.
   - Evidence: No onKeyDown handler at all
   - User group: Keyboard users
   - Fix: Add Home/End handlers in onKeyDown

5. **MINOR: Tab panels have no aria-labelledby pointing to their tab**
   Panel divs have no `aria-labelledby` attribute referencing the associated tab button.
   - Evidence: Lines 40-46 — `<div className="tab-panel">` with no aria-labelledby
   - User group: Screen reader users
   - Fix: Add `id={`tab-${tab.id}`}` on button and `aria-labelledby={`tab-${tab.id}`}` on panel

## Difficulty Level

**HAS-BUGS** — Existing dimension: Keyboard & Screen Reader. Classic APG pattern violations. The component looks correct visually — buttons work, content switches, active state shows. But the ARIA contract is entirely missing. This is a regression detection fixture.

## Frameworks

React 18+, CSS
