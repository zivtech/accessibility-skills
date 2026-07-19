# a11y-critic

**a11y-critic** is a prompt-only accessibility design review skill. The tracked install files target Claude Code-compatible discovery, while the protocol and benchmarks are model-agnostic across hosted and local model families. It evaluates accessibility *design decisions* in code — not just automated test violations.

## What This Is

a11y-critic is a **prompt-only repository** that delivers accessibility design critique. The skill reviews how code implements accessibility patterns, whether state is communicated to assistive technology, whether focus management is coherent, whether semantics match intent — issues that automated testing misses.

This is different from:
- **a11y-test** (this bundle): Tests keyboard navigation with real key presses via Playwright
- **perspective-audit** (this bundle): Deep review from 7 access perspectives

All three tools catch *violations*. a11y-critic reviews *design decisions*.

## Repository Structure

```
.claude/
  skills/a11y-critic/SKILL.md       # Skill definition (adds /a11y-critic slash command)
  agents/a11y-critic.md             # Agent definition (read-only reviewer, Opus tier)
```

- **SKILL.md**: Orchestration layer — reads the target code, delegates to a11y-critic subagent with the full 11-phase review protocol embedded.
- **agents/a11y-critic.md**: Standalone agent prompt — contains the 11-phase investigation protocol (semantic audit, ARIA patterns, focus management, state communication, multi-perspective review, gap analysis, synthesis), evidence requirements, and calibration guidance. Runs with `disallowedTools: Write, Edit` (read-only).

Both files encode the same 11-phase a11y-specific review protocol.

## Key Design Decisions

- The agent is **read-only** (Write/Edit disabled) to prevent a reviewer from modifying code while critiquing it.
- The skill routes through OMC's a11y-critic agent type when available, falling back to general-purpose.
- Review scope is *design decisions*, not test results — "tests pass" ≠ "accessible design".
- Severity scale: CRITICAL (blocks access), MAJOR (significantly degrades experience), MINOR (friction), ENHANCEMENT (best practice).
- Verdict scale: REJECT / REVISE / ACCEPT-WITH-RESERVATIONS / ACCEPT.
- CRITICAL and MAJOR findings **must** include code location and evidence.
- Multi-perspective mandatory: screen reader user ≠ keyboard-only ≠ low vision ≠ cognitive.
- Calibration guidance prevents both rubber-stamping ("semantics look fine, assuming tests pass") and manufactured violations ("this ARIA attribute could theoretically be more descriptive").

## When Editing Prompts

- Preserve the exact section headings in the output format — downstream parsers depend on them.
- Keep the 11-phase investigation protocol order intact (semantic audit must precede ARIA pattern audit).
- Maintain the multi-perspective lens: screen reader, keyboard, low vision, cognitive each reveal different issues.
- The "What's Missing" section is load-bearing — it surfaces gaps in state communication, focus management design, and semantic structure.
- Realist Check (phase 7) calibrates findings to actual user impact, not theoretical violations.

## Installation Paths

Users install the Claude Code-compatible surface by copying files to their config:
- Skill: `cp -r .claude/skills/a11y-critic ~/.claude/skills/`
- Agent: `cp .claude/agents/a11y-critic.md ~/.claude/agents/`
- Or via package manager: `npx skills add zivtech/accessibility-skills`

## Companion Skills

- **a11y-planner** (this bundle): Plan accessibility improvements before implementation
- **a11y-test** (this bundle): Run keyboard + axe-core tests after critic review
- **perspective-audit** (this bundle): Deep multi-perspective review, escalated by critic when MEDIUM/HIGH alarm
- **ui-design-critic** (zivtech-design-skill): Evaluates accessibility as one perspective within broader design review

## When to Use

- Reviewing new accessible components or features
- Assessing design decisions in existing code (did we pick the right ARIA pattern?)
- Pre-merge accessibility design validation
- Analyzing accessibility failures beyond what automated tests catch
- Multi-perspective validation: same component tested by screen reader user, keyboard user, low vision user, cognitive accessibility lens

## When NOT to Use

- Running automated compliance checks — use `accessibility-testing` instead
- Keyboard testing with real key presses — use `a11y-test` instead
- Quick WCAG reference lookup — use `accessibility-standards` instead
- Making code changes — this is a read-only critic
- If you haven't read the a11y-testing results yet — read those first to understand what automated checks already validated
