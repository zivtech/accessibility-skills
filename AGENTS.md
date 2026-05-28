# AGENTS.md — a11y-meta-skills

| Agent | Type | Command | Companion |
|-------|------|---------|-----------|
| a11y-planner | planner | `/a11y-planner` | a11y-critic |
| a11y-critic | critic | `/a11y-critic` | a11y-planner, a11y-test |
| a11y-test | tester | `/a11y-test` | a11y-critic |
| perspective-audit | auditor | `/perspective-audit` | a11y-planner, a11y-critic |

## Lifecycle

The critic serves at **two checkpoints**, with optional perspective-audit escalation at each:

```
plan → critique plan → [perspective audit] → revise → implement → test → critique implementation → [perspective audit] → fix → re-test
```

- `a11y-planner` is the pre-implementation design surface (step 1).
- `a11y-critic` reviews the plan for gaps (step 2) and the implementation after testing (step 6).
- `perspective-audit` provides deep review from 7 access perspectives when escalated by the planner or critic (steps 2b and 6b).
- `a11y-test` runs automated Playwright keyboard tests and axe-core scans (step 5).
- All four skills are shipped from this repository.

## Benchmark Team Agents

Agents for running, scoring, documenting, and maintaining the eval suite.

| Agent | Type | Model | Tools | Job |
|-------|------|-------|-------|-----|
| bench-runner | executor | sonnet | Bash, Read | Execute benchmarks (Claude API, Codex/OpenAI, Ollama, Gemini/other hosted adapters when present), run scoring scripts |
| bench-reporter | writer | sonnet | all | Update BENCHMARK.md, README.md, EVAL-GAPS-PLAN.md with results |
| bench-reviewer | reviewer | sonnet | read-only | Audit fixture/rubric quality, verify scoring accuracy |
| fixture-builder | builder | sonnet | all | Create/enrich fixture triplets (.md, .metadata.yaml, .rubric.yaml) |

See `.claude/teams/README.md` for team workflows.
