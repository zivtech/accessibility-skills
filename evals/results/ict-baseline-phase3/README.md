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

## Model rows — first local rows, 2026-08-12 (same day, hours after calibration)

**Environment note, disclosed:** at instrument-build time the native Metal
ollama server did not exist (no ollama process; only a CPU-only 0.23.0
container answered, `size_vram: 0`; a 32b attempt timed out the runner's
1200s ceiling and no row was forced through). The Ollama.app was running
again later the same day — native server **0.32.5** on `127.0.0.1:11434`,
`qwen3.6:35b` confirmed fully in VRAM (`size_vram` 24.0 GB) — and all rows
below are Metal-class timings. No pull was needed: both qwen3.6 models were
in the intact 327 GB native store all along.

| Row | Condition | Gate / Status | Elapsed |
|---|---|---|---|
| qwen3.6:35b planner | planner-federal (crosswalk in-prompt) | **10/11 PASS**, 0 markers, 0 fabrications | 107s |
| qwen3.6:35b planner | planner (no crosswalk) | 9/11 → **NEEDS REVIEW** (trap marker, adjudicated false-fire) | 97s |
| qwen3.6:35b bugreport | declared-508 | **FAIL** (value fidelity; baseline filing CORRECT) | 90s |
| qwen3:32b planner (control) | planner-federal | **10/11 PASS**, 0 markers | 602s |
| qwen3:32b planner (control) | planner (no crosswalk) | 7/11 → **NEEDS REVIEW** (gate) | 364s |
| qwen3:32b bugreport (control) | declared-508 | **FAIL** (wrong-but-valid neighbor FILED) | 136s |

**Adjudication (every row was read; the gate is a detector):**

- **35b planner-federal (10/11):** the single miss is a confirmed FALSE MISS
  on paraphrase-prone item 8 — the plan writes "~200 PDFs … fall outside the
  web measurement stack and require dedicated manual evaluation" with no
  listed keyword. Content-adjudicated ≈ 11/11. Certification polarity clean
  ("recognized standards, not certifications"). One flag: it schedules
  "Draft VPAT" as a deliverable — the polarity-blind item-10 hit is
  ambiguous against the annex-feeds-the-ACR boundary; noted, not scored.
- **35b planner no-crosswalk (9/11, NEEDS REVIEW):** the
  `adopts-22-as-conformance-basis` marker fired on a CONCESSION INSIDE A
  REFUTATION ("WCAG 2.2 is the current public standard and will be evaluated
  as *recommendations*. However, Revised Section 508 legally mandates
  WCAG 2.0 …") followed by textbook dual posture — **marker false-fire,
  row adjudicated correct**; the read-verify loop worked as designed. The
  condition's instrumented behaviors: the coverage statement HEDGED honestly
  — literally "Designed to cover **N** of 62 … gaps: …" with N left unfilled
  and zero invented counts (two listed gaps are template echoes of the
  profile's boundary examples) — and its only baseline-ID citation, from
  memory, was a valid, correctly-explained `24.A-Parsing`. Zero fabrications
  in the fabrication condition.
- **35b bugreport (FAIL):** **filed `5.A-ControlName` correctly** — the new
  check's core question — while FAILing on the model's documented
  value-fidelity classes reproducing on cue: CSS selector dropped (XPaths
  only), fabricated "VoiceOver (default)" in an automated scan's environment
  table (honest-N/A trap), and stable IDs copied from the skill doc's
  example hashes instead of computed.
- **32b planner-federal (10/11):** used the supplied crosswalk for a real
  NOT-COVERED enumeration (9.A, 16.A/B, 17.E, in family-shorthand — not
  full-grammar tokens, so unvalidated by the ID check; noted). Item-9 miss
  is real-ish in spirit: it answers "No official government stamp" but adds
  "methodology **aligns with federal standards**" — brushing the
  self-declared-alignment reject the keyword gate cannot see.
- **32b planner no-crosswalk (7/11, NEEDS REVIEW):** **the sharpest
  discrimination of the run — it FABRICATED coverage counts**: "54/62 web
  baseline tests performed; **45/57 PDF baseline tests performed**" —
  inventing both numbers and a documents-baseline capability the stack
  declaredly lacks, while its automated-testing table also lists "PDFs: 200
  files" under axe-core+Playwright coverage (absorption in table form, which
  the sentence-shaped markers do not catch). Numeric-count fabrication
  carries no ID-grammar token, so it is caught by adjudication, not the ID
  check — recorded as the condition's headline hazard. Item-2 miss is a
  false miss (correct dual posture, no keywords: "Compliance is with
  WCAG 2.0 A/AA … Remediation recommendations will include WCAG 2.2 AA …
  e.g., 1.4.10 Reflow"); the 24.A/parsing item is a REAL miss (it
  accommodates the HTML checker without ever teaching the auto-pass — same
  system prompt that 35b nailed it from).
- **32b bugreport (FAIL): the S1 filed-value check's first live catch** —
  it filed **`5.C-ControlState`** for a missing accessible NAME, the
  wrong-but-valid near neighbor the fixture exists to discriminate
  ("expected baseline ID 5.A-ControlName not FILED (filed:
  5.C-ControlState)"). Before the critic gate forced the filed-value
  comparison, this row would have scored the citation as merely valid. Same
  fabrication class as 35b on the environment table ("VoiceOver / NVDA").

**Cross-row facts:** zero fabricated baseline-test IDs in all six rows (the
ID-grammar fabrication class did not fire once — the live fabrication risk
materialized as invented COUNTS, not invented IDs); the federal condition
outscored the no-crosswalk condition on both models (10 vs 9; 10 vs 7); and
both models' bugreport value-fidelity failures reproduce the standing
never-route-generation-without-a-value-check caveat, now with the baseline
field itself instrumented.

**Future instrument-rev candidates (recorded, not applied mid-measurement,
per the step-11 discipline):** the `adopts-22-as-conformance-basis`
alternative `WCAG 2.2 … (is|as) the current standard` fires on
concede-then-refute phrasing (one false-fire in two rows); table-form PDF
absorption ("PDFs: 200 files" under an automated-coverage heading) evades
the sentence-shaped `absorbs-documents-into-web-scan` patterns; and a
count-consistency check (quoted N/62 must match the supplied crosswalk's
totals in the federal condition, and must not exist as concrete numbers in
the no-crosswalk condition) would mechanize what adjudication caught in the
32b fabrication.

Open on the adoption issue: hosted rows, and `run_cloud_benchmark.py`
`planner-federal` condition parity (hosted planner rows are the no-crosswalk
condition until it lands — label the condition per row in any cross-family
table). The detector-not-verdict routing rule extends unchanged: a local
model may surface candidate 508 framing, never conclude conformance.
