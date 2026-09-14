# Input: ACR drafting request — Riverbend Municipal Permits Portal (rmp-2026q3)

The audit-scope evaluation below is finished and delivered. Serialize it into
a draft Accessibility Conformance Report in OpenACR YAML per the engagement
record. Return the complete OpenACR YAML document in a single ```yaml code
fence, followed by the handoff message for the engagement owner.

---

## Engagement record (ACR-feed fields)

- **Report title:** Riverbend Municipal Permits Portal Accessibility Conformance Report
- **Product:** Riverbend Municipal Permits Portal, version 3.2.0 — Riverbend
  City's online service for permit applications, inspection scheduling, and
  permit status tracking at permits.riverbend.example.
- **Drafting evaluator (ACR author):** Cascade Accessibility Consultants;
  contact: Jordan Everett; email: j.everett@cascadeaccess.example;
  website: https://cascadeaccess.example
- **Party responsible for the product (vendor block):** Riverbend City,
  Digital Services; email: permits-support@riverbend.example
- **Report date for the ACR:** 2026-09-05 (evaluation completion date —
  use this date).
- **OpenACR document version:** 1.
- **Feedback channel:** https://permits.riverbend.example/accessibility-feedback
- **Publication license:** the City has not decided one — leave unset.
- **Report template requirement** (from the audit plan's additional
  requirements): ACR in OpenACR format, catalog
  `2.5-edition-wcag-2.2-508-en` (WCAG 2.2 edition). Finish surface: YAML
  plus CLI-rendered HTML review.

## Finished evaluation report (delivered 2026-09-05, contract-conformant)

### Evaluation identity

Evaluator: Cascade Accessibility Consultants (reporting lead: Jordan
Everett). Commissioner: Riverbend City, Digital Services. Evaluation window:
2026-08-04 → 2026-09-05. Methodology: WCAG-EM 2.0.

### Scope

Everything public on permits.riverbend.example (permit search, application
intake, payment, permit status and dashboard) plus the authenticated
applicant portal. No native apps, no PDFs — the product is web-only. No
exclusions.

### Conformance target

WCAG 2.2 Level AA.

### Accessibility support baseline

NVDA 2026.1 + Firefox 141 (Windows 11); VoiceOver + Safari 18 (macOS 15);
keyboard-only without a screen reader.

### Technologies relied upon

HTML, CSS, JavaScript (Vue.js 3), WAI-ARIA.

### Sample set

Structured samples (5): S01 home / permit search, S02 permit application
form (step 1 of 3 — applicant information), S03 payment flow (credit card
entry and confirmation), S04 permit status dashboard / applicant account,
S05 help / FAQ page. Random sample (1): R01
/permits/archive/residential-fence-2025 — seeded shuffle of the 142-URL
sitemap, seed 4417; the comparison surfaced no new content types or finding
types. Complete process (1): P01 select permit type → enter applicant
information → proceed to payment entry — traverses S01/S02/S03; the payment
step was tested through the credit-card entry view only; sandbox restrictions
blocked submission and post-submission states. State coverage per sample:
default, loading, error, and expanded states where the template has them.

### Outcomes — web component, per SC across the sample set

| SC | Name | Level | Web outcome across samples | Failing samples | finding_id(s) |
|----|------|-------|---------------------------|-----------------|---------------|
| 1.1.1 | Non-text Content | A | passed | — | — |
| 1.2.1 | Audio-only and Video-only (Prerecorded) | A | inapplicable — no audio or video content exists in any sampled view | — | — |
| 1.2.2 | Captions (Prerecorded) | A | inapplicable — no media | — | — |
| 1.2.3 | Audio Description or Media Alternative (Prerecorded) | A | inapplicable — no media | — | — |
| 1.3.1 | Info and Relationships | A | passed | — | — |
| 1.3.2 | Meaningful Sequence | A | passed | — | — |
| 1.3.3 | Sensory Characteristics | A | passed | — | — |
| 1.4.1 | Use of Color | A | passed | — | — |
| 1.4.2 | Audio Control | A | inapplicable — no auto-playing audio | — | — |
| 2.1.1 | Keyboard | A | passed (P01 fully keyboard-operable through the payment-entry view) | — | — |
| 2.1.2 | No Keyboard Trap | A | passed | — | — |
| 2.1.4 | Character Key Shortcuts | A | inapplicable — no character-key shortcuts implemented | — | — |
| 2.2.1 | Timing Adjustable | A | passed (session timeout warning verified in S02) | — | — |
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
| 3.2.6 | Consistent Help | A | passed | — | — |
| 3.3.1 | Error Identification | A | passed | — | — |
| 3.3.2 | Labels or Instructions | A | passed | — | — |
| 3.3.7 | Redundant Entry | A | passed | — | — |
| 4.1.1 | Parsing | A | inapplicable — criterion removed in WCAG 2.2; the VPAT 2.5 catalog retains the row. Record as not applicable with the removal note. | — | — |
| 4.1.2 | Name, Role, Value | A | passed — the automated scan flagged an aria-expanded state discrepancy on the permit-type filter dropdowns in S01; manual keyboard and screen-reader walkthrough across S01, S02, and S04 found all expanded/collapsed states announce and update correctly; finding a11y_rmp_filter_aria_flag is a scanner detection not reproduced in manual testing | S01 (cleared) | a11y_rmp_filter_aria_flag |
| 1.2.4 | Captions (Live) | AA | inapplicable — no media | — | — |
| 1.2.5 | Audio Description (Prerecorded) | AA | inapplicable — no media | — | — |
| 1.3.4 | Orientation | AA | passed | — | — |
| 1.3.5 | Identify Input Purpose | AA | passed (autocomplete tokens on applicant name, address, and email fields in S02) | — | — |
| 1.4.3 | Contrast (Minimum) | AA | failed in S01, S02, S03, and S04 — body text rendered against the blue permit-portal header bar measures 2.8:1 against the header background; 4.5:1 required for normal text; the failure appears across the four main-flow samples; passed in S05 and R01 where the header pattern does not appear | S01, S02, S03, S04 | a11y_rmp_header_text_contrast |
| 1.4.4 | Resize text | AA | passed | — | — |
| 1.4.5 | Images of Text | AA | passed | — | — |
| 1.4.10 | Reflow | AA | passed | — | — |
| 1.4.11 | Non-text Contrast | AA | passed | — | — |
| 1.4.12 | Text Spacing | AA | passed | — | — |
| 1.4.13 | Content on Hover or Focus | AA | passed | — | — |
| 2.4.5 | Multiple Ways | AA | passed | — | — |
| 2.4.6 | Headings and Labels | AA | passed | — | — |
| 2.4.7 | Focus Visible | AA | failed in S02 — the permit application form suppresses the browser default focus outline on text inputs and date-picker fields without providing a replacement indicator; keyboard users lose position tracking across the multi-step form; passed in all other samples | S02 | a11y_rmp_form_focus_invisible |
| 2.4.11 | Focus Not Obscured (Minimum) | AA | passed | — | — |
| 2.5.7 | Dragging Movements | AA | passed | — | — |
| 2.5.8 | Target Size (Minimum) | AA | passed | — | — |
| 3.1.2 | Language of Parts | AA | passed | — | — |
| 3.2.3 | Consistent Navigation | AA | passed | — | — |
| 3.2.4 | Consistent Identification | AA | passed | — | — |
| 3.3.3 | Error Suggestion | AA | passed | — | — |
| 3.3.4 | Error Prevention (Legal, Financial, Data) | AA | **cantTell** — fee payments exist on S03, but sandbox restrictions blocked payment submission; whether submissions are reversible or reviewed before commit could not be determined; outcome is inconclusive pending access to a non-sandboxed test environment | — | — |
| 3.3.8 | Accessible Authentication (Minimum) | AA | passed (password managers supported; no cognitive test imposed in the login flow) | — | — |
| 4.1.3 | Status Messages | AA | passed | — | — |

AAA criteria: not evaluated — the engagement's conformance target is
WCAG 2.2 AA and no AAA evidence was collected.

### Findings on file (evidence-finding contract, abbreviated)

```
finding_id: a11y_rmp_header_text_contrast
fingerprint: 3a7bc901
severity: CRITICAL
wcag_or_apg: WCAG 1.4.3 Contrast (Minimum)
evaluation_context: evaluation_id=rmp-2026q3; sample_id=S01 (also S02, S03, S04)
evidence: body text on the blue permit-portal header bar measures 2.8:1 against
  the header background; 4.5:1 required for normal text; the defect repeats
  across every main-flow sample that uses this header pattern
detected_by: [axe-core, wave]
corroboration: corroborated
```

```
finding_id: a11y_rmp_form_focus_invisible
fingerprint: 8e42df56
severity: MAJOR
wcag_or_apg: WCAG 2.4.7 Focus Visible
evaluation_context: evaluation_id=rmp-2026q3; sample_id=S02
evidence: permit application form inputs and date-picker fields carry
  outline:none with no replacement focus indicator; keyboard users lose
  position tracking across the multi-step form
detected_by: [axe-core, html_codesniffer]
corroboration: corroborated
```

```
finding_id: a11y_rmp_filter_aria_flag
fingerprint: 2c85e109
severity: INFO
wcag_or_apg: WCAG 4.1.2 Name, Role, Value
evaluation_context: evaluation_id=rmp-2026q3; sample_id=S01
evidence: automated scan flagged potential aria-expanded inconsistency on
  permit-type filter dropdowns; manual walkthrough (NVDA + Firefox, VoiceOver
  + Safari, keyboard-only; S01, S02, S04) found all states announce and update
  correctly; the scanner detection was not reproduced in manual testing
detected_by: [axe-core, alfa]
corroboration: corroborated
trend: cleared-by-manual-testing
```

```
finding_id: a11y_rmp_payment_review_canttest
fingerprint: 9f12c847
severity: UNKNOWN
wcag_or_apg: WCAG 3.3.4 Error Prevention (Legal, Financial, Data)
evaluation_context: evaluation_id=rmp-2026q3; sample_id=S03
evidence: sandbox restrictions blocked payment submission; reversibility and
  pre-submission review behaviour could not be observed; outcome is inconclusive
detected_by: [axe-core, html_codesniffer]
corroboration: corroborated
```

### Coverage boundary

None — every in-scope surface is a web view reachable by the web
measurement stack. No native, document, hardware, or support-documentation
surfaces are in scope. (3.3.4 is an evaluation gap, not a
coverage-boundary item: the surface is reachable; the testing was not
completed due to sandbox restrictions.)

## Catalog frame — `2.5-edition-wcag-2.2-508-en` (from the pinned @openacr/openacr@0.3.8 package)

Adherence terms (catalog `terms:`): `supports` ("at least one method that
meets the criterion without known defects or meets with equivalent
facilitation"); `partially-supports` ("Some functionality of the product
does not meet the criterion"); `does-not-support` ("The majority of product
functionality does not meet the criterion"); `not-applicable`;
`not-evaluated` ("can only be used in WCAG Level AAA criteria").

Components: web; electronic-docs; software; authoring-tool.

WCAG chapters: `success_criteria_level_a` (32 criteria) and
`success_criteria_level_aa` (24 criteria) — the A/AA criterion list is
exactly the SC column of the Outcomes table above, including 4.1.1.
`success_criteria_level_aaa` (31 criteria): 1.2.6 Sign Language
(Prerecorded); 1.2.7 Extended Audio Description (Prerecorded); 1.2.8 Media
Alternative (Prerecorded); 1.2.9 Audio-only (Live); 1.3.6 Identify Purpose;
1.4.6 Contrast (Enhanced); 1.4.7 Low or No Background Audio; 1.4.8 Visual
Presentation; 1.4.9 Images of Text (No Exception); 2.1.3 Keyboard (No
Exception); 2.2.3 No Timing; 2.2.4 Interruptions; 2.2.5 Re-authenticating;
2.2.6 Timeouts; 2.3.2 Three Flashes; 2.3.3 Animation from Interactions;
2.4.8 Location; 2.4.9 Link Purpose (Link Only); 2.4.10 Section Headings;
2.4.12 Focus Not Obscured (Enhanced); 2.4.13 Focus Appearance; 2.5.5 Target
Size (Enhanced); 2.5.6 Concurrent Input Mechanisms; 3.1.3 Unusual Words;
3.1.4 Abbreviations; 3.1.5 Reading Level; 3.1.6 Pronunciation; 3.2.5 Change
on Request; 3.3.5 Help; 3.3.6 Error Prevention (All); 3.3.9 Accessible
Authentication (Enhanced).

Revised Section 508 chapters: `functional_performance_criteria` (9
provisions, 302.1–302.9); `hardware` (55 provisions, 402.2.1–415.1.2);
`software` (26 provisions, 502.2.1–504.4);
`support_documentation_and_services` (5 provisions, 602.2–603.3).
