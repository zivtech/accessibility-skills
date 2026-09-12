# 2. Visual Regression Tests (REQUIRED)
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

### Contrast Verification
- Use browser DevTools (Chrome: CSS Overview, Firefox: Accessibility Inspector) to audit all text contrast
- Run axe-core with `color-contrast` rule enabled (catches most but not all cases)
- Manually check: text over images/gradients (axe-core misses these)
- Manually check: focus indicator contrast against both focused and unfocused backgrounds
- Check non-text contrast: UI component borders, icons, form control outlines (WCAG 1.4.11)
- Test with forced-colors mode: verify all interactive elements remain distinguishable

### Zoom and Reflow Verification
- Set viewport to 1280px, zoom to 400% (equivalent to 320px)
- Verify: no horizontal scrollbar, content reflows to single column
- Verify: no text truncation, overlap, or content hidden behind other elements
- Test text spacing override: 1.5x line height, 2x paragraph spacing, 0.12em letter spacing
- Verify: all interactive elements remain visible and operable at 200% zoom

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

