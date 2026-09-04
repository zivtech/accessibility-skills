# Accessibility Design Review — `BuggyDropdown` (custom collapsible listbox)

**VERDICT: REJECT**

**Citation convention:** line numbers below are relative to the component source as supplied in the fixture, where line 1 = `import React, { useState, useRef } from 'react';`. The fixture prompt's own numbering is offset by +7 (my line 1 = prompt line 8). Path is written as `BuggyDropdown.jsx` for readability; substitute the real path when filing.

**Overall Assessment**: This widget has the *vocabulary* of an accessible listbox (`aria-haspopup`, `aria-expanded`, `aria-controls`, `role="listbox"`, `role="option"`, `aria-selected`) and almost none of the *mechanics*. Three separate failures each independently break the control for screen reader users: focus is dropped to `<body>` on selection and never restored, arrow-key navigation produces no assistive-technology-observable change of any kind, and the chosen value never reaches the trigger's accessible name — the button announces the identical string before and after a selection. The measured driven trace corroborates all three at the step level. This is the canonical "80% of an ARIA pattern" case: the attributes that are visible in the DOM are present; the ones that make the interaction coherent for AT are absent.

---

## Phase 0 — Test Evidence Consumed

**Review type:** fresh design pass, not a fix verification. The a11y-test Verification-evidence-contract gate (evidence-type-vs-claim mismatch on a remediation) therefore does not fire. No remediation claim is attached to this artifact.

**Evidence supplied:** one CURATED evidence digest (`def_rev: 2026-08-26a`) reporting five observations plus two absence claims from `evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json` (6 steps, driven-live mode, personas keyboard + screen-reader, viewport 1280×800, `start_url=http://127.0.0.1:8777/interactive-dropdown-focus-bug.html`).

**Evidence tier — this is load-bearing for how the findings below are labeled.**

Per the Phase 0 digest rule, an `a11y-evidence-reader` digest is *detector output, one tier below the artifact it cites* — a paraphrase, not the hard evidence. The rule requires re-fetching at the cited handle before a finding rests on a digest line. **I was given the digest, not the trace, and could not re-fetch.** Therefore:

- **Every trace-derived evidence line in this review is labeled `digest-only`.** Each carries its handle (`file :: step_id`) and, where useful, the exact `jq` to close the gap.
- **No CRITICAL below rests solely on digest-only evidence.** The component source was supplied verbatim and is first-party, full-tier evidence; the code-read establishes each CRITICAL on its own, and the trace corroborates. The one place where the digest changes a *severity* rather than merely confirming it is C3 — flagged explicitly there, with its downgrade condition stated.

**Instrument-class mismatch, reported rather than papered over.** The digest's own "Not claimed" section is correct and I am adopting it: the `sr_announcement` and `ax_name_role_state` fields are keyboard-a11y-tester's simulated capture, not `virtual-screen-reader` assertion output (the contract's prescribed instrument for the `name-role-state` class), and this is a driven-live trace rather than the prescribed `npx playwright test` transcript for the `keyboard-operability` class. Both are adjacent, real-keystroke, same-tier-of-rigor records — but they are not the named instruments. Consequence: I use `ax_name_role_state.name` (an AX-tree computation fact) as evidence, and I do **not** use `sr_announcement.new_phrases == []` as proof that a real screen reader is silent. That distinction is what keeps observation 1 out of the findings list (see Open Questions Q1).

**keyboard-a11y-tester calibration rules applied:**
- Rule 1 (batch-crawl 4.1.3 findings are prompts, not failures) — **does not apply**: this is a driven session, not a batch crawl.
- Rule 2 (name-presence checks miss UA-intrinsic names) — **applies in the safe direction**: a `<ul role="listbox">` has no UA-intrinsic name, so observation 2's `name: ""` is a genuine absence, not a tool blind spot.
- Rule 3 (journey-level verdicts are judgment-layer) — **applies**: the digest asserts no verdicts, only per-step trace facts, which is the tier I am consuming.
- Rule 4 (`conformance_level` is a pass/fail gate, not the SC's WCAG level) — **moot**: no `conformance_level`, `wcag`, `sc`, `severity`, or `impact` key exists anywhere in the trace (digest absence claim 1, `grep -o` returned empty). Every SC below is mine, derived independently.

**No axe-core artifact, no batch-crawl findings, no CSS, and no contrast measurements were provided.** Nothing below states or implies a machine-detectable structural verdict.

---

## Direct answer to the evidence pack's framing question

The digest reserved judgment for the consumer. Answering both halves explicitly:

**Interaction defects — YES, three, at step-level granularity.**
1. Focus leaves the widget entirely on the selection keystroke and lands on `body` (step_0005), reaching the trigger again only via an explicit Shift+Tab (step_0006). Focus not returning where expected.
2. `ArrowDown` on the focused listbox produces no recorded change of any kind — same active element, byte-identical states, no active-descendant field present (step_0004). Keyboard operability of the option cursor is not exposed to AT.
3. The trigger's accessible name is a stale constant: `"Sort by"` at step_0001 and `"Sort by"` at step_0006, while the visible text moved from `"Newest▼"` to `"Price: low to high▼"`. A user-visible value change with no corresponding programmatic change.

**Structural defects — the evidence set does NOT answer this, and I decline to answer it from this evidence.** No axe artifact was supplied; the trace's AX snapshots cover only the six elements that happened to receive focus, not a DOM-wide audit. The absence claim that `region.landmark` and `region.heading` are `null` in all six steps is **not** evidence of a missing landmark or a heading-order violation — the digest itself scopes it to the per-step focused-region field, and more decisively, this is a component-scope review of a dropdown, which has no landmark or heading obligation. Filing "missing landmark" here would be a manufactured violation and a scope error. What structural defects I *do* report (M3 listbox has no accessible name, M4 hardcoded IDs, m1 dangling `aria-controls` while collapsed) come from the source, not from that absence claim.

**Unanswered by construction:** the sibling artifact `interactive-dropdown-focus-bug.findings.json` sits in the same directory and was deliberately not opened. It is the cheapest next read and may already carry the tool's own machine verdict.

---

## Phase 1 — Pre-commitment Predictions (made before reading the code)

For a custom dropdown/select, the protocol's prior is: focus management after Escape, arrow-key navigation incomplete, selected state not announced, options container not properly referenced.

| # | Prediction | Outcome |
|---|---|---|
| P1 | Focus not restored to the trigger after Escape/selection | **Confirmed** → C1. Worse than predicted: focus goes to `body`, not merely "stays put" |
| P2 | Arrow-key navigation incomplete — no `aria-activedescendant`, no roving tabindex | **Confirmed** → C2 |
| P3 | Selected state not announced | **Confirmed and worse than predicted** → C3. I predicted "the change isn't announced"; the actual defect is that the value never enters the accessible name *at all*, in any state |
| P4 | Options container not referenced / not labeled | **Split**: `aria-controls` *is* present (better than predicted) but the listbox has no accessible name (M3) and the IDREF dangles while collapsed (m1) |
| P5 | Escape handling missing | **Confirmed in a form I did not predict**: Escape exists but is bound to the listbox — which is not where focus is when the widget opens (M1 + M2 compound) |

**Three things surprised me, and it is worth naming which instrument found each:**

- **The open-focus call is provably dead code**, for a React-specific reason I would not have predicted from the pattern alone (M1). The code-read proves it; the trace's `focus_moved:false` at step_0002 confirms it at runtime.
- **`<label for>` on a `<button>` suppressing the value from the accessible name** (C3). A pure code-read would likely have *passed* this — the markup looks correct and `<button>` is a labelable element, so the HTML is valid. Only the AX-tree `name` field in the trace exposed it. This is the single clearest case in this review of measurement changing the verdict rather than decorating it.
- **The Escape-without-revert value divergence** (M5) — found by code-read, and the trace *could not* have found it, because the driven session never pressed Escape in any of its six steps. Measurement and code-read each caught something the other missed.

---

## Phase 2 — Semantic HTML Audit

Findings here are mostly clean, and calibration requires saying so plainly.

**Correct, verified against source:**
- The trigger is a real `<button>` (line 42), not a `div` with `role="button"`. Native semantics used where available — the non-negotiable rule is satisfied. Enter and Space activate it for free, which the trace confirms at step_0002 (`keystroke_sent: "Enter"` produced `expanded: true`).
- `<span aria-hidden="true">▼</span>` (line 50) correctly hides the decorative glyph from the accessibility tree. This is the exact defect class the state-communication phase warns about (symbols announced as "black down-pointing triangle") and it is done **right** here. Note it as a credit, not a finding.
- `role="listbox"` on `<ul>` with `role="option"` on `<li>` (lines 56, 64) is the APG-sanctioned mapping. Overriding list semantics is correct for this pattern, not a semantic violation.
- `aria-expanded={isOpen}` (line 45) passes a JSX boolean, which React serializes to the string `"true"`/`"false"` — valid values, not `"yes"`/`"no"`.
- No layout tables, no fake lists, no ARIA masking bad structure.

**Not clean:**
- `<label htmlFor="dropdown-btn">` (line 41) targeting a `<button>`. `<button>` *is* a labelable element, so this is valid HTML — the problem is not validity, it is the resulting accessible name. See C3.
- Heading hierarchy and landmark structure are out of scope for a component of this size and cannot be assessed from the artifact. No finding.

---

## Phase 3 — ARIA Pattern Compliance Audit

**Which pattern is this?** It is a hybrid. The trigger uses the *select-only combobox* vocabulary (`aria-haspopup="listbox"` + `aria-expanded` + `aria-controls` on a button), but the focus model is the *collapsible listbox* model — `tabIndex="0"` on the `<ul>` (line 58) and an intent to move focus into the list (lines 10–12). Both are legitimate APG patterns. The problem is that it implements neither one's completion requirements.

| APG requirement (collapsible listbox / select-only combobox) | Present? | Evidence |
|---|---|---|
| Trigger is focusable, named, exposes popup + expanded state | Partial | button + `aria-haspopup` + `aria-expanded` present (42–47); name is wrong (C3) |
| Listbox has an accessible name | **No** | no `aria-label`/`aria-labelledby` on `<ul>` (53–59); `name: ""` measured |
| Active option tracked via `aria-activedescendant` **or** roving tabindex | **No** | neither exists anywhere in the source |
| Options carry `id`s (required for activedescendant) | **No** | `<li>` has `key`, `role`, `aria-selected`, `onClick` only (62–67) |
| `aria-selected` on the current option | Yes | line 65 |
| Escape closes the popup **and returns focus to the trigger** | **No** | closes only (22–24); no focus restore; handler not bound where focus is |
| Selecting an option returns focus to the trigger | **No** | `handleSelect` (15–19) never touches the trigger |
| Down Arrow / Up Arrow on the collapsed trigger opens the popup | **No** | no `onKeyDown` on the button at all (42–48) |
| Home / End move to first / last option | **No** | not handled (21–37) |
| Type-ahead (printable character search) | **No** | not handled |
| Active option kept scrolled into view | **No** | no scroll management |

Six of eleven required behaviors absent. The pattern is roughly 40% implemented, and the missing 60% is entirely the AT-facing half.

---

## Phase 4 — Focus Management Review

The focus design is not merely incomplete; the one deliberate focus call in the component **cannot execute**.

```js
const handleToggle = () => {
  setIsOpen(!isOpen);
  if (!isOpen && listRef.current) {   // line 10
    listRef.current.focus();          // line 11 — unreachable
  }
};
```

The guard `!isOpen` is true exactly when the list is unmounted (so `listRef.current === null`), and `listRef.current` is non-null exactly when `isOpen` is true (so `!isOpen` is false). **The two conditions are mutually exclusive by construction.** The focus call is dead code on every path. Even correcting the stale-closure read of `isOpen` would not help: the `<ul>` is conditionally rendered (line 52), so the ref is still null at the moment `setIsOpen` is queued — React has not rendered yet.

Runtime confirmation, `digest-only`: step_0002 records `keystroke_sent: "Enter"`, `active_element_selector: "#dropdown-btn"`, `focus_moved: false`, with states flipping to `expanded: true`. The widget expanded and focus did not move.

Downstream consequences chain from there:
- With focus still on the button and no `onKeyDown` on the button, Escape/ArrowDown/ArrowUp are all inert in the exact state where a user most wants them (M2).
- The user must Tab into the list. The list is next in DOM order so this works, but it is undocumented and unannounced.
- On commit, focus goes to `body` (C1) — the worst possible landing spot, since the next Tab restarts from the top of the document.
- Tab out of an open list is unhandled: the list stays open and `aria-expanded` stays `true` while focus is elsewhere (M6).

---

## Phase 5 — State Communication Audit

| State | Communicated to AT? | Notes |
|---|---|---|
| Expanded / collapsed | Yes | `aria-expanded` toggles correctly, measured at step_0002 |
| Popup type | Yes | `aria-haspopup="listbox"` |
| Which option is *selected* | Yes, statically | `aria-selected` on the `<li>` (65) |
| Which option is *active* under the arrow cursor | **No** | no `aria-activedescendant`, no DOM focus movement, no option `id`s → C2 |
| **The committed value** | **No** | accessible name is the constant `"Sort by"` → C3 |
| Loading / busy | N/A | no async in this component |
| Errors | N/A | none |
| Disabled | N/A | none |

The two "No" rows are the entire user-facing purpose of the control: *which option am I on* and *which option did I choose*. Neither reaches assistive technology.

---

## Findings

### CRITICAL

---

**C1 — Focus is dropped to `<body>` on selection and never restored to the trigger; the Escape path has the same defect.**

- **Evidence (code, first-party):** `handleSelect` at `BuggyDropdown.jsx:15-19` sets `selectedIndex`, calls `onSelect`, and sets `isOpen(false)`. Nothing focuses the trigger. The `<ul>` at lines 53–72 is conditionally rendered (line 52), so `setIsOpen(false)` unmounts the currently-focused element. When the focused element is removed from the DOM, the browser assigns focus to `document.body`. The Escape branch at lines 22–24 is the identical code path — `setIsOpen(false)` with no focus restoration.
- **Evidence (measured, `digest-only`):** `…/interactive-dropdown-focus-bug.trace.json :: step_0005` — `keystroke_sent: "Enter"`, `active_element_selector: "body"`, `tag: "body"`, `focus_moved: true`, `ax_name_role_state: {"name": null, "role": "none", "states": {}}`, `region: null`, `bounding_box: null`. The trigger is reached again only at step_0006 via an explicit `Shift+Tab`, not automatically.
- **Scope caution:** the driven session pressed Escape zero times in six steps. The Escape defect is a **code-read inference from an identical code path**, high confidence, but unmeasured. Do not report it as measured.
- **User groups:** keyboard-only (primary), screen reader (primary).
- **WCAG / APG:** WCAG 2.2 **2.4.3 Focus Order** (Level A) — focus order must preserve meaning and operability; dumping focus to `body` after a mid-page interaction does neither. WAI-ARIA APG, Combobox (select-only) and Listbox patterns: "When the listbox is closed, focus returns to the combobox/button."
- **Why this matters:** a keyboard user on a results page picks a sort order and their focus position is annihilated. The next Tab starts from the top of the document — they re-traverse the skip link, the entire primary nav, and every control above the dropdown to get back to the results they just sorted. A screen reader user gets no announcement at all on commit (`sr_announcement` fields empty at step_0005) and lands on a nameless, roleless `body`; from their position there is no signal that the action succeeded, failed, or occurred. axe-core cannot see any of this.
- **Confidence:** HIGH (selection path measured + code-read; Escape path code-read).
- **Refutable?** NO for the selection path.
- **GAP or PREFERENCE:** GAP.
- **Fix:** capture the trigger in a ref and restore focus after the close, deferred past React's unmount:
  ```jsx
  const buttonRef = useRef(null);
  const close = ({ restoreFocus = true } = {}) => {
    setIsOpen(false);
    if (restoreFocus) setTimeout(() => buttonRef.current?.focus(), 0);
  };
  ```
  Call `close()` from **both** `handleSelect` and the Escape branch, and attach `ref={buttonRef}` to the button (line 42). The `setTimeout(…, 0)` is not superstition — a synchronous focus call in the same tick as the unmount is dropped by React's commit sequence.

```
### A11y Evidence Finding
finding_id: dropdown-focus-not-restored-to-trigger
fingerprint: not-computed — recipe: sha256("BuggyDropdown.jsx|2.4.3|#dropdown-btn|focus-to-body-after-select")[0:16]; compute in the harness. Do NOT read this line as a hash value.
source: BuggyDropdown.jsx:15-19,22-24 (first-party source) + evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json :: step_0005 (DIGEST-ONLY, not re-fetched)
wcag_or_apg: WCAG 2.2 SC 2.4.3 Focus Order (Level A); WAI-ARIA APG Combobox (select-only) / Listbox — "focus returns to the button when the listbox closes"
section_508_fpc_context: not in scope — component-scope review, no declared Revised Section 508 engagement. Note for scoping: 2.4.3 exists in WCAG 2.0 A/AA, so this would also fail under a federal conformance floor if one is declared.
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, keyboard=HIGH, low-vision=MEDIUM, cognitive=MEDIUM
evidence: step_0005 — {"keystroke_sent":"Enter","active_element_selector":"body","tag":"body","focus_moved":true,"ax_name_role_state":{"name":null,"role":"none","states":{}},"region":null}; step_0006 reaches "#dropdown-btn" only via explicit "Shift+Tab"
reproduction_steps: 1) Tab to #dropdown-btn. 2) Press Enter to expand. 3) Tab into #dropdown-list. 4) Press ArrowDown. 5) Press Enter to commit. 6) Read document.activeElement. Repeat 1-3 then press Escape at step 4 for the unmeasured second path.
expected_behavior: After commit or Escape, document.activeElement === #dropdown-btn and the screen reader announces the trigger with its updated value.
actual_behavior: document.activeElement === body; role "none", name null; no announcement. Trigger reachable only by manual Shift+Tab.
trend: new
```

---

**C2 — Arrow-key navigation produces no assistive-technology-observable change: no `aria-activedescendant`, no roving tabindex, no option IDs.**

- **Evidence (code, first-party):** the arrow branches at `BuggyDropdown.jsx:25-32` mutate React state (`setSelectedIndex`) and nothing else. DOM focus stays on the `<ul>` (line 58, `tabIndex="0"`). The `<ul>` at lines 53–59 carries **no `aria-activedescendant`**. The `<li>` at lines 62–67 carries `key`, `role`, `aria-selected`, `onClick`, `className` — **no `id`** (so activedescendant could not be wired even if it existed) and **no `tabIndex`** (so roving tabindex is not the alternative mechanism either). Neither of the two APG-sanctioned mechanisms for exposing an option cursor is present.
- **Evidence (measured, `digest-only`):** `…trace.json :: step_0004` — `keystroke_sent: "ArrowDown"`, `active_element_selector` stays `"#dropdown-list"`, `focus_moved: false`, captured states **identical to step_0003**, and explicitly "no active-descendant or option-level field present." The AX tree recorded literally nothing changing.
- **User groups:** screen reader (blocking), low vision using a magnifier (the visual `.selected` class may move off-screen with no scroll management — see m2).
- **WCAG / APG:** WCAG 2.2 **4.1.2 Name, Role, Value** (Level A) — the widget's current value/active state must be programmatically determinable. WAI-ARIA APG Listbox pattern: "the listbox element has `aria-activedescendant` set to the ID of the focused option," or equivalently roving tabindex.
- **Why this matters:** this is the finding that makes the control unusable rather than merely annoying. A screen reader user focuses the list, presses Down Arrow three times, and hears nothing on any press. They have no idea which option they are on. They must then press Enter and commit *blind* — and because C3 means the result is also silent, they cannot even discover after the fact what they chose. The visual `.selected` class (line 67) moves, so a sighted mouse or keyboard user sees the cursor advancing. That divergence — works perfectly for one perspective, totally opaque to another — is exactly the class of defect automated testing cannot reach. axe-core passes this markup.
- **Confidence:** HIGH. The code-read alone is dispositive; the trace independently confirms.
- **Refutable?** NO.
- **GAP or PREFERENCE:** GAP.
- **Fix (recommended — `aria-activedescendant`, fewer focus side effects in React):**
  ```jsx
  const uid = useId();
  const optId = (i) => `${uid}-opt-${i}`;

  <ul ref={listRef} id={listId} role="listbox"
      tabIndex={-1}                                   // programmatic focus only; drops the stray tab stop
      aria-labelledby={labelId}
      aria-activedescendant={optId(activeIndex)}      // moves with the arrow cursor
      onKeyDown={handleKeyDown}>
    {options.map((option, index) => (
      <li key={option} id={optId(index)} role="option"
          aria-selected={index === selectedIndex}      // the COMMITTED option, not the cursor
          className={index === activeIndex ? 'active' : ''}
          onClick={() => commit(index)}>
        {option}
      </li>
    ))}
  </ul>
  ```
  **Roving tabindex is the equally valid alternative:** `tabIndex={index === activeIndex ? 0 : -1}` on each `<li>`, remove `tabIndex` from the `<ul>`, and call `.focus()` on the active option in a `useEffect`. Pick one; do not mix them.
  Whichever you pick, also scroll the active option into view (`optionRef.scrollIntoView({ block: 'nearest' })`) — see m2.

```
### A11y Evidence Finding
finding_id: dropdown-no-active-option-exposed
fingerprint: not-computed — recipe: sha256("BuggyDropdown.jsx|4.1.2|#dropdown-list|no-activedescendant")[0:16]; compute in the harness. Do NOT read this line as a hash value.
source: BuggyDropdown.jsx:25-32,53-67 (first-party source) + evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json :: step_0003, step_0004 (DIGEST-ONLY, not re-fetched)
wcag_or_apg: WCAG 2.2 SC 4.1.2 Name, Role, Value (Level A); WAI-ARIA APG Listbox pattern — aria-activedescendant or roving tabindex
section_508_fpc_context: not in scope — component-scope review. Note: 4.1.2 exists in WCAG 2.0 A/AA and would also fail under a declared federal floor.
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, keyboard=MEDIUM, low-vision=MEDIUM, cognitive=MEDIUM
evidence: step_0004 — {"keystroke_sent":"ArrowDown","active_element_selector":"#dropdown-list","focus_moved":false,"sr_announcement":{"new_phrases":[],"live_announcements":[],"focus_announcement":null}}; states byte-identical to step_0003; digest notes "no active-descendant or option-level field present". Source: no aria-activedescendant on the ul, no id or tabIndex on any li.
reproduction_steps: 1) Expand the dropdown. 2) Move focus to #dropdown-list. 3) Press ArrowDown. 4) Inspect the AX node for #dropdown-list for an activeDescendant relation; inspect each li for id/tabindex.
expected_behavior: The listbox exposes aria-activedescendant pointing at the active option's id; each ArrowDown re-points it and the screen reader announces the new option's label and position.
actual_behavior: No activedescendant relation exists. AX states after ArrowDown are identical to before. Only a CSS class changes.
trend: new
```

---

**C3 — The chosen value never reaches the trigger's accessible name; the button announces an identical string before and after selection.**

- **Evidence (code, first-party):** the button's rendered content is `{options[selectedIndex]}` (line 49) — the visible text *does* track the selection. But the button is targeted by `<label htmlFor="dropdown-btn">{label}</label>` (line 41), and there is no `aria-label`, no `aria-labelledby`, and no live region anywhere in the component to carry the value by another route.
- **Evidence (measured, `digest-only`):** `…trace.json :: step_0006` — `text: "Price: low to high▼"` but `ax_name_role_state.name: "Sort by"`, described as the *identical string* to step_0001 (whose `text` was `"Newest▼"`). The `focus_announcement` is byte-identical across both steps: `"button, Sort by, not expanded, has popup listbox"`. The `states.labelledby` relatedNode resolves to `{"backendDOMNodeId": 14, "text": "Sort by"}` — two independent AX fields agreeing that the `<label>` won the name computation over the button's own subtree.
- **User groups:** screen reader (blocking).
- **WCAG / APG:** WCAG 2.2 **4.1.2 Name, Role, Value** (Level A) — the *value* of a user-interface component must be programmatically determinable, and changes to it must be available to user agents including assistive technologies. WAI-ARIA APG Combobox (select-only): the trigger uses `aria-labelledby="<labelId> <triggerId>"` so the accessible name is the label **plus** the current value.
- **Why this matters:** the sighted user's entire feedback loop for this control is "the button now reads *Price: low to high*." A screen reader user never receives that. They cannot confirm their selection, cannot check the current sort on a later visit to the page, and — combined with C1's silent focus loss and C2's silent arrow cursor — complete a full interaction with the control having received *zero* information at any point. There is no in-widget workaround; a browse-mode read of a button renders its accessible name, not its subtree.
- **Where my confidence drops, stated plainly:** the *mechanism* (that `<label for>` overrides the button's subtree in the accessible-name computation) is digest-tier and engine-specific. Browsers differ on whether a `<label>` associated with a `<button>` supersedes the button's content; the trace shows Chrome resolving it to `"Sort by"` and reporting the name source as `labelledby`. **Downgrade condition:** if a re-fetch shows the name tracking the button's subtree instead, C3 drops to MAJOR and largely collapses into C1 (the value would be in the name but only announced when focus returns — which C1's fix supplies). I am filing it at CRITICAL because two independent AX fields in the trace agree, and because the recommended fix is correct and worth making under *either* reading — engine-dependent naming is itself a reason to stop relying on `<label for>` here.
- **Re-fetch to close the gap:**
  ```
  jq -c '[.steps[] | {step_id, text, name: .ax_name_role_state.name,
                      ann: .sr_announcement.focus_announcement}]' \
     evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json
  ```
- **Confidence:** MEDIUM-HIGH.
- **Refutable?** PARTIALLY — a developer could point to an `aria-live` results region elsewhere on the page announcing "Sorted by price, low to high." That would soften the blast radius but does **not** repair the finding: the button's own name stays stale forever, so the current sort remains undiscoverable on any later encounter with the control.
- **GAP or PREFERENCE:** GAP.
- **Fix:** stop naming the button with `<label for>`; use the APG select-only-combobox recipe so the name is *label + current value*:
  ```jsx
  const uid = useId();
  const labelId = `${uid}-label`, btnId = `${uid}-btn`;

  <span id={labelId}>{label}</span>            {/* was <label htmlFor> */}
  <button
    id={btnId}
    ref={buttonRef}
    aria-labelledby={`${labelId} ${btnId}`}    {/* "Sort by" + the button's own content */}
    aria-haspopup="listbox"
    aria-expanded={isOpen}
    aria-controls={listId}
    onClick={handleToggle}
  >
    {options[selectedIndex]}
    <span aria-hidden="true">▼</span>          {/* excluded from the name — already correct */}
  </button>
  ```
  Accessible name becomes `"Sort by Newest"` → `"Sort by Price: low to high"`. Combined with C1's focus restoration, the SR user hears the new value on commit with no live region needed. **Do not also add an `aria-live` region for this** — that produces a double announcement, which is its own defect. See E1.

```
### A11y Evidence Finding
finding_id: dropdown-trigger-accname-omits-value
fingerprint: not-computed — recipe: sha256("BuggyDropdown.jsx|4.1.2|#dropdown-btn|stale-accname-sort-by")[0:16]; compute in the harness. Do NOT read this line as a hash value.
source: BuggyDropdown.jsx:41,49 (first-party source) + evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json :: step_0001, step_0006 (DIGEST-ONLY, not re-fetched)
wcag_or_apg: WCAG 2.2 SC 4.1.2 Name, Role, Value (Level A); WAI-ARIA APG Combobox (select-only) — aria-labelledby="<labelId> <triggerId>"
section_508_fpc_context: not in scope — component-scope review. Note: 4.1.2 exists in WCAG 2.0 A/AA and would also fail under a declared federal floor.
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, keyboard=LOW, low-vision=LOW, cognitive=MEDIUM
evidence: step_0006 — {"text":"Price: low to high▼","ax_name_role_state":{"name":"Sort by","role":"button"},"sr_announcement":{"focus_announcement":"button, Sort by, not expanded, has popup listbox"}}; step_0001 text was "Newest▼" with the byte-identical name and focus_announcement. states.labelledby relatedNode = {"backendDOMNodeId":14,"text":"Sort by"}.
reproduction_steps: 1) Focus #dropdown-btn, record its AX name. 2) Expand, move to the list, arrow to a different option, press Enter. 3) Shift+Tab back to #dropdown-btn and record its AX name and visible text. 4) Compare.
expected_behavior: Accessible name reads label + current value ("Sort by Price: low to high") and changes when the value changes.
actual_behavior: Accessible name is the constant "Sort by" while visible text changed from "Newest▼" to "Price: low to high▼". Focus announcement is byte-identical across both steps.
trend: new
```

---

### MAJOR

**M1 — The only focus call in the component is unreachable; opening the dropdown never moves focus to the list.**

- **Evidence:** `BuggyDropdown.jsx:8-13`. `if (!isOpen && listRef.current)` — the guard is true exactly when the `<ul>` is unmounted (line 52 conditional render ⇒ `listRef.current === null`), and the ref is populated exactly when `isOpen` is true (⇒ guard false). Mutually exclusive by construction: **line 11 can never run.** Correcting the stale-closure read of `isOpen` would not fix it either — the ref is still null on that tick because React has not rendered the list.
- **Evidence (measured, `digest-only`):** `step_0002` — `focus_moved: false`, `active_element_selector` remains `"#dropdown-btn"` while `expanded` flips to `true`.
- **User groups:** keyboard, screen reader.
- **WCAG / APG:** WCAG 2.2 **2.4.3 Focus Order**; WAI-ARIA APG Listbox — "when the listbox is displayed, focus moves to it (or the trigger retains focus with `aria-activedescendant`)." The fixture's own stated expected behavior #1 ("Opens on button click, list receives focus") is not met.
- **Why this matters:** the widget silently does the opposite of what it was designed to do, and every downstream keyboard behavior is bound to the wrong element as a result (see M2). The user must discover, unprompted, that Tab is required to enter the list. **Mitigated by:** the `<ul>` is the next focusable element in DOM order, so Tab does reach it — this is friction, not a barrier, which is why it is MAJOR rather than CRITICAL.
- **Confidence:** HIGH. **Refutable?** NO. **GAP.**
- **Fix:** move the focus into an effect that runs after the list mounts.
  ```jsx
  useEffect(() => { if (isOpen) listRef.current?.focus(); }, [isOpen]);
  ```
  Then delete lines 10–12 entirely. If you adopt the select-only-combobox architecture instead (recommended below), focus never leaves the trigger and this whole mechanism disappears.

---

**M2 — The trigger button has no keydown handler, so Escape, ArrowDown, and ArrowUp are inert in the exact state where users reach for them.**

- **Evidence:** `BuggyDropdown.jsx:42-48` — the button has `onClick` only. `onKeyDown={handleKeyDown}` is bound solely to the `<ul>` (line 57). Because M1 leaves focus on the button after opening, the widget's *default* open state has focus on an element that handles no keys.
- **Evidence (measured, `digest-only`):** step_0002 establishes the premise — `expanded: true` with `active_element_selector: "#dropdown-btn"`.
- **User groups:** keyboard, screen reader.
- **WCAG / APG:** WCAG 2.2 **2.1.1 Keyboard** (Level A); WAI-ARIA APG Combobox — Down Arrow on the collapsed trigger opens the popup and moves to the first/selected option; Escape closes the popup from anywhere in the widget.
- **Why this matters, and how it compounds:** M1 and M2 together mean that the single most common cancel gesture in the world — *open a dropdown, change your mind, press Escape* — does **nothing at all**. Escape is implemented (line 22) and is simply bound to an element that does not have focus. This is the else-branch-coverage anti-pattern from the April 2026 third-party audit exactly: the behavior was fixed on one branch (list focused) and missed on the other (button focused). **Mitigated by:** Enter or Space on the still-focused button re-toggles it closed, so the user is not stuck. That mitigation is why this is MAJOR, not CRITICAL — but no user will discover it as the intended escape hatch.
- **Confidence:** HIGH. **Refutable?** NO. **GAP.**
- **Fix:** hoist the handler to the wrapper so it covers *every* branch, present and future:
  ```jsx
  <div className="dropdown-wrapper" onKeyDown={handleWrapperKeyDown} onBlur={handleFocusOut}>
  ```
  with `handleWrapperKeyDown` handling `Escape` (close + restore focus) unconditionally, and `ArrowDown`/`ArrowUp` opening the list when collapsed. One handler at the wrapper is structurally immune to the branch-coverage failure that produced this finding.

---

**M3 — The listbox has no accessible name.**

- **Evidence (code):** `BuggyDropdown.jsx:53-59` — the `<ul role="listbox">` has `ref`, `id`, `role`, `onKeyDown`, `tabIndex`, `className`. No `aria-label`, no `aria-labelledby`.
- **Evidence (measured, `digest-only`):** `step_0003` (and `step_0004`) — `ax_name_role_state: {"name": "", "role": "listbox"}`. Calibration rule 2 applies in the safe direction: `<ul>` has no UA-intrinsic name, so `""` is a genuine absence rather than a tool blind spot.
- **User groups:** screen reader.
- **WCAG / APG:** WCAG 2.2 **4.1.2 Name, Role, Value** (Level A); WAI-ARIA APG Listbox — "the listbox has a label provided by `aria-label` or `aria-labelledby`."
- **Why this matters:** the user Tabs into the list and hears "listbox" with no indication of what it lists. **Mitigated by:** they just activated a button, so context carries over — which is why this is MAJOR rather than CRITICAL. That mitigation evaporates for anyone who reaches the list by a route other than the trigger (browse-mode wandering, a landmark jump, or an interrupted session).
- **Confidence:** HIGH. **Refutable?** NO. **GAP.**
- **Fix:** `aria-labelledby={labelId}` on the `<ul>`, pointing at the same visible label span from C3's fix. Do not use `aria-label={label}` — that duplicates the text instead of associating it, and drifts when the visible label changes.

---

**M4 — Hardcoded DOM IDs in a prop-driven, reusable component guarantee collisions across instances.**

- **Evidence:** `BuggyDropdown.jsx:43` (`id="dropdown-btn"`), `:46` (`aria-controls="dropdown-list"`), `:55` (`id="dropdown-list"`), `:41` (`htmlFor="dropdown-btn"`). All four are string literals in a component parameterized by `label`, `options`, and `onSelect` — a signature that exists to be instantiated more than once.
- **User groups:** screen reader (primary), keyboard (label click targets the wrong control).
- **WCAG / APG:** WCAG 2.2 **1.3.1 Info and Relationships** (Level A) and **4.1.2 Name, Role, Value** (Level A). Duplicate IDs make every IDREF resolve to the first match in document order.
- **Why this matters:** on a page with a "Sort by" and a "Filter by" dropdown built from this component, the second dropdown's `<label>` names the *first* dropdown's button, and the second button's `aria-controls` points at the *first* list. Clicking the second visible label moves focus to the first dropdown. The AT-exposed structure is not merely incomplete — it is wired to the wrong elements. This is the duplicate-DOM/ID-collision case the focus-management phase calls out directly.
- **Mitigated by:** single-instance pages are entirely unaffected. That conditionality is why this stays MAJOR and is not upgraded to CRITICAL despite the severity of its manifestation.
- **Confidence:** HIGH on the source fact; MEDIUM on the co-occurrence.
- **Refutable?** YES, if the team can state that this component is guaranteed singleton-per-page. I am filing it anyway: a `label` prop on a dropdown is a strong signal of the opposite, and the fix costs one line.
- **GAP.**
- **Fix:** `const uid = useId();` (React 18+) and derive every ID from it — `${uid}-btn`, `${uid}-list`, `${uid}-label`, `${uid}-opt-${index}`. The option IDs are needed for C2's `aria-activedescendant` regardless, so this fix is on the critical path anyway.

---

**M5 — Arrowing mutates the trigger's displayed value without committing it; Escape then leaves the display diverged from the value the application holds.**

- **Evidence:** a single state variable does two jobs. `selectedIndex` is mutated by the arrow branches (`BuggyDropdown.jsx:27-28, 31-32`) *without* calling `onSelect`, and the button renders `{options[selectedIndex]}` (line 49). The Escape branch (lines 22–24) sets `isOpen(false)` and does **not** revert `selectedIndex`.
- **Walk it through:** the trigger shows "Newest". User opens, arrows down twice to "Price: low to high" — the collapsed trigger's text is already changing underneath the open list — then presses Escape to cancel. The list closes. The button now reads "Price: low to high". `onSelect` was never called, so the parent still holds "Newest". Re-opening shows `aria-selected="true"` on "Price: low to high", so the widget is internally consistent about a value the application does not have. **The divergence is undetectable from inside the control.**
- **Evidence (measured, `digest-only`, partial):** step_0006's `text: "Price: low to high▼"` confirms the mechanism — the button's text tracks `selectedIndex`. But at that step a selection *was* committed (Enter at step_0005), so the change is expected there. **The Escape divergence itself is unmeasured** — the driven session pressed Escape zero times.
- **User groups:** all users; disproportionately cognitive and screen reader (who, per C3, cannot even read the divergent value to notice it).
- **WCAG / APG:** WCAG 2.2 **4.1.2 Name, Role, Value** (Level A) — the presented value and the programmatic value must agree. WAI-ARIA APG Combobox, manual-selection variant: "Escape closes the listbox **and the value is not changed**."
- **Why this matters:** the control lies about application state. The user believes they cancelled and can see a value that is not in effect; the results below are sorted by something else. This is a trust failure, not an access failure, which keeps it at MAJOR — but it is the finding most likely to generate a "the site is broken" support ticket from a *sighted* user, which is worth saying out loud.
- **Confidence:** HIGH (code-read is complete and self-contained). **Refutable?** NO. **GAP.**
- **Fix — and this one is a product decision, not just a technical one.** Two coherent options; pick deliberately, do not split the difference:
  1. **Manual selection (matches the current Escape semantics).** Split the state: `activeIndex` is the transient arrow cursor, `selectedIndex` is the committed value. Render the button from `selectedIndex`, drive `aria-activedescendant` from `activeIndex`, put `aria-selected` on `selectedIndex`, reset `activeIndex = selectedIndex` on open, and commit only on Enter/click.
  2. **Selection follows focus.** Call `onSelect` on every arrow press. Also APG-legal, simpler, but it changes product behavior — every arrow keystroke fires a sort — and it makes Escape meaningless as a cancel. Only choose this if a re-sort per keystroke is genuinely acceptable.
  The fixture's stated expected behavior ("Enter or click selects option") points at option 1.

---

**M6 — Tab out of an open list leaves the popup open with `aria-expanded="true"`; there is no focus-out dismissal.**

- **Evidence:** `BuggyDropdown.jsx:21-37` handles Escape, ArrowDown, ArrowUp, Enter. **Tab is not handled**, and there is no `onBlur`/focusout handler anywhere in the component (lines 40, 53–59). Tab from the `<ul>` moves focus to the next document element while `isOpen` stays `true`.
- **User groups:** screen reader, keyboard, low vision.
- **WCAG / APG:** WCAG 2.2 **2.4.3 Focus Order** (Level A); WAI-ARIA APG Combobox — "Tab: … closes the listbox" / the popup is dismissed when focus leaves the widget.
- **Why this matters:** the AX tree now advertises an expanded popup that the user has left. A screen reader user tabbing forward encounters page content while their mental model says they are still inside a dropdown, and there is no cue that they left. Visually an open overlay persists over page content while focus is elsewhere. **Mitigated by:** no keyboard trap results — the user can always continue tabbing, and clicking the trigger closes it. That is why this is MAJOR and not CRITICAL.
- **Confidence:** HIGH. **Refutable?** NO. **GAP.**
- **Fix:** wrapper-level focusout, using `relatedTarget` so intra-widget moves do not close it:
  ```jsx
  const handleFocusOut = (e) => {
    if (!e.currentTarget.contains(e.relatedTarget)) setIsOpen(false);  // no focus restore — the user left deliberately
  };
  ```
  Attach to the wrapper div (line 40). React's `onBlur` has focusout semantics and bubbles, so one handler covers both the button and the list — again immune to branch-coverage drift.

---

### MINOR

- **m1 — `aria-controls="dropdown-list"` dangles while the widget is collapsed.** `BuggyDropdown.jsx:46` renders the attribute unconditionally, but the `<ul id="dropdown-list">` only exists when `isOpen` (line 52). **The measured evidence shows this is benign in practice:** at step_0001 the AX states carry no `controls` key at all, and `controls: "dropdown-list"` appears only at step_0002 once the target exists — Chrome silently drops the unresolvable IDREF. So there is no user impact to report; the reasons to fix are validator noise (axe's `aria-valid-attr-value` treats an unresolvable `aria-controls` as *incomplete*/needs-review) and cross-engine consistency. **This is a place where the evidence prevented an inflated finding** — the code alone reads like a broken relationship, and the trace proves it is not. Fix: render the `<ul>` unconditionally and toggle `hidden`, matching APG's example, which also stabilizes the `aria-activedescendant` wiring from C2.
- **m2 — The active option is never scrolled into view.** No scroll management anywhere in `handleKeyDown` (lines 21–37). On an options list long enough to scroll, arrowing past the visible region moves the `.selected` highlight off-screen with no correction — a screen-magnifier user loses the cursor entirely. Per WAI-ARIA APG Listbox, the active option must be kept visible. (WCAG 2.4.11 Focus Not Obscured is adjacent but does not strictly apply, since the DOM-focused element is the listbox container, not the option — I am not citing it as the basis.) Fix: `optionRefs[activeIndex]?.scrollIntoView({ block: 'nearest' })` in the same effect that updates `aria-activedescendant`.
- **m3 — `Home` and `End` are not handled.** APG lists them for listboxes; on a long list, first/last currently costs N keystrokes. Trivial addition to the existing `handleKeyDown` chain.

### ENHANCEMENTS

- **E1 — Do *not* add an `aria-live` region to announce the selection.** Recording this as an explicit anti-recommendation because it is the reflexive fix for C3 and it is the wrong one: with C1's focus restoration plus C3's `aria-labelledby`, the SR user already hears the new value when focus returns to the trigger. Adding a live region on top produces a double announcement — the redundant-announcement defect. Reach for a live region only if you deliberately choose *not* to restore focus, which would be a worse design.
- **E2 — Type-ahead (printable-character search)** is an APG-recommended listbox behavior and is absent. Worth adding for lists over ~10 options; it is the main reason native `<select>` feels fast.
- **E3 — Reconsider whether this needs to be a custom widget at all.** A native `<select>` would deliver every behavior in the CRITICAL and MAJOR list for free, correctly, on every platform, with mobile-native pickers as a bonus. Custom listboxes earn their keep when options need rich content, grouping, or async loading. Nothing in this fixture shows that requirement. If it does not exist, the highest-leverage fix is deletion. Filed as an enhancement rather than a finding because the requirement may exist and simply is not visible in the artifact — but it deserves an explicit answer before anyone invests in the fixes above.
- **E4 — No `prefers-reduced-motion` handling is present, and none appears needed** — there is no animation in the JSX. The stylesheet was not supplied, so if `.dropdown-list` has an open/close transition, add the guard. Not rated.

---

## What's Missing (gaps and unstated assumptions)

**Missing from the component:**
1. `aria-activedescendant` **and** roving tabindex — both mechanisms for exposing an option cursor, absent (C2).
2. `id` on every `<li role="option">` — prerequisite for the above (C2).
3. Any focus restoration to the trigger, on any close path (C1).
4. A keydown handler on the trigger element (M2).
5. An accessible name on the listbox (M3).
6. Unique per-instance IDs (M4).
7. Separation of the transient arrow cursor from the committed value (M5).
8. A focusout/Tab dismissal path (M6).
9. Scroll-into-view for the active option (m2); `Home`/`End` (m3); type-ahead (E2).

**Missing from the evidence, which bounds what this review can conclude:**
1. **The Escape path was never exercised** — zero of six steps sent Escape, despite Escape being the fixture's own stated expected behavior #4 and the source of two findings (C1's second path, M5). This is the largest single gap in the evidence set.
2. **No axe-core artifact** ⇒ no DOM-wide structural verdict. The curator's structural sub-question is *unanswered*, not answered in the negative.
3. **No focus-indicator measurements surfaced.** `computed_focus_style` appears in the digest only at step_0005 (where it is `null` because the element is `body`). WCAG 2.4.7 Focus Visible and 2.4.13 Focus Appearance are therefore **unrated**, even though this trace type is the one instrument that can measure them. Re-fetch: `jq -c '[.steps[] | {step_id, computed_focus_style}]'`.
4. **No CSS was supplied.** WCAG 1.4.1 (is `.selected` a color-only distinction?), 1.4.3/1.4.11 contrast, 2.5.8 target size, and 2.4.11 focus obscured are all unrated. `.selected` (line 67) and `.dropdown-list` (line 59) are the only visual state channels in the component and neither can be inspected.
5. **Instrument-class mismatch** against the contract's prescribed evidence types for two of the four classes the curator's question spans: `name-role-state` prescribes `virtual-screen-reader` assertion output (supplied: the driven tool's simulated capture), and `keyboard-operability` prescribes an `npx playwright test` transcript (supplied: a driven-live trace). Adjacent and rigorous, but not the named instruments.
6. **Digest tier, not re-fetched.** Every trace citation above is a paraphrase of a handle I could not open.
7. **`step_0003`'s keystroke is unrecorded in the digest.** It matters: if focus reached `#dropdown-list` via `Tab`, that confirms M1's real-world cost (the user had to discover Tab). If the harness forced focus programmatically, M1's *impact* is unmeasured though its mechanism is still proven by code-read. Re-fetch: `jq '.steps[2].keystroke_sent'`.
8. **The sibling `interactive-dropdown-focus-bug.findings.json` was not opened** — a same-fixture artifact one directory listing away, possibly carrying the tool's own machine verdict.

---

## Multi-Perspective Notes

**Screen reader user (NVDA / JAWS / VoiceOver):** the worst-served perspective by a wide margin, and the gap is total rather than partial. Walking the full journey: focus the trigger → "button, Sort by, not expanded, has popup listbox." Press Enter → expands, focus does not move (M1). Press Escape to back out → nothing happens (M2). Tab into the list → "listbox," unnamed (M3). Arrow down three times → **silence on every press**, no active option exposed (C2). Press Enter → **silence**, and focus is now on `body` (C1). Shift+Tab back → "button, Sort by, not expanded, has popup listbox" — the byte-identical string they heard at the start (C3). They have completed a full, successful interaction with the control and received *no information at any point about what they were choosing or what they chose*. Everything axe-core inspects here passes.

**Keyboard-only user:** operable but incoherent. Every element is reachable and there is no trap — so 2.1.1 and 2.1.2 hold. But the interaction model contradicts itself: opening does not move focus where the code intends (M1), the universal cancel gesture is inert in the widget's default open state (M2), Tab silently abandons an open popup (M6), and committing a selection deletes the user's place in the document (C1). The tab-stop count also changes with state — one stop collapsed, two expanded, with the list positioned after the button in DOM order but visually overlaying content below it, so the tab order and the visual order diverge while open.

**Low vision (200% zoom, magnifier, high contrast):** largely unassessable from the artifact, and I will not manufacture findings to fill the space. What is visible from the source: the active option is never scrolled into view (m2), which is a specific magnifier hazard; and `.selected` (line 67) is the sole visual channel for the option cursor, so if that class is a color-only treatment it fails 1.4.1. Contrast, target size, reflow, and focus-indicator sufficiency all need the stylesheet plus an axe run. C1 has a low-vision dimension too: a magnifier user who loses focus to `body` loses their viewport position entirely and must re-hunt the page at 200%.

**Cognitive accessibility:** M5 is the finding that lives here. A control that displays a value the application does not hold — after the user pressed the key that universally means "cancel" — is precisely the kind of inconsistency that erodes confidence in the whole interface, and it is undetectable from inside the widget. Secondary: opening the dropdown and then finding that Escape does nothing (M1 + M2) trains users that this control does not behave like other controls. No timeouts, no destructive actions, no error handling in scope.

**Vestibular & motion:** no animation in the JSX. Stylesheet not supplied. Not rated.

**Auditory access:** no media elements. Not applicable.

**Environmental contrast:** stylesheet not supplied. The one code-visible concern is `.selected` as a possibly color-only state channel (1.4.1). Not rated.

### Perspective Alarm Levels

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | **HIGH** | Custom composite widget; three CRITICALs; the active option, the committed value, and the focus destination are all unexposed |
| Keyboard-only | **HIGH** | Focus lands on `body` after commit; Escape inert in the default open state; open popup survives Tab-out |
| Low vision | **MEDIUM** | No scroll-into-view for the active option; `.selected` may be a color-only channel; no CSS or focus-indicator measurements available to rate it |
| Cognitive | **MEDIUM** | Display/state divergence after Escape; inconsistent open behavior versus platform norms |
| Vestibular & motion | **LOW** | No animation in the component; stylesheet unseen |
| Auditory access | **LOW** | No media elements |
| Environmental contrast | **MEDIUM** | `.selected` is the sole visual state channel and the stylesheet was not supplied |

**Escalation:** screen reader and keyboard-only are both HIGH → escalate to `/perspective-audit` for deep review. Low vision, cognitive, and environmental contrast are MEDIUM and blocked on the same missing input (the stylesheet plus an axe run) — supply those before the deep review rather than during it.

---

## Phase 8 — Realist Check (severity calibration)

Every CRITICAL and MAJOR run through the four questions. Recalibrations and declined findings recorded here.

| Finding | Realistic worst case | Group | Detection | Outcome |
|---|---|---|---|---|
| C1 | Keyboard user re-traverses the entire page header to return to sorted results; SR user gets no signal the action occurred | keyboard, SR | Never automatically — axe passes; user report | **Held CRITICAL** |
| C2 | SR user commits a selection blind, with no way to know which option | SR | Never — no automated rule covers a missing activedescendant | **Held CRITICAL** |
| C3 | SR user can never determine the current sort, before or after selecting | SR | Never | **Held CRITICAL, conditional** — downgrade to MAJOR if re-fetch shows the name tracking the subtree |
| M1 | One extra, undiscoverable Tab | keyboard, SR | Manual keyboard test | **Held MAJOR.** Mitigated by: the list is next in DOM order |
| M2 | Escape does nothing; user clicks the trigger again instead | keyboard, SR | Manual keyboard test | **Held MAJOR.** Mitigated by: Enter/Space on the focused button re-toggles |
| M3 | "listbox" announced with no name | SR | Manual SR test | **Held MAJOR.** Mitigated by: context carries from the just-activated button |
| M4 | Second instance's label and `aria-controls` wire to the first instance | SR, keyboard | Instant, if a second instance ever ships | **Held MAJOR, not upgraded.** Mitigated by: single-instance pages are unaffected |
| M5 | Control displays a value the application does not hold | all | User report ("the sort is broken") | **Held MAJOR.** No access loss; a correctness and trust defect |
| M6 | Open popup persists while focus is elsewhere; `aria-expanded` lies | SR, keyboard, low vision | Manual keyboard test | **Held MAJOR.** Mitigated by: no trap results |

**Findings I considered and declined — recorded so the reasoning is auditable:**

- **"`aria-expanded` changes with no announcement" — DECLINED as a finding, moved to Open Questions Q1.** The digest reports exactly this at step_0002 (`new_phrases: []`, `focus_announcement: null`), and the curator's question invites it. But the `sr_announcement` field is the driven tool's *simulated* capture, which the digest itself flags as not the prescribed `name-role-state` instrument — and real NVDA and JAWS do announce "expanded"/"collapsed" when `aria-expanded` flips on the focused element. Filing this would be manufacturing a violation out of a tool artifact. Note the contrast with C3, which rests on `ax_name_role_state.name` — an AX-tree *computation* fact, not a simulated announcement. That distinction is the whole reason one is a CRITICAL and the other is an open question.
- **"Missing landmark / heading-order violation" — DECLINED as out of scope.** The absence claim showing `region.landmark: null` and `region.heading: null` across all six steps is scoped by the digest to the per-step focused-region field, is not a page-wide census, and in any case a dropdown component carries no landmark or heading obligation. Filing it would be both a scope error and a manufactured violation.
- **"Broken `aria-controls`" at CRITICAL — DOWNGRADED to m1 (MINOR) by measurement.** The code reads like a broken relationship; step_0001 versus step_0002 proves Chrome drops the unresolvable IDREF and exposes it only once the target exists. No user impact. This one is worth flagging as the review's clearest instance of evidence *preventing* an inflated severity rather than adding one.
- **M4 considered for upgrade to CRITICAL and declined** — its manifestation is severe (wrong control wired to the wrong label) but conditional on a second instance existing, which the artifact does not establish.

---

## Phase 9 — Self-Audit

| Finding | Confidence | Developer could refute? | GAP or PREFERENCE |
|---|---|---|---|
| C1 | HIGH | No (selection path measured) | GAP |
| C2 | HIGH | No | GAP |
| C3 | MEDIUM-HIGH | Partially — an external live region would soften impact, not repair the stale name | GAP |
| M1 | HIGH | No — the dead-code proof is self-contained | GAP |
| M2 | HIGH | No | GAP |
| M3 | HIGH | No | GAP |
| M4 | HIGH (source) / MEDIUM (co-occurrence) | Yes, if singleton-per-page is guaranteed | GAP |
| M5 | HIGH | No | GAP |
| M6 | HIGH | No | GAP |

Nothing was moved out of the findings list on confidence grounds. Everything unrated for lack of a stylesheet, an axe run, or a re-fetch is in Open Questions below rather than filed at a guessed severity.

**Calibration statement:** the parts of this component that are correct are called out and not counted against it — native `<button>` for the trigger, correct `aria-hidden` on the `▼` glyph, valid `aria-expanded` values, correct `listbox`/`option` role mapping on `ul`/`li`, `aria-controls` present at all, and a real label association (wrong mechanism, right instinct). This is not a component written carelessly; it is a component written by someone who knew the ARIA vocabulary and did not have a way to observe what assistive technology actually received.

---

## Verdict Justification

**REJECT**, not REVISE.

The distinction I am drawing: REVISE would be right if the pattern were sound and the implementation had gaps. Here, three independent CRITICALs each individually remove the control's core function for screen reader users — *which option am I on*, *which option did I choose*, and *where did I go* — and the sixth-of-eleven APG completion rate means there is no partial version of this that works. The focus architecture additionally needs re-deriving rather than patching: the single focus call in the component is provably unreachable, and the correct React implementation (effect-driven focus, or the select-only-combobox model where focus never leaves the trigger) is a different design, not a repaired line.

**What would make this ACCEPT-WITH-RESERVATIONS:** C1, C2, C3 fixed and verified with the instruments named below; M1–M6 fixed; the stylesheet supplied and the low-vision and contrast perspectives actually rated rather than deferred.

**What would make this REVISE instead of REJECT, hypothetically:** if C1 were the only CRITICAL — the focus bug alone, with a working `aria-activedescendant` and a value-bearing accessible name — this would be a REVISE with a one-line fix. It is the accumulation of three orthogonal AT-facing failures across three different phases of the review that makes the design unsound rather than incomplete.

**Recalibrations applied:** C3 held at CRITICAL with an explicit downgrade condition; M4 considered for upgrade and held at MAJOR; one candidate CRITICAL (`aria-controls`) downgraded to MINOR by measurement; two candidate findings declined outright (simulated-announcement silence; missing landmark) with reasoning recorded above.

**Escalation:** screen reader and keyboard-only at HIGH → `/perspective-audit`.

### Recommended architecture (rather than nine separate patches)

Adopt the APG **select-only combobox** wholesale. Focus never leaves the trigger; `aria-activedescendant` on the trigger tracks the cursor; the listbox is always in the DOM and toggled with `hidden`. That single change resolves C1 (nothing to restore — focus never left), C2 (activedescendant is the mechanism), M1 (no focus move to get wrong), M2 (one keydown handler on one always-focused element), M6 (focusout on one element), and m1 (the target always exists). C3, M3, M4, and M5 remain as separate, small fixes on top. Nine findings collapse to four.

### How to verify the fix — the instrument per evidence class

Closing the two instrument-class mismatches the digest flagged:

- **Focus restoration and Escape (keyboard-operability):** `npx playwright test` with real `page.keyboard.press('Escape')` and `page.keyboard.press('Enter')`, asserting `document.activeElement` resolves to the trigger on **both** paths. The Escape path is currently unmeasured and must be in this spec.
- **Accessible name and active-option announcements (name-role-state):** `@guidepup/virtual-screen-reader` component assertions — assert the spoken phrase after commit contains the newly chosen value, and that each ArrowDown emits a new option phrase. This is the prescribed instrument for this class and was not part of the supplied evidence.
- **Then re-run the `keyboard-a11y-tester` driven goal** with Escape in the path, and diff the trace against the one cited here. Confirm at minimum: `step_*.focus_moved` is `true` on expand; `ax_name_role_state.name` on `#dropdown-list` is non-empty; an active-descendant field appears and changes on each ArrowDown; the post-commit `active_element_selector` is the trigger, not `body`; and the trigger's name differs between the pre- and post-selection steps.
- **Add an axe-core scan** to close the structural half of the original question, which this evidence set cannot answer.

---

## Open Questions (unscored)

- **Q1 — Does a real screen reader announce the `aria-expanded` transition at step_0002?** The trace's simulated capture recorded `new_phrases: []` and `focus_announcement: null`. NVDA and JAWS normally announce "expanded" when the attribute flips on the focused element. Not filed as a finding — it needs `virtual-screen-reader` or a real-AT probe to settle. If real AT is *also* silent here, it becomes a genuine 4.1.2 finding at MAJOR.
- **Q2 — Was `step_0003` reached by `Tab`?** Determines whether M1's real-world cost is measured or only inferred. `jq '.steps[2].keystroke_sent'`.
- **Q3 — Does the trace's `computed_focus_style` satisfy 2.4.7 and 2.4.13 for the button and the listbox?** The one instrument that can measure focus-indicator sufficiency was run and the fields were not surfaced in the digest. `jq -c '[.steps[] | {step_id, computed_focus_style}]'`.
- **Q4 — Is `.selected` a color-only distinction?** If so, WCAG 1.4.1 fails. Needs the stylesheet.
- **Q5 — Does the open `.dropdown-list` overlay obscure the next focused element after a Tab-out (M6)?** Would add WCAG 2.4.11 to M6. Needs the stylesheet and a rendered check.
- **Q6 — Does the page host more than one instance of this component?** Settles M4's blast radius.
- **Q7 — Does a results region elsewhere on the page announce the sort change via `aria-live`?** Would soften C3's impact without repairing the stale accessible name. Worth asking the developer directly before they start work.
- **Q8 — Is there a product requirement that rules out a native `<select>`?** If not, E3 is the cheapest path to every fix in this document.
- **Q9 — What does `interactive-dropdown-focus-bug.findings.json` contain?** Same fixture, same directory, not opened. Read it before commissioning further measurement.
- **Q10 — Re-fetch confirmation for every `digest-only` citation above.** Handles are given inline; none were opened during this review, and each finding's code-read basis is stated separately so the re-fetch can only strengthen or narrow, not invent.
