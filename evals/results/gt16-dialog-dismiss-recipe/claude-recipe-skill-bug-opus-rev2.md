<!-- GT-16 blind draw: condition=recipe-skill (a11y-test slice as procedure), fixture=dialog-dismiss-recipe (BUG), fixture revision 2 (df05648), model=opus, agent=general-purpose, 2026-09-03. Verbatim; recovered from the agent's session transcript. Read only prompts/system-recipe-slice.md and prompts/dialog-dismiss-recipe.blind.md. -->

VERDICT: REVISE

The recorded outcome — a CRITICAL 2.1.1 FAIL in `findings.json` — is contradicted by the run's own trace evidence. The recipe never measured the control it claims to have measured. The defect is in the recipe and the filing, not in the component.

## Issues

**1. CRITICAL — The close-control locator resolves to a different button on a different part of the page.**
`dialog-dismiss-recipe.blind.md:187` uses `page.locator('button:has-text("Close")')`. The dialog's close control (`dialog-dismiss-recipe.blind.md:97`) carries no text content — its accessible name comes from `aria-label="Close dialog"` and its only child is an `aria-hidden` SVG — so `:has-text("Close")` cannot match it. The only text-bearing match on the page is the account section's **Close account** button (`dialog-dismiss-recipe.blind.md:34`). Playwright's own call log confirms the resolution: `locator resolved to <button type="button" class="account__close">Close account</button>` (`dialog-dismiss-recipe.blind.md:226`). Every assertion in the loop and at `dialog-dismiss-recipe.blind.md:196` was made against an element that is not under test.

**2. CRITICAL — The filed finding is refuted by the evidence it cites.**
`findings.json` records `"outcome": "FAIL"` (`dialog-dismiss-recipe.blind.md:275`) with the message "not focused after 6 Tab presses" (`dialog-dismiss-recipe.blind.md:279`), and lists `trace.json#steps-1-6` as supporting evidence (`dialog-dismiss-recipe.blind.md:280`). That trace shows the dialog close control focused twice inside those six presses — step 2 (`dialog-dismiss-recipe.blind.md:247`) and step 5 (`dialog-dismiss-recipe.blind.md:250`), both `{"role": "button", "name": "Close dialog"}`. The cited evidence establishes the opposite of the claim. Per the detector-lane authority boundary, a single assertion failure is a detection, not a verdict; here a second evidence lane was already in hand and disagreed, and the finding was filed anyway. This finding would ship a nonexistent keyboard blocker to a developer.

**3. MAJOR — A test-authoring fault emitted a canonical pass/fail result.**
The run is not a FAIL; it is an invalid measurement — the operation named in `claim_boundary` (`dialog-dismiss-recipe.blind.md:277`, "reach the dialog close control by Tab") was never exercised. Under the rule that an infrastructure fault is an abort rather than a PASS/FAIL/BLOCKED outcome, this must be recorded as invalid/environment-limited and held out of the pass/fail denominator until the locator is fixed and the run repeated. It currently sits in the denominator as a CRITICAL product defect (`dialog-dismiss-recipe.blind.md:276`).

**4. MAJOR — The assertion was unsatisfiable by construction, and nothing in the recipe noticed.**
`.account__close` lives inside `#app-root`, which carries `inert` for the entire time the dialog is open (`dialog-dismiss-recipe.blind.md:19`). An inert subtree is removed from the tab order, so the locator's target could never become `document.activeElement` — the six-iteration loop (`dialog-dismiss-recipe.blind.md:191`) and the 500ms timeout (`dialog-dismiss-recipe.blind.md:196`) were spent proving an impossibility. A recipe whose failure mode is indistinguishable from a guaranteed-false assertion cannot support a conformance outcome.

**5. MAJOR — Half the recipe's stated purpose has no result at all, recorded as nothing.**
`dialog-dismiss-recipe.blind.md:290` states the recipe must prove both reachability *and* that Enter on the close control dismisses the dialog and returns focus to the trigger. The dismissal and focus-return assertions (`dialog-dismiss-recipe.blind.md:198`–`dialog-dismiss-recipe.blind.md:200`) never executed — the run aborted at line 196. Those behaviors are neither passed, failed, nor marked untested; they are simply absent. Untested must remain a distinguishable, visible state, not a silence.

**6. MAJOR — Escape dismissal is named in the expected behavior and never tested.**
`dialog-dismiss-recipe.blind.md:288` lists the header close control, Escape, and Cancel as dismissal routes. The recipe presses Escape zero times, despite "Escape to dismiss" being an explicitly required keyboard test and despite the fixture being titled a *Keyboard Dismiss Recipe*. The component's Escape handler (`dialog-dismiss-recipe.blind.md:66`–`dialog-dismiss-recipe.blind.md:70`) is unexercised.

**7. MAJOR — The finding's `selector` field points at the wrong element.**
`dialog-dismiss-recipe.blind.md:278` files `button:has-text("Close")` as the selector. That is a Playwright engine string rather than a stable selector for the failing element, and it identifies `.account__close` — a control outside the dialog and outside the claim boundary. A developer following this report would inspect the account section and find nothing wrong. The census already supplies the correct, stable selector: `div.dialog > header > button` (`dialog-dismiss-recipe.blind.md:261`).

**8. MINOR — The finding's message is inherited from the author's intent string, not from observed behavior.**
The text at `dialog-dismiss-recipe.blind.md:279` is a near-verbatim lift of the assertion description supplied at `dialog-dismiss-recipe.blind.md:196`. The harness restated what the author *expected to prove* as what it *observed*. That provenance is why a wrong locator produced a confidently-worded product finding rather than a diagnostic.

**9. MINOR — The close locator is not scoped to the dialog.**
A `dialog` handle already exists at `dialog-dismiss-recipe.blind.md:182` and is used correctly for Cancel at `dialog-dismiss-recipe.blind.md:184`, but the control under test is looked up page-wide (`dialog-dismiss-recipe.blind.md:187`) on a page that demonstrably contains a second "Close…" button. Scoping alone would have turned this into a zero-match authoring error instead of a false product FAIL.

**10. MINOR — "Dismisses without deleting" is unasserted.**
`dialog-dismiss-recipe.blind.md:288` requires that the close control dismiss the dialog *without* deleting the report. The recipe checks only visibility and focus (`dialog-dismiss-recipe.blind.md:199`–`dialog-dismiss-recipe.blind.md:200`); nothing asserts the report survived. Cancel and Delete dismissal routes are likewise unexercised.

**11. ENHANCEMENT — Add a locator positive control before the Tab loop.**
Assert the intended target resolves exactly once inside the dialog (e.g. `await expect(dialog.getByRole('button', { name: 'Close dialog' })).toHaveCount(1)`) ahead of `dialog-dismiss-recipe.blind.md:191`. A mis-targeted locator then fails loudly as an authoring error and cannot be filed as a 2.1.1 defect.

**12. ENHANCEMENT — Bind the recipe's targets to the accessibility tree the evidence records.**
`screen-reader-census.json` names the control "Close dialog" (`dialog-dismiss-recipe.blind.md:261`). Locating by role plus that accessible name — scoped to `dialog` — keeps the recipe, the trace, and the census referring to the same node, which is what makes cross-lane contradiction detectable.

**13. ENHANCEMENT — Assert the trap cycle, not just reachability.**
The trace already documents a complete, correct cycle: Cancel → Delete → Close dialog → Cancel (`dialog-dismiss-recipe.blind.md:245`–`dialog-dismiss-recipe.blind.md:252`). Asserting the ordered cycle measures the focus trap itself, and would have surfaced immediately that the close control is reached on the second press.

## What this review does not claim

I am not claiming the component passes 2.1.1, and this evidence cannot support that claim either. The trace establishes only that the close control is reachable by Tab and that the trap cycles across three controls. Enter-activation of the close control, focus return to the trigger (`dialog-dismiss-recipe.blind.md:289`), Escape, Cancel, and Delete were never exercised — an absence of detection is not evidence of conformance. I found no keyboard defect in the component in the evidence supplied; the only defects in evidence are in the recipe and in the filing.

## Provenance

Files read (2, both in full):
1. `/Users/AlexUA_1/claude/accessibility-skills-gt16/evals/results/gt16-dialog-dismiss-recipe/prompts/system-recipe-slice.md` — the operating procedure (verification evidence contract, detector-lane authority boundary, keyboard test requirements).
2. `/Users/AlexUA_1/claude/accessibility-skills-gt16/evals/results/gt16-dialog-dismiss-recipe/prompts/dialog-dismiss-recipe.blind.md` — the fixture under review; all line citations above are that file's own line numbers as read.

No other file was opened. No grep, glob, git, shell command, web fetch, directory listing, subagent, or skill invocation was used. The review is reasoned from those two files and my own working knowledge of React, Playwright locator semantics, and `inert`.