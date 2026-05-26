# Task 3D Menu — Execution Plan

## Target
URL: https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/examples/menu-button-actions-active-descendant/

Pattern: Menu Button with Active Descendant (no roving tabindex — focus stays on the menu container, aria-activedescendant tracks the active item).

## Critical Points

### aria-activedescendant pattern
- In this pattern, the menu `<ul role="menu">` holds DOM focus
- The highlighted item is tracked via `aria-activedescendant` on the focused menu element (not on each menuitem)
- `aria-activedescendant` value = the `id` of the currently active menuitem
- This is different from roving tabindex where individual items receive DOM focus

### Key assertions per step
1. Focus the button: `document.activeElement` is the button
2. Press Enter: menu appears (`aria-expanded="true"`), menu container gains focus, `aria-activedescendant` points to first menuitem id
3. Press ArrowDown: `aria-activedescendant` updates to second menuitem id
4. Press End: `aria-activedescendant` updates to last menuitem id
5. Press Escape: menu hidden (`aria-expanded="false"`), focus returns to button

### Implementation constraints
- Use `page.keyboard.press()` exclusively — no `dispatchEvent`
- Read `aria-activedescendant` via `get_attribute("aria-activedescendant")`
- Check visibility via `is_visible()` or `aria-expanded`
- Browser: Firefox headless, viewport 1280x1800
- No `full_page=True` on screenshots

### Output
- Log: WORKSPACE/final_runs/run_1/final_script_log.txt
- Screenshots: WORKSPACE/final_runs/run_1/screenshots/
- Script: WORKSPACE/final_runs/run_1/final_script.py

## Time estimate
- Phase 1 (plan): done
- Phase 2 (explore): ~1 min
- Phase 3 (script + execute): ~2 min
- Phase 4 (self-verify): ~1 min
- Total: ~4 min
