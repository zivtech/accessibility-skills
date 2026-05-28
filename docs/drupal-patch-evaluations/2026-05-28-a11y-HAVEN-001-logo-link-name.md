# Drupal CMS Haven Accessibility Packet: HAVEN-001 Logo Link Name

> Status: DRAFT
> Prepared: 2026-05-28
> Purpose: Local QA packet stub for Mike Gifford's Haven `a11y-HAVEN-001-logo-link-name` patch.

## Packet Header

| Field | Value |
|---|---|
| Patch ID | `a11y-HAVEN-001-logo-link-name` |
| Status | `DRAFT` |
| Project/package | `mgifford/drupal-cms` |
| Source status | `Haven verified` |
| Local runtime | Not created in this repo |
| Source triage | `docs/drupal-patch-evaluations/reports/haven-verified-qa/2026-05-28-haven-source-triage-boyle.md` |
| Packet readiness triage | `docs/drupal-patch-evaluations/reports/haven-verified-qa/2026-05-28-haven-packet-readiness-faraday.md` |
| Upstream patch | `https://github.com/mgifford/drupal-cms/blob/main/patches/haven-a11y/a11y-HAVEN-001-logo-link-name.patch` |
| Upstream evaluation | `https://github.com/mgifford/drupal-cms/blob/main/patches/haven-a11y/a11y-HAVEN-001-logo-link-name-evaluation.md` |
| AI assistance disclosed? | Required if this packet is reused upstream |

## Current Evidence

Upstream evaluation is the positive source example for this row. Local packet QA still needs a current Drupal CMS/Haven checkout check before this repo should repeat the `VERIFIED` claim.

## Open Debt

- Run local `git apply --check` against a current Drupal CMS/Haven checkout.
- Confirm target-file drift has not invalidated the patch.
- Preserve the `aria-label` plus decorative `alt=""` rationale.
- Complete or explicitly defer NVDA + Chrome and VoiceOver + Safari manual checks.

## Outcome

`DRAFT`

Next action: run local patch hygiene against a current Drupal CMS/Haven checkout and carry the two manual AT checks as open debt.
