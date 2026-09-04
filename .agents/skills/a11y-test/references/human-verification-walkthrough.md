# Human verification walk-through — the fixed-stage confirmation and the not-covered rows

A reference for the `a11y-test` skill, not a new skill: a11y-test already owns retest classification and operation-evidence admissibility, and this walk-through sits on top of both. It specifies how a **person** produces evidence that the rest of the bundle can admit — the observation behind a fix-closure record's `attestation` block ([A11y Fix-Closure Contract](../../../../docs/a11y-fix-closure-contract.md), "Attestation — the human tier"), and the only evidence there will ever be for the 13 ICT baseline rows the machine stack does not cover ([`ict-baseline-crosswalk.yaml`](ict-baseline-crosswalk.yaml), `coverage: not-covered`, `modes: [manual]`).

Two things it is not. It is not a free walk: a person clicking around a product and reporting "it's fine" produces nothing an operation can be bound to, and this reference refuses that shape by construction. And it is not an instrument choice: which overlay or analyzer a person holds while walking is parked (adoption assessment Q2) until this procedure has run once for real.

**Consequence level.** The record this produces is what `acr-reporting` admits an *improved* conformance term on. A wrong record here is a signed overclaim in a document someone may publish and defend — so the shape below is strict where a machine package is strict, and stricter in the one place a person is the weaker instrument: a single human PASS.

## When this runs

- **Fixed-stage confirmation.** A finding the prior evaluation carried is now `trend: resolved`, or a criterion appears in the report's re-evaluation delta as improved. The closure record exists and passes the closure rule (class-matched `interaction_evidence`). Before the improved term can publish, a named person confirms the fix on the pinned version and the closure gains its `attestation` block. This walk-through is that confirmation.
- **A not-covered baseline row.** Under a declared Revised Section 508 floor, `6.C-Captcha`, `6.D-ImageText`, `7.B-SensoryCharacteristics`, `7.C-AudibleCues`, `9.A-Flashes`, `16.A`–`16.D`, `17.E-ADPrerecorded`, `17.F-CaptionsLive`, `17.G-SyncMediaAlternative`, and `20.A-ConformingAltVersion` have no machine mode. Each is a judgment a person makes by looking, listening, or attending. They enter the evidence set as human-sourced packages in one of the two shapes below, take the same four dispositions as every other operation, and the crosswalk's coverage totals do not move — "covered" means the machine stack covers it, and it does not.

Under WCAG 2.2 AA with no floor declaration, only the first trigger applies; the baseline ids above are cited at declared-508 audit scope only, never in a component-scope review.

## Inputs — never a free walk

The walk is driven by the campaign, not by the person's curiosity. Before anyone touches the product, four things exist:

1. **The planned operation set.** The retest campaign's zero-unresolved contract enumerates every planned operation before the run starts. The human tier walks entries from that set — the ones the machine tier left `BLOCKED` or `UNTESTED`, the ones whose closure needs attestation, and the not-covered rows — and nothing off it. An observation with no planned operation to bind to is a note, not evidence.
2. **The closure records** for every finding under confirmation, each already passing the closure rule. The record's `original_observation` is the defect as diagnosed; its `interaction_evidence` names the evidence class. The person repeats *that class* of interaction — a keyboard path for a focus or operability defect, an assistive-technology announcement for a name, role, or state defect, a zoom and viewport check for a reflow defect. Confirming a focus-return defect by looking at a screenshot is the closure rule's failure, repeated by hand.
3. **The product version or content marker** the report names. It goes on every line the person writes and on the attestation block's `attested_against`. A delta after the walk expires the walk for any current-conformance claim, exactly as it expires frozen machine evidence.
4. **The evaluation window and report date.** Confirmations dated outside the window, or after the report, read as draft. Know the window before starting; do not discover it at handoff.

Missing any of the four: stop. The walk-through has nothing to bind its observations to.

## Order

Per sample, per finding, in the order the planned set lists them — the same sample-first traversal the machine campaign uses, so a per-sample evidence artifact gets its human lines appended beside its machine lines. For each finding: read the closure record's `original_observation` and `interaction_evidence`, derive `expected` from the original observation (the defect not reproducing is the expectation, stated concretely — "focus returns to the Renew card trigger", not "works"), perform the class-matched action from the record's stated starting point, write the lines below. Then the next finding on that sample. Then the next sample.

## Shape 1 — the operation package

One block per planned operation the person walked. Every field is required unless marked optional. The reviewer scoring this package applies the five operation-evidence admissibility rules from `a11y-test` SKILL.md unchanged; the table after the block says which field each rule reads.

```yaml
- operation: OP-RETURN                          # id from the planned operation set — never invented here
  closes: rem-focus-return-2c7f0a1b             # the closure item_id (fixed-stage) or the baseline test id (not-covered row)
  version: "2.14.1"                             # the pinned product version / content marker — must equal the report's
  session: 2026-09-04-JR-a                      # date + who + session letter; every line in one continuous sitting shares it
  tooling: "Firefox 143 + NVDA 2026.1, keyboard only"
  before:                                       # where the person was, and how they got there, in the same session
    reached_by: "Loaded /account, Tab ×4 to 'Renew card', Enter to open the dialog"
    locus: "Details dialog open; focus on its heading 'Renew library card'"
    announced: "dialog, Renew library card, heading level 2"   # what the AT said, verbatim as heard (or 'n/a — no AT')
  action: "Escape"                              # the keys, gestures, or AT commands, in order
  expected: "Dialog closes; focus returns to the 'Renew card' button"
  observed: "Dialog closed; NVDA announced 'Renew card, button'; visible focus ring on that button"
  observed_via: announcement                    # announcement | visible-focus | visual | inspector — see rule 4 below
  target_reached: exact                         # exact | "ancestor: <owner>, mapping <ref>" — see rule 5 below
  disposition: PASS                             # PASS | FAIL | BLOCKED | UNTESTED — the disposition block's closed set
  claim_boundary: "Focus returned to the trigger on this dialog at 2.14.1 with NVDA. Nothing about other dialogs, other AT, or 2.4.7 across the sample set."
```

| Rule (stable id) | What a machine package carries | What this package must carry | What the reviewer checks |
|---|---|---|---|
| `bounded_diagnostic_not_promoted` | a `focus_stagnation_observed` note kept bounded | a "focus seemed stuck" observation stays `BLOCKED` unless `action` includes the documented exit attempt (Escape, the exit keys) and `observed` reports what focus did | a `FAIL` on a trap or operability claim names the exit attempt in `action`; without it the disposition is `BLOCKED` and `claim_boundary` says the exit was not attempted |
| `setup_action_continuity` | `before` identity equals the setup's terminal identity, same session | `before.reached_by` and `before.locus` in the same `session` as `action`; the action starts from `locus` | `reached_by` is a continuous path in this session (no "fresh load" between reaching the locus and acting); `locus` is a named control or AT position, not "the page" |
| `natural_only_conditional_state` | a conditional state observed under an approved input, never induced | the same — a person may not edit a response, force an error, or trigger a state from developer tools; if the state did not occur under an approved input the operation is `UNTESTED` | `reached_by` uses approved inputs only; an `UNTESTED` conditional state is the correct disposition, not a gap the person should have closed |
| `passive_observation_binding` | a DOM/AX snapshot bound to the causing key press, source-allowlisted | `observed_via: inspector` (a browser accessibility pane, an overlay) is support bound to this `action` line and never the whole observation; a keyboard or announcement claim carries `observed_via: announcement` or `visible-focus` with the result of the action | an `observed` line whose only content is what an inspector shows, with no announced or visible result of `action`, does not decide reachability or announcement; neither does an `observed` that restates `expected` or says only "works" / "as expected" — the action is there, its observed result is not, and a package with every field filled and nothing observed is rule 4's failure in a tidier shape |
| `ancestor_remapping_review` | a reviewed, frozen owner/descendant mapping | `target_reached: exact`, or `ancestor: <owner>, mapping <ref>` naming the reviewed composite mapping the campaign froze | a person who reached "the filter" and reports on the option inside it, with no mapping cited, has not observed the target |

Two of these rules are weaker for human evidence than for machine evidence, and the record says so rather than hiding it. Rule 2's equality is self-reported: a trace proves its `before` identity, a person states it. Rule 4's allowlist is a vocabulary the person chooses from. What the shape adds is that the self-report is *structured* — a discontinuity or an inspector-only observation is visible on the record to a second person, instead of buried in "I checked it". That is the same tier of assurance `attested_by` has (a string nobody authenticates), and the same remedy applies: the second confirmation and the ACR's countersigned roster, not a stronger field.

**The under-specified package is inadmissible under the existing rules.** "I checked the dialog; focus return works now" has no `before`, no `action`, no `observed` result. Rule 2 cannot be shown without a starting locus, and rule 4 cannot bind an observation to an action that is not there — so the reviewer records `rules_violated: [setup_action_continuity, passive_observation_binding]` and the operation stays where the admitted evidence left it (`UNTESTED` if nothing else bears on it). The tidier failure — every field present, `observed: "as expected"` — is rule 4 alone: `before` and `action` are real, but no observed result of the action is bound to it, and an `observed` that restates `expected` is not an observation. No sixth rule is needed for either case; the package shape gives the five something to read.

A `session` is one continuous sitting on one build: it ends at a browser or tab close, at a reload or navigation that is not part of `reached_by`, or at a break long enough for the product to change under the person; whatever follows takes a new letter. Two packages in different sessions do not compose into one operation's evidence any more than two collector runs do. At the attestation level the same package is "a signature, not an observation" — the contract's fourth rule — and does not attest.

## Shape 2 — the attended-media package

`16.A`–`16.D`, `17.E`, `17.F`, `17.G`, and any attended observation about *content* rather than an operation have no locus identity and no key press. "The player menu lists an audio-description track" is precisely the passive observation rule 4 refuses to stand alone — it must bind to playing the track and hearing it. The package records what was played and what was heard.

```yaml
- operation: MEDIA-AD-ORIENTATION               # id from the planned set; the baseline test id in `closes` under a 508 floor
  closes: 17.E-ADPrerecorded
  version: "2.14.1"
  session: 2026-09-04-MS-b
  tooling: "Chrome 141, built-in player, headphones; no AT"
  media: "Orientation video on /new-members, 4:12, player id 'orientation'"
  expected: "A description track exists and speaks the visual information the primary audio omits during its silent stretches"
  played: "0:00–1:30 with the 'Described' track selected from the CC/AD menu; 0:40–1:10 again without it"
  heard: "With the track: a second voice describes the map, the card desk, and the on-screen phone number during the silent stretch at 0:48–1:05. Without it: silence over that stretch."
  seen: "Menu lists 'Described'; the on-screen phone number at 0:52 is not spoken in the primary audio"
  adequacy: "The description conveys the phone number and the room layout the primary audio omits — the visual information a listener would otherwise miss. Checked one silent stretch; the second stretch at 3:30 was not played."
  disposition: PASS
  claim_boundary: "Description present and adequate for the 0:48–1:05 stretch at 2.14.1. The 3:30 stretch is unchecked; nothing about other videos."
```

`played` is what the person actually played, with positions — a track listed in a menu is not a track heard, and an observation about a stretch that was not played is not an observation. `expected` is derived from the closure's `original_observation` (or, for a not-covered row, from the test's check) before playing, so the judgment has something to be compared against. `heard` and `seen` are the observation; `adequacy` is the judgment, and it is the one line that resembles `a11y-content-judgment`'s draft-then-ratify shape more than an operation trace: anyone can draft the observation, a named person owns the adequacy call, and a PASS needs the second confirmation like any other. Live captions (`17.F`) record the session time attended and the lag and accuracy observed; a transcript (`16.A`) records that it was opened and read against a played stretch, not that a link exists. A non-media attended observation — a flashing region, an audible cue — uses the same shape with `media` naming the content attended, `played` the interval watched or listened to, and `seen` or `heard` the observation; its honest indeterminate state is `BLOCKED` with the instrument named (below).

**Safety clause — photosensitivity-class content is never walked by extended attendance.** WCAG 2.3.1 / 2.3.2 (and `9.A-Flashes` under a 508 floor) exist because flashing content can induce seizures, and this is the one procedure in the bundle a person's body executes. Unaided viewing is also a bad instrument for the criterion: an eye cannot resolve three flashes per second, which is why the outcome is `BLOCKED` regardless of how long anyone watches. So the walk for this class is a **capped first look** — enough to record that the content flashes or alternates and where it sits, no continuous attendance, no repeated cycles — going straight to `BLOCKED` with the analyzer named in `claim_boundary`. A person may decline the first look without giving a reason; a declined look is recorded as `BLOCKED` with the instrument named, never as an `UNTESTED` gap, because no amount of human attendance would have decided it. A retest campaign that needs a 2.3.1 outcome plans the instrument, not the person.

The five rules read Shape 2 through different fields than Shape 1, and two of them do not apply — the package has no locus and no target on a focus path, so there is nothing for continuity or ancestor remapping to check:

| Rule (stable id) | Shape 2 reading |
|---|---|
| `bounded_diagnostic_not_promoted` | "menu lists a track", "looked rapid", "captions seemed late" are bounded observations; a `FAIL` or `PASS` on the alternative's *adequacy* rests only on `played` + `heard`/`seen` over a named stretch. A bounded observation with no played stretch behind it is `BLOCKED` (or `UNTESTED` if nothing was attended), never a conclusion. |
| `setup_action_continuity` | **Not applicable** — no `before` locus, no action. `session` still binds every line of the package to one sitting; a `heard` from one day and a `played` from another do not compose. |
| `natural_only_conditional_state` | Applies unchanged. Live captions are attended during a real session, an error announcement during a real error; a person may not stage the state to hear its alternative. |
| `passive_observation_binding` | The rule that does the work here. `heard` and `seen` are admissible only for stretches `played` names; a menu listing, a transcript link, a track label, or a player's own "described" badge is passive and never stands alone as evidence that the alternative exists or is adequate. |
| `ancestor_remapping_review` | **Not applicable** — no descendant reached through an owner. The analogue is media identity: the `media` line names the exact asset on the sample, and an observation of a different rendition (a different cut, a different page's embed) is not an observation of the target. |

## Dispositions for human observations

The four values and their meanings do not change. What this section adds is where a person's honest states land.

- **`PASS` / `FAIL`** — the person's observation decides the operation's predicate, exactly as a trace does. A person who pressed Escape and watched focus land on the trigger has decided the same thing the trace decides.
- **`BLOCKED`, not `UNTESTED`, for the indeterminate observation.** On `9.A-Flashes` or `7.C-AudibleCues` the honest state is often "I watched, or listened, and cannot decide without an instrument." That is an admitted, bounded observation about the operation standing without the reading that would decide it — `BLOCKED` by the disposition block's own definition, with `claim_boundary` naming the instrument (a flash-frequency analyzer; a sound-level or waveform capture). For the photosensitivity class the look is capped and may be declined — the safety clause under Shape 2 governs, and the disposition is `BLOCKED` either way. Collapsing it to `UNTESTED` — the value for *nobody looked* — in the exact criteria class where the human tier is the only evidence there will ever be throws the observation away.
- **`UNTESTED`** — nobody looked, or the conditional state never occurred under an approved input. Never a synonym for "looked and could not tell".

**The n = 1 rule runs the other way here.** Retest classification says a single failed reproduction is variance, not a finding, because the expensive error at diagnosis is a flaky miss reported as a regression. At the fixed stage the expensive error is the opposite: one human PASS becomes a `supports` in a published document, and the person confirming a fix knows what they expect to see. So:

- A **single `FAIL`** sends the item back to remediation. It does not need a second person; the fix is not confirmed, and the next retest is its second look.
- A **`PASS` that will back a fixed-stage `supports`** needs a second package — a different person, or the same person in a separate session on a later day — and at least one of the two not by the fix's author. That second package is the attestation block's `second_confirmation`; its `observed` line is what `second_confirmation.observed` summarizes. The two branches do not buy the same thing, and the record should not pretend they do: a **different person** is the control on expectation — the confirmer knowing what they expect to see; the **same person on a later day** controls only session and environment variance (a transient state, a cached build, a one-off announcement glitch) and leaves expectation uncontrolled, since the second walk carries more of it than the first. Prefer a different person for any `supports`-bearing confirmation; when the same-person branch is used, the roster shows one name twice and the reader of the ACR can weigh it.

## Recording and retention

- The per-operation blocks are appended to the sample's evidence artifact under the append-only retention rule, in a file named for what it is — `<sample>-human-walkthrough-<date>-<initials>.yaml` beside the machine run, never replacing it — and the artifact's `checksums.json` manifest (`references/hash-evidence.mjs`) gains the new file. A walk that overwrote the machine run would erase the one diff that shows where person and machine disagree.
- The closure record gains its `attestation` block **only on a walked `PASS`.** A `FAIL` sends the item back to remediation and the closure stays `draft_not_attested` with the failing walk cited. A `BLOCKED` walk is recorded and cited but does not attest either: the person looked and could not decide, so the closure stays `draft_not_attested` and `claim_boundary` names the instrument that would close it. The attestation contract's shape rules (a name, a pin, four method parts, two confirmations, dates) are necessary, not sufficient — an "observed: cannot determine by eye" satisfies the shape and must never carry `status: attested`.
- `method` is the summary of the operation block for that closure, in the contract's four parts. Shape 1 maps directly: `tooling`, `action`, `expected`, `observed`. Shape 2 maps as `tooling` ← `tooling`; `action` ← `played` (what was played, which track or alternative was selected, over which positions); `expected` ← `expected`; `observed` ← `heard` / `seen` plus the `adequacy` line. `attested_against.version` is the block's `version`; `attested_at` is the session date; `second_confirmation` summarizes the second package. The block *cites* the walk-through file; it does not replace it — the per-operation lines are the observation, the block is the record of who made it.
- The product version or content marker is on every block and on the artifact. A version delta after the walk expires the walk for current-conformance claims; the file stays as history.
- Where a not-covered baseline row is walked under a 508 floor, `closes` carries the baseline test id, and the finding or report row that results cites it in `baseline_test` exactly as a machine-covered row would — the walk-through changes who produced the evidence, not how the evidence is cited.

## Who signs

Whoever performed it. `attested_by` is the person whose hands were on the keyboard and whose ears heard the announcement; `second_confirmation.by` is the person who walked the second package. A lead who signs for a tester has put a name on an observation that name did not make — the same misattribution as an agent identifier in the field, and the block reads it as draft. When the attester authored the fix, `self_attested: true` is disclosed, and the second confirmation must be by someone else.

The block cannot bind a name to a person; the `acr-reporting` handoff's attestation roster, countersigned by the ACR's signing author, is where that binding happens. The walk-through's job is to make sure that when the roster is countersigned, there is an observation behind every name on it.

## What this does not establish

- **Not a conformance verdict.** A walked `PASS` decides one operation on one sample at one version. The report's outcome map decides the criterion; the ACR's term follows the outcome map; attestation only admits an improved term for publication.
- **Not an override of the machine tier.** Where a machine mode exists for the class, a human `PASS` beside a machine `FAIL` is a disagreement to resolve on the evidence, not a human trump. The walk-through fills the tier the machine stack does not reach; it does not replace the tier it does.
- **Not an instrument.** Whether a person walks with an overlay or an analyzer in hand is the parked Phase 3 question. Nothing here depends on it, and nothing here should be read as choosing one.
- **Not authentication.** `attested_by` remains a string. The structured `before` / `action` / `observed` lines make a second person's check possible; they do not make the first person's report true.
- **Not a change to the crosswalk's totals.** 22 / 26 / 13 / 1 stand. The 13 not-covered rows now have a procedure instead of a dead end; they are still not covered by the stack.

## Where confidence drops

- **Rule 2 and rule 4 are self-report for human evidence.** The shape makes a discontinuity or an inspector-only observation visible; it cannot make it impossible. The second confirmation is the control, and it is a control on the same self-report tier — and in its same-person branch it controls session variance, not expectation.
- **Shape 2 is scored by three rules, not five.** Rules 2 and 5 have no field to read in an attended-media package and are marked not applicable above; `played` carries the whole binding load. A bad Shape 2 package is caught by rule 4 or not at all.
- **`adequacy` is one line of judgment.** Shape 2's adequacy call is the whole finding for the media rows, and it is judged by the reader of the record, not by any check. One concrete moment checked, named with a position, is the floor this reference sets; it is a floor, not a standard.
- **No real walk has produced an attested closure yet.** This reference is specified from the contract and the disposition block, and exercised by the `a11y-test-operation-evidence` suite's human-sourced fixtures. Until one retest campaign has walked a closure, had `acr-reporting` admit its improved term, and had a signing author countersign the roster, the procedure is described, not demonstrated.
