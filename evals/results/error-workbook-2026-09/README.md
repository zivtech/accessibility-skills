# error-workbook-2026-09 — PT-18 canary receipts

Mutation-canary battery for `.claude/skills/bug-reporting/references/build-error-workbook.mjs` (PT-18: XLSX error-workbook builder, `bug-reporting` reference script). The script is a deterministic serializer, so this lane has **no model rows**; its falsifiable check is this battery (PT-21's canary discipline, folded). Boundary and library choice: `docs/error-workbook-adoption-assessment.md`. Maker/community survey: `evals/results/promotion-eval-2026-09/memos/1.9-xlsx-maker-skill-survey.md`.

## Files

- `canaries.md` — the receipt, verbatim, from a sonnet subagent run in a scratch project (`node v24.19.0`, `exceljs@4.4.0`); each section carries the mutation script, the exact command, the verbatim output, and the exit code. The only edit is the canonical script path rewritten to `<repo>/`. The coordinating session re-ran C4 and C6 live and reproduced both.
- `findings.json` — the five-row synthetic input (example.com URLs; no engagement data).

## Results

| Canary | Expected exit | Actual exit | Result | Note |
|---|---|---|---|---|
| C1 clean round trip | 0 | 0 | PASS | rebuild + verify both clean |
| C2 delete Findings row 4 | 1 | 1 | PASS | row-count mismatch + 37 per-cell diffs |
| C3 Findings!F3 → "low" | 1 | 1 | PASS | names `Findings!F3 (severity)` |
| C4 Summary formula `$F$6` → `$F$5` | 1 | 1 | PASS | "range ends at row 5, data ends at row 6" |
| C5 Findings!AF3 → `#REF!` | 1 | 1 | PASS | "Excel error value" reported |
| C6 fill all triage columns (relaxation) | 0 | 0 | PASS | triage columns excluded by design |
| C7 verify against a different input | 1 | 1 | PASS | `E2` diff and Read Me SHA-256 mismatch both present |
| C8a duplicate `instance_id` | 2 | 2 | PASS | names row 3, first seen row 1 |
| C8b `xpath` deleted | 2 | 2 | PASS | names row 2, field xpath |
| C8c severity "blocker" | 2 | 2 | PASS | names row 1, field severity |
| C8d `wcag_sc` "1.4" | 2 | 2 | PASS | names row 4, field wcag_sc |
| C8e 40,000-char `html_snippet` | 2 | 2 | PASS | names row 5, field html_snippet |
| C8f `[]` | 2 | 2 | PASS | "zero issues; nothing to serialize" |
| C8g `--out foo.txt` | 2 | 2 | PASS | "--out must end in .xlsx" |
| C8h `--bogus` | 2 | 2 | PASS | "unrecognized argument --bogus" |
| C8i missing `--in` file | 2 | 2 | PASS | ENOENT named |
| C9 ignored keys on Read Me | read-back | — | PASS | `contract_severity (1), sample_id (1)` |
| C10 SC rollup order and counts | read-back | — | PASS | `1.1.1=2, 2.4.7=1, 4.1.2=1, N/A=1` |
| C11 Summary sheet removed | 1 | 1 | PASS | `missing sheet "Summary"` |
| C12 Read Me Findings → 4 | 1 | 1 | PASS | "Read Me: Findings 4 expected 5" |
| C13 status dropdown validation present | read-back | — | PASS | `AE2` list formula contains "Not Started" |

## Reproduce

From a scratch directory (never inside this repository):

```bash
npm init -y && npm install exceljs@4.4.0
cp <repo>/.claude/skills/bug-reporting/references/build-error-workbook.mjs .
cp <repo>/evals/results/error-workbook-2026-09/findings.json .
node build-error-workbook.mjs --in findings.json --out findings.xlsx --product "Example storefront"
node build-error-workbook.mjs --verify findings.xlsx --in findings.json    # expect exit 0
```

Mutation scripts for C2–C7 and C11–C12 are reproduced in `canaries.md`; each loads `findings.xlsx` with exceljs, applies one change, saves to a new file, and runs `--verify` on it.

## Not covered

No spreadsheet application rendered or recalculated these workbooks; cached formula results are checked, evaluation is not. No screen-reader pass over the workbook. Five rows only.
