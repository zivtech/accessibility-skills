# Accessibility Design Review — Modal Dialog Component

**Line-number convention:** `Modal.jsx:NN` is numbered from the first line of the JSX fenced block (`import React, { useRef, useEffect } from 'react';` = line 1). `modal.css:NN` is numbered from the first line of the CSS fenced block (`.modal-overlay {` = line 1).

---

## Phase 0 — Evidence Intake

**What was supplied:** one CURATED `a11y-evidence-reader` digest (def_rev 2026-08-26a) over a single artifact — `modal-complete-clean.trace.json`, a `keyboard-a11y-tester` driven-live session, 6 steps, personas `["keyboard","screen-reader"]`, goal "open the settings modal, then close it, verifying focus management", desktop 1280×800.

**Tier and traceability.** Per the protocol, an evidence-reader digest is detector output one tier *below* the artifact it cites — a paraphrase, not the hard evidence. The protocol requires re-fetching at each cited handle (`jq` path / line range) before filing a finding that rests on a digest line. **Under this review's conditions I could not re-fetch any handle.** Therefore:

- **Every evidence-derived statement below is labeled `digest-only`.**
- **No CRITICAL or MAJOR finding in this review rests on a digest line.** The single MAJOR is grounded entirely in the supplied source. The digest is used in the *refuting* direction — to kill candidate findings and to confirm the happy path — which is the safe direction for evidence I cannot re-verify.

**Coverage — this is the load-bearing part of the intake.** The digest's own question named three tool outputs. Only one was supplied:

| Named by the question | Supplied? | Consequence for this review |
|---|---|---|
| keyboard-a11y-tester driven trace | YES (read, query-scoped) | Focus-order evidence available |
| keyboard-a11y-tester batch-crawl findings | NO | No independent finding set |
| axe-core scan | NO | **No machine-detectable evidence at all** |
| driven-session `findings.json` (sibling) | NO | The file that would carry pass/fail markers was never read |

Three of the digest's five observations carry the reader's own **SUBSTITUTION FLAG** — the trace was offered where the a11y-test Verification evidence contract names a different instrument:

- **name-role-state** → contract names `virtual-screen-reader` assertions; what was supplied is keyboard-a11y-tester's *self-reported* AX snapshot.
- **keyboard-operability** → contract names a real-keyboard `npx playwright test` transcript; none supplied.
- **machine-detectable** → contract names axe-core rule-fired/rule-stopped output; what was supplied is the trace tool's incidental per-step `region`/`role` capture.

The reader flagged all three correctly and refused to launder them. That discipline is why this review can trust the digest at all.

**One calibration disagreement with the digest, in the developer's favor.** The reader flagged keyboard-operability as substituted. The protocol's own Phase 0 tiering says `keyboard-a11y-tester` per-step trace facts are *the same tier as codified Playwright runs*. So the missing-Playwright flag is a strictness note about the evidence contract's naming, **not** a downgrade of the keystroke→focus pairing itself. I treat steps 1–6 as hard evidence for focus movement, and I say so rather than double-discounting it.

**A mismatched-evidence-type check was run and passed.** This is a fresh design pass, not a fix verification, so the contract-mismatch gate in Phase 0 does not apply. Had this been offered as proof of a remediation, the substitution flags would themselves have been the first finding.

---

## Phase 1 — Pre-commitment Predictions (written before reading the source)

For a modal dialog, the seven failures I expected:

1. Focus trap absent, or computed once on open from a stale element list.
2. Focus does not restore to the trigger on close, or is dropped to `<body>`.
3. Backdrop click closes the dialog with no keyboard equivalent, and the backdrop is exposed to AT.
4. `role="dialog"` present but `aria-modal` missing, or background content left perceivable.
5. Dialog has no accessible name — missing or broken `aria-labelledby`.
6. Escape handled only while focus is inside the dialog.
7. Icon-only close button with no accessible name.

**Result: five of seven refuted, two survived only in modified form.** Detailed in Phase 10 below. This component is materially better than the category prior.

---

## Phase 2 — Semantic HTML Audit

| Check | Result |
|---|---|
| Native interactive elements | **PASS.** The only interactive control the component owns is a real `<button>` (`Modal.jsx:153-159`). No `div role="button"`. |
| ARIA replacing vs. enhancing semantics | **PASS.** `role="dialog"` / `aria-modal` on a `<div>` (`Modal.jsx:147-148`) is enhancement — there is no native element with modal-dialog semantics available here (`<dialog>` is discussed under Open Questions). |
| Heading hierarchy | `<h2 id="modal-title">` (`Modal.jsx:152`). Single heading, inside a dialog, which is its own context. **No heading-order finding is filed** — see the declined-signals table; the trace captures heading *text* only, never *level*, so heading order is unassessable from the supplied evidence and assessable from source only as "one h2, no siblings to skip." |
| Landmarks | Not applicable to this component's subtree. A dialog is not required to contain a landmark. Page-level landmark structure is outside this component's ownership — it portals to `document.body` (`Modal.jsx:137, 164`) and owns only its own subtree. |
| Lists / tables | None present. Layout is flex, not tables. Correct. |
| Form labels | No form controls owned by the component. |
| Hidden ARIA patching broken HTML | None found. |

Nothing to report at MAJOR from this phase.

---

## Phase 3 — ARIA Pattern Compliance Audit

**Pattern: WAI-ARIA APG Modal Dialog.** Verified attribute by attribute against source:

| APG requirement | Present? | Evidence |
|---|---|---|
| `role="dialog"` on the container | YES | `Modal.jsx:147` |
| `aria-modal="true"` | YES | `Modal.jsx:148` |
| Accessible name via `aria-labelledby` (or `aria-label`) | YES | `Modal.jsx:149` → `Modal.jsx:152` |
| Focus moves into the dialog on open | YES | `Modal.jsx:38-42` |
| Focus is contained while open | YES, with the caveat at M1 | `Modal.jsx:72-116` |
| Escape closes | YES | `Modal.jsx:61-65` |
| Focus returns to the invoking element | YES | `Modal.jsx:50` |
| ARIA values valid | YES | `aria-modal="true"` is a valid boolean string; no `aria-current`/`aria-expanded` misuse anywhere. |

**The pattern is complete, not 80%.** This is the phase where most modals fail, and this one does not. Three specific things I checked and found genuinely right rather than incidentally right:

- **The trap recomputes membership on every Tab** (`Modal.jsx:80`, with the intent stated in the comment at `Modal.jsx:78-79`). The overwhelmingly common bug is a one-shot list captured on open, which goes stale the moment a child is disabled or conditionally rendered. This implementation does not have that bug.
- **The trap has an out-of-dialog recovery branch** (`Modal.jsx:93-97`): if `document.activeElement` has escaped the dialog, the next Tab pulls it back to the correct boundary rather than letting Tab walk into the page behind. Most hand-rolled traps have no such branch. This one materially bounds the blast radius of M2 below.
- **The Escape listener is on `document`, not the dialog** (`Modal.jsx:68`), so Escape works even if focus has slipped outside — and it is in its own effect specifically so an unstable `onClose` identity re-binds only the key listener and never churns the focus save/restore lifecycle (`Modal.jsx:55-57`, `Modal.jsx:69`). That separation is a deliberate, correct design decision, not an accident. It is the difference between a modal whose focus restoration survives a parent re-render and one whose does not.

Corroborated `digest-only` at trace step_0002: `new_phrases` = `["dialog, Settings, modal", "button, Close dialog"]`. The dialog's role, name, and modality all reached the simulated AT in a single announcement when focus entered.

---

## Phase 4 — Focus Management Review

**Measured (`digest-only`, observation 1 — the one observation carrying no substitution flag):**

```
step_0001  Tab      #root > div > button                                      (trigger)
step_0002  Enter    body > div:nth-of-type(2) > div > div:nth-of-type(1) > button   (close, in header)
step_0003  Tab      body > div:nth-of-type(2) > div > div:nth-of-type(2) > button   (body button)
step_0004  Tab      body > div:nth-of-type(2) > div > div:nth-of-type(1) > button   (wrapped to close)
step_0005  Tab      body > div:nth-of-type(2) > div > div:nth-of-type(2) > button
step_0006  Escape   #root > div > button                                      (back to trigger)
```

`focus_moved: true` and `is_body: false` at all 6 steps; no step shows `focus_moved: false`. This measures four distinct behaviors as working: focus enters the dialog on open, the trap cycles, the cycle wraps, and Escape restores focus to the exact pre-dialog trigger.

**Source-level review of what the trace could not exercise:**

- **Initial focus target** (`Modal.jsx:38-42`): first focusable in DOM order = the close button. APG permits this. Deferred one macrotask via `setTimeout(…, 0)` so it survives the portal commit, and guarded by `if (!modalRef.current) return;` so a rapid open→close cannot fire a focus call into a detached tree (React detaches refs during the commit's mutation phase, before the timeout can run). Both the deferral and the guard are correct and deliberate.
- **Zero-focusable branch** (`Modal.jsx:81-84`): unreachable in practice, since the close button always renders. Defensive, harmless — but see E1: it is the branch that would benefit from the container fallback the CSS already anticipates.
- **Tab order** matches visual order: header (title, then close) precedes body. Reading order and DOM order agree.
- **Sticky-element obstruction (2.4.11):** `.modal-header` has **no** `position: sticky` (`modal.css:30-36`). The dialog scrolls as a whole (`modal.css:19-20`), so a focused element scrolled into view is not overlapped by a pinned header. This is a very common modal defect and it is absent here. Checked, clean.
- **Keyboard scrolling of the internal scroll region:** `.modal-dialog` is the scroll container (`modal.css:19-20`) and the close button is its descendant. Arrow keys pressed with the close button focused scroll the nearest scrollable ancestor — which is `.modal-dialog`. So a long modal is keyboard-scrollable in all browsers, including Safari, without needing `tabindex="0"` on the scroller. This trap is avoided *because* of where the close button sits. Checked, clean.
- **Async-CRUD deferred focus:** the component owns no async operations. Out of scope for the component; see M5 for the API-shaped residue.

The one real gap from this phase is M1.

---

## Phase 5 — State Communication Audit

The component has **no toggling state to communicate**. There is no loading state, no error state, no selection, no expand/collapse, no disabled/readonly. The dialog's open/closed condition is communicated the way the APG Modal Dialog pattern prescribes: by the dialog's presence in the accessibility tree plus focus movement into it — **not** by an ARIA state attribute on the trigger.

This matters, because the evidence pack contains a signal that looks exactly like a state-communication failure and is not one. See T3 in the declined-signals table.

- No `aria-live` region: **correctly absent**, not a gap. There is nothing asynchronous to announce. Adding one would be manufactured.
- `aria-modal="true"` is a property, not a state, and is static — correct.
- Symbol-as-state check (`✕`, `Modal.jsx:158`): the button carries `aria-label="Close dialog"` (`Modal.jsx:156`), which wins the accessible-name computation over text content. Measured `digest-only` at step_0002: `"button, Close dialog"`. The name is right. The residual is E2, at ENHANCEMENT, not MAJOR.

---

## Phase 6 — Multi-Perspective Review

### Perspective Alarm Levels

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | MEDIUM | Hand-rolled name wiring with a hardcoded element id; portal to `document.body` outside the app root; `aria-modal` is the sole background-suppression mechanism |
| Keyboard-only | **HIGH** | Hand-rolled focus trap with a hand-maintained focusable-element predicate — M1 lives here |
| Low vision | MEDIUM | Forced-colors mode erases the dialog boundary; the trace's focus-appearance measurement is internally self-contradictory and resolves nothing |
| Cognitive | MEDIUM | Three unconditional dismissal paths, no dirty-state guard, no consumer opt-out |
| Vestibular & motion | LOW | No transform, no entrance/exit animation, no parallax, no autoplay — only a 200ms `color` transition (`modal.css:51`), which is not motion |
| Auditory access | LOW | No media elements owned by the component |
| Environmental contrast | MEDIUM | Same forced-colors boundary loss; no measured contrast available (no axe artifact supplied) |

Keyboard-only at HIGH and the four MEDIUMs should be escalated to `/perspective-audit` if this component is going into a design system. The HIGH is the one that matters: a hand-rolled trap is precisely the artifact class that deserves an independent pass.

### Per-perspective notes

**Screen reader user.** The dialog announces as "dialog, Settings, modal" on entry and the close button as "button, Close dialog" (`digest-only`, step_0002). Relationships resolve: `aria-labelledby="modal-title"` → `id="modal-title"` → the `<h2>` text. Reading order matches DOM order matches visual order. Background suppression relies entirely on `aria-modal="true"`; the page behind is not `inert` and its elements are not `aria-hidden`. That is the APG-sanctioned approach and modern NVDA/JAWS/VoiceOver honor it, so this is not a finding — but see E4.

**Keyboard-only user.** Tab and Shift+Tab cycle; Escape dismisses from anywhere; focus enters on open and returns to the trigger on close — all measured. The backdrop is not focusable and needs no keyboard equivalent because Escape *is* the equivalent (measured working at step_0006). The exposure is M1: for modal content containing laid-out-but-unfocusable elements, a wrap anchor can be an element `.focus()` cannot reach, and Tab goes dead at that boundary.

**Low vision user (200% zoom, high contrast, magnifier).** Reflow is genuinely good: `max-width: 500px; width: 90%` (`modal.css:17-18`) at a 320 CSS px viewport yields a 288px dialog with 20px padding — no horizontal scroll, no clipping, and `max-height: 80vh` with `overflow-y: auto` (`modal.css:19-20`) means over-tall content scrolls rather than being cut off. Focus indicators are explicit rather than UA-default: `2px solid #0066cc` with `outline-offset: 2px` on the close button (`modal.css:58-62`). Using `:focus` rather than `:focus-visible` means the indicator appears regardless of input modality — safer, not a defect. Contrast, estimated from hex and **not measured** (no axe artifact): `#333` on white ≈ 12.6:1, `#666` on white ≈ 5.7:1 at 24px, `#0066cc` outline on white ≈ 5.6:1 — all comfortably above threshold; the trace reports `focus_appearance.contrast_pass: true` at all 6 steps (`digest-only`). The genuine gap is M4, forced-colors.

**Cognitive accessibility.** Three redundant dismissal paths (close button, Escape, backdrop) is good for discoverability. The backdrop handler is notably thoughtful: `handleOverlayMouseDown` records the mousedown target (`Modal.jsx:120-122`) and `handleOverlayClick` fires only when the interaction *both started and ended* on the backdrop (`Modal.jsx:124-135`). That kills the two classic accidental dismissals — a click that begins inside the dialog and drifts out, and a text-selection drag that releases on the backdrop. For a user with a tremor or an imprecise pointer, that guard is the difference between keeping and losing their work. It is the single most considered line of code in this file. The residue is E5: there is still no consumer opt-out for form-bearing modals.

**Vestibular & motion.** Nothing to suppress. No `@media (prefers-reduced-motion)` block exists and none is needed — a `color` transition is not motion. Not a finding.

**Auditory access.** No `<video>`, no `<audio>`, no auditory alerts. LOW, genuinely not applicable.

**Environmental contrast.** Covered under low vision; forced-colors is M4.

---

## Evidence Signals Checked and NOT Filed

The supplied evidence pack contains six signals that a checklist-driven read would file as findings. Each is wrong. Naming them is the highest-value output of this review, because filing any one of them would be a false alarm against correct code.

| # | Signal in the pack | Why it is NOT a finding |
|---|---|---|
| **T1** | `region.landmark` is `null` at all 6 steps, including the 4 steps recorded inside the dialog | This is the trace tool's **incidental** per-step region capture, not a landmark audit — the digest flags it as such and states no axe artifact was read. A dialog is not required to contain a landmark, and page-level landmark structure is not this component's to own. Filing "missing landmarks" here would be inventing a machine-detectable determination from a field that makes none. |
| **T2** | `ax_name_role_state.role` is `"button"` at all 6 steps; a query for non-button roles returns `[]`; the dialog container is never the active element | The field records the role of the **active element**, and the active element is a button at every step by construction. It is not an inventory of roles present. `role="dialog"` is verified in source at `Modal.jsx:147` and reached the AT — step_0002's announcement phrase is literally `"dialog, Settings, modal"`. |
| **T3** | `states` is static `{"invalid":"false","focusable":true,"focused":true}` across the whole trace; a whole-file grep for `expanded\|haspopup\|aria-` returns nothing | **This is the correct expected result, not a defect.** A modal dialog trigger is a plain button — `aria-expanded` belongs to the Disclosure pattern, not the Modal Dialog pattern. There is no toggling ARIA state in this component for the trace to capture. A reviewer filing "ARIA state changes with no announcement" would be demanding an attribute the APG says must not be there. |
| **T4** | `focus_appearance.area_pass` / `aaa_pass` are `false` at step_0003 and step_0006 | Three independent reasons. (a) **The measurement contradicts itself inside one trace**: the same "Save changes" selector is `area_pass:false` at step_0003 and `true` at step_0005; the same trigger selector is `true` at step_0001 and `false` at step_0006. Same element, same CSS, same session, opposite verdicts — that is instrument non-determinism, and it means the field certifies nothing in either direction. (b) `area_pass`/`aaa_pass` map to **WCAG 2.4.13 Focus Appearance, which is Level AAA** — above the WCAG 2.2 AA target. (c) The **AA** criterion, 2.4.7 Focus Visible, is satisfied: `focus_visible.visible` and `contrast_pass` are `true` at all 6 steps, and the source provides explicit `:focus` outlines (`modal.css:25-28, 58-62`). Filing a MAJOR here would convert a broken gauge into a defect report. |
| **T5** | `role="presentation"` on a `<div>` carrying an `onClick` (`Modal.jsx:138-143`) — the classic `jsx-a11y/no-noninteractive-element-interactions` shape | Not a 2.1.1 failure: backdrop dismissal is a redundant pointer convenience whose keyboard equivalent is Escape, which exists (`Modal.jsx:61-65`) and is **measured working** (step_0006). The div is not focusable and carries no other ARIA, so `presentation-role-conflict` should not fire either — flagged as an *expectation*, since no axe artifact was read. One correction to the fixture's own claim below. |
| **T6** | "No fail/violation/warning/error/defect/issue marker anywhere in the trace" | **Weak positive evidence, not a clean bill of health.** Nothing establishes that the driven mode emits such markers at all, and the sibling `findings.json` — the file that would actually carry them — was explicitly not supplied. Absence of a marker in a file that may never emit markers is not evidence of absence of defects. |

**Correction to the fixture's stated feature list.** The claim "✓ Backdrop not exposed to AT (`role="presentation"`)" overstates what the attribute does. A bare `<div>` has no semantics to remove, so `role="presentation"` is a near no-op here, and it does **not** hide the page behind the overlay — `aria-modal="true"` is what does that. The attribute is harmless and the *outcome* claimed is true; the stated mechanism is not. Worth correcting because a future maintainer could delete `aria-modal` believing the backdrop role is carrying the suppression.

---

## Phase 7 — Gap Analysis (What's Absent)

Run against the full gap checklist. Absent-and-should-be-present:

- Fallback focus-return target when the trigger no longer exists → **M5**
- Unique-per-instance id generation for the label association → **M3**
- `@media (forced-colors: active)` boundary declaration → **M4**
- `tabindex="-1"` on the dialog container to match the `:focus` style the CSS already declares → **E1**
- Reference-counted scroll lock (`document.body.style.overflow` is set and cleared unconditionally at `Modal.jsx:45` and `Modal.jsx:48`; a nested modal's close re-enables background scroll while the outer modal is still open) → noted below, not filed separately
- Consumer-side dismissal veto for form-bearing content → **E5**
- Non-empty-`title` guard → **E3**

Absent-and-correctly-absent (checked so the record shows they were considered, not skipped): `aria-live` region; `aria-busy`; `prefers-reduced-motion` block; caption/transcript infrastructure; skip link; `aria-current`; `autocomplete` attributes; dragging alternative; `role="alertdialog"`; `lang` attributes. None of these apply to a generic dialog shell that owns no async state, no media, no navigation, and no form fields.

---

# VERDICT: ACCEPT-WITH-RESERVATIONS

**Overall Assessment**: This is a genuinely well-built modal — the WAI-ARIA Modal Dialog pattern is complete rather than the usual 80%, and three of its design decisions (recomputing the focusable set on every Tab, the out-of-dialog focus recovery branch, isolating the Escape listener from the focus lifecycle) are choices most hand-rolled traps get wrong. The measured trace confirms the full happy path: focus enters on open, cycles, wraps, and returns to the exact trigger on Escape. The one MAJOR is latent rather than active — the focusable-element predicate is wrong for content classes the fixture's own trace never exercised — and the remaining findings are cheap. Five of my seven pre-commitment predictions were refuted outright.

**Pre-commitment Predictions vs. Reality**:

| # | Predicted | Actual |
|---|---|---|
| 1 | Trap absent or computed from a stale one-shot list | **Refuted, and then some.** Recomputed on every Tab (`Modal.jsx:80`). But the *membership rule* is wrong — this is where M1 came from. I predicted the right area for the wrong reason. |
| 2 | Focus not restored to trigger | **Refuted by measurement** (step_0006). The theoretical React-16 concern about synchronous focus in an unmount cleanup is contradicted by the trace. Residual is M5, a different gap than predicted. |
| 3 | Backdrop clickable with no keyboard equivalent, exposed to AT | **Refuted.** Escape is the equivalent and is measured working; backdrop is `role="presentation"` and unfocusable; dismissal is additionally guarded against drag-release (`Modal.jsx:124-135`). |
| 4 | `aria-modal` missing | **Refuted** (`Modal.jsx:148`). |
| 5 | No accessible name | **Refuted in the happy path** (measured "dialog, Settings, modal"). Survived only as the ID-collision variant, M3. |
| 6 | Escape only works with focus inside | **Refuted** — listener is on `document` (`Modal.jsx:68`), deliberately. |
| 7 | Icon close button with no name | **Refuted** (`Modal.jsx:156`, measured "button, Close dialog"). |

**Was I surprised?** Yes, twice. First by the out-of-dialog recovery branch — I have not seen that in a hand-rolled trap before, and it is what demotes M2 from MAJOR to MINOR. Second by the mousedown/click pairing on the backdrop, which solves an accidental-dismissal problem most production modals still have. What I did *not* predict, and should have, is that a carefully-written focusable-element predicate can be wrong in both directions at once.

---

## Critical Findings (blocks access)

**None.** No user category is blocked. Screen reader users get a correctly named, correctly roled, correctly modal dialog. Keyboard users can enter it, cycle it, and leave it — all measured. Saying so is a real result, not a courtesy: a clean bill of health on the CRITICAL tier is the signal the developer is paying for.

---

## Major Findings (significantly degrades experience)

### M1 — The focusable-element predicate admits elements that cannot receive focus, which makes Tab go dead at a wrap boundary

**Evidence:** `Modal.jsx:20-25` (the predicate) consumed at `Modal.jsx:80, 86-88, 93-97, 99-111`.

```js
const getFocusableElements = (container) =>
  Array.from(container.querySelectorAll(FOCUSABLE_SELECTOR)).filter(
    // display:none elements produce no client rects and cannot take
    // focus, so they must not become wrap anchors.
    (el) => el.getClientRects().length > 0
  );
```

The comment states the intent exactly right — non-focusable elements must not become wrap anchors — and `getClientRects()` delivers only part of it. `display: none` generates no box, so it is correctly excluded. But **two other classes of element generate boxes and still cannot take focus**:

1. **`visibility: hidden`.** Visibility affects painting, not box generation, so `getClientRects().length > 0` is true — yet the element is not focusable and `.focus()` on it is a no-op. The protocol's own gap list names this exact CSS pattern as a common real-world shape (`opacity: 0; visibility: hidden` reveal-on-hover controls).
2. **Anything inside an `[inert]` subtree.** Inert content is laid out and boxed, but the HTML spec makes it unfocusable and `.focus()` a no-op. React 19 exposes `inert` as a first-class prop, so this is becoming more common inside modal content, not less.

**The failure mechanism.** When such an element lands at position `[0]` or `[length-1]`, it becomes `firstElement` or `lastElement` (`Modal.jsx:86-88`). The handler then calls `e.preventDefault()` **and then** `.focus()` on it (`Modal.jsx:96, 101-102, 107-108`). The preventDefault lands; the focus call does nothing. Net result: **the browser's own Tab was cancelled and nothing replaced it — focus does not move at all.** From the user's seat, Tab or Shift+Tab is simply dead at that boundary, with no indication why, and any dialog content past the phantom anchor is unreachable.

- **User group:** keyboard-only and screen reader users. Both.
- **WCAG:** 2.1.1 Keyboard (content operable via keyboard) and 2.4.3 Focus Order. Not 2.1.2 No Keyboard Trap — Escape still exits the dialog, so the user is not permanently trapped; they simply cannot reach part of the dialog.
- **Confidence: HIGH** on the mechanism (this is specified browser behavior, not a guess). **MEDIUM** on real-world frequency — it depends entirely on what a consumer passes as `children`.
- **Could the developer refute this?** No. They can scope it ("our modals never contain such content"), but that is a usage claim about every future consumer of a shared component, not a refutation of the mechanism.
- **Does the supplied evidence show it?** No — and I want that stated plainly. The trace exercised two plain visible buttons; steps 3–5 show the cycle working correctly. **This finding is source-read, not measured**, and no `digest-only` line supports or contradicts it.

**Realist Check (all four questions):** Worst realistic case is a keyboard user unable to reach a control inside a dialog, with Tab silently doing nothing — not a minor inconvenience, and Escape (the only escape hatch) discards whatever they were doing. Impacted group is two full user categories. Detection is **silent**: axe cannot see it, and the existing driven trace does not catch it because it depends on content the trace never loaded — this is days-to-never, discovered by a user report. Severity is not inflated by review momentum; it is the only MAJOR I am filing on a component where I refuted five of my own seven predictions. **MAJOR survives all four questions.**

**Fix.** Replace the rect heuristic with an actual focusability test, and verify the focus call landed:

```js
const isFocusable = (el) =>
  el.getClientRects().length > 0 &&
  !el.closest('[inert]') &&
  getComputedStyle(el).visibility !== 'hidden';
```

Modern equivalent, one call: `el.checkVisibility({ visibilityProperty: true, contentVisibilityAuto: true })` plus the `[inert]` ancestor check. Belt-and-braces at the call sites (`Modal.jsx:96, 101-102, 107-108`): after `.focus()`, confirm `document.activeElement` actually changed, and walk to the next candidate if it did not. That single guard makes the trap correct against every current and future non-focusable class without maintaining a taxonomy of them.

**No `A11y Evidence Finding` block is attached to this finding.** The block is for findings backed by measured evidence; this one is source-read, and inventing a `fingerprint` or a `reproduction_steps` command to make the block look complete would be fabrication of exactly the kind the evidence contract exists to prevent.

---

## Minor Findings (friction, workaround exists)

### M2 — The enumerated focusable set omits several genuinely tabbable element types

**Evidence:** `Modal.jsx:7-18` (`FOCUSABLE_SELECTOR`).

The list is unusually thorough — it covers `area[href]`, `audio[controls]`, `video[controls]`, and `[contenteditable]`, which most implementations miss. It nevertheless omits element types that browsers place in the tab order:

- **`<summary>`** (the first summary child of a `<details>`) is focusable and tabbable by default and matches none of the ten selectors. `<details>` disclosures inside modal bodies are ordinary content.
- **`<iframe>`** participates in the tab order in every major browser. Worse: keyboard events inside an iframe's document never reach the parent's `document` listener, so the trap does not merely mis-anchor — it does not run at all while focus is inside.
- **`<embed>` / `<object>`** — same class, less common.
- **Radio groups**: only the checked radio in a group is tabbable, but the selector admits all of them, so `lastElement` can be an unchecked radio the user's Tab never actually reaches.

**Effect:** the computed wrap anchors are wrong, so Tab from the *true* last tabbable element falls through the handler (`Modal.jsx:105-111`, since `activeElement !== lastElement`) and the browser moves focus into the page behind an `aria-modal` dialog — content the screen reader has been told does not exist.

**Mitigated by:** the out-of-dialog recovery branch at `Modal.jsx:93-97`. The leak is **one keystroke deep and self-healing** — the next Tab detects that focus is outside the container and pulls it back to the correct boundary. That branch is why this is MINOR and not a second MAJOR; without it this would be a straightforward trap escape.

**Scope caveat, stated honestly:** the fixture's Expected Behavior enumerates the same set the code implements, so this is arguably a *specification* gap rather than an implementation bug — the spec says "every tabbable element inside the dialog" and then enumerates a list that is not every tabbable element. The developer can legitimately answer "scoped deliberately." That answer belongs in the spec text, not in silence. **Confidence: MEDIUM.** WCAG 2.4.3 Focus Order.

**Fix.** Add `details > summary:first-of-type`, `details`, `iframe`, `embed`, `object` to `FOCUSABLE_SELECTOR`; handle radio groups by keeping only the checked member (or the first, if none is checked). Or adopt the `tabbable` package and stop maintaining the taxonomy by hand — which also resolves M1.

### M3 — `id="modal-title"` is hardcoded, so the label association collides across simultaneously-open dialogs

**Evidence:** `Modal.jsx:149` (`aria-labelledby="modal-title"`) → `Modal.jsx:152` (`<h2 id="modal-title">`).

Every instance portals to `document.body` (`Modal.jsx:137, 164`) with the same literal id. `if (!isOpen) return null` (`Modal.jsx:118`) means closed modals contribute nothing, so a collision requires **two dialogs open at once** — stacked confirmations, or a cross-fade where one is still mounted as the next opens. When that happens, `aria-labelledby` resolves to the **first** matching id in document order, so the foreground dialog is announced with the background dialog's title.

- **User group:** screen reader users only.
- **Why it matters:** in the highest-stakes case — a "Confirm delete" opened from inside "Edit profile" — the destructive dialog announces itself with the parent's benign title. The user is reading the wrong context at the moment they are about to make an irreversible choice.
- **Why MINOR and not MAJOR:** the heading text is still present and readable with the virtual cursor, and all controls remain correctly named and reachable. The user is misled, not blocked — there is a workaround (read the heading). It escalates in a destructive-confirmation flow, and the team should decide whether their product has that flow.
- **Detection:** silent. `duplicate-id-aria` would only fire if a scan happened to run with two dialogs open.
- **WCAG:** 4.1.2 Name, Role, Value; 1.3.1 Info and Relationships. **Confidence: HIGH.**

**Fix.** One line: `const titleId = useId();` then `aria-labelledby={titleId}` and `id={titleId}`. (React <18: any per-instance counter or `useRef` seed.)

### M4 — In forced-colors mode the dialog loses its visible boundary

**Evidence:** `modal.css:14-23` (`background: white`, `box-shadow: 0 4px 16px rgba(0,0,0,0.2)`) and `modal.css:1-12` (`background-color: rgba(0,0,0,0.5)`). No `@media (forced-colors: active)` block exists anywhere in the stylesheet.

In Windows High Contrast / forced-colors mode the UA forces `background-color` to system colors and forces `box-shadow` to `none`. Both the dim backdrop and the white dialog become Canvas, and the drop shadow disappears. The two visual cues that say "this is a dialog floating above the page" are the *only* two cues, and both are erased. The result is the title, the header divider (which survives — `border-color` is forced to CanvasText, `modal.css:35`), the ✕ and the body content floating on a full-screen Canvas with no container edge.

- **User group:** low vision users in forced-colors mode.
- **Impact:** content stays readable and every control stays operable — the dialog's *boundary*, not its content, is lost. Genuinely MINOR, and genuinely worth fixing.
- **WCAG:** 1.4.11 Non-text Contrast is the design rationale (UI component boundary), though forced-colors mode guarantees contrast by construction so this is not a clean 1.4.11 failure; the operative check is the protocol's environmental-contrast question, "does the interface function in forced-colors mode without losing information?"
- **Not measured.** No forced-colors screenshot or scan was supplied; this is source-read. **Confidence: HIGH** on the CSS forcing behavior, **MEDIUM** on how much the boundary loss actually costs a given user.

**Fix.**
```css
@media (forced-colors: active) {
  .modal-dialog { border: 1px solid CanvasText; }
}
```

### M5 — Focus restoration has no fallback when the previously-focused element is gone

**Evidence:** `Modal.jsx:35` (capture) and `Modal.jsx:50` (`previouslyFocusedElement.current?.focus();`).

The optional chain guards against `null`, not against **detached**. Calling `.focus()` on an element no longer in the document is a silent no-op, and focus falls to `<body>`. A screen reader user is then dumped at the top of the document with no announcement, having to re-navigate to where they were.

The realistic trigger is the single most common modal flow there is: a per-row "Delete" button opens a confirmation modal; the user confirms; the row unmounts; the modal closes; the trigger no longer exists. This is exactly the deferred-focus-after-async-CRUD case in the protocol's focus checklist, seen from the component-API side.

- **User group:** screen reader and keyboard users.
- **Why MINOR:** it fires only on flows that destroy the trigger, and the consumer *can* work around it by managing focus themselves — but nothing in the component's API tells them they need to.
- **WCAG:** 2.4.3 Focus Order. **Confidence: HIGH** on the mechanism, MEDIUM on frequency in this codebase.

**Fix.** Verify and fall back:
```js
const prev = previouslyFocusedElement.current;
if (prev?.isConnected) prev.focus();
else fallbackRef?.current?.focus?.();
```
and expose an optional `returnFocusTo` prop so a consumer whose flow destroys the trigger can name the replacement (typically the list container or the heading above it) rather than losing focus to `<body>`.

---

## Enhancements (best practice not met, no access barrier)

**E1 — `.modal-dialog:focus` is dead CSS; wire the container fallback the stylesheet already anticipates.** `modal.css:25-28` declares `outline: 3px solid #0066cc` for `.modal-dialog:focus`, but the container has no `tabindex="-1"` (`Modal.jsx:144-150`), so it can never receive focus and the rule can never apply. Corroborated across three sources: the CSS declares the intent, the JSX never wires it, and the trace confirms the dialog container is never the active element at any step (`digest-only`, observation 5). Someone designed a container-focus fallback and it was not finished. Adding `tabindex="-1"` costs one attribute, activates the existing style, and gives the zero-focusable branch at `Modal.jsx:81-84` somewhere to put focus instead of leaving it outside the dialog with Tab suppressed.

**E2 — Wrap the `✕` glyph in `aria-hidden="true"`.** `Modal.jsx:158`. The accessible name is correct today — `aria-label` (`Modal.jsx:156`) wins the name computation, and step_0002 measures `"button, Close dialog"` (`digest-only`). This is defense-in-depth for contexts that read text content rather than the accessible name (braille rendering, some text-search and verbose reading modes), and U+2715 MULTIPLICATION X has no reliable speech mapping. The protocol's symbol rule calls for the wrapper whenever the state is already communicated programmatically. Filing this above ENHANCEMENT would be manufacturing a violation against measured-correct output.

**E3 — Guard the `title` prop.** `Modal.jsx:152` renders `{title}` with no default and no validation. An undefined or empty `title` yields an empty `<h2>`, and `aria-labelledby` pointing at empty text leaves the dialog with **no accessible name** (WCAG 4.1.2) — a genuine failure, reached only through a caller mistake. Add a required-prop assertion, or fall back to `aria-label="Dialog"` when `title` is empty so the failure degrades instead of disappearing.

**E4 — Consider `inert` on the app root as belt-and-braces alongside `aria-modal`.** `aria-modal="true"` (`Modal.jsx:148`) is the APG-sanctioned mechanism and modern AT honors it, so this is not a defect. The APG itself notes that authors may still wish to neutralize background content, and `inert` on `#root` while a dialog is open additionally blocks background focus from routes the Tab handler cannot see — browser find-in-page, autofill dropdowns, and (per M2) iframe content. It also makes the fixture's "backdrop not exposed to AT" claim true by mechanism rather than by coincidence.

**E5 — Give consumers a dismissal veto for form-bearing modals.** Escape (`Modal.jsx:61-65`) and backdrop click (`Modal.jsx:124-135`) both call `onClose()` unconditionally, with no dirty-state check and no opt-out. A stray click or keypress discards a half-filled form with no confirmation and no undo. The mousedown/click pairing already prevents the two *accidental* cases, which is why this is only an ENHANCEMENT — but a deliberate misfire is still unrecoverable. WCAG 3.3.4 Error Prevention applies **only** if the modal's content is legal, financial, or data-deleting; it does not apply to a generic informational dialog, and I am not claiming otherwise. Suggested shape: a `closeOnBackdropClick` boolean and/or an `onRequestClose` the consumer can decline.

---

## What's Missing (gaps, edge cases, unstated assumptions)

- **Reference-counted scroll lock.** `document.body.style.overflow` is set to `'hidden'` (`Modal.jsx:45`) and cleared to `''` (`Modal.jsx:48`) unconditionally. Two stacked modals: the inner one's cleanup unlocks background scroll while the outer is still open, and the background scrolls behind an open dialog. Low accessibility weight on its own, but it is the same stacked-modal assumption that produces M3 — the component assumes single-instance and three separate mechanisms quietly depend on that.
- **Shadow DOM inside modal content.** `querySelectorAll` does not pierce shadow roots (`Modal.jsx:21`). A focusable inside a web component's shadow tree is invisible to the trap, and `document.activeElement` reports the host. The containment check at `Modal.jsx:93` still passes (the host is contained), so the recovery branch does not fire and focus can walk out. Moved to Open Questions — I cannot verify whether this stack uses shadow-DOM components.
- **No stated contract for what `children` may contain.** M1, M2, E5, and the shadow-DOM case are all the same underlying gap: this is a general-purpose container with an unstated content contract. Whatever the team decides about M1/M2, the answer belongs in the component's documented API, not in tribal knowledge.
- **No axe-core evidence at any point in this review.** Every machine-detectable claim above (roles, names, labels, heading order, contrast) is source-read or estimated. The digest states plainly that no axe artifact was supplied and that heading *level* is not captured by the trace at all. A single axe run against the harness page would convert about a third of this review from reasoning to measurement.
- **No real-AT verification.** Everything AT-side here is a simulated announcement from one tool's self-reported AX snapshot, flagged by the reader as a substitution for the `virtual-screen-reader` assertions the evidence contract names. `aria-modal` background suppression in particular — the mechanism the whole design leans on — has never been verified against a real screen reader in this evidence set.

---

## Multi-Perspective Notes

- **Screen reader user:** Enters a correctly named, correctly roled, correctly modal dialog and hears "dialog, Settings, modal" followed by "button, Close dialog" — measured. Semantic structure is clear, relationships resolve, reading order matches DOM order. Two residual exposures: the wrong dialog title if two dialogs are ever open at once (M3), and a one-keystroke excursion into `aria-modal`-suppressed background content for certain child element types (M2). Background suppression rests entirely on `aria-modal` and has never been checked against a real AT.
- **Keyboard-only user:** Fully operable on the measured path — enter, cycle, wrap, Escape, restore. Three redundant dismissal paths. Explicit focus indicators rather than UA defaults, applied on `:focus` so they show regardless of input modality. The exposure is M1: for content containing `visibility: hidden` or `[inert]` focusable-looking elements, Tab goes dead at a wrap boundary with no feedback and later dialog content becomes unreachable.
- **Low vision user (200% zoom, high contrast):** Reflow is genuinely well handled — `width: 90%; max-width: 500px` plus `max-height: 80vh; overflow-y: auto` means no horizontal scroll and no clipping at 320 CSS px, and the internal scroll region is keyboard-scrollable because the close button lives inside it. Estimated contrast is comfortable throughout (12.6:1 body text, 5.7:1 close glyph, 5.6:1 focus outline — hex-derived, not measured), and the trace reports `contrast_pass: true` at every step. The `area_pass` failures in the trace are an unreliable gauge against an AAA criterion and were not filed. The real gap is forced-colors mode (M4), where the dialog's boundary vanishes entirely.
- **Cognitive accessibility:** Calm, uncluttered, one clear title and one clear close affordance. No timeouts. The interaction model is consistent and offers three ways out. The mousedown/click pairing on the backdrop is a real cognitive and motor-accessibility win — it prevents the two classic ways a user loses their work to a stray pointer gesture. The residue is that no dismissal path can be vetoed by the consumer (E5), so a deliberate misfire on a form-bearing modal is still unrecoverable.

---

## Verdict Justification

**ACCEPT-WITH-RESERVATIONS**, and the reservations are narrow and cheap.

Why not **ACCEPT**: M1 is a real defect in the focus trap's central predicate, against the predicate's own stated intent, in a general-purpose component whose `children` are arbitrary. It fails silently, no automated tool detects it, and the supplied trace cannot detect it because it depends on content the trace never loaded. A clean ACCEPT would tell the team the trap is correct for any content, and it is not.

Why not **REVISE**: nothing here blocks shipping this component for the content it currently carries. The APG Modal Dialog pattern is complete. The entire happy path is measured working. Five of my seven pre-commitment predictions were refuted outright, and the two survivors survived in weaker forms than predicted. M1 is latent, and M2–M5 are one-to-three-line fixes.

**Path to ACCEPT:** fix M1 (replace the rect heuristic with a real focusability test and verify the focus call landed), fix M3 (`useId()`), and resolve M2 either by extending the selector or by writing the scope limit into the component's documented contract. M4, M5, and the enhancements are hygiene.

**Recalibrations performed under Phase 8 (Realist Check) and Phase 9 (Self-Audit):**

- **M2 downgraded MAJOR → MINOR.** *Mitigated by:* the out-of-dialog recovery branch at `Modal.jsx:93-97`, which bounds the focus leak to a single keystroke and self-heals on the next Tab. Additionally the developer can legitimately answer "deliberately scoped" — Phase 9's refutability test — so it is presented at MEDIUM confidence with the scope question stated.
- **M3 downgraded MAJOR → MINOR.** *Mitigated by:* the heading text remaining present and readable via the virtual cursor and all controls remaining correctly named, so the user is misled rather than blocked; and by the collision requiring two simultaneously-open dialogs, which not every product has.
- **E5 downgraded MINOR → ENHANCEMENT.** *Mitigated by:* the existing mousedown/click pairing already preventing the two common accidental dismissals; the residual requires a deliberate misfire. Also partly a design preference under Phase 9, since unconditional Escape-to-close is APG-mandated behavior.
- **E2 held at ENHANCEMENT rather than raised.** The protocol's symbol rule as written would support filing it, but the accessible name is measured correct. Raising it would be a manufactured violation against working output.
- **M1 held at MAJOR.** Survived all four Realist Check questions: significant degradation (not inconvenience), two full user categories, silent detection, and it is the only MAJOR filed in a review that refuted most of its own priors — so it is not the product of review momentum.
- **T1–T6 declined entirely.** Six evidence signals that pattern-match to findings and are not findings. Two of them (T3, T4) would have been MAJOR-shaped false alarms against correct code.

**Escalation:** Keyboard-only is at HIGH alarm and should go to `/perspective-audit` before this ships as a shared component — a hand-rolled focus trap is exactly the artifact class that earns an independent pass. Screen reader, low vision, cognitive, and environmental contrast are at MEDIUM.

**Evidence caveat carried into the verdict:** this verdict rests on one artifact, read through a digest I could not re-fetch, with three of five observations carrying substitution flags and no axe-core or real-AT evidence anywhere. The measured happy path is solid. The unmeasured surface — background suppression under a real screen reader, forced-colors rendering, heading level, machine-detectable name/role/label determinations — is entirely unexamined by measurement, and this verdict does not claim otherwise.

---

## Open Questions (unscored)

1. **Do any modals in this codebase stack?** M3's severity turns entirely on this. If a confirmation dialog can ever open from inside another dialog, M3 becomes MAJOR and the scroll-lock counter becomes a real bug rather than a note.
2. **Does modal content ever include shadow-DOM components?** `querySelectorAll` (`Modal.jsx:21`) does not pierce shadow roots, and the containment check at `Modal.jsx:93` passes for a shadow host, so the recovery branch would not fire. LOW confidence, unverifiable from what was supplied — hence Open Question rather than a finding.
3. **Was `<dialog>` with `showModal()` evaluated and rejected?** The native element provides the focus trap, background inertness, Escape handling, and top-layer stacking for free — and would eliminate M1, M2, and the scroll-lock issue outright. There may be a good reason (styling control, `::backdrop` support at the time, framework integration). If there is, it belongs in a comment. If there is not, it is worth revisiting. Raised as a question, not a finding — a working ARIA implementation is not a violation of the native-HTML-first rule when the native element's constraints were genuinely weighed.
4. **Is the `focus_appearance.area_pass` instability a known instrument issue?** The same element yields opposite verdicts at steps 3 and 5 within one session. Worth a bug against the tool independently of this component, since anyone else consuming that field will hit the same contradiction.
5. **Would the unsupplied artifacts change anything?** The sibling `findings.json`, the batch-crawl findings, and the axe-core scan were all named by the digest's question and none was supplied. The axe scan in particular is a five-minute run that would convert several source-read statements in this review into measured ones.
6. **What is the intended content contract for `children`?** M1, M2, E5, and question 2 are four faces of one unstated assumption. Whatever the answer, writing it down is the fix that prevents the next four.
