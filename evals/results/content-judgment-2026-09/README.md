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
| `calibrate.py`, `score-cal-*.txt` | 35 synthetic cases derived from the frozen metadata, all CLEAN before the first model row |
| `claude-cj-*-response.json`, `score-claude-cj-*.txt` | 12 rubric-condition opus draws (6 fixtures × 2) and 4 baselines (fixtures 2, 3 × 2), packaged verbatim |
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

## Rows (17) — final instrument

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

## Gate reading

The lane's own bar for "clause 1 satisfied for the classes with a public
reference": hosted tier must-clean on all fixtures, stable across 2 draws.
**Not met as the rubric stands** — one draw-stable false alarm, on a row
whose verdict WCAG 2.4.4 settles the other way. This is a rubric REVISE
item (filed with the `a11y-critic` pass), not a fixture or scorer item;
the rows the rubric gets right are the clause-1 evidence for the classes
they cover (F25, F30, F65, F89, F63, G130/G131 absence, G197). Nothing
here changes the skill's routing: drafts remain detector output behind a
mandatory human ratification.

## Instrument revisions (pre-verdict, each with its trigger)

| Revision | Trigger | Effect |
|---|---|---|
| R5 quote regex: straight apostrophes inside words are not quote delimiters | first hosted draws fired R5 on "link's alt … user's" | four rows WARN → PASS/WARN-on-R6-only; smoke 63/63 and calibration 35/35 re-run CLEAN, all rows re-scored |
| Technique references: F84 → F63 on the card grid; ARIA14/H44 → G131-based labels; F89's own criteria annotated | live technique verification | reference labels only; no verdict or tier moved |

## Not claimed

Nothing about the second-reader pass, the spot-check sampler, the
ratification file formats, or 3.2.3 as a model task (deterministic by
design and asserted at the builder layer). Two draws detect instability;
they do not demonstrate stability. R4 is armed but cannot fire (no
list-form fabrication tokens exist for content rows); fabrication in these
rows was read, not counted.
