# qwen pre-sort — Stage-A local proof

Stream 2 (qwen detector-step pipeline) Stage-A harness. See the design at
`docs/plans/2026-09-12-qwen-detector-step-design.md`.

`accordion-no-region-role-qwen3.6-35b.json` is a **local, free** proof run of
`ollama/presort_candidates.py` (qwen3.6:35b on the dedicated `:11435` port).
It is not a benchmark result and involves no hosted (Claude API) call.

What it demonstrates:
- The generator produces a schema-valid `candidates.json` (leads only; no
  verdicts, no exact selectors/IDs; location hints).
- Run blind (the generator reads only the fixture `.md`, never its
  `.metadata.yaml`/rubric), qwen surfaced the fixture's planted defect as its
  top lead (`c1`: content containers lacking a landmark role / accessible
  name — the `no-region-role` bug) plus two lower-confidence adjacent leads.

This is the detector half only. Whether these candidates let a hosted judge do
**less real work at equal detection** is what Stage A's hosted A/B measures —
gated on explicit approval to spend, per the design doc.
