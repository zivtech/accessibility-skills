# R5 Decision Memo — Curation vs. Raise-`num_ctx` for Local Models (2026-08-27)

**Plan:** `docs/plans/2026-08-24-context-utilization-plan.md` — §9 pre-mortem **R5**, executed as the
§6 Phase 4 row **4.3**. **Inputs:** the P1b cells
(`evals/results/context-utilization-phase3/scores/adjudicated-predictions.json`) and
`evals/results/context-utilization-phase3/RESULTS-2026-08-26.md` (whole).
**Executor:** opus subagent, effort high, per plan §6 executor table.
**Gate:** proposal-critic REVISE, 2026-08-27 — all findings applied; disposition record at
`docs/plans/2026-08-27-context-utilization-r5-memo-gate-review.md`.

## 1. The question, and the measured answer

R5 asked whether the cheap alternative to Phases 1–2 curation, for local models, is simply raising
`num_ctx`. **It is.** For local models at pack scale, **fit is everything and curation buys no
accuracy.**

The RESULTS doc records this as the **nearest registered branch**, not an exact match —
**"P1 null + P1b null + P2 holds"**, with its stated caveat carried verbatim: *"(P1 here is worse
than null for the prediction; P1b violated in the unfeared direction)"* (RESULTS:105–106). The
branch's consequence, in the plan's own pre-committed words: **"curation delivers no pack-scale
accuracy gain; Phases 1–2 stand on cost/latency/longevity grounds; R5 resolves to map hygiene
(correct `num_ctx` entries), no further curation lanes."**

| model | CURATED@32K | CURATED@40K | DUMP@40K | REAL-FP 32K / 40K / DUMP |
|---|---|---|---|---|
| qwen3.6:35b | 17/18 | 14/18 | 17/18 | 12 / 10 / 3 |
| qwen3:32b | 17/18 | 16/18 | 17/18 | 10 / 9 / 7 |

Three legs, all adjudicated (RESULTS §3–§5):

1. **Curation earned no accuracy claim locally.** P1 net(CURATED@40K − DUMP@40K) = **−4**. The
   predicted CURATED advantage did not appear.
2. **The smaller window carried no penalty.** P1b net(CURATED@32K − CURATED@40K) = **+4** — a
   **violation** of the registered |net| ≤ 1 threshold (plan:145, RESULTS:82), in the *unfeared*
   direction. The registered rule for a violation was to flag it for BENCHMARK.md; §6 does that.
3. **The entire local spread is two items.** `heading-hierarchy-skipped#item1` flips in both
   directions across draws and cells; `file-input-no-labels#item3` (`not-tool-observable`) is a
   single-model, single-cell stable miss.

Leg 3 is why the decision reads "curation buys nothing," not "the dump wins" and not "32K beats
40K." **The decision does not depend on reading P1b's +4 as a real 32K advantage** — it depends on
the absence of a deficit, which the cells show either way. Zero pack-omission misses anywhere:
R1's measured cost of blind curation is **0**. The packs were fine; the gain simply wasn't there.

## 2. Why not curation-for-fit, locally

- **Cost asymmetry.** Buying fit with curation costs an `a11y-evidence-reader` spawn, a digest,
  freeze and provenance discipline, and one hop of rank erosion per run. Buying fit with `num_ctx`
  costs editing one integer in a dict. With a null accuracy delta, the cheaper instrument wins.
- **The measurement.** P1 = −4. There is no local accuracy result to trade the complexity for.
- **Exploratory caution, labeled.** P3 reversed locally on **both** models: CLEAN rows drew 19–22
  adjudicated fabricated violations under CURATED vs 10 under DUMP (RESULTS §4). Untested
  hypothesis: a compact digest hands the model few high-salience rows it over-interprets, where the
  dump's bulk dilutes fabrication pressure. Directional-only, least-confident — a reason not to
  reach for local curation as a fit fix, **not** a finding that curation causes fabrication.
  **Disposition:** RESULTS §5 routed this reversal to this memo. This memo licenses it into
  BENCHMARK.md **only** as an explicitly exploratory, mechanism-free observation that reinforces
  detector-not-verdict-authority — never as a routing rule, and never as a reason to prefer one
  payload shape over another.

Nothing here touches hosted or session routing. P2 held exactly (net 0; opus and sonnet 18/18 in
all four cells), so Phase 2 reader delegation is safe at pack scale on the harm-check it was
powered for, and Phases 1–2 stand for the hosted/session surfaces on cost, latency, and longevity.

## 3. What "map hygiene" concretely means

The sizing instrument is the **`num_predict=1` probe** (recipe:
`evals/results/context-utilization-phase0/README.md:35` — `POST /api/generate` with
`{"options": {"num_ctx": <generous N>, "num_predict": 1, "temperature": 0}}` on the *assembled
production prompt*, then read `prompt_eval_count`). Never chars/3.5: `estimate_tokens` runs 22–30%
high on markdown. Reserve stays **8,192** above the measured figure (`run_benchmark.py:44`,
`ollama_a11y.py:46`) because thinking tokens share the window. Any `qwen3:32b` entry above
**40,960** is fiction — the server clamps silently to its declared ceiling.

**How the table below was computed.** Estimates =
`estimate_tokens(strip_frontmatter(SKILL.md) + PROMPT_PREFIX + strip_answer_key(fixture))`,
chars/3.5, over every fixture in the suite's canonical list — i.e. the exact production
composition (`run_benchmark.py:446` `strip_frontmatter`, `:453` critic, `:458` perspective —
which appends **both `PERSPECTIVE_REFS`** files, `:136–139` — `:632` planner; `:481` `load_fixture`
applies `strip_answer_key`). Budget = `num_ctx − 8,192`. These are **guard estimates, not measured
tokens**: they establish what the guard does, which is the operational fact.

| Entry | file:line | Current | System prompt (est.) | Prompt est. range (n) | Verdict |
|---|---|---|---|---|---|
| `CRITIC_CTX` (10 models) | `run_benchmark.py:517–544` | 32,768 | 17,352 | 17,649–19,906 (41) | **Stands.** 0/41 refuse; measured protocol 13,853 (32b) / 14,276 (35b) leaves real headroom. |
| `CRITIC_CTX_DEFAULT` | `run_benchmark.py:545` | 16,384 | — | same | **→ 32,768.** **41/41 refuse** at 16,384 (budget 8,192). Only unmapped/new models hit it — they get a hard stop, not a run. |
| `PLANNER_CTX` / `_DEFAULT` | `run_benchmark.py:658–659` | `{}` / 32,768 | 23,512 | 23,973–25,709 (28) | **→ 40,960.** **19 of 28 already refuse** at the 32,768 default (budget 24,576); the 9 that clear do so by **≤603 tokens**. 0/28 refuse at 40,960. |
| `BUGREPORT_CTX` / `_DEFAULT` | `run_benchmark.py:728–729` | `{}` / 16,384 | **8,518** | 8,703–9,414 (7) | **→ 32,768.** **7/7 refuse**; the system prompt alone (8,518) already exceeds the 8,192 budget. No bug-report row can run today. |
| `EVALREPORT_CTX` / `_DEFAULT` | `run_benchmark.py:794–795` | `{}` / 32,768 | 3,156 | 5,484 (1) | **Stands.** |
| `ACR_CTX` / `_DEFAULT` | `run_benchmark.py:876–877` | `{}` / 40,960 | 5,270 | 8,170–9,740 (4) | **Stands.** |
| `PERSPECTIVE_CTX` (7 models) | `run_benchmark.py:953–962` | 32,768 | 6,723 | 7,645–10,106 (25) | **Stands.** 0/25 refuse. |
| `PERSPECTIVE_CTX_DEFAULT` | `run_benchmark.py:963` | 16,384 | 6,723 | same | **→ 32,768.** **21/25 refuse** at 16,384 (pilot set 7/7). Unmapped models only — every current model is mapped to 32,768. |
| Wrapper default | `ollama_a11y.py:227` (CLI `--ctx`, `:309`) | 32,768 | — | — | **→ per-command dict.** Flat 32,768 is correct for critic/perspective/bugreport/evalreport and wrong for `planner`. Fix: a small per-command `num_ctx` dict inside `ollama_a11y.py` (`planner`=40,960, others 32,768), **hand-synced** with `run_benchmark.py` per that file's own standalone-scripts convention (`run_benchmark.py:33–34`) — accepting the drift risk that convention already carries for the twin guard code. |

**The Phase 0 razor-thin call was correct — and understated.** The recorded fast-follow
(`docs/plans/2026-08-24-context-utilization-phase1-handoff.md:39`) named planner, bug-report, and
perspective. All three are worse than razor-thin against today's fixtures: planner **19/28 refuse**,
bug-report **7/7 refuse** (system prompt alone over budget), perspective **21/25 refuse at the
default**. Perspective is unaffected in practice only because `PERSPECTIVE_CTX` maps every current
model to 32,768 — the exposure is real for any unmapped model.

**Stale receipt:** plan §10 cites `run_benchmark.py:340–360`, `:661–671`, `:613–616`, and
`ollama_a11y.py:112` for these maps. All four ranges have moved; the table above is current.

## 4. Task sequence (plan §6 convention)

| # | Task | Executor | Model | Effort | Size |
|---|---|---|---|---|---|
| R5.1 | **Prerequisite.** Record `num_ctx` in all six scored `_benchmark` dicts (`run_benchmark.py:621, 714, 780, 857, 938, 1031` — each already carries `declared_context_length`; the field sits beside it). Without it, no future row can be attributed to a window. | bench-runner | sonnet | low | S |
| R5.2 | `num_predict=1` probe receipts for every entry raised in §3, per **(model × suite)** for mapped entries; committed beside the raise. Also covers M5's planner-exposure question below. | bench-runner | sonnet | medium | S |
| R5.3 | **Planner-suite historical exposure analysis** (Phase 0.4-style `eval_count` review of committed planner rows) — see §8. Must land before or alongside R5.4's planner raise. | general-purpose subagent | sonnet | medium | S |
| R5.4 | Apply the raises (4 `_DEFAULT`s + the `ollama_a11y.py` per-command dict), each with its probe receipt. | bench-runner | sonnet | low | S |
| R5.5 | Dated `ollama/BENCHMARK.md` annotation per raised default (§5), folded with the §6 routing section at Phase 4.2. | bench-reporter | sonnet | medium | S |

## 5. Comparability

Raising a default changes what future rows mean. Handle it two ways, never by touching historical rows:

1. **Record `num_ctx` per row** (task R5.1). The evidence lane already does
   (`run_evidence_lane.py:360`, beside `declared_context_length`, `done_reason`, `output_clipped`,
   `prompt_eval_count`). `run_benchmark.py` **does not** at any of its six scored lanes — only the
   overflow row records it (`:387`).
2. **Annotate, don't rewrite.** A dated note per raised default, shaped like the existing
   2026-08-24 retro-probe section (`ollama/BENCHMARK.md:34`): old value, new value, probe receipt,
   which committed rows predate the change. No silent retro-change of historical rows — ever.

**A `_DEFAULT` raise is not consequence-free.** The convenient framing — "defaults only affect
unmapped/new models" — is false as history. `ollama/BENCHMARK.md:36` records that `qwen3:32b`'s
**entire 99-row critic history** ran at the 16,384 `CRITIC_CTX_DEFAULT`, because it had no map entry
until 2026-08-24. Any model can sit on a default for a whole era. The §5.2 annotation therefore
applies to `_DEFAULT` raises exactly as it does to mapped-entry changes.

## 6. Routing-text disposition

**`ollama/BENCHMARK.md`: YES** — one dated section, proposed verbatim below for the gate. It is
proposed-and-gate-approved wording, **folded by Phase 4.2 only after Phase 4.1 completes**, per the
RESULTS doc's "routing-text changes only after those gates" (RESULTS:157–158, plural).
**`CLAUDE.md`: NO** — detector-not-verdict-authority stands unchanged and is if anything reinforced
(§7); the local-model recommendation, funnel history, and routing table are untouched.

*Fold note for Phase 4.2:* the new section will sit beside `ollama/BENCHMARK.md:38`, which still
cites **16,157** as the qwen3.6 protocol figure — superseded by the 14,276 / 13,853 `num_predict=1`
measurements (`run_benchmark.py:518–520`). Correct the neighbor in the same edit.

```markdown
## Context Pressure and `num_ctx` (2026-08-27, from the Phase 3 evidence-volume lane)

Local rows are only comparable when the prompt actually fit. Two failure modes are on record, both
from the same ~30.5K-token prompt sent at `num_ctx=32,768`
(`evals/results/context-utilization-phase3/RESULTS-2026-08-26.md` §2): `qwen3.6:35b` returned
`done_reason=length` (output clipped — visible), while `qwen3:32b` returned `done_reason=stop` after
**silent server-side prompt truncation** (`prompt_eval_count` 28,445 < 30,490 sent) — a row that
looks clean and is not. The client-side guard exists for the second mode: in `run_benchmark.py` and
`run_evidence_lane.py` it **refuses** the run and writes an INVALID row, while the `ollama_a11y.py`
wrapper **warns and still generates** (best-effort, `ollama_a11y.py:230`) — so a wrapper run needs
its warning read, not assumed absent. `declared_context_length` is recorded on every row because
`qwen3:32b` silently clamps any requested `num_ctx` above **40,960** down to 40,960.

**Sizing rule:** size `num_ctx` per suite from real `num_predict=1` probes against the assembled
prompt (protocol + largest fixture or pack) for each model's tokenizer — never from chars/4 or
chars/3.5 estimates, which run 22–30% high on markdown. Keep the 8,192 reserve above the measured
figure for thinking-by-default models. Cap `qwen3:32b` entries at 40,960.

**At pack scale (~20–32K prompts), fit is the lever and payload curation is not.** The Phase 3 lane
measured curated digests against raw dumps on both local models: curation delivered **no** recall
gain (adjudicated net −4 must-find items, CURATED@40K vs DUMP@40K). The 32K↔40K comparison came out
at net +4 toward 32K, which **breaches the lane's registered |net| ≤ 1 threshold in the *unfeared*
direction**; adjudication decomposes it into two items — one that flips in both directions across
draws and cells, one single-model single-cell miss — so it is read as absence of a 32K deficit,
never as a 32K advantage. Exploratory and untested, with no established mechanism: local CLEAN rows
drew *more* adjudicated fabricated violations under curated evidence than under the dump (19–22 v
10) — one more reason no local CLEAN verdict is a conclusion. None of this changes
detector-not-verdict-authority routing, and none of it extends past pack scale.
```

## 7. Negative space — what this memo does NOT establish or change

- **Nothing at session scale.** Pack scale (~20–32K prompts) only; 163–349-turn payloads are untouched.
- **"DUMP wins" is not licensed.** P1's −4 decomposes to flip-prone items; no reverse-direction claim
  was pre-registered and none is made.
- **P1b's +4 is not a 32K advantage.** It breaches the registered threshold in the unfeared
  direction and decomposes to draw variance. The decision rests on the *absence of a deficit*.
- **No local verdict authority is created.** 19–22 fabricated violations across local CURATED CLEAN
  rows re-confirm detector-not-verdict.
- **The planner, evaluation-report, perspective, bug-report, and ACR suites were not measured by the
  lane.** It is critic-suite only; those suites inherit directionally and must be named untested if
  cited. §3's numbers for them are *guard estimates*, not measured tokens.
- **Single adjudicator per fixture** (opus, ground-truth-loaded); no second-adjudicator agreement pass.
- **The P3-local reversal is a hypothesis, not a mechanism.** Testing it needs CLEAN-heavy cells.
- **What this memo does NOT recommend changing:** `CRITIC_CTX`'s 10 mapped model entries,
  `PERSPECTIVE_CTX`'s 7, `EVALREPORT_CTX_DEFAULT`, `ACR_CTX_DEFAULT`, the 8,192 reserve, the
  chars/3.5 estimator, issue #28's flag, and **every committed row in every lane**. No historical
  result is restated, rescored, or withdrawn by this memo.

## 8. Open items and reopen conditions

- **Planner-suite historical exposure is unmeasured** (task R5.3). Every committed planner row ran
  at a hardcoded-then-defaulted 32,768 (`run_benchmark.py:658` comment) with prompts estimated at
  23,973–25,709 — roughly 7–8K left for thinking plus output on a thinking-by-default model. Phase
  0.4's retro-probe was **critic-suite only**; the planner lane has never been examined. Route a
  Phase 0.4-style `eval_count` analysis before or alongside the `PLANNER_CTX_DEFAULT` raise. This is
  an output-side exposure question, not a prompt-side one — the raise fixes the guard refusals
  either way.
- **Probe granularity** (task R5.2): **per (model × suite)** for mapped entries. For `_DEFAULT`s,
  which exist for models that do not yet exist, size from the current models' probes with the
  densest measured tokenizer governing — and state plainly that for an unknown model the
  **client-side guard, not the default, is the real protection**. A default is a starting guess; the
  guard is the safety property.
- **Issue #28** (`flag_context_pressure` compares against requested `num_ctx`, not the
  declared-clamped effective ceiling; `run_benchmark.py:419`) is **unchanged by this memo** and
  remains a fast-follow. It under-reports pressure exactly when a declared ceiling bites; raising
  defaults toward 40,960 keeps `min()` a no-op for both current local models, so the hygiene pass
  neither aggravates nor fixes it.
- **What would reopen this decision:** a model whose fit cannot be bought with an integer — a
  declared window smaller than protocol + fixture, so no legal `num_ctx` fits the prompt; or
  measured long-context quality decay at a scale P1b did not cover (its whole span is 32,768 ↔
  40,960 — it says nothing about 128K or 256K windows). A native harness digest/summarization
  feature (plan §7 watch rule) would also change the arithmetic and should be adopted rather than
  competed with.
