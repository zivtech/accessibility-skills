> Historical initial-harness evidence. The repaired standalone-v2 condition and
> current checks are documented in `evals/results/benchmark-repair-2026-10-09/`.
> The coverage numbers below predate that repair and are not current coverage.

# Offline verification, 2026-10-08

Later native preflight exposed a ten-second streaming socket timeout shorter
than normal prompt processing. The lead added a regression that failed against
that cap, changed streaming I/O to use the remaining total attempt deadline,
and reran all 27 supplemental tests successfully. The bounded global deadline
test still passes. The earlier traced coverage below predates this one-line
transport correction. Native INVALID probes are retained in `receipts`; a
fresh `receipts-v2` freezes corrected executable bytes and identical model
prompt/options hashes. No capability credit comes from the failed probes.

Execution checkout: `/Users/AlexUA_1/claude/accessibility-skills-local-model-eval-2026-10-08`
at `3ffc2cca364456d09e4daca31f54623b02fe9d93`, branch
`codex/local-model-eval-2026-10-08`. Only supplemental runner files and its
new test module were changed by this worker. Concurrent `.gitignore`, plan
and results work was preserved. No commits, runtime/model calls, GPU
generation, downloads or hosted calls occurred.

`python3 -m unittest ollama.test_local_eval_202610 -q`: **PASS, 26 tests**.
Tests use temporary receipt directories and mocked transport streams. They
cover frozen real source prompts, neutral headings, answer/features cuts,
wrong-source rejection, tampering/overwrite/resume, stateless payloads,
same-server identity, context/offload probe admission, strict verdict parsing,
clipping/errors/empty retries, reasoning/usage streams, missing final
termination, deadlines, contamination, blocked admission, complete mocked
SCREEN/CLEAN stages and correlated-draw denominators. Existing scorer text
and its independent fabrication status remain retained.

The bounded repair added eight test methods before their associated fixes.
The initial six regression methods plus the corrected historical title-only
expectation exposed **20 assertion failures and 4 malformed-snapshot errors**
against the original implementation. A later inline honest-absence regression
failed before its focused parser adjustment. These are retained as development
evidence, not model attempts or runtime failures.

Regressions now reject title-only reports, three-label shells, empty required
values, empty HTML fences, and an incomplete second report. They accept
canonical fields/snippets and sparse honest absence without equating structure
with correctness. Shared/own malformed occupancy fails closed, and current
scored admission, every sample and after-stream evidence must show full own
offload. Valid cold probe loading remains admitted. Stream-monitoring failure
preserves raw exception/outcome receipts. Every supplemental Python module is
frozen byte-for-byte; simulated live edits refuse verify, run and summary before
runtime identity calls. Historical scorers and source HEAD guard are unchanged.

Targeted existing tests:

```sh
python3 -m unittest ollama.test_blind_prompts ollama.test_context_guard ollama.test_score_output_contracts ollama.test_baseline_id_checks -q
```

**PASS, 50 tests.** Existing context-guard test diagnostics and one pre-existing
unclosed-file ResourceWarning appeared; the test command exited zero.

`coverage` is not installed in the available Python 3.13 environment. No
dependency was installed. Stdlib `trace.Trace(count=True, trace=False)` ran
test discovery and all new tests under tracing; executable line sets came
from `trace._find_executable_linenos`. This is line coverage, not branch
coverage or runtime qualification:

| File | Executed / executable lines | Coverage |
|---|---:|---:|
| `__init__.py` | 0 / 1 | 0.0% (module docstring) |
| `__main__.py` | 30 / 33 | 90.9% |
| `freeze.py` | 95 / 104 | 91.3% |
| `runner.py` | 281 / 310 | 90.6% |
| `transport.py` | 168 / 187 | 89.8% |
| **Total** | **574 / 635** | **90.4%** |

`git diff --check` exited zero for tracked work. New-file whitespace was
also checked separately. No model capability, loader support, prompt-probe
success, full-offload measurement or GPU capacity is established by these
offline checks. A fresh independent protocol/implementation review and real
runtime qualification remain required before scored control execution.
