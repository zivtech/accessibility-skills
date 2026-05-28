# Drupal Accessibility Evaluation Packet: DRUPAL-A11Y-011 Empty Heading Elements

> Status: OBSOLETE
> Prepared: 2026-05-28
> Purpose: Resolve the stale `DRUPAL-A11Y-011-empty-heading-elements` tracking row.

## Packet Header

| Field | Value |
|---|---|
| Item ID | `DRUPAL-A11Y-011-empty-heading-elements` |
| Status | `OBSOLETE` |
| Project/package | `mgifford/drupal-core` |
| Source status | `Core investigation` |
| Replacement item | `DRUPAL-A11Y-012-empty-heading-elements` |
| Triage report | `docs/drupal-patch-evaluations/reports/baseline-repair/2026-05-28-empty-heading-id-triage-hume.md` |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Reason

The current row conflates two IDs. The pattern report maps canonical `011` to `landmark-unique` on `/message`; empty heading elements are canonical `012` on `/dialog` and `/tabs`.

## Outcome

`OBSOLETE`

Next action: track active empty-heading work as `DRUPAL-A11Y-012-empty-heading-elements`.
