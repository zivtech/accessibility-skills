# A11y-Critic Skill Profile

## Overview

**Skill Type**: CRITIC (reviews and evaluates accessibility in existing code)

**Target Skill**: a11y-critic (/.claude/agents/a11y-critic.md)

**Model**: claude-opus-4-6

**Mode**: Read-only (Write, Edit tools blocked)

**Focus**: Accessibility *design decisions*, not just WCAG compliance violations

## Investigation Protocol (10-Phase)

The skill implements a deep, evidence-backed accessibility design review protocol:

1. **Phase 1 - Pre-commitment Predictions**: Predict 3-5 most likely a11y design issues based on component type before reading code
2. **Phase 2 - Semantic HTML Audit**: Verify semantic structure, heading hierarchy, landmark regions, form labels, list semantics
3. **Phase 3 - ARIA Pattern Compliance**: Check all interactive widgets match WAI-ARIA APG patterns, required attributes present, values valid, patterns complete
4. **Phase 4 - Focus Management Review**: Tab order logic, focus traps, focus restoration, skip navigation, dynamic content focus, roving tabindex for composites
5. **Phase 5 - State Communication Audit**: Loading states, error states, selected/checked/expanded, disabled/readonly, visual-only indicators
6. **Phase 6 - Multi-Perspective Review**: Screen reader, keyboard-only, low vision (200% zoom, high contrast), cognitive accessibility
7. **Phase 7 - Gap Analysis**: Explicitly identify what's MISSING (missing error handling, missing announcements, missing focus restoration, missing skip links, etc.)
8. **Phase 8 - Realist Check**: Severity calibration; actual user impact vs theoretical violations
9. **Phase 9 - Self-Audit**: Confidence gating; move LOW confidence findings to Open Questions
10. **Phase 10 - Synthesis**: Compare actual findings against predictions; produce structured verdict

## Work Types Supported

- **Component/Widget Reviews**: Custom interactive components (dropdowns, modals, tabs, disclosure, form validation)
- **Page/Feature Reviews**: Multi-component accessibility (navigation + content + forms)
- **Refactor Reviews**: Existing accessible code being modified

## Output Format Contract

Required sections (exact heading format):

- **VERDICT**: One of REJECT / REVISE / ACCEPT-WITH-RESERVATIONS / ACCEPT
- **Overall Assessment**: 2-3 sentence summary of accessibility design coherence
- **Pre-commitment Predictions**: Expected vs actual findings
- **Critical Findings** (blocks access): List with file:line, user group impacted, WCAG/APG citation, fix
- **Major Findings** (significantly degrades experience): List with evidence
- **Minor Findings** (friction, workaround exists): List
- **Enhancements** (best practice): List
- **What's Missing**: Explicit gap analysis (missing aria-live, missing focus restoration, etc.)
- **Multi-Perspective Notes**: Organized by: Screen reader user, Keyboard-only user, Low vision user, Cognitive accessibility user
- **Verdict Justification**: Why this verdict, escalation rationale, severity recalibrations
- **Open Questions (unscored)**: Low-confidence and speculative items

## Evidence Requirements

For **CRITICAL/MAJOR** findings, MUST include:

- **File:line reference** pointing to specific code (e.g., `src/components/Modal.tsx:42`)
- **Exact ARIA attribute, HTML element, or pattern** involved
- **Which user group is impacted** (screen reader, keyboard, low vision, cognitive)
- **Expected behavior** (cite WCAG 2.2 criterion or WAI-ARIA APG pattern by name)
- **Concrete fix suggestion**

Example format:
> CRITICAL: Modal dialog missing focus trap. See `src/components/Modal.tsx:42` where the dialog has no `role="dialog"` and focus can escape to background. Per WCAG 2.1.2 (No Keyboard Trap) and WAI-ARIA Modal Dialog pattern, focus must be trapped. Fix: add `role="dialog"`, `aria-modal="true"`, and implement focus trap logic.

## Severity Scale Definition

- **CRITICAL**: Blocks access entirely for a user category. Screen reader users cannot access core functionality. Keyboard users are trapped. Form validation fails silently. Examples: modal with no Escape key and no focus trap; custom dropdown with no arrow key navigation.
- **MAJOR**: Significantly degrades experience for a user category. Wrong ARIA pattern confuses widget use. Focus restoration missing makes navigation hard. Error messages not associated with fields. Examples: tabs with aria-selected but no arrow keys; disclosure without aria-controls.
- **MINOR**: Friction but workaround exists. Heading hierarchy has gaps but landmark structure is clear. aria-label could be more specific but is functional. Examples: div with ARIA instead of native button (works, but not best practice); missing aria-current on current page in nav.
- **ENHANCEMENT**: Best practice not met but no access barrier. Missing reduced-motion media query. Missing skip link. Could use better landmark structure.

## Key WCAG 2.2 & APG Criteria

Core criteria evaluated:

- **1.3.1 Info and Relationships**: Semantic structure, form labels, logical relationships via ARIA
- **2.1.1 Keyboard**: Tab navigation available for all interactive elements
- **2.1.2 No Keyboard Trap**: Tab can always move forward/backward; Escape dismisses overlays
- **2.4.1 Bypass Blocks**: Skip links present; way to reach main content
- **2.4.3 Focus Order**: Tab order matches visual left-to-right, top-to-bottom
- **2.4.7 Focus Visible**: Focus indicator is visible and meets 3:1 contrast
- **2.5.8 Target Size**: Interactive elements 44x44 CSS pixels minimum
- **3.2.1 On Focus**: Focus doesn't cause unexpected context change
- **4.1.2 Name, Role, Value**: Buttons/inputs accessible to AT; state programmable
- **4.1.3 Status Messages**: Dynamic updates announced to AT

WAI-ARIA APG patterns evaluated by component type:
- Disclosure (Show/Hide)
- Menu Button (Dropdown)
- Tabs
- Modal Dialog
- Combobox (Autocomplete)
- Listbox
- Slider
- Tree View
- Data Table
- Live Regions

## Key Differentiators

1. **Design vs Compliance Focus**: Reviews accessibility *decisions* not just test violations. Catches incomplete ARIA patterns, missing focus restoration, multi-perspective gaps.
2. **Structured "What's Missing" section**: Surfaces gaps automated tests miss (missing announcements, missing focus management, missing semantic structure).
3. **10-phase investigation protocol**: Pre-commitment predictions → semantic audit → ARIA audit → focus audit → state audit → multi-perspective → gap analysis → realist check → self-audit → synthesis.
4. **Multi-perspective mandatory**: Each perspective (screen reader, keyboard, low vision, cognitive) reveals different issue classes.
5. **WCAG/APG grounding**: Every finding references specific criterion or pattern, not vague "accessibility concerns."
6. **Metacognitive self-audit**: Confidence gating reduces false positives; genuine design gaps vs stylistic preferences clearly distinguished.
7. **Realist Check calibration**: Severity matches actual user impact; false positives explicitly avoided.

## Success Metrics (Target)

Expected improvements over baseline:

- **Critical Finding Detection**: a11y-critic should identify 70%+ of architectural-level a11y issues (missing focus management, incomplete patterns) vs baseline ~30%
- **Gap Coverage**: "What's Missing" section surfaces 4-5x more design gaps than generic accessibility prompts
- **Evidence Rate**: 85%+ of CRITICAL/MAJOR findings include file:line references; baseline ~40%
- **Multi-perspective Coverage**: All four perspectives analyzed; baseline typically covers 1-2
- **False Positive Rate**: <15% on HAS-BUGS/FLAWED fixtures; maintains specificity while improving sensitivity

## Anti-Patterns to Avoid

The skill explicitly guards against:

- **Rubber-stamping**: Assuming "tests pass so semantics are fine" without verification
- **Manufactured violations**: Inventing gaps that don't exist (e.g., "aria-label could be longer" as a finding)
- **Surface-only criticism**: Reporting minor wording issues while missing architectural gaps
- **Single-perspective tunnel vision**: Only reviewing ARIA correctness, missing focus or low vision issues
- **Findings without evidence**: Opinions vs evidence-backed findings
- **False positives on div + ARIA**: Recognizing div + proper ARIA as acceptable when native element unavailable
- **Alarmist severity**: Treating best-practice missing features as blocking issues

## Companion Configurations

- **Fallback routing**: (if used with OMC) routes through agent tier
- **Tool usage**: Read (load source code), Grep (verify ARIA attributes), Glob (find related files), Bash (git commands for verification)
- **Model tier**: Requires Claude Opus 4.6 for depth of multi-perspective reasoning

## Example Component Types & Expected Findings

### Custom Dropdown/Select
**Predicted issues**:
- Focus doesn't restore to trigger on Escape
- No aria-expanded or not synchronized with state
- Arrow key navigation incomplete
- Selected option not announced to screen reader
- Options container not referenced from button

### Modal Dialog
**Predicted issues**:
- No `role="dialog"` or no `aria-modal="true"`
- Focus doesn't trap (Tab escapes to background)
- Focus doesn't restore to trigger on close
- Heading hierarchy wrong inside modal
- Backdrop clickable but not labeled

### Form with Validation
**Predicted issues**:
- Errors announce via aria-live but not associated via aria-describedby
- Error summary exists but doesn't link to fields
- Disabled state uses CSS `:disabled` not `disabled=""` attribute
- Field-level error announcements conflict with form-level summary

### Custom Tabs Widget
**Predicted issues**:
- No `role="tablist"` on container
- Tabs lack `role="tab"`
- Tab selection not reflected in `aria-selected`
- Panels not referenced via `aria-labelledby`
- Arrow key navigation missing (should cycle tabs)
- Active tab not focused after arrow key navigation

### Data Table
**Predicted issues**:
- Missing `<caption>` or `aria-label` on table
- Column headers lack `scope="col"`
- Row headers lack `scope="row"` (if header cells present)
- Complex tables missing `role="rowheader"` or `role="colheader"`
- Row selection state not announced

## Evaluation Approach

This skill is evaluated on:

1. **Fixture Diversity**: 8-10 realistic React/HTML components with a11y issues planted at varying levels (CLEAN, HAS-BUGS, FLAWED, ADVERSARIAL)
2. **Finding Detection**: Can it find planted issues and distinguish from false positives?
3. **Gap Analysis Depth**: Does "What's Missing" surface design gaps beyond what automated tests catch?
4. **Evidence Quality**: Are file:line references accurate? Are WCAG/APG citations correct?
5. **Multi-Perspective Coverage**: Does the review address all four perspectives?
6. **Severity Calibration**: Are findings rated appropriately (not alarmist, not glossed over)?
7. **Comparison to Baseline**: Does structural protocol + evidence requirements outperform generic accessibility review prompts?
