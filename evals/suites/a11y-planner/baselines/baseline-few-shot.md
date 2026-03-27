# Baseline B: Few-Shot Generic Planning Prompt with Structure and Example

## Usage

This baseline represents a structured request with guided sections and an example response. This is more sophisticated than baseline-zero-shot but less protocol-driven than a11y-planner.

## Prompt

You are an accessibility expert. Create a comprehensive accessibility design plan for the following feature or component.

**Feature:** {feature_description}

---

## Structure for Your Response

Organize your plan with these sections:

1. **Overview and Scope**
   - What is being planned?
   - Who needs accessibility?
   - What is the compliance target (WCAG 2.2 AA)?
   - What assistive technologies must be supported?
   - What is the risk level?

2. **Semantic Structure and Landmarks**
   - Landmark regions (nav, main, aside, footer)
   - Heading hierarchy (h1 → h2 → h3)
   - Semantic elements (form, fieldset, legend, list, table, etc.)
   - HTML structure stub

3. **Interactive Pattern Design**
   - Every interactive element identified
   - For each: APG pattern, keyboard interactions, ARIA roles/states/properties
   - WCAG citations for each design decision

4. **Keyboard Navigation and Focus Management**
   - Tab order design
   - Focus indicators (visibility and contrast)
   - Focus trap design (for modals/overlays)
   - Focus restoration after overlay closure
   - Escape key behavior

5. **State Communication Design**
   - All possible states identified (expanded, disabled, invalid, loading, etc.)
   - Visual + programmatic indicators for each state
   - ARIA attributes (aria-expanded, aria-selected, aria-invalid, aria-busy, etc.)
   - Live regions (aria-live, role="alert", role="status")

6. **Visual Accessibility**
   - Color contrast requirements (WCAG 1.4.3)
   - Non-color alternatives (icon, text, shape, position)
   - Font sizing (relative units, responsive text)
   - Touch target sizing (44×44 CSS pixels)
   - Animation support (prefers-reduced-motion)

7. **Content Accessibility**
   - Alt text strategy for images
   - Link text quality (descriptive, not "click here")
   - Form label association
   - Error message clarity and association
   - Language attributes

8. **Testing Strategy**
   - Automated testing (which tools, which rules)
   - Manual keyboard testing (Tab order, Escape, arrow keys)
   - Screen reader testing (NVDA, JAWS, VoiceOver)
   - Acceptance criteria (measurable, per-feature)

9. **Implementation Tasks**
   - For each component: files, structure, ARIA attributes, keyboard interactions, tests
   - WCAG criteria satisfied
   - Review checkpoints for code review

---

## Example Response (Abbreviated)

For a disclosure widget, your plan might look like:

### Overview and Scope
- **Feature:** A disclosure widget (accordion) where clicking a button shows/hides content
- **Users:** All users benefit from reduced cognitive load; keyboard-only users especially
- **Compliance:** WCAG 2.2 AA
- **Assistive tech:** NVDA, VoiceOver, keyboard-only
- **Risk:** Medium (interactive pattern, focus management required)

### Semantic Structure
- Top-level: div or section containing multiple disclosure items
- Per item: h2 > button (trigger), div (content panel)
- Button announces expanded state

### Interactive Pattern Design
- **Pattern:** APG Disclosure (https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/)
- **Button:** role="button", aria-expanded (true/false), aria-controls (content id)
- **Keyboard:** Tab focuses button, Space/Enter toggles aria-expanded
- **WCAG:** 2.1.1 Keyboard, 4.1.2 Name Role Value, 4.1.3 Status Messages

### Focus Management
- Tab focuses button, no special focus management needed
- Focus indicator must be visible (3:1 contrast)

### State Communication
- aria-expanded = true: content shown
- aria-expanded = false: content hidden
- State change announced to screen reader on Space/Enter

### Visual Accessibility
- Button must have 44×44 pixel touch target
- Focus indicator 3:1 contrast
- No color-only indicators

### Content Accessibility
- Button text clearly describes what expands (e.g., "Show details" not "Toggle")
- Content within panel should have proper heading hierarchy

### Testing Strategy
- Automated: axe-core checks for button role, aria-expanded, aria-controls
- Keyboard: Tab focuses button, Space toggles expansion, focus indicator visible
- Screen reader: Button role announced, aria-expanded state announced, content appears/disappears
- Acceptance: Button responds to Space/Enter on all zoom levels, focus indicator visible

### Implementation Tasks
- Task 1: Create DisclosureButton component with aria-expanded and aria-controls
  - Files: components/Disclosure.tsx
  - ARIA: button role, aria-expanded (true/false), aria-controls
  - Keyboard: Space/Enter toggles aria-expanded
  - Tests: aria-expanded toggles, content visibility changes, screen reader announces state
  - WCAG: 2.1.1, 4.1.2, 4.1.3

---

## Expected Performance

**Estimated composite score range:** 70-80
**Strengths:** Structured approach, explicit sections, example helps with organization and pattern awareness
**Weaknesses:** Example is abbreviated (not comprehensive), may still miss some WCAG citations or APG pattern completeness, no explicit emphasis on WCAG grounding in all decisions, testing strategy less detailed than a11y-planner

## Rationale

This baseline is stronger than zero-shot because:
- Explicit structure guides coverage (all 9 sections)
- Example shows expected format and detail level
- Mentions APG patterns (shows pattern awareness)
- Mentions WCAG citations (shows grounding awareness)

However, it's still weaker than a11y-planner because:
- No explicit protocol (9-phase doesn't guarantee completeness)
- Example is abbreviated (not comprehensive enough for complex features)
- No emphasis on mandatory APG pattern mapping (example shows it, but not required)
- No emphasis on WCAG citation for every decision (shown in example, but not required)
- Testing strategy section is generic (not as detailed as a11y-planner protocol)

