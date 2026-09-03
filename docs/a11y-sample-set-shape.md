# Machine-Readable `sample_set` Shape

The [A11y Evaluation Report Contract](a11y-evaluation-report-contract.md) requires a `sample_set` section and states in prose what it must contain. This document gives that section a machine-readable shape, the validity rules a checker enforces against it, and one mutation canary per rule.

**Audit scope only.** A `sample_set` exists because WCAG-EM sampling was performed. A component or feature review has no sample set, and emitting one there is the same checkbox theater the report contract warns about.

**This is a shape, not a runtime.** The repo stays prompt-only: no sample-set generator, no report builder. A validator implementing the rules below is a separate, later step — it is not shipped here, and nothing in this document should be read as claiming one exists.

Every rule below traces to the verified reference ([wcag-em-2-reference.md](wcag-em-2-reference.md)) or to the report contract itself. Where the two are silent, the rule is marked as a shape decision rather than a methodology requirement.

## Field Placement — What Does Not Live Here

Three fields belong to sibling sections of the report contract, not to `sample_set`. Putting them here would create a second home for a value the contract already places, which is how a report starts disagreeing with itself.

| Field | Lives in | Why |
|---|---|---|
| Representativeness-check outcome | `outcomes` | The contract's `outcomes` row carries "the representativeness-check result (did the random sample surface new content types or findings, and what was expanded in response)". WCAG-EM 4.3 is a comparison step whose *outcome is reported*; `sample_set` records only the consequence — see rule 11. |
| Browser, OS, and assistive-technology matrix | `accessibility_support_baseline` | That section is already required and defined as "the explicit OS + browser + assistive technology combinations evaluated against". A sample is a view; the baseline is what it was evaluated against. |
| Unmeasurable samples and the method that covered them | `coverage_boundary` | Already required, and scoped to exactly this. A sample identified by path description rather than URL (rule 1) is a strong hint that a `coverage_boundary` row is owed, but the two fields answer different questions. |

## Shape

```yaml
sample_set:
  status: frozen                 # draft | frozen
  revision: 2                    # integer, bumped on any post-freeze change
  frozen_at: 2026-09-02T00:00:00Z
  frozen_by: "J. Reviewer"
  evidence_revision: "run-2026-09-02T14:03Z"   # the evidence set this was built from
  sampling_skipped: false        # true only when the whole product was evaluated

  structured:
    - id: str-01
      represents: "product listing template"
      url: "https://portal.example.gov/listings"
      states: [default, loading, empty]
    - id: str-07
      represents: "legacy news template"
      url: "https://portal.example.gov/news/2019-archive"
      states: [default]
      added_by: representativeness_check    # rule 11
      added_at_revision: 2
    - id: str-09
      represents: "benefits enrollment kiosk welcome screen"
      path_description: "kiosk idle screen, touch anywhere, choose 'Enroll'"
      screenshot_ref: "evidence/kiosk/welcome-default.png"
      states: [default, timeout]
    - id: str-04-alt
      represents: "text-only alternate of the listing template"
      url: "https://portal.example.gov/listings?view=text"
      states: [default]
      alternate_of: str-01       # rule 7: not a separate sample, not counted

  random:
    method: "sitemap route list minus selected views, drawn with a recorded seed"
    exhausted: false             # true only when no unselected views remain
    exhausted_reason: null
    items:
      - id: rnd-01
        url: "https://portal.example.gov/detail/9"
        states: [default]

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
          rejoins: str-05        # a branch may terminate where it re-enters the default
          sequence:
            - sample: str-04
              action: "submit step 2 with the required SSN field empty"
      no_branches_reason: null

  carried_from:                  # re-evaluation only; see the contract's Re-Evaluation section
    prior_report: "2026-Q2-portal-eval"
    retained: [str-01, str-02]
    replaced: [str-03, str-05]
```

## Rules

A checker reports `valid: true` only when every rule holds. Any single failure exits non-zero with the rule number.

1. **Identity.** Every entry in `structured`, `random.items`, and `complete_processes` has a unique `id` and a non-empty `represents`. Every sample carries exactly one locator: `url`, or `path_description`, or `screenshot_ref`. WCAG-EM is explicit that for native, hybrid, and kiosk products "a list of URLs cannot be generated" and samples are identified "with unique screenshots and/or descriptions of the path"; a URL-only shape silently excludes them.
2. **Random sizing.** `count(random.items) >= ceil(0.10 * count(structured))`, counting per rule 7. The one exception is `random.exhausted: true` with a non-empty `exhausted_reason` — WCAG-EM directs the evaluator to pick a replacement on collision and says that if no new views exist, the step is complete. Without this escape a small product with a valid sample set fails the rule.
3. **Disjointness.** `random.items` and `structured` share no `id` and no locator value. The random sample is drawn from views *not already selected*, so an overlap means a structured view was relabelled rather than a new one drawn.
4. **Documented method.** `random.method` is a non-empty string. WCAG-EM requires the selection method be *documented*; it does not require it be cryptographically replayable, and a shape that demands a seed receipt over-reads the methodology.
5. **State coverage.** Every sample lists at least one entry in `states`. The report contract requires state coverage per sample.
6. **Complete processes.** At least one `complete_processes` entry exists, or `sampling_skipped: true`. Each entry has a `starting_point`, a non-empty `default_sequence`, and either at least one `branch_sequences` entry or a non-empty `no_branches_reason`. Every step in every sequence carries a non-empty `action`: WCAG-EM requires recording the actions needed to move sample-to-sample, because "in most cases the web address (URL) will not be sufficient to identify the sample in a complete process". The default sequence is the standard use case — no input errors, no optional selections — and branches are the commonly-accessed critical ones.
7. **Alternate versions.** An entry carrying `alternate_of` names an existing sample `id` and is excluded from the counts in rules 2 and 3. WCAG-EM: alternate versions "are not considered to be separate samples" and are evaluated with the sample as one unit.
8. **Skipped sampling.** `sampling_skipped: true` waives rules 2, 3, and 4, and permits an empty `random`. It does not waive rules 1, 5, or 6: the entire product becomes the selected sample set, so every view in it still needs identity, states, and its complete processes. `sampling_skipped: true` alongside a non-empty `random.items` is a contradiction and fails.
9. **Freeze.** `status: frozen` requires `frozen_at`, `frozen_by`, and `revision` all present and non-empty. A frozen set with an anonymous or undated freeze is a claim nobody signed.
10. **Revision binding.** A frozen set names `evidence_revision`. Any post-freeze change increments `revision`. A report aggregating this sample set cites the `revision` it was built from, and a deliverable citing revision N must not aggregate evidence from a different revision — this is the source-revision half of the contract's Generated-Deliverable Verification rule, which otherwise checks totals cell-by-cell without checking that both sides describe the same sample set. *(Shape decision, not a WCAG-EM requirement.)*
11. **Representativeness consequence.** When the report's `outcomes.representativeness_check` records `surfaced_new`, at least one `structured` entry carries `added_by: representativeness_check` with an `added_at_revision` greater than the revision at which the check ran. WCAG-EM 4.3 requires going back to Step 3 and repeating "until the structured sample set is adequately representative" — a report that records a surfaced-new outcome against an unchanged sample set is describing a step it did not finish.

## Mutation Canaries

One single-field mutation per rule, each of which a checker must reject. A checker that passes all eleven mutations is accepting everything and proving nothing — the discipline the promotion ledger tracks as PT-21.

| # | Rule | Mutation | Expected |
|---|---|---|---|
| 1 | Identity | Blank `structured[0].represents` | reject |
| 1b | Identity | Give one sample both `url` and `path_description` | reject |
| 2 | Random sizing | Drop `random.items` to `ceil(0.10 * n) - 1` with `exhausted: false` | reject |
| 3 | Disjointness | Copy a structured `url` into `random.items` | reject |
| 4 | Documented method | Set `random.method` to an empty string | reject |
| 5 | State coverage | Delete `states` from one structured entry | reject |
| 6 | Complete processes | Delete `branch_sequences` and leave `no_branches_reason: null` | reject |
| 6b | Complete processes | Delete `action` from one default-sequence step | reject |
| 7 | Alternate versions | Point `alternate_of` at an `id` that does not exist | reject |
| 8 | Skipped sampling | Set `sampling_skipped: true` while `random.items` is non-empty | reject |
| 9 | Freeze | Set `status: frozen` and delete `frozen_by` | reject |
| 10 | Revision binding | Change a structured entry without incrementing `revision` | reject |
| 11 | Representativeness | Record `surfaced_new` with no entry carrying `added_by` | reject |

Two negative controls belong beside them, because a checker that rejects everything also proves nothing: the shape above must validate clean, and so must a `sampling_skipped: true` variant with an empty `random` block and rule 2 waived.

## What Is Deliberately Not Generalized

The engagement harness this shape was derived from enforces considerably more. These parts stay there:

- **Seeded deterministic replay of the random draw.** WCAG-EM requires the method be recorded, not reproducible from a seed. A replay receipt is one engagement's reproducibility mechanism.
- **Fixed portfolio sizing** (an exact selected count, a minimum alternate count). A staffing and scope decision, not a sampling-adequacy rule — WCAG-EM names size, age, complexity, consistency, development-process adherence, required confidence, and availability of prior findings as the factors, and fixes no number.
- **Weighted candidate-prioritization scoring.** How pages were nominated is rationale, not validity.
- **A named product allowlist.** A generic checker takes scope as input rather than hardcoding a denominator.
- **Charter and substitution-ledger workflow** (commissioner and audit-owner confirmation, cross-owner approval of page swaps). Adjacent engagement-management concerns, outside `sample_set` entirely.
- **Source-fragment hash binding and owner-only-file evidence machinery.** That belongs to an evidence-custody contract, not to a sample-set schema.

## Provenance

Derived from a private engagement harness (22 distinct check families across 11 files, read-only) reduced to the eleven generic rules above; the reduction and the rejected checks are recorded in `evals/results/promotion-eval-2026-09/memos/1.3-memo-pt09.md`.

Three placements that memo left at low confidence were resolved here against the full prose rather than a grep, and all three moved: the representativeness-check outcome stays in `outcomes` (memo proposed a `sample_set` field), the environment matrix belongs to `accessibility_support_baseline` (memo proposed a `sample_set` rule), and the branch-sequence wording is WCAG-EM's own — starting point, default sequence, commonly-accessed critical branches, with recorded actions. Reading the full section also surfaced three defects in the memo's draft shape, now fixed as rules 1, 2, and 6: a required `canonical_url` excluded non-URL products, the 10% rule had no escape for an exhausted view pool, and sequences as bare id lists dropped the actions WCAG-EM requires.
