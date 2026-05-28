# Patch Evaluation Report: a11y-LABEL-IN-NAME-004-filter-format-aria-label-codex-selector-hint-label-004

**Generated:** 2026-05-28 at 1:28:39 PM

## Summary

- **Description:** Fix label-in-name violation for filter format configure link
- **WCAG Criteria:** 2.5.3 (A)
- **Affected Rules:** label-in-name (axe: label-content-name-mismatch)
- **Pattern Source:** reports/pattern-report-2026-05-06.json
- **Pattern Source (Markdown):** reports/pattern-report-2026-05-06.md
- **Pattern ID Match Type:** runtime-generated-only
- **Matched Pattern IDs (pattern source):** none
- **Generated Pattern IDs (current run):** DRU-90c99d19
- **Status:** ✅ **PASS** — Patch resolves targeted issues without introducing new violations
- **Outcome Reason:** `targeted-issues-fixed-without-regressions`
- **Eligible For Patch Recommendation:** yes
- **Requested color mode:** light
- **Patch preflight applicability:** applicable
- **Drupal initial state capture:** complete
- **Enabled modules (captured):** 53
- **Enabled modules hash:** e0133986f3906e2439787af017dcbe0cf6e13cf9cb9271c69393741da46673dd
- **Core extension hash:** 31b259471c42afbd3e30d71ad307fb06ea209bbb58152af62111117b20cec91c
- **Pattern source modified:** 2026-05-28T16:34:13.257Z
- **Pattern source age (hours):** 0.91
- **Case generation mode:** fallback-config-testCases
- **Case generation count:** 1
- **Case generation fallback reason:** no-configured-pattern-ids
- **Page load HTTP statuses (baseline):** 200x1
- **Pages loaded successfully (2xx):** 1/1
- **Pages not loaded as 2xx:** 0/1
- **ID consistency issues:** patterns=0, instances=0
- **Pattern observed before patch attempt:** yes
- **Baseline observed instances:** 1
- **Fixed instances after patch:** 1
- **Remaining instances after patch:** 0

### Replication Instructions

Use the following deterministic steps to reproduce this exact evaluation run:

- Setup: `ddev drush cset system.theme default olivero -y`
- Setup: `ddev drush cset system.theme admin claro -y`
- Setup: `ddev drush cache-rebuild`
- Flow: Navigate to each test case URL under requested conditions and capture baseline evidence.
- Flow: Apply patch with: git apply "/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/patches/a11y-LABEL-IN-NAME-004-filter-format-aria-label.patch"
- Flow: Clear Drupal cache with: ddev drush cache-rebuild
- Flow: Revisit same URL + conditions and capture post-patch evidence.
- Flow: Revert patch with: git apply -R "/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/patches/a11y-LABEL-IN-NAME-004-filter-format-aria-label.patch"
- Variant ID: `codex-selector-hint-label-004`
- Expected proof: Problem must be observed before patch and not observed after patch under the same recorded conditions.

### Drupal Initial State Snapshot

- **Captured at:** 2026-05-28T17:28:29.552Z
- **Capture status:** complete
- **Default theme:** olivero
- **Admin theme:** claro
- **Enabled modules count:** 53
- **Enabled modules hash (sha256):** e0133986f3906e2439787af017dcbe0cf6e13cf9cb9271c69393741da46673dd
- **Core extension hash (sha256):** 31b259471c42afbd3e30d71ad307fb06ea209bbb58152af62111117b20cec91c
- **Core extension modules hash (sha256):** 8bb798d045e892a1aaab3573344f1d0b647d655676db6ee85261d446a4942963
- **Core extension themes hash (sha256):** 30bfe9325153ff420bc86f2bc9e447ecd63a74f52d8d0e329bf8420f15e9c0a3
- **Drush status:** {"drupal-version":"12.0-dev","uri":"https://drupal-core.ddev.site:33001","db-driver":"mysql","db-hostname":"db","db-port":3306,"db-username":"db","db-password":"db","db-name":"db","db-status":"Connected","bootstrap":"Successful","theme":"olivero","admin-theme":"claro","php-bin":"/usr/bin/php8.5","php-conf":["/etc/php/8.5/cli/php.ini"],"php-os":"Linux","php-version":"8.5.5","drush-script":"/var/www/html/vendor/bin/drush.php","drush-version":"14.9999999.9999999.9999999-dev","drush-temp":"/tmp","drush-conf":[],"drush-alias-files":[],"alias-searchpaths":[],"install-profile":"standard","root":"/var/www/html","drupal-settings-file":"sites/default/settings.php","site":"sites/default","themes":"sites/all/themes","modules":"sites/all/modules","files":"sites/default/files","temp":"/tmp","config-sync":"sites/default/files/sync","config":"sites/default/files/sync","%paths":{"%root":"/var/www/html","%site":"sites/default","%modules":"sites/all/modules","%themes":"sites/all/themes","%config-sync":"sites/default/files/sync","%config":"sites/default/files/sync","%files":"sites/default/files","%temp":"/tmp"}}
- **Enabled modules sample (first 40):** actionlink, announcements_feed, automated_cron, big_pipe, block, block_content, breakpoint, button, ckeditor5, comment, config, contact, contextual, datetime, dblog, dialog, dynamic_page_cache, editor, field, field_ui, file, filter, help, image, imagefile, lang_hebrew, language, layout_builder, layout_discovery, link, locale, menu_link_content, menu_ui, message, mysql, navigation, node, options, page_cache, pager
- **Commands used:**
  - ✅ `ddev drush pm:list --type=module --status=enabled --format=json`
  - ✅ `ddev drush cget system.theme --format=json`
  - ✅ `ddev drush cget core.extension --format=json`
  - ✅ `ddev drush status --format=json`

### Pattern Source Candidates

| Path | Modified |
|---|---|
| reports/pattern-report-2026-05-06.json | 2026-05-28T16:34:13.257Z |

### Validation Proof (Before/After)

This run captured the target violation before patch application and confirmed it was absent after patch application under the same recorded conditions.

- Baseline observed: 1
- Fixed after patch: 1
- Remaining after patch: 0
- New violations introduced: 0

### Instance ID Coverage

- **Targeted instance IDs:** 1
- **Seen before patch:** 1
- **Fixed instances:** 1
- **Remaining instances:** 0
- **Not observed in baseline:** 0

| Instance ID | Pattern ID | Rule | Path | Status | Before IDs | After IDs |
|---|---|---|---|---|---|---|
| DRU-bb2f2dd6 | DRU-90c99d19 | label-content-name-mismatch | /admin/config/content/formats | fixed | DRU-bb2f2dd6, DRU-8a215924, DRU-fb14af17, DRU-8701c8e8 | - |

### Violation Counts

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Total violations** | 5 | 1 | -4 |

### Fixed Rules

- `label-content-name-mismatch`: 4 → 0 (−4)

---

## Test Cases

### Test 1: /admin/config/content/formats

**URL:** `http://drupal-core.ddev.site:33000/admin/config/content/formats`

**Elements tested:** table a:has-text("Configure")

**Conditions:**
- Requested: {"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}}
- Before: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}
- After: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}

**Authentication:**
- Before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"loginAttempt":null}

#### Before Patch

- **Total violations:** 5
- **By rule:**
  - `region`: 1
  - `label-content-name-mismatch`: 4

#### After Patch

- **Total violations:** 1
- **By rule:**
  - `region`: 1

---

## Screenshots

Captured 2 screenshot(s) for this run. See the reports directory.

## HTML Snapshots

Captured 2 HTML snapshot(s) for this run.
