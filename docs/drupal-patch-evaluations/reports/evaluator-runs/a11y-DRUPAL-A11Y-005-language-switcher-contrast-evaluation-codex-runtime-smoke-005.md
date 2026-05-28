# Patch Evaluation Report: a11y-DRUPAL-A11Y-005-language-switcher-contrast-codex-runtime-smoke-005

**Generated:** 2026-05-28 at 12:53:19 PM

## Summary

- **Description:** Ensure language switcher links maintain WCAG AA contrast
- **WCAG Criteria:** 1.4.3 (AA)
- **Affected Rules:** color-contrast
- **Pattern Source:** reports/pattern-report-2026-05-06.json
- **Pattern Source (Markdown):** reports/pattern-report-2026-05-06.md
- **Target Pattern IDs:** DRU-F75A07EF
- **Pattern ID Match Type:** source-pattern-matched
- **Matched Pattern IDs (pattern source):** DRU-F75A07EF
- **Generated Pattern IDs (current run):** DRU-F75A07EF
- **Status:** 🟨 **INCONCLUSIVE** — No baseline instances were observed on targeted URLs/selectors
- **Outcome Reason:** `baseline-not-observed-due-to-route-unavailable`
- **Eligible For Patch Recommendation:** no
- **Requested color mode:** light
- **Patch preflight applicability:** applicable
- **Drupal initial state capture:** complete
- **Enabled modules (captured):** 53
- **Enabled modules hash:** e0133986f3906e2439787af017dcbe0cf6e13cf9cb9271c69393741da46673dd
- **Core extension hash:** 31b259471c42afbd3e30d71ad307fb06ea209bbb58152af62111117b20cec91c
- **Pattern source modified:** 2026-05-28T16:34:13.257Z
- **Pattern source age (hours):** 0.32
- **Case generation mode:** pattern-report-derived
- **Case generation count:** 6
- **Page load HTTP statuses (baseline):** 200x5, 404x1
- **Pages loaded successfully (2xx):** 5/6
- **Pages not loaded as 2xx:** 1/6
- **Skip reasons:** baseline-target-not-observedx5, route-unavailablex1
- **ID consistency issues:** patterns=1, instances=0
- **Pattern observed before patch attempt:** no
- **Baseline observed instances:** 0
- **Fixed instances after patch:** 0
- **Remaining instances after patch:** 0

### Replication Instructions

Use the following deterministic steps to reproduce this exact evaluation run:

- Setup: `ddev drush cset system.theme default olivero -y`
- Setup: `ddev drush cset system.theme admin claro -y`
- Setup: `ddev drush cache-rebuild`
- Flow: Navigate to each test case URL under requested conditions and capture baseline evidence.
- Flow: Apply patch with: git apply "/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/patches/a11y-DRUPAL-A11Y-005-language-switcher-contrast.patch"
- Flow: Clear Drupal cache with: ddev drush cache-rebuild
- Flow: Revisit same URL + conditions and capture post-patch evidence.
- Flow: Revert patch with: git apply -R "/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/patches/a11y-DRUPAL-A11Y-005-language-switcher-contrast.patch"
- Variant ID: `codex-runtime-smoke-005`
- Expected proof: Problem must be observed before patch and not observed after patch under the same recorded conditions.

### Drupal Initial State Snapshot

- **Captured at:** 2026-05-28T16:53:08.007Z
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
- **Patterns seen before patch:** 0
- **Fully fixed patterns:** 0
- **Partially fixed patterns:** 0
- **Unchanged patterns:** 1

| Pattern ID | Rule | Paths (sample) | Before | After | Status |
|---|---|---|---:|---:|---|
| DRU-F75A07EF | color-contrast | /action-link, /admin, /admin/appearance | 0 | 0 | unchanged |

### Violation Counts

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Total violations** | 12 | 0 | -12 |

---

## Test Cases

### Test 1: /action-link

**Skipped:** baseline-target-not-observed

**Skip diagnostics:**
- Requested rules: ["color-contrast"]
- Required conditions: {"authRequired":false,"requested":{"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}},"observedBefore":{"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-action-link"]}}
- Matching rule violations before: {"color-contrast":0}
- Selector counts before: {"a[hreflang=\"he\"]":1,"#edit-submit":1,".button--action":0,"p:nth-child(1) > a":0,".feed-icon":0,"#action-link-no-icon":1,"#action-link-plus":1,"#action-link-trash--N":0}
- Navigation before: {"requestedUrl":"http://drupal-core.ddev.site:33000/action-link","finalUrl":"http://drupal-core.ddev.site:33000/action-link","httpStatus":200,"redirected":false,"title":"Action Links | Drupal A11y Eval","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"selectorCounts":{}}
- Reproduction candidates: [{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin","selector":"a[hreflang=\"he\"]","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin","selector":"#edit-submit","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin","selector":".button--action","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/appearance","selector":"a[hreflang=\"he\"]","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/appearance","selector":"#edit-submit","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/appearance","selector":".button--action","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/content","selector":"a[hreflang=\"he\"]","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/content","selector":"#edit-submit","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/content","selector":".button--action","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/form_style","selector":"a[hreflang=\"he\"]","preferred":true}]
- Auth setup: {"attempted":true,"success":true,"method":"uli","uli":"http://drupal-core.ddev.site:33000/user/reset/1/1779987192/[REDACTED]/login","finalUrl":"http://drupal-core.ddev.site:33000/user/1/edit?pass-reset-token=[REDACTED]&check_logged_in=1","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"credentialAttempted":false,"error":null}
- Auth before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"loginAttempt":null}

### Test 2: /admin

**Skipped:** baseline-target-not-observed

**Skip diagnostics:**
- Requested rules: ["color-contrast"]
- Required conditions: {"authRequired":true,"requested":{"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}},"observedBefore":{"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}}
- Matching rule violations before: {"color-contrast":0}
- Selector counts before: {"a[hreflang=\"he\"]":1,"#edit-submit":1,".button--action":0,"p:nth-child(1) > a":0,".feed-icon":0,"#action-link-no-icon":0,"#action-link-plus":0,"#action-link-trash--N":0}
- Navigation before: {"requestedUrl":"http://drupal-core.ddev.site:33000/admin","finalUrl":"http://drupal-core.ddev.site:33000/admin","httpStatus":200,"redirected":false,"title":"Administration | Drupal A11y Eval","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"selectorCounts":{}}
- Reproduction candidates: [{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/action-link","selector":"a[hreflang=\"he\"]","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/action-link","selector":"#edit-submit","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/action-link","selector":".button--action","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/appearance","selector":"a[hreflang=\"he\"]","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/appearance","selector":"#edit-submit","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/appearance","selector":".button--action","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/content","selector":"a[hreflang=\"he\"]","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/content","selector":"#edit-submit","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/content","selector":".button--action","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/form_style","selector":"a[hreflang=\"he\"]","preferred":true}]
- Auth setup: {"attempted":true,"success":true,"method":"uli","uli":"http://drupal-core.ddev.site:33000/user/reset/1/1779987192/[REDACTED]/login","finalUrl":"http://drupal-core.ddev.site:33000/user/1/edit?pass-reset-token=[REDACTED]&check_logged_in=1","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"credentialAttempted":false,"error":null}
- Auth before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"loginAttempt":null}

### Test 3: /admin/appearance

**Skipped:** baseline-target-not-observed

**Skip diagnostics:**
- Requested rules: ["color-contrast"]
- Required conditions: {"authRequired":true,"requested":{"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}},"observedBefore":{"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}}
- Matching rule violations before: {"color-contrast":0}
- Selector counts before: {"a[hreflang=\"he\"]":1,"#edit-submit":1,".button--action":0,"p:nth-child(1) > a":1,".feed-icon":0,"#action-link-no-icon":0,"#action-link-plus":0,"#action-link-trash--N":0}
- Navigation before: {"requestedUrl":"http://drupal-core.ddev.site:33000/admin/appearance","finalUrl":"http://drupal-core.ddev.site:33000/admin/appearance","httpStatus":200,"redirected":false,"title":"Appearance | Drupal A11y Eval","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"selectorCounts":{}}
- Reproduction candidates: [{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/action-link","selector":"a[hreflang=\"he\"]","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/action-link","selector":"#edit-submit","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/action-link","selector":".button--action","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin","selector":"a[hreflang=\"he\"]","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin","selector":"#edit-submit","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin","selector":".button--action","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/content","selector":"a[hreflang=\"he\"]","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/content","selector":"#edit-submit","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/content","selector":".button--action","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/form_style","selector":"a[hreflang=\"he\"]","preferred":true}]
- Auth setup: {"attempted":true,"success":true,"method":"uli","uli":"http://drupal-core.ddev.site:33000/user/reset/1/1779987192/[REDACTED]/login","finalUrl":"http://drupal-core.ddev.site:33000/user/1/edit?pass-reset-token=[REDACTED]&check_logged_in=1","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"credentialAttempted":false,"error":null}
- Auth before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"loginAttempt":null}

### Test 4: /admin/content

**Skipped:** baseline-target-not-observed

**Skip diagnostics:**
- Requested rules: ["color-contrast"]
- Required conditions: {"authRequired":true,"requested":{"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}},"observedBefore":{"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}}
- Matching rule violations before: {"color-contrast":0}
- Selector counts before: {"a[hreflang=\"he\"]":1,"#edit-submit":1,".button--action":1,"p:nth-child(1) > a":0,".feed-icon":0,"#action-link-no-icon":0,"#action-link-plus":0,"#action-link-trash--N":0}
- Navigation before: {"requestedUrl":"http://drupal-core.ddev.site:33000/admin/content","finalUrl":"http://drupal-core.ddev.site:33000/admin/content","httpStatus":200,"redirected":false,"title":"Content | Drupal A11y Eval","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"selectorCounts":{}}
- Reproduction candidates: [{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/action-link","selector":"a[hreflang=\"he\"]","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/action-link","selector":"#edit-submit","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/action-link","selector":".button--action","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin","selector":"a[hreflang=\"he\"]","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin","selector":"#edit-submit","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin","selector":".button--action","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/appearance","selector":"a[hreflang=\"he\"]","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/appearance","selector":"#edit-submit","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/appearance","selector":".button--action","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/form_style","selector":"a[hreflang=\"he\"]","preferred":true}]
- Auth setup: {"attempted":true,"success":true,"method":"uli","uli":"http://drupal-core.ddev.site:33000/user/reset/1/1779987192/[REDACTED]/login","finalUrl":"http://drupal-core.ddev.site:33000/user/1/edit?pass-reset-token=[REDACTED]&check_logged_in=1","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"credentialAttempted":false,"error":null}
- Auth before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"loginAttempt":null}

### Test 5: /admin/form_style

**Skipped:** route-unavailable

**Skip diagnostics:**
- Requested rules: ["color-contrast"]
- Required conditions: {"authRequired":true,"requested":{"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}},"observedBefore":{"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}}
- Matching rule violations before: {}
- Selector counts before: {}
- Navigation before: {"requestedUrl":"http://drupal-core.ddev.site:33000/admin/form_style","finalUrl":"http://drupal-core.ddev.site:33000/admin/form_style","httpStatus":404,"redirected":false,"title":"Page not found | Drupal A11y Eval","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"selectorCounts":{}}
- Reproduction candidates: [{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/action-link","selector":"a[hreflang=\"he\"]","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/action-link","selector":"#edit-submit","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/action-link","selector":".button--action","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin","selector":"a[hreflang=\"he\"]","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin","selector":"#edit-submit","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin","selector":".button--action","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/appearance","selector":"a[hreflang=\"he\"]","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/appearance","selector":"#edit-submit","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/appearance","selector":".button--action","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/content","selector":"a[hreflang=\"he\"]","preferred":true}]
- Auth setup: {"attempted":true,"success":true,"method":"uli","uli":"http://drupal-core.ddev.site:33000/user/reset/1/1779987192/[REDACTED]/login","finalUrl":"http://drupal-core.ddev.site:33000/user/1/edit?pass-reset-token=[REDACTED]&check_logged_in=1","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"credentialAttempted":false,"error":null}
- Auth before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"loginAttempt":null}

### Test 6: /admin/modules

**Skipped:** baseline-target-not-observed

**Skip diagnostics:**
- Requested rules: ["color-contrast"]
- Required conditions: {"authRequired":true,"requested":{"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}},"observedBefore":{"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}}
- Matching rule violations before: {"color-contrast":0}
- Selector counts before: {"a[hreflang=\"he\"]":1,"#edit-submit":1,".button--action":0,"p:nth-child(1) > a":1,".feed-icon":0,"#action-link-no-icon":0,"#action-link-plus":0,"#action-link-trash--N":0}
- Navigation before: {"requestedUrl":"http://drupal-core.ddev.site:33000/admin/modules","finalUrl":"http://drupal-core.ddev.site:33000/admin/modules","httpStatus":200,"redirected":false,"title":"Extend | Drupal A11y Eval","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"selectorCounts":{}}
- Reproduction candidates: [{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/action-link","selector":"a[hreflang=\"he\"]","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/action-link","selector":"#edit-submit","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/action-link","selector":".button--action","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin","selector":"a[hreflang=\"he\"]","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin","selector":"#edit-submit","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin","selector":".button--action","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/appearance","selector":"a[hreflang=\"he\"]","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/appearance","selector":"#edit-submit","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/appearance","selector":".button--action","preferred":true},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/content","selector":"a[hreflang=\"he\"]","preferred":true}]
- Auth setup: {"attempted":true,"success":true,"method":"uli","uli":"http://drupal-core.ddev.site:33000/user/reset/1/1779987192/[REDACTED]/login","finalUrl":"http://drupal-core.ddev.site:33000/user/1/edit?pass-reset-token=[REDACTED]&check_logged_in=1","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"credentialAttempted":false,"error":null}
- Auth before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"loginAttempt":null}

---

## Screenshots

Captured 6 screenshot(s) for this run. See the reports directory.

## HTML Snapshots

Captured 15 HTML snapshot(s) for this run.
