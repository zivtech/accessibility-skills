# A11y-Planner Fixture Inventory

**Total Fixtures:** 25 (25 .md + 25 .metadata.yaml + 25 .rubric.yaml = 75 files)

---

## Domain 1: ARIA Pattern Implementation (5 fixtures)

### 1.1 aria-disclosure-widget
- **Name:** Custom Disclosure Widget
- **Difficulty:** TRIVIAL
- **Risk:** Low
- **Scenario:** Plan accessibility for a disclosure/accordion widget with single and multiple expand options
- **Key a11y concerns:** APG Disclosure pattern, aria-expanded, aria-controls, button interaction
- **Expected plan length:** 1-2 pages
- **Files:**
  - `fixtures/aria-disclosure-widget.md`
  - `fixtures/aria-disclosure-widget.metadata.yaml`
  - `rubrics/aria-disclosure-widget.rubric.yaml`

### 1.2 aria-combobox-autocomplete
- **Name:** Combobox with Autocomplete
- **Difficulty:** MODERATE
- **Risk:** Medium
- **Scenario:** Plan accessibility for a search input with autocomplete results and filtering
- **Key a11y concerns:** APG Combobox pattern, aria-owns, aria-expanded, aria-activedescendant, dynamic listbox, keyboard navigation (Arrow Up/Down, Enter, Escape)
- **Expected plan length:** 3-5 pages
- **Files:**
  - `fixtures/aria-combobox-autocomplete.md`
  - `fixtures/aria-combobox-autocomplete.metadata.yaml`
  - `rubrics/aria-combobox-autocomplete.rubric.yaml`

### 1.3 aria-tab-dynamic-content
- **Name:** Tab Panel with Dynamic Content
- **Difficulty:** MODERATE
- **Risk:** Medium
- **Scenario:** Plan accessibility for tabs where tab panel content loads asynchronously
- **Key a11y concerns:** APG Tab pattern, role="tablist", role="tab", role="tabpanel", aria-selected, aria-controls, aria-busy for loading, roving tabindex, focus management
- **Expected plan length:** 3-5 pages
- **Files:**
  - `fixtures/aria-tab-dynamic-content.md`
  - `fixtures/aria-tab-dynamic-content.metadata.yaml`
  - `rubrics/aria-tab-dynamic-content.rubric.yaml`

### 1.4 aria-data-table-sorting
- **Name:** Custom Data Table with Sorting
- **Difficulty:** COMPLEX
- **Risk:** High
- **Scenario:** Plan accessibility for a data table where column headers are sortable
- **Key a11y concerns:** Table semantics (thead/tbody/tfoot), column scope, aria-sort (none/ascending/descending), roving tabindex for sortable headers, aria-live for sort announcements, keyboard navigation, caption
- **Expected plan length:** 6-10 pages
- **Files:**
  - `fixtures/aria-data-table-sorting.md`
  - `fixtures/aria-data-table-sorting.metadata.yaml`
  - `rubrics/aria-data-table-sorting.rubric.yaml`

### 1.5 aria-modal-form-validation
- **Name:** Modal Dialog with Form
- **Difficulty:** AMBIGUOUS
- **Risk:** High
- **Scenario:** Plan accessibility for a modal containing a form with validation
- **Key a11y concerns:** Dialog role, focus trap, focus restoration, form structure (fieldset/legend), error message association (aria-describedby), aria-invalid for invalid fields, Escape key handling, form submission, success/error state communication
- **Ambiguity:** Should focus move to first error or first field? Should form error be announced immediately or only on submit? How to communicate loading state during submission?
- **Expected plan length:** 6-10 pages
- **Files:**
  - `fixtures/aria-modal-form-validation.md`
  - `fixtures/aria-modal-form-validation.metadata.yaml`
  - `rubrics/aria-modal-form-validation.rubric.yaml`

---

## Domain 2: Keyboard Navigation Design (5 fixtures)

### 2.1 keyboard-button-bar
- **Name:** Simple Button Navigation
- **Difficulty:** TRIVIAL
- **Risk:** Low
- **Scenario:** Plan accessibility for a button bar with 3 buttons
- **Key a11y concerns:** Tab order (left-to-right), focus indicators (3:1 contrast), keyboard activation (Enter/Space), skip link (if at top of page)
- **Expected plan length:** 1-2 pages
- **Files:**
  - `fixtures/keyboard-button-bar.md`
  - `fixtures/keyboard-button-bar.metadata.yaml`
  - `rubrics/keyboard-button-bar.rubric.yaml`

### 2.2 keyboard-menu-dropdown
- **Name:** Menu Button with Dropdown
- **Difficulty:** MODERATE
- **Risk:** Medium
- **Scenario:** Plan accessibility for a menu button that opens a dropdown list
- **Key a11y concerns:** APG Menu Button pattern, focus management (should focus move into menu or stay on button?), arrow key navigation within menu (Up/Down, Escape closes), focus restoration to button, roving tabindex, focus indicator visibility
- **Expected plan length:** 3-5 pages
- **Files:**
  - `fixtures/keyboard-menu-dropdown.md`
  - `fixtures/keyboard-menu-dropdown.metadata.yaml`
  - `rubrics/keyboard-menu-dropdown.rubric.yaml`

### 2.3 keyboard-breadcrumb
- **Name:** Breadcrumb Navigation
- **Difficulty:** MODERATE
- **Risk:** Medium
- **Scenario:** Plan accessibility for breadcrumb navigation with current page indicator
- **Key a11y concerns:** List semantics (nav > ol), link text (descriptive, not "Home" if it's a link), current page marking (aria-current="page"), tab order, focus indicators, skip link placement
- **Expected plan length:** 2-3 pages
- **Files:**
  - `fixtures/keyboard-breadcrumb.md`
  - `fixtures/keyboard-breadcrumb.metadata.yaml`
  - `rubrics/keyboard-breadcrumb.rubric.yaml`

### 2.4 keyboard-modal-focus-trap
- **Name:** Complex Modal with Focus Trap
- **Difficulty:** COMPLEX
- **Risk:** High
- **Scenario:** Plan accessibility for a modal dialog with multiple form sections and nested interactive elements
- **Key a11y concerns:** Focus trap implementation (Tab cycles within modal), focus restoration (focus returns to trigger button), focus movement on open (to first input, h1, or button?), Escape closes modal, all interactive elements reachable via Tab, inert elements outside modal
- **Expected plan length:** 6-10 pages
- **Files:**
  - `fixtures/keyboard-modal-focus-trap.md`
  - `fixtures/keyboard-modal-focus-trap.metadata.yaml`
  - `rubrics/keyboard-modal-focus-trap.rubric.yaml`

### 2.5 keyboard-roving-tabindex
- **Name:** Roving Tabindex in Composite
- **Difficulty:** AMBIGUOUS
- **Risk:** High
- **Scenario:** Plan accessibility for a toolbar or menu with multiple interactive elements (buttons, dropdowns, checkboxes)
- **Key a11y concerns:** Roving tabindex design (only one focusable, others tabindex="-1"), arrow key navigation between items, Home/End key support, focus indicator consistency, which direction? (horizontal vs vertical)
- **Ambiguity:** Should arrow keys move horizontally or vertically? Should Home/End cycle through all items or jump to start/end of row? How to handle nested items (button with submenu)?
- **Expected plan length:** 6-10 pages
- **Files:**
  - `fixtures/keyboard-roving-tabindex.md`
  - `fixtures/keyboard-roving-tabindex.metadata.yaml`
  - `rubrics/keyboard-roving-tabindex.rubric.yaml`

---

## Domain 3: Screen Reader Experience (5 fixtures)

### 3.1 sr-article-page
- **Name:** Simple Article Page
- **Difficulty:** TRIVIAL
- **Risk:** Low
- **Scenario:** Plan accessibility for a blog article with heading, metadata (date, author), content, sidebar, and comments
- **Key a11y concerns:** Landmark structure (main, aside, footer), heading hierarchy (h1 > h2 > h3), article semantic element, metadata markup (time, rel), comment thread structure, skip link
- **Expected plan length:** 1-2 pages
- **Files:**
  - `fixtures/sr-article-page.md`
  - `fixtures/sr-article-page.metadata.yaml`
  - `rubrics/sr-article-page.rubric.yaml`

### 3.2 sr-search-results-live
- **Name:** Search Results with Live Updates
- **Difficulty:** MODERATE
- **Risk:** Medium
- **Scenario:** Plan accessibility for search results where results update when filters change (no page reload)
- **Key a11y concerns:** Search input with associated label, filter options (checkboxes/radios in fieldset), results list, live region for dynamic updates (aria-live vs role="status"), result count announcement, focus behavior (should focus move to results or stay in filter?), landmark regions
- **Expected plan length:** 3-5 pages
- **Files:**
  - `fixtures/sr-search-results-live.md`
  - `fixtures/sr-search-results-live.metadata.yaml`
  - `rubrics/sr-search-results-live.rubric.yaml`

### 3.3 sr-product-listing
- **Name:** Product Listing with Sorting
- **Difficulty:** MODERATE
- **Risk:** Medium
- **Scenario:** Plan accessibility for e-commerce product grid with category filters and sort options
- **Key a11y concerns:** Grid layout as semantic list (ul > li), filter sidebar (fieldset/legend for grouped filters), sort dropdown (select or custom), product cards (heading + price + image + button), image alt text strategy, dynamic updates when sort/filter changes, aria-live announcement
- **Expected plan length:** 3-5 pages
- **Files:**
  - `fixtures/sr-product-listing.md`
  - `fixtures/sr-product-listing.metadata.yaml`
  - `rubrics/sr-product-listing.rubric.yaml`

### 3.4 sr-notification-system
- **Name:** Real-Time Notification System
- **Difficulty:** COMPLEX
- **Risk:** High
- **Scenario:** Plan accessibility for dashboard with live notifications/alerts appearing in real-time
- **Key a11y concerns:** Landmark regions (main dashboard, notification panel), heading hierarchy, notification queue, notification role (role="alert" for urgent, aria-live="polite" for non-urgent), timestamp announcements, dismiss action, focus behavior (should focus move to new notification?), notification grouping
- **Expected plan length:** 6-10 pages
- **Files:**
  - `fixtures/sr-notification-system.md`
  - `fixtures/sr-notification-system.metadata.yaml`
  - `rubrics/sr-notification-system.rubric.yaml`

### 3.5 sr-form-field-help
- **Name:** Complex Form with Field-Level Help
- **Difficulty:** AMBIGUOUS
- **Risk:** High
- **Scenario:** Plan accessibility for a multi-section form with contextual help, inline validation, and conditional field visibility
- **Key a11y concerns:** Form structure (fieldset/legend per section), all input labels (native or aria-label), help text association (aria-describedby), error message association and specificity, validation messages (aria-live or aria-describedby?), disabled fields (aria-disabled or native disabled?), required indicator (aria-required or native required?), conditional fields (show/hide based on other fields affects screen reader perception)
- **Ambiguity:** Should help text always be available to screen readers or only on focus? Should required field be marked visually and programmatically? How to handle conditional field visibility (aria-hidden? removed from DOM? aria-disabled)?
- **Expected plan length:** 6-10 pages
- **Files:**
  - `fixtures/sr-form-field-help.md`
  - `fixtures/sr-form-field-help.metadata.yaml`
  - `rubrics/sr-form-field-help.rubric.yaml`

---

## Domain 4: Visual & Cognitive Accessibility (5 fixtures)

### 4.1 visual-status-colors
- **Name:** Status Indicator Colors
- **Difficulty:** TRIVIAL
- **Risk:** Low
- **Scenario:** Plan accessibility for a status indicator that uses color (green=success, red=error, yellow=warning)
- **Key a11y concerns:** Color contrast (WCAG 1.4.3), non-color alternatives (icon + text + position), WCAG 1.4.1 (color not sole indicator)
- **Expected plan length:** 1-2 pages
- **Files:**
  - `fixtures/visual-status-colors.md`
  - `fixtures/visual-status-colors.metadata.yaml`
  - `rubrics/visual-status-colors.rubric.yaml`

### 4.2 visual-animated-transition
- **Name:** Animated Transition
- **Difficulty:** MODERATE
- **Risk:** Medium
- **Scenario:** Plan accessibility for a page transition with a slide-in animation
- **Key a11y concerns:** prefers-reduced-motion support (WCAG 2.3.3), animation duration and timing, loading state communication during animation, focus movement timing (before/after animation?), focus indicator visibility during animation, content appears before animation completes (so screen readers see it)
- **Expected plan length:** 2-3 pages
- **Files:**
  - `fixtures/visual-animated-transition.md`
  - `fixtures/visual-animated-transition.metadata.yaml`
  - `rubrics/visual-animated-transition.rubric.yaml`

### 4.3 visual-dark-mode
- **Name:** Dark Mode Support
- **Difficulty:** MODERATE
- **Risk:** Medium
- **Scenario:** Plan accessibility for a component that supports both light and dark modes
- **Key a11y concerns:** Color contrast requirements for both light and dark (WCAG 1.4.3 Contrast Minimum), prefers-color-scheme support, focus indicator contrast in both modes, non-color indicators work in both modes, testing in high contrast mode
- **Expected plan length:** 2-3 pages
- **Files:**
  - `fixtures/visual-dark-mode.md`
  - `fixtures/visual-dark-mode.metadata.yaml`
  - `rubrics/visual-dark-mode.rubric.yaml`

### 4.4 visual-form-validation
- **Name:** Complex Form with Validation UI
- **Difficulty:** COMPLEX
- **Risk:** High
- **Scenario:** Plan accessibility for a form with real-time validation feedback with color, icon, and text indicators
- **Key a11y concerns:** Field states (valid, invalid, validating, pristine), visual indicators per state (color + icon + text + position), color contrast (all states, focus indicator), error message clarity (specific, actionable), error message association (aria-describedby), field marking as invalid (aria-invalid), focus management (should focus move to first error?), visual feedback timing
- **Expected plan length:** 6-10 pages
- **Files:**
  - `fixtures/visual-form-validation.md`
  - `fixtures/visual-form-validation.metadata.yaml`
  - `rubrics/visual-form-validation.rubric.yaml`

### 4.5 visual-data-viz
- **Name:** Accessible Data Visualization
- **Difficulty:** AMBIGUOUS
- **Risk:** High
- **Scenario:** Plan accessibility for an interactive chart/graph dashboard with multiple data visualizations
- **Key a11y concerns:** Color palette with sufficient contrast (all colors, focus indicator), non-color alternatives (patterns, textures, position, shape), alt text for chart images, data table alternative (WCAG 1.4.5 Images of Text), keyboard navigation (should users explore chart via keyboard? how?), legend semantics, zoom support (200% without horizontal scroll), animation in charts (prefers-reduced-motion)
- **Ambiguity:** Is interactive chart exploration required for accessibility or is data table alternative sufficient? What's the keyboard interaction model for exploring a multi-series chart?
- **Expected plan length:** 6-10 pages
- **Files:**
  - `fixtures/visual-data-viz.md`
  - `fixtures/visual-data-viz.metadata.yaml`
  - `rubrics/visual-data-viz.rubric.yaml`

---

## Domain 5: Testing & Audit Planning (5 fixtures)

### 5.1 test-simple-button
- **Name:** Simple Component Testing
- **Difficulty:** TRIVIAL
- **Risk:** Low
- **Scenario:** Plan testing strategy for a button component
- **Key a11y concerns:** Automated test (button has proper role, text, contrast via axe-core), keyboard test (Tab focus, Enter/Space activation), screen reader test (name/role announced), focus indicator test
- **Expected plan length:** 1-2 pages
- **Files:**
  - `fixtures/test-simple-button.md`
  - `fixtures/test-simple-button.metadata.yaml`
  - `rubrics/test-simple-button.rubric.yaml`

### 5.2 test-form
- **Name:** Form Testing Strategy
- **Difficulty:** MODERATE
- **Risk:** Medium
- **Scenario:** Plan testing strategy for a contact form with validation and error handling
- **Key a11y concerns:** Automated tests (label association, ARIA attributes, contrast via axe-core), keyboard tests (Tab through fields, submit with Enter, blur validation), screen reader tests (labels announced, errors linked and announced, validation messages), visual tests (focus indicators, error display, required indicator), acceptance criteria per field
- **Expected plan length:** 3-4 pages
- **Files:**
  - `fixtures/test-form.md`
  - `fixtures/test-form.metadata.yaml`
  - `rubrics/test-form.rubric.yaml`

### 5.3 test-modal
- **Name:** Modal Dialog Testing
- **Difficulty:** MODERATE
- **Risk:** Medium
- **Scenario:** Plan testing strategy for a modal dialog (with form inside)
- **Key a11y concerns:** Automated tests (role="dialog", tabindex, ARIA attributes via axe-core), keyboard tests (Tab trap, Escape closes, focus restoration), screen reader tests (title/description announced, role announced, inert background), visual tests (focus indicators visible, backdrop doesn't block interaction), acceptance criteria for each interaction
- **Expected plan length:** 3-4 pages
- **Files:**
  - `fixtures/test-modal.md`
  - `fixtures/test-modal.metadata.yaml`
  - `rubrics/test-modal.rubric.yaml`

### 5.4 test-data-table
- **Name:** Data Table Testing
- **Difficulty:** COMPLEX
- **Risk:** High
- **Scenario:** Plan testing strategy for a data table with sorting and filtering
- **Key a11y concerns:** Automated tests (table semantics, header scope, contrast via axe-core), keyboard tests (Tab through table, sortable header interaction, roving tabindex behavior), screen reader tests (headers announced, sort state announced, table structure clear), visual tests (focus indicators, sort indicators), acceptance criteria for each interaction (sort ascending/descending/none)
- **Expected plan length:** 5-7 pages
- **Files:**
  - `fixtures/test-data-table.md`
  - `fixtures/test-data-table.metadata.yaml`
  - `rubrics/test-data-table.rubric.yaml`

### 5.5 test-multi-page-audit
- **Name:** Multi-Page Audit Plan
- **Difficulty:** COMPLEX
- **Risk:** High
- **Scenario:** Plan accessibility audit strategy for a multi-page website or application
- **Key a11y concerns:** Audit scope (which pages, flows, user journeys), automated testing approach (axe-core rules, which rules apply to which pages), manual testing approach (critical paths, user flows, priority order), screen reader testing (NVDA on Windows, JAWS, VoiceOver on Mac), visual testing (high contrast, 200% zoom, reduced motion), success criteria per page type, a11y-critic review checkpoints per deliverable, remediation prioritization (CRITICAL > MAJOR > MINOR)
- **Expected plan length:** 8-12 pages
- **Files:**
  - `fixtures/test-multi-page-audit.md`
  - `fixtures/test-multi-page-audit.metadata.yaml`
  - `rubrics/test-multi-page-audit.rubric.yaml`

---

## Fixture Distribution Summary

| Domain | Count | TRIVIAL | MODERATE | COMPLEX | AMBIGUOUS |
|--------|-------|---------|----------|---------|-----------|
| **ARIA Pattern** | 5 | 1 | 2 | 1 | 1 |
| **Keyboard Nav** | 5 | 1 | 2 | 1 | 1 |
| **Screen Reader** | 5 | 1 | 2 | 1 | 1 |
| **Visual/Cognitive** | 5 | 2 | 2 | 1 | — |
| **Testing/Audit** | 5 | 1 | 2 | 2 | — |
| **TOTAL** | **25** | **6** | **10** | **6** | **3** |

---

## File Checklist

All 75 fixture files should exist:

- [ ] 25 fixture description files (.md)
- [ ] 25 fixture metadata files (.metadata.yaml)
- [ ] 25 fixture rubric files (.rubric.yaml)

For each fixture, the files should be named consistently:
- Fixture: `{fixture_id}.md`
- Metadata: `{fixture_id}.metadata.yaml`
- Rubric: `{fixture_id}.rubric.yaml`

Example:
- `fixtures/aria-disclosure-widget.md`
- `fixtures/aria-disclosure-widget.metadata.yaml`
- `rubrics/aria-disclosure-widget.rubric.yaml`

---

## Fixture Reference for Rubric Creation

Each rubric evaluates a11y-planner's plan on these dimensions (weight-adjusted):

1. **Completeness** (weight 3): All 9 phases present?
2. **APG Pattern Mapping** (weight 3): Patterns mapped with URLs?
3. **WCAG Grounding** (weight 3): WCAG/APG citations for all decisions?
4. **Specificity** (weight 2): Actionable for developers?
5. **Multi-Perspective** (weight 2): Keyboard, screen reader, low vision, cognitive all covered?
6. **Testing Coverage** (weight 2): Automated, keyboard, screen reader, visual testing all planned?
7. **Calibration** (weight 1): Effort proportional to complexity?

Composite score = weighted average × 100 (0-100)

