# PT-18 critic rounds — build-error-workbook.mjs (2026-09-03)

Two critics ran in parallel against the four-commit branch state (`ab93c01`…`a836af6`), read-only, with predictions written before reading. Verdicts below are verbatim (scratchpad paths rewritten to `<repo>/`). Every finding's disposition is in the fold table; the revised script was re-run through the full canary battery plus five new canaries (`canaries-rev2.md`).

## Fold table

| # | Critic | Severity | Finding (short) | Disposition |
|---|---|---|---|---|
| A-M1 | a11y-critic | MAJOR | Summary sheet tallies by SC/status with no boundary line; boundary lived only on Read Me | FIXED — `SUMMARY_BOUNDARY` written to `Summary!A1`; `--verify` checks it (canary C17) |
| A-M2 | a11y-critic | MAJOR | Status dropdown list-only; the "not verification" note sat three sheets from the cell | FIXED — data-validation input message (`STATUS_PROMPT`) on every status cell (canary C20) |
| A-m1 | a11y-critic | MINOR | "outcomes belong to acr-reporting" skips the evaluation-report step | FIXED — SKILL.md now routes via `docs/a11y-evaluation-report-contract.md`, which acr-reporting serializes |
| A-m2 | a11y-critic | MINOR | No workbook title property | FIXED — `wb.title` / `subject` / `description` set (canary C21) |
| A-m3 | a11y-critic | MINOR | Assessment's a11y-choice list omitted frozen panes | FIXED — list now names frozen header + first two columns, file properties, cell-level prompt |
| A-e1 | a11y-critic | ENH | No negative case inside its own domain | FIXED — SKILL.md: do not add a workbook beside an issue tracker (two sources of truth) |
| A-e2 | a11y-critic | ENH | Header "Colour mode" vs key `color_mode` | FIXED — header is "Color mode" |
| A-e3 | a11y-critic | ENH | `finding_id` called a "pass-through"; it is a fixed column | FIXED — "the one column beyond the schema" in script header, SKILL.md, assessment |
| H-M1 | harsh-critic | MAJOR | `verifySummary` matched formula/result pairs by content; swapping two rows passed clean (reproduced) | FIXED — `summaryLayout()` shared by build and verify; every cell checked by position; stray formulas flagged (canaries C14, C15; coordinating session reproduced both swap variants → exit 1) |
| H-m1 | harsh-critic | MINOR | `B7` numFmt literal hit "Source file", not "Source SHA-256" | FIXED — row located by field name from the same rows array the table is built from |
| H-m2 | harsh-critic | MINOR | `verifyErrorsAndReadme` nested five levels | FIXED — split into `errorStringAt` / `scanErrorStrings` / `verifyReadme` / `verifyTable` |
| H-m3 | harsh-critic | MINOR | Two bare `catch {}` blocks discarded the underlying error | FIXED — `catch (err)` with the message surfaced in both |
| H-m4 | harsh-critic | MINOR | Severity case-fold undisclosed | FIXED — `Normalization` row on Read Me; script header, SKILL.md, assessment all state it |
| H-m5 | harsh-critic | MINOR | 11 of 14 Read Me fields unverified | FIXED — 10 of 15 now recomputed from the input; the five unverifiable rows (title, product, timestamp, two file-name rows) are named in the script (`README_UNVERIFIED`) |
| H-e1 | harsh-critic | ENH | `FindingsTable` asserted at build, never checked | FIXED — `verifyTable` checks presence and span (canary C18) |

Refuted by the harsh-critic's own probes and recorded as such: formula/CSV injection on build (exceljs writes `=`-leading strings as shared-string cells, no `<f>` element); Findings column/header swaps (position-based, caught); `sameCell` coercion (no masking case found).

---

## a11y-critic verdict (verbatim)

# PT-18 critic gate — XLSX client-triage workbook (a11y-critic)

Scope: `learnings/wave2-pt18` @ a836af6, worktree `accessibility-skills-pt18`. Read-only, no sub-agents.

## Pre-commitment predictions (written before opening any file)

| # | Prediction | Outcome |
|---|---|---|
| 1 | Subsection is feature description with no negative space ("when this format does NOT serve") | **Partly refuted.** SKILL.md:510 opens with a real routing condition and :519 carries an explicit "What the workbook is **not**". Residual gap is narrower than predicted — see ENH-1. |
| 2 | Severity/outcome orthogonality leaks somewhere in the text | **Refuted in the text, confirmed in the artifact.** Every prose surface is clean (SKILL.md:519; assessment:32; mjs:80-85). The leak is placement: the Summary sheet's per-SC and per-status rollups sit on a sheet with no boundary line — MAJ-1. |
| 3 | `Resolved` is an overclaim vector; a Read Me note is unenforced mitigation | **Confirmed.** MAJ-2 — and now measured: the dropdown carries a list and nothing else. |
| 4 | Workbook a11y set misses ≥1 of: fill legend, magnification widths, document title metadata | **Confirmed (title metadata).** MIN-2. Widths are set per column (mjs:93-127); fill is secondary to text by design (assessment:36). |
| 5 | An overclaim word ("validated"/"verified") without a receipt | **Refuted.** "Validation performed" (assessment:54-68) names node version, an out-of-repo scratch project, a byte-identity SHA, 21/21 canaries with a receipt path that exists, discloses subagent execution *and* which two canaries the coordinating session re-ran itself, and closes with an explicit **Not validated** list that includes "the workbook's behaviour under a screen reader". This is the strongest part of the submission. |
| 6 | Closed column set + `finding_id` pass-through fits the contract, no invented policy | **Confirmed.** `REQUIRED` (mjs:66) = the skill's six required fields (SKILL.md:417); `SEVERITIES` (mjs:67) = the schema enum verbatim, lowercase, matching SKILL.md:448 (checked — no case mismatch); `ID_RE` (mjs:72) = the skill's PREFIX-8hex; `finding_id` is asked for by SKILL.md:525. No finding. |

## Verdict: **ACCEPT**

The claim architecture is sound and the boundary is honest at every prose surface. Both MAJORs are *placement* defects in the generated deliverable, not defects in the claims — the boundary text exists and is correct, it just isn't where the misread happens. Neither blocks promotion; both should land before the first client workbook ships. No CRITICAL findings.

## Findings

### MAJOR

**MAJ-1 — The Summary sheet is the one place a conformance outcome can be derived, and it is the one sheet with no boundary line.**
`SKILL.md:519` describes `Summary` as "live COUNTIF formulas by severity, by SC, and by remediation status", and `Read Me` as the sheet carrying "the claim boundary as text"; `CLAIM_BOUNDARY` (mjs:80-85) and `TRIAGE_NOTE` (mjs:86-89) are Read Me strings. So a per-criterion tally sits one column from a per-status tally, on a sheet whose reader has been given no boundary. "SC 1.4.3 — 6 findings, 6 Resolved" reads as "1.4.3 passes now." That is exactly the derivation `docs/a11y-orthogonality-register.md:11` (conformance outcome ⊥ impact severity) and `:13` (remediation entry ⊥ conformance evidence) exist to forbid, and the register's own mechanism (`:18-20`) is that the boundary must be carried *on the record*, not adjacent to it.
Realist check: worst realistic case is a client pasting the Summary sheet into a status deck as "criteria fixed." Detection is late and invisible to the auditor — it happens inside the client's org. Holds at MAJOR.
**Fix:** write one boundary line onto `Summary` itself — above the SC rollup, "Counts of findings filed. Not criterion outcomes; zero findings for a criterion is not a PASS," and above the status rollup, "Workflow states reported by the receiving team, not verification." Reuse the existing constants; no new claim.
Confidence: HIGH.

**MAJ-2 — `Resolved` is defensible as a client workflow state, but its boundary is three sheets away from the cell where it is chosen.**
Asked directly: keeping `Resolved` is **sound**, and dropping the retest-outcome dropdown was the right call (`assessment:26` — a retest outcome is an evidence-bearing claim and belongs to the auditor). A client tracker needs a terminal state; deny them one and they invent it in `Notes`, unstructured and unverifiable. But from the receiving team's point of view the word is ambiguous between "we fixed it" and "it's confirmed fixed," and the mitigation the assessment leans on ("the `Read Me` says so in plain text", `:26`) is on a sheet the person filling the cell need never open. Measured: the status validation at `mjs:125` carries `list: REMEDIATION_STATES` and nothing else — zero occurrences of `promptTitle`, `prompt:`, or `errorStyle` in the whole file.
**Fix (minimum):** add an ExcelJS data-validation input message to the status column carrying one sentence of `TRIAGE_NOTE` — "A workflow state, not verification: closure is the auditor's, from class-matched retest evidence." It fires on cell focus, so screen-reader and sighted fillers both get it at the point of the click. **Stronger fix, your call:** rename the value to `Fixed — awaiting retest`, which is self-describing and needs no note; it is a naming change, so it is a decision, not a defect.
Confidence: HIGH.

### MINOR

**MIN-1 — SKILL.md:519's routing shorthand skips a step its own page requires.** "criterion-level outcomes belong to `acr-reporting`" can be read as "send the workbook to acr-reporting." `SKILL.md:525` and `assessment:32` are both precise that acr-reporting takes the *evaluation report* — "not this workbook, as input." **Fix:** "…belong to the evaluation report and, from there, to `acr-reporting`." One clause.

**MIN-2 — No workbook document-title property, so Excel's own Accessibility Checker will flag every generated file.** Grep: `properties` 0 occurrences, `creator` 1. A `--title` flag exists (mjs:22) but nothing sets core document properties. A screen-reader user opening the file gets the filename as the document's identity, and the "missing document title" rule (Excel's checker; WCAG 2.4.2 in spirit for documents) fires on output the auditor generated. **Fix:** set the workbook's core title from `--title`/`--product` beside the `creator` value already being written.

**MIN-3 — The documented a11y-choice list omits a choice actually delivered.** `assessment:36` lists named sheets, header row in a defined table, no merged cells (grep `mergeCells`: 0 — confirmed by absence), severity as text with fill secondary, text-formatted IDs. Frozen panes *are* implemented (grep `frozen`: 3) and are the single choice that most helps a magnification user — headers stay on screen at 200-400%. A claim list that under-reports what shipped is a small provenance gap in the direction nobody checks. **Fix:** add frozen panes to the `:36` list.

### ENHANCEMENT

**ENH-1 — The subsection is not linter-writable, but its negative case stops at the domain edge.** It carries refusal semantics, exit codes, the closed-column rationale, and *why* `--verify` excludes triage columns — none of which a linter knows, and the "What the workbook is not" paragraph is real routing. What is missing is the negative case *inside* its own domain: when a spreadsheet-tracking team still shouldn't get one. **Fix:** one sentence at SKILL.md:510 — "If the client's issue tracker is the system of record, don't fork it into a workbook: export once for triage and take fixes back through the tracker." Two live sources of truth is the failure this format invites.

**ENH-2 — Header spelling inconsistency.** `mjs:107` emits `Colour mode` for key `color_mode`; every other header matches its key's spelling. Anyone matching headers by string (a client macro, a re-import) hits it. **Fix:** `Color mode`.

**ENH-3 — "pass-through" undersells what `finding_id` is.** SKILL.md:517, `assessment:19` and `mjs:14-15` call it the single pass-through beyond the schema; `mjs:96` gives it a fixed column in the closed set. It is a documented column, not a pass-through — the current wording faintly suggests some unknown keys survive, which is the opposite of the design. **Fix:** "the one documented column beyond the schema."

## Direct answers to the gate questions

- **Boundary honest and sufficient?** Honest everywhere in prose; sufficient everywhere except the Summary sheet (MAJ-1). Nothing lets a reader derive conformance from severity, treat a short list as conformance (`mjs:83-85` says so explicitly, on the first sheet a client opens), or treat triage status as verification (`mjs:86-89`; `assessment:34`). Routing to acr-reporting is correct against SKILL.md:525 apart from the shorthand at MIN-1.
- **Triage semantics:** sound; keep `Resolved`, move its boundary to the cell (MAJ-2).
- **Workbook a11y choices:** delivered as claimed (merged cells absent, IDs text-typed at mjs:94-99, widths explicit, frozen panes present-but-undocumented). Gaps a real user hits: no document title (MIN-2), and a dropdown with no input message (MAJ-2) — the same fix serves a screen-reader user and a client who mis-reads the word.
- **Closed column set / `finding_id`:** fits the contract, invents no policy (prediction 6). Wording only (ENH-3).
- **Dead output?** No. It tells you when the format serves and when it doesn't; gap is ENH-1.
- **Overclaims:** none found. The `assessment:68` "Not validated" list — including screen-reader behaviour and every renderer — is what keeps `:36`'s "spreadsheet-accessibility basics only" inside its evidence.

## Not checked

- Everything in `build-error-workbook.mjs` past line 140, per instruction: where fill/frozen/wrapText are applied, whether the defined table range includes the triage columns (affects header announcement in Excel for the only cells the client fills), what `--title` is used for, and all `--verify` internals.
- Whether `FORMULA_ERROR_RE` (mjs:74) can false-flag a legitimate finding whose `html_snippet` or `description` contains `#REF!` / `#N/A`.
- Rendered behaviour in Excel / Numbers / LibreOffice / Sheets and under a screen reader — the assessment discloses this same gap at `:68`; I did not close it.
- Contents of `evals/results/error-workbook-2026-09/canaries.md`, `README.md`, `findings.json`, and the maker-survey memo (existence verified only).
- The `.agents/` byte-identical mirror claim (`assessment:3`); the disposition-ledger row; `docs/a11y-evaluation-report-contract.md`; SKILL.md outside the ranges below.
- Any part of the orthogonality register past line 40.

## Provenance

Read: `.claude/skills/bug-reporting/SKILL.md` lines 36-60, 500-535 (plus grep hits at 362, 417, 448, 492, 525); `docs/error-workbook-adoption-assessment.md` (whole, 76 lines); `.claude/skills/bug-reporting/references/build-error-workbook.mjs` lines 1-140; `docs/a11y-orthogonality-register.md` lines 1-40; grep-only additions in `CLAUDE.md:61` and `README.md:26`.
Commands: `git log --oneline -4`; greps for section anchors and `build-error-workbook`; `ls` on the two receipt paths (existence only, contents unread); count-only greps (`grep -c`, no content returned) on the mjs for `frozen`(3), `fill`(6), `promptTitle`(0), `prompt:`(0), `errorStyle`(0), `properties`(0), `creator`(1), `wrapText`(2), `mergeCells`(0), `autoFilter`(0) — used to test claims without reading past line 140.
No files written outside this scratchpad. No sub-agents spawned.

---

## harsh-critic verdict (verbatim)

# Harsh-critic review — build-error-workbook.mjs (PT-18)

Worktree: `<repo>` (branch `learnings/wave2-pt18`, HEAD `a836af6`). Read-only on the repo; probes run only in `<scratchpad>/pt18-scratch`.

## Pre-commitment predictions (before opening any file)

1. `sameCell`'s number/string branch masks a real value change (e.g. `"1"` vs `1`, `"01"` vs `1`).
2. `lastContent`/the Summary `$X$2:$X$n` regex silently ignores a shape it doesn't recognize (rewritten formula, second table).
3. A column or header swap on the Findings sheet is undetectable because verify matches by header text/content, not position.
4. Values starting with `=`/`+`/`-`/`@` get written in a way that risks formula/CSV injection when the workbook is opened in Excel.
5. At 625 lines, something exceeds the 50-line function cap or 4-level nesting cap.

**Outcome: predictions 1, 3 (as stated), and 4 REFUTED by direct trace/empirical test. Prediction 2 refuted for Findings, but investigating it surfaced a real, different, unpredicted gap in `verifySummary` (see CRIT-01) — the swap vulnerability lives on the Summary sheet, not where I expected it (Findings). Prediction 5 REFUTED for function length, CONFIRMED for nesting (one function).**

## Verdict: REVISE

One MAJOR finding: `--verify`'s Summary-sheet check matches formula+cached-result pairs by content membership in a Map, not by row position, so it cannot detect two Summary rows' (formula, result) pairs being swapped — the label stays put, the numbers underneath it don't, and `--verify` reports 0 drift. This is the tool's central promise (cell-by-cell proof that the workbook matches the input) failing on its own sample sheet, on a sheet the canary battery never permutes. Everything else is MINOR/style/refuted-and-worth-recording.

---

## Findings

### MAJOR — Summary sheet: row-swap of (formula, cached-result) pairs is undetectable by `--verify`
`build-error-workbook.mjs:496-527` (`verifySummary`). `expectedResults` is a `Map<formulaText, {label, result, live}>`; the per-row loop looks up `expectedResults.get(v.formula)` and only ever uses `label` (from column A, `row.getCell(1)`) inside drift *messages* — never as part of the match. So if a mutator swaps the `{formula, result}` object between two rows on the Summary sheet (e.g. rows for "critical" and "high"), each row's formula still resolves to a valid, self-consistent entry in `expectedResults` (found by formula text, cached result matches that formula's own recorded result), and `expectedResults.delete()` still empties the map. Net: 0 drift.

**Empirical probe** (`pt18-scratch/mut-swap.mjs`): read `findings.xlsx`, set `Summary!B2.value = <B3's original {formula,result}>` and `Summary!B3.value = <B2's original>` (i.e., swap only the count cells, not the "critical"/"high" labels in column A), write `swap.xlsx`.
```
node build-error-workbook.mjs --verify swap.xlsx --in findings.json
verify swap.xlsx: 5 findings, 15 formulas, 0 drift
exit=0
```
The workbook now shows "critical: 1 / high: 2" instead of the true "critical: 2 / high: 1" (confirmed via a read-back script before the mutation: B2 originally `{formula: COUNTIF(...,"critical"), result:2}`, B3 `{formula: COUNTIF(...,"high"), result:1}`). `--verify` calls this clean.

Root cause, stated plainly: `verifyFindings` (the sibling function) compares *by position* — column index + row number — which is why header/data swaps on the Findings sheet ARE caught (traced, not just asserted — see Prediction 3 below). `verifySummary` compares *by content set-membership*, decoupled from row position, which is why this class of mutation is not.

- Confidence: HIGH (reproduced, not inferred).
- Realist check: worst case is a client-facing Summary sheet silently misreporting severity/SC counts with the tool's own integrity check giving false assurance. Mitigated by: the documented editable surface for the receiving team is the 3 Findings triage columns only (`TRIAGE_NOTE`, `build-error-workbook.mjs:86-89`) — the Summary sheet is not part of the intended edit path, so this doesn't trigger via the documented workflow. That mitigation is why this is MAJOR and not CRITICAL, not why it's dismissible: the exploit is 3 lines of exceljs with no special access, and it directly falsifies the docstring's claim (`build-error-workbook.mjs:34-37`) that verify checks "the cached finding-count results match a recomputation from the input" — it checks that the cached result matches *some* recomputation, not the recomputation for *that row's own label*.
- Fix: make `verifySummary` position-based like `verifyFindings`. Flatten `summaryBlocks(issues)` in the same row order `buildSummary` writes them, walk the Summary sheet rows in lockstep, and compare `(label, formula, result)` at each matched row index — drop the `Map`-by-formula-text lookup. A cheaper patch that keeps the current structure: also assert `label === exp.label` before treating a formula as matched, and don't delete from `expectedResults` on a label mismatch.
- Not exercised by any of the 21 canaries in `evals/results/error-workbook-2026-09/canaries.md` — none of C1-C13 permute or swap Summary rows; all touch a single cell/row/sheet in isolation.

### MINOR — off-by-one hardcoded cell reference: `numFmt='@'` lands on the wrong Read Me row
`build-error-workbook.mjs:326` — `ws.getCell('B7').numFmt = '@';`. `readmeRows()` (line 292) emits, in order, Title/Product/Generated/Generator/Peer dependency/Source file/**Source SHA-256**/Source bytes/…, with the table header consuming row 1, so row 7 is **"Source file"** and row 8 is **"Source SHA-256"**.
- **Empirical confirmation** (`pt18-scratch/probe-readme.mjs`, read-back of `findings.xlsx`'s Read Me sheet): row 7 = `"Source file"` with `numFmt: '@'`; row 8 = `"Source SHA-256"` with `numFmt: undefined`.
- Practical impact is low: both values are non-numeric strings in every realistic case (a `.json` filename, a hex SHA-256 that will contain `a`-`f` in all but an astronomically unlucky hash), so Excel's default General format already renders both as text; `--verify` doesn't check `numFmt` at all. But it's a real bug — whoever wrote the literal miscounted rows — and it's exactly the failure mode the house rule "no hardcoded values — use constants or config" (`~/.claude/rules/common/coding-style.md`) exists to prevent.
- Fix: either correct the literal to `B8`, or better, compute the row from the `readmeRows()` label ("Source SHA-256") instead of a magic address.

### MINOR — nesting depth 5 in `verifyErrorsAndReadme`, exceeding the house 4-level cap
`build-error-workbook.mjs:529-538`. `wb.eachSheet(ws => { ws.eachRow((row,n) => { row.eachCell((cell,c) => { ...; if (FORMULA_ERROR_RE.test(text)) drift.push(...); }); }); });` — function body(1) → eachSheet callback(2) → eachRow callback(3) → eachCell callback(4) → `if` body(5). `~/.claude/rules/common/coding-style.md`: "No deep nesting beyond 4 levels."
- Fix: extract the cell check into a named helper (`function flagFormulaError(cell, sheetName, rowNum, colNum, drift) {...}`) called from the innermost callback, or use `row.eachCell({includeEmpty:false}, (cell,c) => flagFormulaError(...))` to flatten one level.
- Style-only; no behavioral defect. (This is the one place the file breaks the 50-line/4-nesting budget — every function is otherwise under 50 lines, including the 48-line `validateRow`, which is the file's real high-water mark and stays compliant.)

### MINOR — two bare `catch {}` blocks discard the underlying error
`build-error-workbook.mjs:276` (`loadExcel`: `catch { throw new UsageError('exceljs is not installed...') }`) and `:558` (`verify`'s `stat()` check: `catch { throw new UsageError('cannot read --verify ...') }`). Both convert any failure — including ones unrelated to "not installed"/"not found" (a corrupted install, a permissions error) — into a fixed, possibly-misleading message, with the real `err.message`/stack thrown away. Contrast with `loadInput` (`:252-262`), which correctly does `catch (err) { throw new UsageError(\`...: ${err.message}\`) }` in the same file — this is an inconsistency, not a uniform design choice.
- House rule: "Handle errors explicitly — never silently swallow" (`~/.claude/rules/common/coding-style.md`).
- Fix: `catch (err) { throw new UsageError(\`exceljs failed to load: ${err.message}. Run: npm install ${PEER_DEP}\`); }` and similarly for the `stat()` catch.

### MINOR — severity is silently case-normalized; the alteration isn't disclosed
`build-error-workbook.mjs:163` (`serialize`: `if (key === 'severity') return String(v).toLowerCase();`) is shared by both `buildFindings`/`rowValues` (build) and `verifyFindings` (verify) via the same `rowValues()`/`serialize()` call path — **confirmed mirrored identically**, so this is not a build/verify mismatch. But an input row with `"severity":"Critical"` (capital C) — which `validateRow` accepts, since it lowercases before checking against `SEVERITIES` — is written to the workbook as `"critical"`, silently altering the source value. The file's own docstring makes a point of never being silent about dropped data ("a dropped field is visible, never silent," `:12-14`) but doesn't extend that disclosure to altered values. Low stakes (severity is a closed 4-value vocabulary and Excel's `COUNTIF`/`containsText` are case-insensitive, so nothing downstream breaks), but it is a value alteration the Read Me/claim boundary text doesn't mention.
- Fix: either preserve input casing verbatim and drop the `.toLowerCase()` (validation already normalizes for comparison purposes only), or add one line to `CLAIM_BOUNDARY`/`TRIAGE_NOTE` disclosing that severity is case-folded.

### MINOR — 11 of the Read Me sheet's 14 fields are never checked by `--verify`
`build-error-workbook.mjs:539-550` (`verifyErrorsAndReadme`) checks only `Source SHA-256`, `Findings`, and `Generator`. `Title`, `Product`, `Source file`, `Source bytes`, `Stable instance IDs supplied`, `Input keys not serialized`, `Claim boundary`, `Triage columns`, and `Verify` (9 of 14 data rows, plus `Generated (UTC)` which can't be checked because it's a timestamp) can be edited post-build with zero drift reported. `Stable instance IDs supplied` and `Input keys not serialized` are the ones with actual informational content derived from the finding data (not just boilerplate text) — those two are the closest to a real gap; the rest is static disclosure text where tampering is a lower-stakes, differently-shaped problem (integrity of the workbook's *prose*, not its data).
- Confidence: MEDIUM — genuine gap, but low severity because the affected fields are metadata/disclosure text, not finding data, and the doc doesn't claim full Read Me coverage.

### ENHANCEMENT — `TABLE_NAME`/Excel Table object identity is asserted at build, never checked at verify
`build-error-workbook.mjs:77, 339-346` names the Findings sheet's structured Table `FindingsTable` at build time. `verifyFindings`/`verifySummary` never touch `ws.tables` — verification is entirely raw cell/row access. A mutation that strips or renames the Table object (leaving cell values untouched) would not be flagged, even though it changes the workbook's filter/sort/named-range affordances. Not a data-fidelity issue (matches the claim boundary's actual scope), so ENHANCEMENT not MINOR.

---

## Confirmed non-issues (worth recording — these were genuine hunt targets, not skipped)

- **Formula/CSV injection (build side).** Empirical probe (`pt18-scratch/probe-injection.json` → `probe.xlsx`): wrote `rule_id:"=1+1"`, `tool:"+cmd|' /C calc'!A1"`, `summary:"-2+3 ..."`, `description:"@SUM(1,2) ..."`, `suggested_fix:"=HYPERLINK(...)"`. Read back via exceljs: all five cells report `type: 3` (String), values unmodified/un-evaluated. Unzipped the xlsx and inspected the raw sheet XML directly: `<c r="I2" s="1" t="s"><v>66</v></c>` — `t="s"` (shared-string reference), no `<f>` formula element on any of the five cells. Per OOXML (ECMA-376), Excel only executes a cell as a formula if it carries a `<f>` element; a `t="s"`/`t="str"` cell is inert text regardless of its leading character. **Not vulnerable**, and this is a stronger check than "trust the library" — it's file-format-level proof.
  - What I could NOT establish: actual rendering behavior in a real Excel/Numbers/LibreOffice/Google Sheets client (none available in this environment) — matches the adoption doc's own "Not validated: rendering ... no renderer in the toolchain" disclosure, so this isn't a gap the review is inventing.
- **Column/header swap on the Findings sheet.** `verifyFindings` (`:466-494`) checks headers by fixed position (`headers.forEach((h,i) => ...headerRow.getCell(i+1)...)`) and data by fixed `(row, column)` position per issue — traced through several swap scenarios (whole-column swap, header-only rename, data-only swap between two columns); all are caught because position, not content, drives the comparison. This is the mechanism that does NOT have the Summary sheet's flaw — see CRIT/MAJOR finding above for the contrast.
- **`sameCell` number/string coercion (`:461-464`).** Traced every asymmetric case I could construct (`"007"` vs `7`, `frequency.*` numeric vs string source values, empty-cell vs `0`, `-0` vs `0`) — in every case the two branches converge because both ultimately reduce to a `String()` comparison; I found no case where a real value change is masked. Prediction 1 REFUTED.
- **C4/C6/C5 mechanism claims in the adoption doc, checked against the receipt.** C4's "shrunk range" is caught via the formula-text regex, not the cached number (confirmed by reading `verifySummary`'s regex logic and the C4 transcript's 3-line drift output). C6 (relaxation) fills all 3 triage columns (Owner/status/Notes) across all 5 rows and returns 0 drift — confirmed via the mutation script in `canaries.md`, matching the code's exclusion of `TRIAGE_COLUMNS` from `verifyFindings`'s data checks (though triage *headers* are still checked, per `:467`). C5's `#REF!` injection into a triage cell (`AF3`, Notes) is still caught — confirmed the mechanism is `verifyErrorsAndReadme`'s all-sheets, all-cells scan (`wb.eachSheet`), not a triage-aware check, exactly as the task suspected.
- **Rich-text/hyperlink cells, whitespace-only cells.** `cellText()` (`:448-459`) explicitly unwraps `richText` and stringifies `Date`; a hyperlink cell in exceljs is a `{text, hyperlink}` object, which falls into the `'text' in v` branch and returns the display text (hyperlink target itself is not compared, which is a narrow theoretical gap — not tested empirically, traced only). Whitespace-only cells: traced through `sameCell`, no masking (any non-matching string, including all-whitespace, fails the `String()` equality). Not empirically probed for the hyperlink-target case specifically — see Not Checked.

## Not checked

- Real-application rendering (Excel/Numbers/LibreOffice/Google Sheets) — no renderer available in this environment; matches the adoption doc's own disclosed limitation.
- A live second-table-on-one-sheet mutation (reasoned through code path only — `verifyFindings` is row/cell-based, not table-object-aware, so extra rows would likely surface as a row-count drift — not empirically run).
- Hyperlink-target-only tampering (label text unchanged, `cell.hyperlink` changed) — traced `cellText()`'s handling, not empirically probed.
- Performance/scale beyond 5 rows (doc explicitly disclaims this; out of scope here).
- `baseline_test` membership validation against the ICT manifest (explicitly out of scope per the script's own docstring, `:51-52`).
- Whether other consumers of this script (the `bug-reporting` skill itself) handle a non-zero exit code correctly — outside the file under review.

## Provenance

Read in full: `build-error-workbook.mjs` (625 lines), `evals/results/error-workbook-2026-09/README.md`, `evals/results/error-workbook-2026-09/canaries.md` (all 13 canary sections), `docs/error-workbook-adoption-assessment.md` §"Validation performed" (+ "Reopen triggers" for context). House rules from `~/.claude/rules/common/coding-style.md` per the task's supplied contents. Ran 5 empirical probes in `<scratchpad>/pt18-scratch` (formula-injection write+read+raw-XML-unzip, Read Me row read-back, Summary row read-back, the B2/B3 swap mutation+verify). No repo files modified; `findings.xlsx` was read but never overwritten (all probe outputs went to `probe.xlsx`, `swap.xlsx`, and new `.mjs` scripts alongside it).
