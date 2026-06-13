# Chain Eval Results — /a11y-workflow (PILOT)

> Filled from the 3-fixture pilot, 2026-06-13. S1–S2 human-scored; S3–S5 from
> `score_chain.py` AND re-scored by hand (the automated scores have known defects —
> see PILOT-REPORT.md instrument findings I2–I5). **Manual scores are authoritative.**

---

## Run Metadata

| Field | Value |
|---|---|
| Date | 2026-06-13 |
| Run type | pilot (3 of 8 fixtures) |
| Model tiers | Scout: haiku / Planner: opus / Critic: opus / Audit: opus (Claude Code subagents, production mechanism) |
| Mechanism | Hand-orchestrated /a11y-workflow Mode 1 steps 1–4, depth-1 subagents from main session |
| Subagent calls | 12 total: 3 Haiku scouts + 9 Opus (3 planner, 3 critic, 3 audit — all 3 escalated) |
| Scorer | score_chain.py (automated) + manual re-score (Claude, operator-supervised) |
| Notes | Pilot set = PROTOCOL set (modal, video, login), per operator choice 2026-06-13 |

---

## Per-Fixture Scores (MANUAL — authoritative)

| # | Fixture | S1 (0–2) | S2 (0–2) | S3 (0–1) | S4 (0/1) | S5 (0–2) | Audit Verdict | Tracer | PASS | Wall clock | Notes |
|---|---------|----------|----------|----------|----------|----------|---------------|--------|------|-----------|-------|
| 1 | modal-broken-focus-trap | 1 (S1a=0,S1b=1) | 2 | ~0.6 | 1 | 2 | BLOCK (HAS-BUGS, correct) | 1 | **PASS** | ~10.4 min | Critic used 6-lens taxonomy; audit clean, tracer survived |
| 3 | video-tutorial-no-captions | 1 (S1a=0,S1b=1) | 2 | ⚠️ contaminated | 1 | 2 | BLOCK (HAS-BUGS, correct) | 1 | **PASS*** | ~9.8 min | *Critic READ THE RUBRIC (I1); S3 not creditable. Audit clean & blind |
| 4 | login-form-clean | 1 (S1a=0,S1b=1) | 2 | ~0.86 | **0** | 1 (S5a=1,S5b=0) | **REVISE** (exp PASS) | N/A | **FAIL** | ~10.6 min | Scope-inflated escalation + non-PASS audit — but FIXTURE IS MISLABELED (I8): real MAJOR stale-error bug exists |

(Fixtures 2, 5, 6, 7, 8 — not run in pilot.)

### Automated (score_chain.py) vs Manual — divergences are instrument findings
| Fixture | S3 auto | S3 manual | S4 auto | Tracer auto | Tracer manual | Audit-verdict auto |
|---|---|---|---|---|---|---|
| modal | 0.214 | ~0.6 | 1 | 0 (false-neg) | 1 | — |
| video | 1.0 (contaminated) | discard | 1 | 0 (false-neg) | 1 | — |
| login | 0.429 | ~0.86 | 0 | — | N/A | 1 "PASS" (FALSE-POS; actual REVISE) |

Auto S3 under-counts (taxonomy P_MAP gaps, I2); auto tracer false-negatives (literal
substring, I3); auto audit-verdict false-positive (checklist "PASS" token, I4).

---

## Aggregate (pilot, 3 fixtures — manual)

| Metric | This Run | Watch Threshold | Read |
|--------|----------|-----------------|------|
| S4 escalation accuracy | 2/3 (modal✓ video✓ login✗) | any miss investigated | video✓ contaminated; login✗ = fixture mislabel, not chain defect |
| Audit verdict (CLEAN fixtures) | 0/1 (login REVISE) | non-PASS = failure | login carries a real bug → REVISE is correct; fixture label is wrong |
| S1 mean | 1.0 | ≥ 1.5 | **below** — all 3 scouts blew the 1500-char budget (I7) |
| S2 mean | 2.0 | ≥ 1.5 | **strong** — planner→file→critic handoff perfect every time |
| S3 mean (manual) | ~0.5 usable | ≥ 0.7 | depressed by taxonomy mismatch + 1 contaminated |
| S5 mean | 1.67 | ≥ 1.5 | audits scoped correctly, found real issues |
| Tracer survival (manual) | 2/2 | ≥ 5/6 | both defined tracers survived end-to-end |
| Fixture PASS rate (manual) | 2/3 | 8/8 | login "fail" = mislabeled fixture |

---

## Session Record Index

| Fixture | Session dir | escalated | Plan file |
|---------|------------|-----------|-----------|
| modal-broken-focus-trap | pilot/modal-broken-focus-trap/ | true (audit ran) | docs/a11y-plans/2026-06-13-subscribe-modal-a11y-plan.md |
| video-tutorial-no-captions | pilot/video-tutorial-no-captions/ | true (audit ran) | docs/a11y-plans/2026-06-13-video-tutorial-a11y-plan.md |
| login-form-clean | pilot/login-form-clean/ | true (audit ran) | docs/a11y-plans/2026-06-13-login-form-a11y-plan.md |

Each session dir holds scout.md, planner-plan.md, critic.md, audit.md (+ .txt copies + escalated.txt for the scorer).
