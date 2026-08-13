# acr-reporting Phase 3 — Lane B calibration and first rows (2026-08-12)

Phase 3 of the OpenACR integration plan: the Lane B claims-audit protocol
(subject ACR + finished verification engagement → claims-delta report),
fixtures 4/4b, the `lane: b` scorer path, and first rows. Same-day
continuation of the Phase 2 gate (receipts:
[acr-reporting-phase2](../acr-reporting-phase2/)).

## Instrument calibration (before any model row)

`calibrate.py` (committed; exit 0 = CLEAN; `--dump` writes `score-cal-*`
receipts): honest claims-delta reports derived from each fixture's
metadata, plus verdict-flipping (both directions: the FP arm marks the
vendor's honest disclosed defect overstated; the miss arm confirms a real
overstatement), citation-dropping, trend-emitting, finding-inventing, and
shoulds-missed mutants. **6/6 CLEAN**, re-run CLEAN after each revision
below.

## Instrument revisions (all pre-scoring, each with its trigger)

| Revision | Trigger | Effect |
|---|---|---|
| Trend-token scan made negation-aware | **first local row**: qwen3.6:35b QUOTED the boundary rule ("trend vocabulary (persistent/…/resolved) is out of scope for third-party claims") and all four tokens fired — compliance read as violation, the documented quote-the-rule false-fire class | Local row FAIL→WARN; a rule-quote calibration probe added (6th case); the flipper's real violation line still fires |
| Fixture v2: subject-ACR YAML notes quoted | **two f4 skill draws independently discovered** the vendor YAML did not parse (my generator left the 2.4.7 remark's `Known issue:` colon unquoted — the same YAML trap that broke the local Lane A row) | No scored dimension reads the subject's parseability; all six hosted rows ran against v1 and two of them diagnosed, locally repaired for a receipt, and correctly refused to deliver a corrected ACR — recorded as adjudication color, and the unparseable-subject idea is noted as a future *deliberate* fixture candidate |
| Skill Lane B citation rule amended (both mirrors) | **both f4 skill draws flagged the same protocol gap**: understated-on-pass rows cannot cite a `finding_id` (findings are forbidden for passing checks) — the skill text over-required; the scorer had it right | Understated rows now cite the outcome-map row unless failures back them; no scoring change |
| `na_note_should` paraphrase variants ("rationale wrong" etc.) | f4 draw 2 carried the NA classification content in paraphrase | Should-tier only |

Gate-row byproduct, reproduced and folded into the reference doc +
Phase 4 handoff (Issue E): **`openacr validate` exits 0 on invalid input**
— the Invalid/Valid signal is stdout-only, so exit-status CI gates pass
broken documents silently.

## Method

Identical to Phase 2 (general-purpose opus subagents; skill read from the
repo in the skill condition, all repo reads forbidden in baseline;
fixtures staged alone; per-row `_benchmark` disclosure). The Lane B
deliverable is Markdown — no CLI validation applies to it.

## Rows (7)

| Row | Condition | Draw | Status | Must / Fab / Should |
|---|---|---|---|---|
| opus f4 `shiftline-vendor-acr` | acr | 1 | **PASS** | 0 / 0 / 0 |
| opus f4 `shiftline-vendor-acr` | acr | 2 | **PASS** | 0 / 0 / 0 |
| opus f4b `courseware-vendor-acr-clean` | acr | 1 | **PASS** | 0 / 0 / 0 |
| opus f4b `courseware-vendor-acr-clean` | acr | 2 | **PASS** | 0 / 0 / 0 |
| opus f4 baseline | acr-baseline | 1 | **FAIL** | 8 / 0 / 1 |
| opus f4 baseline | acr-baseline | 2 | **FAIL** | 4 / 0 / 1 |
| qwen3.6:35b f4 (local detector) | acr | 1 | **WARN** | 0 / 0 / 2 |

**Skill condition: 4/4 PASS, both fixtures, both draws, at every tier —
zero must, zero fabrications, zero should.** Adjudication highlights
(every row read):

- **f4 both draws:** all six planted deltas verdicted exactly (3
  overstated with citations, 2 understated incl. the illegal-term hygiene
  flag, 1 unverifiable with the SSO scope reason), the vendor's honest
  disclosed defect **confirmed** with its finding (the FP trap held), the
  NA-passes edge rows confirmed with classification notes, zero trend
  vocabulary with both tempting rows (2.4.7 "persistent", 3.3.3
  "resolved") explicitly denied the language, and routing +
  a11y-critic-adjudication gates stated. Both draws additionally
  discovered the fixture's v1 parse defect and handled it exactly as the
  protocol wants: flagged as a subject-document defect, repaired only in
  a throwaway diagnostic copy, never delivered as a corrected ACR.
- **f4b both draws:** 56/56 confirmed with the clean result stated
  plainly, sample-scoped, and not over-read — both handoffs
  independently caution that a demo-tenant pass says nothing about
  instructor-authored content, and neither manufactured suspicion to
  look thorough.

## A/B condition — draw-stable, and the same shape as Lane A's

Both baselines FAIL on **vocabulary and format carry, not judgment**:
each invented its own disposition taxonomy ("Substantiated / Refuted
(adverse) / Rationale refuted…" in one; "Confirmed / Contradicted /
Misclassified / Under-claimed…" in the other), so verdict extraction
misses rows by design; neither routes overstated claims to bug-reporting;
neither keeps the per-row citation discipline of the canonical table.
Read for substance, both caught the three overstatements, both caught the
illegal term, both refused trend language, and both held the unverifiable
row honestly — zero fabrications in both. What the Lane B protocol
carries is the machine-consumable delta contract (four-verdict
vocabulary, canonical table, citations, routing), not the auditing
judgment — mirroring the Phase 2 Lane A result exactly.

## Local detector row

qwen3.6:35b, f4, skill condition: **WARN — 56/56 verdicts correct**
(spot-read: the FP trap, both overstatement arms, the hygiene flag, and
the SSO unverifiable row are all genuinely right in its table), zero
musts after the negation-aware trend fix, two should-tier misses (NA
classification notes). The instructive asymmetry against its Lane A row
(FAIL, unparseable YAML): **Lane B's Markdown deliverable sidesteps the
local tier's machine-format weakness**. One draw, detector rule
unchanged — but the lane-asymmetry is a real routing datum: local Lane B
output is candidate-quality in a way local Lane A output is not.

## Reproduce

```
python3 evals/results/acr-reporting-phase3/calibrate.py    # exit 0 = CLEAN (no CLI needed for lane B)
python3 ollama/score_acr.py \
  evals/results/acr-reporting-phase3/claude-acr-shiftline-vendor-acr-opus-response.json \
  evals/suites/acr-reporting/fixtures/shiftline-vendor-acr.metadata.yaml
```

Scorer statuses are detector output; every verdict above was made by
reading the row. Open: Lane C (Phase 4 — handoff with ready-to-file
upstream issue drafts in `docs/plans/2026-08-12-openacr-phase4-handoff.md`),
hosted tier breadth, local baselines.
