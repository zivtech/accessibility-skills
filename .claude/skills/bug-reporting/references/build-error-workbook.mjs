#!/usr/bin/env node

/**
 * build-error-workbook.mjs — serialize bug-reporting findings into an XLSX
 * workbook for client triage, and verify a built workbook against its input.
 *
 * Input contract: the bug-reporting skill's "JSON Schema for Automated Tool
 * Output" (AccessibilityIssue) — a JSON array of issue objects, or an object
 * whose `issues` property is that array. Every row must carry the skill's six
 * required fields (url, wcag_sc, severity, rule_id, xpath, html_snippet). The
 * literal string "N/A" is an honest value; an absent or empty field is a
 * defect and the build refuses (exit 2). Keys outside the schema are not
 * serialized — they are counted and listed on the Read Me sheet so a dropped
 * field is visible, never silent. `finding_id` (the evidence-finding
 * contract's identifier) is the one column beyond the schema. Two values are
 * normalized and nothing else is altered: `severity` is lower-cased and a
 * `wcag_sc` of "n/a" is written as "N/A"; the Read Me discloses this.
 *
 * Peer dependency — install in YOUR project, never in this repository:
 *   npm install exceljs@4.4.0        (MIT; exact-pin it)
 *
 * Usage:
 *   node build-error-workbook.mjs --in findings.json --out findings.xlsx
 *       [--title "Accessibility findings"] [--product "Name the client uses"]
 *   node build-error-workbook.mjs --verify findings.xlsx --in findings.json [--json]
 *
 * Sheets:
 *   Read Me   — provenance (source file, SHA-256, size, row count, generator,
 *               ignored keys) and the claim boundary, as text.
 *   Findings  — one row per issue, schema fields in a fixed column order,
 *               as a defined table with a header row; then three owner-fillable
 *               triage columns (Owner, Remediation status, Notes).
 *   Summary   — live COUNTIF formulas over the Findings rows (by severity,
 *               by WCAG SC, by remediation status), each with a cached result,
 *               under a boundary line saying these are counts of findings,
 *               not conformance outcomes.
 *
 * --verify reads the workbook back and checks, cell by cell, that the finding
 * columns equal the input's serialization; that the Findings defined table is
 * present and spans exactly the data rows; that every Summary cell sits at its
 * expected position with the expected label and formula and, for finding
 * counts, the expected cached result; that no cell on any sheet holds an Excel
 * error string; and that every Read Me field derivable from the input (all but
 * title, product, timestamp, and file-name rows) matches it, SHA-256 included.
 * Triage columns are excluded by design — they belong to the receiving team —
 * so --verify still proves the finding data after a client has filled them in.
 *
 * Exit codes:
 *   0  build wrote the workbook, or --verify found no drift
 *   1  --verify found drift (listed)
 *   2  refusal or usage error — invalid input rows, duplicate instance_id,
 *      a cell over Excel's 32,767-character limit, missing files, bad flags
 *
 * What this is NOT: not a conformance report (route ACR/VPAT work to
 * acr-reporting), not a retest ledger (a "Resolved" status here is the
 * receiving team's workflow state, not verification evidence), and not a
 * validator of baseline_test IDs against the ICT baseline manifest — the
 * pattern is checked, membership is not.
 */

import { createHash } from 'node:crypto';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import { createRequire } from 'node:module';

const SCHEMA_VERSION = '1.0';
const GENERATOR = `build-error-workbook.mjs schema ${SCHEMA_VERSION}`;
const PEER_DEP = 'exceljs@4.4.0';
const CELL_MAX = 32767;
const NA = 'N/A';
const REQUIRED = ['url', 'wcag_sc', 'severity', 'rule_id', 'xpath', 'html_snippet'];
const SEVERITIES = ['critical', 'high', 'medium', 'low'];
const WCAG_LEVELS = ['A', 'AA', 'AAA'];
const SCREEN_TYPES = ['desktop', 'mobile'];
const COLOR_MODES = ['light', 'dark'];
const WCAG_SC_RE = /^\d\.\d+\.\d+$/;
const ID_RE = /^[A-Z0-9]+-[0-9a-f]{8}$/;
const BASELINE_RE = /^\d{1,2}\.[A-Z]-[A-Za-z]+$/;
const FORMULA_ERROR_RE = /#(?:REF!|DIV\/0!|VALUE!|NAME\?|NUM!|NULL!|N\/A)/;
const REMEDIATION_STATES = ['Not Started', 'In Progress', 'Ready for Retest', 'Resolved', 'Deferred'];
const SHEETS = { readme: 'Read Me', findings: 'Findings', summary: 'Summary' };
const TABLE_NAME = 'FindingsTable';
const MAX_LISTED = 50;

const CLAIM_BOUNDARY =
  'Each row is one filed finding. Severity is impact on the people affected, ' +
  'not a WCAG conformance outcome: this workbook asserts no criterion-level ' +
  'PASS or FAIL and is not an Accessibility Conformance Report. A clean or ' +
  'short list is not evidence of conformance — it is the set of findings ' +
  'filed from the testing that was done.';
const TRIAGE_NOTE =
  'Owner, Remediation status, and Notes are blank for the receiving team. ' +
  'Remediation status is a workflow state. It is not verification: a fix is ' +
  'closed by the auditor from class-matched retest evidence, not by this cell.';
const STATUS_PROMPT =
  "Your team's workflow state. Not verification: a fix is closed by the " +
  'auditor from class-matched retest evidence, not by this cell.';
const SUMMARY_BOUNDARY =
  'Counts of filed findings. Severity is impact on people, not a conformance ' +
  'outcome, and a count by success criterion is not a criterion result.';
const NORMALIZATION_NOTE =
  'severity lower-cased; a wcag_sc of "n/a" written as "N/A"; nothing else altered.';
const SUMMARY_FIRST_ROW = 3;
const README_UNVERIFIED = new Set(['Title', 'Product', 'Generated (UTC)', 'Source file', 'Verify']);

// Column order is part of the contract: --verify compares by position.
const COLUMNS = [
  { key: '#', header: '#', width: 6 },
  { key: 'instance_id', header: 'Instance ID', width: 16, text: true },
  { key: 'pattern_id', header: 'Pattern ID', width: 16, text: true },
  { key: 'finding_id', header: 'Finding ID', width: 24, text: true },
  { key: 'summary', header: 'Summary', width: 40 },
  { key: 'severity', header: 'Severity', width: 11 },
  { key: 'wcag_sc', header: 'WCAG SC', width: 10, text: true },
  { key: 'wcag_level', header: 'Level', width: 7 },
  { key: 'rule_id', header: 'Rule ID', width: 22 },
  { key: 'act_rule_id', header: 'ACT rule', width: 12 },
  { key: 'baseline_test', header: 'Baseline test (508)', width: 18 },
  { key: 'tool', header: 'Tool', width: 14 },
  { key: 'url', header: 'URL', width: 40 },
  { key: 'screen_type', header: 'Screen', width: 9 },
  { key: 'color_mode', header: 'Color mode', width: 11 },
  { key: 'xpath', header: 'XPath (simplified)', width: 36 },
  { key: 'xpath_full', header: 'XPath (full)', width: 36 },
  { key: 'html_snippet', header: 'HTML snippet', width: 48 },
  { key: 'frequency.instances_on_page', header: 'Instances on page', width: 10 },
  { key: 'frequency.pages_affected', header: 'Pages affected', width: 10 },
  { key: 'frequency.total_pages_scanned', header: 'Pages scanned', width: 10 },
  { key: 'description', header: 'Description', width: 48 },
  { key: 'impact', header: 'Impact', width: 36 },
  { key: 'steps_to_reproduce', header: 'Steps to reproduce', width: 44 },
  { key: 'suggested_fix', header: 'Suggested fix', width: 44 },
  { key: 'environment.browser', header: 'Browser', width: 16 },
  { key: 'environment.os', header: 'OS', width: 14 },
  { key: 'environment.screen_reader', header: 'Screen reader', width: 16 },
  { key: 'environment.zoom_level', header: 'Zoom', width: 8 },
];
const TRIAGE_COLUMNS = [
  { key: 'triage.owner', header: 'Owner', width: 16 },
  { key: 'triage.status', header: 'Remediation status', width: 18, list: REMEDIATION_STATES },
  { key: 'triage.notes', header: 'Notes', width: 40 },
];
const KNOWN_KEYS = new Set([
  ...COLUMNS.map((c) => c.key.split('.')[0]).filter((k) => k !== '#'),
]);

// ---------------------------------------------------------------- helpers

function columnLetter(index1) {
  let n = index1;
  let out = '';
  while (n > 0) {
    const r = (n - 1) % 26;
    out = String.fromCharCode(65 + r) + out;
    n = Math.floor((n - 1) / 26);
  }
  return out;
}

function columnIndex(key) {
  const i = COLUMNS.findIndex((c) => c.key === key);
  if (i < 0) throw new Error(`no column ${key}`);
  return i + 1;
}

function getPath(obj, dotted) {
  return dotted.split('.').reduce((acc, k) => (acc == null ? undefined : acc[k]), obj);
}

function serialize(issue, rowNumber, key) {
  if (key === '#') return rowNumber;
  const v = getPath(issue, key);
  if (v === undefined || v === null) return '';
  if (key === 'impact') return Array.isArray(v) ? v.map(String).join('; ') : String(v);
  if (key === 'steps_to_reproduce') {
    return Array.isArray(v) ? v.map((s, i) => `${i + 1}. ${s}`).join('\n') : String(v);
  }
  if (key === 'severity') return String(v).toLowerCase();
  if (key === 'wcag_sc') return String(v).toUpperCase() === NA ? NA : String(v);
  if (key.startsWith('frequency.')) return typeof v === 'number' ? v : String(v);
  return typeof v === 'object' ? JSON.stringify(v) : String(v);
}

function rowValues(issue, rowNumber) {
  return COLUMNS.map((c) => serialize(issue, rowNumber, c.key));
}

function sha256(buffer) {
  return createHash('sha256').update(buffer).digest('hex');
}

function isPlainObject(v) {
  return v !== null && typeof v === 'object' && !Array.isArray(v);
}

function isFilled(v) {
  return typeof v === 'string' ? v.trim().length > 0 : v !== undefined && v !== null;
}

// ------------------------------------------------------------- validation

function validateRow(issue, i, seenIds, errors) {
  const where = `row ${i + 1}`;
  if (!isPlainObject(issue)) {
    errors.push(`${where}: not an object`);
    return;
  }
  for (const f of REQUIRED) {
    if (!isFilled(issue[f])) errors.push(`${where}: missing required field ${f}`);
  }
  const sev = typeof issue.severity === 'string' ? issue.severity.toLowerCase() : '';
  if (isFilled(issue.severity) && !SEVERITIES.includes(sev)) {
    errors.push(`${where}: severity "${issue.severity}" not in ${SEVERITIES.join('/')}`);
  }
  const sc = String(issue.wcag_sc ?? '');
  if (isFilled(issue.wcag_sc) && !WCAG_SC_RE.test(sc) && sc.toUpperCase() !== NA) {
    errors.push(`${where}: wcag_sc "${sc}" is not x.y.z or ${NA}`);
  }
  if (isFilled(issue.wcag_level) && !WCAG_LEVELS.includes(issue.wcag_level)) {
    errors.push(`${where}: wcag_level "${issue.wcag_level}" not in ${WCAG_LEVELS.join('/')}`);
  }
  if (isFilled(issue.screen_type) && !SCREEN_TYPES.includes(issue.screen_type)) {
    errors.push(`${where}: screen_type "${issue.screen_type}" not in ${SCREEN_TYPES.join('/')}`);
  }
  if (isFilled(issue.color_mode) && !COLOR_MODES.includes(issue.color_mode)) {
    errors.push(`${where}: color_mode "${issue.color_mode}" not in ${COLOR_MODES.join('/')}`);
  }
  for (const idKey of ['instance_id', 'pattern_id']) {
    if (isFilled(issue[idKey]) && !ID_RE.test(String(issue[idKey]))) {
      errors.push(`${where}: ${idKey} "${issue[idKey]}" is not PREFIX-8hex`);
    }
  }
  if (isFilled(issue.instance_id)) {
    if (seenIds.has(issue.instance_id)) {
      errors.push(`${where}: duplicate instance_id ${issue.instance_id} (first seen row ${seenIds.get(issue.instance_id)})`);
    } else {
      seenIds.set(issue.instance_id, i + 1);
    }
  }
  if (isFilled(issue.baseline_test) && !BASELINE_RE.test(String(issue.baseline_test))) {
    errors.push(`${where}: baseline_test "${issue.baseline_test}" does not match the web-test ID pattern`);
  }
  for (const c of COLUMNS) {
    const v = serialize(issue, i + 1, c.key);
    if (typeof v === 'string' && v.length > CELL_MAX) {
      errors.push(`${where}: ${c.key} is ${v.length} characters; Excel cells hold ${CELL_MAX}`);
    }
  }
}

function validateIssues(issues) {
  const errors = [];
  const seenIds = new Map();
  const ignored = new Map();
  issues.forEach((issue, i) => {
    validateRow(issue, i, seenIds, errors);
    if (!isPlainObject(issue)) return;
    for (const k of Object.keys(issue)) {
      if (!KNOWN_KEYS.has(k)) ignored.set(k, (ignored.get(k) ?? 0) + 1);
    }
  });
  return { errors, ignored, stableIds: seenIds.size };
}

async function loadInput(inPath) {
  let buffer;
  try {
    buffer = await readFile(inPath);
  } catch (err) {
    throw new UsageError(`cannot read --in ${inPath}: ${err.message}`);
  }
  let parsed;
  try {
    parsed = JSON.parse(buffer.toString('utf8'));
  } catch (err) {
    throw new UsageError(`--in ${inPath} is not JSON: ${err.message}`);
  }
  const issues = Array.isArray(parsed) ? parsed : parsed?.issues;
  if (!Array.isArray(issues)) {
    throw new UsageError(`--in ${inPath}: expected a JSON array or an object with an "issues" array`);
  }
  if (issues.length === 0) throw new UsageError(`--in ${inPath}: zero issues; nothing to serialize`);
  return { issues, sha: sha256(buffer), bytes: buffer.length, name: path.basename(inPath) };
}

// ------------------------------------------------------------------ build

function loadExcel() {
  try {
    return createRequire(import.meta.url)('exceljs');
  } catch (err) {
    throw new UsageError(`exceljs could not be loaded (${err.message}). Install it in this project: npm install ${PEER_DEP}`);
  }
}

function findingsRange(colKey, lastRow) {
  const L = columnLetter(columnIndex(colKey));
  return `${SHEETS.findings}!$${L}$2:$${L}$${lastRow}`;
}

function triageRange(colKey, lastRow) {
  const i = COLUMNS.length + TRIAGE_COLUMNS.findIndex((c) => c.key === colKey) + 1;
  const L = columnLetter(i);
  return `${SHEETS.findings}!$${L}$2:$${L}$${lastRow}`;
}

function readmeRows(input, opts, counts) {
  const ignored = [...counts.ignored.entries()].map(([k, n]) => `${k} (${n})`).join(', ') || 'none';
  return [
    ['Title', opts.title],
    ['Product', opts.product || '(not supplied)'],
    ['Generated (UTC)', new Date().toISOString()],
    ['Generator', GENERATOR],
    ['Peer dependency', PEER_DEP],
    ['Source file', input.name],
    ['Source SHA-256', input.sha],
    ['Source bytes', input.bytes],
    ['Findings', input.issues.length],
    ['Stable instance IDs supplied', `${counts.stableIds} of ${input.issues.length}`],
    ['Input keys not serialized', ignored],
    ['Normalization', NORMALIZATION_NOTE],
    ['Claim boundary', CLAIM_BOUNDARY],
    ['Triage columns', TRIAGE_NOTE],
    ['Verify', `node build-error-workbook.mjs --verify <this file> --in ${input.name}`],
  ];
}

function buildReadme(wb, input, opts, counts) {
  const ws = wb.addWorksheet(SHEETS.readme);
  ws.columns = [{ width: 30 }, { width: 100 }];
  const rows = readmeRows(input, opts, counts);
  ws.addTable({
    name: 'ReadMeTable',
    ref: 'A1',
    headerRow: true,
    style: { theme: 'TableStyleLight1', showRowStripes: false },
    columns: [{ name: 'Field' }, { name: 'Value' }],
    rows,
  });
  ws.eachRow((row) => {
    row.alignment = { wrapText: true, vertical: 'top' };
  });
  const shaRow = rows.findIndex(([field]) => field === 'Source SHA-256') + 2;
  ws.getCell(`B${shaRow}`).numFmt = '@';
  ws.views = [{ state: 'frozen', ySplit: 1 }];
}

function severityFill(argb) {
  return { fill: { type: 'pattern', pattern: 'solid', bgColor: { argb } } };
}

function buildFindings(wb, issues) {
  const ws = wb.addWorksheet(SHEETS.findings);
  const all = [...COLUMNS, ...TRIAGE_COLUMNS];
  ws.columns = all.map((c) => ({ width: c.width }));
  const rows = issues.map((issue, i) => [...rowValues(issue, i + 1), '', '', '']);
  ws.addTable({
    name: TABLE_NAME,
    ref: 'A1',
    headerRow: true,
    style: { theme: 'TableStyleMedium2', showRowStripes: true },
    columns: all.map((c) => ({ name: c.header, filterButton: true })),
    rows,
  });
  const lastRow = issues.length + 1;
  ws.eachRow((row, n) => {
    row.alignment = { wrapText: true, vertical: 'top' };
    if (n === 1) row.font = { bold: true };
  });
  COLUMNS.forEach((c, i) => {
    if (!c.text) return;
    const L = columnLetter(i + 1);
    for (let r = 2; r <= lastRow; r += 1) ws.getCell(`${L}${r}`).numFmt = '@';
  });
  const statusL = columnLetter(COLUMNS.length + 2);
  for (let r = 2; r <= lastRow; r += 1) {
    ws.getCell(`${statusL}${r}`).dataValidation = {
      type: 'list',
      allowBlank: true,
      formulae: [`"${REMEDIATION_STATES.join(',')}"`],
      showInputMessage: true,
      promptTitle: 'Remediation status',
      prompt: STATUS_PROMPT,
      showErrorMessage: true,
      errorTitle: 'Remediation status',
      error: `Choose one of: ${REMEDIATION_STATES.join(', ')}`,
    };
  }
  const sevL = columnLetter(columnIndex('severity'));
  const fills = { critical: 'FFF4CCCC', high: 'FFFCE8E6', medium: 'FFFFF2CC', low: 'FFE7E6E6' };
  ws.addConditionalFormatting({
    ref: `${sevL}2:${sevL}${lastRow}`,
    rules: SEVERITIES.map((s, i) => ({
      type: 'containsText', operator: 'containsText', text: s, priority: i + 1, style: severityFill(fills[s]),
    })),
  });
  ws.views = [{ state: 'frozen', xSplit: 2, ySplit: 1 }];
}

function summaryBlocks(issues) {
  const lastRow = issues.length + 1;
  const scs = [...new Set(issues.map((x) => serialize(x, 0, 'wcag_sc')))]
    .sort((a, b) => (a === NA) - (b === NA) || a.localeCompare(b, undefined, { numeric: true }));
  const count = (key, val) => issues.filter((x) => serialize(x, 0, key) === val).length;
  return [
    {
      title: 'By severity',
      rows: [
        ...SEVERITIES.map((s) => [s, `COUNTIF(${findingsRange('severity', lastRow)},"${s}")`, count('severity', s)]),
        ['Total findings', `ROWS(${findingsRange('#', lastRow)})`, issues.length],
      ],
    },
    {
      title: 'By WCAG success criterion',
      rows: scs.map((sc) => [sc, `COUNTIF(${findingsRange('wcag_sc', lastRow)},"${sc}")`, count('wcag_sc', sc)]),
    },
    {
      title: 'By remediation status (live; blank until the receiving team fills it)',
      live: true,
      rows: [
        ...REMEDIATION_STATES.map((s) => [s, `COUNTIF(${triageRange('triage.status', lastRow)},"${s}")`, 0]),
        ['Blank', `COUNTBLANK(${triageRange('triage.status', lastRow)})`, issues.length],
      ],
    },
  ];
}

// Row-by-row layout of the Summary sheet. Build writes it; verify reads it
// back by position, so a swapped or moved cell is drift even when the
// formula/result pair still exists somewhere on the sheet.
function summaryLayout(issues) {
  const cells = [];
  let row = SUMMARY_FIRST_ROW;
  for (const block of summaryBlocks(issues)) {
    cells.push({ row, kind: 'title', label: block.title });
    row += 1;
    for (const [label, formula, result] of block.rows) {
      cells.push({ row, kind: 'formula', label, formula, result, live: Boolean(block.live) });
      row += 1;
    }
    row += 1;
  }
  return cells;
}

function buildSummary(wb, issues) {
  const ws = wb.addWorksheet(SHEETS.summary);
  ws.columns = [{ width: 44 }, { width: 12 }];
  ws.getCell('A1').value = SUMMARY_BOUNDARY;
  ws.getCell('A1').alignment = { wrapText: true, vertical: 'top' };
  ws.getRow(1).height = 45;
  for (const cell of summaryLayout(issues)) {
    const a = ws.getCell(`A${cell.row}`);
    const b = ws.getCell(`B${cell.row}`);
    a.value = cell.label;
    if (cell.kind === 'title') {
      a.font = { bold: true };
      b.value = 'Count';
      b.font = { bold: true };
    } else {
      a.numFmt = '@';
      b.value = { formula: cell.formula, result: cell.result };
    }
  }
  ws.views = [{ state: 'frozen', ySplit: 1 }];
}

async function build(args) {
  const input = await loadInput(args.in);
  const counts = validateIssues(input.issues);
  if (counts.errors.length) {
    throw new UsageError(`refusing to build: ${counts.errors.length} invalid row(s)\n  ${counts.errors.slice(0, MAX_LISTED).join('\n  ')}`);
  }
  const ExcelJS = loadExcel();
  const wb = new ExcelJS.Workbook();
  wb.creator = GENERATOR;
  wb.created = new Date();
  wb.title = args.product ? `${args.title} — ${args.product}` : args.title;
  wb.subject = 'Accessibility findings for triage';
  wb.description = CLAIM_BOUNDARY;
  buildReadme(wb, input, args, counts);
  buildFindings(wb, input.issues);
  buildSummary(wb, input.issues);
  await wb.xlsx.writeFile(args.out);
  const ignored = counts.ignored.size ? ` — ignored keys: ${[...counts.ignored.keys()].join(', ')}` : '';
  console.log(`wrote ${args.out}: ${input.issues.length} findings, ${counts.stableIds} with instance_id${ignored}`);
}

// ----------------------------------------------------------------- verify

function cellText(cell) {
  const v = cell.value;
  if (v === null || v === undefined) return '';
  if (typeof v === 'object') {
    if ('formula' in v) return v;
    if ('richText' in v) return v.richText.map((t) => t.text).join('');
    if ('text' in v) return String(v.text);
    if (v instanceof Date) return v.toISOString();
    return String(v);
  }
  return v;
}

function sameCell(expected, actual) {
  if (typeof expected === 'number') return actual === expected || String(actual) === String(expected);
  return String(actual ?? '') === String(expected);
}

function verifyFindings(ws, issues, drift) {
  const headers = [...COLUMNS, ...TRIAGE_COLUMNS].map((c) => c.header);
  const headerRow = ws.getRow(1);
  headers.forEach((h, i) => {
    const got = cellText(headerRow.getCell(i + 1));
    if (got !== h) drift.push(`Findings!${columnLetter(i + 1)}1: header "${got}" expected "${h}"`);
  });
  const expectedLast = issues.length + 1;
  let lastContent = 1;
  ws.eachRow((row, n) => {
    for (let i = 1; i <= COLUMNS.length; i += 1) {
      if (String(cellText(row.getCell(i)) ?? '') !== '') lastContent = Math.max(lastContent, n);
    }
  });
  if (lastContent !== expectedLast) {
    drift.push(`Findings: ${lastContent - 1} data row(s) present, input has ${issues.length}`);
  }
  issues.forEach((issue, i) => {
    const r = i + 2;
    const expected = rowValues(issue, i + 1);
    const row = ws.getRow(r);
    expected.forEach((exp, c) => {
      const got = cellText(row.getCell(c + 1));
      if (!sameCell(exp, got)) {
        drift.push(`Findings!${columnLetter(c + 1)}${r} (${COLUMNS[c].key}): "${String(got).slice(0, 60)}" expected "${String(exp).slice(0, 60)}"`);
      }
    });
  });
}

function describeFormulaDrift(got, cell, expectedLast) {
  const ends = [...got.matchAll(/\$([A-Z]+)\$2:\$\1\$(\d+)/g)].map((m) => Number(m[2]));
  const wrongEnd = ends.find((end) => end !== expectedLast);
  if (wrongEnd !== undefined) return `range ends at row ${wrongEnd}, data ends at row ${expectedLast}`;
  return `formula "${got}" expected "${cell.formula}"`;
}

function verifySummaryCell(ws, cell, expectedLast, drift) {
  const where = `Summary!B${cell.row} ("${cell.label}")`;
  const label = cellText(ws.getCell(`A${cell.row}`));
  if (String(label) !== cell.label) drift.push(`Summary!A${cell.row}: "${label}" expected "${cell.label}"`);
  const v = ws.getCell(`B${cell.row}`).value;
  if (cell.kind === 'title') {
    if (String(cellText(ws.getCell(`B${cell.row}`))) !== 'Count') drift.push(`${where}: expected the "Count" header`);
    return 0;
  }
  if (!v || typeof v !== 'object' || !('formula' in v)) {
    drift.push(`${where}: expected a formula, found "${String(cellText(ws.getCell(`B${cell.row}`))).slice(0, 40)}"`);
    return 0;
  }
  if (v.formula !== cell.formula) drift.push(`${where}: ${describeFormulaDrift(v.formula, cell, expectedLast)}`);
  else if (!cell.live && Number(v.result) !== cell.result) drift.push(`${where}: cached result ${v.result}, recomputed ${cell.result}`);
  return 1;
}

function verifySummary(ws, issues, drift) {
  if (String(cellText(ws.getCell('A1'))) !== SUMMARY_BOUNDARY) drift.push('Summary!A1: boundary line missing or altered');
  const layout = summaryLayout(issues);
  const expectedLast = issues.length + 1;
  let formulas = 0;
  for (const cell of layout) formulas += verifySummaryCell(ws, cell, expectedLast, drift);
  const expectedRows = new Set(layout.map((c) => c.row));
  ws.eachRow((row, n) => {
    const v = row.getCell(2).value;
    if (v && typeof v === 'object' && 'formula' in v && !expectedRows.has(n)) {
      drift.push(`Summary!B${n}: unexpected formula ${v.formula}`);
    }
  });
  return formulas;
}

function errorStringAt(ws, row, n, drift) {
  row.eachCell((cell, c) => {
    const v = cellText(cell);
    const text = typeof v === 'object' ? String(v.result ?? '') : String(v);
    if (FORMULA_ERROR_RE.test(text)) drift.push(`${ws.name}!${columnLetter(c)}${n}: Excel error value "${text}"`);
  });
}

function scanErrorStrings(wb, drift) {
  wb.eachSheet((ws) => ws.eachRow((row, n) => errorStringAt(ws, row, n, drift)));
}

function verifyTable(ws, issues, drift) {
  let table;
  try {
    table = ws.getTable(TABLE_NAME);
  } catch (err) {
    drift.push(`Findings: defined table "${TABLE_NAME}" could not be read (${err.message})`);
    return;
  }
  const ref = table?.table?.tableRef;
  if (!ref) {
    drift.push(`Findings: defined table "${TABLE_NAME}" is missing`);
    return;
  }
  const expectedRef = `A1:${columnLetter(COLUMNS.length + TRIAGE_COLUMNS.length)}${issues.length + 1}`;
  if (ref !== expectedRef) drift.push(`Findings: table "${TABLE_NAME}" spans ${ref}, expected ${expectedRef}`);
}

function verifyReadme(ws, input, counts, drift) {
  const expected = readmeRows(input, { title: '', product: '' }, counts);
  expected.forEach(([field, value], i) => {
    const r = i + 2;
    const gotField = String(cellText(ws.getCell(`A${r}`)));
    if (gotField !== field) {
      drift.push(`Read Me!A${r}: "${gotField}" expected "${field}"`);
      return;
    }
    if (README_UNVERIFIED.has(field)) return;
    const got = String(cellText(ws.getCell(`B${r}`)));
    if (got !== String(value)) drift.push(`Read Me: ${field} "${got.slice(0, 60)}" expected "${String(value).slice(0, 60)}"`);
  });
}

async function verify(args) {
  const input = await loadInput(args.in);
  const counts = validateIssues(input.issues);
  if (counts.errors.length) {
    throw new UsageError(`refusing to verify against invalid input: ${counts.errors.length} invalid row(s)\n  ${counts.errors.slice(0, MAX_LISTED).join('\n  ')}`);
  }
  const ExcelJS = loadExcel();
  try {
    await stat(args.verify);
  } catch (err) {
    throw new UsageError(`cannot read --verify ${args.verify}: ${err.message}`);
  }
  const wb = new ExcelJS.Workbook();
  await wb.xlsx.readFile(args.verify);
  const drift = [];
  for (const name of Object.values(SHEETS)) {
    if (!wb.getWorksheet(name)) drift.push(`missing sheet "${name}"`);
  }
  let formulas = 0;
  if (drift.length === 0) {
    verifyFindings(wb.getWorksheet(SHEETS.findings), input.issues, drift);
    verifyTable(wb.getWorksheet(SHEETS.findings), input.issues, drift);
    formulas = verifySummary(wb.getWorksheet(SHEETS.summary), input.issues, drift);
    scanErrorStrings(wb, drift);
    verifyReadme(wb.getWorksheet(SHEETS.readme), input, counts, drift);
  }
  const report = { file: args.verify, input: input.name, findings: input.issues.length, formulas, drift };
  if (args.json) {
    console.log(JSON.stringify(report, null, 2));
  } else {
    console.log(`verify ${args.verify}: ${input.issues.length} findings, ${formulas} formulas, ${drift.length} drift`);
    for (const line of drift.slice(0, MAX_LISTED)) console.log(`  ${line}`);
    if (drift.length > MAX_LISTED) console.log(`  … ${drift.length - MAX_LISTED} more`);
  }
  return drift.length === 0 ? 0 : 1;
}

// -------------------------------------------------------------------- cli

class UsageError extends Error {}

function parseArgs(argv) {
  const args = { title: 'Accessibility findings', product: '', json: false };
  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    const next = () => {
      if (i + 1 >= argv.length) throw new UsageError(`${a} needs a value`);
      i += 1;
      return argv[i];
    };
    if (a === '--in') args.in = next();
    else if (a === '--out') args.out = next();
    else if (a === '--verify') args.verify = next();
    else if (a === '--title') args.title = next();
    else if (a === '--product') args.product = next();
    else if (a === '--json') args.json = true;
    else throw new UsageError(`unrecognized argument ${a}`);
  }
  if (!args.in) throw new UsageError('--in <findings.json> is required');
  if (!args.verify && !args.out) throw new UsageError('either --out <file.xlsx> or --verify <file.xlsx> is required');
  if (args.verify && args.out) throw new UsageError('--out and --verify are exclusive');
  if (args.out && !args.out.toLowerCase().endsWith('.xlsx')) throw new UsageError('--out must end in .xlsx');
  return args;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.verify) return verify(args);
  await build(args);
  return 0;
}

main().then(
  (code) => process.exit(code),
  (err) => {
    console.error(err instanceof UsageError ? err.message : err.stack ?? String(err));
    process.exit(2);
  },
);
