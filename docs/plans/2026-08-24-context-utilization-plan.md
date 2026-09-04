# Context-Window Utilization Plan — measure first, curate second

**Date:** 2026-08-24 (revised same day per critic review — see companion `2026-08-24-context-utilization-plan-critic-review.md`)
**Status:** REVISED after proposal-critic REVISE verdict; all Critical/Major findings dispositioned (disposition table in the review doc)
**Scope:** How the a11y skills, agents, eval harness, and interactive audit sessions consume context windows; instrumentation to measure it; workflow changes to reduce it; an eval lane to test whether reduction improves accuracy — hosted and local. Scope explicitly includes clearing-or-annotating historical local benchmark rows if the Phase 0 retro-probe (§6, Phase 0.4) finds silent truncation exposure.

---

## 1. Problem statement

Accessibility work is evidence-heavy: axe JSON, keyboard traces, DOM snapshots, screenshots, reference standards. Today that evidence flows into the main context window at full fidelity and then *stays there* for the remainder of sessions that run 163–349 user-turns. The suspected costs: attention dilution on judgment tasks (hosted), silent truncation (local models at 32K), compaction churn that discards evidence mid-engagement, and cache-read spend.

The hypothesis to test, not assume: **carrying less irrelevant payload improves finding accuracy, with a larger effect on local models.** If the accuracy effect is zero for hosted models, the workflow changes still stand on cost/latency/session-longevity grounds — the plan pre-commits to naming which justification survived (§6 Phase 3 decision rules).

## 2. Execution model — subagent-first

Every task below runs as a spawned subagent unless it is (a) an interactive engagement step a human is driving, or (b) a gate/synthesis step whose value *is* the main session's accumulated context. The main session orchestrates, gates, and synthesizes; it does not read artifacts a subagent can digest. Depth-1 always (subagents never spawn subagents). Every subagent returns a summary + file paths per §5 principle 2 — the plan practices its own thesis. (Meta-receipt: this plan's own production used the pattern — session analysis via scripts, docs research, plan critique, archive mining, and arithmetic verification each ran as isolated subagents returning digests.)

Task tables below carry: **Executor** (agent def or main), **Model** (haiku/sonnet/opus per the routing rule: haiku = mechanical scans, sonnet = implementation/drafting, opus = judgment; the plan-gate critic runs at its def's own tier), **Effort** (reasoning-effort to encode at spawn or in the agent def: low/medium/high), **Size** (S ≤ half session, M ≈ one session, L > one session).

## 3. Measured baseline (2026-08-24)

**Method.** Two stdlib-only analyzers streamed every `*.jsonl` transcript under 9 session stores (`accessibility-skills` + 3 worktrees, `a11y-meta-skills` ×2 home-path variants, plus a client engagement's stores ×3 — identifier scrubbed per repo hygiene), attributing `tool_result` payload bytes to the producing tool via `tool_use_id` join, decoding PNG IHDR headers to estimate real image token cost, and separating main-window from subagent-window ingress. Scripts promoted in Phase 0; numbers below are from the 2026-08-24 run. Token estimates use chars/4 (text) and min(1600, px/750) (images) — approximations, good to ±30%, used for *ranking* only; every budget in §6 derives from **measured** tokens (`prompt_eval_count` probes), not these estimates.

**F1 — Read results are the dominant text payload.** 600 Reads of 318 files ≈ 7.7MB into context (2.5MB main / 5.2MB subagent). Bash, despite 2,491 calls, totals only 3.4MB (avg 1.4KB/call).

**F2 — The same files are re-read constantly.** 28 files were read ≥4 times ≈ 6.9MB of the Read total. Worst offenders: a deck HTML read 45× (3.8MB cumulative), `a11y-test/SKILL.md` 9× (619KB), `acr-reporting/SKILL.md` 18× across 18 sessions (514KB), `a11y-planner/SKILL.md` 6× (496KB). Repo-maintenance sessions pay a whole-file tax to edit large SKILL.md files. *Caveat resolved (Phase 0.1, 2026-08-24):* a uuid-level check of the worst case (the 45×-read deck file) found all 45 Read `tool_use` uuids distinct across 10 session files, zero cross-file duplication — **genuine re-reads, not transcript re-serialization double-counting**; two independent code paths (byte tally vs uuid scan) agree on 45×/10.

**F3 — Screenshots are byte-heavy but token-moderate.** ~50 browser-MCP screenshots ≈ 3.4MB bytes but only ≈55K estimated tokens (~1.1–1.6K each; the harness auto-downscales). Interactive retest sessions carry 7–10 shots (463–769KB) each. Separately, PNG files were *re-read* into context at 119–152KB apiece to "check" them. Inline screenshot returns (browser MCP) cannot be path-referenced — they enter context or they don't exist; file-based screenshots (agent-browser, Playwright, keyboard-a11y-tester crops) are on-disk artifacts that only enter context when Read. Images do not survive compaction. So the policy lever differs by tool: prefer file-producing capture, and Read image files only at visual adjudication points.

**F4 — The harness already persists large text outputs.** 79 tool-results files (6.0MB) sat on disk instead of in context across this repo's sessions (Bash inline cap ~30K chars via `BASH_MAX_OUTPUT_LENGTH`; a tool-agnostic persistence wrapper with ~2KB previews observed live; MCP output cap 25K tokens default via `MAX_MCP_OUTPUT_TOKENS` — figures from the 2026-08 docs sweep, to be pinned with a one-line receipt at Phase 0). This mechanism works; the plan builds on it rather than reinventing it.

**F5 — Subagent isolation works where used.** 89 Agent-tool returns totaled 0.1MB (~1.5KB avg) while subagent windows absorbed 5.2MB of Reads + 1.4MB of screenshots. The orchestrated `a11y-workflow` lane is already frugal *by design*: scout returns 500–1500 chars, plans hand off as file paths, keyboard-a11y-tester artifacts pass as paths (SKILL.md:35–38). The gap is everything *outside* that lane: interactive audit/retest sessions, direct `/a11y-test` usage, and repo maintenance.

**F6 — Local models are under real, measured context pressure.** Critic protocol: **16,157 tokens measured** (qwen3.6 tokenizer, `prompt_eval` probe, run_benchmark.py:341–342); gemma4 tokenizer 16,477. Planner protocol ~20.5K est., perspective ~5.9K est. (chars/4 — to be probe-measured at Phase 0). `CRITIC_CTX` maps the 2026-07/08 funnel cohort to 32,768; `CRITIC_CTX_DEFAULT = 16384`. The 2026-08-23 hardening (run_benchmark.py:414) exists because generation *already* hit `done_reason=length` — a thinking model that clips at num_ctx returns an empty scored response.

**F7 — Prompt-side truncation is currently silent, and the exposure is not hypothetical.** Runners record `done_reason` (output side, only since 2026-08-23) but never compare prompt size to `num_ctx`. **Verified 2026-08-24: `qwen3:32b` — the standing fallback baseline — has no `CRITIC_CTX` entry and therefore ran the critic suite at the 16,384 default, while the map's own comment says every measured current-gen tokenizer puts the critic prompt alone at ≥16.1K** (`PERSPECTIVE_CTX` does map it to 32,768, so the perspective lane is unaffected). Whether its historical rows were in fact truncated or clipped is an open empirical question — its high historical scores (65–68/68) argue something kept it functional (different tokenizer count, or truncation mechanics gentler than assumed). **Archived-artifact mining (2026-08-24, Phase 0.4a executed early) confirms the blindness:** the three eras (`ollama-blind`/`-dehinted`/`-rebaseline`, 174 committed qwen3:32b response files — 99 critic + 75 perspective) record **no `prompt_eval_count` at all** — the field appears only from the July–August lanes onward — while those newer lanes measure real qwen3:32b prompts at up to 25,006 tokens, and every mined row reports `done_reason: "stop"` — clean completion does not rule out a clipped prompt. Ollama's over-length behavior (what is dropped, whether the `system` block survives) is version-dependent and **must be established empirically, not assumed** — Phase 0.4's live probe is therefore the *only* way to settle the historical question; the Phase 0.2 guard makes it moot going forward. **Probe verdict (0.4b, 2026-08-24, Ollama v0.32.15):** qwen3:32b's tokenizer measures system+prefix at 13,853 tokens (leaner than qwen3.6's 16,157) and the largest critic fixture at 16,447 total — 63 tokens over the historical 16,384 window; the server did not trim the excess but **silently evaluated only 8,194 tokens (49.8%)**, deterministically across cache-cold and cache-warm draws. Prompt-side overflow is therefore bounded to the ~3 largest of 41 critic fixtures; **output-side budget** (≈1,700–1,900 tokens of generation for fitting fixtures) is the broader historical exposure, quantified from committed `eval_count` fields in the 0.4c analysis. Receipts: `evals/results/context-utilization-phase0/`.

**F8 — Long sessions multiply everything.** Top sessions run 163–349 user-turns. Ingress cost is paid once; carrying cost is paid on every subsequent turn (cache-read) until compaction discards it — and compaction discards *evidence*, not just noise. Transcript ingress ≠ context cost, but in sessions this long, early payloads dominate cumulative spend.

**What was NOT found:** no evidence that images are a token crisis (F3); no compaction markers detected in the top sessions (either large-context models or a marker format the analyzer doesn't catch — unresolved, nothing below depends on it); no Anthropic-shipped mechanism for a11y-artifact summarization (docs sweep, 2026-08 — see the watch rule in §7) — this workflow discipline is ours to build.

## 4. What already works — do not rebuild

| Mechanism | Status | Evidence |
|---|---|---|
| Large-output persistence to `tool-results/` files | Working, automatic | F4: 79 files / 6.0MB kept out of context |
| Subagent window isolation (final text only returns) | Working | F5: 89 returns / 0.1MB |
| a11y-workflow handoff discipline (summaries + paths) | Already specified | SKILL.md:35–38, teams/a11y-workflow.md:26 |
| a11y-scout strict return contract ("the structured summary — nothing else") | Already specified | a11y-scout.md:59 |
| Evidence-finding contract (stable IDs, selectors, fingerprints) | Exists — the natural return schema | docs/a11y-evidence-finding-contract.md |
| a11y-test evidence-class rule (screenshots are never interaction evidence) | Already specified | a11y-test SKILL.md:43 |
| MCP output cap (25K tokens default) / Bash inline cap (~30K chars) | Harness built-ins | docs sweep; pin at Phase 0 |
| Image auto-downscale on Read/screenshot | Harness built-in | docs sweep; F3 sizes confirm |

## 5. Design principles

1. **Evidence lives on disk; context carries claims + handles.** A handle is `file:line`, an axe rule id + selector, a `finding_id`, a trace step number — enough for any later reader to re-fetch the exact 2KB that matters. This is the evidence-finding contract's discipline applied to context flow.
2. **Summaries must carry verification handles, never replace them.** The rank-erosion failure mode (Dead Output: each pass loses information) is real for summarizer chains. Guard: exactly one summarization hop (artifact → contract-shaped digest); no summaries-of-summaries; every digest line cites the handle needed to check it against the raw artifact.
3. **Images enter context only when the defect class is visual.** The skill already says screenshots are not interaction evidence (SKILL.md:43). Extend that from *evidence admissibility* to *context admissibility*: interaction questions get text evidence (trace, AX tree, snapshot -i); pixels get read by the evidence-reader's vision mode, which returns a verdict — unless the main session itself must adjudicate a visual judgment (N≤2 images).
4. **Fail loudly on truncation.** Local runs assert prompt fit client-side; silent truncation (F7) becomes a hard error, not a mystery row.
5. **Measure, then claim.** Single-draw deltas are variance until adjudicated (funnel discipline). Accuracy claims come from the Phase 3 lane; predictions and their adjudication thresholds are registered in this document *before* rows exist.

## 6. Phases

### Phase 0 — Instrumentation (prerequisite for every claim that follows)

| # | Task | Executor | Model | Effort | Size |
|---|---|---|---|---|---|
| 0.1 | Promote analyzers to `scripts/session_context_report.py` (aggregate + `--drill`); self-validate one session's estimate against `/usage`-reported tokens to bound the ±30% (manual step, documented in the script docstring); settle the F2 resumed-session double-count question — **DONE 2026-08-24: all-distinct uuids, genuine re-reads (see F2)**; script landed, smoke-run reproduces baseline figures | general-purpose subagent | sonnet | medium | S |
| 0.2 | Truncation guard in `ollama/ollama_a11y.py` + `run_benchmark.py`: **client-side token estimate is the primary gate** (chars-based, per-tokenizer factor from probes), `prompt_eval_count` recorded as corroboration; lift hardcoded `num_ctx` literals into per-suite maps; **add the missing `qwen3:32b` CRITIC_CTX entry (32,768)**; response reserve 8,192 | general-purpose subagent | sonnet | medium | M |
| 0.3 | INVALID semantics: benchmark rows → `INVALID: context_overflow`, fixture fails loudly; interactive wrapper → output still emitted, loud stderr `CONTEXT OVERFLOW` banner + exit code 2 | (bundled with 0.2) | sonnet | low | — |
| 0.4 | **Retro-probe of historical rows** (M3): (a) mine committed response JSONs under `evals/results/` for `prompt_eval_count`/`done_reason` — **DONE 2026-08-24 (Explore/haiku): committed artifacts cannot settle it; the three critic-suite eras lack the field entirely** (see F7); (b) live `num_predict=1` probes — **DONE 2026-08-24: prompt-side overflow bounded to ~3/41 fixtures but the over-window case evaluated only 49.8% of its prompt (deterministic cache-warm — `prompt_eval_count` did NOT deflate on v0.32.15, easing M1 for this version); output-side budget ≈1,700–1,900 tokens is the broader exposure** (see F7); (c) **DONE 2026-08-24 — annotate, not clear:** output-side clipping **not in evidence** across all 99 critic rows (the naive ceiling formula flagged 44–50 rows but is falsified by the probe's ground truth — prompt truncation *creates* output headroom; corroborated by wrong-signed correlations, 0/99 unclosed `<think>`, legitimate endings); the standing asterisk is prompt-side only, on `multistep-form-error-clearing`'s three rows (~half the input silently absent). BENCHMARK.md annotated (dated section); receipts incl. `historical-exposure-analysis.md` | (b) general-purpose subagent (c) bench-reporter | sonnet / sonnet | medium / medium | S+S |
| 0.5 | Session-ledger convention: audit-scope engagements end with one `session_context_report.py` run stored beside engagement receipts | main session (one doc paragraph) | — | — | S |

*Gate:* scripts land with a smoke run on the current stores; **truncation guard verified in the failing direction cache-warm** — the same deliberately-oversized prompt run twice in succession, both draws must flag INVALID (defeats KV-prefix-cache deflation of `prompt_eval_count`, M1; the client-side estimate is deterministic by construction — verified by paired-draw tests — and the 0.4b probe additionally observed `prompt_eval_count` itself NOT deflating cache-warm on v0.32.15); `BASH_MAX_OUTPUT_LENGTH`/`MAX_MCP_OUTPUT_TOKENS` figures pinned with a one-line receipt (still open).

**Guard-landing finding (2026-08-24, recorded for fast-follow):** with the gate live, real current fixtures on the **planner / bug-report / perspective** lanes sit at or past their unchanged flat defaults (e.g., planner `test-simple-button` estimates ~24,597 tokens vs the 32,768 default with 8,192 reserve — 21 tokens over). The gate will correctly refuse these runs as INVALID instead of running them silently degraded. The conservative estimate overstates by ~7%, so true margins are thin rather than negative — but per-suite default raises are a *behavior-changing* decision (breaks comparability with historical rows) and are deliberately NOT bundled into Phase 0.2: they route through per-model probes at Phase 3 lane setup, or an explicit fast-follow with its own receipt line.

> **Correction, 2026-08-25 (Phase 3 gate ruling, round 3, finding F14 —** `docs/plans/2026-08-25-context-utilization-phase3-gate-review.md` **):** the "~7%" overestimate above does not hold. Measured against Phase 3's own real probes (`CHARS_PER_TOKEN_CONSERVATIVE = 3.5`, `run_benchmark.py:42-44`), the estimator overestimates by **22–30%**, not ~7% — see the gate-review doc's F14 for the measured ratios (1.224–1.297 across protocol-alone and protocol+fixture, both models). Stated plainly, per the gate's own framing: **measured margins are looser than believed; guard margins are tighter.** This does not retroactively invalidate the guard-landing conclusion above (per-suite default raises still correctly route through probes/fast-follow, not a bundled Phase 0.2 change) — it corrects the specific overestimate percentage cited as the reason true margins were "thin rather than negative." Left in place rather than edited out, per this document's own history-stays-legible convention (see the num_ctx=40,960 annotation above the Phase 3 cell table). `estimate_tokens`'s docstring itself (the ~7% claim's other home) is corrected separately, per the gate's F14 routing, not in this plan doc.

### Phase 1 — Consumption discipline in the skills (prompt-repo edits)

| # | Task | Executor | Model | Effort | Size |
|---|---|---|---|---|---|
| 1.1 | a11y-test SKILL.md "Evidence consumption" subsection (≤1.5KB in body) + `references/evidence-extraction.md` (jq recipes: axe → [rule, impact, selector, count]; trace → failing steps; census → counts + first divergence; PreToolUse filter-hook recipe documented here, never shipped as config); `--max-output` in all agent-browser examples; screenshots referenced by path, viewed only for visual-class adjudication; long-running commands write to file | general-purpose subagent drafts | sonnet | medium | M |
| 1.2 | CLAUDE.md "Working In This Repo" bullet: SKILL.md files >30KB navigated by Grep + section reads (`offset`/`limit`); whole-file Reads only for whole-file edits (F2) | main session | — | — | S |
| 1.3 | bug-reporting / acr-reporting: one line each forbidding wholesale evidence-corpus re-reads during serialization (both already cite `finding_id`s) | (bundled with 1.1) | sonnet | low | — |
| 1.4 | Mirror sync (`.agents/skills/`) — `scripts/check_mirrors.py` strict CI already enforces (drift tier: headings/URLs/reference bytes, not body prose) | (bundled with 1.1) | sonnet | low | — |

*Gate:* skill diffs reviewed by **proposal-critic** (def tier, effort high) — workflow change, not a11y design; net context budget of the diff itself is a review criterion (R4); mirror check green.

### Phase 2 — Evidence-reader delegation (agents)

| # | Task | Executor | Model | Effort | Size |
|---|---|---|---|---|---|
| 2.1 | `a11y-evidence-reader` agent def: input = artifact paths + question under adjudication; output = evidence-contract-shaped digest + **coverage note** (read / not read / ambiguous); ≤10-line excerpts tied to handles, nothing else. **Vision mode is part of this same def** (image inputs → verdict + crop refs + confidence — one contract family, not a second def). Runtime routing: haiku for pure extraction, sonnet when interpretation is needed; never opus — **DONE 2026-08-25: `f78af43`** | opus subagent designs + drafts | opus | high | M |
| 2.2 | Wiring: main session / a11y-workflow orchestrator spawns the reader when artifacts exceed the inject budget, passes digest + paths to critic/planner (depth-1 preserved — the orchestrator spawns, never the critic) — **DONE 2026-08-25: `b4ecb3d`** | general-purpose subagent | sonnet | medium | S |
| 2.3 | Worked-example receipt: reader digests a real artifact set → critic consumes digest + paths → finding cites digest handles; committed as the pattern receipt — **DONE 2026-08-25: `637daba`** | reader (haiku/sonnet) + a11y-critic (opus) | mixed | medium/high | S |
| 2.4 | Interactive sessions: route heavy reads through the installed `delegate`/`to-file` helpers (routed, never vendored) — **DONE 2026-08-25: `a398b14`** | main session (doc note) | — | — | S |

*Gate:* agent def reviewed by proposal-critic (def tier, high); worked-example receipt committed.

### Phase 3 — The evidence-volume lane (the accuracy measurement)

**Question:** does curated, contract-shaped evidence beat raw-dump evidence on finding accuracy — and is any local effect dilution (payload) or fit (num_ctx)?

**Scope:** critic suite only. Planner/evalreport fixtures are **out** (planner protocol ~20.5K leaves no meaningful local evidence budget; audit-chain fixtures grade evidence aggregation itself, so a curated digest leaks part of the graded task — C2). Perspective lane inherits conclusions directionally only (§8).

**Fixtures:** 6 critic-suite fixtures = 4 buggy + 2 CLEAN (`button-skip-link-clean` + one further CLEAN chosen at lane setup). Buggy fixtures chosen for evidence-class realism: at least 2 with axe-detectable classes, at least 2 with keyboard-trace classes. Named in the lane README at setup gate.

**Pack construction (C2 fixes — binding rules):**
- **Blind curation:** CURATED packs are generated by the Phase 2 `a11y-evidence-reader` running its normal protocol with **no access to fixture metadata/ground truth**. Phase 3 formally depends on Phase 2. This makes the lane measure the production pipeline, not an oracle.
- **Question provenance:** each pack records, per pack, the verbatim adjudication question and its author, attested as authored without ground-truth access.
- **Question template:** one adjudication question per fixture, authored from artifact filenames and tool types only, recorded verbatim.
- **Recorded, never regenerated:** pack completeness is audited against ground truth *before any model row* and the audit is committed. Packs are then frozen. Post-row misses are partitioned: **pack-omission** (the evidence never made it into CURATED — this *is* R1's number, the measured cost of blind curation) vs **model-miss** (evidence present, model missed it — the attention cost). Both reported per cell. No regeneration loop exists.
- **Raw sets and padding:** both conditions derive from the same raw artifact set per fixture. Raw sets come from real tool runs against rendered fixture HTML where feasible (axe via the baseline-url-scan script on a static server; keyboard traces via keyboard-a11y-tester where the fixture supports a journey), else adapted from committed real-run artifacts (2026-07-10 cross-validation runs, de-identified funnel artifacts). DUMP padding = **real, on-domain, fixture-irrelevant** tool output from other pages/components of the same runs — uniform rule; never synthetic noise.
- **CLEAN packs:** the blind reader digests genuinely clean artifacts; an honest "no violations surfaced; coverage: …" digest is the ecologically valid CURATED pack (it is what production curation produces on clean input). The DUMP arm carries the clean raw output + the same padding rule.
- **Haiku-default re-curation rule (Q2):** a haiku-built pack carrying `AMBIGUOUS` / `re-invoke at sonnet` rows is re-curated at sonnet before freezing. Not a regeneration loop — no ground truth is consulted; this resolves the reader's own self-declared ambiguity before any model row exists, which is a different operation from regenerating in response to a post-row miss (forbidden below).
- **Effort + kill-rule:** pack construction ≈ 1–2 focused sessions (fixture-builder, sonnet, medium). If packs are not built by the lane-setup gate date, **descope to a 2-fixture pilot (1 buggy + 1 CLEAN) and run it anyway** — the lane shrinks; it does not silently evaporate.

**Local design — 2×2 (payload × num_ctx), one num_ctx per cell applied identically to whatever runs in it** (kills the raise-one-arm-only confound):

> **2026-08-25:** lane standardized at num_ctx=40,960 per bench-reviewer gate ruling 7 + measured qwen3:32b clamp (see `docs/plans/2026-08-25-context-utilization-phase3-gate-review.md` and `evals/results/context-utilization-phase3/README.md` §4.1). The 49,152-cell table below is the plan's original design record, superseded by the lane's own current spec — not edited in place so the two documents' history stays legible; do not build packs against the 49,152 values below.

| Cell | num_ctx | Prompt composition (measured-token budget) | Prompt total | + reserve 8,192 | Fits? |
|---|---|---|---|---|---|
| CURATED@32K | 32,768 | 16.2K protocol + ~2K fixture + 2–4K digest | ~20–22K | ~28–30K | ✓ |
| CURATED@49K | 49,152 | same | ~20–22K | ~28–30K | ✓ |
| DUMP@49K | 49,152 | 16.2K protocol + ~2K fixture + **18–20K dump** | ~36–38K | ~44–46K | ✓ |
| OVERFLOW (receipt only) | 32,768 | same as DUMP@49K | ~36–38K | — | ✗ guard fires — 1 fixture × 1 draw per model, documents the failure mode, not scored |

Budgets above use the qwen3.6-class measured protocol size (16,157). **Per-model `num_predict=1` probes at lane setup** re-measure protocol + largest pack for each model's tokenizer (qwen3:32b's critic-prompt token count has never been measured — F7); budgets adjust from probes, never from chars/4 estimates. The 8,192 reserve is for thinking models; DUMP@49K retains ≥11K raw headroom before the reserve.

**Decomposition the 2×2 buys:** (CURATED@49K vs DUMP@49K) = payload effect at fixed fit — the dilution test. (CURATED@32K vs CURATED@49K) = num_ctx effect at fixed payload — the fit/quantized-long-context test, and the data R5 needs. OVERFLOW = the mechanism receipt.

**Models:** local — qwen3.6:35b + qwen3:32b (control). Hosted — opus + sonnet subagent rows; conditions CURATED vs DUMP only (no ctx dimension), **same frozen packs as the local lane**.

**Draws:** ≥2 per cell, content-adjudicated; single-draw deltas are variance (documented flip magnitude 2–3 items on byte-identical prompts). Run count: local 3 scored cells × 2 models × 6 fixtures × 2 draws = 72 + 2 OVERFLOW receipts; hosted 2 × 2 × 6 × 2 = 48.

**Scores:** must-find recall; FP findings on CLEAN; miss partition (pack-omission vs model-miss); `prompt_eval_count` + `done_reason` on every local row (Phase 0 guard active).

**Registered predictions + adjudication thresholds (2026-08-24, before any row):**
- **P1 (local, dilution):** recall(CURATED@49K) ≥ recall(DUMP@49K), by ≥2 net adjudicated must-find items across the grid to count as real (below that: variance, report as null).
- **P1b (local, fit):** recall(CURATED@32K) ≈ recall(CURATED@49K) (|net| ≤1 adjudicated item). A CURATED@32K deficit would mean num_ctx itself degrades quality on these quantized models — flag for BENCHMARK.md.
- **P2 (hosted, non-inferiority harm-check):** CURATED loses **≤1 net adjudicated must-find item** vs DUMP across all hosted cells. This is the safety question Phase 2's default-on delegation needs answered; it is powered as a harm-check, not a benefit estimate. Any null is scoped to pack-scale (~20K) in the results README — it does not license claims about session-scale (163–349-turn) payloads.
- **P3 (both):** FP findings on CLEAN under DUMP ≥ under CURATED. Least confident; directional only.

**Decision rules (pre-committed):**
- P1 real + P2 holds → curation earns an accuracy claim (magnitude = adjudicated items); Phases 1–2 discipline confirmed on both grounds.
- P1 null + P1b null + P2 holds → curation delivers no pack-scale accuracy gain; Phases 1–2 stand on cost/latency/longevity grounds — the results README says so in those words; R5 resolves to map hygiene (correct num_ctx entries), no further curation lanes.
- P2 fails (CURATED loses >1 net item) → Phase 2's reader does NOT become a default path; it stays an opt-in cost tool pending pack-omission analysis (the partition says whether curation or the model lost the item).

*Gates:* lane design + scorer reviewed by **bench-reviewer** (opus, high) before packs; packs + completeness audit committed before rows; results README before any routing-guidance change. Executors: packs = fixture-builder (sonnet, medium); local batches = bench-runner (sonnet, low — mechanical monitoring); hosted rows = **main session spawns** the opus (effort high) / sonnet (effort medium) judgment subagents directly (depth-1); adjudication = opus (high); README = bench-reporter (sonnet, medium).

### Phase 4 — Real-session validation + docs

| # | Task | Executor | Model | Effort | Size |
|---|---|---|---|---|---|
| 4.1 | Re-run one comparable interactive engagement (EPA-style retest) under Phase 1–2 discipline; compare its session ledger to the 2026-08 baselines. **Single case, directional only** — validates adoption friction, not the accuracy hypothesis | main session (interactive by nature) + Phase 2 delegation | main + haiku/sonnet (delegated reads/tests) | low/medium (delegated steps) | M |
| 4.2 | Fold results into `ollama/BENCHMARK.md` (context-pressure section + any Phase 3-earned routing wording + any Phase 0.4 annotations), `CLAUDE.md` pointer, this plan's receipts appendix | bench-reporter | sonnet | medium | S |
| 4.3 | R5 decision memo consuming the P1b cells: curation vs raise-num_ctx, with the measured answer; gated by proposal-critic only if routing text changes | opus subagent | opus | high | S |

## 7. Adopted mechanisms & adoption boundaries (research outcomes)

| Mechanism | Adoption | Boundary |
|---|---|---|
| Harness output persistence (`BASH_MAX_OUTPUT_LENGTH` ~30K chars default; tool-agnostic wrapper) | Rely on it; never cat artifacts around it | No config shipped; harness behavior; figures pinned at Phase 0 |
| `MAX_MCP_OUTPUT_TOKENS` (25K default) | Rely on default | Raise only per-machine if a real need appears |
| Subagent isolation + costs.md delegation guidance | Core of Phase 2 and §2 | Depth-1 repo rule stays (harness allows 3) |
| PreToolUse filter-hook pattern (grep-before-the-model-sees-it) | **Documented recipe only** in `references/evidence-extraction.md` | Never shipped as repo config — hooks are user-level; this bundle stays prompt-only |
| `claude-cost-helpers` (`delegate`, `to-file`, `delegation-report`) | Routed use in interactive sessions | Never vendored; same rule as keyboard-a11y-tester |
| `/context`, `/usage` per-skill attribution, OTEL `tool_result` events | Session-level measurement complement | **Honest split:** the Phase 0 script = *retroactive* analysis of existing stores in a private, versionless JSONL format — a format break on any harness release is *expected*, not exceptional; OTEL/`/usage` = the supported forward surface. Nothing is built on the script beyond analysis. |
| Image handling (auto-downscale; inline MCP screenshot returns not path-referenceable; file-based screenshots are) | Constraint accepted → principle 3 + F3's tool-specific lever | No attempt to build image persistence |
| **Watch rule:** harness-native summarization / context-editing / artifact-digest features | None shipped as of the 2026-08 docs sweep | Re-check on harness release notes; a native mechanism would obsolete parts of Phases 1–2 — adopt and descope rather than compete |

## 8. Negative space — what this plan does NOT claim or do

- **Not claiming screenshots are a token crisis.** Measured ≈1.1–1.6K tokens each (F3). The image policy targets carrying cost, compaction loss, and relevance — not byte panic.
- **Not reducing evidence collection.** Artifacts on disk stay full-fidelity; only what *transits the window* changes. Evidence-class admissibility rules are untouched.
- **Not making local models verdict authorities.** Detector-not-verdict routing stands regardless of Phase 3 outcomes. A local model that fits its context is still a detector.
- **Not measuring the planner/evalreport/perspective suites in Phase 3.** The lane is critic-suite only; other suites inherit directionally and are named as untested if cited.
- **Not covering** Codex CLI lanes (separate harness; parity stays open on issue #17-adjacent work), a11y-test's browser-side runtime cost, hosted funnel receipt conventions, or compaction tuning (the stance is to *need* compaction less, not tune it).
- **Not a general cost program.** Scope is the a11y workflow surfaces named in §6 (plus the Phase 0.4 historical-row remit). The deck-iteration Read pattern (F2's worst row) evidences the *class*; deck workflows are out of scope.

## 9. Pre-mortem

- **R1 Over-curation drops the load-bearing detail.** Now *measured*, not just mitigated: the pack-omission partition (Phase 3) is the standing estimate of blind curation's miss cost; handles-not-prose returns (principle 2) plus the critic's ability to re-fetch raw slices by handle bound the production impact.
- **R2 Rank erosion via summarizer chains.** One hop max; digests are field-structured claims with handles; coverage notes make omissions visible instead of silent.
- **R3 Variance swamps the effect.** Registered thresholds are stated in adjudicated *items* against the documented 2–3-item flip magnitude; effects must replicate across draws; per-item flip reporting as in every funnel.
- **R4 Skill bloat irony.** Phase 1 adds ≤1.5KB to the skill body; recipes live in `references/` (progressive disclosure); net context budget of the diff is a named review criterion at the Phase 1 gate.
- **R5 Cheaper alternative for local (raise num_ctx).** Now answered by data: the P1b cells measure exactly this; Phase 4.3 writes the decision from those cells. If fit-is-everything, the memo says so and the fix is map hygiene.
- **R6 Discipline decays in interactive sessions.** Rules in SKILL.md don't bind a human-driven conversation. The session ledger (Phase 0.5) makes drift visible per-engagement; nothing stronger is proposed — enforcement hooks stay out per §7.
- **R7 Phase 3 stall (the skeptic scenario: Phases 0–2 ship, the lane quietly never runs).** Named kill-rule: descope to the 2-fixture pilot rather than not running; the lane-setup gate date is **2026-09-01** (Phase 2 completed 2026-08-25).

## 10. Receipts

- Baseline numbers: §3 (2026-08-24 run; Phase 0 scripts reproduce it; analyzer self-check vs `/usage` bounds the estimates).
- Verified map facts: run_benchmark.py:340–360 (`CRITIC_CTX`, qwen3:32b absent, default 16,384), :661–671 (`PERSPECTIVE_CTX`, qwen3:32b = 32,768), :613–616 (ACR 40,960 precedent), ollama_a11y.py:112 (wrapper default 32,768).
- Phase artifacts: `evals/results/context-utilization/` (Phase 3 lane README, frozen packs + completeness audits, raw responses, adjudication notes); Phase 0.4 retro-probe receipts beside the affected BENCHMARK.md sections; engagement ledgers beside engagement receipts.
- Plan review: `docs/plans/2026-08-24-context-utilization-plan-critic-review.md` (proposal-critic REVISE + same-day disposition table).
