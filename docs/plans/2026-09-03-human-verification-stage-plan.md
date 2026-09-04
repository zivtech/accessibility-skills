# Guided Human Verification Stage — Plan (issue #57)

> **Status:** DRAFT — Phase 1 implemented on `feat/human-verification-stage`, critic review pending; Phases 2–3 are design decisions recorded here and not yet built.
> **Consequence level:** Conformance-claim provenance. The artifact at the end of this chain is an ACR someone may publish and defend; a wrong decision here is a signed overclaim, not a broken tool.
> **Companion docs:** [`a11y-fix-closure-contract.md`](../a11y-fix-closure-contract.md) (the attestation block), [`a11y-evaluation-report-contract.md`](../a11y-evaluation-report-contract.md) Appendix B (the ratify pattern), `.claude/skills/acr-reporting/SKILL.md` (the gate), [`ict-testing-baseline-adoption-assessment.md`](../ict-testing-baseline-adoption-assessment.md) Q2 (the parked instrument), issue [#57](https://github.com/zivtech/accessibility-skills/issues/57).

## Verified Facts (2026-09-03, against `evals/fixture-leak-gate` @ 6d5e389 — PR #56, the branch this work sits on)

1. **`acr-reporting` never receives fix-closure records.** Its input table is the evaluation report, the findings, and engagement-record metadata (`SKILL.md` "Inputs Required"). A fixed-stage claim reaches an ACR only through the report's `outcomes` map: a criterion that was `failed` and is now `passed`. The closure record sits one layer upstream.
2. **The content-judgment gate is a direct-input gate.** A content-judgment CSV row is refused unless `status` is `RATIFIED` with a name in `ratified_by` (`SKILL.md` "Core Mandate"). It works because the CSV is an input the skill reads.
3. **The fix-closure contract had no attestation field** — required fields were `item_id`, `closes`, `original_observation`, `root_cause_triage`, `fix_approach`, `visual_evidence`, `interaction_evidence`, `commit`, `residual`. A record could be schema-valid, class-matched, and carry nobody's name.
4. **The report contract already has the ratify pattern**, as Appendix B `ratified_receipt`: a status, a named human ratifier, pinned sources, cells re-derived from source rather than trusted from the receipt, and a closed set of outcomes a draft may propose — one of its nine tamper cases is "a draft proposing `passed`." It is non-normative and says a validator is licensed only once a second *independent* instance exists.
5. **The finding contract's `trend: resolved`** means "previously present and now verified absent" and "do not infer trend from a single run." It is the finding-level mark of a fix.
6. **a11y-test's retest classification** requires the product version or content marker on every evidence artifact, and a delta expires every prior baseline as a claim about current conformance.
7. **The disposition block's four values are a closed set** (`PASS`/`FAIL`/`UNTESTED`/`BLOCKED`), and the five admissibility rules are a closed set, both exercised by `evals/suites/a11y-test-operation-evidence`. The values describe what admitted evidence establishes about an operation's predicate; the rules score the evidence package.
8. **The ICT crosswalk's 13 not-covered rows all carry `modes: [manual]`** and no machine mode: `6.C-Captcha`, `6.D-ImageText`, `7.B-SensoryCharacteristics`, `7.C-AudibleCues`, `9.A-Flashes`, `16.A`–`16.D` (audio/video alternatives), `17.E-ADPrerecorded`, `17.F-CaptionsLive`, `17.G-SyncMediaAlternative`, `20.A-ConformingAltVersion`. Every one is a judgment a person makes by looking, listening, or attending.
9. **The "Phase 4a, Q2" the issue cites exists on PR #56, not on `main`.** `origin/main`'s adoption assessment has no such section; the Q1/Q2 split and the tools.md ANDI row landed in PR #56 commit 6d5e389. This plan therefore branches from PR #56 and merges after it.
10. **The orthogonality register** carries six axis pairs; the nearest to this work is *remediation entry vs conformance evidence* — "closing a fix does not change the conformance record either, until re-tested." None of the six is a provenance-vs-outcome pair.

## Two corrections to the issue as filed

**The gate relocates.** The issue frames part 2 as "acr-reporting has no equivalent gate for fix-closure records." It cannot have one as stated, because it never sees them (fact 1). The fix is not a gate on an input the skill lacks; it is to make fix-closure records a *conditional input* — required for every finding the report carries with `trend: resolved` — and gate on that. That is what Phase 1 does. The asymmetry the issue names is real; its location was one layer off.

**"Attested" is not "resolved."** `trend: resolved` stays exactly what the finding contract says it is: what a retest observed. Attestation does not redefine it. What changes is that a resolved finding is no longer, by itself, a conformance input — the criterion goes to the INCOMPLETE list until a person's name is on the closure. The evaluator who runs a full WCAG-EM re-evaluation is the natural attester and writes the block themselves; the remediation loop (executor fixes, a11y-test retests, nobody human in between) is the case that was silently unattested before.

## Decisions

### Part 1 — attestation field (shipped, Phase 1)

`attestation` block on the fix-closure record, following Appendix B's shape, not a new idiom: `status: draft_not_attested | attested`, `attested_by` (a named human, never an agent or model identifier), `attested_at`, `attested_against` (the retest-classification pin — product version or content marker, which must equal the marker on the `interaction_evidence` artifact), `attestation_method` (what the person did and saw, repeatable by a second person), `attester_note`.

Six rules, in the contract: absent is draft; a named human never an agent; pinned to the product, and a product delta expires it; method not just a signature; attestation does not cure a closure failure (the two gates are independent); an authorization never data (the outcome is read from the outcome map, never from the record).

What was rejected: making attestation a *required* field. The closure contract is an optional per-item record used by engineering; a draft closure is a useful engineering record. Requiring the block would push people to fill it in to pass a schema, which is the failure mode the block exists to catch. Absent-is-draft is stricter in the way that matters.

### Part 2 — the `acr-reporting` gate (shipped, Phase 1)

- Fix-closure records are a conditional input: one per `trend: resolved` finding. Missing → block, gap named. Present but draft (no block, `draft_not_attested`, or non-human `attested_by`) → the criterion gets no adherence entry and goes to a **second INCOMPLETE line**: `INCOMPLETE DRAFT — unattested fix-closures on A/AA criteria: <SC (item_id), ...>`, after the untested line when both exist. The handoff names each `item_id`, what is missing, and who can close it — a person confirming on the pinned version, not more automated testing.
- Over-refusal is a must-fail too: an attested closure listed as unattested is the serializer flagging everything.
- Scorer: `ollama/score_acr.py` `check_unattested`, driven by a metadata key (`unattested_closures: {expected, gap_scs, item_ids, reason_tokens}`) the same way the untested gate is driven by `incomplete`, with a false-positive branch for every fixture that does not declare it.
- Fixture #6 `county-library-retest` (ADVERSARIAL): a plain draft closure, a closure "attested" by an agent identifier, an attested closure that must stand as `supports`, and a persistent failure mapped normally. Fixture #2 gains an attested closure for its existing resolved finding so its graded behavior is unchanged and now exercises the positive path.

Scope the gate takes deliberately: **every** resolved finding, not only those on a criterion whose term would be `supports`. A resolved finding on a still-failing criterion changes which samples the note enumerates; keeping one rule decidable beats carving an exception nobody will remember. Recorded as an over-inclusion, not an oversight.

### Part 3 — how a human observation enters the disposition block (decided, not built)

**No fifth disposition value.** A person who performs an operation and observes the result has decided the operation's predicate exactly as a trace does: the disposition is `PASS` or `FAIL`. Encoding *who observed* in the *outcome* axis would put provenance into the disposition, which is the class of collapse the orthogonality register exists to forbid. Human-sourced evidence therefore takes one of the existing four values, and the closed set stays closed.

**The five admissibility rules apply unchanged.** Read against a human session they hold as written: "focus seemed stuck" is a bounded diagnostic and not a trap conclusion until the person attempts the documented exit; the person's setup and action must be one continuous session; a person may not induce a conditional state synthetically; "I saw `role=button` in the inspector" is a passive observation bound to the causing action; a person who reaches a wrapper instead of the target has not observed the target. Nothing needs adding to the rule set.

**What is missing is the package shape, not a rule or a value.** A machine package carries its `before`/terminal identity, the key press, the observed result, and the version pin for free. A human observation needs an equivalent minimum or "I checked it, it's fine" passes as `PASS`. That minimum is: the `attestation` block from Part 1 (who, when, against which version, by what method) plus, per operation, the action performed, the expected result, and the observed result in the person's own words. That is Part 4's procedure, and it is why Parts 3 and 4 ship together.

**Where this lands for the 13 not-covered rows.** Each is a judgment a person makes by looking, listening, or attending (fact 8). Under this decision they enter as human-sourced packages with the attestation block, take `PASS`/`FAIL`, and the crosswalk row's `modes: [manual]` becomes a pointer to the procedure rather than a dead end. The crosswalk's coverage counts (22/26/13/1) do not change — "covered" means the machine stack covers it, and it does not.

### Part 4 — the walk-through procedure (Phase 2)

An a11y-test reference (not a new skill; a11y-test already owns retest classification and admissibility) specifying, for a retest campaign: (a) the input is the campaign's planned operation set and the closure records, never a free walk; (b) order: per sample, per finding, the class-matched action from the closure record's `interaction_evidence`; (c) per operation the person records action / expected / observed, and the retest-classification rule applies to them too — a single failed reproduction is variance, a FAIL needs a second session or a second person; (d) the record is the attestation block plus the per-operation lines, appended to the evidence artifact under the append-only retention rule; (e) who signs is whoever performed it — the block refuses anyone else. Exit criteria for Phase 2: the reference exists in both skill mirrors, an operation-evidence fixture exercises a human-sourced package (including the "I checked it" under-specified package as a REJECT), and one real retest has produced an attested closure that `acr-reporting` accepted.

### Instrument (Phase 3, parked)

ANDI stays where PR #56 put it — deferred, validation-gated, Q2 of the ICT baseline assessment — until Phase 2 exists to be instrumented. Picking it now would be a tool in search of a workflow, and the same-SSA-branch note in `docs/tools.md` (ANDI and YANKI are one bet) stands.

## Phase plan

| Phase | Ships | Exit criterion |
|---|---|---|
| 1 (this branch) | Parts 1 + 2: contract block, cross-refs in the finding and report contracts, `acr-reporting` gate in both mirrors, scorer check, fixture #6, fixture #2 amendment, calibrate cases | `calibrate.py` CLEAN on all cases incl. f6; mirrors in strict sync; all repo gates green; critic REVISE findings folded; PR merged after #56 |
| 2 | Parts 3 + 4: a11y-test walk-through reference, human-sourced package shape, operation-evidence fixture(s) | See Part 4 exit criteria; hosted-tier draws on the new fixture before any local row |
| 3 | Instrument choice, if any | Only after one real Phase 2 retest; Q1 probe and Q2 stay independent |

Model rows for fixture #6 are **not** in Phase 1's exit criterion. The gate is a machine contract like the rest of `acr-reporting` (Phase 2 of the OpenACR plan found bare opus judges correctly and the skill carries the contract, not the judgment); calibration proves the instrument, rows measure models. Rows follow on the usual hosted-first routing.

## Not claimed

- Not that the retest machinery was wrong. It is specified for machine-collected evidence and stays as written; this sits on top.
- Not that Appendix B now has its second instance. The attestation block was written *from* Appendix B, by the same bundle, the same week — it is a derived instance and cannot tell whether the shape survives a need that did not already know it. Recorded in the appendix; no validator is licensed.
- Not scoped to declared-508 engagements. The ACR framing makes it sharpest there; the gate fires on any engagement's resolved finding.
- Not a claim that attestation makes a criterion pass. The outcome is the report's; attestation admits it.
- No estimate for Phases 2–3.

## Where confidence drops

- **The gate's blast radius on existing reports.** Any retest report with resolved findings now blocks an ACR draft until closures are attested. That is the intended friction, and it will land on whoever runs the next retest. If it turns out too heavy in practice the relief is a narrower trigger (only `supports`-bearing criteria), not a weaker attestation.
- **"Non-human attester" is a judgment the scorer cannot make.** The scorer checks the marker, the SC set, and the item_ids; whether a model *recognised* the agent identifier as non-human is visible only in whether 2.4.11 landed on the line. A model that lists it for the wrong reason scores the same as one that reasoned. The fixture's `known_judgment_calls` say so.
- **Part 3's "the five rules apply unchanged" is argued, not exercised.** No human-sourced package has been run through the operation-evidence scorer yet. Phase 2's fixture is where that claim gets tested, and it may need a sixth rule for the under-specified-package case if the existing five turn out not to reject "I checked it."

## Critic Findings Addressed

_Pending — proposal-critic and a11y-critic review of this plan and the Phase 1 diff._
