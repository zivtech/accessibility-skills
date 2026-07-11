# A11y Workflow Team

Orchestrated accessibility lifecycle using Claude Code subagents at depth-1.

## Roles

| Role | Agent | Model | Tools | Job |
|------|-------|-------|-------|-----|
| **Orchestrator** | `/a11y-workflow` skill | main session | all | Sequence lifecycle, spawn specialists, manage escalation |
| **Scout** | `a11y-scout` | haiku | read-only | File discovery, ARIA inventory, component type ID |
| **Planner** | `a11y-planner` | opus | no Bash | Design accessibility before coding (9-phase) |
| **Critic** | `a11y-critic` | opus | read-only | Review ARIA patterns, focus management, state communication (8-phase) |
| **Tester** | `a11y-test` skill | n/a | Playwright / keyboard-a11y-tester / virtual-screen-reader | Keyboard tests, axe-core scans, live-URL journey audits, component SR assertions |
| **Auditor** | `perspective-audit` | opus | read-only | Deep 7-perspective review on escalated perspectives |

## Architecture

The orchestrator is a **skill** (not an agent) that runs in the main session. This keeps all agent spawns at depth-1, respecting the "no nested delegation" rule (92% error rate on depth-2+).

### Context Passing

- Scout output (< 2K chars): injected into next agent's prompt
- Planner output (8-11K chars): written to `docs/a11y-plans/` file, critic reads via Read tool
- Critic alarm levels (< 2K chars): injected into perspective-audit prompt
- Test results (< 2K chars): injected into critic prompt
- keyboard-a11y-tester artifacts (trace/findings/census, > 2K): passed as file paths; critic Phase 0 reads them with its calibration rules. The main session drives the serve/step loop itself (CLI, not an agent) — depth-1 holds.
- virtual-screen-reader results (spoken-phrase log slices, < 2K): injected directly into the critic prompt with tool version + test file path; critic Phase 0 carries the consumption rules.

### Escalation Signals (Benchmark-Derived)

These signals trigger promotion to a higher tier (in `--triage` mode) or perspective-audit invocation:

| Signal | Action | Source |
|--------|--------|--------|
| CLEAN verdict (no bugs) | Re-run at Opus | Haiku 1/4 FP on CLEAN |
| ADVERSARIAL pattern | Re-run at Opus | Haiku 0/3 on ADVERSARIAL |
| Low-confidence CRITICAL | Re-run at Opus | Severity calibration gap |
| No verdict emitted | Re-run at next tier | Budget exhaustion |
| Perspective alarm MEDIUM/HIGH | Invoke perspective-audit | Always Opus |

## Workflows

### Full Lifecycle (New Component)
```
/a11y-workflow full src/components/Modal.tsx
```
1. Scout discovers files, inventories ARIA state
2. Planner designs accessibility (writes plan file)
3. [Optional] Script generation: when the planner's output includes specific test scenarios without existing .spec.js coverage, use `/webwright:craft` (reusable) or `/webwright:run` (one-shot) to generate Python Playwright test scripts. The operator must review generated scripts before treating them as test evidence.
4. Critic reviews the plan (reads plan + source files)
5. [If MEDIUM/HIGH alarm] Perspective audit on escalated perspectives
6. User revises and implements
7. Test runs automated scans — `.spec.js` + axe for components (+ virtual-screen-reader announcement/reading-order assertions when live regions or SR output are in play); a keyboard-a11y-tester journey audit (batch recon, then a driven session) for live-URL targets
8. Critic reviews implementation
9. [If MEDIUM/HIGH alarm] Perspective audit
10. User fixes

### Step-by-Step (User-Driven)
```
/a11y-workflow step scout src/components/Modal.tsx
/a11y-workflow step plan src/components/Modal.tsx
/a11y-workflow step critique src/components/Modal.tsx
/a11y-workflow step audit src/components/Modal.tsx --perspectives keyboard,cognitive
```

### Cost-Sensitive (Triage Mode)
```
/a11y-workflow step critique --triage src/components/Modal.tsx
```
Runs critic at Sonnet first, escalates to Opus on signals.

## Benchmark Basis

Model routing validated on 8 hard fixtures (5 FLAWED + 3 ADVERSARIAL) via Claude Code subagents (2026-05-19):

| Tier | FLAWED (5) | ADVERSARIAL (3) | Quality |
|------|-----------|----------------|---------|
| Opus | 5/5 PASS | 3/3 PASS | Best-tier verdicts on all |
| Sonnet | 5/5 (inherited) | 3/3 (resolved Haiku) | Acceptable verdicts |
| Haiku | 5/5 PASS | 0/3 FAIL | Detection OK, judgment fails |
