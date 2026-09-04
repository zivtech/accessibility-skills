# n=1 reader-calibration checkpoint — first CURATED digest (manifest precondition `n-equals-1-calibration-checkpoint`)

**Date:** 2026-08-26. **Fixture:** `interactive-dropdown-focus-bug` (chosen first
deliberately — single driven-trace artifact whose ARIA `states` dicts exercise the
exact failure family the checkpoint names). **Reader:** `a11y-evidence-reader` agent
def, haiku (`claude-haiku-4-5-20251001`), fresh spawn, blind (artifact path +
adjudication question + question_source only).

## Draw 1 verdict: CHECKPOINT FIRED — reader-def hardening required, digest NOT frozen

Verified against the raw artifact
(`evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json`),
not just read for plausibility:

1. **Condensed `states` dict — the named failure mode, recurring despite 805c084.**
   Obs 1 is an ARIA-state observation (`expanded` false→true at `step_0002`). The raw
   step_0002 `ax_name_role_state.states` carries **7 keys** (`invalid`, `focusable`,
   `focused`, `hasPopup`, `expanded`, `controls`, `labelledby`); the digest's evidence
   block quoted only `expanded` + `controls`. `hasPopup: "listbox"` — directly
   load-bearing for a consumer's 4.1.2 mapping — was dropped. This is byte-for-byte
   the Phase 2.3 receipt's failure class (condensed states invited a wrong
   4.1.3-vs-4.1.2 mapping), reproduced at n=1 with the 805c084 def fix already in
   place: the prose rule exists in `<What_You_Emit>` and haiku did not honor it.
2. **Own-prose judgment in Obs 3.** "Expected behavior for a combobox or dropdown
   listbox pattern is focus should return to the trigger button" — forbidden on three
   counts: `expected_behavior` is a never-emit field, "should" in the reader's own
   prose is banned, and the APG-pattern expectation is training knowledge, which
   `<Blind_Reading>` forbids filling gaps with.
3. **`question_source` truncated.** The handed string's tail ("; no fixture metadata,
   rubrics, ground-truth files, or lane README consulted") was dropped. The scorer
   does not consume `question_source` (verified: no reference in
   `ollama/score_evidence_lane.py`), but §10 step 3 copies it verbatim from the frozen
   digest into the audit file — a truncated copy weakens the provenance chain F3a
   exists to keep checkable.
4. **Evidence lines are reconstructions**, not verbatim artifact bytes (e.g.
   `step_0001 (Tab): "expanded": false` is a composed summary line). Values accurate,
   format not verbatim — the def's "excerpts are verbatim" rule read loosely.

**What was correct (also calibration data):** evidence class declared
`mixed → keyboard-operability + name-role-state` with per-sub-question classes — the
Phase 2.3 single-class undercount did NOT recur. Question reproduced verbatim. All
four observations' values check out against the raw trace (no fabrication). Coverage
note present; absence claims carry queries. Obs 4's `states` dict (step_0003, 5 keys)
was quoted in full — the condensation hit the ARIA-state-change observation, not every
states dict uniformly.

**Disposition (per the manifest precondition's own rule):** treated as a reader-def
defect surfacing, NOT booked as pack-omission, NOT frozen. Draw 1 digest preserved in
the session scratchpad and summarized here; def hardened same day with three surgical
edits (`.claude/agents/a11y-evidence-reader.md`):

- `<Blind_Reading>`: question AND `question_source` both required verbatim-in-full
  (truncation named as a broken provenance chain).
- `<Output_Format>` observation template: new explicit `states:` line — "ARIA-state
  observations only: the artifact's FULL states dict, jq -c compact, every key — never
  selected keys".
- `<Output_Format>`: `actual_behavior` comment now "never what should happen, never a
  pattern expectation"; `evidence` comment now "verbatim artifact lines — copied bytes
  with … elision, never reconstructed summaries".

## Draw 2 (post-hardening re-run, haiku): CHECKPOINT FIRED AGAIN

**Def-version provenance settled first:** agent defs are **hot-reloaded at spawn
time**, not cached at session start — proven by adding a required `def_rev:
2026-08-26a` header line to the def and spawning a trivial probe (axe
`summary.json` question) from the same session: the probe emitted the marker.
Draw 2 was spawned after the three hardening edits landed, so **draw 2 tested the
hardened def**. (The `def_rev` header is now a permanent Output_Format field —
digest def-version provenance, same role `digest_content_hash` plays for content.)

Draw 2 results (verified against the raw trace):

- **Fixed by the hardening:** `question_source` verbatim in full; no own-prose
  "should"/expected-behavior sentence (Obs 3 states focus facts + the step_0006
  Shift+Tab recovery, all artifact-derived).
- **Still failing — full `states` dict:** Obs 1 (the `expanded` state-change
  observation) again quoted 2 of the raw step_0002 dict's 7 keys and omitted the
  new template's dedicated `states:` line. 2/2 haiku draws condensed, once per def
  version.
- **New failure — `wcag_or_apg` fabricated pass-through:** the raw trace contains
  ZERO WCAG strings (`grep -c "wcag\|WCAG\|4\.1\." → 0`), yet draw 2 emitted
  `wcag_or_apg: 4.1.3 Status Messages (WCAG 2.2)` (Obs 1) and `4.1.2 Name, Role,
  Value (WCAG 2.2)` (Obs 2). The rule is pass-through-verbatim-or-"not stated in
  artifact". Worse than a format violation: 4.1.3 on this exact observation is the
  documented WRONG mapping the Phase 2.3 receipt warned about (state exposed on
  the focused element — the real gap is 4.1.2 + APG operability). The reader
  derived and asserted it as if artifact-stated.
- Evidence lines remain reconstructed summaries rather than verbatim bytes (2/2).

**Control observation:** the same def at haiku on a simple machine-detectable
question (the def_rev probe) was flawless — jq-path handle, honest
`wcag_or_apg: not stated in artifact`, correct evidence class. The failure
clusters on keyboard-trace/ARIA-state extraction, not on axe extraction.

## Calibration ruling (n=2, recorded design amendment)

Per the def's own `<Model_Routing>` escalation path and §9.2's mandatory-sonnet
precedent: **this lane's CURATED digests run the reader at sonnet, uniformly for
all 6 fixtures** (uniform to keep the instrument constant across fixtures;
justified by 2/2 verified haiku non-compliance on the exact failure family the
checkpoint guards — silent states-dict condensation is the failure mode that
inflates R1's pack-omission number with an instrument bug's cost). Haiku remains
the def's default for ordinary (non-lane) use; the def's own text is unchanged on
that point. This is a §6.0-style amendment to §10 step 1's "haiku tier by
default", recorded here before any pack freezes.

## Draw 3 (sonnet, hardened def 2026-08-26a): PASS — checkpoint closed

Verified against the raw trace field-by-field (states dicts, text fields, name
strings, announcement strings — all exact):

- `def_rev: 2026-08-26a` stamped (hardened def provably in effect).
- **Full 7-key `states` dict verbatim** in the new dedicated `states:` field for
  the ARIA-state observation (`invalid, focusable, focused, hasPopup, expanded,
  controls, labelledby` — byte-matches raw step_0002). The failure family that
  fired in 2/2 haiku draws did not fire.
- **`wcag_or_apg: not stated in artifact` on every observation**, plus an
  absence claim carrying the exact grep proving the trace holds no
  wcag/sc/severity/impact keys — the draw-2 fabrication class did not recur.
- No own-prose "should"/expected-behavior anywhere; question + question_source
  verbatim in full; `evaluation_context` passed through artifact-stated;
  coverage note correctly declares the fixture's own sibling `.findings.json`
  NOT READ (F11-consistent, and it was never handed to the reader) and the two
  tool-types-without-paths as NOT READ rows; strong Not-claimed section.
- Bonus extraction both haiku draws missed: Obs 5 — visible trigger text
  changed to "Price: low to high▼" at step_0006 while accessible name and
  focus announcement stayed byte-identical to step_0001 ("Sort by") — a real
  name-role-state observation, stated flatly with handles, no judgment.

**Post-checkpoint instrument data (sonnet, remaining 5 digests):** question-header
fidelity was diffed against the manifest for every digest before freeze. 4/5 were
byte-exact on both question and question_source. `tabs-missing-arrow-nav`'s first
sonnet draw restated one character (`scan):` → `scan),`) — content otherwise
strong (the §9.3(c) grouped-PARTIAL glob row was exactly per contract, F11
exclusion honored, per-file jq sweep of the padding corpus). Disposition: not
frozen; re-run once with the same spawn prompt (the verbatim rule is the
provenance chain — §10 step 3 copies the question from the frozen digest, so a
one-character drift would surface as an audit defect). Recorded here as sonnet
question-fidelity slip 1/5.

**Checkpoint disposition:** `n-equals-1-calibration-checkpoint` flips done. The
lane's CURATED instrument is the hardened def (`def_rev: 2026-08-26a`) at
**sonnet** (recorded amendment above). Draw 3 freezes as
`interactive-dropdown-focus-bug`'s CURATED pack; draws 1–2 preserved as
calibration data, never packs. Ruling 5's ≠ assertion: sha256(draw-3 digest) is
recorded in the manifest `digest_content_hash` and differs from the Phase 2.3
worked-example digest hash
(`d248fe7bc7ce603a6de8615e73fa53570e8b2fa48fa8a9077dd959eb6c846a58`, extraction
rule recorded in the session scratchpad and reproducible from
`context-utilization-phase2/README.md`'s "Reader digest" section slice).

