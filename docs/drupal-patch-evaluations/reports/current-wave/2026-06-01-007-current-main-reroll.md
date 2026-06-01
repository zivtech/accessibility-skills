# DRUPAL-A11Y-007 Current-Main Reroll

Checked at `2026-06-01T01:44Z` (`2026-05-31 21:44 -0400`).

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

## Tests Not Run

Browser/functional PHPUnit was not run from this fresh worktree because the checkout does not have its own Composer vendor tree or configured Drupal web-test environment. The dirty runtime has that tooling, but it is evidence space and should not be treated as the source branch.

The previous runtime evaluator pass and DOM/axe role smoke still support the reroll direction, but they do not include the new tabledrag warning adjustment.

## Current Decision

Keep `DRUPAL-A11Y-007` as `INCONCLUSIVE`.

The branch is now a cleaner upstream candidate, but it still should not be filed as AT-verified. The next gate remains a short human NVDA or VoiceOver smoke check for:

- status/warning message announcement;
- error alert urgency;
- landmark navigation without duplicate `contentinfo`;
- tabledrag "unsaved changes" warning behavior if the tester can trigger it cheaply.
