# Eval Harness

There is no standalone harness in this repo. The fixture/rubric suites under
`evals/suites/` are executed by the benchmark runners in `ollama/`:

- `ollama/run_benchmark.py` — local Ollama runs (critic, planner, perspective)
- `ollama/run_cloud_benchmark.py` — hosted Claude / Codex runs with escalation
- `ollama/score_output.py`, `score_perspective.py`, `score_planner.py` — scoring

See `ollama/README.md` for prerequisites and commands, and
`ollama/BENCHMARK.md` for committed results. The original full harness lives
in the upstream `zivtech-meta-skills` monorepo and is not required here.
