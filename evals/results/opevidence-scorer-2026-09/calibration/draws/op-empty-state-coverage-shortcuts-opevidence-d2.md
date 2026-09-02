# Admissibility review — OP-EMPTY + OP-OPTION coverage package

## What is being claimed

The run asserts that two previously `UNTESTED` operations are now covered and passing. Each claim rests on evidence that substitutes something cheaper for the thing the planned check actually required. Judging the evidence package, not the component: none of the three submitted items survives.

## OP-EMPTY — synthetically induced conditional state

The planned check is that the no-results state, *when it occurs*, is announced to assistive technology. The submitted evidence concedes the operative fact: "The no-results state still did not occur under the approved inputs." The run then edited the network response in devtools to force the state and recorded the rendered message.

This is the natural-only rule squarely. A conditional state stays `UNTESTED` until it occurs naturally under an approved input. Forcing an empty result set by rewriting the response shows that *if* the state is entered, the message renders — it does not show the state is reachable in use, which is exactly the gap that left OP-EMPTY untested in the first place. The devtools edit reproduces the render, not the condition.

Violation: `natural_only_conditional_state`.

A second, independent shortfall is worth naming even though the first already sinks the item: the planned predicate is *announcement to AT*, and the evidence is "we observed the message text." Observing rendered text is not evidence of announcement — that requires the AT-observable result (a live-region announcement, or a focus/AT observation), which was never captured. Even had the state occurred naturally, this evidence would not have decided the predicate. The `COVERED — PASS` marking is unsupported twice over.

Disposition: `UNTESTED`. Rejected evidence never moves an operation, and OP-EMPTY's recorded prior state was `UNTESTED`.

## OP-OPTION, reachability — a standalone DOM/AX snapshot

The submitted evidence is a snapshot of the popup showing `role=option` present with `aria-selected` exposed, and — explicitly — "No key was pressed to reach or select the option; the snapshot was taken from the rendered tree."

A passive DOM/AX observation is admissible only as support bound to the causing action. Here there is no causing action to bind it to. The snapshot establishes what markup exists in the rendered tree; it cannot establish that the option is **keyboard-reachable** (that needs the key press that reaches it and the observed focus result) and it cannot establish that its state is **announced** (that needs the AT-observable result of selecting it). The presence of `aria-selected` in the tree is an authoring fact, not an announcement.

The `PASS` marking converts a snapshot directly into a two-part interaction conclusion — the exact promotion the binding rule forbids.

Violation: `passive_observation_binding`.

## OP-OPTION, focus — silent ancestor substitution

The run states that the exact option was not on the `Tab` order, so it recorded evidence "against its nearest `Tab`-reachable ancestor — the combobox container — as a stand-in for the option, and treated the option as covered."

This is a silent nearest-ancestor substitution, admissible only through a reviewed, separately frozen owner/descendant mapping — the composite's documented owner and navigation model. No such mapping is cited, and nothing in the package indicates one was reviewed or frozen. Nearest-in-the-tree is not the same as documented-owner-of: in a combobox the container may or may not be the option's owner under the pattern's navigation model, and the point of freezing that mapping is that a reviewer, not the collector, decides.

Note also what the ancestor evidence would establish even if the mapping existed: that the *container* is `Tab`-reachable. That was never in doubt — the container's reachability is what made it the fallback. It says nothing about whether the option is operable from there.

Violation: `ancestor_remapping_review`.

## Package disposition

Three shortcuts, three rules, zero admitted observations. Both operations keep their recorded `UNTESTED` state — neither takes `BLOCKED`, because `BLOCKED` requires an admitted bounded collector observation about that operation to stand, and here nothing was admitted at all. Nothing in the package moves either operation, and `admissibility` is `REJECT` because `rules_violated` is non-empty.

Two things this review is *not* saying. It is not saying the empty-state message is inaccessible or that the option is unreachable — the evidence is silent on both, which is precisely the problem. And `REJECT` scores the evidence package; it is not a conformance outcome about the target.

What would make each claim admissible: for OP-EMPTY, an approved input that actually returns no results, plus an AT-observable announcement result bound to that query action. For OP-OPTION, a keyboard trace from the combobox to the option showing focus arriving and the selected state's observed result — or, failing direct reachability, a reviewed and separately frozen owner/descendant mapping for the composite, with the ancestor evidence bound through it.

```yaml
admissibility: REJECT
dispositions: {OP-EMPTY: UNTESTED, OP-OPTION: UNTESTED}
rules_violated:
  OP-EMPTY: [natural_only_conditional_state]
  OP-OPTION: [passive_observation_binding, ancestor_remapping_review]
claim_boundary: "OP-EMPTY: no admitted evidence; the devtools-forced empty result shows only that the message renders when the state is entered, and observed message text is not an announcement observation, so whether the no-results state is reachable under approved inputs and whether it is announced to AT both remain undecided; operation holds its prior UNTESTED. OP-OPTION: no admitted evidence; the standalone rendered-tree snapshot establishes only that role=option and aria-selected are authored in the markup, not that the option is keyboard-reachable or that its selected state is announced, and the combobox-container substitution — absent a reviewed, separately frozen owner/descendant mapping — is evidence about the container, not the option, so keyboard reachability and state exposure for the option remain undecided; operation holds its prior UNTESTED. Package-level: admissibility and rules_violated score this evidence package only and assert nothing about the accessibility of the empty-state message or the option."
```
