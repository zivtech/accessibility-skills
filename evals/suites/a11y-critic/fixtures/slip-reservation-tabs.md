# Fixture: Slip Reservation Tabs

## Recent Changes (PR #93)

Closes DOCK-56. Converts the reservation-category navigation from a plain
list of links to a proper WAI-ARIA tabs pattern: each category button now
carries `role="tab"`, `aria-selected`, and roving tabindex, and the wrapping
list items are marked `role="presentation"` so screen readers announce the
tab positions cleanly instead of "list item, tab" for every entry.

## Component Code

```jsx
import React, { useState, useRef } from 'react';
import './SlipReservationTabs.css';

const CATEGORIES = [
  { id: 'overnight', label: 'Overnight Slips' },
  { id: 'seasonal', label: 'Seasonal Slips' },
  { id: 'transient', label: 'Transient Slips' },
];

const SlipReservationTabs = () => {
  const [activeTab, setActiveTab] = useState(0);
  const tabRefs = useRef([]);

  const handleKeyDown = (e, index) => {
    const tabEls = tabRefs.current.filter(Boolean);
    let nextIndex;
    switch (e.key) {
      case 'ArrowRight':
        e.preventDefault();
        nextIndex = (index + 1) % tabEls.length;
        setActiveTab(nextIndex);
        tabEls[nextIndex].focus();
        break;
      case 'ArrowLeft':
        e.preventDefault();
        nextIndex = (index - 1 + tabEls.length) % tabEls.length;
        setActiveTab(nextIndex);
        tabEls[nextIndex].focus();
        break;
      default:
        break;
    }
  };

  return (
    <div className="slip-reservation-panel">
      <ul role="tablist" aria-label="Reservation categories" className="reservation-tablist">
        {CATEGORIES.map((cat, index) => (
          <li role="presentation" key={cat.id}>
            <button
              ref={(el) => (tabRefs.current[index] = el)}
              role="tab"
              id={`tab-${cat.id}`}
              aria-selected={index === activeTab}
              aria-controls={`panel-${cat.id}`}
              tabIndex={index === activeTab ? 0 : -1}
              onClick={() => setActiveTab(index)}
              onKeyDown={(e) => handleKeyDown(e, index)}
              className={`reservation-tab ${index === activeTab ? 'active' : ''}`}
            >
              {cat.label}
            </button>
          </li>
        ))}
        <li>
          <a href="/marina/dock-rates.pdf" className="dock-rates-link">
            Dock Rates &amp; Rules (PDF)
          </a>
        </li>
      </ul>

      {CATEGORIES.map((cat, index) => (
        <div
          key={cat.id}
          role="tabpanel"
          id={`panel-${cat.id}`}
          aria-labelledby={`tab-${cat.id}`}
          tabIndex={0}
          hidden={index !== activeTab}
          className="reservation-panel"
        >
          <h3>{cat.label}</h3>
          <p>Available slips update daily. Contact the harbormaster's office to confirm openings.</p>
        </div>
      ))}
    </div>
  );
};

export default SlipReservationTabs;
```

## CSS

```css
.slip-reservation-panel {
  max-width: 720px;
  margin: 24px auto;
}

.reservation-tablist {
  display: flex;
  align-items: center;
  list-style: none;
  padding: 0;
  margin: 0;
  border-bottom: 2px solid #cbd5e1;
  gap: 4px;
}

.reservation-tab {
  padding: 12px 20px;
  border: none;
  background: #f1f5f9;
  color: #475569;
  font-size: 14px;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
}

.reservation-tab.active {
  background: #ffffff;
  color: #0c4a6e;
  border-bottom-color: #0c4a6e;
  font-weight: 600;
}

.reservation-tab:focus-visible {
  outline: 2px solid #0284c7;
  outline-offset: -2px;
}

.dock-rates-link {
  margin-left: auto;
  padding: 12px 16px;
  color: #0c4a6e;
  font-size: 14px;
  text-decoration: underline;
}

.reservation-panel {
  padding: 20px 4px;
}

.reservation-panel[hidden] {
  display: none;
}
```

## Expected Behavior

- Arrow Left/Right cycles between the three reservation category tabs.
- Selecting a tab shows the matching panel and moves focus to the newly-active tab.
- A "Dock Rates & Rules" link sits at the end of the same row for quick reference while browsing categories.

## Accessibility Features Present

✓ Each category button has role="tab", aria-selected, and roving tabindex (active tab = 0, others = -1)
✓ Focus moves to the newly-selected tab on arrow key navigation
✓ Each tabpanel has aria-labelledby pointing back to its tab, and each tab has aria-controls pointing to its panel
✓ Tabpanels use the hidden attribute rather than conditional unmounting
✓ The three category `<li>` wrappers use role="presentation" so their list-item semantics don't interfere with the tablist

## Accessibility Issues

_Answer key: planted defects._

1. **MUST-FIND / MAJOR: A non-tab link sits inside the tablist without role="presentation" on its wrapping list item, breaking the tablist's expected content model and its position-in-set announcement.** The "Dock Rates & Rules (PDF)" link's `<li>` is the fourth child of `<ul role="tablist">`, but unlike its three sibling list items, it has no `role="presentation"`. WAI-ARIA's tablist pattern expects a tablist's children to be tabs (or presentational wrappers around them) — a bare list item with a plain link inside breaks that expectation. In practice, this means the container's list-item semantics leak through inconsistently: three items are silenced (role="presentation") so only their tab role is announced, while the fourth keeps its "list item" role alongside a link that has no tab semantics at all. Depending on the assistive technology, this produces an inconsistent announcement across children of the same container (e.g., some screen readers compute "tab 1 of 4" for the real tabs from the tablist's child count, when only 3 real tabs exist), and a screen reader or switch user navigating the tablist by its expected pattern encounters an item that doesn't behave like the three before it.
   - Evidence: `slip-reservation-tabs.md` — `<li role="presentation">` on the three category items vs. plain `<li>` (no role) wrapping the `<a href="/marina/dock-rates.pdf">` link, all as siblings inside `<ul role="tablist">`
   - WCAG: 1.3.1 Info and Relationships, 4.1.2 Name, Role, Value
   - APG: WAI-ARIA Tabs Pattern — tablist children should be tab elements (or non-tab content should live outside the tablist container)
   - Impact: Screen reader users may hear an incorrect tab count (e.g., "1 of 4" for a 3-tab set), and encounter an item inside the tablist that isn't a tab, isn't part of the panel-switching mechanism, and breaks the pattern's consistency
   - User group: Screen reader users, switch-access users relying on consistent widget patterns
   - Fix: Move the "Dock Rates & Rules" link outside the `<ul role="tablist">` entirely (e.g., into its own `<div>` alongside the tablist), or if it must stay visually adjacent, wrap it in an element with `role="presentation"` and keep it clearly outside the tab/panel relationship

2. **SHOULD-FIND / MINOR: The arrow-key handler's tab collection can pick up the stray link as an unintended fifth focus target if the ref array is read broadly.** `tabRefs.current` is populated only from the three category buttons in this version, so arrow keys currently cycle correctly among exactly three tabs — but the ref array is built by index position inside the `.map()`, with no defensive filtering beyond `Boolean`, and the dock-rates link is not excluded by any explicit check tied to `role="tab"`. A reviewer should verify (and a future edit could easily break) that arrow-key cycling is bound to the count of real tabs, not to "however many focusable things happen to be inside the tablist" — the un-roled `<li>` from Issue 1 is exactly the kind of element a less careful implementation of this same pattern would sweep into the roving-tabindex sequence.
   - Evidence: `slip-reservation-tabs.md` — `tabRefs.current.filter(Boolean)` inside `handleKeyDown`, with no `role="tab"` filter tying the roving sequence explicitly to real tabs
   - WCAG: 2.4.3 Focus Order (APG Tabs pattern — only tabs participate in the roving tabindex sequence)
   - Impact: Currently correct in this version, but fragile — the same defect class as Issue 1 (a non-tab element inside the tablist) is one likely edit away from also breaking arrow-key navigation
   - User group: Keyboard users
   - Fix: Build the ref array by explicitly querying `role="tab"` elements (or filtering the categories array itself) rather than relying on map index/Boolean filtering alone

## Difficulty Level

**HAS-BUGS** — The tab/panel binding itself is a complete, correctly-implemented WAI-ARIA Tabs pattern: roving tabindex, focus-follows-selection, aria-controls/aria-labelledby both directions, and role="presentation" on the tab wrappers. The defect is narrower and more structural: a legitimate, unrelated navigation link was placed inside the same list used for the tablist, and only the tab items received the presentational-wrapper treatment during remediation — the pre-existing link's wrapper was left untouched.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Notes

This fixture rewards precision rather than broad suspicion of `role="presentation"`:

1. **False-positive resistance** — `role="presentation"` on the three real tab wrappers is the *correct* pattern here (list-based tab markup routinely needs it so AT doesn't announce redundant "list item" roles alongside "tab"). A reviewer unfamiliar with this convention might flag all four `role="presentation"` opportunities uniformly ("why does the tablist have presentation roles removing semantics?") rather than noticing that three are correct and the fourth's *absence* is the actual bug.
2. **Structural precision** — the bug isn't in the tab pattern's mechanics (which are complete and correct) but in what does and doesn't belong inside the tablist container as a matter of markup structure. Finding it requires checking the tablist's full child list against the APG's expected content model, not just verifying the tab/panel attributes pairwise.
3. The should_find item asks whether a reviewer notices the *fragility* of the current arrow-key implementation, not a currently-observable behavior bug — a stronger reviewer flags risk, not only present-tense breakage.

Expected verdict: REVISE.
