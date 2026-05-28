# Core Hygiene Source Triage - 2026-05-28

## Scope

Read-only source triage for core patch-hygiene items:

- `LABEL-IN-NAME-004`
- `DRUPAL-A11Y-002`
- `DRUPAL-A11Y-005`
- `DRUPAL-A11Y-006`
- `DRUPAL-A11Y-008`
- `DRUPAL-A11Y-009`

## Agent

| Field | Value |
|---|---|
| Agent | Cicero |
| Role | Explorer |
| Run ID | `2026-05-28-core-hygiene-source-triage-cicero` |
| Edits made | None |

## Findings

| Item | Source status | Stale/root cause | Patch | Likely target | Next action |
|---|---|---|---|---|---|
| `LABEL-IN-NAME-004-filter-format-aria-label` | `PROPOSED-PATCHES.md` says patch ready; May 7 rollup/per-patch eval says inconclusive, baseline not observed, preflight corrupt. | Raw patch still appears malformed; eval reports corrupt patch at line 23. Target page also did not expose `table a:has-text("Configure")`. | `patches/a11y-LABEL-IN-NAME-004-filter-format-aria-label.patch` | `core/modules/filter/src/FilterFormatListBuilder.php` | Regenerate the patch with valid hunk counts, then recheck `/admin/config/content/formats` for the Configure link accessible name. |
| `DRUPAL-A11Y-002-submit-button-contrast` | Proposed ready; rollup says inconclusive/`patch-does-not-apply`; `reports/patches/INDEX.md` is older and calls it placeholder/no-apply. | Evaluation references old `core/themes/default_admin/css/components/button.pcss.css`, but current raw patch targets `core/themes/default_admin/src/Helper.php`; report is stale against current patch content. | `patches/a11y-DRUPAL-A11Y-002-submit-button-contrast.patch` | `core/themes/default_admin/src/Helper.php` yellow accent `#966705`; verify generated accent/button CSS effects. | Rerun applicability and contrast on an admin/default_admin form with yellow accent primary submit, not the stale `/action-link` selector path. |
| `DRUPAL-A11Y-005-language-switcher-contrast` | Proposed ready; rollup/per-patch eval says inconclusive/`patch-does-not-apply`. | Eval references `button.pcss.css`, while raw patch now targets `core/themes/default_admin/css/base/accents.pcss.css` and generated `accents.css`. Issue title says language switcher links, but patch changes button text variable. | `patches/a11y-DRUPAL-A11Y-005-language-switcher-contrast.patch` | `core/themes/default_admin/css/base/accents.pcss.css` / `accents.css`, pending issue/patch reconciliation. | Decide whether this is actually language-link contrast or yellow-accent button text contrast, then reroll/test against `a[hreflang]` pages. |
| `DRUPAL-A11Y-006-theme-switcher-landmark` | Proposed ready; rollup/per-patch eval says inconclusive, preflight corrupt. | Patch corrupt at line 15 plus no baseline target observed. Raw patch wraps the broad form main block in a `nav`, which may be too wide for a theme-switcher landmark fix. | `patches/a11y-DRUPAL-A11Y-006-theme-switcher-landmark.patch` | `core/themes/default_admin/templates/form/form-two-columns.html.twig`, but check the specific `.themeswitcher-form__form-item` render source first. | Regenerate cleanly and validate whether the landmark should wrap only the theme switcher, not the whole form main region. |
| `DRUPAL-A11Y-008-empty-table-headers` | Proposed ready; rollup/per-patch eval says inconclusive/`patch-target-file-missing`. | Eval looked for removed/wrong `core/modules/field/templates/field-multiple-value-form.html.twig`; current tree has `core/modules/system/templates/field-multiple-value-form.html.twig` and theme overrides. Raw patch targets generic `core/modules/system/templates/table.html.twig`, which may be too broad. | `patches/a11y-DRUPAL-A11Y-008-empty-table-headers.patch` | `core/lib/Drupal/Core/Field/FieldPreprocess.php` header array, plus `field-multiple-value-form.html.twig` overrides. | Reroll against the field-multiple table source, especially the empty second header cell, instead of patching all empty table headers globally. |
| `DRUPAL-A11Y-009-module-summary-names` | Proposed ready; May 7 rollup is stale/inconclusive/`patch-file-corrupt`; newer May 8 per-patch eval says PASS, eligible, targeted issue fixed. | Rollup JSON/MD is outdated relative to the per-patch evaluation. | `patches/a11y-DRUPAL-A11Y-009-module-summary-names.patch` | `core/themes/claro/templates/admin/system-modules-details.html.twig`, with parallel system/default_admin/stable9 templates in the patch. | Promote this out of hygiene triage into source-validated/actionable review, then update the rollup or local ledger so it no longer appears corrupt. |

## Sources Used

- `https://github.com/mgifford/drupal-core/blob/main/patches/PROPOSED-PATCHES.md`
- `https://github.com/mgifford/drupal-core/blob/main/reports/PATCH-EVALUATION-SUMMARY.md`
- `https://github.com/mgifford/drupal-core/blob/main/reports/PATCH-EVALUATION-SUMMARY.json`
- `https://github.com/mgifford/drupal-core/blob/main/reports/patches/INDEX.md`
- Per-patch reports under `https://github.com/mgifford/drupal-core/tree/main/patches/`

## Integration Note

This report updates source triage and next actions only. It does not prove local patch applicability, baseline reproduction, after-patch scans, broad regression scans, or manual checks.
