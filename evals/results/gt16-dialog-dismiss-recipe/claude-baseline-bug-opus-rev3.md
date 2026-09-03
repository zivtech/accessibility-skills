<!-- GT-16 blind draw: condition=baseline (no skill slice), fixture=dialog-dismiss-recipe (BUG), fixture revision 3 (18ba1e8), model=opus, agent=general-purpose, 2026-09-03. Verbatim; recovered from the agent's session transcript (first attempt died on API 529 with no output). Read only prompts/dialog-dismiss-recipe.blind.md. -->

VERDICT: REVISE

The recorded outcome is refuted by the fixture's own evidence. `trace.json` shows the dialog close control receiving focus twice during the same six Tab presses the finding claims never reached it. The FAIL is an artifact of a locator that resolves to a different button on a different part of the page.

---

## CRITICAL

**1. The locator under test resolves to the wrong element; the recorded FAIL is a false positive.**
`dialog-dismiss-recipe.blind.md:187` declares the control under test as `page.locator('button:has-text("Close")')`, unscoped to the dialog. `has-text` matches rendered text content. The dialog's close control (`dialog-dismiss-recipe.blind.md:97`) has *no* text content — its accessible name comes from `aria-label="Close dialog"` and its only child is an `aria-hidden` SVG (`dialog-dismiss-recipe.blind.md:98`). It is therefore unmatchable by `has-text` under any circumstances. The only element on the page whose text contains "Close" is the account section's button (`dialog-dismiss-recipe.blind.md:34`), and the run output confirms exactly that resolution twice: `dialog-dismiss-recipe.blind.md:228` and `dialog-dismiss-recipe.blind.md:230` both log `locator resolved to <button type="button" class="account__close">Close account</button>`.

The contradicting evidence is in the fixture: `dialog-dismiss-recipe.blind.md:249` (step 2) and `dialog-dismiss-recipe.blind.md:252` (step 5) record `focus_after: { "role": "button", "name": "Close dialog" }`. The control was reached on the second Tab press and again on the fifth. Because only one element matched, Playwright strict mode raised nothing — the recipe failed silently against the wrong target.

Corrected record: OP-CLOSE-REACH is **PASS** on this evidence (close control reached in 2 Tab presses from the initial Cancel focus), and OP-CLOSE-DISMISS is **UNTESTED** (see MAJOR 3).

**2. `findings.json` files a conformance FAIL whose own cited evidence refutes it.**
The finding at `dialog-dismiss-recipe.blind.md:281` asserts "not focused after 6 Tab presses" and at `dialog-dismiss-recipe.blind.md:282` cites `trace.json#steps-1-6` as its support. Steps 1–6 are precisely the range in which "Close dialog" appears twice. The harness filed a 2.1.1 FAIL against evidence that shows conformance. Per the header note at `dialog-dismiss-recipe.blind.md:270`, findings are derived from the assertion failure alone — nothing in the pipeline reconciles the assertion outcome against the per-keystroke trace it collected in the same run. A shipped 2.1.1 FAIL that its own attached evidence disproves is the most damaging class of output this harness can produce: it burns developer trust and, filed against a real product, sends someone to "fix" a control that already works.

---

## MAJOR

**3. OP-CLOSE-DISMISS was never executed, and no untested record was filed.**
Execution aborts at `dialog-dismiss-recipe.blind.md:197`; the dismissal assertions at `dialog-dismiss-recipe.blind.md:200`–`dialog-dismiss-recipe.blind.md:202` never ran. `Expected Behavior` (`dialog-dismiss-recipe.blind.md:291`) states the recipe is meant to prove both operations, but `findings.json` (`dialog-dismiss-recipe.blind.md:273`–`dialog-dismiss-recipe.blind.md:285`) contains a single entry. A reader of this run sees one FAIL and infers the rest was measured. Unmeasured operations must be recorded as INCOMPLETE/untested, not omitted — otherwise absence of a finding reads as evidence of conformance.

**4. The assertion message hardcodes a WCAG SC, so every failure mode is laundered into a conformance claim.**
`dialog-dismiss-recipe.blind.md:197` attaches `'2.1.1 Keyboard: the dialog close control must be reachable by Tab'` as the assertion message, and `dialog-dismiss-recipe.blind.md:283` shows the finding sourced from `assertion:tests/dialog-dismiss.spec.js:31`. A typo'd selector, a routing change, a slow build, or a dead page all emit the same string and all become a filed 2.1.1 FAIL at CRITICAL. This is the mechanism that turned a broken locator into a conformance claim. The SC belongs to a verified defect, not to an assertion label.

**5. The test as written cannot pass — it is unfalsifiable, not merely wrong.**
`dialog-dismiss-recipe.blind.md:19` applies `inert` to `#app-root` whenever the dialog is open, and the matched element (`dialog-dismiss-recipe.blind.md:34`) lives inside that subtree. Inert content cannot receive focus, so the assertion at `dialog-dismiss-recipe.blind.md:197` is guaranteed red for as long as the dialog is open — consistent with the `Received: inactive` at `dialog-dismiss-recipe.blind.md:229`. A recipe with no reachable green path proves nothing about the component; the modal's correct inert handling is what pins it red.

**6. Severity CRITICAL is not supported even on the finding's own premise.**
`dialog-dismiss-recipe.blind.md:278` rates the finding CRITICAL. Had the close control genuinely been unreachable, `Expected Behavior` (`dialog-dismiss-recipe.blind.md:290`) documents two further keyboard dismissal paths — Escape (`dialog-dismiss-recipe.blind.md:66`) and Cancel (`dialog-dismiss-recipe.blind.md:107`), the latter holding focus on open per `dialog-dismiss-recipe.blind.md:247`. No keyboard user would be trapped or blocked. Severity must track user impact, not the weight of the cited rule.

---

## MINOR

**7. The finding's `selector` identifies an out-of-scope element.**
`dialog-dismiss-recipe.blind.md:280` records `button:has-text("Close")` — a locator expression, not an identifier for the element the finding is about, and one that resolves to a control in a different section entirely. Anyone triaging from this field is sent to `.account__close`. Evidence fields must name the element actually evaluated.

**8. Fixed sleeps in the reach loop.**
`dialog-dismiss-recipe.blind.md:194` uses `waitForTimeout(250)` per iteration. Flake-prone under load and needlessly slow (1.5s of the 4.9s run at `dialog-dismiss-recipe.blind.md:214`). Prefer an assertion-based poll on focus.

**9. The `reached` probe throws instead of asserting on a zero-match locator.**
`dialog-dismiss-recipe.blind.md:195` calls `close.evaluate(...)`, which raises on no match. Had "Close account" not existed, the run would have died with a locator timeout still carrying the 2.1.1 message from `dialog-dismiss-recipe.blind.md:197`. Same laundering path, louder failure.

**10. Component: Escape becomes inoperable after a backdrop click.**
The Escape handler is bound to the dialog element (`dialog-dismiss-recipe.blind.md:93`, handler at `dialog-dismiss-recipe.blind.md:65`–`dialog-dismiss-recipe.blind.md:70`). The backdrop (`dialog-dismiss-recipe.blind.md:85`) is not focusable, so clicking it moves focus to `<body>`, from which keydown never reaches the dialog's handler. A mouse-then-keyboard user presses Escape and nothing happens; recovery requires a Tab press first. Not a blocker, but a real interaction gap the recipe does not cover.

---

## ENHANCEMENT

**11.** Replace `dialog-dismiss-recipe.blind.md:187` with a name-based, dialog-scoped locator — `dialog.getByRole('button', { name: 'Close dialog' })`. It targets the accessible name the control actually exposes, fails loudly on a name regression (which is itself the 4.1.2 defect worth catching), and cannot escape the dialog subtree.

**12.** Gate finding-filing at `dialog-dismiss-recipe.blind.md:270` on agreement with `trace.json`. Had the harness checked whether the asserted role/name pair appears in any `focus_after` entry before filing a reachability FAIL, this finding would have been blocked at source. The evidence was collected — nothing consumed it.

**13.** Extend coverage to the Escape and Cancel paths named at `dialog-dismiss-recipe.blind.md:290`, and add a focus-return assertion for each. The file is named `dialog-dismiss` but tests one of three documented dismissal routes.

---

## What I checked and found sound (negative space)

These are plausible-looking targets that hold up; I am not filing against them:

- **Focus trap arithmetic** — `dialog-dismiss-recipe.blind.md:72`–`dialog-dismiss-recipe.blind.md:81` correctly wraps three controls; the trace at `dialog-dismiss-recipe.blind.md:248`–`dialog-dismiss-recipe.blind.md:253` matches DOM order exactly (Close → Cancel → Delete cycling). The comment at `dialog-dismiss-recipe.blind.md:190` is arithmetically right.
- **Effect cleanup vs. `inert` removal** — the comment at `dialog-dismiss-recipe.blind.md:60` is accurate for React 18. `useEffect` cleanup for a deleted tree flushes in the passive phase, after the mutation phase has already removed the `inert` attribute from `dialog-dismiss-recipe.blind.md:19`. Focus does not return to an inert trigger. (This would be a real bug with `useLayoutEffect`.)
- **Contrast** — `.danger` (`dialog-dismiss-recipe.blind.md:158`) is ~6.5:1 white-on-#b3261e; the focus indicator (`dialog-dismiss-recipe.blind.md:154`) is ~6.8:1 against the white dialog, well over the 3:1 non-text threshold. Both pass AA.
- **Target size** — `.dialog__close` at 2rem × 2rem (`dialog-dismiss-recipe.blind.md:143`) is 32px, above the 2.5.8 minimum of 24px.
- **Run-output integrity** — the reported location `:9:1` (`dialog-dismiss-recipe.blind.md:214`), the excerpt line numbers 29/30/31/33 (`dialog-dismiss-recipe.blind.md:233`–`dialog-dismiss-recipe.blind.md:238`), and the `source` at `dialog-dismiss-recipe.blind.md:283` all map correctly onto the recipe as listed from `dialog-dismiss-recipe.blind.md:167`. The output is genuine, not fabricated — the defect is upstream of it.
- **`claim_boundary`** — `dialog-dismiss-recipe.blind.md:279` is correctly scoped to the operation, route, and viewport, and explicitly disclaims a criterion-level verdict. This field is well-formed; the problem is the outcome it bounds, not the bounding.
- **BASE_URL guard** — `dialog-dismiss-recipe.blind.md:170`–`dialog-dismiss-recipe.blind.md:173` correctly refuses to run keyboard tests against a non-URL target.

## Confidence

Highest on issues 1–4: the contradiction between `dialog-dismiss-recipe.blind.md:281` and `dialog-dismiss-recipe.blind.md:249`/`:252` is direct, and the resolution log at `dialog-dismiss-recipe.blind.md:228` names the wrong element outright. Lower on issue 10 (backdrop-click focus behavior is asserted from platform semantics, not from anything in this fixture's evidence — the recipe never clicks the backdrop) and on my reading of React 18 passive-cleanup ordering in the negative-space section, which is the one item here I would want re-verified against a live run rather than taken from the fixture's comment.

## Provenance

- **File read:** `/Users/AlexUA_1/claude/accessibility-skills-gt16/evals/results/gt16-dialog-dismiss-recipe/prompts/dialog-dismiss-recipe.blind.md` (one `Read` call, complete file, 298 lines).
- **Line citations** use that file's own line numbers as returned by the read.
- **No other file was opened.** No `grep`, no `git`, no directory listing, no web access, no subagents, no skills invoked, no other tool calls of any kind.
- All reasoning — React 18 commit-phase ordering, WCAG contrast math (computed by hand), Playwright locator and strict-mode semantics, `inert` focusability, ARIA name computation — comes from working knowledge, not from consulted sources.