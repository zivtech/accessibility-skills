# Fixture: Dense Admin Settings Panel With Jargon

## Component Code

```jsx
import React, { useState } from 'react';

// CSS
/*
.admin-settings {
  font-family: system-ui, sans-serif;
  background: #fff;
  padding: 24px;
  max-width: 1100px;
}

.settings-header {
  margin-bottom: 24px;
}

.settings-header h1 {
  font-size: 20px;
  margin: 0 0 4px;
  font-weight: 700;
}

.settings-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 24px;
  /* BUG: 3-column layout at small viewport — no reflow below 320px CSS pixels */
}

.settings-column h2 {
  /* BUG: 9px font size — below readable threshold, fails WCAG 1.4.4 and cognitive legibility */
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #666;
  margin: 0 0 16px;
}

.toggle-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
  /* BUG: 12 toggles with no visual grouping into sub-categories — cognitive overload */
}

.toggle-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.toggle-label {
  font-size: 13px;
  color: #111;
  flex: 1;
  /* BUG: Technical jargon like "Enable HSTS preloading" appears with no tooltip or glossary link */
}

.toggle-switch input[type="checkbox"] {
  /* All checkboxes are native <input type="checkbox"> — keyboard operable, NOT a bug */
  width: 36px;
  height: 20px;
  cursor: pointer;
}

.required-asterisk {
  /* BUG: Required fields marked with tiny red asterisk only — no text, no aria-required */
  color: #e53e3e;
  font-size: 9px;
  margin-left: 2px;
}

.error-inline {
  /* BUG: Error messages use codes like "ERR_CSP_001" not human descriptions */
  font-size: 11px;
  color: #e53e3e;
  margin-top: 4px;
}

.settings-actions {
  margin-top: 32px;
  display: flex;
  justify-content: flex-end;
  /* BUG: Save button is at the bottom right — no unsaved-changes indicator anywhere
     in the UI; users may navigate away without realizing changes are pending */
}

.btn-save {
  background: #2b6cb0;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 8px 24px;
  font-size: 14px;
  cursor: pointer;
  font-weight: 600;
}

.btn-save:focus-visible {
  outline: 2px solid #2b6cb0;
  outline-offset: 2px;
}
*/

const SECURITY_TOGGLES = [
  { id: 'hsts', label: 'Enable HSTS preloading', required: true, error: null },
  { id: 'csp', label: 'Enforce Content Security Policy', required: false, error: 'ERR_CSP_001' },
  { id: 'sri', label: 'Enable SRI validation', required: false, error: null },
  { id: 'cors', label: 'Strict CORS origin checking', required: true, error: null },
];

const PERFORMANCE_TOGGLES = [
  { id: 'brotli', label: 'Enable Brotli compression', required: false, error: null },
  { id: 'h2push', label: 'HTTP/2 server push', required: false, error: null },
  { id: 'prefetch', label: 'Speculative prefetch', required: false, error: null },
  { id: 'stale-wri', label: 'stale-while-revalidate cache', required: false, error: null },
];

const LOGGING_TOGGLES = [
  { id: 'access-log', label: 'Structured access logging', required: true, error: null },
  { id: 'error-log', label: 'Extended error diagnostics', required: false, error: null },
  { id: 'audit-log', label: 'Immutable audit trail (WAL)', required: false, error: null },
  { id: 'metrics', label: 'Prometheus metrics endpoint', required: false, error: null },
];

const AdminSettings = () => {
  const [securityValues, setSecurityValues] = useState(
    Object.fromEntries(SECURITY_TOGGLES.map((t) => [t.id, false]))
  );
  const [performanceValues, setPerformanceValues] = useState(
    Object.fromEntries(PERFORMANCE_TOGGLES.map((t) => [t.id, false]))
  );
  const [loggingValues, setLoggingValues] = useState(
    Object.fromEntries(LOGGING_TOGGLES.map((t) => [t.id, false]))
  );

  // BUG: No unsaved-changes state tracked — user could navigate away silently
  const [saved, setSaved] = useState(true);

  const handleToggle = (group, id) => {
    setSaved(false);
    if (group === 'security') {
      setSecurityValues((prev) => ({ ...prev, [id]: !prev[id] }));
    } else if (group === 'performance') {
      setPerformanceValues((prev) => ({ ...prev, [id]: !prev[id] }));
    } else {
      setLoggingValues((prev) => ({ ...prev, [id]: !prev[id] }));
    }
    // BUG: setSaved(false) is called but no visual indicator of "unsaved changes"
    // is rendered anywhere; the save button appearance does not change
  };

  const handleSave = () => {
    // Simulate save
    setSaved(true);
  };

  const renderToggleGroup = (toggles, values, group) => (
    /* BUG: 12 toggles across 3 columns with no sub-grouping headers or visual separators
       within columns — cognitive overload for users managing complex config */
    <div className="toggle-group">
      {toggles.map((t) => (
        <div key={t.id} className="toggle-row">
          <label className="toggle-label" htmlFor={t.id}>
            {/* BUG: Technical jargon label with no tooltip, glossary link, or plain-English description */}
            {t.label}
            {t.required && (
              /* BUG: Required indicated only by red asterisk — no aria-required on input,
                 no visually-hidden "required" text, no legend or form instruction */
              <span className="required-asterisk" aria-hidden="true">*</span>
            )}
          </label>
          {/* All checkboxes use native <input type="checkbox"> — keyboard accessible, NOT a bug */}
          <input
            type="checkbox"
            id={t.id}
            className="toggle-switch"
            checked={values[t.id]}
            onChange={() => handleToggle(group, t.id)}
          />
          {t.error && (
            /* BUG: Error message is a code string "ERR_CSP_001" — no human-readable description,
               no link to documentation, no ARIA association to the field */
            <span className="error-inline" role="alert">
              {t.error}
            </span>
          )}
        </div>
      ))}
    </div>
  );

  return (
    <main className="admin-settings">
      <div className="settings-header">
        <h1>Server Configuration</h1>
        <p style={{ fontSize: '13px', color: '#555', margin: 0 }}>
          Advanced settings for production deployment.
        </p>
      </div>

      {/* BUG: 3-column layout with 9px section headers — fails magnification/reflow and cognitive legibility */}
      <div className="settings-grid">
        <div className="settings-column">
          {/* BUG: 9px font on column headers */}
          <h2>Security</h2>
          {renderToggleGroup(SECURITY_TOGGLES, securityValues, 'security')}
        </div>
        <div className="settings-column">
          <h2>Performance</h2>
          {renderToggleGroup(PERFORMANCE_TOGGLES, performanceValues, 'performance')}
        </div>
        <div className="settings-column">
          <h2>Logging</h2>
          {renderToggleGroup(LOGGING_TOGGLES, loggingValues, 'logging')}
        </div>
      </div>

      {/* BUG: No unsaved-changes indicator near the save button or at top of form */}
      <div className="settings-actions">
        {/* Save button is keyboard-accessible native <button> — NOT a bug */}
        <button className="btn-save" onClick={handleSave}>
          Save Changes
        </button>
      </div>
    </main>
  );
};

export default AdminSettings;
```

## Expected Behavior

- Admin settings panel with organized, labeled groups of toggles
- Section headers use readable font size (minimum 14px body, 12px minimum for secondary text)
- Technical terms include tooltips, glossary links, or plain-English descriptions
- Toggles are grouped into logical sub-sections within each column
- Unsaved changes are communicated visually (e.g., "You have unsaved changes" banner or disabled-state change on the button)
- Required fields are marked with `aria-required="true"` on the input and a text indicator (not asterisk-only)
- Error messages describe the problem in plain English with suggested remediation
- Layout reflows to single column below 320px

## Accessibility Features Present

- All 12 toggles use native `<input type="checkbox">` elements — keyboard operable
- Each checkbox has a `<label>` associated via `htmlFor`/`id`
- Save button is a native `<button>` with keyboard focus support and `focus-visible` outline
- Page has `<h1>` and `<h2>` landmark headings
- Error span uses `role="alert"` for immediate announcement

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Dense 3-column layout with 9px column headers** — The settings grid uses a fixed 3-column CSS grid with no responsive breakpoints. Section header `<h2>` elements are set to `font-size: 9px` — well below the WCAG 1.4.4 minimum and below any readable threshold at 1x zoom. At 200% magnification, the 3-column layout produces horizontal overflow rather than reflowing to a single column.
   - Evidence: `.settings-grid { grid-template-columns: 1fr 1fr 1fr }` with no media query; `.settings-column h2 { font-size: 9px }` in component CSS
   - User group: Users with low vision using screen magnification; users with cognitive disabilities
   - Expected fix: Add `@media (max-width: 640px)` breakpoint switching grid to single column; increase h2 font-size to minimum 12px

2. **MAJOR: Technical jargon with no tooltips or glossary** — All 12 toggle labels use technical terms (HSTS preloading, SRI validation, Brotli, stale-while-revalidate, WAL) with no tooltip, popover, glossary link, or plain-English description. A non-expert administrator cannot determine what enabling each toggle will do.
   - Evidence: `SECURITY_TOGGLES`, `PERFORMANCE_TOGGLES`, `LOGGING_TOGGLES` arrays contain jargon labels; `/* BUG: Technical jargon label with no tooltip */` comment in render function
   - User group: Users with cognitive disabilities; non-specialist administrators
   - Expected fix: Add `title` attribute or accessible tooltip component with plain-English description for each jargon term

3. **MAJOR: 12 ungrouped toggles cause cognitive overload** — All 12 toggles are rendered in a flat list within each column with no sub-grouping, visual separators, or progressive disclosure. There are no sub-headings, no collapsible sections, and no visual hierarchy within the three flat lists.
   - Evidence: `renderToggleGroup` renders a flat `<div class="toggle-group">` with no internal structure; `/* BUG: 12 toggles with no sub-grouping */` comment in render
   - User group: Users with cognitive and attention disabilities; all users under high cognitive load
   - Expected fix: Add sub-section `<fieldset>`/`<legend>` groupings within each column or collapsible accordion sections

4. **MAJOR: No unsaved-changes indicator** — `setSaved(false)` is called on every toggle change but no visual indicator is rendered anywhere. The save button does not change appearance, no banner appears, and no `aria-live` region announces pending changes. Users can navigate away without knowing changes are unsaved.
   - Evidence: `saved` state is set to `false` on change but never used in any rendered JSX; `/* BUG: setSaved(false) is called but no visual indicator */` comment in handleToggle
   - User group: Users with cognitive and memory disabilities; all users
   - Expected fix: Render a visible "You have unsaved changes" notice when `saved === false`; add `aria-live="polite"` announcement

5. **MINOR: Error messages use opaque codes, not descriptions** — The `ERR_CSP_001` error string rendered in the error span provides no human-readable description of the problem and no remediation guidance. Screen reader users hear "ERR_CSP_001" with no context.
   - Evidence: `SECURITY_TOGGLES` contains `error: 'ERR_CSP_001'`; rendered as-is in `<span role="alert">`
   - User group: All users, especially users with cognitive disabilities
   - Expected fix: Map error codes to human-readable descriptions ("Content Security Policy conflict — disable SRI validation first")

6. **MINOR: Required fields marked with asterisk only, no `aria-required`** — Required toggles render a `<span aria-hidden="true">*</span>` with no `aria-required="true"` on the input, no visually-hidden "required" text, and no form-level legend explaining the asterisk convention.
   - Evidence: `t.required && <span className="required-asterisk" aria-hidden="true">*</span>` — `aria-hidden` explicitly hides from screen readers; no `aria-required` on the `<input>`
   - User group: Screen reader users
   - Expected fix: Add `aria-required="true"` to inputs where `t.required === true`; add a form-level note explaining the asterisk

## Difficulty Level

**HAS-BUGS** — New dimensions: cognitive overload and magnification/reflow. All 12 toggle checkboxes are correctly associated with labels and keyboard-operable — these are intentional true negatives. The challenge is distinguishing the correctly implemented keyboard layer from the cognitive and magnification failures layered on top. The error span correctly uses `role="alert"` — the bug is the opaque content, not the ARIA pattern.

## Frameworks

React 18+, CSS Grid, native HTML form elements
