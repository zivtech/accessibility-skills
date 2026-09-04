# Accessibility Design Review: `BuggyDropdown` (Custom Sort Dropdown)

Target: the `BuggyDropdown` React component (button trigger + popup `role="listbox"`), reviewed against its own stated Expected Behavior and against a keyboard-a11y-tester driven trace captured on a live instance of the component.

## Phase 0 — Evidence Intake

Evidence actually about this component:
- `interactive-dropdown-focus-bug.trace.json` — a driven (live, interactive) keyboard-a11y-tester session against `interactive-dropdown-focus-bug.html`, 6 steps, personas `keyboard` + `screen-reader`. This is hard, measured evidence: DOM selectors, computed AX name/role/state, focus-visible/appearance metrics, and captured SR announcement phrases per step. Treated as hard evidence per the evidence contract, not informal reasoning.
- The fixture's own "Expected Behavior" and "Accessibility Features Present" notes — treated as the author's stated intent/spec, not just my opinion. Two lines are load-bearing: "Escape should close dropdown AND restore focus to button" and "Selection should restore focus to button."

Evidence NOT about this component, excluded from this review:
The pack also bundles keyboard-a11y-tester batch-crawl `findings` JSON for roughly thirty other, unrelated fixture pages — accordion, app-shell focus order, async forms, breadcrumbs, tabs, modal, pagination, popovers, search, video, etc. Each carries its own distinct URL under `http://127.0.0.1:8777/` (e.g. `tabs-incomplete-aria-selected.html`, `popover-no-focus-management.html`, `combobox-autocomplete-no-listbox-role.html`). None of these URLs is `interactive-dropdown-focus-bug.html`, and none of their finding text mentions this component. `interactive-dropdown-clean.json` is a same-family but distinct fixture (the working, bug-free control) with empty findings — it says nothing about the buggy variant under review here. All of these are excluded as out-of-scope; citing them against `BuggyDropdown` would misattribute evidence across unrelated fixtures and would be a fabricated finding. No axe-core or Pa11y run is present in the pack for this component either — this review rests on direct source reading plus the one directly-relevant trace.

No prior audit/trend history for this component is present in the evidence, so all findings below are marked `trend: new`.

## Phase 1 — Pre-commitment Predictions (custom dropdown/select category)

Before weighing the evidence, the standard risk profile for a custom button-triggered listbox predicts:
1. Focus may not restore to the trigger after Escape.
2. Focus may not restore to the trigger after a selection.
3. Arrow-key navigation may update visual/ARIA state without an accompanying AT announcement (missing `aria-activedescendant` or roving tabindex).
4. The trigger's accessible name or the popup's `aria-controls` target may be missing or mismatched.
5. Selected state may be visual-only, not programmatic.

## Phase 2 — Semantic HTML Audit

- Trigger is a native `<button>` (good — not a `div`/`span` with `role="button"`).
- Popup uses native `<ul>`/`<li>` re-roled as `listbox`/`option` — this is the standard, blessed way to build this pattern; ARIA is layered on native list semantics, not masking a bad structure.
- `<label htmlFor="dropdown-btn">{label}</label>` correctly targets the button (a labelable element per the HTML spec). The trace confirms this actually works at runtime: step_0001/step_0002/step_0006 all compute `"name": "Sort by"` via a `labelledby` relationship the browser derived from the `<label for>` association. This is a case where the implementation is correct — no finding filed, credited as sound.
- The decorative `▼` glyph is wrapped in `<span aria-hidden="true">`, correctly preventing "down pointing triangle" from being read into the accessible name. No finding.
- No heading hierarchy or landmark structure is assessable at this component-only scope; not claimed either way.

Verdict for this phase: clean. No MAJOR semantic findings.

## Phase 3 — ARIA Pattern Compliance Audit

Pattern in play: a disclosure-button trigger (`aria-haspopup="listbox"`, `aria-expanded`, `aria-controls`) plus a WAI-ARIA APG **Listbox Pattern** popup (`role="listbox"`, `role="option"`, `aria-selected`).

Present and correct (confirmed by trace, not just source reading):
- `aria-haspopup="listbox"` — present, confirmed in AX state (`hasPopup: "listbox"`).
- `aria-expanded` toggles `false → true` and back, as a real boolean (JSX `aria-expanded={isOpen}`), confirmed in AX state at steps 1/2/6. Not the "yes/no" antipattern.
- `aria-controls="dropdown-list"` correctly resolves to the popup's real `id` — confirmed in AX state (`controls: "dropdown-list"`). Prediction #4 above did **not** pan out; not filed.
- `role="listbox"` / `role="option"` / `aria-selected` are the right roles for this pattern.

Missing (the pattern is incomplete, not just "80%" — the keyboard interaction model is absent):
Per the APG Listbox Pattern, once focus is on the listbox, keyboard navigation must be perceivable to AT either by (a) roving tabindex — DOM focus actually moves to each `<li role="option">` — or (b) `aria-activedescendant` on the `<ul>`, updated to the active option's `id`, while DOM focus stays on the listbox. `BuggyDropdown` implements **neither**: the `<li>` elements have no `tabIndex` and are never focused, and the `<ul>` has no `aria-activedescendant` attribute at all — and the `<li>` elements don't even have an `id` to reference if one were added. This is the root cause of the silent-arrow-key finding in Phase 4/6 below (CRITICAL).

## Phase 4 — Focus Management Review

This is where the fixture's evidence is most direct. Walking the trace step by step:

- **step_0001** (Tab → `#dropdown-btn`): focus lands on the button, `aria-expanded=false`, SR hears "button, Sort by, not expanded, has popup listbox." Correct.
- **step_0002** (Enter → open): `aria-expanded` flips to `true` and `aria-controls` appears in AX state — the toggle logic ran. But `"focus_moved": false` — focus stayed on the button. The fixture's stated Expected Behavior is "Opens on button click, list receives focus," so this is a confirmed regression against the stated spec, not an opinion. Root cause in `BuggyDropdown.jsx:8-13` (`handleToggle`): it reads `!isOpen && listRef.current` and calls `.focus()` in the same synchronous tick as `setIsOpen(!isOpen)`. Because the `<ul ref={listRef}>` (line 52) only renders once `isOpen` is true, `listRef.current` is still `null` at the moment this check runs on the very first open — the ref hasn't attached to anything yet. The focus call is silently skipped.
- **step_0003** (Tab → `#dropdown-list`): the user has to manually Tab a second time to reach the list (it's reachable because of `tabIndex="0"` on the `<ul>`, line 58). SR announces "listbox, orientated vertically" — the container role, but nothing about which option is active.
- **step_0004** (ArrowDown, focus stays on `#dropdown-list`): `focus_moved: false` (expected, since the design intends to keep focus on the container) but `sr_announcement` is completely empty — `new_phrases: []`, `focus_announcement: null`. `selectedIndex` and `aria-selected` did change internally (`BuggyDropdown.jsx:65`), but nothing routes that change to the accessibility tree the way a screen reader can hear it. This directly confirms the Phase 3 gap.
- **step_0005** (Enter → select, on `#dropdown-list`): `active_element_selector` becomes `"body"`, `tag: "body"`, `role: "none"`, `is_body: true`, and `sr_announcement` is again fully empty. This is the named bug: selecting an option calls `handleSelect` (`BuggyDropdown.jsx:15-19`), which calls `setIsOpen(false)` and nothing else — no `.focus()` call anywhere in that path. The `<ul>` that currently holds DOM focus unmounts, and because no replacement focus target is assigned, the browser's default is to drop focus to `<body>`. The fixture's own Expected Behavior states "Selection should restore focus to button" — this is a direct, measured contradiction of stated intent, not a stylistic complaint.
- **step_0006** (Shift+Tab from body → `#dropdown-btn`): the user manually recovers by tabbing backward. This is the user doing cleanup the component should have done itself.

The `handleKeyDown` Escape branch (`BuggyDropdown.jsx:22-24`) is structurally identical to the broken select path — `setIsOpen(false)` with no `.focus()` call anywhere in that branch or afterward. There is no other listener, effect, or blur handler anywhere in the 78-line source that could plausibly intervene. I have **not** directly measured an Escape keypress in the trace (no step exercises it), so I flag this finding as code-verified rather than trace-measured, but the mechanism is identical to the one directly observed at step_0005 (unmount a focused node with no reassignment → focus falls to `body`), so I am not discounting the severity — only the evidence tier.

Tab order otherwise: logical (label → button → list once reached), no positive tabindex misuse, no keyboard trap.

Focus-indicator visibility (2.4.7, AA): an outline is present and `focus_visible.visible: true` at every captured step — this AA-level bar is met.

Focus appearance (2.4.13, AAA — informative only): `area_pass` is `false` at steps 1/2/3/6 and `contrast_pass` is `false` at steps 2 (2.98) and 6 (2.53); only step_0004 (the `<ul>` itself, a much larger element) clears both bars (contrast 5.67, `aaa_pass: true`). This is the one SC in this protocol's citation list that is genuinely AAA-tier by design (not an instance of the known upstream `conformance_level` mislabeling issue, which affects other checks, not this one) — so this is reported as informative, not as an AA blocker, consistent with the project's stated WCAG 2.2 AA target.

## Phase 5 — State Communication Audit

- `aria-expanded`: communicated correctly, confirmed announced at steps 1/2/6. No finding.
- Selected option state: `aria-selected` is kept in sync programmatically (`BuggyDropdown.jsx:65`) — this is **not** a "visual-only indicator" problem (the CSS `.selected` class and `aria-selected` change together, in sync). The actual defect is more specific than "visual only": the state change is programmatic but unreachable by AT because nothing directs assistive-technology attention to it (no focus move, no `aria-activedescendant`). Folded into the Phase 3/4/6 finding rather than double-counted.
- No loading, error, disabled, or readonly states exist in this component — not applicable.
- No confirmation (`aria-live`/status) that a selection was applied beyond the button's own text re-rendering — and that re-render is only perceivable if focus is anywhere near the button, which — per Phase 4 — it isn't, right after a selection.

## Phase 6 — Multi-Perspective Review

**Screen reader user:** The trigger's name/role/state are announced correctly on entry and toggle. Entering the listbox announces only the container ("listbox, orientated vertically") — no active-option name. Arrow-key browsing is completely silent (step_0004) — there is no way to preview which option is current before committing. Committing a selection (Enter) throws focus to `document`/body with zero announcement of what happened or what was chosen. This is a full breakdown of the widget's core task for this persona.

**Keyboard-only (sighted) user:** Tab order is logical. The first-open focus miss costs one extra Tab press — recoverable, and `aria-expanded` still correctly reflects the open state in the meantime. Arrow-key navigation is *visually* legible (the `.selected` CSS class presumably renders a highlight), so this persona is not blocked the way the screen-reader persona is — a clean example of one failure mode hitting one access method and not another. After selecting, this user is dropped to `document.body` with no visible focus ring anywhere on the page — disorienting, though a sighted user can usually reorient by looking at the page and clicking/tabbing again.

**Low vision (zoom / high contrast):** The focus outline exists and is visible at every step (2.4.7 met); several steps fall short of the stricter AAA 2.4.13 contrast/area bar (measured 2.53–2.98 against a 3:1 target). No data exists in either the source or the trace on 200% reflow, touch-target sizing, or body-text contrast — not claimed either way.

**Cognitive accessibility:** The sudden, silent loss of focus to `document.body` after a selection or (predicted) Escape is a disorientation problem independent of assistive technology — any user can lose their place with no "you are here" signal. No timeouts, destructive actions, or multi-step flows exist in this component; most cognitive-specific checks don't apply at this scope.

**Vestibular & motion:** No animation/transition/auto-play in source or trace — not applicable.

**Auditory access:** No media elements — not applicable.

**Environmental contrast:** Only focus-ring contrast is measured (AAA-tier, informative); no body-text/background contrast data is available — not claimed.

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|-----------------|
| Screen reader | HIGH | Silent arrow-key navigation; focus (and all announcement) lost on selection and (predicted) on Escape |
| Keyboard-only | HIGH | Focus dropped to `document.body` after selection/Escape; first-open focus miss |
| Low vision | MEDIUM | Focus indicator present and AA-compliant, but AAA area/contrast shortfalls measured; no visible indicator at all once focus is on `body` |
| Cognitive | MEDIUM | Sudden, silent context loss affects orientation regardless of AT use |
| Vestibular & motion | LOW | No motion in scope |
| Auditory access | LOW | No media in scope |
| Environmental contrast | LOW–MEDIUM | Only AAA-tier focus-ring contrast measured; no body-text contrast data available |

Screen reader and keyboard-only both land at HIGH — this fixture would warrant escalation to a deep perspective audit under the standard escalation rule.

## Phase 7 — Gap Analysis (What's Missing)

- Missing focus restoration to the trigger on the Escape path (code-level).
- Missing focus restoration to the trigger on the selection path (measured).
- Missing `aria-activedescendant` (or roving tabindex) pairing the listbox's arrow-key navigation to an AT-perceivable announcement.
- Missing unique `id` attributes on the `<li role="option">` elements — a prerequisite for the `aria-activedescendant` fix.
- Missing an effect-driven (rather than same-tick-ref-read) focus-on-open, which is why the very first open silently no-ops.
- Missing any AT-facing confirmation that a selection was applied, beyond the button's own accessible name changing (which is moot while focus is elsewhere).

## Phase 8 — Realist Check (Severity Calibration)

- **Focus-to-body on selection** (measured): worst case is a completed task with zero confirmation for a screen-reader user, and several blind Tab presses to reorient for anyone else. Not caught by axe-core/Pa11y (runtime focus behavior, not a static DOM rule) — exactly the class of defect this review exists to catch before a user files it. No downgrade — kept CRITICAL.
- **Escape-path focus loss** (code-inferred): identical mechanism, identical impact reasoning. Kept CRITICAL, but confidence is explicitly flagged as code-verified rather than independently trace-measured (see Phase 9).
- **First-open focus miss** (measured): worst case is one extra Tab press; `aria-expanded` still correctly announces the open state in the meantime, so the user isn't stranded, only inconvenienced. **Downgraded CRITICAL → MAJOR.** Mitigated by: the listbox is still reachable by a single subsequent Tab, and the open-state change is still announced through the button.
- **Silent arrow-key navigation** (measured): worst case is a screen-reader user unable to preview or confirm any option before committing to Enter, and then also hitting the focus-to-body bug with no way to learn what was chosen. Not caught by static tools. No downgrade — kept CRITICAL.
- **AAA focus-appearance shortfall** (measured): 2.4.7 (AA, indicator visible) is met in every step; only the numeric AAA bar is missed in some states. Reported as ENHANCEMENT/informative, not inflated to a blocking AA violation.

## Phase 9 — Self-Audit

| Finding | Confidence | Developer could refute? | Gap or preference? |
|---|---|---|---|
| Focus lost to body on selection | HIGH (directly measured, step_0005) | No — trace is unambiguous | GAP |
| Escape-path focus loss | HIGH (code-verified; not independently trace-measured) | Unlikely — no other listener/effect in the 78-line source could intervene | GAP |
| First-open focus miss | HIGH (measured step_0002 + code mechanism agree) | No | GAP |
| Silent arrow-key navigation | HIGH (measured step_0004, zero phrases) | No | GAP |
| AAA focus-appearance shortfall | HIGH data / correctly downgraded severity | N/A | GAP, but ENHANCEMENT-tier by Realist Check, not inflated |

Explicitly **not** filed, on purpose: the `<label for="dropdown-btn">`-on-a-button pattern. It is unusual to see a `<label>` target a `<button>` rather than a form input, and it would be easy to flag reflexively — but the trace directly proves the accessible name computes correctly ("Sort by" via `labelledby` at every relevant step), and manufacturing a finding against direct contrary evidence would violate the calibration this protocol demands. No LOW-confidence findings needed to move to Open Questions beyond what is already listed there below.

## Phase 10 — Synthesis (Predictions vs. Actual)

- Prediction 1 (focus fails to restore after Escape) — confirmed, code-level.
- Prediction 2 (focus fails to restore after selection) — confirmed, and measured directly (stronger than predicted).
- Prediction 3 (arrow-key navigation lacks an AT-perceivable announcement) — confirmed, and worse than "incomplete": it is completely silent.
- Prediction 4 (`aria-controls` target missing/mismatched) — **not** confirmed; correctly wired and verified working. Not filed.
- Prediction 5 (selected state visual-only) — partially right for the wrong reason: the state *is* programmatic (`aria-selected` syncs correctly); the actual defect is that nothing routes AT attention to the change, not that the change itself is missing.
- Unpredicted discovery: the React ref-timing bug causing the first-open focus miss — a component-specific finding that a generic "custom dropdown" checklist wouldn't necessarily anticipate, found only by tracing the actual synchronous execution order against the trace.

---

**VERDICT: REVISE**

**Overall Assessment**: The ARIA vocabulary and semantic scaffolding are sound — native `<button>`, correct `aria-haspopup`/`aria-expanded`/`aria-controls` wiring (all verified working in the trace), a correctly hidden decorative glyph, and a properly associated `<label>`. But the focus-management layer beneath that scaffolding has three CRITICAL, evidence-backed gaps concentrated on the widget's core interaction lifecycle — opening, browsing, and closing/selecting — that make it unusable or silent for screen-reader users and disorienting for keyboard-only users, contradicting the component's own stated Expected Behavior.

**Pre-commitment Predictions**: Predicted focus-restoration failures on Escape/selection and an incomplete AT-perceivable arrow-key model; both confirmed, the latter more severely than predicted (total silence, not partial coverage). Predicted an `aria-controls` mismatch that did not materialize. Additionally found a React ref-timing bug on first-open not anticipated by the generic prediction set.

**Critical Findings** (blocks access):

1. **Focus is lost to `document.body` after selecting an option**, with zero screen-reader announcement of the selection. See `BuggyDropdown.jsx:15-19` (`handleSelect`), which calls `setIsOpen(false)` and nothing else, unmounting the currently-focused `<ul>` (`BuggyDropdown.jsx:52-72`) without reassigning focus anywhere. Measured at trace step_0005: `active_element_selector: "body"`, `role: "none"`, `sr_announcement.new_phrases: []`. Screen reader and keyboard-only users impacted. Per WCAG 2.4.3 (Focus Order) and the WAI-ARIA APG Listbox Pattern, closing an owned popup must return focus to a sensible location — here, the trigger. This directly contradicts the fixture's own stated behavior: "Selection should restore focus to button."
   - Confidence: HIGH
   - Why this matters: A screen-reader user completes the sort-selection task and receives no confirmation of what happened and no sense of where they now are on the page; recovery requires blind Tab/Shift+Tab presses.
   - Fix: Capture a ref on the button (`const buttonRef = useRef(null)`, `ref={buttonRef}` on the `<button>`) and call `buttonRef.current?.focus()` in `handleSelect` right after `setIsOpen(false)`.

   ### A11y Evidence Finding
   ```
   finding_id: dropdown-select-focus-lost-to-body
   fingerprint: not computed — no hashing tool available in this review pass; derive from step_0005 + the #dropdown-btn/body selector pair if a stable fingerprint is required downstream
   source: evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json (step_0005)
   wcag_or_apg: WCAG 2.4.3 Focus Order; WAI-ARIA APG Listbox Pattern (focus management on selection)
   section_508_fpc_context: not in scope (component-level design review, not a declared Section 508 audit)
   severity: CRITICAL
   perspective_alarms: screen_reader=HIGH, keyboard=HIGH, low_vision=MEDIUM, cognitive=MEDIUM
   evidence: step_0005, keystroke_sent="Enter" → active_element_selector="body", tag="body", role="none", is_body=true, sr_announcement.new_phrases=[], focus_announcement=null. Root cause: BuggyDropdown.jsx:15-19 (handleSelect) + no ref/focus call anywhere in the selection path.
   reproduction_steps: Tab to #dropdown-btn -> Enter to open -> Tab into the listbox -> ArrowDown to an option -> Enter to select -> observe focus.
   expected_behavior: Focus returns to #dropdown-btn (per the fixture's stated "Selection should restore focus to button").
   actual_behavior: Focus lands on document.body with no accessible name/role and no announcement.
   trend: new
   ```

2. **Escape closes the dropdown without restoring focus to the trigger** (predicted to fail identically to Finding 1). See `BuggyDropdown.jsx:22-24`, the Escape branch of `handleKeyDown`, which calls `setIsOpen(false)` and nothing else — structurally identical to the confirmed-broken selection path, and there is no other listener or effect anywhere in the source that could intervene. Not independently exercised in the supplied trace (no Escape step exists), so this is code-verified rather than directly measured — flagged accordingly, not discounted in severity, since the failure mechanism (unmount a focused node, no reassignment, focus falls to `body`) is the same one directly observed at step_0005.
   - Confidence: HIGH (code-verified mechanism; not independently trace-measured for this exact key)
   - Why this matters: Escape is the conventional "back out safely" key for popups; a user who backs out expecting to land back on the trigger instead loses their place entirely, again with no announcement. Directly contradicts the fixture's stated "Escape should close dropdown AND restore focus to button."
   - Fix: In the Escape branch, after `setIsOpen(false)`, call the same `buttonRef.current?.focus()` used in Finding 1's fix.

3. **Arrow-key navigation inside the open listbox produces zero screen-reader announcement.** `selectedIndex` and `aria-selected` update correctly in the DOM (`BuggyDropdown.jsx:65`), but the `<ul>` (`BuggyDropdown.jsx:53-59`) has no `aria-activedescendant`, and the `<li>` options (`BuggyDropdown.jsx:62-68`) have neither an `id` to be referenced nor individual tabindex for a roving-tabindex alternative — the WAI-ARIA APG Listbox Pattern's keyboard-interaction requirement is met by neither mechanism. Measured at trace step_0004 (ArrowDown): `focus_moved: false`, `sr_announcement: {new_phrases: [], focus_announcement: null}`. Also visible at step_0003: entering the listbox announces only "listbox, orientated vertically," never the initially-active option.
   - Confidence: HIGH
   - Why this matters: A screen-reader user has no way to preview which option arrow keys have landed on before committing with Enter — the core "browse options" interaction is inaudible. Not detectable by axe-core/Pa11y (a runtime behavior, not a static rule violation).
   - Fix: Add stable `id`s to each option (`id={`option-${index}`}`) and set `aria-activedescendant={`option-${selectedIndex}`}` on the `<ul>`, updated on every arrow-key press. Verify in the rendered DOM (not just via unit assertions) that the id reference actually resolves.

   ### A11y Evidence Finding
   ```
   finding_id: dropdown-arrow-nav-silent-to-sr
   fingerprint: not computed — no hashing tool available in this review pass
   source: evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json (step_0003, step_0004)
   wcag_or_apg: WCAG 4.1.2 Name, Role, Value; WAI-ARIA APG Listbox Pattern (aria-activedescendant / roving tabindex)
   section_508_fpc_context: not in scope
   severity: CRITICAL
   perspective_alarms: screen_reader=HIGH, keyboard=LOW, low_vision=LOW, cognitive=MEDIUM
   evidence: step_0003 focus enters #dropdown-list with sr_announcement="listbox, orientated vertically" (no option identified); step_0004 ArrowDown changes aria-selected internally (BuggyDropdown.jsx:65) but focus_moved=false and sr_announcement.new_phrases=[]/focus_announcement=null.
   reproduction_steps: Open the dropdown -> Tab into the listbox -> press ArrowDown -> listen for screen reader output.
   expected_behavior: Each ArrowDown/ArrowUp announces the newly active option's name and selected state.
   actual_behavior: Complete silence; no phrase is produced.
   trend: new
   ```

**Major Findings** (significantly degrades experience):

1. **The dropdown's first open does not move focus into the listbox**, contradicting the fixture's stated "Opens on button click, list receives focus." See `BuggyDropdown.jsx:8-13` (`handleToggle`): it checks `!isOpen && listRef.current` and calls `.focus()` synchronously in the same tick as `setIsOpen(!isOpen)`, but the `<ul ref={listRef}>` (line 52) has not mounted yet at that point on the first open, so `listRef.current` is still `null` and the call is silently skipped. Measured at trace step_0002: `aria-expanded` correctly flips to `true`, but `focus_moved: false`. The user recovers by pressing an additional Tab (step_0003, confirmed working).
   - Confidence: HIGH
   - Why this matters: The intended interaction (open → land in the list) silently fails on the very first use; recoverable, but not what was designed or documented.
   - Fix: Move the focus call into a `useEffect` keyed on `isOpen`, so it runs after the list has actually mounted: `useEffect(() => { if (isOpen && listRef.current) listRef.current.focus(); }, [isOpen]);`. This removes the dependency on same-tick ref timing entirely.

   ### A11y Evidence Finding
   ```
   finding_id: dropdown-first-open-focus-miss
   fingerprint: not computed — no hashing tool available in this review pass
   source: evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json (step_0002)
   wcag_or_apg: WCAG 2.4.3 Focus Order; component's own stated Expected Behavior ("list receives focus")
   section_508_fpc_context: not in scope
   severity: MAJOR (recalibrated from a candidate CRITICAL — see Realist Check)
   perspective_alarms: screen_reader=MEDIUM, keyboard=MEDIUM, low_vision=LOW, cognitive=LOW
   evidence: step_0002, keystroke_sent="Enter" on #dropdown-btn -> states.expanded=true but focus_moved=false; focus remains on the button. Root cause: BuggyDropdown.jsx:8-13 reads listRef.current synchronously before the <ul> (line 52) has mounted.
   reproduction_steps: Tab to #dropdown-btn -> press Enter -> observe active element.
   expected_behavior: Focus moves to #dropdown-list immediately on open.
   actual_behavior: Focus remains on #dropdown-btn; an additional Tab (confirmed working at step_0003) is needed to reach the list.
   trend: new
   ```

**Minor Findings** (friction but workaround exists):
- On first entering the listbox, the screen reader announces only the container role ("listbox, orientated vertically") without identifying the initially-active option (step_0003). This is a secondary symptom of the same missing-`aria-activedescendant` root cause as Critical Finding 3, and should resolve once that fix lands — not scored as a separate defect to avoid double-counting.

**Enhancements** (best practice not met):
- Several focus states fall short of the WCAG 2.4.13 (AAA) Focus Appearance area/contrast bar (measured contrast 2.53–2.98 against a 3:1 target at steps 2 and 6) while still meeting the AA-level 2.4.7 Focus Visible requirement. Informative only against the project's stated WCAG 2.2 AA target.
- Consider whether `role="combobox"` (WAI-ARIA APG Select-Only Combobox pattern) would better match user/AT expectations for a single-value picker whose visible button text mirrors the current selection, versus the current simplified disclosure-button-plus-listbox hybrid. Not required — the current pattern is a legitimate, documented alternative — but worth a design conversation.
- Once Critical Finding 1 is fixed and focus correctly returns to the button, consider whether that alone provides sufficient confirmation of a completed selection, or whether a dedicated `aria-live="polite"` status region (WCAG 4.1.3) would give a clearer "X selected" confirmation independent of focus position.

**What's Missing** (gaps, unhandled edge cases, unstated assumptions):
- Focus restoration to the trigger on the Escape path and on the selection path (Critical Findings 1–2).
- `aria-activedescendant` (or roving tabindex) pairing arrow-key navigation to an AT-perceivable announcement, and the `id` attributes on each option that a fix would require (Critical Finding 3).
- An effect-driven (rather than same-tick ref-read) open-focus mechanism (Major Finding 1).
- Any AT-facing confirmation that a selection was applied, independent of the button's own accessible name changing.

**Multi-Perspective Notes**:
- Screen reader user: Trigger name/role/state announce correctly. Entering the listbox and browsing it with arrow keys is silent — no option identification, no announcement of change. Committing a selection drops focus to `document`/body with no announcement of what was chosen. The core task is effectively inaudible.
- Keyboard-only user: Tab order is logical; the first-open miss costs one recoverable extra Tab. Arrow-key browsing is visually legible via the `.selected` CSS class, so this persona is not blocked the way the screen-reader persona is. Selecting an option drops focus to `body` with no visible indicator anywhere — disorienting but recoverable by tabbing again.
- Low vision user (200% zoom, high contrast): The focus outline is present and visible at every measured step (2.4.7 met); several states miss the stricter AAA 2.4.13 numeric bar. No data available on reflow, touch-target sizing, or content contrast — not claimed.
- Cognitive accessibility: The abrupt, silent loss of focus to `document.body` is a general orientation problem, not an AT-specific one. No timeouts, destructive actions, or multi-step flows apply at this scope.

**Verdict Justification**: REVISE, not REJECT or ACCEPT-WITH-RESERVATIONS. The semantic scaffolding — native elements, correct ARIA role/property vocabulary for the disclosure trigger, correct label association, correctly hidden decorative glyph — is sound and should be preserved; this is not a "wrong pattern from scratch" situation. But three CRITICAL findings, each backed by direct trace measurement or an identical code-verified mechanism, break the widget's core open/browse/select/close lifecycle for screen-reader users and meaningfully disorient keyboard-only users, directly contradicting the component's own documented Expected Behavior. Each has a concrete, scoped fix (a captured button ref reused on both exit paths; an `aria-activedescendant`/option-`id` pairing; moving the open-focus call into an effect). Upgrade path to ACCEPT: implement the three fixes, then re-run the driven trace and confirm (a) both Escape and Enter-to-select end with focus on `#dropdown-btn`, not `body`; (b) arrow-key presses produce a non-empty `sr_announcement` naming the active option; (c) the first Enter-to-open produces `focus_moved: true` onto the listbox. Any `aria-*` reference added as part of these fixes should be checked in the actual rendered DOM, not only via unit-test assertions, to confirm the id association resolves.

**Open Questions (unscored)**:
- The mouse-click-to-close path (clicking the trigger while open) was not exercised in the trace. Focus likely stays on the button as an incidental side effect of the click itself, independent of any code-level refocus logic — worth explicit testing to confirm it isn't coincidentally masking the same missing-refocus gap.
- Whether the intended design is a full `role="combobox"` (APG Select-Only Combobox) rather than the current disclosure-button-plus-listbox hybrid is a design-intent question, not a defect — noted above as an enhancement-level discussion point, not scored.
- 200% zoom/reflow, touch-target sizing, and body-text color contrast are not covered by either the source or the supplied trace. Explicitly out of evidence scope for this review — not assumed clean.
