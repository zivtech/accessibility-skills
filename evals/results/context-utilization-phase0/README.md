# Phase 0.4b — live retro-probe of qwen3:32b critic-suite context exposure

**Date:** 2026-08-24
**Task:** Phase 0.4b of `docs/plans/2026-08-24-context-utilization-plan.md` (§3 F6/F7, §6 Phase 0.4 item (b)) — the live `num_predict=1` probe half of the retro-probe, following Phase 0.4a's archive-mining finding (below).
**Model:** `qwen3:32b`
**Server:** Ollama `v0.32.15`, the default GUI-app instance at `http://127.0.0.1:11434` (the dedicated benchmark server on :11435 was NOT started or touched, per task constraints).

## Server identity (receipts: `00-api-version.json`, `00-qwen3-32b-tag-entry.json`, `00-api-tags-full.json`)

- `/api/version`: `{"version": "0.32.15"}`
- `qwen3:32b` digest: `030ee887880fc378860c2dd35101da424377520441ae4bfe7be6deff8ade7840`, size 20,201,253,829 bytes, quantization `Q4_K_M`, declared `context_length: 40960`, capabilities `["completion", "tools", "thinking"]`.

**Version caveat (per task brief, repeated here verbatim in spirit):** token *counts* (`prompt_eval_count`) are tokenizer-determined and robust across server versions — they will not change if Ollama is upgraded, only if the model/tokenizer changes. The *truncation-behavior* observations below (what the server silently does at an undersized `num_ctx`) carry a version caveat: they describe Ollama v0.32.15 specifically. The historical funnel rows this probe is investigating ran on a pinned dedicated instance whose exact version is not re-verified here — this probe establishes what happens on the version available today, not a retroactive guarantee about every historical run's server build.

## Fixture selection

Selected from `evals/suites/a11y-critic/fixtures/` (41 `.md` files total), by raw file byte size:

| Role | Fixture ID | Raw file bytes |
|---|---|---|
| Largest | `multistep-form-error-clearing` | 17,273 |
| Median (21st of 41 sorted) | `tabs-missing-arrow-nav` | 5,363 |
| Smallest | `button-skip-link-clean` | 2,977 |

(Full ranked list is reproducible via `wc -c evals/suites/a11y-critic/fixtures/*.md \| sort -n`.)

## Probe method

Constants and helper logic (`PROMPT_PREFIX`, the answer-key-stripping regex/function, frontmatter-stripping) were **ported verbatim** from git-HEAD snapshots of `ollama/run_benchmark.py` and `ollama/ollama_a11y.py` (commit `d8d2048f0b1e2a38f4a28a55963e54d0d6f2e507`), saved to scratch space rather than importing the live working-tree modules, which another agent was concurrently editing this session. The ported constants/functions were verified byte-identical to the HEAD snapshot programmatically (string/regex equality checks) before use, not just eyeballed.

**System prompt:** `.claude/skills/a11y-critic/SKILL.md` with YAML frontmatter stripped — 60,373 chars. This is stable, read-only source (not touched by the concurrent edit).

**User prompt for each fixture probe:** `PROMPT_PREFIX + strip_answer_key(fixture_content)` — i.e. the exact composition `run_ollama()` sends in production (`run_benchmark.py:363-372`), including the blind-protocol stripping of the fixture's own `## Accessibility Issues (Planted)` answer-key section (`run_benchmark.py:291-301`). All three selected fixtures carry that heading, so blinding materially shrinks what's actually sent — e.g. the largest fixture's 17,273 raw bytes reduce to an 8,818-char blinded body. Using the raw (un-blinded) file would have overstated the true historical prompt size.

**Payload:** `POST /api/generate`, `{"model": "qwen3:32b", "stream": false, "system": <critic prompt>, "prompt": <see above>, "options": {"num_ctx": <N>, "num_predict": 1, "temperature": 0}}`.

### Deviation from the literal probe instruction (system-alone)

The instructed system-alone probe (`"prompt": ""`) does **not** measure the system prompt's token count. Ollama's `/api/generate` treats a truly empty `prompt` as its documented preload-only shortcut: the model loads into memory but no prompt evaluation happens. Observed: `done_reason: "load"`, no `prompt_eval_count`, empty response, ~10s wall time regardless of the 60,373-char system prompt (receipt: `01-system-alone-ctx32768.json`, kept as evidence of this behavior rather than discarded).

**Fix:** re-ran with `"prompt": PROMPT_PREFIX` (121 chars, the real non-empty text every critic run prepends — never a fabricated placeholder) instead of `""`. This measures system + protocol-prefix with zero fixture content, the closest faithful analog to "critic protocol alone" available without inventing prompt text that never appears in production traffic. Receipt: `01b-system-plus-prefix-alone-ctx32768-CORRECTED.json`.

## Results

**Step 2 — true token counts, `num_ctx=32768` (comfortably above every measured count; no overflow risk at this window):**

| Prompt | Raw fixture bytes | Blinded prompt chars | **True prompt tokens (qwen3:32b tokenizer)** | done_reason |
|---|---|---|---|---|
| System + `PROMPT_PREFIX` alone (no fixture) | n/a | 121 | **13,853** | length *(num_predict=1 cap — expected)* |
| Smallest: `button-skip-link-clean` | 2,977 | 2,337 | **14,489** | length |
| Median: `tabs-missing-arrow-nav` | 5,363 | 3,142 | **14,649** | length |
| Largest: `multistep-form-error-clearing` | 17,273 | 8,939 | **16,447** | length |

(`done_reason: "length"` here reflects hitting the `num_predict=1` generation cap, not context overflow — at `num_ctx=32768` every one of these prompts fits with over 16K tokens of headroom to spare. This is confirmed, not assumed: it's the same field used diagnostically at 16384 below, and at 32768 the values move in lockstep with prompt size as expected for a clean fit.)

**Step 3 — the historical config, `num_ctx=16384`, largest fixture, two consecutive identical draws:**

| Fixture | True prompt tokens (from step 2) | num_ctx | **prompt_eval_count draw1** | **prompt_eval_count draw2** | done_reason (both) | response token returned? |
|---|---|---|---|---|---|---|
| `multistep-form-error-clearing` | 16,447 | 16,384 | **8,194** | **8,194** | length | No (`response: ""` both draws) |

Timing (corroborating, not the primary signal): draw1 `total_duration` 47.8s (`prompt_eval_duration` 44.9s, `load_duration` 2.8s — a context-size reallocation from the prior 32768 run); draw2 `total_duration` 0.13s (`prompt_eval_duration` 0.07s, `load_duration` 0.0016s) — a ~365x collapse consistent with a warm KV-prefix cache on the repeat call.

## Arithmetic vs the 16,384 window

- True largest-fixture prompt: **16,447 tokens**. Window: **16,384**. Bare overflow before reserving *any* room for output: **16,447 − 16,384 = 63 tokens (0.4% over).**
- Observed `prompt_eval_count` at 16,384: **8,194 tokens**, identical on both draws.
- Shortfall vs the true prompt: **16,447 − 8,194 = 8,253 tokens never evaluated — 50.2% of the true prompt.**
- That shortfall is **~131× larger** than the 63-token bare overflow. Whatever the server did, it was not "trim the 63 tokens that don't fit" — roughly half the prompt was dropped.
- Numeric note (observed, not explained): 8,194 sits almost exactly at half of `num_ctx` itself (16,384 ÷ 2 = 8,192; observed value is 2 tokens above that). This repo has no source-level visibility into Ollama's truncation algorithm, so this is reported as an empirical correlation, not a confirmed mechanism.
- The result is deterministic, not noisy: both draws — run seconds apart, one cache-cold and one cache-warm — landed on the identical 8,194.

## The `context` field is not usable evidence of what was dropped

A follow-up check (receipt: `04-context-field-comparison.json`, derived from the two receipts above — no extra API call needed) compared the `context` token-array field Ollama returns in both runs. Result: **byte-identical** 16,448-token arrays at both `num_ctx=32768` and `num_ctx=16384`, including the same final generated token id, despite `prompt_eval_count` differing by nearly 2x (16,447 vs 8,194). The `context` field appears to echo the full, untruncated tokenization of system+prompt+response for conversational continuity, independent of whatever the server actually evaluated internally. **A caller checking only `context` length would see no difference and could wrongly conclude nothing was truncated.** `prompt_eval_count` (corroborated by the duration/load-time fields) is the only signal in this API response that exposes the truncation.

This also means the probe **cannot** determine which specific portion of the prompt survived inside the 8,194-token window that was actually evaluated — e.g. whether the critic protocol's instructions (the `system` block) or the fixture content bore the loss, or some mix of both. No evidence collected here speaks to that split either way; it is left open rather than guessed at.

## Plain-language conclusion

At `num_ctx=16,384` — the config `qwen3:32b`'s historical critic-suite rows ran under, per F6/F7 (missing `CRITIC_CTX` map entry → `CRITIC_CTX_DEFAULT`, `run_benchmark.py:340-360`) — the critic system prompt plus the largest fixture in the suite does not fit: the true prompt (16,447 tokens) exceeds the window (16,384) before a single output token is reserved. This is not a hypothetical or a near-miss: measured directly, the server silently evaluated only 8,194 of those 16,447 tokens (49.8%) on both of two identical, reproducible draws, with no error, no warning field, and a normal-looking completion — this is the "silent" in the plan's F7. The shortfall (8,253 tokens, half the prompt) is far larger than the bare 63-token overflow, so whatever the server's internal truncation strategy is, it discards much more than the minimum needed to fit.

This is a **quantified, confirmed overflow finding for the largest fixture specifically** — not a claim about all 41 critic fixtures, which were not all probed. It is, however, directly informative about scope: the system+prefix-alone baseline (13,853 tokens) leaves only 16,384 − 13,853 = **2,531 tokens of headroom** for fixture content before overflow starts. The smallest and median fixtures probed here (14,489 and 14,649 true tokens respectively) both sit comfortably *under* 16,384, meaning their prompts most likely fit without prompt-side truncation at this `num_ctx` — **this is an inference from the step-2 true-token numbers, not a direct `num_ctx=16384` measurement**, since the task scoped the step-3 historical-config probe to the largest fixture only. Combined with the observed ~3.4-3.8 chars/token ratio on these three fixtures, only a raw file size in roughly the same range as the largest fixture (17,273 bytes) would be expected to push a fixture's total prompt over the 16,384 line; by that reasoning only a minority of the 41-fixture suite (candidates by raw size: `app-focus-order-illogical` 14,921B, `dashboard-heading-inconsistency` 14,618B, and `multistep-form-error-clearing` 17,273B are the only three fixtures at or above 14.6KB raw — see the full ranked list in `evals/suites/a11y-critic/fixtures/`) would plausibly be exposed to this truncation on the prompt side, which is consistent with — and gives a concrete, size-gated explanation for — F7's observation that qwen3:32b's historical aggregate scores (65-68/68) stayed high despite the missing `CRITIC_CTX` entry: most fixtures likely never overflowed the window in the first place, and the exposure is not fleet-wide but concentrated in the largest few fixtures. This paragraph is an interpretation built on the measured numbers above, flagged as such — it is not a claim that any specific historical row (as opposed to this fresh, direct probe) was or wasn't truncated, since historical rows predate `prompt_eval_count`/`done_reason` recording entirely (see below) and the exact historical server version/config is not re-verified here.

**What this finding does NOT establish:** the split between system-prompt loss and fixture-content loss within the truncated window (see above); the truncation ratio for fixtures other than the largest (not directly probed at 16384); whether production runs (streaming, `temperature=0.3`, unrestricted `num_predict`, real "thinking" generation) behave identically to these `num_predict=1` diagnostic probes — production output generation would consume additional context budget these probes never touch, which this analysis does not attempt to quantify; and nothing here bears on `qwen3.6`/`gemma4`/other tokenizers, which have their own already-mapped `CRITIC_CTX` entries and are out of this probe's scope.

## Pointer: committed historical artifacts cannot answer this question

Phase 0.4a (Explore/haiku subagent, 2026-08-24, executed early — see `docs/plans/2026-08-24-context-utilization-plan.md` §3 F7 and the critic-review disposition table in `docs/plans/2026-08-24-context-utilization-plan-critic-review.md`) mined the committed response JSONs under `evals/results/` and found that the three critic-suite eras — `evals/results/ollama-blind/`, `evals/results/ollama-dehinted/`, `evals/results/ollama-rebaseline/` (174 committed qwen3:32b response files total, 58 per era, confirmed by direct count in this session) — **record no `prompt_eval_count` field at all**; the field only appears in Ollama's response payload starting with the July-August 2026 lanes. This is exactly why this live probe (Phase 0.4b) was the required path rather than a re-mining pass: the historical question ("was qwen3:32b's critic suite actually truncated at 16,384?") is structurally unanswerable from the committed artifacts alone. This probe answers the *mechanism* question directly (yes, the server truncates silently and severely once the prompt exceeds the window) on today's server version; it does not and cannot retroactively recover what happened token-for-token on the original historical runs, whose exact server build is not re-verified here.

## Receipts in this directory

| File | Contents |
|---|---|
| `00-api-version.json` | `/api/version` response |
| `00-api-tags-full.json` | Full `/api/tags` listing (all locally installed models) |
| `00-qwen3-32b-tag-entry.json` | Just the `qwen3:32b` entry from tags |
| `00-fixture-selection.json` | Selected fixture IDs, raw bytes, blinded content/prompt char counts |
| `01-system-alone-ctx32768.json` | The empty-`prompt` probe that hit Ollama's preload-only shortcut (kept as evidence of the deviation, not discarded) |
| `01b-system-plus-prefix-alone-ctx32768-CORRECTED.json` | The corrected system+prefix-alone probe (13,853 true tokens) |
| `02-largest-multistep-form-error-clearing-ctx32768.json` | True-count probe, largest fixture (16,447 tokens) — includes raw `context` token array |
| `02-median-tabs-missing-arrow-nav-ctx32768.json` | True-count probe, median fixture (14,649 tokens) |
| `02-smallest-button-skip-link-clean-ctx32768.json` | True-count probe, smallest fixture (14,489 tokens) |
| `03-multistep-form-error-clearing-ctx16384-draw1.json` | Historical-config draw 1 (8,194 tokens evaluated) — includes raw `context` token array |
| `03-multistep-form-error-clearing-ctx16384-draw2.json` | Historical-config draw 2 (8,194 tokens evaluated, cache-warm timing) |
| `04-context-field-comparison.json` | Derived analysis: `context` array comparison across the two runs above |
| `99-summary.json` | Machine-readable summary written by the probe script at the end of its primary run (predates the `01b` correction and the `04` follow-up, both captured separately above) |

## Hygiene

All fixture IDs and model tags referenced above are the repo's existing de-identified names (e.g. `multistep-form-error-clearing`, `qwen3:32b`) — no client names appear anywhere in this directory, consistent with the rest of `evals/results/`.

> Note (2026-08-24, post-capture): the raw `context` token-id arrays were stripped from the response receipts to keep them lean (context-utilization plan, principle 1); each file retains `context_length` + `context_sha256`. The byte-identical-across-configs evidence survives as identical hashes on the 02-largest/03-draw1/03-draw2 receipts.
