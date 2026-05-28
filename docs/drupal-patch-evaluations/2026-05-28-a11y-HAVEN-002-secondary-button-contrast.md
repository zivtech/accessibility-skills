# Drupal CMS Haven Accessibility Packet: HAVEN-002 Secondary Button Contrast

> Status: DRAFT
> Prepared: 2026-05-28
> Purpose: Local QA packet stub for Mike Gifford's Haven `a11y-HAVEN-002-secondary-button-contrast` patch.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-HAVEN-002-secondary-button-contrast` |
| Status | `DRAFT` |
| Project/package | `mgifford/drupal-cms` |
| Source status | `Haven verified` |
| Local runtime | Not created in this repo |
| Source triage | `docs/drupal-patch-evaluations/reports/haven-verified-qa/2026-05-28-haven-source-triage-boyle.md` |
| Packet readiness triage | `docs/drupal-patch-evaluations/reports/haven-verified-qa/2026-05-28-haven-packet-readiness-faraday.md` |
| Upstream patch | `https://github.com/mgifford/drupal-cms/blob/main/patches/haven-a11y/a11y-HAVEN-002-secondary-button-contrast.patch` |
| Upstream evaluation | `https://github.com/mgifford/drupal-cms/blob/main/patches/haven-a11y/a11y-HAVEN-002-secondary-button-contrast-evaluation.md` |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Current Evidence

Upstream evaluation reports this as a verified Haven patch. The local QA gap is visual and build-state discipline rather than a new Drupal core evaluator run.

## Open Debt

- Run current patch hygiene against a Drupal CMS/Haven checkout.
- Include `npm run build` and cache rebuild steps in local reproduction.
- Check default, hover, focus, active, and disabled visual states.
- Check dark mode and high-contrast readability.
- Keep the related `#edit-email` boundary issue separate as `HAVEN-003`.

## Outcome

`DRAFT`

Next action: run packet QA plus the visual-state checklist before treating it as upstream-ready.
