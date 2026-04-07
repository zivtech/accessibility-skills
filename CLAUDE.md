# a11y-meta-skills

This repository contains the standalone Claude Code accessibility skill bundle — planner, critic, tester, and perspective auditor.

## Lifecycle

The critic serves at **two checkpoints** in the accessibility development lifecycle:

```
plan → critique plan → [perspective audit] → revise → implement → test → critique implementation → [perspective audit] → fix → re-test
```

| Step | Skill | Role |
|------|-------|------|
| 1. Plan | a11y-planner | Design accessibility before coding |
| 2. Critique plan | a11y-critic | Review plan for gaps before implementation |
| 2b. Perspective audit | perspective-audit | Deep review of MEDIUM/HIGH alarm perspectives (if escalated) |
| 3. Revise | manual | Address critic findings |
| 4. Implement | executor | Build according to reviewed plan |
| 5. Test | a11y-test | Automated scans + keyboard tests (Playwright) |
| 6. Critique implementation | a11y-critic | Review design decisions after tests pass |
| 6b. Perspective audit | perspective-audit | Deep review of escalated perspectives (if escalated) |
| 7. Fix | executor | Address findings |
| 8. Re-test | a11y-test | Verify fixes |

## Skills

| Skill | Type | Command |
|-------|------|---------|
| a11y-planner | planner | `/a11y-planner` |
| a11y-critic | critic | `/a11y-critic` |
| a11y-test | tester | `/a11y-test` |
| perspective-audit | auditor | `/perspective-audit` |

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
- Preserve the companion relationship between planner, critic, and perspective-audit.
- Prefer targeted edits over large rewrites.
- The critic serves at two lifecycle points — keep both documented in companion tables.

## Browser Automation Tooling

The a11y-test skill has two distinct execution modes; other a11y skills in this bundle route testing work to the same split:

- **Codified CI keyboard tests, visual regression, axe-core scans, WCAG compliance** → `npx playwright test` with `.spec.js` files. Primary path. All mandatory "real keyboard events, no synthetic events" rules apply.
- **Interactive agent-driven reconnaissance** (snapshot ARIA structure, navigate a SPA to reach a page under test, verify a single fix, capture annotated screenshots) → `agent-browser` CLI. Uses the snapshot+ref pattern (`@e1`, `@e2`) and calls CDP `Input.dispatchKeyEvent` directly, so real keyboard events are delivered. Verified on both vanilla JS (WAI-ARIA APG disclosure) and React state (react.dev DocSearch Meta+K).
- **Playwright MCP for keyboard events** → do not use. `browser_press_key` calls are silently dropped for most interactive widgets. Use `npx playwright test` or `agent-browser` instead.

See `.claude/skills/a11y-test/SKILL.md` for the full routing table and the interactive reconnaissance quickstart.

## Canonical Source

This standalone repo was extracted from `zivtech-meta-skills`. If upstream source material changes, sync intentionally rather than drifting silently.
