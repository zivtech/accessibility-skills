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

Why scoped: the pager finding is real and now has default config, post-update, rendered-page, and post-update test coverage. It still does not address the datetime wrapper, multiple-value field, or admin block heading-order families.

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
