# Patch Evaluation Report: a11y-DRUPAL-A11Y-002-submit-button-contrast-codex-runtime-smoke-002

**Generated:** 2026-05-28 at 12:52:12 PM

## Summary

- **Description:** Fix primary button color contrast on admin yellow accent
- **WCAG Criteria:** 1.4.3 (AA)
- **Affected Rules:** color-contrast
- **Pattern Source:** reports/pattern-report-2026-05-06.json
- **Pattern Source (Markdown):** reports/pattern-report-2026-05-06.md
- **Pattern ID Match Type:** runtime-generated-only
- **Matched Pattern IDs (pattern source):** none
- **Generated Pattern IDs (current run):** DRU-6be5aeb9, DRU-bc27b0a7, DRU-85a47615
- **Status:** 🟨 **INCONCLUSIVE** — No baseline instances were observed on targeted URLs/selectors
- **Outcome Reason:** `no-baseline-instances-observed`
- **Eligible For Patch Recommendation:** no
- **Requested color mode:** light
- **Patch preflight applicability:** applicable
- **Drupal initial state capture:** complete
- **Enabled modules (captured):** 53
- **Enabled modules hash:** e0133986f3906e2439787af017dcbe0cf6e13cf9cb9271c69393741da46673dd
- **Core extension hash:** 31b259471c42afbd3e30d71ad307fb06ea209bbb58152af62111117b20cec91c
- **Pattern source modified:** 2026-05-28T16:34:13.257Z
- **Pattern source age (hours):** 0.3
- **Case generation mode:** fallback-config-testCases
- **Case generation count:** 1
- **Case generation fallback reason:** no-configured-pattern-ids
- **Page load HTTP statuses (baseline):** 200x1
- **Pages loaded successfully (2xx):** 1/1
- **Pages not loaded as 2xx:** 0/1
- **Skip reasons:** baseline-target-not-observedx1
- **ID consistency issues:** patterns=0, instances=0
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
- Flow: Apply patch with: git apply "/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/patches/a11y-DRUPAL-A11Y-002-submit-button-contrast.patch"
- Flow: Clear Drupal cache with: ddev drush cache-rebuild
- Flow: Revisit same URL + conditions and capture post-patch evidence.
- Flow: Revert patch with: git apply -R "/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/patches/a11y-DRUPAL-A11Y-002-submit-button-contrast.patch"
- Variant ID: `codex-runtime-smoke-002`
- Expected proof: Problem must be observed before patch and not observed after patch under the same recorded conditions.

### Drupal Initial State Snapshot

- **Captured at:** 2026-05-28T16:52:06.585Z
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

### Violation Counts

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Total violations** | 1 | 0 | -1 |

---

## Test Cases

### Test 1: /action-link

**Skipped:** baseline-target-not-observed

**Skip diagnostics:**
- Requested rules: ["color-contrast"]
- Required conditions: {"authRequired":false,"requested":{"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}},"observedBefore":{"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-action-link"]}}
- Matching rule violations before: {"color-contrast":0}
- Selector counts before: {"a[hreflang=\"he\"]":1,"#edit-submit":1,".button--action":0}
- Navigation before: {"requestedUrl":"http://drupal-core.ddev.site:33000/action-link","finalUrl":"http://drupal-core.ddev.site:33000/action-link","httpStatus":200,"redirected":false,"title":"Action Links | Drupal A11y Eval","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"selectorCounts":{}}
- Reproduction candidates: [{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin","selector":"a[hreflang=\"he\"]","preferred":false},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin","selector":"#edit-submit","preferred":false},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin","selector":".button--action","preferred":false},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/appearance","selector":"a[hreflang=\"he\"]","preferred":false},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/appearance","selector":"#edit-submit","preferred":false},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/appearance","selector":".button--action","preferred":false},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/content","selector":"a[hreflang=\"he\"]","preferred":false},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/content","selector":"#edit-submit","preferred":false},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/content","selector":".button--action","preferred":false},{"patternId":"DRU-F75A07EF","ruleId":"color-contrast","path":"/admin/form_style","selector":"a[hreflang=\"he\"]","preferred":false}]
- Auth setup: {"attempted":true,"success":true,"method":"uli","uli":"http://drupal-core.ddev.site:33000/user/reset/1/1779987130/[REDACTED]/login","finalUrl":"http://drupal-core.ddev.site:33000/user/1/edit?pass-reset-token=[REDACTED]&check_logged_in=1","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"credentialAttempted":false,"error":null}
- Auth before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"loginAttempt":null}

---

## Screenshots

No screenshots were captured for this run.

## HTML Snapshots

Captured 2 HTML snapshot(s) for this run.
