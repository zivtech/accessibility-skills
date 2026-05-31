# Drupal Accessibility Patch Evaluation Packet: DRUPAL-A11Y-009 Module Summary Names

> Status: VERIFIED
> Prepared: 2026-05-28
> Updated: 2026-05-31
> Purpose: Local evaluator packet for the `summary-name` violation on empty module descriptions in `/admin/modules`.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-DRUPAL-A11Y-009-module-summary-names` |
| Status | `VERIFIED` |
| Project/package | `mgifford/drupal-core` |
| Target commit checked | `9ec853aac0cd` (`origin/main` on 2026-05-31) |
| Upstream branch | `AlexU-A:codex/module-summary-names-20260531` |
| Upstream PR | https://github.com/mgifford/drupal-core/pull/19 |
| Upstream commit | `01ffe16648` (`fix: label empty module summaries`) |
| Local runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| PR worktree | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-pr-module-summary-names-20260531` |
| Patch artifact | `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-009-module-summary-names-codex-summary-label-fallback.patch` |
| Sanitized evaluator summary | `docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-009-module-summary-names-evaluation-codex-summary-label-fallback-009.md` |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Fixture Repair

The earlier 2026-05-28 packet was blocked because the evaluator selector was absent:

```text
#edit-modules-nyan-cat-enable-description > .module-list__module-summary
```

That blocker was not a Drupal core proof failure. The `nyan_cat` module is a core test module at `core/modules/system/tests/modules/nyan_cat`, and Drupal does not discover test extensions in a normal runtime unless test-extension discovery is enabled. The runtime-only repair was:

```bash
# runtime-only, not part of the upstream patch
$settings['extension_discovery_scan_tests'] = TRUE;
ddev drush cr
```

After that repair, `/admin/modules` exposed the Nyan Cat row and the evaluator observed the baseline `summary-name` violation.

## Patch Decision

The old patch artifact added an unconditional `aria-label="{{ module.name }}: {{ module.description }}"` to every module details summary. That was too broad: it changed accessible names for summaries that already had visible description text.

The upstream PR uses a narrower design:

- `SystemAdminThemePreprocess::preprocessSystemModulesDetails()` computes `module.summary_label` only when the rendered description becomes empty plain text.
- Core, Claro, Default Admin, and Stable 9 module-list templates add `aria-label` only when `module.summary_label` exists.
- The label is `Details for @module`, for example `Details for Nyan cat`.
- The existing `ModulesListFormWebTest::testModulesListFormWithEmptyDescriptionInfoFile()` now asserts both sides: the empty-description module gets the fallback, while a non-empty module summary does not get a new `aria-label`.

## Local Evaluator Result

Command:

```bash
cd /Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
DRUPAL_BASE_URL=http://drupal-core.ddev.site \
  A11Y_VARIANT_ID=codex-summary-label-fallback-009 \
  node core/tests/playwright/scripts/evaluate-patch.js \
  a11y-DRUPAL-A11Y-009-module-summary-names
```

Result:

```text
Status: PASS
Outcome reason: targeted-issues-fixed-without-regressions
Pattern observed before patch attempt: yes
Baseline observed instances: 1
Fixed instances after patch: 1
Remaining instances after patch: 0
Total violations: 5 before, 4 after
summary-name: 1 before, 0 after
New violations introduced: 0
```

Raw evaluator JSON/HTML/Markdown stayed in the runtime checkout only. They include local DDEV status fields, so this repo keeps only the sanitized summary.

## Additional Validation

```bash
git diff --check
php -l core/modules/system/src/Theme/SystemAdminThemePreprocess.php
php -l core/modules/system/tests/src/Functional/Form/ModulesListFormWebTest.php
phpcs --standard=core/phpcs.xml.dist \
  core/modules/system/src/Theme/SystemAdminThemePreprocess.php \
  core/modules/system/tests/src/Functional/Form/ModulesListFormWebTest.php \
  core/modules/system/templates/system-modules-details.html.twig \
  core/themes/claro/templates/admin/system-modules-details.html.twig \
  core/themes/default_admin/templates/admin/system-modules-details.html.twig \
  core/themes/stable9/templates/admin/system-modules-details.html.twig
```

Functional test commands were run in the DDEV runtime with the local DDEV test database value supplied via `SIMPLETEST_DB=[local DDEV DB]`:

```text
phpunit --filter testModulesListFormWithEmptyDescriptionInfoFile core/modules/system/tests/src/Functional/Form/ModulesListFormWebTest.php
OK (1 test, 10 assertions)

phpunit core/modules/system/tests/src/Functional/Form/ModulesListFormWebTest.php
OK (6 tests, 68 assertions)
```

Live DOM smoke on `/admin/modules` after applying the candidate:

```json
{
  "nyanExists": true,
  "nyanText": "",
  "nyanAriaLabel": "Details for Nyan cat",
  "nonEmptyAriaLabel": null,
  "emptySummaryCount": 0
}
```

## Critic Gate

Verdict: `PASS WITH BOUNDARIES`.

The fix is intentionally source-specific to module-list details summaries whose rendered description is empty. It does not claim human assistive-technology verification, does not change the visible module listing UI, and does not change the accessible names for summaries that already expose visible description text. A skeptic could still ask whether an empty visual description column should render a details disclosure at all; that is a broader module-list UX question and is not solved by this patch.

## Outcome

`VERIFIED`

PR #19 is open, not draft, merge state `CLEAN`, and AccessLint passing as of 2026-05-31. Track Mike's review; keep scope limited to empty module description summaries unless review asks for a broader module-list rendering change.
