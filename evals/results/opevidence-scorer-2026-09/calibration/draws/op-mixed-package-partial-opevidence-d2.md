# Admissibility review — OP-CLOSE + OP-OPTION (mixed package)

The package is mixed, so each operation is judged on its own evidence. One
operation's evidence survives; the other's does not. The package-level verdict
then follows mechanically: `admissibility` is ACCEPT only when `rules_violated`
is empty, so a single violated rule anywhere makes the package REJECT — which
says nothing about the operation whose evidence stands.

## OP-CLOSE — evidence admitted

The claim is that pressing `Escape` with the Details dialog open dismisses it and
returns focus to the row-action trigger.

Continuity is the rule an exit-path trace usually fails. Here it holds:

- **One session.** The setup (`load+settle` ok, Details dialog opened from the
  results-table row action) and the action (`Escape`) are in the *same* session.
  Nothing is composed across sessions.
- **Identity match.** The setup's terminal focus is the dialog's initial focus
  (its heading). The action's `before` identity is that same locus. Setup
  terminal identity == action starting identity, exactly what the rule requires.
  No stitching from a different starting locus.
- **The observed result is the operation's own predicate.** Both halves of the
  planned expectation are observed: the dialog dismissed *and* focus returned to
  the row-action trigger. This is the observed result of the causing key press,
  not a post-state inferred from a rendered tree.

The other four rules do not bite:

- Nothing of the `focus_stagnation_observed` class is being promoted. The
  opposite: this is the kind of trace the bounded-diagnostic rule *asks for* when
  a stagnation observation needs deciding — a documented exit attempt with its
  observed result.
- No conditional state is involved; the dialog was reached through the normal row
  action, not induced.
- No passive DOM/AX snapshot stands in for the interaction.
- The target is the dialog itself, on the focus path. No ancestor was
  substituted, silently or otherwise.

Disposition: **PASS** — admitted evidence decides this operation's own predicate.

## OP-OPTION — evidence rejected

The claim is that the nested option inside the filter combobox popup is
keyboard-reachable and that its selected state is exposed to assistive
technology. The submitted evidence is a DOM/AX snapshot of the opened popup
showing `role=option` present with `aria-selected` on the target item — and, by
the run's own admission, **no key was pressed to open the popup, navigate to the
option, or select it, and no causing action is attached to the snapshot at all**.

This is the standalone-passive-observation failure in its plainest form. A DOM/AX
snapshot is admissible only as support *bound to the causing action*; by itself
it is never evidence of keyboard-reachability or of announcement, because those
require the causing key press and its observed result. Both halves of this claim
are precisely the two things the rule names as out of reach for a bare snapshot:

- **Reachability** is a property of the focus path under keyboard operation; the
  snapshot reports what exists in the rendered tree. Presence in the tree and
  reachability by keyboard are different facts — an option can carry the correct
  role and still never receive focus, sit outside the composite's navigation
  model, or be mouse-only. No key was pressed, so nothing here bears on it.
- **Announcement** is a property of what AT conveys as a result of an
  interaction. `aria-selected` present in the tree is markup — a necessary
  condition for the announcement, not an observation that one occurred.

The run compounded this by letting one unbound snapshot carry two distinct
predicates at once, on attributes alone. Even properly bound, a snapshot is
*support* for the causing action's observed result, never a substitute for it.

I cite only `passive_observation_binding`. The neighbouring rules do not
independently fire:

- No bounded diagnostic is being promoted — there is no collector observation
  about this operation at all.
- `setup_action_continuity` governs whether an action's `before` identity matches
  the preceding setup's terminal identity. There is no action here to check the
  continuity *of*; the defect is the missing causing action, which the binding
  rule already covers. Citing continuity as well would double-count one defect.
- Nothing conditional was induced.
- The snapshot is taken against the exact target item, not a nearest reachable
  ancestor, so there is no remapping — silent or reviewed — to flag.

Disposition: **UNTESTED**, not FAIL. Rejected evidence never moves an operation.
There is no recorded prior state for OP-OPTION, and no admitted observation bears
on it, so it takes only what its admitted evidence supports — which is nothing.
BLOCKED would also be wrong: BLOCKED is reserved for an *admitted* bounded
collector observation about the operation standing without the trace that would
decide it, and nothing about OP-OPTION was admitted, so there is no bounded
observation to stand.

Worth saying plainly, because the disposition is easy to misread: UNTESTED is a
verdict about the evidence package, not about the combobox. The option may well
be reachable and correctly announced. This run simply does not establish it, and
the remedy is cheap — press the keys, record the observed results, and bind the
snapshot to them as support.

## Disposition block

```yaml
admissibility: REJECT
dispositions: {OP-CLOSE: PASS, OP-OPTION: UNTESTED}
rules_violated: {OP-OPTION: [passive_observation_binding]}
claim_boundary: "OP-CLOSE — admitted evidence is one continuous same-session trace (setup terminal focus = the dialog's heading; action before-identity identical) showing that Escape dismisses the Details dialog and returns focus to the row-action trigger; it establishes that documented exit path from the dialog's initial focus only, and leaves undecided exit from other loci inside the dialog, other dismissal affordances (close button, overlay click), and every other aspect of the dialog's accessibility. OP-OPTION — no evidence admitted; the standalone DOM/AX snapshot is rejected as unbound to any causing action, so nothing is established about the nested option, and both its keyboard reachability and the exposure/announcement of its selected state remain undecided; role=option and aria-selected present in the rendered tree are markup, not observations of reachability or announcement, and this disposition is not a claim that the option is inaccessible. The package-level REJECT scores the evidence package only and does not disturb OP-CLOSE's admitted result."
```
