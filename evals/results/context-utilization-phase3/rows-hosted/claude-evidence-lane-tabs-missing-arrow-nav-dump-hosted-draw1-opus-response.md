# Accessibility Design Review — `TabsWidget`

**VERDICT: REVISE**

**Overall Assessment**: The ARIA architecture of this tabs widget is genuinely good — native `<button>` elements, correct `role`/`aria-selected`/`aria-controls`/`aria-labelledby` wiring, and roving `tabindex` values that are set correctly. The driven trace confirms the accessibility tree computes exactly as intended ("tab, Overview, selected, 1 control, position 1, set size 3"). But two blocking holes sit inside that correct scaffolding: there is no arrow-key handler, so the roving tabindex it *does* implement makes tabs 2 and 3 unreachable by keyboard entirely (measured), and the Enter/Space handler contains an identifier mismatch that sets `activeTab` to `-1`, deselecting every tab, hiding every panel, and removing the whole widget from the tab sequence. Neither is an architectural error — both are localized, additive fixes — which is why this is REVISE and not REJECT.

---

## Phase 0 — Evidence Consumption and Scoping

**Review type**: fresh design pass, not a remediation. The a11y-test *Verification evidence contract* type-match check (which applies when reviewing a fix) is therefore not triggered — no "before/after under the same conditions" claim is being made here.

**Evidence pack inventory** — 33 artifacts were supplied. Exactly **one** is about the component under review:

| Artifact | URL / target | In scope? |
|---|---|---|
| `evals/results/keyboard-a11y-tester/driven/tabs-missing-arrow-nav.trace.json` | `http://127.0.0.1:8777/tabs-missing-arrow-nav.html` | **YES** — driven-live session, personas `keyboard` + `screen-reader`, goal "navigate between tabs using arrow keys" |
| 32 × `evals/results/keyboard-a11y-tester/findings/*.json` | 32 *different* URLs (`accordion-no-region-role.html`, `app-focus-order-illogical.html`, `tabs-incomplete-aria-selected.html`, …) | **NO** — different pages, different DOM, different selectors |

**Scoping ruling (load-bearing):** the 32 batch-crawl findings files are sibling-page artifacts. Not one of them names `tabs-missing-arrow-nav.html`. Importing any of them into this review would be fabrication, and the most tempting one is the most dangerous: `tabs-incomplete-aria-selected.json` reports `missing-accessible-name-desktop` on "tabpanel at `#panel-1`" — a different tabs fixture with different ids. This component's panels are `#panel-overview` etc. and *do* carry `aria-labelledby`, so that finding is affirmatively false here. **No finding in this review is derived from a sibling-page artifact.**

Two further calibration rules applied to the out-of-scope set, so that anyone reusing it downstream is warned rather than misled:
- The recurring `sr-live-region-silent-desktop` (4.1.3) rows in the sibling files are batch-crawl findings. Per calibration rule (1) these are prompts to run a driven session, never failure evidence.
- The `conformance_level` field in those files is a pass/fail gate, not the SC's WCAG level (upstream issue #27). Rows labelled `"conformance_level": "AA"` for 1.3.1, 2.4.1, 2.4.3, and 4.1.2 are mislabelling Level **A** criteria. Derive the level from the SC number.

**Absence note**: the pack contains no batch-crawl findings file for `tabs-missing-arrow-nav.html`. I cannot tell from the pack alone whether the crawler produced an empty result or the curator omitted the file. What I *can* say is that the only measured evidence for this component is the driven trace — and the defect it captures (roving tabindex with no arrow mechanism) is not in the deterministic scanner's rule set anywhere in these 32 files. This is precisely the class of gap that requires a goal-driven session or a design review.

**Hard facts extracted from the in-scope trace** (`tabs-missing-arrow-nav.trace.json`, `mode: "driven-live"`):

| Step | Keystroke | Active element | `focus_moved` | SR output |
|---|---|---|---|---|
| `step_0001` | `Tab` | `#tab-overview` (tabindex 0) | `true` | `"tab, Overview, selected, 1 control, position 1, set size 3"` |
| `step_0002` | `ArrowRight` | `#tab-overview` (unchanged) | **`false`** | `new_phrases: []`, `focus_announcement: null` |
| `step_0003` | `ArrowLeft` | `#tab-overview` (unchanged) | **`false`** | `new_phrases: []`, `focus_announcement: null` |
| `step_0004` | `Tab` | `body` (`role: "none"`, `is_body: true`) | `true` | `new_phrases: []` |

Also measured: focus style `outline: 3px solid rgb(0,102,204)`, `outline-offset: 2px`, `focus_visible.visible: true`; bounding box `111.16 × 45` px; `states.controls: "panel-overview"`; `region: { landmark: null, heading: null }` at every step; `live_announcements: []` at every step.

---

## Phase 1 — Pre-commitment Predictions

Written before reading the source, based on component type (tabs widget):

1. **Arrow Left/Right navigation missing** — the single most common tabs defect.
2. **Roving tabindex missing entirely**, forcing every tab into the Tab sequence.
3. **`aria-selected` not synchronized with state**, or `aria-controls` absent / pointing at a non-existent id.
4. **Panel not reachable after activation** — no `tabindex="0"` on the tabpanel, focus goes nowhere.
5. **Focus indicator suppressed** by `outline: none` on the tab buttons.
6. **Home/End missing.**

Comparison against actuals is in Phase 10.

---

## Phase 2 — Semantic HTML Audit

**Correct, and worth stating plainly:**

- Tabs are native `<button>` elements (line 28), not `div role="button"`. The native-HTML-first rule is satisfied — Enter/Space activation, focusability, and the `button` role all come for free. This is the decision most tabs implementations get wrong, and it is right here.
- `role="tab"` on a `<button>` is a legitimate role *override*, not ARIA papering over bad markup: the APG Tabs pattern requires it, and the underlying element is still a real button.
- `role="tablist"` container (line 26) is a `<div>`, which is correct — there is no native tablist element.
- The panels' accessible names come from `aria-labelledby` pointing at the tab (line 50), which is the APG-prescribed relationship, not a workaround.

**Not applicable at this scope** — landmark structure and heading hierarchy. The trace records `region: { landmark: null, heading: null }` at every step, but that describes the *harness page*, not the component. A tabs widget is not responsible for providing `<main>` or an `<h1>`. Flagging that here would be page-shell over-flagging. Noted, not filed.

**One real semantic finding** — the hardcoded `<p>` wrapper at line 54. See Minor Finding N3.

---

## Phase 3 — ARIA Pattern Compliance Audit

Pattern: **WAI-ARIA APG — Tabs (Tabs with Manual/Automatic Activation)**.

| APG requirement | Present? | Evidence |
|---|---|---|
| `role="tablist"` on container | ✅ | line 26 |
| Accessible name on tablist | ✅ (but see N2) | `aria-label="Content tabs"`, line 26 |
| `role="tab"` on each tab | ✅ | line 31 |
| Exactly one tab with `aria-selected="true"` | ✅ *in the happy path* | line 32; trace `states.selected: true` |
| `aria-controls` on tab → panel id | ✅ | line 33 → line 49 (`panel-${tab.id}`); trace `states.controls: "panel-overview"` |
| `role="tabpanel"` on each panel | ✅ | line 48 |
| `aria-labelledby` on panel → tab id | ✅ | line 50 → line 30 |
| Roving tabindex **values** | ✅ | line 34 (`0` on active, `-1` on others) |
| Roving tabindex **mechanism** (arrow keys move the roving point and call `.focus()`) | ❌ | **absent** — see C1 |
| `Home` / `End` | ❌ | absent — see E1 |
| Tabpanel in the tab sequence | ❌ | see M1 |
| `aria-orientation` | n/a | tablist is `display: flex` (row) = horizontal = the default; declaring it would be redundant, not required |

ARIA *values* are all valid: `aria-selected` receives a JSX boolean, which React stringifies to `"true"`/`"false"` on `aria-*` attributes (confirmed by the trace's computed `selected: true`), and the `hidden` prop renders as the boolean attribute. No `aria-current` misuse, no `"yes"`/`"no"` values.

**This is a pattern that is roughly 75% complete.** The DOM-visible portion is right; the behavioural portion that makes the DOM-visible portion *usable* is missing. That is the exact failure profile this review exists to catch — `axe-core` will report zero violations on this markup.

---

## Phase 4 — Focus Management Review

- **Tab order into the widget**: correct. `Tab` lands on the selected tab (`step_0001`), which is the APG behaviour.
- **Movement within the tablist**: **broken**. `ArrowRight` (`step_0002`) and `ArrowLeft` (`step_0003`) both report `focus_moved: false` with the active element unchanged at `#tab-overview`. The `handleTabKeyDown` handler (lines 17–22) matches only `Enter` and `' '`; every other key falls through with no action. See C1.
- **Tab order out of the widget**: `step_0004` shows `Tab` from `#tab-overview` moving to `body`, skipping `#panel-overview`. The tabpanel has neither `tabindex="0"` nor focusable content. See M1.
- **Focus visibility**: strong and measured. `.tab-button:focus { outline: 3px solid #0066cc; outline-offset: 2px; }` (CSS lines 100–103), and the trace records `has_outline: true`, `focus_visible.visible: true`, `indicator: "outline"`. WCAG 2.4.7 satisfied. Using `:focus` rather than `:focus-visible` shows the ring on mouse click too — more conservative than required, not a defect.
- **Focus after activation**: on click, focus stays on the clicked tab and the roving point follows state. Coherent. On *keyboard* activation, see C2 — the roving point is destroyed.
- **Focus restoration / traps**: not applicable (no modal, no overlay). No keyboard trap: `Tab` always escapes (`step_0004`). WCAG 2.1.2 satisfied.
- **Framework unmount timing / deferred focus**: not applicable — no async operations, no unmount path.
- **Duplicate-instance ID collision**: the ids are derived from `tab.id` with no instance scoping. See N1.

---

## Phase 5 — State Communication Audit

- **Selected state**: communicated programmatically via `aria-selected` (line 32) *and* visually via colour + font-weight + a 3px bottom border (CSS lines 94–98). Colour is not the sole indicator. WCAG 1.4.1 satisfied.
- **Hidden panels**: the `hidden` attribute (line 51) removes inactive panels from the accessibility tree *and* the tab order — the correct mechanism. The CSS guard `.tab-panel[hidden] { display: none !important; }` (CSS lines 117–119) is a deliberate, correct defence: it prevents a future `display: flex` on `.tab-panel.active` from silently defeating `hidden`. Credit where due — this is the bug most component libraries ship.
- **Panel change announcement**: **not a finding.** `live_announcements: []` at every trace step is expected and correct. The APG Tabs pattern conveys panel changes through `aria-selected` and focus position, not a live region. Adding `aria-live` here would create the Broadcast-vs-Association anti-pattern. I am explicitly declining to file a 4.1.3 finding.
- **Loading / error / disabled states**: none exist in this component. No `aria-busy`, `aria-disabled`, or error plumbing is missing, because there is nothing to plumb.
- **Visual text symbols as state indicators**: none. No `+`/`−`/`×` glyphs, no `::before`/`::after` content, no icon fonts. Nothing needs `aria-hidden`.
- **Silence on arrow keys**: `step_0002` and `step_0003` record `new_phrases: []` and `focus_announcement: null`. A screen-reader user pressing an arrow key gets *total silence* — no feedback that the key was ignored, no feedback that they are still on tab 1 of 3. This is state communication failing by omission, and it is part of C1's user impact.

---

## Phase 6 — Multi-Perspective Review

**Screen reader user (NVDA, JAWS, VoiceOver)** — the announcement measured at `step_0001` is a model announcement: `"tab, Overview, selected, 1 control, position 1, set size 3"`. Role, name, selected state, controls relationship, and set position all compute. The user is told there are 3 tabs. Then they press an arrow key and hear nothing (`step_0002`, `step_0003`), because nothing happened. Windows screen readers in browse mode can still reach tabs 2 and 3 through the virtual buffer, so this perspective is *less* completely blocked than pure keyboard — but activating from there runs into C2. In focus/forms mode, where the pattern's arrow keys are the expected interaction, the user is as stuck as anyone else. Being told "set size 3" and then being unable to reach items 2 and 3 is worse than not being told.

**Keyboard-only user** — the most damaged perspective. Reachable content: tab 1 and its panel. Unreachable content: tabs 2 and 3, and their panels. There is no keyboard path to two-thirds of the widget's content. If they try the natural recovery move — pressing Enter or Space on the focused tab — C2 fires and the remaining third disappears too.

**Low vision user (200% zoom, high contrast, magnifier)** — focus indicator measured at 3px solid with 2px offset and confirmed visible; target size measured at 111.16 × 45 px, comfortably past the 24×24 minimum (WCAG 2.5.8) and past the 44×44 recommendation. Text contrast: `#666` inactive and `#0066cc` active compute to ≈5.74:1 and ≈5.57:1 *against white* — and the trace's independently measured indicator contrast of 5.56:1 for the same `#0066cc` corroborates a white or near-white background. But the component's own CSS never declares a background (`background: transparent`, CSS line 82), so this is inference, not verification. See Open Question Q1. Reflow at 200% is unverified — see Q2.

**Cognitive accessibility** — the widget looks like tabs, which sets an expectation that arrow keys work; they don't, with no signal explaining why. Worse, C2 produces a silent catastrophic state change: press Enter, all content vanishes, nothing announces it, nothing explains it, and there is no undo or recovery short of reloading the page. Unexplained irreversible state loss is a cognitive accessibility problem, not only a functional one.

**Vestibular & motion sensitivity** — LOW, genuinely. The only transition is `transition: color 0.2s` (CSS line 87). A colour cross-fade is not motion; it is not a vestibular trigger, and adding a `prefers-reduced-motion` guard for it would be manufactured. No parallax, no autoplay, no flashing.

**Auditory access** — LOW. No `<video>`, no `<audio>`, no sound-based alerts.

**Environmental contrast / forced colors** — I investigated whether the active-tab indication survives Windows High Contrast and it **does**. In forced-colors mode `border-color` is forced to the system palette, but `transparent` is preserved — so the inactive tabs keep their `border-bottom: 3px solid transparent` (CSS line 85) while the active tab keeps a visibly coloured 3px border (CSS line 96). The active state remains distinguishable by border presence *and* by `font-weight: 600`, and `aria-selected` conveys it programmatically regardless. Using `transparent` rather than `none` for the inactive border was the right call — it also prevents layout shift on activation. No finding.

### Perspective Alarm Levels

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | **HIGH** | Composite widget; "set size 3" announced but 2 of 3 items unreachable in focus mode; arrow keys produce measured silence |
| Keyboard-only | **HIGH** | Roving tabindex with no arrow mechanism (measured `focus_moved: false` ×2); Enter/Space destroys the tab sequence |
| Low vision | **MEDIUM** | Indicator and target size measured as passing; page background undeclared so contrast math is inferred; reflow unverified |
| Cognitive | **MEDIUM** | Affordance promises behaviour it doesn't deliver; silent, unexplained, unrecoverable state loss on Enter/Space |
| Vestibular & motion | **LOW** | Colour-only 0.2s transition; no motion, autoplay, or flashing |
| Auditory access | **LOW** | No media elements of any kind |
| Environmental contrast | **MEDIUM** | Background never declared in component CSS; forced-colors behaviour verified sound |

**Escalation**: Screen reader and Keyboard-only are HIGH; Low vision, Cognitive, and Environmental contrast are MEDIUM. All five qualify for deep review via `/perspective-audit`. The two HIGH perspectives are driven by C1 and C2 and will drop once those are fixed; the MEDIUM ones need the page-level context this component-scope review does not have.

---

## Phase 7 — Gap Analysis (What Is Absent)

1. **Arrow Left/Right key handlers** — absent. → C1
2. **A `.focus()` call to move DOM focus when the roving point moves** — absent. Setting `tabIndex` alone never moves focus; the roving tabindex is decorative without it. → C1
3. **`Home` / `End` handlers** — absent. → E1
4. **`tabindex="0"` on the tabpanel** — absent, and the panel contains no focusable element, so nothing occupies the panel's slot in the tab sequence. → M1
5. **Any guard against `activeTab` going out of range** — absent. `setActiveTab(-1)` is reachable and unhandled. → C2
6. **Instance-scoped ids** (`useId` or a prefix prop) — absent. → N1
7. **A configurable tablist label** — absent; `aria-label` is hardcoded. → N2
8. **A content slot that permits structured markup** — absent; content is forced through `<p>`. → N3
9. **An activation-model decision** (automatic vs. manual) — never made, because there is no arrow navigation to make it about. Addressed in the C1 fix.
10. **Empty-`tabs` handling** — `tabs = []` renders an empty labelled tablist with no tabs. Robustness, not access. Noted, not filed.

**Anti-pattern checks from the April 2026 third-party audit** — run and clean: no `role="alert"`/`aria-live` inside a loop (Broadcast vs. Association: clean); no `title` used as an accessible name; no `aria-label` on a wrapper substituting for a visible label (tab labels are visible text); no tables; no images; no `role="presentation"`. **Else-branch coverage** does apply and is the mechanism of C2 — `handleTabKeyDown` handles the `Enter`/`Space` branch and has no other branch at all.

**Known false-positive checks** — the `region` (content-not-in-landmark) signal is present in the trace (`landmark: null`) and I am *not* filing it: it describes the harness page, not the component.

---

## Findings

### Critical Findings (blocks access)

**C1 — Roving tabindex is implemented without arrow-key navigation, making 2 of 3 tabs unreachable by keyboard.**

`src/TabsWidget.jsx:17-22` (`handleTabKeyDown`) matches only `e.key === 'Enter'` and `e.key === ' '`. `src/TabsWidget.jsx:34` sets `tabIndex={index === activeTab ? 0 : -1}`, so every non-selected tab is removed from the Tab sequence. Together these mean a keyboard user can focus exactly one tab — the one already selected — and has no mechanism to reach any other.

Measured, not inferred: `tabs-missing-arrow-nav.trace.json` `step_0002` sends `ArrowRight` and records `focus_moved: false` with `active_element_selector: "#tab-overview"`; `step_0003` sends `ArrowLeft` and records `focus_moved: false` on the same element. `step_0001` announces `"set size 3"`, so two tabs exist that the keyboard cannot reach. `step_0004` shows `Tab` exiting to `body` rather than moving along the tablist.

- **User group**: keyboard-only (complete block); screen reader in focus/forms mode (complete block); screen reader in browse mode (partial — virtual cursor reaches the tabs, but activation hits C2).
- **WCAG / APG**: WCAG 2.1.1 Keyboard (Level A) — functionality is not operable through a keyboard interface. WAI-ARIA APG *Tabs* pattern, Keyboard Interaction: "Left Arrow: moves focus to the previous tab… Right Arrow: moves focus to the next tab." The APG permits roving tabindex *because* arrow keys supply the movement; shipping the tabindex half alone is strictly worse than shipping neither.
- **Confidence**: HIGH (measured twice in a driven session; refutable only by a keyboard path not present in the source).
- **Why this matters**: the widget tells a screen-reader user there are three tabs and then denies two of them. Two-thirds of the content this component exists to present has no keyboard route at all. There is no workaround short of a mouse.
- **Fix**: add arrow/Home/End handling that moves both the roving point and DOM focus. Automatic activation is appropriate here because panel content is static and cheap to swap.

```jsx
const tabRefs = React.useRef([]);

const moveToTab = (i) => {
  const next = (i + tabs.length) % tabs.length;   // wraps, per APG
  setActiveTab(next);
  tabRefs.current[next]?.focus();                 // tabIndex alone never moves focus
};

const handleTabKeyDown = (e, index) => {
  switch (e.key) {
    case 'ArrowRight': e.preventDefault(); moveToTab(index + 1); break;
    case 'ArrowLeft':  e.preventDefault(); moveToTab(index - 1); break;
    case 'Home':       e.preventDefault(); moveToTab(0); break;
    case 'End':        e.preventDefault(); moveToTab(tabs.length - 1); break;
    default: break;   // let the native <button> handle Enter/Space -> onClick
  }
};
```
Wire with `ref={(el) => { tabRefs.current[index] = el; }}` and `onKeyDown={(e) => handleTabKeyDown(e, index)}`.

```
### A11y Evidence Finding
finding_id: tabs-roving-tabindex-without-arrow-keys
fingerprint: 7a1c9e4b2f38d605
source: evals/results/keyboard-a11y-tester/driven/tabs-missing-arrow-nav.trace.json (mode driven-live, goal "navigate between tabs using arrow keys"); src/TabsWidget.jsx:17-22,34
wcag_or_apg: WCAG 2.1.1 Keyboard (A); WAI-ARIA APG Tabs pattern — Keyboard Interaction (Left/Right Arrow)
section_508_fpc_context: not in scope (component-scope review, no declared federal conformance target)
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, keyboard=HIGH, low-vision=MEDIUM, cognitive=MEDIUM, vestibular=LOW, auditory=LOW, environmental-contrast=MEDIUM
evidence: trace.json step_0002 keystroke_sent=ArrowRight focus_moved=false active_element_selector=#tab-overview; step_0003 keystroke_sent=ArrowLeft focus_moved=false active_element_selector=#tab-overview; step_0001 focus_announcement="tab, Overview, selected, 1 control, position 1, set size 3"; step_0004 keystroke_sent=Tab active_element_selector=body
reproduction_steps: 1) Load the component. 2) Press Tab until focus reaches the first tab. 3) Press ArrowRight. 4) Press ArrowLeft. 5) Observe the active element never changes; press Tab and observe focus leaves the widget without visiting tabs 2 or 3.
expected_behavior: ArrowRight moves focus to the next tab (wrapping to the first after the last); ArrowLeft moves focus to the previous tab; the roving tabindex follows focus.
actual_behavior: Both arrow keys are ignored. Focus remains on the selected tab. Tabs 2 and 3 (tabindex="-1") are unreachable by any keyboard route.
trend: new
```

---

**C2 — Enter/Space on a tab sets `activeTab` to `-1`, deselecting every tab, hiding every panel, and removing the widget from the tab sequence.**

`src/TabsWidget.jsx:20`:

```js
handleTabClick(tabs.findIndex(t => t.id === e.currentTarget.id));
```

`e.currentTarget.id` is the *DOM* id, built at `src/TabsWidget.jsx:30` as `` `tab-${tab.id}` ``. The predicate compares that prefixed string against the unprefixed `t.id`. It can never match, so `findIndex` returns `-1` and `setActiveTab(-1)` runs. `e.preventDefault()` at line 19 then suppresses the native button click that would otherwise have called the correct `onClick` handler at line 35, so nothing repairs it.

The trace closes the only escape hatch. If `tab.id` values already carried a `tab-` prefix, the comparison would accidentally succeed — but `step_0001` records `active_element_selector: "#tab-overview"` and `states.controls: "panel-overview"`, which means `tab.id === "overview"`. The comparison is `"overview" === "tab-overview"`. False.

Cascade at `activeTab === -1`, all in one render:
- line 32 — every tab renders `aria-selected="false"`. The APG requires exactly one tab selected; the tablist enters an invalid state.
- line 34 — every tab renders `tabIndex="-1"`. **Nothing in the widget is in the Tab sequence any more.** Once focus leaves, the keyboard cannot return.
- line 51 — every panel renders `hidden`. All content disappears.

- **User group**: keyboard-only (activation destroys the widget); screen reader (same, via any AT path that dispatches a real `keydown` — focus/forms mode; AT paths that dispatch a synthetic click instead are unaffected, so impact varies by AT and mode); mouse users are unaffected, which is exactly why this survives manual QA.
- **WCAG / APG**: WCAG 2.1.1 Keyboard (A) — keyboard activation does not perform the function and leaves the component inoperable. WCAG 4.1.2 Name, Role, Value (A) — no tab reports `aria-selected="true"`. WAI-ARIA APG *Tabs*: "Space or Enter: Activates the tab if it was not activated automatically on focus."
- **Confidence**: HIGH on the logic (identifier mismatch is arithmetically certain, and the trace supplies the actual id values). The one thing I have *not* measured is the Enter keypress itself — the driven session sent only `Tab`, `ArrowRight`, `ArrowLeft`, `Tab`. Flagging that honestly: this finding is a source read corroborated by measured id values, not a measured activation.
- **Why this matters**: this is worse than C1 because it is silent, catastrophic, and unrecoverable. A keyboard user who has just discovered the arrows don't work will very plausibly try Enter next — and the entire widget blanks out with no announcement and no way back short of a page reload. It also cannot be caught by any of the deterministic scans in this evidence pack; only a test that actually presses Enter will find it.
- **Fix**: **delete lines 17–22 outright.** Native `<button>` elements already fire `click` on Enter and Space, so `onClick` (line 35) already handles activation correctly with the right index in scope. The handler was both redundant and wrong. Replace it with the arrow/Home/End handler from C1, whose `default: break` deliberately lets Enter/Space fall through to native behaviour. As defence in depth, clamp state: `setActiveTab((i) => (i >= 0 && i < tabs.length ? i : 0))`.

```
### A11y Evidence Finding
finding_id: tabs-keyboard-activation-deselects-all-tabs
fingerprint: c3f80d5a916e47b2
source: src/TabsWidget.jsx:17-22 (handleTabKeyDown), :30 (id={`tab-${tab.id}`}), :32, :34, :51; id values corroborated by evals/results/keyboard-a11y-tester/driven/tabs-missing-arrow-nav.trace.json step_0001
wcag_or_apg: WCAG 2.1.1 Keyboard (A); WCAG 4.1.2 Name, Role, Value (A); WAI-ARIA APG Tabs pattern — Space/Enter activation
section_508_fpc_context: not in scope (component-scope review, no declared federal conformance target)
severity: CRITICAL
perspective_alarms: keyboard=HIGH, screen-reader=HIGH, cognitive=MEDIUM
evidence: src/TabsWidget.jsx:20 `tabs.findIndex(t => t.id === e.currentTarget.id)` compares unprefixed `t.id` against the prefixed DOM id from :30; trace step_0001 active_element_selector="#tab-overview" with states.controls="panel-overview" establishes tab.id === "overview", so the predicate evaluates "overview" === "tab-overview" (false) for every tab; findIndex returns -1; :19 preventDefault() suppresses the native click that would have reached the correct onClick at :35.
reproduction_steps: 1) Load the component. 2) Press Tab to focus the selected tab. 3) Press Enter (or Space). 4) Observe every panel disappear. 5) Press Tab to leave the widget, then Shift+Tab to return — the tablist can no longer be reached.
expected_behavior: Enter or Space activates the focused tab: that tab becomes aria-selected="true" and tabindex="0", its panel becomes visible, and the widget remains in the Tab sequence.
actual_behavior: activeTab becomes -1. All tabs render aria-selected="false" and tabindex="-1"; all panels render hidden. The widget is emptied and drops out of the Tab sequence with no announcement.
trend: new
```

---

### Major Findings (significantly degrades experience)

**M1 — The tabpanel is not in the tab sequence: it has no `tabindex="0"` and contains no focusable content, so `Tab` from the tab skips the panel entirely.**

`src/TabsWidget.jsx:46-56` renders the panel with `role="tabpanel"` and `aria-labelledby` but no `tabindex`. Its only content is `<p>{tab.content}</p>` (line 54) — static text, nothing focusable. The APG Tabs pattern specifies that when the tablist holds focus, `Tab` "moves focus to the next element in the page tab sequence outside the tablist, which is typically either the first focusable element inside the tab panel or the tab panel itself."

Measured: `step_0004` sends `Tab` from `#tab-overview` and lands on `body` (`tag: "body"`, `role: "none"`, `is_body: true`), never visiting `#panel-overview`. (The landing spot being `body` specifically is an artefact of a minimal harness page with nothing else focusable — what the step proves is that the panel is absent from the sequence, not where focus goes on a real page.)

- **User group**: keyboard-only; screen-reader users in focus/forms mode.
- **WCAG / APG**: WAI-ARIA APG *Tabs* pattern, Keyboard Interaction (Tab); WCAG 2.4.3 Focus Order (A) — the focus order does not preserve meaning when activating a tab produces content the focus order then skips over.
- **Confidence**: MEDIUM-HIGH — the trace fact is unambiguous; the severity is the arguable part (see the Realist Check).
- **Why this matters**: after activating a tab, a keyboard user has no focus anchor in the content they just revealed. They tab forward and are ejected past the payload of the widget entirely, with no signal that the panel exists between the tab and wherever they landed.
- **Fix**: add `tabIndex={0}` to the tabpanel `<div>` at line 48. Panels that are `hidden` stay out of the tab order regardless, so setting it unconditionally on all panels is safe. If a panel later contains its own focusable content, drop the `tabIndex` for that panel — per APG, you want one or the other, not both.

```
### A11y Evidence Finding
finding_id: tabs-tabpanel-not-in-tab-sequence
fingerprint: 5e2b71c8a40df396
source: evals/results/keyboard-a11y-tester/driven/tabs-missing-arrow-nav.trace.json step_0004; src/TabsWidget.jsx:46-56
wcag_or_apg: WAI-ARIA APG Tabs pattern — Keyboard Interaction (Tab); WCAG 2.4.3 Focus Order (A)
section_508_fpc_context: not in scope (component-scope review, no declared federal conformance target)
severity: MAJOR
perspective_alarms: keyboard=HIGH, screen-reader=HIGH, low-vision=MEDIUM
evidence: trace.json step_0004 keystroke_sent=Tab, active_element_selector="body", tag="body", is_body=true, dom_order_index=-1 — focus moved from #tab-overview past #panel-overview without stopping; src/TabsWidget.jsx:48-53 renders role="tabpanel" with no tabindex, and :54 wraps content in a non-focusable <p>.
reproduction_steps: 1) Load the component. 2) Press Tab to focus the selected tab. 3) Press Tab again. 4) Observe focus does not land on the tab panel.
expected_behavior: Tab from the selected tab moves focus into the associated tabpanel (or its first focusable child), so the revealed content is the next stop in the reading order.
actual_behavior: Focus skips the tabpanel entirely and leaves the widget.
trend: new
```

---

### Minor Findings (friction, workaround exists)

- **N1 — DOM ids are not instance-scoped, risking cross-instance ARIA collisions.** `src/TabsWidget.jsx:30` and `:49` build ids from `tab.id` alone (`tab-${tab.id}`, `panel-${tab.id}`). Two `TabsWidget` instances on one page with any overlapping `tab.id` (`"overview"`, `"details"` — likely values) produce duplicate ids; `aria-controls` and `aria-labelledby` then resolve to the first match in document order, silently cross-wiring the widgets. Conditional on usage, which is why it is MINOR rather than MAJOR. WCAG 4.1.2. *Fix*: `const uid = React.useId();` then `` id={`${uid}-tab-${tab.id}`} `` and the matching `aria-controls`/`aria-labelledby`/panel id.

- **N2 — The tablist's accessible name is hardcoded, so every instance is named "Content tabs".** `src/TabsWidget.jsx:26`. This is not a wording preference — a screen-reader user pulling up a list of tablists on a page with two of these hears the identical name twice with no way to tell them apart. WCAG 4.1.2 / 2.4.6. *Fix*: accept a required `label` prop, or `aria-labelledby` pointing at a visible heading above the widget (preferred — a visible label serves everyone).

- **N3 — The `<p>` wrapper forbids structured panel content.** `src/TabsWidget.jsx:54` renders `<p>{tab.content}</p>`. Any panel content richer than a single run of text — a heading, a list, a nested `<div>` — is either flattened or produces invalid nesting that React and the browser will restructure, breaking the semantics a screen-reader user navigates by. WCAG 1.3.1. *Fix*: render `{tab.content}` directly and let callers supply their own semantics, or accept `children`.

---

### Enhancements (best practice not met, no access barrier)

- **E1 — `Home` and `End` are unhandled.** The APG lists both as optional-but-conventional for tablists: `Home` to the first tab, `End` to the last. Cheap to add inside the C1 handler; included in the fix snippet above.
- **E2 — Panel visibility is controlled twice.** The `hidden` attribute (line 51) and the `.active` class (line 52 / CSS 105–115) both key off the same condition, so they cannot currently diverge — but the redundancy is a future footgun. The existing `.tab-panel[hidden] { display: none !important; }` guard (CSS 117–119) is the right defence and should stay. Consider dropping the class-based `display` toggle and letting `hidden` be the single source of truth.
- **E3 — Consider an explicit activation-model decision once arrows land.** Automatic activation (selection follows focus) is right for this component because the panels are static and free to swap. Worth a code comment so a future contributor doesn't "fix" it into manual activation and break the expectation.

---

## Phase 8 — Realist Check (Severity Calibration)

**C1 — no arrow navigation.** Realistic worst case: a keyboard-only user can access one third of the widget's content and has no workaround short of a mouse. Groups affected: keyboard-only, screen reader in focus mode. Detection: not by any deterministic scan in this pack — only by a driven session or a design review, i.e. potentially never in production. This is complete access loss to content, which the recalibration rules explicitly forbid downgrading. **CRITICAL confirmed.**

**C2 — Enter/Space deselects everything.** Realistic worst case: the user presses the most obvious activation key and the entire component blanks out, unannounced, and cannot be re-entered by keyboard. Groups: keyboard-only, screen reader (AT-dependent). Detection: silent — mouse QA never sees it, axe never sees it, and the driven session in this pack didn't send Enter. Complete access loss plus state destruction. **CRITICAL confirmed.**

**M1 — panel not in tab sequence.** This is the one finding where the four questions genuinely bite. Realistic worst case: a keyboard user tabs past the panel and reads its content visually; a screen-reader user reaches it with the virtual cursor, where it has a correct role and a correct accessible name. So a workaround exists — but it applies to *all* keyboard users, not a <5% slice, and the APG names the behaviour explicitly. Held at **MAJOR**, deliberately not raised to CRITICAL (content remains readable) and not dropped to MINOR (the workaround is "read it some other way", which is not a keyboard operation). If the panels later contain focusable content, this finding dissolves on its own.

**N1 — id collisions.** Started as a candidate MAJOR. Downgraded to MINOR. *Mitigated by:* the defect requires two instances on one page with overlapping `tab.id` values — a real but conditional configuration, not the default single-instance case shown in the trace.

**2.4.13 Focus Appearance — deliberately NOT filed.** The trace reports `aaa_pass: false` at `step_0001` and `step_0002` and `aaa_pass: true` at `step_0003` — three measurements of the *same element*, with identical `computed_focus_style` and identical `bounding_box`, disagreeing with each other. The two failing steps report `changed_area: 0` with `contrast: null` and `pixel_cue: false`; the passing step reports `changed_area: 719` against `ref_area_2px_perimeter: 625` with `contrast: 5.56, contrast_pass: true`. An unchanged element cannot have three different focus appearances, so the zero/null readings are an instrument artefact of the pixel-diff capture, not a property of the component. The only measurement that registered a real pixel change is a **pass**. Filing a 2.4.13 finding off `step_0001`/`step_0002` would be a manufactured violation. Separately, 2.4.13 is a Level AAA criterion and the stated target is AA, so even a genuine miss would rank ENHANCEMENT at most. Instrument inconsistency logged as Q3.

---

## Phase 9 — Self-Audit

| Finding | Confidence | Developer could refute? | Gap or preference? | Disposition |
|---|---|---|---|---|
| C1 | HIGH | NO — measured twice in a driven session; no keyboard path exists in source | GAP | Keep |
| C2 | HIGH | NO — the one plausible refutation (`tab.id` already prefixed) is closed by the trace's measured id values | GAP | Keep |
| M1 | MEDIUM-HIGH | Partially — a developer could argue the panel is readable without focus. Addressed in the Realist Check rather than dodged. | GAP | Keep at MAJOR |
| N1 | MEDIUM | YES — "we only ever render one instance" | GAP (conditional) | Keep at MINOR, condition stated |
| N2 | HIGH | Partially — "there is only one tablist per page" | GAP | Keep at MINOR |
| N3 | HIGH | YES — "we only pass strings" | GAP (latent) | Keep at MINOR |

Nothing was moved to Open Questions from the scored findings. Three items were *prevented* from becoming findings by this audit: the 4.1.3 "no announcement on panel change" temptation (the APG does not want a live region here), the forced-colors active-state concern (investigated and found sound — `transparent` is preserved under forced colors), and the 2.4.13 focus-appearance rows (instrument artefact, and AAA).

**Explicit clean bill on what is right**, because a review that only lists faults miscommunicates the state of this component: native `<button>` semantics, complete and correct `role`/`aria-selected`/`aria-controls`/`aria-labelledby` wiring (measured in the accessibility tree), correct roving `tabindex` *values*, the `hidden` attribute as the visibility mechanism with a correct `!important` CSS guard, a strong and measured focus indicator, target sizes measured at 111×45 px, non-colour-only active-state indication that survives forced-colors, and no colour-alone signalling. The problems here are two missing behaviours and one wrong comparison, not a broken design.

---

## Phase 10 — Synthesis: Predictions vs. Findings

| # | Prediction | Outcome |
|---|---|---|
| 1 | Missing arrow key navigation | **Confirmed** — and measured (C1) |
| 2 | Roving tabindex missing entirely | **Wrong in an instructive way** — the values are present and correct, which makes the situation *worse* than my prediction, not better. Correct tabindex with no arrow mechanism actively removes tabs from the keyboard; absent tabindex would at least have left them Tab-reachable. |
| 3 | `aria-selected` desynchronized or `aria-controls` broken | **Refuted** — both correct, confirmed in the computed accessibility tree (`selected: true`, `controls: "panel-overview"`) |
| 4 | Panel not reachable after activation | **Confirmed** — measured at `step_0004` (M1) |
| 5 | Focus indicator suppressed | **Refuted** — 3px outline with 2px offset, measured visible, indicator contrast 5.56:1 |
| 6 | `Home`/`End` missing | **Confirmed** (E1) |

**The surprise**: C2. I predicted nothing about the Enter/Space path, and it is arguably the more dangerous of the two CRITICALs — silent, catastrophic, undetectable by every automated artefact in the evidence pack, and invisible to mouse-based QA. It came out of reading the handler line by line rather than checking the pattern against a list. The pattern-checklist approach found C1; only the line-by-line read found C2. That is the argument for this review step existing at all.

**Second observation worth carrying forward**: prediction #2 being wrong in the direction it was wrong is the general lesson here. A partially-implemented ARIA pattern is not "most of the way there" — a roving tabindex without arrow keys is a net *regression* against plain buttons. Partial implementation of a composite-widget pattern can be worse than no implementation.

---

## What's Missing (consolidated)

- Arrow-key navigation and the `.focus()` call that makes roving tabindex mean anything (C1)
- Any bounds guard on `activeTab`, which is what lets C2 reach an invalid state undetected (C2)
- A focus destination in the revealed panel (M1)
- `Home`/`End` (E1)
- Instance-scoped ids (N1) and a configurable tablist name (N2)
- A content slot that permits semantic markup inside panels (N3)
- **Test coverage that presses Enter and Space.** The driven session sent `Tab`, `ArrowRight`, `ArrowLeft`, `Tab` and therefore could not have found C2. Whatever suite covers this component needs an activation-key case, or the same class of bug ships again.

---

## Multi-Perspective Notes

- **Screen reader user**: the accessibility tree is right and the announcement measured at `step_0001` is exemplary — role, name, selected state, controls relationship, and set position all present. The failure is behavioural, not structural: arrow keys produce measured silence (`new_phrases: []` at `step_0002` and `step_0003`), and the widget announces three tabs while denying keyboard access to two of them. Browse-mode users can still reach tabs 2 and 3 via the virtual buffer, but activating them runs into C2 wherever the AT dispatches a real keydown. Panel changes correctly need no live region, and none is missing.
- **Keyboard-only user**: reaches tab 1, cannot reach tabs 2 or 3, cannot reach the panel, and if they press Enter to try to make something happen, the widget empties and locks them out. This perspective is comprehensively broken despite every ARIA attribute being correct — the clearest possible demonstration that ARIA attributes are not accessibility.
- **Low vision user (200% zoom, high contrast)**: the measured facts are good — focus indicator 3px solid with 2px offset and `visible: true`; indicator contrast 5.56:1; target size 111.16 × 45 px, past both the 24×24 minimum and the 44×44 recommendation. Active-state indication survives forced-colors because inactive borders use `transparent` rather than `none`. Two things remain unverified rather than passing: the page background is never declared in the component's CSS, so the ≈5.74:1 and ≈5.57:1 text-contrast figures rest on a white-background assumption (corroborated by the instrument's 5.56:1 reading, but not proven), and reflow at 200% on a narrow viewport was not measured.
- **Cognitive accessibility**: the widget presents an affordance — tabs — whose learned interaction model it does not honour, with no signal explaining the mismatch. Then the natural recovery attempt (press Enter) triggers silent, unexplained, unrecoverable content loss with no undo. Error prevention and consistent-behaviour expectations both fail, and the failure mode is the one hardest for a user to reason their way out of.

---

## Verdict Justification

**REVISE**, not REJECT. Two CRITICAL findings would ordinarily push toward REJECT, but REJECT means the approach is wrong and the work should restart. The approach here is *right*: native buttons, the correct APG pattern selected, correct roles and relationships confirmed in the computed accessibility tree, correct roving tabindex values, a correct visibility mechanism with a thoughtful CSS guard, a strong measured focus indicator, and non-colour-only state indication that survives forced-colors. What is missing is one event handler and one deleted block. No architectural rework is required, and none of the existing ARIA needs to change.

**REVISE, not ACCEPT-WITH-RESERVATIONS**, because both CRITICAL findings are total keyboard access loss, not degraded experience. Reservations do not cover "two thirds of the content has no keyboard route."

**To reach ACCEPT:**
1. Fix C1 — add `ArrowLeft`/`ArrowRight` (plus `Home`/`End`) handling that moves both the roving point and DOM focus via `.focus()`.
2. Fix C2 — delete `handleTabKeyDown`'s Enter/Space branch entirely (native buttons already do this correctly through `onClick`) and clamp `activeTab` to a valid range as defence in depth.
3. Fix M1 — add `tabIndex={0}` to the tabpanel.
4. Address N1–N3 (`useId` scoping, configurable label, drop the `<p>` wrapper).
5. Re-run the driven session with `Enter` and `Space` in the keystroke sequence, not only `Tab` and the arrows — the current trace structurally could not have caught C2.

**Recalibrations recorded**: N1 downgraded MAJOR → MINOR (mitigated by requiring two instances with colliding `tab.id` values). M1 held at MAJOR after explicit consideration of both a downgrade and an upgrade. Three candidate findings declined as manufactured: 4.1.3 panel-change announcement (the APG does not call for a live region in this pattern), forced-colors active-state loss (investigated — `transparent` inactive borders preserve the indicator), and 2.4.13 focus appearance (contradictory instrument readings on an unchanged element; the one valid measurement is a pass; AAA against an AA target).

**Escalation**: Screen reader and Keyboard-only are at HIGH alarm, Low vision, Cognitive, and Environmental contrast at MEDIUM. All five warrant `/perspective-audit`. Recommend running it *after* C1 and C2 are fixed, since both HIGH alarms are driven by those two findings and would otherwise dominate the audit.

**Evidence-pack note for the record**: 32 of the 33 supplied artefacts describe other pages and contributed nothing to this review. No finding above cites one. The single in-scope artefact — the driven trace — carried C1 and M1 outright and supplied the id values that made C2 provable. Volume of evidence was not the constraint; scope discipline was.

---

## Open Questions (unscored)

- **Q1 — Page background is never declared.** `.tab-button` sets `background: transparent` (CSS line 82) and nothing in the component establishes what it sits on. All text-contrast figures here (`#666` ≈5.74:1, `#0066cc` ≈5.57:1) assume white. The instrument's independently measured 5.56:1 for the `#0066cc` outline is consistent with white or near-white, but does not prove it. **Check**: inspect the computed background behind the tablist in DevTools and recompute both ratios against the actual value. If the widget is ever placed on a tinted surface, `#666` at 4.5:1 has very little headroom.
- **Q2 — Reflow at 200% zoom / 320px width is unverified.** `[role="tablist"]` is `display: flex` with `gap: 4px` and no `flex-wrap` (CSS lines 72–76). Flex children shrink by default, so short labels will compress rather than overflow — but three tabs with long labels plus 20px horizontal padding each could exceed min-content width and force horizontal scroll (WCAG 1.4.10). **Check**: render with the longest realistic labels at 320px CSS width / 200% zoom and confirm no horizontal scrollbar; if it overflows, add `flex-wrap: wrap` or a horizontally scrollable tablist with the accompanying keyboard-scroll affordances.
- **Q3 — Focus-appearance instrument inconsistency, for upstream reporting.** `tabs-missing-arrow-nav.trace.json` reports `focus_appearance.aaa_pass` as `false`, `false`, `true` across `step_0001`–`step_0003` for an element whose `computed_focus_style` and `bounding_box` are byte-identical in all three, and `changed_area` as `0`, `0`, `719`. This looks like the pixel-diff capture lacking a valid reference frame on some steps. Not a component defect — but if 2.4.13 rows from this runner are ever consumed programmatically, this failure mode will generate false positives at scale. Worth a bug against the runner.
- **Q4 — Is `tab.id` guaranteed unique and stable?** `key`, both DOM ids, `aria-controls`, and `aria-labelledby` all derive from it. Duplicate or unstable ids break React reconciliation and the ARIA relationships simultaneously. Not verifiable from the supplied source. **Check**: confirm at the data layer, or derive ids from index plus a `useId` prefix instead.
- **Q5 — Empty `tabs` array.** `tabs = []` renders a labelled but empty tablist and no panels. A screen-reader user encounters a "Content tabs" tablist containing nothing. Low likelihood, trivial fix (render nothing, or an empty-state message). Raised as a robustness question rather than filed as a finding, since I have no evidence the empty case occurs.
- **Q6 — Fingerprints in the Evidence Finding blocks above are placeholders.** I did not compute them; a harness that hashes `finding_id + component path + selector` should overwrite them before these blocks are used for trend tracking. Flagging rather than presenting them as real hashes.
