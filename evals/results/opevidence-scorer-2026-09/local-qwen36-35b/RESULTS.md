# qwen3.6:35b — a11y-test-operation-evidence, first local rows (2026-09-02)

Runner: `python3 ollama/run_benchmark.py opevidence|opevidence-baseline qwen3.6:35b <fixture>`
(num_ctx 16384, temperature 0.3; skill slice = the "### Operation-evidence
admissibility" section through the Structured disposition block). Scorer:
`ollama/score_operation_evidence.py` at the merged #44 state. One draw per cell.
Raw responses + scorer output beside this file. Ollama was shared with six
claude-smart learning workers for the whole run: the first request timed out
at 1800 s and was redrawn once (the redraw is the row below; the timed-out
attempt produced no artifact), the baseline op-dialog request took 1180 s,
later requests 29–241 s. Timing here is contention, not model speed.

| Fixture | Skill slice | Baseline | What the scorer saw (skill slice) |
|---|---|---|---|
| op-dialog-escape-overreach | **FAIL** | FAIL (structural) | admissibility REJECT ✓, both must-catch rules ✓, 0 fabrications; `OP-CLOSE: BLOCKED` where the contract's admitted-observation clause yields `UNTESTED`; one over-fire (`passive_observation_binding` on OP-CLOSE — the stagnation note treated as a passive snapshot) |
| op-empty-state-coverage-shortcuts | **FAIL** | FAIL (structural) | admissibility REJECT ✓, all three rules chosen correctly and attached to the semantically right sub-claims, 0 fabrications; but OP-OPTION was split into two **invented operation ids** (`OP-OPTION_reachability`, `OP-OPTION_focus`) copied from the fixture's prose sub-headings, so `OP-OPTION` is missing from `dispositions` and its rules land under ids the package never declared |
| op-mixed-package-partial | PASS | FAIL (structural) | exactly the adjudicated block: REJECT, `{OP-CLOSE: PASS, OP-OPTION: UNTESTED}`, `{OP-OPTION: [passive_observation_binding]}` |
| op-retest-clean | PASS | FAIL (structural) | ACCEPT, all three dispositions correct, `rules_violated: {}` — the false-alarm control left alone |

**Reading.** 2/4 skill-slice PASS, 0/4 baseline (no block without the
contract — same A/B direction as the opus calibration). Both FAILs are
detector-class, not instrument-class: (1) an **exact-id fidelity** fault —
inventing operation ids by splitting one declared operation along the input's
prose structure — which is the same class as this model's documented
selector/ID fabrication in the bug-reporting lane and which the scorer refuses
mechanically; (2) the **BLOCKED/UNTESTED** distinction on rejected evidence,
which the skill text had to be revised to decide at all (critic rounds 1–3)
and which opus resolved 2/2 — plus an over-fire the test-critic's
exhaustive-attribution check exists to catch. Rule *selection* was right on
all four fixtures; the misses are in reporting fidelity and one boundary case.

**Routing consequence:** unchanged — qwen3.6:35b is a detector, not a verdict
authority, for this lane as for every other. A local disposition block is a
candidate to be read against the package, never a result.

**Not measured:** draw variance (n=1 per cell); whether the invented-id
fault recurs on a fixture whose prose has no sub-headings; any other local
model; the timed-out first attempt (no artifact).
