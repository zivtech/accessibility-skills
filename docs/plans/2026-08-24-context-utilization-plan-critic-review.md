# Critic Review — Context-Window Utilization Plan

**Reviewed:** `docs/plans/2026-08-24-context-utilization-plan.md` (2026-08-24 draft)
**Reviewer:** proposal-critic (Fable tier), ADVERSARIAL mode (escalated on Critical 1)
**Verdict:** REVISE → findings dispositioned same day; revised plan supersedes the draft in place.

---

## Verdict summary (critic's words, condensed)

> This is an unusually live plan — measured baseline verified against the repo down to the byte counts, honest negative space, registered predictions, doctrine-consistent boundaries. But its centerpiece, the Phase 3 A/B lane, is arithmetically unexecutable as written (DUMP-FIT sizing contradicts the plan's own F6 measurements and its own Phase 0 truncation guard) and methodologically biased as written (unspecified curator + a ground-truth-informed pack-regeneration loop that measures oracle-repaired curation, not the blind curation Phase 2 ships). Phases 0–2 and 4 are sound with fixes at MAJOR level.

Pre-commitment predictions: curation/hint-hygiene confound CONFIRMED; 2-draw underpower CONFIRMED for P2 only; depth-1 collision REFUTED; num_ctx interaction CONFIRMED (stronger than predicted — hard arithmetic contradiction); over-reliance on §2 precision MOSTLY REFUTED.

## Critical findings

**C1 — DUMP-FIT cannot exist at the stated sizes.** Critic protocol is 16,157 *measured* tokens (run_benchmark.py:341–342); 16.2K + 20–24K evidence > 32,768 before generation. Under the plan's own Phase 0 guard (reserve 8,192), max evidence ≈ 8.4K for critic at 32K — below the stated band. Planner protocol (~20.5K) leaves ~2.5K — smaller than the CURATED band — yet a planner fixture was named with no statement of how it runs locally. **qwen3:32b — the named control — is absent from CRITIC_CTX and falls to the 16,384 default.** The harness's own precedent (ACR lane needed 40,960 for a ~10K bundle, run_benchmark.py:613–616) agrees. Natural workaround (raise num_ctx on one arm only) is a silent confound.

**C2 — No blindness rule for pack construction; the curation-fidelity check is an oracle-repair ratchet.** "Regenerate pack, re-run" is ground-truth-informed repair with no defined loop exit; production curation (Phase 2 reader) has no oracle, so reported CURATED accuracy would describe a pipeline that doesn't exist — the repo's de-hinting lesson at condition level. Per-fixture asymmetry: critic fixtures are a clean noise-dose manipulation (valid); audit-chain fixtures (`transit-portal-q3` grades aggregation of the evidence itself) leak — CURATED partially contains the answer. Internal contradiction: the regenerate loop erases exactly the quantity R1 says must be measured.

## Major findings

**M1 — Phase 0.2 guard has a plausible false-pass:** `prompt_eval_count` deflates under Ollama's warm KV-prefix cache; the failing-direction verification as written passes cache-cold and ships the false-pass. Fix: client-side estimate as primary gate, prompt_eval_count as corroboration; verify failing direction cache-warm (twice; both draws must flag).

**M2 — R5 (curation vs raise-num_ctx) promised a comparison arm that never runs.** Phase 4.3 is a discussion step, not a measurement. Fix: add a raised-ctx arm so R5 is answered by data; raised-ctx accuracy on quantized local models is itself open and gets measured for free.

**M3 — F7 indicts historical baseline rows; the plan builds the instrument without pointing it backward.** qwen3:32b critic rows ran at the 16,384 default; `done_reason` recording only exists since 2026-08-23 — historical rows blind on both sides. Fix: retro-probe; clear or annotate the published rows.

**M4 — P2 registered but not adjudicable.** No magnitude threshold; at documented variance (2–3 item flips) with 2 draws, "small/zero/noise" are indistinguishable. Fix: register a threshold; reframe hosted arm as a non-inferiority harm-check ("CURATED loses ≤N net adjudicated must-find items"), which is the question Phase 2's default-on delegation actually needs. Scope any hosted null to pack-scale.

## Minor findings

1. "No path-reference mechanism exists for images" is overbroad — true only for inline browser-MCP screenshot returns; file-based screenshots are re-readable. Reword tool-specifically.
2. Vision subagent is a second, undefined contract — say whether it's the reader def with an image mode or a second def.
3. §6 portability inverted: session-store JSONL is private/versionless (the unresolved compaction-marker note demonstrates it); OTEL is the supported forward surface. Script's real advantage is retroactivity.
4. INVALID semantics unstated for the interactive wrapper.
5. CLEAN control unnamed; CLEAN-pack semantics unstated (honest "artifacts clean" digest is ecologically valid — say so).
6. Load-bearing sizes in parentheticals is how C1 slipped in — put budgets in a table.

## Missing

- Per-model × suite × condition num_ctx table.
- DUMP padding provenance (real vs synthetic changes what "irrelevant payload" means).
- Effort sizing for pack construction — largest unbudgeted item; skeptic scenario: Phases 0–2 ship, Phase 3 quietly never runs.
- Self-validation of the §2 analyzer (one cross-check vs `/usage` or API counts).
- Watch trigger on harness-native summarization/context-editing features (live-skew class).

## Ambiguity risks

- "padded to ~20–24K … fits within 32K with the protocol" — two readings, one overflows, one measures nothing.
- "only if irreducible does it count" — one attempt vs regenerate-until-wins (a ratchet guaranteeing P1).
- planner/evalreport fixtures locally: dropped, hosted-only, or shrunken band — each yields a different lane.

## Open questions (unscored)

- Do resumed sessions re-serialize prior turns (F2's literal counts may double-count; ranking survives)?
- Were historical qwen3:32b critic rows in fact truncated/clipped? (Retro-probe answers; may require annotating BENCHMARK.md — beyond the draft's scope statement.)
- Are the BASH/MCP output-cap figures accurate for the harness versions in use? (Pin with a one-line receipt at Phase 0.)

## What changes the verdict to ACCEPT (critic's list)

Rewrite Phase 3 with a num_ctx/budget table from measured tokens; blind reader-agent pack generation with recorded (not regenerated) completeness audits; the raised-ctx DUMP arm; a registered P2 threshold; harden the Phase 0.2 gate to cache-warm; add the historical retro-probe.

---

## Disposition (2026-08-24, same-day revision)

| Finding | Disposition |
|---|---|
| C1 | **Fixed.** Phase 3 rebuilt around a measured-token budget table; local lane runs a 2×2 design (payload × num_ctx) with one num_ctx per cell applied identically to both payload arms — the raise-one-arm-only confound is designed out, and the decomposition (payload effect at fixed ctx; ctx effect at fixed payload) is exactly what R5 needs. qwen3:32b's missing CRITIC_CTX entry verified in-repo and folded into Phase 0 (map entry + probe). Planner/evalreport fixtures removed from Phase 3 scope. |
| C2 | **Fixed.** CURATED packs are generated blind by the Phase 2 evidence-reader running its normal protocol (Phase 3 now formally depends on Phase 2 — order unchanged). Completeness audited against ground truth pre-rows, **recorded, never regenerated**; misses partitioned pack-omission vs model-miss and both reported (pack-omission *is* R1's number). Audit-chain fixtures dropped from Phase 3. |
| M1 | **Fixed.** Client-side token estimate is the primary gate; `prompt_eval_count` corroborates; gate verified failing-direction cache-warm (two consecutive draws must both flag INVALID). |
| M2 | **Fixed** via the C1 redesign (CURATED@49K arm decomposes fit vs dilution); Phase 4.3 rewritten as a decision memo consuming those cells. |
| M3 | **Fixed.** Phase 0 gains the retro-probe (archived-artifact mining first — committed response JSONs may already carry `prompt_eval_count` — then live `num_predict=1` probes); deliverable is "clear or annotate BENCHMARK.md rows"; scope statement extended accordingly. |
| M4 | **Fixed.** Hosted arm re-registered as non-inferiority: CURATED loses ≤1 net adjudicated must-find item across all hosted cells; any null scoped to pack-scale in the results README. |
| Minor 1–6 | **All fixed** (tool-specific image wording; vision = reader-def mode; §6 retroactivity/OTEL split stated honestly; INVALID semantics split benchmark-vs-interactive; CLEAN fixture named + honest-clean-digest semantics stated; all budgets in tables). |
| Missing ×5 | **All added** (num_ctx table; padding = real on-domain artifacts from the same runs, uniform rule; pack-construction effort sized with a descope kill-rule; analyzer self-check vs `/usage` in Phase 0.1; watch rule on harness-native context features in §6). |
| Ambiguities ×3 | **Resolved** (budget table; packs never regenerated post-audit; planner/evalreport out of Phase 3). |
| Open questions | Resumed-session caveat added to F2; cap-figure pinning added to Phase 0 gate; qwen3:32b history handled by M3 retro-probe. |

Additional revision (user directive, 2026-08-24): every task now carries an executor / model-tier / reasoning-effort / size row; subagent-first execution model stated explicitly.

**Post-revision verification pass** (independent subagent, sonnet, 2026-08-24): disposition fidelity **CLEAN** — every table row above verified present in the revised plan (one noted nuance: the "num_ctx table" Missing-item is resolved by design change — critic-suite-only scope + uniform ctx-per-cell + per-model probes at lane setup — rather than a literal 3-axis table). Found and fixed same day: two low-end arithmetic understatements in the Phase 3 budget table (no Fits? verdict affected), four stale §-references from the §2 insertion, two missing effort levels (Phase 4.1 delegated steps, Phase 3 hosted-row spawns). All repo-side figures (CRITIC_CTX/PERSPECTIVE_CTX/defaults/ACR precedent/16,157 measurement) re-verified exact against source lines.

**Phase 0.4a executed early** (Explore subagent, haiku, 2026-08-24): committed artifacts cannot settle the qwen3:32b historical-truncation question — the three critic-suite eras (174 response files) lack `prompt_eval_count` entirely; the field appears only from the July–August 2026 lanes. Live `num_predict=1` probes (Phase 0.4b) are the required path. Receipt folded into plan F7.
