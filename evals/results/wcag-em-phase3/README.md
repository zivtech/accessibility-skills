# WCAG-EM Phase 3 — Protocol A/B on `test-multi-page-audit` (2026-07-28)

Phase 3 (step 10) of [docs/wcag-em-2-adoption-assessment.md](../../../docs/wcag-em-2-adoption-assessment.md): does the planner protocol now *teach* the WCAG-EM methodology the multi-page-audit rubric grades, instead of relying on training knowledge? Single-fixture controlled A/B: **old protocol (pre-Phase-2, commit `8c4e2f3`) vs new protocol (with AUDIT-SCOPE MODE, commit `cd7ef66`)**, same fixture input for every run.

**This is a single-fixture methodology probe, not a BENCHMARK.md row.** No full-lane numbers are claimed.

## Method

- **Fixture (constant across all runs):** `evals/suites/a11y-planner/fixtures/test-multi-page-audit.md` at `cd7ef66` (post-Phase-1 identity refresh).
- **Claude subagent lane** (production mechanism, mirroring the 2026-06-12 claude-planner recipe): one Claude Code `general-purpose` subagent per run with model override, instructed to read exactly two files — the protocol file and the fixture — then execute the planning protocol and write the plan. Protocol files: the embedded agent prompt `.claude/agents/a11y-planner.md` as of `cbb04f1` (old, 516 lines) vs `cd7ef66` (new, 527 lines). **Deviation from the committed recipe, disclosed:** `subagent_type="general-purpose"` with the protocol injected by file-read, instead of `subagent_type="a11y-planner"` — required to run both protocol variants in one session; identical mechanism for both conditions preserves the A/B's internal validity.
- **Ollama lane:** `ollama_a11y.py planner` (system prompt = full planner SKILL.md), qwen3:32b, temp 0.3, num_ctx 32768, dedicated Metal server `127.0.0.1:11435`, Ollama.app quit. Old condition ran from a worktree at `8c4e2f3`; new from `cd7ef66`. **Two draws per condition** per the variance discipline.
- **Instruments:** `ollama/score_planner.py` (official rubric gate, post-Phase-1 rubric — accepts either EM version, fair to both conditions) plus `depth_markers.py` (committed here): 12 regex markers for methodology content the protocol teaches **but the fixture text never names**. Marker hits were content-adjudicated the same as misses.

## Result 1 — the rubric gate saturates (instrument finding)

Every run scores **11/11 PASS**, both conditions, all models:

| Run | Rubric score | Elapsed |
|---|---|---|
| old-haiku / new-haiku | 11/11 / 11/11 | 202s / 174s |
| old-sonnet / new-sonnet | 11/11 / 11/11 | 649s / 1243s |
| old-opus / new-opus | 11/11 / 11/11 | 703s / 683s |
| qwen3:32b old d1/d2 | 11/11, 11/11 | 394s / 255s |
| qwen3:32b new d1/d2 | 11/11, 11/11 | 418s / 449s |

The fixture's own text cues the graded keywords (its scope hints name WCAG-EM, the tool matrix, risk-based sampling, third-party handling), so the keyword rubric cannot distinguish a plan that name-drops the methodology from one that operationalizes it. This is why the pre-Phase-2 baselines (Opus subagent 11/11, qwen3:32b 11/11) were already perfect, and it means **the rubric gate is the wrong instrument for the Phase 3 question**. Candidate fixture 11(a)/11(b) in the adoption plan (a de-hinted audit fixture) is the durable fix.

## Result 2 — the depth-marker A/B (the actual measurement)

Markers = EM content absent from the fixture text. Presence count out of 12 (see `depth_markers.py` for patterns; raw counts in the JSON/plan artifacts):

| Model | Old protocol | New protocol | Δ |
|---|---|---|---|
| Haiku | 1 | 5 | **+4** |
| Sonnet | 2 | 5 | **+3** |
| Opus | 4 | 10 | **+6** |
| qwen3:32b (d1, d2) | 1, 1 | 5, 5 | **+4, +4** |

Every model at every tier gains under the new protocol, and the qwen delta is draw-stable.

Key marker splits (old → new):

- **Sampling triad** (random sample / 10% rule / representativeness check): old-haiku 0/0/0 → new-haiku **0/0/0** (still missed); old-sonnet 0/0/0 → new-sonnet **7/6/5** (full uptake, cited "per WCAG-EM Step 3"); old-opus 4/1/0 → new-opus 13/2/5; qwen old 0/0/0 → new: structure present both draws.
- **Accessibility support baseline as a declared artifact:** essentially absent old (0/0/0/0) → new-haiku 1, new-opus 4 (new-sonnet paraphrased — see caveats).
- **Per-SC outcome vocabulary** (cantTell/inapplicable/untested): 0 everywhere old → new-haiku 2, new-opus 9, qwen-new-d1 3.

## Content adjudications

1. **Old-protocol Opus already knew EM sampling from training** — hedged as "commonly around 10% of the structured sample," with seeded draws. New-protocol Opus states the exact rule ("10% of 20 = 2, record the seed and the URL list snapshot"). The adoption plan's thesis — Opus passes on training knowledge, the skill should carry the knowledge — is confirmed verbatim.
2. **Old-protocol Sonnet and Haiku have zero EM sampling content** — the first direct measurement of the sub-Opus gap the fixture's scoring notes predicted.
3. **qwen3:32b parameter fidelity varies by draw:** new-d1 absorbed the structured/random/complete-processes structure but flipped the parameter to "Random Sample (20%)" (its two `10%` regex hits are false credits — they label other items); new-d2 applied the rule correctly ("10% of structured set (1.2 pages) → 2 additional pages"). Cite both draws: structure transfer is stable, parameter fidelity is not.
4. **New-Haiku uptake is partial:** EM 2.0 identity, complete processes, baseline, per-SC vocabulary — but the sampling triad did not transfer in one pass.
5. **Two protocol elements transferred nowhere:** the phrase "product enclosure" (0 mentions in any plan) and the evaluation-report contract by name (0 mentions; new-condition plans build report structure without citing `a11y-evaluation-report-contract.md`). Protocol-wording candidates for a later pass; the substance (scope completeness, report fields) does appear.

## Caveats

- Single fixture, single subagent draw per tier (qwen: two draws). Deltas of this size (+3 to +6 of 12 markers, consistent direction across four models) exceed plausible single-draw noise for presence/absence markers, but no fixture-level generalization is claimed.
- Markers are phrase-proxies and undercount paraphrase: new-sonnet declares an AT matrix without the phrase "accessibility support baseline" and gets no credit. Marker totals are therefore conservative for the new condition (adjudication found no inflation in the old condition beyond old-opus's genuine training knowledge).
- The subagent lane's protocol-injection mechanism deviates from the committed `subagent_type="a11y-planner"` recipe (disclosed above); the qwen lane matches its committed recipe exactly.
- Sonnet elapsed times include one retry each for both conditions (6 tool uses vs 3 for the other tiers); timing is not a measured variable here.

## Verdict for Phase 3, step 10

The protocol now demonstrably teaches audit-scope methodology: sub-Opus tiers stop missing the EM sampling discipline (fully at Sonnet tier, partially at Haiku), Opus upgrades from hedged recall to exact operationalization, and the local detector model absorbs the structure with a disclosed parameter-fidelity hazard. The keyword rubric cannot see any of this because the fixture cues its keywords — recorded as an instrument finding in favor of the adoption plan's step 11 candidate fixtures.
