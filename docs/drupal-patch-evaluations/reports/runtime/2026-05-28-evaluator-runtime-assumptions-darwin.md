# Evaluator Runtime Assumptions - 2026-05-28

## Scope

Read-only inspection of Mike Gifford's `mgifford/drupal-core` checkout at `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core`.

## Files And Commands Inspected

- `package.json`
- `core/package.json`
- `core/tests/playwright/scripts/evaluate-patch.js`
- `core/tests/playwright/scripts/evaluate-all-patches.js`
- `core/tests/playwright/scripts/lib/patch-evaluator-config.js`
- `core/tests/playwright/lib/*`
- patch docs and DDEV/settings artifacts
- `git status`, `git remote -v`, `find . -path './.ddev*'`, `ddev status`, `git status --ignored`, `git check-ignore`, and targeted `rg`

## Setup Assumptions

- The evaluator must run against the same checkout it mutates.
- `evaluate-patch.js` applies patches with `git apply` in `REPO_ROOT`, clears cache with `ddev drush`, then reverts with `git apply -R`.
- `evaluate-patch.js` hardcodes `BASE_URL = 'http://drupal-core.ddev.site'`; it does not honor `DRUPAL_BASE_URL`.
- It assumes an already-installed Drupal site with working Drush.
- It attempts admin authentication through `ddev drush uli --name=admin --uri=http://drupal-core.ddev.site`, then falls back to `admin/admin`.
- It does not install Drupal, enable fixture modules, create content, or make routes deterministic.
- It imports `core/tests/playwright/scripts/lib/patch-evaluator-config.js`, not `core/tests/playwright/lib/patch-evaluator-config.js`.
- The script imports `./lib/canonical-patch-map`, but that file is missing in the inspected commit, so `evaluate-patch.js` fails before runtime checks unless that helper is restored or the import is guarded.

## Safest Next Steps

1. Use a disposable DDEV checkout named `drupal-core` so the evaluator URL and `ddev drush` commands point at the same tree that `git apply` mutates.
2. Do not run patch evaluations against the separate `/Users/AlexUA_1/claude/drupal-core-fresh-20260404-164635` checkout while patches are applied in Mike's clone.
3. Add or patch `DRUPAL_BASE_URL` support before running on this machine, because local DDEV is using `:33000/:33001` instead of bare port 80/443.
4. Restore or guard `canonical-patch-map.js`.
5. Smoke check Drush, `/user/login`, admin auth, configured routes, and expected selectors before any before/after patch run.

## Runtime Follow-Through

Completed after this inspection:

- Created a clean disposable runtime clone at `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime`.
- Configured DDEV project `drupal-core` with Drupal 12, PHP 8.5, MariaDB 10.11, and Node 24.
- Avoided `composer install` in the runtime clone because it mutates tracked `core/` files in this repository shape; copied an existing local Drupal `vendor/` tree instead.
- Installed Drupal with the `standard` profile and admin/admin credentials.
- Enabled fixture modules: `theming_tools`, `imagefile`, `button`, `message`, `table`, `dialog`, `tab`, `lang_hebrew`, `actionlink`, `pager`, and `themeswitcher`.
- Smoke-checked public fixture routes: `/message`, `/message/short`, `/message/long`, `/buttons`, `/table`, `/action-link`, `/contact/imagefile_file`, and `/pager`.
- Added runtime-only evaluator fixes for `DRUPAL_BASE_URL` and missing `canonical-patch-map.js`.
- Ran `a11y-DRUPAL-A11Y-007-messages-landmark-role` with variant `codex-runtime-smoke-007`; the evaluator completed and returned `FAIL` because `/admin/modules` retained the targeted failures after patching.

## Blockers And Risks

- Immediate JS blocker: missing `core/tests/playwright/scripts/lib/canonical-patch-map.js`.
- Runtime blocker: no installed site in a clean Mike checkout by default.
- Local routing blocker: evaluator hardcodes `http://drupal-core.ddev.site`, but this machine's DDEV router exposes the project at `http://drupal-core.ddev.site:33000` and `https://drupal-core.ddev.site:33001`.
- Composer install in the inspected clone is risky: it can mutate the core tree through package installation and configured patches, which makes the checkout unsuitable as clean before/after evidence.
- Evaluations mutate git state. Run only from a clean disposable clone or worktree.
