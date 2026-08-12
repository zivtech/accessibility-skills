# Input: ACR claims-verification request — Lumen Courseware (lum-2026v1)

The verification engagement below is finished. Compare each Level A/AA web
claim in the vendor's ACR against the verification evidence and return the
engagement's verification report in Markdown, followed by the handoff note
for the procurement owner.

---

## Engagement record

- **Commissioner:** Ridgeline Community College District, Procurement —
  evaluating Lumen Courseware for a learning-management contract. The
  vendor's ACR (below) arrived with the bid on 2026-07-02.
- **Verifying evaluator:** Hazelwood Digital Access (reporting lead: Imani
  Cole; imani.cole@hazelwooddigital.example).
- **Verification engagement:** lum-2026v1, window 2026-07-27 → 2026-08-08,
  WCAG-EM 2.0 sample of the vendor's demo tenant
  (ridgeline-demo.lumencourseware.example). Conformance target for
  verification: WCAG 2.2 Level AA, web component. No exclusions — every
  in-scope surface was reachable, including the demo-tenant sign-in.
- **Subject product:** Lumen Courseware, version 5.1 (the version the
  vendor's ACR claims to describe).
- The subject ACR is a third-party document: this engagement holds no
  prior fingerprints for it and no earlier verification of this product.

## Subject: the vendor's ACR (received 2026-07-02, verbatim)

```yaml
title: Lumen Courseware Accessibility Conformance Report
product:
  name: Lumen Courseware
  version: "5.1"
author:
  name: Accessibility Office
  email: accessibility@lumencourseware.example
report_date: "2026-06-25"
catalog: 2.5-edition-wcag-2.2-508-en
chapters:
  success_criteria_level_a:
    criteria:
      - num: "1.1.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "1.2.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "1.2.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "All lesson videos carry closed captions."
      - num: "1.2.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Lesson videos provide transcripts as a media alternative."
      - num: "1.3.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "1.3.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "1.3.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "1.4.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "1.4.2"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "No auto-playing audio; lesson media starts only on user action."
      - num: "2.1.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "2.1.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
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
              notes: "Supported."
      - num: "2.2.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "2.3.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "2.4.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "2.4.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "2.4.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "2.4.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "2.5.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "2.5.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "2.5.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
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
              notes: "Supported."
      - num: "3.2.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "3.2.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "3.2.6"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "3.3.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "3.3.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "3.3.7"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
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
              notes: "Supported."
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
              level: supports
              notes: "Lesson videos carry audio description tracks where visual-only content appears."
      - num: "1.3.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "1.3.5"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "1.4.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "1.4.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "1.4.5"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "1.4.10"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "1.4.11"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "1.4.12"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "1.4.13"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "2.4.5"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "2.4.6"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "2.4.7"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "2.4.11"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "2.5.7"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "2.5.8"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "3.1.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "3.2.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "3.2.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "3.3.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "3.3.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "3.3.8"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
      - num: "4.1.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Supported."
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

## Verification evidence (delivered 2026-08-08, contract-conformant)

### Sample set

Structured samples (5): S01 course catalog, S02 course page, S03 lesson
player (video + captions + transcript), S04 quiz, S05 gradebook. Random
sample (1): R01 /help/keyboard-shortcuts-overview — seeded shuffle of the
48-URL demo sitemap, seed 2917; the comparison surfaced no new content
types or finding types. Complete process (1): P01 enroll → complete a
lesson → submit the quiz (default + wrong-answer branch; traverses
S02/S03/S04). State coverage per sample: default, loading, error, and
expanded states where the template has them. Accessibility support
baseline: NVDA 2026.1 + Firefox 141 (Windows 11); VoiceOver + Safari 18
(macOS 15); keyboard-only without a screen reader.

### Outcomes — web component, per SC across the verification sample

Every Level A and Level AA criterion was verified. No criterion failed in
any sample; no criterion was left untested; nothing returned cantTell. No
findings were filed — the evidence contract forbids findings for passing
checks.

| SC | Name | Level | Verification outcome across samples | Failing samples | finding_id(s) |
|----|------|-------|-------------------------------------|-----------------|---------------|
| 1.1.1 | Non-text Content | A | passed | — | — |
| 1.2.1 | Audio-only and Video-only (Prerecorded) | A | passed | — | — |
| 1.2.2 | Captions (Prerecorded) | A | passed — every sampled lesson video carries accurate closed captions | — | — |
| 1.2.3 | Audio Description or Media Alternative (Prerecorded) | A | passed — transcripts present on every sampled lesson | — | — |
| 1.3.1 | Info and Relationships | A | passed | — | — |
| 1.3.2 | Meaningful Sequence | A | passed | — | — |
| 1.3.3 | Sensory Characteristics | A | passed | — | — |
| 1.4.1 | Use of Color | A | passed | — | — |
| 1.4.2 | Audio Control | A | inapplicable — no auto-playing audio; media starts on user action only | — | — |
| 2.1.1 | Keyboard | A | passed | — | — |
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
| 1.2.5 | Audio Description (Prerecorded) | AA | passed — audio description present where visual-only content appears | — | — |
| 1.3.4 | Orientation | AA | passed | — | — |
| 1.3.5 | Identify Input Purpose | AA | passed | — | — |
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
| 2.4.11 | Focus Not Obscured (Minimum) | AA | passed | — | — |
| 2.5.7 | Dragging Movements | AA | passed | — | — |
| 2.5.8 | Target Size (Minimum) | AA | passed | — | — |
| 3.1.2 | Language of Parts | AA | passed | — | — |
| 3.2.3 | Consistent Navigation | AA | passed | — | — |
| 3.2.4 | Consistent Identification | AA | passed | — | — |
| 3.3.3 | Error Suggestion | AA | passed | — | — |
| 3.3.4 | Error Prevention (Legal, Financial, Data) | AA | passed | — | — |
| 3.3.8 | Accessible Authentication (Minimum) | AA | passed | — | — |
| 4.1.3 | Status Messages | AA | passed | — | — |

AAA criteria: not evaluated at this scope (verification target WCAG 2.2
AA); the vendor ACR makes no AAA claims either.

### Findings on file

None. Every claim-relevant check passed; a clean result says so plainly
rather than inventing ritual entries.

### Coverage boundary

None — every in-scope surface is a web view reachable by the web
measurement stack.

## Catalog frame — `2.5-edition-wcag-2.2-508-en` (from the pinned @openacr/openacr@0.3.8 package)

Adherence terms (catalog `terms:`): `supports`; `partially-supports`;
`does-not-support`; `not-applicable`; `not-evaluated` ("can only be used
in WCAG Level AAA criteria"). The A/AA criterion list is exactly the SC
column of the verification outcome table above (32 Level A + 24 Level AA,
including 4.1.1, which WCAG 2.2 removed and the VPAT 2.5 catalog retains).
