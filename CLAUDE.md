# a11y-meta-skills

This repository contains the standalone a11y-meta-skills accessibility bundle — planner, critic, tester, and perspective auditor — plus cross-model benchmark assets. Claude Code is one supported install/runtime surface; the evals and runners now compare Claude, Codex/OpenAI, local Ollama models, and other hosted model families as peer baselines.

## Dead Output

**What dead looks like in this repo:**
- Accessibility reviews that pattern-match ARIA attributes without testing whether the interaction actually works for the user. A finding that says "missing aria-label" without explaining what a screen reader user would experience is dead.
- Plans that cite WCAG success criteria by number without engaging with the actual user experience they protect. "Violates 4.1.2" is a citation, not a finding.
- Findings rated CRITICAL because the checklist says so, not because a real user would be blocked. Severity must reflect impact on people, not rule weight.
- Eval fixtures that test whether the skill finds the planted bug without testing whether it avoids false alarms on clean code. A critic that flags everything is dead — it just looks thorough.

Three rules:
- **Name it when you see it.** If a review, plan, or finding is dead — checking boxes rather than thinking about the person who'll interact with the UI — say so.
- **Friction is the job.** If the planner's recommendations don't fit the component's actual interaction pattern, push back. If a critique applies a pattern from the APG that doesn't match the use case, say so.
- **Watch for rank erosion.** Accessibility guidance that gets summarized into checklists loses the "why." If the output could be produced by a linter, it's not earning its place as a skill.

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
| a11y-workflow | orchestrator | `/a11y-workflow` |
| a11y-planner | planner | `/a11y-planner` |
| a11y-critic | critic | `/a11y-critic` |
| a11y-test | tester | `/a11y-test` |
| perspective-audit | auditor | `/perspective-audit` |

## Team Workflow

The `/a11y-workflow` skill orchestrates the full lifecycle by spawning specialist agents from the main session (depth-1, no nested delegation).

**Quick start:**
```
/a11y-workflow full src/components/Modal.tsx    # full lifecycle
/a11y-workflow step scout src/components/Modal.tsx  # single step
```

**Model routing** (validated on 8 hard fixtures, 2026-05-19):
- Scout: Haiku (recon only)
- Planner/Critic/Auditor: Opus (judgment-heavy — best-tier verdicts on ADVERSARIAL fixtures)
- Orchestrator: main session (sequencing, not judgment)

**Agents:**
- `a11y-scout` — Haiku, read-only. File discovery and ARIA inventory.
- `a11y-planner` — Opus, no Bash. 9-phase accessibility design.
- `a11y-critic` — Opus, read-only. 8-phase investigation protocol.
- `perspective-audit` — Opus, read-only. 7-perspective deep review (escalation only).

See `.claude/teams/a11y-workflow.md` for full team definition and escalation signals.

## Structure

- `.claude/skills/*/SKILL.md` — installable skill definitions
- `.claude/skills/*/references/external-skills-manifest.yaml` — external skill references
- `.claude/agents/*.md` — companion agent prompts
- `.agents/skills/*/SKILL.md` — Codex-compatible skill mirrors
- `.codex/agents/*.toml` — Codex agent definitions for planner/critic
- `docs/` — per-skill documentation and external skills inventory
- `docs/EXTERNAL-SKILLS-INVENTORY.md` — landscape scan of 13 external a11y skills with adoption recommendations
- `templates/` — copied base protocol templates required by the skills
- `evals/suites/` — bundled fixture and rubric assets
- `ollama/` — local model portability layer (see below)

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
- **Test script generation from prose specs** → `/webwright:run` or `/webwright:craft` (Claude Code plugin). LLM generates complete Python Playwright scripts from natural language descriptions. Benchmarked 25/25 on WAI-ARIA APG examples (dialog focus trap, tabs, axe-core injection, menu navigation, ARIA tree inspection). Uses real `page.keyboard.press()` calls (CDP-backed). Claude Code only — not available in Codex CLI; generated `.py` files can be executed from Codex via `python3 script.py`. Do not run simultaneously with agent-browser (port conflicts).

See `.claude/skills/a11y-test/SKILL.md` for the full routing table, decision flowchart, and the interactive reconnaissance quickstart.

## Local Model Portability (Ollama)

The analysis-only skills (critic, planner, perspective-audit) run locally via Ollama with no cloud API. The `ollama/` directory contains the wrapper, benchmark tooling, and full results.

**Recommended model**: `qwen3:32b` (18.8 GB) — 96% must-find detection across 33 critic fixtures, 0% false positives, 100% perspective-audit must-find across 25 fixtures, perfect planner scores.

```bash
python3 ollama/ollama_a11y.py critic path/to/component.jsx --model qwen3:32b
python3 ollama/ollama_a11y.py planner path/to/requirements.md --model qwen3:32b
python3 ollama/ollama_a11y.py perspective path/to/component.jsx --model qwen3:32b
```

Benchmarked against the 33 critic fixtures and 25 perspective-audit fixtures in full, plus 2 of the 25 planner fixtures (planner coverage is a known gap — see EVAL-GAPS-PLAN.md), with cross-platform baselines for Claude API, Codex/OpenAI, and local Ollama models. Treat Gemini and other hosted providers as first-class baseline families when their raw result artifacts are present. See `ollama/BENCHMARK.md` for full results and `ollama/README.md` for usage.

a11y-test is NOT portable — it requires Playwright, axe-core, and browser automation. Only reference knowledge ports.

## Canonical Source

This standalone repo was extracted from `zivtech-meta-skills`. If upstream source material changes, sync intentionally rather than drifting silently.
