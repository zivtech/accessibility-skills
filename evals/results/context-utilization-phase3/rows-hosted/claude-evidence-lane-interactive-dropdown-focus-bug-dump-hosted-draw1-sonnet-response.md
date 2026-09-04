**VERDICT: REVISE**

**Overall Assessment**: `BuggyDropdown` chooses a legitimate, recognized pattern — native `<button>` + `aria-haspopup="listbox"`/`aria-expanded`/`aria-controls`, popped open onto a `<ul role="listbox">` of `<li role="option">` children — and gets the surface markup largely right (valid ARIA value types, a correctly `aria-hidden`-wrapped glyph, a resolvable `aria-controls` reference). But the driven keyboard-a11y-tester trace in the evidence pack proves the pattern is roughly 60% wired, not complete: arrow-key browsing inside the open listbox produces **zero** screen-reader feedback, focus is dropped to `<body>` when an option is selected, and — a defect the trace exposes but a static read of the JSX would likely miss — the "focus the list on open" logic never actually fires because of a stale-ref timing bug, directly contradicting the fixture's own stated expected behavior ("Opens on button click, list receives focus"). None of this is visible from the ARIA attributes alone; it only surfaces once the interaction is actually driven, which is exactly the class of gap this review exists to catch.

**Evidence Consumed (Phase 0)**: The pack contains one directly relevant artifact and roughly thirty that are not.
- **In scope**: `evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json` — a `driven-live` session against `interactive-dropdown-focus-bug.html` with the explicit goal "open the sort dropdown, move into the listbox, pick an option, verify focus returns to trigger." Per Phase 0 guidance, this is treated as hard/measured evidence, one tier above design reasoning, and every CRITICAL/MAJOR finding below cites a specific `step_id` from it.
- **Out of scope**: the ~30 `keyboard-a11y-tester/findings/*.json` batch-crawl files (`accordion-no-region-role`, `app-focus-order-illogical`, `async-form-vague-success`, `breadcrumb-navigation-no-nav-landmark`, `button-skip-link-clean`, `combobox-autocomplete-no-listbox-role`, `dashboard-heading-inconsistency`, `form-field-vs-summary-errors`, `form-validation-missing-aria-describedby`, `heading-hierarchy-skipped`, `image-carousel-no-region`, `multistep-form-error-clearing`, `pagination-no-nav-landmark`, `popover-no-focus-management`, `search-focus-stays-in-input`, `search-results-dynamic-clean`, `tabs-incomplete-aria-selected`, `tooltip-no-role-no-association`, `video-player-missing-captions`, plus several empty-findings files) all carry `url` values pointing at *other* pages in the same benchmark corpus (e.g. `http://127.0.0.1:8777/accordion-no-region-role.html`), never `interactive-dropdown-focus-bug.html`. None of them are evidence about this component, including `interactive-dropdown-clean.json` — a same-family "clean" dropdown variant with zero findings — which is a sibling reference implementation, not this component. Citing any of these against `BuggyDropdown` would be evidence misattribution, so they are excluded from every finding below. This scoping check matters more than usual here: the dump is roughly 30:1 irrelevant-to-relevant by document count, and the one relevant document is buried in the middle of it.
- The recurring `focus-appearance-weak-*` finding shape that appears on nearly every sibling page (AAA-tier, `conformance_level: "AAA"`, confidence 0.5, "informative only") is a page-template-level pattern across the corpus, not something specific to this component — noted for calibration, not cited as a `BuggyDropdown` finding.

**Pre-commitment Predictions**: Before reading the trace in detail, the expected failure modes for a "custom dropdown/select" per the protocol's own component-type list were: (1) focus not restored after Escape/selection, (2) arrow-key navigation incomplete or unsynchronized with AT, (3) selected state communicated visually but not programmatically, (4) the options container missing an accessible name. All four were confirmed — but the trace showed each one to be **more severe** than the generic prediction implied: "incomplete" arrow-key navigation turned out to be *totally silent* (not degraded, absent), and "selected state visual-only" turned out to be *undiscoverable through any path* once combined with the listbox's missing activedescendant wiring, not merely inconvenient. One failure was **not** predicted: a stale-ref timing bug that silently disables the open-transition's auto-focus-into-list, which only became visible by simulating the code's execution order against the trace's `focus_moved: false` result at the open step — a static ARIA-attribute read would not have caught it, since the intent-bearing code (`listRef.current.focus()`) is present in the source and looks correct at a glance.

**Critical Findings** (blocks access):

1. **Open listbox never communicates the active/selected option to assistive technology.** `BuggyDropdown.jsx:53-71` — the `<ul role="listbox">` (line 56) receives DOM focus directly (`tabIndex="0"`, line 58) and stays there while arrow keys move `selectedIndex` through React state (`handleKeyDown`, lines 25-32); no option ever receives DOM focus itself, and there is no `aria-activedescendant` on the `<ul>` pointing at the active `<li>`. This is also structurally impossible to add without a further change: the `<li>` elements (lines 62-71) have no stable `id` — only a React-internal `key={index}` (line 63), which is not a DOM attribute an ARIA reference could point to.
   - Confidence: HIGH
   - Why this matters: A screen reader user tabs into the open listbox and hears only "listbox, oriented vertically" (measured, see evidence block). Pressing ArrowDown moves the visual highlight and the underlying `aria-selected` value, but produces **no announcement whatsoever**. The user has no way to tell that anything happened, which option is now active, or how many options exist. This is not degraded feedback — it is a complete communication blackout during the one interaction (browsing options) that is the entire purpose of opening the widget.
   - Fix: Add stable `id`s to each `<li>` (e.g. `id={`dropdown-option-${index}`}`), add `aria-activedescendant={`dropdown-option-${selectedIndex}`}` to the `<ul>`, updated on every arrow-key press. Per the WAI-ARIA APG Listbox pattern, a listbox that keeps DOM focus on the container (rather than moving focus to each option) must expose the active option via `aria-activedescendant`; this implementation has the container-focus half of that pattern without the half that makes it accessible.

   ```
   ### A11y Evidence Finding
   finding_id: dropdown-activedescendant-missing
   fingerprint: a1c3e7f209b4d581
   source: evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json (step_0004)
   wcag_or_apg: WCAG 4.1.2 Name, Role, Value; WAI-ARIA APG Listbox pattern (active-option communication)
   section_508_fpc_context: not in scope (component-level design review, no federal profile declared)
   severity: CRITICAL
   perspective_alarms: screen_reader=HIGH, keyboard=LOW, low_vision=LOW, cognitive=LOW
   evidence: step_0004 — keystroke_sent="ArrowDown", active_element_selector="#dropdown-list" (focus_moved:false), ax_name_role_state.name="" role="listbox", sr_announcement.new_phrases=[], sr_announcement.focus_announcement=null
   reproduction_steps: Tab to the trigger button, press Enter to open, Tab into the listbox, press ArrowDown
   expected_behavior: Screen reader announces the newly active option (name, position, and/or selected state) as arrow keys move through the list
   actual_behavior: No new phrase and no live announcement are produced; the listbox's own accessible name is also empty ("")
   trend: new
   ```

2. **Focus is not restored to the trigger button when the popup closes.** Measured for the selection path, structurally identical (and unrestored) for the Escape path.
   - Selection path (`handleSelect`, `BuggyDropdown.jsx:15-19`): calls `setIsOpen(false)` (line 18), which unmounts the `<ul>` (line 52's `{isOpen && (...)}` guard becomes false) while that `<ul>` still holds DOM focus. Nothing calls `.focus()` on the button or anywhere else afterward. Confidence: HIGH — directly measured (see evidence block).
   - Escape path (`handleKeyDown`, `BuggyDropdown.jsx:22-24`): identical code shape — `setIsOpen(false)` with no accompanying focus call. Confidence: MEDIUM-HIGH — the trace's driven goal did not independently exercise the Escape keystroke, so this half of the finding is source-verified rather than trace-measured; it is flagged at a lower evidence tier than the selection-path half for that reason, not because the code differs.
   - Why this matters: When the `<ul>` unmounts while focused, the browser's default behavior is to drop focus to `<body>`. The trace shows exactly that: `active_element_selector: "body"`, `role: "none"` (step_0005). For every user relying on keyboard focus tracking — not just AT users — this is total loss of place in the page. This exact shape ("focus doesn't restore") is the canonical CRITICAL example in this protocol's own severity scale, applied here to a listbox instead of a modal.
   - Reading trap worth naming explicitly: the trace's very next step (step_0006, Shift+Tab) lands back on `#dropdown-btn`, which could be misread as "it recovers fine." It does not — this fixture's test page has no other focusable element, so Shift+Tab-from-body happens to hit the last focusable element in the whole document, which is coincidentally the button. On a real page with header nav, sidebar links, or any other control near this widget, the same code would drop focus to whatever happens to be first/last in that page's tab order — not back to the trigger. The Realist Check argues for keeping this at full CRITICAL severity rather than downgrading it, precisely because the isolated test page's coincidental recovery makes the bug easy to miss on casual inspection.
   - Fix: Store a ref to the trigger button; call `triggerRef.current?.focus()` in both the Escape branch and at the end of `handleSelect`, deferred with `setTimeout(...,0)` if needed to survive the unmount/re-render.

   ```
   ### A11y Evidence Finding
   finding_id: dropdown-focus-not-restored-on-close
   fingerprint: 5e2b8f14d3a97c60
   source: evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json (step_0005; step_0002 code path cross-checked at BuggyDropdown.jsx:22-24)
   wcag_or_apg: WCAG 2.4.3 Focus Order; consequential WCAG 2.4.7 Focus Visible (nothing is visibly focused once focus lands on body); WAI-ARIA APG Listbox/Menu Button pattern (focus returns to trigger on dismiss)
   section_508_fpc_context: not in scope (component-level design review, no federal profile declared)
   severity: CRITICAL
   perspective_alarms: screen_reader=HIGH, keyboard=HIGH, low_vision=MEDIUM, cognitive=MEDIUM
   evidence: step_0005 — keystroke_sent="Enter", active_element_selector="body", tag="body", is_body=true, ax_name_role_state.role="none", bounding_box=null, computed_focus_style=null
   reproduction_steps: Tab to trigger, Enter to open, Tab into listbox, ArrowDown, Enter to select an option
   expected_behavior: Per the fixture's own stated spec ("Selection should restore focus to button"), focus returns to #dropdown-btn
   actual_behavior: Focus moves to <body>; no element on the page is focused
   trend: new
   ```

**Major Findings** (significantly degrades experience):

1. **Auto-focus-into-list on open never executes — a stale-ref timing bug, not a missing feature.** `BuggyDropdown.jsx:8-13` (`handleToggle`): the intent to move focus into the list on open is present (`if (!isOpen && listRef.current) { listRef.current.focus(); }`, lines 10-12), but at the moment this line runs, `isOpen` still holds the pre-click value (`false`) from this render's closure, and `listRef.current` is still `null` because the `<ul>` (line 52's `{isOpen && ...}` block) has not yet been rendered — React commits the state update and mounts the list *after* `handleToggle` returns, not during it. The condition therefore evaluates `(true && null)`, short-circuits, and `.focus()` never fires on the open transition.
   - Confidence: HIGH
   - Why this matters: The fixture's own "Expected Behavior" section states "Opens on button click, list receives focus," and the code visibly tries to do this — but it is dead code on every real invocation. The trace confirms it directly: step_0002 (Enter, opening the menu) shows `focus_moved: false`, with focus remaining on `#dropdown-btn`; only a separate, subsequent Tab (step_0003) reaches the listbox. This degrades the experience (an undocumented extra keystroke is required) but does not fully block access, since Tab remains available immediately — hence MAJOR rather than CRITICAL.
   - Fix: Move the focus call into a `useEffect` keyed on `isOpen` (`useEffect(() => { if (isOpen) listRef.current?.focus(); }, [isOpen])`), so it runs after React has committed the render that mounts the `<ul>` and populated the ref.

   ```
   ### A11y Evidence Finding
   finding_id: dropdown-openfocus-stale-ref
   fingerprint: 9f4d21b87ace05f3
   source: evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json (step_0002); code inspection at BuggyDropdown.jsx:8-13
   wcag_or_apg: WCAG 2.4.3 Focus Order; WAI-ARIA APG Listbox pattern (opening moves focus into the popup)
   section_508_fpc_context: not in scope
   severity: MAJOR
   perspective_alarms: screen_reader=MEDIUM, keyboard=MEDIUM, low_vision=LOW, cognitive=LOW
   evidence: step_0002 — keystroke_sent="Enter", active_element_selector remains "#dropdown-btn", focus_moved=false, states.expanded=true
   reproduction_steps: Tab to trigger button, press Enter
   expected_behavior: Per fixture spec, "list receives focus" immediately on open
   actual_behavior: Focus remains on the trigger button; a separate Tab keystroke (step_0003) is required to reach the list
   trend: new
   ```

2. **Trigger button's accessible name never reflects the currently selected option.** `BuggyDropdown.jsx:41,42-51`: `<label htmlFor="dropdown-btn">{label}</label>` (line 41) associates the label text ("Sort by" per the trace) with the button, but the button's *own* visible content — `{options[selectedIndex]}` (line 49), the actual current value — is not part of the computed accessible name. This is measured, not inferred: the trace's `ax_name_role_state.name` is `"Sort by"` identically at step_0001 (before any interaction), step_0002 (menu just opened, still showing "Newest"), and step_0006 (after a selection changed the visible text to "Price: low to high"). The name never changes.
   - Confidence: HIGH
   - Why this matters: A native `<select>` announces both its label and its current value (e.g., "Sort by, combobox, Newest"). This widget announces only the static label, at every point in its lifecycle, including immediately after a selection was just made. Combined with Critical Finding 1 (the open listbox also never exposes which option is active), there is no path — closed-button state or open-listbox state — through which a screen reader user can learn the current sort order. Rated MAJOR rather than escalated further because the failure is about discoverability of state, not about the ability to operate the control (the button remains operable and correctly announces `expanded`/`hasPopup`), but the compounding with Finding 1 is worth flagging explicitly since either gap alone would be a smaller, discrete state-communication issue.
   - Fix: Include the current value in the accessible name, e.g. `aria-label={`${label}: ${options[selectedIndex]}`}` on the button (and drop the `<label htmlFor>` association, or keep it only if it is not the sole source of the accessible name), so the announcement becomes something like "Sort by: Newest, button, has popup listbox."

   ```
   ### A11y Evidence Finding
   finding_id: dropdown-button-name-omits-value
   fingerprint: 3c7a90e1f5b8d246
   source: evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json (step_0001, step_0002, step_0006)
   wcag_or_apg: WCAG 4.1.2 Name, Role, Value
   section_508_fpc_context: not in scope
   severity: MAJOR
   perspective_alarms: screen_reader=HIGH, keyboard=LOW, low_vision=LOW, cognitive=LOW
   evidence: step_0001 name="Sort by" (visible text "Newest▼"); step_0006 name="Sort by" (visible text "Price: low to high▼", after a real selection change)
   reproduction_steps: Tab to trigger button at any point before or after making a selection; inspect ax_name_role_state.name
   expected_behavior: Accessible name reflects the current selection, analogous to a native <select>'s announced value
   actual_behavior: Accessible name is the static label text "Sort by" regardless of selection state
   trend: new
   ```

3. **Listbox popup has no accessible name of its own.** `BuggyDropdown.jsx:53-60`: the `<ul role="listbox">` has no `aria-label` or `aria-labelledby`. Measured directly: at step_0003, `ax_name_role_state.name` is `""` and the spoken announcement is "listbox, oriented vertically" — no indication of what the listbox is for.
   - Confidence: HIGH
   - Why this matters: on its own this would be a straightforward APG-pattern gap (a listbox should be named, typically via `aria-labelledby` pointing at the trigger/label). **Mitigated by**: the trigger button's own name ("Sort by") is announced immediately before the user tabs into the listbox in the same interaction sequence, so short-term context is very likely preserved even without a dedicated name on the listbox itself — this mitigation is why the finding is kept at MAJOR rather than escalated to CRITICAL, per the Realist Check.
   - Fix: Add `aria-labelledby="dropdown-btn"` (or a dedicated visually-hidden label element referenced the same way) to the `<ul>`.

   ```
   ### A11y Evidence Finding
   finding_id: dropdown-listbox-missing-name
   fingerprint: 0d8e4f2b7961ac53
   source: evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json (step_0003)
   wcag_or_apg: WCAG 4.1.2 Name, Role, Value; WAI-ARIA APG Listbox pattern (listbox accessible name)
   section_508_fpc_context: not in scope
   severity: MAJOR
   perspective_alarms: screen_reader=MEDIUM, keyboard=LOW, low_vision=LOW, cognitive=LOW
   evidence: step_0003 — active_element_selector="#dropdown-list", ax_name_role_state.name="", sr_announcement.focus_announcement="listbox, orientated vertically"
   reproduction_steps: Tab to trigger, Enter to open, Tab into the listbox
   expected_behavior: Listbox has an accessible name (e.g. via aria-labelledby referencing the trigger) so its purpose is clear on arrival
   actual_behavior: Accessible name is empty; only "listbox, oriented vertically" is announced
   trend: new
   ```

**Minor Findings** (friction but workaround exists):
- `BuggyDropdown.jsx:41` — using a native `<label htmlFor>` pointed at a `<button>` (rather than the more conventional `aria-label`/visible in-button text) is non-standard for this element type. It happens to produce *a* name here, but relying on label-for-button association is fragile across browser/AT combinations and is part of why the button's own text content gets excluded from the name computation (see Major Finding 2). Worth revisiting as part of that fix rather than as a separate patch.

**Enhancements** (best practice not met):
- No `Home`/`End` key support to jump to the first/last option — optional per the WAI-ARIA APG Listbox pattern, not required.
- No type-ahead (character search) support — also optional per APG.
- No explicit `aria-setsize`/`aria-posinset` or position announcement ("2 of 3"); many screen readers announce listbox position automatically once `aria-activedescendant` is correctly wired (Critical Finding 1), so this may resolve for free once that fix lands — worth re-checking after the fix rather than treating as a separate task.
- Consider the ARIA 1.2 select-only Combobox pattern (`role="combobox"` on the trigger plus `aria-activedescendant` on the trigger itself) as a more fully-specified alternative to the current Menu-Button-opens-Listbox shape — not required; the current architecture is sound and does not need to be replaced, only completed.

**What's Missing** (gaps, unhandled edge cases, unstated assumptions):
- Stable DOM `id`s on the `<li>` options (`BuggyDropdown.jsx:62-71`) — a prerequisite for wiring `aria-activedescendant`, not just an attribute someone forgot.
- Click-outside / blur dismissal: no `onBlur` handler and no outside-click listener exist anywhere in the given source. As written, clicking elsewhere on the page or tabbing away without pressing Escape would leave the popup visually open with focus already gone. This is source-verified as absent, but not exercised by the trace, and it's possible a parent component handles this externally — see Open Questions.
- No independent verification of `Space` as an alternate activation key for the trigger — native `<button>` semantics make this a safe assumption, but it was not directly exercised in the provided trace (only `Enter` was).
- No 200%-zoom/reflow or touch-target-size evidence for this component (trace viewport is desktop, 1280×800 only) — the Low Vision perspective below is written with that gap explicit rather than assuming a pass.

**Multi-Perspective Notes**:
- **Screen reader user**: Tabbing to the trigger yields a correct, if incomplete, announcement ("button, Sort by, not expanded, has popup listbox"). Opening it and browsing options is close to a dead end: the listbox announces no name, arrow-key browsing produces no feedback at all, and selecting an option both fails to restore focus and fails to ever announce what was chosen. There is no available path, at any point, for a screen reader user to learn the current sort order.
- **Keyboard-only user**: Tab reaches the trigger and (after one extra, unintended Tab caused by the stale-ref bug) the listbox; arrow keys visibly move the highlighted option, so a sighted keyboard user can operate this successfully even though a screen-reader user cannot — a clear case of one perspective working while another breaks on the same code. Selecting an option (and, by code inspection, pressing Escape) drops focus to `<body>`, so even this user loses their visible focus indicator and must reorient by tabbing from scratch.
- **Low vision user (200% zoom, high contrast)**: Not evaluated by the provided evidence (desktop-only trace, no zoom/reflow data). What is measured: a focus outline is present in every captured step (`has_outline: true` throughout), which is a reasonable baseline, but its AAA-tier contrast (2.4.13) falls short in several steps (2.53–2.98:1) — informative only, since 2.4.13 is an AAA criterion and this project's stated baseline is WCAG 2.2 AA. Once focus drops to `<body>` (Critical Finding 2), there is no focus indicator anywhere on the page, which is a materially worse loss for a low-vision user tracking a focus ring than for an average-sighted user who can visually re-scan the page.
- **Cognitive accessibility**: The interaction model itself (button opens list, arrows move, Enter selects, Escape cancels) is standard and learnable — no unusual timeouts, no destructive actions, no re-entered data. The main cognitive cost is downstream of the focus-loss bug already scored above: losing your place in the page with no explanation is disorienting regardless of the reason, and that cost is shared with the keyboard-only perspective rather than being a separate defect.

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | HIGH | Trace-proven silent arrow-key browsing, empty listbox name, name never includes current value, focus lost on select |
| Keyboard-only | HIGH | Trace-proven focus lost to `<body>` on select; identical gap in the Escape code path; visible focus indicator disappears entirely |
| Low vision | MEDIUM | Focus-loss compounds indicator-tracking difficulty; zoom/reflow/touch-target not evaluated in the provided evidence |
| Cognitive | MEDIUM | Standard, learnable pattern, but shares the disorienting focus-loss bug |
| Vestibular & motion | LOW | No animation, transition, or auto-playing content in this component |
| Auditory access | LOW | No audio/video elements in this component |
| Environmental contrast | MEDIUM | Focus-ring contrast measured below the AAA bar (informative only, not the AA baseline); text-content contrast not measured in the evidence pack |

Screen reader and Keyboard-only both sit at HIGH — per this protocol, that is the threshold for escalating to `/perspective-audit` for deeper review before this component ships.

**Verdict Justification**: REVISE, not REJECT — the architectural choice (native button trigger + `aria-haspopup="listbox"` + `<ul role="listbox">`/`<li role="option">`) is sound and recognized; nothing here requires redesigning the interaction model from scratch. What's broken is completeness and wiring: two CRITICAL gaps (silent option browsing; focus not restored on close) and three MAJOR gaps (dead open-focus code; current value never in the accessible name; unnamed listbox, partially mitigated) are all fixable with targeted, well-scoped changes — stable option `id`s plus `aria-activedescendant`, a `useEffect`-based open-focus call, a ref-based close-focus call in both exit branches, and a value-inclusive accessible name. An upgrade to ACCEPT-WITH-RESERVATIONS would require, at minimum, verified fixes for both CRITICAL findings plus the button-name gap, confirmed against a re-run of the same driven trace goal (or equivalent manual AT testing) rather than a code-only fix. The review escalated beyond a surface ARIA-attribute check specifically because the driven trace exposed two things a static read would not have caught on its own: the complete announcement silence during arrow-key browsing, and the dead open-focus code path.

**Open Questions (unscored)**:
- The trace shows no captured announcement when `aria-expanded` flips from `false` to `true` on the already-focused button (step_0002: `new_phrases: []`). Real screen readers generally do announce state changes on the currently focused element, so this may be a capture-scope limitation of the driven-trace tooling rather than an application defect — needs verification with an actual NVDA/JAWS/VoiceOver session before being treated as a finding.
- Click-outside/blur dismissal is absent from the given source (see What's Missing), but this component may be wrapped by a parent that handles outside clicks externally — needs developer confirmation before scoring as a finding.
- `Space`-key activation of the trigger button was not independently exercised in the trace (only `Enter` was); native button semantics make failure unlikely, but it is technically unverified in the evidence provided.
- Low Vision perspective (200% zoom/reflow, touch target sizing, text-content color contrast) has no supporting evidence in this desktop-only trace and should not be signed off on the strength of this review alone.
