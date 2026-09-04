**VERDICT: REVISE**

**Overall Assessment**: The ARIA scaffolding on this tabs widget is genuinely correct — native `<button>` elements carrying `role="tab"`, a labelled `role="tablist"`, `aria-selected` bound to state, and bidirectional `aria-controls`/`aria-labelledby` that the supplied trace confirms actually resolve in the accessibility tree. What is missing is the entire behavior layer that makes that scaffolding usable: there is no arrow-key handler, and because roving tabindex *is* implemented (`tabIndex={index === activeTab ? 0 : -1}`), every tab except the active one has been removed from the tab sequence with nothing put in its place. Two of the three tabs are unreachable by keyboard. Separately, the one keyboard handler that does exist is actively destructive: an id-prefix mismatch makes `findIndex` return `-1` on every Enter/Space press, which deselects all tabs, hides all panels, and drops the entire tablist out of the tab order with no keyboard path back.

This is not a widget that needs redesigning. It is a widget whose behavior layer was never written, shipped with a self-declared feature checklist that reads as if it had been.

---

## Evidence Provenance and Tier (Phase 0)

**Review type**: fresh design pass, not a fix/remediation review. The a11y-test *Verification evidence contract* mismatch check (which applies when evidence is offered as proof that a fix landed) does not apply here; no fix is being claimed.

**Prerequisite check — NOT satisfied.** The protocol requires automated checks to have run before design review. The evidence digest's own "Absence claims" and "Not claimed" sections state plainly that **no axe-core artifact of any kind exists in this evidence set**, and no real-keyboard `npx playwright test` transcript exists either. The ten-item "Accessibility Features Present" checklist in the review request is a **developer assertion, not a measurement**, and two of its claims are false (see Finding 2 and Finding 4). I am proceeding, but every finding below that would be stronger with measurement is marked as such.

**Evidence tiers actually available:**

| Evidence | Tier | Bears on |
|---|---|---|
| Component source + CSS (in the review request) | **First-tier.** Read directly. | Findings 1, 2, 3, 4, 5, 6, 7, 8 |
| `keyboard-a11y-tester` driven trace, `tabs-missing-arrow-nav.trace.json` | **Digest-only** (see below) | Corroborates Finding 2; positively confirms the ARIA layer |
| 32 `keyboard-a11y-tester` batch-crawl findings files | **Out of scope — 32 other components.** Not used. | Nothing. See "Evidence Not Used." |

**Digest-only labelling.** The trace observations reach me through an `a11y-evidence-reader` digest, which the protocol classifies as detector output one tier *below* the artifact it paraphrases. The contract requires re-fetching at the cited handle (`jq '.steps[]|{step_id,keystroke_sent,active_element_selector,focus_moved}'` on `evals/results/keyboard-a11y-tester/driven/tabs-missing-arrow-nav.trace.json`) before filing a finding that rests on a digest line. I could not re-fetch in this review. **Every trace-derived claim below is therefore labelled digest-only.** This does not weaken the headline finding: Finding 2 stands independently on first-tier source evidence (the absence of any arrow-key branch in `handleTabKeyDown` and the presence of `tabIndex={-1}` on non-active tabs are both readable in the component itself). The trace corroborates a conclusion already reachable from source; it is not load-bearing for it.

**Positive evidence — the ARIA layer is measured-correct.** The digest reports step_0001's `focus_announcement` as:

```
"tab, Overview, selected, 1 control, position 1, set size 3"
```

Role (`tab`), accessible name (`Overview`), selected state, and `aria-controls` resolving to exactly **one existing element** ("1 control") are all present in the computed AX tree, and `posinset`/`setsize` resolve to 1 of 3. That satisfies the mandatory DOM-verification check for aria-* fixes (anti-pattern #9): the `aria-controls`/`aria-labelledby` id references are not dangling. Digest-only tier, but it is the right shape of evidence and I am crediting it rather than re-litigating the ARIA attributes from first principles.

**Evidence Not Used — and why (this is deliberate, not an oversight).**

The evidence pack contains 32 batch-crawl findings files covering **32 distinct other components**. The digest states explicitly that the one file matching this component's name was withheld by pack policy and that none of the 32 in-policy files is this component. I have imported **zero** findings from them. Four were tempting and I am naming them so the exclusion is auditable:

1. `missing-accessible-name-desktop` (WCAG 4.1.2, severity "serious", *"1 focusable control(s) have no accessible name: tabpanel at #panel-1"*) — in `tabs-incomplete-aria-selected.json`. This is the highest-risk cross-contamination candidate in the whole pack: a *different* tabs fixture, with a *tabpanel* defect. Not filed. This component's tabpanels carry `aria-labelledby` and are not focusable, so the finding does not even transfer on the merits.
2. `focus-appearance-weak-desktop` (WCAG 2.4.13) — present in 19 of 32 files, near-ubiquitous, and therefore the single easiest false positive to import by osmosis. Not filed, for three independent reasons: it describes other components; 2.4.13 is Level **AAA** and the artifact's own `conformance_level: "AAA"` is correct here (the upstream mislabelling caveat does not bite on 2.4.13, which genuinely is AAA); and this component's own `outline: 3px solid #0066cc; outline-offset: 2px` would very likely clear the bar anyway (see Finding 8).
3. `sr-live-region-silent-desktop` (WCAG 4.1.3) — in 5 other components. Not filed, twice over: wrong component, and the calibration rule is explicit that batch-crawl 4.1.3 "silent live region" rows are prompts to run a driven session, never failure evidence.
4. `sr-heading-skip-desktop` (1.3.1), `no-skip-link-desktop` (2.4.1), `positive-tabindex-desktop` (2.4.3) — all other components. This component renders no headings (correct for a widget), needs no landmark or skip link at component scope, and uses only `0` and `-1` for tabindex.

The digest also notes that the corpus's structural-flavoured rows are keyboard-a11y-tester's own `"source":"deterministic"` detector output, **not axe-core rule IDs**, despite the framing question naming axe-core as a candidate producer. I have not cited any of them as axe evidence.

---

## Pre-commitment Predictions (Phase 1)

Made before reading the source, from component type ("tabs widget"):

| # | Prediction | Outcome |
|---|---|---|
| P1 | Missing `role="tablist"` | **Wrong** — present, and labelled |
| P2 | `aria-selected` not synchronized to state | **Wrong** — correctly bound to `index === activeTab` |
| P3 | Panels not referenced by `aria-labelledby` / tabs missing `aria-controls` | **Wrong** — both present, both resolve (trace confirms) |
| P4 | **Arrow-key navigation missing** | **Correct** — and worse than predicted, because roving tabindex is present |
| P5 | Roving tabindex absent | **Wrong in the way that matters** — the *values* are right, the *mechanism* is absent. Half a roving tabindex is worse than none |
| P6 | Tabpanel not focusable when it holds no focusable content | **Correct** |
| P7 | Focus not moved programmatically after selection | **Correct** — there is no `useRef`, so no focus-move mechanism exists at all |

**What I did not predict, and should have**: that the *existing* keyboard handler is destructive rather than merely absent. I went looking for a missing feature and found a live defect. Predicting "arrow keys missing" primed me to read `handleTabKeyDown` for what it lacked rather than for whether what it contains is correct. Noted as a personal miss in Phase 10.

---

## Semantic HTML Audit (Phase 2)

Clean. Recorded explicitly because a clean result here carries signal:

- **Native HTML first — satisfied.** Tabs are real `<button>` elements (`TabsWidget.jsx:21`) with `role="tab"` layered on top. This is ARIA *enhancing* native semantics, which is the APG-sanctioned construction, not ARIA *replacing* them. No `div role="button"` anywhere. Native Enter/Space activation and focusability come for free — which is exactly what makes Finding 1 so avoidable.
- **Container divs** (`TabsWidget.jsx:18`, `:19`, `:37`) carry no inappropriate roles. `role="tablist"` on a `div` is correct per the APG pattern.
- **Headings**: none rendered. Correct for a reusable widget; heading hierarchy is a page-scope concern and this component should not invent one.
- **Landmarks**: none. Correct at component scope.
- **Lists**: the tablist is not a `<ul>`. This is correct — APG's tabs pattern does not use list semantics, and `role="tablist"` supplies the set relationship (`set size 3` in the trace announcement proves it computed).
- **Tables, form labels, layout tables**: not applicable.

No ARIA is masking bad structure here. No MAJOR finding from Phase 2.

---

# Findings

## Critical Findings (blocks access)

### 1. Enter/Space on any tab deselects every tab, hides every panel, and removes the entire tablist from the tab order — with no keyboard path back

**Evidence** — `TabsWidget.jsx:10-15`, specifically line 13:

```jsx
handleTabClick(tabs.findIndex(t => t.id === e.currentTarget.id));
```

`e.currentTarget` is the `<button>`, whose DOM id is set at `TabsWidget.jsx:23` as:

```jsx
id={`tab-${tab.id}`}
```

So `e.currentTarget.id` is `"tab-overview"` while `t.id` is `"overview"`. **`findIndex` returns `-1` for every tab, for every possible shape of the `tabs` prop.** There is no consumer input that makes this match — a caller who pre-prefixes their ids gets `tab-tab-overview` and still fails. (A second, independent defect sits in the same expression: `t.id` may be a number while `e.currentTarget.id` is always a string, so `===` would fail on type even without the prefix.)

`setActiveTab(-1)` then cascades through all four state-derived attributes:

| Line | Expression | Result at `activeTab === -1` |
|---|---|---|
| `:25` | `aria-selected={index === activeTab}` | `false` on **every** tab — an ARIA-invalid tablist with no selected tab |
| `:27` | `tabIndex={index === activeTab ? 0 : -1}` | `-1` on **every** tab — the whole tablist leaves the tab sequence |
| `:44` | `hidden={index !== activeTab}` | `true` on **every** panel — all content disappears |
| `:30`/`:45` | `active` class | removed everywhere — `.tab-panel` base rule (`tabs.css:38-39`) enforces `display: none` regardless |

**Why this is unrecoverable, not merely broken.** The pressed button keeps DOM focus (setting `tabindex="-1"` on a focused element does not blur it), so the user is standing on a control that is still focused but no longer reachable. Pressing Enter again re-runs the same `findIndex` and changes nothing. There are no arrow keys (Finding 2). The moment the user presses Tab, focus leaves the widget and **cannot return** — no tab is tabbable, and no panel is focusable (Finding 3). Recovery requires a mouse click or a page reload.

Note the compounding irony: because these are native `<button>` elements, Enter and Space **already worked correctly** before this handler existed. The `e.preventDefault()` at `TabsWidget.jsx:12` suppresses the browser's own activation click — so `onClick` at `:28`, which receives the correct `index` from the closure and works perfectly, never fires on the keyboard path. The handler replaces working native behavior with broken custom behavior.

- **User group impacted**: keyboard-only users and screen reader users (both of whom activate controls with Enter/Space as the default gesture). Mouse and touch users are entirely unaffected, which is why this survives casual QA.
- **WCAG**: 2.1.1 Keyboard (the widget becomes inoperable by keyboard), 4.1.2 Name, Role, Value (`aria-selected="false"` on all tabs is an invalid tablist state), 1.3.1 Info and Relationships (the tab/panel relationship is destroyed at runtime). WAI-ARIA APG **Tabs** pattern: exactly one tab in a tablist must have `aria-selected="true"`.
- **Confidence**: HIGH. Refutable by developer context? **NO** — the mismatch is between two string expressions ten lines apart in the same file. GAP, not preference.
- **No measured evidence exists for this path.** The supplied trace sends only `Tab`, `ArrowRight`, `ArrowLeft`, `Tab` (steps 0001–0004, digest-only). Enter and Space were never pressed in any artifact in this evidence set. I am **not** attaching an `A11y Evidence Finding` block to this finding, because doing so would dress first-tier source reasoning as measurement. It should be measured before the fix is verified.

**Fix**: delete the Enter/Space branch entirely. Native `<button>` handles activation correctly and `onClick` at `:28` already receives the right index. Then rebuild `handleTabKeyDown` as the arrow-key handler Finding 2 requires (code in Finding 2). Do not "fix" line 13 by stripping the prefix — the index is already in scope; the lookup should not exist.

**Regression guard worth adding alongside**: clamp `activeTab` so no code path can select a nonexistent tab. `setActiveTab(i)` should reject `i < 0 || i >= tabs.length`. This also closes the sibling defect where a shrinking `tabs` prop leaves `activeTab` out of range and reproduces the identical all-hidden state from a different direction.

---

### 2. No arrow-key navigation — and roving tabindex has already removed the fallback, so 2 of 3 tabs are unreachable by keyboard

**Evidence** — `TabsWidget.jsx:10-15` contains branches for `Enter` and `' '` only. There is no `ArrowRight`, `ArrowLeft`, `Home`, or `End` branch anywhere in the component. There is no `useRef`, so **no mechanism to move focus programmatically exists at all** — this is not a handler that was written and left incomplete; the focus-management layer was never started.

Meanwhile `TabsWidget.jsx:27` implements the *values* of roving tabindex:

```jsx
tabIndex={index === activeTab ? 0 : -1}
```

Roving tabindex is two halves: `tabindex="-1"` on inactive items, *and* an arrow-key handler that moves both focus and the `0`. **Only the first half shipped — the half that removes access.** Without arrow keys, this line is not an accessibility feature; it is the defect. A widget with no roving tabindex at all would at least let Tab walk every tab. This one lets Tab reach exactly one.

The review request lists "✓ Roving tabindex (active tab tabindex="0", others "-1")" under **Accessibility Features Present**, and lists "Tab key navigates through tabs" under Expected Behavior. Both are wrong as shipped. That mislabelling is itself worth naming: it is the mechanism by which this defect reaches production believed-fixed.

**Corroborating measured evidence** *(digest-only tier — not re-fetched; handle: `evals/results/keyboard-a11y-tester/driven/tabs-missing-arrow-nav.trace.json`, `jq '.steps[]|{step_id,keystroke_sent,active_element_selector,focus_moved}'`)*:

```
{"step_id":"step_0001","keystroke":"Tab",       "selector":"#tab-overview","focus_moved":true}
{"step_id":"step_0002","keystroke":"ArrowRight","selector":"#tab-overview","focus_moved":false}
{"step_id":"step_0003","keystroke":"ArrowLeft", "selector":"#tab-overview","focus_moved":false}
{"step_id":"step_0004","keystroke":"Tab",       "selector":"body",         "focus_moved":true}
```

Both arrow presses leave focus pinned on `#tab-overview`. And step_0004 is the second half of the proof: Tab from the first tab lands on **`body`** — not on tab 2, not on the tabpanel. The widget contains exactly **one** keyboard-reachable element in total. Step_0001's announcement gives the denominator: `"position 1, set size 3"` — **2 of 3 tabs, and the content of 2 of 3 panels, are unreachable to a keyboard-only or screen reader user.** Those panels are `hidden`, so there is no alternate route to their content.

- **User group impacted**: keyboard-only users, screen reader users (a virtual-cursor user can *read* a hidden panel? No — `hidden` and `display: none` remove it from the AX tree entirely, so the content is gone for them too), switch-access and voice-control users who drive via the tab sequence.
- **WCAG**: 2.1.1 Keyboard (Level A — content is not operable through a keyboard interface). WAI-ARIA APG **Tabs** pattern, Keyboard Interaction: for a horizontal tablist, `Right Arrow` moves focus to the next tab (wrapping to first), `Left Arrow` to the previous (wrapping to last). These are **required**, not optional, in the APG pattern. (`Home`/`End` are the pattern's *optional* keys — see Enhancements; I am not inflating those into this finding.)
- **Confidence**: HIGH, on first-tier source evidence alone. Refutable by developer context? **NO.** GAP.

```
### A11y Evidence Finding
finding_id: tabs-arrow-keys-do-not-move-focus
fingerprint: [NOT COMPUTED — no execution environment in this read-only review. Derive before filing as: sha256("tabs-arrow-keys-do-not-move-focus|TabsWidget.jsx:27|role=tab|WCAG-2.1.1")[0:16]. Deliberately not fabricated; a plausible-looking hex string here would be indistinguishable from a real one.]
source: keyboard-a11y-tester driven trace, evals/results/keyboard-a11y-tester/driven/tabs-missing-arrow-nav.trace.json (DIGEST-ONLY — reached via a11y-evidence-reader digest, not re-fetched at the handle) + first-tier source read of TabsWidget.jsx:10-15, :27
wcag_or_apg: WCAG 2.2 SC 2.1.1 Keyboard (Level A); WAI-ARIA APG Tabs pattern — Keyboard Interaction (Left/Right Arrow)
section_508_fpc_context: In scope if the project has declared Revised Section 508 — 2.1.1 is Level A in WCAG 2.0 and therefore inside the federal web floor (E205.4). Not declared for this review; recorded as context only.
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, keyboard-only=HIGH, low-vision=MEDIUM, cognitive=MEDIUM, vestibular=LOW, auditory=LOW, environmental-contrast=MEDIUM
evidence: trace.json step_0002 keystroke=ArrowRight active_element_selector=#tab-overview focus_moved=false; step_0003 keystroke=ArrowLeft active_element_selector=#tab-overview focus_moved=false; step_0004 keystroke=Tab active_element_selector=body focus_moved=true. Source: TabsWidget.jsx:27 tabIndex={index === activeTab ? 0 : -1} with no ArrowLeft/ArrowRight branch in handleTabKeyDown (TabsWidget.jsx:10-15) and no useRef in the component.
reproduction_steps: 1. Render TabsWidget with 3 tabs. 2. Tab until focus lands on the first tab. 3. Press ArrowRight. 4. Press ArrowLeft. 5. Press Tab.
expected_behavior: ArrowRight moves focus to tab 2 and (under automatic activation) selects it; ArrowLeft from tab 1 wraps focus to tab 3. Tab from the tablist moves focus into the active tabpanel.
actual_behavior: Both arrow presses are no-ops; focus stays on #tab-overview. Tab exits the widget to body. Tabs 2 and 3 and their panel content are unreachable by keyboard.
trend: new
```

**Fix** — add the arrow-key layer and the ref array that makes focus movable. Automatic activation (selection follows focus) is the right choice here because the panels render a single `<p>` and are cheap to swap; the APG permits it explicitly for exactly this case.

```jsx
const tabRefs = useRef([]);

const focusTab = (i) => {
  const next = (i + tabs.length) % tabs.length;   // wrap, per APG
  setActiveTab(next);                              // automatic activation
  tabRefs.current[next]?.focus();
};

const handleTabKeyDown = (e, index) => {
  switch (e.key) {
    case 'ArrowRight': e.preventDefault(); focusTab(index + 1); break;
    case 'ArrowLeft':  e.preventDefault(); focusTab(index - 1); break;
    case 'Home':       e.preventDefault(); focusTab(0); break;
    case 'End':        e.preventDefault(); focusTab(tabs.length - 1); break;
    default: break;   // Enter/Space: let the native <button> fire onClick
  }
};
```

with `ref={(el) => (tabRefs.current[index] = el)}` and `onKeyDown={(e) => handleTabKeyDown(e, index)}` on the button at `:21-31`.

**On focus timing** — the protocol flags React unmount-timing traps where focus assignments are dropped and need `setTimeout(0)`. That trap does **not** apply here, and wrapping this call would be cargo-culting: the target button is already mounted and keyed by `tab.id`, so it is not unmounted by the state change, and `.focus()` works on a `tabindex="-1"` element (which is programmatically focusable by definition). Call it synchronously. Stating this explicitly so the fix is not "improved" into an unnecessary timer.

---

## Major Findings (significantly degrades experience)

### 3. Tabpanel is not focusable, so the widget has no keyboard landing spot for its own content

**Evidence** — `TabsWidget.jsx:39-46`. The panel `div` carries `role="tabpanel"`, `id`, `aria-labelledby`, and `hidden`, but no `tabIndex`. Its only content is `<p>{tab.content}</p>` (`:47`) — **no focusable elements**.

The APG Tabs pattern is conditional and the condition is met: *if the tabpanel contains no focusable elements, the tabpanel itself should have `tabindex="0"`* so that Tab from the tablist lands in the content region. Trace step_0004 (digest-only) confirms the consequence directly: Tab from `#tab-overview` goes to **`body`**, skipping the panel entirely.

- **User group impacted**: keyboard-only users, and low-vision keyboard users using a screen magnifier, who rely on focus position to drive the viewport to the content they just revealed.
- **WCAG / APG**: WAI-ARIA APG Tabs pattern (tabpanel focusability); WCAG 2.4.3 Focus Order (the reading path skips the region the user just activated).
- **Confidence**: HIGH on the pattern gap. Refutable? Partially — a developer could say "panel content will contain links in real use," which would make the panel correctly non-focusable. That is a legitimate objection and it is why this is MAJOR, not CRITICAL. GAP.

**Severity calibration (Phase 8, stated inline because it is contested)**: On its own merits this is **MINOR** — a keyboard user can still scroll the document without focusing the panel, and the realistic worst case is friction, not exclusion. I am filing it at **MAJOR** for one specific compounding reason: combined with Finding 2, it means this widget's total keyboard surface is **one button**. There is nowhere for focus to be inside the component, which is what makes step_0004's jump to `body` possible. If Finding 2 is fixed and Finding 3 is not, this drops to MINOR and should be re-rated then.

**Fix**: `tabIndex={0}` on the panel div at `:39`. If the panel is later given focusable content, compute it (`tabIndex={hasFocusableContent ? undefined : 0}`) rather than leaving it unconditionally focusable.

---

### 4. State-change announcement on panel switch is entirely unmeasured — and this evidence set cannot measure it

Raising this as a finding against the **evidence**, not the code, because the alternative is to guess.

Under automatic activation, focus stays on the tab and `aria-selected` flips from `false` to `true` on the newly focused element while the previous tab flips to `false`. Whether a screen reader announces that transition — and what it says — is exactly the class of behavior that separates a widget that works from one that merely validates. It is not determinable by reading source.

The supplied evidence **cannot** answer it, and the digest says so precisely. Its Absence claims record: *"No step in the trace shows an AX-state change with zero announcement — query `states[i] != states[i-1] and live_announcements==[]` returned empty (states never change in this trace)."* The states dict for `#tab-overview` is byte-identical across steps 0001–0003, and `focus_announcement` is non-null only at step_0001.

**I am explicitly not filing "ARIA state changes without announcement."** The trace shows *inaction*, not a silent state change — the arrow keys did nothing, so nothing changed, so nothing was announced. Reading a defect into that null result would be inventing a finding out of an absence. The digest flags this as an absence claim precisely so a consumer does not make that error, and I am honouring it.

The digest further records that **no `virtual-screen-reader` assertion output exists** in this set — that being the contract's canonical `name-role-state` instrument — and that the trace's own `ax_name_role_state`/`sr_announcement` fields are keyboard-a11y-tester's self-reported data, one instrument short of canonical.

- **User group impacted**: screen reader users. Unknown magnitude, which is the finding.
- **WCAG**: 4.1.2 Name, Role, Value — untested for the transition case.
- **Confidence**: HIGH that the gap in coverage exists; **no confidence claim at all** about the underlying behavior.

**Fix (a test, not a code change)**: add a component-lane `@guidepup/virtual-screen-reader` assertion that mounts the widget, activates tab 2, and asserts the spoken-phrase log contains the new tab's name plus `selected`. Then re-run the driven trace with `ArrowRight` *after* the fix so a state transition actually occurs and `sr_announcement` has something to capture. Until one of those exists, the announcement behavior of this widget is asserted by nobody.

---

## Minor Findings (friction, workaround exists)

- **Flex tablist has no wrap or overflow strategy — reflow risk at 320px / 400% zoom.** `tabs.css:5-9` sets `display: flex` with `gap: 4px` and no `flex-wrap`, no `overflow-x`. Each tab is `padding: 12px 20px` at `font-size: 16px` (`tabs.css:11-16`), so three tabs of moderate label length will exceed a 320 CSS-pixel viewport and force two-dimensional page scrolling. WCAG 1.4.10 Reflow. **Needs user verification** — this is conditional on tab count, label length, and container width, none of which the component controls. Concrete check: render with the longest real label set at a 320px viewport width and at 400% zoom on a 1280px viewport; if the page scrolls horizontally, it fails. Confidence: MEDIUM — filed as MINOR rather than MAJOR precisely because I cannot resolve the condition from the artifacts given.

- **Element ids are not unique across component instances.** `TabsWidget.jsx:23` and `:41` build ids as `tab-${tab.id}` / `panel-${tab.id}`. Two `TabsWidget` instances on one page sharing any `tab.id` produce duplicate ids, and `aria-controls`/`aria-labelledby` then resolve to whichever element the browser finds first — silently wiring a tab to the wrong panel with no visual symptom. WCAG 1.3.1 / 4.1.2. Fix: `const uid = useId();` and prefix both id builders. Confidence: MEDIUM on real-world occurrence (depends entirely on how the component is consumed); HIGH that the exposure exists in a component published for reuse.

- **Empty or shrinking `tabs` prop produces an invalid tablist.** `tabs = []` renders `<div role="tablist" aria-label="Content tabs">` containing zero tabs — announced to screen reader users as a labelled, empty composite widget. And if `tabs` shrinks below the current `activeTab` (React state persists across prop changes), the component reproduces the exact all-deselected/all-hidden state of Finding 1 from a different direction. The `activeTab` clamp recommended in Finding 1 fixes the second case; an early return fixes the first.

---

## Enhancements (best practice not met, no access barrier)

- **`Home` / `End` key support.** APG lists these as **Optional** for the Tabs pattern, so their absence is not a pattern violation. Worth adding with the arrow handler since the code is four lines (already included in the Finding 2 fix sketch) — but I am explicitly not inflating an optional key into a MAJOR, which is the standard way this pattern gets over-flagged.

- **Hardcoded, non-specific tablist label.** `aria-label="Content tabs"` (`TabsWidget.jsx:19`) is a fixed English string baked into a reusable component. Every instance on a page gets the identical accessible name, so a screen reader user encountering two of these cannot tell them apart in a landmark/element listing, and the string cannot be localized. This is a concrete structural argument, not "the label could be more descriptive" — the fix is to accept a required `label` prop and pass it through. Prefer `aria-labelledby` pointing at a visible heading where the page provides one.

- **`:focus` rather than `:focus-visible`.** `tabs.css:33` applies the outline on all focus, including mouse click. This *over*-shows the indicator, which is safe (never an access barrier) and arguably correct for a roving-tabindex widget where focus position is load-bearing. Recorded as a deliberate-looking choice, not a defect.

---

## What's Missing (Phase 7 — gap analysis)

Absences, in rough order of consequence:

1. **Any focus-move mechanism.** No `useRef`, no ref array, no `.focus()` call anywhere in the component. Finding 2 is not a missing handler on top of existing plumbing — the plumbing does not exist. Any fix touches the component's structure, not just its event map.
2. **Arrow-key handling** (Finding 2) — the APG-required half of roving tabindex.
3. **`tabindex="0"` on the tabpanel** (Finding 3) — the widget's only possible content landing spot.
4. **A range guard on `activeTab`.** Nothing prevents the state from holding an index that selects no tab, which is the mechanism by which Finding 1 becomes unrecoverable rather than merely wrong.
5. **`useId()` scoping** for ids in a reusable component.
6. **A `label` prop.** No way to name an instance; no i18n path.
7. **Any axe-core or Pa11y run.** The prerequisite for this review was never met; the digest confirms no machine-detectable artifact of any kind exists in this evidence set.
8. **Any real-keyboard Playwright transcript.** The canonical `keyboard-operability` instrument is absent; the driven trace is the closest substitute available and it reaches me digest-only.
9. **Any component-level screen-reader assertion** (Finding 4) — no `virtual-screen-reader` output, so panel-switch announcement is unasserted.
10. **An Enter/Space test case.** Every artifact in the set presses only Tab and arrows. The single most destructive defect in this component sits on the one keyboard gesture nothing tested.

**Anti-pattern sweep (April 2026 third-party list)** — checked, and I want the negative results on record rather than silently omitted:
- #1 Broadcast vs. association: no `role="alert"` or `aria-live` anywhere; nothing inside the `.map()` loops broadcasts. Not applicable.
- #2 `title` vs `aria-label`: no `title` attributes. Clean.
- #3 ARIA without visible label: tabs have visible text (`{tab.label}`, `:32`) *and* programmatic role/state. Clean.
- **#4 Else-branch coverage: HIT.** `handleTabKeyDown` (`:11`) has exactly one branch — `Enter || ' '` — and no `else`/`default`. Every other key, arrows included, falls through unhandled. This is precisely the pattern the anti-pattern list warns about: one branch handled, the rest silently absent. It is the mechanical root of Finding 2.
- #5 Single-selector scope: not applicable (single render path, no view modes).
- #6 `td` in loop / #7 `role="presentation"` on data tables: no tables.
- #8 Decorative alt: no images.
- **#9 DOM-verification: PASSES**, and this is the one place the trace earns its keep. The announcement `"tab, Overview, selected, 1 control, position 1, set size 3"` proves `aria-controls` resolves to exactly one real element in the rendered output — not merely that the attribute was written. Digest-only tier.

---

## Multi-Perspective Notes (Phase 6)

**Screen reader user (NVDA / JAWS / VoiceOver).** The structure they encounter on arrival is correct and the trace proves it computes: a labelled tablist, a tab with role, name, selected state, `posinset 1`, `setsize 3`. Then it stops. `setsize 3` is an explicit promise of three tabs that the keyboard cannot keep — the widget *tells* the user two more tabs exist and provides no way to reach them. That gap between announced structure and available operation is worse than a widget that never claimed the structure, because the user will hunt for the missing two. If they press Enter on the tab they can reach, the widget collapses (Finding 1): every tab reports `not selected`, all panel content vanishes from the AX tree, and the tablist stops being reachable. What happens on a successful panel switch is **unmeasured** (Finding 4).

**Keyboard-only user.** One reachable control in the entire component. Tab in, Tab out to `body` (trace step_0004). Arrows do nothing (steps 0002–0003). Enter destroys it irrecoverably. Two of three panels' content has no keyboard route at all. The focus indicator itself is fine — 3px solid, 2px offset, roughly 5.6:1 against white — but it can only ever be seen on one button, which is a fair summary of the whole widget: the parts that exist are built well, and most of the parts do not exist.

**Low vision user (200–400% zoom, magnifier, high contrast).** Contrast holds on the numbers I can compute, all against an *assumed* white page background that the supplied CSS never declares (see Open Questions): inactive tab `#666` ≈ 5.74:1, active tab and hover `#0066cc` ≈ 5.57:1 (both clear 4.5:1 for 16px normal text), focus outline `#0066cc` ≈ 5.57:1 (clears the 3:1 non-text bar). Target size passes comfortably — `12px 20px` padding on 16px text gives roughly 43px height, well over the 24×24 minimum of WCAG 2.5.8. The selected state is conveyed by three channels, not color alone: color *plus* a 3px bottom border *plus* `font-weight: 600` (`tabs.css:27-31`), so 1.4.1 is satisfied and the state survives forced-colors mode via the weight change. The live concerns are the unwrapped flex row at narrow widths (MINOR, 1.4.10) and the fact that a magnifier user driving by keyboard can never move the viewport into the panel content (Finding 3).

**Cognitive accessibility.** The interaction model is *inconsistent across input methods*, which is the worst shape this can take: the same widget behaves correctly with a mouse and destructively with a keyboard. A user who switches between input methods — which includes many users with motor or fatigue-related conditions — gets contradictory feedback from the same control. When Enter collapses the widget there is no error message, no undo, no confirmation, and no visible cause: content simply disappears. WCAG 3.2.2 On Input is arguably implicated (activating a control produces a change of context the user was not warned about), though I am not filing it separately — it is a symptom of Finding 1, and splitting it out would be double-counting.

**Vestibular & motion.** Nothing to review. `transition: color 0.2s` (`tabs.css:20`) is a color interpolation with no movement, scale, or parallax — it is not motion animation, and a `prefers-reduced-motion` guard for it would be ceremony. No autoplay, no flashing. **Not filed.** Recording it because "missing `prefers-reduced-motion`" on any CSS containing the word `transition` is one of the most common manufactured findings in this category.

**Auditory access.** No `<video>`, no `<audio>`, no sound-only feedback. Not applicable.

**Environmental contrast.** Covered under low vision. The one open item is the undeclared page background, which every ratio above depends on.

### Perspective Alarm Levels

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | **HIGH** | Custom composite widget; `aria-selected` reachable in an all-false invalid state; `setsize 3` announces structure the keyboard cannot deliver; panel-switch announcement unmeasured |
| Keyboard-only | **HIGH** | 2 of 3 tabs unreachable (measured); Enter irrecoverably removes the tablist from the tab order; no focusable panel |
| Low vision | **MEDIUM** | Ratios computable but rest on an undeclared background; unwrapped flex tablist is a 1.4.10 reflow risk; magnifier user cannot move focus into content |
| Cognitive | **MEDIUM** | Interaction model diverges by input method; destructive action with no warning, message, or undo |
| Vestibular & motion | **LOW** | Single 200ms color transition; no movement, autoplay, or flashing |
| Auditory access | **LOW** | No media elements of any kind |
| Environmental contrast | **MEDIUM** | Page background never declared; forced-colors behavior of the selected-state border unverified (mitigated by the `font-weight` channel) |

**Escalation**: Screen reader and Keyboard-only are HIGH; Low vision, Cognitive, and Environmental contrast are MEDIUM. All five qualify for deep review via `/perspective-audit`. My recommendation is to defer that audit until Findings 1–3 are fixed — a perspective audit run against a widget whose keyboard layer does not exist will spend its budget re-deriving Finding 2 from five angles.

---

## Realist Check (Phase 8 — severity calibration)

**Finding 1 (Enter/Space → index -1) — CRITICAL, held.**
Realistic worst case: a keyboard user presses the most natural activation key on the control they are focused on, and all content in the component vanishes with no recovery path short of a mouse or a reload. Impacted: keyboard and screen reader users, 100% of them, on their first interaction. Detection in production: **days to never** — mouse QA never reproduces it, axe cannot see it (nothing is statically wrong; the defect only exists after an event), and the visual result reads as "the tabs are broken" rather than "accessibility bug," so it may be triaged to the wrong queue. This is complete access loss, which the recalibration rules place off-limits for downgrade. Held at CRITICAL.

**Finding 2 (no arrow keys) — CRITICAL, upgraded from the MAJOR the protocol's own example suggests.**
The protocol's Severity Scale offers "custom tabs with aria-selected but no arrow key navigation" as a MAJOR *example*. I am departing from it deliberately, and the reason is the roving tabindex: in the protocol's implied case, Tab still walks every tab and arrow keys are a missing convenience — genuinely MAJOR. Here `tabIndex={-1}` has already removed that fallback, so the missing arrow keys are the *only* route to 2 of 3 tabs. Measured: focus does not move (steps 0002–0003) and Tab exits to `body` (step_0004). Impacted: keyboard, screen reader, switch, and voice users. Detection: **never by automation** — axe reports no violation here, because every attribute is correct. Content is entirely inaccessible to a user category. Complete access loss again, no downgrade permitted. CRITICAL.

**Finding 3 (tabpanel not focusable) — MAJOR, and I am flagging my own uncertainty.**
This is the one rating I would most expect a developer to push back on, and they would have a point. Standalone realistic worst case: a keyboard user cannot place focus in the panel; document scrolling still works; the content is readable. That is friction with a workaround → **MINOR** by the rules. I am holding MAJOR only on the compounding argument that it removes the last keyboard landing spot in a widget that has one, which is what lets step_0004 jump to `body`. **Explicit note: once Finding 2 is fixed, re-rate this to MINOR.** Flagging rather than quietly holding, because "MAJOR that is really MINOR under a condition that will shortly be true" is exactly the review-momentum inflation Phase 8 exists to catch.

**Finding 4 (announcement unmeasured) — MAJOR, held, but against the evidence not the code.**
No user is harmed by an untested behavior; they are harmed by an untested behavior that turns out to be broken. What justifies MAJOR is that this is the one behavior in the widget that cannot be resolved by reading, the evidence set has no instrument for it, and the fix for Findings 1–2 will change it. Shipping without measuring it means shipping the widget's screen-reader experience on faith.

**Explicitly considered and NOT filed** (recorded so the exclusions are auditable, since a critic that flags everything is indistinguishable from one that is thorough):

| Candidate | Why not filed |
|---|---|
| Missing `prefers-reduced-motion` on `transition: color 0.2s` | A color interpolation is not motion animation. No movement, scale, or parallax. |
| Missing `aria-orientation="horizontal"` on the tablist | `horizontal` is the **default** value for `role="tablist"`. Adding it is redundant, not a fix. |
| `role="tab"` on `<button>` "overriding native semantics" | This is the APG-sanctioned construction — ARIA enhancing a native element, not replacing one. Correct as built. |
| `display: none` / `hidden` double-hiding of panels | Redundant but harmless and defensively correct: `tabs.css:50-51` guards against UA-stylesheet override of `[hidden]`. Both remove the panel from the AX tree, which is the desired outcome. |
| Focus-appearance / 2.4.13 finding | AAA criterion; the corpus rows describing it belong to 19 *other* components; and this component's 3px/2px-offset outline at ~5.6:1 would likely clear the bar. |
| Any 4.1.3 live-region finding | No live region exists or is needed under automatic activation with focus retained on the tab. The corpus's 4.1.3 rows are other components, and batch-crawl 4.1.3 rows are never failure evidence regardless. |
| Missing heading / landmark / skip link | Page-scope concerns. A reusable widget should not invent them. The corpus rows carrying these belong to other components. |
| Tablist not marked up as `<ul>/<li>` | The APG Tabs pattern does not use list semantics; `role="tablist"` supplies the set relationship, and `set size 3` proves it computed. |

---

## Self-Audit (Phase 9)

| # | Finding | Confidence | Developer could refute? | Gap or preference? | Disposition |
|---|---|---|---|---|---|
| 1 | Enter/Space → index -1 | **HIGH** | NO — two string expressions, same file | GAP | Keep, CRITICAL |
| 2 | No arrow keys + inert roving tabindex | **HIGH** | NO — source + corroborating trace | GAP | Keep, CRITICAL |
| 3 | Tabpanel not focusable | **HIGH** on pattern, MEDIUM on severity | PARTIALLY — "real content will have links" is a fair objection | GAP | Keep at MAJOR, flagged for re-rating |
| 4 | Announcement unmeasured | **HIGH** on the coverage gap; no claim on behavior | NO | GAP (in evidence) | Keep, MAJOR |
| — | Flex reflow risk | **MEDIUM** | YES — depends on tab count and container | GAP, conditional | MINOR + "Needs user verification" |
| — | Non-unique ids | **MEDIUM** | YES — depends on consumption | GAP, conditional | MINOR |
| — | Empty/shrinking `tabs` | **MEDIUM** | YES | GAP, conditional | MINOR |
| — | Vague `aria-label` | HIGH on the structural argument | NO | Borderline preference | ENHANCEMENT, not higher |
| — | Missing `Home`/`End` | HIGH | NO | GAP, but APG-optional | ENHANCEMENT, not higher |

Nothing moved to Open Questions on low confidence; the three MEDIUM-confidence items are filed at MINOR **with** their refutation conditions stated inline, which I judge more useful than burying conditional-but-real findings in an unscored section.

---

**Verdict Justification**

**REVISE.** Not ACCEPT-WITH-RESERVATIONS: this must not ship. Two CRITICAL findings each independently deny keyboard and screen reader users access to component content, and one of them is triggered by the single most common keyboard gesture there is.

Not REJECT either, and the distinction is worth being precise about. REJECT would say the approach is unsound and the work should go back to planning. That is not true here. The pattern choice is right (APG Tabs), the element choices are right (native `<button>`, ARIA enhancing rather than replacing), the relationships are right and *measurably* resolve in the AX tree, the tabindex values are right, and the visual state design already satisfies 1.4.1 with three redundant channels. This widget's ARIA layer is better than most. What is absent is its behavior layer — one ref array, one switch statement, one `tabIndex={0}`, and the deletion of a handler that should never have been written because the native element already did its job.

**Recalibrations made** (all recorded above in Phase 8): Finding 2 was **upgraded** from the MAJOR the protocol's own severity example suggests to CRITICAL, on the specific ground that roving tabindex has removed the Tab fallback that makes missing arrow keys a MAJOR elsewhere. Finding 3 is held at MAJOR on a compounding argument only, with an explicit instruction to re-rate it to MINOR once Finding 2 lands. Eight further candidates were considered and not filed, tabulated above with reasons.

**Evidence discipline, stated for the record**: 32 of the 33 artifacts in this evidence pack describe **other components**. I imported nothing from them and named the four highest-risk cross-contamination candidates — including `missing-accessible-name-desktop` on a *tabpanel* in a *different tabs fixture*, which is the near-miss most likely to be laundered into a review of this component. All trace-derived claims are labelled **digest-only** per the evidence-reader contract, because I could not re-fetch at the cited handle; both CRITICAL findings stand on first-tier source evidence without the trace, which merely corroborates them. The `fingerprint` field in the one Evidence Finding block is marked NOT COMPUTED with its derivation recipe rather than filled with a plausible hex string I did not compute.

**To upgrade to ACCEPT**: fix Findings 1 and 2 (delete the Enter/Space branch; add the ref array and arrow/Home/End handler; clamp `activeTab`), fix Finding 3 (`tabIndex={0}` on the panel), then produce measurement that does not exist today — a real-keyboard Playwright transcript showing ArrowRight/ArrowLeft/Home/End moving focus with wrap, an Enter/Space case proving the destructive path is gone, and a `virtual-screen-reader` assertion capturing the panel-switch announcement. Re-review after those exist, not before.

**Open Questions (unscored)**

1. **What is the page background behind this component?** Every contrast ratio in this review — `#666` ≈ 5.74:1, `#0066cc` ≈ 5.57:1, focus outline ≈ 5.57:1 — assumes white. The supplied CSS declares `background: transparent` on the buttons (`tabs.css:14`) and no background anywhere else. On a mid-tone or branded background the inactive `#666` label is the first thing to fail 4.5:1. Concrete check: measure the computed background with the axe `color-contrast` rule against the real page, not from these hex values.
2. **Will panel content ever contain focusable elements?** Determines whether Finding 3's fix is `tabIndex={0}` unconditionally or computed — and whether Finding 3 was ever more than MINOR.
3. **Is `tab.id` a string or a number in real usage?** Does not change Finding 1 (the prefix mismatch fails either way), but determines whether there are one or two defects in that expression, which matters for the regression test.
4. **How many tabs, and how long are the labels, in the widest real deployment?** Resolves the MINOR reflow finding from conditional to filed-or-dropped.
5. **Is more than one `TabsWidget` ever rendered on one page?** Resolves the id-collision MINOR the same way.
6. **Automatic or manual activation?** I have recommended automatic (selection follows focus) because the panels hold a single `<p>` and are trivially cheap to swap. If the panels will later fetch data or render expensively, switch to manual activation — arrows move focus only, Enter/Space selects — which changes the Finding 1 fix from "delete the handler" to "delete the handler and reinstate activation via `onClick` from the native button." Worth deciding before the fix, not after.
7. **`fingerprint` for `tabs-arrow-keys-do-not-move-focus`** is uncomputed. It must be generated by the scorer or harness before this finding enters a tracked evidence set; I deliberately did not fabricate one.
8. **Unresolved scope question inherited from the digest, reported not adjudicated**: whether "the component these artifacts describe" is a coherent framing for an evidence set that pairs one component's driven trace with 32 unrelated components' findings. The digest flagged this and declined to rule. So do I — but I note that the pairing's practical effect on a reviewer is to supply 29 finding rows with real WCAG numbers attached to the wrong component, which is a hazard worth naming whatever the answer is.
