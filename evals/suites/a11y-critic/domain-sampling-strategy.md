# A11y-Critic Evaluation: Domain Sampling Strategy

## Overview

This document specifies the fixture sampling matrix for the a11y-critic skill evaluation. The strategy ensures comprehensive coverage of component types, accessibility issues, and difficulty levels while maintaining statistical power (target n=28-30).

## Sample Size Justification

- **Target sample size**: 28-30 fixtures (sufficient for 80% power at α=0.05, d=0.5 medium effect)
- **Repetitions**: 3 runs per fixture (reduces variance)
- **Total evaluations**: 84-90 (skill + 2 baselines × 28-30 fixtures × 3 repeats)
- **Formula**: n ≈ 2 × (z_α + z_β)² × σ² / δ² ≈ 28 for medium effect size

## Sampling Matrix

Target: 28-30 fixtures across **6 domains** × **4-5 difficulty tiers**, ensuring:

1. **Diversity across component types** (not all dropdowns)
2. **Balanced difficulty distribution** (not all ADVERSARIAL)
3. **Coverage of critical a11y patterns** (modals, tabs, forms, tables, live regions)
4. **Traps for false positives** (CLEAN fixtures, intentional non-issues)
5. **Multi-perspective representation** (every fixture relevant to 2-3 perspectives)

---

## Domain 1: Interactive Widgets (6 fixtures)

Custom interactive components that often have incomplete ARIA patterns.

| Component Type | Difficulty | Issue Class | Count | Notes |
|---|---|---|---|---|
| Custom Dropdown | CLEAN | Baseline | 1 | Properly implemented: aria-expanded, arrow keys, focus restoration |
| Custom Dropdown | HAS-BUGS | Focus Management | 1 | aria-expanded works but focus doesn't restore on Escape |
| Custom Tabs | HAS-BUGS | Pattern Incompleteness | 1 | aria-selected present but no arrow key navigation |
| Custom Tabs | FLAWED | Multi-pattern Gap | 1 | aria-selected + arrow keys present, but active tab not focused; panel not referenced |
| Modal Dialog | CLEAN | Baseline | 1 | Proper role="dialog", aria-modal="true", focus trap, focus restoration |
| Modal Dialog | ADVERSARIAL | Semantic Masking | 1 | Div + ARIA instead of button for modal trigger; role="dialog" correct but trigger semantics wrong |

**Expected findings per component type**:

- **Dropdown**: Focus restoration (MAJOR), selected state announcement (CRITICAL if missing)
- **Tabs**: Arrow key nav (MAJOR), focus management (MAJOR), aria-selected (CRITICAL if missing)
- **Modal**: Focus trap (CRITICAL), focus restoration (MAJOR), semantics of trigger (MINOR if div+ARIA)

**Perspectives covered**: Keyboard (tab/arrow keys), Screen Reader (aria-selected, role, focus management), Cognitive (clear interaction model)

---

## Domain 2: Form & Validation Patterns (5 fixtures)

Form components with state communication challenges.

| Form Type | Difficulty | Issue Class | Count | Notes |
|---|---|---|---|---|
| Login Form | CLEAN | Baseline | 1 | Label associations correct, errors announced + described, required indicated |
| Form with Validation | HAS-BUGS | State Association | 1 | Errors announce (aria-live) but not associated to fields (missing aria-describedby) |
| Complex Form | HAS-BUGS | Field-Level Error Handling | 1 | Error summary exists but doesn't link to specific fields; screen reader user confused |
| Multi-Step Form | FLAWED | Error Recovery & Recovery Messaging | 1 | Error messages specific but no announcement when errors clear; disabled state confusing |
| Dynamic Form | ADVERSARIAL | Live Region Collision | 1 | Multiple validation sources, aria-live regions conflict, user hears duplicate announcements |

**Expected findings per pattern**:

- **Validation**: Missing aria-describedby on inputs (CRITICAL), error association (MAJOR), error summary links (MAJOR)
- **Disabled state**: Using CSS `:disabled` instead of attribute (MINOR), aria-disabled on ARIA widgets (CRITICAL if missing)
- **Dynamic content**: Missing role="status" or aria-live (CRITICAL), announcements not polite/assertive (MAJOR)

**Perspectives covered**: Screen Reader (announcements, associations), Cognitive (error clarity), Keyboard (form navigation, disabled state visibility)

---

## Domain 3: Content & Semantic Structure (5 fixtures)

Proper heading hierarchy, landmark regions, list semantics, table structure.

| Content Type | Difficulty | Issue Class | Count | Notes |
|---|---|---|---|---|
| Landing Page | CLEAN | Baseline | 1 | Proper h1 > h2 hierarchy, landmarks (nav, main, footer), logical reading order |
| Blog Post | HAS-BUGS | Heading Hierarchy | 1 | Skipped heading levels (h1 → h3); landmark structure weak |
| Data Table | HAS-BUGS | Table Semantics | 1 | Missing `<caption>` or `aria-label`; column headers lack scope="col" |
| Complex Dashboard | FLAWED | Multiple Issues | 1 | Heading hierarchy inconsistent; list items in divs; table missing scope attributes; regions not marked |
| E-Commerce Product Page | ADVERSARIAL | False Positive Trap | 1 | Uses `<section>` improperly (not a landmark), but heading hierarchy correct; tests might flag as error but is defensible |

**Expected findings**:

- **Headings**: Skipped levels (MAJOR), missing h1 (MINOR), hierarchy doesn't match visual (MAJOR)
- **Landmarks**: Missing `<main>` (MINOR), missing `<nav>` (MINOR), improperly nested (MAJOR)
- **Tables**: Missing caption (MAJOR), missing scope (MAJOR), complex table missing role attributes (MAJOR)
- **Lists**: Items in divs instead of `<ul>/<li>` (MINOR if nav, MAJOR if contentful list)

**Perspectives covered**: Screen Reader (landmark navigation, reading order), Low Vision (heading anchors, outline view), Cognitive (information hierarchy)

---

## Domain 4: Focus Management & Keyboard Navigation (5 fixtures)

Tab order, skip links, focus indicators, focus restoration, roving tabindex.

| Scenario | Difficulty | Issue Class | Count | Notes |
|---|---|---|---|---|
| Site Navigation | CLEAN | Baseline | 1 | Tab order logical, skip link present, focus indicator visible, no traps |
| Sidebar + Main | HAS-BUGS | Tab Order | 1 | Tab order illogical (sidebar items before main content); skip link missing |
| Nested Menus | HAS-BUGS | Focus Restoration | 1 | Submenu doesn't return focus to parent menu button when Escape pressed |
| Complex App | FLAWED | Multiple Gaps | 1 | Tab order illogical, skip link missing, focus indicator low contrast, roving tabindex not implemented for composite widgets |
| Search Results Page | ADVERSARIAL | Dynamic Content Focus | 1 | Results update dynamically; where should focus go? Ambiguous design intention; test might flag as error but designer chose to leave focus in search box |

**Expected findings**:

- **Tab order**: Illogical order (MAJOR), hidden elements in tab (MAJOR), skipped interactive elements (CRITICAL if unintended)
- **Skip links**: Missing (MINOR/ENHANCEMENT), non-functional (MAJOR), unclear text (MINOR)
- **Focus indicators**: Not visible (CRITICAL), low contrast (MAJOR), removed via CSS (CRITICAL)
- **Focus restoration**: Missing on modal/drawer close (MAJOR), inconsistent (MINOR)
- **Roving tabindex**: Missing on composites like tabs/menus (MAJOR), implementation incomplete (MAJOR)

**Perspectives covered**: Keyboard (100% of navigation), Low Vision (focus visibility), Cognitive (logical tab order reduces confusion)

---

## Domain 5: Dynamic Content & Live Regions (4 fixtures)

Content that appears/disappears, loading states, real-time updates, announcements.

| Scenario | Difficulty | Issue Class | Count | Notes |
|---|---|---|---|---|
| Search Results (Dynamic) | CLEAN | Baseline | 1 | aria-live="polite" on results region, aria-busy on container, loading message announced |
| Loading State | HAS-BUGS | Missing Announcement | 1 | Loading spinner shows visually but no aria-busy or aria-live announcement |
| Chat/Messaging App | HAS-BUGS | Live Region Misconfiguration | 1 | New messages appear but aria-live="assertive" not used; messages announce but hard to follow |
| Async Form Submission | FLAWED | State Communication Gaps | 1 | Success message announced but doesn't specify what succeeded; no confirmation for screen reader user |

**Expected findings**:

- **Live regions**: Missing aria-live (CRITICAL), wrong aria-live value (MAJOR), no aria-busy (MAJOR if loading state)
- **Announcements**: Not specific (MINOR), redundant (MINOR), asynchronous (user expects sync confirmation, MAJOR)
- **Dynamic focus**: Content appears, focus doesn't move (intentional/unintentional, MAJOR if unintentional)

**Perspectives covered**: Screen Reader (100% — live regions are audio-only), Cognitive (clear status messages)

---

## Domain 6: Color, Motion, & Sensory (3 fixtures)

Low vision patterns, high contrast, reduced motion, touch targets.

| Scenario | Difficulty | Issue Class | Count | Notes |
|---|---|---|---|---|
| Status Indicators | CLEAN | Baseline | 1 | Uses color + shape + text; high contrast enforced; 44x44 touch targets |
| Dark Mode Toggle | HAS-BUGS | Color Contrast | 1 | Icon color contrast fails (2:1 vs required 3:1); text label rescues it but icon-only users struggle |
| Animated Carousel | FLAWED | Reduced Motion | 1 | Animation plays on all users; missing prefers-reduced-motion media query |

**Expected findings**:

- **Color**: Insufficient contrast (CRITICAL if text, MAJOR if icon), color-only indication (MAJOR)
- **Touch targets**: Below 44x44 CSS pixels (MAJOR/CRITICAL depending on frequency)
- **Reduced motion**: Missing prefers-reduced-motion media query (ENHANCEMENT if animations are decorative, MAJOR if essential functionality)

**Perspectives covered**: Low Vision (contrast, magnification), Cognitive (color-only indicators confusing)

---

## Difficulty Tier Definitions

| Difficulty | Description | Finder Rate (Baseline) | Finder Rate (A11y-Critic Expected) | Notes |
|---|---|---|---|---|---|
| **CLEAN** | Properly implemented; few/no a11y issues; baseline for skill accuracy | 85-95% | 95-100% | Tests baseline truthfulness; false positive traps |
| **HAS-BUGS** | 1-2 obvious a11y issues; missing ARIA attributes, broken focus management | 40-60% | 75-85% | Baseline should catch some; skill should catch all |
| **FLAWED** | 3-5 issues, some subtle; incomplete patterns, multi-perspective gaps | 15-35% | 60-75% | Gap analysis and multi-perspective shine here |
| **ADVERSARIAL** | Ambiguous or defensive implementation; requires deep understanding of trade-offs | 5-20% | 40-60% | Tests skill's ability to distinguish defensible from broken; high false positive rate acceptable |

---

## Fixture Count by Domain and Difficulty

```
Domain                          | CLEAN | HAS-BUGS | FLAWED | ADVERSARIAL | Total
--------------------------------|-------|----------|--------|-------------|-------
Interactive Widgets             |   1   |    2     |   2    |      1      |   6
Form & Validation               |   1   |    2     |   1    |      1      |   5
Content & Semantic Structure    |   1   |    2     |   1    |      1      |   5
Focus Management                |   1   |    2     |   1    |      1      |   5
Dynamic Content & Live Regions  |   1   |    2     |   1    |      0      |   4
Color, Motion, & Sensory        |   1   |    1     |   1    |      0      |   3
--------------------------------|-------|----------|--------|-------------|-------
TOTAL                           |   6   |    11    |   6    |      4      |   27
```

**Note**: Targeting 27-30 fixtures. If needed, add 1-3 additional fixtures from underrepresented domains (likely from Domain 5-6 if time allows).

---

## Fixture Independence & Avoidance of Dependencies

Each fixture is **independently reviewable**:

- No cross-fixture references
- Each includes standalone component code + metadata
- No "build on previous fixture" patterns
- Metadata includes all context needed for review (framework, intended behavior, etc.)

---

## Coverage of Key WCAG & APG Criteria

| Criterion/Pattern | Covered in Domains | Fixture Count |
|---|---|---|
| 1.3.1 Info & Relationships | 2, 3, 4 | 10 |
| 2.1.1 Keyboard | 1, 4 | 11 |
| 2.1.2 No Keyboard Trap | 1, 4 | 8 |
| 2.4.3 Focus Order | 3, 4 | 8 |
| 2.4.7 Focus Visible | 4, 6 | 7 |
| 2.5.8 Target Size | 6 | 3 |
| 4.1.2 Name, Role, Value | 1, 2, 3 | 13 |
| 4.1.3 Status Messages | 2, 5 | 7 |
| APG: Disclosure | 1 | 2 |
| APG: Menu Button | 1 | 2 |
| APG: Tabs | 1 | 2 |
| APG: Modal | 1 | 2 |
| APG: Live Regions | 5 | 4 |
| APG: Data Table | 3 | 1 |

---

## Perspectives Distribution

| Perspective | Domains | Fixture Count | Notes |
|---|---|---|---|
| Screen Reader | All | 27 | 100% coverage; core to a11y evaluation |
| Keyboard-only | 1, 3, 4 | 16 | Focus, tab order, arrow keys, Escape |
| Low Vision | 4, 6 | 10 | Contrast, zoom/reflow, focus visibility, touch targets |
| Cognitive | 2, 3, 4, 5 | 14 | Error messages, consistency, information hierarchy, status clarity |

---

## Anticipated Fixture Challenges

1. **Interactive Widgets**: Tendency to over-ARIA (adding roles to divs unnecessarily). Adversarial fixture tests this.
2. **Forms**: Common to miss aria-describedby pairing. Multiple HAS-BUGS fixtures test this.
3. **Semantic Structure**: Heading hierarchy gaps subtle; FLAWED fixture has multi-level issues.
4. **Focus Management**: Skip links often forgotten; focus restoration on modals missed. Multiple fixtures target this.
5. **Live Regions**: Most underutilized; baseline likely misses. Skill should shine.
6. **Color/Motion**: Often treated as "nice to have"; adversarial fixture tests if skill conflates MAJOR with ENHANCEMENT.

---

## Pilot Run Selection

Recommended pilot fixtures (5 representative cases):

1. **interactive-dropdown-clean** (CLEAN, baseline truthfulness)
2. **form-validation-missing-aria-describedby** (HAS-BUGS, obvious issue)
3. **modal-dialog-complete** (CLEAN, modal baseline)
4. **tabs-missing-arrow-nav** (HAS-BUGS, incomplete pattern)
5. **live-region-async-updates** (HAS-BUGS, multi-perspective gap)

These 5 cover:
- 2 CLEAN (baseline accuracy)
- 3 HAS-BUGS (skill discrimination)
- 4 of 6 domains
- All 4 perspectives represented
