# Promotion-candidate dispositions — PR #39's 21 candidates

**Date:** 2026-09-02 (v2, after a `proposal-critic` REVISE — see § "Critic pass")
**Status:** Phase 1 output of the promotion program. Every row is a *disposition*, not a promotion. No skill, mirror, fixture, or scorer changes here; nothing is promoted until it clears its own per-candidate approval + critic gate.
**Receipts:** `evals/results/promotion-eval-2026-09/`. Every row whose disposition rests on a measurement or a read-only analysis cites a receipt there. Rows dispositioned on **ledger state alone** (no evidence exists to measure) say so in the Receipt column; the source catalogue for those is PR #39's handoff doc, which is amended (not closed) alongside this document.
**Source catalogue:** `docs/plans/2026-09-02-engagement-tooling-promotion-handoff.md` (PR #39) and the private ledgers in `zivtech/a11y-audits` (PR #6 there). Products of the source engagement are referred to as product-A / product-B, per the repo's client-reference policy (PR #41).

## The bar this document applies

The canonical bar is `.claude/skills/maintain-accessibility-skills/SKILL.md` § "Bar for promoting an engagement pattern to a skill rule" — **six clauses**:

1. **Two independent reproductions** — a single-source claim drives a doc edit at most, never a skill-behavior change, until a fixture reproduces the behavior; *the fixture is the second reproduction, so it lands before the skill text.*
2. **Written negative space.**
3. **A BUG/CLEAN fixture pair**, or a named manual protocol where a fixture is not possible.
4. **Mirrored skill edits**, `scripts/check_mirrors.py --strict` green.
5. **Targeted checks run and shown**, not asserted.
6. **Explicit user approval and a critic acceptance pass.**

The source engagement's accepted-plan Phase 7 (restated in the private ledger) adds a seventh, applied here as a **pre-check**: **proven skill gap** (dedupe against what `main` already carries). PR #39's numbered clause list keeps that dedupe clause but omits clause 6's user approval (present elsewhere in #39, under "Hard constraints", but absent from the bar it quotes) and clause 1's fixture-before-skill-text ordering; the amendment to #39 restores both in the quoted bar.

Disposition vocabulary: `PROMOTE-NOW` · `PROMOTE-AFTER(<dependency>)` · `FOLD-INTO(<existing artifact>)` · `DEFER(<reopen trigger>)` · `DECLINE(<reason>)`. A DECLINE or DEFER is a row state with a reason, never a deletion. The **Reason class** column says *why* a row is where it is: `evidence` (not enough reproductions) · `measured` (a receipt decided it) · `demand` (nothing needs it yet) · `home` (wrong skill to own it) · `scope` (a scope call the user owns).

## Disposition table

| ID | Job to be done (short) | Disposition | Reason class | Receipt | Blocker / next |
|---|---|---|---|---|---|
| PT-01 | operation-evidence admissibility scorer | **PROMOTE-NOW** (option A: structured disposition block in the skill; full six-clause bar). Effort **M**. | measured | `memos/1.2-scorer-spike.md`; clause 1 is met by the three fixtures already on `main` (`evals/suites/a11y-test-operation-evidence/fixtures/` — two BUG, one CLEAN control) | user chose option A in session 2026-09-02 (recorded in prose here; the WP-B PR quotes it as the clause-6 artifact); `a11y-critic` on the ≤15-line skill text **before** the scorer is built |
| PT-02 | append-only SHA-256 custody manifest for evidence | **PROMOTE-AFTER(`--verify` BUG/CLEAN pair lands first, inside WP-C, before any skill text)** — reference script only; the retention prose already exists at `a11y-test/SKILL.md:65-69` and is extended **by reference**, not restated. Effort **S**. | evidence | `memos/1.4-scans.md` § B2 (re-run with retention vocabulary after the first dedupe proved blind to that section) | ledger: 1 of 2 reproductions; the verify pair is the second |
| PT-03 | resume an interrupted detector batch; coverage vs aborts | **FOLD-INTO(`baseline-url-scan.mjs`)**, effort **M** | measured | `memos/1.3-memo-pt03.md` | nothing in the engagement script ports; build the pattern fresh with the four reuse guards (memo § 4) and five canaries (§ 5). Touches only the reference script — no SKILL.md edit — so it can run in parallel with WP-B |
| PT-04 | owner-fillable receipts, fail-closed regression-gate inputs | **DEFER(a fixture or a second remediation engagement)** | evidence | `memos/1.4-scans.md` § B (17 hits: the planner's REMEDIATION PROFILE already carries the checklist) | same ledger row as PT-01 (`1 of 2`, rule landed, tool deferred); the difference is that PT-01's fixtures exist on `main` and PT-04's do not |
| PT-05 | reachability capture as non-conferring evidence | **DECLINE(as an a11y-critic artifact)** + **OPEN(a11y-test home)** | home | `memos/1.4-scans.md` § B (174 hits; composite-descendant clause landed in #36) | the critic is read-only by definition; whether mode 5 (keyboard-a11y-tester) already captures route-entry reachability is **unverified** — its adoption assessment does not say so. Re-home to a11y-test only if a test-mode gap is shown |
| PT-06 | second ACT engine (Alfa) beside axe | **DECLINE(as a coverage-widening 7th mode)** — 2 Alfa-only A/AA rule classes against a bar of ≥3, on ≈3 independent surfaces; **cross-checking confirmed**; **EARL output unmeasured**. **RECORD** the negative result as `docs/alfa-scan-adoption-assessment.md` (decline-with-limits, the repo's existing shape) — the doc-edit ceiling clause 1 permits, and the only home the reopen triggers can have. | measured | `1.1-alfa-overlap/README.md` (+ reviewer correction), `overlap-table.md`, `PRE-DECLARATION.md` | reopen triggers: (a) ≥5 *independent* defect-bearing surfaces (not pages from one demo template) yield ≥3 Alfa-only A/AA classes; (b) Alfa or axe rule sets materially change; (c) an engagement mandates EARL-native output — measure it then. Licence MIT (lockfile). Assessment written 2026-09-02 (user go at checkpoint): `docs/alfa-scan-adoption-assessment.md` |
| PT-07 | WAVE capture with integrity canary | **DEFER(scope call — after a maker/community skill survey)** | scope | ledger state; survey receipt `memos/1.8-maker-skill-survey.md` when it lands | user's ruling 2026-09-02: do not assume other users lack a WAVE licence — the licence is the user's, not the suite's. Before any adapter is built, survey skills.sh, GitHub, npm and WebAIM's own site for maker-published or community skills/clients; reuse beats build. Both source ledgers still rate the candidate "weaker — may stay engagement-side"; the scope question (a commercial API behind a routed adapter in a prompt-only repo) is decided after the survey |
| PT-08 | VSR replay of captured production DOM | **DEFER(second black-box audit)** | evidence | ledger state | needs its own assessment; VSR blind spots (shadow DOM, `aria-busy`) apply |
| PT-09 | WCAG-EM sample-set freeze validator | **PROMOTE-AFTER(machine-readable `sample_set` appendix in the report contract)**, effort **S** | measured | `memos/1.3-memo-pt09.md` | 22-check inventory → 10 generic rules, ≤40-line YAML shape, 10 canaries. Three low-confidence points carried forward, not absorbed: (a) `representativeness_check` is absent from the contract's `sample_set` row (confirmed by the critic) — decide its home; (b) exact WCAG-EM branch-sequence wording; (c) whether the environment matrix belongs in `sample_set` or the accessibility-support baseline |
| PT-10 (GT-01) | chart/grid/map task-level equivalence | **DEFER(second reproduction)** | evidence | ledger state (private `gotcha-candidates.md`: partial code, one surface) | see Tier-3 criterion below |
| PT-11 (GT-02) | custom element real key behaviour vs role | **DEFER(second reproduction)** | evidence | ledger state (0 of 2) | see Tier-3 criterion |
| PT-12 (GT-03) | duplicated responsive controls | **DEFER(second reproduction)** | evidence | ledger state (0 of 2) | see Tier-3 criterion |
| PT-13 (GT-04) | canvas-map region name with no equivalent | **DEFER(second reproduction)** | evidence | ledger state (0 of 2) | see Tier-3 criterion |
| PT-14 (GT-05) | SPA route-change evidence set | **DEFER → wave 2, fixture-first** | evidence | `memos/1.4-scans.md` § C (19 hits: a11y-test SKILL already has SPA sections; a11y-critic focus guidance) | meets the Tier-3 criterion: an independent public reference exists (WCAG techniques for 2.4.3/4.1.3, keyboard-a11y-tester journey coverage). Formalize the evidence set beside keyboard-a11y-tester; do not re-implement |
| PT-15 (GT-06) | copy-action announcement without clipboard echo | **DEFER(second reproduction)** | evidence | ledger state (0 of 2) | see Tier-3 criterion |
| PT-16 (GT-07) | async loading/empty/error/recovery states | **DEFER → wave 2, fixture-first** | evidence | ledger state (0 of 2) | meets the Tier-3 criterion: 4.1.3 Status Messages techniques are the independent reference |
| PT-17 (GT-08) | cross-origin ownership split | **DEFER(second reproduction)** | evidence | ledger state (0 of 2) | overlaps PT-04 and the orthogonality register |
| PT-18 | XLSX error-workbook builder | **DEFER(wave 2; user-queued)** | scope | ledger state | scope: `bug-reporting` reference script, routed exact-pinned peer dep, never vendored; adoption note on the format boundary |
| PT-19 | interim (INCOMPLETE) OpenACR draft builder | **DEFER(input-spine refactor)** | measured | `memos/1.3-memo-pt19.md` | **confirmed** (against the builder's real output): the INCOMPLETE stem uses `:` where the skill and `score_acr.py` require `— untested A/AA criteria:`, so the scorer's regex does not match; **plausible, not confirmed**: one blanket reason for all 56 untested SCs vs the skill's per-SC reason requirement (the memo could not run that check without a fixture's reason tokens) — the likely structural blocker; also: hardcoded author/product/date; no `license` key, so the schema silently defaults to CC-BY-4.0 (only partly surfaced in notes); the HTML postprocessor's in-place edits are a boundary the skill does not address. Omitting untested A/AA criteria from `chapters` is CLI-valid (verified with the pinned CLI) — that part is correct |
| PT-20 | client-report build + ingestion contract | **FOLD-INTO(PT-09's shape work)** | evidence | ledger state | same schema question; no separate artifact |
| PT-21 | contract mutation-canary discipline | **FOLD-INTO(every scorer/validator test set)** | measured | `memos/1.2-scorer-spike.md` § c (18 canaries), `1.3-memo-pt03.md` § 5 (5), `1.3-memo-pt09.md` § 4 (10) | a method, not an artifact; `memos/1.4-scans.md` § B's 33 hits are unrelated uses of the words (0 hits for the compound terms) |

### Tier-3 criterion (why GT-05 and GT-07 get a fixture-first path and the others do not, yet)

Clause 1 says the fixture is the second reproduction. Writing a fixture from a single engagement observation would manufacture that reproduction. The criterion applied: a Tier-3 lead advances fixture-first only when an **independent public reference** — a WCAG technique or failure, an APG pattern, or an already-routed tool's documented coverage — describes the same interaction principle, so the fixture reproduces a documented pattern rather than one site's quirk. GT-05 and GT-07 have that today. GT-01/02/03/04/06/08 may acquire it; when one does, it gets the same path.

### Standing pre-check for routed instruments (added at the 2026-09-02 checkpoint)

Before any Tier-2 or Tier-4 candidate is built as a routed adapter or reference script, survey **skills.sh, GitHub, npm, and the tool maker's own site** for an existing skill, MCP server, client, or integration — maker-published first, then community. Reuse beats build; a maker-published skill also settles most licensing questions the suite cannot answer on a user's behalf. Applies to PT-07 (WAVE), PT-06 (Alfa, reopen trigger d), and PT-18 (XLSX). First survey: `memos/1.8-maker-skill-survey.md`.

## Notes on the rows that needed measurement

### PT-06 — Alfa: measured, scoped, recorded

Three engines (axe-core 4.13.0; HTML_CodeSniffer 2.6.0 via pa11y 9.1.1; Alfa 0.84.2 with rules 0.119.0) on six public pages in a scratch project on 2026-09-02. The requirements join from Alfa's rule metadata is documented and its coverage measured: 16 of 22 failing rule ids map to a WCAG criterion; the other six are best-practice rules with no SC binding. Against the decision rule stated before the run (`PRE-DECLARATION.md`: ≥3 distinct A/AA rule classes Alfa fails that axe+htmlcs miss on the same page, plus ≥1 plausible true positive): **2 classes** — `sia-r14` → 2.5.3 Label in Name on the APG disclosure example; `sia-r69` → 1.4.3 Contrast on a WAI "before" demo page (a quantified 4.02:1 vs 4.5:1 with the sRGB triples used) — both plausible true positives, both agent-assessed and unconfirmed against the live pages.

What the rule did and did not test. The candidate's JTBD names three value propositions: cross-check, widen coverage, EARL-native output. The rule tested **widening** only. **Cross-checking succeeded** (≥2-engine agreement on 1.1.1, 1.4.3, 2.4.4, 2.5.8, 3.1.1, 4.1.2 across the defect-dense pages). **EARL was not measured.** So the disposition is a DECLINE *as a coverage-widening seventh mode*, not a verdict on Alfa.

Sample honesty: pages 3–6 are one authored demo suite with near-identical SC profiles — one template sampled four times — so the run had about three independent defect-bearing surfaces, and a 2-vs-3 result sits inside that noise (`README.md` § Reviewer correction). The reopen trigger is therefore stated in independent surfaces.

Why RECORD rather than merely offer a doc edit: reopen triggers with no home are the "side file nobody is required to populate" failure #39 itself names; the repo's shape for "we evaluated a tool, here is the boundary" is a `docs/*-adoption-assessment.md`, and seven exist including declines-with-limits; and the durable knowledge (default JSON carries no selector or markup; the requirements-join recipe; the pins; MIT licence) is otherwise re-derived at full cost. It is written as a **negative-result record**, not as a routed alternative — routing readers to a third engine is what the measured delta does not justify.

### PT-01 — the scorer is a skill-text change, scoped as one

Clause 1 is the whole argument and it is met: the three fixtures with rubrics landed in PR #34 before any skill text, including the CLEAN control. The spike drafts the 15-line "Structured disposition block" (five stable rule ids matching the fixture metadata; a fenced yaml block with `admissibility`, per-operation `dispositions`, `rules_violated`, `claim_boundary`), maps every fixture metadata key to a mechanical check, and defines 18 smoke canaries (3 gold + 15 single-dimension mutations, including an invented-rule-id contract-integrity case). Two metadata keys are reshaped rather than dropped. The benchmark condition loads a section slice of the skill as system prompt, not the 1,016-line file; the cloud runner is skipped per the acr-reporting precedent; `validate_fixtures.py` gains its first registry-sync block for this suite (the missing acr-reporting block is a separate follow-up).

### PT-02 — script yes, prose no

The first dedupe (`sha256|checksum|custody|tamper`) could not see `a11y-test/SKILL.md:65-69`, which already carries the retention rule. Re-run with retention vocabulary (§ B2), the paragraph half of the candidate is a duplicate; the script half is a genuine gap (no custody manifest tool exists on `main`). And PT-02 is single-source (`1 of 2`), so the `--verify` positive/negative pair is its second reproduction and lands first.

### PT-03 and PT-09 — pattern, not port

Both memos reach the same conclusion: the engagement code is not portable, and what promotes is the pattern rebuilt against the suite's own artifacts with its own canaries. PT-09 additionally needs the report contract to carry a machine-readable `sample_set` shape first; being single-source, that lands as an appendix example before any validator enforces it.

## Recommended order, abort path, definition of done

1. Merge PR #41 (redaction gate) — every later receipt depends on the gate being on.
2. **Amend and merge PR #39** (it stays as the catalogue; closing it would orphan the ledger-state rows above). Amendment: the quoted bar; PT-01, PT-06, PT-19 status; order pointer to this document.
3. **Wave 1 — approved by the user 2026-09-02 (all three; order delegated):** WP-B (PT-01) and WP-D (PT-03) in parallel — different files; WP-C (PT-02) after its verify pair, rebased on whichever lands first. Each work package is its own branch off `main`; only the `a11y-test/SKILL.md` + mirror edits serialize (WP-B, WP-C). **Abort path:** a work package that fails its critic gate stops on its own branch; it blocks nothing else, and no routing row, README, or mirror text is touched until its gate passes.
4. **Wave 2 (user-queued 2026-09-02):** GT-05 and GT-07 fixture-first; PT-18; PT-07 after its scope call; PT-09 after the contract appendix; the redaction history rewrite as a separate user-called step.
5. PT-19 reopens when PT-09's shape exists and the builder can take per-SC outcome + reason.

**Phase 1 is done when:** this document's critic findings are addressed (below), the user's per-candidate checkpoint is recorded, #39 is amended, and the private ledger rows carry these states. **It is wrong if** any PROMOTE row's cited receipt turns out not to establish what the row claims.

## What this document does not do

- It promotes nothing. Each PROMOTE row still needs its own approval and critic verdict, recorded in that PR.
- It does not claim Alfa is useless: it records a measured delta below a pre-stated bar on a small, partly redundant sample, with named reopen triggers and a home for them.
- **Coverage:** the 21-candidate selection is inherited from #39 and the private ledger, which drew it from ~150 engagement scripts; that narrowing is not re-audited here. Eleven rows are dispositioned on ledger state, not on a receipt in this repo, because no evidence exists yet to measure.
- It does not update the private ledger; that happens on a branch off `zivtech/a11y-audits` `origin/main` after PR #6 merges, one row state per disposition here.
- It contains no engagement product names, operation IDs, receipt-profile names, or private URLs; `scripts/check_client_refs.py` is the gate, and this file is tracked so the gate scans it.

## Critic pass

`proposal-critic` (opus), 2026-09-02, against the receipts with the program's pre-registered predictions withheld. Twelve of twelve spot-checked receipt cites resolved exactly on `origin/main`. **Verdict on v1: REVISE** — the receipts were sound; the document was looser than them. Changes made in v2:

- **PT-02** (CRITICAL ×2): dedupe re-run with retention vocabulary (§ B2) — the retention paragraph already exists; row re-scoped to the script and moved to PROMOTE-AFTER its verify pair, because it is single-source and clause 1 caps that at a doc edit until a fixture lands. PT-01's clause-1 argument (the landed fixtures) is now stated.
- **Header** (MAJOR): the "every claim cites a receipt" line replaced with the receipt-or-ledger-state distinction, and a Reason-class column added.
- **PT-05** (MAJOR): split into DECLINE(as critic artifact) + OPEN(a11y-test home) — the mode-5 coverage claim was an assertion.
- **PT-06** (MAJOR ×3): DECLINE scoped to coverage-widening; cross-check recorded as confirmed and EARL as unmeasured; the pre-run decision rule now has a receipt (`PRE-DECLARATION.md`); the receipt's sample-composition paragraph corrected and the one-template-four-pages redundancy stated; the negative-result adoption record made the default rather than an offer.
- **PT-19** (MAJOR): the per-SC-reason finding carries its PLAUSIBLE label; the licence-default defect is listed.
- **MINOR:** #39's user-approval omission described precisely (absent from its quoted bar, present in its constraints); the "zero reproductions" framing replaced with a provenance note consistent with the ledger's `n/a (generic tool)`; WP-D's independence from SKILL.md corrected and the serialization rationale fixed; this file tracked so the gate scans it; effort on PT-01/PT-02; clause-6 evidence for PT-01 named as the WP-B PR; the PT-03 memo's broken table row fixed; #39 amended rather than closed; the 21-of-~150 coverage boundary stated; PT-07 re-scoped to a scope call; PT-20 → FOLD-INTO; PT-04 vs PT-01 differentiator stated; the Tier-3 criterion stated.

Not re-run: any measurement. Not verified by the critic and still open: the two Alfa-only findings against the live pages; the ~28 memo cites it did not sample; whether the 18 and 10 canaries are *sufficient* rather than merely counted.
