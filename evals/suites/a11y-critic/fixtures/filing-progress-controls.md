# Fixture: Filing Progress Controls

## Recent Changes (PR #211)

Closes HELP-64. Redesigns the filing-assistant step navigation with a
cleaner visual style: step circles now use a lighter, less heavy-handed
outline so the progress bar reads as understated rather than distracting,
and every focusable control across the four steps got an explicit
`:focus-visible` treatment matching the new palette.

## Component Code

```jsx
import React, { useState } from 'react';
import './FilingProgressControls.css';

const STEPS = ['Your Information', 'Case Details', 'Review Answers', 'Submit & Print'];

const FilingProgressNav = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [filingRole, setFilingRole] = useState('');

  return (
    <div className="filing-assistant">
      <ol className="step-nav" aria-label="Filing progress">
        {STEPS.map((label, index) => (
          <li
            key={label}
            className={index === currentStep ? 'step current' : 'step'}
            aria-current={index === currentStep ? 'step' : undefined}
          >
            <span className="step-circle" aria-hidden="true">{index + 1}</span>
            <span className="step-label">{label}</span>
          </li>
        ))}
      </ol>

      {currentStep === 0 && (
        <section aria-labelledby="step-1-heading" className="filing-step">
          <h2 id="step-1-heading">Your Information</h2>

          <label htmlFor="filer-name">Full legal name</label>
          <input id="filer-name" type="text" name="filerName" className="text-input" />

          <label htmlFor="filer-address">Mailing address</label>
          <input id="filer-address" type="text" name="filerAddress" className="text-input" />

          <label htmlFor="filer-phone">Phone number</label>
          <input id="filer-phone" type="tel" name="filerPhone" className="text-input" />
        </section>
      )}

      {currentStep === 1 && (
        <section aria-labelledby="step-2-heading" className="filing-step">
          <h2 id="step-2-heading">Case Details</h2>

          <fieldset className="role-fieldset">
            <legend>You are filing as</legend>
            <label className="radio-option">
              <input
                type="radio"
                name="filingRole"
                value="tenant"
                checked={filingRole === 'tenant'}
                onChange={() => setFilingRole('tenant')}
              />
              Tenant
            </label>
            <label className="radio-option">
              <input
                type="radio"
                name="filingRole"
                value="landlord"
                checked={filingRole === 'landlord'}
                onChange={() => setFilingRole('landlord')}
              />
              Landlord
            </label>
          </fieldset>
        </section>
      )}

      <div className="step-controls">
        <button
          type="button"
          className="btn-back"
          disabled={currentStep === 0}
          onClick={() => setCurrentStep((s) => Math.max(0, s - 1))}
        >
          Back
        </button>
        <button
          type="button"
          className="btn-continue"
          onClick={() => setCurrentStep((s) => Math.min(STEPS.length - 1, s + 1))}
        >
          {currentStep === STEPS.length - 1 ? 'Submit' : 'Continue'}
        </button>
      </div>
    </div>
  );
};

export default FilingProgressNav;
```

## CSS

```css
.filing-assistant {
  max-width: 640px;
  margin: 24px auto;
  padding: 24px;
  background: #ffffff;
  font-family: sans-serif;
}

.step-nav {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0 0 32px 0;
  counter-reset: none;
}

.step {
  flex: 1;
  text-align: center;
  color: #667085;
  font-size: 13px;
}

.step-circle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 2px solid #667085;
  margin-bottom: 6px;
}

.step.current .step-circle {
  border-color: #1d4ed8;
  color: #1d4ed8;
  font-weight: 600;
}

.filing-step h2 {
  font-size: 20px;
  color: #101828;
  margin-bottom: 20px;
}

.filing-step label {
  display: block;
  margin: 14px 0 6px;
  font-weight: 600;
  color: #344054;
  font-size: 15px;
}

.text-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #cccccc;
  border-radius: 6px;
  font-size: 15px;
  box-sizing: border-box;
}

.text-input:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px #b8b8b8;
}

.role-fieldset {
  border: none;
  padding: 0;
  margin: 14px 0;
}

.role-fieldset legend {
  font-weight: 600;
  color: #344054;
  font-size: 15px;
  margin-bottom: 8px;
  padding: 0;
}

.radio-option {
  display: block;
  margin: 10px 0;
  font-size: 15px;
  color: #344054;
}

.radio-option input[type="radio"]:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px #b8b8b8;
}

.step-controls {
  display: flex;
  justify-content: space-between;
  margin-top: 28px;
}

.btn-back,
.btn-continue {
  padding: 10px 22px;
  border-radius: 6px;
  font-size: 15px;
  cursor: pointer;
}

.btn-back {
  background: #ffffff;
  border: 1px solid #667085;
  color: #344054;
}

.btn-back:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.btn-continue {
  background: #1d4ed8;
  border: none;
  color: #ffffff;
}

.btn-back:focus-visible,
.btn-continue:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px #ffffff, 0 0 0 4px #b8b8b8;
}
```

## Expected Behavior

- Self-represented filers move through four steps (Your Information, Case Details, Review Answers, Submit & Print) using Back/Continue.
- The step indicator shows progress with a row of numbered circles.
- Text fields, radio buttons, and both navigation buttons all show a focus style when reached via keyboard, using `:focus-visible` so mouse clicks don't trigger it.

## Accessibility Features Present

✓ Every text input has a label associated via htmlFor
✓ The filing-role choice uses fieldset/legend, not a bare pair of radio inputs
✓ Every focusable control (inputs, radios, both buttons) has a dedicated `:focus-visible` style, not just a browser default
✓ The disabled Back button on step 1 uses the disabled attribute, not just visual styling
✓ Step navigation uses ordered-list semantics with an aria-label identifying its purpose
✓ The current step carries aria-current="step" so screen reader users learn which step is active, not only sighted users via the blue circle

## Accessibility Issues (Planted)

1. **MUST-FIND / MAJOR: The custom focus indicator's box-shadow color fails the 3:1 minimum contrast against its adjacent background.** Every `:focus-visible` rule in this stylesheet uses `box-shadow: 0 0 0 Npx #b8b8b8` against a white (`#ffffff`) panel background. Computing relative luminance for `#b8b8b8` (≈0.479) against white (1.0) gives a contrast ratio of roughly 2:1 — well below the 3:1 minimum WCAG 1.4.11 requires for a UI component's focus state. This affects every text input, both radio buttons, and both Back/Continue buttons; the entire step-nav has no compliant keyboard focus indicator anywhere.
   - Evidence: `filing-progress-controls.md` — `.text-input:focus-visible`, `.radio-option input[type="radio"]:focus-visible`, and `.btn-back:focus-visible, .btn-continue:focus-visible` all use `#b8b8b8` against `.filing-assistant { background: #ffffff }`
   - WCAG: 1.4.11 Non-text Contrast
   - Impact: Keyboard users with low vision, and keyboard users generally under poor lighting or on lower-quality displays, cannot reliably see which control currently has focus anywhere in this flow
   - User group: Low-vision users, keyboard users
   - Fix: Darken the focus indicator color to something that clears 3:1 against white, e.g. `#0b3d91` or `#1d4ed8` (the same blue already used for the current-step circle and Continue button), and re-verify against every background the focus ring appears on

2. **MUST-FIND / MAJOR: The text input border color fails the 3:1 minimum contrast against the input's background.** `.text-input` uses `border: 1px solid #cccccc` against a white background. Computing relative luminance for `#cccccc` (≈0.604) against white gives approximately 1.6:1 — below the 3:1 minimum WCAG 1.4.11 requires for the boundary of a UI component that has no other visual means of indicating its edges (no fill color difference, no box-shadow at rest). A user with low vision may not be able to tell where the input field begins and ends against the surrounding white page.
   - Evidence: `filing-progress-controls.md` — `.text-input { border: 1px solid #cccccc; }` against `.filing-assistant { background: #ffffff }`, no other boundary cue
   - WCAG: 1.4.11 Non-text Contrast
   - Impact: Low-vision users may not perceive the input field's boundary, especially on the address and phone fields where content is otherwise unremarkable text on white
   - User group: Low-vision users
   - Fix: Darken the border to something like `#667085` or `#344054` (already used elsewhere in this stylesheet for label/text color) for a compliant boundary

## Difficulty Level

**HAS-BUGS** — Both defects are computable, unambiguous contrast failures rather than subtle interaction bugs: the hex values are stated directly in the CSS and the relevant background is equally explicit. The redesign in the PR description ("lighter, less heavy-handed") is a plausible, realistic reason a team would land on a color this far under the minimum — a lighter focus ring was an explicit design goal, and nobody separately verified it against the 3:1 non-text contrast floor.

## Frameworks & Environment

React 18+, standard CSS

## Notes

This fixture isolates WCAG 1.4.11 (Non-text Contrast) as its subject:

1. **Two related, independently-verifiable defects** — the focus indicator (present on five different controls, all sharing one under-contrast color) and the input border (a separate element type, separate color, same failure mode). A reviewer should recognize these as two distinct instances of the same underlying gap (nobody checked non-text contrast against the redesigned palette), not one.
2. **False-positive resistance**: body text throughout this component (labels, step names, headings) uses dark, high-contrast colors (`#344054`, `#101828`) well above the 4.5:1 text-contrast minimum, and the step-circle borders (`#667085` resting, `#1d4ed8` current) and the Back button's border (`#667085`) are all comfortably above 3:1. A reviewer should not confuse this fixture's actual defect (non-text UI component contrast, 3:1 threshold) with text contrast (4.5:1 threshold), and should not flag any of these already-compliant borders as sharing the same problem as the focus indicator and the text-input border.

Expected verdict: REVISE.
