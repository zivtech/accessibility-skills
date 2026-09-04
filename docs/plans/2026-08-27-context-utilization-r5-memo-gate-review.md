# R5 Decision Memo Gate Review — proposal-critic disposition record

**Date:** 2026-08-27 · **Reviewer:** proposal-critic subagent (opus, adversarial mode) · **Scope:**
`docs/plans/2026-08-27-context-utilization-r5-decision-memo.md` (plan §6 Phase 4 row 4.3), reviewed
as a routing-text change. **Verdict: REVISE** (1 critical, 5 major, 3 medium, 3 minor, 4 missing
items, 2 ambiguities) **→ all findings applied same session.**

The gate explicitly endorsed the memo's decision, its §1 three-leg argument, and its §7
negative-space discipline. Everything below is correction of evidence and completeness, not of the
conclusion — no finding challenged "raise `num_ctx`, not curation."

## Findings and dispositions

| # | Sev | Finding (with evidence) | Action taken | Verify at |
|---|---|---|---|---|
| C1 | **Critical** | §3 "Correcting the recorded call" was **factually inverted**. The 5,596 perspective estimate omitted `PERSPECTIVE_REFS`: the production path (`run_benchmark.py:1102,1107,1128` → `load_perspective_system_prompt`, `:458–465`) concatenates SKILL.md **plus both refs files** = 23,529 chars ≈ 6,723 est. tokens system-prompt-alone. All 25 fixtures est. 7,645–10,106 → **21/25 refuse** at the 16,384 default (pilot 7/7). The Phase 0 razor-thin call (`phase1-handoff.md:39`) was correct and understated. | Paragraph deleted. Replaced with **"The Phase 0 razor-thin call was correct — and understated"**: planner 19/28 refuse, bug-report 7/7 refuse, perspective 21/25 refuse at the default, unaffected in practice only because `PERSPECTIVE_CTX` maps every current model to 32,768. "not because current fixtures are near the line" dropped from the table row. | Memo §3, para after the table; `PERSPECTIVE_CTX_DEFAULT` row |
| M1 | Major | §3 planner row "only the smallest of 28 clears" is false — **9 of 28 clear** at the 32,768 default. | Row now reads "**19 of 28 already refuse** at the 32,768 default (budget 24,576); the 9 that clear do so by **≤603 tokens**." Margins independently recomputed: 603, 552, 492, 390, 264, 228, 127, 103, 55. | Memo §3, `PLANNER_CTX` row |
| M2 | Major | Proposed BENCHMARK.md text called net +4 "within the documented 2–3-item draw-flip magnitude" (4 ∉ 2–3) and dropped that P1b's registered \|net\| ≤ 1 threshold was **VIOLATED** (RESULTS:82, plan:145 — the registered rule was to *flag* it for BENCHMARK.md). | Clause replaced with the gate's wording verbatim: breaches the registered \|net\| ≤ 1 threshold in the *unfeared* direction; decomposition given; read as absence of a deficit, never as an advantage. Same correction propagated to memo §1 leg 2 and §7. | Memo §6 fenced block, ¶3; §1 leg 2; §7 bullet 3 |
| M3 | Major | §2 said the P3 reversal "stays out of routing text" while §5's block included it — self-contradiction. | Per lead's disposition: reversal **kept** in the BENCHMARK.md block; §2 rewritten to own the call — RESULTS §5 routed the disposition here, and this memo licenses it **only** as an explicitly exploratory, mechanism-free observation reinforcing detector-not-verdict, never as a routing rule. Block wording gained "with no established mechanism". | Memo §2, final bullet ("**Disposition:**"); §6 block ¶3 |
| M4 | Major | Every §3 estimate was computed on **un-stripped** SKILL.md; production applies `strip_frontmatter` (`run_benchmark.py:446–456, 632–635`). Gate's corrected figures: bugreport sys-alone 8,518; ACR largest 9,740; planner median/largest 24,899/25,709; critic max 19,906. Memo's critic min 18,148 matched neither variant. | **Whole §3 table recomputed** on the production composition over every canonical fixture (see "Recomputation" below). Recipe line added verbatim to §3. All operational verdicts survived. | Memo §3, "How the table below was computed" + table |
| M5 | Major | The memo raised `PLANNER_CTX_DEFAULT` without surfacing that **every committed planner row** ran at 32,768 pre-guard (`run_benchmark.py:658` comment) with prompts est. 23,973–25,709 — ~7–8K left for thinking + output — and Phase 0.4's retro-probe was **critic-suite only**. | §8 bullet added naming the unmeasured planner output-side exposure and routing a Phase 0.4-style `eval_count` analysis; registered as task **R5.3** in the new §4 table, gated to land before or alongside the raise. | Memo §8 bullet 1; §4 row R5.3 |
| D1 | Medium | §1 presented the decision branch as cleanly fired; RESULTS:105–106 says **"Nearest registered branch"** with the caveat "(P1 here is worse than null for the prediction; P1b violated in the unfeared direction)". | "Nearest registered branch" and the parenthetical caveat carried **verbatim** into §1. | Memo §1, ¶2 |
| D2 | Medium | §5 said "Phase 4.2 folds it" without noting routing-text changes are gated on Phase 4.1 too (RESULTS:157–158, "after those gates", plural). | Per lead's disposition: §6 now states the section is proposed and gate-approved wording, **folded by Phase 4.2 only after Phase 4.1 completes**, citing RESULTS:157–158. | Memo §6, ¶1 |
| D3 | Medium | §3/§4 proposed seven code/config changes with no executor, sequence, or gate. | New **§4 task table** in the plan's §6 convention, 5 rows with executor/model/effort/size: R5.1 record `num_ctx` (prerequisite), R5.2 probe receipts, R5.3 planner-exposure analysis, R5.4 apply raises, R5.5 dated annotation. | Memo §4 |
| N1 | Minor | §5's "refuse as INVALID" is true for `run_benchmark.py` but not `ollama_a11y.py`, whose guard **warns and still runs** (`ollama_a11y.py:230`, "generation still runs (best effort)"). | Distinguishing clause added to the BENCHMARK.md block: runner refuses + writes INVALID; wrapper warns and generates, so a wrapper run needs its warning read. | Memo §6 block, ¶1 |
| N2 | Minor | "Fit is the lever; payload curation is not." was scoped to pack scale five sentences later. | Heading scoped at first mention: "**At pack scale (~20–32K prompts), fit is the lever and payload curation is not.**" | Memo §6 block, ¶3 first sentence |
| N3 | Minor | The new section will sit beside `ollama/BENCHMARK.md:38`'s superseded **16,157** protocol figure (marked replaced by 14,276 / 13,853 at `run_benchmark.py:518–520`). | "*Fold note for Phase 4.2*" added instructing the stale neighbor be corrected in the same edit. | Memo §6, ¶2 |
| MISS-a | Missing | The M4 recipe line. | Added verbatim, with the production-path file:line citations. | Memo §3, "How the table below was computed" |
| MISS-b | Missing | The M5 planner-exposure bullet. | Added (see M5). | Memo §8 bullet 1 |
| MISS-c | Missing | No "what this memo does NOT recommend changing" statement. | Added as the closing §7 bullet: `CRITIC_CTX`'s 10 mapped models, `PERSPECTIVE_CTX`'s 7, `EVALREPORT`/`ACR` defaults, the 8,192 reserve, the chars/3.5 estimator, issue #28's flag, and **every committed row**. | Memo §7, final bullet |
| MISS-d | Missing | "`_DEFAULT` raises are consequence-free (only unmapped/new models)" is false as history — `ollama/BENCHMARK.md:36` records qwen3:32b's entire 99-row critic history running at the 16,384 default before the 2026-08-24 map entry. | §5 closing paragraph: "**A `_DEFAULT` raise is not consequence-free**" — any model can sit on a default for a whole era, so the annotation rule applies to `_DEFAULT` raises too. | Memo §5, final ¶ |
| AMB-1 | Ambiguity | "read the per-suite map instead of carrying a second integer" named no mechanism. | Per lead: **hand-synced duplication (option B)** — a small per-command `num_ctx` dict inside `ollama_a11y.py` (`planner`=40,960, others 32,768), kept in sync by hand per `run_benchmark.py:33–34`'s standalone-scripts convention, with the drift risk named in-clause. | Memo §3, wrapper row |
| AMB-2 | Ambiguity | "each raised default needs its own probe receipt" — per (model × suite) or per suite? | Per lead: **per (model × suite)** for mapped entries; for `_DEFAULT`s, size from current models' probes with the densest measured tokenizer governing, and state plainly that the **client-side guard, not the default, is the real protection** for unknown models. | Memo §8 bullet 2; §4 row R5.2 |

## Recomputation (memo task 1) — my numbers vs. the gate's

Recomputed independently via `run_benchmark`'s own production loaders (`load_system_prompt`,
`load_perspective_system_prompt`, `load_planner_system_prompt`, `strip_frontmatter`,
`load_fixture`→`strip_answer_key`), `estimate_tokens` at chars/3.5, over each suite's canonical
fixture list. Budget = `num_ctx − RESPONSE_RESERVE(8,192)`.

| Suite | Sys chars | Sys alone | n | Est. range | Refuse @ current default |
|---|---|---|---|---|---|
| critic | 60,729 | 17,352 | 41 | 17,649–19,906 | 41/41 @16,384 · 0/41 @32,768 |
| planner | 82,291 | 23,512 | 28 | 23,973–25,709 | 19/28 @32,768 · 0/28 @40,960 |
| perspective (SKILL + 2 refs) | 23,529 | 6,723 | 25 | 7,645–10,106 | 21/25 @16,384 (pilot 7/7) · 0/25 @32,768 |
| bug-report | 29,810 | **8,518** | 7 | 8,703–9,414 | 7/7 @16,384 · 0/7 @32,768 |
| evaluation-report | 11,046 | 3,156 | 1 | 5,484 | 0/1 @32,768 |
| ACR | 18,444 | 5,270 | 4 | 8,170–9,740 | 0/4 @40,960 |

**Agreement with the gate:** exact on every figure it named — bugreport sys-alone 8,518, ACR largest
9,740, planner largest 25,709, critic max 19,906, perspective sys 23,529 / 6,723, planner 19/28,
perspective 21/25 and pilot 7/7.

**Two reconciliations, neither a disagreement:**

1. **Planner "median" 24,895 (mine) vs 24,899 (gate's).** Same data. n = 28 is even; the two middle
   values are **24,891 and 24,899**. The gate reported `median_high`, I computed the average. Not a
   discrepancy — a convention difference over an ambiguous statistic, so the memo now reports the
   **min–max range** instead of a median and the ambiguity disappears.
2. **Critic minimum: the gate was right, my original 18,148 was a selection error.** The gate
   suspected a fixture-set difference; it wasn't. On the production path the minimum is **17,649**
   (`toast-notification-no-role`) — matching the gate's stripped figure exactly. My 18,148 was
   `button-skip-link-clean` with **un-stripped** SKILL.md, and `button-skip-link-clean` is not the
   minimum prompt at all (it is 18,019 stripped): I had picked the smallest *file*, but
   `strip_answer_key` reorders the fixtures by prompt size. The gate's "17,777 raw" is the same
   `toast-notification-no-role` prompt against the un-stripped skill (17,649 + the 449 frontmatter
   chars ≈ 128 tokens). All three numbers now explained; **17,649 is correct**.

## Standing caveat on all §3 numbers

Every figure above is a **guard estimate** (chars/3.5), not a measured token count. `estimate_tokens`
runs 22–30% high on markdown, so the true prompts are smaller — but the guard acts on the estimate,
so the refusals are real and the operational verdicts hold. Actual sizing still requires the
`num_predict=1` probes registered as task R5.2. This caveat is stated in the memo at §3 and §7.
