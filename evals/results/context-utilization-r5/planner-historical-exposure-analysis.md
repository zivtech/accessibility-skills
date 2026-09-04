# R5.3 — Historical local-planner exposure to OUTPUT-side context clipping (num_ctx = 32,768)

**Date:** 2026-08-27
**Task:** R5 decision memo (`docs/plans/2026-08-27-context-utilization-r5-decision-memo.md`) §4 row
**R5.3**, opened by §8: *"Planner-suite historical exposure is unmeasured … Phase 0.4's retro-probe
was critic-suite only; the planner lane has never been examined. Route a Phase 0.4-style
`eval_count` analysis before or alongside the `PLANNER_CTX_DEFAULT` raise."*
**Scope:** all **57** committed local (Ollama) planner rows —
`evals/results/new-local-models-2026-07/stage2-qwen36-35b` (25),
`.../stage2-laguna-s` (25), `evals/results/wcag-em-step11` (3),
`evals/results/ict-baseline-phase3` (4). Hosted planner rows (`claude-planner`, `codex-planner`)
are out of scope — they never ran under `num_ctx`.
**Question:** how many of these rows were cut off *by the ceiling* (output side), as distinct from
the prompt-side truncation Phase 0.4 examined?

---

## Headline

**3 of 57 rows are output-clipped, and unlike Phase 0.4 the flag is corroborated, not contradicted.**
All three carry `done_reason=length`, all three land at `prompt_eval_count + eval_count = 32,768`
**exactly**, and all three end mid-sentence. Phase 0.4's critic-suite verdict was *"(c) not in
evidence"*; the planner lane's verdict is **confirmed clipping, three rows, named below**.

This lane also had a measurement advantage Phase 0.4 lacked: every planner row carries the server's
own `prompt_eval_count`, `eval_count`, and `done_reason` at top level. **Nothing here is estimated
where it could be measured.**

---

## 1. Method

Prompt assembly is imported from `ollama/run_benchmark.py` (`load_planner_system_prompt`,
`load_planner_federal_system_prompt`, `PLANNER_PROMPT_PREFIX`, `load_fixture` → `strip_answer_key`) —
never re-implemented. Historical `num_ctx` for every row is **32,768**: the value was a hardcoded
literal applying identically to both `planner` and `planner-federal` until the 2026-08-24 Phase 0.2
map-hygiene lift, which preserved it as `PLANNER_CTX_DEFAULT = 32768` with an empty `PLANNER_CTX`
(`run_benchmark.py:654-659` comment, verified against git history).

Definitions: `budget = 32,768 − prompt_eval_count`; `headroom = budget − eval_count`.
Ceiling contact = `headroom ≤ tol`.

**Cross-check on the counts themselves:** `len(context)` (the token array Ollama returns) equals
`prompt_eval_count + eval_count` to within 0–2 tokens on all 57 rows. Both counts are real.

### 1.1 A contaminated ratio, found and discarded

The first pass computed each row's guard estimate from **today's** `a11y-planner/SKILL.md` against
each row's **historical** `prompt_eval_count`, yielding a median `est/measured` of **1.394** — well
outside the 1.22–1.30 the codebase documents. That figure is **wrong and is discarded**: the planner
protocol grew from **71,881 chars (2026-07-16)** to **83,013 chars (2026-08-25)**, so it compares a
larger prompt's estimate against a smaller prompt's measurement.

Recomputed against the `SKILL.md` blob **in effect on each row's own date**:

| era dir | row dates | `SKILL.md` as-of | rows | era-correct `est/measured` median |
|---|---|---|---|---|
| `stage2-qwen36-35b` | 2026-07-29 | `c0cedd44` | 25 | 1.293 |
| `stage2-laguna-s` | 2026-07-29 | `c0cedd44` | 25 | 1.297 |
| `wcag-em-step11` | 2026-08-02 | `8f097579` | 3 | 1.219 |
| `ict-baseline-phase3` | 2026-08-12 | `fb399c82` | 4 | 1.222 |

Overall era-correct: **min 1.190 / median 1.295 / max 1.305** — inside the documented 22–30% band and
consistent with the 2026-08-27 live probes (R5.2). The protocol-drift finding is kept as a finding in
its own right (§4).

---

## 2. Per-era table

| era dir | model | condition | rows | `prompt_eval_count` min/med/max | `eval_count` min/med/p90/max | `done_reason=length` | headroom ≤ 1000 |
|---|---|---|---|---|---|---|---|
| `stage2-qwen36-35b` | qwen3.6:35b | planner | 25 | 17204/17890/18551 | 4901/7209/9437/10227 | **0** | 0 |
| `stage2-laguna-s` | laguna-s-2.1:q4_k_m | planner | 25 | 17166/17844/18485 | 116/2796/14510/15455 | **2** | 2 |
| `wcag-em-step11` | qwen3.6:35b | planner | 2 | 18517/18517/18517 | 6093/6893/7693/7693 | 0 | 0 |
| `wcag-em-step11` | qwen3:32b | planner | 1 | 17993 | 2430 | 0 | 0 |
| `ict-baseline-phase3` | qwen3.6:35b | planner | 1 | 20050 | 6781 | 0 | 0 |
| `ict-baseline-phase3` | qwen3.6:35b | **planner-federal** | 1 | 25792 | 6976 | **1** | 1 |
| `ict-baseline-phase3` | qwen3:32b | planner | 1 | 19520 | 3456 | 0 | 0 |
| `ict-baseline-phase3` | qwen3:32b | planner-federal | 1 | 25006 | 3388 | 0 | 0 |

Ceiling contact is **3/57 at every tolerance tested (100, 300, 1000)** — the distribution is bimodal,
not a gradient: rows either finish with thousands of tokens spare or land on 32,768 exactly. There is
no ambiguous middle band, which is why this lane admits a verdict where Phase 0.4's did not.

---

## 3. The three clipped rows, with structural corroboration

| row | `pec` | `eval_count` | sum | response ends |
|---|---|---|---|---|
| `ict-baseline-phase3/ollama-planner-federal-test-federal-agency-audit-qwen36-35b-response.json` | 25,792 | 6,976 | **32,768** | `…\| 🔍 3 \| Report` — mid table row |
| `stage2-laguna-s/ollama-planner-keyboard-modal-focus-trap-laguna-s-21-q4_k_m-response.json` | 17,313 | 15,455 | **32,768** | `…[WCAG 2` — mid link title |
| `stage2-laguna-s/ollama-planner-test-data-table-laguna-s-21-q4_k_m-response.json` | 17,977 | 14,791 | **32,768** | `…const visualIndicator = dateHeader` — mid statement |

Two mechanisms, not one:

- **laguna-s (2 rows): runaway generation.** No thinking stream at all (`thinking` absent), 60–64K
  **characters** of response, `eval_count` 14.8–15.5K. These rows did not run out of room because
  the prompt was large — the prompt was the era's *smallest* — they ran out because the model kept
  going. Consistent with the July funnel's recorded verdict on laguna-s (0/6 on bug-reporting, worst
  data fidelity). Raising `num_ctx` would let these rows run longer; it would not make them better.
- **qwen3.6:35b `planner-federal` (1 row): genuine fit pressure.** 25,792 prompt tokens + 14,441
  chars of thinking + 15,065 chars of response, cut at the ceiling. This is the only row in the
  corpus where the *prompt* is what left too little room.

### 3.1 Disposition of the clipped federal row — annotate, never rewrite

`evals/results/ict-baseline-phase3/README.md:104` scores that row **10/11 PASS, 0 markers, 0
fabrications**, and its adjudication (`:116-122`) attributes the single miss to paraphrase on item 8.
**That score is not restated, rescored, or withdrawn here** (memo §5.2, §7). What is now on record is
that the row is an **incomplete generation**: it was cut mid-table inside a closing verification
checklist, after the plan body the 11-item gate scores against. The recorded adjudication remains the
best reading of what the row contains — but "the response ended there because the model finished" was
never true of this row, and the receipt should say so.

`evals/results/ict-baseline-phase3/README.md` carries no mention of `done_reason`, `length`, or
clipping (grep, 2026-08-27). The three other ICT planner rows are clean (`done_reason=stop`).

---

## 4. What this says about the R5.4 planner raise

1. **The raise is justified on the output side, and that is a different argument from the memo's.**
   The memo's §3 case for 40,960 is prompt-side: *19 of 28 fixtures already refuse at 32,768.* But
   those refusals are the **estimator's**, not the server's — measured against real
   `prompt_eval_count`, only **2 of 57** committed rows would truly have overflowed
   (`pec + 8,192 > 32,768`), both `planner-federal`. On the plain condition the true prompt sits at
   ~17–20K with ~13–15K of real headroom. **The prompt-side case for the raise is largely an artifact
   of the 3.5 chars/token estimator; the output-side case (§3, three confirmed clips) is not.**
2. **No committed row would have clipped at 40,960.** `pec + eval_count ≥ 40,960` on **0/57** rows.
   The raise clears every historical row, including the runaway laguna-s pair.
3. **The 8,192 reserve is not notional on this suite.** **13 of 57** rows generated *more* than 8,192
   output tokens. The reserve is a floor that real planner rows routinely exceed — it is sized for
   the median, not the tail.
4. **Protocol drift eats headroom silently.** `a11y-planner/SKILL.md` grew **+11,132 chars ≈ +2,800
   real tokens** between the July rows and today. Every 2026-07 row in this corpus ran with ~2,800
   more output tokens available than the same fixture would get today at the same `num_ctx`. **The
   historical rows therefore understate today's exposure**, and this analysis's 3/57 is a floor, not
   a current rate. A protocol that grows while `num_ctx` is fixed is a slow squeeze on the output
   side that nothing in the harness currently watches.

## 5. Negative space

- **Only local rows.** Hosted planner rows have no `num_ctx` and are untouched.
- **No score is changed.** Not one row is rescored, re-adjudicated, or withdrawn. §3.1 adds a fact to
  the record; it revises no verdict.
- **Clipping ≠ wrong answer.** Two of three clipped rows are a model over-generating; whether
  truncation changed any *score* was not tested and is not claimed.
- **Not a rate.** 3/57 is this corpus at these protocol sizes. §4.4 gives the reason it is a floor.
- **Not a prompt-side finding.** Prompt-side truncation is Phase 0.4's question and the live-probe
  README's; this is output-side only.
- **`planner-federal` n = 2.** Every claim about the federal condition rests on two rows, one per
  model. Directional.
