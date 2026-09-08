# Input: ACR drafting request — Linden Resident Services Portal retest

The audit-scope evaluation below is finished and delivered. Serialize it into
a draft Accessibility Conformance Report in OpenACR YAML per the engagement
record. Return the complete OpenACR YAML document in a single `yaml` code
fence, followed by the handoff message for the engagement owner.

## Engagement record

- Report title: Linden Resident Services Portal Accessibility Conformance Report
- Product: Linden Resident Services Portal, version 6.4.2
- Drafting evaluator: Northstar Inclusive Design; contact: Ana Mensah;
  email: ana.mensah@northstarinclusive.example
- Report date: 2026-09-05
- OpenACR document version: 2; supersedes the 2026-06-12 draft.
- Publication license: undecided; leave unset.
- Required catalog: `2.5-edition-wcag-2.2-508-en`.
- Finish surface: YAML plus CLI-rendered HTML review.

The initial evaluation covered version 6.3.0. Remediation shipped in 6.4.2.
The WCAG-EM retest ran 2026-08-24 through 2026-09-05 and retained four
structured samples (S01 service search, S02 permit renewal, S03 resident
profile, S04 case-status detail) and one random sample (R01 trash schedule).
The accessibility support baseline was NVDA 2026.1 with Firefox 141,
VoiceOver with Safari 18, and keyboard-only operation.

The structured samples cover each distinct template, shared navigation, and
transaction type. R01 was selected from the 38-URL public sitemap with seed
6421; comparison found no new content or finding type. Complete process P01
starts at service search, opens a permit, renews it, and confirms the updated
case status; its default and validation-error branches were both evaluated.
Default, focus, error, loading, and saved states were covered wherever each
sample exposed them. Technologies relied upon were HTML, CSS, JavaScript, and
WAI-ARIA. The conformance target was WCAG 2.2 AA.

This report does not establish results beyond the named sample set, product
version, states, or accessibility support baseline. It evaluates accessibility
conformance, not usability, performance, security, or SEO.

## Outcomes — web component

All listed outcomes apply across the complete sample set.

- Passed: 1.1.1, 1.3.1, 1.3.2, 1.3.3, 1.4.1, 2.1.1, 2.1.2, 2.2.1,
  2.2.2, 2.3.1, 2.4.1, 2.4.2, 2.4.3, 2.4.4, 2.5.1, 2.5.2, 2.5.3,
  3.1.1, 3.2.1, 3.2.2, 3.2.6, 3.3.1, 3.3.2, 3.3.7, 4.1.2, 1.3.4,
  1.3.5, 1.4.3, 1.4.4, 1.4.5, 1.4.10, 1.4.11, 1.4.12, 1.4.13,
  2.4.5, 2.4.6, 2.4.7, 2.4.11, 2.5.7, 2.5.8, 3.1.2, 3.2.3, 3.2.4,
  3.3.3, 3.3.4, 3.3.8, 4.1.3.
- Inapplicable because the product contains no relevant media or feature:
  1.2.1, 1.2.2, 1.2.3, 1.4.2, 2.1.4, 2.5.4, 1.2.4, 1.2.5.
- 4.1.1 is inapplicable because it was removed in WCAG 2.2.
- AAA criteria were not evaluated; the conformance target is WCAG 2.2 AA.

Three criteria improved from failed in the prior evaluation to passed in this
retest:

| SC | Prior result | Current result | Finding | Closure |
|---|---|---|---|---|
| 2.1.1 | failed in S02 | passed | a11y_renewal_calendar_keyboard | rem-renewal-calendar-kbd-b7310f42 |
| 4.1.3 | failed in S04 | passed | a11y_case_status_not_announced | rem-case-status-live-f2c40e19 |
| 3.3.2 | failed in S03 | passed | a11y_profile_phone_format_instruction | rem-phone-format-help-8a6d91ce |

## Findings on file

The evidence store retains the complete finding-contract records. The excerpts
below reproduce every field the ACR serializer consumes: `finding_id`,
`fingerprint`, the criterion, sample-bound `evaluation_context`, the original
observation, and trend. No omitted finding field supplies attestation or
remediation-authorship facts.

```
finding_id: a11y_renewal_calendar_keyboard
fingerprint: 814db22a
wcag_or_apg: WCAG 2.1.1 Keyboard
evaluation_context: evaluation_id=lrs-2026q3; sample_id=S02
evidence: renewal calendar dates could be selected only with a pointer
trend: resolved
```

```
finding_id: a11y_case_status_not_announced
fingerprint: e7ae928c
wcag_or_apg: WCAG 4.1.3 Status Messages
evaluation_context: evaluation_id=lrs-2026q3; sample_id=S04
evidence: a saved case-status change appeared visually without announcement
trend: resolved
```

```
finding_id: a11y_profile_phone_format_instruction
fingerprint: 32cd780f
wcag_or_apg: WCAG 3.3.2 Labels or Instructions
evaluation_context: evaluation_id=lrs-2026q3; sample_id=S03
evidence: the required telephone format was disclosed only after submission
trend: resolved
```

## Fix-closure records

```
item_id: rem-renewal-calendar-kbd-b7310f42
closes: a11y_renewal_calendar_keyboard
original_observation: renewal calendar dates could be selected only with a pointer
root_cause_triage: C-implement-fresh
fix_approach: replaced pointer-only day divs with buttons using roving tabindex and Arrow/Home/End/Enter handlers
visual_evidence: before, the active day had only a selected fill; after, the keyboard-focused day also has a persistent 3px outline while the selected fill remains unchanged
interaction_evidence: evidence/lrs-2026q3/S02-renewal-calendar-keyboard.json (sha256:61d829c4e0a37f10) — walked keyboard trace on product version 6.4.2 records Tab entry, ArrowRight movement, and Enter selection without pointer input
commit: 4f38a1d (resident-services-web PR #804), landed 2026-08-25
attestation:
  status: attested
  attested_by: "Mateo Ibarra"
  attested_at: 2026-08-27T14:10:00Z
  attested_against: {version: "6.4.2"}
  self_attested: true
  method:
    tooling: "Firefox 141, keyboard only"
    action: "Opened the renewal calendar and selected a date with arrow keys and Enter."
    expected: "Focus moves among dates and the chosen date is applied without a pointer."
    observed: "Walked PASS: focus moved among dates and Enter applied the selected date."
  second_confirmation:
    by: "Priya Okafor"
    at: 2026-08-29T10:40:00Z
    tooling: "Safari 18, keyboard only"
    observed: "Walked PASS: selected and applied a renewal date without a pointer."
  claim_boundary: "Confirms this interaction on version 6.4.2; does not establish criterion-wide conformance."
```

```
item_id: rem-case-status-live-f2c40e19
closes: a11y_case_status_not_announced
original_observation: a saved case-status change appeared visually without announcement
root_cause_triage: C-implement-fresh
fix_approach: added a persistent aria-live status node and writes the saved status text to it after the update response succeeds
visual_evidence: before and after captures show the same saved-status banner; the correction adds a programmatic announcement without changing its visible presentation
interaction_evidence: evidence/lrs-2026q3/S04-case-status-announcement.json (sha256:c9ea720bf1145d3a) — walked announcement trace on product version 6.4.2 records the saved message spoken once by NVDA with focus retained
commit: 972be6c (resident-services-web PR #807), landed 2026-08-26
attestation:
  status: attested
  attested_by: "June Park"
  attested_at: 2026-08-28T09:20:00Z
  attested_against: {version: "6.4.2"}
  self_attested: true
  method:
    tooling: "NVDA 2026.1 and Firefox 141"
    action: "Saved a case-status update while focus remained on the form."
    expected: "The saved status is announced without moving focus."
    observed: "Walked PASS: NVDA announced the saved status and focus remained in place."
  second_confirmation:
    by: "Omar Haddad"
    authored_fix: false
    at: 2026-08-30T15:35:00Z
    tooling: "VoiceOver and Safari 18"
    observed: "Walked PASS: VoiceOver announced the saved case status."
  claim_boundary: "Confirms this interaction on version 6.4.2; does not establish criterion-wide conformance."
```

```
item_id: rem-phone-format-help-8a6d91ce
closes: a11y_profile_phone_format_instruction
original_observation: the required telephone format was disclosed only after submission
root_cause_triage: C-implement-fresh
fix_approach: renders the format instruction beside the telephone field on initial load and binds it with aria-describedby
visual_evidence: before, no format text appeared until validation failed; after, "Use 10 digits, including area code" is visible beside the empty field before entry and remains after validation
interaction_evidence: evidence/lrs-2026q3/S03-phone-format-instruction.json (sha256:2ab41cfd8d65e719) — walked form trace on product version 6.4.2 records the instruction visible and programmatically associated before data entry
commit: b0c674e (resident-services-web PR #811), landed 2026-08-25
attestation:
  status: attested
  attested_by: "Elena Rossi"
  attested_at: 2026-08-26T11:05:00Z
  attested_against: {version: "6.4.2"}
  self_attested: false
  method:
    tooling: "Safari 18, keyboard only"
    action: "Navigated to the telephone field before entering a value."
    expected: "The required telephone format is available before submission."
    observed: "Walked PASS: the format instruction was present and associated with the field."
  second_confirmation:
    by: "Samira Bello"
    at: 2026-08-31T13:15:00Z
    tooling: "Firefox 141, keyboard only"
    observed: "Walked PASS: the format instruction was available before entry."
  claim_boundary: "Confirms this interaction on version 6.4.2; does not establish criterion-wide conformance."
```

## Coverage boundary

No native app, hardware, electronic-document, authoring-tool, or support
documentation surfaces are in scope. All web samples were covered by the web
measurement method.

## Catalog frame — `2.5-edition-wcag-2.2-508-en`

Adherence terms are `supports`, `partially-supports`, `does-not-support`,
`not-applicable`, and `not-evaluated`; `not-evaluated` can only be used for
WCAG Level AAA criteria. Components are web, electronic-docs, software, and
authoring-tool. The Level A and AA catalog rows are exactly the criteria in
the outcome lists above, including 4.1.1.

Level AAA criteria: 1.2.6, 1.2.7, 1.2.8, 1.2.9, 1.3.6, 1.4.6, 1.4.7,
1.4.8, 1.4.9, 2.1.3, 2.2.3, 2.2.4, 2.2.5, 2.2.6, 2.3.2, 2.3.3,
2.4.8, 2.4.9, 2.4.10, 2.4.12, 2.4.13, 2.5.5, 2.5.6, 3.1.3, 3.1.4,
3.1.5, 3.1.6, 3.2.5, 3.3.5, 3.3.6, 3.3.9.

Revised Section 508 chapters are `functional_performance_criteria`,
`hardware`, `software`, and `support_documentation_and_services`.
