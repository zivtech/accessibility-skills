---
name: acr-reporting
description: >
  Load this skill whenever you are converting a finished audit-scope
  accessibility evaluation into an Accessibility Conformance Report (ACR) draft
  in the OpenACR format, validating or rendering OpenACR YAML, or preparing the
  handoff to GSA's ACR Editor (https://acreditor.section508.gov/). Report-level
  companion to bug-reporting: findings→issues is bug-reporting;
  evaluation-report→ACR is this skill. Output is always a DRAFT for human review
  and sign-off — never a final or signed ACR. Under no circumstances map an
  untested Level A/AA criterion to any adherence term, derive a conformance term
  from finding severity, or invent metadata values (contacts, dates, versions).
license: Apache-2.0
compatibility: Claude Code-compatible; protocol is model-agnostic
metadata:
  author: zivtech
  version: "0.1.0"
---

# ACR Reporting Skill (OpenACR)

> **STATUS: EVAL LANE PENDING — NOT YET RECOMMENDED.** This skill ships ahead of its eval suite (`evals/suites/acr-reporting/`, Phase 2 of the [integration plan](../../../docs/plans/2026-08-12-openacr-integration-plan.md)). Until the Phase 2 gate passes (fixtures 1/2/3/5, hosted tier, stable across 2 draws), treat every output as experimental and route every draft through the mandatory human handoff below. Removing this banner **is** the act of recommending the skill — it happens only at gate-pass.

> **Verified facts + receipts:** [docs/openacr-reference.md](../../../docs/openacr-reference.md) (format, schema, CLI behavior, editor behavior — all claims receipted 2026-08-12). **Boundary ruling:** [docs/openacr-adoption-assessment.md](../../../docs/openacr-adoption-assessment.md).

Apply these rules when serializing a finished evaluation into OpenACR YAML, when validating or rendering an OpenACR document, or when preparing the human handoff.

---

## Core Mandate

**An ACR is a conformance-claim document someone may publish. Every value in it must trace to the engagement record or the evidence spine.**

The official toolchain will not catch boilerplate: `openacr validate` enforces neither SC completeness (a 2-criterion document validates) nor the not-evaluated-AAA-only rule (`not-evaluated` on a Level A criterion validates) — both verified, see the reference doc. The gates in this skill are the only thing standing between "untested" and a schema-valid published overclaim.

---

## Position in the Lifecycle

- **Audit-scope only.** Input is an evaluation report conforming to the [A11y Evaluation Report Contract](../../../docs/a11y-evaluation-report-contract.md) plus its findings ([A11y Evidence Finding Contract](../../../docs/a11y-evidence-finding-contract.md) blocks). This skill is the "populate" step the report contract's Boundaries section anticipates: the contract is the internal evidence spine; OpenACR is the external report format it populates.
- **Never generate an ACR from raw findings alone.** The per-SC outcome map, sample set, and coverage boundary live in the evaluation report — without them there is nothing legitimate to serialize.
- **Component-scope reviews never produce ACRs.** The report contract already rules that an EM-shaped report at component scope is checkbox theater; an ACR at component scope is that plus a conformance claim. Treat a component-scope ACR request as a scoping error and say so.
- **Boundary with bug-reporting:** bug-reporting converts individual findings into reproducible issues (finding-level). This skill aggregates the finished evaluation into a conformance report (report-level). One feeds trackers; the other feeds procurement.

---

## Inputs Required (block if any is missing)

| Input | Source | Notes |
|---|---|---|
| Evaluation report | Contract-conformant, incl. `outcomes` per-SC EARL map, `sample_set`, `coverage_boundary`, `conformance_target`, `accessibility_support_baseline` | The spine. No report, no ACR. |
| Findings | Evidence-contract blocks with `finding_id`, `fingerprint`, `evaluation_context` (`sample_id`s) | Cited in notes. |
| Report title | Engagement record | Schema-required (`title`). |
| Product name + version | Engagement record | Schema-optional but a draft without them is useless — required here. |
| Author contact incl. **email** | Engagement record (the drafting evaluator) | `author.email` is the schema's one hard-required contact field (verified: validation fails without it). |
| `report_date` | Engagement record (evaluation completion date) | Never today's date by default — the evaluation's date. |
| Feedback channel, license, repository | Engagement record | Optional; include when the engagement publishes them. |

**Never invent any of these.** If a required input is absent, the draft **blocks** with a named-field gap list in the handoff (e.g., "Blocked: no author email in engagement record"). A fabricated contact, date, or version is the worst failure this skill can produce.

---

## Catalog Selection (decided at planning time — never a fallback)

The planner's AUDIT-SCOPE MODE collects the report template as an additional requirement; the catalog choice is made **there**, not at serialization time.

| Engagement need | Catalog | Finish surface |
|---|---|---|
| Default — WCAG 2.2 AA target (the skills' standard) | `2.5-edition-wcag-2.2-508-en` | YAML + CLI-rendered HTML. **acreditor cannot import 2.2 documents today** (verified: rejects them by criterion). |
| acreditor required as the review/finish surface | `2.4-edition-wcag-2.1-508-en` | acreditor "Open report" import (verified working). 2.2-only outcomes ride the out-of-catalog annex — see below. |
| Plain-WCAG or EU report | `2.5-edition-wcag-2.2-en` / `-508-eu-en` | Best-effort. The EU catalog's non-WCAG clauses (EN 301 549 hardware/functional chapters) have **no mapping** in this skill. |

**Measured outcomes are never dropped.** A 2.1-catalog draft from a 2.2-target evaluation carries every 2.2-only outcome in the annex.

---

## Outcome → Adherence Mapping (normative)

Outcomes use the report contract's EARL vocabulary, aggregated across the sample set. Adherence terms are the catalog's five.

| Outcome across the sample set | Adherence term | Condition |
|---|---|---|
| `passed` everywhere applicable | `supports` | Canonical sample-scope note form. |
| `failed` wherever applicable | `does-not-support` | Note states sample scope + cites `finding_id`(s). |
| Mixed pass/fail across samples or instances | `partially-supports` | Note enumerates failing `sample_id`s + cites `finding_id`(s). |
| `inapplicable` | `not-applicable` | Note states why (content type absent from product and sample). |
| `untested` or `cantTell` on any A/AA SC | **no mapping — emission blocker** | Draft becomes INCOMPLETE (protocol below). |
| AAA criterion without evidence | `not-evaluated` | The only place the term is legal. When AAA evidence exists, map it by outcome like any other SC. |

Two semantic cautions:

- The catalog's official term definitions are **functionality-proportion claims** ("Partially Supports: *Some* functionality … does not meet"; "Does Not Support: *The majority* of product functionality does not meet"). Our evidence is **sample-scoped**. The deterministic mapping above is correct, but every `does-not-support` and `partially-supports` note must carry its sample scope explicitly so the reader can see what the claim rests on.
- **Severity never selects the term** (report contract § Orthogonality Rule). A CRITICAL finding on a passing SC does not downgrade `supports`; a MINOR-severity failure does not soften `does-not-support`. Impact language belongs in notes; terms come only from outcomes.

---

## Chapter & Component Policy

- **Populate only the `web` component** from our evidence. Omit non-web components (`electronic-docs`, `software`, `authoring-tool`) from criteria entries entirely — schema-legal and verified. The document `notes` state the method's web-only scope.
- **508 chapters** (`functional_performance_criteria`, `hardware`, `software`, `support_documentation_and_services`): set `disabled: true` with a chapter note built from the report's `coverage_boundary` (what the web measurement stack could not measure, and what covered it instead — or that nothing did). The FPC note may carry the evidence contract's `section_508_fpc_context` inputs; **conclusions in these chapters stay human**. Verified: `disabled:` chapters pass CLI validation and import into acreditor with their notes rendered.
- **AAA chapter**: `not-evaluated` per the mapping table — the catalog's own device, not `disabled:`.

---

## Canonical Note Forms (machine-checkable — the eval scorer greps these)

| Term | Note MUST begin | Then |
|---|---|---|
| `supports` | `Sample-scoped: passes across <N> structured + <M> random samples (WCAG-EM).` | Optional context. **No `finding_id`** — the evidence contract forbids findings for passing checks. |
| `does-not-support` / `partially-supports` | `Sample-scoped: fails in <sample_id list or scope>.` | At least one `finding_id` (with `fingerprint` where useful for trend). `partially-supports` enumerates failing `sample_id`s. |
| `not-applicable` | `Not present:` | Why the content type is absent. |
| `not-evaluated` (AAA only) | `Not evaluated at this engagement's conformance target (WCAG 2.2 AA).` | — |
| `disabled:` chapter note | `Outside the web evaluation method's coverage:` | The `coverage_boundary` statement. |

`finding_id`s make the ACR a living document — the Drupal OpenACR precedent uses per-remark issue links; our fingerprints formalize the same practice and enable Lane C trend diffs on re-evaluation.

---

## INCOMPLETE Drafts (the untested gate — load-bearing)

- Any A/AA SC with outcome `untested` or `cantTell` gets **no adherence entry** — the SC is omitted from `chapters` so the file stays CLI-valid.
- The document `notes` field MUST begin: `INCOMPLETE DRAFT — untested A/AA criteria: <comma-separated SC numbers>`.
- The handoff message carries the same list with a per-SC reason (not sampled / tooling gap / ran out of scope) so the human can commission the missing testing.
- **`not-evaluated` on an A/AA criterion is forbidden even though the CLI accepts it** (verified it does; the catalog's own term text restricts it to AAA). Emitting it is a must-fail.
- A complete draft MUST NOT carry the INCOMPLETE marker — spurious gap entries on complete evidence are the serializer's version of a critic that flags everything.

---

## Out-of-Catalog Annex (2.1-catalog drafts only)

When the evaluation targeted WCAG 2.2 but the draft uses the 2.4-edition/2.1 catalog (acreditor surface):

- Document `notes` include: `Out-of-catalog annex: <n> WCAG 2.2-only criteria measured under conformance target WCAG 2.2 AA — see handoff annex.`
- The handoff annex lists each 2.2-only SC (2.4.11, 2.4.12, 2.4.13, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8, 3.3.9 as applicable) with its outcome, would-be term, and `finding_id`s.

---

## Serialization Procedure

1. **Verify inputs** against the block list. Missing input → stop, emit the named-field gap list.
2. **Select the catalog** from the engagement record's report-template requirement (never guess; never downgrade silently).
3. **Build the metadata block** field-by-field from the engagement record: `title`, `product`, `author` (with email), `report_date`, `evaluation_methods_used` (MUST state WCAG-EM + sample size: e.g., "WCAG-EM 2.0; 12 structured + 2 random samples + 2 complete processes"), and a **mandatory `legal_disclaimer`** carrying draft language (e.g., "Draft for review — not a legally binding conformance claim until reviewed and issued by <owner>").
4. **Map every A/AA SC in the catalog** — present with a term + canonical note, or blocked into the INCOMPLETE list. Work from the catalog's criterion list, not from the findings list (findings only exist for failures; the catalog is the completeness frame).
5. **AAA chapter and disabled chapters** per the chapter policy.
6. **Self-check completeness**: every catalog A/AA SC accounted for (present-or-blocked). The CLI will not check this — you must.
7. **Validate** via the routed CLI (below). Fix schema/catalog errors; never "fix" by inventing values.
8. **Render** with `openacr output` (`-t` is required — the CLI errors without a template): Markdown for review diffs, HTML for the human read.
9. **Write the handoff message**: finish surface, review checklist, INCOMPLETE list (if any), annex (if any), and the draft/never-final statement.

---

## Validation & Rendering (routed, never vendored)

Exact-pin **`@openacr/openacr@0.3.8`** (frozen upstream; CC0). Consuming projects add it as a devDependency; for ad-hoc runs use a scratch directory:

```bash
mkdir -p /tmp/acr-check && cd /tmp/acr-check && npm init -y >/dev/null && npm i @openacr/openacr@0.3.8
npx openacr validate -f draft.yaml -c node_modules/@openacr/openacr/catalog/<catalog-id>.yaml
npx openacr output -f draft.yaml -c node_modules/@openacr/openacr/catalog/<catalog-id>.yaml \
  -t node_modules/@openacr/openacr/templates/openacr-html-0.1.0.handlebars -o draft.html
```

**Always pass `-c` — on both commands.** Neither command loads the document's
own `catalog:` field (Phase 2, reproduced): `validate` without `-c` is
schema-shape only and accepts nonexistent criterion numbers; `output`
without `-c` exits successfully and silently renders a metadata-only shell
with zero criteria tables. A bare `validate -f` is no validation at all, and
a rendered HTML must be checked to actually contain its criteria tables
before it is circulated.

Catalogs, schemas, and templates all ship inside the package — reference them from `node_modules/@openacr/openacr/`, never copy them into a repo.

| The CLI checks | The CLI does NOT check (skill self-checks) |
|---|---|
| YAML/schema shape; `author.email` present | A/AA completeness (step 6) |
| Criterion numbers exist in the catalog — **only with `-c`** | `not-evaluated` restricted to AAA (INCOMPLETE protocol) |
| Term strings are catalog terms — **only with `-c`** | Term appropriateness vs outcomes; note forms; value provenance |
| — | An absent `license` (the schema assumes **CC-BY-4.0** "in any output" — a withheld license must be surfaced in the handoff as a decision the owner still owes, never treated as safely empty) |

---

## Handoff (mandatory human steps — every draft, every time)

**2.1-catalog drafts (acreditor surface):** the human opens https://acreditor.section508.gov/ → "Open report" → selects the YAML. Verified behavior: the editor validates on import, renders chapter notes, drops `disabled:` chapters from progress, and stores everything in browser localStorage only — the saved YAML file is the persistence mechanism, nothing is uploaded to a server. The human reviews every chapter, adds non-web component conclusions where they hold evidence, completes contact/legal review, and exports.

**2.2-catalog drafts:** the human reviews the rendered HTML + YAML directly (acreditor cannot import them today — reference doc, watch rule). Edits go into the YAML; re-validate after.

**The human owns:** sign-off, publication, removal of the draft disclaimer, the license decision (an absent `license` renders as CC-BY-4.0 by the schema's own default — say so in the handoff whenever the engagement record withholds one), and every conformance statement made to a third party. This skill never auto-publishes, never auto-signs, never emits a final ACR, and never writes to acreditor.

---

## Model Routing

ACR YAML is value-dense (contacts, dates, versions, per-SC terms) — the documented local-model fabrication class. **Generation runs on the hosted tier.** Local models are detectors only; any locally-produced draft requires a mandatory **field-by-field value-check pass** — performed by a hosted-tier model or the human — comparing every metadata value and every term against the source evaluation report before validation counts for anything.

---

## Five Non-Negotiables

1. **Orthogonality** — terms from outcomes only; severity lives in notes.
2. **Untested gate** — no term for untested A/AA; `not-evaluated` is AAA-only; the gate is load-bearing because the CLI provably doesn't enforce it.
3. **No conformance overclaim** — WCAG-EM + sample size stated; sample-scoped language throughout; sampling alone never supports a whole-product conformance claim (report contract rule).
4. **Draft, never final** — `legal_disclaimer` mandatory; publishing is a human act.
5. **Completeness is ours to check** — every catalog A/AA SC present-or-blocked; the CLI accepts fragments.

---

## Boundaries

- **Not yet in this skill:** claims verification of third-party ACRs (Lane B — Phase 3, adjudicated by a11y-critic), ACR drift diffs (Lane C — Phase 4), and merging a new audit into an existing hand-maintained ACR (explicitly out of scope; say so when asked).
- **Naming:** the artifact is "an ACR in OpenACR format" — never "a VPAT" (VPAT® is an ITI trademark; VPAT edition names appear only inside catalog identifiers).
- **Non-web conclusions are human-owned.** This skill serializes their boundary statements, never their conclusions.
- **No report-generator runtime** in the skills repo (existing contract ruling): the agent authors the YAML per this skill; validation/rendering route to the pinned CLI.

---

## Pre-Handoff Quality Checklist

* [ ] Every catalog A/AA SC is present with a term or named in the INCOMPLETE list
* [ ] No `not-evaluated` outside the AAA chapter
* [ ] Every term traceable to the outcome map — no severity-derived terms
* [ ] Every `does-not-support`/`partially-supports` note cites ≥1 real `finding_id` and states sample scope
* [ ] Every `supports` note uses the canonical sample-scope form
* [ ] Metadata values traced to the engagement record — zero invented values
* [ ] `evaluation_methods_used` states WCAG-EM + sample size
* [ ] `legal_disclaimer` present with draft language
* [ ] Disabled chapters carry `coverage_boundary` notes
* [ ] 2.1-catalog drafts: out-of-catalog annex present when 2.2-only outcomes exist
* [ ] `openacr validate` passes on the exact file being handed off
* [ ] Rendered HTML produced and attached to the handoff
* [ ] Handoff message names the finish surface and the human-owned steps

---

## References

- [OpenACR verified reference](../../../docs/openacr-reference.md) — receipts for every format/CLI/editor claim above
- [Integration plan](../../../docs/plans/2026-08-12-openacr-integration-plan.md) — lanes, eval design, phase gates
- [A11y Evaluation Report Contract](../../../docs/a11y-evaluation-report-contract.md) / [A11y Evidence Finding Contract](../../../docs/a11y-evidence-finding-contract.md)
- [GSA/openacr](https://github.com/GSA/openacr) · [GSA/openacr-editor](https://github.com/GSA/openacr-editor) · [ACR Editor (live)](https://acreditor.section508.gov/)
- [WCAG-EM 2.0 reference](../../../docs/wcag-em-2-reference.md) — the methodology the evaluation report cites
