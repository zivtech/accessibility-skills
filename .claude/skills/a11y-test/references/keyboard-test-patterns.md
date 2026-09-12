# Keyboard Accessibility Test Patterns

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

### WAI-ARIA APG Keyboard Test Templates

Reusable Playwright templates for common widget patterns. Each uses real `page.keyboard.press()` calls — never synthetic events.

**1. Tree View**
Interactions: ArrowDown/Up move `aria-activedescendant`; ArrowRight expands closed node or moves to first child; ArrowLeft collapses open node or moves to parent; Home/End jump to first/last visible treeitem; Enter activates.
```js
const tree = page.locator('[role="tree"]');
await tree.focus();
const before = await tree.getAttribute('aria-activedescendant');
await page.keyboard.press('ArrowDown');
await page.waitForTimeout(200);
const after = await tree.getAttribute('aria-activedescendant');
expect(after).not.toBe(before);
expect(after).toBeTruthy(); // must reference a [role="treeitem"] id
```

**2. Roving Tabindex (Tabs)**
Interactions: ArrowRight/Left move focus between `[role="tab"]` elements and update tabindex; active tab keeps `tabindex="0"`, others get `tabindex="-1"`; only one `aria-selected="true"` per `[role="tablist"]`.
```js
const activeTab = page.locator('[role="tab"][tabindex="0"]');
await activeTab.focus();
await page.keyboard.press('ArrowRight');
await page.waitForTimeout(200);
const newActive = page.locator('[role="tab"][tabindex="0"]');
await expect(newActive).toHaveAttribute('aria-selected', 'true');
expect(await page.locator('[role="tab"][aria-selected="true"]').count()).toBe(1);
```

**3. Dialog Focus Trap**
Interactions: Tab/Shift+Tab cycle within `[role="dialog"]` (last focusable→first, first→last); Escape closes; focus returns to trigger after close.
```js
await triggerButton.click();
const dialog = page.locator('[role="dialog"]');
// Tab past last focusable item — should wrap to first
const focusables = dialog.locator('button, [href], input, [tabindex="0"]');
const count = await focusables.count();
for (let i = 0; i < count; i++) await page.keyboard.press('Tab');
await expect(focusables.first()).toBeFocused();
await page.keyboard.press('Escape');
await expect(triggerButton).toBeFocused();
```

**4. Sidebar/Panel Focus Management**
Interactions: Close button receives focus on panel open; Escape closes panel and returns focus to trigger.
```js
await triggerButton.click();
const panel = page.locator('[role="region"]'); // or your panel selector
await expect(panel.locator('button[aria-label*="Close"]')).toBeFocused();
await page.keyboard.press('Escape');
await page.waitForTimeout(150); // allow React unmount + setTimeout(0)
await expect(triggerButton).toBeFocused();
```

**5. Disclosure Widget**
Interactions: Enter/Space toggle `aria-expanded` between "true"/"false"; `aria-controls` references the panel id; panel visibility matches expanded state.
```js
const btn = page.locator('button[aria-expanded]');
await btn.focus();
const initial = await btn.getAttribute('aria-expanded');
await page.keyboard.press('Enter');
await page.waitForTimeout(200);
const toggled = await btn.getAttribute('aria-expanded');
expect(toggled).not.toBe(initial);
const panelId = await btn.getAttribute('aria-controls');
const panel = page.locator(`#${panelId}`);
await expect(panel).toBeVisible(); // when expanded=true
```

**6. Menu Button / Dropdown**
Interactions: Enter/Space opens menu, focus moves to first item; Arrow keys navigate with wrapping; Escape closes and returns focus to trigger; Home/End jump to first/last; type-ahead jumps to matching item.
```js
const trigger = page.locator('button[aria-haspopup="menu"]');
await trigger.focus();
await page.keyboard.press('Enter');
await page.waitForTimeout(200);
const menu = page.locator('[role="menu"]');
await expect(menu).toBeVisible();
await expect(menu.locator('[role="menuitem"]').first()).toBeFocused();
await page.keyboard.press('End');
await expect(menu.locator('[role="menuitem"]').last()).toBeFocused();
await page.keyboard.press('Escape');
await expect(trigger).toBeFocused();
```

**7. Combobox / Autocomplete**
Interactions: typing shows listbox with filtered options; ArrowDown focuses first option; Enter selects and closes; Escape closes without selection; `aria-expanded` and `aria-activedescendant` update.
```js
const input = page.locator('[role="combobox"]');
await input.focus();
await input.type('ap');
await page.waitForTimeout(300);
await expect(input).toHaveAttribute('aria-expanded', 'true');
const listbox = page.locator('[role="listbox"]');
await page.keyboard.press('ArrowDown');
expect(await input.getAttribute('aria-activedescendant')).toBeTruthy();
await page.keyboard.press('Enter');
await expect(listbox).toBeHidden();
```

**8. Listbox (single and multi-select)**
Interactions: Arrow keys move selection in single-select; Space toggles in multi-select; Shift+Arrow extends range; Home/End jump to first/last; type-ahead navigation.
```js
const listbox = page.locator('[role="listbox"]');
await listbox.focus();
await expect(listbox.locator('[role="option"]').first()).toHaveAttribute('aria-selected', 'true');
await page.keyboard.press('ArrowDown');
await page.waitForTimeout(150);
await expect(listbox.locator('[role="option"]').nth(1)).toHaveAttribute('aria-selected', 'true');
await page.keyboard.press('End');
await expect(listbox.locator('[role="option"]').last()).toBeFocused();
```

**9. Slider**
Interactions: ArrowLeft/Right adjust by step; PageUp/Down by larger increment; Home/End set to min/max; `aria-valuenow`, `aria-valuemin`, `aria-valuemax` update.
```js
const slider = page.locator('[role="slider"]');
await slider.focus();
const before = Number(await slider.getAttribute('aria-valuenow'));
await page.keyboard.press('ArrowRight');
await page.waitForTimeout(150);
expect(Number(await slider.getAttribute('aria-valuenow'))).toBeGreaterThan(before);
await page.keyboard.press('Home');
expect(await slider.getAttribute('aria-valuenow')).toBe(await slider.getAttribute('aria-valuemin'));
await page.keyboard.press('End');
expect(await slider.getAttribute('aria-valuenow')).toBe(await slider.getAttribute('aria-valuemax'));
```

**10. Date Picker**
Interactions: Arrow keys navigate days; PageUp/Down navigate months; Shift+PageUp/Down navigate years; Enter selects and closes; Escape closes without selection and returns focus to input.
```js
const input = page.locator('[aria-label*="date" i]');
await input.focus();
await page.keyboard.press('Enter');
const grid = page.locator('[role="grid"]');
await expect(grid).toBeVisible();
await page.keyboard.press('ArrowRight');
await page.keyboard.press('PageDown');
await page.keyboard.press('Enter');
await expect(grid).toBeHidden();
expect(await input.inputValue()).not.toBe('');
```

**11. Accordion**
Interactions: Enter/Space on header toggles panel; `aria-expanded` reflects state; Arrow keys move between headers; Home/End jump to first/last header.
```js
const headers = page.locator('[role="button"][aria-expanded]');
await headers.first().focus();
const initial = await headers.first().getAttribute('aria-expanded');
await page.keyboard.press('Enter');
await page.waitForTimeout(200);
expect(await headers.first().getAttribute('aria-expanded')).not.toBe(initial);
await page.keyboard.press('ArrowDown');
await expect(headers.nth(1)).toBeFocused();
await page.keyboard.press('End');
await expect(headers.last()).toBeFocused();
```

**12. Radio Group**
Interactions: Arrow keys move selection within group (roving tabindex); Tab moves to/from group as a whole; first or checked radio receives initial focus; `aria-checked` updates with selection.
```js
const radios = page.locator('[role="radiogroup"] [role="radio"]');
await radios.first().focus();
await page.keyboard.press('ArrowDown');
await page.waitForTimeout(150);
await expect(radios.nth(1)).toHaveAttribute('aria-checked', 'true');
await expect(radios.first()).toHaveAttribute('aria-checked', 'false');
await page.keyboard.press('Tab');
await expect(radios.nth(1)).not.toBeFocused();
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

