# Chain Eval Protocol — /a11y-workflow End-to-End

> **Version**: 1.0  
> **Planned at**: commit `de0031f`, 2026-06-11  
> **Covers**: Mode 1, Steps 1–4 (Scout → Planner → Critic → Perspective Audit)  
> **Out of scope**: Steps 6–9 (implementation and test phases); requires an implementation to exist.

## Purpose

Measure the integration seams that single-agent benchmarks cannot see:

1. Does the scout output survive injection into the planner without critical loss?
2. Does the planner file-based handoff succeed (path exists, 9 phases present)?
3. Does the critic produce correctly calibrated per-perspective alarm levels?
4. Does the escalation decision trigger accurately (audit ⟺ MEDIUM/HIGH alarm)?
5. Does the audit scope stay within the escalated perspectives (no LOW leakage)?
6. Does the chain's most load-bearing finding survive end-to-end (tracer)?

These boundaries are invisible to isolated critic, planner, and perspective-audit benchmarks. A chain can pass all three single-agent benchmarks and still silently drop findings at handoff, hallucinate a file path, or over-escalate on CLEAN probes.

---

## Rubric Schema

Each `rubrics/<fixture-id>.chain.yaml` follows this schema:

```yaml
chain_fixture: <fixture-id>
source_suite: perspectives | a11y-critic
source_metadata: <path to the source .metadata.yaml>
target_dir: evals/suites/chain/targets/<fixture-id>/
expected_escalation: true | false | null  # MECHANICALLY derived from expected_alarm_levels
                                          # (true iff ANY perspective is MEDIUM/HIGH);
                                          # null when the source suite has no alarm ground truth
s4_graded: false                    # OPTIONAL — present (false) only when the source suite
                                    # carries no expected_alarm_levels; S4 is then observational
expected_escalated_perspectives: [] # OPTIONAL — for CLEAN fixtures that escalate narrowly:
                                    # the exact set of perspectives expected at MEDIUM/HIGH
expected_audit_verdict: PASS        # OPTIONAL — for CLEAN fixtures: the audit must come back
                                    # clean (no MAJOR/CRITICAL findings)
expected_alarm_levels: {}           # COPIED from source metadata (source_metadata is authority);
                                    # null when the source suite carries none
s3_scoring_mode: must_find          # OPTIONAL — a11y-critic-suite fixtures only; S3 scored on
                                    # must_find detection instead of alarm calibration
must_find_items: []                 # OPTIONAL — required when s3_scoring_mode is must_find
tracer_finding: "<verbatim most-important must_find description>"  # null for CLEAN fixtures
component_type: "<type string for S1 scoring>"
stage_notes: |
  Fixture-specific scoring notes for human scorers.
```

`expected_alarm_levels` is duplicated for self-containment. When values conflict, `source_metadata` wins. `expected_escalation` is never a judgment call — it is derived mechanically from the alarm ground truth using the workflow's own escalation rule (audit iff any perspective is MEDIUM/HIGH), or `null` where that ground truth does not exist.

---

## Measured Boundaries

### S1 — Scout Output

**Scoring dimensions (0–2):**
- **S1a** (1 pt): Output ≤ 2000 chars (hard; over budget = 0, under budget = 1). Raised from 1500 (plan 011, I7): all three pilot scouts ran 1779–2072 chars on multi-file directory targets, so 1500 was unrealistically tight.
- **S1b** (1 pt): Component type matches the `component_type` field in the rubric. Award 1 if the scout names the correct type or a close synonym (e.g., "modal dialog" matches "modal"). Award 0 if the type is absent or clearly wrong.

**Total S1**: 0, 1, or 2.  
**Note**: File coverage is not scored mechanically — the targets dir contains a README.md describing expected files; a scorer who sees the scout miss the primary component file should note it but may still award S1b if the description is correct.

### S2 — Planner Handoff

**Scoring dimensions (0–2):**
- **S2a** (1 pt): Plan file exists at `docs/a11y-plans/YYYY-MM-DD-<feature>-a11y-plan.md` (any date; file path must match the documented pattern from SKILL.md).
- **S2b** (1 pt): Plan file contains all 9 planner phases (look for phase headings or numbered sections 1–9). Award 1 if 8 or more phases are present; 0 if fewer than 8.

**Total S2**: 0, 1, or 2.

### S3 — Critic Alarm Accuracy

**For perspective-suite fixtures (1–5)**:  
Score each of the 7 perspectives against `expected_alarm_levels` using the alarm calibration convention:
- Exact match = 1.0
- Off by 1 level (e.g., LOW→MEDIUM or HIGH→MEDIUM) = 0.5
- Off by 2+ levels = 0.0

**S3 score** = mean across all 7 perspectives (0.0 – 1.0).

> **Plan 011 (I2)**: `score_chain.py` maps the critic's heterogeneous lens vocabulary onto the canonical 7 via a documented crosswalk (e.g. "low vision" → magnification_reflow; voice control / switch access / speech → keyboard_motor), taking the **highest** alarm when several lenses collapse onto one axis. A perspective the critic never raises is scored **LOW** (no alarm = not an alarm), **not** zero — penalising correct silence was the dominant S3 distortion (fixed: modal 0.214 → 0.71, login 0.43 → 0.86 against manual ~0.6 / ~0.86).

> **Plan 011 (M2) — the critic MUST emit a structured alarm table.** `parse_alarms` reads levels ONLY from markdown table rows (a leading perspective cell + a cell that is exactly `HIGH`/`MEDIUM`/`LOW`); the perspective is mapped from the first cell, so a rationale column may name other lenses without mis-binding. Prose is never parsed — pre-M2 the scorer scanned every line for a level substring, so "the screen reader experience is HIGH quality" and a one-line operator summary ("auditory: HIGH, screen_reader: MEDIUM, all others LOW") corrupted the alarm map. **The orchestrator prompt must therefore require the critic to emit its alarm levels as a table** (`| Perspective | Alarm |`, one row per lens). A critic that emits only prose scores no alarms (→ all LOW) — that is a protocol-compliance failure to fix in the prompt, not a scorer bug to paper over.

**For a11y-critic-suite fixtures (6–8)**:  
These fixtures do not have `expected_alarm_levels`. Score S3 on must-find detection instead:
- For each item in the fixture's `must_find` list: award 1 if the critic's output contains the finding (by concept, not necessarily verbatim), 0 if absent.
- **S3 score** = (items detected) / (total must_find items).

Rubrics for fixtures 6–8 contain a `s3_scoring_mode: must_find` field to flag this substitution to scorers.

### S4 — Escalation Decision (HEADLINE)

**Graded only where the source suite provides `expected_alarm_levels`** — fixtures 1–5. Fixtures 6–8 (a11y-critic suite) carry `s4_graded: false`: their source suite has no alarm ground truth, so there is nothing to grade the escalation decision against. For those fixtures, record whether escalation occurred as observational data; it does not enter the headline number or the PASS rule.

**The headline number is escalation accuracy n/6** (graded fixtures 1–5 plus the all-LOW probe 9).

**Binary 0 or 1 per graded fixture**:
- For HAS-BUGS fixtures (1–3): award **1** if the audit was invoked, **0** otherwise.
- For CLEAN fixtures (4–5), which carry `expected_escalated_perspectives`: award **1** only if the audit WAS invoked AND the escalated set matches `expected_escalated_perspectives` exactly (for both: `[cognitive_neurodivergent]`). Escalating on additional perspectives, or not escalating at all, scores **0**.

The CLEAN fixtures escalate by design: their source ground truth keeps `cognitive_neurodivergent: MEDIUM`, and the workflow's escalation rule is mechanical (audit iff ANY perspective is MEDIUM/HIGH). A ground-truth-matching critic therefore must escalate them — narrowly. The probe these fixtures provide is not "does the chain refrain from escalating" but "does the chain escalate on exactly the right perspective, and does the audit then come back clean" (`expected_audit_verdict: PASS` — see S5 and the PASS rule).

**This is the chain's primary quality signal.** A missed escalation on a HAS-BUGS fixture, or a scope-inflated escalation on a CLEAN fixture, is a chain failure regardless of per-stage scores.

**Scoring basis**: Check the session record for whether `perspective-audit` was spawned as a subagent, and (for fixtures 4–5) which perspectives the critic flagged MEDIUM/HIGH. If the session record is ambiguous, score 0.

**Never-escalate branch (plan 011 — now probed)**: fixture 9 `site-breadcrumb-nav` is a chain-native, genuinely all-LOW fixture (a correct WAI-ARIA breadcrumb). Its correct outcome is *no escalation at all*; a ground-truth-matching critic flags nothing MEDIUM/HIGH → S4=1, and that happy path IS the probe. It is chain-native precisely because no perspectives/a11y-critic fixture carries all-LOW levels (each "clean" one keeps `cognitive_neurodivergent` at MEDIUM, so it must still escalate).

> **Plan 011 (M1) — over-escalation here is OBSERVATIONAL, not auto-fail** (`s4_observational: true`). The chain critic reviews the planner's *plan*, not just the component, so it can raise a defensible plan-level concern the component-only ground truth omits (exactly what happened on `login-form-clean`, where reviewing the plan surfaced a real stale-error bug). A mechanical scorer cannot distinguish a genuine false-positive from a defensible concern, so an escalation mismatch on this fixture is **reported for human review** (`score_chain.py` prints `OBSERVATIONAL` and returns S4=None, which does not fail the PASS gate) rather than scored 0. Only a human can make that call. The trade-off is named honestly: this fixture can no longer *mechanically* catch a false-positive over-escalation — it surfaces the candidate; the operator adjudicates.

### S5 — Audit Scope Adherence (only when audit runs)

**Scoring dimensions (0–2)**:
- **S5a** (1 pt): Audited perspectives ⊆ escalated perspectives — no LOW perspectives were audited. Award 1 if every perspective discussed in the audit output corresponds to a MEDIUM or HIGH alarm level from the critic; award 0 if the audit discusses any LOW perspective with a findings-level treatment (brief mention in passing is acceptable).
- **S5b** (1 pt): Escalated perspectives receive substantive treatment. For HAS-BUGS fixtures: award 1 if the audit finds or reconfirms the primary must-find items for each escalated perspective; award 0 if a MEDIUM/HIGH perspective receives no findings-level treatment. For CLEAN fixtures (`expected_audit_verdict: PASS`): award 1 if the audit gives the escalated perspective a substantive review AND reports no MAJOR/CRITICAL findings; a MAJOR/CRITICAL audit finding against a CLEAN fixture is a false positive and scores 0.

**Total S5**: 0, 1, or 2. Score is N/A (not averaged) when audit does not run.

**Audit verdict (CLEAN fixtures only)**: where the rubric defines `expected_audit_verdict`, record the audit's verdict alongside S5. Expected PASS — no MAJOR/CRITICAL findings. This is the CLEAN fixtures' outcome probe and enters the PASS rule.

### Tracer Finding

A single named item (copied verbatim into each rubric's `tracer_finding` field) that represents the fixture's most load-bearing finding. The tracer is the item most likely to be dropped at a handoff — it is the chain's primary continuity signal.

**Check**: Is the tracer's concept present (not necessarily verbatim) in the LAST stage's output?
- If audit ran: check the audit output.
- If no audit: check the critic output.

**Score**: Binary 1 (present) or 0 (absent). N/A for fixtures with no tracer defined (fixtures 4 and 5, the CLEAN probes — tracers are not defined because no load-bearing finding exists).

---

## Per-Fixture PASS Rule

A fixture **PASSES** if ALL of the following hold:

1. **S4 = 1** (escalation decision correct) — applies only where `s4_graded` is not false (fixtures 1–5); for fixtures 6–8 this clause is skipped
2. **No stage scored 0** (every scored stage reached at least partial credit)
3. **Tracer survives** (1) where defined
4. **Audit verdict matches `expected_audit_verdict`** where defined (fixtures 4–5: audit comes back PASS, no MAJOR/CRITICAL findings)

A fixture FAILS if any applicable condition is violated. PASS/FAIL is the summary; per-stage scores are the diagnostic.

---

## The Chain Fixtures (8 source-derived + 1 chain-native all-LOW probe)

| # | Fixture ID | Source Suite | Difficulty | Why Selected |
|---|-----------|-------------|-----------|-------------|
| 1 | `modal-broken-focus-trap` | perspectives | HAS-BUGS | keyboard+SR alarms HIGH; audit MUST trigger; classic chain integration smoke test |
| 2 | `product-carousel-autoplay` | perspectives | HAS-BUGS | vestibular HIGH triggers audit on a non-keyboard perspective; tests whether the chain broadens past ARIA/keyboard framing |
| 3 | `video-tutorial-no-captions` | perspectives | HAS-BUGS | auditory HIGH; tests a dimension the critic historically under-weights; tracer is the caption track absence |
| 4 | `login-form-clean` | perspectives | CLEAN | narrow-escalation + clean-audit probe #1; ground truth keeps cognitive_neurodivergent MEDIUM, so the chain must escalate on cognitive ONLY and the audit must come back PASS |
| 5 | `article-page-clean` | perspectives | CLEAN | narrow-escalation + clean-audit probe #2; same expected alarm profile as fixture 4; second data point in a different domain |
| 6 | `tabbed-nav-vs-tab-pattern` | a11y-critic | ADVERSARIAL | verdict calibration through the chain; correct verdict is ACCEPT (or ACCEPT-WITH-RESERVATIONS) articulating the tradeoff — not flagging the ARIA as broken; S4 ungraded (no alarm ground truth) |
| 7 | `app-focus-order-illogical` | a11y-critic | FLAWED | plan-level reasoning required; compound interaction bugs invisible to ARIA checkers; tracer is the CSS order/DOM mismatch; S4 ungraded (no alarm ground truth) |
| 8 | `toast-notification-no-role` | a11y-critic | HAS-BUGS | known `role="alert"` discriminator item; tracer must survive to the critic stage; S4 ungraded (no alarm ground truth) |
| 9 | `site-breadcrumb-nav` | chain-native | ALL-LOW | never-escalate probe (plan 011); correct WAI-ARIA breadcrumb whose correct outcome is NO escalation; the only fixture where any escalation is an over-escalation (S4=0); S4 graded |

**Fixture table rationale**: Fixtures 1–3 cover the three most common audit-trigger perspectives (keyboard, vestibular, auditory). Fixtures 4–5 probe escalation precision with CLEAN components whose ground truth keeps exactly one perspective at MEDIUM (cognitive_neurodivergent): the chain must escalate narrowly — on that perspective only — and the audit must come back clean (PASS). Scope inflation at escalation, LOW leakage in the audit, or MAJOR/CRITICAL audit findings against these fixtures are the failure modes probed. Fixtures 6–8 add critic-suite coverage to validate that the chain's critic stage handles ADVERSARIAL, FLAWED, and discriminator-item cases correctly; their source suite carries no alarm ground truth, so their escalation decisions are recorded observationally, not graded.

---

## Scoring the Full Run

After all 8 fixtures are scored:

| Aggregate Metric | Formula | Watch Threshold |
|-----------------|---------|----------------|
| S4 Escalation accuracy | n correct / 6 (graded fixtures 1–5 + all-LOW probe 9) | < 5/6 is a chain defect; any miss warrants investigation |
| Audit verdict (CLEAN fixtures) | n PASS / 2 (fixtures 4–5) | any non-PASS is a false-positive failure |
| S1 mean | sum S1 / 8 | < 1.5 suggests scout output budget issues |
| S2 mean | sum S2 / 8 | < 1.5 suggests planner handoff issues |
| S3 mean | sum S3 / 8 | < 0.7 suggests critic calibration drift |
| S5 mean (audit fixtures only) | sum S5 / n_audit_fixtures | < 1.5 suggests audit scope creep |
| Tracer survival rate | n tracers survived / n tracer fixtures | < 5/6 suggests context compression loss |

Escalation decisions for fixtures 6–8 are recorded observationally (which perspectives the critic flagged MEDIUM/HIGH, whether the audit ran) but are excluded from the S4 aggregate — their source suite carries no escalation ground truth.

Fixture-level PASS rate (n PASS / 8) is the top-line summary. All 8 should PASS before the chain is declared production-ready.

---

## Pilot Plan & Outcome (Steps 1–4 complete; Step 5 RAN 2026-06-13)

The pilot uses 3 of the 8 fixtures:
- Fixture 1: `modal-broken-focus-trap` (HAS-BUGS with audit trigger)
- Fixture 3: `video-tutorial-no-captions` (HAS-BUGS, auditory dimension)
- Fixture 4: `login-form-clean` (CLEAN narrow-escalation + clean-audit probe)

This selection covers: one broad audit-trigger path, one historically under-scored dimension, and one narrow-escalation probe with a clean-audit outcome expectation. It validates all scoring dimensions (S1–S5 plus audit verdict). Note: the never-escalate branch of S4 is not covered — no fixture in the suite probes it (see the S4 known-limitation note).

**Cost estimate**: ~8–10 Opus-tier subagent calls for the 3-fixture pilot. Operator approval required before execution.

### Pilot Outcome (2026-06-13, operator-approved)

Ran the protocol set (modal, video, login) through the real chain — 12 subagent calls
(3 Haiku scouts + 9 Opus planner/critic/audit; all 3 fixtures escalated). Manual
(authoritative) results: **modal PASS, video PASS (S3 contaminated), login FAIL
(mislabeled fixture)**. Full record: `pilot/RESULTS.md`; findings: `pilot/PILOT-REPORT.md`.

**The full 8-fixture run is BLOCKED on instrument fixes — not merely pending.** The pilot
surfaced a CRITICAL contamination hole (a critic read the rubric; judgment stages are not
sandboxed and `targets/` sits beside the answer key in `rubrics/`), scorer-parsing defects
(perspective-taxonomy mismatch under-counts S3; literal tracer substring match false-negatives;
audit-verdict token match false-positives on checklist "PASS"), and one mislabeled fixture
(`login-form-clean` carries a real MAJOR stale-error-state bug). Until PILOT-REPORT findings
I1–I4 and I8 are fixed in a follow-up plan, the full run's automated scores would be
untrustworthy. The chain *under test* performed well (S2 handoff 2/2; audits caught a critic
false-positive and re-grounded an artifact mismatch; escalation mechanically correct on both
HAS-BUGS fixtures) — the blocker is the measurement apparatus, which is exactly what a pilot
exists to surface before the full run is funded.

---

## Run Hygiene (plan 011 — I1 contamination, I9 capture)

- **Isolation (I1, prevention)**: stage each target with `python3 stage_target.py <id>` and pass the judgment agents ONLY the printed path — a neutral `…/chain-stage/component/` dir outside the eval tree, so `..` reaches no answer key. The orchestrator must also instruct every stage not to read `rubrics/`, `*.chain.yaml`, `*.metadata.yaml`, or `evals/suites/perspectives/`.
- **Detection (I1, backstop — verbatim only)**: `score_chain.py`'s `detect_peek()` scans each stage's PRISTINE text for answer-key fingerprints; a hit marks the fixture CONTAMINATED and voids S3/S4/tracer (auto-fail). **It catches verbatim leaks only** (finding M4): a stage that read the rubric but paraphrased it evades the token scan — which is precisely what the 2026-06-13 video critic did (its "perfect" 7/7 came from the rubric, but it never echoed the answer-key strings into its own output). The operator flag below is what actually flagged it.
- **Pristine capture + operator zone (I9)**: each `<stage>.md` is the agent's output verbatim, followed by a single fenced operator zone the scorer strips before parsing:
  ```
  <!--OPERATOR
  peek: true            # operator integrity judgment: did this stage read the answer key?
  reason: |             # free prose; never scored
    critic navigated to rubrics/ and read expected_alarm_levels …
  OPERATOR-->
  ```
  `split_operator()` reads `peek:` from the zone FIRST, then removes the zone so `detect_peek` / the alarm-table / verdict / tracer parsers see agent text only. **The contamination gate is `peek flag OR detect_peek(pristine)`** — the human flag covers paraphrased peeks the token scan can't (the video case), and the flag is a deliberate integrity judgment with the same standing as the human-scored S1/S2, not the answer key. Without the zone, operator commentary that quotes the rubric (the pilot's first captures did) false-flags a blind stage — that was the login false-positive. Operator notes carry NO weight in the score beyond the structured `peek:` line.
- Fixture IDs must not encode their expected verdict; staging neutralises the path regardless.

## Known Limitations (plan 011 proposal-critic review, 2026-06-13)

Named honestly so no one reads more rigor into the instrument than it has:

- **detect_peek is verbatim-only (M4).** The automated contamination scan matches fixed answer-key tokens; a stage that reads the rubric and paraphrases evades it. The operator `peek:` flag is the only catch for paraphrased peeks, and it depends on a human noticing during the run — so contamination detection is *not* fully mechanical.
- **Staging is defense-in-depth, not a jail (M5).** `stage_target.py` puts the target outside the eval tree so `..` reaches no answer key, and the prompt forbids reading `rubrics/`. Neither is a filesystem sandbox — an agent that constructs an absolute path to `rubrics/` can still read it. The video pilot peek happened *with* the prompt instruction in place. Staging lowers the odds; the `peek:` flag + `detect_peek` are the backstops.
- **Crosswalk low-vision mapping is a one-way facet loss (M3).** "low vision" → `magnification_reflow` collapses a lens that spans BOTH magnification and contrast onto the zoom/reflow axis; a low-vision contrast concern is invisible on `environmental_contrast`. Documented and accepted (the canonical 7 has no combined low-vision axis); the alternative is standardizing the critic's output taxonomy upstream, out of scope here.
- **S5b is a presence check, not a coverage check (m1).** S5b awards 1 if each escalated perspective's name-stem appears in the audit text — it does not verify the audit substantively covered that perspective. A passing S5b means "mentioned," not "audited well"; the operator confirms substance by reading the audit.
- **The all-LOW fixture's over-escalation branch is observational (M1).** See S4 above — it surfaces candidate false-positives for human adjudication; it does not mechanically fail them.
- **No capture harness — discipline is hand-enforced.** The chain run is hand-orchestrated; nothing *enforces* the I9 pristine-zone format at capture time. `scripts/smoke_chain.sh` is the after-the-fact check that captures are well-formed and score as expected.

## Scoring Is Manual for S1–S2

S1 (scout char count and component type) and S2 (plan file existence and phase coverage) require the operator to examine the session record. `score_chain.py` automates S3–S5 from the rubric YAML and text output files — including the `s4_graded: false` skip, the CLEAN fixtures' escalated-scope check (derived from the critic's parsed alarm-table levels), and the I4 audit-verdict check (the explicit `Overall recommendation:` line + MAJOR/CRITICAL counts, not a bare "PASS" token). S1–S2 and audit-verdict confirmation are recorded manually in the results template.

This is the correct division: S1–S2 measure file system and prompt injection mechanics that only exist in a live session, while S3–S5 measure the text content of outputs against known ground truth. The scorer's audit-verdict check (I4) parses the recommendation line and counts MAJOR/CRITICAL markers — a heuristic, so the operator still confirms by reading the audit output.

---

## Maintenance Notes

- The `expected_alarm_levels` in rubrics duplicates source metadata for self-containment. On any metadata edit, re-sync the rubric (including the mechanically derived `expected_escalation` and `expected_escalated_perspectives`).
- S4 (escalation accuracy, n/6) is the number to watch over time — it is the chain's headline metric. Fixtures 6–8 are excluded (`s4_graded: false` — no alarm ground truth); fixture 9 `site-breadcrumb-nav` is the all-LOW never-escalate probe and IS graded.
- Capture hygiene (plan 011, I9): scored stage outputs (`<stage>.md`) are PRISTINE agent text followed by one fenced `<!--OPERATOR … OPERATOR-->` zone (with a structured `peek:` flag) that the scorer strips before parsing — see Run Hygiene above. Stage targets via `stage_target.py` (neutral path, no answer key copied); never let a judgment stage read `rubrics/` or `*.metadata.yaml`. Validate captures for free any time with `bash scripts/smoke_chain.sh` (unit tests + 3-capture integration re-score).
- Tracer-finding choices must be the genuinely load-bearing item (the one most likely to drop in context compression), not an easy keyword. Reviewer should scrutinize these on each new fixture set.
- CLEAN probes (fixtures 4–5) must NOT contain any hint of their cleanliness in extracted targets (no "CLEAN" or "ACCEPT" in the target files). Check this after running `extract_targets.py`.
- The `s3_scoring_mode` field in rubrics 6–8 signals the must-find substitution to human scorers.
