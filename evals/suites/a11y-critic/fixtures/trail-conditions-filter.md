# Fixture: Trail Conditions Filter

## Component Code

```jsx
import React, { useState } from 'react';
import './TrailConditionsFilter.css';

const DIFFICULTIES = ['Easy', 'Moderate', 'Strenuous'];
const REGIONS = ['Northern Ridge', 'Riverside', 'Highlands', 'Coastal Loop'];

const TrailConditionsFilter = ({ onApply }) => {
  const [selectedDifficulties, setSelectedDifficulties] = useState([]);
  const [region, setRegion] = useState('');

  const toggleDifficulty = (difficulty) => {
    setSelectedDifficulties((prev) =>
      prev.includes(difficulty) ? prev.filter((d) => d !== difficulty) : [...prev, difficulty]
    );
  };

  const canApply = selectedDifficulties.length > 0;

  return (
    <form
      className="trail-filter"
      aria-labelledby="filter-heading"
      onSubmit={(e) => {
        e.preventDefault();
        onApply({ selectedDifficulties, region });
      }}
    >
      <h2 id="filter-heading">Filter Trail Conditions</h2>

      <fieldset className="difficulty-fieldset">
        <legend>Trail difficulty</legend>
        {DIFFICULTIES.map((difficulty) => (
          <label key={difficulty} className="checkbox-option">
            <input
              type="checkbox"
              checked={selectedDifficulties.includes(difficulty)}
              onChange={() => toggleDifficulty(difficulty)}
            />
            <span className="checkbox-visual" aria-hidden="true" />
            {difficulty}
          </label>
        ))}
      </fieldset>

      <label htmlFor="region-select" className="region-label">Region</label>
      <select id="region-select" value={region} onChange={(e) => setRegion(e.target.value)}>
        <option value="">All regions</option>
        {REGIONS.map((r) => (
          <option key={r} value={r}>{r}</option>
        ))}
      </select>

      <button
        type="submit"
        className="apply-button"
        disabled={!canApply}
        aria-disabled={!canApply}
        aria-describedby="apply-help"
      >
        Apply Filters
      </button>
      <p id="apply-help" className="apply-help">
        Select at least one trail difficulty to filter results.
      </p>
    </form>
  );
};

export default TrailConditionsFilter;
```

## CSS

```css
.trail-filter {
  max-width: 360px;
  padding: 20px;
  background: #ffffff;
  border: 1px solid #d5dbe0;
  border-radius: 8px;
  font-family: sans-serif;
}

.trail-filter h2 {
  font-size: 17px;
  margin: 0 0 16px 0;
  color: #1c2b36;
}

.difficulty-fieldset {
  border: none;
  padding: 0;
  margin: 0 0 18px 0;
}

.difficulty-fieldset legend {
  font-weight: 600;
  font-size: 14px;
  color: #35434d;
  margin-bottom: 8px;
  padding: 0;
}

.checkbox-option {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 8px 0;
  font-size: 14px;
  color: #35434d;
  cursor: pointer;
}

.checkbox-option input[type="checkbox"] {
  position: absolute;
  opacity: 0;
  width: 20px;
  height: 20px;
  margin: 0;
}

.checkbox-visual {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid #3a4750;
  border-radius: 4px;
  flex-shrink: 0;
  position: relative;
}

.checkbox-option input[type="checkbox"]:checked + .checkbox-visual {
  background: #0b3d91;
  border-color: #0b3d91;
}

.checkbox-option input[type="checkbox"]:checked + .checkbox-visual::after {
  content: '';
  position: absolute;
  left: 6px;
  top: 2px;
  width: 5px;
  height: 10px;
  border: solid #ffffff;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-option input[type="checkbox"]:focus-visible + .checkbox-visual {
  outline: 3px solid #0b3d91;
  outline-offset: 2px;
}

.region-label {
  display: block;
  font-weight: 600;
  font-size: 14px;
  color: #35434d;
  margin-bottom: 6px;
}

#region-select {
  width: 100%;
  padding: 9px 10px;
  border: 2px solid #3a4750;
  border-radius: 5px;
  font-size: 14px;
  margin-bottom: 18px;
  box-sizing: border-box;
}

#region-select:focus-visible {
  outline: 3px solid #0b3d91;
  outline-offset: 2px;
}

.apply-button {
  width: 100%;
  padding: 10px;
  background: #0b3d91;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  font-size: 15px;
  cursor: pointer;
}

.apply-button:disabled {
  background: #9aa7b0;
  cursor: not-allowed;
}

.apply-button:focus-visible {
  outline: 3px solid #0b3d91;
  outline-offset: 2px;
}

.apply-help {
  font-size: 13px;
  color: #566670;
  margin-top: 8px;
}
```

## Expected Behavior

- Visitors filter the trail conditions dashboard by difficulty (checkboxes, multi-select) and region (single-select dropdown).
- "Apply Filters" stays disabled until at least one difficulty is selected, with helper text explaining why.
- Every control shows a visible focus indicator when reached via keyboard, using `:focus-visible` so the ring only appears for keyboard interaction, not mouse clicks.
- Checked checkboxes fill solid and show a checkmark, not only a color change.

## Accessibility Features Present

✓ Difficulty checkboxes are grouped with fieldset/legend
✓ Region select has a label associated via htmlFor
✓ Custom checkbox visual indicates checked state with both a fill color and a checkmark glyph, not color alone
✓ Real `<input type="checkbox">` elements remain in the DOM (visually hidden via opacity, not display:none or removed), preserving native keyboard and screen reader behavior
✓ Disabled Apply button uses both the disabled attribute and aria-disabled, plus aria-describedby pointing to help text explaining why it's disabled
✓ Focus indicators use :focus-visible consistently across checkboxes, select, and button

## Accessibility Issues (None Planted — Clean Baseline)

No accessibility bugs are planted in this fixture. Everything from this
heading down is eval metadata kept below the blind cut line (runners strip
this heading and all following sections from model prompts).

## Difficulty Level

CLEAN — a genuinely well-built filter form intended as an over-flagging trap for WCAG 1.4.11 (Non-text Contrast), the same criterion tested as a defect in the sibling fixture `filing-progress-controls`. Every color pair here was chosen to clear 3:1 comfortably: the checkbox border and select border use `#3a4750` (~9.4:1 against white), and the focus indicator throughout uses `#0b3d91` (~9.7:1 against white) — both far above the 3:1 minimum, not a narrow pass.

## Frameworks & Environment

React 18+, standard CSS

## Notes

This fixture exists specifically to test false-positive resistance around two patterns that superficially resemble bugs but are not:

1. **`:focus-visible`-only styling, no bare `:focus` rule.** Every focus indicator in this stylesheet is scoped to `:focus-visible`, meaning a mouse click does not show the ring, only keyboard interaction does. A reviewer who tests by clicking with a mouse and concludes "no focus indicator" would be wrong — this is the correct, modern pattern (avoiding a focus ring on pointer interaction while preserving it for keyboard users), not a missing indicator.
2. **Non-default focus/border colors.** The focus ring and borders use a dark navy (`#0b3d91`) and dark slate (`#3a4750`) rather than a "traditional" bright blue. A reviewer should verify contrast computationally rather than assume an unfamiliar color choice is non-compliant; both clear 3:1 with a wide margin.
3. The visually-hidden checkbox technique (`opacity: 0` on a full-size, in-flow `<input>`, not `display: none` or `visibility: hidden`, with a custom `.checkbox-visual` sibling) preserves native checkbox keyboard and screen-reader behavior — the real input is still there, still labeled by its wrapping `<label>`, still focusable and operable exactly like a default checkbox. This should not be flagged as "checkbox is hidden from screen readers" — it is hidden only visually, from sighted users, in favor of the custom visual.

Expected verdict: ACCEPT, or ACCEPT-WITH-RESERVATIONS citing at most an enhancement-level suggestion. Any REVISE or REJECT verdict driven by a finding on this component is a false positive; flag it as evidence the fixture's rubric (or the reviewer) needs recalibration, per this suite's CLEAN-fixture discipline.
