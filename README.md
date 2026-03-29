# a11y-meta-skills

Accessibility skill bundle for [Claude Code](https://claude.ai/code) — plan, test, review, and audit from real perspectives.

```bash
npx skills add zivtech/a11y-meta-skills
```

**[Visual Explainer](https://zivtech.github.io/a11y-meta-skills/)**

This bundle packages four companion skills that cover the full accessibility development lifecycle:

- `a11y-planner`: designs accessible implementations before coding (WCAG 2.2, WAI-ARIA APG patterns)
- `a11y-critic`: reviews plans before implementation AND implementations after testing
- `a11y-test`: runs real Playwright keyboard tests, axe-core scans, static analysis, and visual regression
- `perspective-audit`: deep review from 7 disability and situational access perspectives, escalated by the planner or critic when specific perspectives reach MEDIUM or HIGH alarm levels

## Why this bundle exists

Most accessibility failures are not just missing attributes. They come from design decisions:

- the wrong interaction pattern chosen for the job
- focus that technically moves but makes no sense to keyboard users
- loading, error, and success states that are visible but not announced
- semantics that pass automated checks while still confusing screen readers

This repo combines four skills that cover the full lifecycle:

1. **Plan first** so semantic structure, keyboard behavior, APG pattern mapping, and testing strategy are explicit before coding.
2. **Critique the plan** so gaps (missing focus traps, incomplete state communication) are caught before any code is written.
3. **Review after testing** so passing automated checks do not hide broken accessibility design.
4. **Audit from real perspectives** so the planner and critic can escalate specific disability or situational access concerns for deep review by perspective agents grounded in CivicActions personas and the W3C WAI ARRM framework.

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

### `perspective-audit`

`perspective-audit` provides deep accessibility review from 7 disability and situational access perspectives. It is activated by escalation — when the planner or critic flags one or more perspectives at MEDIUM or HIGH alarm level, those perspectives get a focused deep review.

The 7 perspectives:

- **Magnification & Reflow** — zoom users, reflow at 320px, touch target sizing
- **Environmental Contrast** — outdoor use, low-light, color vision deficiency
- **Vestibular & Motion** — motion sensitivity, parallax, auto-playing animation
- **Auditory Access** — deaf/hard-of-hearing, captions, visual alternatives to audio
- **Keyboard & Motor** — switch users, voice control, limited dexterity, one-handed use
- **Screen Reader & Semantic** — NVDA/JAWS/VoiceOver users, semantic structure, live regions
- **Cognitive & Neurodivergent** — reading level, information density, consistent navigation

Each perspective uses a Jobs-to-be-Done checklist derived from CivicActions accessibility personas with ARRM role-responsibility mapping for team assignment.

## Lifecycle

```
plan → critique plan → [perspective audit] → revise → implement → test → critique implementation → [perspective audit] → fix → re-test
```

1. Run `/a11y-planner` to design the feature before implementation.
2. Run `/a11y-critic` on the plan to catch gaps before coding.
3. If the critic escalates perspectives at MEDIUM/HIGH, run `/perspective-audit` for deep review.
4. Revise the plan based on critic and audit findings.
5. Build the feature.
6. Run `/a11y-test` (Playwright keyboard tests, axe-core scans, visual regression).
7. Run `/a11y-critic` on the implementation after tests pass.
8. If the critic escalates perspectives, run `/perspective-audit` again.
9. Fix findings, re-test.

## Commands

- `/a11y-planner` — design accessibility before coding
- `/a11y-critic` — review plans or implementations
- `/a11y-test` — run keyboard, axe-core, and visual regression tests
- `/perspective-audit` — deep review from escalated disability/situational access perspectives

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
    a11y-test/
      SKILL.md
    perspective-audit/
      SKILL.md                         # Escalation-based perspective auditor
      references/
        perspectives.md                # 7 JTBD checklists (CivicActions personas)
        arrm-perspective-mapping.md    # W3C WAI ARRM role routing
docs/
  EXTERNAL-SKILLS-INVENTORY.md         # Landscape scan of 13 external a11y skills
  PERSPECTIVE-AGENTS-PLAN.md           # Architecture plan (v2.1, 3-critic reviewed)
  a11y-planner/
  a11y-critic/
templates/
evals/
  suites/
  harness/
```

Skills and agents live at root `.claude/` for Claude Code discovery. Per-skill documentation lives under `docs/`.

## Testing & Contributing

### Evaluation suite

The `evals/suites/perspectives/` directory contains a 30-fixture evaluation suite (25 main + 5 calibration) that validates the perspective-audit skill and the perspective enhancements to the planner, critic, and tester.

Fixture categories:
- **HAS-BUGS (new dimension)** — 10 fixtures with planted bugs in auditory, vestibular, cognitive, contrast, and magnification dimensions
- **HAS-BUGS (existing dimension)** — 6 regression fixtures with keyboard/screen reader bugs all conditions should catch
- **CLEAN** — 5 fixtures with zero real bugs, measuring false positive rate
- **ADVERSARIAL** — 4 fixtures that pass automated tools but have subtle perspective-specific issues

Each fixture has 3 files:
- `fixtures/{id}.md` — Component code, expected behavior, planted bugs
- `fixtures/{id}.metadata.yaml` — Ground truth: expected findings, alarm levels, false positive traps
- `rubrics/{id}.rubric.yaml` — Scoring dimensions, expected performance per condition, thresholds

### Running evaluations

Generate stripped fixtures (removes `// BUG:` hint comments for blind review):

```bash
cd evals/suites/perspectives
python3 strip_bug_comments.py
# Creates fixtures-eval/ with clean versions
```

The eval harness runs fixtures under 3 conditions:
- **A** — Standard a11y-critic (Sonnet, no perspectives)
- **B** — Standard a11y-critic + "also review for auditory, vestibular, cognitive, and contrast" (Sonnet)
- **C** — Enhanced a11y-critic + perspective-audit (Opus, with alarm levels)

### Baselines to maintain

Any change to the skills must preserve these baselines:

| Baseline | Current | Minimum | How to test |
|----------|---------|---------|-------------|
| **Calibration alarm accuracy** | 35/35 (100%) | 28/35 (80%) | Run 5 calibration fixtures under condition C, score alarm levels against `calibration/*.metadata.yaml` expected levels |
| **CLEAN false positive rate** | 0% | 0% | Run 5 CLEAN fixtures under condition C, count MAJOR/CRITICAL findings (must be 0) |
| **Regression non-inferiority** | C = A (6/6) | C ≥ A - 5% | Run 6 regression fixtures under A and C, compare existing-dimension true positive rate |

Scoring for alarm levels: exact match = 1.0, within +/-1 level = 0.5, off by 2 levels = 0.0.

### Adding new fixtures

1. Create 3 files using the naming convention `{kebab-case-id}.md`, `.metadata.yaml`, `.rubric.yaml`
2. Or add the spec to `generate_fixtures.py` and run it to generate metadata + rubric
3. Use snake_case for perspective keys in metadata: `magnification_reflow`, `environmental_contrast`, `vestibular_motion`, `auditory_access`, `keyboard_motor`, `screen_reader_semantic`, `cognitive_neurodivergent`
4. Include `// BUG:` comments in the fixture `.md` code for documentation, but always test with stripped versions (`strip_bug_comments.py`)
5. CLEAN fixtures must have zero real bugs and 3+ false positive traps
6. Regression fixtures must include `regression_fixture: true` and `non_inferiority_test` in metadata/rubric

See `evals/suites/perspectives/PILOT-REPORT.md` for full evaluation methodology and results.

## Evaluation Assets

This repo includes eval suites for `a11y-critic` and `perspectives`. The fixture and rubric assets are included here; the broader harness originated in the source monorepo.

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
