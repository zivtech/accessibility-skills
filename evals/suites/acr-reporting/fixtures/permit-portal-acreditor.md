# Input: ACR drafting request — Alder Glen Permits Online (agp-2026c2)

The audit-scope evaluation below is finished and delivered. Serialize it into
a draft Accessibility Conformance Report in OpenACR YAML per the engagement
record. Return the complete OpenACR YAML document in a single ```yaml code
fence, followed by the handoff message for the engagement owner.

---

## Engagement record (ACR-feed fields)

- **Report title:** Alder Glen Permits Online Accessibility Conformance Report
- **Product:** Alder Glen Permits Online, version 4.2 — the City of Alder
  Glen's building- and event-permit application portal.
- **Drafting evaluator (ACR author):** Cardinal Accessibility Group;
  contact: Ruth Vance; email: ruth.vance@cardinala11y.example;
  website: https://cardinala11y.example
- **Party responsible for the product (vendor block):** City of Alder Glen,
  Digital Services Office; email: digital@alderglen.example
- **Report date for the ACR:** 2026-07-31 (evaluation completion date — use
  this date).
- **OpenACR document version:** 2 (this is the second evaluation cycle; the
  cycle-1 OpenACR was document version 1).
- **Feedback channel:** https://alderglen.example/accessibility-feedback
- **Publication license:** CC0-1.0 (the City publishes conformance reports
  as public records).
- **Report template requirement** (from the audit plan's additional
  requirements): ACR in OpenACR format. The City's procurement office
  completes and signs its ACRs in **GSA's ACR Editor
  (https://acreditor.section508.gov/)**, so the draft must use catalog
  `2.4-edition-wcag-2.1-508-en` — the editor cannot import WCAG 2.2-catalog
  documents. The evaluation itself measured WCAG 2.2 AA; WCAG 2.2-only
  outcomes must be reported without being dropped.

## Finished evaluation report (delivered 2026-07-31, contract-conformant)

### Evaluation identity

Evaluator: Cardinal Accessibility Group (reporting lead: Ruth Vance).
Commissioner: City of Alder Glen, Digital Services Office. Evaluation
window: 2026-07-06 → 2026-07-31. Methodology: WCAG-EM 2.0. This is the
engagement's second annual cycle (cycle 1 closed 2025-07-30); cycle-1
findings were re-verified this cycle and carry trend values.

### Scope

Everything public on permits.alderglen.example plus the authenticated
applicant dashboard. No native apps, no PDFs, no kiosks — the product is
web-only. No exclusions.

### Conformance target

WCAG 2.2 Level AA (the engagement's measurement target — unchanged by the
2.1-catalog drafting requirement).

### Accessibility support baseline

NVDA 2026.1 + Firefox 141 (Windows 11); VoiceOver + Safari 18 (macOS 15);
keyboard-only without a screen reader.

### Technologies relied upon

HTML, CSS, JavaScript (Vue), WAI-ARIA.

### Sample set

Structured samples (8): S01 home, S02 permit-type chooser, S03 application
form (building permit), S04 applicant dashboard, S05 fee calculator,
S06 document upload, S07 inspection scheduler, S08 help center. Random
sample (1): R01 /permits/fence-height-rules — seeded shuffle of the 96-URL
sitemap, seed 4113; the comparison surfaced no new content types or finding
types. Complete process (1): P01 apply for an event permit → pay the fee →
confirmation (default + declined-payment error branch; traverses
S02/S03/S05). State coverage per sample: default, error, and expanded
states where the template has them.

### Outcomes — web component, per SC across the sample set

| SC | Name | Level | Web outcome across samples | Failing samples | finding_id(s) |
|----|------|-------|---------------------------|-----------------|---------------|
| 1.1.1 | Non-text Content | A | failed in every sample — the sitewide header template announces its decorative divider images as "divider-ornament.svg" (all 9 samples: S01–S08, R01) | S01–S08, R01 (all) | a11y_decorative_divider_alt |
| 1.2.1 | Audio-only and Video-only (Prerecorded) | A | inapplicable — no audio or video content exists in any sampled view | — | — |
| 1.2.2 | Captions (Prerecorded) | A | inapplicable — no media | — | — |
| 1.2.3 | Audio Description or Media Alternative (Prerecorded) | A | inapplicable — no media | — | — |
| 1.3.1 | Info and Relationships | A | passed | — | — |
| 1.3.2 | Meaningful Sequence | A | passed | — | — |
| 1.3.3 | Sensory Characteristics | A | passed | — | — |
| 1.4.1 | Use of Color | A | passed | — | — |
| 1.4.2 | Audio Control | A | inapplicable — no auto-playing audio | — | — |
| 2.1.1 | Keyboard | A | passed (both P01 branches fully keyboard-operable) | — | — |
| 2.1.2 | No Keyboard Trap | A | passed | — | — |
| 2.1.4 | Character Key Shortcuts | A | inapplicable — no character-key shortcuts implemented | — | — |
| 2.2.1 | Timing Adjustable | A | passed in every sample carrying a session (S04, S06, P01) — the cycle-1 CRITICAL finding a11y_session_timeout_no_warning was fixed in v4.2 and re-verified absent this cycle (trend: resolved) | — | — |
| 2.2.2 | Pause, Stop, Hide | A | passed | — | — |
| 2.3.1 | Three Flashes or Below Threshold | A | passed | — | — |
| 2.4.1 | Bypass Blocks | A | passed | — | — |
| 2.4.2 | Page Titled | A | passed | — | — |
| 2.4.3 | Focus Order | A | passed | — | — |
| 2.4.4 | Link Purpose (In Context) | A | passed | — | — |
| 2.5.1 | Pointer Gestures | A | passed | — | — |
| 2.5.2 | Pointer Cancellation | A | passed | — | — |
| 2.5.3 | Label in Name | A | passed | — | — |
| 2.5.4 | Motion Actuation | A | inapplicable — no motion-actuated functions | — | — |
| 3.1.1 | Language of Page | A | passed | — | — |
| 3.2.1 | On Focus | A | passed | — | — |
| 3.2.2 | On Input | A | passed | — | — |
| 3.3.1 | Error Identification | A | passed (declined-payment branch errors announced and associated) | — | — |
| 3.3.2 | Labels or Instructions | A | failed in S05 — the fee-calculator inputs render without visible or programmatic labels; passed in every other sample | S05 | a11y_fee_calc_labels |
| 4.1.1 | Parsing | A | passed — evaluated for the 2.1-catalog draft: automated parsing checks (no duplicate ids, complete start/end tags, valid nesting) across all samples | — | — |
| 4.1.2 | Name, Role, Value | A | passed | — | — |
| 1.2.4 | Captions (Live) | AA | inapplicable — no media | — | — |
| 1.2.5 | Audio Description (Prerecorded) | AA | inapplicable — no media | — | — |
| 1.3.4 | Orientation | AA | passed | — | — |
| 1.3.5 | Identify Input Purpose | AA | passed (autocomplete tokens on all applicant-data fields) | — | — |
| 1.4.3 | Contrast (Minimum) | AA | passed | — | — |
| 1.4.4 | Resize text | AA | passed | — | — |
| 1.4.5 | Images of Text | AA | passed | — | — |
| 1.4.10 | Reflow | AA | passed | — | — |
| 1.4.11 | Non-text Contrast | AA | passed | — | — |
| 1.4.12 | Text Spacing | AA | passed | — | — |
| 1.4.13 | Content on Hover or Focus | AA | passed | — | — |
| 2.4.5 | Multiple Ways | AA | passed | — | — |
| 2.4.6 | Headings and Labels | AA | passed | — | — |
| 2.4.7 | Focus Visible | AA | passed | — | — |
| 3.1.2 | Language of Parts | AA | passed (Spanish help-center fragments marked) | — | — |
| 3.2.3 | Consistent Navigation | AA | passed | — | — |
| 3.2.4 | Consistent Identification | AA | passed | — | — |
| 3.3.3 | Error Suggestion | AA | passed | — | — |
| 3.3.4 | Error Prevention (Legal, Financial, Data) | AA | passed (fee payment has review + confirm step) | — | — |
| 4.1.3 | Status Messages | AA | passed (upload progress and confirmation announced) | — | — |

### Measured beyond the 2.1 catalog — WCAG 2.2-only A/AA outcomes

The evaluation's target is WCAG 2.2 AA; these six criteria have no row in
the `2.4-edition-wcag-2.1-508-en` catalog but were measured:

| SC | Name | Level | Outcome across samples | Failing samples | finding_id(s) |
|----|------|-------|------------------------|-----------------|---------------|
| 2.4.11 | Focus Not Obscured (Minimum) | AA | passed | — | — |
| 2.5.7 | Dragging Movements | AA | passed (parcel-map pan has button alternative) | — | — |
| 2.5.8 | Target Size (Minimum) | AA | failed in S03 and S07 — 16px toolbar icons below 24×24 with no spacing exception; passed elsewhere | S03, S07 | a11y_toolbar_target_size |
| 3.2.6 | Consistent Help | A | passed | — | — |
| 3.3.7 | Redundant Entry | A | failed in P01 — the payment step re-asks the applicant address already entered at S03; P01 is the only surface where redundant entry can occur | P01 | a11y_reentry_address |
| 3.3.8 | Accessible Authentication (Minimum) | AA | passed (password managers supported; no cognitive test) | — | — |

AAA criteria: not evaluated — the engagement's conformance target is
WCAG 2.2 AA and no AAA evidence was collected.

### Findings on file (evidence-finding contract, abbreviated)

```
finding_id: a11y_decorative_divider_alt
fingerprint: 3fa1c8d0
severity: MINOR
wcag_or_apg: WCAG 1.1.1 Non-text Content
evaluation_context: evaluation_id=agp-2026c2; sample_id=S01 (sitewide header template — every sample)
evidence: decorative divider images carry alt="divider-ornament.svg"; announced once per page by screen readers; content and controls unaffected
trend: new
```

```
finding_id: a11y_session_timeout_no_warning
fingerprint: 88e07b41
severity: CRITICAL
wcag_or_apg: WCAG 2.2.1 Timing Adjustable
evaluation_context: evaluation_id=agp-2026c2; sample_id=S04 (cycle-1 origin; re-verified this cycle)
evidence: CYCLE 1 (2025): applicant sessions expired at 20 minutes with no warning and no extend control, discarding in-progress applications. CYCLE 2 (this evaluation): fixed in v4.2 — warning dialog at 15 minutes with an extend control, verified present and operable in S04, S06, and both P01 branches. Re-verified absent in every sample carrying a session.
trend: resolved
```

```
finding_id: a11y_fee_calc_labels
fingerprint: 60b2d9ee
severity: MAJOR
wcag_or_apg: WCAG 3.3.2 Labels or Instructions
evaluation_context: evaluation_id=agp-2026c2; sample_id=S05
evidence: three numeric inputs (lot size, frontage, valuation) render with placeholder text only; no label elements, no aria-label
trend: new
```

```
finding_id: a11y_toolbar_target_size
fingerprint: ac44f17b
severity: MAJOR
wcag_or_apg: WCAG 2.5.8 Target Size (Minimum)
evaluation_context: evaluation_id=agp-2026c2; sample_id=S03 (also S07)
evidence: form-toolbar icon buttons measure 16×16 CSS px with adjacent targets < 24px apart; no equivalent larger control
trend: new
```

```
finding_id: a11y_reentry_address
fingerprint: 19c5e2a7
severity: MAJOR
wcag_or_apg: WCAG 3.3.7 Redundant Entry
evaluation_context: evaluation_id=agp-2026c2; sample_id=S05; process_id=P01/default-sequence
evidence: payment step re-asks the applicant address entered at the application step; no auto-population or selection offered
trend: new
```

### Fix-closure records (a11y-test / remediation lane, abbreviated)

```
item_id: rem-session-warn-3d8f21ac
closes: a11y_session_timeout_no_warning
original_observation: CYCLE 1 (2025): applicant sessions expired at 20 minutes with no warning and no extend control, discarding in-progress applications
root_cause_triage: C-implement-fresh
fix_approach: added a warning dialog at 15 minutes with a keyboard-operable extend control, shipped in v4.2
interaction_evidence: keyboard trace on v4.2 (Firefox, no AT) — dialog appears at the 15-minute mark in S04, S06, and both P01 branches; Tab reaches the extend control, Enter dismisses the dialog and resets the session timer
commit: PR #216 (alderglen-permits-web@4.2)
attestation:
  status: attested
  attested_by: "Diego Salcedo"
  attester_role: "accessibility QA lead, Cardinal Accessibility Group"
  attested_at: 2026-07-29T10:05:00Z
  attested_against:
    version: "4.2"
  attested_under: "WCAG-EM 2.0 retest"
  self_attested: false
  method:
    tooling: "NVDA 2026.1 + Firefox 141, keyboard only, on the v4.2 production build"
    action: "Sat idle on S04 until the 15-minute warning fired, tabbed to the extend control, pressed Enter"
    expected: "The warning dialog announces itself, the extend control is reachable, and Enter resets the session timer"
    observed: "Dialog announced; Tab reached the extend control; Enter dismissed the dialog and reset the session timer"
  second_confirmation:
    by: "Naomi Iheanacho"
    at: 2026-07-30T11:20:00Z
    tooling: "VoiceOver + Safari 18, keyboard only, on the v4.2 production build"
    observed: "Same result on S06: dialog announced at the 15-minute mark, extend control reachable, timer reset"
  claim_boundary: "Confirms rem-session-warn-3d8f21ac no longer reproduces at 4.2 for the S04/S06 session-timeout interaction. Not a re-evaluation of 2.2.1 across the sample set; nothing about other timed interactions."
```

### Coverage boundary

None — every in-scope surface is a web view reachable by the web
measurement stack. No native, document, hardware, or support-documentation
surfaces are in scope.

## Catalog frame — `2.4-edition-wcag-2.1-508-en` (from the pinned @openacr/openacr@0.3.8 package)

Adherence terms (catalog `terms:`): `supports` ("at least one method that
meets the criterion without known defects or meets with equivalent
facilitation"); `partially-supports` ("Some functionality of the product
does not meet the criterion"); `does-not-support` ("The majority of product
functionality does not meet the criterion"); `not-applicable`;
`not-evaluated` ("can only be used in WCAG Level AAA criteria").

Components: web; electronic-docs; software; authoring-tool.

WCAG chapters: `success_criteria_level_a` (30 criteria) and
`success_criteria_level_aa` (20 criteria) — exactly the SC rows of the main
Outcomes table above (the six WCAG 2.2-only criteria in the second table
have **no row in this catalog**). `success_criteria_level_aaa`
(28 criteria): 1.2.6 Sign Language (Prerecorded); 1.2.7 Extended Audio
Description (Prerecorded); 1.2.8 Media Alternative (Prerecorded); 1.2.9
Audio-only (Live); 1.3.6 Identify Purpose; 1.4.6 Contrast (Enhanced); 1.4.7
Low or No Background Audio; 1.4.8 Visual Presentation; 1.4.9 Images of Text
(No Exception); 2.1.3 Keyboard (No Exception); 2.2.3 No Timing; 2.2.4
Interruptions; 2.2.5 Re-authenticating; 2.2.6 Timeouts; 2.3.2 Three
Flashes; 2.3.3 Animation from Interactions; 2.4.8 Location; 2.4.9 Link
Purpose (Link Only); 2.4.10 Section Headings; 2.5.5 Target Size; 2.5.6
Concurrent Input Mechanisms; 3.1.3 Unusual Words; 3.1.4 Abbreviations;
3.1.5 Reading Level; 3.1.6 Pronunciation; 3.2.5 Change on Request; 3.3.5
Help; 3.3.6 Error Prevention (All).

Revised Section 508 chapters: `functional_performance_criteria` (9
provisions, 302.1–302.9); `hardware` (55 provisions, 402.2.1–415.1.2);
`software` (26 provisions, 502.2.1–504.4);
`support_documentation_and_services` (5 provisions, 602.2–603.3).
