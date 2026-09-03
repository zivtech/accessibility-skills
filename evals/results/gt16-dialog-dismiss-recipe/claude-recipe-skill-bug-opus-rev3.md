<!-- GT-16 blind draw: condition=recipe-skill (a11y-test slice as procedure), fixture=dialog-dismiss-recipe (BUG), fixture revision 3 (18ba1e8), model=opus, agent=general-purpose, 2026-09-03. Verbatim; recovered from the agent's session transcript. Read only prompts/system-recipe-slice.md and prompts/dialog-dismiss-recipe.blind.md. -->

VERDICT: REVISE

The recorded outcome is not supported by its own evidence. The recipe's own `trace.json` shows the control under test being focused twice by Tab, while the filed finding says it was never reached. The FAIL is a test-authoring artifact, not a product defect.

---

### CRITICAL — The locator resolves to a control outside the dialog; the filed 2.1.1 FAIL is a false positive
`dialog-dismiss-recipe.blind.md:187`

`page.locator('button:has-text("Close")')` matches by rendered text. The dialog's close control has no text content — it is an `aria-label="Close dialog"` button wrapping an `aria-hidden` SVG (`:97`–`:101`), so `:has-text("Close")` cannot match it. The only button whose text contains "Close" is `.account__close` → "Close account" (`:34`–`:36`), which lives in `#app-root`, outside the dialog. The run's own call log confirms this: `locator resolved to <button type="button" class="account__close">Close account</button>` (`:228`, `:230`).

The trace refutes the finding directly: `focus_after: {"role":"button","name":"Close dialog"}` at step 2 (`:249`) and step 5 (`:252`). OP-CLOSE-REACH passed. `findings.json` (`:274`–`:285`) files a CRITICAL WCAG 2.1.1 FAIL against behavior the run proves working. On this evidence the correct record for OP-CLOSE-REACH is PASS, and the current entry must be withdrawn, not re-severitied.

One part of the record does hold: the `claim_boundary` at `:279` is correctly scoped to the operation, route, and viewport and explicitly disclaims a criterion-level verdict. That is the right shape — it is the outcome inside it that is wrong.

### CRITICAL — The assertion is unfalsifiable: its target sits inside an `inert` subtree
`dialog-dismiss-recipe.blind.md:197`

While `confirming` is truthy, `#app-root` carries `inert` (`:19`), which removes every descendant from the tab order and from programmatic focus. `.account__close` is a descendant. So `expect(close).toBeFocused()` could not have passed under any product behavior — correct, broken, or absent. A check with only one reachable outcome carries zero information about the system under test; it is not weak evidence, it is no evidence.

This is also why the miswiring produced no smell. A red test that can only ever be red looks exactly like a real defect. The recipe needs an assertion whose two outcomes are both physically reachable before it can be filed against anything.

### MAJOR — `findings.json` cites, as its supporting evidence, a trace that contradicts it
`dialog-dismiss-recipe.blind.md:282`

`"evidence": ["stdout", "trace.json#steps-1-6"]` — steps 1–6 are precisely the range in which "Close dialog" appears focused twice. The record therefore attaches its own refutation and files anyway.

The mechanism is stated at `:270`: the finding was "filed by the harness from the assertion failure." That is a detector result promoted straight to a CRITICAL WCAG verdict with no adjudication step. The governing rule is explicit — a detector result "means only 'no detection fired for this route, state, viewport, config, and version' — never a WCAG, Section 508, keyboard, or assistive-technology verdict" (`system-recipe-slice.md:17`), restated as "never promote scanner output straight to a WCAG or Section 508 verdict" (`system-recipe-slice.md:23`). The fix is not only the locator: the harness needs a gate that reconciles an assertion failure against the attached trace before a finding is written, or the same class of false CRITICAL recurs on the next miswired selector.

### MAJOR — OP-CLOSE-DISMISS never executed, and nothing records that it didn't
`dialog-dismiss-recipe.blind.md:199`

Playwright aborts the test body on the first failed `expect`. Lines `:200`–`:202` — the Enter press, `toBeHidden`, and focus-return-to-trigger — never ran. The Expected Behavior states the recipe is meant to prove *both* reach and dismiss-with-focus-return (`:291`), but the run output records only "1 failed" (`:240`) and `findings.json` contains a single entry about reach. Half the recipe's declared scope silently vanished from the ledger.

This is the contract's coverage-vocabulary rule: "never collapse `cantTell` / informational / skipped / blocked / untested into pass or fail — each stays a distinguishable, visible state" (`system-recipe-slice.md:23`), and an abort "is an *abort*, not a PASS/FAIL/BLOCKED outcome — record it as what it is" (`system-recipe-slice.md:19`). An unrun operation that leaves no trace is worse than a recorded BLOCKED, because a reader of `findings.json` cannot tell it was ever in scope. Split the two operations into separate tests (or use soft assertions) and emit an explicit `untested`/`aborted` state for whatever the abort skipped.

### MAJOR — The dismiss step activates `document.activeElement`, not the located control
`dialog-dismiss-recipe.blind.md:200`

`page.keyboard.press('Enter')` goes to the page, not to `close`. Nothing between the loop and that line pins focus to the close control; the recipe relies entirely on the loop's `reached` bookkeeping having exited at the right moment.

Trace the counterfactual. With the loop running to exhaustion, step 6 leaves focus on **Cancel** (`:253`). Had the reach assertion at `:197` been soft or absent, that Enter would have fired `onCancel` (`:107`), the dialog would have unmounted, and the `useEffect` cleanup would have returned focus to the trigger (`:62`) — so `toBeHidden` and `toBeFocused(trigger)` would both have **passed**, and OP-CLOSE-DISMISS would have been filed as verified for a control that was never touched. The reach failure is the only thing that prevented a false PASS here.

Fixing the locator makes this work by accident. Fix it on purpose: assert focus is on the intended control immediately before acting, per the State Verification Pattern's "record initial state → act → verify state actually changed" (`system-recipe-slice.md:54`–`:61`).

### MAJOR — Locator strategy diverges from the rest of the recipe and from the census
`dialog-dismiss-recipe.blind.md:187`

Every other locator in the file resolves by role and accessible name (`:178`, `:182`, `:184`). Line 187 alone drops to an unanchored, case-insensitive CSS text substring, and is not scoped to the dialog. Both correct handles were already sitting in the run artifacts: `screen-reader-census.json` gives the exact accessible name "Close dialog" and the exact selector `div.dialog > header > button` (`:263`).

`dialog.getByRole('button', { name: 'Close dialog' })` is correct, scoped, and matches what a screen-reader user actually addresses. Substring text locators re-bind silently as page copy changes, which is exactly the failure that occurred: a locator intended for one component quietly captured an unrelated one three sections up the page.

### MINOR — Escape and Cancel dismiss paths are untested
`dialog-dismiss-recipe.blind.md:290`

Expected Behavior names three dismiss paths — header close control, Escape, and Cancel. The recipe covers one. "Escape to dismiss: Open a modal/popup/sidebar, press Escape, verify it closed" is item 3 of the procedure's required keyboard tests (`system-recipe-slice.md:48`), and item 7 covers focus return after close (`system-recipe-slice.md:52`).

Rated MINOR rather than MAJOR because the finding's `claim_boundary` (`:279`) scopes the claim to OP-CLOSE-REACH only — this is an honest coverage gap, not an overclaim. But the file is titled a *dismiss* recipe, and the Escape handler at `:66`–`:70` is unexercised code on a path a keyboard user will reach first.

### MINOR — Fixed 250 ms sleep per iteration, waiting on nothing asynchronous
`dialog-dismiss-recipe.blind.md:194`

Six iterations of `waitForTimeout(250)` add 1.5 s of dead time. Nothing here is async: a native Tab moves focus synchronously, and at the wrap points the trap calls `first.focus()` / `last.focus()` synchronously inside the keydown handler (`:75`–`:81`). No React state transition occurs during Tab traversal, so the SPA guidance to allow 200–500 ms applies to "ARIA attributes that change via React state" (`system-recipe-slice.md:90`) — not to this loop. Use `expect.poll` or web-first retry instead.

### MINOR — One test carries two operations; the failure message misreports the blast radius
`dialog-dismiss-recipe.blind.md:175`

The test name covers reach *and* dismiss, while the only assertion message is scoped to reach (`:197`). The stdout headline (`:214`, `:216`) therefore reads as though the whole dialog-dismiss story failed, when a single operation's assertion tripped and the other never ran. One operation per test is what keeps the coverage ledger legible.

### ENHANCEMENT — No containment assertion / negative control
`dialog-dismiss-recipe.blind.md:192`

The trace makes focus containment directly observable (steps 1–6 never leave the dialog), but no assertion captures it, and nothing asserts that controls outside the dialog stay unreachable while it is open. An explicit "no focus target outside `div.dialog` is reachable" check would have failed loudly and immediately on the miswired locator — it would have flagged that the test was interrogating an inert element in the first run, instead of leaving that to a reader diffing the call log against the trace.

---

### Summary of required changes before this outcome can be filed

1. Retarget the locator to `dialog.getByRole('button', { name: 'Close dialog' })`.
2. Withdraw `kbd-dialog-close-reach`; on this evidence OP-CLOSE-REACH is a PASS.
3. Split OP-CLOSE-REACH and OP-CLOSE-DISMISS into separate tests, and record any unrun operation as `aborted`/`untested`, never as absent.
4. Assert focus is on the intended control immediately before pressing Enter.
5. Add a harness gate that reconciles an assertion failure against the attached trace before writing a finding — the locator bug is the instance, the missing gate is the class.

---

## Provenance

Files read (exactly two, both via the Read tool, complete):

1. `/Users/AlexUA_1/claude/accessibility-skills-gt16/evals/results/gt16-dialog-dismiss-recipe/prompts/system-recipe-slice.md` — treated as the operating procedure; cited by its own line numbers as `system-recipe-slice.md:<line>`.
2. `/Users/AlexUA_1/claude/accessibility-skills-gt16/evals/results/gt16-dialog-dismiss-recipe/prompts/dialog-dismiss-recipe.blind.md` — the fixture under review; all `filename.md:<line>` citations use this file's line numbers as they appear in the file as read.

No other file was opened. No grep, glob, find, git, shell command, web fetch, web search, directory listing, subagent, or skill invocation was used. All reasoning is from those two files plus working knowledge of React 18 effect/commit ordering, the HTML `inert` attribute, Playwright locator semantics (`:has-text` substring matching, strict mode, abort-on-first-failed-`expect`), and WCAG 2.2. Contrast and target-size checks on the CSS block (`:122`–`:162`) were computed by hand and produced no findings: `#1a4fd1` on `#fff` ≈ 6.8:1 (passes 1.4.11), `#fff` on `#b3261e` ≈ 6.6:1 (passes 1.4.3), and `.dialog__close` at 32×32 px passes 2.5.8.