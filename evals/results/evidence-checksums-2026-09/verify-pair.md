# hash-evidence.mjs verify-pair receipt (PT-02, WP-C)

Node v24.19.0. Script: `.claude/skills/a11y-test/references/hash-evidence.mjs`. Fixture: a scratch evidence tree with 3 files (`data.json`, `summary.txt`, `nested/run.log`) — run from a scratch dir outside this repo, never committed.

## 1. Write manifest

```
$ node hash-evidence.mjs --root "$FIX" --out "$FIX/checksums.json"
wrote .../evidence-fixture/checksums.json: 3 entries
```
exit=0

## 2. `--verify` on the unchanged tree

```
$ node hash-evidence.mjs --root "$FIX" --out "$FIX/checksums.json" --verify
verify: 0 modified, 0 missing, 0 new (new is informational)
```
exit=0

## 3. Mutate one file, delete one, add one, then `--verify`

Edited `summary.txt`'s content, deleted `nested/run.log`, added `extra.txt`.
```
$ node hash-evidence.mjs --root "$FIX" --out "$FIX/checksums.json" --verify
verify: 1 modified, 1 missing, 1 new (new is informational)
  modified: summary.txt
  missing:  nested/run.log
  new:      extra.txt
```
exit=1

## 4. Overwrite refusal without `--append`

```
$ node hash-evidence.mjs --root "$FIX" --out "$FIX/checksums.json"
refusing to overwrite existing manifest: .../checksums.json
pass --append to add new entries without touching existing ones.
```
exit=2

## 5. `--append` with a changed listed file (still-mutated `summary.txt`)

```
$ node hash-evidence.mjs --root "$FIX" --out "$FIX/checksums.json" --append
refusing to append: listed file(s) changed since capture (append-only, not an update):
  modified: summary.txt
```
exit=1

## 6. `--append` with only new files (restored `summary.txt` to its captured content first)

```
$ node hash-evidence.mjs --root "$FIX" --out "$FIX/checksums.json" --append
appended .../checksums.json: 2 new entries (3 unchanged)
```
exit=0

Diffed the pre-append manifest's entries against the post-append manifest for the three originally-listed keys — `data.json`, `nested/run.log`, `summary.txt` — all three `byte-identical=True`. Two new keys were added: `extra.txt` (the intended new file) and `checksums.before-append.json` (the pre-append manifest copy, placed inside `$FIX` for the diff and correctly picked up by the walk as a genuine new file — a receipt-methodology artifact, not a script defect). `nested/run.log` stays absent from disk and is correctly left untouched by append, not re-added.
