# Perspective Agents Evaluation Suite

Evaluation infrastructure for the perspective-audit skill and the perspective enhancements to a11y-planner, a11y-critic, and a11y-test.

## Suite Overview

**Skills:** a11y-planner (enhanced), a11y-critic (enhanced), a11y-test (enhanced), perspective-audit (new)

**Model:** claude-opus-4-6

**Hypothesis:** Adding 7 explicit access perspectives via the hybrid model (lightweight hints + escalated companion audit) produces more findings in under-covered dimensions without reducing quality in already-strong dimensions.

## Directory Structure

```
perspectives/
├── fixtures/
│   ├── video-tutorial-no-captions.md
│   ├── video-tutorial-no-captions.metadata.yaml
│   ├── product-carousel-autoplay.md
│   ├── product-carousel-autoplay.metadata.yaml
│   ├── article-page-clean.md
│   ├── article-page-clean.metadata.yaml
│   ├── checkout-form-broken-errors.md
│   ├── checkout-form-broken-errors.metadata.yaml
│   ├── color-only-status-indicators.md
│   ├── color-only-status-indicators.metadata.yaml
│   └── ... (25 total)
│
├── rubrics/
│   ├── video-tutorial-no-captions.rubric.yaml
│   ├── product-carousel-autoplay.rubric.yaml
│   └── ... (rubric for each fixture)
│
├── calibration/
│   ├── calibration-static-blog.md
│   ├── calibration-static-blog.metadata.yaml
│   ├── calibration-login-captcha.md
│   ├── calibration-login-captcha.metadata.yaml
│   ├── calibration-video-tutorial.md
│   ├── calibration-video-tutorial.metadata.yaml
│   └── ... (5 total)
│
├── baselines/
│   ├── baseline-A-current.md
│   └── baseline-B-strong-generic.md
│
├── skill-profile.md
├── domain-sampling-strategy.md
├── statistical-design.md
├── eval.yaml
└── README.md (this file)
```

## Three-Condition Design

| Condition | Description |
|---|---|
| A — Current | a11y-planner + a11y-critic + a11y-test without perspective enhancements |
| B — Strong generic | Current skills + "also review for auditory, vestibular, cognitive, and contrast accessibility" |
| C — Enhanced | Enhanced skills with perspective hints + perspective-audit companion |

A vs C: Do perspectives help at all?
B vs C: Does the structured JTBD approach help beyond naming the dimensions?

## Fixture Composition (25 main + 5 calibration)

| Category | Count | Purpose |
|---|---|---|
| HAS-BUGS (new dimensions) | 10 | Auditory, vestibular, cognitive, contrast issues |
| HAS-BUGS (existing dimensions) | 6 | Keyboard, screen reader, ARIA — regression detection |
| CLEAN | 5 | False positive measurement |
| ADVERSARIAL | 4 | Subtle perspective-specific issues |
| Calibration | 5 | Alarm-level accuracy (escalation validation) |

## Pilot Fixtures (5 main + 3 calibration)

| Fixture | Category | Primary Perspective |
|---|---|---|
| video-tutorial-no-captions | HAS-BUGS (new) | Auditory |
| product-carousel-autoplay | HAS-BUGS (new) | Vestibular |
| article-page-clean | CLEAN | All (false positive test) |
| checkout-form-broken-errors | HAS-BUGS (existing) | Screen Reader |
| color-only-status-indicators | ADVERSARIAL | Contrast |
| calibration-static-blog | Calibration | LOW baseline |
| calibration-login-captcha | Calibration | HIGH Cognitive/Keyboard |
| calibration-video-tutorial | Calibration | HIGH Auditory/SR |

## Metrics

| Metric | Target | Method |
|---|---|---|
| Precision-weighted coverage | C >= 1.3x A | Rule-based |
| New-dimension precision | C >= 80% | LLM judge |
| New-dimension recall | C >= 70% | Rule-based |
| Existing-dimension TPR | C >= A (no regression) | Rule-based |
| False positive rate | C <= A + 10% | LLM judge |
| Actionability | C >= 85% | Rule-based |
| Escalation accuracy | >= 80% exact match | Rule-based |

## Running the Evaluation

### Pilot (validate methodology)

1. Run 5 pilot main fixtures + 3 calibration fixtures
2. Validate rubrics are unambiguous
3. Validate baselines are fair (not strawmen)
4. Validate fixtures discriminate across conditions
5. Validate variance is reasonable

### Full Run

1. Run all 25 fixtures x 3 conditions x 3 repeats = 225 evaluations
2. Run 5 calibration fixtures x 3 repeats = 15 escalation assessments
3. Analyze with Wilcoxon signed-rank, Bonferroni correction
4. Report effect sizes, confidence intervals, subgroup analysis

## Key Files

| File | Purpose |
|---|---|
| [eval.yaml](./eval.yaml) | Harness configuration |
| [statistical-design.md](./statistical-design.md) | Power analysis, hypothesis testing |
| [skill-profile.md](./skill-profile.md) | Skills under test, architecture, differentiators |
| [domain-sampling-strategy.md](./domain-sampling-strategy.md) | Fixture allocation, sourcing, coverage |
| [baselines/](./baselines/) | Condition A and B prompts |
| [fixtures/](./fixtures/) | Main fixture artifacts and metadata |
| [rubrics/](./rubrics/) | Per-fixture scoring rubrics |
| [calibration/](./calibration/) | Alarm-level accuracy fixtures |

## Status

**Current:** Pilot infrastructure complete — 5 pilot fixtures + 3 calibration fixtures ready. Foundational files (eval.yaml, statistical design, baselines, skill profile, domain sampling) complete.

**Next:** Run pilot, validate methodology, then build remaining 20 main fixtures + 2 calibration fixtures.
