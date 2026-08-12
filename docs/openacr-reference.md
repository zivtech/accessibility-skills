# OpenACR Verified Reference

Facts verified 2026-08-12 against `@openacr/openacr@0.3.8` (npm), `GSA/openacr` @ main, and the live editor at https://acreditor.section508.gov/ (v1.0). Every claim below carries a receipt from the Phase 0 spike of [the integration plan](plans/2026-08-12-openacr-integration-plan.md); anything not listed here is unverified. Companion: `openacr-adoption-assessment.md` (boundary ruling — to be written in Phase 1).

## Format

- **OpenACR** is GSA's machine-readable Accessibility Conformance Report format: one YAML document per ACR, validated against a JSON schema plus a named catalog. License: CC0-1.0. Source: `GSA/openacr`; npm package `@openacr/openacr`, latest **0.3.8** — package and format frozen since 2024-03-12 (the v1.0 push that added WCAG 2.2, EN 301 549, VPAT 2.5). Treat as a finished spec, not an active dependency.
- **Document structure**: report metadata (`title`, `product`, `author`, `report_date`, `last_modified_date`, `version`, `notes`, `evaluation_methods_used`, `legal_disclaimer`, `license`, `repository`, `feedback`, `related_openacrs`) + `catalog` (names the catalog the document claims against, e.g. `2.4-edition-wcag-2.1-en` in the upstream Drupal example) + `chapters` → `criteria` (`num`) → `components` (`name`: `web` / `electronic-docs` / `software` / `authoring-tool`; 508 chapters use their own component names) → `adherence` (`level`, `notes`).
- **Schema** (`openacr-0.1.0.json`), verified by direct read:
  - Root `required`: `title`, `product`, `author` — and inside those, only **`author.email`** is hard-required (`contact` definition, `required: ['email']`). `product.name`/`version` are schema-optional. Receipt: removing `email` → `Invalid: data/author must have required property 'email'`.
  - Chapter properties: `notes`, `disabled`, `criteria`. **`disabled: true`** is the format's built-in "criteria is not going to be provided in this ACR" marker — the correct way to mark human-owned/out-of-method chapters.
  - `adherence.level` is a **free string at the schema layer** (`"type": "string"`). Term legality is enforced only by the CLI's catalog-values check; level-appropriateness (see terms below) is enforced by nothing.
- **Catalogs shipped in the npm package** (9): `2.4-edition` × {wcag-2.0-508, wcag-2.1-508, wcag-2.1-508-eu, wcag-2.1} and `2.5-edition` × {wcag-2.0-508, wcag-2.1-508, **wcag-2.2-508**, wcag-2.2-508-eu, **wcag-2.2**}, all `-en`. The 2.2 catalogs contain all six WCAG 2.2-only A/AA criteria (verified: 2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8) plus 508 chapters (`functional_performance_criteria`, `hardware`, `software`, `support_documentation_and_services`).
- **Adherence terms** (catalog `terms:` block, official definitions): `supports` ("at least one method that meets the criterion without known defects or meets with equivalent facilitation"), `partially-supports` ("**Some** functionality of the product does not meet the criterion"), `does-not-support` ("The **majority** of product functionality does not meet the criterion"), `not-applicable`, `not-evaluated` ("can **only** be used in WCAG Level AAA criteria"). Note the terms are functionality-proportion claims — sample-scoped evidence must say so in notes.

## CLI (`@openacr/openacr`)

- Installs and runs on Node v24.13.0, 0 vulnerabilities (verified 2026-08-12). Ships catalogs, schemas, Handlebars templates, and example ACRs inside the package — consuming projects get everything from the one pin.
- Commands: `openacr validate -f <file> -c <catalogFile>` and `openacr output -f <file> -c <catalogFile> -t <templateFile> -o <outFile>`. Templates shipped: `openacr-markdown-0.1.0.handlebars`, `openacr-html-0.1.0.handlebars`, `openacr-simple-html-0.1.0.handlebars` (+ CSS). `output` without `-t` fails ("template file is invalid") — always pass the template.
- **`-c` is load-bearing on BOTH commands (Phase 2 gate-row discovery, reproduced 2026-08-12):** neither command loads the document's own `catalog:` field. `validate` without `-c` is schema-shape only — a document claiming nonexistent criterion `9.9.9` validates (`Valid!`); with `-c` it is correctly rejected. `output` without `-c` exits successfully and silently renders a metadata-only shell with zero criteria tables (14 KB vs 120 KB on the package's own `drupal-10-16.yaml`). Treat a bare `validate -f` as no validation at all, and check a rendered HTML actually contains its criteria tables before circulating it.
- **`validate` exits 0 on invalid input** (Phase 3 gate-row observation, reproduced 2026-08-12): the Invalid/Valid signal is stdout-only — a CI check keyed on exit status passes invalid (even unparseable) documents silently. Gate on the `Valid!` string, never the exit code.
- **Absent `license` is not neutral:** the schema states "If none is provided 'CC-BY-4.0' is assumed default in any output" (verbatim, `openacr-0.1.0.json`), and rendered HTML asserts that license. A deliberately-undecided license must be surfaced to the human at handoff, not treated as a safely-empty field.
- Verified round-trip: upstream `drupal-10-16.yaml` → `Valid!`; hand-authored minimal WCAG 2.2 document (catalog `2.5-edition-wcag-2.2-508-en`, incl. 2.2-only SC 2.5.8) → `Valid!` → rendered to Markdown and HTML.
- **Validation gaps — all verified, all load-bearing for consumers:**
  1. `validate` does **not** enforce the not-evaluated-AAA-only rule its own catalog text states: `not-evaluated` on Level A SC 1.1.1 → `Valid!`.
  2. `validate` does **not** enforce SC completeness: a document with 2 of ~50 A/AA criteria → `Valid!`.
  3. `disabled: true` chapters → `Valid!`.
  4. Catalog membership of criterion numbers is checked **only when `-c` is passed** (Phase 2 correction of this document's earlier claim — without `-c`, membership is not checked at all; see the `-c` bullet above).
  - Consequence: "schema-valid" is a weak gate. Completeness checking and per-level term legality fall entirely on the consumer (in this repo: `score_acr.py` and the acr-reporting skill's own gates), and even the membership check requires the explicit catalog flag.

## Editor (acreditor.section508.gov)

- GSA-hosted **OpenACR Editor v1.0** (April 2024), Svelte, derived from the W3C ATAG Report Tool. Editor repo (`GSA/openacr-editor`) is maintained (commits 2026-04-30) while the format is frozen — the two are on **different liveness tracks under the same vendor**.
- Storage: browser localStorage only (key `openacr_editor_store-data-model`); the site's own tips state nothing is saved server-side and the YAML file is the persistence/sharing mechanism.
- **Import works**: "Open report" → `input#import-evaluation` (`accept="application/yaml"`); the file is schema+catalog validated on import, with alert() feedback on failure.
- **Catalog skew (load-bearing constraint)**: the editor validates imports against the **2.4-edition / WCAG 2.1** catalog. Verified both ways on 2026-08-12: a CLI-valid `2.5-edition-wcag-2.2-508-en` document was **rejected** ("criteria '2.5.8' is not included in 'Table 2: Success Criteria, Level AA'"); the equivalent `2.4-edition-wcag-2.1-508-en` document imported cleanly. The AA page header links "Web Content Accessibility Guidelines 2.1". **acreditor can finish WCAG 2.1-catalog drafts only, today.**
- `disabled: true` chapters import cleanly: chapter notes render in the chapter's Notes field; the chapter drops out of the progress sidebar. Progress counts are per-component cells ("Reported on 1 of 327 Total Criteria"; A 1/120, AAA 0/112, FPC 0/9, Hardware 0/55).
- Watch rule: re-verify import compatibility and the catalog edition **on every editor release** (editor moves, pin doesn't — the KAT pin-bump pattern).

## Upstream Issue Candidates (Phase 4 — search existing issues before filing; ready-to-file drafts in [the Phase 4 handoff](plans/2026-08-12-openacr-phase4-handoff.md))

1. `GSA/openacr`: `validate` without `-c` skips catalog checking entirely — nonexistent criteria report `Valid!` (Phase 2 discovery, reproduced).
2. `GSA/openacr`: `output` without `-c` exits successfully while rendering a metadata-only shell with zero criteria tables (reproduced on the shipped Drupal example).
3. `GSA/openacr`: `validate` does not enforce the "Not Evaluated only for WCAG Level AAA" constraint stated in its own catalog term description.
4. `GSA/openacr-editor`: no support for the 2.5-edition / WCAG 2.2 catalogs the format itself ships; valid 2.2 documents are rejected on import.
