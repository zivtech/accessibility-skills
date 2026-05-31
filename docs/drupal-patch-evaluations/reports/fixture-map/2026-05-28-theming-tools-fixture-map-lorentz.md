# Theming Tools Fixture Map - 2026-05-28

## Scope

Read-only map from current Drupal accessibility item IDs to fixture modules and deterministic routes in Mike Gifford's `mgifford/drupal-core` checkout.

## Summary

`modules/contrib/theming_tools` is the fixture layer for most current Drupal core accessibility evaluation routes. `.drupal-a11y-module-config.json` inventories Drupal core modules, but it does not encode per-item theming tools fixture mappings.

## Item Map

| Item | Fixture / Route | Notes |
|---|---|---|
| `DRUPAL-A11Y-001` | `theming_tools:imagefile`, `/contact/imagefile_file` | Route comes from `imagefile` contact-form setup. The fixture creates contact form fields with file defaults and grants contact form access. |
| `DRUPAL-A11Y-003` | `/admin/content`, `/admin/people`, or `theming_tools:table` `/table` | `/table` is the clean deterministic fixture because `TableTestForm` uses `#type: table` and `#tableselect: TRUE`. |
| `DRUPAL-A11Y-004` | `theming_tools:button`, `/buttons` | `ButtonTestForm` deliberately sets positive `tabindex => 1` on primary, danger, and default buttons. Current evaluator selector `button[tabindex]` is likely too narrow because important targets can render as `input#edit-submit[tabindex]`. |
| `DRUPAL-A11Y-007` | `theming_tools:message`, `/message/{type}` | Prefer `/message`, `/message/short`, or `/message/long` for deterministic status/warning/error/info messages. `/admin/appearance` and `/admin/modules` are more state-fragile. |
| `DRUPAL-A11Y-008` | `theming_tools:autocomplete`, `/autocomplete` | `AutocompleteForm` renders a multiple-value field widget table. Enable the `autocomplete` fixture module before evaluating; otherwise the route returns 404. |
| `DRUPAL-A11Y-010` | `/admin/content` pagination | Needs enough node rows to exceed the entity-list page limit. The pager heading comes from core pager preprocessing/templates; no theming tools route fully substitutes for the reported `/admin/content` condition. |
| `DRUPAL-A11Y-011/012` | `message`, `dialog`, `tab` | Source IDs conflict: upstream pattern report maps `011` to `landmark-unique` on `/message` and `012` to `empty-heading` on `/dialog` and `/tabs`. Local docs that call `011` "empty heading" should be reconciled. |
| Language-switcher items | `theming_tools:lang_hebrew` | Creates Hebrew language plus a language switcher block per theme. Useful for language-switcher contrast/name fixtures and multilingual `/admin/content` reproduction. |
| Haven items | Haven / Drupal CMS setup | HAVEN items are not covered by this Drupal core fixture layer. |

## Setup Implications

Enable the root fixture module plus only the needed submodules before evaluating these packets:

```bash
ddev drush en theming_tools imagefile button message table autocomplete dialog tab lang_hebrew actionlink pager themeswitcher -y
ddev drush cr
```

`imagefile` depends on contact and image support. `/admin/content` cases also need seeded content rows, and `DRUPAL-A11Y-010` specifically needs enough rows to trigger a pager.

The module-manager helper is generic. It does not preserve item-specific fixture mappings, and a reset-to-default flow could uninstall optional theming tools fixtures unless the eval harness explicitly preserves them.
