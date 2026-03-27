# a11y-meta-skills

This repository contains the standalone Claude Code package for the accessibility planner-critic pair.

## Skills

| Skill | Type | Command |
|-------|------|---------|
| a11y-planner | planner | `/a11y-planner` |
| a11y-critic | critic | `/a11y-critic` |

## Structure

- Root `.claude/skills/*/SKILL.md` files are the installable skill definitions.
- Root `.claude/agents/*.md` files are the companion agent prompts.
- `docs/` contains per-skill repo documentation.
- `templates/` contains the copied base protocol templates required by the skills.
- `evals/suites/` contains the bundled fixture and rubric assets.

## Working In This Repo

- Treat this as a prompt-only repository.
- Keep skill files installable from the repo root.
- Preserve the companion relationship between planner and critic.
- Prefer targeted edits over large rewrites.

## Canonical Source

This standalone repo was extracted from `zivtech-meta-skills`. If upstream source material changes, sync intentionally rather than drifting silently.
