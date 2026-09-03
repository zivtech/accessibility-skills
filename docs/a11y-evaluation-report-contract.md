# A11y Evaluation Report Contract

The A11y Evaluation Report Contract is the report-level companion to the finding-level [A11y Evidence Finding Contract](a11y-evidence-finding-contract.md). One evaluation report aggregates many findings; findings reference the report through the optional `evaluation_context` field, and the report references findings by `finding_id`.

Use it for **audit-scope work only**: conformance evaluations of an existing site or digital product, pre-VPAT audits, and periodic monitoring — the engagements where the planner's audit-scope mode and a11y-test's sampling discipline apply. Its shape follows WCAG-EM Step 5.1 (verified against the 2.0 Note in [wcag-em-2-reference.md](wcag-em-2-reference.md)). Do not produce an evaluation report for a component or feature review — that is the critic's finding-level territory, and an EM-shaped report there is checkbox theater.

## Required Sections

| Section | Required | Contents |
|---|---:|---|
| `evaluation_identity` | yes | Evaluator name; evaluation commissioner; evaluation date (completion date or duration); methodology + version cited (e.g., WCAG-EM 2.0 — cite the version the engagement requires). Optional: report version/identifier, repeat-evaluation dates, party responsible for the product. ACR-feed fields — required whenever the engagement's report template is an ACR in OpenACR format: report title, product name + version, evaluator contact email (`author.email` is schema-required there), feedback channel. |
| `scope` | yes | Unambiguous in/out rule for every view (full product enclosure); named exclusions only where the engagement's own scope statement makes them explicit. |
| `conformance_target` | yes | WCAG 2 version and level (e.g., WCAG 2.2 AA). |
| `accessibility_support_baseline` | yes | The explicit OS + browser + assistive technology combinations evaluated against. If tools were added mid-evaluation, the extended baseline — as evaluated, not as originally planned. |
| `additional_requirements` | when agreed | Report template (e.g., VPAT edition), issue granularity, user involvement, or other commissioner requirements. |
| `technologies_relied_upon` | yes | Technologies relied upon for conformance (HTML, CSS, JS, WAI-ARIA, PDF...). Optional: common views, essential functionality, sample-type variety, other relevant samples from exploration. |
| `sample_set` | yes | Three parts, each with rationale: structured samples (what each represents — template, functionality, technology, shared component); random samples **and the selection method**; complete processes with their default and branch sequences. State coverage per sample. If sampling was skipped because the whole product was evaluated, say so. A non-normative serialization example is in Appendix A. |
| `outcomes` | yes | Per-SC outcomes across the sample set using the EARL vocabulary already documented in `bug-reporting`: `passed` / `failed` / `cantTell` / `inapplicable` / `untested`. At least one example per conformance requirement and per SC not met. The representativeness-check result (did the random sample surface new content types or findings, and what was expanded in response). Every planned sample-by-SC unit carries a disposition before the report closes — see "Completeness" below. |
| `findings` | yes | The `finding_id` list of A11y Evidence Finding Contract blocks backing the outcomes. Severity in those findings stays user-impact-based and **orthogonal** to conformance outcomes. |
| `coverage_boundary` | yes | Every sample the web measurement stack (Playwright, axe-core, CDP) could not measure — native screens, kiosk hardware, documents — and the manual/AT method that covered it instead. "None" is a valid value; silence is not. |
| `honest_boundary` | yes | An explicit statement of what this report's result does **not** establish — distinct from `coverage_boundary`'s unmeasured-samples list. Named limits on method, tooling, or generalization that a reader could otherwise over-read into the outcome map: for example, a clean automated scan is not a conformance claim; a `passed` outcome on a sampled instance of a pattern is not a claim about every instance of that pattern elsewhere in the product; this evaluation covers accessibility conformance and does not evaluate usability, performance, or SEO. See "Honest Boundary Requirement" below. |
| `evaluation_statement` | optional | Only when every non-optional methodology requirement is satisfied and all evaluated samples meet the target level. Includes issue date, guidelines title/version/URI, level, product definition, technologies relied upon, and baseline. Partial-conformance statements name the non-conforming areas and the reason. Sampling-based evaluation alone does not support a WCAG 2 conformance claim for the whole product — statements must not imply one. |
| `aggregated_score` | discouraged | WCAG-EM cautions that scores can mislead. If the commissioner requires one, document the scoring approach alongside it. |
| `machine_readable` | optional | EARL export reference and/or OpenACR draft reference, when produced. EARL is the assertion-level evidence export; OpenACR is the ACR-shaped deliverable (via the `acr-reporting` skill — recommended as of 2026-08-12, Phase 2 gate passed; format receipts in [openacr-reference.md](openacr-reference.md)). |
| `federal_annex` | optional | Declared-508 engagements only (the planner federal profile's floor declaration is the gate): per-baseline-test outcome rollup — see "Federal Annex" below. Not an ACR/VPAT. |

## Completeness

"We ran the evaluation" and "every planned sample has a result" are different claims until proven equal. A report is not complete when testing stops — it is complete when **zero** planned sample-by-SC units remain unresolved: every unit in the planned `sample_set` × applicable-SC matrix carries a visible disposition (`passed` / `failed` / `cantTell` / `inapplicable` / `untested`), and none silently drop out of the count because a page failed to load, a session ran out of time, or a sample was quietly swapped for an easier one. Untested and cantTell units still count — that is what makes an INCOMPLETE report distinguishable from a complete one, rather than the two looking identical because both omit the same gaps.

This is the report-level half of the same completeness rule `a11y-test`'s Campaign Completeness Contract states at the runner level (zero-unresolved exit condition, recovery path for unresolved operations, resumption across interrupted runs) — promoting either alone would leave the other layer's claim unstated.

## Orthogonality Rule

Conformance outcome and impact severity are different dimensions and both are reported:

- A `failed` outcome on 4.1.2 may be MINOR when the affected widget has an accessible fallback path.
- A `failed` outcome on 2.1.1 inside a checkout process is CRITICAL because the person cannot buy — not because the checklist says so.

Never derive severity from rule weight, and never collapse per-SC outcomes into a severity ranking. The report carries the outcome map; the findings carry the impact judgments.

## Honest Boundary Requirement

An explicit statement of what a result does **not** establish has independently reappeared across this bundle's own working documents — a harness README, a validation record, a retest package README — each written for a different purpose. A convention that reinvents itself that often wants to be a required section, not an author's habit, so `honest_boundary` is required on every report, not optional prose left to the evaluator's discretion.

This is distinct from `coverage_boundary`, which is scoped to *unmeasured samples* (what the stack could not reach). `honest_boundary` is scoped to *over-reading the result that was produced* — the gap between what the outcome map literally says and what a reader might assume it implies. A short, specific list beats a disclaimer: name the actual limits (method, tooling ceiling, sample-to-population generalization, out-of-scope quality dimensions) rather than writing a generic "no warranty" line that says nothing falsifiable.

## Generated-Deliverable Verification

A generated report artifact — a rendered outcome table, an exported workbook, a serialized ACR — can be structurally valid and numerically wrong: a formula range that under-counts, a mapping that drops rows, a rollup that double-counts. Schema and shape validation catch none of it. Every generated deliverable that carries counts or totals is verified cell-by-cell against the known totals in the evidence it aggregates — sample counts, finding counts, per-criterion outcome tallies — before it leaves as a draft. Retaining prior revisions (the append-only retention rule in `a11y-test`) is what makes such an error findable: the wrong number is visible only when a later revision can be diffed against the one that was wrong.

## Appendix A — `sample_set` Serialization (non-normative example)

**Non-normative example; no validator enforces this until a second instance exists.** This block illustrates one way to serialize the `sample_set` row above. It is a worked example, not a schema: the prose row is the requirement, nothing in this bundle validates against the shape below, and a report that expresses the same content differently is not thereby wrong. The line matters because this contract is cited as an input by `acr-reporting` and by `ollama/score_evalreport.py` — a shape read as normative here would silently become a gate there.

Derived from a single engagement (an 11-file validator from which `evals/results/promotion-eval-2026-09/memos/1.3-memo-pt09.md` inventoried 22 check families, drawn from 10 of those files). Single-source, so it lands as an example; a validator waits for a second independent instance.

### Field placement — what this block does not carry

Three values belong to sibling sections and stay there. A serialization that relocates them creates a second home for a value this contract already places, which is how a report starts disagreeing with itself.

| Value | Section that owns it | Why |
|---|---|---|
| Representativeness-check outcome | `outcomes` | That row carries "the representativeness-check result (did the random sample surface new content types or findings, and what was expanded in response)". WCAG-EM 4.3 is a comparison step whose *outcome is reported*. `sample_set` records only the consequence — the entries added in response. |
| Browser, OS, and assistive-technology matrix | `accessibility_support_baseline` | Already required, and defined as "the explicit OS + browser + assistive technology combinations evaluated against". A sample is a view; the baseline is what it was evaluated against. |
| Unmeasurable samples and what covered them instead | `coverage_boundary` | Already required and scoped to exactly this. A sample identified by path description rather than URL is a hint that a `coverage_boundary` row is owed — a hint, not an implication; the two answer different questions. |

The source memo proposed the first two as `sample_set` fields. Both moved.

### Example

```yaml
sample_set:
  status: frozen                 # draft | frozen
  revision: 2
  frozen_at: 2026-09-02T00:00:00Z
  frozen_by: "J. Reviewer"
  evidence_revision: "run-2026-09-02T14:03Z"
  sampling_skipped: false

  structured:
    - id: str-01
      represents: "product listing template"
      covers: [page_type, common_view]
      url: "https://portal.example.gov/listings"
      states: [default, loading, empty]
    - id: str-02
      represents: "benefits application step 1"
      covers: [essential_functionality]
      url: "https://portal.example.gov/apply"
      states: [default, error]
    - id: str-03
      represents: "benefits application step 2"
      covers: [essential_functionality]
      url: "https://portal.example.gov/apply/2"
      states: [default, error]
    - id: str-05
      represents: "application confirmation"
      covers: [essential_functionality]
      url: "https://portal.example.gov/apply/done"
      states: [default]
    - id: str-06
      represents: "PDF benefits schedule"
      covers: [technology]
      path_description: "linked from the confirmation page, opens the 2026 schedule"
      states: [default]
    - id: str-07
      represents: "legacy news template"
      covers: [other_relevant]
      url: "https://portal.example.gov/news/2019-archive"
      states: [default]
      added_by: representativeness_check
      added_at_revision: 2
    - id: str-09
      represents: "enrollment kiosk welcome screen"
      covers: [common_view]
      path_description: "kiosk idle screen, touch anywhere, choose 'Enroll'"
      screenshot_ref: "evidence/kiosk/welcome-default.png"
      states: [default, timeout]
    - id: str-01-alt
      represents: "text-only alternate of the listing template"
      alternate_of: str-01
      url: "https://portal.example.gov/listings?view=text"
      states: [default]

  random:
    method: "sitemap route list minus selected views, drawn with a recorded seed"
    exhausted: false
    exhausted_reason: null
    items:
      - id: rnd-01
        represents: "randomly drawn detail view"
        url: "https://portal.example.gov/detail/9"
        states: [default]

  no_processes_reason: null      # set only when complete_processes is empty
  complete_processes:
    - id: proc-01
      represents: "benefits application"
      starting_point: "https://portal.example.gov/apply"
      default_sequence:
        - sample: str-02
          action: "open /apply from the header 'Apply' link"
        - sample: str-03
          action: "complete step 1 with valid input, activate 'Continue'"
        - sample: str-05
          action: "activate 'Submit application'"
      branch_sequences:
        - name: "step 2 validation error"
          rejoins: str-05
          sequence:
            - sample: str-03
              action: "submit step 2 with the required SSN field empty"
      no_branches_reason: null

  carried_from:
    prior_report: "2026-Q2-portal-eval"
    retained: [str-01, str-02]
    replaced: [str-03, str-05]
```

### What a validator would check, when one is sanctioned

Descriptive, not a CLI contract. Each item names the input it needs, because they are not all the same — the single largest thing to settle before implementing any of this.

**Decidable from the `sample_set` block alone:**

1. **Identity and classification.** Every entry has a unique `id` and a non-empty `represents`. Every `structured` entry that is not an alternate version also carries at least one `covers` value; random items and alternates must not carry it — the random sample is drawn precisely *without* regard to the classification, and an alternate inherits its parent's. A sample carries at least one locator; `url` and the non-URL locators (`path_description`, `screenshot_ref`) are mutually exclusive as *kinds*, but a non-URL sample may carry both — WCAG-EM identifies such samples "with unique screenshots and/or descriptions of the path", so forbidding the pair would forbid what the methodology recommends. A `complete_processes` entry is not a sample and needs no locator; it has a `starting_point`.
2. **Step 2 coverage.** `covers` takes values from a closed set of five, one per WCAG-EM Step 2 list: `common_view`, `essential_functionality`, `page_type`, `technology`, `other_relevant`. The values across `structured` span all five, or a named list carries a non-empty reason for absence. The vocabulary is stated here rather than left to the example, because a checker cannot map values to lists without it — and this item claims to be decidable from the block, which it cannot be while the enum lives only in a sample. Without this a structured sample can be arbitrary and still pass every other check, which would make the shape weaker than the sampling discipline in `a11y-test` and `a11y-planner` that it serializes.
3. **Random sizing.** `count(random.items) >= ceil(0.10 * count(structured))`, counting per item 6. The exception is `random.exhausted: true` with a non-empty `exhausted_reason`: WCAG-EM directs a replacement pick on collision and says that if no new views exist the step is complete, so a small product with a valid sample set must not fail here. *(Two parts of this are shape decisions, not the methodology. WCAG-EM says the number "**is** 10% of the structured sample set" and the verified reference records no minimum in either version — so both the rounding rule and reading it as a floor rather than an exact count are choices made here. `ceil` forces one random sample onto any non-empty structured set, which is a defensible reading and still a reading.)*
4. **Disjointness.** `random.items` and `structured` share no `id` and no locator value.
5. **Documented method.** `random.method` is non-empty. WCAG-EM requires the method be *documented*, not seed-reproducible.
6. **Alternate versions.** An `alternate_of` entry names an existing `id` and is excluded from the counts in items 3 and 4. Note what this item does *not* catch: relabelling a genuine structured sample as an alternate shrinks the item-3 denominator, and item 6 cannot see it — the referent exists and the exclusion only makes the floor easier to clear. That vector is caught by item 1's prohibition on `covers` for alternates, which is the sole thing standing between it and a smaller random sample. Relaxing item 1 reopens it — WCAG-EM: alternate versions "are not considered to be separate samples".
7. **State coverage.** Every sample lists at least one state.
8. **Complete processes.** Each entry has a `starting_point`, a non-empty `default_sequence`, and either a `branch_sequences` entry or a non-empty `no_branches_reason`. Every sequence step carries an `action`: WCAG-EM requires recording the actions needed to move sample-to-sample, because "in most cases the web address (URL) will not be sufficient to identify the sample in a complete process". A product with no multi-step process carries a non-empty `no_processes_reason` at `sample_set` level — a sibling of `complete_processes`, not a child of a process, since an empty list has no entry to hold it — and an empty list — WCAG 2 conformance requirement 3 binds only where a page is part of a process, so a static informational product must be able to say so without falsely declaring `sampling_skipped`.
9. **Referential integrity, and re-evaluation comparability.** Every `sample` in a `default_sequence` or `branch_sequence`, every `rejoins`, and every id in `carried_from.retained` and `carried_from.replaced` names an entry that exists. A `carried_from` block present with an empty `retained` also fails. The trigger is the block's presence, not "this is a re-evaluation" — the sample set cannot know it is a re-run, and writing the rule the other way would have smuggled an undecidable condition in under a decidable heading. WCAG-EM's re-evaluation guidance keeps a sub-set of the prior sample precisely so results stay comparable, and a re-run that retains nothing has quietly become a new evaluation wearing a prior report's name. Without this a process can be traceable in form and dangling in fact, which defeats the one thing item 8 exists to guarantee — and makes this contract's Completeness rule uncomputable, since a sample-by-SC matrix cannot be built over ids that do not resolve.
10. **Skipped sampling.** `sampling_skipped: true` waives items 3, 4, and 5 and permits an empty `random`. It waives nothing else: the whole product becomes the selected sample set, so every view still needs identity, coverage, states, and its processes. That clause rejects nothing by itself — items 1, 2, 7 and 8 do the rejecting, and this item only denies them a waiver. It is exercised by running those items' canaries a second time under `sampling_skipped: true`, which is why item 7 carries a waiver-variant row. That every view is *actually* enumerated is not confirmable from the block — it would take a crawl of the product — so a checker verifies the shape of what is claimed and never the claim itself. Recorded rather than fixed, because there is no fix at this layer. `sampling_skipped: true` alongside a non-empty `random.items` is a contradiction.
11. **Freeze.** `status: frozen` requires `frozen_at`, `frozen_by`, `revision`, and `evidence_revision`. *(Shape decision. WCAG-EM says nothing about freezing a sample set; the source memo classified the draft/freeze mechanism as generic and its status vocabulary as engagement-shaped, and this bundle has one instance of it.)*

**Partly or wholly outside this block — each item says which half is decidable here:**

12. **Draft sets are not citable.** A `status: draft` set may exist and may be serialized; what it may not do is back a shipped report, which is a claim its own sample set does not yet support. Nothing in the block decides this — `status` alone is not a violation — so it is an obligation on the report, not a property of the sample set. *(Shape decision, from the same memo's generic draft-cannot-expose-frozen-claims mechanism.)*

13. **Representativeness consequence.** An entry carrying `added_by: representativeness_check` also carries an `added_at_revision` no greater than the set's `revision`, and an entry carrying `added_at_revision` carries `added_by` — the converse matters, or a bare revision stamp implies a provenance nothing recorded. That much is decidable here, and it is nearly vacuous: it catches a forward-dated typo and a dangling stamp, not whether the representativeness loop actually finished. Nobody should read a passing checker as evidence that it did. The other half is not: WCAG-EM 4.3 requires that when the random sample surfaces new content types the evaluator goes back to Step 3 and repeats "until the structured sample set is adequately representative", so a report recording a surfaced-new result against a sample set with no such entry is describing a step it did not finish. This contract states the representativeness result as prose in `outcomes` and defines no field for it, and no field anywhere records the revision at which the check ran — so the cross-section agreement is a **reader's obligation, not a checker's**, and this example deliberately does not invent the field names that would make it look otherwise. Inventing them is how a non-normative example quietly becomes a schema that something downstream keys on.

**Needs a prior revision and the deliverable that cites it:**

14. **Revision binding.** Any post-freeze change increments `revision`, and a deliverable citing revision N aggregates evidence from revision N. This is the half of Generated-Deliverable Verification that cell-by-cell total-checking cannot reach: a same-cardinality substitution — twelve samples before, twelve after, one swapped — agrees on every count and describes a different sample set. *(Shape decision.)*

### Mutation canaries

Still non-normative, and this is the part most likely to be read on its own: the table below is what a validator *would* check if one were sanctioned, not a suite anything runs today. Nothing in this bundle executes it.

Mutations a checker should reject, with the input each needs — some items need more than the block, which is the point of listing the input at all. Several items carry more than one mutation; the table is the count.

| Item | Mutation | Input needed |
|---|---|---|
| 1 | Blank `structured[0].represents` | block |
| 1 | Delete `covers` from a `structured` entry that is not an alternate | block |
| 1 | Duplicate an `id` across two entries | block |
| 1 | Give one sample both `url` and `path_description` | block |
| 1 | Put `covers` on a random item | block |
| 1 | Put `covers` on an entry carrying `alternate_of` | block |
| 1 | Relabel a real structured sample as `alternate_of` another, keeping its `covers` (the item-3 denominator vector) | block |
| 1 | Remove every locator from one sample, leaving `id` and `represents` | block |
| 2 | Name a list as absent with a blank reason | block |
| 2 | Remove every entry covering `essential_functionality`, with no stated reason | block |
| 2 | Use a `covers` value outside the five-term set | block |
| 3 | Drop `random.items` to one below the 10% floor with `exhausted: false` | block |
| 3 | Set `exhausted: true` with an empty `exhausted_reason` | block |
| 4 | Copy a structured `url` into `random.items` | block |
| 5 | Set `random.method` to an empty string | block |
| 6 | Point `alternate_of` at an id that does not exist | block |
| 7 | A sample missing `states` under `sampling_skipped: true` (the waiver variant) | block |
| 7 | Delete `states` from one structured entry | block |
| 8 | Delete `action` from one default-sequence step | block |
| 8 | Delete `branch_sequences` leaving `no_branches_reason: null` | block |
| 8 | Empty `complete_processes` with `no_processes_reason: null` and `sampling_skipped: false` | block |
| 9 | Change a `default_sequence` sample ref to a nonexistent id | block |
| 9 | Empty `carried_from.retained` with the block present | block |
| 10 | Set `sampling_skipped: true` while `random.items` is non-empty | block |
| 11 | Set `status: frozen` and delete `evidence_revision` | block |
| 11 | Set `status: frozen` and delete `frozen_by` | block |
| 12 | Cite a `status: draft` set from a report | block + report |
| 13 | An entry carrying `added_at_revision` with no `added_by` | block |
| 13 | An entry carrying `added_by` with no `added_at_revision` | block |
| 13 | Set `added_at_revision` greater than the set's `revision` | block |
| 14 | Change a structured entry without incrementing `revision` | two revisions |

The division of labour is worth stating, because getting it wrong is how the earlier drafts of this appendix failed: **a restriction is exercised by a canary, a relaxation is exercised by the clean example.** Item 1's locator rule is the model — the example's kiosk sample carries both non-URL locators, which is the relaxation, and a canary mixes a URL with a non-URL locator, which is the restriction. Every escape hatch (`exhausted_reason`, `no_branches_reason`, `no_processes_reason`, and item 2's reason for absence) additionally needs a canary on its blank-reason case, or the hatch becomes a way to say nothing. And a canary is filed under the rule that **performs the rejection**, never the rule that motivated writing it — two rows here were filed under a motivating rule that could not actually reject their mutation, which reports coverage the table does not have. When a rule's job is to deny a waiver or exclude from a count rather than to reject, say so in the rule and file the row elsewhere.

Negative controls matter as much: the example above validates clean, and so does a variant with `sampling_skipped: true`, an empty `random`, and its `complete_processes` intact. A checker that rejects everything proves as little as one that accepts everything.

### What this deliberately does not generalize

The source engagement's validator enforces considerably more. These stay there, each for a stated reason:

- **Seeded deterministic replay of the random draw.** WCAG-EM requires the method be recorded, not reproducible from a seed.
- **Fixed portfolio sizing** (an exact selected count, a minimum alternate count). WCAG-EM fixes no number — it names the factors (size, age, complexity, consistency, development-process adherence, required confidence, availability of prior findings) and leaves the count to the evaluator.
- **Weighted candidate-prioritization scoring.** How pages were nominated is rationale, not validity.
- **A named product allowlist.** A generic checker takes scope as input rather than hardcoding a denominator.
- **Charter and substitution-ledger workflow.** Adjacent engagement-management concerns, outside `sample_set`.
- **Source-fragment hash binding and owner-only-file evidence machinery.** That belongs to an evidence-custody contract.
- **A declared-complete flag reconciled against the computed gate result.** The memo classified this pattern as generic, and it is — but it describes a validator's own output contract, which does not exist until a validator does. Recorded here so the reduction's ledger is complete rather than silently short.

## Appendix B — `ratified_receipt` Serialization (non-normative example)

**Non-normative example; no validator enforces this until a second instance exists.** Same standing as Appendix A, and the same reason for saying so.

To be explicit, because two appendices sitting together invite the inference: **Appendix B is not Appendix A's second instance.** They are different patterns from the same single engagement, and each needs a second independent instance of *itself* before a validator is licensed for it. Two example blocks are two single-source examples, not one satisfied gate.

Where Appendix A shapes what was sampled, this shapes how an agent-drafted judgment becomes a human-ratified one before it may enter the outcome map. The generic mechanism is: a status, a named human ratifier, pinned sources, cells **re-derived from source rather than trusted from the receipt**, denominator membership, a no-drift check, and a closed set of outcomes a draft may propose. The rubric and the family list in the originating engagement are engagement-shaped and are not part of the pattern.

```yaml
ratified_receipt:
  status: ratified              # draft_not_ratified | ratified
  ratified_by: "J. Reviewer"    # a named human, never an agent identifier
  ratified_at: 2026-09-02T16:20:00Z
  ratifier_note: "Confirmed against the recorded session; the two grid rows differ."
  source_pins:
    outcome_map_revision: "run-2026-09-02T14:03Z"
    sample_set_revision: 2
  rows:
    - view: str-03
      criterion: "3.3.1"
      drafted_judgment: failed
      ratified_judgment: failed
      denominator: planned      # this row is inside the planned sample-by-SC matrix
```

A tamper suite over this shape would need, at minimum, the nine cases the originating engagement wrote: a wrong status, a non-human ratifier, a stale source pin, a draft proposing `passed`, cell drift between receipt and source, a smuggled cell absent from the source, a dropped row, a re-keyed view, and a re-keyed sibling. Those nine are **counted, not shown sufficient** — nobody has demonstrated they cover the space, and a second instance is what would tell.

The load-bearing rule is the one that is easiest to lose: outcome cells are re-derived from the source map at fold-in time and never read out of the receipt. A receipt that is trusted as data rather than used as an authorization is a way for a draft to write itself into the outcome map with a human's name attached.

## Example Skeleton

```markdown
# Accessibility Evaluation Report: Example Benefits Portal

## Evaluation Identity
Evaluator: ... | Commissioner: ... | Dates: 2026-08-03 → 2026-09-12
Methodology: WCAG-EM 2.0 (https://www.w3.org/TR/wcag-em-2/)

## Scope
All content on https://portal.example.gov, including the authenticated
application flow. Third-party: reCAPTCHA v2, YouTube embeds (documented,
not remediable — see Coverage Boundary and VPAT third-party language).

## Conformance Target
WCAG 2.2 Level AA

## Accessibility Support Baseline
NVDA 2026.1 + Firefox / JAWS 2026 + Chrome / VoiceOver + Safari (macOS 15,
iOS 18) / TalkBack + Chrome (Android 15) / keyboard-only / Dragon 16.

## Sample Set
Structured (12): [sample → what it represents]
Random (2 = 10%, script-selected from sitemap, seed recorded): [...]
Complete processes (2): application (6 steps + error branch), login+recovery
State coverage: default, error, loading, expanded per sample

## Outcomes
Per-SC table (passed/failed/cantTell/inapplicable/untested per criterion)
Representativeness check: random sample surfaced a legacy news template
missing from the structured set → template added, re-classified, re-run.

## Findings
a11y_appform_step3_error_assoc (CRITICAL), a11y_megamenu_esc_trap (MAJOR), ...

## Coverage Boundary
None — all samples are web views reachable by the measurement stack.

## Honest Boundary
This evaluation covers WCAG 2.2 AA conformance only — it does not evaluate
usability, performance, or SEO. A `passed` outcome on a sampled instance of
a component is not a claim about every instance of that component; the
random-sample method is designed to surface counterexamples, not to prove
their absence. Automated-scan-clean is not a conformance claim.
```

## Federal Annex (declared Section 508 engagements only)

When the engagement's audit-scope plan carries the planner federal profile's conformance floor declaration (WCAG 2.0 A/AA + the applicable non-WCAG 508 provisions — that declaration is the gate; without it this annex must not exist), the report may append a federal annex that rolls the per-SC outcomes up by ICT Testing Baseline web test:

- One row per web baseline test (62 at the pin — enumerated in [ict-baseline-test-id-manifest.yaml](ict-baseline-test-id-manifest.yaml); every cited ID must exist there). Each row: the test ID, the outcome (same EARL vocabulary: `passed` / `failed` / `cantTell` / `inapplicable` / `untested`), and the backing `finding_id` references.
- Derivation rule: a row is `failed` only from findings carrying that test in `baseline_test` — never from SC-level fan-out (one 4.1.2 failure does not fail every 4.1.2-citing test: `5.A`–`5.D`, `12.A`, `19.A`/`19.B` are distinct rows). A row is `passed` when its constituent SC/provision outcomes pass across the sample set AND no finding carries the test. Rows `17.A`–`17.C` derive from the 503.4.x provision checks (their findings cite the provision in `wcag_or_apg` per the evidence contract), not from the WCAG outcome map.
- Under declared 508 scope, the report's `conformance_target` declaration is the floor itself — "Revised Section 508 (WCAG 2.0 Level A/AA + the named non-WCAG provisions)" — and the per-SC outcome map is built against it. WCAG 2.2 AA appears as the separately-reported recommendation layer, never as the declared conformance target.
- `24.A-Parsing` is always `passed` by upstream design (WCAG 2.0 Errata 13) — record it that way with that note, never as evidence of markup quality.
- A coverage statement sourced from the a11y-test crosswalk (`references/ict-baseline-crosswalk.yaml` in the a11y-test skill): "designed to cover N of 62; gaps: ...", with the not-covered tests' manual/AT assignment named. Never "baseline-aligned" or "baseline-conformant".
- The floor-vs-target dual posture restated: annex outcomes are against the 508 floor; WCAG 2.1/2.2-only findings stay out of the annex's outcome rows and appear as recommendations against the bundle's 2.2 AA target.
- The annex aggregates evidence **for** whoever authors the Accessibility Conformance Report — it is not an ACR/VPAT, must not be presented as one, and carries no conformance badge for the test process itself.
- If the commissioner declines the annex, a declared-508 report still carries the plan's baseline-coverage statement — restate it alongside `coverage_boundary`, the same honesty axis (what the stack could not measure and what covered it instead).

## Lifecycle Wiring

- **a11y-planner (audit-scope mode)** plans the report skeleton in Phase 9 — the declarations exist before testing starts.
- **a11y-test** produces the measured evidence: per-sample scans, keyboard-a11y-tester driven sessions for complete processes, the random-sample comparison result, and finding contracts with `evaluation_context`.
- **bug-reporting** stays finding-level: individual findings become reproducible bug reports; this contract aggregates them and is where the EARL outcome vocabulary rolls up.
- **a11y-critic** reviews the report against this contract the way it reviews findings against the evidence contract — declarations present, sampling rationale real, boundary honest, severity not derived from rule weight.

## Re-Evaluation and Trend

On re-runs, follow WCAG-EM re-evaluation guidance: keep a sub-set of the prior sample for comparability and replace a sub-set (typically about half) for coverage. Carry the evidence contract's trend vocabulary (`new` / `persistent` / `worsening` / `improving` / `resolved`) at the finding level; report deltas at the outcome level (criteria newly passing/failing since the prior evaluation). Do not infer trend from a single run.

## Boundaries

- This contract does not replace VPAT/ACR templates or EN 301 549 report formats — when the engagement requires one, this contract is the internal evidence spine that populates it.
- It adds structure, not judgment: severity, ownership, and user impact stay with the critic, auditor, and evaluator.
- Prompt-only repo ruling applies: no report-generator runtime, no WCAG-EM Report Tool vendoring; EARL export stays a routed capability of external tools.
