# A11y-Planner Skill Profile

## Overview

**Name:** a11y-planner
**Type:** PLANNER
**Model:** claude-opus-4-6
**Agent Path:** `a11y-planner/.claude/agents/a11y-planner.md`
**Description:** Accessibility Design Planner — 9-phase protocol for designing accessible implementations before coding. Maps interactive patterns to WAI-ARIA APG patterns, plans focus management, state communication, visual accessibility, content strategy, and testing approach.

---

## Core Purpose

The a11y-planner generates comprehensive accessibility design specifications BEFORE implementation. Unlike a11y-critic (which reviews implemented code for bugs), a11y-planner produces design documents that prevent accessibility bugs from entering the codebase in the first place.

### Design Philosophy

- **Prevention-focused:** Accessibility is designed in, not tested in
- **Specification-driven:** Produces testable, measurable design requirements
- **WCAG-grounded:** Every design decision cites WCAG 2.2 or WAI-ARIA APG
- **Pattern-mapped:** Every interactive element maps to an established APG pattern
- **No implementation code:** Plans with structure stubs and ARIA attribute lists, not JSX/HTML/PHP

---

## Planning Protocol (9 Phases)

### Phase 1: Scope & Context
Define what's being planned and why:
- Feature scope (one-sentence description)
- User needs addressed
- Accessibility scope (which user groups need a11y)
- Compliance target (WCAG 2.2 AA default)
- Assistive technologies (NVDA, JAWS, VoiceOver, keyboard-only, etc.)
- Risk level (Low/Medium/High)
- Existing code modifications (if any)
- Constraints (browser support, library limitations)

### Phase 2: Semantic Structure Plan
Design HTML structure and landmark regions:
- Landmark regions (nav, main, aside, footer) and relationships
- Heading hierarchy (h1 → h2 → h3, no skips)
- Semantic elements (nav, main, section, article, form, fieldset, table, list)
- Skip link strategy (WCAG 2.4.1)
- Form structure (fieldset/legend for grouped inputs)
- HTML structure stub (semantic elements only, no code)

### Phase 3: Interaction Pattern Design
Map every interactive element to WAI-ARIA APG patterns:
- Widget identification and naming
- APG pattern mapping with explicit URL citation
- Keyboard interaction model (Tab, Enter, Space, Escape, Arrow keys)
- ARIA implementation (roles, states, properties)
- Screen reader experience (announcements on focus, on state change)

### Phase 4: Focus Management Plan
Design how focus moves through the interface:
- Logical tab order (step-by-step documentation)
- Focus trap implementation (modals, dialogs)
- Focus restoration after overlay closure
- Focus movement for dynamic content insertion
- Focus indicator visibility (WCAG 2.4.7 contrast requirements)
- Skip link implementation
- Roving tabindex for composite widgets

### Phase 5: State Communication Design
Plan communication of all states to assistive technology:
- All possible states (loading, error, disabled, expanded, selected, invalid, etc.)
- Visual + programmatic indicators for EACH state
- ARIA attributes (aria-expanded, aria-selected, aria-pressed, aria-checked, aria-disabled, aria-invalid, aria-busy, aria-describedby)
- Live regions (aria-live, role="status", role="alert")
- Error message association (aria-describedby)

### Phase 6: Visual Accessibility Plan
Design visual accessibility:
- Color contrast (WCAG 1.4.3: 4.5:1 normal, 3:1 large)
- Non-color indicators (never sole color indicator per WCAG 1.4.1)
- Font sizing strategy (relative units: rem/em, base 16px)
- Responsive text metrics (line height, letter spacing, word spacing)
- Animation/motion (respects prefers-reduced-motion)
- Dark mode support (prefers-color-scheme)
- Touch target sizing (44×44 CSS pixels minimum per WCAG 2.5.8)

### Phase 7: Content Accessibility Plan
Design content structure for screen readers:
- Alt text strategy (decorative images, informative, complex)
- Link text quality (descriptive, not "click here")
- Form label association (label for, nesting, aria-labelledby, aria-label)
- Error message clarity (specific, actionable, associated)
- Form instructions (formatting, special requirements)
- Language attributes (html lang, lang for foreign phrases)
- Reading order (DOM order matches visual order)

### Phase 8: Testing Strategy
Plan accessibility validation:
- Automated testing (axe-core rules, what it can/cannot catch)
- Manual keyboard testing (Tab order, Escape behavior, arrow keys)
- Screen reader testing (NVDA, JAWS, VoiceOver on real devices)
- Visual regression testing (focus indicators, 200% zoom, high contrast, reduced motion)
- Acceptance criteria (measurable, testable, per-feature)

### Phase 9: Implementation Tasks & Review Checkpoints
Break plan into clear, testable tasks:
- Task name and scope
- Files to create/modify
- Structure stub (semantic elements + ARIA)
- ARIA attributes required (with WCAG citations)
- Keyboard interactions
- Focus management logic
- State communication logic
- Test cases
- WCAG criteria satisfied
- a11y-critic review checkpoint (what to verify after implementation)

---

## Success Criteria for a11y-planner Plans

A complete and high-quality a11y-planner plan MUST include:

1. **Scope & Context:** Clear definition of what, why, who, compliance target, tech support, risk, constraints
2. **Semantic Structure Plan:** Complete with landmarks, heading hierarchy, form structure, HTML structure stub
3. **Interaction Pattern Design:** Every interactive widget mapped to APG pattern with explicit citations
4. **Focus Management Plan:** Tab order, focus traps, focus restoration, skip link, roving tabindex
5. **State Communication Design:** All states documented with visual + programmatic indicators for each
6. **Visual Accessibility Plan:** Contrast requirements, non-color alternatives, responsive text, touch targets, motion
7. **Content Accessibility Plan:** Alt text, link text, form labels, error messages, language, reading order
8. **Testing Strategy:** Automated, keyboard, screen reader, visual regression testing approaches
9. **Implementation Tasks:** Clear, testable, with WCAG citations and a11y-critic checkpoints
10. **WCAG Grounding:** Every design decision cites WCAG 2.2 criterion or APG pattern (URL)
11. **Specificity:** No "figure this out later" placeholders; all details explicit
12. **Calibration:** Simple components = 1-2 pages, medium features = 3-5 pages, complex features = 6-10 pages

---

## Evaluation Dimensions for a11y-planner

### 1. Completeness
- All 9 phases present and addressed
- No missing sections or unspecified details
- Calibration appropriate to feature complexity

### 2. WCAG Grounding & Pattern Mapping
- Every interactive widget maps to specific APG pattern with URL
- Every ARIA attribute cites WCAG 2.2 success criterion
- Every design decision grounded in WCAG 2.2 or APG
- No generic "use aria-expanded" statements; specific patterns with citations

### 3. Specificity & Actionability
- Developers can implement from the plan without guessing
- ARIA attribute lists are complete and precise
- Keyboard interactions explicitly documented
- Focus management logic clearly defined
- Test cases measurable and testable

### 4. Coverage Breadth
- Semantic structure complete (landmarks, headings, form structure)
- All interactive widgets addressed
- All states (expanded, disabled, invalid, loading, etc.) documented
- All user groups considered (keyboard, screen reader, low vision, cognitive)
- Visual + programmatic communication for every state
- Focus management for every modal/overlay/dynamic content

### 5. Multi-Perspective Design
- Keyboard-only user experience planned
- Screen reader user experience planned
- Low vision user considerations addressed
- Cognitive accessibility addressed (consistency, predictability)
- Touch target sizing for mobile accessibility

### 6. Testing Coverage
- Testing strategy includes automated, keyboard, screen reader approaches
- Acceptance criteria are measurable and per-feature
- Failure modes identified and prevented
- a11y-critic checkpoints defined for post-implementation review

### 7. Calibration & Proportionality
- Simple components (buttons, inputs) not over-planned (1-2 pages)
- Medium complexity (forms with validation, disclosures) properly detailed (3-5 pages)
- Complex features (modals, dialogs, data tables) comprehensively planned (6-10 pages)
- No scope creep on trivial components, no under-planning of risky features

---

## Known Failure Modes to Detect

1. **Vague ARIA Implementation:** "Use aria-expanded" without APG pattern, keyboard interactions, or test cases
2. **Missing APG Pattern Mapping:** Designing custom interactions when established APG patterns exist
3. **No WCAG Grounding:** Design decisions without WCAG 2.2 or APG citations
4. **Incomplete State Communication:** Planning some states but missing others (e.g., disabled, invalid, loading)
5. **No Focus Management Planning:** Assuming focus "just works" without explicit design for modals/overlays
6. **Color-Only Indicators:** Using color without text, icon, shape, or position alternatives
7. **No Testing Strategy:** Deferring accessibility validation to "after implementation"
8. **Scope Creep:** Over-detailed planning for trivial components (buttons, links)
9. **Visual-Only State Communication:** "Error indicated by red border" without aria-invalid and error message
10. **Missing Skip Link:** No bypass for repetitive navigation per WCAG 2.4.1
11. **Incomplete Implementation Breakdown:** Tasks not specific enough to guide development
12. **Missing a11y-Critic Checkpoints:** No clear review points defined for post-implementation verification

---

## Evaluation Output Contract

Plans output to: `docs/a11y-plans/YYYY-MM-DD-<feature-name>-a11y-plan.md`

Minimum document sections (order matters):
1. Scope & Context
2. Semantic Structure Plan
3. Interaction Pattern Design
4. Focus Management Plan
5. State Communication Design
6. Visual Accessibility Plan
7. Content Accessibility Plan
8. Testing Strategy
9. Implementation Tasks
10. a11y-Critic Review Checkpoints

Optional tables for clarity:
- Interactive Elements Table (Widget | APG Pattern | Keyboard | ARIA | WCAG)
- State Communication Table (State | Visual | Programmatic | ARIA | WCAG)
- a11y-Critic Checkpoints Table (Checkpoint | After Task | Focus)

---

## Calibration Guidance

### Low Risk (Simple Component)
**Expected length:** 1-2 pages
**Examples:** Button, link, text input, label
**Coverage:** Structure, basic ARIA (if needed), keyboard activation, basic tests

### Medium Risk (Form/Disclosure)
**Expected length:** 3-5 pages
**Examples:** Form with validation, disclosure widget, filter sidebar
**Coverage:** Full semantic structure, ARIA states, focus management, state communication, comprehensive tests

### High Risk (Modal/Dialog/Complex)
**Expected length:** 6-10 pages
**Examples:** Modal dialog, tabs with dynamic content, data table with sorting
**Coverage:** Detailed semantic structure, complete ARIA, focus trap design, focus restoration, state communication for all states, testing across all interactions

---

## Comparison to Related Skills

| Aspect | a11y-planner | a11y-critic | accessibility-testing |
|--------|--------------|------------|----------------------|
| **Phase** | Design (pre-code) | Review (post-code) | Validation (post-code) |
| **Output** | Design specification | Bug report + recommendations | Test results + log |
| **Focus** | Prevention | Detection | Measurement |
| **User** | Designer/Architect | Code reviewer | QA/Tester |
| **When to use** | Before implementation | After implementation | After implementation |
| **Workflow** | a11y-planner → code → a11y-critic | Code → a11y-critic | Code → accessibility-testing |

---

## Companion Skills in Workflow

1. **brainstorming:** Explore multiple accessibility design approaches (before a11y-planner)
2. **writing-plans:** Convert a11y-planner output into structured implementation tasks
3. **Implementation:** Build according to the a11y-planner specification
4. **a11y-critic:** Review implementation against the a11y-planner design
5. **accessibility-testing:** Run automated tests to validate accessibility
6. **a11y-test:** Manual keyboard testing with real key presses

---

## Evidence Requirements

When a11y-planner makes claims about existing code:
- **Existing code references:** Cite `file:line` of components being modified
- **Current state:** Show the current accessibility state before proposing changes
- **User impact claims:** Cite specific WCAG criterion and affected user group
- **Effort estimates:** Base on number of components affected, citing each by file:line

---

## Key Differentiators

1. **9-Phase Protocol:** Comprehensive coverage ensures nothing is overlooked
2. **Mandatory WCAG Grounding:** Every decision cites WCAG 2.2 or APG (URL)
3. **Mandatory APG Pattern Mapping:** Every interactive element mapped to established patterns
4. **Specific Implementation Guidance:** Developers implement without guessing
5. **Focus Management by Design:** Focus traps, restoration, and indicators designed before code
6. **Testing Strategy Embedded:** Acceptance criteria defined upfront
7. **a11y-Critic Checkpoints:** Clear review points for post-implementation verification
8. **Calibration:** Effort proportional to risk (simple = brief, complex = detailed)
9. **Multi-Perspective Design:** Keyboard, screen reader, low vision, cognitive all covered
10. **Prevention-Focused:** Catches accessibility issues at design phase, not implementation phase

