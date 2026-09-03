<!-- GT-16 blind draw: condition=recipe-skill (a11y-test slice as procedure), fixture=dialog-dismiss-recipe-clean (CLEAN), fixture revision 2 (df05648), model=opus, agent=general-purpose, 2026-09-03. Verbatim; recovered from the agent's session transcript. Read only prompts/system-recipe-slice.md and prompts/dialog-dismiss-recipe-clean.blind.md. -->

VERDICT: ACCEPT

The two PASS rows in `findings.json` are supported by the recipe's own evidence. Every load-bearing number, citation, and evidence class checks out.

## What I verified (and why it holds)

**Trace matches the component's actual focus mechanics.** DOM order inside the dialog is close → Cancel → Delete (`dialog-dismiss-recipe-clean.blind.md:97`, `:107`, `:110`). Mount focus goes to Cancel (`:59`), so Tab 1 → Delete, and Tab 2 hits the last element and the trap wraps to `items[0]` = the close control (`:78-81`). That is exactly `trace.json` steps 1–2 (`:224-225`). The finding's message "Tab press 2 of a 3-control cycle" (`:253`) is arithmetically correct, and `evidence: ["trace.json#step-2"]` (`:254`) points at the right step.

**Focus return is real, not asserted.** Step 3 records Enter on the close control with `focus_after: "Delete report"` and `dialog_open_after: false` (`:226`), which is what row 2 claims (`:263-264`).

**Line citations in `source` are accurate.** The spec block starts at `:167`, so fixture line − 166 = spec line. `:198` → spec 32 (matches `:255`); `:201-202` → spec 35–36 (matches `:265`); the stdout's `spec.js:9:1` (`:214`) → fixture `:175`, the `test(` call. The harness's self-references are internally consistent.

**Evidence class matches defect class** per the contract. Keyboard operability is proved by real `page.keyboard.press()` calls (`:180`, `:193`, `:200`), not attribute inspection; focus behavior is proved by a per-keystroke accessibility-tree trace (`:219-228`). No screenshot is offered as evidence for any interaction-class claim — the mismatch that would force a "partial" label does not occur here.

**Detector-lane boundary respected.** Both rows carry an explicit `claim_boundary` scoping to a named operation, route, and viewport and disclaiming a criterion-level verdict (`:251`, `:261`). The PASS is filed as "no detection fired for this configuration," not as WCAG conformance.

**Live-site guard present** in the required form (`:170-173`).

## Baits I checked and am *not* flagging

Stating these explicitly, because each is a plausible false positive:

- **`inert` under React 18.3** (`:19`) — passed as the string `''` (active) / `undefined` (removed), and the environment note confirms it renders as an attribute (`:278`). Not dropped.
- **React 16 `setTimeout(0)` focus-after-unmount rule** — does not apply. This is a passive `useEffect` cleanup (`:62`), which React runs after the commit that removes `inert` from `#app-root`, so the comment at `:60-61` is correct and the trigger is focusable when focus returns. The test also uses auto-retrying `toBeFocused()` (`:202`) rather than a bare `activeElement` read, so async settling is handled.
- **Playwright strict mode / substring name matching** — `getByRole('button', { name: 'Delete report' })` (`:178`) does not also match the dialog's "Delete" button; substring matching runs the other direction. All four locators resolve uniquely.
- **Cycle arithmetic** (`:191-197`) — 3 controls, 6-press cap = 2 full cycles; loop exits at press 2.
- **Close-button target size** — 32×32 CSS px (`:143-145`) clears SC 2.5.8's 24×24 AA floor; 44×44 is the AAA criterion.
- **Contrast** — `.danger` #b3261e on white ≈ 6.5:1; focus outline #1a4fd1 on white ≈ 6.8:1 at 3px with 2px offset (`:154-161`).

## Issues

**ENHANCEMENT — `dialog-dismiss-recipe-clean.blind.md:259`**: the row `kbd-dialog-close-dismiss-focus-return` carries a single SC (`2.4.3`) but its message (`:263`) asserts two behaviors — that Enter *dismissed* the dialog (a 2.1.1 operability claim) and that focus *returned* to the trigger (2.4.3). The row is operation-scoped with an explicit boundary, so nothing is overstated, but a reader mining `findings.json` by SC will not see the dismissal evidence under 2.1.1. Consider dual-citing or splitting the row. Does not affect the verdict.

**ENHANCEMENT — `dialog-dismiss-recipe-clean.blind.md:272`**: Expected Behavior names three dismissal routes (close control, Escape, Cancel); the recipe exercises one, and `:274` correctly declares that narrower scope. Nothing is collapsed into PASS and the untested routes are genuinely out of scope, so this is not a defect in what is filed — but `findings.json` alone gives no signal that two sibling routes exist and are unmeasured. A coverage note or sibling recipes would be needed before any route-level 2.1.1 statement about this dialog. Does not affect the verdict.

## Where my confidence drops

The commit-ordering claim in `:60-61` is the one place the fixture asks to be trusted on framework internals rather than shown. My reasoning (passive-effect cleanup runs after the mutation phase that strips `inert`) supports it and the trace's step 3 is consistent with it, but the trace cannot distinguish "correct by construction" from "correct by timing luck on this run." A single passing run is weaker evidence for that specific ordering than for anything else in the recipe. It does not change the verdict — the recorded outcome is about observed behavior on this route, and that is what the evidence shows.

## Provenance

Files read (exactly two, both via the Read tool):
1. `/Users/AlexUA_1/claude/accessibility-skills-gt16/evals/results/gt16-dialog-dismiss-recipe/prompts/system-recipe-slice.md`
2. `/Users/AlexUA_1/claude/accessibility-skills-gt16/evals/results/gt16-dialog-dismiss-recipe/prompts/dialog-dismiss-recipe-clean.blind.md`

No other file was opened. No grep, glob, git, bash, web fetch, web search, directory listing, or subagent was used. All line citations are the line numbers of file 2 as returned by that single read. Contrast and target-size figures were computed from the CSS in file 2 using working knowledge of the WCAG relative-luminance formula; no external lookup was performed.