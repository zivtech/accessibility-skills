# New Local Model Benchmark — August 2026 reopen: Qwen 3.8 (receipts, in progress)

Reopens the funnel of [docs/plans/2026-07-28-new-local-model-benchmark-plan.md](../../../docs/plans/2026-07-28-new-local-model-benchmark-plan.md) on its own reopen-trigger: **Qwen 3.8 open weights** (the plan's watch item was "Qwen 3.7 open weights"; 3.7 never shipped open, 3.8 did). Same staged protocol (Stage 0 smoke → Stage 1 ten-fixture screen → Stage 2 full lanes → Stage 3 ×3-draw verdict stability), same gates, same scorers. Comparison baselines: the post-PR-4 unassisted qwen3:32b lane (`evals/results/ollama-rebaseline/`) and the July champion qwen3.6:35b (`evals/results/new-local-models-2026-07/`).

## Candidate

| Model | Tag | Size | Arch | Notes |
|---|---|---|---|---|
| Qwen 3.8 27B | `qwen3.8:27b` (= `qwen3.8:latest`) | 18 GB | dense 27B, 256K ctx, **thinking on by default** (per-request disable, `reasoning_effort`), vision + tools | Only size published on the Ollama library (verified 2026-08-23, 12 tags, all 27B). The `:27b`/`:latest` digest `22130167c4c2` is the **MTP** q4_K_M build (identical digest to `27b-mtp-q4_K_M`); the plain `27b-q4_K_M` is a different digest (`25b843619e94`). Run as pulled — default tag, default reasoning effort, thinking left on. |

Size-class note: this is a 27B against a 35B champion; the July sibling `qwen3.6:27b` stopped at Stage 1 (15/15 detection, 3/4 CLEAN wrong).

## Environment (as run, 2026-08-23)

- Hardware: MacBook Pro M5 Max, 128 GB unified (Metal reports 107.5 GiB available).
- **ollama 0.32.15** — newer than every July lane (0.31.1 / 0.32.5). Runtime shift is a disclosed condition, not controlled for.
- Transport: dedicated server `127.0.0.1:11435` (`OLLAMA_HOST=127.0.0.1:11435 …/Ollama.app/Contents/Resources/ollama serve`, version-pinned for the window). **Deviation from the July invariant:** Ollama.app was *not* quit — it declined the graceful AppleScript quit (`-128`) and force-killing a GUI app was judged worse than the risk; its `:11434` server was verified idle (`/api/ps` → `[]`) at every stage boundary and received no traffic. `caffeinate -is` wraps every batch.
- Corpus: branch `feat/verification-evidence-contract` @ `67d5847` = `main@0503744` + 9 new critic/planner fixtures (2026-08-14, no model rows from any model yet) + **one conditional Phase 0 bullet in the critic prompt** (fix-review evidence typing; no benchmark fixture attaches fix evidence, so it is inert for this lane — disclosed, not byte-identical to July). Preflight `test_blind_prompts.py`: **OK, 188 prompts**.
- Runner (uncommitted at run time; diff recorded here): `qwen3.8:27b` added to `CRITIC_CTX` and `PERSPECTIVE_CTX` at 32768 (new-model default since July); the two streaming runners (`run_ollama`, `run_perspective`) now record `done_reason` and `thinking_chars` in `_benchmark` — the July README's hardening item (finding 2). Scorers unmodified.
- Screening subset (10): `form-validation-missing-aria-describedby`, `toast-notification-no-role`, `infinite-scroll-no-announcement`, `accordion-no-region-role`, `tooltip-no-role-no-association`; CLEAN ×4 (`button-skip-link`, `interactive-dropdown`, `modal-complete`, `search-results-dynamic`); ADVERSARIAL `tabbed-nav-vs-tab-pattern`.
- Gates (recomputed from the July artifacts with the unmodified scorer, same subset): qwen3:32b unassisted = **12/15 must-find, 1/4 CLEAN wrong**; qwen3.6:35b = **15/15, 1/4**. Advance requires **≥10/15, ≤1/4 CLEAN wrong, 0 incompletions**.

## Pre-run probes (`stage0/probes/`, 2026-08-23)

1. **Thinking-token audit** (trivial prompt, streamed): reasoning lands in a separate `thinking` field (105 chars on the trivial probe), zero inline `<think>` in `response`, `done_reason=stop` — scored text is clean by construction, same mechanism as qwen3.6. The runner's new `thinking_chars`/`done_reason` capture sees the channel.
2. **Critic-prompt token count** (real system prompt + `form-validation-missing-aria-describedby`, `num_predict=1`): **`prompt_eval_count` 15,609** — the first current-gen tokenizer measured *under* the 16,384 boundary, but only by ~775 tokens; with thinking sharing the window the 32768 `CRITIC_CTX` entry stands (the artifact's `done_reason=length` is the forced `num_predict=1`, not a clip).

## Stage 0 — smoke (2026-08-23 15:07–15:35, `stage0/`)

| Fixture | Verdict | Must-find | Status | elapsed | thinking chars | done_reason |
|---|---|---|---|---|---|---|
| form-validation-missing-aria-describedby | REVISE (expected REVISE) | **2/2** | PASS | 885 s | 16,576 | stop |
| button-skip-link-clean | ACCEPT-WITH-RESERVATIONS (correct) | – | WARN — correct verdict, raised findings | 801 s | 23,483 | stop |

**Kill criteria: PASS** (both `done_reason=stop`, verdicts parseable, no `<think>` leak, no empty response). The CLEAN draw raised the known `tabindex="-1"`-on-`<main>` hardening note as a MAJOR finding (the same item qwen3:32b turned into its wrong REVISE in the rebaseline lane) but held the correct verdict and stated explicitly what would flip it either way.

**Speed finding (default tag, as pulled):** ~**12 tok/s** end-to-end (eval_count ≈ 10K per fixture over 800–885 s) — roughly 5× slower per fixture than qwen3.6:35b's July pace. Not a CPU fallback: `/api/ps` shows `size == size_vram` (18.3 GB, ctx 32768). The cause is visible in the server log: ollama 0.32.15 launches `llama-server --spec-type draft-mtp --spec-draft-n-max 4 --spec-draft-backend-sampling` (Modelfile `PARAMETER draft_num_predict 4`), and the MTP speculative path reports draft acceptance 0.61 (mean accepted length 3.4) with drafting alone costing ~183 s of the first ~1,690 s. Speed is a reported characteristic, not a gate; the lane runs the default configuration users get. A `draft_num_predict 0` (plain-decode) speed probe is a follow-up side experiment, deliberately not run inside the lane.

## Stage 1 — screening (2026-08-23 15:07–17:08, `stage1-qwen38-27b/`; smoke artifacts copied in)

| Fixture | Kind | Verdict | Must-find | Status | thinking chars |
|---|---|---|---|---|---|
| form-validation-missing-aria-describedby | BUGS | REVISE | 2/2 | PASS | 16,576 |
| toast-notification-no-role | BUGS | REJECT | 4/4 | PASS | 5,050 |
| infinite-scroll-no-announcement | BUGS | REJECT | 4/4 | PASS | 5,921 |
| accordion-no-region-role | BUGS | REVISE | 2/2 | PASS | 8,015 |
| tooltip-no-role-no-association | BUGS | REJECT | 2/3 scorer → **3/3 content-adjudicated** | PASS | 7,016 |
| button-skip-link-clean | CLEAN | ACCEPT-WITH-RESERVATIONS | – | WARN (correct verdict, findings raised) | 23,483 |
| interactive-dropdown-clean | CLEAN | **REVISE — wrong** | – | FAIL | 30,898 |
| modal-complete-clean | CLEAN | **NONE — 0-char response** | – | FAIL (incompletion) | 38,824 |
| search-results-dynamic-clean | CLEAN | ACCEPT-WITH-RESERVATIONS | – | WARN (correct verdict, findings raised) | 24,720 |
| tabbed-nav-vs-tab-pattern | ADV | **REJECT — outside valid set** | – | FAIL | 26,108 |

- **Detection: 15/15 content-adjudicated** (scorer 14/15; the tooltip announcement item is stated verbatim in the response — "Screen reader announces only the button's text content. Tooltip content is inaccessibly orphaned" — a keyword gap, the same adjudication this pair fixture needed in the July lanes). Matches qwen3.6:35b's screening draw; above the qwen3:32b baseline (12/15 scorer).
- **CLEAN verdicts: 1 judged wrong of 3 judged** — interactive-dropdown REVISE, lead findings (`aria-activedescendant`, click-outside, active/selected conflation) in the same class as qwen3.6:35b's *stable* failure on this exact fixture: a third sibling confirming the family blind spot. button-skip-link and search-results correct-with-findings (button-skip-link raised the known `tabindex="-1"` hardening note but held the verdict — better calibrated here than the qwen3:32b baseline's wrong REVISE).
- **Incompletion: 1** — `modal-complete-clean` produced **38,824 chars of thinking then a clean `stop` with zero response tokens** (25.4K/32K ctx used — *not* a context clip; the July hardening fields distinguish this for the first time). This is the qwen-family "/think stall" class (qwen3.5:27b's documented flaw) in a new shape: thought-then-silence rather than thought-forever. Re-draw adjudication below.
- **ADVERSARIAL: REJECT** where {ACCEPT-WITH-RESERVATIONS, REVISE} are valid — severity overshoot one notch beyond the family trait July recorded (REJECT-where-REVISE now reaching the adversarial fixture).
- **CLEAN-rumination signature:** thinking volume 3–5× higher on CLEAN fixtures (23K–39K chars) than HAS-BUGS (5–8K) — clean code makes it ruminate, and both failures (the false alarm and the stall) sit in the high-rumination bucket.

### Gate verdict — **STOP as-run**

| Gate | Requirement | qwen3.8:27b | Result |
|---|---|---|---|
| Detection | within 2 of qwen3:32b's 12/15 (≥10/15) | 15/15 adjudicated | ✓ |
| CLEAN verdicts wrong | ≤1 | 1 judged wrong + 1 non-execution | ✗ (borderline read) / ✓ (strict judged-only read) |
| Incompletions | zero | **1** (modal stall) | **✗** |

The zero-incompletions gate is violated on either reading, so the funnel stops at Stage 1 per protocol — the same gate that stopped ornith:35b (2/10) in July. Stage 2 full lanes were **not** run.

### Stall re-draw (adjudication, not a lane row)

One byte-identical re-draw (`…-response-REDRAW1.json`, thinking text captured this time, clearly off-lane — the as-run 0-char artifact stands and the gate ruling is unchanged):

| Draw | resp chars | thinking chars | done_reason | Verdict | Scorer |
|---|---|---|---|---|---|
| as-run | 0 | 38,824 | stop | NONE | FAIL (incompletion) |
| REDRAW1 | 20,028 | 23,582 | stop | ACCEPT-WITH-RESERVATIONS (correct) | **PASS, zero structured findings** |

**Adjudication: stochastic stall, recovers on retry** — the qwen3.5:27b reliability profile ("prone to /think stalls — use with retry") reappearing in 3.8 in a new shape (think-then-silent-stop rather than think-forever; `done_reason=stop`, no context clip, MTP speculative path active). And when it does answer, its modal-complete verdict is a *cleaner* pass than qwen3.6:35b's July draws on the same fixture (correct-with-findings WARNs). Frequency observed: 1 stall in 11 critic generations this window.

## Outcome — STOP at Stage 1; no routing change

Best 27B screening profile ever recorded in this funnel — champion-equal detection (15/15 adjudicated), CLEAN calibration far better than qwen3.6:27b's 3/4-wrong — stopped by **reliability** (stochastic stall class, zero-incompletions gate) plus the severity overshoot reaching the ADVERSARIAL fixture, not by detection. qwen3.6:35b remains the detector recommendation; every routing rule stands. Stage 2/3 not run.

Reopen watch items for this candidate line: (a) a qwen3.8 ≥32B sibling on the library (only 27B tags exist as of 2026-08-23); (b) an ollama runtime change to the MTP/termination path — the stall and the ~12 tok/s default-tag speed are both plausibly runtime-coupled (`--spec-type draft-mtp`, acceptance 0.61) and worth one cheap re-probe on the next ollama minor; (c) the deferred `draft_num_predict 0` plain-decode speed probe.
