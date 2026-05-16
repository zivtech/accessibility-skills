# Fixture: Tabs with Incomplete Selection and Panel Binding

## Component Code

```jsx
import React, { useState, useRef } from 'react';

const ProductTabs = ({ products }) => {
  const [activeTab, setActiveTab] = useState(0);
  const tabRefs = useRef([]);

  const handleKeyDown = (e, index) => {
    let newIndex;
    switch (e.key) {
      case 'ArrowRight':
        e.preventDefault();
        newIndex = (index + 1) % products.length;
        setActiveTab(newIndex);
        // BUG: Focus not moved to newly active tab
        break;
      case 'ArrowLeft':
        e.preventDefault();
        newIndex = (index - 1 + products.length) % products.length;
        setActiveTab(newIndex);
        // BUG: Focus not moved to newly active tab
        break;
      case 'Home':
        e.preventDefault();
        setActiveTab(0);
        break;
      case 'End':
        e.preventDefault();
        setActiveTab(products.length - 1);
        break;
      default:
        break;
    }
  };

  return (
    <div className="product-tabs">
      <div role="tablist" aria-label="Product categories">
        {products.map((product, index) => (
          <button
            key={product.id}
            ref={el => tabRefs.current[index] = el}
            role="tab"
            id={`tab-${product.id}`}
            aria-selected={index === activeTab}
            tabIndex={index === activeTab ? 0 : -1}
            onClick={() => setActiveTab(index)}
            onKeyDown={(e) => handleKeyDown(e, index)}
            className={`product-tab ${index === activeTab ? 'active' : ''}`}
          >
            {product.name}
            {product.count > 0 && (
              <span className="badge">{product.count}</span>
            )}
          </button>
        ))}
      </div>

      {products.map((product, index) => (
        <div
          key={product.id}
          role="tabpanel"
          id={`panel-${product.id}`}
          tabIndex={0}
          hidden={index !== activeTab}
          className="product-panel"
        >
          <h3>{product.name}</h3>
          <p>{product.description}</p>
          <ul>
            {product.items.map(item => (
              <li key={item.id}>
                <a href={item.url}>{item.title}</a>
                <span className="price">${item.price}</span>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
};

export default ProductTabs;
```

## CSS

```css
.product-tabs {
  max-width: 800px;
  margin: 24px auto;
}

[role="tablist"] {
  display: flex;
  border-bottom: 2px solid #e2e8f0;
  gap: 2px;
}

.product-tab {
  padding: 12px 20px;
  border: none;
  background: #f8fafc;
  color: #64748b;
  font-size: 14px;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.product-tab:hover {
  background: #f1f5f9;
  color: #334155;
}

.product-tab.active {
  color: #1e40af;
  border-bottom-color: #1e40af;
  background: white;
  font-weight: 600;
}

.product-tab:focus {
  outline: 2px solid #3b82f6;
  outline-offset: -2px;
}

.badge {
  background: #e2e8f0;
  color: #475569;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.product-tab.active .badge {
  background: #dbeafe;
  color: #1e40af;
}

.product-panel {
  padding: 24px;
  border: 1px solid #e2e8f0;
  border-top: none;
}

.product-panel[hidden] {
  display: none;
}

.product-panel h3 {
  margin: 0 0 12px;
  font-size: 18px;
  color: #1e293b;
}

.product-panel ul {
  list-style: none;
  padding: 0;
}

.product-panel li {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f1f5f9;
}

.price {
  color: #059669;
  font-weight: 600;
}
```

## Expected Behavior

- Arrow Left/Right cycles through tabs
- Tab content updates when selection changes
- aria-selected reflects the active tab
- Each panel displays product details with links
- Badge counts shown on tabs

## Accessibility Features Present

✓ role="tablist" on container with aria-label
✓ role="tab" on each button
✓ aria-selected toggles correctly
✓ Roving tabindex (active=0, others=-1)
✓ Arrow key navigation implemented (Left, Right, Home, End)
✓ role="tabpanel" on each content panel
✓ hidden attribute on inactive panels
✓ Focus indicator visible (2px solid blue)
✓ Semantic list for product items

## Accessibility Issues (Planted)

1. **MAJOR: Focus does not follow aria-selected on arrow key navigation** — When a user presses Arrow Right/Left, aria-selected updates and the visual state changes, but DOM focus stays on the previously active tab. The user's screen reader announces the old tab while the panel content has changed. Per WAI-ARIA Tabs pattern, focus MUST move to the newly selected tab.
   - Evidence: `tabs-incomplete-aria-selected.md:16-19` and `tabs-incomplete-aria-selected.md:22-25` — setActiveTab called but tabRefs.current[newIndex].focus() never called
   - WCAG: 2.1.1 Keyboard, 4.1.2 Name/Role/Value
   - APG: WAI-ARIA Tabs — "When a tab is activated, focus moves to the active tab element"
   - Impact: Screen reader user hears wrong tab name; keyboard user sees focus indicator on wrong tab
   - Fix: Add `tabRefs.current[newIndex].focus()` after setActiveTab in arrow key handlers

2. **MAJOR: Tab panels missing aria-labelledby** — Each tabpanel has an id but no aria-labelledby linking back to its tab. Screen reader users landing on the panel (via Tab from the tablist) won't hear which tab the panel belongs to.
   - Evidence: `tabs-incomplete-aria-selected.md:60-68` — tabpanel divs have id and role but no aria-labelledby
   - WCAG: 1.3.1 Info and Relationships, 4.1.2 Name/Role/Value
   - APG: WAI-ARIA Tabs — "Each element with role tabpanel has the property aria-labelledby referring to its associated tab element"
   - Impact: Screen reader user can't identify which tab owns the panel content
   - Fix: Add `aria-labelledby={`tab-${product.id}`}` to each tabpanel

3. **MINOR: Tabs missing aria-controls linking to panels** — Tab buttons don't reference their associated panels. While aria-controls has mixed screen reader support, it's part of the complete APG Tabs pattern and aids programmatic association.
   - Evidence: `tabs-incomplete-aria-selected.md:40-52` — tab buttons have id but no aria-controls
   - WCAG: 4.1.2 Name/Role/Value (recommended, not required)
   - APG: WAI-ARIA Tabs — "Each element with role tab has the property aria-controls referring to its associated tabpanel element"
   - Impact: Low — most screen readers don't use aria-controls for navigation. But omitting it breaks the bidirectional tab↔panel relationship.
   - Fix: Add `aria-controls={`panel-${product.id}`}` to each tab button

4. **MINOR: Badge count not announced in accessible context** — The badge `<span>` has a visible count but no accessible name explaining what the number means. A screen reader user hears "Electronics 42" — is 42 the count of items, reviews, or something else?
   - Evidence: `tabs-incomplete-aria-selected.md:48-50` — bare `<span className="badge">{product.count}</span>` with no aria-label or visually-hidden label
   - WCAG: 1.3.1 Info and Relationships
   - Impact: Low — context usually makes it clear, but explicit labeling is better
   - Fix: Add `aria-label={`${product.count} items`}` or use visually-hidden text

## Difficulty Level

**FLAWED** — The ARIA structure looks mostly complete at first glance (tablist, tab, tabpanel, aria-selected, roving tabindex, arrow keys). A surface-level check sees "all the pieces" and moves on. The bugs are in the *connections* between pieces: focus doesn't follow selection, panels aren't linked to tabs, tabs aren't linked to panels. You have to trace the interaction flow, not just check attribute presence.

Expected baseline detection: ~25%. A zero-shot reviewer will see aria-selected toggling, arrow keys implemented, correct roles — and conclude the pattern is complete. The focus-not-following bug requires understanding that aria-selected alone doesn't move focus. The missing aria-labelledby requires checking the panel side after verifying the tab side.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Notes

This fixture tests three distinct skills:

1. **Interaction tracing** (must_find) — Can the critic trace what happens AFTER an arrow key press? The state updates but focus doesn't follow. This requires reading the handler code, not just the JSX.

2. **Bidirectional pattern verification** (should_find) — The tab→panel and panel→tab links are both incomplete. A thorough reviewer checks BOTH directions of the APG association, not just one.

3. **Contextual completeness** (nice_to_find) — The badge is a real-world pattern (counts on tabs) where the a11y gap is small but real. Tests whether the critic catches nuanced labeling gaps vs only checking structural ARIA.
