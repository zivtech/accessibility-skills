# Accessibility Design Review — `TabsWidget`

**VERDICT: REJECT**

**Overall Assessment**: The ARIA *vocabulary* here is close to exemplary — roles, relationships, `aria-selected`, and roving tabindex are all present and all resolve correctly in the accessibility tree (confirmed by the driven trace). The ARIA *behavior* is missing, and the combination is worse than either defect alone: roving tabindex removes tabs 2 and 3 from the Tab sequence, and no arrow-key handler exists to put them back, so a keyboard-only user has **no path of any kind** to two of the three panels. Separately, the one keyboard handler that does exist contains an identifier-comparison bug that sets `activeTab` to `-1` on Enter or Space, deselecting every tab, hiding every panel, and dropping the whole tablist out of the tab sequence. This is not a pattern that needs polishing; it is a pattern whose interactive half was never wired up.

---

## Phase 0 — Test Evidence Consumed (and Rejected)

**Evidence type check.** This is a fresh design pass, not a remediation review, so the a11y-test verification-evidence-contract mismatch check does not apply. No axe-core, Playwright `.spec.js`, `agent-browser`, or `virtual-screen-reader` artifacts were supplied.

**What is in scope.** Exactly one artifact in the supplied pack describes the component under review:

- `evals/results/keyboard-a11y-tester/driven/tabs-missing-arrow-nav.trace.json` — `mode: driven-live`, `start_url: http://127.0.0.1:8777/tabs-missing-arrow-nav.html`, personas `keyboard` + `screen-reader`, desktop 1280×800, goal `adhoc` / "navigate between tabs using arrow keys", 4 steps.

**What is out of scope — and why I am not importing any of it.** The remaining 27 artifacts are `findings/*.json` files from a **batch crawl of sibling pages**. Every one of them carries a different `url` (`accordion-no-region-role.html`, `app-focus-order-illogical.html`, `pagination-no-nav-landmark.html`, …). None describes `tabs-missing-arrow-nav.html`. Three specific traps in this pack that I am declining:

1. **`tabs-incomplete-aria-selected.json`** is the most seductive misattribution in the dump — it is about tabs, and it carries `missing-accessible-name-desktop` / "1 focusable control(s) have no accessible name: tabpanel at `#panel-1`". That finding belongs to `http://127.0.0.1:8777/tabs-incomplete-aria-selected.html`, a *different fixture*. The component under review names its panels via `aria-labelledby`, and the selectors (`#tab-1`, `#panel-1`) do not match this component's generated ids (`#tab-overview`, `#panel-overview`). Importing it would be a fabricated finding.
2. **`test_case_id` is not a page discriminator.** Every artifact in the pack — driven trace and all 27 crawl files — carries `"test_case_id": "127-0-0-1"`. That is derived from the host, not the page. The only reliable discriminator is the `url` / `start_url` field. Anyone joining these artifacts on `test_case_id` will silently merge 28 unrelated pages.
3. **`sr-live-region-silent-desktop` (WCAG 4.1.3)** appears in five sibling files. Per keyboard-a11y-tester calibration rule 1, batch-crawl "silent live region" findings are prompts to run a driven session, never failure evidence — and here they are doubly inapplicable, being about other pages entirely. Not filed.

**Calibration applied to the in-scope trace.** `conformance_level` is a pass/fail gate, not the SC's WCAG level (upstream issue #27), so I derived levels from the SC numbers. WCAG 2.4.13 genuinely is AAA, so the "informative only" framing in the sibling crawls is coincidentally right there — but it is not the reason I am treating it as informative.

**Coverage note (what the trace does *not* cover).** Desktop 1280×800 only; four keystrokes (`Tab`, `ArrowRight`, `ArrowLeft`, `Tab`); one goal. It contains **no** Enter/Space activation, no Home/End, no mobile or 320px viewport, no 200% zoom, no forced-colors run, and no multi-instance render. Findings 2, 4, 5, and 6 below therefore rest on source reading, and I say so in each.

**Fingerprint provenance.** The `fingerprint` values in the evidence blocks below are report-local content hashes over (finding_id + primary selector + WCAG SC). They are **not** emitted by keyboard-a11y-tester; do not expect to find them in `trace.json`.

---

## Phase 1 — Pre-commitment Predictions

Written before reading the source, based on component type (custom tabs widget):

| # | Prediction | Outcome |
|---|---|---|
| P1 | Arrow-key navigation missing from the tablist | **Confirmed** — and worse than predicted (see Phase 10) |
| P2 | `aria-selected` present but not synchronized with visual active state | **Refuted** — synchronized correctly |
| P3 | Panels not referenced by `aria-controls` / `aria-labelledby` | **Refuted** — both directions wired and resolving |
| P4 | Tabpanel not reachable when it has no focusable content | **Confirmed** — measured |
| P5 | A live region will be missing for panel-change announcements | **Refuted, and it should be** — the APG Tabs pattern needs no live region; announcing the panel swap would be redundant with the `selected` state change. Filing this would have been a manufactured violation. |

Two things I did not predict: the activation handler's identifier bug (Finding 2), and the possibility that screen-reader browse-mode users have an accidental workaround the keyboard-only user does not (Phase 6).

---

## Phase 2 — Semantic HTML Audit

Genuinely correct, and worth saying so plainly:

- **Native `<button>` is used for tabs** (line 28). No `div role="button"`. The "native HTML first" constraint is satisfied at the element level. Trace `step_0001` confirms `"tag": "button"`.
- **Roles enhance, not replace.** `role="tab"` on a `<button>` is the APG-sanctioned overlay; it is not papering over a non-interactive element.
- Panels are `<div role="tabpanel">` — correct; there is no native tabpanel element.
- No tables, no lists misused, no `role="presentation"` misuse, no `title`-as-accessible-name, no font-icon or `::before`/`::after` text leakage. All the third-party-audit anti-patterns (items 1–9) come back clean here.

Two observations that are **not** component findings:

- **No landmark, no heading.** Trace reports `"region": { "landmark": null, "heading": null }` at every step. For a reusable widget exported from its own module, landmark and heading structure belong to the consuming page, not to `TabsWidget`. Flagging a component for the absence of `<main>` is page-shell over-flagging. Moved to Open Questions.
- **Background color is undeclared.** `.tab-button { background: transparent }` with no ancestor background in the supplied CSS. All contrast reasoning below assumes white. Stated as an assumption, not asserted as measured.

---

## Phase 3 — ARIA Pattern Compliance Audit

**Pattern: WAI-ARIA APG Tabs (Tabs with Manual Activation / Automatic Activation).**

Structural requirements — verified against source *and* against the computed accessibility tree in the trace, not assumed:

| APG requirement | Present? | Evidence |
|---|---|---|
| `role="tablist"` on container | Yes | line 26 |
| Accessible name on tablist | Yes | `aria-label="Content tabs"`, line 26 |
| `role="tab"` on each tab | Yes | line 31; trace `step_0001.ax_name_role_state.role: "tab"` |
| `aria-selected` true on active, false on others | Yes | line 32; trace `states.selected: true` |
| `aria-controls` → panel id | Yes | line 33; trace `states.controls: "panel-overview"` — resolves, and the SR announcement says `1 control` |
| `role="tabpanel"` on each panel | Yes | line 47 |
| `aria-labelledby` → tab id | Yes | line 50, matching `id` at line 30 |
| Roving tabindex (0 on active, −1 on others) | Yes | line 34 |
| Inactive panels removed from AT | Yes | `hidden` at line 51 |
| `aria-orientation` | Omitted, correctly | default is `horizontal`; CSS is `display: flex` row (line 73) |
| **Arrow key navigation (Left/Right)** | **NO** | lines 17–22 handle only Enter/Space |
| Home / End (APG-optional) | No | lines 17–22 |

React serializes `aria-selected={boolean}` to the string `"true"`/`"false"` — valid values, confirmed by the computed state in the trace. No invalid ARIA values anywhere.

So the pattern is roughly 80% complete in exactly the way the protocol warns about: everything visible in the DOM is right, and the part that makes the interaction coherent for assistive technology is absent.

**Activation-model incoherence.** The presence of a (broken) Enter/Space handler implies an intent toward **manual activation**. But manual activation requires the roving tabindex to track a *focused* tab independently of the *selected* tab. Here `tabIndex` is bound to `activeTab` (line 34) — the selection state. There is no `focusedTab` state at all. The component has therefore committed to neither activation model; it has the tabindex wiring of automatic activation and the (intended) key handler of manual activation, with no arrow keys to connect either.

---

## Phase 4 — Focus Management Review

**Measured tab order (trace, 4 steps):**

| Step | Key | Resulting focus | `focus_moved` |
|---|---|---|---|
| `step_0001` | `Tab` | `#tab-overview` (tabindex 0) | true |
| `step_0002` | `ArrowRight` | `#tab-overview` — unchanged | **false** |
| `step_0003` | `ArrowLeft` | `#tab-overview` — unchanged | **false** |
| `step_0004` | `Tab` | `body` | true |

Three facts fall out of that table:

1. Arrow keys are inert. `focus_moved: false` on both, with `sr_announcement.new_phrases: []` — nothing happened, and nothing was said about nothing happening.
2. Tabs 2 and 3 are never reached. The SR announcement at `step_0001` reports `set size 3`, so the widget advertises three tabs; the keyboard can reach one.
3. Tab from the active tab lands on `body`, skipping the tabpanel entirely.

**Focus indicator.** `.tab-button:focus { outline: 3px solid #0066cc; outline-offset: 2px }` (lines 100–103), confirmed as computed style in every step. WCAG 2.4.7 Focus Visible: **passes**.

**A deliberate non-finding on WCAG 2.4.13.** The trace's `focus_appearance` block reports `aaa_pass: false` on `step_0001`/`step_0002` and `aaa_pass: true` (`changed_area: 719` vs `ref_area_2px_perimeter: 625`, `contrast: 5.56`) on `step_0003` — for the *same element with the same computed outline*. The `false` results carry `changed_area: 0` and `contrast: null`, which is the signature of a frame-delta measurement taken when the indicator was already painted in the reference frame (steps 1 and 2 had `pixel_cue: false`; step 3 had `pixel_cue: true`). The measurable read is step 3's: 3px solid #0066cc at 2px offset gives 5.56:1 against white and exceeds the 2px-perimeter area reference. I independently computed #0066cc on #FFFFFF as **5.56:1**, matching the tool exactly. **No focus-appearance finding.** Reporting one off `aaa_pass: false` would be a false positive manufactured from a measurement artifact — and 2.4.13 is AAA regardless, above this project's WCAG 2.2 AA target.

**Other focus checks:** no modal/drawer, so no focus trap or restoration requirement. No SPA route change. No async CRUD. No positive tabindex. No `visibility:hidden` focus-reveal pattern. No `aria-hidden` container needing `inert` (panels use the `hidden` attribute, which correctly removes them from both the a11y tree and the tab sequence). Focus stays on the clicked tab after mouse activation — correct per APG.

---

## Phase 5 — State Communication Audit

Selection state is communicated **correctly and completely** — this is the component's strongest area:

- `aria-selected` toggles with `activeTab` and is computed as `selected: true` in the accessibility tree.
- The focus announcement at `step_0001` is `"tab, Overview, selected, 1 control, position 1, set size 3"` — role, name, selection state, controls relationship, and set position all present.
- Visual active state is **not** color-alone: `.tab-button.active` adds `font-weight: 600` and `border-bottom-color` alongside `color` (lines 94–98). WCAG 1.4.1 satisfied.
- No `title`-as-name, no visual text symbols (`+`/`×`/`>`) needing `aria-hidden`.

Gaps:

- **No state communication for the `activeTab === -1` collapse** (Finding 2). When Enter/Space fires the buggy handler, every panel disappears and every tab reports `aria-selected="false"`. Nothing is announced; there is no live region and, correctly, there shouldn't be one for normal tab switching — but there is also no recovery affordance. The user hears silence and finds an empty widget.
- **No live region needed for normal panel switching.** Explicitly not a finding. The APG Tabs pattern communicates the change through the `selected` state on the focused tab. Adding `aria-live` here would produce the "broadcast vs. association" anti-pattern in reverse — redundant announcements on every arrow press.

---

## Phase 6 — Multi-Perspective Review

**Screen reader user (NVDA / JAWS / VoiceOver).** Structure and naming are good; the computed announcement is complete and unredundant. But the experience splits by mode, and the split is counterintuitive:

- *Browse/virtual-cursor mode:* the user can move the virtual cursor to any tab and press Enter. NVDA/JAWS dispatch a synthetic `click()` for this, which reaches `onClick={() => handleTabClick(index)}` with the correct closure index — bypassing the broken keydown handler entirely. **Tab switching works.** This is an accident, not a design.
- *Focus/forms mode:* the user is in the same position as a keyboard-only user — arrow keys do nothing, Tab exits the widget, and Enter triggers the `-1` collapse.

**Keyboard-only user (sighted, no AT).** This is the group with **no workaround at all**. Tab reaches one tab. Arrows do nothing. Enter or Space — the two keys any user would try next — destroys the widget. Two-thirds of the component's content is unreachable, and the one interaction available makes things worse. Switch-access and voice-control users who drive the focus ring inherit the same dead end.

**Low vision user (200% zoom, magnifier, forced colors).** Focus indicator is strong (3px, 5.56:1, 2px offset) and survives magnification. Targets measure 111.16 × 45 CSS px (trace `bounding_box`) — comfortably above WCAG 2.5.8's 24×24 and above the 44×44 recommendation. Text contrast computes as #666 on white = **5.74:1** and #0066cc on white = **5.56:1**, both above 4.5:1 for normal text (applying the stricter *text* threshold, not the 3:1 UI-boundary threshold). Two unverified exposures, both in Open Questions: forced-colors mode overrides both `color` and `border-bottom-color`, leaving only `font-weight: 600` to distinguish the active tab; and `display: flex` with no `flex-wrap` on a 3-tab row of ~111px each plus gaps exceeds a 320px viewport.

**Cognitive accessibility.** The interaction model is undiscoverable and, worse, actively misleading. A tab strip looks like three clickable things; two of them cannot be reached by keyboard and there is no cue explaining that arrow keys would be the mechanism (there are no arrow keys). Pressing Enter — the most conventional "activate this" key in the entire platform — produces an unexplained empty state with no undo, no message, and no way back. That is a consistency violation (WCAG 3.2.1-adjacent, and a plain design failure): the same key that activates every other control on the page here erases content.

**Vestibular & motion.** `transition: color 0.2s` (line 87) is a color fade, not motion — no translation, scale, parallax, or auto-play. This does **not** require a `prefers-reduced-motion` guard, and flagging it would be a manufactured violation. LOW.

**Auditory access.** No `<video>`, `<audio>`, or auditory alerts. LOW.

**Environmental contrast.** Ratios computed above all pass AA. Color is never the sole indicator (font-weight + border co-signal). Forced-colors behavior unverified.

### Perspective Alarm Levels

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | MEDIUM | Custom composite widget; ARIA correct and verified, but forms-mode users hit the same dead end as keyboard users, and Enter collapses state |
| Keyboard-only | **HIGH** | Measured: arrows inert, roving tabindex removes 2 of 3 tabs from the sequence, Tab exits to `body`; Enter/Space destroys widget state |
| Low vision | MEDIUM | Indicator and target size measured-good; forced-colors and 320px reflow unverified |
| Cognitive | MEDIUM | Undiscoverable interaction model; Enter produces unexplained, unrecoverable empty state |
| Vestibular & motion | LOW | Only a 0.2s color transition — not motion |
| Auditory access | LOW | No media elements, no auditory alerts |
| Environmental contrast | MEDIUM | Ratios pass on an assumed-white background; forced-colors overrides both active-state color cues |

**Escalation:** Keyboard-only (HIGH) warrants `/perspective-audit`. Screen reader, Low vision, Cognitive, and Environmental contrast (MEDIUM) should be included in that pass.

---

## Phase 7 — Gap Analysis (What Is Absent)

- **No arrow-key handler.** The single largest absence. Lines 17–22 contain the only keydown logic in the file.
- **No `Home` / `End`.** APG-optional, but trivial to add alongside arrows.
- **No `focusedTab` state.** Manual activation is impossible without it; the component cannot currently express "focus is on tab 3, selection is still tab 1."
- **No `tabIndex={0}` on the tabpanel**, and no focusable content inside it — so the panel is unreachable (measured, `step_0004`).
- **No `useId`/instance prefix on generated ids.** `tab-${tab.id}` and `panel-${tab.id}` are global.
- **No `forced-colors` media query.**
- **No `flex-wrap` on the tablist**, and no narrow-viewport evidence.
- **No guard on `handleTabClick`'s index.** `setActiveTab(-1)` is accepted silently; a `if (index < 0) return;` would have converted Finding 2 from a widget-destroying bug into a no-op.
- **No test covering Enter/Space.** The driven trace sent four keystrokes and none of them was an activation key — which is precisely how a defect this severe survived a measured session.

Checked and confirmed **not** missing: live region (not required by the pattern), focus restoration (no dismissible surface), skip link (page-level), `lang` (page-level), field labels (no form), reduced motion (no motion), captions/transcripts (no media), `aria-current` (not a navigation component), dragging alternative (no drag), destructive-action confirmation — see Finding 2, where an *undo* is exactly what is missing, though the correct fix is to remove the destructive behavior rather than confirm it.

---

## Findings

### Critical Findings (blocks access)

**1. CRITICAL — Roving tabindex plus missing arrow-key handler makes 2 of 3 tabs unreachable by keyboard.**

Evidence: `tabIndex={index === activeTab ? 0 : -1}` at line 34 removes every non-active tab from the Tab sequence. `handleTabKeyDown` (lines 17–22) handles only `Enter` and `' '` — there is no `ArrowRight`, `ArrowLeft`, `Home`, or `End` branch, so nothing restores a keyboard path to those tabs. Measured in `tabs-missing-arrow-nav.trace.json`: `step_0002` (`ArrowRight`) and `step_0003` (`ArrowLeft`) both report `"focus_moved": false` with `active_element_selector` unchanged at `#tab-overview` and `sr_announcement.new_phrases: []`; `step_0004` (`Tab`) leaves the widget for `body`. The tab's own announcement declares `set size 3`.

User group: keyboard-only (complete loss), switch and voice-control users driving the focus ring (complete loss), screen-reader users in focus/forms mode (complete loss). Screen-reader users in browse mode retain an accidental workaround via synthetic click — which is not a mitigation, because it does nothing for the group with no AT.

Standard: WAI-ARIA APG **Tabs** pattern — "When focus is on a tab in a horizontal tab list, Left Arrow moves focus to the previous tab, Right Arrow to the next tab." WCAG **2.1.1 Keyboard**.

- Confidence: **HIGH** (measured, two independent keystrokes, corroborated by source)
- Why this matters: This is not degraded navigation; it is the absence of navigation. Two panels' worth of content exist in the DOM, are announced as existing (`set size 3`), and cannot be opened by anyone using a keyboard. A sighted keyboard user can see the tabs they cannot reach.
- **Severity note (why CRITICAL and not MAJOR):** the generic "custom tabs lack arrow keys" defect is usually MAJOR, because tabs typically remain individually Tab-reachable and the user merely loses an ergonomic shortcut. Roving tabindex is what converts this one to CRITICAL: it deliberately removes the Tab path *on the assumption that arrow keys will supply it*, and that assumption was never honored. Had `tabIndex={0}` been left on all tabs, this would be MAJOR.
- Fix:
  ```jsx
  const tabRefs = useRef([]);

  const handleTabKeyDown = (e, index) => {
    const last = tabs.length - 1;
    let next;
    switch (e.key) {
      case 'ArrowRight': next = index === last ? 0 : index + 1; break;
      case 'ArrowLeft':  next = index === 0 ? last : index - 1; break;
      case 'Home':       next = 0; break;
      case 'End':        next = last; break;
      default: return;                       // let Enter/Space reach the native button
    }
    e.preventDefault();
    setActiveTab(next);                      // automatic activation
    tabRefs.current[next]?.focus();
  };
  ```
  with `ref={(el) => (tabRefs.current[index] = el)}` and `onKeyDown={(e) => handleTabKeyDown(e, index)}` on each tab. **Automatic activation is the right model here** because panel content is already in the DOM (`<p>{tab.content}</p>`, line 54) — selection-follows-focus costs nothing. If panel content ever becomes async-loaded, switch to manual activation by introducing a separate `focusedTab` state, binding `tabIndex` to it, and selecting on Enter/Space.

```
### A11y Evidence Finding
finding_id: tabs-arrow-key-navigation-absent
fingerprint: 7c3f9a1e5b02d4a8
source: evals/results/keyboard-a11y-tester/driven/tabs-missing-arrow-nav.trace.json (mode: driven-live); TabsWidget source lines 17-22, 34
wcag_or_apg: WCAG 2.1.1 Keyboard; WAI-ARIA APG Tabs pattern (Left Arrow / Right Arrow keyboard interaction)
section_508_fpc_context: In scope if project policy declares Revised Section 508 — 2.1.1 is WCAG 2.0 Level A and maps to the 508 web basis. Not declared for this review; treated as WCAG 2.2 AA.
severity: CRITICAL
perspective_alarms: keyboard=HIGH, screen-reader=MEDIUM, cognitive=MEDIUM, low-vision=MEDIUM, vestibular=LOW, auditory=LOW, environmental-contrast=MEDIUM
evidence: trace.json step_0002 keystroke_sent="ArrowRight" focus_moved=false active_element_selector="#tab-overview"; step_0003 keystroke_sent="ArrowLeft" focus_moved=false active_element_selector="#tab-overview"; step_0004 keystroke_sent="Tab" active_element_selector="body"; step_0001 sr_announcement.focus_announcement="tab, Overview, selected, 1 control, position 1, set size 3"; source line 34 tabIndex={index === activeTab ? 0 : -1}
reproduction_steps: Load http://127.0.0.1:8777/tabs-missing-arrow-nav.html; press Tab to focus the first tab; press ArrowRight; press ArrowLeft; press Tab.
expected_behavior: ArrowRight moves focus to tab 2 (and wraps from the last tab to the first); ArrowLeft moves focus to the previous tab; Tab from the tablist moves to the active tabpanel.
actual_behavior: Focus remains on #tab-overview through both arrow presses with no announcement; the next Tab leaves the component for body. Tabs 2 and 3 (set size 3) are never focusable.
trend: new
```

---

**2. CRITICAL — The Enter/Space handler compares mismatched identifiers, sets `activeTab` to `-1`, and destroys the widget.**

Evidence: line 30 renders `id={`tab-${tab.id}`}` — so `e.currentTarget.id` is `"tab-overview"`. Line 20 then evaluates `tabs.findIndex(t => t.id === e.currentTarget.id)` — comparing the *raw* `tab.id` (`"overview"`) against the *prefixed* DOM id (`"tab-overview"`). These can never be equal, so `findIndex` returns `-1` and `handleTabClick(-1)` runs `setActiveTab(-1)`. Because line 19 calls `e.preventDefault()` first, the native button click that would otherwise fire the correct `onClick` handler is suppressed, so nothing corrects the bad value.

Consequences after a single Enter or Space press, all deterministic from the render logic:
- Line 32: every tab renders `aria-selected="false"` — the tablist reports no selection.
- Line 51: every panel renders `hidden` — all content vanishes.
- Line 34: every tab renders `tabIndex="-1"` — **the entire tablist drops out of the tab sequence.** Once focus leaves, no keyboard user can ever return to it.

User group: keyboard-only, screen-reader users in focus/forms mode, switch and voice-control users. Mouse users are unaffected (their `onClick` path is correct), which is why this survives manual QA.

Standard: WCAG **2.1.1 Keyboard**; WCAG **4.1.2 Name, Role, Value** (`aria-selected` no longer reflects any valid widget state); WAI-ARIA APG Tabs pattern (exactly one tab in a tablist has `aria-selected="true"`).

- Confidence: **HIGH** on the logic; the state transition is deterministic from source. **Unmeasured** — the supplied trace sent `Tab`, `ArrowRight`, `ArrowLeft`, `Tab` and never sent an activation key, so no artifact in the pack exercises this path.
- Could the developer refute this? Only by showing that `tab.id` values already carry the `tab-` prefix — in which case line 30 would render `id="tab-tab-overview"` and the `aria-controls`/`aria-labelledby` pairs would still resolve (they are built from the same expression), so the trace's observed `#tab-overview` selector rules that out. The refutation does not survive the evidence.
- Why this matters: Enter and Space are the two keys a user reaches for first. Pressing either on the one tab they *can* reach empties the component, tells them nothing, and locks them out of it permanently for the rest of the page session. It is a worse outcome than the missing arrow keys, produced by the only keyboard code in the file.
- Fix: **Delete `handleTabKeyDown`'s Enter/Space branch entirely and remove `onKeyDown={handleTabKeyDown}` in its present form.** These are native `<button>` elements; the browser already fires `click` on Enter and Space, and `onClick={() => handleTabClick(index)}` (line 35) already closes over the correct index. Intercepting activation on a native button and calling `preventDefault()` is the "native HTML first" violation that created this bug. Replace the handler with the arrows-only version from Finding 1, whose `default: return;` branch deliberately lets activation keys fall through to native behavior. As defense in depth, guard the setter: `const handleTabClick = (index) => { if (index < 0 || index >= tabs.length) return; setActiveTab(index); };`

```
### A11y Evidence Finding
finding_id: tabs-activation-handler-index-mismatch
fingerprint: b41d8e07f2569cc3
source: TabsWidget source lines 17-22 (handleTabKeyDown), line 20 (findIndex comparison), line 30 (id template), lines 32/34/51 (render consequences) — code-read, not measured
wcag_or_apg: WCAG 2.1.1 Keyboard; WCAG 4.1.2 Name, Role, Value; WAI-ARIA APG Tabs pattern (exactly one aria-selected="true" per tablist)
section_508_fpc_context: In scope if project policy declares Revised Section 508 — 2.1.1 and 4.1.2 are WCAG 2.0 Level A and map to the 508 web basis. Not declared for this review; treated as WCAG 2.2 AA.
severity: CRITICAL
perspective_alarms: keyboard=HIGH, screen-reader=MEDIUM, cognitive=MEDIUM
evidence: line 30 id={`tab-${tab.id}`} yields e.currentTarget.id === "tab-overview" (corroborated by trace step_0001 active_element_selector="#tab-overview"); line 20 tabs.findIndex(t => t.id === e.currentTarget.id) compares "overview" !== "tab-overview" and returns -1; line 19 e.preventDefault() suppresses the native click that would have invoked the correct onClick path.
reproduction_steps: Load the component; press Tab to focus the selected tab; press Enter (or Space). Inspect the DOM: every [role=tab] should now report aria-selected="false" and tabindex="-1", and every [role=tabpanel] should carry the hidden attribute. Then press Tab twice and attempt to return to the tablist.
expected_behavior: Enter or Space on the focused tab selects that tab; exactly one tab reports aria-selected="true" and its panel remains visible.
actual_behavior: DERIVED FROM SOURCE, NOT MEASURED IN THE SUPPLIED TRACE — activeTab becomes -1; no tab is selected, all panels are hidden, and all tabs receive tabindex="-1", removing the tablist from the tab sequence with no recovery path.
trend: new
```

### Major Findings (significantly degrades experience)

**3. MAJOR — Tabpanel has no focusable content and no `tabIndex={0}`, so keyboard users cannot reach or scroll panel content.**

Evidence: the panel at lines 46–56 contains only `<p>{tab.content}</p>` — no interactive descendants — and carries no `tabIndex`. Measured: `step_0004` sends `Tab` from `#tab-overview` and lands on `body`, with `dom_order_index: -1` and `is_body: true`; the panel is never a focus stop.

User group: keyboard-only and screen-magnifier users (a screen-reader user reading in browse mode reaches the text via the virtual cursor and is unaffected).

Standard: WAI-ARIA APG **Tabs** pattern — "If the tab panel does not contain any focusable elements, the panel itself should be included in the tab sequence by adding `tabindex='0'`." WCAG **2.1.1 Keyboard** (a scrollable region must be operable by keyboard; this is the `scrollable-region-focusable` class of defect).

- Confidence: **HIGH** (measured skip + source read)
- Why this matters: with short content this is invisible. With a panel longer than the viewport, a keyboard-only user cannot scroll it — there is no focusable element inside to receive arrow-key scrolling and the container itself refuses focus. In a reusable component the content length is the consumer's decision, so the defect is latent by design.
- Fix: add `tabIndex={0}` to the tabpanel div (line 46). Because the panel is already named via `aria-labelledby` and has `role="tabpanel"`, it will announce correctly as a focus stop. If a future version puts focusable controls inside panels, drop the `tabIndex` conditionally rather than leaving a redundant stop.

```
### A11y Evidence Finding
finding_id: tabpanel-not-in-tab-sequence
fingerprint: 2ea6740b9d18f5a1
source: evals/results/keyboard-a11y-tester/driven/tabs-missing-arrow-nav.trace.json step_0004; TabsWidget source lines 46-56
wcag_or_apg: WCAG 2.1.1 Keyboard; WAI-ARIA APG Tabs pattern (tabindex="0" on a tabpanel with no focusable descendants)
section_508_fpc_context: In scope if project policy declares Revised Section 508 — 2.1.1 is WCAG 2.0 Level A. Not declared for this review; treated as WCAG 2.2 AA.
severity: MAJOR
perspective_alarms: keyboard=HIGH, low-vision=MEDIUM, screen-reader=LOW
evidence: trace.json step_0004 keystroke_sent="Tab" active_element_selector="body" tag="body" is_body=true dom_order_index=-1; source lines 46-53 render role="tabpanel" with no tabIndex and only a <p> child at line 54.
reproduction_steps: Load the page; press Tab to focus the active tab; press Tab again and observe the active element.
expected_behavior: Tab from the tablist moves focus into the active tabpanel so its content can be read and scrolled by keyboard.
actual_behavior: Focus moves past the tabpanel directly to body; the panel is never a focus stop.
trend: new
```

### Minor Findings (friction, workaround exists)

- **ARIA ids are globally derived and will collide across instances.** Lines 30, 33, 50, and 48 build ids from `tab.id` with no instance prefix. Two `TabsWidget` instances on one page sharing any `tab.id` value produce duplicate ids, and `aria-controls`/`aria-labelledby` then resolve to the first match — silently associating a tab with another widget's panel. WCAG 1.3.1 Info and Relationships, 4.1.2. Confidence MEDIUM (depends on consumer usage; unverifiable from the single-instance trace). Fix: `const uid = useId();` then `id={`${uid}-tab-${tab.id}`}` with matching references. Note that fixing this also removes the temptation that produced Finding 2 — the prefix mismatch — by making the derived-id relationship explicit.
- **`aria-label="Content tabs"` is weakly distinguishing.** Screen readers announce the role, so "tabs" is redundant, and "Content" does not identify *which* content if a page carries more than one tablist. Functional as-is; this is polish, not a gap. Fix: name the tablist after what it organizes (e.g. `aria-label="Product details"`), or reference a visible heading with `aria-labelledby`.

### Enhancements (best practice not met, no access barrier)

- **No `forced-colors` handling.** In Windows High Contrast Mode, `color: #0066cc` and `border-bottom-color: #0066cc` (lines 95–96) are both overridden by system colors, leaving `font-weight: 600` as the only visual distinction between the active and inactive tabs. `aria-selected` keeps the state programmatically available, so this is not an access barrier — but a `@media (forced-colors: active)` block using `Highlight`/`HighlightText` or a `border-bottom-style` change would restore the visual cue. WCAG 1.4.1 (forced-colors robustness).
- **`Home` / `End` keys.** APG-optional but conventional; already included in the Finding 1 fix.
- **No `flex-wrap` on the tablist** (line 73). See Open Questions for the unverified reflow exposure.

---

## Phase 8 — Realist Check (Severity Calibration)

**Finding 1 (CRITICAL):** Realistic worst case — a keyboard-only user reaches one tab of three and can never open the other two; the content simply does not exist for them. Impacted groups: keyboard-only, switch, voice, SR-in-forms-mode. Detection if shipped: **never**, silently — mouse QA passes, axe-core passes (all required ARIA attributes are present), and even the driven trace's *deterministic* findings would not have caught it without the arrow-key goal being specified. Proportional? Yes — this is complete access loss for a user category, which the recalibration rules forbid downgrading. **Kept CRITICAL.**

**Finding 2 (CRITICAL):** Realistic worst case — one keypress empties the widget with no announcement and permanently removes the tablist from the tab sequence. Impacted: keyboard-only, SR-in-forms-mode, switch, voice. Detection if shipped: **days at best** — it is invisible to mouse testing and to automated scanning, and the user-facing symptom ("the tabs disappeared") is easy to misattribute to a data problem. Proportional? Yes; complete access loss plus unrecoverable state. **Kept CRITICAL.** I considered downgrading to MAJOR on the argument that a page reload restores the widget — I rejected it. A reload is not a workaround for a user who has just lost their place in a document, and the same keypress reproduces it immediately.

**Finding 3 (MAJOR):** Realistic worst case — a keyboard user cannot scroll a long panel. With short panels the impact is nil. Impacted: keyboard-only, magnifier. Detection: days (user report). Proportional? Considered downgrading to MINOR on the "short content, no impact" argument. **Rejected the downgrade** — this is a reusable component whose panel content is supplied by the consumer, so the defect is latent in every deployment rather than absent from this one, and the APG names the requirement explicitly. **Kept MAJOR.**

**Recalibrations made:** the ID-collision finding was drafted at MAJOR and **downgraded to MINOR** — *Mitigated by:* the failure only manifests when two instances with overlapping `tab.id` values render on the same page, which no supplied evidence demonstrates and which many consumers will never do. The forced-colors item was drafted at MINOR and **downgraded to ENHANCEMENT** — *Mitigated by:* `aria-selected` keeps selection state programmatically available in forced-colors mode, and `font-weight: 600` survives the override, so information is degraded rather than lost.

**Findings I declined to raise** (recorded so the calibration is auditable): WCAG 2.4.13 focus appearance (measurement artifact — see Phase 4); missing `prefers-reduced-motion` (a color transition is not motion); missing live region for panel changes (the pattern does not want one); the `tabpanel`-missing-name finding from `tabs-incomplete-aria-selected.json` (different page); all five `sr-live-region-silent` findings (different pages, and calibration rule 1 makes them prompts rather than failures); missing landmark/heading (page-shell concern, not a component defect).

---

## Phase 9 — Self-Audit

| Finding | Confidence | Developer could refute? | Gap or preference? |
|---|---|---|---|
| 1 — arrow keys absent | HIGH | No — measured twice, plus source | GAP |
| 2 — activation index mismatch | HIGH (logic), unmeasured | No — the trace's `#tab-overview` selector rules out the only refutation | GAP |
| 3 — tabpanel not focusable | HIGH | No — measured skip to `body` | GAP |
| ID collision | MEDIUM | Yes, with usage context | GAP (conditional) — filed MINOR |
| `aria-label` wording | HIGH | Yes | PREFERENCE — kept MINOR, non-blocking |
| forced-colors | MEDIUM | Yes | GAP (minor) — filed ENHANCEMENT |

Moved to Open Questions: 320px reflow, forced-colors behavior, page-level landmark/heading context, and the undeclared background color — all are either unmeasured or outside the component's boundary.

---

## Phase 10 — Synthesis (Predictions vs. Findings)

I predicted the missing arrow keys (P1) and the unreachable tabpanel (P4). I was wrong about `aria-selected` (P2), `aria-controls`/`aria-labelledby` (P3), and the live region (P5) — all three are handled correctly, and P5 in particular would have been a manufactured violation had I filed it from the prediction rather than checking the pattern.

Two genuine surprises:

1. **The severity of P1 was higher than the generic case**, because roving tabindex was implemented *correctly and in isolation*. The component was penalized by getting one half of the pattern right. That is the sharpest lesson here: partial APG implementation can be worse than none, because roving tabindex actively removes the fallback that the naive implementation would have left in place.
2. **The activation handler bug (Finding 2) was not on my prediction list at all**, and it is arguably the more dangerous of the two CRITICALs. It was invisible to the supplied measured evidence — the driven session sent four keystrokes and none of them was Enter or Space. This is the strongest argument in this review for reading source alongside traces: a trace can only falsify the hypotheses someone thought to test.

---

## Multi-Perspective Notes

- **Screen reader user:** Semantic structure and computed announcements are correct and verified — `"tab, Overview, selected, 1 control, position 1, set size 3"` is a complete, non-redundant announcement with role, name, state, relationship, and set position. The experience then splits by mode: browse-cursor users can switch tabs through a synthetic click and are largely fine; forms-mode users hit the same dead end as keyboard users and can additionally trigger the Enter collapse, after which the tablist reports three tabs and zero selection.
- **Keyboard-only user:** The worst-served group, with no workaround. One of three tabs reachable, arrows inert (measured), Tab exits to `body` (measured), and the two conventional activation keys destroy the widget (source). The focus indicator is excellent — which means the user can see precisely where they are stuck.
- **Low vision user (200% zoom, high contrast):** Focus indicator measures 3px solid #0066cc at 2px offset, 5.56:1, exceeding both the AA requirement and the AAA area/contrast reference. Targets are 111×45 CSS px, well above 24×24. Text contrast passes AA on an assumed white background (#666 = 5.74:1; #0066cc = 5.56:1). Unverified: forced-colors strips both active-state color cues, and a no-wrap flex tablist at 320px may force horizontal scroll.
- **Cognitive accessibility:** The interaction model is undiscoverable — there is no cue that arrow keys are the intended mechanism, and no arrow keys anyway. Pressing Enter, the platform's most conventional activation key, produces an unexplained empty state with no message, no undo, and no path back to the tablist. Consistency with the rest of any host page is broken in the most disorienting way available.

---

## Verdict Justification

**REJECT.** Two independent CRITICAL defects block keyboard access, and one of them silently and unrecoverably destroys widget state. The component cannot ship in this condition, and I am not treating it as REVISE-able-in-place because the second defect means the only keyboard code currently in the file must be removed rather than extended.

That said, the honest framing matters: **the ARIA architecture is sound.** Roles, relationships, naming, selection state, roving tabindex, and panel hiding are all correct, and I verified each against the computed accessibility tree rather than assuming from source. The failure is entirely in the interaction layer — perhaps twenty lines of behavior that were specified in the fixture's own "Expected Behavior" section ("Arrow Left/Right should cycle through tabs") and never written. The distance from REJECT to ACCEPT-WITH-RESERVATIONS here is short but non-negotiable.

**To upgrade to ACCEPT-WITH-RESERVATIONS**, all three must be true:
1. Arrow Left/Right (with wrap) plus Home/End move focus within the tablist, verified by a new driven `keyboard-a11y-tester` session showing `focus_moved: true` and the correct `active_element_selector` at each arrow step.
2. The Enter/Space keydown interception is removed so native button activation applies, and `handleTabClick` rejects out-of-range indices — verified by a test that presses Enter on each tab and asserts exactly one `aria-selected="true"` remains.
3. The tabpanel carries `tabIndex={0}`, verified by a trace step showing `active_element_selector` matching the panel id after Tab from the tablist.

**To reach ACCEPT**, additionally resolve the ID-collision risk with `useId` and add the `forced-colors` block.

**Escalation:** Keyboard-only is at HIGH alarm. Run `/perspective-audit` on this component after the fixes land, covering keyboard-only (HIGH) plus screen reader, low vision, cognitive, and environmental contrast (MEDIUM). The re-test must include activation keys and a narrow viewport — the gap that let Finding 2 through was the test plan, not the tool.

---

## Open Questions (unscored)

1. **320px reflow (WCAG 1.4.10).** `[role="tablist"]` is `display: flex` with `gap: 4px` and no `flex-wrap` (lines 72–76). Three tabs at the measured 111.16px plus gaps total roughly 341px, and flex items will not shrink below min-content. Does the tablist overflow horizontally at a 320px viewport? Unmeasured — the trace is desktop 1280 only, and the answer depends on label length. **Check:** re-run the driven session at 320×640 and inspect for horizontal scroll on the tablist.
2. **Forced-colors behavior.** Does the active tab remain visually distinguishable in Windows High Contrast Mode with only `font-weight: 600` surviving? **Check:** load in Edge with High Contrast enabled and screenshot the tab strip.
3. **Background color.** `.tab-button { background: transparent }` with no ancestor background in the supplied CSS. All contrast figures above assume white. **Check:** confirm the host page background; if it is anything darker than roughly #E8E8E8, re-verify #666 against it.
4. **Page-level context.** The trace reports `landmark: null, heading: null` at every step. Does the consuming page wrap this widget in a landmark and precede it with a heading? Out of scope for the component itself, but a screen-reader user's ability to *find* this widget depends on it.
5. **Multi-instance usage.** Is `TabsWidget` ever rendered more than once per page, and can `tab.id` values repeat across instances? Determines whether the ID-collision MINOR is latent or live.
6. **Panel content length.** Are panels ever taller than the viewport? Determines the real-world weight of Finding 3.
7. **Is manual activation ever required?** If panel content becomes async-loaded, the automatic-activation fix in Finding 1 must be replaced with a `focusedTab`-based manual model. Worth deciding now rather than after the fix ships.
