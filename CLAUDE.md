# a11y-meta-skills

This repository contains the standalone Claude Code package for the accessibility planner-critic pair.

## Lifecycle

The critic serves at **two checkpoints** in the accessibility development lifecycle:

```
plan → critique plan → revise → implement → test → critique implementation → fix → re-test
```

| Step | Skill | Role |
|------|-------|------|
| 1. Plan | a11y-planner | Design accessibility before coding |
| 2. Critique plan | a11y-critic | Review plan for gaps before implementation |
| 3. Revise | manual | Address critic findings |
| 4. Implement | executor | Build according to reviewed plan |
| 5. Test | a11y-test | Automated scans + keyboard tests (Playwright) |
| 6. Critique implementation | a11y-critic | Review design decisions after tests pass |
| 7. Fix | executor | Address findings |
| 8. Re-test | a11y-test | Verify fixes |

## Skills

| Skill | Type | Command |
|-------|------|---------|
| a11y-planner | planner | `/a11y-planner` |
| a11y-critic | critic | `/a11y-critic` |

## Structure

- `.claude/skills/*/SKILL.md` — installable skill definitions
- `.claude/skills/*/references/external-skills-manifest.yaml` — external skill references
- `.claude/agents/*.md` — companion agent prompts
- `docs/` — per-skill documentation and external skills inventory
- `docs/EXTERNAL-SKILLS-INVENTORY.md` — landscape scan of 13 external a11y skills with adoption recommendations
- `templates/` — copied base protocol templates required by the skills
- `evals/suites/` — bundled fixture and rubric assets

## Working In This Repo

- Treat this as a prompt-only repository.
- Keep skill files installable from the repo root.
- Preserve the companion relationship between planner and critic.
- Prefer targeted edits over large rewrites.
- The critic serves at two lifecycle points — keep both documented in companion tables.

## Canonical Source

This standalone repo was extracted from `zivtech-meta-skills`. If upstream source material changes, sync intentionally rather than drifting silently.
