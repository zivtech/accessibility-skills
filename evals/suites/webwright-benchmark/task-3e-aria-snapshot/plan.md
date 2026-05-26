# Task 3e: ARIA Snapshot — WAI-ARIA APG Tabs (Automatic Activation)

## URL
https://www.w3.org/WAI/ARIA/apg/patterns/tabs/examples/tabs-automatic/

## Critical Points

1. **Target elements**: tablist (1), tab (multiple), tabpanel (multiple)
2. **States to capture**:
   - tab: aria-selected (true/false)
   - tab: aria-controls (panel ID)
   - tabpanel: aria-labelledby (tab ID)
3. **Method**: `page.locator("body").aria_snapshot()` — YAML-like ARIA tree output
4. **Relationships**: Map tab → panel via aria-controls / aria-labelledby cross-reference
5. **Output**: Write full snapshot + parsed analysis to final_script_log.txt
6. **Screenshot**: Save to screenshots/ directory

## Execution Plan

1. Launch Firefox headless, viewport 1280x1800
2. Navigate to URL, wait for networkidle
3. Capture aria_snapshot() of body
4. Parse snapshot for tablist, tab (with aria-selected), tabpanel (with aria-labelledby)
5. Build tab→panel relationship map
6. Write log file with raw snapshot + parsed analysis
7. Take screenshot
8. Print summary to stdout

## Time Estimate
- Setup + navigation: ~5s
- Snapshot + parsing: ~2s
- File writes: ~1s
- Total: ~10s
