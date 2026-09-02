# Review — OP-CLOSE evidence package (dialog dismiss via Escape)

## What the package claims vs. what it contains

The operation as planned is narrow and specific: **with the dialog open, press `Escape`; expect dismissal and focus return to the row-action trigger.** The claim entered against it is `FAIL — WCAG 2.1.2 No Keyboard Trap`.

The action record does not contain that operation. It contains a different one, run in a different session, against a different page state:

| Planned | Actually recorded |
|---|---|
| Dialog open | Session B was a *fresh page load, dialog not yet open* |
| Press `Escape` | Six `Tab` presses from the filter combobox |
| Observe dismissal + focus return | Observed focus stagnation in the page header |

The package states plainly: **"No `Escape` was pressed."** The planned interaction was never executed. Everything downstream of that — the diagnostic conclusion, the SC citation, the disposition — rests on an observation of a different interaction on a different page state.

## Why this is not a recoverable gap

Three separate defects, any one of which would be disqualifying on its own.

**1. Setup/action state discontinuity.** Session A established the precondition the operation requires (dialog open, focus on the dialog heading). Session B discarded it — fresh load, dialog closed. The two records cannot be composed into one operation: nothing in the package shows the dialog was ever open at the moment the recorded keystrokes were delivered. The setup record is therefore inert; it establishes a state that no recorded action ever acted on.

**2. The observation does not support the cited criterion.** WCAG 2.1.2 (No Keyboard Trap) is an *exit* criterion: it requires demonstrating that focus **moved into** a component and **could not be moved out** by standard means. The recorded evidence shows focus failing to **advance into** the dialog region from the header. That is the inverse relationship. Whatever the header stagnation is — a non-advancing custom widget, a scripted focus loop, an unreachable region, or simply a control that swallows `Tab` — it is an entry/operability observation, closer to 2.1.1 or 2.4.3 territory, and it is not on the dialog at all. Even reading the run's own words at face value ("focus could not progress past the header"), the trap it describes is in the *header*, not in the operation's target. The evidence and the claim are about different components.

**3. No exit-path diagnostic was run.** The package concedes it: no `Escape`, no exit-path test, no trace of the dialog's focus behavior. 2.1.2 requires the exhaustion of standard exit mechanisms — `Tab`, `Shift+Tab`, `Escape`, and any documented alternative — before a trap can be asserted. Zero of those were attempted at the observed location. This is not thin evidence for the claim; it is an absence of any evidence for the claim's central element.

## The attachment does not rescue it

One DOM snapshot of the header showing an unchanged focused element across six presses is real data, honestly captured, and it may well be worth a finding **of its own** — under its own operation, with its own planned interaction. But it is a snapshot of the header, not the dialog, and a single unchanging-focus observation is also consistent with benign explanations the package never ruled out (a single-tab-stop composite widget behaving to spec, a lazily-rendered region, a still-settling page). Without a `Shift+Tab` or `Escape` probe at that location, even the header finding is undercooked.

## Reading the run charitably

There is a plausible reconstruction where the tester meant well: they tried to reach the dialog, hit a wall, and reported the wall. The problem is that the wall was recorded against a slot reserved for a different question, under an SC that does not describe it, with the operation's own interaction never attempted. That is a scoping and bookkeeping failure, not a judgment call — and it is the kind that inflates a report, because a reader scanning dispositions sees "dialog fails 2.1.2" and infers a trapped user in a modal, which no one has shown to exist.

Note also what I am **not** saying: I am not saying the dialog dismisses correctly on `Escape`, or that focus returns to the trigger, or that the header behaves acceptably. All three remain unknown. Rejecting this package leaves the underlying component entirely untested — which is precisely the state the record should reflect.

## Where my confidence is lower

The one place I hedge: if the run's actual intent was "the dialog cannot be reached at all by keyboard, therefore the close operation is unreachable," that would be a coherent (though differently-cited) claim — but the package would still need to show that the row-action trigger itself is unreachable, and Session A demonstrates the *opposite*: the dialog was successfully opened from the row-action menu. The run's own setup record contradicts the reachability reading of its action record. So even the most generous reconstruction fails on the package's internal evidence.

## Required to make the operation admissible

1. Re-run OP-CLOSE as planned, in a single continuous session: open the dialog from the row action, confirm focus lands inside it, press `Escape`.
2. Record the post-`Escape` state: dialog present/absent, and the terminal focus element (expected: the row-action trigger).
3. If the dialog does not dismiss, run the full exit-path diagnostic before any 2.1.2 assertion — `Tab` cycle, `Shift+Tab` cycle, `Escape`, plus any documented mechanism — and capture the focus trace across the cycle, not a single snapshot.
4. File the header stagnation separately as its own operation with its own planned interaction and its own probes; do not attach it to OP-CLOSE.

---

## Disposition

```
operation_id:        OP-CLOSE
claim_reviewed:      FAIL — WCAG 2.1.2 No Keyboard Trap
disposition:         INADMISSIBLE — REJECT
resulting_status:    NOT TESTED (operation not executed)
claim_action:        WITHDRAW — claim is not supported by any evidence in the package

primary_defects:
  - operation_not_executed: planned interaction (Escape with dialog open) never performed;
    package states "No Escape was pressed"
  - state_discontinuity: setup (Session A, dialog open) and action (Session B, fresh load,
    dialog closed) are separate sessions; no recorded action occurred in the required state
  - evidence_claim_mismatch: observation is failure to enter the dialog region from the header;
    2.1.2 requires demonstrated failure to exit an entered component — inverse relationship
  - wrong_target: observed behavior is located in the page header, not in the dialog under retest
  - missing_required_diagnostic: no exit-path probe (Tab / Shift+Tab / Escape / documented
    mechanism) at the observed location; single DOM snapshot only

salvageable_material:
  - header focus-stagnation observation (6 x Tab, focus unchanged) — re-file as its own
    operation; requires Shift+Tab and Escape probes before any SC is cited

underlying_component_verdict: UNKNOWN — dialog Escape-dismissal and focus-return behavior
                              remain untested by this package

required_before_resubmission:
  1. single continuous session: open dialog -> confirm focus inside -> press Escape
  2. record post-Escape dialog presence and terminal focus element
  3. if no dismissal: full exit-path diagnostic with focus trace before asserting 2.1.2
  4. file header stagnation as a separate operation
```
