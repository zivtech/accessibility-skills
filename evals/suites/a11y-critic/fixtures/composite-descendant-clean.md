# Fixture: Toolbar Composite with Non-Tabbable Descendants

## Component Code

```jsx
import React, { useState, useRef } from 'react';

// APG Toolbar pattern: a single Tab stop for the whole toolbar, with a
// roving tabindex. Arrow keys move among the buttons; only the active
// button is in the Tab sequence (tabindex="0"), the rest are tabindex="-1".
const FormatToolbar = ({ onCommand }) => {
  const buttons = ['bold', 'italic', 'underline', 'link'];
  const [active, setActive] = useState(0);
  const refs = useRef([]);

  const focusButton = (i) => {
    setActive(i);
    refs.current[i]?.focus();
  };

  const handleKeyDown = (e) => {
    switch (e.key) {
      case 'ArrowRight':
        e.preventDefault();
        focusButton((active + 1) % buttons.length);
        break;
      case 'ArrowLeft':
        e.preventDefault();
        focusButton((active - 1 + buttons.length) % buttons.length);
        break;
      case 'Home':
        e.preventDefault();
        focusButton(0);
        break;
      case 'End':
        e.preventDefault();
        focusButton(buttons.length - 1);
        break;
      default:
        break;
    }
  };

  return (
    <div role="toolbar" aria-label="Text formatting" onKeyDown={handleKeyDown}>
      {buttons.map((name, i) => (
        <button
          key={name}
          ref={(el) => (refs.current[i] = el)}
          type="button"
          tabIndex={i === active ? 0 : -1}
          aria-pressed={false}
          onClick={() => onCommand(name)}
        >
          {name}
        </button>
      ))}
    </div>
  );
};

export default FormatToolbar;
```

## CSS Styles

```css
[role="toolbar"] { display: flex; gap: 4px; }
[role="toolbar"] button { padding: 8px 12px; }
[role="toolbar"] button:focus-visible { outline: 3px solid #1a5fb4; outline-offset: 2px; }
```

## Expected Behavior

- One Tab press moves focus into the toolbar, landing on the active button.
- ArrowRight / ArrowLeft move focus among the four buttons (wrapping at the ends).
- Home / End jump to the first / last button.
- The button that currently has focus is the only one with `tabindex="0"`; the rest are `tabindex="-1"` (roving tabindex).
- A second Tab press moves focus out of the toolbar to the next control on the page — it does not step through the individual buttons.

## Accessibility Features Implemented

✓ `role="toolbar"` with an accessible name (`aria-label="Text formatting"`)
✓ Roving tabindex: exactly one button is Tab-focusable at a time
✓ ArrowLeft/ArrowRight/Home/End navigation per the WAI-ARIA APG Toolbar pattern
✓ Native `<button>` elements (correct role, Enter/Space activation)
✓ Visible focus indicator (`:focus-visible` outline)
✓ Descendants reached via the toolbar's documented arrow-key model, not via Tab

## Accessibility Issues

**NONE.** This is a CLEAN fixture — the component above is a correct implementation with no planted bugs. Everything from this heading down is eval metadata kept below the blind cut line (runners strip this heading and all following sections from model prompts).

The false-positive trap: three of the four buttons carry `tabindex="-1"`, so a keyboard-reachability check that counts only Tab stops sees a single stop and concludes the other three buttons are "unreachable." They are not — they are reached through the toolbar's documented ArrowLeft/ArrowRight/Home/End model. A non-tabbable descendant reached via a composite widget's documented internal keys is correct roving tabindex, not a keyboard-operability failure. A competent critic recognizes the APG Toolbar pattern and does not flag it.

## Frameworks & Environment

- React 18+
- No external libraries (vanilla roving-tabindex focus management)
- Works with any screen reader (NVDA, JAWS, VoiceOver)

## Difficulty Level

**CLEAN** — a correct composite-widget implementation that a Tab-only reachability sweep will wrongly flag. A11y-critic should:
1. Identify the WAI-ARIA APG Toolbar pattern by name.
2. Recognize roving tabindex (one `tabindex="0"`, the rest `tabindex="-1"`) as intentional and correct.
3. Confirm the non-tabbable buttons are reachable via the documented arrow-key model — not report them as unreachable.
4. Give a clean verdict (ACCEPT); at most an ENHANCEMENT note (e.g., `aria-pressed` could reflect real toggle state if these were toggle buttons).
