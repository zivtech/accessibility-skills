# Accessibility Design Review — `BuggyFileInput` (file upload control)

**Line-number convention:** all `file:line` citations are relative to the component source as supplied in the review packet (`BuggyFileInput.jsx`, snippet line 1 = `import React...`). For anyone reading against the raw prompt file, snippet line N = prompt line N+7.

---

## Phase 0 — Consume Test Evidence

**Evidence inventory (21 artifacts attached; 3 in scope, 18 out of scope).**

In-scope, measured, and used below:

| Artifact | Type | Tier |
|---|---|---|
| `raw/axe-batch-2026-08-25/010-127-0-0-1-8777-file-input-no-labels-html.json` | axe-core 4.13.0, 1280x800, `status: measured`, HTTP 200 | Hard evidence |
| `raw/file-input-no-labels-kat-driven/trace.json` | keyboard-a11y-tester driven-live trace, personas keyboard + screen-reader, 3 steps | Hard evidence (per-step measured facts) |
| `raw/file-input-no-labels-kat-census/sr-census.json` | keyboard-a11y-tester reading-order census, `captured_at 2026-08-26T18:02:20Z`, `truncated: false` | Hard evidence |

Out of scope — **18 axe scans of sibling pages** in the same batch (`000` accordion, `001` app-focus-order, `002` async-form, `003` breadcrumb, `004` button-skip-link-clean, `005` checkbox-group, `006` combobox, `007` dashboard, `008` data-table, `009` expandable-section, `011` form-field-vs-summary, `012` form-validation, `013` heading-hierarchy, `014` image-carousel, `015` infinite-scroll, `016` interactive-dropdown-clean, `017` interactive-dropdown-focus-bug, `018` loading-state).

These describe **different URLs** and are not evidence about the component under review. Nothing in this review derives from them. Specifically **not** imported: the `target-size` violations on `accordion-no-region-role.html` and `image-carousel-no-region.html`, the `aria-valid-attr-value` incompletes on the two dropdown pages, the `color-contrast` violations on `dashboard-heading-inconsistency.html`, the `heading-order` violations, or the `bypass` incomplete on the breadcrumb page. Carrying any of those into this finding set would be fabricated evidence. Volume of attached artifacts is not evidence depth.

**What the in-scope evidence establishes:**

1. **axe (target page), violations:** `label` (impact **critical**, `node_count: 1`, `sample_selectors: ["input"]`, tags include `wcag2a`, `wcag412`, `section508.22.n`, `ACT`); plus `landmark-one-main`, `page-has-heading-one`, `region` — all three tagged `best-practice` only, i.e. **not WCAG failures**. `incomplete: []`, `passes_count: 11`, `inapplicable_count: 76`.
2. **Capture-state caveat (load-bearing):** the axe scan ran `2026-08-26T00:06:29Z`, in the component's initial state. The error branch renders conditionally (`BuggyFileInput.jsx:25`), so the error `<div>` was almost certainly **absent from the DOM during the axe run**. Consequences: axe's empty `incomplete: []` and the absence of any `color-contrast` entry are **not** evidence that `.error-message` styling passes — that element was never measured. The census (captured ~18 hours later, `18:02:20Z`) *does* show the error text present. Treat the axe run and the census as two different page states; I do not fuse them into a single claim anywhere below.
3. **KAT trace:** `step_0001` Tab → `#root > div > input`, `ax_name_role_state.name: "Choose File"`, `role: "button"`, `states.invalid: "false"`, `focus_moved: true`, box `253x21`, `computed_focus_style.outline_style: "auto"`, `focus_visible.visible: true`, `focus_appearance {changed_area: 1107, ref_area_2px_perimeter: 1096, area_pass: true, contrast: 4.86, contrast_pass: true, aaa_pass: true}`, `region: {landmark: null, heading: null}`, `ancestor_boxes: []`. `step_0002` Tab → `body` (input is the only tab stop). `step_0003` Shift+Tab → back to the input, identical measured focus values.
4. **KAT calibration rule 2 fires exactly as documented.** Name-presence checks do not cover UA-intrinsic names: the trace reports `name: "Choose File"` — that string is Chromium's built-in shadow-DOM button text for `<input type="file">`, not an author-supplied label. The AX tree showing a name here is **not** counter-evidence to the axe `label` violation; the two are consistent. Any reviewer who reads `name: "Choose File"` as "the control is labeled" has been trapped by the exact case this calibration rule exists for.
5. **KAT census:** three entries only — `document`, `"Upload file"`, `"File too large"`. `declared_live_regions: []`, `declared_broken_aria_refs: []`, `declared_alternate_reading_order: []`, `truncated: false`. The empty live-region list is direct measured evidence for the announcement finding below. The empty broken-ARIA-refs list is consistent with there being **no** ARIA relationships at all rather than broken ones.
6. **Census data quality limitation:** entries 2 and 3 carry `role` values identical to their `spoken_phrase` and `tag: null / selector: null`. That is degraded/echoed field data. I use those two entries only for the fact that the phrases appear in the reading order as free-standing text — I do **not** infer element type or DOM position from them.
7. **Coverage gaps in the supplied evidence** (stated so no one reads absence as a pass): no `deterministic-findings.json` was supplied, so there are no KAT judgment-layer findings to accept or reject; no keystroke other than Tab/Shift+Tab was exercised, so **Enter/Space activation of the file picker was never measured**; no stylesheet was supplied, so `.file-upload` and `.error-message` rendering is unverified; no zoom/reflow or forced-colors capture exists; and no real-AT (NVDA/JAWS/VoiceOver) pass exists — the census is an emulated screen reader.

This is not a fix/remediation review, so the a11y-test Verification evidence contract type-match check does not apply.

---

## Phase 1 — Pre-commitment Predictions

Component type: **native file input with client-side validation and a conditionally rendered error message.** Before reading the source, the five most likely design failures for this type:

1. The visible caption is a `<div>`, not a `<label for>` — no programmatic name; the control relies on the UA's "Choose File".
2. The error message is not associated with the input (no `id` + `aria-describedby`).
3. The error is not announced (no `role="alert"` / `aria-live`) — silent failure after user action.
4. `aria-invalid` never set, so the field reports itself as valid while visibly showing an error.
5. Constraints (accepted types, max size) exist only in `accept` and in JS — no visible or programmatic instructions before the user fails.

Secondary predictions: no success confirmation; error text describes the problem without stating the limit or the remedy; focus behavior after the OS picker closes undefined.

**Result: 5/5 primary predictions confirmed, plus both secondaries.** Two things I did not predict and the evidence forced: (a) the keyboard/focus layer is **measurably clean** — this component's entire defect surface is naming and state communication, not operability; (b) the reject branch leaves component state and the control's displayed value in contradiction (Major 4), which is a design decision no automated tool would surface.

---

## Phase 2 — Semantic HTML Audit

- **Native element used correctly.** `<input type="file">` (`BuggyFileInput.jsx:20-24`) is the right element. No `div role="button"`, no ARIA replacing native semantics, no re-implemented picker. The non-negotiable "native HTML first" rule is **satisfied** — say so plainly; this is the one structural decision the component gets right, and it is the reason every finding below is additive rather than a rewrite.
- **`<div>Upload file</div>` (`:19`) is a caption, not a label.** No `htmlFor`, no `id` on the input, no nesting, no `aria-labelledby`. This is the classic "text that looks like a label to sighted users and is nothing to the accessibility tree" pattern. Confirmed by axe `label` (critical) with `sample_selectors: ["input"]`. Reported as Critical 1.
- **Wrapper `<div className="file-upload">` (`:18`)** carries no semantics. For a single control this is acceptable; it is not a grouping that needs `<fieldset>`.
- **No heading, no landmark** on the host page. axe reports `landmark-one-main`, `page-has-heading-one`, `region` — all `best-practice`-tagged, and the trace corroborates (`region: {landmark: null, heading: null}`). This is a **fixture-harness artifact**: the component is mounted standalone into `#root` with no page shell. Flagging these as component defects would be a manufactured violation. Recorded as an Enhancement with that caveat attached.
- No tables, no lists, no images, no media in this component — the corresponding audit branches are inapplicable, not silently skipped.

---

## Phase 3 — ARIA Pattern Compliance Audit

There is **no ARIA in this component at all** — zero attributes across `:18-30`.

- **No APG widget pattern applies.** `<input type="file">` is a native form control, not a composite widget; there is no Combobox, Listbox, Disclosure, or Dialog pattern to complete. The relevant reference is the WAI-ARIA APG **form/field labeling and error-message guidance**, not a widget pattern. Citing a widget pattern here would be pattern-matching against the wrong model.
- **Consequence:** there is no "80% complete pattern" failure mode to report. What is missing is the field-level contract every form control owes AT: accessible name, description, validity state. That contract is 0% implemented.
- **No invalid ARIA values** — there are none to be invalid. `declared_broken_aria_refs: []` in the census is consistent.
- **No roving tabindex needed** (single control), no `aria-modal`, no `aria-controls` obligations.

Nothing in this phase is a finding on its own; the substance lands in Phase 5.

---

## Phase 4 — Focus Management Review

This is the phase where the component is **measurably clean**, and it should be recorded as such.

| Check | Measured value | Verdict |
|---|---|---|
| Tab reaches the control | `trace.json step_0001`: Tab → `#root > div > input`, `focus_moved: true` | PASS |
| Tab order logical | Single tab stop; `step_0002` Tab → `body` | PASS (trivially) |
| No keyboard trap (2.1.2) | `step_0003` Shift+Tab returns to the input, `focus_moved: true` | PASS |
| Focus visible (2.4.7) | `focus_visible.visible: true`, `indicator: "outline"`, `style_cue` + `pixel_cue` + `shape_cue` all true | PASS |
| Focus appearance (2.4.13, AAA) | `changed_area: 1107` vs `ref_area_2px_perimeter: 1096` → `area_pass: true`; `contrast: 4.86` → `contrast_pass: true`, `aaa_pass: true` | PASS |
| Focus not obscured (2.4.11) | `ancestor_boxes: []` — nothing overlaying the focused control | PASS at this page complexity |
| Positive `tabindex` | `tabindex: null` on the focused element | PASS |

Two honest qualifications:

- The focus ring is the **UA default** (`outline_style: "auto"`, `outline_color: rgb(0, 95, 204)`), not an author decision. It passes here; it will need re-measuring the moment a design system applies a global `outline: none` or restyles the control. This is a measured pass on borrowed credit, not a design achievement.
- **Enter/Space activation was never exercised** by the driven session. Native file inputs open the picker on Enter/Space, so the expected result is a pass, but "expected" is not "measured." Named in the coverage gaps.

**No focus-management finding is filed.** There is no modal, no dynamic focus move, no async CRUD, no SPA route change, and — importantly — **no focus move is required when the error appears**: the error renders adjacent to the control the user just operated, and focus is already there. Moving focus to the error would be the wrong fix. The correct fix is announcement + association (Critical 2), not focus manipulation. Recommending a focus move here would be a pattern applied because it is familiar, not because it fits.

---

## Phase 5 — State Communication Audit

This is where the component fails.

| State | Communicated visually? | Communicated to AT? | Evidence |
|---|---|---|---|
| What the control is for | Yes — `<div>Upload file</div>` `:19` | **No** | axe `label` critical; no `for`/`id`/`aria-label*` at `:19-24` |
| Accepted file types | Only via the OS picker's filter (`accept` `:23`) | **No** | No visible help text, no `aria-describedby` |
| Maximum file size | **Nowhere** until after failure | **No** | `5000000` exists only at `:9` |
| Validation error | Yes — `:25-29` | **No announcement, no association** | census `declared_live_regions: []`; no `id`/`aria-describedby` |
| Field validity | Red styling implied by class name | **No** | `states.invalid: "false"` (`step_0001`); `aria-invalid` never set anywhere in source |
| Successful selection | Partially — UA writes the filename into the control | Partially — via the control's value, on next focus | `trace.json step_0001 text: "C:\\fakepath\\quarterly-report.pdf"` |
| Rejected-file state cleared | **No** — control still displays the rejected filename | **No** | `:9-14`: reject branch never resets the input |

No visual text symbols (`+`, `×`, `>`) are used as state indicators, so that check is clean.

---

## Phase 6 — Multi-Perspective Review

**Screen reader user (NVDA / JAWS / VoiceOver).** Tabbing to the control announces approximately *"Choose File, button"* — the UA's boilerplate, identical for every file input in existence. Nothing conveys that this is the upload for anything in particular. In browse mode the user will encounter the free-standing phrase `"Upload file"` immediately before it (census entry 2), which is a partial mitigation on this one-field page — and which evaporates in forms mode, in NVDA's Elements List, in JAWS's form-field list (F key / `INSERT+F5`), and in any real form with two file fields ("résumé" vs "cover letter"). When the size check rejects a file, the census shows `"File too large"` enters the reading order (entry 3) inside **no live region** (`declared_live_regions: []`) — so the user hears nothing at all. They believe the upload succeeded. Returning to the field later, the AX tree still reports `invalid: "false"` and the control's value still reads back the rejected filename. Every channel this user has agrees the upload worked. It did not. **Alarm: HIGH.**

**Keyboard-only user.** Reaches the control on the first Tab, focus indicator measured visible and above the 2.4.13 AAA threshold (contrast 4.86, area 1107 ≥ 1096), Shift+Tab returns cleanly, no trap, no positive tabindex. Operability is not the problem here, and I am not going to invent one. The unresolved item is coverage, not defect: the driven session never sent Enter or Space, so picker activation is unmeasured. **Alarm: MEDIUM** — trigger is the unmeasured activation path, not an observed failure.

**Low vision user (200% zoom, magnifier, forced colors).** The control is 253x21 CSS px at 1280x800 — a short, low-contrast-by-default native widget that a magnifier user will have to hunt for, sitting directly under a caption that is not programmatically tied to it, so a magnified viewport can easily show the control without its caption. The error text's contrast is **unverified**: no stylesheet was supplied, and axe's `incomplete: []` on this page carries no information about `.error-message` because that element was not in the DOM at scan time. If `.error-message` is red-on-white with no icon or prefix, the error is signalled by color alone (1.4.1). Neither claim is provable from the evidence given, so both go to Open Questions rather than into the finding list. **Alarm: MEDIUM.**

**Cognitive accessibility user.** The two constraints that govern success — max 5 MB and PDF/DOC/DOCX only — are invisible until violated. The size limit is expressed nowhere in the UI at all; it lives at `:9` as `5000000`. When it is violated, the message is `"File too large"`: it names the problem and neither the threshold nor the remedy. The user is placed in a blind retry loop (WCAG 3.3.3 Error Suggestion, Level AA — the suggestion *is* known and is withheld). Compounding it: the rejected filename remains displayed in the control, so the interface simultaneously says "this file is chosen" and "this file is too large." For a user who processes one signal at a time, that contradiction is the whole experience. **Alarm: HIGH.**

**Vestibular & motion sensitivity.** No animation, transition, parallax, or auto-playing content in the source. No `prefers-reduced-motion` obligation arises. Caveat: no stylesheet supplied, so a CSS-only transition on `.error-message` cannot be excluded. **Alarm: LOW.**

**Auditory access.** No `<video>`, no `<audio>`, no auto-playing media, no sound-only alerts. Genuinely inapplicable. **Alarm: LOW.**

**Environmental contrast.** No contrast ratio for any component content was measured (see the capture-state caveat). The only measured ratio in the entire packet is the *focus indicator's* 4.86 — that is a focus-appearance measurement, not text contrast, and must not be reported as if it covered the error text. Forced-colors behavior unknown. Color-alone risk on `.error-message` unresolved. **Alarm: MEDIUM.**

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | **HIGH** | No accessible name beyond UA boilerplate; `declared_live_regions: []` with an error in the reading order; `invalid: "false"` in the error state |
| Keyboard-only | **MEDIUM** | All measured checks pass; Enter/Space picker activation unmeasured |
| Low vision | **MEDIUM** | Caption not programmatically bound to a 253x21 control; `.error-message` contrast unmeasured (element absent at scan time) |
| Cognitive | **HIGH** | Constraints undisclosed pre-failure; error names no threshold and no remedy; control keeps displaying the rejected file |
| Vestibular & motion | **LOW** | No motion in source (CSS unsupplied) |
| Auditory access | **LOW** | No media elements |
| Environmental contrast | **MEDIUM** | No component contrast measured; possible color-only error signal |

**Escalation:** Screen reader and Cognitive are HIGH; Keyboard-only, Low vision, and Environmental contrast are MEDIUM. Per the escalation rule, this component warrants a deep pass via `/perspective-audit`, and the low-vision / contrast questions need a run with a stylesheet loaded and the error branch forced open before they can be resolved either way.

---

## Phase 7 — Gap Analysis (What Is Absent)

- No `<label>` element anywhere in the component.
- No `id` on the input — nothing for `for` or `aria-describedby` to point at.
- No help/instructions element for accepted types or the size limit.
- No `aria-describedby` on the input (would need to reference help text **and** error, space-separated).
- No `aria-invalid` toggle.
- No live region of any kind — corroborated measured: `declared_live_regions: []`.
- No `role="alert"` / `role="status"` container.
- No success confirmation announcement after an accepted file (partially covered by the UA writing the filename into the control's value — which is why this is an Enhancement, not a Major).
- No reset of the control when a file is rejected.
- No type validation in JS — `accept` at `:23` is a picker filter only, trivially bypassed by choosing "All Files"; `handleFileChange` checks size and never checks type.
- No indication of whether the field is required.
- `selectedFile` state (`:4`, set at `:12`) is **never rendered or read anywhere** — dead state. Not an a11y defect in itself, but it means the component has no application-level confirmation surface at all; every confirmation the user gets is the browser's, not the app's.
- No stable-id strategy for the fix: if this component is ever rendered twice on a page, hardcoded `id="file-upload"` collides and `for`/`aria-describedby` resolve to the wrong element. Use `useId()`.

**Anti-pattern checks from the April 2026 third-party audit** — applied to the *fix*, since these are the ways this exact remediation is usually rejected on re-test:

- **#1 Broadcast vs. Association.** One field, one error → `role="alert"` on the error container is correct here and is *not* the per-field-broadcast anti-pattern. But it must be paired with `aria-describedby`, not substituted for it: alert fires once at render time; `aria-describedby` is what re-reads the error when the user returns to the field.
- **#3 ARIA without visible label.** The fix must keep `Upload file` visible and convert it to a real `<label>`. Adding `aria-label="Upload file"` to the input while leaving the `<div>` in place would satisfy axe and still be the wrong fix — a hidden name diverging from visible text.
- **#9 DOM verification required.** Verify in the rendered DOM (not a unit test) that `for` resolves to the input's `id`, that `aria-describedby` resolves to *both* target ids, and that `aria-invalid` lands on the `<input>` and not the wrapper.
- **Conditional-mount alert trap (not in the numbered list but the higher-frequency failure here).** `{error && <div role="alert">…</div>}` mounts the node with its text already inside. Several AT/browser combinations do not announce a live region that appears already populated. Render the container **unconditionally** and inject the text into it. This is the difference between a fix that tests green and a fix that speaks.

Nothing in the component matches anti-patterns #2, #4, #5, #6, #7, or #8.

---

## Phase 8 — Realist Check (Severity Calibration)

**Critical 1 (no label).** Worst realistic case: a screen reader user navigating by form field encounters an unidentifiable "Choose File button" and cannot determine what to upload. Groups: screen reader, and low vision at magnification (caption can scroll out of view). Detection if shipped: **fast** — axe catches it in CI at critical impact. Proportional? I considered downgrading to MAJOR on the grounds that browse-mode adjacency to `"Upload file"` (census entry 2) gives a linear reader the context. I rejected the downgrade: form-field-list and forms-mode navigation are the primary modes for form completion, and in both the control's identity is completely absent, not merely degraded — and a Level A 4.1.2/1.3.1 failure on the *identity* of a control is access loss, not inconvenience. **Stays CRITICAL.**

**Critical 2 (error neither announced nor associated).** Worst realistic case: the user selects a file, hears nothing, and leaves believing the upload succeeded. Silent failure with a false success signal is the worst shape a validation defect can take. Groups: screen reader primarily; cognitive secondarily. Detection if shipped: **never, silently** — no automated rule fires (axe reported nothing here), and the user does not know to report it. Survives all four questions. **Stays CRITICAL.**

**Major 1 (`aria-invalid` never set).** Worst case: on returning to the field, AT reports the field as valid while it visibly is not. Real, but the user who has *already been told* about the error (once Critical 2 is fixed) is not blocked by this alone. Not access loss on its own. **Stays MAJOR** — and note it must be fixed in the same change as Critical 2, or the fix is half-done.

**Major 2 (constraints undisclosed).** Affects **all** users, not a subgroup; the size limit exists nowhere in the interface. There is a workaround (fail, then retry), which is exactly the failure the SC exists to prevent. Detection: slow — surfaces as support tickets, not test failures. **Stays MAJOR.**

**Major 3 (error text is not a suggestion).** I checked this against the "has a workaround → downgrade to MINOR" rule. Trial-and-error is a workaround, so the rule is in play — but it applies to issues affecting <5% of users, and this affects 100%, compounding for cognitive and screen reader users who get the least information from a retry loop. The threshold is known to the code and withheld from the user; 3.3.3 is Level AA. **Stays MAJOR.**

**Major 4 (rejected file still displayed as chosen).** Worst case: interface state contradicts itself; the control's value asserts success while the message asserts failure. Groups: all, most acutely cognitive and screen reader. Detection: **never automated.** Considered downgrading to MINOR since a sighted user reading both lines can reconcile them — rejected, because for the AT user the contradiction is not visible-and-reconcilable, it is the only signal they have and it is the wrong one. **Stays MAJOR.**

**Minor 1 (accept is not enforced).** Downgraded from an initial MAJOR. *Mitigated by:* the OS picker's filter is the default path, so the bypass requires a deliberate "All Files" switch; and any competent server rejects the type regardless. It becomes MAJOR if server-side rejection is the only feedback path and it is not surfaced back into this control. **Downgraded to MINOR.**

**Landmark / heading / region axe entries.** *Mitigated by:* all three are `best-practice`-tagged, not WCAG-mapped, and are artifacts of a component mounted standalone into `#root` with no page shell. **Held at ENHANCEMENT with the harness caveat**, not counted toward the verdict.

---

## Phase 9 — Self-Audit

| Finding | Confidence | Refutable with dev context? | Gap or preference? |
|---|---|---|---|
| Critical 1 — no label | HIGH | No — axe `label` critical + source | GAP |
| Critical 2 — error not announced/associated | HIGH | No — `declared_live_regions: []` + source | GAP |
| Major 1 — no `aria-invalid` | HIGH | No — absent in source; trace shows `invalid: "false"` | GAP |
| Major 2 — constraints undisclosed | HIGH | No — `5000000` exists only at `:9` | GAP |
| Major 3 — error text not actionable | HIGH | Partially — copy may be owned by content, not code | GAP (ownership may sit with a content author) |
| Major 4 — rejected file still displayed | MEDIUM-HIGH | Possibly — a parent may reset the input via `key` or a ref | GAP |
| Minor 1 — `accept` not enforced | MEDIUM | Yes — server-side validation may exist out of frame | GAP, correctly de-rated |
| Enhancement — landmarks/heading | HIGH that axe reported it; LOW that it is a *component* defect | Yes — harness artifact | Held as ENHANCEMENT |

Moved to Open Questions on this pass: `.error-message` contrast; color-alone error signalling; the picker-cancel path; 2.5.8 target size. Each is stated there with the specific check that would settle it.

Explicitly **not** filed, to keep this calibrated: no focus-management finding (measured clean), no ARIA-pattern finding (no widget pattern applies), no keyboard-operability finding, no 2.4.7/2.4.13 finding (measured pass), no 1.3.5 `autocomplete` finding (no autocomplete token applies to `type="file"`), no 2.5.7 dragging finding (no author-implemented drag interaction), and nothing carried over from the 18 sibling-page scans.

---

# VERDICT: REVISE

**Overall Assessment**: The component makes the single most important structural decision correctly — it uses the native `<input type="file">` rather than a re-implemented picker — and the measured keyboard and focus layer is clean, including a 2.4.13 AAA-passing focus indicator. Everything else that assistive technology needs is absent: the control has no accessible name beyond the browser's boilerplate "Choose File", and a validation failure is neither announced nor associated with the field, so a screen reader user is told nothing when their upload is rejected and every remaining signal tells them it succeeded. All findings are additive fixes to correct markup, not a redesign.

**Pre-commitment Predictions**: 5/5 primary predictions confirmed (missing label, missing association, missing announcement, missing `aria-invalid`, undisclosed constraints), plus both secondaries (no success announcement, non-actionable error text). Two surprises: the focus/keyboard layer measured entirely clean, which narrows the defect surface to naming and state communication and rules out the focus-management fixes one would reflexively reach for; and the reject branch leaves component state and the control's displayed value contradicting each other (Major 4), which no scanner in the packet detected.

---

## Findings

### Critical Findings (blocks access)

**Critical 1 — File input has no programmatic label; its only accessible name is the browser's boilerplate.**

`BuggyFileInput.jsx:19` renders `<div>Upload file</div>`. `BuggyFileInput.jsx:20-24` renders the input with `type`, `onChange`, and `accept` and **no** `id`, `aria-label`, or `aria-labelledby`; the caption has no `htmlFor` and does not wrap the control. Measured: axe `label`, impact **critical**, `node_count: 1`, `sample_selectors: ["input"]`. The KAT trace's `name: "Choose File"` (`step_0001`) is the Chromium UA-intrinsic name, not a label — per KAT calibration rule 2, a name-presence check does not cover this case, and the two artifacts agree rather than conflict.

- **User group**: screen reader (primary); low vision at magnification (secondary — the caption can leave the viewport while the 253x21 control remains).
- **WCAG**: 1.3.1 Info and Relationships (A), 4.1.2 Name, Role, Value (A), 3.3.2 Labels or Instructions (A).
- **Confidence**: HIGH.
- **Why this matters**: In forms mode, and in NVDA's Elements List or JAWS's form-field list, this control announces as "Choose File, button" — a string identical for every file input on the web. The user cannot tell what to upload. On a real form with two file fields, they cannot tell the fields apart at all.
- **Fix**: `<label htmlFor="file-upload">Upload file</label>` at `:19` and `id="file-upload"` on the input at `:20`. Keep the text visible — do not substitute `aria-label` on the input while leaving the `<div>` (audit anti-pattern #3). Generate the id with `useId()` so multiple instances cannot collide.

*Evidence-block note: `fingerprint` values below are content-derived identifiers assigned by this review, not tool-computed hashes. Recompute them with the evidence harness before these findings enter a trend series.*

```
### A11y Evidence Finding
finding_id: file-input-no-programmatic-label
fingerprint: a1f3c07d9b2e4856
source: axe-core 4.13.0 rule `label` — raw/axe-batch-2026-08-25/010-127-0-0-1-8777-file-input-no-labels-html.json; BuggyFileInput.jsx:19-24
wcag_or_apg: WCAG 2.2 1.3.1 (A), 4.1.2 (A), 3.3.2 (A)
section_508_fpc_context: Not in scope — no declared Revised Section 508 engagement. axe tags the rule `section508.22.n` as context only. Noted for completeness: 1.3.1 and 4.1.2 are WCAG 2.0 Level A, so this finding would also map to a 508 failure if a federal scope were declared.
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, low-vision=MEDIUM, keyboard=MEDIUM, cognitive=HIGH
evidence: axe violation id `label`, impact critical, node_count 1, sample_selectors ["input"]; trace.json step_0001 ax_name_role_state.name = "Choose File" (UA-intrinsic, KAT calibration rule 2); sr-census.json entry 2 "Upload file" present as free-standing text with no association
reproduction_steps: Load http://127.0.0.1:8777/file-input-no-labels.html; press Tab once; inspect the accessibility tree for the focused input, or open NVDA Elements List filtered to form fields
expected_behavior: The control's accessible name is "Upload file", supplied by a <label for> bound to the input id
actual_behavior: Accessible name is "Choose File" (UA shadow-DOM button text); the visible caption is an unassociated <div>
trend: new
```

**Critical 2 — Validation error is neither announced nor associated with the field; the failure is silent.**

`BuggyFileInput.jsx:25-29` renders `{error && <div className="error-message">{error}</div>}` — no `id`, no `role="alert"`, no `aria-live`. `BuggyFileInput.jsx:20-24` has no `aria-describedby`. Measured: `sr-census.json` shows `"File too large"` present in the reading order (entry 3) while `declared_live_regions: []` — the page declares **no** live regions in the state where the error text exists. Nothing in the axe run contradicts this; axe reported no violation here because no axe rule covers "an error message that is never announced," which is precisely why this review exists.

- **User group**: screen reader (primary); cognitive (secondary).
- **WCAG**: 4.1.3 Status Messages (AA), 3.3.1 Error Identification (A), 1.3.1 Info and Relationships (A).
- **Confidence**: HIGH.
- **Why this matters**: The user selects a file. The app rejects it. The user hears nothing. They move on believing the upload worked — and every other channel confirms that belief: the control still displays their filename (`trace.json step_0001 text: "C:\fakepath\quarterly-report.pdf"`) and the field still reports `invalid: "false"`. This is a silent failure with an active false-success signal, the worst shape a validation defect takes, and the least likely to ever be reported as a bug.
- **Fix**: (1) Render the error container **unconditionally** with `id="file-upload-error"` and `role="alert"`, injecting text into it rather than mounting the node with text already inside — a live region that appears pre-populated is unreliably announced. (2) Add `aria-describedby="file-upload-help file-upload-error"` to the input so the error is re-read whenever focus returns to the field; `role="alert"` fires once, `aria-describedby` persists, and both are needed. (3) Verify in the rendered DOM that both id references resolve (anti-pattern #9).

```
### A11y Evidence Finding
finding_id: file-input-error-not-announced-or-associated
fingerprint: 6d2b84e1fa07c539
source: raw/file-input-no-labels-kat-census/sr-census.json (captured_at 2026-08-26T18:02:20Z); BuggyFileInput.jsx:20-29
wcag_or_apg: WCAG 2.2 4.1.3 (AA), 3.3.1 (A), 1.3.1 (A)
section_508_fpc_context: Not in scope — no declared Revised Section 508 engagement. Note the distinction if one is ever declared: 3.3.1 and 1.3.1 are WCAG 2.0 Level A and would map to a 508 failure, but 4.1.3 Status Messages is WCAG 2.1-and-later only and does NOT map to the Revised Section 508 WCAG 2.0 A/AA basis.
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, cognitive=HIGH, low-vision=MEDIUM
evidence: sr-census.json declared_live_regions = []; entries include "File too large" (index 3) as free-standing text; declared_broken_aria_refs = [] (no ARIA relationships exist at all); BuggyFileInput.jsx:25-29 conditional div with no role/aria-live/id; BuggyFileInput.jsx:20-24 input with no aria-describedby
reproduction_steps: Load http://127.0.0.1:8777/file-input-no-labels.html with a screen reader running; choose a file larger than 5,000,000 bytes; listen for any announcement; then Shift+Tab away and Tab back to the input and listen again
expected_behavior: The error is announced when it appears, and is re-read as the field's description whenever the field regains focus
actual_behavior: No announcement on appearance (no live region on the page) and no re-read on refocus (no aria-describedby)
trend: new
```

### Major Findings (significantly degrades experience)

**Major 1 — `aria-invalid` is never set; the field reports itself valid while visibly in error.**

`BuggyFileInput.jsx:20-24` — no `aria-invalid`; the state variable at `:5` drives only the conditional render at `:25`. `trace.json step_0001` and `step_0003` both record `states.invalid: "false"`.

- **User group**: screen reader. **WCAG**: 4.1.2 Name, Role, Value (A). **Confidence**: HIGH.
- **Why this matters**: Even after Critical 2 is fixed, a user who navigates away and returns is told the field is fine. The programmatic validity state must track the visible one or the field lies on every subsequent encounter.
- *Evidence caution*: the trace and the census are separate captures of different page states; I do not claim the trace measured `invalid: "false"` *while the error was displayed*. The claim rests on source — `aria-invalid` is never set on any code path — which makes `false` the value in the error state by construction.
- **Fix**: `aria-invalid={error ? 'true' : undefined}` on the input at `:20`. Ship in the same change as Critical 2.

**Major 2 — The constraints that determine success are invisible until the user violates them.**

The 5 MB ceiling exists only as the literal `5000000` at `BuggyFileInput.jsx:9`. The accepted types exist only as `accept=".pdf,.doc,.docx"` at `:23`, which filters the OS picker and is never exposed as text. There is no help text element and no `aria-describedby`.

- **User group**: all users; disproportionately cognitive and screen reader. **WCAG**: 3.3.2 Labels or Instructions (A). **Confidence**: HIGH.
- **Why this matters**: The interface withholds its own rules and then enforces them. A user on a metered or slow connection selects a 40 MB scan and only then learns it was never going to work.
- **Fix**: Add `<p id="file-upload-help">PDF, DOC, or DOCX. Maximum 5 MB.</p>` and reference it from the input's `aria-describedby` alongside the error id.

**Major 3 — The error message names the problem and withholds the remedy.**

`BuggyFileInput.jsx:10` sets `'File too large'`. The threshold is known to the code at `:9` and is not in the message; neither is the size of the file the user actually chose.

- **User group**: all users; acutely cognitive. **WCAG**: 3.3.3 Error Suggestion (AA). **Confidence**: HIGH (though the copy may be owned by a content author rather than this component — route accordingly).
- **Why this matters**: "Too large" starts a blind retry loop. The user has no way to know whether to try a 20 MB file or a 4 MB one. For a screen reader user this compounds with Critical 2 — they are looping without even hearing the failures.
- **Fix**: `Selected file is 12.4 MB. The maximum is 5 MB — try compressing the file or splitting it.` Derive both numbers from `file.size` and the constant. Extract `5000000` to a named constant used by both the check and the message so they cannot drift.

**Major 4 — A rejected file stays displayed as the chosen file; the interface contradicts itself.**

`BuggyFileInput.jsx:9-14`: on the reject branch, `setError` is called and `setSelectedFile` is not, and nothing resets the input element. The control continues to display and expose the rejected filename as its value (`trace.json step_0001 text: "C:\fakepath\quarterly-report.pdf"`), while `error` renders below it. Separately, `selectedFile` (`:4`, `:12`) is never read or rendered anywhere in the component — the application has no confirmation surface of its own.

- **User group**: all; acutely cognitive and screen reader. **WCAG**: 3.3.1 Error Identification (A); 4.1.2 (A) for the value/state divergence. **Confidence**: MEDIUM-HIGH (a parent could remount via `key` or clear via a ref — out of frame; see Open Questions).
- **Why this matters**: The control's value is the most authoritative "did it work?" signal an AT user has, and here it asserts success at the same moment the app has rejected the file. Two sources of truth, one of them wrong, and the wrong one is the one AT reads.
- **Fix**: On rejection, clear the control (`e.target.value = ''`) and `setSelectedFile(null)` so the value, the app state, and the message all agree. Then render `selectedFile` as an explicit application-level confirmation — which also creates the surface for the success announcement below.

### Minor Findings (friction but workaround exists)

- **`accept` is a filter, not validation.** `BuggyFileInput.jsx:23` restricts the picker; `handleFileChange` (`:7-15`) validates size only. A user who switches the OS dialog to "All Files" and picks a `.txt` gets no error and no feedback — a silent accept of a file the interface said it would not take. *Mitigated by:* the filtered picker is the default path and server-side rejection is likely. Becomes MAJOR if the server is the only validator and its rejection is not surfaced back into this control. WCAG 3.3.1.
- **No indication of whether the field is required.** No `required`, no visible marker, no text. WCAG 3.3.2.

### Enhancements (best practice not met, no access barrier)

- **No success announcement.** After an accepted file there is no `role="status"` message. Partially covered by the UA writing the filename into the control's value — which is why this is not a Major. Once Major 4's fix adds an application-level confirmation, announce it politely in the same persistent region. WCAG 4.1.3.
- **Page-level landmark and heading gaps.** axe reports `landmark-one-main`, `page-has-heading-one`, and `region` on this page (trace corroborates: `region: {landmark: null, heading: null}`). All three carry `best-practice` tags only and are **not** WCAG failures. These are artifacts of mounting the component standalone into `#root` with no page shell; they are properties of the host page, not the component. Re-evaluate in the real page context; do not "fix" them inside this component.
- **Stable ids.** Use `useId()` for the label, help, and error ids so two instances on one page cannot collide on `for` / `aria-describedby`.

---

## What's Missing

Consolidated from Phase 7 — the absences that matter most, in fix order:

1. A `<label for>` and an `id` — nothing else can be wired up until these exist.
2. A persistent, unconditionally rendered live-region container for the error (not a conditionally mounted `role="alert"`).
3. `aria-describedby` on the input referencing help text **and** error together.
4. `aria-invalid` tracking the error state.
5. A help-text element stating types and size limit *before* failure.
6. A remedy in the error copy, and a reset of the control when a file is rejected.
7. An application-level confirmation of the accepted file (`selectedFile` is currently dead state), and a polite announcement of it.
8. Type validation to match the type constraint the interface advertises.

---

## Multi-Perspective Notes

- **Screen reader user**: Announces as "Choose File, button" — no identity. Rejection is silent (`declared_live_regions: []`), the field reports `invalid: "false"`, and the control still reads back the rejected filename. The user's belief that the upload succeeded is actively reinforced by every channel available to them.
- **Keyboard-only user**: The clean one. First Tab reaches the control, Shift+Tab returns, no trap, no positive tabindex, focus indicator measured visible with area 1107 ≥ 1096 ref and contrast 4.86 (2.4.7 and 2.4.13 both measured pass). Unmeasured: Enter/Space picker activation. The indicator is the UA default — it will need re-measuring the moment a design system touches `outline`.
- **Low vision user (200% zoom, high contrast)**: The caption is not programmatically bound to a 253x21 control, so a magnified viewport can show one without the other and nothing recovers the association. `.error-message` contrast is unmeasured — axe's clean `incomplete: []` says nothing here, because the error element was not in the DOM when axe ran. Forced-colors behavior unknown.
- **Cognitive accessibility**: The rules are hidden until broken; the failure message names no threshold and no remedy; and the control keeps presenting the rejected file as chosen. A user is asked to solve a constraint they were never told, from a message that will not tell them, while the screen shows a contradiction.

---

## Verdict Justification

**REVISE.** Two CRITICAL findings — a control with no accessible identity, and a validation failure that is silent and actively signals false success — are Level A/AA failures that block screen reader users from completing the task correctly. That rules out ACCEPT and ACCEPT-WITH-RESERVATIONS.

It is not REJECT. The component makes the correct foundational choice (native `<input type="file">`, no re-implemented picker, no ARIA masking bad semantics), and its keyboard and focus behavior is measurably sound. Every finding is additive markup — a label, an id, a persistent live region, `aria-describedby`, `aria-invalid`, a help-text element, better copy, and a reset on reject. No architectural rework, no pattern replacement.

**To upgrade to ACCEPT-WITH-RESERVATIONS**: fix Critical 1 and Critical 2 together with Major 1 (they form one change — a field is not fixed until its name, its description, and its validity state all land), and re-run the driven KAT session with the error branch forced open to confirm `declared_live_regions` is non-empty and the announcement actually fires.
**To upgrade to ACCEPT**: additionally fix Majors 2, 3, and 4, and supply a capture with the stylesheet loaded so the low-vision and contrast questions can be closed rather than deferred.

**Recalibrations applied (Phase 8)**: Minor 1 downgraded from MAJOR — *mitigated by* the OS picker filter being the default path and server-side validation being the likely backstop. Landmark/heading/region held at ENHANCEMENT — *mitigated by* their `best-practice`-only tags and their origin as a standalone-mount harness artifact rather than a component property. Critical 1 was considered for downgrade to MAJOR on browse-mode adjacency and held at CRITICAL, because form-field-list navigation loses the control's identity entirely. Major 3 was considered for downgrade to MINOR under the workaround rule and held at MAJOR, because the workaround is blind retry and the population affected is everyone.

**Escalation**: Screen reader and Cognitive at HIGH; Keyboard-only, Low vision, and Environmental contrast at MEDIUM → recommend `/perspective-audit`, run against a capture that includes the stylesheet and the error branch open.

**Evidence discipline note**: 18 of the 21 attached artifacts are axe scans of unrelated sibling pages. No finding above draws on them. The volume of the evidence pack is not a measure of its coverage — and for this component the pack is thinner than it looks: no deterministic KAT findings file, no keystroke beyond Tab/Shift+Tab, no CSS, no zoom or forced-colors capture, and no real-AT verification.

---

## Open Questions (unscored)

1. **`.error-message` contrast and color-alone signalling (1.4.3, 1.4.1).** No stylesheet was supplied, and axe's `incomplete: []` for this page carries no information because the error element was absent at scan time. *Check*: force the error branch open, re-run axe, and inspect whether the error is distinguished by anything other than red text (icon, bold prefix, the word "Error"). **Needs user verification.**
2. **Target size, 2.5.8 (AA).** The trace measures the control at 253x21 CSS px — 21 < 24. axe did not flag `target-size` here, and I believe it is correct not to: the size of an unstyled native file input is user-agent-determined, which is an explicit 2.5.8 exception. *Check*: if any project CSS sizes or restyles the control, the exception no longer applies and it must be re-measured. Not filed as a finding.
3. **Picker-cancel path.** `:8` reads `e.target.files[0]`; if a change event ever fires with an empty file list, the `else` branch (`:11-13`) silently clears both the error and the selection with no announcement. Most browsers do not fire `change` on cancel, so this may be unreachable. *Check*: instrument the handler and cancel the dialog in Chrome, Firefox, and Safari. **Low confidence — not filed.**
4. **Does a parent reset the input?** Major 4 assumes nothing outside this component clears the control after a rejection. *Check*: confirm no ancestor remounts via `key` or clears via a ref. If one does, Major 4 drops to MINOR (the `aria-invalid` half of the problem remains).
5. **Is the field required, and is there a submit step?** The component has no `<form>`, no submit, and no upload call — `selectedFile` goes nowhere. The surrounding flow determines whether "required" needs indicating and whether upload progress needs its own status region (4.1.3).
6. **Type enforcement server-side.** If the server rejects a `.txt` that bypassed `accept`, is that rejection surfaced back into this control's error region, or does the user see a page-level failure? Determines whether Minor 1 stays MINOR.
7. **Enter/Space activation.** Unmeasured by the driven session. Expected to pass on a native input; confirm before the keyboard perspective is closed out.
