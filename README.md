# Accessibility Skills: AI accessibility testing and WCAG 2.2 audits for Claude Code

**Accessibility Skills** is an open-source set of AI agent skills that help Claude Code plan, test, review, and audit web accessibility. It targets **WCAG 2.2 AA** by default and supports **Revised Section 508** engagements. It pairs real browser tests (Playwright keyboard testing, axe-core scans, screen reader assertions) with expert-style design reviews. It turns the results into developer-ready bug reports and draft Accessibility Conformance Reports (ACRs, the reports a VPAT produces).

```bash
npx skills add zivtech/accessibility-skills
```

**[Visual explainer](https://zivtech.github.io/accessibility-skills/)** · **[Documentation](docs/)** · **[Skills reference](docs/skills.md)** · **[Model benchmarks](ollama/BENCHMARK.md)** · **[Latest release](https://github.com/zivtech/accessibility-skills/releases/latest)**

## Why use it

Automated checkers like axe-core find roughly 30–40% of WCAG issue types. The rest come from design decisions: a custom dropdown that traps keyboard focus, a modal that loses the user's place, a status message a screen reader never announces. These skills cover that gap. They plan accessible interactions before code is written, test them with real keyboard events, and review them from the point of view of the people who use them.

They are built for:

- **Front-end developers** building accessible components (menus, dialogs, tabs, forms, comboboxes) with WAI-ARIA Authoring Practices (APG) patterns
- **Accessibility specialists and QA testers** running WCAG 2.2 audits and keyboard and screen reader testing
- **Teams preparing Section 508 or procurement documentation** who need an evidence-backed draft ACR
- **Design and product teams** who want accessibility problems caught at the plan stage, not after launch

## What you can ask it

```text
/a11y-planner   Plan an accessible autocomplete search with keyboard support and live results
/a11y-critic    Review src/components/Modal.tsx for focus management and ARIA problems
/a11y-test      Run axe-core and keyboard tests against http://localhost:3000/checkout
/a11y-workflow  full src/components/Tabs.tsx
/bug-reporting  Turn these axe-core results into issues a developer can reproduce
```

## Skills

| Command | What it does |
|---|---|
| `/a11y-workflow` | Runs the whole accessibility lifecycle and hands each step to a specialist agent. Claude Code only |
| `/a11y-planner` | Designs the accessible implementation (semantics, APG pattern, keyboard and focus behavior, state announcements) before code is written |
| `/a11y-critic` | Reviews a plan before implementation, and the implementation after tests pass, for WCAG 2.2 and ARIA design problems automated tools miss |
| `/a11y-test` | Runs real tests: Playwright keyboard tests, axe-core scans, URL-list scans, user-journey audits, component screen reader assertions |
| `/perspective-audit` | Reviews from seven access perspectives, including screen reader, keyboard-only, low vision, and cognitive |
| `/a11y-role-audit` | Assigns each finding to the team role that owns the fix (designer, developer, content author, and others), using the W3C ARRM framework |
| `/bug-reporting` | Turns findings into reproducible accessibility bug reports with URL, selector, HTML snippet, WCAG success criterion, and severity |
| `/acr-reporting` | Drafts an Accessibility Conformance Report in OpenACR format from completed audit evidence, for human review and sign-off |
| `/a11y-content-judgment` | *(experimental)* Drafts judgments on page titles, headings, link text, and alt text for a person to review and approve |

The three review skills ask different questions. **a11y-critic** asks *is the accessibility approach sound?* **perspective-audit** asks *who is blocked?* **a11y-role-audit** asks *who on the team owns this?*

Three more skills (`/maintain-accessibility-skills`, `/verify`, `/drupal-a11y-patch-eval`) are for working on this repository rather than with it. See [docs/skills.md](docs/skills.md).

## How the skills fit together

```
plan → [role audit] → critique plan → [perspective audit] → revise → implement
     → test → [role audit] → critique implementation → [perspective audit] → fix → re-test
```

The critic runs at two checkpoints: before code is written, and after tests pass. Bracketed steps run when the planner or critic flags a perspective as MEDIUM or HIGH risk. Start with `/a11y-workflow` if you want the whole sequence run for you.

## Testing tools

The skills call these tools at pinned versions. None of them are bundled into this repository.

| Tool | Used for |
|---|---|
| **Playwright** `1.62.1` | Real keyboard events through the Chrome DevTools Protocol. Everything else builds on it |
| **axe-core** `4.13.0` | Automated WCAG violation scanning, via `@axe-core/playwright` |
| **keyboard-a11y-tester** `0.5.0` | Keyboard and screen reader journey audits of a live URL, including focus indicator measurement |
| **@guidepup/virtual-screen-reader** `0.32.1` | Screen reader announcements and reading order in component tests (Vitest, Jest, Storybook) |
| **pa11y-ci** · **eslint-plugin-jsx-a11y** · **BackstopJS** | Sitemap-wide scans, static analysis, visual regression |
| **agent-browser** · **Webwright** | Interactive browser checks; test generation from plain-language descriptions |
| **@openacr/openacr** `0.3.8` · **exceljs** `4.4.0` | Draft ACRs; issue triage spreadsheets |

Automated results are treated as leads, not verdicts. axe-core results never count as keyboard or screen reader evidence. The virtual screen reader simulates interactions, so it never counts as proof that something works with a keyboard. Of the 62 federal ICT Testing Baseline web tests, 13 are not covered by any tool here and need manual testing with real assistive technology.

Per-tool blind spots, the routing table, and tools that were evaluated and rejected: [docs/tools.md](docs/tools.md).

## Standards

- **WCAG 2.2 Level AA** is the default target.
- **Site and product audits** follow **WCAG-EM 2.0**, the W3C method for choosing a sample and evaluating it.
- **Revised Section 508** engagements also use the federal **ICT Testing Baseline** as the minimum test set. The target stays at WCAG 2.2 AA and is never lowered to the Section 508 WCAG 2.0 floor.
- **Conformance and severity are separate.** Every finding reports whether it fails a success criterion and how badly it affects people, and neither is derived from the other. See the [orthogonality register](docs/a11y-orthogonality-register.md).

Full detail: [docs/standards-and-contracts.md](docs/standards-and-contracts.md).

## FAQ

**Can AI replace manual accessibility testing?**
No. The skills make testing faster and more thorough, but they never produce a final conformance judgment on their own. Draft ACRs and content judgments stay drafts until a named person signs off, and the gaps that need real assistive technology testing are listed rather than hidden.

**Does it work with Codex, Gemini, or local models?**
Claude Code is the supported way to run the skills and the `/a11y-workflow` agents. Codex-format copies are in `.agents/skills/`, and the analysis skills (planner, critic, perspective audit) can run on local models through [Ollama](ollama/README.md). Local models are treated as detectors that need review. None tested so far is reliable enough to make final accessibility judgments. Cross-model results are in [ollama/BENCHMARK.md](ollama/BENCHMARK.md).

**Will it make my site WCAG or ADA compliant?**
It finds, explains, and helps fix accessibility barriers, and produces evidence for an audit. Compliance is a legal and organizational determination it does not make.

**Can it generate a VPAT?**
It drafts an Accessibility Conformance Report in the open [OpenACR](https://github.com/GSA/openacr) format from a completed audit, ready for review in GSA's ACR Editor. The draft never marks an untested criterion as passing, and a person must review and sign it.

## Status

Latest release: **[v1.2.0](https://github.com/zivtech/accessibility-skills/releases/tag/v1.2.0)** (September 14, 2026). It added cross-checking between scanners, optional WebAIM WAVE and Siteimprove Alfa scans, and one-pass-per-page audits as the default.

`/a11y-content-judgment` is still experimental and needs a pilot with real reviewers. The [human verification milestone](https://github.com/zivtech/accessibility-skills/issues/57) is waiting on a real retest from a client engagement.

See the [release notes](https://github.com/zivtech/accessibility-skills/releases), the [improvements record](https://github.com/zivtech/accessibility-skills/issues/40), and [open issues](https://github.com/zivtech/accessibility-skills/issues).

## Where things live

| Path | What |
|---|---|
| `.claude/skills/` | Skill definitions. This is what `npx skills add` installs |
| `.claude/agents/` | Agent prompts used by `/a11y-workflow` |
| `.agents/`, `.codex/` | Codex-format copies; CI checks that they match |
| `docs/` | Contracts, tool assessments, and standards references ([index](docs/)) |
| `evals/suites/` | Test fixtures and scoring rubrics, 13 suites |
| `evals/results/` | Raw benchmark results; every published number traces back to one |
| `ollama/` | Benchmark runners and scorers for local and hosted models |
| `templates/` | Base templates the skills build on |

## Manual install

```bash
git clone https://github.com/zivtech/accessibility-skills.git
cp -r accessibility-skills/.claude/skills/* ~/.claude/skills/
cp accessibility-skills/.claude/agents/*.md ~/.claude/agents/
```

## Contributing

Read [docs/evaluation.md](docs/evaluation.md) before adding a test fixture. The evaluation suites follow a blind protocol that controls what a prompt may show a model, and CI fails any fixture that breaks it.

## License and credits

GPL-3.0-or-later. See [LICENSE](LICENSE).

`bug-reporting` is based on the MIT-licensed [ACCESSIBILITY.md](https://github.com/mgifford/ACCESSIBILITY.md) guide by @mgifford. The perspective checklists are based on CivicActions accessibility personas. Role mapping follows the W3C WAI [Accessibility Roles and Responsibilities Mapping (ARRM)](https://www.w3.org/WAI/planning/arrm/) framework. Built by [Zivtech](https://www.zivtech.com).

> **History note (2026-08-12):** repository history was rewritten and all commit hashes changed. Re-clone, or fetch and hard-reset local branches to the new `origin/main`.
