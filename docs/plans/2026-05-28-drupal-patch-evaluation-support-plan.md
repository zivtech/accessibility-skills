# Drupal Accessibility Patch Evaluation Support Plan

> Status: Draft support plan
> Date: 2026-05-28
> Scope: How `a11y-meta-skills` can help Mike Gifford's Drupal patch-evaluation workflow without replacing his evidence-first process.

## Source Observations

- Mike's Haven workflow uses a patch plus evaluation packet model: each patch has a unified diff, a reproduction/evaluation report, status, axe rule, WCAG mapping, root cause, before/after evidence, and follow-up manual AT checks.
- The Haven README states the important trust boundary: every patch is driven by a confirmed automated finding, not by AI code inspection alone.
- The Drupal core reports directory is broader: axe pattern reports, keyboard review, label-in-name contract evidence, module impact summaries, patch cross-reference indexes, and patch evaluation summaries.
- The current Drupal core patch evaluation summary shows a useful triage signal: 10 patches evaluated, 0 passed, 10 inconclusive, with root causes split across patch hygiene and unreproduced baseline state.

Primary sources:

- Haven patch evaluation README: https://github.com/mgifford/drupal-cms/blob/main/patches/haven-a11y/PATCH-EVALUATION-README.md
- Haven proposed patches index: https://github.com/mgifford/drupal-cms/blob/main/patches/haven-a11y/PROPOSED-PATCHES.md
- Drupal core reports directory: https://github.com/mgifford/drupal-core/tree/main/reports
- Drupal core patch evaluation summary: https://github.com/mgifford/drupal-core/blob/main/reports/PATCH-EVALUATION-SUMMARY.md
- Drupal core patch cross-reference: https://github.com/mgifford/drupal-core/blob/main/reports/patches/INDEX.md
- Drupal core keyboard review: https://github.com/mgifford/drupal-core/blob/main/reports/KEYBOARD-REVIEW-latest.md

## What Mike Already Has

The workflow is strongest where it is empirical:

- Baseline first: prove the violation exists on an unpatched site.
- Same-command verification: run the same targeted scan after applying the patch.
- Broad regression scan: verify the fix did not introduce new violations.
- Patch hygiene: `git apply --check`, build steps, cache rebuild, and revert path.
- Issue-ready narrative: root cause, file changed, selector, WCAG mapping, axe rule, and reproduction command.
- Explicit remaining debt: manual AT checks are listed separately from automated verification.

This is exactly the line we should preserve. Our help should improve evidence quality, triage, reproducibility, and issue packaging, not generate speculative patches from static code reading.

## Where We Can Help

### 1. Evidence Packet QA

Run `a11y-critic` on each patch evaluation packet before filing or sharing it.

The critic should check:

- PASS claims include a reproduced baseline and a clean after-state.
- Remaining violations are explicitly classified as same issue, adjacent issue, or unrelated issue.
- WCAG mapping matches the actual failure mode. For example, text contrast and non-text boundary contrast should not be collapsed.
- The selector, route, theme, color mode, viewport, directionality, auth state, and build/cache steps are present.
- Manual AT checks are not implied complete unless they were actually run.

Output: a canonical local status recommendation: `VERIFIED`, `INCONCLUSIVE`, `FAILED`, `PATCH HYGIENE BLOCKED`, `TEST STATE BLOCKED`, `NEEDS PATCH`, or `OBSOLETE`.

### 2. Inconclusive Triage

Use the Drupal core summary root causes as work queues:

| Queue | Meaning | Useful next move |
|---|---|---|
| `patch-file-corrupt` | The diff cannot be evaluated reliably | Recreate the patch from a clean branch, then rerun `git apply --check` before scanning. |
| `patch-does-not-apply` | Target code drifted or paths are wrong | Rebase/remap the diff against current core and record the target commit. |
| `patch-target-file-missing` | The proposed file path no longer exists in the tested checkout | Locate the modern equivalent file before re-running evidence. |
| `baseline-not-reproduced` | The scan did not observe the original violation | Fix test state first: route, theme, module, auth, sample content, viewport, color mode, or interaction setup. |

This is a good fit for `a11y-test` plus `a11y-critic`: test measures the environment; critic refuses to call a patch verified if the baseline never appeared.

Also normalize rule IDs before treating "baseline not observed" as a site-state failure. In local testing, `LABEL-IN-NAME-004` used `label-in-name` while axe-core 4.11.4 reports the relevant check as `label-content-name-mismatch`; the baseline existed manually but the evaluator missed it. The local runtime now proves the fix needs three pieces together: rule aliasing, explicit `runOnly` scans for required non-default axe rules, and selector-hint matching from Playwright selectors to concrete axe selectors.

### 3. Manual Verification Scripts

Turn each packet's unfinished manual AT check into a small script or checklist.

Candidate format:

- Keyboard-only steps using Playwright real key presses.
- Voice-control/label-in-name checks using visible label versus accessible name contracts.
- Screen reader smoke scripts written as human steps, with the tested browser and AT named.
- Forced-colors and dark-mode checks included when the issue is color, contrast, focus, or visual affordance.

This does not replace NVDA/VoiceOver judgment, but it makes the manual queue precise.

### 4. Drupal-Specific Fixtures for This Repo

Add benchmark fixtures that mirror Mike's evidence problems:

- `drupal-patch-baseline-not-reproduced`: packet claims a patch is inconclusive because the target violation disappeared; critic must refuse a PASS and prescribe test-state triage.
- `drupal-patch-adjacent-contrast-rule`: packet fixes text contrast but leaves a non-text contrast boundary issue; critic must keep the issue taxonomy separate.
- `drupal-patch-label-in-name-contract`: visible label and accessible name differ; critic must map the voice-control impact to WCAG 2.5.3.
- `drupal-patch-contentinfo-role`: status messages misuse `contentinfo`; critic must map the landmark problem and recommend `status` or `alert` depending on message type.

This would make the skills better at exactly the kind of Drupal accessibility review Mike is doing.

### 5. Filing Support

Prepare drupal.org issue-ready packets from verified evaluations:

- Short title with rule, component, and WCAG criterion.
- Environment block.
- Steps to reproduce.
- Before evidence.
- Patch attached or linked.
- After evidence.
- Remaining limitations and manual verification status.
- AI assistance disclosure.

The template in `templates/drupal-a11y-patch-evaluation-template.md` is designed for this.

## Suggested First Contribution

Start with one packet and one inconclusive core item rather than the whole report set:

1. Use the Haven format as the positive example.
2. Pick one Drupal core inconclusive patch from the hygiene queue, preferably `patch-does-not-apply` or `patch-file-corrupt`, because that can be fixed without debating accessibility semantics.
3. Run the support template against it.
4. Use `a11y-critic` for submission-readiness review.
5. Only after it passes packet QA, help file or update the upstream issue.

The best immediate value is not "AI finds more bugs." It is "AI helps keep accessibility patch evidence disciplined enough that maintainers can trust and act on it."

First trial packet:

- `docs/drupal-patch-evaluations/2026-05-28-a11y-DRUPAL-A11Y-007-messages-landmark-role.md`
- `docs/drupal-patch-evaluations/reports/current-wave/2026-05-28-evaluator-support-reroll-and-next-items.md`

Full evaluation program:

- `docs/plans/2026-05-28-drupal-all-items-evaluation-plan.md`
- `docs/plans/2026-05-28-drupal-all-items-evaluation-plan.md#parallel-subagent-operating-model`
- `docs/drupal-patch-evaluations/STATUS.md`

The full program uses the parallel wave model in the evaluation plan, with `STATUS.md` as the canonical scheduler and todo ledger. The first trial packet remains local-only until the blocked test state is repaired and the official evaluator can produce before/after evidence.

## Critic Checkpoints

Before upstreaming:

- `a11y-planner`: Use for new patch work where the accessible implementation approach is not settled.
- `a11y-test`: Run targeted axe, keyboard, color-mode, forced-colors, and interaction-state checks.
- `a11y-critic`: Review the final packet for evidence gaps and severity/WCAG calibration.
- `perspective-audit`: Escalate only when a patch affects a perspective-sensitive workflow, such as voice control, screen reader navigation, magnification/reflow, forced colors, vestibular motion, or cognitive recovery from errors.
