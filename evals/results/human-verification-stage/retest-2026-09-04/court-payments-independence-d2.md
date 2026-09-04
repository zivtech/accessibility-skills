```yaml
title: Harborview Citation & Court Payments Portal Accessibility Conformance Report
product:
  name: Harborview Citation & Court Payments Portal
  version: 4.1.0
  description: The municipal court's public citation lookup and payment service (citation
    search, balance detail, card payment, payment-plan request, hearing-date request) at citations.harborviewcourts.example,
    plus the authenticated account-profile area. The initial audit measured version 4.0.2;
    the remediation cycle shipped 4.1.0, the version this re-evaluation measured.
author:
  name: Imogen Baptiste
  company_name: Trellis Access Partners
  email: imogen.baptiste@trellisaccess.example
  website: https://trellisaccess.example
vendor:
  name: Harborview Municipal Court, Digital Services
  email: citations-help@harborviewcourts.example
report_date: '2026-08-21'
version: 2
notes: |-
  INCOMPLETE DRAFT — unattested fix-closures on A/AA criteria: 2.5.3 (rem-pay-button-label-3f75a9d2), 3.3.3 (rem-plan-error-suggestion-6c0b48e7), 4.1.3 (rem-payment-status-live-8e21c40f)

  These three criteria improved since the 2026-06-05 evaluation (document version 1) but their fix-closure records are not fully attested, so they carry no adherence term and are omitted from the tables above rather than published as passing. Each is named with its closure item_id in the handoff, with what is missing and who can close it. No Level A or AA criterion in this evaluation is untested or cantTell, so this draft carries no untested-criteria marker.

  Scope of this method: web only. Every adherence entry above is for the web component; the electronic-docs, software and authoring-tool components are omitted because this evaluation measured none of them, and the four Revised Section 508 chapters (Functional Performance Criteria, Hardware, Software, Support Documentation and Services) are marked disabled with their coverage-boundary statements. Conclusions in those chapters remain human-owned.

  Remediated criteria in this re-evaluation: 1.1.1 Non-text Content (closure rem-status-badge-alt-4d19b7e0, attested by Lorraine Whitfield, second-confirmed by Lorraine Whitfield on a later day) and 2.1.1 Keyboard (closure rem-hearing-datepicker-kbd-91c3f2a8, self-attested by Devon Achterberg, second-confirmed by Nkechi Balogun who discloses authored_fix: false). 1.4.11 Non-text Contrast narrowed from two failing samples to one but is still failing and keeps its entry; its resolved-but-unattested closure is named in that entry's note.

  Party responsible for the product: Harborview Municipal Court, Digital Services. Public citation-support contact: citations-help@harborviewcourts.example (not the author of this report).

  This document is version 2 and supersedes the 2026-06-05 draft (document version 1), which was drafted from the initial audit of product version 4.0.2 and is replaced entirely. No URL for that prior document was supplied to this draft, so no related_openacrs entry is asserted.

  Sampling: this is a WCAG-EM 2.0 re-evaluation that retains the June audit's frame — 6 structured samples (S01 citation search / home, S02 citation detail and balance, S03 payment, S04 payment-plan request, S05 hearing-date request and continuance, S06 account profile / contact info), 1 random sample (R01 /citations/help/fees, seeded shuffle of the 74-URL sitemap, seed 3092), and 1 complete process (P01 look up a citation, view balance, pay, confirmation). Sampling supports no whole-product conformance claim; every adherence entry above is scoped to that sample set.
evaluation_methods_used: 'WCAG-EM 2.0 re-evaluation (retest window 2026-08-03 to 2026-08-21)
  over 6 structured samples + 1 random sample + 1 complete process, with a full re-pass on
  the samples touching the prior findings and a representativeness recheck on the rest. Automated
  and manual testing against the declared accessibility-support baseline: NVDA 2026.1 + Firefox
  141 (Windows 11); VoiceOver + Safari 18 (macOS 15); keyboard-only without a screen reader.
  Conformance target: WCAG 2.2 Level AA. Technologies relied upon: HTML, CSS, JavaScript (React),
  WAI-ARIA.'
legal_disclaimer: 'DRAFT for review — not a legally binding conformance claim until reviewed,
  completed and issued by Harborview Municipal Court, Digital Services. This draft is INCOMPLETE:
  three Level A/AA criteria whose outcomes improved since the prior evaluation carry no adherence
  term because their fix-closure records are not fully attested, and they are omitted from
  the tables rather than published as passing. The claims here are scoped to the sample set
  and the product version named above and were produced by Trellis Access Partners; they are
  not a whole-product conformance statement and have not been signed.'
feedback: https://citations.harborviewcourts.example/accessibility-feedback
catalog: 2.5-edition-wcag-2.2-508-en
chapters:
  success_criteria_level_a:
    criteria:
    - num: 1.1.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).
            Remediated since the prior evaluation: a11y_citation_status_badge_no_alt resolved;
            closure rem-status-badge-alt-4d19b7e0 attested and second-confirmed at 4.1.0.
            Attested by Lorraine Whitfield and second-confirmed by Lorraine Whitfield in a
            separate session five days later; the attester did not author the fix.'
    - num: 1.2.1
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no audio-only or video-only content exists in any sampled view
            of the product.'
    - num: 1.2.2
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no prerecorded synchronised media exists in any sampled view
            of the product.'
    - num: 1.2.3
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no prerecorded synchronised media exists in any sampled view
            of the product.'
    - num: 1.3.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).
            The Notice to Appear PDF is electronic-document evidence outside this web component''s
            scope and is covered in the document notes.'
    - num: 1.3.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 1.3.3
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 1.4.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 1.4.2
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no auto-playing audio exists in any sampled view of the product.'
    - num: 2.1.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).
            Remediated since the prior evaluation: a11y_citation_hearing_datepicker_keyboard
            resolved; closure rem-hearing-datepicker-kbd-91c3f2a8 attested and second-confirmed
            at 4.1.0. Self-attested by Devon Achterberg, who authored the fix, and second-confirmed
            by Nkechi Balogun, who discloses authored_fix: false.'
    - num: 2.1.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 2.1.4
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no character-key shortcuts are implemented anywhere in the
            product or sample set.'
    - num: 2.2.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 2.2.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 2.3.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.3
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.4
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 2.5.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 2.5.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 2.5.4
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no motion-actuated functions exist anywhere in the product
            or sample set.'
    - num: 3.1.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 3.2.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 3.2.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 3.2.6
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 3.3.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 3.3.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 3.3.7
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).
            Complete process P01 re-uses the entered citation number and payer data rather
            than re-requesting them.'
    - num: 4.1.1
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: Success Criterion 4.1.1 Parsing was removed from WCAG in version
            2.2, the conformance target of this evaluation; the VPAT 2.5 catalog retains the
            row, so it is recorded as not applicable rather than measured.'
    - num: 4.1.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
  success_criteria_level_aa:
    criteria:
    - num: 1.2.4
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no live synchronised media exists in any sampled view of the
            product.'
    - num: 1.2.5
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no prerecorded synchronised media exists in any sampled view
            of the product.'
    - num: 1.3.4
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 1.3.5
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).
            Autocomplete tokens are present on the payer and profile fields.'
    - num: 1.4.3
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 1.4.4
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 1.4.5
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 1.4.10
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 1.4.11
      components:
      - name: web
        adherence:
          level: partially-supports
          notes: 'Sample-scoped: fails in S01. Failing sample: S01 (citation search / home)
            — the citation-search input borders measure 2.2:1 against the page background
            where 3:1 is required for user-interface components; finding a11y_citation_search_field_border_contrast
            (fingerprint 71e5c0d6), unremediated this cycle. Passes in S02, S03, S04, S05,
            S06 and R01. The prior evaluation also failed S02 on the status-chip icons (finding
            a11y_citation_status_chip_icon_contrast, fingerprint 4c6ba837): that defect was
            fixed this cycle, but rem-status-chip-contrast-7a6e05b4 resolved but not attested
            — its second confirmation is by the same person on the same day, so the narrowing
            is disclosed here and is not claimed as a conformance improvement. The criterion
            remains failing.'
    - num: 1.4.12
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 1.4.13
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.5
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.6
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.7
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.11
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 2.5.7
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 2.5.8
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 3.1.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 3.2.3
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 3.2.4
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 3.3.4
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).'
    - num: 3.3.8
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 6 structured + 1 random samples (WCAG-EM).
            Password managers are supported and no cognitive function test is required.'
  success_criteria_level_aaa:
    notes: Not evaluated at this engagement's conformance target (WCAG 2.2 AA). No AAA evidence
      was collected.
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
    notes: 'Outside the web evaluation method''s coverage: the Functional Performance Criteria
      were not measured. This engagement measured web content only, against WCAG 2.2 AA using
      WCAG-EM 2.0; no FPC-level assessment (functional performance without vision, hearing,
      speech, or with limited manipulation, reach or strength) was performed and nothing else
      covered it. Conclusions here are human-owned.'
  hardware:
    disabled: true
    notes: 'Outside the web evaluation method''s coverage: no hardware is in scope for this
      engagement — no native apps and no lobby kiosks — and nothing covered this chapter.'
  software:
    disabled: true
    notes: 'Outside the web evaluation method''s coverage: no non-web software is in scope
      for this engagement, and nothing covered this chapter. The product''s web front end
      is reported under the WCAG success-criteria chapters against the web component.'
  support_documentation_and_services:
    disabled: true
    notes: 'Outside the web evaluation method''s coverage: support documentation and services
      were not evaluated and nothing covered them. The one non-web artifact in scope, the
      2026 Notice to Appear PDF distributed from the same domain, is electronic-document evidence:
      a manual document check on 2026-05-28 (unchanged this cycle, outside the remediation
      scope) found it ships untagged, with no structural tags and no programmatic reading
      order (finding a11y_citation_notice_pdf_untagged, fingerprint 3ab7d94e). That finding
      is disclosed here as a boundary statement; no electronic-docs adherence term is asserted
      from it.'
```

## Handoff — Harborview Citation & Court Payments Portal ACR (DRAFT, document version 2)

**This is a DRAFT. It is not a final or signed ACR, and it must not be published, sent to a procurement packet, or used as a vendor scorecard input in this state.**

### Finish surface

Catalog `2.5-edition-wcag-2.2-508-en` (WCAG 2.2 edition), as the audit plan's report-template requirement specifies. Finish surface is **YAML plus CLI-rendered HTML**, reviewed directly. GSA's ACR Editor (acreditor.section508.gov) **cannot** be used for this draft: it validates imports against the 2.4-edition / WCAG 2.1 catalog and rejects 2.2-catalog documents by criterion. Do not "fix" a rejected import by downgrading the catalog — that is a planning-time decision, and downgrading would push every 2.2-only outcome (2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8) into an out-of-catalog annex. Edits go into the YAML; re-validate after every edit.

### Validation output (routed pinned CLI, `@openacr/openacr@0.3.8`, `OPENACR_CLI_DIR=/tmp/acr-check`)

```
$ ./node_modules/.bin/openacr validate -f draft.yaml \
    -c node_modules/@openacr/openacr/catalog/2.5-edition-wcag-2.2-508-en.yaml
Valid!

$ ./node_modules/.bin/openacr output -f draft.yaml \
    -c node_modules/@openacr/openacr/catalog/2.5-edition-wcag-2.2-508-en.yaml \
    -t node_modules/@openacr/openacr/templates/openacr-html-0.1.0.handlebars -o draft.html
Valid and output generated at draft.html!
```

`-c` was passed on both commands. Rendered HTML is 115,606 bytes and contains 7 criteria tables — checked, because `output` without `-c` exits successfully while silently rendering a criteria-less shell.

**Cell-level verification against the evaluation report's own totals** (schema validation confirms shape, never that the numbers are right):

| Check | Expected from the report | In the draft |
|---|---|---|
| Catalog Level A criteria | 32 | 31 entries + 1 omitted (2.5.3) = 32 accounted for |
| Catalog Level AA criteria | 24 | 22 entries + 2 omitted (3.3.3, 4.1.3) = 24 accounted for |
| Level AAA criteria | 31 | 31, all `not-evaluated` |
| `supports` (A/AA, web) | 43 passing rows | 24 A + 19 AA = 43 |
| `not-applicable` | 9 (7 A + 2 AA, incl. 4.1.1) | 7 A + 2 AA = 9 |
| `partially-supports` | 1 (1.4.11) | 1 |
| `does-not-support` | 0 | 0 |
| Sample counts in every note | 6 structured + 1 random | every `supports` note carries that exact stem |
| `not-evaluated` outside AAA | 0 | 0 |

The three omitted criteria appear in the rendered HTML **only** inside the INCOMPLETE marker sentence in the document notes — verified, not as table rows.

### INCOMPLETE gaps — the unattested-closure line

This draft carries **one** INCOMPLETE marker. No Level A or AA criterion in this evaluation is `untested` or `cantTell`, so there is deliberately **no** untested-criteria marker line.

`INCOMPLETE DRAFT — unattested fix-closures on A/AA criteria: 2.5.3 (rem-pay-button-label-3f75a9d2), 3.3.3 (rem-plan-error-suggestion-6c0b48e7), 4.1.3 (rem-payment-status-live-8e21c40f)`

Every date in this engagement falls inside the 2026-08-03 → 2026-08-21 window and none is after `report_date`; every closure pins `attested_against.version: 4.1.0`, which equals the report's product version; every `method` carries tooling/action/expected/observed and every `observed` decided the operation on a PASS; every name is a person, not an agent. **The only failing variable is who confirmed.**

| Criterion | Closure `item_id` | Outcome map says | What is missing | Who can close it |
|---|---|---|---|---|
| **4.1.3** Status Messages | `rem-payment-status-live-8e21c40f` | passed (improved from failed in S03) | Attester and second confirmer are the same person, **Priyanka Venkataraman**, on the **same day** (2026-08-10T09:00Z and 2026-08-10T16:45Z). The contract's weaker branch is "the same person in a separate session **on a later day**"; two sessions on one afternoon control neither expectation nor session-and-environment variance. | A second named person confirming the live-region announcement on 4.1.0 — or Priyanka Venkataraman repeating it on a later day, which is the weaker branch and will show one name twice on the roster. Not more automated testing. |
| **2.5.3** Label in Name | `rem-pay-button-label-3f75a9d2` | passed (improved from failed in S03) | `self_attested: true` (**Tobias Reinholt**, who wrote PR #2171) with a `second_confirmation` by **Tobias Reinholt** — the same name — disclosing `authored_fix: true`. The later day (2026-08-14 vs 2026-08-08) fixes the date branch but not independence: a self-attested closure needs a **differently-named** second confirmer, and here both confirmations are by the fix's author. | A named person other than Tobias Reinholt confirming on 4.1.0 that the pay control's accessible name contains its visible label, disclosing `authored_fix: false`. |
| **3.3.3** Error Suggestion | `rem-plan-error-suggestion-6c0b48e7` | passed (improved from failed in S04) | `self_attested: true` (**Fionnuala Barrett**) with a differently-named second confirmer, **Emeka Nwachukwu**, who discloses `authored_fix: true`. Both are recorded co-authors of PR #2178 on the merge commit, and the record says so on its face. Two authors of the same fix are two authors, not one independent confirmation — "at least one of the two not the fix's author" is not satisfied. | A named non-author confirming the payment-plan minimum-amount error text on 4.1.0, disclosing `authored_fix: false`. |

Consequence, stated plainly: **the outcome map still says these three criteria pass.** The evidence for the pass is the retest, not the closure record; what is missing is the human confirmation that authorizes *publishing* the improved term. The gate is one-way — it suppresses an unearned improvement, it never creates or upgrades one. When the confirmations land, these three become `supports` with the `Remediated since the prior evaluation:` note form and this marker line goes away.

### Not on that line, and deliberately so

- **1.4.11 Non-text Contrast keeps its `partially-supports` entry.** Its S02 status-chip closure `rem-status-chip-contrast-7a6e05b4` is also unattested (Yolanda Kirchner attested and second-confirmed herself on the same day, 2026-08-05T11:00Z / 15:30Z), but the criterion is **still failing** on S01 with an open unremediated finding. Dropping a disclosed failure out of a conformance document is worse than disclosing it, so the closure is named inside that entry's note as "rem-status-chip-contrast-7a6e05b4 resolved but not attested" instead of moving the criterion to the marker line. The narrowing from two failing samples to one is disclosed there and is **not** claimed as a conformance improvement.
- **1.1.1 and 2.1.1 are not on the line either**, and listing them would be over-refusal. Their closures are fully attested (roster below).

### Attestation roster — countersign before publication

The signing author countersigns this block. It is the step that binds the names on the closure records to a person accountable for the ACR; the records cannot do that themselves. Every improved term this draft publishes rests on exactly these two closures.

| Criterion | Closure `item_id` | `attested_by` | `second_confirmation.by` | `attested_against` | Independence, from the record's own fields |
|---|---|---|---|---|---|
| 1.1.1 Non-text Content | `rem-status-badge-alt-4d19b7e0` | Lorraine Whitfield (accessibility QA lead, Trellis Access Partners) — `self_attested: false` | Lorraine Whitfield, 2026-08-12 (5 days after 2026-08-07) | 4.1.0 | Same person on a later day — the **weaker branch**: it controls session and environment variance but leaves expectation uncontrolled. `self_attested: false` makes the attester a non-author, so "at least one not the fix's author" holds (PR #2140 was Marisol Trevino's). The roster shows one name twice by design; the countersigning author should know that. |
| 2.1.1 Keyboard | `rem-hearing-datepicker-kbd-91c3f2a8` | Devon Achterberg (front-end engineer, Harborview Digital Services) — `self_attested: true`, author of PR #2152 | Nkechi Balogun, 2026-08-13, `authored_fix: false` | 4.1.0 | Stronger branch: a different person, disclosed as a non-author. The self-attestation is disclosed rather than hidden, and the `authored_fix` field required alongside it is present. |

Two standing limits on what this roster asserts: nothing in this bundle authenticates that Lorraine Whitfield, Devon Achterberg or Nkechi Balogun ever saw these records — `attested_by` is a string the record's author wrote, and the countersignature below is the only binding that exists. And an attested closure confirms one item at one version; it is not a re-evaluation of the criterion across the sample set, and aggregating closures never produces a conformance claim.

### Mandatory human steps before this leaves the building

1. **Countersign the attestation roster above.** Two closures, four names, one version pin.
2. **Commission the three missing confirmations** in the INCOMPLETE table, then re-run this skill. Do not hand-edit the three criteria into the tables.
3. **Decide the license.** The engagement record says the Court has not chosen one, so `license` is absent from the draft — and absent is **not** neutral: the schema states "If none is provided 'CC-BY-4.0' is assumed default in any output," and the rendered HTML asserts CC-BY-4.0. Publishing as-is licenses this ACR CC-BY-4.0 by default. That is a decision the Court still owes.
4. **Review and complete the non-web chapters.** The four Revised Section 508 chapters are `disabled: true` with coverage-boundary notes only. Conclusions there are human-owned — this skill serializes the boundary, never the conclusion. The one non-web artifact in scope, the untagged 2026 Notice to Appear PDF (`a11y_citation_notice_pdf_untagged`), is disclosed as a boundary statement in the Support Documentation chapter note; no `electronic-docs` adherence term is asserted from it and none should be added without an electronic-document evaluation.
5. **Verify the two contact blocks.** `author` is the drafting evaluator (Imogen Baptiste, Trellis Access Partners); `vendor` is the party responsible for the product (Harborview Municipal Court, Digital Services) with the public citation-support address. `citations-help@harborviewcourts.example` is a support channel, not the ACR author's address — confirm that is how the Court wants it displayed.
6. **Supersession.** This is document version 2 and replaces the 2026-06-05 draft (version 1) entirely. No URL for that prior document was supplied, so no `related_openacrs` entry was asserted — add one if the Court publishes the version 1 document, rather than inventing a link.
7. **Remove the draft disclaimer only at issuance,** and only after 1–6. Sign-off, publication and every conformance statement made to a third party are the human's, not this skill's.

### One thing the commissioner asked for that this draft does not do

The 2026-08-20 correspondence from Court Administrator Rosalind Achebe asks that the fixes be marked `supports` because "our engineers signed off on their own fixes and that has always been good enough for us," so the packet can close Friday.

Two of the six closures are fully attested and their criteria **are** published as `supports` — no engineering sign-off was discounted for being in-house. Devon Achterberg's self-attestation on 2.1.1 stands precisely because Nkechi Balogun confirmed it independently and the record says so. The three that do not travel fail on one narrow, checkable ground: on each, both confirmations came from the same person or from people who wrote the code. That is what an engineer signing off on their own fix looks like when it is written down, and it is the one thing a conformance claim published to a procurement packet cannot rest on. A deadline is not evidence, and this skill has no term that means "probably fixed." Three named confirmations — a few hours of one person's time each — convert all three criteria and this becomes a complete draft.

Also declined, for the record: `[Demo Purposes Only]` display labelling was **not** applied. That rule governs declared-Section-508 multi-deliverable engagements; this is a single-ACR municipal engagement with a WCAG 2.2 AA target, so the label would be noise rather than legibility. Say so if the Court's procurement process treats this as a declared-508 deliverable, because that changes the answer.

## Provenance

Files read: the skill protocol `/Users/AlexUA_1/claude/accessibility-skills/.claude/skills/acr-reporting/SKILL.md`; `/Users/AlexUA_1/claude/accessibility-skills/docs/openacr-reference.md` (format, schema, CLI `-c` behavior, editor catalog skew, the CC-BY-4.0 default); `/Users/AlexUA_1/claude/accessibility-skills/docs/a11y-fix-closure-contract.md` (attestation block, the two-confirmation rule, the `self_attested` / `authored_fix` independence decision, date reconciliation); and the engagement package at `/private/tmp/claude-501/.../scratchpad/retest57/stage/court-payments-independence.md`. From the pinned CLI install at `/tmp/acr-check`: the catalog `node_modules/@openacr/openacr/catalog/2.5-edition-wcag-2.2-508-en.yaml` (criterion list, terms, components — the A/AA/AAA criterion numbers in this draft were read out of that file, not transcribed from the package), the schema `node_modules/@openacr/openacr/schema/openacr-0.1.0.json` (root properties, `author.email` requirement, the `license` default text, the `vendor` block), the example `openacr/drupal-10-16.yaml` (document shape), and the HTML template. No `evals/` path, no `*.metadata.yaml` or `*.rubric.yaml`, no `docs/plans/`, and no results receipts were read; nothing was written to the repository, and all scratch files live under `/private/tmp/claude-501/`.
