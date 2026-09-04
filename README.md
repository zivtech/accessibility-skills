# Accessibility Skills

Skills and evaluation assets for planning, testing, reviewing, and auditing web accessibility — WCAG 2.2 AA by default, Revised Section 508 when an engagement declares it.

```bash
npx skills add zivtech/accessibility-skills
```

**[Visual explainer](https://zivtech.github.io/accessibility-skills/)** · **[Documentation index](docs/)** · **[Benchmarks](ollama/BENCHMARK.md)**

## What it does

Most accessibility failures are not missing attributes. They come from design decisions: the wrong interaction pattern for the job, focus that moves but makes no sense, states that are visible but never announced, semantics that pass axe-core and still confuse a screen reader. Linters do not catch those. These skills are built to.

The bundle covers the lifecycle — design it, review the design, measure it, review what you measured, file what you found, and report it — plus two orthogonal audit lenses:

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
| `/acr-reporting` | Serializes a finished audit into a draft OpenACR conformance report for human sign-off |
| `/a11y-content-judgment` | *(candidate)* Drafts per-row judgments on the criteria a scanner cannot decide; a named human ratifies |

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
| `.agents/`, `.codex/` | Codex-compatible mirrors, kept byte-identical by CI |
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

Current release: **[v1.0.0](https://github.com/zivtech/accessibility-skills/releases)** (2026-08-12). The supported runtime is Claude — the skills in `.claude/skills/` and the subagent lane behind `/a11y-workflow`.

Everything else ships as benchmark infrastructure, not a supported runtime. In particular the local Ollama lane is what its own results say it is: a **detector, never a verdict authority**. No local model has passed the verdict-authority bar at any size tested. Open work is tracked in [issues](https://github.com/zivtech/accessibility-skills/issues).

Model comparisons across Claude, Codex/OpenAI, Gemini and local Ollama families — with the caveats that make each number readable — are in [ollama/BENCHMARK.md](ollama/BENCHMARK.md).

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
