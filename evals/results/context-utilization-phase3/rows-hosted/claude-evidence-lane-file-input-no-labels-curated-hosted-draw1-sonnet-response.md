# Accessibility Design Critic — Review of `BuggyFileInput`

## Phase 0 — Evidence Triage

This is a review of an original component design, not a fix/remediation pass (the fixture presents `BuggyFileInput` in its current, uncorrected state), so the fix-specific evidence-type-mismatch check does not apply here.

Test evidence is available and is treated as HARD EVIDENCE, upgrading several findings from design reasoning to measured fact:

- **axe-core 4.13.0** scan of `http://127.0.0.1:8777/file-input-no-labels.html` at viewport `1280x800`: 4 violations (`label` critical, `landmark-one-main` moderate, `page-has-heading-one` moderate, `region` moderate).
- **keyboard-a11y-tester driven trace** (3 steps: Tab, Tab, Shift+Tab; stated goal "Choose a file to upload using only the keyboard and review any feedback the page gives"): captures `ax_name_role_state`, `focus_visible`, and `sr_announcement` for each step.
- **keyboard-a11y-tester screen-reader reading-order census**: 3 spoken-phrase entries for the page.

No `findings.json` (batch-crawl) artifact was supplied, so no claim below is sourced from batch-crawl output. Tool/version provenance for the trace and census rests on directory naming, not a self-declared field inside those files — axe's version is self-declared. These provenance boundaries are inherited from the evidence pack and are not re-verified here.

## Phase 1 — Pre-commitment Predictions

Before weighing the evidence, the predicted defects for "static form field with a visual label and a conditional inline error" are:
1. Visual label text not programmatically associated with the input (missing `<label for>`).
2. Error message rendered but not tied to the input via `aria-describedby`.
3. No `aria-invalid` set when validation fails.
4. Accepted-file-type / size-limit constraints not surfaced as accessible help text.
5. Error not announced proactively (no live region), so a user whose focus stays on the input never learns validation failed.

All five were confirmed. One thing not predicted going in: the *mechanism* by which the missing label surfaces. A shallow "does the element have an accessible name at all" check would pass here, because Chromium supplies file inputs a UA-default accessible name ("Choose File", role `button`) even with zero authored labelling. The real defect is that "Upload file" — the only text a sighted user reads as the field's purpose — never reaches that name. This is confirmed independently by two tools (axe's `label` rule and the keyboard-a11y-tester trace's captured `ax_name_role_state`), which is a stronger basis than either alone.

## Investigation Summary (Phases 2–7)

**Semantic HTML (Phase 2):** The interactive control itself is native (`<input type="file">`) — correct, no ARIA-replacing-native anti-pattern on the widget. But the intended label (`<div>Upload file</div>`, line 26) is a bare `div`, not a `<label>`, with no `htmlFor`/`id` pairing and no wrapping. This isn't ARIA masking bad semantics (Phase 2's specific red flag) — it's a plainer defect: no semantic layer, native or ARIA, connects the visible text to the control at all.

**ARIA pattern compliance (Phase 3):** Not a composite widget (no tabs/menu/listbox/combobox/dialog), so no APG interaction pattern applies. There are zero ARIA attributes anywhere in the component — Phase 3's question "is the pattern complete or partial" resolves to "there is no ARIA layer to be partial." The real gaps are in native semantics (Phase 2) and state communication (Phase 5), not APG pattern completeness.

**Focus management (Phase 4):** Verified by hard evidence, and it's clean. Step 1: Tab reaches the input (`dom_order_index 12`), `focus_moved: true`, `focus_visible` reports `outline` indicator at 4.86:1 contrast (`aaa_pass: true`, `area_pass: true`) — WCAG 2.4.7/2.4.13 are well satisfied. Step 2: Tab moves to `body` (role `none`) — expected, since this fixture page has exactly one focusable element; not a trap (WCAG 2.1.2 holds). Step 3: Shift+Tab returns to the same input with identical `ax_name_role_state`. No focus-trap, no dead end, no restoration logic needed (nothing opens/closes). This is a genuinely clean result and is reported as such rather than manufactured into a finding.

One unresolved wrinkle from the trace: `sr_announcement.focus_announcement` is `"document"` at step 1 (plausibly a page-load artifact coinciding with the first Tab) and `null` at step 3, when landing on the *identical* element in the *identical* state via Shift+Tab. Routed to Open Questions below rather than scored — see reasoning there.

**State communication (Phase 5):** This is where the component fails hardest, and it is independently confirmed by the evidence pack's own absence claims: `.steps[].sr_announcement.live_announcements` → `[[],[],[]]` and `.declared_live_regions` → `[]` across all three artifacts. Combined with a direct code read (no `aria-live`, no `role="alert"`, no `aria-describedby`, no `aria-invalid` anywhere in the JSX), this is now a measured fact, not an inference: the error state is entirely invisible to assistive technology unless a user happens to navigate directly to that part of the DOM.

**Gap analysis / mandatory anti-pattern checks (Phase 7):** Working through the "known anti-patterns from prior third-party audit" checklist explicitly rather than skipping it:
1. *Broadcast vs. Association* — not violated. This is a single field, not a loop/repeating template, so recommending `role="alert"` (or `aria-live`) on the one error container below is the correct pattern here, not the anti-pattern (which targets per-field alert regions inside repeating templates).
2. *title vs. aria-label conflation* — N/A, no `title` attribute used anywhere.
3. *ARIA without visible label* — N/A in the form described (no `aria-label` on a wrapper while children lack visible text); the inverse problem exists instead — no visible-and-associated label AND no `aria-label`, either.
4. *Else-branch coverage* — N/A; the only branch (`if/else` in `handleFileChange`) is size-validation logic, not a UI-variant fix that could apply to one branch and miss another.
5. *Single-selector scope* — N/A, no CMS/selector-driven DOM targeting.
6. *td-in-for-loop row headers* / 7. *role="presentation" on data tables* — N/A, no tables.
8. *Empty/decorative alt on content images* — N/A, no images.
9. *DOM-verification required* — applicable as a forward constraint on the fix: once `id`/`htmlFor`/`aria-describedby` are added, verify in the rendered DOM that the `aria-describedby` id reference actually resolves to the error element at the moment it's conditionally rendered, not before.

**Known false positives** (axe `no-noninteractive-element-interactions`, `anchor-is-valid`, `color-contrast` on gradients, `region` on portals, `aria-allowed-attr` via spread props) — none apply to this code; no props are spread, no portals, no anchors, no custom `role` pass-through. The `label` critical finding is not on that watch-list and is corroborated by a second, independent tool (the trace's captured name), so it is reported at HIGH confidence rather than "axe said so."

## Perspective Alarm Levels (Phase 6)

| Perspective | Alarm Level | Trigger Signal |
|-------------|-------------|-----------------|
| Screen reader | **HIGH** | Missing accessible label (confirmed by axe `label` critical + trace showing the UA-generic name "Choose File", not "Upload file"); zero state communication for the error path (no `aria-describedby`, `aria-invalid`, or live region) |
| Keyboard-only | LOW | Tab/Shift+Tab verified working with no trap; focus indicator measured at 4.86:1 contrast, AAA-passing; single native tab stop, no composite widget requiring roving tabindex |
| Low vision | MEDIUM | No CSS was supplied with this fixture, so contrast, 200% zoom reflow, and touch target sizing for `.error-message`/`.file-upload` cannot be verified either way — flagged as unknown, not cleared |
| Cognitive | MEDIUM | Error message states the problem ("File too large") but omits the actual limit (5MB), a low-cost fix; otherwise a minimal, uncluttered single-field interaction |
| Vestibular & motion | LOW | No animation, transition, or auto-playing content present |
| Auditory access | LOW | No audio/video content present |
| Environmental contrast | MEDIUM | Cannot verify contrast ratios or color-only reliance without the stylesheet — same evidence gap as Low vision, called out separately because it governs a distinct SC set (1.4.3/1.4.11/1.4.1) |

Screen reader is HIGH; Low vision, Cognitive, and Environmental contrast are MEDIUM. Per protocol, this component should be flagged for `/perspective-audit` before this is considered resolved, particularly on the screen-reader axis.

---

**VERDICT: REJECT**

**Overall Assessment**: The architectural choice (native `<input type="file">`, no custom ARIA widget) is correct and requires no rework. But every one of the component's own five stated "Expected Behavior" requirements is unmet, and two of the gaps independently block core functionality for screen reader users: the field has no real accessible label, and a failed validation produces no announcement at all. This is not a "mostly there" component with a few rough edges — it is a native input with zero of its required wiring in place.

**Pre-commitment Predictions**: All 5 predicted gaps (label association, error association, missing `aria-invalid`, missing help text, silent error) were confirmed. The specific mechanism behind the label gap — a UA-default accessible name masking the missing authored label — was not anticipated in the initial prediction and only surfaced by cross-referencing the axe violation against the trace's captured `ax_name_role_state`.

**Critical Findings** (blocks access entirely for a user category):

1. **Missing accessible label on the file input.** `Component Code, line 26`: `<div>Upload file</div>` is a plain, unassociated `div` — not a `<label>`, no `htmlFor`, no `id` on the input at line 27 to point to. Confirmed by axe-core rule `label` (impact: critical, selector `input`, tags include `wcag2a`, `wcag412`) and independently corroborated by the keyboard-a11y-tester trace: at both step_0001 and step_0003, the input's computed accessible name is `"Choose File"` with role `"button"` — the browser's built-in default for an unlabelled file input, not "Upload file." A screen reader user tabbing to this field hears "Choose File, button" with no indication of what file is being requested. In a form with more than one file field, every instance would be indistinguishable.
   - Confidence: HIGH (two independent tools converge on the same fact)
   - Why this matters: Screen reader and voice-control users get no task context from the field itself. This is the archetypal "Name" failure under WCAG 4.1.2 — the accessible name exists (so a naive "has some name" check would wrongly pass it) but does not reflect the field's purpose.
   - Fix: `<label htmlFor="file-upload-input">Upload file</label>` wrapping or paired via `htmlFor`/`id` with the `<input id="file-upload-input" type="file" .../>`.
   - WCAG/APG: 1.3.1 Info and Relationships (A), 4.1.2 Name, Role, Value (A), 3.3.2 Labels or Instructions (A).

2. **Validation failure is entirely silent to assistive technology.** `Component Code, lines 32–36`: the error `<div className="error-message">{error}</div>` has no `role="alert"`, no `aria-live`, and is not referenced by the input via `aria-describedby`. Native file inputs return focus to themselves after the OS picker closes, so focus does not move toward the error text. Confirmed absent in the evidence pack independently of the code read: `.steps[].sr_announcement.live_announcements` → `[[],[],[]]` and `.declared_live_regions` → `[]` across the trace and census. A screen reader user who selects an oversized file gets no announcement that anything happened at all.
   - Confidence: HIGH (code read + independent evidence-pack absence claims agree)
   - Why this matters: This is functionally the same failure mode the protocol names as an archetypal CRITICAL example — validation fails and nothing is communicated. A user may believe the upload succeeded, or may simply be confused, with no path to discovering otherwise short of guessing to explore the DOM.
   - Fix: Add `role="alert"` (or wrap in a persistent `aria-live="assertive"` container) on the error `div`. This is a single field, not a repeating template, so this does not trigger the "broadcast vs. association" anti-pattern that specifically targets per-field alert regions inside loops.
   - WCAG/APG: 4.1.3 Status Messages (AA), 3.3.1 Error Identification (A).

**Major Findings** (significantly degrades experience):

1. **Error text not associated with the input via `aria-describedby`.** `Component Code, line 27` (`<input>`) has no `id`; the error `div` at line 33 has no `id` either, so there is no `aria-describedby` link even after the live-region fix above. A user who discovers the error once (via the live-region fix, or by chance) and later tabs back to the field will not hear it re-stated as part of the field's description.
   - Confidence: HIGH (direct code read)
   - Why this matters: Durable, repeatable access to "why is this field invalid" depends on this association, independent of whether the initial announcement fired.
   - Fix: `<input id="file-upload-input" aria-describedby={error ? "file-upload-error" : undefined} .../>` with `<div id="file-upload-error" className="error-message">`.
   - WCAG/APG: 1.3.1 Info and Relationships (A), 3.3.1 Error Identification (A).
   - Recalibration note: this would be CRITICAL on its own if the live-region fix (Critical Finding 2) were absent — since that fix already guarantees the first occurrence of the error is announced, this finding is downgraded to MAJOR. Mitigated by: Critical Finding 2's fix independently covers the first-encounter silent-failure risk; this finding is about repeat-visit durability, a real but lesser gap.

2. **`aria-invalid` is never set.** `handleFileChange` (lines 15–21) sets `error` state but never toggles an `aria-invalid` attribute on the input at line 27. The field's own validity state is not programmatically exposed at any point.
   - Confidence: HIGH (direct code read)
   - Why this matters: Without `aria-invalid`, many screen reader/browser combinations give no "invalid entry" signal when focus is on the field after a failed validation — the user must rely entirely on discovering and remembering the error text.
   - Fix: `<input aria-invalid={error ? "true" : "false"} .../>` (or omit the attribute when not invalid, but never send `"yes"/"no"` — only the string `"true"`/`"false"`).
   - WCAG/APG: 4.1.2 Name, Role, Value (A).
   - Recalibration note: same mitigation as above — downgraded from a CRITICAL candidate because Critical Finding 2 already prevents total silence on first failure. Mitigated by: overlapping coverage with the live-region fix.

3. **No accessible or visible help text for file-type and size constraints.** The `accept=".pdf,.doc,.docx"` attribute (line 29) only filters what the OS file-picker dialog shows — it is not rendered as visible text and is not announced to assistive technology. There is no text anywhere in the component stating "PDF, DOC, or DOCX only" or "maximum 5MB" before a user acts. This gap affects sighted and non-sighted users equally: nobody is told the constraints up front.
   - Confidence: HIGH (direct code read — no such text exists in the render output at all, not merely unassociated)
   - Why this matters: Users can only learn the size limit by triggering the error, and can only learn the type restriction by trial and error against the OS picker's filtering (which some OS/browser combinations apply loosely). This is a discoverability failure, not an access-blocking one — the task remains completable via trial and error.
   - Fix: Add visible instruction text (e.g., "Accepted formats: PDF, DOC, DOCX. Maximum size: 5MB.") associated via the same `aria-describedby` used for the error, or a separate `id` referenced alongside it (`aria-describedby="file-upload-help file-upload-error"` when both are present).
   - WCAG/APG: 3.3.2 Labels or Instructions (A).

**Minor Findings** (friction but workaround exists):

- The error message text ("File too large," line 17) states the problem but not the actual limit or a corrective action. WCAG 3.3.3 Error Suggestion (AA) expects a suggested fix where one is known and low-cost to provide — here the 5,000,000-byte threshold is a fixed constant already known in code. Recalibrated to MINOR rather than MAJOR: the message isn't absent or misleading, only underspecified, and a user can reasonably infer "pick a smaller file." Confidence: MEDIUM (this edges toward a UX-writing judgment call rather than a hard binary defect — a developer could plausibly argue the current text is adequate).
- `selectedFile` state (line 11, set at line 19) is tracked but never rendered anywhere in the component's own output. There is no custom confirmation that a file was successfully chosen, or what its name is — success feedback is delegated entirely to the native browser file-input widget's own built-in filename display, which this review has no evidence about either way (no step in the supplied trace captured a successful file-selection state; all 3 steps are Tab/Tab/Shift+Tab with no file chosen). Flagged MINOR rather than left unmentioned because it's the silent-success mirror of Critical Finding 2 (silent failure) and the fixture's own "Expected Behavior" list is silent on it — this was found by reading the code independently of that checklist, not by checking boxes against it.

**Enhancements** (best practice not met, no access barrier):

- axe-core also flagged `landmark-one-main` (moderate), `page-has-heading-one` (moderate), and `region` (moderate) against `html`/`#root` for the page hosting this fixture. None of these three carry a `wcag2*` tag in the evidence pack (only `label` does) — axe itself classifies them as `best-practice`, not WCAG violations. Scope caveat: this component renders a `div`-wrapped fragment, not a page shell; it is not this component's job to own `<main>`/`<h1>`/landmark structure, and in a real application it would be mounted inside a page that supplies those elsewhere. Because the fixture's evaluated page appears to contain only this component with no surrounding shell, these three findings are recorded here for completeness but not scored against the component under review. Needs verification: confirm in the real integration context (not this isolated fixture page) whether a landmark/heading structure exists around the mounted component.

**What's Missing** (gap analysis, Phase 7):

- No programmatic label association (Critical 1).
- No live announcement of the error (Critical 2).
- No `aria-describedby` link (Major 1).
- No `aria-invalid` state exposure (Major 2).
- No visible/accessible statement of accepted file types or the size limit (Major 3).
- No confirmation of a successful selection beyond whatever the native control shows on its own (Minor, unverified either way).
- Non-a11y aside, noted only for completeness and not scored: `handleFileChange` validates file *size* but never validates file *type* in JavaScript — `accept` is a soft browser-level filter a user can sometimes bypass. This is a functional/business-logic gap, not an accessibility finding, and is out of this review's scope.

**Multi-Perspective Notes**:

- **Screen reader user**: Tabbing to the field announces "Choose File, button" — generic, UA-supplied, disconnected from "Upload file." The visible label text and the error text both exist in the DOM as plain, unassociated text (confirmed by the reading-order census: entries for "Upload file" and "File too large" both carry `tag: null, selector: null`, meaning the census tool could not resolve either to a real element/role — they are anonymous text nodes, not a labelled control or an announced status). A user navigating by landmarks or headings (a common orientation strategy) would find neither, since none exist around this control in the evaluated page. A user relying on Tab-based forms navigation gets the field's generic name only; a user doing a full linear read-through would eventually hear "Upload file" and, if it's present at read time, "File too large" as incidental body text — but only via that specific navigation method, and never as validation feedback delivered at the moment it matters.
- **Keyboard-only user**: Clean. Tab reaches the input, Shift+Tab returns to it, no trap, focus indicator measured at 4.86:1 contrast (AAA-passing). The only unaddressed keyboard-relevant gap is that nothing shifts focus or draws attention toward the error when it appears — a sighted keyboard user without a screen reader would still see the error visually, so this is a screen-reader/state-communication gap more than a keyboard-operability one.
- **Low vision user (200% zoom, high contrast)**: Cannot be assessed — no CSS was included in this fixture. Contrast of `.error-message` text, reflow behavior, and whether the focus indicator (verified at 4.86:1 in the trace, for whatever default styling was live during that test) survives 200% zoom are all unknown. Recorded as an evidence gap, not cleared and not failed.
- **Cognitive accessibility**: The interaction is minimal and uncluttered (a real strength — no unnecessary complexity to navigate). The one gap is the error message omitting the specific size threshold, addressed as a Minor finding above.

**Verdict Justification**: Two CRITICAL findings — no real accessible label, and a validation failure that produces zero assistive-technology feedback — each independently satisfy the protocol's own definition of CRITICAL ("blocks access entirely for a user category" / "form validation fails silently"). Per Phase 8's recalibration rule, neither is eligible for downgrade: the missing label is unambiguous and corroborated by two independent tools, and the silent-error finding involves the user plausibly believing a submission succeeded when it didn't, which is treated the same as a data-loss-adjacent risk, not a minor inconvenience. Two candidate findings (`aria-describedby`, `aria-invalid`) were explicitly evaluated against the Realist Check and downgraded from CRITICAL-candidate to MAJOR, each with a stated mitigation (overlap with the live-region fix's first-encounter coverage) rather than a silent severity reduction.

REJECT rather than REVISE because the component implements none of its own five stated Expected Behaviors — every piece of AT-facing wiring (label, description, invalid state, live announcement, help text) is absent, not merely incomplete. This would upgrade to REVISE, and likely to ACCEPT-WITH-RESERVATIONS, once the two Critical findings and Major Finding 3 (help text) are addressed, since the underlying architecture (native `<input type="file">`, no ARIA anti-pattern, clean and already-verified focus behavior) requires no structural rework — only the missing wiring needs to be added.

**Open Questions (unscored)**:

- The keyboard-a11y-tester trace shows `sr_announcement.focus_announcement` as `"document"` at step_0001 and `null` at step_0003, for the identical element in the identical state (same `ax_name_role_state`, confirmed unchanged). This could be a genuine announcement-pipeline inconsistency, or it could be ordinary repeat-focus suppression (many real screen readers do not re-announce an unchanged control on a second, immediate re-focus) — and this component's code contains no mechanism (no state change, no ARIA mutation between visits) that would explain or fix a difference either way. A developer could reasonably refute a finding built on this alone. Recommend verification with a real screen reader before treating this as a code-level defect.
- Whether the native browser's own built-in "selected filename" display next to the file-input button is sufficient success confirmation, or whether a custom `selectedFile` confirmation should be rendered — no trace step captured a state where a file was actually chosen, so this cannot be resolved from the supplied evidence either way.
- All low-vision/contrast/zoom/target-size questions, pending the component's stylesheet (not included in this fixture).
- Whether the real integration context (as opposed to this isolated single-component fixture page) supplies the page-level landmark and heading structure that axe flagged missing at the `html`/`#root` level.
