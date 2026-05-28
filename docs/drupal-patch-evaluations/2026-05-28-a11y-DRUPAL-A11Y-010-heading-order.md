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
| Patch candidate | `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-010-heading-order-codex-content-pager-heading-level.patch` |
| Triage report | `docs/drupal-patch-evaluations/reports/baseline-repair/2026-05-28-heading-order-route-triage-noether.md` |
| Focused baseline check | `docs/drupal-patch-evaluations/reports/baseline-repair/2026-05-28-focused-baseline-check-main.md` |
| Route-family reproduction | `docs/drupal-patch-evaluations/reports/current-wave/2026-05-28-010-route-family-reproduction.md` |
| Critic gate | `docs/drupal-patch-evaluations/reports/current-wave/2026-05-28-010-pager-candidate-critic-gate.md` |
| Upstream handoff draft | `docs/drupal-patch-evaluations/reports/current-wave/2026-05-28-010-upstream-handoff.md` |
| Follow-on backlog | `docs/drupal-patch-evaluations/reports/current-wave/2026-05-28-010-follow-on-family-backlog.md` |
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

This verifies the canonical baseline route and selector in the local runtime.

Follow-up reproduction confirmed that related `heading-order` evidence splits into four render families:

| Family | Route examples | Likely source |
|---|---|---|
| Pager | `/admin/content` | Views pager config/defaults and `PagerPreprocess` |
| Datetime wrapper | `/admin/form_style`, `/contact/textform` | `datetime-wrapper.html.twig` and theme overrides |
| Multiple-value field | `/contact/field_cardinality_test`, `/contact/presuf_formatted`, `/contact/presuf_number` | `FieldPreprocess::preprocessFieldMultipleValueForm()` |
| Admin block | `/cd-navigation/config` | `admin-block.html.twig` and admin theme overrides |

## Pager Patch Candidate

Candidate fix: change the `/admin/content` View pager heading level from `h4` to `h2` in `core/modules/node/config/optional/views.view.content.yml`.

Targeted after-patch evidence in the disposable runtime:

```text
Route: /admin/content
Selector: #pagination-heading
Rendered heading: <h2 id="pagination-heading" class="visually-hidden">Pagination</h2>
heading-order nodes after candidate: 0
```

Default axe after-patch scan on `/admin/content`:

```text
heading-order: 0
remaining unrelated rules: color-contrast, label-title-only, region
```

Critic verdict: `REVISE-BEFORE-UPSTREAM`.

Boundary: this patch changes default optional View config. The local after-patch validation also updated active runtime config with Drush. Existing sites may need an update path or explicit test-plan note; the patch artifact alone primarily covers new/default config installs.

Keep `DRUPAL-A11Y-010` scoped to the pager family unless the tracking row is intentionally broadened. The other families need separate rows or explicit issue comments; a single mechanical heading-level patch would obscure different render contracts.

Next action: decide whether to post the narrow upstream handoff as a scoped default-config patch, add an update path, or broaden to pager/Views defaults with tests.
