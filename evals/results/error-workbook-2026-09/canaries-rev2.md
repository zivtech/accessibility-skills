# build-error-workbook.mjs — mutation canary battery (rev 2)

- `node --version`: v24.19.0
- exceljs version (node_modules/exceljs/package.json): 4.4.0
- `build-error-workbook.mjs` SHA-256 (scratchpad copy): `2550ab116138cb8cb303b046a3e2937c661db3965cabdd362d6d28c304381656`
- `build-error-workbook.mjs` SHA-256 (canonical `<repo>/.claude/skills/bug-reporting/references/build-error-workbook.mjs`): `2550ab116138cb8cb303b046a3e2937c661db3965cabdd362d6d28c304381656`
- Hashes match — no copy was needed.

Revision under test vs. the rev-1 script this battery previously exercised (see `canaries.md`, not overwritten by this file):
- Summary sheet gained a boundary text line in `A1`; blocks now start at row 3 (`SUMMARY_FIRST_ROW = 3`), so "By severity" is titled at row 3 and "critical" sits at `B4` (was `B2`), "high" at `B5` (was `B3`).
- `--verify` now additionally checks Summary cells by exact position, the Findings defined table's span, and ten Read Me fields (all rows except Title, Product, Generated (UTC), Source file, Verify).
- The status dropdown (`Findings!AE` data validation) now carries `showInputMessage: true` and a `prompt`.
- Read Me gained a "Normalization" row, shifting field rows below "Input keys not serialized" down by one.
- Findings header "Colour mode" → "Color mode".

All commands below were run with cwd = the scratchpad directory. Step 1 built `findings-rev2.xlsx` (`--in findings.json --out findings-rev2.xlsx --product "Example storefront"`); every mutation script below loads `findings-rev2.xlsx` and saves to a new file, never overwriting it. C1 reuses this same base build as its "fresh build" (its content is unaffected by `--product`, since `--verify`'s Read Me check excludes the Title/Product rows), and it is also the source read back by C9/C10/C13/C20/C21.

---

## C1 clean rebuild

Build (step 1), then verify the fresh build against its own input.

```
node build-error-workbook.mjs --in findings.json --out findings-rev2.xlsx --product "Example storefront"
```
```
wrote findings-rev2.xlsx: 5 findings, 3 with instance_id — ignored keys: contract_severity, sample_id
```
exit=0

```
node build-error-workbook.mjs --verify findings-rev2.xlsx --in findings.json
```
```
verify findings-rev2.xlsx: 5 findings, 15 formulas, 0 drift
```
exit=0

Expected: exit 0. **PASS**

---

## C2 delete Findings row 4

`mut-c2v2.mjs` (unchanged from rev-1's `mut-c2.mjs` — Findings sheet layout unaffected by the Summary/Read Me revisions — retargeted at `findings-rev2.xlsx` → `c2v2.xlsx`):
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings-rev2.xlsx');
const ws = wb.getWorksheet('Findings');
ws.spliceRows(4, 1); // delete data row 4 (issue index 2)
await wb.xlsx.writeFile('c2v2.xlsx');
```

```
node mut-c2v2.mjs
```
```
wrote c2v2.xlsx
```
exit=0

```
node build-error-workbook.mjs --verify c2v2.xlsx --in findings.json
```
```
verify c2v2.xlsx: 5 findings, 15 formulas, 38 drift
  Findings: 4 data row(s) present, input has 5
  Findings!A4 (#): "4" expected "3"
  Findings!B4 (instance_id): "" expected "EX-11223344"
  Findings!D4 (finding_id): "a11y_focus_not_visible_nav" expected ""
  Findings!E4 (summary): "Focus indicator not visible on nav links" expected "Icon-only button has no accessible name"
  Findings!F4 (severity): "medium" expected "high"
  Findings!G4 (wcag_sc): "2.4.7" expected "4.1.2"
  Findings!H4 (wcag_level): "AA" expected "A"
  Findings!I4 (rule_id): "N/A" expected "button-name"
  Findings!K4 (baseline_test): "" expected "5.A-ControlName"
  Findings!L4 (tool): "manual keyboard test" expected "axe-core 4.13.0"
  Findings!M4 (url): "https://example.com/" expected "https://example.com/checkout"
  Findings!P4 (xpath): "//nav/a[3]" expected "//form/button[2]"
  Findings!R4 (html_snippet): "<a href="/about">About</a>" expected "<button class="icon"><svg/></button>"
  Findings!V4 (description): "outline: none with no replacement." expected ""
  Findings!X4 (steps_to_reproduce): "1. Load the home page
2. Press Tab three times" expected ""
  Findings!A5 (#): "5" expected "4"
  Findings!D5 (finding_id): "" expected "a11y_focus_not_visible_nav"
  Findings!E5 (summary): "Content outside landmarks" expected "Focus indicator not visible on nav links"
  Findings!F5 (severity): "low" expected "medium"
  Findings!G5 (wcag_sc): "N/A" expected "2.4.7"
  Findings!H5 (wcag_level): "" expected "AA"
  Findings!I5 (rule_id): "best-practice: region" expected "N/A"
  Findings!L5 (tool): "axe-core 4.13.0 (best-practice)" expected "manual keyboard test"
  Findings!M5 (url): "https://example.com/faq" expected "https://example.com/"
  Findings!P5 (xpath): "//details[1]/summary" expected "//nav/a[3]"
  Findings!R5 (html_snippet): "<summary>How do I…</summary>" expected "<a href="/about">About</a>"
  Findings!V5 (description): "" expected "outline: none with no replacement."
  Findings!X5 (steps_to_reproduce): "" expected "1. Load the home page
2. Press Tab three times"
  Findings!A6 (#): "" expected "5"
  Findings!E6 (summary): "" expected "Content outside landmarks"
  Findings!F6 (severity): "" expected "low"
  Findings!G6 (wcag_sc): "" expected "N/A"
  Findings!I6 (rule_id): "" expected "best-practice: region"
  Findings!L6 (tool): "" expected "axe-core 4.13.0 (best-practice)"
  Findings!M6 (url): "" expected "https://example.com/faq"
  Findings!P6 (xpath): "" expected "//details[1]/summary"
  Findings!R6 (html_snippet): "" expected "<summary>How do I…</summary>"
```
exit=1

Expected: exit 1, row-count mismatch plus per-cell diffs. **PASS**

---

## C3 set Findings!F3 severity to "low"

`mut-c3v2.mjs` (unchanged logic, retargeted at `findings-rev2.xlsx` → `c3v2.xlsx`):
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings-rev2.xlsx');
const ws = wb.getWorksheet('Findings');
ws.getCell('F3').value = 'low'; // was 'critical'
await wb.xlsx.writeFile('c3v2.xlsx');
```

```
node mut-c3v2.mjs
```
```
wrote c3v2.xlsx
```
exit=0

```
node build-error-workbook.mjs --verify c3v2.xlsx --in findings.json
```
```
verify c3v2.xlsx: 5 findings, 15 formulas, 1 drift
  Findings!F3 (severity): "low" expected "critical"
```
exit=1

Expected: exit 1, names `Findings!F3 (severity)`. **PASS**

---

## C4 shrink Summary!B4 formula range ($F$6 → $F$5), cached result unchanged

`mut-c4v2.mjs` — **adapted from rev-1's `mut-c4.mjs`**: the "critical" cell moved from `B2` to `B4` (Summary now has a boundary line at row 1 and the first block title at row 3, per `SUMMARY_FIRST_ROW = 3`):
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings-rev2.xlsx');
const ws = wb.getWorksheet('Summary');
const cell = ws.getCell('B4'); // "critical" row is now B4, not B2
const v = cell.value;
if (!v || typeof v !== 'object' || !('formula' in v) || !v.formula.includes('$F$6')) {
  throw new Error('B4 does not hold the expected $F$6 formula; aborting');
}
cell.value = { formula: v.formula.replace('$F$6', '$F$5'), result: v.result };
await wb.xlsx.writeFile('c4v2.xlsx');
```

```
node mut-c4v2.mjs
```
```
before: {"formula":"COUNTIF(Findings!$F$2:$F$6,\"critical\")","result":2}
wrote c4v2.xlsx, new formula: COUNTIF(Findings!$F$2:$F$5,"critical")
```
exit=0

```
node build-error-workbook.mjs --verify c4v2.xlsx --in findings.json
```
```
verify c4v2.xlsx: 5 findings, 15 formulas, 1 drift
  Summary!B4 ("critical"): range ends at row 5, data ends at row 6
```
exit=1

Expected: exit 1, "range ends at row 5, data ends at row 6" (now on `Summary!B4`). **PASS**

---

## C5 set Findings!AF3 (Notes) to "#REF!"

`mut-c5v2.mjs` (unchanged — triage column position is unaffected by the revision — retargeted at `findings-rev2.xlsx` → `c5v2.xlsx`):
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings-rev2.xlsx');
const ws = wb.getWorksheet('Findings');
ws.getCell('AF3').value = '#REF!'; // triage Notes column, row 3
await wb.xlsx.writeFile('c5v2.xlsx');
```

```
node mut-c5v2.mjs
```
```
wrote c5v2.xlsx
```
exit=0

```
node build-error-workbook.mjs --verify c5v2.xlsx --in findings.json
```
```
verify c5v2.xlsx: 5 findings, 15 formulas, 1 drift
  Findings!AF3: Excel error value "#REF!"
```
exit=1

Expected: exit 1, "Excel error value". **PASS**

---

## C6 RELAXATION — fill Owner/Remediation status/Notes on rows 2-6

`mut-c6v2.mjs` (unchanged logic, retargeted at `findings-rev2.xlsx` → `c6v2.xlsx`):
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings-rev2.xlsx');
const ws = wb.getWorksheet('Findings');
for (let r = 2; r <= 6; r += 1) {
  ws.getCell(`AD${r}`).value = 'Sam';
  ws.getCell(`AE${r}`).value = 'In Progress';
  ws.getCell(`AF${r}`).value = 'on it';
}
await wb.xlsx.writeFile('c6v2.xlsx');
```

```
node mut-c6v2.mjs
```
```
wrote c6v2.xlsx
```
exit=0

```
node build-error-workbook.mjs --verify c6v2.xlsx --in findings.json
```
```
verify c6v2.xlsx: 5 findings, 15 formulas, 0 drift
```
exit=0

Expected: triage columns excluded by design → exit 0. **PASS**

---

## C7 input drift — findings-b.json (row 1 summary changed by one word) verified against the base findings-rev2.xlsx

No new script needed: `findings-b.json` already existed from the rev-1 run (rev-1's `gen-c7.mjs`, unchanged — it reads `findings.json`, which is unchanged, so its output is unaffected by this revision).

```
node build-error-workbook.mjs --verify findings-rev2.xlsx --in findings-b.json
```
```
verify findings-rev2.xlsx: 5 findings, 15 formulas, 3 drift
  Findings!E2 (summary): "Hero image has no text alternative" expected "Hero graphic has no text alternative"
  Read Me: Source SHA-256 "2791fcb288efed34bf387e6b587209d7c9583077972bfc194fcb52707f05" expected "7fb75b59e96aa441c7c76731ce28f3c5c4b702445a3654ecd7e1d80ea714"
  Read Me: Source bytes "2406" expected "2918"
```
exit=1

Expected: exit 1 with a `Findings!E2` diff and a Read Me Source SHA-256 mismatch line. **PASS** — the revised `--verify` also now names a third drift line, "Read Me: Source bytes", that rev-1's receipt did not show (rev-1's Read Me check evidently didn't diff that row, or used a different message shape); this is the revised script's own uniform per-field Read Me diff format (`verifyReadme`) correctly catching a real byte-count difference between `findings.json` and `findings-b.json`, not a false positive — no adaptation was needed, the extra line is genuine broader coverage.

---

## C8 build refusals

Reused rev-1's `c8a.json` .. `c8f.json` unchanged (generated from `findings.json`, which did not change; `gen-c8.mjs` needed no adaptation). Outputs written to `*-v2.xlsx` names; all of these exit before any file is written.

### (a) duplicate instance_id
```
node build-error-workbook.mjs --in c8a.json --out c8a-v2.xlsx
```
```
refusing to build: 1 invalid row(s)
  row 3: duplicate instance_id EX-a3f1b2c4 (first seen row 1)
```
exit=2 — names row 3 and the field. **PASS**

### (b) delete xpath from row 2
```
node build-error-workbook.mjs --in c8b.json --out c8b-v2.xlsx
```
```
refusing to build: 1 invalid row(s)
  row 2: missing required field xpath
```
exit=2 — names row 2 and field `xpath`. **PASS**

### (c) severity "blocker" on row 1
```
node build-error-workbook.mjs --in c8c.json --out c8c-v2.xlsx
```
```
refusing to build: 1 invalid row(s)
  row 1: severity "blocker" not in critical/high/medium/low
```
exit=2 — names row 1 and field `severity`. **PASS**

### (d) wcag_sc "1.4" on row 4
```
node build-error-workbook.mjs --in c8d.json --out c8d-v2.xlsx
```
```
refusing to build: 1 invalid row(s)
  row 4: wcag_sc "1.4" is not x.y.z or N/A
```
exit=2 — names row 4 and field `wcag_sc`. **PASS**

### (e) html_snippet of 40,000 'x' characters on row 5
```
node build-error-workbook.mjs --in c8e.json --out c8e-v2.xlsx
```
```
refusing to build: 1 invalid row(s)
  row 5: html_snippet is 40000 characters; Excel cells hold 32767
```
exit=2 — names row 5 and field `html_snippet`. **PASS**

### (f) `[]` empty array
```
node build-error-workbook.mjs --in c8f.json --out c8f-v2.xlsx
```
```
--in c8f.json: zero issues; nothing to serialize
```
exit=2 — usage-level refusal. **PASS**

### (g) --out foo.txt (wrong extension)
```
node build-error-workbook.mjs --in findings.json --out foo.txt
```
```
--out must end in .xlsx
```
exit=2 — usage error naming the bad flag value. **PASS**

### (h) --bogus flag
```
node build-error-workbook.mjs --bogus
```
```
unrecognized argument --bogus
```
exit=2 — usage error naming the bad flag. **PASS**

### (i) --in nonexistent.json
```
node build-error-workbook.mjs --in nonexistent.json --out foo.xlsx
```
```
cannot read --in nonexistent.json: ENOENT: no such file or directory, open 'nonexistent.json'
```
exit=2 — usage error naming the missing file. **PASS**

---

## C9 ignored keys (read findings-rev2.xlsx Read Me back)

`read-c9v2.mjs` (unchanged logic — search is by field label, not row position, so the new "Normalization" row does not require adaptation — retargeted at `findings-rev2.xlsx`).

```
node read-c9v2.mjs
```
```
contract_severity (1), sample_id (1)
```

Expected: `contract_severity (1), sample_id (1)`. **PASS**

---

## C10 SC ordering (read findings-rev2.xlsx Summary back)

`read-c10v2.mjs` (unchanged logic — the scan walks rows by content, detecting the "By WCAG success criterion" title text and reading until the next non-data row, so it is layout-shift-safe and needed no adaptation for the row-4 relayout — retargeted at `findings-rev2.xlsx`).

```
node read-c10v2.mjs
```
```
1.1.1=2, 2.4.7=1, 4.1.2=1, N/A=1
```

Expected: `1.1.1=2, 2.4.7=1, 4.1.2=1, N/A=1` in that order. **PASS**

---

## C11 remove the Summary worksheet

`mut-c11v2.mjs` (unchanged logic, retargeted at `findings-rev2.xlsx` → `c11v2.xlsx`):
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings-rev2.xlsx');
const ws = wb.getWorksheet('Summary');
wb.removeWorksheet(ws.id);
await wb.xlsx.writeFile('c11v2.xlsx');
```

```
node mut-c11v2.mjs
```
```
wrote c11v2.xlsx
```
exit=0

```
node build-error-workbook.mjs --verify c11v2.xlsx --in findings.json
```
```
verify c11v2.xlsx: 5 findings, 0 formulas, 1 drift
  missing sheet "Summary"
```
exit=1

Expected: exit 1, "missing sheet". **PASS**

---

## C12 set Read Me "Findings" value cell to 4

`mut-c12v2.mjs` (unchanged logic — finds the row by scanning for label `"Findings"` in column A, so the new "Normalization" row's shift needed no adaptation — retargeted at `findings-rev2.xlsx` → `c12v2.xlsx`):
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings-rev2.xlsx');
const ws = wb.getWorksheet('Read Me');
ws.eachRow((row) => {
  if (row.getCell(1).value === 'Findings') row.getCell(2).value = 4;
});
await wb.xlsx.writeFile('c12v2.xlsx');
```

```
node mut-c12v2.mjs
```
```
wrote c12v2.xlsx
```
exit=0

```
node build-error-workbook.mjs --verify c12v2.xlsx --in findings.json
```
```
verify c12v2.xlsx: 5 findings, 15 formulas, 1 drift
  Read Me: Findings "4" expected "5"
```
exit=1

Expected: exit 1, names Read Me Findings. **PASS**

---

## C13 data validation present (read findings-rev2.xlsx back)

`read-c13v2.mjs` reads `Findings!AE2`'s `dataValidation` (unchanged logic and cell address — the triage column position is unaffected by the revision — retargeted at `findings-rev2.xlsx`):

```
node read-c13v2.mjs
```
```
AE2 dataValidation: {"type":"list","formulae":["\"Not Started,In Progress,Ready for Retest,Resolved,Deferred\""],"allowBlank":true,"showInputMessage":true,"showErrorMessage":true,"promptTitle":"Remediation status","prompt":"Your team's workflow state. Not verification: a fix is closed by the auditor from class-matched retest evidence, not by this cell.","errorTitle":"Remediation status","error":"Choose one of: Not Started, In Progress, Ready for Retest, Resolved, Deferred"}
true
```

Expected: list dataValidation whose formula contains "Not Started" → true. **PASS** (the object now also carries `showInputMessage: true` and a `prompt`, which C20 below checks explicitly — this is the revision's new behavior, not a false read.)

---

## C14 (NEW) Summary row swap — swap label AND formula/result of "critical" and "high" rows

`mut-c14.mjs`:
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings-rev2.xlsx');
const ws = wb.getWorksheet('Summary');
const a4 = ws.getCell('A4').value;
const b4 = ws.getCell('B4').value;
const a5 = ws.getCell('A5').value;
const b5 = ws.getCell('B5').value;
ws.getCell('A4').value = a5;
ws.getCell('B4').value = b5;
ws.getCell('A5').value = a4;
ws.getCell('B5').value = b4;
await wb.xlsx.writeFile('c14.xlsx');
```

```
node mut-c14.mjs
```
```
swapped A4/B4 <-> A5/B5 (label+formula/result)
```
exit=0

```
node build-error-workbook.mjs --verify c14.xlsx --in findings.json
```
```
verify c14.xlsx: 5 findings, 15 formulas, 4 drift
  Summary!A4: "high" expected "critical"
  Summary!B4 ("critical"): formula "COUNTIF(Findings!$F$2:$F$6,"high")" expected "COUNTIF(Findings!$F$2:$F$6,"critical")"
  Summary!A5: "critical" expected "high"
  Summary!B5 ("high"): formula "COUNTIF(Findings!$F$2:$F$6,"critical")" expected "COUNTIF(Findings!$F$2:$F$6,"high")"
```
exit=1

Expected: exit 1, output names Summary!A4/B4/A5/B5. **PASS**

---

## C15 (NEW) Summary formula-only swap — swap only B4 and B5 values, leave labels

`mut-c15.mjs`:
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings-rev2.xlsx');
const ws = wb.getWorksheet('Summary');
const b4 = ws.getCell('B4').value;
const b5 = ws.getCell('B5').value;
ws.getCell('B4').value = b5; // labels A4/A5 left untouched
ws.getCell('B5').value = b4;
await wb.xlsx.writeFile('c15.xlsx');
```

```
node mut-c15.mjs
```
```
swapped B4/B5 values only, labels unchanged
```
exit=0

```
node build-error-workbook.mjs --verify c15.xlsx --in findings.json
```
```
verify c15.xlsx: 5 findings, 15 formulas, 2 drift
  Summary!B4 ("critical"): formula "COUNTIF(Findings!$F$2:$F$6,"high")" expected "COUNTIF(Findings!$F$2:$F$6,"critical")"
  Summary!B5 ("high"): formula "COUNTIF(Findings!$F$2:$F$6,"critical")" expected "COUNTIF(Findings!$F$2:$F$6,"high")"
```
exit=1

Expected: exit 1 naming B4 and B5. **PASS**

---

## C16 (NEW) Read Me tamper — "Stable instance IDs supplied" set to "5 of 5"

`mut-c16.mjs`:
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings-rev2.xlsx');
const ws = wb.getWorksheet('Read Me');
ws.eachRow((row) => {
  if (row.getCell(1).value === 'Stable instance IDs supplied') row.getCell(2).value = '5 of 5';
});
await wb.xlsx.writeFile('c16.xlsx');
```

```
node mut-c16.mjs
```
```
wrote c16.xlsx
```
exit=0

```
node build-error-workbook.mjs --verify c16.xlsx --in findings.json
```
```
verify c16.xlsx: 5 findings, 15 formulas, 1 drift
  Read Me: Stable instance IDs supplied "5 of 5" expected "3 of 5"
```
exit=1

Expected: exit 1, names that field. **PASS**

---

## C17 (NEW) Summary boundary altered — Summary!A1 set to "Conformance summary"

`mut-c17.mjs`:
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings-rev2.xlsx');
const ws = wb.getWorksheet('Summary');
ws.getCell('A1').value = 'Conformance summary';
await wb.xlsx.writeFile('c17.xlsx');
```

```
node mut-c17.mjs
```
```
wrote c17.xlsx
```
exit=0

```
node build-error-workbook.mjs --verify c17.xlsx --in findings.json
```
```
verify c17.xlsx: 5 findings, 15 formulas, 1 drift
  Summary!A1: boundary line missing or altered
```
exit=1

Expected: exit 1 mentioning the boundary line. **PASS**

---

## C18 (NEW) table removed — ws.removeTable('FindingsTable') on Findings

`mut-c18.mjs`:
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings-rev2.xlsx');
const ws = wb.getWorksheet('Findings');
try {
  ws.removeTable('FindingsTable');
  await wb.xlsx.writeFile('c18.xlsx');
  console.log('removeTable succeeded; wrote c18.xlsx');
} catch (err) {
  console.log('removeTable threw:', err && err.stack ? err.stack : String(err));
  process.exitCode = 9;
}
```

```
node mut-c18.mjs
```
```
removeTable succeeded; wrote c18.xlsx
```
exit=0 — exceljs 4.4.0 *can* remove a table on a freshly-read workbook; the hedge in the assignment (record the exact error and mark NOT RUN if it can't) does not apply here.

```
node build-error-workbook.mjs --verify c18.xlsx --in findings.json
```
```
verify c18.xlsx: 5 findings, 15 formulas, 1 drift
  Findings: defined table "FindingsTable" is missing
```
exit=1

Expected: exit 1 mentioning the defined table. **PASS**

---

## C19 (NEW) verify against invalid input

`c19.json` = `findings.json` with row 1's `severity` overwritten to `"blocker"`:
```
node -e "const fs=require('fs');const i=JSON.parse(fs.readFileSync('findings.json','utf8'));i[0].severity='blocker';fs.writeFileSync('c19.json',JSON.stringify(i,null,2));"
```
```
(no stdout)
```
exit=0

```
node build-error-workbook.mjs --verify findings-rev2.xlsx --in c19.json
```
```
refusing to verify against invalid input: 1 invalid row(s)
  row 1: severity "blocker" not in critical/high/medium/low
```
exit=2

Expected: exit 2, "refusing to verify against invalid input". **PASS**

---

## C20 (NEW) status prompt present — read back Findings!AE2 dataValidation

`read-c20.mjs`:
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings-rev2.xlsx');
const ws = wb.getWorksheet('Findings');
const dv = ws.getCell('AE2').dataValidation;
const showInputMessage = Boolean(dv && dv.showInputMessage === true);
const promptOk = Boolean(dv && typeof dv.prompt === 'string' && dv.prompt.includes('Not verification'));
```

```
node read-c20.mjs
```
```
AE2 dataValidation: {"type":"list","formulae":["\"Not Started,In Progress,Ready for Retest,Resolved,Deferred\""],"allowBlank":true,"showInputMessage":true,"showErrorMessage":true,"promptTitle":"Remediation status","prompt":"Your team's workflow state. Not verification: a fix is closed by the auditor from class-matched retest evidence, not by this cell.","errorTitle":"Remediation status","error":"Choose one of: Not Started, In Progress, Ready for Retest, Resolved, Deferred"}
showInputMessage: true
prompt contains "Not verification": true
```

Expected: `showInputMessage` true and `prompt` contains "Not verification" → true. **PASS**

---

## C21 (NEW) workbook title

`read-c21.mjs`:
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings-rev2.xlsx');
console.log('wb.title:', JSON.stringify(wb.title));
console.log('matches expected:', wb.title === 'Accessibility findings — Example storefront');
```

```
node read-c21.mjs
```
```
wb.title: "Accessibility findings — Example storefront"
matches expected: true
```

Expected: `wb.title` equals "Accessibility findings — Example storefront". **PASS**

---

## Summary

21/21 canaries PASS. No canary was marked NOT RUN — C18's hedge condition (exceljs unable to remove a table on a read-back workbook) did not occur; the removal and the resulting drift detection both worked as expected.
