# Critic Gate: DRUPAL-A11Y-010 Pager Heading Order Candidate

> Date: 2026-05-28
> Reviewed artifact: `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-010-heading-order-codex-content-pager-heading-level.patch`
> Verdict: `REVISE-BEFORE-UPSTREAM`

## Status Recommendation

Keep `DRUPAL-A11Y-010-heading-order` at `BASELINE VERIFIED`.

The pager-family candidate is useful and targeted, but it should not be marked `VERIFIED` yet. It fixes the focused runtime node after active config is changed, but the patch artifact currently changes only default optional Views config.

## Evidence Reviewed

- Canonical pattern row: `/admin/content`, selector `#pagination-heading`, `heading-order`.
- Local baseline: `#pagination-heading` rendered as `<h4 ...>Pagination</h4>` and produced one `heading-order` node.
- Candidate patch: `core/modules/node/config/optional/views.view.content.yml` changes `pagination_heading_level: h4` to `h2`.
- Runtime validation also updated active config with:

```bash
ddev drush cset views.view.content display.default.display_options.pager.options.pagination_heading_level h2 -y
ddev drush cache-rebuild
```

- Focused after-patch result: `#pagination-heading` rendered as `<h2 ...>Pagination</h2>` and `heading-order` went to zero on `/admin/content`.
- Default axe after-patch result on `/admin/content`: remaining `color-contrast`, `label-title-only`, and `region`; no remaining `heading-order`.

## Findings

The candidate addresses the canonical scanner row without touching unrelated heading families. That is the right scope for the first `010` patch lane.

The weak point is upstream packaging. A default optional config change affects new/default config installs. It does not automatically update existing active `views.view.content` config on already-installed sites. The local proof needed a Drush active config change, which is exactly the gap an upstream reviewer may challenge.

There is also a broader pager-default question. Core pager preprocessing and Views pager defaults still use `h4` when no explicit level is set. This candidate does not claim to solve all pager heading-order cases; it only addresses the reported `/admin/content` default View.

## Required Revision Before Upstream

Choose one of these paths before filing as a patch-ready upstream candidate:

1. Keep the patch narrow and state explicitly that it fixes the default `/admin/content` View configuration for new installs/default config, with test evidence based on active config adjusted to the same value.
2. Add an update path or config update strategy for existing sites if the upstream issue is expected to remediate existing installations.
3. Broaden the pager-family patch to review core pager and Views pager defaults, with corresponding test coverage, if the intended claim is generic pager heading-order remediation.

## Negative Space

This review is not claiming:

- that the datetime wrapper, multiple-value field, or admin block families are fixed;
- that every core View pager heading should be changed to `h2`;
- that a default config change alone remediates existing installed sites;
- that remaining `color-contrast`, `label-title-only`, or `region` issues on `/admin/content` are related to this candidate.
