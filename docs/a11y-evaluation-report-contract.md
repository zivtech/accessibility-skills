# A11y Evaluation Report Contract

The A11y Evaluation Report Contract is the report-level companion to the finding-level [A11y Evidence Finding Contract](a11y-evidence-finding-contract.md). One evaluation report aggregates many findings; findings reference the report through the optional `evaluation_context` field, and the report references findings by `finding_id`.

Use it for **audit-scope work only**: conformance evaluations of an existing site or digital product, pre-VPAT audits, and periodic monitoring — the engagements where the planner's audit-scope mode and a11y-test's sampling discipline apply. Its shape follows WCAG-EM Step 5.1 (verified against the 2.0 Note in [wcag-em-2-reference.md](wcag-em-2-reference.md)). Do not produce an evaluation report for a component or feature review — that is the critic's finding-level territory, and an EM-shaped report there is checkbox theater.

## Required Sections

| Section | Required | Contents |
|---|---:|---|
| `evaluation_identity` | yes | Evaluator name; evaluation commissioner; evaluation date (completion date or duration); methodology + version cited (e.g., WCAG-EM 2.0 — cite the version the engagement requires). Optional: report version/identifier, repeat-evaluation dates, party responsible for the product. |
| `scope` | yes | Unambiguous in/out rule for every view (full product enclosure); named exclusions only where the engagement's own scope statement makes them explicit. |
| `conformance_target` | yes | WCAG 2 version and level (e.g., WCAG 2.2 AA). |
| `accessibility_support_baseline` | yes | The explicit OS + browser + assistive technology combinations evaluated against. If tools were added mid-evaluation, the extended baseline — as evaluated, not as originally planned. |
| `additional_requirements` | when agreed | Report template (e.g., VPAT edition), issue granularity, user involvement, or other commissioner requirements. |
| `technologies_relied_upon` | yes | Technologies relied upon for conformance (HTML, CSS, JS, WAI-ARIA, PDF...). Optional: common views, essential functionality, sample-type variety, other relevant samples from exploration. |
| `sample_set` | yes | Three parts, each with rationale: structured samples (what each represents — template, functionality, technology, shared component); random samples **and the selection method**; complete processes with their default and branch sequences. State coverage per sample. If sampling was skipped because the whole product was evaluated, say so. |
| `outcomes` | yes | Per-SC outcomes across the sample set using the EARL vocabulary already documented in `bug-reporting`: `passed` / `failed` / `cantTell` / `inapplicable` / `untested`. At least one example per conformance requirement and per SC not met. The representativeness-check result (did the random sample surface new content types or findings, and what was expanded in response). |
| `findings` | yes | The `finding_id` list of A11y Evidence Finding Contract blocks backing the outcomes. Severity in those findings stays user-impact-based and **orthogonal** to conformance outcomes. |
| `coverage_boundary` | yes | Every sample the web measurement stack (Playwright, axe-core, CDP) could not measure — native screens, kiosk hardware, documents — and the manual/AT method that covered it instead. "None" is a valid value; silence is not. |
| `evaluation_statement` | optional | Only when every non-optional methodology requirement is satisfied and all evaluated samples meet the target level. Includes issue date, guidelines title/version/URI, level, product definition, technologies relied upon, and baseline. Partial-conformance statements name the non-conforming areas and the reason. Sampling-based evaluation alone does not support a WCAG 2 conformance claim for the whole product — statements must not imply one. |
| `aggregated_score` | discouraged | WCAG-EM cautions that scores can mislead. If the commissioner requires one, document the scoring approach alongside it. |
| `machine_readable` | optional | EARL export reference, when produced. |

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
