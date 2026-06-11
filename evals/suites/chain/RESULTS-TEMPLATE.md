# Chain Eval Results — /a11y-workflow

> **Template**: Copy and fill in for each run. Store completed records in `evals/suites/chain/pilot/` (pilot) or a dated `results/` subdirectory.  
> **S1–S2**: Human-scored from session record.  
> **S3–S5**: Run `python3 evals/suites/chain/score_chain.py <fixture-id> <session-dir>` after saving stage outputs.  
> **Stage output files**: Save each stage's full text as `critic.txt`, `audit.txt`, `escalated.txt` (see score_chain.py header).

---

## Run Metadata

| Field | Value |
|---|---|
| Date | YYYY-MM-DD |
| Run type | pilot / full |
| Model tiers | Scout: haiku / Planner: opus / Critic: opus / Audit: opus |
| Session link | (Claude Code session ID or transcript path) |
| Scorer | (name or handle) |
| Notes | |

---

## Per-Fixture Scores

| # | Fixture | S1 Scout (0–2) | S2 Handoff (0–2) | S3 Critic (0–1) | S4 Escalation (0/1) | S5 Audit (0–2 or N/A) | Tracer (1/0/N/A) | PASS | Wall clock | Notes |
|---|---------|---------------|-----------------|-----------------|--------------------|-----------------------|-----------------|------|-----------|-------|
| 1 | modal-broken-focus-trap | | | | | | | | | |
| 2 | product-carousel-autoplay | | | | | | | | | |
| 3 | video-tutorial-no-captions | | | | | | | | | |
| 4 | login-form-clean | | | | | N/A | N/A | | | |
| 5 | article-page-clean | | | | | N/A | N/A | | | |
| 6 | tabbed-nav-vs-tab-pattern | | | | | N/A | | | | |
| 7 | app-focus-order-illogical | | | | | N/A | | | | |
| 8 | toast-notification-no-role | | | | | N/A | | | | |

---

## S1 Scoring Guidance (human)

For each fixture, check the scout output saved in the session record:
- **S1a** (1 pt): Output ≤ 1500 chars. Count characters; record Yes/No.
- **S1b** (1 pt): Component type matches rubric `component_type`. Accept close synonyms.

## S2 Scoring Guidance (human)

Check the planner output (plan file path and contents):
- **S2a** (1 pt): Plan file exists at `docs/a11y-plans/YYYY-MM-DD-<feature>-a11y-plan.md`.
- **S2b** (1 pt): Plan file contains 8+ phase headings or numbered sections 1–9.

---

## Aggregate Scores

| Metric | Formula | This Run | Watch Threshold |
|--------|---------|----------|----------------|
| **S4 Escalation accuracy** | n correct / 8 | | ≥ 7/8 |
| S1 mean | sum S1 / 8 | | ≥ 1.5 |
| S2 mean | sum S2 / 8 | | ≥ 1.5 |
| S3 mean | sum S3 / 8 | | ≥ 0.7 |
| S5 mean (audit fixtures) | sum S5 / n_audit | | ≥ 1.5 |
| Tracer survival | n survived / n defined | | ≥ 5/6 |
| **Fixture PASS rate** | n PASS / 8 | | 8/8 target |

---

## PASS Rule Reminder

A fixture PASSES if ALL of:
1. S4 = 1
2. No stage scored 0
3. Tracer survives (where defined)

---

## Findings / Regression Notes

_Document any stage failures, surprising calibration results, or tracer drops here._

---

## Model Tier Details

| Stage | Model | Version | Notes |
|-------|-------|---------|-------|
| Scout | haiku | | |
| Planner | opus | | |
| Critic | opus | | |
| Audit | opus | (only for escalated fixtures) | |

---

## Session Record Index

| Fixture | Session dir | escalated.txt | Notes |
|---------|------------|--------------|-------|
| modal-broken-focus-trap | | | |
| product-carousel-autoplay | | | |
| video-tutorial-no-captions | | | |
| login-form-clean | | | |
| article-page-clean | | | |
| tabbed-nav-vs-tab-pattern | | | |
| app-focus-order-illogical | | | |
| toast-notification-no-role | | | |
