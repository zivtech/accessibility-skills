# Accessibility Design Critic Review: `BuggyFileInput`

**VERDICT: REVISE**

**Overall Assessment**: `BuggyFileInput` makes the right foundational choice — a native `<input type="file">` rather than an ARIA-faked substitute — so there is no "bad semantics masked by ARIA" anti-pattern here. But the component supplies zero programmatic association layer on top of that native element: no label, no error-to-input association, no invalid-state signaling, and no live-region announcement for the one dynamic state (validation failure) it produces. A screen reader user's only information about this control is the browser's generic "Choose File, button" caption; if they select an oversized file, the rejection is silent. These are additive, well-understood fixes rather than an architectural rework, which is why the verdict is REVISE rather than REJECT.

**Evidence Provenance Note**: This review had direct, first-hand access to the component source (reproduced in the review material) — all source-cited findings below are independently verified against that code, with line numbers as they appear in the material provided. The review material also included a CURATED evidence digest describing an axe-core scan, a keyboard-a11y-tester driven trace, and a keyboard-a11y-tester screen-reader reading-order census. Per this protocol's Phase 0 guidance, a digest is "detector output, one tier BELOW the artifact it cites... a finding that cannot be traced to a re-fetched handle is labeled digest-only." This review had no ability to re-fetch the underlying axe JSON / trace.json / sr-census.json files, so every claim sourced from the digest is explicitly marked **digest-only** below and treated as corroborating context rather than independently re-verified hard evidence. Findings fully supported by the source code alone are marked **source-verified** and stand independent of the digest.

Consistent with the digest's own "Not claimed" disclosures: no batch-crawl findings artifact was supplied (only a driven trace, the stronger evidence tier for interaction claims); the keyboard-a11y-tester attribution for `trace.json`/`sr-census.json` rests on directory naming, not an in-file tool/version key; and no WCAG SC-number mapping was offered by the digest itself — SC numbers cited below are this review's own standard decoding of axe's raw tag tokens (e.g., tag `wcag412` → SC 4.1.2), not something the tooling itself asserted.

**Pre-commitment Predictions (Phase 1)**: Before auditing the code in detail, the predicted failure modes for a "file input with client-side validation" component were: (1) missing/incomplete label, (2) error not associated with the field via `aria-describedby`, (3) no `aria-invalid` toggling, (4) error not announced via `aria-live`, (5) no accessible disclosure of file-type/size constraints before failure. All five were confirmed directly in source. Two things were not predictable from source alone and came from the evidence digest (digest-only): keyboard reachability and focus-indicator quality both measure as fully passing (Tab/Shift+Tab both reach and leave the input correctly; focus-ring contrast 4.86, comfortably above the 3:1 minimum) — a genuine positive the investigation would otherwise have had to leave as "unverifiable from source." No prediction was falsified; the investigation did not surface a different failure class than expected.

## Semantic HTML Audit (Phase 2)

The component root is a plain `<div className="file-upload">` (line 25) — an acceptable generic container. Inside it:

- Line 26: `<div>Upload file</div>` — reads visually as a label but is not a `<label>` element, has no `htmlFor`/`for`, no `id` to be referenced by, and does not wrap the input. It is inert text as far as the accessibility tree's name computation for the input is concerned.
- Lines 27–31: `<input type="file" onChange={handleFileChange} accept=".pdf,.doc,.docx" />` — correct native element for this job. No ARIA role is used to fake this control, so the protocol's core "native HTML first" anti-pattern (div/span with `role="button"` replacing a real `<button>`) does not apply here. The defect class in this component is *missing association*, not *masked semantics*.
- Lines 32–36: `<div className="error-message">{error}</div>` — plain text container, no `role`, no `aria-live`, no `id`.
- No `<label>`, `<form>`, `<fieldset>`, or heading element appears anywhere in the component. No `id` attribute is set on the input or the error container, which is the root enabler of every association gap below — without an `id`, `aria-describedby`/`htmlFor` cannot be wired even if someone tried.

Checked and not applicable: no tables (row-header / `role="presentation"` checks N/A), no images (alt-text checks N/A), no icon fonts, no CSS pseudo-element content, no lists, no repeating templates. None of the "Known False Positives to Watch For" patterns (portal content, spread-prop ARIA, gradient backgrounds, `anchor-is-valid`) apply to this component. Of the nine third-party-audit anti-patterns, only #9 (DOM-verification of any added `aria-*` attribute) is forward-relevant here — it's called out explicitly in the fixes below.

## ARIA Pattern Compliance Audit (Phase 3)

No WAI-ARIA composite widget pattern applies here — this is a native form control, not a custom tabs/menu/listbox/dialog. The correct pattern is simply the native HTML forms labeling model (`<label for>` + `aria-describedby` for hints/errors), and no ARIA `role` attribute is used anywhere in the source (confirmed by direct read of lines 8–42).

One calibration point worth stating precisely: the evidence digest (digest-only; `trace.json` steps `step_0001`/`step_0003`, jq path `.steps[0].ax_name_role_state` / `.steps[2].ax_name_role_state`) reports the input's computed accessibility-tree name as `"Choose File"` with role `"button"`. This is the browser's User-Agent-generated caption for `<input type="file">` — a platform default, not something this component's code produced. It would be a mistake to read "name is present" as evidence the labeling problem is solved; this protocol's own Phase 0 calibration rule names this exact trap ("a 'Choose File' file input can still be missing its label"). The AX name tells a screen reader user *that a file chooser exists*, not *what it's for* or *what files are acceptable* — that context is exactly what's missing. Axe-core's independent `label` rule (digest-only; see Critical Finding 1) fires precisely because it checks for a programmatic label association, which this generic button caption does not provide.

No `aria-invalid`, no `aria-describedby`, no `aria-required` appear anywhere in source — confirmed directly, not merely inferred from the digest's silence.

## Focus Management Review (Phase 4)

Only one interactive element exists in this component, so there is no composite-widget tab order, no modal focus trap, and no focus-restoration scenario to evaluate. What can be evaluated:

- Digest-only (`trace.json` `step_0001`): Tab reaches the input (`#root > div > input`, `dom_order_index 12`), `focus_moved: true`, `focus_visible: {visible:true, indicator:"outline", contrast:4.86, contrast_pass:true, aaa_pass:true, area_pass:true}`. The native default focus ring is intact and passes contrast comfortably — nothing in the component suppresses it (no CSS is present in the source at all).
- Digest-only (`trace.json` `step_0003`): `Shift+Tab` returns focus to the same input with AX values identical to `step_0001` — no keyboard trap; bidirectional Tab movement works.
- Digest-only, unresolved (`trace.json` `step_0002`): the second `Tab` moves the active element to `body` (`ax_name_role_state: {name:null, role:"none"}`, `dom_order_index: -1`). The digest explicitly declines to characterize this as a defect, and this review cannot inspect the full page's DOM or focusable-element count beyond this 3-step, goal-driven session (stated goal: "Choose a file to upload using only the keyboard and review any feedback the page gives"). Plausibly just "reached the end of a single-input test-harness page," which would be unremarkable. Logged as an Open Question rather than a finding, per this protocol's self-audit rule (LOW confidence → Open Questions).

Net: focus management for the component's one control is not where its accessibility problems live, and it's worth stating plainly rather than manufacturing a finding to fill the phase.

## State Communication Audit (Phase 5)

This is where the component's real defects concentrate.

- **Error state**: `error &&` conditionally renders the message div (lines 32–36, source-verified) with no `role="alert"`, no `aria-live`, no `aria-atomic`. Digest-only corroboration: the digest's "Absence claims" report zero live-region announcements anywhere in the evidence set (`.steps[].sr_announcement.live_announcements` → `[[],[],[]]`; sr-census `.declared_live_regions` → `[]`). A screen reader user not already focused on/near the error node when it appears receives no notification that their action failed.
- **Invalid state**: no `aria-invalid` attribute exists in source regardless of `error` state (source-verified). The digest's captured `states: {"invalid":"false", ...}` (digest-only) is consistent with this but uninformative on its own, since the 3-step trace never actually drove the error path — the source-level absence is the decisive evidence here, not the trace snapshot.
- **Error-to-field association**: no `id` on the error div, no `aria-describedby` on the input (source-verified) — even a properly-announced error would leave no persistent, re-discoverable association if the user tabs away and back.
- **Success/selection state**: `selectedFile` is set in React state (line 19) but nothing in the render output (lines 24–38, the component's full return statement) surfaces it — no "Selected: filename" text, for sighted or AT users alike. This is a plain gap-analysis catch independent of any evidence artifact.
- **Help/instructional text**: `accept=".pdf,.doc,.docx"` (line 30, source-verified) constrains the native file-picker dialog but is never surfaced as visible or associated instructional text, and the 5,000,000-byte size ceiling (line 16) is disclosed nowhere before a rejection occurs.

## Multi-Perspective Review (Phase 6)

| Perspective | Alarm Level | Trigger Signal |
|---|---|---|
| Screen reader | HIGH | Only interactive element has no application-supplied label (generic UA "Choose File" caption only); validation failure is entirely unannounced; no error/field association |
| Keyboard-only | LOW | Native control; Tab/Shift+Tab both confirmed working (digest-only); focus indicator passes contrast; no trap |
| Low vision | MEDIUM | No CSS supplied to verify text contrast, reflow, or 200% zoom behavior; only the focus-ring contrast (4.86) is in evidence, not label/error text contrast |
| Cognitive | MEDIUM | Error names the problem category but not the limit or a fix; no upfront disclosure of constraints; no success confirmation for anyone |
| Vestibular & motion | LOW | No animation, transition, or auto-playing content in this component |
| Auditory access | LOW | No audio/video content |
| Environmental contrast | MEDIUM | Text contrast for the label/error content is unmeasured in the supplied evidence; cannot confirm 1.4.3 pass/fail |

Screen reader is flagged HIGH and, per this protocol, should be escalated to `/perspective-audit` for deeper review.

**Screen reader user**: Hears "Choose File, button" on Tab-in — the browser's generic caption, not "Upload file," not the accepted formats, not the size limit. If they select an oversized file, nothing is announced; if they succeed, nothing confirms it either. They cannot distinguish "it worked" from "it silently failed" without independently re-discovering the visual error text.

**Keyboard-only user**: Fully operational as far as the evidence shows — reaches the control, activates it (native `Enter`/`Space` opens the OS picker by platform convention), can Tab away and back. Their disadvantage is informational, identical to the screen reader user's, not operational.

**Low vision user (200% zoom, high contrast)**: Cannot be assessed with confidence — no CSS was supplied in the review material, and the only contrast measurement available is for the focus ring, not for the "Upload file" or "File too large" text. Flagged as Open Question / needs measurement rather than scored pass or fail.

**Cognitive accessibility**: The error message states a category ("File too large") without a threshold or fix ("under 5MB"), which is real but modest friction — a workaround (trial and error) exists. The larger cognitive gap is asymmetric: neither success nor failure produces an application-level acknowledgment, so every user is left uncertain whether their action completed.

## Gap Analysis — What's Missing (Phase 7)

- No `<label>` (or `aria-labelledby`) associating "Upload file" with the input
- No `id` on the input or error container — the structural prerequisite for every association below
- No `aria-describedby` linking the error message to the input
- No `aria-invalid` toggling on validation failure
- No accessible, upfront disclosure of accepted file types or the size ceiling (the `accept` attribute alone constrains the OS picker; it is not perceivable instruction)
- No `role="alert"` / `aria-live` on the error container
- No confirmation, for any user, that a valid file was accepted
- No error-correction guidance (the actual 5MB threshold is never stated to the user)

## Realist Check & Self-Audit (Phases 8–9)

- **Finding 1 (missing label) — kept CRITICAL, not downgraded.** Realistic worst case on this single-field page: a screen reader user is not physically blocked from operating the control, so a case could be made for MAJOR. Rejected in favor of CRITICAL because (a) this protocol's Phase 5 instructs CRITICAL when "core state is not communicated to assistive technology," and an accessible *name* is squarely inside WCAG 4.1.2 Name, Role, Value's scope; (b) axe-core itself rates the `label` rule `impact: "critical"` (digest-only, but an industry-standard signal for exactly this defect class); and (c) the realistic deployment context for a reusable component is not "one isolated field on a bare page" — a real form with two or three of these components (resume upload, cover letter upload, photo upload) would make every instance announce identically, which is a genuine disambiguation failure, not a theoretical one.
- **Finding 2 (silent validation failure) — kept CRITICAL.** This is this protocol's own Severity Scale example verbatim: "Form validation fails silently." No credible downgrade path — the affected user group has no self-service workaround, and detection would only happen via a bug report, not a test.
- **Finding 4 (no success confirmation) — deliberately downgraded from what would otherwise be a CRITICAL "silent success" claim to MAJOR.** Mitigated by: browsers typically surface the chosen filename in the native file-input's own UI chrome (varies by browser/OS), a platform-level signal outside this component's control. The gap is specifically the *application's* missing acknowledgment, not a total absence of any signal.
- **Error-suggestion gap — kept MINOR, not raised to MAJOR.** A workaround (trial and error) exists, and the affected population, while not narrow, experiences friction rather than blocked access.
- **Three page-shell axe findings excluded from scoring.** `landmark-one-main`, `page-has-heading-one`, and `region` (all moderate impact, selectors `html`/`#root`, digest-only) describe the test-harness page shell — no `<main>`, no `<h1>`, content outside a landmark — not anything `BuggyFileInput`'s own code controls. Self-audit question "could the developer immediately refute this with context I might be missing?" — yes, with the page-shell context, since a real application embedding this component would supply those at the page-shell level, not inside the widget. Listed for transparency in Open Questions, not scored as component findings.
- **Trace anomalies (`step_0002` body-focus; the `step_0001`/`step_0003` `sr_announcement` divergence) — moved to Open Questions.** Both are LOW confidence: the digest itself declines to characterize either as a defect, and this review cannot inspect the raw trace file to investigate further.

## Findings

**Critical Findings** (blocks access):

1. **No accessible label for the file input beyond the browser's generic caption.** `BuggyFileInput`, lines 26–31: the text `<div>Upload file</div>` is not associated with the `<input type="file">` via `<label>`, `htmlFor`, or `aria-labelledby`. Source-verified. Corroborated digest-only by axe-core's `label` rule (impact: critical, tags include `wcag2a`, `wcag412`, selector `input`, node_count 1). Distinct from the AX tree's `"Choose File"` / `role: button` reading (digest-only, `trace.json` steps 1 and 3), which is the platform's generic caption for this element type, not an application-supplied label.
   - Confidence: HIGH
   - Why this matters: A screen reader user hears only "Choose File, button." Nothing tells them what they're choosing a file for, what formats are acceptable, or what the size limit is. In a real page with more than one file-upload control, every one of them would announce identically, with no way to tell them apart.
   - Fix: Wrap the text in a real `<label htmlFor="file-upload-input">Upload file</label>` and add `id="file-upload-input"` to the `<input>` (or use `aria-labelledby` if the visual design requires the text to live elsewhere in the DOM). Per this protocol's Anti-Pattern #9, verify in the rendered DOM (not just the JSX) that the `for`/`id` pair actually resolves.

2. **Validation failure is communicated only visually — no announcement, and no success confirmation to contradict it.** `BuggyFileInput`, lines 32–36: `{error && <div className="error-message">{error}</div>}` has no `role="alert"`, `role="status"`, or `aria-live`. Source-verified. Corroborated digest-only by the evidence pack's explicit absence claims: `.steps[].sr_announcement.live_announcements` → `[[],[],[]]` and sr-census `.declared_live_regions` → `[]`.
   - Confidence: HIGH
   - Why this matters: This is the Severity Scale's own textbook CRITICAL example — "form validation fails silently." A screen reader user who selects an oversized file gets no announcement of failure, and because the component also never confirms success (Major Finding 4), the realistic worst case is a user who believes their document was received when it was not.
   - Fix: Add `role="alert"` (or a dedicated `aria-live="assertive"` region reserved for this one error — one region per event type, not per field, per this protocol's Anti-Pattern #1, worth keeping in mind if this component is ever templated into a multi-file form) so the message is announced the moment it renders, independent of where focus currently is.

**Major Findings** (significantly degrades experience):

1. **Error message is not associated with the input via `aria-describedby`.** Lines 27–36, source-verified: no `id` exists on the error `<div>`, and the `<input>` carries no `aria-describedby`. Even with Critical Finding 2 fixed, a user tabbing back to the field later has no persistent, re-discoverable link telling them *this* field is the one with the problem.
   - Confidence: HIGH
   - Why this matters: Per WCAG 1.3.1 (Info and Relationships), the relationship between an error and its field must be programmatic, not merely sequential in the DOM.
   - Fix: Give the error container a stable `id` (e.g., `file-upload-error`) and set `aria-describedby="file-upload-error"` on the input, updated/removed in sync with the `error` state.

2. **No `aria-invalid` on the input at any point.** Lines 27–31, source-verified — no conditional `aria-invalid` attribute exists in the JSX regardless of `error`.
   - Confidence: HIGH
   - Why this matters: WCAG 4.1.2 (Name, Role, Value) requires validity state to be programmatically exposed. Without it, a screen reader user re-visiting the field after an error has no indication that it is currently in an invalid state.
   - Fix: Set `aria-invalid={!!error}` on the input, synchronized with the `error` state in `handleFileChange`.

3. **No accessible instructions for accepted file types or the size ceiling, disclosed only after failure.** Line 30 (`accept=".pdf,.doc,.docx"`) and line 16 (`file.size > 5000000`), source-verified: neither constraint is rendered as visible or programmatically associated help text anywhere in the component.
   - Confidence: HIGH — matches the fixture's own stated expected behavior ("Help text (file type restrictions) associated with input"); the gap is a clean absence, not a judgment call.
   - Why this matters: WCAG 3.3.2 (Labels or Instructions) calls for this context before the user acts, not after. The `accept` attribute filters the OS file-picker dialog but is not perceivable text for someone deciding what to do.
   - Fix: Add visible help text ("PDF, DOC, or DOCX, up to 5MB") near the input, with an `id`, referenced via `aria-describedby` (combine with the error id in a space-separated list when both are present).

4. **No confirmation of any kind when a valid file is selected.** Lines 18–19 (`setSelectedFile(file); setError(null);`) and the full render return (lines 24–38), source-verified: `selectedFile` is stored in state but never rendered — no "Selected: filename.pdf" text for sighted or AT users.
   - Confidence: MEDIUM-HIGH
   - Why this matters: WCAG 4.1.3 (Status Messages) is the closest fit for the missing acknowledgment; the practical effect is that success and silence look identical to the user.
   - Mitigated by: browsers typically surface the chosen filename in the native file-input's own UI chrome, a platform-level signal outside this component's control — which is why this is rated MAJOR rather than the CRITICAL "silent success" it would otherwise be.
   - Fix: Render `selectedFile.name` in an app-level confirmation once set, ideally inside or referenced by the same describedby chain as the help text.

**Minor Findings** (friction but workaround exists):

- Error message names the failure category but not the actual threshold or a corrective action: `"File too large"` vs., e.g., `"File too large — choose a file under 5MB"`. WCAG 3.3.3 (Error Suggestion). A workaround (trial and error) exists.

**Enhancements** (best practice not met):

- None warranted beyond the Minor item above. Most of this component's gaps land at Major/Critical because the association *layer itself* is absent, not because best-practice polish is missing on top of a working foundation — manufacturing an Enhancement item here would not reflect real signal.

**What's Missing**: See Gap Analysis above — consolidated: label association, `id` scaffolding, `aria-describedby` (error and help text), `aria-invalid`, live-region announcement, upfront constraint disclosure, and success confirmation.

**Multi-Perspective Notes**: See the alarm table and perspective narratives in the Multi-Perspective Review section above (Screen reader: HIGH; Keyboard-only: LOW; Low vision: MEDIUM/unmeasured; Cognitive: MEDIUM; Vestibular, Auditory: LOW/not applicable; Environmental contrast: MEDIUM/unmeasured).

**Verdict Justification**: Two CRITICAL findings — no application-supplied label on the component's only control, and a silent validation failure with no compensating success signal — are enough on their own to bar ACCEPT or ACCEPT-WITH-RESERVATIONS; per the Severity Scale, both match the CRITICAL bar exactly ("core state is not communicated," "form validation fails silently"), and neither survives the Realist Check (see Phases 8–9 section above) — the affected user group has no self-service workaround for either gap. The verdict is REVISE rather than REJECT because the architectural foundation is sound — a native `<input type="file">`, no ARIA-masking anti-pattern — and every finding is an additive wiring fix (label, ids, `aria-describedby`, `aria-invalid`, a live region, and instructional text), not a pattern replacement. Screen reader is flagged HIGH alarm and should go through `/perspective-audit` before this component ships, given how much of the review's severity is concentrated in that one perspective.

Structured `A11y Evidence Finding` blocks (the optional contract) are omitted throughout: this review had no hashing/Bash tooling available to compute genuine stable fingerprints, and inventing a hex string to fill that field would violate this protocol's own "do not invent fields to make weak evidence look complete" instruction. The prose findings above carry the full required evidence (file:line, element, user group, citation, fix) instead.

**Open Questions (unscored)**:

- Whether a `<form>`/submit affordance exists outside this fragment — the component as shown has no submit control, which may be intentional (auto-processing on change) or an artifact of the fixture being trimmed for review. Not enough context to score.
- Three axe-core findings — `landmark-one-main`, `page-has-heading-one`, `region` (digest-only, moderate impact) — describing the test-harness page shell rather than this component's own code. Flagged for the developer to confirm once this component is embedded in a real page, not scored against `BuggyFileInput`.
- The second `Tab` in the trace moving the active element to `body` (digest-only, `step_0002`) — the digest itself declines to characterize this as a defect, and this review cannot inspect the full page's focus order beyond the supplied 3-step session. Plausibly just "end of a single-control test page."
- The `sr_announcement` difference between `step_0001` (`new_phrases: ["document"]`, `focus_announcement: "document"`) and `step_0003` (`new_phrases: []`, `focus_announcement: null`) for the same element in the same AX state (digest-only) — the digest explicitly leaves this judgment call to the consumer, and without the raw trace file this review cannot determine whether it's a page-landing artifact unrelated to the input or something worth independent investigation.
- Text contrast for the "Upload file" label and "File too large" error text — no CSS was supplied, and the only contrast figure in evidence (4.86, digest-only) is for the focus ring, not this text. WCAG 1.4.3 cannot be scored either way.
- Target size (WCAG 2.5.8) of the OS-rendered file-picker button — platform-controlled and not assessable from the supplied source.
