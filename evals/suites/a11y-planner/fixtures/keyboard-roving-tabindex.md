# Fixture: Roving Tabindex in Composite Widget

## Feature Description

You're planning accessibility for a toolbar component in a rich text editor. The toolbar contains 24 formatting buttons organized into 4 groups (Text Style, Alignment, Lists, Insert). The toolbar must behave as a single tab stop in the page's tab order — pressing Tab from the document body moves focus to the toolbar, then pressing Tab again moves focus past the toolbar to the next landmark. Within the toolbar, arrow keys navigate between buttons.

The ambiguity: the WAI-ARIA APG documents roving tabindex for both `role="toolbar"` and `role="menubar"`, but the patterns have different keyboard contracts. Toolbar uses Left/Right arrows with optional Home/End. Menubar uses Left/Right for top-level items plus Down to open submenus. The component has no submenus — it's a flat button collection — but the design team has labeled it "Format Menu" in the mockup.

Additional complexity: some buttons are toggle buttons (Bold, Italic, Underline) with pressed/unpressed state. Others are action buttons (Insert Image, Insert Link) that open dialogs. The plan must handle both within the same roving tabindex scheme.

## Context

- **Platform:** React web application (TypeScript)
- **Existing code:** Yes — current toolbar uses 24 individual `<button>` elements, each in the tab order (`tabindex="0"`). Users must press Tab 24 times to get past the toolbar. No grouping, no arrow key navigation, no roving tabindex.
- **Compliance target:** WCAG 2.2 AA
- **Assistive technologies:** NVDA (Windows), JAWS (Windows), VoiceOver (macOS), keyboard-only users
- **Scope:** Toolbar with roving tabindex — single tab stop, arrow key internal navigation, grouped buttons
- **Constraints:** Must support 24 buttons across 4 groups; some buttons are toggles (aria-pressed), others open dialogs; design mockup says "Format Menu" but there are no submenus; must integrate with existing rich text editor focus management (editor ↔ toolbar ↔ sidebar)

## Requirement

Create a comprehensive accessibility design plan that a developer with no accessibility knowledge can use to implement the component correctly on the first attempt.

The plan should cover:
- The toolbar vs. menubar decision — which role is correct when there are no submenus?
- Roving tabindex implementation: which button gets `tabindex="0"` and which get `tabindex="-1"`
- Arrow key navigation: Left/Right cycle through buttons, wrapping at edges
- Group navigation: whether arrow keys skip between groups or step through every button
- Toggle button state: `aria-pressed="true"/"false"` for Bold/Italic/Underline
- Action button behavior: buttons that open dialogs vs. buttons that toggle state
- Focus restoration: when a dialog opened from the toolbar closes, focus returns to the triggering button
- Home/End key support (optional per APG, but expected by power users)
- Focus indicator visibility across all 24 buttons
- Screen reader announcements: button label, group label, pressed state
- Testing strategy with specific keyboard test sequences
- Implementation tasks with a11y-critic checkpoints

## Scope Hints

This is an **AMBIGUOUS** difficulty fixture — the core ambiguity is toolbar vs. menubar role selection, and the secondary ambiguity is whether arrow keys should navigate every button or jump between groups. Expected plan length: 3-5 pages. Focus on:

1. The role decision: `role="toolbar"` is correct (no submenus). The plan should explain WHY menubar is wrong despite the "Format Menu" label in the mockup — label ≠ role.
2. Roving tabindex: `tabindex="0"` on the currently focused button, `tabindex="-1"` on all others. First button gets `tabindex="0"` by default. After arrow navigation, the focused button gets `tabindex="0"` and the previous one gets `tabindex="-1"`.
3. Group handling: APG Toolbar pattern says groups are optional. If groups are used, toolbar may support Left/Right within group and Tab/Shift+Tab between groups — but this is a design decision, not a spec requirement.
4. Toggle vs action: `aria-pressed` for toggles, no `aria-pressed` for action buttons. Both use `<button>` element.

## What Success Looks Like

An excellent plan would:
- ✓ Choose `role="toolbar"` and explain why `role="menubar"` is wrong for this flat layout
- ✓ Document roving tabindex: `tabindex="0"` on active button, `tabindex="-1"` on others
- ✓ Reference APG Toolbar pattern with URL
- ✓ Distinguish toggle buttons (`aria-pressed`) from action buttons (no `aria-pressed`)
- ✓ Document keyboard model: Tab enters/exits toolbar, Left/Right navigate, Home/End optional
- ✓ Address the group navigation ambiguity with a clear recommendation and rationale
- ✓ Plan focus restoration from dialogs opened by action buttons
- ✓ Include `aria-label` on the toolbar element ("Formatting toolbar" not "Format Menu")
- ✓ Plan group labeling with `role="group"` and `aria-label` for each group
- ✓ Cite WCAG 2.1.1 (Keyboard), 4.1.2 (Name, Role, Value), 2.4.7 (Focus Visible)
- ✓ Include test cases: Tab enters toolbar at first button, arrows navigate, Tab exits

## What Would Be Below Expectations

- ✗ Choosing `role="menubar"` because the mockup says "Format Menu" — roles are semantic, not visual labels
- ✗ No roving tabindex — keeping all 24 buttons at `tabindex="0"` (the existing bug)
- ✗ Using `aria-selected` instead of `aria-pressed` for toggle buttons — selected is for single-select patterns
- ✗ No group structure — 24 undifferentiated buttons in a toolbar is poor for screen reader orientation
- ✗ Not addressing the group navigation ambiguity — "use arrow keys" without specifying within-group vs across-groups
- ✗ No focus restoration plan for dialogs opened from toolbar buttons
- ✗ Vague keyboard description ("support keyboard navigation") without specifying Tab/Arrow/Home/End
