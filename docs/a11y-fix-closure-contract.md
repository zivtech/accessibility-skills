# A11y Fix-Closure Contract

The A11y Fix-Closure Contract is an optional per-item record shared by `a11y-test` and the `a11y-planner` remediation profile. It exists to make the evidence behind a *closed fix* as stable and reviewable as the [A11y Evidence Finding Contract](a11y-evidence-finding-contract.md) makes the evidence behind a *diagnosis finding*.

The bundle already contracts the evidence for finding a defect. It has never contracted the evidence for closing one. Diagnosis and remediation are different jobs: a diagnosis skill assumes the code in front of it *is* the current state, so it reasons from what it sees. Remediation cannot make that assumption — the same defect can have three different histories, and which one it has changes what "fixed" even means.

Do not emit a fix-closure record for a diagnosis finding, a clean review, or a fix that has not actually landed. A record with no interaction evidence keyed to the defect class is not a closed fix; it is a claim.

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

## The closure rule

A fix-closure record whose `interaction_evidence` does not match the class of its `original_observation` fails closure. A focus defect closed with only a screenshot, a screen-reader-name defect closed with only a passing automated scan, a reflow defect closed with a desktop screenshot — each is a structurally valid record that has not demonstrated the fix. Schema validity is not closure; class-matched interaction evidence is.

## Relationship to the other contracts

- The [A11y Evidence Finding Contract](a11y-evidence-finding-contract.md) is the *input*: a fix-closure record's `closes` and `original_observation` come from a finding. One finding closes to at most one fix-closure record.
- The `a11y-planner` remediation profile is where the triage-first discipline is planned before code is written; this contract is where the closure is recorded after.

## What this does not establish

- A closed fix is a corrected *defect*, not a conformance verdict for the product or page. Aggregating closures does not produce a conformance claim.
- Triage A ("already fixed upstream") asserts only that the named defect no longer reproduces under the tested condition — not that the surrounding code is otherwise correct.
- This contract records the evidence for a fix; it does not decide whether the fix is complete against the full component. That is the reviewer's judgment.
