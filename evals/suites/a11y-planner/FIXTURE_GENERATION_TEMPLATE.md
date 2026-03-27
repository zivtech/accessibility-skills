# Fixture Generation Template for A11y-Planner Evaluation Suite

This document provides templates and examples for generating the remaining 24 fixture triplets (`.md` + `.metadata.yaml` + `.rubric.yaml`).

Use the **aria-disclosure-widget** fixtures as a complete example, then follow the patterns below for each remaining fixture.

---

## Template Structure

For each fixture, create 3 files:

### 1. Fixture Description (.md)
**Path:** `fixtures/{fixture_id}.md`

**Structure:**
```markdown
# Fixture: {Display Name}

## Feature Description
[What's being planned, context, scope]

## Context
- **Platform:** [React/Vue/vanilla JS/etc]
- **Existing code:** [Yes/No]
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** [NVDA, VoiceOver, keyboard-only, etc]
- **Scope:** [Single component/Page/Feature]
- **Constraints:** [Design system, mobile, etc]

## Requirement
Create a comprehensive accessibility design plan that a developer with no accessibility knowledge can use to implement correctly on the first attempt.

## Scope Hints
This is a **{DIFFICULTY}** difficulty fixture — {brief description of what makes it this difficulty}.

The plan should be concise ({expected pages}) but complete. Focus on:
1. [Key focus area 1]
2. [Key focus area 2]
3. [Key focus area 3]

## What Success Looks Like
An excellent plan would:
- ✓ [Success criterion 1]
- ✓ [Success criterion 2]
- ✓ [Success criterion 3]

## What Would Be Below Expectations
- ✗ [Below-expectation indicator 1]
- ✗ [Below-expectation indicator 2]
```

**Reference:** See `fixtures/aria-disclosure-widget.md` for complete example

### 2. Fixture Metadata (.metadata.yaml)
**Path:** `fixtures/{fixture_id}.metadata.yaml`

**Structure:**
```yaml
fixture_id: {fixture_id}
name: {Display Name}
description: {One sentence description}
language: jsx  # or other
framework: React  # or other
difficulty: {TRIVIAL|MODERATE|COMPLEX|AMBIGUOUS}
domain: {Domain Name}
work_type: component_plan
risk_level: {Low|Medium|High}

scenario:
  feature: {Feature description}
  user_need: {User need addressed}
  compliance_target: WCAG 2.2 AA
  assistive_technologies:
    - NVDA (Windows)
    - VoiceOver (macOS)
    - Keyboard-only users
  scope: {Scope description}
  constraints:
    - {Constraint 1}
    - {Constraint 2}

expected_plan_sections:
  - Scope & Context
  - Semantic Structure
  - Interaction Pattern Design
  - Focus Management
  - State Communication
  - Visual Accessibility
  - Content Accessibility
  - Testing Strategy
  - Implementation Tasks

key_evaluation_criteria:
  - {Criterion 1}
  - {Criterion 2}

expected_findings:
  must_have:
    - {Finding 1}
    - {Finding 2}
  should_have:
    - {Finding 1}
  nice_to_have:
    - {Finding 1}

false_positive_traps:
  - {Trap 1}
  - {Trap 2}

multi_perspective_coverage:
  keyboard: "{Description}"
  screen_reader: "{Description}"
  low_vision: "{Description}"
  cognitive: "{Description}"
  mobile_touch: "{Description}"

notes: |
  [What this fixture tests about a11y-planner]
  [Expected verdict]
  [What to look for in evaluation]
```

**Reference:** See `fixtures/aria-disclosure-widget.metadata.yaml` for complete example

### 3. Fixture Rubric (.rubric.yaml)
**Path:** `rubrics/{fixture_id}.rubric.yaml`

**Structure:**
```yaml
fixture_id: {fixture_id}
rubric_version: "1.0"
scoring_method: hybrid
hybrid_weights:
  rule_based: 0.7
  llm_judge: 0.3

dimensions:
  - id: completeness
    name: "Completeness"
    description: "Are all 9 phases addressed?"
    weight: 3
    rule_based_checks:
      - has_scope_section: true
      - has_semantic_structure: true
      - has_interaction_design: true
      - has_focus_management: true
      - has_state_communication: true
      - has_visual_accessibility: true
      - has_content_accessibility: true
      - has_testing_strategy: true
      - has_implementation_tasks: true

  - id: apg_pattern_mapping
    name: "APG Pattern Mapping"
    description: "Does plan reference relevant APG patterns with URLs?"
    weight: 3
    rule_based_checks:
      - mentions_apg_pattern: true
      - includes_apg_url: true
      - maps_keyboard_interactions: true
    expected_citations:
      - "APG pattern URL"
      - "WCAG citation"

  - id: wcag_grounding
    name: "WCAG Grounding"
    description: "Does every design decision cite WCAG 2.2 or APG?"
    weight: 3
    rule_based_checks:
      - design_decisions_cite_wcag: true
    expected_citations:
      - "WCAG criterion 1"
      - "WCAG criterion 2"

  - id: specificity
    name: "Specificity & Actionability"
    description: "Can developers implement without guessing?"
    weight: 2
    rule_based_checks:
      - includes_aria_specifics: true
      - includes_html_stub: true
      - documents_keyboard_events: true

  - id: multi_perspective
    name: "Multi-Perspective Coverage"
    description: "Are all perspectives addressed?"
    weight: 2
    rule_based_checks:
      - addresses_keyboard: true
      - addresses_screen_reader: true
      - addresses_low_vision: true
      - addresses_cognitive: true
      - addresses_mobile: true

  - id: testing_coverage
    name: "Testing Coverage"
    description: "Is complete testing strategy present?"
    weight: 2
    rule_based_checks:
      - documents_automated_testing: true
      - documents_keyboard_testing: true
      - documents_screen_reader_testing: true
      - specifies_acceptance_criteria: true

  - id: calibration
    name: "Calibration & Proportionality"
    description: "Is plan length appropriate for difficulty?"
    weight: 1
    rule_based_checks:
      - estimated_length_pages: {min}-{max}
      - no_scope_creep: true

composite_score_formula: |
  score = sum(dimension_score × weight) / sum(weights) × 100

scoring_thresholds:
  excellent: 90-100
  good: 75-89
  adequate: 60-74
  weak: 40-59
  poor: 0-39

expected_reviewer_performance:
  - condition: a11y-planner
    expected_score: {min}-{max}
    reasoning: "Description of expected performance"

  - condition: baseline-zero-shot
    expected_score: {min}-{max}
    reasoning: "Description"

verdict_expectations:
  a11y-planner: {ACCEPT|REVISE|ACCEPT-WITH-RESERVATIONS}
  baseline-zero-shot: {ACCEPT|REVISE}

notes: |
  [What this fixture tests]
  [Key evaluation focus]
  [Expected findings]
```

**Reference:** See `rubrics/aria-disclosure-widget.rubric.yaml` for complete example

---

## Quick Generation Guide

### Step 1: For Each Fixture in FIXTURE_INVENTORY.md

Extract from inventory:
- Fixture ID (e.g., `aria-disclosure-widget`)
- Name (e.g., `Custom Disclosure Widget`)
- Domain (e.g., `ARIA Pattern Implementation`)
- Difficulty (e.g., `TRIVIAL`)
- Risk level (e.g., `Low`)
- Scenario description
- Key a11y concerns
- Expected plan length

### Step 2: Create .md File

Use the feature description from FIXTURE_INVENTORY.md as basis for the `.md` file.

**Key sections:**
- Feature Description: Adapt from inventory
- Context: Specify platform (React assumed), compliance (WCAG 2.2 AA), assistive tech
- Requirement: Always "Create accessibility design plan..."
- Scope Hints: Use difficulty and focus areas from inventory
- What Success Looks Like: Extract "must-have" expected findings
- What Would Be Below Expectations: Extract from "false positive traps"

### Step 3: Create .metadata.yaml File

Use the metadata file from aria-disclosure-widget as template.

**Key customizations:**
- fixture_id, name, description, difficulty, domain, risk_level
- scenario: feature, user_need, scope, constraints (from inventory)
- expected_findings: must_have, should_have, nice_to_have (from inventory)
- multi_perspective_coverage: custom per scenario (from inventory)

### Step 4: Create .rubric.yaml File

Use aria-disclosure-widget.rubric.yaml as template.

**Key customizations:**
- dimensions: All 7 dimensions are standard (copy as-is)
- rule_based_checks: Customize for specific APG patterns or WCAG concerns
- expected_citations: Specific WCAG criteria and APG patterns for this fixture
- expected_reviewer_performance: Expected scores for each condition (difficulty-based)
- verdict_expectations: Expected verdict for each condition

---

## Difficulty-Based Customization Guide

### TRIVIAL Fixtures (6 total)
**Expected scores:**
- a11y-planner: 90-100
- baseline-zero-shot: 75-85
- baseline-few-shot: 80-90

**Expected length:** 1-2 pages
**Characteristics:** Well-documented patterns, straightforward interactions

**Examples:**
- aria-disclosure-widget (DONE)
- keyboard-button-bar
- sr-article-page
- visual-status-colors
- test-simple-button

### MODERATE Fixtures (11 total)
**Expected scores:**
- a11y-planner: 85-95
- baseline-zero-shot: 65-75
- baseline-few-shot: 70-80

**Expected length:** 3-5 pages
**Characteristics:** Multiple concerns, established patterns, medium complexity

**Examples:**
- aria-combobox-autocomplete
- aria-tab-dynamic-content
- keyboard-menu-dropdown
- sr-search-results-live
- visual-animated-transition
- test-form
- test-modal
- Plus 4 more

### COMPLEX Fixtures (5 total)
**Expected scores:**
- a11y-planner: 80-95
- baseline-zero-shot: 50-65
- baseline-few-shot: 55-70

**Expected length:** 6-10 pages
**Characteristics:** High complexity, multiple interacting requirements

**Examples:**
- aria-data-table-sorting
- keyboard-modal-focus-trap
- sr-notification-system
- visual-form-validation
- test-data-table

### AMBIGUOUS Fixtures (3 total)
**Expected scores:**
- a11y-planner: 85-95
- baseline-zero-shot: 50-65
- baseline-few-shot: 55-70

**Expected length:** 6-10 pages
**Characteristics:** Intentional ambiguities, trade-offs, decision points

**Examples:**
- aria-modal-form-validation
- keyboard-roving-tabindex
- sr-form-field-help

---

## Domain-Specific Notes

### ARIA Pattern Implementation
**What to check:**
- APG pattern referenced with URL?
- aria-* attributes documented?
- WCAG 4.1.2 cited?
- Keyboard interactions per pattern?

**Pattern URLs:**
- Disclosure: https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/
- Combobox: https://www.w3.org/WAI/ARIA/apg/patterns/combobox/
- Tab: https://www.w3.org/WAI/ARIA/apg/patterns/tabs/
- Dialog: https://www.w3.org/WAI/ARIA/apg/patterns/dialogmodal/
- Listbox: https://www.w3.org/WAI/ARIA/apg/patterns/listbox/
- Menu Button: https://www.w3.org/WAI/ARIA/apg/patterns/menubutton/

### Keyboard Navigation
**What to check:**
- Tab order documented?
- Focus indicators (3:1 contrast) specified?
- Escape behavior for modals?
- Arrow key patterns?
- Focus restoration after overlay?

**Key WCAG criteria:**
- 2.1.1 Keyboard
- 2.4.3 Focus Order
- 2.4.7 Focus Visible
- 2.1.2 No Keyboard Trap

### Screen Reader Experience
**What to check:**
- Landmarks (nav, main, aside, footer)?
- Heading hierarchy (h1 → h2 → h3)?
- List semantics (ul, ol, li)?
- Form labels and associations?
- Live regions (aria-live, role="status", role="alert")?

**Key WCAG criteria:**
- 1.3.1 Info and Relationships
- 2.4.1 Bypass Blocks
- 4.1.2 Name, Role, Value
- 4.1.3 Status Messages

### Visual & Cognitive
**What to check:**
- Color contrast (4.5:1 normal, 3:1 large)?
- Non-color indicators (icon, text, shape, position)?
- Font sizing (relative units, responsive)?
- Animation (prefers-reduced-motion)?
- Touch targets (44×44 minimum)?

**Key WCAG criteria:**
- 1.4.1 Use of Color
- 1.4.3 Contrast Minimum
- 1.4.4 Resize Text
- 2.5.8 Target Size
- 2.3.3 Animation from Interactions

### Testing & Audit
**What to check:**
- Automated testing approach (axe-core, rules)?
- Keyboard testing (Tab, Escape, Arrow keys)?
- Screen reader testing (NVDA, JAWS, VoiceOver)?
- Acceptance criteria (measurable)?
- a11y-critic checkpoints defined?

---

## Batch Generation Command

Once all 25 fixtures are created, verify completeness:

```bash
# Check all fixture files exist
for id in aria-disclosure-widget aria-combobox-autocomplete aria-tab-dynamic-content aria-data-table-sorting aria-modal-form-validation keyboard-button-bar keyboard-menu-dropdown keyboard-breadcrumb keyboard-modal-focus-trap keyboard-roving-tabindex sr-article-page sr-search-results-live sr-product-listing sr-notification-system sr-form-field-help visual-status-colors visual-animated-transition visual-dark-mode visual-form-validation visual-data-viz test-simple-button test-form test-modal test-data-table test-multi-page-audit; do
  echo -n "$id: "
  [ -f "fixtures/${id}.md" ] && echo -n "md✓ " || echo -n "md✗ "
  [ -f "fixtures/${id}.metadata.yaml" ] && echo -n "meta✓ " || echo -n "meta✗ "
  [ -f "rubrics/${id}.rubric.yaml" ] && echo "rub✓" || echo "rub✗"
done
```

---

## Validation Checklist

For each fixture triplet, verify:

### .md File
- [ ] Feature description is clear and specific
- [ ] Context specifies platform, compliance, assistive tech
- [ ] Scope is well-defined
- [ ] Success criteria are clear
- [ ] Expected length is specified (1-2 / 3-5 / 6-10 pages)

### .metadata.yaml File
- [ ] fixture_id, name, difficulty, domain, risk_level correct
- [ ] scenario includes all required fields
- [ ] expected_findings have must_have, should_have, nice_to_have
- [ ] multi_perspective_coverage covers all 5 perspectives
- [ ] notes explain what fixture tests

### .rubric.yaml File
- [ ] All 7 dimensions present with correct weights
- [ ] rule_based_checks are specific to fixture
- [ ] expected_citations include relevant WCAG criteria
- [ ] expected_reviewer_performance has realistic scores
- [ ] verdict_expectations reasonable for difficulty

---

## Reference Files

**Complete Example:** `fixtures/aria-disclosure-widget.*` and `rubrics/aria-disclosure-widget.rubric.yaml`

**Inventory:** `FIXTURE_INVENTORY.md` (all 25 fixtures described in detail)

**Criteria:** `domain-sampling-strategy.md` (domain-by-domain expectations)

---

## Support

For questions about:
- **Structure:** See aria-disclosure-widget fixtures (complete example)
- **Domain requirements:** See domain-sampling-strategy.md
- **Rubric approach:** See statistical-design.md (hybrid scoring section)
- **WCAG citations:** See skill-profile.md (references section)

