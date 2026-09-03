# error-workbook-2026-09 — PT-18 canary receipts

Mutation-canary battery for `.claude/skills/bug-reporting/references/build-error-workbook.mjs` (PT-18: XLSX error-workbook builder, `bug-reporting` reference script). The script is a deterministic serializer, so this lane has **no model rows**; its falsifiable check is this battery (PT-21's canary discipline, folded). Boundary and library choice: `docs/error-workbook-adoption-assessment.md`. Maker/community survey: `evals/results/promotion-eval-2026-09/memos/1.9-xlsx-maker-skill-survey.md`.

## Files

- `canaries-rev2.md` — **current.** The receipt for the committed script (SHA-256 `2550ab11…`, commit `07dd471`, after the critic fold): 29 canary rows across 21 sections, verbatim, from a sonnet subagent run in a scratch project (`node v24.19.0`, `exceljs@4.4.0`). The coordinating session re-ran C14 and C18 live and reproduced both.
- `canaries.md` — rev 1, kept for the record: the same battery's first 21 rows against the pre-fold script (SHA-256 `f31d7bc2…`, commit `ab93c01`). It is the receipt the harsh-critic gated; its Summary cells sit two rows higher than rev 2's.
- `critic-rounds.md` — both critic verdicts verbatim (a11y-critic ACCEPT with 2 MAJOR placement fixes; harsh-critic REVISE with 1 MAJOR) and the fold table. The MAJOR — `--verify` matching Summary cells by content, so a row swap passed clean — is why rev 2 exists.
- `findings.json` — the five-row synthetic input (example.com URLs; no engagement data).

## Results (rev 2, current)

| Canary | Expected exit | Actual exit | Result | Note |
|---|---|---|---|---|
| C1 clean round trip | 0 | 0 | PASS | rebuild + verify both clean |
| C2 delete Findings row 4 | 1 | 1 | PASS | row-count mismatch + per-cell diffs |
| C3 Findings!F3 → "low" | 1 | 1 | PASS | names `Findings!F3 (severity)` |
| C4 Summary formula `$F$6` → `$F$5` (now B4) | 1 | 1 | PASS | "range ends at row 5, data ends at row 6" |
| C5 Findings!AF3 → `#REF!` | 1 | 1 | PASS | "Excel error value" reported |
| C6 fill all triage columns (relaxation) | 0 | 0 | PASS | triage columns excluded by design |
| C7 verify against a different input | 1 | 1 | PASS | `E2` diff + Read Me SHA-256 + Source bytes drift |
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
| C14 Summary rows swapped (labels + formulas) | 1 | 1 | PASS | names A4/B4/A5/B5 — the harsh-critic MAJOR |
| C15 Summary formulas swapped, labels kept | 1 | 1 | PASS | names B4 and B5 |
| C16 Read Me "Stable instance IDs" → "5 of 5" | 1 | 1 | PASS | names the field |
| C17 Summary!A1 boundary line altered | 1 | 1 | PASS | "boundary line missing or altered" |
| C18 `FindingsTable` removed | 1 | 1 | PASS | "defined table … is missing" |
| C19 verify with an invalid input | 2 | 2 | PASS | "refusing to verify against invalid input" |
| C20 status-cell input message present | read-back | — | PASS | `showInputMessage` true, prompt carries the boundary |
| C21 workbook title property | read-back | — | PASS | "Accessibility findings — Example storefront" |

Rev 1 (pre-fold script) scored 21/21 on C1–C13; C14–C21 did not exist then, and C14/C15 would have passed clean against that script — which is the defect the harsh-critic found.

## Reproduce

From a scratch directory (never inside this repository):

```bash
npm init -y && npm install exceljs@4.4.0
cp <repo>/.claude/skills/bug-reporting/references/build-error-workbook.mjs .
cp <repo>/evals/results/error-workbook-2026-09/findings.json .
node build-error-workbook.mjs --in findings.json --out findings.xlsx --product "Example storefront"
node build-error-workbook.mjs --verify findings.xlsx --in findings.json    # expect exit 0
```

Mutation scripts for every mutating canary are reproduced in `canaries-rev2.md`; each loads `findings.xlsx` with exceljs, applies one change, saves to a new file, and runs `--verify` on it.

## Not covered

No spreadsheet application rendered or recalculated these workbooks; cached formula results are checked, evaluation is not. No screen-reader pass over the workbook. Five rows only. A table whose *span* (not presence) is wrong was not mutated — exceljs exposes no API to resize a read-back table — so that branch of `verifyTable` is exercised only by the C2 row deletion, where the table ref and the row count disagree together.
