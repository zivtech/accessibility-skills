# DRUPAL-A11Y-007 Current-Main Reroll

Checked at `2026-06-01T01:54Z` (`2026-05-31 21:54 -0400`).

## Worktree

Runtime evidence checkout remains read-only/evidence space for this decision.

Fresh upstream candidate worktree:

```text
/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-pr-007-messages-landmark-role-20260601
```

Branch:

```text
codex/messages-landmark-role-20260601
```

Base:

```text
origin/main 9ec853aac0cd
```

Local candidate commit:

```text
c297c18d98 fix: use status roles for non-error messages
```

## What Changed From The Saved Reroll

The saved `007` reroll patch still applied cleanly to current `origin/main`.

During critic review, the tabledrag warning path was flagged as inconsistent with the reroll's role model: Drupal.Message warnings and server-rendered warning messages were `role="status"`, but tabledrag "You have unsaved changes." warnings still hardcoded `role="alert"`.

The candidate branch extends the reroll so tabledrag warnings use `role="status"` in:

- `core/misc/tabledrag.js`
- `core/themes/claro/js/tabledrag.js`
- `core/themes/default_admin/js/tabledrag.js`
- `core/themes/default_admin/migration/js/tabledrag.js`

This does not change the original axe target from `contentinfo` landmarks. It keeps the broader message-role claim coherent: errors are alert-urgent; non-error messages are status/polite.

## Checks Run

```text
git apply --check saved 007 reroll patch against origin/main: pass
git diff --check: pass
php -l changed PHP test files: pass
node --check changed JS files: pass
Drupal PHPCS on changed PHP/Twig files: pass
credential-pattern scan on changed files: no hits
```

Additional grep check:

```text
tabledrag-changed-warning hardcoded role="alert": no remaining matches in core/misc, Claro, or Default Admin tabledrag copies
```

## Runtime Evaluator Rerun

The regenerated candidate patch was copied into the disposable runtime patch slot and evaluated with:

```bash
DRUPAL_BASE_URL=http://drupal-core.ddev.site \
  A11Y_VARIANT_ID=codex-current-main-tabledrag-007 \
  node core/tests/playwright/scripts/evaluate-patch.js \
  a11y-DRUPAL-A11Y-007-messages-landmark-role
```

Sanitized result:

```text
Status: PASS
Outcome reason: targeted-issues-fixed-without-regressions
Baseline observed instances: 2
Fixed instances after patch: 2
Remaining instances after patch: 0
New violations introduced: 0
Total violations: 12 before, 3 after
```

Route summary:

| Route | Before | After | Target result |
|---|---:|---:|---|
| `/admin/appearance` | 4 violations | 1 violation | Target `contentinfo` landmark rules removed |
| `/admin/modules` | 5 violations | 2 violations | Target `contentinfo` landmark rules removed |

Remaining after-patch violations were pre-existing adjacent issues (`region`, `summary-name`), not patch-owned target regressions.

Raw runtime artifacts were left in the disposable runtime under `patches/a11y-DRUPAL-A11Y-007-messages-landmark-role-evaluation-codex-current-main-tabledrag-007.*`. Do not copy those raw files into this repo without sanitizing because the evaluator captures local DDEV status fields.

## DOM Role Probe

With the regenerated patch applied in the runtime, a focused Playwright DOM probe confirmed:

```text
Drupal.Message warning: role="status"
Drupal.Message error: role="alert"
```

Tabledrag warning probe:

| Route | Result |
|---|---|
| `/admin/structure/menu/manage/main` | `Drupal.theme('tableDragChangedWarning')` available; emitted `role="status"` |
| `/admin/structure/block` | `Drupal.theme('tableDragChangedWarning')` available; emitted `role="status"` |
| `/admin/structure/taxonomy/manage/tags/overview` | `Drupal.theme('tableDragChangedWarning')` available; emitted `role="status"` |

Two content-display routes did not load tabledrag in this runtime, so they were not counted as tabledrag evidence.

## Functional Test Rerun

With the regenerated patch temporarily applied in the runtime harness:

```text
PlaceholderMessageTest::testMessagePlaceholder: OK (1 test, 2 assertions)
ModulesListFormWebTest::testModulesListFormStatusMessage: OK (1 test, 15 assertions)
```

The patch was reverted after the test run, and a follow-up `git apply --check` confirmed the runtime target files were clean enough for the patch to apply again.

## Tests Not Run

Browser/functional PHPUnit was not run from the fresh candidate worktree because the checkout does not have its own Composer vendor tree or configured Drupal web-test environment. The dirty runtime has that tooling, but it is evidence space and should not be treated as the source branch.

Human NVDA or VoiceOver smoke was not run in this session.

## Current Decision

Keep `DRUPAL-A11Y-007` as `INCONCLUSIVE`.

The branch is now a cleaner upstream candidate with refreshed evaluator and DOM evidence, but it still should not be filed as AT-verified. The next gate remains a short human NVDA or VoiceOver smoke check for:

- status/warning message announcement;
- error alert urgency;
- landmark navigation without duplicate `contentinfo`;
- tabledrag "unsaved changes" warning behavior if the tester can trigger it cheaply.
