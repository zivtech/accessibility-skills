# Calibration results — opevidence lane (2026-09-02)

Scorer: `ollama/score_operation_evidence.py` at the commit this file lands in.
Draws: Claude subagents (opus), blind (see README.md for the exact spawn prompt).
Prompts: `prompts/` — the skill-slice condition is byte-for-byte what
`run_benchmark.py opevidence` sends (4,028-char slice of `a11y-test/SKILL.md`
from "### Operation-evidence admissibility" to the end of the Structured
disposition block, plus the task prefix and the fixture).

| Fixture | Condition | Draw | Status | Must misses | Fabrications | Should misses |
|---|---|---|---|---|---|---|
| op-dialog-escape-overreach | skill slice | d1 | PASS | 0 | 0 | 0 |
| op-dialog-escape-overreach | skill slice | d2 | PASS | 0 | 0 | 0 |
| op-dialog-escape-overreach | baseline | d1 | FAIL | 8 (structural: no block, keys, must_catch) | 0 | — |
| op-empty-state-coverage-shortcuts | skill slice | d1 | PASS | 0 | 0 | 0 |
| op-empty-state-coverage-shortcuts | skill slice | d2 | PASS | 0 | 0 | 0 |
| op-empty-state-coverage-shortcuts | baseline | d1 | FAIL | structural | 0 | — |
| op-mixed-package-partial | skill slice | d1 | PASS | 0 | 0 | 0 |
| op-mixed-package-partial | skill slice | d2 | PASS | 0 | 0 | 0 |
| op-mixed-package-partial | baseline | d1 | FAIL | structural | 0 | — |
| op-retest-clean | skill slice | d1 | PASS | 0 | 0 | 0 |
| op-retest-clean | skill slice | d2 | PASS | 0 | 0 | 0 |
| op-retest-clean | baseline | d1 | FAIL | 6 (structural) | 0 | — |

**Gate: 8/8 skill-slice draws must-clean across two draws on all four fixtures**
(no WARN either — every should-tier hook and every `claim_boundary` operation
mention hit). Every skill-slice draw wrote exactly the block the critic's
round-3 adjudication predicted, including `OP-CLOSE: UNTESTED` on op-dialog
(not `BLOCKED`) and `{OP-CLOSE: PASS, OP-OPTION: UNTESTED}` with
`rules_violated: {OP-OPTION: [passive_observation_binding]}` on op-mixed.

**A/B direction is draw-stable and structural.** All four baselines FAIL only
because no block exists without the contract (no forbidden verdict phrase
fired; prose judgments use the right vocabulary — "inadmissible", "UNTESTED").
Same reading as the acr-reporting Phase 2 lane: bare opus judges correctly;
what the slice carries is the machine contract (stable rule ids, the four-value
closed set, per-operation attribution), not the judgment.

**Re-scored after the test-critic round** (exhaustive attribution check added —
any rule fired outside a fixture's `must_catch` is a must-miss): every status
unchanged, zero `unexpected rule fired` lines across all twelve draws. No opus
draw over-attributed; the gate result stands under the stricter instrument.

**Not measured here:** any local model (see `../local-qwen36-35b/` when it
lands — that row is detector output, not a verdict authority); hosted rows
other than Claude; draw variance beyond n=2 per fixture. The scorer's own
correctness is gated by the 30 smoke canaries in `evals/suites/smoke/`
(`scripts/smoke_scorers.sh` cases 20–49), not by these draws.
