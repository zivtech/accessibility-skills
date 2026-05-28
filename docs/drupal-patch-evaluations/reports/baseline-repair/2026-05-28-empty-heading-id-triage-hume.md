# DRUPAL-A11Y-011 / DRUPAL-A11Y-012 Empty Heading ID Triage

> Agent: Hume
> Mode: read-only explorer
> Date: 2026-05-28
> Scope: Resolve the apparent `011` empty-heading conflict.

## Verdict

For the current row `DRUPAL-A11Y-011-empty-heading-elements`, recommended local status is `OBSOLETE`. The ID/name pairing is invalid against the pattern report, which states it is the source of truth for pattern IDs.

## Replacement Tracking

`DRUPAL-A11Y-012-empty-heading-elements` should be the active empty-heading item, with local status `DRAFT` until `/dialog` and `/tabs` baseline reproduction is done.

## Evidence

- `docs/drupal-patch-evaluations/reports/fixture-map/2026-05-28-theming-tools-fixture-map-lorentz.md:20` warned about the ID conflict.
- `docs/drupal-patch-evaluations/reports/baseline-repair/2026-05-28-baseline-source-triage-herschel.md:35` warned that source maps `011` to landmark uniqueness and empty headings to `012`.
- `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/patches/PROPOSED-PATCHES.md:110` is the stale/proposed mapping that calls `011` empty headings.
- `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/reports/PATTERN-REPORT-latest.md:22` identifies the pattern report as the source of truth.
- `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/reports/PATTERN-REPORT-latest.md:898` maps canonical `011` to `landmark-unique` on `/message`.
- `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime/reports/PATTERN-REPORT-latest.md:966` maps canonical `012` to `empty-heading` on `/dialog` and `/tabs`.

## Next Action

Mark `DRUPAL-A11Y-011-empty-heading-elements` obsolete and track the active empty-heading work as `DRUPAL-A11Y-012-empty-heading-elements` targeting `/dialog` and `/tabs`.
