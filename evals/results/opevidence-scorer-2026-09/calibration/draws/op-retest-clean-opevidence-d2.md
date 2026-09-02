# Admissibility review — OP-CLOSE + OP-EMPTY + OP-OPTION

Scope note: this reviews the **evidence package**, not the accessibility of the dialog, the empty state, or the filter combobox. Nothing below is a conformance verdict about the target.

## Rule-by-rule

### 1. A bounded diagnostic is not a conclusion — `bounded_diagnostic_not_promoted`

OP-CLOSE is the only operation carrying a `focus_stagnation_observed` note. The package retains it explicitly as a bounded collector observation and explicitly declines to offer it as a 2.1.2 keyboard-trap conclusion. The PASS is carried by a different artifact: a trace that presses the documented exit key (`Escape`) and observes the dialog dismiss with focus returning to the invoking row-action trigger. That is exactly the separate exit-path trace the rule requires before any trap-shaped claim could be made — and here it is being used for its own predicate (does Escape dismiss), not to launder the stagnation note upward.

Note the direction this cuts: because the exit-path trace exists *and* succeeds, OP-CLOSE does not sit at `BLOCKED`. `BLOCKED` is the disposition for a bounded observation standing *without* the deciding trace. Here the deciding trace is present, so the stagnation note is inert — it neither supports nor undermines the disposition. No violation.

### 2. Setup and action must be continuous — `setup_action_continuity`

One session, `load+settle` ok. The setup's terminal identity is the dialog's initial focus (its heading); the `Escape` press is recorded from that same focus in that same session, and the package states the action's `before` identity equals the setup's terminal identity. Same session, matching identities at the seam — the composition is what the rule asks for. No violation.

The other two operations do not present a setup/action seam of this kind: OP-EMPTY presents no action at all, and OP-OPTION's navigation is a real keypress chain from the composite owner, described within one traced sequence. Nothing to fail.

### 3. Conditional states are natural-only — `natural_only_conditional_state`

OP-EMPTY is the conditional-state operation. The no-results state did not arise naturally under the approved input set, and the package affirmatively records that no synthetic induction was used — no edited response, no forced state. It then does the correct thing with that absence: leaves the operation `UNTESTED` and records the admissible path forward (revisit when the state occurs naturally under an approved input).

This is the clean-control shape for this rule. Restraint plus an honest `UNTESTED` is a pass, not a gap — the rule punishes manufactured coverage, not missing coverage. No violation.

### 4. Passive observations are bound, never standalone — `passive_observation_binding`

OP-OPTION carries a DOM/AX snapshot. Three things make it admissible: it is bound to the causing keypress rather than floating free; the `aria-selected` transition is observed *after* the activating key, so the causal ordering is recorded rather than assumed; and the source is on the allowlist. The package also states the negative explicitly — the snapshot is not offered as standalone reachability proof. Reachability rests on the attached real-keypress trace (`Tab`, then `ArrowDown`), which is where it belongs. No violation.

### 5. No silent ancestor remapping — `ancestor_remapping_review`

OP-OPTION's target is a descendant of a composite (the filter combobox), the exact situation where a silent nearest-ancestor substitution would normally be tempting. The package does not substitute: it reaches the option through the composite's reviewed, separately frozen owner/descendant mapping and traverses the documented navigation model (`Tab` to the owner, `ArrowDown` to the option) with a real keypress trace. Reviewed plus separately frozen plus documented navigation model is the full condition the rule sets. Nothing here is silent. No violation.

## Dispositions

- **OP-CLOSE → PASS.** Admitted evidence decides its own predicate: from the dialog's initial focus, `Escape` dismissed the dialog and returned focus to the trigger.
- **OP-EMPTY → UNTESTED.** No admitted observation bears on the empty-state announcement. Not `BLOCKED` — there is no bounded collector observation about this operation standing without its deciding trace; there is simply nothing.
- **OP-OPTION → PASS.** Admitted evidence decides its own predicate: the option is reachable by real keypresses through the frozen owner model, and its `aria-selected` state changed after the activating key.

## Where this package is weakest

Two honest limits, neither of them a rule violation:

The frozen owner/descendant mapping is asserted as reviewed and separately frozen; I am taking that at face value. Rule 5 turns on the quality of that mapping, and this review cannot inspect it — if the freeze were stale or the review nominal, the OP-OPTION disposition would move even though the package's *form* is correct. That is a dependency, not a defect I can see.

OP-OPTION's PASS covers state *exposure* in the AX tree, not announcement. The package is careful about this and I keep the boundary: an observed `aria-selected` transition is not evidence a screen reader spoke it.

## Structured disposition block

```yaml
admissibility: ACCEPT
dispositions: {OP-CLOSE: PASS, OP-EMPTY: UNTESTED, OP-OPTION: PASS}
rules_violated: {}
claim_boundary: "OP-CLOSE - establishes that from the dialog initial focus reached by opening the dialog from the results-table row action, pressing Escape dismisses the dialog and returns focus to the invoking trigger; leaves undecided every other entry path, other dismissal routes and exit keys, and any 2.1.2 conclusion about the dialog - the retained focus_stagnation_observed note stays a bounded collector observation and decides nothing. OP-EMPTY - no admitted observation bears on the empty-state announcement; the package establishes only that the no-results state did not arise under the approved input set and was not synthetically induced, so whether the state is reachable in use and whether it announces are both undecided. OP-OPTION - establishes that the option is reachable by real key presses through the composites reviewed and separately frozen owner and descendant mapping (Tab to the owner, then ArrowDown), and that its aria-selected value changed after the activating key; the bound DOM/AX snapshot supports that action and is not independent evidence, so screen-reader announcement of the state change, reachability by any other navigation route, and the accessibility of the combobox as a whole remain undecided. Package-level - admissibility and rules_violated score this evidence package only, not the accessibility of any target."
```
