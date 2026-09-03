<!-- GT-16 blind draw: condition=baseline (no skill slice), fixture=dialog-dismiss-recipe-clean (CLEAN), fixture revision 3 (18ba1e8), model=opus, agent=general-purpose, 2026-09-03. Verbatim; recovered from the agent's session transcript. Read only prompts/dialog-dismiss-recipe-clean.blind.md. -->

VERDICT: ACCEPT

The two PASS rows in `findings.json` are supported by the recipe's own evidence. The keystrokes the recipe issues, the trace, the census, and the assertion citations are mutually consistent, and both `claim_boundary` values are narrow enough that neither row overclaims. Every issue below is hardening, not a defect in the recorded outcome.

## What I verified before accepting

- **Trap arithmetic matches the trace.** DOM order inside the dialog is close → Cancel → Delete (`dialog-dismiss-recipe-clean.blind.md:97`, `:107`, `:110`), so `FOCUSABLE` yields `[close, Cancel, Delete]`. Initial focus is Cancel (`:59`). Tab 1 → Delete natively; Tab 2 → Delete is `last`, so the wrap fires `first.focus()` → close (`:78`–`:80`). That is exactly trace steps 1 and 2 (`:226`–`:227`), and it is exactly two presses, which is what the short-circuiting loop executes (`:194`). The 4-step trace contains no keystroke the recipe does not issue and omits none it does.
- **Focus return is real, not asserted-by-comment.** The cleanup's claim at `:60`–`:61` holds: removing `inert` from `#app-root` (`:19`) and unmounting the dialog (`:39`) are DOM mutations in the same commit, and a `useEffect` destroy function is a passive effect that runs after that mutation phase — so the trigger is focusable when `returnFocusRef.current?.focus()` runs (`:62`). `triggerRef` is a stable ref object, so the dep array (`:63`) does not re-fire the effect mid-life. Trace step 3 corroborates independently (`:228`).
- **Citations are accurate, which is where these fixtures usually break.** `assertion:tests/dialog-dismiss.spec.js:33` (`:257`) resolves to fixture `:199`, the reach assertion; `:37-38` (`:267`) resolves to fixture `:203`–`:204`, the two dismiss assertions; and the runner's `dialog-dismiss.spec.js:9:1` (`:216`) matches `test(` at fixture `:175`. All three are correct against the code block's own numbering.
- **No fabricated values.** The locator name at `:189` traces to the census row at `:238` and to `aria-label` at `:97`. The census's concrete report title "Q3 spend by region" (`:239`) is never asserted — the recipe uses the title-independent `p:has-text("cannot be undone")` (`:185`), so no run-specific datum leaks into a claim.
- **Real keyboard events, hard failure without a site.** `page.keyboard.press` throughout, and the `BASE_URL` guard throws at module load (`:170`–`:173`) rather than silently skipping.

## Issues

**MINOR — The press budget exceeds the cycle it documents, so the assertion alone cannot distinguish a correct cycle from a broken one.** The comment states three controls and "six presses is two full cycles" (`dialog-dismiss-recipe-clean.blind.md:193`), and the loop honors that budget (`:194`). A correct trap reaches every control within 3 presses. A trap that took 4–6 presses — a double-visit or an off-by-one wrap — would still exit the loop, still satisfy `:199`, and still be filed PASS. This specific PASS is rescued only because `trace.json` is complete and shows press 2 (`:227`). Bound the loop to the control count and assert the press index.

**MINOR — The finding's press-count claim is carried by the trace, not by any assertion.** `"close control focused on Tab press 2 of a 3-control cycle"` (`:256`) is true per `:227`, but nothing in the recipe records the iteration count (`:194`–`:198` discards `i`). If the trace emitter and the spec ever diverge, this message becomes unfalsifiable.

**MINOR — Two operations are coupled in one test, so a failure silently under-reports instead of filing a FAIL row.** One `test()` (`:175`) produces both findings. If OP-CLOSE-REACH fails at `:199`, execution stops and OP-CLOSE-DISMISS produces no row at all — the findings file shows a gap, not a FAIL. For a per-operation evidence contract, that is the wrong failure shape. Split per operation, or make the dismiss step independent of the reach outcome.

**MINOR — Both `claim_boundary` values scope the claim to a viewport that the evidence never records.** `:253` and `:263` say "on this route and viewport"; the run output (`:213`–`:219`) and Frameworks & Environment (`:277`–`:281`) name Chromium but no viewport size or Playwright project. The boundary names a dimension the evidence cannot support. Either capture the viewport in the run record or drop it from the boundary.

**MINOR — `selector` fields carry Playwright locator expressions, not the DOM selectors the census uses.** `:254` and `:265` are `getByRole(...)` strings; the census gives real DOM selectors, e.g. `div.dialog > header > button` (`:238`). There is no machine path from either finding to its census row, and a locator expression is not reproducible outside this runner. Carry the census selector and keep the locator as a separate field.

**MINOR — "Dismisses without deleting" is declared but never asserted.** `:274` states the close control "dismisses it without deleting". The recipe asserts only hidden + focus-returned (`:203`–`:204`). A close control mis-wired to `onConfirm` instead of `onCancel` (`:97`) would produce byte-identical evidence — dialog hidden, focus returned, `dialog_open_after: false`. The filed boundary (`:263`) correctly excludes deletion, so the row is not an overclaim; but the operation as written in Expected Behavior is not covered by any row.

**ENHANCEMENT — Fixed 250 ms sleep is the only focus-settle mechanism.** `:196` is a hard sleep inside the loop; Playwright discourages `waitForTimeout` in favor of a polled expectation. On a slower commit this is both the flake surface and most of the 1.6 s runtime (`:216`).

**ENHANCEMENT — Accessible-name matching is inconsistently exact.** `:189` uses `exact: true`; `:178` and `:186` do not, and `getByRole`'s `name` defaults to case-insensitive substring matching. No live collision exists in this DOM, but "Cancel" and "Delete report" are exactly the names most likely to acquire a substring sibling ("Cancel and keep", "Delete report permanently").

**ENHANCEMENT — The trigger is focused programmatically, so its own keyboard reachability is unproven.** `:179` calls `trigger.focus()` rather than Tab-navigating to it. Legitimate scoping, and the boundary confines the 2.1.1 claim to the dialog control — but the recipe's own precondition (a keyboard user can get to "Delete report") rests on no evidence, and the final assertion at `:204` inherits that.

**ENHANCEMENT — The recorded path is the expensive one; the cheap one is untested.** OP-CLOSE-REACH (`:191`) records forward Tab, which from initial focus on Cancel routes through the destructive "Delete" button before wrapping to close. Shift+Tab from Cancel reaches close in one native press (`:75` falls through, since Cancel is not `first`). A reachability operation should record the shortest path, and the one-press reverse path is the mitigation for making users pass "Delete" to reach dismiss.

**ENHANCEMENT — Escape dismissal is declared in scope and implemented, but no row covers it.** `:274` lists Escape as a dismiss mechanism and `:66`–`:70` implements it. No finding exists for it. Since the trap wraps Tab within the dialog (`:75`–`:81`), Escape is also the mechanism that keeps this out of 2.1.2 territory — the argument that the trap is permissible currently rests on unmeasured code.

**ENHANCEMENT — The census is dialog-subtree only, so `inert` background exclusion is unsubstantiated.** `:232` scopes the census to the dialog subtree. `inert` (`:19`) plus `aria-modal="true"` (`:89`) is the modal-isolation mechanism, and nothing here measures it. Fine while no isolation row is filed; capture a page-scope census before any 1.3.2/4.1.2 modal claim is made.

**ENHANCEMENT — Focus lands on the close control, but nothing shows it is visible there.** `.dialog__close` is borderless and background-less (`:142`–`:148`), and the only indicator is `button:focus-visible` (`:154`–`:157`). Chromium should apply `:focus-visible` to the trap's programmatic `first.focus()` because the preceding interaction was keyboard, but "should" is the operative word and no 2.4.7/2.4.13 evidence is filed. Per this bundle's routing, focus-indicator sufficiency evidence comes from keyboard-a11y-tester, not from `toBeFocused`.

**ENHANCEMENT — One finding bundles two behaviors under one SC.** `kbd-dialog-close-dismiss-focus-return` (`:260`) covers both "Enter dismisses" (an operability behavior) and "focus returns" (`:261`, filed as 2.4.3). The two assertions at `:203` and `:204` fail independently; the rows should too.

**ENHANCEMENT — Component: an empty `reports` array makes the trigger a silent dead end.** `:23` sets `confirming` to `reports[0]`; if that is `undefined`, the guard at `:39` renders nothing and `inert` is never applied — the button activates with no dialog, no focus move, and no status message. Out of the recipe's scope and not part of the recorded outcome, but it is the operability hole nearest this control.

## Where my confidence drops

The React commit-ordering argument behind the focus-return claim (`:60`–`:62`) is reasoning about passive-effect scheduling, not measurement. I accept it here because trace step 3 (`:228`) is independent corroboration from the accessibility tree — but if that trace row were absent, I would have flagged the comment as an unverified claim rather than accepted it. Likewise, the `:focus-visible`-on-programmatic-focus behavior in the focus-indicator note is engine heuristic; I have not measured it and have rated the item accordingly.

## What I am not claiming

Not claiming either criterion conforms — both rows are correctly scoped to single operations on one route, and I have not widened them. Not claiming the dialog is accessible: no evidence here covers screen-reader announcement of the dialog's open/close, focus-indicator contrast, target size, reflow, or the confirm path. Not claiming the trap is complete against browser-chrome escape or shadow roots. Not claiming the component is correct outside the two traced operations — the empty-`reports` path and the delete path are unmeasured.

## Provenance

- **File read:** `/Users/AlexUA_1/claude/accessibility-skills-gt16/evals/results/gt16-dialog-dismiss-recipe/prompts/dialog-dismiss-recipe-clean.blind.md` (single `Read` call, full file, 282 lines).
- **No other file was read.** No `Grep`, `Glob`, `Bash`, or directory listing was run. No git history was consulted. No web search or fetch. No subagents were spawned. No other tool of any kind was invoked.
- All citations use the line numbers as they appear in that file. All reasoning is from the file's contents plus my own working knowledge of WCAG 2.2, the WAI-ARIA APG dialog pattern, React 18 commit/effect ordering, and Playwright locator and assertion semantics.