# a11y-content-judgment eval suite

Measures the **judge step** of the `a11y-content-judgment` skill — the only
model-facing step of its four-step pipeline (inventory → build rows → judge →
merge/ratify). Given the rows the skill's own deterministic pipeline emits
for a set of pages, does a model mark the planted defective rows `no`, leave
the planted clean rows alone (the false-alarm half — must-tier), write
rationales that name what the person loses without asserting facts absent
from the row, and hold identical constructs to one verdict?

The lane exists because the skill was promoted from one engagement run with
the bar's fixture-before-skill-text order violated (dispositions v3
addendum, 2026-09-02). The remedy is blindness: a subagent that never read
the skill wrote the fixtures from W3C technique text, and every planted
class cites the technique it reproduces (`clause1_evidence`). Rows without
a public reference — borderline naming variants, the rubric's own
conventions (file-format cues, readable-domain URLs, repeated-construct
handling), audience shorthand, long formal names, and every unplanted
incidental element — are **calibration tier**: reported by the scorer,
never counted toward status.

## What the judge receives, and what the fixture is

Fixtures are **HTML sources run through the real pipeline**. Each
`sources/<id>/` holds a small fictional site (2–6 views, `.example`
origins), the blind author's `scenario.md` (product + audience — the batch
line carries neither, and the rubric's audience-shorthand rule needs both),
`views.txt`, `expectations.yaml` (the author's per-element verdicts,
references, and evidence phrases), and the maintainer's `overrides.yaml`.
`build-fixtures.sh` serves the site on a fixed origin (unit ids hash
host:port), runs `content-inventory.mjs` + `build-judgment-rows.mjs`,
rewrites the origin to the fictional domain, and `assemble_fixture.py`
writes `fixtures/<id>.md` = scenario + the output contract + the rows.
`map_expectations.py` is the one non-blind step: a **lookup** from each
author locator to an emitted unit id, receipted in
`sources/<id>/build/mapping.log`.

Freeze guards, asserted on every build: row counts per type; the builder's
own exclusions (pseudo-hrefs and paired ID/name columns emit no 3.2.4 row;
3.2.3 nav order per view); `evidence_contains` / `evidence_absent` per
planted row (the row must carry, in its own fields, what its verdict
needs); emitted id-set == metadata id-set.

## Fixtures (6)

| # | Fixture | Rows | Must no / yes | Planted defective (failure side) | Planted clean (sufficient side) | Calibration / invalid |
|---|---|---|---|---|---|---|
| 1 | `page-titles-shared` | 37 | 3 / 2 | bare site name shared by three views (F25) | site + page phrase; record page "ID — name — site" (G88) | long formal title; 31 incidental |
| 2 | `link-purpose-cards` | 43 | 7 / 3 | five card-grid "Learn more" whose card text is a sibling `<p>` outside the link's programmatically determined context (F63); one "Learn more" whose disambiguating text is elsewhere on the page (F63); icon-only link whose alt names the icon (F89) | "Learn more" inside a sentence naming the destination (H30); icon link named by `aria-label` (ARIA8); "Annual report (PDF, 2 MB)" (H30) | raw-URL text and a PDF link without a format cue (rubric conventions); **6 ID-column links INVALID** (capture limit, below); an image twin of the F89 link |
| 3 | `images-role-routing` | 23 | 4 / 3 | alt is a filename (F30); `alt="gauge"` on a data image (F30); no alt attribute (F65); linked image with `alt=""` as the link's only content (F89) | `alt=""` beside a text label (H67); informative alt carrying the reading (G94); chart with short alt + figcaption (G95, `unsure_ok`) | link-row twin of the F89 image |
| 4 | `headings-fields-labels` | 19 | 5 / 3 | placeholder-only field (G131/H44 absent); "Overview", "Details", an empty `<h2>`, a numeric-only heading (G130 failure side) | wrapping `<label>` (G131 + H44); `aria-label`led search field (G131 via ARIA14) | invented specialist shorthand label; long formal heading |
| 5 | `identification-across-views` | 53 | 2 / 1 | "Resources"/"Help" and "v2.5"/"Release notes" naming one destination (G197 / Understanding 3.2.4) | logo "… home" + text "Home" → `/` (G197) | "Contact"/"Contact us" (borderline); **deterministic:** no 3.2.4 row for the paired ID/name trail columns or the `javascript:` zoom controls; sub-nav on the detail page is not an order finding |
| 6 | `clean-control` | 25 | 0 / 7 | none — any `no` on a must row is a false alarm | descriptive titles/headings, labelled fields, in-sentence link (H30), correct alts (G94/H67), consistent identification (G197), same nav order (G61) | long formal title/heading, shorthand, a PDF link without a format cue |

Totals: 39 must rows (21 no / 18 yes — all clause-1 evidence), 156
calibration rows (144 of them incidental unplanted elements), 7 invalid
(6 for the table-cell capture limit, 1 blind-author error found by draw output — the
home view titled for a different page).

**Invalid rows** (`invalid: true`, excluded from every check, listed by the
scorer): the inventory's link context is the nearest text block, which for
`<td><a>DL-1002</a></td>` is the cell itself, so the record name in the
sibling cell never reaches the row and the rubric's paired-column rule is
undecidable from what the judge sees. That is a skill capture limit, filed
for the critic pass — never a model miss, never a silent fixture edit.

**Live technique verification** (receipt in
`evals/results/content-judgment-2026-09/technique-verification.md`)
corrected three reference labels before any draw: the card grid is F63, not
F84 (F84 is the 2.4.9 Link-Only failure); ARIA14 is a 4.1.2 naming
technique (descriptiveness is G131); F89's own criteria are 2.4.4/2.4.9/
4.1.2 although the skill files the image row under 1.1.1.

## Conditions

- **cj** (default): `references/judgment-rubric.md` as the system prompt —
  the only file the judge step reads in the skill's own pipeline
  (`SKILL.md` is the orchestrator's protocol; `judge-prompt.md` is subagent
  plumbing).
- **cj-baseline**: identical fixture, no system prompt. The output contract
  (keys, one line per row, the fence) lives in the fixture's task line so the
  baseline is scorable at all; what the rubric carries — in-context judging,
  functional/decorative/informative routing, "length alone is never a no",
  audience shorthand, never inventing destination content, one verdict per
  construct — is what the A/B prices. Baselines run on fixtures 2 and 5
  (flag polarity on both sides of each) and the A/B is **reported over
  discriminating rows only**; fixture 3's baseline rows exist (first
  round) but its clean side is entirely unflagged, and the clean control is
  degenerate (all-`yes` passes it) — neither is A/B evidence.

## Scoring (`ollama/score_content_judgment.py`, rule-based)

```
python3 ollama/score_content_judgment.py <response.json> <fixture>.metadata.yaml
```

Checks are labelled by what prices them:

| Check | Tier | Priced by | What it grades |
|---|---|---|---|
| C1 | must | contract | exactly one line per input id; no extras |
| C2 | must | contract | `judgment` ∈ {yes,no,unsure}; `drafted_by` present |
| C3 | should | contract | confidence enum; `needs_human` on unsure; empty `fix` on yes; ≤ 25 words |
| R1 | must | rubric | every expected-`no` must row judged `no` (`unsure` only where `unsure_ok`) |
| R2 | must | rubric | no expected-`yes` must row judged `no`; `unsure` there = should-tier over-hedge |
| R3 | info | rubric | calibration rows reported, never counted |
| R4 | must | rubric | metadata `fabricated_tokens` in a rationale/fix — **empty on every fixture**: no credible list-form invention class exists for content rows (the ACR lane's environment-token analogue has no counterpart), so R4 is armed but cannot fire; fabrication is read, not counted |
| R5 | should | rubric | a quoted span ≥ 3 words absent from the row and the line's own `fix` — should-tier by calibration on the origin run (recall 2/6, 8.5 % false-fire on second-reader-agreed rationales; receipt `r5-quoted-span-calibration.md`) |
| R6 | should | rubric | a `no` rationale names ≥ 1 of the row's blind-authored `loses` phrases (uncalibrated WARN rate) |
| R7 | should | rubric | every `pattern_group` unanimous |
| D | info | rubric | **discriminating rows** — must rows whose heuristic flags are absent or point the wrong way (an expected-`no` with no flag, an expected-`yes` with a flag). On this fixture set every planted defect carries a flag and 14 of 19 clean must rows carry none, so R1 is solvable by "trust the flag" in either arm; D is the headline judgment signal (test-critic finding 1). Unflagged defective rows are a follow-up fixture item. |

Status: **PASS** (all musts, no fabrication), **WARN** (musts pass, should
missed), **FAIL** (any must miss or fabrication), **INCOMPLETE** (truncated
or unparseable). Exit 0 always. R4 prints "not armed" when a fixture lists
no tokens (all six do).

## Instrument calibration (2026-09-02, pre-model-rows)

`evals/results/content-judgment-2026-09/calibrate.py` (exit 0 = CLEAN;
`--dump` writes `score-cal-*.txt`): per fixture, synthetic responses derived
from the frozen metadata — honest → PASS, hedger → WARN, flagger → FAIL,
blind → FAIL, silent → FAIL, inventor → WARN, regression (no `loses`
phrase) → WARN, split-group → R7 fires — **43/43 CLEAN**. What CLEAN
certifies: C1/C2/R1/R2/R5/R6/R7 wiring and metadata self-consistency; it
does not exercise R4 (no fixture lists tokens; the smoke case covers it) or
the C3 word cap. Scorer smoke (`evals/suites/smoke/cj-*`, asserted in
`scripts/smoke_scorers.sh`): gold PASS, seven must-family mutations FAIL
naming the line, three should-family WARN (over-hedge, loses, split group),
truncation INCOMPLETE.

## Rebuilding from sources

```
mkdir -p /tmp/cj-pw && cd /tmp/cj-pw && npm init -y && npm i playwright@1.57.0 && npx playwright install chromium
PW_DIR=/tmp/cj-pw bash evals/suites/a11y-content-judgment/build-fixtures.sh          # all fixtures; exit 1 on any freeze-guard mismatch
python3 evals/suites/a11y-content-judgment/map_expectations.py <fixture-id>          # only when expectations/overrides change
```

Playwright is a scratch install, never a repo dependency. A fixture changes
only on a demonstrated authoring error recorded in `mapping.log`; a
demonstrated row-evidence defect after the freeze makes the row invalid.

## Running the lane (local detector rows)

```
python3 ollama/run_benchmark.py cj qwen3.6:35b link-purpose-cards
python3 ollama/run_benchmark.py cj-baseline qwen3.6:35b link-purpose-cards
python3 ollama/score_content_judgment.py /tmp/ollama-cj-link-purpose-cards-<tag>-response.json \
  evals/suites/a11y-content-judgment/fixtures/link-purpose-cards.metadata.yaml
```

Routing (unchanged from the skill): judgment on the hosted tier; a local
model is a detector that pre-sorts, never the `drafted_by` of record.

## Known instrument limits

- R6 `loses` phrases were written by someone who never read the rubric;
  read a WARN before counting it.
- R5 is a paraphrase-blind substring heuristic; 8.5 % of honest rationales
  quote something the row does not literally contain.
- Two draws detect instability; they never demonstrate stability. Any
  inter-draw disagreement on a must row triggers a third draw. With 19
  clean must rows in 3 pattern groups (effective N ≈ 25 over all 40) and
  rows within a fixture sharing one draw, "0 false alarms in 2 draws"
  bounds the per-row false-alarm rate only at roughly ≤ 15 % (95 %), and
  that assumes an independence the rows do not have.
- Maintainer overrides moved 3 author-listed rows to calibration tier
  (rubric conventions: two PDF links without a format cue, one raw-URL
  text) and gave 2 incidental twins of planted F89 elements the planted
  verdict; overrides can neither promote a row to must nor change the
  blind author's expected verdict (refused and logged).
- Scorer statuses are detector output, not verdict authority.

## Out of scope (deliberate)

The second-reader pass (same rubric, downstream), the spot-check sampler,
ratification and receipt discipline (file-format contracts reviewed as code
by `test-critic`, no model row), and 3.2.3 as a model task (deterministic by
design; asserted at the builder layer).
