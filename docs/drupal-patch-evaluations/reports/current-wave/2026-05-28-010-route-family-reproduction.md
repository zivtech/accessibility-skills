# DRUPAL-A11Y-010 Route Family Reproduction

> Date: 2026-05-28
> Runtime: `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime`
> Base URL: `http://drupal-core.ddev.site`
> Rule: `heading-order`

## Summary

`DRUPAL-A11Y-010` should not be patched as one generic heading-level change.

The canonical pattern report row maps `DRUPAL-A11Y-010` to `/admin/content` and `#pagination-heading`, but related heading-order evidence exists in three other route families. Local reproduction confirms the families are distinct:

| Family | Route | Selector | Current status |
|---|---|---|---|
| Pager | `/admin/content` | `#pagination-heading` | Reproduced |
| Datetime wrapper | `/admin/form_style`, `/contact/textform` | `.form-datetime-wrapper ... > h4` | Reproduced after fixture modules enabled |
| Multiple-value field | `/contact/field_cardinality_test`, `/contact/presuf_formatted`, `/contact/presuf_number` | multiple field table heading `h4` | Reproduced after fixture modules enabled |
| Admin block | `/cd-navigation/config` | `.panel__title` | Reproduced after fixture module enabled |

## Runtime Setup

The first focused run reproduced only `/admin/content`; the other historical routes returned 404 because their fixture modules were disabled. I enabled the required disposable-runtime fixture modules:

```bash
ddev drush pm:install -y form_style fieldcardinality presuf textform tt_navigation
ddev drush cache-rebuild
```

Drush also installed dependencies: `testfilters`, `textfixtures`, `datetime_range`, and `telephone`.

This changed only the disposable runtime state. It did not change tracked files in the review repo.

## Reproduced Families

### Pager

```text
Route: /admin/content
Status: 200
Selector count: #pagination-heading = 1
heading-order nodes: 1
HTML: <h4 id="pagination-heading" class="visually-hidden">Pagination</h4>
```

Likely source:

- `core/modules/node/config/optional/views.view.content.yml` sets `pagination_heading_level: h4`.
- `core/lib/Drupal/Core/Pager/PagerPreprocess.php` defaults pager headings to `h4` when no level is provided.
- Views pager defaults also use `h4`.

Patch boundary: pager heading level is partly a Views configuration/default problem, not only a Twig template problem.

### Datetime Wrapper

```text
Route: /admin/form_style
Status: 200
Selector count: .form-datetime-wrapper.form-item:nth-child(4) > h4 = 1
heading-order nodes: 1
HTML: <h4 class="form-item__label">Datelist</h4>

Route: /contact/textform
Status: 200
Selector count: #edit-timestamp-wrapper > .form-datetime-wrapper.form-item > h4 = 1
heading-order nodes: 1
HTML: <h4 class="form-item__label">Timestamp</h4>
```

Likely source:

- `core/modules/system/templates/datetime-wrapper.html.twig`
- `core/themes/claro/templates/datetime-wrapper.html.twig`
- `core/themes/default_admin/templates/form/datetime-wrapper.html.twig`
- related theme overrides in Olivero, Stable 9, and Starterkit.

Patch boundary: datetime wrappers are form element group labels. Changing them from `h4` to a different heading level may quiet axe, but the real design question is whether these should be headings at all or should expose group labeling through form semantics.

### Multiple-Value Field

```text
Route: /contact/field_cardinality_test
Status: 200
Selector count: #multitext-unlimited-values ... > h4 = 1
heading-order nodes: 1
HTML: <h4 class="form-item__label form-item__label--multiple-value-form">Multiple, unlimited text</h4>

Route: /contact/presuf_formatted
Status: 200
Selector count: #presuf-formatted-m-values ... .form-item__label--multiple-value-form = 1
heading-order nodes: 1
HTML: <h4 class="form-item__label form-item__label--multiple-value-form">Formatted multiple</h4>

Route: /contact/presuf_number
Status: 200
Selector count: #presuf-number-m-values ... > h4 = 1
heading-order nodes: 1
HTML: <h4 class="form-item__label form-item__label--multiple-value-form">Number multiple</h4>
```

Likely source:

- `core/lib/Drupal/Core/Field/FieldPreprocess.php` builds the multiple-value field table heading with `#tag => 'h4'`.
- Claro and Default Admin add `form-item__label--multiple-value-form` classes in their `preprocess_field_multiple_value_form()` hooks.

Patch boundary: this is a field API render contract. It should be patched and tested separately from pager or datetime wrapper changes.

### Admin Block

```text
Route: /cd-navigation/config
Status: 200
Selector count: historical selector for first column = 0
Actual heading-order node target: .layout-column.layout-column--half:nth-child(2) > .panel:nth-child(1) > .panel__title
heading-order nodes: 1
HTML: <h3 class="panel__title">People</h3>
```

Likely source:

- `core/modules/system/templates/admin-block.html.twig`
- `core/themes/default_admin/templates/admin/admin-block.html.twig`
- Stable 9 and related admin theme overrides.

Patch boundary: the historical selector drifted from first column to second column after runtime fixture state changed, but the render path remains the admin block panel title. This is a separate admin-page hierarchy issue.

## Recommendation

Treat the current `DRUPAL-A11Y-010` packet as the pager family only, because that is the canonical pattern-report row.

A pager-family-only candidate was tested after this split:

```text
Patch artifact: docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-010-heading-order-codex-content-pager-heading-level.patch
Change: core/modules/node/config/optional/views.view.content.yml pagination_heading_level h4 -> h2
Runtime active config update: ddev drush cset views.view.content display.default.display_options.pager.options.pagination_heading_level h2 -y
Focused result: /admin/content #pagination-heading rendered as h2; heading-order nodes 1 -> 0
Default axe after patch: remaining color-contrast, label-title-only, region
```

This is not yet a final upstream-ready verdict. The critic question is whether a default optional config change is sufficient, or whether existing installs need an update path or explicit scope note.

Open or track follow-on rows for:

- datetime wrapper heading-order;
- multiple-value field heading-order;
- admin block heading-order. Opened as `DRUPAL-A11Y-010-admin-block-heading-order` and upstream PR #15 on 2026-05-31.

The next patch should target one family at a time. The safest first candidate is the pager family, because `/admin/content` has a specific default Views config value and a narrow reproduced selector. The form-label families need design review before changing heading tags globally.

## Negative Space

This report is not claiming:

- that all four families should be fixed by changing headings to `h2`;
- that axe should be treated as the only arbiter of the correct form-label semantics;
- that the disabled fixture routes were live baseline failures before the fixture modules were enabled;
- that `/admin/modules` is part of the canonical `DRUPAL-A11Y-010` row.
