# Upstream Handoff Draft: LABEL-IN-NAME-004 Filter Format Configure Link

> Date: 2026-05-31
> Patch artifact: `docs/drupal-patch-evaluations/patches/a11y-LABEL-IN-NAME-004-filter-format-aria-label-codex-configure-link-label.patch`
> Scope: `/admin/config/content/formats` Configure operation links
> Upstream PR: https://github.com/mgifford/drupal-core/pull/11
> PR state as of 2026-05-31: open, not draft, merge state `CLEAN`, AccessLint pass

## Suggested Issue Comment

I rerolled the `LABEL-IN-NAME-004-filter-format-aria-label` patch against current `mgifford/drupal-core` `main`.

The issue is the filter format overview's operation link:

```html
<a href="/admin/config/content/formats/manage/basic_html" aria-label="Edit Basic HTML">Configure</a>
```

`EntityListBuilder` creates the edit operation with an accessible name beginning with `Edit`. `FilterFormatListBuilder` then changes the visible operation title to `Configure`, leaving the visible label out of the accessible name. That creates a WCAG 2.5.3 Label in Name mismatch for speech-input users and for anyone relying on consistent visible and programmatic naming.

The patch keeps the accessible name aligned with the overridden operation title:

```text
Configure Basic HTML
Configure Restricted HTML
Configure Full HTML
Configure Plain text
```

Regression coverage included in the patch:

```text
core/modules/filter/tests/src/Functional/FilterAdminTest.php
```

Local validation:

```text
php -l core/modules/filter/src/FilterFormatListBuilder.php: pass
php -l core/modules/filter/tests/src/Functional/FilterAdminTest.php: pass
git diff --check: pass
vendor/bin/phpcs --standard=core/phpcs.xml.dist core/modules/filter/src/FilterFormatListBuilder.php core/modules/filter/tests/src/Functional/FilterAdminTest.php: pass
SIMPLETEST_BASE_URL=http://drupal-core.ddev.site SIMPLETEST_DB=mysql://db:db@db/db BROWSERTEST_OUTPUT_DIRECTORY=/tmp vendor/bin/phpunit -c core --filter testFilterEnableAndDisable core/modules/filter/tests/src/Functional/FilterAdminTest.php: OK (1 test, 27 assertions)
```

Keyboard-user smoke evidence:

```text
Route: /admin/config/content/formats
Tool: Playwright with real page.keyboard.press('Tab') and page.keyboard.press('Enter')
Tab reached all 6 Configure links in sequence.
Each focused Configure link had an accessible name starting with visible text "Configure".
Enter on the focused Configure link navigated to its manage route.
axe rule label-content-name-mismatch after patch: 0 violations.
```

What this patch does not claim:

- It does not claim NVDA, JAWS, VoiceOver, or voice-control verification.
- It does not change the operation URL or visible text.
- It does not address unrelated existing findings on the filter format overview page.
