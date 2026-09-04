**VERDICT: REJECT**

**Overall Assessment**: `BuggyDropdown` chooses the right ARIA vocabulary for a collapsible listbox (role="listbox"/"option", aria-haspopup, aria-expanded, aria-controls, aria-selected) but the focus-management and state-communication layer underneath that vocabulary is broken at every stage of the interaction lifecycle — open, navigate, and close all fail for keyboard and screen reader users, and the trigger's accessible name is permanently wrong. Four of these failures are independently CRITICAL and three are directly confirmed by measured keyboard-a11y-tester trace evidence, not just code inspection. The pattern choice does not need to change; the implementation cannot ship as-is.

**Pre-commitment Predictions**: Based on component type ("custom dropdown/select"), predicted before detailed investigation: (1) focus restoration after Escape/selection would be missing or inconsistent — the fixture's own name confirms this was the intended defect; (2) arrow-key navigation would be visually present but incomplete for assistive technology; (3) the options container might not be properly referenced/named; (4) selected state might not be announced; (5) an accidental focus-management gap might exist somewhere in the open path as well as the close path.

What was actually found matched (3) and (4) and confirmed (1), but was broader and more severe than predicted in two ways I did not anticipate going in: first, the "focus restoration" bug is not confined to closing — the documented "list receives focus" behavior on **opening** is also completely non-functional, and for a different, more subtle reason (a stale ref read inside the same synchronous handler that flips the state gating the ref's existence). Second, the ARIA-attribute-level accessible name of the trigger button is not merely "could be more specific" (a MINOR concern I expected) — it is measurably and permanently frozen to the static label text, never reflecting the selected value, which is a full state-communication failure, not a polish issue. Neither of these two root causes was part of my initial prediction list; both were surfaced only by combining code reading with the trace evidence.

---

**Critical Findings** (blocks access):

1. **Opening the dropdown never moves focus into the listbox — the documented "list receives focus" behavior is a no-op on every open.**
   `BuggyDropdown` component, lines 15–20 (`handleToggle`):
   ```
   const handleToggle = () => {
     setIsOpen(!isOpen);
     if (!isOpen && listRef.current) {
       listRef.current.focus();
     }
   };
   ```
   The `<ul ref={listRef}>` (lines 60–67) only mounts when `isOpen` is true (line 59: `{isOpen && (...)}`). On the render in which the user clicks/activates the button to open the dropdown, `isOpen` is still `false` at the time `handleToggle` runs, so the `<ul>` has not yet mounted and `listRef.current` is `null`. The guard `listRef.current &&` short-circuits, and `.focus()` is never called. `setIsOpen` is asynchronous/batched in React, so there is no tick within this handler where the ref becomes non-null before the check runs. This is not an edge case — it reproduces on every single open, every time, because the ref can never be attached in the same synchronous handler that first makes the condition for opening true.
   - Confidence: HIGH — directly measured, and independently explained by the code's control flow.
   - User group: Keyboard-only users and screen reader users. A sighted keyboard user's visible focus ring stays on the button while the list silently appears; a screen reader user hears no navigation into the popup at all.
   - Why this matters: The component's own "Expected Behavior" states "Opens on button click, list receives focus." This is the documented contract for the pattern, and it fails on the very first interaction. A user has no signal that pressing Enter/Space "did" anything beyond a state flip that isn't independently perceivable (see also the linked announcement gap below).
   - Fix: Do not call `.focus()` inside the click handler. Move the intent into a `useEffect` keyed on `isOpen`: `useEffect(() => { if (isOpen) listRef.current?.focus(); }, [isOpen]);`. This lets the effect run after React commits the DOM with the `<ul>` mounted, so the ref is guaranteed to be attached. Verify in DevTools' Accessibility/DOM inspector that focus actually lands on `#dropdown-list` after activation — do not rely on visual inspection alone (a sighted tester without a focus-ring check can easily miss this).

   ```
   ### A11y Evidence Finding
   finding_id: dropdown-open-focus-lost
   fingerprint: 4f1a9c02
   source: keyboard-a11y-tester driven-live trace — evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json, step_0002 (per the CURATED evidence digest supplied for this review)
   wcag_or_apg: WCAG 2.4.3 Focus Order; WAI-ARIA APG Listbox pattern (Collapsible/Popup variant) — activation is expected to move focus into the popup
   section_508_fpc_context: not in scope (no federal/508 profile declared for this review)
   severity: CRITICAL
   perspective_alarms: screen_reader=HIGH, keyboard=HIGH, low_vision=MEDIUM, cognitive=MEDIUM
   evidence: |
     step_0002 — keystroke_sent="Enter", active_element_selector stays "#dropdown-btn", focus_moved:false. States move from step_0001's expanded:false to expanded:true and gain controls:"dropdown-list". sr_announcement.new_phrases=[] and focus_announcement=null.
   reproduction_steps: Focus the "Sort by" trigger button; press Enter (or click) to open the listbox; observe active element and focus_moved flag.
   expected_behavior: Per the fixture's stated contract, activation opens the dropdown AND moves focus into the listbox (`listRef.current.focus()` is present in source, indicating this was the intended design).
   actual_behavior: aria-expanded flips true and aria-controls is gained, but the active element never changes and focus_moved is false — the intended focus call did not execute.
   trend: new
   ```

2. **Arrow-key navigation between options produces zero perceivable change for assistive technology — the Listbox pattern's focus-management requirement is unimplemented on both possible paths.**
   `BuggyDropdown` component, lines 32–35 (ArrowDown branch of `handleKeyDown`) and lines 60–78 (the `<ul>`/`<li>` markup):
   ```
   } else if (e.key === 'ArrowDown') {
     e.preventDefault();
     const nextIndex = selectedIndex < options.length - 1 ? selectedIndex + 1 : 0;
     setSelectedIndex(nextIndex);
   }
   ...
   <ul ref={listRef} id="dropdown-list" role="listbox" onKeyDown={handleKeyDown} tabIndex="0" className="dropdown-list">
     {options.map((option, index) => (
       <li key={index} role="option" aria-selected={index === selectedIndex} onClick={() => handleSelect(index)} className={index === selectedIndex ? 'selected' : ''}>
   ```
   The WAI-ARIA APG Listbox pattern requires ONE of two focus-management strategies for composite widgets: (a) roving tabindex, where DOM focus itself moves to each `<li>` (alternating `tabindex="0"`/`tabindex="-1"`), or (b) `aria-activedescendant` on the container that keeps DOM focus but tells assistive technology which option is "active." This implementation does neither. DOM focus stays on the `<ul>` (consistent with strategy b), but no `<li>` has an `id`, and the `<ul>` never sets `aria-activedescendant`. `aria-selected` does toggle correctly on the underlying `<li>` elements per the code, but with focus never moving and no activedescendant link, there is no mechanism for a screen reader to know that changed. The trace confirms this is not merely a theoretical gap: pressing ArrowDown produces literally no captured change beyond the keystroke itself.
   - Confidence: HIGH — directly measured (no option-level field appears in the AX capture at all), and independently confirmed by the complete absence of `id`/`aria-activedescendant`/per-option `tabindex` in the source.
   - User group: Screen reader users primarily — this is the widget's core task (choosing among options) and it is completely silent.
   - Why this matters: A screen reader user pressing ArrowDown/ArrowUp is attempting to browse the options. With zero announcement, they are selecting blind — they cannot know which option is "current" before pressing Enter to commit. This is exactly "screen reader users cannot access core functionality" per the severity scale, not a secondary polish gap.
   - Fix: Add a stable `id` to each `<li>` (e.g., `id={`dropdown-option-${index}`}`), and set `aria-activedescendant={`dropdown-option-${selectedIndex}`}` on the `<ul>`, updated in the same handler that updates `selectedIndex`. Verify via the accessibility tree inspector (not just visually) that `aria-activedescendant` resolves to the correct live `id` after each arrow press — per the "DOM-verification required" discipline for any fix that adds/wires an ARIA reference attribute.

   ```
   ### A11y Evidence Finding
   finding_id: dropdown-arrowkey-silent-nav
   fingerprint: 7b3e0d51
   source: keyboard-a11y-tester driven-live trace — evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json, step_0004 (per the CURATED evidence digest); corroborated by source inspection of lines 32–35 and 60–78
   wcag_or_apg: WCAG 4.1.2 Name, Role, Value; WAI-ARIA APG Listbox pattern, keyboard interaction / focus-management section (roving tabindex or aria-activedescendant)
   section_508_fpc_context: not in scope
   severity: CRITICAL
   perspective_alarms: screen_reader=HIGH, keyboard=MEDIUM, low_vision=LOW, cognitive=MEDIUM
   evidence: |
     step_0004 — keystroke_sent="ArrowDown", active_element_selector stays "#dropdown-list", focus_moved:false. Captured states are identical to step_0003 — no active-descendant or option-level field present. sr_announcement.new_phrases=[] and focus_announcement=null.
   reproduction_steps: Open the dropdown, move focus onto the listbox (via Tab, since the open-focus path is separately broken — see Critical Finding 1), press ArrowDown, inspect the accessibility tree for any change tied to the newly-highlighted option.
   expected_behavior: The newly active option should be exposed to assistive technology, either via DOM focus moving to it (roving tabindex) or via aria-activedescendant naming it while focus stays on the container.
   actual_behavior: No option-level state, id, or activedescendant reference appears anywhere in the captured AX data before or after the keystroke.
   trend: new
   ```

3. **Closing the dropdown — by selecting an option OR by pressing Escape — abandons focus to `<body>` with no restoration to the trigger.**
   `BuggyDropdown` component, lines 22–26 (`handleSelect`) and lines 29–31 (Escape branch of `handleKeyDown`):
   ```
   const handleSelect = (index) => {
     setSelectedIndex(index);
     onSelect(options[index]);
     setIsOpen(false);
   };
   ...
   if (e.key === 'Escape') {
     e.preventDefault();
     setIsOpen(false);
   }
   ```
   Both branches set `isOpen` to `false`, which unmounts the `<ul>` (line 59's conditional render). At the moment of unmount, the `<ul>` (or a descendant `<li>`, depending on how it was reached) currently holds DOM focus, per the interaction sequence. Neither branch contains any call that returns focus to `#dropdown-btn`. When a browser unmounts the focused node, focus falls through to `<body>` by default — there is no framework or browser mechanism that infers "the logical place to return to is the trigger that opened this." This is a textbook instance of the "else-branch coverage" anti-pattern: one might assume a developer wired restoration for the "normal" selection path and simply forgot Escape, but in fact **neither** path has any restoration code — the gap is total, not partial.
   - Confidence: HIGH for the selection path (directly measured in the trace). HIGH-but-not-independently-measured for the Escape path — no Escape keystroke appears anywhere in the supplied trace steps, so this half of the finding is derived from code inspection, not trace measurement. The code for both paths is structurally identical in what it lacks (a state-set with no accompanying focus call), so I hold the same confidence in both, but I am flagging the provenance difference explicitly per the evidence-tiering rule that test evidence outranks design reasoning.
   - User group: ALL keyboard users (sighted and screen reader alike) — this is a keyboard-operability failure, not solely an assistive-technology-communication gap. Being dropped to `<body>` means the next Tab press starts essentially from the top of the page's focus order, not from anywhere near the control just used.
   - Why this matters: This is the fixture's own named defect ("Focus Restoration Bug"), and the trace shows it is not a partial/inconsistent problem — it is a complete, 100%-reproducible loss of position on the only meaningful outcome of the widget (making a selection). The user must manually re-navigate the page to get back to the control they were just using.
   - Fix: In `handleSelect`, capture the trigger's intent to refocus before the state change causes anything to unmount, and call `.focus()` on a ref to the button after `setIsOpen(false)`, deferred with `setTimeout(() => triggerRef.current?.focus(), 0)` (or an effect keyed on `isOpen` transitioning false→already-was-true) so the call survives React's unmount/commit timing. Apply the identical fix to the Escape branch — do not fix only the selection path and leave Escape's branch unaddressed, per the "else-branch coverage" anti-pattern.

   ```
   ### A11y Evidence Finding
   finding_id: dropdown-close-focus-to-body
   fingerprint: c02f88a6
   source: keyboard-a11y-tester driven-live trace — evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json, step_0005 (selection path, measured); Escape path derived from source lines 29–31 (not independently measured in the supplied trace — no Escape keystroke appears in the digest's steps)
   wcag_or_apg: WCAG 2.4.3 Focus Order; WCAG 2.1.1 Keyboard (practical operability of the rest of the page is impaired until the user re-navigates)
   section_508_fpc_context: not in scope
   severity: CRITICAL
   perspective_alarms: screen_reader=HIGH, keyboard=HIGH, low_vision=MEDIUM, cognitive=MEDIUM
   evidence: |
     step_0005 — keystroke_sent="Enter" (sent per goals[0].intent to "pick an option"). active_element_selector becomes "body", tag="body", focus_moved:true. ax_name_role_state={"name":null,"role":"none","states":{}}; region, bounding_box, computed_focus_style all null. sr_announcement fields all empty/null. The next step (step_0006) reaches "#dropdown-btn" only via an explicit, separately-sent Shift+Tab — not automatically.
   reproduction_steps: Reach the listbox, press Enter on an option to select it; inspect active_element_selector immediately afterward. For the Escape path: open the dropdown, press Escape, inspect active_element_selector (not independently exercised in the supplied trace — recommend a dedicated driven step to convert this half of the finding from code-reasoning to measured fact).
   expected_behavior: Per the fixture's stated contract, "Selection should restore focus to button" and "Escape should close dropdown AND restore focus to button."
   actual_behavior: Focus moves to `<body>` (role:none, name:null) with no restoration; the trigger is only reached again via a manually-sent, separate navigation keystroke.
   trend: new
   ```

4. **The trigger button's accessible name is permanently frozen to the static label text and never reflects the currently selected option.**
   `BuggyDropdown` component, line 48 (`<label htmlFor="dropdown-btn">{label}</label>`) in combination with lines 49–58 (the button, whose visible content is `{options[selectedIndex]}`):
   ```
   <label htmlFor="dropdown-btn">{label}</label>
   <button id="dropdown-btn" aria-haspopup="listbox" aria-expanded={isOpen} aria-controls="dropdown-list" onClick={handleToggle}>
     {options[selectedIndex]}
     <span aria-hidden="true">▼</span>
   </button>
   ```
   The trace measures the button's computed accessible name as `"Sort by"` (the `label` prop's value) at the initial baseline (step_0001, referenced for comparison) AND again after a full open→navigate→select cycle (step_0006) — identical both times, even though the button's *visible* text content changed from `"Newest▼"` to `"Price: low to high▼"` in the same interval. The most likely mechanism, per HTML-AAM's accessible-name computation for `<button>` (a labelable element), is that the associated `<label for>` text takes precedence over the button's own subtree content when computing the accessible name — but regardless of the exact cross-engine mechanism, the *observed defect* is unambiguous and directly measured twice: the accessible name never tracks the selection.
   - Confidence: HIGH on the defect itself (measured twice, both before and after a state change that visibly altered the button's text). MEDIUM-HIGH on the specific causal mechanism (label-for-button precedence) — I have not independently verified this exact accessible-name-computation behavior across browser/AT engines beyond what the trace shows; the fix recommended below resolves the observed defect regardless of which mechanism is the precise cause.
   - User group: Screen reader users exclusively (this is a purely programmatic/AT-facing gap — sighted keyboard users see the correct updated text).
   - Why this matters: A sort-by control's entire purpose is to let a user choose and later confirm a selection. If a screen reader user tabs to this button at any point — before, during, or long after interacting with it — they hear only `"button, Sort by, ..."`, never the current sort order. Combined with Critical Finding 2 (silent navigation) and Critical Finding 3 (focus lost on close), there is no point in the interaction lifecycle at which a screen reader user can confirm what is currently selected. This is core-state communication failure, not a wording-preference issue.
   - Fix: Stop relying on `<label for>` to carry the button's accessible name if the button's name must be dynamic. Either (a) remove the `for`/`id` association and instead compose an explicit `aria-label={`${label}: ${options[selectedIndex]}`}` on the button so the name always includes both the static context and the live value, or (b) keep the visible `<label>` as a purely visual/contextual heading and verify in the accessibility tree that the button's own content-derived name is what actually gets exposed once the `for` association is removed. Whichever path is chosen, verify with a DOM/accessibility-tree inspection after a selection change — do not rely on the visible text alone, since that is precisely what is misleading here.

   ```
   ### A11y Evidence Finding
   finding_id: dropdown-trigger-name-stale
   fingerprint: 91dd4b17
   source: keyboard-a11y-tester driven-live trace — evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json, step_0001 (baseline, referenced) and step_0006 (per the CURATED evidence digest)
   wcag_or_apg: WCAG 4.1.2 Name, Role, Value (primary); WCAG 1.3.1 Info and Relationships (secondary — programmatically exposed information does not match the visually presented information)
   section_508_fpc_context: not in scope
   severity: CRITICAL
   perspective_alarms: screen_reader=HIGH, keyboard=LOW, low_vision=LOW, cognitive=MEDIUM
   evidence: |
     step_0006 — keystroke_sent="Shift+Tab", active_element_selector="#dropdown-btn". text field = "Price: low to high▼" (step_0001's text was "Newest▼"). ax_name_role_state.name = "Sort by" — identical to step_0001. sr_announcement.focus_announcement = "button, Sort by, not expanded, has popup listbox" — identical string to step_0001's focus_announcement.
   reproduction_steps: Note the button's accessible name and focus announcement at rest; open the dropdown, select a different option than the current default, return focus to the button; compare the accessible name/announcement to the initial reading.
   expected_behavior: The button's accessible name should reflect the currently selected option (or at minimum change when the visible text changes), so a screen reader user can learn the current state without re-opening the widget.
   actual_behavior: The accessible name and focus announcement are byte-identical before and after a selection that visibly changed the button's text.
   trend: new
   ```

---

**Major Findings** (significantly degrades experience):

1. **The listbox popup has no accessible name.**
   `BuggyDropdown` component, lines 60–67 (`<ul ref={listRef} id="dropdown-list" role="listbox" ...>`). No `aria-label` or `aria-labelledby` is present anywhere on the `<ul>`. The trace measures the listbox's computed accessible name as an empty string (`""`) while its role is correctly `"listbox"`.
   - Confidence: HIGH — directly measured (empty name captured twice, step_0003 and step_0004), and confirmed absent in source.
   - Why this matters: A screen reader user who reaches the listbox (by whatever means, since the intended auto-focus path is separately broken) hears an unnamed listbox — "listbox" with no further context. This is a real, if less severe, degradation than the CRITICAL findings above: the user has *some* contextual continuity from having just left the "Sort by" button, but that continuity is not programmatically guaranteed (e.g., if focus reaches the listbox by a different path, or if the page has more than one such control).
   - Fix: Add `aria-labelledby` on the `<ul>` pointing to the same visible `<label>` element's `id` (give the `<label htmlFor="dropdown-btn">` an explicit `id`, e.g. `id="dropdown-btn-label"`, and reference it: `aria-labelledby="dropdown-btn-label"`), or add a direct `aria-label` matching the `label` prop.

   ```
   ### A11y Evidence Finding
   finding_id: dropdown-listbox-unnamed
   fingerprint: 2a6f0e39
   source: keyboard-a11y-tester driven-live trace — evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json, step_0003 (per the CURATED evidence digest); corroborated by source inspection of lines 60–67 (no aria-label/aria-labelledby present)
   wcag_or_apg: WCAG 4.1.2 Name, Role, Value; WAI-ARIA APG Listbox pattern (accessible name requirement for the listbox element)
   section_508_fpc_context: not in scope
   severity: MAJOR
   perspective_alarms: screen_reader=HIGH, keyboard=LOW, low_vision=LOW, cognitive=LOW
   evidence: |
     step_0003 — active_element_selector="#dropdown-list", tag="ul". ax_name_role_state.name = "" (empty string), role="listbox".
   reproduction_steps: Move focus onto the `<ul id="dropdown-list">` and read its computed accessible name.
   expected_behavior: The listbox should have a non-empty accessible name (matching or complementing the trigger's label).
   actual_behavior: Accessible name is the empty string; role is correctly "listbox".
   trend: new
   ```

---

**Minor Findings** (friction but workaround exists):

- **No blur/outside-interaction close handling.** Neither `handleToggle` nor `handleKeyDown` includes an `onBlur` handler on the `<ul>` or wrapper. If a user Tabs away from the open listbox without pressing Escape or selecting an option, `isOpen` remains `true` indefinitely — the popup stays visually expanded with `aria-expanded="true"` on a trigger that no longer has focus, creating a lingering, orphaned expanded region. Workaround exists (Escape or a selection does close it), so this is not blocking, but it is a real design-coherence gap worth closing. (`BuggyDropdown` component, lines 8–44 — no blur handler anywhere in the component.)
- **No Home/End key support.** The WAI-ARIA APG Listbox pattern's full keyboard interaction model includes Home (jump to first option) and End (jump to last option) in addition to Arrow Up/Down. Only Arrow Up/Down (with wraparound) are implemented (lines 32–39). A user can still reach any option via repeated arrow presses, so this is friction, not a blocker.

**Enhancements** (best practice not met):

- Add an explicit `type="button"` to the trigger element (line 49) so this component is defensively safe if ever rendered inside a `<form>` — a bare `<button>` defaults to `type="submit"`, which could trigger unintended form submission in that context. Not evidenced as an active bug here (the fixture doesn't show a surrounding `<form>`), but a low-cost robustness improvement.
- Consider type-ahead (single-letter-key jump to a matching option) per the full WAI-ARIA APG Listbox keyboard interaction model — not required, but expected in mature implementations of this pattern.

---

**What's Missing** (gaps, unhandled edge cases, unstated assumptions):

- No `id` on any `<li>` option, which is the prerequisite for wiring `aria-activedescendant` (see Critical Finding 2).
- No focus-restoration call in either dropdown-closing branch (see Critical Finding 3) — the gap is total, not partial; this is not a case of one branch being fixed and another forgotten, but of neither branch ever having the logic at all.
- No mechanism, anywhere in the component, for a screen reader user to learn the current selection independent of re-opening the listbox and separately re-discovering which `<li>` carries `aria-selected="true"` (a path that is itself broken per Critical Finding 2). Fixing the trigger's accessible name (Critical Finding 4) is the primary remedy; an additional `aria-live="polite"` confirmation region is a reasonable supplementary mitigation but should not be treated as a substitute for the name fix.
- **Explicitly not claimed**: this review does not assert a page-level landmark or heading-structure verdict. The evidence pack's own per-step `region` field (`landmark:null, heading:null`) is scoped to whatever element happened to hold focus at each step, not a DOM-wide census, and a leaf dropdown component would not be expected to establish its own landmark/heading context regardless. No axe-core artifact was supplied for this review, so no machine-detectable/structural-scan verdict (full ARIA-role validity across the DOM, landmark census) is being asserted either — only what source inspection and the supplied trace directly support.

---

**Multi-Perspective Notes**:

- **Screen reader user**: Broken at every stage. Opening produces an `aria-expanded` flip with no focus movement and no captured announcement (Critical Finding 1). Once inside the listbox (reachable only by manually Tabbing, since auto-focus is broken), the listbox announces as an unnamed "listbox" (Major Finding 1). Arrow-key navigation produces no perceivable change at all — the user is choosing blind (Critical Finding 2). Confirming a selection drops focus to `<body>`, announced as nothing (`role:none`, `name:null`) (Critical Finding 3). Returning to the trigger by any means yields the same static "Sort by, not expanded, has popup listbox" announcement regardless of what is actually selected (Critical Finding 4). There is no point in this interaction lifecycle at which a screen reader user can both operate the widget and confirm its resulting state.
- **Keyboard-only user**: The visible focus ring does not follow the documented behavior on open (stays on the button instead of moving into the list, per Critical Finding 1) — recoverable only because `tabIndex="0"` on the `<ul>` happens to make Tab work as a fallback path, which is not the same as the intended one-key-press interaction. Arrow keys inside the list do move the visual `.selected` styling (assuming supporting CSS, not shown in this fixture), so this population fares somewhat better than screen reader users during navigation. Selecting an option, however, drops focus to `<body>` (Critical Finding 3) for every keyboard user, sighted or not — the next Tab press starts essentially from the top of the page's focus order, forcing a full re-navigation to get back to the control just used.
- **Low vision user (200% zoom, high contrast)**: No CSS was supplied with this fixture, so focus-indicator visibility/contrast (WCAG 2.4.7, 2.4.13), reflow at 200% zoom, and target size of the `<li>` rows (WCAG 2.5.8) cannot be assessed from the artifacts provided — flagged as an evidence gap in Open Questions rather than scored either way. The decorative `▼` glyph is correctly `aria-hidden="true"` (line 57), so it does not introduce screen-reader noise, but its visual contrast as a low-vision affordance is likewise unverifiable without CSS.
- **Cognitive accessibility**: The chosen interaction model (open → arrow keys → Enter, or direct click) is conventional and learnable; there are no timeouts, no destructive actions, and no validation/error states in this component, so most of the cognitive-perspective checklist is not applicable here. The one cross-cutting concern is that the disorienting focus-loss-to-`<body>` behavior (Critical Finding 3) would compound confusion for any user with attention or processing differences layered on top of assistive technology use — this is the same underlying defect as the keyboard/screen-reader findings above, not an independent cognitive-specific gap, so it is not counted separately.

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | HIGH | Custom composite widget (listbox/option) with confirmed, measured failures at open, navigate, and close/confirm stages |
| Keyboard-only | HIGH | Measured, 100%-reproducible focus loss to `<body>` on selection; code-confirmed identical gap on Escape; broken auto-focus on open |
| Low vision | MEDIUM | Standard control shape, but focus-indicator contrast, zoom reflow, and target size are unverifiable — no CSS supplied |
| Cognitive | MEDIUM | Conventional, learnable pattern with no dedicated cognitive-only defects, but shares exposure to the disorienting focus-loss behavior above |
| Vestibular & motion | LOW | No animation, transition, or auto-playing content present in the code |
| Auditory access | LOW | No media elements present |
| Environmental contrast | MEDIUM | No CSS supplied to verify text/icon contrast ratios; flagged for a check before shipping rather than scored |

Screen reader and Keyboard-only are both at HIGH — per the protocol, this component should be flagged for deep review via `/perspective-audit` before any revised implementation ships.

---

**Verdict Justification**: REJECT, not REVISE. This verdict is about the *implementation as submitted*, not the underlying pattern choice — the WAI-ARIA APG Listbox-popup vocabulary chosen here (role="listbox"/"option", aria-haspopup, aria-expanded, aria-controls, aria-selected) is the right skeleton, and several details are genuinely correct: the decorative `▼` glyph is properly `aria-hidden` (line 57), `aria-expanded`/`aria-selected` serialize to valid ARIA boolean strings via React's pass-through handling (not "yes"/"no", not omitted), a native `<button>` is used for the trigger rather than a div-with-role, and both the Escape and Arrow-key handlers correctly call `e.preventDefault()` to suppress unwanted native behavior. None of that is in question.

What blocks shipping is that four independent CRITICAL defects span the *entire* interaction lifecycle rather than one isolated point: the open path's focus movement is a no-op (stale ref), the navigate path is completely silent to assistive technology (no roving tabindex or aria-activedescendant), both close paths abandon focus to `<body>` with zero restoration code in either branch, and the trigger's accessible name is permanently disconnected from the value it is supposed to represent. Running the Realist Check against each: the realistic worst case is not a theoretical edge case but the widget's single primary use case failing on the first attempt, every time, for the population that depends on ARIA most; detection would very plausibly take days rather than minutes in production, since a sighted developer testing by mouse would see the visible button text update correctly and would not notice that the *accessible* name never does, and would not notice the focus-to-`<body>` jump unless specifically watching the focus ring after using the keyboard. No CRITICAL finding was downgraded — each independently meets "blocks access entirely for a user category" with no workaround present in the code, and none involves a theoretical-only violation.

To move this to REVISE or better on re-review: implement the four CRITICAL fixes (effect-based open-focus, aria-activedescendant or roving tabindex for navigation, deferred focus-restoration on both close paths, and a trigger accessible-name that tracks the selected value) plus the MAJOR listbox-naming fix. None of these require abandoning the chosen pattern.

**Open Questions (unscored)**:

- Focus-indicator visibility and contrast (WCAG 2.4.7 Focus Visible, 2.4.11 Focus Not Obscured, 2.4.13 Focus Appearance) cannot be assessed — no CSS was supplied with this fixture.
- Target size of the `<li>` option rows (WCAG 2.5.8) cannot be assessed — no CSS was supplied.
- Text/icon color contrast (WCAG 1.4.3, 1.4.11) cannot be assessed — no CSS was supplied.
- Whether this component is ever rendered inside a `<form>` element is not stated; this affects how much weight the missing `type="button"` (Enhancement) should carry in practice.
- The Escape-key half of Critical Finding 3 (focus abandoned to `<body>`) is derived from code inspection, not independently measured in the supplied trace — no Escape keystroke appears in the digest's steps. A dedicated driven-trace step exercising Escape would convert this from a high-confidence code-reasoning claim to a fully measured one.
- Whether `sr_announcement.new_phrases` being empty on the aria-expanded state change in step_0002 reflects a genuine "screen readers announce nothing here" behavior, or a limitation of the driven-trace tool's capture when focus does not move, is not fully resolved by the evidence supplied. It is folded into Critical Finding 1 rather than treated as an independent finding, since it is confounded with the same root cause (focus never moves on open).
