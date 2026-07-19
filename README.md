# Accessibility Skills

Cross-model accessibility skill and evaluation bundle — plan, test, review, and audit web accessibility from real perspectives. It ships Claude Code-compatible skills and benchmark assets used across Claude, Codex/OpenAI, Gemini-ready hosted runs, and local Ollama models.

```bash
npx skills add zivtech/accessibility-skills
```

**[Visual Explainer](https://zivtech.github.io/accessibility-skills/)** | **[Project Recap](docs/project-recap.html)** (open locally)

This bundle packages four core skills that cover the full accessibility development lifecycle:

- **Accessibility Planner** (`a11y-planner`): designs accessible implementations before coding (WCAG 2.2, WAI-ARIA APG patterns)
- **Accessibility Critic** (`a11y-critic`): reviews plans before implementation AND implementations after testing
- **Accessibility Tester** (`a11y-test`): runs real Playwright keyboard tests, axe-core scans, static analysis, and visual regression
- **Perspective Audit** (`perspective-audit`): deep review from 7 disability and situational access perspectives, escalated by the planner or critic when specific perspectives reach MEDIUM or HIGH alarm levels

Additional companion skill:

- **Accessibility Bug Reporting** (`bug-reporting`): converts findings into reproducible accessibility issues with required reporting fields (URL, XPath, HTML snippet, WCAG SC, rule ID, severity, frequency)

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

### Accessibility Planner (`a11y-planner`)

The Accessibility Planner is the pre-implementation design surface. It produces plans for:

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

### Accessibility Critic (`a11y-critic`)

The Accessibility Critic reviews accessibility design decisions at two points: **after planning** (to catch gaps before code is written) and **after testing** (to verify the implementation). It looks for:

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

### Accessibility Tester (`a11y-test`)

The Accessibility Tester is the measurement layer. It runs real tests and produces evidence that feeds into the critic's review, with five execution modes:

- **`npx playwright test`** — Codified CI keyboard tests, visual regression, axe-core scans. Primary path.
- **`agent-browser`** — Interactive reconnaissance: snapshot ARIA structure, verify fixes, probe widgets. Fastest for exploratory work (~1.5-2.6s per task).
- **`/webwright:run`** — Generate complete Python Playwright test scripts from prose descriptions. LLM-generated, ~30-130s first run, then ~4s re-runs with no LLM cost. Produces reusable `.py` artifacts.
- **`keyboard-a11y-tester`** — Goal-driven journey audits of live URLs: keyboard + emulated screen-reader personas, evidence-linked WCAG findings, live-region capture, focus-indicator measurement. External clone pinned to release `0.5.0`; cross-validated against this repo's 33 critic fixtures. See [adoption assessment](docs/keyboard-a11y-tester-adoption-assessment.md).
- **`@guidepup/virtual-screen-reader`** — Component/unit-level screen-reader assertions (accessible names, reading order, live-region announcements) in the project's own Vitest/Jest suite or Storybook play functions, pre-deploy, no URL needed. npm devDependency exact-pinned `0.32.1`; validated in jsdom, Vitest, Chromium, and Storybook 10. See [adoption assessment](docs/virtual-screen-reader-adoption-assessment.md).

Test capabilities:

- Playwright keyboard interaction tests (Tab, Enter, Escape, arrow keys — real key presses, not attribute checks)
- axe-core scanning via Playwright injection for automated WCAG violation detection
- eslint-plugin-jsx-a11y static analysis for React/Vue/JSX projects
- Visual regression testing with Playwright screenshots and optional BackstopJS
- WCAG 2.2 compliance checks including new criteria (2.4.11, 2.4.13, 2.5.7, 2.5.8, 3.3.7, 3.3.8)
- Dynamic test prioritization based on automated scan findings
- ARIA tree inspection via `aria_snapshot()` (Webwright) or `snapshot -i` (agent-browser)
- Goal-driven journey audits with per-step trace, reading-order census, and screenshot evidence (keyboard-a11y-tester)
- Screen-reader announcement and reading-order assertions at the component level, including live-region capture with politeness prefixes (virtual-screen-reader)

### Perspective Audit (`perspective-audit`)

The Perspective Audit provides deep accessibility review from 7 disability and situational access perspectives. It is activated by escalation — when the planner or critic flags one or more perspectives at MEDIUM or HIGH alarm level, those perspectives get a focused deep review.

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
plan → [generate test scripts] → critique plan → [perspective audit] → revise → implement → test → critique implementation → [perspective audit] → fix → re-test
```

1. Run `/a11y-planner` to design the feature before implementation.
2. Optionally run `/webwright:run` to generate test scripts from the planner's output.
3. Run `/a11y-critic` on the plan to catch gaps before coding.
4. If the critic escalates perspectives at MEDIUM/HIGH, run `/perspective-audit` for deep review.
5. Revise the plan based on critic and audit findings.
6. Build the feature.
7. Run `/a11y-test` (Playwright keyboard tests, axe-core scans, visual regression; virtual-screen-reader assertions for component announcement behavior; a keyboard-a11y-tester journey audit for live-URL targets).
8. Run `/a11y-critic` on the implementation after tests pass.
9. If the critic escalates perspectives, run `/perspective-audit` again.
10. Fix findings, re-test.

## Commands

- `/a11y-workflow` — Accessibility Workflow: orchestrate the full lifecycle (scout → plan → critique → test → critique), Claude Code only
- `/a11y-planner` — Accessibility Planner: design accessibility before coding
- `/a11y-critic` — Accessibility Critic: review plans or implementations
- `/a11y-test` — Accessibility Tester: run keyboard, axe-core, and visual regression tests; journey audits (keyboard-a11y-tester); component screen-reader assertions (virtual-screen-reader)
- `/perspective-audit` — Perspective Audit: deep review from escalated disability/situational access perspectives
- `/bug-reporting` — Accessibility Bug Reporting: produce reproducible bug reports from test or review findings

## Evidence Contract and Vital-Core Boundary

This repo adopts Vital-Core's reporting discipline, not its scanner runtime. The optional [A11y Evidence Finding Contract](docs/a11y-evidence-finding-contract.md) gives `a11y-test`, `a11y-critic`, and `perspective-audit` stable finding IDs, fingerprints, source evidence, WCAG/APG citations, Section 508/FPC context, perspective alarms, reproduction steps, expected/actual behavior, and trend language. Clean reviews should not emit empty finding contracts.

The v1 boundary keeps continuous crawling, ISO-week dashboards, generated report state, Wappalyzer/ParaCharts vendors, Lighthouse/security/sustainability engines, and mutable crawl state out of this bundle. See [Vital-Core Adoption Assessment](docs/vital-core-adoption-assessment.md). Use [Section508.gov conformance guidance](https://www.section508.gov/develop/applicability-conformance/) as regulatory context for WCAG 2.0 Level A/AA, and use [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) as the current planning and review target.

## Model Baselines

The evaluation story is cross-provider. The benchmark suite compares the same fixtures and rubrics across hosted and local model families.

Current committed result summaries cover:

- **Claude API** — Haiku-first escalation to Sonnet/Sonnet+thinking across 33 critic fixtures
- **Claude Code subagents** — Opus a11y-planner agents across all 25 planner fixtures (25/25 PASS, 234/235 must-have criteria), raw artifacts in `evals/results/claude-planner/`; Opus perspective-audit agents across all 25 perspective fixtures (2026-07-13, **first blind lane** — answer key withheld: post-003 scorer 20 PASS / 5 WARN / 0 FAIL, must-find 36/37; content-adjudicated 25/25 verdicts, 37/37 must-find, 0 CRITICAL/MAJOR on all 5 CLEAN fixtures), raw artifacts in `evals/results/claude-perspective/`. **Note:** all critic/perspective rows dated before 2026-07-13 ran non-blind (runners embedded fixture answer keys — since fixed, see BENCHMARK.md's blind-protocol disclosure); planner rows are exempt. Additionally, all critic/perspective rows dated before 2026-07-16 — blind lanes included — saw inline `// BUG:` hint comments in fixture code (de-hinted 2026-07-16); detection numbers are hint-assisted upper bounds, per BENCHMARK.md's hint-comment disclosure
- **Codex/OpenAI** — GPT-5.2-first escalation to GPT-5.5-low across 33 critic fixtures
- **Gemini** — Gemini 2.5 Flash across all 33 critic fixtures via the gemini CLI (31/33 PASS, 98% criteria-level must-find; pro escalation pending quota), raw artifacts in `evals/results/gemini/`
- **Ollama local models** — qwen3:32b **blind re-run 2026-07-13** (critic 33/33 PASS, 97% must-find, 0 false positives — blind-confirmed; perspective detection 20/20 + 36/37 must-find blind-confirmed, but 4/5 CLEAN perspective fixtures draw false REVISE/BLOCK verdicts blind, so the historical "100% perspective / 0% FP" row was answer-key-assisted on CLEAN), 25/25 planner; raw blind artifacts in `evals/results/ollama-blind/`. Same-day blind full-suite critic lanes: qwen3.5:latest 33/33 PASS + 98.5% must-find (needs ≥32K num_ctx on 4 long fixtures — receipts in BENCHMARK.md) and llama3.3:70b 33/33 PASS + 92.6%/97.1% adjudicated must-find. Historical non-blind rows: qwen3.5:27b (partial run: stopped 17/33 on /think stalls), deepseek-r1 probes. All of these rows predate the 2026-07-16 fixture de-hint (inline `// BUG:` comments were still in the prompts), so detection numbers are hint-assisted upper bounds; they also predate the same-day reassurance/verdict-steering fix (critic CLEAN/ADVERSARIAL prompts included their expected verdicts — those rows are verdict-assisted upper bounds; see the disclosure in `ollama/BENCHMARK.md`). **De-hinted re-run (qwen3:32b, 2026-07-16, `evals/results/ollama-dehinted/`)**: critic detection held exactly (33/33 PASS, 67/68 content-adjudicated must-find in both lanes; CLEAN 4/4 with zero findings — verdict-assisted except the repaired modal-complete-clean, whose prompt was properly cut); perspective lost exactly one hint-carried must-find item (36/37 vs 37/37 — map-interface-zoom target size); and the blind lane's "4/5 CLEAN wrong verdicts" proved run-unstable (1/5 wrong in the re-run on byte-identical CLEAN prompts) — cite both draws or neither. The post-verdict-fix re-baseline lane is open

Every hosted family is a peer row backed by committed raw artifacts. See [ollama/BENCHMARK.md](ollama/BENCHMARK.md) and [ollama/README.md](ollama/README.md) for the detailed tables, commands, and caveats.

## Install

```bash
npx skills add zivtech/accessibility-skills
```

Manual install:

```bash
git clone https://github.com/zivtech/accessibility-skills.git
cp -r accessibility-skills/.claude/skills/* ~/.claude/skills/
cp accessibility-skills/.claude/agents/*.md ~/.claude/agents/
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
  teams/                               # a11y-workflow team definition
.agents/
  skills/                              # Codex-compatible skill mirrors
.codex/
  agents/                              # Codex agent definitions for planner/critic
docs/
  EXTERNAL-SKILLS-INVENTORY.md         # Landscape scan of external a11y skills + adopted tools
  PERSPECTIVE-AGENTS-PLAN.md           # Architecture plan (v2.1, 3-critic reviewed)
  a11y-evidence-finding-contract.md     # Shared optional finding contract
  vital-core-adoption-assessment.md     # Adopt/adapt/defer/reject boundary
  keyboard-a11y-tester-adoption-assessment.md   # Journey-audit mode adoption + cross-validation
  virtual-screen-reader-adoption-assessment.md  # Component SR-assertion mode adoption + cross-validation
  drupal-patch-evaluations/            # Drupal core a11y patch evaluation ledger, patches, reports
  a11y-planner/
  a11y-critic/
templates/
evals/
  suites/
    a11y-critic/                         # 33 critic fixtures + rubrics
    a11y-planner/                        # 25 planner fixtures + rubrics
    perspectives/                        # 25 + 5 calibration perspective fixtures
    webwright-benchmark/                 # Webwright vs agent-browser speed + correctness data
  results/                               # Committed raw benchmark + cross-validation artifacts
    keyboard-a11y-tester/                #   KAT vs 33 critic fixtures agreement record
    virtual-screen-reader/               #   VSR fixture sweep, probes, Storybook lane record
  harness/
ollama/                                  # Local + hosted benchmark runners and score scripts
```

Tracked install surfaces now include `.claude/` for Claude Code-compatible discovery, `.agents/skills/` for Codex-compatible skills, and `.codex/agents/` for Codex agent definitions. The protocols, fixtures, rubrics, and benchmark runners are model-agnostic. Per-skill documentation lives under `docs/`.

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

Fixture code blocks ship hint-free (since 2026-07-16): planted-bug documentation lives only in
each fixture's `## Accessibility Issues` answer-key section, which both runners strip from
prompts (blind protocol). The CI guard `ollama/test_blind_prompts.py` fails if either leak —
answer keys or inline `BUG` hint comments — reappears in any composed prompt. (The former
`strip_bug_comments.py` workflow, which wrote stripped copies to a `fixtures-eval/` directory
no runner read, is deleted; see the hint-comment disclosure in `ollama/BENCHMARK.md`.)

The perspective eval harness runs fixtures under 3 prompt conditions. These are prompt-condition baselines, separate from model-family baselines such as Claude, Codex/OpenAI, Gemini, and local Ollama runs:
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
4. Document planted bugs only in the fixture's `## Accessibility Issues` answer-key section below the blind cut line — never as inline comments in the code blocks (the CI guard `ollama/test_blind_prompts.py` fails any composed prompt that leaks `BUG` hints)
5. CLEAN fixtures must have zero real bugs and 3+ false positive traps
6. Regression fixtures must include `regression_fixture: true` and `non_inferiority_test` in metadata/rubric

See `evals/suites/perspectives/PILOT-REPORT.md` for full evaluation methodology and results.

## Evaluation Assets

This repo includes eval suites for `a11y-planner`, `a11y-critic`, and `perspectives`. The fixture and rubric assets are included here; the broader harness originated in the source monorepo.

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
