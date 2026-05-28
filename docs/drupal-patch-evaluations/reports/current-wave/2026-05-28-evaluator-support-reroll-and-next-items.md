# Current Wave Report: Evaluator Support, 007 Reroll, and Next Items

> Date: 2026-05-28
> Workspace: `/Users/AlexUA_1/claude/a11y-meta-skills`
> Runtime: `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime`

## Parallel Agents

| Agent | Role | Result |
|---|---|---|
| Dirac | evaluator support review | Confirmed `label-in-name` needs aliasing to `label-content-name-mismatch`, explicit required-rule scans, selector matching, and that `canonical-patch-map.js` must be present for clean evaluator runs. |
| Dewey | `DRUPAL-A11Y-007` source analysis | Confirmed the old patch only changed the system template while Claro still emitted `role="contentinfo"` on `/admin/modules`; recommended status/error semantics over `region`. |
| Erdos | `010`/`012` source triage | Split `010` into pager, datetime, multiple-value field, and admin-block heading paths; split `012` into filter-tip empty `h3` and home-page empty `h1` paths. |
| Carver | critic gate | Accepted `LABEL-IN-NAME-004` as locally verified; accepted `007` with reservations and forced a DOM check for the server/client warning-role mismatch. |

## Evaluator Support

Local runtime evaluator changes now support:

- `DRUPAL_BASE_URL` / `DRUPAL_TEST_BASE_URL` for nonstandard DDEV ports.
- A restored `core/tests/playwright/scripts/lib/canonical-patch-map.js` helper.
- Rule aliasing from human packet labels to concrete axe rule IDs.
- Explicit `runOnly` scans for required axe rules that are not part of the default axe pass.
- Selector hint matching from configured Playwright selectors to concrete axe selectors.

Validation:

```bash
node --check core/tests/playwright/scripts/evaluate-patch.js
node --check core/tests/playwright/scripts/evaluate-all-patches.js
git diff --check -- core/tests/playwright/scripts/evaluate-patch.js core/tests/playwright/scripts/lib/canonical-patch-map.js
```

## Verified Items

### `LABEL-IN-NAME-004-filter-format-aria-label`

Report:

```text
docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-LABEL-IN-NAME-004-filter-format-aria-label-evaluation-codex-selector-hint-label-004.md
```

Result:

```text
Status: PASS
Outcome reason: targeted-issues-fixed-without-regressions
Baseline observed instances: 1
Fixed instances after patch: 1
Remaining instances after patch: 0
Fixed rule: label-content-name-mismatch 4 -> 0
```

### `DRUPAL-A11Y-007-messages-landmark-role`

Reroll patch:

```text
docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-007-messages-landmark-role-codex-reroll-status-alert-007.patch
```

Report:

```text
docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-007-messages-landmark-role-evaluation-codex-reroll-status-alert-js-007.md
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
```

Remaining caveat: run a short NVDA or VoiceOver smoke check before filing the reroll as user-verified upstream evidence.

Critic follow-up resolved: the first reroll left JavaScript-created warning messages as `role="alert"`. The final reroll now patches Drupal's JavaScript message themers too. A DOM probe with the final patch applied confirmed `/admin/appearance`, `/admin/modules`, and a JavaScript-created warning all render warnings as `role="status"` and errors as `role="alert"`.

## Next Patch Lanes

1. `DRUPAL-A11Y-012-empty-heading-elements`: patch/test filter tips first, especially `DialogController.php` and `TabController.php`; track the home-page empty `h1` as a separate path.
2. `DRUPAL-A11Y-010-heading-order`: split route families before patching: pager `#pagination-heading`, datetime wrapper `h4`, multiple-value field `h4`, and admin-block `h3`.
3. Evaluator upstreaming: move the runtime-only evaluator support into a clean branch after deciding whether `canonical-patch-map.js` should be committed or the import guarded.

## Talk-To-Drupal Pass

Saved reviews:

```text
/Users/AlexUA_1/Codex/drupal-core-reviews/2026-05-28-drupal-a11y-007-reroll-review.md
/Users/AlexUA_1/Codex/drupal-core-reviews/2026-05-28-drupal-a11y-007-packet-review.md
```

Both reviews returned `REVISE`. The raw patch review was a weak fit because the tool treated the patch like an ADR and complained about missing ADR sections. The packet review was more useful: it selected `site-builder-experience`, `eval-driven-rigor`, and `api-surface-discipline`, which reinforces three upstream-readiness requirements:

- explain the site-builder/admin accessibility value in plain terms,
- keep the before/after evaluator evidence tied to the same conditions,
- make the theme/template override surface explicit so the patch does not look like an ad hoc Claro-only fix.
