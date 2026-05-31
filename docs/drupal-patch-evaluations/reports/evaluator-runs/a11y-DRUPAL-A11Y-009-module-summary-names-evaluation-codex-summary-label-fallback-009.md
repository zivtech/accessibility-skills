# Sanitized Evaluator Summary: DRUPAL-A11Y-009 Module Summary Names

## Run Metadata

| Field | Value |
|---|---|
| Patch ID | `a11y-DRUPAL-A11Y-009-module-summary-names` |
| Variant | `codex-summary-label-fallback-009` |
| Run date | 2026-05-31 |
| Runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| Target route | `/admin/modules` |
| Target selector | `#edit-modules-nyan-cat-enable-description > .module-list__module-summary` |
| Rule | `summary-name` |
| WCAG | 4.1.2 Name, Role, Value |
| Raw artifacts | Runtime-only; not committed because they include local DDEV status fields |

## Fixture State

The original local packet was blocked because the Nyan Cat test module was not discoverable in the runtime. The fixture repair was runtime-only:

```text
$settings['extension_discovery_scan_tests'] = TRUE
ddev drush cr
```

After repair, Drupal discovered `core/modules/system/tests/modules/nyan_cat`, `/admin/modules` rendered the expected row, and the evaluator observed the baseline selector.

## Evaluator Result

```text
Status: PASS
Outcome reason: targeted-issues-fixed-without-regressions
Case generation mode: pattern-report-derived
Pattern source: reports/pattern-report-2026-05-06.json
Target pattern ID: DRU-4422E904
Generated pattern ID: DRU-4422E904
Pattern observed before patch attempt: yes
Baseline observed instances: 1
Fixed instances after patch: 1
Remaining instances after patch: 0
Eligible for patch recommendation: yes
```

## Violation Counts

| Rule | Before | After | Change |
|---|---:|---:|---:|
| `summary-name` | 1 | 0 | -1 |
| `landmark-contentinfo-is-top-level` | 2 | 2 | 0 |
| `landmark-no-duplicate-contentinfo` | 1 | 1 | 0 |
| `region` | 1 | 1 | 0 |
| Total | 5 | 4 | -1 |

No new violations were introduced.

## Implementation Under Test

The candidate patch does not add a blanket `aria-label` to every module details summary. Instead:

- preprocess computes a `summary_label` only when the rendered module description becomes empty plain text;
- module-list templates add `aria-label` only when that fallback exists;
- the fallback label is `Details for @module`, for example `Details for Nyan cat`;
- non-empty description summaries keep their visible text as the accessible name.

## Additional Validation

```text
git diff --check: pass
php -l SystemAdminThemePreprocess.php: pass
php -l ModulesListFormWebTest.php: pass
Drupal PHPCS on changed PHP/Twig/test files: pass
Focused functional test: OK (1 test, 10 assertions)
Full ModulesListFormWebTest.php: OK (6 tests, 68 assertions)
```

Live DOM smoke after applying the candidate:

```json
{
  "nyanExists": true,
  "nyanText": "",
  "nyanAriaLabel": "Details for Nyan cat",
  "nonEmptyAriaLabel": null,
  "emptySummaryCount": 0
}
```

## Boundary

This is DOM and axe evidence plus Drupal functional coverage. It is not a human screen-reader verification run. The patch fixes the missing accessible name for empty module-description summaries; it does not decide whether the module listing should suppress empty details disclosures entirely.
