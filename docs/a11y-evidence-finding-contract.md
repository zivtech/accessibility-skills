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
| `detected_by` | optional | Machine-detector findings only: the list of scanner engines that produced this finding on the same target, e.g. `[axe-core, html_codesniffer]`. Each entry is an engine id, not a rule id (engines name the same defect differently). See Cross-Detector Corroboration below. |
| `corroboration` | optional | Machine-detector findings only: `single` (one engine) or `corroborated` (≥2 distinct engines agree on the same WCAG criterion + target; same-family agreement is a weaker signal than cross-family — see below). A triage-confidence tag, never a conformance input. Absent on non-detector findings. See Cross-Detector Corroboration below. |

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

## Cross-Detector Corroboration

Running more than one machine detector over the same page serves two ends, and
neither is ranking one engine against another: **breadth** — the union of what
the engines flag is a broader automated candidate net than any one of them — and
**aggregate signal** — where independent engines agree, that agreement is itself
a triage signal, and the combined output is a source to mine (engines serialize
different detail). This section covers the agreement axis; the breadth axis and
the lane mechanics live in the `a11y-test` *Supplemental detector lanes* section.

Agreement makes structured the rule the `a11y-test` *Detector-lane authority
boundary* section already states in prose: *cross-tool agreement on the same
target raises triage priority; it never confirms a defect by itself, and an
absence of detection is not evidence of conformance.*

Two optional fields carry it:

- `detected_by` — the engines whose detections were merged into this finding, as
  a list of engine ids. Use the fixed vocabulary `axe-core`, `html_codesniffer`,
  `alfa`, `wave` (extend it deliberately, not ad hoc, so the values stay
  joinable).
- `corroboration` — `single` when one engine produced the finding, `corroborated`
  when two or more **distinct** engines did. "Distinct" means different engines,
  not necessarily different families: any two set `corroborated`; the family split
  below qualifies how much weight the tag carries, it does not gate the tag.

**Corroboration is decided by merging, then fingerprinting once — not by
comparing per-engine fingerprints.** Each engine's raw output keeps its own
identity and receipt (its own rule/item id, selector, and raw JSON, retained
under the append-only rule). A single contract finding is assembled for the
defect, and its `fingerprint` is computed once on that merged finding — never
embedding any engine's rule or item id (the "never rule id" rule extends to the
fingerprint's inputs). Do **not** fingerprint each engine's output separately and
join on hash equality: the per-tool recipes deliberately embed engine-specific
targets (a WAVE item id, an Alfa serialization id — and Alfa emits no selector at
all), so per-engine fingerprints never collide and corroboration would silently
stay `single` forever. "Same target" is a normalization judgment — the same
rendered element or component — never selector-string equality.

**The join is on WCAG criterion, never rule id.** Engines name the same defect
differently (axe `color-contrast`, Alfa `sia-r69`, WAVE `contrast_error` all map
to 1.4.3), so two detections corroborate only when they share the same
`wcag_or_apg` criterion on the same normalized target. Each engine's own
item→criterion mapping is therefore load-bearing: Alfa's is `rule.uri` → the
rule's `requirements` where `type === "criterion"`; WAVE's is its documented
item→success-criterion mapping. A detection whose criterion cannot be resolved
cannot corroborate — it stays `single` rather than being force-matched.

**Word choice is deliberate: `corroborated`, not "confirmed."** In this bundle
"confirmed" belongs to the human/AT verification tier (the
[human verification walk-through](../.claude/skills/a11y-test/references/human-verification-walkthrough.md)
and the fix-closure `attestation` block). Scanner agreement never reaches that
bar — the *Detector-lane authority boundary* says cross-tool agreement "never
confirms a defect by itself." So `corroborated` is a triage-confidence tag: it
raises the priority of a *detection*, never establishes that a criterion conforms
or fails, and never enters an outcome map.

**Same-family agreement is weaker than it looks.** axe-core, HTML_CodeSniffer,
and Alfa test the same machine-decidable ~30–40% of WCAG (axe and Alfa via
ACT-style rules, HTML_CodeSniffer via Squiz's older techniques-based checks); two
of them agreeing is common *because they overlap*, and they tend to miss — and to
false-positive on — the same hard cases together. Agreement across engine
*families* (for example WebAIM's WAVE against axe) is a stronger signal than
agreement within one. When it matters, note the family split in a trailing line
rather than treating a same-family pair as independent confirmation.
Corroboration counts detections that agree; it never counts a silence as
agreement — an engine that did not flag a target contributes nothing, for or
against.

**A corroboration tag is never load-bearing for validity.** A lane that becomes
unavailable (no WAVE credit, an engine dropped) costs a finding only its
corroboration tag, never its validity — the finding stands on its own evidence.
No workflow may *require* cross-family corroboration, which would make the one
commercial engine (WAVE) a de facto dependency; the stronger cross-family signal
is a bonus when present, never a gate.

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
