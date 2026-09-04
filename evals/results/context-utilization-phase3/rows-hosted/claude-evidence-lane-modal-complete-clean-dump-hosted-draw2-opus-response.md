# Accessibility Design Review — Modal Dialog Component

**Line-reference convention:** `Modal.jsx:NN` = line N counted from `import React…` (first line of the JSX fence). `Modal.css:NN` = line N counted from `.modal-overlay {` (first line of the CSS fence). Trace citations use `trace.json <step_id>: <field>`.

---

**VERDICT: ACCEPT-WITH-RESERVATIONS**

**Overall Assessment**: This is a genuinely complete WAI-ARIA APG Modal Dialog implementation, and the driven trace measures — does not merely assert — the four behaviors that usually fail in hand-rolled modals: the dialog's name/role/modal state are announced on open, focus enters the dialog, Tab wraps at the boundary, and Escape restores focus to the trigger. I found no CRITICAL findings and I am not manufacturing one. The two MAJOR findings are not defects in the ARIA pattern; they are the two places where the component has no designed behavior for a foreseeable failure state — focus restoration when the trigger is gone, and keyboard access to the scroll container the CSS unconditionally creates. Both are additive fixes, not redesigns, which is why this is ACCEPT-WITH-RESERVATIONS rather than REVISE.

A second, separate finding concerns the evidence pack itself: 29 of the 30 supplied artifacts are for other pages, and the one relevant artifact contains an internal contradiction that invalidates a whole metric class. That is reported in Phase 0 because it changes what can be claimed as measured.

---

## Phase 0 — Test Evidence Intake

### What the pack actually contains for the component under review

**One artifact.** `evals/results/keyboard-a11y-tester/driven/modal-complete-clean.trace.json` — a 6-step `driven-live` session at 1280×800, personas `keyboard` + `screen-reader`, against `http://127.0.0.1:8777/modal-complete-clean.html`.

**Twenty-nine artifacts that are not.** Every `findings/*.json` file in the pack carries a different `url`: `accordion-no-region-role.html`, `app-focus-order-illogical.html`, `async-form-vague-success.html`, `breadcrumb-navigation-no-nav-landmark.html`, `button-skip-link-clean.html`, `checkbox-group-no-fieldset.html`, `combobox-autocomplete-no-listbox-role.html`, `dashboard-heading-inconsistency.html`, `data-table-missing-scope.html`, `expandable-section-no-button.html`, `file-input-no-labels.html`, `form-field-vs-summary-errors.html`, `form-validation-missing-aria-describedby.html`, `heading-hierarchy-skipped.html`, `image-carousel-no-region.html`, `infinite-scroll-no-announcement.html`, `interactive-dropdown-clean.html`, `interactive-dropdown-focus-bug.html`, `loading-state-missing-aria-busy.html`, `megamenu-no-structure.html`, `multistep-form-error-clearing.html`, `pagination-no-nav-landmark.html`, `popover-no-focus-management.html`, `radio-button-group-no-grouping.html`, `search-focus-stays-in-input.html`, `search-results-dynamic-clean.html`, `tabbed-nav-vs-tab-pattern.html`, `tabs-incomplete-aria-selected.html`, `tabs-missing-arrow-nav.html`.

None of these describe this component. **No finding in this review is derived from any of them.** Importing a sibling page's `sr-live-region-silent-desktop` or `focus-appearance-weak-desktop` row into a modal review would be fabrication dressed as evidence, and the volume of adjacent-but-irrelevant JSON in this pack is exactly the condition under which that happens.

**Notably absent: there is no `findings/modal-complete-clean.json`.** Its absence is not a clean bill of health. Four sibling files (`checkbox-group-no-fieldset`, `data-table-missing-scope`, `expandable-section-no-button`, `file-input-no-labels`, and others) do exist with `"findings": []`, which proves the harness emits a file even when it finds nothing. So I cannot distinguish "batch crawl ran and found nothing on this page" from "batch crawl was never run on this page." Treat this component's deterministic-findings status as **unknown**, not clean.

### Measured facts I am relying on

| Fact | Citation |
|---|---|
| Dialog role, name, and modal state announced on open | `trace.json step_0002: sr_announcement.new_phrases = ["dialog, Settings, modal", "button, Close dialog"]` |
| `aria-labelledby="modal-title"` resolves — dialog name computes to the `title` prop value | same step; name "Settings" matches `region.heading: "Settings"` at steps 0002–0005 |
| Focus enters the dialog on open (Enter on trigger → close button focused) | `trace.json step_0002: keystroke_sent "Enter", active_element_selector "body > div:nth-of-type(2) > div > div:nth-of-type(1) > button", focus_moved true` |
| Close button accessible name is the `aria-label`, not the `✕` glyph | `trace.json step_0002: ax_name_role_state.name = "Close dialog"`, while `text = "✕"` |
| Tab wraps at the trap boundary (last → first) | `trace.json step_0003` (Save changes, dom_order_index 23) → `step_0004` (Close dialog, dom_order_index 20), `focus_moved: true` |
| Escape closes the dialog and restores focus to the trigger | `trace.json step_0006: keystroke_sent "Escape", active_element_selector "#root > div > button", ax_name_role_state.name "Open settings", focus_moved true` |
| Close button target size 34.30 × 36 CSS px | `trace.json step_0002 / step_0004: bounding_box` |
| Close button focus indicator passes 2.4.13 (AAA) | `trace.json step_0002 / step_0004: focus_appearance {changed_area 300, ref_area_2px_perimeter 281, area_pass true, contrast 4.31, contrast_pass true, aaa_pass true}` |
| No live-region announcements fired at any step | `sr_announcement.live_announcements = []` on all six steps |

### Instrument caveat — `focus_appearance` is not stable in this trace

The trace contradicts itself on two elements:

- `#root > div > button` ("Open settings") — **step_0001**: `contrast 3.58, area_pass true, aaa_pass true`. **step_0006**: `contrast 3.14, area_pass false, aaa_pass false`. Identical selector, identical `bounding_box` (x 16, y 16, w 98.265625, h 21), identical `computed_focus_style`.
- `Save changes` — **step_0003**: `contrast 3.14, area_pass false, aaa_pass false`. **step_0005**: `contrast 4.74, area_pass true, aaa_pass true`. Identical selector, identical `bounding_box` (x 410, y 457.5, w 100.484375, h 21), identical `computed_focus_style`.

Both flipping elements use `outline_style: "auto"` (the UA-default indicator). The one element with an author-declared `outline: 2px solid` — the close button, `Modal.css:58-62` — measures byte-identically at both steps 0002 and 0004 (`300 / 281 / 4.31`).

**Consequence:** a single sub-threshold `focus_appearance` reading from this runner is not sufficient evidence to file a focus-appearance finding against a UA-default outline. I am therefore filing **no** 2.4.13 finding against the host page's trigger button, despite step_0006 reading `aaa_pass: false`. I am willing to rely on the close button's readings because they are reproducible across two steps. This caveat is not in the skill's four KAT calibration rules; it should be, and it is the reason a reviewer must read the trace rather than the summary line.

### KAT calibration rules applied

1. **Batch-crawl 4.1.3 "silent live region" findings are prompts, never failures.** Five sibling files carry `sr-live-region-silent-desktop` rows. All are for other pages; none is treated as a failure and none is imported here.
2. **Name-presence checks don't cover UA-intrinsic names.** Not triggered — the only named control in this component carries an explicit `aria-label`, measured resolved.
3. **Journey-level verdicts are judgment-layer.** The trace's `goals[0].intent` ("open the settings modal, then close it, verifying focus management") is a stated goal, not a measured pass. Every claim above is a per-step fact, not the journey verdict.
4. **`conformance_level` is a pass/fail gate, not the SC's WCAG level (upstream issue #27).** Confirmed in this pack: `sr-heading-skip-desktop` (1.3.1), `no-skip-link-desktop` (2.4.1), `positive-tabindex-desktop` (2.4.3), and `missing-accessible-name-desktop` (4.1.2) are all labeled `"AA"` — all four are Level **A** in WCAG 2.2. Only 2.4.13 is correctly `"AAA"`. Derive the level from the SC number. This matters here only prospectively, because no findings file for this page exists.

### Evidence coverage gaps

The trace establishes forward Tab, Enter activation, and Escape. It does **not** establish:

- **Shift+Tab reverse wrap.** `Modal.jsx:99-104` is code-read only. No step sends Shift+Tab.
- **Focus-outside recovery.** `Modal.jsx:93-97` is code-read only. No step puts focus on `<body>` and then Tabs.
- **Backdrop dismissal and the mousedown guard.** `Modal.jsx:120-135` is code-read only. No pointer step exists — the entire mousedown/click pairing that the fixture's Expected Behavior section leans on is unverified.
- **Focus restoration when the trigger is gone.** Not exercised; see MAJOR-1.
- **Any content overflowing `max-height: 80vh`.** The traced modal has 2 focusable stops and evidently fits. See MAJOR-2.
- **Zoom / reflow (1.4.10), forced-colors, and tool-measured contrast.** No axe scan, no `virtual-screen-reader` component assertions, no 200 %/400 % capture, no forced-colors capture. All contrast figures I give below are computed from the declared hex values, not measured — stated as such at each use.

---

## Phase 1 — Pre-commitment Predictions

Written before reading the source, using the protocol's modal-dialog prediction set plus my own:

1. Focus trap absent or partial (Tab escapes at one boundary, or Shift+Tab unhandled).
2. Focus does not restore to the trigger on close.
3. Backdrop is a clickable div that is either exposed to AT or has no keyboard equivalent.
4. Close button semantics wrong (`div role="button"`, or `✕` as the accessible name).
5. Hardcoded ARIA ids colliding when two instances render.
6. Escape bound globally with no topmost-dialog scoping.
7. Background not `inert`; reliance on `aria-modal` alone.
8. Body scroll lock set and never correctly restored.
9. Scroll container in the dialog not reachable by keyboard.

**Result of the comparison (Phase 10 in full below): predictions 1–4 — the four canonical modal failures — all came back clean, and three of the four are measured clean, not merely code-read clean.** That is the surprise in this review. Predictions 5, 6, 8, 9 landed. Prediction 7 landed as an enhancement rather than a finding, because `aria-modal` plus a document-level Tab handler is a defensible design.

---

## Phase 2 — Semantic HTML Audit

- **Native-first: satisfied.** The only interactive control the component owns is a real `<button>` (`Modal.jsx:153-159`). No `div role="button"`, no `span` with a click handler and a tabindex. The non-negotiable rule is not violated.
- **Overlay (`Modal.jsx:138-143`)** is a `div` with `role="presentation"`, no `tabindex`, carrying `onMouseDown`/`onClick`. This is the correct choice, not a violation: `role="presentation"` removes a purely decorative scrim from the accessibility tree, the element is not focusable, and the mouse-only dismissal it provides is duplicated by both Escape (`Modal.jsx:61-65`) and the close button. WCAG 2.1.1 requires the *functionality* to be keyboard-operable, and it is — twice over. `role="presentation"` is also correctly **not** inherited by the dialog child; the trace proves the dialog still reaches AT (`step_0002: "dialog, Settings, modal"`).
- **Heading:** one `<h2>` (`Modal.jsx:152`), used as the dialog's label. Level is hardcoded — see ENH-3.
- **Landmarks:** `region.landmark` is `null` at every trace step, including inside the dialog. This is **not** a finding. The dialog is portaled to `document.body` (`Modal.jsx:164`) and carries `aria-modal="true"`; a modal dialog is its own AT context and landmark membership is irrelevant while it is open. I note it because a reader skimming the trace for `landmark: null` would be tempted to file it.
- No lists, tables, or form controls are owned by the component. Nothing to audit there; those belong to `children`.

**No Phase 2 findings.**

---

## Phase 3 — ARIA Pattern Compliance Audit

Pattern: **WAI-ARIA APG Modal Dialog.** Checked attribute by attribute against the source:

| APG requirement | Present? | Evidence |
|---|---|---|
| `role="dialog"` on the container | Yes | `Modal.jsx:147`; measured `step_0002` |
| `aria-modal="true"` | Yes | `Modal.jsx:148`; measured as "modal" in `step_0002` |
| Accessible name via `aria-labelledby` → visible title | Yes | `Modal.jsx:149` → `Modal.jsx:152`; name resolves to "Settings" |
| Focus moves into the dialog on open | Yes | `Modal.jsx:38-42`; measured `step_0002` |
| Tab cycles forward within the dialog | Yes | `Modal.jsx:107-110`; measured `step_0003 → step_0004` |
| Shift+Tab cycles backward within the dialog | Yes (code-read) | `Modal.jsx:101-104` — not measured |
| Escape closes the dialog | Yes | `Modal.jsx:61-65`; measured `step_0006` |
| Focus returns to the invoking element | Yes | `Modal.jsx:50`; measured `step_0006` |
| Fallback focus target when no child is focusable | **No** | see ENH-5 |

ARIA values are valid: `aria-modal="true"` (not `"yes"`), `role="dialog"` (correctly `dialog` rather than `alertdialog` for a generic container — `alertdialog` is reserved for urgent, response-required messages and would be wrong as a default).

The pattern is **complete**, not 80 %. The single APG element absent is the no-focusable-children fallback, which is unreachable in this component because the close button is rendered unconditionally (`Modal.jsx:153-159`) — meaning `focusableElements.length === 0` at `Modal.jsx:81` is dead code in the shipped configuration. I am rating that as an enhancement, not a finding, for exactly that reason. Inflating it to CRITICAL on the strength of "no fallback focus target" would be a manufactured violation.

**No Phase 3 findings.**

---

## Phase 4 — Focus Management Review

The focus architecture is unusually deliberate, and the code comments show the reasoning rather than hiding it. Specifically worth crediting because each is a place implementations normally fail:

- **The save/restore lifecycle and the Escape listener are deliberately split into separate effects** (`Modal.jsx:32-53` vs `Modal.jsx:58-69`), with the comment at `Modal.jsx:55-57` explaining why: an unstable `onClose` identity (an inline arrow prop) re-binds only the Escape listener and never re-runs the focus save/restore. Collapsing these into one effect keyed on `[isOpen, onClose]` is the single most common way modals destroy their own focus restoration on every parent re-render. This is designed, not accidental.
- **The focusable set is recomputed on every Tab** (`Modal.jsx:80`), not captured once at open. Children added, removed, or disabled mid-session are handled.
- **`getClientRects().length > 0`** (`Modal.jsx:24`) prevents `display:none` elements from becoming wrap anchors — a real bug class, pre-empted.
- **The out-of-container recovery branch** (`Modal.jsx:93-97`) pulls focus back to the correct boundary depending on Shift state, rather than blindly to the first element. This branch also contains the damage from every trap leak described in MINOR-2 below: the next Tab keydown reaching `document` re-captures focus.
- **The `setTimeout(…, 0)` open-focus is guarded** by `if (!modalRef.current) return` (`Modal.jsx:39`), so an open-then-immediately-close within one tick does not throw or steal focus post-unmount.

Tab order is DOM order and matches visual order — close button (header, top-right, `dom_order_index 20`) then Save changes (`dom_order_index 23`). WCAG 2.4.3 satisfied, measured.

Focus indicators: the close button declares `outline: 2px solid #0066cc; outline-offset: 2px` (`Modal.css:58-62`). Computed contrast of `#0066cc` against the dialog's white background is **5.57:1** (computed from declared hex, not tool-measured), clearing the 3:1 bar of 2.4.11/1.4.11 with margin; the runner's own perimeter measurement agrees at 4.31 (`step_0002`, reproducible at `step_0004`). WCAG 2.4.7 satisfied.

**Two findings fall out of this phase and Phase 7 — MAJOR-1 and MAJOR-2 below.**

---

## Phase 5 — State Communication Audit

The component owns almost no state to communicate. Open/closed is communicated by the dialog's presence and by focus movement, which is the APG-correct mechanism.

- **On close, nothing is announced beyond the re-focused trigger** (`step_0006: new_phrases = ["button, Open settings"]`, `live_announcements: []`). **This is correct and I am explicitly not filing it.** A reviewer working from a checklist would demand an `aria-live` "Dialog closed" announcement. That would be wrong: focus movement to the trigger *is* the announcement in the APG Modal Dialog pattern, and an added live region would produce a redundant double-announcement on every close.
- **The `✕` glyph** (`Modal.jsx:158`) is the protocol's canonical "visual text symbol as state indicator" trap. Here it is neutralized: `aria-label="Close dialog"` (`Modal.jsx:156`) overrides the content, and the trace measures the computed name as `"Close dialog"`, not `"times"` or `"multiplication x"`. Not a finding. See ENH-4 for the defense-in-depth version.
- No loading, error, disabled, selected, or expanded state exists in this component. Those belong to `children` and are out of scope — stated here as a deliberate scope boundary, not an omission.

**No Phase 5 findings.**

---

## Phase 6 — Multi-Perspective Review

### Perspective Alarm Levels

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | MEDIUM | Hand-rolled `aria-modal` dialog rendered through a portal; name/role/state measured correct, but hardcoded `id="modal-title"` and an unguarded `title` prop are both unverified name-resolution risks |
| Keyboard-only | **HIGH** | Hand-rolled focus trap, hand-rolled restoration, and an unconditional CSS scroll container — MAJOR-1 and MAJOR-2 both live here |
| Low vision | MEDIUM | Dialog's only outer boundary is `box-shadow`, which forced-colors suppresses; close button 34.3 × 36 px passes 2.5.8 but is under the 44 × 44 recommendation |
| Cognitive | LOW | Three consistent dismissal affordances (Escape, close button, backdrop); no timeout; no destructive action owned by the component |
| Vestibular & motion | LOW | Only animation is `transition: color 0.2s` on the close button (`Modal.css:51`) — a colour fade, not a vestibular trigger. No entrance/exit animation, no parallax, no autoplay |
| Auditory access | LOW | No `<video>`, `<audio>`, or auditory alert owned by the component |
| Environmental contrast | MEDIUM | Forced-colors boundary loss (MINOR-3); text contrast computed passing but never tool-measured |

Keyboard-only (HIGH) and the three MEDIUM perspectives should be escalated to `/perspective-audit`. **Vestibular is LOW and I want to be explicit about why:** a 200 ms colour transition is not motion, and filing a `prefers-reduced-motion` finding against it would be a manufactured violation. There is no motion in this component to suppress.

Detail per perspective is in the Multi-Perspective Notes section near the end.

---

## Phase 7 — Gap Analysis (What Is Absent)

Walked against the protocol's absence checklist. Present and correct: focus restoration, focus trap, Escape handling, dialog role, accessible name, field associations (n/a), landmark reasoning (n/a under `aria-modal`), skip link (n/a), `aria-current` (n/a), composite widget role (n/a), reduced-motion (n/a — no motion), caption/transcript infrastructure (n/a — no media), `inert` (see ENH-2), CSS `visibility:hidden` focus-reveal catch-22 (not present), pseudo-element content exposure (no `::before`/`::after` in the stylesheet), font-icon exposure (none — the glyph is a text node with an overriding `aria-label`).

Genuinely absent:

1. **No fallback when the restore target is gone.** → MAJOR-1
2. **No keyboard path into the scroll container the CSS creates.** → MAJOR-2
3. **No id uniqueness strategy; no instance scoping for the document-level listeners or the scroll lock.** → MINOR-1
4. **No capture-phase binding, no positive-tabindex ordering, no `visibility:hidden` filter, no iframe strategy in the trap.** → MINOR-2
5. **No forced-colors boundary for the dialog.** → MINOR-3
6. **No `tabindex="-1"` on the dialog, despite CSS declaring a `:focus` style for it.** → ENH-5
7. **No guard on the `title` prop.** → ENH-3

Against the April 2026 third-party audit anti-pattern list: (1) broadcast-vs-association — n/a, no live regions; (2) `title` vs `aria-label` — clean, `aria-label` used, no `title` attribute anywhere; (3) ARIA without visible label — clean, the `aria-labelledby` target is the visible `<h2>`; (4) else-branch coverage — **checked and clean**: the Shift+Tab branch (`Modal.jsx:101-104`) and the Tab branch (`Modal.jsx:107-110`) are both implemented, and the out-of-container recovery (`Modal.jsx:95`) handles both Shift states; (5) single-selector scope — n/a; (6) `td`-in-loop row headers — n/a; (7) `role="presentation"` on data tables — n/a, the presentation role is on a scrim with no `<th>`; (8) decorative alt — n/a, no images; (9) DOM-verification — **satisfied by the trace**, which confirms `aria-labelledby` actually resolves rather than merely being present in source.

---

## Findings

### Critical Findings (blocks access)

**None.** Stated deliberately. Every mechanism that would produce a CRITICAL in this component type — missing trap, missing restoration, missing Escape, unnamed dialog, non-native close control — is present, and three of the five are confirmed by measurement rather than by reading. A CRITICAL here would have to be invented.

---

### Major Findings (significantly degrades experience)

#### MAJOR-1 — Focus restoration has no fallback when the previously focused element is gone, unfocusable, or detached

**Evidence:** `Modal.jsx:50` — `previouslyFocusedElement.current?.focus();` inside the cleanup at `Modal.jsx:47-51`. The saved value comes from `Modal.jsx:35` (`document.activeElement` at open time). There is no check that the saved node is still in the document, still visible, or still focusable.

**What happens:** `.focus()` on a node detached from the document, or on a node that has since become `disabled`/`display:none`, is a **silent no-op**. Nothing throws, nothing logs. Focus falls to `<body>`.

**Why this is not hypothetical:** the trigger being destroyed by the very action the modal performs is the single most common modal-in-a-CRUD-app pattern — a row's "Delete" button opening a confirmation dialog and the row unmounting on confirm; a cart item's "Remove"; an "Unpublish" action on a card that then disappears; any trigger inside a list that re-renders on save. For a general-purpose `Modal` accepting arbitrary `children` and an arbitrary `onClose`, this is a matter of when, not if.

**User group impacted:** keyboard-only and screen reader users. A keyboard user is dropped to the top of the document and must Tab from the beginning to get back to where they were. A screen reader user loses reading position entirely — the virtual cursor resets to the document start with no announcement explaining why.

**Expected behavior:** WCAG 2.4.3 Focus Order (Level A) — focus order must preserve meaning and operability. The WAI-ARIA APG Modal Dialog pattern is explicit that when the element that had focus before the dialog opened is no longer available, focus is moved to another element, usually a logical parent of where the trigger was.

**Confidence:** HIGH that the code has no fallback (directly readable at `Modal.jsx:50`). MEDIUM that it manifests frequently in any given consumer, since it depends on the consumer's `children` and `onClose`.

**Could the developer refute this?** Only by narrowing the component's contract — "this Modal is never used where the trigger can unmount." That is a documentation change, and it is not currently documented anywhere in the fixture's Expected Behavior list, which asserts flatly "Focus returns to trigger button when modal closes."

**Why this matters:** it is a silent failure. No test in the supplied pack would catch it. No automated scanner can catch it. It surfaces in production as the unactionable bug report "the page jumps to the top when I close the popup," which is why it survives for years.

**Fix:**
```js
return () => {
  document.body.style.overflow = '';
  const prev = previouslyFocusedElement.current;
  const restorable =
    prev && document.contains(prev) && prev.getClientRects().length > 0;
  if (restorable) {
    prev.focus();
  } else {
    // Documented, deliberate fallback — never leave focus on <body>.
    (fallbackRef?.current ?? document.querySelector('main, [role="main"]'))
      ?.focus();
  }
};
```
Give the component an optional `returnFocusRef` prop so consumers whose trigger is destined to unmount can name the replacement target explicitly (usually the list container or the heading above it), and give that fallback element `tabindex="-1"`.

---

#### MAJOR-2 — The dialog is an unconditional scroll container that keyboard users cannot scroll

**Evidence:** `Modal.css:14-23` — `.modal-dialog { max-height: 80vh; overflow-y: auto; }` (`max-height` at `Modal.css:20`, `overflow-y` at `Modal.css:21`). The scroll container is created for every instance regardless of content. Nothing in `Modal.jsx:144-150` gives that container `tabindex`, and the container is not returned by `getFocusableElements` in any case — `Modal.jsx:21` calls `container.querySelectorAll(...)`, which never matches the container itself.

**What happens when content overflows 80vh:** a keyboard-only user can Tab to the focusable controls, and the browser scrolls each into view — but the *non-interactive text between them* is unreachable. Tabbing from the close button (top) to a "Save changes" button (bottom) scrolls straight past the body copy. There is no keystroke that scrolls the region, because in browsers without keyboard-focusable scrollers the container is not a focus target and arrow keys therefore act on the document (which is `overflow: hidden`, `Modal.jsx:45`). The user can operate the dialog but cannot read it.

**User group impacted:** keyboard-only sighted users (motor impairment, tremor, no-mouse setups, speech input). Screen reader users are largely unaffected — the virtual cursor reads and auto-scrolls independently of the tab sequence.

**Expected behavior:** WCAG 2.1.1 Keyboard (Level A). Scrolling a region to read its content is functionality, and it must be operable from the keyboard. This is the same defect axe-core encodes as `scrollable-region-focusable` (serious impact) — worth naming because it means the finding is *machine-detectable*, and the reason it is not in this evidence pack is that no axe scan was supplied and the traced fixture's content does not overflow.

**Confidence:** HIGH on the mechanism (both the CSS declaration and the absence of any tabindex are directly readable). MEDIUM on frequency, because it manifests only when a consumer's content exceeds 80vh — which for a shared Modal is routine (terms text, changelogs, long settings forms, error detail).

**Realist Check — I considered downgrading this to MINOR and declined.** Chrome 127+ makes scrollable regions keyboard-focusable by default, which removes the defect for a large share of real users; Firefox and Safari do not. The recalibration rule permits a downgrade when a finding affects under 5 % of users or has a workaround, and the browser-share argument arguably clears the first bar. I kept it at MAJOR on the second: the "workaround" (Tab to the next control) *skips* the content rather than delivering it, so for the affected user the outcome is loss of access to content, not loss of convenience. A component should not rely on one browser vendor's default to meet a Level A criterion.

**Fix:** move the scroll to the body and make the body a tab stop, so it joins the trap's element set naturally (adding `tabindex="0"` to `.modal-dialog` would make it browser-tabbable but leave it *outside* `getFocusableElements`, desynchronising the trap boundaries — avoid that):
```jsx
<div className="modal-body" tabindex="0" role="group" aria-label={title}>
  {children}
</div>
```
```css
.modal-dialog { max-height: 80vh; display: flex; flex-direction: column; }
.modal-body   { overflow-y: auto; }
```
Ideally apply `tabindex="0"` only when the body actually overflows (a `ResizeObserver`/`scrollHeight > clientHeight` check), so non-overflowing dialogs do not gain a pointless tab stop.

---

### Minor Findings (friction, workaround exists)

#### MINOR-1 — Instance-global state: hardcoded ARIA id, unscoped scroll lock, unscoped listeners

Three symptoms, one root cause — the component assumes it is the only instance.

- **`id="modal-title"` is a literal** (`Modal.jsx:152`), referenced by a literal `aria-labelledby="modal-title"` (`Modal.jsx:149`). Two simultaneously open Modals produce two `#modal-title` nodes; `aria-labelledby` resolves to the first in document order, so the second dialog announces the **first dialog's title**. A screen reader user in a confirm-on-top-of-settings stack is told they are in the wrong dialog. WCAG 1.3.1 / 4.1.2. **Fix:** `const titleId = useId();` (React 18+) or a module-level counter.
- **`document.body.style.overflow = ''`** (`Modal.jsx:48`) is not refcounted and does not restore a prior inline value. Closing an inner modal unlocks background scroll while the outer modal is still open. **Fix:** refcount, and capture/restore the previous inline value rather than assigning `''`.
- **Both the Escape handler (`Modal.jsx:67`) and the Tab handler (`Modal.jsx:114`) bind to `document`** with no topmost-instance check. Two open modals means two Escape handlers — one Escape closes both — and two trap handlers fighting over the same keydown. **Fix:** a small module-level stack; only the top entry acts.

**Confidence:** HIGH on all three mechanisms; MEDIUM that stacking occurs in any given consumer. **GAP, not preference** — but MINOR, because a consumer that never stacks modals never sees any of it, and the code is otherwise correct for the single-instance case that the trace measured.

#### MINOR-2 — Four narrow escape hatches in the focus-trap boundary computation

Filed as one finding because they share one fix, and because splitting them into four would inflate the finding count without adding information.

1. **Bubble-phase binding.** `Modal.jsx:114` uses the default (bubble) phase. Any child that calls `e.stopPropagation()` on keydown — Monaco, CodeMirror, TipTap, most date pickers, many combobox libraries — silently disables both the trap and, via `Modal.jsx:67`, Escape. **Fix:** pass `true` as the third argument to both `addEventListener` calls (and their matching `removeEventListener`s) to bind in the capture phase.
2. **DOM order is assumed to equal tab order.** `Modal.jsx:86-87` takes `focusableElements[0]` and `[length - 1]` from `querySelectorAll` output, which is document order. A positive `tabindex` on any child sorts it ahead of everything else in the real sequential focus order, so the computed `lastElement` is not the real last stop and the wrap check at `Modal.jsx:107` never fires. Conditional on an anti-pattern that the harness itself flags elsewhere (`positive-tabindex-desktop`), but the assumption is unstated.
3. **`visibility: hidden` is not filtered.** `Modal.jsx:24` filters on `getClientRects().length > 0`, which correctly excludes `display: none` — but a `visibility: hidden` element still generates layout boxes and therefore still passes the filter, while being unfocusable. If such an element becomes the wrap anchor, `.focus()` is a no-op and Tab is swallowed at the boundary with focus stuck in place. **Fix:** add a `getComputedStyle(el).visibility !== 'hidden'` check.
4. **`<iframe>` is absent from `FOCUSABLE_SELECTOR`** (`Modal.jsx:7-18`), along with `object`, `embed`, and `details > summary`. Embedded video, maps, and payment forms are common modal content. The iframe case is the one that **no selector fix can close**: keydown events inside a cross-origin iframe's document never reach the parent's `document` listener, so the trap cannot observe the Tab that exits the iframe.

**Damage containment — worth crediting:** the out-of-container recovery branch at `Modal.jsx:93-97` heals items 2 and 4 on the *next* Tab, because once focus is on a background element, `!modalRef.current.contains(activeElement)` is true and focus is pulled back to the boundary. That is why this is MINOR rather than MAJOR: the leak is transient, not persistent. It is not fully healed — the user could activate the background control with Enter before Tabbing again — but they are not stranded.

**Confidence:** HIGH on the mechanisms, MEDIUM on manifestation. **Structural fix that closes all four at once:** replace boundary-comparison trapping with focus sentinels — a `tabindex="0"` span before and after the dialog whose `focus` handler redirects into the dialog — combined with `inert` on the background root (ENH-2). That architecture does not depend on enumerating focusables, does not depend on DOM order, and does not depend on observing keydown at all.

#### MINOR-3 — In forced-colors mode the dialog loses its only visual boundary — *Needs user verification*

**Evidence:** `.modal-dialog`'s separation from the page comes entirely from `background: white` (`Modal.css:15`), `border-radius: 8px` (`Modal.css:16`), and `box-shadow: 0 4px 16px rgba(0,0,0,0.2)` (`Modal.css:17`). There is no `border`.

**What happens:** forced-colors mode suppresses `box-shadow` outright and forces both `.modal-overlay`'s `rgba(0,0,0,0.5)` (`Modal.css:7`) and `.modal-dialog`'s `white` to the same system `Canvas` colour. `border-radius` carries no colour of its own. The result is dialog text floating on an undifferentiated field with no container edge and no visible dimming of the page behind it. The header's `border-bottom: 1px solid #eee` (`Modal.css:35`) does survive as a `CanvasText` rule, so a single horizontal line remains — which arguably reads as more confusing than no line at all.

**User group impacted:** low-vision users running Windows High Contrast / forced colors. They can still read and operate the dialog — text and focus indicators resolve to system colours — so this is disorientation, not blockage.

**Expected behavior:** the interface should function in forced-colors mode without losing information; the container boundary is information (it is what communicates "this is a separate, modal surface"). Related to WCAG 1.4.11 Non-text Contrast in spirit, though the forced-colors case is a robustness expectation rather than a criterion failure.

**Confidence:** MEDIUM. I am reasoning about forced-colors behaviour from the declared CSS; no forced-colors capture exists in the evidence pack. **Marked Needs user verification** — concrete check: enable Windows High Contrast (or Chrome DevTools → Rendering → Emulate CSS `forced-colors: active`), open the modal, and confirm whether the dialog has any visible edge.

**Fix:**
```css
.modal-dialog { border: 1px solid transparent; }
@media (forced-colors: active) {
  .modal-dialog { border-color: CanvasText; }
}
```

---

### Enhancements (best practice not met; no access barrier)

- **ENH-1 — Native-first points at `<dialog showModal()>`.** The skill's non-negotiable rule says ARIA must not replace available native semantics. `<dialog>` provides `role=dialog`, modal semantics, top-layer rendering, a `::backdrop`, native Escape, and native focus containment; it is baseline-available (Chrome 37+, Firefox 98+, Safari 15.4+). **I am filing this as an enhancement rather than a finding, deliberately.** The rule's teeth are aimed at `div role="button"` where the native element is a drop-in with strictly better behaviour. `<dialog>` is not a drop-in: its open-focus behaviour has shifted across versions, its Escape handling is not cancelable in the same way, and `::backdrop` styling is a real migration. This implementation is complete and measured correct, so the honest framing is "the native path would delete most of this file's risk surface, including MINOR-2 in full," not "this is a violation."
- **ENH-2 — `inert` on the background root.** `aria-modal="true"` plus the document-level Tab handler is a defensible design and I am not calling it a gap. Adding `inert` to the app root (or `#root`'s siblings) while the modal is open is nonetheless strictly stronger: it removes background content from the tab order at the browser level, which closes the iframe hole in MINOR-2 that no JS trap can reach, and it hardens against find-in-page and caret browsing.
- **ENH-3 — `title` is unguarded and the heading level is hardcoded.** `Modal.jsx:152` renders `{title}` into a fixed `<h2>`. An empty or `undefined` `title` yields an empty `<h2>`, `aria-labelledby` resolves to empty, and the dialog ships **with no accessible name** (WCAG 4.1.2). Add a required-prop guard or an `aria-label` fallback. Separately, expose a `headingLevel` prop; the hardcoded `h2` cannot be right for every host outline — though `aria-modal` suppresses the surrounding outline while open, so the practical impact is small.
- **ENH-4 — Wrap the `✕` glyph.** `<span aria-hidden="true">✕</span>` at `Modal.jsx:158`. The accessible name already computes correctly (measured, `step_0002`), so this is defense in depth against browse-mode reading of the raw text node, not a fix for a live defect.
- **ENH-5 — `.modal-dialog:focus` is dead CSS.** `Modal.css:25-28` declares a 3px focus outline for the dialog container, but the container has no `tabindex` (`Modal.jsx:144-150`) and can never receive focus. Either delete the rule or — better — add `tabindex="-1"` to the dialog, which makes the rule live *and* supplies the APG's no-focusable-children fallback focus target. That fallback is currently unreachable because the close button always renders (`Modal.jsx:153-159`), making `Modal.jsx:81-84` dead code — but it becomes reachable the moment a theme sets `.modal-close { display: none }`, at which point Tab is swallowed at `Modal.jsx:82` with focus outside the dialog and no way in (Escape still works, so this is not a 2.1.2 keyboard trap).
- **ENH-6 — Close button is 34.30 × 36 CSS px** (`trace.json step_0002: bounding_box`). This **passes** WCAG 2.5.8 Target Size (Minimum), which requires 24 × 24. It is below the 44 × 44 recommendation. Raising `padding` at `Modal.css:49` from `4px 8px` to roughly `10px` would clear 44 × 44 without changing the glyph. Enhancement only — the AA criterion is met, measured.

---

## What's Missing

- **A designed failure mode for focus restoration.** The component has restoration; it has no answer for restoration failing. (MAJOR-1)
- **A keyboard path into the scroll container the component itself creates.** (MAJOR-2)
- **Any instance-scoping strategy** — for the ARIA id, the body scroll lock, or the two document-level listeners. (MINOR-1)
- **A stated component contract.** No propTypes, no TypeScript, no documented invariants. Several findings above (`title` required; trigger must survive; children must not `stopPropagation` keydown; children must not use positive `tabindex`) are really unstated assumptions. Writing them down would convert three of them from latent defects into documented constraints.
- **A forced-colors boundary.** (MINOR-3)
- **Evidence for half the claimed behaviors.** The fixture's "Accessibility Features Implemented" list asserts eleven properties. The trace measures five of them. Shift+Tab wrap, out-of-container recovery, the backdrop mousedown/click guard, disabled/`tabindex="-1"` exclusion from the trap set, and "unaffected by parent re-renders" are all assertions, not measurements. The code supports each of them on reading — but the checklist reads as though they were verified, and they were not.

---

## Multi-Perspective Notes

**Screen reader user (NVDA, JAWS, VoiceOver):** The experience is good and largely measured. Activating the trigger produces `"dialog, Settings, modal"` followed by `"button, Close dialog"` (`step_0002`) — role, name, modal state, and the first control, in that order, which is exactly the APG-intended opening. The name comes from a real visible `<h2>`, not a floating `aria-label`, so the spoken name and the seen name are the same string. On close, focus returns to the trigger and the trigger re-announces (`step_0006`) with no live-region noise. `role="presentation"` correctly keeps the scrim out of the tree without suppressing the dialog inside it. Two unverified risks: stacked instances resolve `aria-labelledby` to the wrong title (MINOR-1), and an empty `title` prop produces an unnamed dialog (ENH-3). No `virtual-screen-reader` component-level assertions were supplied, so component-scope announcement behaviour outside this one journey is uncharacterized.

**Keyboard-only user:** This is where both MAJORs live, and it is the perspective to escalate. The happy path is measured working: focus enters on open, Tab cycles the two controls with a measured wrap at the boundary (`step_0003 → step_0004`), Escape closes and restores. The focus indicator on the close button is measured passing even the AAA 2.4.13 bar (`4.31` contrast, reproducible across two steps). What is not covered: a user reading long content cannot scroll it (MAJOR-2); a user closing a modal whose trigger has been destroyed is dropped to `<body>` (MAJOR-1); Shift+Tab is code-correct but never exercised. There is no keyboard trap in the 2.1.2 sense — Escape is bound at `document` and always escapes.

**Low vision user (200 % zoom, high contrast, magnifier):** Reflow is sound by construction — `width: 90%; max-width: 500px` (`Modal.css:18-19`) with `max-height: 80vh` and vertical-only overflow means no horizontal scroll is forced at zoom, satisfying 1.4.10 in principle (unmeasured; no zoom capture in the pack). Text contrast computed from the declared values: `#333` on white = **12.63:1** (`Modal.css:41`, `Modal.css:66`) and `#666` on white = **5.74:1** (`Modal.css:50`) — both clear the 4.5:1 text bar, and the close glyph at 24px additionally qualifies as large text. These are arithmetic on two opaque declared colours, not tool measurements; a scan would confirm them cheaply. Two real gaps: the forced-colors boundary loss (MINOR-3), and MAJOR-2 bites harder here, because a magnifier user reaches the 80vh overflow at far less content than a 1280×800 user does. The close button at 34.3 × 36 px passes 2.5.8 but is small for a tremor user (ENH-6).

**Cognitive accessibility:** Strong. Three consistent dismissal affordances — Escape, an explicitly labeled close button, and backdrop click — and the backdrop path is guarded so that a text-selection drag ending on the scrim does not destroy the user's work (`Modal.jsx:124-135`), which is a genuine cognitive-load protection that most implementations skip. No timeout, no cognitive function test, no destructive action owned by the component. The one caveat is a scope boundary rather than a finding: a consumer using this as a confirmation dialog owns WCAG 3.3.4 (Error Prevention) inside `children`; the component neither helps nor hinders. Worth noting that MINOR-1's "one Escape closes both stacked modals" would land hardest here — losing two levels of context to one keystroke is precisely the kind of unpredictability that costs cognitively disabled users the most.

---

## Phase 8 — Realist Check (Severity Calibration)

Applied to both MAJORs.

**MAJOR-1 (restoration fallback).** Worst realistic case: focus lands on `<body>`; a screen reader user loses their place in a long page and must re-navigate. Group: keyboard + screen reader. Detection: **never** by automated means, and slowly by user report — it is a silent no-op with no error signal. Proportionality: it is not complete access loss (the page remains fully operable from the top), so not CRITICAL; it is materially degrading and undetectable, so not MINOR. **MAJOR confirmed, no recalibration.**

**MAJOR-2 (unscrollable region).** Worst realistic case: a keyboard-only user in Firefox or Safari cannot read the middle of an overflowing dialog. Group: keyboard-only sighted users, plus speech-input users. Detection: fast *if* an axe scan is run against overflowing content (`scrollable-region-focusable`); otherwise slow. Proportionality: **I considered a downgrade to MINOR on the strength of Chrome 127+ making scrollable regions keyboard-focusable by default, and declined it** — the recalibration rule's "workaround" clause requires a workaround that delivers the outcome, and Tabbing past the content does not deliver the content. **MAJOR confirmed, downgrade considered and rejected on the record.**

**One severity was recalibrated downward during review:** the four focus-trap escape hatches (MINOR-2) were initially drafted as MAJOR on the strength of the iframe case. **Mitigated by:** the out-of-container recovery branch at `Modal.jsx:93-97`, which re-captures focus on the next Tab, making every leak in that group transient rather than persistent. Downgraded to MINOR.

**One finding was not filed at all after this check:** the `focus-appearance` sub-threshold readings at `step_0003` and `step_0006`. Both flip to passing when the identical element is measured again in the same session, both concern the host page's own buttons rather than the Modal component, and 2.4.13 is Level AAA. Filing it would be an instrument artifact promoted to a finding.

---

## Phase 9 — Self-Audit

| # | Severity | Confidence | Developer could refute with missing context? | Gap or preference? | Disposition |
|---|---|---|---|---|---|
| MAJOR-1 | MAJOR | HIGH (mechanism) / MEDIUM (frequency) | Only by narrowing an undocumented contract | GAP | Keep |
| MAJOR-2 | MAJOR | HIGH (mechanism) / MEDIUM (frequency) | Only by asserting Chrome-only support | GAP | Keep |
| MINOR-1 | MINOR | HIGH / MEDIUM | Yes — "we never stack modals" | GAP (conditional) | Keep at MINOR |
| MINOR-2 | MINOR | HIGH / MEDIUM | Yes — "children are controlled" | GAP (conditional) | Keep at MINOR |
| MINOR-3 | MINOR | MEDIUM | Possibly — I have no forced-colors capture | GAP | Keep, marked *Needs user verification* |
| ENH-1…6 | ENHANCEMENT | HIGH | n/a | Mixed | Kept as enhancements, not findings |

**No `A11y Evidence Finding` blocks are emitted, and that is deliberate.** The structured block is for CRITICAL/MAJOR findings *backed by measured evidence*. Both MAJORs here are design-reasoning findings; neither was exercised in the supplied trace. Emitting blocks would require inventing a `fingerprint` and dressing `source` as a test result, which is precisely the fabrication class the evidence contract exists to prevent. The measured facts in this review support the component's **correct** behaviors, not its defects — which is worth saying plainly, because it is the opposite of the usual shape.

**Calibration statement.** The ARIA pattern is correct and I have said so in Phases 2, 3, and 5 rather than burying it. Five specific things a checklist-driven review would have flagged here and that I am explicitly declining to flag: the `✕` glyph (name measured overridden), the absent close-announcement live region (focus movement is the correct mechanism), `prefers-reduced-motion` against a colour transition (not motion), `region.landmark: null` inside the dialog (irrelevant under `aria-modal`), and `:focus` instead of `:focus-visible` on the close button (`:focus` is the safer choice, not the worse one).

---

## Phase 10 — Synthesis: Predictions vs. Findings

| Prediction | Outcome |
|---|---|
| 1. Focus trap absent or partial | **Wrong.** Complete, including a recovery branch most implementations lack. Forward wrap measured. |
| 2. Focus does not restore | **Wrong.** Implemented and measured working (`step_0006`) — but with no fallback, which became MAJOR-1. |
| 3. Backdrop exposed / no keyboard equivalent | **Wrong.** `role="presentation"`, non-focusable, Escape provides the keyboard path, and the mousedown/click pairing guards against drag-dismiss. |
| 4. Close button semantics wrong | **Wrong.** Native `<button>`, `aria-label` overriding the glyph, name measured correct. |
| 5. Hardcoded ids collide | **Right.** MINOR-1. |
| 6. Escape bound globally, unscoped | **Right.** MINOR-1 / MINOR-2. |
| 7. No `inert` on background | **Partially right**, but downgraded to ENH-2 — `aria-modal` + document-level trap is defensible. |
| 8. Body scroll lock mishandled | **Right.** MINOR-1. |
| 9. Scroll container unreachable by keyboard | **Right.** MAJOR-2, and the finding I would most expect a review of this component to miss, because it lives in the stylesheet rather than the ARIA. |

**What surprised me:** the four canonical modal failures — the ones the protocol lists first and the ones that account for most real modal defects — are all absent here, and three are absent by measurement rather than by my reading. Everything I found lives one layer out: in the *failure modes around* a correct pattern (what happens when the trigger is gone, when content overflows, when a second instance opens, when a child eats the keydown), not in the pattern itself. That is a meaningfully different review than the usual "80 % of the ARIA pattern" outcome, and it is the reason the verdict is not REVISE.

**What I nearly missed:** MAJOR-2 is invisible from the JSX. Nothing in `Modal.jsx` suggests a scroll container exists; `max-height: 80vh; overflow-y: auto` is two lines in a stylesheet that a review focused on ARIA attributes never opens. A reviewer who read only the component and the trace would return a clean verdict.

---

## Verdict Justification

**ACCEPT-WITH-RESERVATIONS**, not ACCEPT and not REVISE.

Not REVISE, because REVISE would imply the accessibility design needs rework, and it does not. The APG Modal Dialog pattern is implemented completely, the focus architecture is deliberate (the split-effect design at `Modal.jsx:32-69` shows someone thought about React's re-render semantics, not just about ARIA attribute presence), and the measured evidence confirms role, name, modal state, focus entry, Tab wrap, and focus restoration. Both MAJOR findings are additive — a conditional guard in a cleanup function and one attribute plus a two-line CSS change. Neither touches the pattern.

Not ACCEPT, because both MAJORs will manifest in production for a shared component of this kind, and both fail silently. MAJOR-1 in particular has no detection path at all: no scanner finds it, no test in the supplied pack would catch it, and users report it in terms that do not identify it.

**To upgrade to ACCEPT:**
1. Add the restorability guard and a documented fallback target to `Modal.jsx:47-51` (MAJOR-1).
2. Move the scroll to `.modal-body` and make it a conditional tab stop (MAJOR-2).
3. Extend the evidence: one Shift+Tab step, one focus-outside-then-Tab step, and one overflowing-content run in the driven session; plus a single axe pass to confirm `scrollable-region-focusable` and the computed contrast figures.

**Escalation:** keyboard-only is HIGH and screen reader / low vision / environmental contrast are MEDIUM — send all four to `/perspective-audit`. If this component is destined to be a shared design-system primitive rather than an app-local one, resolve MINOR-1 before it ships, because the id collision and the shared scroll lock are the two things that become expensive to fix once consumers exist.

**Negative space — what this review does not cover.** It reviews the `Modal` component only. Everything inside `children` is out of scope: form validation and error association, `autocomplete` attributes, 3.3.4 confirmation semantics for destructive confirms, and any composite widget a consumer nests inside. Nothing here is an audit-scope conformance claim — this is a component-scope design review, so no WCAG-EM or ICT Testing Baseline framing applies and none is asserted. The trace establishes behavior at one viewport (1280×800), one browser engine, and one content configuration; mobile viewports, touch interaction, and overflowing content are entirely uncharacterized by the supplied evidence.

---

## Open Questions (unscored)

1. **Is this component ever used with two instances open at once?** MINOR-1's three symptoms are all conditional on that. If the answer is no and it is written down, MINOR-1 becomes a documented constraint rather than a defect.
2. **Was the batch crawl run against `modal-complete-clean.html`?** No findings file for this URL exists in the pack, and four sibling files prove the harness emits `"findings": []` when it finds nothing. I cannot distinguish "clean" from "not run," and I have not treated the absence as either.
3. **Is `focus_appearance` known to be unstable for `outline-style: auto` in this runner pin?** Two elements flip verdict across steps in a single session with identical bounding boxes and computed styles (`step_0001`/`step_0006`; `step_0003`/`step_0005`). If this reproduces, it is an instrument bug worth filing upstream and worth adding as a fifth KAT calibration rule — a single sub-threshold reading against a UA-default outline should not found a finding.
4. **Does `previouslyFocusedElement.current` reliably capture the trigger?** `Modal.jsx:35` reads `document.activeElement` inside a passive effect, i.e. after commit. If the click that opened the modal also triggered a re-render that unmounted or blurred the trigger, the captured value could already be `<body>`, and restoration would be a no-op even with MAJOR-1 fixed. Measured working in this trace (`step_0006`); flagged because the failure would be silent and the fix for MAJOR-1 would mask rather than resolve it.
5. **Should `role` be configurable?** `role="dialog"` is the correct default and `alertdialog` would be wrong as one. But a consumer building a destructive-action confirm wants `alertdialog`, and today they cannot get it. Low confidence that this is worth the API surface — raised for the developer, not filed.
6. **What is the intended contract for keyboard-consuming children?** MINOR-2's first item (bubble-phase binding) is the single highest-value one-character fix in this review — `addEventListener(..., true)` — but it changes interaction semantics for any child that deliberately handles Tab or Escape itself. Worth a decision rather than a silent change.
