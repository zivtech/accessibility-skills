# Input: ACR drift request — RiverCity Metro Rider Portal (rcm-2026q3 → rcm-2027q1)

Both documents below are finished and delivered. Report what changed
between them, in Markdown, followed by the handoff note for the engagement
owner.

---

## Engagement record

- **Commissioner:** RiverCity Metro Authority, Office of Civil Rights —
  the Authority publishes an ACR per major release and asked its evaluator
  what moved between the 2026.3 and 2027.1 reports.
- **Evaluator (both cycles):** Meridian Digital Accessibility (reporting
  lead: Dana Okafor; dana.okafor@meridian-a11y.example).
- **Prior cycle:** evaluation_id `rcm-2026q3`, window 2026-06-22 →
  2026-07-28. **Current cycle:** evaluation_id `rcm-2027q1`, window
  2027-01-12 → 2027-02-19. Conformance target both cycles: WCAG 2.2
  Level AA, web component, catalog `2.5-edition-wcag-2.2-508-en`.
- Both ACRs were produced by this engagement from this evaluator's own
  evidence spine; the adherence notes carry this engagement's
  `finding_id` and `fingerprint` values.
- No third-party document is involved. Nothing new was tested for this
  request — the current cycle's evaluation is finished and is quoted
  below as delivered.

## Prior document — rcm-2026q3 ACR (issued 2026-07-28, verbatim)

```yaml
title: RiverCity Metro Rider Portal Accessibility Conformance Report
product:
  name: RiverCity Metro Rider Portal
  version: "2026.3"
author:
  name: Dana Okafor
  email: dana.okafor@meridian-a11y.example
  company_name: Meridian Digital Accessibility
report_date: "2026-07-28"
version: 1
evaluation_methods_used: "WCAG-EM 2.0; 11 structured + 1 random samples + 2 complete processes"
legal_disclaimer: "Draft for review — not a legally binding conformance claim until reviewed and issued by RiverCity Metro Authority."
notes: "Web component only — the evaluation method is a web measurement stack (WCAG-EM 2.0); non-web surfaces are covered in the disabled chapters' boundary notes."
catalog: 2.5-edition-wcag-2.2-508-en
chapters:
  success_criteria_level_a:
    criteria:
      - num: "1.1.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.2.1"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no audio or video content exists in any sampled view."
      - num: "1.2.2"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no media."
      - num: "1.2.3"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no media."
      - num: "1.3.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.3.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.3.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.2"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no auto-playing audio."
      - num: "2.1.1"
        components:
          - name: web
            adherence:
              level: partially-supports
              notes: "Sample-scoped: fails in S07 (checkout, both P01 branches). finding_id: a11y_fare_zone_slider_keyboard (fingerprint 7c1f22ab)."
      - num: "2.1.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.1.4"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no character-key shortcuts implemented."
      - num: "2.2.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.2.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.3.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.1"
        components:
          - name: web
            adherence:
              level: partially-supports
              notes: "Sample-scoped: fails in R01 and S11 (legacy info-page template). finding_id: a11y_legacy_skiplink_anchor (fingerprint 5f77ab02)."
      - num: "2.4.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.4"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no motion-actuated functions."
      - num: "3.1.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.2.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.2.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.2.6"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.3.1"
        components:
          - name: web
            adherence:
              level: partially-supports
              notes: "Sample-scoped: fails in S07 (P01 declined-payment branch). finding_id: a11y_payment_error_association (fingerprint c30e51f9)."
      - num: "3.3.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.3.7"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "4.1.1"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: criterion removed in WCAG 2.2; the VPAT 2.5 catalog retains the row."
      - num: "4.1.2"
        components:
          - name: web
            adherence:
              level: partially-supports
              notes: "Sample-scoped: fails in S02 (trip planner). finding_id: a11y_swap_button_name (fingerprint 91d4e0c3)."
  success_criteria_level_aa:
    criteria:
      - num: "1.2.4"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no media."
      - num: "1.2.5"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no media."
      - num: "1.3.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.3.5"
        components:
          - name: web
            adherence:
              level: does-not-support
              notes: "Sample-scoped: fails in S07 and S08 — every sample where input-purpose fields exist. finding_id: a11y_form_autocomplete_missing (fingerprint 44b09ce6)."
      - num: "1.4.3"
        components:
          - name: web
            adherence:
              level: partially-supports
              notes: "Sample-scoped: fails in S03 and S09. finding_id: a11y_route_badge_contrast (fingerprint 2ab9d871)."
      - num: "1.4.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.5"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.10"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.11"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.12"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.13"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.5"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.6"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.7"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.11"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.7"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.8"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.1.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.2.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.2.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.3.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.3.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.3.8"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "4.1.3"
        components:
          - name: web
            adherence:
              level: partially-supports
              notes: "Sample-scoped: fails in S07 (P01 purchase confirmation). finding_id: a11y_purchase_confirm_silent (fingerprint e8c2447d)."
  success_criteria_level_aaa:
    notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    criteria: []
  functional_performance_criteria:
    disabled: true
    notes: "Outside the web evaluation method's coverage: the RideRC native app and the monthly PDF timetables were covered by manual AT and document sessions; conclusions for those surfaces are the Authority's to make."
  hardware:
    disabled: true
    notes: "Outside the web evaluation method's coverage: no hardware surfaces are in scope (fare validators belong to a separate procurement)."
  software:
    disabled: true
    notes: "Outside the web evaluation method's coverage: the RideRC native app is non-web software, covered by a manual AT session outside this method."
  support_documentation_and_services:
    disabled: true
    notes: "Outside the web evaluation method's coverage: no support-documentation surfaces were evaluated."
```

## Current document — rcm-2027q1 ACR (issued 2027-02-19, verbatim)

```yaml
title: RiverCity Metro Rider Portal Accessibility Conformance Report
product:
  name: RiverCity Metro Rider Portal
  version: "2027.1"
author:
  name: Dana Okafor
  email: dana.okafor@meridian-a11y.example
  company_name: Meridian Digital Accessibility
report_date: "2027-02-19"
version: 2
evaluation_methods_used: "WCAG-EM 2.0 re-evaluation; 11 structured + 1 random samples + 2 complete processes; 7 structured samples and P01 carried over from rcm-2026q3 for comparability"
legal_disclaimer: "Draft for review — not a legally binding conformance claim until reviewed and issued by RiverCity Metro Authority."
notes: "Web component only — the evaluation method is a web measurement stack (WCAG-EM 2.0); non-web surfaces are covered in the disabled chapters' boundary notes."
catalog: 2.5-edition-wcag-2.2-508-en
chapters:
  success_criteria_level_a:
    criteria:
      - num: "1.1.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.2.1"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no audio or video content exists in any sampled view."
      - num: "1.2.2"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no media."
      - num: "1.2.3"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no media."
      - num: "1.3.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.3.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.3.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.2"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no auto-playing audio."
      - num: "2.1.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.1.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.1.4"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no character-key shortcuts implemented."
      - num: "2.2.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.2.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.3.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.1"
        components:
          - name: web
            adherence:
              level: does-not-support
              notes: "Sample-scoped: fails in S03, S06, S11, S12, S15 and R02 — every template now built on the legacy shell. finding_id: a11y_legacy_skiplink_anchor (fingerprint 5f77ab02)."
      - num: "2.4.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.4"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no motion-actuated functions."
      - num: "3.1.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.2.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.2.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.2.6"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.3.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.3.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.3.7"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "4.1.1"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: criterion removed in WCAG 2.2; the VPAT 2.5 catalog retains the row."
      - num: "4.1.2"
        components:
          - name: web
            adherence:
              level: partially-supports
              notes: "Sample-scoped: fails in S02 (trip planner). finding_id: a11y_swap_button_name (fingerprint 91d4e0c3)."
  success_criteria_level_aa:
    criteria:
      - num: "1.2.4"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no media."
      - num: "1.2.5"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no media."
      - num: "1.3.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.3.5"
        components:
          - name: web
            adherence:
              level: partially-supports
              notes: "Sample-scoped: fails in S08 (paratransit application form). finding_id: a11y_form_autocomplete_missing (fingerprint 44b09ce6)."
      - num: "1.4.3"
        components:
          - name: web
            adherence:
              level: partially-supports
              notes: "Sample-scoped: fails in S03 and S15. finding_id: a11y_route_badge_contrast (fingerprint 2ab9d871)."
      - num: "1.4.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.5"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.10"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.11"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.12"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.13"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.5"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.6"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.7"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.11"
        components:
          - name: web
            adherence:
              level: partially-supports
              notes: "Sample-scoped: fails in S14 (station detail). finding_id: a11y_sticky_filterbar_obscures_focus (fingerprint 3d90c7e1)."
      - num: "2.5.7"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.8"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.1.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.2.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.2.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.3.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.3.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "3.3.8"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
      - num: "4.1.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 11 structured + 1 random samples (WCAG-EM)."
  success_criteria_level_aaa:
    notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    criteria: []
  functional_performance_criteria:
    disabled: true
    notes: "Outside the web evaluation method's coverage: the RideRC native app and the monthly PDF timetables were covered by manual AT and document sessions; conclusions for those surfaces are the Authority's to make."
  hardware:
    disabled: true
    notes: "Outside the web evaluation method's coverage: no hardware surfaces are in scope (fare validators belong to a separate procurement)."
  software:
    disabled: true
    notes: "Outside the web evaluation method's coverage: the RideRC native app is non-web software, covered by a manual AT session outside this method."
  support_documentation_and_services:
    disabled: true
    notes: "Outside the web evaluation method's coverage: no support-documentation surfaces were evaluated."
```

## Sample sets, both cycles (from the two engagement records)

**rcm-2026q3** — structured (11): S01 home, S02 trip planner, S03 route
schedule, S04 service alerts, S05 fares, S06 account dashboard, S07
checkout steps 1-2, S08 contact + paratransit application form, S09 news
article, S10 accessibility policy, S11 title-vi (legacy info-page
template). Random (1): R01 /riders/lost-and-found, seeded shuffle of the
214-URL sitemap, seed 7391. Complete processes (2): P01 plan trip → buy
monthly pass → confirmation (web; default + declined-payment branch);
P02 activate a ticket in the RideRC native app (non-web).

**rcm-2027q1** — structured (11): S01 home, S02 trip planner, S03 route
schedule, S06 account dashboard, S07 checkout steps 1-2, S08 contact +
paratransit application form, S11 title-vi (legacy info-page template),
S12 alerts subscription (template shipped 2026-11), S13 fare calculator
(rebuilt 2026-10, replacing the 2026 fares page), S14 station detail
(template shipped 2026-12), S15 news index (replacing the 2026 news
article template). Random (1): R02 /riders/bike-racks, seeded shuffle of
the 251-URL sitemap, seed 8815. Complete processes (2): P01 plan trip →
buy monthly pass → confirmation (default + declined-payment branch); P02
activate a ticket in the RideRC native app (non-web).

Per WCAG-EM re-evaluation guidance the current cycle retained a sub-set of
the prior sample and replaced a sub-set: **carried over** — S01, S02, S03,
S06, S07, S08, S11, and both complete processes; **retired** — S04, S05,
S09, S10, R01; **added** — S12, S13, S14, S15, R02.

Accessibility support baseline, both cycles: NVDA 2026.1 + Firefox 141
(Windows 11); VoiceOver + Safari 18 (macOS 15); TalkBack 15 + Chrome
(Android 15); keyboard-only without a screen reader.

## rcm-2027q1 evidence — re-check of every prior-cycle fingerprint

Each finding carried by the prior ACR was re-checked in the current
cycle. This table is the current evaluation's evidence as delivered; no
further testing was performed for this drift request.

| finding_id | fingerprint | Prior severity | Re-check result in rcm-2027q1 |
|---|---|---|---|
| a11y_fare_zone_slider_keyboard | 7c1f22ab | CRITICAL | Verified absent. The S07 fare-zone slider now exposes a stepper with full keyboard operation; re-tested in both P01 branches and in a driven keyboard session. |
| a11y_payment_error_association | c30e51f9 | MAJOR | Verified absent. The declined-payment message is announced and programmatically associated with its field (P01 error branch). |
| a11y_purchase_confirm_silent | e8c2447d | MAJOR | Verified absent. The purchase confirmation renders into a live region and was announced in the driven session (P01 default branch). |
| a11y_route_badge_contrast | 2ab9d871 | MAJOR | Still present. Fails in S03, and in S15, which reuses the same route-badge component. Measured 2.8:1 against 4.5:1 — the same component, the same measurement, the same severity as the prior cycle. |
| a11y_swap_button_name | 91d4e0c3 | MINOR | Still present. S02 icon-only swap control, unchanged in scope and severity; the origin and destination fields remain directly editable. |
| a11y_form_autocomplete_missing | 44b09ce6 | MAJOR | Still present, on a smaller surface. The S07 checkout form now carries autocomplete tokens on every applicable field; the S08 paratransit application form still carries none. Severity MAJOR, unchanged. |
| a11y_legacy_skiplink_anchor | 5f77ab02 | MINOR | Still present, on a larger surface. The legacy info-page shell was rolled out across the schedules and account areas in 2026-11: the missing skip-link target now fails in S03, S06, S11, S12, S15 and R02 — the majority of the sample, including two templates that passed this criterion in the prior cycle (S03, S06). Severity raised to MAJOR. |
| a11y_sticky_filterbar_obscures_focus | 3d90c7e1 | — | First observed this cycle. The sticky filter bar on the S14 station-detail template (shipped 2026-12) covers focused rows in the departures table. Severity MAJOR. S14 has no counterpart in the rcm-2026q3 sample. |

## Catalog frame — `2.5-edition-wcag-2.2-508-en` (from the pinned @openacr/openacr@0.3.8 package)

Adherence terms (catalog `terms:`): `supports`; `partially-supports`;
`does-not-support`; `not-applicable`; `not-evaluated` ("can only be used
in WCAG Level AAA criteria"). Both documents use this catalog; the A/AA
criterion list is exactly the criteria carried by the two documents above
(32 Level A + 24 Level AA, including 4.1.1, which WCAG 2.2 removed and the
VPAT 2.5 catalog retains).
