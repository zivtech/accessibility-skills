# A11y-Critic Evaluation: Statistical Design

## Overview

This document specifies the statistical methodology for the a11y-critic skill evaluation. The goal is to rigorously measure whether a11y-critic outperforms generic accessibility review baselines across diverse fixtures and difficulty levels.

## Sample Size Calculation

### Target Sample Size

- **n_fixtures = 25** (slightly below power-calculated 28 to fit domain coverage)
- **n_repeats = 3** (3 independent runs per fixture to reduce variance)
- **total_evaluations = 75** (skill + baseline A + baseline B × 25 × 3)

### Justification

Power analysis for paired comparison (Wilcoxon signed-rank test):

```
n ≈ 2 × (z_α + z_β)² × σ² / δ²

where:
- z_α = 1.645 (one-tailed, α=0.05)
- z_β = 0.842 (80% power, β=0.20)
- δ = 0.5 (medium effect size, Cohen's d)
- σ ≈ 0.8 (expected std dev in composite scores)

n ≈ 2 × (1.645 + 0.842)² × 0.64 / 0.25
n ≈ 2 × 6.41 × 0.64 / 0.25
n ≈ 32.8 → round to 28 minimum, 25 acceptable

With 3 repeats per fixture and Wilcoxon (non-parametric, conservative), 25 fixtures provides adequate power for 0.5 medium effect size at 80% power.
```

### Assumptions

- **Effect size (δ)**: 0.5 medium (a11y-critic expected to outperform baseline by ~0.5 SD)
- **Variance (σ)**: 0.8 expected across fixtures (some fixtures discriminate well, others don't)
- **Correlation between repeats**: 0.7 (three runs of same fixture are correlated; reduces effective n slightly)
- **Significance level (α)**: 0.05 one-tailed (a11y-critic > baseline)
- **Power**: 80% (probability of detecting true effect)

## Primary Hypothesis

**H1**: The composite score of a11y-critic exceeds baseline-zero-shot by 15+ percentage points, with p < 0.05 (one-tailed).

**H0**: No significant difference between a11y-critic and baseline-zero-shot composite scores.

## Significance Testing

### Primary Test: Wilcoxon Signed-Rank Test

**Why Wilcoxon?**
- Paired comparison (skill vs baseline on same fixtures)
- Non-parametric (doesn't assume normality; scores may be bimodal or skewed)
- More robust than paired t-test to outliers
- Conservative (less likely to find false positives)

**Test procedure**:
1. For each fixture, calculate: Δ = score(a11y-critic) - score(baseline-zero-shot)
2. Rank absolute differences |Δ|, ignoring zeros
3. Sum ranks of positive differences (T+)
4. Compare T+ to critical value for n=25 at α=0.05, one-tailed
5. Report p-value and effect size (r = Z / √N)

**Interpretation**:
- p < 0.05: Significant difference (a11y-critic > baseline)
- p ≥ 0.05: No significant difference

### Secondary Tests

1. **Gap Coverage (What's Missing)**: Wilcoxon on count of gap items identified
   - Hypothesis: a11y-critic identifies 25%+ more gaps than baseline
   - Success criterion: p < 0.05, median gap count delta ≥ 1.5 items

2. **Evidence Rate**: Wilcoxon on percentage of CRITICAL/MAJOR findings with file:line evidence
   - Hypothesis: a11y-critic provides evidence for 85%+ of findings; baseline ~40%
   - Success criterion: p < 0.05, difference ≥ 20 percentage points

3. **Pattern Completeness Detection**: Wilcoxon on detection rate of must-find issues
   - Hypothesis: a11y-critic finds 80%+ of incomplete ARIA patterns; baseline ~50%
   - Success criterion: p < 0.05, difference ≥ 25 percentage points

4. **False Positive Rate**: Wilcoxon on percentage of non-issues incorrectly flagged
   - Hypothesis: a11y-critic has <15% false positive rate; baseline ~25%
   - Success criterion: p < 0.05, a11y-critic rate lower than baseline

### Multiple Comparison Correction

**Bonferroni correction**: α_adjusted = 0.05 / 2 = 0.025 (comparing against 2 baselines)

All tests use adjusted significance level to control family-wise error rate.

## Effect Size Estimation

### Cohen's d

For each metric (composite score, gap coverage, evidence rate):

```
d = (mean(a11y-critic) - mean(baseline-zero-shot)) / pooled_std

where:
pooled_std = sqrt(((n-1)*var(a11y-critic) + (n-1)*var(baseline)) / (2n-2))

Interpretation:
- d < 0.2: small effect
- 0.2 ≤ d < 0.5: small-medium effect
- 0.5 ≤ d < 0.8: medium effect
- d ≥ 0.8: large effect
```

**Expected effect sizes**:
- Composite score: d ≥ 0.5 (medium)
- Gap coverage: d ≥ 0.8 (large, this is key differentiator)
- Evidence rate: d ≥ 0.7 (medium-large)
- False positive rate: d ≤ -0.3 (a11y-critic lower)

## Confidence Intervals

### Bootstrap 95% CI

For each metric:

1. Pool all 75 evaluations (25 fixtures × 3 repeats)
2. Resample with replacement: 1000 bootstrap samples of size 75
3. Calculate statistic (mean composite score, gap coverage, etc.) for each sample
4. Sort results, extract 2.5th and 97.5th percentiles
5. Report as [lower_CI, point_estimate, upper_CI]

**Interpretation**: 95% CI that doesn't contain baseline value indicates significant difference.

## Subgroup Analysis

### Dimensions

1. **By Domain** (6 subgroups):
   - Interactive Widgets (5 fixtures)
   - Form & Validation (5 fixtures)
   - Content & Semantic Structure (5 fixtures)
   - Focus Management & Keyboard (5 fixtures)
   - Dynamic Content & Live Regions (3 fixtures)
   - Color, Motion, & Sensory (2 fixtures)

2. **By Difficulty** (4 subgroups):
   - CLEAN (6 fixtures): baseline accuracy test
   - HAS-BUGS (11 fixtures): pattern detection
   - FLAWED (5 fixtures): gap analysis
   - ADVERSARIAL (3 fixtures): edge cases

3. **By Pattern Type** (5 subgroups):
   - ARIA Pattern Completeness (8 fixtures)
   - Semantic HTML (5 fixtures)
   - Focus Management (8 fixtures)
   - State Communication (6 fixtures)
   - Multi-perspective Accessibility (all 25)

### Subgroup Reporting

For each subgroup:
- n (number of fixtures)
- Mean composite score (a11y-critic vs baseline)
- 95% CI
- Cohen's d
- Wilcoxon p-value (if n ≥ 5)
- Win/loss/tie count
- Standout fixtures (highest and lowest a11y-critic performance)

### Interpretation

- **Consistent across subgroups**: Skill improvement is general, not domain-specific
- **Large variance by subgroup**: Skill excels at some domains (e.g., gap analysis) but not others
- **CLEAN/HAS-BUGS similar, FLAWED divergent**: Suggests skill adds value on complex cases, not just obvious bugs

## Hypothesis for Subgroup Performance

**Expected pattern**:
- **CLEAN**: a11y-critic ≈ baseline (both 90%+), tests false-positive rate
- **HAS-BUGS**: a11y-critic > baseline (80%+ vs 50%), obvious issues detected by both
- **FLAWED**: a11y-critic >> baseline (70%+ vs 30%), skill excels at complex issues
- **ADVERSARIAL**: a11y-critic > baseline (55%+ vs 40%), skill handles ambiguity better

This gradient suggests skill adds value primarily on pattern completeness and gap analysis (complex cases), not just basic issue detection.

## Scoring Aggregation

### Composite Score (Primary Metric)

For each reviewer output on each fixture:

```
score = sum(found_items * weight) / sum(positive_weights) * 100

where:
- found_items = {must_find_count, should_find_count, nice_to_find_count,
                  evidence_quality_present, format_compliant}
- weights = {3, 2, 1, 1, 1}
- positive_weights = 8 (sum of weights)
- false_positive_trap penalizes by subtracting 2 per false positive

Example:
- Found: 2/2 must-find issues (6 points)
- Found: 1/1 should-find issue (2 points)
- Found: 1/1 nice-to-find issue (1 point)
- Evidence quality: yes (1 point)
- Format compliant: yes (1 point)
- No false positives (0 penalty)
- Total: 11 / 8 * 100 = 137.5%

Capped at 100% if all categories met; can go >100% if excellence demonstrated.
```

### Gap Coverage

Count of distinct gaps identified in "What's Missing" section. Each distinct gap counts as 1 point.

Expected:
- a11y-critic: 4-6 gaps per HAS-BUGS/FLAWED fixture
- baseline: 1-2 gaps per fixture

### Evidence Rate

Percentage of CRITICAL/MAJOR findings with file:line or code quote evidence.

Expected:
- a11y-critic: 85%+
- baseline: 40-50%

## Variance Components

Expected sources of variance in composite scores:

1. **Fixture difficulty** (≈40% of variance)
   - CLEAN fixtures score high across all conditions
   - FLAWED/ADVERSARIAL fixtures show largest skill separation

2. **Reviewer consistency** (≈20% of variance)
   - Same fixture, different run may yield ±5-10 points
   - Repeated runs of same condition average out over 3 repeats

3. **Domain-specific challenges** (≈25% of variance)
   - Focus management issues: a11y-critic excels (large effect)
   - Color/motion issues: smaller differences (both miss some)
   - Live regions: a11y-critic excels (large effect)

4. **Noise and measurement error** (≈15% of variance)
   - Rubric interpretation variance
   - LLM judge consistency

Total expected variance (σ²) ≈ 0.64 (σ ≈ 0.8 composite score std dev)

## Contingency: If Power Insufficient

If pilot shows variance higher than expected (σ > 0.9):
- Extend fixtures to 28-30 (trade off domain coverage for power)
- Increase repeats to 5 (reduces variance ~10%)
- Use permutation test instead of Wilcoxon (may detect smaller effects)

If effect size smaller than expected (Cohen's d < 0.4):
- Investigate why baselines perform better than expected
- Check if baseline prompts need adjustment
- May indicate skill is less differentiated than hypothesized

## Pilot Run

**Pilot fixtures** (5 representative):
1. interactive-dropdown-clean (CLEAN, should be 90%+ for all)
2. interactive-dropdown-focus-bug (HAS-BUGS, should discriminate)
3. form-validation-missing-aria-describedby (HAS-BUGS, live region + association)
4. modal-complete-clean (CLEAN, false-positive test)
5. tabs-missing-arrow-nav (HAS-BUGS, pattern incompleteness)

**Pilot outputs**:
- Composite scores for all conditions (skill + 2 baselines × 5 fixtures × 1 run)
- Variance estimate
- Qualitative assessment of baseline fairness
- Rubric ambiguities identified

**Success criteria for pilot**:
- Variance σ ≤ 0.85 (acceptable)
- Effect size (a11y-critic vs baseline zero-shot) ≥ 0.4 (meaningful)
- No rubric ambiguities that prevent fair scoring
- Baselines are genuinely good (not strawmen)
- Fixtures discriminate (not all 90%+ or all 30%)

If pilot passes, proceed to full evaluation. If not, adjust fixtures/rubrics/baselines and re-pilot.

## Success Criteria Summary

| Metric | Threshold | Reasoning |
|--------|-----------|-----------|
| Composite score delta | ≥ 15 points | 15%+ improvement over baseline |
| Gap coverage delta | ≥ 25% | a11y-critic's key differentiator |
| Evidence rate delta | ≥ 20 points | Stronger evidence quality |
| Pattern completeness detection | ≥ 80% | Should find incomplete patterns |
| False positive rate | < 15% | Maintain specificity |
| Win rate | ≥ 60% | Beat baseline on majority of fixtures |
| p-value (primary test) | < 0.05 | Statistically significant |
| Wilcoxon effect size (r) | ≥ 0.3 | Medium effect (r = 0.3 ≈ d = 0.6) |

## Reporting

Final report includes:
- Primary hypothesis test results with p-value and effect size
- Secondary test results (gap coverage, evidence rate, pattern detection)
- Subgroup analysis with breakdowns by domain, difficulty, pattern type
- Confidence intervals for all metrics
- Win/loss/tie summary
- False positive analysis
- Key differentiators between skill and baselines
- Limitations and caveats
