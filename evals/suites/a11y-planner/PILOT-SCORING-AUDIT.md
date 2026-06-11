# Planner Benchmark Pilot — Scoring Instrument Audit (Plan 006, Phase B)

**Date**: 2026-06-11
**Model**: qwen3:32b (local Ollama, Metal GPU, M5 Max 128 GB)
**Scorer**: `ollama/score_planner.py` post-002, with rubric-supplied `scoring_keywords` (commit `7919215` + round-1 revision)
**Fixtures**: keyboard-breadcrumb (TRIVIAL/MODERATE), aria-combobox-autocomplete (MODERATE), visual-dark-mode (MODERATE)
**Runtime note**: Runs targeted a native `ollama serve` on port 11435 (`OLLAMA_URL` override) because port 11434 is held by an Open Notebook Docker container that runs CPU-only inference. Timings: 609s / 459s / 475s — consistent with prior Metal-backed planner runs (500–710s).

## Method

Per plan 006 Step 4: every scored criterion gets three judgments — the keyword
verdict, the executor's judgment from actually reading the response, and
whether they agree. Disagreements drive keyword revision (max 2 rounds),
re-scoring the SAME stored responses. Response JSONs are preserved in
`~/a11y-bench-results/` (and `/tmp/ollama-planner-*-qwen3-response.json`).
None of the three responses contained `<think>` blocks — the scored text is
pure plan text.

## Round 0 — initial scoring (21/23 agreement, 91.3%)

### keyboard-breadcrumb (round 0: 4/5, PASS)

| # | Criterion | Keyword verdict | Response actually satisfies? | Agree |
|---|-----------|-----------------|------------------------------|-------|
| 1 | Semantic `<nav>` with aria-label='Breadcrumb' | HIT `aria-label="Breadcrumb"` | YES — stub line 25 + prose | ✓ |
| 2 | Ordered list `<ol>`/`<li>` | HIT `<ol` | YES — stub + "Ordered list structure" prose | ✓ |
| 3 | aria-current='page' on current item | HIT `aria-current="page"` | YES — stub + state table | ✓ |
| 4 | Current page item not wrapped in `<a>` | **MISS** (`not a link`, `<span`, `static text`) | **YES — satisfied in code**: stub renders `<li aria-current="page">Laptops</li>` with no anchor, twice; state table says "No link styling" | ✗ FALSE MISS |
| 5 | WCAG 1.3.1 citation | HIT `1.3.1` | YES — explicit citation | ✓ |

### aria-combobox-autocomplete (round 0: 11/11, PASS)

| # | Criterion | Keyword verdict | Response actually satisfies? | Agree |
|---|-----------|-----------------|------------------------------|-------|
| 1 | APG Combobox reference with URL | HIT `w3.org/WAI/ARIA/apg/patterns/combobox` | YES — full URL twice | ✓ |
| 2 | aria-expanded | HIT `aria-expanded` | YES — stub + state table | ✓ |
| 3 | aria-owns or aria-controls | HIT `aria-owns` | YES — both present | ✓ |
| 4 | aria-activedescendant | HIT `aria-activedescendant` | YES — stub + keyboard model | ✓ |
| 5 | aria-autocomplete="list" on input | HIT `aria-autocomplete` | YES (with placement caveat — see margin notes) | ✓ |
| 6 | Keyboard model: type/arrows/Enter/Escape/Tab | HIT `arrow up` | YES — complete model documented | ✓ |
| 7 | HTML stub: input, listbox, option | HIT `role="listbox"` | YES — full JSX + HTML stubs | ✓ |
| 8 | Focus remains in input | HIT `focus stays in input` | YES — explicit, with aria-activedescendant rationale | ✓ |
| 9 | aria-busy during async | HIT `aria-busy` | YES — stub + state table | ✓ |
| 10 | WCAG citations per decision | HIT `2.1.1` | YES — citations on every table row and task | ✓ |
| 11 | Test cases keyboard/SR/async | HIT `test case` (weak-match criterion) | YES — all three scenario types have named test cases | ✓ |

### visual-dark-mode (round 0: 7/7, PASS)

| # | Criterion | Keyword verdict | Response actually satisfies? | Agree |
|---|-----------|-----------------|------------------------------|-------|
| 1 | aria-pressed or role="switch" + aria-label, justified | HIT `aria-pressed` | YES — aria-pressed chosen with explicit justification vs role="switch" | ✓ |
| 2 | WCAG 1.4.3, 4.5:1, both modes | HIT `1.4.3` | YES — contrast table covers both modes | ✓ |
| 3 | WCAG 1.4.11, 3:1 | HIT `1.4.11` | YES — cited + applied in Task 2 | ✓ |
| 4 | WCAG 2.4.7 — focus indicator re-eval for dark | **HIT `dark background`** | **NO — 2.4.7 is never cited.** The substance (re-evaluation plan) is present, but the criterion requires the Focus Visible citation; round-0 keywords (`dark background`, `focus indicator`) were generic on a dark-mode fixture | ✗ FALSE HIT |
| 5 | Flag #0066CC for re-test | HIT `#0066CC` | YES — explicit fix plan with computed check and fallbacks | ✓ |
| 6 | Forced-colors distinct from dark mode | HIT `forced-colors` | YES — separate Task 3 + failure mode names the confusion | ✓ |
| 7 | localStorage + aria-pressed sync | HIT `localStorage` | YES — "must reflect current DOM state, not just localStorage value" + stale-state failure mode | ✓ |

## Round 1 — keyword revision (2 criteria), re-scored stored responses

Both disagreements were instrument defects, revised per Phase A authoring rules:

1. **keyboard-breadcrumb #4** (false miss): prose-shaped keywords couldn't see
   code-level satisfaction. Revised to `["not a link", "no link", "static text",
   "plain text", "<span", "aria-current=\"page\">Laptops"]` — adds the state-table
   phrasing and the code-shape token. Re-score: HIT via `no link` ("No link
   styling" state-table row). Criterion remains flagged `# weak-match criterion`.
2. **visual-dark-mode #4** (false hit): generic tokens auto-passed on a dark-mode
   fixture. Revised to `["2.4.7", "Focus Visible"]` — the citation is the
   load-bearing requirement. Re-score: MISS, which is correct — the plan
   genuinely lacks the 2.4.7 citation.

### Post-revision scores (final)

| Fixture | Score | Gate (≥70%) | Status |
|---------|-------|-------------|--------|
| keyboard-breadcrumb | 5/5 | 100% | PASS |
| aria-combobox-autocomplete | 11/11 | 100% | PASS |
| visual-dark-mode | 6/7 | 86% | PASS |

**Post-revision agreement: 23/23 (100%).** Zero `WARN: fallback keywords`
lines in any scoring output — every criterion resolved through
`scoring_keywords`.

## Margin observations (content quality the instrument cannot see)

These do not affect agreement counting but belong in Phase E's caveats:

- **Combobox ARIA 1.0-style placement**: the plan puts `role="combobox"`,
  `aria-expanded`, and `aria-autocomplete` on a wrapper `<div>` rather than on
  the `<input>` (ARIA 1.2 pattern). Section-presence scoring counts the
  attributes as planned; it cannot penalize placement. A content-quality
  instrument (LLM-judge) would.
- **visual-dark-mode misses the 2.4.7 citation** while doing the underlying
  work — the one honest miss in 23 criteria after revision.
- **Instrument is a floor, not a ceiling** (per plan 006 maintenance notes):
  it measures whether load-bearing tokens appear, not whether the plan is
  coherent or correct. The two round-0 disagreements show both failure
  directions: prose-shaped keywords miss code-shaped satisfaction, and
  topic-generic keywords pass topic-matched fixtures.

## Pre-pilot instrument repair (context for reviewer)

Before this pilot, 40 criteria across 18 fixtures carried generic or
substring-hazard keywords (bare `WCAG`/`test`/`keyboard`/`Tab`/`dark`/`list`/
`text`/`none`, code-fence ```` ``` ````, etc.) that auto-pass under the
scorer's any-match substring semantics — the exact "benchmark goes dead" trap
plan 006 §Why warns about. Repaired in commit `7919215` (before any scoring),
with honest-but-weak structural proxies flagged `# weak-match criterion` in
the metadata. The two round-1 revisions above are the residue that only
response-reading could catch.

## Operator review

- Gate: agreement ≥ 90% — **met at round 0 (91.3%) and round 1 (100%)**,
  within the plan's two-revision-round budget (one round used).
- Revision policy honored: re-scored the same stored responses; no re-runs.
- **Awaiting operator approval of this audit before Phase C results are
  treated as final** (per plan 006 Step 5 gate). Phase C response generation
  is scoring-independent; any further keyword revision re-scores stored
  responses at zero model cost.
