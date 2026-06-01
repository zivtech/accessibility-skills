# Drupal Accessibility Patch Evaluation Packet: DRUPAL-A11Y-007 Messages Landmark Role

> Status: INCONCLUSIVE
> Prepared: 2026-05-28
> Purpose: Trial packet using `templates/drupal-a11y-patch-evaluation-template.md` against Mike Gifford's current Drupal core patch/report artifacts.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-DRUPAL-A11Y-007-messages-landmark-role` |
| Status | `INCONCLUSIVE` |
| Project/package | `mgifford/drupal-core` |
| Target commit checked | `3728741f23122018f1f26206fe563cb6c9ad49f8` (`main` on 2026-05-28) |
| Current upstream base checked | `9ec853aac0cd` (`origin/main` on 2026-06-01 UTC) |
| Current PR worktree | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-pr-007-messages-landmark-role-20260601` |
| Current local candidate commit | `c297c18d98` (`fix: use status roles for non-error messages`) |
| Target file SHA | `core/modules/system/templates/status-messages.html.twig` blob `be6711b270df98d2aee223db7af2aa6b49c2ffa2` |
| Patch file SHA | Upstream raw patch: `patches/a11y-DRUPAL-A11Y-007-messages-landmark-role.patch` blob `59a6ebaac7d5fe500d1ab1d8b5cb848466060a93`; local reroll artifact: `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-007-messages-landmark-role-codex-reroll-status-alert-007.patch` |
| Evaluation artifact | PASS reroll: `docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-007-messages-landmark-role-evaluation-codex-reroll-status-alert-js-007.{md,json,html}`; cleaned rerun: `docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-007-messages-landmark-role-evaluation-codex-rerun-cleaned-007.{md,json,html}`; earlier failed run: `docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-007-messages-landmark-role-evaluation-codex-runtime-smoke-007.{md,json}` |
| Role smoke | `docs/drupal-patch-evaluations/reports/manual-checks/2026-05-28-drupal-a11y-007-role-smoke.md` |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Source Links

- Patch: https://github.com/mgifford/drupal-core/blob/main/patches/a11y-DRUPAL-A11Y-007-messages-landmark-role.patch
- Patch evaluation Markdown: https://github.com/mgifford/drupal-core/blob/main/patches/a11y-DRUPAL-A11Y-007-messages-landmark-role-evaluation.md
- Patch evaluation JSON: https://github.com/mgifford/drupal-core/blob/main/patches/a11y-DRUPAL-A11Y-007-messages-landmark-role-evaluation.json
- Pattern report: https://github.com/mgifford/drupal-core/blob/main/reports/PATTERN-REPORT-latest.md
- Batch summary: https://github.com/mgifford/drupal-core/blob/main/reports/PATCH-EVALUATION-SUMMARY.md
- Proposed patches index: https://github.com/mgifford/drupal-core/blob/main/patches/PROPOSED-PATCHES.md
- Patch evaluation README: https://github.com/mgifford/drupal-core/blob/main/patches/PATCH-EVALUATION-README.md

## Current Verdict

`INCONCLUSIVE` pending a human NVDA or VoiceOver smoke check. Local automated evidence supports the reroll candidate, but it is not AT-verified.

The original upstream patch only changed `core/modules/system/templates/status-messages.html.twig` from `contentinfo` to `region`; the repaired local evaluator showed that version still left targeted failures on `/admin/modules`. The local reroll saved in this packet changes message wrappers to `role="alert"` for errors and `role="status"` for non-error messages across server-rendered status-message templates, JavaScript message themers, and tabledrag warning generators. The current candidate has refreshed evaluator and DOM role evidence, but still needs human AT smoke before upstream filing.

## Issue Summary

| Field | Value |
|---|---|
| Rule/source | `axe-core landmark-contentinfo-is-top-level`, `axe-core landmark-no-duplicate-contentinfo` |
| Tool version | Upstream report: axe-core via Playwright; batch infrastructure documents axe-core 4.x |
| WCAG SC | Needs calibration. Upstream artifacts cite `1.3.6`; the proposed patches index says AAA, while the pattern report labels it Level A. WCAG 2.2 SC 1.3.6 is AAA. |
| Impact | `moderate` in axe/pattern report |
| User groups affected | Screen reader users and users navigating by landmarks |
| Route(s) | `/admin/appearance`, `/admin/modules`, `/message` in pattern report |
| Selector(s) | `.messages--error`; evaluation also targeted `.messages` and `[role="contentinfo"]` |
| Pattern ID(s) | `DRU-2E022F2F`, `DRU-1260AB7D` |
| Instance ID(s) | `INS-176AF555`, `INS-1E1F5949`, `INS-F35573C5`, `INS-90DB76B9`, `INS-C77800EB`, `INS-E1083638`, `INS-33B07066`, `INS-8F094E37`, `INS-35544EB1`, `INS-83F42AFC`, `INS-54574906`, `INS-20150FA9`, `INS-32AE2346`, `INS-6340BB49`, `INS-8EA427CF`, `INS-44531B14`, `INS-B015FF40`, `INS-91297A72`, `INS-EBE0F49A`, `INS-FF71DDFC`; and `INS-0F387792`, `INS-594DA129`, `INS-D74E025B`, `INS-CD2D6DED`, `INS-217D3820`, `INS-1358DBF4` |
| Theme/profile/modules | Evaluation setup requested default `olivero`, admin `claro` |
| Auth/content state | Local disposable runtime installed with local admin credentials redacted; theming tools fixtures enabled; evaluator authenticated as uid 1 |
| Viewport(s) | `1280x1024` desktop landscape in patch evaluation |
| Color mode / forced colors / direction | Requested light, LTR; detected light, forced colors none, prefers contrast no-preference |

## Baseline Evidence

### Pattern Report Baseline

The pattern report says the target problem exists:

- `DRU-2E022F2F`: `landmark-contentinfo-is-top-level`, selector `.messages--error`, affected routes `/admin/appearance`, `/admin/modules`, `/message`, 20 instances.
- `DRU-1260AB7D`: `landmark-no-duplicate-contentinfo`, selector `.messages--error`, affected routes `/admin/appearance`, `/admin/modules`, 6 instances.

Smallest reported failing snippet:

```html
<div role="contentinfo" aria-labelledby="message-error-title" class="messages-list__item messages messages--error">
```

The current target template on upstream `main` still renders `role="contentinfo"` for each message group:

```twig
<div data-drupal-messages>
{% for type, messages in message_list %}
  <div role="contentinfo" aria-label="{{ status_headings[type] }}"{{ attributes|without('role', 'aria-label') }}>
```

### Patch Evaluation Baseline

The upstream patch evaluation did not reproduce the baseline target:

```text
Status: INCONCLUSIVE
Outcome reason: no-baseline-instances-observed
Baseline observed instances: 0
Fixed instances after patch: 0
Remaining instances after patch: 0
Test case: /admin/appearance
Skipped: baseline-target-not-observed
```

The JSON evidence is more specific:

```text
Element not found: .messages
Element not found: [role="contentinfo"]
before.axe.total: 0
skipReason: baseline-target-not-observed
```

### Baseline Acceptance Gate

- [x] The target violation was observed before applying the patch in the local rerun.
- [x] The observed selector matches the packet selector in the local rerun.
- [x] Pattern/instance IDs are captured in the pattern report.
- [ ] The observed WCAG/rule mapping is consistent across artifacts.
- [x] Required interaction or message state was reached before scanning.

### Local Evaluator Rerun Baseline

After repairing the local runtime, I reran the evaluator against a disposable `mgifford/drupal-core` clone:

```bash
cd /Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
DRUPAL_BASE_URL=http://drupal-core.ddev.site:33000 \
  A11Y_VARIANT_ID=codex-runtime-smoke-007 \
  node core/tests/playwright/scripts/evaluate-patch.js \
  a11y-DRUPAL-A11Y-007-messages-landmark-role
```

Runtime conditions:

- DDEV v1.25.2, project `drupal-core`, PHP 8.5.
- Drupal 12.0-dev installed with the `standard` profile.
- Admin login available through Drush ULI and redacted local admin credentials.
- Enabled fixture modules included `theming_tools`, `message`, `button`, `table`, `imagefile`, `actionlink`, `pager`, `dialog`, `tab`, `lang_hebrew`, and `themeswitcher`.
- Local evaluator-only fixes were needed: `DRUPAL_BASE_URL` support and a missing `canonical-patch-map.js` helper.

Original upstream patch result:

```text
Status: FAIL
Outcome reason: targeted-instances-not-fixed
Case generation mode: pattern-report-derived
Baseline observed instances: 4
Fixed instances after patch: 2
Remaining instances after patch: 2
Introduced new violations: 0
```

The local report shows `/admin/appearance` was fixed, but `/admin/modules` still had `landmark-contentinfo-is-top-level` and `landmark-no-duplicate-contentinfo` after the patch.

Because remaining targeted instances were observed after patching, the original upstream patch should be treated as failed rather than merely blocked by test state.

### Local Reroll Evaluator Result

I rerolled the patch locally to use message semantics instead of `region`:

- error messages render the outer message wrapper with `role="alert"`,
- non-error messages render the outer message wrapper with `role="status"`,
- nested error-only `role="alert"` wrappers were removed,
- the same pattern was applied to the default system template, Claro, Default Admin, Olivero, Starterkit, Stable 9 media-library status messages, and the system test message template,
- JavaScript message themers in core, Claro, Default Admin, Olivero, and Umami were aligned so warnings are `status` rather than `alert`,
- tabledrag "unsaved changes" warning generators in core, Claro, and Default Admin were aligned so non-error warnings are `status` rather than `alert`,
- functional test expectations that asserted `role="contentinfo"` for status messages were updated to `role="status"`.

Patch artifact:

```text
docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-007-messages-landmark-role-codex-reroll-status-alert-007.patch
```

Validation command:

```bash
cd /Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
DRUPAL_BASE_URL=http://drupal-core.ddev.site:33000 \
  A11Y_VARIANT_ID=codex-reroll-status-alert-js-007 \
  node core/tests/playwright/scripts/evaluate-patch.js \
  a11y-DRUPAL-A11Y-007-messages-landmark-role
```

Result:

```text
Status: PASS
Outcome reason: targeted-issues-fixed-without-regressions
Case generation mode: pattern-report-derived
Baseline observed instances: 1
Fixed instances after patch: 1
Remaining instances after patch: 0
Total axe violations: 7 before, 1 after
Fixed rules:
- landmark-contentinfo-is-top-level: 2 -> 0
- landmark-no-duplicate-contentinfo: 1 -> 0
Introduced new violations: 0
```

Coverage note: the evaluator generated four cases from the pattern report. Three did not observe the historical baseline in this runtime, so this pass proves the observed target was fixed under the recorded conditions; it should not be worded as "all historical routes revalidated."

### Cleaned Rerun and Role Smoke

I reran the final `007` patch after cleaning runtime patch whitespace:

```bash
cd /Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
DRUPAL_BASE_URL=http://drupal-core.ddev.site:33000 \
  A11Y_VARIANT_ID=codex-rerun-cleaned-007 \
  node core/tests/playwright/scripts/evaluate-patch.js \
  a11y-DRUPAL-A11Y-007-messages-landmark-role
```

Result:

```text
Status: PASS
Outcome reason: targeted-issues-fixed-without-regressions
Baseline observed instances: 1
Fixed instances after patch: 1
Remaining instances after patch: 0
Fixed rules:
- landmark-contentinfo-is-top-level: 2 -> 0
- landmark-no-duplicate-contentinfo: 1 -> 0
Introduced new violations: 0
```

DOM/axe role smoke also passed for `/admin/appearance` and `/admin/modules`: server-rendered and JavaScript-created warnings use `role="status"` while errors use `role="alert"`.

This is not a true assistive-technology smoke check. NVDA is unavailable on this macOS runtime, and I did not enable VoiceOver because that changes the user's desktop state. Run one short human NVDA or VoiceOver check before describing the reroll as AT-verified upstream evidence.

## Patch Hygiene

### Published Evaluation Preflight

The May 7 evaluation says patch preflight failed:

```text
git apply --check "/Users/mike.gifford/drupal-core/patches/a11y-DRUPAL-A11Y-007-messages-landmark-role.patch"
error: corrupt patch at /Users/mike.gifford/drupal-core/patches/a11y-DRUPAL-A11Y-007-messages-landmark-role.patch:22
```

### Current Raw Patch Re-Check

I rechecked the current raw patch against the current raw target template by recreating the target path in a temporary git repo:

```bash
tmp=$(mktemp -d /tmp/drupal-a11y-007.XXXXXX)
cd "$tmp"
git init -q
mkdir -p core/modules/system/templates patches
curl -fsSL https://raw.githubusercontent.com/mgifford/drupal-core/main/core/modules/system/templates/status-messages.html.twig \
  -o core/modules/system/templates/status-messages.html.twig
curl -fsSL https://raw.githubusercontent.com/mgifford/drupal-core/main/patches/a11y-DRUPAL-A11Y-007-messages-landmark-role.patch \
  -o patches/a11y-DRUPAL-A11Y-007-messages-landmark-role.patch
git apply --check patches/a11y-DRUPAL-A11Y-007-messages-landmark-role.patch
```

Result:

```text
patch_lines=12
git apply --check: exit 0
```

Current patch body:

```diff
diff --git a/core/modules/system/templates/status-messages.html.twig b/core/modules/system/templates/status-messages.html.twig
index 1234567..abcdefg 100644
--- a/core/modules/system/templates/status-messages.html.twig
+++ b/core/modules/system/templates/status-messages.html.twig
@@ -23,6 +23,6 @@
 <div data-drupal-messages>
 {% for type, messages in message_list %}
-  <div role="contentinfo" aria-label="{{ status_headings[type] }}"{{ attributes|without('role', 'aria-label') }}>
+  <div role="region" aria-label="{{ status_headings[type] }}"{{ attributes|without('role', 'aria-label') }}>
     {% if type == 'error' %}
       <div role="alert">
     {% endif %}
```

### Patch Hygiene Gate

- [x] Current raw patch applies cleanly in a minimal current-file path check.
- [x] Target file exists on upstream `main`.
- [x] Full-repo patch apply/revert succeeded in the local disposable runtime.
- [x] Drupal caches were rebuilt after applying the patch in the local rerun.
- [x] Revert command is known: `git apply -R patches/a11y-DRUPAL-A11Y-007-messages-landmark-role.patch`.

Patch hygiene should be treated as currently usable for this item. The current blocker is not patch corruption; it is that the patch only partially fixes the targeted pattern instances.

### Local Reroll Patch Hygiene

The local reroll patch applies cleanly in the disposable full runtime checkout:

```bash
git apply --check patches/a11y-DRUPAL-A11Y-007-messages-landmark-role.patch
```

The evaluator applied and reverted the reroll successfully during `codex-reroll-status-alert-js-007`.

### Current-Main Reroll

On 2026-06-01 UTC, the saved reroll patch was checked against current `origin/main` at `9ec853aac0cd` in a fresh worktree:

```text
/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-pr-007-messages-landmark-role-20260601
```

The saved patch applied cleanly. A critic pass then found that tabledrag warning messages still hardcoded `role="alert"` despite being non-error warning messages. The current local candidate commit `c297c18d98` extends the reroll to set those tabledrag warnings to `role="status"` as well.

Static checks on the current branch:

```text
git diff --check: pass
php -l changed PHP test files: pass
node --check changed JS files: pass
Drupal PHPCS on changed PHP/Twig files: pass
credential-pattern scan on changed files: no hits
```

Runtime evaluator rerun with variant `codex-current-main-tabledrag-007`:

```text
Status: PASS
Outcome reason: targeted-issues-fixed-without-regressions
Baseline observed instances: 2
Fixed instances after patch: 2
Remaining instances after patch: 0
New violations introduced: 0
Total violations: 12 before, 3 after
```

Focused DOM role probe with the regenerated patch applied:

```text
Drupal.Message warning: role="status"
Drupal.Message error: role="alert"
Tabledrag warnings on /admin/structure/menu/manage/main, /admin/structure/block, and /admin/structure/taxonomy/manage/tags/overview: role="status"
```

Functional test rerun in the runtime harness:

```text
PlaceholderMessageTest::testMessagePlaceholder: OK (1 test, 2 assertions)
ModulesListFormWebTest::testModulesListFormStatusMessage: OK (1 test, 15 assertions)
```

Report: `docs/drupal-patch-evaluations/reports/current-wave/2026-06-01-007-current-main-reroll.md`

## After-Patch Verification

The original upstream after-patch verification was valid for the repaired runtime, and it failed:

- `/admin/appearance`: target landmark failures went from 3 to 0.
- `/admin/modules`: target landmark failures remained 3 to 3.
- Overall targeted instance state: 4 observed before, 2 fixed, 2 remaining.
- No new violations were introduced by the patch in this run.

The local reroll after-patch verification passed in the refreshed runtime evaluator run:

- `/admin/appearance`: target `contentinfo` landmark failures went from present to absent.
- `/admin/modules`: target `contentinfo` landmark failures went from present to absent.
- Observed pattern-report-derived target: `landmark-contentinfo-is-top-level` was removed from the after scan; `landmark-no-duplicate-contentinfo` was also absent after patching.
- Overall targeted instance state: 2 observed before, 2 fixed, 0 remaining.
- No new violations were introduced by the reroll in this run.

### DOM Role Probe

After a critic flagged a mismatch between server-rendered and JavaScript-created warning messages, I expanded the reroll to cover JavaScript message themers and ran a direct DOM probe with the final patch applied:

```text
/admin/appearance:
- error: role="alert"
- warning: role="status"

/admin/modules:
- error: role="alert"
- warning: role="status"

JavaScript-created warning on /admin/appearance:
- warning: role="status"
```

This resolves the earlier after-patch snippet where a client-created warning rendered as `role="alert"`.

### Targeted Re-Scan Command

Expected rerun command from upstream infrastructure:

```bash
yarn a11y:evaluate-patch a11y-DRUPAL-A11Y-007-messages-landmark-role
```

### Verification Gate

- [x] Same targeted command was used before and after the patch after baseline reproduction.
- [ ] Target rule is absent on the target selector after the patch.
- [x] Pattern-report-derived broad target cases were run after the patch.
- [x] New violations, if any, are listed and classified.
- [x] Remaining adjacent issues are separated from the fixed issue.
- [ ] The packet does not claim that adjacent issues are fixed by this patch.

## Runtime Repair Notes

The original upstream evaluation did not render `.messages` or `[role="contentinfo"]`. The local repair made message state deterministic enough for the evaluator to observe pattern-report-derived `/admin/appearance` and `/admin/modules` failures.

Remaining evaluator improvements:

1. Upstream the evaluator `DRUPAL_BASE_URL` support so nonstandard DDEV ports work.
2. Restore or commit `core/tests/playwright/scripts/lib/canonical-patch-map.js`.
3. Prefer deterministic `/message` fixtures for status-message semantic review, while keeping `/admin/modules` in regression coverage because it remained failing.
4. Capture HTML before patch and require this exact role failure before applying any rerolled patch:

```html
<div role="contentinfo" ... class="... messages--error">
```

5. Only then run the same route, state setup, viewport, color mode, direction, and axe rules after applying the rerolled patch.

## Manual and Perspective Verification

| Check | Environment | Result | Notes |
|---|---|---|---|
| Keyboard-only | Browser/version | `not run` | Not primary for this rule, but messages should not disrupt focus order. |
| NVDA + Chrome | Versions | `not run` | Confirm error/status message announcement and landmark list behavior. |
| VoiceOver + Safari | Versions | `not run` | Confirm message announcement and rotor landmarks do not show duplicate contentinfo. |
| Voice control / label in name | Tool/version | `not run` | Not primary. |
| Forced colors | Browser/version | `not run` | Not primary, but message affordances should remain visible. |
| Zoom/reflow | Browser/version | `not run` | Not primary. |

Manual checks may remain open, but the packet must not imply they passed.

## Outcome

`INCONCLUSIVE`

The issue is real in the local repaired runtime. The original upstream patch partially fixed the target but left the same failures on `/admin/modules`. The local reroll candidate applies, reverts, and passes the standard evaluator with observed targeted `contentinfo` landmark failures removed and no new violations introduced. The remaining gap is human AT behavior: the packet has DOM/axe role evidence, not NVDA or VoiceOver evidence.

Before upstream filing, run at least one assistive-technology smoke check for message announcement behavior and landmark navigation. This packet does not claim that NVDA, VoiceOver, or Dragon testing has passed.

## Root Cause and Fix Narrative

### Root Cause

Drupal status messages are rendered with `role="contentinfo"`. When those messages appear inside other landmarks or alongside the page footer, screen reader landmark navigation can expose nested or duplicate `contentinfo` landmarks. The pattern report ties this to `landmark-contentinfo-is-top-level` and `landmark-no-duplicate-contentinfo`.

### Proposed Fix Under Review

The local reroll follows the pattern report's semantic direction: non-error messages use `role="status"` and errors use `role="alert"`. This avoids exposing status messages as footer/contentinfo landmarks, avoids nested alert wrappers, and aligns server-rendered messages, JavaScript-created Drupal messages, and tabledrag warning messages.

Design caveat: `status` and `alert` are live-region roles. Because these messages are often present on page load as well as after actions, the upstream issue should include a short screen reader smoke note confirming message announcement is not duplicated or missed in Drupal's common message flows.

## Draft Drupal.org Issue Block

This block is not ready to file as verified evidence. It is a draft for when test state is repaired.

### Title

`[Accessibility] Status messages create duplicate or nested contentinfo landmarks`

### Steps to Reproduce

1. In a local Drupal core checkout, enable the same theme setup used in the evaluation: default `olivero`, admin `claro`.
2. Navigate to a route that deterministically renders an error/status message, such as `/message` or a route where an error message is triggered immediately before scanning.
3. Run axe on the rendered page and confirm `landmark-contentinfo-is-top-level` and/or `landmark-no-duplicate-contentinfo` on `.messages--error`.

### Expected Result

Status messages are announced as status/error messages and do not create duplicate or nested `contentinfo` landmarks.

### Actual Result

The message wrapper renders `role="contentinfo"`, causing contentinfo landmark failures when messages appear.

### Proposed Resolution

Revise `core/modules/system/templates/status-messages.html.twig` so status messages use a role appropriate to message semantics. Verify with axe and manual screen reader smoke checks.

### Evidence Needed Before Filing

- Rerolled patch that fixes both observed core status-message render paths.
- After scan using the same route/state/conditions with no remaining target instances.
- Broad regression scan with no patch-owned regressions.
- Manual NVDA/VoiceOver smoke notes before claiming assistive-technology verification.

### Tags

- `Accessibility`
- `Needs steps to reproduce`
- `Needs reroll` if the current patch is not the final role design

### AI Assistance Disclosure

This packet was prepared with AI assistance. The accessibility finding must be verified with the evidence above and must not be filed from AI code inspection alone.

## a11y-Critic Readiness Verdict

Canonical local status recommendation: `INCONCLUSIVE` until human AT smoke evidence is recorded

Readiness note: the reroll has automated before/after evidence and is a plausible upstream replacement candidate, but manual assistive-technology behavior still needs a short smoke check before filing as fully user-verified.

Findings:

1. The original upstream patch failure is supported by local evidence: baseline observed 4 target instances, fixed 2, remaining 2; `/admin/modules` still failed both target rules after patching.
2. The reroll design now matches status/error message semantics better than `region`, but the live-region behavior should still be smoke-tested with a screen reader.
3. Do not carry the evaluator's "eligible for patch recommendation" wording forward as full upstream readiness; it means the patch candidate has automated evidence, while manual AT evidence remains open.
4. WCAG level mapping is inconsistent across artifacts. Before filing, cite the axe rule and correct WCAG mapping rather than preserving the pattern report's Level A wording for SC 1.3.6.

Recommended next action: run a short NVDA or VoiceOver smoke check on error/status message announcement, then prepare the reroll patch for upstream review.
