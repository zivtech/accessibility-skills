# a11y-critic round on WP-C (2026-09-02)

Gate for `references/hash-evidence.mjs` + the one-sentence reference in
`a11y-test/SKILL.md` § Evidence retention (PT-02). Reviewer: `a11y-critic`
agent at sonnet, read-only on the repo, running the script against scratch
trees (13 probes). Single round: PASS with two MINOR + two ENHANCEMENT items,
all applied before commit (symlink exclusion documented in the header,
receipt wording, `drift` field in `--json`, exit-code 2 docstring). Verbatim,
recovered from the agent transcript.

---

## Predictions (written before testing)

1. Manifest hashes itself when `--out` defaults inside `--root` — *false*, `outFile` is excluded from the walk (T2/T3).
2. `--append` can silently rewrite a changed entry — *false*, refuses at exit 1, manifest byte-identical (T8).
3. Plain write over an existing manifest silently clobbers it — *false*, refuses at exit 2, byte-identical (T4).
4. Path separators leak OS-specific `\` on this platform — *not applicable*, POSIX only; `.split(path.sep).join('/')` is a no-op here, code is defensively correct for Windows too.
5. A symlink in the tree crashes the walk — *false*, but **silently excluded** from tracking entirely (new finding, not predicted this way).
6. `--verify` exit code disagrees with its printed summary — *false*, exit matches drift state in every mode (T6/T7/T12b).
7. The SKILL.md sentence restates lines 65–69 or overclaims — *false*, it describes the script's mechanism, doesn't restate the rule, and its exit-condition wording (`modified`/`missing` always, `new` only under `--strict`) matches observed behavior exactly.

## Probe table

| # | Check | Result |
|---|---|---|
| 1 | Write + self-exclusion (default & custom `--out` inside `--root`) | Manifest never lists itself (T1–T3) |
| 2 | Plain write over existing manifest | Exit 2, refused, byte-identical after (T4) |
| 3 | `--append` after mutating a listed file | Exit 1, refused, byte-identical after (T8) |
| 4 | `--append` with only new files | Exit 0, existing entry byte-identical, new entry added (T9) |
| 5 | Determinism (manifest outside root, 2 clean writes) | `entries` identical, only `generated_at` differs (T5, corrected — first attempt wrote the manifest inside `root`, which is expected self-referential noise, not a bug, matching the receipt's own noted methodology artifact) |
| 6 | `--verify` clean / modified+missing+new / `--strict` / `--json` | All correct; strict promotes `new` to drift (exit 1); json shape = `{modified,missing,new}` (T6/T7) |
| 7 | Nonexistent `--root` | ENOENT surfaces via `main().catch`, exit 2 (T10) |
| 8 | Empty tree | 0 entries written, verify clean, exit 0 (T11) |
| 9 | Symlink in tree: write, then verify (incl. `--strict`) | Symlink never appears as entry or as `new` under any mode — silently invisible (T12/T12b) |
| 10 | Unrecognized flag | Exit 2, `unrecognized argument: --bogus-flag` (T13) |
| 11 | Receipt fidelity vs. re-run | Steps 1–6 reproduce exactly; one wording inconsistency (below) |
| 12 | Header negative-space clause | Present: "not a signing or custody system... a manifest can be deleted by whoever can delete evidence" |

## Findings

1. **MINOR** — `references/hash-evidence.mjs` walkFiles(): symlinked files inside an evidence tree are silently excluded from tracking in every mode, including `--verify --strict` (confirmed T12/T12b: a tree with `real.txt` + `link.txt -> real.txt` produces one entry, and `--verify --json` reports `{modified:[],missing:[],new:[]}` for the untracked symlink). Not a crash, but undocumented — the "What this is NOT" clause doesn't mention it. Fix: add one line noting symlinked files are excluded from tracking.
2. **MINOR** — `evals/results/evidence-checksums-2026-09/verify-pair.md:3` says the fixture has "4 files (`data.json`, `summary.txt`, `nested/run.log`, one JSON)" but step 1's own output says "3 entries" and names only 3 files — "one JSON" is an editing leftover, not a real 4th file. Fix: drop "one JSON."
3. **ENHANCEMENT** — `--json` payload shape is identical with/without `--strict`; only the exit code reflects whether `new` counted as drift, so a caller parsing JSON alone can't tell. Optional: add a `"drift": true/false` field.
4. **ENHANCEMENT** — Script's exit-code docstring for `2` doesn't name the generic catch-all cases (bad flag, missing `--root`) that also land there via `main().catch`, though behavior is correct and consistent with the documented bucket.

## Not checked
- Windows path-separator behavior (no Windows box available; code path reviewed, looks correct).
- Concurrent/racing writers to the same manifest (no lockfile — plausible gap, not exercised).
- Very large trees / performance.

**Verdict: PASS**

Append-only semantics hold under every invocation tried (plain write, `--append` after mutation, `--append` with only additions) — no path rewrites an existing entry. `--verify` classification and exit codes are correct across clean/dirty/strict/json modes. Self-exclusion, determinism, and empty-tree edge cases are correct. The SKILL.md sentence doesn't restate lines 65–69 and doesn't overclaim. Both file pairs are byte-identical (`cmp`). Findings are cosmetic (symlink docs, one receipt wording slip, JSON self-description) — none block the disposition.
