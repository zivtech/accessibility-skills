<!-- GT-16 blind draw: condition=baseline (no skill slice), fixture=dialog-dismiss-recipe-clean (CLEAN), fixture revision 2 (df05648), model=opus, agent=general-purpose, 2026-09-03. Verbatim; recovered from the agent's session transcript. Read only prompts/dialog-dismiss-recipe-clean.blind.md. -->

VERDICT: ACCEPT

The two PASS rows in `findings.json` are supported by the artifacts filed alongside them. Nothing rises to CRITICAL or MAJOR.

## Why the outcome stands

I checked the places this kind of recipe usually breaks, and each one holds:

- **Source line provenance.** The spec block starts at `dialog-dismiss-recipe-clean.blind.md:167`, so spec line *n* = fixture line *166+n*. `assertion:…spec.js:32` (`dialog-dismiss-recipe-clean.blind.md:198`) is exactly the `toBeFocused` reachability assertion; `assertion:…spec.js:35-36` (`dialog-dismiss-recipe-clean.blind.md:201`–`202`) is exactly the `toBeHidden` + trigger-`toBeFocused` pair. The runner's own `spec.js:9:1` (`dialog-dismiss-recipe-clean.blind.md:214`) maps to the `test(` call at `dialog-dismiss-recipe-clean.blind.md:175`. All three agree.
- **Tab arithmetic.** `FOCUSABLE` in DOM order is Close → Cancel → Delete, so `items[0]` is the close control and `items[items.length - 1]` is Delete (`dialog-dismiss-recipe-clean.blind.md:72`–`74`). From the Cancel initial focus, Tab 1 → Delete (natural), Tab 2 → wrap to Close via `first.focus()`. Trace steps 1 and 2 (`dialog-dismiss-recipe-clean.blind.md:224`–`225`) record precisely that, and the message "Tab press 2 of a 3-control cycle" (`dialog-dismiss-recipe-clean.blind.md:254`) is arithmetically correct.
- **Loop/trace consistency.** The early-exit loop should produce exactly two Tab keystrokes. The trace contains exactly two. A trace padded to six presses would have contradicted the recipe; it doesn't.
- **Focus return.** `useEffect` cleanup fires in the passive phase, after the mutation phase has already dropped `inert` from `#app-root`, so the trigger is focusable when `returnFocusRef.current.focus()` runs — the comment at `dialog-dismiss-recipe-clean.blind.md:60`–`61` is accurate, the dep array `[returnFocusRef]` is a stable ref so the effect neither re-fires nor re-steals focus, and trace step 3 (`dialog-dismiss-recipe-clean.blind.md:226`) corroborates it empirically rather than by assertion alone.
- **`toBeHidden` is not a vacuous pass here.** It could be, on a locator that never resolved — but `toBeVisible` at `dialog-dismiss-recipe-clean.blind.md:183` establishes existence first, so the visible→hidden sequence carries real information.
- **`inert={confirming ? '' : undefined}`** (`dialog-dismiss-recipe-clean.blind.md:19`) is the correct React 18 idiom, not the `inert={false}` footgun that would render a truthy `inert="false"`.
- **Name provenance.** `aria-label="Close dialog"` with an `aria-hidden` SVG yields the accessible name used by the locator (`dialog-dismiss-recipe-clean.blind.md:189`), and it matches census row `dialog-dismiss-recipe-clean.blind.md:236`.
- **Boundaries are honest.** Both rows say "not a criterion-level verdict" and name the operation, so the PASSes are not overclaimed into 2.1.1/2.4.3 conformance.

## Issues

**1. MINOR — the claim boundary scopes to a viewport that no artifact records.**
`dialog-dismiss-recipe-clean.blind.md:251` and `dialog-dismiss-recipe-clean.blind.md:261` both bound the claim to "this route and viewport," but neither findings row carries a route/URL or viewport field, and the spec never sets a viewport — it inherits the Playwright config default, which appears nowhere in the fixture. The route is at least recoverable from `dialog-dismiss-recipe-clean.blind.md:176` and the stdout command line; the viewport is not recoverable at all. A boundary that names a parameter the evidence doesn't record can't be re-verified on its own terms. Fix by emitting the resolved viewport (and route) into the findings rows, not by loosening the boundary text.

**2. MINOR — hard-coded 250 ms sleep inside the Tab loop.**
`dialog-dismiss-recipe-clean.blind.md:195` sleeps a fixed 250 ms after every Tab. It buys nothing here — the loop re-polls and `toBeFocused` auto-retries — but as a reusable recipe it would let a component whose focus move arrives late still pass, while a keyboard user perceives the lag. Drop the sleep and let the retrying assertion carry the wait.

**3. ENHANCEMENT — dismiss routes named in Expected Behavior are untested, and no assertion proves close-dismiss doesn't delete.**
`dialog-dismiss-recipe-clean.blind.md:272` states that the close control, Escape, and Cancel all dismiss *without deleting*. The recipe exercises only the close control, and even there asserts only "hidden + focus returned" — never that `onDelete` was not called. This is correctly excluded by the claim boundary at `dialog-dismiss-recipe-clean.blind.md:261`, so it does not undermine the filed outcome; it is a coverage note for the next recipe in this operation set.

**4. ENHANCEMENT — the trigger is focused programmatically, so trigger reachability is assumed, not measured.**
`dialog-dismiss-recipe-clean.blind.md:179` calls `trigger.focus()` rather than tabbing to it. The 2.4.3 row therefore proves focus *lands on* the trigger, not that a keyboard user can reach it in the first place. Again correctly boundaried, but worth stating so the row isn't later read as a full open-and-return keyboard proof.

**5. ENHANCEMENT — silent no-op when the report list is empty (outside the recorded outcome).**
`dialog-dismiss-recipe-clean.blind.md:23` sets `confirming` to `reports[0]`. With an empty list that is `undefined`, so the dialog never opens and the activated control produces no perceptible result and no status message. Unrelated to the two filed rows; noted because the component was in scope for review.

## Provenance

- **File read:** `/Users/AlexUA_1/claude/accessibility-skills-gt16/evals/results/gt16-dialog-dismiss-recipe/prompts/dialog-dismiss-recipe-clean.blind.md` (single `Read` call, whole file).
- **No other file was opened.** No grep, no glob, no directory listing, no git commands, no shell/Bash, no web search or fetch, no subagents, no skills invoked.
- All line citations are that file's own line numbers as returned by the read. The spec-line ↔ fixture-line mapping used in the provenance check was derived arithmetically from the code fence position within the same file, not from any external copy of the spec.
- Contrast, target-size, React commit-phase ordering, and Playwright locator/matcher semantics were reasoned from working knowledge; no documentation was consulted. My confidence is highest on the trace/assertion/line-number consistency checks (fully verifiable in-file) and lower on the React passive-effect ordering claim — though trace step 3 corroborates that one empirically, so the verdict does not rest on my reading of React internals.