# Drupal CMS Haven Accessibility Packet: HAVEN-003 Email Input Boundary Contrast

> Status: DRAFT
> Prepared: 2026-05-28
> Purpose: Local planning packet stub for the Haven `#edit-email` input boundary contrast issue.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-HAVEN-003-email-input-boundary-contrast` |
| Status | `DRAFT` |
| Project/package | `mgifford/drupal-cms` |
| Source status | `Haven patch needed` |
| Local runtime | Not created in this repo |
| Source triage | `docs/drupal-patch-evaluations/reports/haven-verified-qa/2026-05-28-haven-source-triage-boyle.md` |
| Packet readiness triage | `docs/drupal-patch-evaluations/reports/haven-verified-qa/2026-05-28-haven-packet-readiness-faraday.md` |
| Upstream proposal | `https://github.com/mgifford/drupal-cms/blob/main/patches/haven-a11y/PROPOSED-PATCHES.md` |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Current Evidence

The upstream Haven work separates this from `HAVEN-002`. There is no local patch or evaluation artifact yet, so this row should not be local `NEEDS PATCH` until the exact baseline has been reproduced in the Haven scan setup.

## Accessibility Contract

This should be mapped to WCAG 1.4.11 non-text contrast for input boundaries, not WCAG 1.4.3 text contrast.

## Open Debt

- Reproduce the `#edit-email` boundary contrast baseline under the Haven scan setup.
- Decide whether the right implementation path is token darkening or an explicit input border.
- Capture default, focus, disabled, dark mode, and forced-colors behavior.

## Outcome

`DRAFT`

Next action: reproduce the `#edit-email` boundary contrast baseline under the Haven scan setup, then choose the token/border fix path.
