# Wave-1 build handoff — PT-01, PT-03, PT-02

**Date:** 2026-09-02 · **For:** a fresh session picking up the approved wave-1 builds of the promotion program.
**Authority:** the user approved all three work packages at the 2026-09-02 checkpoint and delegated the order; each still needs its own critic pass before merge (bar clause 6). Dispositions and receipts: `docs/plans/2026-09-02-promotion-candidate-dispositions.md`, `evals/results/promotion-eval-2026-09/`.

## State to verify first (do not trust this file over `git`)

- PR #41 `redaction/product-names-gate` — the extended client-reference gate + receipt scrub. **Must merge first**; every branch below assumes the four-group gate with `--self-test` and path scanning.
- PR for `promotion/phase1-dispositions` — dispositions doc, receipts, `docs/alfa-scan-adoption-assessment.md`, this file. Stacked on #41; retarget to `main` once #41 merges.
- PR #39 — the catalogue, amended (bar text, PT-01/06/19 status, order pointer). Merge, do not close.
- Private ledger (`zivtech/a11y-audits`, PR #6 branch): one row state per disposition, on a branch off its `origin/main` after #6 merges. Not done yet.
- Untracked files in this working tree named after engagement products are **never** committed as-is.

## Order

WP-B and WP-D in parallel (disjoint files) → WP-C after its verify pair. Each on its own branch off `main`; only `a11y-test/SKILL.md` + its `.agents` mirror serialize (WP-B, WP-C). A work package that fails its gate stops on its branch and blocks nothing.

## WP-B · PT-01 operation-evidence scorer (effort M) — spec: `evals/results/promotion-eval-2026-09/memos/1.2-scorer-spike.md`

1. Skill text first, critic first: insert the 15-line "Structured disposition block" (spike § a) after the fifth admissibility bullet in `.claude/skills/a11y-test/SKILL.md` (and the `.agents` mirror byte-identically). Spawn `a11y-critic` (opus) on that text **before** writing any scorer. Negative space is in the block's last line.
2. `ollama/score_operation_evidence.py` on `score_common` (spike § d): admissibility, per-op dispositions, `rules_violated` ⊆ the five ids (any other id = fabrication FAIL), `expected_verdict_must_not` after negation strip, `nice_to_have` → WARN. Promote `strip_negation_lines` + `NEGATION_RE` from `score_evalreport.py` into `score_common.py`; update the caller; re-run all smoke cases.
3. Fixture metadata: `expected_coverage_must_stay` → `expected_dispositions` on `op-empty-state-coverage-shortcuts`; `hook_absent_in_evidence` stays unwired; the three rubrics' `scorer:` comment dropped; `RUBRIC_TEMPLATE.md` + suite README status updated.
4. Smoke: 3 gold + 15 single-dimension mutations (spike § c) under `evals/suites/smoke/`, asserted in `scripts/smoke_scorers.sh` — gold PASS, every mutation FAIL with its named must-miss line.
5. Runner: `opevidence` / `opevidence-baseline` in `run_benchmark.py` with a **section-slice** system prompt (not the 1,016-line file); `OPEVIDENCE_FIXTURES`; a registry-sync block in `scripts/validate_fixtures.py`. Skip `run_cloud_benchmark.py` (acr precedent).
6. Calibration before any model row: opus subagent 2 draws × 3 fixtures must-clean; then one qwen3.6:35b row via `bench-runner`; `bench-reporter` appends to BENCHMARK.md.
7. Critics: `test-critic` (opus) on scorer + canaries; the a11y-critic verdict from step 1 quoted in the PR with the user's option-A approval.

## WP-D · PT-03 folded into `baseline-url-scan.mjs` (effort M) — spec: `memos/1.3-memo-pt03.md`

`--resume` (skip a URL only when its per-URL JSON exists, parses, has `status: measured`, the same viewport set, the same recorded `axe_core_version`, and the same `--census`/`--alt-snapshot` keys — otherwise rescan) + a `coverage` block in `summary.json` (`measured`, `aborted` by reason class, `skipped_resumed`; aborts never enter a denominator); `schema_version` 1.2 → 1.3; the five canaries in memo § 5 as a scratch-run receipt appended to `docs/baseline-url-scan-adoption-assessment.md` § Validation Performed. Mirror the `references/` file byte-identically. Critic: `a11y-critic` at sonnet (reference-script change, no skill text).

## WP-C · PT-02 evidence checksums (effort S) — after its verify pair

`references/hash-evidence.mjs`: `--root`, `--out checksums.json`, `--verify` (recompute, list drift, exit non-zero), refuse to overwrite an existing manifest without `--append`. **Second reproduction first:** the `--verify` positive/negative pair (unchanged tree passes; one deliberately edited file fails) as a scratch receipt. Then extend `a11y-test/SKILL.md` § "Evidence retention (append-only)" **by one reference sentence only** — the retention rule already lives there (lines 65–69); do not restate it. Mirror. Critic: `a11y-critic` at sonnet.

## Gates for every PR

`python3 scripts/check_client_refs.py --self-test && python3 scripts/check_client_refs.py`; `py_compile`; `validate_fixtures.py`; `lint_skills.py`; `smoke_scorers.sh`; `test_blind_prompts.py`; `check_mirrors.py --strict`. PR body carries the six-clause table with receipts, the critic verdict quoted, the user approval quoted. Model routing: haiku for mirror copies/greps/gates, sonnet for builds and doc-level critics, opus for every verdict that gates a skill-text change.

## Not in wave 1

PT-06 (declined as a mode; recorded), PT-07 (scope call after the maker/community skill survey), PT-09 (needs the report-contract appendix first), PT-19, Tier 3 (GT-05/GT-07 are wave 2, fixture-first), PT-18, the redaction history rewrite (user-called).
