# Statistical Design for A11y-Planner Evaluation

## Overview

This evaluation uses a **fixed-effects experimental design** with 25 fixtures evaluated 3 times each (75 total evaluations) across multiple baseline conditions. The design tests whether a11y-planner produces superior accessibility design specifications compared to generic planner baselines.

---

## Study Design

### Type
**Paired comparison** (each fixture evaluated under multiple conditions: a11y-planner vs baselines)

### Fixtures
- **Count:** 25 fixtures
- **Domains:** 5 (ARIA patterns, keyboard navigation, screen reader, visual/cognitive, testing/audit)
- **Difficulty:** TRIVIAL(6), MODERATE(11), COMPLEX(5), AMBIGUOUS(3)

### Conditions
1. **a11y-planner** (target skill, read-only agent with 9-phase protocol)
2. **baseline-zero-shot** (generic planning prompt, no examples)
3. **baseline-few-shot** (generic planning prompt + structured approach + examples)

### Repetitions
- **Per fixture:** 3 repetitions
- **Total evaluations:** 25 fixtures × 3 conditions × 3 repetitions = 225 evaluations
- **Randomization:** Random order within fixture × condition

---

## Primary Hypothesis

**H₀ (null):** a11y-planner composite score = baseline-zero-shot composite score
**H₁ (alternative):** a11y-planner composite score > baseline-zero-shot composite score
**Direction:** One-tailed (greater)

**Success criteria:** a11y-planner mean composite score exceeds baseline by ≥15 points with p < 0.05

---

## Evaluation Dimensions & Scoring

### Dimensions

1. **Completeness (weight: 3)**
   - All 9 phases present (scope, structure, interaction, focus, state, visual, content, testing, tasks)
   - No missing critical sections
   - Scoring: 0 (missing multiple phases) → 100 (all phases complete)

2. **APG Pattern Mapping (weight: 3)**
   - Every interactive widget maps to specific APG pattern
   - URL citations provided for each pattern
   - Pattern completeness (not custom reinventions)
   - Scoring: 0 (no pattern mapping) → 100 (all patterns mapped with URLs)

3. **WCAG Grounding (weight: 3)**
   - Every design decision cites WCAG 2.2 criterion or APG pattern
   - No generic statements ("make it accessible")
   - Criterion numbers and specific requirements cited
   - Scoring: 0 (no WCAG citations) → 100 (all decisions grounded)

4. **Specificity & Actionability (weight: 2)**
   - Developers can implement from plan without guessing
   - ARIA attribute lists complete and precise
   - Keyboard interactions explicitly documented
   - Focus management logic clearly defined
   - Test cases measurable and testable
   - Scoring: 0 (vague, incomplete) → 100 (highly specific, actionable)

5. **Multi-Perspective Coverage (weight: 2)**
   - Keyboard-only user experience planned
   - Screen reader user experience planned
   - Low vision user considerations addressed
   - Cognitive accessibility addressed
   - Touch target sizing for mobile accessibility
   - Scoring: 0 (single perspective) → 100 (all perspectives)

6. **Testing Coverage (weight: 2)**
   - Automated testing approach documented
   - Manual keyboard testing documented
   - Screen reader testing approach specified
   - Acceptance criteria measurable and per-feature
   - a11y-critic review checkpoints defined
   - Scoring: 0 (no testing strategy) → 100 (comprehensive)

7. **Calibration & Proportionality (weight: 1)**
   - Simple components appropriately brief (1-2 pages)
   - Medium complexity appropriately detailed (3-5 pages)
   - Complex features comprehensively planned (6-10 pages)
   - No scope creep or under-planning
   - Scoring: 0 (poorly calibrated) → 100 (well-calibrated)

### Composite Score Formula

```
Composite Score = sum(dimension_score × weight) / sum(weights) × 100
                = (C×3 + APG×3 + WCAG×3 + Spec×2 + Multi×2 + Test×2 + Cal×1) / 16 × 100
```

**Interpretation:**
- 90-100: Excellent plan (implementable, complete, grounded)
- 75-89: Good plan (mostly complete, minor gaps)
- 60-74: Adequate plan (usable but notable gaps)
- 40-59: Weak plan (significant gaps or specificity issues)
- 0-39: Poor plan (incomplete, vague, unactionable)

---

## Baseline Conditions

### Baseline A: Zero-Shot Generic Planning
**Prompt:** Simple accessibility planning request without structure or examples
**Model:** Claude Opus 4.6
**Example prompt:**
```
Create an accessibility design plan for [feature]. Ensure it covers
all aspects of accessibility including ARIA, keyboard navigation,
screen reader support, visual accessibility, and testing.
```
**Expected performance:** ~65-75 on composite score
**Why lower:** No protocol guidance, no example structure, no emphasis on WCAG grounding

### Baseline B: Few-Shot Generic Planning
**Prompt:** Simple planning request + structured approach + example response
**Model:** Claude Opus 4.6
**Example structured approach:**
```
Your response should include:
1. Overview and scope
2. Semantic structure and landmarks
3. Interactive pattern design
4. Keyboard navigation
5. State communication
6. Visual accessibility
7. Testing strategy
8. Implementation tasks

Also reference WAI-ARIA patterns where applicable and WCAG criteria.
```
**Expected performance:** ~70-80 on composite score
**Why higher than baseline A:** Explicit structure + example helps with organization and WCAG awareness

### Target: A11y-Planner
**Agent:** 9-phase protocol embedded in agent prompt
**Model:** Claude Opus 4.6
**Structure:** Detailed protocol covering all phases, explicit WCAG/APG citations, failure mode prevention
**Expected performance:** ~85-95 on composite score
**Why higher:** Comprehensive protocol, explicit pattern mapping requirement, WCAG grounding enforced

---

## Statistical Tests

### Primary Test: Wilcoxon Signed-Rank Test

**Test:** Wilcoxon signed-rank test (non-parametric paired comparison)
**Why:** Non-parametric test appropriate for non-normal distributions and small sample sizes
**Null hypothesis:** Median difference between a11y-planner and baseline scores = 0
**Alternative hypothesis:** Median difference > 0 (one-tailed)
**Significance level:** α = 0.05

**Interpretation:**
- If p < 0.05: Reject null, a11y-planner significantly better than baseline
- If p ≥ 0.05: Fail to reject null, no significant difference

### Secondary Tests

1. **Gap Coverage Test**
   - Metric: Number of items in "What's Missing" section
   - Hypothesis: a11y-planner identifies more gaps than baselines
   - Test: Wilcoxon signed-rank
   - Success: a11y-planner has 25%+ more gap items (p < 0.05)

2. **Specificity Test**
   - Metric: Percentage of design decisions with explicit WCAG/APG citations
   - Hypothesis: a11y-planner more strongly grounds decisions
   - Test: Wilcoxon signed-rank
   - Success: a11y-planner has 20%+ higher citation rate (p < 0.05)

3. **Pattern Completeness Test**
   - Metric: Percentage of interactive widgets with complete APG pattern mapping
   - Hypothesis: a11y-planner maps patterns more completely
   - Test: Wilcoxon signed-rank
   - Success: a11y-planner maps 90%+ of patterns with explicit citations (p < 0.05)

4. **Multi-Perspective Coverage Test**
   - Metric: Number of user perspectives explicitly addressed (keyboard, screen reader, low vision, cognitive, mobile)
   - Hypothesis: a11y-planner covers more perspectives
   - Test: Wilcoxon signed-rank
   - Success: a11y-planner addresses 4+ perspectives per fixture (p < 0.05)

5. **False Positive Test**
   - Metric: Percentage of non-issues incorrectly flagged as accessibility problems
   - Hypothesis: a11y-planner has fewer false positives
   - Test: Wilcoxon signed-rank (lower is better)
   - Success: a11y-planner has false positive rate < 5% (p < 0.05)

---

## Effect Size Estimation

### Cohen's d
Calculated for each condition pair (a11y-planner vs baseline):

**Effect size interpretation:**
- d = 0.2: Small effect
- d = 0.5: Medium effect
- d = 0.8: Large effect

**Expected effect sizes:**
- a11y-planner vs baseline-zero-shot: d ≈ 0.7-0.9 (large effect)
- a11y-planner vs baseline-few-shot: d ≈ 0.5-0.7 (medium-large effect)

### Bootstrap Confidence Intervals
- Method: Percentile bootstrap
- Resamples: 1000
- Confidence level: 95%
- Output: CI around composite score mean, gap coverage mean, specificity rate, etc.

---

## Power Analysis

### Sample Size Planning
- **Alpha (α):** 0.05
- **Beta (β):** 0.20 (80% power)
- **Effect size (δ):** 0.5 (medium effect, conservative estimate)
- **Paired samples n calculation:** n = 28 (two-tailed)

### Actual Sample
- **n = 25 fixtures** × 3 repetitions = 75 paired observations
- **Power:** Approximately 78% (slightly underpowered for detecting small effects, adequate for medium effects)
- **Risk:** May miss small true differences, but sufficient for large/medium effects

### Bonferroni Correction
Applied to secondary tests to maintain experiment-wise error rate:
- Number of tests: 2 (primary + secondary)
- Correction factor: 2
- Adjusted α: 0.05 / 2 = 0.025

---

## Subgroup Analysis

### By Domain
Analyze performance across 5 domains to identify where a11y-planner excels:
- **ARIA Pattern Implementation:** Expected strength
- **Keyboard Navigation:** Expected strength
- **Screen Reader Experience:** Expected strength
- **Visual & Cognitive Accessibility:** Expected strength
- **Testing & Audit Planning:** Expected strength

Null hypothesis: No interaction between skill and domain
Alternative: Skill performance varies by domain

### By Difficulty
Analyze performance across difficulty levels:
- **TRIVIAL:** Expected high performance (well-structured simple cases)
- **MODERATE:** Expected high performance (protocol covers all aspects)
- **COMPLEX:** Expected high performance (protocol designed for complex features)
- **AMBIGUOUS:** Interesting comparison (how does skill handle trade-offs?)

Null hypothesis: Performance is constant across difficulty levels
Alternative: Performance varies by difficulty

### By Pattern Type
Analyze performance across pattern categories:
- **Semantic Structure:** Expected strength
- **Interactive Patterns:** Expected strength
- **Focus Management:** Expected strength
- **State Communication:** Expected strength
- **Testing & Validation:** Expected strength

---

## Subgroup Analysis Details

### Domain-Specific Hypotheses

1. **ARIA Pattern Implementation (fixtures 1.1-1.5)**
   - Expected: a11y-planner significantly outperforms baselines in APG pattern mapping
   - Metric: APG Pattern Mapping dimension score
   - Expected delta: +20-30 points vs baselines

2. **Keyboard Navigation (fixtures 2.1-2.5)**
   - Expected: a11y-planner significantly outperforms baselines in focus management design
   - Metric: Specificity & Actionability dimension score (focus management detail)
   - Expected delta: +15-25 points vs baselines

3. **Screen Reader Experience (fixtures 3.1-3.5)**
   - Expected: a11y-planner produces more complete semantic structure plans
   - Metric: Completeness dimension score
   - Expected delta: +10-20 points vs baselines

4. **Visual & Cognitive Accessibility (fixtures 4.1-4.5)**
   - Expected: a11y-planner better handles multiple state indicators and non-color alternatives
   - Metric: Specificity & Actionability dimension score
   - Expected delta: +15-25 points vs baselines

5. **Testing & Audit Planning (fixtures 5.1-5.5)**
   - Expected: a11y-planner produces more measurable acceptance criteria
   - Metric: Testing Coverage dimension score
   - Expected delta: +15-25 points vs baselines

### Difficulty-Specific Hypotheses

1. **TRIVIAL fixtures (n=6):** a11y-planner and baselines perform similarly (both can handle simple cases)
   - Expected delta: +5-10 points (protocol overhead on simple cases)

2. **MODERATE fixtures (n=11):** a11y-planner begins to outperform (protocol addresses multiple concerns)
   - Expected delta: +15-20 points

3. **COMPLEX fixtures (n=5):** a11y-planner significantly outperforms (protocol scales to complexity)
   - Expected delta: +25-35 points

4. **AMBIGUOUS fixtures (n=3):** a11y-planner shows metacognitive awareness of trade-offs
   - Expected delta: +20-30 points (recognizing ambiguity is valuable)

---

## Outlier Detection & Handling

### Outlier Definition
Observations >2 SD from condition mean (identified per condition, per dimension)

### Handling Strategy
1. **Flag outliers:** Document any score >100 or <0 (scoring errors)
2. **Investigate extreme values:** Score >95 or <10 may indicate unusual response
3. **Keep outliers in primary analysis:** Non-parametric tests robust to outliers
4. **Sensitivity analysis:** Re-run tests with outliers excluded, compare results
5. **Report both:** Present primary analysis with outliers and sensitivity analysis without

---

## Success Criteria

### Primary Success
✓ a11y-planner composite score > baseline-zero-shot by ≥15 points
✓ p < 0.05 on Wilcoxon signed-rank test

### Secondary Success
✓ Gap coverage: a11y-planner identifies 25%+ more plan gaps
✓ WCAG grounding: a11y-planner cites WCAG/APG 20%+ more often
✓ Pattern mapping: a11y-planner maps 90%+ of interactive patterns with citations
✓ Multi-perspective: a11y-planner addresses 4+ user perspectives per fixture
✓ False positive rate: a11y-planner <5% false positives

### Subgroup Success
✓ Significant advantage in ARIA Pattern and Keyboard Navigation domains
✓ Progressive improvement with difficulty (higher delta on COMPLEX vs TRIVIAL)
✓ Recognition of ambiguous fixtures (documents trade-offs, alternatives)

---

## Reporting Plan

### Statistical Tests Report
- Test name, hypothesis, test statistic, p-value, effect size
- 95% confidence intervals for mean differences
- One table per test

### Descriptive Statistics
- Mean, SD, min, max per condition
- Median (for non-parametric context)
- Per-dimension breakdowns

### Subgroup Comparisons
- Performance by domain (table + visualization)
- Performance by difficulty (table + visualization)
- Performance by pattern type (table + visualization)

### Visualizations
1. Box plot: Composite scores by condition × difficulty
2. Scatter plot: Composite score vs dimension breakdown
3. Bar chart: Win rate by domain (a11y-planner wins vs baseline)
4. Line plot: Performance trajectory (TRIVIAL → AMBIGUOUS)

### Narrative Summary
- Primary findings (p-value, effect size, practical significance)
- Subgroup insights (where does skill shine?)
- Baseline comparison (what makes baselines weaker?)
- Recommendations (when to use each approach)

---

## Robustness Checks

### Variation in Rubric Interpretation
- **Risk:** LLM judges (30% of hybrid rubric weight) may score inconsistently
- **Mitigation:** Rubric calibration on 5 pilot fixtures before full evaluation
- **Check:** Inter-rater reliability (if using multiple judges) or consistency checks

### Model Variation
- **Risk:** Model performance may vary by day or version
- **Mitigation:** Use consistent model (claude-opus-4-6) and same API setup
- **Check:** Consistency across repetitions (high variance suggests instability)

### Prompt Sensitivity
- **Risk:** Baseline prompts may be underspecified
- **Mitigation:** Baseline prompts reviewed against existing literature on planning prompts
- **Check:** Sensitivity analysis with slightly different baseline prompts

### Fixture Quality
- **Risk:** Fixtures may be biased toward a11y-planner strengths
- **Mitigation:** Independent fixture review, domain expert validation
- **Check:** Verify fixtures are realistic and represent common scenarios

---

## Analysis Timeline

1. **Pilot evaluation (5 fixtures):** Validate rubrics, baselines, fixture quality
2. **Main evaluation (25 fixtures × 3 repetitions):** Full dataset generation
3. **Statistical analysis:** Wilcoxon tests, effect sizes, confidence intervals
4. **Subgroup analysis:** Domain, difficulty, pattern type comparisons
5. **Robustness checks:** Outlier analysis, sensitivity analysis
6. **Report generation:** Statistical results, visualizations, narrative

**Estimated timeline:** 2-3 weeks (depending on evaluation latency)

