<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-03-08 | Updated: 2026-03-08 -->

# a11y-planner

## Purpose
Accessibility implementation planner skill for Claude Code and companion to a11y-critic. Designs accessible implementations BEFORE coding so accessibility is built in from the start rather than bolted on after review. Uses a 9-phase planning protocol covering semantic structure, interaction patterns (mapped to WAI-ARIA APG), focus management, state communication, visual accessibility, content accessibility, and testing strategy.

## Key Files

| File | Description |
|------|-------------|
| `CLAUDE.md` | Repository documentation: what this is, 9-phase protocol overview, key design decisions, a11y design principles, installation, companion skills, planning workflow |
| `.claude/skills/a11y-planner/SKILL.md` | Skill definition -- orchestration layer that reads the feature/component scope and invokes the planner agent with the 9-phase protocol embedded |
| `.claude/agents/a11y-planner.md` | Agent definition -- standalone agent prompt with full 9-phase protocol, output format contract, calibration guidance, examples. Has full tool access (unlike the read-only critic) |

## For AI Agents

### Working In This Directory

- This is a **prompt-only** skill package. No build system, no runtime code, no dependencies.
- The planner is **read-write** (unlike a11y-critic which is read-only) -- it creates plan documents and may write structure stubs.
- Both SKILL.md and the agent file encode the same 9-phase protocol. Keep them in sync when editing.
- Preserve exact section headings in the output format contract -- downstream tools and benchmarks depend on them.
- Every interactive pattern MUST map to a WAI-ARIA Authoring Practices Guide (APG) pattern with explicit citations.
- Every ARIA attribute MUST cite the WCAG success criterion it satisfies.
- No implementation code is produced -- plans include HTML structure stubs and ARIA attribute lists, not JSX/implementation.

### The 9-Phase Protocol

1. Scope & Context
2. Semantic Structure Plan
3. Interaction Patterns (mapped to APG)
4. Focus Management Design
5. State Communication Strategy
6. Visual Accessibility
7. Content Accessibility
8. Testing Strategy
9. Implementation Tasks

### Key Design Principles Encoded

- Accessibility is a design decision, not a retrofit
- ARIA is a last resort -- correct semantic HTML is always preferred
- APG patterns exist for a reason -- do not invent custom interaction patterns
- Focus management is the #1 source of a11y bugs in SPAs and complex UIs
- Screen reader experience does not equal visual experience
- Live regions are powerful but dangerous -- plan them carefully
- Testing strategy must include real assistive tech, not just automated checks

### Testing Requirements

- Test by running the planner against component designs and verifying the output covers all 9 phases
- Verify APG pattern citations are correct
- Verify WCAG success criterion references are accurate
- Focus Management and State Communication phases are where most a11y design bugs originate -- verify these are thorough

## Dependencies

### Internal
- Companion: **a11y-critic** (reviews implementations after the a11y-planner design is built)

### External
- **accessibility-testing** (zivtech-claude-skills): Run automated axe-core, Pa11y-CI, and keyboard tests against the implemented feature
- **a11y-test** (zivtech-claude-skills): Manual keyboard navigation testing with real Playwright key presses
- **accessibility-standards** (zivtech-claude-skills): WCAG 2.2 AA reference patterns
- **brainstorming** (obra/superpowers): Explore accessibility design options before committing to the planner output
- **writing-plans** (obra/superpowers): Convert a11y-planner output into implementation-ready tasks with exact file paths

<!-- MANUAL: -->
