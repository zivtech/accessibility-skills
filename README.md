# a11y-meta-skills

Accessibility skill bundle for [Claude Code](https://claude.ai/code) — plan, test, and review.

```bash
npx skills add zivtech/a11y-meta-skills
```

**[Visual Explainer](https://zivtech.github.io/a11y-meta-skills/)**

This bundle packages three companion skills that cover the full accessibility development lifecycle:

- `a11y-planner`: designs accessible implementations before coding (WCAG 2.2, WAI-ARIA APG patterns)
- `a11y-critic`: reviews plans before implementation AND implementations after testing
- `a11y-test`: runs real Playwright keyboard tests, axe-core scans, static analysis, and visual regression

## Why this bundle exists

Most accessibility failures are not just missing attributes. They come from design decisions:

- the wrong interaction pattern chosen for the job
- focus that technically moves but makes no sense to keyboard users
- loading, error, and success states that are visible but not announced
- semantics that pass automated checks while still confusing screen readers

This repo combines three skills that cover the full lifecycle:

1. **Plan first** so semantic structure, keyboard behavior, APG pattern mapping, and testing strategy are explicit before coding.
2. **Critique the plan** so gaps (missing focus traps, incomplete state communication) are caught before any code is written.
3. **Review after testing** so passing automated checks do not hide broken accessibility design.

## What’s in the bundle

### `a11y-planner`

`a11y-planner` is the pre-implementation design surface. It produces plans for:

- semantic HTML structure and landmark strategy
- APG pattern choice for interactive components
- keyboard behavior and focus management
- state communication for assistive technology
- visual accessibility concerns like contrast, motion, and resize behavior
- testing strategy for automated and manual checks

The planner uses a 9-phase protocol:

1. Scope and context
2. Semantic structure plan
3. Interaction pattern plan
4. Focus management
5. State communication
6. Visual accessibility
7. Content accessibility
8. Testing strategy
9. Implementation tasks

### `a11y-critic`

`a11y-critic` reviews accessibility design decisions at two points: **after planning** (to catch gaps before code is written) and **after testing** (to verify the implementation). It looks for:

- semantic mismatches between UI intent and HTML structure
- incomplete or incorrect ARIA pattern implementations
- broken focus traps, restoration, or tab order
- missing live regions or state announcements
- low-vision and cognitive accessibility friction
- gaps that pass axe-core but still fail real users

The critic uses an 8-phase review protocol with evidence-backed severity and a mandatory multi-perspective pass:

- screen reader user
- keyboard-only user
- low-vision user
- cognitive accessibility lens

### `a11y-test`

`a11y-test` is the measurement layer. It runs real tests and produces evidence that feeds into the critic's review:

- Playwright keyboard interaction tests (Tab, Enter, Escape, arrow keys — real key presses, not attribute checks)
- axe-core scanning via Playwright injection for automated WCAG violation detection
- eslint-plugin-jsx-a11y static analysis for React/Vue/JSX projects
- Visual regression testing with Playwright screenshots and optional BackstopJS
- WCAG 2.2 compliance checks including new criteria (2.4.11, 2.4.13, 2.5.7, 2.5.8, 3.3.7, 3.3.8)
- Dynamic test prioritization based on automated scan findings

## Lifecycle

```
plan → critique plan → revise → implement → test → critique implementation → fix → re-test
```

1. Run `/a11y-planner` to design the feature before implementation.
2. Run `/a11y-critic` on the plan to catch gaps before coding.
3. Revise the plan based on critic findings.
4. Build the feature.
5. Run `a11y-test` (Playwright keyboard tests, axe-core scans, visual regression).
6. Run `/a11y-critic` on the implementation after tests pass.
7. Fix findings, re-test.

## Commands

- `/a11y-planner` — design accessibility before coding
- `/a11y-critic` — review plans or implementations
- `/a11y-test` — run keyboard, axe-core, and visual regression tests

## Install

```bash
npx skills add zivtech/a11y-meta-skills
```

Manual install:

```bash
git clone https://github.com/zivtech/a11y-meta-skills.git
cp -r a11y-meta-skills/.claude/skills/* ~/.claude/skills/
cp a11y-meta-skills/.claude/agents/*.md ~/.claude/agents/
```

## Repository Layout

```text
.claude/
  agents/                              # Standalone agent prompts
  skills/
    a11y-critic/
      SKILL.md                         # Skill definition
      references/
        external-skills-manifest.yaml  # External skill references
    a11y-planner/
      SKILL.md
      references/
        external-skills-manifest.yaml
docs/
  EXTERNAL-SKILLS-INVENTORY.md         # Landscape scan of 13 external a11y skills
  a11y-planner/
  a11y-critic/
templates/
evals/
  suites/
  harness/
```

Skills and agents live at root `.claude/` for Claude Code discovery. Per-skill documentation lives under `docs/`.

## Evaluation Assets

This repo includes the `a11y-planner` and `a11y-critic` eval suites. The fixture and rubric assets are included here; the broader harness originated in the source monorepo.

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
