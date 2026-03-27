# A11y-Planner Evaluation Suite

Comprehensive evaluation framework for the **a11y-planner** skill — a 9-phase protocol for designing accessible implementations before coding.

---

## Quick Start

```bash
# Review the skill
cat /a11y-planner/.claude/agents/a11y-planner.md

# Read the evaluation design
cat skill-profile.md           # What does a11y-planner do?
cat domain-sampling-strategy.md # What scenarios are evaluated?
cat statistical-design.md      # How is performance measured?

# See example fixtures
ls fixtures/aria-disclosure-widget.* # Complete fixture example
ls rubrics/aria-disclosure-widget.*  # Scoring rubric example

# Run evaluation
python eval_runner.py --suite a11y-planner --n-fixtures 25 --repetitions 3
```

---

## Suite Overview

| Aspect | Details |
|--------|---------|
| **Skill** | a11y-planner |
| **Type** | PLANNER (design before code) |
| **Model** | claude-opus-4-6 |
| **Fixtures** | 25 realistic accessibility planning scenarios |
| **Domains** | 5 (ARIA patterns, keyboard nav, screen reader, visual/cognitive, testing/audit) |
| **Difficulty** | TRIVIAL(6), MODERATE(11), COMPLEX(5), AMBIGUOUS(3) |
| **Baselines** | 2 (zero-shot generic prompt, few-shot with structure) |
| **Repetitions** | 3 per fixture (75 total evaluations) |
| **Duration** | ~2-3 weeks for full evaluation |

---

## Core Files

### Configuration
- **`eval.yaml`** — Master evaluation configuration (fixtures, baselines, rubrics, statistical design)
- **`skill-profile.md`** — Comprehensive profile of a11y-planner skill (what it does, how it works, success criteria)
- **`domain-sampling-strategy.md`** — Domain taxonomy and fixture descriptions (25 scenarios across 5 domains)
- **`statistical-design.md`** — Statistical methodology (Wilcoxon signed-rank tests, effect sizes, subgroup analysis)

### Fixtures (25 total = 75 files)
- **`fixtures/{id}.md`** — Feature description and context (what to plan)
- **`fixtures/{id}.metadata.yaml`** — Scenario details, expected findings, key criteria
- **`rubrics/{id}.rubric.yaml`** — Scoring rubric (dimensions, weights, rule-based checks, LLM criteria)

### Baselines (2 conditions)
- **`baselines/baseline-zero-shot.md`** — Simple generic planning prompt (no structure, no examples)
- **`baselines/baseline-few-shot.md`** — Generic planning with structured approach and example response

### Inventory
- **`FIXTURE_INVENTORY.md`** — Complete listing of all 25 fixtures with descriptions

---

## The 5 Domains

### 1. ARIA Pattern Implementation (5 fixtures)
Tests whether a11y-planner maps interactive patterns to WAI-ARIA APG patterns with complete ARIA specifications.

| Fixture | Difficulty | Risk | Focus |
|---------|-----------|------|-------|
| 1.1 Custom Disclosure Widget | TRIVIAL | Low | Basic pattern mapping, aria-expanded, aria-controls |
| 1.2 Combobox with Autocomplete | MODERATE | Medium | Complex pattern, aria-owns, aria-activedescendant, dynamic content |
| 1.3 Tab Panel with Dynamic Content | MODERATE | Medium | Tab pattern, async loading, aria-busy, roving tabindex |
| 1.4 Custom Data Table with Sorting | COMPLEX | High | Table semantics, aria-sort, complex keyboard navigation |
| 1.5 Modal Dialog with Form | AMBIGUOUS | High | Dialog pattern, form pattern, focus trap, error handling |

### 2. Keyboard Navigation Design (5 fixtures)
Tests whether a11y-planner designs complete focus management including tab order, focus traps, focus restoration, and keyboard interactions.

| Fixture | Difficulty | Risk | Focus |
|---------|-----------|------|-------|
| 2.1 Simple Button Navigation | TRIVIAL | Low | Tab order, focus indicators, Enter/Space activation |
| 2.2 Menu Button with Dropdown | MODERATE | Medium | Focus movement into menu, Escape behavior, focus restoration |
| 2.3 Breadcrumb Navigation | MODERATE | Medium | List semantics, aria-current, link text quality |
| 2.4 Complex Modal with Focus Trap | COMPLEX | High | Focus trap implementation, Tab cycling, Escape, focus restoration |
| 2.5 Roving Tabindex in Composite | AMBIGUOUS | High | Roving tabindex design, arrow key navigation, Home/End support |

### 3. Screen Reader Experience (5 fixtures)
Tests whether a11y-planner designs semantic structure, landmarks, headings, live regions, form labels, and error associations.

| Fixture | Difficulty | Risk | Focus |
|---------|-----------|------|-------|
| 3.1 Simple Article Page | TRIVIAL | Low | Landmarks, heading hierarchy, semantic structure |
| 3.2 Search Results with Live Updates | MODERATE | Medium | Live regions, aria-live vs status role, dynamic updates |
| 3.3 Product Listing with Sorting | MODERATE | Medium | Complex heading hierarchy, filter semantics, sorting announcements |
| 3.4 Real-Time Notification System | COMPLEX | High | Live region role selection, urgency levels, timing |
| 3.5 Complex Form with Field-Level Help | AMBIGUOUS | High | Label/help/error associations, field visibility, conditional fields |

### 4. Visual & Cognitive Accessibility (5 fixtures)
Tests whether a11y-planner designs for color contrast, non-color alternatives, responsive text, motion, and consistency.

| Fixture | Difficulty | Risk | Focus |
|---------|-----------|------|-------|
| 4.1 Status Indicator Colors | TRIVIAL | Low | Color contrast, non-color alternatives (icon+text+position) |
| 4.2 Animated Transition | MODERATE | Medium | prefers-reduced-motion, animation timing, focus during animation |
| 4.3 Dark Mode Support | MODERATE | Medium | Contrast in both light and dark, prefers-color-scheme |
| 4.4 Complex Form with Validation UI | COMPLEX | High | Multi-indicator state communication, error clarity, field-to-error link |
| 4.5 Accessible Data Visualization | AMBIGUOUS | High | Chart alt text, data table alternative, interactive exploration, zoom |

### 5. Testing & Audit Planning (5 fixtures)
Tests whether a11y-planner designs complete testing strategies with automated, keyboard, screen reader, and visual testing approaches.

| Fixture | Difficulty | Risk | Focus |
|---------|-----------|------|-------|
| 5.1 Simple Component Testing | TRIVIAL | Low | Automated tests (axe-core), keyboard, screen reader |
| 5.2 Form Testing Strategy | MODERATE | Medium | Multiple test types, validation testing, acceptance criteria |
| 5.3 Modal Dialog Testing | MODERATE | Medium | Focus trap testing, Escape testing, focus restoration |
| 5.4 Data Table Testing | COMPLEX | High | Complex table testing, multiple test dimensions |
| 5.5 Multi-Page Audit Plan | COMPLEX | High | Audit scope, testing across pages, prioritization |

---

## Evaluation Dimensions (7 dimensions, 16 total weight)

Each plan is scored on 7 dimensions (0-100 per dimension). Composite score = weighted average.

| Dimension | Weight | Description |
|-----------|--------|-------------|
| **Completeness** | 3 | All 9 phases present (Scope, Structure, Interaction, Focus, State, Visual, Content, Testing, Tasks) |
| **APG Pattern Mapping** | 3 | Every interactive widget maps to specific APG pattern with URL citation |
| **WCAG Grounding** | 3 | Every design decision cites WCAG 2.2 criterion or APG pattern |
| **Specificity & Actionability** | 2 | Developers can implement from plan without guessing; ARIA lists precise; interactions explicit |
| **Multi-Perspective Coverage** | 2 | Keyboard, screen reader, low vision, cognitive, mobile accessibility all addressed |
| **Testing Coverage** | 2 | Automated, keyboard, screen reader, visual testing; measurable acceptance criteria; a11y-critic checkpoints |
| **Calibration & Proportionality** | 1 | Plan length appropriate to complexity (1-2 for TRIVIAL, 3-5 for MODERATE, 6-10 for COMPLEX) |

### Composite Score Ranges
- **90-100:** Excellent plan (implementable, complete, grounded, actionable)
- **75-89:** Good plan (mostly complete, minor gaps)
- **60-74:** Adequate plan (usable but notable gaps)
- **40-59:** Weak plan (significant gaps or specificity issues)
- **0-39:** Poor plan (incomplete, vague, unactionable)

---

## Baseline Conditions (3 conditions)

### Condition 1: a11y-planner (Target Skill)
- **Type:** Agent with 9-phase protocol
- **Model:** Claude Opus 4.6
- **Structure:** Detailed protocol covering all phases, mandatory WCAG/APG citations, explicit pattern mapping
- **Expected score:** 85-95 (strong across all dimensions)

### Condition 2: baseline-zero-shot (Generic Zero-Shot)
- **Type:** Simple unstructured prompt
- **Model:** Claude Opus 4.6
- **Structure:** "Create a comprehensive accessibility design plan" with no guidance
- **Expected score:** 65-75 (covers basics, lacks structure and citations)

### Condition 3: baseline-few-shot (Generic Few-Shot)
- **Type:** Structured prompt with example
- **Model:** Claude Opus 4.6
- **Structure:** Explicit sections + example response
- **Expected score:** 70-80 (better than zero-shot, still lacks protocol rigor)

---

## Statistical Testing

### Primary Test
**Wilcoxon signed-rank test** (one-tailed)
- **Hypothesis:** a11y-planner composite score > baseline-zero-shot
- **Success:** p < 0.05 AND delta ≥ 15 points
- **Sample size:** 25 fixtures × 3 repetitions = 75 paired observations

### Secondary Tests
1. **Gap Coverage:** a11y-planner identifies 25%+ more design gaps
2. **Specificity Rate:** a11y-planner cites WCAG/APG 20%+ more often
3. **Pattern Completeness:** a11y-planner maps 90%+ of interactive patterns
4. **Multi-Perspective Coverage:** a11y-planner addresses 4+ user perspectives per fixture
5. **False Positive Rate:** a11y-planner <5% false positives

### Effect Size
**Cohen's d** expected: 0.7-0.9 (large effect between a11y-planner and baselines)

### Subgroup Analysis
- **By domain:** Expected strengths in ARIA patterns and keyboard navigation
- **By difficulty:** Expected progressive advantage (TRIVIAL ~5-10pts, MODERATE ~15-20pts, COMPLEX ~25-35pts)
- **By pattern type:** Expected consistent advantage across semantic structure, patterns, focus, state, testing

---

## How to Run Evaluation

### Prerequisites
```bash
pip install anthropic pyyaml json
```

### Pilot Run (5 fixtures for validation)
```bash
python eval_runner.py \
  --suite a11y-planner \
  --mode pilot \
  --fixtures aria-disclosure-widget aria-combobox-autocomplete keyboard-modal-focus-trap sr-form-field-help test-data-table
```

### Full Evaluation (25 fixtures × 3 repetitions)
```bash
python eval_runner.py \
  --suite a11y-planner \
  --mode full \
  --n-fixtures 25 \
  --repetitions 3 \
  --randomize true \
  --output-dir results/
```

### Analysis
```bash
python analyze_results.py \
  --input results/evaluation_results.json \
  --output results/report.md \
  --include-subgroup-analysis true
```

---

## Fixture Structure

Each fixture consists of 3 files:

### 1. Fixture Description (.md)
Contains:
- Feature description and context
- Planning scope and constraints
- Success criteria
- What would be below expectations

**Example:** `fixtures/aria-disclosure-widget.md`

### 2. Metadata (.metadata.yaml)
Contains:
- Fixture ID, name, difficulty, domain, risk level
- Scenario details
- Expected plan sections
- Key evaluation criteria
- Expected findings (must-have, should-have, nice-to-have)
- Multi-perspective coverage expectations
- False positive traps

**Example:** `fixtures/aria-disclosure-widget.metadata.yaml`

### 3. Rubric (.rubric.yaml)
Contains:
- Scoring dimensions with weights
- Rule-based checks (binary or scalar)
- LLM judge criteria
- Composite score formula
- Scoring thresholds
- Expected reviewer performance (per condition)
- Verdict expectations
- Example excellent/weak responses

**Example:** `rubrics/aria-disclosure-widget.rubric.yaml`

---

## Expected Outcomes

### Primary Finding
a11y-planner should significantly outperform baselines on composite score:
- **vs baseline-zero-shot:** +15-25 points (p < 0.05)
- **vs baseline-few-shot:** +10-20 points (p < 0.05)

### Domain-Specific Strengths
1. **ARIA Pattern Implementation:** Strongest advantage (APG mapping is core strength)
2. **Keyboard Navigation Design:** Strong advantage (explicit focus management planning)
3. **Screen Reader Experience:** Strong advantage (semantic structure completeness)
4. **Visual & Cognitive Accessibility:** Moderate advantage (multi-indicator planning)
5. **Testing & Audit Planning:** Strong advantage (comprehensive testing strategy)

### Difficulty Progression
- **TRIVIAL fixtures:** Small advantage (+5-10 points, overhead for simple cases)
- **MODERATE fixtures:** Moderate advantage (+15-20 points, protocol shines)
- **COMPLEX fixtures:** Large advantage (+25-35 points, protocol handles complexity)
- **AMBIGUOUS fixtures:** Large advantage (+20-30 points, recognition of trade-offs)

### Secondary Metrics
- **Gap coverage:** a11y-planner identifies 25%+ more missing elements
- **Specificity rate:** a11y-planner cites WCAG/APG 30-40% more often
- **Pattern completeness:** a11y-planner maps 95%+ of patterns vs 70% baseline
- **False positive rate:** a11y-planner <5% vs 15%+ baseline

---

## Key Differentiators from Baselines

### What Makes a11y-planner Stronger

1. **Structured 9-Phase Protocol**
   - Ensures completeness (all aspects covered)
   - Baselines: Ad-hoc coverage, may miss sections

2. **Mandatory WCAG Grounding**
   - Every decision cites WCAG 2.2 or APG
   - Baselines: Some decisions lack grounding

3. **Mandatory APG Pattern Mapping**
   - Every interactive widget maps to established pattern
   - Baselines: May design custom interactions

4. **Explicit ARIA Attribute Lists**
   - Precise ARIA attributes with WCAG citations
   - Baselines: May mention attributes generically

5. **Focus Management by Design**
   - Focus traps, restoration, indicators all designed before code
   - Baselines: May defer to implementation phase

6. **Testing Strategy Embedded**
   - Acceptance criteria defined upfront
   - a11y-critic checkpoints for post-implementation
   - Baselines: Testing strategy generic or vague

---

## Limitations & Caveats

### Sample Size
- **25 fixtures** is adequate for large effects (d=0.8) but underpowered for small effects
- **Power = ~78%** at α=0.05, medium effect size (d=0.5)
- Small true differences may not reach significance

### Model Variation
- **Claude Opus 4.6** was current at evaluation time
- Model updates may affect performance
- Results specific to this model version

### Fixture Quality
- **25 fixtures** is broad but not exhaustive
- May not cover all edge cases or niche patterns
- Domain expert review recommended

### Rubric Subjectivity
- **30% LLM judge** component introduces some subjectivity
- Rule-based component (70%) more objective
- Rubric calibration on pilot run recommended

---

## References

- **WAI-ARIA Authoring Practices Guide (APG):** https://www.w3.org/WAI/ARIA/apg/
- **WCAG 2.2 Spec:** https://www.w3.org/WAI/WCAG22/quickref/
- **a11y-planner Agent:** `/a11y-planner/.claude/agents/a11y-planner.md`
- **a11y-critic Skill (Companion):** Accessibility code review after implementation
- **accessibility-testing Skill:** Automated accessibility testing

---

## Maintenance & Updates

### Adding New Fixtures
1. Create `.md` fixture description
2. Create `.metadata.yaml` with expectations
3. Create `.rubric.yaml` with scoring rules
4. Add to `FIXTURE_INVENTORY.md`
5. Update `eval.yaml` fixture list

### Updating Rubrics
- Keep rule-based checks synchronized across fixtures
- Maintain consistent dimension weights
- Document changes in rubric version

### Re-running Evaluation
- Pilot run validates rubrics before full suite
- Full suite can be run weekly/monthly for stability
- Compare results across model versions/updates

---

## Support

For questions about:
- **Skill design:** See `/a11y-planner/.claude/agents/a11y-planner.md`
- **Evaluation methodology:** See `statistical-design.md`
- **Specific fixtures:** See `fixtures/{id}.metadata.yaml`
- **Scoring:** See `rubrics/{id}.rubric.yaml`

