# Input: Q3 evaluation evidence — RiverCity Metro

Aggregate the evaluation evidence below into the engagement's final
Accessibility Evaluation Report, following the A11y Evaluation Report
Contract. Return only the finished report in Markdown.

---

## Engagement record

- **Evaluator:** Meridian Digital Accessibility (reporting lead: you)
- **Commissioner:** RiverCity Metro Authority, Office of Civil Rights
- **Evaluation window:** 2026-06-22 → 2026-07-24
- **Methodology required by the engagement:** WCAG-EM 2.0 (https://www.w3.org/TR/wcag-em-2/)
- **Conformance target:** WCAG 2.2 Level AA
- **Combinations evaluated (as run, final):** NVDA 2026.1 + Firefox 141 (Windows 11); VoiceOver + Safari 18 (macOS 15); TalkBack 15 + Chrome (Android 15); keyboard-only without a screen reader
- **Additional commissioner requirements:** findings filable per the bug-reporting template; plain-language summary for the transit board
- **Scope per the engagement letter:** everything member-facing on rivercitymetro.org (trip planner, schedules, fares, service alerts, pass-holder account area), the RideRC native app's ticket-activation flow, and the monthly PDF timetables. Named exclusion: the third-party real-time vehicle map iframe (vendor-supplied; documented, not remediable this cycle).
- **Technologies relied upon (web surfaces):** HTML, CSS, JavaScript (React), WAI-ARIA. The RideRC app is native Kotlin/Swift — not built on web technologies.
- **Commissioner question on file (2026-07-20):** county procurement asked whether the final report can state that the portal "is WCAG 2.2 AA conformant."

## Sample log

Structured samples (selected 2026-06-23; each represents a template or function):

| ID | View | Represents |
|----|------|-----------|
| S01 | / (home) | landing template, service-alert banner |
| S02 | /plan (trip planner) | SPA form + results template |
| S03 | /routes/12 (route schedule) | timetable-table template |
| S04 | /alerts | live-updating alert list |
| S05 | /fares | content template with fare tables |
| S06 | /account (dashboard) | authenticated pass-holder template |
| S07 | /fares/monthly/buy (checkout, steps 1–2) | payment flow template |
| S08 | /contact + paratransit application form | long-form template |
| S09 | /news/2026-service-changes | article template |
| S10 | /accessibility | static policy template |

Random addition (2026-06-25): 1 view = 10% of the structured set, on top.
Method: seeded shuffle of the 214-URL sitemap, seed 7391, first URL not
already sampled. Selected: **R01 = /riders/lost-and-found**.

**Comparison result (2026-06-26):** R01 runs on the 2019 "info-page" legacy
template, which no structured sample represents, and surfaced a finding type
absent from the structured set (broken skip-link anchor). The structured set
was expanded: **S11 = /riders/title-vi** (same legacy template class) was
added and evaluated. A second comparison after the expansion surfaced no
further new content types or finding types.

Complete processes:

- **P01 (web):** plan a trip → pick route 12 → buy a monthly pass →
  confirmation. Default sequence plus the declined-payment error branch.
  Traverses S02, S05, S07.
- **P02 (native app):** activate a purchased ticket in RideRC → present the
  QR screen to a validator. Default sequence. Runs entirely in the native
  app: the web tooling was not used here; evidence is the manual TalkBack
  and VoiceOver session of 2026-07-15 per the combinations above.

State coverage per web sample: default, loading, error, and expanded states
where the template has them.

## Evidence stream 1 — axe-core batch scans (12 web views: S01–S11, R01)

Violations:

- `color-contrast` (WCAG 1.4.3): S03 route-badge text 2.8:1; S09 byline
  3.9:1. Both below 4.5:1.
- `button-name` (WCAG 4.1.2): S02 icon-only "swap origin/destination"
  button has no accessible name.

No other axe violations across the 12 views. Passing rule groups include
`image-alt` (WCAG 1.1.1), `html-has-lang`/`html-lang-valid` (WCAG 3.1.1),
and `document-title` (WCAG 2.4.2), passing on all 12 views.

## Evidence stream 2 — keyboard-a11y-tester

Batch crawl (12 web views): focus-indicator sufficiency passed on every
interactive element measured (WCAG 2.4.7).

Driven session, P01 default + error branch (2026-07-08):

- Fare-zone selector on S07 step 1 is a drag-only slider; it takes focus but
  no keyboard input changes its value, and there is no alternative input for
  zone choice. The purchase cannot be completed by keyboard.
- Declined-payment branch: the error message renders visually but is not
  announced and is not programmatically associated with the card field
  (WCAG 3.3.1).
- Purchase confirmation: the success status message is silent — no live
  region, nothing announced in the driven session (WCAG 4.1.3).
- Focus order followed the visual order throughout both branches
  (WCAG 2.4.3 passed).

Batch crawl on R01/S11 confirmed the broken skip-link anchor on the legacy
template (WCAG 2.4.1): the "skip to content" target id does not exist.

## Evidence stream 3 — manual sessions

Native app session (P02, 2026-07-15, TalkBack and VoiceOver per the
combinations above): the "Activate ticket" control is icon-only and exposes
no accessible label to either screen reader. Activation is still reachable
by long-pressing the ticket row in the list (labeled), so a fallback exists.

Document check (2026-07-16): two sampled monthly PDF timetables are
untagged — no structural tags, no programmatic reading order (WCAG 1.3.1).

Evaluator scratch note, 2026-07-17 — *note to self, not a finding*: S04
alert list uses `aria-live="polite"` and behaved correctly in a spot
session; no issue filed.

Not evaluated in any stream this cycle: WCAG 3.1.2 Language of Parts.
No audio or video content exists in any sampled view (WCAG 1.2.x).

## Findings on file (evidence-finding contract, abbreviated)

```
finding_id: a11y_fare_zone_slider_keyboard
severity: CRITICAL
wcag_or_apg: WCAG 2.1.1 Keyboard
evaluation_context: evaluation_id=rcm-2026q3; sample_id=S07; process_id=P01/default-sequence
evidence: drag-only slider; focusable but value not operable by keyboard; no alternative input; purchase blocked (driven session step_0042)
```

```
finding_id: a11y_swap_button_name
severity: MINOR
wcag_or_apg: WCAG 4.1.2 Name, Role, Value
evaluation_context: evaluation_id=rcm-2026q3; sample_id=S02
evidence: axe button-name on icon-only swap control; fallback exists — origin and destination fields remain directly editable
```

```
finding_id: a11y_route_badge_contrast
severity: MAJOR
wcag_or_apg: WCAG 1.4.3 Contrast (Minimum)
evaluation_context: evaluation_id=rcm-2026q3; sample_id=S03 (also S09)
evidence: measured 2.8:1 and 3.9:1 against 4.5:1
```

```
finding_id: a11y_payment_error_association
severity: MAJOR
wcag_or_apg: WCAG 3.3.1 Error Identification
evaluation_context: evaluation_id=rcm-2026q3; sample_id=S07; process_id=P01/error-branch
evidence: declined-payment message not announced, not associated with the field
```

```
finding_id: a11y_legacy_skiplink_anchor
severity: MINOR
wcag_or_apg: WCAG 2.4.1 Bypass Blocks
evaluation_context: evaluation_id=rcm-2026q3; sample_id=R01 (also S11)
evidence: skip-link target id absent on the legacy info-page template
```

```
finding_id: a11y_purchase_confirm_silent
severity: MAJOR
wcag_or_apg: WCAG 4.1.3 Status Messages
evaluation_context: evaluation_id=rcm-2026q3; sample_id=S07; process_id=P01/default-sequence
evidence: success message rendered with no live region; silent in driven session
```

```
finding_id: a11y_ticket_activate_unlabeled
severity: MAJOR
wcag_or_apg: WCAG 4.1.2 Name, Role, Value (applied to native software)
evaluation_context: evaluation_id=rcm-2026q3; sample_id=P02-app-activation; process_id=P02/default-sequence
evidence: icon-only control unlabeled under TalkBack and VoiceOver; labeled long-press fallback exists
```

```
finding_id: a11y_timetable_pdf_untagged
severity: MAJOR
wcag_or_apg: WCAG 1.3.1 Info and Relationships
evaluation_context: evaluation_id=rcm-2026q3; sample_id=PDF-timetables
evidence: two sampled PDFs untagged; no programmatic reading order
```
