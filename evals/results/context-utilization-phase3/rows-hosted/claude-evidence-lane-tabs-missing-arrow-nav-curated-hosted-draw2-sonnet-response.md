# Accessibility Design Critique — Tabs Widget

**Reviewed artifact**: `TabsWidget` (React), its CSS, and the accompanying evidence pack (a driven keyboard-a11y-tester trace for this exact component, plus a 32-file findings corpus belonging to 32 other, distinct components).

**VERDICT: REVISE**

**Overall Assessment**: The markup layer of this Tabs widget is unusually clean — native buttons, correct `tablist`/`tab`/`tabpanel` roles, correctly paired `aria-controls`/`aria-labelledby` ids, valid boolean ARIA values, and a roving-tabindex attribute distribution that is textbook-correct. But the interaction layer that roving tabindex depends on was never built: there is no ArrowLeft/ArrowRight (or Home/End) handler anywhere in the component, so keyboard-only and screen-reader users can reach the active tab but have no way to reach any other tab. A driven keyboard trace against this exact component confirms the failure directly. A second, independent defect — a string-comparison bug in the Enter/Space handler — was found by close reading and is reported separately.

**Evidence Basis**: This review is grounded in (1) direct reading of the supplied JSX/CSS, and (2) the one evidence-pack artifact that actually describes this component: `tabs-missing-arrow-nav.trace.json` (4-step driven trace, read in full). The pack also bundles a 32-file findings corpus from 32 *other* components (accordion, modal, pagination, async form, a different tabs fixture, etc.) — none of those rows are used as evidence here, because none of them are about this component (the pack itself flags this: the one findings file that would have covered this component, `tabs-missing-arrow-nav.json`, was withheld). No axe-core scan, no virtual-screen-reader assertion log, and no codified `npx playwright test` transcript exist for this component in the supplied evidence — findings below are scoped accordingly, and I have not borrowed conclusions from any of the other 32 components' findings.

---

**Pre-commitment Predictions**: For a custom tabs widget, the most likely design gaps are (in order of likelihood): incomplete or absent arrow-key navigation; roving tabindex present in markup but not actually driven by any handler; `aria-controls`/`aria-labelledby` id mismatches; `aria-selected` not toggling correctly; and the tablist missing an accessible name. Investigation confirmed the first two and found nothing wrong with the latter three — see Synthesis for what this component got right that similar fixtures usually get wrong, and for one defect that wasn't on this prediction list at all.

---

**Critical Findings** (blocks access):

1. **Arrow-key navigation is entirely unimplemented; roving tabindex has no driver, so no tab other than the active one is keyboard-reachable.**
   `handleTabKeyDown` (lines 17–22) only branches on `'Enter'` and `' '`:
   ```
   const handleTabKeyDown = (e) => {
     if (e.key === 'Enter' || e.key === ' ') {
       e.preventDefault();
       handleTabClick(tabs.findIndex(t => t.id === e.currentTarget.id));
     }
   };
   ```
   There is no `ArrowLeft`/`ArrowRight`/`Home`/`End` branch anywhere in the component. Meanwhile `tabIndex={index === activeTab ? 0 : -1}` (line 34) removes every *non*-active tab from the natural Tab sequence — that's correct roving-tabindex markup, but roving tabindex exists specifically so arrow keys can move the "roving" 0 between siblings. With no arrow-key handler, the mechanism has no driver: once focus lands on the active tab via Tab, there is no keyboard path to any other tab. Mouse click still works, which is irrelevant to a keyboard-only or switch-access user.

   - Confidence: HIGH
   - User group impacted: keyboard-only users and screen-reader users (both drive this widget via focus/keys, not click). This is not a "trap" — Tab/Shift+Tab still move past the widget normally — it is a complete absence of the widget's primary interaction for anyone who can't click.
   - Why this matters: A screen reader user tabbing in hears the tab announce its full composite-widget state correctly (see evidence below — role, name, selection, set size are all communicated) — so they correctly learn there are 3 tabs. But the documented, expected next move (arrow keys) does nothing at all: no focus change, no announcement, no error. There is no fallback path either, because roving tabindex has already removed the other tab buttons from the Tab sequence. The realistic worst case here is a full content wall: a keyboard-only user cannot view whatever the second or third tab contains, full stop, without switching to a mouse. Detection is unlikely via casual QA (everything *looks* right — attributes are all present and correct) and axe-core cannot detect a missing keyboard handler. This is exactly the "looks accessible, isn't operable" trap the ARIA-pattern-compliance check exists to catch, made more convincing than usual because the roving-tabindex markup is done properly.
   - Measured evidence: `keyboard-a11y-tester` driven trace, `tabs-missing-arrow-nav.trace.json`. Tab correctly moves focus (`step_0001`: `{"keystroke":"Tab","selector":"#tab-overview","focus_moved":true}`; `step_0004`: `{"keystroke":"Tab","selector":"body","focus_moved":true}`), but both arrow-key presses fail to move focus at all: `step_0002`: `{"keystroke":"ArrowRight","selector":"#tab-overview","focus_moved":false}`; `step_0003`: `{"keystroke":"ArrowLeft","selector":"#tab-overview","focus_moved":false}`. The AX-state dict for `#tab-overview` is byte-identical across `step_0001`–`step_0003` (`{"invalid":"false","focusable":true,"focused":true,"selected":true,"controls":"panel-overview"}`), and `sr_announcement.focus_announcement` fires only at `step_0001` ("tab, Overview, selected, 1 control, position 1, set size 3") and is `null` at every subsequent step — consistent with focus simply never moving, not with a separate announcement defect (see calibration note below).
   - WCAG / APG: WCAG 2.1.1 Keyboard (the tab-switching function is not operable by keyboard); WAI-ARIA APG Tabs pattern, keyboard interaction (Left/Right Arrow must move focus among tabs, wrapping at the ends; the pattern additionally recommends Home/End to jump to first/last); WCAG 4.1.2 Name, Role, Value (the composite widget's expected operable contract is not fulfilled even though its static attributes are).
   - Fix: Add a keydown branch that, on `ArrowRight`/`ArrowLeft` (and ideally `Home`/`End`), computes the next/previous tab index (with wraparound), calls `.focus()` on that tab's button, and calls `setActiveTab` with the new index (or, per the manual-activation variant of the pattern, moves focus without changing selection until Enter/Space — either is APG-conformant as long as it's intentional and consistent). Verify with a live keyboard pass (Playwright `page.keyboard.press('ArrowRight')` or an `agent-browser` trace) confirming `focus_moved:true` and a correct `aria-selected` transition — the same instrument that caught this defect is the right one to confirm the fix.

   ```
   ### A11y Evidence Finding
   finding_id: tabs-arrow-key-navigation-missing
   fingerprint: not computed — no hashing tool available in this review pass; do not treat this line as a stable dedup key
   source: keyboard-a11y-tester driven trace, tabs-missing-arrow-nav.trace.json (steps step_0001–step_0004), corroborated by direct source read of handleTabKeyDown / tabIndex wiring
   wcag_or_apg: WCAG 2.1.1 Keyboard; WAI-ARIA APG Tabs pattern (arrow-key interaction); WCAG 4.1.2 Name, Role, Value
   section_508_fpc_context: not in scope — component-scope review, no declared Section 508 profile in the review request
   severity: CRITICAL
   perspective_alarms: screen_reader=HIGH, keyboard_only=HIGH, low_vision=MEDIUM, cognitive=MEDIUM, vestibular=LOW, auditory=LOW, environmental_contrast=MEDIUM
   evidence: |
     Code: no ArrowLeft/ArrowRight/Home/End branch in handleTabKeyDown (lines 17-22); tabIndex={index === activeTab ? 0 : -1} (line 34) removes non-active tabs from Tab order with no compensating path.
     Trace: step_0002 {"keystroke":"ArrowRight","focus_moved":false}; step_0003 {"keystroke":"ArrowLeft","focus_moved":false}; step_0001/step_0004 Tab presses both show focus_moved:true.
   reproduction_steps: |
     1. Tab into the tablist; focus lands on the active tab (#tab-overview).
     2. Press ArrowRight or ArrowLeft.
     3. Observe: selector, states, and aria-selected are unchanged; no other tab becomes reachable.
   expected_behavior: Per WAI-ARIA APG Tabs, ArrowRight/ArrowLeft move focus to the adjacent tab (wrapping) and update roving tabindex/aria-selected accordingly.
   actual_behavior: Focus and all ARIA/tabIndex state are unchanged; no tab besides the active one is reachable without a mouse.
   trend: new
   ```

**Major Findings** (significantly degrades experience):

1. **`handleTabKeyDown`'s Enter/Space branch compares the wrong id and always resolves to `-1`, which would zero out every tab's selection state for a render cycle.**
   Line 30 sets the DOM id as `` id={`tab-${tab.id}`} `` (e.g. `"tab-overview"`). Line 20's lookup compares the *bare* array id against that *prefixed* DOM id: `` tabs.findIndex(t => t.id === e.currentTarget.id) `` — `t.id` (`"overview"`) will never equal `e.currentTarget.id` (`"tab-overview"`), so this `findIndex` returns `-1` on every Enter/Space press, and `handleTabClick(-1)` calls `setActiveTab(-1)`. With `activeTab = -1`, every tab's `aria-selected` becomes `false`, every tab's `tabIndex` becomes `-1` (all tabs drop out of the tab sequence at once), and every panel's `hidden={index !== activeTab}` becomes `true` (all panel content disappears).
   - Confidence: HIGH on the defect itself (a plain string-equality bug, confirmed by reading lines 20 and 30 together) — MEDIUM on the exact user-visible severity, which depends on event-timing specifics I can't verify statically (see below) and which the evidence pack does not cover (the trace exercises arrow keys, not Enter/Space).
   - Why this matters: this branch only fires from a keyboard-originated event (`onKeyDown`), so it disproportionately exposes keyboard and screen-reader users to whatever it does — mouse clicks never touch this code path at all, since `onClick` uses the correctly closed-over numeric `index` (line 35) rather than the buggy id lookup. The two native key events don't behave identically here: for **Enter**, the browser's synthetic click follows the keydown almost immediately in the same task, so the correct `onClick`-driven `setActiveTab(index)` likely lands in the same React batch and overwrites the bad `-1` before anything paints — probably an inert no-op in practice. For **Space**, native button activation fires the synthetic click on `keyup`, a genuinely separate later event/task from the `keydown` that ran the buggy branch — meaning the `-1` state is plausibly committed and rendered (all tabs unselected, all panels hidden) *before* the correcting click resolves it on key-release. I can't confirm this timing without a live browser pass, so I'm reporting the defect at HIGH confidence and the "does it visibly flash" question as an open, testable claim rather than a settled fact.
   - WCAG / APG: WCAG 4.1.2 Name, Role, Value — the widget's exposed selection/visibility state can become simultaneously invalid across every tab and panel for a render cycle, specifically on keyboard activation.
   - Fix: Simplest correct fix is to delete this branch entirely — native `<button>` elements already activate via Enter and Space through the existing `onClick` handler, so the manual re-implementation is both buggy and redundant. If arrow-key handling is added to the same `onKeyDown` (per the Critical finding above), keep `onKeyDown` scoped to `ArrowLeft`/`ArrowRight`/`Home`/`End` only and let native activation semantics own Enter/Space. Verify with a live keyboard pass on Space specifically (not just Enter), watching for a mid-press flash of `aria-selected="false"` on all tabs.

**Minor Findings** (friction but workaround exists):
- No `Home`/`End` key support is defined for jumping to the first/last tab. This is a secondary piece of the same APG pattern gap above — once Left/Right exist, a user can still reach any tab by repeated arrow presses, so this is convenience rather than a blocker. Fold it into the arrow-key fix rather than treating it as a separate pass.

**Enhancements** (best practice not met):
- Each tab panel's content is a bare `<p>{tab.content}</p>` with no heading. Depending on how this widget is embedded in a page, a heading inside each panel (referenced from nowhere else) can help orient screen-reader users who tab past the tablist directly into panel content. Not enough page-level context here to call this a defect — noting it as a best-practice consideration only.
- Focus-indicator and text-contrast values computed from the given CSS (outline `#0066cc` on likely-white background ≈ 5.6:1; inactive tab text `#666` on likely-white ≈ 5.7:1; active tab text `#0066cc` ≈ 5.6:1) all clear the relevant 3:1/4.5:1 thresholds comfortably — but the actual production background behind `.tabs-container` isn't specified in the supplied CSS, so this is a calculation against an assumed white background, not a verified in-context measurement.
- The redundant Enter/Space handler (see Major finding #1) is also a plain code-hygiene issue independent of its accessibility angle — worth removing on general maintainability grounds even where it happens not to be user-visible.

**What's Missing** (gaps, unhandled edge cases, unstated assumptions):
- No codified, repeatable keyboard test exists for this component. The only hard keyboard evidence available is a single 4-step interactive trace — sufficient to catch the arrow-key defect, but not a committed regression guard. Once the arrow-key handler is added, a `.spec.js` Playwright test asserting `ArrowRight`/`ArrowLeft` move focus and update `aria-selected` (and one asserting Space doesn't transiently clear all tabs' selected state) should be committed alongside the fix.
- A findings file specifically for this component (`tabs-missing-arrow-nav.json`) exists in the evidence pack's source directory but was withheld from what I was given — I can neither corroborate nor rule out whatever it contains, and I have not guessed at its contents.
- No axe-core, virtual-screen-reader, or real-keyboard-Playwright evidence exists for this component in the supplied pack at all (the pack's 32-file findings corpus is `keyboard-a11y-tester`'s own deterministic detector output for *other* components, not axe-core, and not applicable here). Any future claim that this component "passes automated scanning" would need an actual scan run against it — none has been.
- Reflow/behavior at 200% zoom and in forced-colors mode is unverified either way; nothing in the supplied CSS suggests a problem (no fixed pixel widths on the flex tab row), but no viewport/zoom evidence exists to confirm it.

**Multi-Perspective Notes**:

| Perspective | Alarm Level | Trigger Signal |
|---|---|---|
| Screen reader | HIGH | Composite tablist widget with a confirmed keyboard-operability defect blocking access to non-active tabs; announcement is correct and complete when reachable, but most of the widget is unreachable |
| Keyboard-only | HIGH | Same defect — arrow-key navigation is fully non-functional per driven-trace evidence, and roving tabindex removes the sequential-Tab fallback |
| Low vision | MEDIUM | Standard interactive elements; computed contrast and apparent touch-target sizing pass on available evidence, but reflow at 200% zoom is unverified |
| Cognitive | MEDIUM | Arrow keys fail completely silently — no focus change, no announcement, no error — which compounds the access gap with pure confusion about whether the widget is broken |
| Vestibular & motion | LOW | Only a 0.2s color transition on hover; not motion-heavy |
| Auditory access | LOW | No media elements present |
| Environmental contrast | MEDIUM | Computed ratios pass comfortably against an assumed white background; true production background not confirmed in the supplied CSS |

- **Screen reader user**: Semantic structure is correct and complete — `role="tablist"` with an accessible name ("Content tabs"), `role="tab"` with `aria-selected`/`aria-controls`, `role="tabpanel"` with `aria-labelledby` pointing back at the right tab id. The trace confirms the announcement on reaching a tab is a well-formed, complete composite-widget announcement ("tab, Overview, selected, 1 control, position 1, set size 3"). The gap is entirely on the interaction side: arrow keys — the standard, taught way to move through a tablist — do nothing, and the only other tabs are not reachable by any other keyboard means either.
- **Keyboard-only user**: Tab correctly enters the tablist and lands on the active tab; focus indicator is visible. Arrow keys are dead. There is no keyboard trap in the literal sense (Tab/Shift+Tab still move past the widget), but there is also no way to switch tabs without a mouse — the core function of the widget is inoperable by keyboard alone.
- **Low vision user (200% zoom, high contrast)**: Nothing in the supplied CSS suggests fixed-width overflow at zoom; the focus outline (3px, offset 2px, `:focus` not gated to `:focus-visible`) should remain visible under magnification. Not independently verified against a live viewport.
- **Cognitive accessibility**: The silent no-op on arrow-key press is a discoverability problem on top of the access problem — a user who tries the "correct" interaction and gets no feedback at all has no way to know whether they made a mistake or the widget is broken.

**Verdict Justification**: One CRITICAL finding — complete loss of the widget's core function (switching tabs) for keyboard-only and screen-reader users, confirmed by both direct code reading and a measured driven-keyboard trace against this exact component — is sufficient on its own to require REVISE rather than ACCEPT-WITH-RESERVATIONS. A second, independently-discovered MAJOR finding (a real id-comparison bug in the Enter/Space handler, with a plausible but not live-confirmed visible consequence specifically on Space) reinforces this without changing the verdict tier. Realist Check: this is not a theoretical worst case — a keyboard-only user genuinely cannot view non-default tab content today, detection is unlikely via casual QA or axe-core (neither tests custom keyboard wiring), and there is no partial workaround once roving tabindex has removed the other tabs from the Tab sequence — so CRITICAL is not inflated by review momentum, and per the recalibration rules I did not downgrade it. What would need to change for an upgrade: implement APG-conformant Left/Right (and ideally Home/End) arrow-key navigation with wraparound, fix or remove the buggy Enter/Space id lookup, and verify both with a live keyboard pass (the same instrument class that surfaced the original defect). Given both Screen reader and Keyboard-only perspectives are flagged HIGH, this component is a good candidate for `/perspective-audit` escalation before re-review.

**Open Questions (unscored)**:
- Whether the Enter/Space id-mismatch bug (Major finding #1) produces a visible flash of "all tabs unselected / all panels hidden" in real browsers on Space release specifically is a testable claim, not a confirmed observation — it rests on React batching/event-timing reasoning I could not verify live in this pass (no browser tool access here). A single Playwright assertion capturing DOM state immediately after a `keyup` Space event would settle it either way.
- The withheld `tabs-missing-arrow-nav.json` findings file may contain additional detector output about this component that I have not seen and have deliberately not speculated about.
- Whether "the component these artifacts describe" is a coherent frame for an evidence pack that pairs one component's trace with 32 unrelated components' findings is a scope question the pack itself raises and leaves unresolved; I have treated only the trace as evidence about this component and treated the 32-file corpus as context about the pack's construction, not as findings against this widget.
- No conformance verdict, WCAG-SC pass/fail table, or severity rating for any *other* component mentioned in the padding corpus is offered here — that would be out of scope for a review of this component and is explicitly not claimed.
