# Drupal Accessibility Patch Evaluation Packet: DRUPAL-A11Y-005 Language Switcher Contrast

> Status: OBSOLETE
> Prepared: 2026-05-28
> Last updated: 2026-05-31
> Purpose: Local evaluator packet for Mike Gifford's current `a11y-DRUPAL-A11Y-005-language-switcher-contrast` patch.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-DRUPAL-A11Y-005-language-switcher-contrast` |
| Status | `OBSOLETE` |
| Project/package | `mgifford/drupal-core` |
| Target commit checked | `3728741f23122018f1f26206fe563cb6c9ad49f8` (`main` on 2026-05-28) |
| Local runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| Evaluation artifact | `docs/drupal-patch-evaluations/reports/evaluator-runs/a11y-DRUPAL-A11Y-005-language-switcher-contrast-evaluation-codex-runtime-smoke-005.{md,json}` |
| Superseding packet | `docs/drupal-patch-evaluations/2026-05-28-a11y-DRUPAL-A11Y-002-submit-button-contrast.md` |
| Superseding PR | https://github.com/mgifford/drupal-core/pull/20 |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Local Evaluator Result

Command:

```bash
cd /Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime
DRUPAL_BASE_URL=http://drupal-core.ddev.site:33000 \
  A11Y_VARIANT_ID=codex-runtime-smoke-005 \
  node core/tests/playwright/scripts/evaluate-patch.js \
  a11y-DRUPAL-A11Y-005-language-switcher-contrast
```

Result:

```text
Status: INCONCLUSIVE
Outcome reason: baseline-not-observed-due-to-route-unavailable
Case generation mode: pattern-report-derived
Target pattern ID: DRU-F75A07EF
Routes attempted: /action-link, /admin, /admin/appearance, /admin/content, /admin/form_style, /admin/modules
Pages loaded successfully: 5/6
Baseline observed instances: 0
```

The evaluator confirmed that the patch is syntactically applicable in the disposable runtime, but it did not reproduce the targeted `color-contrast` baseline. The candidate pages included Hebrew-language links and submit/action-button selectors on five successful page loads, plus one unavailable route (`/admin/form_style`).

## Source Mismatch

The patch label says language switcher contrast, while the current source triage flagged a mismatch between that description and a button-text/default-admin accent target. The evaluator's generated candidates also mixed language-link selectors (`a[hreflang="he"]`) and button selectors (`#edit-submit`, `.button--action`), which makes the expected failing state too ambiguous for a patch verdict.

The later source reconciliation resolved the canonical measured failure to `DRUPAL-A11Y-002` / pattern `DRU-F75A07EF`: Default Admin orange accent links such as `a[hreflang="he"]` used `#c55228` on `#fefaf8` at 4.38:1. PR #20 fixes that shared orange accent source.

This packet is not a separate verified target. Its old raw patch changed button/accent CSS variables that do not match the canonical source report. If yellow-accent button contrast resurfaces with a current source report, open a fresh packet with the exact preset, route, selector, and measured baseline.

## Outcome

`OBSOLETE`

No separate upstream PR should be opened from this packet. Use `DRUPAL-A11Y-002` / PR #20 for the orange language-link contrast fix.
