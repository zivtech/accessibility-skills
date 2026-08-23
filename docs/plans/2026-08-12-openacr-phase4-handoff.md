# OpenACR Phase 4 handoff — Lane C + upstream filing

> Written 2026-08-12 at the close of Phase 3 (Lane B). Parent plan:
> [2026-08-12-openacr-integration-plan.md](2026-08-12-openacr-integration-plan.md).
> Everything here is executable without this session's context; receipts
> live in `docs/openacr-reference.md` and `evals/results/acr-reporting-phase{2,3}/`.

## Part 1 — Lane C (ACR drift: YAML N vs YAML N+1) — **EXECUTED 2026-08-13**

All five items below are done; receipts in
[`evals/results/acr-reporting-phase4/`](../../evals/results/acr-reporting-phase4/)
and the suite README. Summary: protocol + Codex mirror landed
(`check_mirrors.py` clean), fixtures 6/6b built as triplets and verified
de-hinted (zero trend vocabulary in either input), `lane: c` scorer
calibrated **10/10** before any row — catching four instrument defects,
two of which had made checks silently unfailable — and seven rows scored
and adjudicated by reading: **opus 4/4 must-clean** across both fixtures
and both draws, baselines FAIL draw-stably on vocabulary carry with the
judgment intact, qwen3.6:35b PASS with three unscored prose errors. Two
revisions were folded back and disclosed (one should-tier instrument
repair; one skill amendment for the self-pair routing rule). Item 5's
wiring is complete except the remaining open work listed in Part 3.

The original scope, retained as the executed record:

1. **SKILL.md Lane C section** (+ Codex mirror; run `scripts/check_mirrors.py`):
   diff two OpenACR documents at SC/component level; express results in the
   report contract's re-evaluation vocabulary — outcome deltas at the SC
   level (criteria newly passing/failing since the prior document), and
   finding-level trend (`new`/`persistent`/`worsening`/`improving`/
   `resolved`) **only when the subject pair is self-produced and carries our
   fingerprints in the notes** (the Lane A note forms embed
   `finding_id`+fingerprint precisely to enable this). Foreign pairs:
   term-level deltas only — same boundary Lane B already enforces, now for
   pairs. Never narrate a delta as a whole-product improvement claim;
   sample scopes of the two documents may differ and the narration must say
   whether they are comparable (the WCAG-EM re-evaluation guidance the
   report contract cites: keep a comparable sub-set, replace a sub-set).
2. **Fixtures** (suite pattern is established — triplets, minimal task
   instruction, skill-as-system-prompt vs bare A/B):
   - Fixture 6 `<product>-acr-drift-self`: a self-produced pair (cycle 1 +
     cycle 2 drafts with overlapping fingerprints) → expected finding-level
     trend rows (one resolved, one persistent, one new, one worsening) +
     SC-level deltas; trap: an SC whose term changed while its finding
     fingerprint persists (worsening vs resolved discrimination).
   - Fixture 6b `<product>-acr-drift-foreign`: a foreign pair (two vendor
     ACR versions, no fingerprints) → term-level deltas only; any trend
     vocabulary is the must-fail; FP arm: rows whose terms did not change
     must be reported unchanged, not dramatized.
3. **Scorer**: `lane: c` path in `ollama/score_acr.py` (the lane-b branch
   shows the shape: no CLI, metadata-driven row checks). Calibrate in
   `evals/results/acr-reporting-phase4/calibrate.py` before any row (the
   phase-3 harness is the template — honest report derived from metadata).
4. **Rows**: opus ×2 draws × both fixtures + baseline ×2 on fixture 6 +
   one qwen3.6:35b detector row. Adjudicate every row by reading; statuses
   are detector output.
5. **Wiring on clean rows**: suite README fixtures table + rows section;
   CLAUDE.md acr-reporting prose sentence (Lane C landed); plan doc Phase 4
   status; SKILL Boundaries list (drop Lane C from "not yet"; the merge-
   into-hand-maintained-ACR exclusion stays permanently).

## Part 2 — Upstream filing (GSA repos) — **EXECUTED 2026-08-13 (user-approved)**

Filed after searching both repos' open AND closed issues (no duplicates;
adjacent history: #352, #246, openacr-editor#83; the editor repo routes
issues to the main repo per openacr-editor#43). All five landed on
`GSA/openacr` with fresh reproduction transcripts:
A → [#363](https://github.com/GSA/openacr/issues/363) ·
B → [#364](https://github.com/GSA/openacr/issues/364) ·
E → [#365](https://github.com/GSA/openacr/issues/365) ·
C → [#366](https://github.com/GSA/openacr/issues/366) ·
D → [#367](https://github.com/GSA/openacr/issues/367).
URLs + the KAT-style watch rule are in `docs/openacr-reference.md`
§Upstream. The drafts below are retained as the filed record.

**Requires explicit user approval before posting — filing issues on
external repos is outward-facing publication.** Search each repo's open
AND closed issues first (KAT #27 precedent: file once, cite precisely,
watch the pin). Candidates, strongest first, with ready-to-adapt drafts —
all four behaviors verified against `@openacr/openacr@0.3.8` on 2026-08-12
(receipts: `docs/openacr-reference.md` §CLI; reproduction one-liners
below):

### Issue A — GSA/openacr: `validate` without `-c` skips catalog checking entirely

> **Title:** `validate` silently skips all catalog checks when `-c` is omitted — documents with nonexistent criteria report "Valid!"
>
> **Body sketch:** `openacr validate -f doc.yaml` (no `-c`) does not load
> the catalog named in the document's own `catalog:` field. A document
> claiming criterion `9.9.9` in `success_criteria_level_a` reports
> `Valid!`; with `-c catalog/2.5-edition-wcag-2.2-508-en.yaml` it is
> correctly rejected ("criteria '9.9.9' is not included…"). Suggest:
> resolve the catalog from the document's `catalog:` field by default, or
> exit non-zero / warn loudly when no catalog is available. Repro: (two
> commands, versions, output).

### Issue B — GSA/openacr: `output` without `-c` silently renders an empty shell

> **Title:** `output` without `-c` reports success but renders a
> metadata-only page with no criteria tables
>
> **Body sketch:** `openacr output -f openacr/drupal-10-16.yaml -t
> templates/openacr-html-0.1.0.handlebars -o out.html` exits successfully
> ("Valid and output generated") and writes 14 KB with zero criteria
> tables; adding `-c catalog/2.4-edition-wcag-2.1-en.yaml` produces the
> real 120 KB report. Reproduced on the package's own shipped example. A
> silently criteria-less "rendered ACR" is exactly the artifact that gets
> attached to a procurement packet unread. Suggest: same default-catalog
> resolution as Issue A, or a hard error when the catalog is absent.

### Issue C — GSA/openacr: `validate` accepts `not-evaluated` on Level A/AA criteria

> **Title:** `validate` does not enforce the catalog's own "Not Evaluated
> may only be used for WCAG Level AAA" rule
>
> **Body sketch:** the catalogs' `terms:` text restricts `not-evaluated`
> to Level AAA; `validate` accepts it on 1.1.1 (`Valid!`). Combined with
> no completeness checking (a 2-criterion document also validates), a
> boilerplate ACR passes the official toolchain end to end. Repro included.

### Issue E — GSA/openacr: `validate` exits 0 on invalid input

> **Title:** `validate` always exits 0 — Invalid results are stdout-only,
> so CI gates keyed on exit status pass invalid documents
>
> **Body sketch:** `openacr validate -f invalid.yaml -c <catalog>` prints
> `Invalid: …` and exits 0; unparseable files behave the same. Any
> pipeline using the conventional exit-status contract silently passes
> broken ACRs. Suggest exit 1 on Invalid (and on parse failure). Pairs
> with Issues A/B (the no-`-c` behaviors) as the toolchain-trust cluster.

### Issue D — GSA/openacr-editor: cannot import the 2.5-edition / WCAG 2.2 catalogs the format ships

> **Title:** Editor rejects valid `2.5-edition-wcag-2.2-*` documents —
> catalog skew with the frozen format
>
> **Body sketch:** acreditor.section508.gov validates imports against the
> 2.4-edition/WCAG 2.1 catalog only; a CLI-valid
> `2.5-edition-wcag-2.2-508-en` document is rejected by criterion
> ("criteria '2.5.8' is not included in 'Table 2…'") while its
> 2.4-edition equivalent imports cleanly (verified 2026-08-12, editor
> v1.0 April 2024). Ask: 2.5-edition catalog support, or a documented
> statement of the supported catalog set.

Filing order: A and B are the sharp, actionable ones (same root cause —
consider cross-referencing); C strengthens A; D is the editor-repo skew
issue the reference doc's watch rule already tracks. After filing, add the
issue URLs to `docs/openacr-reference.md` §Upstream and set the KAT-style
recheck-on-pin-bump note.

## Part 3 — Loose ends from Phases 2–3 (optional, non-blocking)

- Hosted tier breadth: sonnet/Codex/Gemini rows for both lanes; local
  `acr-baseline` rows (the A/B has hosted rows only).
- Instrument-rev candidates recorded, not applied mid-measurement: none
  outstanding from Phase 2/3 calibration; the Lane A stem-after-context
  paraphrase limit remains a documented adjudicate-by-reading item.
- The `.claude/agents/` roster has no acr-reporting agent-def (the skill
  runs in-session or via general-purpose subagents reading SKILL.md). If
  one is ever added, `scripts/check_mirrors.py` marker discipline applies
  from day one.
