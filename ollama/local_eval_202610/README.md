# Local receipt runner — explicit standalone condition

Fresh freezes default to `critic-standalone-v2-202610`. Its concise source-only
critic prompt, four reviewed CLEAN controls and advancement rules are documented
in [the condition](../../evals/conditions/critic-standalone-v2/README.md).
Actual HEAD and all source/prompt hashes are captured. The original October
condition is sealed; its snapshots and receipts are preserved as history.
No runtime is started, stopped, or downloaded by this CLI.

```sh
python3 -m ollama.local_eval_202610 freeze --condition critic-standalone-v2-202610 --out evals/results/NEW-COHORT
python3 -m ollama.local_eval_202610 verify-files --out evals/results/local-models-2026-10/receipts-v3
python3 -m ollama.local_eval_202610 run --out evals/results/NEW-COHORT --model ACTUAL_TAG --stage screen --backend ollama --url http://127.0.0.1:11435
python3 -m ollama.local_eval_202610 summary --out evals/results/NEW-COHORT
python3 -m unittest ollama.test_local_eval_202610 ollama.test_critic_standalone_condition -q
```

`verify-files` checks immutable frozen-byte integrity only and returns
`resume_authorized: false`. `run`/`summary` also require current source HEAD,
scorers, adapter modules, condition and fixture inputs to match the freeze.
Do not reuse old output roots for a new condition. No inference is launched by
freezing or verifying files.

These examples are execution instructions, not evidence that any model was run.
The operator qualifies local runtime/cloud-disable/headroom before executing
scored lanes. The shared runtime defaults to `http://127.0.0.1:11434`; override
with `--shared-url` only for a reviewed equivalent setup. The dedicated and
shared base URLs must differ, and both must be loopback HTTP addresses.

The repaired freeze contains ten SCREEN fixtures, four reviewed CLEAN controls,
and seven established bug-report fixtures; Riverbend corroboration is excluded.
It stores fixture source and metadata, companion rubrics from their actual
rubrics directory, selected condition files, scorer/guard sources, baseline-ID
manifest, supplemental executable modules, rendered system/user prompts and hashes.
Only rendered system/user strings enter model requests. Metadata, filenames,
fixture IDs and answer keys remain in receipts. The critic uses the standalone
system rather than the full orchestration skill; bug reports retain their own
skill. No previous chat context/history is supplied. Original code identifiers
remain: title/feature removal is not complete semantic blindness.

Common options are frozen: temperature `0.3`, context `32768`, output budget
`16384`, output/thinking reserve `8192`, default reasoning mode, no seed. A
different output budget requires `freeze --num-predict N` into a fresh output
directory and the same `run --num-predict N` for every comparable model.
Changing context or reasoning condition requires a separate reviewed lane.
Every cell uses the existing conservative context estimate, a same-server
declared ceiling, and a recorded one-token prompt probe. The probe must emit
actual prompt token count within the reserve guard. Its deliberate one-token
length finish is retained and does not qualify as a scored answer. Ollama's
own residency metadata must demonstrate full offload before scored generation
and throughout the scored receipt. Missing/partial residency evidence fails
closed at scored admission, during every sample, and after the stream. The
one-token cold probe may initially observe a valid empty own `models` list
before loading; it must end with full offload and may not lose own residency
after first observing the loaded model. Malformed or absent shared/own
`models` lists never establish idleness or offload. No silent truncation or guessed ceiling is allowed.

Ollama uses `/api/generate` with native system/user separation, streaming,
`keep_alive: "15m"`, and explicit options. Identity comes from that server's
`/api/version`, `/api/tags`, and `/api/show`, preserving digest, template,
parameters, capabilities and model metadata. Identity and options must match
exactly to resume a completed cell.

For a vendor-supported OpenAI-compatible local backend, use `--backend openai`
and a qualified `--identity-file FILE.json`. The base URL excludes the `/v1`
suffix. Requests use `/v1/chat/completions`, stateless system/user messages,
streamed usage, and the same temperature/output budget. Context is the
qualified server configuration recorded in the identity; OpenAI chat requests
do not set a nonstandard context parameter. The identity JSON must contain:

```json
{
  "model": "exact --model value",
  "url": "http://127.0.0.1:8080",
  "digest": "verified model digest",
  "quantization": "actual quantization",
  "runtime": "vendor-supported runtime",
  "version": "actual version",
  "template": "actual native template or its verified artifact reference",
  "reasoning_mode": "runtime default",
  "declared_context_length": 32768,
  "full_offload": true,
  "loader": "actual qualified loader"
}
```

This file is operator qualification evidence, not an automatic MLX memory
measurement. Preserve its supporting measurements separately; backend memory
metadata differs from Ollama. Missing emitted `usage.prompt_tokens` makes the
probe INVALID. Backend differences preclude direct speed comparisons.

Admission checks shared idleness immediately before each probe and attempt.
Shared and own residency snapshots are captured before, during (at intervals
of at least five seconds), and after streams. Shared occupancy or another
model on the dedicated server invalidates a receipt. Busy admission produces
a BLOCKED receipt and stops the run; retry later when idle. Other tasks are
never unloaded. A total 1800-second deadline bounds each probe/attempt and
captures any partial stream and exception. A failed own connection may be
cancelled, without manipulating runtime model residency.
The streaming socket may wait through the remaining attempt deadline, including
initial prompt processing; short metadata calls keep their separate bound.
The first native control lane exposed an erroneous ten-second socket cap and
was stopped. Its INVALID probe receipts remain preserved; `receipts-v2` uses
the corrected transport with unchanged rendered model prompts and limits.

Each raw NDJSON receipt includes the request, exact streamed lines, reasoning,
residency and final outcome/exception. Final cells retain the probe, all
attempt records/hashes, assembled answer/thinking, final termination metadata,
timings/token counts when emitted, and unchanged descriptive scorer output.
Completed cells have hashes and may resume only after identity, options,
prompt and receipt checks. Partial existing receipts refuse overwrite; retain
them and use a fresh output directory for a reviewed restart. An interrupted
cell is not silently retried. `progress.json` is an atomic mutable ledger;
freeze, attempts, completed cells and BLOCKED receipts are immutable.

At most three scored attempts are allowed, exclusively when a final `stop`
answer is empty. Exceptions, length finishes, missing final termination,
unclosed thinking, missing/ambiguous verdict and contamination receive zero
detection credit and are not retried. Critic execution requires one explicit
`Verdict:` line (Markdown bold/headings accepted); keywords elsewhere do not
qualify. Bug reports have no canonical Verdict field, so completed report
structure qualifies execution: every emitted report block must contain all
seven nonempty required label values and a nonempty HTML fence/snippet or an
explicit honest absence for HTML. A title, empty label shell, or partially
structured second report cannot qualify. Honest unavailable field values can
qualify structure; expected report count, exact values, IDs, citations and
fabrication remain correctness dimensions. The existing bug-report scorer retains
its independent PASS/WARN/FAIL and fabrication checks. Execution eligibility
does not assert task correctness or substantive review completeness.

Summary partitions strict ACCEPT, reservations, REVISE/REJECT and unparseable
answers; first-attempt versus retry-assisted completion stays separate.
Per-stage planned denominators include missing and invalid outcomes as zero
numerators. CLEAN draw1 reuses the four matching SCREEN cells; three draws
remain correlated within each fixture. The scorer's apparent findings are
distinct from adjudicated fabrication, which stays unset until review.

The operator must enforce stage gates: the control needs all ten eligible
SCREEN answers before comparison; manually adjudicate nonanswers, apparent
misses and every CLEAN finding. A reservations verdict does not automatically
mean a false positive, and a valid Verdict does not establish a substantive
answer. Advancement requires the plan's must-find/control, nonexecution and
correct-CLEAN conditions plus review; the CLI never promotes a candidate
automatically. Freeze/resume checks and mocked tests do not demonstrate GPU
capacity, runtime qualification, real model capability or production readiness.
The unchanged SCREEN scorer has 15 legacy must-find expectations. Pre-output
review found optional patterns, duplicate defects and missing-context assumptions
among them. Manual advancement uses the plan's fixed five code-grounded findings
(two form, one toast and two tooltip findings), requiring at least four hits.
The descriptive summary retains the legacy scorer denominator of 15; it is not
the adjudicated advancement score. Actual findings on other fixtures remain
reviewable even when they conflict with an answer-key assertion.
