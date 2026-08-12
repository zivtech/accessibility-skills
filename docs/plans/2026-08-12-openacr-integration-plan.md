# OpenACR / acreditor.section508.gov Integration Plan

> **Status:** APPROVED + REVISED — recommendations accepted 2026-08-12; proposal-critic verdict REVISE, all findings addressed below; **Phase 0 spike COMPLETE 2026-08-12** (results in Assumption Register)
> **Consequence level:** Internal Tool (prompt-only skill + docs + eval lane; no production runtime). One consequence-raising caveat: the output artifact is a *conformance report draft* that a human may publish — the gates below exist because of that.
> **Companion docs:** `docs/openacr-reference.md` (verified format facts, written from the Phase 0 spike), `docs/openacr-adoption-assessment.md` (boundary ruling — Phase 1)

**Goal:** Users of the accessibility-skills bundle can turn a finished audit-scope engagement into a draft Accessibility Conformance Report in the OpenACR format, finish and sign it in GSA's hosted editor (https://acreditor.section508.gov/) where the catalog allows, and — in the reverse direction — audit someone else's OpenACR claims against evidence.

---

## Verified Facts

Moved to [`docs/openacr-reference.md`](../openacr-reference.md) with receipts. Summary: OpenACR is GSA's YAML ACR format (CC0, npm `@openacr/openacr@0.3.8`, frozen at v1.0 since 2024-03; catalogs through VPAT 2.5 / WCAG 2.2 / 508 / EN 301 549); the CLI validates and renders; the hosted editor imports/round-trips YAML but **speaks the 2.4-edition / WCAG 2.1 catalog only** (verified: rejects valid 2.2 documents — live version skew between frozen format and maintained editor). The CLI enforces neither SC completeness nor the not-evaluated-AAA-only rule; `author.email` is the one hard-required contact field. Lineage note: the canonical upstream example is Drupal's, authored by Mike Gifford / CivicActions — the same @mgifford whose guide became our `bug-reporting` skill. The external-skills inventory shows the scanned landscape explicitly scoping VPAT work out; this is open ground.

## Why This Fits (the hook already exists)

`docs/a11y-evaluation-report-contract.md` § Boundaries: *"This contract does not replace VPAT/ACR templates … this contract is the internal evidence spine that populates it."* OpenACR makes "populates" a concrete, **testable** step:

| Evaluation report contract | OpenACR field |
|---|---|
| `outcomes` per-SC EARL map (`passed`/`failed`/`cantTell`/`inapplicable`/`untested`) | per-SC adherence terms (mapping table below) |
| `findings` (evidence contract blocks, fingerprints) | per-SC `notes` — remarks cite the findings behind them |
| `evaluation_identity` + `accessibility_support_baseline` + `sample_set` | `title`, `author` block, `report_date`, `evaluation_methods_used` (WCAG-EM cited, sample size stated) |
| `coverage_boundary` + evidence contract `section_508_fpc_context` | `disabled:` chapters with notes; FPC chapter note text |
| `conformance_target` (WCAG 2.2 AA) | catalog selection (policy below) |

The planner's AUDIT-SCOPE MODE already collects "report template (e.g., VPAT edition)" as an additional requirement; this plan names OpenACR as a selectable value of that requirement, not a new concept.

## Critic Findings Addressed (proposal-critic, 2026-08-12, verdict REVISE)

| Finding | Severity | Resolution |
|---|---|---|
| Lane A unexecutable as written: schema requires `author.email`; contract carries no email/product/title; A5 overrated | CRITICAL | A5 downgraded and its fallback executed as a Phase 1 task: contract gains ACR-feed fields. Author-block policy added (below). Spike re-run confirmed the failure mode empirically. |
| Mapping table silent on half the catalog surface (AAA, FPC, catalog default, non-web component shape, blocked-SC shape, `disabled:` flag) | MAJOR | Five normative policies added (below). `disabled:` verified working on both CLI and editor. |
| A2 fallback = silent truncation of nine 2.2-only SCs | MAJOR | A2 passed, but the no-silent-truncation rule is now the **dual-catalog policy** (below) — mandatory because the editor skew makes down-catalog drafting a *routine* path, not a fallback. |
| Phase ordering: lifecycle wiring before the eval gate contradicts house precedent | MAJOR | Wiring moved behind the Phase 2 gate; "recommended" operationally defined (below). |
| Fixture 5 mis-homed (Lane B shape in a Lane A phase); gate has no false-positive condition, no draw policy | MAJOR | Fixture 5 redefined as Lane A complete-bundle FP control; Lane B clean control moved to Phase 3; gate gains FP condition + 2-draw stability. |
| Scorer shells out to Node with no provisioning story | MINOR | Recipe specified: scratch-dir `npm i @openacr/openacr@0.3.8` per the `verify`-skill reproduce-from-scratch pattern. |
| "Sampling statement" escape hatch ungradeable; most notes use it | MINOR | Canonical machine-checkable note forms specified (below). |
| finding_id vs sample_id conflation | MINOR | Notes cite `finding_id`s; sample enumeration uses `sample_id`s from `evaluation_context`. Both, explicitly. |
| EARL alternative unacknowledged in `machine_readable` | MINOR | Adoption assessment gets the one-paragraph EARL-vs-OpenACR ruling (assertion-level vs ACR-shaped; both remain valid values of `machine_readable`). |
| A1 verified point-in-time against a moving editor | MINOR | Watch rule added to reference doc + adoption assessment: re-verify on every editor release. Skew is already live — see dual-catalog policy. |
| Lane C trend vocabulary needs self-produced fingerprints | MINOR | Boundary stated: foreign ACRs get term-level deltas only. |
| No rollback table / success criteria | MINOR | Added (below). |
| Talk demo stakes its import beat on A1 | MINOR | Resolved by skew discovery: import beat uses the 2.1-catalog demo file; the 2.2 story renders via CLI HTML. Both artifacts exist from the spike. |
| Terms are functionality-proportion claims; sample-scoped outcomes must say so | MINOR | Note-template requirement: every `does-not-support`/`partially-supports` note carries explicit sample scope (scorer-checked). |

## Three Lanes

### Lane A — ACR drafting (evidence spine → OpenACR YAML) — build first
After an audit-scope engagement completes (planner audit mode → a11y-test WCAG-EM sampling → critic → evaluation report), the agent serializes the report into a **draft** OpenACR YAML, validates via the routed `openacr validate` CLI, renders via `openacr output`, and hands off to a human who finishes and signs — in acreditor when the draft uses a 2.1 catalog, via YAML + CLI HTML otherwise.

**Outcome → adherence mapping (normative for the skill):**

| Outcome across the sample set | Adherence term | Condition |
|---|---|---|
| `passed` everywhere applicable | `supports` | note uses the canonical sample-scope form |
| `failed` wherever applicable | `does-not-support` | note MUST state sample scope + cite `finding_id`s |
| mixed pass/fail across samples or instances | `partially-supports` | note MUST enumerate failing `sample_id`s and cite `finding_id`s |
| `inapplicable` | `not-applicable` | note states why (content type absent) |
| `untested` or `cantTell` on any A/AA SC | **no mapping — emission blocker** | draft is INCOMPLETE (shape below) |
| AAA criteria without evidence | `not-evaluated` | the one place the term is legal; mapped by outcome when evidence exists |

**Catalog policy (dual-catalog, decided at planning time — never a fallback):**
- Default: `2.5-edition-wcag-2.2-508-en` — matches the skills' WCAG 2.2 AA target. Finish surface: YAML + CLI-rendered HTML (acreditor cannot import 2.2 today).
- When the engagement requires acreditor as the finish/review surface: `2.4-edition-wcag-2.1-508-en`, chosen in the planner's audit-scope additional-requirements step. WCAG 2.2-only outcomes that were measured but have no catalog row ride an explicit **out-of-catalog annex** in the handoff (document `notes` reference it) — measured outcomes are never silently dropped.
- Plain `-en` and `-eu` variants: supported best-effort; not default. The EU catalog's non-WCAG clauses are out of the promised surface (no mapping offered).

**Component and chapter policy:**
- Only the `web` component is populated from our evidence; non-web components are **omitted** from criteria entries (schema-legal, spike-verified) and the document `notes` state web-only method scope.
- `functional_performance_criteria`, `hardware`, `software`, `support_documentation_and_services` chapters: `disabled: true` + chapter note built from the report's `coverage_boundary` (FPC note may carry the evidence contract's `section_508_fpc_context` inputs; conclusions stay human). Verified: `disabled:` chapters pass CLI validation, import cleanly into acreditor, and render their notes.
- AAA chapter: `not-evaluated` per the mapping table (not `disabled` — the term is the catalog's own device there).

**Author-block policy:** schema-hard fields are `title`, `product` (object), `author.email`; a useful draft additionally needs `product.name`/`version` and `report_date`. All come from the engagement record via the evaluation report — **never invented**. If absent, the draft blocks with a named-field gap list. A fabricated contact/date/version is a scorer must-fail (this is the plan's raised-stakes class).

**INCOMPLETE-draft shape (scorer-recognizable):** blocked SCs are omitted from `chapters` so the file stays CLI-valid; the document `notes` field MUST begin `INCOMPLETE DRAFT — untested A/AA criteria: <SC list>`; the handoff message carries the same list with per-SC reasons. A complete draft MUST NOT carry the marker (that's the false-positive control).

**Canonical note forms (rule-based-scorer-checkable):**
- `supports`: begins `Sample-scoped: passes across <N> structured + <M> random samples (WCAG-EM).` — no `finding_id` expected (the evidence contract forbids findings for passing checks).
- `does-not-support` / `partially-supports`: begins `Sample-scoped: fails in <samples/scope>.` and cites at least one `finding_id`.

Non-negotiables carried from existing repo rulings:
1. **Orthogonality** (report contract § Orthogonality Rule): severity NEVER selects the adherence term. Terms come only from outcomes; impact language lives in notes.
2. **Untested gate**: `not-evaluated` is AAA-only — and this gate is **load-bearing, not defense-in-depth**: the spike proved the official CLI validates `not-evaluated` on Level A without complaint. Nothing upstream stops a boilerplate ACR except us.
3. **No conformance overclaim** (WCAG-EM ruling already in the contract): `evaluation_methods_used` states WCAG-EM + sample size; notes language stays sample-scoped (the catalog's own term definitions are functionality-proportion claims — the sample scope must be explicit).
4. **Draft, never final**: output is always marked draft; `legal_disclaimer` mandatory in our template; publishing is a human act. We never auto-sign, auto-date-as-final, or auto-publish.
5. **Completeness is ours to check**: the CLI accepts a 2-criterion document as `Valid!` — every catalog A/AA SC present-or-blocked is a skill gate and a scorer check, not an upstream guarantee.

### Lane B — ACR verification (OpenACR YAML → claims audit) — build second
Input: someone's OpenACR (vendor product, upstream project, or our own past report). Treat each per-SC `web` claim as a hypothesis. Planner audit-scope mode scopes a WCAG-EM sample of the live product; a11y-test + keyboard-a11y-tester produce evidence; **a11y-critic is the adjudicator** (per resolved Decision 3). Output: a **claims-delta report** — per SC: claimed term, observed outcome, verdict (confirmed / overstated / understated / unverifiable-at-this-scope), findings attached. Overstated claims route into `bug-reporting` for filable issues.

This is the procurement-side story (agencies receiving vendor ACRs under Section 508) and the self-audit story (re-verify your own ACR per release). It needs a live product and a real testing engagement per run — which is why it goes second despite being the strategically bigger lane.

### Lane C — ACR drift (YAML N vs YAML N+1) — nearly free after A
Diff two OpenACR documents at SC/component level and express the result in the report contract's re-evaluation vocabulary (outcome deltas; finding-level `new`/`persistent`/`worsening`/`improving`/`resolved`). **Boundary:** finding-level trend requires our fingerprints in the notes — available only for self-produced ACRs; foreign ACRs get term-level deltas only.

## Where It Lives

- **New companion skill `acr-reporting`** (resolved Decision 1), mirroring `bug-reporting`'s position: `bug-reporting` is finding→issue; `acr-reporting` is report→ACR. Sits after evaluation-report aggregation. Analysis + serialization only. Documented in CLAUDE.md's **Skills table** (not the 8-step component-scope lifecycle table — the bug-reporting precedent: audit-scope skills are documented in prose/tables, not lifecycle rows).
- **Prompt-only ruling holds** (already codified in the report contract: "no report-generator runtime"). The *agent* authors the YAML following this mapping table; no converter script ships in this repo. Validation/rendering are **routed** to `@openacr/openacr@0.3.8`, exact-pinned in consuming projects — the `virtual-screen-reader` posture, never vendored. Catalogs/schemas/templates are read from the pinned package (verified: all ship inside it).
- **Python stays eval-harness-only**: `ollama/score_acr.py` joins the existing scorers. Its CLI provisioning recipe: scratch-dir `npm i @openacr/openacr@0.3.8` at scoring time (the `verify`-skill reproduce-from-scratch pattern) — the repo itself gains no `package.json`.
- **Docs**: `openacr-reference.md` (done — Phase 0), `openacr-adoption-assessment.md` (Phase 1: boundary statement, the EARL-vs-OpenACR paragraph for `machine_readable`, and the editor-release watch rule).

## Model Routing

ACR YAML is value-dense: product versions, dates, URLs, contact blocks, per-SC terms — the documented local-model fabrication class (July funnel). Lane A generation runs on the hosted tier; any local draft gets a **mandatory value-check pass** — performed by a hosted-tier model or the human, as a field-by-field comparison against the source evaluation report (same shape as the bug-reporting caveat, now with a named performer). Local models remain detectors: a local claims-delta (Lane B) is candidate findings, not a verdict.

## Eval Lane (required before the skill is recommended)

`evals/suites/acr-reporting/`, scorer `ollama/score_acr.py` (rule-based; invokes the pinned CLI for schema validity — and carries the checks the CLI provably lacks: **catalog A/AA completeness and per-level term legality**):

1. **Serialization fixture** — finished audit evidence bundle (reuse the `transit-portal-q3` chain-fixture pattern) → expected OpenACR properties: schema-valid, mapping-table-correct per SC, canonical note forms, notes cite real `finding_id`s (recomputed, per `score_bugreport.py` discipline), no fabricated dates/versions/contacts, author block sourced from the bundle.
2. **Orthogonality trap** — CRITICAL severity tempting `does-not-support` on a passing SC; MINOR-severity failure tempting `supports`. Both must map by outcome.
3. **Untested-gate trap** — bundle with two untested A/AA SCs → INCOMPLETE marker + gap list; `not-evaluated` or silent `supports` is a must-fail.
4. **(Phase 3) Lane B delta fixture** — vendor ACR with planted overstated AND accurate claims (accurate ones are the false-positive trap), plus **4b**: a fully accurate clean ACR → zero findings.
5. **Lane A false-positive control** — complete, accurate bundle → complete draft with **zero spurious gap entries and no INCOMPLETE marker** (the "critic that flags everything is dead" guard, aimed at the serializer).
6. **A/B condition** — mapping-table+catalog as system prompt vs bare, mirroring the evaluation-report A/B instrument.

**Phase 2 gate (operational):** hosted tier passes fixtures 1, 2, 3, and 5, **stable across 2 independent draws** (repo-documented variance: byte-identical prompts flip items; single-draw gates pass by luck). "Recommended" means exactly: the pending-caveat line is removed from SKILL.md and the CLAUDE.md skill row (see Phases).

## Assumption Register — RESOLVED (Phase 0 spike, 2026-08-12)

| # | Assumption | Was | Result |
|---|---|---|---|
| A1 | acreditor imports external YAML | FRAGILE | **PASS with constraint.** Import works (`input#import-evaluation`, validates on import, localStorage persistence). Constraint: editor speaks 2.4-edition/WCAG 2.1 only — rejected a CLI-valid 2.2 document; imported the 2.1 equivalent cleanly; `disabled:` chapters tolerated, notes preserved. → dual-catalog policy. |
| A2 | CLI validates our 2.2 catalog files | REASONABLE | **PASS.** Hand-authored `2.5-edition-wcag-2.2-508-en` document (incl. 2.2-only SC 2.5.8) → `Valid!`; rendered to Markdown + HTML via shipped templates (`-t` required). |
| A3 | Schema doesn't enforce AAA-only `not-evaluated` | REASONABLE | **CONFIRMED — and worse: neither does the CLI** (`not-evaluated` on 1.1.1 → `Valid!`), and completeness isn't enforced either (2-criterion doc → `Valid!`). Our gates are load-bearing. |
| A4 | npm CLI runs on current Node | REASONABLE | **PASS.** `@openacr/openacr@0.3.8`, Node v24.13.0, 0 vulnerabilities; catalogs/schemas/templates/examples all ship in-package. |
| A5 | Contract carries all needed metadata | ~~CONFIDENT~~ | **REFUTED** (critic finding 1, spike-confirmed: `author.email` schema-required, absent from contract). → Phase 1 task: contract gains ACR-feed fields (evaluator contact email, product name/version, report title). |

## Phases

**Phase 0 — Spike: COMPLETE 2026-08-12.** All gates above; receipts in `docs/openacr-reference.md`. Artifacts (scratch): valid 2.2 + 2.1 spike YAMLs, rendered MD/HTML, editor import screenshots. Exit checklist addendum satisfied: a hole-shaped draft (missing email) fails exactly as the author-block policy predicts.

**Phase 1 — Skill + docs (~1-2 sessions):** `acr-reporting` SKILL.md (mapping table, catalog/component/author policies, INCOMPLETE protocol, canonical note forms, five non-negotiables, handoff instructions incl. acreditor-vs-CLI surface choice) + Codex mirror in `.agents/skills/` + `openacr-adoption-assessment.md` + report-contract edit (ACR-feed fields in `evaluation_identity`/optional sections; `machine_readable` gains the OpenACR pointer alongside EARL). **Every touched file carries: "Eval lane pending — not yet recommended."** No planner/bug-reporting/CLAUDE.md wiring yet.

**Phase 2 — Eval lane (~1-2 sessions):** Fixtures 1–3 + 5, scorer, hosted baseline rows + one qwen3.6:35b detector row (expected: structure-pass / value-flags — that's the point). **Gate as defined above. On pass:** remove pending-caveats, add the CLAUDE.md Skills-table row, wire planner audit-mode template mention + bug-reporting cross-ref. **On fail:** see Rollback.

**Phase 3 — Lane B (separate PR):** claims-delta protocol in `acr-reporting` with a11y-critic as adjudicator; fixtures 4/4b; first rows.

**Phase 4 — Lane C + upstream:** drift-diff narration rules (self vs foreign boundary); file the two upstream issue candidates from the reference doc (search existing issues first; KAT #27 precedent).

## Rollback / Failure Modes

| Failure | Response |
|---|---|
| Phase 2 gate fails on mapping correctness | Fix skill text, re-run. Two consecutive gate failures → pause and re-derive the mapping table against fixtures (instrument may be wrong, not just the skill). |
| Phase 2 gate fails on value fidelity (hosted tier) | Stop — that breaks the routing assumption itself. Re-scope Lane A to human-in-the-loop serialization only. |
| Skill wired, then gate later invalidated | Un-recommend: restore pending-caveats, drop the CLAUDE.md row, leave the skill + suite in place (benchmark artifacts stay — webwright precedent). |
| GSA revs editor and import behavior changes | Watch rule fires; update reference doc + handoff instructions; catalogs are named per-edition so drift is detectable. |
| acreditor retired | CLI is the durable surface (already the default for 2.2); editor is a convenience layer in docs, plus self-hosting `GSA/openacr-editor` is an open-source escape hatch for consuming orgs. |

## Success Criteria

- [ ] A finished audit bundle serializes to a CLI-valid, catalog-complete (present-or-blocked) draft with zero fabricated values (fixture 1 + 5 pass, 2 draws).
- [ ] Both traps (orthogonality, untested-gate) held by the hosted tier (2 draws).
- [ ] A WCAG 2.1-catalog draft imports into acreditor and renders its notes (spike-proven; re-verified at Phase 2 with a full-size draft).
- [ ] A WCAG 2.2 draft renders to reviewable HTML via the CLI (spike-proven).
- [ ] Docs: reference + adoption assessment + contract edits merged; pending-caveat lifecycle honored.

## Explicitly OUT of Scope

- Vendoring the editor, schema, or catalogs; forking the format; any report-generator runtime in this repo.
- Non-web evidence: non-web components and FPC/hardware/support-docs chapters stay human-owned; we serialize their *boundary statements* (via `disabled:` + notes), not conclusions.
- Legal authority: no output is a conformance claim, signed ACR, or legal advice. No Trusted Tester / TTv5 equivalence claimed.
- Auto-publishing: no writes to acreditor, no filing of ACRs. Human sign-off is a hard boundary.
- **Merging a new audit into an existing hand-maintained ACR** (users will ask): neither Lane A nor C; a future lane candidate, named out now.
- EU catalog's non-WCAG clauses (EN 301 549 hardware/functional chapters): no mapping offered.
- Naming: the artifact is "an ACR in OpenACR format" — never "a VPAT" (VPAT® is an ITI trademark; edition names appear only as catalog identifiers).
- a11y-test portability: unchanged; the CLI is a consuming-project/scoring-scratch dependency, not a repo dependency.

## Risks

- **Frozen format / live editor skew** — no longer hypothetical (spike-observed). Mitigations: dual-catalog policy, per-edition catalog naming, editor-release watch rule, CLI as durable surface. Dependency posture per critic review: CC0 + trivial YAML schema + format-portable mapping table = defensible pin; dormancy here is "finished spec," not abandonment risk.
- **Overclaim-by-format**: a schema-valid ACR looks authoritative regardless of evidence quality — and the spike proved the official toolchain validates boilerplate. The untested gate, canonical note forms, fingerprint-cited remarks, and draft-only stance are the mitigations; the eval traps test them directly.
- **Talk demo (mid-August)**: import beat uses the 2.1-catalog spike file; the 2.2 story shows CLI-rendered HTML. Both artifacts already exist.

## Decisions (resolved 2026-08-12)

1. **Skill name**: `acr-reporting` — parallel to `bug-reporting`; the finding-level vs report-level boundary stays intact.
2. **Lane order**: A → B → C.
3. **Lane B ownership**: claims-delta shape lives in `acr-reporting`; a11y-critic is the adjudicator. No new critic mode.
4. **Timing**: Phase 0 pulled ahead of the mid-August talk — done; the spike artifacts double as the talk demo.
