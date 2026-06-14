# Local (no-API) chain-eval re-run — qwen3:32b

**Date:** 2026-06-14 · **Model:** qwen3:32b · **Server:** native macOS Ollama on `:11435`
(Metal/GPU, `OLLAMA_HOST=127.0.0.1:11435`) · **Context:** 32768 · **Wall time:** ~47 min for 3 fixtures.

Driver: `ollama/run_chain_local.py` hand-orchestrates planner → critic → (audit if escalated)
through `ollama_a11y.run()`, captures each stage in the I9 pristine format, then `score_chain.py`
scores against the committed rubrics.

> **GPU note (cost the first two attempts):** the runner's default `localhost:11434` is **OrbStack**,
> a Linux container with no Metal access — qwen3:32b ran 100% on CPU there (>3 min for 10 tokens).
> The native macOS Ollama on `:11435` runs `100% GPU` (~25 tok/s). `ollama_a11y.py` now honors
> `OLLAMA_HOST` so a run can target the Metal server explicitly.

## Scorecard

| Fixture | S3 (alarm) | S4 (escalation) | Tracer (found real issue?) | PASS |
|---|---|---|---|---|
| modal-broken-focus-trap | 0.643 | 0 — exp=True act=False | 1 — "focus not moved to modal on open" | False |
| video-tutorial-no-captions | 0.786 | 0 — exp=True act=False | 1 — "missing `<track kind=captions>`" | False |
| login-form-clean | 0.929 | 0 — exp=True act=False | n/a (clean) | False |

## What this validates — PASSED (this lane's purpose)

- **M2 `parse_alarms` on real, non-hand-authored output.** All three critics contained prose
  alarm-like tokens — `Confidence: HIGH` (per-finding confidence) and `Low vision user` (the word
  "Low" inside a perspective label). These are exactly what the **pre-M2** parser mis-bound. M2
  ignored all of them and returned `{}`. First "wild" input it has seen; correct behavior.
- **I9 capture round-trip + scorer integration.** Pristine captures + operator zones written;
  `score_chain.py` produced full S3/S4/S5/tracer verdicts on every capture without crashing.
  `PASS: False` is the scorer *succeeding* — correctly reporting non-escalation.

## Finding — escalation is model-sensitive (real, model-attributable)

The a11y-critic SKILL.md **mandates** a `| Perspective | Alarm Level | Trigger Signal |` table
(`.claude/skills/a11y-critic/SKILL.md:359`), and the runner loads that SKILL.md as the critic
system prompt. qwen3:32b emitted a **prose** `**Multi-Perspective Notes**:` list instead — **3/3**.
No table → no alarm rows → no MEDIUM/HIGH → **escalation never fires** (S4=0 everywhere), even
though qwen3 *did* identify the real defects (Tracer=1 on both non-clean fixtures).

**Control — plan-vs-component confound ruled out (2026-06-14):** re-running the critic on each
fixture's component source directly (no plan framing; same model / SKILL / content) again produced
prose `**Multi-Perspective Notes**:` — `parse_alarms` `{}`, no table, **3/3**. Framing is
irrelevant: **6/6 prose across both runs**. (Reconciles with the committed "qwen3 96% must-find"
critic-fixture score — that measures *detection* of planted issues, which qwen3 does well, not
*emission of the escalation table*, a separate axis the chain is the first to require.) Captures:
`local-qwen3-control/`.

Implication: the chain's escalation gate depends on the critic model reliably emitting the
structured table. This does **not** argue for loosening M2 (that re-admits the prose garbage
above) — it argues for enforcing the table at the critic.

## Caveats (do not over-read)

- **S3 values (0.64–0.93) are not a qwen3 quality signal.** They are a mechanical artifact of the
  all-LOW collapse: genuinely-LOW perspectives match by default (1.0); genuinely-alarming ones
  score 0. login-form-clean scores 0.93 *because* a clean fixture rewards all-LOW.
- **The runner reviews the plan, not the component** (critic input is "PLAN UNDER REVIEW…"), while
  the SKILL is component-oriented. This framing mismatch is a plausible co-contributor to the prose
  drift — but the component-input control (`local-qwen3-control/`) ruled this out: prose 3/3 there too,
  so it is stable qwen3 behavior, not a plan-framing artifact (see Finding -> Control).
- **Not a measure of Claude chain quality.** Per project preference, the production skill benchmark
  uses Claude Code subagents; this lane only exercises the fixed instrument on fresh local output.
- **Does NOT validate I1 staging** (peek-blocking) — moot locally: qwen3 has no filesystem access,
  so every stage is `peek: false` by construction.

## Reproduce

```bash
# native Metal Ollama must be serving on :11435 (qwen3:32b in ~/.ollama store)
OLLAMA_HOST=127.0.0.1:11435 python3 ollama/run_chain_local.py --model qwen3:32b
for f in modal-broken-focus-trap video-tutorial-no-captions login-form-clean; do
  python3 evals/suites/chain/score_chain.py "$f" "evals/suites/chain/local-qwen3/$f"
done
```
