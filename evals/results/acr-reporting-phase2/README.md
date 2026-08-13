# acr-reporting Phase 2 — calibration, gate rows, and gate verdict (2026-08-12)

Phase 2 of the OpenACR integration plan
([docs/plans/2026-08-12-openacr-integration-plan.md](../../../docs/plans/2026-08-12-openacr-integration-plan.md)):
instrument calibration, the hosted gate rows, the A/B baseline rows, and one
local detector row for the `acr-reporting` eval lane
([evals/suites/acr-reporting/](../../suites/acr-reporting/)).

## Instrument calibration (before any model row)

`calibrate.py` (committed; exit 0 = CLEAN; `--dump` writes the
`score-cal-*.txt` receipts): nine synthetic cases — four honest drafts
derived from each fixture's metadata plus the installed catalog (metadata
self-consistency is itself under calibration, and every honest case asserts
the real CLI ran: `CLI validate: + Valid!`), plus five mutants covering
every trap family. **9/9 CLEAN**, re-run CLEAN after each instrument
revision below. Three adversarial probes (stem-after-context supports note
→ documented paraphrase miss fires; ASCII-hyphen INCOMPLETE marker → still
recognized; unquoted YAML date → the CLI itself rejects it) are documented
in the suite README.

## Instrument revisions (all pre-verdict, each with its trigger)

| Revision | Trigger | Effect on statuses |
|---|---|---|
| Fixtures: `3.3.9 Accessible Authentication (Enhanced)` added to the three 2.2-catalog fixtures' AAA enumerations (they said "31 criteria" and listed 30) | **Caught by a baseline row mid-run** — opus flagged the count/list mismatch and reconciled from the catalog | None — AAA enumeration is not a scored dimension; all rows ran against the v1 text and every draw either reconciled to 31 from the catalog or serialized the 30 given, both explicitly disclosed in their handoffs |
| Scorer: withheld-field check fires only on non-empty values | baseline draw 2 emitted `license: ''` — an empty field is not an invented value | None (would have been one false fabrication on a baseline row) |
| Scorer: structural `web_only_components` check + forbidden-id scan across ALL components | the baseline rows populated `electronic-docs`/`software` components — invisible to the web-scoped checks, i.e. a real component-policy hole | Baselines gain the component-policy must-miss; all skill rows unaffected (0 non-web entries) |
| Scorer: `openacr validate` now passes `-c <catalog>` | **gate-row discovery, reproduced**: bare `validate -f` does not load the document's own `catalog:` field — criterion `9.9.9` validates without `-c` | None — all 11 rows re-scored under the hardened instrument with **identical statuses**; the scorer's own catalog-derived completeness check had covered membership all along |

## Method (hosted rows)

`Agent(subagent_type=general-purpose, model=opus)`, one subagent per draw,
byte-identical prompts across draws. Skill condition: the subagent reads
`.claude/skills/acr-reporting/SKILL.md` (at `9168457`, the Phase 1 commit)
as its protocol; baseline condition: all repo reads forbidden, no skill.
Fixtures staged alone in a scratch directory (metadata/rubrics not staged;
`evals/` read-barred). A pinned `@openacr/openacr@0.3.8` scratch install
was offered for the skill's optional self-validate step (most skill-row
agents used it; that is the skill's own step 7, not contamination — the
scorer validates independently). No repo writes; the final message is
extracted verbatim from the subagent transcript. Full per-row disclosure in
each response file's `_benchmark`.

## Rows (11) — scored with the final instrument

| Row | Condition | Draw | Status | Must / Fab / Should |
|---|---|---|---|---|
| opus f1 `transit-portal-q3-acr` | acr | 1 | **PASS** | 0 / 0 / 0 |
| opus f1 `transit-portal-q3-acr` | acr | 2 | **PASS** | 0 / 0 / 0 |
| opus f2 `permit-portal-acreditor` | acr | 1 | **PASS** | 0 / 0 / 0 |
| opus f2 `permit-portal-acreditor` | acr | 2 | **PASS** | 0 / 0 / 0 |
| opus f3 `campus-events-untested` | acr | 1 | **WARN** | 0 / 0 / 1 (adjudicated below) |
| opus f3 `campus-events-untested` | acr | 2 | **PASS** | 0 / 0 / 0 |
| opus f5 `parks-registration-clean` | acr | 1 | **PASS** | 0 / 0 / 0 |
| opus f5 `parks-registration-clean` | acr | 2 | **PASS** | 0 / 0 / 0 |
| opus f1 baseline | acr-baseline | 1 | **FAIL** | 20 / 0 / 6 |
| opus f1 baseline | acr-baseline | 2 | **FAIL** | 19 / 0 / 6 |
| qwen3.6:35b f1 (local detector) | acr | 1 | **FAIL** | 21 / 0 / 9 |

## Gate verdict: **PASSED**

The plan's Phase 2 gate — hosted tier passes fixtures 1, 2, 3, and 5,
stable across 2 independent draws — is met: **eight of eight skill-condition
rows carry zero must-tier misses and zero fabrications**, across all four
fixtures and both draws. Seven rows are PASS; the eighth (f3 draw 1) is
WARN on exactly one should-tier item, adjudicated a **false miss by
reading** (the wcag-em-phase3 practice): the handoff's commissioning group
looks for tokens like "commission"/"further testing", and the draw carries
the content as a per-SC "What closes it" table ("a driven session over the
views carrying tooltips…", "a test environment that permits completing a
payment…") plus the literal sentence "Commission the missing testing before
this draft is completed, signed, or published" **inside the document
notes** — which the handoff check excludes by construction. Content-
adjudicated ≈ 8/8 PASS at every tier. Stated strictly: even counting the
un-adjudicated WARN, no must-tier property flipped in any draw — the gate's
honesty dimensions (mapping, untested gate, FP control, value provenance)
are 8/8 clean and draw-stable.

Per-fixture adjudication highlights (every row was read):

- **f1 (serialization, both draws):** 56/56 completeness and 56/56 term
  mapping; the non-web findings never entered criteria entries (draw 1's
  software-chapter boundary note carries the native finding as evidence
  prose — policy-conformant: disabled-chapter notes are exactly where
  boundary statements live); 4.1.1 handled as not-applicable with the
  removal note; 2.5.7 held to the panel decision with the defect counted
  once under 2.1.1. Both draws flagged the fixture's AAA count/list
  mismatch in their handoffs.
- **f2 (orthogonality + dual catalog, both draws):** both trap arms held —
  2.2.1 stayed `supports` with the resolved CRITICAL in prose only (no id
  in its note), 1.1.1 went `does-not-support` on the MINOR sitewide
  failure with all-samples scope; the catalog stayed 2.4-edition against
  the target-is-2.2 pull; all six annex SCs accounted with the two
  failures carrying ids. Draw 1's handoff even pre-argues the "1.1.1 will
  be misread" proportion-claim tension — the exact semantic caution the
  plan's mapping table documents.
- **f3 (untested gate, both draws):** both shipped INCOMPLETE under the
  commissioner's ship-it-now pressure — marker + exact gap list opening
  the notes, 1.4.13/3.3.4 absent from chapters, per-SC reasons carried;
  no `not-evaluated` leaked into A/AA. Draw 1 prefixed one line of
  self-check narration before the YAML fence (minor protocol deviation,
  harmless to scoring).
- **f5 (FP control, both draws):** complete drafts, zero a11y_* tokens,
  no INCOMPLETE machinery, the 2024 prior-platform rumor kept out with
  the reasoning addressed to the program director in the handoff, and the
  evidenced AAA pass (2.4.8) mapped `supports` against the blanket
  not-evaluated pull.

## A/B condition (what the skill carries) — draw-stable

Both baseline draws FAIL with near-identical miss lists (20 vs 19) and —
the sharp result — **zero fabrications and zero term-mapping misses in
both**. Bare opus gets the judgment right: orthogonality held (CRITICAL
slider finding stayed `partially-supports`), 1.3.5 correctly escalated to
`does-not-support` with written reasoning, values were never invented
(absent fields left blank and flagged). What only the skill carries is the
**machine contract**, missed by both draws: schema exactness (`version` as
a string → the CLI rejects both drafts; draw 2 invented the field name
`release_date`, losing `report_date`), the component policy (both
populated `electronic-docs`/`software` entries and cited non-web ids
inside criteria), every canonical note form (40 supports stems + 7 DNS/PS
stems off), the disabled-chapter boundary stems, and the
methods/disclaimer phrasing. Routing consequence, mirroring the
evaluation-report lane: the skill is not teaching opus accessibility
judgment — it is the difference between a thoughtful report and a
machine-valid, convention-conformant ACR another tool (or Lane C diff) can
consume.

## Local detector row (plan-required)

qwen3.6:35b, fixture 1, skill condition (119s Metal): **FAIL — the YAML
does not parse**. The draft wrote canonical note stems as unquoted plain
scalars (`notes: Sample-scoped: passes across…`), and the colon inside the
value is a YAML mapping error; the CLI rejects it identically. The
documented data-fidelity class surfaced as artifact-integrity failure —
inverse of the expected structure-pass/value-flags split (the values in
the raw text are actually correct: title, email, date all match; zero
fabrications). Same routing conclusion, stronger: a local draft is not
machine-valid output — the mandatory hosted/human value-and-validate pass
stands.

## Toolchain discoveries (agent-reported, independently reproduced)

1. **`openacr validate` without `-c` is schema-shape only.** It does not
   load the document's own `catalog:` field: criterion `9.9.9` → `Valid!`;
   with `-c` → correctly Invalid. This falsifies the Phase 0 reference
   line "criterion numbers exist in the named catalog is CLI-checked" —
   true only with `-c`. Scorer hardened; reference doc corrected.
2. **`openacr output` without `-c` silently renders an empty shell** —
   exit success, 14 KB metadata-only page with zero criteria tables
   (120 KB with `-c`), reproduced on the package's own `drupal-10-16.yaml`.
3. **Absent `license` is not neutral**: the schema states "If none is
   provided 'CC-BY-4.0' is assumed default in any output" (verified
   verbatim), and rendered HTML asserts it. The skill's handoff now warns.

## Success-criteria re-verifications (plan checklist items 3 and 4)

- **acreditor import, full-size draft** (criterion 3): the f2 draw-1 gate
  draft (27 KB, 78 entries, 2.4-edition catalog) imported via "Open
  report" at acreditor.section508.gov on 2026-08-12 — validation alert
  named the product, progress read "Reported on 78 of 312 Total Criteria"
  (30 A + 20 AA + 28 AAA — exactly the draft's web entries), the four
  `disabled:` chapters dropped from the progress sidebar, and the imported
  values populated the editor's own controls (1.1.1 level select =
  `does-not-support`; chapter-notes and criterion-notes textareas carry
  the imported text verbatim).
- **CLI HTML render, 2.2 draft** (criterion 4): the f1 draw-1 gate draft →
  `Valid!` → 123 KB HTML with all criteria tables, rendered with `-c`.

## Reproduce

```
mkdir -p /tmp/acr-check && cd /tmp/acr-check && npm init -y && npm i @openacr/openacr@0.3.8
export OPENACR_CLI_DIR=/tmp/acr-check
python3 evals/results/acr-reporting-phase2/calibrate.py            # exit 0 = CLEAN
python3 ollama/score_acr.py \
  evals/results/acr-reporting-phase2/claude-acr-transit-portal-q3-acr-opus-response.json \
  evals/suites/acr-reporting/fixtures/transit-portal-q3-acr.metadata.yaml
```

Scorer statuses are detector output; every verdict above was made by
reading the row. Open for later phases: sonnet/Codex/Gemini tier rows,
local acr-baseline rows, and Lane B fixtures 4/4b (Phase 3).
