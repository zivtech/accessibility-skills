# Accessibility Design Review — Modal Dialog Component

**VERDICT: ACCEPT**

**Overall Assessment**: This is a complete, correctly-implemented WAI-ARIA Modal Dialog. Every load-bearing promise of the pattern — dialog role and modal state exposed, accessible name wired to a real heading, focus moved into the dialog, focus cycled inside it, Escape dismissal, focus restored to the trigger — is present in the source and independently confirmed by the supplied driven keyboard/screen-reader trace. There are no CRITICAL and no MAJOR findings. What remains is a set of five MINOR robustness gaps that all live in the same place: the component's *enumeration* of what counts as a tabbable element and its *assumptions about a single instance with cooperative children*. The architecture is sound; the edges are not fully swept. For a one-off dialog, ship it. For a design-system component that will host arbitrary consumer content, fix MINOR-1 and MINOR-2 before it propagates.

**Line-number convention**: the fixture supplies inlined source, not real file paths. Citations use `Modal.jsx:NN` for lines counted from `import React` (= line 1) in the JSX block, and `modal.css:NN` for lines counted from `.modal-overlay {` (= line 1) in the CSS block.

---

## Phase 0 — Test Evidence Intake and Hygiene

**This review is a fresh design pass, not a fix verification**, so the a11y-test Verification evidence contract type-match check does not apply. No before/after remediation claim was made.

### Evidence that applies to this component (1 artifact)

`evals/results/keyboard-a11y-tester/driven/modal-complete-clean.trace.json` — keyboard-a11y-tester driven-live session, desktop 1280×800, personas `keyboard` + `screen-reader`, goal "open the settings modal, then close it, verifying focus management". Six steps. This is hard evidence at the same tier as a codified Playwright run, and I cite step ids and measured values below rather than reasoning about what the code "should" do.

### Evidence that does NOT apply — and must not be imported

The pack contains **28 `findings/*.json` files, none of which is for this page.** Every one carries a different `url` (`accordion-no-region-role.html`, `app-focus-order-illogical.html`, `async-form-vague-success.html`, `pagination-no-nav-landmark.html`, `tabs-incomplete-aria-selected.html`, and so on). Their contents — silent live regions, positive tabindex, heading skips, missing skip links, an unnamed tabpanel — are properties of **other fixture pages**. Attributing any of them to this modal would be fabrication, and I have imported none of them.

Three consequences worth stating plainly:

1. **There is no `deterministic-findings.json` for `modal-complete-clean.html` in this pack.** Absence of a findings artifact is *not* a zero-findings result. Compare `checkbox-group-no-fieldset.json`, which contains a genuine `"findings": []` — that is a measured clean result. This component has no such artifact, so I cannot and do not claim "the tool found nothing here." Every clean call below rests on the trace's per-step facts or on the source, not on tool silence.

2. **Calibration rule 4 (upstream keyboard-a11y-tester issue #27) is directly observable in this pack and is a reason not to trust the `conformance_level` field even if a findings file for this page had existed.** `heading-hierarchy-skipped.json` labels WCAG 1.3.1 as `conformance_level: "AA"` (1.3.1 is Level A). `tabs-incomplete-aria-selected.json` labels 4.1.2 as `"AA"` (Level A). `pagination-no-nav-landmark.json` labels 2.4.1 as `"AA"` (Level A). `app-focus-order-illogical.json` labels 2.4.3 as `"AA"` (Level A). Only the 2.4.13 rows emit `"AAA"`. That is exactly the documented pass/fail-gate-not-SC-level behavior; derive levels from the SC number.

3. **Calibration rule 1** — batch-crawl `sr-live-region-silent-desktop` rows (present on four sibling pages) are prompts to run a driven session, never failure evidence. Moot here, since none of them belong to this page, but noted so the exclusion is principled rather than convenient.

### What the trace measures — mapped to each protocol promise

| Promise | Measured evidence | Result |
|---|---|---|
| Dialog exposes role + modal state + name | `step_0002` `sr_announcement.new_phrases: ["dialog, Settings, modal", "button, Close dialog"]` | PASS |
| Focus moves into the dialog on open | `step_0002` Enter on trigger → `active_element_selector: body > div:nth-of-type(2) > div > div:nth-of-type(1) > button`, `ax_name_role_state.name: "Close dialog"`, `focus_moved: true` | PASS |
| Tab cycles forward inside the dialog | `step_0003` Close → Save changes; `step_0004` Save → **Close** (wrap at last element); `step_0005` Close → Save (second cycle) | PASS |
| Escape closes and restores focus to the trigger | `step_0006` Escape → `active_element_selector: #root > div > button`, name "Open settings", `focus_moved: true` | PASS |
| Focus indicator visible at every stop (2.4.7 AA) | `focus_visible.visible: true`, `style_cue: true`, `pixel_cue: true`, `indicator: "outline"` at all six steps | PASS |
| Focus indicator non-text contrast ≥ 3:1 (1.4.11 AA) | measured `focus_appearance.contrast`: 3.58 / 4.31 / 3.14 / 4.31 / 4.74 / 3.14 — all ≥ 3:1, `contrast_pass: true` at all six steps | PASS |
| Close button target size (2.5.8 AA) | `step_0002`/`step_0004` `bounding_box: 34.30 × 36` | PASS (≥ 24×24) |

**Where the trace is silent (evidence coverage gaps — these claims rest on code reading alone, and would be stronger measured):**

- **Shift+Tab is never sent.** The reverse wrap (`Modal.jsx:99–104`) is unverified. Given the forward wrap is proven and the code is symmetric, confidence is high, but it is design reasoning, not measured fact.
- **Backdrop click and the mousedown-drag guard are never exercised** (`Modal.jsx:120–134`). The pointer-cancellation analysis in MINOR-3 is mechanism reasoning with a manual repro attached, not a measurement.
- **The out-of-dialog focus recovery branch is never triggered** (`Modal.jsx:93–97`). This branch is the mitigation I rely on to downgrade MINOR-1 and MINOR-4; that downgrade is therefore one tier less certain than the findings themselves.
- **One viewport, one persona pair, one content shape.** No 200%/400% zoom pass, no forced-colors pass, no real-AT (NVDA/JAWS/VoiceOver) pass. The screen-reader persona here is an emulation; it is good evidence that the accessibility tree is right, and weak evidence about what any specific AT actually voices.

**No `A11y Evidence Finding` block is emitted.** The contract reserves it for CRITICAL/MAJOR findings backed by measured evidence; there are none, and inventing fields to make MINOR findings look instrumented is exactly what the contract prohibits.

---

## Phase 1 — Pre-commitment Predictions

Written from the modal-dialog prior before reading the source:

1. Focus trap absent, or present but with an incomplete tabbable-element set.
2. Focus does not restore to the trigger on close (or restores to `<body>`).
3. Backdrop is clickable but mouse-only — no keyboard equivalent for backdrop dismissal, or the backdrop is exposed to AT as a spurious control.
4. Missing one of `role="dialog"` / `aria-modal="true"` / an accessible name.
5. Escape handler bound to the dialog node, so it silently fails whenever focus is not inside the dialog.
6. Background content left reachable and hardcoded ARIA ids reused across instances.

**Outcome — where I was wrong, and where the surprise is:**

- **(2), (3), (4), (5) refuted outright.** Restoration is implemented and *measured* (`step_0006`). Backdrop dismissal is deliberately guarded and Escape is the documented keyboard equivalent. All three dialog attributes are present and the trace proves the resulting announcement. The Escape listener is on `document` (`Modal.jsx:67`), which is the robust choice, not the naive one.
- **(1) partially confirmed** — the trap exists, is recomputed on every Tab, and even recovers focus that has escaped the dialog. What is wrong is only the *set membership rules* (MINOR-1).
- **(6) confirmed on both halves** (MINOR-2, ENH-1).

The genuine surprise: this author anticipated two bugs that most hand-rolled modals ship with — (a) splitting the Escape effect from the focus-save/restore effect so an unstable `onClose` prop identity cannot re-run the focus lifecycle mid-interaction (`Modal.jsx:58–69` and its comment), and (b) the mousedown/click pairing so a text-selection drag released on the backdrop does not dismiss (`Modal.jsx:124–134`). Both are subtle, both are correct. The residual gaps are therefore *not* architectural — they are all failures to enumerate an edge case in an otherwise correct mechanism. That pattern is worth naming for the team: the design thinking here is well above the median; the list-keeping is not.

---

## Phase 2 — Semantic HTML Audit

**Clean.** Specifics verified rather than assumed:

- The only interactive control the component itself renders is a native `<button>` (`Modal.jsx:153–157`). No `div role="button"`. The native-HTML-first rule is satisfied for controls.
- The title is a real `<h2>` (`Modal.jsx:152`), not a styled div — the trace confirms it is exposed, `region.heading: "Settings"` at `step_0002`–`step_0005`. Level `h2` inside a dialog is appropriate; a dialog begins its own heading context, so this is not a 1.3.1 skip.
- `role="presentation"` on the overlay (`Modal.jsx:142`) is **correct, not a smell.** The overlay is a dimming scrim with a mouse convenience handler; the accessible alternative (Escape) exists and is implemented. The wrong "fix" here would be promoting the backdrop to a `<button>` — that would inject a second, redundant close control into the tab order and into the SR's control list. Presentation role does not strip the child dialog's role, and the overlay has neither focusability nor global ARIA attributes, so the role is honored rather than ignored. **See ENH-5** for the lint consequence.
- One structural note, non-finding: `role="dialog"` on a `<div>` where the platform now offers `<dialog>` + `showModal()`. This is *not* a native-HTML-first violation — the APG Modal Dialog pattern explicitly sanctions the ARIA construction, and this implementation follows it completely. It is raised as ENH-1 only because the native element would eliminate two of the five MINOR findings for free.

No tables, no lists, no form inputs, no landmarks are rendered by this component, so the layout-table, list-semantics, and label-association checks are not applicable. The trace's `region.landmark: null` at every step is a property of the harness page, not of the component under review.

---

## Phase 3 — ARIA Pattern Compliance Audit

**Pattern: WAI-ARIA APG Modal Dialog. Implementation is complete.** Checked against the pattern's required set rather than eyeballed:

| APG requirement | Source | Status |
|---|---|---|
| `role="dialog"` on the dialog container | `Modal.jsx:147` | Present |
| `aria-modal="true"` | `Modal.jsx:148` | Present, and voiced — `step_0002` announces "modal" |
| Accessible name via `aria-labelledby` (or `aria-label`) | `Modal.jsx:149` → `Modal.jsx:152` `id="modal-title"` | Present, reference resolves in-component; announced as "Settings" |
| Focus placed inside the dialog when opened | `Modal.jsx:38–42` | Present, measured `step_0002` |
| Tab and Shift+Tab confined to the dialog | `Modal.jsx:72–116` | Present; forward wrap measured `step_0004`, reverse wrap unmeasured |
| Escape closes the dialog | `Modal.jsx:58–69` | Present, measured `step_0006` |
| Focus returns to the invoking element | `Modal.jsx:47–51` | Present, measured `step_0006` |

ARIA *values* are valid: `aria-modal="true"` (boolean string, not "yes"), `aria-labelledby` a bare id token. No invented attributes, no `aria-*` on elements that cannot bear them.

Two things the pattern permits that this component does not do, both legitimately: no `aria-describedby` to a primary body message (optional in APG; the body is arbitrary consumer content, so the component cannot pick a describing node), and no `alertdialog` variant (correct — this is not an interruption).

Where the pattern is *claimed* more strongly than it is implemented: the fixture's own checklist asserts "Focus trap covers the full tabbable set … disabled and `tabindex="-1"` elements excluded." Both halves of that sentence are overstated. See MINOR-1 — this is a claim-versus-code discrepancy, not just a code gap, and it matters because the claim is what a downstream consumer will trust.

---

## Phase 4 — Focus Management Review

The strongest part of the component, and largely proven rather than argued.

**Verified correct:**

- **Save-then-restore is stored before focus moves** (`Modal.jsx:35`) and applied in the effect cleanup (`Modal.jsx:50`). Restoration is not wrapped in `setTimeout`, which the protocol flags as a React-unmount hazard — here it is measured working (`step_0006`), because the cleanup of a *passive* effect runs after the commit that removed the portal. The theoretical concern is refuted by measurement for the tested configuration. It is **not** refuted for the trigger-was-also-unmounted case; see MINOR-5.
- **Initial focus is deferred with `setTimeout(…, 0)`** (`Modal.jsx:38–42`) and guarded by `if (!modalRef.current) return` (`Modal.jsx:39`), so a stale timer from an open-and-immediately-close sequence cannot steal focus back after restoration. That guard is deliberate and correct.
- **The tabbable list is recomputed on every Tab** (`Modal.jsx:80`), not cached at open time — so children added, removed, or disabled while the dialog is open are handled. This is the failure mode of most hand-rolled traps, and it is handled.
- **The trap recovers focus that has landed outside the dialog** (`Modal.jsx:93–97`) rather than only wrapping at the ends. This is above-baseline and is the mitigation that keeps MINOR-1 and MINOR-4 from escalating.
- **Escape is bound at `document`** (`Modal.jsx:67`), so it fires regardless of where focus currently is — including the window between open and the deferred initial focus.
- **Tab order matches visual order**: DOM order Close (`dom_order_index: 20`) → Save (`23`); the trace shows exactly that sequence, and the close button is visually top-right of a header that precedes the body. No positive `tabindex` anywhere.
- **`display:none` children are excluded** from wrap-anchor candidacy via `getClientRects().length > 0` (`Modal.jsx:22–25`).

**Gaps** — MINOR-1 (set membership), MINOR-4 (listener phase), MINOR-5 (restore fallback), detailed below. SPA route changes, roving tabindex, duplicate mobile/desktop rendering, and deferred-focus-after-async-CRUD are not applicable to this component's surface.

---

## Phase 5 — State Communication Audit

The component has a small state surface, and all of it is communicated programmatically:

- **Open/closed** is communicated by *existence*: `if (!isOpen) return null` (`Modal.jsx:118`) unmounts the dialog entirely rather than hiding it with CSS. This is the right choice — it makes `aria-hidden`/`inert` on the dialog itself unnecessary and rules out the "hidden content still tabbable" trap.
- **Modal state** is exposed via `aria-modal` and is voiced (`step_0002`: "dialog, Settings, modal").
- **The close control's name is programmatic**, not visual: `aria-label="Close dialog"` (`Modal.jsx:156`) overrides the `✕` glyph in the name computation. Measured: `ax_name_role_state.name: "Close dialog"`, and the `✕` character appears nowhere in `new_phrases` at `step_0002` or `step_0004`. The protocol's rule about `×`/`+`/`>` symbols leaking as "times"/"plus" is satisfied in outcome; ENH-2 covers the defensive form.
- **No loading, error, success, disabled, selected, or busy state exists in this component**, so `aria-live`, `aria-busy`, `role="status"`, and `aria-describedby` error association have nothing to attach to. This is why importing the sibling pages' `sr-live-region-silent-desktop` findings would be doubly wrong: not only different URLs, but this component declares no live region at all.
- **`live_announcements: []` at every step is the expected result here**, not a defect. A dialog opening is announced by the focus/role change, not by a live region; adding one would double-announce.

No visual-only state indicators. No color-carried meaning. Nothing to report at CRITICAL or MAJOR.

---

## Findings

### Critical Findings (blocks access)

**None.** No user category is blocked. Keyboard users can open, traverse, dismiss, and return. Screen-reader users receive role, modal state, name, and the close control's purpose — all measured.

### Major Findings (significantly degrades experience)

**None.** I looked specifically for the four MAJOR-tier modal failures — trap absent, restoration absent, name absent, Escape absent — and all four are present and, for three of them, measured working.

### Minor Findings (friction, workaround exists)

---

**MINOR-1 — The tabbable-element enumeration is wrong in three specific ways, so a wrap anchor can be an element that Tab cannot reach.**

Evidence: `Modal.jsx:4–18` (the selector and its comment), `Modal.jsx:20–25` (the visibility filter), consumed at `Modal.jsx:86–87` where `firstElement`/`lastElement` become the wrap anchors.

- **(a) `tabindex="-1"` is excluded only from the generic clause.** `[tabindex]:not([tabindex="-1"])` (`Modal.jsx:17`) does that work, but `button:not([disabled])`, `a[href]`, `input:not(…)`, `select`, `textarea` (`Modal.jsx:8–13`) do not. A `<button tabindex="-1">` matches `button:not([disabled])` and enters the list. The comment at `Modal.jsx:4–6` states the opposite — "Excludes `tabindex="-1"`" — and the fixture's feature checklist repeats the claim. This is not hypothetical content: any roving-tabindex composite inside the dialog (a menu, listbox, toolbar, or tab list) renders its inactive items at `tabindex="-1"` by design, and a `<summary>`-style or programmatically-focusable heading is common.
- **(b) Genuinely tabbable elements are missing from the list.** `iframe`, `summary` (of a `<details>`), `object`, and `embed` are all Tab-reachable and none appears in `FOCUSABLE_SELECTOR` — while the rarer `audio[controls]`/`video[controls]` do. A dialog hosting a video embed, a payment iframe, or an FAQ disclosure computes its anchors wrongly.
- **(c) `visibility: hidden` survives the filter.** The comment at `Modal.jsx:22–23` is correct that `display:none` produces no client rects — but `visibility: hidden` elements *do* produce client rects and *cannot* take focus. The `opacity:0; visibility:hidden` reveal-on-hover pattern on card action buttons is exactly the case the protocol's gap list calls out, and it passes this filter.

All three produce the same failure: if the wrongly-included element is `lastElement`, then when the user Tabs from the genuinely-last control, `activeElement !== lastElement`, the handler does not `preventDefault`, and the browser advances focus past the un-tabbable anchor and out of the dialog. With `aria-modal="true"` set, the user lands on content their AT is being told does not exist. Symmetrically for Shift+Tab and `firstElement`.

- Confidence: **HIGH** on the mechanism (pure CSS-selector and focusability semantics); **MEDIUM** on frequency (depends entirely on consumer children — the demo content contains only two plain buttons, which is why the trace passes).
- User group: keyboard-only, screen reader.
- WCAG/APG: 2.1.2 No Keyboard Trap (inverse — the trap fails open), WAI-ARIA APG Modal Dialog ("Tab and Shift+Tab do not move focus outside the dialog").
- Why this matters: this is a reusable component. The defect is invisible until a consumer puts an iframe, a `<details>`, or any roving-tabindex widget in a dialog — and then it is invisible again because it looks like an ordinary Tab.
- **Fix**: apply the negative-tabindex exclusion to every clause (`button:not([disabled]):not([tabindex^="-"])`, and likewise for `a[href]`, `input`, `select`, `textarea`), add `iframe`, `object`, `embed`, and `details > summary:first-of-type` to the list, and extend the filter to reject computed `visibility: hidden`/`content-visibility: hidden` and elements matching `[inert], [inert] *`. Better: replace the hand-rolled selector with a maintained tabbable implementation, which exists precisely because this list is hard to keep right. Also correct the comment at `Modal.jsx:4–6` and the fixture checklist, which currently assert behavior the code does not have.
- **Mitigated by**: the out-of-dialog recovery branch at `Modal.jsx:93–97`. Once focus has escaped, the *next* Tab sees `!modalRef.current.contains(activeElement)` and pulls focus back to the boundary. So the realistic worst case is one disorienting stop followed by automatic recovery — not a permanent escape. That mitigation is why this is MINOR and not MAJOR. It is also itself unmeasured (see Phase 0 coverage gaps).

---

**MINOR-2 — `id="modal-title"` is a hardcoded constant in a component designed to be instantiated more than once.**

Evidence: `Modal.jsx:149` (`aria-labelledby="modal-title"`) and `Modal.jsx:152` (`<h2 id="modal-title">`).

Two simultaneously-open `Modal` instances put two `id="modal-title"` nodes in the document. `aria-labelledby` resolves against the *first* match in document order, so the second dialog is announced with the first dialog's name. The realistic shape of this is the confirm-on-close flow: a "Discard changes?" dialog opens over "Settings", and the screen-reader user is told they are in "Settings" while looking at a destructive confirmation. The same collision fires if the host application (or any other modal library, or a CMS template) already uses that id anywhere.

- Confidence: **HIGH** on the collision mechanism; **MEDIUM** on whether this codebase stacks dialogs.
- User group: screen reader (exclusively — sighted users see the correct heading).
- WCAG/APG: 4.1.2 Name, Role, Value; 1.3.1 Info and Relationships. APG Modal Dialog requires the dialog's accessible name to identify *that* dialog.
- **Fix**: one line — `const titleId = useId();` (React 18+) or a module-scoped counter, then `aria-labelledby={titleId}` / `id={titleId}`.
- **Mitigated by**: single-dialog-at-a-time usage, which is the common case and the only case the fixture's Expected Behavior claims. Escalates to MAJOR the moment the application stacks dialogs — and note that stacking is broken here for other reasons too (see What's Missing), so the id is the cheapest of several fixes needed before stacking is safe.

---

**MINOR-3 — The backdrop-dismissal guard is one-directional: a pointer-down on the backdrop that releases *inside* the dialog still closes it.**

Evidence: `Modal.jsx:120–134`. `handleOverlayMouseDown` records `e.target`; `handleOverlayClick` closes when `e.target === e.currentTarget && mouseDownTarget.current === e.currentTarget`.

The author's comment (`Modal.jsx:126–128`) shows the model: guard against drags that *start inside and end on the backdrop*. That direction is handled correctly. The reverse is not. Per UI Events, when mousedown and mouseup have different targets the `click` event is dispatched at their nearest common ancestor — which for (backdrop-down, dialog-up) is the overlay itself. So `e.target === e.currentTarget` is true, `mouseDownTarget.current` is still the overlay, and the dialog closes. The universal learned gesture for aborting a click — press, then drag away from the target before releasing — does not abort here.

Manual repro (30 seconds, no tooling): open the dialog, press and hold the primary button on the dimmed area, drag the pointer onto the white dialog surface, release. Expected: dialog stays open. Actual: dialog closes.

- Confidence: **HIGH** on the mechanism; **MEDIUM** on how often users perform this gesture deliberately.
- User group: motor (tremor, imprecise pointing, drag overshoot), cognitive (unexpected dismissal with no undo), low vision (the backdrop/dialog boundary is harder to judge under magnification).
- WCAG: 2.5.2 Pointer Cancellation (Level A) — the up-event completes the function and no abort mechanism is available for a down-event that began on the backdrop. Related: 3.3.4 Error Prevention and the cognitive-perspective requirement for confirmation before destructive actions, since a dismissal discards whatever the consumer's children hold.
- **Fix**: make the guard symmetric — require that *both* the mousedown target and the mouseup target are the overlay. Capture `e.target` in an `onMouseUp` handler and compare both, or use `onPointerDown`/`onPointerUp` with `pointerId` matching. Separately, expose a `dismissOnBackdropClick` prop (defaulting to `false` for any dialog holding unsaved input) so consumers can opt out entirely.
- **Mitigated by**: the common accidental case — text-selection drag ending on the backdrop — is already guarded, which removes the highest-frequency variant. Escape and the close button remain unaffected. Escalates to MAJOR in any dialog holding unsaved user input, where the same gesture becomes silent data loss.

---

**MINOR-4 — Both global key handlers are bubble-phase listeners on `document`, so a single `stopPropagation()` in consumer content disables the trap *and* Escape.**

Evidence: `Modal.jsx:67` (`document.addEventListener('keydown', handleEscape)`) and `Modal.jsx:114` (`document.addEventListener('keydown', handleTabKey)`) — neither passes `{ capture: true }`.

Third-party widgets that consumers routinely drop into dialogs — comboboxes, date pickers, rich-text editors, code editors — very commonly call `stopPropagation()` on `keydown` to protect their own key handling. When they do, neither handler on `document` ever runs: Tab from the last control walks straight out of the dialog, and Escape does nothing. Related and independent: if the dialog body contains a cross-origin `<iframe>` (payment form, embedded video), keydown inside it never reaches the parent document at all, so Escape is inoperative for as long as focus is inside the frame.

- Confidence: **HIGH** on the mechanism; **MEDIUM** on frequency (entirely determined by what consumers mount).
- User group: keyboard-only, screen reader.
- WCAG: 2.1.1 Keyboard, 2.1.2 No Keyboard Trap.
- **Fix**: register both listeners with `{ capture: true }` so they run before any descendant can stop propagation. For the iframe case there is no complete fix from the parent frame — document the limitation and keep the visible close button as the guaranteed path (it already is).
- **Mitigated by**: the same out-of-dialog recovery branch (`Modal.jsx:93–97`) heals the escape on the next Tab that *is* allowed through, and the close button is always rendered and always reachable, so no configuration produces a hard trap. Capture-phase registration is a two-character change with no downside — worth doing regardless of the current impact estimate.

---

**MINOR-5 — Focus restoration has no fallback when the previously-focused element is gone or no longer focusable.**

Evidence: `Modal.jsx:50` — `previouslyFocusedElement.current?.focus();`. The optional chain guards against `null`, not against a *detached* or *now-unfocusable* node.

`.focus()` on an element removed from the document is a silent no-op, and focus falls to `<body>`. This is not exotic: the dialog's own action commonly removes its trigger (delete the row whose "Delete" button opened the confirm; complete the step whose button opened the wizard; the trigger re-renders under a new key). It also fires if the trigger became `disabled` while the dialog was open — a common pattern during a submit. When focus lands on `<body>`, a screen-reader user is returned to the top of the document with no announcement of what happened, and a keyboard user's next Tab starts from the beginning of the page.

- Confidence: **MEDIUM** — measured working for the tested case (`step_0006`), unmeasured for the trigger-removed case, and the frequency depends on how consumers use it.
- User group: screen reader, keyboard-only.
- WCAG: 2.4.3 Focus Order — focus after close must preserve meaning and operability.
- **Fix**: before restoring, verify the target is still connected and focusable (`el?.isConnected && typeof el.focus === 'function' && !el.disabled`); otherwise fall back to a caller-supplied `returnFocusTo` ref, and past that to a `tabindex="-1"` container near where the trigger was, so the user resumes in context rather than at the document root. Never fall back to bare `document.body`.
- **Mitigated by**: the common path is measured working. This is hardening for a known-fragile case, not a repair of observed breakage.

---

### Enhancements (best practice not met, no access barrier)

**ENH-1 — Background content is not inert; `aria-modal` and the JS trap are each a single point of failure.** `aria-modal="true"` (`Modal.jsx:148`) asks AT to ignore background content, and the trap keeps Tab inside. Neither prevents background reachability by other means: AT virtual-cursor navigation on platforms with imperfect `aria-modal` support, browser find-in-page, mobile swipe navigation, or a screen-reader user's own reading-cursor commands. Adding `inert` to the application root (or `aria-hidden` on the siblings of the portal) while the dialog is open makes the guarantee structural rather than advisory, and would neutralize MINOR-1 and MINOR-4 as a side effect. The strongest version of this is `<dialog>` + `showModal()`, which supplies role, modal semantics, top-layer, background inertness, the Escape behavior, and the focus trap from the platform — the ARIA construction here is fully APG-legitimate, so this is a robustness argument, not a correctness one.

**ENH-2 — Wrap the `✕` glyph in `<span aria-hidden="true">`.** `Modal.jsx:158`. The `aria-label` at `Modal.jsx:156` already wins the name computation and the trace confirms no "times"/"multiplication" leakage in `new_phrases`, so there is **no measured user impact today**. The defensive form protects against the label being dropped in a refactor and against braille/verbose-mode variation across real AT that the emulated persona cannot represent.

**ENH-3 — `.modal-dialog:focus` is dead CSS.** `modal.css:25–27` styles a focus state on the dialog container, but the container has no `tabIndex` (`Modal.jsx:144–150`), so it can never receive focus. The rule encodes an intent — focus the dialog itself — that was not implemented. Either implement it (add `tabIndex={-1}` and prefer focusing the dialog when the content is long enough that focusing the first control would scroll the heading out of view, which APG explicitly contemplates) or delete the rule. Leaving it is a false signal to the next maintainer that container focus is handled.

**ENH-4 — `title` is load-bearing for the dialog's accessible name but is not enforced.** `Modal.jsx:27` destructures `title` with no PropTypes, no TypeScript, and no fallback. A consumer omitting it ships a dialog whose name resolves to an empty `<h2>` — most AT will then announce only "dialog". Require the prop at the type level, or fall back to `aria-label="Dialog"` when `title` is empty, so the failure is impossible rather than merely unlikely.

**ENH-5 — Pre-empt the lint false positive on the overlay.** `Modal.jsx:138–142` will trip `jsx-a11y/click-events-have-key-events` and `jsx-a11y/no-noninteractive-element-interactions`. Per the protocol's known-false-positive guidance, this is a **false positive in context** and must not be "fixed" by adding `onKeyDown`/`tabIndex` to the backdrop — that would create a redundant tab stop and a spurious control in the AT tree. Add an eslint-disable with a comment pointing at the Escape handler as the keyboard equivalent, so the reasoning survives.

---

## Phase 7 — What's Missing (gaps, unhandled edge cases, unstated assumptions)

- **No stacking support, and the failure is silent.** Two simultaneously-open instances break in at least four ways: duplicate `id="modal-title"` (MINOR-2); both Escape handlers fire, closing the whole stack on one keypress (`Modal.jsx:58–69`); both Tab handlers are live on `document`, and the outer instance sees focus as "outside my dialog" and yanks it back to its own boundary on every Tab (`Modal.jsx:93–97`) — the inner dialog becomes untraversable; and whichever instance closes first restores `document.body.style.overflow = ''` (`Modal.jsx:48`) while the other is still open, unlocking page scroll underneath. None of this is documented as a limitation. Either add a dialog-stack registry so only the topmost instance owns Escape, the trap, and the scroll lock, or document loudly that instances must not overlap.
- **The scroll lock clobbers pre-existing inline style.** `Modal.jsx:45` writes `document.body.style.overflow = 'hidden'` and `Modal.jsx:48` resets it to `''` — not to its prior value. Any application that sets body overflow inline for its own reasons loses that setting permanently after the first dialog closes.
- **No `prefers-reduced-motion` block** — correctly, and worth stating so nobody "fixes" it: the only transition is `color 0.2s` on the close button (`modal.css:50`). Color transitions are not motion; there is no entry/exit animation, no parallax, no autoplay. Nothing to suppress. If an entry animation is added later, the media query becomes required.
- **No `lang`, no landmark, no skip link** — all out of scope. A dialog is not a page region and needs none of them; `region.landmark: null` in the trace is a harness-page property.
- **Unstated assumption: consumer children are keyboard-cooperative.** The whole trap rests on children not calling `stopPropagation()` (MINOR-4) and on their focusable elements being ones this selector recognizes (MINOR-1). A design-system component should say so in its docs.
- **Unstated assumption: `onClose` is safe to call unconditionally.** There is no unsaved-changes hook and no confirm affordance; backdrop click, Escape, and the close button all invoke `onClose` with no distinction between them, so a consumer cannot treat accidental dismissal differently from deliberate dismissal.
- **The zero-focusable branch is unreachable defensive code, not a trap.** `Modal.jsx:81–84` `preventDefault`s every Tab when the dialog contains nothing focusable — which would be a keyboard trap, except the component always renders the close button, so the list is never empty. Worth keeping, worth knowing it is dead. It would become live only if a consumer's CSS hid the close button (`display:none`), which is a stronger reason to give the close button a non-overridable presence than to change the branch.

---

## Phase 6 — Multi-Perspective Review

### Perspective Alarm Levels

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | MEDIUM | Hand-rolled ARIA dialog; hardcoded label id (MINOR-2); `aria-modal` is the sole background-suppression mechanism (ENH-1) |
| Keyboard-only | MEDIUM | Hand-rolled focus trap with a manually enumerated tabbable set (MINOR-1) and bubble-phase listeners (MINOR-4) |
| Low vision | LOW | Focus visibility and indicator contrast measured passing at all six stops; component's own control measures 34×36; no sticky chrome; no unmeasured 200%/400% pass, hence LOW rather than NONE |
| Cognitive | MEDIUM | Unconfirmed, un-undoable dismissal via a one-directional backdrop guard (MINOR-3); no unsaved-changes path |
| Vestibular & motion | LOW | Single 0.2s color transition; no motion, no parallax, no autoplay, no flashing |
| Auditory access | LOW | Component renders no media and no auditory alerts |
| Environmental contrast | LOW | Computed text ratios pass with margin; no color-only meaning; nothing depends on the sub-threshold divider |

Screen reader, keyboard-only, and cognitive are at MEDIUM and are the candidates for deep review via `/perspective-audit` if the team wants one. I do not think it is required for this component at its current scope — the MEDIUMs are driven by *architecture class* (hand-rolled ARIA widget) rather than by observed defects, and the observed defects are all MINOR.

### Notes per perspective

**Screen reader user (NVDA, JAWS, VoiceOver):** The measured experience is correct. Entering the dialog produces "dialog, Settings, modal" followed by "button, Close dialog" (`step_0002`) — role, name, modal state, and the first control's purpose, in that order, with no redundancy and no leaked `✕`. Live-region silence at every step is the right outcome, not a gap: a dialog announces itself through the focus and role change, and adding `aria-live` would double-announce. The two residual concerns are the label-id collision under stacking (MINOR-2) and the fact that background suppression rests entirely on `aria-modal` (ENH-1). Calibration caveat the evidence forces: this is the keyboard-a11y-tester screen-reader *persona*, an emulation of the accessibility tree, not NVDA/JAWS/VoiceOver. It is strong evidence the tree is right and weak evidence about real voicing — in particular, `aria-modal` support and virtual-cursor containment are exactly the things that vary between real AT and an emulation.

**Keyboard-only user:** Fully operable on the tested content, and measured: Tab reaches the trigger with a visible indicator (`step_0001`), Enter opens and focus lands inside (`step_0002`), Tab cycles Close → Save → Close → Save (`step_0003`–`step_0005`, the wrap at `step_0004` being the proof the trap holds), Escape closes and returns focus to "Open settings" (`step_0006`). No positive tabindex, no keyboard trap, no undiscoverable shortcuts — the only key bindings are Tab and Escape, both conventional for a dialog. Shift+Tab is unverified (code-symmetric, so high confidence). The exposure is entirely in what a consumer mounts inside: an iframe, a `<details>`, or a roving-tabindex widget will produce a wrong wrap anchor (MINOR-1), and a `stopPropagation()`-ing child will silence both handlers (MINOR-4). Both degrade to "one stop outside the dialog, then automatic recovery," not to lost access.

**Low vision user (200% zoom, high contrast, magnifier):** Measured focus indicators are visible at all six stops with `indicator: "outline"`, and their non-text contrast is 3.14–4.74 — all clearing the 3:1 bar for 1.4.11. The component's own close button clears 2.4.13 Focus Appearance (AAA) as well, at contrast 4.31 with `area_pass: true`. Two steps fail the AAA area bar (`step_0003` and `step_0006`, `area_pass: false`, contrast 3.14) — these are the *harness page's* default-outlined buttons, 2.4.13 is Level AAA and outside the WCAG 2.2 AA target, and the finding class is informative by the tool's own labeling. Not a finding. Text contrast computed from the CSS: `#333` on white = 12.6:1 for both the `<h2>` (`modal.css:40`) and the body (`modal.css:66`); `#666` on white = 5.74:1 for the close glyph (`modal.css:49`) — all clear 4.5:1 as normal text, before the 24px size even brings the large-text allowance into play. The `#eee` header divider (`modal.css:34`) is 1.16:1 against white and needs no ratio *because it carries no information*; if the team ever makes it the sole delimiter of the header region, it fails. Reflow: `max-width: 500px; width: 90%; max-height: 80vh; overflow-y: auto` (`modal.css:14–20`) keeps the dialog inside the viewport and scrolls overflow internally; because `overflow-y: auto` forces `overflow-x` to compute to `auto`, wide content scrolls inside the dialog rather than the page — 1.4.10 is handled by construction. Text spacing (1.4.12) is safe for the same reason: increased line-height scrolls rather than clips. `px` font sizes are **not** a 1.4.4 failure — browser zoom scales them; flagging px here would be a false positive. Target size: the component's own control measures 34×36 (`step_0002`), passing 2.5.8. The harness's "Save changes" (100.5 × 21) and "Open settings" (98.3 × 21) are under 24px tall, but their measured positions are hundreds of pixels apart, so the 2.5.8 spacing exception applies and they pass — and in any case they are demo-page content, not this component. Not measured: an actual 200%/400% pass, forced-colors mode, or whether the outline survives Windows High Contrast.

**Cognitive accessibility:** Consistent and calm — one dialog, one heading, one close control, two dismissal routes that behave identically. No timeouts, no cognitive-function tests, no multi-step re-entry, no motion. The gap is dismissal safety: backdrop click closes unconditionally, the abort gesture does not abort (MINOR-3), there is no undo, and the component gives the consumer no seam for a confirm. For an informational dialog this is nothing; for the fixture's own demo shape — a Settings dialog with a "Save changes" button — an accidental dismissal is silent data loss with no signal that anything was lost.

---

## Phase 8 — Realist Check (Severity Calibration)

Every finding was run through the four questions. Three recalibrations, all documented with mitigations:

- **MINOR-1 was drafted as MAJOR.** Worst realistic case: a keyboard or screen-reader user Tabs once into background content that `aria-modal` has told their AT does not exist. But the recovery branch at `Modal.jsx:93–97` pulls them back on the very next Tab, Escape still works from anywhere because its listener is on `document`, and the demo content never triggers the bug at all. Self-healing within one keystroke is not "significantly degrades." **Downgraded. Mitigated by: the out-of-dialog focus recovery branch, plus a document-scoped Escape handler that remains operative wherever focus lands.**
- **MINOR-3 was drafted as MAJOR.** Worst realistic case: a user with a tremor loses unsaved form input. But the highest-frequency accidental variant (drag-select released on the backdrop) is already guarded, backdrop dismissal is a conventional and expected affordance, and the confirm-before-discard decision genuinely belongs to the consumer's `onClose`. **Downgraded. Mitigated by: the existing mousedown guard covering the common accidental case, and consumer ownership of `onClose` semantics.** Flagged as escalating to MAJOR for any dialog holding unsaved input.
- **MINOR-2 was drafted as MAJOR.** Worst realistic case: a screen-reader user is told they are in the wrong dialog. Severe *if* it happens — but it requires two simultaneously-open instances, which the component does not claim to support and which the fixture's Expected Behavior does not describe. **Downgraded. Mitigated by: single-instance usage being the documented and overwhelmingly common case.** Flagged as escalating to MAJOR the moment stacking is introduced.

Nothing was downgraded that involves complete access loss, data loss without a named escalation condition, or safety. Nothing was upgraded by review momentum: I specifically resisted rating the `<div role="dialog">` construction as a native-HTML-first violation (the APG sanctions it), the `✕` glyph as a 4.1.2 finding (the trace proves the name computation is correct), `px` font sizes as 1.4.4 (zoom handles them), the harness's 21px-tall buttons as 2.5.8 (spacing exception applies, and they are not this component), and the `role="presentation"` overlay as a semantics smell (it is the correct choice).

## Phase 9 — Self-Audit

| Finding | Confidence | Developer could refute? | Gap or preference? |
|---|---|---|---|
| MINOR-1 (tabbable set) | HIGH on mechanism, MEDIUM on frequency | No on mechanism — it is CSS selector semantics. Yes on impact, if children are constrained by policy | GAP |
| MINOR-2 (hardcoded id) | HIGH on mechanism, MEDIUM on applicability | Yes, if the app provably never stacks dialogs | GAP |
| MINOR-3 (one-directional guard) | HIGH on mechanism, MEDIUM on gesture frequency | Partially — a product decision to accept backdrop dismissal is legitimate; the *asymmetry* is not intentional | GAP |
| MINOR-4 (bubble-phase listeners) | HIGH on mechanism, MEDIUM on frequency | Yes, if consumer content is fully controlled | GAP |
| MINOR-5 (no restore fallback) | MEDIUM | Yes, if triggers are guaranteed stable | GAP |
| ENH-1 … ENH-5 | HIGH | Enhancements by construction | Mixed — ENH-2/ENH-5 are defensive practice, correctly rated below MINOR |

No finding was held at LOW confidence, so nothing moved to Open Questions on that basis. Nothing rated MINOR or above is a stylistic preference. **Explicit calibration statement: the semantics here are correct and I am saying so rather than manufacturing a finding to justify the review.** The dialog role, modal state, name association, heading, native button, presentational backdrop, unmount-on-close, deferred initial focus with a stale-timer guard, per-Tab recomputation, out-of-dialog recovery, document-scoped Escape, and the deliberate effect split are all right, and several of them are right in ways that most hand-rolled modals get wrong.

## Phase 10 — Synthesis

Predictions versus reality: four of six priors were refuted outright, and the two that landed did so in an unexpected place. I expected to find a *missing or half-built* pattern — the usual "80% modal." Instead the pattern is 100% present and three of its hardest parts are measured working. Every remaining defect is a list-keeping failure inside a correct mechanism: which selectors count as tabbable, which id is unique, which pointer direction the guard covers, which event phase the listener uses, which restore target still exists. That is a meaningfully different diagnosis than "incomplete pattern," and it points at a different fix: not more design work, but replacing hand-maintained enumerations (the tabbable selector, the hardcoded id) with sources that cannot drift.

One thing the review turned up that the code alone would not: the fixture's own feature checklist asserts two things the code does not do — that the trap "covers the full tabbable set" and that `tabindex="-1"` elements are excluded. The code comment at `Modal.jsx:4–6` makes the same claim. Documentation that overstates a guarantee is worse than absent documentation, because it is what the next consumer will trust instead of testing.

---

## Verdict Justification

**ACCEPT.** Zero CRITICAL, zero MAJOR. The WAI-ARIA Modal Dialog pattern is implemented completely, and the four failure modes that make modals inaccessible — no focus containment, no focus restoration, no accessible name, no Escape — are all absent, three of them confirmed by measurement rather than by reading. The measured evidence is unambiguous on the load-bearing behaviors: "dialog, Settings, modal" announced on entry, the Tab wrap at `step_0004`, focus back on the trigger at `step_0006`, a visible focus indicator at 3.14–4.74:1 non-text contrast at every one of six stops.

A clean bill of health here carries real signal, and it is worth being explicit about what I checked *for the purpose of not finding it*: the `<div role="dialog">` construction is APG-sanctioned and not a native-HTML-first violation; the `role="presentation"` backdrop with a click handler is the correct choice and its lint warning is a known false positive; the `✕` glyph does not leak into the accessible name, which the trace proves; `px` font sizes are not a 1.4.4 failure; the AAA 2.4.13 area misses belong to the harness page and are informative by the tool's own labeling; the undersized harness buttons pass 2.5.8 via the spacing exception; and the empty `live_announcements` arrays are the expected result for a component that declares no live region, not a gap. None of the 28 sibling findings files in the evidence pack describe this page, and none were imported.

**What would move this to ACCEPT-WITH-RESERVATIONS or lower:** introducing dialog stacking without first fixing MINOR-2 and the Escape/trap/scroll-lock ownership described in What's Missing; or shipping this as a design-system primitive whose consumers can mount arbitrary content, without fixing MINOR-1. Either change converts today's MINORs into MAJORs by widening the exposure, not by changing the code.

**Recommended order of work**, all small: MINOR-1 (a) and (b) plus the corrected comment and checklist (highest ratio of risk removed to effort); MINOR-2 via `useId()` (one line); MINOR-4 via `{ capture: true }` (two characters, no downside); MINOR-3's symmetric guard plus a `dismissOnBackdropClick` prop; MINOR-5's connected-and-focusable check; then ENH-1's `inert` on the app root, which retires a whole class of residual risk. ENH-3 costs nothing and removes a false signal for the next maintainer.

**Escalation:** not required. Screen reader, keyboard-only, and cognitive sit at MEDIUM and are eligible for `/perspective-audit`, but they are MEDIUM because of the component's architecture class (hand-rolled ARIA widget hosting arbitrary content), not because of anything observed. If the component is being promoted to a shared design system, run the audit at that point — the exposure changes, and so should the scrutiny.

---

## Open Questions (unscored)

1. **Does this application ever stack dialogs?** The answer converts MINOR-2 from a one-line hygiene fix into a MAJOR with three siblings (Escape ownership, competing traps, premature scroll-unlock). I cannot determine this from the component in isolation.
2. **What React version is this on, and does the trigger ever unmount with the dialog?** The trace proves synchronous restoration works in the tested configuration, but the version is not stated and the trigger-removed path (MINOR-5) is untested.
3. **Is Shift+Tab actually symmetric in practice?** The code says yes and I rate it high-confidence, but the trace never sends it. One driven step would convert design reasoning into measured fact — cheap, and worth adding to the fixture.
4. **Does the out-of-dialog recovery branch behave as read?** It is the mitigation carrying two of my three severity downgrades, and it is entirely unexercised by the evidence. If it does not work as written, MINOR-1 and MINOR-4 both revert to MAJOR. This is the single highest-value gap to close in the next test pass.
5. **What is the intended `.modal-dialog:focus` behavior (ENH-3)?** If the author meant to focus the container for long content, the rule should be implemented; if it is vestigial, deleting it prevents a future maintainer from assuming container focus is handled.
6. **Will consumer content include iframes, `<details>`, or roving-tabindex composites?** Determines whether MINOR-1(b) is theoretical or imminent.
7. **Does any dialog in this product hold unsaved user input?** Determines whether MINOR-3 stays MINOR or escalates, and whether `dismissOnBackdropClick` needs to default to `false`.
8. **Is `aria-modal` sufficient for the AT this product actually supports?** The emulated screen-reader persona cannot answer this. A real NVDA/JAWS/VoiceOver pass — particularly a virtual-cursor sweep to confirm background content is genuinely unreachable — is the check that would either close ENH-1 or promote it.
