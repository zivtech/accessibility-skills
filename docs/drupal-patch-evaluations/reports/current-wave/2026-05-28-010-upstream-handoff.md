# Upstream Handoff Draft: DRUPAL-A11Y-010 Pager Heading Order

> Date: 2026-05-28
> Patch artifact: `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-010-heading-order-codex-content-pager-heading-level.patch`
> Scope: `/admin/content` pager heading only
> Upstream PR: https://github.com/mgifford/drupal-core/pull/10
> PR state as of 2026-05-31: open, not draft, merge state `CLEAN`, AccessLint pass

## Suggested Issue Comment

I traced the canonical `DRUPAL-A11Y-010` finding to the pager heading on the default `/admin/content` View.

The reproduced node is:

```html
<h4 id="pagination-heading" class="visually-hidden">Pagination</h4>
```

On `/admin/content`, this visually hidden pager heading follows the page `h1` without an intervening visible or structural `h2` for that section, so axe reports `heading-order` on `#pagination-heading`.

The attached patch changes the default Content View pager option from:

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

Important scope note: this patch changes the default optional View configuration in `core/modules/node/config/optional/views.view.content.yml` and adds `node_post_update_content_view_pager_heading_level()` for existing sites where the active Content view still has the old `h4` value. The post-update preserves non-`h4` active config values so customized heading levels are not overwritten.

Regression coverage included in the patch:

```text
core/modules/node/tests/src/Functional/NodeAdminTest.php
core/modules/node/tests/src/Kernel/NodePostUpdateTest.php
```

Local validation:

```text
php -l core/modules/node/node.post_update.php: pass
php -l core/modules/node/tests/src/Functional/NodeAdminTest.php: pass
php -l core/modules/node/tests/src/Kernel/NodePostUpdateTest.php: pass
SIMPLETEST_DB=sqlite://localhost/sites/simpletest/db/test-010.sqlite BROWSERTEST_OUTPUT_DIRECTORY=sites/simpletest/browser_output vendor/bin/phpunit -c core/phpunit.xml.dist core/modules/node/tests/src/Kernel/NodePostUpdateTest.php: OK (1 test, 6 assertions)
SIMPLETEST_BASE_URL=http://127.0.0.1:8888 SIMPLETEST_DB=sqlite://localhost/sites/simpletest/db/test-010-functional.sqlite BROWSERTEST_OUTPUT_DIRECTORY=sites/simpletest/browser_output vendor/bin/phpunit -c core/phpunit.xml.dist --filter testContentAdminPagerHeadingLevel core/modules/node/tests/src/Functional/NodeAdminTest.php: OK (1 test, 18 assertions)
vendor/bin/phpcs --standard=core/phpcs.xml.dist core/modules/node/node.post_update.php core/modules/node/tests/src/Functional/NodeAdminTest.php core/modules/node/tests/src/Kernel/NodePostUpdateTest.php: pass
git diff --check: pass
```

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
