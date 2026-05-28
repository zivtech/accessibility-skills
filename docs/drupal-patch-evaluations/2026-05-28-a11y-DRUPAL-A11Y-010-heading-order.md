# Drupal Accessibility Evaluation Packet: DRUPAL-A11Y-010 Heading Order

> Status: BASELINE VERIFIED
> Prepared: 2026-05-28
> Purpose: Resolve the source route for `DRUPAL-A11Y-010-heading-order` before patch planning.

## Packet Header

| Field | Value |
|---|---|
| Item ID | `DRUPAL-A11Y-010-heading-order` |
| Status | `BASELINE VERIFIED` |
| Project/package | `mgifford/drupal-core` |
| Source status | `Core investigation` |
| Local runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| Route | `/admin/content` |
| Selector | `#pagination-heading` |
| Rule | `heading-order` |
| Triage report | `docs/drupal-patch-evaluations/reports/baseline-repair/2026-05-28-heading-order-route-triage-noether.md` |
| Focused baseline check | `docs/drupal-patch-evaluations/reports/baseline-repair/2026-05-28-focused-baseline-check-main.md` |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Baseline Evidence

The source report maps this item to `/admin/content` pagination, not `/admin/modules`:

```text
Rule: heading-order
Selector: #pagination-heading
HTML: <h4 id="pagination-heading"...>
Affected route: /admin/content
```

The by-path axe evidence includes `heading-order` on `/admin/content` and excludes it from `/admin/modules`.

Local focused check after seeding 60 page nodes:

```text
Route: /admin/content
Rule: heading-order
Selector: #pagination-heading
Selector count: 1
Violation nodes: 1
Observed HTML: <h4 id="pagination-heading" class="visually-hidden">Pagination</h4>
```

## Outcome

`BASELINE VERIFIED`

This verifies the baseline route and selector in the local runtime. It does not prove a patch approach. Next action: decide whether the pager heading hierarchy needs a core patch or a fixture/test-state correction, then draft the smallest candidate fix.
