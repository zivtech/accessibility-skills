# ICT Testing Baseline — Verified Reference

Phase 0 deliverable of [the adoption assessment](ict-testing-baseline-adoption-assessment.md). Facts below were read directly from the published pages and the pinned source tree on 2026-08-12, not from secondary sources. Machine-readable companion: [ict-baseline-test-id-manifest.yaml](ict-baseline-test-id-manifest.yaml) — the ground truth for baseline-test-ID validity checks.

**Originating source (license-required citation):** the ICT Testing Baseline Portfolio is authored under the Federal CIO Council's Accessibility Community of Practice (ACOP, <https://www.cio.gov/about/accessibility-cop/>) and distributed at <https://ictbaseline.access-board.gov/> and <https://github.com/atbcb/ICTTestingBaseline>. Its 2018 `LICENSE` (SPDX: none asserted; MIT-style) grants use/copy/modify/publish rights on two conditions verified in the license text: the ACOP must be cited as originating source **including the URL of the distribution**, and modifications **must not be attributed to ACOP**. Accordingly: baseline content below restates the published source; the manifest's `classification` fields and this document's stack commentary are this repository's additions, not ACOP content. Section 508 rule text quoted below is U.S. federal work, read from the [Access Board's published Revised 508 standards](https://www.access-board.gov/ict/).

## Provenance and pin

- **Published pages, fetched raw** (plain `curl`, no summarizer — the drafting session's truncation trap): `/allwebbaselines.html` (214,526 bytes; size-consistent with the critic pass's ~214KB) and `/alldocsbaselines.html` (183,606 bytes), 2026-08-12. Enumeration extracted by parser with hand verification of every anomaly; per-test data cross-checked against `_baselines/` sources at the pinned SHA (spot-checks matched byte-for-substance, including upstream typos — the all-tests pages are Jekyll-assembled from the same `.md` files, so source and rendered page share one origin).
- **The pin (the identity of "what we verified"):** `atbcb/ICTTestingBaseline` `main` @ **`6c537a3b79992237b6edb9b0b608730d8da8cdef`** (committed 2026-07-24, a dependency bump). The repo-level push timestamp 2026-08-09 is a working-branch push, not `main`. Last `main` commit touching `_baselines/` content: `fc8fb9b1b`, 2026-02-05 (#570, documents-baseline Appendix A 18.A addition); before that #561 (2025-08-27, heading/typo fixes) and #534 (2025-02-18, H44 link fix).
- **Site self-labels vs tags:** the landing page says Web "version 3.1 (published April 1, 2024)" and Documents "Version 1.0 (published September 30, 2024)". Nearest release tag: `v3.1` = `b0e0fe2e2ba728cd87380e1181ece450297f1938` (2024-04-01). **No tag or release exists for the Documents baseline** — document versions are cut on `main`. Tag→SHA delta: repository restructure (flat `_baselines/` → `web-baselines/` + `document-baselines/`, the latter being the Documents v1.0 addition) plus the three content-fix commits above; 18 commits touched `_baselines/` since the tag date. The rendered site is not the tag; the SHA is the identity.
- **Archive anchors (confirmed):** Wayback snapshots of both all-tests pages exist — the SPN saves requested 2026-08-12 were confirmed the same day via the CDX API (the availability API was rate-limiting): [allwebbaselines @ 20260812143029](https://web.archive.org/web/20260812143029/https://ictbaseline.access-board.gov/allwebbaselines.html) and [alldocsbaselines @ 20260812143044](https://web.archive.org/web/20260812143044/https://ictbaseline.access-board.gov/alldocsbaselines.html), both HTTP 200.

## Identity

- **What it is:** "the minimum requirements for evaluating the conformance of ICT with the Revised Section 508" — a benchmark of test components that Section 508 conformance test processes must include. Its own Is/Is-NOT framing: it **is** "a comprehensive set of test components … independent of any testing tools"; it **is not** "a step-by-step testing procedure or methodology" nor a testing tool. The web introduction is explicit: "The ICT Testing Baseline is not intended to be a test process itself."
- **Who:** authored under ACOP; maintained by the ICT Testing Baseline Working Group (ITBWG); led by U.S. Access Board and GSA Government-wide IT Accessibility Program with DHS contributions; site hosted by the Access Board. Contacts: `ictbaseline@gsa.gov` (landing page), `itbwg@gsa.gov` (site config). The Web baseline is recognized as a Best Practice by the Federal CIO Council's ACOP. (Source-quality note: the introduction's ITBWG sentence has blank organization names on the live page — "led by US federal government representatives from  and the ." — `main` is live and imperfect.)
- **Two published baselines:** Web (v3.1-as-served) and Electronic Documents (v1.0). Software and hardware baselines are planned, not published.
- **Lineage:** 2009 DHS/SSA harmonized baseline → DHS Trusted Tester process (v3) built on it → 2017 Revised 508 rule → baseline updated for WCAG 2.0 A/AA incorporation. DHS **Trusted Tester v5** is the dominant baseline-aligned test process (secondary sources; TT course v5.1.3, April 2024).

## Structure and ID grammar

- Numbered **test families** (h2), each with: Accessibility Requirements → Test Method Rationale → Limitations/Assumptions/Exceptions → lettered **test procedures** (h3) → Advisory tips → WCAG 2.2 Techniques.
- Each test procedure: **Identify Content → Test Instructions → Test Results**, declaring `Baseline Test ID: <family>.<letter>-<CamelCaseName>` (e.g. `5.C-ControlState`). The identify-content step is a gate: per the v3.0 changelog, "If those conditions are not met, the test does not apply." Instructions cite their basis inline (`[SC 3.3.1]`, `[508 503.4.1]`).
- **Assembly mechanism (settles "published list vs file list"):** the all-tests pages are ~4.8KB Jekyll wrappers including each family **by front-matter title**. Source files without matching titles never render: `03FocusOrder.md` and `25Noninterference.md` (tombstones for pre-3.x renumbering), `00WCAG-Applicability.md`, `DevelopTestProcess.md`, and `AppendixB.md` all 404 on the live site. The published page is the citable enumeration; the file list is not.
- Published per-baseline appendices: **Appendix A – Cross Reference Tables** (live at `/web-baselines/AppendixA1/` and the documents equivalent) maps at **test-instruction granularity** (`1.A-1`, `1.A-2` → SC/508 requirement) with sortable tables — the upstream seed for any coverage crosswalk, finer-grained than this repo's test-level manifest. Appendix B (change log) and a glossary render per baseline.

## Published enumeration — Web: 24 families, 62 active tests

Verified from the complete raw fetch; no family 25 exists. Basis column = citations inside the test instructions themselves (family-level Accessibility Requirements sections carry the full SC quotations).

| # | Family | 508 / WCAG 2.0 basis (as cited in test instructions) | Active tests |
|---|---|---|---|
| 1 | Keyboard Accessible | 2.1.1, 2.1.2 | `1.A-KeyboardAccess` · `1.B-NoKeyboardTrap` |
| 2 | Focus | 2.4.7, 2.4.3, 3.2.1 | `2.A-FocusVisible` · `2.B-FocusOrder` · `2.C-OnFocus` |
| 3 | Non-Interference | Conformance Requirement 5 (non-interference: SC 1.4.2, 2.1.2, 2.3.1, 2.2.2) | `3.A-NonInterference` |
| 4 | Repetitive Content | 2.4.1, 3.2.3, 3.2.4 | `4.A-BypassBlocks` · `4.B-ConsistentNavigation` · `4.C-ConsistentIdentification` |
| 5 | User Controls | 4.1.2 | `5.A-ControlName` · `5.B-ControlRole` · `5.C-ControlState` · `5.D-ControlValue` |
| 6 | Images | 1.1.1, 4.1.2, 1.4.5 | `6.A-MeaningfulImage` · `6.B-DecorativeImage` · `6.C-Captcha` · `6.D-ImageText` |
| 7 | Sensory Characteristics | 1.4.1, 1.3.3, 1.1.1 | `7.A-Color` · `7.B-SensoryCharacteristics` · `7.C-AudibleCues` |
| 8 | Contrast | 1.4.3 | `8.A-ContrastMinimum` |
| 9 | Flashing | 2.3.1 | `9.A-Flashes` |
| 10 | Forms | 1.3.1, 4.1.2, 2.4.6, 3.2.2, 3.3.1, 3.3.2, 3.3.3, 3.3.4 | `10.A-FormName` · `10.B-FormDescriptiveLabel` · `10.C-OnInput` · `10.D-ErrorIdentification` · `10.E-FormHasLabel` · `10.F-ErrorSuggestion` · `10.G-ErrorPrevention` |
| 11 | Page Titles | 2.4.2 | `11.A-PageTitled` |
| 12 | Tables | 4.1.2, 1.3.1 | `12.A-DataTableRole` · `12.B-DataTableHeaderAssociation` · `12.C-LayoutTable` |
| 13 | Content Structure | 2.4.6, 1.3.1 | `13.A-HeadingDescriptive` · `13.B-VisHeadingProg` · `13.C-ProgHeadingVisual` · `13.D-List` |
| 14 | Links | 2.4.4, 4.1.2 | `14.A-LinkPurpose` |
| 15 | Language | 3.1.1, 3.1.2 | `15.A-LanguagePage` · `15.B-LanguagePart` |
| 16 | Audio-Only and Video-Only | 1.2.1 | `16.A-AudioOnlyTranscript` · `16.B-VideoOnlyAlt` · `16.C-AudioMediaAlternative` · `16.D-VideoMediaAlternative` |
| 17 | Synchronized Media | 1.2.2, 1.2.3, 1.2.4, 1.2.5, 508 503.4, 508 503.4.1, 508 503.4.2 | `17.A-MediaPlayerCCADControls` · `17.B-MediaPlayerCCLevel` · `17.C-MediaPlayerADLevel` · `17.D-CaptionsPrerecorded` · `17.E-ADPrerecorded` · `17.F-CaptionsLive` · `17.G-SyncMediaAlternative` |
| 18 | CSS Positioning | 1.3.2 | `18.B-CSSPositionedContent` |
| 19 | Frames and iFrames | 4.1.2 | `19.A-FrameTitle` · `19.B-iFrameName` |
| 20 | Conforming Alternate Version | Conformance Requirement 1 (conforming alternate versions) | `20.A-ConformingAltVersion` |
| 21 | Timed Events | 2.2.1, 2.2.2, 1.4.2 | `21.A-TimingAdjustable` · `21.B-MovingInfo` · `21.C-AutoUpdate` · `21.D-AudioControl` |
| 22 | Resize Text | 1.4.4 | `22.A-ResizeText` |
| 23 | Multiple Ways | 2.4.5 | `23.A-MultipleWays` |
| 24 | Parsing | 4.1.1 | `24.A-Parsing` |

### Anomaly ledger (upstream defects an extractor or scorer must survive)

All present verbatim in both the published pages and the pinned sources; captured structurally in the manifest's `invalid_id_strings_on_published_pages` and `retired_sections`:

1. **`18.A` is a retired stub, not a test.** Heading (with upstream typo): "18.A for Test Procedure for Meaningful Background Image"; body redirects to `6.B` (v3.1 removed the test — CSS background images are covered there). It declares no test ID; family 18's only active test is `18.B-CSSPositionedContent`.
2. **`21.B-AutoUpdate` is not a valid ID.** The `21.C-AutoUpdate` test's Results sentence reads "then Baseline Test 21.B-AutoUpdate fails" — a pre-3.x renumbering remnant. The declared ID is authoritative.
3. **Documents page, same defect class:** `15.A-LanguageDocument`'s Results line cites `15.A-LanguagePage`, and `15.B-LanguageParts`'s cites `15.B-LanguagePart` — both *web* IDs leaked into documents Results sentences (cross-baseline confusables: valid in the web list, invalid in documents). `5.A-ControlName`'s Results line has a space typo ("Baseline Test 5.A-Control Name fails").

## Published enumeration — Documents: 57 declared tests

The Documents baseline does **not** simply mirror web families 1–24 with N/A markers (the pre-Phase-0 assumption — wrong in the details):

- **23 family sections.** Family **19 (Frames and iFrames) has no section at all** — only a note: "not implemented in non-web documents … Baseline Tests 19.A-FrameTitle and 19.B-iFrameName are not applicable to documents." Those two are not valid documents-baseline IDs.
- **Families 4 (Repetitive Content) and 23 (Multiple Ways) are retained but empty**, each citing the E205.4 exception verbatim ("was not removed to maintain harmonization").
- **`6.C-Captcha` is declared yet marked "Not applicable to documents"** — its Results text is "Baseline Test 6.C-Captcha is not applicable to documents." It counts in the 57 as a declared ID; a documents-scope outcome for it is always N/A.
- **Documents-specific IDs** replace web ones where the unit differs: `11.A-DocumentTitled`, `15.A-LanguageDocument`, `15.B-LanguageParts`, and family 18 ("Meaningful Content and Sequence") with `18.A-MeaningfulContent` + `18.B-MeaningfulSequence`. All other IDs are shared with the web list — an ID is valid only within its baseline.
- Arithmetic cross-check: 62 web − 6 (families 4, 19, 23) + 1 (documents 18 has two tests where web has one) = 57. ✓

This repo's measurement stack is web-only; the Documents baseline is a **declared boundary** (assessment Tier 3) — its IDs are listed in the manifest for validity checking, nothing more.

## Standards mapping — the version-skew traps, now source-confirmed

1. **The floor is WCAG 2.0 A/AA via Revised 508.** Web introduction: the baseline tests conformance "to Revised 508 Standards for Web, which incorporates by reference the WCAG 2.0 Level A and AA Success Criteria."
2. **WCAG 2.2 citations are reading aids, never 2.2 mappings.** Confirmed mechanism: requirement sections quote SC text but link to WCAG 2.2 Understanding articles; the v3.1 changelog states the links were mass-changed to 2.2 "for the improved explanations." The introduction is explicit that "Section 508 does not incorporate WCAG 2.2."
3. **`24.A-Parsing` always passes — verbatim.** Test Instructions: "No testing necessary." Test Results: "Baseline Test 24.A-Parsing passes." Rationale: SC 4.1.1 is deprecated in WCAG 2.2 but "is not deprecated in WCAG 2.0, and the criterion is a Section 508 requirement. However, this Baseline test will incorporate the WCAG 2.0 Errata," which deems 4.1.1 always satisfied for HTML/XML. The Limitations section adds that real markup consequences (missing roles from bad nesting, duplicate-ID name/state errors) "are covered by different Success Criteria and should be reported under those criteria." So the federal-profile trap is not "test parsing": it is knowing the test exists, auto-passes, and where its former content went.
4. **The media-player chapter discrepancy.** The test tables (family 17.A–C) cite **508 503.4 / 503.4.1 / 503.4.2** (software chapter); the introduction instead cites **415.1 / 415.1.1 / 415.1.2** (the hardware-chapter analogues, near-identical obligations phrased for "operable parts"). Cite 503.4.x when citing what the tests test.

## Non-WCAG Section 508 provisions relevant to web engagements (minimal extract)

Verbatim-anchored from the Access Board's published Revised 508 standards; this is the content a federal-profile conformance floor declaration names beyond "WCAG 2.0 A/AA":

- **E205.2 Public Facing** — public-facing electronic content shall conform to E205.4.
- **E205.3 Agency Official Communication** — non-public-facing content must conform when it "constitutes official business" and is communicated via any of nine categories: emergency notification; initial or final adjudication decision; internal or external program or policy announcement; notice of benefits, program eligibility, employment opportunity, or personnel action; formal acknowledgement of receipt; survey questionnaire; template or form; educational or training materials; intranet content designed as a Web page. (Exception: NARA-maintained archival records.)
- **E205.4 Accessibility Standard** — content conforms to WCAG 2.0 Level A and AA SC and Conformance Requirements. **Exception:** non-web *documents* are exempt from SC 2.4.1, 2.4.5, 3.2.3, and 3.2.4 (this is exactly why documents-baseline families 4 and 23 are empty); **E205.4.1** substitutes "document" for "Web page" in non-web documents.
- **E207.2.1 Word Substitution (non-web software)** — substitutes "software" for "Web page" when applying WCAG to software (quoted in the repo-only `00WCAG-Applicability.md`; relevant to the planned software baseline, not to web engagements).
- **503.4 User Controls for Captions and Audio Description** — "Where ICT displays video with synchronized audio, ICT shall provide user controls for closed captions and audio descriptions"; **503.4.1** captions selectable "at the same menu level as the user controls for volume or program selection"; **503.4.2** same for audio description. These are the only non-WCAG technical provisions the web baseline directly tests (17.A–C) — a WCAG-only review has no reason to check caption/AD **control placement**, which is why these three tests exist.
- **415.1.1 / 415.1.2** — hardware-chapter caption/AD control analogues ("operable parts"); cited by the baseline's introduction for media players, not by the test tables.
- Chapter 3 (302 Functional Performance Criteria) applies via E204 where technical provisions don't address a function — the existing `section_508_fpc_context` field's regime; no baseline test cites FPC directly.

## Alignment rules (what "using the baseline" obligates)

From the published web introduction: test processes claiming alignment "must include all baseline tests and provide baseline test results"; agencies may "streamline and combine tests" and add agency-specific tests, but those "must be identified, and these results must be reported separately from the baseline results"; shared baseline results are the trust mechanism across agencies. Alignment is a property of a *test process*, evaluable against the baseline — certification of human testers (Trusted Tester) is DHS's program, distinct from baseline alignment. Note: the fuller how-to guide `DevelopTestProcess.md` exists **only in the repo** (404 on the live site) and is legacy v2-era text (pre-refresh 1194.22 citations, old test numbering, tool-specific rows deleted from v3.0+) — its alignment principles match the introduction, but the introduction is the published authority.

## Change history (from the published Appendix B change logs)

- **Web v3.0 (Sept 2020):** the modern shape — tool-agnostic rewrite, test conditions aligned with the draft W3C ACT rules format, positive pass/fail checks, identify-content gating, and unique Baseline Test IDs introduced.
- **Web v3.0.1 (March 2021):** structural only (anchor IDs).
- **Web v3.1 (April 2024):** ID grammar changed number→letter ("1.A was 1.1"); WCAG links moved to 2.2 Understanding/Techniques; family 5 became User Controls (was "Changing Content") with new 5.B; new tests 7.C, 12.B, 16.C, 16.D, 17.G; 10 dropped "Form Changes"; 18.A removed (→6.B); 24.A instructions removed per Errata 13; the single-file all-tests pages added.
- **Documents v1.0 (Sept 2024):** initial release.

## What this settles from the adoption assessment

Corrections applied to the assessment in place: the enumeration is now exact (24 families / **62 active web tests**; **57 documents**); the family-18/21 "irregularities" are precisely characterized (retired stub; stale Results-line ID) rather than described as hyphenation issues; the Documents baseline does *not* mirror families 1–24 (family 19 absent, 4/23 retained-empty, 6.C declared-N/A); `00WCAG-Applicability.md` is the E207.2.1 word-substitution note and **not** the SC↔test crosswalk (that is the published Appendix A, at instruction granularity); `DevelopTestProcess.md` is repo-only legacy; the 4.1.1/24.A stance is resolved (always-passes, with re-routing guidance); the family-17 non-WCAG basis is 503.4.x (introduction's 415.1.x noted as the discrepancy it is); "last push 2026-08-09" was a working-branch push (`main` HEAD is 2026-07-24); and the no-documents-tag observation is confirmed fact, not conjecture.

## Recheck triggers

Re-verify this reference (and re-run the enumeration parse) on: any upstream release; **any push to `main` touching `_baselines/`**; publication from the working branches signalling churn (`keng-nextversion-3x` — a 3.x successor; `keng-porfolio-reorg` — site reorg, breaks URL anchors, archive snapshots are the hedge; `kengdoj-BaselinetoACT` — upstream ACT mapping that supersedes the manifest's hand classification by design); a quiet gap >6 months; or first use in a declared-508 engagement (executing the first federal engagement itself obligates this recheck).
