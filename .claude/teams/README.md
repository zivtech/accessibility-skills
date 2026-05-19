# A11y Benchmark Team

Default team structure for the a11y-meta-skills eval suite.

## Roles

| Role | Agent | Model | Tools | Job |
|------|-------|-------|-------|-----|
| **Lead** | (you) | opus | all | Orchestrate, decide, commit |
| **Runner** | bench-runner | sonnet | Bash, Read | Execute benchmarks, run scoring scripts |
| **Reporter** | bench-reporter | sonnet | all | Update BENCHMARK.md, README.md, EVAL-GAPS-PLAN.md |
| **Reviewer** | bench-reviewer | sonnet | read-only | Review fixture/rubric quality, verify results |
| **Builder** | fixture-builder | sonnet | all | Create/enrich fixture triplets |

## Workflows

### Full Benchmark Cycle
1. Lead creates team and tasks
2. Runner executes benchmark (e.g., `claude-escalate`)
3. Runner scores results and reports summary
4. Reporter updates documentation with results
5. Reviewer spot-checks a sample of results and fixtures
6. Lead commits and pushes

### Fixture Development
1. Lead creates team and tasks
2. Builder creates fixture triplets
3. Reviewer reviews fixtures for quality
4. Runner benchmarks new fixtures
5. Reporter updates documentation
6. Lead commits and pushes

### Eval Suite Audit
1. Lead creates team and tasks
2. Reviewer audits fixture consistency, rubric quality, scoring accuracy
3. Builder fixes issues found by reviewer
4. Runner re-benchmarks affected fixtures
5. Reporter updates documentation
6. Lead commits and pushes

## Quick Start

From Claude Code, say:
```
Create the a11y-bench team and run a full benchmark cycle on Claude Haiku
```

Or for fixture work:
```
Create the a11y-bench team and build 5 new HAS-BUGS critic fixtures
```
