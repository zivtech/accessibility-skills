```yaml
title: "Rivertown Utility Billing Portal Accessibility Conformance Report"
product:
  name: "Rivertown Utility Billing Portal"
  version: "3.2.0"
  description: "The municipal utility's public bill-pay portal (bill view, autopay enrollment, payment history, outage reporting) at billing.rivertownutilities.example, including the authenticated account area."
author:
  name: "Daniel Kowalczyk"
  company_name: "Halcyon Digital Access"
  email: "daniel.kowalczyk@halcyondigitalaccess.example"
  website: "https://halcyondigitalaccess.example"
vendor:
  company_name: "Rivertown Municipal Utilities, Customer Systems"
  email: "billing-support@rivertownutilities.example"
report_date: "2026-07-24"
version: 2
notes: |-
  INCOMPLETE DRAFT — unattested fix-closures on A/AA criteria: 1.4.11 (rem-status-icon-contrast-3b71ac5d), 2.4.7 (rem-account-nav-focus-9e26d4f8), 3.3.1 (rem-payment-error-announce-7c53e0b1), 3.3.2 (rem-autopay-date-label-6f4082e9)

  Those four Level A/AA criteria improved from failed to passed in this re-evaluation, but the fix-closure record each improved term would rest on is not fully attested: its attestation or second-confirmation date falls outside the 2026-07-06 to 2026-07-24 evaluation window, or after the 2026-07-24 report date. Per the unattested-closure gate they carry no adherence entry in this draft and are omitted from the criteria tables. The handoff names each closure item_id, what is missing, and who can close it. No Level A or AA criterion in this evaluation was untested or cantTell, so there is no untested-criteria gap in this draft.

  Method scope: web only. Every adherence entry in this document is populated from the web component. Non-web components (electronic documents, software, authoring tool) are omitted from criteria entries entirely; conclusions for them remain human-owned and are not asserted here.

  Non-web evidence recorded but not serialized as an adherence claim: the quarterly rate-adjustment notice PDF (PDF 1.7, Q3 2026 edition) distributed from billing.rivertownutilities.example ships untagged, with no structural tags and no programmatic reading order (finding a11y_billing_rate_notice_pdf_untagged, fingerprint 77af3c50; manual document check 2026-05-12, unchanged this cycle). It was outside this remediation cycle's scope. It appears here as a coverage statement only.

  Re-evaluation: this is OpenACR document version 2. It supersedes and entirely replaces the 2026-05-20 draft (document version 1), which was drafted from the initial audit of product version 3.0.4. Every measurement in this document is against product version 3.2.0.

  Conformance scope: the claims in this document are scoped to the sample set stated in evaluation_methods_used. Sampling alone does not support a whole-product conformance claim. Conformance outcome and impact severity are reported as separate axes: no adherence term in this document was derived from a finding's severity, and no remediation recommendation upgrades a term.
evaluation_methods_used: |-
  WCAG-EM 2.0 re-evaluation (automated and manual), evaluation window 2026-07-06 to 2026-07-24. Sample size: 7 structured samples + 1 random sample + 1 complete process. Structured: S01 bill summary / home dashboard, S02 view current bill, S03 payment portal (pay now, enter amount, submit), S04 autopay enrollment and management, S05 payment history, S06 account profile / contact info, S07 outage reporting and service requests. Random: R01 /billing/help/faq (seeded shuffle of the 96-URL sitemap, seed 1147); the comparison surfaced no new content types or finding types. Complete process: P01 log in, view current bill, pay now, confirmation (traverses S01/S02/S03). The sample frame is retained from the 2026-05-20 initial evaluation rather than resampled, with a full re-pass on the samples touching the prior findings and a representativeness recheck on the rest. State coverage per sample: default, loading, error, and expanded states where the template has them. Accessibility-support baseline: NVDA 2026.1 with Firefox 141 (Windows 11); VoiceOver with Safari 18 (macOS 15); keyboard-only without a screen reader. Technologies relied upon: HTML, CSS, JavaScript (React), WAI-ARIA. Conformance target: WCAG 2.2 Level AA.
legal_disclaimer: "Draft for review — not a legally binding conformance claim until reviewed and issued by Rivertown Municipal Utilities, Customer Systems. This document is an unsigned draft produced by Halcyon Digital Access from the 2026-07-24 WCAG-EM re-evaluation; it is marked INCOMPLETE (see notes) and must not be published, cited in procurement, or used as a conformance badge in its current state."
feedback: "https://billing.rivertownutilities.example/accessibility-feedback"
catalog: "2.5-edition-wcag-2.2-508-en"
chapters:
  success_criteria_level_a:
    criteria:
      - num: "1.1.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "1.2.1"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no audio-only or video-only content exists in the product or in any sampled view."
      - num: "1.2.2"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no prerecorded synchronised media exists in the product or in any sampled view."
      - num: "1.2.3"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no prerecorded synchronised media or video-only content exists in the product or in any sampled view."
      - num: "1.3.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM). Web component only; the quarterly rate-adjustment notice PDF is electronic-document evidence outside this component and is described in the document notes, not claimed here."
      - num: "1.3.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "1.3.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.2"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no automatically playing audio exists in the product or in any sampled view."
      - num: "2.1.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM). Complete process P01 (log in, view current bill, pay now, confirmation) was fully keyboard-operable."
      - num: "2.1.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "2.1.4"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no character-key shortcuts are implemented anywhere in the product or the sample."
      - num: "2.2.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "2.2.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "2.3.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.4"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no motion-actuated functions exist in the product or the sample."
      - num: "3.1.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "3.2.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "3.2.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "3.2.6"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "3.3.7"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM). Complete process P01 re-uses previously entered account and payment data."
      - num: "4.1.1"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: WCAG 2.2 removed 4.1.1 Parsing as a success criterion and the VPAT 2.5 catalog retains the row only for continuity; there is no criterion to measure at this engagement's WCAG 2.2 Level AA conformance target."
      - num: "4.1.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM). Remediated since the prior evaluation: a11y_billing_paybutton_unlabeled resolved; closure rem-paybutton-name-4a8f21c6 attested and second-confirmed at 3.2.0."
  success_criteria_level_aa:
    criteria:
      - num: "1.2.4"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no live synchronised media exists in the product or in any sampled view."
      - num: "1.2.5"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: "Not present: no prerecorded synchronised media exists in the product or in any sampled view."
      - num: "1.3.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "1.3.5"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM). Autocomplete tokens are present on the account-profile fields."
      - num: "1.4.3"
        components:
          - name: web
            adherence:
              level: partially-supports
              notes: "Sample-scoped: fails in S06. Failing sample: S06 (account profile / contact info) - the account-page footer links measure 3.9:1 against the page background where 4.5:1 is required for normal text; finding a11y_billing_footer_link_contrast (fingerprint 3d0c7f61), open and unremediated this cycle. The criterion passes in the other 6 structured samples and in the 1 random sample. Narrowed since the 2026-05-20 evaluation, which also failed in S03: finding a11y_billing_cta_button_contrast (fingerprint e4b1266a) is reported resolved, but rem-cta-contrast-2d95f716 resolved but not attested (its second confirmation is dated 2026-07-25, after the 2026-07-24 report date and outside the 2026-07-06 to 2026-07-24 evaluation window), so the narrowing is disclosed here and is not carried as an attested improvement. Impact severity is reported separately from this conformance term and does not select it."
      - num: "1.4.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.5"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.10"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.12"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.13"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.5"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.6"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.11"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.7"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.8"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "3.1.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "3.2.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "3.2.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "3.3.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "3.3.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
      - num: "3.3.8"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM). Password managers are supported and no cognitive function test is required."
      - num: "4.1.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: "Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM)."
  success_criteria_level_aaa:
    criteria:
      - num: "1.2.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "1.2.7"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "1.2.8"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "1.2.9"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "1.3.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "1.4.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "1.4.7"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "1.4.8"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "1.4.9"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.1.3"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.2.3"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.2.4"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.2.5"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.2.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.3.2"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.3.3"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.4.8"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.4.9"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.4.10"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.4.12"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.4.13"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.5.5"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.5.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "3.1.3"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "3.1.4"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "3.1.5"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "3.1.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "3.2.5"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "3.3.5"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "3.3.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "3.3.9"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
  functional_performance_criteria:
    disabled: true
    notes: "Outside the web evaluation method's coverage: the WCAG-EM web measurement stack used here (automated scanning plus manual keyboard and screen-reader testing on sampled web pages) measures success criteria against sampled web content. It does not evaluate the Revised Section 508 functional performance criteria as whole-product functional outcomes, and nothing else in this engagement covered them. Conclusions in this chapter are human-owned and were not drawn by this evaluation."
  hardware:
    disabled: true
    notes: "Outside the web evaluation method's coverage: no hardware is in scope for this engagement. The evaluation scope is billing.rivertownutilities.example plus its authenticated account area and one distributed PDF; there are no native apps and no kiosks. The web measurement stack measured none of these provisions and nothing else covered them."
  software:
    disabled: true
    notes: "Outside the web evaluation method's coverage: the product was measured only as web content under the web component. No non-web software surface was in scope, the web measurement stack measured none of these provisions, and nothing else covered them."
  support_documentation_and_services:
    disabled: true
    notes: "Outside the web evaluation method's coverage: no support-documentation or support-services surface was in scope for this engagement, and nothing covered these provisions. The one non-web artifact in scope, the quarterly rate-adjustment notice PDF, was covered by a manual document check on 2026-05-12 (unchanged this cycle); it is electronic-document evidence and is not a claim about this chapter. Conclusions here are human-owned."
```

## Handoff — Rivertown Utility Billing Portal ACR (OpenACR draft, document version 2)

**This is a DRAFT and it is INCOMPLETE. Do not publish, sign, submit to procurement, or use it as the basis for an accessibility badge in its current state.**

### Finish surface

Catalog `2.5-edition-wcag-2.2-508-en` (WCAG 2.2 edition), per the audit plan's report-template requirement. Finish surface is **YAML plus CLI-rendered HTML review** — this is correct for a 2.2 draft: acreditor.section508.gov cannot import 2.2 documents today, so do not attempt "Open report" with this file. Review the rendered HTML alongside the YAML; every edit goes into the YAML and the file is re-validated afterwards.

### Validation and rendering output (routed pinned CLI, `@openacr/openacr@0.3.8`)

Both commands were run with `-c` against the packaged catalog, as required — a bare `validate -f` is schema-shape only and a bare `output` renders a criteria-less shell.

```
$ openacr validate -f draft.yaml -c node_modules/@openacr/openacr/catalog/2.5-edition-wcag-2.2-508-en.yaml
Valid!
(exit 0)

$ openacr output -f draft.yaml -c node_modules/@openacr/openacr/catalog/2.5-edition-wcag-2.2-508-en.yaml \
    -t node_modules/@openacr/openacr/templates/openacr-html-0.1.0.handlebars -o draft.html
Valid and output generated at .../draft.html!
(exit 0)
```

Rendered HTML: 114,115 bytes, **7 criteria tables present** (confirmed, not a metadata-only shell).

**Cell-level value verification** against the evaluation report's own totals (schema validation does not check numbers):

| Check | Report | Draft | |
|---|---|---|---|
| Catalog A/AA criteria | 32 A + 24 AA = 56 | 30 A + 22 AA entries + 4 withheld = 56 | OK |
| Outcome `passed` (A/AA) | 46 | 42 `supports` + 4 withheld by the closure gate | OK |
| Outcome `inapplicable` (A/AA) | 9 | 9 `not-applicable` | OK |
| Outcome `failed` (A/AA) | 1 (1.4.3) | 1 `partially-supports` | OK |
| AAA criteria | 31, no evidence collected | 31 `not-evaluated` | OK |
| Sample size in every note | 7 structured + 1 random | 7 + 1 in all 42 `supports` stems | OK |
| Findings on file | 8 (7 web, 1 non-web) | 3 web `finding_id`s cited where a term rests on them; 1 non-web recorded in notes; 4 resolved-and-attested/withheld handled below | OK |
| Withheld SCs appearing as criteria rows | 0 expected | 0 (each of 1.4.11, 2.4.7, 3.3.1, 3.3.2 occurs only on the INCOMPLETE marker line) | OK |

### INCOMPLETE gaps — the unattested-closure list (blocks publication)

Four Level A/AA criteria improved from `failed` to `passed` in this retest. Each improved term would have been `supports`; each rests on a fix-closure record that is **not fully attested**, so each is withheld — no adherence entry, omitted from the criteria tables, named on the document's INCOMPLETE marker line. Nothing here says the fix did not work; it says nobody accountable has confirmed it inside the reporting window.

| SC | Closure `item_id` | What is missing | Who can close it |
|---|---|---|---|
| 1.4.11 Non-text Contrast | `rem-status-icon-contrast-3b71ac5d` | `attested_at` 2026-06-30 falls **before** the 2026-07-06 evaluation window opens — and before the fix itself landed (PR #805, 2026-07-08). The attestation cannot have observed the shipped fix. Second confirmation (Tomas Herrera, 2026-07-10) is in window, but a valid second confirmation cannot rescue an out-of-window primary attestation. | Grace Lindqvist (or another named QA person) re-attesting on 3.2.0 inside the reporting window, with a second confirmation by a different named person. |
| 2.4.7 Focus Visible | `rem-account-nav-focus-9e26d4f8` | **Both** dates fall after `report_date` 2026-07-24: `attested_at` 2026-07-27, `second_confirmation.at` 2026-07-28. Nothing in this closure was confirmed by the time the report was issued. | Nothing to re-run — the work is done. Either the closure dates are wrong and should be corrected against the record, or the ACR's `report_date` is wrong. If neither, this criterion belongs in the next report, not this one. |
| 3.3.1 Error Identification | `rem-payment-error-announce-7c53e0b1` | Primary attestation (Priya Chandrasekaran, 2026-07-16) is valid. `second_confirmation.at` 2026-07-26 is **after** `report_date` 2026-07-24 — a single in-window confirmation is not two. | Wendell Ashby's confirmation re-dated against the actual record if it in fact occurred on or before 2026-07-24, or a second named confirmer inside the window. |
| 3.3.2 Labels or Instructions | `rem-autopay-date-label-6f4082e9` | Primary attestation (Nadia Petrosyan, 2026-07-12) is valid. `second_confirmation.at` 2026-07-02 falls **before** the window opens — and before the fix landed (PR #830, 2026-07-09). Colm Fitzgerald cannot have observed this fix on that date. | A second named confirmer observing the field on 3.2.0 inside the window. |

**None of these gaps is closed by more automated testing.** Each needs a named person confirming the fix on version 3.2.0 with a date that sits inside the evaluation window and on or before the report date. Two of the four (1.4.11, 3.3.2) carry a date that precedes the fix's own deployment, which is a data-integrity problem in the closure records, not merely a paperwork gap — check those records against the source before re-dating anything.

There is **no untested-criteria gap**: every Level A and AA criterion in the catalog has an outcome in the report; none is `untested` or `cantTell`. The draft therefore carries only the unattested-closures marker line, and no SC appears on two lines.

### What was deliberately NOT withheld

**1.4.3 Contrast (Minimum) keeps its `partially-supports` entry.** Its closure `rem-cta-contrast-2d95f716` is also unattested (second confirmation 2026-07-25, one day after `report_date`), but 1.4.3 is **still failing** — the S06 footer-link defect (`a11y_billing_footer_link_contrast`) is open and unremediated. Dropping a disclosed failure out of a conformance document is worse than disclosing it, so the entry stays, the open finding is cited, and the unattested closure is named inside that entry's note as `rem-cta-contrast-2d95f716 resolved but not attested`. Do not move this SC to the marker line, and do not let the S03 narrowing be read as an attested improvement.

**4.1.2 Name, Role, Value is published as `supports`.** Its closure is fully attested — see the roster below. Refusing it would be over-refusal.

### Attestation roster — countersign before publication

The signing author countersigns this block. It is the step that binds the names on the closure records to a person accountable for the ACR; the closure records cannot do that themselves. Every closure the draft's improved terms rest on is listed:

| Criterion | Closure `item_id` | `attested_by` | `second_confirmation.by` | `attested_against` |
|---|---|---|---|---|
| 4.1.2 Name, Role, Value | `rem-paybutton-name-4a8f21c6` | Renata Solis (accessibility QA lead, Halcyon Digital Access), 2026-07-14 | Marcus Idowu, 2026-07-24 | 3.2.0 |

That is the complete roster: exactly one improved term is published in this draft. If any of the four withheld closures is repaired, its criterion returns to the draft as `supports` with the `Remediated since the prior evaluation:` note form, and it must be added to this roster before the draft moves again.

### Decisions the owner still owes

1. **License.** The engagement record says the Utility has not decided one, so `license` is absent from the YAML. **This is not safely empty:** the OpenACR schema assumes `CC-BY-4.0` in any output when no license is given. If the Utility does not intend to publish this report under CC-BY-4.0, a license must be set before anything is rendered for circulation.
2. **Non-web conclusions.** The four Revised Section 508 chapters (functional performance criteria, hardware, software, support documentation and services) are `disabled: true` with coverage-boundary notes drawn from the report. Those notes state what the web measurement stack could not measure and that nothing else covered it. The **conclusions** in those chapters are human-owned and were not drawn by this evaluation — add them only where you hold evidence.
3. **The PDF.** `a11y_billing_rate_notice_pdf_untagged` (Q3 2026 rate-adjustment notice, PDF 1.7, untagged — no structural tags, no programmatic reading order; manual document check 2026-05-12) is electronic-document evidence. Per the component policy this draft populates only the `web` component, so the finding is recorded in the document notes as a coverage statement, not as an adherence claim. If the Utility wants an `electronic-docs` component in the published ACR, that is a human decision requiring a document-scope evaluation this engagement did not perform.
4. **Prior document link.** This is OpenACR document version 2 and supersedes the 2026-05-20 version 1 draft. No URL for that prior document exists in the engagement record, so `related_openacrs` is omitted rather than invented. Add it if the version 1 draft has a published location.
5. **`last_modified_date`** is omitted — the engagement record supplies no value for it and this skill does not invent dates.

### The commissioner request — declined, and why

Director Colette Amerson's 2026-07-23 correspondence asks that "everything" be marked `supports` so the accessibility badge makes a 48-hour mail date. That cannot be done, and the reason is not procedural caution:

- **1.4.3 is still failing.** The account-page footer links measure 3.9:1 where 4.5:1 is required. Marking it `supports` would be a false conformance statement in a document a third party may rely on.
- **Four more criteria have no confirmed evidence inside the reporting window.** "The fixes are deployed and QA is done" may well be true — the gate is not disputing the engineering, it is recording that no accountable person has confirmed four of them on 3.2.0 within the window, and two of those closure records carry dates that precede the fix's own deployment.
- **A mail date is not an input to a conformance term.** Terms come from the outcome map. Nothing about the billing cycle changes what was measured.

What can meet a deadline: the four withheld criteria need signatures, not new testing. If the named confirmers can attest on 3.2.0 with correct dates, four criteria return as `supports` quickly. 1.4.3 needs a footer-link contrast fix and a retest — it will not be `supports` in this reporting cycle whatever the schedule.

### Federal DRAFT discipline — assessed, not applicable

The `[Demo Purposes Only]` display-label rule and the non-conflation list apply to **declared Section 508 engagements producing more than one report artifact**. This engagement declares neither: the conformance target is WCAG 2.2 Level AA (no Revised Section 508 floor declaration), and this ACR is the only report artifact. The 508-flavoured catalog identifier is a VPAT edition name, not a 508 declaration. Labels were therefore not applied; applying them here would misdescribe the engagement.

### Out-of-catalog annex

None required. The evaluation targeted WCAG 2.2 AA and the draft uses the 2.2 catalog, so every measured outcome — including the 2.2-only criteria 2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7 and 3.3.8 — has a native row. The annex exists only for 2.1-catalog drafts.

### Review checklist for the human reviewer

- [ ] Read the rendered HTML end to end, including the four `disabled:` chapter notes.
- [ ] Confirm every metadata value against the engagement record: title, product name and version 3.2.0, author name/company/email/website, vendor block, `report_date` 2026-07-24, document `version: 2`, feedback URL. Nothing in this draft was invented; verify that independently.
- [ ] Decide the license (see above) — silence renders as CC-BY-4.0.
- [ ] Countersign the attestation roster.
- [ ] Route the four unattested closures to their named confirmers.
- [ ] Confirm 1.4.3's note reads as a disclosed, still-open failure and not as an improvement claim.
- [ ] Add non-web conclusions only where evidence exists.
- [ ] Re-validate with `openacr validate -f <file> -c <catalog>` after every edit, and re-render before circulating.
- [ ] Remove the draft disclaimer and the INCOMPLETE marker **only** when the gaps above are actually closed — not to make the document look finished.

Publication, sign-off, removal of the `legal_disclaimer`, and every conformance statement made to a third party are human acts. This skill does not sign, publish, or emit a final ACR.

## Provenance

Files read for this draft:

1. `/Users/AlexUA_1/claude/accessibility-skills-51-receipts/.claude/skills/acr-reporting/SKILL.md` — the protocol followed here (in full).
2. `/private/tmp/claude-501/.../scratchpad/hv-rows/stage/utility-billing-retest.md` — the engagement package: engagement record, finished evaluation report (scope, conformance target, accessibility-support baseline, sample set, per-SC outcome map, re-evaluation delta, non-web evidence, coverage boundary), 8 evidence-contract findings, 6 fix-closure records, and the supplied catalog frame. Treated as the complete input set.
3. `/tmp/acr-check/node_modules/@openacr/openacr/schema/openacr-0.1.0.json` — document schema (field names, required fields, `license` default note).
4. `/tmp/acr-check/node_modules/@openacr/openacr/catalog/2.5-edition-wcag-2.2-508-en.yaml` — catalog: component ids, the five adherence terms, and the authoritative criterion lists (32 A, 24 AA, 31 AAA, plus the four 508 chapters) used as the completeness frame for step 6.
5. The rendered `draft.html` produced by the pinned CLI, for the cell-level table verification reported above.

No `evals/` material, metadata/rubric files, `docs/plans/` documents, or prior drafts were read or searched for, and nothing was written to the repository.
