# A11y Orthogonality Register

Two measures are **orthogonal** when neither may be derived from the other: each must be reported on its own evidence, and collapsing them into a single verdict destroys information a reader needs. This register collects the orthogonal axis pairs this bundle relies on, and the machine mechanism (`claim_boundary`) that makes "report both, never derive one from the other" checkable rather than aspirational.

The bundle already states one such pair — conformance outcome vs impact severity — in [CLAUDE.md](../CLAUDE.md) and the [evaluation report contract](a11y-evaluation-report-contract.md). It is listed here for completeness; **do not re-derive or restate it as new**. The remaining pairs follow the identical rule.

## The register

| Axis A | Axis B | Why neither derives from the other |
|---|---|---|
| conformance outcome | impact severity | *(already stated in CLAUDE.md / evaluation report contract)* A criterion can FAIL with low user impact, or be a serious barrier while technically passing with an exception. |
| package integrity | product conformance | A deliverable package can pass all of its own integrity assertions while the product it describes still has a REVISE conformance posture. A valid package is not a conforming product. |
| remediation entry | conformance evidence | A remediation entry is a testable *correction target*, not evidence that the product currently passes or fails. Opening a fix does not change the conformance record; closing one does not either, until re-tested. |
| interaction-journey count | WCAG-EM page/view sample count | Separate ledgers with separate sampling logic, reconciled explicitly and never conflated: journeys are task paths, samples are pages/views. |
| issue-tracker state / freshness | adherence term | The issue tracker is a *control plane* (what work exists, who owns it, its state); the evaluation report is the *evidence spine*. Issue state or staleness must never gate or determine an adherence term. |
| Revised-508 floor (WCAG 2.0 A/AA) | WCAG 2.2 AA remediation layer | Reported as two layers, never merged into one verdict. The federal floor and the recommendation layer answer different questions. (See the federal profile in CLAUDE.md.) |
| evidence provenance (who confirmed, when, at which version) | conformance outcome | Provenance decides whether an outcome may be *published* as an improved term, never what the outcome *is*. The gate is one-way: absent provenance suppresses a term that improves on the prior evaluation; present provenance never creates or upgrades one, and never reaches a still-failing criterion's disclosed failure. Added 2026-09-03 with the fix-closure `attestation` block (issue #57); the block's `claim_boundary` is this pair's machine mechanism. |

## The mechanism: `claim_boundary`

A register of rules is only as good as its enforcement. The machine mechanism is a `claim_boundary` field carried on the adjudication or finding record itself, which states — in the artifact, not in a reviewer's head — what the entry **does** and **does not** assert. Paired with it is an **attachment rule**: a remediation entry may attach only to a source-adjudicated WCAG row that is still joined to a selected FAIL operation. An entry that attaches a remediation claim to a PASS row, or that derives one axis from the other (for example, inferring a conformance term from a fix having been made), is malformed and must fail validation.

This is the clearest diagnosis↔remediation bridge in the bundle: it lets a single record carry both "here is the correction target" and "this is not yet evidence of conformance" without the two claims bleeding into each other.

## Fixture discipline

The register earns an eval lane the way the rest of the bundle does: a fixture in which an entry derives one axis from the other — a `claim_boundary` that lets a fix silently upgrade a conformance term, or a remediation entry attached to a PASS row — must be rejected. An entry that keeps the axes separate must pass.

## What this register does not establish

- It does not add new conformance semantics; it names pairs that were already being conflated and states the separation.
- It is not exhaustive. New orthogonal pairs are added here when an engagement surfaces one that keeps getting collapsed — not speculatively.
- The `claim_boundary` field is a discipline, not a proof: it records the boundary an author asserts; it does not verify the underlying evidence is correct.
