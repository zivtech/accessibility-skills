# Fresh Chat Handoff: Drupal A11y Patch Queue After PR #11

> Date: 2026-05-31
> Local repo: `/Users/AlexUA_1/claude/a11y-meta-skills`
> Upstream target: `mgifford/drupal-core`

## What Was Completed

- Opened evaluator infrastructure PR #8:
  - https://github.com/mgifford/drupal-core/pull/8
  - Branch: `AlexU-A:codex/evaluator-support-mike-20260529`
- Opened `DRUPAL-A11Y-012-empty-heading-elements` PR #9:
  - https://github.com/mgifford/drupal-core/pull/9
  - Branch: `AlexU-A:codex/filter-tips-empty-heading-20260530`
- Opened `DRUPAL-A11Y-010-heading-order` PR #10:
  - https://github.com/mgifford/drupal-core/pull/10
  - Branch: `AlexU-A:codex/content-pager-heading-20260531`
- Opened `LABEL-IN-NAME-004-filter-format-aria-label` PR #11:
  - https://github.com/mgifford/drupal-core/pull/11
  - Branch: `AlexU-A:codex/filter-format-label-in-name-20260531`

## Live PR State Checked 2026-05-31

```text
PR #8  evaluator support
State: open, not draft
Merge state: UNSTABLE
Checks: AccessLint PENDING
Comments/reviews: none
```

```text
PR #9  filter tips empty heading
State: open, not draft
Merge state: CLEAN
Checks: AccessLint SUCCESS
Comments/reviews: AccessLint has one COMMENTED review from the earlier commit; current check is passing.
```

```text
PR #10 content overview pager heading
State: open, not draft
Merge state: CLEAN
Checks: AccessLint SUCCESS
Comments/reviews: none
```

```text
PR #11 filter format Configure link label
State: open, not draft
Merge state: CLEAN
Checks: AccessLint SUCCESS
Comments/reviews: none
```

Before doing new work, recheck live state with:

```bash
gh pr view 8 --repo mgifford/drupal-core --json number,state,isDraft,mergeStateStatus,url,headRefName,statusCheckRollup,reviews,comments
gh pr view 9 --repo mgifford/drupal-core --json number,state,isDraft,mergeStateStatus,url,headRefName,statusCheckRollup,reviews,comments
gh pr view 10 --repo mgifford/drupal-core --json number,state,isDraft,mergeStateStatus,url,headRefName,statusCheckRollup,reviews,comments
gh pr view 11 --repo mgifford/drupal-core --json number,state,isDraft,mergeStateStatus,url,headRefName,statusCheckRollup,reviews,comments
```

## Worktrees

Local docs repo:

```text
/Users/AlexUA_1/claude/a11y-meta-skills
branch: main
```

Runtime evaluator checkout:

```text
/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
branch: main
state: dirty runtime/evaluator worktree
use for: reproductions and local evaluator/browser runs only
do not use for: PR commits
```

PR worktrees:

```text
/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-pr-evaluator-support-20260529
/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-pr-012-empty-heading-20260530
/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-pr-010-heading-order-20260531
/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-pr-label-in-name-004-20260531
```

Important remote rule: use `mike-fork` (`AlexU-A/mgifford-drupal-core`) for Mike-facing work. Do not push Mike-facing work to `AlexU-A/drupal-core`.

## Keyboard-User Boundary

The browser tools here are allowed and expected to act like keyboard users for keyboard operability, focus order, and activation checks. Do not reduce those checks to static DOM assertions when the question is whether a keyboard user can reach or operate the control.

Keep the boundary precise: keyboard-user evidence is not the same as human screen-reader, voice-control, NVDA, JAWS, or VoiceOver verification. For `DRUPAL-A11Y-007`, do not claim AT verification until the human checklist is complete.

## Next Decision

Valid next lanes:

- Track review/check state for PRs #8-#11.
- If a human can run NVDA or VoiceOver, finish the `DRUPAL-A11Y-007` smoke checklist before upstream wording.
- If no human AT check is available, continue with an agent-verifiable packet and require real keyboard/browser evidence where interaction is part of the user impact.

Key files:

```text
docs/drupal-patch-evaluations/STATUS.md
docs/drupal-patch-evaluations/reports/current-wave/2026-05-28-mike-review-queue.md
docs/drupal-patch-evaluations/reports/current-wave/2026-05-31-label-in-name-004-upstream-handoff.md
docs/drupal-patch-evaluations/reports/manual-checks/2026-05-28-drupal-a11y-007-at-smoke-checklist.md
```
