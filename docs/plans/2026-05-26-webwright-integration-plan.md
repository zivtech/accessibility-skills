# Webwright Integration into a11y-test — Reconciled Plan

> **Status:** Complete — Phase 1 gate passed 25/25, Phases 2-3 docs applied 2026-05-26
> **Consequence level:** Internal Tool (prompt-only skill modification, no production code, no user-facing risk)
> **Reconciles:** Original integration plan (plan-writer) + benchmark protocol (test-planner) + proposal-critic findings

**Goal:** Add Microsoft Webwright as a third browser-automation lane in the a11y-test skill, alongside `npx playwright test` and `agent-browser`, without breaking existing workflows.

**Timeframe:** 1 focused session (~2.5-3 hours). Phase 1 (verify + benchmark) is ~2 hours; Phases 2-3 (docs) add ~45 minutes if the gate passes.

**Scope:**
- **Must-have:** Plugin installation, keyboard event verification, 5-task a11y benchmark, updated SKILL.md routing table, workflow docs.
- **Nice-to-have:** `score_webwright.py` static scorer, `/webwright:craft` template evaluation.
- **Explicitly OUT of scope:** Replacing agent-browser or npx playwright test. Modifying planner/critic/perspective-audit skills. Building Webwright itself. Changes to Ollama portability layer. CI integration of Python scripts. Statistical significance testing.

---

## Why Webwright (Approach A: Script Generation Focus)

Webwright fills a gap neither existing tool covers: **generating complete test scripts from prose specifications**. You describe what to test in natural language; it produces a runnable Python Playwright script.

| Tool | What the LLM does | Persistent artifact | Best for |
|---|---|---|---|
| `npx playwright test` | Nothing — human wrote the test | `.spec.js` file | CI, regression, codified APG patterns |
| `agent-browser` | Issues discrete CLI commands | Session log | Interactive recon, ARIA probing, fix verification |
| **Webwright** | Writes full Python scripts, iterates | `.py` file (reusable) | Generating tests from prose specs |

**Why not replace agent-browser?** agent-browser's command-by-command interactivity (snapshot → inspect ref → act → check state) is superior for exploratory work where the next action depends on what you just found. Webwright's batch-script model re-runs the whole script when one step is wrong.

**Why not full convergence (Approach C)?** Both Approach A and C introduce Python/JS friction. We accept this at Approach A's smaller scale — generated drafts only, not production tests. The language boundary acts as a forced review gate: nothing enters CI without conscious porting. If generated Python scripts become the primary output rather than drafts (scope creep), revisit this decision.

---

## Critic Findings Addressed

| Critic Finding | Severity | Resolution |
|---|---|---|
| Two plans uncoordinated — no defined relationship | CRITICAL | Merged into single plan. One benchmark, one gate decision. |
| Fixture format mismatch — React JSX not convertible to static HTML | CRITICAL | Use public WAI-ARIA APG example pages instead. No build step, already hosted. |
| `page.press()` is Node.js syntax, not Python async API | MAJOR | Corrected to `page.keyboard.press()` and `locator.press()` throughout. |
| Routing table 6 rows creates decision fatigue | MAJOR | Merged Webwright rows into one. Table stays at 5 rows. |
| Statistical claims on insufficient data (3 reps) | MAJOR | Dropped statistical tests. Descriptive stats + qualitative judgment. |
| Approach A/C friction framing gap | MAJOR | Explicitly acknowledged as same friction, smaller scale (see above). |
| No consolidated decision framework | MISSING | Single gate with explicit thresholds (see Phase 1 scoring). |
| No cost accounting for 540 LLM runs | MISSING | Reduced to ~15 Webwright runs + 5 agent-browser runs. One CC session. |
| Plan 2 artifacts rollback undefined | MISSING | Benchmark artifacts stay regardless — they document what we learned. |
| ARIA snapshot row pre-committed before validation | MISSING | ARIA snapshot mentioned as sub-bullet, not separate row. Validated in Task 5. |

---

## Assumption Register

| # | Assumption | Rating | Gate | Impact if Wrong |
|---|---|---|---|---|
| A1 | Webwright plugin installs via `/plugin marketplace add microsoft/Webwright` + `/plugin install webwright@webwright` | FRAGILE | Task 1 | Plan halts. Fallback: local clone. |
| A2 | Webwright's LLM generates `page.keyboard.press()` / `locator.press()` (Playwright Python async API), not synthetic `page.evaluate('el.dispatchEvent(...)')` | FRAGILE | Task 2 | Scripts violate "real keyboard events" mandate. Restrict to non-keyboard tasks. |
| A3 | Webwright's LLM-generated scripts are useful for a11y testing without a11y-specific fine-tuning | FRAGILE | Task 3 | Lane is technically functional but practically useless. Defer integration. |
| A4 | CC plugin mode uses host subscription (no extra API cost) | REASONABLE | Task 1 | Hidden costs. Document prominently. |
| A5 | Webwright subprocess doesn't conflict with agent-browser's Chrome instance | REASONABLE | Runtime | Document: don't run simultaneously on same Chrome. |
| A6 | Both tools run same Claude model in CC plugin mode (model parity) | CONFIDENT | Verify logs | If Webwright calls a different model internally, results aren't comparable. |

---

## Phase 1: Verification and Benchmark (GATE)

**Duration:** ~90 minutes. **If Tasks 1-2 fail: STOP.** If Task 3 scores 0/5: defer integration.

### Task 1: Install and Verify Webwright Plugin

**Prerequisites:** Python 3.10+, Playwright Python (`pip install playwright && playwright install chromium`)

**Steps:**
1. `/plugin marketplace add microsoft/Webwright`
2. `/plugin install webwright@webwright`
3. Invoke `/webwright:run "Navigate to https://example.com and take a screenshot"`
4. Confirm: `.py` script generated, executes, produces output

**If marketplace fails:** `git clone https://github.com/microsoft/Webwright && /plugin install ./Webwright`
**If both fail:** STOP. Document failure. Plan cannot proceed.

**Record:** Exact install commands, version, any gotchas, Codex CLI incompatibility (plugin is CC-only).

### Task 2: Keyboard Event Code Generation Verification (Canary Gate)

**Target:** WAI-ARIA APG Disclosure FAQ — `https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-faq/`

**Prompt for Webwright:**
> Navigate to https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-faq/. Find the first disclosure button. Record its aria-expanded value. Press Enter on it using Playwright's keyboard API. Record the new aria-expanded value. Assert they are different. Take a screenshot before and after.

**Primary gate — Code inspection:** Read the generated `.py` script. Verify it uses:
- `page.keyboard.press("Enter")` or `locator.press("Enter")` — the Playwright Python async keyboard API
- NOT `page.evaluate('element.dispatchEvent(new KeyboardEvent(...))')` — synthetic events
- `get_attribute("aria-expanded")` called before AND after the keyboard action

Both Playwright Python and Node.js dispatch via CDP `Input.dispatchKeyEvent` under the hood. The risk isn't the delivery mechanism — it's whether the LLM writes the correct API calls.

**Secondary — Execution verification:** Run the script. Confirm `aria-expanded` toggles from `"false"` to `"true"`.

**Baseline comparison:** Run the same task with agent-browser:
```bash
agent-browser open https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-faq/
agent-browser snapshot -i
agent-browser focus @<trigger-ref>
agent-browser get attr @<trigger-ref> aria-expanded   # expect "false"
agent-browser press Enter
agent-browser get attr @<trigger-ref> aria-expanded   # expect "true"
```

**If code inspection fails (LLM generates synthetic events):** Add prompt engineering guidance ("always use page.keyboard.press, not dispatchEvent"). Re-test once. If still fails, restrict Webwright to non-keyboard tasks only (axe-core injection, ARIA snapshots).

**If execution fails despite correct API calls:** Investigate (timeout? selector mismatch? async timing?). This is script quality, not keyboard delivery.

### Task 3: A11y Capability Benchmark (5 tasks against WAI-ARIA APG examples)

All targets are public WAI-ARIA APG example pages — no build step, no React conversion, stable URLs.

| # | Task | APG Example URL | What to verify | Widget Pattern |
|---|---|---|---|---|
| 3a | Focus trap detection | APG Dialog (Modal) example | Tab wraps inside dialog, Escape closes, focus returns to trigger | Dialog |
| 3b | Tab panel ARIA state | APG Tabs (Automatic) example | Only one tab has aria-selected="true", tabpanel visible matches active tab, arrow keys move selection | Tabs |
| 3c | axe-core injection | APG Disclosure FAQ example | Inject axe-core via CDN, run axe.run(), report violations with impact level | Scanning |
| 3d | Menu keyboard navigation | APG Menu Button example | Enter opens menu, arrow keys navigate, Escape closes, Home/End work | Menu |
| 3e | ARIA tree inspection | APG Tabs example (same as 3b) | Capture `aria_snapshot()` / full accessibility tree, identify all roles and states | ARIA snapshot |

**Exact prompts for Webwright:**

**3a (Dialog focus trap):**
> Navigate to https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/dialog/. Click the button that opens the modal dialog. Verify focus moves inside the dialog. Tab through all focusable elements and verify focus wraps from the last element back to the first (focus trap). Press Escape and verify the dialog closes and focus returns to the trigger button. Take screenshots before and after each interaction.

**3b (Tabs ARIA state):**
> Navigate to https://www.w3.org/WAI/ARIA/apg/patterns/tabs/examples/tabs-automatic/. Click each tab. For each tab, verify: only one tab has aria-selected="true", the corresponding tabpanel is visible, and the previously active tabpanel is hidden. Then test keyboard: focus the first tab, press ArrowRight, verify the next tab becomes selected.

**3c (axe-core injection):**
> Navigate to https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-faq/. Inject axe-core by adding a script tag pointing to https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js. Run axe.run(document) and report all violations with their impact level, description, and affected elements.

**3d (Menu keyboard navigation):**
> Navigate to https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/examples/menu-button-actions-active-descendant/. Focus the menu button. Press Enter to open the menu. Verify the menu appears and the first menuitem receives focus. Press ArrowDown and verify focus moves to the next item. Press End and verify focus moves to the last item. Press Escape and verify the menu closes and focus returns to the button.

**3e (ARIA tree inspection):**
> Navigate to https://www.w3.org/WAI/ARIA/apg/patterns/tabs/examples/tabs-automatic/. Capture the full ARIA accessibility tree using aria_snapshot(). Identify all elements with roles (tablist, tab, tabpanel), their states (aria-selected, aria-controls, aria-labelledby), and the relationships between tabs and panels.

**Execution protocol:**
- Run each task once with Webwright (`/webwright:run "<prompt above>"`)
- Run tasks 3a, 3b, 3d with agent-browser **sequentially after Webwright** for qualitative comparison (do not run simultaneously — both tools launch Chrome instances that may conflict on ports). The agent-browser runs are informational context, not scored — the gate decision is based solely on Webwright's scores.
- Tasks 3c and 3e test Webwright-only capabilities (axe-core injection, aria_snapshot) with no agent-browser comparison.
- Record: generated `.py` file, execution log, screenshots, wall-clock time
- Store raw results in `evals/suites/webwright-benchmark/`

**Per-task scoring (binary + quality):**

| Metric | Scoring |
|---|---|
| Reachable | Did the tool reach the target widget? 0/1 |
| Keyboard API correct | Generated script uses `page.keyboard.press()` / `locator.press()`, not synthetic events? 0/1 |
| State verification | Script reads ARIA state before AND after interaction? 0/1 |
| Correct outcome | Script's assertions match the expected widget behavior? 0/1 |
| CI-runnable | Script has proper imports, assertions, no hardcoded waits > 5s? 0/1 |
| Wall-clock time | Seconds from prompt to completed script |

**Score per task:** 0-5 (sum of binary metrics). **Score across tasks:** 0-25.

### Task 3 Gate Decision

| Total Score (0-25) | Verdict | Action |
|---|---|---|
| 0-7 (< 30%) | **DEFER** | Do not add to SKILL.md. Document what failed. Revisit when Webwright matures. |
| 8-14 (30-55%) | **ADD WITH CAVEATS** | Add to SKILL.md with heavy warnings. Frame as experimental. |
| 15-19 (60-75%) | **ADD** | Full routing table entry with documented limitations. |
| 20-25 (80%+) | **ADD + HIGHLIGHT** | Routing table entry + recommend as preferred for script generation. |

This is a single gate, not two competing benchmarks. The threshold is intentionally generous (30% = add with caveats) because the value proposition is novel capability, not replacement of existing tools.

### Task 4: Eval Fixture Compatibility (Informational, not gated)

Feed 2 existing eval fixtures (one HAS-BUGS, one CLEAN) to Webwright as prose prompts:
- HAS-BUGS: `accordion-no-region-role` — "Test this accordion for accessibility. The code has buttons with aria-expanded but the expanded panels lack role='region' and aria-labelledby. Generate a Playwright test that catches these issues."
- CLEAN: `button-skip-link-clean` — "Test this skip link implementation for accessibility. Generate a Playwright test that verifies it works correctly."

**Grade:** Does the HAS-BUGS script detect the planted issues? Does the CLEAN script avoid false alarms? Results inform caveats in Phase 2, not the gate decision.

### Task 5: ARIA Snapshot Capability (Informational, not gated)

Webwright's Playwright environment has `page.locator("body").aria_snapshot()` — the full accessibility tree.

**Prompt:** "Navigate to the APG Tabs example. Capture the ARIA snapshot. Identify all roles, states, and relationships."

**Compare:** Run `agent-browser snapshot -i` on the same page. Is Webwright's `aria_snapshot()` output richer for structural analysis? Results determine whether the SKILL.md mentions this as a differentiator, not a separate routing row.

### Optional: Build `score_webwright.py`

If time permits, create a deterministic scorer (mirroring `ollama/score_output.py`) that checks generated `.py` files via regex/AST:

1. Contains `page.keyboard.press(` or `locator.press(` (not `dispatchEvent`)? 0/1
2. Contains `get_attribute("aria-` before keyboard action? 0/1
3. Contains `get_attribute("aria-` after keyboard action? 0/1
4. Contains assertion comparing before/after? 0/1
5. Uses `await` correctly (async pattern)? 0/1
6. Proper imports (`from playwright.async_api import` or `from playwright.sync_api import`)? 0/1
7. No `time.sleep()` > 5 seconds? 0/1
8. Matches expected key sequence for widget type? 0/1

Score: 0-8 per script. Enables repeatable scoring on future Webwright versions without manual review.

---

## Phase 2: SKILL.md Modifications (conditional on Phase 1 gate)

**Duration:** ~30 minutes. **Depends on:** Phase 1 gate passes (score >= 8/25).

### Task 6: Update Routing Table

Replace current 4-row table (SKILL.md lines 16-22) with a 5-row table. **One** Webwright row, not two:

```
| Task | Tool | Why |
|---|---|---|
| Codified CI keyboard tests, visual regression, axe-core scans, WCAG compliance suites | `npx playwright test` with `.spec.js` files | Real keyboard events, CI-runnable, version-controlled. Primary path. |
| Interactive agent-driven recon: snapshot ARIA structure, navigate SPA, verify fix, capture screenshots | `agent-browser` CLI | One shell call per action, CDP keyboard events verified. Best for exploratory work. |
| Generate a test script from a prose spec ("test that this modal traps focus and Escape closes it") | `/webwright:run` or `/webwright:craft` (Claude Code plugin) | LLM generates complete Python Playwright script. Review before trusting. Also captures `aria_snapshot()` for deep ARIA tree inspection. |
| Visual inspection, DOM queries from a conversational session | `agent-browser screenshot` / `snapshot` | Same daemon, no test runner needed. |
| Anything requiring Playwright MCP keyboard events | **DO NOT USE Playwright MCP.** | browser_press_key silently dropped. |
```

Add decision flowchart after the table:

```
Do you have a prose description of what to test, but no test script yet?
  YES → /webwright:run (one-shot) or /webwright:craft (reusable parameterized tool)
  NO, you need to run an existing test → npx playwright test
  NO, you need to explore interactively → agent-browser
```

### Task 7: Add "Test Script Generation with Webwright" Section

New section after "Interactive reconnaissance with agent-browser." Contents:

- **When to use:** Prose a11y requirement → runnable test script, without hand-writing it
- **What it produces:** Python Playwright script with navigation, interactions, assertions, screenshots
- **Language mismatch warning:** Webwright generates Python. Existing CI is Node.js/.spec.js. Generated scripts are starting points — for CI, port logic to .spec.js using APG templates, or run Python directly if a Python test runner is available.
- **Example `/webwright:run`** using actual WAI-ARIA APG URL (not example.com):
  ```
  /webwright:run Navigate to https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/dialog/.
  Open the modal by clicking the trigger button.
  Verify focus moves into the modal.
  Tab through all focusable elements and verify focus wraps (focus trap).
  Press Escape and verify the modal closes and focus returns to the trigger.
  ```
- **Quality gate:** The human operator must review generated scripts before trusting results. Check that keyboard events use `page.keyboard.press()` or `locator.press()`, NOT synthetic `dispatchEvent`. Check that assertions verify state changes, not just attribute presence.
- **Limitations:** No built-in axe-core (LLM must write injection code). May miss a11y-specific patterns unless prompt is specific. Python scripts don't run in JS CI without a Python runner. Requires CC plugin install. Not available in Codex CLI.
- **ARIA snapshot note** (if Task 5 confirms): "Webwright's Playwright environment captures `aria_snapshot()` — the full accessibility tree with roles, states, and relationships. Richer than `agent-browser snapshot -i` for structural analysis."

### Task 8: Add Installation Instructions

- Prerequisites: Python 3.10+, Playwright Python, Chromium
- Two-step install: `/plugin marketplace add microsoft/Webwright` then `/plugin install webwright@webwright`
- Fallback: local clone if marketplace unavailable
- Platform note: CC-only. Not available in Codex CLI. agent-browser remains the only browser automation usable from Codex.

### Task 9: Update Lifecycle Note

Current lifecycle (SKILL.md "Lifecycle integration" section):
```
plan → critique plan → revise → implement → test (this skill) → critique implementation → fix → re-test
```

Add: "Webwright script generation fits between 'plan' and 'test' — use it to generate test scripts from the planner's output before running them. Generated scripts are inputs to the test phase, not a replacement for it."

---

## Phase 3: Workflow Documentation (conditional on Phase 2)

**Duration:** ~15 minutes.

### Task 10: Update a11y-workflow Team Definition

Add optional step in `.claude/teams/a11y-workflow.md` between Plan and Test:
- **Script Generation (optional):** When the planner's output includes specific test scenarios without existing .spec.js coverage, use `/webwright:craft` to generate reusable scripts or `/webwright:run` for one-off verification
- **Review gate:** Generated scripts must be reviewed (by the human operator) before being treated as test evidence

### Task 11: Update Project CLAUDE.md

Add Webwright to the "Browser Automation Tooling" section after agent-browser:
- Brief when-to-use summary
- Cross-reference to a11y-test SKILL.md for full routing table
- Note: CC-only, Codex CLI incompatible (but generated `.py` files can be executed from Codex via `python3 script.py`)

---

## Failure Modes and Rollback

| Failure | Detection | Rollback | Time |
|---|---|---|---|
| Plugin install fails | Immediate — Task 1 | Stop. No changes made. | 0 min |
| Keyboard events use synthetic API | Task 2 code inspection | Restrict to non-keyboard tasks or defer entirely | 5 min |
| 0/5 a11y tasks useful | Task 3 scoring | Defer integration. Document results. | 0 min |
| Routing table confusing | Post-deployment feedback | Move Webwright to appendix or remove row | 15 min |
| Webwright abandoned by Microsoft | Future — monitoring | Remove SKILL.md row + section | 5 min |
| Full rollback | Any cascade | `git revert` SKILL.md changes, uninstall plugin | 5 min |

**Benchmark artifacts** (`evals/suites/webwright-benchmark/`) stay regardless of outcome — they document what we learned and enable future re-evaluation.

---

## Proportionality Note

This is a single-developer project evaluating a speculative third tool. The benchmark scope (5 tasks, 1 rep each, qualitative scoring) is deliberately lean — enough to make an informed routing decision, not enough for publication. If Webwright proves valuable and the results are worth sharing externally (conference talk, blog post), expand to 10+ tasks with 3+ reps and formal statistical analysis at that time.

---

## Success Criteria

- [ ] Webwright plugin installs and runs (Task 1)
- [ ] Generated scripts use Playwright keyboard API, not synthetic events (Task 2)
- [ ] Benchmark score >= 8/25 (Task 3 gate)
- [ ] SKILL.md routing table updated — 5 rows, decision flowchart, no ambiguity (Task 6)
- [ ] New "Script Generation with Webwright" section with examples and quality gate (Task 7)
- [ ] Installation instructions with two-step install + Codex limitation (Task 8)
- [ ] Existing npx playwright test and agent-browser workflows unchanged (verified by diff)
- [ ] a11y-workflow team definition updated (Task 10)
- [ ] Project CLAUDE.md updated (Task 11)
