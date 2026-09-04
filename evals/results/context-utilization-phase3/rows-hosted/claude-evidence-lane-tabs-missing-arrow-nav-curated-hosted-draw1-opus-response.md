**VERDICT: REVISE**

**Overall Assessment**: The ARIA scaffolding on this tabs widget is complete and correct — roles, `aria-selected`, `aria-controls`, `aria-labelledby`, roving tabindex, and `hidden` are all wired properly, and the supplied trace confirms the accessibility tree computes as intended. What is missing is the entire keyboard interaction layer the pattern depends on, and what is present in its place is actively destructive. Two CRITICAL defects compound: the roving tabindex removes every inactive tab from the tab order while no arrow-key handler exists to reach them, and the one keyboard handler that does exist contains an identifier mismatch that sets `activeTab` to `-1` on any Enter or Space press — blanking every panel and removing every tab from the tab order permanently. A mouse user will never see either defect. A keyboard-only user is locked out of the widget after one keypress.

---

## Phase 0 — Evidence Intake and Scope Ruling

**Review type**: Fresh design pass, not a remediation review. The a11y-test *Verification evidence contract* type-match check (which fires when evidence is offered as proof of a *fix*) does not apply here. No prior-state evidence was offered and none is required.

**Evidence tier of the supplied pack**: The material provided is an `a11y-evidence-reader` digest (`def_rev 2026-08-26a`), not the artifacts themselves. Per the Phase 0 rule, a digest is **detector output, one tier below the artifact it cites** — a paraphrase. The rule requires re-fetching at the cited handle before filing a finding that rests on a digest line. This review was executed against the supplied pack only; **no re-fetch was performed**. Consequence, applied honestly throughout:

- Every evidence line drawn from the digest is labeled **digest-only** at the point of use.
- **No finding in this review rests on a digest line alone.** Both CRITICAL findings are established from the component source supplied inline in the prompt (primary evidence, directly readable), with the digest serving as corroboration.

**Evidence inventory**:

| Instrument | Present? | For this component? |
|---|---|---|
| keyboard-a11y-tester driven trace (4 steps) | Yes | **Yes** — `tabs-missing-arrow-nav.trace.json` |
| keyboard-a11y-tester batch-crawl findings | Yes, 32 files | **No** — 32 other, distinct components |
| axe-core scan (`machine-detectable`) | **No** | — |
| virtual-screen-reader assertions (`name-role-state`) | **No** | — |
| Real-keyboard Playwright transcript (`keyboard-operability`) | **No** | — |

**Scope ruling on the 32-file findings corpus — none of it is evidence about this component.** The digest's own absence claim is explicit: no in-policy findings file names `tabs-missing-arrow-nav`; every non-empty row belongs to one of 32 other components. I am therefore filing **zero findings** derived from that corpus. This matters because the corpus is shaped to invite transplantation:

- `focus-appearance-weak-desktop` (19 of 32 files, WCAG 2.4.13) is the most numerous row in the pack and is doubly inapplicable. First, it is not this component's. Second, calibration rule 4 applies — `conformance_level: "AAA"` on this row is a pass/fail-gate artifact (upstream issue #27), and the digest correctly marks the row "Informative only." Third, and decisively, this component's declared focus style at `TabsWidget.css:33-36` (`outline: 3px solid #0066cc; outline-offset: 2px`) computes to a 3px perimeter at **5.56:1** against white — it would *pass* the AAA bar the row describes. Importing that row would have been a fabricated finding contradicted by the source.
- `missing-accessible-name-desktop` (WCAG 4.1.2, severity "serious") appears in `tabs-incomplete-aria-selected.json` — an adjacently-named but **different** tabs fixture, reporting "tabpanel at `#panel-1` has no accessible name." This component's panels *do* have accessible names, via `aria-labelledby={`tab-${tab.id}`}` at `TabsWidget.jsx:43`. Out of scope and factually inapplicable.
- `sr-live-region-silent-desktop` (5 files, WCAG 4.1.3): out of scope, and calibration rule 1 caps these at *prompts to run a driven session*, never failure evidence, even in their own components.
- `positive-tabindex-desktop`, `sr-heading-skip-desktop`, `no-skip-link-desktop`: out of scope. This component declares no positive tabindex, no headings, and is not a page.

**On the trace's `sr_announcement` field**: the digest correctly notes this is keyboard-a11y-tester's self-reported data, **not** the canonical `name-role-state` instrument (virtual-screen-reader assertions), which is absent from this set. Phase 0 admits keyboard-a11y-tester per-step trace facts (`keystroke`, `selector`, `focus_moved`) at Playwright tier, so I use those as hard evidence for focus behavior. The announcement *strings* I treat as corroborating only — **I make no claim in this review that any behavior was verified with a real screen reader.**

**Two scope caveats worth stating up front**:

1. **No axe-core artifact exists in this set.** The skill's stated precondition — "automated checks pass" — is therefore **unverified** for this component. I proceed (the defects below are not axe-detectable anyway) but the reader should not read this review as confirming a clean automated baseline.
2. **The measured evidence never exercised the failure that matters most.** The trace sent exactly four keystrokes: `Tab`, `ArrowRight`, `ArrowLeft`, `Tab`. **Enter and Space were never pressed.** CRITICAL-2 below — the most destructive defect in the component — sits entirely outside the measured evidence. A 33-file evidence pack was assembled and the one keypress that breaks the widget was not among them. That is the substantive finding about this evidence set: its volume is padding, and its coverage has a hole exactly where the component is weakest.

---

## Pre-commitment Predictions

Made before reading the source, from component type alone (custom tabs widget):

1. **Arrow key navigation (Left/Right) missing or incomplete**, and Home/End almost certainly absent — the most common APG Tabs gap.
2. **Roving tabindex absent or wrong**, leaving all tabs in the tab order (the usual failure) or the active one unmarked.
3. **`aria-selected` present but desynchronized** from visual state, or `aria-controls`/`aria-labelledby` not paired.
4. **Tabpanel not focusable** (`tabindex="0"` missing) when panels contain no focusable content.
5. **Activation model undefined** — automatic vs manual not chosen; focus behavior after activation unspecified.
6. **Panels hidden with CSS only** (a class toggling `display:none`) rather than the `hidden` attribute, leaving them in the AT tree.

Results are compared against these in the Synthesis section. Short version: two predictions confirmed, three refuted, and the worst defect in the component was not among them.

---

## Critical Findings (blocks access)

### CRITICAL-1 — Roving tabindex plus no arrow-key handler makes every inactive tab keyboard-unreachable

**Evidence (source, primary):**
- `TabsWidget.jsx:27` — `tabIndex={index === activeTab ? 0 : -1}`. Every tab except the active one is removed from the tab sequence.
- `TabsWidget.jsx:10-15` — `handleTabKeyDown` branches on `e.key === 'Enter' || e.key === ' '` **only**. There is no `ArrowRight`, `ArrowLeft`, `Home`, or `End` branch anywhere in the component.
- `TabsWidget.jsx:19` — the `role="tablist"` container carries no `onKeyDown` either, so there is no delegated handler to compensate.

**Evidence (measured, corroborating — digest-only, not re-fetched):**
`keyboard-a11y-tester` driven trace `tabs-missing-arrow-nav.trace.json`, handle `jq '.steps[]|{step_id,keystroke_sent,active_element_selector,focus_moved}'`:
```
{"step_id":"step_0002","keystroke":"ArrowRight","selector":"#tab-overview","focus_moved":false}
{"step_id":"step_0003","keystroke":"ArrowLeft", "selector":"#tab-overview","focus_moved":false}
```
Both arrow presses land on the focused tab and move nothing. `step_0001` and `step_0004` (both `Tab`) show `focus_moved:true`, so the harness was dispatching real key events that the page did receive — the arrows were delivered and ignored, not dropped.

**Why the two halves compound.** Roving tabindex is implemented *correctly*, and that is precisely what makes this fatal rather than merely non-conformant. In a tablist with no roving tabindex, a keyboard user can at least Tab through all tabs. Here, `Tab` reaches exactly one tab and then exits the widget (trace `step_0004`: `#tab-overview` → `body`). Arrow keys, the only remaining route to tabs 2..n, do nothing. **There is no keyboard path to any tab other than the currently active one.** The content behind those panels is mouse-only.

**User group impacted**: Keyboard-only users are blocked outright. Screen reader users have a partial workaround — NVDA/JAWS browse mode and VoiceOver's VO+arrow navigation can reach the other tab buttons through the virtual buffer — but activating one from there routes straight into CRITICAL-2 below, so the workaround terminates in a broken state. I am not claiming all AT users are equally blocked; keyboard-only users are.

**Standard**: WAI-ARIA APG **Tabs (Tabbed Interface) pattern**, Keyboard Interaction — for a horizontal tablist, `Right Arrow` moves focus to the next tab (wrapping to first), `Left Arrow` to the previous (wrapping to last), `Home` to the first tab, `End` to the last. WCAG **2.1.1 Keyboard** (all functionality operable through a keyboard interface). WCAG **2.4.3 Focus Order** secondarily.

**Confidence**: HIGH. Source-verifiable without measurement; measurement agrees.

**Fix**: Add an arrow-key branch and manage focus explicitly via refs. Sketch:

```jsx
const tabRefs = useRef([]);

const focusTab = (i) => {
  const next = (i + tabs.length) % tabs.length;   // wrap both directions
  setActiveTab(next);                              // automatic activation (see note)
  tabRefs.current[next]?.focus();
};

const handleTabKeyDown = (e, index) => {
  switch (e.key) {
    case 'ArrowRight': e.preventDefault(); focusTab(index + 1); break;
    case 'ArrowLeft':  e.preventDefault(); focusTab(index - 1); break;
    case 'Home':       e.preventDefault(); focusTab(0); break;
    case 'End':        e.preventDefault(); focusTab(tabs.length - 1); break;
    default: break;    // let native <button> handle Enter/Space — see CRITICAL-2
  }
};
```
Attach with `onKeyDown={(e) => handleTabKeyDown(e, index)}` and `ref={(el) => (tabRefs.current[index] = el)}`.

**Activation model — choose deliberately and document it.** The sketch above uses **automatic activation** (panel switches as focus moves), which the APG recommends when panels are cheap to render. These panels render a single `<p>` (`TabsWidget.jsx:47`), so automatic is the right call. If panels later become expensive or fetch data, switch to **manual activation**: move focus only on arrow, and select only on Enter/Space. Do not leave this implicit — an undocumented activation model is how the next contributor reintroduces CRITICAL-2.

**If the tablist ever becomes vertical**, add `aria-orientation="vertical"` to the container and swap to `ArrowUp`/`ArrowDown`. Currently horizontal (`TabsWidget.css:5-9`, `display: flex` default row), and `horizontal` is the default for `role="tablist"`, so no attribute is required today.

```
### A11y Evidence Finding
finding_id: tabs-arrowkeys-absent-roving-tabindex-strands-inactive-tabs
fingerprint: not-computed-in-this-pass (recompute over canonical string: "TabsWidget.jsx:10-15,27|apg-tabs-keyboard|wcag-2.1.1|arrow-nav-absent") — a hex value is deliberately not emitted here rather than fabricated, since no hash was actually computed in this pass
source: component source TabsWidget.jsx:10-15,27 (primary) + keyboard-a11y-tester driven trace tabs-missing-arrow-nav.trace.json steps 0002-0003 (corroborating, DIGEST-ONLY — not re-fetched at handle)
wcag_or_apg: WAI-ARIA APG Tabs pattern, Keyboard Interaction (Left/Right/Home/End); WCAG 2.2 SC 2.1.1 Keyboard (Level A)
section_508_fpc_context: In scope if the project declares Revised Section 508 — SC 2.1.1 is WCAG 2.0 Level A and maps to the 508 web conformance basis. Otherwise not in scope; this review's target is WCAG 2.2 AA.
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, keyboard-only=HIGH, low-vision=MEDIUM, cognitive=MEDIUM, vestibular=LOW, auditory=LOW, environmental-contrast=MEDIUM
evidence: TabsWidget.jsx:27 `tabIndex={index === activeTab ? 0 : -1}`; TabsWidget.jsx:11 `if (e.key === 'Enter' || e.key === ' ')` with no arrow branch; trace step_0002 ArrowRight focus_moved:false, step_0003 ArrowLeft focus_moved:false, step_0004 Tab #tab-overview -> body
reproduction_steps: 1) Render TabsWidget with 3+ tabs. 2) Press Tab until the active tab receives focus. 3) Press ArrowRight, then ArrowLeft. 4) Observe focus does not move. 5) Press Tab — focus leaves the widget entirely, having visited only one tab.
expected_behavior: ArrowRight moves focus to the next tab and wraps to the first; ArrowLeft moves to the previous and wraps to the last; Home/End jump to first/last. Tab enters the tablist once and exits to the panel.
actual_behavior: Arrow keys are inert. Only the active tab is reachable by keyboard; all other tabs and their panel content are mouse-only.
trend: new
```

---

### CRITICAL-2 — Enter or Space on any tab sets `activeTab` to `-1`, blanking all panels and removing every tab from the tab order

This defect was **not** exercised by the supplied evidence and is established purely from source. It is the more severe of the two.

**Evidence (source, primary):**
- `TabsWidget.jsx:23` — the rendered DOM id is `` id={`tab-${tab.id}`} `` → e.g. `tab-overview`.
- `TabsWidget.jsx:13` — the handler looks up `tabs.findIndex(t => t.id === e.currentTarget.id)`, comparing the **raw data id** (`overview`) against the **prefixed DOM id** (`tab-overview`).
- These never match. `findIndex` returns **`-1`**, which is passed straight into `handleTabClick` → `setActiveTab(-1)` (`TabsWidget.jsx:6-8`). There is no guard.
- `TabsWidget.jsx:12` — `e.preventDefault()` runs *before* the lookup, suppressing the button's synthesized `click`, so the correct `onClick={() => handleTabClick(index)}` at `TabsWidget.jsx:28` **never fires** to repair the value.

**Cascade once `activeTab === -1`** (all four consequences follow mechanically from the render):
1. `TabsWidget.jsx:44` — `hidden={index !== activeTab}` is true for every index → **every panel is hidden. The content area goes blank.**
2. `TabsWidget.jsx:27` — `tabIndex={index === activeTab ? 0 : -1}` yields `-1` for every tab → **no tab is in the tab order at all.** Once focus leaves the widget it can never return by keyboard.
3. `TabsWidget.jsx:25` — `aria-selected` is `false` on every tab. A `role="tablist"` with zero selected tabs is an invalid state under the APG Tabs pattern; a screen reader announces a tab list in which nothing is selected.
4. `TabsWidget.jsx:30` — the `.active` class is dropped from every tab, so the visual selected state disappears too.

**Recovery is mouse-only.** The buttons remain clickable, so a mouse user clicks a tab and everything snaps back — they will never reproduce this. A keyboard-only user has no route back into the widget short of a page reload or component remount. This is why the defect can survive review indefinitely.

**Browser precision.** For **Enter**, this is certain: a `<button>`'s activation is dispatched from `keydown`, and `preventDefault()` there cancels it. For **Space**, activation is dispatched from `keyup`, and preventing the `keydown` default cancels the activation sequence in Chromium and Gecko (this is exactly why the canonical custom-button recipe calls `preventDefault` on Space keydown). If some engine were to still fire the click, the result would be a race — keydown sets `-1`, click then sets the correct index — producing a visible flicker rather than a stable break. **The finding holds unconditionally for Enter.**

**Why axe-core would not catch this**, even had a scan been run: the invalid state exists only *after* a keypress. A static scan of the initial render sees a well-formed tablist with exactly one selected tab. This is precisely the class of defect this critic exists for.

**User group impacted**: Keyboard-only and screen reader users — both are locked out and lose all panel content. Cognitively, the failure is silent and unexplained: content vanishes with no message, no error, and no visible cause.

**Standard**: WCAG **2.1.1 Keyboard** (Level A) — keyboard activation must perform the same function as pointer activation, not destroy state. WCAG **4.1.2 Name, Role, Value** (Level A) — `aria-selected` must reflect the widget's actual state; a tablist with no selected tab does not. WAI-ARIA APG **Tabs pattern** — exactly one tab in a tablist has `aria-selected="true"`.

**Confidence**: HIGH for Enter, HIGH for Space in mainstream engines.

**Fix — delete the handler's activation branch entirely.** These are native `<button>` elements (`TabsWidget.jsx:21`). Enter and Space already activate them and already fire `onClick` with the correct closure index. The handler is not merely buggy, it is redundant: the correct behavior is what you get by writing nothing. Replace `handleTabKeyDown` with the arrow-key-only switch from CRITICAL-1, whose `default:` branch lets Enter and Space fall through to native activation.

If a lookup by element id is ever genuinely needed elsewhere, do not reconstruct it by string surgery — pass the index down (`onKeyDown={(e) => handleTabKeyDown(e, index)}`) as the fix above does, or read `e.currentTarget.dataset.index`. Deriving state from a formatted DOM id is the root cause here, and a `-1` guard would only mask it.

```
### A11y Evidence Finding
finding_id: tabs-keydown-id-mismatch-sets-active-index-negative-one
fingerprint: not-computed-in-this-pass (recompute over canonical string: "TabsWidget.jsx:13,23|apg-tabs-selection|wcag-2.1.1+4.1.2|findIndex-returns-negative-one") — deliberately not fabricated
source: component source TabsWidget.jsx:12-13 vs TabsWidget.jsx:23 (primary, code-read). NOT covered by any supplied measured evidence — the driven trace sent only Tab/ArrowRight/ArrowLeft/Tab.
wcag_or_apg: WCAG 2.2 SC 2.1.1 Keyboard (Level A) and SC 4.1.2 Name, Role, Value (Level A); WAI-ARIA APG Tabs pattern (exactly one tab aria-selected="true")
section_508_fpc_context: In scope if the project declares Revised Section 508 — both SCs are WCAG 2.0 Level A and map to the 508 web conformance basis. Otherwise not in scope.
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, keyboard-only=HIGH, low-vision=MEDIUM, cognitive=MEDIUM, vestibular=LOW, auditory=LOW, environmental-contrast=LOW
evidence: TabsWidget.jsx:23 `id={`tab-${tab.id}`}` renders "tab-overview"; TabsWidget.jsx:13 `tabs.findIndex(t => t.id === e.currentTarget.id)` compares against "overview" -> -1; TabsWidget.jsx:12 `e.preventDefault()` suppresses the synthesized click that would have called onClick with the correct index
reproduction_steps: 1) Render TabsWidget with 3 tabs whose ids are "overview","details","specs". 2) Press Tab to focus the active tab. 3) Press Enter (or Space). 4) Observe all three panels disappear, all tabs lose the active style, and no tab is announced as selected. 5) Press Shift+Tab then Tab — focus can no longer enter the tablist.
expected_behavior: Enter or Space on a focused tab selects that tab, reveals its panel, and leaves that tab as the single focus stop in the tablist.
actual_behavior: activeTab becomes -1. All panels hidden, aria-selected="false" on all tabs, tabIndex="-1" on all tabs, .active class removed everywhere. The widget is unrecoverable by keyboard; only a mouse click restores it.
trend: new
```

---

## Major Findings (significantly degrades experience)

**None.** This is a deliberate calibration, not an oversight. The two blocking defects are correctly CRITICAL, and everything else in this component genuinely resolves to MINOR or below. Manufacturing a MAJOR tier to make the review look balanced would be severity inflation — the failure mode this protocol names explicitly.

---

## Minor Findings (friction but workaround exists)

**MINOR-1 — Tab panel is not a focus stop, so keyboard users tab straight past the content**

`TabsWidget.jsx:39-46` renders each panel as a `div` with `role="tabpanel"` and no `tabIndex`. The panel content is a single `<p>` (`TabsWidget.jsx:47`) with nothing focusable inside it. Per the WAI-ARIA APG Tabs pattern, a tabpanel whose first content element is not focusable **should** carry `tabindex="0"` so the panel itself becomes the next stop after the tablist.

Measured corroboration (**digest-only, not re-fetched**): trace `step_0004` — `Tab` from `#tab-overview` moves focus to `body` with `focus_moved:true` and an empty states dict. The panel is confirmed not to be a focus stop. Caveat on generalization: `body` here reflects the fixture harness page having no further content; on a real page focus would land on whatever follows the widget. The source read is what carries this finding.

**Realist Check → held at MINOR.** *Mitigated by:* the panel content is visually present and immediately adjacent for sighted keyboard users, and it sits in the screen reader reading order correctly labeled by `aria-labelledby` (`TabsWidget.jsx:43`), so AT users reach it by browse-mode reading. The friction is real but bounded, and a workaround exists for both affected groups. WCAG 2.4.3 Focus Order is not violated; this is an APG recommendation.

**Fix**: add `tabIndex={index === activeTab ? 0 : undefined}` to the panel div. Apply it to the visible panel only — do not put `tabindex="0"` on hidden panels. (`hidden` already removes them from the focus order, so this is belt-and-braces, but scoping it keeps the intent legible.)

**MINOR-2 — DOM ids are not instance-namespaced; two widgets on one page collide**

`TabsWidget.jsx:23,26,41,43` construct ids as `` `tab-${tab.id}` `` and `` `panel-${tab.id}` `` from caller-supplied data with no per-instance prefix. If this reusable component renders twice on a page with overlapping `tab.id` values — a "Products" tab in a sidebar and in a main region, say — the document contains duplicate ids, and `aria-controls` / `aria-labelledby` resolve against the *first* match in document order. A screen reader user on the second widget would be told the tab controls a panel belonging to the first. WCAG **1.3.1 Info and Relationships**, **4.1.2 Name, Role, Value**.

**Needs user verification** — this is conditional on how the component is consumed, which the fixture does not show. Concrete check: render two `TabsWidget` instances on one page with any shared `tab.id`, then in DevTools run `$$('[id^="tab-"]').map(e => e.id)` and look for duplicates; confirm in the accessibility tree that each tab's "controls" target is the panel in its own widget.

**Fix**: derive a stable instance prefix with `useId()` (React 18+) and thread it through both id constructions and both reference attributes.

---

## Enhancements (best practice not met, no access barrier)

- **Forced-colors mode**: the selected tab is distinguished by `color`, `border-bottom-color`, and `font-weight: 600` (`TabsWidget.css:27-31`). In Windows High Contrast / `forced-colors: active`, the two color cues are overridden by system colors and may collapse. `font-weight: 600` survives, and `aria-selected` carries the state programmatically, so information is not lost — hence an enhancement, not a finding. Consider a `@media (forced-colors: active)` block adding a non-color cue (e.g. `border-bottom-width` change, or `forced-color-adjust` handling) to keep the selected tab visually obvious for sighted HCM users.
- **Hover color equals active color**: `.tab-button:hover { color: #0066cc }` (`TabsWidget.css:23-25`) is the same blue as `.tab-button.active` (`TabsWidget.css:28`). An inactive tab under the cursor partly mimics the selected tab. The border and weight still differentiate them, so this is polish, not a 1.4.1 issue.
- **Panel border contrast**: `.tab-panel { border: 1px solid #ddd }` (`TabsWidget.css:41`) is roughly 1.3:1 against white. I am explicitly **not** filing this as a 1.4.11 violation — a decorative grouping boundary is not "visual information required to identify a user interface component or state," and the panel's identity comes from the selected tab, not this border. Raised only so the design system team can decide deliberately.
- **`:focus` vs `:focus-visible`**: `TabsWidget.css:33` uses `:focus`, so the ring shows on mouse click too. This is defensible and arguably safer; noted only so the choice is intentional.
- **Panel content has no heading**: `<p>{tab.content}</p>` (`TabsWidget.jsx:47`) gives screen reader users no heading-navigation anchor into panel content. Acceptable for short panels since `aria-labelledby` names the panel; worth revisiting if panels grow.
- **`aria-label="Content tabs"`** (`TabsWidget.jsx:19`) produces a mildly redundant announcement ("Content tabs, tab list"). Functional as-is; if the widget is ever given a visible heading, prefer `aria-labelledby` pointing at it. Deliberately not filed as a finding — "the label could be more descriptive" is preference, not a gap.

---

## What's Missing (gaps and unstated assumptions)

- **The entire arrow-key handler.** Not partially implemented — absent. See CRITICAL-1.
- **`Home` and `End`.** Absent. Folded into CRITICAL-1's fix rather than filed separately; on their own, with arrows working, they would be MINOR.
- **A documented activation model.** Automatic vs manual activation is not chosen anywhere in code or comment. This gap is what allowed the broken keydown handler to be written in the first place.
- **`tabindex="0"` on the visible panel.** See MINOR-1.
- **Instance-scoped id generation.** See MINOR-2.
- **Any test that presses Enter or Space.** The 33-artifact evidence pack contains no such measurement, and CRITICAL-2 is invisible without it. Prescribed test, in the project's own Playwright suite (real key events, not synthetic): focus the active tab, `page.keyboard.press('Enter')`, then assert `await page.locator('[role="tab"][aria-selected="true"]').count()` **is exactly 1** and `await page.locator('[role="tabpanel"]:not([hidden])').count()` **is exactly 1**. Repeat with `'Space'`. Both currently fail.
- **Any axe-core baseline for this component.** The critic's stated precondition is unverified. Not blocking — neither CRITICAL is axe-detectable — but it should be stated rather than assumed.
- **Component-level screen-reader assertions.** No `virtual-screen-reader` output exists in this set. After the fixes land, that is the right lane for asserting the announcement on arrow-key movement (does moving focus to tab 2 announce "tab, Details, selected, 2 of 3"?). The keyboard-a11y-tester trace's announcement strings are not a substitute for that instrument.

**Checks I ran that did *not* produce a finding** (recorded so the absence is legible, not assumed):
- `aria-hidden` used to hide content while leaving it focusable → **not present**; the component uses the `hidden` attribute (`TabsWidget.jsx:44`), which removes panels from both the AT tree and the focus order. No `inert` needed.
- Visual text symbols (`+`/`−`/`×`) needing `aria-hidden` → **none present**.
- CSS `::before`/`::after` content leaking into the AT tree → **none declared**.
- `visibility:hidden` on focus-reveal elements → **not present**.
- `title` used as the sole accessible name → **not present**; names come from button text (`TabsWidget.jsx:32`).
- `role="alert"` / `aria-live` inside a loop (broadcast-vs-association anti-pattern) → **not present**.
- Positive `tabindex` values → **none**; the only values are `0` and `-1`.
- `prefers-reduced-motion` → the sole transition is `color 0.2s` (`TabsWidget.css:20`), a non-motion property. Not a vestibular trigger. Deliberately not filed.
- Target size (WCAG 2.5.8) → `padding: 12px 20px` at `font-size: 16px` (`TabsWidget.css:12,16`) yields roughly 46px tall and well over 24px wide. Passes comfortably.

---

## What Is Correct (explicit acknowledgment)

Calibration requires saying this plainly, because most of this component is right and a review that implied otherwise would be untrustworthy:

- **Native HTML first is honored.** Tabs are real `<button>` elements (`TabsWidget.jsx:21`), not divs with `role="button"`. ARIA here *enhances* native semantics rather than replacing them — the correct relationship. `role="tablist"`/`role="tabpanel"` on divs is the only way to build this pattern; there is no native equivalent being bypassed.
- **The full ARIA relationship graph is wired and paired.** `aria-controls` (`:26`) → panel id (`:41`); `aria-labelledby` (`:43`) → tab id (`:23`). Both directions resolve.
- **`aria-selected` is synchronized to state**, not stale (`:25`). Note for reviewers who might flag a false positive here: React renders `aria-*` boolean props as strings, so `aria-selected={false}` emits `aria-selected="false"` — the attribute is present on inactive tabs, not dropped.
- **Roving tabindex is implemented correctly** (`:27`) — `0` on the active tab, `-1` on the rest. The pattern half that is right; it is the missing arrow keys, not this, that break it.
- **`hidden` is used for panel visibility** (`:44`), with `.tab-panel[hidden] { display: none !important }` (`TabsWidget.css:50-52`) guarding against the `.tab-panel.active` rule overriding it. That defensive `!important` is deliberate and correct.
- **The accessibility tree computes as intended.** Trace `step_0001` (**digest-only, not re-fetched**): `"tab, Overview, selected, 1 control, position 1, set size 3"`. Role, name, selected state, the `aria-controls` relationship, and position-in-set all resolve — and `posinset`/`setsize` come free from the correct `tablist` → `tab` structure, so no `aria-posinset` is needed.
- **The focus indicator is strong.** `outline: 3px solid #0066cc; outline-offset: 2px` (`TabsWidget.css:33-36`) — #0066cc computes to **5.56:1** against white, clearing 3:1 for 2.4.11 and meeting the 2px-perimeter/3:1 bar of 2.4.13 (AAA).
- **Text contrast passes.** `#666` on white ≈ **5.74:1** and `#0066cc` on white ≈ **5.56:1** (`TabsWidget.css:15,28`), both above 4.5:1 for 16px text.
- **Selected state is not color-alone.** `border-bottom-color` and `font-weight: 600` accompany the color change (`TabsWidget.css:27-31`). WCAG 1.4.1 satisfied.

*Contrast caveat*: these ratios are computed from the declared hex values against an **assumed white page background**. No background is declared on `.tabs-container` or `.tab-button` (`background: transparent`, `TabsWidget.css:14`). If this widget is placed on a tinted surface, re-verify. No measured contrast evidence exists in this set — no axe `color-contrast` results were supplied — so these are calculations, not measurements, and are labeled as such.

---

## Multi-Perspective Notes

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | **HIGH** | Custom composite widget; keyboard activation drives the tablist into a zero-selected-tab state (CRITICAL-2), invalidating the announced model mid-session |
| Keyboard-only | **HIGH** | Roving tabindex with no arrow-key handler strands n−1 tabs (CRITICAL-1); one keypress removes the widget from the tab order entirely (CRITICAL-2) |
| Low vision | **MEDIUM** | Contrast and focus indicator verified from source and pass, but the page background is undeclared so ratios are assumptions; selected-state cues are partly color-based |
| Cognitive | **MEDIUM** | Content disappears with no message, no error, and no recoverable cause after a single keypress; the interaction model is inconsistent between mouse and keyboard |
| Vestibular & motion | **LOW** | One `color 0.2s` transition; no motion, parallax, autoplay, or flashing |
| Auditory access | **LOW** | No media elements, no audio, no sound-based alerts |
| Environmental contrast | **MEDIUM** | Selected state leans on two color cues in forced-colors mode; `font-weight` survives, so information is degraded rather than lost |

**Screen reader user**: The initial announcement is genuinely good — `"tab, Overview, selected, 1 control, position 1, set size 3"` tells the user the role, name, state, relationship, and position. The problem is what happens next. Reaching tab 2 requires browse-mode virtual navigation (Tab will not get there), and activating it from browse mode fires Enter → CRITICAL-2 → a tablist where nothing is selected and every panel is gone. The user is left in a widget that announces three tabs, reports none selected, and exposes no content. No live region communicates that anything changed; there is no `aria-live` anywhere in the component, and correctly so — a tabs widget does not need one, because the panel/tab state changes *are* the announcement mechanism. That is exactly why breaking those states is so damaging.

**Keyboard-only user**: Tab reaches exactly one tab. Arrow keys do nothing (measured: trace steps 0002–0003, digest-only). Tab again exits the widget without stopping in the panel (MINOR-1). Press Enter at any point and the widget goes blank and becomes permanently unreachable. There is no keyboard trap in the 2.1.2 sense — focus can always leave — but the inverse failure is arguably worse: focus can never come back. Focus indication itself is excellent when focus is somewhere to be had.

**Low vision user (200% zoom, high contrast, magnifier)**: Text and focus contrast pass by calculation. Target sizes clear 2.5.8 comfortably. `display: flex` with `gap: 4px` and no fixed widths (`TabsWidget.css:5-9`) reflows without horizontal scroll, though with many tabs the row will overflow rather than wrap — worth checking at 320px-equivalent, since no `flex-wrap` is set. Under magnification, the roving-tabindex problem compounds: a magnifier user relies on focus to drive the viewport, and with only one focusable tab, the viewport never travels to the others.

**Cognitive accessibility**: The mouse experience is clean, calm, and conventional. The keyboard experience is arbitrary — press a key that in every other tabs widget on the web selects a tab, and instead all content vanishes with no explanation, no error message, and no undo. Nothing tells the user what happened or how to recover. The mouse/keyboard inconsistency itself is the cognitive load: two input methods, two entirely different mental models.

**Escalation**: Screen reader and keyboard-only are both **HIGH**. Per protocol, both should go to `/perspective-audit` for deep review — though the sensible sequence is to fix both CRITICALs first, since a perspective audit of a widget that self-destructs on Enter will spend its budget re-deriving the same two defects.

---

## Realist Check (Phase 8) — Severity Calibration

**CRITICAL-1** — Realistic worst case: keyboard-only users can never reach any tab but the first-rendered active one; that content is mouse-only. Group: keyboard-only (total block), screen reader (degraded, partial browse-mode workaround that leads into CRITICAL-2). Detection if shipped: **never**, absent a keyboard test — arrow keys silently do nothing, which looks identical to "no arrow keys implemented yet." Proportional? Yes. This is complete access loss for a user category. **Held at CRITICAL — no downgrade permitted by rule.**

**CRITICAL-2** — Realistic worst case: any keyboard or AT user who presses Enter (the single most reflexive activation key) loses all widget content and all keyboard access to it for the rest of the page session. Group: keyboard-only and screen reader — total. Detection if shipped: **never** by mouse-based QA, and it was in fact not detected by the 33-artifact evidence pack assembled for this component. Proportional? Yes, and if anything the pairing with CRITICAL-1 makes it worse: the *only* tab a keyboard user can reach is the active one, and pressing Enter on the tab you are already on — a no-op in every correct tabs widget — is what destroys the component. **Held at CRITICAL.**

**MINOR-1 (panel not focusable)** — Initially considered at MAJOR. **Downgraded to MINOR.** *Mitigated by:* the panel content is visible and adjacent for sighted keyboard users and is correctly placed and labeled in the screen reader reading order via `aria-labelledby`, so both affected groups retain a working route to the content. APG states this as a recommendation, not a requirement, and no WCAG SC is failed.

**MINOR-2 (id collision)** — Held at MINOR and marked *Needs user verification*, because it is conditional on consumption patterns not visible in the fixture. It would rise to MAJOR on confirmation of two same-page instances with overlapping tab ids.

**Enhancement candidates deliberately not promoted**: hover/active color similarity, `#ddd` panel border, `aria-label` phrasing, `:focus` vs `:focus-visible`. Each is real and each is preference or polish. Promoting them would inflate the review and dilute the two findings that actually matter.

---

## Self-Audit (Phase 9)

| Finding | Confidence | Refutable by developer context? | Gap or preference? |
|---|---|---|---|
| CRITICAL-1 | HIGH | No — source shows no arrow branch; trace independently shows no focus movement | GAP |
| CRITICAL-2 | HIGH (Enter certain; Space certain in Chromium/Gecko) | No — the id mismatch is arithmetically unambiguous. The only context that would soften it is a caller passing `tab.id` values already prefixed with `tab-`, and even then the rendered id becomes `tab-tab-overview` and the mismatch persists | GAP |
| MINOR-1 | HIGH | Partially — if real panel content contains focusable elements, the recommendation does not apply. Stated in the finding | GAP (conditional) |
| MINOR-2 | MEDIUM | Yes — depends on consumption. Marked *Needs user verification* with a concrete DevTools check rather than suppressed | GAP (conditional) |

Nothing was moved to Open Questions for low confidence. Two items are carried in Open Questions below as genuine unknowns requiring information the fixture does not contain.

I want to name one weakness in my own review: **CRITICAL-2 rests entirely on a code read.** No supplied evidence exercised Enter or Space, and I could not re-fetch the trace to confirm the harness never pressed them beyond what the digest reports. The finding is a mechanical consequence of two lines I can read directly, so my confidence is high — but it is reasoning, not measurement, and the prescribed Playwright assertion in *What's Missing* exists precisely to convert it. If a developer runs that test and it passes, I am wrong and want to know.

---

## Synthesis (Phase 10) — Predictions vs Findings

| # | Prediction | Outcome |
|---|---|---|
| 1 | Arrow keys / Home / End missing | **Confirmed** — CRITICAL-1 |
| 2 | Roving tabindex absent or wrong | **Refuted, and inverted.** Roving tabindex is implemented *correctly*, which is what escalates prediction 1 from MAJOR to CRITICAL. I predicted the wrong failure shape: I expected the usual "all tabs in the tab order, no arrows" (annoying but survivable) and found "one tab in the tab order, no arrows" (a total block) |
| 3 | `aria-selected` desynchronized or relationships unpaired | **Refuted.** Fully synchronized and paired; the trace's computed announcement confirms it |
| 4 | Tabpanel not focusable | **Confirmed** — MINOR-1, though calibrated lower than I expected once impact was checked |
| 5 | Activation model undefined | **Confirmed and then some.** Not merely undefined — the keyboard activation path is actively destructive |
| 6 | Panels hidden by CSS class only | **Refuted.** The `hidden` attribute is used correctly, with a deliberate `!important` guard |

**The surprise, stated plainly**: I predicted *missing* keyboard support. What I found was *present-but-destructive* keyboard support. CRITICAL-2 was in none of my six predictions, and it is the more severe of the two defects. The mental model I brought — "tabs widgets are usually 80% of the APG pattern with the arrow keys missing" — is a reasonable prior and it correctly caught CRITICAL-1, but it primed me to look for absence and would have primed me to stop after finding it. Reading the one handler that *does* exist, line by line, is what surfaced the worse bug.

**The second observation is about the evidence, not the component.** This pack contains 33 artifacts. Exactly one of them describes this component. The other 32 describe 32 different components and contribute nothing but the temptation to transplant their findings — a temptation with at least one well-baited hook (`missing-accessible-name-desktop` sitting inside a file named `tabs-incomplete-aria-selected.json`, a row that is not only out of scope but factually false for this component, whose panels *are* named). Meanwhile the single in-scope artifact ran four keystrokes and skipped the two that matter most. Volume of evidence and coverage of evidence moved in opposite directions here. The right response to a large evidence set is not more confidence; it is a scope ruling first, and a coverage check second.

---

## Verdict Justification

**REVISE.** This must not ship. Two CRITICAL defects each independently block keyboard access to the widget, and together they produce a component where the only reachable tab is the active one and pressing Enter on it destroys the whole thing.

**Why not REJECT**: the accessibility *design* is sound. Roles, relationships, states, roving tabindex, panel hiding, focus styling, and contrast are all correct — the trace confirms the accessibility tree computes exactly as the pattern intends. What is wrong is a missing interaction handler and one line with an identifier mismatch. Both fixes are contained, well-specified by the APG, and touch roughly fifteen lines. That is revision, not restart. Rejecting would misdescribe the state of the work and waste the substantial part that is right.

**Why not ACCEPT-WITH-RESERVATIONS**: two findings at CRITICAL, both complete access loss for a user category, neither eligible for downgrade under the recalibration rules.

**Path to ACCEPT**:
1. Fix CRITICAL-2 by deleting the Enter/Space branch — native `<button>` already does it correctly. (Smallest change, largest severity reduction. Do it first.)
2. Fix CRITICAL-1 by adding the `ArrowLeft`/`ArrowRight`/`Home`/`End` handler with ref-based focus movement and wrapping, and record the activation model choice (automatic is right for these panels) in a comment.
3. Fix MINOR-1 by adding `tabIndex={0}` to the visible panel.
4. Resolve MINOR-2 with `useId()` namespacing, or confirm in writing that single-instance usage is guaranteed.
5. Add the Enter/Space Playwright assertions from *What's Missing*, plus arrow-key focus assertions, so neither CRITICAL can silently return.
6. Run an axe-core scan to establish the automated baseline this review could not verify — not because it would have caught either defect, but because the precondition should be a fact rather than an assumption.

**Recalibrations reported**: MINOR-1 downgraded from MAJOR with an explicit mitigation. No CRITICAL downgraded. No MAJOR tier manufactured. Zero findings imported from the 32 out-of-scope findings files.

**Escalation**: Screen reader and keyboard-only perspectives are both HIGH and warrant `/perspective-audit`, best scheduled after steps 1–2 above.

---

## Open Questions (unscored)

1. **Page background color.** All contrast ratios in this review are calculated against assumed white; no background is declared on the container or buttons, and no measured contrast evidence exists in the supplied set. If this widget sits on a tinted or dark surface, `#666` at 5.74:1 and `#0066cc` at 5.56:1 both need re-verification. Concrete check: run axe-core's `color-contrast` rule against the widget in its real page context and use the measured ratio.
2. **Multi-instance usage.** Does any page render more than one `TabsWidget` with overlapping `tab.id` values? Determines whether MINOR-2 stays MINOR or becomes MAJOR.
3. **Panel content shape.** `<p>{tab.content}</p>` (`TabsWidget.jsx:47`) assumes `content` is a string. If callers pass JSX containing block-level elements, the browser will restructure the invalid `<p>` nesting, which can move content out from under the `role="tabpanel"` element and break the `aria-labelledby` association at runtime. Not filed as a finding — the fixture gives no evidence of rich content — but worth confirming, and worth a DOM inspection rather than a snapshot test if rich content is in scope.
4. **Tab overflow at narrow widths.** `display: flex` with no `flex-wrap` (`TabsWidget.css:5-9`). With enough tabs at 320px, does the row overflow horizontally? WCAG 1.4.10 Reflow. Not measurable from the source alone.
5. **Space-key behavior in WebKit.** CRITICAL-2 is certain for Enter in all engines and for Space in Chromium and Gecko. Safari's handling of `preventDefault` on Space keydown for buttons should be confirmed directly. This changes nothing about the fix — the handler should be deleted regardless — but it affects how the reproduction is written for a bug report.
6. **Evidence-set coherence.** The digest leaves unresolved whether an evidence set combining one component's trace with 32 unrelated components' findings is coherently "the component these artifacts describe." I have treated it as incoherent and ruled the 32 out of scope. If the pack was intended to supply page-level context for a page containing all 33 components, that intent was not visible in anything I was given, and the ruling should be revisited with that context supplied.
