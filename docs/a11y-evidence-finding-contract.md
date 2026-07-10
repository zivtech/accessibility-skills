# A11y Evidence Finding Contract

The A11y Evidence Finding Contract is an optional per-finding block shared by `a11y-test`, `a11y-critic`, and `perspective-audit`. It exists to make measured or source-backed accessibility findings stable across reruns, benchmarks, and handoffs.

Do not emit a contract for passing checks or clean reviews. A clean result with no findings should say that clearly and avoid empty ritual fields.

## Required Fields

| Field | Required | Meaning |
|---|---:|---|
| `finding_id` | yes | Stable lowercase identifier for the finding, at least 8 characters. |
| `fingerprint` | yes | Stable 8-64 character hex hash derived from component/target/rule, not a route alone. |
| `source` | yes | Test command, spec name, axe rule id, snapshot ref, source file, or critic/audit source. |
| `wcag_or_apg` | yes | WCAG 2.2 criterion or WAI-ARIA APG pattern citation. |
| `section_508_fpc_context` | yes | Section 508/FPC context when applicable, or explicit "not in scope" boundary. |
| `severity` | yes | `CRITICAL`, `MAJOR`, `MINOR`, or `ENHANCEMENT`. |
| `perspective_alarms` | yes | Perspective alarm map such as `screen_reader_semantic=HIGH; keyboard_motor=LOW`. |
| `evidence` | yes | File:line, DOM excerpt, axe node, screenshot, keyboard trace, measured ratio, or source excerpt. |
| `reproduction_steps` | yes | Commands or user steps needed to reproduce the finding. |
| `expected_behavior` | yes | What the user or assistive technology should experience. |
| `actual_behavior` | yes | What the evidence shows happened instead. |
| `trend` | optional | One of `new`, `persistent`, `worsening`, `improving`, or `resolved`. |

## Example

```markdown
### A11y Evidence Finding
finding_id: a11y_form_error_describedby
fingerprint: a1b2c3d4
source: a11y-test Playwright keyboard and axe evidence
wcag_or_apg: WCAG 1.3.1 Info and Relationships
section_508_fpc_context: Revised Section 508 maps web conformance to WCAG 2.0 Level A/AA; FPC context: screen reader access
severity: MAJOR
perspective_alarms: screen_reader_semantic=HIGH; keyboard_motor=LOW; cognitive_neurodivergent=MEDIUM
evidence: LoginForm.tsx:72 input has aria-invalid but no aria-describedby pointing to visible error text
reproduction_steps: Submit an empty email field, focus the email input, and inspect the accessible description
expected_behavior: Screen reader announces the field label and associated error description
actual_behavior: Screen reader receives invalid state but no programmatic error description
trend: persistent
```

## Fingerprint Guidance

Build fingerprints from stable properties:

- Component or artifact name.
- Selector, accessible name, or semantic target.
- Rule, APG pattern, or WCAG criterion.
- Finding kind, such as keyboard failure or missing relationship.

Avoid route-only fingerprints. A page URL can change while the same underlying component bug persists, and one route can contain many distinct findings.

## keyboard-a11y-tester Source Mapping

When wrapping a `keyboard-a11y-tester` journey-audit finding (adopted 2026-07-10, see the [adoption assessment](keyboard-a11y-tester-adoption-assessment.md)) in this contract:

| Contract field | Mapping from the tool's finding shape |
|---|---|
| `source` | `keyboard-a11y-tester <batch or driven> @ <pinned SHA>, <finding id or step id(s)>` |
| `severity` | `serious` → MAJOR (CRITICAL if it blocks the journey goal); `moderate` → MINOR or MAJOR by user impact; `minor` and all AAA-informative → ENHANCEMENT |
| `fingerprint` | derive from selector + WCAG SC + check kind. Do not reuse the tool's `id` — it embeds the viewport and is run-scoped. |
| `perspective_alarms` | `persona: keyboard` → `keyboard_motor`; `persona: screen-reader` → `screen_reader_semantic` |
| `evidence` | trace step ids + measured values (e.g., `step_0003: outline 3px solid; AAA contrast 2.34`), or census selector for structural findings |
| `reproduction_steps` | the serve/step keystroke sequence from the trace, or the batch command + URL |

Calibration: never wrap a batch-crawl 4.1.3 "silent live region" finding as a failure — it is a verification prompt; re-test with a driven session and cite `live_announcements` presence/absence instead.

## Trend Language

Use trend only when comparing against prior evidence:

- `new`: not seen in the prior comparable run.
- `persistent`: still present with materially the same fingerprint.
- `worsening`: affects more routes, more components, higher severity, or more users than before.
- `improving`: still present, but affected scope or severity decreased.
- `resolved`: previously present and now verified absent.

Do not infer trend from a single run.

## Section 508 and WCAG Boundary

For this bundle, WCAG 2.2 AA is the current planning and review target. Section 508 context should be used carefully:

- Use Section 508 language when the project scope explicitly requires Revised Section 508.
- Map Section 508 web conformance to WCAG 2.0 Level A/AA.
- Do not label WCAG 2.1 or 2.2-only criteria as Section 508 failures unless the project policy explicitly adopts them.

## Perspective and ARRM Routing

`perspective_alarms` should preserve the access-risk signal that triggered review. Any MEDIUM or HIGH alarm can trigger `perspective-audit`, which should keep ARRM ownership in its normal `Route to` field.

Common perspective keys:

- `screen_reader_semantic`
- `keyboard_motor`
- `magnification_reflow`
- `environmental_contrast`
- `vestibular_motion`
- `auditory_access`
- `cognitive_neurodivergent`

The contract adds traceability. It does not replace the critic or auditor's judgment about severity, ownership, or user impact.
