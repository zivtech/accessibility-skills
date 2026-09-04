**VERDICT: REJECT**

**Overall Assessment**: This component advertises the WAI-ARIA Select-Only Combobox / collapsed-Listbox contract (`aria-haspopup="listbox"`, `aria-expanded`, `aria-controls`, `role="listbox"`, `role="option"`, `aria-selected`, arrow keys) and then fails to honor almost any of the behavior that contract promises. The attribute layer is close to complete; the behavior layer is broken in both directions of the open/close transition, and the widget's entire reason for existing — reporting which sort order is currently selected — never reaches the accessibility tree at all. The supplied driven-keystroke trace corroborates this from the outside: focus does not enter the list on open, the listbox has an empty accessible name, ArrowDown produces no observable state delta and no announcement, selection dumps focus to `body`, and the trigger's focus announcement after selection is byte-identical to its announcement before the user ever opened the dropdown. This is not a focus-restoration bug with an otherwise sound widget attached. It is a widget whose keyboard model is inert in the state it actually enters, and which needs re-architecture (ideally to native `<select>`), not a patch.

---

## Evidence provenance and tier (read before the findings)

Two things about the evidence set must be stated up front, because they govern how much weight each finding carries.

**1. The evidence I was handed is an `a11y-evidence-reader` digest, and I could not re-fetch it.**

Per the Phase 0 rule for digests: an evidence-reader digest is *detector output, one tier below the artifact it cites* — a paraphrase, not the hard evidence. The rule requires re-fetching at the cited handle (`evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json`, per-step `jq` selections) before filing any finding that rests on a digest line, and labeling anything untraceable as **digest-only**.

I was not able to re-fetch: the underlying trace artifact was not available to me in this review context. Therefore **every trace-derived observation below is labeled `digest-only`.**

This matters less than it normally would, because of the second point:

**2. Every CRITICAL and MAJOR finding below is independently established from the component source, which I read first-hand.**

The digest is used as *corroboration* — measured confirmation that the code defect reproduces in a real browser under real keystrokes — never as the sole basis for a finding. Where a finding would rest on the digest alone, I say so and route it to Open Questions. Readers should treat the source-code evidence as first-hand and the trace citations as second-hand-but-consistent.

**3. Instrument-tier notes (Phase 0 calibration rules applied):**

- This is a **driven-live** session (`mode=driven-live`), not a batch crawl. The keyboard-a11y-tester calibration rule that batch-crawl 4.1.3 "silent live region" findings are *prompts to run a driven session, never failure evidence* does not suppress these observations — a driven session is precisely the follow-up that rule prescribes, so the empty `sr_announcement` captures carry weight here.
- However, `sr_announcement` and `ax_name_role_state` are the driven runner's **own simulated capture**, not a real screen reader and not the contract's prescribed name-role-state instrument (`virtual-screen-reader` assertion output). The digest says this itself. Treat them as strong corroboration of computed-AX-tree facts, not as verified NVDA/JAWS/VoiceOver output.
- Likewise, this is not the contract's canonical `npx playwright test` keyboard transcript; it is an adjacent real-keystroke record. Adjacent, and I accept it as such, but I am not calling it the canonical artifact.
- No `conformance_level` field appears in the digest, so the KAT `conformance_level` pass/fail-gate trap (upstream issue #27) is not in play.
- The digest asserts **no** severity, WCAG mapping, or pass/fail verdict — it explicitly reserves those for the consumer. Nothing in it is a journey-level judgment claim I need to gate behind supporting trace steps.
- This is a **fresh design pass**, not a fix/remediation review, so the a11y-test Verification evidence contract type-match check (screenshot-offered-as-proof-of-announcement, etc.) does not trigger as a finding.

**4. Line numbers.** The fixture supplied the component inline with no file path. All `file:line` references below use `BuggyDropdown.jsx:N` where N is the line number **within the fenced source block in the review prompt** (line 1 = `import React, { useState, useRef } from 'react';`). I have not invented a repository path.

---

## Phase 1 — Pre-commitment Predictions (made before reading the code)

Component type: custom dropdown / select replacement. Predicted the five most likely design gaps:

| # | Prediction | Outcome |
|---|---|---|
| P1 | Focus does not restore to the trigger after Escape | **Confirmed** — and worse than predicted (focus goes to `body`, not "stays somewhere reasonable") |
| P2 | Arrow-key navigation is incomplete — no `aria-activedescendant`, no roving tabindex, so the cursor is invisible to AT | **Confirmed exactly** |
| P3 | Selected state is not announced when it changes | **Confirmed, but root cause was upstream of where I looked** (see Surprise C) |
| P4 | The options container is unnamed / not properly referenced | **Confirmed** — empty accessible name on the listbox |
| P5 | Escape does not *cancel* — it commits the arrow-key cursor as a selection visually while never firing `onSelect` | **Confirmed** |

**Three surprises the predictions missed:**

- **Surprise A — the open transition is broken too, not just the close.** I predicted a close-side focus bug. There is also an open-side one: `listRef.current.focus()` at line 11 runs before the `<ul>` has mounted, so it is a no-op. Both directions of the transition are inoperative. The measured trace confirms `focus_moved:false` on the opening keystroke.
- **Surprise B — the trigger button has no keydown handler at all.** `handleKeyDown` is bound only to the `<ul>` (line 57). Because focus never leaves the button on open, the widget's *entire* advertised keyboard model — Escape, ArrowDown, ArrowUp — is inert in the state the widget actually enters. I predicted incomplete keyboard support; I did not predict that it would be unreachable.
- **Surprise C — `<label htmlFor>` on a `<button>` silently suppresses the button's own value text from the accessible name.** I predicted "selected state not announced" and expected to find a missing `aria-live` region. The real mechanism is an accessible-name override that is invisible in the visual layer and invisible in a code skim. The trace caught it as a byte-identical announcement string across a state change.
- (Half-surprise: hardcoded DOM ids in a component that takes props and is obviously built for reuse.)

---

## Phase 2 — Semantic HTML Audit

| Check | Result |
|---|---|
| Native HTML vs. ARIA-on-divs | **Mixed.** The trigger is a real `<button>` (correct). The popup is a real `<ul>`/`<li>` re-roled to `listbox`/`option` (correct APG markup shape). But the *whole component* is a hand-rolled `<select>` — see MAJOR-1. |
| Is ARIA replacing bad semantics or enhancing good ones? | Enhancing at the element level, **replacing at the component level**. |
| Heading hierarchy | Not applicable — component contributes no headings. |
| Landmarks | Component contributes none. See "Not claimed" below. |
| Lists for list content | Yes — `<ul>`/`<li>`, correctly re-roled. Note that `role="listbox"` on `<ul>` intentionally suppresses list semantics; that is correct for this pattern, not a defect. |
| Tables | None. |
| `<label>` associated with every form control | **Defective** — `<label htmlFor="dropdown-btn">` targets a `<button>`, which is not a labelable element per HTML. See MAJOR-2. |
| Hidden ARIA papering over broken HTML | The `aria-hidden="true"` on the `▼` glyph (line 50) is **correct usage**, not papering. |

**Not claimed:** the digest's absence claim (`region:{"landmark":null,"heading":null}` for every focused element) is explicitly scoped to the per-step focused-region field, **not** a page-wide landmark or heading census, and no axe-core artifact was supplied. I am therefore **not** asserting that the host page lacks landmarks or has a heading-order violation. That question is open and unmeasured. This is exactly the DOM-wide structural verdict the digest says it cannot support, and I am not going to launder it into one.

---

## Phase 3 — ARIA Pattern Compliance Audit

**Pattern identified:** WAI-ARIA APG **Combobox Pattern — Select-Only Combobox** (equivalently, the collapsed **Listbox Pattern** with a button trigger). The `aria-haspopup="listbox"` + `aria-expanded` + `aria-controls` trigger controlling a `role="listbox"` popup is that pattern's signature.

The APG allows two mutually exclusive focus strategies for the popup, and the implementation must pick one and complete it:

- **Strategy A (`aria-activedescendant`)** — DOM focus stays on the combobox/trigger; the listbox carries `aria-activedescendant` pointing at the active option's `id`; every option has a unique `id`; `tabindex="-1"` on the listbox.
- **Strategy B (roving tabindex)** — DOM focus moves onto the active `<li role="option">` itself; active option has `tabindex="0"`, all others `tabindex="-1"`.

This component implements **neither**. It moves DOM focus to the *container* (`tabIndex="0"` on the `<ul>`, line 58) and then tracks the cursor in React state only. That is the one arrangement the pattern does not support, because the accessibility tree has no way to express "the cursor is on option 3" when focus is on the container and no `aria-activedescendant` exists.

| APG requirement | Present? | Evidence |
|---|---|---|
| Trigger has `aria-expanded` reflecting popup state | ✅ Yes, and measured correct | line 45; trace `step_0002` `expanded:true`, `step_0006` `expanded:false` (digest-only) |
| Trigger has `aria-haspopup="listbox"` | ✅ Yes | line 44; measured `hasPopup:"listbox"` (digest-only) |
| Trigger `aria-controls` references the popup id | ⚠️ Yes when open, **dangling IDREF when closed** | lines 46, 52, 55 — see MINOR-1 |
| Trigger's accessible name conveys **name + current value** | ❌ **No — value never reaches the name** | lines 41, 49; see CRITICAL-1 |
| Popup has `role="listbox"` | ✅ Yes | line 56 |
| Popup has an accessible name | ❌ **No — computed name is `""`** | lines 53–60; see MAJOR-3 |
| Options have `role="option"` | ✅ Yes | line 64 |
| Options have unique `id`s (required for Strategy A) | ❌ **No ids at all** | lines 62–68 |
| `aria-activedescendant` on listbox (Strategy A) | ❌ **Absent** | see CRITICAL-2 |
| Roving `tabindex` on options (Strategy B) | ❌ **Absent** | see CRITICAL-2 |
| `aria-selected` on options | ✅ Present, but semantically conflated | line 65; see MAJOR-5 |
| Escape closes popup **and returns focus to trigger** | ❌ **Closes only; focus is lost** | lines 22–24; see CRITICAL-3 |
| Selection closes popup **and returns focus to trigger** | ❌ **Closes only; focus is lost** | lines 15–19; see CRITICAL-3 |
| Opening moves focus per the chosen strategy | ❌ **No-op** | lines 10–11; see MAJOR-4 |
| ARIA values are valid literals | ✅ Yes — `aria-expanded` is a real boolean, `aria-selected` is a real boolean, `aria-haspopup="listbox"` is a valid token | lines 44–45, 65 |

**Verdict on the pattern:** the attribute surface is roughly 80% of the pattern; the interaction contract those attributes announce is roughly 15% implemented. This is the exact failure class this review exists to catch — a widget that will pass axe-core cleanly (every ARIA attribute it has is valid, every role is allowed in its context, the trigger has a name) while being unusable with a screen reader.

---

## Phase 4 — Focus Management Review

Trace the focus lifecycle through the four transitions:

**T1 — Opening (click or Enter/Space on the trigger).** `handleToggle` (lines 8–13) queues `setIsOpen(!isOpen)` and then, in the same synchronous tick, reads `listRef.current`. The `<ul>` is conditionally rendered (`{isOpen && (...)}`, line 52), so on the opening transition it has never mounted and `listRef.current` is `null`. The guard `if (!isOpen && listRef.current)` short-circuits on the ref, the `.focus()` at line 11 never runs, and focus stays on the trigger.

Note the double defect: the `!isOpen` half of the guard is reading the *stale pre-update* value, which happens to be the correct test for "we are opening," so the logic reads as intentional — but the ref half makes it unreachable. This is a focus-management *intention* with no focus-management *effect*, which is worse than no code at all, because it looks handled in review.

Corroborated (digest-only): `step_0002` — `keystroke_sent:"Enter"`, `active_element_selector:"#dropdown-btn"`, `focus_moved:false`, while `expanded` goes `false → true` and `controls:"dropdown-list"` appears. The state changed; focus did not.

**T2 — While open, focus is on the trigger.** The trigger has only `onClick` (line 47). No `onKeyDown`. So in the state the widget actually occupies after opening:
- **Escape does nothing.** The popup stays open.
- **ArrowDown / ArrowUp do nothing** — worse, `e.preventDefault()` is never reached because `handleKeyDown` is not bound here, so the browser's default action fires and **the page scrolls behind the open popup**.
- The only way forward is Tab, which lands on the `<ul>` because of `tabIndex="0"` (line 58) — undiscoverable, and contrary to what `aria-haspopup` promised.

**T3 — Focus on the listbox, arrowing.** `handleKeyDown` now fires. `selectedIndex` updates, `aria-selected` flips, the `.selected` class moves, and the trigger's visible text changes. DOM focus stays on the `<ul>`. Because there is no `aria-activedescendant` and no roving tabindex, **the accessibility tree registers no change of position whatsoever.**

Corroborated (digest-only): `step_0004` — `keystroke_sent:"ArrowDown"`, `focus_moved:false`, captured states **identical** to `step_0003`, no active-descendant or option-level field present, `new_phrases:[]`, `focus_announcement:null`.

**T4 — Closing (Enter, click on an option, or Escape).** All three paths call `setIsOpen(false)` (lines 18, 24) and stop. The `<ul>` unmounts. The `document.activeElement` was the `<ul>`; when a focused element is removed from the DOM, focus falls to `<body>`. Nothing anywhere in the component calls `.focus()` on the trigger.

Corroborated (digest-only): `step_0005` — `active_element_selector:"body"`, `tag:"body"`, `focus_moved:true`, `ax_name_role_state:{"name":null,"role":"none","states":{}}`, `region:null`, `bounding_box:null`, `computed_focus_style:null`. And decisively: `step_0006` reaches `#dropdown-btn` **only via an explicit subsequent `Shift+Tab`**, not automatically from `step_0005`.

**Other focus-management checks:**

- **Focus escape / no dismissal on blur.** With `tabIndex="0"` on the listbox and no `onBlur`/`focusout` handler and no outside-click listener, a Tab from the open listbox walks focus into the rest of the page while the popup remains open and `aria-expanded` remains `true`. This is the protocol's **else-branch coverage** anti-pattern (#4): Escape was handled, blur was not.
- **Keyboard trap:** none. Tab always moves forward. WCAG 2.1.2 is satisfied.
- **Phantom tab stops when collapsed:** none. Because the popup is conditionally rendered rather than hidden with `aria-hidden`, the protocol's "missing `inert` on hidden content" gap **does not apply here**. Credit where due.
- **Framework unmount timing:** the protocol's `setTimeout(0)` guidance is directly relevant to the fix — a focus-return call placed synchronously before/inside the state update that unmounts the list will be lost. The fix must run after commit.
- **Focus indicator on the `<ul>`:** the digest does not report `computed_focus_style` for `step_0003`/`step_0004`, and no CSS was supplied. **Unverified** — routed to Open Questions, not filed as a finding.
- **Tab order left-to-right/top-to-bottom:** consistent with visual order in the supplied markup.

WCAG in play: **2.4.3 Focus Order**, **2.1.1 Keyboard**, **4.1.2 Name, Role, Value**, **3.2.1 On Focus** (not violated).

---

## Phase 5 — State Communication Audit

| State | Communicated visually | Communicated programmatically |
|---|---|---|
| Expanded / collapsed | ✅ (list renders; `▼` glyph) | ✅ `aria-expanded` — **works, measured** |
| Cursor position while arrowing | ✅ `.selected` class + trigger text changes | ❌ **Nothing.** No `aria-activedescendant`, no focus movement, no live region |
| Which option is selected, after commit | ✅ trigger text becomes "Price: low to high" | ❌ **Nothing.** Accessible name stays "Sort by" |
| Selection committed vs. merely previewed | ⚠️ Ambiguous — visual text changes on arrow, before commit | ❌ Not distinguishable |
| Popup dismissed | ✅ list disappears | ⚠️ `aria-expanded` flips, but focus is on `body` so nothing is announced |
| Loading / busy | N/A — `onSelect` is fire-and-forget; see Gap G6 | N/A |
| Disabled / readonly | Not implemented at all | Not implemented |

The decisive measurement is observation 5 (digest-only), `step_0006`: after a full open → arrow → select → return cycle, the trigger's `text` field is `"Price: low to high▼"` (it was `"Newest▼"` at `step_0001`), while `ax_name_role_state.name` is `"Sort by"` — **the identical string to `step_0001`** — and `focus_announcement` is `"button, Sort by, not expanded, has popup listbox"`, **byte-identical to `step_0001`'s announcement.**

A screen reader user who completes the entire interaction hears exactly what they heard before starting it. The visual layer moved; the accessibility tree did not. This is WCAG **4.1.2 Name, Role, Value** in its purest form: the control's *value* is not programmatically determinable.

The `▼` in `<span aria-hidden="true">` (line 50) is handled correctly — without it, a screen reader would append "black down-pointing triangle" to every announcement. The protocol calls this out as a common defect; this code gets it right, and I am noting that rather than manufacturing a finding around it.

WCAG in play: **4.1.2 Name, Role, Value**; **4.1.3 Status Messages**; **1.3.1 Info and Relationships**.

---

## Phase 6 — Multi-Perspective Review

**Screen reader user (NVDA / JAWS / VoiceOver).** Tabs to a button announced as *"Sort by, button, collapsed, has popup listbox."* Note what is missing already: no current value. Presses Enter. Hears **nothing** — `expanded` flipped to `true` in the AX tree but focus did not move and there is no announcement, so unless the user's AT happens to re-poll the trigger they have no signal the popup opened. Presses ArrowDown expecting the APG contract — the page scrolls. Eventually Tabs, landing on an element announced as *"listbox"* with **no name** and no announced option. Arrows down: **complete silence**, because the cursor lives only in React state. Guesses at Enter. Focus lands on `body`. Tabs or Shift+Tabs back to the trigger and hears *"Sort by, button, collapsed, has popup listbox"* — the same string as before they started. **They cannot determine whether they changed the sort order, or to what.** Alarm: **HIGH**.

**Keyboard-only (sighted) user.** Better off, because the visual `.selected` class and the trigger's changing text carry the information the AX tree drops — but still: Escape is inert from the state the widget enters; ArrowDown scrolls the page behind an open popup; after selecting, focus is on `body`, so the next Tab restarts from the top of the document. On a sorted results page — which is what `goals[0].intent` describes ("open the sort dropdown... pick an option") — that means re-traversing the entire header and navigation to get back to the results the user just re-sorted. Alarm: **HIGH**.

**Low vision user (200% zoom, magnifier, high contrast).** Cannot fully assess — no CSS was supplied. Two concrete concerns, both unverified: (a) the focus indicator on `<ul tabIndex="0">` — the UA default outline on a block-level list container is frequently overridden or visually swallowed by `.dropdown-list` styling; (b) `className={index === selectedIndex ? 'selected' : ''}` (line 67) is the *only* markup hook for the cursor, so if `.selected` is implemented as a background-color change alone it is a WCAG 1.4.1 use-of-color failure and disappears in forced-colors mode. When focus lands on `body` after selection, a magnifier viewport is thrown to the document origin with no visible focus anywhere. Alarm: **MEDIUM** (would be HIGH with CSS in hand).

**Cognitive accessibility user.** The Escape-does-not-cancel behavior is the real problem: arrowing changes the trigger's visible text *before* commit, and Escape leaves that changed text in place while never calling `onSelect`. The user sees "Price: low to high" on a control whose owning application still believes the value is "Newest." That is a false report of system state, and there is no undo, no confirmation, no way to tell committed from previewed. It also breaks the learned `<select>` mental model, where Escape reverts. Alarm: **MEDIUM**.

**Vestibular & motion.** No animation, transition, parallax, or autoplay in the supplied code. CSS not supplied, so `prefers-reduced-motion` cannot be checked against a real stylesheet. Alarm: **LOW**.

**Auditory access.** No media elements, no audio, no sound-based alerts. Alarm: **LOW**.

**Environmental contrast.** No colors, no computed contrast values, and no axe `color-contrast` artifact were supplied — the digest states plainly that no axe-core scan was provided. I have **no measured ratios** and will not estimate any. The one structural concern is the color-only selection indicator noted under Low vision. Alarm: **MEDIUM**, on the strength of the `.selected`-class-only cursor, not on any contrast measurement.

### Perspective Alarm Levels

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | **HIGH** | Custom listbox widget; measured empty accessible name on the popup; measured byte-identical announcement across a value change; no `aria-activedescendant` |
| Keyboard-only | **HIGH** | Measured focus loss to `body`; no focus restoration on any close path; Escape/arrows inert on the trigger; open popup survives blur |
| Low vision | **MEDIUM** | Cursor indicated by a single CSS class; focus indicator on a re-roled `<ul>` unverified; no CSS supplied |
| Cognitive | **MEDIUM** | Escape commits visually without committing programmatically; no cancel semantics; diverges from the native `<select>` model |
| Vestibular & motion | **LOW** | No animation, transition, or autoplay present in supplied code |
| Auditory access | **LOW** | No media elements |
| Environmental contrast | **MEDIUM** | Color/class-only selection indicator; no contrast measurements supplied |

**Escalation:** Screen reader and Keyboard-only are at HIGH and should go to `/perspective-audit` for deep review. Low vision, Cognitive, and Environmental contrast are at MEDIUM and warrant a pass once the CSS is available.

---

## Phase 7 — Gap Analysis (What Is Absent)

- **G1 — No `aria-activedescendant` and no roving tabindex.** The single largest structural absence. Without one of them, arrow-key navigation is invisible to AT no matter how correct the rest of the ARIA is.
- **G2 — No `id` on any `<li role="option">`** (lines 62–68), which forecloses the `aria-activedescendant` fix until it is added.
- **G3 — No accessible name on the listbox** — no `aria-label`, no `aria-labelledby` (lines 53–60). Measured `name: ""`.
- **G4 — No focus restoration on any close path.** Neither `handleSelect` (lines 15–19) nor the Escape branch (lines 22–24) nor the option `onClick` (line 66) touches focus.
- **G5 — No keydown handler on the trigger** (lines 42–51). Escape, ArrowDown, ArrowUp, Home, End, and type-ahead are all unreachable from where focus actually is when the popup is open.
- **G6 — No dismissal on focus-out and no outside-click dismissal.** The popup can be left open indefinitely with `aria-expanded="true"` while focus is elsewhere on the page.
- **G7 — No `Home` / `End` / `Space` / type-ahead handling.** APG lists Home/End as expected listbox keys and printable-character type-ahead as recommended; `Tab` should select-and-close in the select-only combobox variant.
- **G8 — No unique-id strategy.** `id="dropdown-btn"` (line 43) and `id="dropdown-list"` (line 55) are hardcoded in a component that takes `label`/`options`/`onSelect` props — i.e. one explicitly built to be instantiated more than once. Two instances on a page (or one responsive component rendered twice for mobile + desktop) produce duplicate ids: `htmlFor` binds to the first button, `aria-controls` points at the wrong list, and any `getElementById`-based tooling resolves incorrectly. The protocol names this exact case under duplicate DOM rendering.
- **G9 — No cancel/revert semantics.** `selectedIndex` is mutated during navigation and never restored on Escape, so cancel is indistinguishable from commit in the UI while being entirely distinguishable to the application.
- **G10 — No status announcement of the committed value.** With the accessible name pinned to "Sort by" (CRITICAL-1), nothing — not a name change, not a `role="status"` region — tells AT what was chosen.
- **Not a gap:** `inert` on hidden content. The popup is conditionally rendered, so nothing hidden receives Tab focus. Explicitly checked, explicitly clean.
- **Not assessable:** landmark structure, heading order, DOM-wide role validity, contrast ratios, target sizes. No axe artifact, no CSS, and the trace's AX snapshots cover only the six elements that received focus. See Open Questions.

**Anti-pattern checks from the April 2026 third-party audit list:**

| # | Anti-pattern | Applies? |
|---|---|---|
| 1 | Broadcast vs. association (`role="alert"`/`aria-live` inside a loop) | No — no live regions anywhere (which is its own gap, G10) |
| 2 | `title` as sole accessible name | No — no `title` attributes |
| 3 | ARIA label on a wrapper substituting for a visible label | **Partially, inverted** — a visible `<label>` exists, but it is attached to a non-labelable element and *displaces* the value. See MAJOR-2 |
| 4 | **Else-branch coverage** | **Yes** — Escape branch handled, blur/outside-click branch not; keydown handled on the popup, not on the trigger. See G5, G6 |
| 5 | Single-selector scope | Not applicable — single React component, no CMS view modes |
| 6 | `<td>` row headers in loops | Not applicable |
| 7 | `role="presentation"` on data tables | Not applicable |
| 8 | Verbose alt on decorative image links | Not applicable — decorative glyph is correctly `aria-hidden` |
| 9 | **DOM-verification required for ARIA fixes** | **Yes, prospectively** — every fix below must be verified in the rendered accessibility tree, not just in unit tests. The measured `name:""` on the listbox and the stale `name:"Sort by"` on the trigger are precisely the class of defect that only DOM/AX inspection catches |

---

## Audit of the fixture's own "Accessibility Features Present" claims

The claim list is worth auditing directly, because "present" and "working" diverge on five of seven rows. This is the 80%-pattern problem in tabular form.

| Claimed | Present in DOM? | Actually functional? |
|---|---|---|
| `aria-haspopup="listbox"` | ✅ | ✅ — measured |
| `aria-expanded` toggles | ✅ | ✅ — measured `false → true → false` |
| `aria-controls` references list | ✅ when open | ⚠️ Dangling IDREF when collapsed (MINOR-1) |
| `role="listbox"` and `role="option"` | ✅ | ⚠️ Roles are correct; the listbox has **no accessible name** (MAJOR-3) and no active-descendant relationship (CRITICAL-2) |
| `aria-selected` on items | ✅ | ⚠️ Present, but conflates cursor with selection and is **never announced** (MAJOR-5, CRITICAL-2) |
| Arrow key navigation | ✅ in code | ❌ **Inert from where focus actually is**; produces zero AT-perceivable change even when reachable (CRITICAL-2, MAJOR-4) |
| Label association via `htmlFor` | ✅ | ❌ **Invalid target type**, and it suppresses the control's value from the accessible name (CRITICAL-1, MAJOR-2) |

And against the fixture's own "Expected Behavior" spec: 2 of 5 bullets hold.

| Expected | Actual |
|---|---|
| Opens on button click, **list receives focus** | Opens; **focus stays on the button** (measured `focus_moved:false`) |
| Arrow Down/Up navigate options | Only once focus is manually Tabbed into the list; no AT-perceivable effect |
| Enter or click selects option | ✅ Holds |
| Escape should close dropdown **AND restore focus to button** | Closes only when focus is in the list; **never restores focus** |
| Selection should restore focus to button | **Focus goes to `body`** (measured) |

---

## Findings

### Critical Findings (blocks access)

---

**CRITICAL-1 — The dropdown's selected value never reaches the accessible name; a screen reader user cannot determine what the control is set to.**

`<label htmlFor="dropdown-btn">{label}</label>` (`BuggyDropdown.jsx:41`) supplies the button's accessible name. Because a labelling relationship outranks element contents in the accessible-name computation, the `{options[selectedIndex]}` text node at `BuggyDropdown.jsx:49` — the entire point of the control — is **discarded** from the name. The button announces "Sort by" and only "Sort by," at every value.

- **User group:** Screen reader users (total loss of value information); secondarily voice-control users, who cannot target the control by its visible text.
- **WCAG:** 4.1.2 Name, Role, Value — a user interface component's *value* must be programmatically determinable. Also WAI-ARIA APG Combobox (Select-Only), whose reference implementation composes the name as `aria-labelledby="<visible-label-id> <combobox-id>"` so the announcement is "Sort by, Price: low to high."
- **Corroboration (digest-only):** `interactive-dropdown-focus-bug.trace.json :: step_0006` — `text: "Price: low to high▼"` (changed from `"Newest▼"` at `step_0001`) while `ax_name_role_state.name: "Sort by"` and `focus_announcement: "button, Sort by, not expanded, has popup listbox"`, both **string-identical to `step_0001`**. A complete interaction produced zero change in what AT reports.
- **Confidence:** HIGH. Established from source; independently measured.
- **Could the developer refute this?** NO. The name-computation precedence is unambiguous and the trace shows the resulting string.
- **GAP or PREFERENCE:** GAP.
- **Why this matters:** This is not "the announcement could be more descriptive." A sort control that cannot report its own sort order is a control whose state is unknowable without sight. The user cannot verify their action succeeded, cannot re-check the value later, and cannot recover from a mis-selection except by trial and error.
- **Fix:** Remove `htmlFor` from the `<label>` (see MAJOR-2) and give the button `aria-labelledby="sort-label sort-btn"` where `sort-label` is the visible label's id and `sort-btn` is the button's own id, so the name resolves to "Sort by Price: low to high." Do not use `aria-label` for this — it would drop the visible label and break the voice-control name match (WCAG 2.5.3). Verify in the browser's accessibility-tree inspector after the change; a unit test asserting on `textContent` will not catch a regression here.

```
### A11y Evidence Finding
finding_id: dropdown-selected-value-absent-from-accessible-name
fingerprint: NOT-COMPUTED — read-only review; the cited trace could not be re-fetched, and inventing hex digits would fabricate provenance. Compute as sha256("dropdown-selected-value-absent-from-accessible-name|BuggyDropdown.jsx|41,49") at ingest.
source: BuggyDropdown.jsx (component source, read first-hand) + a11y-evidence-reader digest of evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json :: step_0001, step_0006 (DIGEST-ONLY — not re-fetched)
wcag_or_apg: WCAG 2.2 SC 4.1.2 Name, Role, Value; WAI-ARIA APG Combobox Pattern (Select-Only Combobox)
section_508_fpc_context: not in scope — no declared Section 508 conformance target for this review. If one were declared, 4.1.2 is within the WCAG 2.0 A/AA basis Revised Section 508 incorporates.
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, keyboard-only=MEDIUM, low-vision=LOW, cognitive=MEDIUM
evidence: BuggyDropdown.jsx:41 (`<label htmlFor="dropdown-btn">{label}</label>`) overrides BuggyDropdown.jsx:49 (`{options[selectedIndex]}`). Trace step_0006: text="Price: low to high▼", ax_name_role_state.name="Sort by", focus_announcement="button, Sort by, not expanded, has popup listbox" — identical to step_0001.
reproduction_steps: 1) Focus the trigger; note announced name. 2) Open, arrow to a different option, press Enter. 3) Return focus to the trigger. 4) Compare announced name and the browser AX-tree "Name" property against the visible button text.
expected_behavior: Trigger announces label plus current value, e.g. "Sort by Price: low to high, button, collapsed, has popup listbox".
actual_behavior: Trigger announces "button, Sort by, not expanded, has popup listbox" both before and after the value changes.
trend: new
```

---

**CRITICAL-2 — Arrow-key navigation is invisible to assistive technology: no `aria-activedescendant`, no roving tabindex, no option ids.**

`handleKeyDown` (`BuggyDropdown.jsx:25–32`) advances `selectedIndex` in React state. DOM focus remains on the `<ul>` (`BuggyDropdown.jsx:53–60`, `tabIndex="0"` at line 58). The listbox carries no `aria-activedescendant`, the options (`BuggyDropdown.jsx:62–68`) carry no `id` and no `tabindex`. The cursor therefore exists **only** in React state and CSS. Nothing in the accessibility tree changes when the user arrows.

- **User group:** Screen reader users — the widget's primary interaction is entirely imperceptible.
- **WCAG / APG:** WAI-ARIA APG Listbox Pattern and Combobox Pattern (Select-Only) — the listbox must manage its active option either via `aria-activedescendant` on the focus-holding element (each option needing a unique `id`) or via roving `tabindex` moving DOM focus onto the option itself. WCAG 4.1.2 Name, Role, Value; WCAG 4.1.3 Status Messages.
- **Corroboration (digest-only):** `step_0004` — `keystroke_sent:"ArrowDown"`, `active_element_selector:"#dropdown-list"`, `focus_moved:false`, captured states **byte-identical to `step_0003`**, no active-descendant or option-level field present in the capture at all, `sr_announcement.new_phrases:[]`, `focus_announcement:null`. Nothing observable happened.
- **Confidence:** HIGH. Established from source; the trace's identical-states capture is exactly the expected signature.
- **Could the developer refute this?** NO.
- **GAP or PREFERENCE:** GAP.
- **Why this matters:** The fixture lists "Arrow key navigation" as an accessibility feature present. It is present in the sense that a keystroke changes a variable, and absent in the sense that any assistive technology can perceive it. A screen reader user arrowing through this list hears silence and has no way to know how many options exist, which one is under the cursor, or when they have wrapped past the end.
- **Fix:** Give each option a stable unique id (`id={`${instanceId}-opt-${index}`}` — see MAJOR-6 for the instance id), add `aria-activedescendant={`${instanceId}-opt-${selectedIndex}`}` to the element holding DOM focus, and set the listbox to `tabIndex={-1}`. Then implement the fuller APG keyboard set (Home, End, type-ahead). Verify by inspecting the AX tree while arrowing — the active option must change there, not just in CSS.

```
### A11y Evidence Finding
finding_id: dropdown-listbox-cursor-not-exposed-to-at
fingerprint: NOT-COMPUTED — see CRITICAL-1 note. Compute as sha256("dropdown-listbox-cursor-not-exposed-to-at|BuggyDropdown.jsx|53-68") at ingest.
source: BuggyDropdown.jsx (read first-hand) + a11y-evidence-reader digest of interactive-dropdown-focus-bug.trace.json :: step_0003, step_0004 (DIGEST-ONLY — not re-fetched)
wcag_or_apg: WAI-ARIA APG Listbox Pattern / Combobox Pattern (Select-Only); WCAG 2.2 SC 4.1.2 Name, Role, Value
section_508_fpc_context: not in scope
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, keyboard-only=MEDIUM, low-vision=MEDIUM, cognitive=LOW
evidence: BuggyDropdown.jsx:53-60 (listbox has tabIndex="0", no aria-activedescendant); BuggyDropdown.jsx:62-68 (options have no id, no tabindex). Trace step_0004 vs step_0003: states identical, focus_moved:false, new_phrases:[], focus_announcement:null after ArrowDown.
reproduction_steps: 1) Open the dropdown. 2) Tab into the listbox. 3) Press ArrowDown several times. 4) Watch the accessibility tree and the screen reader speech log.
expected_behavior: Each ArrowDown moves the active option — announced as e.g. "Price: low to high, 2 of 4" — via aria-activedescendant or DOM focus.
actual_behavior: No AX-tree change, no announcement; only a CSS class and the trigger's visible text move.
trend: new
```

---

**CRITICAL-3 — Focus is dropped to `document.body` on every close path; it is never restored to the trigger.**

Three close paths — Escape (`BuggyDropdown.jsx:22–24`), Enter-to-select (`BuggyDropdown.jsx:33–35` → `handleSelect`, lines 15–19), and option click (`BuggyDropdown.jsx:66` → `handleSelect`) — all call `setIsOpen(false)` and nothing else. The `<ul>` holding focus is conditionally unmounted (`BuggyDropdown.jsx:52`), and when the focused element is removed from the DOM the browser resets focus to `<body>`. No `.focus()` call on the trigger exists anywhere in the component.

- **User group:** Keyboard-only users and screen reader users (both).
- **WCAG:** 2.4.3 Focus Order — after a dismissible popup closes, focus must move to a location that preserves meaning and operability, conventionally the trigger. Also WAI-ARIA APG Combobox/Listbox, whose Escape and selection behaviors both specify "focus returns to the combobox/button."
- **Corroboration (digest-only):** `step_0005` — `keystroke_sent:"Enter"`, `active_element_selector:"body"`, `tag:"body"`, `focus_moved:true`, `ax_name_role_state:{"name":null,"role":"none","states":{}}`, `region:null`, `computed_focus_style:null`, all `sr_announcement` fields empty/null. And the clincher: `step_0006` reaches `#dropdown-btn` **only via an explicit `Shift+Tab`**, not automatically.
- **Confidence:** HIGH.
- **Could the developer refute this?** NO — the trace measures the outcome directly.
- **GAP or PREFERENCE:** GAP.
- **Realist Check:** Worst realistic case — a user sorting a product results page presses Enter, focus lands on `body` with no visible indicator anywhere, and their next Tab restarts from the top of the document, forcing them back through the skip link, header, and full navigation to reach the results they just re-sorted. For a screen reader user this compounds with CRITICAL-1: they receive no announcement of the selection *and* lose their place. Detection in production: **never** — this is a silent failure that produces no error, no console warning, and no automated-test failure. Survives all four Realist questions. **Correctly rated CRITICAL; not downgraded.**
- **Fix:** Store a ref to the trigger and restore focus after the close commits, not synchronously inside the state update. In React: keep `triggerRef`, and in a `useEffect` keyed on `isOpen` call `triggerRef.current?.focus()` when `isOpen` transitions `true → false` *and* the close was user-initiated. If unmount timing still drops the assignment (React 16 in particular), wrap in `setTimeout(..., 0)`. Apply to **all three** close paths — this is the else-branch coverage trap; fixing only the Escape branch is the classic partial fix.

```
### A11y Evidence Finding
finding_id: dropdown-focus-lost-to-body-on-close
fingerprint: NOT-COMPUTED — see CRITICAL-1 note. Compute as sha256("dropdown-focus-lost-to-body-on-close|BuggyDropdown.jsx|15-19,22-24,52") at ingest.
source: BuggyDropdown.jsx (read first-hand) + a11y-evidence-reader digest of interactive-dropdown-focus-bug.trace.json :: step_0005, step_0006 (DIGEST-ONLY — not re-fetched)
wcag_or_apg: WCAG 2.2 SC 2.4.3 Focus Order; WAI-ARIA APG Combobox Pattern (Select-Only) — Escape and selection return focus to the combobox
section_508_fpc_context: not in scope — 2.4.3 is within the WCAG 2.0 A/AA basis if a 508 target is later declared
severity: CRITICAL
perspective_alarms: keyboard-only=HIGH, screen-reader=HIGH, low-vision=MEDIUM, cognitive=MEDIUM
evidence: BuggyDropdown.jsx:18 and BuggyDropdown.jsx:24 call setIsOpen(false) with no focus restoration; BuggyDropdown.jsx:52 unmounts the focused <ul>. Trace step_0005: active_element_selector="body", focus_moved:true, role="none". step_0006 reaches "#dropdown-btn" only after an explicit Shift+Tab.
reproduction_steps: 1) Tab to the trigger, press Enter to open. 2) Tab into the listbox. 3) Press Enter to select (or Escape to dismiss). 4) Inspect document.activeElement. 5) Press Tab and observe where focus resumes.
expected_behavior: Focus returns to the trigger button, which announces the label and the newly selected value.
actual_behavior: document.activeElement is <body>; no focus indicator is visible; the next Tab resumes from the top of the document.
trend: new
```

---

**CRITICAL-4 — The listbox's `role="option"` children are unreachable as individual AT targets, so the widget has no working selection interaction for screen reader users at all.**

This is the compound consequence of CRITICAL-2 plus MAJOR-3, and I am filing it separately because the individual fixes do not add up to a working widget unless someone verifies the whole loop. With DOM focus parked on an **unnamed** `<ul role="listbox">`, no `aria-activedescendant`, and no per-option focus, a screen reader user reaching the popup encounters a named-nothing container whose children are announced — if at all — only through the AT's own object-navigation review mode, entirely outside the widget's keyboard model. Pressing Enter then commits whatever `selectedIndex` happens to be, which the user has had no way to observe.

- **User group:** Screen reader users.
- **WCAG / APG:** WCAG 4.1.2 Name, Role, Value; WAI-ARIA APG Listbox Pattern (the listbox must have an accessible name and a determinable active option).
- **Evidence:** `BuggyDropdown.jsx:53–60` (unnamed container holding focus) + `BuggyDropdown.jsx:62–68` (options with no id/tabindex). Corroborated digest-only by `step_0003` (`ax_name_role_state.name:""`, `role:"listbox"`) and `step_0004` (no state delta on ArrowDown).
- **Confidence:** HIGH for the mechanism; **MEDIUM** for the strength of "at all," since a determined user can fall back to AT review-mode object navigation to read the options. That fallback is outside the widget's declared keyboard contract and does not make the widget operable in browse-forms mode, so the rating stands.
- **Could the developer refute this?** Partially — a developer could argue review-mode navigation makes the options readable. That is a workaround, not the pattern, and it does not restore the cursor. Rating held.
- **GAP or PREFERENCE:** GAP.
- **Fix:** Fix CRITICAL-2 and MAJOR-3 together, then verify the complete loop with an actual screen reader or a component-level `virtual-screen-reader` assertion, not by re-reading the diff.

---

### Major Findings (significantly degrades experience)

---

**MAJOR-1 — The component reimplements `<select>` in ARIA when native HTML provides the semantics and behavior for free.**

The widget is a single-select control over an array of plain strings (`options[index]` is rendered as a bare text node at `BuggyDropdown.jsx:69` and passed whole to `onSelect` at line 17). That is the textbook `<select>`/`<option>` case. The critic's non-negotiable rule applies directly: ARIA must not be used where equivalent native semantics and behavior exist.

- **User group:** All — but especially screen reader and mobile users, who get platform-optimized pickers from `<select>`.
- **WCAG / APG:** WAI-ARIA "First Rule of ARIA Use"; WCAG 4.1.2. Phase 2 of this protocol directs MAJOR when ARIA masks semantics that native HTML would supply.
- **Evidence:** `BuggyDropdown.jsx:42–72` — the full hand-rolled trigger + listbox.
- **Confidence:** HIGH that the rule applies; **MEDIUM** on whether the team can act on it, since custom styling is the usual (and often legitimate) driver.
- **Could the developer refute this?** PARTIALLY — "design requires custom option styling" is a real constraint, and a *correctly built* custom listbox is a legitimate outcome. What is not refutable is the cost: `<select>` supplies for free every one of CRITICAL-1 through CRITICAL-4, MAJOR-3, MAJOR-4, MAJOR-5, MAJOR-7, and MINOR-2. Eight defects were purchased with the styling.
- **GAP or PREFERENCE:** GAP (rule-level), with a legitimate design escape hatch.
- **Fix:** Prefer `<select id="sort" name="sort">` with a real `<label for="sort">`. If custom styling is genuinely required, do not hand-roll — port the APG Select-Only Combobox reference implementation, or adopt a maintained headless primitive that ships the full pattern, and keep this review's checklist as the acceptance criteria.

---

**MAJOR-2 — `<label htmlFor>` targets a `<button>`, which is not a labelable element; the association is spec-invalid and cross-browser-unreliable.**

`BuggyDropdown.jsx:41` binds a `<label>` to `id="dropdown-btn"`, a `<button>`. HTML defines labelable elements as `button`-*like* form controls only in the sense of `<input type=button>`; the labelable set is `input` (non-hidden), `select`, `textarea`, `output`, `progress`, `meter`, and form-associated custom elements. A `<button>` element is **not** in it.

- **User group:** Screen reader users on non-Chromium engines.
- **WCAG:** 1.3.1 Info and Relationships; 4.1.2 Name, Role, Value.
- **Evidence and its limits:** The trace shows Chromium **did** compute the association — `states.labelledby: {"type":"nodeList","relatedNodes":[{"backendDOMNodeId":14,"text":"Sort by"}]}` at `step_0002` and `step_0006` (digest-only). So on the tested engine it "works," in the specific sense that it produces the wrong-but-nonempty name of CRITICAL-1. I am explicitly **not** claiming the button is nameless. I am claiming the mechanism is out of spec and its behavior varies by engine — and no WebKit or Gecko evidence was supplied.
- **Confidence:** HIGH on the spec point; **MEDIUM** on real-world cross-browser impact, because I have measurement from exactly one engine.
- **Could the developer refute this?** PARTIALLY — "it computes fine in Chrome" is true and measured. It is not evidence about Safari or Firefox, and it is not evidence that this is the right construction. **Needs user verification**: inspect the button's computed Name in Safari's and Firefox's accessibility inspectors and compare against Chromium.
- **GAP or PREFERENCE:** GAP.
- **Fix:** Same fix as CRITICAL-1 — keep the visible `<label>` element as a styled text node (or switch it to a `<span>`), drop `htmlFor`, and wire the name with `aria-labelledby="<label-id> <button-id>"`. This is spec-valid, engine-independent, and simultaneously restores the value to the name.

---

**MAJOR-3 — The listbox has no accessible name; its computed name is the empty string.**

`BuggyDropdown.jsx:53–60` renders `<ul role="listbox">` with no `aria-label` and no `aria-labelledby`. A `<ul>` has no UA-intrinsic name to fall back on.

- **User group:** Screen reader users.
- **WCAG / APG:** WCAG 4.1.2 Name, Role, Value; WAI-ARIA APG Listbox Pattern — "the listbox must have a label."
- **Corroboration (digest-only):** `step_0003` and `step_0004` — `ax_name_role_state: {"name":"","role":"listbox", ...}`. Directly measured empty string, not inferred.
- **Confidence:** HIGH.
- **Note on the instrument:** the keyboard-a11y-tester calibration rule that name-presence checks miss UA-intrinsic names cuts the *other* way here — that rule guards against false negatives (a "Choose File" input that looks named but is not). A `<ul>` has no intrinsic name, so an empty measured name is a true positive.
- **Could the developer refute this?** NO.
- **GAP or PREFERENCE:** GAP.
- **Why this matters:** With focus on the container (which is where this implementation puts it), the container's name is the *only* orienting announcement the user gets on arrival. "Listbox" with no name, followed by silence on every arrow press, is the entire experience.
- **Fix:** Add `aria-labelledby="<visible-label-id>"` to the `<ul>`, pointing at the same visible "Sort by" label. Do not duplicate the text in an `aria-label` — reuse the visible string so the announcement and the screen agree.

---

**MAJOR-4 — Opening the dropdown never moves focus into the list; the `.focus()` call is dead code.**

`handleToggle` (`BuggyDropdown.jsx:8–13`) queues `setIsOpen(!isOpen)` at line 9 and then, in the same synchronous tick, evaluates `if (!isOpen && listRef.current)` at line 10. On the opening transition the `<ul>` has not yet rendered (`{isOpen && (...)}`, line 52), so `listRef.current` is `null`, the guard short-circuits, and `listRef.current.focus()` at line 11 never executes.

The `!isOpen` half of the guard is correct (it reads the stale pre-update value, which is exactly the "we are opening" test); the ref half is what kills it. The result is a focus-management intention with no effect — which reviews readily mistake for handled behavior.

- **User group:** Keyboard-only and screen reader users.
- **WCAG / APG:** WCAG 2.4.3 Focus Order; WAI-ARIA APG Combobox Pattern (Select-Only) — opening must either move focus to the listbox or establish `aria-activedescendant` on the trigger.
- **Corroboration (digest-only):** `step_0002` — `keystroke_sent:"Enter"`, `active_element_selector:"#dropdown-btn"`, `focus_moved:false`, while `expanded` goes `false → true` and `controls:"dropdown-list"` appears, with `new_phrases:[]` and `focus_announcement:null`. State changed, focus did not, nothing was announced.
- **Confidence:** HIGH.
- **Could the developer refute this?** NO.
- **GAP or PREFERENCE:** GAP.
- **Realist Check:** Downgraded from CRITICAL to MAJOR. **Mitigated by:** the listbox carries `tabIndex="0"` (`BuggyDropdown.jsx:58`), so a keyboard user *can* reach the options with one extra Tab. That workaround is real but undiscoverable and contradicts what `aria-haspopup="listbox"` advertises, so this is not downgraded further.
- **Fix:** Move the focus assignment out of the click handler and into a commit-time effect: `useEffect(() => { if (isOpen) listRef.current?.focus(); }, [isOpen])`. Better, fix this together with CRITICAL-2 by adopting the `aria-activedescendant` strategy, in which case focus should stay on the trigger deliberately and the trigger gains the `aria-activedescendant` and the keyboard handler.

---

**MAJOR-5 — Escape does not cancel: it commits the cursor visually while never notifying the application.**

`handleKeyDown`'s ArrowUp/ArrowDown branches (`BuggyDropdown.jsx:25–32`) mutate `selectedIndex`, which drives both `aria-selected` on the options (line 65) and the **trigger's visible text** (line 49). The Escape branch (lines 22–24) closes the popup without restoring the prior `selectedIndex`, and `onSelect` (line 17) fires only from `handleSelect`.

So: open, arrow twice, press Escape → the button now visibly reads a value the parent application was never told about. The UI reports a state the system does not hold.

Two distinct defects are tangled here: (a) `aria-selected` is being used as a *cursor*, when in a listbox it denotes *selection* — an AT observing the options during navigation is told the selection has already changed; (b) there is no cancel semantic at all.

- **User group:** Cognitive (false report of system state, no undo), screen reader (premature selection announcement in review mode), all users (silent data divergence).
- **WCAG:** 4.1.2 Name, Role, Value (reported state must match actual state); 3.2.1 On Focus is *not* violated. WAI-ARIA APG Listbox — where selection-follows-focus is used, Escape must revert to the value in effect when the listbox opened.
- **Evidence:** `BuggyDropdown.jsx:16, 22–24, 28, 32, 49, 65` — `selectedIndex` is the only state, shared by cursor and committed value; nothing restores it.
- **Confidence:** HIGH (mechanism is plain in the source). Not directly measured — the trace's goal was a commit path, not a cancel path.
- **Could the developer refute this?** NO on the mechanism. A developer could argue the parent re-syncs from props — but `options[selectedIndex]` is read from local state at line 49, so it will not.
- **GAP or PREFERENCE:** GAP.
- **Fix:** Split the two concerns into separate state: `activeIndex` (cursor, drives `aria-activedescendant` and the option highlight) and `selectedIndex` (committed value, drives `aria-selected` and the trigger's text). On open, seed `activeIndex` from `selectedIndex`. On Escape, discard `activeIndex` and leave `selectedIndex` untouched. Only `handleSelect` writes `selectedIndex` and calls `onSelect`.

---

**MAJOR-6 — Hardcoded DOM ids in a reusable component collide on any page with two instances.**

`id="dropdown-btn"` (`BuggyDropdown.jsx:43`) and `id="dropdown-list"` (line 55) are literals inside a component parameterized by `label`, `options`, and `onSelect` — i.e. one explicitly designed to be instantiated more than once. Two instances (or one component rendered twice in a mobile/desktop duplicate-DOM pattern) produce duplicate ids. Consequences: the `<label htmlFor="dropdown-btn">` of *both* instances binds to the first button; `aria-controls="dropdown-list"` on both triggers points at the first list; and any `aria-activedescendant` added by the CRITICAL-2 fix will resolve to the wrong element.

- **User group:** Screen reader users on multi-instance pages.
- **WCAG:** 4.1.2 Name, Role, Value; 1.3.1 Info and Relationships. Duplicate-id ARIA reference collision is one of the cases the protocol's duplicate-DOM-rendering check exists to catch.
- **Evidence:** `BuggyDropdown.jsx:43, 46, 55` plus the component signature at line 3.
- **Confidence:** HIGH on the mechanism; **MEDIUM** on realized impact, because I have not seen a consuming page.
- **Could the developer refute this?** PARTIALLY — "we only ever render one" is possible but undocumented and unenforced, and the props signature argues against it. **Needs user verification:** search the consuming app for multiple `<BuggyDropdown>` renders, including responsive duplicates.
- **GAP or PREFERENCE:** GAP.
- **Fix:** Generate ids per instance with React's `useId()` and derive every id and every IDREF from it (`${id}-btn`, `${id}-list`, `${id}-opt-${index}`).

---

**MAJOR-7 — The open popup survives focus leaving it, and the trigger has no keyboard handler, so the widget is inert in the state it actually occupies.**

Two absences that compound into one broken state:

1. The trigger (`BuggyDropdown.jsx:42–51`) has only `onClick`. No `onKeyDown`. Because MAJOR-4 leaves focus on the trigger after opening, **Escape does nothing, ArrowDown/ArrowUp do nothing** — and since `e.preventDefault()` is never reached, the arrow keys' default action fires and the page scrolls behind the open popup.
2. There is no `onBlur`/`focusout` handler on the wrapper and no outside-click listener. Tabbing out of the open listbox leaves the popup rendered with `aria-expanded="true"` while focus is elsewhere in the page — a stale, orphaned popup that AT will still report as expanded.

This is the protocol's **else-branch coverage** anti-pattern precisely: the Escape branch was implemented on one element and not the other; the dismiss-on-blur branch was never implemented at all.

- **User group:** Keyboard-only and screen reader users.
- **WCAG / APG:** WCAG 2.1.1 Keyboard; 2.4.3 Focus Order; WAI-ARIA APG Combobox (Select-Only) — the combobox element itself must handle Escape, ArrowDown/ArrowUp (open + move), Home, and End, and the popup must close when focus leaves the composite.
- **Corroboration (digest-only):** `step_0002` establishes the precondition — the widget really does sit open with focus on `#dropdown-btn`. The inertness in that state follows from the source (no handler bound at lines 42–51).
- **Confidence:** HIGH.
- **Could the developer refute this?** NO.
- **GAP or PREFERENCE:** GAP.
- **Fix:** Bind a keydown handler to the trigger covering Escape (close + keep focus), ArrowDown (open and move to first/selected), ArrowUp (open and move to last), Home, End, and printable-character type-ahead. Add a `focusout` handler on the wrapper that closes when `relatedTarget` is outside it, plus a pointerdown listener on `document` for outside clicks. Test **every** branch — this is the anti-pattern that gets half-fixed.

---

### Minor Findings (friction, workaround exists)

- **MINOR-1 — `aria-controls` is a dangling IDREF whenever the dropdown is collapsed.** `aria-controls="dropdown-list"` (`BuggyDropdown.jsx:46`) is always present, but `#dropdown-list` only exists while `isOpen` (lines 52–55). Real-world impact is low: most AT ignores `aria-controls` on a collapsed trigger, and `aria-expanded` carries the state that actually matters. Some validators will flag it. WCAG 4.1.2. Fix: render `aria-controls` conditionally (`aria-controls={isOpen ? listId : undefined}`), or keep the list mounted with `hidden` — the latter only if you also verify it stays out of the tab order.
- **MINOR-2 — Missing Home / End / Space / type-ahead, and Tab does not select-and-close.** `handleKeyDown` (`BuggyDropdown.jsx:21–37`) covers only Escape, ArrowDown, ArrowUp, and Enter. The APG Listbox and Select-Only Combobox patterns list Home and End as expected, printable-character type-ahead as recommended, and (for the select-only variant) Tab as select-and-close. Workaround: arrow keys reach every option. Friction scales with list length. WAI-ARIA APG Listbox Pattern.
- **MINOR-3 — `onClick` on `<li role="option">` with no keyboard handler on that element.** `BuggyDropdown.jsx:66`. Keyboard operability is preserved by the container-level Enter handler, so this is **not** a WCAG 2.1.1 failure. Static analysis (`jsx-a11y/click-events-have-key-events`, `no-noninteractive-element-interactions`) will flag it; that flag is a **partial false positive** in this context. Resolves naturally under the roving-tabindex fix. **Needs user verification** if the lint rule is being suppressed — confirm the suppression is scoped and documented rather than blanket.
- **MINOR-4 — Selection cursor is carried by a CSS class alone.** `className={index === selectedIndex ? 'selected' : ''}` (`BuggyDropdown.jsx:67`) is the only markup hook for the visible cursor. If `.selected` is a background-color change with no border, weight, or glyph, it fails WCAG 1.4.1 Use of Color and vanishes in forced-colors mode. **Unverified** — no CSS was supplied. Rated MINOR pending the stylesheet; would rise to MAJOR if confirmed color-only.

### Enhancements (best practice not met, no access barrier)

- Add `aria-setsize` / `aria-posinset` if options are ever virtualized or paginated, so "3 of 40" stays truthful.
- Consider `role="status"` confirmation of the committed sort ("Sorted by price, low to high") if the results region updates without moving focus. Once CRITICAL-1 and CRITICAL-3 are fixed the restored trigger announcement usually suffices — do not add both, or the user hears the change twice.
- `key={index}` (`BuggyDropdown.jsx:63`) is a React reconciliation smell, not an accessibility defect. Out of scope for this review; noted so it is not mistaken for one.
- Document the widget's keyboard model in the component's docblock or Storybook entry. Custom widgets carry undiscoverable shortcuts by construction.

---

## What's Missing (consolidated)

- No `aria-activedescendant` and no roving tabindex — the cursor has no representation in the accessibility tree (G1).
- No `id` on any option, foreclosing the activedescendant fix (G2).
- No accessible name on the listbox — measured `""` (G3).
- No focus restoration on any of the three close paths (G4).
- No keydown handler on the trigger, where focus actually is while the popup is open (G5).
- No dismissal on focus-out and no outside-click dismissal (G6).
- No Home/End/Space/type-ahead; Tab does not select-and-close (G7).
- No per-instance id strategy in a component built for reuse (G8).
- No cancel/revert semantics — Escape commits visually and silently diverges from application state (G9).
- No announcement of the committed value, by name change or by status region (G10).
- **Explicitly checked and clean:** no `inert` gap (the popup is conditionally rendered, so nothing hidden takes Tab focus); the decorative `▼` is correctly `aria-hidden`; `e.preventDefault()` correctly suppresses page scroll *within* the list; option wrapping (lines 27, 31) matches the APG's optional wrap behavior; `role="listbox"`/`role="option"` on `<ul>`/`<li>` is the APG-recommended markup shape.

---

## Multi-Perspective Notes

- **Screen reader user:** The widget's roles are right and its behavior is absent. The trigger announces a label and never a value; opening produces no announcement; the popup is an unnamed listbox; arrowing is silent; selecting drops focus to `body` with no confirmation; returning to the trigger produces a string identical to the one heard before the interaction began. Three of these are directly measured in the trace. A user completing the full journey cannot determine whether anything happened.
- **Keyboard-only user:** Reaches everything and is never trapped (2.1.2 is satisfied), but the interaction model contradicts what the ARIA advertises. Escape is inert where focus lands on open; arrow keys scroll the page behind the open popup; the way into the list is an undiscoverable extra Tab; and after selecting, focus resets to the document origin, forcing a full re-traversal back to the content just re-sorted.
- **Low vision user (200% zoom, magnifier, high contrast):** Not fully assessable — no CSS supplied. Two live concerns: the focus indicator on a re-roled `<ul>` container is often overridden or visually lost, and the cursor is carried by a single CSS class that may be color-only. The focus-to-`body` behavior is particularly hostile under magnification, where the viewport is thrown to the document origin with no visible focus target. No contrast ratios were measured and none are claimed.
- **Cognitive accessibility:** The Escape-does-not-cancel behavior is the standout. The control visibly reports a value the application does not hold, with no undo, no confirmation, and no distinction between "previewing" and "chosen." It also breaks the deeply learned `<select>` mental model where Escape reverts. Compounding it, the widget's behavior differs depending on which of two elements holds focus — with no visible cue as to which one that is.

---

## Verdict Justification

**REJECT**, on four grounds:

1. **Core function is inaccessible, not merely degraded.** A sort control whose value never reaches the accessible name (CRITICAL-1) and whose cursor is invisible to AT (CRITICAL-2) has no working interaction for screen reader users. That is access loss for a user category, which the severity scale defines as CRITICAL and the Realist Check forbids downgrading.
2. **The defects are measured, not inferred.** Four independent trace observations corroborate four source-code findings: `focus_moved:false` on open, `name:""` on the listbox, zero state delta on ArrowDown, `activeElement === body` after select, and a byte-identical announcement string across a completed value change. This is not design reasoning about what *might* happen.
3. **The fix set is a re-architecture, not a patch.** Working through the findings: pick a focus strategy and implement it end to end; add option ids; rewire the accessible name away from an invalid `<label for>` association; add restoration to all three close paths; add a keyboard handler to the trigger; add focus-out and outside-click dismissal; split cursor state from selection state; add per-instance ids. That is a rewrite of every behavioral line in the component. The honest recommendation is to replace it with `<select>`, or to port the APG Select-Only Combobox reference implementation wholesale rather than continue repairing this one.
4. **It would ship clean through automated testing.** Every ARIA attribute present is valid, every role is permitted in context, and the trigger computes a non-empty accessible name. axe-core has nothing to say here. That is precisely the failure class this review exists to catch, and it is the argument for treating the verdict as blocking rather than advisory.

**What would move this to REVISE:** CRITICAL-1 and CRITICAL-3 fixed and verified in a rendered accessibility tree.
**What would move it to ACCEPT-WITH-RESERVATIONS:** all four CRITICALs plus MAJOR-3, MAJOR-4, MAJOR-5, and MAJOR-7 fixed, with a screen-reader or `virtual-screen-reader` component assertion demonstrating the full open → navigate → select → confirm loop announcing correctly.

**Severity recalibrations performed (Phase 8):**
- **MAJOR-4** was downgraded from CRITICAL. *Mitigated by:* `tabIndex="0"` on the listbox (`BuggyDropdown.jsx:58`) gives keyboard users a one-extra-Tab route into the options. Undiscoverable and contrary to the advertised pattern, so no further downgrade.
- **MINOR-3** was downgraded from MAJOR. *Mitigated by:* the container-level `onKeyDown` supplies the keyboard equivalent, so the `onClick`-on-`<li>` lint flag is a partial false positive here rather than a real 2.1.1 failure.
- **MINOR-4** was held at MINOR rather than raised to MAJOR. *Mitigated by:* no CSS was supplied, so a color-only indicator is a hypothesis, not a measurement. It rises to MAJOR if the stylesheet confirms it.
- **CRITICAL-3** was tested against all four Realist questions and survives every one — realistic worst case is a full-document tab-order reset with no announcement, impact spans two user groups, and production detection is *never* (silent failure, no error, no failing test). Held at CRITICAL.
- **No finding was inflated to reach a verdict.** Where the code is right — the `aria-hidden` glyph, `aria-expanded`, `preventDefault` inside the list, wrapping navigation, conditional rendering avoiding phantom tab stops, `role="listbox"`/`role="option"` markup shape — it is named as right.

**Escalation:** Screen reader and Keyboard-only perspectives are at **HIGH** and should go to `/perspective-audit`. Low vision, Cognitive, and Environmental contrast are at **MEDIUM** and should be revisited once the stylesheet is available.

---

## Open Questions (unscored)

1. **Focus-indicator sufficiency on the `<ul role="listbox">`.** The digest reports `computed_focus_style` only for `step_0005` (`null`, on `body`, where it is meaningless). No value is reported for `step_0003`/`step_0004`, and no CSS was supplied. WCAG 2.4.7 Focus Visible and 2.4.13 Focus Appearance are **unmeasured**. keyboard-a11y-tester is the one mode that produces machine evidence for focus-indicator sufficiency — re-run and read `computed_focus_style` for the listbox steps.
2. **Is `.selected` a color-only indicator?** Determines whether MINOR-4 is MINOR or MAJOR (WCAG 1.4.1). Needs the stylesheet.
3. **Target size of the `<li role="option">` rows.** WCAG 2.5.8 requires 24×24 CSS px. `bounding_box` was not reported for the option elements (only `null` for `body` at `step_0005`), and no CSS was supplied. Unmeasured.
4. **Page-wide landmark and heading structure.** The digest's `region:{"landmark":null,"heading":null}` is explicitly scoped to the per-step focused-region field, and the digest states plainly that it does **not** establish a landmark census or a heading-order verdict. No axe-core artifact was supplied. Open, and deliberately not converted into a finding.
5. **Which keystroke produced `step_0003`?** The digest reports `step_0003` with `active_element_selector:"#dropdown-list"` but records no `keystroke_sent` for it. Given `step_0002`'s `focus_moved:false` and `goals[0].intent` ("move into the listbox"), the most likely explanation is a Tab. Confirming it would strengthen MAJOR-4 from "the `.focus()` call cannot fire" to "and here is the manual key the runner needed instead." Requires re-fetching the trace, which I could not do.
6. **Do the sibling artifacts contradict any of this?** `interactive-dropdown-focus-bug.findings.json` sits beside the trace and was **NOT READ** (out of the digest's question scope). It may contain the tool's own deterministic findings. Worth reading before this review is acted on — not to change the source-code findings, which stand on their own, but to check for anything measured that this review missed.
7. **Cross-engine accessible-name computation for `<label for>` on a `<button>`** (MAJOR-2). Measured in Chromium only. Needs a WebKit and Gecko check.
8. **Is `<BuggyDropdown>` ever rendered more than once per page?** Determines whether MAJOR-6's id collision is realized or latent. Needs a search of the consuming application, including responsive duplicate-render patterns.
9. **Instrument-tier caveat, standing.** Every trace citation above is **digest-only** — an `a11y-evidence-reader` paraphrase that I could not re-fetch at its cited handle. Additionally, `sr_announcement` and `ax_name_role_state` are the driven runner's simulated capture, not the contract's prescribed `virtual-screen-reader` assertion output, and this is not the canonical `npx playwright test` keyboard transcript. None of the CRITICAL or MAJOR findings *depend* on the trace — all are established from the component source — but anyone re-verifying should re-fetch the artifact rather than trusting this review's second-hand citations.
