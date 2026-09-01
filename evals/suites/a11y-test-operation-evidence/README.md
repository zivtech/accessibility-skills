# a11y-test-operation-evidence eval suite

**Status: fixtures landed; rule-based scorer pending.** This suite measures
whether an operation-evidence claim (a retest hitting a specific interactive
target, a keyboard trace, a passive DOM/AX observation) meets the
evidence-quality rules the `a11y-test` skill states, rather than whether the
underlying interaction itself is accessible. It is a sibling of
`evaluation-report` (which measures report-level aggregation honesty) at the
individual-operation level.

## What this suite is for

Each future fixture pairs a described retest operation with an evidence
package (trace excerpt, DOM/AX observation, setup/action record) and checks
whether the evidence package satisfies rules such as:

- a bounded diagnostic conclusion is not silently promoted into a keyboard-trap
  or WCAG 2.1.2 conclusion without the separate trace that establishes one;
- an action's evidence is rejected if its starting identity does not match
  the terminal state of the setup that preceded it in the same session;
- a conditional state stays `UNTESTED` when it was never naturally observed —
  a synthetic induction of the same state does not clear coverage;
- passive DOM/AX observations are accepted as supporting evidence only when
  bound to the causing action and a source allowlist, and never accepted as
  a substitute for reachability or announcement evidence;
- an ancestor substituted for an unreachable descendant is accepted only via
  a reviewed, separately frozen owner/descendant mapping — never a silent
  nearest-ancestor guess.

## Fixtures

Three fixtures cover the five rules, with a clean control for false-alarm
resistance (per this bundle's rule that a suite must prove it leaves clean
evidence alone, not only that it catches a planted violation):

| Fixture | Kind | Rules exercised |
|---|---|---|
| `op-dialog-escape-overreach` | BUG | bounded-diagnostic-not-promoted; setup/action continuity |
| `op-empty-state-coverage-shortcuts` | BUG | natural-only conditional state; passive-observation binding; ancestor-remapping review |
| `op-retest-clean` | CLEAN control | all five, in their admissible forms — must not be flagged |

Each fixture follows this bundle's existing triplet convention, matching
`evaluation-report` and `a11y-planner`:

- `fixtures/<id>.md` — the operation description + evidence package, sent to
  the model verbatim.
- `fixtures/<id>.metadata.yaml` — machine-checkable expectations, never sent.
- `rubrics/<id>.rubric.yaml` — dimension tiers and adjudication notes, never
  sent. See `RUBRIC_TEMPLATE.md` in this directory for the shape.

## Engagement-neutral by construction

The rules describe evidence-quality checks for accessibility retest operations
in general — they are not tied to any one engagement or product. The fixtures
use a generic component (a results table with a filter combobox and a details
dialog) and carry no engagement identifiers, routes, selectors, or counts.

## Scorer status

The rules here are about the **logic** of an evidence package — whether a
diagnostic was over-promoted, whether an action is continuous with its setup,
whether a coverage claim rests on a natural occurrence — not about token
presence. A naive pattern-matching scorer would be a false instrument for
them, so `ollama/score_operation_evidence.py` is deliberately **not yet
written**; each fixture's `metadata.yaml` declares the checks a future scorer
(or a model-judge) would formalize, with pattern hooks only where a hit is
mechanical. Until it exists, the fixtures serve as adjudication material read
directly against the `a11y-test` operation-evidence rules.

**Reproduce:** no scorer yet — read each `fixtures/<id>.md` against the
operation-evidence admissibility rules in `a11y-test/SKILL.md` and compare to
the expectations in the matching `metadata.yaml` / `rubrics/<id>.rubric.yaml`.
Zero model rows (calibration lane).
