# Input: ACR drafting request — RiverCity Metro Rider Portal (rcm-2026q3)

The audit-scope evaluation below is finished and delivered. Serialize it into
a draft Accessibility Conformance Report in OpenACR YAML per the engagement
record. Return the complete OpenACR YAML document in a single ```yaml code
fence, followed by the handoff message for the engagement owner.

---

## Engagement record (ACR-feed fields)

- **Report title:** RiverCity Metro Rider Portal Accessibility Conformance Report
- **Product:** RiverCity Metro Rider Portal, version 2026.3 — the public
  rider portal for trip planning, schedules, fares, service alerts, and
  pass-holder accounts.
- **Drafting evaluator (ACR author):** Meridian Digital Accessibility;
  contact: Dana Okafor; email: dana.okafor@meridian-a11y.example;
  website: https://meridian-a11y.example
- **Party responsible for the product (vendor block):** RiverCity Metro
  Authority, Digital Services; email: digital@rivercitymetro.example
- **Report date for the ACR:** 2026-07-28 — the evaluation completion date,
  including the follow-up session. Use this date.
- **OpenACR document version:** 1 (first OpenACR for this product).
- **Feedback channel:** https://rivercitymetro.example/accessibility-feedback
- **Publication license:** the Authority has not decided one — leave unset.
- **Report template requirement** (from the audit plan's additional
  requirements): ACR in OpenACR format, catalog
  `2.5-edition-wcag-2.2-508-en` (WCAG 2.2 edition). Finish surface: YAML
  plus CLI-rendered HTML review.

## Finished evaluation report (delivered 2026-07-28, contract-conformant)

### Evaluation identity

Evaluator: Meridian Digital Accessibility (reporting lead: Dana Okafor).
Commissioner: RiverCity Metro Authority, Office of Civil Rights.
Evaluation window: 2026-06-22 → 2026-07-28 (base window closed 2026-07-24; a
follow-up session on 2026-07-28 closed the one open criterion — see
Outcomes). Methodology: WCAG-EM 2.0 (https://www.w3.org/TR/wcag-em-2/).

### Scope

Everything member-facing on rivercitymetro.org (trip planner, schedules,
fares, service alerts, pass-holder account area), the RideRC native app's
ticket-activation flow, and the monthly PDF timetables. Named exclusion: the
third-party real-time vehicle map iframe (vendor-supplied; documented, not
remediable this cycle).

### Conformance target

WCAG 2.2 Level AA.

### Accessibility support baseline

NVDA 2026.1 + Firefox 141 (Windows 11); VoiceOver + Safari 18 (macOS 15);
TalkBack 15 + Chrome (Android 15); keyboard-only without a screen reader.

### Technologies relied upon

HTML, CSS, JavaScript (React), WAI-ARIA. The RideRC app is native
Kotlin/Swift — not built on web technologies. PDF timetables are PDF 1.7.

### Sample set

Structured samples (11): S01 home, S02 trip planner, S03 route schedule,
S04 service alerts, S05 fares, S06 account dashboard, S07 checkout steps
1–2, S08 contact + paratransit application form, S09 news article,
S10 accessibility policy, S11 title-vi (legacy info-page template — added
after the representativeness check). Random sample (1): R01
/riders/lost-and-found — seeded shuffle of the 214-URL sitemap, seed 7391.
Complete processes (2): P01 plan trip → buy monthly pass → confirmation
(web; default + declined-payment error branch, traverses S02/S05/S07);
P02 activate a purchased ticket in the RideRC native app (manual AT session
— outside the web measurement stack). State coverage per web sample:
default, loading, error, and expanded states where the template has them.

Representativeness check: R01 surfaced the 2019 legacy info-page template
missing from the structured set → S11 added and evaluated; the second
comparison surfaced no further new content types or finding types.

### Outcomes — web component, per SC across the sample set

Outcomes below are for the **web** samples (S01–S11, R01, P01). Native-app
and PDF evidence is non-web and listed separately under Non-web evidence.

| SC | Name | Level | Web outcome across samples | Failing samples | finding_id(s) |
|----|------|-------|---------------------------|-----------------|---------------|
| 1.1.1 | Non-text Content | A | passed | — | — |
| 1.2.1 | Audio-only and Video-only (Prerecorded) | A | inapplicable — no audio or video content exists in any sampled view | — | — |
| 1.2.2 | Captions (Prerecorded) | A | inapplicable — no media | — | — |
| 1.2.3 | Audio Description or Media Alternative (Prerecorded) | A | inapplicable — no media | — | — |
| 1.3.1 | Info and Relationships | A | passed (web samples; the untagged PDFs are electronic-document evidence — see Non-web evidence) | — | — |
| 1.3.2 | Meaningful Sequence | A | passed | — | — |
| 1.3.3 | Sensory Characteristics | A | passed | — | — |
| 1.4.1 | Use of Color | A | passed | — | — |
| 1.4.2 | Audio Control | A | inapplicable — no auto-playing audio | — | — |
| 2.1.1 | Keyboard | A | failed in S07 (both P01 branches); passed in every other sample | S07 | a11y_fare_zone_slider_keyboard |
| 2.1.2 | No Keyboard Trap | A | passed | — | — |
| 2.1.4 | Character Key Shortcuts | A | inapplicable — no character-key shortcuts implemented | — | — |
| 2.2.1 | Timing Adjustable | A | passed (session warning + extend control verified in S06/S07) | — | — |
| 2.2.2 | Pause, Stop, Hide | A | passed (alert ticker has pause control) | — | — |
| 2.3.1 | Three Flashes or Below Threshold | A | passed | — | — |
| 2.4.1 | Bypass Blocks | A | failed on the legacy template (R01, S11); passed elsewhere | R01, S11 | a11y_legacy_skiplink_anchor |
| 2.4.2 | Page Titled | A | passed | — | — |
| 2.4.3 | Focus Order | A | passed (verified across both P01 branches) | — | — |
| 2.4.4 | Link Purpose (In Context) | A | passed | — | — |
| 2.5.1 | Pointer Gestures | A | passed (map excluded; slider is single-pointer) | — | — |
| 2.5.2 | Pointer Cancellation | A | passed | — | — |
| 2.5.3 | Label in Name | A | passed | — | — |
| 2.5.4 | Motion Actuation | A | inapplicable — no motion-actuated functions | — | — |
| 3.1.1 | Language of Page | A | passed | — | — |
| 3.2.1 | On Focus | A | passed | — | — |
| 3.2.2 | On Input | A | passed | — | — |
| 3.2.6 | Consistent Help | A | passed (contact link consistent across templates) | — | — |
| 3.3.1 | Error Identification | A | failed in the P01 declined-payment branch (S07); passed elsewhere | S07 | a11y_payment_error_association |
| 3.3.2 | Labels or Instructions | A | passed | — | — |
| 3.3.7 | Redundant Entry | A | passed (P01 re-uses entered data) | — | — |
| 4.1.1 | Parsing | A | inapplicable — criterion removed in WCAG 2.2; the VPAT 2.5 catalog retains the row. Record as not applicable with the removal note. | — | — |
| 4.1.2 | Name, Role, Value | A | failed in S02; passed in every other sample | S02 | a11y_swap_button_name |
| 1.2.4 | Captions (Live) | AA | inapplicable — no media | — | — |
| 1.2.5 | Audio Description (Prerecorded) | AA | inapplicable — no media | — | — |
| 1.3.4 | Orientation | AA | passed | — | — |
| 1.3.5 | Identify Input Purpose | AA | failed in S07 and S08 — the only samples containing input-purpose fields; no autocomplete tokens anywhere they apply | S07, S08 | a11y_form_autocomplete_missing |
| 1.4.3 | Contrast (Minimum) | AA | failed in S03 and S09; passed elsewhere | S03, S09 | a11y_route_badge_contrast |
| 1.4.4 | Resize text | AA | passed | — | — |
| 1.4.5 | Images of Text | AA | passed | — | — |
| 1.4.10 | Reflow | AA | passed | — | — |
| 1.4.11 | Non-text Contrast | AA | passed | — | — |
| 1.4.12 | Text Spacing | AA | passed | — | — |
| 1.4.13 | Content on Hover or Focus | AA | passed (tooltip pass on S02/S07 dismissible + hoverable) | — | — |
| 2.4.5 | Multiple Ways | AA | passed (search + sitemap + nav) | — | — |
| 2.4.6 | Headings and Labels | AA | passed | — | — |
| 2.4.7 | Focus Visible | AA | passed (focus-indicator sufficiency measured on every interactive element) | — | — |
| 2.4.11 | Focus Not Obscured (Minimum) | AA | passed (sticky header verified not to cover focused items) | — | — |
| 2.5.7 | Dragging Movements | AA | passed everywhere except the fare-zone slider, which is recorded under 2.1.1 as the operability failure; a keyboard/button alternative is absent there — the slider evidence is carried by a11y_fare_zone_slider_keyboard. Panel decision 2026-07-22: single-pointer operation without dragging is available (tap-to-position), so 2.5.7 itself passed | — | — |
| 2.5.8 | Target Size (Minimum) | AA | passed | — | — |
| 3.1.2 | Language of Parts | AA | passed — follow-up session 2026-07-28 evaluated the Spanish-language fragments across all 12 web samples (previously untested; now closed) | — | — |
| 3.2.3 | Consistent Navigation | AA | passed | — | — |
| 3.2.4 | Consistent Identification | AA | passed | — | — |
| 3.3.3 | Error Suggestion | AA | passed (field-level suggestions in S08 forms) | — | — |
| 3.3.4 | Error Prevention (Legal, Financial, Data) | AA | passed (P01 review step + confirmation before charge) | — | — |
| 3.3.8 | Accessible Authentication (Minimum) | AA | passed (password managers supported; no cognitive test) | — | — |
| 4.1.3 | Status Messages | AA | failed at the P01 purchase confirmation (S07); the S04 alert list passed (aria-live verified in a spot session) | S07 | a11y_purchase_confirm_silent |

AAA criteria: not evaluated — the engagement's conformance target is
WCAG 2.2 AA and no AAA evidence was collected.

Evaluator scratch note, 2026-07-17 — *note to self, not a finding*: S04
alert list uses `aria-live="polite"` and behaved correctly in a spot
session; no issue filed.

### Non-web evidence (outside the web component)

- RideRC native app (P02, manual TalkBack + VoiceOver session 2026-07-15):
  the "Activate ticket" control is icon-only and unlabeled under both screen
  readers; a labeled long-press fallback exists. Finding
  a11y_ticket_activate_unlabeled. Native software evidence — not web.
- Monthly PDF timetables (manual document check 2026-07-16): two sampled
  PDFs are untagged — no structural tags, no programmatic reading order.
  Finding a11y_timetable_pdf_untagged. Electronic-document evidence — not
  web.

### Findings on file (evidence-finding contract, abbreviated)

```
finding_id: a11y_fare_zone_slider_keyboard
fingerprint: 7c1f22ab
severity: CRITICAL
wcag_or_apg: WCAG 2.1.1 Keyboard
evaluation_context: evaluation_id=rcm-2026q3; sample_id=S07; process_id=P01/default-sequence
evidence: drag-only slider; focusable but value not operable by keyboard; no alternative input; purchase blocked (driven session step_0042)
```

```
finding_id: a11y_swap_button_name
fingerprint: 91d4e0c3
severity: MINOR
wcag_or_apg: WCAG 4.1.2 Name, Role, Value
evaluation_context: evaluation_id=rcm-2026q3; sample_id=S02
evidence: axe button-name on icon-only swap control; fallback exists — origin and destination fields remain directly editable
```

```
finding_id: a11y_route_badge_contrast
fingerprint: 2ab9d871
severity: MAJOR
wcag_or_apg: WCAG 1.4.3 Contrast (Minimum)
evaluation_context: evaluation_id=rcm-2026q3; sample_id=S03 (also S09)
evidence: measured 2.8:1 and 3.9:1 against 4.5:1
```

```
finding_id: a11y_payment_error_association
fingerprint: c30e51f9
severity: MAJOR
wcag_or_apg: WCAG 3.3.1 Error Identification
evaluation_context: evaluation_id=rcm-2026q3; sample_id=S07; process_id=P01/error-branch
evidence: declined-payment message not announced, not associated with the field
```

```
finding_id: a11y_legacy_skiplink_anchor
fingerprint: 5f77ab02
severity: MINOR
wcag_or_apg: WCAG 2.4.1 Bypass Blocks
evaluation_context: evaluation_id=rcm-2026q3; sample_id=R01 (also S11)
evidence: skip-link target id absent on the legacy info-page template
```

```
finding_id: a11y_purchase_confirm_silent
fingerprint: e8c2447d
severity: MAJOR
wcag_or_apg: WCAG 4.1.3 Status Messages
evaluation_context: evaluation_id=rcm-2026q3; sample_id=S07; process_id=P01/default-sequence
evidence: success message rendered with no live region; silent in driven session
```

```
finding_id: a11y_form_autocomplete_missing
fingerprint: 44b09ce6
severity: MAJOR
wcag_or_apg: WCAG 1.3.5 Identify Input Purpose
evaluation_context: evaluation_id=rcm-2026q3; sample_id=S07 (also S08)
evidence: no autocomplete tokens on name/email/address/payment fields in the checkout and application forms — the only samples where input-purpose fields exist; failed in both
```

```
finding_id: a11y_ticket_activate_unlabeled
fingerprint: 0d6b93aa
severity: MAJOR
wcag_or_apg: WCAG 4.1.2 Name, Role, Value (applied to native software)
evaluation_context: evaluation_id=rcm-2026q3; sample_id=P02-app-activation; process_id=P02/default-sequence
evidence: icon-only control unlabeled under TalkBack and VoiceOver; labeled long-press fallback exists
```

```
finding_id: a11y_timetable_pdf_untagged
fingerprint: b1590f3e
severity: MAJOR
wcag_or_apg: WCAG 1.3.1 Info and Relationships
evaluation_context: evaluation_id=rcm-2026q3; sample_id=PDF-timetables
evidence: two sampled PDFs untagged; no programmatic reading order
```

### Coverage boundary

- RideRC native app (P02 ticket activation): outside the web measurement
  stack; covered by the manual TalkBack and VoiceOver session of 2026-07-15.
  Conclusions about the native software surface are the Authority's to make
  with its mobile team.
- Monthly PDF timetables: outside the web measurement stack; covered by the
  manual document check of 2026-07-16.
- Third-party real-time vehicle map iframe: excluded by the engagement
  letter; vendor-supplied, not remediable this cycle.
- No hardware surfaces are in scope (fare validators belong to a separate
  procurement), and no support-documentation surfaces were evaluated.
- All web samples: fully covered by the web measurement stack.

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
