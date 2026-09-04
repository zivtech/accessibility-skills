# Pack construction — session receipt (2026-08-25/26)

Executed across three sessions: the original pack-construction orchestrator
(died ~00:24Z on a network outage, transcript `b43838df`), and the 2026-08-26
recovery session (this one) plus one mid-day harness restart. Everything below
is committed in this directory tree; per-step receipts are the sibling files.

## What was recovered from the dead session (never re-run)

- The 33-page axe batch (`raw/axe-batch-2026-08-25/`, 0 errors, ruling-4
  "should"-string confirmed), the file-input driven trace
  (`raw/file-input-no-labels-kat-driven/`), the heading census
  (`raw/heading-hierarchy-skipped-kat-census/`), the build_fixtures.py path
  fix + 41-page render + SHIMS-restricted sweep (precondition F10).
- question-author's pre-correction 6-question YAML, recovered from the dead
  session's transcript (delivered 00:24:13Z as the session died; the corrected
  regeneration failed mid-response at 00:18:10Z). 5 questions accepted; the
  stale heading question discarded and re-authored blind
  (`question-authoring-spawn-prompt.md` recovery record).

## Instrument events (full record: n1-calibration-checkpoint.md)

- n=1 calibration checkpoint FIRED: 2 haiku draws condensed the ARIA `states`
  dict (the Phase 2.3 failure class recurring, once per def revision) and
  draw 2 fabricated `wcag_or_apg: 4.1.3` — the documented wrong mapping — on
  a trace with zero WCAG strings. Def hardened; **agent defs proven
  hot-reloaded at spawn** via the new permanent `def_rev` output stamp.
- Recorded amendment: this lane's CURATED digests run the reader at **sonnet**
  (haiku stays the def default outside the lane). Sonnet question-fidelity
  slip observed once (tabs draw 1, one character) — caught by pre-freeze
  byte-diff, re-run clean.
- Every frozen digest was verified against raw artifacts field-by-field
  before freeze (values, states dicts, census sequences, corpus counts).
  One prose-level blur recorded, not re-run (file-input obs 6 labels
  `focus_appearance` values under `focus_visible`; all values exact,
  step-granularity handle resolves both — noted in the audit `note`).

## Ruling 6 completion (file-input raw-set expansion)

The ground-truth audit pass found the collected raw set (axe + driven trace)
carried NO error-present evidence — items [1]/[2] would have stayed a
raw-set-gap despite ruling 6. A fresh SR census on the same rendered page
(error pre-triggered at mount) captured `"File too large"` as a bare
unassociated text node (`raw/file-input-no-labels-kat-census/`), completing
the evidence pair BEFORE any pack froze. Question re-authored blind over the
3-artifact set (question-author-3); reader re-run; digest re-frozen. The
lane's tool-observable pool is genuinely 8 as ruling 6 intended.

## Freeze inventory

- 6 CURATED digests frozen (`packs/*.curated.md`, sonnet, def_rev 2026-08-26a,
  sha256 per fixture in `lane_manifest.yaml` `digest_content_hash`).
  Ruling-5 ≠ assertion PASSED (dropdown hash ≠ Phase 2.3 worked-example hash
  `d248fe7b…`, extraction rule in the calibration receipt).
- 6 DUMP packs built (`packs/*.dump.txt`, deterministic sorted-filename
  first-fit padding to the estimated ceiling − 500; build record
  `packs/dump-sizing-build-record.json`; file-input rebuilt 2026-08-26b with
  the census, other 5 byte-identical across rebuilds).
- 6 completeness audits (`completeness/*.audit.yaml`, §10 gate-F4 4-field
  shape, validated through `score_evidence_lane.load_completeness_audit` +
  `flatten_must_find_items` index alignment). Notable partitions:
  dropdown item [1] (post-Escape focus) = genuine **raw-set-gap** (no Escape
  keystroke was ever driven); file-input item [3] = **not-tool-observable**
  (source-only, README §10's own worked example).
- F14 closed with data (`receipts/dump-measured-probes-2026-08-26.json`,
  24 probes: 6 fixtures × 2 models × {dump-40k, curated-32k}): JSON dumps
  tokenize at est/measured 1.07–1.11 (qwen3:32b) and 1.01–1.03 (qwen3.6:35b);
  every assembled DUMP prompt fits 40,960 (worst margin 1,047, modal @ 35b).
  known_risk `f14-dump-json-tokenization-ratio-unmeasured` → RESOLVED-BY-
  MEASUREMENT. CURATED@32K fit + gate-F2 digest-cap verdicts recorded in the
  same receipt (see manifest per-fixture notes).

## Environmental findings (affects every local benchmark on this machine)

1. **Port 11434 was shadowed for ~2 weeks** by an OrbStack container
   (`open-notebook-ollama-1`, `ollama/ollama:latest` 0.23.0, Linux/CPU-only,
   `restart: always`, sharing the host model store). It intermittently
   captured localhost connections, serving models at ~0.2 tok/s with
   `size_vram: 0` — it ate this run's first probe attempt, resurrected itself
   mid-run (re-shadowing the port), and retroactively explains the dead
   session's mysterious "~1.7h model pull". Fixed for this machine state:
   `docker update --restart no open-notebook-ollama-1 && docker stop
   open-notebook-ollama-1` (reversible: `docker update --restart always` +
   `docker start`, or remap the open-notebook compose to another port).
   **Rule: verify `/api/ps` shows nonzero `size_vram` and `lsof -nP
   -iTCP:11434 -sTCP:LISTEN` shows only the native `ollama` before any local
   benchmark row.**
2. The native Ollama app **auto-updated mid-run** (0.32.15 → 0.33.0,
   self-restart at ~13:57) — a second way in-flight local rows can die.
   Declared context lengths re-verified after both events: qwen3:32b=40,960,
   qwen3.6:35b=262,144 — the lane's standardization holds. Native Metal
   performance verified twice (25–26.3 tok/s, 29.2 GiB VRAM).
3. The pinned 11435 instance remains down (same caveat as the 2026-08-24
   probes).

## Next (not this session's scope)

Scored model rows: local 72 (+2 OVERFLOW receipts) per §5's matrix via
`ollama/run_evidence_lane.py`, hosted 48 via subagents — 2-draw adjudication
discipline, registered predictions P1/P1b/P2/P3.
