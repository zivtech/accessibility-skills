# Continuation Report: 007 Rerun, Evaluator Support, and 012 Candidate

> Date: 2026-05-28
> Workspace: `/Users/AlexUA_1/claude/a11y-meta-skills`
> Runtime: `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime`

## Summary

This continuation preserved the `DRUPAL-A11Y-007` evidence chain, packaged the local evaluator-support changes as a reviewable patch artifact, and advanced the `DRUPAL-A11Y-012` patch lane from targeted before/after evidence to a patch artifact with a focused core regression test.

## DRUPAL-A11Y-007

Fresh cleaned evaluator rerun:

```text
docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-007-messages-landmark-role-evaluation-codex-rerun-cleaned-007.{md,json,html}
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

Additional role smoke:

```text
docs/drupal-patch-evaluations/reports/manual-checks/2026-05-28-drupal-a11y-007-role-smoke.md
```

The role smoke confirmed server-rendered and JavaScript-created warning messages use `role="status"` while errors use `role="alert"`. This is DOM/axe evidence, not a real NVDA or VoiceOver check.

## Evaluator Support Patch

Reviewable artifact:

```text
docs/drupal-patch-evaluations/patches/evaluator-support/codex-evaluator-support-baseurl-rule-alias-runonly-selector-hints.patch
```

It packages the runtime-only evaluator changes:

- `DRUPAL_BASE_URL` / `DRUPAL_TEST_BASE_URL` support.
- `label-in-name` aliasing to axe-core's `label-content-name-mismatch`.
- explicit `runOnly` scans for required rules outside the default axe pass.
- selector-hint matching for broad Playwright selectors such as `table a:has-text("Configure")`.
- restored `canonical-patch-map.js` loader.

Validation:

```text
node --check evaluate-patch.js: pass
node --check evaluate-all-patches.js: pass
node --check canonical-patch-map.js: pass
git diff --check for evaluator support and 007 patch: pass
```

## DRUPAL-A11Y-012

Patch candidate:

```text
docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-012-empty-heading-elements-codex-filter-tips-preprocess.patch
```

Root cause:

`filter-tips.html.twig` expects normalized `tip.name` and `tip.list` values, but `filter_tips` had no core preprocess step to normalize the raw format-label buckets. On the `/dialog` and `/tabs` fixture routes, this rendered empty `h3` elements for each text format.

Targeted before/after evidence:

| Route | Before `empty-heading` nodes | After `empty-heading` nodes |
|---|---:|---:|
| `/dialog` | 4 | 0 |
| `/tabs` | 4 | 0 |
| `/tabs/format/plain_text` | 1 | 0 |

After patch, the formerly empty headings rendered as real text format names:

```text
Basic HTML
Restricted HTML
Subtitle three
Full HTML
Plain text
```

Validation:

```text
php -l core/modules/filter/src/Hook/FilterThemeHooks.php: pass
php -l core/modules/filter/tests/src/Kernel/FilterTipsRenderTest.php: pass
phpunit core/modules/filter/tests/src/Kernel/FilterTipsRenderTest.php: OK (3 tests, 10 assertions)
ddev drush cache-rebuild: pass
targeted Playwright + axe-core empty-heading scan: pass
default axe regression scan on affected routes: pass, no new rule families
shared-surface smoke on /admin/config/content/formats, /admin/config/content/formats/manage/basic_html, and /node/add/page: pass
```

Broad regression summary:

| Route | Before default axe total | After default axe total | Remaining rules after patch |
|---|---:|---:|---|
| `/dialog` | 5 | 1 | `region` |
| `/tabs` | 8 | 4 | `heading-order`, `region` |
| `/tabs/format/plain_text` | 4 | 3 | `heading-order`, `region` |

Critic gate:

```text
docs/drupal-patch-evaluations/reports/current-wave/2026-05-28-012-critic-gate.md
```

Verdict: `ACCEPT`. The candidate can be treated as locally verified and the refreshed patch artifact now includes a core-appropriate kernel regression test for multi-format and single-format long filter tips.

Upstream handoff draft:

```text
docs/drupal-patch-evaluations/reports/current-wave/2026-05-28-012-upstream-handoff.md
```

## Remaining Work

- `DRUPAL-A11Y-007`: run one real NVDA or VoiceOver smoke check before calling the reroll AT-verified upstream evidence.
- Evaluator support: review the patch artifact and decide whether to upstream as one support patch or split `canonical-patch-map.js` into a separate helper restoration.
- `DRUPAL-A11Y-012`: post or adapt the upstream handoff draft, with AI assistance disclosed if reused externally.
- `DRUPAL-A11Y-010`: keep split by route family; do not start with a central heading patch until each route family is classified.
