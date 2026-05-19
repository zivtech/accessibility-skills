---
name: a11y-workflow
description: "Orchestrate the a11y accessibility lifecycle: scout → plan → critique → [perspective audit] → test → critique. Dual-mode: full lifecycle automation or step-by-step dispatch. Spawns specialist agents at depth-1 from the main session."
---

# A11y Workflow Orchestrator

This skill sequences the accessibility lifecycle by spawning specialist agents from the main session. All agents run at depth-1 — no nested delegation.

## When to Use

- `/a11y-workflow full <target>` — run the complete plan-critique-test-critique lifecycle
- `/a11y-workflow step <step-name> <target>` — run a single step, user drives the sequence
- When reviewing or planning accessibility for a component, page, or feature

## Team Roles

| Role | Agent | Model | Job |
|------|-------|-------|-----|
| Scout | `a11y-scout` | haiku | File discovery, ARIA inventory, component type ID |
| Planner | `a11y-planner` | opus | Design accessibility before coding (9-phase) |
| Critic | `a11y-critic` | opus | Review ARIA patterns, focus management, state communication (8-phase) |
| Tester | `a11y-test` skill | n/a | Playwright keyboard tests, axe-core scans |
| Auditor | `perspective-audit` | opus | Deep 7-perspective review on escalated perspectives |

## Context Passing Between Agents

Each agent starts with a fresh context window. The main session bridges context between them:

- **Scout → Planner/Critic**: Scout returns a structured recon summary (~500-1500 chars). Inject verbatim into the next agent's prompt.
- **Planner → Critic**: Planner writes plan to `docs/a11y-plans/YYYY-MM-DD-<feature>-a11y-plan.md`. Critic is spawned with file paths to the plan and source code — it reads both using its Read tool.
- **Critic → Perspective Audit**: Extract only the alarm levels and findings for escalated perspectives (~500-1500 chars). Inject into the perspective-audit prompt.
- **Test → Critic**: Inject structured test results summary (~500-1000 chars) into the critic prompt alongside source file paths.
- **Size budget rule**: Output > 2K chars → write to file, next agent reads. Output ≤ 2K chars → inject into prompt.

## Mode 1 — Full Lifecycle

Invocation: `/a11y-workflow full <target>`

The main session follows these steps sequentially. Do NOT spawn all agents at once — each step's output informs the next.

### Step 1: Scout
```
Agent(subagent_type="a11y-scout", model="haiku", prompt="
  Discover and inventory the accessibility state of: <target>
  Return: file paths, component type, existing ARIA attributes, estimated complexity.
  Keep output under 1500 chars — structured summary only.
")
```

### Step 2: Plan
```
Agent(subagent_type="a11y-planner", model="opus", prompt="
  Design accessibility for the following component.
  Scout recon: <inject scout output>
  Source files: <file paths from scout>
  Write the plan to docs/a11y-plans/YYYY-MM-DD-<feature>-a11y-plan.md
")
```

### Step 3: Critique the Plan
```
Agent(subagent_type="a11y-critic", model="opus", prompt="
  Review this accessibility plan for gaps before implementation.
  Plan file: <path written by planner>
  Source files: <file paths from scout>
  Flag perspective alarm levels (LOW/MEDIUM/HIGH) for each of the 7 perspectives.
")
```

### Step 4: Perspective Audit (conditional)
Only if the critic flags any perspective at MEDIUM or HIGH alarm:
```
Agent(subagent_type="perspective-audit", model="opus", prompt="
  Deep review from escalated perspectives.
  Escalated perspectives and findings: <extract from critic output>
  Source files: <file paths>
")
```

### Step 5: Return to User
Present the plan + critique + perspective audit findings. User revises and implements.

### Step 6: Test (after implementation)
Invoke the `/a11y-test` skill to run Playwright keyboard tests and axe-core scans.

### Step 7: Critique the Implementation
```
Agent(subagent_type="a11y-critic", model="opus", prompt="
  Review this implementation for accessibility design issues.
  Source files: <file paths>
  Test results summary: <inject test output summary>
")
```

### Step 8: Perspective Audit (conditional)
Same as Step 4 — only if critic flags MEDIUM/HIGH alarms.

### Step 9: Return to User
Present implementation critique + perspective audit findings. User fixes and re-tests.

## Mode 2 — Step Dispatcher

Invocation: `/a11y-workflow step <step-name> <target>`

User drives each step manually. The skill spawns the appropriate agent for the requested step.

| Step Name | Agent | Model | What It Does |
|-----------|-------|-------|-------------|
| `scout` | a11y-scout | haiku | Discover files, inventory ARIA state |
| `plan` | a11y-planner | opus | Design accessibility (pass prior recon if available) |
| `critique` | a11y-critic | opus | Review plan or implementation |
| `test` | a11y-test skill | n/a | Run Playwright + axe-core |
| `audit` | perspective-audit | opus | Deep perspective review (specify `--perspectives` to limit) |

### Examples
```
/a11y-workflow step scout src/components/Modal.tsx
/a11y-workflow step plan src/components/Modal.tsx
/a11y-workflow step critique src/components/Modal.tsx
/a11y-workflow step audit src/components/Modal.tsx --perspectives keyboard,cognitive
```

## Triage Mode (Cost-Sensitive)

For cost-sensitive runs, add `--triage` to critique steps:
```
/a11y-workflow step critique --triage src/components/Modal.tsx
```

This spawns the critic at Sonnet first, reads the structured output, and checks escalation signals:
- **CLEAN verdict** (no bugs found) → re-run at Opus (false positive risk)
- **ADVERSARIAL pattern** / ambiguous tradeoff → re-run at Opus (verdict calibration)
- **Low-confidence CRITICAL finding** → re-run at Opus (severity calibration)
- **No verdict emitted** → re-run at Opus (model budget exhausted)

Perspective audit escalation (MEDIUM/HIGH alarm) always runs at Opus regardless of triage mode.

## Benchmark Validation

Phase 1 benchmark (8 hard fixtures via Claude Code subagents, 2025-05-19):

| Tier | FLAWED (5) | ADVERSARIAL (3) | Total |
|------|-----------|----------------|-------|
| Opus | 5/5 PASS | 3/3 PASS (best-tier verdicts) | **8/8** |
| Sonnet-think | inherited from Haiku (pass) | resolved Haiku failures (acceptable verdicts) | 8/8 |
| Haiku | 5/5 PASS | 0/3 (wrong verdicts) | 5/8 |

Opus achieves best-tier verdict quality on every ADVERSARIAL fixture on the first pass. This is the measured basis for Opus-default routing.
