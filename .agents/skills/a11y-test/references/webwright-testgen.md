# Test script generation with Webwright

**When to use:** You have a prose a11y requirement (from the planner or a ticket) and need a runnable test script, without hand-writing it.

**What it produces:** A Python Playwright script with navigation, keyboard interactions, ARIA state assertions, and screenshots. Webwright generates `sync_playwright` scripts by default — if you need async for an existing test harness, specify in the prompt.

**Language mismatch warning:** Webwright generates Python. Existing CI is Node.js/.spec.js. Generated scripts are starting points — for CI, port logic to .spec.js using the APG templates in `references/keyboard-test-patterns.md`, or run Python directly if a Python test runner is available.

**Example `/webwright:run`** (actual prompt that produced a passing dialog focus trap test in benchmark):
```
/webwright:run Navigate to https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/dialog/.
Open the modal by clicking the trigger button.
Verify focus moves into the modal.
Tab through all focusable elements and verify focus wraps (focus trap).
Press Escape and verify the modal closes and focus returns to the trigger.
```

**Quality gate:** The operator must review generated scripts before trusting results. Check that:
- Keyboard events use `page.keyboard.press()` or `locator.press()`, NOT synthetic `dispatchEvent`
- Assertions verify state changes (before/after), not just attribute presence
- No `time.sleep()` > 5 seconds or hardcoded waits that mask timing issues

**ARIA snapshot capability:** Webwright's Playwright environment captures `page.locator("body").aria_snapshot()` — the full accessibility tree with roles, states, and relationships as structured YAML. Richer than `agent-browser snapshot -i --max-output 8000` for structural analysis (captures all 4 tab→panel relationships via aria-controls/aria-labelledby cross-references, vs. agent-browser which shows only interactive element refs).

**Limitations:**
- No built-in axe-core — the LLM must write injection code (it does this correctly; see benchmark task 3c)
- May miss a11y-specific patterns unless the prompt is specific about what to check
- Python scripts don't run in JS CI without a Python runner
- Requires Claude Code plugin install — not available in Codex CLI
- Do not run simultaneously with agent-browser — both launch Chrome instances that may conflict on ports

**Benchmark results (2026-05-26):** 25/25 across 5 WAI-ARIA APG tasks (dialog focus trap, tabs ARIA state, axe-core injection, menu keyboard navigation, ARIA tree inspection). All scripts used real `page.keyboard.press()` calls. Full results in `evals/suites/webwright-benchmark/`.

### Installation

**Prerequisites:** Python 3.10+, Playwright Python (`pip install playwright && playwright install chromium`)

**Two-step install:**
1. `/plugin marketplace add microsoft/Webwright`
2. `/plugin install webwright@webwright`

**If marketplace fails:** `git clone https://github.com/microsoft/Webwright && /plugin install ./Webwright`

**Platform note:** Claude Code plugin only. Not available in Codex CLI. From Codex, the usable browser automation options are `agent-browser` and `keyboard-a11y-tester` (both plain CLIs). Generated `.py` scripts can be executed from Codex via `python3 script.py`.

