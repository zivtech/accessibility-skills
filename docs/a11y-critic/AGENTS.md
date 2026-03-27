<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-03-08 | Updated: 2026-03-08 -->

# a11y-critic

## Purpose
Accessibility design reviewer skill for Claude Code. Evaluates accessibility *design decisions* in code -- not automated test violations, but whether ARIA patterns are complete, focus management is coherent, state is communicated to assistive technology, and semantic structure matches intent. Uses an 8-phase investigation protocol with multi-perspective review (screen reader, keyboard, low vision, cognitive).

## Key Files

| File | Description |
|------|-------------|
| `CLAUDE.md` | Repository documentation: what this is, key design decisions, when to edit prompts, installation paths, companion skills |
| `.claude/skills/a11y-critic/SKILL.md` | Skill definition -- orchestration layer that reads target code and delegates to the a11y-critic subagent with the full 8-phase protocol embedded |
| `.claude/agents/a11y-critic.md` | Agent definition -- standalone agent prompt with 8-phase investigation protocol, evidence requirements, calibration guidance. Runs with `disallowedTools: Write, Edit` (read-only) |

## For AI Agents

### Working In This Directory

- This is a **prompt-only** skill package. There is no build system, no tests to run, no dependencies to install.
- The skill is **read-only** -- the agent has Write/Edit disabled to prevent a reviewer from modifying code while critiquing it.
- Both SKILL.md and the agent file encode the same 8-phase protocol. If you change one, you must keep the other in sync.
- Preserve exact section headings in output format -- downstream parsers depend on them.
- The 8-phase investigation protocol order is fixed: semantic audit must precede ARIA pattern audit.

### The 8-Phase Protocol

1. Pre-commitment predictions
2. Semantic HTML Audit
3. ARIA Pattern Review
4. Focus Management
5. State Communication
6. Multi-Perspective Review (screen reader, keyboard, low vision, cognitive)
7. Gap Analysis ("What's Missing")
8. Synthesis (verdict with Realist Check calibration)

### Key Differentiator

Automated testing tools (axe-core, Pa11y) catch *violations*. This critic catches *design mistakes that automated tests miss*: incomplete ARIA patterns, focus management that works but confuses users, states communicated visually but not programmatically, wrong ARIA pattern selection.

### Severity and Verdict Scales

- Severity: CRITICAL (blocks access) > MAJOR (significantly degrades) > MINOR (friction) > ENHANCEMENT (best practice)
- Verdict: REJECT / REVISE / ACCEPT-WITH-RESERVATIONS / ACCEPT
- CRITICAL and MAJOR findings MUST include code location and evidence

### Testing Requirements

- Test by running the skill against components with known accessibility issues
- Verify the critic identifies real design gaps without manufacturing false positives
- Multi-perspective review must cover all four lenses (screen reader, keyboard, low vision, cognitive)

## Dependencies

### Internal
- Companion: **a11y-planner** (designs accessible implementations before coding)

### External
- **accessibility-testing** (zivtech-claude-skills): Run automated checks after critic review
- **a11y-test** (zivtech-claude-skills): Keyboard navigation testing with real key presses
- **accessibility-standards** (zivtech-claude-skills): WCAG 2.2 AA reference patterns
- **ui-design-critic** (zivtech-design-skill): Broader design review that includes accessibility as one perspective

<!-- MANUAL: -->
