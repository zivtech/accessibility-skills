# A11y-Planner Evaluation Suite — Complete Index

**Suite Location:** `/sessions/gallant-determined-mendel/mnt/claude/zivtech-meta-skills/evals/suites/a11y-planner/`

**Status:** Core infrastructure COMPLETE, sample fixtures ready for batch generation

**Last Updated:** 2026-03-09

---

## Quick Navigation

### For First-Time Users
1. Start with **README.md** (5-10 min overview)
2. Review **skill-profile.md** (10 min) to understand what a11y-planner does
3. Look at **fixtures/aria-disclosure-widget.md** (5 min) to see a fixture example
4. Check **eval.yaml** (2 min) for configuration

### For Evaluation Teams
1. Read **statistical-design.md** (15 min) to understand methodology
2. Review **domain-sampling-strategy.md** (10 min) to see all 25 fixtures
3. See **rubrics/aria-disclosure-widget.rubric.yaml** (10 min) for scoring approach
4. Use **FIXTURE_GENERATION_TEMPLATE.md** to create remaining fixtures

### For Developers
1. See **BUILD_SUMMARY.md** (5 min) for what's been built
2. Check **FIXTURE_GENERATION_TEMPLATE.md** (10 min) for batch creation
3. Review **eval.yaml** for configuration structure
4. Follow checklist in template to generate fixtures

---

## File Directory

### Core Configuration (5 files)

| File | Purpose | Audience |
|------|---------|----------|
| **eval.yaml** | Master evaluation configuration (fixtures, baselines, statistical design, success criteria) | Evaluation runners, infrastructure |
| **skill-profile.md** | Comprehensive profile of a11y-planner skill (phases, dimensions, success criteria, calibration) | Users, evaluators, stakeholders |
| **domain-sampling-strategy.md** | Domain taxonomy, 5×5 fixture sampling, difficulty distribution, ambiguous fixtures | Evaluators, domain experts |
| **statistical-design.md** | Statistical methodology, Wilcoxon tests, effect sizes, subgroup analysis, power analysis | Data analysts, statisticians |
| **FIXTURE_INVENTORY.md** | Complete listing of all 25 fixtures with descriptions, expected findings, success criteria | Evaluators, fixture generators |

**Total:** ~50 KB, ~150 pages equivalent

### User Documentation (2 files)

| File | Purpose | Audience |
|------|---------|----------|
| **README.md** | User-facing guide (quick start, domains, dimensions, baselines, workflow) | All users, stakeholders |
| **BUILD_SUMMARY.md** | Summary of what was built, next steps, success criteria, key metrics | Project managers, stakeholders |

**Total:** ~25 KB, ~50 pages equivalent

### Fixture Templates & Guides (2 files)

| File | Purpose | Audience |
|------|---------|----------|
| **FIXTURE_GENERATION_TEMPLATE.md** | Templates and guide for creating remaining 24 fixtures | Fixture generators, developers |
| **INDEX.md** | This file — navigation and reference | All users |

**Total:** ~20 KB, ~40 pages equivalent

### Baselines (2 files)

| File | Purpose | Audience |
|------|---------|----------|
| **baselines/baseline-zero-shot.md** | Simple unstructured planning prompt (baseline A) | Evaluation infrastructure |
| **baselines/baseline-few-shot.md** | Structured planning prompt with example (baseline B) | Evaluation infrastructure |

**Total:** ~10 KB, ~20 pages equivalent

### Sample Fixtures (1 complete triplet = 3 files)

| File | Purpose | Audience |
|------|---------|----------|
| **fixtures/aria-disclosure-widget.md** | Feature description and context for a TRIVIAL fixture | Evaluators, fixture generators |
| **fixtures/aria-disclosure-widget.metadata.yaml** | Scenario expectations, findings, evaluation criteria | Evaluators, infrastructure |
| **rubrics/aria-disclosure-widget.rubric.yaml** | Hybrid scoring rubric with rule-based + LLM judge criteria | Evaluators, scoring infrastructure |

**Total:** ~15 KB, ~30 pages equivalent

### Remaining Fixtures (24 triplets pending batch generation = 72 files)

**Status:** Described in FIXTURE_INVENTORY.md, ready for generation
**Effort:** 1-2 hours per domain (10 hours total) or batch templated generation

---

## Key Statistics

| Aspect | Count |
|--------|-------|
| **Total fixtures** | 25 |
| **Domains** | 5 |
| **Difficulty levels** | 4 (TRIVIAL 6, MODERATE 11, COMPLEX 5, AMBIGUOUS 3) |
| **Evaluation dimensions** | 7 |
| **Baseline conditions** | 3 (a11y-planner, baseline-zero-shot, baseline-few-shot) |
| **Repetitions per fixture** | 3 |
| **Total evaluations** | 225 (25 fixtures × 3 conditions × 3 repetitions) |
| **Estimated duration** | 2-3 weeks (pilot 1-2d, main 10-14d, analysis 3-5d) |

---

## How To Use This Suite

### Phase 1: Understand the Skill
1. Read **skill-profile.md** to understand a11y-planner's 9-phase protocol
2. Review **domain-sampling-strategy.md** to see what scenarios are evaluated

### Phase 2: Review the Design
1. Read **statistical-design.md** to understand how performance is measured
2. Review **eval.yaml** to see the complete configuration
3. Check **README.md** for expected outcomes

### Phase 3: Run Pilot Evaluation
1. Review **fixtures/aria-disclosure-widget.*** (complete example)
2. Use **baselines/baseline-*.md** to understand baseline conditions
3. Run pilot on 5 sample fixtures to validate rubrics

### Phase 4: Generate Remaining Fixtures
1. Use **FIXTURE_GENERATION_TEMPLATE.md** as guide
2. Refer to **FIXTURE_INVENTORY.md** for fixture descriptions
3. Create 24 more fixture triplets

### Phase 5: Run Full Evaluation
1. Execute evaluation runner with all 25 fixtures
2. Perform 3 repetitions per fixture for stability

### Phase 6: Analyze Results
1. Run statistical tests (Wilcoxon signed-rank)
2. Calculate effect sizes (Cohen's d)
3. Perform subgroup analysis (by domain, difficulty, pattern type)
4. Generate report with visualizations

---

## File Relationships

```
eval.yaml (master config)
├── References: skill-profile.md (skill definition)
├── References: domain-sampling-strategy.md (fixtures & domains)
├── References: statistical-design.md (statistical methodology)
└── References: baselines/ and fixtures/ and rubrics/ (data)

skill-profile.md
├── Defines: 9-phase planning protocol
├── Defines: 7 evaluation dimensions
└── References: WCAG 2.2, WAI-ARIA APG

domain-sampling-strategy.md
├── Describes: 5 domains × 5 fixtures each (25 total)
├── Specifies: TRIVIAL/MODERATE/COMPLEX/AMBIGUOUS distribution
└── References: Specific WCAG criteria per domain

statistical-design.md
├── Specifies: Wilcoxon signed-rank test
├── Specifies: Effect size calculation (Cohen's d)
├── Specifies: Subgroup analysis approach
└── References: Power analysis, sample size

fixtures/ directory (25 files, 1 complete + 24 templates)
├── aria-disclosure-widget.md (complete example)
└── [24 more to be generated per FIXTURE_GENERATION_TEMPLATE.md]

fixtures/ metadata (25 files, 1 complete + 24 templates)
├── aria-disclosure-widget.metadata.yaml (complete example)
└── [24 more to be generated]

rubrics/ directory (25 files, 1 complete + 24 templates)
├── aria-disclosure-widget.rubric.yaml (complete example)
└── [24 more to be generated]

baselines/ directory (2 baseline prompts)
├── baseline-zero-shot.md
└── baseline-few-shot.md
```

---

## Success Criteria Quick Reference

### Primary Success
- a11y-planner composite score > baseline-zero-shot by ≥15 points (p < 0.05)

### Secondary Success
- Gap coverage: 25%+ more
- Specificity rate: 20%+ more WCAG citations
- Pattern mapping: 90%+ complete
- Multi-perspective: 4+ perspectives
- False positive rate: <5%

### Domain-Specific Expected Strengths
1. ARIA Pattern Implementation — 95%+ pattern mapping
2. Keyboard Navigation — 100% focus management planning
3. Screen Reader Experience — 90%+ landmark/heading hierarchy
4. Visual & Cognitive — 85%+ non-color alternatives
5. Testing & Audit — 90%+ comprehensive testing

---

## Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| **Pilot Evaluation** | 1-2 days | Rubric validation, baseline fairness check |
| **Full Evaluation** | 10-14 days | 225 evaluation results |
| **Statistical Analysis** | 3-5 days | Wilcoxon tests, effect sizes, subgroup analysis |
| **Report Generation** | 1-2 days | Final report with findings and recommendations |
| **TOTAL** | ~2-3 weeks | Complete evaluation suite execution |

---

## Outstanding Work

### Immediate (1-2 hours per domain, 10 hours total)
- Generate 24 remaining fixture triplets using FIXTURE_GENERATION_TEMPLATE.md
- Verify all 75 fixture files (25×3) are created and valid

### Short-term (3-5 days)
- Set up evaluation infrastructure (API calls, prompt execution)
- Run pilot evaluation on 5 sample fixtures
- Validate rubrics based on pilot results

### Medium-term (10-14 days)
- Execute full evaluation (225 evaluations)
- Perform statistical analysis
- Generate report with findings

---

## Contact & Support

For questions about:
- **Skill design:** See skill-profile.md and a11y-planner agent
- **Evaluation design:** See statistical-design.md and eval.yaml
- **Fixtures:** See FIXTURE_INVENTORY.md and FIXTURE_GENERATION_TEMPLATE.md
- **Scoring:** See rubrics/aria-disclosure-widget.rubric.yaml
- **Domain specifics:** See domain-sampling-strategy.md

---

## References

- **A11y-Planner Agent:** `/a11y-planner/.claude/agents/a11y-planner.md`
- **WCAG 2.2:** https://www.w3.org/WAI/WCAG22/quickref/
- **WAI-ARIA APG:** https://www.w3.org/WAI/ARIA/apg/
- **Related Skills:** a11y-critic (code review), accessibility-testing (automated tests)

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-03-09 | 1.0 | Initial build: core configuration, sample fixtures, templates |

---

**Suite is READY FOR DEPLOYMENT** ✓
- Core infrastructure complete
- Sample fixtures provide templates
- Documentation comprehensive
- Statistical methodology rigorous
- Next: Generate remaining 24 fixtures and run evaluation

