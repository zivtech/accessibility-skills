# Plan 006: Complete the a11y-planner benchmark (2/25 → 25/25), scoring instrument first

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat de0031f..HEAD -- ollama/score_planner.py ollama/run_benchmark.py evals/suites/a11y-planner/ ollama/BENCHMARK.md`
> Changes from plans 001–003 in `ollama/` are EXPECTED (named constants,
> truncation guard, results dir). If `evals/suites/a11y-planner/` fixture
> files changed, or `score_planner.py` changed beyond what plans 001/002
> describe, compare against "Current state" before proceeding; on a mismatch,
> STOP.

## Status

- **Priority**: P2
- **Effort**: L (Phase A is ~25 small file edits + scorer change; Phase C is mostly unattended runtime)
- **Risk**: MED (defines the scoring basis for a new published table)
- **Depends on**: plans/001 (smoke tests), plans/002 (scorer fixes — run on the corrected basis, not the buggy one), plans/003 recommended (persistent results dir)
- **Category**: direction (tests)
- **Planned at**: commit `de0031f`, 2026-06-11

## Why this matters

The planner is the first stage of the lifecycle — quality failures there propagate through every downstream stage — yet it has benchmark coverage on only 2 of its 25 fixtures (`EVAL-GAPS-PLAN.md:14`, `ollama/run_benchmark.py:39-42`). The suite, rubrics, runner, and scorer all exist; only the measurement is missing. But there is a trap: `score_planner.py`'s keyword table (`SECTION_KEYWORDS`, lines 32–81) covers only the 2 already-benchmarked fixtures' criteria. For the other 23, scoring falls through to a first-4-words fallback (`score_planner.py:114-115`) where generic tokens like "Semantic" match almost any plan — the resulting numbers would look complete and mean nothing. So this plan fixes the instrument first (Phase A), validates it on a pilot (Phase B), and only then runs the suite (Phase C). Do not write any BENCHMARK.md numbers before the measurements exist and have been spot-checked.

## Current state

Verified at commit `de0031f`:

- `ollama/run_benchmark.py:39-42`:
```python
PLANNER_FIXTURES = [
    "aria-modal-form-validation",
    "keyboard-roving-tabindex",
]
```
  `run_planner()` (`:257-300`) loads from `PLANNER_FIXTURES_DIR = evals/suites/a11y-planner/fixtures`, sends `PLANNER_PROMPT_PREFIX` + fixture content with the planner SKILL.md as system prompt, `num_ctx=32768`, `stream=False`, timeout 1200s, writes `ollama-planner-<fixture>-<tag>-response.json`.
- `ollama/score_planner.py:84-132` (`score_planner`): reads `expected_findings.must_have` (list of plain strings in the planner metadata — verified in `keyboard-breadcrumb.metadata.yaml:44-50`) or falls back to `key_evaluation_criteria`; looks up each criterion string in `SECTION_KEYWORDS` by EXACT match; otherwise takes the first 4 words >3 chars. Gate: `found/total >= 0.7` → `Status: PASS`, else `Status: NEEDS REVIEW`.
- Planner metadata files are rich and consistent: `scenario`, `expected_plan_sections`, `key_evaluation_criteria`, `expected_findings.{must_have,should_have,nice_to_have}` (strings), `false_positive_traps`, `multi_perspective_coverage`, `notes` (see `evals/suites/a11y-planner/fixtures/keyboard-breadcrumb.metadata.yaml` as the exemplar).
- Existing planner results in BENCHMARK.md: 2 fixtures, local models (qwen3:32b "perfect planner"). Hosted planner lanes have never run.
- Operator's standing benchmarking rule: Claude-family runs for Claude Code skills go through **Claude Code subagents** (the production mechanism — see BENCHMARK.md Phase 7 for the precedent and method), not direct API calls; local models run through the Ollama runner; cloud spend requires explicit approval.

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Compile | `python3 -m py_compile ollama/score_planner.py ollama/run_benchmark.py` | exit 0 |
| Smoke | `bash scripts/smoke_scorers.sh` | exit 0 |
| Fixture validation | `python3 scripts/validate_fixtures.py` | exit 0 |
| Single planner run (local) | `BENCHMARK_RESULTS_DIR=$HOME/a11y-bench-results python3 ollama/run_benchmark.py planner qwen3:32b <fixture-id>` | result JSON written (requires Ollama serving qwen3:32b — Phase B/C only) |
| Score one | `python3 ollama/score_planner.py <response.json> evals/suites/a11y-planner/fixtures/<id>.metadata.yaml` | `Score: N/M` + `Status:` line |

(If plan 003 is not yet applied, drop the `BENCHMARK_RESULTS_DIR` prefix — results then land in `/tmp`; copy them out before reboot.)

## Scope

**In scope**:
- `evals/suites/a11y-planner/fixtures/*.metadata.yaml` (all 25 — additive `scoring_keywords` block only)
- `ollama/score_planner.py` (keyword lookup change)
- `ollama/run_benchmark.py` (extend `PLANNER_FIXTURES` to all 25; or replace with a directory-derived list)
- `evals/suites/smoke/planner.metadata.yaml` + `scripts/smoke_scorers.sh` (one added smoke case for the new lookup path)
- `ollama/BENCHMARK.md` (append-only: new "Planner benchmark (post-002 scoring)" section — ONLY in Phase E, only with real data)

**Out of scope** (do NOT touch):
- Fixture `.md` content, `rubrics/*.rubric.yaml`, and every existing `must_have` string — `scoring_keywords` is a NEW additive key; never reword existing criteria to make scoring easier.
- `score_output.py` / `score_perspective.py` / `run_cloud_benchmark.py`.
- Historical BENCHMARK.md tables.

## Git workflow

- Branch: `advisor/006-planner-benchmark`
- Conventional commits per phase, e.g. `test: add scoring_keywords to planner fixture metadata`.
- Do NOT push or open a PR unless the operator instructed it.

## Steps

### Phase A — Step 1: Teach `score_planner.py` to read rubric-supplied keywords

In `score_planner.py`, inside the criterion loop (currently `keywords = SECTION_KEYWORDS.get(desc, [])` at line 112), change the lookup order to:

```python
        rubric_keywords = rubric.get("scoring_keywords", {})
        keywords = rubric_keywords.get(desc) or SECTION_KEYWORDS.get(desc, [])
        if not keywords:
            keywords = fallback_keywords(desc)   # from score_common (plan 002)
            print(f"  WARN: fallback keywords for criterion: {desc[:60]}")
```

(If plan 002's `score_common.py` is absent, STOP — dependency not met.) Also print a per-criterion keyword list on misses, same convention plan 002 added to the other scorers.

**Verify**: `python3 -m py_compile ollama/score_planner.py` → exit 0; `bash scripts/smoke_scorers.sh` → still passes (smoke planner case uses `SECTION_KEYWORDS` keys, unaffected).

### Phase A — Step 2: Author `scoring_keywords` for all 25 planner metadata files

For each `evals/suites/a11y-planner/fixtures/*.metadata.yaml`, append a top-level block mapping EVERY `must_have` string (verbatim, as a quoted YAML key) to 3–6 detection keywords. Authoring rules — these decide whether the benchmark means anything:

- Keywords must be **specific tokens a correct plan would necessarily contain** (attribute names, element names, ARIA tokens, WCAG numbers): `aria-current="page"`, `<ol`, `aria-label`, `1.3.1`. Include syntax variants where quoting differs (`aria-current='page'`).
- NEVER use generic words that any plan contains (`semantic`, `element`, `structure`, `accessible`, `plan`, `keyboard` alone).
- Mine each criterion string itself plus the fixture's `notes` ("discriminating items") for the load-bearing token. Worked example for `keyboard-breadcrumb.metadata.yaml`:

```yaml
scoring_keywords:
  "Semantic `<nav>` element with aria-label='Breadcrumb' (disambiguates from site nav)":
    - "aria-label=\"Breadcrumb\""
    - "aria-label='Breadcrumb'"
    - "<nav"
  "Ordered list `<ol>` with `<li>` items — ol communicates sequential/hierarchical relationship":
    - "<ol"
    - "ordered list"
  "aria-current='page' on the current page item (last breadcrumb item)":
    - "aria-current=\"page\""
    - "aria-current='page'"
  "Current page item is not wrapped in `<a>` — static text or `<span>` only":
    - "not a link"
    - "<span"
    - "static text"
  "WCAG 1.3.1 (Info and Relationships) citation":
    - "1.3.1"
```

- A criterion that is a *negative* requirement ("X is not applicable", "do not do Y") gets keywords for the phrase a plan uses when honoring it (as in "not a link" above) — accept that these are weaker and flag them with a YAML comment `# weak-match criterion` for the pilot review.
- Work in batches of 5 files; after each batch run the YAML validation.

**Verify** (after each batch and at the end): `python3 scripts/validate_fixtures.py` → exit 0. Then completeness:
```bash
python3 - <<'EOF'
import glob, yaml, sys
bad = []
for p in sorted(glob.glob("evals/suites/a11y-planner/fixtures/*.metadata.yaml")):
    m = yaml.safe_load(open(p))
    must = (m.get("expected_findings") or {}).get("must_have", [])
    sk = m.get("scoring_keywords", {})
    missing = [c for c in must if c not in sk or not sk[c]]
    if missing: bad.append((p, missing))
for p, m in bad: print(p, "→ missing keywords for", len(m), "criteria")
sys.exit(1 if bad else 0)
EOF
```
→ exit 0, no output. (25 files, zero criteria without keywords.)

### Phase A — Step 3: Extend the runner's fixture list and add a smoke case

1. In `run_benchmark.py`, replace the 2-item `PLANNER_FIXTURES` literal with the full 25 ids (basenames of `evals/suites/a11y-planner/fixtures/*.md`), keeping the constant name. (`scripts/validate_fixtures.py` from plan 001 checks critic/perspective registries; ALSO add the planner comparison to it now — same pattern, `run_benchmark.PLANNER_FIXTURES` vs the fixtures dir.)
2. Add to `evals/suites/smoke/planner.metadata.yaml` a `scoring_keywords` entry exercising the new lookup path, and a corresponding assertion in `scripts/smoke_scorers.sh` (e.g. add a third criterion whose keywords only resolve via `scoring_keywords`).

**Verify**: `python3 scripts/validate_fixtures.py` → exit 0 (now 5 registry checks); `bash scripts/smoke_scorers.sh` → all pass.

### Phase B — Step 4: Pilot — 3 fixtures, instrument audit (operator gate)

Requires local Ollama with `qwen3:32b` pulled. Run 3 fixtures spanning difficulty (suggest: `keyboard-breadcrumb` (TRIVIAL), `aria-combobox-autocomplete`, `visual-dark-mode`):

```bash
export BENCHMARK_RESULTS_DIR=$HOME/a11y-bench-results && mkdir -p "$BENCHMARK_RESULTS_DIR"
python3 ollama/run_benchmark.py planner qwen3:32b keyboard-breadcrumb   # repeat per fixture
python3 ollama/score_planner.py "$BENCHMARK_RESULTS_DIR/ollama-planner-keyboard-breadcrumb-qwen3-32b-response.json" evals/suites/a11y-planner/fixtures/keyboard-breadcrumb.metadata.yaml
```

Then produce a pilot audit table the OPERATOR reviews (this gate is human, not automated): for each scored criterion, columns = criterion / keyword that hit (or miss) / does the response actually satisfy the criterion (executor judgment by reading the response) / agree? Save as `evals/suites/a11y-planner/PILOT-SCORING-AUDIT.md`. Count agreement.

**Verify**: agreement ≥ 90% across the 3 pilots' criteria. If below, revise the offending `scoring_keywords` (Phase A rules), re-score the SAME stored responses (no re-runs needed), and re-audit. Two revision rounds maximum — then STOP and report.

### Phase C — Step 5: Full local run (25 fixtures, qwen3:32b)

After the operator approves the pilot audit: run the remaining 22 fixtures the same way (a simple shell loop over the fixture ids is fine). Expect ~5–20 min/fixture; run unattended, resumable (re-running skips nothing today for planner — check file existence before each run with a loop guard, or just re-run misses). Score all 25; collect `Score: N/M` + `Status:` per fixture into `evals/suites/a11y-planner/RESULTS-qwen3-32b.md` (raw table, no narrative).

**Verify**: 25 result JSONs exist under `$BENCHMARK_RESULTS_DIR`; 25 rows in the results file; zero `WARN: fallback keywords` lines in any scoring output (if any appear, a criterion lost its mapping — fix before reporting).

### Phase D — Step 6 (OPTIONAL, operator-gated): hosted lanes

STOP and ask the operator before any of this — it costs money:
- **Claude lane**: per the standing rule, run via Claude Code subagents (the production mechanism), following the documented method in `ollama/BENCHMARK.md` Phase 7 (operator drives sessions; one subagent per fixture with the planner agent; save outputs as response JSONs in the same shape so `score_planner.py` can score them).
- **Codex lane** (optional): `run_cloud_benchmark.py` has no planner path for codex/claude today — adding one is NOT in this plan's scope; if the operator wants it, that is a follow-up plan.

### Phase E — Step 7: Publish — append-only BENCHMARK.md section

Only after Phases B–C are done and verified. Append a `## Planner benchmark (post-002 scoring, 25 fixtures)` section: scoring method (scoring_keywords + score_common, link the pilot audit file), per-fixture table, aggregate section-hit rate, explicit caveats (single local model unless Phase D ran; section-presence is a structural proxy, not a quality judgment). Every number must come from the Phase C results file.

**Verify**: `git diff ollama/BENCHMARK.md` is append-only; every number in the new section greps back to `RESULTS-qwen3-32b.md`.

## Test plan

- The smoke case from Step 3 covers the new `scoring_keywords` lookup path permanently.
- The pilot audit (Phase B) is the validity test for the instrument — it is deliberately human-reviewed; keep the artifact in the repo.
- `validate_fixtures.py` gains the planner-registry check and the Step 2 completeness probe can be folded into it (optional, recommended).

## Done criteria

ALL must hold (through Phase C; D optional, E conditional on C):

- [ ] All 25 planner metadata files have complete `scoring_keywords` (Step 2 probe exits 0)
- [ ] `score_planner.py` prefers rubric keywords; fallback prints a WARN
- [ ] `PLANNER_FIXTURES` lists 25 ids and `validate_fixtures.py` checks it
- [ ] Smoke suite passes with the added scoring_keywords case
- [ ] Pilot audit file exists with ≥90% agreement, operator-reviewed
- [ ] 25/25 fixtures run and scored on the post-002 scorer; results file committed
- [ ] BENCHMARK.md untouched until Phase E, then append-only
- [ ] `plans/README.md` status row updated

## STOP conditions

Stop and report back (do not improvise) if:

- Plans 001/002 are not landed (no smoke suite, no `score_common.py`).
- Pilot agreement stays <90% after two keyword-revision rounds — the instrument design needs a human decision (possibly LLM-judge scoring instead of keywords; that is a different plan).
- Any planner metadata file deviates from the documented schema (e.g. `must_have` items that are dicts, not strings) — report which files; do not improvise a second schema.
- Ollama is unavailable or qwen3:32b is not pulled and cannot be (disk).
- Anything in Phase D before explicit operator cost approval.

## Maintenance notes

- New planner fixtures now require: triplet + `scoring_keywords` + `PLANNER_FIXTURES` entry — `validate_fixtures.py` enforces the registry, the Step 2 probe (if folded in) enforces keywords.
- The section-presence metric is a floor, not a ceiling: it cannot distinguish a brilliant plan from a checklist-shaped one. If planner quality becomes contested, the next instrument is an LLM-judge rubric pass — design that separately; do not stretch keywords past what they can measure.
- Reviewer should scrutinize: Step 2 keyword choices for generic tokens (the #1 way this benchmark goes dead).
