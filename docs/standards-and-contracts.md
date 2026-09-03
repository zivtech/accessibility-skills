# Standards and contracts

What this bundle targets, what shape its output takes, and where its boundaries are.

## Targets

**WCAG 2.2 AA** is the default planning and review target, including the criteria added in 2.2 (2.4.11, 2.4.13, 2.5.7, 2.5.8, 3.3.7, 3.3.8).

**Revised Section 508** is a floor, not a replacement. When an engagement declares it, the conformance target becomes "Revised Section 508: WCAG 2.0 A/AA + named provisions" and 2.2 AA stays as the recommendation layer. The default target never drops to the federal floor.

Regulatory context: [Section508.gov conformance guidance](https://www.section508.gov/develop/applicability-conformance/). Current standard: [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/).

## Orthogonality

**Conformance outcome and impact severity are orthogonal.** A criterion can fail on a defect nobody notices; a criterion can pass while a person is badly served. Report both. Never derive one from the other, and never let a severity rating stand in for an outcome.

Five further axis pairs work the same way, along with `claim_boundary` — the machine mechanism that makes the rule checkable rather than aspirational. See the [orthogonality register](a11y-orthogonality-register.md).

The three audit lenses are orthogonal too, which is why they are separate skills rather than sections of one:

| Lens | Question |
|---|---|
| `a11y-critic` | Is the accessibility approach sound? |
| `perspective-audit` | Who is blocked? |
| `a11y-role-audit` | Who on the team owns this? |

## Contracts

### Finding contract

The [A11y Evidence Finding Contract](a11y-evidence-finding-contract.md) gives `a11y-test`, `a11y-critic`, and `perspective-audit` a shared finding shape: stable IDs, fingerprints, source evidence, WCAG/APG citations, Section 508 context, perspective alarms, reproduction steps, expected versus actual behaviour, and trend language.

Optional. A clean review should emit no findings at all, not empty contracts.

### Evaluation report contract

At audit scope, the [A11y Evaluation Report Contract](a11y-evaluation-report-contract.md) aggregates findings into a WCAG-EM-shaped report: scope, conformance target, accessibility support baseline, sample set with rationale, per-SC outcomes, and an explicit coverage boundary. Findings link into it through the optional `evaluation_context` field.

Appendix A carries a worked `sample_set` serialization and Appendix B a `ratified_receipt`. Both are non-normative examples — nothing validates against either until a second independent instance exists.

The contract has its own eval lane, `evals/suites/evaluation-report/`, which measures exactly the aggregation seam: the contract document is the system prompt under test, against a no-contract baseline.

### Fix closure contract

[a11y-fix-closure-contract.md](a11y-fix-closure-contract.md) covers what has to be true before a finding is closed, and [remediation-owner-handoff.md](remediation-owner-handoff.md) covers handing work to whoever fixes it.

## WCAG-EM 2.0

Audit-scope engagements follow [WCAG-EM 2.0](https://www.w3.org/WAI/test-evaluate/conformance/wcag-em/). It is implemented across three surfaces: the planner's AUDIT-SCOPE MODE, `a11y-test`'s sampling discipline (structured sample + 10% random + representativeness check + complete processes), and the report contract above.

**EM citations belong at audit scope only.** An EM citation in a component-scope review is a finding against the output, not a sign of thoroughness.

- [Adoption assessment](wcag-em-2-adoption-assessment.md) — what was adopted, adapted, deferred, rejected
- [Verified spec reference](wcag-em-2-reference.md) — the Phase 0 gate artifact

## ICT Testing Baseline

Declared Revised-508 engagements additionally reference the [ICT Testing Baseline](https://ictbaseline.access-board.gov/) — the federal test-completeness standard defining what minimum tests a 508 conformance process must include.

It sits **beside** WCAG-EM, not on top of it: EM structures the evaluation, the baseline defines the minimum test set. Same scope rule as EM — a baseline citation in a component-scope review is a finding against the output.

Two reading traps worth knowing before you cite it. The baseline text links WCAG 2.2 *Understanding* articles as reading aids while mapping to 508's WCAG 2.0 A/AA basis; that is not a 2.2 conformance mapping. And `24.A-Parsing` always passes by upstream design.

How it is wired here:

- The planner's **FEDERAL PROFILE** in AUDIT-SCOPE MODE, where the conformance floor declaration is the gate every baseline citation passes through
- A hand-built [coverage crosswalk](../.claude/skills/a11y-test/references/ict-baseline-crosswalk.yaml) mapping all 62 web baseline tests to execution modes — 22 covered, 26 partial, 13 not-covered, 1 always-passes. **The not-covered rows are the deliverable**: they name what has to go to manual and AT methods
- An optional manifest-validated `baseline_test` field on findings and bug reports (17.A–C cite 503.4.x provisions in place of a WCAG SC)
- An optional federal annex on the evaluation report, derived from findings' `baseline_test` values — never from SC fan-out

Baseline-ID generation may be routed to a model **with** a value check, never without one. The measured failure mode is not fabricated IDs — those came back clean — but fabricated *counts*: a model claiming a number of baseline tests performed that the stack cannot perform.

- [Adoption assessment](ict-testing-baseline-adoption-assessment.md)
- [Verified reference](ict-testing-baseline-reference.md)
- [Test-ID manifest](ict-baseline-test-id-manifest.yaml) — machine-readable ground truth, 62 web / 57 documents

## OpenACR

Conformance reports serialize to GSA's [OpenACR](https://github.com/GSA/openacr) format through the routed exact-pinned `@openacr/openacr` CLI — routed, never vendored.

The finish surface is human: [acreditor.section508.gov](https://acreditor.section508.gov/) for 2.1-catalog drafts, CLI-rendered HTML for 2.2. Note the live skew — the official editor cannot import the 2.2 catalogs the frozen format itself ships.

Verified CLI behaviour and the reproduced traps are in [openacr-reference.md](openacr-reference.md); the adoption boundary is in [openacr-adoption-assessment.md](openacr-adoption-assessment.md).

## Boundaries

This bundle adopts Vital-Core's **reporting discipline** — stable evidence findings, fingerprints, trend language, benchmark gates — and none of its runtime. Explicitly out: continuous crawling, ISO-week dashboards, generated report state, Wappalyzer/ParaCharts vendors, Lighthouse/security/sustainability engines, mutable crawl state. See the [Vital-Core adoption assessment](vital-core-adoption-assessment.md).

External tools are **routed, never vendored**. `keyboard-a11y-tester`, `@guidepup/virtual-screen-reader`, `exceljs`, `@openacr/openacr`, `pa11y-ci` — each is pinned and called, and each has an adoption assessment recording what was adopted and what was deliberately left out. That is what keeps this a prompt-only repository.
