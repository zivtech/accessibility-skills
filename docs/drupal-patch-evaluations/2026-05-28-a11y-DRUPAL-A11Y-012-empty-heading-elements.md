# Drupal Accessibility Evaluation Packet: DRUPAL-A11Y-012 Empty Heading Elements

> Status: BASELINE VERIFIED
> Prepared: 2026-05-28
> Purpose: Start the active empty-heading tracking row after resolving the stale `011` conflict.

## Packet Header

| Field | Value |
|---|---|
| Item ID | `DRUPAL-A11Y-012-empty-heading-elements` |
| Status | `BASELINE VERIFIED` |
| Project/package | `mgifford/drupal-core` |
| Source status | `Core investigation` |
| Local runtime | `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/mgifford-drupal-core-runtime` |
| Candidate routes | `/dialog`, `/tabs` |
| Rule | `empty-heading` |
| Triage report | `docs/drupal-patch-evaluations/reports/baseline-repair/2026-05-28-empty-heading-id-triage-hume.md` |
| Focused baseline check | `docs/drupal-patch-evaluations/reports/baseline-repair/2026-05-28-focused-baseline-check-main.md` |
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

## Outcome

`BASELINE VERIFIED`

Next action: inspect the dialog and tabs fixture/render paths for the empty `h3` elements, then decide whether this is fixture noise or a patch-worthy core issue.
