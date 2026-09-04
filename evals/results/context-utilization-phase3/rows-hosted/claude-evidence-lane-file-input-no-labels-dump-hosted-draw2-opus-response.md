**VERDICT: REJECT**

**Overall Assessment**: This component ships a file upload control that a screen reader user cannot identify and a validation failure that no user of assistive technology will ever be told about. The visible label exists as a `<div>` with no programmatic tie to the input, so the only accessible name is the user agent's intrinsic "Choose File" — confirmed by both axe-core (`label`, impact critical) and the driven keyboard trace (`ax_name_role_state.name: "Choose File"`). The error path is worse: the "File too large" message renders into the DOM with no `role`, no `aria-live`, no `id`, no `aria-describedby` reference, and no `aria-invalid` on the input, so a screen reader user who selects a 6 MB PDF is told nothing and has no reason to go look. The keyboard layer, by contrast, measures genuinely clean — single tab stop, no trap, focus indicator passing 2.4.7 *and* 2.4.13 — so the remediation is additive, not a rebuild.

**Citation convention**: The fixture supplies no file path. Line numbers below are relative to the component source block (`import React...` = line 1); add 7 to map onto the prompt file. Cited as `BuggyFileInput.jsx:NN`.

---

## Phase 0 — Evidence Intake

**Review type**: Fresh design pass, not a remediation review. The component is presented as new code, not as a fix for a prior finding, so a11y-test's Verification evidence contract type-match check does not apply here — there is no claimed fix whose evidence type could be mismatched. Noting this rather than skipping it silently.

**Scope ruling on the evidence pack (load-bearing)**

The pack contains **21 artifacts. Three are in scope. Eighteen are not.**

In scope — all three resolve to `http://127.0.0.1:8777/file-input-no-labels.html`:
| Artifact | Type | Key facts used |
|---|---|---|
| `raw/axe-batch-2026-08-25/010-127-0-0-1-8777-file-input-no-labels-html.json` | axe-core 4.13.0, 1280x800, status `measured` | `label` violation (impact critical, node_count 1, selector `input`); 3 best-practice violations; `incomplete: []`; passes 11 |
| `raw/file-input-no-labels-kat-driven/trace.json` | keyboard-a11y-tester, `mode: driven-live`, personas keyboard + screen-reader | steps 0001–0003; AX name/role/state; focus_visible; focus_appearance; sr_announcement |
| `raw/file-input-no-labels-kat-census/sr-census.json` | KAT screen-reader reading-order census, captured 2026-08-26T18:02:20Z | 3 entries; `declared_live_regions: []`; `declared_broken_aria_refs: []`; `truncated: false` |

Out of scope — 18 same-batch axe scans of **different URLs** (`accordion-no-region-role`, `app-focus-order-illogical`, `async-form-vague-success`, `breadcrumb-navigation-no-nav-landmark`, `button-skip-link-clean`, `checkbox-group-no-fieldset`, `combobox-autocomplete-no-listbox-role`, `dashboard-heading-inconsistency`, `data-table-missing-scope`, `expandable-section-no-button`, `form-field-vs-summary-errors`, `form-validation-missing-aria-describedby`, `heading-hierarchy-skipped`, `image-carousel-no-region`, `infinite-scroll-no-announcement`, `interactive-dropdown-clean`, `interactive-dropdown-focus-bug`, `loading-state-missing-aria-busy`).

**No finding in this review derives from those 18 files.** The `target-size` violations belong to the accordion and carousel pages; the `color-contrast` violations belong to the dashboard page; the `tabindex` violation belongs to `app-focus-order-illogical.html`; the `aria-valid-attr-value` incompletes belong to the two dropdown pages. Importing any of them into this review would be fabrication. They are used exactly once below, as *negative* cross-checks (see the target-size note in Enhancements), which is the only legitimate use of a sibling scan: proving a rule was live in the batch.

**KAT calibration rules — all four applied**

1. *Batch-crawl 4.1.3 findings are prompts, not failures.* Not applicable: `mode` is `driven-live`, not a batch crawl, and no `deterministic-findings.json` was supplied, so the tool emitted no 4.1.3 verdict at all. My 4.1.3 finding below is derived from source plus the census's declared field, not from a crawl artifact.
2. *Name-presence checks don't cover UA-intrinsic names — a "Choose File" file input can still be missing its label.* **Directly on point, and this is the documented example verbatim.** The trace reports a non-null name; that non-null name is the user agent's, not the author's. Applied in CRITICAL-1.
3. *Journey-level verdicts are judgment-layer claims.* Not applicable: the trace carries no verdict fields, only per-step measured facts. Nothing here is accepted as a bare journey verdict.
4. *`conformance_level` is a pass/fail gate, not the SC's WCAG level.* Not applicable: no `conformance_level` field appears in either KAT artifact.

**Coverage gaps in the evidence (material — read before trusting the pack)**

- **The driven session never exercises the journey it declares.** The stated goal is *"Choose a file to upload using only the keyboard and review any feedback the page gives."* The trace contains three keystrokes — `Tab`, `Tab`, `Shift+Tab`. No `Enter`/`Space` opens the picker; no step follows a selection. Yet step_0001 already reports `text: "C:\fakepath\quarterly-report.pdf"`, so a file was in place before the first keystroke (harness setup). **The selection-and-feedback half of the goal is unmeasured.** Every error-path finding below therefore rests on source reading corroborated by the census, *not* on the driven trace. Anyone treating "a driven trace exists" as coverage of the error path is reading the filename, not the file.
- **No `deterministic-findings.json`.** The tool's own findings layer is absent, so there is no measured verdict to defer to or contest.
- **No CSS.** The `.file-upload` and `.error-message` rules are not in the pack, so contrast and color-only-indication claims for the error state cannot be closed out (see Low vision perspective).
- **Two captures, not one session.** The axe scan (00:06:29Z) and the census (18:02:20Z) are ~18 hours apart, and the trace is undated. The census shows "File too large" present; the trace shows `invalid: "false"`. I do **not** claim these describe one moment, and no finding depends on their being the same session.

**Two artifact-reading traps in this pack, named so they are not filed as findings**

- In `sr-census.json`, entries 2 and 3 carry `"role": "Upload file"` and `"role": "File too large"` — the `role` field is echoing the spoken phrase, with `tag: null` and `selector: null`. These are **not** ARIA roles. Reporting "invalid role value" here would manufacture a violation.
- The census lists **no entry for the input itself**. The trace proves the control *is* in the accessibility tree (`role: "button"`, name `"Choose File"`). The census gap is most consistent with the census enumerating text content, not with the control being absent from the AX tree. **Not filed as a finding** — the two artifacts would contradict each other, and the trace is the stronger evidence.

---

## Phase 1 — Pre-commitment Predictions

Before reading the source, for a file input with client-side validation I predicted:

1. Visible label present as non-`<label>` markup, no `htmlFor`/`id` pair → **HIT** (CRITICAL-1).
2. Error not associated via `aria-describedby`, `aria-invalid` never set → **HIT** (CRITICAL-2).
3. Error rendered without any live region, so it appears silently → **HIT** (CRITICAL-2).
4. `accept` treated as if it were validation and as if it communicated the constraint to users → **HIT** (MAJOR-2).
5. Accepted-file state held in React but never surfaced as confirmation → **HIT** (MINOR-1).
6. Focus indicator weak or focus mismanaged when the error appears → **MISS, and the measurement says so.** Focus is measurably fine. I predicted a problem that does not exist; the trace refutes me (see Keyboard perspective).
7. Focus should move to the error on failure → **deliberately not filed.** For a single-field inline error, moving focus is the wrong pattern and edges into 3.2.1 surprise. Association plus one alert region is correct here.

Surprise: the *size* of the gap between "the error is in the accessibility tree" and "the user is ever told about it." The census proves the error text is reachable by exploration (index 3). That makes this a subtler failure than "invisible to AT" — it is discoverable but unannounced, which is worse, because nothing gives the user a reason to go look.

---

## Findings

> **Fingerprint disclosure**: the `fingerprint` values in the blocks below are author-assigned stable identifiers for this review. They are **not** tool-recomputed hashes — no hashing tool was run in this read-only pass. Re-derive them from the harness before filing these as issues.

### Critical Findings (blocks access)

**CRITICAL-1 — The file input has no author-supplied accessible name; the visible label is an unassociated `<div>`.**

`BuggyFileInput.jsx:19` renders `<div>Upload file</div>`. `BuggyFileInput.jsx:20-24` renders the `<input type="file">` with `onChange` and `accept` only — no `id`, no wrapping `<label>`, no `aria-label`, no `aria-labelledby`. The two are siblings with nothing connecting them.

- **Measured**: axe-core 4.13.0 on `file-input-no-labels.html` → rule `label`, `impact: "critical"`, `node_count: 1`, `sample_selectors: ["input"]`, tags `wcag2a`, `wcag412`.
- **Measured**: `trace.json` step_0001 → `active_element_selector: "#root > div > input"`, `ax_name_role_state: {name: "Choose File", role: "button"}`. Per KAT calibration rule 2, a non-null name here is the **user agent's** intrinsic name, not evidence of a label. Step_0003 (`Shift+Tab` back) reports the identical name.
- **Measured**: `trace.json` step_0001 `sr_announcement.focus_announcement: "document"`, `new_phrases: ["document"]`; step_0003 `focus_announcement: null`, `new_phrases: []`. On neither arrival at the control did the author's text "Upload file" enter the announcement stream.
- **Measured**: `sr-census.json` index 2 → `"Upload file"` sits in the reading order as free-floating text with `tag: null, selector: null` — present on the page, attached to nothing.
- **Impacted**: screen reader users (primary); voice-control users (secondary — "click Upload file" will not match a control named "Choose File"); cognitive users on a multi-control form.
- **Citation**: WCAG 2.2 **1.3.1 Info and Relationships**, **4.1.2 Name, Role, Value**, **3.3.2 Labels or Instructions**.
- **What the user actually experiences**: tabbing to the control announces "Choose File, button" — the same string this page would produce for a résumé upload, an avatar upload, or a tax return upload. On a page with two file inputs the user has no way to tell them apart. The word "Upload" is never spoken in connection with the control.

**Fix** — a native `<label>` pairing, not an ARIA patch:

```jsx
<label htmlFor="file-upload">Upload file</label>
<input
  id="file-upload"
  type="file"
  onChange={handleFileChange}
  accept=".pdf,.doc,.docx"
/>
```

**Do not fix this with `aria-label="Upload file"` on the input.** Per the prior-audit anti-pattern on ARIA-without-visible-label, the visible label must exist *alongside* programmatic association — here the visible text already exists, so `aria-label` would leave line 19 orphaned, duplicate the name, and break voice-control matching if the two strings ever drift. `<label htmlFor>` is the only correct fix; `aria-labelledby` pointing at an `id` on line 19 is an acceptable second choice if the layout forbids a `<label>`.

```
### A11y Evidence Finding
finding_id: file-input-no-author-supplied-accessible-name
fingerprint: f11ea7c0
source: axe-core 4.13.0 rule `label` (010-127-0-0-1-8777-file-input-no-labels-html.json); keyboard-a11y-tester driven trace step_0001/step_0003 (file-input-no-labels-kat-driven/trace.json)
wcag_or_apg: WCAG 2.2 1.3.1, 4.1.2, 3.3.2
section_508_fpc_context: not in scope — this is a component review with no declared 508 scope. Context only: axe tags this rule `section508` / `section508.22.n`, and it is a WCAG 2.0 Level A failure, so it would sit inside the Revised Section 508 web floor if 508 scope were later declared.
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, keyboard=LOW, low-vision=LOW, cognitive=MEDIUM
evidence: BuggyFileInput.jsx:19 `<div>Upload file</div>`; BuggyFileInput.jsx:20-24 `<input type="file">` with no id/label/aria-label; axe `label` impact=critical node_count=1 selector=`input`; trace step_0001 ax_name_role_state.name="Choose File" role="button"
reproduction_steps: 1) Serve the fixture at http://127.0.0.1:8777/file-input-no-labels.html. 2) Run axe-core 4.13.0 via Playwright at 1280x800 — observe the `label` violation on selector `input`. 3) Run keyboard-a11y-tester in driven-live mode with the keyboard + screen-reader personas and send one `Tab` — observe active element `#root > div > input` with accessible name "Choose File".
expected_behavior: On focus, assistive technology announces the author's label ("Upload file") as the control's accessible name, and voice control can target the control by that visible text.
actual_behavior: The accessible name is the user-agent-intrinsic "Choose File". The author's text "Upload file" exists only as an unassociated text node (sr-census index 2) and is never announced with the control.
trend: new
```

---

**CRITICAL-2 — The validation error has no programmatic existence: not announced, not associated, and `aria-invalid` is never set. Validation fails silently.**

`BuggyFileInput.jsx:9-10` sets the error when `file.size > 5000000`. `BuggyFileInput.jsx:25-29` renders `<div className="error-message">{error}</div>` — no `role="alert"`, no `aria-live`, no `id`. `BuggyFileInput.jsx:20-24` shows the input carries no `aria-describedby` and no `aria-invalid`. The string `aria-` does not appear anywhere in this component.

- **Measured**: `sr-census.json` → `"declared_live_regions": []`. This is a *declared* field, not an inference: the page declares zero live regions. Structural absence in source plus declared absence in the census is exactly the two-part evidence shape that makes silence defect evidence rather than an inconclusive log.
- **Measured**: `sr-census.json` → `"declared_broken_aria_refs": []`. No ARIA references exist to be broken — consistent with a component that authors none.
- **Measured**: `sr-census.json` index 3 → `"File too large"` is present in the reading order. The error is in the tree; it is simply never announced and never tied to the field.
- **Measured**: `trace.json` step_0001 and step_0003 → `states: {invalid: "false", ...}` on the input. Consistent with `aria-invalid` never being authored. (Capture caveat: I cannot prove the error was displayed at trace time, so this corroborates the source reading rather than standing alone.)
- **Measured**: `live_announcements: []` at all three trace steps.
- **Impacted**: screen reader users (complete loss of the failure signal); cognitive users (no persistent, associated explanation at the point of failure).
- **Citation**: WCAG 2.2 **3.3.1 Error Identification**, **4.1.3 Status Messages**, **1.3.1 Info and Relationships**.
- **What the user actually experiences**: the user picks a 6 MB PDF. The picker closes. Nothing is announced. The control still reads out the chosen filename. The user moves on and submits the form believing the file is attached — it is not, because `setSelectedFile` never ran (line 12 is in the `else` branch only). The failure surfaces days later, if at all. This is the severity scale's own CRITICAL exemplar: *form validation fails silently.*

**Fix** — three coordinated changes, all required:

```jsx
<label htmlFor="file-upload">Upload file</label>
<p id="file-hint">PDF, DOC, or DOCX. Maximum size 4.7 MB.</p>
<input
  id="file-upload"
  type="file"
  accept=".pdf,.doc,.docx"
  aria-describedby={error ? "file-hint file-error" : "file-hint"}
  aria-invalid={error ? "true" : undefined}
  onChange={handleFileChange}
/>
{error && (
  <div id="file-error" className="error-message">
    <span aria-hidden="true">⚠ </span>{error}
  </div>
)}
```

plus a persistent, always-mounted announcement container so the message is announced when it *changes*, not when it mounts:

```jsx
<div role="alert" aria-live="assertive" className="visually-hidden">
  {error}
</div>
```

**Scope caveat on the alert region (prior-audit anti-pattern 1, Broadcast vs. Association)**: one alert region is correct *here* because this is a single-field component. If `BuggyFileInput` is ever rendered in a loop — a multi-attachment form, a table of upload rows — a per-instance `role="alert"` becomes exactly the broadcast anti-pattern that audit rejected. In that case, hoist one region to the form and keep per-field feedback on `aria-describedby`. Decide this before the component is reused, not after.

```
### A11y Evidence Finding
finding_id: file-upload-validation-error-has-no-programmatic-surface
fingerprint: e77a05b2
source: BuggyFileInput.jsx:9-10, 20-24, 25-29; keyboard-a11y-tester sr-census (file-input-no-labels-kat-census/sr-census.json); keyboard-a11y-tester driven trace step_0001/step_0003
wcag_or_apg: WCAG 2.2 3.3.1, 4.1.3, 1.3.1
section_508_fpc_context: not in scope — no 508 scope declared for this component review. Context only: 3.3.1 and 1.3.1 are WCAG 2.0 Level A and would sit inside the federal web floor; 4.1.3 is WCAG 2.1-only and must not be labeled a Section 508 failure.
severity: CRITICAL
perspective_alarms: screen-reader=HIGH, cognitive=HIGH, keyboard=LOW, low-vision=MEDIUM
evidence: BuggyFileInput.jsx:26 `<div className="error-message">` with no role/aria-live/id; BuggyFileInput.jsx:20-24 input with no aria-describedby/aria-invalid; sr-census `declared_live_regions: []` and `declared_broken_aria_refs: []`; sr-census index 3 spoken_phrase "File too large"; trace step_0001/step_0003 `states.invalid: "false"`; live_announcements empty at all 3 steps
reproduction_steps: 1) Serve the fixture and start a screen reader. 2) Select a file larger than 5,000,000 bytes. 3) Listen — no announcement occurs. 4) Assert on the page: no element carries role="alert" or aria-live (sr-census `declared_live_regions` is empty). 5) Inspect the input's accessibility node — no aria-describedby reference and invalid=false.
expected_behavior: On rejection the message is announced without the user moving focus; the input reports invalid; and moving to the input reads the error as its description.
actual_behavior: The message renders as static text reachable only by exploration (sr-census index 3). No live region is declared, no describedby association exists, and the input continues to report invalid=false. The rejected file is discarded from React state while the control still displays its filename.
trend: new
```

---

### Major Findings (significantly degrades experience)

**MAJOR-1 — Rejected files leave the UI and the app in contradictory states, and the cancel path silently clears the error.**

`BuggyFileInput.jsx:9-14`. On the reject branch only `setError` runs; `setSelectedFile` (line 12) never fires. But the browser has *already* committed the selection to the native control — trace step_0001 shows `text: "C:\fakepath\quarterly-report.pdf"` on the input. So the interface asserts "quarterly-report.pdf is chosen" while the application holds nothing.

The `else` branch has a second defect: it also runs when `file` is `undefined` — the user opened the picker and cancelled. That path sets `selectedFile` to `undefined` **and** clears any existing error (line 13), so a previously-displayed error vanishes with no announcement of its removal and no announcement of its arrival (CRITICAL-2). Prior-audit anti-pattern 4 (else-branch coverage) is the general form of this: the state logic was written for the happy path and the reject path, and the cancel path fell through the middle.

- **Impacted**: all users; screen reader and cognitive users disproportionately, because for them the displayed filename is the *only* remaining signal and it is wrong.
- **Citation**: WCAG 2.2 **4.1.2 Name, Role, Value** (the control's value no longer reflects application state), **3.3.1 Error Identification**.
- **Fix**: on rejection, clear the native control (`e.target.value = ''`) so the displayed value matches application state, and guard the cancel path explicitly:

```jsx
const handleFileChange = (e) => {
  const file = e.target.files[0];
  if (!file) return;                         // cancelled — change nothing
  if (file.size > MAX_UPLOAD_BYTES) {
    e.target.value = '';                     // don't display a file we discarded
    setSelectedFile(null);
    setError(`That file is ${formatSize(file.size)}. The maximum is ${formatSize(MAX_UPLOAD_BYTES)}. Choose a smaller file.`);
    return;
  }
  setSelectedFile(file);
  setError(null);
};
```

`5000000` on line 9 is also a hardcoded magic number; hoist it to a named constant so the limit stated in the hint text and the limit enforced in code cannot drift apart — a drift that would produce an error message contradicting the instructions, which is a worse cognitive-accessibility failure than having neither.

---

**MAJOR-2 — The upload constraints are never communicated, and the error message names no remedy.**

`BuggyFileInput.jsx:23` carries `accept=".pdf,.doc,.docx"`. That attribute is a *picker filter*: it is not exposed to assistive technology as a description, it is not enforced (most OS pickers offer "All Files"), and it appears nowhere in the page's accessible text. The 5,000,000-byte limit on line 9 is stated to the user **nowhere at all** — not before selection, not in the failure message.

- **Measured**: `sr-census.json` has exactly three entries — `"document"`, `"Upload file"`, `"File too large"`, with `truncated: false`. The complete accessible text of this page is two strings. **No instruction of any kind exists**, and this is measured, not inferred.
- The error text "File too large" (line 10) states that a rule was broken without stating the rule or the remedy. The threshold is genuinely unguessable: 5,000,000 bytes is 4.77 MiB, so a user who correctly guesses "5 MB" and trims to 4.9 MiB as reported by their OS still fails.
- Because `accept` is unenforced and the code validates size but never type, a user who picks a `.exe` through "All Files" takes the `else` branch — the component reports success for a file it should have rejected, silently. I am scoping that as an accessibility finding only insofar as the type constraint is communicated exclusively through a mechanism invisible to AT and then not enforced; the general input-validation engineering is out of this review's scope.
- **Impacted**: cognitive accessibility (primary), screen reader users, anyone on a metered or slow connection who uploads repeatedly on trial and error.
- **Citation**: WCAG 2.2 **3.3.2 Labels or Instructions**, **3.3.3 Error Suggestion**.
- **Fix**: render a persistent hint associated via `aria-describedby` (shown in the CRITICAL-2 fix), state both constraints in it, validate type as well as size, and rewrite the message to name the actual and permitted values and the corrective action — as in the MAJOR-1 snippet.

---

### Minor Findings (friction, workaround exists)

**MINOR-1 — No confirmation that an accepted file was accepted.** `selectedFile` (lines 4, 12) is written and never read; the component renders no success state. There is no `role="status"` announcement and no visible confirmation beyond whatever the native control shows. *Downgraded from MAJOR — see the Realist Check for the mitigation and its limits.* Fix: render the accepted filename and size into a `role="status"` region, which also gives sighted users the confirmation they currently lack.

**MINOR-2 — `.error-message` is a bare `<div>` with no non-color affordance in the markup.** Line 26. The CSS is not in the evidence pack, so I cannot confirm this resolves to color-only signalling, but the markup carries no icon, no prefix word, and no structural cue. Fix: add an `aria-hidden="true"` icon or the literal word "Error:" inside the message (WCAG **1.4.1 Use of Color**). Marked **Needs user verification**: open the stylesheet and check whether `.error-message` differs from adjacent text by more than color.

---

### Enhancements (best practice not met, no access barrier)

- **Wrap the group in a `<fieldset>`/`<legend>` or a labelled region when this component joins a real form.** Standing alone, the single control needs nothing; inside a multi-field form, "Upload file" as an orphan `<div>` will read as stray prose.
- **Target size, with the exception noted.** The trace measures the control's `bounding_box` as `{width: 253, height: 21}` — 21 CSS px is under the WCAG 2.2 **2.5.8 Target Size (Minimum)** 24 px threshold. I am **not** filing this as a finding: the target is a user-agent-rendered control that the author does not style (the input carries no class; only the wrapper does), which is the UA-control exception. This is corroborated negatively — axe's `target-size` rule fired on two *sibling* pages in this same batch (`accordion-no-region-role.html`, `image-carousel-no-region.html`), proving the rule was live and capable of firing, and it did not fire here. **Forward-looking**: the near-universal next step for upload UIs is replacing the native control with a styled button plus a visually-hidden input. The moment that happens the UA exception is gone and the 24×24 minimum applies. Size it then.
- **`autocomplete` is not applicable** to `type="file"` (WCAG 1.3.5 covers personal-data fields). Checked and dismissed — noting it so its absence is not read as an oversight.

---

## What's Missing (gap analysis)

| Absent | Why it matters | Citation |
|---|---|---|
| Programmatic label association | The control has no author-supplied name (CRITICAL-1) | 1.3.1, 4.1.2 |
| Any live region on the page (`declared_live_regions: []`) | Nothing this component ever renders can be announced | 4.1.3 |
| `aria-describedby` on the input | Error and hint cannot be read as the field's description | 1.3.1 |
| `aria-invalid` toggling | The field never reports its own error state; trace shows `invalid: "false"` | 4.1.2 |
| Any statement of the size or type constraint | Users cannot succeed except by trial and error | 3.3.2 |
| A remedy in the error text | "File too large" names no limit and no next step | 3.3.3 |
| Success/confirmation state | `selectedFile` is written and never rendered | 4.1.3 |
| Cancel-path handling | Falls into `else`, silently clearing state and errors | 3.3.1 |
| Type validation | `accept` is a picker filter, not enforcement; bypass produces silent success | 3.3.1 |
| Native control reset on rejection | UI displays a filename the app discarded | 4.1.2 |
| A stated maximum in machine-readable form | Nothing lets a client or server share one source of truth for the limit | — |

**Not missing, verified present**: native `<input type="file">` rather than a div-with-role construction (the Native-HTML-first rule is satisfied — this component earns credit here, and it is the reason the keyboard layer measures clean); a visible label *string*, even though it is unassociated; `accept` narrowing the picker for mouse users.

---

## Test-Harness Artifacts — Explicitly NOT Component Findings

axe reported three additional violations on `file-input-no-labels.html`, all tagged `best-practice`, none tagged `wcag*`:

- `landmark-one-main` (moderate, selector `html`)
- `page-has-heading-one` (moderate, selector `html`)
- `region` (moderate, selector `#root`)

Corroborated at focus time by the trace: step_0001 and step_0003 both report `region: {landmark: null, heading: null}` — a screen reader user landing on this control gets no positional context.

**These are page-shell properties of the fixture harness, not defects in `BuggyFileInput`.** The component under review renders `<div className="file-upload">`; it does not own the document's `<main>`, its `<h1>`, or the `#root` wrapper. Filing them against this component would be the page-shell over-flagging failure mode. They belong to whichever page eventually hosts the component, and they should be checked *there*. Recorded as context, scored as nothing.

---

## Multi-Perspective Review

### Perspective Alarm Levels

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|----------------|
| Screen reader | **HIGH** | Control has no author-supplied name (axe `label` critical; trace name "Choose File"); zero declared live regions; error unassociated and unannounced |
| Keyboard-only | **LOW** | Measured clean — single tab stop, no trap, focus visible, 2.4.13 pass. Residual: picker activation unmeasured (see below) |
| Low vision | **MEDIUM** | `.error-message` CSS absent from pack; color-only error signalling unverifiable; forced-colors behavior unknown |
| Cognitive | **HIGH** | Unstated 4.77 MiB limit; error names no remedy; no confirmation; silent state clearing on cancel |
| Vestibular & motion | **LOW** | No animation, transition, parallax, or autoplay anywhere in source |
| Auditory access | **LOW** | No `<video>`, `<audio>`, or auditory alert in source |
| Environmental contrast | **MEDIUM** | Same CSS gap as Low vision; axe reported no `color-contrast` violation *and* `incomplete: []` for this page, so the text that exists resolved and passed — but the error styling is not covered by that scan |

**Escalate to `/perspective-audit`**: Screen reader (HIGH) and Cognitive (HIGH). Low vision and Environmental contrast (MEDIUM) should be included in that audit once the stylesheet is supplied — auditing them now would produce speculation, not findings.

### Notes

**Screen reader user.** Tab lands on a control announced as "Choose File, button" — the user agent's string, identical to what any other upload on any other page would say. The word "Upload" never reaches them in connection with the control. They choose a file. Nothing is announced (`declared_live_regions: []`). If it was rejected they are not told; the control still reads back a filename; the application has discarded the file. The rejection message *does* exist in the reading order (census index 3) — they could find it by browsing forward. But nothing has given them any reason to browse forward, because from their side the interaction succeeded. That gap — between "present in the tree" and "the user has a reason to look" — is the whole failure, and it is the part axe cannot see: axe caught the missing label and reported `incomplete: []` for everything else on this page.

**Keyboard-only user.** Measurably fine, and worth saying plainly. `Tab` reaches the input (step_0001, `focus_moved: true`), `Tab` again exits to `body` (step_0002), `Shift+Tab` returns (step_0003) — no trap (**2.1.2** satisfied). Focus is visible: `outline_style: "auto"`, `outline_color: rgb(0, 95, 204)`, `focus_visible.visible: true`, `indicator: "outline"` (**2.4.7** satisfied). Focus appearance clears the stricter bar too: `changed_area: 1107` against `ref_area_2px_perimeter: 1096` (`area_pass: true`) at `contrast: 4.86` (`contrast_pass: true`, `aaa_pass: true`) — **2.4.13 Focus Appearance** passes on measurement. I predicted a focus problem here and the evidence refutes me. **Honest residual**: no keystroke in the trace activates the picker, so keyboard *operability* of the control rests on native user-agent behavior, not on this measurement. That claim is sound but it is unmeasured, and the driven session that was supposed to measure it did not.

**Low vision user (200% zoom, high contrast, magnifier).** Cannot be closed out. axe found no contrast violations and no incompletes for this page, so the text present resolved and passed — but the error state's styling is not in the pack, and `.error-message` in the markup carries no non-color cue. At 200% zoom the error appears below the control, outside a magnifier viewport centered on the input; with no announcement (CRITICAL-2) a magnifier user has the same discovery problem a screen reader user has. In forced-colors mode a color-only error would disappear entirely. Supply the CSS and re-audit.

**Cognitive accessibility.** The weakest perspective after screen reader, and the one that fails for *sighted* users too. The user is told what is allowed only through a picker filter they may never notice, is never told the size limit, fails, is told "File too large" with no number and no instruction, and is left looking at the filename of the file that was just rejected. If they cancel the picker on the next attempt, the error silently disappears and they are back to a blank slate with no memory of what went wrong. Every one of those is fixable with text.

---

## Phase 8 — Realist Check (Severity Calibration)

**CRITICAL-1 (no accessible name).** Worst realistic case: on a single-control page a screen reader user infers the purpose from surrounding text and proceeds — friction, not blockage. On a form with two or more file inputs, they cannot tell them apart and will attach the wrong document. Impacted: screen reader + voice control. Detection: fast — axe catches it in CI (impact `critical`), which is how it was caught here. Proportional? **Yes, held at CRITICAL.** The downgrade rule for "easy workaround" does not apply: the workaround depends on page context the component cannot guarantee, and this is total loss of the control's identity, not degraded quality. axe rating it `critical` independently corroborates.

**CRITICAL-2 (silent validation failure).** Worst realistic case: the user submits a form believing a required document is attached when it is not, and discovers the failure through a rejected application, a missed deadline, or nothing at all. Impacted: screen reader (total) and cognitive (severe). Detection: **never** — no automated rule fires (axe reported `incomplete: []` for this page beyond the label rule), no test asserts it, and the user cannot report a failure they were not told about. Proportional? **Yes, held at CRITICAL.** The severity scale names "form validation fails silently" as a CRITICAL exemplar, and the no-downgrade rule for complete access loss applies squarely.

**MAJOR-1 (contradictory state / cancel path).** Worst realistic case: a user re-selects the same file repeatedly because the UI shows it as chosen. Impacted: all, worst for screen reader and cognitive. Detection: days — likely surfaces as a "my upload doesn't work" support ticket. Proportional? **Yes, held at MAJOR.** It degrades rather than blocks, and once CRITICAL-2 is fixed the user at least knows something failed.

**MAJOR-2 (no instructions / no remedy).** Worst realistic case: repeated failed attempts with no path to success; a cognitively-impaired user abandons the task. Impacted: cognitive primarily, all users secondarily. Detection: days to never. I considered downgrading to MINOR on the grounds that trial and error is a workaround. **Rejected.** The 4.77 MiB threshold is not reachable by reasonable guessing (a user trimming to "under 5 MB" as their OS reports it still fails), the type constraint is invisible *and* unenforced, and 3.3.3 requires the error to suggest a correction — this one names no value and no action. **Held at MAJOR.** The 3.3.2 half alone would be MINOR; the 3.3.3 half carries the rating.

**MINOR-1 (no success confirmation) — downgraded from MAJOR.** *Mitigated by*: the native control displays the chosen filename adjacent to the button (trace step_0001 `text: "C:\fakepath\quarterly-report.pdf"`), and most screen readers surface a file input's value on focus, so a user who returns to the control can usually confirm the selection. **The limits of that mitigation, stated honestly**: this evidence does not prove the announcement. The captured `ax_name_role_state.name` is "Choose File" with no `value` in `states`, so the filename's presence in the *announcement* is inferred from general screen reader behavior, not measured here. Treat the mitigation as likely, not proven — and note that the recommended fix removes the dependence on it entirely.

---

## Phase 9 — Self-Audit

| Finding | Confidence | Refutable by developer context? | Gap or preference? |
|---|---|---|---|
| CRITICAL-1 | **HIGH** | No — two independent measured artifacts plus source | GAP |
| CRITICAL-2 | **HIGH** | No — source shows zero ARIA; census declares zero live regions | GAP |
| MAJOR-1 | **HIGH** | No — pure control-flow reading of lines 9-14 | GAP |
| MAJOR-2 | **HIGH** | Partially — a wrapping form might supply instructions the component doesn't. But the census proves the *page as tested* has no instructions, and a component should not depend on an unstated host contract. Held. | GAP |
| MINOR-1 | MEDIUM | Yes — the design may deliberately rely on the native control's own display. Downgraded accordingly. | GAP (minor) |
| MINOR-2 | **LOW on the color-only claim** | Yes — the CSS is not in the pack | GAP if confirmed; marked *Needs user verification* rather than suppressed |

Moved to Open Questions: the target-size measurement, the census/trace discrepancy over the input's reading-order entry, and the reduced-motion question.

Calibration statement, since a clean bill carries signal: **the keyboard layer of this component is genuinely sound and I am saying so** — native element, single tab stop, no trap, focus indicator passing both 2.4.7 and the stricter 2.4.13 on measurement. The choice of `<input type="file">` over a div-with-role construction is correct and is exactly why the keyboard evidence is clean. Nothing about the remediation requires changing that.

---

## Phase 10 — Synthesis

Five of seven predictions hit. The two that did not are the informative ones. I predicted a focus-management defect and the trace refutes it — the component's keyboard behavior is measurably fine because it uses a native control, and manufacturing a focus finding here would have been the failure mode this protocol exists to prevent. I also predicted the error would be "invisible to assistive technology"; the census shows it is in the reading order (index 3). The truth is more precise and more damaging: the error is *reachable but unannounced*. Reachable-but-unannounced is worse than absent, because the user has no trigger to go looking, and it is the exact class of defect that survives an axe run — this page's scan reported `incomplete: []`, meaning axe was confident about everything it checked and simply does not check this.

The surprise worth carrying forward is in the evidence, not the component: the driven trace declares the goal *"choose a file and review any feedback the page gives"* and then sends three navigation keystrokes and never selects a file. The artifact that looks like the strongest evidence for the error path covers none of it. The error-path findings here are source-derived with census corroboration, and any consumer of this review should know that.

---

## Verdict Justification

**REJECT.** Two CRITICAL findings, each independently sufficient. The control has no author-supplied accessible name — a WCAG 2.0 Level A failure that axe rates `critical` impact. Validation fails silently for every assistive technology user, which is the severity scale's own named CRITICAL example, and it is the failure mode with no detection path: no automated rule catches it, and the user cannot report a rejection they were never told about.

Severity was recalibrated once, downward, with a stated and limited mitigation (MINOR-1). Nothing was inflated: three axe best-practice violations on this page were examined and explicitly excluded as harness artifacts; a sub-24px target measurement was examined and excluded under the UA-control exception with negative cross-evidence from two sibling scans; a census `role` field echoing spoken text was identified as a serialization quirk rather than filed as an invalid-role violation; and 18 of the 21 supplied artifacts describe other URLs and contributed nothing to any finding.

**To reach ACCEPT-WITH-RESERVATIONS**, all of the following:
1. `<label htmlFor>` + matching `id` (CRITICAL-1).
2. A persistent, always-mounted `role="alert"` container, `aria-describedby` wiring the hint and error to the input, and `aria-invalid` toggling with the error state (CRITICAL-2).
3. Constraints stated in visible, associated hint text with a real number, and an error message naming the actual size, the limit, and the corrective action (MAJOR-2).
4. Reject path clears the native control; cancel path guarded with an early return (MAJOR-1).

**To reach ACCEPT**, add a `role="status"` confirmation of accepted files (MINOR-1) and a non-color cue in the error (MINOR-2, once the CSS confirms it is needed).

**Verification contract for the fix** — per the prior-audit rule that any fix adding `aria-*` requires DOM inspection, not unit tests. Re-run the same three artifacts against the same URL and assert:
- axe-core 4.13.0: `label` violation count **0** (the three best-practice rules may legitimately persist — they are the harness).
- KAT driven trace: at the input's step, `ax_name_role_state.name == "Upload file"` (not `"Choose File"`), and with an error present `states.invalid == "true"`.
- KAT census: `declared_live_regions` **non-empty**, and `declared_broken_aria_refs` still `[]` — the new `aria-describedby` must resolve to real ids, and this field is what proves it.
- Extend the driven session so it actually executes the declared goal: activate the picker, complete a rejecting selection, and capture `live_announcements` at that step. Without that step, the error-path fix is unverified no matter what the source says.

---

## Open Questions (unscored)

1. **Target size after restyling.** The measured 21 px height is under the 2.5.8 minimum but exempt as a UA-rendered control (corroborated: axe's `target-size` fired on two sibling pages in this batch and not on this one). If the roadmap includes a styled upload button — the usual next step — the exception disappears. Is that planned?
2. **Census/trace discrepancy.** The sr-census lists no entry for the input, while the trace proves it is in the AX tree as `role: "button"`, name `"Choose File"`. Most consistent with the census enumerating text content only. Not filed, but worth a note to the KAT pin owner if the census is meant to be a complete reading-order enumeration.
3. **Component context.** Is `BuggyFileInput` ever rendered more than once on a page? This decides whether one `role="alert"` per instance is correct or is the broadcast anti-pattern. Answer before shipping the fix.
4. **`.error-message` styling.** Colour-only, or does it carry weight/icon/border? Determines whether MINOR-2 is real (1.4.1) and whether it survives forced-colors mode.
5. **Server-side enforcement.** Client-side size and type checks are advisory. If the server enforces a different limit, the hint text will lie to users — a cognitive-accessibility failure worse than having no hint. Is there one source of truth for `MAX_UPLOAD_BYTES`?
6. **Reduced motion.** No animation exists in this source, but if `.file-upload` or `.error-message` animates the error in via CSS, `prefers-reduced-motion` needs checking (2.3.3). Unanswerable without the stylesheet.
7. **Multi-file support.** `multiple` is absent. If it is added later, every finding here compounds — per-file errors would need a fundamentally different association strategy than a single `aria-describedby`.
