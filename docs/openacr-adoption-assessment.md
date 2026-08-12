# OpenACR Gap Analysis & Adoption Assessment

> **Status: adopted for Lane A drafting via the `acr-reporting` skill — RECOMMENDED as of 2026-08-12** (the [integration plan](plans/2026-08-12-openacr-integration-plan.md)'s Phase 2 gate passed: hosted tier, fixtures 1/2/3/5, stable across 2 draws, zero must-tier misses — receipts in `evals/results/acr-reporting-phase2/`). Lanes B/C remain future phases.
> Verified facts + receipts: [openacr-reference.md](openacr-reference.md) (2026-08-12).

## What It Is

OpenACR is GSA's machine-readable Accessibility Conformance Report format: YAML documents validated by JSON schemas against named catalogs (VPAT 2.4/2.5 editions × WCAG 2.0/2.1/2.2 × plain/508/EU), with an official CLI (`@openacr/openacr`, CC0) for validation and Markdown/HTML rendering, and a GSA-hosted human editor at https://acreditor.section508.gov/. The format is frozen at v1.0 (March 2024); the editor is maintained separately.

## Gap Analysis — What It Adds

- The **"populate" step** the evaluation report contract's Boundaries section anticipates: a concrete, validatable external report format for audit-scope engagements (pre-VPAT work becomes actual ACR drafting).
- **Machine-readability**: per-SC, per-component terms diffable across releases (Lane C trend), claim-checkable against evidence (Lane B verification).
- **A government-native surface**: Section 508 procurement speaks this format; acreditor is the human finish/review surface for 2.1-catalog drafts.
- **Landscape position**: every external skill in `EXTERNAL-SKILLS-INVENTORY.md` scopes VPAT/ACR work out; nothing else in the inventoried ecosystem produces ACRs.

## Gap Analysis — What It Does NOT Cover (and what keeps covering it)

- **Quality enforcement**: `openacr validate` checks shape, not honesty — it accepts SC-incomplete documents and `not-evaluated` on A/AA (both verified). The `acr-reporting` skill's gates and the Phase 2 scorer carry completeness, per-level term legality, orthogonality, and value provenance.
- **Non-web evidence**: electronic-docs/software/authoring-tool components and 508 hardware/support-docs/FPC chapters — human-owned; the skill serializes only their boundary statements via `disabled:` chapters.
- **WCAG 2.2 in the hosted editor**: acreditor speaks the 2.4-edition/WCAG 2.1 catalog only (verified: rejects valid 2.2 documents). 2.2 drafts finish via CLI-rendered HTML + YAML.

## Adoption Boundary (the ruling)

- **Routed dependency, never vendored**: `@openacr/openacr@0.3.8` exact-pinned in consuming projects or scratch-installed at scoring time. No editor vendoring, no schema/catalog copies in this repo, no format fork, no report-generator runtime (existing contract ruling) — the agent authors YAML per the skill's normative tables.
- **This repo gains no `package.json`**: the eval scorer (`ollama/score_acr.py`, Phase 2) provisions the CLI in a scratch directory per the `verify`-skill reproduce-from-scratch pattern.
- **No auto-publishing**: no writes to acreditor, no signed/final ACRs, no conformance claims. Draft + human sign-off is a hard boundary.

## Alternatives Considered

**EARL** (W3C Evaluation and Report Language) is the report contract's original `machine_readable` value and is documented at length in `bug-reporting`. EARL is **assertion-level** — one test result per subject/criterion — with no ACR chapters, no VPAT-edition catalogs, no adherence-term vocabulary, and no editor; it is the right export for aggregating raw test results across tools. OpenACR is **ACR-shaped** — the procurement document itself. They are complementary, not competing: EARL remains a valid `machine_readable` value for evidence export; OpenACR is the value for conformance-report deliverables. Nothing here deprecates EARL.

**Hand-authored VPAT documents** (Word/PDF) remain what many engagements contractually require; this adoption does not replace them — the OpenACR draft can be the evidence-complete source the human transcribes from, and the naming rule holds (our artifact is never called "a VPAT").

## Calibration Rules

- A schema-`Valid!` result is a **weak gate** — treat CLI validation as necessary, never sufficient. The skill's completeness self-check and the scorer are the real gates.
- acreditor import failures name the offending criterion (alert text) — read them as catalog-mismatch signals first (2.2-in-a-2.1-editor), YAML errors second.
- `disabled: true` chapters drop out of acreditor's progress counts by design — that is correct behavior for human-owned chapters, not data loss (chapter notes still render).

## Watch Rule

The format pin is frozen; **the editor moves** (commits April 2026). On every `GSA/openacr-editor` release: re-verify YAML import, the catalog edition the editor validates against, and `disabled:` chapter tolerance — then update [openacr-reference.md](openacr-reference.md). Same pattern as the KAT pin-bump recheck. If the editor gains 2.5-edition/WCAG 2.2 catalogs, the dual-catalog policy's default finish surface flips to acreditor — that is a skill edit, not just a docs edit.

## Risks & Uncertainty

- **Dormant format upstream**: schema 0.1.0, issues may sit unanswered. Accepted: CC0 + trivial YAML schema + a format-portable mapping table make this closer to "finished spec" than abandonment exposure; community forking is already precedented (CivicActions lineage).
- **Editor availability/policy**: GSA could move or retire acreditor. CLI is the durable surface; self-hosting `GSA/openacr-editor` (open source) is a consuming-org escape hatch.
- **Overclaim-by-format**: schema-valid drafts look authoritative regardless of evidence quality — the named risk the skill's gates and eval traps exist to hold.

## What This Does Not Claim

- No legal authority: outputs are drafts, not conformance claims, signed ACRs, or legal advice; no Trusted Tester/TTv5 equivalence.
- No non-web conclusions, no EU non-WCAG clause mapping, no merge-into-existing-ACR flow (named out of scope in the plan).
- No statement about local-model fitness for ACR generation — value-dense output stays hosted-tier or value-checked, per the plan's routing rule; the eval lane will produce the actual rows.
