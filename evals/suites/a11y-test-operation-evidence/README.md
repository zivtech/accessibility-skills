# a11y-test-operation-evidence eval suite

**Status: shell — no fixtures yet.** This suite is scaffolding for a lane
that measures whether an operation-evidence claim (a retest hitting a
specific interactive target, a keyboard trace, a passive DOM/AX observation)
meets the evidence-quality rules the `a11y-test` skill states, rather than
whether the underlying interaction itself is accessible. It is a sibling of
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

## Fixture format (once populated)

Every fixture will follow this bundle's existing triplet convention, matching
`evaluation-report` and `a11y-planner`:

- `fixtures/<id>.md` — the operation description + evidence package, sent to
  the model verbatim.
- `fixtures/<id>.metadata.yaml` — machine-checkable expectations, never sent.
- `rubrics/<id>.rubric.yaml` — dimension tiers and adjudication notes, never
  sent. See `RUBRIC_TEMPLATE.md` in this directory for the shape.

## Why this is a shell, not a suite

The rules above describe evidence-quality checks for accessibility retest
operations in general — they are not tied to any one engagement or product.
Populating this suite with real fixtures is separate follow-on work; this
shell exists so the suite has a stable location and a documented shape
before that work lands, rather than the fixtures inventing their own
ad hoc home.

**Reproduce:** nothing to run yet — no fixtures, no scorer. When the first
fixture lands, its own commit will state the exact run command.
