# Admissibility review — OP-CLOSE (dialog dismiss via Escape)

## What the package claims vs. what it contains

The planned operation is narrow and specific: **with the dialog open, press `Escape`**; expected result — dialog dismissed, focus returns to the row-action trigger. The run files `FAIL — WCAG 2.1.2 No Keyboard Trap`.

Nothing in the submitted evidence touches that interaction. `Escape` was never pressed. No trace of the dialog's own focus behavior was captured. The action record is a *tabbing sweep from the page's filter combobox* in a session where **the dialog was never opened at all**.

## Rule-by-rule

### 1. Bounded diagnostic not promoted — **VIOLATED**

The only observation in the package is a `focus_stagnation_observed` note: six `Tab` presses, focus did not leave the page header. The diagnostic conclusion promotes that directly to "the user is stuck… Recorded as a keyboard trap — **WCAG 2.1.2 FAIL**."

That is the textbook promotion the rule forbids. Stagnation on a forward-traversal probe is a bounded collector observation. A 2.1.2 conclusion requires a separate trace that attempts the documented exit — press `Escape` (or the documented exit keys) and show focus cannot leave. The package states explicitly that no `Escape` was pressed and no exit-path diagnostic was run. There is no trap conclusion available here, and stagnation alone is neither a trap nor a conformance failure.

### 2. Setup / action continuity — **VIOLATED**

- Setup: **Session A**, `load+settle` ok, dialog opened from the row-action menu, terminal focus = the dialog's initial heading.
- Action: **Session B**, *fresh page load, dialog not yet open*, starting locus = the filter combobox at the top of the page.

Two independent failures of the same rule: different session, and a `before` identity (filter combobox) that is not the setup's terminal identity (dialog initial heading). The setup that would have put the run in position to test OP-CLOSE and the action that was actually performed do not compose into evidence about the planned operation. Session B's traversal is an observation about the page header in a no-dialog state — a different locus in a different page state.

### 3. Natural-only conditional state — **not violated**

OP-CLOSE is not a conditional state, and nothing was induced synthetically. The Session B state (dialog not open) is an ordinary fresh load, not a forced or edited state. This rule is not engaged; charging it here would be over-reach.

### 4. Passive observation binding — **not violated**

The one attachment is a DOM snapshot of the header region showing the focused element did not change across the six presses. That snapshot is bound to its causing action (the `Tab` presses) and sits in the same session as them — it is not offered standalone as proof of keyboard-reachability or announcement. It is admissible *in form* as support for the header observation.

Its problem is not binding; it is that the action it is bound to is the wrong action for OP-CLOSE. A correctly-bound snapshot of an off-target action does not become on-target evidence. (Source allowlist is not stated in the package. I am not charging a violation on an unstated field.)

### 5. Ancestor remapping review — **not violated**

No owner/descendant substitution occurred. The header is not an ancestor of the dialog standing in for an unreachable target; it is simply where a different traversal stopped. This is a continuity failure, not a silent nearest-ancestor remap. Charging this rule would mislabel the defect.

## Disposition reasoning — why not `BLOCKED`

The tempting call is `BLOCKED`: a bounded stagnation observation exists, and the deciding trace is missing. That is wrong here, and the distinction is the whole point of this package.

`BLOCKED` requires an **admitted** bounded observation **about that operation**. The stagnation note fails admissibility on the continuity rule — it was collected in a different session, from a different starting locus, with the dialog not open. So it is not an admitted observation *about OP-CLOSE*; it is inadmissible for this operation entirely. Rejected evidence never moves an operation. With no admitted observation bearing on OP-CLOSE, and no prior recorded state cited in the package, the operation takes **`UNTESTED`**.

Two rule violations, so `admissibility: REJECT`.

## What this review is not saying

Rejecting the package says nothing about the dialog. `Escape` may dismiss it correctly with clean focus return, or may genuinely trap a keyboard user — this run produced no evidence either way, and a reviewer reading "REJECT" as "the dialog is fine" would be reading the wrong axis. Likewise, the header stagnation may be a real problem worth its own planned operation with a proper exit-path trace; it is simply not evidence about OP-CLOSE, and it is not a 2.1.2 finding as submitted.

```yaml
admissibility: REJECT
dispositions:
  OP-CLOSE: UNTESTED
rules_violated:
  OP-CLOSE:
    - bounded_diagnostic_not_promoted
    - setup_action_continuity
claim_boundary: "OP-CLOSE: no admitted evidence bears on the operation. The Session A setup (dialog open, focus on dialog heading) is never continued by an action, and the Session B observation (six Tab presses from the filter combobox not advancing past the page header, dialog never opened) is inadmissible for this operation on setup/action continuity, so it establishes nothing about OP-CLOSE. The header DOM snapshot is correctly bound to its causing Tab presses but inherits that action's off-target locus. Left undecided: whether Escape dismisses the Details dialog, whether focus returns to the row-action trigger, and whether any keyboard trap exists in or around the dialog. The run's WCAG 2.1.2 FAIL claim is not carried forward — no exit-path trace was attempted, and focus stagnation on forward traversal is neither a trap nor a conformance outcome. Rejection scores the evidence package only and implies nothing about the dialog's actual accessibility. The header stagnation may warrant its own separately planned operation; it is not one in this package."
```
