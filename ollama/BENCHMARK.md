# A11y Model Benchmark Results

**Date**: 2026-05-14 (initial), 2026-05-15 (Phase 4A full benchmark), 2026-05-19 (cross-platform baselines)
**Protocol**: Full 11-phase a11y-critic Investigation Protocol (Phase 0 + Phases 1-10, single-shot, no orchestration)
**System prompt**: ~40K chars (Role + Investigation_Protocol + Severity_Scale + Output_Format from SKILL.md)
**Scoring**: `ollama/score_output.py` against graded fixture rubrics

## Baseline Families

This file began as an Ollama benchmark log and now serves as the cross-model benchmark record. Keep Claude, Codex/OpenAI, Gemini, and local models as peer baseline families when result artifacts exist.

| Family | Models / Tiers in committed results | Status |
|--------|-------------------------------------|--------|
| Claude API | Opus 4.6, Sonnet 4.6, Sonnet 4.6 + thinking, Haiku 4.5 | 33-fixture escalation complete |
| Codex/OpenAI | GPT-5.2, GPT-5.2 low, GPT-5.5, GPT-5.5 low | 33-fixture escalation complete |
| Ollama local | qwen3:32b, qwen3.5:27b, llama3.3:70b, qwen3.5:latest, deepseek-r1:70b probe | Critic, planner, and perspective coverage varies by model |
| Gemini / other hosted | Add rows when raw results are committed | In scope; not represented by committed result tables in this file |

The first fixture tables below are historical Phase 4 local-model rows. Hosted results were added later in Phases 5-7.

> **Blind-protocol disclosure (2026-07-13).** Every critic- and perspective-suite row recorded before
> 2026-07-13 ran **non-blind**: both runners' `load_fixture()` embedded the fixture's full
> `## Accessibility Issues (Planted Bugs)` answer section in the prompt (truncation logic never
> existed — verified via `git log -S`). The planner suite is exempt (its fixtures carry no answer
> sections — verified). Runners now strip the answer key (post-003; regression guard:
> `ollama/test_blind_prompts.py`), so pre- and post-2026-07-13 rows are not comparable; treat the
> historical critic/perspective numbers as non-blind upper bounds pending blind re-runs. The first
> blind lane is the Claude subagent perspective run (2026-07-13, section below). **Blind local
> re-runs landed the same day** (qwen3:32b, full critic + perspective suites; see "Ollama blind
> re-run lane" below): the critic-suite numbers are blind-confirmed, but the perspective-suite
> CLEAN false-positive resistance was answer-key-dependent — the historical CLEAN rows for local
> models overstate it. Structural note: critic CLEAN fixtures carry no answer sections (their
> prompts were identical all along); all 5 perspective CLEAN fixtures do.
>
> **2026-07-16 amendment:** "identical all along" must not be read as *unhinted* — all 4 critic
> CLEAN fixtures carried "should receive a clean verdict / ACCEPT" prose in their model-visible
> body, so critic CLEAN rows measured hint-following as much as calibrated false-positive
> avoidance. Additionally, `modal-complete-clean` carried two real unplanted defects until
> 2026-07-16 (fixed at source; hint prose moved below the strip boundary for that fixture).
> See Scoring changelog → 2026-07-16 fixture erratum.

> **Hint-comment disclosure (2026-07-16).** Independent of the answer-key leak above, fixture
> *code blocks* carried inline planted-bug hint comments (`// BUG: …`, `{/* BUG: … */}`, bare
> `BUG:` lines inside block comments, and a handful of unmarked defect-stating comments) that
> answer-key stripping never touched: **24 of 33 critic fixtures** carried `BUG`-marked hints
> (25 counting `dashboard-heading-inconsistency`, whose comments state each planted flaw without
> the token) and **20 of 25 perspective fixtures** did. Every prompt-based lane in this file —
> **including the 2026-07-13 blind lanes** — saw those hints. Direction of bias: the hints name
> the planted defects (often with the exact attribute or WCAG SC the rubric keys on), so
> must-find/detection rates and PASS verdicts on hinted fixtures are **hint-assisted upper
> bounds** pending de-hinted re-runs (first such re-run: qwen3:32b, 2026-07-16 — see the
> de-hinted lane section at the end of this file). Not affected by *hints* (but see the follow-up
> disclosure below — critic CLEAN and ADVERSARIAL prompts carried their expected verdicts through
> a different channel, the de-hinted lane included): CLEAN-fixture false-positive rows (no CLEAN
> fixture in either suite carried hints — the blind perspective CLEAN-FP weakness stands as a
> hint-analysis statement, but the de-hinted re-run re-characterizes it as run-unstable), the
> 3 critic ADVERSARIAL fixtures (unhinted), planner rows (suite verified hint-free), and
> within-lane cross-model comparisons (every model saw identical prompts, so relative rankings
> hold). Measured effect size, in-repo: the perspective pilot's hinted-vs-stripped A/B
> (`evals/suites/perspectives/PILOT-REPORT.md`, Rounds 1–2) found **no finding-count difference**
> for Claude Opus/Sonnet on 5 fixtures; the 2026-07-16 de-hinted re-run measures it for
> qwen3:32b at **nil on the critic suite** (67/68 content-adjudicated in both lanes) and
> **−1 must-find item on perspective** (the hint-carried `map-interface-zoom` target-size
> defect; 36/37 vs 37/37 content). The effect remains unmeasured for the other local models,
> so absolute historical rows should not be quoted as hint-free performance. Remediation
> (2026-07-16): fixtures de-hinted in place (hints removed above the blind cut line; answer-key
> sections kept; line references in answer keys, `.metadata.yaml`, and `.rubric.yaml`
> renumbered; scorers untouched); `test_blind_prompts.py` extended to fail on hint patterns
> across critic + perspective + planner prompts from both runners (166 prompts) and added to CI;
> the never-wired `evals/suites/perspectives/strip_bug_comments.py` (wrote stripped copies to a
> `fixtures-eval/` directory no runner read) deleted as superseded; the chain suite's extracted
> targets were already stripped at extraction and are unaffected. Deliberately kept, disclosed:
> reassurance comments (`NOT a bug — …`, `Works: …`, contrast-ratio annotations) that defuse
> false-positive traps — removing them changes the FP-trap difficulty the rubrics were normed on
> and is a separate calibration decision. *(That decision was executed later the same day — see the
> reassurance & verdict-steering disclosure below.)* Rows recorded before 2026-07-16 are not
> comparable on absolute detection metrics with post-de-hint runs.

> **Reassurance & verdict-steering disclosure (2026-07-16, follow-up to the hint-comment
> disclosure).** The mirror-image leak class the de-hint pass deliberately kept was removed the
> same day, and the removal surfaced a worse structural leak. **(1) Reassurance comments** —
> eval-authored text steering reviewers away from false-positive traps: `NOT a bug — …` comments
> (chat-cognitive-load ×8, dense-admin-jargon, multi-column-pricing, podcast-audio-only,
> video-tutorial-no-captions), `Works:`/`Good:` annotations (data-table-sortable-columns,
> color-only-status-indicators, modal-broken-focus-trap), comment self-verdicts (`— correct`,
> `works correctly`, `passes automated check`, `automated tools won't flag`) and prose denials
> (`(all correct — not a bug)`, `should NOT be flagged`, `— not a keyboard trap`) — removed above
> the blind cut line from 16 perspective and 2 critic fixtures. Kept: realistic developer
> documentation (contrast-ratio annotations, `passes AA` conformance notes, rationale comments
> such as "controls receive focus, not the video element") — the per-comment test was "would a
> competent developer plausibly write this in production code?". **(2) Verdict-steering sections
> (more serious)** — 7 critic fixtures, the 4 CLEAN (button-skip-link, interactive-dropdown,
> modal-complete, search-results-dynamic) and all 3 ADVERSARIAL (form-field-vs-summary-errors,
> search-focus-stays-in-input, tabbed-nav-vs-tab-pattern), had **no `## Accessibility Issues` cut
> line at all**, so `strip_answer_key()` passed their full text to every prompt in every lane,
> 2026-07-13 blind lanes included: CLEAN prompts contained "**CLEAN** — … Should receive a clean
> verdict or ACCEPT" plus "A11y-critic should verify…" grading notes; ADVERSARIAL prompts
> contained the full two-sided tension analysis ("The Ambiguity") plus "The 'correct' review is
> NOT to flag…" grading criteria. The rubrics' own baseline expectations were written assuming
> those sections were invisible, so the fixtures leaked against their rubrics' premises. Fix:
> cut-line headings inserted (CLEAN: directly after the features section, mirroring buggy-fixture
> shape — which also removes a structural tell; ADVERSARIAL: after Design Rationale, which stays
> visible as realistic PR-description content); modal-complete-clean's heading landed via the
> same-day fixture erratum (see Scoring changelog), this pass added the remaining 6. Direction of bias: critic CLEAN
> false-positive-resistance rows and critic ADVERSARIAL analysis-quality rows are
> **verdict-assisted upper bounds** in every lane recorded before this change. Perspective-suite
> CLEAN rows are structurally unaffected (all 25 perspective fixtures already had cut lines; the
> blind CLEAN-FP weakness stands), but perspective FP-trap difficulty rises corpus-wide with the
> reassurance comments gone. Also fixed in this pass: two residual defect-stating hints the
> de-hint pass missed (color-only-status-indicators "color is the ONLY selection indicator";
> modal-broken-focus-trap "Background content remains fully interactive…" plus the claims-list
> parenthetical "(though never used for focus restoration)") — must-find rates for those two
> fixtures were hint-assisted; five stale answer-key citations of already-removed `// BUG:`
> comments (below-cut, no prompt impact); and the committed chain-suite targets were regenerated
> (never re-extracted post-de-hint, they still carried both comment classes, and
> tabbed-nav-vs-tab-pattern's target README shipped the full Ambiguity + grading notes to the
> chain lane). Guard: `test_blind_prompts.py` gains REASSURANCE_PATTERNS (not-a-bug,
> flag-steering, Works:/Good: openers, comment self-verdicts, color-only denials, difficulty
> verdict tokens, fixture-class reveals, "A11y-critic should"), verified to catch 21 of the 22
> pre-fix leaking fixtures; the one shape with no machine-checkable invariant
> (autocomplete-fast-timeout's `fails AA for text but it's a status message` excuse, trimmed to
> the bare ratio — "fails AA" in a comment is legitimate developer vocabulary) is documented here
> instead. CLEAN-side titles were de-hinted with this pass: "(CLEAN)" suffixes and verdict-bearing
> tails ("With Proper/Complete Accessibility", "Full") dropped from the 3 critic and 5 perspective
> CLEAN h1 titles, matching the modal-complete-clean erratum's title treatment (guard: `tier
> suffix in title`). Known residual, deliberately unchanged: HAS-BUGS/FLAWED H1 titles and all
> fixture ids still name their planted defect ("Custom Dropdown with Focus Restoration Bug",
> "Tabs Component Missing Arrow Key Navigation") and titles sit above the cut line — ids double as
> filenames and result keys, so renaming is a separate decision (the fixture erratum's open
> axis (b)). A second known residual, surfaced in the merge review of this pass: the
> `## Accessibility Features Present` checklists (suite-wide, above the cut line by design)
> occasionally carry self-verdict phrasing ("— correct pattern for chat", "works correctly
> (Tab/Shift+Tab)") — factual feature context by suite convention, but eval-authored assurance
> at the margin; not machine-guarded because the checklist form is intentional, logged here so
> the axis is named. Scorers untouched. **Comparability:** rows recorded before this change
> are not comparable with post-change runs on (a) critic CLEAN false-positive resistance,
> (b) critic ADVERSARIAL analysis quality, (c) perspective FP-trap avoidance — in addition to the
> hint-comment caveat on detection rates; within-lane cross-model rankings hold (identical
> prompts per lane). The perspective pilot's FP calibration (`evals/suites/perspectives/`
> `PILOT-REPORT.md`, "0% FP validated") predates this change.

## Evidence Contract Smoke Gate

`ollama/score_output.py` now recognizes optional `A11y Evidence Finding` blocks when a rubric sets `require_evidence_contract: true`. The smoke gate validates required evidence fields, stable `finding_id`/`fingerprint` values, allowed trend metadata, and clean-fixture false-positive resistance. This is a scoring discipline for critic output, not a generated dashboard or scanner runtime. Existing benchmark rows are not retroactively rescored unless their raw artifacts are rerun through the updated scorer.

## Fixture 1: form-validation-missing-aria-describedby

**Difficulty**: HAS-BUGS | **Must-find**: 2 | **Should-find**: 1 | **Expected verdict**: REVISE

| Metric | llama3.3:70b | qwen3:32b | Hosted baselines |
|--------|-------------|-----------|------------------|
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

| Metric | llama3.3:70b | qwen3:32b | Hosted baselines |
|--------|-------------|-----------|------------------|
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

| Metric | llama3.3:70b | qwen3:32b | Hosted baselines |
|--------|-------------|-----------|------------------|
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

**Historical note**: The initial local-only interpretation suspected rubric overlap because both models caught `aria-live="assertive"` but missed `role="alert"`. Later hosted and qwen3.5:27b results found both items, so this was treated as a real model-specific detection gap rather than a rubric issue. **Blind update (2026-07-13)**: the blind qwen3:32b re-run found all 4/4 including `role="alert"` — the "gap" is run-to-run variance at temperature 0.3, not a stable characteristic.

## Abort Threshold

- **Gate**: < 40% must-find detection rate across all fixtures
- **Hosted/local baselines calibrate the gate** — later Claude API, Codex/OpenAI, and local-model results show that 40% is permissive for these fixtures; current comparisons should use the cross-platform tables below.

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

> ⚠ **2026-07-16 erratum**: when this row was recorded the fixture carried two real unplanted
> defects (focus-trap selector gaps; unguarded overlay onClick) and its prompt included "should
> receive ACCEPT" prose. The ACCEPT rows below are missed-defect data points — see Scoring changelog.

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

3. **Zero false positives on CLEAN fixtures.** Both models correctly identify well-implemented components and produce ACCEPT/ACCEPT-WITH-RESERVATIONS verdicts without manufacturing findings. *(2026-07-16 caveat: modal-complete-clean carried two real unplanted defects at the time, and every critic CLEAN prompt included "should receive a clean verdict" prose — see Scoring changelog erratum.)*

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

### a11y-critic — All Models

| Model | Fixtures | HAS-BUGS must-find | CLEAN failures / FP | FLAWED | ADVERSARIAL | Overall |
|-------|----------|-------------------|---------------------|--------|-------------|---------|
| Claude API escalation | 33 | **100%** | 0 remaining | 5/5 (100%) | 3/3 resolved | **33/33 PASS** |
| Codex/OpenAI escalation | 33 | **100%** | 0 remaining | 5/5 (100%) | 3/3 (100%) | **33/33 PASS** |
| GPT-5.2 | 33 | **100%** | 3 CLEAN WARN/FAIL | 5/5 (100%) | 3/3 (100%) | 30/33 PASS |
| Claude Haiku 4.5 | 33 | **100%** | 2 CLEAN WARN/FAIL | 5/5 (100%) | 0/3 verdict pass | 28/33 PASS |
| Claude Opus 4.6 | 7 | **7/7 (100%)** | 0/4 (0%) | — | — | **7/7 PASS** |
| Claude Sonnet 4.6 | 7 | **7/7 (100%)** | 0/4 (0%) | — | — | **7/7 PASS** |
| qwen3.5:27b | 17* | **37/37 (100%)** | 1/4 FAIL† | — | — | 16/17 PASS |
| qwen3:32b | 33 | 68/71 (96%) | 0/4 (0%) | 5/5 (100%) | 3/3 (100%) | **33/33 PASS** |
| llama3.3:70b | 7 | 6/7 (86%) | 0/4 (0%) | — | — | 7/7 PASS |
| qwen3.5:latest | 7 | 6/7 (86%) | 0/4 (0%) | — | — | 7/7 PASS |

*qwen3.5:27b run stopped at 17/33 due to `/think` stalls. †CLEAN FAIL is context exhaustion (no verdict emitted), not a false positive.*

*Claude, GPT-5.2, and qwen3.5:27b found 4/4 must-find items on toast-notification-no-role including `role="alert"`; qwen3:32b, llama3.3:70b, and qwen3.5:latest missed that item.*
*qwen3:32b HAS-BUGS must-find: 62/64 on the 18 new fixtures + 6/7 on the 3 original = 68/71 total*

### a11y-planner (2 fixtures)

| Model | Complex fixture | Focused fixture |
|-------|----------------|-----------------|
| llama3.3:70b | 13/15 (87%) | 8/8 (100%) |
| qwen3:32b | 15/15 (100%) | 8/8 (100%) |

### a11y-perspective-audit (25 fixtures, full benchmark)

| Model | HAS-BUGS | CLEAN | Must-find | Perspective coverage | Verdict accuracy |
|-------|----------|-------|-----------|---------------------|-----------------|
| qwen3:32b | 16/16 PASS | 4/5 PASS + 4 WARN | 100% | 100% | 24/25 correct |

### Model Comparison (Updated with Cross-Platform Baselines)

| Dimension | Claude Opus 4.6 | Claude Sonnet 4.6 | Claude Haiku 4.5 | GPT-5.2 | Codex/OpenAI escalation | Gemini 2.5 Flash | qwen3.5:27b | qwen3:32b | llama3.3:70b | qwen3.5:latest |
|-----------|----------------|-------------------|-----------------|---------|-------------------------|------------------|------------|-----------|-------------|----------------|
| Critic must-find (HAS-BUGS) | **100% (n=7)** | **100% (n=7)** | **100% (n=33)** | **100% (n=33)** | **100% (n=33)** | 98% (n=33) | **100% (n=13)** | 96% (n=33) | 86% (n=7) | 86% (n=7) |
| CLEAN failures / FP risk | 0% | 0% | 2 CLEAN failures | 3 CLEAN WARN/FAIL | 0 remaining after escalation | 1 CLEAN failure | 0%* | 0% | 0% | 0% |
| toast `role="alert"` (4/4) | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | No (3/4) | No (3/4) | No (3/4) |
| FLAWED detection | 5/5 via Phase 7 | 5/5 via escalation | 5/5 | 5/5 | 5/5 | 5/5 | — | 100% (n=5) | — | — |
| ADVERSARIAL articulation | 3/3 best-tier via Phase 7 | 3/3 via escalation | 0/3 verdict pass | 3/3 | 3/3 | 2/3 | — | 100% (n=3) | — | — |
| Perspective-audit (25 fix) | — | — | — | — | — | — | — | 20P/4W/1F | — | NOT VIABLE |
| Reliability (completion) | 100% | 100% | 100% | 100% | 100% after script fix | 100% (flash; pro quota-blocked) | 94% (16/17) | 100% | 100% | 100% |
| WCAG citation quality | Consistent | Consistent | Consistent | Consistent | Consistent | Consistent | Consistent | Consistent | Inconsistent | Consistent |
| Deployment | Cloud API | Cloud API | Cloud API | Codex CLI | Codex CLI | Gemini CLI | Local (17 GB) | Local (20 GB) | Local (40 GB) | Local (6.6 GB) |

*qwen3.5:27b: 1 CLEAN FAIL from context exhaustion (no verdict emitted), not a false positive. Run stopped at 17/33 due to stalls.*

### Key Findings (Updated with Cross-Platform Baselines)

1. **Bug detection is strong across hosted and local baselines.** Claude Haiku and GPT-5.2 both detect 100% of must-find items across the 33 critic fixtures at their base tiers. qwen3:32b passes all 33 fixtures locally with 96% HAS-BUGS must-find detection.

2. **The hardest failures are calibration failures, not simple bug-finding failures.** Claude Haiku and GPT-5.2 failures concentrate in CLEAN false positives and ADVERSARIAL verdicts. Escalation resolves the remaining failures without changing the fixture/rubric set.

3. **qwen3:32b remains the best committed local default.** It achieves 96% must-find on HAS-BUGS critic fixtures (68/71), 33/33 critic PASS, and 100% perspective-audit must-find. Only 3 partial misses out of 71 HAS-BUGS must-find items are documented.

4. **`role="alert"` is a real model-differentiating item.** Claude, GPT-5.2, and qwen3.5:27b found it; qwen3:32b, llama3.3:70b, and qwen3.5:latest did not. The initial rubric-overlap hypothesis is no longer the best explanation.

5. **Perspective-audit false-positive pattern: page-shell WCAG concerns.** On CLEAN fixtures presenting React components, the model sometimes flags `<html lang>`, `<title>`, or `<main>` — real WCAG requirements that live at the page-shell level, not the component level.

6. **Architecture: simple wrapper, not orchestrator.** A Python script that sends the full SKILL.md protocol as system prompt is sufficient for local Ollama and hosted model runners. No per-phase state management needed.

## Wrapper

`ollama/ollama_a11y.py` — supports critic, planner, and perspective-audit skills. See `ollama/README.md`.

## Phase 4C: Full Perspective-Audit Benchmark (qwen3:32b)

**Date**: 2026-05-14 (pilot, 7 fixtures), 2026-05-16 (full, 18 remaining fixtures)
**Protocol**: Full perspective-audit SKILL.md + reference files (20K chars) as system prompt.
**Input**: Fixture with injected escalation list from metadata (MEDIUM/HIGH perspectives only).
**Scoring**: `ollama/score_perspective.py` — checks perspective coverage, must-find detection, LOW leakage, ARRM routing, verdict.
**Verdict note**: Perspective-audit uses a PASS/REVISE/BLOCK ladder. BLOCK is valid when CRITICAL findings are present, even if metadata says REVISE.

### Results Summary (25 fixtures)

| Tier | Fixtures | PASS | WARN | FAIL | Must-find rate | Avg time |
|------|----------|------|------|------|---------------|----------|
| HAS-BUGS | 16 | 16 | 0 | 0 | 100% | ~198s |
| ADVERSARIAL | 4 | 4 | 0 | 0 | 100% | ~800s (pilot) |
| CLEAN | 5 | 0 | 4 | 1 | n/a | ~185s |
| **Total** | **25** | **20** | **4** | **1** | **100% (HAS-BUGS)** | **~198s (batch)** |

### HAS-BUGS Fixtures (16)

| Fixture | Verdict | Must-find | Perspectives | Time | Status |
|---------|---------|-----------|-------------|------|--------|
| animated-onboarding-flow | BLOCK ✓ | 2/2 | 2/2 | 801s* | PASS |
| autocomplete-fast-timeout | ✓ | 100% | 100% | ~200s | PASS |
| chat-cognitive-load | ✓ | 100% | 100% | ~200s | PASS |
| checkout-form-broken-errors | REVISE ✓ | 3/3 | 4/4 | 374s* | PASS |
| custom-select-combobox | ✓ | 50% | 100% | ~200s | PASS |
| data-table-sortable-columns | ✓ | 100% | 100% | ~200s | PASS |
| data-viz-color-encoding | ✓ | 100% | 100% | ~200s | PASS |
| dense-admin-jargon | REVISE ✓ | 1/1 | 4/4 | ~200s | PASS |
| hover-reveal-navigation | ✓ | 100% | 100% | ~200s | PASS |
| image-gallery-small-targets | ✓ | 100% | 100% | ~200s | PASS |
| infinite-scroll-cognitive | ✓ | 100% | 100% | ~200s | PASS |
| map-interface-zoom | ✓ | 100% | 100% | ~371s | PASS |
| modal-broken-focus-trap | REVISE ✓ | 2/2 | 3/3 | ~200s | PASS |
| podcast-audio-only | ✓ | 100% | 100% | ~200s | PASS |
| product-carousel-autoplay | ✓ | 100% | 100% | ~165s | PASS |
| tab-panel-arrow-keys | ✓ | 100% | 100% | ~200s | PASS |

*Pilot timings include dual-model memory pressure.

All 16 HAS-BUGS fixtures passed with 100% must-find detection and 100% perspective coverage.

### ADVERSARIAL Fixtures (4)

| Fixture | Key Test | Must-find | Status |
|---------|----------|-----------|--------|
| color-only-status-indicators | 1.4.3 vs 1.4.1 discrimination | 2/2 | PASS |
| search-results-dynamic-update | Live region + update pattern | 100% | PASS |
| video-tutorial-no-captions | Caption absence detection | 100% | PASS |
| multi-column-pricing | Reflow + cognitive pattern | 100% | PASS |

**Discriminator fixture confirmed**: color-only-status-indicators correctly distinguished WCAG 1.4.3 (contrast ratio — all colors pass) from WCAG 1.4.1 (color as sole differentiator — fails).

### CLEAN Fixtures (5)

> **⚠ ERRATUM (2026-06-14) — `login-form-clean` row refreshed.** This batch ran 2026-05-14/16, when the `login-form-clean` fixture still carried a real MAJOR **stale-error** bug (`aria-invalid` + error text persisted after a field was corrected, until re-submit). That bug was the I8 finding fixed only on 2026-06-13 (`0761855`, plan 011). So the *original* "PASS / matches nice_to_find" was qwen3:32b **missing a real bug under a mislabeled-CLEAN ground truth**, not validated false-positive avoidance. A free local re-run against the now-fixed fixture was completed 2026-06-14 (Metal :11435) and replaces the row below. The other 4 CLEAN rows are unaffected (their components were genuinely clean). Full re-run: "login-form-clean refresh" below.

| Fixture | Verdict | Findings | Status | Note |
|---------|---------|----------|--------|------|
| article-page-clean | PASS ✓ | 2 ENHANCEMENT | WARN | Correct — matches nice_to_find |
| dashboard-text-labels | PASS ✓ | 2 ENHANCEMENT | WARN | Correct — matches nice_to_find |
| login-form-clean | PASS ✓ | 2 ENHANCEMENT | WARN | **Refreshed 2026-06-14 on the fixed fixture — now a VALID clean-recognition** (the original 2026-05 PASS was a missed bug; see refresh) |
| nav-menu-landmarks | REVISE | 2 MAJOR | WARN* | Flagged missing `<title>` and `<html lang>` |
| media-player-captions | BLOCK | 2 findings | FAIL | Flagged page-shell concerns on sub-component |

**CLEAN false-positive analysis**:
- 3 fixtures (article, dashboard, login): Correct PASS verdicts with ENHANCEMENT-level notes matching rubric nice_to_find items. (login-form-clean's 2026-06-14 refresh on the fixed fixture confirms this; its original 2026-05 run scored the buggy component — see erratum.)
- nav-menu-landmarks: Gave REVISE for missing `<title>` (2.4.2) and `<html lang>` (3.1.1). These are real WCAG requirements the fixture's React component doesn't satisfy (React components don't render `<html>` or `<head>` — the app shell does). Rubric updated to accept REVISE as valid for this fixture since the component presents itself as a full page. *Scored as WARN after rubric update.
- media-player-captions: Gave BLOCK after flagging missing `<main>` landmark, missing `lang`, and transcript association issues. This is a clear sub-component (`MediaPlayer`, returns `<section>`) — page-level concerns are out of scope. Fixture updated with scope note for future runs.

#### login-form-clean refresh (2026-06-14 · fixed fixture · qwen3:32b · Metal :11435)

Re-ran after the I8 component fix (`0761855`) against the now-genuinely-clean fixture — same protocol (escalation-injection from metadata + `score_perspective.py`), qwen3:32b on the native Metal server (`OLLAMA_URL=http://localhost:11435/api/generate`, since `run_benchmark.py` reads `OLLAMA_URL`, not `OLLAMA_HOST`).

| Metric | qwen3:32b (post-fix — VALID) |
|--------|------------------------------|
| Verdict | PASS (expected PASS) ✓ |
| CRITICAL / MAJOR | 0 / 0 |
| Findings raised | 2 ENHANCEMENT — password-visibility toggle (3.3.7) + optional `aria-live` on error summary; both match the rubric's `nice_to_find` |
| Page-shell over-flag | none (did **not** flag `<html lang>`/`<title>`) |
| Status | WARN — correct verdict, enhancements noted |
| Generation | 336s · 1,959 tokens · 5,254 chars |

**Interpretation:** The verdict is identical to the original (PASS / 2 ENHANCEMENT / WARN) — which *confirms* the 2026-05 run genuinely **missed** the stale-error bug (it produced the same clean verdict whether the bug was present or not). The refresh does not change the headline CLEAN false-positive rate; it converts an **invalid** data point (clean verdict on a buggy, mislabeled-CLEAN component, scored as a virtue) into a **valid** one (clean verdict on a genuinely clean component). login-form-clean is now a legitimate false-positive-avoidance pass.

### Known Model Characteristic: Page-Shell WCAG Over-Flagging

qwen3:32b on perspective-audit consistently flags page-level WCAG requirements (`<html lang>`, `<title>`, `<main>` landmark) on component-level React fixtures. This is technically correct WCAG analysis but scope-inappropriate for component review. The pattern is:
- On sub-components (clear `<section>` or `<div>` root): model should not flag → fixture scope notes prevent this
- On page-level components (header → main → footer): model flags are arguably correct → rubrics accept alternate verdicts
- On all HAS-BUGS fixtures: no impact — real bugs dominate the output

This is a real characteristic worth knowing for practitioners using the Ollama wrapper on component code.

### Pilot Fixtures (detailed results from 2026-05-14)

<details>
<summary>Click to expand 7 pilot fixture details</summary>

#### animated-onboarding-flow (Vestibular HIGH, Cognitive MEDIUM)

| Metric | qwen3:32b |
|--------|-----------|
| Perspective coverage | 2/2 (100%) |
| LOW perspective leakage | none |
| Must-find detection | 2/2 (100%) |
| Should-find detection | 2/2 (100%) |
| Nice-to-find detection | 1/1 (100%) |
| WCAG citations | All present |
| ARRM routing | YES |
| Verdict | BLOCK (valid — 2 CRITICAL findings) |
| Response chars | 7,955 |
| Tokens generated | 2,682 |
| Generation time | 801s (dual-model memory pressure) |
| **Status** | **PASS** |

#### checkout-form-broken-errors (Screen Reader HIGH, Keyboard/Contrast/Cognitive MEDIUM)

| Metric | qwen3:32b |
|--------|-----------|
| Perspective coverage | 4/4 (100%) |
| Must-find detection | 3/3 (100%) |
| Should-find detection | 2/2 (100%) |
| Verdict | REVISE ✓ |
| Generation time | 374s |
| **Status** | **PASS** |

#### color-only-status-indicators (ADVERSARIAL — Contrast HIGH, Cognitive HIGH, others MEDIUM)

| Metric | qwen3:32b |
|--------|-----------|
| Perspective coverage | 5/5 (100%) |
| Must-find detection | 2/2 (100%) |
| Should-find detection | 2/2 (100%) |
| Verdict | BLOCK (valid — CRITICAL findings) |
| Generation time | 2,849s (dual-model pressure) |
| **Status** | **PASS** |

Must-find: (1) Status indicators rely on color alone (1.4.1), (2) Hover-only tooltips, no :focus (1.4.13/2.1.1).

#### modal-broken-focus-trap (Keyboard HIGH, Screen Reader HIGH, Cognitive MEDIUM)

| Metric | qwen3:32b |
|--------|-----------|
| Perspective coverage | 3/3 (100%) |
| Must-find detection | 2/2 (100%) |
| Verdict | REVISE ✓ |
| **Status** | **PASS** |

#### dense-admin-jargon (Cognitive HIGH, Magnification/Screen Reader/Contrast MEDIUM)

| Metric | qwen3:32b |
|--------|-----------|
| Perspective coverage | 4/4 (100%) |
| Must-find detection | 1/1 (100%) |
| Should-find detection | 3/3 (100%) |
| Verdict | REVISE ✓ |
| **Status** | **PASS** |

#### login-form-clean (CLEAN — Cognitive MEDIUM)

> **⚠ ERRATUM (2026-06-14):** This result scored the pre-I8-fix component, which carried a real MAJOR stale-error bug (fixed 2026-06-13, `0761855`). The "PASS" reflects a missed bug under a mislabeled-CLEAN ground truth. See the "login-form-clean refresh" subsection for the valid post-fix re-run.

| Metric | qwen3:32b (pre-fix — INVALID) |
|--------|-----------|
| Verdict | PASS ✓ |
| **Status** | **PASS (WARN — enhancements noted)** — superseded, see refresh |

#### article-page-clean (CLEAN — Cognitive MEDIUM)

| Metric | qwen3:32b |
|--------|-----------|
| Verdict | PASS ✓ |
| **Status** | **PASS (WARN — enhancements noted)** |

</details>

## Additional Model Results (Preliminary)

### deepseek-r1:70b — a11y-critic (n=1)

| Fixture | Must-find | Verdict | Time |
|---------|----------|---------|------|
| form-validation-missing-aria-describedby | 2/2 (100%) | REVISE ✓ | 760s |

**Note**: Single-fixture result only. DeepSeek-R1 did not emit `<think>` blocks through the Ollama generate API on this fixture — the stripping logic in the scorer is present but was not exercised. More fixtures needed before conclusions.

### qwen3.5:latest (6.6 GB) — a11y-critic (n=7)

| Fixture | Difficulty | Must-find | Verdict | Time |
|---------|-----------|----------|---------|------|
| form-validation-missing-aria-describedby | HAS-BUGS | 2/2 (100%) | REVISE ✓ | 130s |
| tabs-missing-arrow-nav | HAS-BUGS | 1/1 (100%) | REVISE ✓ | 109s |
| toast-notification-no-role | HAS-BUGS | 3/4 (75%) | REJECT ✓ | 75s |
| button-skip-link-clean | CLEAN | 0 expected | ACCEPT ✓ | 170s |
| interactive-dropdown-clean | CLEAN | 0 expected | ACCEPT ✓ | 70s |
| modal-complete-clean | CLEAN | 0 expected | ACCEPT ✓ | 400s |
| search-results-dynamic-clean | CLEAN | 0 expected | ACCEPT ✓ | 95s |

| Metric | Result |
|--------|--------|
| HAS-BUGS must-find rate | 6/7 (86%) |
| CLEAN false positive rate | 0/4 (0%) |
| Verdict accuracy | 7/7 (100%) |
| Average generation time (HAS-BUGS) | 105s |
| Average generation time (CLEAN) | 134s |
| Model size | 6.6 GB |

**Finding**: qwen3.5:latest matches qwen3:32b and llama3.3:70b on all measured dimensions — same 86% must-find rate, same 0% false positive rate, same 100% verdict accuracy — while being 3-6x faster and using 1/3 the memory. The same `role="alert"` rubric overlap miss hits all 4 models tested, suggesting a rubric issue rather than a model-specific blind spot. *(2026-07-16: the modal-complete-clean ACCEPT is a missed-defect data point — see Scoring changelog erratum.)*

**Scorer note**: The search-results-dynamic-clean fixture initially scored as FAIL due to a verdict-detection bug — the scorer matched "REVISE" in a hypothetical section ("What would need to change for REVISE") rather than the declared verdict (ACCEPT-WITH-RESERVATIONS). Fixed in `score_output.py` by prioritizing explicit `# Verdict:` declarations.

### qwen3.5:27b (17.4 GB) — a11y-critic (n=17 of 33, run stopped)

**Date**: 2026-05-17
**Settings**: num_ctx=16384, temperature=0.3, streaming mode
**Run stopped at 17/33**: fixture 12 (interactive-dropdown-focus-bug) stalled after 50 min with runner at 0.5% CPU — same `/think` context exhaustion pattern as qwen3.5:latest on perspective-audit.

| Tier | Fixtures | PASS | Must-find rate | Avg time |
|------|----------|------|---------------|----------|
| HAS-BUGS | 13 | 13/13 | **37/37 (100%)** | ~460s |
| CLEAN | 4 | 3/4 | n/a | ~580s |
| **Total** | **17** | **16** | **100% (HAS-BUGS)** | ~500s |

**CLEAN results**: 3 PASS, 1 FAIL (search-results-dynamic-clean — context exhaustion produced malformed response with no verdict after 1399s), 1 WARN (button-skip-link-clean — correct verdict, minor findings).

**Key finding**: qwen3.5:27b achieved **100% must-find on all 13 HAS-BUGS fixtures** including 4/4 on toast-notification (`role="alert"`) — matching Claude and surpassing qwen3:32b (which missed this item). This is the first local model to find it. However, the model is prone to `/think` context exhaustion on some fixtures (1 CLEAN FAIL, 1 stall) and is 2x slower than qwen3:32b on average.

**Recommendation updated**: qwen3.5:27b has better detection accuracy than qwen3:32b on the tested fixtures (100% vs 86% on the 7-fixture comparison set), but its reliability is lower — some fixtures stall or produce empty output. For production use, qwen3:32b remains the safer choice due to consistent completion.

## Phase 4A: Full Critic Benchmark (qwen3:32b)

**Date**: 2026-05-15
**Protocol**: Full a11y-critic SKILL.md as system prompt, single-shot generation
**Model**: qwen3:32b (18.8 GB, Q4_K_M)
**Settings**: num_ctx=16384, temperature=0.3
**Fixtures**: 26 (18 HAS-BUGS + 5 FLAWED + 3 ADVERSARIAL) — plus 4 CLEAN + 3 HAS-BUGS from prior sessions = 33 total

### Results Summary

| Tier | Fixtures | PASS | Must-find rate | Avg time | Avg chars |
|------|----------|------|---------------|----------|-----------|
| HAS-BUGS | 18 | 18/18 (100%) | 62/64 (97%) | 231s | 3,791 |
| FLAWED | 5 | 5/5 (100%) | 5/5 (100%) | 3,265s | 4,462 |
| ADVERSARIAL | 3 | 3/3 (100%) | 3/3 (100%) | 2,769s | 4,683 |
| **Total** | **26** | **26/26 (100%)** | **70/72 (97%)** | **1,107s** | **3,997** |

Combined with prior sessions (4 CLEAN + 3 HAS-BUGS): **33/33 fixtures, all PASS.**

### HAS-BUGS Tier (18 fixtures)

| Fixture | Verdict | Must-find | Time | Tokens |
|---------|---------|-----------|------|--------|
| accordion-no-region-role | REVISE ✓ | 2/2 | 340s | 1,544 |
| breadcrumb-navigation-no-nav-landmark | REVISE ✓ | 2/2 | 192s | 1,428 |
| checkbox-group-no-fieldset | REJECT | 2/2 | 204s | 1,769 |
| combobox-autocomplete-no-listbox-role | REVISE ✓ | 4/4 | 191s | 1,705 |
| data-table-missing-scope | REVISE ✓ | 2/2 | 142s | 1,192 |
| expandable-section-no-button | REJECT | 4/4 | 193s | 1,711 |
| file-input-no-labels | REVISE ✓ | 3/4 | 169s | 1,466 |
| heading-hierarchy-skipped | REVISE ✓ | 2/2 | 122s | 1,115 |
| image-carousel-no-region | REVISE ✓ | 4/4 | 165s | 1,572 |
| infinite-scroll-no-announcement | REJECT | 4/4 | 140s | 1,471 |
| interactive-dropdown-focus-bug | REVISE ✓ | 2/2 | 165s | 1,845 |
| loading-state-missing-aria-busy | REVISE ✓ | 2/2 | 128s | 1,447 |
| megamenu-no-structure | REJECT | 6/6 | 175s | 1,909 |
| pagination-no-nav-landmark | REVISE ✓ | 3/3 | 124s | 1,353 |
| popover-no-focus-management | REJECT | 5/5 | 181s | 1,550 |
| radio-button-group-no-grouping | REJECT | 2/2 | 1,051s | 1,550 |
| tooltip-no-role-no-association | REVISE ✓ | 2/3 | 120s | 1,652 |
| video-player-missing-captions | REJECT | 3/3 | 358s | 1,584 |

**Partial detections** (2 fixtures):
- `file-input-no-labels`: Missed "File type restrictions not announced" — found the other 3 must-find items (missing label, no aria-describedby, no aria-invalid)
- `tooltip-no-role-no-association`: Missed "Tooltip not announced when button is focused" — found hover-not-focus and missing aria-describedby

**Verdict notes**: REJECT vs REVISE — the model sometimes rates severity higher than the rubric expects. REJECT for fixtures with multiple CRITICAL-level issues (megamenu, popover, infinite-scroll) is arguably correct; the rubric REVISE expectation is conservative. All REJECT verdicts still pass the scoring gate (detection, not verdict match, determines pass/fail).

### FLAWED Tier (5 fixtures)

Subtle, incomplete patterns. These fixtures have bugs that are harder to spot because the implementation is partially correct.

| Fixture | Verdict | Must-find | Time | Tokens |
|---------|---------|-----------|------|--------|
| app-focus-order-illogical | REVISE ✓ | 1/1 | 3,508s | 1,722 |
| async-form-vague-success | REVISE ✓ | 1/1 | 2,753s | 1,550 |
| dashboard-heading-inconsistency | REVISE ✓ | 1/1 | 4,256s | 2,158 |
| multistep-form-error-clearing | REVISE ✓ | 1/1 | 4,212s | 1,513 |
| tabs-incomplete-aria-selected | REVISE ✓ | 1/1 | 1,596s | 1,691 |

**Key finding**: FLAWED fixtures take 10-25x longer than HAS-BUGS (avg 3,265s vs 231s). The model generates significantly more internal reasoning (`/think` tokens) before committing to findings on subtle bugs. Token output is similar (~1,500-2,100), so the extra time is spent reasoning, not writing.

### ADVERSARIAL Tier (3 fixtures)

Genuinely ambiguous patterns where both sides of a design tradeoff are defensible. Scored on tradeoff articulation, not bug detection.

| Fixture | Verdict | Must-articulate | Time | Tokens |
|---------|---------|----------------|------|--------|
| tabbed-nav-vs-tab-pattern | ACCEPT-WITH-RESERVATIONS ✓ | 1/1 | 3,536s | 1,810 |
| form-field-vs-summary-errors | ACCEPT-WITH-RESERVATIONS ✓ | 1/1 | 1,764s | 1,890 |
| search-focus-stays-in-input | ACCEPT-WITH-RESERVATIONS ✓ | 1/1 | 3,007s | 1,490 |

**Key findings**:
1. All 3 produced ACCEPT-WITH-RESERVATIONS — the model correctly identifies these as design tradeoffs rather than clear bugs. This is the ideal verdict for ambiguous patterns.
2. All 3 articulated the central tension (tabs-vs-nav semantic model, dual-announcement redundancy, focus-stays-in-input agency tradeoff).
3. The `should_find` items were also detected (2/2 on search-focus, 1/1 on tabbed-nav, 1/1 on form-field).

### Phase 4A Timing Analysis

| Tier | Min | Median | Max | Explanation |
|------|-----|--------|-----|-------------|
| HAS-BUGS | 120s | 172s | 1,051s | Most straightforward; radio-button outlier due to qwen3 thinking mode |
| FLAWED | 1,596s | 3,508s | 4,256s | Subtle bugs require extended reasoning chains |
| ADVERSARIAL | 1,764s | 3,007s | 3,536s | Ambiguity triggers deliberative reasoning |

Total Phase 4A runtime: **8.0 hours** (26 fixtures, single model, sequential). The FLAWED/ADVERSARIAL tiers account for 78% of total runtime despite being only 31% of fixtures.

**Memory note**: qwen3:32b with `/think` mode active (default for qwen3) uses extended context for internal reasoning. The 16384 num_ctx may be a bottleneck on FLAWED/ADVERSARIAL fixtures where the model is reasoning for 30-60+ minutes. Testing with num_ctx=32768 on FLAWED fixtures could reduce generation time.

---

## Phase 4D: qwen3.5:latest on Perspective-Audit (NOT VIABLE)

**Date**: 2026-05-17
**Model**: qwen3.5:latest (6.6 GB, Q4_K_M, 9.7B params)
**Settings**: num_ctx=16384, temperature=0.3, streaming mode
**Fixtures attempted**: 10/25 (run aborted — model not viable)

### Results

| Outcome | Fixtures | Avg time | Avg output |
|---------|----------|----------|------------|
| Usable response | 5/10 | ~157s | 4,033 chars |
| Empty (0 chars) | 5/10 | ~4,582s (76 min) | 0 chars |

**Fixtures with usable responses:**
- animated-onboarding-flow: 127s, 6,255 chars
- article-page-clean: 111s, 1,026 chars
- chat-cognitive-load: 144s, 6,989 chars
- custom-select-combobox: 116s, 1,712 chars
- data-viz-color-encoding: 194s, 4,173 chars

**Fixtures that produced 0 chars after 75+ min each:**
- autocomplete-fast-timeout: 4,610s
- checkout-form-broken-errors: 4,521s
- color-only-status-indicators: 796s
- dashboard-text-labels: 4,481s
- data-table-sortable-columns: 4,501s

### Analysis

qwen3.5:latest exhausts its 16K context window on `/think` reasoning for complex perspective-audit fixtures, leaving no room for output tokens. The model spends 60-75 minutes generating internal reasoning chains that consume the entire context, then emits nothing.

This is a **fundamental model capacity issue**, not a timeout or configuration problem:
- The perspective-audit protocol (~20K chars system prompt + ~7-10K chars fixture) leaves ~40-50% of the 16K token window for generation
- The model's `/think` mode consumes all available generation space on complex fixtures
- Simple fixtures (CLEAN, straightforward HAS-BUGS) complete in 2-3 minutes with good output
- Complex fixtures (multi-perspective HAS-BUGS, ADVERSARIAL) spin for 75+ minutes and produce nothing

**Conclusion**: qwen3.5:latest (9.7B) is viable for a11y-critic (single-focus review) but NOT for perspective-audit (multi-perspective deep review). The perspective-audit skill requires qwen3:32b or larger.

### Recommendation update

| Skill | Minimum model | Recommended |
|-------|--------------|-------------|
| a11y-critic | qwen3.5:latest (6.6 GB) | qwen3:32b (20 GB) |
| a11y-planner | qwen3.5:latest (6.6 GB) | qwen3:32b (20 GB) |
| perspective-audit | qwen3:32b (20 GB) | qwen3:32b (20 GB) |

---

## Phase 5: Claude Baselines (a11y-critic)

**Date**: 2026-05-17
**Protocol**: Same SKILL.md as Ollama runs, delivered via Claude Code subagents with explicit model routing.
**Fixtures**: 7 core (3 HAS-BUGS + 4 CLEAN) — the set all Ollama models were tested on.
**Scoring**: Same `score_output.py` rubrics as Ollama.

### Results

| Model | Must-find (7 items) | Verdict accuracy | CLEAN FP | Status |
|-------|-------------------|------------------|----------|--------|
| Claude Opus 4.6 | **7/7 (100%)** | 7/7 | 0% | **7/7 PASS** |
| Claude Sonnet 4.6 | **7/7 (100%)** | 7/7 | 0% | **7/7 PASS** |
| Claude Haiku 4.5 | **7/7 (100%)** | 7/7 | 0% | **7/7 PASS** |

### Per-Fixture Detail

| Fixture | Difficulty | Opus 4.6 | Sonnet 4.6 | Haiku 4.5 |
|---------|-----------|----------|------------|-----------|
| form-validation-missing-aria-describedby | HAS-BUGS | REVISE ✓ (2/2) | REVISE ✓ (2/2) | REVISE ✓ (2/2) |
| tabs-missing-arrow-nav | HAS-BUGS | REVISE ✓ (1/1) | REVISE ✓ (1/1) | REVISE ✓ (1/1) |
| toast-notification-no-role | HAS-BUGS | REJECT (4/4) | REVISE ✓ (4/4) | REJECT (4/4) |
| button-skip-link-clean | CLEAN | ACCEPT ✓ | ACCEPT ✓ | ACCEPT ✓ |
| interactive-dropdown-clean | CLEAN | ACCEPT ✓ | ACCEPT-W-R ✓ | ACCEPT ✓ |
| modal-complete-clean† | CLEAN | ACCEPT ✓ | ACCEPT ✓ | ACCEPT ✓ |
| search-results-dynamic-clean | CLEAN | ACCEPT ✓ | ACCEPT-W-R ✓ | ACCEPT ✓ |

*† Recorded against the pre-2026-07-16 fixture, which carried two real unplanted defects — see Scoring changelog erratum.*

### Key Observations

1. **All Claude models found `role="alert"` (4/4 on toast).** Every Ollama model missed this item (3/4). The earlier hypothesis that this was a rubric overlap (`aria-live="assertive"` covers the same semantic as `role="alert"`) is disproven — Claude models recognize both as distinct requirements. The Ollama miss is a real detection gap.

2. **Tier separation is minimal on these fixtures.** Opus, Sonnet, and Haiku produce identical pass/fail results. Sonnet was slightly more cautious on CLEAN fixtures (2 ACCEPT-WITH-RESERVATIONS vs clean ACCEPT from Opus/Haiku). The structured protocol levels the playing field on straightforward fixtures.

3. **Verdict calibration differs.** Opus and Haiku gave REJECT on toast-notification (more severe); Sonnet gave REVISE (more conservative). All are valid — the scoring gate uses must-find detection, not verdict match.

4. **Response characteristics by model:**
   - Opus: ~8-11K chars, thorough phase compliance, nuanced CLEAN verdicts
   - Sonnet: ~10-13K chars, most verbose, most cautious on CLEAN
   - Haiku: ~5-7K chars, concise but complete, zero false findings on CLEAN

5. **Next step for differentiation**: Run Claude models on FLAWED and ADVERSARIAL fixtures where subtle bugs and ambiguous tradeoffs may expose tier differences that straightforward HAS-BUGS/CLEAN fixtures don't.

### Phase 5B: Full Escalation Benchmark (33 fixtures)

**Date**: 2026-05-18
**Protocol**: Anthropic SDK via `run_cloud_benchmark.py`, same SKILL.md system prompt, temperature 0.3.
**Fixtures**: All 33 (4 CLEAN + 21 HAS-BUGS + 5 FLAWED + 3 ADVERSARIAL).
**Method**: Bottom-up escalation — start at cheapest tier, score all, promote only failures.

#### Escalation Results

| Tier | Fixtures Run | PASS | FAIL | Must-find Rate | Tokens (in/out) | Time |
|------|-------------|------|------|----------------|-----------------|------|
| **Haiku 4.5** | 33 | 28 | 5 | 100% (HAS-BUGS) | 521K/255K | 37 min (67s avg) |
| **Sonnet 4.6** | 5 | 4 | 1 | n/a (CLEAN/ADV) | 81K/35K | 11 min (129s avg) |
| **Sonnet 4.6 + thinking** | 1 | 1 | 0 | n/a (CLEAN) | 16K/8K | 2.5 min |

**Cheapest tier with 100% pass: Sonnet 4.6 + thinking** (budget_tokens=2048)

#### Haiku Failures (5 of 33)

| Fixture | Difficulty | Haiku Verdict | Why Failed | Resolved At |
|---------|-----------|--------------|------------|-------------|
| button-skip-link-clean | CLEAN | REVISE | False positive on clean code | Sonnet |
| modal-complete-clean† | CLEAN | ACCEPT (WARN) | Correct verdict but raised structured findings | Sonnet-think |
| tabbed-nav-vs-tab-pattern | ADVERSARIAL | NONE | Found tradeoffs (1/1) but no verdict emitted | Sonnet |
| form-field-vs-summary-errors | ADVERSARIAL | ACCEPT | Found tradeoffs (1/1) but wrong verdict | Sonnet |
| search-focus-stays-in-input | ADVERSARIAL | ACCEPT | Found tradeoffs (1/1) but wrong verdict | Sonnet |

*† 2026-07-16 erratum: the fixture carried two real unplanted defects at the time — Haiku's "structured findings on clean code" may have been correct observations (raw artifacts not retained). See Scoring changelog.*

**Pattern**: Haiku handles all HAS-BUGS (21/21) and FLAWED (5/5) fixtures perfectly. Failures concentrate in CLEAN (false positives) and ADVERSARIAL (verdict calibration). Bug detection is not the issue — judgment is.

#### Full Haiku Results (33 fixtures)

| Fixture | Difficulty | Verdict | Must-find | Status |
|---------|-----------|---------|-----------|--------|
| accordion-no-region-role | HAS-BUGS | REVISE | 2/2 | PASS |
| app-focus-order-illogical | FLAWED | REJECT | 1/1 | PASS |
| async-form-vague-success | FLAWED | REVISE | 1/1 | PASS |
| breadcrumb-navigation-no-nav-landmark | HAS-BUGS | REJECT | 2/2 | PASS |
| button-skip-link-clean | CLEAN | REVISE | — | **FAIL** |
| checkbox-group-no-fieldset | HAS-BUGS | REJECT | 2/2 | PASS |
| combobox-autocomplete-no-listbox-role | HAS-BUGS | REJECT | 4/4 | PASS |
| dashboard-heading-inconsistency | FLAWED | REVISE | 1/1 | PASS |
| data-table-missing-scope | HAS-BUGS | REVISE | 2/2 | PASS |
| expandable-section-no-button | HAS-BUGS | REJECT | 4/4 | PASS |
| file-input-no-labels | HAS-BUGS | REJECT | 4/4 | PASS |
| form-field-vs-summary-errors | ADVERSARIAL | ACCEPT | 1/1 | **FAIL** |
| form-validation-missing-aria-describedby | HAS-BUGS | REJECT | 2/2 | PASS |
| heading-hierarchy-skipped | HAS-BUGS | REJECT | 2/2 | PASS |
| image-carousel-no-region | HAS-BUGS | REJECT | 4/4 | PASS |
| infinite-scroll-no-announcement | HAS-BUGS | REJECT | 4/4 | PASS |
| interactive-dropdown-clean | CLEAN | ACCEPT | — | PASS |
| interactive-dropdown-focus-bug | HAS-BUGS | REVISE | 2/2 | PASS |
| loading-state-missing-aria-busy | HAS-BUGS | REJECT | 2/2 | PASS |
| megamenu-no-structure | HAS-BUGS | REJECT | 6/6 | PASS |
| modal-complete-clean | CLEAN | ACCEPT | — | **WARN** |
| multistep-form-error-clearing | FLAWED | REJECT | 1/1 | PASS |
| pagination-no-nav-landmark | HAS-BUGS | REJECT | 3/3 | PASS |
| popover-no-focus-management | HAS-BUGS | REJECT | 5/5 | PASS |
| radio-button-group-no-grouping | HAS-BUGS | REJECT | 2/2 | PASS |
| search-focus-stays-in-input | ADVERSARIAL | ACCEPT | 1/1 | **FAIL** |
| search-results-dynamic-clean | CLEAN | ACCEPT-W-R | — | PASS |
| tabbed-nav-vs-tab-pattern | ADVERSARIAL | NONE | 1/1 | **FAIL** |
| tabs-incomplete-aria-selected | FLAWED | REJECT | 1/1 | PASS |
| tabs-missing-arrow-nav | HAS-BUGS | REVISE | 1/1 | PASS |
| toast-notification-no-role | HAS-BUGS | REJECT | 4/4 | PASS |
| tooltip-no-role-no-association | HAS-BUGS | REJECT | 2/3 | PASS |
| video-player-missing-captions | HAS-BUGS | REJECT | 3/3 | PASS |

#### Key Observations

1. **Haiku is production-viable for bug detection.** 28/33 PASS (85%), with all 21 HAS-BUGS and all 5 FLAWED fixtures passing. Every must-find item detected. At $0.25/1M in + $1.25/1M out, the Haiku tier costs ~$0.45 total for all 33 fixtures.

2. **Failures are judgment, not detection.** Haiku found the tradeoffs in all 3 ADVERSARIAL fixtures (1/1 must-articulate) but couldn't calibrate verdicts for ambiguous cases. It also generated one false positive on a CLEAN fixture. These are higher-order reasoning failures, not pattern-matching gaps.

3. **Sonnet resolves almost everything.** 4 of 5 Haiku failures pass at Sonnet with no thinking. Only the most nuanced CLEAN fixture (modal-complete-clean) needed thinking enabled. *(2026-07-16: "most nuanced" now has a simpler explanation — the fixture carried two real defects that stronger reviewers kept almost-flagging; see Scoring changelog erratum.)*

4. **Cost-optimal strategy**: Use Haiku for triage (catches all real bugs), escalate CLEAN and ADVERSARIAL fixtures to Sonnet for verdict quality. Total cost for the full 33-fixture run: ~$0.65 (Haiku $0.45 + Sonnet $0.18 + Sonnet-think $0.02).

---

## Phase 6: Cross-Platform Benchmark (Codex/OpenAI)

**Date**: 2026-05-19
**Protocol**: Codex CLI (`codex exec`) via `run_cloud_benchmark.py`, same SKILL.md prompt, read-only sandbox.
**Fixtures**: All 33 critic fixtures.
**Method**: Bottom-up escalation via `bash ollama/codex-benchmark.sh`. GPT-5.3 does not exist in Codex — escalation skipped from 5.2-low directly to 5.5.

#### Escalation Results

| Tier | Fixtures Run | PASS | WARN | FAIL | Time |
|------|-------------|------|------|------|------|
| **GPT-5.2** | 33 | 30 | 2 | 1 | 22 min (41s avg) |
| **GPT-5.2 (low)** | 3 | 1 | 2 | 0 | 1.5 min (31s avg) |
| **GPT-5.5** | 2 | 1 | 0 | 1 | 1 min (32s avg) |
| **GPT-5.5 (low)** | 1 | 1 | 0 | 0 | 34s |

**Cheapest path to 100% pass:**
- GPT-5.2 handles 30/33 (91%)
- GPT-5.2 (low effort) clears `button-skip-link-clean`
- GPT-5.5 clears `modal-complete-clean`
- GPT-5.5 (low effort) clears `search-results-dynamic-clean`

#### Failure Cascade

| Fixture | Difficulty | GPT-5.2 | 5.2-low | 5.5 | 5.5-low |
|---------|-----------|---------|---------|-----|---------|
| button-skip-link-clean | CLEAN | WARN | **PASS** | — | — |
| modal-complete-clean† | CLEAN | WARN | WARN | **PASS** | — |
| search-results-dynamic-clean | CLEAN | FAIL | WARN | FAIL | **PASS** |

*† 2026-07-16 erratum: fixture carried two real unplanted defects at the time — the GPT-5.2/5.2-low WARNs ("raised findings on clean code") may have been correct observations. See Scoring changelog.*

**Pattern**: Identical to Claude — all HAS-BUGS (21/21), FLAWED (5/5), and ADVERSARIAL (3/3) pass at the cheapest tier. Only CLEAN fixtures cause failures (false positives or raised findings on clean code). Bug detection is solved across both platforms; false positive suppression requires larger models or lower effort settings.

#### GPT-5.2 vs Claude Haiku Comparison

| Metric | GPT-5.2 | Claude Haiku 4.5 |
|--------|---------|-----------------|
| Fixtures at base tier | 33 | 33 |
| PASS at base tier | 30 (91%) | 28 (85%) |
| All HAS-BUGS pass? | Yes (21/21) | Yes (21/21) |
| All FLAWED pass? | Yes (5/5) | Yes (5/5) |
| All ADVERSARIAL pass? | **Yes (3/3)** | No (0/3) |
| CLEAN failures | 3 (all WARN/FAIL) | 2 (1 FAIL, 1 WARN) |
| Avg time/fixture | 41s | 67s |
| Total cost (33 fix) | included in Codex sub | ~$0.45 |

GPT-5.2 outperforms Haiku on ADVERSARIAL fixtures (3/3 vs 0/3) — it calibrates verdicts on genuinely ambiguous tradeoffs. Haiku beats GPT-5.2 on CLEAN fixture count (2 failures vs 3). Both achieve 100% must-find detection on all HAS-BUGS and FLAWED fixtures.

#### Bug in escalation script (fixed)

The initial run hit GPT-5.3 (which doesn't exist in Codex), causing `codex exec` to fail with rc=1. The escalation script incorrectly counted the failed tier as 100% pass because `not_run` fixtures weren't treated as failures to escalate. Fixed in `run_cloud_benchmark.py`: `not_run` fixtures now escalate alongside failures, and GPT-5.3 has been removed from the tier list.

---

## Phase 7: Opus Subagent Benchmark (Claude Code, 8 Hard Fixtures)

**Date**: 2026-05-19
**Protocol**: Claude Code subagents using `a11y-critic` agent definition (Opus 4.6), single-shot.
**Fixtures**: 5 FLAWED + 3 ADVERSARIAL — the tiers where model quality diverges.
**Method**: Direct invocation via `Agent(subagent_type="a11y-critic")` from main session.

### Results

| Fixture | Difficulty | Verdict | Must-find | Quality |
|---------|-----------|---------|-----------|---------|
| tabs-incomplete-aria-selected | FLAWED | REVISE | 1/1 | Full compound analysis |
| multistep-form-error-clearing | FLAWED | REVISE | 1/1 | Found compound dead-end |
| dashboard-heading-inconsistency | FLAWED | REVISE | 1/1 | Upgraded landmarks to MAJOR |
| app-focus-order-illogical | FLAWED | REVISE | 1/1 | Cascading failure analysis |
| async-form-vague-success | FLAWED | REVISE | 1/1 | Found aria-busy timing bug |
| tabbed-nav-vs-tab-pattern | ADVERSARIAL | ACCEPT-W-R | 1/1 | Best-tier (both sides) |
| form-field-vs-summary-errors | ADVERSARIAL | ACCEPT-W-R | 1/1 | Best-tier (both sides) |
| search-focus-stays-in-input | ADVERSARIAL | ACCEPT-W-R | 1/1 | Best-tier (both sides) |

**Total: 8/8 PASS. 100% must-find. All ADVERSARIAL at best-tier verdict quality.**

### Opus vs Other Tiers on Hard Fixtures

| Metric | Opus | Sonnet-think | Haiku | GPT-5.2 |
|--------|------|-------------|-------|---------|
| FLAWED pass rate | 5/5 | 5/5 (inherited) | 5/5 | 5/5 |
| ADVERSARIAL pass rate | 3/3 | 3/3 (resolved) | 0/3 | 3/3 |
| ADVERSARIAL verdict quality | Best | Acceptable | N/A | Acceptable |
| First-pass (no escalation) | Yes | No (needs Haiku triage) | No | Yes |

**Decision**: Opus achieves best-tier verdicts on first pass. This confirms Opus-default routing for planner/critic/auditor in the a11y workflow team.

### Phase 7B: Scout→Critic Workflow Validation

**Method**: Haiku scout (general-purpose, ~8s) → Opus critic (a11y-critic agent) with scout context injected.
**Fixtures**: 1 HAS-BUGS + 1 CLEAN + 1 ADVERSARIAL.

| Fixture | Tier | Scout Time | Scout Flags | Critic Verdict | vs Standalone |
|---------|------|-----------|-------------|----------------|---------------|
| form-validation-missing-aria-describedby | HAS-BUGS | 8s | 4 accurate flags | REJECT (2/2 must-find) | Equivalent |
| button-skip-link-clean | CLEAN | 7s | "None — clean" | ACCEPT (0 FP) | Equivalent |
| tabbed-nav-vs-tab-pattern | ADVERSARIAL | 9s | Semantic tension flagged | ACCEPT-W-R (best-tier) | Equivalent |

**Key finding**: The scout's "no flags — clean" signal on the CLEAN fixture helped the Opus critic avoid the false positive that Haiku alone produces (Haiku gave REVISE on this same fixture in Phase 5B). The scout→critic chain is at least as accurate as standalone Opus invocation, with the added benefit of structured pre-commitment context.

---

## Next Steps

- [x] ~~Build simple `ollama_a11y.py` wrapper (not orchestrator)~~
- [x] ~~Test on CLEAN fixtures (verify models don't manufacture false positives)~~ — 8/8 PASS
- [x] ~~Test a11y-planner protocol on both models~~ — both viable, qwen3 perfect
- [x] ~~Test perspective-audit on qwen3:32b (3 pilot fixtures)~~ — **3/3 PASS, 100% must-find**
- [x] ~~Test discriminator fixture (color-only-status-indicators)~~ — **PASS, key capability confirmed**
- [x] ~~Test deepseek-r1:70b on critic (n=1)~~ — **PASS, more fixtures needed**
- [x] ~~Test qwen3.5:latest on critic (n=6)~~ — **86% must-find, 0% FP, 3-6x faster**
- [x] ~~Complete qwen3.5:latest CLEAN~~ — **4/4 PASS, 0% false positives**
- [x] ~~Complete perspective-audit pilot~~ — **7/7 PASS, 100% must-find, 0% false positives**
- [x] ~~Phase 4A: Full critic benchmark (qwen3:32b, 26 fixtures)~~ — **26/26 PASS, 97% must-find**
- [x] ~~Phase 4C: Full perspective-audit benchmark (qwen3:32b, 25 fixtures)~~ — **20 PASS, 4 WARN, 1 FAIL (page-shell scope)**
- [x] ~~Phase 4D: Test qwen3.5:latest on perspective-audit~~ — **NOT VIABLE (50% empty responses, context exhaustion)**
- [x] ~~Re-run media-player-captions with updated scope note~~ — **FAIL → WARN (scope note fixed it)**
- [x] ~~Test qwen3.5:27b on critic fixtures~~ — **17/33 completed, 100% must-find on 13 HAS-BUGS, stopped due to /think stalls**
- [x] ~~Establish Claude baseline (7 core fixtures)~~ — **All 3 tiers: 7/7 PASS, 100% must-find, 0% FP**
- [x] ~~Phase 5B: Full Claude escalation (33 fixtures)~~ — **Haiku 85%, Sonnet resolves 4/5, Sonnet-think 100%**
- [ ] Run deepseek-r1:70b on remaining critic fixtures (optional)
- [x] ~~Phase 6: Codex/OpenAI escalation (33 fixtures)~~ — **GPT-5.2 91%, full pass at 5.5-low. 3/3 ADVERSARIAL pass (better than Haiku)**
- [x] ~~Phase 7: Opus subagent benchmark (8 hard fixtures)~~ — **8/8 PASS, best-tier verdicts on all ADVERSARIAL. Confirms Opus-default routing.**
- [x] ~~Phase 7B: Scout→Critic workflow validation (3 fixtures)~~ — **3/3 PASS. Haiku scout (~8s) + Opus critic chain works end-to-end.**

## Scoring changelog

- 2026-07-16 (reassurance follow-up, after de-hint): fixture content change, not a scorer change —
  the reassurance-comment class the de-hint entry below deliberately kept was removed, and the pass
  surfaced a structural leak: 7 critic fixtures (4 CLEAN + 3 ADVERSARIAL) had no
  `## Accessibility Issues` cut line, so their Difficulty Level / Notes (expected verdict, grading
  guidance) and — for ADVERSARIAL — "The Ambiguity" tension analysis reached every prompt in every
  recorded lane, blind lanes included. Changes: eval-authored reassurance removed above the cut line
  in 16 perspective + 2 critic fixtures (realistic developer documentation kept); cut-line headings
  inserted in the 7 cut-less critic fixtures — 6 in this pass, modal-complete-clean's via the
  same-day fixture erratum below (CLEAN prompts now end at the features section like
  buggy fixtures; ADVERSARIAL prompts end at Design Rationale); "(CLEAN)" suffixes and
  verdict-bearing tails dropped from the 3 critic + 5 perspective CLEAN h1 titles (closes the
  fixture erratum's open axis (a); axis (b), defect-naming HAS-BUGS titles, remains open); two residual defect-stating hints
  removed (color-only-status-indicators, modal-broken-focus-trap ×2) and five stale below-cut
  answer-key citations of removed `// BUG:` comments rewritten; line references re-anchored where
  affected (video-tutorial-no-captions answer key, `.metadata.yaml`, `.rubric.yaml` — several were
  already stale from the de-hint renumbering and were corrected to verified current anchors);
  committed chain-suite targets regenerated (stale since de-hint); YAML calibration comments added
  to the 7 affected critic rubrics (comments only — `yaml.safe_load` never sees them; the scorer
  reads rubric `notes:`, which was not touched). `test_blind_prompts.py` gains REASSURANCE_PATTERNS
  and now fails on reassurance/verdict text across the same 166 prompts (verified against the
  pre-fix corpus: catches 21/22 previously-leaking fixtures; the autocomplete-fast-timeout excuse
  comment has no machine-checkable invariant and is handled by removal + disclosure). Scorer logic,
  rubric weights, and rubric keywords untouched. Comparability: pre-change rows are verdict-assisted
  upper bounds on critic CLEAN FP-resistance and critic ADVERSARIAL analysis quality, and
  reassurance-assisted on perspective FP-trap avoidance; do not compare 1:1 with post-change runs
  (see the reassurance & verdict-steering disclosure at the top of this file). The perspective
  pilot's "0% FP" calibration (PILOT-REPORT.md) predates this change.

- 2026-07-16 (de-hint): fixture content change, not a scorer change — inline planted-bug hint
  comments stripped from critic (25 fixtures) and perspective (20 fixtures) code above the blind
  cut line; answer-key sections kept; line references in fixture answer keys, `.metadata.yaml`,
  and `.rubric.yaml` renumbered to the new line numbers; scorer logic and rubric keywords
  untouched. `test_blind_prompts.py` now also fails on hint patterns (`\bBUG\b` anywhere,
  any-case `bug` after a comment opener) across critic + perspective + planner prompts composed
  by both runners (166 prompts) and runs in CI. Every critic/perspective row above this line —
  including the 2026-07-13 blind lanes — was produced against hinted prompts (see the
  hint-comment disclosure at the top of this file): treat their must-find/detection numbers as
  hint-assisted upper bounds, and do not compare them 1:1 with post-de-hint runs. Within-lane
  cross-model comparisons are unaffected (identical prompts per lane).

- 2026-07-16 (fixture erratum — `modal-complete-clean`, critic suite): the CLEAN fixture carried
  two real, **unplanted** defects since creation, surfaced by an Opus-tier a11y-critic run
  2026-07-16: (1) the focus-trap selector `'button, [href], input, [tabindex]'` omitted
  `select`/`textarea`/`[contenteditable]` and did not exclude disabled or `tabindex="-1"`
  elements — a trailing `<select>` in `children` was Tab-unreachable because the wrap logic
  preventDefaults at the last *recognized* element; (2) the overlay's bare `onClick={onClose}`
  had no target guard, so any click inside the dialog bubbled up and closed the modal.
  **Resolution** (same as the login-form-clean erratum, 2026-06-14): fixed at source — complete
  `FOCUSABLE_SELECTOR` with a visibility filter, guarded backdrop dismissal (click must start and
  end on the backdrop), focus save/restore isolated from `onClose` identity. The fixture stays
  CLEAN, rubric counts unchanged (must 0 / should 0 / nice 1), both false-positive traps
  preserved, rubric_version 1.0 → 1.1. The same revision moved the fixture's "Difficulty Level /
  should receive ACCEPT" prose below a new `## Accessibility Issues (None Planted — CLEAN
  Baseline)` strip boundary and de-hinted the h1 title (was "Modal Dialog Component (Complete,
  CLEAN)"): before this, **every lane — including the blind ones — saw that verdict hint in its
  prompt** (the 2026-07-13 disclosure's "critic CLEAN prompts were identical all along" holds,
  but identical-with-hint, not unhinted). **Comparability:** committed
  ACCEPT/PASS rows for this fixture are missed-defect data points, not validated false-positive
  avoidance — headline "zero CLEAN false positives" tallies stand as measured but this fixture's
  contribution to them measured hint-following plus defect blindness. Reviewers that raised these
  findings were penalized for being right: gemini-flash's committed artifact flags the overlay
  `onClick` (minor); Claude Haiku's Phase 5B ACCEPT (WARN) "raised structured findings" and
  GPT-5.2/5.2-low WARNs are plausibly the same defects (raw artifacts not retained — cannot be
  adjudicated). The scoring gate itself (`ACCEPT`/`ACCEPT-W-R` = pass, `REVISE` = false alarm)
  meant a reviewer that correctly demanded fixes FAILed. keyboard-a11y-tester cross-validation
  (2026-07-10) is unaffected: its HTML port's content never exercised the latent trap gap and
  pointer dismissal is outside the keyboard persona; the committed port predates the fix and
  stands as a historical artifact. **These rows convert to valid FP-avoidance evidence only via a
  blind re-run against the 1.1 fixture** (now genuinely blind for this fixture). Coordination with
  the concurrent de-hinting workstream (branch `claude/interesting-thompson-78979c`), which strips
  inline `{/* BUG: … */}` code comments that survive above the `## Accessibility Issues` strip
  boundary: that pass does not touch this fixture (it has no BUG comments) and does not rename h1
  titles, so two hinting axes remained open and additive to it — (a) the other 3 critic CLEAN
  fixtures (button-skip-link-clean, interactive-dropdown-clean, search-results-dynamic-clean) still
  carried "should receive clean verdict" prose above the strip boundary plus "(CLEAN)" title
  suffixes; (b) every HAS-BUGS/FLAWED fixture's h1 title names its planted bug outright (e.g.
  "Toast Notification Without Alert Role"), title-level leakage that reaches prompts in all lanes
  and qualifies historical must-find rates the same way the prose hint qualifies CLEAN rows.
  *Axis (a) was closed later the same day by the reassurance follow-up entry above: cut-line
  headings now hold the verdict prose below the strip boundary in all critic CLEAN/ADVERSARIAL
  fixtures, and the "(CLEAN)" suffixes and verdict-bearing title tails ("With Proper/Complete
  Accessibility", "Full") were dropped from the 3 critic and 5 perspective CLEAN h1 titles
  (guarded: `tier suffix in title` pattern in `test_blind_prompts.py`). Axis (b) remains open.*

- 2026-07-13 (post-003): (a) `detect_verdict` gains a middle tier — a bolded conclusion line
  (`**PASS** — …`, last occurrence wins) is recognized before the whole-word fallback ladder, which
  had been matching boilerplate `BLOCK` tokens in audits whose actual conclusion was
  `**PASS** — no CRITICAL or MAJOR findings`; (b) keyword matching in `score_perspective.py` and
  `score_output.py` is quote-normalized (`role='tab'` ≡ `role="tab"`); (c) both runners now strip
  fixture answer keys before prompting (blind protocol; guard: `test_blind_prompts.py`). Re-scores
  of committed artifacts: **gemini critic lane unchanged** (31/33 PASS, same 2 fixtures fail at
  flash and pro); **claude-perspective lane** raw tally moved 20 PASS / 1 WARN / 4 FAIL →
  **20 PASS / 5 WARN / 0 FAIL** (the 4 verdict-artifact FAILs now score their literal PASS
  conclusions; the 5 CLEAN WARNs are the severity-blind finding-count flag, all with 0
  CRITICAL/MAJOR) and keyword-level must-find moved 35/37 → **36/37** (custom-select-combobox
  fixed by quote normalization; the tab-panel-arrow-keys residual is a rubric artifact — its
  scoring keyword is the compound string `role='tablist'/role='tab'/role='tabpanel'`, which no
  prose audit emits verbatim; content coverage is 37/37). Planner scorer untouched.

- 2026-06-11 (plan 002): scorer fixes — two-tier verdict detection in
  score_perspective.py (was: bare substring, BLOCK-first), CLEAN false-positive
  check now uses the declared verdict (was: body-wide BLOCK|REVISE regex),
  truncated `<think>` responses now score `Status: INCOMPLETE` (was: scored as
  normal output), keyword fallback can no longer return an empty list, and the
  40% gate is named MUST_FIND_ABORT_THRESHOLD (escalation gate, not a quality
  bar). Results recorded above this line were produced by the pre-fix scorers
  and are not number-compatible with re-runs. Raw /tmp artifacts were not
  retained, so historical tables stand as-is.

## Planner benchmark (post-002 scoring, 25 fixtures)

**Date**: 2026-06-11 | **Model**: qwen3:32b (Q4_K_M) | **Run**: plan 006 Phase C

First full planner-suite measurement (previously 2/25 fixtures). Produced on the
post-plan-002 scorers — this section sits below the scoring changelog because it is
the first dataset on the corrected basis; it is not number-compatible with the
pre-fix planner rows in earlier sections.

**Scoring method**: `score_planner.py` resolves each must-have criterion through
rubric-supplied `scoring_keywords` in the fixture metadata (exact-match table
retained as fallback, `score_common.fallback_keywords` as last resort with WARN —
zero WARN lines in this run). Instrument validated by a 3-fixture pilot audit with
23/23 criterion agreement, operator-approved: `evals/suites/a11y-planner/PILOT-SCORING-AUDIT.md`.
Raw per-fixture data: `evals/suites/a11y-planner/RESULTS-qwen3-32b.md`.

| Fixture | Must-have hits | Status |
|---------|---------------|--------|
| aria-combobox-autocomplete | 11/11 | PASS |
| aria-data-table-sorting | 10/10 | PASS |
| aria-disclosure-widget | 9/9 | PASS |
| aria-modal-form-validation | 11/11 | PASS |
| aria-tab-dynamic-content | 10/10 | PASS |
| keyboard-breadcrumb | 5/5 | PASS |
| keyboard-button-bar | 6/6 | PASS |
| keyboard-menu-dropdown | 9/9 | PASS |
| keyboard-modal-focus-trap | 10/10 | PASS |
| keyboard-roving-tabindex | 9/9 | PASS |
| sr-article-page | 8/8 | PASS |
| sr-form-field-help | 13/13 | PASS |
| sr-notification-system | 12/12 | PASS |
| sr-product-listing | 8/10 | PASS |
| sr-search-results-live | 11/11 | PASS |
| test-data-table | 13/13 | PASS |
| test-form | 10/11 | PASS |
| test-modal | 9/11 | PASS |
| test-multi-page-audit | 11/11 | PASS |
| test-simple-button | 7/9 | PASS |
| visual-animated-transition | 7/7 | PASS |
| visual-dark-mode | 6/7 | PASS |
| visual-data-viz | 6/6 | PASS |
| visual-form-validation | 10/10 | PASS |
| visual-status-colors | 6/6 | PASS |
| **Aggregate** | **227/235 (96.6%)** | **25/25 PASS** |

Partial-hit fixtures (5): sr-product-listing (8/10), test-form (10/11), test-modal (9/11), test-simple-button (7/9), visual-dark-mode (6/7).

**Caveats**:
- Single local model lane (qwen3:32b). Hosted lanes (Claude subagents, Codex) have
  not run for the planner suite — plan 006 Phase D is operator-cost-gated and was not exercised.
  *(Superseded 2026-06-12: both hosted lanes have run — see "Claude subagent lane"
  and "Codex planner lane" below.)*
- Section-presence keyword scoring is a structural proxy: it verifies a plan contains
  the load-bearing tokens of each must-have criterion, not that the plan is good.
  It cannot distinguish a brilliant plan from a checklist-shaped one (see plan 006
  maintenance notes; an LLM-judge rubric is the next instrument if quality becomes contested).
- One environmental incident during the run: a second resident copy of the model
  (native app on port 11434, kept hot by an unrelated local service) caused GPU
  contention and one 1200s timeout. The affected fixture (visual-data-viz) was re-run
  cleanly after the duplicate was unloaded; scores are unaffected (timing column in the
  raw results file reflects post-fix runs).

### Claude subagent lane (2026-06-12, post-002 scoring)

**Run**: plan 006 Phase D Claude lane, operator-approved 2026-06-12.
**Mechanism**: Claude Code subagents — `Agent(subagent_type="a11y-planner", model="opus")`,
one background subagent per fixture, all 25 in parallel (~12.5 min wall-clock) —
the production mechanism per the standing benchmarking rule.
**Scorer**: same instrument as the qwen3:32b section above (rubric `scoring_keywords`,
zero fallback warnings). Raw artifacts committed: `evals/results/claude-planner/`
(25 response JSONs + README); per-fixture table with timings:
`evals/suites/a11y-planner/RESULTS-claude-opus-subagent.md`.

| Fixture | Must-have hits | Status |
|---------|---------------|--------|
| aria-combobox-autocomplete | 10/11 | PASS |
| aria-data-table-sorting | 10/10 | PASS |
| aria-disclosure-widget | 9/9 | PASS |
| aria-modal-form-validation | 11/11 | PASS |
| aria-tab-dynamic-content | 10/10 | PASS |
| keyboard-breadcrumb | 5/5 | PASS |
| keyboard-button-bar | 6/6 | PASS |
| keyboard-menu-dropdown | 9/9 | PASS |
| keyboard-modal-focus-trap | 10/10 | PASS |
| keyboard-roving-tabindex | 9/9 | PASS |
| sr-article-page | 8/8 | PASS |
| sr-form-field-help | 13/13 | PASS |
| sr-notification-system | 12/12 | PASS |
| sr-product-listing | 10/10 | PASS |
| sr-search-results-live | 11/11 | PASS |
| test-data-table | 13/13 | PASS |
| test-form | 11/11 | PASS |
| test-modal | 11/11 | PASS |
| test-multi-page-audit | 11/11 | PASS |
| test-simple-button | 9/9 | PASS |
| visual-animated-transition | 7/7 | PASS |
| visual-dark-mode | 7/7 | PASS |
| visual-data-viz | 6/6 | PASS |
| visual-form-validation | 10/10 | PASS |
| visual-status-colors | 6/6 | PASS |
| **Aggregate** | **234/235 (99.6%)** | **25/25 PASS** |

The single miss (aria-combobox-autocomplete, "focus remains in input during
navigation") is a keyword-phrasing miss, not a content gap: the response states
"DOM focus stays on the `<input>` at all times" and "focus does NOT move to the
list. It stays in the input" — phrasing outside the criterion's keyword set.
Reported as scored; this is the documented section-presence-proxy limitation.

### Codex planner lane (2026-06-12, post-002 scoring)

**Run**: plan 010 Codex planner lane, operator-approved 2026-06-12 (in-session).
**Mechanism**: OpenAI Codex CLI (`codex-cli 0.125.0`), model **gpt-5.5 effort=low**
(tier `5.5-low`), one `codex exec` call per fixture (25 total, sequential — the CLI
is not parallelized), via `python3 ollama/run_cloud_benchmark.py codex-planner-all 5.5-low`.
Per-fixture wall-clock 47.7s–170.9s (no 300s timeouts).
**Scorer**: same instrument as the lanes above (rubric `scoring_keywords`, zero
fallback warnings). Raw artifacts committed: `evals/results/codex-planner/`
(25 response JSONs + README).

| Fixture | Must-have hits | Status |
|---------|---------------|--------|
| aria-combobox-autocomplete | 10/11 | PASS |
| aria-data-table-sorting | 10/10 | PASS |
| aria-disclosure-widget | 9/9 | PASS |
| aria-modal-form-validation | 11/11 | PASS |
| aria-tab-dynamic-content | 10/10 | PASS |
| keyboard-breadcrumb | 5/5 | PASS |
| keyboard-button-bar | 6/6 | PASS |
| keyboard-menu-dropdown | 9/9 | PASS |
| keyboard-modal-focus-trap | 10/10 | PASS |
| keyboard-roving-tabindex | 9/9 | PASS |
| sr-article-page | 8/8 | PASS |
| sr-form-field-help | 13/13 | PASS |
| sr-notification-system | 12/12 | PASS |
| sr-product-listing | 10/10 | PASS |
| sr-search-results-live | 11/11 | PASS |
| test-data-table | 13/13 | PASS |
| test-form | 11/11 | PASS |
| test-modal | 11/11 | PASS |
| test-multi-page-audit | 11/11 | PASS |
| test-simple-button | 9/9 | PASS |
| visual-animated-transition | 7/7 | PASS |
| visual-dark-mode | 7/7 | PASS |
| visual-data-viz | 6/6 | PASS |
| visual-form-validation | 10/10 | PASS |
| visual-status-colors | 6/6 | PASS |
| **Aggregate** | **234/235 (99.6%)** | **25/25 PASS** |

This lane matches the Claude Opus subagent lane exactly — same 234/235, same
25/25 PASS, and the same single miss (aria-combobox-autocomplete, "focus remains
in input during navigation"), a keyword-phrasing miss rather than a content gap
(the plan states focus stays in the input). Two different hosted families landing
on an identical section-hit profile is consistent with the section-presence proxy:
the bar measures whether the load-bearing tokens of each criterion are present, and
both families clear it — it does not discriminate plan quality between them.

**Caveats**:
- **Tier deviation**: plan 010's default tier is `5.2-low`, but OpenAI no longer
  accepts `gpt-5.2` (or the CLI-default `gpt-5.3-codex`) on ChatGPT-account Codex
  ("model not supported"). This lane ran **gpt-5.5 (low)** — same family, low
  effort, mirroring the critic lane's full-pass-tier philosophy. Numbers are not
  tier-comparable to the historical GPT-5.2 critic rows.
- Single hosted tier; section-presence keyword scoring is the same structural proxy
  documented for the lanes above (it verifies load-bearing tokens, not plan quality).

**Cross-lane planner summary (same instrument, same 25 fixtures)**:

| Lane | Aggregate | PASS | Partial-hit fixtures |
|------|-----------|------|----------------------|
| qwen3:32b (local, 2026-06-11) | 227/235 (96.6%) | 25/25 | 5 |
| Claude Opus subagents (2026-06-12) | 234/235 (99.6%) | 25/25 | 1 |
| Codex GPT-5.5 low (2026-06-12) | 234/235 (99.6%) | 25/25 | 1 |

All three lanes share the same 25 fixtures and the same `score_planner.py`
instrument. The Codex lane ran at **gpt-5.5 (low)**, not plan 010's default
`5.2-low` — OpenAI no longer accepts `gpt-5.2` or the CLI-default `gpt-5.3-codex`
on ChatGPT-account Codex; see the Codex planner lane subsection above for the
tier-deviation caveat.

## Gemini baseline — critic suite (2026-06-12, post-002 scoring)

**Run**: plan 007 (operator-approved 2026-06-12). **Transport**: authenticated
`gemini` CLI v0.46.0 (plan 007 amendment — mirrors the codex lane), per-call
isolation: neutral temp cwd + `--skip-trust` (prevents the CLI loading this
repo's own `.agents` skills into the model prompt), `--approval-mode default`,
headless preamble forbidding file writes (the gate-1 probe caught the CLI agent
saving — and then hallucinating — a report file instead of answering; the
fixed adapter re-probed 3/3 PASS before the full run).
**Raw artifacts committed**: `evals/results/gemini/` (33 flash responses + 2
pro error placeholders). Per-call token counts in each `_benchmark` block;
CLI harness overhead ~18.7K input tokens/call.

| Tier | Ran | Pass | Fail | Infra-error |
|------|-----|------|------|-------------|
| Gemini 2.5 Flash | 33 | 31 (94%) | 2 | 0 |
| Gemini 2.5 Pro (escalation) | 2 | 0 | 0 | 2 (capacity exhausted — resumable) |

- **Must-find, criteria level (HAS-BUGS + FLAWED)**: 130/132 (98%); 26/26
  fixtures PASS. Partial-hit fixtures: file-input-no-labels (3/4),
  tooltip-no-role-no-association (2/3).
- **CLEAN**: 3/4 PASS — 1 false positive (interactive-dropdown-clean).
- **ADVERSARIAL**: 2/3 — form-field-vs-summary-errors at 0% must-articulate;
  search-focus-stays-in-input and tabbed-nav-vs-tab-pattern at 100%.
- **Cheap-tier ladder across lanes**: Haiku 85% → GPT-5.2 91% → Gemini 2.5
  Flash 94% → qwen3:32b 100% (local).
- **Pro escalation pending**: the 2 flash failures escalate to
  gemini-2.5-pro, which was capacity-exhausted on this account at run time
  (6 retries with backoff, then the resumable errored lane). Re-run
  `python3 ollama/run_cloud_benchmark.py gemini-escalate` after quota reset
  to complete the ladder; the flash rows above are final either way.
- Zero scorer fallback-keyword warnings; every number re-derives from
  `evals/results/gemini/` via `score_output.py`.

## Claude subagent lane — perspective suite (2026-07-13, BLIND)

**Run**: closes the "Claude perspective-audit escalation" backlog item via the subagent mechanism
(the API-escalation variant remains open — blocked on a valid `ANTHROPIC_API_KEY`; it measures the
Haiku-first cost ladder, which subagents cannot).
**Mechanism**: Claude Code subagents — `Agent(subagent_type="general-purpose", model="opus")`, one
background subagent per fixture, 25 in parallel, prompts composed identically to
`run_cloud_benchmark.py` (system prompt + metadata escalation block).
**Protocol difference — first BLIND lane**: fixtures truncated at `## Accessibility Issues` before
prompting; composed prompts assert-verified answer-free. Rationale: both runners were found feeding
the full fixture answer key to models (`load_fixture()` reads raw fixtures; truncation logic never
existed per `git log -S`) — every earlier critic/perspective row in this document is therefore
non-blind, and this lane's numbers must not be compared 1:1 against them. Remediation (runner
truncation, caveats on published rows, blind re-runs) is tracked as follow-up work.
**Hint-comment caveat (2026-07-16)**: answer-key-blind but not hint-blind — 20/25 perspective
fixtures still carried inline `// BUG:` hint comments at run time (de-hinted 2026-07-16; see the
hint-comment disclosure). Detection numbers below are hint-assisted upper bounds; the CLEAN
false-positive result is unaffected by hints (CLEAN fixtures carried none), though two perspective
CLEAN fixtures carried reassurance comments until the same-day follow-up (see the reassurance &
verdict-steering disclosure) — treat the CLEAN-FP result as measured against slightly softer traps
than the current fixtures.
**Scorer**: `score_perspective.py`, unmodified for comparability. Raw artifacts committed:
`evals/results/claude-perspective/` (25 response JSONs + scorer outputs + README with adjudication
receipts); per-fixture table: `evals/suites/perspectives/RESULTS-claude-opus-subagent.md`.

| Measure | Pre-003 scorer | Post-003 scorer | Content-adjudicated |
|---|---|---|---|
| Fixture statuses | 20 PASS / 1 WARN / 4 FAIL | **20 PASS / 5 WARN / 0 FAIL** | **25/25** correct verdicts |
| Must-find (37 items across 20 fixtures) | 35/37 | **36/37** | **37/37** (residual is a compound rubric keyword no prose emits verbatim) |
| CLEAN false positives (MAJOR/CRITICAL) | n/a (4 verdict-extraction FAILs) | 0 (5 WARNs are the severity-blind finding-count flag) | **0 across all 5 CLEAN fixtures** — every CLEAN audit concludes `**PASS** — no CRITICAL or MAJOR findings` |

The pre-003 deductions were receipted scorer artifacts (verdict fallback ladder matching boilerplate
`BLOCK` when the audit's verdict line is formatted `**PASS** — …`; quote-sensitive keyword matching);
they motivated the post-003 scorer fixes recorded in the Scoring changelog, and the re-score confirms
the adjudication. Run integrity: 24/25 agents clean on first pass; one agent returned injected
non-task instructions with zero tool calls and was retried successfully (documented in the lane README).

## Ollama blind re-run lane — qwen3:32b (2026-07-13, BLIND)

**Run**: first blind **local** lane; gives the historical non-blind qwen3:32b critic and perspective
rows their blind counterparts (the remediation item from the blind-protocol disclosure).
**Machine protocol**: dedicated `127.0.0.1:11435` ollama server (0.31.1), Ollama.app quit,
full Metal offload verified (`size == size_vram`, 24.7 GB); `OLLAMA_URL` override +
`BENCHMARK_RESULTS_DIR` → `evals/results/ollama-blind/` (raw JSONs + per-fixture scorer outputs
committed — unlike the historical /tmp runs, these artifacts are re-scorable).
**Protocol**: identical prompts/settings to the historical lanes except post-003 answer-key
stripping (guard-verified). **Scorer**: post-003 `score_output.py` / `score_perspective.py`.
**Wall-clock**: critic 33 fixtures in 1.45 h; perspective 25 in 1.36 h.
**Hint-comment caveat (2026-07-16)**: answer-key-blind but not hint-blind — 24/33 critic and
20/25 perspective fixtures still carried inline `// BUG:` hint comments at run time (de-hinted
2026-07-16; see the hint-comment disclosure). "Confirmed blind" below means confirmed with
answer keys withheld: must-find/detection numbers are hint-assisted upper bounds, while the
CLEAN rows (critic 4/4, perspective CLEAN-FP finding) are unaffected by hints — no CLEAN
fixture carried hints. **Reassurance/verdict caveat (2026-07-16 follow-up)**: the critic
CLEAN 4/4 row is nonetheless a verdict-assisted upper bound — at run time the 4 critic CLEAN
fixtures had no cut line, so their prompts included "**CLEAN** — should receive a clean verdict"
grading text (the 3 critic ADVERSARIAL fixtures likewise included their grading notes); the
perspective CLEAN-FP finding stands structurally, measured against slightly softer traps
(reassurance comments since removed). See the reassurance & verdict-steering disclosure.
**Outcome (de-hinted re-run, same day)**: the upper bound is now measured for qwen3:32b —
nil on critic (67/68 content-adjudicated in both lanes), −1 must-find item on perspective
(`map-interface-zoom`); and this lane's perspective CLEAN characterization (4/5 wrong verdicts)
proved run-unstable — the de-hinted re-run drew 1/5 wrong on byte-identical CLEAN prompts. The
de-hinted lane also ran before the verdict-steering fix, so its critic CLEAN rows (except
`modal-complete-clean`, whose cut line landed with the fixture erratum) and ADVERSARIAL rows
carry the same verdict-assisted caveat. See the de-hinted lane section below.

### a11y-critic (33 fixtures) — historical numbers CONFIRMED blind

| Measure | Blind (post-003) | Historical non-blind (2026-05-15) |
|---|---|---|
| Fixture statuses | **33/33 PASS** | 33/33 PASS |
| Must-find aggregate | **66/68 (97.1%)** scorer / **67/68 (98.5%)** content-adjudicated | ~97% (pre-002 scorer basis) |
| CLEAN false positives | **0** structured findings, 4/4 correct verdicts | 0 |
| ADVERSARIAL | 3/3 ACCEPT-WITH-RESERVATIONS, 3/3 must-articulate | 3/3 |
| toast `role="alert"` | **found** (4/4) | missed (3/4) |

The two scorer-level misses: one keyword artifact (`<div>` literal vs prose "div"), one genuine
partial miss (scroll-to-load discoverability raised as impact, not finding) — receipts in
`evals/results/ollama-blind/README.md`. Critic CLEAN fixtures carry no answer sections, so this
suite's CLEAN prompts were never affected by the leak; the blind confirmation covers the
detection tiers.

**Timing**: FLAWED median 224 s and ADVERSARIAL median 222 s vs historical 3,508 s / 3,007 s —
same model/quant/settings on an uncontended GPU. The Phase 4A "extended reasoning on subtle
bugs" slowdown was substantially GPU contention (claude-smart's :11434 traffic), not intrinsic
think-time; treat Phase 4A wall-clock numbers as contended-machine artifacts.

### perspective-audit (25 fixtures) — detection confirmed; CLEAN resistance was answer-key-dependent

| Measure | Blind (post-003) | Historical non-blind (Phase 4C) |
|---|---|---|
| Fixture statuses | **20 PASS / 1 WARN / 4 FAIL** | 20 PASS / 4 WARN / 1 FAIL |
| HAS-BUGS + ADVERSARIAL | **20/20 PASS**, no LOW-perspective leakage | 20/20 PASS |
| Must-find (37 items) | **36/37** scorer / **37/37** content-adjudicated (residual = the same compound-keyword rubric artifact as the Claude lane) | 37/37 |
| CLEAN verdicts | **1/5 correct** (4 FAIL: REVISE/REVISE/REVISE/BLOCK) | 4/5 correct (4 WARN + 1 FAIL) |

All four CLEAN FAILs are genuine model output, not scorer artifacts — the audits literally
conclude REVISE/BLOCK (receipts in the lane README): two fixtures get manufactured
CRITICAL/MAJOR findings (`nav-menu-landmarks`: page-shell over-flagging — missing `<title>`/
`lang` CRITICALs against a component fixture; `dashboard-text-labels`: a contrast claim
contradicted by the fixture's documented ratios), and two get verdict inflation over
MINOR-level content (`login-form-clean` declares "MAJOR finding present" contradicting its own
findings table; `media-player-captions` REVISEs over two human-verification open questions).

**Interpretation**: every perspective CLEAN fixture embeds an answer section stating
"**NONE.** …correctly implemented", which the non-blind run showed the model. With it, qwen3:32b
echoed PASS; without it, the model's documented page-shell over-flagging and severity inflation
surface as false positives on 4/5 clean components. **The historical "0% false positives"
claim survives blind for the critic suite only.** Detection quality (must-find, coverage,
escalation discipline) is unaffected by blinding. Comparison caveat: the historical Phase 4C row
was scored pre-002/pre-003, so its WARN/FAIL split is not scorer-identical either — but the
verdict flip on the four receipted fixtures is model behavior, not scoring drift.

### Blind lanes for the other historical local models (same day)

First full-suite runs for both models — the historical rows were n=7 (4 CLEAN + 3 HAS-BUGS
only, never the FLAWED/ADVERSARIAL tiers), so these lanes widen coverage as well as blind it.
Perspective is intentionally skipped for both: qwen3.5:latest is documented NOT-VIABLE
(context exhaustion), and llama3.3:70b has no historical perspective row to counterpart.

| Measure | qwen3.5:latest (6.6 GB) | llama3.3:70b (42 GB) |
|---|---|---|
| Fixture statuses | **33/33 PASS** | **33/33 PASS** |
| Must-find aggregate | **67/68 (98.5%)** scorer | 63/68 (92.6%) scorer / **66/68 (97.1%)** content-adjudicated |
| CLEAN | 4/4 correct verdicts, 0 structured findings | 4/4 PASS |
| ADVERSARIAL | 3/3 valid verdicts, 3/3 articulated | 3/3 PASS |
| Wall-clock | 0.33 h base lane (median **34 s**/fixture) + 4 override re-runs | 1.66 h (median 171 s), zero truncations |
| Historical (non-blind, n=7) | 7/7 PASS, 86% must-find | 7/7 PASS, 86% must-find |

**qwen3.5:latest context-ceiling receipts (mechanism, not model failure).** At the lane-standard
`num_ctx=16384`, 4 of 33 fixtures were mechanically truncated: 3 produced *empty* responses
(`done_reason=length` while still in the thinking phase — the prompts alone tokenize to
15,773–16,102 tokens on this model, leaving exactly 335/282/611 tokens of room, matching the
observed eval_counts token-for-token; reproducible across 2 attempts each), and 1
(`multistep-form-error-clearing`, prompt 16,899 tokens — larger than the whole 16K window) cut
mid-audit ≈ the 8192 `num_predict` default. All 4 were re-run at `num_ctx=32768` (the
accommodation pattern `PERSPECTIVE_CTX` already establishes per-model), completed with
`done_reason=stop`, and their artifacts carry explicit `num_ctx_override` provenance. With the
ceiling removed the model scores 33/33 — including finding the multistep planted bug it had
appeared to miss. Practical routing note: **qwen3.5:latest needs ≥32K num_ctx on long critic
fixtures**; its historical "/think stall" reputation (and plausibly qwen3.5:27b's) is context
exhaustion, not reasoning failure.

**llama3.3:70b adjudication.** 3 of the 5 scorer-level misses are keyword artifacts with the
content present verbatim (file-input type restrictions raised as help-text association; tooltip
"no announcement for screen reader users" + hover-not-focus; video-player "No visible or
accessible caption toggle button" vs keyword 'controllable'); 2 are genuine (megamenu arrow-key
navigation; infinite-scroll discoverability).

**Cross-model observation**: the `infinite-scroll-no-announcement` item "Scroll-to-load
mechanism not discoverable" is missed blind by all three local models (each surfaces the
impact, none raises it as a standalone finding) — the hardest item in the suite for local
models, worth remembering when reading per-model must-find deltas.

## Ollama de-hinted re-run lane — qwen3:32b (2026-07-16, first post-de-hint rows)

**Run**: the remediation lane promised by the hint-comment disclosure — the first rows in this
file produced against comment-de-hinted fixtures. Per the Scoring changelog (2026-07-16
de-hint), **not 1:1 comparable with any row above this section**; the paired lane for reading
deltas is the 2026-07-13 blind lane, via the attribution ledger below.
**Machine protocol**: identical to the blind lane — dedicated `127.0.0.1:11435` server (Ollama
0.31.1), Ollama.app quit (`*:11434` reverted to the OrbStack container), full Metal offload
verified (`size == size_vram`, 24.2 GB). The app-server stall behavior was independently
re-verified the same day (single CLEAN fixture 15+ min stalled on the app server vs 66–215 s
dedicated).
**Fixture state**: main@ff982fb — de-hint pass (c0d21cc/0011346/f1f0b2b) + `modal-complete-clean`
repair (6420ea9). Guards green at run time: `test_blind_prompts.py` (166 prompts, no answer-key
markers, no hint comments) and the `\bBUG\b` leak one-liner (`[]`).
**Attribution ledger — the lanes differ by more than the de-hint**: (a) `modal-complete-clean`
conflates the component repair with its verdict-hint strip (both in 6420ea9) — the other 32
critic / 25 perspective fixtures differ only on the hint-comment axis; (b) the critic system
prompt gained 3 lines between lanes (native-HTML-first rule, 4d8f196) — the perspective system
prompt is byte-identical; (c) at run time the 3 non-modal critic CLEAN and all 3 ADVERSARIAL
fixtures had no blind cut line — their verdict prose and Ambiguity/grading sections reached
this lane's prompts (named after this run by the reassurance & verdict-steering disclosure),
so those rows are **verdict-assisted upper bounds here too**; PR #4 closed the CLEAN-title
axis after this run, and the bug-naming-title axis stays open; (d) reassurance comments were
still present at run time (removed suite-wide by PR #4 afterward), so this lane's FP traps are
softer than the post-PR-4 corpus — the post-PR-4 re-baseline is the open follow-up lane.
**Wall-clock**: critic 33 fixtures in 1.57 h (median 159 s), perspective 25 in 1.38 h (median
192 s) — the uncontended dedicated-server profile reproduced, no FLAWED/ADVERSARIAL blowup.
Full receipts and per-fixture adjudication: `evals/results/ollama-dehinted/README.md`.

### a11y-critic (33 fixtures) — detection survives de-hinting intact

| Measure | De-hinted (this lane) | Hinted blind lane (2026-07-13) |
|---|---|---|
| Fixture statuses | **33/33 PASS** | 33/33 PASS |
| Must-find aggregate | **67/68 (98.5%) scorer / 67/68 content-adjudicated** | 66/68 scorer / 67/68 content |
| CLEAN false positives | **0 structured findings**, 4/4 correct verdicts — incl. the repaired `modal-complete-clean` (ACCEPT-W-R, 0 findings: its **first valid FP-avoidance data point**, and the lane's only unassisted CLEAN row — the other 3 prompts carried verdict prose, ledger c) | 0 findings, 4/4 (modal row = hint-following + defect blindness per the erratum; all 4 verdict-assisted) |
| ADVERSARIAL | 3/3 ACCEPT-W-R, 3/3 tradeoffs articulated (verdict-assisted — prompts carried the Ambiguity/grading sections, ledger c) | 3/3 (same assist) |
| Verdict inflation | 5 REJECT (3 where rubric expects REVISE) | 7 REJECT |

The single miss is the same in both lanes and content-adjudicates as genuine both times:
`infinite-scroll-no-announcement` scroll-to-load discoverability (impact mentioned, never raised
as a finding) — the cross-model hardest item holds de-hinted. The scorer-level +1 is the
`expandable-section-no-button` `<div>` keyword artifact resolving (the audit emits the literal
`<div>` this run, plausibly nudged by the new native-HTML-first rule; content coverage was 4/4
in both lanes). **For qwen3:32b on this suite, the measured hint effect on detection is nil.**

### perspective-audit (25 fixtures) — one hint-dependent miss; the CLEAN flip is variance

| Measure | De-hinted (this lane) | Hinted blind lane (2026-07-13) |
|---|---|---|
| Fixture statuses | **20 PASS / 4 WARN / 1 FAIL** | 20 PASS / 1 WARN / 4 FAIL |
| HAS-BUGS + ADVERSARIAL | **20/20 PASS** | 20/20 PASS |
| Must-find (37 items) | **35/37 scorer / 36/37 content** | 36/37 scorer / 37/37 content |
| CLEAN verdicts | **4/5 correct** (1 FAIL) | 1/5 correct (4 FAIL) |

The content-level miss is the run's one measured de-hint effect: `map-interface-zoom`'s
18×18px target-size defect — found in the hinted lane, absent from this audit (no discussion of
control size at all), named by the stripped hint comment. The other scorer residual is the
`tab-panel-arrow-keys` compound-keyword rubric artifact, present in every lane.

**The CLEAN flip (4/5 wrong → 1/5 wrong) is run-to-run variance, not a de-hint effect.** No
CLEAN perspective fixture carried hints; none of the five fixture/metadata files changed since
2026-06-13 or earlier; the perspective system prompt is byte-identical across lanes — the five
CLEAN prompts are **byte-identical in both runs** (temperature 0.3). Stable across the two
draws: correct PASS on `article-page-clean`; wrong REVISE on `media-player-captions` (this run
manufactures a MAJOR demanding `aria-expanded` on a native `<details>`/`<summary>` disclosure,
miscited as 2.4.4; the blind run over-escalated two MINOR open questions); and
`nav-menu-landmarks`' manufactured page-shell findings (missing `<title>`/`lang` against a
component fixture) in both runs with only the verdict moving (BLOCK → REVISE, the latter
metadata-accepted). Everything else flipped. **Neither draw is the model's stable CLEAN rate —
cite both or neither.** The routing rule (don't route CLEAN-confirmation perspective audits to
local models without a second opinion) is reinforced, with verdict instability as the mechanism.
