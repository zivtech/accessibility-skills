# a11y-critic rounds on the WP-B skill text (2026-09-02)

Gate for the "Structured disposition block" subsection added to
`.claude/skills/a11y-test/SKILL.md` (mirror byte-identical). Reviewer:
`a11y-critic` agent at opus, read-only, same agent across rounds. Round 1 was
against the spike § (a) draft with three deviations (INADMISSIBLE dropped,
semantics sentence, quoted claim_boundary); round 2 against the per-operation
rewrite plus the fourth fixture; round 3 against the two one-line NEW-1/NEW-2
fixes. Verbatim, recovered from the agent transcript.


---

## Round 1

**Verdict: REVISE**

Four of my six predictions confirmed; the two that mattered most confirmed harder than predicted. Deviations 2 and 3 are correct and I'd keep them; deviation 1 (dropping `INADMISSIBLE`) is correct in intent but left the ambiguity it was meant to remove.

## Findings

**F1 (MAJOR) — the enum contradicts the vocabulary it claims to inherit.** `SKILL.md:107`. Line 112 says "in the vocabulary above," but the vocabulary above is not four values. Line 63 mandates that `cantTell` / informational / skipped / blocked / untested "each stays a distinguishable, visible state," and line 85 requires every planned operation to carry "a disposition (pass, fail, or **one of the non-pass values above**)" — an explicitly open reference. The block closes it to four and silently deletes `cantTell`, `skipped`, and `informational`. A reviewer obeying line 63 who writes `cantTell` emits a value the scorer will score wrong, and the skill will have made line 63 unfollowable inside its own new block.
*Change:* `dispositions: {<operation id>: PASS | FAIL | UNTESTED | BLOCKED}` → add a sentence to line 112: "The four values are the closed set for this block; a state line 63 keeps distinct that does not map onto one of them (`cantTell`, `skipped`, `informational`) is recorded in `claim_boundary`, never collapsed into `BLOCKED`."

**F2 (MAJOR, the (b) trigger) — two defensible blocks exist for `op-dialog-escape-overreach`.** `SKILL.md:112`. The sentence gives two rules that fork on this fixture: the primary rule ("rejected evidence leaves the prior state in place") and the parenthetical ("a bounded diagnostic stays `BLOCKED`"). The fixture never declares a prior state for OP-CLOSE — unlike `op-empty-state-coverage-shortcuts.md:12,17`, which declares `UNTESTED` for both ops — and its action record never attempts the planned Escape at all, so `UNTESTED` is as defensible as `BLOCKED`. The fixture metadata does not break the tie either: it has no `expected_dispositions` key, and `nice_to_have` lists `"BLOCKED"` alongside `"inconclusive"` and `"re-run"` as equal alternatives.
*Change (two edits, both needed):* in line 112, make the parenthetical govern: "…leaves the prior state in place, and where no prior state was recorded the operation takes the state its own evidence supports — a bounded diagnostic with no exit-path trace is `BLOCKED`, an operation whose planned interaction was never attempted is `UNTESTED`." Then add `expected_dispositions: {OP-CLOSE: BLOCKED}` to `op-dialog-escape-overreach.metadata.yaml` so the fixture pins what the text now decides.

**F3 (MAJOR, the (c) answer) — mixed packages are undefined, and no fixture exercises the case.** `SKILL.md:106,108`. Package-level binary `admissibility` plus a flat `rules_violated` has no encoding for "OP-A's evidence is admissible, OP-B's is not." `ACCEPT` ratifies OP-B's bad claim; `REJECT` condemns OP-A's good evidence and, under line 112, rolls a legitimate `PASS` back to its prior state. I checked all three fixtures: none hits it — `op-dialog` has one operation, `op-empty` has a violation on each of its two, `op-retest-clean` has none. So the contract would be built and smoke-tested against a case set that structurally cannot expose the defect, while `op-retest-clean.md` (three operations) proves multi-op packages are in scope and real campaigns are mixed by default.
*Change:* attach violations to operations — `rules_violated: {<operation id>: [<rule id>, ...]}` — and redefine the package field as derived: "`admissibility` is `ACCEPT` only when no operation has a violation; a package with any violated operation is `REJECT`, and the per-operation map is what says which claims failed." Then add a fourth mixed fixture before the scorer is written.

**F4 (MAJOR, the (f) answer) — the block is not self-sufficient in its own prompt slice.** `SKILL.md:107,112`. In the slice (lines 91–112), `UNTESTED` is defined at line 97 ✓, but `BLOCKED` is **never defined** — line 95 says "the operation stays a collector block" in lowercase prose, and the token's definitional home is lines 59/61/63, outside the slice. Line 112's "a bounded diagnostic stays `BLOCKED`" is circular. `PASS`/`FAIL` are undefined in-slice too. This lands on exactly the value F2's fork turns on.
*Change:* in line 95, replace "stays a collector block" with "stays `BLOCKED` (a collector block, not a conformance outcome)" — one word, puts the definition inside the slice at no cost to the section's voice.

**F5 (MINOR, the (e) answer) — `claim_boundary` cannot fail as specified.** `SKILL.md:109`. The split is otherwise honest: judgment stays with the model (which rule ids apply, ACCEPT vs REJECT, each operation's state — none derivable without reading the setup/action records), and only equality-checking is mechanized. That is the `score_acr.py` precedent applied correctly. But `claim_boundary` is free text with no stated requirement, and the spike's check map (§b) assigns it none. A model can paste line 112's own last sentence and satisfy it. It will then be reported as boundary discipline it did not perform.
*Change:* pin the content — `claim_boundary: "<which operations this block decides, and which it explicitly leaves undecided>"` — which is checkable (every operation id must appear on one side or the other) and is the thing worth asserting.

**F6 (MINOR, the (g) answer) — the closing disclaimer is broader than the block.** `SKILL.md:112`. "This block scores the evidence package's admissibility, not the target's accessibility" is true of `admissibility` and `rules_violated`, but `dispositions: {OP-CLOSE: PASS}` in `op-retest-clean` *is* a claim about the target (the dialog dismisses on Escape and restores focus). The block disclaims something it does.
*Change:* "`admissibility` and `rules_violated` score the evidence package, not the target's accessibility; `dispositions` carries forward what the admitted evidence establishes about each operation."

Mirror verified byte-identical (`diff` clean). Deviation 3 (quoted `claim_boundary`) is correct — no finding.

## (b) The three blocks

```yaml
# op-dialog-escape-overreach
admissibility: REJECT
dispositions: {OP-CLOSE: BLOCKED}    # ← F2: UNTESTED is equally defensible on today's text
rules_violated: [bounded_diagnostic_not_promoted, setup_action_continuity]
claim_boundary: "Asserts the OP-CLOSE package is inadmissible; asserts nothing about whether the dialog dismisses on Escape."
```
```yaml
# op-empty-state-coverage-shortcuts
admissibility: REJECT
dispositions: {OP-EMPTY: UNTESTED, OP-OPTION: UNTESTED}
rules_violated: [natural_only_conditional_state, passive_observation_binding, ancestor_remapping_review]
claim_boundary: "Asserts three coverage claims are inadmissible and both operations remain uncovered; asserts nothing about whether the empty state announces or the option is reachable."
```
```yaml
# op-retest-clean
admissibility: ACCEPT
dispositions: {OP-CLOSE: PASS, OP-OPTION: PASS, OP-EMPTY: UNTESTED}
rules_violated: []
claim_boundary: "Asserts all three packages are admissible as submitted; OP-EMPTY carries no coverage claim and none is asserted."
```
Fixtures 2 and 3 are determinate — exactly one defensible block each. Fixture 1 is not.

## Not checked

- No CI gate run (`check_mirrors.py`, `validate_fixtures.py`, `smoke_scorers.sh`) — mirror identity verified by `diff` only.
- `ollama/score_acr.py` and `score_evalreport.py` not read; the precedent's actual extraction and verdict mechanics are taken from the spike's description, not verified.
- `docs/a11y-orthogonality-register.md` not read — the spike's cited `claim_boundary` precedent (its line 20) is unverified, so F5's fix is my proposal, not a match to an existing house form.
- The spike's measured claims (SKILL.md 1016 lines/78.5KB, `num_ctx` budget math, `section_span()` reuse) not reproduced.
- No model was run against the block — whether a local model actually emits parseable YAML under this template is unmeasured, and the qwen3.6:35b acr-reporting parse failure deviation 3 targets is therefore preempted in design only, not in evidence.
- SKILL.md outside lines 40–130 read only via the vocabulary grep above; other sections not reviewed for downstream conflicts.
- Whether `rules_violated` as a flat list survives contact with a real multi-dozen-operation campaign package (only the 1–3 operation fixtures were examined).

---

## Round 2

**F1 — CLOSED.** `SKILL.md:112`: "The four disposition values are this block's closed set… A non-conclusive run state outside the four (`cantTell`, `skipped`) is `UNTESTED` here and named in `claim_boundary`, never folded into `BLOCKED`." That closes the enum against line 63 without weakening it — line 63's "never collapse into pass or fail" survives, since `UNTESTED` is a non-pass value and the distinction is preserved in `claim_boundary`. `informational` is unnamed but is not a coverage state, so no gap.

**F2 — CLOSED, and your pin is better than mine.** I withdraw `OP-CLOSE: BLOCKED`. The chain is airtight in the new text: `setup_action_continuity` rejects the Session B record; "Rejected evidence never moves an operation"; "an operation with none takes only what its admitted evidence supports"; `UNTESTED` = "no admitted observation bears on it." Nothing admitted survives about OP-CLOSE, so `BLOCKED` would assert a bounded observation that does not exist. My round-1 reading treated the note as OP-CLOSE's simply because the run labeled it so — which is the exact error `setup_action_continuity` exists to catch. The inline metadata reason is correct as written.

**F3 — CLOSED.** `rules_violated: {<op id>: [...]}` plus "`ACCEPT` exactly when `rules_violated` is empty" makes package-level admissibility *derived* rather than independently asserted, which is what removed the undefined case. `op-mixed-package-partial` exercises it in both directions.

**F4 — CLOSED.** `SKILL.md:95` now carries the token, and `:112` defines all four in-slice. The prompt slice (91–112) is self-sufficient: `BLOCKED` :95+:112, `UNTESTED` :97+:112, `PASS`/`FAIL` :112.

**F5 — CLOSED.** `claim_boundary` is now per-operation and content-pinned ("what the admitted evidence establishes, and what it leaves undecided about the target"), so every operation id must appear on one side. Checkable; no longer satisfiable by pasting the disclaimer.

**F6 — CLOSED.** `SKILL.md:112` final sentence splits the disclaimer per field.

## NEW-1 (MAJOR) — `BLOCKED`'s definition omits the admissibility qualifier, giving `op-mixed-package-partial` a second defensible block

`SKILL.md:112`. Three of the four values are defined against *admitted* evidence — `PASS`/`FAIL` "mean **admitted** evidence decides"; `UNTESTED` "means no **admitted** observation bears on it." `BLOCKED` alone drops it: "a bounded collector observation *about that operation* stands without the trace that would decide it."

On the new fixture, OP-OPTION's DOM/AX snapshot satisfies that clause read literally: it is an observation, it is bounded, it is unambiguously *about* OP-OPTION (the popup's target item, `role=option`, `aria-selected`), and it stands with no trace that would decide reachability or announcement. A reviewer landing there writes `OP-OPTION: BLOCKED` — and the rubric's FAIL condition (`op-mixed-package-partial.rubric.yaml`, `status_semantics.FAIL`) names only "rolled up to PASS" and "mischaracterized as FAIL`", so `BLOCKED` would be scored FAIL against `expected_dispositions` on text that does not exclude it.

The counter-chain ("rejected evidence never moves an operation" → the snapshot is rejected → nothing admitted → `UNTESTED`) is the correct reading and is present, but it lives one sentence away and requires the reader to import "admitted" into a definition that pointedly lacks it while its three siblings have it. That asymmetry is the whole gap — and it is the same defect class as F2, now landing on the fixture built to close F3.

*Change (one word, `SKILL.md:112`):* "`BLOCKED` means an **admitted** bounded collector observation *about that operation* stands without the trace that would decide it."

Verified this does not disturb the other three: `op-retest-clean` OP-CLOSE keeps `PASS` (its bounded note is admitted, but the Escape trace decides it); `op-dialog-escape-overreach` OP-CLOSE becomes doubly determinate at `UNTESTED` (the note is rejected, so it cannot be admitted); `op-empty` unaffected.

## NEW-2 (MINOR) — `SKILL.md:95` states the `BLOCKED` consequence without the scoping the block adds

"Absent that trace the operation stays `BLOCKED`" is unqualified; `:112` adds "*about that operation*". Specific governs general and a careful reader resolves it, but `:95` is the rule bullet a reader hits first, and it is the sentence that made me write `BLOCKED` in round 1. *Change:* "…the operation stays `BLOCKED` **where the observation is admitted evidence about that operation**". Not a blocker on its own.

## The op-mixed block — one defensible block, once NEW-1 lands

```yaml
admissibility: REJECT
dispositions: {OP-CLOSE: PASS, OP-OPTION: UNTESTED}
rules_violated: {OP-OPTION: [passive_observation_binding]}
claim_boundary: "OP-CLOSE: admitted evidence establishes that Escape dismisses the dialog and returns focus to the row-action trigger; it decides nothing about the combobox popup. OP-OPTION: no admitted observation bears on it — neither keyboard-reachability nor announcement is decided in either direction, and the run's PASS is not carried forward."
```

A second defensible block exists **today**: identical except `OP-OPTION: BLOCKED` (NEW-1). After the one-word fix, no second block survives — `PASS` is excluded by `passive_observation_binding`, `FAIL` by "nothing admitted decides it in either direction," `BLOCKED` by the added qualifier. The fixture itself is well-built: single-rule on the violating side, both failure directions live, and `rules_violated_must_be_empty_for: [OP-CLOSE]` is the right shape for the contamination trap.

## Not checked

- No CI gate run (`check_mirrors.py`, `validate_fixtures.py`, `scripts/check_client_refs.py`, `smoke_scorers.sh`); mirror identity verified by `diff` only. The new fixture triplet is not registered in `run_benchmark.py`/`validate_fixtures.py` — out of this delta's scope, but it means no automated check currently sees the fourth fixture.
- `score_acr.py` / `score_evalreport.py` still unread; the `score_acr.py` precedent is taken from the spike's description.
- `docs/a11y-orthogonality-register.md` still unread — the `claim_boundary` house form is unverified, so F5's closure is judged against your stated intent, not against the register.
- No model run against the rewritten block; YAML parseability of the nested `rules_violated` map under a local model is unmeasured (the flow-map template `{<op id>: [<rule id>, ...]}` is more nesting than the round-1 shape, and the qwen3.6:35b parse failure that motivated deviation 3 is still preempted in design only).
- `RUBRIC_TEMPLATE.md` not re-read; it may still describe the round-1 flat-list shape.
- SKILL.md outside 91–118 not re-reviewed this round.

Verdict: REVISE

---

## Round 3

**NEW-1 — CLOSED.** `:112` now reads "an **admitted** bounded collector observation *about that operation*", restoring the qualifier its three siblings carry. Note your `:95` wording went slightly beyond my proposal — "where the **stagnation** observation is admitted evidence" — which scopes the clause to that rule's own observation class rather than to observations generally. That is the tighter reading and correct in context (the bullet is about `focus_stagnation_observed`); it does not narrow `:112`, which stays the general definition. No objection.

**NEW-2 — CLOSED.** `:95`'s consequence clause now carries the scoping, so the rule bullet and the block agree. The round-1 misreading that produced my `BLOCKED` pin is no longer available from either sentence.

**`op-mixed-package-partial` — exactly one defensible block survives.** Re-tested all four values against OP-OPTION's passive-snapshot-only record:

- `PASS` — excluded: `passive_observation_binding` rejects a snapshot with no causing keypress as standalone reachability/announcement proof.
- `FAIL` — excluded: `FAIL` requires admitted evidence to *decide* the predicate; nothing admitted decides it in either direction.
- `BLOCKED` — **now excluded**, which is the delta. The snapshot is rejected under `passive_observation_binding`, so it is not admitted; `:112` requires an *admitted* observation for `BLOCKED`. Under round-2 text this reading survived and produced the second block.
- `UNTESTED` — the only value left: "no admitted observation bears on it."

```yaml
admissibility: REJECT
dispositions: {OP-CLOSE: PASS, OP-OPTION: UNTESTED}
rules_violated: {OP-OPTION: [passive_observation_binding]}
claim_boundary: "OP-CLOSE: admitted evidence establishes that Escape dismisses the dialog and returns focus to the row-action trigger; it decides nothing about the combobox popup. OP-OPTION: no admitted observation bears on it — neither keyboard-reachability nor announcement is decided in either direction, and the run's PASS is not carried forward."
```

Re-checked the other three for collateral damage from the two edits: `op-retest-clean` OP-CLOSE stays `PASS` (its bounded note is admitted, and the Escape trace decides it, so `BLOCKED` does not apply); `op-dialog-escape-overreach` OP-CLOSE stays `UNTESTED` and is now determinate from `:95` alone as well as `:112`; `op-empty` untouched. Mirror byte-identical.

F1–F6 and NEW-1/NEW-2 all closed; nothing new introduced. Standing preconditions carried from round 2, deferred by agreement to the scorer build and not re-checked here: `RUBRIC_TEMPLATE.md` still describes the round-1 flat-list `rules_violated`; the fourth fixture is unregistered in `run_benchmark.py`/`validate_fixtures.py`; no CI gate run this round (mirror verified by `diff` only); the nested flow-map's parseability under a local model is still unmeasured — the qwen3.6:35b class of failure deviation 3 targets remains preempted in design, not in evidence.

Verdict: PASS
