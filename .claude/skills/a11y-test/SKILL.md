---
name: a11y-test
description: "Use when you need to run real accessibility tests — Playwright keyboard interactions, axe-core scanning, visual regression, and WCAG 2.2 compliance checks. The measurement layer that feeds evidence into a11y-critic reviews."
license: Apache-2.0
compatibility: Designed for Claude Code
metadata:
  author: zivtech
  version: "1.1.0"
---

# Accessibility Testing Skill

Use Playwright MCP (not Bash) to test accessibility comprehensively:

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

### WAI-ARIA APG Keyboard Test Templates

Reusable Playwright templates for the five most common widget patterns. Each uses real `page.keyboard.press()` calls — never synthetic events.

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

## 2. Visual Regression Tests (REQUIRED)
Visual regression tests ensure accessibility fixes don't introduce unintended visual changes. Supports **Playwright** and optionally **BackstopJS** for side-by-side HTML reports.

### Baseline Strategy
- **Preferred**: Use `npx playwright test --update-snapshots` on the current branch to establish baselines, then run tests after further changes to detect regressions.
- **CRITICAL — build must be complete first**: Only run `--update-snapshots` after any build (React, webpack, etc.) has fully finished. Running it during a concurrent build captures mixed pre/post-build screenshots — some pages reflect old code, some new. The resulting baseline is internally inconsistent and will fail on the next clean run. Wait for the build to complete, then run `--update-snapshots`, then run the tests.
- **Cross-branch comparison**: Only when explicitly requested. Requires branch switching, cache clearing, and potential config sync — avoid unless necessary.
- **Never** assume branch-switching is safe without checking with the user first.

### Playwright Screenshot Configuration
Use `toHaveScreenshot()` with the correct options:

- **`maxDiffPixelRatio`** (0 to 1): Maximum ratio of *different pixels* to total pixels. Use `0.01` (1%) for element screenshots, `0.03` (3%) for full-page screenshots. This is the primary control for flakiness.
- **`threshold`** (0 to 1): Per-pixel *color distance* tolerance (0 = exact, 1 = any color). Default `0.2` is fine for most cases. This is NOT the overall diff threshold.
- **`maxDiffPixels`**: Absolute count of allowed different pixels. Alternative to `maxDiffPixelRatio`.

```js
// Element screenshot — tight tolerance
await expect(element).toHaveScreenshot('name.png', {
  maxDiffPixelRatio: 0.01,
});

// Full-page screenshot — looser for dynamic content
await expect(page).toHaveScreenshot('name.png', {
  fullPage: true,
  maxDiffPixelRatio: 0.03,
  mask: [page.locator('.dynamic-region')],
});
```

### BackstopJS (Optional)
BackstopJS provides an HTML report with side-by-side visual diffs — useful for manual review. It can run alongside Playwright tests.

**Setup:**
```bash
npm install --save-dev backstopjs
```

**Configuration** (`backstop.json`):
- Use `scenarioDefaults` for shared settings (delay, misMatchThreshold, removeSelectors)
- Use `"selectors": ["document"]` for full-page, or class/tag selectors for elements
- Avoid attribute selectors with quoted values (e.g. `[type='text']`) — they cause parse errors in Puppeteer engine
- Use `requireSameDimensions: false` for pages with dynamic heights
- Full-page scenarios need higher `misMatchThreshold` (15-20%) due to dynamic content
- Element scenarios can use tighter thresholds (5-10%)

**Popup/overlay handling:**
Create an `onReady.cjs` engine script (use `.cjs` extension if project has `"type": "module"` in package.json):
```js
const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));
module.exports = async (page, scenario, vp) => {
  await wait(2000);
  await page.evaluate(() => {
    document.querySelectorAll('dialog, [role="dialog"], .modal, .popup').forEach(el => el.remove());
  });
  await wait(300);
};
```

**Workflow:**
```bash
npx backstop reference --config=path/to/backstop.json  # Capture baseline
npx backstop test --config=path/to/backstop.json       # Compare against baseline
npx backstop approve --config=path/to/backstop.json    # Promote test -> reference
npx backstop openReport --config=path/to/backstop.json # View HTML report
```

### Handling Dynamic Content
CMS pages often contain dynamic elements (timestamps, session blocks, popups). These cause false failures.

- **Prefer element-level screenshots** over full-page — more stable and more useful for a11y regression detection.
- **Mask dynamic regions**: Playwright uses `mask: [page.locator()]`, BackstopJS uses `removeSelectors` or `hideSelectors`.
- **Common elements to mask/remove**: `.contextual`, `.toolbar-tray`, `.messages`, `[data-drupal-messages]`, `dialog`, `[role="dialog"]`, time/date elements.
- **Dismiss popups before capture**: Use Playwright's `dismissPopups()` helper or BackstopJS `onReadyScript`.
- **Use `waitForLoadState('networkidle')`** and a short wait to let JS behaviors settle before capture.

### Elements to Test
- Focus indicators (links, buttons, inputs in :focus state)
- Breadcrumbs (structure and current page indicator)
- Navigation menus (default, hover, active states)
- Form inputs (borders, focus states)
- Link underlines in content areas
- External link icons
- Skip links (when visible)
- Progress bars and loading indicators

### Viewport Sizes
- Desktop: 1280x800
- Tablet: 768x1024
- Mobile: 320x568

### Reporting
- Playwright: `npx playwright show-report` for HTML report with side-by-side diffs
- BackstopJS: `npx backstop openReport` for visual comparison dashboard

## 3. WCAG Compliance Checks
- 1.1.1 Non-text Content (alt text, aria-labels)
- 1.4.1 Use of Color (link underlines)
- 1.4.3 Contrast Minimum (4.5:1 normal text, 3:1 large text — note: text inside UI components like buttons uses TEXT thresholds, not the 3:1 UI component boundary threshold)
- 1.4.10 Reflow (320px viewport)
- 1.4.11 Non-text Contrast (form borders, focus indicators)
- 2.4.4 Link Purpose (contextual aria-labels)
- 2.4.6 Headings and Labels (no empty headings)
- 2.4.7 Focus Visible (outline visibility)
- 2.4.8 Location (breadcrumbs with aria-current)
- 2.4.11 Focus Not Obscured (focused element not hidden by sticky headers/footers/banners) [WCAG 2.2]
- 2.4.13 Focus Appearance (focus indicator ≥2px perimeter, 3:1 contrast change) [WCAG 2.2]
- 2.5.7 Dragging Movements (drag ops have single-pointer alternative) [WCAG 2.2]
- 2.5.8 Target Size (interactive targets ≥24x24 CSS pixels) [WCAG 2.2]
- 3.3.7 Redundant Entry (don't re-ask for info already provided) [WCAG 2.2]
- 3.3.8 Accessible Authentication (no cognitive function tests for login, paste/autofill supported) [WCAG 2.2]

## 4. Automated Scanning (axe-core via Playwright)

Inject axe-core into live pages via Playwright for automated WCAG violation detection. This catches issues that manual review misses (computed contrast through CSS layers, missing ARIA on dynamically rendered content, landmark coverage).

### axe-core Injection Pattern
```js
// In a Playwright test file (.spec.js)
const { test, expect } = require('@playwright/test');
const fs = require('fs');

test('axe-core accessibility scan', async ({ page }) => {
  await page.goto(BASE_URL);
  await page.waitForLoadState('networkidle');

  // Inject axe-core
  const axeSource = fs.readFileSync(
    require.resolve('axe-core/axe.min.js'), 'utf-8'
  );
  await page.evaluate(axeSource);

  // Run audit
  const results = await page.evaluate(() =>
    axe.run(document, {
      runOnly: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice']
    })
  );

  // Report violations
  const violations = results.violations;
  if (violations.length > 0) {
    const report = violations.map(v => ({
      id: v.id,
      impact: v.impact,
      description: v.description,
      helpUrl: v.helpUrl,
      nodes: v.nodes.length
    }));
    console.log('axe violations:', JSON.stringify(report, null, 2));
  }
  expect(violations.length).toBe(0);
});
```

### Multi-Page Scanning
For sites with multiple routes, scan each page variant:
- Default state (no interactions)
- Loading state (if applicable — trigger a load and scan before it completes)
- Error state (submit an invalid form, then scan)
- Expanded state (open all disclosures/tabs, then scan)

### Dynamic Test Prioritization
After the axe-core scan, use findings to prioritize manual testing effort:
- **axe found ARIA violations** → prioritize screen reader testing (Section 1 keyboard + ARIA checks)
- **axe found color-contrast violations** → prioritize visual inspection (Section 2 focus indicators, link underlines)
- **axe found heading/structure violations** → prioritize keyboard navigation order testing
- **axe found no form violations** → deprioritize form testing with a note that automated checks passed
- **Always test regardless**: focus indicators at zoom, reduced-motion, skip links

### Scale and Sampling (>15 pages)
For large sites, classify pages into template groups and scan one representative per group:
1. Run `discover` phase: list all routes, group by template (list page, detail page, form page, etc.)
2. Select 1-2 pages per template group
3. Scan representatives, report which templates were covered
4. Document sampling strategy in the test report

### Output Format
Report axe-core results alongside keyboard and visual regression results:
```
## axe-core Scan Results
Pages scanned: [count]
Total violations: [count]
Critical: [n] | Serious: [n] | Moderate: [n] | Minor: [n]

### Violations by Rule
| Rule ID | Impact | Description | Pages | Elements |
|---------|--------|-------------|-------|----------|
| color-contrast | serious | Elements must meet color contrast | 3 | 12 |
```

This output feeds directly into the a11y-critic's Phase 0 (Consume Test Evidence) — measured violations become hard evidence in the design review.

## 5. Static Analysis (eslint-plugin-jsx-a11y) — React/Vue/JSX projects only

Static analysis catches accessibility issues at build time, complementing axe-core's runtime scanning. Different tools catch different issue classes.

### When to Use
- Project uses React, Next.js, Vue, or other JSX/TSX framework
- Want CI-gate a11y checks that don't require a running server
- Catches: missing alt text in JSX, invalid ARIA attributes in markup, inaccessible element nesting

### Setup
```bash
# Install as dev dependency
pnpm add -D eslint-plugin-jsx-a11y  # or npm/yarn

# Create temporary standalone config (avoids ESLint 9 flat config issues)
cat > eslint.a11y.mjs << 'EOF'
import jsxA11y from "eslint-plugin-jsx-a11y";
import tseslint from "typescript-eslint";
export default [{
  files: ["src/**/*.tsx", "src/**/*.jsx"],
  plugins: { "jsx-a11y": jsxA11y },
  languageOptions: {
    parser: tseslint.parser,
    parserOptions: { ecmaFeatures: { jsx: true } },
  },
  rules: { ...jsxA11y.flatConfigs.recommended.rules },
}];
EOF

# Run
npx eslint --config eslint.a11y.mjs src/

# Clean up temp config (keep the plugin installed)
rm eslint.a11y.mjs
```

### Known False Positives
- Custom component `role` props (not HTML role attributes)
- Components that pass ARIA attributes through to child elements via spread
- Dynamic content loaded after initial render
- Next.js `<Link>` components that render valid anchors at runtime

## Test Execution Order
1. Run static analysis first (fast, no server needed) — Section 5
2. Run keyboard accessibility tests — Section 1
3. Run visual regression tests — Section 2
4. Run axe-core automated scans — Section 4
5. Run WCAG compliance checks — Section 3
6. Report consolidated results with pass/fail counts per section

**Lifecycle integration:** These test results feed into a11y-critic reviews. The full a11y lifecycle is:
plan → critique plan → revise → implement → **test (this skill)** → critique implementation → fix → re-test
