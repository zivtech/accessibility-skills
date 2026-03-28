# AGENTS.md — a11y-meta-skills

| Agent | Type | Command | Companion |
|-------|------|---------|-----------|
| a11y-planner | planner | `/a11y-planner` | a11y-critic |
| a11y-critic | critic | `/a11y-critic` | a11y-planner |

## Lifecycle

The critic serves at **two checkpoints**:

```
plan → critique plan → revise → implement → test → critique implementation → fix → re-test
```

- `a11y-planner` is the pre-implementation design surface (step 1).
- `a11y-critic` reviews the plan for gaps (step 2) and the implementation after testing (step 6).
- Both agents are shipped from this repository.
