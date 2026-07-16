# Fixture: File Input Without Proper Label and Error Messages

## Component Code

```jsx
import React, { useState } from 'react';

const BuggyFileInput = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.size > 5000000) {
      setError('File too large');
    } else {
      setSelectedFile(file);
      setError(null);
    }
  };

  return (
    <div className="file-upload">
      <div>Upload file</div>
      <input
        type="file"
        onChange={handleFileChange}
        accept=".pdf,.doc,.docx"
      />
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
    </div>
  );
};

export default BuggyFileInput;
```

## Expected Behavior

- File input has clear label
- Input is associated with label via htmlFor
- Error messages are associated with input via aria-describedby
- Input announces aria-invalid when error is present
- Help text (file type restrictions) associated with input

## Accessibility Features Present

✓ accept attribute specifies allowed file types
✓ Visual error message displayed

## Accessibility Issues (Planted Bugs)

1. **CRITICAL: Missing <label> element** — Visual "Upload file" text is a div, not a semantic label. Screen reader user cannot identify input purpose. Per HTML form semantics, file inputs must have <label> with htmlFor attribute.
   - Evidence: `file-input-no-labels.md:23` (div instead of label)
   - User group: Screen reader users (critical)
   - Expected: Should have <label htmlFor="file-input">Upload file</label>
   - Fix: Replace div with <label> and add htmlFor attribute to input

2. **CRITICAL: No aria-describedby linking to error message** — Error message is displayed but not associated with input. Screen reader user cannot know that error message relates to this input. Per WCAG 3.3.1 (Error Identification), errors must be associated with their fields.
   - Evidence: `file-input-no-labels.md:24-28` (error div has no id, input has no aria-describedby)
   - User group: Screen reader users (critical)
   - Expected: Error should have id, input should have aria-describedby="error-id"
   - Fix: Add aria-describedby linking input to error message

3. **MAJOR: No aria-invalid when error present** — When error is displayed, input should announce aria-invalid="true" to notify screen reader user of invalid state. Without it, user doesn't know input has an error.
   - Evidence: `file-input-no-labels.md:24-28` (no aria-invalid attribute)
   - User group: Screen reader users
   - Expected: Input should have aria-invalid={!!error}
   - Fix: Add aria-invalid attribute that toggles with error state

4. **MAJOR: File type restrictions not announced** — accept attribute specifies .pdf,.doc,.docx but this is not communicated to screen reader user. Help text should be associated with input via aria-describedby.
   - Evidence: `file-input-no-labels.md:26` (accept attribute not announced)
   - User group: Screen reader users
   - Expected: Help text should explain accepted file types
   - Fix: Add aria-describedby linking to help text about file types

## Difficulty Level

**HAS-BUGS** — File input missing fundamental form semantics. Label, error association, and validity announcement all missing.

## Frameworks & Environment

React 18+, standard HTML/CSS

## Difficulty Rating

A11y-critic should identify that file inputs require the same semantic rigor as text inputs: labels, error association, and validity announcement. This tests understanding of form accessibility patterns.
