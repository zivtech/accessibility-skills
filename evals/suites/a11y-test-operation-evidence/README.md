# a11y-test-operation-evidence eval suite

**Status: fixtures + rule-based scorer landed; zero model rows.** This suite measures
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

Six fixtures cover the five rules, with clean controls for false-alarm
resistance (per this bundle's rule that a suite must prove it leaves clean
evidence alone, not only that it catches a planted violation):

| Fixture | Kind | Rules exercised |
|---|---|---|
| `op-dialog-escape-overreach` | BUG | bounded-diagnostic-not-promoted; setup/action continuity |
| `op-empty-state-coverage-shortcuts` | BUG | natural-only conditional state; passive-observation binding; ancestor-remapping review |
| `op-retest-clean` | CLEAN control | all five, in their admissible forms — must not be flagged |
| `op-mixed-package-partial` | BUG (mixed) | passive-observation binding on one operation; the other operation fully admissible — per-operation attribution |
| `op-human-walkthrough-clean` | CLEAN control (human-sourced) | all five, in their human-sourced admissible forms — a structured self-report, an honest BLOCKED, a played-and-heard media record — must not be flagged |
| `op-human-signature-only` | BUG (mixed, human-sourced) | setup/action continuity + passive-observation binding on one operation; passive-observation binding alone on another; ancestor-remapping review on a third; one operation fully admissible — per-operation attribution |

### Human-sourced packages

`op-human-walkthrough-clean` and `op-human-signature-only` exercise
[`references/human-verification-walkthrough.md`](../../../.claude/skills/a11y-test/references/human-verification-walkthrough.md),
the reference for how a person — not a machine collector — produces
operation evidence. The same five admissibility rules apply, scored against
the human-sourced fields the reference specifies (`before`/`action`/`observed`
for Shape 1, `played`/`heard`/`seen`/`adequacy` for Shape 2's attended-media
packages; Shape 2 is read by rules 1, 3 and 4 only — it has no locus and no
target, so rules 2 and 5 are marked not applicable in the reference).
`op-human-signature-only` carries three under-specified records beside one
admissible operation: the canonical "I checked it; it's fine" (rules 2 + 4),
a menu listing offered as audio-description evidence (rule 4), and a nested
option reported from the combobox owner with no session, no locus, a bare
visual read, and no mapping (rules 2 + 4 + 5, the same set the suite's
precedent attaches to that shape). No sixth rule is invented for any of them.

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
presence. Rule *selection* stays the model's semantic judgment; a naive
pattern-matching scorer could never make that call. What `a11y-test`
SKILL.md's Structured disposition block adds is a fenced yaml block every
review closes with, so *reporting* the judgment already made is mechanical —
the same split `score_acr.py` uses for the ACR yaml block.
`ollama/score_operation_evidence.py` checks that block against each fixture's
`expected_admissibility`, `expected_dispositions`, `must_catch[]`,
`rules_violated_must_be_empty_for`, and `expected_verdict_must_not`, and fails
a review that fires any rule outside `must_catch` (over-flagging is a miss,
not thoroughness); it is
detector output, not verdict authority — same routing rule as every other
rule-based scorer in this bundle.

**Reproduce:**

```bash
python3 ollama/run_benchmark.py opevidence <model> <fixture-id>
python3 ollama/score_operation_evidence.py <response.json> <metadata.yaml>
```

Zero model rows as of 2026-09-02 (calibration lane).
