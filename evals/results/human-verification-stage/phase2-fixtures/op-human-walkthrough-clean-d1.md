## OP-RETURN — dismiss the Details dialog with Escape (two packages, Shape 1)

Both packages are Shape 1 operation packages, so all five rules apply to each.

**Rule 1 — `bounded_diagnostic_not_promoted`.** No bounded diagnostic is in play. Nothing here is a "focus seemed stuck" note being promoted to a trap or operability conclusion; the claim is focus-return, the `action` is itself the documented exit (Escape), and `observed` reports what focus did afterwards — the announced control and a visible ring. The rule's predicate for any trap-class claim (the exit attempt named in `action`) is satisfied even though no trap claim is made. Not violated.

**Rule 2 — `setup_action_continuity`.** `before.reached_by` is a continuous path inside the stated session — load the results view, Tab ×5 to the 'Renew' row action, Enter — with no reload or fresh load interposed between reaching the locus and pressing Escape. `before.locus` is a named AT position ("Details dialog open; focus on its heading 'Item details'"), not "the page", and `action` starts from that locus. Both packages carry one `session` each (2026-09-02-JR-a; 2026-09-05-MS-a), and neither straddles two. The assurance tier is worth naming rather than hiding: for human evidence this equality is self-reported, not a verified trace identity. The record says so, and the second package — not a stronger field — is the control. Not violated.

**Rule 3 — `natural_only_conditional_state`.** The dialog is reached through the product's own keyboard path under approved input. No state was induced, forced, or opened from developer tools, and no conditional state (empty result, error) is at issue. Not violated.

**Rule 4 — `passive_observation_binding`.** `observed_via: announcement` in both, and the `observed` line carries the AT's verbatim output for the control focus landed on ("Renew, button") plus a visible focus ring — the result of the action, bound to it. It is not an inspector-only reading, and it is not a restatement of `expected`: `expected` says "focus returns to the row-action trigger", `observed` names which control was announced and that a ring was visible. The tidy failure this rule catches — every field filled, `observed: "as expected"` — is not present. Not violated.

**Rule 5 — `ancestor_remapping_review`.** `target_reached: exact` in both. The target is the row-action trigger itself, and it is the control the announcement names. No nearest-ancestor substitution, so no frozen owner/descendant mapping is needed. Not violated.

**n = 1 at the fixed stage.** `closes` carries a closure item_id, so this PASS would back a fixed-stage `supports` and needs a second package. It has one, on the preferred branch: a different person (MS vs JR), a later date (09-05 vs 09-02), same pinned version 3.4.0, same trigger. Because the two are different people, at most one of them can be the fix's author, so "at least one of the two not by the fix's author" holds structurally. The different-person branch is the one that controls the confirmer's expectation, which is the error the reversed n = 1 rule exists to guard. Disposition **PASS**.

Two things I am not scoring as violations but that belong on the record: neither package discloses `self_attested`, and neither carries the evaluation window or report date that the walk-through requires as input #4. Neither is one of the five rules — these are attestation-roster and handoff concerns, not admissibility ones — so they go to `claim_boundary`, not to `rules_violated`.

## OP-FLASH — homepage carousel transition (Shape 2, attended non-media observation)

Shape 2. Rules 2 and 5 do not apply: no `before` locus, no action, and no descendant reached through an owner.

**Rule 1 — `bounded_diagnostic_not_promoted`.** This is the rule the package is built around, and it satisfies it. "A brief bright flash and a rapid alternation" is a bounded observation and stays bounded; it is not promoted to a 2.3.1/2.3.2 (or `9.A-Flashes`) failure. `adequacy` states plainly that the general and red flash thresholds cannot be decided by eye, that no longer look would decide it, and that the call needs a flash-frequency analyzer. Disposition is BLOCKED with that instrument named in `claim_boundary`. Not violated. A reviewer who upgraded this to FAIL on the strength of "it flashes" would be making precisely the promotion this rule forbids.

**Rule 2 — N/A** for Shape 2. `session` (2026-09-02-JR-b) still binds every line of the package to one sitting, and it does.

**Rule 3 — `natural_only_conditional_state`.** Applies unchanged, and holds. The carousel autoplays; the transition occurred on its own during the look. Nothing was staged, forced, or replayed to produce it.

**Rule 4 — `passive_observation_binding`.** The binding field is `played`, and it is narrow and honest: one capped first look at a single slide change, about two seconds, then looked away, no further attendance. `seen` reports only that one slide change and says so explicitly ("that is all that was attended"). No menu listing, player badge, or label is offered in place of an attended stretch. Not violated.

**Rule 5 — N/A.** The Shape 2 analogue is media identity, and `media` names the asset and where it sits on the sample; both the `played` and `seen` lines are about that same rendition.

**Safety clause and disposition.** Photosensitivity-class content is never walked by extended attendance: the walk is a capped first look (or a declined one), going straight to BLOCKED with the analyzer named. That is exactly what this package does — capped, ~2 seconds, no repeated cycles. And BLOCKED is the correct value, not UNTESTED: the person looked and could not decide, which is an admitted bounded observation about the operation standing without the reading that would settle it. UNTESTED means nobody looked, and collapsing this to UNTESTED would discard the observation in the one criterion class where human attendance is the only evidence there will ever be. Disposition **BLOCKED**.

Consequence downstream: a BLOCKED walk never attests. Closure `rem-carousel-flash-9a41` stays `draft_not_attested`, the walk is cited, and the analyzer is named as what would close it.

## OP-AD — audio description track for the training video (Shape 2, attended media)

Shape 2. Rules 2 and 5 do not apply.

**Rule 1 — `bounded_diagnostic_not_promoted`.** The `seen` line does contain a bounded passive observation — "Menu lists 'Described'" — but it is not what the conclusion rests on. The FAIL rests on `played` + `heard` over a named stretch: 0:40–0:55 played with the track selected, and the same stretch played again with it deselected. The bounded item is context, not the finding. Not violated.

**Rule 2 — N/A.** All lines sit in one session (2026-09-03-MS-c), including both plays, so the with/without comparison composes as one package rather than two sittings glued together.

**Rule 3 — `natural_only_conditional_state`.** Applies unchanged and holds. The track was selected from the player's own CC/AD menu — the user-facing path, an approved input. No state was staged in order to hear its alternative.

**Rule 4 — `passive_observation_binding`.** This is the rule that carries the whole binding load in Shape 2, and the package meets it on the strongest available shape. Every `heard`/`seen` claim falls inside an interval `played` names: the 0:40–0:55 silence and the 1:02 chapter-title utterance are inside 0:00–1:10 with the track selected; the without-track silence over 0:40–0:55 is inside 0:35–1:00 deselected; the on-screen error code at 0:44 is inside both. The A/B — the same stretch with and without the track — is what turns "the track is silent there" from an impression into an observation, and it is what rule 4 asks for. The menu listing is present but never stands alone. Not violated.

**Rule 5 — N/A.** Media identity is exact: named page, 3:40 runtime, player id 'walkthrough'; both plays are of that same rendition.

**Disposition and n = 1.** A single human FAIL sends the item back to remediation on its own — the reversal in the n = 1 rule applies only to a PASS that will back a fixed-stage `supports`, so no second package is required here and its absence is not a gap. Disposition **FAIL**. Closure `rem-video-ad-inadequate-77c2` stays `draft_not_attested` with the failing walk cited.

Where my confidence is lowest on this operation, and the reference agrees: `adequacy` is one line of judgment and is the whole finding for a media row — it is judged by the reader of the record, not by any check. What makes it admissible rather than an impression is that it is anchored to concrete named moments (the 0:44 error code, the silence across 0:40–0:55, the single second-voice utterance at 1:02) rather than a general "the description seemed thin". That is the floor the reference sets. It is a floor, not a standard: one silent stretch was checked, and the package's own `claim_boundary` says so.

## Package level

No operation's evidence breaks a rule, so `rules_violated` is empty and admissibility is ACCEPT. What ACCEPT does not mean is worth stating with the same specificity: it scores the evidence package, not the target's accessibility, and it does not make OP-RETURN a conformance verdict — the report's outcome map decides the criterion, and attestation only admits an improved term for publication. Two of the five rules (2 and 4) are structured self-report at the human-evidence tier rather than a verified identity and a source allowlist; these packages are admissible in that tier and no higher, and OP-RETURN's second confirmation is the only control that tier provides.

```yaml
admissibility: ACCEPT
dispositions: {OP-RETURN: PASS, OP-FLASH: BLOCKED, OP-AD: FAIL}
rules_violated: {}
claim_boundary: "OP-RETURN: two packages establish that Escape closed the Details dialog and returned focus to the 'Renew' row-action trigger on the results view at 3.4.0, confirmed by different people on different dates under Firefox 143 + NVDA 2026.1 and Chrome 141 + VoiceOver; undecided are every other dialog, every other AT/browser pairing, 2.4.3/2.4.7 across the sample set, and the criterion-level outcome, which the report's outcome map decides and this walk does not. OP-FLASH: a capped first look establishes that one slide transition of the promo carousel flashes and rapidly alternates at 3.4.0 and where it sits; whether it crosses the general or red flash threshold is undecided, and no length of human attendance would decide it — the missing instrument is a flash-frequency analyzer reading, so closure rem-carousel-flash-9a41 stays draft_not_attested; nothing about other slides, other carousels, or other pages. OP-AD: playing 0:40-0:55 with the 'Described' track selected and again deselected establishes that the description track plays silence over the stretch where the primary audio omits the settings panel and the on-screen error code at 0:44, so the description is inadequate for that stretch at 3.4.0 and closure rem-video-ad-inadequate-77c2 stays draft_not_attested pending remediation; the remainder of the 3:40 runtime, other videos, and caption/transcript adequacy are undecided. Package-wide: rules 2 and 4 are structured self-report at the human-evidence tier, not verified identity or a source allowlist; no package carries an evaluation window, a report date, or a self_attested disclosure, so window-fit and authorship-of-fix are undecided from this package alone."
```

**Provenance.** I read the operation-evidence admissibility protocol slice at `scratchpad/hv-rows/opevidence-protocol.md`; the evidence package under review at `scratchpad/hv-rows/stage/op-human-walkthrough-clean.md`; the walk-through reference at `<root>/.claude/skills/a11y-test/references/human-verification-walkthrough.md` (both package shapes, the per-rule field tables, the Shape 2 safety clause, the dispositions section, and the reversed n = 1 rule); and the "Human verification walk-through", "Operation-evidence admissibility", and "Structured disposition block" sections of `<root>/.claude/skills/a11y-test/SKILL.md` (lines 80–125), with `<root>` = `/Users/AlexUA_1/claude/accessibility-skills-51-receipts`. Nothing else in the repository was read or searched.
