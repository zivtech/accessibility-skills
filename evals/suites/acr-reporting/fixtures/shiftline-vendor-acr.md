# Input: ACR claims-verification request — ShiftLine Workforce Scheduling (mar-2026v1)

The verification engagement below is finished. Compare each Level A/AA web
claim in the vendor's ACR against the verification evidence and return the
engagement's verification report in Markdown, followed by the handoff note
for the procurement owner.

---

## Engagement record

- **Commissioner:** City of Marlow, IT Procurement — evaluating ShiftLine
  for a workforce-scheduling contract. The vendor's ACR (below) arrived
  with the bid on 2026-06-30.
- **Verifying evaluator:** Cardinal Accessibility Group (reporting lead:
  Ruth Vance; ruth.vance@cardinala11y.example).
- **Verification engagement:** mar-2026v1, window 2026-07-20 → 2026-08-07,
  WCAG-EM 2.0 sample of the vendor's demo tenant
  (marlow-demo.shiftline.example). Conformance target for verification:
  WCAG 2.2 Level AA, web component.
- **Subject product:** ShiftLine Workforce Scheduling, version 9.3 (the
  version the vendor's ACR claims to describe).
- **Commissioner-directed exclusion:** the staff SSO sign-in enclave (the
  city's identity provider) is production-only and could not be provisioned
  in the demo tenant — no authentication flow was exercisable at this
  scope.
- The subject ACR is a third-party document: this engagement holds no
  prior fingerprints for it and no earlier verification of this product.

## Subject: the vendor's ACR (received 2026-06-30, verbatim)

```yaml
title: ShiftLine Workforce Scheduling Accessibility Conformance Report
product:
  name: ShiftLine Workforce Scheduling
  version: "9.3"
author:
  name: Accessibility Office
  email: acr@shiftline.example
report_date: "2026-06-12"
catalog: 2.5-edition-wcag-2.2-508-en
chapters:
  success_criteria_level_a:
    criteria:
      - num: "1.1.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "1.2.1"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "No audio-only or video-only media in the product."
      - num: "1.2.2"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "No prerecorded media in the product."
      - num: "1.2.3"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "No prerecorded media in the product."
      - num: "1.3.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "1.3.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "1.3.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "1.4.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "1.4.2"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "No auto-playing audio."
      - num: "2.1.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Full keyboard operation across the application."
      - num: "2.1.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "2.1.4"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "No character-key shortcuts."
      - num: "2.2.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "2.2.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "2.3.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "2.4.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "2.4.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "2.4.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "2.4.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "2.5.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "2.5.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "2.5.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "2.5.4"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "No motion-actuated functions."
      - num: "3.1.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "3.2.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "3.2.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "3.2.6"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "3.3.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "3.3.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "3.3.7"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "4.1.1"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Criterion removed in WCAG 2.2; row retained by the catalog."
      - num: "4.1.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
  success_criteria_level_aa:
    criteria:
      - num: "1.2.4"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "No live media in the product."
      - num: "1.2.5"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "No prerecorded media in the product."
      - num: "1.3.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "1.3.5"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "1.4.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "All text meets the 4.5:1 minimum."
      - num: "1.4.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "1.4.5"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "1.4.10"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "1.4.11"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "1.4.12"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "1.4.13"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "2.4.5"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "2.4.6"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "2.4.7"
        components:
          - name: web
            adherence:
              level: partially-supports
              notes: "Known issue: the schedule grid's focus indicator can be difficult to see. A fix is on the roadmap."
      - num: "2.4.11"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "2.5.7"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "2.5.8"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "3.1.2"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Deferred to a future assessment."
      - num: "3.2.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "3.2.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "3.3.3"
        components:
          - name: web
            adherence:
              level: partially-supports
              notes: "Error suggestions are missing on the timeclock form; fix scheduled for v9.4."
      - num: "3.3.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
      - num: "3.3.8"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Single sign-on integrates with customer identity providers; no cognitive test."
      - num: "4.1.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Fully supported."
  success_criteria_level_aaa:
    notes: Not evaluated (Level AAA is outside the product's conformance target).
    criteria: []
  functional_performance_criteria:
    disabled: true
    notes: Not addressed in this report.
  hardware:
    disabled: true
    notes: Not addressed in this report.
  software:
    disabled: true
    notes: Not addressed in this report.
  support_documentation_and_services:
    disabled: true
    notes: Not addressed in this report.
```

## Verification evidence (delivered 2026-08-07, contract-conformant)

### Sample set

Structured samples (6): S01 dashboard, S02 schedule grid, S03 shift-swap
dialog, S04 timeclock, S05 reports, S06 employee profile + help area
(contains the onboarding walkthrough videos). Random sample (1): R01
/help/exporting-schedules — seeded shuffle of the 61-URL demo sitemap,
seed 6402; the comparison surfaced no new content types or finding types.
Complete process (1): P01 pick up an open shift → confirm (default +
conflict-error branch; traverses S02/S03). State coverage per sample:
default, loading, error, and expanded states where the template has them.
Accessibility support baseline: NVDA 2026.1 + Firefox 141 (Windows 11);
VoiceOver + Safari 18 (macOS 15); keyboard-only without a screen reader.

### Outcomes — web component, per SC across the verification sample

| SC | Name | Level | Verification outcome across samples | Failing samples | finding_id(s) |
|----|------|-------|-------------------------------------|-----------------|---------------|
| 1.1.1 | Non-text Content | A | passed | — | — |
| 1.2.1 | Audio-only and Video-only (Prerecorded) | A | inapplicable — no audio-only or video-only media exists in any sampled view | — | — |
| 1.2.2 | Captions (Prerecorded) | A | failed in S06 — three onboarding walkthrough videos in the employee-profile help area carry no captions | S06 | a11y_training_video_captions |
| 1.2.3 | Audio Description or Media Alternative (Prerecorded) | A | passed — the S06 walkthrough videos fully narrate their visual content (spoken UI walkthroughs), so a media alternative is not required beyond the existing audio | — | — |
| 1.3.1 | Info and Relationships | A | passed | — | — |
| 1.3.2 | Meaningful Sequence | A | passed | — | — |
| 1.3.3 | Sensory Characteristics | A | passed | — | — |
| 1.4.1 | Use of Color | A | passed | — | — |
| 1.4.2 | Audio Control | A | inapplicable — no auto-playing audio | — | — |
| 2.1.1 | Keyboard | A | failed in S02 and S03 — schedule-grid cells and the shift-swap dialog's shift picker are not reachable or operable by keyboard; passed in every other sample | S02, S03 | a11y_grid_cells_keyboard |
| 2.1.2 | No Keyboard Trap | A | passed | — | — |
| 2.1.4 | Character Key Shortcuts | A | inapplicable — no character-key shortcuts implemented | — | — |
| 2.2.1 | Timing Adjustable | A | passed | — | — |
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
| 4.1.1 | Parsing | A | inapplicable — criterion removed in WCAG 2.2; the VPAT 2.5 catalog retains the row | — | — |
| 4.1.2 | Name, Role, Value | A | passed | — | — |
| 1.2.4 | Captions (Live) | AA | inapplicable — no live media exists in any sampled view | — | — |
| 1.2.5 | Audio Description (Prerecorded) | AA | passed — the S06 walkthrough videos' audio already describes all visual information | — | — |
| 1.3.4 | Orientation | AA | passed | — | — |
| 1.3.5 | Identify Input Purpose | AA | passed | — | — |
| 1.4.3 | Contrast (Minimum) | AA | failed in every sample — the product-wide body text renders at 3.2:1 (brand gray on white) across S01–S06 and R01 | S01–S06, R01 (all) | a11y_body_text_contrast |
| 1.4.4 | Resize text | AA | passed | — | — |
| 1.4.5 | Images of Text | AA | passed | — | — |
| 1.4.10 | Reflow | AA | passed | — | — |
| 1.4.11 | Non-text Contrast | AA | passed | — | — |
| 1.4.12 | Text Spacing | AA | passed | — | — |
| 1.4.13 | Content on Hover or Focus | AA | passed | — | — |
| 2.4.5 | Multiple Ways | AA | passed | — | — |
| 2.4.6 | Headings and Labels | AA | passed | — | — |
| 2.4.7 | Focus Visible | AA | failed in S02 — the schedule grid suppresses the focus indicator exactly as the vendor's ACR discloses; passed in every other sample | S02 | a11y_grid_focus_invisible |
| 2.4.11 | Focus Not Obscured (Minimum) | AA | passed | — | — |
| 2.5.7 | Dragging Movements | AA | passed | — | — |
| 2.5.8 | Target Size (Minimum) | AA | passed | — | — |
| 3.1.2 | Language of Parts | AA | passed — Spanish UI fragments are language-marked across all samples | — | — |
| 3.2.3 | Consistent Navigation | AA | passed | — | — |
| 3.2.4 | Consistent Identification | AA | passed | — | — |
| 3.3.3 | Error Suggestion | AA | passed — field-level suggestions present on every form including the timeclock (the vendor's disclosed defect is no longer observable in v9.3) | — | — |
| 3.3.4 | Error Prevention (Legal, Financial, Data) | AA | passed | — | — |
| 3.3.8 | Accessible Authentication (Minimum) | AA | untested at this scope — the staff SSO sign-in enclave (city IdP) is production-only and was excluded by the commissioner; no authentication flow was exercisable in the demo tenant | — | — |
| 4.1.3 | Status Messages | AA | passed | — | — |

AAA criteria: not evaluated at this scope (verification target WCAG 2.2
AA); the vendor ACR makes no AAA claims either.

### Findings on file (evidence-finding contract, abbreviated)

```
finding_id: a11y_grid_cells_keyboard
fingerprint: 6e3a91d7
severity: CRITICAL
wcag_or_apg: WCAG 2.1.1 Keyboard
evaluation_context: evaluation_id=mar-2026v1; sample_id=S02 (also S03); process_id=P01/default-sequence
evidence: schedule-grid cells receive no focus; shift-swap picker operable only by pointer; a keyboard-only scheduler cannot pick up a shift (driven session step_0027)
```

```
finding_id: a11y_body_text_contrast
fingerprint: 4c88be02
severity: MAJOR
wcag_or_apg: WCAG 1.4.3 Contrast (Minimum)
evaluation_context: evaluation_id=mar-2026v1; sample_id=S01 (product-wide body text — every sample)
evidence: brand gray #8a8f98 on white measures 3.2:1 against the 4.5:1 requirement; present in all samples
```

```
finding_id: a11y_training_video_captions
fingerprint: d17f5c40
severity: MAJOR
wcag_or_apg: WCAG 1.2.2 Captions (Prerecorded)
evaluation_context: evaluation_id=mar-2026v1; sample_id=S06
evidence: three onboarding walkthrough videos carry no captions and no caption toggle; the audio narrates the visuals fully (relevant to 1.2.3/1.2.5, which pass)
```

```
finding_id: a11y_grid_focus_invisible
fingerprint: 0b264ae9
severity: MAJOR
wcag_or_apg: WCAG 2.4.7 Focus Visible
evaluation_context: evaluation_id=mar-2026v1; sample_id=S02
evidence: the schedule grid sets outline:none with no replacement indicator — the defect the vendor's own ACR discloses, still present in v9.3
```

### Coverage boundary

The staff SSO sign-in enclave (city IdP) — excluded by the commissioner;
production-only, not provisionable in the demo tenant; no method covered
it. Everything else in scope is a web view reachable by the web
measurement stack.

## Catalog frame — `2.5-edition-wcag-2.2-508-en` (from the pinned @openacr/openacr@0.3.8 package)

Adherence terms (catalog `terms:`): `supports`; `partially-supports`;
`does-not-support`; `not-applicable`; `not-evaluated` ("can only be used
in WCAG Level AAA criteria"). The A/AA criterion list is exactly the SC
column of the verification outcome table above (32 Level A + 24 Level AA,
including 4.1.1, which WCAG 2.2 removed and the VPAT 2.5 catalog retains).
