# Rubric skeleton for a11y-test-operation-evidence fixtures

This is a template. When a fixture lands under `fixtures/<id>.md`, its rubric
goes in `rubrics/<id>.rubric.yaml` and should follow this shape (matching the
`evaluation-report` and `a11y-planner` suites' existing rubric format):

```yaml
fixture_id: <id>
suite: a11y-test-operation-evidence
rubric_version: "1.0"
scoring_method: rule_based
scorer: ollama/score_operation_evidence.py

dimensions:
  - id: <dimension_id>
    name: "<one-line description of the check>"
    tier: must | should
    note: "<optional adjudication note — what trap this dimension catches>"
```

## Structured disposition block

`ollama/score_operation_evidence.py` scores the fenced yaml block a review
closes with, per the `a11y-test` SKILL.md contract ("### Structured
disposition block", which follows "### Operation-evidence admissibility" —
read both before writing a fixture or its metadata). Rule *selection* is the
model's semantic judgment; the block only makes *reporting* that judgment
mechanical, the same split `score_acr.py` uses for the ACR yaml block.

A fixture's `metadata.yaml` drives the scorer through these keys:

- `expected_admissibility`: `ACCEPT` or `REJECT`.
- `expected_dispositions`: `{<operation id>: PASS|FAIL|UNTESTED|BLOCKED}` for
  every operation the scorer should check.
- `must_catch[]`: `{id: <stable rule id>, operation: <OP>, hook_present: [...],
  hook_absent_in_evidence: [...]}` — `hook_present` tokens are should-tier
  (any one, case-insensitive, in the review's prose). `hook_absent_in_evidence`
  is **documentation only** — it names what a well-formed rejection's prose
  should not need to say, but the scorer does not check it (penalizing a
  correct review for not describing evidence the package never had would be a
  false instrument).
- `rules_violated_must_be_empty_for: [<OP>, ...]`: operations where any fired
  rule is a false positive (must-tier).
- `must_catch` is the **complete** expected `rules_violated` map, not a floor:
  the scorer treats any (operation, rule) pair outside it as an unexpected fire
  (must-tier), so a review that flags every rule fails. Opt out for a fixture
  that deliberately under-specifies with `rules_violated_exhaustive: false`
  (no fixture does today — prefer completing `must_catch`).
- Values are matched case-sensitively against the contract's uppercase closed
  sets (`ACCEPT`/`REJECT`, `PASS`/`FAIL`/`UNTESTED`/`BLOCKED`); a lowercase
  value is an unknown value, not a near miss.
- `expected_verdict_must_not: [...]`: forbidden phrases (checked against the
  prose after negation-stripping — a fabrication if it survives).
- `nice_to_have`: informational only, printed but never scored.

See `fixtures/*.metadata.yaml` for worked examples of every key.

## Candidate dimensions, one per operation-evidence rule

Each rule named in the suite README suggests its own `must`-tier dimension
once a fixture exercises it:

| Candidate dimension | What it should catch |
|---|---|
| `bounded_diagnostic_not_promoted` | A `focus_stagnation_observed`-class diagnostic reported as a keyboard-trap or WCAG 2.1.2 conclusion without the separate trace that would establish one. |
| `setup_action_continuity` | An action's evidence accepted even though its starting identity does not match the terminal identity of the setup that preceded it in the same session. |
| `natural_only_conditional_state` | A conditional state marked covered from a synthetic induction rather than a natural occurrence — should stay `UNTESTED`. |
| `passive_observation_binding` | A passive DOM/AX observation accepted as reachability or announcement evidence, rather than only as support bound to the causing action plus a source allowlist. |
| `ancestor_remapping_review` | A nearest-ancestor substitution accepted silently instead of via a reviewed, separately frozen owner/descendant mapping. |

A real fixture does not need to exercise all five in one pass — a fixture
that cleanly exercises one or two rules, with a clean (non-violating)
counterpart to control for over-flagging, is preferable to one fixture
trying to carry every rule at once.
