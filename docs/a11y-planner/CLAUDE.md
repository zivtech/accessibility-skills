# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

a11y-planner is a Claude Code skill and companion to a11y-critic. It is a **prompt-only repository** — no build system, no runtime code, no dependencies. The deliverables are two markdown prompt files that get installed into a user's `~/.claude/` directory.

a11y-planner designs accessible implementations BEFORE coding, so accessibility is built in from the start rather than bolted on after review. It complements a11y-critic, which reviews accessibility design decisions post-implementation.

## Repository Structure

```
.claude/
  skills/a11y-planner/SKILL.md       # Skill definition (adds /a11y-planner slash command)
  agents/a11y-planner.md             # Agent definition (planning protocol, Opus tier)
```

- **SKILL.md**: Orchestration layer — reads the feature/component to be designed, invokes the planner agent with the 9-phase accessibility planning protocol embedded in the prompt.
- **agents/a11y-planner.md**: Standalone agent prompt — contains the full 9-phase planning protocol, output format contract, calibration guidance, and examples. Runs with no tool restrictions (tools available for reading, planning, analysis).

Both files encode the same 9-phase accessibility design protocol (Scope & Context, Semantic Structure, Interaction Patterns, Focus Management, State Communication, Visual Accessibility, Content Accessibility, Testing Strategy, and Implementation Tasks) but serve different entry points.

## Key Design Decisions

- The planner is **read-write** (unlike a11y-critic which is read-only) — it creates plan documents and may write structure stubs
- The skill routes through accessible OMC agent types when available (general-purpose as fallback)
- The 9-phase protocol ensures accessibility is designed for all aspects: semantic structure, keyboard navigation, screen reader experience, visual design, and content
- Every interactive pattern MUST map to WAI-ARIA Authoring Practices Guide (APG) patterns with explicit citations
- Every ARIA attribute MUST cite the WCAG success criterion it satisfies
- Focus management MUST be planned for every overlay, modal, and dynamic content insertion
- State communication MUST cover all possible states (expanded, selected, pressed, checked, disabled, invalid, busy, loading)
- Color usage MUST have a non-color alternative documented
- No implementation code is produced — plans include HTML structure stubs and ARIA attribute lists, not JSX/implementation

## When Editing Prompts

- Preserve the exact section headings in the output format contract — downstream tools and benchmarks depend on them
- Keep the 9-phase planning protocol order intact (Scope & Context must come before Semantic Structure Plan)
- The Planning Protocol is the load-bearing part — removing phases reduces coverage of a11y design dimensions
- Calibration guidance (neither under-plan trivial components nor over-plan simple features) prevents scope creep
- Focus Management and State Communication phases are where most a11y design bugs originate — expand these sections if needed

## Installation Paths

Users install by copying files to their Claude Code config:
- Skill: `cp -r .claude/skills/a11y-planner ~/.claude/skills/`
- Agent: `cp .claude/agents/a11y-planner.md ~/.claude/agents/`
- Or via: `npx claude-skills add https://github.com/zivtech/a11y-meta-skills`

## Companion Skills

- **a11y-critic** (read-only reviewer): Reviews the implementation AFTER a11y-planner design is built. Detects incomplete ARIA patterns, missing focus management, state communication gaps
- **accessibility-testing** (testing & tooling): Runs automated axe-core, Pa11y-CI, and keyboard tests against the implemented feature
- **a11y-test** (real keyboard testing): Manual keyboard navigation testing with real Playwright key presses
- **accessibility-standards** (WCAG 2.2 AA reference): Standards enforcement, coding patterns, four-layer architecture
- **brainstorming** (idea exploration): Explore accessibility design options before committing to the planner output
- **writing-plans** (task breakdown): Convert a11y-planner output into implementation-ready tasks with exact file paths

## A11y Planning Workflow

1. **a11y-planner** (this skill): Design accessible implementation upfront. Specifies semantic structure, ARIA patterns, focus management, state communication, visual design
2. **Implementation**: Build according to the plan (using react-planner for React, other tools for other frameworks)
3. **a11y-critic**: Review the implementation. Verify design decisions were followed, detect incomplete patterns, surface design gaps
4. **accessibility-testing**: Run automated tests, keyboard navigation tests, visual regression tests
5. **Refinement**: Fix gaps found in critic review and testing

This workflow prevents the costly mistake of discovering a11y gaps after implementation when rewrites are expensive.

## Key A11y Design Principles

- **Accessibility is a design decision, not a retrofit.** The cheapest time to get it right is before the first line of code.
- **ARIA is a last resort — correct semantic HTML is always preferred.** `aria-label` on a div is almost always worse than a native `<button>`.
- **APG patterns exist for a reason — don't invent custom interaction patterns** when established ones exist (Menu Button, Disclosure, Modal Dialog, Tab Panel, etc.)
- **Focus management is the #1 source of a11y bugs in SPAs and complex UIs.** Plan it explicitly for every modal, overlay, and dynamic content change.
- **Screen reader experience ≠ visual experience.** What you see is not what they hear. Plan the experience for assistive tech users.
- **"It works with a keyboard" is not the same as "it's keyboard accessible."** Tab order, focus visibility, and expected key behaviors all matter independently.
- **Live regions are powerful but dangerous.** Too many announcements overwhelm users. Plan them carefully.
- **Testing strategy must include real assistive tech**, not just automated checks. axe-core catches ~30% of a11y issues; the rest require manual verification.

## Important

- Make files substantial and production-quality (400+ lines for SKILL.md, 300+ for agent)
- Include deep accessibility domain knowledge (WCAG 2.2, APG, ARIA spec, focus management patterns)
- Reference specific WCAG success criteria by number (e.g., "1.4.3 Contrast (Minimum)")
- Reference companion a11y-critic for review checkpoints
- Follow the same patterns as react-planner and harsh-critic
