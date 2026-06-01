# PR #8-#20 Agent Browser Verification Wave

Checked at `2026-06-01T02:49Z` (`2026-05-31 22:49 -0400`).

## Scope

This pass rechecked the open Mike-facing PR queue and then ran a focused agent-browser verification wave against the local DDEV evidence runtime:

```text
/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
https://drupal-core.ddev.site
```

It used Playwright real keyboard events (`page.keyboard.press('Tab')`, `Enter`, and `Space`) plus focused axe-core rule scans and DOM assertions. It did not use synthetic keyboard events.

## Runtime Preparation

The first browser pass found that the runtime still had only some earlier patch state applied. That was useful negative evidence: most PRs would have failed if verified against that stale runtime.

The following patch artifacts then applied cleanly to the evidence runtime, followed by `ddev drush cr`:

```text
a11y-LABEL-IN-NAME-004-filter-format-aria-label-codex-configure-link-label.patch
a11y-DRUPAL-A11Y-004-tabindex-buttons-test-form-codex-remove-positive-tabindex.patch
a11y-DRUPAL-A11Y-003-select-all-checkbox-label-codex-select-all-aria-label.patch
a11y-DRUPAL-A11Y-006-theme-switcher-landmark-codex-form-landmark-006.patch
a11y-DRUPAL-A11Y-010-admin-block-heading-order-codex-admin-block-heading-level.patch
a11y-DRUPAL-A11Y-010-multiple-value-field-heading-order-codex-multiple-value-field-label.patch
a11y-DRUPAL-A11Y-010-datetime-wrapper-heading-order-codex-datetime-wrapper-label.patch
a11y-DRUPAL-A11Y-008-empty-table-headers-codex-field-operations-header.patch
a11y-DRUPAL-A11Y-009-module-summary-names-codex-summary-label-fallback.patch
```

`DRUPAL-A11Y-002` / PR #20 was checked under its required conditions by temporarily setting:

```text
system.theme default: default_admin
system.theme admin: default_admin
default_admin.settings preset_accent_color: orange
```

The runtime was restored afterward to:

```text
system.theme default: olivero
system.theme admin: claro
```

## Live PR State

Rechecked with `gh pr list` / `gh pr view` against `mgifford/drupal-core`.

| PR | State | Check state | Review/comment state |
|---:|---|---|---|
| #8 | Open, not draft, `UNSTABLE` | AccessLint pending on `fac67e0a78` | No comments or reviews |
| #9 | Open, not draft, `CLEAN` | AccessLint success | Old AccessLint review is stale and already answered |
| #10 | Open, not draft, `CLEAN` | AccessLint success | No comments or reviews |
| #11 | Open, not draft, `CLEAN` | AccessLint success | No comments or reviews |
| #12 | Open, not draft, `CLEAN` | AccessLint success | No comments or reviews |
| #13 | Open, not draft, `CLEAN` | AccessLint success | No comments or reviews |
| #14 | Open, not draft, `CLEAN` | AccessLint success | No comments or reviews |
| #15 | Open, not draft, `CLEAN` | AccessLint success | No comments or reviews |
| #16 | Open, not draft, `CLEAN` | AccessLint success | No comments or reviews |
| #17 | Open, not draft, `CLEAN` | AccessLint success | No comments or reviews |
| #18 | Open, not draft, `CLEAN` | AccessLint success | No comments or reviews |
| #19 | Open, not draft, `CLEAN` | AccessLint success | No comments or reviews |
| #20 | Open, not draft, `CLEAN` | AccessLint success | No comments or reviews |

## Verification Results

| PR | Result | Evidence |
|---:|---|---|
| #8 | `PARTIAL` | Local infrastructure checks passed: `node --check` on evaluator files, `node --test core/tests/playwright/scripts/evaluator-support.test.js` passed 6/6 tests, and `git diff --check` passed. GitHub AccessLint is still pending, so the PR remains a monitoring/blocker state rather than fully CI-verified. |
| #9 | `AGENT VERIFIED` | `/dialog`, `/tabs`, and `/tabs/format/plain_text` returned 200; empty heading DOM count 0; axe `empty-heading` violations 0 on all three routes. |
| #10 | `AGENT VERIFIED` | `/admin/content` returned 200; `#pagination-heading` rendered as `h2`; axe `heading-order` violations 0. |
| #11 | `AGENT VERIFIED` | `/admin/config/content/formats` returned 200; six visible `Configure` links all had accessible names beginning with `Configure`; real Tab reached all six Configure links; real Enter from a focused Configure link navigated to `/admin/config/content/formats/manage/basic_html?...`; axe `label-content-name-mismatch` violations 0. |
| #12 | `AGENT VERIFIED` | `/buttons` and `/buttons/disabled` returned 200; positive/explicit form `tabindex` count 0; axe `tabindex` violations 0; real Tab order reached the fixture controls in native DOM order, including `edit-submit`, `edit-danger`, `edit-cancel`, `edit-submit--3`, `edit-delete`, `edit-cancel--3`, `edit-submit--2`, and `edit-danger--2`. |
| #13 | `AGENT VERIFIED` | `/table` returned 200; select-all checkbox had `aria-label="Select all rows in this table"` and no `title`; real Space toggled checked `false -> true`; label changed to `Deselect all rows in this table`; axe `label-title-only` violations 0. |
| #14 | `AGENT VERIFIED` | `/`, `/admin`, `/admin/appearance`, `/admin/config/content/formats`, and `/admin/content` returned 200 and rendered `form[aria-label="Theme switcher"]` with a select control. Real Tab reached the `preferred_theme` select on `/admin/content`. The test did not change the selected theme. |
| #15 | `AGENT VERIFIED` | `/cd-navigation/config` returned 200; `h2.panel__title` count 9; `h3.panel__title` count 0; axe `heading-order` violations 0. |
| #16 | `AGENT VERIFIED` | `/contact/field_cardinality_test`, `/contact/presuf_formatted`, and `/contact/presuf_number` returned 200; table-header nested heading count 0; axe `heading-order` violations 0 on all three routes. |
| #17 | `AGENT VERIFIED` | `/admin/form_style` returned 200 with 2 datetime wrappers, 0 wrapper `h4` elements, 2 grouped wrappers; `/contact/textform` returned 200 with 14 datetime wrappers, 0 wrapper `h4` elements, 12 grouped wrappers; axe `heading-order` violations 0 on both routes. |
| #18 | `AGENT VERIFIED` | `/autocomplete` returned 200; table headers were `Select some other countries`, `Operations`, and `Order`; empty header count 0; axe `empty-table-header` violations 0. |
| #19 | `AGENT VERIFIED` | `/admin/modules` returned 200; Nyan Cat empty summary had `aria-label="Details for Nyan cat"`; real Space toggled its parent details element closed -> open; empty unnamed summary count 0; axe `summary-name` violations 0. |
| #20 | `AGENT VERIFIED` | Under Default Admin + orange accent, `/action-link`, `/admin`, and `/admin/content` returned 200; `data-gin-accent="orange"`; `--accent-base` / `--gin-color-primary` resolved to `#bf4e25`; axe `color-contrast` violations 0 on all three routes. |

## Current Decision

PRs #9-#20 are agent-browser verified under the patched evidence runtime.

PR #8 has strong local helper-level verification, but it is still not fully check-verified on GitHub because AccessLint remains pending. Treat #8 as a monitor/blocker state until AccessLint resolves or reviewer feedback appears.

## Non-Claims

- This is not human screen-reader verification.
- This does not prove NVDA, JAWS, VoiceOver, switch control, or voice-control behavior for every PR.
- This does not claim Mike has reviewed or accepted any PR.
- This does not expand any PR beyond its scoped target.
- `DRUPAL-A11Y-007` is not part of the open PR queue and remains `INCONCLUSIVE` until a human NVDA or VoiceOver announcement-behavior smoke pass is recorded.
