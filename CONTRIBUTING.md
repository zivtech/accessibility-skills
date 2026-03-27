# Contributing

## Scope

This is a prompt-only repository. Changes usually affect markdown prompt files, skill definitions, templates, or eval assets.

## Expectations

- Keep root `.claude/skills/` and `.claude/agents/` installable.
- Maintain the planner-critic companion loop.
- Preserve exact load-bearing headings in output contracts.
- Keep copied templates in sync intentionally, not accidentally.

## Verification

Before shipping changes:

1. Verify both skill files and both agent files exist under root `.claude/`.
2. Check install instructions reference `https://github.com/zivtech/a11y-meta-skills`.
3. Check no stale `(future)` wording remains for the companion relationship.
4. Confirm eval suite directories are still present.
