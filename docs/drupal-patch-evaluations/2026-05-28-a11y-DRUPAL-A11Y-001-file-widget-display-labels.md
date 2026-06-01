# Drupal Accessibility Patch Evaluation Packet: DRUPAL-A11Y-001 File Widget Display Labels

> Status: VERIFIED
> Prepared: 2026-05-28
> Purpose: Local evaluator packet for a revised `a11y-DRUPAL-A11Y-001-file-widget-display-labels` patch candidate.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-DRUPAL-A11Y-001-file-widget-display-labels` |
| Status | `VERIFIED` |
| Project/package | `mgifford/drupal-core` |
| Target commit checked | `9ec853aac0cd55c6ed574343440b5d31e75ce81c` (`origin/main` on 2026-06-01) |
| Local runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| Evaluation artifact | `docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-001-file-widget-display-labels-evaluation-codex-invisible-label-001.md` |
| Patch artifact | `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-001-file-widget-display-labels-codex-invisible-label.patch` |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Issue Summary

| Field | Value |
|---|---|
| Rule/source | `axe-core label` |
| WCAG SC | `1.3.1 Info and Relationships (A)` in upstream artifacts |
| Route | `/contact/imagefile_file` |
| Selector | `[id^="edit-imagefile-file-limited-"][id$="-display"]` |
| Fixture | `theming_tools:imagefile` |
| Runtime state | DDEV project `drupal-core`, Drupal 12.0-dev, admin/admin, fixture modules enabled |

## Local Evaluator Result

Command:

```bash
cd /Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
DRUPAL_BASE_URL=http://drupal-core.ddev.site \
  A11Y_VARIANT_ID=codex-invisible-label-001 \
  node core/tests/playwright/scripts/evaluate-patch.js \
  a11y-DRUPAL-A11Y-001-file-widget-display-labels
```

Result:

```text
Status: PASS
Outcome reason: targeted-issues-fixed-without-regressions
Target pattern ID: DRU-6CA3D5EB
Pattern ID match type: source-pattern-matched
Case generation mode: pattern-report-derived
Baseline observed instances: 1
Fixed instances after patch: 1
Remaining instances after patch: 0
Introduced new violations: 0
```

The evaluator observed four `label` violations before patching and zero `label` violations after patching on `/contact/imagefile_file`. Remaining non-target violations were `color-contrast` and `region`.

## Revised Patch Shape

The earlier patch added `aria-label` to the file display checkbox render element. The revised patch instead keeps the existing native `#title` and changes the multiple-file table preprocess from unsetting that title to rendering it with `#title_display = 'invisible'`.

This is narrower and more semantic: the visible table remains unchanged, while the checkbox gets a real associated label:

- Source change: `core/modules/file/src/Hook/FileThemeHooks.php`
- Regression coverage: `core/modules/file/tests/src/Functional/FileFieldDisplayTest.php`
- Patch SHA-256: `a2e5a5eddbf42e6f09b51d4e3412ac942c9e340f1de6924d2838313ce7e2ec9e`

## Agent Browser Smoke

Patched runtime route: `/contact/imagefile_file`

- Target selector count: 4 checkboxes.
- Each target checkbox had a `label[for]` with text `Include file in display`.
- Each target label included `visually-hidden`.
- No target checkbox used `aria-label`; the accessible name came from the native label.
- axe `label` run after patch: 0 violations.
- Real keyboard path: repeated `Tab` reached `#edit-imagefile-file-limited-0-display`; focused checkbox responded to `Space` from checked `true` to `false` and a second `Space` restored `true`.

This is an agent browser accessible-name and keyboard smoke check, not a human VoiceOver/NVDA session. Unlike `DRUPAL-A11Y-007`, this issue is a static form-label association, so the role/name and keyboard evidence is enough for local verification; no live announcement timing claim is being made.

## Focused Test/Hygiene

```text
php -l core/modules/file/src/Hook/FileThemeHooks.php
php -l core/modules/file/tests/src/Functional/FileFieldDisplayTest.php
git diff --check
vendor/bin/phpcs --standard=core/phpcs.xml.dist <changed files>
ddev exec ... ./vendor/bin/phpunit -c core/phpunit.xml.dist core/modules/file/tests/src/Functional/FileFieldDisplayTest.php --filter testNodeDisplay
```

Result: syntax checks passed, diff whitespace passed, PHPCS passed, and the focused Drupal functional test passed with 1 test / 37 assertions.

## Gates

- [x] Baseline target observed before patch.
- [x] Patch applied and reverted.
- [x] Same route and state tested after patch.
- [x] Target rule absent after patch.
- [x] No new violations introduced.
- [x] Pattern report ID mapping reconciled to source pattern `DRU-6CA3D5EB`; latest run used pattern-report-derived cases.
- [x] Agent browser accessible-name and keyboard smoke check completed.

## Outcome

`VERIFIED`

The revised patch fixes the target source pattern with native invisible labels, preserves the visible table layout, passes the standard evaluator with source pattern mapping, and has focused browser/keyboard proof.

Upstream PR: https://github.com/mgifford/drupal-core/pull/21

Next action: track Mike review on PR #21; keep scope limited to native invisible labels for multiple file display checkboxes unless reviewer asks for unique per-file label text.
