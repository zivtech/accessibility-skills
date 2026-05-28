# Runtime Preflight Critic - 2026-05-28

## Scope

Critic pass on the evaluation ledger after the first runtime preflight attempts.

## Verdict

Keep the global runtime state separate from item-level conclusions. A global DDEV or Drupal setup blocker is not evidence that every item is `TEST STATE BLOCKED`.

## Findings

1. Do not bulk-update item rows from global runtime failure.
   - Item rows should remain `NOT STARTED` until a per-item baseline, patch hygiene, or evaluator attempt happens.
   - Exception: `DRUPAL-A11Y-007-messages-landmark-role` already has an item-specific packet, so its local `TEST STATE BLOCKED` status can remain.

2. Do not reuse stale patch-hygiene summaries as current evidence.
   - Old May 2026 reports can guide where to look, but current raw patches and current target files must be checked before declaring `PATCH HYGIENE BLOCKED`.

3. Do not launch test-wave subagents until the runtime target is settled.
   - Read-only source/provenance work is safe in parallel.
   - Before/after scan workers require an installed Drupal site, deterministic fixture state, and isolated DDEV/worktree ownership.

4. Ledger updates should name the blocker and one next action.
   - Good: "DDEV starts, Drush works, HTTP redirects to install.php; choose/install evaluator checkout."
   - Bad: "Environment broken" with no concrete next step.

## Integrated Changes

- Global preflight remains the only place for broad runtime readiness.
- Item rows stay source-triage-only unless item-specific evidence exists.
- `VERIFIED` remains unavailable until automated and required manual checks are complete.

## Next Action

Settle the evaluator runtime: determine whether Mike Gifford's `mgifford/drupal-core` checkout should become the DDEV project, then install the required fixture modules and run the evaluator against that environment.
