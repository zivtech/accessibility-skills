# Input: ACR drift request — ShiftLine Workforce Scheduling (vendor ACR 9.3 → 9.6)

Both documents below are the vendor's own. Report what changed between
them, in Markdown, followed by the handoff note for the procurement owner.

---

## Engagement record

- **Commissioner:** City of Marlow, IT Procurement. ShiftLine's original
  bid arrived with the v9.3 ACR on 2026-06-30. The vendor submitted an
  updated ACR for v9.6 with its contract-renewal packet on 2027-01-15,
  and procurement asked what changed between the two documents before the
  renewal review.
- **Subject product:** ShiftLine Workforce Scheduling — a third-party
  product. Both documents were authored by the vendor's own accessibility
  office.
- **Available evidence for this request: the two documents below, and
  nothing else.** No evaluation of v9.6 has been commissioned; no sample
  was drawn; no testing session was run. The city holds no fingerprints
  for either document.
- The city's earlier verification engagement (`mar-2026v1`, a WCAG-EM
  sample of the v9.3 demo tenant) is closed and its findings are not in
  scope for this request; the renewal review covers the documents.

## Prior document — vendor ACR for v9.3 (received 2026-06-30, verbatim)

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

## Current document — vendor ACR for v9.6 (received 2027-01-15, verbatim)

```yaml
title: ShiftLine Workforce Scheduling Accessibility Conformance Report
product:
  name: ShiftLine Workforce Scheduling
  version: "9.6"
author:
  name: Accessibility Office
  email: acr@shiftline.example
report_date: "2027-01-08"
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
              notes: "Full keyboard operation across the application; the schedule grid was rebuilt in 9.5."
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
              level: partially-supports
              notes: "Body text on the reporting dashboard does not meet the 4.5:1 minimum; remediation planned for v9.7."
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
              level: supports
              notes: "The schedule grid focus indicator was rebuilt in 9.5."
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
              level: supports
              notes: "Language of parts is marked throughout."
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
              level: supports
              notes: "Error suggestions were added to the timeclock form in 9.4."
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

## Catalog frame — `2.5-edition-wcag-2.2-508-en` (from the pinned @openacr/openacr@0.3.8 package)

Adherence terms (catalog `terms:`): `supports`; `partially-supports`;
`does-not-support`; `not-applicable`; `not-evaluated` ("can only be used
in WCAG Level AAA criteria"). Both documents declare this catalog. Its
A/AA criterion list is 32 Level A + 24 Level AA: 1.1.1, 1.2.1, 1.2.2, 1.2.3, 1.3.1, 1.3.2, 1.3.3, 1.4.1, 1.4.2, 2.1.1, 2.1.2, 2.1.4, 2.2.1, 2.2.2, 2.3.1, 2.4.1, 2.4.2, 2.4.3, 2.4.4, 2.5.1, 2.5.2, 2.5.3, 2.5.4, 3.1.1, 3.2.1, 3.2.2, 3.2.6, 3.3.1, 3.3.2, 3.3.7, 4.1.1, 4.1.2
(Level A) and 1.2.4, 1.2.5, 1.3.4, 1.3.5, 1.4.3, 1.4.4, 1.4.5, 1.4.10, 1.4.11, 1.4.12, 1.4.13, 2.4.5, 2.4.6, 2.4.7, 2.4.11, 2.5.7, 2.5.8, 3.1.2, 3.2.3, 3.2.4, 3.3.3, 3.3.4, 3.3.8, 4.1.3 (Level AA), including 4.1.1, which
WCAG 2.2 removed and the VPAT 2.5 catalog retains.
