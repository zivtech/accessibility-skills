# Fixture: Garden Plot Directory

## Recent Changes (PR #77 and PR #103)

PR #77 (WBROOK-12) added `aria-label="Main navigation"` to the site header
nav as part of the initial landmark-labeling pass across the plot directory.
PR #103, filed two months later by a different contributor, added a sticky
mini-header that clones the header navigation into a fixed-position bar once
a visitor scrolls past the hero image, so the same links stay reachable
without scrolling back to the top.

## Component Code

```jsx
import React, { useEffect, useRef, useState } from 'react';
import './GardenPlotDirectory.css';

const NAV_LINKS = [
  { href: '/plots', label: 'Browse Plots' },
  { href: '/waitlist', label: 'Join Waitlist' },
  { href: '/plots/map', label: 'Garden Map' },
  { href: '/events', label: 'Events' },
];

const SiteNav = ({ className }) => (
  <nav aria-label="Main navigation" className={className}>
    <ul>
      {NAV_LINKS.map((link) => (
        <li key={link.href}>
          <a href={link.href}>{link.label}</a>
        </li>
      ))}
    </ul>
  </nav>
);

const StickyNavClone = () => {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const onScroll = () => setVisible(window.scrollY > 320);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  if (!visible) return null;

  return <SiteNav className="sticky-nav-clone" />;
};

const PlotMapFilters = () => (
  <nav aria-label="Plot map filters" className="map-filters">
    <ul>
      <li><a href="/plots/map?filter=available">Available plots</a></li>
      <li><a href="/plots/map?filter=raised-bed">Raised beds only</a></li>
      <li><a href="/plots/map?filter=full-sun">Full sun</a></li>
    </ul>
  </nav>
);

const GardenPlotDirectory = () => (
  <div className="garden-site">
    <header className="site-header">
      <div className="brand">Willowbrook Community Garden</div>
      <SiteNav className="site-nav" />
    </header>

    <StickyNavClone />

    <main>
      <section aria-labelledby="map-heading">
        <h1 id="map-heading">Find a Garden Plot</h1>
        <PlotMapFilters />
        <div className="plot-map" role="img" aria-label="Map of available garden plots by section">
          {/* interactive map rendered here */}
        </div>
      </section>
    </main>
  </div>
);

export default GardenPlotDirectory;
```

## CSS

```css
.site-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: #ffffff;
  border-bottom: 1px solid #e2e8e0;
}

.brand {
  font-weight: 700;
  color: #2f4a2f;
}

.site-nav ul,
.sticky-nav-clone ul,
.map-filters ul {
  display: flex;
  list-style: none;
  gap: 20px;
  padding: 0;
  margin: 0;
}

.site-nav a,
.sticky-nav-clone a,
.map-filters a {
  color: #2f4a2f;
  text-decoration: none;
  font-size: 14px;
}

.sticky-nav-clone {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 40;
  background: #ffffff;
  padding: 12px 24px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.map-filters {
  margin: 16px 0 20px 0;
}

.plot-map {
  height: 420px;
  background: #eef3e4;
  border-radius: 8px;
}
```

## Expected Behavior

- The header shows the garden's main navigation (Browse Plots, Join Waitlist, Garden Map, Events).
- Once a visitor scrolls past the hero image, a sticky mini-header appears at the top of the viewport with the same navigation, so the links stay reachable without scrolling back up.
- The plot-finder page also has its own, separately-labeled navigation for filtering the map (available plots, raised beds, full sun).

## Accessibility Features Present

✓ Main navigation has aria-label distinguishing it from other landmarks on the page
✓ Plot map filters are a separate nav landmark with its own distinct aria-label ("Plot map filters")
✓ The interactive plot map has an accessible name via role="img" aria-label
✓ All navigation links are real anchor elements with visible, descriptive text
✓ Sticky nav only mounts once the visitor has actually scrolled past the hero (not present in the DOM before that point)

## Accessibility Issues

_Answer key: planted defects._

1. **MUST-FIND / MINOR (severity-calibration item — see rubric): Once scrolled, two `<nav aria-label="Main navigation">` landmarks with identical content exist in the accessibility tree at the same time.** `StickyNavClone` renders a full second `<SiteNav>` once `window.scrollY > 320`, and nothing hides or removes the original header `<nav>` when the clone appears — it simply scrolls out of the visible viewport but remains fully present in the DOM and the accessibility tree. A screen reader user navigating by landmark (e.g., NVDA/JAWS "next landmark," or the VoiceOver rotor) encounters "navigation, Main navigation" twice, with the same four links each time, and has no way to tell from the announcement alone that one is a duplicate of the other.
   - Evidence: `garden-plot-directory.md` — `<SiteNav className="site-nav" />` in `.site-header` and `<SiteNav className="sticky-nav-clone" />` rendered by `StickyNavClone`, both using the identical `aria-label="Main navigation"` from the shared `SiteNav` component; neither is hidden from assistive technology when the other is present
   - WCAG: 1.3.1 Info and Relationships (duplicate landmark relationship is misleading), 4.1.2 Name, Role, Value (two elements share one accessible name and role simultaneously)
   - Impact: Landmark-navigation efficiency is degraded — a user has to work out which "Main navigation" is the real one, or tab/arrow through both — but every link remains reachable, correctly labeled, and fully operable through either copy. No functionality is lost and no content is unreachable.
   - User group: Screen reader users navigating by landmark
   - Fix: Do not clone the nav into a second DOM node. Either apply `position: sticky` directly to the single existing `<SiteNav>` (so there is only ever one nav element, repositioned by CSS rather than duplicated by JS), or, if a genuinely separate sticky element is required, hide one copy from the accessibility tree at all times (e.g., `aria-hidden="true"` plus `tabIndex="-1"` on its links) while the other is the exposed copy — never expose both simultaneously
   - **Severity note**: This must be rated MINOR (or ENHANCEMENT), not CRITICAL or MAJOR. See "Difficulty Level" below for why inflating this finding's severity is scored as a calibration failure, not extra credit.

2. **SHOULD-FIND / MINOR: The duplicate isn't only a landmark-navigation issue — it also duplicates the same links in the sequential Tab order once the sticky bar is visible.** A keyboard user who has scrolled past the hero and starts tabbing forward encounters the sticky clone's four links, and — depending on where the original header nav sits relative to the current scroll position in the DOM's tab sequence — may encounter the same four destinations again from the original header nav that is now scrolled out of view. This is a distinct symptom of the same root cause (full DOM duplication) from Issue 1's landmark-level framing.
   - Evidence: `garden-plot-directory.md` — both nav copies remain in the DOM and neither has `tabIndex="-1"` applied to its links, so both are part of the normal tab sequence whenever both are present
   - WCAG: 2.4.3 Focus Order (redundant tab stops), 1.3.1 Info and Relationships
   - Impact: Minor friction for keyboard users — extra, identical tab stops to pass through — not a blocked task
   - User group: Keyboard users
   - Fix: Same root fix as Issue 1 (stop duplicating the DOM node); as an interim measure, `tabIndex="-1"` on the hidden copy's links would at least remove the redundant tab stops

## Difficulty Level

**HAS-BUGS** — This fixture is a deliberate severity-calibration test, not a detection-difficulty test. The duplicate landmark is easy to notice once a reviewer checks the DOM at a scrolled state — it is not hidden or subtle. What is being tested is whether the reviewer's severity rating matches actual user impact: every link in both nav copies is correctly labeled and fully operable; nothing is unreachable; no task is blocked. This is friction with a workaround (the user can simply keep navigating past the duplicate), which the a11y-critic severity ladder defines as MINOR — "friction but workaround exists" — not CRITICAL ("blocks access entirely") or MAJOR ("significantly degrades experience for a user category"). A reviewer who inflates this to CRITICAL or MAJOR ("screen reader users can't navigate the page!") has overstated the impact; a reviewer who finds it and rates it MINOR (or a clearly-reasoned low severity) has calibrated correctly.

## Frameworks & Environment

React 18+, standard CSS

## Notes

This fixture pairs a real, findable defect with a severity-calibration test rather than a needle-in-a-haystack detection test:

1. **Detection is the easy part** — inspecting the DOM after scrolling past the hero reveals two identically-labeled nav landmarks immediately. Most competent reviewers who think to check DOM state at a scrolled position will find this.
2. **Calibration is the hard part** — the finding must be rated proportionally to its actual impact (workaround exists, nothing is blocked, all content remains reachable) rather than to the reviewer's discomfort at seeing "duplicate ARIA" in the abstract. Landmark duplication sounds alarming as a category of defect; here, concretely, it costs a user some navigational efficiency and nothing else.
3. **False-positive resistance**: `<nav aria-label="Plot map filters">` is a second, entirely legitimate navigation landmark on the same page, with a different accessible name and a genuinely different purpose (filtering the map, not sitewide navigation). A reviewer should recognize multiple nav landmarks with *distinct* names as normal and expected, and not lump it in with the actual duplicate (same role, same name) as if multiple `<nav>` elements were inherently the problem.

Expected verdict: REVISE (the finding is real and should be fixed), but a REVISE built on a CRITICAL/MAJOR misrating of this specific finding is itself a scoring failure — see the rubric's dedicated severity-calibration dimension.
