# Patch Evaluation Report: a11y-DRUPAL-A11Y-007-messages-landmark-role-codex-runtime-smoke-007

**Generated:** 2026-05-28 at 12:38:49 PM

## Summary

- **Description:** Wrap status messages in proper landmark with role
- **WCAG Criteria:** 1.3.6 (AAA)
- **Affected Rules:** landmark-contentinfo-is-top-level, landmark-no-duplicate-contentinfo
- **Pattern Source:** reports/pattern-report-2026-05-06.json
- **Pattern Source (Markdown):** reports/pattern-report-2026-05-06.md
- **Target Pattern IDs:** DRU-2E022F2F, DRU-1260AB7D
- **Pattern ID Match Type:** source-pattern-matched
- **Matched Pattern IDs (pattern source):** DRU-2E022F2F, DRU-1260AB7D
- **Generated Pattern IDs (current run):** DRU-2E022F2F, DRU-1260AB7D
- **Status:** ❌ **FAIL** — Patch did not fix the targeted issues
- **Outcome Reason:** `targeted-instances-not-fixed`
- **Eligible For Patch Recommendation:** yes
- **Requested color mode:** light
- **Patch preflight applicability:** applicable
- **Drupal initial state capture:** complete
- **Enabled modules (captured):** 53
- **Enabled modules hash:** e0133986f3906e2439787af017dcbe0cf6e13cf9cb9271c69393741da46673dd
- **Core extension hash:** 31b259471c42afbd3e30d71ad307fb06ea209bbb58152af62111117b20cec91c
- **Pattern source modified:** 2026-05-28T16:34:13.257Z
- **Pattern source age (hours):** 0.07
- **Case generation mode:** pattern-report-derived
- **Case generation count:** 4
- **Page load HTTP statuses (baseline):** 200x4
- **Pages loaded successfully (2xx):** 4/4
- **Pages not loaded as 2xx:** 0/4
- **ID consistency issues:** patterns=1, instances=0
- **Pattern observed before patch attempt:** yes
- **Baseline observed instances:** 4
- **Fixed instances after patch:** 2
- **Remaining instances after patch:** 2

### Replication Instructions

Use the following deterministic steps to reproduce this exact evaluation run:

- Setup: `ddev drush cset system.theme default olivero -y`
- Setup: `ddev drush cset system.theme admin claro -y`
- Setup: `ddev drush cache-rebuild`
- Flow: Navigate to each test case URL under requested conditions and capture baseline evidence.
- Flow: Apply patch with: git apply "/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/patches/a11y-DRUPAL-A11Y-007-messages-landmark-role.patch"
- Flow: Clear Drupal cache with: ddev drush cache-rebuild
- Flow: Revisit same URL + conditions and capture post-patch evidence.
- Flow: Revert patch with: git apply -R "/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/patches/a11y-DRUPAL-A11Y-007-messages-landmark-role.patch"
- Variant ID: `codex-runtime-smoke-007`
- Expected proof: Problem must be observed before patch and not observed after patch under the same recorded conditions.

### Drupal Initial State Snapshot

- **Captured at:** 2026-05-28T16:38:25.026Z
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

- **Targeted patterns:** 2
- **Patterns seen before patch:** 2
- **Fully fixed patterns:** 0
- **Partially fixed patterns:** 2
- **Unchanged patterns:** 0

| Pattern ID | Rule | Paths (sample) | Before | After | Status |
|---|---|---|---:|---:|---|
| DRU-2E022F2F | landmark-contentinfo-is-top-level | /admin/appearance, /admin/modules, /message | 2 | 1 | partially-fixed |
| DRU-1260AB7D | landmark-no-duplicate-contentinfo | /admin/appearance, /admin/modules | 2 | 1 | partially-fixed |

### Instance ID Coverage

- **Targeted instance IDs:** 6
- **Seen before patch:** 4
- **Fixed instances:** 2
- **Remaining instances:** 2
- **Not observed in baseline:** 2

| Instance ID | Pattern ID | Rule | Path | Status | Before IDs | After IDs |
|---|---|---|---|---|---|---|
| DRU-c59ff778 | DRU-2E022F2F | landmark-contentinfo-is-top-level | /admin/appearance | fixed | DRU-c59ff778 | - |
| DRU-4b16856d | DRU-2E022F2F | landmark-contentinfo-is-top-level | /admin/appearance | not-observed | - | - |
| DRU-53ec2bb1 | DRU-2E022F2F | landmark-contentinfo-is-top-level | /admin/modules | remaining | DRU-53ec2bb1 | DRU-53ec2bb1 |
| DRU-98d69441 | DRU-2E022F2F | landmark-contentinfo-is-top-level | /admin/modules | not-observed | - | - |
| DRU-3430d034 | DRU-1260AB7D | landmark-no-duplicate-contentinfo | /admin/appearance | fixed | DRU-3430d034 | - |
| DRU-e6e58987 | DRU-1260AB7D | landmark-no-duplicate-contentinfo | /admin/modules | remaining | DRU-e6e58987 | DRU-e6e58987 |

### Violation Counts

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Total violations** | 16 | 10 | -6 |

### Fixed Rules

- `landmark-contentinfo-is-top-level`: 2 → 0 (−2)
- `landmark-no-duplicate-contentinfo`: 1 → 0 (−1)
- `landmark-contentinfo-is-top-level`: 2 → 0 (−2)
- `landmark-no-duplicate-contentinfo`: 1 → 0 (−1)

---

## Test Cases

### Test 1: /admin/appearance

**URL:** `http://drupal-core.ddev.site:33000/admin/appearance`

**Elements tested:** .messages--error, .messages-list__item

**Conditions:**
- Requested: {"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}}
- Before: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}
- After: {"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}

**Authentication:**
- Before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"loginAttempt":null}

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

### Test 2: /admin/modules

**URL:** `http://drupal-core.ddev.site:33000/admin/modules`

**Elements tested:** .messages--error, .messages-list__item

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

- **Total violations:** 4
- **By rule:**
  - `landmark-contentinfo-is-top-level`: 2
  - `landmark-no-duplicate-contentinfo`: 1
  - `region`: 1

### Test 3: /admin/appearance

**URL:** `http://drupal-core.ddev.site:33000/admin/appearance`

**Elements tested:** .messages--error

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

### Test 4: /admin/modules

**URL:** `http://drupal-core.ddev.site:33000/admin/modules`

**Elements tested:** .messages--error

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

- **Total violations:** 4
- **By rule:**
  - `landmark-contentinfo-is-top-level`: 2
  - `landmark-no-duplicate-contentinfo`: 1
  - `region`: 1

---

## Screenshots

Captured 12 screenshot(s) for this run. See the reports directory.

## HTML Snapshots

Captured 12 HTML snapshot(s) for this run.
