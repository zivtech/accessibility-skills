# a11y-meta-skills

Accessibility planner-critic skill bundle for [Claude Code](https://claude.ai/code).

```bash
npx skills add zivtech/a11y-meta-skills
```

**[Visual Explainer](https://zivtech.github.io/a11y-meta-skills/)**

This bundle packages two companion skills that work at different points in the development lifecycle:

- `a11y-planner`: designs accessible implementations before coding (WCAG 2.2, WAI-ARIA APG patterns)
- `a11y-critic`: reviews plans before implementation AND implementations after testing

## Why this bundle exists

Most accessibility failures are not just missing attributes. They come from design decisions:

- the wrong interaction pattern chosen for the job
- focus that technically moves but makes no sense to keyboard users
- loading, error, and success states that are visible but not announced
- semantics that pass automated checks while still confusing screen readers

This repo combines the two surfaces needed to catch that work at the right times:

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

`a11y-critic` is the post-implementation review surface. It is for accessibility design critique, not just rule checking. It looks for:

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

## Workflow

1. Run `/a11y-planner` to design the feature before implementation.
2. Build the feature.
3. Run `/a11y-critic` on the implementation.
4. Run automated and manual accessibility testing.
5. Refine based on critic findings and test evidence.

## Commands

- `/a11y-planner`
- `/a11y-critic`

## Install

```bash
npx claude-skills add https://github.com/zivtech/a11y-meta-skills
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
  agents/
  skills/
docs/
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
