# Baseline Repair Source Triage - 2026-05-28

## Scope

Read-only source triage for baseline-repair and investigation items:

- `DRUPAL-A11Y-001`
- `DRUPAL-A11Y-003`
- `DRUPAL-A11Y-004`
- `DRUPAL-A11Y-010`
- `DRUPAL-A11Y-011`

## Agent

| Field | Value |
|---|---|
| Agent | Herschel |
| Role | Explorer |
| Run ID | `2026-05-28-baseline-source-triage-herschel` |
| Upstream commit checked | `mgifford/drupal-core` main `3728741f...` |
| Edits made | None |

## Upstream Batch State

The May 7 patch summary has 10 inconclusive, 0 passed, and 0 actionable baseline-observed patches. It names `DRUPAL-A11Y-001`, `DRUPAL-A11Y-003`, and `DRUPAL-A11Y-004` as test-state triage because the baseline was not reproduced.

## Findings

| Item | Baseline state needed | Current source status | Related refs | Next action |
|---|---|---|---|---|
| `DRUPAL-A11Y-001-file-widget-display-labels` | Route `/contact/imagefile_file`; enable `theming_tools:imagefile` with contact/image/file config and pre-existing file defaults; auth account that can view the contact form; Claro variants. | Proposed patch is marked ready for 4 unnamed file-display checkboxes, but latest eval is inconclusive / baseline not reproduced. Pattern report expects `#edit-imagefile-file-limited-N-display` with missing label. | `PROPOSED-PATCHES.md`, `PATCH-EVALUATION-SUMMARY.md`, `PATTERN-REPORT-latest.md`, item eval MD. | Reinstall/verify `imagefile` fixture defaults and confirm the checkbox HTML before applying the patch. |
| `DRUPAL-A11Y-003-select-all-checkbox-label` | `/admin/content`, `/admin/people`, or `/table`; rows must exist and expose bulk-select header checkbox; admin/auth user with relevant list permissions; admin/default_admin and Claro variants. | Proposed patches are marked ready for table + Views templates, but latest eval is inconclusive / baseline not reproduced. Pattern report still describes title-only select-all checkboxes. | `PROPOSED-PATCHES.md`, `PATCH-EVALUATION-SUMMARY.md`, `reports/patches/INDEX.md`, `PATTERN-REPORT-latest.md`. | Seed list rows or use `/table`, then confirm `input[title="Select all rows in this table"]` exists before patch testing. |
| `DRUPAL-A11Y-004-tabindex-buttons-test-form` | Route `/buttons`; enable theming tools button module; no content seed needed; auth with `access content`; Claro variants. | Proposed patch is marked ready, latest eval is inconclusive / baseline not reproduced. Pattern report expects `tabindex="1"` on `#edit-submit`. Source triage should verify patch target, because `/buttons` maps to theming-tools `ButtonTestForm`, not the form-test class named in the proposed summary. | `PROPOSED-PATCHES.md`, `PATCH-EVALUATION-SUMMARY.md`, `PATTERN-REPORT-latest.md`, item eval MD. | Reproduce `/buttons` with the real `ButtonTestForm`, then reroll the patch target if it is still aimed at the wrong class. |
| `DRUPAL-A11Y-010-heading-order` | `/admin/content`; seed enough content to render pager/pagination heading; admin/auth user with content overview access; admin/default_admin and Claro variants. | No patch in evaluator; proposed index says needs investigation, but mentions `/admin/modules`; current pattern report points to `/admin/content` `#pagination-heading` as `heading-order`. | `PROPOSED-PATCHES.md`, `PATTERN-REPORT-latest.md`. | Reproduce with a paged `/admin/content` list and decide whether this is pager markup, page hierarchy, or fixture noise. |
| `DRUPAL-A11Y-011-empty-heading-elements` | If following local/proposed scope: `/dialog` and `/tabs`, with dialog/off-canvas interaction state if needed; enable theming tools dialog/tab modules; auth with `access content`; admin/default_admin and Claro variants. | Source ID conflict: proposed index calls `011` empty headings, but current pattern report maps `011` to `landmark-unique` on `/message` and maps `empty-heading` to `012` on `/dialog` + `/tabs`. | `PROPOSED-PATCHES.md`, `PATTERN-REPORT-latest.md`. | Resolve the canonical ID first. If preserving local `011 = empty headings`, explicitly remap it to upstream pattern `DRUPAL-A11Y-012` before running. |

## Sources Used

- `https://github.com/mgifford/drupal-core/blob/main/reports/PATCH-EVALUATION-SUMMARY.md`
- `https://github.com/mgifford/drupal-core/blob/main/patches/PROPOSED-PATCHES.md`
- `https://github.com/mgifford/drupal-core/blob/main/reports/PATTERN-REPORT-latest.md`
- `https://github.com/mgifford/drupal-core/blob/main/reports/patches/INDEX.md`

## Integration Note

This report updates source triage and next actions only. It does not prove local baseline reproduction or local patch validity.
