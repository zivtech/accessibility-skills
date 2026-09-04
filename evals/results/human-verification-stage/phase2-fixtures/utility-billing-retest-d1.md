```yaml
title: Rivertown Utility Billing Portal Accessibility Conformance Report
product:
  name: Rivertown Utility Billing Portal
  version: 3.2.0
  description: The municipal utility's public bill-pay portal (bill view, autopay enrollment, payment history, outage reporting) at billing.rivertownutilities.example, plus its authenticated account area. The initial audit measured version 3.0.4; the remediation cycle shipped 3.2.0, which is the version this retest evaluated.
author:
  name: Daniel Kowalczyk
  company_name: Halcyon Digital Access
  email: daniel.kowalczyk@halcyondigitalaccess.example
  website: https://halcyondigitalaccess.example
vendor:
  company_name: Rivertown Municipal Utilities, Customer Systems
  email: billing-support@rivertownutilities.example
report_date: '2026-07-24'
version: 2
notes: |-
  INCOMPLETE DRAFT - unattested fix-closures on A/AA criteria: 3.3.1 (rem-payment-error-announce-7c53e0b1), 3.3.2 (rem-autopay-date-label-6f4082e9), 1.4.11 (rem-status-icon-contrast-3b71ac5d), 2.4.7 (rem-account-nav-focus-9e26d4f8)

  These four Level A/AA criteria improved from failed to passed since the 2026-05-20 evaluation (document version 1). Each improvement rests on a fix-closure record whose attestation dates do not reconcile with this report's evaluation window (2026-07-06 to 2026-07-24) or its report_date (2026-07-24), so each is a draft closure. Per the acr-reporting untested/unattested gate, those criteria carry NO adherence entry in this draft and are omitted from the chapters above. The handoff names each item_id, what is missing, and who can close it. This draft is not ready for publication until they are closed or the report is re-issued.

  No Level A or AA criterion in this evaluation is untested or cantTell: every catalog A/AA criterion is either present with a term above or named on the unattested-fix-closures line. There is no untested-criteria marker on this draft.

  Scope and method: this report serializes a finished WCAG-EM 2.0 re-evaluation (retest) of Rivertown Utility Billing Portal 3.2.0, conducted 2026-07-06 to 2026-07-24, superseding the 2026-05-20 draft (OpenACR document version 1). Only the web component is populated. Non-web components (electronic documents, software, authoring tool) are omitted from every criterion entry because the evaluation method is web-only; conclusions for them are human-owned and are not asserted here.

  Out-of-web-component evidence carried by the engagement but not claimed above: the quarterly rate-adjustment notice PDF (Q3 2026 edition, PDF 1.7, distributed from billing.rivertownutilities.example) ships untagged - no structural tags, no programmatic reading order - per a manual document check on 2026-05-12, unchanged this cycle and outside the remediation scope. It is electronic-document evidence and is recorded in the evaluation report, not in this draft's web adherence entries.

  Orthogonality: every adherence term above is derived only from the evaluation report's per-SC outcome map aggregated across the sample set. Finding severity, remediation activity, and the presence of a proposed or landed fix never select or upgrade a term; impact language appears in notes only.

  Sampling boundary: the claims above are sample-scoped (7 structured samples S01-S07, 1 random sample R01, 1 complete process P01). Sampling alone does not support a whole-product conformance claim.
evaluation_methods_used: 'WCAG-EM 2.0 re-evaluation (retest of the 2026-05-20 evaluation), conducted 2026-07-06 to 2026-07-24. Sample set: 7 structured samples (S01 bill summary / home dashboard; S02 view current bill; S03 payment portal; S04 autopay enrollment and management; S05 payment history; S06 account profile / contact info; S07 outage reporting and service requests) + 1 random sample (R01 /billing/help/faq, seeded shuffle of the 96-URL sitemap, seed 1147, comparison surfaced no new content or finding types) + 1 complete process (P01 log in, view current bill, pay now, confirmation, traversing S01/S02/S03). State coverage per sample: default, loading, error, and expanded states where the template has them. The retest retained the May frame rather than resampling, with a full re-pass on the samples touching the prior findings and a representativeness recheck on the rest. Automated and manual testing against the declared accessibility-support baseline: NVDA 2026.1 + Firefox 141 (Windows 11); VoiceOver + Safari 18 (macOS 15); keyboard-only without a screen reader. Technologies relied upon: HTML, CSS, JavaScript (React), WAI-ARIA.'
legal_disclaimer: 'DRAFT FOR REVIEW - not a legally binding conformance claim, and not a signed or final Accessibility Conformance Report. This document is an INCOMPLETE DRAFT: four Level A/AA criteria carry no adherence entry because the fix-closure records their improved outcomes rest on are not fully attested (see the report notes). It becomes a conformance claim only when reviewed and issued by Rivertown Municipal Utilities, Customer Systems, the party responsible for the product. Until then no statement in it may be made to a third party, and the accessibility conformance of Rivertown Utility Billing Portal 3.2.0 is not represented by it.'
feedback: https://billing.rivertownutilities.example/accessibility-feedback
catalog: 2.5-edition-wcag-2.2-508-en
chapters:
  success_criteria_level_a:
    notes: 'Web component only. Two Level A criteria carry no adherence entry in this draft: 3.3.1 Error Identification (closure rem-payment-error-announce-7c53e0b1) and 3.3.2 Labels or Instructions (closure rem-autopay-date-label-6f4082e9). Both improved from failed to passed since the 2026-05-20 evaluation and both improvements rest on fix-closure records that are not fully attested - see the INCOMPLETE DRAFT marker in the report notes and the handoff.'
    criteria:
    - num: 1.1.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 1.2.1
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no audio-only or video-only content exists in any sampled view (7 structured + 1 random samples).'
    - num: 1.2.2
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no media content exists in any sampled view (7 structured + 1 random samples).'
    - num: 1.2.3
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no media content exists in any sampled view (7 structured + 1 random samples).'
    - num: 1.3.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM). This entry covers the web component only; the quarterly rate-adjustment notice PDF is electronic-document evidence outside the web measurement stack and is not part of this claim - see the report notes.'
    - num: 1.3.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 1.3.3
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 1.4.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 1.4.2
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no auto-playing audio exists in any sampled view (7 structured + 1 random samples).'
    - num: 2.1.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM). Complete process P01 (log in, view current bill, pay now, confirmation) is fully keyboard-operable.'
    - num: 2.1.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 2.1.4
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no character-key shortcuts are implemented in any sampled view (7 structured + 1 random samples).'
    - num: 2.2.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 2.2.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 2.3.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.3
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.4
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 2.5.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 2.5.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 2.5.3
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 2.5.4
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no motion-actuated functions exist in any sampled view (7 structured + 1 random samples).'
    - num: 3.1.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 3.2.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 3.2.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 3.2.6
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 3.3.7
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM). Complete process P01 re-uses entered account and payment data rather than requiring re-entry.'
    - num: 4.1.1
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: success criterion 4.1.1 Parsing was removed from WCAG 2.2 and carries no applicable requirement at this engagement''s conformance target (WCAG 2.2 Level AA); the VPAT 2.5 catalog retains the row. No content type is measured against it.'
    - num: 4.1.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM). Remediated since the prior evaluation: a11y_billing_paybutton_unlabeled (fingerprint 5e1a92c7) resolved; closure rem-paybutton-name-4a8f21c6 attested and second-confirmed at 3.2.0.'
  success_criteria_level_aa:
    notes: 'Web component only. Two Level AA criteria carry no adherence entry in this draft: 1.4.11 Non-text Contrast (closure rem-status-icon-contrast-3b71ac5d) and 2.4.7 Focus Visible (closure rem-account-nav-focus-9e26d4f8). Both improved from failed to passed since the 2026-05-20 evaluation and both improvements rest on fix-closure records that are not fully attested - see the INCOMPLETE DRAFT marker in the report notes and the handoff. 1.4.3 Contrast (Minimum) keeps its entry above: it is still failing in S06 and a disclosed failure is never dropped from a conformance document.'
    criteria:
    - num: 1.2.4
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no live media exists in any sampled view (7 structured + 1 random samples).'
    - num: 1.2.5
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no prerecorded media exists in any sampled view (7 structured + 1 random samples).'
    - num: 1.3.4
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 1.3.5
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM). Autocomplete tokens are present on the account-profile input fields (S06).'
    - num: 1.4.3
      components:
      - name: web
        adherence:
          level: partially-supports
          notes: 'Sample-scoped: fails in S06. Failing sample: S06 account profile / contact info - the account-page footer links measure 3.9:1 against the page background where 4.5:1 is required for normal text; finding a11y_billing_footer_link_contrast (fingerprint 3d0c7f61), open and unremediated this cycle. Passes in S01, S02, S03, S04, S05, S07 and in random sample R01. At the 2026-05-20 evaluation this criterion also failed in S03; that Pay Now call-to-action defect (finding a11y_billing_cta_button_contrast, fingerprint e4b1266a) is reported fixed at 3.2.0, but rem-cta-contrast-2d95f716 resolved but not attested - its second confirmation is dated 2026-07-25, after this report''s report_date of 2026-07-24 - so the narrowing of the failing-sample list from (S03, S06) to (S06) is disclosed here rather than attested. The still-open S06 failure keeps this entry.'
    - num: 1.4.4
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 1.4.5
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 1.4.10
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 1.4.12
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 1.4.13
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.5
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.6
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.11
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 2.5.7
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 2.5.8
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 3.1.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 3.2.3
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 3.2.4
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 3.3.3
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 3.3.4
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
    - num: 3.3.8
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM). Password managers are supported and no cognitive function test is imposed (P01).'
    - num: 4.1.3
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).'
  success_criteria_level_aaa:
    notes: AAA criteria were not evaluated. The engagement's conformance target is WCAG 2.2 Level AA and no Level AAA evidence was collected.
    criteria:
    - num: 1.2.6
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 1.2.7
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 1.2.8
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 1.2.9
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 1.3.6
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 1.4.6
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 1.4.7
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 1.4.8
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 1.4.9
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 2.1.3
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 2.2.3
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 2.2.4
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 2.2.5
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 2.2.6
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 2.3.2
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 2.3.3
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 2.4.8
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 2.4.9
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 2.4.10
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 2.4.12
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 2.4.13
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 2.5.5
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 2.5.6
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 3.1.3
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 3.1.4
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 3.1.5
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 3.1.6
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 3.2.5
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 3.3.5
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 3.3.6
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
    - num: 3.3.9
      components:
      - name: web
        adherence:
          level: not-evaluated
          notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
  functional_performance_criteria:
    disabled: true
    notes: 'Outside the web evaluation method''s coverage: the Revised Section 508 functional performance criteria (302.1-302.9) were not evaluated. This engagement''s conformance target is WCAG 2.2 Level AA and its method is WCAG-EM 2.0 applied to web content; no functional-performance assessment was performed and nothing else in the engagement covered it. Conclusions in this chapter are human-owned and are not asserted by this draft.'
  hardware:
    disabled: true
    notes: 'Outside the web evaluation method''s coverage: no hardware is in scope. The product is a web portal with no native application, kiosk, or hardware surface, and the evaluation scope declares no exclusions in this area. Nothing was measured here and nothing else covered it.'
  software:
    disabled: true
    notes: 'Outside the web evaluation method''s coverage: no non-web software surface is in scope. No native applications and no kiosks were evaluated. Nothing was measured here and nothing else covered it.'
  support_documentation_and_services:
    disabled: true
    notes: 'Outside the web evaluation method''s coverage: support documentation and services (602.2-603.3) were not in scope for this engagement and were not measured. Nothing else covered them. The one non-web artifact the engagement examined - the quarterly rate-adjustment notice PDF - is product content, not support documentation; its manual document check is recorded as electronic-document evidence in the evaluation report and in the report notes above.'
```

---

# Handoff — Rivertown Utility Billing Portal DRAFT ACR (OpenACR)

**Status: INCOMPLETE DRAFT.** Not a final ACR, not signed, not publishable as-is. Four Level A/AA criteria carry no adherence entry.

## 1. Finish surface

Catalog `2.5-edition-wcag-2.2-508-en` (WCAG 2.2 edition), per the audit plan's report-template requirement. Finish surface is **YAML + CLI-rendered HTML**, reviewed directly.

Do **not** route this draft to acreditor.section508.gov: the GSA ACR Editor cannot import 2.2-catalog documents today — it rejects them by criterion. Edits go into the YAML; re-validate and re-render after every edit.

Rendering command actually used (both commands passed `-c`; a bare `validate -f` is schema-shape only and a bare `output` silently renders a criteria-less shell):

```
openacr validate -f draft.yaml -c node_modules/@openacr/openacr/catalog/2.5-edition-wcag-2.2-508-en.yaml
openacr output   -f draft.yaml -c node_modules/@openacr/openacr/catalog/2.5-edition-wcag-2.2-508-en.yaml \
  -t node_modules/@openacr/openacr/templates/openacr-html-0.1.0.handlebars -o draft.html
```

## 2. Validation and rendering output (pinned `@openacr/openacr@0.3.8`)

| Step | Command | Result |
|---|---|---|
| Validate | `openacr validate -f … -c …2.5-edition-wcag-2.2-508-en.yaml` | `Valid!` (exit 0) |
| Render | `openacr output -f … -c … -t openacr-html-0.1.0.handlebars -o draft.html` | `Valid and output generated at draft.html!` (exit 0) — 116,221 bytes, 7 tables |

**Cell-level verification of the rendered tables** (schema/catalog validation confirms shape, never that the numbers are right):

| Rendered table | Rows | Adherence cells | Reconciles to report |
|---|---:|---|---|
| Table 1 — Level A | 30 | Supports 23, Not Applicable 7 | 32 catalog criteria − 2 gated (3.3.1, 3.3.2) = 30 ✔ |
| Table 2 — Level AA | 22 | Supports 19, Not Applicable 2, Partially Supports 1 | 24 catalog criteria − 2 gated (1.4.11, 2.4.7) = 22 ✔ |
| Table 3 — Level AAA | 31 | Not Evaluated 31 | full AAA catalog ✔ |
| 508 chapters (FPC / hardware / software / support docs) | — | `disabled: true`, coverage notes rendered | 4 chapters ✔ |

Independent self-checks the CLI does not perform, all run and passing: every catalog A/AA criterion is present-or-gated (52 present + 4 gated = 56); every note begins with its canonical stem for its term; `not-evaluated` appears only in the AAA chapter; no `supports` note cites a `finding_id` except the one remediated criterion; every non-passing entry cites a real `finding_id`; sample counts in `evaluation_methods_used` (7 structured + 1 random + 1 complete process) match the report's sample set exactly; product version `3.2.0` matches every closure's `attested_against.version`.

## 3. INCOMPLETE gaps — four criteria with no adherence entry

There is **no untested-criteria marker** on this draft, and that is correct: every Level A/AA criterion in the report's outcome map carries `passed`, `failed`, or `inapplicable`. Nothing is `untested` or `cantTell`. The single INCOMPLETE marker is the unattested-fix-closures line.

All four gaps have the same cause class — **attestation dates that do not reconcile with the report's own evaluation window (2026-07-06 → 2026-07-24) and `report_date` (2026-07-24)**. Each is a `draft` closure under the fix-closure contract's "dates reconcile" rule, so its criterion's *improved* term is refused. Gap owner in every case: **a named person confirming the fix on 3.2.0 inside a window that closes on or before the report date — not more automated testing.**

| SC | Closure `item_id` | What is missing | Who can close it |
|---|---|---|---|
| 3.3.1 Error Identification | `rem-payment-error-announce-7c53e0b1` | `second_confirmation.at` is 2026-07-26 — **after `report_date` 2026-07-24** and outside the evaluation window. Wendell Ashby looked after the report closed. The primary attestation (Priya Chandrasekaran, 2026-07-16) is in-window and complete. | Needs a human owner: re-date or re-perform the second confirmation inside the window, or re-issue the report with a later `report_date` covering it. |
| 3.3.2 Labels or Instructions | `rem-autopay-date-label-6f4082e9` | `second_confirmation.at` is 2026-07-02 — **before the evaluation window opened** (2026-07-06) and before the fix landed (PR #830, 2026-07-09). Colm Fitzgerald cannot have confirmed this fix on 3.2.0 on that date. | Needs a human owner: a fresh second confirmation on 3.2.0, inside the window. |
| 1.4.11 Non-text Contrast | `rem-status-icon-contrast-3b71ac5d` | `attested_at` is 2026-06-30 — **before the evaluation window opened** and before the fix landed (PR #805, 2026-07-08). Grace Lindqvist's primary attestation predates the change it attests. The second confirmation (Tomas Herrera, 2026-07-10) is in-window. | Needs a human owner: a fresh primary attestation on 3.2.0, inside the window. |
| 2.4.7 Focus Visible | `rem-account-nav-focus-9e26d4f8` | **Both** dates are after `report_date`: `attested_at` 2026-07-27, `second_confirmation.at` 2026-07-28. The entire closure was confirmed after the report closed. | Needs a human owner: re-issue the report with a later `report_date`, or re-confirm inside the current window. |

What each gate does **not** do, stated so the reviewer can check it:

- It does not touch **1.4.3 Contrast (Minimum)**, which is still failing in S06. That criterion keeps its `partially-supports` entry, cites the open finding `a11y_billing_footer_link_contrast`, and names `rem-cta-contrast-2d95f716 resolved but not attested` (second confirmation 2026-07-25, after `report_date`) inside that entry's note. Dropping a disclosed failure out of a conformance document would be worse than disclosing it, so the unattested closure on it is disclosed in place rather than moved to the marker line.
- It does not list **4.1.2 Name, Role, Value**, whose closure `rem-paybutton-name-4a8f21c6` is fully attested. Refusing an attested closure would be over-refusal.
- No SC appears on both INCOMPLETE lines (there is only one line, and an untested criterion has no outcome to improve).

**Secondary observation, not a term-changing finding:** the two contrast closures (`rem-status-icon-contrast-3b71ac5d`, `rem-cta-contrast-2d95f716`) carry `interaction_evidence` (computed-style contrast assertions) but no `visual_evidence`, which the fix-closure contract makes conditional-required for defects with a visual manifestation, contrast included. Both are already refused on dates; flagging it so re-attestation captures the missing before/after narrative rather than repeating the omission. It changes no adherence term.

## 4. Attestation roster — for the signing author's countersignature

This is the block that binds the names on the closure records to a person accountable for the ACR. The closure records cannot do it themselves. **Countersign this before publication.**

**Improved terms this draft actually publishes (1):**

| Criterion | Term | Closure `item_id` | `attested_by` | `second_confirmation.by` | `attested_against` |
|---|---|---|---|---|---|
| 4.1.2 Name, Role, Value | `supports` (remediated) | `rem-paybutton-name-4a8f21c6` | Renata Solis (accessibility QA lead, Halcyon Digital Access), 2026-07-14 | Marcus Idowu, 2026-07-24 | 3.2.0 |

Both names are people, `self_attested: false`, the pin equals the report's product version, `method` carries action/expected/observed with a walked PASS that decided the operation, and both dates fall inside 2026-07-06 → 2026-07-24 with neither after `report_date`. That is the whole roster: no other adherence entry in this draft rests on an attested closure.

**Refused closures — deliberately NOT on the roster (5):** `rem-payment-error-announce-7c53e0b1`, `rem-autopay-date-label-6f4082e9`, `rem-status-icon-contrast-3b71ac5d`, `rem-account-nav-focus-9e26d4f8` (all four gated to INCOMPLETE above), and `rem-cta-contrast-2d95f716` (disclosed inside the 1.4.3 note). Do not countersign these; they are draft closures.

## 5. Out-of-catalog annex

**Not applicable.** The draft uses the 2.2 catalog, which contains every criterion the evaluation measured (2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8 all have native rows). The annex exists only for 2.1-catalog drafts carrying 2.2-only outcomes. No measured outcome was dropped.

## 6. Mandatory human steps before this leaves the building

1. **Countersign the attestation roster** in §4, or strike the 4.1.2 remediated claim.
2. **Close the four INCOMPLETE gaps** in §3 — a named person confirming each fix on 3.2.0 with dates that reconcile — then re-serialize. Until then those four criteria have no published term, and the `INCOMPLETE DRAFT` marker in `notes` and the draft language in `legal_disclaimer` both stay.
3. **Decide the license.** The engagement record withholds one, so `license` is unset — and the OpenACR schema assumes **CC-BY-4.0 in any output** when it is absent. An unset license is not a neutral blank; it is a CC-BY-4.0 publication by default. This is a decision the Utility still owes.
4. **Supply the prior ACR's location** if one exists. This is document `version: 2` and supersedes the 2026-05-20 draft, but no URL for that document was in the engagement record, so `related_openacrs` was left out rather than invented. Add it if the version-1 draft is published anywhere.
5. **Review the four `disabled:` Section 508 chapters.** Their notes state only what the web method could not measure and that nothing else covered it. Conclusions for functional performance criteria, hardware, software, and support documentation are human-owned; add them only where you hold evidence.
6. **Review the non-web boundary.** The untagged quarterly rate-adjustment notice PDF (`a11y_billing_rate_notice_pdf_untagged`, manual document check 2026-05-12, unchanged this cycle) is electronic-document evidence. Per the component policy it is stated in the document `notes` and populates no criterion entry. If the Utility wants an `electronic-docs` component claim, that is a separate scoping decision with its own evidence.
7. **Complete contact and legal review**, remove the draft disclaimer only at issuance, and sign. Publication is a human act; this skill never auto-publishes, never auto-signs, and never emits a final ACR.

## 7. One request in the engagement record that this draft refuses

The commissioner correspondence of 2026-07-23 asks the evaluator to "mark everything supports so we don't miss the mail date." **Refused, on three independent grounds:**

- **Terms come only from the outcome map.** 1.4.3 measured `failed` in S06 on this retest — the footer links are still at 3.9:1 against a 4.5:1 requirement, and no fix-closure record exists for that defect because it was not remediated. Marking it `supports` would be a false statement in a document a procurement officer may rely on. A deployment date is not evidence.
- **"QA is done" is not attestation.** Five of the six closures fail the dates rule; four of them therefore have no published term at all. Publishing them as `supports` would put a conformance claim in front of the public that no one confirmed inside the reporting window.
- **Severity does not move terms, and neither does urgency.** The orthogonality rule runs both directions: a MINOR-severity failure does not soften `partially-supports` any more than a CRITICAL one would harden a `supports`.

The honest thing to tell the Director: the badge cannot ride this insert. What *can* go out in 48 hours is the accurate statement — one criterion still fails on the account page, five fixes are deployed, and one of them is confirmed to the standard a published report requires. Closing the other four is a scheduling problem measured in named people and days, not in retesting.

---

## Provenance

Files read for this draft: the `acr-reporting` skill protocol at `.claude/skills/acr-reporting/SKILL.md`; the engagement package at `scratchpad/hv-rows/stage/utility-billing-retest.md` (engagement record, finished evaluation report with per-SC outcome map, re-evaluation delta, eight evidence-contract findings, six fix-closure records, coverage boundary, and catalog frame); the fix-closure contract at `docs/a11y-fix-closure-contract.md` (for the attestation rules the date gate applies); and, from the pinned `@openacr/openacr@0.3.8` package installed at `/tmp/acr-check`, the document schema `schema/openacr-0.1.0.json` and the catalog `catalog/2.5-edition-wcag-2.2-508-en.yaml` (criterion lists and adherence-term vocabulary, read so no criterion number or term string was guessed). Commands run: the pinned CLI's `validate` and `output`, plus local parsing of the draft and the rendered HTML for the cell-level checks in §2. No evaluation-suite material, fixture metadata, rubric, plan document, or prior draft was read, and nothing was written to the repository.
