# DRUPAL-A11Y-010 Heading Order Route Triage

> Agent: Noether
> Mode: read-only explorer
> Date: 2026-05-28
> Scope: Resolve `/admin/modules` versus `/admin/content` for heading-order evidence.

## Verdict

The strongest current evidence points to `/admin/content` pagination, specifically `#pagination-heading`. Do not treat `/admin/modules` as the failing heading-order route; current by-path evidence shows `summary-name` and landmark failures there, but not `heading-order`.

## Recommended Status

`BASELINE VERIFIED` for the baseline route and selector only. Patch decision remains open.

## Evidence

- `docs/drupal-patch-evaluations/STATUS.md` asked to resolve `/admin/modules` versus `/admin/content`.
- `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/reports/PATTERN-REPORT-latest.md:835` maps `DRUPAL-A11Y-010` to `heading-order`, selector `#pagination-heading`, affected URL `/admin/content`.
- `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/reports/pattern-report-2026-05-06.json:4574` has raw pattern data: `ruleId: heading-order`, `selectorKey: #pagination-heading`, and `html: <h4 id="pagination-heading"...>`.
- `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/reports/axe-results/latest/by-path.json:3` shows `/admin/content` includes `heading-order`.
- `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/reports/axe-results/latest/by-path.json:180` shows `/admin/modules` rule IDs exclude `heading-order`.

## Next Action

Create a local packet for `DRUPAL-A11Y-010` around `/admin/content` with enough seeded rows to render the pager, then run a focused baseline axe check on `#pagination-heading`.
