```yaml
title: Millbrook County Library Catalog Accessibility Conformance Report
product:
  name: Millbrook County Library Catalog
  version: 5.3.1
  description: The county library system's public search catalog, holds, digital-collection access, and
    patron account portal (catalog.millbrookcolibrary.example).
author:
  name: Priya Ostrander
  company_name: Fernbank Access Partners
  email: priya.ostrander@fernbankaccess.example
  website: https://fernbankaccess.example
vendor:
  company_name: Millbrook County Library System, Digital Services
  email: digital@millbrookcolibrary.example
report_date: '2026-08-28'
version: 2
notes: 'INCOMPLETE DRAFT — unattested fix-closures on A/AA criteria: 2.4.7 (rem-focus-ring-a17c4e2b),
  2.4.11 (rem-header-offset-2b6f9ac4), 3.3.1 (rem-hold-error-announce-5c9f14e0), 3.3.2 (rem-renewal-label-6d81ecf3).
  Each of these four criteria improved since the 2026-06-12 evaluation, and the fix-closure record its
  improved term would rest on is not fully attested; they therefore carry no adherence entry in this draft
  and are omitted from the criteria tables. The handoff names what each record is missing and who can
  close it.


  Method scope: only the web component is populated. Evidence was collected by a WCAG-EM 2.0 web evaluation
  of catalog.millbrookcolibrary.example; the electronic-documents, software, and authoring-tool components
  were not evaluated and are omitted from every criterion entry. The quarterly PDF program guides are
  electronic-document content outside the web component, covered by a separate manual document check (2026-06-05,
  unchanged this cycle) whose conclusions are human-owned and are not serialized here.


  Re-evaluation: this is document version 2 and supersedes the 2026-06-12 draft (document version 1) entirely.
  It reports a re-evaluation run 2026-08-25 to 2026-08-28 against product version 5.3.1; the initial audit
  measured 5.2.0. Criteria whose outcomes changed since that evaluation are 2.4.7, 2.4.11, 4.1.2, 3.3.1,
  3.3.2 (all improved) and 1.4.11 (still failing, narrower). Only 4.1.2 rests on a fully attested closure
  and publishes its improved term.


  Draft: this document has not been reviewed, signed, or issued. Sample-scoped evidence does not support
  a whole-product conformance claim.'
evaluation_methods_used: 'WCAG-EM 2.0 re-evaluation, run 2026-08-25 to 2026-08-28 against product version
  5.3.1. Sample set: 8 structured samples (S01 home/search landing, S02 search results, S03 item detail
  + place-hold, S04 patron account dashboard, S05 digital-collection e-reader launch, S06 programs & events
  calendar, S07 branch hours & locations, S08 help/FAQ) + 1 random sample (R01 /catalog/collections/local-history-archive,
  seeded shuffle of the 142-URL sitemap, seed 2290) + 1 complete process (P01 search a title, place a
  hold, confirmation). The frame is retained from the 2026-06-12 audit, with a full re-pass on the samples
  touching the prior findings and a representativeness recheck on the rest; the random-sample comparison
  surfaced no new content or finding types. State coverage per sample: default, loading, error, and expanded
  states where the template has them. Automated and manual testing against the accessibility-support baseline:
  NVDA 2026.1 + Firefox 141 (Windows 11); VoiceOver + Safari 18 (macOS 15); keyboard-only without a screen
  reader. Technologies relied upon: HTML, CSS, JavaScript (Angular), WAI-ARIA. Conformance target: WCAG
  2.2 Level AA.'
legal_disclaimer: 'Draft for review — not a legally binding conformance claim until reviewed and issued
  by Millbrook County Library System, Digital Services. Prepared by Fernbank Access Partners from a sample-scoped
  WCAG-EM 2.0 re-evaluation; sampling alone never supports a whole-product conformance claim. This draft
  is INCOMPLETE: four Level A/AA criteria whose outcomes improved since the prior evaluation carry no
  adherence entry because the fix-closure records behind them are not fully attested.'
feedback: https://millbrookcolibrary.example/accessibility-feedback
catalog: 2.5-edition-wcag-2.2-508-en
chapters:
  success_criteria_level_a:
    notes: 'Sample scope as stated in evaluation methods: 8 structured + 1 random samples + 1 complete
      process, re-passed 2026-08-25 to 2026-08-28 at product version 5.3.1. 30 of the catalog''s 32 Level
      A criteria carry an entry. 3.3.1 Error Identification and 3.3.2 Labels or Instructions are omitted:
      both improved since the 2026-06-12 evaluation and their fix-closure records (rem-hold-error-announce-5c9f14e0;
      rem-renewal-label-6d81ecf3) are not fully attested. Only the web component is populated.'
    criteria:
    - num: 1.1.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 1.2.1
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no audio-only or video-only content exists in the product or in any sampled
            view.'
    - num: 1.2.2
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no prerecorded media exists in the product or in any sampled view.'
    - num: 1.2.3
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no prerecorded media exists in the product or in any sampled view.'
    - num: 1.3.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM). Non-web electronic-document
            content (the quarterly PDF program guides) lies outside the web component and is not covered
            by this entry — see the document notes.'
    - num: 1.3.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 1.3.3
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 1.4.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 1.4.2
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no auto-playing audio exists in the product or in any sampled view.'
    - num: 2.1.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM). Complete process
            P01 (search a title, place a hold, confirmation) was fully keyboard-operable.'
    - num: 2.1.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 2.1.4
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no character-key shortcuts are implemented in the product or in any sampled
            view.'
    - num: 2.2.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 2.2.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 2.3.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.3
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.4
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 2.5.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 2.5.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 2.5.3
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 2.5.4
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no motion-actuated functions exist in the product or in any sampled view.'
    - num: 3.1.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 3.2.1
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 3.2.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 3.2.6
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 3.3.7
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM). Complete process
            P01 re-uses previously entered data.'
    - num: 4.1.1
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: WCAG 2.2 removed this criterion; the VPAT 2.5 catalog retains the row.
            No product content is measured against it at this engagement''s conformance target (WCAG 2.2
            AA).'
    - num: 4.1.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM). Remediated since
            the prior evaluation: a11y_catalog_holds_button_unlabeled resolved; closure rem-holds-btn-name-7f3c88d1
            attested and second-confirmed at 5.3.1. Attested by Marisol Fenn (2026-08-27), second-confirmed
            by Owen Bratcher (2026-08-27); previously failed in S03 at the 2026-06-12 evaluation.'
  success_criteria_level_aa:
    notes: 'Sample scope as for Table 1. 22 of the catalog''s 24 Level AA criteria carry an entry. 2.4.7
      Focus Visible and 2.4.11 Focus Not Obscured (Minimum) are omitted: both improved since the 2026-06-12
      evaluation and their fix-closure records (rem-focus-ring-a17c4e2b; rem-header-offset-2b6f9ac4) are
      not fully attested. Only the web component is populated.'
    criteria:
    - num: 1.2.4
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no live media exists in the product or in any sampled view.'
    - num: 1.2.5
      components:
      - name: web
        adherence:
          level: not-applicable
          notes: 'Not present: no prerecorded media exists in the product or in any sampled view.'
    - num: 1.3.4
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 1.3.5
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM). Autocomplete
            tokens are present on the patron-account fields.'
    - num: 1.4.3
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 1.4.4
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 1.4.5
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 1.4.10
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 1.4.11
      components:
      - name: web
        adherence:
          level: partially-supports
          notes: 'Sample-scoped: fails in S02, S03. Format-type icons — the e-book glyph and the "new
            arrival" badge — in the search-results list and on item-detail badges measure 1.8:1 and 2.1:1
            against the adjacent row background where 3:1 is required (finding a11y_catalog_format_icon_contrast,
            fingerprint 9e02cc45). Remediation item rem-icon-contrast-88be5f13 redrew the DVD and audiobook
            glyphs to 3.2:1 but did not close: the e-book and new-arrival glyphs were outside this release''s
            icon-redesign scope and were re-measured unchanged. Passes on S01, S04, S05, S06, S07, S08
            and R01. The S04 status-icon defect a11y_catalog_status_icon_contrast (fingerprint d47a1e6c)
            was fixed this cycle: rem-status-icon-99a6dd2f resolved but not attested.'
    - num: 1.4.12
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 1.4.13
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.5
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 2.4.6
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 2.5.7
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 2.5.8
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 3.1.2
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 3.2.3
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 3.2.4
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 3.3.3
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 3.3.4
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
    - num: 3.3.8
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM). Password managers
            are supported; no cognitive-function test is required.'
    - num: 4.1.3
      components:
      - name: web
        adherence:
          level: supports
          notes: 'Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM).'
  success_criteria_level_aaa:
    notes: AAA criteria lie outside this engagement's conformance target (WCAG 2.2 Level AA) and no AAA
      evidence was collected.
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
    notes: 'Outside the web evaluation method''s coverage: the functional performance criteria were not
      measured. This engagement''s method is a WCAG-EM 2.0 web evaluation against WCAG 2.2 AA, which produces
      no FPC evidence, and no other activity in this engagement covered them. Conclusions in this chapter
      are human-owned and are not asserted by this draft.'
  hardware:
    disabled: true
    notes: 'Outside the web evaluation method''s coverage: no hardware is in the evaluation scope and
      none was measured. The product is a web application; the engagement scope excludes native apps and
      kiosks. Conclusions in this chapter are human-owned and are not asserted by this draft.'
  software:
    disabled: true
    notes: 'Outside the web evaluation method''s coverage: no non-web software is in the evaluation scope
      and none was measured. Conclusions in this chapter are human-owned and are not asserted by this
      draft.'
  support_documentation_and_services:
    disabled: true
    notes: 'Outside the web evaluation method''s coverage: no support-documentation or support-services
      surfaces are in the evaluation scope and none were measured. The quarterly PDF program guides distributed
      from the same domain are electronic-document content, covered by a separate manual document check
      (2026-06-05, unchanged this cycle) whose conclusions are human-owned and are not serialized here.
      Conclusions in this chapter are human-owned and are not asserted by this draft.'
```

---

# Handoff — Millbrook County Library Catalog ACR (OpenACR DRAFT, document version 2)

**Status: INCOMPLETE DRAFT.** Five criteria improved since the 2026-06-12 evaluation. Exactly one of them (4.1.2) rests on a fully attested fix-closure and publishes its improved term. The other four publish **no adherence term at all** and are omitted from the criteria tables, because the closure records their improved terms would rest on are not fully attested. This is not a final, signed, or publishable ACR.

## Finish surface

2.2-catalog draft (`2.5-edition-wcag-2.2-508-en`, chosen at planning time per the engagement record's report-template requirement — not a fallback). **Review the rendered HTML plus the YAML directly.** acreditor.section508.gov cannot import this document: the editor validates against the 2.4-edition / WCAG 2.1 catalog and rejects 2.2 criteria by number. Edits go into the YAML; re-validate with `-c` after every edit.

No out-of-catalog annex is required. The 2.2 catalog carries every 2.2-only criterion this evaluation measured (2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8), so nothing rides an annex.

## Validation output (routed pinned CLI, `@openacr/openacr@0.3.8`, `-c` on both commands)

```
$ node /tmp/acr-check/node_modules/.bin/openacr validate \
    -f draft.yaml \
    -c node_modules/@openacr/openacr/catalog/2.5-edition-wcag-2.2-508-en.yaml
Valid!

$ node /tmp/acr-check/node_modules/.bin/openacr output \
    -f draft.yaml -c <same catalog> \
    -t node_modules/@openacr/openacr/templates/openacr-html-0.1.0.handlebars -o draft.html
Valid and output generated at draft.html!        # 114,374 bytes

$ node ... -t .../openacr-markdown-0.1.0.handlebars -o draft.md
Valid and output generated at draft.md!          # 30,061 bytes
```

**Cell-level verification of the rendered HTML** (parsed the criteria tables, not just checked they exist — the CLI validates shape, never numbers):

| Rendered table | Rows | Terms counted in cells | Matches the report's outcome map |
|---|---|---|---|
| Table 1, Level A | 30 of the catalog's 32 | supports 23, not-applicable 7 | yes — 7 `inapplicable` rows (1.2.1, 1.2.2, 1.2.3, 1.4.2, 2.1.4, 2.5.4, 4.1.1); 3.3.1 and 3.3.2 correctly absent |
| Table 2, Level AA | 22 of the catalog's 24 | supports 19, partially-supports 1, not-applicable 2 | yes — 2 `inapplicable` (1.2.4, 1.2.5); 1.4.11 the only mixed row; 2.4.7 and 2.4.11 correctly absent |
| Table 3, Level AAA | 31 of 31 | not-evaluated 31 | yes — AAA is the only place the term appears |
| 508 chapters (4) | disabled, notes rendered | — | yes |

Sample tallies in `evaluation_methods_used` and in every `supports` note reconcile to the report's own sample set: 8 structured (S01–S08) + 1 random (R01) + 1 complete process (P01). Finding IDs cited in the draft (2 in the 1.4.11 note, 1 in the 4.1.2 remediated note) all exist in the findings list; no fingerprint or ID was invented.

## INCOMPLETE gaps — the unattested-closure gate (4 criteria, no adherence entry)

Marker line carried verbatim in the document `notes`:
`INCOMPLETE DRAFT — unattested fix-closures on A/AA criteria: 2.4.7 (rem-focus-ring-a17c4e2b), 2.4.11 (rem-header-offset-2b6f9ac4), 3.3.1 (rem-hold-error-announce-5c9f14e0), 3.3.2 (rem-renewal-label-6d81ecf3).`

| SC | Closure `item_id` | What is missing | Who closes it |
|---|---|---|---|
| **2.4.7** Focus Visible | `rem-focus-ring-a17c4e2b` | **No attestation at all** — `status: draft_not_attested`, no `attested_by`, no method, no second confirmation. The closure record itself is a sound engineering record (keyboard trace on 5.3.1, class-matched to a focus-indicator defect); nobody has confirmed it. | A named person on the engagement walks S02's filter chips and S07's accordion headers on **5.3.1**, records action/expected/observed, and a second named person confirms. |
| **2.4.11** Focus Not Obscured (Min) | `rem-header-offset-2b6f9ac4` | Says `status: attested` but **both name fields hold an agent identifier** (`a11y-fix-executor (agent run …)`), which is a misleading status, not an attestation. Compounding: `self_attested: true` with `second_confirmation` omitting `authored_fix` (absence is not independence), and the "second" confirmation is the same identifier 2h26m later the same day — not a different person, and not the same person on a later day. | Two named people. The bounding-rect replay is useful evidence; it is not a human observation. More automated re-runs will not close this. |
| **3.3.1** Error Identification | `rem-hold-error-announce-5c9f14e0` | **Only one confirmation.** Everything else is in order — Grace Okonjo, 2026-08-27, pinned to 5.3.1, four-part method with an `observed` that decided the operation. Its own `claim_boundary` says "No second person has reproduced it." | A second named person reproduces the already-held-item error on S03 at 5.3.1 (a different person, or Grace Okonjo in a separate session on a later day — the weaker branch). |
| **3.3.2** Labels or Instructions | `rem-renewal-label-6d81ecf3` | **Stale version pin**: `attested_against.version: 5.3.0`, an interim build, while this report names **5.3.1**. Both dates (2026-08-21) also fall outside the retest evaluation window (2026-08-25 → 2026-08-28). Two named non-agent people and a complete method — but confirmed on a product that is not the one this ACR claims for. | Tomas Reyes and Grace Okonjo (or any two named people) re-confirm the bulk-renewal date-override label **on 5.3.1**, inside the window. There is no grandfathering: attestation is about the product now. |

Two closures each block a criterion for a *different* reason; do not treat these as one ticket.

**These are human gaps, not testing gaps.** None of the four is closed by more automated testing, more samples, or another scanner run. Each needs a named person to operate the fixed control on 5.3.1 and record what they saw, plus a second named person to confirm.

## Criteria deliberately kept in the tables

- **1.4.11 Non-text Contrast → `partially-supports`, entry retained.** This criterion is *still failing* (S02, S03), so the unattested-closure gate does not touch it — dropping a disclosed failure from a conformance document would be worse than disclosing it. Its note discloses the unattested resolved defect in the required form: `rem-status-icon-99a6dd2f resolved but not attested`. The improvement (S04 status icons fixed, narrowing the failure from three samples to two) is **not** claimed as a narrowing anywhere in the term.
- **4.1.2 Name, Role, Value → `supports`, remediated form.** The only fully attested closure: Marisol Fenn (named, `self_attested: false`, pinned to 5.3.1, four-part method whose `observed` decided the operation), second-confirmed by Owen Bratcher, a different person, both dates inside the window and not after `report_date`. `interaction_evidence` is a screen-reader announcement trace — class-matched to a name/role/value defect. Refusing this one would be over-refusal.
- **4.1.1 Parsing → `not-applicable`.** The criterion was removed in WCAG 2.2; the VPAT 2.5 catalog retains the row. Recorded per the report's own instruction, with the removal note.

## Attestation roster — for the signing author's countersignature

The signing author countersigns this block before publication. It is the step that binds the names on the closure records to a person accountable for the ACR; the records themselves cannot do that.

**Admitted — backs a published improved term (1 item):**

| Criterion | `item_id` | `attested_by` | `second_confirmation.by` | `attested_against` |
|---|---|---|---|---|
| 4.1.2 Name, Role, Value | `rem-holds-btn-name-7f3c88d1` | Marisol Fenn (accessibility QA lead, Fernbank Access Partners), 2026-08-27T14:20Z, `self_attested: false` | Owen Bratcher, 2026-08-27T19:05Z, VoiceOver + Safari 18 | 5.3.1 |

**Not admitted — named here so the roster is complete, backing nothing (4 items):**

| Criterion | `item_id` | Attester of record | Confirmer of record | Pin | Ruling |
|---|---|---|---|---|---|
| 2.4.7 | `rem-focus-ring-a17c4e2b` | — | — | — | draft_not_attested |
| 2.4.11 | `rem-header-offset-2b6f9ac4` | `a11y-fix-executor` (agent) | `a11y-fix-executor` (agent), same day | 5.3.1 | agent in both name fields; self-attested without a disclosed independent confirmer |
| 3.3.1 | `rem-hold-error-announce-5c9f14e0` | Grace Okonjo | *none* | 5.3.1 | single confirmation |
| 3.3.2 | `rem-renewal-label-6d81ecf3` | Tomas Reyes | Grace Okonjo | **5.3.0** | stale pin; dates outside the evaluation window |

A fifth record, `rem-icon-contrast-88be5f13` (1.4.11), is not on the roster and needs none: it did not close, its own `residual` says so, and no improved term rests on it. A sixth, `rem-status-icon-99a6dd2f`, is draft and backs nothing — it is disclosed inside the still-failing 1.4.11 note.

## Decisions the engagement owner still owes

1. **License — unset, and that is not neutral.** The engagement record says the County has not decided one, so no `license` field was written. The schema states verbatim that "If none is provided 'CC-BY-4.0' is assumed default in any output," and the rendered HTML **does assert Creative Commons Attribution 4.0** (verified in `draft.html`). If CC-BY-4.0 is not the intent, set `license` before anything circulates.
2. **`last_modified_date` — omitted.** No value exists in the engagement record. Not invented; the owner supplies it or it stays out.
3. **`repository` — omitted.** No publication location supplied.
4. **`related_openacrs` — omitted.** Document version 1 (2026-06-12) is superseded and is named in `notes`, but no URL for it exists in the engagement record, and the schema's link field would have to be fabricated to include it. Add the link if version 1 is published anywhere.
5. **`vendor.name` — omitted.** The record supplies the responsible organization and its email, not a named contact person.

## Refusals recorded on this draft

- **The commissioner's request is refused.** The 2026-08-27 correspondence from County Commissioner Elena Marsh asks to "mark them supports so we can publish before the bond vote," citing a green automated retest. A green automated retest is not an attestation. Four of the five improved criteria carry no term in this draft, and a publication deadline is not an input to the outcome→term mapping. The bond-vote timeline is a reason to staff the four confirmations this week, not a reason to publish the terms without them.
- **Severity never moved a term.** `a11y_catalog_holds_button_unlabeled` is CRITICAL and its criterion publishes `supports`; `a11y_catalog_format_icon_contrast` is MAJOR and its criterion publishes `partially-supports`. Both come from the outcome map alone. Impact language stays in notes.
- **No `[Demo Purposes Only]` labels.** That discipline applies to declared Section 508 multi-deliverable engagements. This engagement declares WCAG 2.2 Level AA (no Revised-508 conformance floor) and produces one report artifact. The catalog carries 508 chapters as a *format* property, which is not a declared-508 engagement. Applying demo labels here would deface the real names of real people who did the work.
- **Non-web components omitted entirely.** Only `web` is populated. The four 508 chapters are `disabled: true` with coverage-boundary notes; their conclusions stay human-owned. The untagged quarterly PDF program guide (`a11y_program_guide_pdf_untagged`) is electronic-document evidence and is disclosed as a boundary in the document notes — it is **not** serialized as a criterion outcome and did not touch 1.3.1's web term.
- **No untested marker line.** Every A/AA criterion in the report's outcome map carries `passed`, `failed`, or `inapplicable`; none is `untested` or `cantTell`, and no tool-lane skip was reported. Emitting a spurious untested marker would be as wrong as omitting a real one. No SC appears on both marker lines — only one marker line exists.

## Review checklist for the signing author

1. Read the four INCOMPLETE gaps above and decide who performs each confirmation, on 5.3.1.
2. Countersign the attestation roster, or strike 4.1.2's `supports` back to INCOMPLETE if you do not accept Fenn/Bratcher.
3. Decide the license (see above) before any copy leaves the building.
4. Confirm the vendor block and the supersession statement with Millbrook County Library System, Digital Services.
5. Add non-web component conclusions only where you hold evidence for them; this draft asserts none.
6. Remove the draft disclaimer only at issuance, and re-validate the exact file being issued with `-c` on both commands.

**This skill never signs, never publishes, and never emits a final ACR.** Sign-off, publication, removal of the draft disclaimer, the license decision, and every conformance statement made to a third party are the human's.

---

## Provenance

Files read: the skill protocol `/Users/AlexUA_1/claude/accessibility-skills/.claude/skills/acr-reporting/SKILL.md`; the linked contracts `docs/a11y-fix-closure-contract.md` and `docs/openacr-reference.md` under the same root; the engagement package `/private/tmp/claude-501/.../scratchpad/retest57/stage/county-library-retest.md`; and, from the pinned `@openacr/openacr@0.3.8` install at `/tmp/acr-check`, the JSON schema `schema/openacr-0.1.0.json`, the catalog `catalog/2.5-edition-wcag-2.2-508-en.yaml` (every A/AA/AAA criterion ID, chapter ID, component ID, and adherence term was extracted from that file rather than recalled), and `openacr/drupal-10-16.yaml` as a document-shape precedent. Scratch artifacts were written only under `/private/tmp/claude-501/acr-mcl/` (`gen.py`, `draft.yaml`, `draft.html`, `draft.md`). No `evals/` path, no `*.metadata.yaml` or `*.rubric.yaml`, no `docs/plans/` file, and no results receipt was read; the repository was not written to and was not searched for this fixture's name or for prior drafts. No subagents were spawned.
