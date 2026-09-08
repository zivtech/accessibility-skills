# Content review: export, observe, return

This is a small offline return path for **content judgments**. It renders the existing content units as review tasks, then imports explicit human responses into `ratifications.jsonl`. It makes no tracker/API calls and owns no assignments, workflow states, or human identities. The receiving tracker owns those.

The script uses Node built-ins only. Run it from the skill's `references/` directory, or substitute the absolute script paths below. Keep each capture and its review history in a dedicated inventory directory.

## 1. Prepare and export

First finish the usual inventory/build/draft steps. Refresh the merged view, then export a **new** directory:

```bash
node build-judgment-rows.mjs --merge --inventory /path/to/inventory
node review-content-judgments.mjs --export --inventory /path/to/inventory --out /path/to/review-bundle
```

The bundle contains:

| File | Purpose |
|---|---|
| `bundle.json` | Exact source units, per-unit hashes, source-snapshot hash, original draft, and each prior decision ID |
| `review-tasks.csv` | Portable draft tasks; use `unit_id` as the primary key in an ordinary CSV workspace |
| `review-tasks.md` | Human questions, context, and blank observation prompts |
| `return-template.json` | Bundle identity and unit pins, with human decision, name, date, and observation fields blank |

Default export includes only units still awaiting a complete WCAG content judgment. `--all` explicitly requests rereview, including completed units. Existing bundles are never overwritten. A partial export caused by a filesystem failure must not be used; preserve it and export a fresh directory after resolving the error.

The CSV contains draft tasks, not adjudicated findings. Do not manufacture finding fingerprints or load these rows as confirmed accessibility violations. Text beginning with a spreadsheet formula prefix is prefixed with an apostrophe in the CSV; the bundle retains the exact source. The CSV deliberately excludes the agent verdict so a reviewer can record their observation first; the original draft is available in `bundle.json` for comparison.

The local coordination layer may group setup and navigation, assign a reviewer, record a blocker/provider, or link a remediation task. It must preserve the unit identity, bundle and unit hashes, and base decision ID. A tracker status edit cannot create a judgment or attestation. A generic decision export lacking these pins is not a valid return file: adapt it explicitly when the tracker supports the necessary linkage, rather than filling missing provenance by guessing.

## 2. Observe and return

A person reviews the captured context, and the live page when the judgment depends on facts absent from that context. They supply the observation/rationale, `yes`, `no`, or `unsure`, their own name, and a UTC timestamp with seconds ending in `Z`. The agent must not invent any of these on their behalf. Keep test instructions available; do not prefill an observed result or approval.

Copy the template into a response file. Retain only units actually reviewed; omitted units remain pending. The wrapper is:

```json
{
  "bundle_id": "<copied from the issued bundle>",
  "decisions": [
    {
      "id": "<unit_id>",
      "scope": "wcag",
      "unit_sha256": "<copied from that task>",
      "ratified_by": "<actual reviewer>",
      "ratified_judgment": "<yes, no, or unsure>",
      "ratified_utc": "<actual review time in UTC>",
      "ratifier_note": "<what the reviewer observed and why it supports this judgment>"
    }
  ]
}
```

These placeholders are instructions, not a completed human review. When replacing an earlier decision, retain the template's `supersedes` ID and supply `supersession_reason`. The new response must describe a real reconsideration; copying an earlier response is not a new confirmation.

If the human and agent disagree, retain both observations. Use `unsure` when the available evidence cannot decide the content question. The tracker should name the adjudicator, the competing explanations, and the next check that can distinguish them. If it cannot decide, retain the disagreement and name the missing evidence. A later ruling explicitly supersedes the earlier human decision; file order never resolves a disagreement.

## 3. Apply and regenerate

```bash
node review-content-judgments.mjs --apply --inventory /path/to/inventory --bundle /path/to/review-bundle --responses /path/to/response.json
node build-judgment-rows.mjs --merge --inventory /path/to/inventory
```

`--apply` validates the entire response and accumulated history before replacing `ratifications.jsonl`. The successful result names `merge_judgments` as the next action; applying the response does not itself regenerate the CSV/JSON views. The subsequent merge produces the normal outputs and diagnostics.

- Incomplete returned decisions, missing observations, unknown/duplicate units, unsupported scopes, altered bundles, mismatched pins, and competing decisions fail with exit **2** before history changes.
- Repeating the same valid response is idempotent: no duplicate history line is added.
- A fresh contrary response from an old bundle is a conflict, not an implicit correction. Preserve it as a response artifact, resolve the disagreement, and issue a fresh rereview bundle.
- The entire inventory snapshot is pinned conservatively in this first loop. Rebuilding it requires a new bundle, even if some unit IDs are unchanged. Changed evidence belongs in a fresh inventory directory, with the previous capture and receipts retained. Do not remove old receipts to make a new snapshot pass. This is particularly important for title units, whose IDs are based on view identity rather than title text.
- Writers using `--apply` serialize with `.content-review-return.lock`. An outstanding lock blocks another writer and is never automatically stolen. If a process crashes, confirm it is no longer running before removing its lock. Atomic rename protects the history replacement; editors and external tools that ignore the lock are not coordinated writers. The script also rechecks history and source before replacement, but does not claim a database transaction across independent editors or generated views.

Hashes bind content and detect accidental drift; they do not authenticate a person or defeat intentional rewriting of both data and hashes. Keep the original response and the actual human confirmation in the engagement's normal custody mechanism.

## Direct JSONL import compatibility

The existing `--merge` entry point still accepts complete legacy `ratifications.jsonl` records without pins, labels them `legacy_unpinned`, and warns. A legacy record without unit pins or supersession fields may retain a real calendar date (`YYYY-MM-DD`); the merged view labels its `date_precision` as `day` and emits a `legacy_day_precision` diagnostic. Its original date string and decision identity stay intact: no midnight or other time is invented. Full UTC dates are labeled `timestamp`. Invalid dates still refuse the import, and missing names/results remain draft. Shape alone cannot establish that an unpinned record is old.

These labels do not retroactively prove which content was reviewed or when within that day. New external returns through this loop always require unit pins and a full UTC timestamp ending in `Z`, as do direct records containing pins or supersession fields. Historical date precision is a compatibility boundary, not a relaxation of the new return contract.

Direct JSONL inputs may carry the existing independent client scope. `ratified_client_result` remains an engagement-specific nonblank string; it does not become a WCAG outcome. This portable wrapper initially covers WCAG content review only.

For direct import, a missing name, result, or date is an incomplete draft with a warning; named-but-incomplete records do not populate effective `ratified_by`. A malformed line, unknown unit/scope/field, invalid result/date/pin, or unresolved duplicate refuses the entire import before output writes. Diagnostics identify the line. Completing or withdrawing a prior draft/decision requires `supersedes` and a nonblank reason; decision IDs are exposed on the merged rows. Unknown or forward supersession references are refused.

## Evidence boundaries and pilot

A content `yes` remains sample-scoped and cannot yield Supports. A ratified `no` may enter the existing finding/receipt path; this tool creates no finding or report outcome itself. Interactive retests, class-matched fix evidence, human attestation, second confirmation, and ACR admission continue to use their separate existing contracts.

Run a small real pilot only when its source inventory and participating humans are available. Track clarification exchanges, duplicate work, rejected incomplete/stale returns, observation-quality corrections, and actual handling time. A synthetic round trip proves the software path, not a human verification campaign or attested closure. Do not count the software tests toward issue #57's real-campaign exit criterion.
