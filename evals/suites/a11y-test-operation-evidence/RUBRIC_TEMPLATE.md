# Rubric skeleton for a11y-test-operation-evidence fixtures

This is a template, not a graded rubric — no fixture exists yet. When a
fixture lands under `fixtures/<id>.md`, its rubric goes in
`rubrics/<id>.rubric.yaml` and should follow this shape (matching the
`evaluation-report` and `a11y-planner` suites' existing rubric format):

```yaml
fixture_id: <id>
suite: a11y-test-operation-evidence
rubric_version: "1.0"
scoring_method: rule_based
scorer: ollama/score_operation_evidence.py   # does not exist yet

dimensions:
  - id: <dimension_id>
    name: "<one-line description of the check>"
    tier: must | should
    note: "<optional adjudication note — what trap this dimension catches>"
```

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
