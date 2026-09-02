# Admissibility review — OP-CLOSE + OP-OPTION (mixed package)

The package is mixed, so each operation is judged on its own evidence. The run claims PASS for both. One of those claims is supported; the other rests on evidence that is not admissible for what it asserts.

## OP-CLOSE — admissible, decides the operation

Against the five rules:

- **Setup/action continuity.** One session, `load+settle` ok. The setup terminates at the dialog's initial focus (its heading); the `Escape` press is issued from that same focus in that same session. The action's `before` identity equals the terminal identity of the setup that immediately preceded it. This is the rule's satisfied case — nothing is being stitched together across sessions or from a different starting locus.
- **Bounded diagnostic.** No `focus_stagnation_observed`-class note is present and nothing bounded is being promoted to a conclusion. The reverse, in fact: this *is* the documented-exit trace the stagnation rule demands elsewhere — the exit key was pressed and the resulting focus destination was observed.
- **Conditional state.** Nothing conditional, nothing induced. The dialog was reached through the ordinary route (the results-table row action).
- **Passive observation binding.** The observation — dialog dismissed, focus returned to the row-action trigger — is the observed result of a causing key press, bound to it. Not a standalone snapshot.
- **Ancestor remapping.** Evidence is recorded against the dialog itself and the actual return locus (the trigger), both of which are the planned targets. No nearest-reachable-ancestor substitution.

No rule broken. The admitted evidence bears on OP-CLOSE's own predicate — Escape dismisses the dialog and focus returns to the trigger — and reports it satisfied. **PASS.**

What it does not buy: this decides one exit path from one entry route. Other dismissal affordances, other entry points into the dialog, and the dialog's accessibility beyond this path are untouched by it.

## OP-OPTION — inadmissible

The whole submission is a DOM/AX snapshot of the filter combobox's popup showing `role=option` with `aria-selected` exposed on the target item. The submission then concedes the decisive fact itself: no key was pressed to open the popup, navigate to the option, or select it, and no causing action is attached to the snapshot.

That is precisely the standalone passive observation the fourth rule excludes. A DOM/AX snapshot is admissible only as support bound to the causing action; on its own it is never evidence of keyboard-reachability and never evidence of announcement. The run asserted both from it, which is the whole of its PASS.

The two asserted claims fail for related but distinct reasons, and naming them separately matters more than citing the rule id:

- **"Reachable."** The snapshot shows a node exists in the rendered tree with a role. Presence is not reachability. An option can sit in the AX tree and still be unreachable — no key handling on the popup, focus never entering the listbox, `aria-activedescendant` never moving to it. Deciding reachability requires the key press and the observed focus or active-descendant result. Neither exists here.
- **"State announced."** `aria-selected` in the markup is a static authored attribute. Announcement is a runtime event — the state reaching AT as the user moves through the popup. The snapshot cannot distinguish "the attribute is authored on the element" from "a user hears the selected state," and only establishes the former.

No other rule is separately violated. The snapshot is of the target option itself, not of a nearest reachable ancestor standing in for it, so `ancestor_remapping_review` is not engaged; the popup is not a conditional state and nothing was synthetically induced.

Disposition follows the block's own rule that rejected evidence never moves an operation. There is no recorded prior state for OP-OPTION to keep, and once the snapshot is excluded no admitted observation bears on it, so it is **UNTESTED** — not FAIL. Nothing here shows the option is unreachable or its state unexposed; the operation simply was not tested. Nor is it BLOCKED: BLOCKED requires an *admitted* bounded collector observation about the operation standing without the trace that would decide it, and here the only observation offered is inadmissible, so there is nothing standing to block on.

## Package verdict

`admissibility` scores the evidence package, not the targets. One operation's evidence breaks a rule, so `rules_violated` is non-empty and the package is **REJECT** — even though OP-CLOSE's own evidence is clean and its PASS carries forward unaffected. The thing to reject is the run's headline: it converts an unbound snapshot into two runtime claims it cannot support and closes out coverage on an operation that was never exercised.

```yaml
admissibility: REJECT
dispositions:
  OP-CLOSE: PASS
  OP-OPTION: UNTESTED
rules_violated:
  OP-OPTION: [passive_observation_binding]
claim_boundary: "OP-CLOSE — the admitted evidence is a continuous single-session setup+action trace (setup terminal focus equals the action's before identity) establishing that Escape dismisses the Details dialog and returns focus to the row-action trigger for this entry route; it leaves undecided every other dismissal affordance, every other entry point into the dialog, and the dialog's accessibility beyond this one exit path. OP-OPTION — no admitted evidence bears on it: the standalone DOM/AX popup snapshot is inadmissible because no causing action is bound to it, so the keyboard-reachability of the nested option and the announcement of its selected state are both undecided; the snapshot's role=option and authored aria-selected attribute show markup presence, not that the option can be reached by key press or that its state is announced to assistive technology, and equally they do not show the option is inaccessible."
```
