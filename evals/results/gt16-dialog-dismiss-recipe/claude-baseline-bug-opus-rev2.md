<!-- GT-16 blind draw: condition=baseline (no skill slice), fixture=dialog-dismiss-recipe (BUG), fixture revision 2 (df05648), model=opus, agent=general-purpose, 2026-09-03. Verbatim; recovered from the agent's session transcript. Read only prompts/dialog-dismiss-recipe.blind.md. -->

VERDICT: REVISE

The recorded outcome is a false positive. The run's own `trace.json` shows the dialog close control receiving focus twice (`dialog-dismiss-recipe.blind.md:247`, `dialog-dismiss-recipe.blind.md:250`), while the assertion that filed the FAIL was never looking at that control at all. The correct outcome for OP-CLOSE-REACH on this evidence is PASS. The recipe must be fixed and re-run before any outcome is filed.

---

## CRITICAL

**C1 — The locator resolves to a different component, in an inert subtree, so the assertion can never pass.** `dialog-dismiss-recipe.blind.md:187`

`page.locator('button:has-text("Close")')` matches on rendered text content. The dialog's close control has no text — its accessible name comes from `aria-label="Close dialog"` on an SVG-only button (`dialog-dismiss-recipe.blind.md:97`–`dialog-dismiss-recipe.blind.md:98`). `:has-text()` is a case-insensitive substring match, so the only element it can match is the page-background **"Close account"** button (`dialog-dismiss-recipe.blind.md:34`) — which is exactly what the run log reports (`dialog-dismiss-recipe.blind.md:226`, `dialog-dismiss-recipe.blind.md:228`).

That element lives inside `#app-root`, which carries `inert` for the entire time the dialog is open (`dialog-dismiss-recipe.blind.md:19`). An inert element cannot receive focus. So `dialog-dismiss-recipe.blind.md:196` was guaranteed to fail on every run, for every possible component behavior. A test that cannot pass is not a measurement — it produces the same output whether the component is correct or broken, and therefore carries zero information about the component.

Only one element matched, so Playwright strict mode raised nothing. The failure was silent and looked like a real result.

Fix: `page.getByRole('button', { name: 'Close dialog' })`, scoped to the dialog (`dialog.getByRole(...)`) so a background match is structurally impossible, not merely unlikely.

**C2 — The filed finding is contradicted by evidence generated in the same run.** `dialog-dismiss-recipe.blind.md:272`–`dialog-dismiss-recipe.blind.md:283`

`trace.json` records focus landing on `{ "role": "button", "name": "Close dialog" }` at step 2 and again at step 5 (`dialog-dismiss-recipe.blind.md:247`, `dialog-dismiss-recipe.blind.md:250`). The tab cycle is Cancel → Delete → Close dialog → Cancel, wrapping correctly — which is exactly what the focus-trap code at `dialog-dismiss-recipe.blind.md:72`–`dialog-dismiss-recipe.blind.md:81` implements, given the close button is `items[0]` in DOM order (confirmed by the census at `dialog-dismiss-recipe.blind.md:261`). The close control is reachable by Tab in **two** presses from the dialog's initial focus.

Filing `"outcome": "FAIL"` on 2.1.1 here does not overstate a real problem — it reports a problem that does not exist. If this ships to a developer, they will investigate a working focus trap; if it ships to a client in a conformance report, it is a fabricated failure.

This is the dead-output pattern in its purest form: the harness derived a finding from an assertion string without anything — human or agent — reading the trace file sitting beside it. The pipeline is fluent and produced a well-shaped finding object. Nothing in it was true.

---

## MAJOR

**M1 — The `evidence` array cites the artifact that refutes the finding.** `dialog-dismiss-recipe.blind.md:280`

`"evidence": ["stdout", "trace.json#steps-1-6"]` names precisely the steps that show the close control focused. Evidence was attached by reference, never inspected. Any harness that can cite a trace can also read it; the missing step is a cross-check that the trace does not contradict the assertion before a finding is filed. Without that check, every future assertion bug becomes a filed WCAG failure with a citation that lends it false weight.

**M2 — The `selector` field records the broken test locator, not the failing element.** `dialog-dismiss-recipe.blind.md:278`

`"selector": "button:has-text(\"Close\")"` points a developer at `button.account__close` in the Account section (`dialog-dismiss-recipe.blind.md:34`) — a different component, in a different region, with no defect. The evidence contract's selector field is meant to identify the element that failed, and a test locator is not that. Even after C1 is fixed, this field should carry a selector resolved from the page (e.g. the census's `div.dialog > header > button`, `dialog-dismiss-recipe.blind.md:261`), not the query string the test happened to use.

**M3 — Severity is assigned from criterion weight, not user impact.** `dialog-dismiss-recipe.blind.md:276`

`"severity": "CRITICAL"` is unsupported even on the finding's own (false) premise. If the header close control were genuinely unreachable, the dialog would still be dismissible by **Escape** (`dialog-dismiss-recipe.blind.md:66`) and by **Cancel**, which holds initial focus (`dialog-dismiss-recipe.blind.md:59`, `dialog-dismiss-recipe.blind.md:107`). No keyboard user is trapped or blocked from completing or abandoning the task; they lose one of three redundant exits. That is not CRITICAL by impact under any calibration. Outcome and severity are independent axes — deriving "2.1.1 FAIL ⇒ CRITICAL" collapses them and makes severity a restatement of the rule rather than a statement about people.

**M4 — Two of the recipe's three stated claims are never exercised.** `dialog-dismiss-recipe.blind.md:198`–`dialog-dismiss-recipe.blind.md:200`, against `dialog-dismiss-recipe.blind.md:290`

The recipe is declared to prove (a) the close control is Tab-reachable, (b) Enter on it dismisses the dialog, and (c) focus returns to the trigger. The run aborts at `dialog-dismiss-recipe.blind.md:196`, so (b) and (c) never execute. This is independent of the false positive: even a run that reached them would only exercise the *close-button* dismissal path, while the return-focus behavior under test (`dialog-dismiss-recipe.blind.md:62`) is the subtlest thing in the component — a cleanup effect whose correctness depends on ordering against the parent commit that removes `inert` (`dialog-dismiss-recipe.blind.md:60`–`dialog-dismiss-recipe.blind.md:61`). That ordering claim is asserted in a code comment and verified nowhere. It is the one thing in this component genuinely worth a test, and the recipe never reaches it.

**M5 — The WCAG criterion is derived from a free-text assertion message with no validation.** `dialog-dismiss-recipe.blind.md:196` → `dialog-dismiss-recipe.blind.md:274`

`"wcag": "2.1.1"` was parsed out of the string `'2.1.1 Keyboard: the dialog close control must be reachable by Tab'`. Any assertion label a test author types becomes a criterion-level claim in a filed finding. A typo'd, stale, or mis-chosen SC propagates into machine-readable output that downstream consumers (bug reports, ACR drafts) treat as authoritative. The SC mapping needs to be declared and validated against the criterion catalog, not scraped from prose.

---

## MINOR

**N1 — Fixed 250 ms sleeps in the Tab loop.** `dialog-dismiss-recipe.blind.md:193` — `waitForTimeout` after each keypress adds 1.5 s of guaranteed wall-clock and is still not a correctness guarantee on a slower machine. Focus after a synchronous `Tab` needs no wait; where a wait is genuinely needed, poll the condition.

**N2 — Hand-rolled focus check duplicates the assertion and is weaker than it.** `dialog-dismiss-recipe.blind.md:194` — `el === document.activeElement` does not descend into shadow roots (`activeElement` returns the host), and the `reached` value is used only to break the loop, then discarded. `expect.poll` or a single `toBeFocused` with an adequate timeout expresses the same intent with better diagnostics.

**N3 — Arbitrary 500 ms assertion timeout.** `dialog-dismiss-recipe.blind.md:196` — reduced below the project default without stated justification. Here it shortened the wait on an element that could never focus; in a working recipe it becomes a flake source under CI load.

**N4 — `claim_boundary` scopes to a viewport the recipe never pins.** `dialog-dismiss-recipe.blind.md:277` — the boundary reads "on this route and viewport", but the spec sets no `test.use({ viewport })` and the run output records none. The boundary claims a scoping dimension that is not captured in evidence, so a re-run at a different size cannot be distinguished from this one. (Otherwise the boundary is correctly formed — operation-scoped and explicitly not a criterion-level verdict. It is the one part of the finding object that is right, and it does not rescue a false positive: correctly scoping a claim that is untrue only makes the untruth precise.)

**N5 — The recipe breaks its own locator convention exactly once.** `dialog-dismiss-recipe.blind.md:187` vs `dialog-dismiss-recipe.blind.md:178` and `dialog-dismiss-recipe.blind.md:182` — every other target is addressed by role and accessible name; only the control actually under test uses a CSS/text selector. That single deviation is the whole defect, and it is mechanically detectable. A lint rule forbidding raw `:has-text()` on interactive elements in keyboard recipes would have caught this before the run.

**N6 — The loop's sizing comment reasons about the wrong quantity.** `dialog-dismiss-recipe.blind.md:189` — "three focusable controls; six presses is two full cycles" is arithmetically right but starts from the wrong model: focus begins on Cancel (`dialog-dismiss-recipe.blind.md:184`), and the close button is `items[0]` in the trap's DOM-ordered list (`dialog-dismiss-recipe.blind.md:72`), so a correct locator reaches it in two presses. Reasoning in cycles rather than in the trap's actual order is how a bound like this gets mis-sized when the dialog grows a fourth control.

---

## ENHANCEMENT

**E1 — Escape and Cancel dismissal are untested.** `dialog-dismiss-recipe.blind.md:288` names three dismiss routes; the recipe covers one. The file is named `dialog-dismiss`, and Escape is the route a keyboard user reaches for first. Both are cheap to add and both exercise the same return-focus path as M4.

**E2 — The `inert` background is never asserted.** `dialog-dismiss-recipe.blind.md:19` is the mechanism preventing focus from escaping the dialog into the page behind it, and the trace already contains the data to prove it holds across a full cycle (`dialog-dismiss-recipe.blind.md:245`–`dialog-dismiss-recipe.blind.md:251`). Ironically, the run's own failure — the background button refusing focus — is positive evidence for this, currently discarded as noise.

**E3 — The BASE_URL guard's message does not match its check.** `dialog-dismiss-recipe.blind.md:171`–`dialog-dismiss-recipe.blind.md:173` rejects unset/malformed values with "Keyboard tests require a real site", but the regex accepts `http://localhost:3000`, which the run used (`dialog-dismiss-recipe.blind.md:209`). The guard is good practice — no synthetic fallback — but the message overstates what it enforces.

---

## Required before this outcome can be filed

1. Replace the locator at `dialog-dismiss-recipe.blind.md:187` with a dialog-scoped role+name query and re-run.
2. Withdraw the finding at `dialog-dismiss-recipe.blind.md:272`–`dialog-dismiss-recipe.blind.md:283`; record OP-CLOSE-REACH as PASS on the existing trace, or as a superseded false positive with the corrected run attached.
3. Add a harness gate: a finding whose `evidence` cites a trace must not be filed when that trace records focus on the named target. This run had the disproof in hand and filed anyway.

---

## Provenance

- **File read:** `/Users/AlexUA_1/claude/accessibility-skills-gt16/evals/results/gt16-dialog-dismiss-recipe/prompts/dialog-dismiss-recipe.blind.md` (297 lines, read in full via the Read tool, one call).
- **No other file was read.** No grep, glob, or directory listing. No git commands. No Bash. No web search or fetch. No subagents spawned. No skills invoked. No MCP or browser tools used.
- All line citations are to that file's own line numbers as returned by the single read.
- All reasoning about React effect ordering, Playwright `:has-text()` semantics, `inert` focus behavior, and WCAG 2.1.1 is from working knowledge, not from any consulted source. Where that knowledge is load-bearing, it is flagged in place: the `useEffect` cleanup/commit-ordering claim at `dialog-dismiss-recipe.blind.md:60`–`dialog-dismiss-recipe.blind.md:62` is plausible as written but unverified by this fixture's evidence, which is why M4 treats it as untested rather than as a defect.