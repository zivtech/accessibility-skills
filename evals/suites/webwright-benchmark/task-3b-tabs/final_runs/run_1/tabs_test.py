"""
Task 3b: Tabs Automatic Activation — ARIA verification script
Target: https://www.w3.org/WAI/ARIA/apg/patterns/tabs/examples/tabs-automatic/

Verifies:
1. Click each tab → only that tab has aria-selected="true", its panel visible, others hidden
2. Keyboard: focus first tab, ArrowRight → second tab selected
"""

import os
from datetime import datetime
from playwright.sync_api import sync_playwright

WORKSPACE = "/Users/AlexUA_1/claude/a11y-meta-skills/evals/suites/webwright-benchmark/task-3b-tabs/final_runs/run_1"
SCREENSHOTS_DIR = os.path.join(WORKSPACE, "screenshots")
LOG_FILE = os.path.join(WORKSPACE, "final_script_log.txt")
URL = "https://www.w3.org/WAI/ARIA/apg/patterns/tabs/examples/tabs-automatic/"

os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

lines = []

def log(msg=""):
    print(msg)
    lines.append(msg)

def save_log():
    with open(LOG_FILE, "w") as f:
        f.write("\n".join(lines) + "\n")

def get_all_tab_states(tabs):
    return [(t.get_attribute("id"), t.get_attribute("aria-selected"), t.inner_text().strip()) for t in tabs]

def get_all_panel_states(panels):
    return [(p.get_attribute("id"), p.is_visible()) for p in panels]

def check_only_one_selected(tab_states, expected_selected_id):
    errors = []
    for tid, selected, text in tab_states:
        if tid == expected_selected_id:
            if selected != "true":
                errors.append(f"  ERROR: {tid} ({text!r}) should be aria-selected='true' but got {selected!r}")
        else:
            if selected != "false":
                errors.append(f"  ERROR: {tid} ({text!r}) should be aria-selected='false' but got {selected!r}")
    return errors

def check_panel_visibility(panel_states, expected_visible_id):
    errors = []
    for pid, visible in panel_states:
        if pid == expected_visible_id:
            if not visible:
                errors.append(f"  ERROR: {pid} should be visible but is hidden")
        else:
            if visible:
                errors.append(f"  ERROR: {pid} should be hidden but is visible")
    return errors

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 1800})

    log("=" * 70)
    log(f"Task 3b: Tabs Automatic Activation")
    log(f"URL: {URL}")
    log(f"Run: {datetime.now().isoformat()}")
    log("=" * 70)

    page.goto(URL, wait_until="networkidle")

    tabs = page.query_selector_all('[role="tab"]')
    panels = page.query_selector_all('[role="tabpanel"]')

    log(f"\nDiscovered {len(tabs)} tabs and {len(panels)} tabpanels")

    tab_ids = [t.get_attribute("id") for t in tabs]
    tab_controls = [t.get_attribute("aria-controls") for t in tabs]
    tab_labels = [t.inner_text().strip() for t in tabs]
    panel_ids = [p.get_attribute("id") for p in panels]

    log("\nTab inventory:")
    for i, (tid, ctrl, label) in enumerate(zip(tab_ids, tab_controls, tab_labels)):
        log(f"  Tab {i}: id={tid!r}, aria-controls={ctrl!r}, text={label!r}")

    log("\nPanel inventory:")
    for pid in panel_ids:
        log(f"  Panel: id={pid!r}")

    # ─────────────────────────────────────────────────────────────────
    # SECTION 1: Click each tab
    # ─────────────────────────────────────────────────────────────────
    log("\n" + "─" * 70)
    log("SECTION 1: Click each tab")
    log("─" * 70)

    all_click_pass = True

    for i, tab in enumerate(tabs):
        tab_id = tab_ids[i]
        expected_panel_id = tab_controls[i]
        label = tab_labels[i]

        log(f"\n[Tab {i+1}/{len(tabs)}] Clicking: {label!r} (id={tab_id!r})")

        tab.click()
        page.wait_for_timeout(200)  # slight settle for visibility changes

        tab_states = get_all_tab_states(tabs)
        panel_states = get_all_panel_states(panels)

        log(f"  aria-selected state after click:")
        for tid, selected, tlabel in tab_states:
            marker = " <-- clicked" if tid == tab_id else ""
            log(f"    {tid}: aria-selected={selected!r}{marker}")

        log(f"  tabpanel visibility after click:")
        for pid, visible in panel_states:
            marker = " <-- expected visible" if pid == expected_panel_id else ""
            log(f"    {pid}: visible={visible}{marker}")

        # Verify
        sel_errors = check_only_one_selected(tab_states, tab_id)
        vis_errors = check_panel_visibility(panel_states, expected_panel_id)
        all_errors = sel_errors + vis_errors

        if all_errors:
            all_click_pass = False
            log(f"  RESULT: FAIL")
            for e in all_errors:
                log(e)
        else:
            log(f"  RESULT: PASS — only {tab_id!r} selected, {expected_panel_id!r} visible, all others hidden")

        # Screenshot
        screenshot_path = os.path.join(SCREENSHOTS_DIR, f"tab_{i+1}_click_{tab_id}.png")
        page.screenshot(path=screenshot_path)
        log(f"  Screenshot: {screenshot_path}")

    log("\n" + "─" * 70)
    log(f"SECTION 1 SUMMARY: {'ALL PASS' if all_click_pass else 'FAILURES DETECTED'}")
    log("─" * 70)

    # ─────────────────────────────────────────────────────────────────
    # SECTION 2: Keyboard test — ArrowRight from first tab
    # ─────────────────────────────────────────────────────────────────
    log("\n" + "─" * 70)
    log("SECTION 2: Keyboard test — ArrowRight from first tab")
    log("─" * 70)

    # Reset to page load state by navigating again so tab-1 is selected
    page.goto(URL, wait_until="networkidle")
    tabs = page.query_selector_all('[role="tab"]')
    panels = page.query_selector_all('[role="tabpanel"]')

    log(f"\nPage reloaded. Initial state:")
    initial_tab_states = get_all_tab_states(tabs)
    for tid, selected, tlabel in initial_tab_states:
        log(f"  {tid}: aria-selected={selected!r}")

    # Focus the first tab
    tabs[0].focus()
    page.wait_for_timeout(100)
    log(f"\nFocused first tab: {tab_ids[0]!r}")

    before_tab_states = get_all_tab_states(tabs)
    before_panel_states = get_all_panel_states(panels)

    log(f"\nBEFORE ArrowRight:")
    log(f"  aria-selected:")
    for tid, selected, tlabel in before_tab_states:
        log(f"    {tid}: aria-selected={selected!r}")
    log(f"  panel visibility:")
    for pid, visible in before_panel_states:
        log(f"    {pid}: visible={visible}")

    # Press ArrowRight using real Playwright keyboard API
    log(f"\nPressing ArrowRight via page.keyboard.press('ArrowRight')...")
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(200)

    after_tab_states = get_all_tab_states(tabs)
    after_panel_states = get_all_panel_states(panels)

    log(f"\nAFTER ArrowRight:")
    log(f"  aria-selected:")
    for tid, selected, tlabel in after_tab_states:
        log(f"    {tid}: aria-selected={selected!r}")
    log(f"  panel visibility:")
    for pid, visible in after_panel_states:
        log(f"    {pid}: visible={visible}")

    # Expected: tab-2 now selected, tab-1 deselected
    expected_after_id = tab_ids[1]  # second tab
    expected_after_panel = tab_controls[1]

    kb_sel_errors = check_only_one_selected(after_tab_states, expected_after_id)
    kb_vis_errors = check_panel_visibility(after_panel_states, expected_after_panel)
    kb_all_errors = kb_sel_errors + kb_vis_errors

    # Additional specific checks for the keyboard transition
    first_before = before_tab_states[0][1]   # tab-1 before
    first_after  = after_tab_states[0][1]    # tab-1 after
    second_before = before_tab_states[1][1]  # tab-2 before
    second_after  = after_tab_states[1][1]   # tab-2 after

    log(f"\nKeyboard transition detail:")
    log(f"  {tab_ids[0]!r}: {first_before!r} → {first_after!r}  (expected: 'true' → 'false')")
    log(f"  {tab_ids[1]!r}: {second_before!r} → {second_after!r}  (expected: 'false' → 'true')")

    kb_pass = len(kb_all_errors) == 0
    if kb_all_errors:
        log(f"\nKEYBOARD RESULT: FAIL")
        for e in kb_all_errors:
            log(e)
    else:
        log(f"\nKEYBOARD RESULT: PASS — ArrowRight moved selection from {tab_ids[0]!r} to {tab_ids[1]!r}")

    screenshot_path = os.path.join(SCREENSHOTS_DIR, "keyboard_after_arrow_right.png")
    page.screenshot(path=screenshot_path)
    log(f"Screenshot: {screenshot_path}")

    log("\n" + "─" * 70)
    log(f"SECTION 2 SUMMARY: {'PASS' if kb_pass else 'FAIL'}")
    log("─" * 70)

    # ─────────────────────────────────────────────────────────────────
    # OVERALL SUMMARY
    # ─────────────────────────────────────────────────────────────────
    log("\n" + "=" * 70)
    log("OVERALL SUMMARY")
    log("=" * 70)
    log(f"  Click tests:    {'PASS' if all_click_pass else 'FAIL'}")
    log(f"  Keyboard test:  {'PASS' if kb_pass else 'FAIL'}")
    overall = all_click_pass and kb_pass
    log(f"  OVERALL:        {'PASS' if overall else 'FAIL'}")
    log("=" * 70)

    browser.close()

save_log()
print(f"\nLog written to: {LOG_FILE}")
