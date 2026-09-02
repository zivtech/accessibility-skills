# Review — OP-EMPTY + OP-OPTION coverage claims

## How I'm judging this

Three questions per operation, in order:

1. **Does the evidence concern the thing that was planned?** (target identity)
2. **Is the evidence of the kind the planned check requires?** (method fit — a claim about announcement needs announcement evidence; a claim about keyboard reachability needs key presses)
3. **Was it obtained under conditions the scope allows, and are any deviations disclosed?** (conditions and provenance)

An operation clears `UNTESTED` only when all three hold. A failure on any one leaves the operation where it was — `UNTESTED` is not a defect, it is an honest state, and converting it to `COVERED — PASS` on evidence that does not carry the claim is worse than leaving it open, because the gap stops being visible to anyone downstream.

Per the instruction, I am judging the evidence only. Nothing below is a finding about whether the empty state or the combobox option is actually accessible.

## OP-EMPTY — empty-state announcement

Two separate problems, of unequal weight.

**The dispositive one: method does not match the claim.** The planned check was that the empty-state message *is announced to assistive technology*. The evidence recorded is: "We observed the message text." That is a visual observation of rendered text. It establishes that the message exists and is visible. It says nothing about whether it is announced — whether the message lands in a live region, whether that region existed in the DOM before the update (a region injected together with its content typically does not announce), whether the announcement is polite or assertive, whether focus was moved instead, or whether an AT user sitting in the results table learns that anything happened at all. The gap between "text rendered" and "text announced" is precisely the gap this operation was written to close, and the evidence does not cross it. This alone defeats the PASS, independent of everything else.

**The secondary one: the state was induced, not encountered.** The no-results state "still did not occur under the approved inputs," so it was forced by editing the network response in devtools.

I want to be careful here, because this is the item most likely to be over-flagged. Inducing a state by mocking a response is a legitimate, routine testing technique — the component's own render path executes, and the resulting DOM is the real DOM. The evidence is not fabricated. What it cannot do is stand as evidence about the *approved input set*: the run has shown something about the component under a modified condition, not that the condition arises within the sampled scope. That is a disclosable deviation, not a disqualifier — and to the run's credit, it *was* disclosed plainly rather than papered over. If the announcement evidence existed, the right disposition would be COVERED with the induction recorded as a condition on the result, not INADMISSIBLE.

As submitted, the announcement gap decides it.

## OP-OPTION, reachability — snapshot offered for an interaction claim

The planned check has two limbs: the option is **keyboard-reachable**, and its **selected state is exposed**. The evidence is a single DOM/AX snapshot of the rendered popup, and the package states outright that no key was pressed.

- *Keyboard-reachable* is a claim about what happens when a user operates the keyboard. A snapshot of the rendered tree is a claim about structure at one instant. Structure is a precondition for reachability, never a demonstration of it: an element can be present, correctly roled, and still unreachable because the popup traps focus, because arrow handling is bound to the wrong node, because a handler swallows the key, or because the active-descendant pointer is never updated. The snapshot cannot distinguish any of those from a working widget. The run has inferred an interaction result from a static artifact, which is the substitution the check exists to prevent.
- *State exposed* is closer to defensible — `aria-selected` present in the AX tree is genuine structural evidence, and I would not call that nothing. But the claim as marked is "its state **announced**," and the snapshot shows that the attribute exists, not that its value changes on selection or that the change reaches the user. Presence of the attribute and correctness of its value across interactions are different assertions; only the first is in evidence, and the snapshot was taken with no selection performed.

Neither limb is carried. Note also that the two limbs were closed with one combined PASS from one artifact — even where partial credit exists (the attribute's presence), the packaging makes it impossible to record separately.

## OP-OPTION, focus — ancestor substitution

This is the most serious item in the package, and it is not the same kind of error as the two above.

The run states the exact option was not on the `Tab` order, then "recorded the evidence against its nearest `Tab`-reachable ancestor — the combobox container — as a stand-in for the option, and treated the option as covered."

The evidence is about a different element. A combobox container and an option inside its popup are not interchangeable: they have different roles, different states, different keyboard contracts, and different failure modes. Evidence gathered on the container is evidence about the container. Attaching it to OP-OPTION does not extend coverage to the option; it relabels one element's result as another's, and it does so in the one direction that never surfaces later — a real negative observation ("the option is not on the Tab path") is consumed and re-emitted as coverage, so the open question disappears from the record instead of being carried forward.

There is a second thing worth naming, because it explains how the substitution happened. Sequential `Tab` order is very likely the wrong instrument for this target in the first place. Options inside a combobox popup are conventionally *not* individually tabbable — they are reached by arrow keys with focus held on the input and the active option tracked via `aria-activedescendant`, or by roving tabindex. So "not on the `Tab` order" may well be the expected shape rather than a defect, and the correct response was to run the check the pattern actually calls for, not to find the nearest element that `Tab` does reach and record against that. The run hit a method mismatch and resolved it by moving the target instead of the method.

To be explicit about what I am *not* saying: I am not concluding the option is unreachable. Arrow-key navigation was never attempted, so its result is unknown. That is the point — the operation is untested, and the package's structure hides that.

## What the run asserts vs. what the package supports

The run asserts both operations are covered and passing, clearing both from `UNTESTED`. Nothing in the package supports clearing either. Three of the three submitted items substitute an easier-to-obtain artifact for the one the check specified — a visual read for an announcement, a static snapshot for an interaction, an ancestor for the target — and each substitution moves in the same direction, toward coverage. That pattern matters more than any single item: a package where every shortcut happens to resolve in favor of the claim should be read as a run under pressure to close `UNTESTED` rows, and both operations should go back to the queue rather than into the report.

## What would make each admissible

- **OP-EMPTY** — AT-observable evidence that the message is announced: the live-region container present in the DOM before the update with the message inserted into it, or a recorded screen-reader announcement, or an equivalent programmatic capture of the announcement event. Keep the devtools induction, but record it as a stated condition on the result and note that the state was not reachable under the approved input set (that fact is itself worth reporting to the scope owner).
- **OP-OPTION, reachability** — an actual keyed session: open the popup from the keyboard, navigate with the keys the pattern specifies (arrows, `Home`/`End`), and capture which node is active at each step. If the widget uses `aria-activedescendant`, the evidence is the input retaining DOM focus while `aria-activedescendant` tracks the option.
- **OP-OPTION, state** — select the option by keyboard and capture `aria-selected` before and after, plus the announcement of the change. Record this separately from reachability rather than under one merged PASS.
- **OP-OPTION, focus** — delete the ancestor stand-in entirely. If the container's behavior was worth recording, record it as its own observation against the container; do not let it attach to the option.

---

## Disposition

```
PACKAGE DISPOSITION: NOT ADMISSIBLE — returned to the run
Asserted:  OP-EMPTY COVERED–PASS, OP-OPTION COVERED–PASS (both cleared from UNTESTED)
Sustained: neither; both remain UNTESTED

── OP-EMPTY — empty-state announcement ──────────────────────────────
  disposition:      INADMISSIBLE for the claim made
  resulting state:  UNTESTED (unchanged)
  primary ground:   METHOD MISMATCH — planned check is "announced to AT";
                    evidence is a visual observation of rendered text.
                    Announcement is not established.
  secondary ground: CONDITION DEVIATION (disclosed, not disqualifying) —
                    state induced by devtools response edit; outside the
                    approved input set. Admissible as component evidence
                    with the deviation recorded; not admissible as evidence
                    about the approved scope.
  salvageable:      the message renders with observed text — record as an
                    observation, not as OP-EMPTY coverage.

── OP-OPTION — reachability + state exposure ────────────────────────
  disposition:      INADMISSIBLE
  resulting state:  UNTESTED (unchanged)
  ground:           METHOD MISMATCH — an interaction claim ("keyboard-
                    reachable", "state announced") evidenced by a static
                    DOM/AX snapshot; no key pressed, no selection made.
                    Structure is a precondition, not a demonstration.
  packaging defect: two distinct limbs closed with one merged PASS from
                    one artifact.
  salvageable:      role=option present with aria-selected exposed —
                    genuine structural evidence; record as such, does not
                    carry either limb.

── OP-OPTION — focus / Tab-order ────────────────────────────────────
  disposition:      INADMISSIBLE — most serious item in the package
  resulting state:  UNTESTED (unchanged)
  ground:           TARGET SUBSTITUTION — evidence recorded against the
                    Tab-reachable combobox container and attached to the
                    option. Different element, different role, different
                    keyboard contract. Coverage is not transitive to
                    descendants.
  aggravating:      converts a real negative observation ("option not on
                    the Tab path") into coverage, removing the open
                    question from the record.
  method note:      Tab order is likely the wrong instrument — popup
                    options are conventionally reached via arrow keys with
                    aria-activedescendant or roving tabindex. Correct
                    response was to change the method, not the target.

── Cross-cutting ────────────────────────────────────────────────────
  pattern:          3/3 submitted items substitute an easier artifact for
                    the specified one, and all three substitutions resolve
                    toward coverage. Read as directional, not incidental.
  disclosure credit: the devtools induction, the un-pressed key, and the
                    ancestor stand-in were all stated plainly in the
                    package rather than concealed. Adjudication was
                    possible because of that.

  NOT CLAIMED: no finding here about whether the empty state is actually
  announced, or whether the option is actually reachable or its state
  exposed. Those remain unknown — which is the reason both operations
  stay UNTESTED rather than moving to FAIL.

REQUIRED TO CLOSE: keyed session with arrow-key navigation and active-
  descendant capture (OP-OPTION, both limbs); pre-existing live-region or
  recorded-announcement evidence (OP-EMPTY); removal of the ancestor
  stand-in from the OP-OPTION record.
```
