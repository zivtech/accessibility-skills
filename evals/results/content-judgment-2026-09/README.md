# a11y-content-judgment — lane calibration, first rows, and the gate reading (2026-09-02)

Wave-2 item #1 of the engagement-tooling promotion program (dispositions v3
addendum, `docs/plans/2026-09-02-promotion-candidate-dispositions.md`):
the eval lane for the candidate skill `a11y-content-judgment`
([suite README](../../suites/a11y-content-judgment/README.md)). This
directory is the receipt trail: blindness, calibration, every model row,
every adjudication.

## Receipts in this directory

| File | What it proves |
|---|---|
| `blind-author-brief.md`, `blind-author-provenance.md` | the exact spawn text the fixture author (sonnet) received, and its own statement of what it did and did not open |
| `technique-verification.md` | every cited W3C technique id fetched live (haiku) — three reference labels corrected before any draw |
| `r5-quoted-span-calibration.md` | the quoted-span fabrication check measured on the origin engagement's 530 spot-checked rows (counts only) → should-tier |
| `calibrate.py`, `score-cal-*.txt` | synthetic cases derived from the frozen metadata — 35 CLEAN before the first model row, 43 after the test-critic fold (regression + split-group cases) |
| `claude-cj-*-response.json`, `score-claude-cj-*.txt` | opus draws packaged verbatim: 12 rubric-v0.1 (6 fixtures × 2), 4 re-draws on link-purpose-cards (v0.2 ×2, v0.3 ×2), baselines on fixtures 2 and 3 (×2) and 5 (×3) |
| `critic-a11y-critic-verdict.md`, `critic-test-critic-verdict.md` | both critic verdicts verbatim (opus) |
| `ollama-cj-link-purpose-cards-qwen36-35b-response.json`, `score-cj-…qwen36-35b.txt` | the one local detector row (exact command in `_benchmark`) |

## Method (hosted rows)

`Agent(general-purpose, model=opus)`, one subagent per draw. Rubric
condition: the subagent reads exactly two staged files — the skill's
`references/judgment-rubric.md` and the fixture `.md` — no repo access, no
search, no other reads; baseline: the fixture alone. Each subagent writes
its ```jsonl fence to a scratch file, which is packaged into the
`response.json` unchanged (the `_benchmark` block records the method). Draw
prompts are byte-identical apart from the output filename. Deviations from
the parent plan, disclosed: the qwen row was run with
`run_benchmark.py cj` directly rather than through the `bench-runner`
agent, and the `BENCHMARK.md` section was written by the orchestrating
session rather than `bench-reporter`.

## Rows (first round, rubric v0.1) — 17

| Fixture | Condition | Draw 1 | Draw 2 | Must-no found | False alarms |
|---|---|---|---|---|---|
| page-titles-shared | cj | WARN | WARN | 3/3, 3/3 | 0, 0 |
| link-purpose-cards | cj | **FAIL** | **FAIL** | 7/7, 7/7 | **1, 1** (same row) |
| link-purpose-cards | baseline | FAIL | FAIL | 2/7, 2/7 | 0, 0 |
| images-role-routing | cj | WARN | WARN | 4/4, 4/4 | 0, 0 |
| images-role-routing | baseline | WARN | WARN | 4/4, 4/4 | 0, 0 |
| headings-fields-labels | cj | WARN | WARN | 5/5, 5/5 | 0, 0 |
| identification-across-views | cj | WARN | WARN | 2/2, 2/2 | 0, 0 |
| clean-control | cj | PASS | PASS | — | 0, 0 (after one invalid row, below) |
| link-purpose-cards | qwen3.6:35b, cj | FAIL | — | 1/7 | 0 |

Every WARN is R6 (a `no` rationale not carrying one of the blind author's
`loses` phrases — the check is uncalibrated by design) and, in three rows,
R5 spans. No inter-draw disagreement on any must row, so the pre-committed
third-draw trigger did not fire. Pre-committed reading of two draws: **no
false alarm observed in 2 draws** on five of six fixtures; one false alarm
observed in 2 of 2 draws on the sixth.

## Adjudications (read, not just counted)

1. **clean-control `TITLE-CO-a92da72862`** — judged `no` in both draws
   ("Home page announces 'Class Schedule'…"). The blind author attached the
   "site + page phrase" clean title to the home view, whose h1 is a welcome
   heading: the title misidentifies the page and the judges are right.
   Frozen-fixture rule applied: the row is **INVALID** (excluded and listed
   by the scorer; `sources/clean-control/overrides.yaml`), not edited, and
   not counted as a model miss. The clean control then reads PASS/PASS on
   its remaining 7 must rows.
2. **link-purpose-cards `LINK-LI-33337c9396`** — "Learn more" inside a
   sentence that names the maker space (H30 sufficient: same-paragraph
   context). Both draws: `no`, "seven identical 'Learn more' links are
   indistinguishable when a screen reader lists links". That is the
   rubric's card-grid rule, which reasons from 2.4.9 (Link Purpose, Link
   Only — AAA); at the skill's Level AA target, 2.4.4 accepts the sentence
   as programmatically determined context. The row stands as authored. The
   FAIL is real and is **attributable to the rubric**, not to the judge or
   the fixture.
3. **The five card-grid rows** the rubric arm finds (and bare opus misses)
   are F63 at 2.4.4 — each card's text is a sibling `<p>` inside a `<div>`
   with no heading, outside the link's programmatically determined
   context — so the rubric reaches the right verdict there for the AAA
   reason. A card whose link shared the paragraph would pass 2.4.4 while
   the rubric still said `no`. Same defect as (2), seen from the other
   side.
4. **Calibration-row mismatches** (never counted): the rubric arm marks
   two generic-ish incidental headings `no` on link-purpose-cards and one
   on images-role-routing; bare opus hedges the raw-URL and PDF-without-cue
   links to `unsure`. All are convention rows; recorded, not adjudicated.

## What the A/B shows

- **Link purpose in context (fixture 2):** the rubric carries the card-grid
  detection — bare opus finds 2/7 must-no rows and judges all five grid
  rows `yes`/`unsure`; the rubric arm finds 7/7. The same rule induces the
  one false alarm. Direction is draw-stable in both arms.
- **Image role routing (fixture 3):** bare opus already scores 4/4 with
  zero false alarms; the rubric adds nothing measurable for this tier.
- **The local detector** (qwen3.6:35b, rubric condition) judged every
  "Learn more" row `yes` — it does not follow the rubric's grid rule at
  all — with zero false alarms: consistent with the repo-wide routing rule
  (detector, never the `drafted_by` of record).

## Rubric rounds on link-purpose-cards (the fixture that gates)

| Rubric | Draws | Must-no found | False alarms | Discriminating rows | Reading |
|---|---|---|---|---|---|
| v0.1 (origin text: card grid `no` "because indistinguishable when listed") | 1, 2 | 7/7, 7/7 | **1, 1** (in-sentence "Learn more") | 2/2, 2/2 | detects the grid for the 2.4.9 reason and false-alarms a conforming link for the same reason |
| v0.2 (AA rule: `no` only when no programmatically determined context names the destination; AAA listing → ratifier note) | 3, 4 | 2/7, 2/7 | 0, 0 | 2/2, 1/1 | WCAG-correct but **undecidable from the row**: the flattened `context` carries the card text and cannot show it is a sibling block, so both draws passed the grid; draw 3 also emitted one malformed JSON line (C1) |
| v0.3 (same-sentence proxy: destination in the link's own sentence → `yes`; other-sentence context → `unsure`, needs_human, "context boundary not captured"; `no` only when nothing names it) | 5, WARN | 7/7 (5 deferred as `unsure`), 7/7 (5 deferred) | 0, 0 | 2/2, 2/2 | decidable from current rows: the grid goes to the human instead of to a silent `yes` or a WCAG-unsupported `no`; the in-sentence link stays `yes` |

The v0.2 → v0.3 step is the measured form of the skill critic's M2 second
half ("the capture makes it unfixable at the judge"): text alone cannot
apply the AA rule until the inventory reports the block relationship; the
proxy is the honest interim. The five grid rows carry `unsure_ok` for that
capture limit (same class as the six invalid td rows), expected `no`
unchanged. Baselines on identification-across-views (bare opus, 3 draws
after an inter-draw disagreement): "Resources"/"Help" found in 1 of 3 and
hedged to `unsure` in 2 of 3; the rubric arm found it in both draws — the
rubric carries the 3.2.4 different-names call. All rows: `score-claude-*.txt`.

## Gate reading (after the fold)

Rubric v0.3 on the gating fixture: must-clean on draw 5 (7/7 found with 5
deferred, 0 false alarms) and must-clean (7/7 (5 deferred) found, 0 false alarms). Every other fixture: must-clean in
both draws (v0.1 text unchanged for those classes; the v0.2/v0.3 edits touch
only link-context and file-cue rules). Per the pre-committed language: no
false alarm observed in 2 draws on any must row under v0.3 — which bounds
the per-row false-alarm rate only at roughly ≤ 15 % (95 %, non-independent
rows). The rubric fold is text-level; the capture changes it needs to
become fully decidable (preceding heading, list item, table row) and the
batch-line product/audience fields are the follow-up PR, after which the
lane re-draws with the six invalid rows made valid.

## Instrument revisions (pre-verdict, each with its trigger)

| Revision | Trigger | Effect |
|---|---|---|
| R5 quote regex: straight apostrophes inside words are not quote delimiters | first hosted draws fired R5 on "link's alt … user's" | four rows WARN → PASS/WARN-on-R6-only; smoke and calibration re-run CLEAN, all rows re-scored |
| D discriminating-row score; R4 "not armed" line; C3 fix-on-yes exempts file links; calibrate regression + split-group cases (43); smoke R7 case (64) | test-critic REVISE; rubric v0.3's file-cue rule | reporting only — no status moved except the file-link C3 line on v0.3 draws |
| Technique references: F84 → F63 on the card grid; ARIA14/H44 → G131-based labels; F89's own criteria annotated | live technique verification | reference labels only; no verdict or tier moved |

## Not claimed

Nothing about the second-reader pass, the spot-check sampler, the
ratification file formats, or 3.2.3 as a model task (deterministic by
design and asserted at the builder layer). Two draws detect instability;
they do not demonstrate stability. R4 is armed but cannot fire (no
list-form fabrication tokens exist for content rows); fabrication in these
rows was read, not counted.
