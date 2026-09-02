# Engagement-tooling promotion handoff

**Date:** 2026-09-02
**Status:** OPEN — work order for a follow-up agent. No promotion is authorized by this document.
**Source:** the private `zivtech/a11y-audits` engagement package (2026-08 federal public-sites audit + interactive retest). Exact per-candidate paths and reproduction status live in that repo at
`…/skills-feedback/promotion-ledger.md` (master register, `PT-*` IDs) and `…/skills-feedback/gotcha-candidates.md` (`GT-*` interaction-rule leads).

## Why this exists

The interactive-retest engagement built ~150 harness scripts and contracts. Several are candidates to graduate into this suite — the way the `baseline-url-scan` (a11y-test's 6th mode) graduated from a one-off engagement harness on 2026-08-14. The engagement's own capture ledgers were set up but left empty (`COLLECTION_NOT_STARTED`), which is itself the failure mode PR #32 named: *"a side file nobody is required to populate is not a mechanism."* This handoff catalogues the 21 candidates, states the **job-to-be-done (JTBD)** each would perform here, and hands the gated work to a follow-up agent.

**This document does not promote anything.** It is a map, not an authorization.

## Hard constraints (do not violate)

1. **No skill edit without the explicit per-candidate user-approval checkpoint.** Approval to *catalogue* candidates is not approval to *promote* one.
2. **The promotion bar is per-candidate and non-negotiable** (see `.claude/skills/maintain-accessibility-skills/SKILL.md` § promotion bar and the source engagement's accepted-plan Phase 7):
   - two independent surface/component reproductions (a single engagement is one surface);
   - a generalized interaction principle **with** an explicit counterexample / negative space;
   - a proof the skill does not already cover it;
   - a BUG + CLEAN fixture pair, or a documented manual protocol where automation doesn't fit;
   - mirrored `.claude` and `.agents` edits with `scripts/check_mirrors.py --strict` green;
   - targeted lint / mirror / smoke / eval results shown;
   - an `a11y-critic` review of the rule and its overgeneralization risk.
3. **This is a prompt-only repository.** Tier-2/4 candidates that carry runtime (Alfa, WAVE, workbook/ACR builders) are **routed, never vendored** — a pinned dependency + adoption assessment (`docs/*-adoption-assessment.md`), never copied source. See the existing `keyboard-a11y-tester` / `virtual-screen-reader` / `baseline-url-scan` adoption assessments for the pattern.
4. **Do not import client identifiers** (site names, private URLs, engagement-specific selectors) into this public repo. Generalize; cite the private ledger for evidence.
5. **A favorable characterization is not a reproduction.** Detector output stays detector output.

## Recommended order

- **Start with PT-01 and PT-06** — the two genuinely unblocked items. PT-01's rule is already in the suite (only the scorer is missing, no new rule to argue); PT-06 is a generic open-source engine that needs generalization + an adoption assessment, not a second reproduction.
- **Then PT-09, PT-19, PT-02** — high-value tooling whose rules/skills already exist to attach to.
- **Tier 3 (PT-10…PT-17) is blocked on a genuinely second engagement.** Do not attempt to manufacture the second reproduction from the same site. Park these until a second audit supplies it.
- **Tier 4 (PT-18/20/21) are scope calls** — raise the "does this belong in a prompt-only suite?" question with the user before building.

## Candidate catalogue

Tier tags: **T1** reference implementation of a rule already in the suite · **T2** new routed instrument · **T3** interaction-rule lead · **T4** deliverable format / method.

### Tier 1 — reference implementations (rule landed, tool deferred)

- **PT-01 · Operation-evidence scorer** → `a11y-test`.
  JTBD: *when an agent retests one operation, make each PASS/FAIL admissible only with evidence bound to the real action, so a retest is trustworthy rather than a generic keyboard-chain pass.*
  Work: turn the engagement's `operation-retest/` contracts into the deferred `ollama/score_operation_evidence.py` + BUG/CLEAN fixtures under `evals/suites/`. Rule already in SKILL (PR #34); this is wiring, not a new rule.
- **PT-02 · Evidence custody & integrity tooling** → `a11y-test` evidence contract.
  JTBD: *hash every artifact append-only and tamper-evident, so evidence can't be silently edited between capture and report.*
  Work: generalize `post-capture-manifest.mjs` / `hash-evidence.mjs` into a reference script + contract text. Boundary already stated in PRs #33/#34.
- **PT-03 · Detector-resumption & coverage ledgers** → `a11y-test` detector lane.
  JTBD: *resume an interrupted batch without double-counting and separate coverage from aborts, so a collector fault isn't misread as an untestable product.*
  Work: reference implementation behind the detector-authority / collector-saturation prose.
- **PT-04 · Owner-fillable receipt templates + fail-closed gate** → `a11y-planner` REMEDIATION PROFILE.
  JTBD: *fail closed until the product owner supplies the 10 regression-gate inputs, so nobody claims a regression gate they can't build.*
  Work: runnable form of the owner-handoff checklist (PR #30).
- **PT-05 · Reachability capture & receipt** → `a11y-critic`.
  JTBD: *record route-entry reachability as evidence that can't by itself confer a journey PASS, so operability isn't over-claimed from presence.*
  Work: evidence generator behind the composite-descendant reachability clause (PR #36).

### Tier 2 — new routed instruments (generalization + adoption assessment)

- **PT-06 · Alfa-via-Playwright scan lane** → `a11y-test` (candidate 7th mode). **Strongest candidate.**
  JTBD: *run a second independent ACT-rules engine (Alfa) beside axe with native EARL output, so detections can be cross-checked and rule coverage widened.*
  Work: pin `@siteimprove/alfa-*` (open source), add a routing-table row + decision-flowchart branch + `docs/alfa-scan-adoption-assessment.md`. Mirror the `baseline-url-scan` promotion exactly. Detector output, never a verdict.
- **PT-07 · WAVE visible-canary lane** → `a11y-test` detector adapter.
  JTBD: *capture WAVE output with an integrity canary, so client-mandated WAVE evidence can be included without trusting an unverifiable capture.*
  Work: routed adapter with an explicit auth/licensing boundary (WAVE is a commercial WebAIM API). Weaker — may stay engagement-side.
- **PT-08 · VSR captured-DOM component replay** → `a11y-test` VSR (M3) sub-mode.
  JTBD: *replay captured production DOM through the virtual screen reader when source isn't supplied, so black-box audits still get component-level SR evidence.*
  Work: extend the VSR lane to audit-scope with the "not a live-site or real-SR test" boundary inline.
- **PT-09 · WCAG-EM sampling & freeze validator** → `a11y-test` audit sampling + evaluation-report contract.
  JTBD: *refuse to freeze the sample until census, random 10%, complete-process, and environment coverage all exist, so an under-sampled audit can't ship as complete.*
  Work: generalize the `validate-phase1*.mjs` family into the runnable enforcement of the sampling discipline that is currently prose only.

### Tier 3 — interaction-rule leads (blocked on a second engagement)

Full leads with negative-space requirements are in the private `gotcha-candidates.md`. Each needs a second surface + BUG/CLEAN fixtures before it becomes a rule.

- **PT-10 (GT-01) · Chart/grid/map task-level equivalence** → `a11y-critic` + `a11y-test`. *Pass a viz only when a non-visual user can do the task.* Partial code exists (one surface).
- **PT-11 (GT-02) · Custom element real key behaviour vs role** → `a11y-critic`. *Flag widgets that advertise a role they don't behave as.*
- **PT-12 (GT-03) · Duplicated responsive controls** → `a11y-critic`. *Catch ambiguous-target failures from twice-rendered controls.*
- **PT-13 (GT-04) · Canvas-map region name** → `a11y-critic` + `perspective-audit`. *Reject a named region exposing no operable equivalent.*
- **PT-14 (GT-05) · SPA route-change evidence** → `a11y-test` + `a11y-critic`. *Require title/heading/focus/update-context on silent navigations.* Overlaps keyboard-a11y-tester.
- **PT-15 (GT-06) · Copy-action announcement** → `a11y-critic`. *Announce copy success without leaking clipboard content.*
- **PT-16 (GT-07) · Async states scanners miss** → `a11y-test` + `a11y-critic`. *Cover loading/empty/error/recovery states.*
- **PT-17 (GT-08) · Cross-origin ownership split** → `a11y-planner` + report contract. *Route findings to the party who can fix them.*

### Tier 4 — deliverable formats / methods (scope calls)

- **PT-18 · Error-workbook (XLSX) builder** → `bug-reporting` / report contract.
  JTBD: *give a client team a validated spreadsheet, so non-technical owners triage and track fixes in a tool they already use.*
- **PT-19 · OpenACR interim (INCOMPLETE) draft builder** → `acr-reporting`.
  JTBD: *generate an explicitly-INCOMPLETE OpenACR draft mid-audit that never fabricates SC results, so interim conformance state can ship without over-claiming.* Direct extension of the untested→INCOMPLETE path.
- **PT-20 · Client-report build + ingestion contract** → report contract.
  JTBD: *validate an assembled report against a source-revision-checked contract, so the report can't drift from the evidence it cites.*
- **PT-21 · Contract mutation-canary discipline** → `maintain-accessibility-skills` / evals.
  JTBD: *prove a contract rejects each defective shape one dimension at a time, so a scorer that accepts everything can't masquerade as thorough.*

## How to pick this up

1. Read the private `promotion-ledger.md` / `gotcha-candidates.md` for exact paths, code, and reproduction status.
2. Pick one candidate (start PT-01 or PT-06). Confirm the user approves promoting *that* candidate.
3. Walk the seven-clause promotion bar above. For Tier 1, the rule already exists — you are wiring a scorer/tool and its fixtures. For Tier 2/4, you are pinning a dependency + writing an adoption assessment.
4. Record progress back in the private ledger's promotion-bar table, and update this file's status line when a candidate lands.

## Out of scope for this handoff

- Promoting any candidate without its per-candidate user approval and `a11y-critic` pass.
- Manufacturing a second reproduction from the same engagement surface.
- Vendoring any runtime into this repo.
- Anything that names a client site, private URL, or engagement-specific selector in this public repo.
