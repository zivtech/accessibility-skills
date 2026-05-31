# Clean Evaluation Summary: DRUPAL-A11Y-008 Empty Table Headers

> Date: 2026-05-31
> Variant: `codex-field-operations-header-008`
> Runtime: `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime`
> Raw generated files: runtime-only, not committed

## Why This Replaced The Old Run

The previous `codex-runtime-smoke-008` evaluator run was inconclusive because `/autocomplete` returned 404. The fixture module existed but was not enabled.

The route was repaired with:

```bash
ddev drush en autocomplete -y
ddev drush cr
```

## Baseline

After enabling the fixture, `/autocomplete` returned 200 and rendered a multiple-value field table with one empty operations header:

```text
Header 1: Select some other countries
Header 2: [empty]
Header 3: Order
```

## Patch Under Test

Patch artifact:

```text
docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-008-empty-table-headers-codex-field-operations-header.patch
```

The patch labels the operations header at the field-multiple-value render source:

```text
<th><span class="visually-hidden">Operations</span></th>
```

## Evaluator Result

```text
Status: PASS
Outcome reason: targeted-issues-fixed-without-regressions
Route: /autocomplete
HTTP status: 200
Rule: empty-table-header
Axe violation count: 1 -> 0
Total violations: 3 -> 2
New violations introduced: 0
```

The two remaining axe violations were unrelated `heading-order` and `region` issues already present on the route.

## Artifact Hygiene

The generated JSON/HTML report files were not committed because they include local Drush status with database fields and redacted reset-link URLs. This clean summary preserves the actionable evidence without committing local runtime output.

## Boundary

The evaluator reported eight targeted selector instances for the source pattern. That is selector coverage, not eight distinct rendered empty header cells in this runtime. The observed live route had one empty `<th>` before patch and none after patch.
