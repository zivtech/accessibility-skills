# Drupal Accessibility Evaluation Packet: DRUPAL-A11Y-012 Empty Heading Elements

> Status: VERIFIED
> Prepared: 2026-05-28
> Purpose: Start the active empty-heading tracking row after resolving the stale `011` conflict.

## Packet Header

| Field | Value |
|---|---|
| Item ID | `DRUPAL-A11Y-012-empty-heading-elements` |
| Status | `VERIFIED` |
| Project/package | `mgifford/drupal-core` |
| Source status | `Core investigation` |
| Local runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| Candidate routes | `/dialog`, `/tabs` |
| Rule | `empty-heading` |
| Patch candidate | `docs/drupal-patch-evaluations/patches/a11y-DRUPAL-A11Y-012-empty-heading-elements-codex-filter-tips-preprocess.patch` |
| Triage report | `docs/drupal-patch-evaluations/reports/baseline-repair/2026-05-28-empty-heading-id-triage-hume.md` |
| Focused baseline check | `docs/drupal-patch-evaluations/reports/baseline-repair/2026-05-28-focused-baseline-check-main.md` |
| Continuation report | `docs/drupal-patch-evaluations/reports/current-wave/2026-05-28-continuation-007-012-evidence.md` |
| Critic gate | `docs/drupal-patch-evaluations/reports/current-wave/2026-05-28-012-critic-gate.md` |
| Upstream handoff draft | `docs/drupal-patch-evaluations/reports/current-wave/2026-05-28-012-upstream-handoff.md` |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Current Evidence

The source report maps empty heading elements to canonical `DRUPAL-A11Y-012`, not `011`.

Local focused checks reproduced the baseline:

```text
Route: /dialog
Rule: empty-heading
Heading selector count: 14
Violation nodes: 4

Route: /tabs
Rule: empty-heading
Heading selector count: 14
Violation nodes: 4
```

Observed failing nodes were empty `h3` elements.

## Patch Candidate

Root cause: `filter-tips.html.twig` expects normalized `tip.name` and `tip.list` variables, but the raw `filter_tips` theme hook data was reaching the template without a core preprocess step. On the `/dialog` and `/tabs` fixture routes, that produced empty text-format headings.

Candidate fix: add `FilterThemeHooks::preprocessFilterTips()` and wire it as the initial preprocess callback for `filter_tips`.

The refreshed patch also includes a focused kernel regression test:

```text
core/modules/filter/tests/src/Kernel/FilterTipsRenderTest.php
```

The test covers:

- single-format long filter tips rendered through Claro, where the bug produced an empty `h3`;
- multi-format long filter tips rendered through Claro;
- direct preprocess normalization for `tip.name`, format-level `attributes`, and per-item `attributes`.

Targeted before/after evidence:

| Route | Before `empty-heading` nodes | After `empty-heading` nodes |
|---|---:|---:|
| `/dialog` | 4 | 0 |
| `/tabs` | 4 | 0 |
| `/tabs/format/plain_text` | 1 | 0 |

After patch, the previously empty `h3` elements render text-format names such as `Basic HTML`, `Restricted HTML`, `Full HTML`, and `Plain text`.

Broad regression evidence on the affected routes showed no new axe rule families:

| Route | Before default axe total | After default axe total | Remaining rules after patch |
|---|---:|---:|---|
| `/dialog` | 5 | 1 | `region` |
| `/tabs` | 8 | 4 | `heading-order`, `region` |
| `/tabs/format/plain_text` | 4 | 3 | `heading-order`, `region` |

Additional shared-surface smoke checks passed on `/admin/config/content/formats`, `/admin/config/content/formats/manage/basic_html`, and `/node/add/page`, with `empty-heading` at zero after patch.

Regression test evidence:

```text
php -l core/modules/filter/tests/src/Kernel/FilterTipsRenderTest.php: pass
php -l core/modules/filter/src/Hook/FilterThemeHooks.php: pass
phpunit core/modules/filter/tests/src/Kernel/FilterTipsRenderTest.php: OK (3 tests, 10 assertions)
```

## Outcome

`VERIFIED` for the local patch candidate with a core regression test included in the patch artifact.

Next action: post or adapt the upstream handoff draft, with AI assistance disclosed if reused externally.
