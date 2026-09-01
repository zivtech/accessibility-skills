# A11y Evaluation Report Contract

The A11y Evaluation Report Contract is the report-level companion to the finding-level [A11y Evidence Finding Contract](a11y-evidence-finding-contract.md). One evaluation report aggregates many findings; findings reference the report through the optional `evaluation_context` field, and the report references findings by `finding_id`.

Use it for **audit-scope work only**: conformance evaluations of an existing site or digital product, pre-VPAT audits, and periodic monitoring — the engagements where the planner's audit-scope mode and a11y-test's sampling discipline apply. Its shape follows WCAG-EM Step 5.1 (verified against the 2.0 Note in [wcag-em-2-reference.md](wcag-em-2-reference.md)). Do not produce an evaluation report for a component or feature review — that is the critic's finding-level territory, and an EM-shaped report there is checkbox theater.

## Required Sections

| Section | Required | Contents |
|---|---:|---|
| `evaluation_identity` | yes | Evaluator name; evaluation commissioner; evaluation date (completion date or duration); methodology + version cited (e.g., WCAG-EM 2.0 — cite the version the engagement requires). Optional: report version/identifier, repeat-evaluation dates, party responsible for the product. ACR-feed fields — required whenever the engagement's report template is an ACR in OpenACR format: report title, product name + version, evaluator contact email (`author.email` is schema-required there), feedback channel. |
| `scope` | yes | Unambiguous in/out rule for every view (full product enclosure); named exclusions only where the engagement's own scope statement makes them explicit. |
| `conformance_target` | yes | WCAG 2 version and level (e.g., WCAG 2.2 AA). |
| `accessibility_support_baseline` | yes | The explicit OS + browser + assistive technology combinations evaluated against. If tools were added mid-evaluation, the extended baseline — as evaluated, not as originally planned. |
| `additional_requirements` | when agreed | Report template (e.g., VPAT edition), issue granularity, user involvement, or other commissioner requirements. |
| `technologies_relied_upon` | yes | Technologies relied upon for conformance (HTML, CSS, JS, WAI-ARIA, PDF...). Optional: common views, essential functionality, sample-type variety, other relevant samples from exploration. |
| `sample_set` | yes | Three parts, each with rationale: structured samples (what each represents — template, functionality, technology, shared component); random samples **and the selection method**; complete processes with their default and branch sequences. State coverage per sample. If sampling was skipped because the whole product was evaluated, say so. |
| `outcomes` | yes | Per-SC outcomes across the sample set using the EARL vocabulary already documented in `bug-reporting`: `passed` / `failed` / `cantTell` / `inapplicable` / `untested`. At least one example per conformance requirement and per SC not met. The representativeness-check result (did the random sample surface new content types or findings, and what was expanded in response). Every planned sample-by-SC unit carries a disposition before the report closes — see "Completeness" below. |
| `findings` | yes | The `finding_id` list of A11y Evidence Finding Contract blocks backing the outcomes. Severity in those findings stays user-impact-based and **orthogonal** to conformance outcomes. |
| `coverage_boundary` | yes | Every sample the web measurement stack (Playwright, axe-core, CDP) could not measure — native screens, kiosk hardware, documents — and the manual/AT method that covered it instead. "None" is a valid value; silence is not. |
| `evaluation_statement` | optional | Only when every non-optional methodology requirement is satisfied and all evaluated samples meet the target level. Includes issue date, guidelines title/version/URI, level, product definition, technologies relied upon, and baseline. Partial-conformance statements name the non-conforming areas and the reason. Sampling-based evaluation alone does not support a WCAG 2 conformance claim for the whole product — statements must not imply one. |
| `aggregated_score` | discouraged | WCAG-EM cautions that scores can mislead. If the commissioner requires one, document the scoring approach alongside it. |
| `machine_readable` | optional | EARL export reference and/or OpenACR draft reference, when produced. EARL is the assertion-level evidence export; OpenACR is the ACR-shaped deliverable (via the `acr-reporting` skill — recommended as of 2026-08-12, Phase 2 gate passed; format receipts in [openacr-reference.md](openacr-reference.md)). |
| `federal_annex` | optional | Declared-508 engagements only (the planner federal profile's floor declaration is the gate): per-baseline-test outcome rollup — see "Federal Annex" below. Not an ACR/VPAT. |

## Completeness

"We ran the evaluation" and "every planned sample has a result" are different claims until proven equal. A report is not complete when testing stops — it is complete when **zero** planned sample-by-SC units remain unresolved: every unit in the planned `sample_set` × applicable-SC matrix carries a visible disposition (`passed` / `failed` / `cantTell` / `inapplicable` / `untested`), and none silently drop out of the count because a page failed to load, a session ran out of time, or a sample was quietly swapped for an easier one. Untested and cantTell units still count — that is what makes an INCOMPLETE report distinguishable from a complete one, rather than the two looking identical because both omit the same gaps.

This is the report-level half of the same completeness rule `a11y-test`'s Campaign Completeness Contract states at the runner level (zero-unresolved exit condition, recovery path for unresolved operations, resumption across interrupted runs) — promoting either alone would leave the other layer's claim unstated.

## Orthogonality Rule

Conformance outcome and impact severity are different dimensions and both are reported:

- A `failed` outcome on 4.1.2 may be MINOR when the affected widget has an accessible fallback path.
- A `failed` outcome on 2.1.1 inside a checkout process is CRITICAL because the person cannot buy — not because the checklist says so.

Never derive severity from rule weight, and never collapse per-SC outcomes into a severity ranking. The report carries the outcome map; the findings carry the impact judgments.

## Example Skeleton

```markdown
# Accessibility Evaluation Report: Example Benefits Portal

## Evaluation Identity
Evaluator: ... | Commissioner: ... | Dates: 2026-08-03 → 2026-09-12
Methodology: WCAG-EM 2.0 (https://www.w3.org/TR/wcag-em-2/)

## Scope
All content on https://portal.example.gov, including the authenticated
application flow. Third-party: reCAPTCHA v2, YouTube embeds (documented,
not remediable — see Coverage Boundary and VPAT third-party language).

## Conformance Target
WCAG 2.2 Level AA

## Accessibility Support Baseline
NVDA 2026.1 + Firefox / JAWS 2026 + Chrome / VoiceOver + Safari (macOS 15,
iOS 18) / TalkBack + Chrome (Android 15) / keyboard-only / Dragon 16.

## Sample Set
Structured (12): [sample → what it represents]
Random (2 = 10%, script-selected from sitemap, seed recorded): [...]
Complete processes (2): application (6 steps + error branch), login+recovery
State coverage: default, error, loading, expanded per sample

## Outcomes
Per-SC table (passed/failed/cantTell/inapplicable/untested per criterion)
Representativeness check: random sample surfaced a legacy news template
missing from the structured set → template added, re-classified, re-run.

## Findings
a11y_appform_step3_error_assoc (CRITICAL), a11y_megamenu_esc_trap (MAJOR), ...

## Coverage Boundary
None — all samples are web views reachable by the measurement stack.
```

## Federal Annex (declared Section 508 engagements only)

When the engagement's audit-scope plan carries the planner federal profile's conformance floor declaration (WCAG 2.0 A/AA + the applicable non-WCAG 508 provisions — that declaration is the gate; without it this annex must not exist), the report may append a federal annex that rolls the per-SC outcomes up by ICT Testing Baseline web test:

- One row per web baseline test (62 at the pin — enumerated in [ict-baseline-test-id-manifest.yaml](ict-baseline-test-id-manifest.yaml); every cited ID must exist there). Each row: the test ID, the outcome (same EARL vocabulary: `passed` / `failed` / `cantTell` / `inapplicable` / `untested`), and the backing `finding_id` references.
- Derivation rule: a row is `failed` only from findings carrying that test in `baseline_test` — never from SC-level fan-out (one 4.1.2 failure does not fail every 4.1.2-citing test: `5.A`–`5.D`, `12.A`, `19.A`/`19.B` are distinct rows). A row is `passed` when its constituent SC/provision outcomes pass across the sample set AND no finding carries the test. Rows `17.A`–`17.C` derive from the 503.4.x provision checks (their findings cite the provision in `wcag_or_apg` per the evidence contract), not from the WCAG outcome map.
- Under declared 508 scope, the report's `conformance_target` declaration is the floor itself — "Revised Section 508 (WCAG 2.0 Level A/AA + the named non-WCAG provisions)" — and the per-SC outcome map is built against it. WCAG 2.2 AA appears as the separately-reported recommendation layer, never as the declared conformance target.
- `24.A-Parsing` is always `passed` by upstream design (WCAG 2.0 Errata 13) — record it that way with that note, never as evidence of markup quality.
- A coverage statement sourced from the a11y-test crosswalk (`references/ict-baseline-crosswalk.yaml` in the a11y-test skill): "designed to cover N of 62; gaps: ...", with the not-covered tests' manual/AT assignment named. Never "baseline-aligned" or "baseline-conformant".
- The floor-vs-target dual posture restated: annex outcomes are against the 508 floor; WCAG 2.1/2.2-only findings stay out of the annex's outcome rows and appear as recommendations against the bundle's 2.2 AA target.
- The annex aggregates evidence **for** whoever authors the Accessibility Conformance Report — it is not an ACR/VPAT, must not be presented as one, and carries no conformance badge for the test process itself.
- If the commissioner declines the annex, a declared-508 report still carries the plan's baseline-coverage statement — restate it alongside `coverage_boundary`, the same honesty axis (what the stack could not measure and what covered it instead).

## Lifecycle Wiring

- **a11y-planner (audit-scope mode)** plans the report skeleton in Phase 9 — the declarations exist before testing starts.
- **a11y-test** produces the measured evidence: per-sample scans, keyboard-a11y-tester driven sessions for complete processes, the random-sample comparison result, and finding contracts with `evaluation_context`.
- **bug-reporting** stays finding-level: individual findings become reproducible bug reports; this contract aggregates them and is where the EARL outcome vocabulary rolls up.
- **a11y-critic** reviews the report against this contract the way it reviews findings against the evidence contract — declarations present, sampling rationale real, boundary honest, severity not derived from rule weight.

## Re-Evaluation and Trend

On re-runs, follow WCAG-EM re-evaluation guidance: keep a sub-set of the prior sample for comparability and replace a sub-set (typically about half) for coverage. Carry the evidence contract's trend vocabulary (`new` / `persistent` / `worsening` / `improving` / `resolved`) at the finding level; report deltas at the outcome level (criteria newly passing/failing since the prior evaluation). Do not infer trend from a single run.

## Boundaries

- This contract does not replace VPAT/ACR templates or EN 301 549 report formats — when the engagement requires one, this contract is the internal evidence spine that populates it.
- It adds structure, not judgment: severity, ownership, and user impact stay with the critic, auditor, and evaluator.
- Prompt-only repo ruling applies: no report-generator runtime, no WCAG-EM Report Tool vendoring; EARL export stays a routed capability of external tools.
