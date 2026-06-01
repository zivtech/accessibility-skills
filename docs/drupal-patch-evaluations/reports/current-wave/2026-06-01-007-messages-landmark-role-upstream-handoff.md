# DRUPAL-A11Y-007 Messages Landmark Role Upstream Handoff

Date: 2026-06-01

## Status

`UPSTREAM PR OPEN`

PR #22 is filed as a bounded fix for the landmark-role problem: Drupal messages should not be exposed as `contentinfo` landmarks.

It is not filed as a claim that all warning/status live-region behavior has been human-AT verified. That boundary matters; otherwise this packet turns into a polished overclaim.

## Candidate Worktree

- Worktree: `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-pr-007-messages-landmark-role-20260601`
- Branch: `codex/messages-landmark-role-20260601`
- Base commit: `9ec853aac0cd55c6ed574343440b5d31e75ce81c`
- Candidate commit: `e187965ce86e` (`fix: use status roles for non-error messages`)
- Upstream PR: https://github.com/mgifford/drupal-core/pull/22
- Patch artifact: `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-007-messages-landmark-role-codex-reroll-status-alert-007.patch`
- Patch SHA-256: `b70efc3a4f20349dd082fce31da37cf0e2b204c72269ffd3bff291fa7fe1be8c`

## Patch Shape

Files changed:

- `core/modules/system/templates/status-messages.html.twig`
- `core/modules/system/tests/themes/test_messages/templates/status-messages.html.twig`
- `core/themes/claro/templates/misc/status-messages.html.twig`
- `core/themes/default_admin/templates/misc/status-messages.html.twig`
- `core/themes/olivero/templates/misc/status-messages.html.twig`
- `core/themes/stable9/templates/media-library/status-messages.html.twig`
- `core/themes/starterkit_theme/templates/misc/status-messages.html.twig`
- `core/misc/message.js`
- `core/misc/tabledrag.js`
- `core/themes/claro/js/messages.js`
- `core/themes/claro/js/tabledrag.js`
- `core/themes/default_admin/js/messages.js`
- `core/themes/default_admin/js/tabledrag.js`
- `core/themes/default_admin/migration/js/messages.js`
- `core/themes/default_admin/migration/js/tabledrag.js`
- `core/profiles/demo_umami/themes/umami/js/components/messages/messages.js`
- `core/themes/olivero/js/message.theme.js`
- `core/modules/system/tests/src/Functional/Form/ModulesListFormWebTest.php`
- `core/modules/system/tests/src/Functional/Render/PlaceholderMessageTest.php`
- `core/tests/Drupal/FunctionalJavascriptTests/Ajax/MessageCommandTest.php`

The candidate replaces message-group `contentinfo` landmarks with message roles:

- Errors render as `role="alert"`.
- Status, warning, and non-error messages render as `role="status"`.
- JavaScript errors are announced assertively.
- JavaScript warnings stay polite.
- Tabledrag unsaved-change warnings render as `role="status"`.

## Evidence

Evaluator:

- Command: `DRUPAL_BASE_URL=http://drupal-core.ddev.site A11Y_VARIANT_ID=codex-current-main-announce-priority-007 node core/tests/playwright/scripts/evaluate-patch.js a11y-DRUPAL-A11Y-007-messages-landmark-role`
- Result: `PASS`
- Outcome reason: `targeted-issues-fixed-without-regressions`
- Baseline observed instances: 2
- Fixed instances after patch: 2
- Remaining instances after patch: 0
- New violations introduced: 0
- Target `contentinfo` landmark rules were removed on `/admin/appearance` and `/admin/modules`.

Focused DOM and test evidence:

- `Drupal.Message` warning: `role="status"`; live region `aria-live="polite"`.
- `Drupal.Message` error: `role="alert"`; live region `aria-live="assertive"`.
- Tabledrag warning probe emitted `role="status"` on the tested menu, block, and taxonomy overview routes.
- `MessageCommandTest::testMessageDefaultAnnouncementPriorities`: pass, 1 test / 7 assertions.
- `PlaceholderMessageTest::testMessagePlaceholder`: pass, 1 test / 2 assertions.
- `ModulesListFormWebTest::testModulesListFormStatusMessage`: pass, 1 test / 15 assertions.

VoiceOver caption-panel evidence:

- Dynamic error message text was captured in the macOS VoiceOver caption panel.
- Direct assertive `Drupal.announce()` output was captured in the macOS VoiceOver caption panel.
- Warning/status polite output rendered correctly in the DOM and live region, but timed caption-panel captures did not show the polite warning/status text.

Final hygiene before PR:

- `git diff --check origin/main...HEAD`: pass.
- `node --check` on changed message/tabledrag JavaScript files: pass.
- `php -l` on changed PHP test files: pass.
- Secret-pattern scan on branch diff: no hits.
- No PR template was present in the checkout.

GitHub state at creation:

- PR #22: open, not draft.
- Merge state: `CLEAN`.
- AccessLint: `SUCCESS`.

## Boundaries

This PR claims:

- Drupal status messages are no longer exposed as `contentinfo` landmarks.
- Error messages are represented as alerts.
- Non-error messages are represented as status messages.
- Warning live-region priority remains polite.
- The observed target axe landmark issues are fixed without introducing new evaluator violations.

This PR does not claim:

- A human VoiceOver or NVDA user verified every live-region announcement behavior.
- VoiceOver caption-panel testing proved polite warning/status announcements are spoken.
- Warnings should interrupt users assertively.
- Non-target adjacent `region` or `summary-name` violations are fixed.

## Next Action

Track Mike review on PR #22. If reviewers want warnings to interrupt, handle that as an explicit follow-up AT/product decision rather than silently changing warning priority inside the landmark fix.
