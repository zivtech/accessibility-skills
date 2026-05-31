# Mike Review Queue

> Date: 2026-05-28
> Purpose: Triage the current Drupal accessibility review artifacts into a practical sharing order.

## Ready To Share As Infrastructure

### Evaluator Support Patch

Upstream PR:

```text
https://github.com/mgifford/drupal-core/pull/8
```

State as of 2026-05-30: open, not draft. Branch: `AlexU-A:codex/evaluator-support-mike-20260529`.

Artifact:

```text
docs/drupal-patch-evaluations/patches/evaluator-support/codex-evaluator-support-baseurl-rule-alias-runonly-selector-hints.patch
```

Handoff:

```text
docs/drupal-patch-evaluations/reports/current-wave/2026-05-28-evaluator-support-upstream-handoff.md
```

Why first: several packet outcomes depend on evaluator behavior that was previously too brittle. This patch is not an accessibility remediation, but it makes the evidence pipeline more trustworthy. It has now been opened upstream as PR #8 for Mike review.

Review ask:

- Should this land as one evaluator-reliability patch, or split into helper restoration, base-URL portability, and rule/selector matching?
- Is the hardcoded DDEV hostname intended policy, or just a local default that should allow environment overrides?
- Is there an existing test harness for evaluator scripts where these behaviors should be covered?

## Ready To Share As A Scoped Accessibility Patch

### `DRUPAL-A11Y-012-empty-heading-elements`

Upstream PR:

```text
https://github.com/mgifford/drupal-core/pull/9
```

State as of 2026-05-31: open, not draft, merge state `CLEAN`. Branch: `AlexU-A:codex/filter-tips-empty-heading-20260530`.

Patch:

```text
docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-012-empty-heading-elements-codex-filter-tips-preprocess.patch
```

Packet:

```text
docs/drupal-patch-evaluations/2026-05-28-a11y-DRUPAL-A11Y-012-empty-heading-elements.md
```

Handoff:

```text
docs/drupal-patch-evaluations/reports/current-wave/2026-05-28-012-upstream-handoff.md
```

Why second: this is the cleanest remediation candidate. It has a narrow source cause, before/after axe evidence, and a focused kernel regression test. It has now been opened upstream as PR #9 for Mike review.

Review ask:

- Does `FilterThemeHooks::preprocessFilterTips()` belong as the initial preprocess callback for `filter_tips`?
- Are the normalized `tip.name`, `tip.list`, format attributes, and per-item attributes the right public shape for Claro and Default Admin templates?
- Should the separate home-page empty `h1` evidence stay out of this issue?

## Opened Upstream As A Scoped Accessibility Patch

### `DRUPAL-A11Y-010-heading-order`

Upstream PR:

```text
https://github.com/mgifford/drupal-core/pull/10
```

State as of 2026-05-31: open, not draft, merge state `CLEAN`, AccessLint pass. Branch: `AlexU-A:codex/content-pager-heading-20260531`.

Patch:

```text
docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-010-heading-order-codex-content-pager-heading-level.patch
```

Packet:

```text
docs/drupal-patch-evaluations/2026-05-28-a11y-DRUPAL-A11Y-010-heading-order.md
```

Handoff:

```text
docs/drupal-patch-evaluations/reports/current-wave/2026-05-28-010-upstream-handoff.md
```

Why scoped: the pager finding is real and now has default config, post-update, rendered-page, and post-update test coverage. It still does not address the datetime wrapper or multiple-value field heading-order families. The admin block family has since been split into PR #15.

Review ask:

- Is changing the default Content view pager heading to `h2` the right semantic level for `/admin/content`?
- Is the post-update narrow enough: update only existing active Content views that still have `h4`, and preserve other values?
- Should the non-pager route families become separate follow-up issues rather than one broad heading-order patch?

### `LABEL-IN-NAME-004-filter-format-aria-label`

Upstream PR:

```text
https://github.com/mgifford/drupal-core/pull/11
```

State as of 2026-05-31: open, not draft, merge state `CLEAN`, AccessLint pass. Branch: `AlexU-A:codex/filter-format-label-in-name-20260531`.

Patch:

```text
docs/drupal-patch-evaluations/patches/a11y-LABEL-IN-NAME-004-filter-format-aria-label-codex-configure-link-label.patch
```

Packet:

```text
docs/drupal-patch-evaluations/2026-05-28-a11y-LABEL-IN-NAME-004-filter-format-aria-label.md
```

Handoff:

```text
docs/drupal-patch-evaluations/reports/current-wave/2026-05-31-label-in-name-004-upstream-handoff.md
```

Why scoped: the issue is limited to filter format Configure operation links whose visible text is changed after the parent entity list builder has already assigned an `Edit ...` accessible name. The patch aligns the accessible name with the visible label and adds functional regression coverage.

Review ask:

- Is updating the operation URL attributes in `FilterFormatListBuilder` the right local fix for this override?
- Should any broader entity-list-builder follow-up be separate from this scoped filter-format patch?
- Is the functional assertion enough, given the added keyboard-user smoke evidence?

### `DRUPAL-A11Y-004-tabindex-buttons-test-form`

Upstream PR:

```text
https://github.com/mgifford/drupal-core/pull/12
```

State as of 2026-05-31: open, not draft, merge state `CLEAN`, AccessLint pass. Branch: `AlexU-A:codex/tabindex-buttons-test-form-20260531`.

Patch:

```text
docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-004-tabindex-buttons-test-form-codex-remove-positive-tabindex.patch
```

Packet:

```text
docs/drupal-patch-evaluations/2026-05-28-a11y-DRUPAL-A11Y-004-tabindex-buttons-test-form.md
```

Handoff:

```text
docs/drupal-patch-evaluations/reports/current-wave/2026-05-31-004-tabindex-buttons-upstream-handoff.md
```

Why scoped: the failing route is `/buttons`, rendered by `ButtonTestForm`, not the earlier `FormTestClickedButtonForm` target. The patch removes positive `tabindex` instead of replacing it with `-1`, preserving native keyboard reachability and DOM tab order.

Review ask:

- Was the positive `tabindex` in the button fixture intentional as an anti-pattern demo, or should the fixture avoid shipping axe-detectable keyboard failures?
- Is the functional assertion enough alongside the evaluator pass and real keyboard Tab-order smoke?
- Should the two remaining `/buttons` `region` violations stay in a separate fixture/layout issue?

### `DRUPAL-A11Y-003-select-all-checkbox-label`

Upstream PR:

```text
https://github.com/mgifford/drupal-core/pull/13
```

State as of 2026-05-31: open, not draft, merge state `CLEAN`, AccessLint pass. Branch: `AlexU-A:codex/select-all-checkbox-label-20260531`.

Patch:

```text
docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-003-select-all-checkbox-label-codex-select-all-aria-label.patch
```

Packet:

```text
docs/drupal-patch-evaluations/2026-05-28-a11y-DRUPAL-A11Y-003-select-all-checkbox-label.md
```

Handoff:

```text
docs/drupal-patch-evaluations/reports/current-wave/2026-05-31-003-select-all-checkbox-upstream-handoff.md
```

Why scoped: the original patch added `aria-label` only in a Default Admin Twig path, but the live Claro/core target can be inserted by `core/misc/tableselect.js`. The reroll replaces title-only labeling with `aria-label` across core table-select behavior and Default Admin sticky header paths, and removes `title` to avoid duplicate accessible name/description output.

Review ask:

- Is replacing the title-only select-all checkbox label with `aria-label` acceptable for core table-select behavior?
- Should the Default Admin sticky header paths stay in this same patch because they hardcode the same checkbox?
- Is removing `title` acceptable to avoid duplicate accessible name/description output, even though it removes the old browser tooltip?

### `DRUPAL-A11Y-006-theme-switcher-landmark`

Upstream PR:

```text
https://github.com/mgifford/drupal-core/pull/14
```

State as of 2026-05-31: open, not draft, merge state `CLEAN`, AccessLint pass. Branch: `AlexU-A:codex/theme-switcher-form-landmark-20260531`.

Patch:

```text
docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-006-theme-switcher-landmark-codex-form-landmark-006.patch
```

Packet:

```text
docs/drupal-patch-evaluations/2026-05-28-a11y-DRUPAL-A11Y-006-theme-switcher-landmark.md
```

Handoff:

```text
docs/drupal-patch-evaluations/reports/current-wave/2026-05-31-006-theme-switcher-upstream-handoff.md
```

Why scoped: the old patch wrapped a broad Default Admin layout in `nav`, which was neither the actual render path nor the right semantic claim. The reroll names the actual `ThemeSwitcherForm` wrapper so the fixed preference control is exposed as a native form landmark. The evaluator matched and fixed the targeted `region` instances it observed, but still returned overall FAIL because unrelated `/admin/config` heading-order state noise appeared after status-message state changed.

Review ask:

- Is a named native form landmark the right semantic treatment for the fixed theme switcher preference control?
- Should the evaluator metadata be corrected separately so the issue is no longer described as a `nav` wrapper?

### `DRUPAL-A11Y-010-admin-block-heading-order`

Upstream PR:

```text
https://github.com/mgifford/drupal-core/pull/15
```

State as of 2026-05-31: open, not draft, merge state `CLEAN`, AccessLint pass. Branch: `AlexU-A:codex/admin-block-heading-order-20260531`.

Patch:

```text
docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-010-admin-block-heading-order-codex-admin-block-heading-level.patch
```

Packet:

```text
docs/drupal-patch-evaluations/2026-05-31-a11y-DRUPAL-A11Y-010-admin-block-heading-order.md
```

Handoff:

```text
docs/drupal-patch-evaluations/reports/current-wave/2026-05-31-010-admin-block-heading-upstream-handoff.md
```

Why scoped: this is the admin block panel title family split out from the broader `DRUPAL-A11Y-010` heading-order reproduction. The patch changes active `admin_block` panel titles from `h3` to `h2` in the core system template and Default Admin override, with functional coverage and an exact-route `/cd-navigation/config` Playwright/axe smoke. It does not change datetime wrapper labels, multiple-value field labels, or Stable 9's deprecated compatibility markup.

Review ask:

- Is `h2` the right heading level for admin block panel titles under admin overview page `h1` headings?
- Should this remain separate from the existing Content view pager heading PR?
- Is leaving Stable 9 unchanged the right BC boundary for this patch?

### `DRUPAL-A11Y-010-multiple-value-field-heading-order`

Upstream PR:

```text
https://github.com/mgifford/drupal-core/pull/16
```

State as of 2026-05-31: open, not draft, merge state `CLEAN`, AccessLint pass. Branch: `AlexU-A:codex/multiple-value-field-heading-order-20260531`.

Patch:

```text
docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-010-multiple-value-field-heading-order-codex-multiple-value-field-label.patch
```

Packet:

```text
docs/drupal-patch-evaluations/2026-05-31-a11y-DRUPAL-A11Y-010-multiple-value-field-heading-order.md
```

Handoff:

```text
docs/drupal-patch-evaluations/reports/current-wave/2026-05-31-010-multiple-value-field-heading-upstream-handoff.md
```

Why scoped: this is the multiple-value field label family split out from the broader `DRUPAL-A11Y-010` heading-order reproduction. The patch removes redundant nested `h4` markup from multiple-value field table labels while keeping the label text inside the existing table header cell and preserving the active theme styling classes. It includes core functional coverage, Olivero unit coverage, and exact-route `/contact/field_cardinality_test`, `/contact/presuf_formatted`, and `/contact/presuf_number` Playwright/axe smoke. It does not change datetime wrapper labels, pager headings, or admin block panel titles.

Review ask:

- Is replacing the nested heading with non-heading text inside the existing table header cell the right semantic treatment?
- Should field table labeling stay scoped here, or does it need a broader follow-up beyond the heading-order violation?
- Are the Claro, Default Admin, and Olivero styling updates broad enough for the supported active themes?

## Needs Human AT Smoke Before Upstream Wording

### `DRUPAL-A11Y-007-messages-landmark-role`

Patch:

```text
docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-007-messages-landmark-role-codex-reroll-status-alert-007.patch
```

Packet:

```text
docs/drupal-patch-evaluations/2026-05-28-a11y-DRUPAL-A11Y-007-messages-landmark-role.md
```

Why blocked: local DOM and axe evidence supports the reroll, but the packet correctly says it is not AT-verified. Do not upgrade the claim to "screen reader verified" until a human NVDA or VoiceOver smoke check is done.

Review ask:

- Confirm whether warning/status messages are announced appropriately as `role="status"`.
- Confirm whether error messages interrupt appropriately as `role="alert"`.
- Confirm that changing the wrapper role from `contentinfo` does not remove a useful navigation affordance that users relied on.

## Explicit Non-Claims

This queue does not claim that all Mike Gifford Drupal accessibility patches are verified. It only organizes the current local evidence into shareable lanes.

It also does not claim that local evaluator passes are equivalent to assistive-technology validation. Axe/DOM evidence is useful, but it is not a substitute for human screen reader or voice-control checks where behavior depends on announcement timing or accessible-name matching.
