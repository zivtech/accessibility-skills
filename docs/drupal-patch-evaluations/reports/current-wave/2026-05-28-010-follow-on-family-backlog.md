# Follow-On Backlog: Heading-Order Families Split From DRUPAL-A11Y-010

> Date: 2026-05-28
> Runtime: `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime`
> Purpose: Preserve non-pager heading-order evidence without broadening the canonical `DRUPAL-A11Y-010` pager row.

## Why This Exists

The canonical `DRUPAL-A11Y-010` row maps to `/admin/content` and `#pagination-heading`.

During route-family reproduction, three additional heading-order families were confirmed after enabling their fixture modules in the disposable runtime. They are real local findings, but they should not be silently folded into the pager patch. Each has a different render contract.

## Fixture Modules Enabled

```bash
ddev drush pm:install -y form_style fieldcardinality presuf textform tt_navigation
ddev drush cache-rebuild
```

Drush also installed dependencies: `testfilters`, `textfixtures`, `datetime_range`, and `telephone`.

## Family 1: Datetime Wrapper Headings

Routes:

- `/admin/form_style`
- `/contact/textform`

Reproduced nodes:

```html
<h4 class="form-item__label">Datelist</h4>
<h4 class="form-item__label">Timestamp</h4>
```

Likely render sources:

- `core/modules/system/templates/datetime-wrapper.html.twig`
- `core/themes/claro/templates/datetime-wrapper.html.twig`
- `core/themes/default_admin/templates/form/datetime-wrapper.html.twig`
- related Olivero, Stable 9, and Starterkit overrides.

Open question:

Are these labels supposed to be headings, or should the datetime component expose group labeling through form semantics instead? A simple `h4` to `h2` change would satisfy axe in this fixture, but it may be the wrong semantic fix.

## Family 2: Multiple-Value Field Headings

Status update 2026-05-31: split out and opened upstream as PR #16.

```text
Packet: docs/drupal-patch-evaluations/2026-05-31-a11y-DRUPAL-A11Y-010-multiple-value-field-heading-order.md
Patch: docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-010-multiple-value-field-heading-order-codex-multiple-value-field-label.patch
PR: https://github.com/mgifford/drupal-core/pull/16
```

Routes:

- `/contact/field_cardinality_test`
- `/contact/presuf_formatted`
- `/contact/presuf_number`

Reproduced nodes:

```html
<h4 class="form-item__label form-item__label--multiple-value-form">Multiple, unlimited text</h4>
<h4 class="form-item__label form-item__label--multiple-value-form">Formatted multiple</h4>
<h4 class="form-item__label form-item__label--multiple-value-form">Number multiple</h4>
```

Likely render source:

- `core/lib/Drupal/Core/Field/FieldPreprocess.php` builds the table heading with `#tag => 'h4'`.
- Claro and Default Admin add label classes in `preprocess_field_multiple_value_form()`.

Open question:

Should the label stay in the existing table header cell as non-heading text, or should field table labeling be redesigned more broadly in a follow-up?

## Family 3: Admin Block Panel Headings

Status update 2026-05-31: split out and opened upstream as PR #15.

```text
Packet: docs/drupal-patch-evaluations/2026-05-31-a11y-DRUPAL-A11Y-010-admin-block-heading-order.md
Patch: docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-010-admin-block-heading-order-codex-admin-block-heading-level.patch
PR: https://github.com/mgifford/drupal-core/pull/15
```

Route:

- `/cd-navigation/config`

Reproduced node:

```html
<h3 class="panel__title">People</h3>
```

Likely render sources:

- `core/modules/system/templates/admin-block.html.twig`
- `core/themes/default_admin/templates/admin/admin-block.html.twig`
- Stable 9 and related admin theme overrides.

Open question:

Should admin block titles be `h2` under admin overview page `h1` headings, or should admin pages introduce a higher-level section wrapper before panel titles?

## Recommended Tracking

Create separate follow-on rows or issue comments for:

- `heading-order`: datetime wrapper headings;
- `heading-order`: multiple-value field headings. Done locally as `DRUPAL-A11Y-010-multiple-value-field-heading-order`, pending upstream review in PR #16;
- `heading-order`: admin block panel headings. Done locally as `DRUPAL-A11Y-010-admin-block-heading-order`, pending upstream review in PR #15.

Do not patch these inside the current pager candidate unless the upstream issue is explicitly broadened and the patch includes tests for each render family.
