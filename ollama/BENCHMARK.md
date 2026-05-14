# Ollama A11y-Critic Benchmark Results

**Date**: 2026-05-14
**Protocol**: Full 10-phase a11y-critic Investigation Protocol (single-shot, no orchestration)
**System prompt**: ~40K chars (Role + Investigation_Protocol + Severity_Scale + Output_Format from SKILL.md)
**Scoring**: `ollama/score_output.py` against graded fixture rubrics

## Models Tested

| Model | Size | Tier |
|-------|------|------|
| llama3.3:70b | 39.6 GB | Tier 1 (full protocol) |
| qwen3:32b | 18.8 GB | Tier 2 (compressed) |
| *Claude Opus 4.6* | *cloud* | *Baseline (TODO)* |

## Fixture 1: form-validation-missing-aria-describedby

**Difficulty**: HAS-BUGS | **Must-find**: 2 | **Should-find**: 1 | **Expected verdict**: REVISE

| Metric | llama3.3:70b | qwen3:32b | Claude (TODO) |
|--------|-------------|-----------|---------------|
| Must-find detection | 2/2 (100%) | 2/2 (100%) | |
| Should-find detection | 1/1 (100%) | 1/1 (100%) | |
| Verdict | REVISE ✓ | REVISE ✓ | |
| Phases followed | 11/11 | 0/11 | |
| WCAG citations | Names only | Numbers ✓ | |
| Response chars | 7,486 | 3,652 | |
| Tokens generated | 1,463 | 1,581 | |
| Generation time | 350s | 508s | |
| **Status** | **PASS** | **PASS** | |

### Must-find items:
1. Error messages not associated with form inputs via aria-describedby — **Both found**
2. Error summary not announced as dynamic content update — **Both found**

### Should-find items:
1. Error summary doesn't provide links to associated fields — **Both found**

## Fixture 2: tabs-missing-arrow-nav

**Difficulty**: HAS-BUGS | **Must-find**: 1 | **Should-find**: 1 | **Expected verdict**: REVISE

| Metric | llama3.3:70b | qwen3:32b | Claude (TODO) |
|--------|-------------|-----------|---------------|
| Must-find detection | 1/1 (100%) | 1/1 (100%) | |
| Should-find detection | 1/1 (100%) | 1/1 (100%) | |
| Verdict | REVISE ✓ | REVISE ✓ | |
| Phases followed | 11/11 | 0/11 | |
| WCAG citations | Numbers ✓ | Numbers ✓ | |
| Response chars | 8,243 | 3,679 | |
| Tokens generated | ~1,500 (est) | 1,694 | |
| Generation time | ~350s (est) | 303s | |
| **Status** | **PASS** | **PASS** | |

### Must-find items:
1. Arrow key navigation not implemented for tab cycling — **Both found**

### Should-find items:
1. Active tab not focused after keyboard selection — **Both found**

## Fixture 3: toast-notification-no-role

**Difficulty**: HAS-BUGS | **Must-find**: 4 | **Should-find**: 0 | **Expected verdict**: REVISE

| Metric | llama3.3:70b | qwen3:32b | Claude (TODO) |
|--------|-------------|-----------|---------------|
| Must-find detection | 3/4 (75%) | 3/4 (75%) | |
| Verdict | REVISE ✓ | REVISE ✓ | |
| Phases followed | 11/11 | 0/11 | |
| WCAG citations | Partial | Numbers ✓ | |
| Response chars | 7,483 | 4,031 | |
| Tokens generated | ~1,500 (est) | 1,540 | |
| Generation time | ~350s (est) | 171s | |
| **Status** | **PASS** | **PASS** | |

### Must-find items:
1. Missing role='alert' — **Both MISSED** (X)
2. Missing aria-live='assertive' — **Both found**
3. No way for keyboard user to dismiss toast — **Both found**
4. Message not labeled or described — **Both found**

**Note**: Both models missed the same item (`role="alert"`) but caught `aria-live`. This is a rubric overlap — `aria-live="assertive"` functionally covers the same semantic as `role="alert"`. The miss may reflect the rubric double-counting rather than a true blind spot.

## Abort Threshold

- **Gate**: < 40% must-find detection rate across all fixtures
- **Claude baseline needed** to calibrate — if Claude scores 80%, 40% is a real gate; if Claude scores 60%, 40% is permissive

## CLEAN Fixture Results (False Positive Test)

**Purpose**: Verify models don't manufacture false positives on correctly implemented components.
**Scoring**: Correct verdict (ACCEPT or ACCEPT-WITH-RESERVATIONS) + no structured findings at CRITICAL/SERIOUS.

### Fixture 4: button-skip-link-clean

**Difficulty**: CLEAN | **Must-find**: 0 | **Expected verdict**: ACCEPT

| Metric | llama3.3:70b | qwen3:32b |
|--------|-------------|-----------|
| Verdict | ACCEPT | ACCEPT-WITH-RESERVATIONS |
| Verdict correct | YES | YES |
| False positives | 0 | 0 |
| Phases followed | 11/11 | 0/11 |
| **Status** | **PASS** | **PASS** |

### Fixture 5: interactive-dropdown-clean

**Difficulty**: CLEAN | **Must-find**: 0 | **Expected verdict**: ACCEPT

| Metric | llama3.3:70b | qwen3:32b |
|--------|-------------|-----------|
| Verdict | ACCEPT | ACCEPT-WITH-RESERVATIONS |
| Verdict correct | YES | YES |
| False positives | 0 | 0 |
| Phases followed | 11/11 | 0/11 |
| **Status** | **PASS** | **PASS** |

### Fixture 6: modal-complete-clean

**Difficulty**: CLEAN | **Must-find**: 0 | **Expected verdict**: ACCEPT

| Metric | llama3.3:70b | qwen3:32b |
|--------|-------------|-----------|
| Verdict | ACCEPT | ACCEPT |
| Verdict correct | YES | YES |
| False positives | 0 | 0 |
| Phases followed | 11/11 | 0/11 |
| **Status** | **PASS** | **PASS** |

### Fixture 7: search-results-dynamic-clean

**Difficulty**: CLEAN | **Must-find**: 0 | **Expected verdict**: ACCEPT

| Metric | llama3.3:70b | qwen3:32b |
|--------|-------------|-----------|
| Verdict | ACCEPT | ACCEPT |
| Verdict correct | YES | YES |
| False positives | 0 | 0 |
| Phases followed | 11/11 | 0/11 |
| **Status** | **PASS** | **PASS** |

## Summary

### HAS-BUGS Fixtures (Detection Accuracy)

| Model | Fixtures | Must-find rate | Verdict accuracy | Phase compliance |
|-------|----------|---------------|------------------|-----------------|
| llama3.3:70b | 3/3 | 6/7 (86%) | 3/3 (100%) | 33/33 phases |
| qwen3:32b | 3/3 | 6/7 (86%) | 3/3 (100%) | 0/33 phases |

### CLEAN Fixtures (False Positive Rate)

| Model | Fixtures | Correct verdict | False positives |
|-------|----------|----------------|-----------------|
| llama3.3:70b | 4/4 | 4/4 (100%) | 0 |
| qwen3:32b | 4/4 | 4/4 (100%) | 0 |

### Model Comparison

| Dimension | llama3.3:70b | qwen3:32b |
|-----------|-------------|-----------|
| Must-find accuracy | 86% | 86% |
| False positive rate | 0% (4 fixtures) | 0% (4 fixtures) |
| Phase compliance | Full (11/11 every time) | None (skips to output) |
| WCAG citation quality | Inconsistent (names sometimes, numbers sometimes) | Consistent (criterion numbers) |
| Response verbosity | ~7,500 chars avg (HAS-BUGS), ~5,500 avg (CLEAN) | ~3,800 chars avg (HAS-BUGS), ~2,500 avg (CLEAN) |
| Generation speed | ~350-500s per fixture | ~170-500s per fixture |
| Model size | 39.6 GB | 18.8 GB |

**Note**: Generation speed varies significantly with memory pressure. When both models are loaded simultaneously (74 GB total), swap pressure causes 2-3x slowdowns. Running one model at a time is recommended on 128 GB systems.

### Key Findings

1. **Phase-prompted orchestrator is unnecessary.** Both models produce correct findings in single-shot mode with the full protocol as system prompt. llama3.3 follows all phases; qwen3 skips phases but gets the same results.

2. **Both models hit the same ceiling on the hardest fixture.** 3/4 must-find on toast (both missed `role="alert"` while finding `aria-live`). This appears to be rubric overlap rather than a true blind spot.

3. **Zero false positives on CLEAN fixtures.** Both models correctly identify well-implemented components and produce ACCEPT/ACCEPT-WITH-RESERVATIONS verdicts without manufacturing findings.

4. **qwen3:32b is the better value proposition for Tier 2.** Half the model size, same detection rate, better WCAG citations, more concise output. The only trade-off is no phase structure in output.

5. **Architecture decision: ship a simple wrapper, not an orchestrator.** A Python script that sends the full SKILL.md protocol as system prompt and the fixture as user prompt is sufficient. No per-phase state management needed.

## Planner Results

**Protocol**: Full a11y-planner SKILL.md (71K chars) as system prompt, fixture description as user prompt.
**Scoring**: Key section presence check against fixture rubric criteria.

### Fixture 8: aria-modal-form-validation (AMBIGUOUS difficulty)

| Metric | llama3.3:70b | qwen3:32b |
|--------|-------------|-----------|
| Key sections | 13/15 | **15/15** |
| APG pattern URL | Yes | Yes |
| Focus trap plan | Yes | Yes |
| Focus restoration | Yes | Yes |
| aria-modal/labelledby | Yes | Yes |
| aria-invalid/describedby | Yes | Yes |
| fieldset/legend | Yes | Yes |
| Live region plan | Yes | Yes |
| HTML stubs | Yes | Yes |
| WCAG 2.1.1 citation | **No** | Yes |
| WCAG 4.1.2 citation | **No** | Yes |
| Response chars | 6,059 | 12,405 |
| Generation time | 591s | ~710s |

### Fixture 9: keyboard-roving-tabindex (MODERATE difficulty)

| Metric | llama3.3:70b | qwen3:32b |
|--------|-------------|-----------|
| Key sections | **8/8** | **8/8** |
| Roving tabindex plan | Yes | Yes |
| Arrow key navigation | Yes | Yes |
| APG pattern reference | Yes | Yes |
| WCAG 2.1.1 citation | Yes | Yes |
| Grid/menu structure | Yes | Yes |
| HTML stubs | Yes | Yes |
| Response chars | 4,488 | 7,704 |
| Generation time | ~610s | ~500s |

### Planner Summary

| Model | Fixture | Score |
|-------|---------|-------|
| llama3.3:70b | Modal (complex) | 13/15 |
| llama3.3:70b | Keyboard (focused) | 8/8 |
| qwen3:32b | Modal (complex) | **15/15** |
| qwen3:32b | Keyboard (focused) | **8/8** |

qwen3:32b produced perfect plans on both fixtures with explicit WCAG citations. llama3.3 missed criterion numbers on the complex fixture but covered all structural elements.

## Full Summary

### a11y-critic (7 fixtures)

| Model | HAS-BUGS must-find | CLEAN false positives | Verdict accuracy |
|-------|-------------------|----------------------|------------------|
| llama3.3:70b | 6/7 (86%) | 0/4 (0%) | 7/7 (100%) |
| qwen3:32b | 6/7 (86%) | 0/4 (0%) | 7/7 (100%) |

### a11y-planner (2 fixtures)

| Model | Complex fixture | Focused fixture |
|-------|----------------|-----------------|
| llama3.3:70b | 13/15 (87%) | 8/8 (100%) |
| qwen3:32b | 15/15 (100%) | 8/8 (100%) |

### Model Comparison

| Dimension | llama3.3:70b | qwen3:32b |
|-----------|-------------|-----------|
| Critic must-find accuracy | 86% | 86% |
| Critic false positive rate | 0% | 0% |
| Planner section coverage | 87-100% | 100% |
| Phase compliance | Full (11/11 every time) | None (skips to output) |
| WCAG citation quality | Inconsistent | Consistent (criterion numbers) |
| Response verbosity | ~5,000-7,500 chars | ~2,500-12,400 chars |
| Generation speed | ~350-600s per fixture | ~170-710s per fixture |
| Model size | 39.6 GB | 18.8 GB |

**Note**: Generation speed varies significantly with memory pressure. When both models are loaded simultaneously (74 GB total), swap pressure causes 2-3x slowdowns on 128 GB systems. Run one model at a time.

### Key Findings

1. **Phase-prompted orchestrator is unnecessary.** Both models produce correct findings in single-shot mode with the full protocol as system prompt.

2. **Both models hit the same ceiling on the hardest critic fixture.** 3/4 must-find on toast (both missed `role="alert"` while finding `aria-live`). Likely rubric overlap.

3. **Zero false positives on CLEAN fixtures.** Both models correctly identify well-implemented components without manufacturing findings.

4. **qwen3:32b is the recommended model.** Half the size, same or better accuracy, better WCAG citations, perfect planner scores. The only trade-off is no phase structure in critic output.

5. **a11y-planner works on local models.** Both models produce usable accessibility plans with APG pattern references, focus management plans, ARIA attribute specifications, and HTML stubs.

6. **Architecture: simple wrapper, not orchestrator.** A Python script that sends the full SKILL.md as system prompt is sufficient. No per-phase state management needed.

## Wrapper

`ollama/ollama_a11y.py` — supports critic, planner, and perspective-audit skills. See `ollama/README.md`.

## Next Steps

- [x] ~~Build simple `ollama_a11y.py` wrapper (not orchestrator)~~
- [x] ~~Test on CLEAN fixtures (verify models don't manufacture false positives)~~ — 8/8 PASS
- [x] ~~Test a11y-planner protocol on both models~~ — both viable, qwen3 perfect
- [ ] Test perspective-audit protocol on both models
- [ ] Establish Claude baseline (optional)
- [ ] Test on additional models (deepseek-r1:70b, qwen3.5:27b)
