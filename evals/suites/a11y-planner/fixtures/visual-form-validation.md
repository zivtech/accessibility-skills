# Fixture: Multi-Step Form with Inline Validation

## Feature Description

You're planning accessibility for a multi-step registration form for a healthcare portal. The form has four steps: personal info, insurance details, medical history, and review/submit. Each step has 4-8 fields. Validation runs in two modes: real-time inline validation (on field blur) and submit-time validation (all errors surfaced on attempted step advancement). When step-level errors occur, a summary panel appears at the top of the step with a count ("3 errors on this page") and links to each invalid field. Individual fields show a red left-border highlight, a red error message below the input, and the input label turns red. The submit step checks for incomplete required fields across all four previous steps and shows a consolidated error list. No accessible error communication is currently implemented — only the visual treatments described above.

## Context

- **Platform:** React SPA, React Hook Form for form state management
- **Existing code:** Yes — form structure and validation logic are implemented; visual error treatments (red border, red text) are in place; no ARIA attributes on error states, no programmatic association between error messages and inputs
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA (Windows), JAWS (Windows), VoiceOver (macOS), keyboard-only users
- **Scope:** Full multi-step form error communication system — inline validation, error summary, cross-step consolidation on final submit; does not include the form's data submission or server-side validation
- **Constraints:** React Hook Form must remain; visual error treatments (red border, red text) must remain; real-time inline validation on blur is a product requirement; the error summary panel placement (top of step) is a design constraint

## Requirement

Create a comprehensive accessibility design plan that a developer with no accessibility knowledge can use to implement the component correctly on the first attempt.

The plan should cover:
- Semantic structure
- ARIA implementation (pattern mapping, attributes)
- Keyboard interaction model
- Focus management
- State communication
- Visual accessibility (error color not sole indicator)
- Content accessibility (error message clarity)
- Testing strategy
- Implementation tasks with a11y-critic checkpoints

## Scope Hints

This is a **COMPLEX** difficulty fixture — four interdependent concerns must all be addressed at depth: error identification (1.4.1 + 3.3.1), focus management on step advancement and on validation, cognitive load management in the error summary, and the cross-step error consolidation at final submit. The plan should be 5-7 pages. Focus on:

1. Error identification beyond color: each invalid field needs an icon or shape in addition to red treatment; `aria-invalid="true"` on inputs; programmatic association via `aria-describedby` to error message IDs
2. Error summary panel: focus management when errors appear — focus should move to the summary; links in summary should navigate to the invalid field (not just scroll); `role="alert"` or `aria-live="assertive"` for dynamic appearance
3. Blur-time validation: real-time error announcement strategy — announcing an error as the user leaves each field can be disruptive; plan an announcement strategy that doesn't interrupt the user mid-form
4. Cognitive load on submit-time errors: showing all errors at once vs. one-at-a-time; document the tradeoff and justify the choice
5. Step navigation with errors: if the user tries to advance with errors, what does focus do? If they navigate back to a prior step, are errors preserved and announced?
6. Cross-step final submit: the consolidated error list spans all four steps; the links in that list must navigate the user back to the right step and field

## What Success Looks Like

An excellent plan would:
- ✓ Cite WCAG 3.3.1 (Error Identification), 3.3.3 (Error Suggestion), and 1.4.1 (Use of Color) as the core requirements
- ✓ Specify `aria-invalid="true"` on invalid inputs and `aria-describedby` pointing to the error message element ID
- ✓ Plan the error summary as a `role="alert"` or `aria-live="assertive"` region that appears dynamically; focus moves to it on submit-time errors
- ✓ Specify that error summary links navigate the user to the invalid field AND focus that field
- ✓ Address the blur-time announcement strategy: options include aria-live="polite" (low priority, waits for user to pause), delaying announcement by 500ms, or only showing errors on blur after the first submit attempt
- ✓ Address cognitive load: document the tradeoff between showing all errors simultaneously vs. progressive disclosure; recommend a specific approach with justification
- ✓ Plan the non-color error indicator: icon (✗ or warning triangle) in addition to red treatment; cite WCAG 1.4.1
- ✓ Cite WCAG 4.1.3 (Status Messages) for error summary announcement without focus movement
- ✓ Plan cross-step error handling: links in final submit error list navigate back to the correct step AND the correct field, with focus sent to that field

## What Would Be Below Expectations

- ✗ Adding `aria-label` to error messages but not `aria-describedby` on the input (the association must be bidirectional from the input)
- ✗ Using `role="alert"` for blur-time inline validation — too aggressive, will interrupt screen reader users after every field
- ✗ Error summary that announces "errors occurred" without linking to individual fields
- ✗ No plan for focus management when the error summary appears (focus stays on submit button)
- ✗ No plan for the cross-step consolidated error list in the final step
- ✗ Cognitive load section missing or vague ("show errors clearly") — must recommend a specific approach
- ✗ Red border and red text as the only error indicators (fails 1.4.1 for colorblind users)
- ✗ `aria-required="true"` mentioned but `aria-invalid="true"` omitted (they serve different purposes)
