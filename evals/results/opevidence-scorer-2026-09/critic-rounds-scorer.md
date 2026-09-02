# test-critic rounds on the opevidence scorer + canaries (2026-09-02)

Reviewer: `test-critic` agent at opus, read-only on the repo, running the
scorer against its own scratch probes (empty/prose-only/lowercase/flat-list/
unfenced/tab/unquoted-colon inputs, canary swaps, an all-five-rules over-flag).
Round 1 REVISE: over-attribution unpunished (F1), canary 35 a decoy (F2),
parse failures reported as absent block (F3), plus three MINORs. Round 2 PASS
after the fixes, with the 12 calibration draws re-scored live. Verbatim,
recovered from the agent transcript.


---

## Round 1

**Predictions → outcome**

| # | Prediction | Result |
|---|---|---|
| P1 | An assertion satisfiable by a different failure than the canary's name | **CONFIRMED** (F2) |
| P2 | A metadata key parsed but never consumed | **CONFIRMED-benign** (`why`, `notes`, `suite`, `input_format`, `difficulty`, `description` unread; `hook_absent_in_evidence` unwired **and documented**) |
| P3 | Format variants silently unparsed or crash | **CONFIRMED (no crash)** — tab and unquoted-colon `claim_boundary` discard the whole block (F3) |
| P4 | Empty/prose never PASS | **REFUTED (good)** — 8/8 FAIL, no crash |
| P5 | Negation strip evadable/over-fires | **PARTLY** — negated + interrogative survive, plain asserts FAIL; a ratification on a line with an unrelated "no"/"not" survives (inherited, documented upstream) |
| P6 | smoke false-pass path | **PARTLY** — no assertion-string false pass; crash is fail-closed (exit 1); `break` + PASS-only gold assertions are weak but not false-passing (F5) |
| P7 | A mutation the scorer can't distinguish from gold | **REFUTED for committed set** (all 26 fire) — but an entire *unrepresented* mutation class does (F1) |

**Findings**

**F1 — MAJOR. Over-flagging is unpunished on both REJECT fixtures; a "flag everything" review scores PASS.**
`op-dialog-escape-overreach.metadata.yaml` and `op-empty-state-coverage-shortcuts.metadata.yaml` have no `rules_violated_must_be_empty_for`, and `score_operation_evidence.py:check_must_catch/check_must_be_empty_for` (L189-206) only ever checks *presence*, never *absence of unexpected rules*. Probe: a response firing **all five** stable rule ids on OP-CLOSE (op-dialog) and on both ops (op-empty) → `Must misses: 0 / Should misses: 0 / Status: PASS` on both. This is precisely the failure `CLAUDE.md` names ("a critic that flags everything is dead — it just looks thorough"), and the suite has a false-positive control only in the ACCEPT direction (`op-retest-clean`) and per-operation only in `op-mixed`.
Change: add a scorer-side check — any rule id in `rules_map[op]` not in the fixture's `must_catch` for that op is a false fire (must-tier), gated on a new metadata flag (e.g. `rules_violated_exhaustive: true`) so partial-spec fixtures aren't broken; set it on all four fixtures; add two canaries (`opdialog-overflag`, `opempty-overflag`).

**F2 — MAJOR. Canary 35 (`opempty-misattributed-rule`) does not test misattribution; it is byte-swappable with canary 30.**
`smoke_scorers.sh:309` asserts `"rules_violated missing: natural_only_conditional_state under OP-EMPTY"` — *identical* to `smoke_scorers.sh:284` (case 30). The two response files differ only by an extra `natural_only_conditional_state` under `OP-OPTION`, and that extra rule produces **no output line at all** (same root cause as F1). Proof: swapping the two response JSONs → smoke still reports `49 passed, 0 failed`. The canary is named for a defect the scorer provably cannot see.
Change: fix F1 first, then assert case 35 on the false-fire line (`rule fired on … OP-OPTION: natural_only_conditional_state`) in addition to the missing line.

**F3 — MAJOR (mitigated). A colon or tab inside the block discards the model's entire judgment and reports it as "no structured disposition block found".**
`YAML_FENCE_RE` + `extract_disposition_yaml` (L67, L88-102) skip any fence that raises `YAMLError`, so `claim_boundary: OP-CLOSE: decided, OP-OPTION: decided` (an unquoted scalar with a colon — the shape SKILL.md's own template literally displays: `claim_boundary: "<per operation: what …>"`) yields 6 must-misses including `missing key: admissibility`, indistinguishable from a model that emitted nothing. Same for a tab-indented mapping. A correct ACCEPT/REJECT + correct dispositions + correct rules is scored as a total judgment failure on a quoting slip. *Mitigated by:* `score_acr.py:245` has the same conflation, so this is precedent-consistent, not novel; and it is fail-closed (never a false PASS).
Change: in `extract_disposition_yaml`, retain the highest-scoring fence that *failed* to parse and emit a distinct `must_miss` (`"disposition block present but not parseable YAML: <err>"`) so live rows are adjudicable; add a canary for it.

**F4 — MINOR. Zero canary coverage for the should-tier `hook_present` path.** Case 48 is the only WARN and it exercises `claim_boundary`. I verified by probe that `hook_present` is not a no-op (a gold block with hookless prose → `Status: WARN`, 2 hook misses), but nothing in the committed set would catch it becoming one. Add a `*-no-hooks` WARN canary.

**F5 — MINOR. `smoke_scorers.sh:31` `break` reports only the first failed assertion per case**, and the four gold cases assert only `Status: PASS` (no positive assertion that any must-catch actually fired). Drop the `break`; add `"+ bounded_diagnostic_not_promoted under OP-CLOSE"`-style progress-line assertions to the golds.

**F6 — MINOR. `rules_violated` as a flat list of *valid* ids is reported only as a shape error**, and because `normalize_rules_violated` returns `{}` (L166), `check_admissibility_consistency` then reports `REJECT but rules_violated is empty` — a second, misleading line. Also: lowercase `accept`/`pass` produce **duplicated** must-misses (unknown-value *and* mismatch, 7 lines for 4 fields). Case-sensitivity is defensible (SKILL.md declares an uppercase closed set) but is nowhere stated as case-sensitive; suppress the mismatch line when the value is already flagged unknown.

**Probe table**

| Probe | Input | Result | Intended? |
|---|---|---|---|
| 1 | `{"response":""}` × 4 fixtures | FAIL (6-9 must-misses), no crash | ✅ |
| 1 | prose-only × 4 fixtures | FAIL, no crash | ✅ |
| 2 | lowercase `accept`/`pass`/`untested` | FAIL, 7 must-misses (duplicated) | ⚠️ strict-by-design, double-counted (F6) |
| 2 | `rules_violated` flat list of valid ids | FAIL `must be a mapping` | ⚠️ (F6) |
| 2 | block unfenced (bare yaml) | FAIL `no structured disposition block` | ✅ contract says "one fenced yaml block" |
| 2 | ` ```YAML ` fence | **PASS** | ✅ `re.IGNORECASE` |
| 2 | tab-indented mapping | FAIL, reported as *absent* block | ⚠️ (F3) |
| 2 | unquoted `claim_boundary` with colon | FAIL, reported as *absent* block | ⚠️ (F3) |
| 3 | 26 mutations vs metadata | all FAIL/WARN, 25 with a unique diagnostic; 1 collision | ⚠️ (F2) |
| 3 | swap canaries 30↔35 | smoke still 49/49 green | ❌ (F2) |
| 3 | all-five-rules over-flag (op-dialog, op-empty) | **PASS** | ❌ (F1) |
| 5 | `we do not confirm '2.1.2 FAIL confirmed'` | PASS (survives) | ✅ |
| 5 | `Should the report say 2.1.2 FAIL confirmed here?` | PASS (survives) | ✅ |
| 5 | plain `2.1.2 FAIL confirmed.` | FAIL, fabrication | ✅ |
| 5 | ratification + unrelated "no" on same line | PASS (survives) | ⚠️ known line-level limit, inherited |
| 6 | malformed response JSON | script aborts, **exit 1** | ✅ fail-closed |
| 7 | registry entry with no files | `op-ghost-fixture not on filesystem`, FAIL | ✅ |
| 7 | files with no registry entry | `filesystem has op-retest-clean not in list`, FAIL | ✅ |

**Metadata-key table** (all keys present across the four files)

| Key | Consumer |
|---|---|
| `fixture_id` | printed (`run_checks` L211); also KeyError-guards the INCOMPLETE path |
| `expected_admissibility` | `check_admissibility` (must) |
| `expected_dispositions` | `check_dispositions` (must) |
| `rules_violated_must_be_empty_for` | `check_must_be_empty_for` (must) — **present only in `op-mixed`** |
| `expected_verdict_must_not` | `check_forbidden_phrases` (fabrication) |
| `must_catch[].id` / `.operation` | `check_must_catch` (must) |
| `must_catch[].hook_present` | `check_must_catch` (should) |
| `must_catch[].hook_absent_in_evidence` | **unwired — documented** in docstring pt 7 *and* inline at L204-205 ✅ |
| `must_catch[].why` | silently ignored (human-facing) |
| `nice_to_have` | printed only, never scored (labelled "informational only") |
| `suite`, `input_format`, `difficulty`, `description`, `notes` | silently ignored by the scorer; not read by `validate_fixtures.py` either |

**Pure-move check:** `strip_negation_lines` + `NEGATION_RE` moved verbatim from `score_evalreport.py` to `score_common.py` — diff is delete-and-insert of byte-identical body and comment, plus the import change. **Confirmed pure move.**

**Not checked:** live model rows (no Ollama call); `run_benchmark.py` `load_opevidence_system_prompt()` heading-anchor behavior against a mutated SKILL.md; the four fixture `.md` bodies vs. their metadata expectations (semantic ground-truth correctness of `expected_dispositions`); rubric `must`-tier dimension counts vs. the scorer's actual checks; whether `OPEVIDENCE_PROMPT_PREFIX` leaks rule names into the baseline condition; CI wiring of `validate_fixtures.py`/`smoke_scorers.sh`.

The instrument is fail-closed, correctly discriminates 25 of 26 committed canaries, and its INCOMPLETE/negation/registry paths all behave as documented. But it is blind in one whole direction — over-attribution — and that blindness is what makes canary 35 a decoy. For a lane whose stated purpose includes catching over-rejection, that is a gate, not a polish item.

Verdict: REVISE

---

## Round 2

**Round 2 — delta verification**

| F | Status | Live evidence |
|---|---|---|
| **F1** | **CLOSED** | `check_no_unexpected_rules` (`score_operation_evidence.py:216-236`), default-ON. My round-1 over-flag probes now FAIL: `d_overflag` → 3 `unexpected rule fired on OP-CLOSE:` lines, `e_overflag` → 7 lines across both ops. Fabricated ids are excluded via `rid in STABLE_RULE_IDS`, so `opclean-invented-rule` still reports one line, not two — no double-counting. `already`-skip correctly suppresses a duplicate on op-mixed's `OP-CLOSE`. |
| **F2** | **CLOSED** | Case 35 now asserts both lines (`smoke_scorers.sh:309-312`). Swap test redone: `FAIL: opevidence opempty misattributed-rule` → `52 passed, 1 failed`. The canary now discriminates. |
| **F3** | **CLOSED** | `extract_disposition_yaml` returns `(None, (body, err), text)`; both failure shapes now report distinctly — tab → `disposition block present but not parseable YAML: while scanning for the next token`; unquoted colon → `…: mapping values are not allowed here`; genuinely absent block still → `no structured disposition block found`. Canary 52 covers the colon case. Still fail-closed (never a PASS). |
| **F4** | **CLOSED** | Canary 53 asserts `hook not mentioned for bounded_diagnostic_not_promoted` + `Status: WARN` — the should-tier path is now pinned and can't silently become a no-op. |
| **F5** | **CLOSED** | `break` gone (`run_case` L25-33), so all failed assertions in a case report. All four golds carry positive progress assertions: opdialog 2 rules, opempty 3 rules, opmixed 1 rule, opclean `Rules violated: {}`. A gold can no longer pass on a no-op check. |
| **F6** | **CLOSED** | Lowercase probe: 7 must-misses → **4** (unknown-value only, mismatch suppressed via the `unknown` set). Flat-list probe: **1** line, reworded `rules_violated must be a mapping of operation id to rule ids`, and the bogus `REJECT but rules_violated is empty` second line is gone (`normalize` returns `None`, consistency check skipped). Case-sensitivity intent is commented at `check_dispositions`. |

**Regressions checked — none found**
- Empty / prose-only, all four fixtures: FAIL, no crash.
- Negation strip unchanged: negated → PASS, interrogative → PASS, plain assertion → FAIL (fabrication).
- ` ```YAML ` fence → PASS; unfenced → `no structured disposition block found` (correctly distinct from the new unparseable line).
- Smoke baseline: `Results: 53 passed, 0 failed`.
- **All 12 calibration draws re-scored live** against the new scorer: 8/8 `opevidence` PASS, 4/4 `baseline` FAIL, `unexpected rule fired` count = 0 on every draw, and each matches its committed `.score.txt` last line. The new must-tier check adds no false fires on real model output.

**Residual, non-blocking (no action needed this round)**
- `allowed_anywhere` (must_catch entries with no `operation:`) is dead code today — no fixture uses it. Harmless, and it is the right shape for future fixtures; noting only so it isn't mistaken for tested behavior.
- Ratification on a line carrying an unrelated `no`/`not` still survives `strip_negation_lines`. Inherited from `score_evalreport.py`, documented upstream, out of this change's scope.
- `suite` / `input_format` / `difficulty` / `description` / `notes` / `must_catch[].why` remain unread by the scorer (human-facing metadata); `hook_absent_in_evidence` remains unwired **and** documented in both the docstring and inline.

Every finding is closed by a mechanism I re-exercised myself rather than by an assertion string alone — the over-attribution blindness that made canary 35 a decoy is gone in both places at once, and the fix costs nothing on real draws.

Verdict: PASS
