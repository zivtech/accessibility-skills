## Per-operation reasoning

**Rule 3 (`natural_only_conditional_state`) up front, once.** No operation in this package turns on a conditional state — no empty result, no error, no state reachable only under a condition. Nothing was induced, no response was edited, no developer-tools forcing appears anywhere. Rule 3 is not violated by any of the five, and I do not list it below.

### OP-ESC — dismiss the Details dialog with Escape

Full Shape 1 package. Taking the rules in order:

- `bounded_diagnostic_not_promoted` — **clean.** There is no bounded diagnostic here to promote. `action: "Escape"` *is* the documented exit attempt, and the claim rests on what focus did after it, not on an impression that focus was stuck. Nothing is elevated to a trap or operability conclusion on a stagnation-class note.
- `setup_action_continuity` — **clean.** `before.reached_by` is a continuous path in one sitting (load the results view → Tab ×5 to the Renew row action → Enter to open the dialog), `before.locus` is a named AT position ("focus on its heading 'Item details'"), not "the page", and the action starts from that locus inside `session: 2026-09-02-JR-a`. No fresh load intervenes between reaching the locus and pressing Escape. The load that opens `reached_by` is part of `reached_by`, so it does not break the session.
- `natural_only_conditional_state` — clean (see above).
- `passive_observation_binding` — **clean.** `observed` reports a result of the action, not a restatement of `expected`: the dialog closed, NVDA announced "Renew, button", and a visible focus ring landed on that button. `observed_via: announcement` matches the defect class the closure names (focus return / name-role-state on landing), and the announcement is given as heard rather than paraphrased. This is the only one of the five packages where an action and its observed result are both present and distinct.
- `ancestor_remapping_review` — **clean.** `target_reached: exact`; no ancestor is substituted and none needs a mapping.

Admissible. Disposition **PASS** — the admitted observation decides this operation's own predicate exactly as a trace would.

Two calibrations that are *not* rule violations and must not be recorded as such. First, rules 2 and 4 are structured self-report for human evidence, not a verified `before` identity and not an allowlisted source; the shape makes a discontinuity visible to a second reader, it does not make one impossible. Second, this PASS closes `rem-focus-return-2c7f0a1b`, and at the fixed stage the n = 1 rule runs against a single PASS: a `supports`-bearing confirmation needs a second package by a different person (preferred — it is the only branch that controls the confirmer's expectation), or the same person in a separate session on a later day, with at least one of the two not by the fix's author. This walk supplies one package. So OP-ESC is admissible and PASS, and the closure still stands `draft_not_attested`. That is an attestation-tier consequence recorded in `claim_boundary`; inventing a sixth rule for it would break the five-rule closed set.

### OP-RETURN — focus return on the Renew dialog

"Checked the Renew dialog; focus return works fine now — J.R." No `before`, no `action`, no `observed` detail, no `session`.

This is the under-specified shape the walk-through names by construction, and it fails the rules whose predicates it cannot show:

- `setup_action_continuity` — **violated.** There is no starting locus and no session id. Rule 2's predicate is that `before` identity equals the terminal identity of the setup immediately preceding it in the *same* session; with neither field present, nothing can satisfy or be checked against it.
- `passive_observation_binding` — **violated.** There is no action for an observation to bind to, and "works fine now" is a verdict rather than an observed result. No `observed_via` is declared, so not even the vocabulary is on the record.
- `bounded_diagnostic_not_promoted` — not violated. "Works fine now" is not a bounded diagnostic being promoted; it is a conclusion with no observation of any kind behind it. Rule 1 has nothing to read.
- `ancestor_remapping_review` — not violated. No target substitution is claimed or implied; there is simply no target evidence.

Disposition **UNTESTED.** Rejected evidence never moves an operation, and nothing else in this package bears on it. In particular OP-ESC does not carry over: OP-ESC is the *Details* dialog, OP-RETURN is a second finding on the *Renew* dialog, and OP-ESC's own `claim_boundary` disclaims other dialogs. Treating one dialog's walked PASS as covering another would be the ancestor-substitution error at page scope.

### OP-AD — audio description track for the training video

"The player's CC/AD menu lists a 'Described' track — J.R." Nothing was played and nothing was heard.

This is an observation about *content*, not an operation, so it is scored as a Shape 2 attended-media package. Rules 2 and 5 have no field to read here — there is no locus and no descendant reached through an owner — and the reference marks them not applicable. I do not record them as violations; doing so would punish the shape rather than the evidence.

- `passive_observation_binding` — **violated**, and it carries the whole load here. A menu listing, a track label, or a player's "described" badge is precisely the passive artifact the rule refuses to let stand alone. `played` is the binding field and it is empty. A track offered is not a track heard.
- `bounded_diagnostic_not_promoted` — **violated.** "The menu lists a track" is the canonical Shape 2 bounded observation, and the package promotes it to `PASS` on the alternative's existence *and* adequacy. A bounded observation with no played stretch behind it is never a conclusion.
- `natural_only_conditional_state` — not violated; nothing was staged.

Disposition **UNTESTED**, not BLOCKED. This is the discrimination that matters. BLOCKED is for the attended-but-indeterminate observation — the person looked or listened and cannot decide without an instrument, and `claim_boundary` names the instrument. Here nothing was attended at all: what is missing is not an analyzer or a waveform capture but an action anyone could have taken (select the Described track and play a stretch). Collapsing that into BLOCKED would launder a non-attendance into a bounded observation. UNTESTED is the value for *nobody attended the media*.

### OP-OPTION — nested option state inside the filter combobox

"Tabbed to the filter and the highlighted option's selected state looked right — J.R." No mapping cited.

- `ancestor_remapping_review` — **violated**, and this is the operative failure. The person reached "the filter" — the combobox owner — and reports on the option inside it. That is a silent nearest-ancestor substitution: the option is not on the focus path, the composite's reviewed, separately frozen owner/descendant mapping is not cited, and no `target_reached` field exists to claim `exact` or to name the mapping. The target was not observed.
- `passive_observation_binding` — **violated.** "Looked right" is the "works" / "as expected" shape the rule explicitly refuses: it restates the expectation and reports no announced or visible result of the action on the target. No `observed_via` is declared, and a `selected` state claim is a name-role-state class that needs an announcement, not an appearance.
- `setup_action_continuity` — **violated.** There is no `before.locus` (where the person was before tabbing) and no `session`, so the rule's predicate cannot be shown. I flag this deliberately and for consistency: OP-RETURN and OP-OPTION are the same one-line free-prose shape, both missing a starting locus and a session id, and applying rule 2 to one but not the other because a scaffolding sentence points at rule 5 would be scoring the hint rather than the record. "Tabbed to the filter" names a destination, not a starting identity.
- `bounded_diagnostic_not_promoted` — not violated. This is not a trap or operability claim, and "looked right" is not a stagnation-class bounded diagnostic; it is an unbound impression, which is rule 4's business.

Disposition **UNTESTED.** At most the record supports that the person reached the combobox owner; nothing admitted bears on the option's own state.

### OP-LABEL — accessible name of the row-action button

Full Shape 1 package, every field present, `observed: "As expected"`.

- `passive_observation_binding` — **violated, alone.** This is the tidier failure the reference names verbatim. `before` and `action` are real, `observed_via: announcement` is declared — but no observed result of the Tab is bound to it. "As expected" restates `expected` and is not an observation; the field is filled, its content is not. A declared `observed_via` is a vocabulary choice, not evidence that anything was heard.
- `setup_action_continuity` — **clean.** `before.reached_by` (load → Tab ×4 to the first row's action group) is continuous, `before.locus` names a control position ("the first row-action control, before the 'Renew' control"), and the Tab starts from it in `session: 2026-09-02-JR-a`. The predicate is shown; that it is self-reported is the known tier, not a violation.
- `ancestor_remapping_review` — **clean.** `target_reached: exact` is asserted and no ancestor is substituted. That we cannot confirm focus actually landed on the Renew control flows from rule 4's failure, not from rule 5 — rule 5 governs substitution, and none is claimed.
- `bounded_diagnostic_not_promoted` — not violated. No bounded diagnostic is present.

Disposition **UNTESTED.** Nothing admitted bears on the Renew button's accessible name.

One observation on the record worth a second reader's eye, which I am *not* converting into a disposition: `before.announced: "button"` is a bare role with no name, recorded at the first row-action control. That is setup, at a different control from the target, so it decides nothing about OP-LABEL and cannot move it — but a control announcing as "button" with no name, on the same row group as a closure for `rem-renew-button-name-51e0c9a7`, is the defect shape that closure describes. It belongs in the campaign's planned set as its own operation, not folded into this one.

### Package as a whole

The walk asserts five PASSes from one sitting. Admitted evidence supports one. Four of the five records are the failure modes the human-verification reference was written to refuse — two free-prose notes, one menu listing offered as a media alternative, and one fully-shaped package with nothing observed in it. `admissibility` scores the package, so it is REJECT; that verdict does not retract OP-ESC's PASS, because `dispositions` carries forward independently what each operation's admitted evidence establishes.

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
  OP-AD: [bounded_diagnostic_not_promoted, passive_observation_binding]
  OP-OPTION: [setup_action_continuity, passive_observation_binding, ancestor_remapping_review]
  OP-LABEL: [passive_observation_binding]
claim_boundary: "OP-ESC — establishes that on the Details dialog at 3.4.0, in
  Firefox 143 with NVDA 2026.1, keyboard only, Escape from the dialog heading
  closed the dialog and returned focus to the 'Renew' row-action trigger, heard
  as 'Renew, button' and visibly indicated. Undecided- every other dialog, every
  other row, other browser/AT pairs, and 2.4.3 or 2.4.7 across the sample set.
  Rules 2 and 4 are satisfied here as structured self-report, not as a verified
  before identity or an allowlisted source. This is one package, so closure
  rem-focus-return-2c7f0a1b does not gain its attestation block- a fixed-stage
  supports needs a second confirmation, preferably by a different person, with
  at least one of the two not by the fix's author; until then the closure stays
  draft_not_attested. | OP-RETURN — nothing established. No admitted evidence
  bears on focus return for the Renew dialog; OP-ESC covers a different dialog
  and disclaims others, so it does not carry over. Closing this needs a package
  with before.reached_by, before.locus, a session, an action, and an observed
  result of that action. | OP-AD — nothing established about the audio
  description. The menu listing does not show that a described track exists in
  this rendition, plays, or conveys the visual information the primary audio
  omits. UNTESTED rather than BLOCKED because nothing was attended- what is
  missing is playing the track, not an instrument reading. Closing this needs a
  Shape 2 package naming the media asset, the stretches played with the
  Described track selected, what was heard and seen, and an adequacy call on a
  named position. | OP-OPTION — nothing established about the option. At most
  the record supports that the person reached the filter combobox, the owner
  rather than the target; the option's selected state and its announcement are
  undecided. Closing this needs target_reached exact with the announced result
  of the action, or an ancestor line citing the campaign's reviewed and frozen
  owner/descendant mapping. | OP-LABEL — nothing established about the accessible
  name of the 'Renew' row-action button at 3.4.0. The setup line's announced
  'button' is an observation about the preceding control, not a result of the
  Tab, and does not bear on the target. Closure rem-renew-button-name-51e0c9a7
  stays draft_not_attested. Closing this needs the verbatim announcement heard
  after the Tab, in place of 'As expected'."
```

## Provenance

I read four files: the protocol slice at `scratchpad/hv-rows/opevidence-protocol.md` and the evidence package at `scratchpad/hv-rows/stage/op-human-signature-only.md`, both under the session scratchpad; and, under the repository root `/Users/AlexUA_1/claude/accessibility-skills-51-receipts` only, `.claude/skills/a11y-test/references/human-verification-walkthrough.md` in full and `.claude/skills/a11y-test/SKILL.md` lines 80–120 (the human verification walk-through, campaign completeness, operation-evidence admissibility, and structured disposition block sections). I read nothing under `evals/`, no `*.metadata.yaml` or `*.rubric.yaml`, nothing under `docs/plans/`, and no results receipts; I did not search the repo for the fixture name or for prior drafts, wrote nothing to the repository, and spawned no subagents. My only write was this file at OUT_PATH.
