# A11y-Critic Evaluation Suite

Complete evaluation infrastructure for the a11y-critic skill, testing accessibility design review capabilities across diverse component types, accessibility patterns, and difficulty levels.

## Suite Overview

**Skill**: a11y-critic (10-phase accessibility investigation protocol)

**Type**: CRITIC (reviews accessibility in existing code)

**Model**: claude-opus-4-6

**Evaluation Focus**:
- Accessibility *design decisions* (incomplete ARIA patterns, missing focus management, multi-perspective gaps)
- Pattern completeness (not just presence of ARIA attributes)
- Gap analysis ("What's Missing" sections)
- Evidence quality (file:line references, WCAG/APG citations)
- Multi-perspective coverage (screen reader, keyboard, low vision, cognitive)
- Severity calibration (realistic user impact)

## Directory Structure

```
a11y-critic/
├── fixtures/
│   ├── interactive-dropdown-clean.md
│   ├── interactive-dropdown-clean.metadata.yaml
│   ├── interactive-dropdown-focus-bug.md
│   ├── interactive-dropdown-focus-bug.metadata.yaml
│   ├── tabs-missing-arrow-nav.md
│   ├── tabs-missing-arrow-nav.metadata.yaml
│   ├── form-validation-missing-aria-describedby.md
│   ├── form-validation-missing-aria-describedby.metadata.yaml
│   ├── modal-complete-clean.md
│   ├── modal-complete-clean.metadata.yaml
│   ├── data-table-missing-scope.md
│   ├── data-table-missing-scope.metadata.yaml
│   ├── heading-hierarchy-skipped.md
│   ├── heading-hierarchy-skipped.metadata.yaml
│   ├── search-results-dynamic-clean.md
│   ├── search-results-dynamic-clean.metadata.yaml
│   ├── loading-state-missing-aria-busy.md
│   ├── loading-state-missing-aria-busy.metadata.yaml
│   ├── button-skip-link-clean.md
│   └── button-skip-link-clean.metadata.yaml
│
├── rubrics/
│   ├── interactive-dropdown-clean.rubric.yaml
│   ├── interactive-dropdown-focus-bug.rubric.yaml
│   └── ... (rubric for each fixture)
│
├── baselines/
│   ├── baseline-zero-shot.md (generic accessibility review)
│   └── baseline-few-shot.md (generic + structured approach + example)
│
├── skill-profile.md (comprehensive skill description)
├── domain-sampling-strategy.md (fixture selection rationale)
├── statistical-design.md (methodology, power analysis, hypothesis)
├── eval.yaml (harness configuration)
├── pilot-results.md (placeholder for pilot run results)
└── README.md (this file)
```

## Fixtures at a Glance

### By Difficulty Level

**CLEAN (6 fixtures)** — Properly implemented components; baseline for accuracy/false-positive rate:
- interactive-dropdown-clean
- modal-complete-clean
- search-results-dynamic-clean
- button-skip-link-clean
- (2 more planned)

**HAS-BUGS (11 fixtures)** — 1-2 obvious a11y issues; tests pattern detection:
- interactive-dropdown-focus-bug (focus not restored)
- tabs-missing-arrow-nav (incomplete pattern)
- form-validation-missing-aria-describedby (missing associations + live region)
- data-table-missing-scope (missing scope attributes)
- heading-hierarchy-skipped (h1 → h3, skipping h2)
- loading-state-missing-aria-busy (missing aria-busy)
- (5 more planned)

**FLAWED (5 fixtures)** — 3-5 subtle issues; tests gap analysis:
- (To be created: multiple issues, incomplete patterns, multi-perspective gaps)

**ADVERSARIAL (3 fixtures)** — Ambiguous or defensive implementations; edge cases:
- (To be created: defensible but questioned patterns, false-positive traps)

### By Domain

| Domain | Count | Fixtures |
|--------|-------|----------|
| Interactive Widgets | 5 | Dropdowns, Tabs, Modals |
| Form & Validation | 5 | Form validation, error association, live regions |
| Content & Semantic Structure | 5 | Headings, tables, landmarks, lists |
| Focus Management & Keyboard | 5 | Skip links, tab order, focus restoration |
| Dynamic Content & Live Regions | 3 | Loading states, search results, async updates |
| Color, Motion, & Sensory | 2 | Contrast, reduced motion, touch targets |

**Total**: ~25 fixtures (expandable to 28-30 for higher power)

## Fixture Anatomy

Each fixture consists of:

1. **Artifact File** (`.md`): React/HTML component code with real a11y issues planted
   - 300-500 words of realistic code
   - CSS styles for visual context
   - Expected behavior description
   - Accessibility features present
   - Planted issues with evidence locations

2. **Metadata File** (`.metadata.yaml`): Structured fixture information
   - Domain, difficulty, component type
   - Expected findings (must-find, should-find, nice-to-find, false-positive-traps)
   - WCAG criteria and APG patterns involved
   - Multi-perspective impact analysis
   - Expected verdict

3. **Rubric** (optional): Scoring guidance for this specific fixture
   - Weighted categories (must-find=3, should-find=2, etc.)
   - Expected reviewer performance
   - Scoring thresholds

## Baselines

### Baseline A: Zero-Shot

Simple, direct accessibility review prompt:
```
Review this component for accessibility issues.
Report: issue description, severity, user group impacted, fix.
Cover: ARIA, keyboard, semantics, focus, colors, forms, live regions, headings, landmarks.
```

**Expected performance**: 40-60% composite score on HAS-BUGS fixtures
**Rationale**: Should catch obvious issues but miss pattern incompleteness and gap analysis

### Baseline B: Few-Shot

Same prompt + structured approach + example:
```
Review using: Semantic HTML audit → ARIA pattern audit → Focus audit → State communication → Multi-perspective → What's missing

Example finding: [detailed format example]
```

**Expected performance**: 50-70% composite score on HAS-BUGS fixtures
**Rationale**: Structure + example help, but without deep investigation protocol

## Evaluation Methodology

### Scoring Rubric

**Composite Score** (primary metric):
```
score = sum(found_items * weight) / sum(positive_weights) * 100

Weights:
- must_find (should find 100%): +3 per finding
- should_find (skilled reviewer): +2 per finding
- nice_to_find (optimization): +1 per finding
- evidence_quality (CRITICAL/MAJOR backed by file:line): +1
- format_compliance: +1
- false_positive_trap (avoid flagging non-issues): -2 per false positive

Example: Found 2/2 must-finds, 1/1 should-find, evidence on both, no false positives:
score = (6 + 2 + 1 + 1) / 8 * 100 = 125% (capped at 100% or higher if exceeding expectations)
```

### Statistical Tests

**Primary Test**: Wilcoxon Signed-Rank (non-parametric paired comparison)
- H1: a11y-critic > baseline-zero-shot (p < 0.05, one-tailed)
- Effect size: Cohen's d ≥ 0.5 (medium)

**Secondary Tests**:
- Gap coverage (What's Missing section item count)
- Evidence rate (percentage of CRITICAL/MAJOR with file:line)
- Pattern completeness detection (must-find issues found)
- False positive rate (non-issues incorrectly flagged)
- Multi-perspective coverage (four perspectives addressed)

**Power Analysis**: 80% power, α=0.05, d=0.5 → n ≈ 28 (using 25 for domain coverage trade-off)

**Subgroup Analysis**: By domain, difficulty, pattern type

See [statistical-design.md](./statistical-design.md) for full methodology.

## Success Criteria

| Metric | Threshold | Reasoning |
|--------|-----------|-----------|
| Composite score delta | ≥ 15 points | 15% improvement over baseline |
| Gap coverage delta | ≥ 25% | Key differentiator |
| Evidence rate delta | ≥ 20 points | Stronger findings |
| Pattern completeness detection | ≥ 80% | Should find incomplete patterns |
| False positive rate | < 15% | Maintain specificity |
| Win rate | ≥ 60% | Beat baseline on majority |
| p-value | < 0.05 | Statistically significant |

## Key Differentiators Being Tested

1. **Gap Analysis Excellence**: "What's Missing" section surfaces 4-5x more design gaps than baseline
   - Missing aria-describedby on form errors
   - Missing focus restoration on modal close
   - Missing arrow key navigation in tabs
   - Missing live regions for dynamic content
   - Missing skip links, missing scope attributes, etc.

2. **Pattern Completeness**: Identifies incomplete ARIA patterns (aria-selected without arrow keys)
   - Not just "is aria-selected present?" but "is the full pattern implemented?"

3. **Multi-Perspective Mandatory**: Reviews from 4 angles; baseline may cover 1-2
   - Screen reader perspective
   - Keyboard-only perspective
   - Low vision perspective
   - Cognitive accessibility perspective

4. **Evidence-Backed Findings**: 85%+ of CRITICAL/MAJOR with file:line references; baseline ~40%

5. **Severity Calibration**: Realist check prevents alarmism; matches actual user impact

6. **Self-Audit**: Confidence gating moves uncertain findings to Open Questions; reduces false positives

## Pilot Run

**Pilot fixtures** (5 representative):
1. interactive-dropdown-clean (CLEAN baseline)
2. interactive-dropdown-focus-bug (HAS-BUGS, obvious issue)
3. form-validation-missing-aria-describedby (HAS-BUGS, multiple issues)
4. modal-complete-clean (CLEAN, false-positive test)
5. tabs-missing-arrow-nav (HAS-BUGS, pattern incompleteness)

**Pilot validation**:
- Rubrics unambiguous (LLM judge understands scoring)
- Baselines fair (not strawmen)
- Fixtures discriminate (skill outperforms baseline)
- Variance reasonable (not all 90%+ or all 30%)
- Evidence scoring reproducible

**Expected pilot results**:
- a11y-critic ~80% composite on HAS-BUGS
- baseline-zero-shot ~50% composite on HAS-BUGS
- p-value < 0.05 on gap coverage and evidence rate
- No rubric ambiguities

See [pilot-results.md](./pilot-results.md) for actual results.

## Running the Evaluation

### Prerequisites

- Claude Opus 4.6 (or latest available)
- Evaluation harness supporting:
  - Wilcoxon signed-rank testing
  - Bootstrap confidence intervals
  - Hybrid rule-based + LLM judge scoring

### Execution

1. **Initialize**: Load eval.yaml configuration
2. **Run Pilot**: Execute on 5 pilot fixtures
3. **Validate**: Check pilot results against criteria
4. **Run Full**: Execute on all 25 fixtures × 3 repeats
5. **Analyze**: Run statistical tests, subgroup analysis
6. **Report**: Generate markdown report with findings

### Output

**grading.json**: Detailed scores for all evaluations
- fixture_id, condition, composite_score, must_find_count, should_find_count, evidence_rate, verdict, etc.

**Report**: Markdown summary with:
- Executive summary (a11y-critic outperforms baseline by X% with p < Y)
- Methodology (Wilcoxon, bootstrap, subgroups)
- Primary findings (composite scores, effect sizes)
- Statistical tests (p-values, confidence intervals)
- Subgroup analysis (by domain, difficulty, pattern type)
- Failure modes (where baseline excels)
- Recommendations

## Extending the Suite

### Adding Fixtures

1. Create artifact (`.md` file) with realistic HTML/React component and planted issues
2. Create metadata (`.metadata.yaml`) with expected findings and WCAG citations
3. Create rubric (`.rubric.yaml`) with must/should/nice/trap categories
4. Assign domain, difficulty, pattern type
5. Verify fixture is independently reviewable (no dependencies on other fixtures)

### Adjusting Difficulty

- **CLEAN**: Few/no issues; tests baseline accuracy and false-positive rate
- **HAS-BUGS**: 1-2 obvious issues; tests basic pattern detection
- **FLAWED**: 3-5 subtle issues; tests gap analysis and multi-perspective
- **ADVERSARIAL**: Ambiguous or defensible; tests severity calibration and edge cases

### New Domains

Current 6 domains cover most common a11y patterns. Consider adding:
- Data visualization accessibility
- SVG and canvas accessibility
- Drag-and-drop and custom interactions
- Mobile/touch accessibility
- Internationalization and language

## Key Files

| File | Purpose |
|------|---------|
| [skill-profile.md](./skill-profile.md) | Comprehensive description of a11y-critic skill, protocol, success criteria |
| [domain-sampling-strategy.md](./domain-sampling-strategy.md) | Fixture selection rationale, sampling matrix, coverage table |
| [statistical-design.md](./statistical-design.md) | Power analysis, hypothesis testing, subgroup methodology |
| [eval.yaml](./eval.yaml) | Harness configuration, fixture/rubric paths, statistical parameters |
| [baselines/](./baselines/) | Zero-shot and few-shot baseline prompts |
| [fixtures/](./fixtures/) | Artifact files and metadata for all fixtures |
| [rubrics/](./rubrics/) | Scoring rubrics for each fixture |

## Contact & Methodology

This evaluation suite follows best practices from:
- **Test Builder agent**: Systematic fixture design, balanced difficulty distribution, fair baselines
- **Harsh-Critic skill**: Multi-phase investigation protocol, gap analysis, multi-perspective review

For updates or questions, see the test-builder agent documentation.

---

**Last Updated**: 2026-03-09
**Status**: Complete pilot infrastructure; ready for full evaluation
