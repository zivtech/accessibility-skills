# Upstream Handoff Draft: DRUPAL-A11Y-012 Empty Heading Elements

> Date: 2026-05-28
> Patch artifact: `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-012-empty-heading-elements-codex-filter-tips-preprocess.patch`

## Suggested Issue Comment

I traced the empty headings on the theming tools `/dialog` and `/tabs` fixture routes to the `filter_tips` theme hook data shape.

The `filter-tips.html.twig` templates expect each format bucket to expose normalized `tip.name`, `tip.list`, and attributes. The raw data from `FilterThemeHooks::getFilterTips()` is keyed by text format label and did not have a core preprocess step normalizing that shape before template rendering. In Claro and Default Admin, that can render empty long-tip headings such as `<h3></h3>`.

This patch adds `FilterThemeHooks::preprocessFilterTips()` as the initial preprocess callback for `filter_tips`. It normalizes:

- the format label into `tip.name`;
- the filter-tip items into `tip.list`;
- format-level attributes used by Claro/Default Admin;
- per-item attributes used by Claro/Default Admin.

Focused before/after axe evidence:

| Route | Before `empty-heading` nodes | After `empty-heading` nodes |
|---|---:|---:|
| `/dialog` | 4 | 0 |
| `/tabs` | 4 | 0 |
| `/tabs/format/plain_text` | 1 | 0 |

After the patch, the formerly empty headings render text format names such as `Basic HTML`, `Restricted HTML`, `Full HTML`, and `Plain text`.

Regression coverage included in the patch:

```text
core/modules/filter/tests/src/Kernel/FilterTipsRenderTest.php
```

The test covers single-format long tips and multi-format long tips rendered through Claro, plus direct preprocess normalization of `tip.name`, format-level attributes, and item-level attributes.

Local validation:

```text
php -l core/modules/filter/src/Hook/FilterThemeHooks.php: pass
php -l core/modules/filter/tests/src/Kernel/FilterTipsRenderTest.php: pass
phpunit core/modules/filter/tests/src/Kernel/FilterTipsRenderTest.php: OK (3 tests, 10 assertions)
```

I also ran broader axe checks on the affected routes. The patch did not introduce new axe rule families. Remaining `region` and `heading-order` findings on those pages were present before this patch and are not addressed here.

What this patch does not claim:

- It does not resolve the separate `heading-order` findings.
- It does not resolve existing `region` findings.
- It is not a full-site accessibility closure; it is scoped to the `filter_tips` empty-heading regression.
