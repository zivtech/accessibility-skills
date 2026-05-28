# Haven Packet Readiness Triage

> Agent: Faraday
> Mode: read-only explorer
> Date: 2026-05-28
> Scope: HAVEN-001, HAVEN-002, HAVEN-003

## Summary

Recommended ledger move: advance all three Haven rows to `DRAFT` once packet paths are created. None should be `VERIFIED`; `HAVEN-003` should not be local `NEEDS PATCH` until the baseline is reproduced.

## Item Findings

| Item | Recommended local status | Packet readiness gaps | Evidence | Next action |
|---|---|---|---|---|
| `HAVEN-001-logo-link-name` | `DRAFT` | No local current `git apply --check` or target-file drift check recorded; NVDA + Chrome and VoiceOver + Safari checks remain open; packet must preserve the `aria-label` and decorative `alt=""` rationale without overclaiming local verification. | `docs/drupal-patch-evaluations/reports/haven-verified-qa/2026-05-28-haven-source-triage-boyle.md`; upstream `PROPOSED-PATCHES.md#L22-L43`; upstream `a11y-HAVEN-001-logo-link-name-evaluation.md#L66-L103`; upstream `a11y-HAVEN-001-logo-link-name.patch`. | Run local patch hygiene against a current Drupal CMS/Haven checkout and carry the two manual AT checks as open debt. |
| `HAVEN-002-secondary-button-contrast` | `DRAFT` | Visual state checklist is incomplete for default, hover, focus, active, and disabled; dark-mode visual review and NVDA + Chrome high-contrast readability remain open; packet must include `npm run build` and cache rebuild steps; keep `#edit-email` separated as `HAVEN-003`. | `docs/drupal-patch-evaluations/reports/haven-verified-qa/2026-05-28-haven-source-triage-boyle.md`; upstream `PROPOSED-PATCHES.md#L47-L68`; upstream `PROPOSED-PATCHES.md#L99-L118`; upstream `a11y-HAVEN-002-secondary-button-contrast-evaluation.md#L89-L135`; upstream patch. | Run packet QA plus the visual-state checklist before treating it as upstream-ready. |
| `HAVEN-003-email-input-boundary-contrast` | `DRAFT` | No upstream patch or evaluation artifact; baseline reproduction is still owed; fix approach undecided between token darkening and explicit border; packet must map this to WCAG 1.4.11 non-text contrast, not WCAG 1.4.3 text contrast. | `docs/drupal-patch-evaluations/reports/haven-verified-qa/2026-05-28-haven-source-triage-boyle.md`; upstream `PROPOSED-PATCHES.md#L71-L96`; upstream `HAVEN-002` evaluation separates this issue at `#L108-L111` and related details at `#L146-L150`. | Reproduce the `#edit-email` boundary contrast baseline under the Haven scan setup, then choose the token/border fix path. |

## Guardrail

Source status stays separate from local status. `VERIFIED` requires same-condition baseline evidence, after-patch evidence, broad regression classification, and completed required manual checks.
