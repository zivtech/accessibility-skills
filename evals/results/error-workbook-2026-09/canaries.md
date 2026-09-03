# build-error-workbook.mjs — mutation canary battery

- `node --version`: v24.19.0
- exceljs version (node_modules/exceljs/package.json): 4.4.0
- `build-error-workbook.mjs` SHA-256 (scratchpad copy): f31d7bc299c9ff511e21309b758c0d6a4c394ea6655f21be28fafdf6a224f899
- `build-error-workbook.mjs` SHA-256 (canonical `<repo>/.claude/skills/bug-reporting/references/build-error-workbook.mjs`): f31d7bc299c9ff511e21309b758c0d6a4c394ea6655f21be28fafdf6a224f899
- Hashes match — no copy was needed.

All commands below were run with cwd = the scratchpad directory. `findings.xlsx` is the pre-built workbook already present in the scratchpad (built from `findings.json`); mutation scripts load it and save to a new file, never overwriting it. `c1.xlsx` is the fresh rebuild produced by C1 and is the source for C9/C10/C13's read-backs.

---

## C1 clean rebuild

Build, then verify the fresh build against its own input.

```
node build-error-workbook.mjs --in findings.json --out c1.xlsx
```
```
wrote c1.xlsx: 5 findings, 3 with instance_id — ignored keys: contract_severity, sample_id
```
exit=0

```
node build-error-workbook.mjs --verify c1.xlsx --in findings.json
```
```
verify c1.xlsx: 5 findings, 15 formulas, 0 drift
```
exit=0

Expected: exit 0. **PASS**

---

## C2 delete Findings row 4

`mut-c2.mjs`:
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings.xlsx');
const ws = wb.getWorksheet('Findings');
ws.spliceRows(4, 1); // delete data row 4 (issue index 2)
await wb.xlsx.writeFile('c2.xlsx');
```

```
node mut-c2.mjs
```
```
wrote c2.xlsx
```
exit=0

```
node build-error-workbook.mjs --verify c2.xlsx --in findings.json
```
```
verify c2.xlsx: 5 findings, 15 formulas, 38 drift
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

`mut-c3.mjs`:
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings.xlsx');
const ws = wb.getWorksheet('Findings');
ws.getCell('F3').value = 'low'; // was 'critical'
await wb.xlsx.writeFile('c3.xlsx');
```

```
node mut-c3.mjs
```
```
wrote c3.xlsx
```
exit=0

```
node build-error-workbook.mjs --verify c3.xlsx --in findings.json
```
```
verify c3.xlsx: 5 findings, 15 formulas, 1 drift
  Findings!F3 (severity): "low" expected "critical"
```
exit=1

Expected: exit 1, names `Findings!F3 (severity)`. **PASS**

---

## C4 shrink Summary!B2 formula range ($F$6 → $F$5), cached result unchanged

`mut-c4.mjs`:
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings.xlsx');
const ws = wb.getWorksheet('Summary');
const cell = ws.getCell('B2');
const v = cell.value; // {"formula":"COUNTIF(Findings!$F$2:$F$6,\"critical\")","result":2}
cell.value = { formula: v.formula.replace('$F$6', '$F$5'), result: v.result };
await wb.xlsx.writeFile('c4.xlsx');
```

```
node mut-c4.mjs
```
```
before: {"formula":"COUNTIF(Findings!$F$2:$F$6,\"critical\")","result":2}
wrote c4.xlsx, new formula: COUNTIF(Findings!$F$2:$F$5,"critical")
```
exit=0

```
node build-error-workbook.mjs --verify c4.xlsx --in findings.json
```
```
verify c4.xlsx: 5 findings, 15 formulas, 3 drift
  Summary!B2 ("critical"): range ends at row 5, data ends at row 6
  Summary!B2 ("critical"): formula not among the 15 expected: COUNTIF(Findings!$F$2:$F$5,"critical")
  Summary: expected formula for "critical" is missing: COUNTIF(Findings!$F$2:$F$6,"critical")
```
exit=1

Expected: exit 1, "range ends at row 5, data ends at row 6". **PASS**

---

## C5 set Findings!AF3 (Notes) to "#REF!"

`mut-c5.mjs`:
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings.xlsx');
const ws = wb.getWorksheet('Findings');
ws.getCell('AF3').value = '#REF!'; // triage Notes column, row 3
await wb.xlsx.writeFile('c5.xlsx');
```

```
node mut-c5.mjs
```
```
wrote c5.xlsx
```
exit=0

```
node build-error-workbook.mjs --verify c5.xlsx --in findings.json
```
```
verify c5.xlsx: 5 findings, 15 formulas, 1 drift
  Findings!AF3: Excel error value "#REF!"
```
exit=1

Expected: exit 1, "Excel error value". **PASS**

---

## C6 RELAXATION — fill Owner/Remediation status/Notes on rows 2-6

`mut-c6.mjs`:
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings.xlsx');
const ws = wb.getWorksheet('Findings');
for (let r = 2; r <= 6; r += 1) {
  ws.getCell(`AD${r}`).value = 'Sam';
  ws.getCell(`AE${r}`).value = 'In Progress';
  ws.getCell(`AF${r}`).value = 'on it';
}
await wb.xlsx.writeFile('c6.xlsx');
```

```
node mut-c6.mjs
```
```
wrote c6.xlsx
```
exit=0

```
node build-error-workbook.mjs --verify c6.xlsx --in findings.json
```
```
verify c6.xlsx: 5 findings, 15 formulas, 0 drift
```
exit=0

Expected: triage columns excluded by design → exit 0. **PASS**

---

## C7 input drift — findings-b.json (row 1 summary changed by one word) verified against the original findings.xlsx

`gen-c7.mjs`:
```js
import { readFile, writeFile } from 'node:fs/promises';
const issues = JSON.parse(await readFile('findings.json', 'utf8'));
issues[0].summary = issues[0].summary.replace('Hero image', 'Hero graphic'); // one-word change
await writeFile('findings-b.json', JSON.stringify(issues, null, 2));
```

```
node gen-c7.mjs
```
```
wrote findings-b.json; row1 summary now: Hero graphic has no text alternative
```
exit=0

```
node build-error-workbook.mjs --verify findings.xlsx --in findings-b.json
```
```
verify findings.xlsx: 5 findings, 15 formulas, 2 drift
  Findings!E2 (summary): "Hero image has no text alternative" expected "Hero graphic has no text alternative"
  Read Me: Source SHA-256 2791fcb288efed34bf387e6b587209d7c9583077972bfc194fcb52707f053cc9 is not this input's 7fb75b59e96aa441c7c76731ce28f3c5c4b702445a3654ecd7e1d80ea7141c6b
```
exit=1

Expected: exit 1 with both a `Findings!E2` diff and a Read Me SHA-256 mismatch line. **PASS**

---

## C8 build refusals

`gen-c8.mjs` produced c8a.json .. c8f.json from findings.json (a: row 3's `instance_id` overwritten with row 1's; b: `xpath` deleted from row 2; c: row 1 `severity` set to `"blocker"`; d: row 4 `wcag_sc` set to `"1.4"`; e: row 5 `html_snippet` set to 40,000 `'x'` characters; f: `[]`).

### (a) duplicate instance_id
```
node build-error-workbook.mjs --in c8a.json --out c8a.xlsx
```
```
refusing to build: 1 invalid row(s)
  row 3: duplicate instance_id EX-a3f1b2c4 (first seen row 1)
```
exit=2 — names row 3 and the field. **PASS**

### (b) delete xpath from row 2
```
node build-error-workbook.mjs --in c8b.json --out c8b.xlsx
```
```
refusing to build: 1 invalid row(s)
  row 2: missing required field xpath
```
exit=2 — names row 2 and field `xpath`. **PASS**

### (c) severity "blocker" on row 1
```
node build-error-workbook.mjs --in c8c.json --out c8c.xlsx
```
```
refusing to build: 1 invalid row(s)
  row 1: severity "blocker" not in critical/high/medium/low
```
exit=2 — names row 1 and field `severity`. **PASS**

### (d) wcag_sc "1.4" on row 4
```
node build-error-workbook.mjs --in c8d.json --out c8d.xlsx
```
```
refusing to build: 1 invalid row(s)
  row 4: wcag_sc "1.4" is not x.y.z or N/A
```
exit=2 — names row 4 and field `wcag_sc`. **PASS**

### (e) html_snippet of 40,000 'x' characters on row 5
```
node build-error-workbook.mjs --in c8e.json --out c8e.xlsx
```
```
refusing to build: 1 invalid row(s)
  row 5: html_snippet is 40000 characters; Excel cells hold 32767
```
exit=2 — names row 5 and field `html_snippet`. **PASS**

### (f) `[]` empty array
```
node build-error-workbook.mjs --in c8f.json --out c8f.xlsx
```
```
--in c8f.json: zero issues; nothing to serialize
```
exit=2 — usage-level refusal (zero rows, so no single row/field applies); message clearly states the cause. **PASS**

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

## C9 ignored keys (read c1.xlsx Read Me back)

```
node read-c9.mjs
```
```
contract_severity (1), sample_id (1)
```

Expected: `contract_severity (1), sample_id (1)`. **PASS**

---

## C10 SC ordering (read c1.xlsx Summary back)

```
node read-c10.mjs
```
```
1.1.1=2, 2.4.7=1, 4.1.2=1, N/A=1
```

Expected: `1.1.1=2, 2.4.7=1, 4.1.2=1, N/A=1` in that order. **PASS**

---

## C11 remove the Summary worksheet

`mut-c11.mjs`:
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings.xlsx');
const ws = wb.getWorksheet('Summary');
wb.removeWorksheet(ws.id);
await wb.xlsx.writeFile('c11.xlsx');
```

```
node mut-c11.mjs
```
```
wrote c11.xlsx
```
exit=0

```
node build-error-workbook.mjs --verify c11.xlsx --in findings.json
```
```
verify c11.xlsx: 5 findings, 0 formulas, 1 drift
  missing sheet "Summary"
```
exit=1

Expected: exit 1, "missing sheet". **PASS**

---

## C12 set Read Me "Findings" value cell to 4

`mut-c12.mjs`:
```js
import ExcelJS from 'exceljs';
const wb = new ExcelJS.Workbook();
await wb.xlsx.readFile('findings.xlsx');
const ws = wb.getWorksheet('Read Me');
ws.eachRow((row) => {
  if (row.getCell(1).value === 'Findings') row.getCell(2).value = 4;
});
await wb.xlsx.writeFile('c12.xlsx');
```

```
node mut-c12.mjs
```
```
wrote c12.xlsx
```
exit=0

```
node build-error-workbook.mjs --verify c12.xlsx --in findings.json
```
```
verify c12.xlsx: 5 findings, 15 formulas, 1 drift
  Read Me: Findings 4 expected 5
```
exit=1

Expected: exit 1, names Read Me Findings. **PASS**

---

## C13 data validation present (read c1.xlsx back)

`read-c13.mjs` reads `Findings!AE2`'s `dataValidation`:

```
node read-c13.mjs
```
```
AE2 dataValidation: {"type":"list","formulae":["\"Not Started,In Progress,Ready for Retest,Resolved,Deferred\""],"allowBlank":true,"showErrorMessage":true,"errorTitle":"Remediation status","error":"Choose one of: Not Started, In Progress, Ready for Retest, Resolved, Deferred"}
true
```

Expected: list dataValidation whose formula contains "Not Started" → true. **PASS**
