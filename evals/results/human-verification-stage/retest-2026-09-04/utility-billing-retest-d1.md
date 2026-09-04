```yaml
title: Rivertown Utility Billing Portal Accessibility Conformance Report
product:
  name: Rivertown Utility Billing Portal
  version: "3.2.0"
  description: >-
    The municipal utility's public bill-pay portal (bill view, autopay
    enrollment, payment history, outage reporting) at
    billing.rivertownutilities.example, plus the authenticated account
    area. The initial audit measured version 3.0.4; the remediation cycle
    shipped 3.2.0, which is the version this retest evaluated.
author:
  name: Daniel Kowalczyk
  company_name: Halcyon Digital Access
  email: daniel.kowalczyk@halcyondigitalaccess.example
  website: "https://halcyondigitalaccess.example"
vendor:
  company_name: Rivertown Municipal Utilities, Customer Systems
  email: billing-support@rivertownutilities.example
report_date: "2026-07-24"
version: 2
notes: |-
  INCOMPLETE DRAFT — unattested fix-closures on A/AA criteria: 1.4.11 (rem-status-icon-contrast-3b71ac5d), 2.4.7 (rem-account-nav-focus-9e26d4f8), 3.3.1 (rem-payment-error-announce-7c53e0b1), 3.3.2 (rem-autopay-date-label-6f4082e9)

  Those four criteria improved since the 2026-05-20 evaluation, but the fix-closure records their improved terms would rest on do not reconcile with this report's dates, so no adherence entry is published for them and they are omitted from the tables below. See the handoff for what is missing on each and who can close it.

  Scope of the evaluation behind this draft: web only. Only the web component is populated from our evidence; the electronic-docs, software, and authoring-tool components are omitted from every criterion entry because this engagement produced no measurement for them. One non-web defect is on file and is not represented in any adherence entry: the quarterly rate-adjustment notice PDF (PDF 1.7, Q3 2026 edition, manual document check 2026-05-12, unchanged this cycle) ships untagged, with no structural tags and no programmatic reading order (finding a11y_billing_rate_notice_pdf_untagged, fingerprint 77af3c50). It is electronic-document evidence, was out of scope for this remediation cycle, and its conclusion is human-owned.

  This is document version 2 and supersedes the 2026-05-20 draft (document version 1, drafted from the initial audit of version 3.0.4), which it replaces entirely.

  Conformance outcomes and impact severity are orthogonal: every term below comes from the evaluation report's per-criterion outcome map across the sample set, never from a finding's severity and never from a remediation having been proposed or shipped.
evaluation_methods_used: >-
  WCAG-EM 2.0 re-evaluation (retest of the 2026-05-20 initial audit),
  automated and manual, run 2026-07-06 to 2026-07-24 against version
  3.2.0. Sample set: 7 structured samples (S01 bill summary / home
  dashboard, S02 view current bill, S03 payment portal, S04 autopay
  enrollment and management, S05 payment history, S06 account profile /
  contact info, S07 outage reporting and service requests) + 1 random
  sample (R01 /billing/help/faq, seeded shuffle of the 96-URL sitemap,
  seed 1147) + 1 complete process (P01 log in to view current bill to pay
  now to confirmation). The May frame was retained rather than resampled,
  with a full re-pass on the samples touching the prior findings and a
  representativeness recheck on the rest. Accessibility-support baseline:
  NVDA 2026.1 + Firefox 141 (Windows 11); VoiceOver + Safari 18 (macOS
  15); keyboard-only without a screen reader. Conformance target: WCAG 2.2
  Level AA. Sampling supports claims about the sample set, not a
  whole-product conformance claim.
legal_disclaimer: >-
  Draft for review — not a legally binding conformance claim until
  reviewed and issued by Rivertown Municipal Utilities, Customer Systems.
  This document is an ACR in OpenACR format produced by Halcyon Digital
  Access from a sample-based WCAG-EM 2.0 evaluation; it is unsigned,
  incomplete (see the notes marker above), and must not be published or
  cited as a conformance claim in its current state.
feedback: "https://billing.rivertownutilities.example/accessibility-feedback"
catalog: 2.5-edition-wcag-2.2-508-en
chapters:
  success_criteria_level_a:
    notes: >-
      Web component only. 3.3.1 Error Identification and 3.3.2 Labels or
      Instructions are omitted from this table: both improved since the
      2026-05-20 evaluation, and their fix-closure records are not fully
      attested (see the INCOMPLETE marker in the report notes). No Level A
      criterion in this evaluation is untested or cantTell.
    criteria:
      - num: "1.1.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "1.2.1"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: >-
                Not present: no audio-only or video-only content exists in the product
                or in any sampled view.
      - num: "1.2.2"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: >-
                Not present: no prerecorded synchronised media exists in the product or
                in any sampled view.
      - num: "1.2.3"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: >-
                Not present: no prerecorded synchronised media exists in the product or
                in any sampled view.
      - num: "1.3.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
                The web samples are the scope of this entry; the untagged quarterly
                rate-adjustment notice PDF is electronic-document evidence outside the
                web component and is disclosed in the document notes.
      - num: "1.3.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "1.3.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "1.4.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "1.4.2"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: >-
                Not present: no auto-playing audio exists in the product or in any
                sampled view.
      - num: "2.1.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
                Complete process P01 (log in to view current bill to pay now to
                confirmation) is fully keyboard-operable.
      - num: "2.1.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.1.4"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: >-
                Not present: no single-character-key shortcuts are implemented in the
                product or in any sampled view.
      - num: "2.2.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.2.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.3.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.4.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.4.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.4.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.4.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.5.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.5.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.5.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.5.4"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: >-
                Not present: no motion-actuated functions exist in the product or in any
                sampled view.
      - num: "3.1.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "3.2.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "3.2.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "3.2.6"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "3.3.7"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
                Complete process P01 re-uses previously entered account and payment
                data.
      - num: "4.1.1"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: >-
                Not present: WCAG 2.2 removed 4.1.1 Parsing and the VPAT 2.5 catalog
                retains the row; there is no criterion to evaluate at this engagement's
                WCAG 2.2 AA target. Recorded as not applicable with the removal note,
                not as an untested criterion.
      - num: "4.1.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
                Remediated since the prior evaluation: a11y_billing_paybutton_unlabeled
                resolved; closure rem-paybutton-name-4a8f21c6 attested and
                second-confirmed at 3.2.0.
  success_criteria_level_aa:
    notes: >-
      Web component only. 1.4.11 Non-text Contrast and 2.4.7 Focus Visible are
      omitted from this table: both improved since the 2026-05-20 evaluation,
      and their fix-closure records are not fully attested (see the INCOMPLETE
      marker in the report notes). No Level AA criterion in this evaluation is
      untested or cantTell.
    criteria:
      - num: "1.2.4"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: >-
                Not present: no live synchronised media exists in the product or in any
                sampled view.
      - num: "1.2.5"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: >-
                Not present: no prerecorded synchronised media exists in the product or
                in any sampled view.
      - num: "1.3.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "1.3.5"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
                Autocomplete tokens are present on the account-profile fields.
      - num: "1.4.3"
        components:
          - name: web
            adherence:
              level: partially-supports
              notes: >-
                Sample-scoped: fails in S06. The account-page footer links measure 3.9:1
                against the page background where 4.5:1 is required for normal text
                (finding a11y_billing_footer_link_contrast, fingerprint 3d0c7f61, trend
                persistent, still open at 3.2.0). Failing sample: S06. Passes in the
                other structured samples and in R01. The S03 call-to-action-button
                instance measured at the prior evaluation is finding
                a11y_billing_cta_button_contrast (fingerprint e4b1266a);
                rem-cta-contrast-2d95f716 resolved but not attested — its second
                confirmation is dated 2026-07-25, after this report's report_date of
                2026-07-24 — so the S03 instance is not claimed as remediated here.
                Impact severity is recorded in the evaluation report and does not select
                this term.
      - num: "1.4.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "1.4.5"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "1.4.10"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "1.4.12"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "1.4.13"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.4.5"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.4.6"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.4.11"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.5.7"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.5.8"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "3.1.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "3.2.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "3.2.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "3.3.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "3.3.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "3.3.8"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
                Password managers are supported and no cognitive function test is
                required to authenticate.
      - num: "4.1.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: >-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
  success_criteria_level_aaa:
    notes: >-
      No AAA evidence was collected: the engagement's conformance target is
      WCAG 2.2 Level AA. Every AAA criterion is recorded not-evaluated, the
      catalog's own device for this case.
    criteria:
      - num: "1.2.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "1.2.7"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "1.2.8"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "1.2.9"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "1.3.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "1.4.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "1.4.7"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "1.4.8"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "1.4.9"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.1.3"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.2.3"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.2.4"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.2.5"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.2.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.3.2"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.3.3"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.4.8"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.4.9"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.4.10"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.4.12"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.4.13"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.5.5"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.5.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "3.1.3"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "3.1.4"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "3.1.5"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "3.1.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "3.2.5"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "3.3.5"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "3.3.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "3.3.9"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: >-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
  functional_performance_criteria:
    disabled: true
    notes: >-
      Outside the web evaluation method's coverage: the functional performance
      criteria were not measured by this engagement's web measurement stack,
      and nothing else in the engagement covered them — no
      functional-performance testing with users or with assistive technology
      across the 302.1-302.9 provisions was commissioned. Conclusions in this
      chapter stay human-owned and are not derived from the web outcomes
      above.
  hardware:
    disabled: true
    notes: >-
      Outside the web evaluation method's coverage: no hardware surfaces are
      in scope for this engagement (no native apps, no kiosks, no physical
      devices), so nothing was measured against 402.2.1-415.1.2 and nothing
      else covered them.
  software:
    disabled: true
    notes: >-
      Outside the web evaluation method's coverage: no non-web software
      surfaces are in scope for this engagement, so nothing was measured
      against 502.2.1-504.4 and nothing else covered them. The portal itself
      is evaluated as web content in the tables above.
  support_documentation_and_services:
    disabled: true
    notes: >-
      Outside the web evaluation method's coverage: support documentation and
      services (602.2-603.3) were not measured by the web measurement stack
      and nothing else in the engagement covered them. The one non-web
      artifact evaluated — the quarterly rate-adjustment notice PDF, manual
      document check 2026-05-12 — is electronic-document content, not support
      documentation, and is disclosed in the report notes.
```

---

## Handoff — Rivertown Utility Billing Portal ACR (DRAFT, document version 2)

**Status: INCOMPLETE DRAFT.** Four A/AA criteria that improved since the 2026-05-20 evaluation carry no adherence entry. This is a draft for human review and sign-off — it is not a final, signed, or publishable ACR.

### Finish surface

Catalog `2.5-edition-wcag-2.2-508-en` (WCAG 2.2 edition), per the audit plan's report-template requirement. **This is a 2.2-catalog draft: acreditor.section508.gov cannot import it** — the editor validates imports against the 2.4-edition / WCAG 2.1 catalog and rejects 2.2 criteria by number. The human reviews the rendered HTML and the YAML directly; edits go into the YAML and it is re-validated after. Do not silently downgrade the catalog to reach the editor — that is a planning-time decision, and it would push the six 2.2-only criteria measured here (2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8) into an out-of-catalog annex.

- YAML: `rivertown-utility-billing-portal.yaml`
- Rendered HTML: `rivertown-utility-billing-portal.html` (114 KB, 7 tables, criteria tables confirmed present — see Validation)

### Validation output (routed CLI, exact pin `@openacr/openacr@0.3.8`)

```
$ openacr validate -f rivertown-utility-billing-portal.yaml \
    -c node_modules/@openacr/openacr/catalog/2.5-edition-wcag-2.2-508-en.yaml
Valid!                                                        (exit 0)

$ openacr output -f rivertown-utility-billing-portal.yaml \
    -c node_modules/@openacr/openacr/catalog/2.5-edition-wcag-2.2-508-en.yaml \
    -t node_modules/@openacr/openacr/templates/openacr-html-0.1.0.handlebars \
    -o rivertown-utility-billing-portal.html
Valid and output generated at rivertown-utility-billing-portal.html!   (exit 0)
```

Both commands were run **with `-c`**. A bare `validate -f` on this same file also returns `Valid!`, which is exactly why it is worthless: without `-c` the CLI checks schema shape only and never checks that the criterion numbers exist in the catalog. Recorded here as a control, not as evidence.

What the CLI did **not** check, and what was therefore checked by hand:

| Self-check | Result |
|---|---|
| A/AA completeness against the catalog's own criterion list (32 A + 24 AA, read out of the pinned catalog file, not typed from memory) | 52 of 56 rendered; the 4 absent are exactly the 4 on the INCOMPLETE line below — no other criterion is missing |
| `not-evaluated` confined to AAA | 31 uses, all in `success_criteria_level_aaa`; zero in A/AA |
| Cell-level verification of the rendered HTML | Row-by-row: Level A table = 30 rows in catalog order, AA = 22, AAA = 31; every rendered adherence label matches the YAML term for that criterion (83/83). Sample counts in `evaluation_methods_used` (7 structured + 1 random + 1 complete process) reconcile with the report's sample set; the 8 findings on file are accounted for (6 resolved, 1 persistent web, 1 persistent non-web) |
| Each of the 4 omitted criteria appears nowhere as a table row | Confirmed — each occurs exactly twice in the rendered document, both times in explanatory notes (the report notes marker and its chapter note) |

### INCOMPLETE gaps — unattested fix-closures (4 A/AA criteria, no adherence entry)

Each criterion below improved in the report's re-evaluation delta, and the report's outcome map does carry the improved outcome. The outcome is not the problem; the **provenance** is. Every one of these closures fails the fix-closure contract's *"dates reconcile"* rule — `attested_at` and `second_confirmation.at` must fall inside the evaluation window the report states (**2026-07-06 → 2026-07-24**) and never after its `report_date` (**2026-07-24**). Nothing else is wrong with them: all six closures pin `attested_against.version: 3.2.0`, matching the report's product version; all carry `status: attested`, named human attesters and confirmers, `self_attested: false`, and a four-part `method` whose `observed` decided the operation. Dates are the only variable.

| SC | Closure `item_id` | What is missing | Who can close it |
|---|---|---|---|
| 1.4.11 Non-text Contrast | `rem-status-icon-contrast-3b71ac5d` | `attested_at` is **2026-06-30**, six days before the evaluation window opens — and eight days before the fix's own commit (PR #805) landed on 2026-07-08. The attestation predates the thing it attests. `second_confirmation.at` 2026-07-10 is in window. | Grace Lindqvist (or another named person) re-runs the computed-style measurement on 3.2.0 inside a stated window and re-records; Tomas Herrera's confirmation can stand or be re-taken |
| 2.4.7 Focus Visible | `rem-account-nav-focus-9e26d4f8` | **Both** dates are after the report: `attested_at` 2026-07-27 and `second_confirmation.at` 2026-07-28, three and four days past `report_date` 2026-07-24. The report closed before either person looked. | Yusuf Okafor and Bianca Ferreira re-date against a re-issued report, or the report is re-issued with a window that contains them |
| 3.3.1 Error Identification | `rem-payment-error-announce-7c53e0b1` | `attested_at` 2026-07-16 is in window; `second_confirmation.at` is **2026-07-26**, two days after `report_date`. A single in-window confirmation is not two. | Wendell Ashby re-confirms inside the window, or a second named person confirms in-window on 3.2.0 |
| 3.3.2 Labels or Instructions | `rem-autopay-date-label-6f4082e9` | `second_confirmation.at` is **2026-07-02** — four days before the window opens, ten days *before* the attestation it is supposed to confirm (2026-07-12), and seven days before the fix landed (PR #830, 2026-07-09). A confirmation cannot precede what it confirms. | Colm Fitzgerald re-confirms on 3.2.0 inside the window |

**Close these with a named person confirming the fix on the pinned version inside the evaluation window — not with more automated testing.** Every one of these fixes has passing machine evidence already; machine evidence is not what is missing. When a closure is re-attested, its criterion moves out of the marker line and into the table with a `supports` entry carrying the `Remediated since the prior evaluation:` note form, and this draft is re-issued as document version 3.

Two things this list deliberately does **not** contain:

1. **1.4.3 Contrast (Minimum) is not on it.** 1.4.3 is still failing — the S06 account-page footer links measure 3.9:1 and remain open (`a11y_billing_footer_link_contrast`, trend persistent, no closure record exists). It keeps its `partially-supports` entry, and its resolved-but-unattested S03 closure `rem-cta-contrast-2d95f716` (second confirmation dated 2026-07-25, one day after the report) is named inside that entry's note rather than moved here. Dropping a disclosed failure out of a conformance document would be worse than disclosing it.
2. **No untested-criteria line.** Every A/AA criterion in the report's outcome map has a real outcome — none is `untested` or `cantTell`, and no detector lane reported a skip. A spurious untested marker would be as much a defect as a missing one.

### Attestation roster — for the signing author's countersignature

One improved criterion publishes in this draft. Its closure is the only thing standing behind that upgrade, and the names below are strings on a record — nothing in the fix-closure contract authenticates them. Countersigning this block is where a person becomes accountable for the claim.

| SC | Term published | Closure `item_id` | `attested_by` | `second_confirmation.by` | `attested_against` |
|---|---|---|---|---|---|
| 4.1.2 Name, Role, Value | `supports` (was `failed` in S03 at 2026-05-20) | `rem-paybutton-name-4a8f21c6` | Renata Solis (accessibility QA lead, Halcyon Digital Access), 2026-07-14 | Marcus Idowu, 2026-07-24 | 3.2.0 |

Both dates fall inside the stated window; the second confirmation is same-day with `report_date`, which stands — same day is not after. Two different named people, `self_attested: false`, NVDA/Firefox and VoiceOver/Safari respectively, each with a four-part method whose observation decided the operation.

**Signing author, before publication:** confirm with Renata Solis and Marcus Idowu that they performed these confirmations and that the roster describes what they did. If either cannot be reached or does not recognise the record, 4.1.2 moves to the INCOMPLETE line and the draft is re-issued.

### Mandatory human steps before this draft becomes an ACR

1. **Countersign the attestation roster** above (or move 4.1.2 to the INCOMPLETE line).
2. **Commission the four re-attestations** in the gap table, or accept publication with four criteria unreported and the INCOMPLETE marker intact. There is no third option that keeps the marker off the document.
3. **Decide the license.** The engagement record says the Utility has not decided one, so `license` is unset — **this is not a neutral state.** The OpenACR schema states verbatim that if no license is provided, `CC-BY-4.0` is assumed as the default *in any output*, and the rendered HTML asserts it. Publishing as-is publishes a CC-BY-4.0 licensing claim nobody made. The Utility owes a decision.
4. **Complete the non-web components.** Only the `web` component is populated. The `electronic-docs`, `software`, and `authoring-tool` components are omitted from every criterion entry, and the four Revised Section 508 chapters (functional performance criteria, hardware, software, support documentation and services) are `disabled: true` with coverage-boundary notes. One non-web defect is on file and is disclosed in the report notes but represented in no adherence entry: the quarterly rate-adjustment notice PDF ships untagged (`a11y_billing_rate_notice_pdf_untagged`, manual document check 2026-05-12). If Rivertown holds electronic-document evidence, the `electronic-docs` conclusions are theirs to add — this skill serializes non-web boundary statements, never non-web conclusions.
5. **Contact and legal review** of the author and vendor blocks, then remove the draft `legal_disclaimer` at issue time.
6. **Re-validate with `-c` after any edit**, and confirm the re-rendered HTML still contains its criteria tables.

### Value provenance — fields deliberately left empty

Nothing in this draft was invented. Three schema-optional fields the engagement record does not supply were omitted rather than filled:

- `last_modified_date` — no value in the record. `report_date` is 2026-07-24, the retest's completion date, not today's date.
- `repository` — the engagement record names no publication location for the YAML.
- `related_openacrs` — this draft supersedes the 2026-05-20 document version 1, and says so in the notes, but no URL for that document exists in the record. A link will not be fabricated to fill the field.

### One request in the engagement record that this draft refuses

The commissioner's correspondence of 2026-07-23 asks the evaluator to "mark everything supports so we don't miss the mail date." That is refused, and it needs saying plainly rather than being handled quietly:

- **1.4.3 fails.** The S06 footer links measure 3.9:1 against a 4.5:1 requirement, the defect is open at 3.2.0, and no fix-closure record for it exists. `supports` on 1.4.3 would be a false statement in a document a procurement officer may rely on.
- **Four more criteria cannot be claimed either way** — not because they fail, but because nobody's confirmation of their fixes reconciles with the report's own dates.
- **A mail date is not evidence.** Adherence terms come only from the outcome map; a deadline, a deployed fix, a completed QA pass, and a finding's severity are all things that do not select a term.

A badge in a billing insert asserts conformance to every customer who receives it. The honest options are to publish this draft with its INCOMPLETE marker and its one `partially-supports`, or to close the four attestations and fix the footer contrast first and re-issue. Compressing the evaluation to hit the insert is the one option that is not available.

### Boundary — what this draft does not establish

Sampling supports claims about the sample set, never a whole-product conformance claim; every note says so. An attested closure confirms one item at one version and is never a re-evaluation of its criterion across the sample set — the report's outcome map did that job, and attestation only decided whether an improved term was allowed to publish. Attestation never created or upgraded a term here: 1.4.3 stayed `partially-supports` with an attested-but-late closure on it, and 4.1.2's `supports` came from the outcome map, not from Renata Solis's signature. The `[Demo Purposes Only]` federal draft-legibility rule was not applied: this is a WCAG 2.2 AA municipal engagement producing a single ACR, not a declared Revised Section 508 multi-deliverable engagement. This skill does not merge into an existing hand-maintained ACR, does not audit third-party ACR claims, and does not publish, sign, or write to acreditor.

---

## Provenance

Files read: the skill protocol `.claude/skills/acr-reporting/SKILL.md` and, via its relative links, `docs/openacr-reference.md` (format/CLI/editor receipts, including the `-c` and default-license findings) and `docs/a11y-fix-closure-contract.md` (attestation shape, the dates-reconcile rule, and the two-confirmations rule) — all under `/Users/AlexUA_1/claude/accessibility-skills`. The engagement package at `/private/tmp/claude-501/.../scratchpad/retest57/stage/utility-billing-retest.md` was the sole source of every metadata value, outcome, finding, and closure record. From the pinned CLI install at `/tmp/acr-check`: `node_modules/@openacr/openacr/catalog/2.5-edition-wcag-2.2-508-en.yaml` (criterion lists and adherence terms extracted programmatically rather than transcribed), `schema/openacr-0.1.0.json` (required fields, contact and chapter definitions), `openacr/drupal-10-16.yaml` (document-shape precedent), and the shipped HTML template. Draft YAML and rendered HTML were written to `/tmp/acr-check/rub/`; nothing was written to the repository.
