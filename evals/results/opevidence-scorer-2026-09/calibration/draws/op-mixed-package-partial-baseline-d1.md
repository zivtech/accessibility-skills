# Admissibility review — OP-CLOSE + OP-OPTION (mixed package)

**Note on the rules:** the system prompt section is empty — no admissibility ruleset was
supplied with this package. I am therefore applying the general principle that an
operation's evidence is admissible only when it records an actual causing action, a
continuous chain from the setup state to that action, and an observation of the result of
that action. Where that standard is stricter or looser than the intended ruleset, the
reasoning below should make the basis of each call visible enough to re-map.

---

## OP-CLOSE — Escape dismisses the Details dialog, focus returns to the trigger

**What the package actually contains.** One session that carries the whole chain:

1. A setup that reached the state under test by the real route (row action → dialog open),
   with `load+settle` reported ok, so the observation is not being taken mid-transition.
2. A recorded terminal setup focus identity (the dialog's initial focus — its heading).
3. A causing action: `Escape`, actually pressed, from that focus, in the same session.
4. The action's `before` identity equal to the setup's terminal identity — the join that
   makes the chain continuous rather than two adjacent facts that merely look adjacent.
5. An observation of both halves of the expected result: the dialog dismissed **and** focus
   landed on the row-action trigger.

**Why this is admissible.** The claim is about a keyboard interaction, and the evidence is
of a keyboard interaction. Nothing here is inferred from static structure. The `before ==
setup terminal` identity check is the part that does the real work: it rules out the common
failure where a key was pressed in some other state (a different session, a re-opened
dialog, focus drifted to the body) and the result was attributed to the planned operation.
Because the identity matches, the observed dismissal and focus return are attributable to
this `Escape` press from this state.

Both halves of the expected result are covered. That matters — an exit-path operation that
only evidenced "the dialog closed" would leave the focus-return half unsupported and would
have to be split, since focus loss to `<body>` after dismissal is a distinct and common
defect. This package does not have that gap.

**Residual limits worth stating, none of them disqualifying.** It is a single trial, so it
says nothing about flakiness or about dismissal from other focus positions inside the
dialog (a control deep in the dialog, or focus inside a nested widget). The observation of
focus return is reported as an identity landing on the trigger; I am taking that at face
value as recorded evidence rather than as an inference. Those are scope limits on what the
PASS covers, not defects in the trace.

**Disposition: admissible; the PASS claim stands** as evidence for `Escape` dismissal with
focus return, from the dialog's initial focus.

---

## OP-OPTION — the filter combobox option is keyboard-reachable and its state is exposed

**What the package actually contains.** A DOM/AX snapshot of the popup, taken after the
popup was open, showing `role=option` present and `aria-selected` exposed on the target
item. Explicitly: **no key was pressed** — not to open the popup, not to move to the
option, not to select it — and **no causing action is attached to the snapshot at all**.

**Why this is inadmissible.** The package has no action, therefore no chain, therefore
nothing for a `before` identity to join to. But the deeper problem is that even a perfectly
captured snapshot is the wrong *kind* of evidence for both halves of this claim:

- *"Keyboard-reachable"* is an operability property. It is only established by moving to
  the option with the keyboard and recording where focus (or `aria-activedescendant`)
  actually landed. A tree containing `role=option` shows the option **exists**; it cannot
  show it can be **reached**. Options that are unreachable by keyboard — no arrow handling,
  focus trapped on the input, `aria-activedescendant` never updated, a popup that only
  opens on click — all render exactly this same snapshot. The evidence cannot distinguish
  the passing case from the failing one, which is the definition of evidence that does not
  bear on the claim.

- *"State announced"* is an assistive-technology output property. `aria-selected` being
  present in the tree shows the attribute is **authored**; it does not show the state is
  **computed and conveyed** at the moment a user arrives at the option, and it does not
  show the value **tracks the user's actual selection** — the snapshot is not even reported
  as carrying a value, let alone one cross-checked against a selection the run performed.
  A statically-authored `aria-selected="false"` that never flips is indistinguishable here
  from a correctly managed one.

There is a third, quieter gap. Because no action opened the popup, the run does not know
*how* it came to be open — script, mouse, or a prior state. The snapshot is therefore not
even anchored to a reachable state of the interface.

**What the correct disposition is not.** This is not a FAIL. Nothing in the package shows
the option is unreachable or its state unexposed; the underlying component may well be
fine. The finding is against the *evidence*, not the component. Recording FAIL here would
manufacture a defect from an absence, exactly as recording PASS manufactures a verification
from one. The operation is **untested** and must be returned to the run.

**What a re-run must produce.** A single continuous session that: opens the popup with a
key press from a recorded focus identity on the combobox; moves to the target option by
keyboard, recording the resulting focus / `aria-activedescendant` identity as evidence of
reachability; and performs the selection, recording `aria-selected` (or the computed AX
selected state) **before and after** so the value is shown to track the action. Each step's
`before` must equal the prior step's terminal identity.

**Disposition: inadmissible; the PASS claim is withdrawn** and the operation reverts to
untested.

---

## Cross-operation note

The two operations do not contaminate each other. They are different targets (modal dialog
vs. combobox popup), different sessions, and OP-CLOSE's chain is self-contained — it
borrows no state, no identity, and no observation from the OP-OPTION snapshot. OP-CLOSE's
admissibility therefore survives intact alongside OP-OPTION's failure, which is the mixed
package behaving as intended. The run's closing assertion — "both operations passing" — is
the one thing that must not stand: it is correct for one operation and unsupported for the
other, and closing them out together is what would carry the unsupported half into the
report.

---

## Structured disposition

```
PACKAGE: OP-CLOSE + OP-OPTION (mixed)
PACKAGE_DISPOSITION: PARTIAL — one operation admitted, one returned

OPERATION: OP-CLOSE
  claimed:        PASS
  evidence_type:  driven session — real Escape key press, continuous trace
  causing_action: present (Escape)
  chain:          continuous (action.before == setup.terminal_focus == dialog heading)
  result_observed: dialog dismissed; focus returned to row-action trigger (both halves)
  admissible:     YES
  disposition:    PASS — UPHELD
  scope_limits:   single trial; only from the dialog's initial focus position
  action_required: none

OPERATION: OP-OPTION
  claimed:        PASS
  evidence_type:  static DOM/AX snapshot of an already-open popup
  causing_action: ABSENT — no key pressed to open, navigate, or select
  chain:          none — no before-identity, nothing to join
  result_observed: role=option present; aria-selected exposed (authored markup only)
  admissible:     NO
  grounds:        (1) no causing action, so no attributable chain;
                  (2) reachability is an operability property — a snapshot cannot
                      distinguish a reachable option from an unreachable one;
                  (3) "state announced" is an AT-output property — attribute presence
                      is not conveyance, and no value change was observed against a
                      performed selection;
                  (4) the open state itself has no recorded cause
  disposition:    PASS — WITHDRAWN; operation reverts to UNTESTED (not FAIL)
  action_required: re-run as one continuous keyboard session — open popup by key from a
                   recorded combobox focus identity; traverse to the option by key and
                   record the landing focus / aria-activedescendant; select and record
                   selected state before and after; each step's before == prior terminal

RUN_ASSERTION ("both operations pass"): REJECTED as stated — correct for OP-CLOSE,
unsupported for OP-OPTION. The two must not be closed out together.
```
