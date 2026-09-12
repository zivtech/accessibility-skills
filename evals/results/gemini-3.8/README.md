# Gemini 3.8 Flash — a11y-critic benchmark (effort sweep)

**Date:** 2026-09-12 · **Runner:** `ollama/run_gemini_agy_critic.py` (via the Antigravity
`agy` CLI — the repo has no `gemini` CLI). **Scorer:** `ollama/score_output.py`.
**Corpus:** the same 33 a11y-critic fixtures the committed Gemini **2.5 Flash** baseline
used (`evals/results/gemini/`, 31/33). Blind-cut with the hosted lane's `strip_answer_key`.

## Results

| Effort | PASS | FAIL | WARN | Stalls (empty response) |
|---|---|---|---|---|
| **low** | 28/33 | 4 | 1 | 0 |
| **medium** | 28/33 | 5 | 0 | 0 |
| **high** | 28/33 | 5 | 0 | 2 → recovered by retry (raw 26) |
| Gemini 2.5 Flash (baseline) | **31/33** | 2 | — | — |

## Findings

1. **3.8 Flash underperforms 2.5 Flash on this suite** (28 vs 31 / 33) at every effort level.
2. **The failure mode is CLEAN over-flagging, not missed bugs.** Recall on HAS-BUGS is
   near-perfect (100% must-find on almost all). But it flags clean components as REVISE:
   `button-skip-link-clean`, `interactive-dropdown-clean`, and `search-results-dynamic-clean`
   fail at **every** effort level; `modal-complete-clean` fails at medium/high (WARN at low).
   Plus one over-severe verdict on the adversarial `tabbed-nav-vs-tab-pattern` (REJECT where
   ACCEPT-WITH-RESERVATIONS/REVISE is the ceiling). This is the **detector-not-verdict**
   ceiling — same as the local models.
3. **Effort does not improve judgment.** Low = medium = high on PASS count; the failing
   fixtures are essentially the same set. Higher effort only *adds* cost and stall risk.
4. **Reliability: a stochastic empty-response ("/think") stall** hit 2/33 fixtures at HIGH
   effort (valid JSON, clean `stop`, 0-char `response`) — the same failure the repo's funnel
   saw on `qwen3.8:27b` (2026-08-23). **Fixed by retry-on-empty** (`MAX_ATTEMPTS=3`): both
   recovered, taking high 26 → 28. Low/medium had 0 stalls.

## Recommendation

- Gemini 3.8 Flash is a strong **detector** (high recall, cheap) but **not a trustworthy
  verdict authority** — it over-flags clean code regardless of effort. Use it the same way
  as the local tier: surface candidates → human or stronger judge verifies.
- If used, run at **low effort** — equal detection to medium/high, cheapest, no stalls.
- It is **not** a drop-in cheaper replacement for a Claude critic verdict.

## Connective note

The retry-on-empty fix validated here targets the exact stall that made the repo **stop
`qwen3.8:27b`** at Stage 1 (zero-incompletions gate) despite champion-equal detection.
Re-testing `qwen3.8:27b` with retry could unblock a stalled *local* model — a separate
follow-up.

## Files

`gemini-bench-<fixture>-flash-<effort>-response.json` — raw response + token usage +
`attempts` per fixture-effort. Reproduce: `python3 ollama/run_gemini_agy_critic.py <low|medium|high>`;
tally: `python3 ollama/tally_gemini_38.py <effort>`.
