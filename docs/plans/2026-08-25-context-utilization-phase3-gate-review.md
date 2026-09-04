# Phase 3 lane-setup gate review — bench-reviewer verdict (2026-08-25)

**Reviewer:** bench-reviewer (opus, high) per plan §Phase 3 gate line ("lane design + scorer reviewed by bench-reviewer before packs").
**Artifacts reviewed (uncommitted drafts):** `evals/results/context-utilization-phase3/README.md` (762-line revision incl. both orchestrator addenda), `evals/results/context-utilization-phase3/lane_manifest.yaml`, `ollama/score_evidence_lane.py`.
**Verdict: REVISE — packs must NOT proceed** until F1–F6 land. Disposition column to be filled by the fixer (lane designer) as fixes land; re-verification by the same reviewer before the pack phase opens.

Verbatim findings and rulings follow.

---

## VERDICT: REVISE — 6 blocking findings (F1–F6), 6 non-blocking (F7–F12)

The lane design is well-reasoned and every KAT citation in the README verifies verbatim; the blocker is that the *instrument* cannot measure what the lane registered.

Selftest: 10/10 PASS, exit 0. Scorer is 537 lines (≤800 ✓), longest function `score_row` = 50 lines (at limit ✓), zero hardcoded fixture lists — manifest is genuinely the source ✓. Index-stability docstring claim verified against score_output.py:373–378 ✓.

## BLOCKING

**F1 — CRITICAL — keyword matcher cannot discriminate on 5 of this lane's 9 must-finds (ceiling effect kills P1).**
`ollama/score_output.py:86-113` (`check_finding`) inherits its branch cascade + `fallback_keywords` (score_common.py:62-66, first 4 words, len>3). All 9 buggy must-finds were run against a response that reports NOTHING:
- heading-hierarchy-skipped [0] → kw `['heading','hierarchy','skips','from']` → **FOUND on the stopword "from"**
- heading-hierarchy-skipped [1] → kw `['inconsistent','heading','hierarchy']` → **FOUND**
- file-input-no-labels [2] → kw `['aria-invalid','when','error']` → **FOUND on "when"**
- interactive-dropdown-focus-bug [0] AND [1] → **both kw `['focus','restored']` — byte-identical** → both FOUND; the two items can never be told apart, and `find_evidence_quote` (score_evidence_lane.py:126-138) returns the *same line* for both.
5/9 must-finds are pinned TRUE regardless of model output. Measurable range collapses to 4 items, and one of those 4 is mis-branched (below). CURATED and DUMP will both sit near ceiling, so P1's registered ≥2-net-item effect has nowhere to appear.
Compounding: file-input-no-labels [3] "File type restrictions not announced" hits the `"announced"` branch → kw `['aria-live','role="alert"','live region','status message','4.1.3']`. That is a **3.3.2 labels/instructions defect routed to live-region keywords** — a model that correctly says "the accept attribute's restriction isn't conveyed" scores MISSED; a model mentioning aria-live for an unrelated reason scores FOUND.
Why adjudication does not save this: the failures are *false positives*, and this repo's documented funnel practice re-checks rows scoring **below** 100% ("for any fixture where the scorer's must-find detection rate is below 100% … manually re-extract"). Auto-matched positives would never be read.
FIX: add per-item `keywords:` overrides to `lane_manifest.yaml` (or to each completeness audit, already per-item), and have `score_evidence_lane.py` use them in place of `check_finding`'s inference. Leaves `score_output.py` untouched → no regression to historical rows. 9 items to hand-author; ~30 min. Calibrate by re-running the null-response test: all 9 must score False.

**F2 — MAJOR — README budgets from the superseded 16,157, and presents neither num_ctx branch.**
`README.md:325` ("16,157 tokens, run_benchmark.py:341-342") and the §4 table's "16.2K protocol + ~2K fixture" (`README.md:318-323`). Correct probe figures: 35b 14,276 protocol / +2,877 largest / +891 median; 32b 13,853 / +2,594 / +796. Note none of the 6 lane fixtures IS the largest (multistep-form-error-clearing); tabs-missing-arrow-nav is the median case, so real fixture cost is ~0.8–2.9K.
Recomputed, 35b, conservative: CURATED = 14,276 + 2,877 + 4,000 = 21,153; +8,192 = **29,345** vs 32,768 → 3,423 margin. But the guard's client-side estimate overstates ~7% (plan §6 guard-landing finding): 21,153×1.07 + 8,192 = **30,826** → only **1,942 tokens of real margin**. A 5K digest trips the guard and INVALIDates the CURATED@32K cell.
FIX: rewrite §4 from probes; add a **hard CURATED digest cap of ≤3,000 measured tokens**, probe-verified on the largest of the 6 fixtures before freeze.
Also: `run_benchmark.py:424-425`'s own CRITIC_CTX comment still cites 16,157 — stale, fast-follow (assigned to the runner-builder, since it is in ollama/ anyway).

**F3 — MAJOR — the three binding rules Phase 2's review created are absent from the README.**
Plan §6 Phase 3 now carries them at lines 112, 113, 117. `README.md` §9 (lines 413-431) reproduces only *Blind curation*, *Recorded-never-regenerated*, *Raw sets and padding*, *CLEAN packs*. **Missing: (a) question provenance** (per-pack verbatim question + author, attested authored without ground-truth access); **(b) question template** (one question per fixture, authored from artifact filenames + tool types only, recorded verbatim); **(c) haiku re-curation** (haiku packs carrying AMBIGUOUS / re-invoke-at-sonnet rows re-curated at sonnet before freeze).
Gate date **2026-09-01 IS present** (`README.md:401`, `lane_manifest.yaml:19`) ✓.
FIX: add all three verbatim to §9 and add a `question_provenance:` block per fixture in the manifest. (a) is also the mechanism that closes ambiguity 5 — see ruling below.

**F4 — MAJOR — `tool_observable` is defined "in principle", but used as if it meant "in this fixture's raw set" — corrupting the partition a pre-committed decision rule routes on.**
`README.md:483-488` defines it as "could **any** real tool run (axe or keyboard-a11y-tester) **in principle** surface evidence." `score_evidence_lane.py:141-154` then classifies against the actual pack. Consequence for an item that is in-principle observable but absent from *this fixture's* collected raw set: CURATED → `pack-omission` (blames blind curation), DUMP → `model-miss` (blames the model). Both wrong; the truth is "the lane never collected it." The plan's P2-fails branch routes explicitly on this partition ("the partition says whether curation or the model lost the item"), so a mislabelled partition corrupts a pre-registered decision rule.
This is live, not hypothetical: the README calls 3 of file-input-no-labels' 4 must-finds source-only, but by its own "any tool" definition items [1] (aria-describedby relation) and [2] (aria-invalid state) **are** tool-observable — KAT's own driven session on the sibling fixture proves that exact class (`keyboard-a11y-tester/README.md:103`, verified verbatim). Only item [3] is genuinely source-only.
FIX: split into two audit fields — `tool_observable` (informational, in-principle) and **`evidence_in_raw_set`** (bool, checked against the committed raw artifact). Classify: not in raw set → new `raw-set-gap` bucket (excluded from P1/P1b, reported); in raw set + CURATED + not in digest → `pack-omission`; in raw set + present → `model-miss`. Update `classify_miss` accordingly.

**F5 — MAJOR — three silent-default / aggregation defects that all bias toward the registered predictions.**
(a) `score_evidence_lane.py:150` — `if entry is None … return "not-tool-observable"`. An audit missing an `item_index` silently **excludes that item from the dilution comparison**. Should raise ScorerError. Same line: `.get("tool_observable", True)` / `:152` `.get("in_curated_pack", True)` — an absent or typo'd key silently becomes `model-miss` (blames the model). Absent key must be an error, not a default. **The selftest never exercises a malformed audit.**
(b) `aggregate_by_condition:270-289` keys by `condition` **only**, pooling qwen3.6:35b with the qwen3:32b control into one bucket — destroying the control comparison and the per-model P1/P1b the plan needs. Must key by `(model, condition)`.
(c) Same function: `agg["possible"] += mf.get("total")` counts **all** must-finds including `not-tool-observable` ones — directly contradicting README §10's "excluded from the P1/P1b dilution comparison." And `:282` drops `invalid` rows with **no count returned**, so a guard fire shrinks that condition's denominator invisibly instead of being visible.
(d) No per-item identity survives aggregation, so the plan's mandated per-item flip reporting cannot be produced. Key by `(model, condition, fixture, item_index)`.

**F6 — MAJOR — no runner exists, and nobody owns building one.**
`run_benchmark.py:452-470`: `run_ollama(model, fixture_id, system_prompt)` sets `num_ctx = CRITIC_CTX.get(model, CRITIC_CTX_DEFAULT)` — **one value per model**. The 2×2 requires per-*cell* num_ctx for the same model. No pack-injection path into the critic prompt exists anywhere in ollama/*.py. README §5 states a 74-row local matrix with no execution path.
FIX: name the runner as an explicit pre-pack deliverable with an owner and a size estimate. Minimum shape: `run_evidence_lane.py` taking `--fixture-id --condition --draw`, reading pack path + num_ctx from the manifest, injecting the pack into `PROMPT_PREFIX`, and reusing `context_overflow`/`write_overflow_row` unchanged. This is the single largest schedule risk against 2026-09-01 and the kill-rule.
**Orchestrator disposition: owner assigned same day — dedicated runner-builder agent (sonnet), spawned 2026-08-25.**

## NON-BLOCKING

**F7 — CONCERN — `done_reason == "length"` recorded but never flagged.** `score_evidence_lane.py:203`. Output clipping depresses recall, and clipping risk rises with prompt size — i.e. **higher in the DUMP arm, the direction that would falsely confirm P1**. Post-hoc exclusion is a researcher-degrees-of-freedom problem, so the rule must be registered before rows exist. Fix: set an explicit `output_clipped` flag and state the exclusion rule in README §5.

**F8 — CONCERN — CLEAN scoring emits a verdict and miscounts good behaviour.** `score_evidence_lane.py:312` prints `Status: PASS/FAIL` for CLEAN while the HAS-BUGS branch correctly prints "SCORED (candidate matches — content-adjudication required)". Worse, `count_false_positives` (score_output.py:140-143) counts any `Finding N:` regardless of severity, and **both** CLEAN fixtures carry exactly one legitimate `nice_to_find` ENHANCEMENT. A model that correctly reports the enhancement as a numbered finding scores an FP. This feeds P3 directly. Fix: README must state that P3's FP counts need the same adjudication pass and that a correctly-scoped `nice_to_find` report is not an FP.

**F9 — CONCERN — P1's ≥2-item threshold was never re-derived for this lane's pool.** The 2–3-item flip magnitude is documented against a **68-item** suite; this lane has **9** must-finds (6–8 usable after F4's fix). Fix: after F1+F4, re-derive and state the threshold in §6 with the pool size shown. Gate arithmetic: with F1+F4 fixed and file-input given AX evidence (ruling 6), 8 discriminating items × 2 draws × 2 models = 32 observations/condition; ≥2 net ≈ 6.25%, roughly 3σ against ~±0.7 items of pooled draw noise. **Powered — but only after those fixes.**

**F10 — CONCERN — `build_fixtures.py` path fix has a second-order trap.** `evals/results/keyboard-a11y-tester/harness/build_fixtures.py:8` hardcodes the old `a11y-meta-skills` path (confirmed). Repointing exposes **41** fixtures to a `SHIMS` dict authored for **33** — 8 fixtures render as bare `<Component />` and may fail. Fix: restrict the sweep to the 33 shimmed fixtures, or verify shims before the batch; carry as a manifest blocking checklist item with owner.

**F11 — OBSERVATION — `.findings.json` must be excluded from both arms.** §3's table lists `driven/X.{trace,findings}.json` as raw source for 3 fixtures. The trace is raw observation; **`findings.json` is a tool's conclusion in near-ground-truth language** — dumping it hands the model the answer in both arms. Binding: raw packs carry `.trace.json` only. (Padding use of *other* fixtures' `findings/*.json` is fine.)

**F12 — OBSERVATION — metadata schema inconsistency across the two CLEAN fixtures.** `modal-complete-clean.metadata.yaml` declares `false_positive_trap: 0`; `button-skip-link-clean.metadata.yaml` has no such category. Count-0 so nothing scores differently. Cosmetic.

## RULINGS ON §12 AMBIGUITIES 1–6

**1. Narrowest natural context — ACCEPT.** A uniform shell manufactures page-level findings absent from `expected_findings`, and manufactures **more of them in the DUMP arm** — a hidden confound biasing P3 toward its own prediction. Put that reason on the record in §3.
**2. `build_fixtures.py` deferral — ACCEPT, with F10's constraint attached.** Move from README prose into the manifest as a blocking checklist item with an owner, carrying the 41-vs-33 SHIMS constraint.
**3. Reuse vs fresh re-runs — REUSE.** Committed KAT driven traces *are* real tool output; they satisfy "where feasible" on the merits. The live risk is F11 (`.findings.json` is a conclusion, not an observation), not contamination. Fix F11 and reuse is strictly better.
**4. Unverified "should" string — ACCEPT the hedge, but make it mechanical.** At lane setup run axe once, grep output for `"should"`, record the actual rule id + verbatim string in that fixture's completeness audit before freeze. If `heading-order`'s real wording doesn't contain it, reassign the exercise to whichever fixture's real output does — **never synthesize one**.
**5. No mechanical guard against reusing the Phase 2.3 digest — NOT acceptable as prose.** The recorded verbatim question + attested author (F3a) makes a digest answering a different question detectable. Add: record a content hash of each frozen CURATED digest in the manifest and assert it differs from the committed Phase 2.3 digest.
**On the fixture swap: KEEP `interactive-dropdown-focus-bug`, conditional on F1.** Under the current matcher its two must-finds are keyword-identical and pinned TRUE (zero discriminating signal); with F1's per-item overrides that evaporates, and its already-validated Phase 2.3 chain reduces execution risk against a hard gate date. If F1 is NOT fixed, the fixture choice is moot — nothing in this lane can measure.
**6. `file-input-no-labels` denominator — fixture stays; fix the evidence set.** Per F4, only item [3] is genuinely source-only; [1] and [2] are AX-observable (proven by KAT's driven session on the sibling fixture). **Collect a keyboard/AX artifact for this fixture too** — `harness/drive.sh` already exists. That lifts the tool-observable pool from 6 to 8 items and resolves F9's power question directly.

## DUMP-CELL RULING (issued before the over/under probe verdict; both branches)

**Branch A — 49,152 HONORED for qwen3:32b:** cell fits (13,853 + 2,594 + 20,000 + 8,192 = 44,639 ≤ 49,152 ✓); no re-spec beyond F2's rewrite.
**Branch B — CAPPED at 40,960:** usable ceiling = 40,960 − 8,192 = 32,768. DUMP needs 34,447–36,447 → **over by 1,679–3,679; does not fit.** Max dump that fits = 32,768 − 16,447 = 16,321 tokens.
**Ruling: DUMP@40K with a resized dump DOES still answer P1 — but only if the dump is resized for BOTH models** (a 16K dump vs a 2–4K digest is still 4–8× payload ratio at a fitting num_ctx; running 35b on 20K and 32b on 16.3K would reintroduce the exact confound the one-num_ctx-per-cell clause kills and break the "same frozen packs" rule the hosted arm depends on). Under Branch B, P1b becomes different contrasts per model (32K→40K vs 32K→49K) and **must not be pooled**.
**Either-way recommendation: standardize the whole lane on num_ctx = 40,960.** It matches the repo's existing high-water mark (ACR lane, run_benchmark.py:613-616), makes P1b a matched 32K→40K contrast across both models, and removes the unexamined assumption on qwen3.6:35b's own declared context_length. Verify both models' `/api/tags` at lane setup regardless of the probe verdict. Sizing under that standard: dump target **~15,000 measured tokens** with ≥10% guard margin. The OVERFLOW receipt still works: 14,276 + 891 + 15,000 + 8,192 = 38,359 > 32,768 → guard fires ✓.

## WHAT MAY PROCEED

**Nothing beyond fixes.** Pack construction is blocked until F1–F6 land. F1 and F6 are the two that make the difference between a lane that measures and a lane that produces 120 rows of noise.

---

## Re-review (same day, 2026-08-25) — status before this disposition table

The gate re-reviewed the addenda-folded artifacts (the version predating this F1–F5
fix pass) and returned: **verdict still REVISE, blocking findings dropped 6→4.**

- **F3 — RESOLVED** by the re-review (the orchestrator addenda already covered
  question-provenance/template/re-curation in §9.1/§9.2 before this pass started).
- **F2 — RESOLVED**, residual = the ≤3,000-measured-token CURATED digest cap, which was
  already in this fixer's assignment and is applied below.
- **F1 / F4 / F5 — remained blocking going into this pass; fixed by it** (see the table).
- **F6 — covered**, not actually open: the re-review didn't know the runner-builder
  agent was already live and building `ollama/run_evidence_lane.py` in parallel.
- **F13 — new finding surfaced during this pass** (not in the original review): the
  Phase 0 overflow guard is blind to a model's declared `context_length`, confirmed
  MAJOR by the gate, credited to phase3-lane-designer, routed to the runner-builder as a
  Phase 0 fast-follow — not fixed in this lane's files.

## Disposition (fixer: phase3-lane-designer, 2026-08-25) — SELF-REPORTED, pending re-verification

Per this team's own standing practice, a fixer's "applied and verified" is not a substitute for the same reviewer re-checking the diff. This table records what changed and where; it is not a claim that the gate is closed. F1–F5 + F7–F12 + rulings 1–6 below; F6 (the runner) was owned and built by a separate agent (`ollama/run_evidence_lane.py`, phase3-runner-builder) and is not self-reported here.

| # | Outcome | What changed | Where |
|---|---|---|---|
| F1 | fixed | 9 must-finds' generic-cascade matching replaced with explicit per-item `keywords:` overrides; scorer raises `ScorerError` if an override is missing rather than falling back. Calibrated: null response scores 0/9; spot-checked positive direction (the dropdown pair now discriminates on trigger event). | `ollama/score_evidence_lane.py:164` (`match_must_find_item`), `:180` (`score_must_find_items`); `evals/results/context-utilization-phase3/lane_manifest.yaml:166,205,235,268` (`must_find_keywords`, 4 fixtures, 9 items); README §9.4 (line 723); selftest real-fixture calibration block |
| F2 | fixed | §4/§4.1 rewritten from the measured probe table (superseded 16,157 dropped); added a hard ≤3,000-measured-token CURATED digest cap, probe-verified before freeze. Noted: this doc's own line citations for this finding don't match the version being fixed — see README §12 item 9. | README §4 (line 345), §4.1 (line 379) |
| F3 | fixed (already landed via the prior orchestrator addenda; manifest block added this pass) | Question-provenance + template (a) and haiku re-curation (c) were already in §9.1/§9.2 from the same-day addenda pass preceding this gate. This pass adds the missing (per-fixture) manifest mechanism: `question_provenance:` block (adjudication_question / question_source / attested_no_ground_truth_access / digest_content_hash) on all 6 fixtures. | README §9.1 (line 609), §9.2 (line 659); `lane_manifest.yaml:108,133,154,200,230,257` (`question_provenance:`, all 6 fixtures) |
| F4 | fixed | Audit schema split `tool_observable` (informational) from a new `evidence_in_raw_set` (operative); `classify_miss` rewritten to a 4-bucket priority order (`not-tool-observable` / `raw-set-gap` / `pack-omission` / `model-miss`). `file-input-no-labels`' evidence-class claim corrected per ruling 6 (see below). | `ollama/score_evidence_lane.py:210` (`classify_miss`); README §10 (line 756, step 3/5 rewritten) |
| F5a | fixed | Every audit key (`tool_observable`, `evidence_in_raw_set`, `in_curated_pack`) now raises `ScorerError` if absent — no silent True/False default. New selftest case: a malformed audit entry (present item_index, missing key) → raises. | `ollama/score_evidence_lane.py:210` (`classify_miss`); `:605` (`_selftest_malformed_audit_and_raw_set_gap`) |
| F5b | fixed | `aggregate_by_condition` re-keyed to `(model, condition)`, never `condition` alone. New selftest: two models, same condition, land in separate buckets. | `ollama/score_evidence_lane.py:363` (`aggregate_by_condition`); `:629` (`_selftest_per_model_aggregation`) |
| F5c | fixed | `possible` denominator now excludes `not-tool-observable`/`raw-set-gap` misses via a new `_dilution_eligible_count` helper; INVALID rows counted per `(model,condition)` key (`invalid_rows`) instead of silently dropped. | `ollama/score_evidence_lane.py:350` (`_dilution_eligible_count`), `:363` (`aggregate_by_condition`) |
| F5d | fixed | New `per_item_rows` flattens to `(model, condition, fixture, item_index)` granularity for the plan's per-item flip reporting. | `ollama/score_evidence_lane.py:388` (`per_item_rows`) |
| F6 | not self-reported | Owned by phase3-runner-builder (`ollama/run_evidence_lane.py`, 597 lines, own selftest). This manifest carries the interface contract the runner reads: `pack_paths: {curated, dump}` per fixture, `conditions.local[].num_ctx`, top-level `draws`. Prompt-assembly order (previously undecided) confirmed via direct coordination. | `lane_manifest.yaml:280` (`conditions:`), `:294` (`draws:`); README §9.5 (line 742) |
| F7 | fixed | `output_clipped` (`done_reason == "length"`) added to every row; new selftest proves both directions. | `ollama/score_evidence_lane.py:256` (`_base_result`); README §5, §11 |
| F8 | fixed (code) + documented | CLEAN-row reporting changed from a bare PASS/FAIL to the same "candidate — adjudication required" framing as HAS-BUGS rows (`count_false_positives` itself, in `score_output.py`, deliberately left untouched per F1's "leave it untouched" instruction). README states the `nice_to_find`-is-not-an-FP rule explicitly under P3. | `ollama/score_evidence_lane.py:407` (`print_report`); README §6 (P3, line ~535) |
| F9 | fixed | Pool-size re-derivation done independently (not copied) — caught and corrected my own miscount mid-derivation (7 vs the correct 8) before presenting it; final numbers match the gate's. | README §6.0 (line 493) |
| F10 | fixed (checklist, not a code fix) | 41-vs-33 SHIMS constraint recorded as an owned, blocking manifest precondition. | `lane_manifest.yaml:48` (`build-fixtures-path-and-shims-check`) |
| F11 | fixed | Sourcing table + manifest `raw_source_note` updated to `.trace.json` only for the 3 driven-trace fixtures' own raw packs; `.findings.json` demoted to padding-only. Surfaced and resolved a second-order collision with the glob-partial-coverage exercise (README §12 item 11). | README §3 (line 268); `lane_manifest.yaml` (`modal-complete-clean`, `tabs-missing-arrow-nav`, `interactive-dropdown-focus-bug` `raw_source_note` fields) |
| F12 | noted, not fixed | Recorded as cosmetic per the gate's own characterization; no fixture-metadata edit made. | README §9 (CLEAN packs bullet) |
| F13 | confirmed by gate, routed elsewhere | New finding, surfaced by this lane's own §4.1 analysis (the Phase 0 overflow guard estimates against the *requested* num_ctx only, never a model's declared `context_length`) and confirmed MAJOR by the gate as escaping this lane's scope. Routed to the runner-builder as a Phase 0 fast-follow. **Not fixed here — `ollama/run_benchmark.py` is explicitly not touched by this pass.** | README §4.1, §12 item 12; `lane_manifest.yaml` `known_risks: f13-phase0-guard-blind-to-declared-context-length` |
| F14 | fixed (parts 1+2 of 3; part 3 routed) | Independently re-derived the full arithmetic before writing anything (est/measured ratios 1.224–1.297, 13,764-estimated-token guard headroom, 0.918 required ratio, 5,572-estimated-token CURATED headroom / 1.857 ratio) — all matched the gate's figures. Restated the binding dump spec in estimated tokens (§4.1a, new subsection), superseded the old measured-basis margin paragraph rather than deleting it silently, added the per-fixture pre-freeze assertion to §10 (new step 4, `rb.estimate_tokens(assembled_prompt) + 8192 <= 40960`, citing `run_evidence_lane.py --dry-run` as the mechanism), and flagged the still-open empirical question (does real JSON dump content clear the guard) as genuinely unresolved, not settled by this pass. Part 3 (estimate_tokens docstring + plan guard-landing-finding correction) explicitly left to the runner-builder, referenced not performed. Round-4 addenda: plan:80 dated blockquote correcting the "~7%" claim (round-3 ruling cited by name), and a drift caveat in §4.1a (durable ratio 1.22–1.30 vs. absolute counts tagged "pre-`805c084`", §10 step 4 confirmed not exposed to the drift since it estimates the then-current assembled prompt). | README §4.1a (new), §4.2 (DUMP@40K row marked UNVERIFIED), §10 step 4 (new), §12 item 13 (new); `lane_manifest.yaml` `preconditions: dump-spec-estimated-units` (done:true — restatement only, not per-fixture execution), `known_risks: f14-dump-json-tokenization-ratio-unmeasured`, per-fixture `dump_sizing:` blocks (6x, all TBD, drift note added), `dump-40k` condition note rewritten; `docs/plans/2026-08-24-context-utilization-plan.md:80` (new blockquote) |
| F15 | not mine (runner-builder, parallel fast-follow) | Stale "~7%"/16,157 comment surviving on `CHARS_PER_TOKEN_CONSERVATIVE` itself in both twins (`run_benchmark.py:35-38`, `ollama_a11y.py:37-40`) — three of four homes for this correction were fixed (plan doc, both docstrings); this fourth was found by the gate in round 4. Owned by the runner-builder, folded into their issue-#28 fast-follow. Not touched here — neither file is this lane's. | `ollama/run_benchmark.py`, `ollama/ollama_a11y.py` (runner-builder's files, referenced not edited) |
| F16 | fixed | README §9.1's question-template illustrative filename list named `<fixture-id>.findings.json` as an example artifact handed to the reader for a fixture's own pack — F11 excludes that exact pattern from a fixture's own raw pack (padding-eligible for *other* fixtures only). Removed it from the example list and, rather than a bare silent removal, added the exclusion rule inline in the template's own bracketed instruction — this template's actual audience is whoever operationalizes it into a per-fixture extraction (§9.6: the fresh question-authoring agent never sees this README directly, only a manifest-derived extracted list), so the constraint needs to reach that operationalization step, not just be implied by an example's absence. Landed *before* the `adjudication-questions-authored` precondition's fresh-agent pass, per the gate's ordering requirement. | README §9.1 (line ~802-805) |

**Rulings on items 4 and 5 (round 3) — read, understood, no action taken, as directed.** Ruling on item 4 (`flag_context_pressure` residual): fast-follow with an issue, not fix-before-packs — not this lane's file (`run_benchmark.py`/`run_evidence_lane.py`), not touched. Ruling on item 5 (pre-existing >50-line functions in `run_benchmark.py`'s other lane functions, +3 lines each from uniform threading): accepted as-is by the gate — not this lane's file, not touched, no action needed from the fixer.
| Ruling 1 | applied | Narrowest-natural-context rendering confirmed as designed; reasoning now on the record in §3, not just §12. | README §3 (line 268), §12 item 1 |
| Ruling 2 | applied | `build_fixtures.py` path-fix deferral moved from prose to an owned manifest checklist item (= F10's fix). | `lane_manifest.yaml:48`; README §12 item 2 |
| Ruling 3 | applied | Reuse (not fresh re-run) confirmed for the 3 committed-trace fixtures, now that F11 removes the contamination risk. | README §3, §12 item 3 |
| Ruling 4 | applied | "Should"-hedge kept but made mechanical: run axe once at lane setup, record the real rule id + string before freeze; reassign if `heading-order` doesn't carry it. | README §9.3 (line 676), §12 item 4 |
| Ruling 5 | applied | `digest_content_hash` field added per fixture; pack construction must assert it differs from the Phase 2.3 receipt's digest hash for `interactive-dropdown-focus-bug`. | `lane_manifest.yaml` `question_provenance.digest_content_hash` (all 6 fixtures); README §12 item 5 |
| Ruling 6 | applied | `file-input-no-labels` fixture kept; evidence-set corrected instead — a new keyboard/AX artifact planned (items [1]/[2] become tool-observable), lifting the lane-wide dilution pool from 6 to 8 items, resolving F9. | README §3 (table row), §6.0, §10 (audit-shape rationale), §12 item 6; `lane_manifest.yaml` `evidence_class_note` |

**New items surfaced during this fix pass, not in the original gate review** (recorded in README §12 as items 9–12): a likely stale-snapshot mismatch in F2's own line citations, and — separately, confirmed the same pattern recurred twice more this same day (a "still says CURATED@49K" report and an "F11 still lists findings.json" report, both against content already fixed in an earlier revision the reporter hadn't re-read) — item 9; qwen3.6:35b's declared `context_length`, since RESOLVED verified-safe by the 2026-08-25 ceiling probe — item 10; the glob-partial-coverage exercise's collision with gate F11's fix, resolved inline — item 11; F13, the Phase 0 guard's blindness to declared context_length, confirmed MAJOR and routed to the runner-builder — item 12 (also its own table row above).

**Ruling 7 and Ruling 8 also applied in this pass** (re-review deltas, not in the original six rulings' first pass): Ruling 7 finalized independent of the probe outcome (whole lane at num_ctx=40,960, one uniform ~15,000-token dump target across both models and all 6 fixtures — not resized per fixture/model; re-verified the "headroom" arithmetic and caught a mislabeling in my own first draft of it, corrected inline, README §4.2). Ruling 8 hardened: a new `adjudication-questions-authored` manifest precondition (a TBD field alone is not a gate); spawn-prompt recording required alongside each authored question for auditability; the fresh-question-authoring agent's README-blindness requirement named explicitly as a practical tension with a concrete resolution (README §9.6).

**Verification performed by the fixer before reporting** (not a substitute for re-verification): `score_evidence_lane.py` compiles, is exactly 800 lines (≤800), no function exceeds 50 lines, `score_output.py` is git-diff-clean (confirmed untouched); `--selftest` is 17/17 PASS including the real-fixture F1 calibration (9/9 must-finds score False on a null response) and positive-direction discrimination spot checks; `lane_manifest.yaml` parses and resolves via the manifest-driven CLI path from a non-repo-root cwd; README markdown tables pass a column-count sanity check.


---

## Final gate ruling (bench-reviewer, 2026-08-25, round 3)

**VERDICT: REVISE — one blocking item (F14). Packs may proceed the moment it is closed; nothing else blocks.**

Every fix from rounds 1–2 verified independently, live, against re-read files. This is a narrow spec defect, not a re-architecture.

### Independently re-verified (not accepted on report)

| Item | Method | Result |
|---|---|---|
| **F1** keyword ceiling | Ran my **own** adversarial null — plausible critic prose deliberately reusing the old trigger words ("heading structure", "focus", "when", "missing", "error") | **0/9** (was 5/9) ✓ |
| F1 discrimination | Dropdown selection-only / escape-only / both | `[0]` / `[1]` / `[0,1]` — clean separation ✓ |
| F1 non-degradation | True-positive prose per fixture | 9/9 recall ✓ |
| **F4** | `evidence_in_raw_set` split, `raw-set-gap` bucket, file-input manifest note | Present; note now correctly states only item [3] is source-only, citing `keyboard-a11y-tester/README.md:103` ✓ |
| **F5** | Fail-loud paths, `(model, condition)` keying, `output_clipped`, invalid visibility | Scorer selftest 22 checks ALL PASS, incl. all four cases I named ✓ |
| 800-line limit | AST scan + blank/comment ratio | 656 code+doc of 800; **no function >50 lines**. No padding games ✓ |
| **F6** runner | `--selftest` + `--dry-run` run by me | Both pass. Dry-run surfaces `declared_context_length`, effective ceiling, pack sha256, and an explicit placeholder caveat ✓ |
| **F13** guard | `python3 -m unittest ollama.test_context_guard` | 39 tests OK. `GuardedResponse(str)` intact at `ollama_a11y.py:190/271` ✓ |
| Ruling 7 | Manifest conditions | `curated-32k` / `curated-40k` / `dump-40k` / `overflow-32k` — adopted ✓ |
| Branch B | README:419–441 | Server-log WARN **plus** behavioral 45,176→20,482, **plus** the decisive control: 40,493 clean at `num_ctx=40960` requested exactly. Ruling 7 is empirically validated, not just argued ✓ |
| Plan annotation | plan:122 | Correctly annotates without editing history in place ✓ |

`NON_LANE_API_FUNCTIONS = {"check_ollama", "fetch_declared_context_length"}` — sound: both are metadata/health calls that carry no prompt, so gating them would be meaningless.

### F14 — BLOCKING — the dump spec is stated in the wrong units, and the freeze rule makes it uncorrectable after the fact

`estimate_tokens` (`run_benchmark.py:42-44`) uses `CHARS_PER_TOKEN_CONSERVATIVE = 3.5` and its docstring claims it "overestimates ~7%". **Measured against the very probes this lane budgets from, it overestimates 22–30%:**

| | est | measured | ratio |
|---|---:|---:|---:|
| protocol (35b) | 17,480 | 14,276 | **1.224** |
| protocol (32b) | 17,480 | 13,853 | **1.262** |
| protocol+tabs (35b) | 19,004 | 15,167 | **1.253** |
| protocol+tabs (32b) | 19,004 | 14,649 | **1.297** |

The guard gates on **estimated** tokens, but the lane's binding dump spec is stated in **measured** tokens. At `dump-40k`: `40,960 − 8,192 = 32,768` estimated available, minus `est(protocol+fixture) = 19,004`, leaves **13,764 estimated tokens of guard headroom for the pack.** A 15,000-*measured*-token dump therefore passes only if its est/measured ratio is **≤ 0.918** — i.e. only if the estimator *under*-counts the dump by ≥8%, the opposite direction from every ratio measured so far.

This is genuinely unresolved, not a predicted failure: JSON tokenizes densely (punctuation, quotes, braces), plausibly 2.5–3.5 chars/token, which could put the ratio near 0.7–1.0 and pass. **Nobody has measured it.** Scaling by the only ratio in hand (prose, 1.25) gives −4,602 (35b) / −5,163 (32b) — every DUMP row refused as INVALID, which is the entire dilution arm of P1.

**Why this blocks rather than waits:** §10's "recorded, never regenerated" rule means a wrong dump size cannot be corrected after freeze without violating the lane's own binding protocol. It must be measured *before* freeze. Nothing in the README or manifest currently asserts `estimate_tokens` against a real DUMP pack (grepped — zero hits), and the runner's dry-run honestly says "a real pack changes this estimate" without anyone having computed what it changes it *to*.

**Fix (small, three parts):**
1. Restate the binding dump spec in the units the guard gates on: **≤13,764 estimated tokens minus each fixture's own delta**, with the measured-token figure recorded as secondary.
2. At pack construction, before freeze, assert per fixture: `rb.estimate_tokens(assembled_prompt) + 8192 <= 40960`. Record **both** estimated and measured counts in the manifest.
3. Correct the `estimate_tokens` docstring and the plan's guard-landing finding ("overstates by ~7%, so true margins are thin rather than negative") — measured 22–30%. The consequence is asymmetric and worth stating plainly: measured margins are *looser* than believed, guard margins are *tighter*.

**Differentiated — CURATED is safe.** Same arithmetic at `curated-32k` leaves 5,572 estimated tokens for a ≤3,000-measured digest → ratio headroom **1.857**, comfortably above the observed 1.25–1.30. The ≤3,000 cap stands as-is; only the dump cell is at risk.

### Ruling on item 4 — `flag_context_pressure` residual: **fast-follow with an issue, not fix-before-packs**

Confirmed: called with the requested `num_ctx` at all 7 sites (`run_benchmark.py:591,684,750,827,908,1001`; `run_evidence_lane.py:368`), never `effective_ctx`. Three reasons it does not block:
1. **Unreachable in this lane.** All four cells are 32,768 or 40,960 against 32b's declared 40,960 — `min()` is a no-op in every one. It cannot fire here.
2. It is a **corroboration flag, not a gate.** The mechanism that actually refuses bad rows (`context_overflow`) correctly uses `effective_ctx` at `:64`, `:378`, `:433`.
3. The fix threads one argument across 7 sites — exactly the surgical edit that should not be rushed into a pre-pack window.

**Conditions:** file the issue with the direction of error recorded — when declared < requested it compares against the *larger* value, so it **under-reports** pressure, the same silent-under-reporting family as F13 itself — and leave an issue-referencing comment at `flag_context_pressure` so it is not lost.

### Ruling on item 5 — pre-existing >50-line functions: **acceptable; file `main` separately if desired**

Measured against `HEAD` rather than accepting the claim:

| function | HEAD | now | delta |
|---|---:|---:|---:|
| `run_ollama` | 79 | 82 | +3 |
| `run_perspective` | 71 | 74 | +3 |
| `run_evalreport` | 64 | 67 | +3 |
| `run_acr` | 63 | 66 | +3 |
| `run_planner` | 57 | 60 | +3 |
| `run_bugreport` | 53 | 56 | +3 |
| `main` | 261 | 261 | +0 |

**Zero functions newly crossed the threshold.** All six were already over; each grew by exactly +3 (uniform threading); `main` untouched. Refactoring six lane functions in a pre-pack window would be a large untested diff across every benchmark lane — worse risk/reward than +3 lines each. The debt is real, pre-existing, and not created by this work. The genuine debt is `main` at 261 lines, which predates all of it.

### Preconditions that remain open (tracked in `lane_manifest.yaml`)

- `build-fixtures-path-and-shims-check` — `done: false` (path fix + the 41-vs-33 SHIMS constraint)
- `adjudication-questions-authored` — `done: false` (fresh agent, per §9.6; spawn prompt recorded; fed only manifest-extracted paths, never this README)
- `n-equals-1-calibration-checkpoint` — `done: false`
- **New: dump-spec re-derivation in estimated tokens + per-fixture pre-freeze assertion (F14)**

### What may proceed

**Close F14 — restate the dump spec in estimated tokens and wire the per-fixture pre-freeze assertion — and packs may proceed** against the three standing preconditions above. F1's fix is real and verified by independent test, not by report; F6's runner works end to end; F13's clamp is proven by server log, behavioral replication, and a positive control. The lane can now measure what it registered.


---

## Final gate ruling (bench-reviewer, 2026-08-25, round 4 — FINAL)

**VERDICT: PASS. Packs may proceed against the standing preconditions below.**

F14 is closed correctly. All four blocking findings from rounds 1–3 (F1, F4, F5, F6) plus F14 are verified fixed by independent execution, not by report.

### Round-4 verification (live, re-read after concurrent edits)

| Check | Result |
|---|---|
| §4.1a restatement | 13,764 EST primary; 15,000 measured explicitly demoted to "SECONDARY/informational" in both README:581 and the manifest's `dump_spec_note` ✓ |
| Superseded paragraph | README:600–606 marked **in place**: *"Kept here only as the record of what this paragraph said before F14, not as a live claim."* Cannot be mistaken for live spec ✓ |
| CURATED re-derivation | 5,572 EST headroom / 1.857 ratio headroom, matching my own arithmetic exactly ✓ |
| §10 step 4 assertion | `rb.estimate_tokens(assembled_prompt) + 8192 <= 40960` per fixture per model before freeze; `--dry-run` cited as the mechanism; correctly distinguished from the no-regeneration rule ✓ |
| `dump_sizing:` blocks | Present on **all 6** fixtures, 5 keys each ✓ |
| New known_risk | `f14-dump-json-tokenization-ratio-unmeasured`, status `genuinely-unresolved-not-a-predicted-failure` — honest framing, matches my finding ✓ |
| Plan doc | plan:80 dated blockquote correcting the line-78 "~7%" claim, appended per the doc's own convention, citing the round-3 ruling ✓ |
| Docstrings, both twins | Corrected with my measured figures and the asymmetry framing; `3.5` unchanged ✓ |
| Issue #28 comment | `run_benchmark.py:421–427` — present, and it carries the direction-of-error condition I required ✓ |
| Guard tests | 39/39 OK; all four files `py_compile` clean ✓ |
| Selftests | Scorer ALL PASS, runner ALL PASS ✓ |
| **F11** (round 2) | Applied uniformly to all 3 driven fixtures, with the padding nuance correctly preserved — own `.findings.json` excluded from its own pack, padding-eligible for others ✓ |
| **Ruling 6** (round 2) | `file-input-no-labels` now gets a KAT driven session so items [1]/[2] become `evidence_in_raw_set: true` rather than a documented gap ✓ |
| **Ruling 5** (round 2) | `digest_content_hash` field exists, making the Phase 2.3 reuse ban mechanically checkable ✓ |

### The semantics concern — resolved

`dump-spec-estimated-units: done: true` **cannot** be misread as the per-fixture assertions having run. Its description scopes itself explicitly to the restatement ("README §4.1a restates the spec… and §10 step 4 adds the per-fixture pre-freeze assertion"), and the assertions carry their own independent per-fixture flag: **`asserted_before_freeze: False` on all 6**, with every `dump_sizing` value still `TBD`. Two separate tracks, correctly separated. This is the right design.

### New findings — both non-blocking documentation nits

**F15 — the stale "~7%" survives on the constant itself, in both twins.** `run_benchmark.py:35-38` and `ollama_a11y.py:37-40` still read: *"measured critic protocol = 60,373 chars / 16,157 prompt_eval tokens = 3.74 chars/token… so 3.5 overestimates tokens by ~7% — the safe direction."* That comment carries **two** superseded facts — the 16,157 protocol figure (already ruled superseded per plan F6) and the ~7% ratio — and it sits three lines above the docstring that correctly refutes it. The correction reached three homes (plan doc, both docstrings) and missed the fourth, which is the first place a reader looks. Real measured value is 4.23 chars/token (35b) / 4.36 (32b). Cannot affect any computed value. **Fold into the issue-#28 fast-follow.**

**F16 — the §9.1 question template lists an artifact F11 excludes.** README:803 offers `<fixture-id>.findings.json` among the example filenames handed to the reader. Under F11 that file is excluded from the fixture's own raw pack, so a fresh agent authoring questions from this template could enumerate an artifact that isn't in the pack. One-line fix to the illustrative list. **Do this one before the fresh-agent authoring pass**, since that pass consumes the template.

### Standing preconditions before packs freeze

1. `build-fixtures-path-and-shims-check` — `done: false` (path fix + the 41-vs-33 SHIMS constraint)
2. `adjudication-questions-authored` — `done: false` (fresh agent per §9.6; spawn prompt recorded; fed only manifest-extracted paths — **apply F16 first**)
3. `n-equals-1-calibration-checkpoint` — `done: false`
4. **Per-fixture dump assertions** — `asserted_before_freeze: false` ×6, gating freeze independently of precondition #4's `done: true`

### For the record — what pack construction must deliver before any row

I will review `completeness/<fixture_id>.audit.yaml` ×6 for:

- **Per must-find item:** `item_index`, `tool_observable`, `evidence_in_raw_set`, `in_curated_pack`, `raw_handle` — with `raw_handle` resolvable (jq path / trace step / file:line), because the audit must itself be re-checkable.
- **Provenance:** `adjudication_question` + `question_source` verbatim from the frozen digest, plus the authoring agent's spawn prompt. A placeholder or generic attestation fails.
- **Coverage note:** zero unresolved `AMBIGUOUS` rows, or the sonnet re-curation evidence showing they were resolved before the audit ran.
- **`dump_sizing` filled and passing:** `dump_estimated_tokens`, `dump_measured_tokens`, `est_measured_ratio`, `guard_ceiling_estimated_tokens`, `asserted_before_freeze: true` — for **both models**, since the two protocols differ by ~400 tokens.
- **The two Phase 2 exercises actually fired:** `tabs-missing-arrow-nav` shows one grouped `PARTIAL` glob row with N-matched/read/not-read counts; `heading-hierarchy-skipped` names the **real** axe rule id and its verbatim "should"-bearing string (or the reassigned fixture, if `heading-order`'s pinned wording lacks it).
- **`interactive-dropdown-focus-bug`:** `digest_content_hash` present and ≠ the committed Phase 2.3 digest.
- **`file-input-no-labels`:** items [1] and [2] recorded `evidence_in_raw_set: true` on the strength of the new KAT session — if that session doesn't happen, they revert to `raw-set-gap` and the P1 denominator drops from 8 to 6, which I would want flagged rather than absorbed silently.

One standing caution for the run phase, not a gate item: the JSON tokenization ratio is genuinely unmeasured. If the pre-freeze assertion fails on some fixtures, that is the instrument working as designed — resize the dump to the ceiling and record the real ratio. It is not a reason to raise `num_ctx`, which would break the symmetry ruling 7 established.
