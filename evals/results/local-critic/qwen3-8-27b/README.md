# qwen3.8:27b — retry-on-empty unblock (2026-09-13)

**Question:** the July/August funnel stopped `qwen3.8:27b` at Stage 1 on 2026-08-23
*solely* on the zero-incompletions gate — a stochastic `/think` stall (valid JSON, clean
`done_reason=stop`, 0-char response) — despite champion-equal detection (15/15 adjudicated).
The `run_local_critic.py` retry-on-empty fix (`MAX_ATTEMPTS=3`, from the Gemini bench PR #79)
was hypothesized to unblock it. This run tests that on the full 33-fixture critic set.

## Result — UNBLOCKED

| Metric | qwen3.8:27b | Champion qwen3.6:35b |
|---|---|---|
| Empty-stall incidents | **3 fired, all recovered, 0 hard fails** | n/a |
| HAS-BUGS detection | **29/29 caught** | strong |
| Correct verdict (PASS + WARN) | **31/33** | 31/33 |
| CLEAN false-alarms | **2/4** (`button-skip-link-clean`, `interactive-dropdown-clean`) | 1/4 |
| gpt-oss-style Phase 0 refusals | **0/33** | 0 |
| Speed | ~6 min/fixture (~3.3 hr full sweep), ~15 tok/s | faster |

The stall fired on 2 fixtures: `app-focus-order-illogical` (empty attempt 1 → recovered
attempt 2) and `async-form-vague-success` (empty attempts 1 **and** 2 → recovered attempt 3).
Because a fixture can stall twice in a row, **`MAX_ATTEMPTS=3` is the correct floor** — a
2-attempt cap would have hard-failed `async-form`. Retry-on-empty is the durable, generalizable
win (same failure class as the Gemini 3.8 high-effort stall in PR #79).

## Verdict — champion holds

`qwen3.8:27b` is now a **viable candidate** (past the Stage-1 gate that stopped it), with
champion-equal detection and zero task-refusals. It does **not** displace `qwen3.6:35b`:
CLEAN over-flagging is worse (2/4 vs 1/4), it is ~6× slower, and this is a **single draw**.
The promotion bar requires ×3-draw CLEAN characterization, and single-draw CLEAN verdicts are
known-unreliable on this family (see `ollama/BENCHMARK.md` disclosures). Detector-not-verdict
stands. Recommendation: keep `qwen3.6:35b` as the local detector; keep retry-on-empty in the
runner; run the ×3-draw CLEAN characterization before considering qwen3.8:27b for adoption.

## Reproduce

`python3 ollama/run_local_critic.py qwen3.8:27b` (dedicated `:11435`, `:11434` idle). Files:
`qwen3-8-27b/<fixture>.json` (33), blind-cut, retry-on-empty, `attempts` field records retries.
