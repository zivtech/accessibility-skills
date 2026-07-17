# Ollama blind re-run lane — raw artifacts (2026-07-13)

- Run date: 2026-07-13; transport: local Ollama 0.31.1 on a **dedicated `127.0.0.1:11435` server** (Ollama.app quit for the run; `*:11434` reverted to the OrbStack container so claude-smart traffic never touched the benchmark GPU). Full Metal offload verified via `/api/ps` (`size == size_vram`, 24.7 GB).
- Runner: `python3 ollama/run_benchmark.py critic-remaining qwen3:32b` then `perspective-remaining qwen3:32b`, with `OLLAMA_URL=http://127.0.0.1:11435/api/generate` and `BENCHMARK_RESULTS_DIR` pointed at this directory. Same prompts, num_ctx (16384 critic / 32768 perspective), and temperature (0.3) as the historical lanes.
- **Blind protocol (post-003):** `load_fixture()` strips everything from the `## Accessibility Issues…` heading onward before prompting (guard: `ollama/test_blind_prompts.py`, 116 prompts verified answer-free). This is the first **local** blind lane; every pre-2026-07-13 local row ran non-blind — see the blind-protocol disclosure at the top of `ollama/BENCHMARK.md`.
- Scoring: post-003 `ollama/score_output.py` / `ollama/score_perspective.py`, one output per fixture under `scores/`. Raw response JSONs (`response` + `_benchmark` provenance) are committed here so every number below can be re-derived.

> **Hint-comment caveat (2026-07-16).** These prompts were answer-key-blind but **not hint-blind**:
> at run time, 24/33 critic and 20/25 perspective fixtures still carried inline `// BUG: …` hint
> comments in their code blocks (removed repo-wide 2026-07-16 — see the hint-comment disclosure in
> `ollama/BENCHMARK.md`). "Blind-confirmed" below means confirmed with answer keys withheld, not
> hint-free: must-find/detection numbers are hint-assisted upper bounds pending a de-hinted re-run.
> The CLEAN rows carried no hints, and the perspective CLEAN false-positive finding stands.

> **Reassurance/verdict caveat (2026-07-16 follow-up).** The critic CLEAN and ADVERSARIAL rows in
> this lane are additionally **verdict-assisted**: at run time the 4 critic CLEAN and 3 critic
> ADVERSARIAL fixtures had **no** `## Accessibility Issues` cut line, so `load_fixture()` passed
> their Difficulty Level / Notes sections — "**CLEAN** — … Should receive a clean verdict", the
> ADVERSARIAL grading criteria, and (for adversarial) the full "The Ambiguity" tension analysis —
> into the prompts. The paragraph below the headline table reads "critic CLEAN prompts are
> identical blind or not" as evidence the result is not inflated; identical, yes — but identically
> *including the expected verdict*. Treat critic CLEAN 4/4 (0 FP) and ADVERSARIAL 3/3 as
> verdict-assisted upper bounds pending a re-run against the fixed fixtures (cut lines inserted
> 2026-07-16; reassurance comments also removed suite-wide the same day, raising FP-trap
> difficulty). See the reassurance & verdict-steering disclosure in `ollama/BENCHMARK.md`.

## Headline — qwen3:32b

| Suite | Result (post-003 scorer) | Historical non-blind row | Verdict on the historical number |
|---|---|---|---|
| a11y-critic, 33 fixtures | **33/33 PASS**, must-find 66/68 (97.1%), CLEAN 4/4 with **0** structured findings, ADVERSARIAL 3/3 articulated | 33/33 PASS, ~97% must-find, 0 FP | **Confirmed blind.** Not answer-key-inflated. |
| perspective-audit, 25 fixtures | **20 PASS / 1 WARN / 4 FAIL**; HAS-BUGS 16/16, ADVERSARIAL 4/4, must-find 36/37; **CLEAN 4/5 wrong verdicts** (REVISE/BLOCK on clean components) | 16/16, 4/4, must-find 100%, CLEAN 4 WARN / 1 FAIL (4/5 correct PASS verdicts) | **Detection confirmed; CLEAN false-positive resistance does NOT survive blinding.** |

The asymmetry has a structural explanation: **critic CLEAN fixtures never carried answer sections** (verified — no `## Accessibility Issues` heading in any of the 4), so critic CLEAN prompts are identical blind or not, and the result reproduced exactly. **All 5 perspective CLEAN fixtures carry an answer section that literally says "NONE. This … is correctly implemented"** — the historical run showed that reassurance to the model. Withhold it and qwen3:32b manufactures findings or inflates verdicts on 4 of 5 clean components.

> **2026-07-16 amendment (modal-complete-clean erratum).** Two qualifiers to the critic CLEAN row
> above. (1) "Identical blind or not" is not the same as *unhinted*: all 4 critic CLEAN fixtures
> carried "should receive a clean verdict / ACCEPT" prose in the model-visible body, so the
> critic CLEAN 4/4 measured hint-following as much as calibrated false-positive avoidance.
> (2) `modal-complete-clean` carried two real **unplanted** defects at run time (incomplete
> focus-trap selector; unguarded overlay `onClick` closing the dialog on any in-dialog click) —
> this lane's committed response mentions neither, so that ACCEPT is a missed-defect data point,
> not validated FP avoidance. Fixture fixed at source and de-hinted 2026-07-16; the row converts
> to valid evidence only via a re-run against the 1.1 fixture. See `ollama/BENCHMARK.md` →
> Scoring changelog (2026-07-16).

## a11y-critic detail (33 fixtures, 1.45 h total, avg 158 s/fixture)

- Tier statuses: HAS-BUGS 21/21 PASS, FLAWED 5/5 PASS, CLEAN 4/4 PASS, ADVERSARIAL 3/3 PASS.
- Aggregate must-find 66/68 (97.1%). The two scorer-level misses, adjudicated against the committed response text:
  1. `expandable-section-no-button` — "Using `<div>` instead of `<button>`": **keyword artifact, content present.** The audit writes "uses a non-interactive div as a toggle trigger" and "Fix: Replace div with `<button>` element"; the rubric keyword is the literal angle-bracketed `<div>`, which prose doesn't emit. Content-adjudicated coverage 4/4.
  2. `infinite-scroll-no-announcement` — "Scroll-to-load mechanism not discoverable": **genuine partial miss.** The audit notes the impact ("won't know new content is available until they scroll") but never raises discoverability/manual-load-more as a finding.
  - Content-adjudicated must-find: **67/68 (98.5%)**.
- CLEAN: all four fixtures scored PASS with **zero** structured findings and correct verdicts (one plain ACCEPT, three ACCEPT-WITH-RESERVATIONS). *(2026-07-16: the modal-complete-clean pass is a missed-defect data point — see amendment above.)*
- ADVERSARIAL: 3/3 ACCEPT-WITH-RESERVATIONS with the central tradeoff articulated — same behavior as non-blind.
- **The historical toast `role="alert"` detection gap did not reproduce**: blind run found 4/4 on `toast-notification-no-role`, including `role="alert"`. The "real model-specific detection gap" language in the historical notes overstated stability — treat it as run-to-run variance at temperature 0.3.
- Verdict severity inflation persists blind (7 REJECT where rubric expects REVISE); as before, the gate scores detection, not verdict match, on HAS-BUGS/FLAWED.

### Timing — the historical FLAWED/ADVERSARIAL slowdown was contention, not reasoning depth

| Tier | Blind (this run) median | Historical (2026-05-15) median |
|---|---|---|
| HAS-BUGS | 133 s | 172 s |
| FLAWED | **224 s** | **3,508 s** |
| ADVERSARIAL | **222 s** | **3,007 s** |

Same model, quant, num_ctx, temperature. The dedicated-server protocol (no second model copy resident, no :11434 traffic) removes the 15× FLAWED-tier blowup. The Phase 4A "extended reasoning on subtle bugs" interpretation should be read as substantially a GPU-contention artifact. (Negative space: the May run wasn't instrumented for contention, so attribution is inferred, not proven — but the 8.0 h → 1.45 h collapse under otherwise-identical settings leaves little room.)

## perspective-audit detail (25 fixtures, 1.36 h total, median 192 s/fixture)

- HAS-BUGS 16/16 PASS, ADVERSARIAL 4/4 PASS. No LOW-perspective leakage anywhere.
- Must-find 36/37 scorer-level. The single residual is the known rubric artifact also seen in the Claude Opus blind lane: `tab-panel-arrow-keys`' scoring keyword is the compound string `role='tablist'/role='tab'/role='tabpanel'`, which no prose audit emits verbatim; the audit cites the criterion and discusses the roles (scorer shows `[W]`). Content-adjudicated: **37/37**.
- **CLEAN lane — the blind finding of this run.** 4/5 wrong verdicts, all receipts verifiable in the committed JSONs:
  1. `nav-menu-landmarks` — **BLOCK** on two manufactured CRITICALs: missing `<title>` and missing `lang` on `<html>` — flagged against a React *component* fixture with no document shell, while the audit's own checklist records nine PASS lines. This is the documented "page-shell WCAG over-flagging" characteristic, now producing a false BLOCK when unrestrained by the answer key.
  2. `dashboard-text-labels` — **REVISE** on two manufactured MAJORs: "status indicator contrast below 3:1" is contradicted by the fixture source (documented ratios 5.6:1–18.4:1, status uses text + icon, explicitly not color-only), and "missing forced-colors support" is cited as 1.4.11, which does not require forced-colors support.
  3. `login-form-clean` — verdict line "**REVISE** (MAJOR finding present)" while its own findings table contains nothing above MINOR (2 MINOR + 1 ENHANCEMENT). Internally inconsistent verdict inflation. (Scorer extracted BLOCK via the tier-3 fallback because the conclusion format `**REVISE** (…` has a parenthesis where the tier-2 regex expects a dash; immaterial to status — REVISE and BLOCK both fail a CLEAN fixture.)
  4. `media-player-captions` — **REVISE** over two MINOR "cannot be confirmed from source — requires human verification" open questions. Correct open questions, over-severe next-step.
  - `article-page-clean` — correct PASS verdict; 3 findings at MINOR/ENHANCEMENT → scorer WARN (severity-blind finding-count flag). Meets the repo's CLEAN bar (0 CRITICAL/MAJOR).
- Failure-mode split: 2 fixtures with manufactured CRITICAL/MAJOR findings (breach the CLEAN bar on substance), 2 fixtures with verdict inflation over MINOR-level content (breach on calibration). Both modes are model behavior, **not** scorer artifacts — unlike the Claude lane's pre-003 FAILs, these audits literally conclude REVISE/BLOCK.

## What changes in the published story

- qwen3:32b's **critic-suite** numbers (including the "0% false positives" claim) are blind-confirmed and slightly improved.
- qwen3:32b's **perspective-audit CLEAN false-positive resistance was answer-key-dependent** and must be caveated wherever the historical 25-fixture perspective row is cited. Detection (must-find, coverage, escalation discipline) survives blinding fully.
- Published rows live in `ollama/BENCHMARK.md` → "Ollama blind re-run lane"; historical rows stand with the non-blind caveat per the disclosure block.

## Also in this directory — qwen3.5:latest and llama3.3:70b blind critic lanes

Same day, same protocol, same server. First **full-suite** runs for both (historical rows were
n=7 and never touched FLAWED/ADVERSARIAL). Both lanes' CLEAN tallies carry the 2026-07-16
modal-complete-clean amendment above (their committed responses mention neither defect).

- **llama3.3:70b**: 33/33 PASS, must-find 63/68 scorer / 66/68 content-adjudicated (three
  keyword artifacts — file-input restrictions raised as help-text association, tooltip
  announcement described in prose, video-player "caption toggle button" vs keyword
  'controllable' — and two genuine misses: megamenu arrow-key navigation, infinite-scroll
  discoverability). 1.66 h, median 171 s, zero truncations.
- **qwen3.5:latest**: 33/33 PASS, must-find 67/68 (98.5%), CLEAN 4/4 with zero findings,
  ADVERSARIAL 3/3. Median 34 s/fixture — the fastest lane. **Context-ceiling receipts**: at the
  lane-standard 16K ctx, 4 fixtures truncated mechanically — 3 empty (`done_reason=length`
  inside the thinking phase; prompts tokenize to 15,773–16,102 tokens, leaving exactly the
  335/282/611 tokens of generation room the empty runs recorded; reproduced twice each) and 1
  cut mid-audit (`multistep-form-error-clearing`, prompt 16,899 tokens — bigger than the whole
  16K window). Re-run at `num_ctx=32768` with `num_ctx_override` provenance in the artifacts:
  all four complete (`done_reason=stop`), and multistep finds the planted bug it appeared to
  miss. The three empty-at-16K originals were replaced (they contained no audit content — the
  retry precedent set by the qwen3.5:27b stall handling and the claude-perspective lane);
  the multistep original was replaced under the same mechanical-truncation rationale, receipt
  above. The single remaining scorer miss is the same `infinite-scroll` discoverability item
  all three local models miss blind.

Score any response here with:

```bash
python3 ollama/score_output.py <response.json> evals/suites/a11y-critic/fixtures/<id>.metadata.yaml
python3 ollama/score_perspective.py <response.json> evals/suites/perspectives/fixtures/<id>.metadata.yaml
```
