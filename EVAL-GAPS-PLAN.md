# Eval Suite Gap-Fill Plan

**Created**: 2026-05-15
**Purpose**: Historical gap-fill plan for the 3 eval suites plus the cross-model benchmark suite. The benchmark scope now includes local Ollama models, Claude API, Codex/OpenAI, and peer hosted families such as Gemini when result artifacts are added.
**Note**: This plan supersedes the dashboard at `~/.agent/diagrams/a11y-testing-architecture.html` — fixture counts there are stale (says 20 critic / 1 real planner; actual is 25 critic / 10 real planner).

> **STATUS: COMPLETE (2026-05-19).** All phases below are done; this document
> is retained as a historical record. Open follow-ons (Gemini baselines,
> planner benchmark expansion) are tracked as direction items in
> `plans/README.md`, not here.

> **FOLLOW-ON (2026-06-19):** Vital-Core reporting discipline has been adopted
> as an optional A11y Evidence Finding Contract. Smoke and focused scorer tests
> now cover required fields, stable finding IDs, trend metadata, and clean
> false-positive resistance. See `docs/a11y-evidence-finding-contract.md` and
> `docs/vital-core-adoption-assessment.md`.

---

## Current State

| Area | Built | Stubs/Missing | Benchmarked | Blocking Issues |
|------|-------|---------------|-------------|-----------------|
| Critic eval | 33 fixtures (4 CLEAN + 21 HAS-BUGS + 5 FLAWED + 3 ADVERSARIAL) | 0 | Ollama, Claude API, Codex/OpenAI, Gemini (flash, 2026-06-12) | Resolved — Gemini artifacts committed (`evals/results/gemini/`) |
| Planner eval | 25 fixtures | 0 | 25/25 Ollama (qwen3:32b) + 25/25 Claude subagents (2026-06-12) | Resolved (plans 006 + Phase D); Codex lane is plan 010 |
| Perspectives eval | 30 fixtures (25 main + 5 calibration) | 0 | qwen3:32b full run + calibration results | Hosted perspective-audit baselines still optional |
| Benchmark runners | Production-ready for Ollama, Claude API, and Codex/OpenAI | Gemini/other provider adapters as needed | Yes | Keep result tables model-family neutral |

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

## Phase 3: Critic FLAWED + ADVERSARIAL Tiers ✅ DONE (2026-05-15)

Per `domain-sampling-strategy.md`, the target is 27-30 total fixtures. Now have 33 (4 CLEAN + 21 HAS-BUGS + 5 FLAWED + 3 ADVERSARIAL).

### FLAWED fixtures (5 created)

Subtle bugs, incomplete patterns. Baseline finder rate 15-35%.

| Fixture ID | Domain | What's wrong |
|------------|--------|-------------|
| `tabs-incomplete-aria-selected` | Interactive Widgets | Focus doesn't follow aria-selected on arrow keys; panels missing aria-labelledby; tabs missing aria-controls |
| `multistep-form-error-clearing` | Form & Validation | Error clearance is silent (no SR announcement); Next button uses disabled instead of aria-disabled; step indicator lacks aria-current |
| `dashboard-heading-inconsistency` | Content & Semantic | Heading hierarchy h1→h3 skip; table th missing scope; metric cards use divs not dl/dt/dd; no landmarks |
| `app-focus-order-illogical` | Focus Management | CSS order creates visual/DOM mismatch; skip link targets non-focusable div; focus indicator 1.55:1 contrast; positive tabindex on FAB |
| `async-form-vague-success` | Dynamic Content | Generic success message; aria-busy clears 200ms before content arrives; form stays editable after submit |

### ADVERSARIAL fixtures (3 created)

Genuinely ambiguous — rubrics use `must_articulate` (tradeoff analysis), not `must_find` (bug detection). LLM judge weight 0.4 (vs 0.3 standard).

| Fixture ID | Domain | What's ambiguous |
|------------|--------|-----------------|
| `tabbed-nav-vs-tab-pattern` | Interactive Widgets | WAI-ARIA Tabs pattern used for page-level route navigation. Tabs interaction model vs nav semantic model — both defensible. |
| `form-field-vs-summary-errors` | Form & Validation | Dual error announcement (role="alert" summary + aria-live inline). Thorough or redundant? GOV.UK recommends both; SR users hear errors twice. |
| `search-focus-stays-in-input` | Focus Management | Focus stays in search box after results update. Google/Algolia do this. Lets user refine, but SR users may miss results. |

**Design decisions during Phase 3:**
- Replaced `modal-div-trigger-correct-aria` — div-instead-of-button is arguably just wrong, not genuinely ambiguous. Replaced with `tabbed-nav-vs-tab-pattern` (tabs-vs-nav is one of the most debated patterns in a11y).
- Reframed `dynamic-form-duplicate-announcements` → `form-field-vs-summary-errors` — "duplicate announcements" framed it as a bug. The real ambiguity is whether field-level + summary errors is thorough or confusing.

---

## Phase 4: Local Model Benchmark Completion

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

## Phase 5: Hosted Baselines (Claude API complete; extend with Gemini/other providers)

Establish how hosted model families perform on the same fixtures to calibrate the eval suite's expected performance ranges.

The historical Phase 5 run sent the 7 benchmarked fixtures through Claude Opus via the actual a11y-critic and a11y-planner skills (not Ollama). Later phases expanded this to a full Claude escalation run and a Codex/OpenAI escalation run. Gemini or other hosted baselines should follow the same fixture/rubric discipline.

**Effort**: ~1 hour of API cost per hosted family. Use `ollama/run_cloud_benchmark.py` or the equivalent provider adapter.

---

## Execution Order

```
Phase 1A: Write 8 missing critic rubrics ............... ✅ DONE (2026-05-15)
Phase 1B: Reconcile planner eval.yaml vs files ......... ✅ DONE (2026-05-15, Option 1: replaced stubs)
Phase 2:  Generate 15 planner fixture triplets .......... ✅ DONE (2026-05-15)
Phase 2b: Enrich 5 keyboard fixtures ................... ✅ DONE (2026-05-15)
Phase 3:  Create 5 FLAWED + 3 ADVERSARIAL critic fixtures ✅ DONE (2026-05-15, 5F+3A=8 new, 33 total)
Phase 4A: Run critic benchmarks (26 fixtures) ........... ✅ DONE (2026-05-15, 26/26 PASS, 97% must-find)
Phase 4C: Run perspective benchmarks (18 fixtures) ...... ✅ DONE (2026-05-16, 20 PASS / 4 WARN / 1 FAIL)
Phase 4D: Test qwen3.5:latest on perspective-audit ...... ✅ DONE (2026-05-17, NOT VIABLE — 50% empty responses)
Phase 5:  Claude API baseline ........................... ✅ DONE (2026-05-18, Haiku 85%, escalation to Sonnet-think 100%)
Phase 6:  Cross-platform (Codex/OpenAI) ................. ✅ DONE (2026-05-19, GPT-5.2 91%, escalation to 5.5-low 100%)
                                                  Total: ~29 hours
                                              Remaining: 0 (all phases complete)
```

**Session strategy**: Phases 1-3 are generation work that benefits from one session per phase. Phase 4 is unattended local-model runtime that can be kicked off at the end of any session. Hosted baselines should be tracked as model-family additions, not as a return to single-provider framing.

### Recommended session breakdown

1. ~~**Session A** — Phase 1A + 1B (fix structural issues). ~3 hours.~~ ✅ Complete
2. ~~**Session B** — Phase 2 first half (SR + Visual domains, 10 fixtures). ~3 hours.~~ ✅ Complete
3. ~~**Session C** — Phase 2 second half (Testing domain, 5 fixtures) + Phase 2b (keyboard enrichment).~~ ✅ Complete
4. ~~**Session D** — Phase 3 (FLAWED + ADVERSARIAL). ~5 hours. Kick off Phase 4A overnight.~~ ✅ Complete
5. ~~**Session E (part 1)** — Phase 4A (full critic benchmark). 8 hours Ollama, 26/26 PASS.~~ ✅ Complete
6. ~~**Session E (part 2)** — Phase 4C complete (20P/4W/1F). BENCHMARK.md updated. Fixture/rubric fixes for CLEAN scope.~~ ✅ Complete
7. ~~**Session F** — Phase 4D + Phase 5 (Claude API baseline).~~ ✅ Complete (2026-05-18)
8. ~~**Session G** — Phase 6 (Codex/OpenAI). `bash ollama/codex-benchmark.sh` from Codex.~~ ✅ Complete (2026-05-19)

---

## Validation Checklist (run after each phase)

- [x] Every `.md` fixture has a matching `.metadata.yaml` (verified 2026-05-15)
- [x] Every `.metadata.yaml` has a matching `.rubric.yaml` (verified 2026-05-15)
- [x] eval.yaml fixture IDs match actual filenames (25/25 match, verified 2026-05-15)
- [x] `python3 ollama/run_benchmark.py score-all` runs without errors (verified 2026-05-15)
- [x] `python3 ollama/run_benchmark.py score-perspective` runs without errors (verified 2026-05-18, 49 scored: 34P/10W/5F)
- [x] No fixture has "Feature overview for" as its description (verified 2026-05-15)
- [x] BENCHMARK.md updated with Phase 4A results (verified 2026-05-15)
