# Accessibility Design Review — `BuggyDropdown`

**VERDICT: REJECT**

**Overall Assessment**: This component has the *vocabulary* of the WAI-ARIA Listbox pattern (`role="listbox"`, `role="option"`, `aria-selected`, `aria-haspopup`, `aria-expanded`, `aria-controls`) and almost none of its *grammar*. The two mechanisms that make a listbox usable by assistive technology — an active-option pointer (`aria-activedescendant` or roving `tabindex`) and focus restoration to the trigger on close — are both absent, and the driven trace measures the consequences directly: pressing ArrowDown repaints 6,555 px² of the screen at 5.67:1 contrast while emitting exactly zero screen-reader phrases (`step_0004`), and pressing Enter to commit a selection drops focus onto `body` (`step_0005`). Separately, and not predicted, the trigger's measured accessible name is `"Sort by"` — the label text only — so the currently selected value is never in the accessibility tree at all: before selection and after selection the announcement is the byte-identical string `"button, Sort by, not expanded, has popup listbox"` (`step_0001`, `step_0006`). A screen-reader user cannot perceive which option they are on, cannot perceive which option they chose, and loses their place in the document when they choose it. That is the core function of the widget, and it does not work.

---

## Phase 0 — Evidence Consumed (and Evidence Refused)

**Evidence type check.** This is a fresh design review of an implementation, not a review of a remediation, so the a11y-test Verification evidence contract's fix/evidence-type match rule does not apply. No "after" artifact is claimed. No axe-core, Pa11y, Playwright `.spec.js`, `agent-browser`, `virtual-screen-reader`, or `a11y-evidence-reader` digest evidence is present in this pack.

**In scope — exactly one artifact.**

| Artifact | Status | Why |
|---|---|---|
| `evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json` | **USED as hard evidence** | `mode: "driven-live"`, `start_url: .../interactive-dropdown-focus-bug.html`, personas `keyboard` + `screen-reader`, 6 steps. Per Phase 0 calibration rule (1), a *driven* session is the tier that produces real announcement evidence; its `sr_announcement` fields are citable. |
| 27 × `evals/results/keyboard-a11y-tester/findings/*.json` | **REFUSED — out of scope** | Every one carries a `url` for a *different* page (`accordion-no-region-role.html`, `app-focus-order-illogical.html`, `tabs-incomplete-aria-selected.html`, …). None of them is `interactive-dropdown-focus-bug.html`. |

**Trap worth naming explicitly.** All 28 files share `"test_case_id": "127-0-0-1"` and near-identical `generated_at` timestamps, so the *only* field that separates this component's evidence from 27 sibling pages' evidence is `url` / `start_url`. A reviewer who keys on `test_case_id` will merge a `missing-accessible-name` finding from `tabs-incomplete-aria-selected.html`, a `positive-tabindex` finding from `app-focus-order-illogical.html`, and a `no-skip-link` finding from `pagination-no-nav-landmark.html` into this dropdown. None of those are findings against this component. There is also a decoy near-name: `findings/interactive-dropdown-clean.json` (`findings: []`) is the **clean sibling fixture**, a different page — its empty result is not a clean bill of health for the component under review.

**Coverage gap in the evidence.** There is **no** `deterministic-findings.json` and **no** `screen-reader-census.json` for `interactive-dropdown-focus-bug.html` in this pack. So there are zero tool-adjudicated findings for this component; every measured claim below is read off raw trace steps and cross-checked against source. The driven trace also exercised only one path (Tab → Enter → Tab → ArrowDown → Enter → Shift+Tab). **Escape was never pressed.** Any Escape-path claim below is labeled as source-derived, not measured.

**Instrument skepticism (two artifacts I will not over-read).**

1. `focus_visible.visible: true` at `step_0001` and `step_0003` is a *computed-style* claim (`style_cue: true`, `pixel_cue: false`, `changed_area: 0`) — the pixel differ saw nothing. It means "an `outline: auto 1px rgb(0,95,204)` is declared," not "a human perceived an indicator." I therefore do **not** assert that 2.4.7 Focus Visible passes on measured grounds.
2. `step_0004`'s `focus_appearance` "passes" (`area_pass: true`, `contrast 5.67`, `aaa_pass: true`) only because the differ credited the moving `.selected` row highlight as the listbox's focus indicator. It is not. That row highlight is the *selection* repaint. Treating `step_0004` as evidence of a good focus indicator would be a measurement artifact; I use its `changed_area: 6555` for what it actually proves — that a large, high-contrast **visual** state change occurred — and pair it with the empty `new_phrases` array in the same step.

Calibration rules (2) and (3) from the Phase 0 contract are noted but not load-bearing here: no file inputs are involved, and the trace carries a `goals[].intent` but no journey-level verdict field, so there is no judgment-layer claim to accept or reject.

**Scope declaration.** This is a **component-scope** review. WCAG-EM citations and ICT Testing Baseline test IDs are deliberately absent — they belong to audit scope only, and an EM or baseline citation here would itself be a defect in this output. Section 508 is not a declared scope for this engagement; `section_508_fpc_context` is `not in scope` throughout. (If scope later changes: 1.3.1, 2.4.3, and 4.1.2 map to the WCAG 2.0 A/AA federal floor; 2.5.8 and 2.4.13 are WCAG 2.1/2.2-only and must not be labeled Section 508 failures.)

---

## Phase 1 — Pre-commitment Predictions

Before reading the source, for a "custom dropdown/select" the protocol predicts a specific failure family. My five:

1. **Focus does not restore to the trigger** after Escape and/or after selection — the popup unmounts while focused and focus falls to `body`.
2. **Arrow-key navigation is visual only** — no `aria-activedescendant`, no roving `tabindex`; `aria-selected` is being used as if it were a focus pointer.
3. **The selected value is not announced** when it changes.
4. **The options container is not named** and/or `aria-controls` dangles while collapsed.
5. **A React timing bug in the open path** — a `.focus()` call fired synchronously against a ref for an element that has not been committed yet.

All five confirmed. Reconciliation and the three things I did **not** predict are in Phase 10.

---

## Phase 2 — Semantic HTML Audit

- **Native-first violation (non-negotiable rule).** `BuggyDropdown.jsx:53-72` hand-rolls a value-selecting dropdown out of `<ul>`/`<li>` + ARIA. Nothing in this component requires custom option rendering: no per-option icons, no grouping, no multi-line option content, no custom filtering. A native `<select>` would supply the active-option pointer, value announcement, focus restoration, mobile pickers, forced-colors rendering, and type-ahead for free — all of which are missing or broken below. Reported as a MAJOR architectural finding (M1), not as a separate CRITICAL, to avoid double-counting the user impact already carried by C1–C3.
- **Interactive elements.** The trigger is a real `<button>` (`:42-51`) — correct, and the reason `Enter` works at all (`step_0002` measured `expanded: false → true`). Acknowledged, not a finding.
- **`<label for>` on a `<button>`** (`:41`). `button` *is* a labelable element per HTML, so this is not invalid markup — but its measured effect is destructive and is written up as C3: Chromium computed `name: "Sort by"` via `labelledby` (`step_0001`, `relatedNodes[0].text: "Sort by"`) while the button's own `text` is `"Newest▼"`. The label wins; the value disappears.
- **List semantics.** `<ul role="listbox">` / `<li role="option">` is the APG's own example markup for a listbox. Overriding the list role here is correct, not a semantics-masking red flag. Not a finding.
- **Headings, landmarks, tables, forms.** The trace reports `region: {landmark: null, heading: null}` on every step. This is a single-component fixture page; page-shell landmark/heading structure is **not** this component's responsibility and I am not flagging it. (Over-flagging component fixtures for missing page shells is a known false-positive class in this suite.)
- **`aria-hidden="true"` on the `▼` glyph** (`:50`) is correct — it prevents "black down-pointing triangle" being spoken alongside a state already carried by `aria-expanded`. Explicitly right; acknowledged.

---

## Phase 3 — ARIA Pattern Compliance Audit

**Which pattern applies.** A button that opens a list of mutually exclusive values and writes the chosen one back into the button is, in ARIA 1.2 terms, the APG **Select-Only Combobox** pattern (`role="combobox"` on the trigger, `aria-expanded`, `aria-controls` → a `role="listbox"` popup, `aria-activedescendant` on the combobox pointing at the active `role="option"`, options carrying `id`s). This code instead uses the ARIA-1.1-era `button` + `aria-haspopup="listbox"` hybrid and then implements neither pattern's option-tracking machinery.

Checked against the APG **Listbox** pattern requirements:

| APG requirement | Present? | Evidence |
|---|---|---|
| `role="listbox"` on container | Yes | `:56`; `step_0003` `role: "listbox"` |
| `role="option"` on each child | Yes | `:64` |
| `aria-selected` on options | Yes | `:65` |
| Listbox has an accessible name | **No** | `step_0003` `name: ""`; SR heard `"listbox, orientated vertically"` |
| Active option tracked (`aria-activedescendant` **or** roving `tabindex`) | **No** | Neither appears anywhere in `:53-72` |
| Options carry `id`s (required for activedescendant) | **No** | `:62-70` |
| Focus returns to trigger on close | **No** | `:18`, `:24`; `step_0005` → `body` |
| `Home` / `End` / type-ahead | **No** | `:21-37` handles only Escape/ArrowDown/ArrowUp/Enter |
| Space activates | **No** | `:33` handles `Enter` only |

**ARIA values are valid.** `aria-expanded` is a real boolean bound to state (`:45`) and the trace confirms it tracks correctly in both directions (`false` at `step_0001` → `true` at `step_0002` → `false` at `step_0006`). `aria-selected` is a real boolean. `aria-haspopup="listbox"` is a legal token. No invalid-value findings — say so rather than manufacture one.

**`aria-controls` dangles while collapsed** (`:46`): `#dropdown-list` does not exist when `isOpen` is false. Measured behavior is benign — Chromium simply omits `controls` from the collapsed AX node (`step_0001` states have no `controls` key) and populates it when expanded (`step_0002`: `"controls": "dropdown-list"`). No user impact; ENHANCEMENT at most.

**The pattern is roughly 55% implemented.** Everything a DOM-inspecting linter can see is present. Everything that makes the interaction legible to AT is missing.

---

## Phase 4 — Focus Management Review

The measured focus path, step by step:

| Step | Key | Active element | `focus_moved` | Read |
|---|---|---|---|---|
| 0001 | Tab | `#dropdown-btn` | true | Trigger reached normally |
| 0002 | Enter | `#dropdown-btn` | **false** | List opened; **focus did not move into it** |
| 0003 | Tab | `#dropdown-list` | true | Popup is a second tab stop |
| 0004 | ArrowDown | `#dropdown-list` | false | Correct (container-level nav) — but nothing points at the active option |
| 0005 | Enter | **`body`** | true | **Focus destroyed on commit** (`is_body: true`, `dom_order_index: -1`) |
| 0006 | Shift+Tab | `#dropdown-btn` | true | Recovery only because this is the first control on a near-empty page |

**Open path (`:8-13`).** `handleToggle` calls `setIsOpen(!isOpen)` then immediately tests `if (!isOpen && listRef.current)`. Two independent defects stacked: `isOpen` is the pre-update value captured in the closure, and `listRef.current` is `null` because the `<ul>` is conditionally rendered (`:52`) and React has not committed the new tree yet. The `.focus()` at `:11` can never fire on the opening transition. `step_0002` measures exactly that: `focus_moved: false`.

**Close path (`:18` and `:24`).** Both `handleSelect` and the Escape branch set `isOpen` false, which unmounts the `<ul>` that currently holds focus. Neither restores focus. `step_0005` measures the selection path landing on `body`. The Escape path was never exercised by the trace but shares the identical unmount-without-restore mechanism (source-derived, HIGH confidence).

**Tab order.** `tabIndex="0"` on the popup (`:58`) inserts an extra tab stop. Under the APG combobox pattern, Tab while the popup is open should close it and move on; here Tab *enters* it. It only appears to "work" as a fallback because the open-path focus move is broken.

**No keyboard trap** — Tab and Shift+Tab both escape (`step_0003`, `step_0006`). 2.1.2 passes; do not inflate.

**Focus indicator.** Computed style is the UA default in all steps: `outline: auto 1px rgb(0, 95, 204)`, offset 0. Against WCAG **2.4.13 Focus Appearance (Level AAA)** the trigger measures `contrast 2.98` (`step_0002`) and `2.53` (`step_0006`) — both under the 3:1 bar — with `area_pass: false` at `step_0002` (367 px² changed vs a 379 px² reference perimeter). 2.4.13 is **AAA**, therefore this is *not* an AA conformance failure against the project's WCAG 2.2 AA target, and I am filing it as MINOR, not MAJOR.

WCAG in play: **2.4.3 Focus Order (A)** — violated on the close path; **2.1.1 Keyboard (A)** — satisfied for operability but the open path requires an undiscoverable extra Tab; **2.1.2 (A)** — satisfied; **2.4.7 Focus Visible (AA)** — probably satisfied, unverified perceptually (see Phase 0); **2.4.13 (AAA)** — measured below bar.

---

## Phase 5 — State Communication Audit

Three states exist in this component: expanded/collapsed, which-option-is-active, and which-option-is-selected. Two of the three never reach assistive technology.

- **Expanded/collapsed** — programmatic and correct (`:45`; measured `false → true → false`). The trace shows no announcement fired at `step_0002`, but a state mutation on the *already-focused* element is exactly the case an emulated SR is weakest at modeling, so I am **not** filing that silence as a finding. Moved to Open Questions for real-AT verification.
- **Active option** — nothing. No `aria-activedescendant`, no roving `tabindex`, no option `id`s. `step_0004` is the proof in both directions in a single step: `changed_area: 6555` px² repainted at `contrast: 5.67` (a large, high-contrast **visual** change) alongside `sr_announcement.new_phrases: []` and `focus_announcement: null`. This is the textbook visual-only state indicator, and unusually, both halves of it are measured.
- **Selected value** — never in the accessible name. `step_0001` and `step_0006` return the identical `focus_announcement` string, `"button, Sort by, not expanded, has popup listbox"`, while the rendered `text` changed from `"Newest▼"` to `"Price: low to high▼"`. The selection is visible and inaudible.
- **Loading / error / disabled / readonly** — none exist in this component. Not applicable; no manufactured findings.
- **Live regions** — none, and **none should be added**. See the "wrong fix" warning in Phase 7.

WCAG in play: **4.1.2 Name, Role, Value (A)** — the "Value" clause fails twice (active option, selected value); **4.1.3 Status Messages (AA)** — not applicable, because the correct fix is an active-descendant pointer, not a broadcast.

---

## Phase 6 — Multi-Perspective Review

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | **HIGH** | Custom listbox with no active-option pointer; value absent from accessible name; measured silence on the only two state changes that matter (`step_0004`, `step_0005`) |
| Keyboard-only | **HIGH** | Focus destroyed to `body` on commit (`step_0005`); focus never enters popup on open (`step_0002`); Escape handler unreachable from the default focus position |
| Low vision | **MEDIUM** | Focus indicator measured 2.53–2.98:1; active/selected distinction may be color-only (CSS not supplied); trigger measures 21 px tall |
| Cognitive | **MEDIUM** | Arrowing mutates the displayed value before commit; Escape leaves the button displaying a value the parent never received |
| Vestibular & motion | **LOW** | No animation, transition, parallax, or autoplay in source (CSS not supplied — see Open Questions) |
| Auditory access | **LOW** | No media elements |
| Environmental contrast | **MEDIUM** | Selected-state indication is a bare class name (`:67`) with no supplied stylesheet; forced-colors behavior unverifiable |

Screen reader, keyboard-only, low vision, cognitive, and environmental contrast are at MEDIUM or HIGH and should be escalated to `/perspective-audit`.

---

## Phase 7 — Gap Analysis (What Is Absent)

- `aria-activedescendant` on the focused container, and `id` on every `role="option"` — the single missing mechanism that causes C2.
- Focus restoration on *both* close paths (select and Escape).
- A `useEffect`-based open-path focus move; the current synchronous ref call cannot work.
- An accessible name on the listbox.
- The current value in the trigger's accessible name.
- `Home` / `End` / type-ahead / `Space`, all recommended by the APG Listbox pattern.
- Dismiss-on-outside-click and dismiss-on-focus-loss; the popup can be left open behind the user.
- `Escape` and `ArrowDown` handling **on the trigger**. This is anti-pattern **#4 (else-branch coverage)** from the April 2026 third-party audit list, in its purest form: the key handler is bound to one branch (`:57`, the popup) and the *default measured focus position while open is the other branch* (`step_0002`, the trigger). The Escape affordance exists in code and is unreachable in practice.
- Any DOM/AX-tree verification of the fix. Anti-pattern **#9** applies with unusual force here: the measured evidence already shows Chromium computing an accessible name (`"Sort by"`) that no one reading `:42-51` would predict. Any remediation must be re-measured in the accessibility tree, not accepted on the strength of the diff.

**A warning about the wrong fix.** The obvious-looking remedy for C2/C3 is to bolt an `aria-live` region onto the dropdown so option changes get read out. Do not. That is anti-pattern **#1 (broadcast vs. association)**: the state belongs to a specific element and must be *associated* (`aria-activedescendant` → the option's `id`; value → the trigger's `aria-labelledby`), not broadcast. A live region here produces double-speaking on every arrow press and still leaves the accessibility tree wrong.

**Known false positives I checked and am not filing.** `aria-controls` dangling while collapsed (measured benign). Missing landmarks/headings (page-shell, not component). `jsx-a11y/no-noninteractive-element-interactions` on `<li onClick>` (`:66`) — the element carries `role="option"` inside a `role="listbox"`, which is the APG's own markup; the container handles keys, so this is not a keyboard gap. The 27 sibling `findings/*.json` files in their entirety, including their `sr-live-region-silent` rows — which are batch-crawl 4.1.3 rows, i.e. per calibration rule (1) prompts to run a driven session and never failure evidence, and which in any case belong to other URLs and to components that *have* live regions, unlike this one.

---

## Phase 8 — Realist Check (Severity Calibration)

**C1 (focus to `body` on commit).** Realistic worst case: on this near-empty fixture the user recovers with one Shift+Tab (`step_0006`). On a real page with the dropdown mid-document, `body` focus means the next Tab restarts from the top of the document. For the screen-reader user the loss compounds — the virtual cursor resets *and* the value change is unannounced, so they cannot confirm the selection happened at all. Impacted: keyboard + screen reader. Detection in production: days-to-never (silent; automated tools cannot see it — no findings row exists for this page). **CRITICAL survives** as the combined selection-path failure, on the grounds that the task "choose an option and know you chose it" cannot be completed by a screen-reader user, and no workaround restores that information.

**C2 (silent arrow navigation).** Worst case: the screen-reader user presses ArrowDown and receives nothing. There is no alternative channel — no announcement, no focus move, no live region. Impacted: screen reader (total), low vision using magnification (partial — the highlight is off-viewport-center). **CRITICAL survives**; this is complete loss of the widget's core function for a user category, which the recalibration rules explicitly forbid downgrading.

**C3 (value absent from accessible name).** Worst case: the user can never learn the dropdown's current value, before or after interacting. Byte-identical announcements at `step_0001` and `step_0006` prove it across a state change. Impacted: screen reader, speech-recognition users targeting by name. **CRITICAL survives.**

**Downgraded: open-path focus move (was CRITICAL → now MAJOR M2).** *Mitigated by:* Tab reaches the popup (measured, `step_0003`), so the widget remains operable by keyboard; the failure is disorientation and an undiscoverable extra step, not access loss. It stays MAJOR rather than MINOR because it is what strands the user on an element where Escape is not handled.

**Downgraded: 2.4.13 focus appearance (was MAJOR → now MINOR N1).** *Mitigated by:* 2.4.13 is Level AAA and the project target is WCAG 2.2 AA; a visible UA outline is declared in computed style at every step. Reporting a AAA shortfall as a MAJOR against an AA target would be severity inflation.

**Downgraded: 2.5.8 target size (was MAJOR → now MINOR N2).** *Mitigated by:* the spacing exception appears to be met on the measured geometry — see the arithmetic in N2 — and the shortfall is 3 px.

---

## Phase 9 — Self-Audit

| Finding | Confidence | Refutable with dev context? | Gap or preference? |
|---|---|---|---|
| C1 focus to `body` | HIGH | No — measured `step_0005` | GAP |
| C2 silent arrow nav | HIGH | No — measured silence **plus** structural absence in source | GAP |
| C3 value not in accessible name | HIGH | Partly — see below | GAP |
| M1 native `<select>` available | MEDIUM | **Yes** — product requirements not supplied | GAP (architectural) |
| M2 open-path focus | HIGH | No — measured `step_0002` + source | GAP |
| M3 listbox unnamed | HIGH | No — measured `name: ""` | GAP |
| M4 Escape unreachable from trigger | HIGH | No — source + measured focus position | GAP |
| M5 value/state desync on Escape-after-arrow | HIGH | No — pure source reading | GAP |
| N1 focus appearance (AAA) | HIGH | No | GAP (informative) |
| N2 target size | MEDIUM | Yes — fixture styling | GAP (conditional) |

C3 carries one caveat that keeps it honest without demoting it: the name-from-`<label>` precedence for `<button>` is the *measured Chromium* result, and other engines may instead compute name-from-contents. I keep it CRITICAL because **both** outcomes fail: if the label wins, the value is absent; if contents win, the value is conflated into the *name* rather than exposed as a value, and either way the post-selection change goes unannounced because focus is on `body`. The fix is identical under both.

M1 is the one finding a developer could legitimately refute with requirements I do not have. It stays as a MAJOR recommendation rather than a blocking defect, and its impact is explicitly *not* additive to C1–C3.

Moved to Open Questions: the `step_0002` expansion silence; all CSS-dependent claims.

---

## Critical Findings (blocks access)

> Note on the evidence blocks below: `fingerprint` values are **author-assigned placeholders**, not recomputed digests. They must be regenerated by the evidence pipeline before these findings are filed or trended. I have not verified them and do not present them as stable hashes.

**C1. Focus is destroyed on every close — the popup unmounts while holding focus and nothing restores the trigger.**

`BuggyDropdown.jsx:15-19` (`handleSelect`) and `:22-24` (Escape branch) both call `setIsOpen(false)`, unmounting the `<ul>` at `:52-73` that currently has focus. Neither stores or restores a focus target. Measured: `trace.json step_0005` — keystroke `Enter`, `active_element_selector: "body"`, `tag: "body"`, `is_body: true`, `dom_order_index: -1`, `focus_moved: true`, `sr_announcement.new_phrases: []`. Recovery at `step_0006` (Shift+Tab back to `#dropdown-btn`) succeeds only because this fixture page has no other content.

- **User group**: keyboard-only, screen reader
- **WCAG / APG**: 2.4.3 Focus Order (Level A); WAI-ARIA APG Listbox / Select-Only Combobox — "when the listbox is dismissed, focus returns to the combobox"
- **Confidence**: HIGH (selection path measured; Escape path source-derived from the identical mechanism)
- **Why this matters**: A sighted keyboard user is thrown to the top of the document on every selection. A screen-reader user loses their reading position *and* gets no confirmation the selection occurred — the combination of C1 and C3 means the task cannot be completed with confidence.
- **Fix**: capture the trigger before closing and restore after the DOM settles, on **both** paths:
  ```jsx
  const btnRef = useRef(null);
  const close = () => { setIsOpen(false); setTimeout(() => btnRef.current?.focus(), 0); };
  ```
  Call `close()` from `handleSelect` and from the Escape branch. The `setTimeout(0)` is not decoration — a synchronous `focus()` issued during the same commit that unmounts the popup is dropped by React.

```
### A11y Evidence Finding
finding_id: dropdown-focus-lost-to-body-on-close
fingerprint: PLACEHOLDER-a11y-c1-focus-body
source: evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json steps[4] (step_0005); BuggyDropdown.jsx:15-19, :22-24
wcag_or_apg: WCAG 2.2 SC 2.4.3 Focus Order (Level A); WAI-ARIA APG Select-Only Combobox / Listbox dismissal behavior
section_508_fpc_context: not in scope (component-scope review; no declared Section 508 engagement)
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, keyboard=HIGH, low-vision=MEDIUM, cognitive=MEDIUM
evidence: step_0005 keystroke_sent="Enter" -> active_element_selector="body", tag="body", is_body=true, dom_order_index=-1, focus_moved=true, computed_focus_style=null
reproduction_steps: Tab to #dropdown-btn; Enter to open; Tab into #dropdown-list; ArrowDown; Enter to commit; observe document.activeElement
expected_behavior: On dismissal (selection or Escape), focus returns to #dropdown-btn
actual_behavior: Focus lands on body with no indicator and no announcement; recovery requires Shift+Tab
trend: new
```

**C2. Arrow-key navigation is a visual-only state change — no `aria-activedescendant`, no roving tabindex, no option `id`s.**

`BuggyDropdown.jsx:25-32` mutates `selectedIndex` on ArrowDown/ArrowUp. The only consequences are `aria-selected` at `:65` and the `.selected` class at `:67`. Focus stays on the container (`:58`) and nothing tells AT which option is active. Measured: `trace.json step_0004` — keystroke `ArrowDown`, `focus_moved: false`, `sr_announcement.new_phrases: []`, `focus_announcement: null`, while `focus_appearance.changed_area: 6555` px² at `contrast: 5.67`. The silence is corroborated structurally, not merely observed: `aria-activedescendant` and option `id` appear nowhere in `:53-72`.

- **User group**: screen reader (total loss of the widget's core function)
- **WCAG / APG**: 4.1.2 Name, Role, Value (Level A); WAI-ARIA APG Listbox — "if the listbox has focus, `aria-activedescendant` refers to the focused option"
- **Confidence**: HIGH
- **Why this matters**: The user presses ArrowDown three times and hears nothing at all. They cannot tell where they are in the list, how long the list is, or what they are about to commit. Meanwhile 6,555 px² of the screen changes at better than 5:1 contrast for everyone else. This is the exact shape the critic exists to catch: every attribute a linter inspects is present, and the interaction is inoperable.
- **Fix**: give each option a stable `id` and point the focused container at the active one:
  ```jsx
  <ul role="listbox" tabIndex={-1} aria-activedescendant={`opt-${activeIndex}`} …>
    <li id={`opt-${index}`} role="option" aria-selected={index === selectedIndex} …>
  ```
  Track `activeIndex` (which option has virtual focus) separately from `selectedIndex` (which is committed) — see M5. Do **not** substitute an `aria-live` region.

```
### A11y Evidence Finding
finding_id: dropdown-listbox-no-activedescendant-silent-arrow-nav
fingerprint: PLACEHOLDER-a11y-c2-activedescendant
source: evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json steps[3] (step_0004); BuggyDropdown.jsx:25-32, :53-72
wcag_or_apg: WCAG 2.2 SC 4.1.2 Name, Role, Value (Level A); WAI-ARIA APG Listbox (aria-activedescendant)
section_508_fpc_context: not in scope (component-scope review; no declared Section 508 engagement)
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, keyboard=MEDIUM, low-vision=MEDIUM, cognitive=MEDIUM
evidence: step_0004 keystroke_sent="ArrowDown", active_element_selector="#dropdown-list", focus_moved=false, sr_announcement.new_phrases=[], focus_announcement=null, focus_appearance.changed_area=6555, contrast=5.67; source has no aria-activedescendant and no option id
reproduction_steps: Open the dropdown, place focus on #dropdown-list, press ArrowDown, capture the screen-reader phrase log
expected_behavior: Each arrow press announces the newly active option and its position (e.g. "Price: low to high, 2 of 3")
actual_behavior: Zero phrases emitted; only a visual row highlight moves
trend: new
```

**C3. The trigger's accessible name is the label text only — the selected value is never exposed, before or after selection.**

`BuggyDropdown.jsx:41` associates a `<label>` with the `<button>`, and `:49` renders the current value as button *text content*. Measured in Chromium: `step_0001` `ax_name_role_state.name: "Sort by"`, `states.labelledby.relatedNodes[0].text: "Sort by"`, while the element's rendered `text` is `"Newest▼"`. After committing a different option, `step_0006` reports `text: "Price: low to high▼"` and a `focus_announcement` that is **byte-identical to step_0001**: `"button, Sort by, not expanded, has popup listbox"`.

- **User group**: screen reader; speech-recognition users targeting controls by name
- **WCAG / APG**: 4.1.2 Name, Role, Value (Level A) — the Value clause; WAI-ARIA APG Select-Only Combobox naming (`aria-labelledby="<label-id> <value-id>"`)
- **Confidence**: HIGH on the failure; MEDIUM on the *mechanism* being label-precedence specifically (other engines may compute name-from-contents — but both outcomes fail, see Phase 9)
- **Why this matters**: The user cannot answer "what is this sorted by right now?" at any point in the interaction. Combined with C1 (focus is on `body` at the moment of commit) and C2 (no per-option announcement), the entire selection round-trip is inaudible from start to finish.
- **Fix**: replace the `<label for>` with an explicit two-part name so the value is part of the accessible name and re-announced when the user returns to the control:
  ```jsx
  <span id="dropdown-label">{label}</span>
  <span id="dropdown-value">{options[selectedIndex]}</span>
  <button id="dropdown-btn" aria-labelledby="dropdown-label dropdown-value" …>
  ```
  Then verify in the browser's accessibility tree (anti-pattern #9) that the computed name is `"Sort by Price: low to high"` — do not accept the diff as proof.

```
### A11y Evidence Finding
finding_id: dropdown-trigger-value-not-in-accessible-name
fingerprint: PLACEHOLDER-a11y-c3-name-value
source: evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json steps[0] (step_0001) and steps[5] (step_0006); BuggyDropdown.jsx:41, :49
wcag_or_apg: WCAG 2.2 SC 4.1.2 Name, Role, Value (Level A); WAI-ARIA APG Select-Only Combobox naming
section_508_fpc_context: not in scope (component-scope review; no declared Section 508 engagement)
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, cognitive=MEDIUM, keyboard=LOW
evidence: step_0001 name="Sort by" / text="Newest▼"; step_0006 name="Sort by" / text="Price: low to high▼"; focus_announcement identical across both steps: "button, Sort by, not expanded, has popup listbox"
reproduction_steps: Focus the trigger and capture the announcement; select a different option; return focus to the trigger and capture again; compare
expected_behavior: The accessible name includes the current value and changes when the value changes
actual_behavior: Accessible name is invariant at "Sort by"; the value exists only as visual text
trend: new
```

---

## Major Findings (significantly degrades experience)

**M1. A native `<select>` is available and is being re-implemented in ARIA without the pattern's machinery.**

`BuggyDropdown.jsx:53-72`. Nothing in the component requires custom option rendering — options are plain strings (`:69`), there is no grouping, no icons, no filtering. Every one of C1, C2, C3, M3, and the missing Home/End/type-ahead behaviors are supplied for free by `<select>`, along with mobile native pickers and forced-colors rendering.

- **User group**: all
- **WCAG / APG**: the "native HTML first" rule — ARIA must not be used where equivalent HTML semantics and behavior exist (ARIA in HTML / APG "No ARIA is better than bad ARIA")
- **Confidence**: MEDIUM — a developer could refute this with product requirements I have not been shown
- **Why this matters**: Not additive to the CRITICALs; it is their *root cause*. If custom rendering is genuinely required, the correct target is the APG Select-Only Combobox with `aria-activedescendant`, not this hybrid.
- **Fix**: either replace with `<select>` + `<label>`, or commit fully to the Select-Only Combobox pattern (`role="combobox"` on the trigger, popup `role="listbox"`, `aria-activedescendant`, option `id`s, `Home`/`End`/type-ahead, Tab-closes-popup).

**M2. Focus never enters the popup on open — the `.focus()` call is unreachable.**

`BuggyDropdown.jsx:8-13`. `setIsOpen(!isOpen)` does not update `isOpen` synchronously, so the `!isOpen` guard reads the pre-update value; and `listRef.current` is `null` because the `<ul>` is gated behind `isOpen` at `:52` and has not been committed. Measured: `step_0002` — `Enter`, `expanded: true`, `focus_moved: false`, active element still `#dropdown-btn`.

- **User group**: keyboard-only, screen reader
- **WCAG / APG**: 2.4.3 Focus Order (Level A); APG Listbox opening behavior
- **Confidence**: HIGH
- **Why this matters**: The user opens the list and is not in it. Nothing announces that an extra Tab is required. It also strands them on the one element where Escape is not handled (M4).
- **Fix**: `useEffect(() => { if (isOpen) listRef.current?.focus(); }, [isOpen]);` and delete the ref call from `handleToggle`.

**M3. The listbox has no accessible name.**

`BuggyDropdown.jsx:53-60` — no `aria-label`, no `aria-labelledby`. Measured: `step_0003` `ax_name_role_state.name: ""`; the announcement is `"listbox, orientated vertically"`.

- **User group**: screen reader
- **WCAG / APG**: 4.1.2 Name, Role, Value (Level A); 1.3.1 Info and Relationships (Level A); APG Listbox — the listbox requires an accessible name
- **Confidence**: HIGH
- **Why this matters**: A user landing in the popup via Tab or virtual cursor hears "listbox" with no indication of what it selects. On a page with several dropdowns they are indistinguishable.
- **Fix**: `aria-labelledby="dropdown-label"` on the `<ul>`.

**M4. The Escape handler is bound to the popup only — and the measured default focus position while open is the trigger.**

`BuggyDropdown.jsx:57` attaches `onKeyDown` to the `<ul>`; the Escape branch lives at `:22-24`. But `step_0002` measures focus remaining on `#dropdown-btn` after opening. Escape pressed there does nothing, and no ArrowDown-opens-and-moves-to-first-option behavior exists on the trigger either.

- **User group**: keyboard-only, screen reader
- **WCAG / APG**: 2.1.1 Keyboard (Level A); APG Select-Only Combobox — the combobox itself handles Escape, ArrowDown, ArrowUp, Alt+ArrowDown
- **Confidence**: HIGH
- **Why this matters**: This is anti-pattern #4 (else-branch coverage) exactly: the dismissal affordance was implemented for one branch and the *reachable* branch is the other one. Reviewing `:22-24` in isolation makes Escape look handled.
- **Fix**: hoist key handling to the wrapper at `:40`, or bind `onKeyDown` to the trigger as well, covering Escape (close + restore focus) and ArrowDown/ArrowUp (open + move to first/last option).

**M5. Arrowing mutates the displayed value without committing it; Escape then leaves the button displaying a value the parent never received.**

`BuggyDropdown.jsx:25-32` calls `setSelectedIndex` directly, and `:49` renders `options[selectedIndex]` as the button's text. `onSelect` fires only from `handleSelect` (`:17`). So: open → ArrowDown ×2 → Escape leaves the button reading "Rating" while the parent still holds "Newest". No announcement, no revert.

- **User group**: cognitive (primary), screen reader, all users
- **WCAG / APG**: 4.1.2 Name, Role, Value (Level A) — displayed state diverges from actual value; APG Listbox — distinguish the *active* option from the *selected* option
- **Confidence**: HIGH (pure source reading; the trace never pressed Escape)
- **Why this matters**: The interface lies about its own state, silently, with no way to detect the divergence. For a user relying on the visible text as ground truth, every subsequent decision is made on false information.
- **Fix**: separate `activeIndex` (virtual focus, moved by arrows, drives `aria-activedescendant`) from `selectedIndex` (committed, drives the button text, `aria-selected`, and `onSelect`). Escape resets `activeIndex` to `selectedIndex` and commits nothing.

---

## Minor Findings (friction, workaround exists)

- **N1. Focus indicator measures below the 2.4.13 AAA bar.** Trigger contrast `2.98` (`step_0002`) and `2.53` (`step_0006`), `area_pass: false` at `step_0002` (367 vs 379 px² reference). WCAG **2.4.13 Focus Appearance is Level AAA**, so this is *not* an AA conformance failure against the WCAG 2.2 AA target — it is a perceptibility risk for low-vision users running the UA default `outline: auto 1px`. Fix: an explicit `:focus-visible { outline: 2px solid; outline-offset: 2px; }` with a token meeting 3:1 against both adjacent surfaces. Note: the `step_0004` "pass" is the selection highlight being miscredited as the focus indicator, not evidence of a good indicator.
- **N2. Trigger height measures 21 CSS px, below the 24×24 minimum.** `step_0001` `bounding_box: {width: 73.66, height: 21}`. WCAG **2.5.8 Target Size (Minimum), Level AA**. The spacing exception appears to be satisfied on the measured geometry: trigger centre ≈ y 26.5, first option centre ≈ y 62 (`step_0003` list box `y: 53, height: 54`), a 35.5 px separation against the 24 px circle-diameter test — the circles do not intersect. So this is very likely **not** an AA failure as laid out on this fixture page. It is filed as MINOR / needs-verification because production layouts that place this trigger beside other controls will lose the exception. Fix: `min-height: 24px` (44 px recommended) on the trigger.
- **N3. `tabIndex="0"` on the popup adds a second tab stop** (`:58`). Per the combobox pattern the popup should not be tabbable and Tab should dismiss it. Currently harmless-looking only because it is masking M2. Fix: `tabIndex={-1}` once M2 is fixed, and make Tab close the popup.
- **N4. No dismiss-on-outside-click and no dismiss-on-focus-loss.** Tabbing past the popup leaves it open with `aria-expanded="true"` behind the user; a virtual-cursor user will encounter a dangling open listbox. Workaround exists (re-click the trigger). Fix: `onBlur`/`focusout` on the wrapper with a `relatedTarget` containment check, plus a document pointer-down handler.

---

## Enhancements (best practice not met, no access barrier)

- `Home` / `End` / `PageUp` / `PageDown` and printable-character type-ahead, all recommended by the APG Listbox pattern (`:21-37` handles four keys only).
- `Space` should activate the active option in a listbox; only `Enter` is handled (`:33`).
- `aria-controls="dropdown-list"` at `:46` dangles while collapsed. Measured benign — Chromium drops it from the collapsed AX node (`step_0001`) and populates it when expanded (`step_0002`). Cosmetic; some validators will flag it. Fix if desired: render it conditionally.
- `key={index}` at `:63` is a React-correctness nit with no accessibility consequence; noted only so it is not mistaken for the missing option `id` required by C2.

---

## What's Missing (gaps, unhandled edge cases, unstated assumptions)

- **The active-option pointer.** `aria-activedescendant` + option `id`s. One missing mechanism accounts for the largest single finding in this review.
- **Focus restoration on both close paths** — and a `setTimeout`-deferred one, because React drops focus assignments issued in the same commit that unmounts the focused node.
- **Keyboard handling on the trigger** — the branch the user actually occupies.
- **A distinction between active and selected** — the component has one index doing two jobs (M5).
- **An accessible name on the popup.**
- **The current value in the accessible name.**
- **Any stylesheet.** No CSS was supplied for `.dropdown-wrapper`, `.dropdown-list`, or `.selected`. Therefore: the active/selected indicator may be colour-only (WCAG 1.4.1), forced-colors/high-contrast behaviour is unknown, reflow at 200% zoom is unknown, and `prefers-reduced-motion` coverage is unknown. These are **unassessed**, not clean — do not read their absence from the findings list as a pass.
- **Any test evidence for the fix.** The pack contains no `deterministic-findings.json` for this page and no component-level SR assertions. When the fix lands, the verification must be an AX-tree inspection plus a re-run driven session — a screenshot or a passing unit test would be the wrong evidence type for a focus-and-announcement fix.

---

## Multi-Perspective Notes

**Screen reader user (NVDA / JAWS / VoiceOver).** The measured experience of the full task is: hear `"button, Sort by, not expanded, has popup listbox"`; press Enter and hear nothing; press Tab and hear `"listbox, orientated vertically"` — an unnamed container; press ArrowDown and hear **nothing** (`step_0004`); press Enter and land on `body` with **nothing** announced (`step_0005`); Shift+Tab back and hear the byte-identical string from the beginning (`step_0006`). At no point in the round trip does the user learn which option was active, which was chosen, or that anything changed. Semantic structure exists; state communication does not.

**Keyboard-only user.** Reachable and not trapped — Tab and Shift+Tab both work, so 2.1.2 is fine. But the open path silently requires an extra, unadvertised Tab (M2), the Escape affordance is bound to an element the user is not on (M4), and every selection ejects focus to `body` (C1). The interaction is operable and incoherent.

**Low vision (200% zoom, magnifier, high contrast).** The focus indicator is the UA default measured at 2.53–2.98:1 against the AAA 2.4.13 bar (N1) — visible in computed style, weak in pixels. The 21 px trigger (N2) is small for magnifier-driven pointing. The active-option highlight *is* strong where measured (5.67:1, `step_0004`), which is worth acknowledging. Reflow and forced-colors behaviour cannot be assessed without the stylesheet.

**Cognitive accessibility.** The most under-appreciated defect here is M5: arrowing changes what the button says without changing what the application believes, and Escape does not undo it. The visible interface can end a session asserting a value that was never selected. Add to that the absence of any confirmation that a selection took effect (C1 + C3), and the widget gives the user no reliable way to verify their own action. No timeouts, no destructive actions, no re-entry burden — those parts are fine.

**Vestibular, auditory, environmental contrast.** No motion and no media in the source, so vestibular and auditory are LOW. Environmental contrast sits at MEDIUM only because the stylesheet is missing and the selected state is expressed as a bare class name — colour-only indication (1.4.1) is a live possibility that cannot be confirmed or dismissed from what was supplied.

---

## Phase 10 — Synthesis: Predictions vs. Findings

Four of five pre-commitment predictions landed on their first investigation: focus restoration missing (C1), arrow navigation incomplete with no activedescendant (C2), selected state not announced (C2/C3), popup not named (M3), and the React open-path timing bug (M2). For a "custom dropdown" the prediction list from the protocol was close to a complete map of the defects — which is itself worth noting: this failure family is stereotyped, and a planner consulted before implementation would have caught nearly all of it.

Three things I did not predict:

1. **The accessible name collapsing to the label** (C3). I expected the value to be *announced badly*; I did not expect it to be *absent from the accessibility tree entirely*, and I would not have found it by reading `:41-51` — it took the measured `name: "Sort by"` vs. `text: "Newest▼"` pair to expose it. This is the clearest case in the review of measurement beating code reading.
2. **The state/value desync on Escape-after-arrow** (M5). A correctness bug with an accessibility consequence, invisible to any tool, invisible to the trace (Escape was never pressed), and reachable only by reading the two state paths against each other.
3. **The evidence pack's shape.** 27 of 28 files are about other pages, all sharing this one's `test_case_id`, with a near-name decoy (`interactive-dropdown-clean.json`) and no findings file for the component under review at all. The correct amount of evidence to import from those 27 files is zero.

The single most valuable artifact in the entire pack is one step: `step_0004`, which measures 6,555 px² of high-contrast visual change and an empty announcement array in the same object. That is the visual-versus-programmatic gap, both halves measured, in one place.

---

**Verdict Justification**: REJECT. Three CRITICAL findings, each surviving the Realist Check, and together they mean a screen-reader user cannot perform the widget's only function: choose a value and know they chose it. The remediation is not a patch — it requires an active-option pointer that does not exist, an accessible-name strategy that must be rebuilt, focus restoration on two paths, and a split between active and selected state. That is a re-implementation against the APG Select-Only Combobox pattern, or a replacement with `<select>`.

Recalibrations applied and disclosed: the open-path focus failure was downgraded CRITICAL → MAJOR (mitigated by: Tab reaches the popup, measured `step_0003`, so operability survives); 2.4.13 focus appearance MAJOR → MINOR (mitigated by: AAA criterion against an AA target, with a visible indicator declared in computed style); 2.5.8 target size MAJOR → MINOR (mitigated by: the spacing exception is satisfied on the measured geometry, 35.5 px separation vs. a 24 px circle test).

To upgrade to **REVISE**: fix C1 and C3 — restore focus to the trigger on both close paths, and put the current value into the trigger's accessible name. To upgrade to **ACCEPT-WITH-RESERVATIONS**: additionally fix C2 (`aria-activedescendant` + option `id`s) and M3 (name the listbox), then re-run the driven session and show a non-empty `sr_announcement.new_phrases` on ArrowDown and a non-`body` `active_element_selector` after Enter. To upgrade to **ACCEPT**: complete the APG pattern (Home/End/type-ahead/Space, Tab dismisses, trigger handles Escape and arrows), supply the stylesheet for a contrast and forced-colors pass, and verify the computed accessible name in a real accessibility tree with a real screen reader — not in a diff.

Escalation: Screen reader (HIGH), Keyboard-only (HIGH), Low vision (MEDIUM), Cognitive (MEDIUM), and Environmental contrast (MEDIUM) should go to `/perspective-audit`.

---

**Open Questions (unscored)**

1. **Is the `aria-expanded` change announced by a real screen reader?** `step_0002` shows `new_phrases: []` on the open transition. A state mutation on the *already-focused* element is precisely where an emulated SR is least reliable, so I am not filing this as a finding. Verify with real NVDA/JAWS/VoiceOver before treating it as either a defect or a pass.
2. **Which accessible-name computation wins for `<button>` with an associated `<label>` outside Chromium?** The measured result is label-precedence. Firefox and WebKit may compute name-from-contents instead. C3's fix is correct under both, but the *diagnosis wording* should be re-verified cross-browser before it goes into a bug report.
3. **What does the stylesheet do?** No CSS was supplied. Colour-only selected state (1.4.1), 200% reflow (1.4.10), forced-colors survival, focus-indicator tokens, and `prefers-reduced-motion` are all unassessed. Request `.dropdown-wrapper`, `.dropdown-list`, and `.selected` before signing off on the low-vision and environmental-contrast perspectives.
4. **Is custom rendering actually required (M1)?** If the product requirement is a plain list of string options, `<select>` is the correct answer and most of this review disappears. This is the one finding a developer can refute with context I do not have.
5. **How is this component used on a real page?** The trace ran on a near-empty fixture, which is why Shift+Tab recovered from `body` in one keystroke (`step_0006`) and why the 2.5.8 spacing exception held (N2). Both mitigations may evaporate in production layout.
6. **Does `onSelect` have side effects that constitute a context change?** If selecting re-sorts or navigates, 3.2.1/3.2.2 come into play on top of C1's focus loss. Not visible from the component alone.
