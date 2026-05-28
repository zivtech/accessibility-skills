# Generated Evaluator Report Errata

> Date: 2026-05-28
> Scope: Local copied evaluator reports under `docs/drupal-patch-evaluations/reports/evaluator-runs/`

## Erratum

Some generated evaluator reports with `FAIL` status also include:

```text
Eligible For Patch Recommendation: yes
```

In the local ledger, this must not be read as "the current patch is ready to recommend." For failed runs, read it as "the baseline was reproduced and the issue remains eligible for remediation work." The local packet and `STATUS.md` row are the controlling verdict.

Affected copied reports:

- `a11y-DRUPAL-A11Y-003-select-all-checkbox-label-evaluation-codex-runtime-smoke-003.md`
- `a11y-DRUPAL-A11Y-004-tabindex-buttons-test-form-evaluation-codex-runtime-smoke-004.md`
- `a11y-DRUPAL-A11Y-006-theme-switcher-landmark-evaluation-codex-runtime-smoke-006.md`
- `a11y-DRUPAL-A11Y-007-messages-landmark-role-evaluation-codex-runtime-smoke-007.md`

## Reason Raw Reports Were Not Edited

The generated reports are preserved as run artifacts. This errata file records the interpretation fix without mutating raw evaluator output.
