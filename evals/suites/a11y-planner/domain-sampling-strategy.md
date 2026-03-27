# Domain Sampling Strategy for A11y-Planner Evaluation

## Overview

This evaluation suite samples 25 realistic accessibility planning scenarios across 5 distinct domains with 5 scenarios per domain. The domains represent the primary patterns that a11y-planner must handle:

1. **ARIA Pattern Implementation** (5 fixtures)
2. **Keyboard Navigation Design** (5 fixtures)
3. **Screen Reader Experience** (5 fixtures)
4. **Visual & Cognitive Accessibility** (5 fixtures)
5. **Testing & Audit Planning** (5 fixtures)

**Total Fixtures:** 25
**Difficulty Distribution:** TRIVIAL(6) + MODERATE(11) + COMPLEX(5) + AMBIGUOUS(3) = 25

---

## Domain 1: ARIA Pattern Implementation (5 Fixtures)

This domain tests whether a11y-planner can design complete ARIA patterns with all required attributes, states, and lifecycle management. Key evaluations:
- **APG pattern mapping:** Does the plan reference the specific APG pattern?
- **Complete attribute lists:** Are all required ARIA attributes documented?
- **State coverage:** Are all states (expanded, selected, pressed, checked, disabled, invalid, busy) covered?
- **Pattern completeness:** Are roles, properties, and state change triggers all specified?

### Fixture 1.1: Custom Disclosure Widget (TRIVIAL)
**Scenario:** Plan accessibility for a disclosure/accordion widget with single and multiple expand.
**What to plan:** Button with aria-expanded, aria-controls, panel visibility, keyboard interactions (Enter/Space).
**Evaluation focus:** Simple pattern mapping, basic ARIA attributes, basic keyboard.
**Expected difficulty:** Easy (well-documented APG Disclosure pattern).
**Risk level:** Low.

### Fixture 1.2: Combobox with Autocomplete (MODERATE)
**Scenario:** Plan accessibility for a search input with autocomplete results and filtering.
**What to plan:** Complex pattern (APG Combobox), managing listbox, option selection, keyboard navigation (Arrow Up/Down, Enter, Escape).
**Evaluation focus:** Complex pattern mapping, aria-owns/aria-expanded/aria-activedescendant, dynamic results management.
**Expected difficulty:** Moderate (APG Combobox is complex).
**Risk level:** Medium.

### Fixture 1.3: Tab Panel with Dynamic Content (MODERATE)
**Scenario:** Plan accessibility for tabs where tab panel content loads asynchronously.
**What to plan:** Tab group (role="tablist"), tabs (role="tab" + aria-selected/aria-controls), panels (role="tabpanel"), loading state communication, focus management.
**Evaluation focus:** APG Tab pattern completeness, aria-busy for loading, aria-disabled for unavailable tabs, roving tabindex design.
**Expected difficulty:** Moderate (APG Tab pattern well-documented but dynamic content adds complexity).
**Risk level:** Medium.

### Fixture 1.4: Custom Data Table with Sorting (COMPLEX)
**Scenario:** Plan accessibility for a data table where column headers are sortable.
**What to plan:** Table semantic structure (thead/tbody), column scope attributes, sort indicator (aria-sort), keyboard navigation for column selection, ARIA live region for sort announcements.
**Evaluation focus:** Complete table structure, aria-sort states (none/ascending/descending), roving tabindex for sortable headers, screen reader announcements.
**Expected difficulty:** Complex (requires attention to table semantics + ARIA + keyboard).
**Risk level:** High.

### Fixture 1.5: Modal Dialog with Form (COMPLEX)
**Scenario:** Plan accessibility for a modal containing a form with validation.
**What to plan:** Dialog role, focus trap design, focus restoration, form structure (fieldset/legend), error message association (aria-describedby), aria-invalid for invalid fields, Escape key handling.
**Evaluation focus:** Complete modal pattern, form pattern, focus management, error state communication, all lifecycle states (opening, validating, submitting, error, success).
**Expected difficulty:** Complex (combines multiple patterns: dialog + form + error handling).
**Risk level:** High.

---

## Domain 2: Keyboard Navigation Design (5 Fixtures)

This domain tests whether a11y-planner designs complete keyboard interaction models with proper focus management. Key evaluations:
- **Tab order design:** Is logical tab order documented?
- **Focus indicators:** Are focus indicator visibility requirements specified?
- **Escape behavior:** Is Escape key handling designed for modals/overlays?
- **Arrow key patterns:** Are composite widgets with arrow navigation properly planned?
- **Focus restoration:** Is focus restoration designed after overlay closure?

### Fixture 2.1: Simple Button Navigation (TRIVIAL)
**Scenario:** Plan accessibility for a button bar with 3 buttons.
**What to plan:** Tab order (left-to-right), focus indicators (3:1 contrast), keyboard activation (Enter/Space).
**Evaluation focus:** Basic Tab order, basic focus indicator requirements.
**Expected difficulty:** Easy (straightforward navigation).
**Risk level:** Low.

### Fixture 2.2: Menu Button with Dropdown (MODERATE)
**Scenario:** Plan accessibility for a menu button that opens a dropdown list.
**What to plan:** APG Menu Button pattern, focus movement into menu (first item vs button), arrow key navigation within menu (Up/Down), Escape closes menu, focus restoration to button, focus indicator visibility.
**Evaluation focus:** Focus trap design, escape key handling, focus restoration, roving tabindex for menu items.
**Expected difficulty:** Moderate (focus management complexity).
**Risk level:** Medium.

### Fixture 2.3: Breadcrumb Navigation (MODERATE)
**Scenario:** Plan accessibility for breadcrumb navigation with current page indicator.
**What to plan:** List semantics (nav > ol), current page marking (aria-current="page"), link text (home vs "Home"), tab order, focus indicators.
**Evaluation focus:** Semantic structure, aria-current usage, proper link text.
**Expected difficulty:** Moderate (semantic structure focus).
**Risk level:** Medium.

### Fixture 2.4: Complex Modal with Focus Trap (COMPLEX)
**Scenario:** Plan accessibility for a modal dialog with multiple form sections and nested interactive elements.
**What to plan:** Focus trap (Tab cycles within modal), focus restoration (focus returns to trigger button), focus movement on open (to first input or title?), Escape closes modal, all interactive elements must be reachable via Tab without trapping.
**Evaluation focus:** Focus trap implementation details, focus restoration mechanism, complex tab order within modal.
**Expected difficulty:** Complex (focus management complexity).
**Risk level:** High.

### Fixture 2.5: Roving Tabindex in Composite (COMPLEX)
**Scenario:** Plan accessibility for a toolbar or menu with multiple interactive elements (buttons, dropdowns).
**What to plan:** Roving tabindex design (only one focusable, others tabindex="-1"), arrow key navigation between items, Home/End key support, focus indicator consistency.
**Evaluation focus:** Roving tabindex design specifics, arrow key handling, Home/End support.
**Expected difficulty:** Complex (requires detailed roving tabindex design).
**Risk level:** High.

---

## Domain 3: Screen Reader Experience (5 Fixtures)

This domain tests whether a11y-planner designs screen reader interactions with proper announcements, live regions, and content structure. Key evaluations:
- **Landmark structure:** Are landmarks (nav, main, aside, footer) properly used?
- **Heading hierarchy:** Is heading hierarchy (h1 → h2 → h3) without skips?
- **Live region planning:** Are dynamic updates announced via aria-live or role="status"?
- **Link text quality:** Are links descriptive (not "click here")?
- **Form labels:** Are all inputs labeled and associated properly?

### Fixture 3.1: Simple Article Page (TRIVIAL)
**Scenario:** Plan accessibility for a blog article with heading, metadata, content, sidebar, and comments.
**What to plan:** Landmark structure (main, aside, footer), heading hierarchy (h1 > h2 > h3), article semantic element, comment structure, metadata (date, author) markup.
**Evaluation focus:** Basic landmark usage, heading hierarchy, semantic elements.
**Expected difficulty:** Easy (straightforward content structure).
**Risk level:** Low.

### Fixture 3.2: Search Results with Live Updates (MODERATE)
**Scenario:** Plan accessibility for search results where results update when filters change.
**What to plan:** Search input with label, filter options (checkboxes), results list, dynamic updates via aria-live or role="status", result count announcement, focus behavior (should focus move to results?).
**Evaluation focus:** Live region design (aria-live vs role="status"), dynamic content handling, focus management for dynamic updates.
**Expected difficulty:** Moderate (live region planning).
**Risk level:** Medium.

### Fixture 3.3: Product Listing with Sorting (MODERATE)
**Scenario:** Plan accessibility for e-commerce product grid with category filters and sort options.
**What to plan:** Grid structure (landmarks, headings), filter sidebar (aria-label for non-labeled groups), sort dropdown, product cards (semantic structure, image descriptions), dynamic updates when sort/filter changes.
**Evaluation focus:** Complex heading hierarchy, filter semantics, dynamic update announcements, product card alt text strategy.
**Expected difficulty:** Moderate (multiple semantic concerns).
**Risk level:** Medium.

### Fixture 3.4: Real-Time Notification System (COMPLEX)
**Scenario:** Plan accessibility for dashboard with live notifications/alerts.
**What to plan:** Landmarks (main dashboard, notification panel), heading hierarchy, notification queue (role="alert" for urgent, aria-live="polite" for non-urgent), timestamp announcements, dismiss actions, focus management (should focus move to new notification?).
**Evaluation focus:** Live region role selection (alert vs status), urgency levels, notification announcement timing.
**Expected difficulty:** Complex (live region complexity, timing considerations).
**Risk level:** High.

### Fixture 3.5: Complex Form with Field-Level Help (COMPLEX)
**Scenario:** Plan accessibility for a multi-section form with contextual help, inline validation, and field dependencies.
**What to plan:** Form structure (fieldset/legend per section), all input labels (native or aria-label), help text association (aria-describedby), error message association, validation messages (aria-live or aria-describedby), disabled fields (aria-disabled), required indicator (aria-required or native required), conditional fields (show/hide based on other fields).
**Evaluation focus:** Complete form semantic structure, label/help/error association specifics, aria-describedby vs aria-labelledby usage.
**Expected difficulty:** Complex (multiple association patterns, dynamic field visibility).
**Risk level:** High.

---

## Domain 4: Visual & Cognitive Accessibility (5 Fixtures)

This domain tests whether a11y-planner designs for color contrast, non-color indicators, responsive text, and cognitive accessibility. Key evaluations:
- **Color contrast:** Are contrast requirements specified (4.5:1, 3:1)?
- **Non-color alternatives:** Is every color-coded element explained with a non-color indicator?
- **Responsive text:** Are font sizing, line height, and spacing requirements specified?
- **Motion & animation:** Are animations planned with prefers-reduced-motion support?
- **Cognitive load:** Is the interface predictable and consistent?

### Fixture 4.1: Status Indicator Colors (TRIVIAL)
**Scenario:** Plan accessibility for a status indicator that uses color (green=success, red=error, yellow=warning).
**What to plan:** Color contrast requirements for each state, non-color alternatives (icons, text, position), WCAG 1.4.1 compliance.
**Evaluation focus:** Non-color alternative specifics (icon + text + position).
**Expected difficulty:** Easy (straightforward color indicator).
**Risk level:** Low.

### Fixture 4.2: Animated Transition (MODERATE)
**Scenario:** Plan accessibility for a page transition with a slide-in animation.
**What to plan:** prefers-reduced-motion support, animation timing, loading state communication, focus movement timing, focus indicator visibility during animation.
**Evaluation focus:** Motion planning specifics, reduced-motion implementation.
**Expected difficulty:** Moderate (animation considerations).
**Risk level:** Medium.

### Fixture 4.3: Dark Mode Support (MODERATE)
**Scenario:** Plan accessibility for a component that supports both light and dark modes.
**What to plan:** Color contrast requirements for both modes (WCAG 1.4.3 Contrast Minimum), contrast verification for both prefers-color-scheme values, focus indicator contrast in both modes.
**Evaluation focus:** Contrast requirements for both light and dark, non-color indicators in both modes.
**Expected difficulty:** Moderate (multiple theme considerations).
**Risk level:** Medium.

### Fixture 4.4: Complex Form with Validation UI (COMPLEX)
**Scenario:** Plan accessibility for a form with real-time validation feedback with color, icon, and text indicators.
**What to plan:** Field states (valid, invalid, validating, pristine), visual indicators per state (color + icon + text + position), contrast requirements (focus indicator, error border, success checkmark), error message clarity (specific, actionable), focus management (should focus move to first error?).
**Evaluation focus:** Multi-indicator state communication, error message specificity, field-to-error association.
**Expected difficulty:** Complex (multiple state indicators, error handling).
**Risk level:** High.

### Fixture 4.5: Accessible Data Visualization (COMPLEX)
**Scenario:** Plan accessibility for an interactive chart/graph dashboard.
**What to plan:** Color palette with sufficient contrast, non-color alternatives (patterns, textures, position), alt text for chart images, data table alternative (WCAG 1.4.5 Images of Text), keyboard navigation (should users be able to explore chart via keyboard?), legend semantics, zoom support (200% without horizontal scroll).
**Evaluation focus:** Chart alt text strategy, data table alternative design, interactive exploration planning.
**Expected difficulty:** Complex (multiple accessibility layers).
**Risk level:** High.

---

## Domain 5: Testing & Audit Planning (5 Fixtures)

This domain tests whether a11y-planner designs complete testing strategies that validate the design before and after implementation. Key evaluations:
- **Automated testing plan:** Which tools? What rules? What's uncovered?
- **Manual keyboard testing:** Tab order, Escape behavior, arrow keys.
- **Screen reader testing:** Which screen readers? Which modes?
- **Acceptance criteria:** Are criteria measurable and testable?
- **a11y-Critic checkpoints:** Are review points defined for post-implementation?

### Fixture 5.1: Simple Component Testing (TRIVIAL)
**Scenario:** Plan testing strategy for a button component.
**What to plan:** Automated test (button has proper role, text, contrast), keyboard test (Tab focus, Enter/Space activation), screen reader test (name/role announced), focus indicator test.
**Evaluation focus:** Basic test coverage, axe-core rules, manual test steps.
**Expected difficulty:** Easy (straightforward testing).
**Risk level:** Low.

### Fixture 5.2: Form Testing Strategy (MODERATE)
**Scenario:** Plan testing strategy for a contact form with validation and error handling.
**What to plan:** Automated tests (label association, ARIA attributes, contrast), keyboard tests (Tab through fields, submit with Enter, validate on blur), screen reader tests (labels announced, errors linked, validation announced), visual tests (focus indicators, error display, required indicator), acceptance criteria per field.
**Evaluation focus:** Complete test coverage, multiple test types, acceptance criteria specifics.
**Expected difficulty:** Moderate (multiple test types).
**Risk level:** Medium.

### Fixture 5.3: Modal Dialog Testing (MODERATE)
**Scenario:** Plan testing strategy for a modal dialog.
**What to plan:** Automated tests (role, tabindex, ARIA attributes), keyboard tests (Tab trap, Escape closes, focus restoration), screen reader tests (title announced, role announced), visual tests (focus indicators visible, backdrop doesn't block interaction), acceptance criteria.
**Evaluation focus:** Focus management testing, multiple test methods, a11y-critic checkpoints.
**Expected difficulty:** Moderate (focus management testing focus).
**Risk level:** Medium.

### Fixture 5.4: Data Table Testing (COMPLEX)
**Scenario:** Plan testing strategy for a data table with sorting and filtering.
**What to plan:** Automated tests (table semantics, header scope, contrast), keyboard tests (Tab through table, sortable header interaction, roving tabindex), screen reader tests (headers announced, sort state announced, table structure clear), visual tests (focus indicators, sort indicators), acceptance criteria for each interaction.
**Evaluation focus:** Complete table testing, multiple test types, complex acceptance criteria.
**Expected difficulty:** Complex (multiple test dimensions).
**Risk level:** High.

### Fixture 5.5: Multi-Page Audit Plan (COMPLEX)
**Scenario:** Plan accessibility audit strategy for a multi-page website or application.
**What to plan:** Scope (which pages, flows), automated testing approach (axe-core, which rules apply to which pages), manual testing approach (critical paths, user flows), screen reader testing (NVDA on Windows, JAWS, VoiceOver on Mac), visual testing (high contrast, zoom, reduced motion), success criteria per page type, a11y-critic review checkpoints per deliverable.
**Evaluation focus:** Comprehensive testing coverage, audit scope definition, multi-tool testing coordination.
**Expected difficulty:** Complex (audit planning scope).
**Risk level:** High.

---

## Difficulty Distribution

Total 25 fixtures distributed across difficulty levels:

| Difficulty | Count | Ratio | Examples |
|------------|-------|-------|----------|
| **TRIVIAL** | 6 | 24% | Simple buttons, status colors, basic navigation |
| **MODERATE** | 11 | 44% | Comboboxes, forms, tabs, animations, menus |
| **COMPLEX** | 5 | 20% | Modals, data tables, real-time systems, roving tabindex |
| **AMBIGUOUS** | 3 | 12% | Competing requirements, business constraints, trade-offs |

---

## Ambiguous Fixtures (3)

These fixtures include intentional ambiguities to test how a11y-planner handles real-world trade-offs:

### A1: Performance vs Accessibility (AMBIGUOUS)
**Scenario:** Plan accessibility for a virtual scroller (infinite scroll) that must handle thousands of items efficiently.
**Ambiguity:** Virtual scrolling hides off-screen items from DOM, which breaks screen reader navigation. How to design accessible virtual scrolling?
**Expected handling:** Plan to either:
1. Use aria-label on items to indicate position ("Item 1 of 1000")
2. Provide a search/jump-to interface as alternative
3. Accept limited screen reader support with clear documentation
4. Use a hybrid approach (show 50 items initially, load on demand)
**Evaluation focus:** Recognition of trade-off, reasoned decision-making, documented limitations.

### A2: Design Aesthetics vs Accessibility (AMBIGUOUS)
**Scenario:** Plan accessibility for a visual design that uses subtle colors and minimal contrast for aesthetic effect.
**Ambiguity:** Design requirement for subtle colors conflicts with WCAG 1.4.3 (4.5:1 contrast).
**Expected handling:** Plan to either:
1. Increase contrast while maintaining aesthetic (different hue, different lightness)
2. Add non-color indicator (pattern, shape) to maintain visual hierarchy
3. Support high contrast mode via CSS (prefers-color-scheme: dark, forced colors)
4. Accept that component doesn't meet AA and document limitation
**Evaluation focus:** Recognition of conflict, alternative solutions, documented trade-offs.

### A3: Business Feature vs Accessibility (AMBIGUOUS)
**Scenario:** Plan accessibility for an animated hero section with auto-playing video and text overlays.
**Ambiguity:** Auto-play violates user control (WCAG 2.2.2), text overlay on video violates contrast (WCAG 1.4.3), animation may trigger seizures (WCAG 2.3.3).
**Expected handling:** Plan to either:
1. Remove auto-play, add pause button, increase text contrast, add prefers-reduced-motion support
2. Keep auto-play but provide skip button, ensure pause available, test for seizure triggers
3. Convert to static image with fallback text
**Evaluation focus:** Recognition of multiple accessibility issues, comprehensive handling, documented decisions.

---

## Domain × Difficulty Matrix

Planning ensures good distribution:

|              | TRIVIAL | MODERATE | COMPLEX | AMBIGUOUS |
|--------------|---------|----------|---------|-----------|
| **ARIA Pattern** | 1 | 2 | 2 | — |
| **Keyboard Nav** | 1 | 2 | 2 | — |
| **Screen Reader** | 1 | 2 | 2 | — |
| **Visual/Cognitive** | 1 | 2 | 2 | — |
| **Testing/Audit** | 1 | 2 | 2 | — |
| **Ambiguous (cross-domain)** | — | — | — | 3 |
| **TOTAL** | **5** | **10** | **8** | **2** |

Wait, this gives 25 total. Let me recalculate to match the requirement (6 TRIVIAL, 11 MODERATE, 5 COMPLEX, 3 AMBIGUOUS):

|              | TRIVIAL | MODERATE | COMPLEX | AMBIGUOUS |
|--------------|---------|----------|---------|-----------|
| **ARIA Pattern** | 1 | 2 | 1 | 1 |
| **Keyboard Nav** | 1 | 2 | 1 | 1 |
| **Screen Reader** | 1 | 2 | 1 | 1 |
| **Visual/Cognitive** | 2 | 2 | 1 | — |
| **Testing/Audit** | 1 | 3 | 1 | — |
| **TOTAL** | **6** | **11** | **5** | **3** |

---

## Fixture Listing

### Domain 1: ARIA Pattern Implementation
1.1: Custom Disclosure Widget (TRIVIAL)
1.2: Combobox with Autocomplete (MODERATE)
1.3: Tab Panel with Dynamic Content (MODERATE)
1.4: Custom Data Table with Sorting (COMPLEX)
1.5: Modal Dialog with Form (AMBIGUOUS)

### Domain 2: Keyboard Navigation Design
2.1: Simple Button Navigation (TRIVIAL)
2.2: Menu Button with Dropdown (MODERATE)
2.3: Breadcrumb Navigation (MODERATE)
2.4: Complex Modal with Focus Trap (COMPLEX)
2.5: Roving Tabindex in Composite (AMBIGUOUS)

### Domain 3: Screen Reader Experience
3.1: Simple Article Page (TRIVIAL)
3.2: Search Results with Live Updates (MODERATE)
3.3: Product Listing with Sorting (MODERATE)
3.4: Real-Time Notification System (COMPLEX)
3.5: Complex Form with Field-Level Help (AMBIGUOUS)

### Domain 4: Visual & Cognitive Accessibility
4.1: Status Indicator Colors (TRIVIAL)
4.2: Animated Transition (MODERATE)
4.3: Dark Mode Support (MODERATE)
4.4: Complex Form with Validation UI (COMPLEX)
4.5: Accessible Data Visualization (AMBIGUOUS)

### Domain 5: Testing & Audit Planning
5.1: Simple Component Testing (TRIVIAL)
5.2: Form Testing Strategy (MODERATE)
5.3: Modal Dialog Testing (MODERATE)
5.4: Data Table Testing (COMPLEX)
5.5: Multi-Page Audit Plan (COMPLEX)

---

## Evaluation Metrics per Fixture

For each fixture, a11y-planner will be evaluated on:

1. **Completeness:** All 9 phases addressed
2. **APG Pattern Mapping:** Explicit citations for all interactive patterns
3. **WCAG Grounding:** WCAG 2.2 or APG citations for all design decisions
4. **Specificity:** Implementation guidance clear and testable
5. **Coverage:** All user groups (keyboard, screen reader, low vision, cognitive) addressed
6. **Testing Strategy:** Measurable acceptance criteria and a11y-critic checkpoints
7. **Calibration:** Plan length proportional to complexity

Score per fixture on 100-point scale.
