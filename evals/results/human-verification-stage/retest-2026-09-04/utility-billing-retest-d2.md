```yaml
title: Rivertown Utility Billing Portal Accessibility Conformance Report
product:
  name: Rivertown Utility Billing Portal
  version: "3.2.0"
  description: |-
    The municipal utility's public bill-pay portal (bill view, autopay enrollment, payment
    history, outage reporting) at billing.rivertownutilities.example, plus the authenticated
    account area. The initial audit measured version 3.0.4; the remediation cycle shipped 3.2.0,
    and this retest measures 3.2.0.
author:
  name: Daniel Kowalczyk
  company_name: Halcyon Digital Access
  email: daniel.kowalczyk@halcyondigitalaccess.example
  website: "https://halcyondigitalaccess.example"
vendor:
  name: Rivertown Municipal Utilities, Customer Systems
  company_name: Rivertown Municipal Utilities
  email: billing-support@rivertownutilities.example
report_date: "2026-07-24"
version: 2
catalog: 2.5-edition-wcag-2.2-508-en
feedback: "https://billing.rivertownutilities.example/accessibility-feedback"
notes: |-
  INCOMPLETE DRAFT — unattested fix-closures on A/AA criteria: 3.3.1 (rem-payment-error-announce-7c53e0b1), 3.3.2 (rem-autopay-date-label-6f4082e9), 2.4.7 (rem-account-nav-focus-9e26d4f8), 1.4.11 (rem-status-icon-contrast-3b71ac5d)

  Scope of this document. It serializes the WCAG-EM 2.0 re-evaluation delivered 2026-07-24
  (evaluation window 2026-07-06 to 2026-07-24) and supersedes OpenACR document version 1 of
  2026-05-20, which was drafted from the initial audit. Only the web component is populated;
  the electronic-docs, software and authoring-tool components are omitted from every criterion
  because the evaluation method measured the web portal only.

  Sample scope. 7 structured samples (S01 bill summary / home dashboard, S02 view current
  bill, S03 payment portal, S04 autopay enrollment and management, S05 payment history, S06
  account profile / contact info, S07 outage reporting and service requests), 1 random sample
  (R01 /billing/help/faq, seeded shuffle of the 96-URL sitemap, seed 1147) and 1 complete
  process (P01 log in, view current bill, pay now, confirmation). Every term below is scoped
  to that sample set; sampling alone supports no whole-product conformance claim.

  Withheld criteria. Four Level A/AA criteria whose outcomes improved since the 2026-05-20
  evaluation carry no adherence entry above, because the fix-closure records their improved
  terms would rest on are not fully attested: in each case the attestation dates do not
  reconcile with this report's evaluation window and report date. Each is named on the marker
  line at the top of these notes with its closure item_id. 1.4.3 Contrast (Minimum) is a
  different case: it is still failing (S06 footer links, unremediated), so it keeps its
  partially-supports entry and its resolved-but-unattested closure is disclosed in that
  entry's note rather than withheld.

  Non-web evidence, carried into no adherence term. The quarterly rate-adjustment notice PDF
  (Q3 2026 edition, manual document check 2026-05-12, unchanged this cycle) ships untagged: no
  structural tags, no programmatic reading order (finding
  a11y_billing_rate_notice_pdf_untagged, fingerprint 77af3c50). It is electronic-document
  evidence, was outside this remediation cycle's scope, and is disclosed here rather than
  mapped to a term.
evaluation_methods_used: |-
  WCAG-EM 2.0 re-evaluation, 2026-07-06 to 2026-07-24. Sample size: 7 structured samples + 1
  random sample + 1 complete process, retained from the initial 2026-04-27 to 2026-05-20 audit
  frame rather than resampled, with a full re-pass on the samples touching the prior findings
  and a representativeness recheck on the rest. Automated and manual testing against the
  declared accessibility-support baseline: NVDA 2026.1 + Firefox 141 (Windows 11); VoiceOver +
  Safari 18 (macOS 15); keyboard-only without a screen reader. Conformance target: WCAG 2.2
  Level AA.
legal_disclaimer: |-
  Draft for review — not a legally binding conformance claim until reviewed and issued by
  Rivertown Municipal Utilities, Customer Systems. Prepared by Halcyon Digital Access from the
  WCAG-EM 2.0 re-evaluation completed 2026-07-24. This draft is INCOMPLETE: four Level A/AA
  criteria are withheld pending attested fix-closure records, as stated in the notes. It is
  unsigned, not final, and not approved for publication or for inclusion in any
  customer-facing material.
chapters:
  success_criteria_level_a:
    notes: |-
      Web component only. 3.3.1 Error Identification and 3.3.2 Labels or Instructions carry no
      entry: both improved from failed to passed since the 2026-05-20 evaluation, and the
      fix-closure records behind those improvements are not fully attested. See the INCOMPLETE
      marker line in the document notes.
    criteria:
      - num: "1.1.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "1.2.1"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: |-
                Not present: no audio-only or video-only content exists in the product or in any sampled
                view.
      - num: "1.2.2"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: |-
                Not present: no prerecorded media exists in the product or in any sampled view.
      - num: "1.2.3"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: |-
                Not present: no prerecorded media exists in the product or in any sampled view.
      - num: "1.3.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM). Web component only.
                The quarterly rate-adjustment notice PDF is electronic-document evidence outside this
                report's web scope and is disclosed in the document notes, not here.
      - num: "1.3.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "1.3.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "1.4.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "1.4.2"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: |-
                Not present: no auto-playing audio exists in the product or in any sampled view.
      - num: "2.1.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM). Complete process P01
                (log in, view current bill, pay now, confirmation) is fully keyboard-operable.
      - num: "2.1.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.1.4"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: |-
                Not present: no character-key shortcuts are implemented in the product.
      - num: "2.2.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.2.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.3.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.4.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.4.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.4.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.4.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.5.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.5.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.5.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.5.4"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: |-
                Not present: no motion-actuated functions exist in the product.
      - num: "3.1.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "3.2.1"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "3.2.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "3.2.6"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "3.3.7"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM). P01 re-uses
                previously entered account and payment data rather than requiring re-entry.
      - num: "4.1.1"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: |-
                Not present: the criterion was removed in WCAG 2.2; the VPAT 2.5 catalog retains the row. No
                parsing obligation applies at this engagement's conformance target (WCAG 2.2 AA).
      - num: "4.1.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM). Remediated since the
                prior evaluation: a11y_billing_paybutton_unlabeled (fingerprint 5e1a92c7) resolved; closure
                rem-paybutton-name-4a8f21c6 attested and second-confirmed at 3.2.0. Attested by Renata Solis
                on 2026-07-14 (NVDA 2026.1 + Firefox 141, keyboard only) and second-confirmed by Marcus
                Idowu on 2026-07-24 (VoiceOver + Safari 18, keyboard only); both dates fall inside the
                2026-07-06 to 2026-07-24 evaluation window and neither is after the 2026-07-24 report date.
  success_criteria_level_aa:
    notes: |-
      Web component only. 1.4.11 Non-text Contrast and 2.4.7 Focus Visible carry no entry: both
      improved from failed to passed since the 2026-05-20 evaluation, and the fix-closure records
      behind those improvements are not fully attested. See the INCOMPLETE marker line in the
      document notes.
    criteria:
      - num: "1.2.4"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: |-
                Not present: no live media exists in the product or in any sampled view.
      - num: "1.2.5"
        components:
          - name: web
            adherence:
              level: not-applicable
              notes: |-
                Not present: no prerecorded media exists in the product or in any sampled view.
      - num: "1.3.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "1.3.5"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM). Autocomplete tokens
                are present on the account-profile input fields.
      - num: "1.4.3"
        components:
          - name: web
            adherence:
              level: partially-supports
              notes: |-
                Sample-scoped: fails in S06. Failing samples: S06 (account profile / contact info), where
                the account-page footer links measure 3.9:1 against the page background and 4.5:1 is
                required for normal text; finding a11y_billing_footer_link_contrast (fingerprint 3d0c7f61),
                open and unremediated this cycle. Passes in S01, S02, S03, S04, S05 and S07 and in random
                sample R01. The S03 Pay Now call-to-action defect (a11y_billing_cta_button_contrast,
                fingerprint e4b1266a) was fixed this cycle, but rem-cta-contrast-2d95f716 resolved but not
                attested: its second confirmation is dated 2026-07-25, after this report's 2026-07-24 report
                date. The criterion is still failing, so it keeps this entry and the narrowing is disclosed
                here rather than claimed.
      - num: "1.4.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "1.4.5"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "1.4.10"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "1.4.12"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "1.4.13"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.4.5"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.4.6"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.4.11"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.5.7"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "2.5.8"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "3.1.2"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "3.2.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "3.2.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "3.3.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "3.3.4"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
      - num: "3.3.8"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM). Password managers
                are supported and no cognitive function test is required.
      - num: "4.1.3"
        components:
          - name: web
            adherence:
              level: supports
              notes: |-
                Sample-scoped: passes across 7 structured + 1 random samples (WCAG-EM).
  success_criteria_level_aaa:
    notes: |-
      No Level AAA evidence was collected. This engagement's conformance target is WCAG 2.2 Level
      AA.
    criteria:
      - num: "1.2.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "1.2.7"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "1.2.8"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "1.2.9"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "1.3.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "1.4.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "1.4.7"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "1.4.8"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "1.4.9"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.1.3"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.2.3"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.2.4"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.2.5"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.2.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.3.2"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.3.3"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.4.8"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.4.9"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.4.10"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.4.12"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.4.13"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.5.5"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "2.5.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "3.1.3"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "3.1.4"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "3.1.5"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "3.1.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "3.2.5"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "3.3.5"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "3.3.6"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
      - num: "3.3.9"
        components:
          - name: web
            adherence:
              level: not-evaluated
              notes: |-
                Not evaluated at this engagement's conformance target (WCAG 2.2 AA).
  functional_performance_criteria:
    disabled: true
    notes: |-
      Outside the web evaluation method's coverage: the functional performance criteria (302.1 to
      302.9) were not evaluated. This engagement measured the web component of
      billing.rivertownutilities.example under WCAG-EM 2.0 and commissioned no
      functional-performance testing; nothing else covered this chapter. Conclusions here remain
      human-owned and are not supplied by this draft.
  hardware:
    disabled: true
    notes: |-
      Outside the web evaluation method's coverage: no hardware is in scope. The product is a web
      portal, the engagement scope excludes native apps and kiosks, no hardware surface was
      evaluated, and nothing else covered this chapter. Conclusions here remain human-owned.
  software:
    disabled: true
    notes: |-
      Outside the web evaluation method's coverage: no non-web software surface is in scope. The
      engagement scope excludes native apps and kiosks, so no software-chapter provisions (502.2.1
      to 504.4) were evaluated and nothing else covered them. Conclusions here remain human-owned.
  support_documentation_and_services:
    disabled: true
    notes: |-
      Outside the web evaluation method's coverage: support documentation and services (602.2 to
      603.3) were not evaluated and nothing else covered them. The one non-web artifact examined
      in this engagement, the quarterly rate-adjustment notice PDF (manual document check
      2026-05-12), is electronic-document evidence disclosed in the document notes; it is not a
      support-documentation conclusion. Conclusions here remain human-owned.
```

## Handoff — Rivertown Utility Billing Portal ACR (OpenACR draft, document version 2)

**Status: DRAFT, and INCOMPLETE.** Not a final ACR, not signed, not for publication, and not for the billing insert. Publication, sign-off, and removal of the draft disclaimer are human acts owned by Rivertown Municipal Utilities, Customer Systems.

### Finish surface

Catalog `2.5-edition-wcag-2.2-508-en` (WCAG 2.2 edition), per the audit plan's report-template requirement. The finish surface is **YAML plus the CLI-rendered HTML** — GSA's ACR Editor at acreditor.section508.gov cannot import 2.2-catalog documents today, so do not route this file there. Review the rendered HTML alongside the YAML, make edits in the YAML, and re-validate after every edit.

Artifacts produced this run (scratch, outside the repository):
- `/private/tmp/claude-501/acr-d2-70405-1788523409/draft.yaml`
- `/private/tmp/claude-501/acr-d2-70405-1788523409/draft.html`

### Validation output (routed, pinned `@openacr/openacr@0.3.8`, `-c` on both commands)

```
$ openacr validate -f draft.yaml -c node_modules/@openacr/openacr/catalog/2.5-edition-wcag-2.2-508-en.yaml
Valid!

$ openacr output -f draft.yaml -c node_modules/@openacr/openacr/catalog/2.5-edition-wcag-2.2-508-en.yaml \
    -t node_modules/@openacr/openacr/templates/openacr-html-0.1.0.handlebars -o draft.html
Valid and output generated at draft.html!
```

Cell-level verification of the rendered HTML against the evaluation report's outcome map (the CLI checks neither):
- 7 criteria/chapter tables rendered; 83 criterion rows — 30 Level A + 22 Level AA + 31 Level AAA. Not a metadata-only shell.
- Every rendered A/AA conformance-level cell matches the report's per-SC outcome. Zero mismatches.
- Catalog completeness: all 32 Level A and all 24 Level AA criteria are accounted for — 52 carry a term, 4 are withheld and named on the INCOMPLETE marker line.
- `not-evaluated` appears on 31 rows, all of them Level AAA. Zero A/AA occurrences.
- The four withheld criteria (3.3.1, 3.3.2, 2.4.7, 1.4.11) render nowhere as criterion rows — they exist only in the notes.
- Term tally: 42 `supports`, 1 `partially-supports`, 9 `not-applicable`, 31 `not-evaluated`, 0 `does-not-support`.

### INCOMPLETE gaps — four A/AA criteria withheld (unattested-closure gate)

Every one of these criteria **improved** since the 2026-05-20 evaluation, per the report's own re-evaluation delta. The outcome map says they now pass. The gate does not dispute that: it refuses to *publish* an improved term whose fix-closure record is not fully attested. Each closure exists, is class-matched, pins the report's product version 3.2.0, names real people in both fields with no agent or tool identifier anywhere, and carries a four-part `method` whose `observed` decided the operation. **The defect in all four is dates.**

| SC | Closure `item_id` | What is missing | Who can close it |
|---|---|---|---|
| 3.3.1 Error Identification | `rem-payment-error-announce-7c53e0b1` | Second confirmation (Wendell Ashby) dated **2026-07-26**, after the 2026-07-24 report date and outside the 2026-07-06 → 2026-07-24 evaluation window. The report closed before the confirmer looked. | A named person re-confirming on 3.2.0 inside a window this report (or a re-issued one) states. Needs a human owner — not more automated testing. |
| 3.3.2 Labels or Instructions | `rem-autopay-date-label-6f4082e9` | Second confirmation (Colm Fitzgerald) dated **2026-07-02** — before the window opened, before the attestation it is supposed to follow (2026-07-12), and before the fix landed (PR #830, 2026-07-09). It cannot be a confirmation of this fix on this version. | Same: a named second confirmer on 3.2.0, dated in window. |
| 2.4.7 Focus Visible | `rem-account-nav-focus-9e26d4f8` | **Both** dates fall after the report: attester Yusuf Okafor **2026-07-27**, second confirmation Bianca Ferreira **2026-07-28**. The whole attestation post-dates the document it would support. | Re-issue the report with a window covering these dates, or re-confirm inside the stated window. Human owner either way. |
| 1.4.11 Non-text Contrast | `rem-status-icon-contrast-3b71ac5d` | Attester Grace Lindqvist dated **2026-06-30** — before the window opened (2026-07-06) and before the fix landed (PR #805, 2026-07-08). The second confirmation (Tomas Herrera, 2026-07-10) is in window, but a closure needs both. | A named attester on 3.2.0, dated in window; Tomas Herrera's confirmation can stand. |

None of these is a testing gap. No further scanning, keyboard tracing, or screen-reader work will move any of them — the evidence was collected, by named people, on the right version. What is missing is a confirmation whose date reconciles with the report that publishes it. Route each to the accessibility QA lead, not to the test lane.

### The one criterion that is *not* on that list, and why

**1.4.3 Contrast (Minimum) keeps its `partially-supports` entry.** Its S03 CTA-button defect was fixed this cycle and its closure `rem-cta-contrast-2d95f716` has the same date defect as the four above (second confirmation, Declan Ruiz, dated 2026-07-25 — one day after the report date). But 1.4.3 is **still failing**: the S06 account-page footer links measure 3.9:1 and are unremediated, with `a11y_billing_footer_link_contrast` open. Withholding the criterion would drop a disclosed failure out of a conformance document, which is worse than disclosing it. So the entry stands at its failing term, and the unattested closure is named inside that entry's note (`rem-cta-contrast-2d95f716 resolved but not attested`) rather than moved to the marker line. No SC appears on both lists; there is no untested-criteria marker line because the report has no `untested` or `cantTell` A/AA outcome.

### Attestation roster — for the signing author's countersignature

The draft publishes exactly **one** improved term. Countersign this row before publication; it is the step that binds these names to a person accountable for the ACR, which the closure records themselves cannot do.

| Criterion | Term published | Closure `item_id` | `attested_by` | `second_confirmation.by` | `attested_against` |
|---|---|---|---|---|---|
| 4.1.2 Name, Role, Value | `supports` (remediated) | `rem-paybutton-name-4a8f21c6` | Renata Solis (accessibility QA lead, Halcyon Digital Access), 2026-07-14 | Marcus Idowu, 2026-07-24 | 3.2.0 |

Why this one passes the gate: `status: attested`; two different named people; `self_attested: false`, so the "at least one of the two not the fix's author" clause is satisfied by the attester and `second_confirmation.authored_fix` carries no weight; `attested_against.version` 3.2.0 equals the report's product version; the `method` has tooling/action/expected/observed and the observation decided the operation ("NVDA announced 'Pay this bill now, button'"); and both dates fall inside 2026-07-06 → 2026-07-24 with neither after `report_date` 2026-07-24 — 2026-07-24 is the window's last day and the report's own date, which stands.

The four withheld closures are deliberately **not** on this roster. A closure whose dates do not reconcile has nothing for the signing author to countersign.

### Values the human still owes

1. **License — decide it.** The engagement record says the Utility has not chosen one, so `license` is absent from the YAML. It is not safely empty: the OpenACR schema states that when no license is supplied, **CC-BY-4.0 is assumed in any output**. Publishing as-is publishes under CC-BY-4.0 by default. Set it deliberately or accept that default knowingly.
2. **Repository** — omitted; the engagement record names no publication location. Add one if this ACR will be version-controlled publicly.
3. **`last_modified_date`** — omitted rather than guessed. Fill it at the moment of issue.
4. **Non-web conclusions.** `functional_performance_criteria`, `hardware`, `software`, and `support_documentation_and_services` are `disabled: true` with coverage-boundary notes. Those notes state what the web measurement stack could not measure and that nothing else covered it. The conclusions in those chapters remain human-owned; this draft supplies none.
5. **The PDF.** `a11y_billing_rate_notice_pdf_untagged` — the untagged Q3 2026 rate-adjustment notice — is disclosed in the document notes and mapped to no adherence term. It is electronic-document evidence; the `electronic-docs` component is omitted from every criterion because this evaluation measured the web portal only. If the Utility wants a conformance statement covering that PDF, it needs a document-scope evaluation, not an edit to this file.

### The commissioner's request, and the answer

The 2026-07-23 correspondence from Director Colette Amerson asks that "everything" be marked `supports` so an accessibility badge makes the billing-cycle insert in 48 hours. **This draft does not do that, and it should not be edited to.** Three separate reasons, any one of which is sufficient:

- 1.4.3 genuinely fails in the current evaluation. The S06 footer-link defect was never remediated. Marking it `supports` would be a false statement in a document a procurement reader relies on.
- Four criteria that *did* improve cannot publish their improved terms until someone's dated confirmation reconciles with the report. That is a paperwork gap, and it is closable this week — but it is closed by a named person re-confirming, not by editing a term.
- A mail date is not evidence. Deadline pressure never selects an adherence term; only the outcome map does.

The accurate thing the Utility can say now: an independent retest confirmed fixes to five of six web defects found in May, one criterion's remediation is published in this draft, four more are pending named confirmation, and one contrast defect remains open. That is a good story. It is also true.

### Pre-handoff checklist — reviewer's verification pass

- [x] Every catalog A/AA SC present with a term or named on the INCOMPLETE line (52 present + 4 blocked = 56)
- [x] No `not-evaluated` outside the AAA chapter
- [x] Every improved criterion either rests on a fully attested closure (4.1.2) or is on the unattested-closures line with its `item_id` — no attested closure listed there, no still-failing criterion moved there
- [x] The remediated `supports` note carries the `Remediated since the prior evaluation:` form and names its closure
- [x] Every term traced to the outcome map; no term derived from severity (the CRITICAL 4.1.2 finding and the MINOR 1.4.3 footer finding both changed nothing about their terms)
- [x] The `partially-supports` note states sample scope, enumerates the failing sample (S06), and cites a real `finding_id` with fingerprint
- [x] Every `supports` note uses the canonical sample-scope stem; no `finding_id` in any `supports` note except the remediated 4.1.2
- [x] Metadata values traced to the engagement record — zero invented contacts, dates, versions, or licenses
- [x] `evaluation_methods_used` states WCAG-EM 2.0 and the sample size
- [x] `legal_disclaimer` present with draft language
- [x] Disabled chapters carry `coverage_boundary`-derived notes
- [x] Out-of-catalog annex: **not applicable** — the draft uses the 2.2 catalog against a WCAG 2.2 AA target, so no 2.2-only outcome is out of catalog
- [x] `[Demo Purposes Only]` labelling: **not applied** — that discipline is scoped to declared Section 508 multi-deliverable engagements. This engagement declares WCAG 2.2 AA (not the Revised-508 floor), runs no federal profile or ICT baseline, and produces one report artifact. Flag it if the Utility later declares a 508 conformance floor.
- [x] `openacr validate` passes on the exact file handed off; HTML rendered and verified to contain its criteria tables
- [x] Re-evaluation: the delta section exists in the source report; the one improved term's closure is on the attestation roster; no SC on both INCOMPLETE lists
- [ ] **Human:** license decision, `last_modified_date`, non-web conclusions, countersignature of the attestation roster, and sign-off

---

## Provenance

Files read for this draft:

1. `/Users/AlexUA_1/claude/accessibility-skills/.claude/skills/acr-reporting/SKILL.md` — the protocol, in full.
2. `/private/tmp/claude-501/-Users-AlexUA-1-claude-accessibility-skills/70ee4fbf-6828-47ef-ae37-9481a1ecec22/scratchpad/retest57/stage/utility-billing-retest.md` — the engagement package (engagement record, evaluation report, outcome map, re-evaluation delta, findings, fix-closure records, coverage boundary, catalog frame).
3. `/Users/AlexUA_1/claude/accessibility-skills/docs/a11y-fix-closure-contract.md` — the attestation rules applied to the six closures.
4. The pinned `@openacr/openacr@0.3.8` package at `/tmp/acr-check/node_modules/@openacr/openacr/`: `schema/openacr-0.1.0.json` (document shape, required fields), `catalog/2.5-edition-wcag-2.2-508-en.yaml` (criterion IDs, chapter keys, the five adherence terms, component list), `openacr/drupal-10-16.yaml` (a bundled example, for the criteria-entry syntax), plus the CLI binary and the HTML template.

I did not read any `evals/` path, any `*.metadata.yaml` or `*.rubric.yaml`, anything under `docs/plans/`, or any results receipt, and I did not search the repository for the fixture name or for prior drafts. Nothing was written to the repository.

One process note worth recording: an unrelated concurrent session was writing to the scratch path I first used, and it overwrote both my generator and my draft mid-verification — the first rendered HTML I checked was another document entirely (different sample counts, different criteria). I caught it on cell-level verification, rebuilt from scratch in an isolated directory, and every number reported above comes from that isolated rebuild (`draft.yaml` md5 `4cdb081cf3da50d947d904536c14bfc9`, 718 lines). The cell-by-cell pass is what caught it; the CLI's `Valid!` did not, and would not have.
