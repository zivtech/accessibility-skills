# Codex skill mirrors

These are Codex-compatible mirrors of `.claude/skills/`. The `.claude/`
surface is the source of truth; edit there first, then sync here.

Intentional divergences (everything else must match):
- frontmatter `compatibility:` line (Codex vs Claude Code)
- path prefixes in body text (`.agents/skills/...` vs `.claude/skills/...`)
- Webwright lane notes: script GENERATION is Claude Code-only; Codex runs the
  generated `.py` scripts.

Intentionally absent from this surface:
- `a11y-workflow` — it orchestrates Claude Code subagent spawning, which has
  no Codex equivalent. On Codex, run the four skills individually in lifecycle
  order: planner → critic → test → perspective-audit (on escalation).
- `drupal-a11y-patch-eval` — Claude Code only; orchestrates subagents, DDEV,
  and local worktrees.

Drift is checked by `scripts/check_mirrors.py --strict` in CI (heading-set
comparison + broken-path scan). If you add a heading to a `.claude` skill,
sync the mirror in the same commit or CI fails.
