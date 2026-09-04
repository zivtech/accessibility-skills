# A11y Fix-Closure Contract

The A11y Fix-Closure Contract is an optional per-item record shared by `a11y-test` and the `a11y-planner` remediation profile. It exists to make the evidence behind a *closed fix* as stable and reviewable as the [A11y Evidence Finding Contract](a11y-evidence-finding-contract.md) makes the evidence behind a *diagnosis finding*.

The bundle already contracts the evidence for finding a defect. It has never contracted the evidence for closing one. Diagnosis and remediation are different jobs: a diagnosis skill assumes the code in front of it *is* the current state, so it reasons from what it sees. Remediation cannot make that assumption — the same defect can have three different histories, and which one it has changes what "fixed" even means.

Do not emit a fix-closure record for a diagnosis finding, a clean review, or a fix that has not actually landed. A record with no interaction evidence keyed to the defect class is not a closed fix; it is a claim.

A record has two independent gates. **Closure** asks whether the evidence matches the defect class (below). **Attestation** asks whether a named person confirmed the fix on the product. A record can pass either without the other, and a fixed-stage conformance input — an ACR `supports` on a criterion that previously failed — needs both.

## Root-cause triage — the required first field

Before any fix approach is recorded, classify the item into exactly one of three histories. This field has no analogue in the finding contract, and it is mandatory:

- **A — already fixed upstream.** The defect is not present in current state; the task is to *verify only*, not to re-implement. The evidence is a confirmation that the defect no longer reproduces under the tested condition.
- **B — a fix exists on an abandoned or reverted branch.** The correction was written but never landed; the task is to *recover* it (cherry-pick, re-apply) and then verify. The evidence includes the provenance of the recovered change.
- **C — never fixed.** The task is to *implement fresh*. The evidence is the new change plus its verification.

Skipping triage is the single most common way a remediation claim goes wrong: an item assumed to be C ("implement fresh") that is really A ("already fixed") produces a redundant change and a misleading closure note; an item assumed A that is really C ships nothing and reports success.

## Required fields

| Field | Required | Meaning |
|---|---:|---|
| `item_id` | yes | Stable lowercase identifier for the remediation item, at least 8 characters. |
| `closes` | yes | The `finding_id` (or `fingerprint`) of the diagnosis finding this item closes. |
| `original_observation` | yes | The defect as the diagnosis finding stated it — carried verbatim, not paraphrased, so closure is checked against the original claim. |
| `root_cause_triage` | yes | Exactly one of `A-verify-only`, `B-cherry-pick`, or `C-implement-fresh`. See above. |
| `fix_approach` | yes | What changed and why, at the code/config level. For triage A this is "no change; verified current state." |
| `visual_evidence` | conditional | A before/after diff *narrative* keyed to the original observation — not a bare screenshot. Required for any defect with a visual manifestation (layout, spacing, contrast, focus indicator). |
| `interaction_evidence` | yes | Evidence keyed to the defect class: a keyboard trace for a focus/operability defect, a screen-reader announcement for a name/role/state defect, a computed-style + zoom assertion for a reflow/resize defect. Must match the class of the original observation. |
| `commit` | yes | The commit SHA(s) or PR that lands the fix. For triage A, the commit that recorded the verification. |
| `residual` | optional | Anything not closed by this item, or follow-up required. Absence asserts nothing remains. |
| `attestation` | conditional | The human tier: who confirmed the fix on the product, when, against which product version, by what method. Required before the record may back a fixed-stage conformance input. Absent means `draft_not_attested` — absence never asserts attestation. Shape and rules below. |

## The closure rule

A fix-closure record whose `interaction_evidence` does not match the class of its `original_observation` fails closure. A focus defect closed with only a screenshot, a screen-reader-name defect closed with only a passing automated scan, a reflow defect closed with a desktop screenshot — each is a structurally valid record that has not demonstrated the fix. Schema validity is not closure; class-matched interaction evidence is.

## Attestation — the human tier

The closure rule decides whether the evidence *could* demonstrate the fix. It does not record that anyone looked. A closure record can be schema-valid, class-matched, and carry nobody's name — and until this block existed, that record could travel unchanged into a conformance claim. The `a11y-content-judgment` skill already refuses that for a far weaker claim (one judgment on one element): nothing is an outcome until a person's name is in `ratified_by`. This block gives fix closures the same shape, following the report contract's Appendix B `ratified_receipt` pattern rather than inventing a second idiom.

```yaml
attestation:
  status: attested                      # draft_not_attested | attested
  attested_by: "J. Reviewer"            # a named human, never an agent or model identifier
  attested_at: 2026-09-03T15:10:00Z
  attested_against:                     # the retest-classification pin: version or content marker
    version: "2.14.1"
  attestation_method: "Keyboard walk, Firefox + NVDA: Tab to the trigger, Enter, Escape; focus returned to the trigger. Reproduced in a second session."
  attester_note: "Confirmed on the staging build named above; the production deploy is not covered."
```

Rules:

- **Absent is draft.** A record with no `attestation` block, or with `status: draft_not_attested`, is a draft closure. It may still pass the closure rule and still be a useful engineering record; it may not back a fixed-stage conformance input.
- **A named human, never an agent.** `attested_by` is a person's name. A model name, an agent identifier, "automated", "CI", or a tool name in that field is a draft with a misleading status — treat it as `draft_not_attested` and name it in the handoff.
- **Pinned to the product, not the evidence.** `attested_against` carries the product version or content marker the person confirmed the fix on, and it must equal the marker recorded on the `interaction_evidence` artifact (a11y-test's retest classification requires that marker on every evidence artifact). A mismatch is a stale attestation. A product delta after `attested_at` expires the attestation for any *current*-conformance claim exactly as it expires frozen machine evidence: the record stays valid history, and a fresh confirmation is required.
- **Method, not just a signature.** `attestation_method` states what the person did — the input method, the assistive technology if any, the action, and what they observed — in enough detail that a second person could repeat it. A bare "verified" is a signature without an observation and does not attest.
- **Attestation does not cure a closure failure.** An attested record whose `interaction_evidence` still does not match the class of `original_observation` still fails closure. The two gates are independent; a signature on the wrong kind of evidence is a signed claim, not a demonstrated fix.
- **An authorization, not data.** A downstream consumer (a retest evaluation report, an `acr-reporting` draft) uses an attested record only to *admit* an outcome that its own outcome map already carries. It never reads an outcome out of the closure record. This is Appendix B's load-bearing rule: a receipt trusted as data is a way for a draft to write itself into the outcome map with a human's name attached.

What attestation asserts is narrow: the named person performed or directly observed the class-matched interaction on the product at the pinned version, and the original observation did not reproduce. It does not assert that the person reviewed the code, that the surrounding component is correct, or anything about a version other than the one pinned.

## Relationship to the other contracts

- The [A11y Evidence Finding Contract](a11y-evidence-finding-contract.md) is the *input*: a fix-closure record's `closes` and `original_observation` come from a finding. One finding closes to at most one fix-closure record.
- The `a11y-planner` remediation profile is where the triage-first discipline is planned before code is written; this contract is where the closure is recorded after.
- The [A11y Evaluation Report Contract](a11y-evaluation-report-contract.md) is the *downstream* on a retest: a finding this record closes carries `trend: resolved` there, and the outcome map — not this record — carries the criterion's new outcome. Appendix B of that contract is the pattern the `attestation` block follows; whether this block counts as the second independent instance that contract says it needs before a validator is licensed is an open call recorded there, not decided here.
- The `acr-reporting` skill refuses to map a previously-failed criterion to `supports` on the strength of a draft closure; the criterion goes to the INCOMPLETE list with this record's `item_id` named in the handoff — the same refusal it already makes for an unratified content judgment.

## What this does not establish

**How a person establishes it.** This contract states what must be true before a finding closes, and — since 2026-09-03 — records who confirmed it (the `attestation` block below). It still does not describe the guided verification pass that gets a human there: walking the affected pages, confirming the fix on the real thing, recording what they saw. A VPAT/ACR chain needs that pass: `acr-reporting` emits a draft somebody signs, `a11y-content-judgment` refuses any row without a name in `ratified_by`, and `acr-reporting` now refuses a fixed-stage `supports` on a draft closure. The pass itself is scoped as [#57](https://github.com/zivtech/accessibility-skills/issues/57) parts 3–4 (plan: `docs/plans/2026-09-03-human-verification-stage-plan.md`); candidate instruments stay parked in the ICT baseline assessment's Q2 until it lands. Before 2026-09-03 this contract had no attestation field at all — a closure record could be schema-valid, class-matched, and unattested, and nothing downstream noticed.



- A closed fix is a corrected *defect*, not a conformance verdict for the product or page. Aggregating closures does not produce a conformance claim.
- Triage A ("already fixed upstream") asserts only that the named defect no longer reproduces under the tested condition — not that the surrounding code is otherwise correct.
- This contract records the evidence for a fix; it does not decide whether the fix is complete against the full component. That is the reviewer's judgment.
- An attested closure is a person's confirmation of one item at one version. It is not a re-evaluation of the criterion across the sample set — that is the retest evaluation report's job — and aggregating attested closures still does not produce a conformance claim.
- This contract does not say what the attesting person does, in what order, on which pages. That walk-through procedure is a11y-test's to specify (issue #57, parts 3–4); this block only records its result.
