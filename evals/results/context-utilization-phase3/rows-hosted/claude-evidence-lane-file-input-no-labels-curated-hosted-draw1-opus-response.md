**VERDICT: REVISE**

**Overall Assessment**: The component's foundation is right — a native `<input type="file">`, no ARIA misuse to unwind, and a measured-sufficient focus indicator. Everything above that foundation is missing: the control has no programmatic label (its accessible name is the user-agent's "Choose File", not the author's visible "Upload file"), the validation error is rendered as an inert `<div>` with no association, no invalid state, and no announcement, and the only enforced constraint (a 5,000,000-byte size cap) is never disclosed. A screen reader user can operate this control but cannot learn what it is for, and can fail validation without ever being told. The fixes are additive and small; nothing needs to be redesigned, which is why this is REVISE and not REJECT.

**Citation convention**: no file path was supplied with the fixture. I cite `BuggyFileInput.jsx:NN` using line numbers relative to the component source block exactly as given, where line 1 = `import React, { useState } from 'react';` and line 34 = `export default BuggyFileInput;`.

---

## Phase 0 — Test Evidence Intake

Evidence supplied is an `a11y-evidence-reader` CURATED digest (`def_rev: 2026-08-26a`) over three artifacts: an axe-core 4.13.0 scan, a keyboard-a11y-tester driven trace, and a keyboard-a11y-tester screen-reader reading-order census. All three are recorded as READ in full in the digest's Coverage Note. This is not a fix/remediation review, so the a11y-test Verification evidence contract type-match check does not apply.

### Evidence tiering (mandatory, and it changes how the findings below are labeled)

Per the protocol's digest rule, an evidence-reader digest is **detector output one tier below the artifact it cites** — a paraphrase, not the hard evidence. Findings resting on a digest line must be traced back by re-fetching at the cited handle, and anything that cannot be re-fetched is labeled **digest-only**.

This review operated under read constraints that permitted only the review prompt itself. I did **not** re-fetch at any of the digest's jq handles (`.viewports["1280x800"].violations[0]`, `.steps[0].ax_name_role_state`, `.entries[0..2]`, etc.). Therefore:

| Tier | What it covers here | Label |
|---|---|---|
| **Primary (in-prompt, verbatim)** | The component source block — supplied in full, not paraphrased | source-verified |
| **Digest-only** | Every axe rule row, every trace field, every census entry | digest-only |

Consequence: **no finding below rests solely on a digest line.** Each CRITICAL and MAJOR finding is anchored in the verbatim source; the digest lines are used as corroboration and are marked digest-only wherever cited. Where the digest is the *only* support for a claim, I have not filed it as a finding — those are in Open Questions.

### What the evidence actually establishes

**Machine-detectable / structural (digest-only):**
- axe-core 4.13.0 rule `label`, impact `critical`, `node_count 1`, `sample_selectors: ["input"]`, tags include `wcag2a`, `wcag412` (digest obs. 1, handle `.viewports["1280x800"].violations[0]`).
- Three further axe rows — `landmark-one-main`, `page-has-heading-one`, `region` — all impact `moderate`, all against `html` / `#root` (digest obs. 2–4). The digest states verbatim that **none of these three carries a `wcag2*` tag**; their tags are `best-practice` (plus RGAA tokens on `region`). See "Calibration" below — these are page-shell rows, not component findings.
- `.incomplete` is `[]`; `passes_count: 11`, `inapplicable_count: 76` with no corresponding arrays.

**Keyboard operability (digest-only, and it is clean):**
- step_0001 `Tab` → `#root > div > input`, `focus_moved: true`, `dom_order_index 12`, `focus_visible: {visible: true, indicator: "outline", contrast: 4.86, contrast_pass: true, aaa_pass: true, area_pass: true}` (obs. 6).
- step_0003 `Shift+Tab` returns to the same selector with identical AX values and identical focus-visible measurements (obs. 8).
- `[.steps[].focus_moved]` → `[true,true,true]` — no unresponsive keystroke in the session (obs. 11, absence claim 4).

This is measured fact, not design reasoning: **WCAG 2.4.7 Focus Visible and 2.4.13 Focus Appearance pass for this control**, at 4.86:1 against a 3:1 requirement, with `area_pass: true`. I am not manufacturing a focus-indicator finding, and I say so plainly.

### Evidence reconciliation — three traps in this pack, handled explicitly

**1. The trace records a name, and that name does not refute the axe `label` violation.**
Obs. 5/6/8 show `ax_name_role_state.name = "Choose File"`, `role = "button"` for `#root > div > input`. A name-presence check reading only the trace would conclude the control is named. It is not *author*-named. "Choose File" is the user-agent-intrinsic name of the file-picker button inside the input's UA shadow DOM — this is precisely the keyboard-a11y-tester calibration rule that name-presence checks do not cover UA-intrinsic names, and that a "Choose File" file input can still be missing its label. The axe `label` row and the trace name are **consistent, not contradictory**: an unlabeled file input has exactly this signature. Finding 1 stands.

**2. The trace's `role: "button"` is not a defect and I am not filing it as one.**
Chromium exposes `input[type=file]` through its UA shadow button; "button" is the computed exposure, not an authoring error. The digest itself notes (obs. 5) that no axe rule in this artifact belongs to a role-token family — the id list is exactly `["label","landmark-one-main","page-has-heading-one","region"]` (absence claim 1). No role finding.

**3. The census omits the file input entirely, and that is a tool blind spot, not a component defect.**
The census has three entries — `"document"`/body, `"Upload file"` (tag `null`, selector `null`), `"File too large"` (tag `null`, selector `null`) — with `truncated: false` (obs. 10). The input, which the trace proves has a name and role, does not appear. The best explanation is the documented shadow-DOM blind spot of the underlying virtual screen reader engine: it cannot see into shadow roots, and the file input's button lives in a UA shadow root. I flag this as a limitation of the census for this component and draw **no** conclusion that the control is invisible to real AT.

What the census *does* establish (digest-only): both `"Upload file"` and `"File too large"` resolve to **no tag and no selector**, and their `role` field echoes the phrase text rather than a WAI-ARIA role token. They are bare text in reading order with no element semantics and no relationship to any control. `declared_live_regions: []`, `declared_broken_aria_refs: []`, `declared_alternate_reading_order: []`. Nothing is broken because nothing exists.

### What the evidence does NOT establish (stated so I do not over-claim it later)

- **`live_announcements: [[],[],[]]` is not proof the error fails to announce.** The recorded keystrokes are `["Tab","Tab","Shift+Tab"]` — no file was ever selected, so the error branch never ran during the trace. Empty live announcements are *consistent with* the defect but do not measure it. The proof for Finding 2 comes from the verbatim source (no `role`, no `aria-live` at line 26) plus the census's `declared_live_regions: []`, which is the structural absence that the calibration rules require before silence counts as defect evidence.
- **`states.invalid: "false"` (obs. 5) is baseline-only.** It was captured with no file selected and no error present. It does not measure what `aria-invalid` does during the error state. The evidence for the missing invalid state is the source: there is no `aria-invalid` anywhere in the component, conditional or otherwise.
- **Focus reaching `body` after one Tab (obs. 7) is not a defect.** With exactly one focusable element on the page, Tab past it exits the document; CDP records `body` as the active element. The digest's own Not-claimed is explicit that a 3-step goal-driven session cannot establish the page's total focusable count. I file nothing here.
- **The `sr_announcement` delta between step_0001 and step_0003 (obs. 9) is not filed as a finding.** `new_phrases` is a delta field; an empty delta on revisit is expected behavior, not a missing announcement. The genuinely interesting fact — that step_0001's `focus_announcement` was `"document"` rather than the input's name/role — is ambiguous between coarse focus tracking in the emulated reader and a real gap. It goes to Open Questions with a concrete verification step.
- **No CSS was supplied.** Contrast (except the measured focus indicator), 200% reflow, and forced-colors behavior are unassessable. I mark them unmeasured rather than guessing from class names.

---

## Phase 1 — Pre-commitment Predictions (made before reading the source)

Component type: form with a file input and client-side validation. Predicted the five most likely design gaps:

1. Error message not associated with the input via `aria-describedby`.
2. `aria-invalid` never set, so the control reports itself valid while showing an error.
3. Visible label text present but not programmatically associated (a `<div>` where a `<label for>` belongs).
4. No live region, so the error is silent to assistive technology.
5. Constraints (accepted types, size cap) not exposed as programmatic help text.

All five landed. Comparison against actuals is in Phase 10 below.

---

## Phase 2 — Semantic HTML Audit

- Interactive element **is** native: `<input type="file">` at line 20-24. Native-HTML-first is satisfied for the control itself. No `div role="button"`, no `span` masquerading as anything.
- **Zero `aria-*` attributes exist anywhere in the component.** No ARIA is being used to paper over bad semantics — the defect class here is *absent* native association, not ARIA misuse. That distinction matters for the fix: the remedy is a `<label>`, not an ARIA retrofit.
- `<div>Upload file</div>` (line 19) is a text node where a `<label htmlFor>` belongs. The visible text exists; the association does not.
- `<div className="error-message">` (line 26) is a text node where a status container belongs.
- No headings, no landmarks, no lists, no tables in the component. Heading hierarchy and landmark structure are page-shell concerns (see Calibration).
- `<label>` is associated with **no** form input in this component — by `for`, by nesting, or by `aria-labelledby`.

## Phase 3 — ARIA Pattern Compliance Audit

There is no custom widget here, and therefore **no WAI-ARIA APG pattern applies**. A native file input with an associated `<label>`, an `aria-describedby` pointing at help text and error text, and `aria-invalid` toggled on failure *is* the complete pattern. Inventing an APG citation for this component would be a manufactured finding, and I am not making one. The correct references are WCAG 2.2 criteria, not APG patterns, and they are cited per finding below.

## Phase 4 — Focus Management Review

Measured clean within session scope (digest-only): Tab reaches the control, Shift+Tab returns to it, focus indicator is visible with `contrast 4.86 / contrast_pass true / aaa_pass true / area_pass true`, every keystroke moved focus. No keyboard trap in the recorded steps. No modal, no popover, no dynamic focus target, so focus restoration and focus trapping do not apply.

One unmeasured design point, source-derived: when the OS file dialog closes, the browser returns focus to the input. The component does not move focus, which is correct. But it also renders nothing new for the success case and renders an unassociated `<div>` for the failure case — so the returned focus lands on a control whose accessible name, role, and states are byte-identical before and after the outcome. Focus is fine; what focus lands on communicates nothing. That is a state-communication problem (Phase 5), not a focus problem, and I rate it there.

## Phase 5 — State Communication Audit

| State | Communicated visually | Communicated programmatically |
|---|---|---|
| Error present | Yes — `<div className="error-message">` (line 26-28) | **No** — no `role`, no `aria-live`, no `aria-describedby`, no `aria-invalid` |
| Invalid control | No (no styling supplied) | **No** — `aria-invalid` absent |
| File successfully selected | UA shadow text only (author renders nothing) | **No** — `selectedFile` is set at line 12 and never read |
| Selection discarded on cancel | UA shadow text reverts to "No file chosen" | **No** — silent |
| Accepted file types | Only inside the OS picker filter | **No** — no help text, no association |
| Size limit (5,000,000 bytes) | **Never, anywhere** | **No** |
| Loading / upload in progress | N/A — no upload code exists | N/A |

Four of the six real states are visual-only or absent entirely. That is the shape of this component's defect.

---

## Findings

### Critical Findings (blocks access)

**1. CRITICAL — The file input has no programmatic label; its accessible name is the browser's, not the author's.**

Evidence (source-verified): `BuggyFileInput.jsx:19` renders `<div>Upload file</div>` — a plain div, no `<label>`, no `htmlFor`. `BuggyFileInput.jsx:20-24` renders the input with `type`, `onChange`, and `accept` only — **no `id`, no `aria-label`, no `aria-labelledby`**. There is no mechanism of any kind connecting the visible text to the control.

Corroboration (digest-only, handle `.viewports["1280x800"].violations[0]`): axe-core 4.13.0 rule `label`, impact `critical`, `node_count 1`, `sample_selectors: ["input"]`, tags include `wcag2a`, `wcag412`. Cross-checked against the trace's captured name for the same selector (obs. 5/6/8, digest-only): `name = "Choose File"` — the UA-intrinsic name, confirming the control falls back to the browser's own string.

- **User groups impacted**: screen reader, speech input, cognitive.
- **WCAG**: 1.3.1 Info and Relationships (A), 4.1.2 Name, Role, Value (A), 3.3.2 Labels or Instructions (A), **2.5.3 Label in Name (A, WCAG 2.1+)**.
- **Confidence**: HIGH. **Could the developer refute this with context I'm missing?** NO — the source is complete and contains no labeling mechanism. **GAP, not preference.**

**Why this matters** — and why this is CRITICAL rather than MAJOR: the strongest argument is not the screen reader one. It is **speech input**. The visible label reads "Upload file"; the accessible name is "Choose File". A Dragon or Voice Control user who says *"click Upload file"* — the only label they can see — matches nothing. Their command does not work at all. That is complete loss of operability for one access method, which the Realist Check's recalibration rules explicitly forbid downgrading. The WCAG 2.5.3 mapping is a plain text comparison and is not arguable: the accessible name does not contain the visually presented label text.

Secondarily, a screen reader user navigating by form control (Tab, or NVDA/JAWS's forms list) hears only "Choose File, button" with no indication of purpose. On this single-control page, linear reading recovers the context because "Upload file" precedes the control in reading order (census obs. 10 records that order, digest-only). In any real form with a résumé, a cover letter, and a transcript, three controls all named "Choose File" are indistinguishable, and the user can upload the wrong document to the wrong field.

**Fix** — use the native element; do **not** reach for `aria-label`:

```jsx
<label htmlFor="file-upload">Upload file</label>
<input id="file-upload" type="file" accept=".pdf,.doc,.docx" onChange={handleFileChange} />
```

The tempting one-line fix, `aria-label="Upload file"` on the input, is the **wrong** fix and worth naming explicitly. It leaves the visible `<div>` text orphaned, it forgoes the click-target expansion a real `<label>` provides, and it re-creates the 2.5.3 risk the moment the two strings drift apart. A `<label htmlFor>` makes the visible text and the accessible name the same string by construction.

```
### A11y Evidence Finding
finding_id: file-input-missing-programmatic-label
fingerprint: not computed — this read-only review performed no hashing. Recompute as sha256("label|input|BuggyFileInput.jsx:20") for a stable id across runs.
source: component source BuggyFileInput.jsx:19-24 (primary, verbatim in prompt); axe-core 4.13.0 rule `label` via evidence digest def_rev 2026-08-26a, handle .viewports["1280x800"].violations[0] (digest-only, not re-fetched)
wcag_or_apg: WCAG 2.2 — 1.3.1, 3.3.2, 4.1.2, 2.5.3. No WAI-ARIA APG pattern applies (native control).
section_508_fpc_context: Section 508 not declared in scope for this review. If a Revised Section 508 claim is made, its web basis is WCAG 2.0 A/AA — 1.3.1, 3.3.2 and 4.1.2 fall inside that basis; 2.5.3 is WCAG 2.1-only and must NOT be labeled a Section 508 failure.
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, cognitive=HIGH, keyboard=LOW, low-vision=MEDIUM
evidence: BuggyFileInput.jsx:19 `<div>Upload file</div>`; BuggyFileInput.jsx:20-24 input with no id/aria-label/aria-labelledby; axe row {"id":"label","impact":"critical","node_count":1,"sample_selectors":["input"],"tags":[...,"wcag2a","wcag412",...]}; trace ax_name_role_state.name = "Choose File" (UA-intrinsic)
reproduction_steps: 1) Render the component. 2) Speech input: say "click Upload file" — no match. 3) Screen reader: navigate by form control to the input — hear "Choose File, button" with no purpose. 4) axe-core: rule `label` fires against selector `input`.
expected_behavior: The control's accessible name is the author's visible label, "Upload file", supplied by a <label for> association.
actual_behavior: The control's accessible name is the user-agent string "Choose File"; the visible text "Upload file" is an unassociated div with no tag or selector resolution in the reading-order census.
trend: new
```

---

**2. CRITICAL — Validation failure is silent to assistive technology. The error is rendered, never announced, and the control never reports itself invalid.**

Evidence (source-verified): `BuggyFileInput.jsx:25-29` conditionally renders `<div className="error-message">{error}</div>`. That div has **no `role="alert"`, no `aria-live`, and no `id`**. The input at `BuggyFileInput.jsx:20-24` has **no `aria-describedby` and no `aria-invalid`**. `setError('File too large')` fires at line 10; nothing in the component communicates that to AT.

Corroboration (digest-only): census `declared_live_regions: []` and `declared_broken_aria_refs: []` (obs. 10) — the structural absence that the calibration rules require before treating silence as defect evidence. The census does record `"File too large"` as a spoken phrase with `tag: null, selector: null`, i.e. reachable as bare document text in reading order but bound to nothing.

**Explicitly not claimed**: the trace's `live_announcements: [[],[],[]]` is *not* offered as proof, because no file was selected during that 3-keystroke session and the error branch never ran.

- **User groups impacted**: screen reader (primary), cognitive.
- **WCAG**: 4.1.3 Status Messages (AA, WCAG 2.1+), 3.3.1 Error Identification (A), 1.3.1 Info and Relationships (A), 4.1.2 Name, Role, Value (A).
- **Confidence**: HIGH. **Could the developer refute this?** NO — the absence is total and visible in the supplied source. **GAP.**

**Why this matters**: a screen reader user picks a 6 MB PDF. The OS dialog closes. Focus returns to the input. Absolutely nothing happens in their world — no announcement, no state change on the control they are focused on, no reason to suspect anything. They move on and submit. This is the textbook case the severity scale names as CRITICAL: *form validation fails silently*. There is no workaround the user can discover, because discovering it requires knowing to go looking for text they have no reason to believe exists.

**Fix** — and the naive fix does not work. Adding `role="alert"` to the conditionally-rendered div at line 26 mounts an alert element that already contains its text; that pattern announces unreliably across AT and is the documented inconclusive case. Use a **persistent container** that is always in the DOM and whose *contents* change:

```jsx
const errorId = 'file-upload-error';

<input
  id="file-upload"
  type="file"
  accept=".pdf,.doc,.docx"
  onChange={handleFileChange}
  aria-describedby={`file-upload-help${error ? ` ${errorId}` : ''}`}
  aria-invalid={error ? 'true' : undefined}
/>

{/* always rendered, never conditionally mounted */}
<div id={errorId} role="alert" className="error-message">
  {error}
</div>
```

Two mechanisms, deliberately, because they do different jobs: `role="alert"` on the persistent container handles **notification** at the moment of failure; `aria-describedby` + `aria-invalid` handle **recovery**, so that a user returning to the control later hears "Choose File, button, invalid, File too large" instead of the same neutral announcement they heard before the failure. Per the DOM-verification anti-pattern: verify in the accessibility tree that the `aria-describedby` id reference actually resolves and that `aria-invalid` lands on the input, not on a wrapper — a unit test asserting the prop is not sufficient.

```
### A11y Evidence Finding
finding_id: file-error-not-announced-not-associated
fingerprint: not computed — this read-only review performed no hashing. Recompute as sha256("no-live-region|div.error-message|BuggyFileInput.jsx:26") for a stable id across runs.
source: component source BuggyFileInput.jsx:20-29 (primary, verbatim in prompt); sr-census declared_live_regions and entry index3 via evidence digest def_rev 2026-08-26a, handle .["http://127.0.0.1:8777/file-input-no-labels.html"].entries[0..2] (digest-only, not re-fetched)
wcag_or_apg: WCAG 2.2 — 4.1.3, 3.3.1, 1.3.1, 4.1.2
section_508_fpc_context: Section 508 not declared in scope. If claimed, the WCAG 2.0 A/AA basis covers 3.3.1, 1.3.1 and 4.1.2; 4.1.3 Status Messages is WCAG 2.1-only and must NOT be labeled a Section 508 failure.
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, cognitive=HIGH, low-vision=MEDIUM, keyboard=LOW
evidence: BuggyFileInput.jsx:26 `<div className="error-message">` with no role/aria-live/id; BuggyFileInput.jsx:20-24 input with no aria-describedby/aria-invalid; census {"declared_live_regions":[],"declared_broken_aria_refs":[]}; census entry {"index":3,"spoken_phrase":"File too large","role":"File too large","tag":null,"selector":null}
reproduction_steps: 1) With a screen reader running, focus the file input. 2) Select a file larger than 5,000,000 bytes. 3) Observe: no announcement on return from the picker. 4) Shift+Tab away and Tab back to the control — it still announces as valid with no description.
expected_behavior: On validation failure the error is announced without moving focus, the control reports aria-invalid="true", and re-focusing the control announces the error text via aria-describedby.
actual_behavior: The error div is inserted with no role, no aria-live, no id and no inbound reference; the control's name, role and states are unchanged by the failure.
trend: new
```

---

### Major Findings (significantly degrades experience)

**3. MAJOR — The enforced constraint is never stated, and the stated constraint is never enforced.**

Evidence (source-verified): `BuggyFileInput.jsx:9` enforces `file.size > 5000000` — 5,000,000 bytes, ≈5 MB decimal / ≈4.77 MiB. **This limit appears nowhere in the rendered output.** `BuggyFileInput.jsx:23` sets `accept=".pdf,.doc,.docx"`, which filters the OS picker but is never checked in `handleFileChange` — a user who switches the picker to "All Files" can select a `.exe` and the component accepts it (line 12).

The inversion is the point: **the constraint that is communicated is not enforced, and the constraint that is enforced is not communicated.** There is no help text element, and consequently nothing for `aria-describedby` to point at even if the association from Finding 2 were added.

The error text compounds it. `BuggyFileInput.jsx:10` sets `'File too large'` — it names the failure but not the threshold and not the corrective action. A user cannot determine whether 4 MB or 2 MB will succeed; they can only bisect by trial, and for a screen reader user each trial produces no feedback at all (Finding 2). The recovery loop is closed.

- **User groups impacted**: cognitive (primary), screen reader, all users.
- **WCAG**: 3.3.2 Labels or Instructions (A), 3.3.3 Error Suggestion (AA).
- **Confidence**: HIGH. **Refutable?** NO. **GAP.**
- **Why this matters**: undiscoverable constraints guarantee failure for anyone whose file happens to be large — and this component makes that failure unrecoverable for the users least able to absorb it.

**Fix**:
```jsx
const MAX_FILE_BYTES = 5_000_000;   // no magic number in the handler

<p id="file-upload-help">PDF, DOC or DOCX. Maximum size 5 MB.</p>
// ...aria-describedby="file-upload-help" on the input (see Finding 2)

// and make the error actionable and consistent with the stated rule:
setError(`That file is ${formatMB(file.size)}. The maximum size is 5 MB — please choose a smaller file.`);
```
Also validate the extension/MIME type in the handler so the `accept` promise is actually kept.

---

**4. MAJOR — Successful selection is never confirmed by the component. `selectedFile` is dead state.**

Evidence (source-verified): `selectedFile` is declared at `BuggyFileInput.jsx:4` and written at `BuggyFileInput.jsx:12`. It is **never read** — it appears in no JSX expression anywhere in lines 17-31. On success the component's rendered output is byte-identical to its output before the file was chosen.

- **User groups impacted**: screen reader (primary), cognitive.
- **WCAG**: 1.3.1 Info and Relationships (A) for the general absence of author-controlled confirmation. Note the precise scope: **4.1.3 Status Messages does not apply to the success path**, because 4.1.3 governs status messages that *are* presented; here none is presented at all. I am deliberately not stretching the citation.
- **Confidence**: HIGH on the structural fact (dead state, verified in source); the *degree* of downstream AT impact is browser-dependent, and I scope the claim accordingly rather than overstating it.
- **GAP.**

**Why this matters**: the component delegates its entire success feedback to the browser's own shadow-DOM filename text — a string the author cannot style, position, associate, or announce. The asymmetry is the design defect worth naming: the failure path renders something (unannounced), and the success path renders nothing. Neither outcome produces an author-controlled signal, so the two most important events in this interaction are both invisible to the layer that AT actually consumes. Whether a given screen reader re-announces the UA filename when focus returns from the picker is exactly the kind of thing a design should not be depending on.

**Fix**: render the selection into the same persistent status container used for the error, or a sibling one, e.g. `<p role="status">Selected: {selectedFile.name}</p>`. This also removes the dead-state smell — the value gets a job.

---

**5. MAJOR — Cancelling the file picker silently discards a previously chosen file, and the error branch leaves stale state behind.**

Evidence (source-verified): `BuggyFileInput.jsx:8-14`.

```js
const file = e.target.files[0];
if (file && file.size > 5000000) {
  setError('File too large');
} else {
  setSelectedFile(file);
  setError(null);
}
```

Two branch defects:
- **Cancel path**: if the user opens the picker and cancels, `e.target.files[0]` is `undefined`, so `file` is falsy, so the condition is false, so the **else** branch runs — `setSelectedFile(undefined)` and `setError(null)`. A previously valid selection is wiped and any standing error is cleared, with no notice. This is the else-branch-coverage anti-pattern in its purest form: the guard `file &&` protects the size check but hands the empty case to the success branch.
- **Error path**: when a too-large file is chosen, `setSelectedFile` is never called, so a previously accepted file stays in state while an error is displayed. State and message now disagree.

- **User groups impacted**: screen reader and cognitive disproportionately; all users somewhat.
- **WCAG**: 1.3.1 (A) and 4.1.2 (A) for the uncommunicated state change. **WCAG 3.3.4 Error Prevention (AA) is conditionally applicable** — it governs user-controllable data being deleted, which a discarded upload arguably is, but only if this form's context qualifies. I flag that citation as conditional rather than asserting it.
- **Confidence**: HIGH on the control-flow reading. **Refutable?** NO — the branch behavior follows directly from the quoted lines. **GAP.**

**Why I am rating this at MAJOR despite the weak direct WCAG hook**: severity here reflects user impact, not criterion weight. A sighted user gets a real cue — the UA text reverts to "No file chosen". A screen reader user gets nothing, which makes silent data loss an access issue rather than a general bug. Rating this MINOR because the SC mapping is soft would be exactly backwards.

**Fix**:
```js
const handleFileChange = (e) => {
  const file = e.target.files[0];
  if (!file) return;                      // cancel: change nothing, say nothing
  if (file.size > MAX_FILE_BYTES) {
    setSelectedFile(null);                // don't leave a stale selection alongside an error
    setError(`That file is ${formatMB(file.size)}. The maximum size is 5 MB — please choose a smaller file.`);
    return;
  }
  setSelectedFile(file);
  setError(null);
};
```

---

### Minor Findings (friction but workaround exists)

- **Error message may rely on colour alone — needs verification.** `BuggyFileInput.jsx:26` supplies `className="error-message"` and no stylesheet was provided. The **markup itself carries no non-colour indicator**: no icon, no "Error:" prefix, no programmatic role. If `.error-message` is the conventional `color: red`, WCAG 1.4.1 Use of Color (A) fails, and nothing in the component provides a fallback. **Needs user verification** — concrete check: inspect the computed styles for `.error-message`, and view the component in Windows High Contrast / forced-colors mode to confirm the error remains distinguishable from body text. Fixing Finding 2 with `role="alert"` supplies the missing non-colour signal for AT users but not for sighted users who do not use AT; an icon or an "Error:" prefix covers them.
- **No `id` on the input at all** (`BuggyFileInput.jsx:20-24`), so there is currently no anchor for any future `aria-describedby`, `aria-errormessage`, or `<label for>`. Subsumed by the fixes above; noted because it is the single attribute that unblocks three of them.
- **`5000000` is an unnamed magic number** at `BuggyFileInput.jsx:9`. It is also the number that must appear in the help text and the error string, so it needs to become a single named constant or the three will drift apart — and a help text that disagrees with the enforced limit is worse than no help text.

### Enhancements (best practice not met, no access barrier from this component)

- **Page-shell axe rows are not component findings.** `landmark-one-main` (`html`), `page-has-heading-one` (`html`), and `region` (`#root`) fired at `moderate` impact (digest obs. 2-4, digest-only). The digest states verbatim that **none carries a `wcag2*` tag** — they are `best-practice` rules. A component that renders into `#root` cannot supply the host document's `<main>` or `<h1>`. These belong to whatever page embeds this component and should be verified at page scope, where 1.3.1 and 2.4.1 may genuinely apply. Converting three moderate best-practice rows into findings against a 34-line file would be a manufactured violation, and I am declining to do it.
- **`role="status"` on a success container** (Finding 4's fix) and an upload-progress region would both be worth designing now if this component will eventually POST the file — there is currently no upload code, so no `aria-busy` / progress finding exists yet.

---

## What's Missing (gap analysis)

Absences, stated as absences:

1. **A `<label>` element.** None exists in the component. (Finding 1)
2. **An `id` on the input.** No association of any kind is currently possible. (Finding 1, 2)
3. **`aria-describedby`.** No help text and no error text is bound to the control. (Finding 2, 3)
4. **`aria-invalid`.** The control reports itself valid in every state it can reach. (Finding 2)
5. **A persistent live-region container.** `declared_live_regions: []` (digest-only) confirms nothing announces. (Finding 2)
6. **Any statement of the 5,000,000-byte limit.** Enforced, never disclosed. (Finding 3)
7. **Any enforcement of the declared `accept` types.** Declared, never enforced. (Finding 3)
8. **Any success confirmation.** `selectedFile` is written and never read. (Finding 4)
9. **Cancel-path handling.** The empty-file case falls through to the success branch. (Finding 5)
10. **A non-colour error indicator in markup.** No icon, no prefix, no role. (Minor)
11. **`required` / `aria-required` semantics.** The fixture does not state whether upload is mandatory, so I make no finding — but the component cannot express it either way today. Noted as an unstated assumption, not a defect.
12. **Any CSS.** Contrast beyond the measured focus indicator, 200% reflow, and forced-colors behavior are unassessed, not passed.
13. **Any `<form>` or submit context.** Whether the error blocks submission is unknowable from this fragment; if it does not, Finding 2's silent failure gets worse.

Anti-pattern checks run against this component: broadcast-vs-association — **would apply** if `role="alert"` were added per-field inside a loop, which is why Finding 2's fix specifies one persistent container rather than a per-error one; `title`-as-name — not present; ARIA-without-visible-label — the mirror image is present (visible label without ARIA or native association, Finding 1); else-branch coverage — **hit** (Finding 5); single-selector scope, td-in-loop headers, `role="presentation"` on data tables, decorative alt — not applicable to this component; DOM-verification — required for the Finding 2 fix and called out there.

---

## Phase 6 — Multi-Perspective Notes

**Screen reader user**: Encounters, in order, the text "Upload file" bound to nothing, then a control named "Choose File" with role button. Activates it, chooses a file, and returns to a control whose name, role, and state are exactly what they were before. On failure, the words "File too large" are inserted into the document behind them with no announcement, no association, and no invalid state on the control they are focused on. The census (digest-only) records both text strings with `tag: null, selector: null` — bare text in reading order, related to nothing. This perspective carries both CRITICALs.

**Keyboard-only user**: The best-served perspective, and measured rather than assumed. Tab reaches the control (`dom_order_index 12`), Shift+Tab returns to it, `focus_moved: true` on all three recorded keystrokes, focus indicator visible as an outline at **4.86:1** with `contrast_pass`, `aaa_pass`, and `area_pass` all true (digest-only, obs. 6/8/11). No trap. WCAG 2.1.1, 2.1.2, 2.4.7, and 2.4.13 have no findings against them here. Scope caveat: this was a 3-step goal-driven session, not a full-page tab sweep, so it establishes what this session encountered and not the page's total focus order.

**Low vision user (200% zoom, high contrast, magnifier)**: Largely unassessed — no CSS supplied. The one measured fact is favourable (focus indicator 4.86:1). Two open risks: the error may be distinguished by colour alone (Minor), and a magnifier user who has zoomed into the file input will not see an error inserted below the viewport with no announcement to pull them there — which is the same defect as Finding 2 arriving through a different door. **WCAG 2.5.8 Target Size is NOT a finding**: the file-picker button is a user-agent control the author has not modified with any CSS, which is an explicit exception to 2.5.8. Filing it would be a false positive.

**Cognitive accessibility user**: The second-worst-served perspective. A size limit that is enforced but never stated; a type restriction that is stated but never enforced; an error that names the problem but not the threshold or the remedy; a cancel action that silently destroys a prior selection; and no confirmation that anything succeeded. Each of these is individually survivable. Together they produce an interaction where the user cannot form a correct mental model of the rules, cannot tell whether they have complied, and cannot tell what changed.

**Vestibular & motion**: No animation, transition, parallax, or auto-playing content in the source. Nothing to review. No `prefers-reduced-motion` finding, because there is no motion to suppress.

**Auditory access**: No `<video>`, `<audio>`, or media of any kind. Not applicable.

**Environmental contrast**: Focus indicator measured at 4.86:1 (passes the 3:1 requirement for a non-text UI indicator, and would pass even the stricter 4.5:1 text threshold). Everything else is unverifiable without the stylesheet: text contrast, forced-colors behavior, and the colour-only error risk. Marked unmeasured, not passed.

### Perspective Alarm Levels

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | **HIGH** | Unlabeled control (axe `label`, critical); error with no role/aria-live/aria-describedby/aria-invalid; `declared_live_regions: []` |
| Keyboard-only | LOW | Measured clean in session: focus reaches and returns, indicator 4.86:1 with area_pass, `focus_moved: [true,true,true]`. Caveat: 3-step session, not a full tab-order sweep |
| Low vision | MEDIUM | No CSS supplied; error may be colour-only; off-viewport error insertion with no announcement under magnification |
| Cognitive | **HIGH** | Undisclosed size limit; unenforced type restriction; error without correction; silent cancel-discard; no success confirmation |
| Vestibular & motion | LOW | No animation, transition, or auto-playing content in source |
| Auditory access | LOW | No media elements |
| Environmental contrast | MEDIUM | Stylesheet not supplied; colour-only error risk; forced-colors behavior unknown |

**Escalation**: Screen reader and Cognitive are at HIGH; Low vision and Environmental contrast are at MEDIUM. All four should be flagged for deep review via `/perspective-audit`, with the low-vision and contrast lanes blocked until the stylesheet is available.

---

## Phase 8 — Realist Check (severity calibration)

Every CRITICAL and MAJOR was run through the four questions. Recalibrations and confirmations:

- **Finding 1 (no label) — held at CRITICAL, not downgraded.** Worst realistic case is not "slightly confusing"; it is a speech-input user whose spoken command for the only label they can see matches nothing, which is complete loss of operability for that access method. The rules forbid downgrading complete access loss. Detection is fast (axe caught it in one scan), and I note that in the finding — but fast detection does not change the severity, it changes the cost of the fix.
- **Finding 2 (silent validation) — held at CRITICAL.** The severity scale names "form validation fails silently" as CRITICAL by definition, and there is no user-discoverable workaround. Held.
- **Association + `aria-invalid`, considered separately, would be MAJOR, not CRITICAL** — with a single control the "which field?" problem is trivial, and the error text sits in reading order immediately after the input. I have kept it inside Finding 2 rather than splitting it, because the announcement gap is the CRITICAL half and splitting would either double-count the severity or bury the recovery gap. **In a multi-field form this half becomes CRITICAL on its own.** Flagging that explicitly so the calibration is not mistaken for a judgment that association is optional.
- **Findings 3 and 4 (instructions, error suggestion) — merged into one MAJOR.** I initially had 3.3.2 and 3.3.3 as separate findings. They share a root cause (the constraint layer does not exist) and their severity would have been double-counted. Merged, both SCs cited, both fixes given. *Mitigated by: nothing — but merging prevents inflation of the finding count.*
- **Finding 4 (no success confirmation) — held at MAJOR with the claim scoped.** A workaround arguably exists (re-focus the control and hope the browser exposes the filename), which under the recalibration rules would suggest MINOR. I held MAJOR but narrowed the claim to what is refutation-proof — dead state, no author-controlled confirmation, asymmetric success/failure paths — and moved the browser-dependent question of what AT actually announces on focus return to Open Questions. *Mitigated by: browsers render the filename in UA shadow text, so sighted users are not affected and screen reader users may recover it on re-focus.*
- **Finding 5 (silent cancel-discard) — held at MAJOR despite a soft SC mapping.** Severity here reflects impact on people, not criterion weight. Sighted users get a UA cue; screen reader users get nothing, which is what makes it an access finding rather than a general bug.
- **Three axe rows deliberately NOT promoted to findings.** `landmark-one-main`, `page-has-heading-one`, `region` are page-shell, best-practice-tagged, and carry no `wcag2*` tag per the digest's own verbatim quotation. Filed as ENHANCEMENT with page-scope verification instead.
- **Three further candidate findings rejected outright** as false positives: the trace's `role: "button"` (correct UA exposure), focus reaching `body` (expected end-of-document behavior with one focusable element), and WCAG 2.5.8 target size (explicit user-agent-control exception applies, no author CSS).

## Phase 9 — Self-Audit

| Finding | Confidence | Developer could refute? | Gap or preference? | Disposition |
|---|---|---|---|---|
| 1 — no programmatic label | HIGH | NO | GAP | Keep, CRITICAL |
| 2 — silent validation | HIGH | NO | GAP | Keep, CRITICAL |
| 3 — constraints undisclosed / unenforced | HIGH | NO | GAP | Keep, MAJOR |
| 4 — no success confirmation | HIGH (structural) / MEDIUM (AT impact) | Partly, on AT impact only | GAP | Keep MAJOR with the claim scoped; AT-impact question → Open Questions |
| 5 — silent cancel-discard | HIGH | NO | GAP | Keep, MAJOR |
| Error colour-only | LOW (no CSS supplied) | YES | GAP if confirmed | Downgraded to MINOR + Needs user verification |
| `sr_announcement` delta (obs. 9) | LOW | YES | Undetermined | → Open Questions, not filed |
| Census omits the input (obs. 10) | LOW as a defect claim | YES | Tool limitation | → Reconciliation note, not filed |

Calibration statement, made deliberately: **the semantics that are present are correct.** The control is native, no ARIA is misused, no `div role="button"` is masking anything, and the keyboard and focus-indicator behavior is measured clean at 4.86:1 with `area_pass: true`. This component's problem is entirely one of missing associations and missing announcements, and saying so precisely is more useful than treating a 34-line file as broadly broken.

## Phase 10 — Synthesis vs. Pre-commitment Predictions

| Prediction | Outcome |
|---|---|
| Error not associated via `aria-describedby` | **Confirmed** (Finding 2) |
| `aria-invalid` never set | **Confirmed** (Finding 2) |
| Visible label not programmatically associated | **Confirmed** (Finding 1) |
| No live region → silent error | **Confirmed** (Finding 2) |
| Constraints not exposed as help text | **Confirmed** (Finding 3) |

Five for five, which is itself a signal — this fixture's defects are the canonical ones for its component type, and prediction accuracy is not evidence of thoroughness.

**What I did not predict, and would have missed without reading closely:**
- The **cancel-path fall-through** at line 8-14 (Finding 5). No checklist produces this; it required tracing what `e.target.files[0]` is when the picker is dismissed.
- **`selectedFile` as dead state** (Finding 4) — the success path renders nothing at all, which is a stronger statement than "success is announced poorly".
- The **constraint inversion** in Finding 3 — `accept` communicated but unenforced, size enforced but uncommunicated.
- The **2.5.3 Label in Name / speech-input** angle, which turned out to be the strongest argument for Finding 1's severity and is stronger than the screen reader argument I expected to lean on.

**What surprised me in the evidence rather than the code**: three of the four axe rows are page-shell noise with no WCAG tag, the trace supplies a name that superficially contradicts the axe `label` violation but actually corroborates it, and the reading-order census omits the very control under review. This pack rewards reconciliation and punishes row-counting.

---

## Verdict Justification

**REVISE.** Two CRITICAL findings — an unlabeled control and a validation failure that is silent to assistive technology — are each sufficient on their own to block shipping. Together they mean a screen reader or speech-input user cannot reliably identify what the control is for, and cannot learn that their upload failed.

**Why not REJECT**: the underlying approach is sound. The control is a native `<input type="file">`, there is no ARIA to unwind, no wrong APG pattern has been adopted, and the keyboard and focus-indicator behavior is measured clean. Every defect is repaired by *adding* markup — a `<label htmlFor>`, an `id`, a persistent status container, `aria-describedby`, `aria-invalid`, and a help-text element — plus one small control-flow correction in `handleFileChange`. That is roughly fifteen lines and no architectural change. Rejecting a design whose foundation is correct would misdirect the fix.

**Why not ACCEPT-WITH-RESERVATIONS**: silent validation failure is not a reservation. It is the failure mode where the user believes they succeeded.

**To upgrade to ACCEPT**, all of the following must be true and DOM-verified in the rendered output (not asserted by unit tests on props):
1. The input has an `id`, and a `<label htmlFor>` supplies the accessible name "Upload file". Verify in the accessibility tree that the computed name is the author's string, not "Choose File".
2. A persistent (always-mounted) container carries the error text with `role="alert"`, and the input carries `aria-describedby` pointing at it plus `aria-invalid="true"` while the error is present. Verify both id references actually resolve.
3. Help text stating the accepted types and the 5 MB limit exists, is visible, and is referenced by `aria-describedby`.
4. The error text names the limit and the corrective action.
5. `handleFileChange` returns early on cancel and clears `selectedFile` on the error branch.
6. Success is confirmed by author-rendered, programmatically-determinable output.
7. The stylesheet is supplied and the error is distinguishable by more than colour, including in forced-colors mode.

**Review escalation**: Screen reader and Cognitive perspectives are at HIGH and should go to `/perspective-audit`. Low vision and Environmental contrast are at MEDIUM and are blocked on the stylesheet.

**Standing caveat on this review's evidence**: all machine evidence cited above is **digest-only** and was not re-fetched at the handles the digest names. Every CRITICAL and MAJOR finding is independently anchored in the verbatim component source, so no finding collapses if a digest line turns out to be a paraphrase error — but any downstream consumer treating the axe rule ids, trace values, or census entries as measured fact should re-fetch at the stated jq paths first.

---

## Open Questions (unscored)

1. **What does a screen reader actually announce when focus returns from the file picker after a successful selection?** The trace never selected a file, so this is unmeasured. This is the one question that would move Finding 4's severity in either direction. Concrete check: a `@guidepup/virtual-screen-reader` component assertion in the project's Vitest suite capturing spoken phrases before and after a programmatic file selection — noting that VSR cannot see into the file input's UA shadow root, so this may need a real-AT smoke test instead.
2. **Why was `step_0001.focus_announcement` `"document"` rather than the input's name and role?** (digest obs. 9, digest-only.) `new_phrases: []` at step_0003 is an expected delta on revisit and is not suspicious. The step_0001 value is. It is ambiguous between coarse focus tracking in the emulated reader and a genuine gap, and the digest explicitly declines to judge it. I have not filed it. Concrete check: re-run the driven session with a focus-announcement assertion, or capture the same focus event under a real screen reader.
3. **Is this control required?** If upload is mandatory, `required` / `aria-required` and a submit-blocking path are missing, and the silent-failure severity in Finding 2 rises. Not knowable from the fixture.
4. **What does `.error-message` actually render as?** Determines whether the colour-only Minor is a real 1.4.1 failure. Needs the stylesheet.
5. **Does the host page supply `<main>`, an `<h1>`, and landmark structure?** The three moderate axe rows fired against `html` / `#root` and are page-shell, not component. They need verification at page scope, where they may map to real WCAG criteria even though the artifact tags them `best-practice` with no `wcag2*` token.
6. **Does anything consume `selectedFile` downstream?** If a parent lifts this state, Finding 4's fix may belong there rather than here. The fragment as supplied gives no indication either way.
7. **Tool provenance gap, carried forward from the digest's Not-claimed**: neither `trace.json` nor `sr-census.json` self-declares a tool or version; the keyboard-a11y-tester attribution rests on directory naming. Only axe-core self-declares (`axe_core_version: 4.13.0`). If these artifacts are used as evidence in a conformance claim, that provenance should be established rather than inferred. The digest also notes the question named a fourth tool ("batch-crawl findings") for which no artifact was supplied — nothing in this review is sourced from it.
