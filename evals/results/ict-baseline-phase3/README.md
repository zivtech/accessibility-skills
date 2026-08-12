# ICT Testing Baseline Phase 3 — Instrument Calibration (2026-08-12)

Synthetic calibration of the two Phase 3 instruments from
[docs/ict-testing-baseline-adoption-assessment.md](../../../docs/ict-testing-baseline-adoption-assessment.md)
(steps 10–11), run **before any model rows**, per house practice:

- **Step 10** — de-hinted declared-508 planner fixture
  `test-federal-agency-audit` (planner fixture #27; `check_dehinted.py` CLEAN,
  11/11 keyword alignment, 0 collisions) with two runner conditions:
  `planner-federal` (a11y-test crosswalk supplied in-prompt — the
  report-contract-as-system-prompt precedent) and plain `planner`
  (no crosswalk; instruments what the plan does without the reference).
- **Step 11** — ICT baseline test-ID fidelity in the scorers:
  `score_common.check_baseline_ids` (per-baseline manifest validation,
  upstream stale-string ledger hints, case-insensitive membership, narrow
  grammar), wired into `score_bugreport.py` (filed-row required under
  declared scope; 24.A filing rejected; documents IDs rejected; any citation
  outside declared scope rejected) and `score_planner.py` (fabrications and
  out-of-scope citations force NEEDS REVIEW regardless of gate score).
  First declared-508 bug-reporting fixture: `axe-button-name-federal`
  (bug-reporting fixture #7; the valid 62-ID web list is supplied in the
  input, so the task is honest selection, never memory).

## Reproduce

```
python3 evals/results/ict-baseline-phase3/calibrate.py   # exit 0 = CLEAN
python3 -m pytest ollama/test_baseline_id_checks.py -q   # 10 unit tests
```

## Calibration results (2026-08-12, pre-model-rows)

| Case | Instrument | Expected | Got |
|---|---|---|---|
| planner-protocol-shaped | score_planner + federal fixture | PASS, gate 11/11, no fabrications, zero trap markers | PASS, 11/11, 0 markers |
| planner-baseline-shaped | 〃 | NEEDS REVIEW + FABRICATION (7.D-ColorContrast) | NEEDS REVIEW + line present |
| planner-mixed-fabricating | 〃 | gate-saturating text still forced to NEEDS REVIEW by fabricated 5.E-ControlLabel | NEEDS REVIEW + line present |
| planner-undeclared-creep | score_planner + non-508 metadata | NEEDS REVIEW + out-of-scope VIOLATION | NEEDS REVIEW + line present |
| planner-trap-taker | 〃 | NEEDS REVIEW — fluent all-four-baits plan caught by trap markers | NEEDS REVIEW, gate 7/11, **5/5 markers** |
| planner-cross-baseline-prose | 〃 | PASS — documents ID in boundary-declaring prose is flagged for reading, never auto-failed | PASS + `!` line |
| bugreport-correct-federal | score_bugreport + federal fixture | PASS (5.A-ControlName filed) | PASS |
| bugreport-fabricated-id | 〃 | FAIL (5.E-ControlLabel) | FAIL |
| bugreport-missing-row | 〃 | FAIL (declared scope, no Baseline test row) | FAIL |
| bugreport-24a-filed | 〃 | FAIL (24.A always passes; filing it is the violation) | FAIL |
| bugreport-documents-id | 〃 | FAIL (11.A-DocumentTitled is documents-only) | FAIL |
| bugreport-undeclared-creep | score_bugreport + axe-image-alt-single | FAIL (citation outside declared scope) | FAIL |
| bugreport-clean-non508 | 〃 | PASS (extension inert without citations) | PASS |
| bugreport-wrong-but-valid-neighbor | score_bugreport + federal fixture | FAIL — files 10.A-FormName while quoting 5.A in prose; the FILED value is compared, not mere mention | FAIL + "not FILED" |
| bugreport-json-filing | 〃 | PASS — `"baseline_test": "5.A-ControlName"` recognized as a filed row | PASS, filed rows 1 |
| bugreport-stale-ledger-id | 〃 | FAIL — filing `21.B-AutoUpdate` gets the ledger hint (valid ID is 21.C-AutoUpdate) | FAIL + hint |

**Regression — the extension is inert on history:** all 65 committed response
files across the bugreport and planner lanes rescored with the extended
scorers → zero baseline findings on all 65 (the durable property the
committed harness asserts), and a one-time old-vs-new scorer A/B (old
scorers materialized from the pre-change git HEAD) produced **65/65
identical statuses**.

**Critic gate (bench-reviewer, 2026-08-12, verdict REVISE — all findings
fixed pre-commit and re-calibrated).** The two blocking findings reshaped the
instrument:

1. *The filed value is the check.* The bug-report scorer originally validated
   the expected ID against the whole text — a wrong filing with the right ID
   quoted in a "candidates considered" footer scored PASS. Now the expected
   ID must appear among the FILED rows (`bugreport-wrong-but-valid-neighbor`
   is the regression case), and the filed-row regex accepts dash bullets,
   prefixed labels, parentheticals, table rows, and JSON-shaped fields
   (unit-tested) while still rejecting prose mentions — which is what keeps
   the 24.A prose-vs-filed distinction meaningful.
2. *The keyword gate is polarity-blind; trap markers carry polarity.* The
   critic's probe — a fluent plan taking all four baits with no fabricated
   IDs — scored **8/11 PASS** on the original keywords. The honest framing:
   items 1, 3, 5, 7, 9, 10 use vocabulary a trap-taking plan emits as
   readily as a correct one. Fixes: the `boundary` keyword dropped from the
   PDF item, profile-literal strings added to the dual-posture item (it was
   the one item the FEDERAL PROFILE did not literally teach), count-shaped
   alternates added to the coverage item, and a `trap_markers` metadata
   block whose regexes match bait-AGREEMENT language and force NEEDS REVIEW
   regardless of gate score (the fabrication-override pattern). The adapted
   trap-taker now scores 7/11 on keywords and fires 5/5 markers. Marker
   patterns are negation-aware where calibration demanded it (a correct plan
   *quoting* the vendor's "WCAG 2.2 replaced it" claim in order to refute it
   must not fire) and every marker hit is a read-this-row signal, not a
   verdict.

If future live baselines saturate this gate WITHOUT tripping a marker or the
fidelity check, treat it as an instrument finding — but read the row first:
the gate is a detector at every layer.

## Model rows

None — and the reason is an environment finding, disclosed: at build time
(2026-08-12) the host's native Metal ollama server (the one the wcag-em-step11
rows ran on) no longer exists. The only server answering on either loopback is
a CPU-only container at ollama **0.23.0** (`/api/ps` shows `size_vram: 0` for
the loaded model; no native ollama process). Consequences: `qwen3.6:35b` (the
recommended detector, needs ollama ≥0.31) cannot even be pulled there, and a
qwen3:32b attempt on the federal fixture (the lane's largest prompt: protocol
+ crosswalk ≈ 19k tokens) timed out the runner's 1200s client ceiling on CPU
prompt-eval alone. Per the BENCHMARK.md discipline on mixed CPU/Metal
timings, no row was forced through.

First rows (hosted + local, both planner conditions + the bug-report fixture)
are tracked on the adoption issue; they land in this directory as
`ollama-planner-federal-*` / `ollama-planner-*` / `ollama-bugreport-*`
response files with matching `score-*` files once a Metal-class local server
or hosted lane runs them. Also tracked there: `run_cloud_benchmark.py`
carries the fixture but not the `planner-federal` condition, so hosted
planner rows are the no-crosswalk condition until that parity lands — any
cross-family table must label the condition per row. The detector-not-verdict
routing rule extends unchanged: a local model may surface candidate 508
framing, never conclude conformance.
