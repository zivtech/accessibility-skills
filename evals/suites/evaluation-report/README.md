# evaluation-report eval suite

Measures the report-level seam that the finding-level `bug-reporting` lane
deliberately does not (adoption plan step 11(b),
`docs/wcag-em-2-adoption-assessment.md`): given a **finished** audit's
evidence — the model tests nothing and decides nothing new — does it
aggregate that evidence into the shape required by
`docs/a11y-evaluation-report-contract.md` without inventing, collapsing, or
over-claiming?

The contract **is** the skill under test (prompt-only repo): the lane's
system prompt is the contract document itself, the same loading idea as the
skill lanes. The fixture's task instruction stays minimal on purpose — every
honesty rule being graded (untested ≠ passed, severity ⊥ outcome, boundary
carry, statement restraint) must come from the contract, not the task prompt.

## Fixtures (1)

| Fixture | Input format | Difficulty | What it tests |
|---|---|---|---|
| `transit-portal-q3` | engagement record + sample log + 3 evidence streams (axe batch, keyboard-a11y-tester batch + driven, manual native/PDF sessions) + 8 evidence-finding blocks | COMPLEX | Aggregation honesty: never-evaluated criterion reported untested (not passed), severity kept orthogonal to outcomes and per-finding, finding_id integrity both directions, native/PDF coverage boundary carried, product-wide conformance sentence refused |

Every fixture is a **triplet**: `fixtures/<id>.md` (the evidence package,
sent to the model verbatim), `fixtures/<id>.metadata.yaml` (machine-checkable
expectations, never sent), `rubrics/<id>.rubric.yaml` (dimension tiers and
adjudication notes, never sent).

## Conditions

- **contract** (default): `docs/a11y-evaluation-report-contract.md` as the
  system prompt.
- **baseline**: identical fixture, no system prompt — measures what the
  contract carries. Baseline output files get the
  `ollama-evalreport-baseline-` prefix and never count as contract-condition
  runs.

## Why there is no blind cut line here

Same reasoning as `bug-reporting`: the fixture is an **input**, not a
component with planted bugs. The `.md` contains only the evidence package an
agent would actually receive; every expectation lives in
`.metadata.yaml`/`.rubric.yaml`, which never enter a prompt. There is nothing
to strip; `strip_answer_key()` passes the file through unchanged.

## Scoring (`ollama/score_evalreport.py`, rule-based)

```
python3 ollama/score_evalreport.py <response.json> <fixture>.metadata.yaml
```

Checks, all driven by metadata:

1. **Required sections** — the contract's nine required sections (heading
   scan with whole-document token fallback).
2. **finding_id integrity, both directions** — all eight ids present; any
   other `a11y_*` token is an invented finding (hard FAIL). The un-id'd
   evaluator scratch note in the input is the bait.
3. **Severity preservation** — the orthogonality probe: 2.1.1 stays CRITICAL,
   the 4.1.2 swap-button stays MINOR, the second 4.1.2 finding stays MAJOR.
   The match span truncates at the next finding-id token so a list neighbor's
   severity can never satisfy the check.
4. **Per-SC outcomes** — seven evidenced failures reported `failed`; 3.1.2
   reported untested-class, where a surviving `passed` is a fabrication
   (nothing evaluated it); 1.2.x inapplicable. Should-tier: the three
   evidenced passes.
5. **Aggregation fidelity** — representativeness result reported honestly
   (divergence → S11 expansion), random-selection method (seeded shuffle,
   seed 7391), support-baseline echo as evaluated, identity/methodology/dates;
   boundary-scoped groups for the native app and PDFs.
6. **Statement discipline** — after negation-stripping (honest refusals and
   withholding phrasing survive), any assertive product-wide conformance
   claim is a hard FAIL.
7. **Fabricated environment tokens** — JAWS/Dragon appear in no input stream;
   word-boundary presence is a hard FAIL (training-prior regurgitation).

Status: **PASS** (all musts, no fabrication), **WARN** (musts pass,
should/nice missed), **FAIL** (any must missed or fabrication detected).

## Instrument calibration (2026-08-01)

Three synthetic reports (authored fresh, not committed — same practice as the
step-11a planner fixture; reproduce from this section plus the metadata):

- **Contract-shaped honest report** → PASS, 0 must / 0 fabrication / 0 should.
- **Musts-pass, shoulds-missed report** (failures-only outcome table, no
  statement language, no orthogonality note) → WARN with exactly the five
  intended should/nice misses.
- **Trap-hitting over-claimer** (3.1.2 passed, invented ninth id from the
  scratch note, JAWS in the baseline, both severity re-ranks, boundary
  section dropped with an "automation covered the app" claim, assertive
  county-filing conformance sentence, seed/S11/TalkBack omitted) → FAIL with
  12 must misses + 4 fabrications; every trap family fired individually.

Two adversarial probes: honest withholding phrasing containing the quoted
claim but no classic negation word → PASS with no false claim hit; a bare
assertive claim appended to the otherwise-honest report → FAIL.

Calibration caught three instrument defects, fixed the same day: the
metadata's `description` plain scalar did not parse (colon in a continuation
line), the severity window bled into neighboring list findings and masked
both planted re-ranks (now truncated at the next id token), and honest
withholding sentences without cannot/not/no tripped the assertive-claim scan
(withholding stems added to the negation strip).

No model rows yet — instrument validated, contract and baseline conditions
unrun.

## Running the lane

```
# contract condition (the lane)
python3 ollama/run_benchmark.py evalreport qwen3.6:35b transit-portal-q3

# baseline condition (what does the contract carry?)
python3 ollama/run_benchmark.py evalreport-baseline qwen3.6:35b transit-portal-q3

# all un-benchmarked fixtures, contract condition
python3 ollama/run_benchmark.py evalreport-remaining qwen3.6:35b

# score
python3 ollama/score_evalreport.py /tmp/ollama-evalreport-transit-portal-q3-<model-tag>-response.json \
  evals/suites/evaluation-report/fixtures/transit-portal-q3.metadata.yaml
```

## Known instrument limits

- Any-token line checks undercount paraphrase: an outcomes line naming
  "Language of Parts" without `3.1.2` misses the untested must. Adjudicate
  misses by reading before counting them (wcag-em-phase3 practice).
- The negation strip is a heuristic in both directions — it can be evaded by
  a claim sharing a line with a negation word, and paraphrased claims that
  avoid the listed phrasings pass it. Adjudicate by reading.
- Bonus inferences (adding 2.5.7 Dragging Movements as failed for the
  drag-only slider) are defensible extensions, not fabrications; unchecked
  either way.
- Scorer statuses are detector output, not verdict authority — the repo-wide
  local-model routing rule applies unchanged.

## Out of scope (deliberate)

EARL machine-readable export and VPAT/ACR template population (no consumer in
the benchmark; the contract keeps them routed to external tools), and
WCAG-EM Report Tool integration (Phase 4 watch item — the tool has not
shipped).
