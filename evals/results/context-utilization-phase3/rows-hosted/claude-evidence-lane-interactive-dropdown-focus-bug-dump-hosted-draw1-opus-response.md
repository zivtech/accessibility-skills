**VERDICT: REVISE**

**Overall Assessment**: The right APG pattern was chosen and about 60% of it was built — `aria-haspopup`, `aria-expanded`, `role="listbox"`/`role="option"`, `aria-selected`, and a correctly `aria-hidden` chevron are all present and correct. What is missing is the half that makes the pattern work for assistive technology: there is no `aria-activedescendant` and no roving tabindex, so arrow-key navigation is measurably silent; and the `<label htmlFor>` on the trigger overrides the button's content as its accessible name, so the currently selected value is never exposed to a screen reader at any point in the interaction. The advertised focus-restoration bug is real and measured, but it is not the worst thing here — it is the third-worst.

**Citation convention**: line numbers are relative to the component source exactly as supplied (line 1 = `import React, { useState, useRef } from 'react';`), cited as `BuggyDropdown.jsx:NN`. Trace citations are to `evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json`, shortened after first use to `trace.json`.

---

## Phase 0 — Test Evidence Intake

**Review type**: fresh design pass, not a fix verification. The a11y-test *Verification evidence contract* check (evidence-type mismatch on a remediation claim) does not trigger. No before/after pairing is claimed.

**Evidence actually usable for this component — exactly one artifact:**

- `interactive-dropdown-focus-bug.trace.json` — keyboard-a11y-tester driven-live session, personas `keyboard` + `screen-reader`, desktop 1280×800, 6 steps against `http://127.0.0.1:8777/interactive-dropdown-focus-bug.html`. Per the skill's evidence tiering, driven per-step trace facts (active element, `focus_moved`, AX name/role/state, `sr_announcement`, `focus_appearance`) are the same tier as codified Playwright runs. The trace contains **no journey-level verdicts** — only measured per-step facts — so calibration rule (3) does not bite: I am not accepting any judgment-layer claim here, only measurements.

**Evidence in the pack that is NOT evidence about this component — 27 files:**

Every other artifact supplied is a batch-crawl `findings/*.json` for a **different URL**. None is scoped to `interactive-dropdown-focus-bug.html`. Three specific traps in that pile, named so they are not silently absorbed:

1. **`findings/interactive-dropdown-clean.json` is a different page.** Its `"findings": []` is for `interactive-dropdown-clean.html`, a sibling fixture. It is not a clean bill of health for the component under review, and must not be cited as one.
2. **Absence of deterministic findings proves nothing.** The crawler emitted `"findings": []` for `tabs-missing-arrow-nav.json`, `toast-notification-no-role.json`, `loading-state-missing-aria-busy.json`, `expandable-section-no-button.json`, `data-table-missing-scope.json`, and others — pages whose names announce a planted defect. The deterministic layer is a detector with known blind spots, not a verdict authority. There is no crawl file for this page at all.
3. **The `focus-appearance-weak-desktop` findings are WCAG 2.4.13 — Level AAA.** They appear in 15 of the sibling files at `conformance_level: "AAA"`, `severity: "minor"`, and each carries `"Informative only."` in its own summary. Per calibration rule (4), `conformance_level` on this tool is a pass/fail gate rather than the SC's WCAG level — but 2.4.13 genuinely *is* AAA, so the label is correct by accident here. These are not AA failures, they belong to other pages, and I have not carried any of them into a finding. The same rule (1) applies to the `sr-live-region-silent-desktop` (4.1.3) entries in `async-form-vague-success.json`, `form-field-vs-summary-errors.json`, `multistep-form-error-clearing.json`, `search-focus-stays-in-input.json`, and `search-results-dynamic-clean.json`: batch-crawl silent-live-region findings are prompts to run a driven session, never failure evidence — and again, other pages.

**Evidence that does not exist and would have changed this review:**

- No axe-core scan. The skill's own prerequisite step asks whether automated checks have been run; the pack answers no. I proceeded, because the driven trace is a *stronger* tier for every claim I am making, but a contrast/name/role sweep is still owed.
- No CSS. Option row height, selected-row styling, focus-ring contrast against the real background, forced-colors behavior, and `prefers-reduced-motion` cannot be verified from the JSX alone. This constrains two findings below and one perspective alarm.
- No `virtual-screen-reader` component assertions. The announcement claims in this review rest on the trace's `sr_announcement` emulation. A VSR spoken-phrase log asserting the silence at ArrowDown would be the natural corroborating measurement, and it is the cheapest missing piece.

---

## Phase 1 — Pre-commitment Predictions

Recorded before reading the source, from component type (custom dropdown/select):

1. Focus will not restore to the trigger after Escape or after selection.
2. Arrow-key navigation will be present but incomplete — no Home/End/type-ahead.
3. The selected state will be visual-only or otherwise not announced.
4. The options container will not be referenced by the trigger (`aria-controls` missing).
5. The React ref-based focus call on open will be a no-op because the ref is null on the toggling render.
6. Nothing will dismiss the popup on outside click or Tab-out.

Results against these are in Phase 10 (Synthesis), below.

---

## Phase 2 — Semantic HTML Audit

What is **correct**, stated plainly so the calibration of the rest is legible:

- The trigger is a real `<button>` (`BuggyDropdown.jsx:42-51`), not a `div role="button"`. Native-HTML-first is satisfied.
- The chevron `<span aria-hidden="true">▼</span>` (`:50`) is correctly hidden. This is exactly the "visual text symbol as state indicator" trap in Phase 5 of the protocol, and it was handled right — `▼` would otherwise be announced as "down pointing triangle" or "black down-pointing triangle" on top of an already-announced `aria-expanded`.
- `<ul role="listbox">` with `<li role="option">` (`:53-70`) is the correct APG mapping. `role="listbox"` intentionally suppresses list semantics; that is not a finding.
- `aria-selected` is a boolean expression (`:65`), and `aria-expanded` is bound to real state (`:45`). Values are valid — no `"yes"`/`"no"` or `aria-current="true"` sloppiness.
- No layout tables, no ARIA masking bad structure, no icon-font exposure.

Landmarks and heading hierarchy are **out of scope**: this is a component-scope review of a leaf widget with no page shell supplied. The trace confirms it — `region: {landmark: null, heading: null}` at every step. I am not manufacturing a "missing `<main>`" finding against a dropdown.

One semantic defect, carried to CRITICAL-2 below: `<label htmlFor="dropdown-btn">` (`:41`). `<button>` is a labelable element, so this is valid HTML — but the accessible-name consequence is severe and measured.

---

## Phase 3 — ARIA Pattern Compliance Audit

**Pattern**: WAI-ARIA APG *Collapsible Dropdown Listbox* (button + `role="listbox"` popup). The implementation partially drifts toward the APG *Select-Only Combobox* variant, and lands cleanly in neither.

| APG requirement | Present? | Evidence |
|---|---|---|
| Trigger has `aria-haspopup="listbox"` | Yes | `:44`; `trace.json step_0001` `hasPopup: "listbox"` |
| Trigger has `aria-expanded`, synchronized | Yes | `:45`; `step_0001` `expanded: false` → `step_0002` `expanded: true` → `step_0006` `expanded: false` |
| Trigger references popup | Partly | `:46`; `controls: "dropdown-list"` present only while open (`step_0002`), absent when closed (`step_0001`) |
| Popup has `role="listbox"` | Yes | `:56`; `step_0003` `role: "listbox"` |
| Popup has an accessible name | **No** | `step_0003` `name: ""` |
| Options have `role="option"` | Yes | `:64` |
| Active option identified via `aria-activedescendant` **or** roving tabindex | **No** | Neither exists in source; `step_0004` `focus_moved: false` with no descendant reference |
| Options have `id`s (prerequisite for activedescendant) | **No** | `:62-68` — `key` only, no `id` |
| Focus moves into listbox on open | **No** (intended, dead) | `:11`; `step_0002` `focus_moved: false` |
| Focus returns to trigger on close | **No** | `step_0005` `active_element_selector: "body"` |
| Escape closes | Only from inside the popup | `:22-24`, handler bound at `:57` |
| Home / End / type-ahead | **No** | `:21-37` handles only Escape/ArrowDown/ArrowUp/Enter |
| Tab closes the popup | **No** | Tab is unhandled in `:21-37` |

The pattern is **partial**. The two gaps that matter most are the missing active-option identification and the missing name, both of which are invisible to automated tooling — which is precisely why the batch crawler found nothing anywhere near this page.

---

## Phase 4 — Focus Management Review

Measured behavior of a complete keyboard journey, from `trace.json`:

| Step | Key | Active element | `focus_moved` | New SR phrases |
|---|---|---|---|---|
| `step_0001` | Tab | `#dropdown-btn` | true | "button, Sort by, not expanded, has popup listbox" |
| `step_0002` | Enter | `#dropdown-btn` | **false** | **[]** |
| `step_0003` | Tab | `#dropdown-list` | true | "listbox, orientated vertically" |
| `step_0004` | ArrowDown | `#dropdown-list` | **false** | **[]** |
| `step_0005` | Enter | **`body`** | true | **[]** |
| `step_0006` | Shift+Tab | `#dropdown-btn` | true | "button, Sort by, not expanded, has popup listbox" |

Read as a journey: activating the trigger moves nothing and says nothing; reaching the options requires an undocumented extra Tab; arrowing says nothing; committing a choice says nothing and ejects focus to `<body>`; and the user must reverse-tab to find their way back to the control they were just operating. The goal declared in the trace — *"open the sort dropdown, move into the listbox, pick an option, verify focus returns to trigger"* — completes on the first three clauses and fails on the fourth.

Note `step_0006` `bounding_box.width` grew from 73.66 to 130.72 and `text` changed from `"Newest▼"` to `"Price: low to high▼"`. The selection *did* commit. The mechanism works; the communication around it does not.

---

## Phase 5 — State Communication Audit

The single most useful measurement in this pack is the pair of numbers at `step_0004`:

- `focus_appearance.changed_area: 6555` px², `contrast: 5.67`, `contrast_pass: true`, `focus_visible.border_band: 0.3287` — a large, high-contrast visual change fired on ArrowDown.
- `sr_announcement.new_phrases: []`, `live_announcements: []`, `focus_announcement: null` — nothing was conveyed.

That is the entire design failure in two lines: the state change is loud visually and silent programmatically. The `className={index === selectedIndex ? 'selected' : ''}` cursor at `:67` works. The ARIA channel that should carry the same information does not fire, because `aria-selected` is being mutated on a descendant that neither holds focus nor is pointed at by `aria-activedescendant`.

Everything else in the state audit: no loading state, no error state, no disabled state, no readonly state, no timeouts — none apply to this component, and I am not inventing findings for absent features.

---

## Critical Findings (blocks access)

### CRITICAL-1 — Arrow-key navigation is measurably silent: no `aria-activedescendant`, no roving tabindex

`BuggyDropdown.jsx:53-70` renders a `role="listbox"` with `tabIndex="0"` on the container and no `id` on any `role="option"` child. `handleKeyDown` (`:25-32`) moves `selectedIndex`, which flips `aria-selected` (`:65`) — but DOM focus never leaves the `<ul>` and no `aria-activedescendant` is set, so no assistive technology has any reason to announce the change.

- **Measured**: `trace.json step_0004`: `keystroke_sent: "ArrowDown"`, `active_element_selector: "#dropdown-list"`, `focus_moved: false`, `sr_announcement.new_phrases: []`, `focus_announcement: null` — against `focus_appearance.changed_area: 6555` at `contrast: 5.67` in the same step.
- **User group**: screen reader users (all of them). Secondarily, speech-recognition users, who have no addressable target for an individual option.
- **Expected**: per the WAI-ARIA APG *Listbox* pattern, the listbox must identify its active option either by moving DOM focus to it (roving tabindex, `tabindex="0"` on the active option and `-1` on the rest) or by setting `aria-activedescendant` on the focused container to the active option's `id`. Every arrow keypress must retarget it. WCAG 4.1.2 Name, Role, Value.
- **Realistic worst case**: the user arrows through an unlabelled set of unknown length and presses Enter on an option they cannot identify. They then receive no confirmation of what they chose (see CRITICAL-2), so they cannot even detect the error afterward. There is no workaround inside this widget.
- **Fix**: give each option a stable `id` (`id={`${listId}-opt-${index}`}`), set `aria-activedescendant={`${listId}-opt-${selectedIndex}`}` on whichever element holds focus, and keep `aria-selected` as-is. Do **not** solve this with an `aria-live` region announcing the option name — that is the *Broadcast vs. Association* anti-pattern; the active-descendant relationship is the correct mechanism and lets AT announce role, position, and selected state together.
- **Confidence**: HIGH on impact (measured silence). MEDIUM on the exact SC mapping — see the refutation below.
- **Developer could refute?** Partly, and it deserves a straight answer. A developer can correctly say "`aria-selected` *is* in the DOM, so the state is programmatically determinable — 4.1.2 is satisfied." Under a static-inspection reading of 4.1.2 that is arguable. It does not rescue the experience: AT announces on focus change and on `aria-activedescendant` change, not on attribute mutation of an unfocused descendant, which is exactly what `step_0004` measured. If the SC mapping is contested, the APG *Listbox* pattern requirement is not — and the user impact is identical either way. Severity stands on impact, not on which citation wins.

```
### A11y Evidence Finding
finding_id: dropdown-listbox-no-active-descendant
fingerprint: derivation recipe, not computed — sha256("BuggyDropdown.jsx|listbox|no-active-descendant|4.1.2")[0:16]; this is a read-only pass with no execution, and a hand-written hex string would be a fabricated value
source: evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json step_0004 (driven-live, personas keyboard+screen-reader, desktop 1280x800)
wcag_or_apg: WAI-ARIA APG Listbox pattern (aria-activedescendant / roving tabindex); WCAG 2.2 4.1.2 Name, Role, Value
section_508_fpc_context: not in scope — component-scope review, no declared Revised Section 508 obligation in the request
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, keyboard=HIGH, low-vision=MEDIUM, cognitive=MEDIUM
evidence: BuggyDropdown.jsx:53-70 (no option ids, no aria-activedescendant, no roving tabindex); trace.json step_0004 focus_moved=false, sr_announcement.new_phrases=[], focus_announcement=null, focus_appearance.changed_area=6555 contrast=5.67
reproduction_steps: Tab to #dropdown-btn; Enter; Tab to #dropdown-list; ArrowDown; observe zero new screen-reader phrases while the visual selection cursor moves
expected_behavior: each ArrowDown/ArrowUp announces the newly active option's name, position, and selected state
actual_behavior: no announcement of any kind; only a visual class change on the li
trend: new (no prior baseline in the supplied pack)
```

### CRITICAL-2 — The trigger's accessible name is the field label only; the selected value is never exposed to AT

`BuggyDropdown.jsx:41` associates `<label htmlFor="dropdown-btn">{label}</label>` with the `<button>`. In the tested browser this label **wins** the accessible-name computation over the button's own subtree content, so the button's name is the static field label and the dynamic value rendered at `:49` is excluded from it.

- **Measured, twice**: `trace.json step_0001` — `name: "Sort by"`, `labelledby.relatedNodes[0].text: "Sort by"`, while `text: "Newest▼"`. `trace.json step_0006`, *after* a successful selection — `name: "Sort by"` still, while `text` has changed to `"Price: low to high▼"`. The visible value changed; the accessible name did not move. Both steps announce identically: `"button, Sort by, not expanded, has popup listbox"`.
- **User group**: screen reader users.
- **Why this is CRITICAL and not MAJOR**: there is no second channel. A sighted user reads the current sort off the button. A screen reader user cannot: the name omits it, `aria-selected` inside the listbox is never announced (CRITICAL-1), and there is no live region. In browse mode the virtual buffer renders a button as its accessible name, so the inner text is not separately reachable either. The result is that a screen reader user can **set** a sort order but can never **determine** the current one — before, during, or after the interaction. That is total loss of an information channel that every other user has, which is the definition in the severity scale, and it is a silent failure: axe-core sees a button with a non-empty accessible name and passes it, and so does the crawler's `missing-accessible-name` check (calibration rule 2 — name-presence checks do not evaluate whether the name is the *right* name).
- **Expected**: WCAG 4.1.2 requires that values a user can set be programmatically determinable. Per the APG *Select-Only Combobox* / *Collapsible Listbox* examples, the trigger's name concatenates the field label with the current value.
- **Fix (smallest correct change)**: drop `<label htmlFor>` — it is the wrong element for a button anyway — and use a self-referencing labelledby:
  ```jsx
  <span id="sort-label">{label}</span>
  <button id="dropdown-btn" aria-labelledby="sort-label dropdown-btn" ...>
    {options[selectedIndex]}
    <span aria-hidden="true">▼</span>
  </button>
  ```
  This computes to `"Sort by Newest"`, and updates on every commit. The `aria-hidden` chevron is correctly excluded from the traversal because it is not itself directly referenced.
- **Confidence**: HIGH for the tested environment. **Honest caveat**: HTML-AAM's ordering for `<button>` (aria-labelledby → aria-label → subtree → title) does not obviously give a `<label for>` precedence over subtree content, and implementations have historically differed. The trace measures Chrome's actual computation directly, so for the environment under test this is a fact rather than an inference. If the target matrix includes Firefox/WebKit, verify there before assuming the same result — but note that *either* outcome is a defect: if the label loses, the field label "Sort by" disappears from the name instead. The fix above is correct under both computations, which is why I am confident in the remedy even where I am not fully confident in the mechanism.

```
### A11y Evidence Finding
finding_id: dropdown-trigger-value-not-in-accessible-name
fingerprint: derivation recipe, not computed — sha256("BuggyDropdown.jsx|dropdown-btn|value-not-in-accname|4.1.2")[0:16]; see CRITICAL-1 note on why no digest is asserted
source: evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json step_0001 and step_0006
wcag_or_apg: WCAG 2.2 4.1.2 Name, Role, Value; WAI-ARIA APG Select-Only Combobox / Collapsible Dropdown Listbox naming
section_508_fpc_context: not in scope — component-scope review, no declared Revised Section 508 obligation in the request
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, cognitive=MEDIUM, keyboard=LOW
evidence: BuggyDropdown.jsx:41 label htmlFor + :49 value in button subtree; trace.json step_0001 name="Sort by" / text="Newest▼"; step_0006 name="Sort by" / text="Price: low to high▼"
reproduction_steps: Tab to #dropdown-btn and listen; complete a selection; Shift+Tab back to #dropdown-btn and listen again — the announcement is byte-identical across a changed value
expected_behavior: "Sort by Newest, button, collapsed, has popup listbox", updating to "Sort by Price: low to high" after commit
actual_behavior: "button, Sort by, not expanded, has popup listbox" both times; the value is never spoken
trend: new (no prior baseline in the supplied pack)
```

---

## Major Findings (significantly degrades experience)

### MAJOR-1 — Focus is destroyed on close and reverts to `<body>`; it never returns to the trigger

`handleSelect` (`:15-19`) and the Escape branch (`:22-24`) both set `isOpen` false. The `<ul>` is conditionally rendered (`:52`), so React unmounts the element that currently holds focus, and the browser resets the active element to `<body>`. Neither path calls `.focus()` on the trigger.

- **Measured**: `trace.json step_0005`: `keystroke_sent: "Enter"`, `active_element_selector: "body"`, `tag: "body"`, `is_body: true`, `role: "none"`, `dom_order_index: -1`, `focus_moved: true`, `sr_announcement.new_phrases: []`. `step_0006` then shows the user pressing Shift+Tab to get back to `#dropdown-btn`.
- **User group**: keyboard-only and screen reader users.
- **Why this matters beyond "focus is lost"**: on the isolated fixture page, Shift+Tab happens to land back on the trigger. On a real page, focus reset to `<body>` means the *next* Tab restarts from the top of the document. A user who sorts a product listing is thrown back to the site header and must re-traverse the entire page to return to the results they just re-sorted. The trace's tidy recovery is an artifact of the fixture's short tab ring, not a property of the fix.
- **Expected**: WCAG 2.4.3 Focus Order; APG *Collapsible Dropdown Listbox* — "when the listbox closes, focus returns to the button."
- **Fix**: see the architectural recommendation below — under the recommended restructure this finding disappears rather than being patched, because focus never leaves the trigger in the first place. If the current two-element structure is retained instead, store a ref to the button and call `btnRef.current.focus()` inside a `useEffect` keyed on `isOpen`, not synchronously in the handler (a synchronous call fires before the unmount and is discarded).
- **Confidence**: HIGH. Measured. Not refutable.
- **Severity note**: this is the top of the MAJOR band, not CRITICAL. Access is not lost — the selection commits correctly (`step_0006` text `"Price: low to high▼"`) and the user can recover by Tab or Shift+Tab. *Mitigated by:* a working, if punishing, keyboard recovery path.

### MAJOR-2 — Focus never enters the listbox on open: `listRef.current.focus()` at `:11` is dead code

`handleToggle` (`:8-13`) calls `setIsOpen(!isOpen)` and then immediately tests `listRef.current`. On that render the `<ul>` does not exist yet (`:52` still evaluates `isOpen === false`), so `listRef.current` is `null`, the guard short-circuits, and `.focus()` never runs.

- **Measured**: `trace.json step_0002`: `keystroke_sent: "Enter"`, `expanded: true` (the popup *did* open), `active_element_selector: "#dropdown-btn"`, `focus_moved: false`, `sr_announcement.new_phrases: []`. The user then needed `step_0003` — an extra, undiscoverable Tab — to reach `#dropdown-list`.
- **Precision matters here**: the *stale-closure* read of `!isOpen` is actually correct for the intent ("we are opening"). The bug is purely ref timing, not the stale value. Blaming the closure would send the developer to fix the wrong line.
- **User group**: keyboard-only (extra undiscoverable step) and screen reader (a popup opened and nothing was said — `new_phrases: []`).
- **Expected**: APG *Collapsible Dropdown Listbox* moves focus into the listbox on open. WCAG 2.4.3.
- **Fix**: `useEffect(() => { if (isOpen) listRef.current?.focus(); }, [isOpen])` — or, preferably, adopt the activedescendant model where focus intentionally stays on the trigger and this code is deleted.
- **Confidence**: HIGH. Both the code path and the measurement agree.

### MAJOR-3 — Escape is unreachable from the state the widget actually lands in

`handleKeyDown` is bound only to the `<ul>` (`:57`). The `<button>` (`:42-51`) has `onClick` and nothing else. Because MAJOR-2 leaves focus on the button after opening, the state the user is guaranteed to occupy immediately after opening is the one state in which Escape does nothing.

- **Evidence**: `:57` handler binding vs. `:42-51` button props; `trace.json step_0002` proves focus is on `#dropdown-btn` with the popup open.
- **This is the *else-branch coverage* anti-pattern** from the protocol's prior-third-party-audit list (item 4): the Escape handler covers one branch (focus-inside-list) and misses the other (focus-on-trigger), and the missed branch is the default one.
- **User group**: keyboard-only, screen reader.
- **Expected**: APG requires Escape to close the popup from anywhere within the composite widget. WCAG 2.1.1 is not violated (the widget is still operable), so this maps to the APG pattern requirement plus 2.4.3.
- **Fix**: bind the keydown handler at the wrapper (`:40`) or on the trigger, so both branches are covered by one handler.
- **Confidence**: HIGH.
- *Mitigated by:* pressing Enter on the focused trigger re-invokes `handleToggle` and closes the popup, so there is an escape route — just not the one every user's muscle memory reaches for.

### MAJOR-4 — The listbox has no accessible name

`:53-60` — the `<ul role="listbox">` has `id`, `role`, `tabIndex`, and `className`, but no `aria-label` or `aria-labelledby`.

- **Measured**: `trace.json step_0003`: `ax_name_role_state.name: ""`; announcement is the bare `"listbox, orientated vertically"`.
- **User group**: screen reader.
- **Expected**: APG *Listbox* pattern requires the listbox be labelled, normally via `aria-labelledby` pointing at the visible field label. WCAG 4.1.2 / 1.3.1.
- **Fix**: `aria-labelledby="sort-label"` on the `<ul>`, reusing the label span introduced in the CRITICAL-2 fix.
- **Confidence**: HIGH.
- **Severity calibration**: this stays MAJOR *in the shipped state*, because MAJOR-2 means the user arrives at the listbox by a bare Tab from an origin the widget did not control — there is no reliable context to infer from. Once MAJOR-2 is fixed so activation flows directly from the named trigger into the listbox, the realistic impact drops and this becomes MINOR. Recording the conditionality rather than picking one number and defending it.

### MAJOR-5 — Escape does not cancel: the trigger displays an uncommitted value

`:49` renders `options[selectedIndex]` as the button's visible text, and the arrow branches (`:25-32`) mutate `selectedIndex` directly while browsing. `onSelect` is only called on commit (`:17`). So arrowing to an option and pressing Escape (`:22-24`) closes the popup and leaves the trigger displaying an option the user never chose, while the parent's state still holds the previous value.

- **Evidence**: source only — `:5`, `:27-32`, `:49`, `:22-24`. This path is **not** in the trace; the trace's Escape branch was never exercised. Labeling that explicitly: this is code reasoning, not measured fact, and would be stronger with a driven Escape-after-arrow step.
- **User group**: all users, most acutely cognitive and low-vision (a magnified viewport shows a control whose label silently contradicts application state) — but screen reader users are the ones who cannot detect the discrepancy at all, since neither value is announced.
- **Expected**: APG *Listbox* — "Escape: closes the listbox **without changing the value**." WCAG 4.1.2 (the control's presented value does not correspond to the state it controls).
- **Fix**: separate cursor from commitment. Keep `activeIndex` (moves on arrow) distinct from `selectedIndex` (moves only on commit); render `options[selectedIndex]` on the trigger, drive `aria-activedescendant` and the visual cursor from `activeIndex`, and reset `activeIndex = selectedIndex` on close.
- **Confidence**: HIGH on the code behavior. MEDIUM that it is MAJOR rather than MINOR — the failure requires arrow-then-Escape, which is not the modal path.

### MAJOR-6 — Nothing dismisses the popup on Tab-out or outside click; `aria-expanded` goes stale

Tab is unhandled in `handleKeyDown` (`:21-37`), and there is no `onBlur`/`focusout` handler and no document-level click listener. Tabbing out of the `<ul>` moves focus into the page behind an open, still-mounted listbox, with the trigger still reporting `aria-expanded="true"`.

- **Evidence**: `:21-37` (no Tab branch), `:40-74` (no blur or outside-click handling). Scale from the trace: `step_0003` `bounding_box: {x:16, y:53, width:1248, height:54}` — the popup spans 1248 of 1280 available px, so the orphaned overlay covers the full content width.
- **User group**: keyboard-only, low vision, mouse users.
- **Why it matters**: a full-width overlay left floating over the content is a live WCAG 2.4.11 *Focus Not Obscured* risk for whatever the user tabs to next, and the stale `aria-expanded="true"` misreports the widget's state to AT indefinitely.
- **Expected**: APG *Listbox* — Tab closes the popup (optionally committing) and moves on. WCAG 2.4.3, 2.4.11.
- **Fix**: handle Tab in the keydown branch to close before the move; add a `focusout` handler on the wrapper that closes when `relatedTarget` is outside it; add a document `pointerdown` listener for outside clicks.
- **Confidence**: HIGH on the code gap; MEDIUM on the 2.4.11 consequence, which depends on CSS not supplied.

### MAJOR-7 — Hardcoded DOM ids collide when the component renders more than once

`id="dropdown-btn"` (`:43`) and `id="dropdown-list"` (`:55`) are literals in a component whose entire prop API (`label`, `options`, `onSelect`) is built for reuse.

- **Evidence**: `:43`, `:46`, `:55`, and the `htmlFor` at `:41`.
- **Consequence with two instances on a page** (a sort dropdown and a filter dropdown; or the duplicate mobile/desktop render the protocol calls out explicitly): every `<label htmlFor="dropdown-btn">` binds to the *first* button, so the second dropdown's label points at the wrong control; every `aria-controls="dropdown-list"` resolves to the first list; and the CRITICAL-2 fix's `aria-labelledby` self-reference would resolve across instances. The associations do not merely degrade — they cross-wire.
- **User group**: screen reader.
- **Expected**: WCAG 4.1.2 / 1.3.1 require associations that actually resolve. The protocol's *DOM-verification required* rule (prior-audit item 9) applies: any `aria-*` association must be verified to resolve in the rendered output.
- **Fix**: `const id = useId();` and derive `${id}-btn`, `${id}-list`, `${id}-label`, `${id}-opt-${index}`.
- **Confidence**: HIGH that the code is unsafe; the *impact* is conditional. If this component is guaranteed single-instance per page, this drops to ENHANCEMENT. Given a generic `label`/`options` API, multi-instance is the expected deployment, so I am rating for that.

### MAJOR-8 — Option rows measure roughly 18 CSS px tall, below the 24×24 minimum — **Needs user verification**

Each `<li role="option">` carries an `onClick` (`:66`), making it a pointer target subject to WCAG 2.5.8 *Target Size (Minimum)*.

- **Derivation, shown so it can be checked**: `trace.json step_0003` gives the `<ul>` `bounding_box.height: 54` and `text: "Newest\nPrice: low to high\nRating"` — three options. 54 ÷ 3 = 18 CSS px per row. The `width: 1248` (viewport 1280 minus the 16 px body margins visible in `x: 16`) indicates the `<ul>` carries no horizontal padding, consistent with a reset list where the rows are bare line boxes.
- **Why the 2.5.8 exceptions do not apply**: the *spacing* exception fails — 24 px diameter circles centred on rows stacked 18 px apart intersect. The *equivalent control* exception fails — the keyboard path is not "another control on the same page." The *user-agent* exception fails — this is author-styled markup.
- **User group**: motor-impaired pointer and touch users; magnifier users, for whom an 18 px row is a small target relative to a magnified pointer.
- **Fix**: give `[role="option"]` a `min-height: 24px` (44 px recommended) with matching padding.
- **Confidence**: **MEDIUM**, and I am not going to launder it. The per-option box was never measured; it is inferred from a container box divided by an option count. **Concrete verification**: in DevTools, select a single `<li role="option">` on the rendered page and read its computed height. If it is ≥ 24 px, this finding is void and the 54 px container is being reported with padding I have not accounted for. No CSS was supplied with the review, which is why this cannot be settled from the artifacts on hand.

---

## Recommended Architectural Fix (collapses MAJOR-1, -2, -3, and half of -6)

Findings MAJOR-1 through MAJOR-3 are all symptoms of one decision: DOM focus is supposed to travel into a conditionally-rendered popup and back out again. Every bug in that cluster is a timing or branch-coverage failure of that travel.

The APG *Select-Only Combobox* pattern removes the travel entirely, and is the smaller change:

```jsx
<span id={`${id}-label`}>{label}</span>
<button
  id={`${id}-btn`}
  role="combobox"                    // aria-haspopup="listbox" is implicit
  aria-expanded={isOpen}
  aria-controls={`${id}-list`}
  aria-labelledby={`${id}-label ${id}-btn`}
  aria-activedescendant={isOpen ? `${id}-opt-${activeIndex}` : undefined}
  onClick={handleToggle}
  onKeyDown={handleKeyDown}          // one handler, all branches
>
```
…with the `<ul>` losing `tabIndex` and `onKeyDown` entirely, and each `<li>` gaining `id={`${id}-opt-${index}`}`.

Consequences: focus never leaves the trigger, so there is nothing to restore (MAJOR-1 void) and nothing to move on open (MAJOR-2 void); one keydown handler serves every state, so Escape works everywhere (MAJOR-3 void); Tab naturally leaves the trigger, needing only a `focusout` close (MAJOR-6 halved); and `aria-activedescendant` supplies exactly what CRITICAL-1 is missing.

**Stated uncertainty**: for `role="combobox"` on a non-input element, how browsers expose the *value* (the button's own text) varies more than the name computation does. The `aria-labelledby` self-reference in CRITICAL-2 is what I actually rely on for value exposure, and it works on a plain `<button>` today with or without the combobox role. If the team prefers not to take on `role="combobox"`, keep the plain button, keep `aria-haspopup="listbox"`, move the keydown handler up to the wrapper, and add `aria-activedescendant` to the `<ul>` while restoring focus explicitly on close — that route needs the MAJOR-1/-2 patches, but it is the more conservative change.

---

## Minor Findings (friction, workaround exists)

- **`aria-controls` dangles while closed** — `:46` references `dropdown-list`, which does not exist in the DOM until `:52` renders it. *Mitigated by:* the browser drops the unresolvable IDREF cleanly (`trace.json step_0001` shows no `controls` key in the button's states, and it appears at `step_0002` when the target exists), and AT support for `aria-controls` is minimal in practice. Bind it conditionally on `isOpen` for hygiene.
- **Missing Home / End / PageUp / PageDown / type-ahead** — `:21-37` handles only four keys. The APG *Listbox* keyboard interaction table specifies Home and End (jump to first/last) and printable-character type-ahead. With three options this is negligible friction; with thirty options it becomes MAJOR. Rating for the fixture, flagging the scaling.
- **Options are not focusable and have no keyboard handler of their own** — `:62-68` has `onClick` only. This is *correct* under the activedescendant model and I am not flagging it as a defect; noting it only because a `jsx-a11y/click-events-have-key-events` lint hit here would be a false positive, and suppressing it silently would be worse than recording why.

## Enhancements (best practice, no access barrier)

- **Focus indicator is the browser default and thin.** `computed_focus_style` is identical at every stop: `outline: auto`, `1px`, `rgb(0, 95, 204)`, `offset 0`, no box-shadow. Measured indicator contrast: `2.98` at `step_0002` and `2.53` at `step_0006` on the trigger; `5.67` at `step_0004` on the listbox. **This is WCAG 2.4.13 Focus Appearance, which is Level AAA — not an AA conformance failure.** WCAG 2.4.7 *Focus Visible* (AA) is satisfied: `focus_visible.visible: true` at all five measured stops. Recorded as an enhancement with the AAA level stated explicitly, because the same measurement appears 15 times in the sibling findings files at `severity: "minor"` / `"Informative only."` and is easy to over-promote. A 2 px custom outline at ≥ 3:1 would clear the AAA bar and is cheap.
- **No usage hint for the interaction model.** With the current structure, discovering that Tab (not Enter, not ArrowDown) is what reaches the options is trial and error. Under the recommended restructure this evaporates. Not worth a finding on its own.
- **`prefers-reduced-motion`** — no animation exists in the supplied JSX. LOW relevance; unverifiable without CSS.

---

## What's Missing (gaps, unhandled edge cases, unstated assumptions)

**In the component:**
- No `aria-activedescendant`, no option `id`s, no roving tabindex — the active-option channel does not exist at all.
- No focus restoration on either close path.
- No `focusout` or outside-click dismissal; no Tab handling.
- No `useId()` — every id is a page-global literal.
- No empty-`options` guard: `options[selectedIndex]` at `:49` renders `undefined` if `options` is `[]`, leaving the trigger with no visible text and (after the CRITICAL-2 fix) an accessible name of just the field label. `handleKeyDown`'s ArrowUp branch (`:31`) would also compute `options.length - 1 === -1`. Small, but it is a state the component accepts and does not handle.
- No cursor/commitment separation (MAJOR-5's root).
- No disabled-option support. Not a defect — the `options` prop is plain strings — but worth naming as an assumption that will break the pattern the moment options become objects.

**In the evidence:**
- **No CSS.** This blocks direct verification of MAJOR-8 (target size), the real-background focus contrast, selected-row contrast, forced-colors behavior, and reduced-motion. Three separate findings and two perspective alarms are constrained by this single absence — it is the highest-value missing artifact.
- **No axe-core scan.** The skill's prerequisite step is unanswered. It would not have found either CRITICAL (a button with a name passes; a listbox without activedescendant passes), which is itself the argument for this review existing — but the pack should say so rather than leave it blank.
- **No `virtual-screen-reader` component assertions.** The announcement claims here rest on the trace's SR emulation. A VSR spoken-phrase log asserting `phrases after ArrowDown = []` alongside the structural absence would satisfy the skill's "silence is defect evidence only alongside the structural absence" rule with two independent tools instead of one.
- **No driven Escape step.** The trace never presses Escape. MAJOR-3 and MAJOR-5 are therefore code-reasoned, not measured, and are labeled as such above.
- **No mobile viewport or duplicate-render run.** MAJOR-7's id collision is exactly what a mobile+desktop duplicate render would expose, and the trace is desktop-only.
- **No batch-crawl findings file for the page under review**, and empty findings files for several pages with planted defects — so nothing in the 27 sibling artifacts can be read as corroborating anything about this component in either direction.

---

## Multi-Perspective Notes

**Screen reader user (NVDA / JAWS / VoiceOver)**: This is where the component fails hardest, and every claim is measured. Activating the trigger announces nothing (`step_0002` `new_phrases: []`). Arriving at the popup announces `"listbox, orientated vertically"` — no name, no option count, no current position (`step_0003` `name: ""`). Arrowing announces nothing (`step_0004`). Committing announces nothing and drops focus to `<body>` (`step_0005`). Returning to the trigger announces `"button, Sort by, not expanded, has popup listbox"` — identical before and after the value changed (`step_0001` vs `step_0006`). Across a complete successful interaction, the total information conveyed about the user's own choice is zero. Every ARIA attribute in the component is individually valid; the relationships that would make them speak were never wired.

**Keyboard-only user**: Operable but incoherent. Enter on the trigger opens something that does not receive focus; a Tab that no affordance advertises is required to reach the options; arrows work and are visually clear (`step_0004` `changed_area: 6555` at `5.67:1` — the sighted keyboard experience is genuinely fine); Enter commits and then ejects focus to `<body>`, which on any real page means the next Tab restarts at the document top. Escape works in the one state the user is least likely to be in. No keyboard trap exists — 2.1.2 is satisfied — and the task does complete.

**Low vision user (200% zoom, magnifier, high contrast)**: Focus indicators are present at every stop (`focus_visible.visible: true` ×5) but are the 1 px browser default measuring 2.53–2.98:1 on the trigger — passing 2.4.7 (AA), missing 2.4.13 (AAA). The 1248 px-wide popup that never auto-dismisses (MAJOR-6) is a 2.4.11 obscuring risk for whatever gains focus behind it. Option rows derive to ~18 px (MAJOR-8, unverified). The trigger's visible label changing mid-browse without commitment (MAJOR-5) is disorienting under magnification, where the trigger and the option list may not be in view together. Reflow and forced-colors are unassessable — no CSS.

**Cognitive accessibility**: The interaction model is internally inconsistent — Enter on the trigger opens, Enter in the list commits, Enter on the trigger again closes, Escape works in one state only. The trigger displaying an uncommitted browsed value (MAJOR-5) is a direct consistency violation: the control reports a state that is not the application's state. No destructive actions, no timeouts, no redundant entry, no authentication — 3.3.4, 3.3.7, and 3.3.8 are not in play. No error messaging exists to evaluate.

**Vestibular & motion**: No animation, transition, parallax, or autoplay in the supplied source. LOW — with the caveat that CSS was not supplied and a `.dropdown-list` transition could exist outside what was reviewed.

**Auditory access**: No `<video>`, no `<audio>`, no auditory alerts. LOW, definitively.

**Environmental contrast**: Measured focus-indicator contrast is 2.53–2.98:1 on the trigger (AAA-only concern). Selected-row styling is class-driven (`:67`) with unsupplied CSS, so whether the selected state survives forced-colors mode — and whether it relies on color alone — cannot be determined. The `.selected` class being the *only* cursor indicator makes 1.4.1 a live question the CSS must answer.

### Perspective Alarm Levels

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | **HIGH** | Custom composite widget; measured zero announcements at 3 of 6 steps; accessible name omits the control's value |
| Keyboard-only | **HIGH** | Focus never enters popup on open; focus reverts to `body` on close; Escape branch unreachable from the default state |
| Low vision | MEDIUM | Derived ~18 px option rows; full-width non-dismissing overlay (2.4.11 risk); trigger label mutates while browsing |
| Cognitive | MEDIUM | Inconsistent key semantics across states; trigger displays uncommitted value; undiscoverable Tab-to-enter-list |
| Vestibular & motion | LOW | No animation in supplied source (CSS not reviewed) |
| Auditory access | LOW | No media elements, no auditory alerts |
| Environmental contrast | MEDIUM | Selected-state cursor is class-only with unsupplied CSS; forced-colors and color-alone unverifiable |

**Escalation**: Screen reader and Keyboard-only are at HIGH. Both warrant deep review via `/perspective-audit` before this ships.

---

## Phase 10 — Synthesis: Predictions vs. Findings

| # | Prediction | Outcome |
|---|---|---|
| 1 | Focus won't restore after Escape/selection | **Confirmed and measured** (`step_0005` → `body`) |
| 2 | Arrow navigation present but incomplete | **Confirmed** — but for a reason I did not predict. I expected missing Home/End/type-ahead (true, MINOR). The real defect is that the arrows that *do* exist are programmatically silent. |
| 3 | Selected state not announced | **Confirmed**, and worse than predicted — not announced *anywhere*, including on the trigger |
| 4 | Options container not referenced | **Wrong.** `aria-controls` is present and correct at `:46`. Recording the miss. |
| 5 | React ref focus call is a no-op | **Confirmed and measured** (`step_0002` `focus_moved: false`) |
| 6 | No outside-click / Tab-out dismissal | **Confirmed** |

**What surprised me**: CRITICAL-2. Nothing in the component-type priors points at "a valid `<label htmlFor>` on a valid `<button>` silently strips the control's value out of its accessible name," and it is the finding with the widest blast radius — it is the reason there is no fallback channel when CRITICAL-1 goes silent. It is also the finding most likely to survive a remediation pass, because it looks like good practice: a label associated with a control reads as a fix, not a bug. Two of the "Accessibility Features Present" claimed in the fixture header — *"aria-selected on items"* and *"Label association via htmlFor"* — are precisely the two attributes that are actively causing the CRITICAL findings. Present, valid, and inert.

**What I under-weighted going in**: the id-collision exposure (MAJOR-7). Hardcoded ids in a props-driven reusable component are a structural certainty, not a possibility, and I did not predict it.

---

## Verdict Justification

**REVISE**, not REJECT. The pattern selection is right, the semantics are right, and roughly 60% of the APG listbox implementation is correct and worth keeping. The failures are wiring failures — missing relationships between elements that already exist — not a wrong architecture. The recommended restructure is roughly 20 lines and removes four findings outright. REJECT would signal "start over," which would be inaccurate and would throw away correct work.

**REVISE, not ACCEPT-WITH-RESERVATIONS**, because two CRITICAL findings mean a screen reader user can neither perceive which option they are on while navigating nor determine which option is currently selected at any point — before, during, or after the interaction. Both are measured, not argued. That is not a reservation; it is a blocker.

**Recalibrations applied in Phase 8:**

- **MAJOR-1 (focus reverts to `body`) was considered for CRITICAL and held at MAJOR.** *Mitigated by:* the selection itself commits correctly (`step_0006` confirms the value changed) and Tab/Shift+Tab recovers. Access is degraded, not lost. Noted that the trace's clean Shift+Tab recovery is an artifact of the fixture's short tab ring and will be materially worse on a real page.
- **CRITICAL-2 was considered for MAJOR and held at CRITICAL.** It survived all four Realist Check questions: realistic worst case is that a screen reader user can never determine the current sort order; the affected group is all screen reader users, not a slice; detection is *never* — axe passes it, the crawler's name-presence check passes it (calibration rule 2), and only a user report or this kind of review surfaces it; and the severity is not review momentum, because the compounding with CRITICAL-1 removes the only alternative channel.
- **MAJOR-4 (unnamed listbox) is conditional and recorded as such** — MAJOR while MAJOR-2 leaves the user arriving by bare Tab, MINOR once activation flows from the named trigger.
- **MAJOR-7 (id collision) is conditional on multi-instance deployment** and drops to ENHANCEMENT if single-instance is guaranteed. Rated for the expected deployment given the component's prop API.
- **MAJOR-8 (target size) is MEDIUM confidence, derived rather than measured**, and carries an explicit verification step rather than being asserted or quietly dropped.
- **The `focus-appearance` measurements were deliberately NOT promoted to findings.** They are WCAG 2.4.13, Level AAA, and the tool's own summaries say "Informative only." Fifteen sibling files repeat the same measurement for other pages; treating any of them as an AA failure here would be a manufactured violation.
- **No finding was raised from the 27 sibling batch-crawl files.** None of them is about this component.

**A note on the evidence blocks**: the contract requires a `fingerprint`, which is a computed digest. This is a read-only review with no execution, so rather than write a plausible-looking hex string I recorded the derivation recipe and said why. A fabricated digest would look more complete and be worth less than nothing — it would be a stable-looking identifier that does not correspond to anything.

**What would upgrade this to ACCEPT-WITH-RESERVATIONS**: both CRITICALs fixed (option `id`s + `aria-activedescendant`; `aria-labelledby` self-reference on the trigger), plus MAJOR-1/-2/-3 resolved — which the recommended restructure does in one pass — and re-run of the same driven trace showing non-empty `sr_announcement.new_phrases` at the ArrowDown and commit steps, and `active_element_selector: "#dropdown-btn"` rather than `body` after Enter. Same tool, same viewport, same goal, so the before/after is comparable under the verification evidence contract. ACCEPT additionally needs MAJOR-4 through -8 addressed and the CSS supplied so the target-size and contrast questions can be closed with measurement rather than inference.

---

## Open Questions (unscored)

1. **Focus-appearance measurement inconsistency.** `step_0001` and `step_0003` report `focus_appearance.changed_area: 0`, `contrast: null`, and `focus_visible.pixel_cue: false`, while `step_0002` reports `changed_area: 367` on the *same element* (`#dropdown-btn`) one keystroke later. The tool concluded `visible: true` from `style_cue` rather than pixels at those steps. Most likely a capture-timing artifact (screenshot taken before paint), not a real "invisible on first focus" defect. I have **not** raised a 2.4.7 finding on this basis. Worth confirming whether the harness captures before or after paint, because if it captures after, `changed_area: 0` on a Tab-arrival would be a real problem.
2. **Does `<label htmlFor>` beat button subtree content outside Chromium?** The trace measures one engine. The CRITICAL-2 fix is correct under either computation, but the *description* of the mechanism may need adjusting for Firefox/WebKit, and the failure mode inverts (the field label would drop out of the name instead of the value).
3. **What is the actual computed height of a single `<li role="option">`?** MAJOR-8 rests entirely on 54 ÷ 3. One DevTools reading settles it.
4. **Is this component ever rendered more than once per page?** Settles whether MAJOR-7 is MAJOR or ENHANCEMENT.
5. **Is there CSS on `.dropdown-list` or `.selected` involving transitions, or color as the sole cursor indicator?** Determines whether Vestibular stays LOW and whether 1.4.1 is in play.
6. **Was the batch crawler run against `interactive-dropdown-focus-bug.html` at all?** No findings file exists for it. Given that the crawler emitted `findings: []` for several pages with names announcing planted defects, a missing file and an empty file carry roughly the same (near-zero) information — but knowing which one this is tells us whether the detector was silent or absent.
7. **Was `role="combobox"` considered and rejected?** If the team already evaluated the select-only combobox route and chose the two-element structure deliberately, the architectural recommendation above should be re-scoped to the conservative variant, and I would want the reasoning rather than assume it was never considered.
