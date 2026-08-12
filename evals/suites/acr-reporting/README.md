# acr-reporting eval suite

Measures both directions of the ACR seam (integration plan
`docs/plans/2026-08-12-openacr-integration-plan.md`): **Lane A** (Phase 2)
— given a finished audit-scope evaluation, does the model serialize the
evidence spine into a schema-valid, catalog-complete, honestly-mapped
OpenACR draft without inventing a single value? — and **Lane B** (Phase 3)
— given someone else's OpenACR plus a completed verification engagement,
does it audit the claims into an honest claims-delta report (catching real
overstatements with evidence, confirming accurate claims including a
vendor's honest disclosed defect, and saying unverifiable where the scope
could not reach)? In both lanes the model tests nothing and decides
nothing new.

The skill **is** the instrument (prompt-only repo): the lane's system
prompt is `.claude/skills/acr-reporting/SKILL.md`, the same loading idea as
the evaluation-report lane (where the contract is the system prompt). The
fixture's task instruction stays minimal on purpose — every gate being
graded (outcome→term mapping, the untested gate, canonical note forms,
value provenance, the component and chapter policies, draft-only stance)
must come from the skill, not the task prompt.

Why this lane is raised-stakes: the output artifact is a conformance-claim
document a human may publish, and the Phase 0 spike proved the official
toolchain validates boilerplate — `openacr validate` accepts a 2-criterion
fragment and accepts `not-evaluated` on a Level A criterion. The skill's
gates are the only enforcement layer; this suite is where they are priced.

## Fixtures (6 — Lane A items 1/2/3/5; Lane B items 4/4b)

| # | Fixture | Catalog | Difficulty | What it tests |
|---|---|---|---|---|
| 1 | `transit-portal-q3-acr` | 2.5 / WCAG 2.2-508 | COMPLEX | Serialization chain fixture (the finished rcm-2026q3 evaluation, one step downstream of the evaluation-report suite's `transit-portal-q3`): full 56-SC mapping with all five terms exercised, component policy (native + PDF findings stay out of web entries), the 4.1.1 removed-criterion edge, value provenance incl. a withheld license |
| 2 | `permit-portal-acreditor` | 2.4 / WCAG 2.1-508 | ADVERSARIAL | Orthogonality trap both directions (CRITICAL trend:resolved on a passing SC tempts does-not-support; MINOR sitewide failure tempts supports) + the dual-catalog policy end to end (acreditor surface → 2.1 catalog, six measured 2.2-only outcomes ride the out-of-catalog annex, never dropped, never criteria rows) |
| 3 | `campus-events-untested` | 2.5 / WCAG 2.2-508 | ADVERSARIAL | The untested gate: 1.4.13 untested + 3.3.4 cantTell → INCOMPLETE draft (both omitted from chapters, marker + exact gap list opening the document notes, per-SC reasons in the handoff); `not-evaluated` or silent `supports` on either is a must-fail |
| 5 | `parks-registration-clean` | 2.5 / WCAG 2.2-508 | CLEAN | Complete-bundle false-positive control: all-passing evidence → complete draft with zero spurious gaps, zero INCOMPLETE machinery, zero a11y_* tokens (no findings exist), the evidenced AAA pass mapped supports, and the out-of-scope 2024 rumor left out |
| 4 | `shiftline-vendor-acr` | 2.5 / WCAG 2.2-508 | ADVERSARIAL | **Lane B claims audit**: vendor ACR with 3 overstated claims (supports on keyboard + sitewide-contrast failures; NA on uncaptioned videos), 2 understated (fixed defect still declared partial; illegal not-evaluated on AA), 1 unverifiable (commissioner-excluded SSO enclave), and 50 accurate claims — including the vendor's HONEST partially-supports on a still-failing focus indicator, which must come back confirmed (the FP trap). Foreign ACR: trend vocabulary forbidden |
| 4b | `courseware-vendor-acr-clean` | 2.5 / WCAG 2.2-508 | CLEAN | **Lane B clean control**: fully accurate vendor ACR (honest supports claims on real captioned media) + a verification that found nothing → all 56 claims confirmed, zero invented findings, zero hygiene flags, no vendor-hostile drift |

Every fixture is a **triplet**: `fixtures/<id>.md` (the engagement record +
finished evaluation report + finding blocks + catalog frame, sent to the
model verbatim), `fixtures/<id>.metadata.yaml` (machine-checkable
expectations, never sent), `rubrics/<id>.rubric.yaml` (dimension tiers and
adjudication notes, never sent).

The catalog frame (terms, AAA list, 508 chapter shape) is supplied in the
input, mirroring the bug-reporting federal fixture's in-input ID list: the
task is honest serialization against a supplied frame, never memory. The
A/AA criterion list arrives as the outcome map itself — the completeness
check "work from the catalog, not the findings list" stays honest because
findings exist only for failures.

## Conditions

- **acr** (default): `.claude/skills/acr-reporting/SKILL.md` as the system
  prompt.
- **acr-baseline**: identical fixture, no system prompt — measures what the
  skill carries. Baseline output files get the `-baseline-` infix and never
  count as skill-condition runs.

## Why there is no blind cut line here

Same reasoning as `bug-reporting` and `evaluation-report`: the fixture is
an **input**, not a component with planted bugs. The `.md` contains only
the bundle an agent would actually receive; every expectation lives in
`.metadata.yaml`/`.rubric.yaml`, which never enter a prompt. There is
nothing to strip; `strip_answer_key()` passes the file through unchanged.

## Scoring (`ollama/score_acr.py`, rule-based + routed CLI)

```
python3 ollama/score_acr.py <response.json> <fixture>.metadata.yaml
```

The scorer needs the pinned CLI once per machine (the `verify`-skill
reproduce-from-scratch pattern; the repo itself gains no package.json):

```
mkdir -p /tmp/acr-check && cd /tmp/acr-check && npm init -y && npm i @openacr/openacr@0.3.8
export OPENACR_CLI_DIR=/tmp/acr-check
```

Checks, all driven by metadata plus the pinned package's catalog file:

1. **Structural** — exactly one ACR-shaped YAML fence, parseable; `npx
   openacr validate` passes on the exact document (schema + catalog-member
   checks are the CLI's; everything after this line is what the CLI
   provably does not check).
2. **Catalog A/AA completeness** — every A/AA SC in the named catalog has a
   web adherence entry or (fixture 3) sits in the INCOMPLETE gap list.
   Ground truth is read from the installed catalog YAML, never hand-typed.
3. **Per-level term legality** — `not-evaluated` outside the AAA chapter is
   a must-fail even though the CLI validates it (spike-verified gap).
4. **Term mapping** — per-SC expected terms from the metadata (the mapping
   table is deterministic; severity never moves a term).
5. **Note forms + citations** — DNS/PS notes open with the sample-scoped
   stem, enumerate failing samples, and cite ≥1 correct `finding_id`
   (recomputed against the bundle, per `score_bugreport.py` discipline —
   the cited value is compared, never mere mention); supports notes carry
   the canonical stem with the fixture's exact sample counts and never
   cite a finding; forbidden ids (non-web evidence, resolved findings)
   must not appear inside criteria entries.
6. **Value provenance** — title/product.name/product.version/author.email/
   report_date compared exactly (structural YAML paths); a different
   well-formed value is a fabrication, not a miss; withheld fields
   (license where the record says "leave unset") must stay absent;
   last_modified_date, if present, must equal report_date; environment
   tokens absent from every input stream (JAWS/Dragon) are hard FAILs.
7. **INCOMPLETE protocol** — fixture 3: notes begin with the marker + the
   exact SC list, blocked SCs omitted from chapters, per-SC reasons in the
   handoff. Fixtures 1/2/5: the marker's presence is the spurious-gap
   false positive (must-fail).
8. **Annex** (fixture 2) — marker in document notes; all six measured
   2.2-only SCs accounted for in the response with the two failures
   carrying outcome + id; none of the six as YAML criteria rows.
9. **Chapter policy** — the four 508 chapters `disabled: true` with notes
   opening the canonical boundary stem; document notes state web-only
   method scope; AAA per the fixture's evidence map.

Status: **PASS** (all musts, no fabrication), **WARN** (musts pass,
should missed), **FAIL** (any must missed or fabrication detected).
Results always exit 0; the Status line is the machine signal.

## Lane B scoring (`ollama/score_acr.py`, `lane: b` metadata)

The Lane B deliverable is a Markdown claims-delta report, not an OpenACR
document — no CLI validation applies. Metadata-driven checks: per-SC
verdict extraction against the four-token vocabulary (table rows preferred;
mismatch-direction tokens scanned before `confirmed` so prose like
"confirmed the claim is overstated" resolves to the mismatch), claim
completeness, per-row citations, the illegal-claim hygiene flag,
unverifiable scope reasons, the foreign-ACR trend-vocabulary ban,
routing-to-bug-reporting, and the same fabrication frames as Lane A.
Lane B calibration is its own committed harness:
`evals/results/acr-reporting-phase3/calibrate.py` (5/5 CLEAN pre-rows).

## Instrument calibration (2026-08-12, pre-model-rows)

Committed and reproducible: `evals/results/acr-reporting-phase2/calibrate.py`
(exit 0 = CLEAN; `--dump` writes per-case scorer receipts). The honest
drafts are **derived from each fixture's metadata plus the installed
catalog** — metadata self-consistency is itself under calibration — and
every honest case is asserted to have exercised the real CLI
(`CLI validate: + Valid!` on both the 2.5/2.2 and 2.4/2.1 catalogs).

Nine cases, 9/9 CLEAN on the committed instrument:

| Case | Expected | Asserted lines |
|---|---|---|
| f1/f2/f3/f5-honest | PASS | CLI Valid! actually ran |
| f1-trap-taker | FAIL | all ten families individually: fabricated email, drafting-day date, invented license, invented finding_id, PDF id inside a web note (component policy), not-evaluated on Level A, dropped rows (completeness), severity-escalated 2.1.1 term, spurious INCOMPLETE marker, JAWS |
| f1-shoulds-missed | WARN | NA-stem + doc-version should lines |
| f2-orthogonality-taker | FAIL | 2.2.1 does-not-support term, forbidden resolved-id citation, 1.1.1 supports term, silent catalog upgrade, annex marker dropped, annex SC unaccounted |
| f3-gate-breaker | FAIL | not-evaluated outside AAA, blocked SCs carrying entries, missing marker |
| f5-flagger | FAIL | spurious marker, invented finding, paranoid 1.4.3 term, blanket AAA burying evidenced 2.4.8 |

Three adversarial probes (run alongside, documented not committed —
reproduce from this section):

- **Stem-after-context supports note** ("All images carry text
  alternatives. Sample-scoped: passes across …") → must-miss fires. This is
  the instrument's documented paraphrase limit working as designed —
  adjudicate by reading before counting the miss.
- **ASCII-hyphen INCOMPLETE marker** → still recognized (the marker regex
  accepts em-dash/en-dash/hyphen runs).
- **Unquoted YAML date** (`report_date: 2026-07-28`) → FAIL, and the
  failing check is the **CLI itself** ("data/report_date must be string") —
  a real authoring hazard, not an instrument artifact; the skill's
  validate-and-fix step exists exactly for it, and the scorer's own field
  comparison handles the typed date without cascading.

## Phase 2 gate (operational, from the integration plan)

Hosted tier passes fixtures 1, 2, 3, and 5, **stable across 2 independent
draws** (repo-documented variance: byte-identical prompts flip items;
single-draw gates pass by luck). "Recommended" means exactly: the
pending-caveat line is removed from SKILL.md and the CLAUDE.md skill row.
On fail: the plan's rollback table applies.

## First model rows + gate verdict (2026-08-12) — **GATE PASSED**

Eleven rows (opus subagents ×8 skill-condition + ×2 baseline, one
qwen3.6:35b detector row), full adjudications and the instrument-revision
log in [`evals/results/acr-reporting-phase2/`](../../results/acr-reporting-phase2/):

| Fixture | opus draw 1 | opus draw 2 |
|---|---|---|
| transit-portal-q3-acr | **PASS** | **PASS** |
| permit-portal-acreditor | **PASS** | **PASS** |
| campus-events-untested | **WARN** (1 should-tier token miss, adjudicated a false miss — content present) | **PASS** |
| parks-registration-clean | **PASS** | **PASS** |
| f1 baseline (A/B) | FAIL (20 must) | FAIL (19 must) |
| f1 qwen3.6:35b (detector) | FAIL (unparseable YAML) | — |

**Eight of eight skill rows: zero must-tier misses, zero fabrications,
across all four fixtures and both draws** — both traps held, the FP
control stayed clean, and every metadata value traced. The A/B direction
is draw-stable and characterizes what the skill carries precisely: both
baselines had **zero term-mapping misses and zero fabrications** (bare
opus judges correctly) but missed the machine contract everywhere —
schema exactness (CLI-invalid `version` string; an invented
`release_date` field), the component policy, all canonical note stems,
boundary stems, and methods/disclaimer phrasing. The local detector row
FAILed at the structural gate (canonical stems emitted as unquoted plain
scalars — the colon breaks the YAML; values in the raw text were correct),
reinforcing the mandatory hosted/human value-and-validate pass on any
local draft.

**Lane B rows (Phase 3, same day)** — full adjudications and the
instrument-revision log in
[`evals/results/acr-reporting-phase3/`](../../results/acr-reporting-phase3/):
skill condition **4/4 PASS at every tier** (f4 + f4b × 2 draws — all six
planted deltas verdicted exactly, the honest-vendor FP trap held, zero
trend vocabulary); baselines FAIL draw-stably on vocabulary/format carry
with sound judgment underneath (each invented its own disposition
taxonomy; zero fabrications); qwen3.6:35b **WARN with 56/56 correct
verdicts** — Lane B's Markdown deliverable sidesteps the local tier's
machine-format weakness that failed its Lane A row. Lane B calibration is
its own committed harness (6/6 CLEAN, incl. the quote-the-rule
trend-scan probe).

Gate-row byproducts, independently reproduced and folded back into the
skill + reference doc: `validate`/`output` both require `-c` (bare
`validate -f` accepts nonexistent criteria; bare `output` silently renders
a criteria-less shell), and an absent `license` renders as CC-BY-4.0 by
the schema's own default. The plan's re-verification checklist also
closed: a full-size 2.1-catalog gate draft imported into acreditor
(78/312 progress, disabled chapters dropped, notes populated into the
editor's controls) and a 2.2 gate draft rendered to full HTML via the CLI.

## Running the lane (local detector rows)

```
# skill condition (the lane)
python3 ollama/run_benchmark.py acr qwen3.6:35b transit-portal-q3-acr

# baseline condition (what does the skill carry?)
python3 ollama/run_benchmark.py acr-baseline qwen3.6:35b transit-portal-q3-acr

# score
python3 ollama/score_acr.py /tmp/ollama-acr-transit-portal-q3-acr-<model-tag>-response.json \
  evals/suites/acr-reporting/fixtures/transit-portal-q3-acr.metadata.yaml
```

Model routing (unchanged from the plan): ACR generation runs on the hosted
tier; local models are detectors, and any locally-produced draft requires a
field-by-field value-check pass by a hosted-tier model or the human before
validation counts for anything.

## Known instrument limits

- Canonical-stem checks are anchored regexes; models that lead notes with
  context before the stem undercount — adjudicate misses by reading before
  counting them (wcag-em-phase3 practice).
- Line-scoped token checks (annex accounting, handoff reasons) undercount
  paraphrase.
- The CLI validates schema shape and catalog membership only — every
  honesty property above is scorer-side by design; a `Valid!` line alone
  means almost nothing.
- Scorer statuses are detector output, not verdict authority — the
  repo-wide local-model routing rule applies unchanged.

## Out of scope (deliberate)

Lane B claims verification (fixtures 4/4b — Phase 3, adjudicated by
a11y-critic), Lane C drift diffs (Phase 4), acreditor UI automation (the
editor is a human finish surface; import re-verification is a release-watch
item, not a per-run eval step), and EN 301 549 non-WCAG clause mapping
(explicitly out of the promised surface).
