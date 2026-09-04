# Accessibility Design Review — Modal Dialog Component

**Citation convention**: no filenames were supplied with the fixture. Line numbers below are relative to the start of each fenced block in the review material: `Modal.jsx:N` = line N counting from `import React...`; `modal.css:N` = line N counting from `.modal-overlay {`. Every cited line is quoted inline so the reference is checkable without the offset.

---

## Phase 0 — Consume Test Evidence

### 0.1 Evidence tier (reported before anything is consumed)

The supplied Evidence Pack is an **`a11y-evidence-reader` digest**, not the artifact. Per the protocol, a digest is detector output one tier BELOW the artifact it cites — a paraphrase. The rule is: re-fetch at the cited handle before filing any finding that rests on a digest line; a finding that cannot be traced to a re-fetched handle is labeled digest-only.

I could not re-fetch. `modal-complete-clean.trace.json` was not supplied and I have no access to it. **Every evidence-derived claim in this review is therefore labeled `digest-only`.** I am not suppressing them — the digest is unusually disciplined (verbatim jq handles, explicit substitution flags, explicit not-claimed list) — but no measurement below is independently verified, and none of my scored findings rests on a digest line alone.

### 0.2 Substitution flags — what the evidence set does and does not license

The digest flags three of its five observations as substitutions against a11y-test's Verification evidence contract. Handling each:

| Class | Canonical evidence | What was actually supplied | My ruling |
|---|---|---|---|
| `focus-order-indicator` | keyboard-a11y-tester driven trace | driven trace (obs. 1, 2) | **In-contract.** Hard-evidence tier. |
| `name-role-state` | virtual-screen-reader assertions | KAT's own AX snapshot (obs. 3) | **Substitution stands.** KAT self-reports its simulated announcement; it is not a screen-reader assertion. Usable as corroboration, not as name-role-state proof. |
| `keyboard-operability` | `npx playwright test` real-keyboard transcript | driven trace (obs. 4) | **Substitution over-strict for this review.** Phase 0 of *this* protocol explicitly tiers keyboard-a11y-tester driven artifacts *equal to* codified Playwright runs (it drives CDP `Input.dispatchKeyEvent`). The stricter contract-type gate binds when reviewing a **fix**; this is a fresh design pass, so the trace counts as keyboard evidence. Noting the disagreement rather than deferring to it. |
| `machine-detectable` | axe-core scan | KAT's incidental `region`/`role` fields (obs. 5) | **Substitution stands, and it is the consequential one.** No axe artifact was read. |

**Consequence of the last row**: the structural half of the digest's own question ("missing or incorrect ARIA role, landmark, label, or heading-order violation") is **unanswered by the supplied evidence**. Everything structural in this review is source-read reasoning, not measurement. I say so at each point rather than letting the trace's incidental fields stand in for a scanner.

### 0.3 Findings against the evidence itself

**E-1 (MAJOR, against the instrument — not against the component): observation 2 is self-contradictory within a single trace.**
`digest-only`. Handle: `modal-complete-clean.trace.json — jq '.steps[] | {step_id, active_element_selector, area_pass: .focus_appearance.area_pass, aaa_pass: .focus_appearance.aaa_pass}'`. The same `active_element_selector` yields `area_pass:false` at `step_0003` and `area_pass:true` at `step_0005` (the "Save changes" button), and `area_pass:true` at `step_0001` / `false` at `step_0006` (the "Open settings" trigger). Same element, same trace, same session, opposite verdicts.

A measurement that contradicts itself on the same element under the same conditions is **not evidence of a component property**. It cannot be filed against the component in either direction. Three further reasons not to file it:

1. **Both false readings sit at DOM-transition moments.** `step_0003` is the first Tab after the dialog mounts; `step_0006` is the Escape step where the dialog unmounts and focus restores. A geometry measurement racing paint/unmount is the parsimonious explanation.
2. **WCAG 2.4.13 Focus Appearance is Level AAA.** The `aaa_pass` field name agrees. A failing `area_pass` does not touch a WCAG 2.2 **AA** conformance target. (Repo calibration, KAT upstream issue #27: the tool's `conformance_level` field is a pass/fail gate, not the SC's WCAG level — derive level from the SC number. Applied here.)
3. **Neither inconsistent element is styled by this component.** `body > div:nth-of-type(2) > div > div:nth-of-type(2) > button` resolves to a button inside `.modal-body`, i.e. consumer-supplied `children`; `#root > div > button` is the host page's trigger. The component's *own* focused control — `.modal-close`, at `div:nth-of-type(1)`, steps 2 and 4 — is `area_pass:true` on **both** visits, and `focus_appearance.contrast_pass` is true at all six steps.

Recommended action against the instrument: re-run with a settle delay after focus before sampling geometry, then re-read. Do not file 2.4.13 against this component on the current data.

**E-2 (MAJOR, against the evidence set): the absence claims are weaker than they look.**
The digest reports `grep -oiE '(fail|violat|warn|error|defect|issue)[a-z]*' → empty`. The digest itself establishes that this artifact is a **focus walk, not a rule engine** — obs. 5 says explicitly "NOT an axe-core artifact... not axe rule-fired/rule-stopped findings." Absence of a violation marker in an artifact that emits no violation markers is not evidence of no violations. Reading "no fail markers → clean" would be rubber-stamping. I do not treat any absence claim here as clean-bill evidence.

**E-3 (MAJOR, against the evidence set): coverage does not reach the claim it appears to support.**
The fixture's Expected Behavior asserts the trap "cycle[s] through every tabbable element inside the dialog — links, buttons, inputs, selects, textareas, contenteditable regions, and elements with a non-negative tabindex — skipping disabled controls and `tabindex="-1"` elements." The trace exercises **two buttons**. `jq '.steps[].ax_name_role_state.role'` is `"button"` at all six steps, and the digest's own absence claim confirms no non-button role appears. No input, select, textarea, contenteditable, `[tabindex]`, disabled control, or `tabindex="-1"` element ever entered the trap. **The broad claim is untested.** This matters directly: finding M-1 below is a defect in the focusable-set filter that this trace could not have surfaced.

**E-4 (MINOR, against the evidence set): only one close path is traced.**
`step_0006` is Escape. The close-button path and the backdrop-click path — and focus restoration under each — are unmeasured.

### 0.4 Two false-positive traps in the evidence, declined

**Trap A — "no landmark anywhere" (obs. 5).** `region.landmark` is null at all six steps including the four inside the dialog. This is **not** a finding. A dialog is not a landmark; content inside a modal dialog carries no landmark requirement; and the component renders through `ReactDOM.createPortal(..., document.body)` (`Modal.jsx:137`, `Modal.jsx:164`), so the correct container semantics are `role="dialog"` + `aria-modal="true"` — which are present. Filing "missing landmark structure" here would be a scoping error, and the field is incidental trace capture rather than scanner output in any case.

**Trap B — "no `aria-expanded` / static `states` dict" (obs. 3).** `grep -oE '(expanded|haspopup|aria-[a-z]+)' → empty`, and `ax_name_role_state.states` is `{"invalid":"false","focusable":true,"focused":true}` at every step. This is **not** a finding either. The WAI-ARIA APG **Modal Dialog** pattern does not put `aria-expanded` on the dialog trigger — that belongs to Disclosure and Combobox. There is no toggling ARIA state in this component to report. Absence is correct.

### 0.5 What the evidence does license (digest-only, corroborative)

- **Focus enters the dialog on open.** `step_0002` (Enter) → `active_element_selector` = the header close button; `focus_moved:true`, `is_body:false`.
- **The dialog boundary is announced with the right name and modality.** `step_0002.sr_announcement.new_phrases` = `["dialog, Settings, modal", "button, Close dialog"]`. This is the one line that corroborates `role="dialog"` + `aria-modal="true"` + `aria-labelledby` resolving to the `<h2>` — and it lands **before** the button phrase, which resolves the "does focusing a child skip the dialog name" question in the component's favour. Tier caveat: KAT's simulated announcement, not a screen-reader assertion.
- **The trap cycles.** Steps 3→4→5 alternate between the two in-dialog buttons; `focus_moved` is true at every step and never lands on `body`.
- **Focus restores on Escape.** `step_0006` (Escape) → `active_element_selector` returns to `#root > div > button`, the pre-dialog trigger. This is the measured fact that retires my second pre-commitment prediction.

---

## Phase 1 — Pre-commitment Predictions

Written before reading the source, from component type (modal dialog):

1. Focus trap absent or only partially implemented.
2. Focus does not restore to the trigger on close.
3. Backdrop is clickable-to-dismiss with no keyboard equivalent, and/or exposed to AT as a stray node.
4. Close control is a `div`/`span` with `role="button"` rather than a native `<button>`.
5. Background content is not made inert — `aria-modal` alone, or nothing.
6. ARIA `id`s hardcoded, so two instances collide.

Scored against what I found:

| # | Prediction | Outcome |
|---|---|---|
| 1 | Trap absent/partial | **Partly wrong.** Trap is implemented and unusually thorough — recomputed per Tab, with an out-of-dialog recovery clause most implementations lack. But the focusable-set filter is incomplete in a way that can invalidate its wrap anchors (M-1). |
| 2 | No focus restoration | **Wrong.** Implemented (`Modal.jsx:50`) and measured working (`step_0006`). Residual gap is only the no-fallback case (m-1). |
| 3 | Backdrop keyboard/AT problem | **Wrong.** `role="presentation"` (`Modal.jsx:142`), not focusable, Escape is the documented keyboard equivalent, and the dismissal is guarded against text-selection drags. Correct design. |
| 4 | Non-native close control | **Wrong.** Native `<button>` (`Modal.jsx:153`). |
| 5 | Background not inert | **Right.** `aria-modal="true"` only; no `inert` (m-2). |
| 6 | Hardcoded ARIA ids | **Right.** `id="modal-title"` is a static literal (M-2). |

Three of six predictions were wrong **in the component's favour**. Stating that plainly, because it is the calibration signal: this is not a component where the standard modal failure list applies, and a review that reported the standard list here would be manufacturing.

---

## Phase 2 — Semantic HTML Audit

Verified against source, not assumed:

- **Native elements throughout.** The close control is `<button>` (`Modal.jsx:153`), not a `div` with `role="button"`. No ARIA is masking bad semantics anywhere in this component. The Non-negotiable rule (native HTML first) is satisfied.
- **Heading.** `<h2 id="modal-title">{title}</h2>` (`Modal.jsx:152`). The dialog is portal-rendered under `document.body` and `aria-modal="true"` removes the rest of the page from the AT tree, so page heading sequence does not run through it. `h2` is a defensible, conventional choice. **No finding.** Note the evidence limit: the digest states the trace captures nearest-heading *text* only, never *level*, so heading order cannot be assessed from measurement either way — I am not claiming it passed a check that was never run.
- **Landmarks.** None, correctly — see Trap A.
- **Lists / tables** — none present.
- **Form labels** — no form controls owned by this component; `children` is the consumer's responsibility and out of scope.
- **`role="presentation"` on the overlay (`Modal.jsx:142`)** is correct and worth crediting: it is a plain `div`, neither focusable nor carrying global ARIA, so `presentation` applies; and because `presentation` (unlike `aria-hidden`) does not propagate to descendants, the dialog inside stays fully exposed. This is a deliberate, correct choice, not an accident.
- **The `✕` glyph (`Modal.jsx:158`)** is superseded by `aria-label="Close dialog"` (`Modal.jsx:156`) in accessible-name computation, so it is never announced as "times"/"multiplication x". The Phase 5 symbol rule is **satisfied**; wrapping it in `aria-hidden="true"` would be belt-and-braces only. Not a finding. (WCAG 2.5.3 Label in Name does not fire either — an icon glyph is not a visible text label, so there is no visible-text string a speech-input user would say.)

**Phase 2 result: no findings.** The semantic layer is correct.

---

## Phase 3 — ARIA Pattern Compliance Audit

Pattern: **WAI-ARIA APG Modal Dialog.** Checked element by element.

| APG requirement | Present? | Evidence |
|---|---|---|
| `role="dialog"` (or `alertdialog`) on the container | Yes | `Modal.jsx:147` |
| `aria-modal="true"` | Yes | `Modal.jsx:148` |
| Accessible name via `aria-labelledby` or `aria-label` | Yes | `Modal.jsx:149` → `Modal.jsx:152`; corroborated by `"dialog, Settings, modal"` at `step_0002` (digest-only) |
| Focus moves into the dialog on open | Yes | `Modal.jsx:38-41`; corroborated at `step_0002` |
| Tab/Shift+Tab confined to the dialog | Yes, with a defect in the anchor computation | `Modal.jsx:75-113`; see M-1 |
| Escape closes | Yes | `Modal.jsx:61-63` |
| Focus returns to the invoking element | Yes | `Modal.jsx:50`; corroborated at `step_0006` |
| Content outside the dialog inert | **`aria-modal` only** | see m-2 |
| `aria-describedby` when a descriptive message exists | N/A / no API | see Enhancements |

ARIA **values** are valid: `aria-modal="true"` (not `"yes"`), `role="dialog"` on the container, `role="presentation"` on the scrim. No invalid enumerations anywhere.

**This is a genuinely complete APG Modal Dialog pattern.** The two ARIA-layer findings below are about robustness of the implementation under conditions the pattern itself does not enumerate, not about missing required attributes. No CRITICAL is warranted at this phase — no required ARIA attribute is absent.

---

## Phase 4 — Focus Management Review

The most substantial part of this component, and the part most worth reading closely.

**What is right, verified in source:**

- **Save/restore split from the Escape binding.** The save/restore effect depends on `[isOpen]` only (`Modal.jsx:53`); Escape depends on `[isOpen, onClose]` (`Modal.jsx:69`). An unstable inline `onClose` prop re-binds the key listener without ever re-running the focus lifecycle. That is a deliberate design decision, and the code comment says so. Most hand-rolled modals get this wrong and silently re-save `previouslyFocusedElement` on every parent render — which restores focus to the wrong element. This one does not.
- **Entry focus deferred with `setTimeout(..., 0)`** (`Modal.jsx:38-42`), which is exactly the framework-unmount-timing guard the protocol calls for.
- **Restore is safe despite being synchronous** (`Modal.jsx:50`): `useEffect` cleanups are passive and run *after* the mutation phase, so the portal is already detached and focus has already fallen to `body` by the time `.focus()` is called. `step_0006` confirms the trigger receives focus. No finding.
- **Focusables recomputed on every Tab** (`Modal.jsx:80`) rather than captured once at open — handles children added, removed, or disabled while the dialog is open.
- **Out-of-dialog recovery clause** (`Modal.jsx:93-96`): if `activeElement` has escaped the dialog (a click on static text drops focus to `body`), the next Tab pulls it back to the boundary instead of letting Tab walk into the page behind. This is above the standard for hand-rolled traps and it materially reduces the blast radius of M-1 below. Credit where due.
- **Empty-set guard** (`Modal.jsx:81-84`): `preventDefault()` when nothing is focusable. Unreachable in practice — the close button is always rendered — but harmless.

**Defect: the focusable-set filter is incomplete → see M-1.**

**Dead CSS declaring unfulfilled intent → see m-3.** `modal.css:25-27` styles `.modal-dialog:focus { outline: 3px solid #0066cc; outline-offset: 2px; }`, but `.modal-dialog` carries no `tabindex` (`Modal.jsx:144-149`). The container can never be programmatically focused, so this rule is unreachable. The author evidently intended the APG-common "focus the dialog container" option and stopped one attribute short.

**Tab order** is DOM order: close button (header) → children (body). Logical, matches visual reading order.

**Focus indicators**: `.modal-close:focus` is `outline: 2px solid #0066cc; outline-offset: 2px` (`modal.css:58-62`). #0066cc against the dialog's white background computes to **5.56:1**, comfortably over the 3:1 that 2.4.11/1.4.11 require for a focus indicator, and corroborated by `focus_appearance.contrast_pass:true` at all six steps. No finding — and see E-1 for why the `area_pass` flapping does not change that.

**WCAG checked**: 2.1.1 Keyboard, 2.1.2 No Keyboard Trap, 2.4.3 Focus Order, 2.4.7 Focus Visible, 3.2.1 On Focus.

**On 2.1.2 specifically**: the trap is intentional and escapable by Escape, which is the documented and expected mechanism for a modal dialog. Not a keyboard trap violation — except in the narrow M-1 sub-case described below, where Tab can dead-end.

---

## Phase 5 — State Communication Audit

This component has almost no state to communicate, and that is the correct answer rather than a gap:

- **No loading state, no error state, no success state** in the component itself — those live in `children`.
- **Open/closed** is communicated by the dialog's existence plus focus movement plus the `"dialog, Settings, modal"` announcement, which is the APG-correct mechanism. No `aria-live` needed, and adding one would be wrong.
- **No disabled/readonly/selected/checked/expanded state exists** — see Trap B. The static `states` dict in the trace is the expected reading, not a defect.
- **Symbol-as-state check**: the `✕` is covered by `aria-label` — see Phase 2. Satisfied.
- **Nothing is conveyed by colour alone.** `.modal-close:hover { color: #333 }` is a hover affordance, not state.

**Phase 5 result: no findings.** Reporting this explicitly rather than reaching for one, because a manufactured `aria-live` recommendation here would be exactly the dead output this review is supposed to avoid.

---

## Phase 6 — Multi-Perspective Review

**Screen reader user (NVDA / JAWS / VoiceOver).** Opening the dialog announces `"dialog, Settings, modal"` then `"button, Close dialog"` (digest-only, `step_0002`) — correct boundary, correct name, correct modality, in the correct order. Relationships resolve: `aria-labelledby` → the `<h2>`. Reading order matches DOM order. Two residual exposures: (a) if a second Modal instance mounts, `aria-labelledby="modal-title"` resolves to whichever `#modal-title` is first in document order — the wrong dialog's title (M-2); (b) with `aria-modal` but no `inert`, non-Tab AT navigation — iOS VoiceOver swipe in particular — can leave the dialog, and the Tab-based recovery clause never fires for a swipe (m-2).

**Keyboard-only user.** Tab confined, Shift+Tab wraps, Escape closes, focus returns to the trigger — all measured. Two residuals: the wrap anchors can be wrong when a `visibility:hidden` or `[inert]` focusable sits in the dialog (M-1), and a long text-only dialog body cannot be scrolled from the keyboard in browsers without focusable scrollers, because `.modal-dialog` is the scroll container and has no `tabindex` (m-3).

**Low vision (200% zoom, magnifier, forced colors).** Reflow is fine and I checked it rather than assuming: at 200% on a 1280px viewport the effective width is 640px, `width:90%` = 576px capped by `max-width:500px` (`modal.css:18-19`); at 400% (320px effective) it is 288px. `max-height:80vh` with internal `overflow-y:auto` (`modal.css:20-21`) keeps the dialog inside the viewport, so no page-level horizontal scroll. WCAG 1.4.10 satisfied. Text contrast: `#333` on white = **12.6:1** for both the title (`modal.css:33`) and the body (`modal.css:66`); `#666` on white = **5.74:1** for the close glyph (`modal.css:49`) — over the 4.5:1 normal-text threshold, and the glyph is 24px = 18pt = large text anyway. The real exposure here is forced-colors mode (m-4). Target size: the close button is roughly 38×37 CSS px (24px glyph + 8px horizontal and 8px vertical padding at any plausible line-height), well over the 24×24 that WCAG 2.5.8 requires. **No 2.5.8 finding** — stating that explicitly because "close button too small" is the reflexive finding on this component and the arithmetic does not support it.

**Cognitive accessibility.** The `mouseDownTarget` guard (`Modal.jsx:120-134`) is a real cognitive-accessibility win: it prevents a text-selection drag that ends on the scrim from dismissing the dialog and discarding whatever the user was doing. Someone thought carefully about accidental dismissal. But the thought stops one step short — there is no way for a consumer to turn backdrop dismissal *off* on a data-entry dialog, so a single stray click still discards unsaved input with no confirmation and no undo (WCAG 3.3.4-adjacent). Second cognitive residual: the document-level Escape listener closes every stacked dialog and can be consumed by an inner widget's Escape (m-5).

**Vestibular & motion.** The only animation in the component is `transition: color 0.2s` on the close button (`modal.css:50`). A colour fade involves no movement, parallax, scaling, or autoplay. WCAG 2.2.2, 2.3.1, 2.3.3, 2.5.4 do not fire. **`prefers-reduced-motion` is not needed here** — recommending it would be a manufactured finding, and I am not making one. (The one motion-adjacent nit is the scrollbar-width layout shift on body-scroll-lock; see Enhancements.)

**Auditory access.** No `<video>`, no `<audio>`, no auditory alerts. Not applicable.

**Environmental contrast.** All measured ratios pass (above). Colour is never the sole carrier of meaning. Forced-colors is the exposure (m-4).

### Perspective Alarm Levels

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | MEDIUM | Custom dialog pattern; `aria-modal` without `inert`; static `aria-labelledby` target id; only one instance and one close path ever measured |
| Keyboard-only | MEDIUM | Hand-rolled focus trap with a hand-rolled focusable-set filter; scroll container with no focusable affordance |
| Low vision | MEDIUM | Forced-colors boundary loss; reflow and contrast verified clean |
| Cognitive | MEDIUM | Backdrop dismissal with no opt-out on data-entry dialogs; Escape closes stacked dialogs |
| Vestibular & motion | LOW | Single 0.2s colour transition; no movement, parallax, or autoplay |
| Auditory access | LOW | No media elements of any kind |
| Environmental contrast | MEDIUM | `box-shadow` dropped and both backgrounds forced in forced-colors mode → dialog boundary can vanish |

Five perspectives at MEDIUM → **escalate to `/perspective-audit`**, with screen reader and keyboard-only as the priority lenses.

---

## Phase 7 — Gap Analysis (What Is Absent)

Working the absence list rather than the presence list:

1. **`inert` on background content** — absent. `aria-modal="true"` is the only mechanism. (m-2)
2. **Unique ARIA id generation** — absent. `id="modal-title"` is a literal, with no `useId()`. (M-2)
3. **`tabindex="-1"` on the dialog container** — absent, though `modal.css:25` styles for it. (m-3)
4. **A fallback for focus restoration** when the saved element is detached or was `document.body` — absent. No `isConnected` check at `Modal.jsx:50`. (m-1)
5. **A visibility/inertness check in the focusable filter** — absent. `getClientRects().length > 0` covers `display:none` only. (M-1)
6. **An `initialFocusRef` API** — absent. Initial focus is always the first focusable, which is always the Close button. APG allows this, but a form dialog usually wants the first field. (Enhancement)
7. **A `role="alertdialog"` option** — absent. `role="dialog"` is hardcoded (`Modal.jsx:147`), so a destructive-confirm consumer cannot get the APG-correct role.
8. **An `aria-describedby` hook** — absent, and arguably correct to omit for arbitrary `children`, but there is no escape hatch for the alert-dialog case above.
9. **A guard on an empty/missing `title`** — absent. An empty `title` yields a dialog with an empty accessible name (WCAG 4.1.2), and nothing warns the consumer.
10. **A backdrop-dismissal opt-out** — absent. (Cognitive, above.)
11. **Scrollbar-width compensation on body-scroll-lock** — absent (`Modal.jsx:45`); the page shifts on open.
12. **Restoration of the prior inline `body` overflow value** — absent; the cleanup writes `''` (`Modal.jsx:48`), which clobbers any pre-existing inline value and breaks nested-modal scroll lock.
13. **A forced-colors boundary for the dialog** — absent. (m-4)
14. **An Escape-consumption contract** — absent. Document-level listener, no `e.defaultPrevented` check. (m-5)

Checked and **not** absent, to be explicit about negative space: focus trap, focus restoration, Escape handling, dialog role, modality, accessible name, native button semantics, non-exposed scrim, keyboard equivalent for backdrop dismissal, visible focus indicator, adequate target size, adequate contrast, reflow.

Anti-pattern list from the April 2026 third-party audit, applied: **1** broadcast-vs-association — N/A, no `role="alert"` or `aria-live` anywhere; **2** `title`-as-name — N/A, no `title` attributes; **3** ARIA-without-visible-label — the icon button's `aria-label` is on the control itself, not a wrapper, which is the correct shape; **4** else-branch coverage — the Shift+Tab and Tab branches at `Modal.jsx:99-112` are symmetric, and both are reached by the recovery clause above them; **5** single-selector scope — this is the live root of M-1; **6/7** table row headers and `role="presentation"` on data tables — N/A; **8** decorative alt — N/A, no images; **9** DOM verification — the trace supplies it for the announce path, and does not for the structural claims (see E-3).

---

## Phase 8 — Realist Check (Severity Calibration)

**M-1 (focusable-set filter).** Worst realistic case: a dialog containing an action button hidden with `opacity:0; visibility:hidden` — the exact pattern this protocol's own gap list calls out — makes `lastElement` unfocusable, so Tab from the true last element is not intercepted and focus escapes to the page behind for one stop before the recovery clause pulls it back. In the `firstElement` variant, entry focus silently no-ops and the first Tab both `preventDefault()`s and fails to focus, leaving Tab dead. Impacted: keyboard-only and screen-reader users. Detection: never automated; a user reports it. Not downgraded — the second variant is an operability dead-end, and the trigger pattern is common. **MAJOR confirmed.** Not raised to CRITICAL: the first variant self-heals on the next Tab via the author's recovery clause, and Escape always remains available.

**M-2 (hardcoded id).** Worst realistic case: a confirm dialog stacked over a form dialog announces the *form* dialog's title, so a screen-reader user acts on the wrong mental model at a confirmation step. Impacted: screen reader. Detection: silent; a static axe run will not catch it because both dialogs are never open during the scan. Conditional on multiple simultaneous instances — but this is a reusable component whose props contract permits exactly that, and the fix is one `useId()` call. Not downgraded. **MAJOR confirmed.**

**m-3 (dialog not focusable) — downgraded from MAJOR.** The keyboard-scrolling consequence is real but narrow: it needs a dialog whose body overflows *and* contains no focusable element (any focusable child scrolls into view on Tab), in a browser without keyboard-focusable scrollers. **Mitigated by:** Chrome 127+ ships keyboard-focusable scrollers and Firefox has long made scrollable regions focusable, so the largest browser share is unaffected; and any dialog with a footer action button is unaffected regardless. **MINOR**, with an explicit escalation trigger rather than a quiet downgrade.

**m-2 (no `inert`) — downgraded from MAJOR.** **Mitigated by:** `aria-modal="true"` is honoured by current NVDA, JAWS, and VoiceOver; the scrim blocks pointer access to background content; and the recovery clause at `Modal.jsx:93-96` reclaims focus on the next Tab. The residual is non-Tab AT navigation (iOS VoiceOver swipe, find-in-page, F6), which the recovery clause cannot see. **MINOR**, escalation trigger stated.

**m-5 (Escape scope) — downgraded from MAJOR. Mitigated by:** a consumer *can* stop it — a React `onKeyDown` inside the dialog that calls `stopPropagation()` halts the native event at the React root before it reaches `document`. A real, standard workaround exists. **MINOR.**

**Not filed at all**, after the same four questions: 2.4.13 focus-appearance (E-1: contradictory instrument, AAA criterion, and the flapping elements are not this component's); 2.5.8 target size (arithmetic clears it by ~55%); missing landmark (Trap A); missing `aria-expanded` (Trap B); `prefers-reduced-motion` (no motion to reduce); heading level (unmeasurable, and `h2` under `aria-modal` is defensible).

---

## Phase 9 — Self-Audit

| Finding | Confidence | Refutable by dev context? | Gap or preference? | Disposition |
|---|---|---|---|---|
| M-1 focusable-set filter | HIGH (mechanism) / MEDIUM (frequency) | No on mechanism | GAP | Keep as MAJOR |
| M-2 hardcoded `id` | HIGH | Only by "we guarantee one instance" — which is a constraint the component does not encode | GAP | Keep as MAJOR |
| m-1 no restore fallback | HIGH | No | GAP | MINOR |
| m-2 no `inert` | HIGH | Partly — "our AT matrix honours aria-modal" | GAP | MINOR + escalation trigger |
| m-3 dialog not focusable | HIGH on the dead CSS / MEDIUM on the scrolling consequence | Yes on browser support | GAP | MINOR + "needs user verification" check |
| m-4 forced-colors boundary | MEDIUM | Yes — "we don't support HCM" | GAP | MINOR |
| m-5 Escape scope | HIGH | Yes — workaround exists | GAP | MINOR |
| E-1 instrument contradiction | HIGH | No | GAP (against evidence) | Reported against instrument, not component |
| "Close button too small" | — | — | Would be MANUFACTURED | **Not filed** |
| "Add prefers-reduced-motion" | — | — | PREFERENCE | **Not filed** |
| "Wrap `✕` in aria-hidden" | LOW value | Yes | PREFERENCE | Demoted to a one-line Enhancement |

Moved to Open Questions: nothing at LOW confidence survived as a scored finding.

---

## Phase 10 — Synthesis

The predictions were wrong three times out of six, all in the component's favour. The standard modal failure list — no trap, no restoration, div-as-button, unreachable backdrop dismissal — does not apply here, and the measured evidence corroborates the parts it covers. What survives is a different, harder class: a component that implements the APG Modal Dialog pattern correctly but assumes it is a **singleton** (M-2, m-5) and assumes its **children are simple** (M-1, m-3). Both assumptions are unstated in the code and unverified by the evidence, and both break quietly.

The single most useful thing this review found is M-1, and it is worth naming why: the code comment at `Modal.jsx:22-23` shows the author reasoning about exactly this class of problem — "display:none elements produce no client rects and cannot take focus, so they must not become wrap anchors" — and covering one member of the class while leaving the others. That is the textbook 80%-complete pattern this critic exists to catch, and no automated tool and no trace in the supplied evidence set would have surfaced it.

---

# Output

**VERDICT: ACCEPT-WITH-RESERVATIONS**

**Overall Assessment**: This is a well-built modal. It implements the complete WAI-ARIA APG Modal Dialog pattern with native semantics throughout, a focus trap that recomputes per keystroke and recovers focus that has escaped the dialog, focus restoration that is measured working, a scrim correctly hidden from AT with Escape as its keyboard equivalent, and a mousedown/click guard against accidental dismissal — all of which are above the median for hand-rolled modals. Two MAJOR findings remain, both narrow in trigger and trivial to fix, and both invisible to the supplied evidence: the focusable-set filter excludes only `display:none`, so wrap anchors can be wrong when a `visibility:hidden` or `[inert]` focusable is present; and `id="modal-title"` is a hardcoded literal, so two simultaneous instances misname each other to screen readers. Separately, the supplied evidence pack has a self-contradicting focus-indicator measurement that must not be filed against the component, and no structural/machine-detectable determination is available from it at all.

**Pre-commitment Predictions**: Predicted absent focus trap, absent focus restoration, an unreachable-by-keyboard backdrop, a `div role="button"` close control, no background inerting, and hardcoded ARIA ids. The first four were wrong — the component gets each of them right, and `step_0006` measures the focus restoration. The last two were right, and the two MAJOR findings below are the hardcoded-id prediction plus one I did not predict at all: an incomplete visibility filter inside an otherwise strong focus trap.

## Critical Findings (blocks access)

**None.** No required ARIA attribute is missing, no user category is blocked from the dialog's core function, and no keyboard trap exists on the primary path. Saying so plainly: the search for a CRITICAL here was genuine and came up empty, and inventing one would degrade the signal of every CRITICAL this skill files elsewhere.

## Major Findings (significantly degrades experience)

### M-1 — Focusable-set filter excludes only `display:none`, so focus-trap wrap anchors can be wrong

**Evidence**: `Modal.jsx:20-25`

```js
const getFocusableElements = (container) =>
  Array.from(container.querySelectorAll(FOCUSABLE_SELECTOR)).filter(
    // display:none elements produce no client rects and cannot take
    // focus, so they must not become wrap anchors.
    (el) => el.getClientRects().length > 0
  );
```

Consumed at `Modal.jsx:40` (entry focus) and `Modal.jsx:80` (per-Tab anchor computation).

`getClientRects().length > 0` filters `display:none` correctly — those elements generate no boxes. It does **not** filter three other classes that match `FOCUSABLE_SELECTOR`, are not focusable, and *do* generate boxes:

- `visibility: hidden` elements, and anything inside a `visibility:hidden` ancestor — they participate in layout and return rects, they are simply not painted, and browsers skip them in sequential focus navigation while `.focus()` on them is a no-op. This is precisely the `opacity:0; visibility:hidden` reveal-on-hover pattern this protocol's own gap list flags.
- Elements inside an `[inert]` subtree.
- Elements inside a collapsed `<details>` — mitigated in practice, since the UA stylesheet applies `display:none` there.

Two distinct failure modes follow:

1. **Hidden element lands last.** `lastElement` (`Modal.jsx:87`) is unfocusable, so `activeElement === lastElement` at `Modal.jsx:107` is never true, `preventDefault()` never fires, and Tab from the true last element walks into the page behind the dialog. The out-of-dialog recovery clause at `Modal.jsx:93-96` catches it on the *next* Tab — so focus escapes for one stop and is then reclaimed.
2. **Hidden element lands first.** `firstFocusable?.focus()` at `Modal.jsx:41` silently no-ops, leaving focus on the trigger outside the portal. The first Tab then hits the recovery clause, calls `preventDefault()`, and calls `.focus()` on the same unfocusable element — which does nothing. **Tab is dead**: the user cannot reach any control in the dialog. Escape still closes it, so this is not a permanent trap, but it is an operability dead-end.

**Confidence**: HIGH on the mechanism, MEDIUM on how often a consumer ships such a child.
**User group**: keyboard-only, and screen-reader users navigating by Tab.
**WCAG/APG**: 2.1.1 Keyboard; 2.4.3 Focus Order; WAI-ARIA APG Modal Dialog (Tab/Shift+Tab must be confined to the dialog). Mode 2 additionally touches 2.1.2 No Keyboard Trap.
**Why this matters**: the trap is otherwise the strongest part of this component, so the failure is silent — it looks like a working trap right up until a consumer adds one hover-revealed action button, and then it degrades in a way no test in the supplied evidence set would show (see E-3: the trace only ever sees two plain buttons).
**Not measured**: no evidence in the pack bears on this either way.

**Fix** — replace the rects heuristic with an explicit visibility and inertness check:

```js
const isFocusable = (el) =>
  el.getClientRects().length > 0 &&
  getComputedStyle(el).visibility !== 'hidden' &&
  !el.closest('[inert]');

const getFocusableElements = (container) =>
  Array.from(container.querySelectorAll(FOCUSABLE_SELECTOR)).filter(isFocusable);
```

`Element.checkVisibility({ visibilityProperty: true, contentVisibilityAuto: true, opacityProperty: false })` is the modern equivalent for the first two clauses and is worth preferring where the browser matrix allows — note `opacityProperty: false` is deliberate, since `opacity: 0` elements *are* focusable and must stay in the set. Then harden mode 2 so a no-op `.focus()` cannot dead-end Tab: after calling `.focus()`, verify `modalRef.current.contains(document.activeElement)` and fall through to the next candidate if it does not.

### M-2 — `id="modal-title"` is a hardcoded literal, so simultaneous instances misname each other

**Evidence**: `Modal.jsx:149` `aria-labelledby="modal-title"` referencing `Modal.jsx:152` `<h2 id="modal-title">{title}</h2>`.

Nothing in the component's props contract prevents two `<Modal>` instances being mounted at once — a confirm dialog over a form dialog, or a new dialog opening while the previous one is still unmounting. When that happens, both `<h2>` elements carry `id="modal-title"`. IDREF resolution takes the **first** match in document order, so the second dialog is announced with the first dialog's title. The same collision fires if any consumer page happens to use the generic id `modal-title` elsewhere.

**Confidence**: HIGH.
**User group**: screen reader.
**WCAG/APG**: 4.1.2 Name, Role, Value (the dialog's accessible name is wrong, not merely suboptimal); 1.3.1 Info and Relationships; WAI-ARIA APG Modal Dialog (accessible name requirement). This is also the protocol's own Phase 4 duplicate-DOM check: "Are ARIA IDs unique across duplicates, or do they collide?"
**Why this matters**: a screen-reader user at a confirmation step hears the wrong dialog's title and forms the wrong mental model at exactly the moment the interface is asking them to commit to something. Automated scanning will not catch it — the IDREF resolves, just to the wrong node, and a static scan never has two dialogs open at once.
**Not measured**: the trace exercises one instance only (E-3).

**Fix**:

```jsx
const titleId = React.useId();
// ...
<div ref={modalRef} className="modal-dialog" role="dialog" aria-modal="true" aria-labelledby={titleId}>
  <div className="modal-header">
    <h2 id={titleId}>{title}</h2>
```

Pre-18 codebases can substitute any per-instance unique-id hook. While there, guard the empty case: if `title` is falsy, the dialog ships with an empty accessible name — either require the prop or fall back to an `aria-label`.

## Minor Findings (friction but workaround exists)

- **m-1 — Focus restoration has no fallback when the saved element is gone.** `Modal.jsx:50` calls `previouslyFocusedElement.current?.focus()` unconditionally. Two real cases produce nothing: the trigger was removed from the DOM by the dialog's own action (a "Delete this row" dialog launched from that row's button), and `document.activeElement` was `<body>` at open time (dialog opened programmatically or on load) — `body.focus()` is a no-op. In both, focus falls to the top of the document and the user loses their place. WCAG 2.4.3. *Fix*: check `isConnected` and fall back to a consumer-supplied `returnFocusRef`, then to the nearest connected ancestor, then to a temporarily `tabindex="-1"` `<main>`.
- **m-2 — `aria-modal="true"` with no `inert` on background content.** `Modal.jsx:148`; nothing applies `inert` or `aria-hidden` to the app root. *Mitigated by:* current NVDA/JAWS/VoiceOver honour `aria-modal`; the scrim blocks pointer access; and the recovery clause at `Modal.jsx:93-96` reclaims Tab-escaped focus. Residual: non-Tab AT navigation — iOS VoiceOver swipe especially — leaves the dialog with no recovery, because swipe dispatches no Tab keydown. WAI-ARIA APG Modal Dialog; WCAG 2.4.3. *Fix*: `appRootEl.inert = true` on open, `false` in cleanup. **Escalate to MAJOR if** the product supports mobile screen readers or an AT matrix predating solid `aria-modal` support.
- **m-3 — `.modal-dialog` is styled `:focus` but can never receive focus.** `modal.css:25-27` defines `.modal-dialog:focus { outline: 3px solid #0066cc; ... }`, while `Modal.jsx:144-149` gives the element no `tabindex`. The rule is unreachable — the CSS declares an intent the markup never fulfils. The consequence that matters: `.modal-dialog` is also the scroll container (`modal.css:20-21`, `max-height:80vh; overflow-y:auto`), so a dialog whose body overflows and contains **no** focusable element cannot be scrolled from the keyboard in browsers without keyboard-focusable scrollers. WCAG 2.1.1. *Mitigated by:* Chrome 127+ and Firefox make scrollable regions keyboard-focusable, and any dialog with a footer action button scrolls incidentally via Tab. **Needs user verification** — concrete check: render this Modal with ~3 screens of plain text and no buttons in the body, open it in Safari, and confirm whether arrow keys/Page Down scroll the body. *Fix*: add `tabindex="-1"` to the dialog container, which both activates the existing focus style and makes the scroll region reachable. **Escalate to MAJOR if** the check fails and the product ships text-only scrolling dialogs.
- **m-4 — The dialog loses its visible boundary in forced-colors / Windows High Contrast mode.** `modal.css:15-17` gives the dialog `background: white` and `box-shadow: 0 4px 16px rgba(0,0,0,0.2)`, and `modal.css:7` gives the scrim `background-color: rgba(0,0,0,0.5)`. In forced-colors mode `box-shadow` is forced to `none` and both backgrounds are forced to system colors, so the dialog and the scrim resolve to the same surface with no separating edge and no shadow. The `1px solid #eee` header rule (`modal.css:35`) survives as `CanvasText`, so the user sees a stray horizontal line rather than a dialog. WCAG 1.4.11 Non-text Contrast; 1.4.1 Use of Color. **Confidence MEDIUM** — I have not rendered this in HCM. *Fix*: `@media (forced-colors: active) { .modal-dialog { border: 1px solid CanvasText; } }`.
- **m-5 — Escape is bound at `document` with no consumption contract.** `Modal.jsx:67` attaches `handleEscape` to `document`. Two consequences: stacked dialogs all close on one Escape press, since every mounted instance has its own document listener; and a custom combobox, date picker, or popover inside the dialog that uses Escape to dismiss itself will also close the whole dialog, discarding the user's work. WCAG 3.2.1-adjacent; cognitive. *Mitigated by:* a consumer's inner `onKeyDown` calling `stopPropagation()` does halt the native event at the React root before it reaches `document` — a real, standard workaround. *Fix*: bind to `modalRef.current` instead of `document`, or check `e.defaultPrevented` before calling `onClose()`.

## Enhancements (best practice not met, no access barrier)

- No `initialFocusRef` API — entry focus is always the first focusable, i.e. always Close. APG permits this, but a form dialog conventionally opens on its first field, and there is no way for a consumer to choose.
- `role="dialog"` is hardcoded at `Modal.jsx:147` with no `role="alertdialog"` option, and no `aria-describedby` hook, so a destructive-confirm consumer cannot reach the APG-correct shape for that case.
- No backdrop-dismissal opt-out. The `mouseDownTarget` guard (`Modal.jsx:120-134`) handles the drag case thoughtfully but a single stray click still discards unsaved input with no confirmation or undo. WCAG 3.3.4-adjacent. Add a `dismissOnBackdropClick={false}` escape hatch for data-entry dialogs.
- Body scroll lock at `Modal.jsx:45`/`Modal.jsx:48` writes `''` on cleanup rather than restoring the prior inline value, so a nested inner dialog closing unlocks the page behind a still-open outer dialog. It also does not compensate for scrollbar width, so the page shifts horizontally on open — a small but real disorientation for magnifier users.
- Wrapping the `✕` at `Modal.jsx:158` in `<span aria-hidden="true">` is belt-and-braces only (the `aria-label` already supersedes it in name computation) but costs nothing and protects against browse-mode text search surfacing a stray glyph.
- `previouslyFocusedElement.current?.focus()` could pass `{ preventScroll: true }` to avoid a jump on restore.

## What's Missing

Restating the Phase 7 absences that carry user impact, in priority order: a visibility/inertness check in the focusable filter (M-1); unique per-instance ARIA ids (M-2); a focus-restoration fallback for detached or body-valued triggers (m-1); `inert` on background content (m-2); `tabindex="-1"` on the dialog container, which both activates already-written CSS and makes the scroll region keyboard-reachable (m-3); a forced-colors boundary (m-4); an Escape-consumption contract (m-5); and a consumer API for initial focus, dialog role, describedby, and backdrop-dismissal opt-out.

Unstated assumptions the code makes and does not encode: **exactly one instance is mounted at a time**, and **`children` contains no `visibility:hidden` or `[inert]` focusables**. Both are load-bearing. Both break quietly.

## Multi-Perspective Notes

- **Screen reader user**: The dialog boundary, name, and modality are announced correctly and in the correct order — `"dialog, Settings, modal"` precedes `"button, Close dialog"` at `step_0002` (digest-only). Semantic structure is clean; `aria-labelledby` resolves; there are no redundant or duplicated announcements, and the `✕` is correctly suppressed by the button's `aria-label`. Two exposures: a second instance misnames the dialog (M-2), and swipe navigation can leave a dialog whose background is not `inert` with no recovery path (m-2).
- **Keyboard-only user**: Tab is confined, Shift+Tab wraps, Escape closes, and focus returns to the trigger — three of those four measured. The focus indicator on the component's own control is visible at 5.56:1. Residuals: wrap anchors can be wrong when a hidden focusable is present, and in one variant Tab dead-ends (M-1); a text-only overflowing body may not be scrollable from the keyboard (m-3); Escape in a nested widget closes the whole dialog (m-5).
- **Low vision user (200% zoom, high contrast)**: Reflow verified at both 200% and 400% — `max-width:500px` / `width:90%` / `max-height:80vh` with internal scroll keeps everything inside the viewport with no horizontal page scroll. Text contrast verified: 12.6:1 for title and body, 5.74:1 for the close glyph. Target size verified at roughly 38×37 CSS px, well over 24×24. The one real gap is forced-colors, where the dialog can lose its boundary entirely (m-4).
- **Cognitive accessibility**: The interaction model is consistent and the dialog is calm — one title, one close control, one content region. The mousedown/click guard shows genuine care about accidental dismissal. The gaps are the ones that guard stops short of: no opt-out for data-entry dialogs, and an Escape binding broad enough to close things the user did not mean to close.

## Verdict Justification

**ACCEPT-WITH-RESERVATIONS**, not ACCEPT, because two MAJOR findings are live: the focusable-set filter (M-1) can silently invalidate the trap's wrap anchors and in one variant dead-ends Tab, and the hardcoded `id` (M-2) gives a stacked dialog the wrong accessible name. Neither is speculative — both are visible in the source and both are outside what the supplied evidence could ever have tested.

Not REVISE, because nothing here blocks shipping under the conditions the evidence actually covers — one instance, simple children, Escape to close — and the underlying APG Modal Dialog pattern is complete rather than 80% complete. The component gets right the things modals usually get wrong.

**Upgrade to ACCEPT** requires: M-1 fixed with a visibility/inertness check plus a post-`focus()` verification that focus actually landed inside the dialog; M-2 fixed with `useId()` plus an empty-`title` guard; and m-1's `isConnected` fallback added, since focus restoration is the component's headline behaviour and it currently has no failure path.

**Downgrade to REVISE** if the "needs user verification" check in m-3 fails and the product ships text-only scrolling dialogs, or if the AT matrix includes mobile screen readers (escalating m-2).

**Recalibrations performed in Phase 8**: m-3 downgraded MAJOR→MINOR (mitigated by Chrome 127+/Firefox focusable scrollers and by any focusable child scrolling incidentally); m-2 downgraded MAJOR→MINOR (mitigated by current AT support for `aria-modal`, by the scrim blocking pointer access, and by the Tab-recovery clause); m-5 downgraded MAJOR→MINOR (mitigated by a working `stopPropagation()` workaround). Four candidate findings were considered and **not filed** as manufactured or unsupported: 2.4.13 focus appearance (contradictory instrument, AAA criterion, wrong elements), 2.5.8 target size (arithmetic clears it), missing landmark (a dialog is not a landmark), and missing `prefers-reduced-motion` (a 0.2s colour fade is not motion).

**Review escalation**: five perspectives at MEDIUM → escalate to `/perspective-audit`, screen reader and keyboard-only first.

**Evidence-quality escalation**: E-1 through E-4 are findings against the evidence pack, not the component. E-1 (the self-contradicting `area_pass`) should go back to the instrument owner before any 2.4.13 claim is made from this trace. E-3 (coverage) is the one that should change the next test run: the trap's stated contract covers eight element classes and the trace exercised one.

**No `A11y Evidence Finding` blocks are emitted.** No finding in this review rests on measured evidence I could re-fetch at its handle — the pack is a digest and the artifact was not supplied — and the block's `fingerprint` field requires a stable computed hash I would have to invent. Per Evidence_Requirements, I am not padding weak provenance into a complete-looking block.

## Open Questions (unscored)

1. **Is more than one `<Modal>` ever mounted simultaneously in this product?** If the answer is a hard no *and* that is enforced somewhere, M-2's severity drops to ENHANCEMENT — but the enforcement should then be visible in the code, not in a convention.
2. **Does the browser/AT support matrix include Safari, and iOS VoiceOver?** Safari governs m-3's real-world severity; iOS VoiceOver governs m-2's.
3. **What is the intended scrolling story for long dialog content?** `max-height:80vh; overflow-y:auto` says the author expects overflow, but nothing was built to make that overflow keyboard-reachable, and the dead `.modal-dialog:focus` rule suggests the design was started and abandoned.
4. **Is Windows High Contrast in scope?** Determines whether m-4 is worth fixing at all.
5. **Was the `.modal-dialog:focus` rule left over from an earlier version that did focus the container?** Git history would resolve this in one command and would tell us whether m-3 is an oversight or a deliberate reversal — I could not check it in this review.
6. **What produced the `area_pass` flapping in E-1?** My hypothesis is a measurement racing paint at mount and unmount, but that is a hypothesis about the instrument, not a conclusion — it needs a re-run with a settle delay to confirm or kill.
