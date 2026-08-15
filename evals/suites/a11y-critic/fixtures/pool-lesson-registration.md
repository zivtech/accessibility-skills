# Fixture: Pool Lesson Registration

## Recent Changes (PR #329)

Closes AQUA-77. Completes the accessibility remediation pass on the swim
lesson registration form: every field now has an associated label, error
messages are linked to their fields via aria-describedby and announced
through a persistent status region, the lesson-level choice uses
fieldset/legend, and the submit confirmation announces without requiring
the parent to move focus.

## Component Code

```jsx
import React, { useState } from 'react';
import './PoolLessonRegistration.css';

const LEVELS = ['Level 1 — Water Introduction', 'Level 2 — Basic Skills', 'Level 3 — Stroke Development'];

const PoolLessonRegistration = () => {
  const [swimmerName, setSwimmerName] = useState('');
  const [age, setAge] = useState('');
  const [level, setLevel] = useState('');
  const [emergencyContact, setEmergencyContact] = useState('');
  const [medicalNotes, setMedicalNotes] = useState('');
  const [errors, setErrors] = useState({});
  const [submitted, setSubmitted] = useState(false);

  const validate = () => {
    const nextErrors = {};
    if (!swimmerName.trim()) nextErrors.swimmerName = 'Enter the swimmer’s full name.';
    if (!age || age < 3 || age > 17) nextErrors.age = 'Enter an age between 3 and 17.';
    if (!level) nextErrors.level = 'Choose a lesson level.';
    if (!emergencyContact.trim()) nextErrors.emergencyContact = 'Enter an emergency contact phone number.';
    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(false);
    if (validate()) {
      setSubmitted(true);
    }
  };

  return (
    <form className="pool-registration-form" aria-labelledby="registration-heading" onSubmit={handleSubmit} noValidate>
      <h2 id="registration-heading">Swim Lesson Registration</h2>

      <div role="alert" className="error-summary">
        {Object.keys(errors).length > 0 && (
          <>
            <p className="error-summary-title">Please fix the following:</p>
            <ul>
              {Object.values(errors).map((message) => (
                <li key={message}>{message}</li>
              ))}
            </ul>
          </>
        )}
      </div>

      <div className="form-field">
        <label htmlFor="swimmer-name">Swimmer&rsquo;s full name</label>
        <input
          id="swimmer-name"
          type="text"
          autoComplete="name"
          value={swimmerName}
          aria-invalid={Boolean(errors.swimmerName)}
          aria-describedby={errors.swimmerName ? 'swimmer-name-error' : undefined}
          onChange={(e) => setSwimmerName(e.target.value)}
        />
        {errors.swimmerName && (
          <span id="swimmer-name-error" className="field-error">{errors.swimmerName}</span>
        )}
      </div>

      <div className="form-field">
        <label htmlFor="swimmer-age">Age</label>
        <input
          id="swimmer-age"
          type="number"
          min="3"
          max="17"
          value={age}
          aria-invalid={Boolean(errors.age)}
          aria-describedby={errors.age ? 'swimmer-age-error' : undefined}
          onChange={(e) => setAge(e.target.value)}
        />
        {errors.age && <span id="swimmer-age-error" className="field-error">{errors.age}</span>}
      </div>

      <fieldset className="level-fieldset">
        <legend>Lesson level</legend>
        {LEVELS.map((option) => (
          <label key={option} className="radio-option">
            <input
              type="radio"
              name="level"
              value={option}
              checked={level === option}
              onChange={() => setLevel(option)}
              aria-describedby={errors.level ? 'level-error' : undefined}
            />
            {option}
          </label>
        ))}
        {errors.level && <span id="level-error" className="field-error">{errors.level}</span>}
      </fieldset>

      <div className="form-field">
        <label htmlFor="emergency-contact">Emergency contact phone number</label>
        <input
          id="emergency-contact"
          type="tel"
          autoComplete="tel"
          value={emergencyContact}
          aria-invalid={Boolean(errors.emergencyContact)}
          aria-describedby={errors.emergencyContact ? 'emergency-contact-error' : undefined}
          onChange={(e) => setEmergencyContact(e.target.value)}
        />
        {errors.emergencyContact && (
          <span id="emergency-contact-error" className="field-error">{errors.emergencyContact}</span>
        )}
      </div>

      <div className="form-field">
        <label htmlFor="medical-notes">Medical notes (optional)</label>
        <textarea
          id="medical-notes"
          value={medicalNotes}
          aria-describedby="medical-notes-help"
          onChange={(e) => setMedicalNotes(e.target.value)}
        />
        <span id="medical-notes-help" className="field-help">
          Include any allergies or medical conditions the instructor should know about.
        </span>
      </div>

      <button type="submit" className="submit-button">Register</button>

      <div role="status" className="submit-confirmation">
        {submitted && 'Registration submitted. You will receive a confirmation email shortly.'}
      </div>
    </form>
  );
};

export default PoolLessonRegistration;
```

## CSS

```css
.pool-registration-form {
  max-width: 460px;
  margin: 24px auto;
  padding: 24px;
  background: #ffffff;
  border: 1px solid #d5dbe0;
  border-radius: 8px;
  font-family: sans-serif;
}

.pool-registration-form h2 {
  font-size: 19px;
  color: #17303d;
  margin: 0 0 18px 0;
}

.error-summary {
  border-radius: 6px;
}

.error-summary:not(:empty) {
  background: #fdeceb;
  border: 2px solid #a3352a;
  padding: 14px 16px;
  margin-bottom: 18px;
}

.error-summary-title {
  margin: 0 0 6px 0;
  font-weight: 700;
  color: #7a251c;
}

.error-summary ul {
  margin: 0;
  padding-left: 20px;
  color: #7a251c;
}

.form-field {
  margin-bottom: 16px;
}

.form-field label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  color: #2b3a44;
  font-size: 14px;
}

.form-field input,
.form-field textarea {
  width: 100%;
  padding: 9px 10px;
  border: 2px solid #4a5a63;
  border-radius: 5px;
  font-size: 15px;
  box-sizing: border-box;
}

.form-field input:focus-visible,
.form-field textarea:focus-visible,
.level-fieldset input:focus-visible {
  outline: 3px solid #0b3d91;
  outline-offset: 2px;
}

.field-error {
  display: block;
  color: #a3352a;
  font-size: 13px;
  margin-top: 4px;
}

.field-help {
  display: block;
  color: #566670;
  font-size: 13px;
  margin-top: 4px;
}

.level-fieldset {
  border: none;
  padding: 0;
  margin: 0 0 16px 0;
}

.level-fieldset legend {
  font-weight: 600;
  color: #2b3a44;
  font-size: 14px;
  margin-bottom: 8px;
  padding: 0;
}

.radio-option {
  display: block;
  margin: 8px 0;
  font-size: 14px;
  color: #2b3a44;
}

.submit-button {
  width: 100%;
  padding: 11px;
  background: #0b3d91;
  color: #ffffff;
  border: none;
  border-radius: 6px;
  font-size: 15px;
  cursor: pointer;
  margin-top: 6px;
}

.submit-button:focus-visible {
  outline: 3px solid #17303d;
  outline-offset: 2px;
}

.submit-confirmation {
  margin-top: 14px;
  font-size: 14px;
  color: #205c2f;
}
```

## Expected Behavior

- A parent registers a swimmer for lessons: name, age, lesson level, an emergency contact number, and optional medical notes.
- Submitting with missing or invalid fields shows an error summary and per-field error text; submitting successfully shows a confirmation message.
- All fields remain in place across submission attempts — the form does not remount on error or success.

## Accessibility Features Present

✓ Every input and the textarea have a label associated via htmlFor
✓ Lesson-level choice uses fieldset/legend
✓ Invalid fields carry aria-invalid and aria-describedby pointing to their specific error text
✓ The error summary is a persistently-rendered role="alert" element (present from initial render, never conditionally mounted or unmounted) whose text content changes; only its decorative border/background react to :not(:empty), never its display or presence in the DOM
✓ The submit confirmation is a persistently-rendered role="status" element for the same reason — its text is set from empty to populated, not mounted fresh, and nothing about its display or presence in the DOM ever changes
✓ The medical notes field is clearly marked optional in its label text, with no required attribute or asterisk
✓ Name and phone fields use autoComplete hints (name, tel)
✓ Focus indicators are visible and use dark, high-contrast colors across every focusable control

## Accessibility Issues (None Planted — Clean Baseline)

No accessibility bugs are planted in this fixture. Everything from this
heading down is eval metadata kept below the blind cut line (runners strip
this heading and all following sections from model prompts).

## Difficulty Level

CLEAN — this is a remediated-framing control fixture. The changelog above uses the same "closes a remediation ticket" framing as this suite's HAS-BUGS remediated-code-with-residue fixtures, but here the remediation is actually complete and correct: there is no residue to find. Specifically, the error-summary and submit-confirmation regions avoid the mount-with-content trap planted in the sibling fixture `seed-availability-panel` — both are rendered unconditionally from initial mount and never unmounted, never given a changing `key`, and never toggled via `hidden`/`display:none` (the error summary's CSS reacts to `:not(:empty)` for decorative border/background only, never for `display`). Only their text content changes, so `role="alert"`/`role="status"` correctly observe every update.

## Frameworks & Environment

React 18+, standard CSS

## Notes

This fixture is a methodological control: it tests whether "this code was recently remediated for accessibility" framing alone induces an unearned REVISE verdict, independent of the code's actual state. Two deliberate false-positive traps reinforce this:

1. **The medical notes field has no required indicator, unlike every other field.** This is correct — it is genuinely optional, and its label says so in words ("Medical notes (optional)") rather than relying on the *absence* of a required marker to communicate that. A reviewer who flags this as "inconsistent required-field marking" has misread an intentional, correctly-communicated distinction as an error.
2. **The submit confirmation uses `role="status"` (polite), not `role="alert"` (assertive).** This is the correct choice for a non-urgent success confirmation — interrupting a screen reader user mid-task for a routine "your registration was submitted" message is worse UX than a polite announcement, which is exactly what alerts are meant to avoid for non-critical content. A reviewer who suggests upgrading this to `role="alert"` "for a stronger announcement" would be recommending a regression, not an improvement.

Expected verdict: ACCEPT. Any REVISE or REJECT verdict on this fixture — especially one that cites the changelog framing itself ("recently touched code likely still has issues") rather than a specific, real defect in the component — is a false positive and should be treated as a signal that the reviewer over-weighted narrative context over verification of the actual code.
