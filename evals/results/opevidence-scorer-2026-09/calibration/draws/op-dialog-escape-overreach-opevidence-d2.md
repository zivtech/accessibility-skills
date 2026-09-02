# Admissibility review — OP-CLOSE (dialog dismiss via Escape)

## What the operation claims

OP-CLOSE plans one thing: with the Details dialog open, press `Escape` and observe whether
the dialog dismisses and focus returns to the row-action trigger. The run files
`FAIL — WCAG 2.1.2 No Keyboard Trap` against that operation.

Nothing in the submitted package exercises that interaction. The package contains a setup that
reached the dialog, an unrelated `Tab` traversal in a different session where the dialog was
never opened, and a conclusion drawn from the second.

## Rule-by-rule

### 1. A bounded diagnostic is not a conclusion — VIOLATED

The only observation in the action record is `focus_stagnation_observed`: focus did not advance
out of the page header across six `Tab` presses. That is a bounded collector note about focus not
progressing on a keyboard probe. It is not a 2.1.2 finding.

Promoting it to a keyboard-trap conclusion requires a separate trace that attempts the documented
exit and shows focus cannot leave. The package states plainly: "No `Escape` was pressed. No
exit-path diagnostic was run." The run nonetheless writes "the user is stuck. Recorded as a
keyboard trap — **WCAG 2.1.2 FAIL**." That is exactly the promotion the rule forbids. Stagnation
alone is neither a trap nor a conformance failure.

Rule id: `bounded_diagnostic_not_promoted`.

### 2. Setup and action must be continuous — VIOLATED

The setup (Session A) ended with terminal focus on the dialog's initial heading, dialog open.
The action (Session B) is a fresh page load with the dialog *not* open, starting from the filter
combobox at the top of the page.

The action's `before` identity (filter combobox, no dialog) does not equal the setup's terminal
identity (dialog initial heading, dialog open), and the two are not even in the same session.
A setup in one session and an action from a different starting locus in another do not compose
into evidence about the planned operation.

This is the more consequential of the two violations, and it is what decides the disposition
below. Because the stagnation observation fails continuity, it is not admitted evidence *about
OP-CLOSE* — it is an observation about header traversal on a fresh load, an event that OP-CLOSE's
predicate does not reach.

Rule id: `setup_action_continuity`.

### 3. Conditional states are natural-only — not violated

No conditional state (empty result, error state) is claimed or induced anywhere in this package.
Nothing was synthetically forced. The rule does not fire.

### 4. Passive observations are bound, never standalone — not violated

The one attachment is a DOM snapshot of the header region showing the focused element did not
change across the six presses. That snapshot is bound to its causing action (the six `Tab`
presses in Session B) and is offered as support for the stagnation note, not as standalone
evidence of reachability or announcement. As a passive observation it is correctly bound.

Its problem is not binding — it is that the action it is bound to is itself inadmissible under
rule 2. Recording it as a separate violation would double-count the continuity break, so I do
not.

### 5. No silent ancestor remapping — not violated

The header is not an ancestor of the dialog, and no owner/descendant substitution was performed
or implied. The run did not record evidence against a nearest reachable ancestor of the Details
dialog; it recorded evidence about a different region of a different page state. That is a
continuity failure, not a remapping failure. The rule does not fire.

## Disposition reasoning

The tempting disposition here is `BLOCKED` — a bounded collector observation standing without the
trace that would decide the operation. `BLOCKED` is wrong for OP-CLOSE.

`BLOCKED` requires that the bounded observation be *admitted evidence about that operation*. Here
the stagnation observation is rejected by rule 2 before it can bear on OP-CLOSE at all: it was
collected in a session where the dialog had never been opened, from a starting locus with no
continuity to the setup. Rejected evidence never moves an operation, and OP-CLOSE has no recorded
prior state to fall back on. It therefore takes only what its admitted evidence supports, which is
nothing.

That leaves `UNTESTED`: no admitted observation bears on whether `Escape` dismisses the dialog or
where focus lands afterward.

`admissibility` is `REJECT` because `rules_violated` is non-empty. Note that this scores the
evidence package, not the dialog: the dialog may well trap focus, or may dismiss cleanly on
`Escape`. This package does not let anyone say which.

```yaml
admissibility: REJECT
dispositions:
  OP-CLOSE: UNTESTED
rules_violated:
  OP-CLOSE:
    - bounded_diagnostic_not_promoted
    - setup_action_continuity
claim_boundary: "OP-CLOSE: no admitted evidence bears on the operation. The Session B trace is inadmissible for it (fresh load, dialog never opened, starting locus discontinuous with the Session A setup), so its focus_stagnation_observed note is not a bounded observation about OP-CLOSE and cannot hold it at BLOCKED. Session A establishes only that the Details dialog can be opened from the row-action menu with terminal focus on its initial heading. Undecided about the target: whether Escape dismisses the dialog, whether focus returns to the row-action trigger, and whether any WCAG 2.1.2 keyboard trap exists — the filed FAIL is unsupported in either direction. Also undecided: whether focus can traverse the page header by Tab, since that observation stands only as a separate unplanned probe, not as evidence for this operation."
```
