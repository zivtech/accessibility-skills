# Patch Evaluation Report: a11y-DRUPAL-A11Y-004-tabindex-buttons-test-form-codex-remove-positive-tabindex-004

**Generated:** 2026-05-30 at 10:06:35 PM

## Summary

- **Description:** Remove explicit tabindex from buttons on test form
- **WCAG Criteria:** 2.1.1 (A)
- **Affected Rules:** tabindex
- **Pattern Source:** reports/pattern-report-2026-05-06.json
- **Pattern Source (Markdown):** reports/pattern-report-2026-05-06.md
- **Target Pattern IDs:** DRU-CC36FB25
- **Pattern ID Match Type:** source-pattern-matched
- **Matched Pattern IDs (pattern source):** DRU-CC36FB25
- **Generated Pattern IDs (current run):** DRU-CC36FB25
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
- **Pattern source age (hours):** 57.54
- **Case generation mode:** pattern-report-derived
- **Case generation count:** 1
- **Page load HTTP statuses (baseline):** 200x1
- **Pages loaded successfully (2xx):** 1/1
- **Pages not loaded as 2xx:** 0/1
- **ID consistency issues:** patterns=1, instances=0
- **Pattern observed before patch attempt:** yes
- **Baseline observed instances:** 2
- **Fixed instances after patch:** 2
- **Remaining instances after patch:** 0

### Replication Instructions

Use the following deterministic steps to reproduce this exact evaluation run:

- Setup: `ddev drush cset system.theme default olivero -y`
- Setup: `ddev drush cset system.theme admin claro -y`
- Setup: `ddev drush cache-rebuild`
- Flow: Navigate to each test case URL under requested conditions and capture baseline evidence.
- Flow: Apply patch with: git apply "/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/patches/a11y-DRUPAL-A11Y-004-tabindex-buttons-test-form.patch"
- Flow: Clear Drupal cache with: ddev drush cache-rebuild
- Flow: Revisit same URL + conditions and capture post-patch evidence.
- Flow: Revert patch with: git apply -R "/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/patches/a11y-DRUPAL-A11Y-004-tabindex-buttons-test-form.patch"
- Variant ID: `codex-remove-positive-tabindex-004`
- Expected proof: Problem must be observed before patch and not observed after patch under the same recorded conditions.

### Drupal Initial State Snapshot

- **Captured at:** 2026-05-31T02:06:24.019Z
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

- Baseline observed: 2
- Fixed after patch: 2
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
| DRU-CC36FB25 | tabindex | /buttons | 4 | 0 | fully-fixed |

### Instance ID Coverage

- **Targeted instance IDs:** 2
- **Seen before patch:** 2
- **Fixed instances:** 2
- **Remaining instances:** 0
- **Not observed in baseline:** 0

| Instance ID | Pattern ID | Rule | Path | Status | Before IDs | After IDs |
|---|---|---|---|---|---|---|
| DRU-dceab886 | DRU-CC36FB25 | tabindex | /buttons | fixed | DRU-dceab886, DRU-0f4d13c3 | - |
| DRU-53df30ff | DRU-CC36FB25 | tabindex | /buttons | fixed | DRU-53df30ff, DRU-02365f9b | - |

### Violation Counts

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Total violations** | 8 | 2 | -6 |

### Fixed Rules

- `tabindex`: 6 → 0 (−6)

---

## Test Cases

### Test 1: /buttons

**URL:** `http://drupal-core.ddev.site/buttons`

**Elements tested:** #edit-submit, #edit-danger--N

**Conditions:**
- Requested: {"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}}
- Before: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-buttons"]}
- After: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-buttons"]}

**Authentication:**
- Before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"loginAttempt":null}

#### Before Patch

- **Total violations:** 8
- **By rule:**
  - `region`: 2
  - `tabindex`: 6

#### After Patch

- **Total violations:** 2
- **By rule:**
  - `region`: 2

---

## Screenshots

Captured 2 screenshot(s) for this run. See the reports directory.

## HTML Snapshots

Captured 2 HTML snapshot(s) for this run.
