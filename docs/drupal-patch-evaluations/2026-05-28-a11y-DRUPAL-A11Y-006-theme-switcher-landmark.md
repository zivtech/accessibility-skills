# Drupal Accessibility Patch Evaluation Packet: DRUPAL-A11Y-006 Theme Switcher Landmark

> Status: FAILED
> Prepared: 2026-05-28
> Purpose: Local evaluator packet for Mike Gifford's current `a11y-DRUPAL-A11Y-006-theme-switcher-landmark` patch.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-DRUPAL-A11Y-006-theme-switcher-landmark` |
| Status | `FAILED` |
| Project/package | `mgifford/drupal-core` |
| Target commit checked | `3728741f23122018f1f26206fe563cb6c9ad49f8` (`main` on 2026-05-28) |
| Local runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| Evaluation artifact | `docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-006-theme-switcher-landmark-evaluation-codex-runtime-smoke-006.{md,json}` |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Local Evaluator Result

Command:

```bash
cd /Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
DRUPAL_BASE_URL=http://drupal-core.ddev.site:33000 \
  A11Y_VARIANT_ID=codex-runtime-smoke-006 \
  node core/tests/playwright/scripts/evaluate-patch.js \
  a11y-DRUPAL-A11Y-006-theme-switcher-landmark
```

Result:

```text
Status: FAIL
Outcome reason: new-violations-introduced
Case generation mode: pattern-report-derived
Baseline observed instances: 8
Fixed instances after patch: 0
Remaining instances after patch: 8
Introduced new violations: 1
```

The patch applied and reverted cleanly, but the target `region` pattern was unchanged across the observed routes. The run also reported one new `heading-order` violation.

## Gates

- [x] Baseline target observed before patch.
- [x] Patch applied and reverted.
- [x] Same route and state tested after patch.
- [ ] Target rule absent after patch.
- [ ] No new violations introduced.
- [ ] Manual landmark navigation review completed.

## Outcome

`FAILED`

The current patch does not fix the observed theme-switcher/region pattern and introduces at least one new violation in the evaluator run. Next action: re-scope the patch to the actual theme switcher render path and run a design review before rerolling; wrapping broad form/page regions risks replacing one landmark problem with another.
