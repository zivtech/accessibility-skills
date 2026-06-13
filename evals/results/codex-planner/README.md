# Codex planner lane — raw artifacts (plan 010)

- Run date: 2026-06-12; mechanism: OpenAI Codex CLI (`codex-cli 0.125.0`), model
  **gpt-5.5 effort=low** (tier `5.5-low`), one `codex exec` call per fixture
  (25 total), via `python3 ollama/run_cloud_benchmark.py codex-planner-all 5.5-low`.
- Operator approval: Alex, 2026-06-12, in-session (recorded step-5 "go").
- Tier note: plan 010's default tier `5.2-low` is rejected account-wide on
  ChatGPT-account Codex ("The 'gpt-5.2' model is not supported when using Codex
  with a ChatGPT account"); the CLI default `gpt-5.3-codex` is likewise rejected.
  This lane ran `5.5-low` — same family, low effort, mirroring the critic lane's
  full-pass-tier philosophy. Numbers are not tier-comparable to the historical
  GPT-5.2 critic rows.
- Shape: runner-compatible response JSONs (`response` + `_benchmark` provenance);
  score with `python3 ollama/run_cloud_benchmark.py score-codex-planner` (or per
  file: `python3 ollama/score_planner.py <json> evals/suites/a11y-planner/fixtures/<id>.metadata.yaml`).
- Result: **234/235 must-have hits (99.6%), 25/25 PASS**, zero scorer fallback
  warnings — identical to the Claude Opus subagent lane, including the same single
  keyword-phrasing miss on `aria-combobox-autocomplete`. Per-fixture wall-clock
  47.7s–170.9s (no 300s timeouts). Published section: `ollama/BENCHMARK.md` →
  "Codex planner lane".
