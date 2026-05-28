# Haven Source Triage - 2026-05-28

## Scope

Read-only source triage for `HAVEN-001`, `HAVEN-002`, and `HAVEN-003`.

## Agent

| Field | Value |
|---|---|
| Agent | Boyle |
| Role | Explorer |
| Run ID | `2026-05-28-haven-source-triage-boyle` |
| Edits made | None |

## Findings

| Item | Source status | Evidence artifacts | Likely packet focus | Manual verification debt | Next action |
|---|---|---|---|---|---|
| `HAVEN-001-logo-link-name` | Upstream says patch verified: `link-name` went to 0 after patch. | Upstream patch and evaluation: before `link-name` serious count 2, after 0 across `/` and `/blog`, light/dark/forced-colors. | QA the existing verified packet for filing readiness: accessible name rationale, decorative logo `alt=""`, same-condition before/after evidence, no overclaiming. | NVDA + Chrome and VoiceOver + Safari still unchecked for logo link announcement. | Create/QA the local packet from the upstream evaluation and explicitly preserve the two manual AT checks as open debt. |
| `HAVEN-002-secondary-button-contrast` | Upstream says patch verified: `.bg-secondary` `color-contrast` went to 0 after CSS rebuild/cache clear. | Upstream patch and evaluation: before ratio about 3.11:1; after secondary button violations 0 across `/` and `/blog`, light/dark/forced-colors. Remaining `#edit-email` is separated as `HAVEN-003`. | Packet should focus on visual-state review and contrast taxonomy: text contrast for secondary buttons, not the input-boundary issue. Include `npm run build` and cache rebuild requirements. | Default/hover/focus/active/disabled visual review, dark-mode visual review, and NVDA + Chrome high-contrast readability are still unchecked. | Run packet QA plus a visual state checklist before treating it as upstream-ready. |
| `HAVEN-003-email-input-boundary-contrast` | Upstream says patch needed. Directory listing shows no `HAVEN-003` patch/evaluation artifact yet. | Evidence is source notes only: `#edit-email`, `--input` token, reported by axe under `color-contrast` but mapped locally to WCAG 1.4.11; ratio noted as about 1.14:1. `HAVEN-002` evaluation also identifies it as separate. | New patch decision packet: reproduce boundary contrast, choose token darkening vs visible border, verify light/dark/forced-colors, and avoid conflating 1.4.3 text contrast with 1.4.11 non-text contrast. | Baseline reproduction is still owed, plus manual/visual verification of input boundary visibility across modes and states. | Reproduce `#edit-email` baseline under the Haven scan setup, then draft the `--input`/border fix approach. |

## Sources Used

- `https://github.com/mgifford/drupal-cms/blob/main/patches/haven-a11y/PROPOSED-PATCHES.md`
- `https://github.com/mgifford/drupal-cms/blob/main/patches/haven-a11y/PATCH-EVALUATION-README.md`
- `https://github.com/mgifford/drupal-cms/blob/main/patches/haven-a11y/a11y-HAVEN-001-logo-link-name-evaluation.md`
- `https://github.com/mgifford/drupal-cms/blob/main/patches/haven-a11y/a11y-HAVEN-002-secondary-button-contrast-evaluation.md`

## Integration Note

This report should update report paths and next actions for Haven rows only. It should not advance any local status to `VERIFIED` because manual checks remain open and local packet QA has not run.
