# Parallel Subagent Review - 2026-05-28

## Purpose

Capture the parallel review feedback used to harden the Drupal accessibility evaluation plan, ledger, and packet template.

## Agents Used

| Agent | Role | Focus | Integrated changes |
|---|---|---|---|
| Franklin | `a11y-planner` | Parallel work model and accessibility evaluation workflow | Added ownership rules, environment locks, batch-size caps, main-agent ledger ownership, and saved report convention. |
| Heisenberg | `explorer` | Internal consistency across plan, support plan, and ledger | Corrected wave placement for `HAVEN-003` and `DRUPAL-A11Y-008`, linked the canonical parallel model, and removed older status vocabulary. |
| Averroes | `a11y-critic` | Evidence standards and drift risks | Split source status from local evaluation status, added canonical status enum, expanded ledger metadata, and required global environment preflight before test waves. |
| `talk-to-drupal` | Drupal core philosophy lens | Site-builder, project-stewardship, and content-modeling fit | Added Drupal Core Philosophy Gate and saved the review under `/Users/AlexUA_1/Codex/drupal-core-reviews/`. |

## Main Integration Decisions

- `STATUS.md` is the canonical scheduler and ownership ledger.
- Subagents may draft packets, research source provenance, or review evidence, but the main agent owns final status changes and shared planning docs.
- Source status describes upstream/source claims; local status describes the evidence state in this repo.
- `VERIFIED` requires baseline evidence, patch hygiene, after-patch evidence, broad regression classification, and explicit manual verification status.
- Global environment failures must be recorded as global blockers, not copied into every item as item-specific test-state failures.
- Subagent reports should be saved under `docs/drupal-patch-evaluations/reports/{wave}/{item}-{run-id}.md`.
- `VERIFIED` is reserved for completed required manual checks, not merely explicit manual debt.
- Drupal-core fit is a separate filing gate: site-builder value, maintainer actionability, content-modeling blast radius, release safety, and backward compatibility must be checked before upstream-ready packets are filed.

## Follow-Up Checks

- Run environment preflight before launching any test wave.
- Assign one owner, run ID, and report path per row before parallel work starts.
- Run `a11y-critic` on every packet recommended as `VERIFIED` or upstream-ready.
- Escalate to `perspective-audit` for voice-control, screen-reader, forced-colors, magnification/reflow, or error-recovery-sensitive changes.
