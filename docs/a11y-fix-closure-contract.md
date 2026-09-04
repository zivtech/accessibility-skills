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
| `attestation` | conditional | The human tier: who confirmed the fix on the product, when, against which product version, doing what and seeing what, and who confirmed it a second time. Required before the record may back a fixed-stage conformance input. Absent means `draft_not_attested` — absence never asserts attestation. Shape and rules below. |

## The closure rule

A fix-closure record whose `interaction_evidence` does not match the class of its `original_observation` fails closure. A focus defect closed with only a screenshot, a screen-reader-name defect closed with only a passing automated scan, a reflow defect closed with a desktop screenshot — each is a structurally valid record that has not demonstrated the fix. Schema validity is not closure; class-matched interaction evidence is.

## Attestation — the human tier

The closure rule decides whether the evidence *could* demonstrate the fix. It does not record that anyone looked. A closure record can be schema-valid, class-matched, and carry nobody's name — and until this block existed, that record could travel unchanged into a conformance claim. The `a11y-content-judgment` skill already refuses that for a far weaker claim (one judgment on one element): nothing is an outcome until a person's name is in `ratified_by`. This block gives fix closures the same shape, following the report contract's Appendix B `ratified_receipt` pattern rather than inventing a second idiom — with one addition Appendix B does not need: because a closure is about an *operation*, the confirmation records what the person did and saw, not just that they signed.

```yaml
attestation:
  status: attested                        # draft_not_attested | attested
  attested_by: "J. Reviewer"              # a named human, never an agent or model identifier
  attester_role: "accessibility QA lead"  # optional: who this person is to the engagement
  attested_at: 2026-09-03T15:10:00Z       # inside the evaluation window; never after the report date
  attested_against:                       # the retest-classification pin
    version: "2.14.1"                     # must equal the product version on the report and on interaction_evidence
  attested_under: "WCAG-EM 2.0 retest"    # optional; declared-508: the named test process + version
  self_attested: false                    # true when attested_by also authored the fix — disclosed, never hidden
  method:                                 # what the person did and saw — the observation, not a signature
    tooling: "Firefox 143 + NVDA 2026.1, keyboard only"
    action: "Tab to the 'Renew card' trigger, press Enter, press Escape"
    expected: "Dialog closes; focus returns to the 'Renew card' trigger"
    observed: "Dialog closed; focus on 'Renew card' — NVDA announced 'Renew card, button'"
  second_confirmation:                    # required before the record may back a fixed-stage supports
    by: "M. Second"                       # a different person, or the same person in a separate session on a later day
    at: 2026-09-04T09:02:00Z
    tooling: "Chrome 141 + JAWS 2026, keyboard only"
    observed: "Same result; focus returned to the trigger on both of two openings"
  claim_boundary: "Confirms rem-focus-return-2c7f0a1b no longer reproduces at 2.14.1 for this interaction. Not a re-evaluation of 2.4.7 across the sample set; nothing about other versions or other dialogs."
```

Rules:

- **Absent is draft.** A record with no `attestation` block, or with `status: draft_not_attested`, is a draft closure. It may still pass the closure rule and still be a useful engineering record; it may not back a fixed-stage conformance input.
- **A named human, never an agent.** `attested_by` and `second_confirmation.by` are people's names. A model name, an agent identifier, "automated", "CI", or a tool name in either field is a draft with a misleading status — treat it as `draft_not_attested` and name it in the handoff.
- **Pinned to the product, not the evidence.** `attested_against` carries the product version or content marker the person confirmed the fix on. It must equal — exact string, whitespace-trimmed, no normalization — the marker on the `interaction_evidence` artifact (a11y-test's retest classification requires that marker on every evidence artifact) and, at report time, the product version the evaluation report names. A record with several evidence artifacts pins to one marker they all carry; if they disagree, or `visual_evidence` carries a different one, the record is not attestable until re-captured. Either mismatch is a stale attestation and reads as draft. A product delta after `attested_at` expires the attestation for any *current*-conformance claim exactly as it expires frozen machine evidence: the record stays valid history, and a fresh confirmation is required.
- **An observation, not a signature.** `method` carries what the person did (`action`, with `tooling` naming the input method and any assistive technology), what they expected, and what they observed — each a non-empty statement a second person could repeat and compare. A bare "verified" is a signature without an observation and does not attest; a `method` missing any of the four is the same thing in a different shape. The observation `method` summarizes is produced by a11y-test's [human verification walk-through](../.claude/skills/a11y-test/references/human-verification-walkthrough.md): a per-operation record — where the person started and how they got there, the action, the expected and observed results — appended to the sample's evidence artifact, which the block cites rather than replaces. And the observation must have *decided* the operation: a closure attests only on a walked `PASS`. A walked `FAIL` sends the item back; a walked `BLOCKED` ("I watched and cannot decide without an instrument") is cited but leaves the record `draft_not_attested` with the instrument named — the four parts being non-empty is necessary, never sufficient, and `status: attested` over an `observed` that did not decide the operation is a misleading status.
- **Two confirmations for a fixed-stage supports.** The retest-classification rule that n = 1 is variance runs the *other* way here: a single failed reproduction costs a re-fix cycle, while a single passed one becomes a `supports` in a published document, and the person confirming a fix knows what they expect to see. A record backs a fixed-stage `supports` only with a `second_confirmation` — a different person, or the same person in a separate session on a later day — and at least one of the two confirmations not by the fix's author. The two branches are not equal: a different person is the control on that expectation; the same person on a later day controls session and environment variance only and leaves expectation uncontrolled, so it is the weaker branch, disclosed by the roster showing one name twice. When the attester authored the fix, `self_attested: true` says so; hiding it is a misleading status.
- **Dates reconcile.** `attested_at` and `second_confirmation.at` fall inside the evaluation window the report states and never after its `report_date`. A confirmation dated after the report it supports means the report closed before the person looked; it reads as draft until the report is re-issued.
- **Attestation does not cure a closure failure.** An attested record whose `interaction_evidence` still does not match the class of `original_observation` still fails closure. The two gates are independent; a signature on the wrong kind of evidence is a signed claim, not a demonstrated fix.
- **An authorization, not data.** A downstream consumer (a retest evaluation report, an `acr-reporting` draft) uses an attested record only to *admit* an outcome its own outcome map already carries. It never reads an outcome out of the closure record, and attestation never creates or upgrades a term. This is Appendix B's load-bearing rule: a receipt trusted as data is a way for a draft to write itself into the outcome map with a human's name attached. `claim_boundary` carries the record's own statement of what it does and does not assert — the orthogonality register's mechanism, applied to the register's provenance-vs-outcome pair.

What attestation asserts is narrow, and `claim_boundary` says so on the record: the named people performed or directly observed the class-matched interaction on the product at the pinned version, and the original observation did not reproduce. It does not assert that they reviewed the code, that the surrounding component is correct, that the criterion passes across the sample set, or anything about a version other than the one pinned.

And what this block cannot do: **bind a name to a person.** `attested_by` is a string the record's author writes. Nothing here authenticates it, counter-signs it, or proves the named person ever saw the record; the checks that exist are shape checks (a status, a non-agent-looking name, a matching pin, four method parts, two confirmations). The binding happens one step later and outside this contract — the `acr-reporting` handoff carries an attestation roster (every `item_id` the draft's improved terms rest on, with both names and the version) that the ACR's own signing author countersigns, and a published ACR names its remediated criteria and their closures in the notes, so a reader can see which claims depended on whom. There is no grandfathering: a fix confirmed before this block existed is attested by confirming it again on the current version, because attestation is about the product now, not about when the fix landed. There is no revocation path yet — an attester who later withdraws, or a name that turns out to be nobody, is handled by re-issuing the report, and that is recorded as an open item, not a solved one.

## Relationship to the other contracts

- The [A11y Evidence Finding Contract](a11y-evidence-finding-contract.md) is the *input*: a fix-closure record's `closes` and `original_observation` come from a finding. One finding closes to at most one fix-closure record.
- The `a11y-planner` remediation profile is where the triage-first discipline is planned before code is written; this contract is where the closure is recorded after.
- The [A11y Evaluation Report Contract](a11y-evaluation-report-contract.md) is the *downstream* on a retest: a finding this record closes carries `trend: resolved` there, and the outcome map — not this record — carries the criterion's new outcome. Appendix B of that contract is the pattern the `attestation` block follows; whether this block counts as the second independent instance that contract says it needs before a validator is licensed is an open call recorded there, not decided here.
- The `acr-reporting` skill refuses to map a previously-failed criterion to `supports` on the strength of a draft closure; the criterion goes to the INCOMPLETE list with this record's `item_id` named in the handoff — the same refusal it already makes for an unratified content judgment.

## What this does not establish

**How a person establishes it.** This contract states what must be true before a finding closes, and — since 2026-09-03 — records who confirmed it (the `attestation` block above). It still does not describe the guided verification pass that gets a human there: walking the affected pages, confirming the fix on the real thing, recording what they saw. A VPAT/ACR chain needs that pass: `acr-reporting` emits a draft somebody signs, `a11y-content-judgment` refuses any row without a name in `ratified_by`, and `acr-reporting` now refuses a fixed-stage `supports` on a draft closure. The pass itself is scoped as [#57](https://github.com/zivtech/accessibility-skills/issues/57) parts 3–4 (plan: `docs/plans/2026-09-03-human-verification-stage-plan.md`); candidate instruments stay parked in the ICT baseline assessment's Q2 until it lands. Before 2026-09-03 this contract had no attestation field at all — a closure record could be schema-valid, class-matched, and unattested, and nothing downstream noticed.



- A closed fix is a corrected *defect*, not a conformance verdict for the product or page. Aggregating closures does not produce a conformance claim.
- Triage A ("already fixed upstream") asserts only that the named defect no longer reproduces under the tested condition — not that the surrounding code is otherwise correct.
- This contract records the evidence for a fix; it does not decide whether the fix is complete against the full component. That is the reviewer's judgment.
- An attested closure is a person's confirmation of one item at one version. It is not a re-evaluation of the criterion across the sample set — that is the retest evaluation report's job — and aggregating attested closures still does not produce a conformance claim.
- This contract does not say what the attesting person does, in what order, on which pages. That walk-through procedure is a11y-test's to specify (issue #57, parts 3–4); this block only records its result.
