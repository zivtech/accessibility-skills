# Promotion-candidate evaluation receipts (2026-09-02)

Receipts for `docs/plans/2026-09-02-promotion-candidate-dispositions.md` — Phase 1 of the program that evaluates the 21 engagement-tooling candidates catalogued in PR #39. Nothing here is a promotion; these are the measurements and read-only analyses the dispositions cite. Engagement products are referred to as product-A / product-B (client-reference policy, PR #41).

## Contents

| Path | What it is | Produced by |
|---|---|---|
| `1.1-alfa-overlap/` | Alfa vs axe-core + HTML_CodeSniffer overlap measurement on six public pages: `README.md` (setup, resolved versions, robots check, requirements-join method + coverage, verdict, negative space), `overlap-table.md` (per-page and cross-page tables, threshold computation), `commands.sh` (verbatim commands), `package.json` + `package-lock.json` (exact pins), `analysis-summary.json`, `project/` (the runner, join, and analysis scripts plus `requirements-map.json` and `join-coverage.json`), `raw/` (per-page per-engine output) | sonnet subagent, scratch project — nothing installed in this repo |
| `memos/1.2-scorer-spike.md` | PT-01 structured-output contract spike: draft skill text, metadata-key → check map, 18-canary set, file-by-file work-package scope, CI/cost | sonnet subagent, read-only |
| `memos/1.3-memo-pt09.md` | PT-09 sample-set validator: 22-check inventory classified generic / engagement-shaped, 10 generic rules, YAML shape, 10 canaries | sonnet subagent, read-only |
| `memos/1.3-memo-pt19.md` | PT-19 interim OpenACR builder vs acr-reporting skill: nine items with builder ↔ skill ↔ scorer line cites, two verified empirically with the pinned CLI in a scratch dir | sonnet subagent, read-only |
| `memos/1.3-memo-pt03.md` | PT-03 resumption ledger: what the engagement builder does, separability into `baseline-url-scan.mjs`, reuse guards, canaries | sonnet subagent, read-only |
| `memos/1.4-scans.md` | Mechanical scans: client-identifier counts per candidate script (with the EPA positive control), dedupe grep on `main` per candidate, GT-05 overlap grep, gate coverage. **Redacted copy** — literal patterns replaced by `<…>` placeholders so the report passes the gate it describes | haiku subagent |

## Raw Alfa outputs are slimmed

`raw/page-<n>-alfa.json` keep only `failed` and `cantTell` outcomes plus `resultAggregates` and per-kind outcome counts; `passed`/`inapplicable` outcomes (the bulk of the 1–2 MB originals) are dropped. Each slimmed file records the original's SHA-256 and byte size (`_full_file_sha256`, `_full_file_bytes`) so a re-run can be compared. axe and htmlcs raw outputs are complete.

## Headline numbers

| Measure | Value |
|---|---|
| Pages × engines | 6 × 3, all ran clean |
| Alfa rules (default stable set) | 89; 58 carry ≥1 WCAG criterion requirement |
| Failing Alfa rule ids mapped to a criterion | 16 of 22 (72.7 %); the 6 unmapped are best-practice rules with no SC binding |
| Alfa-only A/AA rule classes (not flagged by axe or htmlcs on the same page) | **2** (`sia-r14` → 2.5.3; `sia-r69` → 1.4.3), both plausible true positives, agent-assessed |
| Pre-declared threshold | ≥3 classes + ≥1 plausible true positive |
| Verdict | **below threshold** |

## Not claimed

Six pages, one viewport, one day, one version set. No keyboard or screen-reader evidence — all three engines are static DOM detectors. No conformance verdict of any kind. The two Alfa-only findings have not been human-confirmed against the live pages.
