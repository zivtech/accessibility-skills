# acr-reporting Phase 4 — Lane C calibration and first rows (2026-08-13)

Phase 4 Part 1 of the OpenACR integration plan: the Lane C drift protocol
(two OpenACR documents for one product → a drift report), fixtures 6/6b,
the `lane: c` scorer path, and first rows. Part 2 (upstream filing) was
executed 2026-08-13 — five issues on `GSA/openacr`, receipts in
`docs/openacr-reference.md` §Upstream. Prior phases:
[phase2](../acr-reporting-phase2/) (Lane A), [phase3](../acr-reporting-phase3/)
(Lane B).

## What Lane C measures

Two ACRs for the same product, and nothing else. The protocol's load-
bearing split is **self-produced vs foreign, decided by fingerprints
rather than authorship**: a pair whose adherence notes carry our own
`finding_id` + `fingerprint` values supports finding-level trend; any
other pair supports term-level deltas only, because the evidence
contract's trend vocabulary against a foreign document fabricates a
comparison history that does not exist.

The traps that follow from that split are what the two fixtures price:

- **Read the fingerprint before the term.** A criterion that moves
  `does-not-support` → `partially-supports` while its finding is still on
  the ledger is `improving`, not `resolved`; one that moves the other way
  under a single fingerprint is `worsening`, not a new finding.
- **Two ACRs rest on two sample sets.** WCAG-EM re-evaluation guidance
  keeps a sub-set and replaces a sub-set by design, so a delta whose
  evidence lives only in a newly added sample is a coverage change, not
  movement.
- **A term delta is never a product delta**, and for a foreign pair it is
  not even an evidence delta — the vendor rewrote a sentence.

## Instrument calibration (before any model row)

`calibrate.py` (committed; exit 0 = CLEAN; `--dump` writes `score-cal-*`
receipts): honest drift reports derived from each fixture's metadata —
so metadata self-consistency is itself under calibration — plus
trap-taking, dramatizing, comparability-dropping, trend-leaking,
absence-missing and shoulds-missed mutants. **10/10 CLEAN.** Lane A
(9/9) and Lane B (6/6) re-run CLEAN after the shared-code edits, so the
`lane: c` addition carries no regression.

### Instrument defects found by calibration, fixed before any row

| Defect | How it surfaced | Fix |
|---|---|---|
| Line-level negation guard swallowed real overclaims | The dramatizer mutant's "Overall accessibility improved this cycle." sat on the same line as the honest summary's own anti-overclaim sentence, which carries "never" — so the line was exempted and the violation went unseen | Overclaim scan moved to **sentence** scope with a local negation guard; the broad line-level `TREND_NEGATION` stays where it belongs, on the forbidden-trend scan |
| The claim-change gate passed on the bare word "claim" | The trend-leaker mutant kept the column header `v9.3 claim`, which satisfied the check on its own — "claim" is free vocabulary in a document diff | Gate is now **colocated**: one sentence must carry both halves (this is a claim / nothing verified it) |
| The 3.1.2 claim-hygiene check was unfailable | `not-evaluated` was in the token list, and it is the row's own prior term, so every possible report matched | Token dropped; the check now keys on the hygiene vocabulary (AAA-only, illegal, reserved) |
| `mar-2026v1` wrongly listed as a fabrication token | The foreign fixture's engagement record names that closed verification as out of scope, so a report may legitimately cite it while excluding it | Removed; the cross-lane bleed check is the empty `expected_finding_ids` — importing any `a11y_*` id from the Lane B fixture is the real fabrication |

Two calibration cases also proved the scorer right and the *mutant*
wrong, which is worth recording: a caveat carried on the trend row rather
than the delta row is still a caveat, and a report whose every delta row
says "unverified" has framed its claims. Both mutants were strengthened
rather than the checks weakened.

## Method

Identical to Phases 2 and 3 (general-purpose opus subagents; the skill
read from the repo in the skill condition, all repo reads forbidden in
baseline; fixtures staged alone in a scratch directory so the grading
metadata is unreachable; per-row `_benchmark` disclosure). The Lane C
deliverable is Markdown, so no CLI validation applies to it.

## Rows (7)

| Row | Condition | Draw | As first scored | Final | Must / Fab / Should |
|---|---|---|---|---|---|
| opus f6 `transit-portal-drift-self` | acr | 1 | WARN | **PASS** | 0 / 0 / 0 |
| opus f6 `transit-portal-drift-self` | acr | 2 | WARN | **PASS** | 0 / 0 / 0 |
| opus f6b `shiftline-drift-foreign` | acr | 1 | WARN | **PASS** | 0 / 0 / 0 |
| opus f6b `shiftline-drift-foreign` | acr | 2 | WARN | **WARN** | 0 / 0 / 1 (read-adjudicated false miss) |
| opus f6 baseline | acr-baseline | 1 | FAIL | **FAIL** | 1 / 0 / 2 |
| opus f6 baseline | acr-baseline | 2 | FAIL | **FAIL** | 2 / 0 / 2 |
| qwen3.6:35b f6 (local detector) | acr | 1 | PASS | **PASS** | 0 / 0 / 0 |

The two status columns are the same rows scored before and after the
should-tier instrument revision disclosed below. **No must-tier result
changed**, and the revision is the only difference between them.

**Skill condition: 4/4 must-clean, both fixtures, both draws — zero
must-tier misses and zero fabrications.** Adjudication highlights (every
row read):

- **f6 both draws** name the pair self-produced *by fingerprint rather
  than by authorship*, quoting a fingerprint that appears in both
  documents; get all eight trends right; and reason explicitly through
  both discrimination traps rather than landing on them by luck — draw 1:
  "Better term, unresolved finding… `improving`, not `resolved`. A better
  term alone never earns `resolved`", and on the mirror trap "`worsening`,
  not a new defect: nothing new was found, an existing defect was rolled
  out across more of the product." Both mark 2.4.11 non-comparable, both
  state the carried-over / retired / added split, and both close with an
  explicit anti-overclaim section (draw 1: "Four improved rows against two
  worsened rows is not a product that got more accessible, and must not be
  summarized that way in any release communication").
- **A sharper reading than the fixture asked for:** draw 1 declines to
  give 1.4.3 an SC-level row at all, because its term is identical in both
  cycles while only its note moved (S03+S09 → S03+S15) — "The sample list
  moved; the finding did not. Reporting that as movement would be
  manufacturing a delta." That is the FP arm reasoned from first
  principles, on a criterion the metadata does not police.
- **f6b both draws** hold the foreign boundary completely: **zero
  occurrences of any trend token** in either row, every changed term framed
  as a claim change, the withdrawn 1.2.2 row caught, routing sent to Lane B
  and explicitly not to `bug-reporting`. Draw 2 goes further than the
  fixture's own reference answer: it observes that neither vendor document
  discloses a sample set, method, or coverage boundary, and therefore marks
  **0 of 5 deltas comparable** — deriving the comparability rule's
  consequence for a document pair that cannot support it at all. It also
  catches that the v9.6 withdrawal of 1.2.2 contradicts the same document's
  own 1.2.3/1.2.5 rationale, and refuses to resolve the contradiction:
  "This is a question to put to the vendor in writing, not something to
  infer."

## A/B condition — draw-stable, and the same shape as Lanes A and B

Both baselines FAIL on **vocabulary carry, not judgment**. Each built its
own trend taxonomy — draw 1's is `Closed` / `Open and worsening` / `Open
and improving` / `Open and flat` / `New` — which maps onto the ground
truth *exactly* (3 closed, 1 worsening, 1 improving, 2 flat, 1 new) while
matching none of the evidence contract's five terms, so trend extraction
misses seven of eight rows by construction. Both nonetheless got the
SC-level deltas right (6/6, both terms), cited every fingerprint,
dramatized none of the fifty stable criteria, and fabricated nothing; draw
1 reasoned about sample drift unprompted ("Sample drift, and what it costs
the comparison"). Draw 2 additionally omits any sample-scope statement,
the second must.

What the Lane C protocol carries is therefore the **machine-consumable
contract** — the evidence contract's trend vocabulary, the two canonical
tables, the comparability statement, the anti-overclaim sentence — not the
drift judgment, which bare opus already has. That is the third consecutive
lane with this result.

## Local detector row — first local PASS in this suite, and read anyway

qwen3.6:35b on f6, skill condition: **PASS at every tier** — all eight
trends correct including both traps, all eight fingerprints cited, 6/6 SC
deltas, the non-comparable row marked, the FP arm clean, zero fabricated
ids or fingerprints. Lane C's Markdown deliverable sidesteps the local
tier's machine-format weakness exactly as Lane B's did, and the drift task
is more mechanical than either.

**The status is still detector output, and reading it proves why.** Three
errors sit in prose the scorer does not read:

1. Its 1.3.5 delta row says "S07 was retired from the sample set" — S07 is
   a carried-over sample that was *fixed*. Its own trend row states this
   correctly ("fails only in S08 (carried over) vs prior S07+S08"), so the
   report contradicts itself on the fixture's central trap.
2. It states that `worsening` and `new` trends "retire defects from the
   prior document's ledger" — backwards; `resolved` retires, the other two
   add.
3. It routes the self-pair's open findings to Lane B. Lane B is the
   *foreign* remedy; our own verified findings route to `bug-reporting`.

None of the three is in a scored dimension. Recorded as instrument-revision
candidates for the next phase — a self-consistency check between a delta
row's sample claims and its trend row's would have caught (1) — and **not**
applied mid-measurement.

## Instrument revision from the rows (one, should-tier, disclosed)

| Revision | Trigger | Effect |
|---|---|---|
| Count checks moved from token lists to order- and punctuation-insensitive patterns (`summary_should_patterns`) | **All six opus rows** stated their counts in tables (`` `resolved` 3 · ``, `\| Terms changed \| 4 \|`) and all six were scored as missing them — the token groups encoded prose word order, not the check's stated intent | Should-tier only, **no must-tier result changed**: three rows WARN→PASS, three unaffected. Lane C re-calibrated 10/10; Lane A 9/9 and Lane B 6/6 re-run CLEAN |

**One revision, then stop.** f6b draw 2 still scores a should-miss because
it writes `| Term deltas | 4 |` — "deltas" rather than "changed/criteria/
terms". The count is plainly present, so this is recorded as a
**read-adjudicated false miss** and the pattern was *not* loosened again:
one revision for a systematic flaw across all six rows is instrument
repair, a second for a single row's noun choice is fitting the check to
the data. (Phase 2 precedent: `campus-events-untested` draw 1.)

## Skill amendment from the rows (one, post-scoring)

The Lane C Boundaries stated where *foreign* drift routes but never where
a **self-pair's** open findings route. Both opus draws supplied the missing
rule unprompted and identically — draw 2: "they route on the strength of
the **rcm-2027q1 evaluation's** evidence — which did test — not on the
strength of this diff" — while the local row got it wrong (routed to Lane
B). A rule that the strong tier derives and the weak tier misses is a rule
the protocol should state, so it is now stated in both mirrors. No scored
dimension changes; all seven rows above predate the amendment.

## Reproduce

```
python3 evals/results/acr-reporting-phase4/calibrate.py    # exit 0 = CLEAN (no CLI needed for lane C)
python3 ollama/score_acr.py \
  evals/results/acr-reporting-phase4/ollama-acr-transit-portal-drift-self-qwen36-35b-response.json \
  evals/suites/acr-reporting/fixtures/transit-portal-drift-self.metadata.yaml
```

Scorer statuses are detector output; every verdict below was made by
reading the row.
