# Eval Suite Gap-Fill Plan

**Created**: 2026-05-15
**Purpose**: Close all gaps across the 3 eval suites + Ollama benchmarks so every suite is production-ready.
**Note**: This plan supersedes the dashboard at `~/.agent/diagrams/a11y-testing-architecture.html` — fixture counts there are stale (says 20 critic / 1 real planner; actual is 25 critic / 10 real planner).

---

## Current State

| Area | Built | Stubs/Missing | Benchmarked | Blocking Issues |
|------|-------|---------------|-------------|-----------------|
| Critic eval | 25 fixtures (5 CLEAN + 20 HAS-BUGS) | 8 fixtures missing rubrics; 0 FLAWED; 0 ADVERSARIAL | 7/25 Ollama | Missing rubrics, missing tiers |
| Planner eval | 10 real (5 ARIA + 5 keyboard) | 15 stubs + eval.yaml ID mismatch | 2/25 Ollama | Stubs need real content; eval.yaml out of sync |
| Perspectives eval | 30 fixtures (all real) | 0 | 7/30 Ollama pilot | Needs full benchmark run |
| Ollama wrapper | Production-ready | N/A | Yes | N/A |

---

## Phase 1: Fix Structural Issues (do first)

### 1A. Critic — Write 8 missing rubrics

These fixtures have `.md` + `.metadata.yaml` but no `.rubric.yaml`:

| Fixture | Type | Priority |
|---------|------|----------|
| `form-validation-missing-aria-describedby` | HAS-BUGS | HIGH (already benchmarked) |
| `tabs-missing-arrow-nav` | HAS-BUGS | HIGH (already benchmarked) |
| `button-skip-link-clean` | CLEAN | HIGH (already benchmarked) |
| `modal-complete-clean` | CLEAN | HIGH (already benchmarked) |
| `search-results-dynamic-clean` | CLEAN | HIGH (already benchmarked) |
| `data-table-missing-scope` | HAS-BUGS | MEDIUM |
| `heading-hierarchy-skipped` | HAS-BUGS | MEDIUM |
| `loading-state-missing-aria-busy` | HAS-BUGS | MEDIUM |

**Pattern**: Copy structure from `aria-disclosure-widget.rubric.yaml` (critic version at `evals/suites/a11y-critic/rubrics/interactive-dropdown-clean.rubric.yaml`). Each rubric needs:
- `scoring_method: hybrid`
- `dimensions` array with must_find (wt 3), should_find (wt 2), nice_to_find (wt 1), false_positive_trap (wt -2), evidence_quality (wt 1), format_compliance (wt 1)
- `expected_findings` matching the fixture's `.metadata.yaml`
- `scoring_thresholds` (excellent 90-100, good 75-89, adequate 60-74, weak 40-59, poor 0-39)
- `expected_reviewer_performance` ranges for all 3 conditions

**Effort**: ~20 min per rubric. The metadata already has expected findings — rubric just formalizes them.

### 1B. Planner — Reconcile eval.yaml with actual files

The eval.yaml lists fixture IDs that don't exist as files. Three domains are completely mismatched:

| eval.yaml ID | Actual file | Action |
|--------------|-------------|--------|
| `sr-article-page` | `screenreader-landmark-regions` | Decide: rename file or update eval.yaml |
| `sr-search-results-live` | `screenreader-liveregion` | Same |
| `sr-product-listing` | `screenreader-image-context` | Same |
| `sr-notification-system` | `screenreader-form-errors` | Same |
| `sr-form-field-help` | `screenreader-skiplinks` | Same |
| `visual-status-colors` | `visual-color-contrast` | Same |
| `visual-animated-transition` | `visual-reduced-motion` | Same |
| `visual-dark-mode` | `visual-responsive-design` | Same |
| `visual-form-validation` | `visual-focus-indicator` | Same |
| `visual-data-viz` | `visual-text-resize` | Same |
| `test-simple-button` | `testing-axe-automation` | Same |
| `test-form` | `testing-keyboard-audit` | Same |
| `test-modal` | `testing-screenreader-audit` | Same |
| `test-data-table` | `testing-wcag-compliance` | Same |
| `test-multi-page-audit` | `testing-mobile-accessibility` | Same |

**Decision needed**: The eval.yaml IDs are more descriptive for the eval purpose. The actual files have different (sometimes better) topic coverage. Two options:
1. **Replace stub files** with new files matching eval.yaml IDs (recommended — stubs are generic anyway)
2. **Update eval.yaml** to match existing file names (faster but topics diverge from eval design)

**Recommendation**: Option 1. The stubs are 42-line templates with no real content. Generating new files with the eval.yaml IDs is the same effort as filling in the stubs but produces a coherent eval suite.

**Cleanup**: After generating replacements, `git rm` the 15 old stub files (`screenreader-*.md`, `screenreader-*.metadata.yaml`, `visual-*.md`, `visual-*.metadata.yaml`, `testing-*.md`, `testing-*.metadata.yaml` and their rubrics). Don't leave dead stubs alongside the new files.

---

## Phase 2: Generate Planner Fixture Content (biggest gap)

### Fixtures to generate

**15 stub fixtures** need real content. Each fixture needs 3 files:

| File | Template | Size (real) |
|------|----------|-------------|
| `{id}.md` | Specific feature description, context, requirement, scope hints, success criteria | 50-80 lines |
| `{id}.metadata.yaml` | Scenario, expected sections, evaluation criteria, must/should/nice findings, false positive traps | 95-115 lines |
| `{id}.rubric.yaml` | Hybrid scoring, dimension weights, composite formula, expected performance, verdict expectations | 140-190 lines |

**Reference fixtures** (fully developed — use as templates):
- TRIVIAL: `aria-disclosure-widget` (67L / 98L / 190L)
- MODERATE: `aria-combobox-autocomplete` (69L / 115L / 190L)
- COMPLEX: `aria-data-table-sorting` (72L / 106L / 146L)
- AMBIGUOUS: `aria-modal-form-validation` (82L / 114L / 165L)

### Generation order (by domain)

Generate domain-by-domain so you can cross-reference within each domain for consistency.

#### Domain 3: Screen Reader Experience (5 fixtures — all stubs)

Replace `screenreader-*` stubs with eval.yaml IDs:

| New ID | Difficulty | What to describe |
|--------|-----------|-----------------|
| `sr-article-page` | TRIVIAL | Blog article with heading hierarchy, landmark regions, image alt text, time element. Plan should cover semantic structure, heading order, alt text strategy, landmark coverage. |
| `sr-search-results-live` | MODERATE | Search results page with live-updating result count, filter chips, sort controls. Plan should cover aria-live for count, aria-relevant, grouped results, filter state communication. |
| `sr-product-listing` | MODERATE | E-commerce product grid with sort, filter, price ranges, add-to-cart. Plan should cover grid semantics, sort state (aria-sort), price announcement, cart confirmation. |
| `sr-notification-system` | COMPLEX | Real-time notification panel with multiple priority levels (info/warning/error), dismissible, badge count. Plan should cover aria-live regions by priority, assertive vs polite, badge updates, notification history. |
| `sr-form-field-help` | AMBIGUOUS | Complex form with field-level help text, conditional fields, progressive disclosure of help. Plan should cover aria-describedby, help text timing (before vs after), conditional field announcements, error vs help disambiguation. |

#### Domain 4: Visual & Cognitive Accessibility (5 fixtures — all stubs)

Replace `visual-*` stubs:

| New ID | Difficulty | What to describe |
|--------|-----------|-----------------|
| `visual-status-colors` | TRIVIAL | Status indicator dots (red/yellow/green) next to list items. Plan should cover 1.4.1 (not color alone), text labels, icon alternatives, sufficient contrast. |
| `visual-animated-transition` | MODERATE | Page transition with slide/fade animation between routes. Plan should cover prefers-reduced-motion, animation duration limits, focus management during transition, content not hidden by animation. |
| `visual-dark-mode` | MODERATE | Dark mode toggle with system preference detection. Plan should cover contrast ratios in both modes, focus indicator visibility, forced-colors media query, no information loss between modes. |
| `visual-form-validation` | COMPLEX | Multi-step form with inline validation, error summary, field-level error display. Plan should cover error color + icon (not color alone), error message contrast, focus management on error, cognitive load (one error at a time vs all). |
| `visual-data-viz` | AMBIGUOUS | Interactive chart (bar/line) with hover tooltips, legend, axis labels. Plan should cover color alternatives (patterns/textures), keyboard-navigable data points, screen reader data table fallback, zoom/reflow behavior. |

#### Domain 5: Testing & Audit Planning (5 fixtures — all stubs)

Replace `testing-*` stubs:

| New ID | Difficulty | What to describe |
|--------|-----------|-----------------|
| `test-simple-button` | TRIVIAL | Plan automated and manual testing for a custom button component. Simple scope: axe-core scan, keyboard test (focus, activation), screen reader test (name, role). |
| `test-form` | MODERATE | Plan testing strategy for a registration form with validation. Cover axe-core, keyboard navigation order, error announcement testing, screen reader form mode, visual regression for focus indicators. |
| `test-modal` | MODERATE | Plan testing strategy for a modal dialog. Cover focus trap testing, escape key, focus restoration, background inert, screen reader mode announcement, visual regression. |
| `test-data-table` | COMPLEX | Plan testing strategy for a sortable data table with pagination. Cover table semantics testing, sort state testing, keyboard navigation of cells, screen reader table mode, responsive behavior testing. |
| `test-multi-page-audit` | COMPLEX | Plan a full-page accessibility audit methodology for a 20-page site. Cover page sampling strategy, tool selection (axe/WAVE/manual), testing matrix (automated + keyboard + SR + visual), prioritization framework, reporting template. |

### Generation process (per fixture)

For each fixture, generate all 3 files in one pass:

1. **`.md` file**: Write a specific, realistic feature description. Include:
   - Feature Description (what the component does, not generic)
   - Context (platform, framework, compliance target, AT list, scope, constraints)
   - Requirement (what the plan should cover)
   - Scope Hints (difficulty-calibrated: TRIVIAL = 1-2 pages, MODERATE = 3-4, COMPLEX = 5-7, AMBIGUOUS = varies)
   - What Success Looks Like (specific criteria with checkmarks)
   - What Would Be Below Expectations (specific anti-patterns with X marks)

2. **`.metadata.yaml` file**: Specify grading criteria. Include:
   - `fixture_id`, `name`, `description`, `language`, `framework`, `difficulty`, `domain`, `work_type`, `risk_level`
   - `scenario` with feature, user_need, compliance_target, AT list, scope, constraints
   - `expected_plan_sections` (all 9 phases)
   - `key_evaluation_criteria`
   - `expected_findings` with `must_have`, `should_have`, `nice_to_have` (specific items)
   - `notes` with expected verdict and expected scores per condition

3. **`.rubric.yaml` file**: Formalize scoring. Include:
   - `scoring_method: hybrid` with 70/30 split
   - `dimensions` with weights (completeness:3, apg:3, wcag:3, specificity:2, multi_perspective:2, testing:2, calibration:1 — plus domain-specific dimensions for MODERATE+)
   - `composite_score_formula`
   - `scoring_thresholds`
   - `expected_reviewer_performance` for all 3 conditions
   - `verdict_expectations`
   - `expected_findings_baseline` percentages
   - `outlier_indicators`

**Effort**: ~15-20 min per fixture triplet using the reference fixtures as templates. ~4-5 hours for all 15.

### Partially-developed keyboard fixtures (verify, don't regenerate)

These 5 keyboard fixtures have real `.md` content (51-62 lines) but some have stub-level metadata (53L) and rubrics (58-73L):

| Fixture | .md | .metadata | .rubric | Action |
|---------|-----|-----------|---------|--------|
| `keyboard-button-bar` | 62L (real) | 54L (stub-ish) | 73L (partial) | Enrich metadata + rubric |
| `keyboard-menu-dropdown` | 54L (real) | 57L (partial) | 59L (stub) | Enrich rubric |
| `keyboard-breadcrumb` | 51L (real) | 53L (stub-ish) | 129L (real) | Enrich metadata |
| `keyboard-modal-focus-trap` | 60L (real) | 53L (stub-ish) | 58L (stub) | Enrich metadata + rubric |
| `keyboard-roving-tabindex` | 42L (stub) | 53L (stub-ish) | 58L (stub) | Full rewrite |

**Effort**: ~10 min each for enrichment, ~20 min for roving-tabindex full rewrite. ~1 hour total.

---

## Phase 3: Critic FLAWED + ADVERSARIAL Tiers

Per `domain-sampling-strategy.md`, the target is 27-30 total fixtures. Current: 25 (5 CLEAN + 20 HAS-BUGS). Need: 5-8 more.

### FLAWED fixtures (3-5 to create)

Subtle bugs, incomplete patterns. Baseline finder rate 15-35%. The domain-sampling-strategy already specifies examples:

| Fixture ID (proposed) | Domain | What's wrong |
|-----------------------|--------|-------------|
| `tabs-incomplete-aria-selected` | Interactive Widgets | aria-selected + arrow keys present, but active tab not focused after selection; panel not referenced by aria-controls |
| `multistep-form-error-clearing` | Form & Validation | Error messages specific but no announcement when errors clear; disabled Next button confusing |
| `dashboard-heading-inconsistency` | Content & Semantic | Heading hierarchy inconsistent; list items in divs; table missing scope; regions not marked |
| `app-focus-order-illogical` | Focus Management | Tab order illogical, skip link targets wrong element, focus indicator low contrast, roving tabindex not implemented |
| `async-form-vague-success` | Dynamic Content | Success message announced but doesn't specify what succeeded; aria-busy removed too early |

**Files per fixture**: `.md` (component code, 80-150 lines), `.metadata.yaml` (must/should/nice findings), `.rubric.yaml`

**Effort**: ~30-40 min per fixture (code + metadata + rubric). ~2.5-3 hours for 5.

### ADVERSARIAL fixtures (2-3 to create)

Ambiguous implementations. Baseline finder rate 5-20%.

| Fixture ID (proposed) | Domain | What's ambiguous |
|-----------------------|--------|-----------------|
| `modal-div-trigger-correct-aria` | Interactive Widgets | Div + ARIA instead of button for trigger; role="dialog" correct but trigger semantics wrong. Defensible if you squint. |
| `dynamic-form-duplicate-announcements` | Form & Validation | Multiple validation sources, aria-live regions conflict, user hears duplicate announcements. Not clearly "wrong." |
| `search-focus-stays-in-input` | Focus Management | Results update dynamically; where should focus go? Designer chose to leave focus in search box. Defensible. |

**Effort**: ~40 min per fixture (more thought needed). ~2 hours for 3.

---

## Phase 4: Ollama Benchmark Completion

### 4A. Critic benchmarks (remaining 18/25 fixtures)

After Phase 1 adds rubrics, all 25 fixtures are scorable. Run:

```bash
# Add new fixtures to run_benchmark.py's fixture lists, then:
python3 ollama/run_benchmark.py ollama-bugs    # expanded HAS-BUGS list
python3 ollama/run_benchmark.py ollama-clean   # already done (4/5)
python3 ollama/run_benchmark.py score-all
```

**Models**: qwen3:32b (primary), llama3.3:70b (secondary). Skip incomplete models until critic suite is stable.

**Memory constraint**: Run one model at a time. BENCHMARK.md documents that loading two 70B+ models simultaneously on 128 GB causes 2-3x slowdowns from swap pressure. Run all qwen3:32b fixtures first, unload, then run llama3.3:70b.

**Effort**: ~6-8 hours of Ollama runtime (18 fixtures × 2 models × ~5-8 min each, sequential). Unattended.

### 4B. Complete in-progress models

| Model | Remaining | Priority |
|-------|-----------|----------|
| qwen3.5:27b | 5 critic fixtures | LOW (no accuracy advantage over qwen3.5:latest) |
| deepseek-r1:70b | 6 critic fixtures | LOW (slow, no advantage yet) |

**Recommendation**: Defer these. They're not blocking anything and qwen3:32b + qwen3.5:latest cover the value range.

### 4C. Perspective benchmarks (remaining 23/30 fixtures)

```bash
python3 ollama/run_benchmark.py perspective-pilot qwen3:32b  # already done (7/7)
# Need: run remaining 23 fixtures individually
for fixture in data-viz-color-encoding podcast-audio-only product-carousel-autoplay ...; do
  python3 ollama/run_benchmark.py perspective qwen3:32b "$fixture"
done
python3 ollama/run_benchmark.py score-perspective
```

**Effort**: ~3-4 hours Ollama runtime (23 × ~8-10 min). Unattended.

### 4D. qwen3.5:latest on perspective-audit

Test whether the lightweight model handles perspective-audit as well as it handles critic:

```bash
for fixture in animated-onboarding-flow checkout-form-broken-errors color-only-status-indicators ...; do
  python3 ollama/run_benchmark.py perspective qwen3.5:latest "$fixture"
done
```

**Effort**: ~2 hours (7 pilot fixtures × ~3-5 min).

---

## Phase 5: Claude Baseline (optional, lower priority)

Establish how Claude performs on the same fixtures to calibrate the eval suite's expected performance ranges.

Run the 7 benchmarked fixtures through Claude Opus via the actual a11y-critic and a11y-planner skills (not Ollama). Compare scores.

**Effort**: ~1 hour of API cost. Can be done via the run_benchmark.py with a Claude adapter.

---

## Execution Order

```
Phase 1A: Write 8 missing critic rubrics ............... ✅ DONE (2026-05-15)
Phase 1B: Reconcile planner eval.yaml vs files ......... ✅ DONE (2026-05-15, Option 1: replaced stubs)
Phase 2:  Generate 15 planner fixture triplets .......... ✅ DONE (2026-05-15)
Phase 2b: Enrich 5 keyboard fixtures ................... ✅ DONE (2026-05-15)
Phase 3:  Create 5 FLAWED + 3 ADVERSARIAL critic fixtures ~5 hours
Phase 4A: Run critic benchmarks (18 fixtures) ........... ~8 hours (unattended)
Phase 4C: Run perspective benchmarks (23 fixtures) ...... ~4 hours (unattended)
Phase 4D: Test qwen3.5:latest on perspective-audit ...... ~2 hours (unattended)
Phase 5:  Claude baseline (optional) .................... ~1 hour
                                                  Total: ~29 hours
                                              Remaining: ~16 hours (5h human + 14h machine)
```

**Session strategy**: Phases 1-3 are generation work that benefits from one session per phase. Phase 4 is unattended Ollama runs that can be kicked off at the end of any session.

### Recommended session breakdown

1. ~~**Session A** — Phase 1A + 1B (fix structural issues). ~3 hours.~~ ✅ Complete
2. ~~**Session B** — Phase 2 first half (SR + Visual domains, 10 fixtures). ~3 hours.~~ ✅ Complete
3. ~~**Session C** — Phase 2 second half (Testing domain, 5 fixtures) + Phase 2b (keyboard enrichment).~~ ✅ Complete
4. **Session D** — Phase 3 (FLAWED + ADVERSARIAL). ~5 hours. Kick off Phase 4A overnight.
5. **Session E** — Phase 4C + Phase 4D + Phase 5 + update BENCHMARK.md with full results. ~3 hours.

---

## Validation Checklist (run after each phase)

- [x] Every `.md` fixture has a matching `.metadata.yaml` (verified 2026-05-15)
- [x] Every `.metadata.yaml` has a matching `.rubric.yaml` (verified 2026-05-15)
- [x] eval.yaml fixture IDs match actual filenames (25/25 match, verified 2026-05-15)
- [x] `python3 ollama/run_benchmark.py score-all` runs without errors (verified 2026-05-15)
- [ ] `python3 ollama/run_benchmark.py score-perspective` runs without errors
- [x] No fixture has "Feature overview for" as its description (verified 2026-05-15)
- [ ] BENCHMARK.md updated with latest results
