# Patch Evaluation Report: a11y-DRUPAL-A11Y-003-select-all-checkbox-label-codex-select-all-aria-label-003

**Generated:** 2026-05-30 at 10:37:19 PM

## Summary

- **Description:** Add aria-label to select-all checkboxes in tables
- **WCAG Criteria:** 1.3.1 (A)
- **Affected Rules:** label, label-title-only
- **Pattern Source:** reports/pattern-report-2026-05-06.json
- **Pattern Source (Markdown):** reports/pattern-report-2026-05-06.md
- **Target Pattern IDs:** DRU-987EB788
- **Pattern ID Match Type:** source-pattern-matched
- **Matched Pattern IDs (pattern source):** DRU-987EB788
- **Generated Pattern IDs (current run):** DRU-987EB788
- **Status:** ✅ **PASS** — Patch resolves targeted issues without introducing new violations
- **Outcome Reason:** `targeted-issues-fixed-without-regressions`
- **Eligible For Patch Recommendation:** yes
- **Requested color mode:** light
- **Patch preflight applicability:** applicable
- **Drupal initial state capture:** complete
- **Enabled modules (captured):** 62
- **Enabled modules hash:** 2d83d0e6db0770aba0ff204c019cb0083815a23c6a682d4fd91a4486c560a892
- **Core extension hash:** 9bed4a03680499fbfeb08f353ac83775bccbd7e65a9352f00129bd33fad3c892
- **Pattern source modified:** 2026-05-28T16:34:13.257Z
- **Pattern source age (hours):** 58.05
- **Case generation mode:** pattern-report-derived
- **Case generation count:** 2
- **Page load HTTP statuses (baseline):** 200x2
- **Pages loaded successfully (2xx):** 2/2
- **Pages not loaded as 2xx:** 0/2
- **Skip reasons:** baseline-target-not-observedx1
- **ID consistency issues:** patterns=1, instances=0
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
- Flow: Apply patch with: git apply "/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/patches/a11y-DRUPAL-A11Y-003-select-all-checkbox-label.patch"
- Flow: Clear Drupal cache with: ddev drush cache-rebuild
- Flow: Revisit same URL + conditions and capture post-patch evidence.
- Flow: Revert patch with: git apply -R "/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/patches/a11y-DRUPAL-A11Y-003-select-all-checkbox-label.patch"
- Variant ID: `codex-select-all-aria-label-003`
- Expected proof: Problem must be observed before patch and not observed after patch under the same recorded conditions.

### Drupal Initial State Snapshot

- **Captured at:** 2026-05-31T02:36:58.297Z
- **Capture status:** complete
- **Default theme:** olivero
- **Admin theme:** claro
- **Enabled modules count:** 62
- **Enabled modules hash (sha256):** 2d83d0e6db0770aba0ff204c019cb0083815a23c6a682d4fd91a4486c560a892
- **Core extension hash (sha256):** 9bed4a03680499fbfeb08f353ac83775bccbd7e65a9352f00129bd33fad3c892
- **Core extension modules hash (sha256):** 563021e81a804826aa26f8246802a8b18b11cab28512141f0a3ac32d68fe6e01
- **Core extension themes hash (sha256):** 30bfe9325153ff420bc86f2bc9e447ecd63a74f52d8d0e329bf8420f15e9c0a3
- **Drush status:** {"drupal-version":"12.0-dev","uri":"https://drupal-core.ddev.site","db-driver":"mysql","db-hostname":"db","db-port":3306,"db-username": "[REDACTED]","db-password": "[REDACTED]","db-name":"db","db-status":"Connected","bootstrap":"Successful","theme":"olivero","admin-theme":"claro","php-bin":"/usr/bin/php8.5","php-conf":["/etc/php/8.5/cli/php.ini"],"php-os":"Linux","php-version":"8.5.5","drush-script":"/var/www/html/vendor/bin/drush.php","drush-version":"14.9999999.9999999.9999999-dev","drush-temp":"/tmp","drush-conf":[],"drush-alias-files":[],"alias-searchpaths":[],"install-profile":"standard","root":"/var/www/html","drupal-settings-file":"sites/default/settings.php","site":"sites/default","themes":"sites/all/themes","modules":"sites/all/modules","files":"sites/default/files","temp":"/tmp","config-sync":"sites/default/files/sync","config":"sites/default/files/sync","%paths":{"%root":"/var/www/html","%site":"sites/default","%modules":"sites/all/modules","%themes":"sites/all/themes","%config-sync":"sites/default/files/sync","%config":"sites/default/files/sync","%files":"sites/default/files","%temp":"/tmp"}}
- **Enabled modules sample (first 40):** actionlink, announcements_feed, automated_cron, big_pipe, block, block_content, breakpoint, button, ckeditor5, comment, config, contact, contextual, datetime, datetime_range, dblog, dialog, dynamic_page_cache, editor, field, field_ui, fieldcardinality, file, filter, form_style, help, image, imagefile, lang_hebrew, language, layout_builder, layout_discovery, link, locale, menu_link_content, menu_ui, message, mysql, navigation, node
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

### Pattern Coverage (From Scan Report)

- **Targeted patterns:** 1
- **Patterns seen before patch:** 1
- **Fully fixed patterns:** 1
- **Partially fixed patterns:** 0
- **Unchanged patterns:** 0

| Pattern ID | Rule | Paths (sample) | Before | After | Status |
|---|---|---|---:|---:|---|
| DRU-987EB788 | label-title-only | /admin/content, /admin/people, /table | 1 | 0 | fully-fixed |

### Instance ID Coverage

- **Targeted instance IDs:** 5
- **Seen before patch:** 1
- **Fixed instances:** 1
- **Remaining instances:** 0
- **Not observed in baseline:** 4

| Instance ID | Pattern ID | Rule | Path | Status | Before IDs | After IDs |
|---|---|---|---|---|---|---|
| DRU-528caf9d | DRU-987EB788 | label-title-only | /admin/content | fixed | DRU-528caf9d | - |
| DRU-338f4951 | DRU-987EB788 | label-title-only | /admin/content | not-observed | - | - |
| DRU-59f64256 | DRU-987EB788 | label-title-only | /admin/content | not-observed | - | - |
| DRU-71b9023a | DRU-987EB788 | label-title-only | /admin/content | not-observed | - | - |
| DRU-5b7a8b3e | DRU-987EB788 | label-title-only | /admin/content | not-observed | - | - |

### Violation Counts

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Total violations** | 5 | 2 | -3 |

### Fixed Rules

- `label-title-only`: 1 → 0 (−1)

---

## Test Cases

### Test 1: /admin/content

**URL:** `http://drupal-core.ddev.site/admin/content`

**Elements tested:** input[title="Select all rows in this table"], .gin--sticky-table-header > thead > tr > .select-all.gin--sticky-bulk-select > .form-checkbox.form-boolean[title="Select all rows in this table"], .views-table > thead > tr > .select-all.gin--sticky-bulk-select > .form-checkbox.form-boolean[title="Select all rows in this table"], #edit-checkbox-hidden-label-value, #edit-checkbox-hidden-label-disabled-value

**Conditions:**
- Requested: {"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}}
- Before: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}
- After: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}

**Authentication:**
- Before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"loginAttempt":null}

#### Before Patch

- **Total violations:** 3
- **By rule:**
  - `color-contrast`: 1
  - `label-title-only`: 1
  - `region`: 1

#### After Patch

- **Total violations:** 2
- **By rule:**
  - `color-contrast`: 1
  - `region`: 1

### Test 2: /admin/people

**Skipped:** baseline-target-not-observed

**Skip diagnostics:**
- Requested rules: ["label-title-only"]
- Required conditions: {"authRequired":true,"requested":{"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}},"observedBefore":{"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}}
- Matching rule violations before: {"label-title-only":0}
- Selector counts before: {"input[title=\"Select all rows in this table\"]":0,".gin--sticky-table-header > thead > tr > .select-all.gin--sticky-bulk-select > .form-checkbox.form-boolean[title=\"Select all rows in this table\"]":0,".views-table > thead > tr > .select-all.gin--sticky-bulk-select > .form-checkbox.form-boolean[title=\"Select all rows in this table\"]":0,"#edit-checkbox-hidden-label-value":0,"#edit-checkbox-hidden-label-disabled-value":0}
- Navigation before: {"requestedUrl":"http://drupal-core.ddev.site/admin/people","finalUrl":"http://drupal-core.ddev.site/admin/people","httpStatus":200,"redirected":false,"title":"People | Drupal A11y Eval","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"selectorCounts":{}}
- Reproduction candidates: [{"patternId":"DRU-987EB788","ruleId":"label-title-only","path":"/admin/content","selector":"input[title=\"Select all rows in this table\"]","preferred":true},{"patternId":"DRU-987EB788","ruleId":"label-title-only","path":"/admin/content","selector":".gin--sticky-table-header > thead > tr > .select-all.gin--sticky-bulk-select > .form-checkbox.form-boolean[title=\"Select all rows in this table\"]","preferred":true},{"patternId":"DRU-987EB788","ruleId":"label-title-only","path":"/admin/content","selector":".views-table > thead > tr > .select-all.gin--sticky-bulk-select > .form-checkbox.form-boolean[title=\"Select all rows in this table\"]","preferred":true},{"patternId":"DRU-987EB788","ruleId":"label-title-only","path":"/table","selector":"input[title=\"Select all rows in this table\"]","preferred":true},{"patternId":"DRU-987EB788","ruleId":"label-title-only","path":"/table","selector":".gin--sticky-table-header > thead > tr > .select-all.gin--sticky-bulk-select > .form-checkbox.form-boolean[title=\"Select all rows in this table\"]","preferred":true},{"patternId":"DRU-987EB788","ruleId":"label-title-only","path":"/table","selector":".views-table > thead > tr > .select-all.gin--sticky-bulk-select > .form-checkbox.form-boolean[title=\"Select all rows in this table\"]","preferred":true},{"patternId":"DRU-987EB788","ruleId":"label-title-only","path":"/admin/people","selector":"input[title=\"Select all rows in this table\"]","preferred":true},{"patternId":"DRU-987EB788","ruleId":"label-title-only","path":"/admin/people","selector":".gin--sticky-table-header > thead > tr > .select-all.gin--sticky-bulk-select > .form-checkbox.form-boolean[title=\"Select all rows in this table\"]","preferred":true},{"patternId":"DRU-987EB788","ruleId":"label-title-only","path":"/admin/people","selector":".views-table > thead > tr > .select-all.gin--sticky-bulk-select > .form-checkbox.form-boolean[title=\"Select all rows in this table\"]","preferred":true}]
- Auth setup: {"attempted":true,"success":true,"method":"uli","uli":"http://drupal-core.ddev.site/user/reset/1/1780195028/[REDACTED]/login","finalUrl":"http://drupal-core.ddev.site/user/1/edit?pass-reset-token=[REDACTED]&check_logged_in=1","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"credentialAttempted":false,"error":null}
- Auth before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"loginAttempt":null}

---

## Screenshots

Captured 1 screenshot(s) for this run. See the reports directory.

## HTML Snapshots

Captured 1 HTML snapshot(s) for this run.
