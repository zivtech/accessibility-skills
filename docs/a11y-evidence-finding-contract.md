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
| `evaluation_context` | optional | Audit-scope only: `evaluation_id` plus `sample_id` (and `process_id` when the finding sits inside a complete process), linking the finding into an evaluation report's sample set. |
| `baseline_test` | optional | Declared-508 audit scope only: the ICT Testing Baseline **web** test this finding files under (e.g. `5.C-ControlState`). Valid only if the ID exists in the web list of [ict-baseline-test-id-manifest.yaml](ict-baseline-test-id-manifest.yaml) — see the Section 508 boundary rules below. |

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

Calibration: never wrap a batch-crawl 4.1.3 "silent live region" finding as a failure — it is a verification prompt; re-test with a driven session and cite `live_announcements` presence/absence instead. And never carry the tool's `conformance_level` into the finding or a report as the SC's WCAG level — it is a pass-fail (`AA`) / informative (`AAA`) gate ([upstream #27](https://github.com/ezufelt/keyboard-a11y-tester/issues/27): only the 2.4.13 check emits `AAA`; every other finding defaults to `AA`, mislabeling Level A SCs). The "AAA-informative → ENHANCEMENT" severity mapping above is the field's only safe reading; derive the SC's true WCAG level from the SC number. Drop this rule when the pin advances past a fix.

## virtual-screen-reader Source Mapping

When wrapping a `virtual-screen-reader` component-assertion result (adopted 2026-07-11, see the [adoption assessment](virtual-screen-reader-adoption-assessment.md)) in this contract — note VSR emits no findings or severities; the asserting test plus the author's judgment produce the finding, and this mapping structures it:

| Contract field | Mapping from the assertion result |
|---|---|
| `source` | `virtual-screen-reader @ <exact version>, <test file>::<test name>` |
| `severity` | by user impact, judged by the author: announcement never reaches the user on a task-critical flow → CRITICAL or MAJOR; degraded context or vague announcement text → MINOR or MAJOR; robustness/redundancy improvements → ENHANCEMENT |
| `fingerprint` | component + region selector + event kind (e.g., `toast-region + show-event + no-announcement`). Never the phrase text alone — wording changes must not change identity. |
| `perspective_alarms` | `screen_reader_semantic` only. Never `keyboard_motor` — VSR interactions are synthetic (user-event), not keyboard evidence. |
| `evidence` | the exact spoken-phrase log slice **plus** the structural fact (e.g., `phrases after mount = []; div.toast has no role/aria-live`) |
| `reproduction_steps` | install pin (`npm i -D @guidepup/virtual-screen-reader@<version>`) + committed test file path + runner command |

Calibration: never wrap a silent mount-with-content `role="alert"` as a failed fix — it is inconclusive; restate the assertion in the persistent-container shape first. An empty `"polite: "` entry is an `aria-atomic` region-clear marker. Components containing open shadow roots are outside VSR evidence entirely (record: `evals/results/virtual-screen-reader/`).

## Evaluation Context (audit scope only)

When a finding is produced inside an audit-scope engagement (see the [A11y Evaluation Report Contract](a11y-evaluation-report-contract.md)), `evaluation_context` records its sample-set membership so the report can aggregate findings and re-evaluations can compare like with like:

```
evaluation_context: evaluation_id=portal-2026q3; sample_id=S07-application-step3; process_id=application/default-sequence
```

Omit the field entirely outside audit engagements — it must not become ritual on component-scope findings.

## Trend Language

Use trend only when comparing against prior evidence:

- `new`: not seen in the prior comparable run.
- `persistent`: still present with materially the same fingerprint.
- `worsening`: affects more routes, more components, higher severity, or more users than before.
- `improving`: still present, but affected scope or severity decreased.
- `resolved`: previously present and now verified absent.

Do not infer trend from a single run.

`resolved` records what a retest observed; it does not by itself make the criterion a fixed-stage conformance input. That is decided one layer down: the finding's fix-closure record must carry a fully attested `attestation` block (a named person confirmed the fix on the product at the report's version, doing what and seeing what, and a second person or session confirmed it — [A11y Fix-Closure Contract](a11y-fix-closure-contract.md)) before `acr-reporting` will publish the improved term on a previously-failed criterion. A still-failing criterion keeps its failing entry either way. A resolved finding with a draft closure is still resolved. It is not yet a conformance input.

## Section 508 and WCAG Boundary

For this bundle, WCAG 2.2 AA is the current planning and review target. Section 508 context should be used carefully:

- Use Section 508 language when the project scope explicitly requires Revised Section 508.
- Map Section 508 web conformance to WCAG 2.0 Level A/AA.
- Do not label WCAG 2.1 or 2.2-only criteria as Section 508 failures unless the project policy explicitly adopts them.
- The federal test-completeness standard for a Section 508 conformance test process is the [ICT Testing Baseline for Web](https://ictbaseline.access-board.gov/) — what minimum tests a 508 test process must include, orthogonal to WCAG-EM's evaluation structure. Verified reference: [ict-testing-baseline-reference.md](ict-testing-baseline-reference.md); test-ID ground truth: [ict-baseline-test-id-manifest.yaml](ict-baseline-test-id-manifest.yaml).
- Baseline reading trap: baseline text quotes WCAG 2.0-basis requirements while linking WCAG 2.2 Understanding articles as reading aids — never read a 2.2 link in baseline text as a WCAG 2.2 conformance mapping. Related: baseline test `24.A-Parsing` always passes by upstream design (WCAG 2.0 Errata 13), with markup consequences re-routed to other SCs.

### `baseline_test` rules (declared 508 scope only)

"Declared 508 scope" exists iff the engagement's audit-scope plan carries the planner federal profile's conformance floor declaration (WCAG 2.0 A/AA + the applicable non-WCAG 508 provisions); the finding links into that engagement through `evaluation_context`. Under it:

- Populate `baseline_test` with the web baseline test the finding files under. Validity is per-baseline against the manifest's web list — documents-baseline IDs never appear (the documents baseline is a declared measurement boundary), and an ID not in the manifest is a fabrication, not a citation.
- The three media-player-control tests (`17.A`–`17.C`) test 508 provisions 503.4/503.4.1/503.4.2, not WCAG SCs — a caption control buried below the volume control's menu level violates 503.4.1 while 1.2.2 passes. For that class, `wcag_or_apg` carries the named provision citation instead (e.g. `508 503.4.1 caption control menu level`). This substitution is valid only under declared 508 scope; everywhere else `wcag_or_apg` keeps its WCAG/APG requirement.
- `24.A-Parsing` never appears on a finding: it always passes upstream, and real markup consequences file under the SCs they break (name/role/state and peers).
- Severity stays user-impact-based and orthogonal — never derive it from the baseline outcome, and never derive a baseline outcome from severity.
- Outside declared 508 scope the field is absent entirely; a populated `baseline_test` on a component-scope finding is itself a finding against the output.

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

## Honest Boundary Note

A finding's `evidence` field states what was observed; it does not automatically state what that observation does **not** establish, and the two get conflated easily. When a finding's evidence could plausibly be over-read — an automated-rule hit read as a full WCAG verdict, a single reproduction read as a confirmed pattern across the product, a passing scan read as "no accessibility issues" rather than "no issues this rule set detects" — say so in `actual_behavior` or a trailing note, rather than leaving the gap implicit. This is the same discipline the [A11y Evaluation Report Contract](a11y-evaluation-report-contract.md)'s required `honest_boundary` section applies at the report level; at finding granularity it stays a habit the evidence field should make explicit, not a new required field of its own.
