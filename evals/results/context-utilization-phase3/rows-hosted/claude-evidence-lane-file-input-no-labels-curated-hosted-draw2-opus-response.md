# Accessibility Design Review — `BuggyFileInput` (file upload control)

**Citation convention**: line numbers are relative to the component source as supplied in the review packet, counting `import React, { useState } from 'react';` as line 1. Cited as `BuggyFileInput.jsx:NN`.

---

## Phase 0 — Test Evidence Intake

**Review type**: fresh design pass, not a fix/remediation review. The a11y-test *Verification evidence contract* check (evidence-type-vs-claim mismatch) therefore does not apply — there is no prior fix whose proof-type I could mismatch. Noted and skipped deliberately, not overlooked.

**Evidence tier — read this before trusting any citation below.**

Everything I was given as "evidence" is an `a11y-evidence-reader` **digest**. Per the Phase 0 rule, a digest is detector output one tier *below* the artifact it cites — a paraphrase, not the hard evidence. The protocol requires re-fetching at the cited handle before filing a finding on a digest line. **I could not re-fetch**: the three underlying artifacts (`axe-batch-2026-08-25/010-...json`, `file-input-no-labels-kat-driven/trace.json`, `file-input-no-labels-kat-census/sr-census.json`) were not supplied to this review, only the digest of them.

Consequence, stated plainly:

- **Every measured-evidence citation in this review is labeled `digest-only`.** The digest is unusually good — it quotes verbatim JSON and records jq handles — but a verbatim quote inside a paraphrase is still a paraphrase. The handles are reproduced in each finding so a reviewer can re-fetch and upgrade the tier.
- **No verdict-bearing finding rests on digest-tier evidence.** Findings C-1 and C-2 (both CRITICAL) are provable from the component source alone, which *is* first-tier material — it was supplied in full in the review packet. The axe and trace lines corroborate; they do not carry the finding. If every digest line were struck, the verdict would not move.

**What the digest establishes (all `digest-only`):**

| Source | Tool + version provenance | What it gives |
|---|---|---|
| axe json, `.viewports["1280x800"].violations[0..3]` | axe-core **4.13.0**, self-declared via `axe_core_version` | 4 rules fired: `label` (critical, selector `input`), `landmark-one-main`, `page-has-heading-one`, `region` |
| `trace.json`, `steps[0..2]` | **not self-declared** — keyboard-a11y-tester attribution rests on directory naming (`-kat-driven`) and the question's labeling, per the digest's own Not-claimed | 3 keystrokes (`Tab`, `Tab`, `Shift+Tab`), all `focus_moved: true`; AX name/role/state for the input; focus-visible measurements |
| `sr-census.json` | **not self-declared** (`-kat-census` directory naming only) | 3 reading-order entries; `declared_live_regions: []`, `declared_broken_aria_refs: []`, `truncated: false` |

Shared evaluation context, stated in the artifacts rather than derived: url `http://127.0.0.1:8777/file-input-no-labels.html`; viewport 1280x800 for both axe and trace.

**Calibration rules applied (keyboard-a11y-tester, pin `0.5.0`):**

1. *Batch-crawl 4.1.3 findings are prompts, not failures* — **no occasion to apply**. The digest's question names "keyboard-a11y-tester batch-crawl findings" as a fourth tool, but no corresponding artifact was supplied and the digest makes no claim from it. Neither do I.
2. *Name-presence checks don't cover UA-intrinsic names — a "Choose File" file input can still be missing its label* — **directly load-bearing here.** See finding C-1. This rule is the difference between a correct review and a rubber-stamp on this fixture.
3. *Journey-level verdicts are judgment-layer claims, accepted only with supporting trace steps* — applied. The digest offers no journey verdict; it explicitly declines to judge whether obs. 7, 9, and 10 are defects. I make those judgments below and show the steps.
4. *`conformance_level` is a pass/fail gate, not the SC's WCAG level (upstream issue #27)* — **no occasion to apply**; no `conformance_level` field appears anywhere in this digest.

**WCAG token translation.** The axe artifact emits tag tokens, not SC numbers — the digest is explicit that it quotes them "verbatim, untranslated." The `label` rule carries `wcag2a` and `wcag412`. Translating `wcag412` → **4.1.2 Name, Role, Value** is *my* mapping, not the artifact's. Where I cite 1.3.1 and 3.3.2 alongside it, those are my analysis of the source code, not axe output.

**Section 508 wording.** Scope here is a component review; Revised Section 508 is not declared in scope, so nothing below is labeled a 508 failure. For context only: the SCs at issue (1.3.1, 3.3.1, 3.3.2, 4.1.2) are all WCAG 2.0 Level A and would sit inside the Revised 508 floor if a project declared it. Note also that axe's `section508` / `section508.22.n` tokens map to the *legacy* §1194.22(n) provision superseded by the Revised rule's WCAG 2.0 incorporation — I quote them as verbatim tool tokens, not as a conformance mapping.

---

## Phase 1 — Pre-commitment Predictions (written before reading the source)

Component type from the packet title: a form control with client-side validation. Predicted, per the protocol's "Form with validation" and native-input profiles:

| # | Prediction | Outcome |
|---|---|---|
| P1 | Visible label text exists as a non-`<label>` element; no `htmlFor`/`id` pairing | **CONFIRMED** — `<div>Upload file</div>` at :19 |
| P2 | Error rendered but not associated via `aria-describedby`; no `aria-invalid` on the input | **CONFIRMED** — :20-24 and :25-29 |
| P3 | Error not announced — no `role="alert"`, no `aria-live` | **CONFIRMED** — and corroborated: `declared_live_regions: []` |
| P4 | Constraints (`accept` list, size cap) never stated as user-facing help text | **CONFIRMED** — the 5 MB cap exists only in JS at :9 |
| P5 | Focus behavior after the OS file dialog closes is unhandled | **CONFIRMED in code** (nothing handles it), **UNMEASURED in evidence** — the trace never activated the control |

**Two things I did not predict:**

- **The UA-intrinsic-name trap fires in this fixture.** The trace records `ax_name_role_state.name = "Choose File"`, `role = "button"`. A naive name-presence check reads that as "control has a name — labeled." It is not a label; it is Chromium's shadow-DOM button text for `<input type="file">`. Calibration rule 2 exists for exactly this, and this fixture is the canonical instance of it.
- **`selectedFile` is written and never read.** Dead state (:12), and stale on the error path — see M-4.

---

## Phase 2 — Semantic HTML Audit

- **Native-first: PASS.** The control is a real `<input type="file">` (:20-24). No `div role="button"`, no ARIA substituting for available HTML semantics. The `accept` attribute is used correctly as a native filter. This is the right primitive and the review should say so plainly — the failures below are all *omissions around* a correctly chosen element, not a wrong element.
- **Label association: FAIL.** `<div>Upload file</div>` (:19) is a plain `div`. No `htmlFor`, no `id` on the input, no nesting, no `aria-labelledby`. The visible label text and the control have no programmatic relationship of any kind. → **C-1**
- **Error element: FAIL on association.** `<div className="error-message">` (:25-29) has no `id` and is referenced by nothing. → **C-2**
- **Heading hierarchy**: the component contributes no heading. axe's `page-has-heading-one` fired against selector `html` — that is the harness page, not this component (see E-1 on scope).
- **Landmarks**: none in the component; axe's `landmark-one-main` and `region` fired against `html` and `#root` respectively. Harness scope again.
- **Tables / lists**: none present. The layout-table and `role="presentation"` checks are inapplicable — noted so the omission reads as deliberate, not skipped.
- **Hidden ARIA papering over broken HTML**: none. There is no ARIA in this component at all. That is the problem, but it is an absence, not a misuse.

## Phase 3 — ARIA Pattern Compliance Audit

There is **no ARIA widget pattern here** — no combobox, no dialog, no disclosure, no composite widget. This is a native form control, so no WAI-ARIA APG pattern applies and none should be invented. The relevant contract is the form-field contract (label + description + validity state), not an APG widget pattern.

- Required ARIA states/properties for a validated field: `aria-describedby` (absent), `aria-invalid` (absent). Both missing.
- ARIA value validity: no ARIA values present, so nothing invalid.
- Roving tabindex, `aria-controls`, `aria-modal`, `aria-expanded`: all inapplicable. Not manufacturing findings here.

**Explicitly NOT a finding — role `"button"` on the file input.** The trace's `role: "button"` (obs. 5, both visits) is Chromium's standard AX exposure of `<input type="file">`, whose shadow root contains a button. It is UA behavior, not an author defect. The digest corroborates negatively: the fired-rule id list is `["label","landmark-one-main","page-has-heading-one","region"]` — no role-token rule (`aria-allowed-role`, `aria-valid-attr-value`, etc.) fired. **No role defect exists.** I am naming this because "role=button on an input" is a tempting false positive and filing it would be a manufactured violation.

## Phase 4 — Focus Management Review

Measured behavior is **clean on everything the session actually exercised**, and I want that on the record before the gaps:

- `Tab` reaches the input: `active_element_selector "#root > div > input"`, `focus_moved: true`, `dom_order_index 12` (obs. 6, digest-only).
- Focus indicator: `{visible: true, indicator: "outline", contrast: 4.86, contrast_pass: true, aaa_pass: true, area_pass: true}` (obs. 6, digest-only). **2.4.7 Focus Visible and 2.4.13 Focus Appearance pass on measurement** for this element. Caveat: the component ships no CSS, so this is the UA default ring. If the consuming project's stylesheet resets `outline`, this measurement does not transfer.
- `Shift+Tab` returns to the input with identical AX values (obs. 8, digest-only). No reverse-navigation defect.
- Every keystroke moved focus: `[.steps[].focus_moved] → [true,true,true]` (obs. 11, digest-only). **No keyboard trap. 2.1.2 satisfied** on the evidence available.

**Explicitly NOT a finding — `Tab` landing on `body` at step_0002.** `active_element_selector: "body"`, `role: "none"`, `name: null`, `dom_order_index: -1`, with `bounding_box`, `computed_focus_style`, `region`, and `focus_visible` all null (obs. 7). The digest declines to judge this; I will. The page has exactly one focusable element. Tabbing past the last focusable element hands focus to browser chrome, and `document.activeElement` falls back to `body` — the null measurement fields are precisely what you would expect when there is no focusable element to measure. **This is correct end-of-document behavior, not a focus-order defect.** Filing it would be a manufactured violation.

**The real focus gap is unmeasured, not measured-bad:**

- The trace's own stated goal is `"Choose a file to upload using only the keyboard and review any feedback the page gives"` (obs. 11). **The session never did either.** Three keystrokes, all navigation: `Tab`, `Tab`, `Shift+Tab`. No `Enter` or `Space` to open the file dialog, no file chosen, no feedback reviewed. The driven session did not complete the goal it declares.
- Therefore **keyboard operability of the actual upload action is unmeasured** (2.1.1), and so is focus restoration after the OS file-picker dialog closes. The component has no code touching either. This is an evidence-coverage gap, and I am reporting it as such rather than inventing a measured claim — see W-6.
- The two artifacts capture *different application states*: the trace never triggered an error, yet the census contains `"File too large"`. The census was taken with the error rendered; the trace was not. They cannot be cross-read as one timeline.
- Multi-instance ID collision: not yet a defect (single instance, no IDs at all), but it becomes one the moment the fix adds hard-coded `id` values and the component renders twice. Pre-empted in the fix and filed as **E-2**.

## Phase 5 — State Communication Audit

Every state this component tracks is communicated **visually only**. Nothing reaches assistive technology.

| State | Visual | Programmatic | Evidence |
|---|---|---|---|
| Invalid (file too large) | error div renders (:25-29) | **none** — no `aria-invalid` | trace: `states.invalid = "false"` at *both* visits (obs. 5) |
| Error text | rendered | **not associated, not announced** | no `id`/`aria-describedby`; `declared_live_regions: []`; `live_announcements: [[],[],[]]` |
| Selected file | UA renders filename beside the button | app renders nothing (`selectedFile` never read) | :12 sets it; no JSX consumes it |
| Constraints (types, 5 MB) | not stated anywhere | not stated anywhere | :9, :23 |

The `states.invalid = "false"` reading is the sharpest single line in the evidence: the AX tree was asked for the validity state and answered *false*. That is a measured negative, and it gives the fix a re-run assertion (see C-2's verification note).

## Phase 7 — Gap Analysis

Consolidated under **What's Missing** in the verdict block below.

---

**VERDICT: REVISE**

**Overall Assessment**: The component picks the right primitive — a native `<input type="file">` with a real `accept` filter, zero ARIA abuse, and a measured-clean focus indicator and tab path. Everything around that primitive is missing: no label association, no description association, no validity state, no announcement, and no statement of the constraints the JS silently enforces. The result is a control that a screen reader user encounters as a generic button called "Choose File", and a size-rejection that fails **silently** while the control itself continues to report the rejected file as selected. Two CRITICAL findings; this must not ship. The verdict is REVISE rather than REJECT because nothing needs rearchitecting — every fix is additive against a correctly chosen element.

**Pre-commitment Predictions**: All five predictions (P1–P5) confirmed — see the Phase 1 table. Two surprises: (a) the fixture is the canonical instance of the UA-intrinsic-name trap — the trace's `name: "Choose File"` would pass a naive name-presence check while the control is entirely unlabeled; (b) `selectedFile` is dead state, written at :12 and never read, and left stale on the error path. I was *not* surprised by any absence of findings — the areas I predicted would be clean (native semantics, focus indicator, no keyboard trap) measured clean.

---

## Findings

### Critical Findings (blocks access)

**C-1 — The file input has no label. Its accessible name is the browser's button text, which is why automated name-presence checks pass.**

`BuggyFileInput.jsx:19` renders the label text as `<div>Upload file</div>`. `BuggyFileInput.jsx:20-24` renders the input with no `id`, and nothing associates the two — no `htmlFor`, no nesting, no `aria-labelledby`, no `aria-label`.

The consequence is worse than a blank name. Chromium exposes `<input type="file">` as `role: "button"` with the shadow-DOM text as the name, so the AX tree reports `name: "Choose File"` (obs. 5, both visits, digest-only). A screen reader user encounters a button that announces "Choose File, button" — plausible-sounding, entirely context-free. Upload *what*? In which format? For what purpose? On a page with two upload fields, both announce identically. The visible answer, "Upload file", is a detached `div` that a virtual cursor may pass on a different line with no relationship to the control.

This is exactly the case keyboard-a11y-tester calibration rule 2 names: *name-presence checks don't cover UA-intrinsic names — a "Choose File" file input can still be missing its label.* Any tool or reviewer scoring "does the control have an accessible name?" scores this PASS. It is not.

- **Evidence (source, first-tier)**: `BuggyFileInput.jsx:19` (`<div>Upload file</div>`), `BuggyFileInput.jsx:20-24` (input, no `id`).
- **Evidence (measured, `digest-only`)**: axe-core 4.13.0 rule `label`, `impact: "critical"`, `node_count: 1`, `sample_selectors: ["input"]`, help "Form elements must have labels", tags `["cat.forms","wcag2a","wcag412","section508","section508.22.n","TTv5","TT5.c","EN-301-549","EN-9.4.1.2","ACT","RGAAv4","RGAA-11.1.1"]`. Handle: axe json, jq `.viewports["1280x800"].violations[0]`.
- **Corroborating, weaker (`digest-only`, tool-shape caveated)**: the reading-order census records 3 entries — `"document"` (body), `"Upload file"` (tag `null`, selector `null`), `"File too large"` (tag `null`, selector `null`); `truncated: false`. The control does not appear among them, and the label text resolves to no selector. I hold this at MEDIUM confidence only, because the same entries show `role` equal to the spoken phrase — a degraded tool output, not a WAI-ARIA role token. The strong reading of this census is in Open Questions, not here.
- **User group**: screen reader users (blocking); voice-control users (cannot say "click Upload file" — the accessible name is "Choose File"); cognitive (label/control proximity is visual only).
- **WCAG**: 1.3.1 Info and Relationships (A); 3.3.2 Labels or Instructions (A); 4.1.2 Name, Role, Value (A) — the latter is axe's own `wcag412` token, translated by me.
- **Confidence**: HIGH. Provable from source alone.
- **Fix**: give the input an `id` and convert the `div` to `<label htmlFor={...}>`. **Do not "fix" this with `aria-label` on the input** — that leaves the visible text still unassociated (3.3.2 wants the visible label *and* the programmatic association), lets the visible text and the name drift apart in future edits, and adds a 2.5.3 Label in Name exposure the native pairing avoids. Use `useId()` rather than a literal string id (see E-2). Full code in the Recommended Fix section.

```
### A11y Evidence Finding
finding_id: file-input-missing-label-association
fingerprint: not-computed — requires hashing the normalized tuple (finding_id | url | selector | wcag_or_apg) with the emitting harness's hasher; not derivable in a read-only review. Recipe recorded so the value is stable when emitted. Not fabricated.
source: axe-core 4.13.0, rule "label" (digest-only; handle: axe json .viewports["1280x800"].violations[0]) + component source BuggyFileInput.jsx:19-24 (first-tier)
wcag_or_apg: WCAG 2.2 — 1.3.1 Info and Relationships (A), 3.3.2 Labels or Instructions (A), 4.1.2 Name, Role, Value (A). No APG pattern applies (native control).
section_508_fpc_context: not declared in scope for this component review. Context only: all three SCs are WCAG 2.0 Level A and would fall inside the Revised Section 508 floor if the project declares it. axe's "section508.22.n" token maps to the legacy §1194.22(n) provision, superseded by the Revised rule — quoted as a verbatim tool token, not as a conformance mapping.
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, cognitive=HIGH, keyboard=MEDIUM, low-vision=MEDIUM, environmental-contrast=MEDIUM, vestibular=LOW, auditory=LOW
evidence: BuggyFileInput.jsx:19 `<div>Upload file</div>`; BuggyFileInput.jsx:20-24 `<input type="file" onChange={...} accept=".pdf,.doc,.docx" />` with no id. Measured (digest-only): {"id":"label","impact":"critical","node_count":1,"sample_selectors":["input"]}; trace ax_name_role_state {"name":"Choose File","role":"button"} at step_0001 and step_0003.
reproduction_steps: 1) load http://127.0.0.1:8777/file-input-no-labels.html; 2) Tab to the file control; 3) with a screen reader running, listen to the focus announcement; 4) observe the name is the UA button text "Choose File", with no relationship to the visible "Upload file" text; 5) re-run axe-core 4.13.0 and observe rule "label" firing once against selector "input".
expected_behavior: focus announces the author-supplied label ("Upload file"), and the visible label text is programmatically associated with the control via label/for.
actual_behavior: focus announces the UA-intrinsic name "Choose File" with role "button"; the visible text is an unassociated div; axe rule "label" fires at critical impact.
trend: new
```

---

**C-2 — The size-rejection error is not associated, not announced, and not reflected in the validity state — and the control keeps reporting the rejected file. This is a silent validation failure.**

`BuggyFileInput.jsx:9-10` rejects any file over 5,000,000 bytes by setting an error string. `BuggyFileInput.jsx:25-29` renders it into `<div className="error-message">` — with no `id`, referenced by nothing, wrapped in no live region, with no `role="alert"`. The input at `:20-24` never receives `aria-invalid`.

Four mechanisms fail together, and the compounding is what makes this CRITICAL rather than MAJOR:

1. **No association.** No `aria-describedby`, so the error is not read when the field is focused (1.3.1, 3.3.1).
2. **No announcement.** No live region, so nothing is spoken at the moment the error appears (4.1.3). Corroborated by measurement: `declared_live_regions: []` in the census, and `live_announcements` is `[]` at all three trace steps.
3. **No validity state.** The AX tree reports `states.invalid = "false"` at both recorded visits (obs. 5, digest-only). Not "absent" — measured *false*. A screen reader asking "is this field invalid?" is answered no while an error is on screen (4.1.2).
4. **The control still reports the rejected file.** The browser populates `input.files` before `change` fires. The handler never clears `e.target.value`, so after a 6 MB PDF is rejected the control continues to display and expose `big-report.pdf` as its value. Meanwhile `selectedFile` was never updated (the `else` branch at :11-13 did not run), so the app holds a *different* file — or none.

Realistic worst case, and it is not exotic: a screen reader user tabs to the control, activates it, picks a 6 MB PDF, the dialog closes, focus returns to the input. **Nothing is spoken.** They re-read the control to confirm — and it says the file is there. They tab on and submit. The app never had the file. There is no moment in that sequence at which assistive technology is told anything is wrong.

Note precisely *why* `aria-describedby` alone would not rescue this: the error appears while the user is **already focused on the control**, and `aria-describedby` is announced on focus change. Focus does not change, so a describedby-only fix stays silent at exactly the moment it matters. Both mechanisms are required — association for later re-reads, a live region for the moment of failure. This is the design point, not a checklist item.

- **Evidence (source, first-tier)**: `BuggyFileInput.jsx:9-10` (rejection, no state reset, no `e.target.value` clear); `:20-24` (no `aria-describedby`, no `aria-invalid`); `:25-29` (error div, no `id`, no live region).
- **Evidence (measured, `digest-only`)**: trace `states: {"invalid":"false","focusable":true,"focused":true}` at `step_0001` and `step_0003` (handle: `trace.json`, `.steps[0].ax_name_role_state` / `.steps[2].ax_name_role_state`). Absence claims: `.steps[].sr_announcement.live_announcements → [[],[],[]]`; `.declared_live_regions → []`; `.declared_broken_aria_refs → []`.
- **User group**: screen reader users (blocking — silent data loss); cognitive (no feedback that an action failed); low vision using magnification (error text may render outside the viewport at 200–400% zoom with no announcement to pull attention to it).
- **WCAG**: 3.3.1 Error Identification (A); 1.3.1 Info and Relationships (A); 4.1.2 Name, Role, Value (A); 4.1.3 Status Messages (AA).
- **Confidence**: HIGH. Mechanisms 1–3 are provable from source; mechanism 4 follows from standard `<input type="file">` behavior. The measured `invalid: "false"` independently confirms 3.
- **Fix**: see Recommended Fix. Use an **always-mounted** live-region container that also carries the error `id` — a single element serving both association and announcement, avoiding double-speech. Mounting a `role="alert"` element *with content already inside* is the pattern that reads silent in real AT and in virtual-screen-reader; the persistent-container shape is the one that works. Also clear `e.target.value` and `selectedFile` on rejection so the control stops reporting a file the app refused.
- **Verification hook (concrete, reuses existing instrumentation)**: per anti-pattern 9, any fix adding `aria-*` needs DOM verification, not just unit tests. This finding hands you a measured baseline — re-run the same driven session after the fix and assert `ax_name_role_state.states.invalid` flips `"false"` → `"true"` while the error is present, that `sr_announcement.live_announcements` is non-empty on the step that triggers rejection, and that the `aria-describedby` id token actually resolves to a node in the rendered DOM.

```
### A11y Evidence Finding
finding_id: file-input-error-not-associated-or-announced
fingerprint: not-computed — same recipe and rationale as C-1. Not fabricated.
source: component source BuggyFileInput.jsx:9-10, 20-24, 25-29 (first-tier) + keyboard-a11y-tester driven trace, steps 0001/0003 (digest-only; attribution rests on directory naming "-kat-driven", no tool/version field in the artifact) + sr-census.json declared_live_regions (digest-only)
wcag_or_apg: WCAG 2.2 — 3.3.1 Error Identification (A), 1.3.1 Info and Relationships (A), 4.1.2 Name, Role, Value (A), 4.1.3 Status Messages (AA). No APG pattern applies (native control).
section_508_fpc_context: not declared in scope. Context only: 3.3.1 / 1.3.1 / 4.1.2 are WCAG 2.0 Level A and inside the Revised 508 floor if declared; 4.1.3 is WCAG 2.1-only and must NOT be labeled a 508 failure.
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, cognitive=HIGH, low-vision=MEDIUM, keyboard=MEDIUM, environmental-contrast=MEDIUM, vestibular=LOW, auditory=LOW
evidence: BuggyFileInput.jsx:25-29 error div has no id and no live region; :20-24 input has no aria-describedby and no aria-invalid; :9-10 rejects without clearing e.target.value or selectedFile. Measured (digest-only): states {"invalid":"false"} at step_0001 and step_0003; live_announcements [[],[],[]]; declared_live_regions [].
reproduction_steps: 1) load the page with a screen reader running; 2) Tab to the control and activate it; 3) choose a file larger than 5,000,000 bytes; 4) observe the visual error appears; 5) observe nothing is announced; 6) re-read the focused control and observe it still reports the rejected filename and an invalid state of false.
expected_behavior: on rejection the field is marked aria-invalid="true", the error is referenced by aria-describedby, the error text is announced via a live region, and the control no longer reports the rejected file.
actual_behavior: error is visual-only; AX validity state reads "false"; no live announcement anywhere in the session; the control continues to expose the rejected file as its value.
trend: new
```

---

### Major Findings (significantly degrades experience)

**M-1 — The constraints the component enforces are never stated to the user.** The `accept` list at `:23` filters the picker dialog but is not user-facing text, and the 5 MB cap at `:9` exists *only* inside the handler. Nothing on screen or in the accessibility tree tells anyone what may be uploaded or how large it may be. Users discover the limit by failing. For a cognitive-access user, and for anyone on a metered or slow connection uploading a large document, that is a costly way to learn a rule the page already knows. `accept` is additionally a soft filter — most OS dialogs offer "All Files", and the handler validates size but **never type**, so a `.txt` passes silently with no error at all. The feedback model is therefore inconsistent: sometimes an error, sometimes nothing.
- **Evidence**: `BuggyFileInput.jsx:9` (`file.size > 5000000`, no user-facing counterpart), `:23` (`accept=".pdf,.doc,.docx"`), and the absence of any help-text node in the JSX.
- **User group**: cognitive (primary); all users.
- **WCAG**: 3.3.2 Labels or Instructions (A); 1.3.1 Info and Relationships (A) for the association once the text exists.
- **Confidence**: HIGH. **GAP**, not preference.
- **Fix**: render help text ("PDF, DOC, or DOCX. Maximum size 5 MB.") and reference it from `aria-describedby` so it is announced on focus, before the user commits to a file. Derive the limit from a named constant so the text and the check cannot drift. Add a type check alongside the size check, or drop the pretense that type is enforced.

**M-2 — "File too large" does not say what the limit is or what to do about it.** `BuggyFileInput.jsx:10` sets the entire error string to four words. The threshold is known to the code at the moment it fires; the user is told none of it. No file name, no actual size, no limit, no remediation.
- **Evidence**: `BuggyFileInput.jsx:10` (`setError('File too large')`); corroborating (`digest-only`): the census records the spoken phrase verbatim as `"File too large"` — that is the whole announcement content in the reading order.
- **User group**: cognitive (primary); screen reader users, who get the least context to begin with.
- **WCAG**: 3.3.3 Error Suggestion (AA).
- **Confidence**: HIGH. **GAP** — this is a named SC with a known-correct answer available in the code, not a copywriting preference.
- **Fix**: `` `"${file.name}" is ${(file.size / 1048576).toFixed(1)} MB. The maximum is 5 MB. Choose a smaller PDF, DOC, or DOCX file, or compress this one and try again.` ``

**M-3 — There is no error-state contract at the page level, only a div that appears.** Beyond C-2's association and announcement gaps: nothing marks whether the upload is required, nothing renders the error in a form-level summary, and there is no `<form>`, submit path, or submit-time revalidation in the component. A user who triggers the error, tabs away, and submits gets no second chance to hear it. I am reporting the *shape* of this gap rather than a verdict on submit behavior, because the surrounding form was not supplied — see Open Questions.
- **Evidence**: `BuggyFileInput.jsx:17-31` — the entire render output is a `div`, an unassociated `div`, an `input`, and a conditional `div`.
- **User group**: screen reader, cognitive.
- **WCAG**: 3.3.1 Error Identification (A).
- **Confidence**: MEDIUM on the page-level portion (depends on the unsupplied parent form); HIGH that the component itself contributes no error contract.

**M-4 — `selectedFile` is dead state and goes stale on the error path, so the app's model of "what is selected" diverges from what the control reports.** `:12` sets it; **no JSX ever reads it**. And the rejection branch at `:9-10` sets the error *without* clearing `selectedFile`, so: pick a valid `small.pdf` → `selectedFile = small.pdf`; then pick `huge.pdf` → error renders, `selectedFile` is *still* `small.pdf`, and the input's own value is now `huge.pdf`. Three sources of truth, three different answers, none of them shown to the user. Separately, cancelling the dialog takes the `else` branch (`file` is `undefined`) and silently clears both states with no feedback.
- **Evidence**: `BuggyFileInput.jsx:4` (state declared), `:9-13` (branch logic, no reset on the error path), `:17-31` (no consumer of `selectedFile` anywhere in the render).
- **User group**: all users; the divergence is invisible to everyone, which is why it will ship.
- **WCAG**: 4.1.2 Name, Role, Value (A) — the programmatic state does not reflect the actual state. Also a plain correctness bug.
- **Confidence**: HIGH. Directly readable from the source.
- **Fix**: clear `selectedFile` and `e.target.value` on rejection; handle the no-file (cancel) case explicitly and early; render the selected filename so the state has a consumer and a user-visible meaning.

---

### Minor Findings (friction but workaround exists)

- **N-1 — No app-level confirmation that a file was selected.** `selectedFile` is never rendered, so the only confirmation is whatever the UA provides. *Mitigated by: the native `<input type="file">` exposes the chosen filename as the control's own value, so a screen reader user can confirm selection by re-reading the control — the confirmation exists, it is just not authored.* Held at MINOR for that reason, and note it is only a *reliable* mitigation once C-2's `e.target.value` reset lands; until then, re-reading the control can confirm a file the app rejected.
- **N-2 — The visible label text is a bare `div` with no element semantics of any kind.** Even setting aside association, `div` communicates nothing about what the text is for. Folded into C-1's fix; listed separately because a team might associate via `aria-labelledby` and leave the `div`, which resolves C-1 but leaves this.

### Enhancements (best practice not met, no access barrier)

- **E-1 — The three landmark/heading axe results describe the test harness page, not this component. Do not fix them here.** `landmark-one-main` (selector `html`), `page-has-heading-one` (selector `html`), and `region` (selector `#root`) all fired (`digest-only`). Two things matter: (a) the digest is explicit that **none of these carry a `wcag2*` tag** — `landmark-one-main` and `page-has-heading-one` are tagged `["cat.semantics","best-practice"]`, and `region` is `["cat.keyboard","best-practice","RGAAv4","RGAA-9.2.1"]`. They are axe best-practice rules, **not WCAG failures**, and labeling them as such would be a manufactured violation. (b) This component is a fragment mounted into `#root`; `<main>` and `<h1>` belong to the page that hosts it. Dropped into a real page with a `main` landmark, all three resolve with zero changes here. ENHANCEMENT, scoped to the harness.
- **E-2 — Use `useId()` for the label/help/error ids the fix introduces.** The component takes no props and could render twice on one page (e.g. "Upload résumé" and "Upload cover letter"). Hard-coded `id="file-upload"` would collide, and duplicate ids silently break `htmlFor` and `aria-describedby` resolution — the association *appears* correct in source and is wrong in the DOM. Pre-empted in the fix below.
- **E-3 — Announce successful selection.** A short polite status ("`report.pdf` selected") closes the confirmation loop. Flagged as an enhancement rather than a requirement because the native control already exposes its value, and because it carries a real double-speech risk with the UA's own value announcement. Test it with a real screen reader before shipping it; do not add it on faith.

---

### What's Missing (gaps, unhandled edge cases, unstated assumptions)

- **W-1** — No `<label>` and no `id` on the input; the visible label has no programmatic relationship to the control. (C-1)
- **W-2** — No `aria-describedby`, so neither help text nor error text is announced on focus. (C-2, M-1)
- **W-3** — No `aria-invalid`; measured as `"false"` while an error is displayed. (C-2)
- **W-4** — No live region anywhere; `declared_live_regions: []` and `live_announcements: [[],[],[]]` confirm the page ships none. (C-2)
- **W-5** — No user-facing statement of accepted types or the 5 MB cap, and no type validation to match the `accept` filter's implied promise. (M-1)
- **W-6** — **Evidence gap: keyboard operability of the upload action itself was never measured.** The driven session sent `Tab`, `Tab`, `Shift+Tab` and stopped, though its own declared goal was `"Choose a file to upload using only the keyboard and review any feedback the page gives"`. No activation keystroke, no file chosen, no feedback reviewed. So 2.1.1 for the *action* and focus restoration after the OS dialog closes are both **unmeasured**, and the component contains no code addressing either. I am not filing this as a defect — I am filing it as the reason a clean trace here does not license a keyboard clean bill.
- **W-7** — No `e.target.value` reset on rejection; the control keeps reporting a file the app refused. (C-2 mech. 4)
- **W-8** — No handling of the dialog-cancel path; state clears silently with no feedback. (M-4)
- **W-9** — No CSS supplied with the component, so `.error-message` and `.file-upload` are unverifiable. Three checks are consequently **unresolvable, not passed**: 1.4.1 Use of Color (a class literally named `error-message` is the standard place a red-only error signal lives — is there a non-color indicator?), 1.4.3 Contrast (error text ratio unknown), and whether project CSS resets the `outline` the trace measured at 4.86.
- **W-10** — No surrounding `<form>`, submit handler, required-field indication, or error summary. The submit-time error path cannot be reviewed from this packet.
- **W-11** — No page-level landmark or `h1` in the harness. Best-practice tier, harness scope. (E-1)
- **W-12** — The two artifacts capture different application states (trace: no error; census: error present) and cannot be read as one timeline.

---

### Multi-Perspective Notes

**Screen reader user (NVDA, JAWS, VoiceOver)** — the blocked perspective. Encounters "Choose File, button" with no indication of purpose, format, or size limit. Picks a too-large file and hears **nothing**; re-reads the control and is told the rejected file is selected, with validity state `false`. In a linear read the reachable content is three orphan strings — `"document"`, `"Upload file"`, `"File too large"` — with no field between them and no relationship among them. Every state this component tracks is invisible to them. This perspective cannot complete the task reliably.

**Keyboard-only user** — measured clean on everything exercised, and I will not manufacture a finding here. `Tab` reaches the control (`focus_moved: true`), `Shift+Tab` returns to it, all three keystrokes moved focus, no trap, and the focus indicator measures `visible: true`, `outline`, contrast `4.86`, with `contrast_pass`, `aaa_pass`, and `area_pass` all true — 2.4.7 and 2.4.13 satisfied on measurement. Tab landing on `body` at step_0002 is correct end-of-document behavior on a one-control page, not a defect. The honest qualifier: the session never *activated* the control, so operability of the upload action and focus restoration after the OS dialog are unmeasured, and the focus measurement is of the UA default ring on a component that ships no CSS.

**Low vision user (200% zoom, high contrast, magnifier)** — the focus ring measures well above the 3:1 threshold. Unresolved by absence of CSS: whether the error is signalled by red text alone (1.4.1), whether error text meets 4.5:1 (1.4.3), and whether project styles preserve the outline. There is a magnification-specific compounding of C-2 worth naming: at 300–400% zoom the error text may render entirely outside the viewport, and because nothing is announced, there is no signal at all to pull attention toward it. Announcement is not only a screen reader concern.

**Cognitive accessibility** — the second HIGH. The rules are secret until broken (M-1), the error names neither the limit nor a remedy (M-2), the feedback model is inconsistent (wrong *size* errors, wrong *type* is silent), and the app's own model of what is selected can diverge from the control without anyone being told (M-4). The user's workflow is guess, fail, guess again — with no information gained per failure.

**Vestibular & motion** — no animation, transition, parallax, or auto-playing content in the component. LOW, genuinely inapplicable.

**Auditory access** — no `<video>`, `<audio>`, or auditory alert. LOW, genuinely inapplicable.

**Environmental contrast** — same unresolved CSS questions as low vision. The `.error-message` class name is the specific signal keeping this above LOW: color-only error signalling is the default failure mode for exactly that class name. Needs verification, not assumption.

#### Perspective Alarm Levels

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | **HIGH** | Unlabeled control announcing as a generic UA button; validation failure with no association, no announcement, and `invalid: "false"`; control reports a rejected file |
| Keyboard-only | MEDIUM | Native single control, measured clean over 3 steps — but the session never activated it, so upload operability and post-dialog focus restoration are unmeasured |
| Low vision | MEDIUM | Focus ring measured pass (4.86); no CSS supplied, so error contrast, color-only signalling, and outline survival are unresolved; un-announced error may sit outside the magnified viewport |
| Cognitive | **HIGH** | Undisclosed constraints; error with no threshold and no remedy; inconsistent feedback (size errors, type silent); stale invisible state |
| Vestibular & motion | LOW | No animation, transition, or auto-playing content |
| Auditory access | LOW | No media elements, no auditory-only signalling |
| Environmental contrast | MEDIUM | `.error-message` class with no supplied CSS — 1.4.1 color-only signalling unverifiable |

**Escalation**: Screen reader and Cognitive at HIGH; Keyboard-only, Low vision, and Environmental contrast at MEDIUM. Per the protocol, all five should be flagged for deep review via `/perspective-audit`. The two HIGH perspectives are where the ship-blocking findings live.

---

### Recommended Fix

```jsx
import React, { useId, useState } from 'react';

const MAX_BYTES = 5 * 1024 * 1024;          // single source of truth for the cap
const MAX_LABEL = '5 MB';                    // ...and for every string that states it
const ACCEPTED = '.pdf,.doc,.docx';

const FileInput = () => {
  const inputId = useId();                   // E-2: safe when rendered more than once
  const helpId  = `${inputId}-help`;
  const errorId = `${inputId}-error`;

  const [selectedFile, setSelectedFile] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];

    if (!file) {                             // M-4: dialog cancelled — handle explicitly
      setSelectedFile(null);
      setError(null);
      return;
    }

    if (file.size > MAX_BYTES) {             // M-2: name the limit and the remedy
      setSelectedFile(null);                 // M-4: no stale selection behind an error
      e.target.value = '';                   // C-2 mech.4: stop reporting a rejected file
      setError(
        `"${file.name}" is ${(file.size / 1048576).toFixed(1)} MB. ` +
        `The maximum is ${MAX_LABEL}. Choose a smaller PDF, DOC, or DOCX file, ` +
        `or compress this one and try again.`
      );
      return;
    }

    setSelectedFile(file);
    setError(null);
  };

  return (
    <div className="file-upload">
      {/* C-1: real label/for pairing — not aria-label */}
      <label htmlFor={inputId}>Upload file</label>

      {/* M-1: state the constraints before the user commits to a file */}
      <p id={helpId} className="file-upload__help">
        PDF, DOC, or DOCX. Maximum size {MAX_LABEL}.
      </p>

      <input
        id={inputId}
        type="file"
        onChange={handleFileChange}
        accept={ACCEPTED}
        aria-describedby={error ? `${helpId} ${errorId}` : helpId}
        aria-invalid={error ? 'true' : undefined}
      />

      {/*
        C-2: ONE always-mounted element serving both roles —
          - referenced by aria-describedby  → read on focus / re-read
          - role="alert" with text injected → announced at the moment of failure
        Always mounted and empty when there is no error. Mounting role="alert"
        *with content already inside* is the shape that reads silent in real AT
        and in virtual-screen-reader; injecting into a persistent container is not.
        Give it `min-height: 0` / no reserved box in CSS so the empty state is invisible.
        Keep it a single element so the text is never announced twice.
      */}
      <div id={errorId} className="error-message" role="alert">
        {error ? <><span aria-hidden="true">⚠ </span>Error: {error}</> : null}
      </div>

      {/* E-3: optional. Verify with a real screen reader before shipping —
          the UA also announces the control's value, so this can double-speak. */}
      <div className="visually-hidden" role="status" aria-live="polite">
        {selectedFile ? `${selectedFile.name} selected.` : ''}
      </div>
    </div>
  );
};

export default FileInput;
```

Notes on the fix, in decreasing order of how easy they are to get wrong:

1. **`role="alert"` is assertive and interrupting.** For a user-initiated single-field validation error that is defensible, and it is the reliable choice. If the team prefers non-interrupting, `role="status"` / `aria-live="polite"` on the same persistent container is acceptable — the `aria-describedby` association is what makes either safe, because it guarantees the error is available on re-read regardless of whether the announcement was caught.
2. **CSS still owes three answers** (W-9): a non-color error indicator (the `⚠` glyph above is a start, but it is `aria-hidden` and decorative — the word "Error:" is the real non-color signal), error text at ≥4.5:1, and an `outline` that is not reset away.
3. **Verify in the DOM, not in a unit test** (anti-pattern 9): confirm `aria-describedby`'s id tokens resolve to real nodes, that `aria-invalid` lands on the `<input>` and not a wrapper, and re-run the driven session to assert `states.invalid` flips `"false"` → `"true"`.
4. Type validation is still absent — `accept` remains a soft filter. Add a type check beside the size check, or accept that a `.txt` will pass silently.

---

**Verdict Justification**

**REVISE**, and REVISE here is not a soft verdict — **this must not ship.** Two CRITICAL findings mean a screen reader user cannot identify the control and cannot learn that their upload was rejected. The verdict is REVISE rather than REJECT for one reason: the component's *structure* is right. It uses a native `<input type="file">` with a real `accept` filter, it does not substitute ARIA for available HTML semantics, its focus behavior measures clean, and there is no keyboard trap. Every finding is a missing association, a missing announcement, or a missing sentence. The upgrade path is ~20 additive lines against a correctly chosen element — no rearchitecting, no pattern change. That is REVISE by definition. REJECT would imply the approach is wrong; it is not.

**For an upgrade to ACCEPT-WITH-RESERVATIONS**: land C-1 and C-2 — real `label`/`for` pairing, `aria-describedby`, `aria-invalid`, the persistent live-region container, and the `e.target.value` reset — and verify them in the rendered DOM rather than in unit tests. **For ACCEPT**: additionally land M-1 and M-2 (state the constraints up front, and name the limit and remedy in the error), resolve W-9 by supplying the CSS, and close W-6 by running a driven session that actually activates the control and measures where focus lands after the OS dialog closes.

**Phase 8 Realist Check — recalibrations performed:**

- **C-1 held at CRITICAL.** Worst case is not "the label is suboptimal" — it is a control whose only name is UA chrome text, identical across every file input on any page, with the human-meaningful label present but unreachable programmatically. Detection: **never** by automated name-presence tooling, which scores this PASS (calibration rule 2). It surfaces only in user testing or a bug report. No downgrade; no workaround exists for a user who cannot see the adjacent div.
- **C-2 held at CRITICAL.** Explicitly tested against the downgrade rules and it survives all four questions. Realistic worst case is silent data loss — the user believes a file is attached and it is not. Affects 100% of screen reader users, not <5%. Detection is `never` in the protocol's own terms: nothing throws, nothing logs, no test fails. The severity scale names "form validation fails silently" as CRITICAL explicitly. **And the downgrade rules forbid it**: this is complete access loss to the error state for a user category. There is a partial mitigation — the error text *is* in the DOM and reachable by browse-mode exploration (the census records it) — but that mitigation is what makes it a *silent* failure rather than an inaccessible one, and it requires the user to already suspect something went wrong. It does not lower the severity.
- **N-1 downgraded MAJOR → MINOR.** *Mitigated by: the native `<input type="file">` exposes the chosen filename as the control's own value, so confirmation of selection is available on re-read even without an app-level announcement.* Recorded with the caveat that this mitigation is only trustworthy after C-2's `e.target.value` reset lands.
- **E-1 downgraded from a candidate MAJOR to ENHANCEMENT, twice over.** First on tags: the digest shows `landmark-one-main`, `page-has-heading-one`, and `region` carry **no `wcag2*` tag** — they are axe best-practice rules, and filing them as WCAG failures would be a manufactured violation. Second on scope: they target `html` and `#root`, i.e. the harness page hosting this fragment, not the component. This is the page-shell over-flagging trap and I am declining it deliberately.
- **E-3 held at ENHANCEMENT rather than promoted.** A success announcement is good practice but carries a genuine double-speech risk against the UA's own value announcement. Promoting it would be adding an unverified requirement.
- **Three candidate findings declined outright as manufactured violations**: (a) `role: "button"` on the file input — UA exposure of the native control, corroborated by the absence of any role-token rule in the fired list; (b) `Tab` landing on `body` — correct end-of-document behavior on a one-control page, with null measurement fields exactly where you would expect them; (c) the census `role` field equalling the spoken phrase for entries 2 and 3 — a degraded tool output shape, not evidence of a role defect in the page.

**Phase 9 Self-Audit** — every CRITICAL/MAJOR rated:

| Finding | Confidence | Developer could refute? | GAP or PREFERENCE | Disposition |
|---|---|---|---|---|
| C-1 label association | HIGH | NO — provable from source; corroborated by axe `label` at critical impact | GAP | Keep CRITICAL |
| C-2 error association/announcement/state | HIGH | NO — mechanisms 1–3 from source, 3 independently measured (`invalid: "false"`) | GAP | Keep CRITICAL |
| M-1 constraints never stated | HIGH | NO — the JSX contains no help-text node | GAP | Keep MAJOR |
| M-2 error lacks limit and remedy | HIGH | NO — the string is four words at `:10` and the threshold is in scope at that line | GAP | Keep MAJOR |
| M-3 no page-level error contract | MEDIUM | **PARTLY** — the parent form was not supplied and may carry a summary | GAP | Keep MAJOR, scoped to the component; page-level portion moved to Open Questions |
| M-4 dead/stale `selectedFile` | HIGH | NO — the branch logic and the absence of any consumer are both readable at `:9-13` and `:17-31` | GAP | Keep MAJOR |

No finding was demoted for LOW confidence; the low-confidence material never became a finding in the first place and sits in Open Questions below.

**Phase 10 Synthesis** — all five predictions confirmed, which is itself a signal: this component fails in the entirely ordinary way that unlabeled validated inputs fail, and there was nothing exotic to discover. The two things I did not predict are the two things worth carrying forward. First, the UA-intrinsic-name trap is not theoretical here — it is the fixture's central feature, and a reviewer or tool checking "does the control have an accessible name?" scores this control PASS while it is completely unlabeled. Second, the driven trace declares a goal it does not execute: it says "choose a file and review any feedback" and sends three navigation keystrokes. A clean trace that never exercised the failing path is not evidence of a clean component, and treating it as such would have been the easiest way to get this review wrong.

---

**Open Questions (unscored)**

1. **Does the `sr_announcement` difference between step_0001 and step_0003 mean anything?** Step 1 reports `new_phrases: ["document"]`, `focus_announcement: "document"`; step 3, same element with identical states, reports `new_phrases: []`, `focus_announcement: null`. The most likely explanation is that `new_phrases` is a **delta** — nothing is new on the second visit, so the list is empty — making this a tool artifact rather than a defect. The digest declines to judge it and I decline to file it. What *is* mildly interesting: at neither step does the control's own name/role ("Choose File, button") appear as a focus announcement. That could equally be delta behavior. **Not admissible as evidence in either direction. Needs a real screen reader.**
2. **Is the input's absence from the reading-order census real?** Three entries, `truncated: false`, and none of them the control. That reads as significant — but entries 2 and 3 have `tag: null`, `selector: null`, and a `role` field containing their own spoken phrase, which is degraded output. I do not know whether the census under-captures form controls by design. **Corroborating only, at MEDIUM confidence; the strong reading stays here.**
3. **Digest-tier upgrade.** Every measured citation in this review is `digest-only`; the underlying artifacts were not available to re-fetch. All jq handles are recorded inline. Re-fetching would upgrade the evidence tier — it would not change the verdict, since both CRITICALs rest on the first-tier component source.
4. **Tool provenance for two of three artifacts.** Neither `trace.json` nor `sr-census.json` self-declares a tool or version; keyboard-a11y-tester attribution rests on directory naming (`-kat-driven`, `-kat-census`) and the question's own labeling. Only axe-core self-declares (`axe_core_version: 4.13.0`). This matters for the calibration rules, which are pinned to keyboard-a11y-tester `0.5.0` behavior — if these artifacts came from a different tool or pin, the rules I applied may not be the right rules.
5. **The CSS.** `.file-upload` and `.error-message` were not supplied. 1.4.1 (color-only error signalling), 1.4.3 (error text contrast), and outline survival are all **unresolved, not passed**. The class name `error-message` is precisely where a red-only signal lives.
6. **The parent form.** Is the upload required? Is there a `<form>`, a submit handler, submit-time revalidation, or an error summary? M-3's page-level portion depends entirely on this and cannot be settled from the packet.
7. **Post-dialog focus.** Where does focus land after the OS file-picker closes — in Chrome, Firefox, Safari, and on iOS/Android? The component addresses it nowhere and the trace never triggered it (W-6). Worth one driven session that actually presses `Enter`.
8. **Does the error announcement double-speak with the UA's value announcement** once E-3's status region is added? Test before shipping; do not add it on faith.
