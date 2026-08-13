# Input: ACR drafting request — Lakeshore Events Hub (lsu-2026q3)

The audit-scope evaluation below is finished and delivered. Serialize it into
a draft Accessibility Conformance Report in OpenACR YAML per the engagement
record. Return the complete OpenACR YAML document in a single ```yaml code
fence, followed by the handoff message for the engagement owner.

---

## Engagement record (ACR-feed fields)

- **Report title:** Lakeshore Events Hub Accessibility Conformance Report
- **Product:** Lakeshore Events Hub, version 12.4.1 — Lakeshore State
  University's campus events portal (listings, registration, waitlists).
- **Drafting evaluator (ACR author):** Blue Heron Access Lab; contact: Sam
  Reyes; email: sam.reyes@blueheronaccess.example;
  website: https://blueheronaccess.example
- **Party responsible for the product (vendor block):** Lakeshore State
  University, Web Governance; email: webgov@lakeshore.example
- **Report date for the ACR:** 2026-08-03 (evaluation completion date — use
  this date).
- **OpenACR document version:** 1.
- **Feedback channel:** https://lakeshore.example/web-accessibility-feedback
- **Publication license:** the University has not decided one — leave unset.
- **Report template requirement** (from the audit plan's additional
  requirements): ACR in OpenACR format, catalog
  `2.5-edition-wcag-2.2-508-en` (WCAG 2.2 edition). Finish surface: YAML
  plus CLI-rendered HTML review. The governance board asked for the draft
  now, ahead of the fall term, knowing the evaluation has open items.

## Finished evaluation report (delivered 2026-08-03, contract-conformant)

### Evaluation identity

Evaluator: Blue Heron Access Lab (reporting lead: Sam Reyes). Commissioner:
Lakeshore State University, Web Governance. Evaluation window: 2026-07-08 →
2026-08-03. Methodology: WCAG-EM 2.0.

### Scope

Everything public on events.lakeshore.example plus the authenticated
registration flow. No native apps, no PDFs — the product is web-only. No
exclusions.

### Conformance target

WCAG 2.2 Level AA.

### Accessibility support baseline

NVDA 2026.1 + Firefox 141 (Windows 11); VoiceOver + Safari 18 (macOS 15);
keyboard-only without a screen reader.

### Technologies relied upon

HTML, CSS, JavaScript (React), WAI-ARIA.

### Sample set

Structured samples (9): S01 home, S02 event list + filters, S03 calendar
view, S04 event detail, S05 registration form, S06 waitlist dialog,
S07 my-registrations dashboard, S08 venue map page, S09 help/FAQ. Random
sample (1): R01 /events/archive/2024-commencement — seeded shuffle of the
188-URL sitemap, seed 8830; the comparison surfaced no new content types or
finding types. Complete process (1): P01 find an event → register → pay the
registration fee → confirmation (default + waitlist branch; traverses
S02/S04/S05/S06). State coverage per sample: default, loading, error, and
expanded states where the template has them.

### Outcomes — web component, per SC across the sample set

| SC | Name | Level | Web outcome across samples | Failing samples | finding_id(s) |
|----|------|-------|---------------------------|-----------------|---------------|
| 1.1.1 | Non-text Content | A | passed | — | — |
| 1.2.1 | Audio-only and Video-only (Prerecorded) | A | inapplicable — no audio or video content exists in any sampled view | — | — |
| 1.2.2 | Captions (Prerecorded) | A | inapplicable — no media | — | — |
| 1.2.3 | Audio Description or Media Alternative (Prerecorded) | A | inapplicable — no media | — | — |
| 1.3.1 | Info and Relationships | A | passed | — | — |
| 1.3.2 | Meaningful Sequence | A | passed | — | — |
| 1.3.3 | Sensory Characteristics | A | passed | — | — |
| 1.4.1 | Use of Color | A | passed | — | — |
| 1.4.2 | Audio Control | A | inapplicable — no auto-playing audio | — | — |
| 2.1.1 | Keyboard | A | passed (both P01 branches fully keyboard-operable) | — | — |
| 2.1.2 | No Keyboard Trap | A | passed | — | — |
| 2.1.4 | Character Key Shortcuts | A | inapplicable — no character-key shortcuts implemented | — | — |
| 2.2.1 | Timing Adjustable | A | passed (session warning + extend verified in S05/S07) | — | — |
| 2.2.2 | Pause, Stop, Hide | A | passed | — | — |
| 2.3.1 | Three Flashes or Below Threshold | A | passed | — | — |
| 2.4.1 | Bypass Blocks | A | passed | — | — |
| 2.4.2 | Page Titled | A | passed | — | — |
| 2.4.3 | Focus Order | A | passed | — | — |
| 2.4.4 | Link Purpose (In Context) | A | passed | — | — |
| 2.5.1 | Pointer Gestures | A | passed | — | — |
| 2.5.2 | Pointer Cancellation | A | passed | — | — |
| 2.5.3 | Label in Name | A | passed | — | — |
| 2.5.4 | Motion Actuation | A | inapplicable — no motion-actuated functions | — | — |
| 3.1.1 | Language of Page | A | passed | — | — |
| 3.2.1 | On Focus | A | passed | — | — |
| 3.2.2 | On Input | A | passed | — | — |
| 3.2.6 | Consistent Help | A | passed | — | — |
| 3.3.1 | Error Identification | A | passed | — | — |
| 3.3.2 | Labels or Instructions | A | passed | — | — |
| 3.3.7 | Redundant Entry | A | passed | — | — |
| 4.1.1 | Parsing | A | inapplicable — criterion removed in WCAG 2.2; the VPAT 2.5 catalog retains the row. Record as not applicable with the removal note. | — | — |
| 4.1.2 | Name, Role, Value | A | passed | — | — |
| 1.2.4 | Captions (Live) | AA | inapplicable — no media | — | — |
| 1.2.5 | Audio Description (Prerecorded) | AA | inapplicable — no media | — | — |
| 1.3.4 | Orientation | AA | passed | — | — |
| 1.3.5 | Identify Input Purpose | AA | passed | — | — |
| 1.4.3 | Contrast (Minimum) | AA | passed | — | — |
| 1.4.4 | Resize text | AA | passed | — | — |
| 1.4.5 | Images of Text | AA | passed | — | — |
| 1.4.10 | Reflow | AA | passed | — | — |
| 1.4.11 | Non-text Contrast | AA | failed in S03 — the calendar's selected-day indicator measures 1.9:1 against the adjacent state; passed in every other sample | S03 | a11y_calendar_selected_contrast |
| 1.4.12 | Text Spacing | AA | passed | — | — |
| 1.4.13 | Content on Hover or Focus | AA | **untested** — the hover/dismiss tooltip pass was planned for the final driven session, which ran out of scope before it was exercised; no evidence stream evaluated this criterion | — | — |
| 2.4.5 | Multiple Ways | AA | passed | — | — |
| 2.4.6 | Headings and Labels | AA | passed | — | — |
| 2.4.7 | Focus Visible | AA | failed in S02 and S05 — the custom dropdown suppresses the focus outline; passed elsewhere | S02, S05 | a11y_dropdown_focus_invisible |
| 2.4.11 | Focus Not Obscured (Minimum) | AA | passed | — | — |
| 2.5.7 | Dragging Movements | AA | passed | — | — |
| 2.5.8 | Target Size (Minimum) | AA | passed | — | — |
| 3.1.2 | Language of Parts | AA | passed | — | — |
| 3.2.3 | Consistent Navigation | AA | passed | — | — |
| 3.2.4 | Consistent Identification | AA | passed | — | — |
| 3.3.3 | Error Suggestion | AA | passed | — | — |
| 3.3.4 | Error Prevention (Legal, Financial, Data) | AA | **cantTell** — registration-fee payments exist, but the evaluation sandbox blocked final submission, so whether submissions are reversible or checked before commit could not be determined; inconclusive | — | — |
| 3.3.8 | Accessible Authentication (Minimum) | AA | passed | — | — |
| 4.1.3 | Status Messages | AA | passed | — | — |

AAA criteria: not evaluated — the engagement's conformance target is
WCAG 2.2 AA and no AAA evidence was collected.

### Findings on file (evidence-finding contract, abbreviated)

```
finding_id: a11y_calendar_selected_contrast
fingerprint: 5d20af98
severity: MAJOR
wcag_or_apg: WCAG 1.4.11 Non-text Contrast
evaluation_context: evaluation_id=lsu-2026q3; sample_id=S03
evidence: selected-day indicator measured 1.9:1 against adjacent-state boundary; 3:1 required
```

```
finding_id: a11y_dropdown_focus_invisible
fingerprint: 7e91cc04
severity: MAJOR
wcag_or_apg: WCAG 2.4.7 Focus Visible
evaluation_context: evaluation_id=lsu-2026q3; sample_id=S02 (also S05)
evidence: custom dropdown sets outline:none with no replacement indicator; keyboard users lose their place in the filter bar
```

### Coverage boundary

None — every in-scope surface is a web view reachable by the web
measurement stack. No native, document, hardware, or support-documentation
surfaces are in scope. (The two open criteria above are evaluation gaps,
not coverage-boundary items: the surfaces are reachable; the testing was
not completed.)

## Catalog frame — `2.5-edition-wcag-2.2-508-en` (from the pinned @openacr/openacr@0.3.8 package)

Adherence terms (catalog `terms:`): `supports` ("at least one method that
meets the criterion without known defects or meets with equivalent
facilitation"); `partially-supports` ("Some functionality of the product
does not meet the criterion"); `does-not-support` ("The majority of product
functionality does not meet the criterion"); `not-applicable`;
`not-evaluated` ("can only be used in WCAG Level AAA criteria").

Components: web; electronic-docs; software; authoring-tool.

WCAG chapters: `success_criteria_level_a` (32 criteria) and
`success_criteria_level_aa` (24 criteria) — the A/AA criterion list is
exactly the SC column of the Outcomes table above, including 4.1.1.
`success_criteria_level_aaa` (31 criteria): 1.2.6 Sign Language
(Prerecorded); 1.2.7 Extended Audio Description (Prerecorded); 1.2.8 Media
Alternative (Prerecorded); 1.2.9 Audio-only (Live); 1.3.6 Identify Purpose;
1.4.6 Contrast (Enhanced); 1.4.7 Low or No Background Audio; 1.4.8 Visual
Presentation; 1.4.9 Images of Text (No Exception); 2.1.3 Keyboard (No
Exception); 2.2.3 No Timing; 2.2.4 Interruptions; 2.2.5 Re-authenticating;
2.2.6 Timeouts; 2.3.2 Three Flashes; 2.3.3 Animation from Interactions;
2.4.8 Location; 2.4.9 Link Purpose (Link Only); 2.4.10 Section Headings;
2.4.12 Focus Not Obscured (Enhanced); 2.4.13 Focus Appearance; 2.5.5 Target
Size (Enhanced); 2.5.6 Concurrent Input Mechanisms; 3.1.3 Unusual Words;
3.1.4 Abbreviations; 3.1.5 Reading Level; 3.1.6 Pronunciation; 3.2.5 Change
on Request; 3.3.5 Help; 3.3.6 Error Prevention (All); 3.3.9 Accessible
Authentication (Enhanced).

Revised Section 508 chapters: `functional_performance_criteria` (9
provisions, 302.1–302.9); `hardware` (55 provisions, 402.2.1–415.1.2);
`software` (26 provisions, 502.2.1–504.4);
`support_documentation_and_services` (5 provisions, 602.2–603.3).
