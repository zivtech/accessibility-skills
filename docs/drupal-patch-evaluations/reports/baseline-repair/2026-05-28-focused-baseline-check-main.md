# Focused Baseline Check: DRUPAL-A11Y-010 and DRUPAL-A11Y-012

> Runner: Main
> Date: 2026-05-28
> Runtime: `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime`
> Base URL: `http://drupal-core.ddev.site:33000`

## Runtime Setup

Seeded admin content so `/admin/content` renders pagination:

```bash
ddev drush php:eval 'use Drupal\node\Entity\Node; $count = 0; for ($i = 1; $i <= 60; $i++) { $node = Node::create(["type" => "page", "title" => "A11Y pager seed " . $i, "status" => 1]); $node->save(); $count++; } print "created $count nodes\n";'
ddev drush cache-rebuild
```

Result:

```text
created 60 nodes
Cache rebuild complete.
```

## DRUPAL-A11Y-010 Heading Order

Focused Playwright + axe-core check:

```text
Route: /admin/content
Rule: heading-order
Selector: #pagination-heading
Selector count: 1
Violation nodes: 1
```

Observed failing node:

```html
<h4 id="pagination-heading" class="visually-hidden">Pagination</h4>
```

Failure summary:

```text
Heading order invalid
```

## DRUPAL-A11Y-012 Empty Heading Elements

Focused Playwright + axe-core check:

```text
Route: /dialog
Rule: empty-heading
Heading selector count: 14
Violation nodes: 4
```

Observed failing nodes were empty `h3` elements such as:

```html
<h3></h3>
```

Focused Playwright + axe-core check:

```text
Route: /tabs
Rule: empty-heading
Heading selector count: 14
Violation nodes: 4
```

Observed failing nodes were empty `h3` elements such as:

```html
<h3></h3>
```

## Interpretation

Both items now have local baseline evidence in the disposable runtime. Neither has after-patch evidence or a proposed patch path yet, so neither is `VERIFIED`.
