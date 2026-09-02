# Admissibility review — OP-CLOSE + OP-EMPTY + OP-OPTION

Scope note: what follows judges the *evidence package* — whether each operation's
evidence is admissible for the claim it carries — not the accessibility of the
dialog, the results table, or the filter combobox.

## Rule-by-rule pass

### 1. A bounded diagnostic is not a conclusion — `bounded_diagnostic_not_promoted`

The only bounded diagnostic in the package is the `focus_stagnation_observed`
note attached to OP-CLOSE, carried over from an earlier probe. The package
holds it at the right altitude: it is explicitly retained as a **collector
observation only** and explicitly **not** offered as a 2.1.2 keyboard-trap
conclusion. Nothing in the OP-CLOSE claim leans on it — the PASS rests on the
separate Escape exit-path trace (Escape pressed, dialog dismissed, focus
returned to the row-action trigger), which is exactly the trace the rule
requires before an exit-path question can be decided at all.

This is the non-violating shape of the rule: the stagnation note neither
inflates into a finding nor forces the operation to `BLOCKED`, because a
conclusive exit-path trace exists alongside it. **No violation.**

### 2. Setup and action must be continuous — `setup_action_continuity`

OP-CLOSE is the only operation with a setup/action pair to check. One session,
`load+settle` ok; the setup terminates with focus on the dialog's initial focus
(its heading); the Escape action's `before` identity is that same locus, in the
same session. Starting identity equals the immediately preceding setup's
terminal identity, with no cross-session composition. **No violation.**

OP-OPTION's `Tab` → `ArrowDown` sequence is a single continuous keypress trace
rather than a setup-in-one-session/action-in-another composition, so the rule
is satisfied there too.

### 3. Conditional states are natural-only — `natural_only_conditional_state`

OP-EMPTY is the conditional state. The no-results state did not occur naturally
under the approved input set, and the run reports **no synthetic induction** —
no edited response, no forced state. The run correspondingly declines to claim
coverage and leaves the operation `UNTESTED`, recording the admissible path
(revisit when the state arises under an approved input).

Declining to test is the compliant outcome here; the rule is violated by
inducing the state, not by leaving it unreached. **No violation.**

### 4. Passive observations are bound, never standalone — `passive_observation_binding`

OP-OPTION carries a DOM/AX snapshot. It is (a) bound to the causing action —
the `aria-selected` transition was observed *after* the activating key, not
merely read out of a rendered tree — (b) on the source allowlist, and (c)
explicitly **not** offered as standalone reachability proof; reachability is
carried by the attached real keypress trace instead. That is the bound-support
shape the rule permits. **No violation.**

No other operation submits a passive observation.

### 5. No silent ancestor remapping — `ancestor_remapping_review`

OP-OPTION's target is a descendant of a composite (the filter combobox), so the
option is not itself on the focus path — precisely the situation the rule
governs. The run does not substitute the nearest reachable ancestor and call it
the target. It reaches the option through the composite's **reviewed,
separately frozen owner/descendant mapping** (documented owner + navigation
model), and the trace walks that model explicitly: `Tab` to the combobox owner,
`ArrowDown` to the option. The remapping is disclosed and reviewed, not silent.
**No violation.**

## Dispositions

- **OP-CLOSE → PASS.** Continuous setup/action plus a conclusive exit-path
  trace decide the operation's own predicate. The retained stagnation note does
  not pull it to `BLOCKED`, because the trace that would decide it is present.
- **OP-EMPTY → UNTESTED.** No admitted observation bears on the operation. Not
  `BLOCKED`: there is no bounded collector observation *about* OP-EMPTY
  standing without its deciding trace — there is simply nothing.
- **OP-OPTION → PASS.** Reviewed owner/descendant mapping plus a real keypress
  trace and a bound state observation decide the operation's predicate.

`rules_violated` is empty, so `admissibility` is `ACCEPT`.

## Where this is weakest

Two things I am explicitly *not* concluding. First, ACCEPT is a statement about
the evidence package, not about the component: OP-CLOSE and OP-OPTION passing
says nothing about the dialog's or the combobox's overall conformance. Second,
OP-OPTION's PASS is bounded by what the trace actually exercised — one option
reached along one documented path, with a state transition observed after the
key. The snapshot is support; it is not announcement evidence, and no screen
reader output was captured. Those boundaries are recorded below rather than
smoothed into the PASS.

```yaml
admissibility: ACCEPT
dispositions:
  OP-CLOSE: PASS
  OP-EMPTY: UNTESTED
  OP-OPTION: PASS
rules_violated: {}
claim_boundary: "OP-CLOSE: the admitted evidence establishes that from the dialog's initial focus, in the same session as the setup that produced it, Escape dismissed the Details dialog and returned focus to the row-action trigger; it leaves undecided any other exit affordance (close button, click-outside), the dialog's behavior from other internal focus positions, and any 2.1.2 keyboard-trap question generally - the retained focus_stagnation_observed note is a bounded collector observation, not a conformance outcome, and is not carried into this PASS. OP-EMPTY: no admitted observation bears on the empty-state announcement; the state did not occur naturally under the approved input set and was not induced, so reachability of the state and anything about how it announces remain entirely undecided, revisitable only when the state arises under an approved input. OP-OPTION: the admitted evidence establishes that the option is keyboard-reachable via the composite's reviewed, separately frozen owner/descendant mapping (Tab to the combobox owner, ArrowDown to the option) and that its aria-selected state transitioned after the activating key; the bound DOM/AX snapshot is support for that action only. It leaves undecided what a screen reader actually announces on that transition (no announcement evidence was captured), the reachability of the composite's other descendants, and any alternative navigation path to the option."
```
