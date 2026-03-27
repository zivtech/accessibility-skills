# a11y-meta-skills

Accessibility planner-critic skill pair for Claude Code.

This repository packages two companion skills:

- `a11y-planner`: plan accessible implementations before coding
- `a11y-critic`: review ARIA, focus, semantics, and state communication after implementation

## Install

```bash
npx claude-skills add https://github.com/zivtech/a11y-meta-skills
```

Both slash commands are provided by the same repo:

- `/a11y-planner`
- `/a11y-critic`

## Repository Layout

```text
.claude/
  agents/
  skills/
docs/
  a11y-planner/
  a11y-critic/
templates/
evals/
  suites/
  harness/
```

Skills and agents live at root `.claude/` for Claude Code discovery. Per-skill documentation lives under `docs/`.

## Companion Workflow

1. Use `a11y-planner` to design semantic structure, ARIA pattern choice, focus management, and testing strategy.
2. Implement the feature.
3. Use `a11y-critic` to review the result for accessibility design gaps that automated tooling can miss.
4. Run automated and manual accessibility testing.

## Evaluation Assets

This repo includes the `a11y-planner` and `a11y-critic` eval suites. The fixture and rubric assets are included here; the broader harness originated in the source monorepo.

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
