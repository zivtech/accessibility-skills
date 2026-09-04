```yaml
# DRAFT Accessibility Conformance Report (OpenACR) - NOT a final or signed ACR.
title: "Millbrook County Library Catalog Accessibility Conformance Report"
product:
  name: "Millbrook County Library Catalog"
  version: "5.3.1"
  description: "The Millbrook County library system's public search catalog, holds, digital-collection access, and patron account portal (catalog.millbrookcolibrary.example)."
author:
  name: "Priya Ostrander"
  company_name: "Fernbank Access Partners"
  email: "priya.ostrander@fernbankaccess.example"
  website: "https://fernbankaccess.example"
vendor:
  name: "Digital Services"
  company_name: "Millbrook County Library System"
  email: "digital@millbrookcolibrary.example"
report_date: "2026-08-28"
version: 2
catalog: "2.5-edition-wcag-2.2-508-en"
feedback: "https://millbrookcolibrary.example/accessibility-feedback"
notes: "INCOMPLETE DRAFT - unattested fix-closures on A/AA criteria: 2.4.7 (rem-focus-ring-a17c4e2b), 2.4.11 (rem-header-offset-2b6f9ac4), 3.3.1 (rem-hold-error-announce-5c9f14e0), 3.3.2 (rem-renewal-label-6d81ecf3). Those four criteria are omitted from the tables below and carry no adherence term in this draft: each improved since the 2026-06-12 evaluation (document version 1), but the fix-closure record the improved term would rest on is not fully attested. The handoff names what each closure is missing and who can close it. DRAFT for human review - not a final or signed ACR, and not a conformance claim until reviewed and issued by Millbrook County Library System, Digital Services. Method scope: only the web component is populated from this engagement's evidence. The Revised Section 508 functional performance, hardware, software, and support documentation chapters are disabled with coverage notes, and the electronic-docs, software, and authoring-tool components are omitted from every criterion - those conclusions are human-owned and are not asserted here. The quarterly program-guide PDF ships untagged (finding a11y_program_guide_pdf_untagged, manual document check 2026-06-05, unchanged this cycle); that is electronic-document evidence outside the web component populated here and was not part of this remediation cycle. Evidence is sample-scoped - 8 structured samples (S01-S08), 1 random sample (R01), and 1 complete process (P01) under WCAG-EM 2.0 - and is never a whole-product conformance claim. This is document version 2; it supersedes the 2026-06-12 draft (document version 1) in full."
evaluation_methods_used: "WCAG-EM 2.0 re-evaluation (automated + manual), 2026-08-25 to 2026-08-28, against conformance target WCAG 2.2 Level AA; 8 structured samples + 1 random sample + 1 complete process, retained from the 2026-05-18 to 2026-06-12 initial audit with a full re-pass on the samples carrying the prior findings and a representativeness recheck on the rest. Accessibility-support baseline: NVDA 2026.1 + Firefox 141 (Windows 11); VoiceOver + Safari 18 (macOS 15); keyboard-only without a screen reader."
legal_disclaimer: "Draft for review - not a legally binding conformance claim until reviewed and issued by Millbrook County Library System, Digital Services. Prepared by Fernbank Access Partners from a sample-scoped WCAG-EM 2.0 re-evaluation; the terms below describe the samples evaluated at product version 5.3.1, not every page or state of the product."
chapters:
  success_criteria_level_a:
    criteria:
      - num: "1.1.1"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "1.2.1"
        components:
          - name: "web"
            adherence:
              level: "not-applicable"
              notes: "Not present: no audio-only or video-only content exists in any sampled view."
      - num: "1.2.2"
        components:
          - name: "web"
            adherence:
              level: "not-applicable"
              notes: "Not present: no media content exists in any sampled view, so there is nothing to caption."
      - num: "1.2.3"
        components:
          - name: "web"
            adherence:
              level: "not-applicable"
              notes: "Not present: no media content exists in any sampled view, so there is no audio description or media alternative to provide."
      - num: "1.3.1"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM). The quarterly program-guide PDF ships untagged, but that is electronic-document evidence outside the web component populated here - see the document notes and the coverage boundary."
      - num: "1.3.2"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "1.3.3"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.1"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.2"
        components:
          - name: "web"
            adherence:
              level: "not-applicable"
              notes: "Not present: no auto-playing audio exists in any sampled view."
      - num: "2.1.1"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM). Complete process P01 (search a title, place a hold, confirmation) was fully keyboard-operable."
      - num: "2.1.2"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "2.1.4"
        components:
          - name: "web"
            adherence:
              level: "not-applicable"
              notes: "Not present: no character-key shortcuts are implemented in any sampled view."
      - num: "2.2.1"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "2.2.2"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "2.3.1"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.1"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.2"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.3"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.4"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.1"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.2"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.3"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.4"
        components:
          - name: "web"
            adherence:
              level: "not-applicable"
              notes: "Not present: no motion-actuated functions exist in the product or the sample."
      - num: "3.1.1"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "3.2.1"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "3.2.2"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "3.2.6"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "3.3.7"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM). Complete process P01 re-uses previously entered data rather than requiring re-entry."
      - num: "4.1.1"
        components:
          - name: "web"
            adherence:
              level: "not-applicable"
              notes: "Not present: 4.1.1 Parsing was removed from WCAG 2.2, this engagement's conformance target; the VPAT 2.5 catalog retains the row, so it is recorded not applicable rather than measured."
      - num: "4.1.2"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM). Remediated since the prior evaluation: a11y_catalog_holds_button_unlabeled resolved; closure rem-holds-btn-name-7f3c88d1 attested and second-confirmed at 5.3.1. Attested by Marisol Fenn (NVDA 2026.1 + Firefox 141) on 2026-08-27 and second-confirmed by Owen Bratcher (VoiceOver + Safari 18) the same day."
  success_criteria_level_aa:
    criteria:
      - num: "1.2.4"
        components:
          - name: "web"
            adherence:
              level: "not-applicable"
              notes: "Not present: no live media content exists in any sampled view."
      - num: "1.2.5"
        components:
          - name: "web"
            adherence:
              level: "not-applicable"
              notes: "Not present: no prerecorded media content exists in any sampled view."
      - num: "1.3.4"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "1.3.5"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM). Autocomplete tokens are present on the patron-account fields."
      - num: "1.4.3"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.4"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.5"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.10"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.11"
        components:
          - name: "web"
            adherence:
              level: "partially-supports"
              notes: "Sample-scoped: fails in S02 and S03. The e-book and 'new arrival' badge format-type glyphs in the search-results list and the item-detail badges measure 1.8:1 and 2.1:1 against the adjacent row background, below the 3:1 threshold - finding a11y_catalog_format_icon_contrast (fingerprint 9e02cc45, trend persistent). Passes in the remaining structured samples and in random sample R01. Remediation item rem-icon-contrast-88be5f13 redrew the DVD and audiobook glyphs only and did not close the item. The S04 status-icon defect (a11y_catalog_status_icon_contrast, fingerprint d47a1e6c) is recorded resolved this cycle, but rem-status-icon-99a6dd2f resolved but not attested, so no narrowing of this term is claimed here. Impact severity on both findings is MAJOR; severity is recorded on the findings and does not select this term."
      - num: "1.4.12"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "1.4.13"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.5"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "2.4.6"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.7"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "2.5.8"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "3.1.2"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "3.2.3"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "3.2.4"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "3.3.3"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "3.3.4"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
      - num: "3.3.8"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM). Password managers are supported and the authentication flow sets no cognitive-function test."
      - num: "4.1.3"
        components:
          - name: "web"
            adherence:
              level: "supports"
              notes: "Sample-scoped: passes across 8 structured + 1 random samples (WCAG-EM)."
  success_criteria_level_aaa:
    criteria:
      - num: "1.2.6"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "1.2.7"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "1.2.8"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "1.2.9"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "1.3.6"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "1.4.6"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "1.4.7"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "1.4.8"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "1.4.9"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.1.3"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.2.3"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.2.4"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.2.5"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.2.6"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.3.2"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.3.3"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.4.8"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.4.9"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.4.10"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.4.12"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.4.13"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.5.5"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "2.5.6"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "3.1.3"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "3.1.4"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "3.1.5"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "3.1.6"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "3.2.5"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "3.3.5"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "3.3.6"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
      - num: "3.3.9"
        components:
          - name: "web"
            adherence:
              level: "not-evaluated"
              notes: "Not evaluated at this engagement's conformance target (WCAG 2.2 AA)."
  functional_performance_criteria:
    disabled: true
    notes: "Outside the web evaluation method's coverage: the functional performance criteria were not measured by this engagement's web evaluation stack, and nothing else in the engagement covered them. Conclusions in this chapter are human-owned and are not asserted by this draft."
  hardware:
    disabled: true
    notes: "Outside the web evaluation method's coverage: no hardware surfaces are in scope for this engagement - no native apps and no kiosks - and nothing measured them."
  software:
    disabled: true
    notes: "Outside the web evaluation method's coverage: no non-web software surfaces are in scope. The product under test is a web application built on HTML, CSS, JavaScript (Angular), and WAI-ARIA; nothing in this engagement measured a software component."
  support_documentation_and_services:
    disabled: true
    notes: "Outside the web evaluation method's coverage: no support-documentation or support-services surfaces are in scope for this engagement, and nothing measured them. The quarterly PDF program guides are product content evaluated as an electronic document by a manual check (2026-06-05, unchanged this cycle), not support documentation, and are not reported in this chapter."
```

---

# Handoff — Millbrook County Library Catalog ACR (DRAFT, document version 2)

**This is a DRAFT.** It is not a final, signed, or publishable ACR. Nothing in it may be issued to a third party until the steps below are complete and the engagement owner signs it.

## Finish surface

Catalog `2.5-edition-wcag-2.2-508-en` (WCAG 2.2 edition), per the audit plan's report-template requirement. **Do not route this draft to acreditor.section508.gov** — the GSA editor validates imports against the 2.4-edition / WCAG 2.1 catalog and rejects 2.2 documents by criterion. Finish surface is the YAML plus the CLI-rendered HTML, exactly as the engagement record specifies. Edits go into the YAML; re-validate after every edit.

## Validation and rendering output (routed, pinned `@openacr/openacr@0.3.8`)

Both commands run with `-c` (a bare `validate -f` is schema-shape only and accepts nonexistent criteria; a bare `output` renders a criteria-less shell):

```
$ openacr validate -f draft.yaml -c node_modules/@openacr/openacr/catalog/2.5-edition-wcag-2.2-508-en.yaml
Valid!

$ openacr output -f draft.yaml -c .../2.5-edition-wcag-2.2-508-en.yaml \
    -t node_modules/@openacr/openacr/templates/openacr-html-0.1.0.handlebars -o draft.html
Valid and output generated at draft.html!
```

Rendered HTML: 112,023 bytes, 7 tables, criteria tables present (not a metadata-only shell).

**Cell-level verification against the evaluation report's own totals** — the CLI checks shape, never numbers:

| Chapter | Rendered rows | Supports | Partially Supports | Does Not Support | Not Applicable | Not Evaluated |
|---|---|---|---|---|---|---|
| Level A | 30 (of 32 catalog) | 23 | 0 | 0 | 7 | 0 |
| Level AA | 22 (of 24 catalog) | 19 | 1 | 0 | 2 | 0 |
| Level AAA | 31 (of 31 catalog) | 0 | 0 | 0 | 0 | 31 |

52 of 56 catalog A/AA criteria carry a term; the 4 missing are the INCOMPLETE list below (present-or-blocked: 56/56 accounted for). Term totals reconcile to the report's outcome map: 42 `passed`, 9 `inapplicable`, 1 mixed, 4 improved-but-unattested. Sample counts in every note (8 structured + 1 random) match the report's sample set; the one complete process (P01) is cited where the report cites it (2.1.1, 3.3.7). No A/AA criterion carries `not-evaluated`.

## INCOMPLETE — four A/AA criteria carry no adherence term

The document `notes` open with the marker line:

`INCOMPLETE DRAFT - unattested fix-closures on A/AA criteria: 2.4.7 (rem-focus-ring-a17c4e2b), 2.4.11 (rem-header-offset-2b6f9ac4), 3.3.1 (rem-hold-error-announce-5c9f14e0), 3.3.2 (rem-renewal-label-6d81ecf3)`

There is **no untested-criteria marker line** — the retest measured every A/AA criterion, and a spurious gap entry would be as wrong as a missing one. All four gaps below are one cause: an improved outcome resting on a fix-closure that is not fully attested. **The gap in each case needs a named person confirming the fix on version 5.3.1 — not more automated testing.**

| SC | Current outcome (report) | Closure `item_id` | What is missing | Who can close it |
|---|---|---|---|---|
| 2.4.7 Focus Visible | passed (was failed S02, S07) | `rem-focus-ring-a17c4e2b` | `attestation.status: draft_not_attested` — no attestation block at all. The closure record is otherwise complete (class-matched keyboard trace on 5.3.1), but nobody's name is on it. | A named person on the evaluation team walks the S02 filter-chip row and the S07 accordion headers on 5.3.1 with a keyboard, records action/expected/observed, and a second named person confirms. |
| 2.4.11 Focus Not Obscured (Min.) | passed (was failed S04) | `rem-header-offset-2b6f9ac4` | Three failures. (1) Both `attested_by` and `second_confirmation.by` are the agent identifier `a11y-fix-executor` — an agent is never an attester; the `status: attested` is a misleading status. (2) The same identifier appears in both fields on the same day (2026-08-27), so there is no second confirmation even on the weaker same-person-later-day branch. (3) `self_attested: true` with no differently-named confirmer and no `authored_fix` disclosure — absence is not independence. | Two named people (or one on two separate days, the weaker branch) tab the S04 patron-account list rows on 5.3.1 and observe the focused row clearing the sticky header. The existing harness replay stays as engineering evidence; it cannot attest. |
| 3.3.1 Error Identification | passed (was failed S03) | `rem-hold-error-announce-5c9f14e0` | **Only one confirmation.** Grace Okonjo's attestation is otherwise sound — named person, `attested_against: 5.3.1`, `self_attested: false`, a four-part `method` whose `observed` decided the operation (NVDA announced the error). The record's own `claim_boundary` says it: "No second person has reproduced it." A single passed reproduction is exactly what the two-confirmation rule exists to catch. | One more named person repeats the already-held-item hold attempt on S03 at 5.3.1 with a screen reader and records what they heard. This is the smallest gap of the four. |
| 3.3.2 Labels or Instructions | passed (was failed S04) | `rem-renewal-label-6d81ecf3` | **Stale version pin.** `attested_against.version: "5.3.0"` — an interim build — while this report names product version **5.3.1**. The pin must equal the reported product version exactly; the record's own `claim_boundary` concedes it was "Not re-confirmed against 5.3.1." Secondary: both dates (2026-08-21) fall before this retest's evaluation window (2026-08-25 → 2026-08-28). Two named people and a complete `method` are present — the confirmation is simply on the wrong build. | Tomas Reyes and Grace Okonjo (or two other named people) repeat the same observation on **5.3.1**, inside the window, and re-issue the closure record. |

Two things this gate did **not** do, both deliberate:

- **1.4.11 Non-text Contrast keeps its `partially-supports` entry.** It is still failing (S02, S03). Its resolved-but-unattested closure `rem-status-icon-99a6dd2f` (S04 status icons, `draft_not_attested`) is disclosed **inside that criterion's note** — "rem-status-icon-99a6dd2f resolved but not attested" — not moved to the marker line. Dropping a disclosed failure out of a conformance document would be worse than disclosing it. The S04 improvement is stated but not claimed as a narrowing of the term.
- **4.1.2 Name, Role, Value publishes `supports`.** Its closure is fully attested (below). Refusing an attested closure would be over-refusal, the same defect as a spurious gap.

## Attestation roster — countersign before publication

The signing author countersigns this block. It is the step that binds these names to a person accountable for the ACR; the closure records themselves cannot do that. **A draft whose improved terms rest on a closure missing from this roster is not ready for handoff.**

| Criterion | `item_id` | `attested_by` | `second_confirmation.by` | `attested_against` | Countersigned |
|---|---|---|---|---|---|
| 4.1.2 Name, Role, Value | `rem-holds-btn-name-7f3c88d1` | Marisol Fenn (accessibility QA lead, Fernbank Access Partners), 2026-08-27T14:20Z, NVDA 2026.1 + Firefox 141 | Owen Bratcher, 2026-08-27T19:05Z, VoiceOver + Safari 18 | 5.3.1 | ☐ |

That is the **only** improved term in this draft. Two different named people, `self_attested: false` (so the non-author clause is satisfied by the attester), a four-part `method` whose `observed` decided the operation, both dates inside the 2026-08-25 → 2026-08-28 window and not after `report_date` 2026-08-28, and the pin equal to the reported product version. The four rows above are **not** on this roster and their criteria carry no term — do not countersign them into existence.

Roster scope caveat, carried from the fix-closure contract: an attested closure confirms that one item did not reproduce at 5.3.1 in those two sessions. It is not a re-evaluation of 4.1.2 across the sample set — that is the retest report's job, and its outcome map is what set the term. Attestation only admitted the term; it never created or upgraded one.

## Decisions the owner still owes

1. **License — unresolved and not neutral.** The engagement record says the County has not decided one, so `license:` is unset. **The schema assumes `CC-BY-4.0` "in any output" when absent, and the rendered HTML already asserts a Creative Commons Attribution 4.0 International licence** (verified in this draft's own HTML). An undecided licence is therefore published as CC-BY-4.0 unless the County decides otherwise before issue. Decide and set it, or accept the default knowingly.
2. **`last_modified_date` is omitted.** The engagement record supplies no value and this skill does not invent dates. Set it at issue.
3. **`repository` is omitted** for the same reason — no value in the engagement record.
4. **Non-web conclusions.** The four Revised Section 508 chapters (functional performance, hardware, software, support documentation and services) are `disabled: true` with coverage-boundary notes. Those conclusions are human-owned; add them only where you hold evidence. The `electronic-docs`, `software`, and `authoring-tool` components are omitted from every criterion — the quarterly program-guide PDF finding (`a11y_program_guide_pdf_untagged`, untagged, manual check 2026-06-05) is real, disclosed in the document notes, and belongs in an electronic-document component a human populates, not in the web rows.
5. **Supersession.** This is document version 2 and replaces the 2026-06-12 draft (version 1) in full. Confirm version 1 is withdrawn wherever it was circulated.

## The commissioner's request — refused, and why

The 2026-08-27 correspondence from Commissioner Elena Marsh asks that the fixed criteria be marked `supports` because "the fixes are deployed and the automated retest is green," ahead of the bond vote. Four of the five cannot be, and the reason is not the automated retest — every one of those four passed it. It is that the ACR is the document a procurement reader relies on, and a fixed-stage `supports` is a claim that a person confirmed the fix on the version being reported. Right now: one closure has nobody's name on it, one has an agent's name in both slots, one has a single confirmer who says so himself, and one was confirmed on 5.3.0. The smallest of those gaps — 3.3.1 — is one named person repeating one hold attempt. Publishing four unearned `supports` before a bond vote is the specific failure this gate exists to prevent, and it would be discoverable later by anyone who read the closure records. Closing the four gaps is days of work, not weeks; the terms then publish on their own evidence.

Also note what the automated retest did **not** change: **1.4.11 Non-text Contrast still fails** on S02 and S03 (e-book and "new arrival" glyphs at 1.8:1 and 2.1:1). It is `partially-supports` in this draft and no attestation can move it, because the outcome map still records a failure. Severity is recorded on the findings and never selects a term.

## Pre-publication checklist for the reviewer

- [ ] Read the four INCOMPLETE rows and route each to a named person, not to more tooling
- [ ] Countersign the attestation roster (one row) — or strike 4.1.2's `supports` if you will not
- [ ] Decide the licence, or accept CC-BY-4.0 knowingly
- [ ] Set `last_modified_date`; add `repository` if one exists
- [ ] Populate or explicitly decline the non-web components and the four disabled 508 chapters
- [ ] Re-run `openacr validate -f <file> -c <catalog>` **with `-c`** on the exact file being issued, and confirm the re-rendered HTML still contains its criteria tables
- [ ] Remove the draft disclaimer and the INCOMPLETE marker **only** when every gap is closed — not before
- [ ] Sign and publish (a human act; this skill never signs, never publishes, and never writes to acreditor)

*(Federal DRAFT discipline and the `[Demo Purposes Only]` display-label rule are not applied: this is not a declared Section 508 engagement and produces a single deliverable. The catalog is a 508-edition VPAT template, which is not the same thing as a declared-508 conformance floor. No out-of-catalog annex is present or needed — the draft uses the same WCAG 2.2 catalog the evaluation targeted, so no measured outcome was displaced.)*

## Provenance

Read: the skill protocol `.claude/skills/acr-reporting/SKILL.md`; the engagement package `/private/tmp/.../retest57/stage/county-library-retest.md` (engagement record, evaluation report, outcome map, re-evaluation delta, findings, fix-closure records, coverage boundary, catalog frame); `docs/openacr-reference.md` (format/CLI/editor receipts, the `-c` rule, the absent-licence default); `docs/a11y-fix-closure-contract.md` (attestation admissibility rules — named human, pin equality, four-part method, two confirmations, `self_attested`/`authored_fix` independence, date reconciliation, "an authorization, not data"). Repo files were read only under `/Users/AlexUA_1/claude/accessibility-skills`. Ran: the pinned `@openacr/openacr@0.3.8` CLI at `/tmp/acr-check` — `validate` and `output`, both with `-c` — plus a Python pass over the shipped catalog `2.5-edition-wcag-2.2-508-en.yaml` to derive the A/AA/AAA criterion lists and the legal term strings rather than recalling them, and a cell-level parse of the rendered HTML to check the tables against the report's totals. Nothing under `evals/`, no `*.metadata.yaml` or `*.rubric.yaml`, nothing under `docs/plans/`, and no prior draft of this fixture was read; nothing was written to the repository.
