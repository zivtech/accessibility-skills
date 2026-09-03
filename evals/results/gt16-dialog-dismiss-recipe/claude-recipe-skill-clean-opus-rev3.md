<!-- GT-16 blind draw: condition=recipe-skill (a11y-test slice as procedure), fixture=dialog-dismiss-recipe-clean (CLEAN), fixture revision 3 (18ba1e8), model=opus, agent=general-purpose, 2026-09-03. Verbatim; recovered from the agent's session transcript (first attempt died on API 529 with no output). Read only prompts/system-recipe-slice.md and prompts/dialog-dismiss-recipe-clean.blind.md. -->

VERDICT: ACCEPT

The two PASS rows in `findings.json` are supported by the recipe's own evidence, and their `claim_boundary` fields do not overreach what the run actually measured. No issues filed — no CRITICAL, MAJOR, MINOR, or ENHANCEMENT findings survived verification.

## What I checked, and why each candidate defect did not hold

**Real-keyboard requirement.** Every state change under test is driven by `page.keyboard.press` — Enter to open (`dialog-dismiss-recipe-clean.blind.md:180`), Tab to traverse (`:195`), Enter to dismiss (`:202`). No `dispatchEvent(new KeyboardEvent(...))` anywhere, and no assertion claims keyboard operability from ARIA-attribute inspection alone. The live-site guard at `:170–173` is present and matches the required form.

**The Tab-reach claim is arithmetically what the code does.** `FOCUSABLE` (`:10–11`) matched against the dialog subtree yields three controls in document order: the header close button (`:97`), Cancel (`:107`), Delete (`:110`). Initial focus is Cancel (`:59`). Tab 1 moves natively to Delete; on Tab 2, `document.activeElement === last` so the trap fires `first.focus()` (`:78–80`), landing on the close control. `trace.json` steps 1–2 (`:226–227`) record exactly that, and finding 1's message — "close control focused on Tab press 2 of a 3-control cycle" (`:255`) — is the true count, not a rounded one. The loop bound comment (`:192`) is also correct: six presses is two full cycles of three.

**The poll loop does not manufacture a pass.** `reached` (`:193–198`) only short-circuits the loop; the row is filed by the independent assertion at `:199`. Loop exhaustion still fails the test, so there is no path where a non-reachable close control yields PASS.

**Focus return on dismiss is real, not asserted-by-comment.** Enter on the close button reaches `onCancel` unimpeded — the dialog's `onKeyDown` returns early for any non-Escape, non-Tab key (`:71`). Unmount cleanup returns focus to the trigger (`:62`), and `trace.json` step 3 (`:228`) records `focus_after: "Delete report"` with `dialog_open_after: false`. The inert lifecycle comment at `:60–61` is accurate for a *passive* effect: `useEffect` destroy functions for an unmounted subtree flush after the commit that already removed `inert` from `#app-root` (`:19`), so the trigger is focusable when focus returns. Had this been `useLayoutEffect`, it would have been a real defect; it is not. This is the point where my confidence is lowest — it rests on React 18.3 passive-effect ordering (`:279`) rather than on an artifact — but the trace independently corroborates the outcome.

**Evidence type matches defect class.** Finding 1 (2.1.1, keyboard operability) is backed by a real-keyboard Playwright transcript. Finding 2 (2.4.3, focus return) is backed by a per-keystroke accessibility-tree focus trace, declared at `:281` as a contract-conforming trace artifact — the journey-level focus-trace lane, not a screenshot. No interaction-class claim is propped up by a visual artifact.

**Provenance is exact, not decorative.** Finding 1 cites `spec.js:33` (`:257`), which is the `toBeFocused` assertion at `:199`. Finding 2 cites `spec.js:37-38` (`:267`), which is `toBeHidden` + `toBeFocused` at `:203–204`. The stdout test location `spec.js:9:1` (`:216`) resolves to the `test(...)` declaration at `:175`. All three line references check out against the embedded file's own numbering.

**Census corroborates rather than contradicts.** The reading-order census (`:236–242`) matches JSX document order — close control before the description, Cancel then Delete in the footer — which is consistent with the trap wrapping from Delete back to close. No conflict between the SR census and the focus trace.

**Detector-lane discipline is observed.** Both rows scope themselves to a named operation on this route and viewport and explicitly disclaim criterion-level verdicts (`:253`, `:263`). Neither promotes a passing assertion to a WCAG conformance claim.

## Candidates I deliberately did not file

- **Escape and Cancel dismissal are untested** despite appearing in Expected Behavior (`:274`). This is not an issue against the recorded outcome: the recipe's stated scope (`:275`) is the close control only, and the `claim_boundary` fields already declare that negative space. Filing it would restate a boundary the artifact draws for itself.
- **`page.goto('${BASE_URL}/reports')` as a possible SPA 404.** The SPA-routing caution is conditional, and the run output (`:213–218`) shows the route resolved and the dialog opened. Flagging it would be speculation against evidence.
- **`inert=""` under React 18.3** emits a forward-compat console warning but still renders the attribute — which `:279` stipulates and step 3 of the trace demonstrates working.
- **Focus-indicator sufficiency.** `button:focus-visible` (`:154–157`) yields roughly 6.8:1 for `#1a4fd1` against the white dialog surface, above the 3:1 non-text threshold, with no `overflow: hidden` ancestor to clip the 2px-offset outline. Nothing here is claimed as a finding either way.

## What these PASS rows do not license

They are not a verdict on 2.1.1 or 2.4.3 for the page, nor evidence that Escape or Cancel dismiss correctly, nor evidence for 2.1.2 (no keyboard trap), 4.1.3 announcements, focus-indicator sufficiency, or any non-default viewport. They cover two named operations on one route at one viewport, in one run.

## Provenance

Files read (2, both in full, via the Read tool):
1. `/Users/AlexUA_1/claude/accessibility-skills-gt16/evals/results/gt16-dialog-dismiss-recipe/prompts/system-recipe-slice.md`
2. `/Users/AlexUA_1/claude/accessibility-skills-gt16/evals/results/gt16-dialog-dismiss-recipe/prompts/dialog-dismiss-recipe-clean.blind.md`

No other file was opened. No grep, glob, git, directory listing, shell command, web fetch, web search, browser tool, or subagent was used. All line citations are into file 2 using its own numbering as read; contract references are to file 1. Reasoning is from those two files plus my own working knowledge of Playwright, React effect ordering, and WCAG.