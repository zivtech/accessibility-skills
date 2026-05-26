# Task 3b: Tabs Automatic Activation — Execution Plan

## Target
https://www.w3.org/WAI/ARIA/apg/patterns/tabs/examples/tabs-automatic/

## Critical Points

### What to verify per tab click
1. Exactly one tab has aria-selected="true" (the clicked tab)
2. All other tabs have aria-selected="false"
3. The tabpanel associated with the selected tab is visible (is_visible() == True)
4. All other tabpanels are hidden (is_visible() == False)

### Keyboard test
1. Focus the first tab (click or focus())
2. Press ArrowRight using page.keyboard.press("ArrowRight") — real Playwright API, NOT dispatchEvent
3. Verify: second tab now has aria-selected="true"
4. Verify: first tab now has aria-selected="false"

### ARIA pattern for automatic tabs
- Tabs use role="tab" within a role="tablist"
- Active tab has aria-selected="true"
- Each tab has aria-controls pointing to its tabpanel id
- Tabpanels use role="tabpanel"
- In automatic activation mode, focus = selection (ArrowRight moves AND selects)

### Implementation constraints
- Browser: Firefox headless, viewport 1280x1800
- Keyboard: page.keyboard.press("ArrowRight") only
- aria-selected: read via get_attribute("aria-selected")
- tabpanel visibility: is_visible()
- Output: WORKSPACE/final_runs/run_1/final_script_log.txt
- Screenshots: WORKSPACE/final_runs/run_1/screenshots/

## Phase sequence
1. Explore page structure (quick script to inventory tabs/panels)
2. Write final instrumented script
3. Execute and capture log + screenshots
4. Self-verify log completeness

## Time estimate
- Phase 1 (explore): ~1 min
- Phase 2 (write script): ~2 min
- Phase 3 (execute): ~1 min
- Phase 4 (verify): ~1 min
- Total: ~5 min
