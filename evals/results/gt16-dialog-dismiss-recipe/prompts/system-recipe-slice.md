## Verification evidence contract

**Evidence type must match the failing condition.** A screenshot is never evidence for an interaction-class fix (keyboard operability, focus behavior, or a status-message announcement) — it shows what a sighted mouse user sees, not what a keyboard or screen-reader user experiences. When a fix's evidence doesn't match its defect class, the fix ships labeled **partial**, naming which defect classes still lack matching evidence.

| Defect class | Evidence REQUIRED before "verified" | Mode |
|---|---|---|
| Keyboard operability (reachable, operable with Tab/Enter/Space/Escape/arrows) | Real-keyboard Playwright transcript — actual `page.keyboard.press()` calls, never ARIA-attribute inspection alone | `npx playwright test` |
| Focus order & focus-visible sufficiency | Journey-level focus trace evidence | `keyboard-a11y-tester` |
| Accessible name/role/state; status-message announcements | Assertion output against actual computed screen-reader output | `virtual-screen-reader` |
| Machine-detectable semantics, contrast, alt-presence (a rule fires or stops firing) | Re-scan of the touched page(s) after the fix | `baseline-url-scan.mjs` (axe-core violations; `--census`/`--alt-snapshot` for the heuristic classes) |
| Visual-only classes (layout, spacing, color/swatch correctness) | Screenshot comparison | screenshots (`agent-browser screenshot` / Playwright screenshot) |

This table is what `a11y-critic` Phase 0 checks a remediation's attached evidence against, and what `bug-reporting`'s "Verification evidence" field cites.

### Detector-lane authority boundary

A detector PASS means only "no detection fired for this route, state, viewport, config, and version" — never a WCAG, Section 508, keyboard, or assistive-technology verdict. Cross-tool agreement on the same target raises triage priority; it never confirms a defect by itself, and an absence of detection is not evidence of conformance.

**An infrastructure limit must never emit a canonical result.** A step-cap watchdog, a timeout, or a crashed collector is an *abort*, not a PASS/FAIL/BLOCKED outcome — record it as what it is (aborted, incomplete, environment-limited) and keep it out of the pass/fail denominator until it is resolved.

**Mandatory cross-check rule:** whenever a run's non-conclusive rate (`BLOCKED`, `cantTell`, or equivalent) approaches saturation for a batch — most of the sampled set landing in a single non-conclusive bucket rather than spread across pass/fail — treat that as a signal about the collector, not about the product, and cross-check the batch against an independent evidence lane (a different tool, a driven session, or manual sampling) before the numbers reach a client-facing report. A near-saturated non-conclusive rate that ships unchecked reads as "almost entirely untestable," which may simply be an ordinary pass/fail distribution obscured by a collector fault.

Related discipline, restated for this boundary: never promote scanner output straight to a WCAG or Section 508 verdict; never treat count-parity between two runs as completeness; never collapse `cantTell` / informational / skipped / blocked / untested into pass or fail — each stays a distinguishable, visible state (see the coverage-ledger vocabulary in `acr-reporting`'s untested gate for the report-side version of the same rule).

### Evidence retention (append-only)

Never overwrite an evidence run. Failed, intermediate, and superseded captures are retained beside the final result under names that state *why* they are not final (for example `-raw-live-capture`, `-script-error`, `-modifier-mismatch`, `-pre-final-adjudication`). The same discipline extends to generated deliverables: every non-final revision is kept beside the final one with an append-only supersession log, and each non-final revision is explicitly marked not client-facing and not a conformance, certification, publication, or acceptance artifact.

Retention is not bookkeeping for its own sake — it is what makes silent errors findable. A numeric error in an otherwise structurally valid generated deliverable — a formula range that under-counts, a mapping that drops rows — passes schema validation and surfaces only when a later revision can be diffed against the one that was wrong. Overwrite the run and that diff is gone.

`references/hash-evidence.mjs` makes the rule checkable: it writes an append-only `checksums.json` manifest beside an evidence tree and `--verify` lists every modified, missing, or unlisted file, exiting non-zero on drift (modified or missing; unlisted too under `--strict`) — it makes silent edits findable, not impossible.

## 1. Keyboard Accessibility Tests

**MANDATORY: All keyboard tests MUST use real Playwright keyboard interactions against a live or local site. Never check ARIA attributes alone and claim a keyboard test passed — you must actually press keys and verify the result.**

### Required Testing Method
- Use `page.keyboard.press('Enter')`, `page.keyboard.press('Tab')`, `page.keyboard.press('Escape')`, `page.keyboard.press('Space')` for single keys
- Use `page.keyboard.press('Shift+ArrowRight')`, `page.keyboard.press('Control+Enter')`, `page.keyboard.press('Meta+Enter')` for key combos
- Use `page.keyboard.down('Shift')` / `page.keyboard.up('Shift')` with `page.keyboard.press('ArrowRight')` for held-key sequences (e.g., text selection)
- Use `element.focus()` then verify with `toBeFocused()` or `document.activeElement === element`
- **NEVER** use synthetic `dispatchEvent(new KeyboardEvent(...))` to test keyboard features — that bypasses the real browser keyboard path and proves nothing
- **NEVER** claim a keyboard test passed by only reading DOM attributes (aria-expanded, aria-pressed, etc.) without actually pressing a key and observing the state change

### What to Test (with real key presses)
1. **Tab order**: Press Tab repeatedly and verify focus moves to each interactive element in logical order
2. **Enter/Space activation**: Focus a button/link, press Enter or Space, verify the expected action occurred (panel opened, state toggled, navigation happened)
3. **Escape to dismiss**: Open a modal/popup/sidebar, press Escape, verify it closed
4. **Arrow key navigation**: For tablists, menus, and custom widgets — press Arrow keys and verify focus/selection moves
5. **Keyboard text selection**: For content areas — use Shift+Arrow to select text, verify selection was created via `window.getSelection()`
6. **Modifier combos**: Test Ctrl+Enter, Meta+Enter, and other app-specific shortcuts
7. **Focus management**: After opening/closing panels, verify focus moves to the correct element (e.g., CKEditor gets focus when annotation form opens, focus returns to trigger after modal closes)

### State Verification Pattern
Every keyboard test must follow this pattern:
```
1. Record initial state (aria-expanded, aria-pressed, visibility, activeElement)
2. Perform real keyboard action (page.keyboard.press)
3. Wait for UI to update (waitForTimeout or waitForFunction)
4. Verify state actually changed (attribute toggled, element visible/hidden, focus moved)
```

Example — testing a toggle button:
```js
const btn = page.locator('button[aria-expanded]');
const initialExpanded = await btn.getAttribute('aria-expanded');
await btn.focus();
await page.keyboard.press('Enter');
await page.waitForTimeout(300);
const afterExpanded = await btn.getAttribute('aria-expanded');
expect(initialExpanded).not.toBe(afterExpanded); // State MUST change
```

### Live Site Requirement
Keyboard tests MUST run against a real site (local dev environment like Lando/DDEV, or staging). Guard against accidental use of mocks:
```js
if (!BASE_URL || !BASE_URL.match(/https?:\/\/.+/)) {
  throw new Error('Keyboard tests require a real site. Set BASE_URL.');
}
```

### SPA-Specific Testing Patterns

React and other SPA frameworks introduce gotchas that break naive Playwright tests:

- **No direct URL navigation**: SPA routes (e.g., `/book/truth-lending/2460032`) return 404 from the server — the server has no route for them. Navigate WITHIN the app by clicking menu items and waiting for React to render. Use `waitForSelector()` to confirm content has loaded before interacting.

- **Duplicate DOM (mobile + desktop)**: Many React apps render the same component twice — once for desktop, once for mobile. Playwright strict mode throws when a selector matches both. Fix by scoping to a container (`nav.left-sidebar [role="tree"]`) or appending `.first()` / `.last()` to your locator.

- **React state waits**: After `page.keyboard.press()`, React state updates are async — the DOM may not reflect the new state for tens of milliseconds. Add `waitForTimeout(200–500)` or `waitForFunction(() => ...)` before asserting on ARIA attributes that change via React state.

- **React 16 `setTimeout(0)` for focus-after-unmount**: In React 16, focus calls issued inside async callbacks do not survive component unmount. Production code must wrap the focus call in `setTimeout(() => el.focus(), 0)`. Tests must account for this by allowing 100–200ms after a panel closes before checking `document.activeElement`.

- **DOMPurify stripping `data-*` attributes**: A bare `DOMPurify.sanitize()` call strips `data-*` attributes by default. If tests find click handlers broken after sanitization, the fix is to route sanitization through a wrapper component that calls sanitize at render time (not as a pre-processing step that discards needed attributes).

- **Playwright MCP cannot deliver keyboard events**: The Playwright MCP browser integration CANNOT forward keyboard events — `browser_press_key` calls are silently dropped for most interactive widgets. Always run keyboard a11y tests with `npx playwright test` using `.spec.js` files. Use the MCP browser only for visual inspection and DOM queries.

### CSS Anti-patterns That Break Keyboard Access

**`visibility:hidden` + `:focus-within` catch-22 (CRITICAL)**

Never use `visibility: hidden` on elements that are supposed to become visible when a parent receives keyboard focus via `:focus-within`. The pattern creates an impossible state for keyboard users:

- `visibility: hidden` removes the element from the tab order entirely
- Because the element can't receive focus, `:focus-within` is never triggered on the parent
- Result: keyboard users can never reach the element at all

```css
/* ❌ BROKEN — keyboard users can never trigger :focus-within on the parent */
.annotation-block-edit {
  opacity: 0;
  visibility: hidden; /* removes from tab order → :focus-within never fires */
}
.annotation-block:focus-within .annotation-block-edit {
  opacity: 1;
  visibility: visible;
}

/* ✅ CORRECT — opacity keeps element in tab order; :focus-within works */
.annotation-block-edit {
  opacity: 0; /* visually hidden but still focusable */
}
.annotation-block:hover .annotation-block-edit,
.annotation-block:focus-within .annotation-block-edit {
  opacity: 1;
}
```

This applies to any "reveal on hover/focus" pattern: edit buttons, delete buttons, action menus inside cards. Use `opacity` only (not `visibility`) when the element must remain keyboard-reachable.

### ARIA Attribute Checks (supplement, not substitute)
After verifying keyboard operability, also check:
- Buttons have `aria-label` or visible text
- Toggle buttons have `aria-pressed` or `aria-expanded`
- Tab widgets have `role="tablist"`, `role="tab"`, `aria-selected`
- SVGs inside buttons have `aria-hidden="true"`
- Close buttons have descriptive `aria-label`
- Only one tab has `aria-selected="true"` per tablist