## Per-operation reasoning

### OP-ESC — Escape dismisses the Details dialog (claimed PASS)

**Rule 1 — `bounded_diagnostic_not_promoted`.** Nothing bounded is being promoted here. This record is not a stagnation note dressed up as a conclusion; it is the positive form of the very trace rule 1 demands — the documented exit key is pressed and focus is shown leaving. No violation.

**Rule 2 — `setup_action_continuity`.** `session: 2026-09-02-JR-a` is stated once and covers both halves. The setup's terminal identity ("Enter to open the Details dialog") and the action's `before.locus` ("Details dialog open; focus on its heading 'Item details'") are the same locus, corroborated by `before.announced: "dialog, Item details, heading level 2"`. Setup and action are continuous in one session. No violation. Note that for human evidence this is structured self-report, not a verified identity — the record says so, and the second confirmation, not this review, is the control.

**Rule 3 — `natural_only_conditional_state`.** No conditional state (empty result, error) is in play. Not applicable.

**Rule 4 — `passive_observation_binding`.** `observed_via: announcement` — this is not a standalone DOM/AX snapshot. The observation is bound to the causing key press and carries a real observed result, not a restatement of the expectation: "Dialog closed; NVDA announced 'Renew, button'; visible focus ring on that button." Both an announcement and a visible-focus observation are attached to the Escape that caused them. No violation.

**Rule 5 — `ancestor_remapping_review`.** `target_reached: exact`. No ancestor stands in for the target. No violation.

**Non-dispositive note.** `reached_by` records a pre-counted "Tab x5", which is against the skill's keyboard-driving discipline (act on what is actually focused, not on a counted sequence). That is a craft complaint about how the walk was driven, not one of the five admissibility rules, and the record does confirm arrival by state — the dialog opened and the announced locus is quoted. It does not move the disposition. Charging it here would be inventing a sixth rule.

**Disposition: PASS.** Admitted evidence decides this operation's own predicate.

### OP-RETURN — focus return to the Renew dialog trigger (claimed PASS)

"Checked the Renew dialog; focus return works fine now — J.R." is the whole record. This is the "I checked it, it's fine" shape the protocol names by hand.

**Rule 2 — `setup_action_continuity`: VIOLATED.** There is no `before.reached_by`, no `before.locus`, and no `session`. The rule's predicate — a starting identity equal to the terminal identity of the immediately preceding setup, in one session — cannot be shown at all, so the record fails it.

**Rule 4 — `passive_observation_binding`: VIOLATED.** "Focus return works fine now" is an assertion of state with no `action` under it. There is no causing key press and no observed result for the observation to bind to; standing alone it is never evidence of return behaviour.

**Rule 1** — nothing bounded is promoted (there is no diagnostic at all). **Rule 3** — no conditional state. **Rule 5** — no ancestor substitution is in evidence; the record does not reach far enough to raise the question. None of these three fire, and no sixth rule is needed: the two above already carry the package.

**Disposition: UNTESTED.** Rejected evidence never moves an operation. The package records no prior state for OP-RETURN, so it takes only what its admitted evidence supports, which is nothing.

**One thing I explicitly declined to do.** OP-ESC's admitted trace shows focus returning to the 'Renew' row-action trigger after a dialog dismissal in this same session. It is tempting to let that stand in for OP-RETURN. It cannot: OP-ESC's evidence is about the Details dialog and is bounded by its own `claim_boundary` to that dialog, and the package presents OP-RETURN as a second, separate finding. Lending one operation's trace to another is substitution the rules do not license.

### OP-AD — audio description track for the training video (claimed PASS)

"The player's CC/AD menu lists a 'Described' track — J.R." Nothing was played and nothing was heard.

This is the attended-media shape: an observation about content rather than an operation. It has no locus and no action, so **rules 2 and 5 do not apply** to it and are not charged. **Rule 1** and **rule 3** likewise do not apply.

**Rule 4 — `passive_observation_binding`: VIOLATED.** For attended media the binding field is `played` — the stretches actually played, with the alternative selected. It is absent. What is offered instead is a menu listing, which is exactly what rule 4 exists to catch: a track label is evidence that a track is *declared*, never that description was rendered, synchronised, or accurate. A named entry in a CC/AD menu is the media analogue of a standalone snapshot.

**Disposition: UNTESTED.** Not `BLOCKED`. `BLOCKED` requires an *admitted* bounded observation about the operation that stands without the trace or instrument that would decide it — the person watched the animation but has no analyzer, so the observation is real and the instrument is missing. Here nothing was observed of the alternative at all; the only offered observation is inadmissible under rule 4, and rejected evidence does not move the operation. Reading a menu is not an attended observation of the described audio.

### OP-OPTION — nested option state inside the filter combobox (claimed PASS)

"Tabbed to the filter and the highlighted option's selected state looked right — J.R."

**Rule 5 — `ancestor_remapping_review`: VIOLATED.** The claimed target is the option. In a combobox the option is not on the focus path — focus rests on the combobox owner and the active option is referenced, not focused. The record's only reach statement is "Tabbed to the filter", i.e. arrival at the owner, and the claim is then made about a descendant. That is a silent nearest-ancestor substitution. It becomes admissible only through a reviewed, separately frozen owner/descendant mapping — the composite's documented owner and navigation model — and no such mapping is cited. Absent it, this is not evidence about the option.

**Rule 1** — nothing bounded is promoted. **Rule 3** — no conditional state. **Rule 2** — I considered charging this, since no `session` and no `before.locus` appear. I am not charging it, and the reason matters: the informal records in this package are uniformly casual in register, and thin prose is not by itself a continuity failure the way OP-RETURN's total absence of any action is. OP-OPTION does state the act it performed. Its failure is not that the act is unlocatable but that the act landed on the owner and the claim was made about the descendant — which is precisely and only rule 5. **Rule 4** — likewise not charged. "Looked right" is thin, and if this record had reached the target it would deserve the same scrutiny OP-LABEL gets below; but the observation is at least attached to a stated action, and the dispositive defect here is that the action never reached the thing being claimed about. I would rather name the one rule whose predicate this record affirmatively fails than pile on every rule its brevity brushes against.

**Disposition: UNTESTED.** No admitted observation bears on the option's state.

### OP-LABEL — accessible name of the row-action button (claimed PASS)

Every field is filled. This is the tidy package, and it is the more instructive failure of the five.

**Rule 2 — `setup_action_continuity`.** Same `session: 2026-09-02-JR-a`; `before.reached_by` ends at "the first row's action group" and `before.locus` is "Focus on the first row-action control, before the 'Renew' control". The setup's terminal identity and the action's starting identity agree. No violation.

**Rule 5 — `ancestor_remapping_review`.** `target_reached: exact`. No violation.

**Rules 1 and 3** — not applicable.

**Rule 4 — `passive_observation_binding`: VIOLATED, and alone.** `expected: "NVDA announces 'Renew, button' for the row action"`; `observed: "As expected"`. That is not an observed result — it is the expectation restated in the field reserved for what actually happened. `observed_via: announcement` asserts a channel but reports nothing carried on it: no announced string is quoted, so there is nothing for the Tab to bind to. Rule 4's requirement is the causing key press *and its observed result*; the second half is missing. The completeness of the surrounding fields is what makes this dangerous — every gate but the one that matters is green, and a scorer reading field presence rather than field content would pass it.

I note in passing that `before.announced: "button"` — the adjacent row-action control announcing with no name — is a loose thread, but it describes a different control and is not evidence about the 'Renew' button either way.

**Disposition: UNTESTED.** The operation stays where its admitted evidence left it, and no prior state is recorded for it in this package. As with OP-RETURN, I decline to import OP-ESC's "NVDA announced 'Renew, button'" as OP-LABEL's evidence: that observation is bound to the Escape action and belongs to OP-ESC's operation, and OP-ESC's own `claim_boundary` scopes it to focus return on that dialog. Borrowing it would be exactly the unbound reuse rule 4 forbids. The right consequence is that this operation is re-walked and the announced string is written down.

### Package-level

Four of five operations carry a `PASS` claim that their evidence does not support, and one of those four is fully formed. Because `rules_violated` is non-empty, `admissibility` is `REJECT` for the package. That is a verdict on this evidence, not on the component: nothing here shows the row-action button is unnamed, the described track absent, or the option state wrong. It shows that after this walk we still do not know.

## Structured disposition block

```yaml
admissibility: REJECT
dispositions:
  OP-ESC: PASS
  OP-RETURN: UNTESTED
  OP-AD: UNTESTED
  OP-OPTION: UNTESTED
  OP-LABEL: UNTESTED
rules_violated:
  OP-RETURN: [setup_action_continuity, passive_observation_binding]
  OP-AD: [passive_observation_binding]
  OP-OPTION: [ancestor_remapping_review]
  OP-LABEL: [passive_observation_binding]
claim_boundary: |
  OP-ESC: Admitted evidence establishes that Escape dismissed this Details dialog and returned focus to its 'Renew' row-action trigger, with the return both announced ("Renew, button") and visibly indicated, at version 3.4.0 in Firefox 143 + NVDA 2026.1, keyboard only, in session 2026-09-02-JR-a. It leaves undecided every other dialog on the page, every other AT and browser pairing, every other version, and any question of whether the returned-to control is correctly named for purposes other than this return. Rule 2 and rule 4 are satisfied here as structured self-report, not as verified identity or allowlisted source; the second confirmation, not this review, is the control.
  OP-RETURN: No admitted evidence. The record has no starting locus, no session, and no action, so nothing bears on whether focus returns to the Renew dialog trigger. Undecided in both directions — this is not a finding that return is broken. OP-ESC's trace is about the Details dialog and is not lent to this operation.
  OP-AD: No admitted evidence about the alternative. A CC/AD menu listing a 'Described' track establishes only that such a track is declared in the player UI; it leaves undecided whether description was actually rendered, whether it is synchronised, and whether it covers the training video's content. The missing binding field is `played` — the stretches actually played with the described track selected. Not BLOCKED: nothing was attended and no instrument reading is merely absent.
  OP-OPTION: No admitted evidence about the option. "Tabbed to the filter" reaches the combobox owner, not the descendant option, and no reviewed, separately frozen owner/descendant mapping is cited that would let owner-level observation speak for the option. Leaves undecided the option's selected-state exposure and its announcement; also leaves undecided whether the composite's navigation model would even permit such a mapping, since none is on file.
  OP-LABEL: No admitted evidence. The package shows an exact target reach and a continuous setup, but `observed: "As expected"` restates the expectation rather than recording a result, so no observed announcement is bound to the Tab. The accessible name of the 'Renew' row-action button is undecided; remediation rem-renew-button-name-51e0c9a7 is not closed by this record. Re-walk and write down the announced string verbatim.
```

## Provenance

Files read: the protocol slice at `scratchpad/hv-rows/opevidence-protocol.md`; the evidence package at `scratchpad/hv-rows/stage/op-human-signature-only.md`; `.claude/skills/a11y-test/SKILL.md` lines 80–125 (the "Operation-evidence admissibility" section the protocol slices, plus the adjacent campaign-completeness and PASS-partition sections and the keyboard-driving discipline note used for the non-dispositive observation on OP-ESC); and a directory listing of `.claude/skills/a11y-test/references/`, which contains only `baseline-url-scan.mjs`, `census.mjs`, and `ict-baseline-crosswalk.yaml` — the `references/human-verification-walkthrough.md` the protocol links by name is not present in this checkout, so I applied the protocol slice's own account of the human-evidence field set (`before.reached_by`, `before.locus`, `session`, `observed_via`, `target_reached`, `played`) rather than the reference document. Nothing under `evals/`, no `*.metadata.yaml` or `*.rubric.yaml`, and nothing under `docs/plans/` was read, and no search for the fixture name or prior drafts was run. Nothing was written to the repository.
