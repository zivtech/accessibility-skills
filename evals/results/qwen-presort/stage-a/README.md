# Stage-A hosted-judge A/B — run on your desktop (subscription, no $)

This measures whether qwen's candidate leads let the hosted a11y-critic do
**less real work at equal detection** (M0 value-add + M1 token delta). The
judge runs via `claude -p` on your **claude.ai subscription** — no metered API
spend.

## Why you run it (not this session)

Nested `claude -p` inside a Claude Code session hangs, and this repo's shell
env has `ANTHROPIC_API_KEY` set (that path is metered $). The runner
`env -u ANTHROPIC_API_KEY`s each call so it uses your subscription login — but
that only takes effect in a normal terminal where you're logged into claude.ai.

## Steps

1. **Candidates** (already generated locally, committed under
   `evals/results/qwen-presort/<fixture>-qwen3.6-35b.json`). To regenerate or
   add fixtures, with a dedicated Ollama on `:11435`:
   ```
   OLLAMA_HOST=127.0.0.1:11435 ollama serve &
   python3 ollama/presort_candidates.py <fixture-id> --model qwen3.6:35b --port 11435
   ```

2. **Run the A/B** (pilot set is the default; pass fixture ids to override):
   ```
   # sanity-check the plan first — no model calls:
   DRY_RUN=1 bash ollama/run_stage_a_judge.sh

   # real run on your subscription:
   bash ollama/run_stage_a_judge.sh
   ```
   Writes `evals/results/qwen-presort/stage-a/<fixture>--<arm>--opus.json`, each
   carrying the critic's findings (`result`) and token `usage`.

3. **Score** (next step, once outputs exist): extract each arm's `result`, run
   it through the critic scorer against the fixture's `must_find` items to get
   per-arm recall, then diff the arms:
   - **M0 value-add** = must-finds the *with-cands* arm confirms that the *blind*
     arm missed, minus any the *with-cands* arm now misses. ~0 → kill.
   - **M1** = token/cost delta (blind vs with-cands) from the `usage` fields,
     dollar-weighted via `cost_usd()` once `PRICES` is verified.
   - **M3 (anchoring)** first look on the CLEAN fixtures: does *with-cands*
     confirm a non-bug the *blind* arm did not?

## Pilot set (default)

`accordion-no-region-role` (name-role-state), `app-focus-order-illogical`
(focus-order), `async-retry-error-unannounced` (live-region),
`async-retry-recovery-clean` + `button-skip-link-clean` (CLEAN),
`trail-conditions-filter` (mixed). Spans classes + 2 clean for a first M3 read.

Not a decision on its own — the pilot is a signal; the full go/no-go uses the
draw counts and per-item M3 in the design doc.
