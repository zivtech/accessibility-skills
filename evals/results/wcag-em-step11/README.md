# WCAG-EM Step 11 — First Rows on Both Instruments: Two Draws + Control (2026-08-01)

First live rows on the two step-11 instruments the same day they were built
(adoption plan: [docs/wcag-em-2-adoption-assessment.md](../../../docs/wcag-em-2-adoption-assessment.md),
Step 11 status): the evaluation-report chain lane (`transit-portal-q3`,
contract vs baseline conditions) and the de-hinted planner audit fixture
(`test-hybrid-product-audit`). Coverage: **qwen3.6:35b × 2 draws per
condition** (byte-identical prompts, temp 0.3) plus a **qwen3:32b single-draw
control** — the same model that scored 11/11 draw-stable on the *hinted*
sibling in the step-10 A/B, which makes it the cleanest possible probe of
the de-hint.

Files without a draw suffix are draw 1; `-draw2-` marks the repeat;
`qwen3-32b` files are the control (one draw). Every response has a matching
`score-*.txt`.

## Method

- Runner: `ollama/run_benchmark.py` (`evalreport` / `evalreport-baseline` /
  `planner`), temp 0.3, evalreport num_ctx 32768. Native Metal server on
  IPv4 `127.0.0.1:11434`.
- **Server gotcha, disclosed:** the very first launch 404'd — on this
  dual-stack macOS host `localhost` resolves `::1` first, where the CPU-only
  OrbStack container listens with a 5-model store lacking qwen3.6:35b. The
  runner default now pins 127.0.0.1 (matching `ollama_a11y.py`). Historical
  note: models present on *both* servers (e.g. qwen3:32b) would have run
  correctly-but-on-CPU under the old default, so elapsed-seconds columns in
  older lanes may mix CPU and Metal timings — detection scores unaffected.
- Scoring: `ollama/score_evalreport.py` (post-calibration, including the
  interrogative-line exemption below) and `ollama/score_planner.py`
  (untouched). **No instrument was tuned between draw 1 and draw 2 or for
  the control** — keyword-undercount candidates found by adjudication are
  recorded here for a future instrument rev, not applied mid-measurement.

## Results

| Instrument | Condition | qwen3.6:35b d1 | qwen3.6:35b d2 | qwen3:32b (control) |
|---|---|---|---|---|
| evaluation-report | contract | **WARN** (0 must, 0 fab) | **FAIL** (3 must, 0 fab) | **FAIL** (1 must, 0 fab) |
| evaluation-report | baseline (no contract) | **FAIL** (12 must) | **FAIL** (9 must) | **FAIL** (18+ must) |
| planner de-hinted #26 | full protocol | **7/11** NEEDS REVIEW | **9/11** PASS | **3/11** NEEDS REVIEW |

Elapsed: 35b 72–182s/run; 32b 178–362s/run.

## Evaluation-report lane

**What is draw-stable: the A/B direction.** In every draw of every model,
the no-contract baseline FAILs on report *shape* — the per-SC outcome map,
the coverage-boundary declaration, and the random-selection method do not
exist without the contract (35b baseline: 12 → 9 must misses across draws,
same failure class; 32b baseline: 18+ must misses, four required sections
missing outright). What the contract carries is the report's shape.

**What is not draw-stable: the 35b contract verdict.** Draw 1 WARN — every
trap passed, severities carried per-finding. Draw 2 FAIL — the findings
section lists all eight ids, keeps the orthogonality *sentence*, and drops
the severity *data* entirely: no CRITICAL/MAJOR/MINOR token anywhere in the
document. Adjudicated a legitimate must-tier failure, not a scorer format
gap (checked: severities appear nowhere, in any format). This is the exact
data-fidelity class CLAUDE.md already flags for qwen3.6:35b (silent loss of
exact field values); the lane now demonstrates it at WARN↔FAIL magnitude on
byte-identical prompts. Consequence for routing: a local contract-condition
report is detector output — human reads the report before it leaves the
building, every time.

**Control nuance:** qwen3:32b's contract run is the best single evalreport
row by miss count (1 must miss: it reported 1.2.x as `untested` where the
evidence — "no audio or video content exists" — supports `inapplicable`; a
real vocabulary-class error, the conservative direction, not a fabrication).
Single draw; no stability claim.

**Adjudication notes carried from draw 1, plus new ones:**

- Draw-1 baseline's "assertive claim" fabrication was overturned on reading
  (the response *quoted the commissioner's question* above an explicit
  "Determination: No."); the scorer now exempts interrogative lines —
  questions are not assertions. Fix landed before any row was published;
  calibration/smoke unchanged; flatters neither condition.
- The baseline's representativeness `must_contain` group can hit
  coincidentally ("expanded **states**" — UI vocabulary, not sample
  expansion), so measured contract-vs-baseline gaps are conservative.
- Embellished-rationale class, present in **both models**: 3.1.2 rationales
  claim "no multilingual content exists" — the evidence never says that,
  only that nothing evaluated the criterion. Outcome tokens correct,
  rationales invented. The 32b contract run also writes "EARL export
  available at `https://example.com/earl/rcm-2026q3.xml`" — an invented
  artifact reference for an export nobody produced (the contract marks
  machine_readable *optional when produced*). The scorer grades outcome
  classes and listed tokens, not rationale prose; readers of these reports
  must not.

## Planner lane: the de-hint holds, and the control is the proof

**qwen3:32b — 3/11.** The control model scored **11/11 draw-stable on the
hinted sibling** (`evals/results/wcag-em-phase3/`) and 25/25 on the planner
suite. De-hinted, with the identical protocol in its system prompt, it
produces a component-style protocol walk with **zero evaluation
methodology**: no WCAG-EM naming, no random sample, no 10% rule, no
complete-process framing, no support-baseline declaration, no statement
restraint ("sampling strategy: high-risk surfaces prioritized" is the
entire sampling story). The eight misses are real absences, not keyword
undercounts — adjudicated by token sweep and read. **The hinted fixture's
saturation was fixture-cueing; the de-hint removes it, on the same model.**
Consistent with step-10's depth-marker finding (qwen 1→5/12 markers under
the new protocol: partial EM uptake, nowhere near operationalization).
Note: even at 3/11 it passes the central trap — mobile flows routed to
manual TalkBack/VoiceOver, axe's blind spots named. False-coverage honesty
and methodology knowledge are different capabilities.

**qwen3.6:35b — 7/11 → 9/11 across draws (NEEDS REVIEW → PASS).** Status
flips at exactly the item-flip magnitude the variance discipline predicts.
Item-level picture:

- Draw 1's two genuine gaps (support-baseline declaration, statement
  restraint) are **present in draw 2** ("Partial conformance
  documentation", explicit baseline section) — they were capability, not
  absence; single draws under-sample it.
- The native-boundary item misses in both draws **as a keyword artifact**:
  draw 2 writes "the QA lead's current axe DevTools + Playwright setup …
  **cannot evaluate native mobile apps or PDFs**" and ships a "Coverage
  Honesty Statement" deliverable — but the gate keywords are
  `boundary`/`does not run`/`do not run`. Recorded as an undercount both
  draws; `cannot evaluate` / `cannot measure` are candidate keywords for a
  future rev (not applied mid-measurement).
- The representativeness-comparison rule cuts the other way: **present in
  draw 1** ("if new finding types appear, structured sample expanded and
  re-checked" — an undercount there), **genuinely absent in draw 2**. Item
  variance runs in both directions; neither draw alone would have shown it.
- Central false-coverage trap: passed in both draws, more explicitly in
  draw 2.

Content-adjudicated: d1 ≈9/11, d2 ≈10/11. Measured rows stand as scored —
adjudication is reported, never substituted.

## What this does not claim

- Not stable rows for anything single-drawn (all three 32b rows).
- Not a full planner-lane run: one fixture; BENCHMARK.md's 25-fixture
  aggregates and the n/26 denominator rule are untouched.
- Not evidence that the contract condition "passes" for qwen3.6:35b: the
  two-draw record is WARN/FAIL, and the unstable dimension (severity
  carriage) is must-tier.
- Not a comparison of model quality beyond these two fixtures and these
  draws.
