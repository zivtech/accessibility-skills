# a11y-critic rounds on WP-D (2026-09-02)

Gate for the `--resume` + `coverage` fold-in to the a11y-test reference script
`baseline-url-scan.mjs` (PT-03). Reviewer: `a11y-critic` agent at sonnet
(reference-script change, no skill text), read-only, same agent across rounds,
with live re-runs of canaries 4 and 6 in a scratch project. Verbatim, recovered
from the agent transcript. Canary receipts: `docs/baseline-url-scan-adoption-assessment.md`.


---

## Round 1

# WP-D (PT-03) Gate Review — `--resume` + `coverage` in `baseline-url-scan.mjs`

**Predictions (before reading code):** (1) resume compares a subset not exact set of viewports; (2) alt_snapshot only checked on the wrong viewport; (3) `axe_core_version` resolved from the wrong install location, failing unsafe; (4) `aborted` leaks into a rate somewhere; (5) `skipped_resumed` unit mismatches `measured`/`aborted`; (6) persisted `resumed:true` is unprovenanced. Confirmed: #3 (safe direction, but undiagnosed), #6 (mitigated). Not found as predicted: #1, #2, #4 — guards are correct. New, unpredicted: `coverage.measured` conflates fresh and resumed data (below), and the receipt's own canaries don't actually exercise the unit change they claim to prove.

## Findings (ranked)

**MAJOR — Receipt doesn't prove the `skipped_resumed` unit change it documents.** `docs/baseline-url-scan-adoption-assessment.md` §"2026-09-02" canary 1's shown command uses a single viewport (`--viewports 1280x800`); canaries 2 and 5 report `skipped_resumed: 0`. None distinguish URL-count from viewport-scan-count — the exact mutation the team lead flagged as changed post-build. I live-verified the code is correct (2 URLs × 2 viewports, both resumed → `skipped_resumed: 4`, not 2 — see below), but the shipped receipt doesn't demonstrate it, and its canary-4 quote (`{"measured":1,"aborted":{"count":1,"by_reason":{"navigation":1}}}`) omits `unit` and `skipped_resumed`, which the current script always emits. Fix: replace the canary-4 quote with current output and add a multi-viewport resume assertion to canary 1 or a new canary.

**MAJOR — `coverage.measured`/`totals.measured` (`baseline-url-scan.mjs:231-235, 292-301`) don't distinguish fresh-this-run from resumed data.** Live proof: rerunning with `--resume` against 2 fully-cacheable URLs × 2 viewports (zero fresh scans) reports `coverage: {measured:4, skipped_resumed:4}` — identical `measured` count to what a fully-fresh run would show. A consumer reading `coverage.measured` alone (or `totals.measured`) cannot tell "gathered now" from "carried forward N runs ago" without also reading and subtracting `skipped_resumed`. This is exactly item 7's concern: resumed data is legible as measured coverage without an explicit warning. Doesn't violate the SKILL.md:59 denominator rule (resumed data is valid, not aborted) but the module docstring (lines 40-52) never states the overlap. Fix: one doc line, e.g. "`coverage.measured` includes resumed viewport-scans; subtract `skipped_resumed` for freshly-gathered-this-run count."

**MINOR — Version-provenance comment overclaims (`baseline-url-scan.mjs:119-122`).** `resolveAxeCoreVersion()` resolves `axe-core/package.json` via `createRequire(import.meta.url)` from the script's own location, not from wherever `@axe-core/playwright` actually resolves its injected engine. In a project with a nested/conflicting `axe-core` (top-level vs. `@axe-core/playwright`'s own dependency), this comparison could systematically mismatch every run, silently making `--resume` never skip anything — fails safe (forces rescan, never serves stale data) but with zero diagnostic beyond an unmoving `skipped_resumed:0`, defeating the feature in exactly the setup being probed. The comment's claim ("the same version @axe-core/playwright would inject") is unproven. Needs a comment softening the claim; a fix (resolve the same way AxeBuilder does, or compare against the freshly-measured `axeResults.testEngine.version` on the fly instead of pre-resolving) would be better but isn't required to satisfy memo §4 guard 3, which only requires *some* correct mismatch detection.

**MINOR — Duplicate independent counters (`baseline-url-scan.mjs:231-235` vs `292-301`).** `totals.measured`/`totals.errors` and `coverage.measured`/`coverage.aborted.count` are computed via two separate loops over the same predicate (verified numerically identical live). DRY/drift risk: a future edit to one loop's classification could silently diverge from the other, undermining the exact accounting SKILL.md:59 needs kept trustworthy. Recommend `buildCoverage` reuse the totals loop's counts instead of re-deriving them.

**MINOR — `classifyAbortReason` (lines 280-286) partially unverified.** `navigation` pattern confirmed live (`net::ERR_CONNECTION_REFUSED` → `navigation`). `timeout` is unverified but high-confidence (Playwright timeout messages contain literal "Timeout"). `axe-injection` is unverified and unproven — plausible but speculative. Safe fallback to `other` on non-match avoids miscategorization; recommend testing before the `by_reason` breakdown is relied on for client-facing reporting.

**MINOR — Persisted `resumed: true` (line 93, written back at line 97) has no run-identifying timestamp.** Mitigated: original `started`/`finished` are preserved transitively across repeated resumes (verified by code trace), so staleness age is still recoverable from the file alone. A `resumed_at` field would give fuller traceability but isn't required.

**Note, not a defect — alt_snapshot cache check is order-dependent (`baseline-url-scan.mjs:151`).** Keys off `ctx.firstViewportKey` (current run's `--viewports` order). Same viewport set requested in a different order across runs → valid alt_snapshot cache spuriously forces a rescan. Fails safe (over-cautious), not a data-integrity issue.

**Guards clean:** memo §4 guards 1–4 vs. `reusableCachedRecord` (lines 137-153) all verified exact, not weakened: status-gate exact (`!== 'measured'`), viewport-set exact-match (size+subset check on a duplicate-free key set = exact equality), `axe_core_version` checked per-viewport across all viewports, census checked per-viewport (correct — census runs per viewport per line 162), alt_snapshot checked first-viewport-only (correct — alt_snapshot is captured only at index 0, matching `extractAltSnapshot`). No rate/percentage field anywhere in `summary.json` computes over `aborted` (grep-confirmed, false-positive substring hits only).

## Canary 4, re-run live (current worktree code, copied byte-identical into scratch for node_modules resolution — verified via `diff`)
```
coverage: {
  "unit": "viewport_scan",
  "measured": 1,
  "aborted": { "count": 1, "by_reason": { "navigation": 1 } },
  "skipped_resumed": 0
}
```
Raw error matched: `page.goto: net::ERR_CONNECTION_REFUSED at http://127.0.0.1:19999/nope.html`. This differs from the receipt's quoted object (missing `unit`, `skipped_resumed`) — confirms the MAJOR finding above.

## Not checked
- Canaries 1, 2, 3, 5 not independently re-run (only verified against code reading + one supplemental live 2×2-viewport resume test I ran to settle the unit question).
- `axe-injection` classifier branch not exercised (no live axe-core injection failure induced).
- `@axe-core/playwright` nested-vs-top-level `axe-core` version-conflict scenario not reproduced (would require a contrived monorepo dependency layout); analysis is code-trace-based, not empirical.
- Byte-identical `.agents` mirror confirmed via `diff` — not separately re-executed.

**Verdict: REVISE**

---

## Round 2

## WP-D Round 2 — Delta Review

**Mirror check:** `.claude` / `.agents` copies byte-identical (`diff` clean). Worktree copy → scratch copy byte-identical before running.

**MAJOR — receipt canary 4 stale quote → CLOSED.** Doc now shows `{"unit":"viewport_scan","measured":1,"aborted":{"count":1,"by_reason":{"navigation":1}}},"skipped_resumed":0}`. Live re-run (current code, copied to scratch) reproduces this exactly.

**MAJOR — receipt didn't exercise the viewport-scan unit change → CLOSED.** New canary 6 lands. Live re-run (2 URLs × 2 viewports, clean then `--resume`): `measured:4, skipped_resumed:4` — matches doc verbatim, and matches my own round-1 number (no regression from the single-pass refactor).

**MAJOR — `coverage.measured`/`totals.measured` conflate fresh vs. resumed data → CLOSED (doc).** Docstring (lines 53-55) now states the overlap and the subtraction explicitly. Code behavior unchanged (still requires the reader to do `measured - skipped_resumed`), but that's now documented rather than a silent trap — resolves the finding as asked (a fix wasn't required, a comment was).

**MINOR — duplicate counters → CLOSED.** `buildSummary` (line 263) now calls `buildCoverage(results)` once and reads `totals.measured`/`totals.errors` from it (lines 292-293); no second independent loop re-deriving the same predicate. Verified live: `totals` and `coverage` numerically consistent in every run above.

**MINOR — version-provenance comment overclaim → CLOSED, comment now honest.** `resolveAxeCoreVersion` (lines 145-161) resolves `@axe-core/playwright`'s own entry file first, scopes a `createRequire` to it, then resolves `axe-core/package.json` from there — correctly following the same resolution chain `@axe-core/playwright`'s internal code would use, with a documented fallback to script-relative resolution. The comment (128-144) now states plainly what's compared, that a mismatch fails safe, and that it's silent beyond `skipped_resumed` staying 0. Live: fresh scan's `axe_core_version` (`4.13.0`) matches the version the function resolves in this scratch env — consistent, not contradicted. Not independently stress-tested against a genuinely nested-vs-top-level version divergence (same gap noted in round 1; not practically constructible here) — code logic is sound on inspection.

**MINOR — `resumed_at` added → CLOSED.** Line 99 stamps `resumed_at` on reuse; `started`/`finished` still preserved transitively. Not re-verified live this round (straightforward, low-risk change) — code-read confirmed only.

**Note — alt_snapshot order-independence → CLOSED.** `firstViewportKey` removed; guard (line 183) and `extractAltSnapshot` (lines 122-125) now check `.some(...)` / `.find(...)` across all cached viewport records. Correct fix for the order-dependency edge case.

**Not checked this round:** canaries 1/2/3/5 not re-run (unchanged code paths, no round-1 finding against them); nested-axe-core-version divergence still unreproduced; `axe-injection` classifier branch still unexercised (unchanged, pre-existing MINOR, not blocking).

No new issues found. All round-1 findings closed with either a verified code fix or an accurate doc correction.

**Verdict: PASS**
