# Task 3a: Dialog Modal Focus Trap - Execution Plan

## Target
URL: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/dialog/

## Critical Points

### CP1: Initial Page State
- Capture screenshot of page before any interaction
- Identify the trigger button selector (likely "Add Delivery Address" or similar)
- Verify page loaded successfully

### CP2: Open Dialog
- Click the trigger button using page.click()
- Screenshot immediately after click
- Verify focus moved inside dialog using page.evaluate("document.activeElement.tagName")
- Check aria-modal="true" or role="dialog" on the dialog container
- Check dialog is visible (not hidden)

### CP3: Focus Trap - Forward Tab
- Use page.keyboard.press("Tab") — REAL keyboard API (CDP Input.dispatchKeyEvent)
- NEVER use page.evaluate('element.dispatchEvent(new KeyboardEvent(...))')
- Tab through all focusable elements, logging activeElement at each step
- Record: tagName, id, textContent, aria-label for each focused element
- Screenshot at each Tab press

### CP4: Focus Wrap (Last → First)
- After reaching last focusable element, press Tab once more
- Verify focus returns to FIRST focusable element inside dialog
- This confirms the focus trap is working
- Screenshot showing focus on first element again

### CP5: Escape to Close
- Press page.keyboard.press("Escape")
- Screenshot immediately after
- Verify dialog is no longer visible (hidden/removed from DOM)
- Verify focus returned to trigger button (the element that opened the dialog)

## Selectors Strategy
- Explore the page first with a short script to find dialog button selectors
- Use role/aria attributes where possible (more robust than CSS class selectors)
- Fallback to text content matching

## File Outputs
- WORKSPACE/plan.md (this file)
- WORKSPACE/final_runs/run_1/final_script_log.txt — full text log
- WORKSPACE/final_runs/run_1/screenshots/ — named sequentially:
  - 01-initial-page.png
  - 02-dialog-opened.png
  - 03-tab-1.png, 04-tab-2.png, ... (one per Tab press)
  - N-dialog-wrap.png (focus wrapped back to first)
  - N+1-escape-pressed.png (dialog closed)
  - N+2-focus-returned.png (focus on trigger button)

## Keyboard API Confirmation
All keyboard interactions use Playwright's real keyboard API:
- page.keyboard.press("Tab") → CDP Input.dispatchKeyEvent → real browser keyboard event
- page.keyboard.press("Escape") → CDP Input.dispatchKeyEvent → real browser keyboard event
- page.keyboard.press("Shift+Tab") → if needed for reverse tab
NO synthetic events via page.evaluate() dispatchEvent

## Time Estimate
- Phase 1 (exploration script): ~1 min
- Phase 2 (full instrumented script): ~2 min
- Phase 3 (self-verification): ~1 min
Total: ~4 min
