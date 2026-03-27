# Fixture: Tabs Component Missing Arrow Key Navigation

## Component Code

```jsx
import React, { useState } from 'react';

const TabsWidget = ({ tabs }) => {
  const [activeTab, setActiveTab] = useState(0);

  const handleTabClick = (index) => {
    setActiveTab(index);
  };

  // BUG: No keyboard handler for arrow keys
  const handleTabKeyDown = (e) => {
    // Only handles Enter/Space, not arrow keys
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleTabClick(tabs.findIndex(t => t.id === e.currentTarget.id));
    }
  };

  return (
    <div className="tabs-container">
      <div role="tablist" aria-label="Content tabs">
        {tabs.map((tab, index) => (
          <button
            key={tab.id}
            id={`tab-${tab.id}`}
            role="tab"
            aria-selected={index === activeTab}
            aria-controls={`panel-${tab.id}`}
            tabIndex={index === activeTab ? 0 : -1}
            onClick={() => handleTabClick(index)}
            onKeyDown={handleTabKeyDown}
            className={`tab-button ${index === activeTab ? 'active' : ''}`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="tab-panels">
        {tabs.map((tab, index) => (
          <div
            key={tab.id}
            id={`panel-${tab.id}`}
            role="tabpanel"
            aria-labelledby={`tab-${tab.id}`}
            hidden={index !== activeTab}
            className={`tab-panel ${index === activeTab ? 'active' : ''}`}
          >
            <p>{tab.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TabsWidget;
```

## CSS

```css
.tabs-container {
  margin: 20px 0;
}

[role="tablist"] {
  display: flex;
  border-bottom: 2px solid #0066cc;
  gap: 4px;
}

.tab-button {
  padding: 12px 20px;
  border: none;
  background: transparent;
  color: #666;
  font-size: 16px;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
  transition: color 0.2s;
}

.tab-button:hover {
  color: #0066cc;
}

.tab-button.active {
  color: #0066cc;
  border-bottom-color: #0066cc;
  font-weight: 600;
}

.tab-button:focus {
  outline: 3px solid #0066cc;
  outline-offset: 2px;
}

.tab-panel {
  display: none;
  padding: 20px;
  border: 1px solid #ddd;
  border-top: none;
  margin-bottom: 20px;
}

.tab-panel.active {
  display: block;
}

.tab-panel[hidden] {
  display: none !important;
}
```

## Expected Behavior

- Clicking tabs switches active panel
- Tab key navigates through tabs
- Arrow Left/Right should cycle through tabs (standard pattern)
- aria-selected reflects active tab
- aria-controls links tab to panel
- Panels shown/hidden based on active tab

## Accessibility Features Present

✓ role="tablist" on container
✓ role="tab" on buttons
✓ role="tabpanel" on panels
✓ aria-selected toggles with state
✓ aria-controls links tabs to panels
✓ aria-labelledby links panels to tabs
✓ Roving tabindex (active tab tabindex="0", others "-1")
✓ hidden attribute hides inactive panels
✓ Focus indicator visible on buttons
✓ Label on tablist

## Accessibility Issues (Planted)

1. **MAJOR: Arrow key navigation not implemented** — Per WAI-ARIA Tabs pattern, Left/Right arrow keys should cycle through tabs. Currently, arrow keys do nothing. Keyboard-only users must use Tab to navigate, which is inefficient for widgets with many tabs.
   - Evidence: `tabs-missing-arrow-nav.md:10-16` (handleTabKeyDown only handles Enter/Space, not arrow keys)
   - WCAG citation: 2.1.1 Keyboard (keyboard access for all functionality)
   - WAI-ARIA pattern: Tabs pattern requires arrow key navigation
   - User group: Keyboard-only users
   - Expected: Arrow Left cycles to previous tab (wrapping), Arrow Right cycles to next tab
   - Fix: Add arrow key handling to handleTabKeyDown, update focus after setting active tab

2. **MINOR: Active tab not automatically focused after arrow key navigation** — Even if arrow keys were implemented, the code doesn't move focus to the newly active tab. The pattern shows roving tabindex but focus doesn't follow tabindex change.
   - Evidence: `tabs-missing-arrow-nav.md:10-16` (no focus management on tab switch)
   - WAI-ARIA pattern: Active tab should receive focus after keyboard selection
   - User group: Keyboard users (reduces discoverability)
   - Expected: After arrow key, focus moves to newly active tab
   - Fix: After handleTabClick, query and focus the newly active tab button

## Difficulty Level

**HAS-BUGS** — The ARIA structure is correct and complete (tablist, tab role, aria-selected, aria-controls, roving tabindex all present). However, the keyboard interaction pattern is incomplete. Arrow key navigation is a "must-have" per WAI-ARIA Tabs pattern, not optional.

Expected that baseline might miss this if it only checks for ARIA attributes. A11y-critic should identify this as a pattern incompleteness issue.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Notes

This fixture tests whether a11y-critic can distinguish between:
1. **ARIA attributes present and correct** (this is true)
2. **Keyboard interaction pattern complete** (this is false)

Generic a11y reviewers often check boxes (aria-selected? ✓ aria-controls? ✓) and miss pattern completeness. A11y-critic should catch this via the "Pattern Compliance Audit" phase and explicitly note the gap in the "What's Missing" section.
