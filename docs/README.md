# Documentation

Start here. The root [README](../README.md) is the landing page; this is the map.

## Start here

| Document | What it answers |
|---|---|
| [skills.md](skills.md) | What each of the twelve skills does, and when to reach for it |
| [evaluation.md](evaluation.md) | How the eval suites work, the blind protocol, how to add a fixture, how to read a benchmark number |
| [tools.md](tools.md) | The toolkit every investigation runs on, what each tool cannot tell you, and what was evaluated and rejected |
| [standards-and-contracts.md](standards-and-contracts.md) | What this targets (WCAG 2.2 AA, Section 508), the output contracts, and the adoption boundaries |

## Contracts

Machine-readable output shapes the skills produce.

- [a11y-evidence-finding-contract.md](a11y-evidence-finding-contract.md) — the shared finding shape: stable IDs, fingerprints, evidence, citations
- [a11y-evaluation-report-contract.md](a11y-evaluation-report-contract.md) — audit-scope report, WCAG-EM-shaped, with the federal annex
- [a11y-fix-closure-contract.md](a11y-fix-closure-contract.md) — what must be true before a finding closes
- [a11y-orthogonality-register.md](a11y-orthogonality-register.md) — six axis pairs that must not collapse into each other, and the mechanism that checks it
- [remediation-owner-handoff.md](remediation-owner-handoff.md) — handing findings to whoever fixes them
- [ict-baseline-test-id-manifest.yaml](ict-baseline-test-id-manifest.yaml) — baseline test-ID ground truth, 62 web / 57 documents

## Verified spec references

Each is a gate artifact: the spec read and recorded before anything was built against it, so later claims can be checked rather than recalled.

- [wcag-em-2-reference.md](wcag-em-2-reference.md) — WCAG-EM 2.0
- [ict-testing-baseline-reference.md](ict-testing-baseline-reference.md) — ICT Testing Baseline
- [openacr-reference.md](openacr-reference.md) — OpenACR format and CLI, including two reproduced traps in the official toolchain

## Adoption assessments

Every external dependency and standard has one. Each records what was adopted, what was adapted, what was deliberately deferred, and what was rejected — so a future reader can tell a decision from an omission.

| Assessment | Subject |
|---|---|
| [vital-core-adoption-assessment.md](vital-core-adoption-assessment.md) | Vital-Core — reporting discipline adopted, scanner runtime rejected |
| [wcag-em-2-adoption-assessment.md](wcag-em-2-adoption-assessment.md) | WCAG-EM 2.0 at audit scope |
| [ict-testing-baseline-adoption-assessment.md](ict-testing-baseline-adoption-assessment.md) | ICT Testing Baseline for declared-508 engagements |
| [openacr-adoption-assessment.md](openacr-adoption-assessment.md) | OpenACR serialization boundary |
| [keyboard-a11y-tester-adoption-assessment.md](keyboard-a11y-tester-adoption-assessment.md) | Journey-audit execution mode |
| [virtual-screen-reader-adoption-assessment.md](virtual-screen-reader-adoption-assessment.md) | Component screen-reader assertion mode |
| [baseline-url-scan-adoption-assessment.md](baseline-url-scan-adoption-assessment.md) | URL-list scan mode |
| [error-workbook-adoption-assessment.md](error-workbook-adoption-assessment.md) | XLSX triage workbook builder |
| [content-judgment-adoption-assessment.md](content-judgment-adoption-assessment.md) | Content-judgment skill — candidate, gate not met |
| [alfa-scan-adoption-assessment.md](alfa-scan-adoption-assessment.md) | Siteimprove Alfa — negative result, recorded |

[EXTERNAL-SKILLS-INVENTORY.md](EXTERNAL-SKILLS-INVENTORY.md) is the landscape scan behind these: external accessibility skills surveyed, with adoption recommendations.

## Plans and architecture

- [PERSPECTIVE-AGENTS-PLAN.md](PERSPECTIVE-AGENTS-PLAN.md) — perspective agent architecture
- [plans/](plans/) — integration and adoption plans
- [a11y-plans/](a11y-plans/) — per-engagement accessibility plans
- [a11y-planner/](a11y-planner/), [a11y-critic/](a11y-critic/) — per-skill documentation

## Evaluation records

- [drupal-patch-evaluations/](drupal-patch-evaluations/) — Drupal core accessibility patch evaluation ledger, patches, reports
- [benchmark-charts.html](benchmark-charts.html), [webwright-benchmark-results.html](webwright-benchmark-results.html) — rendered result views
- [project-recap.html](project-recap.html) — project state overview (open locally)

Raw benchmark artifacts live in [`evals/results/`](../evals/results/), not here. Every published number traces to one.

## Writing

- [blog-post-draft.md](blog-post-draft.md), [linkedin-post-draft.md](linkedin-post-draft.md)

---

`index.html` in this directory is the published [visual explainer](https://zivtech.github.io/accessibility-skills/); GitHub Pages deploys `docs/` on push to `main`.
