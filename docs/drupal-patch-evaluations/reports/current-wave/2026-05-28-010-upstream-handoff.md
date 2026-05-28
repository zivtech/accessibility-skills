# Upstream Handoff Draft: DRUPAL-A11Y-010 Pager Heading Order

> Date: 2026-05-28
> Patch artifact: `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-010-heading-order-codex-content-pager-heading-level.patch`
> Scope: `/admin/content` pager heading only

## Suggested Issue Comment

I traced the canonical `DRUPAL-A11Y-010` finding to the pager heading on the default `/admin/content` View.

The reproduced node is:

```html
<h4 id="pagination-heading" class="visually-hidden">Pagination</h4>
```

On `/admin/content`, this visually hidden pager heading follows the page `h1` without an intervening visible or structural `h2` for that section, so axe reports `heading-order` on `#pagination-heading`.

The attached candidate changes the default Content View pager option from:

```yaml
pagination_heading_level: h4
```

to:

```yaml
pagination_heading_level: h2
```

Focused local evidence:

| Route | Selector | Before | After |
|---|---|---|---|
| `/admin/content` | `#pagination-heading` | `h4`, 1 `heading-order` node | `h2`, 0 `heading-order` nodes |

Default axe after-patch scan on `/admin/content` did not report `heading-order`. Remaining findings were unrelated existing `color-contrast`, `label-title-only`, and `region` issues.

Important scope note: this patch changes the default optional View configuration in `core/modules/node/config/optional/views.view.content.yml`. In local validation, I also updated the active runtime config to match the patch:

```bash
ddev drush cset views.view.content display.default.display_options.pager.options.pagination_heading_level h2 -y
ddev drush cache-rebuild
```

That means the current patch primarily covers new/default config installs. If the issue is expected to remediate already-installed sites, it may need an update path or a separate config update strategy.

I also checked related heading-order evidence and confirmed it splits into separate render families:

- datetime wrapper headings;
- multiple-value field headings;
- admin block panel headings.

Those are not fixed by this pager patch and should be tracked separately. They involve different render contracts and should not be folded into a single mechanical heading-level change.

What this patch does not claim:

- It does not fix datetime wrapper heading order.
- It does not fix multiple-value field heading order.
- It does not fix admin block panel heading order.
- It does not claim that all pager headings in core should be `h2`.
- It does not remediate existing active config unless an update path or equivalent strategy is added.
