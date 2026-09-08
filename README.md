# Accessibility Skills

Skills and evaluation assets for planning, testing, reviewing, and auditing web accessibility — WCAG 2.2 AA by default, Revised Section 508 when an engagement declares it.

```bash
npx skills add zivtech/accessibility-skills
```

**[Visual explainer](https://zivtech.github.io/accessibility-skills/)** · **[Documentation index](docs/)** · **[Benchmarks](ollama/BENCHMARK.md)**

## What it does

Accessibility problems can start with design decisions: controls that behave unexpectedly, focus that moves to the wrong place, or status changes that a screen reader never announces. These skills help teams plan those interactions, test them, and investigate problems that automated scans cannot settle.

The bundle covers planning, design review, testing, reporting findings, and checking fixes. Three review tools ask different questions:

- **a11y-critic** asks *is the accessibility approach sound?*
- **perspective-audit** asks *who is blocked?* (seven access-method perspectives)
- **a11y-role-audit** asks *who on the team owns this?* (six ARRM responsibility roles)

## Commands

| Command | What it does |
|---|---|
| `/a11y-workflow` | Orchestrates the whole lifecycle; spawns the specialist agents. Claude Code only |
| `/a11y-planner` | Designs the accessible implementation before code hardens the wrong pattern |
| `/a11y-critic` | Reviews a plan before implementation, and the implementation after tests pass |
| `/a11y-test` | Runs real tests — Playwright keyboard, axe-core, journey audits, component screen-reader assertions |
| `/perspective-audit` | Deep review from the access perspectives the planner or critic escalated |
| `/a11y-role-audit` | Attributes findings to the team role that owns the fix |
| `/bug-reporting` | Turns findings into reproducible issues a developer can act on without a follow-up conversation |
| `/acr-reporting` | Prepares a draft Accessibility Conformance Report (ACR) in OpenACR format from completed audit evidence, for human review and sign-off |
| `/a11y-content-judgment` | *(candidate; experimental)* Drafts content judgments for human review; exports review tasks and imports the person's decisions |

Repository-maintenance skills — `/maintain-accessibility-skills`, `/verify`, `/drupal-a11y-patch-eval` — are for working *on* this repo rather than with it. See [docs/skills.md](docs/skills.md).

## Lifecycle

```
plan → [role audit] → critique plan → [perspective audit] → revise → implement
     → test → [role audit] → critique implementation → [perspective audit] → fix → re-test
```

The critic serves at **two** checkpoints, not one: before code is written, and after tests pass. Bracketed steps run on escalation — the planner or critic flags a perspective at MEDIUM or HIGH and the audit follows. Start with `/a11y-workflow` if you want the sequence driven for you.

## Tools

Every investigation runs on the same routed stack — pinned, called, never vendored:

| | |
|---|---|
| **Playwright** `1.62.1` | Real keyboard events via CDP. The substrate everything else stands on |
| **axe-core** `4.13.0` | Machine-decidable violations, via `@axe-core/playwright` |
| **keyboard-a11y-tester** `0.5.0` | Journey audits of a live URL, with focus-indicator measurement |
| **@guidepup/virtual-screen-reader** `0.32.1` | Component announcements and reading order, pre-deploy |
| **pa11y-ci** · **eslint-plugin-jsx-a11y** · **BackstopJS** | Sitemap sweeps, static analysis, visual regression |
| **agent-browser** · **Webwright** | Interactive recon; test-script generation |
| **@openacr/openacr** `0.3.8` · **exceljs** `4.4.0` | Conformance-report draft; triage workbook |

The boundary matters more than the list. axe-core covers roughly **30–40% of WCAG issue classes** and is never keyboard or screen-reader evidence; virtual-screen-reader's interactions are synthetic, so it is never keyboard-operability evidence; every automated lane is a detector, not a verdict authority. The ICT Baseline crosswalk puts a number on the gap — of 62 federal web tests, **13 are not covered by any tool here** and have to go to manual and real-AT testing.

Full inventory, per-tool blind spots, routing table, and what was evaluated and rejected: [docs/tools.md](docs/tools.md).

## Where things live

| Path | What |
|---|---|
| `.claude/skills/` | Skill definitions — this is what `npx skills add` installs |
| `.claude/agents/` | Companion agent prompts for the workflow lane |
| `.agents/`, `.codex/` | Copies of the instructions for Codex; automated checks detect differences unless explicitly allowed |
| `docs/` | Contracts, adoption assessments, verified spec references — [index](docs/) |
| `evals/suites/` | Fixtures and rubrics, 13 suites |
| `evals/results/` | Committed raw benchmark artifacts; every published number traces to one |
| `ollama/` | Benchmark runners and scorers, local and hosted |
| `templates/` | Base protocol templates the skills build on |

## Standards

WCAG 2.2 AA is the default target. Audit-scope engagements follow **WCAG-EM 2.0**; engagements that declare Revised Section 508 additionally reference the **ICT Testing Baseline** — which sits *beside* WCAG-EM (EM structures the evaluation, the baseline defines the minimum test set), never on top of it, and never lowers the 2.2 AA target to the federal 2.0 floor.

Conformance outcomes and impact severity are orthogonal: report both, derive neither from the other. Five further orthogonal axis pairs, and the machine mechanism that makes the rule checkable, are in the [orthogonality register](docs/a11y-orthogonality-register.md).

Full detail: [docs/standards-and-contracts.md](docs/standards-and-contracts.md).

## Status

Latest release: **[v1.1.0](https://github.com/zivtech/accessibility-skills/releases/tag/v1.1.0)** (September 4, 2026). It added draft OpenACR reports, human-verification procedures for fixes, scans of URL lists, repository maintenance tools, and checks that keep benchmark answer keys out of model prompts.

The following improvements are now merged into `main`, after v1.1.0:

- **Return human content reviews without losing earlier decisions.** Export review tasks, then import a person's observations and decisions against the exact content they reviewed. Incomplete, stale, or conflicting submissions are rejected; corrections preserve the earlier decision and require an explanation. See the [export-and-return instructions](.claude/skills/a11y-content-judgment/references/content-review-return-loop.md). ([PR #71](https://github.com/zivtech/accessibility-skills/pull/71))
- **Compare federal accessibility plans with and without a supplied reference.** The Codex benchmark runner now supports the `planner-federal` condition, which supplies the toolkit's federal test-coverage reference. It keeps those results and scores separate from runs without that reference, and rejects incomplete or mismatched saved results. See the [hosted benchmark commands](ollama/README.md#codexopenai-requires-codex-cli-auth). ([PR #72](https://github.com/zivtech/accessibility-skills/pull/72))
- **Test a missing disclosure about who wrote a fix.** A new report test checks that an improved rating stays in draft when the fix's author confirms it and the second reviewer has not disclosed whether they also wrote the fix. Two valid examples guard against rejecting acceptable confirmations. These checks and the new cloud-runner tests run automatically on pull requests. See the [report test cases](evals/suites/acr-reporting/README.md). ([PR #72](https://github.com/zivtech/accessibility-skills/pull/72))

Content judgment remains a candidate and is still experimental. The return workflow still needs a pilot with real reviewers, and the [human-verification milestone](https://github.com/zivtech/accessibility-skills/issues/57) still requires a real retest, accepted fix confirmation, and review record countersigned by the report's signing author. Passing software tests does not complete that work. These two PRs add no new model-comparison results.

Claude is the supported way to run the skills in `.claude/skills/` and the specialist agents behind `/a11y-workflow`. Codex/OpenAI, Gemini, and local Ollama integrations support benchmarking. Local-model findings require further review; no tested local model has met the requirements for making final accessibility judgments.

See the [improvements record](https://github.com/zivtech/accessibility-skills/issues/40) for recent work, [open issues](https://github.com/zivtech/accessibility-skills/issues) for what remains, and [model comparisons](ollama/BENCHMARK.md) for results and their limits.

## Contributing

Read [docs/evaluation.md](docs/evaluation.md) before adding a fixture. The eval suites carry a blind protocol with machine-enforced rules about what a prompt may show a model, and a fixture that breaks them fails CI rather than quietly producing a wrong number.

Install manually if you would rather not use `npx`:

```bash
git clone https://github.com/zivtech/accessibility-skills.git
cp -r accessibility-skills/.claude/skills/* ~/.claude/skills/
cp accessibility-skills/.claude/agents/*.md ~/.claude/agents/
```

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).

`bug-reporting` derives from the MIT-licensed [ACCESSIBILITY.md](https://github.com/mgifford/ACCESSIBILITY.md) guide, contributed by @mgifford. Perspective checklists derive from CivicActions accessibility personas; role mapping follows the W3C WAI [ARRM](https://www.w3.org/WAI/planning/arrm/) framework.

> **History note (2026-08-12):** repository history was rewritten and all commit hashes changed. Re-clone, or fetch and hard-reset local branches to the new `origin/main`.
