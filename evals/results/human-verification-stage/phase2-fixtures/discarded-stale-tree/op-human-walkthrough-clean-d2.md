## Per-operation reasoning

### OP-RETURN — Escape dismisses the Details dialog (claimed PASS)

**Rule 1 — `bounded_diagnostic_not_promoted`.** No stagnation-class note is present and no trap conclusion is drawn. The shape here is the inverse of the rule's concern: the package records the documented exit attempt (Escape) *and* its outcome, which is the very trace rule 1 demands before any trap talk. Nothing bounded is promoted. Not violated.

**Rule 2 — `setup_action_continuity`.** The setup's terminal identity — `reached_by` ending at "Enter to open the Details dialog" — equals `before.locus`, "Details dialog open; focus on its heading 'Item details'", and both sit inside one `session` (2026-09-02-JR-a). The action fires from that locus. Continuous.

The plausible false fire here is the second confirmation: different person, later date, session `2026-09-05-MS-a`. That is **not** a rule-2 violation. Rule 2 forbids *composing* a setup from one session with an action from a different starting locus in another. Nothing is composed here — row two is a second, independently complete package carrying its own `reached_by`, its own `locus`, and its own `action` within its own session. The protocol names this construction explicitly: for human evidence rules 2 and 4 are structured self-report, "and the second confirmation is the control." Two complete packages agreeing is the control operating as designed, not a broken chain.

The pre-counted "Tab x5" is worth naming and not scoring. In a machine trace it would violate the keyboard-driving discipline in SKILL.md (never send a pre-counted sequence of Tabs; confirm by state change). In a human self-report it is narrative describing what the person did, and the terminal state is independently pinned by `locus` and `announced` ("dialog, Item details, heading level 2") rather than by the count. It is not the predicate of any of the five rules, so it does not move the disposition.

**Rule 3 — `natural_only_conditional_state`.** Not a conditional state (no empty result, no error); nothing induced synthetically. No predicate to fail.

**Rule 4 — `passive_observation_binding`.** `observed_via: announcement`, and the observation is bound to its causing key press: Escape → "Dialog closed; NVDA announced 'Renew, button'; visible focus ring on that button." This clears both human traps the protocol names. It is not "I checked it, it's fine" — there is a starting locus and an action for the observation to bind to. And it is not the tidier trap either: `observed` is not "as expected" but a distinct, specific result — an announced name and role plus a visible indicator — separable from the `expected` field above it. Row two is the same shape with VoiceOver. No standalone DOM/AX snapshot is offered in place of the key press.

**Rule 5 — `ancestor_remapping_review`.** `target_reached: exact`. No nearest-ancestor substitution, silent or otherwise.

**Disposition PASS.** Admitted evidence decides the operation's own predicate — dialog closed, focus returned to the row-action trigger — on two independent runs.

### OP-FLASH — homepage carousel transition (claimed BLOCKED)

This is the attended-media shape the protocol carves out: an observation about content rather than an operation, with no locus and no action. Rules 2 and 5 therefore do not apply, and the package's field set is consistent with that — it carries no `before`, no `action`, no `target_reached`, rather than filling them with plausible-looking prose. `played` is the binding field.

**Rule 1 — `bounded_diagnostic_not_promoted`.** This is the load-bearing rule here and the package passes it precisely. A bright flash and a rapid alternation were seen; the person declines to promote that to a flash-threshold failure, and `adequacy` states why in instrument terms — "no longer look would decide it; that call needs a flash-frequency analyzer reading." The protocol's own BLOCKED definition names this exact case ("a person's 'I watched the animation and cannot count flashes per second' with no analyzer reading"), and `tooling` declares the analyzer absent up front. Not violated. Promoting this to FAIL would be the violation.

**Rule 3 — `natural_only_conditional_state`.** The carousel autoplays; the slide change occurred on its own during an unaided first look. Nothing was forced or edited to make the transition happen. Not violated.

**Rule 4 — `passive_observation_binding`.** `played` is present and specific — "One capped first look at a single slide change, about two seconds, then looked away; no further attendance" — and `seen` is scoped to exactly that: "that is all that was attended." The observation does not outrun the attendance, and no label or listing is substituted for the thing attended. Not violated.

**Disposition BLOCKED.** An admitted bounded observation about this operation stands without the instrument reading that would decide it, and `claim_boundary` names the missing instrument. Two adjacent values are wrong: `UNTESTED` would be wrong because an admitted observation does bear on the operation (a flash was seen), and `FAIL` would be wrong because the predicate is a threshold the eye cannot resolve.

### OP-AD — audio description track for the training video (claimed FAIL)

Also the attended-media shape — audio description, content rather than operation — so rules 2 and 5 do not apply, and again the package omits `before`/`action`/`target_reached` rather than confabulating them.

**Rule 4 — `passive_observation_binding`.** This is the rule the protocol says catches the AD failure mode, and it is the one to scrutinize, because `seen` does contain "Menu lists 'Described'". That listing would break rule 4 if it were offered *as* the evidence of the alternative. It is not. The verdict rests on `played` — "0:00-1:10 with the 'Described' track selected from the CC/AD menu; 0:35-1:00 again with the track deselected" — and on `heard` over that attended stretch: silence across 0:40-0:55 with the track on, the second voice speaking only once at 1:02 to read a chapter title, and silence across the same stretch with the track off. The menu listing carries only presence, and `claim_boundary` says exactly that: present in the menu, inadequate for the stretch. The with/without pair is the strongest part of this package — it separates "the track is not doing anything here" from "nothing was audible at all." Not violated.

**Rule 1 — `bounded_diagnostic_not_promoted`.** FAIL is not an over-promotion of a bounded observation, and the contrast with OP-FLASH is the test. OP-FLASH's predicate is a rate threshold that unaided attendance cannot resolve, so it stops at BLOCKED. OP-AD's predicate — does the Described track speak the settings panel and the on-screen error code during the silent stretch — is decided by listening: the stretch was played with the track selected and the track spoke nothing. No instrument stands between the observation and the predicate, so there is no missing reading to block on. Not violated.

**Rule 3 — `natural_only_conditional_state`.** Deselecting the description track is worth checking against this rule and clears it. Rule 3 targets a state that appears only under a condition, induced by editing a response or forcing the state. Selecting and deselecting a track through the player's own CC/AD menu is an approved input exercised naturally; no response was edited and no state was forced into existence. Not violated.

**Disposition FAIL.** Admitted evidence decides the operation's own predicate, and that predicate is itself stretch-scoped in `expected` (0:40-0:55), so the finding does not outrun what was played.

### Package-level

No rule is broken by any of the three operations, so the package is admissible as a whole. Where my confidence is lowest: OP-RETURN's continuity and OP-AD's binding both rest on structured self-report, which the protocol admits as self-report by design rather than as verified identity or an allowlisted source. That is a known property of the instrument, not a defect in this package — and OP-RETURN supplies the second confirmation that the protocol designates as the control for it. OP-FLASH and OP-AD carry no second confirmation; each rests on one person's attendance, which their claim boundaries already reflect.

## Structured disposition block

```yaml
admissibility: ACCEPT
dispositions: {OP-RETURN: PASS, OP-FLASH: BLOCKED, OP-AD: FAIL}
rules_violated: {}
claim_boundary: "OP-RETURN: Escape dismisses the Details dialog and returns focus to the Renew row-action trigger, confirmed twice at 3.4.0 (Firefox 143 + NVDA, Chrome 141 + VoiceOver); undecided are other dialogs, other AT and browser pairings, and any conformance claim across the wider sample set. OP-FLASH: one homepage carousel slide change, attended once for about two seconds, does show a bright flash and a rapid alternation; whether it crosses the general or red flash threshold is undecided pending a flash-frequency analyzer reading, and nothing is established about other slides, other carousels, or other pages. OP-AD: the Described track is present in the CC/AD menu but plays silence over 0:40-0:55 - the same stretch played with the track deselected - so it does not convey the settings panel or the on-screen error code that the primary audio omits at 3.4.0; undecided are the remaining 1:10-3:40 of the video, other videos, and every other description track on the product."
```

## Provenance

I read four things. The protocol slice at `scratchpad/hv-rows/opevidence-protocol.md`, in full, as the governing instrument. The evidence package at `scratchpad/hv-rows/stage/op-human-walkthrough-clean.md`, treated as the complete record for this retest. `.claude/skills/a11y-test/SKILL.md`, lines 80-125 — the Operation-evidence admissibility section the slice derives from, plus the campaign-completeness and PASS-partition sections bracketing it, and the keyboard-driving discipline paragraph I cite on the "Tab x5" point. And a `find` across the working tree for `human-verification-walkthrough.md`, which returned nothing: the walk-through reference the protocol links by name is not present in this checkout, so the protocol slice's own paragraph on human-sourced packages is the sole authority I applied for the human field semantics (`played` as the binding field, rules 2 and 5 inapplicable to the attended-media shape, second confirmation as the control). I read nothing under `evals/`, no metadata or rubric files, nothing under `docs/plans/`, and searched for no fixture name or prior draft.
