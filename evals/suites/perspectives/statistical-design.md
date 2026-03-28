# Perspective Agents — Statistical Design

## Hypothesis

**H1:** Adding 7 explicit access perspectives via the hybrid model (lightweight hints + escalated companion audit) produces more findings in under-covered dimensions without reducing quality in already-strong dimensions.

**H1a (structured vs named):** The structured JTBD/escalation approach (condition C) outperforms simply naming the dimensions (condition B), isolating the value of the structured checklist protocol.

## Conditions

| Condition | Description |
|---|---|
| A — Current | a11y-planner + a11y-critic + a11y-test without perspective enhancements |
| B — Strong generic | Current skills + "also review for auditory, vestibular, cognitive, and contrast accessibility" appended to prompt |
| C — Enhanced | Enhanced skills with perspective hints + perspective-audit companion |

A vs C measures whether perspectives help at all. B vs C isolates whether the structured JTBD approach helps beyond simply naming the dimensions.

## Sample Size and Power

- **n = 25 fixtures** (matching existing a11y-critic eval suite standard)
- **3 repeats** per fixture per condition
- **Total evaluations:** 25 x 3 conditions x 3 repeats = 225
- **Power:** ~80% for medium effect (d = 0.5) at alpha = 0.05 with Wilcoxon signed-rank
- **Pilot:** 5 fixtures first to validate scoring methodology

## Fixture Composition

| Category | Count | Purpose |
|---|---|---|
| HAS-BUGS (new dimensions) | 10 | Planted issues in auditory, vestibular, cognitive, contrast |
| HAS-BUGS (existing dimensions) | 6 | Planted issues in keyboard, screen reader, ARIA — regression detection |
| CLEAN | 5 | New dimensions satisfied — false positive measurement |
| ADVERSARIAL | 4 | Subtle perspective-specific issues requiring deep reasoning |
| **Total main** | **25** | |
| Calibration | 5 | Alarm-level accuracy (escalation mechanism validation) |

### Fixture Sourcing

- At least 50% from external accessibility audit failures (WebAIM survey patterns, Deque case studies, real GitHub issues)
- Remaining designed independently from JTBD tables to prevent data leakage
- No fixture reused from the a11y-critic eval suite

## Metrics

| # | Metric | Method | Target |
|---|---|---|---|
| 1 | Precision-weighted coverage | Rule-based: cited WCAG vs planted ground truth | C >= 1.3x A |
| 2 | New-dimension precision | LLM judge against rubric | C >= 80% |
| 3 | New-dimension recall | Rule-based against ground truth | C >= 70% |
| 4 | Existing-dimension TPR | Rule-based against ground truth | C >= A (no regression) |
| 5 | False positive rate | LLM judge against rubric | C <= A + 10% |
| 6 | Actionability | Rule-based: 4-point checklist per finding | C >= 85% |
| 7 | Escalation accuracy | Rule-based: exact match or +/-1 level | >= 80% exact, >= 95% within +/-1 |

## Statistical Tests

**Primary:** Wilcoxon signed-rank (non-parametric paired comparison)
- Paired on fixture: each fixture scored under all 3 conditions
- One-tailed for A vs C (H1: C > A)
- Two-tailed for B vs C (H1a: C != B)

**Multiple comparisons:** Bonferroni correction across 7 metrics (adjusted alpha = 0.007)

**Effect size:** Cohen's d (or r = Z/sqrt(N) for non-parametric)

**Confidence intervals:** Bootstrap with B = 1000

**Repeats:** 3 per fixture per condition. Report mean scores with within-fixture SD. Use mean fixture score as the unit of analysis for Wilcoxon.

## Scoring Method

Hybrid — 70% rule-based, 30% LLM judge.

**Rule-based (0.7 weight):**
- WCAG criteria matching: cited criteria vs planted-issues ground truth
- Element reference detection: does finding include file:line or specific element?
- Actionability checklist: element ref + problem description + user group + fix suggestion
- Alarm-level accuracy: exact match against expected levels

**LLM judge (0.3 weight):**
- Model: claude-sonnet-4-6, temperature 0
- Finding quality: is the finding description accurate and useful?
- False positive adjudication: does the finding correspond to a real issue?
- Rubric: per-fixture rubric.yaml with expected findings and scoring thresholds

## Calibration Fixtures (Escalation Validation)

5 fixtures with documented expected alarm levels per perspective (35 total assessments):

| Fixture | HIGH | MEDIUM | LOW |
|---|---|---|---|
| C1. Static blog post | — | Screen Reader, Cognitive | Magnification, Contrast, Vestibular, Auditory, Keyboard |
| C2. Login form with CAPTCHA | Cognitive, Keyboard | Screen Reader | Magnification, Contrast, Vestibular, Auditory |
| C3. Video tutorial page | Auditory, Screen Reader | Cognitive, Keyboard | Magnification, Vestibular, Contrast |
| C4. Animated dashboard | Vestibular, Contrast, Keyboard, Screen Reader | Magnification, Cognitive | Auditory |
| C5. Drag-and-drop kanban | Keyboard, Cognitive | Screen Reader, Magnification | Vestibular, Auditory, Contrast |

Scoring: exact match = 1.0, within +/-1 level = 0.5, off by 2 levels = 0.0.

## Reproducibility

- Model version: pin to claude-opus-4-6
- Temperature: 0 for all conditions
- Seed: not available for Claude API; rely on 3 repeats for variance measurement
- All fixture files, rubrics, and baselines versioned in this repository

## Success Criteria

The enhancement is validated if (at Bonferroni-corrected alpha = 0.007):

1. Precision-weighted coverage: C >= 1.3x A (significant improvement)
2. New-dimension precision >= 80% (findings are real)
3. New-dimension recall >= 70% (planted issues found)
4. Existing-dimension TPR: C >= A at -5% non-inferiority (no regression)
5. False positive rate: C <= A + 10% (precision preserved)
6. Actionability >= 85% (findings usable)
7. Escalation accuracy >= 80% exact match on calibration fixtures
