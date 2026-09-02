# Admissibility review — OP-EMPTY + OP-OPTION coverage claims

## Scope of this review

I am judging the **evidence package**, not the results table, the combobox, or the
option. Nothing below says the empty-state message is inaccessible or that the
option is unreachable. The question is narrower: does the submitted evidence
establish the coverage the run claims, so that two operations can leave
`UNTESTED`?

It does not. Every claim in the package is carried by a shortcut that the
operation-evidence rules name explicitly.

---

## OP-EMPTY — synthetic induction of a conditional state

The run states plainly what happened: the no-results state **still did not occur
under the approved inputs**. It was obtained by editing the network response in
devtools to return an empty result set.

That is the `natural_only_conditional_state` rule in its literal form. An empty
result is a conditional state — it exists only when a condition holds — so it
stays `UNTESTED` until it occurs naturally under an approved input. Forcing the
response does not clear the coverage gap; it changes what was measured.

What the forced render actually shows is narrow and worth stating precisely:
given an empty result payload, the empty-state message **renders**. That is a
real observation about the rendering path. It is not evidence that:

- the state is **reachable** under the approved input set (the run's own text
  says it is not — this is the second consecutive attempt that failed to reach
  it naturally); or
- the message is **announced** to assistive technology, which was the planned
  check. Nothing in the submission describes a live-region observation, a
  screen-reader capture, or any announcement evidence at all — only that "we
  observed the message text." Even if the state had occurred naturally, reading
  the text off the screen is not announcement evidence.

So OP-EMPTY fails on two levels: the state was induced rather than reached, and
the planned predicate (announcement) was never exercised. The first is the rule
violation; the second means that even a repaired natural occurrence would not
have supported the `PASS` as written.

The recorded prior state was `UNTESTED`. Rejected evidence never moves an
operation, so it stays `UNTESTED` — not `BLOCKED`. `BLOCKED` is reserved for an
*admitted* bounded collector observation about the operation; there is no
admitted observation here, and a devtools-forced render is not a collector
block.

**Rule violated:** `natural_only_conditional_state`.

---

## OP-OPTION — two independent shortcuts

The submission makes two separate claims about the same target, and each breaks
a different rule. They compound rather than substitute: repairing one would not
rescue the other.

### Reachability and state, from a DOM/AX snapshot alone

The package offers a DOM/AX snapshot of the popup showing `role=option` present
with `aria-selected` exposed, and marks the option "keyboard-reachable and its
state announced — PASS." The parenthetical is explicit that **no key was
pressed**; the snapshot was read off the rendered tree.

This is the `passive_observation_binding` rule. A DOM/AX snapshot is admissible
only as support bound to a causing action, and by itself is never evidence of
keyboard-reachability or of announcement. Both of the things the run concluded
are exactly the two things the rule names as out of reach for a standalone
snapshot.

The gap is not pedantic. A snapshot proves the node exists in the rendered tree
with certain attributes present. It cannot distinguish an option a user can
arrive at from one that is present but unreachable, and `aria-selected` being
*present in the tree* is a different fact from a state change being *announced
on selection*. Reachability requires the key press that reaches it; announcement
requires the key press and its observed result.

There is a second, quieter problem: the snapshot was taken of the popup, which
means the popup was open. The submission does not say how. If the popup was
opened by a script or by a means outside the documented interaction, the
snapshot is not even bound to an admissible causing action. I flag this as an
unresolved provenance question rather than a separate finding, because the rule
already rejects the snapshot on its own terms.

### Nearest-ancestor substitution

The run then records that the exact option was not on the `Tab` order, and that
evidence was recorded **against its nearest `Tab`-reachable ancestor — the
combobox container — as a stand-in for the option**, treating the option as
covered.

This is `ancestor_remapping_review`. The remapping was silent: there is no
reviewed, separately frozen owner/descendant mapping cited, no reference to the
composite's documented owner and navigation model. Evidence against the
container is evidence about the container.

Worth noting on the merits, and against the run's framing: for a combobox, the
option *not* being on the `Tab` order is the expected and correct design — APG
composites put a single stop in the tab sequence and move an active descendant
with arrow keys. The run treated "not on the `Tab` path" as an obstacle to work
around, when it is a signal that the option's reachability lives in a
**different navigation model** the package never exercised. The correct route
here is a frozen owner/descendant mapping plus an arrow-key trace, not a
substitution. That is a design observation about how the evidence should have
been gathered; it does not change the disposition.

**Rules violated:** `passive_observation_binding`, `ancestor_remapping_review`.

Since no admitted evidence bears on OP-OPTION, its recorded `UNTESTED` stands.

---

## Rules not violated

Stating these to bound the finding:

- `bounded_diagnostic_not_promoted` — no `focus_stagnation_observed`-class note
  appears anywhere in the package. The OP-OPTION focus item reports that the
  option is absent from the `Tab` order, which is a structural observation about
  the tab sequence, not a stagnation diagnostic being promoted to a trap
  conclusion. No promotion occurred.
- `setup_action_continuity` — the package submits no setup/action pair whose
  identities could be compared. No session boundaries or `before` identities are
  described. There is nothing to fail here; this is absence of the pattern, not
  a clean result on it.

---

## Disposition

Both operations were `UNTESTED` before this run and remain so. The run asserts
the opposite — that both are now covered and passing — and that assertion is the
core failure of the package: every shortcut taken (synthetic state, standalone
snapshot, ancestor stand-in) moves in the direction of clearing a coverage gap
that was not actually closed. The single most consequential consequence of
accepting this package would be that two untested targets would be recorded as
passing, which is worse than an honest gap.

`admissibility` is `REJECT` because `rules_violated` is non-empty. That is a
verdict on the evidence, not on the interface.

```yaml
admissibility: REJECT
dispositions:
  OP-EMPTY: UNTESTED
  OP-OPTION: UNTESTED
rules_violated:
  OP-EMPTY:
    - natural_only_conditional_state
  OP-OPTION:
    - passive_observation_binding
    - ancestor_remapping_review
claim_boundary: "OP-EMPTY: the devtools-forced response is inadmissible, so nothing is established about the empty state; the forced render shows only that the message renders given an empty payload, and leaves undecided whether the state is reachable under approved inputs and whether it is announced to assistive technology. OP-OPTION: the standalone DOM/AX snapshot and the combobox-container stand-in are both inadmissible, so nothing is established about the option; the snapshot shows only that a node with role=option and aria-selected is present in the rendered tree, and leaves undecided whether the option is reachable by its actual navigation model (arrow keys within the composite, not Tab) and whether its selected state is announced on change. No operation is BLOCKED: there is no admitted bounded collector observation about either one, so both retain their prior recorded UNTESTED. This block scores the evidence package only and makes no claim about the accessibility of the empty-state message, the combobox, or the option."
```
