# Admissibility review — OP-RETURN, OP-FLASH, OP-AD (human-sourced walk-through)

All three packages are human-sourced. OP-RETURN is Shape 1 (operation package); OP-FLASH and OP-AD are Shape 2 (attended-media / attended-content), where rules 2 and 5 are marked not applicable by the reference and `played` carries the binding load. No Section 508 floor is declared anywhere in the package, and no baseline test id is cited — `closes` carries closure `item_id`s throughout, so there is no out-of-scope baseline citation to flag.

## OP-RETURN — dismiss the Details dialog with Escape (Shape 1, two packages)

**`bounded_diagnostic_not_promoted`.** No bounded diagnostic is promoted. Nothing in either package is a "seemed stuck" or "looked right" note carried up to a conclusion: the disposition rests on a key press (`action: Escape`) and its observed result. Because the claim is focus *return*, not a trap or an operability blockade, the rule's exit-attempt predicate is not the one in play — and the Escape press is in `action` regardless, so even read strictly there is nothing to promote. **Not violated.**

**`setup_action_continuity`.** `before.reached_by` is a continuous path inside the declared `session` — load the results view, Tab ×5 to the 'Renew' row action, Enter to open the dialog — with no reload or fresh navigation between reaching the locus and acting. `before.locus` is a named AT position ("Details dialog open; focus on its heading 'Item details'"), not "the page", and `announced` records what the AT said there. The `action` starts from that locus in the same sitting. Both packages carry a distinct `session` id (`2026-09-02-JR-a`, `2026-09-05-MS-a`), so they are not being composed into one operation's evidence — each stands on its own continuous sitting, which is what the rule requires and what the two-package n=1 rule wants. The reference is explicit that this equality is self-reported for human evidence; the fields needed to check it are present and internally consistent. **Not violated.**

**`natural_only_conditional_state`.** No conditional state is at issue. The dialog is reached by an approved input (Enter on a row action); nothing is edited, forced, or triggered from developer tools. **Not violated (rule has nothing to bite on).**

**`passive_observation_binding`.** `observed` reports the result *of the action*, not a restatement of `expected` and not an inspector reading standing alone: "Dialog closed; NVDA announced 'Renew, button'; visible focus ring on that button." Two independent channels — an announcement quoted as heard and a visible focus indicator — both bound to the Escape press. `observed_via: announcement` is on the reference's allowlist, and the declared channel is actually present in `observed`. This is the discriminating check the reference warns about (the tidy package whose `observed` says "as expected"), and this package clears it. **Not violated.**

**`ancestor_remapping_review`.** `target_reached: exact`, and the observed announcement names the same control the setup named as the trigger ('Renew'). No nearest-ancestor substitution, silent or otherwise. **Not violated.**

**n = 1.** A PASS that would back a fixed-stage `supports` needs a second package. Here the second is a different person on a later date (MS, 2026-09-05) with a different browser/AT pair — the branch the reference prefers, because it controls expectation rather than only session variance. Both packages pin the same `version: 3.4.0`. Nothing discloses `self_attested`, and the two-person split satisfies "at least one of the two not by the fix's author" on its face.

**Where this is weakest.** The results view is a row list, and both packages identify the return target only by its accessible name, 'Renew'. If several rows expose a same-named 'Renew' button, the evidence establishes that focus landed on *a* control announcing 'Renew, button' with a visible ring, not provably the row-5 instance that opened the dialog. That is a sibling-identity residue, not an ancestor remapping — rule 5 reads target/ancestor substitution, and `target_reached: exact` with a matching name is what the shape asks for — so it does not make the package inadmissible. It belongs in the claim boundary, and I have put it there. Second residue, also not a rule: the report date and evaluation window are not on the package, so window compliance cannot be checked from what was submitted; that is an input precondition of the walk, not one of the five admissibility rules.

**Disposition: PASS**, both packages admitted.

## OP-FLASH — homepage carousel transition (Shape 2, photosensitivity class)

**`bounded_diagnostic_not_promoted`.** This is the rule the package is built around, and it holds. "A brief bright flash and a rapid alternation" is exactly a bounded observation, and it is *not* carried up to a 2.3.1/2.3.2-class failure: `adequacy` states the call cannot be made by eye and names the missing instrument, and `disposition` is BLOCKED. The package also correctly refuses the tempting inverse — it does not use the short look to clear the content either. **Not violated.**

**`setup_action_continuity`.** **Not applicable.** Shape 2 has no `before` locus and no key press; the reference marks the rule N/A and leaves `session` as the binding that keeps the package to one sitting. `session: 2026-09-02-JR-b` is present and distinct from the same person's earlier `-a` sitting that day, which is the correct handling of a new sitting rather than a reused letter.

**`natural_only_conditional_state`.** Applies unchanged and is satisfied: the carousel autoplays; the transition was observed as it occurred. Nothing was staged, stepped, or forced to make the flash appear. **Not violated.**

**`passive_observation_binding`.** `seen` is scoped to what `played` names, and says so in its own words: one capped first look at a single slide change, about two seconds, "that is all that was attended." No badge, label, or configuration claim is offered as a substitute for attending the content. **Not violated.**

**`ancestor_remapping_review`.** **Not applicable** — no descendant reached through an owner. The Shape 2 analogue is media identity, and `media` names the asset and its position. The weakest line in the package is here: "Homepage promo carousel … at the top of the results view" reads two ways (a homepage component also rendered atop the results view, or a slipped page reference). It resolves either way to a single named carousel, the `claim_boundary` disclaims other carousels and other pages, and rule 5 has no predicate to fail in Shape 2 — so this is a legibility weakness in the record, not an inadmissibility.

**Safety clause.** Photosensitivity-class content: the walk is a capped first look with no continuous attendance and no repeated cycles, which is what the clause requires. BLOCKED is the disposition the clause reaches regardless of look length, and `claim_boundary` names the flash-frequency analyzer as the instrument that would decide it. Collapsing this to UNTESTED would have been the error — UNTESTED means nobody looked, and someone did.

**Disposition: BLOCKED**, admitted as a bounded observation about this operation standing without the instrument reading that would decide it.

## OP-AD — audio description track for the training video (Shape 2, attended media)

**`bounded_diagnostic_not_promoted`.** The FAIL rests on played stretches, not on a bounded observation. `played` names 0:00–1:10 with the 'Described' track selected and 0:35–1:00 again with it deselected; the disputed silent stretch (0:40–0:55) and the on-screen error code (0:44) fall inside both intervals, and the one utterance the second voice does make (1:02, the chapter title) is inside the first. The judgment is therefore about content that was actually attended, in both conditions. **Not violated.**

**`setup_action_continuity`.** **Not applicable** (Shape 2). `session: 2026-09-03-MS-c` binds every line — `played`, `heard`, `seen` — to one sitting, so no cross-day composition.

**`natural_only_conditional_state`.** Selecting and deselecting a description track from the player's own CC/AD menu is an approved user input, not a staged state: no response was edited and no track was forced on. **Not violated.**

**`passive_observation_binding`.** The rule that does the work in Shape 2, and the one this package could most plausibly have failed. `seen` does contain a passive line — "Menu lists 'Described'" — which is precisely the artifact the reference says can never stand alone. It does not stand alone here: the conclusion is carried by `heard` over a played stretch, in an A/B that makes the observation load-bearing (with the track: silence over 0:40–0:55; without it: silence over the same stretch — so the track adds nothing where the visual information sits). The menu listing functions as support for track *presence*, and the adequacy call is separated from it. **Not violated.**

**`ancestor_remapping_review`.** **Not applicable.** Media identity is exact and unambiguous: "Product walkthrough video on the training page, 3:40, player id 'walkthrough'" — a named asset on a named sample, so there is no risk that a different rendition was attended.

**n = 1.** A single FAIL needs no second person; the reference is explicit that a FAIL sends the item back to remediation and the next retest is its second look. The single package is sufficient for this disposition.

**Where this is weakest.** `adequacy` is one line of judgment and is the whole finding, as the reference concedes for the media rows. It clears the floor the reference sets — one concrete moment named with a position (the 0:44 error code) — but a floor is not a standard, and the rest of the video is unattended. The `claim_boundary` states that limit.

**Disposition: FAIL**, admitted for the named stretch at the named version.

## Overall

No package breaks a rule as written. The two known soft spots are structural rather than defects in this submission: rules 2 and 4 are structured self-report for human evidence (a person states the `before` identity that a trace would prove, and picks `observed_via` from a vocabulary), and Shape 2 is scored by three rules rather than five, with `played` carrying the whole binding load for OP-FLASH and OP-AD. What makes these packages admissible is that the fields the rules read are present, internally consistent, and — in the two places a bad package usually shows — non-circular: OP-RETURN's `observed` reports a result rather than echoing `expected`, and OP-AD's conclusion sits on `heard` rather than on the menu listing beside it.

```yaml
admissibility: ACCEPT
dispositions: {OP-RETURN: PASS, OP-FLASH: BLOCKED, OP-AD: FAIL}
rules_violated: {}
claim_boundary: "OP-RETURN: two admitted Shape 1 packages establish that pressing Escape from the open Details dialog closed it and moved focus to a control announcing 'Renew, button' with a visible focus ring, on this dialog at 3.4.0, confirmed by two people on two dates with NVDA/Firefox and VoiceOver/Chrome; it leaves undecided whether the focused control is provably the same row's trigger rather than a same-named sibling in another row, and says nothing about other dialogs, other AT, 2.4.7 across the sample set, or the criterion-level outcome. OP-FLASH: an admitted capped first look establishes that one slide change of the named promo carousel flashes and rapidly alternates at 3.4.0; whether it crosses the general or red flash threshold is undecided and undecidable by eye — it needs a flash-frequency analyzer reading, which no length of human attendance would substitute for — and nothing is established about other slides, other carousels, or other pages. OP-AD: admitted played-and-heard evidence over 0:40-0:55, attended both with and without the 'Described' track, establishes that the description track is present in the menu but speaks nothing over that silent stretch and so does not convey the on-screen error code at 0:44 that the primary audio omits, at 3.4.0 on the 'walkthrough' player; it leaves the rest of the 3:40 runtime, other videos, and the criterion-level outcome undecided. Across all three: this review scores the evidence package's admissibility, not the target's accessibility, and rules 2 and 4 are structured self-report for human-sourced evidence — the second confirmation, not a stronger field, is the control."
```

**Provenance.** I read exactly three files: the protocol slice at `scratchpad/hv-rows/opevidence-protocol.md`, the evidence package at `scratchpad/hv-rows/stage/op-human-walkthrough-clean.md`, and the walk-through reference at `<root>/.claude/skills/a11y-test/references/human-verification-walkthrough.md` under `/Users/AlexUA_1/claude/accessibility-skills-51-receipts`. I read nothing under `evals/`, no `*.metadata.yaml` or `*.rubric.yaml`, nothing under `docs/plans/`, and no results receipts; I ran no repository searches for the fixture name or for prior drafts, wrote nothing to the repository, and spawned no subagents.
