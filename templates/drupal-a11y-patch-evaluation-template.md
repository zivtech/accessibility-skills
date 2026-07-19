# Drupal Accessibility Patch Evaluation Packet

> Use this for one patch and one accessibility issue pattern. Do not mark a patch verified unless the baseline violation was observed before the patch and the same targeted check passes after the patch.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-PROJECT-NNN-short-description` |
| Source status | Example: `Core patch ready`, `Core investigation`, `Haven verified`, or `Haven patch needed` |
| Local status | `NOT STARTED`, `DRAFT`, `BASELINE VERIFIED`, `PATCH HYGIENE BLOCKED`, `TEST STATE BLOCKED`, `INCONCLUSIVE`, `NEEDS PATCH`, `FAILED`, `VERIFIED`, or `OBSOLETE` |
| Manual status | `not_run`, `debt_explicit`, or `complete` |
| Owner / run ID |  |
| Report path |  |
| Project/package |  |
| Target commit |  |
| Patch file |  |
| Evaluation date |  |
| Evaluator |  |
| AI assistance disclosed? | `yes/no` |

## Issue Summary

| Field | Value |
|---|---|
| Rule/source | Example: `axe-core color-contrast` |
| Tool version | Example: `@axe-core/playwright 4.11` |
| WCAG SC | Example: `1.4.3 Contrast (Minimum)` |
| Impact | Example: `serious` |
| User groups affected | Example: `low vision`, `screen reader`, `voice control` |
| Route(s) |  |
| Selector(s) |  |
| Pattern ID(s) |  |
| Instance ID(s) |  |
| Theme/profile/modules |  |
| Auth/content state |  |
| Viewport(s) |  |
| Color mode / forced colors / direction |  |

## Baseline Evidence

### Baseline Command

```bash
# Run against the unpatched site.
BASE_URL=https://example.ddev.site npx playwright test path/to/a11y.spec.js --grep "rule-or-patch-id"
```

### Baseline Result

```text
Expected: the target rule appears on the target selector.
Observed:
```

### Baseline HTML or Accessibility Snapshot

```html
<!-- Include the smallest useful snippet that proves the failure. -->
```

### Baseline Acceptance Gate

- [ ] The target violation was observed before applying the patch.
- [ ] The observed selector matches the packet selector.
- [ ] Pattern/instance IDs are captured when the scanner or report provides them.
- [ ] The observed WCAG/rule mapping matches the issue summary.
- [ ] Required interaction state was reached before scanning, if applicable.

If any item is unchecked, status must be `TEST STATE BLOCKED` or `INCONCLUSIVE`, not `VERIFIED`.

## Patch Hygiene

### Apply Check

```bash
git apply --check path/to/patch.patch
```

Result:

```text

```

### Apply, Build, Cache

```bash
git apply path/to/patch.patch
# If theme/CSS/JS changes:
npm run build
# If Drupal render/cache state matters:
ddev drush cache-rebuild
```

### Patch Hygiene Gate

- [ ] Patch applies cleanly to the target commit.
- [ ] Target files exist and match the packet.
- [ ] Build steps were run where required.
- [ ] Drupal caches were rebuilt where required.
- [ ] Revert command is known: `git apply -R path/to/patch.patch`.

If any item is unchecked, status must be `PATCH HYGIENE BLOCKED`, not `VERIFIED`.

## After-Patch Verification

### Targeted Re-Scan Command

```bash
# Run the same targeted check used for baseline verification.
BASE_URL=https://example.ddev.site npx playwright test path/to/a11y.spec.js --grep "rule-or-patch-id"
```

### Targeted Re-Scan Result

```text
Expected: the target rule no longer appears on the target selector.
Observed:
```

### Broad Regression Command

```bash
BASE_URL=https://example.ddev.site npx playwright test path/to/a11y.spec.js
```

### Broad Regression Result

```text
Expected: no new violations introduced by the patch.
Observed:
```

### Verification Gate

- [ ] Same targeted command was used before and after the patch.
- [ ] Target rule is absent on the target selector after the patch.
- [ ] Broad scan was run after the patch.
- [ ] New violations, if any, are listed and classified.
- [ ] Remaining adjacent issues are separated from the fixed issue.
- [ ] The packet does not claim that adjacent issues are fixed by this patch.

## Manual and Perspective Verification

Use this section to track checks that automated tools cannot fully prove.

| Check | Environment | Result | Notes |
|---|---|---|---|
| Keyboard-only | Browser/version | `not run`, `pass`, `fail` |  |
| NVDA + Chrome | Versions | `not run`, `pass`, `fail` |  |
| VoiceOver + Safari | Versions | `not run`, `pass`, `fail` |  |
| Voice control / label in name | Tool/version | `not run`, `pass`, `fail` |  |
| Forced colors | Browser/version | `not run`, `pass`, `fail` |  |
| Zoom/reflow | Browser/version | `not run`, `pass`, `fail` |  |

Manual checks may remain open, but the packet must say so plainly. If any expected manual check is still `not run`, set manual status to `debt_explicit` and list the debt in the outcome. Do not mark the packet `VERIFIED` unless every required manual check has a recorded result.

## Outcome

Choose one:

- `VERIFIED`: baseline reproduced, patch applies, targeted after-scan passes, broad regression scan has no patch-owned regressions, and manual status is `complete`.
- `INCONCLUSIVE`: evidence is incomplete, target baseline cannot be reproduced, or automated evidence passes but required manual checks remain open.
- `FAILED`: baseline reproduced, patch applies, but the target issue remains or a patch-owned regression appears.
- `PATCH HYGIENE BLOCKED`: patch cannot be applied, target file is missing, or build/cache steps fail.
- `TEST STATE BLOCKED`: route/content/theme/auth/viewport/interaction state does not reproduce the baseline.
- `NEEDS PATCH`: the issue is reproduced but no usable patch is available yet.
- `OBSOLETE`: the target issue or patch target no longer exists in the tested source, with evidence.

## Root Cause and Fix Narrative

### Root Cause

Describe why the failure happened in user-impact terms.

### Fix

Describe the smallest code change that fixes the issue and why it matches the WCAG criterion.

### Diff Summary

```diff

```

## Drupal.org Issue Block

### Title

`[Accessibility] Component/route fails rule-name: short user-impact summary`

### Steps to Reproduce

1. TODO
2. TODO
3. TODO

### Expected Result


### Actual Result


### Proposed Resolution


### Evidence

- Before scan:
- Patch:
- After scan:
- Broad regression scan:
- Manual checks:

### Tags

- `Accessibility`
- Add project/component-specific tags as appropriate.

### AI Assistance Disclosure

This packet and/or patch was prepared with AI assistance. The accessibility finding was verified with the evidence above and was not filed from AI code inspection alone.

## accessibility-skills Review Checklist

- [ ] `a11y-test` measured the target rule, keyboard behavior, or color/visual condition.
- [ ] `a11y-critic` reviewed the packet for evidence gaps, WCAG mapping, severity, and overclaiming.
- [ ] `perspective-audit` was escalated if the patch affects a perspective-sensitive workflow.
