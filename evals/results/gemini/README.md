# Gemini critic baseline — raw artifacts (plan 007)

- Run date: 2026-06-12; transport: authenticated `gemini` CLI v0.46.0 (plan 007 amendment) via `python3 ollama/run_cloud_benchmark.py gemini-escalate`, isolated per-call (neutral cwd, `--skip-trust`, `--approval-mode default`, headless no-file-writes preamble).
- Contents: 33 `*-flash-response.json` (Gemini 2.5 Flash, full critic suite) + 2 `*-pro-response.json` error placeholders (pro escalation attempts capacity-blocked at run time; resumable via `gemini-escalate` after quota reset).
- Score with `python3 ollama/score_output.py <json> evals/suites/a11y-critic/fixtures/<id>.metadata.yaml`; published section: `ollama/BENCHMARK.md` → "Gemini baseline"; per-call token counts in each `_benchmark` block.
