# Modal Dialog Accessibility Design Plan

> **For Claude:** Use a11y-planner protocol. Review with a11y-critic after implementation.
> **Compliance target:** WCAG 2.2 AA
> **Users who need accessibility:** Screen reader users, keyboard-only users, low vision users
> **Assistive technologies:** NVDA, JAWS, VoiceOver, keyboard-only

**Feature:** React modal dialog with form content and broken focus trap
**Risk Level:** High
**Component/Page Type:** Modal Dialog with Form

---

## Scope & Context

The component is a React modal dialog containing a subscription form. Current issues include missing focus trap, no role="dialog" or aria-modal, missing close button label, and no Escape key functionality. The goal is to implement full accessibility according to APG Modal Dialog pattern with WCAG 2.2 AA compliance.

## Semantic Structure Plan

### Structure Diagram

```html
<main>
  <button aria-haspopup="dialog" ref={triggerRef}>Subscribe Now</button>
  <nav class="background-nav">...</nav>
  {isOpen && (
    <div role="dialog" aria-modal="true" aria-labelledby="modal-title" tabIndex="-1">
      <h2 id="modal-title">Subscribe to Updates</h2>
      <button aria-label="Close dialog">×</button>
      <form>...</form>
    </div>
  )}
</main>
```

## Interaction Pattern Design

| Widget | APG Pattern | Keyboard Model | ARIA Attributes | WCAG Citation |
|--------|-------------|----------------|------------------|---------------|
| Modal Dialog | [APG Modal Dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialogmodal/) | Tab/Shift+Tab: cycle within dialog, Escape: close | role="dialog", aria-modal="true", aria-labelledby, aria-describedby | 2.1.1, 2.1.2, 4.1.2 |
| Close Button | APG Button | Enter/Space: close | aria-label="Close dialog" | 2.1.1, 4.1.2 |
| Form Inputs | Native HTML | Tab: navigate | aria-required="true" | 1.3.1, 4.1.2 |

## Focus Management Plan

1. **Focus on Open**: Move focus to modal's first focusable element (close button)
2. **Focus Trap**: Tab/Shift+Tab cycles within modal only
3. **Focus Restoration**: On close, return focus to trigger button
4. **Escape Key**: Closes modal and restores focus

## State Communication Design

| State | Visual Indicator | Programmatic Indicator | ARIA Attribute | WCAG Citation |
|-------|------------------|------------------------|----------------|---------------|
| Modal Open | Backdrop overlay | role="dialog", aria-modal="true" | role="dialog" | 4.1.2 |
| Modal Closed | None | None | None | N/A |
| Form Submission | Success message | aria-live="polite" | role="status" | 4.1.3 |

## Visual Accessibility Plan

- Focus indicators: 3px solid #1565c0 (3:1 contrast)
- Close button: 44x44px touch target
- Text: 16px base font (4.5:1 contrast)
- Color is not sole indicator (text + icon for close button)

## Content Accessibility Plan

- Modal title: aria-labelledby="modal-title"
- Close button: aria-label="Close dialog"
- Form labels: htmlFor/id association
- Success message: aria-live="polite" for screen readers

## Testing Strategy

- **Automated**: axe-core for role/aria validation
- **Keyboard**: Tab/Shift+Tab/Escape testing
- **Screen Reader**: Verify dialog announcement and focus trapping
- **Visual**: 200% zoom test for layout reflow
- **Acceptance**: Focus must stay within modal, Escape must close, focus must restore

### Test Cases

- [Focus trap: Tab cycles within modal only]
- [Escape closes modal and restores focus]
- [Close button labeled "Close dialog"]
- [Modal announced as "Subscribe to Updates, dialog"]
- [Form inputs have associated labels]
- [Success message announced via live region]

## Implementation Tasks

### Task 1: Modal Dialog Accessibility

🔍 **Review checkpoint after this task**

**Files:**
- `component.jsx` (SubscribeModal and SubscribePage)

**Structure Stub:**
```jsx
<div 
  role="dialog" 
  aria-modal="true" 
  aria-labelledby="modal-title" 
  tabIndex="-1"
>
  <h2 id="modal-title">Subscribe to Updates</h2>
  <button aria-label="Close dialog" onClick={handleClose}>×</button>
  <form>...</form>
</div>
```

**ARIA Attributes:**
- `role="dialog"` (WCAG 4.1.2)
- `aria-modal="true"` (WCAG 4.1.2)
- `aria-labelledby="modal-title"` (WCAG 4.1.2)
- `aria-label="Close dialog"` on close button (WCAG 4.1.2)

**Keyboard Interactions:**
- `Tab`: Cycle within dialog
- `Shift+Tab`: Reverse cycle within dialog
- `Escape`: Close dialog and restore focus

**Tests:**
- Focus trap test
- Escape key test
- Screen reader announcement test

**WCAG Criteria:**
- WCAG 2.1.1 Keyboard
- WCAG 2.1.2 No Keyboard Trap
- WCAG 2.4.3 Focus Order
- WCAG 4.1.2 Name, Role, Value

## a11y-Critic Review Checkpoints

| Checkpoint | After Task | Focus Areas |
|------------|------------|-------------|
| 🔍 1 | Task 1 | Verify focus trap implementation, aria-modal="true", Escape key functionality, and focus restoration |

---

### Architecture Overview
Modal dialog follows APG pattern with focus trap, role="dialog", and proper keyboard interactions. Form inputs maintain existing accessibility features.

### Implementation Tasks
#### Task 1: Modal Dialog Accessibility
Estimated Effort: Medium
Depends on: none
#### Test Strategy for Task 1
- Focus trap test
- Escape key test
- Screen reader announcement test
#### Acceptance Criteria for Task 1
- Modal has role="dialog" and aria-modal="true"
- Focus is trapped within modal
- Escape key closes modal and restores focus
- Close button has aria-label="Close dialog"

### Failure Modes
- Missing focus trap leading to keyboard trap
- Missing role="dialog" causing screen reader confusion
- Missing focus restoration on close

## References

- [WAI-ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [WCAG 2.2 Specification](https://www.w3.org/WAI/WCAG22/quickref/)
- [a11y-critic skill](https://github.com/zivtech/a11y-meta-skills)
- [accessibility-testing skill](https://github.com/zivtech/zivtech-claude-skills)