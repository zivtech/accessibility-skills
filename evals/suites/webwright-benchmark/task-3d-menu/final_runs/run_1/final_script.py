"""
Task 3D: Menu Button with Active Descendant — Keyboard Interaction Test
WAI-ARIA APG example: menu-button-actions-active-descendant

Pattern: aria-activedescendant on the focused menu container (#menu1)
Keys tested: Enter, ArrowDown, End, Escape
"""

import os
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright

WORKSPACE = "/Users/AlexUA_1/claude/a11y-meta-skills/evals/suites/webwright-benchmark/task-3d-menu/final_runs/run_1"
LOG_PATH = os.path.join(WORKSPACE, "final_script_log.txt")
SS_DIR = os.path.join(WORKSPACE, "screenshots")
URL = "https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/examples/menu-button-actions-active-descendant/"

os.makedirs(SS_DIR, exist_ok=True)

lines = []

def log(msg):
    lines.append(msg)
    print(msg)

def check(label, actual, expected, passed_list):
    if actual == expected:
        result = f"  PASS  {label}: got {actual!r}"
        passed_list.append(True)
    else:
        result = f"  FAIL  {label}: expected {expected!r}, got {actual!r}"
        passed_list.append(False)
    log(result)

results = []

log("=" * 70)
log(f"Task 3D: Menu Button Active Descendant")
log(f"Run: {datetime.now().isoformat()}")
log(f"URL: {URL}")
log("=" * 70)

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 1800})

    log("\n[SETUP] Navigating to page...")
    page.goto(URL, wait_until="networkidle")
    log("  Page loaded.")

    btn = page.locator("#menubutton1")
    menu = page.locator("#menu1")

    # ── Step 0: Focus the button ──────────────────────────────────────────
    log("\n[STEP 0] Focus the menu button (#menubutton1)")
    btn.focus()
    page.wait_for_timeout(100)

    focused_id = page.evaluate("document.activeElement.id")
    log(f"  Key pressed: (Tab/focus — no keyboard press, direct .focus() call)")
    log(f"  Focused element id: {focused_id!r}")
    check("Button has focus", focused_id, "menubutton1", results)

    expanded = btn.get_attribute("aria-expanded")
    check("Menu closed before Enter", expanded, "false", results)

    page.screenshot(path=os.path.join(SS_DIR, "01_button_focused.png"))
    log("  Screenshot: 01_button_focused.png")

    # ── Step 1: Press Enter — open menu ───────────────────────────────────
    log("\n[STEP 1] Press Enter to open menu")
    page.keyboard.press("Enter")
    page.wait_for_timeout(300)

    expanded = btn.get_attribute("aria-expanded")
    menu_visible = menu.is_visible()
    focused_id = page.evaluate("document.activeElement.id")
    aad = menu.get_attribute("aria-activedescendant")

    log(f"  Key pressed: Enter")
    log(f"  aria-expanded on button: {expanded!r}")
    log(f"  menu #menu1 visible: {menu_visible}")
    log(f"  DOM focused element: {focused_id!r}")
    log(f"  aria-activedescendant on #menu1: {aad!r}")

    check("aria-expanded=true after Enter", expanded, "true", results)
    check("Menu is visible", str(menu_visible), "True", results)
    check("Focus moved to #menu1", focused_id, "menu1", results)
    check("aria-activedescendant = mi1 (first item)", aad, "mi1", results)

    page.screenshot(path=os.path.join(SS_DIR, "02_menu_opened_enter.png"))
    log("  Screenshot: 02_menu_opened_enter.png")

    # ── Step 2: Press ArrowDown — move to second item ─────────────────────
    log("\n[STEP 2] Press ArrowDown — expect focus moves to second menuitem (mi2)")
    page.keyboard.press("ArrowDown")
    page.wait_for_timeout(150)

    aad = menu.get_attribute("aria-activedescendant")
    focused_id = page.evaluate("document.activeElement.id")

    log(f"  Key pressed: ArrowDown")
    log(f"  DOM focused element: {focused_id!r}")
    log(f"  aria-activedescendant on #menu1: {aad!r}")

    check("Focus on #menu1 still", focused_id, "menu1", results)
    check("aria-activedescendant = mi2 (second item)", aad, "mi2", results)

    page.screenshot(path=os.path.join(SS_DIR, "03_arrowdown_mi2.png"))
    log("  Screenshot: 03_arrowdown_mi2.png")

    # ── Step 3: Press End — move to last item ─────────────────────────────
    log("\n[STEP 3] Press End — expect focus moves to last menuitem (mi4)")
    page.keyboard.press("End")
    page.wait_for_timeout(150)

    aad = menu.get_attribute("aria-activedescendant")
    focused_id = page.evaluate("document.activeElement.id")

    log(f"  Key pressed: End")
    log(f"  DOM focused element: {focused_id!r}")
    log(f"  aria-activedescendant on #menu1: {aad!r}")

    check("Focus on #menu1 still", focused_id, "menu1", results)
    check("aria-activedescendant = mi4 (last item)", aad, "mi4", results)

    page.screenshot(path=os.path.join(SS_DIR, "04_end_mi4.png"))
    log("  Screenshot: 04_end_mi4.png")

    # ── Step 4: Press Escape — close menu, return focus to button ─────────
    log("\n[STEP 4] Press Escape — expect menu closes, focus returns to button")
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)

    expanded = btn.get_attribute("aria-expanded")
    menu_visible = menu.is_visible()
    focused_id = page.evaluate("document.activeElement.id")

    log(f"  Key pressed: Escape")
    log(f"  aria-expanded on button: {expanded!r}")
    log(f"  menu #menu1 visible: {menu_visible}")
    log(f"  DOM focused element: {focused_id!r}")

    check("aria-expanded=false after Escape", expanded, "false", results)
    check("Menu is hidden", str(menu_visible), "False", results)
    check("Focus returned to #menubutton1", focused_id, "menubutton1", results)

    page.screenshot(path=os.path.join(SS_DIR, "05_escaped_menu_closed.png"))
    log("  Screenshot: 05_escaped_menu_closed.png")

    browser.close()

# ── Summary ───────────────────────────────────────────────────────────────
log("\n" + "=" * 70)
passed = sum(results)
total = len(results)
log(f"SUMMARY: {passed}/{total} checks passed")
if passed == total:
    log("STATUS: ALL PASS")
else:
    log("STATUS: SOME FAILURES — see FAIL lines above")
log("=" * 70)

with open(LOG_PATH, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"\nLog written to: {LOG_PATH}")
sys.exit(0 if passed == total else 1)
