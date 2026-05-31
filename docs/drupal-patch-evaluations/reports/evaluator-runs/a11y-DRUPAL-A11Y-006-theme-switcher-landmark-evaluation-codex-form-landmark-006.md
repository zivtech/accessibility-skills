# Patch Evaluation Report: a11y-DRUPAL-A11Y-006-theme-switcher-landmark-codex-form-landmark-006

**Generated:** 2026-05-31 at 2:48:06 PM

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
- **Enabled modules (captured):** 62
- **Enabled modules hash:** 2d83d0e6db0770aba0ff204c019cb0083815a23c6a682d4fd91a4486c560a892
- **Core extension hash:** 9bed4a03680499fbfeb08f353ac83775bccbd7e65a9352f00129bd33fad3c892
- **Pattern source modified:** 2026-05-28T16:34:13.257Z
- **Pattern source age (hours):** 74.22
- **Case generation mode:** pattern-report-derived
- **Case generation count:** 8
- **Page load HTTP statuses (baseline):** 200x8
- **Pages loaded successfully (2xx):** 8/8
- **Pages not loaded as 2xx:** 0/8
- **Skip reasons:** baseline-target-not-observedx5
- **ID consistency issues:** patterns=1, instances=0
- **Pattern observed before patch attempt:** yes
- **Baseline observed instances:** 3
- **Fixed instances after patch:** 3
- **Remaining instances after patch:** 0

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
- Variant ID: `codex-form-landmark-006`
- Expected proof: Problem must be observed before patch and not observed after patch under the same recorded conditions.

### Drupal Initial State Snapshot

- **Captured at:** 2026-05-31T18:47:34.557Z
- **Capture status:** complete
- **Default theme:** olivero
- **Admin theme:** claro
- **Enabled modules count:** 62
- **Enabled modules hash (sha256):** 2d83d0e6db0770aba0ff204c019cb0083815a23c6a682d4fd91a4486c560a892
- **Core extension hash (sha256):** 9bed4a03680499fbfeb08f353ac83775bccbd7e65a9352f00129bd33fad3c892
- **Core extension modules hash (sha256):** 563021e81a804826aa26f8246802a8b18b11cab28512141f0a3ac32d68fe6e01
- **Core extension themes hash (sha256):** 30bfe9325153ff420bc86f2bc9e447ecd63a74f52d8d0e329bf8420f15e9c0a3
- **Drush status:** captured successfully; credential-bearing fields omitted from this committed report.
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

- Baseline observed: 3
- Fixed after patch: 3
- Remaining after patch: 0
- New violations introduced: 1

### Pattern Coverage (From Scan Report)

- **Targeted patterns:** 1
- **Patterns seen before patch:** 1
- **Fully fixed patterns:** 1
- **Partially fixed patterns:** 0
- **Unchanged patterns:** 0

| Pattern ID | Rule | Paths (sample) | Before | After | Status |
|---|---|---|---:|---:|---|
| DRU-6BA9E02D | region | /, /action-link, /admin | 3 | 0 | fully-fixed |

### Instance ID Coverage

- **Targeted instance IDs:** 9
- **Seen before patch:** 3
- **Fixed instances:** 3
- **Remaining instances:** 0
- **Not observed in baseline:** 6

| Instance ID | Pattern ID | Rule | Path | Status | Before IDs | After IDs |
|---|---|---|---|---|---|---|
| DRU-2b59ef7e | DRU-6BA9E02D | region | / | fixed | DRU-2b59ef7e | - |
| DRU-8a858898 | DRU-6BA9E02D | region | / | not-observed | - | - |
| DRU-5338860c | DRU-6BA9E02D | region | / | not-observed | - | - |
| DRU-c240cbdd | DRU-6BA9E02D | region | /admin/config | fixed | DRU-c240cbdd | - |
| DRU-b507ad97 | DRU-6BA9E02D | region | /admin/config | not-observed | - | - |
| DRU-4014357b | DRU-6BA9E02D | region | /admin/config | not-observed | - | - |
| DRU-bc8272a1 | DRU-6BA9E02D | region | /admin/config/content/formats/manage/restricted_html | fixed | DRU-bc8272a1 | - |
| DRU-6ce03e08 | DRU-6BA9E02D | region | /admin/config/content/formats/manage/restricted_html | not-observed | - | - |
| DRU-7cb2794c | DRU-6BA9E02D | region | /admin/config/content/formats/manage/restricted_html | not-observed | - | - |

### Violation Counts

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Total violations** | 20 | 12 | -8 |

### Fixed Rules

- `region`: 1 → 0 (−1)
- `landmark-contentinfo-is-top-level`: 1 → 0 (−1)
- `region`: 1 → 0 (−1)
- `region`: 1 → 0 (−1)

### ⚠️ New Violations Introduced

- `heading-order`: 0 → 1 (+1)

---

## Test Cases

### Test 1: /

**URL:** `http://drupal-core.ddev.site/`

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

- **Total violations:** 11
- **By rule:**
  - `link-in-text-block`: 11

### Test 2: /admin

**Skipped:** baseline-target-not-observed

**Skip diagnostics:**
- Requested rules: ["region"]
- Required conditions: {"authRequired":true,"requested":{"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}},"observedBefore":{"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}}
- Matching rule violations before: {"region":0}
- Selector counts before: {".themeswitcher-form__form-item":1,"#primary-tabs-title":1,".top-bar__actions":0}
- Navigation before: {"requestedUrl":"http://drupal-core.ddev.site/admin","finalUrl":"http://drupal-core.ddev.site/admin","httpStatus":200,"redirected":false,"title":"Administration | Drupal A11y Eval","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"selectorCounts":{}}
- Reproduction candidates: [{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/","selector":".themeswitcher-form__form-item","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/","selector":"#primary-tabs-title","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/","selector":".top-bar__actions","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/action-link","selector":".themeswitcher-form__form-item","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/action-link","selector":"#primary-tabs-title","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/action-link","selector":".top-bar__actions","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/admin/appearance","selector":".themeswitcher-form__form-item","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/admin/appearance","selector":"#primary-tabs-title","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/admin/appearance","selector":".top-bar__actions","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/admin/config","selector":".themeswitcher-form__form-item","preferred":true}]
- Auth setup: ULI login succeeded; reset URL and pass-reset token redacted from this committed report.
- Auth before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"loginAttempt":null}

### Test 3: /admin/appearance

**Skipped:** baseline-target-not-observed

**Skip diagnostics:**
- Requested rules: ["region"]
- Required conditions: {"authRequired":true,"requested":{"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}},"observedBefore":{"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}}
- Matching rule violations before: {"region":0}
- Selector counts before: {".themeswitcher-form__form-item":1,"#primary-tabs-title":1,".top-bar__actions":0}
- Navigation before: {"requestedUrl":"http://drupal-core.ddev.site/admin/appearance","finalUrl":"http://drupal-core.ddev.site/admin/appearance","httpStatus":200,"redirected":false,"title":"Appearance | Drupal A11y Eval","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"selectorCounts":{}}
- Reproduction candidates: [{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/","selector":".themeswitcher-form__form-item","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/","selector":"#primary-tabs-title","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/","selector":".top-bar__actions","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/action-link","selector":".themeswitcher-form__form-item","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/action-link","selector":"#primary-tabs-title","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/action-link","selector":".top-bar__actions","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/admin","selector":".themeswitcher-form__form-item","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/admin","selector":"#primary-tabs-title","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/admin","selector":".top-bar__actions","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/admin/config","selector":".themeswitcher-form__form-item","preferred":true}]
- Auth setup: ULI login succeeded; reset URL and pass-reset token redacted from this committed report.
- Auth before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"loginAttempt":null}

### Test 4: /admin/config

**URL:** `http://drupal-core.ddev.site/admin/config`

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

- **Total violations:** 1
- **By rule:**
  - `heading-order`: 1

### Test 5: /admin/config/content/formats

**Skipped:** baseline-target-not-observed

**Skip diagnostics:**
- Requested rules: ["region"]
- Required conditions: {"authRequired":true,"requested":{"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}},"observedBefore":{"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}}
- Matching rule violations before: {"region":0}
- Selector counts before: {".themeswitcher-form__form-item":1,"#primary-tabs-title":0,".top-bar__actions":0}
- Navigation before: {"requestedUrl":"http://drupal-core.ddev.site/admin/config/content/formats","finalUrl":"http://drupal-core.ddev.site/admin/config/content/formats","httpStatus":200,"redirected":false,"title":"Text formats and editors | Drupal A11y Eval","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"selectorCounts":{}}
- Reproduction candidates: [{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/","selector":".themeswitcher-form__form-item","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/","selector":"#primary-tabs-title","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/","selector":".top-bar__actions","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/action-link","selector":".themeswitcher-form__form-item","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/action-link","selector":"#primary-tabs-title","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/action-link","selector":".top-bar__actions","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/admin","selector":".themeswitcher-form__form-item","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/admin","selector":"#primary-tabs-title","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/admin","selector":".top-bar__actions","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/admin/appearance","selector":".themeswitcher-form__form-item","preferred":true}]
- Auth setup: ULI login succeeded; reset URL and pass-reset token redacted from this committed report.
- Auth before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"loginAttempt":null}

### Test 6: /admin/config/content/formats/manage/restricted_html

**URL:** `http://drupal-core.ddev.site/admin/config/content/formats/manage/restricted_html`

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

- **Total violations:** 0

### Test 7: /admin/config/system/site-information

**Skipped:** baseline-target-not-observed

**Skip diagnostics:**
- Requested rules: ["region"]
- Required conditions: {"authRequired":true,"requested":{"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}},"observedBefore":{"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}}
- Matching rule violations before: {"region":0}
- Selector counts before: {".themeswitcher-form__form-item":1,"#primary-tabs-title":0,".top-bar__actions":0}
- Navigation before: {"requestedUrl":"http://drupal-core.ddev.site/admin/config/system/site-information","finalUrl":"http://drupal-core.ddev.site/admin/config/system/site-information","httpStatus":200,"redirected":false,"title":"Basic site settings | Drupal A11y Eval","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"selectorCounts":{}}
- Reproduction candidates: [{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/","selector":".themeswitcher-form__form-item","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/","selector":"#primary-tabs-title","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/","selector":".top-bar__actions","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/action-link","selector":".themeswitcher-form__form-item","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/action-link","selector":"#primary-tabs-title","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/action-link","selector":".top-bar__actions","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/admin","selector":".themeswitcher-form__form-item","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/admin","selector":"#primary-tabs-title","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/admin","selector":".top-bar__actions","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/admin/appearance","selector":".themeswitcher-form__form-item","preferred":true}]
- Auth setup: ULI login succeeded; reset URL and pass-reset token redacted from this committed report.
- Auth before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":true,"uid":1,"authenticated":true},"loginAttempt":null}

### Test 8: /admin/content

**Skipped:** baseline-target-not-observed

**Skip diagnostics:**
- Requested rules: ["region"]
- Required conditions: {"authRequired":true,"requested":{"screenType":"desktop","orientation":"landscape","colorMode":"light","direction":"ltr","viewport":{"width":1280,"height":1024}},"observedBefore":{"screenType":"desktop","orientation":"landscape","viewport":{"width":1280,"height":1024},"colorMode":"light","direction":"ltr","language":"en","colorSchemeDetected":"light","prefersContrast":"no-preference","forcedColors":"none","theme":"unknown","bodyClasses":["user-logged-in","path-admin"]}}
- Matching rule violations before: {"region":0}
- Selector counts before: {".themeswitcher-form__form-item":1,"#primary-tabs-title":1,".top-bar__actions":0}
- Navigation before: {"requestedUrl":"http://drupal-core.ddev.site/admin/content","finalUrl":"http://drupal-core.ddev.site/admin/content","httpStatus":200,"redirected":false,"title":"Content | Drupal A11y Eval","authState":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"selectorCounts":{}}
- Reproduction candidates: [{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/","selector":".themeswitcher-form__form-item","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/","selector":"#primary-tabs-title","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/","selector":".top-bar__actions","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/action-link","selector":".themeswitcher-form__form-item","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/action-link","selector":"#primary-tabs-title","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/action-link","selector":".top-bar__actions","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/admin","selector":".themeswitcher-form__form-item","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/admin","selector":"#primary-tabs-title","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/admin","selector":".top-bar__actions","preferred":true},{"patternId":"DRU-6BA9E02D","ruleId":"region","path":"/admin/appearance","selector":".themeswitcher-form__form-item","preferred":true}]
- Auth setup: ULI login succeeded; reset URL and pass-reset token redacted from this committed report.
- Auth before case: {"ensured":true,"neededRelogin":false,"before":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"after":{"loggedInClass":true,"logoutLink":true,"loginForm":false,"uid":1,"authenticated":true},"loginAttempt":null}

---

## Screenshots

Captured 14 screenshot(s) for this run. See the reports directory.

## HTML Snapshots

Captured 14 HTML snapshot(s) for this run.
