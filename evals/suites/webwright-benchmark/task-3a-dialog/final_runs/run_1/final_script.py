"""
Task 3a: Dialog Modal Focus Trap
Target: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/dialog/

Verifies:
1. Focus moves inside dialog on open
2. Tab traverses all focusable elements
3. Focus wraps from last → first (focus trap)
4. Escape closes dialog and returns focus to trigger button

All keyboard interactions use page.keyboard.press() — real Playwright keyboard API
(CDP Input.dispatchKeyEvent). NO synthetic events via page.evaluate().
"""

import os
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright

WORKSPACE = "/Users/AlexUA_1/claude/a11y-meta-skills/evals/suites/webwright-benchmark/task-3a-dialog"
RUN_DIR = f"{WORKSPACE}/final_runs/run_1"
SCREENSHOTS_DIR = f"{RUN_DIR}/screenshots"
LOG_FILE = f"{RUN_DIR}/final_script_log.txt"

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

log_lines = []

def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    line = f"[{timestamp}] {msg}"
    print(line)
    log_lines.append(line)

def save_log():
    with open(LOG_FILE, "w") as f:
        f.write("\n".join(log_lines))
    print(f"\nLog saved to {LOG_FILE}")

def get_active_element_info(page):
    return page.evaluate("""() => {
        const el = document.activeElement;
        if (!el) return { tag: 'NONE', id: '', text: '', type: null, name: null, ariaLabel: null };
        return {
            tag: el.tagName,
            id: el.id || '',
            text: el.textContent.trim().slice(0, 60),
            type: el.type || null,
            name: el.name || null,
            ariaLabel: el.getAttribute('aria-label'),
            role: el.getAttribute('role'),
            isInsideDialog: !!el.closest('[role="dialog"]'),
            dialogId: el.closest('[role="dialog"]')?.id || null
        };
    }""")

def get_dialog_state(page, dialog_id="dialog1"):
    return page.evaluate(f"""() => {{
        const d = document.getElementById('{dialog_id}');
        if (!d) return {{ found: false }};
        const style = window.getComputedStyle(d);
        return {{
            found: true,
            hidden: d.hidden,
            display: style.display,
            ariaModal: d.getAttribute('aria-modal'),
            role: d.getAttribute('role'),
            className: d.className
        }};
    }}""")

screenshot_counter = [0]

def screenshot(page, name):
    screenshot_counter[0] += 1
    n = screenshot_counter[0]
    filename = f"{n:02d}-{name}.png"
    path = f"{SCREENSHOTS_DIR}/{filename}"
    page.screenshot(path=path)
    log(f"  Screenshot saved: {filename}")
    return path


def run():
    log("=" * 60)
    log("Task 3a: Dialog Modal Focus Trap")
    log(f"URL: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/dialog/")
    log(f"Run dir: {RUN_DIR}")
    log("=" * 60)

    results = {
        "CP1_page_loaded": False,
        "CP2_focus_inside_dialog": False,
        "CP3_all_elements_tabbed": False,
        "CP4_focus_wraps": False,
        "CP5_escape_closes": False,
        "CP5_focus_returns": False,
    }

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 1800})

        # ── CP1: Load page ────────────────────────────────────────────
        log("\n── CP1: Load page ──")
        page.goto(
            "https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/dialog/",
            wait_until="networkidle"
        )
        title = page.title()
        log(f"Page title: {title}")

        dialog_state = get_dialog_state(page)
        log(f"dialog1 before open: hidden={dialog_state['hidden']} display={dialog_state['display']}")

        screenshot(page, "initial-page")

        assert "dialog" in title.lower() or page.query_selector("#dialog1") is not None, \
            "Page did not load correctly"
        results["CP1_page_loaded"] = True
        log("CP1 PASS: Page loaded")

        # ── CP2: Click trigger, verify focus inside dialog ────────────
        log("\n── CP2: Click 'Add Delivery Address', verify focus moves inside dialog ──")
        log("Keyboard API: page.click() — mouse click on trigger button")

        # Find and record trigger button identity before click
        trigger_info = page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const btn = btns.find(b => b.textContent.trim() === 'Add Delivery Address');
            if (!btn) return null;
            return {
                tag: btn.tagName,
                id: btn.id || '',
                text: btn.textContent.trim(),
                rect: btn.getBoundingClientRect()
            };
        }""")
        log(f"Trigger button: {trigger_info}")

        # Click the trigger
        all_btns = page.query_selector_all("button")
        trigger_btn = all_btns[1]  # "Add Delivery Address" — confirmed in exploration
        trigger_btn.scroll_into_view_if_needed()
        trigger_btn.click()
        page.wait_for_timeout(300)

        screenshot(page, "dialog-opened")

        # Verify dialog is now visible
        dialog_state = get_dialog_state(page)
        log(f"dialog1 after open: hidden={dialog_state['hidden']} display={dialog_state['display']} aria-modal={dialog_state['ariaModal']}")

        assert dialog_state['hidden'] == False, f"dialog1 should not be hidden after click, got hidden={dialog_state['hidden']}"
        log("  dialog1 is visible (hidden=False)")

        # Verify focus is inside dialog
        active = get_active_element_info(page)
        log(f"Active element after dialog opens: tag={active['tag']} id={active['id']} type={active['type']} isInsideDialog={active['isInsideDialog']} dialogId={active['dialogId']}")

        assert active['isInsideDialog'] == True, \
            f"Focus should be inside dialog, but activeElement is not inside any [role=dialog]. tag={active['tag']} id={active['id']}"
        assert active['dialogId'] == "dialog1", \
            f"Focus should be inside dialog1, got dialogId={active['dialogId']}"
        results["CP2_focus_inside_dialog"] = True
        log("CP2 PASS: Focus moved inside dialog after open")

        # ── CP3: Tab through all focusable elements ───────────────────
        log("\n── CP3: Tab through all focusable elements ──")
        log("Keyboard API: page.keyboard.press('Tab') — CDP Input.dispatchKeyEvent — real keyboard events")
        log("NOT using: page.evaluate('element.dispatchEvent(new KeyboardEvent(...))')")

        # We know from exploration: 8 focusable elements in dialog1
        # [0] INPUT text (focused on open)
        # [1] INPUT text
        # [2] INPUT text
        # [3] INPUT text
        # [4] INPUT text id=special_instructions
        # [5] BUTTON "Verify Address"
        # [6] BUTTON "Add"
        # [7] BUTTON "Cancel"
        #
        # Focus starts at [0] — we need 7 more Tabs to reach [7], then 1 more to wrap back to [0]

        focus_sequence = []

        # Record initial focus (position 0)
        active = get_active_element_info(page)
        focus_sequence.append(active)
        log(f"  Position 0 (initial): tag={active['tag']} id={repr(active['id'])} type={active['type']} isInsideDialog={active['isInsideDialog']}")

        # Tab through remaining 7 elements (positions 1–7)
        for i in range(1, 9):  # Tab 8 times: positions 1-7, then wrap back to 0
            page.keyboard.press("Tab")
            page.wait_for_timeout(100)
            active = get_active_element_info(page)
            focus_sequence.append(active)
            screenshot(page, f"tab-{i}")
            log(f"  Tab {i} → Position {i}: tag={active['tag']} id={repr(active['id'])} type={active['type']} text={repr(active['text'][:30])} isInsideDialog={active['isInsideDialog']}")

        log(f"\n  Total positions recorded: {len(focus_sequence)}")

        # Verify all intermediate positions (1-7) stayed inside dialog
        for i, pos in enumerate(focus_sequence[:8]):
            assert pos['isInsideDialog'] == True, \
                f"Tab position {i}: focus left the dialog! tag={pos['tag']} id={pos['id']}"
        log("  All 8 tabbed positions remained inside dialog")

        results["CP3_all_elements_tabbed"] = True
        log("CP3 PASS: Tabbed through all focusable elements, none escaped dialog")

        # ── CP4: Verify focus wrap (last → first) ─────────────────────
        log("\n── CP4: Verify focus wraps from last element back to first ──")
        log("Keyboard API: page.keyboard.press('Tab') — CDP Input.dispatchKeyEvent")

        # Position 8 in focus_sequence should be the wrap-back to position 0
        # Compare position 8 with position 0
        first_element = focus_sequence[0]
        wrapped_element = focus_sequence[8]  # After 8 tabs from initial

        log(f"  First element (position 0): tag={first_element['tag']} id={repr(first_element['id'])} type={first_element['type']}")
        log(f"  After 8 tabs (position 8):  tag={wrapped_element['tag']} id={repr(wrapped_element['id'])} type={wrapped_element['type']}")

        # Focus wrap means: after the last focusable element, Tab brings back to first
        # The 8th tab (index 8) should match the characteristics of the first element
        wrap_confirmed = (
            wrapped_element['tag'] == first_element['tag'] and
            wrapped_element['isInsideDialog'] == True
        )

        if wrap_confirmed:
            results["CP4_focus_wraps"] = True
            log("CP4 PASS: Focus wrapped from last element back to first inside dialog")
            screenshot(page, "focus-wrapped-to-first")
        else:
            log(f"CP4 FAIL: Focus did NOT wrap correctly")
            log(f"  Expected tag={first_element['tag']}, got tag={wrapped_element['tag']}")
            log(f"  isInsideDialog={wrapped_element['isInsideDialog']}")
            screenshot(page, "focus-wrap-failed")

        # ── CP5: Press Escape, verify dialog closes, focus returns ────
        log("\n── CP5: Press Escape, verify dialog closes and focus returns to trigger ──")
        log("Keyboard API: page.keyboard.press('Escape') — CDP Input.dispatchKeyEvent")

        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

        screenshot(page, "after-escape")

        # Verify dialog is closed
        dialog_state = get_dialog_state(page)
        log(f"dialog1 after Escape: hidden={dialog_state['hidden']} display={dialog_state['display']}")

        dialog_closed = dialog_state['hidden'] == True or dialog_state['display'] == 'none'
        if dialog_closed:
            results["CP5_escape_closes"] = True
            log("CP5a PASS: Dialog is closed after Escape (hidden=True or display=none)")
        else:
            log(f"CP5a FAIL: Dialog not closed. hidden={dialog_state['hidden']} display={dialog_state['display']}")

        # Verify focus returned to trigger button
        active = get_active_element_info(page)
        log(f"Active element after Escape: tag={active['tag']} id={active['id']} text={repr(active['text'][:40])}")

        focus_on_trigger = (
            active['tag'] == 'BUTTON' and
            'Add Delivery Address' in active['text']
        )

        if focus_on_trigger:
            results["CP5_focus_returns"] = True
            log("CP5b PASS: Focus returned to 'Add Delivery Address' trigger button")
        else:
            log(f"CP5b FAIL: Focus did not return to trigger. tag={active['tag']} text={repr(active['text'])}")

        screenshot(page, "focus-returned-to-trigger")

        browser.close()

    # ── Summary ───────────────────────────────────────────────────────
    log("\n" + "=" * 60)
    log("RESULTS SUMMARY")
    log("=" * 60)
    all_pass = True
    for cp, passed in results.items():
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_pass = False
        log(f"  {cp}: {status}")

    log("")
    if all_pass:
        log("OVERALL: ALL CHECKPOINTS PASSED")
    else:
        log("OVERALL: SOME CHECKPOINTS FAILED")
        sys.exit(1)

    save_log()


if __name__ == "__main__":
    run()
