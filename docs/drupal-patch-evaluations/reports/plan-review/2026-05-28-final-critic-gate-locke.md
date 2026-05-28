# Final Critic Gate

> Agent: Locke
> Mode: read-only `a11y-critic`
> Date: 2026-05-28
> Scope: Drupal patch evaluation packets, TODO ledger, and all-items plan.

## Result

Revise before handoff, mostly for wording and evidence hygiene. The critic did not recommend changing the main local statuses except one source-status wording cleanup.

## Findings Applied

- Preserved raw generated evaluator reports, but added errata because some failed reports say `Eligible For Patch Recommendation: yes`; local packets and `STATUS.md` remain the controlling verdict.
- Tightened Haven Batch A wording so draft packet work is not described as upstream-ready before local checkout, visual/manual, and build/cache evidence exists.
- Added a source-link note that `blob/main` links are orientation links and must be replaced or supplemented with immutable permalinks and SHA evidence before upstream filing.
- Simplified ledger next actions to one concrete command or decision per row.
- Expanded `LABEL-IN-NAME-004` manual evidence with the exact Playwright/axe command, exit code, and axe-core version.
- Reworded `DRUPAL-A11Y-009` source status back to `Core patch ready` and moved the source PASS claim into packet notes.

## Calibration Summary

`BASELINE VERIFIED` for 010 and 012 is calibrated because both have local baseline-only evidence and explicitly do not claim patch verification. `OBSOLETE` for 011 is calibrated because the ID/name mapping is stale. `FAILED` for 003, 004, 006, and 007 is calibrated by before/after runs. `INCONCLUSIVE` for 001 and `LABEL-IN-NAME-004` is conservative pending manual/evaluator cleanup.
