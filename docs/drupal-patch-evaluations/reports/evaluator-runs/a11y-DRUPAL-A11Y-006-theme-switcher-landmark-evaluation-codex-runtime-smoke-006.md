# Patch Evaluation Report: a11y-DRUPAL-A11Y-006-theme-switcher-landmark-codex-runtime-smoke-006

**Generated:** 2026-05-28 at 12:50:00 PM

## Summary

- **Description:** Wrap theme switcher form in nav landmark
- **WCAG Criteria:** 1.3.6 (AAA)
- **Affected Rules:** region
- **Pattern Source:** reports/pattern-report-2026-05-06.json
- **Pattern Source (Markdown):** reports/pattern-report-2026-05-06.md
- **Target Pattern IDs:** DRU-6BA9E02D
- **Pattern ID Match Type:** source-pattern-matched
- **Matched Pattern IDs (pattern source):** DRU-6BA9E02D
- **Generated Pattern IDs (current run):** DRU-6BA9E02D
- **Status:** ❌ **FAIL** — Patch introduced new accessibility violations
- **Outcome Reason:** `new-violations-introduced`
- **Eligible For Patch Recommendation:** yes
- **Requested color mode:** light
- **Patch preflight applicability:** applicable
- **Drupal initial state capture:** complete
- **Enabled modules (captured):** 53
- **Enabled modules hash:** e0133986f3906e2439787af017dcbe0cf6e13cf9cb9271c69393741da46673dd
- **Core extension hash:** 31b259471c42afbd3e30d71ad307fb06ea209bbb58152af62111117b20cec91c
- **Pattern source modified:** 2026-05-28T16:34:13.257Z
- **Pattern source age (hours):** 0.25
- **Case generation mode:** pattern-report-derived
- **Case generation count:** 8
- **Page load HTTP statuses (baseline):** 200x8
- **Pages loaded successfully (2xx):** 8/8
- **Pages not loaded as 2xx:** 0/8
- **ID consistency issues:** patterns=1, instances=0
- **Pattern observed before patch attempt:** yes
- **Baseline observed instances:** 8
- **Fixed instances after patch:** 0
- **Remaining instances after patch:** 8

### Replication Instructions

Use the following deterministic steps to reproduce this exact evaluation run:

- Setup: `ddev drush cset system.theme default olivero -y`
- Setup: `ddev drush cset system.theme admin claro -y`
- Setup: `ddev drush cache-rebuild`
- Flow: Navigate to each test case URL under requested conditions and capture baseline evidence.
- Flow: Apply patch with: git apply "/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/patches/a11y-DRUPAL-A11Y-006-theme-switcher-landmark.patch"
- Flow: Clear Drupal cache with: ddev drush cache-rebuild
- Flow: Revisit same URL + conditions and capture post-patch evidence.
- Flow: Revert patch with: git apply -R "/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/patches/a11y-DRUPAL-A11Y-006-theme-switcher-landmark.patch"
- Variant ID: `codex-runtime-smoke-006`
- Expected proof: Problem must be observed before patch and not observed after patch under the same recorded conditions.

### Drupal Initial State Snapshot

- **Captured at:** 2026-05-28T16:49:21.135Z
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

### Pattern Coverage (From Scan Report)

- **Targeted patterns:** 1
- **Patterns seen before patch:** 1
- **Fully fixed patterns:** 0
- **Partially fixed patterns:** 0
- **Unchanged patterns:** 1

| Pattern ID | Rule | Paths (sample) | Before | After | Status |
|---|---|---|---:|---:|---|
| DRU-6BA9E02D | region | /, /action-link, /admin | 8 | 8 | unchanged |

### Instance ID Coverage

- **Targeted instance IDs:** 24
- **Seen before patch:** 8
- **Fixed instances:** 0
- **Remaining instances:** 8
- **Not observed in baseline:** 16

| Instance ID | Pattern ID | Rule | Path | Status | Before IDs | After IDs |
|---|---|---|---|---|---|---|
| DRU-2b59ef7e | DRU-6BA9E02D | region | / | remaining | DRU-2b59ef7e | DRU-2b59ef7e |
| DRU-8a858898 | DRU-6BA9E02D | region | / | not-observed | - | - |
| DRU-5338860c | DRU-6BA9E02D | region | / | not-observed | - | - |
| DRU-10356e11 | DRU-6BA9E02D | region | /admin | remaining | DRU-10356e11 | DRU-10356e11 |
| DRU-604740ed | DRU-6BA9E02D | region | /admin | not-observed | - | - |
| DRU-9bb0aa67 | DRU-6BA9E02D | region | /admin | not-observed | - | - |
| DRU-f196e08d | DRU-6BA9E02D | region | /admin/appearance | remaining | DRU-f196e08d | DRU-f196e08d |
| DRU-65293652 | DRU-6BA9E02D | region | /admin/appearance | not-observed | - | - |
| DRU-24cabae4 | DRU-6BA9E02D | region | /admin/appearance | not-observed | - | - |
| DRU-c240cbdd | DRU-6BA9E02D | region | /admin/config | remaining | DRU-c240cbdd | DRU-c240cbdd |
| DRU-b507ad97 | DRU-6BA9E02D | region | /admin/config | not-observed | - | - |
| DRU-4014357b | DRU-6BA9E02D | region | /admin/config | not-observed | - | - |
| DRU-6081a3b8 | DRU-6BA9E02D | region | /admin/config/content/formats | remaining | DRU-6081a3b8 | DRU-6081a3b8 |
| DRU-add43fc3 | DRU-6BA9E02D | region | /admin/config/content/formats | not-observed | - | - |
| DRU-a41c0d72 | DRU-6BA9E02D | region | /admin/config/content/formats | not-observed | - | - |
| DRU-bc8272a1 | DRU-6BA9E02D | region | /admin/config/content/formats/manage/restricted_html | remaining | DRU-bc8272a1 | DRU-bc8272a1 |
| DRU-6ce03e08 | DRU-6BA9E02D | region | /admin/config/content/formats/manage/restricted_html | not-observed | - | - |
| DRU-7cb2794c | DRU-6BA9E02D | region | /admin/config/content/formats/manage/restricted_html | not-observed | - | - |
| DRU-b5617113 | DRU-6BA9E02D | region | /admin/config/system/site-information | remaining | DRU-b5617113 | DRU-b5617113 |
| DRU-7315a74b | DRU-6BA9E02D | region | /admin/config/system/site-information | not-observed | - | - |
| DRU-8de12cb3 | DRU-6BA9E02D | region | /admin/config/system/site-information | not-observed | - | - |
| DRU-71da4971 | DRU-6BA9E02D | region | /admin/content | remaining | DRU-71da4971 | DRU-71da4971 |
| DRU-6fc100b1 | DRU-6BA9E02D | region | /admin/content | not-observed | - | - |
| DRU-5ded6396 | DRU-6BA9E02D | region | /admin/content | not-observed | - | - |

### Violation Counts

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Total violations** | 24 | 21 | -3 |

### Fixed Rules

- `landmark-contentinfo-is-top-level`: 2 → 0 (−2)
- `landmark-no-duplicate-contentinfo`: 1 → 0 (−1)
- `landmark-contentinfo-is-top-level`: 1 → 0 (−1)

### ⚠️ New Violations Introduced

- `heading-order`: 0 → 1 (+1)

---

## Test Cases

### Test 1: /

**URL:** `http://drupal-core.ddev.site:33000/`

**Elements tested:** .themeswitcher-form__form-item, #primary-tabs-title, .top-bar__actions

**Conditions:**
- Requested: {"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}}
- Before: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-frontpage"]}
- After: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-frontpage"]}

**Authentication:**
- Before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"loginAttempt":null}

#### Before Patch

- **Total violations:** 12
- **By rule:**
  - `link-in-text-block`: 11
  - `region`: 1

#### After Patch

- **Total violations:** 12
- **By rule:**
  - `link-in-text-block`: 11
  - `region`: 1

### Test 2: /admin

**URL:** `http://drupal-core.ddev.site:33000/admin`

**Elements tested:** .themeswitcher-form__form-item, #primary-tabs-title, .top-bar__actions

**Conditions:**
- Requested: {"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}}
- Before: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}
- After: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}

**Authentication:**
- Before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"loginAttempt":null}

#### Before Patch

- **Total violations:** 1
- **By rule:**
  - `region`: 1

#### After Patch

- **Total violations:** 1
- **By rule:**
  - `region`: 1

### Test 3: /admin/appearance

**URL:** `http://drupal-core.ddev.site:33000/admin/appearance`

**Elements tested:** .themeswitcher-form__form-item, #primary-tabs-title, .top-bar__actions

**Conditions:**
- Requested: {"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}}
- Before: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}
- After: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}

**Authentication:**
- Before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"loginAttempt":null}

#### Before Patch

- **Total violations:** 4
- **By rule:**
  - `landmark-contentinfo-is-top-level`: 2
  - `landmark-no-duplicate-contentinfo`: 1
  - `region`: 1

#### After Patch

- **Total violations:** 1
- **By rule:**
  - `region`: 1

### Test 4: /admin/config

**URL:** `http://drupal-core.ddev.site:33000/admin/config`

**Elements tested:** .themeswitcher-form__form-item, #primary-tabs-title, .top-bar__actions

**Conditions:**
- Requested: {"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}}
- Before: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}
- After: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}

**Authentication:**
- Before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"loginAttempt":null}

#### Before Patch

- **Total violations:** 2
- **By rule:**
  - `landmark-contentinfo-is-top-level`: 1
  - `region`: 1

#### After Patch

- **Total violations:** 2
- **By rule:**
  - `heading-order`: 1
  - `region`: 1

### Test 5: /admin/config/content/formats

**URL:** `http://drupal-core.ddev.site:33000/admin/config/content/formats`

**Elements tested:** .themeswitcher-form__form-item, #primary-tabs-title, .top-bar__actions

**Conditions:**
- Requested: {"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}}
- Before: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}
- After: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}

**Authentication:**
- Before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"loginAttempt":null}

#### Before Patch

- **Total violations:** 1
- **By rule:**
  - `region`: 1

#### After Patch

- **Total violations:** 1
- **By rule:**
  - `region`: 1

### Test 6: /admin/config/content/formats/manage/restricted_html

**URL:** `http://drupal-core.ddev.site:33000/admin/config/content/formats/manage/restricted_html`

**Elements tested:** .themeswitcher-form__form-item, #primary-tabs-title, .top-bar__actions

**Conditions:**
- Requested: {"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}}
- Before: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}
- After: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}

**Authentication:**
- Before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"loginAttempt":null}

#### Before Patch

- **Total violations:** 1
- **By rule:**
  - `region`: 1

#### After Patch

- **Total violations:** 1
- **By rule:**
  - `region`: 1

### Test 7: /admin/config/system/site-information

**URL:** `http://drupal-core.ddev.site:33000/admin/config/system/site-information`

**Elements tested:** .themeswitcher-form__form-item, #primary-tabs-title, .top-bar__actions

**Conditions:**
- Requested: {"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}}
- Before: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}
- After: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}

**Authentication:**
- Before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"loginAttempt":null}

#### Before Patch

- **Total violations:** 1
- **By rule:**
  - `region`: 1

#### After Patch

- **Total violations:** 1
- **By rule:**
  - `region`: 1

### Test 8: /admin/content

**URL:** `http://drupal-core.ddev.site:33000/admin/content`

**Elements tested:** .themeswitcher-form__form-item, #primary-tabs-title, .top-bar__actions

**Conditions:**
- Requested: {"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}}
- Before: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}
- After: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}

**Authentication:**
- Before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"loginAttempt":null}

#### Before Patch

- **Total violations:** 2
- **By rule:**
  - `empty-table-header`: 1
  - `region`: 1

#### After Patch

- **Total violations:** 2
- **By rule:**
  - `empty-table-header`: 1
  - `region`: 1

---

## Screenshots

Captured 22 screenshot(s) for this run. See the reports directory.

## HTML Snapshots

Captured 22 HTML snapshot(s) for this run.
