# Plan: Evaluate All Mike Gifford Drupal Accessibility Items

> Status: Draft execution plan
> Date: 2026-05-28
> Scope: Evaluate the current accessibility patch/investigation items surfaced in Mike Gifford's `drupal-core` and `drupal-cms` Haven patch artifacts.

## Goal

Turn every current item into one canonical local status with a durable evidence trail. The main outcome families are:

- `VERIFIED`: baseline reproduced, patch applies, same-condition after-scan passes, broad regression scan has no patch-owned regressions, and required manual checks are complete.
- `PATCH HYGIENE BLOCKED` or `TEST STATE BLOCKED`: patch drift, target file drift, or test-state setup prevents verification, with exact next repair step.
- `NEEDS PATCH`: baseline reproduced and issue is real, but no current patch is ready or the proposed design does not match the accessibility need.
- `INCONCLUSIVE`, `FAILED`, or `OBSOLETE`: evidence shows the item cannot yet be decided, does not fix the target issue, or no longer applies to the tested source.

Every item should leave behind a packet under `docs/drupal-patch-evaluations/` using `templates/drupal-a11y-patch-evaluation-template.md`.

## Source Inventory

Sources checked on 2026-05-28:

- Drupal core proposed patches: https://github.com/mgifford/drupal-core/blob/main/patches/PROPOSED-PATCHES.md
- Drupal core patch summary: https://github.com/mgifford/drupal-core/blob/main/reports/PATCH-EVALUATION-SUMMARY.json
- Drupal core pattern report: https://github.com/mgifford/drupal-core/blob/main/reports/PATTERN-REPORT-latest.md
- Haven proposed patches: https://github.com/mgifford/drupal-cms/blob/main/patches/haven-a11y/PROPOSED-PATCHES.md
- First trial packet: `docs/drupal-patch-evaluations/2026-05-28-a11y-DRUPAL-A11Y-007-messages-landmark-role.md`

The Drupal core summary is from 2026-05-07 and may be stale. Current raw patches must be rechecked before trusting old patch-hygiene failures.

## Evaluation Rules

1. No item is verified unless the target baseline violation is observed before patching.
2. Use the same URL, theme, viewport, color mode, direction, content state, auth state, and interaction state before and after patching.
3. Patch labels like "ready" in `PROPOSED-PATCHES.md` are treated as claims to test, not as evidence.
4. Automated results must be separated from manual AT checks. Manual checks may remain open, but they must not be implied complete.
5. WCAG mapping must be calibrated before filing. Do not copy inconsistent levels such as `1.3.6 Level A` when the criterion is actually AAA.
6. AI can assist triage and packet assembly, but every finding must be backed by measured evidence or explicitly marked as design review.

## Status Vocabulary

Use one canonical status enum across the plan, ledger, packets, and subagent reports:

- `NOT STARTED`
- `DRAFT`
- `BASELINE VERIFIED`
- `PATCH HYGIENE BLOCKED`
- `TEST STATE BLOCKED`
- `INCONCLUSIVE`
- `NEEDS PATCH`
- `FAILED`
- `VERIFIED`
- `OBSOLETE`

`NEEDS PATCH` is a local evaluation outcome, not a source claim. Do not use it unless a packet has reproduced the local baseline and shows that no usable patch is available yet. Keep unreproduced upstream/source claims in `Source status` plus `DRAFT`, `TEST STATE BLOCKED`, or `INCONCLUSIVE`.

## Parallel Subagent Operating Model

Use subagents aggressively for independent work, but keep one main agent as the integration lead. Parallelism should increase coverage, not create competing sources of truth.

### Main Agent Responsibilities

The main agent owns:

- `docs/drupal-patch-evaluations/STATUS.md`
- final packet readiness verdicts
- environment preflight and runtime locks
- upstream filing decisions
- any edit that changes shared evaluator strategy
- resolving conflicts between subagent findings

The main agent should keep the current blocking item local when the next action depends on it. Subagents should take sidecar work that can proceed without blocking the current focus.

### Subagent Roles

| Role | Owns | May change | Must not decide |
|---|---|---|---|
| Source/provenance researcher | Upstream source URLs, patch SHA, target SHA, stale-summary notes | Assigned packet source section or saved report | Verification status |
| Patch hygiene owner | `git apply --check`, target drift, corrupt/missing classification | Assigned packet hygiene section | Accessibility correctness |
| Baseline state owner | Route/content/theme/auth/viewport/interaction setup | Assigned packet baseline section | Patch readiness |
| Evaluation runner | Same-condition before/after scans and broad regression scan | Assigned packet evidence sections | Final `VERIFIED` |
| Packet drafter | Template completion from measured evidence | One assigned packet path | Inventing missing evidence |
| `a11y-critic` reviewer | Evidence gaps, WCAG calibration, overclaiming, manual debt | Saved review report | Primary evaluation |
| `perspective-audit` reviewer | Voice control, landmarks, status messages, forced colors, cognitive-risk escalations | Saved review report | Routine packet QA |
| Filing-package drafter | Drupal.org-ready title, reproduction steps, evidence block | Filing block in assigned packet | Actual upstream filing |

### Subagent Ownership Rules

- Assign exactly one item owner per row in the ledger.
- Give each subagent a disjoint packet path or a read-only research task.
- Do not let multiple subagents edit `STATUS.md`; they report status back and the main agent updates the ledger.
- Do not let subagents mark an item `VERIFIED`; they can recommend a canonical status, but the main agent performs the final evidence check.
- For code/patch work, assign disjoint patch files or target modules to avoid overlapping diffs.
- Every subagent final report must include: item ID, files inspected/changed, evidence gathered, blocker, and one next action.
- Every subagent write task must name allowed files, forbidden files, packet path, report path, checkout/worktree path, DDEV project name, and environment lock.
- No subagent may patch or reroll in a shared checkout without a main-agent-granted environment lock.

### Parallelism Caps

Run as many subagents as the environment can safely support. Default to 4-6 concurrent agents only for independent, read-only or disjoint packet work.

| Work type | Default parallelism | Hard rule |
|---|---:|---|
| Read-only source/provenance research | 6-8 | Safe when no checkout or packet mutation occurs. |
| Patch hygiene checks | 3-4 | Parallel only with isolated worktrees/checkouts, otherwise 1. |
| Baseline reproduction on DDEV | 2-3 | Parallel only with isolated DB/content state or reset snapshots. |
| Patch apply/build/cache before-after evaluation | 1 per checkout | Parallel only with separate DDEV project names, ports, DBs, and worktrees. |
| Packet drafting | 4-6 | One packet path per agent. |
| `a11y-critic` packet review | 3-5 | Read-only, non-overlapping packet sets. |
| `perspective-audit` | 1-2 | Use only for flagged categories. |
| Upstream filing | 1 | Main agent only. |

### Wave Assignment Model

`docs/drupal-patch-evaluations/STATUS.md` is the canonical scheduler. Its `Wave`, `Owner`, `Run ID`, `Claimed at`, `Report path`, `Environment lock`, `Checkout/worktree`, `DDEV project`, and `Allowed files/scope` columns decide what can run in parallel. The summary below explains the intended waves; update the ledger first when reality changes.

| Wave | Subagents | Ownership |
|---|---:|---|
| Haven verified QA | 2 | One agent each for `HAVEN-001`, `HAVEN-002`. |
| New patch decisions | 3 | One agent each for `HAVEN-003`, `DRUPAL-A11Y-010`, `DRUPAL-A11Y-011`. |
| Core patch hygiene | 6 | One agent each for `LABEL-IN-NAME-004`, `DRUPAL-A11Y-002`, `DRUPAL-A11Y-005`, `DRUPAL-A11Y-006`, `DRUPAL-A11Y-008`, `DRUPAL-A11Y-009`, subject to isolated worktrees. |
| Core baseline repair | 3 | One agent each for `DRUPAL-A11Y-001`, `DRUPAL-A11Y-003`, `DRUPAL-A11Y-004`, subject to DDEV state isolation. |
| Critic gate | 2-3 | `a11y-critic` agents review completed packet groups by non-overlapping item sets. |

### Saved Report Convention

Subagent reports must be saved before the ledger status changes:

```text
docs/drupal-patch-evaluations/reports/{wave}/{item}-{run-id}.md
```

The main agent updates `STATUS.md` only from saved reports, not from transient chat summaries.

### Subagent Prompt Template

```text
Workspace: /path/to/evaluation/checkout.
Item: ITEM-ID.
Ownership: You own only ITEM-ID, packet path PACKET-PATH, and report path REPORT-PATH. Do not edit STATUS.md.
Environment lock: LOCK-ID or read-only/no-lock.
Task:
1. Recheck current source and patch evidence.
2. Run or specify the exact baseline setup needed.
3. Fill or update your packet section with evidence.
4. Return a readiness recommendation using the canonical local status enum: VERIFIED, INCONCLUSIVE, FAILED, TEST STATE BLOCKED, PATCH HYGIENE BLOCKED, NEEDS PATCH, or OBSOLETE.
5. Report one concrete next action.
Rules:
- Do not claim verification without before/after evidence under identical conditions.
- Do not revert or overwrite unrelated edits.
- If the live Drupal/DDEV environment is unavailable, mark the item blocked and preserve the exact command needed next.
- Save your report to REPORT-PATH with commands, cwd, exit codes, source SHAs, evidence paths, blocker, and next action.
```

### Convergence Gate

After each wave:

1. Main agent reviews subagent reports.
2. Main agent updates `STATUS.md`.
3. Run `git diff --check`.
4. Run `a11y-critic` over any packet proposed as ready.
5. Only then proceed to upstream filing or the next wave.

## Workstreams

### Phase 0: Workspace Setup

Prepare a local Drupal core evaluation checkout with DDEV. The evaluator must run in the same checkout it mutates with `git apply`; do not apply patches in one clone while testing a different DDEV checkout.

```bash
git clone https://github.com/mgifford/drupal-core.git /path/to/mgifford-drupal-core
cd /path/to/mgifford-drupal-core
ddev config --auto --project-name=drupal-core --project-type=drupal12 --docroot=. --php-version=8.5 --database=mariadb:10.11 --nodejs-version=24 --corepack-enable --composer-version=2
ddev start
ddev drush status
ddev drush site:install standard --account-name=admin --account-pass=admin --site-name='Drupal A11y Eval' -y
ddev drush en theming_tools imagefile button message table dialog tab lang_hebrew actionlink pager themeswitcher -y
ddev drush cset system.theme default olivero -y
ddev drush cset system.theme admin claro -y
ddev drush cache-rebuild
```

Current local caveats:

- Mike's evaluator currently hardcodes `http://drupal-core.ddev.site`; on machines where DDEV uses alternate router ports, add `DRUPAL_BASE_URL` support and run with `DRUPAL_BASE_URL=http://drupal-core.ddev.site:33000`.
- `core/tests/playwright/scripts/evaluate-patch.js` imports `core/tests/playwright/scripts/lib/canonical-patch-map.js`; if that helper is missing, restore it or guard the import before running evaluations.
- In the inspected checkout, running Composer inside Mike's repo mutated tracked `core/` files. Use a disposable runtime clone and keep the source/provenance clone read-only.

Prepare the Haven/Drupal CMS checkout separately if evaluating Haven patches:

```bash
git clone https://github.com/mgifford/drupal-cms.git /path/to/mgifford-drupal-cms
```

Record:

- repo commit SHA
- patch file SHA
- target file SHA
- tool versions: Node, Playwright, axe-core, DDEV, Drupal

### Phase 0b: Environment Preflight

Run this before launching item-owning subagents:

```bash
ddev status
ddev drush status
yarn --version
node --version
npx playwright --version
```

If preflight fails, subagents may do read-only source/provenance work only. Do not mark individual items `TEST STATE BLOCKED` for a global DDEV outage; record the global blocker in `STATUS.md` and keep item statuses unchanged until a per-item test is attempted.

### Phase 1: Patch Hygiene Sweep

For every patch file:

```bash
git apply --check patches/{patch-name}.patch
```

Classify:

- `APPLIES`: continue to baseline repair.
- `PATCH_DOES_NOT_APPLY`: inspect target file drift and rebuild patch against current `main`.
- `PATCH_FILE_CORRUPT`: regenerate a clean unified diff from a clean working tree.
- `TARGET_FILE_MISSING`: locate the current equivalent file, then decide whether to reroll or close as obsolete.

Output: one short hygiene section in each packet, even when no scan has run yet.

### Phase 2: Baseline State Repair

For every item with `baseline-not-reproduced`, repair the test state before touching the patch.

Common repairs:

- Use concrete selectors from the pattern report, not only broad selectors.
- Create required sample content first.
- Trigger status/error messages immediately before scanning.
- Ensure admin pages have rows/items to expose bulk checkboxes, summaries, headings, and language switcher links.
- Open dialogs, expand details, or type into autocomplete fields when the failing element is interaction-dependent.
- Run light, dark, forced-colors, and mobile only when the issue can vary across those conditions.

Baseline acceptance requires:

- failing selector captured as HTML or accessibility snapshot
- axe rule observed with pattern/instance IDs when available
- route/content/state setup saved in the packet

### Phase 3: Before/After Evaluation

Use Mike's evaluator when available:

```bash
yarn a11y:evaluate-patch {patch-name}
```

If the evaluator route is wrong, patch evaluator config first rather than hand-waving the issue.

After patching:

- clear Drupal cache
- rerun same targeted scan
- run broad regression scan
- revert patch
- save all packet evidence

### Phase 4: Design Critique

Run `a11y-critic` on every packet before calling it ready.

Critic checks:

- baseline and after-state proof are both present
- WCAG mapping and severity are calibrated
- proposed code matches the accessibility problem, not just the axe rule
- adjacent issues are not claimed as fixed
- manual AT debt is explicit

Escalate to `perspective-audit` for:

- label-in-name / voice control
- landmark navigation
- status/error message announcements
- forced colors, contrast, focus indication
- cognitive recovery from form errors

### Phase 5: Manual Verification

Minimum manual checks by category:

- Contrast/color: visual review in light, dark, forced-colors, and focus/hover/disabled states.
- Labels/name/role: accessible name inspection plus voice-control label-in-name contract when visible text differs from accessible name.
- Landmarks/messages: NVDA + Chrome and VoiceOver + Safari smoke checks for landmark lists and message announcement.
- Keyboard/tabindex: real keyboard traversal with Playwright plus at least one human keyboard pass.
- Tables/headings: screen reader heading/table navigation smoke where the issue affects structure.

### Phase 6: Filing Package

Only file or update upstream once a packet is `VERIFIED` or clearly marked as a blocked reroll request.

Each issue package should include:

- concise title
- environment
- exact reproduction steps
- before evidence
- patch
- after evidence
- broad regression result
- manual check status
- AI assistance disclosure

## Drupal Core Philosophy Gate

The `talk-to-drupal` review pass on 2026-05-28 returned `REVISE`. Its structural complaint is partly a tool-fit issue because this plan is not an ADR, but the selected lenses are useful Drupal-core guardrails:

- `site-builder-experience`: each patch packet should explain how the change affects accessible administration, theming, content authoring, or site-building workflows.
- `project-stewardship`: each upstream-ready packet should be small, evidence-backed, and maintainer-actionable rather than widening into speculative product direction.
- `content-modeling`: field/widget/table-header and entity-form items must name the field or entity API surface they affect and call out schema, storage, translation, revision, and workspace risks when relevant.
- Counter-lenses to check before filing: core boundary pragmatism, release-gate conservatism, and backward compatibility.

Saved review output:

- `/Users/AlexUA_1/Codex/drupal-core-reviews/2026-05-28-drupal-a11y-evaluation-plan.md`
- `/Users/AlexUA_1/Codex/drupal-core-reviews/2026-05-28-drupal-a11y-evaluation-plan-grounding.json`

## Item Matrix

| Item | Source status | Current summary root cause | First gate | Packet focus |
|---|---|---|---|---|
| `LABEL-IN-NAME-004-filter-format-aria-label` | Core patch ready | local evaluator PASS after rule alias, required-rule scan, and selector-hint support | Optional voice-control smoke check before upstream filing | Voice-control contract and WCAG 2.5.3 |
| `DRUPAL-A11Y-002-submit-button-contrast` | Core patch ready | `patch-does-not-apply` | Reroll contrast patch against current button CSS/token system | Contrast ratios for all button states |
| `DRUPAL-A11Y-005-language-switcher-contrast` | Core patch ready | `patch-does-not-apply` | Reroll against current language link CSS | Contrast across admin/Claro, language links, forced colors |
| `DRUPAL-A11Y-001-file-widget-display-labels` | Core patch ready | `baseline-not-reproduced` | Recreate `/contact/imagefile_file` fixture and observe unlabeled display checkboxes | Missing accessible names on file display controls |
| `DRUPAL-A11Y-003-select-all-checkbox-label` | Core patch ready | `baseline-not-reproduced` | Ensure `/admin/content`, `/admin/people`, or table test pages have rows | Bulk select checkbox name and voice-control impact |
| `DRUPAL-A11Y-006-theme-switcher-landmark` | Core patch ready | `patch-file-corrupt` | Recreate clean patch and reproduce theme switcher region issue | Landmark design; avoid landmark noise |
| `DRUPAL-A11Y-007-messages-landmark-role` | Core patch ready | original patch was partial; local `status`/`alert` reroll now passes evaluator | Run NVDA or VoiceOver smoke check and prepare upstream reroll | `contentinfo` misuse, `status`/`alert` vs `region` design |
| `DRUPAL-A11Y-004-tabindex-buttons-test-form` | Core patch ready | `baseline-not-reproduced` | Reproduce `/buttons` positive tabindex elements | Real keyboard order and focus behavior |
| `DRUPAL-A11Y-008-empty-table-headers` | Core patch ready | `patch-target-file-missing` | Locate current field/widget table header source | Table header semantics and current file ownership |
| `DRUPAL-A11Y-009-module-summary-names` | Core patch ready | `patch-file-corrupt` | Recreate patch and reproduce `/admin/modules` summary-name failures | Details/summary accessible names |
| `DRUPAL-A11Y-010-heading-order` | Core investigation | baseline spans pager, datetime, multiple-value field, and admin-block heading paths | Split by route family before writing a patch | Decide whether patch is needed or fixture-only issue |
| `DRUPAL-A11Y-011-empty-heading-elements` | Core investigation | obsolete ID/name mapping | Keep as obsolete and avoid using `011` for empty-heading | Replacement tracked as `DRUPAL-A11Y-012` |
| `DRUPAL-A11Y-012-empty-heading-elements` | Core investigation | baseline splits into filter-tip empty `h3` and empty home-page `h1` paths | Patch/test filter-tip shape mismatch first, then classify home-page title path | Separate test/demo noise from actionable core issue |
| `HAVEN-001-logo-link-name` | Haven verified | local packet draft, manual AT debt open | Run current patch hygiene and carry manual AT checks | Ready-to-file packet quality |
| `HAVEN-002-secondary-button-contrast` | Haven verified | local packet draft, visual-state debt open | Run visual-state QA and build/cache reproduction | Confirm no design regressions in light/dark/forced-colors |
| `HAVEN-003-email-input-boundary-contrast` | Haven patch needed | local packet draft, baseline not reproduced | Reproduce input boundary contrast and design token fix | Correctly map to WCAG 1.4.11 non-text contrast |

## Recommended Execution Order

`docs/drupal-patch-evaluations/STATUS.md` is the canonical scheduler and ownership ledger. The batches below are narrative execution notes for the wave model in the ledger and the parallel operating model above. Current-focus work may run before a wave when the next action is already known.

### Current Focus

1. `DRUPAL-A11Y-007-messages-landmark-role` because the reroll now has automated PASS evidence and needs only a short AT smoke before upstream prep.
2. `DRUPAL-A11Y-012-empty-heading-elements` because the likely first patch is fixture/local-render-path sized.
3. `DRUPAL-A11Y-010-heading-order` after splitting route families so pager, datetime, field, and admin-block fixes do not collapse into one overbroad patch.

Goal: turn the two verified candidates into shareable upstream evidence and start the next smallest patchable investigation without losing the route-family distinctions.

### Batch A: Haven Quick Wins and Packet QA

1. `HAVEN-001-logo-link-name`
2. `HAVEN-002-secondary-button-contrast`

Goal: produce two local draft/QA Haven packets, promoting them only after local patch hygiene, visual/manual checks, and build/cache evidence pass.

### Batch B: Patch Hygiene Recovery

1. `DRUPAL-A11Y-002-submit-button-contrast`
2. `DRUPAL-A11Y-005-language-switcher-contrast`
3. `LABEL-IN-NAME-004-filter-format-aria-label` (automated PASS; only optional voice-control smoke remains)
4. `DRUPAL-A11Y-006-theme-switcher-landmark`
5. `DRUPAL-A11Y-008-empty-table-headers`
6. `DRUPAL-A11Y-009-module-summary-names`

Goal: convert stale/corrupt/non-applying patches into clean current diffs or mark obsolete.

### Batch C: Baseline State Repair

1. `DRUPAL-A11Y-001-file-widget-display-labels`
2. `DRUPAL-A11Y-003-select-all-checkbox-label`
3. `DRUPAL-A11Y-004-tabindex-buttons-test-form`

Goal: fix evaluator state so original findings are observed before patching.

### Batch D: New Patch Decisions

1. `HAVEN-003-email-input-boundary-contrast`
2. `DRUPAL-A11Y-012-empty-heading-elements`
3. `DRUPAL-A11Y-010-heading-order`

Goal: decide whether to write patches, close as test/demo-only, or keep as investigation. Start with `012` because the first likely fix is narrower than `010`'s route-family spread.

## Status Ledger

Maintain a simple ledger while executing:

| Field | Meaning |
|---|---|
| Item | Patch/investigation ID |
| Upstream repo | `drupal-core` or `drupal-cms` |
| Source status | Upstream/source claim, such as `Core patch ready`, `Core investigation`, `Haven verified`, or `Haven patch needed` |
| Local status | Canonical local enum: `NOT STARTED`, `DRAFT`, `BASELINE VERIFIED`, `PATCH HYGIENE BLOCKED`, `TEST STATE BLOCKED`, `INCONCLUSIVE`, `NEEDS PATCH`, `FAILED`, `VERIFIED`, `OBSOLETE` |
| Owner / run ID / claimed at | Parallel-work claim fields |
| Environment lock | Shared checkout/DDEV lock ID or `read-only/no-lock` |
| Checkout/worktree | Filesystem path used for the evidence run |
| DDEV project | DDEV project name or `n/a` |
| Allowed files/scope | Files or packet sections the owner may change |
| Packet path | Local packet artifact |
| Report path | Saved subagent or main-agent report artifact |
| Integrated by/at | Who merged the evidence into the ledger and when |
| Upstream issue | Drupal.org URL when filed/updated |
| Next action | One concrete command or decision |

Living ledger: `docs/drupal-patch-evaluations/STATUS.md`.

Source-link note: `blob/main` links in the source inventory are orientation links. Before any packet is filed upstream, replace or supplement them with immutable permalinks plus source commit, patch-file SHA, target-file SHA, and tool versions.

## Completion Criteria

This evaluation program is complete when:

- Every row in the item matrix has a packet.
- Every packet has a readiness verdict.
- Every ready packet has a filing block.
- Every blocked packet has one concrete repair action.
- No packet claims automated or manual verification that did not actually run.
- Every subagent-owned row has an owner, run ID, report path, and integration timestamp.
- The status ledger has no `NOT STARTED` rows.

## Critic Review of This Plan

Verdict: `EXECUTABLE WITH ONE ENVIRONMENT BLOCKER`

Findings:

1. P1 - The plan depends on a real local DDEV Drupal checkout. Without it, the work can only produce packet triage from upstream artifacts, not verified before/after results.
2. P1 - Several source claims conflict: `PROPOSED-PATCHES.md` says patches are ready, while the patch summary says all 10 core evaluations are inconclusive. The plan correctly treats the summary as evidence and the proposed-patches file as claims to test.
3. P2 - WCAG 1.3.6 mapping must be corrected before filing landmark issues. This should be a specific QA check in each affected packet.
4. P2 - Haven items should not be skipped just because they are marked verified; they still need packet QA, manual debt review, and upstream filing readiness.
