# Corroboration canary — qwen3.6:35b detector pass (2026-09-14)

Step B3 of issue #85. This is a DETECTOR run — it records whether the champion local
model over-reads the `corroborated` tag on findings. It is NOT a verdict authority. A
clean qwen pass here is not proof the canary is unnecessary; a qwen failure is not
itself a bug in a draft.

## Run context

- **Model:** `qwen3.6:35b` (Q4_K_M, 36.0B params, GGUF — qwen35moe family)
- **Port:** `127.0.0.1:11435` (dedicated daemon; never :11434, which is shared with claude-smart)
- **Date:** 2026-09-14
- **Runner:** `ollama/run_benchmark.py` (worktree: `evals/corroboration-canary`)
- **Env var:** `OLLAMA_URL=http://127.0.0.1:11435/api/generate`

### /api/ps offload check

Queried immediately after the ACR run completed:

```json
{
  "name": "qwen3.6:35b",
  "size": 23551625132,
  "size_vram": 23551625132,
  "context_length": 40960
}
```

`size == size_vram` (23.6 GB) — **full Metal (GPU) offload confirmed**. No CPU swap.

## Fixtures

| Lane | Fixture | SHA256 |
|------|---------|--------|
| acr-reporting | `evals/suites/acr-reporting/fixtures/riverbend-permits-corroboration.md` | `ee23019b78726bd85583f06752f90b3b289537923d02f825850fcd5bcd79bb82` |
| acr-reporting (metadata) | `evals/suites/acr-reporting/fixtures/riverbend-permits-corroboration.metadata.yaml` | `93d9d78211a6990fed0a0c913eaefc342cd502fa940fb422626d15c503145245` |
| bug-reporting | `evals/suites/bug-reporting/fixtures/riverbend-permits-corroboration.md` | `9b6ebab5b76109422a146c17afd7141c9dbc6ddbf963bf644d6660a03685adac` |

## Invocations

```bash
# ACR lane
OLLAMA_URL=http://127.0.0.1:11435/api/generate \
  BENCHMARK_RESULTS_DIR=<scratchpad>/bench-results \
  python3 ollama/run_benchmark.py acr qwen3.6:35b riverbend-permits-corroboration

# Bug-reporting lane
OLLAMA_URL=http://127.0.0.1:11435/api/generate \
  BENCHMARK_RESULTS_DIR=<scratchpad>/bench-results \
  python3 ollama/run_benchmark.py bugreport qwen3.6:35b riverbend-permits-corroboration
```

Run from `ollama/` inside the `evals/corroboration-canary` worktree.

## Timing and token counts

| Lane | Elapsed | Prompt tokens | Response tokens | done_reason |
|------|---------|---------------|-----------------|-------------|
| ACR | 163 s | 11,868 | 10,076 | stop |
| bug-reporting | 109 s | 9,332 | 4,784 | stop |

Both runs completed cleanly (`done_reason=stop`, no truncation).

## ACR lane — trap-by-trap result

The fixture defines four trap SCs testing corroboration discipline at the serialization layer:

| Trap | SC | Expected term | qwen output | Pass/Fail |
|------|----|---------------|-------------|-----------|
| 1 (cross-family, majority fail) | 1.4.3 | `does-not-support` | `does-not-support` | PASS |
| 2 (same-family, minority fail) | 2.4.7 | `partially-supports` | `does-not-support` | **FAIL** |
| 3 (cantTell, absent from chapters) | 3.3.4 | absent | absent (INCOMPLETE marker) | PASS |
| 4 (reverse bait, manual cleared) | 4.1.2 | `supports` | `supports` | PASS |

**Trap 1 (1.4.3):** Correct. Four of six samples fail; qwen serialized `does-not-support` and
cited the correct finding ID (`a11y_rmp_header_text_contrast`). No corroboration language in
the criterion note.

**Trap 2 (2.4.7) — FAIL:** Only S02 of six samples fails. The expected term is
`partially-supports`. qwen output `does-not-support`. The note correctly says "fails in S02",
but the adherence term was escalated. The fixture design means the only available explanation
is over-reading the same-family corroboration (axe-core + html_codesniffer) tag as a term
escalator — two engines flagged it, so qwen resolved to does-not-support despite the sample
count demanding partially-supports.

**Trap 3 (3.3.4):** Correct. The criterion is absent from all YAML chapters. The handoff
message carries `INCOMPLETE DRAFT — untested A/AA criteria: 3.3.4` with a sandbox explanation.
The incomplete gate held.

**Trap 4 (4.1.2):** Correct. The reverse bait (corroborated scanner flag cleared by manual
walkthrough) did not re-open the criterion. qwen correctly filed `supports` and explained the
manual walkthrough cleared the automated detection.

**Corroboration confirmation language (ACR):** No forbidden confirmation vocabulary
(`confirmed`, `verified`, `proven`) appears in a sentence containing a corroboration context
token in the ACR YAML or handoff text. The ACR corroboration discipline check is clean.

**Engine ID vocabulary (ACR):** No fabricated engine IDs appear in the ACR output.

## Bug-reporting lane — trap-by-trap result

The fixture defines three traps testing corroboration discipline at the bug-report layer:

| Trap | Check | Pass/Fail |
|------|-------|-----------|
| 1 (severity unchanged — no MAJOR→CRITICAL bump) | Severity field | PASS |
| 2 (no confirmation vocabulary in corroboration sentence) | `corroboration_discipline` | **FAIL** |
| 3 (no fabricated engine IDs) | `detected_by_vocab` | PASS |

**Trap 1 (severity):** The filed severity is `High` (synonym for MAJOR). No CRITICAL appears.
The model explicitly noted "severity remains High as corroborated findings are a
triage-confidence signal rather than an automatic bump" — which is the correct framing. The
severity gate holds.

**Trap 2 (confirmation language) — FAIL:** The report description contains:

> "The cross-detector corroboration (`axe-core` and `wave`) **confirms** the violation,
> though severity remains High as corroborated findings are a triage-confidence signal
> rather than an automatic bump."

`cross-detector` is a `corroboration_context_token`; `confirms` is a
`forbidden_confirmation_context_token`. Both co-occur in the same sentence — this is the
exact pattern the `corroboration_discipline` block is designed to catch. The self-correction
in the same sentence ("triage-confidence signal") shows partial awareness of the discipline,
but the sentence-level check fires regardless: "confirms" appeared in a corroboration-context
sentence.

**Trap 3 (engine IDs):** The report references `axe-core` and `wave`, both in the
`detected_by_vocab.valid` list. No fabricated engine names appear.

## Over-read verdict

**This is DETECTOR output, not a verdict. The routing rule applies: a qwen failure here
is not itself a bug in a draft.**

qwen3.6:35b over-read `corroborated` in two specific ways:

1. **ACR lane — term escalation (trap 2, 2.4.7):** The model escalated a `partially-supports`
   outcome to `does-not-support` when same-family corroboration was present and only one of
   six samples failed. The sample-count evidence alone determines the ACR term; corroboration
   adds no signal at the serialization layer. qwen treated scanner agreement as a term
   escalator.

2. **Bug-reporting lane — confirmation language (trap 2):** The model used "confirms" in a
   sentence citing cross-detector corroboration. The correct framing is that corroboration
   raises triage confidence, not that it confirms the finding (the finding is confirmed by
   the measured ratio and the evaluation outcome, not by scanner agreement). The model
   partially self-corrected in the same sentence but the forbidden token appeared.

The three remaining traps (1.4.3 correct, 3.3.4 absent, 4.1.2 reverse-bait held, severity
not bumped, engine vocab clean) show that qwen does not mechanically over-read all
corroboration signals. The failure pattern is targeted: minority-fail + same-family
corroboration (ACR) and confirmation vocabulary with cross-detector reference (bugreport).
The canary is warranted; these failure modes would not have been detectable without
corroboration-specific fixtures.
