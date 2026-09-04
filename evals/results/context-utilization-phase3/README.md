# Context-Utilization Phase 3 — Evidence-Volume Lane

> **2026-08-26: rows run and adjudicated — results in `RESULTS-2026-08-26.md`**
> (local 72 scored + 2 OVERFLOW receipts, hosted 48, opus content adjudication,
> P1/P1b/P2/P3 folded against the registered thresholds). This README remains the
> lane's design record.

**Status: DRAFT — REVISE fixes applied 2026-08-25, pending bench-reviewer
RE-verification.** First gate verdict: REVISE, 6 blocking findings (F1–F6) + 6
non-blocking (F7–F12) + rulings on ambiguities 1–6 —
`docs/plans/2026-08-25-context-utilization-phase3-gate-review.md`. F1–F5 and F7–F12
fixed here (disposition table appended to that doc); F6 (the runner) owned and built by
a separate agent (`ollama/run_evidence_lane.py`), coordinated directly (§9.5, §11).
Fixes are **self-reported, not yet independently re-verified** — per this team's own
practice, a fixer's "applied and verified" is not a substitute for the same
reviewer/critic re-checking the diff; that re-verification is the next gate, not this
one. Nothing in this directory beyond this README, `lane_manifest.yaml`, and the
runner-builder's file has been built. No packs exist, no model rows have been run,
nothing here is committed. Per the plan's Phase 3 gate: *"lane design + scorer reviewed
by bench-reviewer (opus, high) before packs; packs + completeness audit committed
before rows; results README before any routing-guidance change."*

**Date:** 2026-08-25. **Branch:** `feat/verification-evidence-contract`. **Authoring
agent:** teammate delegate, sonnet, per team-lead task assignment (Phase 3 lane design
+ scorer only — no packs, no rows, no commits; see task constraints below).

**Plan reference:** `docs/plans/2026-08-24-context-utilization-plan.md`, §6 Phase 3
(lines 102–147). This document follows that spec section-by-section and quotes its
predictions/decision rules verbatim rather than paraphrasing them. Supporting reads:
`.claude/agents/a11y-evidence-reader.md` (the blind curator this lane measures),
`docs/a11y-evidence-finding-contract.md`, `evals/results/context-utilization-phase2/README.md`
(the Phase 2 worked-example receipt this lane's pack construction must exercise two
untested cases from — §9 below).

**What this document is not:** a decision about whether curation helps. That's the
lane's *output*, produced only after packs are built, frozen, audited, and scored. This
document is the design the bench-reviewer approves before any of that work starts.

**Revision note (2026-08-25, same day):** two orchestrator addenda folded in after the
first draft: (1) four binding rules from the Phase 2 post-ship review (GAPS-FOUND),
being written into the plan itself in parallel — question-provenance, a question
template, a re-curation gate, and a named pack-construction precondition (§9.1, §9.2,
§10); (2) real `num_predict=1` protocol-token probes for both local models, which
supersede §4's plan-copied estimates and surface a ceiling risk for qwen3:32b's DUMP@49K
cell that this document presents but does not resolve (§4).

---

## 0. Scope (unchanged from plan)

Critic suite only. Planner/evalreport/perspective fixtures are out of scope for this
lane (plan §6 Phase 3 "Scope"; planner protocol leaves no local context budget, and
audit-chain fixtures grade evidence aggregation itself — a curated digest would leak
part of the graded task). Perspective inherits conclusions directionally only.

## 1. Question under test (verbatim)

> Does curated, contract-shaped evidence beat raw-dump evidence on finding accuracy —
> and is any local effect dilution (payload) or fit (num_ctx)?

---

## 2. Fixture selection

### 2.0 The critic suite, enumerated

`evals/suites/a11y-critic/fixtures/` (Glob-verified 2026-08-25: 41 `.md` + 41
`.metadata.yaml`, one pair per fixture — matches `ollama/run_benchmark.py`'s
`ALL_CRITIC_FIXTURES` constant exactly, cross-checked against the raw directory
listing, not just the Python source). **Flagging one factual correction to the task
brief:** the brief describes "~33 fixtures" — that was accurate as of the 2026-07-10
keyboard-a11y-tester (KAT) cross-validation (`evals/results/keyboard-a11y-tester/README.md`
line 6: "all 33 a11y-critic eval fixtures"), but six more were added 2026-08-14 (the
"remediated-code-with-residue" batch named in CLAUDE.md). The suite is **41 fixtures**
today. None of my six picks below are from the newer batch, so this doesn't change the
selection, but it matters for §3: the real committed KAT artifacts I'm reusing cover
only the original 33.

| Tier | Fixtures (41 total) |
|---|---|
| CLEAN (6) | `button-skip-link-clean`, `interactive-dropdown-clean`, `modal-complete-clean`, `search-results-dynamic-clean`, `trail-conditions-filter`, `pool-lesson-registration` |
| HAS-BUGS (27) | `form-validation-missing-aria-describedby`, `tabs-missing-arrow-nav`, `toast-notification-no-role`, `accordion-no-region-role`, `breadcrumb-navigation-no-nav-landmark`, `checkbox-group-no-fieldset`, `combobox-autocomplete-no-listbox-role`, `data-table-missing-scope`, `expandable-section-no-button`, `file-input-no-labels`, `heading-hierarchy-skipped`, `image-carousel-no-region`, `infinite-scroll-no-announcement`, `interactive-dropdown-focus-bug`, `loading-state-missing-aria-busy`, `megamenu-no-structure`, `pagination-no-nav-landmark`, `popover-no-focus-management`, `radio-button-group-no-grouping`, `tooltip-no-role-no-association`, `video-player-missing-captions`, `rehearsal-schedule-panel`, `seed-availability-panel`, `slip-reservation-tabs`, `filing-progress-controls`, `tool-catalog-layout`, `garden-plot-directory` |
| FLAWED (5) | `tabs-incomplete-aria-selected`, `multistep-form-error-clearing`, `dashboard-heading-inconsistency`, `app-focus-order-illogical`, `async-form-vague-success` |
| ADVERSARIAL (3) | `tabbed-nav-vs-tab-pattern`, `form-field-vs-summary-errors`, `search-focus-stays-in-input` |

### 2.1 Chosen fixtures

The plan fixes `button-skip-link-clean` as one of the two CLEAN fixtures and requires
≥2 buggy fixtures with axe-detectable evidence, ≥2 with keyboard-trace evidence, from a
total of 4 buggy + 2 CLEAN. I chose an exact 2×2 split (no ambiguous overlap fixture)
so the axe/keyboard evidence-class assignment is unambiguous for pack construction and
for the completeness-audit partition in §10.

**A note on how "evidence class" was derived.** No fixture `.metadata.yaml` in this
suite tags an evidence class — that field doesn't exist in the schema (confirmed by
reading 12 metadata files across HAS-BUGS/CLEAN tiers). Per the task brief's fallback
instruction, I derived evidence class from fixture content, checked against two
independent real-world sources rather than my own judgment alone: (a) the actual axe-core
rule surface I know to be component-scoped and stable (`heading-order`, `label`) versus
rules that require page-level landmark context or don't exist for a given defect class,
and (b) `evals/results/keyboard-a11y-tester/README.md`'s own **already-completed**
cross-validation of this exact suite against real KAT deterministic-layer output — which
independently confirms or refutes several of my axe-detectability judgments (cited
per-fixture below). Where I could not find external confirmation, I say so rather than
asserting confidence I don't have.

#### CLEAN #1 — `button-skip-link-clean` (fixed by plan)

Not my choice; no runner-up applicable. Skip link + nav/main/footer landmark shell,
0 must-finds. Notable for pack construction: it's the **only** one of my six fixtures
whose JSX already renders a full page shell (nav/main/footer), so page-level axe rules
(landmark, bypass) can fire meaningfully on it without a synthetic wrapper — see §3.
Real batch-crawl KAT findings already exist for it
(`evals/results/keyboard-a11y-tester/findings/button-skip-link-clean.json`) and the KAT
README's false-positive analysis section does **not** list it among the fixtures with
FP or rendering-artifact caveats — a clean, uncaveated real result.

#### CLEAN #2 — `modal-complete-clean` (chosen)

Complete WAI-ARIA Modal Dialog pattern (focus trap, restoration, Escape, correct
ARIA). Chosen because it is the **only** CLEAN candidate with a real, already-committed
**driven** keyboard-a11y-tester trace (`evals/results/keyboard-a11y-tester/driven/modal-complete-clean.trace.json`
+ `.findings.json`, 2026-07-10) in addition to batch-crawl findings — meaning both the
axe-adjacent and keyboard-trace raw-evidence sourcing for this fixture are already real,
committed, previously-validated artifacts rather than new tool-executions. The KAT
README's driven-sessions table confirms the trace is unambiguously clean: *"Enter →
focus lands on 'Close dialog' inside modal; Tab cycles Save↔Close (trap holds); Escape
→ focus restored to 'Open settings'. Clean verdict, no false-alarm material."* This
mirrors the buggy set's 2-axe/2-keyboard split with a CLEAN fixture that has real
interaction evidence to curate or dump, and its 2026-07-16 fixture-notes revision
history (two real defects found by an opus-tier critic run and fixed at source, with
counts unchanged) is itself a receipt that this fixture has been adversarially poked at
and genuinely holds up as a true negative — the strongest such evidence among the 6
CLEAN candidates.

**Runner-up rejected:** `interactive-dropdown-clean`. Thematically it would pair
neatly with `interactive-dropdown-focus-bug` (a minimal-pair design), and it is CLEAN
with real batch-crawl findings — but it has **no committed driven trace**
(`driven/` contains only 6 fixtures; `interactive-dropdown-clean` isn't one of them), so
its keyboard-trace raw evidence would require a fresh tool execution rather than reuse
of an already-validated artifact. Under the plan's effort constraint ("pack construction
≈ 1–2 focused sessions") and the general preference for lower execution risk in a
lane the kill-rule can shrink but must not stall, `modal-complete-clean`'s ready-made
real trace was decisive.

#### Buggy, axe-detectable #1 — `heading-hierarchy-skipped`

h1→h3→h1→h2 heading-level skips, 2 must-finds, both structural (WCAG 1.3.1). This is
the **cleanest** axe pick in the suite: axe-core's `heading-order` rule is a stable,
long-standing, component-scoped check (it needs only the heading sequence, not a page
landmark shell) that fires exactly on this defect class. This is not just my own
inference — `evals/results/keyboard-a11y-tester/README.md` independently confirms it:
KAT's deterministic layer (AX-tree-based, a different mechanism than axe-core's DOM
rules but detecting the same structural fact) is reachable on only 3 of 68 suite-wide
must-finds, and **both of the 2 it actually catches are this exact fixture's heading
skips**, flagged as `sr-heading-skip` (1.3.1) — "*The second one matters: the fixture
styles h2 and h3 identically so the skip is invisible on screen; the census catches it
structurally*" (README line 57-58, re: the sibling fixture `dashboard-heading-inconsistency`,
which shares the same defect class). Component-scoped rendering (no page shell needed)
also sidesteps the rendering-artifact risk documented in §3.

**Runner-up rejected:** `data-table-missing-scope` (missing `scope="col"`/`scope="row"`
on table headers, 2 must-finds MAJOR). I could not confirm a reliable, stable axe-core
rule that fails on scope-attribute *absence* alone on a simple two-dimensional table —
browsers/AT can often still infer header association heuristically, so a real axe run
risks returning a clean or near-empty result despite the finding being real. This
uncertainty is resolved by the same KAT cross-validation cited above: its own
pre-registered classification lists table-header-scope explicitly **out of scope**
("*Out of KAT's declared scope: 5 of 68 (video captions ×3, table header scope ×2)*",
README line 41) — independent, already-published evidence from this repo that this
defect class is not reliably machine-detectable, which is exactly the risk I was
guarding against. Selecting it as an "axe-detectable" representative would risk an
ecologically invalid pack (empty or near-empty real tool output next to a real
REVISE-worthy finding).

#### Buggy, axe-detectable #2 — `file-input-no-labels`

Missing `<label>`, missing `aria-describedby`/`aria-invalid` on error, unannounced
file-type restriction — 4 must-finds, only the first (missing `<label>`, CRITICAL) is a
clean single-rule axe hit; the other 3 require source-code/interaction evidence that
the fixture's own JSX (always fully visible to the critic in both conditions) already
supplies, independent of the evidence pack. I chose this fixture *because* it is
mixed, not despite it: it's a realistic test of whether pack volume dilutes attention to
the one item the pack *can* corroborate, without inflating the axe-detectable bucket
with an over-clean fixture. Confirmation, again from the KAT cross-validation rather
than my own assertion alone: KAT's root-cause section explicitly names this exact
defect "*a label-association defect axe-core catches statically*" (README line 64),
after tracing why KAT's own AX-tree check missed it (Chromium gives `<input type="file">`
an intrinsic UA-provided name, "Choose File", masking the missing-label defect from a
pure name-presence check — axe-core's `label` rule, which checks for an explicit
programmatic label association rather than AX-tree name presence, still catches it).

**Runner-up rejected:** `radio-button-group-no-grouping` (and its near-twin
`checkbox-group-no-fieldset`) — missing `<fieldset>`/`<legend>` to group related
controls, 2 must-finds CRITICAL. Rejected because the group-*relationship* gap is
invisible to per-control axe rules: each individual radio/checkbox already has a
working `<label>` via `htmlFor` (confirmed in the fixture's own metadata: "Labels and
name present but group context missing"), so axe's `label` rule would **pass** on every
control while the real defect (no semantic grouping) goes undetected — a pattern-
completeness judgment that needs source review or APG-pattern knowledge, not a
machine-detectable signal. Picking it would mislabel a source-review-class fixture as
axe-detectable.

#### Buggy, keyboard-trace #1 — `tabs-missing-arrow-nav`

Tabs widget with correct ARIA but no arrow-key cycling — 1 must-find MAJOR (WCAG 2.1.1),
1 should-find (focus not moved to newly active tab). Pure interaction defect: axe cannot
see it (static DOM inspection can't observe keyboard-event-handler behavior). Chosen
because it already has a **real, committed driven trace**
(`evals/results/keyboard-a11y-tester/driven/tabs-missing-arrow-nav.trace.json` +
`.findings.json`, 2026-07-10) that proves the defect directly and unambiguously — KAT's
own driven-sessions table: *"On `[role=tab]`: ArrowRight → `focus_moved=false`;
ArrowLeft → `focus_moved=false`"* (README line 102). Single-mechanism, single must-find,
low adjudication surface — a clean representative of the class.

**Runner-up rejected:** `popover-no-focus-management` (5 must-finds: focus not moved
in, not restored on close, missing `role="dialog"`, missing `aria-modal`, missing
`aria-labelledby`). It also has a real committed driven trace and would be a strong
keyboard-trace pick, but only 2 of its 5 must-finds are cleanly trace-provable (the
focus-movement items); the other 3 are static ARIA-pattern-completeness gaps that
neither a keyboard trace nor axe can explain without APG-pattern knowledge — the same
"needs source judgment, not machine evidence" problem that ruled out the fieldset
fixtures above, just on the keyboard side. A noisier, harder-to-adjudicate
representative of the class than `tabs-missing-arrow-nav`'s single clean mechanism. (It
remains a strong candidate if this lane is ever expanded past 6 fixtures — flagging for
the gate reviewer as a good 7th pick.)

#### Buggy, keyboard-trace #2 — `interactive-dropdown-focus-bug`

Custom dropdown, correct ARIA, focus not restored to trigger after selection or Escape
— 2 must-finds MAJOR (WCAG 2.1.2 + WAI-ARIA Listbox Pattern). Chosen for three
compounding reasons: (1) real committed driven trace exists
(`driven/interactive-dropdown-focus-bug.trace.json` + `.findings.json`); (2) it is the
**exact fixture already used in the Phase 2.3 worked-example receipt**
(`evals/results/context-utilization-phase2/README.md`, Receipt B) — meaning the
reader(haiku)→critic(opus) chain on this precise trace has already been run once and
independently validated end-to-end, which lowers execution risk for a lane under a hard
gate date; and (3) both must-finds are single-mechanism failures (focus-target
absence) that a trace proves cleanly, unlike fixtures mixing static-attribute and
live-announcement defects. **Important gotcha this receipt surfaces for pack
construction (not yet resolved, flagging explicitly — see §12):** reusing the *raw*
trace artifact is exactly what the plan's "recorded, never regenerated" sourcing rule
encourages, but the Phase 2.3 receipt's **digest** must NOT simply be copied into this
lane's CURATED pack — that digest answered a *different* question ("Which components…
changed ARIA state without any accessible announcement…") authored for a different
provenance chain, and the plan's blind-curation rule requires the CURATED pack be
generated fresh, blind, for *this* lane's own question. The raw trace is reusable; the
digest is not.

**Runner-up rejected:** `form-validation-missing-aria-describedby`. A genuinely strong
alternate — both its must-finds are trace-evidenced per KAT's own driven session table
("*After submitting empty: field flips `invalid=true`... yet zero `live_announcements`;
refocused field's AX shows `labelledby` only — no `describedby` relation*", README line
103) — but it mixes a structural fact (missing `describedby` relation, visible in an AX-
tree snapshot) with a live-announcement fact (nothing fired), which is a slightly
harder adjudication surface than `interactive-dropdown-focus-bug`'s two focus-target
failures, and it lacks the latter's already-validated Phase 2.3 chain. Kept as a strong
candidate for a future lane expansion.

### 2.2 Selection summary

| Fixture | Tier | Evidence class (primary) | Real raw-artifact status |
|---|---|---|---|
| `button-skip-link-clean` | CLEAN | axe-detectable (page-shell-capable) | real, committed (batch-crawl) |
| `modal-complete-clean` | CLEAN | keyboard-trace | real, committed (driven trace) |
| `heading-hierarchy-skipped` | HAS-BUGS | axe-detectable | real tool run required (new) |
| `file-input-no-labels` | HAS-BUGS | axe-detectable (mixed w/ source-only items) | real tool run required (new) |
| `tabs-missing-arrow-nav` | HAS-BUGS | keyboard-trace | real, committed (driven trace) |
| `interactive-dropdown-focus-bug` | HAS-BUGS | keyboard-trace | real, committed (driven trace) — reuse trace only, not digest |

---

## 3. Per-fixture raw-artifact sourcing plan

**De-risking finding, not previously known to the task brief:** this repo already has a
working pipeline that turns these markdown/JSX critic fixtures into real, servable HTML
pages — `evals/results/keyboard-a11y-tester/harness/build_fixtures.py` (React 18 UMD +
Babel standalone, per-fixture prop shims, served via `python3 -m http.server`), built
2026-07-10 for the KAT cross-validation and covering the original 33 fixtures including
all 6 chosen here. Real axe-core runs against rendered fixture HTML do not need a new
rendering approach invented — they need this existing harness re-pointed and re-run
with `references/baseline-url-scan.mjs` in place of (or alongside) KAT's runner.

**One concrete blocker to flag for lane setup (not fixed by me — out of this task's
scope, see hard constraints):** `build_fixtures.py`'s `FIXTURES` constant (line 8) is
hardcoded to `/Users/AlexUA_1/claude/a11y-meta-skills/evals/suites/a11y-critic/fixtures`
— the old canonical-source repo path, not this repo's own
`evals/suites/a11y-critic/fixtures`. This is a one-line path fix, but it's a shared
harness script outside my two deliverables, so I'm naming it as a lane-setup
prerequisite rather than editing it myself.

**A documented rendering-artifact risk to design around, with a citation:** the KAT
README already records that rendering an isolated component as a full page manufactures
findings that wouldn't be real in context — *"`pagination-no-nav-landmark` drew a 2.4.1
no-skip-link finding — true of the page we built but an artifact of rendering a lone
component as a full page... Fixture-granularity noise, not a tool error"* (README lines
87-89). The same risk applies to axe's page-level rules (landmark, region, bypass) for
any of my fixtures rendered without their original page context. This is exactly why
both axe-primary picks (`heading-hierarchy-skipped`, `file-input-no-labels`) were chosen
for defects whose relevant axe rules are **component-scoped** (`heading-order`, `label`)
rather than page-scoped — sidestepping the artifact class entirely rather than needing
to filter it out after the fact. `button-skip-link-clean` is the one fixture in this set
that legitimately ships its own page shell (nav/main/footer), so it's the only one where
page-level landmark rules should be allowed to fire meaningfully.

**Gate F11 (binding):** for the 3 driven-trace fixtures below, only `.trace.json` is
this fixture's own raw pack evidence — `.findings.json` is the tool's near-ground-truth
*conclusion*, not a raw observation, and including it would hand the model the answer in
both arms. `.findings.json` remains valid **padding**, sourced from *other* fixtures.
**Ruling 6 (binding):** `file-input-no-labels` additionally needs a fresh
keyboard-a11y-tester driven session (`harness/drive.sh` — the harness already exists) so
its items [1]/[2] (aria-describedby relation, aria-invalid state) become genuinely
`evidence_in_raw_set: true` rather than a documented `raw-set-gap` (§10) — this is new
work this table did not originally plan for.

| Fixture | Raw evidence source | Concrete path | DUMP padding source |
|---|---|---|---|
| `button-skip-link-clean` | Real tool run: axe via `baseline-url-scan.mjs` against `build_fixtures.py`'s rendered page (page-shell-capable) | New — reuse existing harness, fix path first | Real axe rows from sibling fixtures scanned in the **same batch** (see below) |
| `modal-complete-clean` | Real, committed: `evals/results/keyboard-a11y-tester/driven/modal-complete-clean.trace.json` ONLY (2026-07-10) | Reuse as-is, or fresh re-run via `harness/drive.sh` if the gate wants lane-isolated artifacts | Real batch-crawl `findings/*.json` rows from sibling fixtures (this fixture's own `.findings.json` is padding-eligible for *other* fixtures' packs, never its own) |
| `heading-hierarchy-skipped` | Real tool run: axe via `baseline-url-scan.mjs`, component-scoped render (no page shell needed) | New — reuse existing harness | Real axe rows from sibling fixtures in the same batch |
| `file-input-no-labels` | Real tool run: axe via `baseline-url-scan.mjs` (component-scoped) **+ new keyboard-a11y-tester driven session** (ruling 6) | New axe run + new driven session via `harness/drive.sh` | Real axe rows from sibling fixtures in the same batch |
| `tabs-missing-arrow-nav` | Real, committed: `driven/tabs-missing-arrow-nav.trace.json` ONLY | Reuse as-is, or fresh re-run via `harness/drive.sh` | Real batch-crawl `findings/*.json` rows from sibling fixtures |
| `interactive-dropdown-focus-bug` | Real, committed: `driven/interactive-dropdown-focus-bug.trace.json` ONLY — digest must be regenerated blind (§2.1) | Reuse trace as-is | Real batch-crawl `findings/*.json` rows from sibling fixtures |

**Rulings 1–3 confirmed by the gate, applied above:** narrowest-natural-context
rendering (ruling 1 ACCEPT — a uniform page shell would manufacture *more* false
findings in the DUMP arm specifically, a confound biasing P3 toward its own prediction);
`build_fixtures.py`'s path fix deferred to a manifest blocking-checklist item (ruling 2
ACCEPT, `lane_manifest.yaml` `preconditions:`, carrying F10's 41-vs-33 SHIMS constraint);
reuse over fresh re-runs for the 3 committed-trace fixtures (ruling 3: "committed KAT
driven traces *are* real tool output; they satisfy 'where feasible' on the merits" — the
live risk was F11, not contamination, and F11 is now fixed above).

**Batch-scan design (satisfies the binding "real, on-domain, fixture-irrelevant"
padding rule efficiently):** because `build_fixtures.py` already renders every fixture
into one `pages/` directory in a single pass, a single `baseline-url-scan.mjs` sweep
across all rendered pages (or a representative subset, e.g. 10–15 pages) in one sitting
produces real axe output for every fixture at once. DUMP padding for
`heading-hierarchy-skipped`, for example, is then literally the real axe rows the same
batch produced for `file-input-no-labels` or any other sibling page — real tool output,
same run, fixture-irrelevant to the fixture being padded. This exactly mirrors how the
Phase 2.3 worked-example receipt already used real "other pages of the same runs"
(EPA/product-a product-b pages) as its corpus (`context-utilization-phase2/README.md`,
Receipt B corpus description). The existing `findings/*.json` batch-crawl corpus
(already covering the original 33 fixtures) serves the identical role for the two
keyboard-trace picks' DUMP padding.

---

## 4. Local design — 2×2 (payload × num_ctx)

**Revised 2026-08-25 per the bench-reviewer gate (F2, F9, DUMP-cell ruling) —
`docs/plans/2026-08-25-context-utilization-phase3-gate-review.md`.** This section
replaces the prior 49,152-based design. **A discrepancy worth recording rather than
quietly overwriting:** gate finding F2 cites this section at "README.md:325" and
"README.md:318-323" containing "16.2K protocol + ~2K fixture" — neither string appears
at those lines (or anywhere) in the version this fix is applied to; that text only ever
appeared, correctly framed as *superseded*, in this section's own "F6 is superseded"
paragraph. The most likely explanation is that the gate reviewed a snapshot taken before
this document's second orchestrator-addenda edit pass (real probe numbers) landed —
possible under concurrent multi-agent editing of the same branch. This does not make F2
moot: its substantive requirement (a hard, probe-verified CURATED digest cap) was
genuinely still missing from the prior draft and is added below. Flagging the citation
mismatch for the record, not as a dismissal.

**Protocol-side numbers are measured, not estimated** — real `num_predict=1` probes
(2026-08-25, temperature=0, num_ctx=49152, byte-identical to `run_benchmark.py`'s own
prompt assembly), both local models, zero anomalies. Raw receipts: session scratchpad
`phase3-lane-setup-probes/` (protocol-token probes) and `phase3-lane-setup-probes/CEILING-PROBE-SUMMARY.md`
+ JSON + server-log excerpts + script (the §4.1 ceiling/clamp probe) — both sets to be
promoted into `evals/results/context-utilization-phase3/receipts/` at commit time
(orchestrator will handle promotion).

| Model | Protocol alone | + `multistep-form-error-clearing` (17,273 B — largest fixture in the 41-fixture suite, stress-test reference, not one of this lane's 6) | + `tabs-missing-arrow-nav` (5,363 B — median-sized, and one of this lane's 6 chosen fixtures) |
|---|---:|---:|---:|
| qwen3.6:35b | 14,276 | 17,153 (fixture ≈ 2,877 tok) | 15,167 (fixture ≈ 891 tok) |
| qwen3:32b | 13,853 | 16,447 (fixture ≈ 2,594 tok) | 14,649 (fixture ≈ 796 tok) |

qwen3.6:35b tokenizes ~3.0–4.3% denser than qwen3:32b on byte-identical prompts — first
measurement of this. qwen3:32b's 13,853 corroborates the plan's own F7/0.4b probe figure
exactly. **F6 superseded:** the plan's "16,157 tokens measured (qwen3.6 tokenizer)" (F6)
does not reconcile with the protocol-alone probe (14,276) — F6 most likely measured a
production row (protocol + fixture already folded in) on an ambiguous qwen3.6 tier;
mark F6 superseded-by-probe in the plan doc's own receipts when next touched (not edited
here — out of this task's scope).

### 4.1 Standardized on num_ctx = 40,960 (DUMP-cell ruling, adopted now)

The gate reviewed the qwen3:32b `/api/tags` `context_length=40960`-vs-49,152 risk this
document originally raised and issued a ruling before the parallel over/under probe
even reported back, because the ruling holds under **either** branch. The orchestrator
adopted it as a settled design decision, not a contingency: **the whole lane now runs
at num_ctx = 32,768 (CURATED@32K) or 40,960 (CURATED@40K, DUMP@40K), never 49,152.**
Verifying the gate's own arithmetic rather than copying it (both branches, qwen3:32b,
conservatively using the largest-fixture-in-suite probe cost of 2,594 tok — the
worst-case fixture-size assumption, not `tabs-missing-arrow-nav`'s smaller 796):

- **Usable ceiling under a 40,960 cap:** 40,960 − 8,192 (reserve) = **32,768** tokens
  for protocol + fixture + dump.
- **At the old 49,152-cell's originally-planned 18–20K dump:** 13,853 + 2,594 + 18,000 =
  **34,447**; 13,853 + 2,594 + 20,000 = **36,447**. Both exceed 32,768 by **1,679–3,679**
  tokens — confirmed over, matching the gate's stated range exactly.
- **Max dump qwen3:32b's budget could absorb under 32,768 usable (an upper bound, not
  the spec):** 32,768 − 16,447 (protocol + largest-fixture, i.e. the table's own
  "+ largest fixture" cell) = **16,321** tokens.
- **Binding spec (ruling 7, finalized independent of the probe): the dump is 15,000
  measured tokens, uniform** — not a target to hit approximately, and not the 16,321/
  15,615 max-budget figures above (those bound how large a dump *could* run before
  breaching the ceiling; 15,000 is what pack construction actually builds). Margin at
  the binding 15,000 spec, re-derived, not restated: 16,321 − 15,000 = **1,321 tokens
  (qwen3:32b)**; the tighter, binding constraint is qwen3.6:35b's 15,615 − 15,000 =
  **615 tokens** (§4.2 below) — **1,321/15,000 ≈ 8.8%** for 32b, not the earlier-cited
  "≥10%" I first wrote before re-checking the subtraction; presenting my verified number
  rather than the rounder one. The discrepancy is small and doesn't change the spec.
- **OVERFLOW receipt still fires at 32,768,** checked with qwen3.6:35b at
  `tabs-missing-arrow-nav`'s measured size (not the largest-fixture assumption — any
  fixture size trips this cell, so the smaller one is sufficient to prove the point):
  14,276 + 891 + 15,000 + 8,192 = **38,359** > 32,768 ✓ guard fires, matching the gate
  exactly.

**The over/under probe has returned — Branch B is CONFIRMED WITH HARD EVIDENCE, Branch A
is dead.** Reported directly by the orchestrator (not the earlier one-line memory
summary): server log — *"requested context size too large... n_ctx_train=40960"* —
plus a behavioral replication: a 45,176-token prompt was silently evaluated at only
20,482 tokens (54.7% dropped). Controls rule out a general instability: ~30K tokens
clean under the clamp; **40,493 clean at `num_ctx=40960` requested exactly** — the model
runs fine at its own real ceiling, it just won't honor a request above it.

**Direct citation, read from the receipt myself** —
`phase3-lane-setup-probes/CEILING-PROBE-SUMMARY.md` (session scratchpad; to be promoted
into `evals/results/context-utilization-phase3/receipts/` at commit time). Confirmed two
independent ways, per the receipt's own framing: (1) direct server-log evidence, no
inference required; (2) a behavioral over/under probe reproducing the exact
silent-truncation formula. **The clamp itself**, logged at model load:
```
level=WARN source=server.go:114 msg="requested context size too large for model" num_ctx=49152 n_ctx_train=40960
llama_context: n_ctx = 40960
```
**The truncation event**, on the decisive (~44.5K-target) probe:
```
level=WARN source=llama_server.go:317 msg="truncating input prompt" limit=20482 prompt=45176 keep=4 new=20482
```
This WARN line is a **direct, non-estimated report of the true prompt size** (45,176
tokens) truncated to 20,482 before evaluation — not an inference from
`prompt_eval_count` alone. The 3-probe behavioral table cross-validates it: calibration
(~30K target, 29,660 evaluated, not truncated), **decisive (45,176 true, 20,482
evaluated, truncated)**, confirm (`num_ctx=40960` requested exactly, 40,493 evaluated,
not truncated — the model runs cleanly at its own real ceiling). I re-derived the
arithmetic myself rather than taking the round numbers on faith: floor(40,960/2)+2 =
**20,482**, exact match; (45,176−20,482)/45,176 = **54.7%**, exact match.

**Same formula as the Phase 0.4b historical finding** (qwen3:32b's old 16,384-window
default silently evaluated floor(16,384/2)+2 = 8,194 tokens of a 16,447-token prompt,
49.8%) — **now replicated 2/2 at a different applied `n_ctx` (16,384 vs 40,960) and a
different overflow ratio (0.4% over vs 10.3% over), both landing exactly on**
`floor(n_ctx/2)+2`. Quoting the receipt's own calibrated framing rather than overstating
it: Phase 0 called this "an empirical correlation, not a confirmed mechanism... it still
isn't source-confirmed, but it's no longer a single data point — worth treating as a
working predictive formula for budget arithmetic until/unless a counterexample appears."
This document adopts that same framing (`known_risks:` in the manifest).

**Consequence, stated plainly:** had this lane's design stayed at the original
49,152, every one of qwen3:32b's DUMP rows would have silently truncated to ~20,482
tokens — reproducing the exact F7 silent-truncation failure the whole plan exists to
prevent, invisibly, because the Phase 0.2 client-side guard gates on the *requested*
`num_ctx`, never the model's declared ceiling (this gap is F13 below — routed to the
runner-builder as a Phase 0 fast-follow, not fixed here). The 40,960 standardization is
therefore **empirically mandatory now, not merely the gate's safer either-way
preference** — Branch A (the 49,152 design) is dead, kept above only as the arithmetic
record of why.

**qwen3.6:35b resolves the other way, doubly confirmed.** It declares `context_length`
262,144. Per the same receipt's server-log evidence, a **direct test at `num_ctx=49,152`
applied cleanly** — `llama_context: n_ctx = 49152`, `n_ctx_seq (49152) < n_ctx_train
(262144)`, no WARN, no clamp. 40,960 was not itself probed for this model, but sits
*below* the already-confirmed-clean 49,152, so it's a safe inference from the same
evidence, not an untested leap — stating that distinction precisely rather than
blurring "directly tested" into "inferred." The declared value (262,144) is
independently corroborated a second way: the runner-builder ran their own live
`/api/tags` query this session and got the identical number for both models
(qwen3:32b → 40,960, qwen3.6:35b → 262,144) — two independently-run checks agreeing.
The earlier "unflagged, not confirmed-safe" hedge is retired: **verified-safe** at both
40,960 and 49,152 for this model.

**Why 40,960 over a resize-per-model compromise:** the gate's own DUMP-cell ruling notes
that under a 40,960 cap, only qwen3:32b was structurally forced there — qwen3.6:35b
could in principle keep running a larger dump at some higher ceiling. Doing that would
mean "a 16K dump vs a [different-sized] digest is still a different payload ratio at a
fitting num_ctx... reintroduc[ing] the exact confound the one-num_ctx-per-cell clause
kills" (gate review, DUMP-cell ruling). Standardizing both models on the same 40,960
ceiling and the same 15,000-token dump spec (binding, ruling 7 — not a per-model or
per-fixture target) keeps every cell's "one num_ctx applied
identically to whatever runs in it" property intact, and makes P1b a **matched 32K→40K
contrast for both models** — see the Amendments section below. It also matches this
repo's existing high-water mark (the ACR lane runs at 40,960, `run_benchmark.py:768-769`).

### 4.1a F14 (BLOCKING, closed in this pass) — the binding spec was stated in the wrong units

**The guard gates on ESTIMATED tokens (`rb.estimate_tokens`, chars/3.5); every binding
number in the sections above was stated in MEASURED tokens (real `num_predict=1`
probes).** These are not the same currency, and the conversion factor between them is
not the plan's documented ~7% — **measured against this lane's own real probes, the
estimator overestimates 22–30%**, re-derived and confirmed myself, not copied:

| | est (chars/3.5, model-agnostic) | measured | est/measured ratio |
|---|---:|---:|---:|
| protocol alone | 17,480 | 14,276 (35b) / 13,853 (32b) | **1.224** / **1.262** |
| protocol + `tabs-missing-arrow-nav` (median fixture) | 19,004 | 15,167 (35b) / 14,649 (32b) | **1.253** / **1.297** |

**Drift caveat on the absolute counts above, not the conclusion.** These are the
protocol/fixture byte counts as measured against the **2026-08-25 probe corpus**,
frozen the day the probes ran. The a11y-critic `SKILL.md` (the "protocol" text these
figures estimate) has already changed since — commit `805c084` landed real content
edits (+356 chars) after this round's probes, and the runner-builder's live recompute
against the *current* file gets **17,386/18,249**, not 17,480/19,004. The **durable
fact is the est/measured ratio range, 1.22–1.30**, not either set of absolute counts —
both snapshots agree on that range within rounding. The absolute figures below are
**"as of the 2026-08-25 probe corpus (pre-`805c084`)"** and will drift again with the
next protocol edit; the ratio is what this document's arithmetic actually depends on.

**Restated binding spec, in the units the guard actually gates on** (not the runner's
prompt-assembly guard specifically — the same `context_overflow` function §9.5's runner
reuses unchanged): available estimated headroom for the dump = 32,768 (usable budget at
num_ctx=40,960) − est(protocol) − est(this fixture), **as of the 2026-08-25 probe
corpus (pre-`805c084`)** — for the one fixture this lane has directly measured
(`tabs-missing-arrow-nav`): 32,768 − 19,004 = **13,764 estimated tokens** at that
snapshot — this is the actual binding ceiling, not the 15,000-*measured*-token figure
stated as "the spec" earlier in this section. **§10 step 4's pre-freeze assertion is
not exposed to this drift** — it estimates the *actual assembled prompt* at pack-
construction time, by construction, not a cached number from this section; whatever the
then-current protocol text is, that's what gets measured. **The other 5 fixtures' real
headroom is not yet known regardless of drift** — it depends on each fixture's own byte
size, which hasn't been probed individually, so it is *not* safe to assume 13,764
applies lane-wide even before accounting for protocol drift; §10 now requires computing
it per fixture before freeze (below), against whatever the protocol text is at that time.

For a dump that measures 15,000 real tokens to pass a 13,764-estimated-token ceiling,
its own est/measured ratio must be **≤ 13,764/15,000 = 0.918** — i.e. the estimator
would need to *under*count the dump by ≥8%, the opposite direction from every ratio
measured so far (all four above overestimate). **This is genuinely unresolved, not a
predicted failure.** JSON's dense punctuation (braces, quotes, colons) plausibly
tokenizes differently from prose — the gate's own estimate is "plausibly 2.5–3.5
chars/token, which could put the ratio near 0.7–1.0 and pass. Nobody has measured it."
Scaling the only ratio in hand (prose, ~1.25–1.30) instead would refuse every DUMP row
as INVALID — the entire dilution arm of P1. **§10's "recorded, never regenerated" rule
is exactly why this cannot wait**: a wrong dump size discovered after freeze cannot be
corrected without violating the lane's own binding protocol, so it must be measured
*before* freeze, not assumed. 15,000 measured tokens remains the **secondary,
informational** target pack construction aims for; the estimated-token ceiling above is
what actually gates whether a real pack is accepted.

**CURATED remains differentiated and safe — corrected from the earlier ~7%-based
framing, which is now known to understate the true overestimate.** Re-derived using the
same estimated-token method, not the old ~7% factor: at `curated-32k`, usable estimated
budget = 32,768 − 8,192 = 24,576; minus est(protocol+`tabs-missing-arrow-nav`) 19,004
(pre-`805c084` snapshot; see the drift caveat above — the ratio conclusion, not this
count, is what's durable) = **5,572 estimated tokens of headroom**. For the
≤3,000-measured-token digest cap (still standing, unchanged) to clear that:
**5,572/3,000 ≈ 1.857 ratio headroom** — comfortably
above the observed 1.224–1.297 prose range, with room to spare even if a digest
tokenizes somewhat more densely than prose. The digest cap does not need to change; only
the dump cell was ever at risk.

**What this pass fixes (2 of 3 parts — the third is not mine):**
1. This restatement — the spec is now stated in the units that gate it, done here.
2. §10's pack-freeze protocol now requires, per fixture, asserting
   `rb.estimate_tokens(assembled_prompt) + 8192 <= 40960` **before** freeze, recording
   both the estimated and measured token counts in the manifest (not just the measured
   figure as before) — see §10 below. `ollama/run_evidence_lane.py`'s `--dry-run` mode
   against a real pack computes exactly this number; it is the mechanism, not a new tool.
3. **Not mine, referenced only**: correcting `estimate_tokens`'s docstring
   (`run_benchmark.py:42-44`, currently claims "~7% overestimate") and the plan's
   guard-landing finding text that repeats that number
   (`docs/plans/2026-08-24-context-utilization-plan.md`) is assigned to the
   runner-builder — `ollama/run_benchmark.py` is explicitly not touched by this lane's
   files, consistent with F13's routing. The corrected direction is worth stating
   plainly regardless of who lands the docstring edit: **measured margins are looser
   than believed; guard margins are tighter.**

### 4.2 Revised cell table

| Cell | num_ctx | Prompt composition (protocol measured; fixture measured for `tabs-missing-arrow-nav`, others pending; digest capped ≤3,000 measured tok; dump targeted ~15,000 measured tok) | Fits? |
|---|---:|---|---|
| CURATED@32K | 32,768 | protocol (13,853–14,276) + fixture (~0.8–2.9K) + digest (≤3,000) ≈ 17.7–20.2K prompt (+8,192 reserve ≈ 25.9–28.4K) | ✓ both models, real margin (§4.1's ~1,942-token floor is the binding constraint, not the nominal total) |
| CURATED@40K | 40,960 | same prompt as CURATED@32K, larger window | ✓ both, generous margin |
| DUMP@40K | 40,960 | protocol + fixture + dump (15,000 measured, informational — §4.1a: the guard-binding ceiling is 13,764 EST tokens for `tabs-missing-arrow-nav`, unmeasured for the other 5 fixtures) ≈ 29.7–32.2K measured-basis prompt (+8,192 reserve ≈ 37.9–40.4K) | **UNVERIFIED per fixture until F14's §10 pre-freeze assertion runs (gate F14)** — the measured-basis totals shown fit comfortably, but the guard gates on estimated tokens, not measured, and that ratio is unmeasured for real dump content |
| OVERFLOW (receipt only) | 32,768 | same prompt as DUMP@40K | ✗ guard fires on both models, by design — holds under F14 too: even at the most favorable plausible JSON tokenization (est/measured ≈ 0.7, well below anything measured so far), est(protocol+fixture) 19,004 (pre-805c084 snapshot) + est(dump) ~10,500 + reserve 8,192 ≈ 37,696 still exceeds 32,768. 1 fixture × 1 draw per model, documents the failure mode, not scored |

**Decomposition this buys** (verbatim from plan, cell names updated): *(CURATED@40K vs
DUMP@40K) = payload effect at fixed fit — the dilution test. (CURATED@32K vs
CURATED@40K) = num_ctx effect at fixed payload — the fit/quantized-long-context test,
and the data R5 needs. OVERFLOW = the mechanism receipt.*

**Models:** local — qwen3.6:35b + qwen3:32b (control), both at the same standardized
num_ctx per cell, and **both now verified against their declared `/api/tags`
`context_length`** (§4.1: qwen3:32b clamps at 40,960, confirmed with server-log
evidence; qwen3.6:35b declares 262,144, no clamp — resolved, not an open item as of
this revision). Hosted — opus + sonnet subagent rows; conditions CURATED vs DUMP only
(no ctx dimension), same frozen packs as local.

**One dump size, aimed uniform across both models and all 6 fixtures — 15,000 measured
tokens is the informational target pack construction builds toward, not the number that
gates a real pack.** The margin arithmetic that used to live in this paragraph (615/
1,321-measured-token margins, computed on the measured-vs-measured "max dump" basis) is
**superseded by gate F14 (§4.1a): the guard that actually accepts or refuses a real pack
gates on ESTIMATED tokens, and the est/measured conversion factor is not close enough to
1:1 to treat measured-basis margin as the binding number.** Kept here only as the
record of what this paragraph said before F14, not as a live claim. The binding ceiling
is the estimated-token headroom worked out in §4.1a (13,764 EST for the one fixture
measured so far), and §10 now requires computing it per fixture, per model, before
freeze — a uniform 15,000-measured target may or may not clear that ceiling depending on
how the real dump content (mostly JSON) actually tokenizes, which is exactly the
open question F14 identifies as unresolved.

---

## 5. Run matrix + draw discipline

**Draws:** ≥2 per cell, content-adjudicated. Single-draw deltas are variance
(documented flip magnitude 2–3 items on byte-identical prompts — plan §3 F-series /
§9 R3).

**Run count** (verified by re-deriving the arithmetic from the lane's own dimensions,
not just copied):
- Local: 3 scored cells (CURATED@32K, CURATED@40K, DUMP@40K) × 2 models × 6 fixtures ×
  2 draws = **72**, + 2 OVERFLOW receipts (1 fixture × 1 draw × 2 models, unscored) = 74
  local rows total, 72 of them scored.
- Hosted: 2 conditions (CURATED, DUMP) × 2 models (opus, sonnet) × 6 fixtures × 2 draws
  = **48**.

This matches the plan's stated totals exactly (local 72 + 2 OVERFLOW receipts; hosted
48) — cell renaming (§4.1) changes num_ctx values, not the count.

**Scores per row** (plan verbatim, partition revised per gate F4): must-find recall; FP
findings on CLEAN; miss partition — `not-tool-observable` / `raw-set-gap` /
`pack-omission` / `model-miss` (4 buckets, not the plan's original 2 — see §10);
`prompt_eval_count` + `done_reason` (+ `output_clipped`, gate F7) on every local row
(Phase 0 guard active). See §10 for how the miss partition is produced and §11 (scorer)
for how it's consumed.

### 5.1 Prompt composition — binding lane spec (was unspecified; the runner surfaced the gap)

Neither this document nor the plan ever specified where the evidence pack splices into
the prompt relative to the fixture source and the critic protocol's own ask — a real
gap, not an ambiguous phrasing, surfaced when `ollama/run_evidence_lane.py` needed one
and had none to read. **Binding for both arms — local and hosted must use the identical
composition, since comparability depends on it, not just local execution:**

```
[critic-protocol ask — run_benchmark.py's PROMPT_PREFIX, unchanged]
[fixture source — blind protocol applied, i.e. the answer-key section withheld]

## Evidence Pack (CURATED)   -- or -- ## Evidence Pack (DUMP)

[the pack content]
```

Ask, then fixture, then a labeled `## Evidence Pack (CURATED|DUMP)` block — matching how
a human reviewer naturally receives the material (instructions, then the code under
review, then supporting tool evidence). This is the runner's own already-implemented
default (`assemble_prompt()`, isolated in one function); this section makes it the
lane's spec rather than the runner's private choice, so hosted-arm subagent prompts are
built to the same shape by construction.

**Watch item, not a preemptive change:** the runner reuses the critic lane's 300s
network timeout (`run_benchmark.py`'s `run_ollama`) unchanged. DUMP@40K prompts run
substantially larger than a plain critic row (~30–32K vs ~16K), and generation time
scales with prompt size on top of output length — this may be tight for the first real
DUMP rows. Watch the first batch's `elapsed_seconds`; raise the timeout only if it
actually times out, not speculatively.

---

## 6. Registered predictions (verbatim, 2026-08-24, before any row)

### 6.0 Amendments to registered design (added 2026-08-25 per gate review)

Per the plan's own design principle 5 ("measure, then claim") and the funnel discipline
of registering thresholds before rows exist, amendments to a pre-registered design get
recorded explicitly rather than silently folded into the predictions below as if they
always read this way. Full citation: `docs/plans/2026-08-25-context-utilization-phase3-gate-review.md`.

- **P1b's contrast changed from 32K→49K to 32K→40K** (§4.1, DUMP-cell ruling). The
  predictions below are written against the new cell names; the *comparison being made*
  — num_ctx effect at fixed CURATED payload — is unchanged, only which two num_ctx
  values are being compared. This keeps P1b a **matched contrast across both models**
  (32K→40K for qwen3.6:35b and qwen3:32b alike), which the original 32K→49K design did
  not guarantee once qwen3:32b's declared context length entered the picture.
- **P1's ≥2-item threshold gets the F9 pool-size re-derivation, verified not copied.**
  The plan's documented 2–3-item flip magnitude was measured against the full 68-item
  critic suite; this lane's pool is far smaller. After gate F1 (per-item keyword
  overrides — §9.4) and F4 + ruling 6 (evidence-set correction — file-input-no-labels'
  items [1]/[2] are AX-observable once its keyboard artifact is collected, leaving only
  item [3] genuinely source-only), the **tool-observable, dilution-eligible pool is 8 of
  this lane's 9 must-finds** — verified by re-adding: heading-hierarchy-skipped (2) +
  file-input-no-labels (2 of 4) + tabs-missing-arrow-nav (1) + interactive-dropdown-focus-bug
  (2) + button-skip-link-clean/modal-complete-clean (0, CLEAN fixtures carry no
  must-finds) = 7... **correction caught while re-deriving, not copied:** 2+2+1+2 = 7,
  not 8. Re-checking the gate's own count: "file-input given AX evidence (ruling 6)"
  lifts file-input from 1 tool-observable item (only [0], the axe-clean label hit) to 3
  (adding [1] and [2]) — so the pool is `heading(2) + file-input(3) + tabs(1) +
  dropdown(2)` = **8**, matching the gate. My first pass above miscounted file-input's
  contribution as 2 instead of 3 — flagging the correction inline per the same
  verify-before-presenting discipline as §4.1's earlier arithmetic catch, rather than
  quietly fixing it. Per condition: 8 items × 2 models × 2 draws = **32 observations**.
  P1's ≥2-net-item threshold ≈ 2/32 = **6.25%** of the pool. Against the gate's stated
  ~±0.7-item pooled draw-noise estimate (an input I have not independently re-derived —
  I can confirm the *arithmetic given that input* checks out: 2/0.7 ≈ 2.86, "roughly 3σ"
  as the gate states — but not the noise estimate itself, which would need a statistical
  derivation from the 68-item suite's documented flip magnitude that isn't shown in the
  gate doc), the lane is **powered for P1 once the file-input AX artifact is actually
  collected** at pack-construction time — not yet, as of this fix pass, which only
  authors the keyword overrides and corrects the evidence-set documentation.

- **P1 (local, dilution):** recall(CURATED@40K) ≥ recall(DUMP@40K), by ≥2 net
  adjudicated must-find items across the grid to count as real (below that: variance,
  report as null). Pool size and threshold-as-percentage: see 6.0 above.
- **P1b (local, fit):** recall(CURATED@32K) ≈ recall(CURATED@40K) (|net| ≤1 adjudicated
  item). A CURATED@32K deficit would mean num_ctx itself degrades quality on these
  quantized models — flag for BENCHMARK.md.
- **P2 (hosted, non-inferiority harm-check):** CURATED loses ≤1 net adjudicated
  must-find item vs DUMP across all hosted cells. This is the safety question Phase 2's
  default-on delegation needs answered; it is powered as a harm-check, not a benefit
  estimate. Any null is scoped to pack-scale (~20K) in the results README — it does not
  license claims about session-scale (163–349-turn) payloads.
- **P3 (both):** FP findings on CLEAN under DUMP ≥ under CURATED. Least confident,
  directional only. **Gate F8 (binding addition):** raw structured-finding counts need
  the same content-adjudication pass as must-find recall before they count as FP. Both
  CLEAN fixtures (`button-skip-link-clean`, `modal-complete-clean`) carry one legitimate
  `nice_to_find` ENHANCEMENT each in their metadata — a model that correctly reports that
  enhancement as a numbered finding is not producing a false positive, but the scorer's
  `count_false_positives` (`score_output.py`, unmodified per F1's "leave it untouched"
  instruction) counts any numbered `Finding N:` regardless of severity and cannot tell
  the difference on its own. `score_evidence_lane.py`'s CLEAN-row reporting was changed
  to state this candidate status explicitly rather than printing a bare PASS/FAIL (§11).

## 7. Decision rules (verbatim, pre-committed)

- P1 real + P2 holds → curation earns an accuracy claim (magnitude = adjudicated
  items); Phases 1–2 discipline confirmed on both grounds.
- P1 null + P1b null + P2 holds → curation delivers no pack-scale accuracy gain;
  Phases 1–2 stand on cost/latency/longevity grounds — the results README says so in
  those words; R5 resolves to map hygiene (correct num_ctx entries), no further
  curation lanes.
- P2 fails (CURATED loses >1 net item) → Phase 2's reader does NOT become a default
  path; it stays an opt-in cost tool pending pack-omission analysis (the partition says
  whether curation or the model lost the item).

## 8. Kill-rule + lane-setup gate date

Verbatim from plan §9 R7 / §6 Phase 3: *"pack construction ≈ 1–2 focused sessions
(fixture-builder, sonnet, medium). If packs are not built by the lane-setup gate date,
**descope to a 2-fixture pilot (1 buggy + 1 CLEAN) and run it anyway** — the lane
shrinks; it does not silently evaporate."*

**Lane-setup gate date: 2026-09-01** — confirmed (being written into the plan's own §9
R7 row as this document is drafted; consistent with the date given in the original task
assignment, not a date I chose). If this design + scorer pass the bench-reviewer gate but packs are not built
and audited by 2026-09-01, the lane descopes to a 2-fixture pilot. My recommendation for
which 2 fixtures survive that descope, if it's invoked: **`heading-hierarchy-skipped`**
(buggy, lowest-execution-risk axe pick — component-scoped rule, no page-shell
complication, direct KAT-confirmed axe-detectability) + **`modal-complete-clean`**
(CLEAN, both raw-evidence types already real and committed, zero new tool execution
needed). This is a recommendation, not a binding choice — flagging it for the
bench-reviewer to confirm or override.

---

## 9. Pack construction — binding rules (verbatim from plan) + how this lane exercises the two untested Phase 2 gaps

**Blind curation:** CURATED packs are generated by the Phase 2 `a11y-evidence-reader`
running its normal protocol with no access to fixture metadata/ground truth. Phase 3
formally depends on Phase 2.

**Recorded, never regenerated:** pack completeness is audited against ground truth
before any model row and the audit is committed. Packs are then frozen. Post-row misses
are partitioned: pack-omission vs model-miss. Both reported per cell. No regeneration
loop exists.

**Raw sets and padding:** both conditions derive from the same raw artifact set per
fixture (§3 above). DUMP padding = real, on-domain, fixture-irrelevant tool output from
other pages/components of the same runs — uniform rule; never synthetic noise.

**CLEAN packs:** the blind reader digests genuinely clean artifacts; an honest "no
violations surfaced; coverage: …" digest is the ecologically valid CURATED pack. The
DUMP arm carries the clean raw output + the same padding rule. **Gate F12 (cosmetic,
noted not fixed):** the two CLEAN fixtures' metadata schemas differ slightly —
`modal-complete-clean.metadata.yaml` declares a `false_positive_trap: 0` category that
`button-skip-link-clean.metadata.yaml` omits entirely. Both count zero either way, so
nothing scores differently; not worth a fixture-metadata edit for this lane alone.

### 9.1 Adjudication question — provenance rule and template (binding, added 2026-08-25 per Phase 2 post-ship review)

This is not a new mechanism — the `a11y-evidence-reader` agent def already carries the
fields (`Output_Format`: `**Question (verbatim)**` and `**question_source**`, the
latter's own example text reading *"Phase 3 pack curation, authored without
ground-truth access"*). The binding addition is that Phase 3 pack construction must
actually populate `question_source` with an explicit no-ground-truth attestation for
every one of the 6 fixtures, and the completeness audit (§10) must check that
attestation is present and specific, not a placeholder.

**Question template**, generalized from the Phase 2.3 worked-example receipt's own
question (`context-utilization-phase2/README.md`, Receipt B — authored "from artifact
filenames and tool types only; no fixture metadata, rubrics, or ground-truth files
consulted"):

> Based on [list the exact artifact filenames/paths handed to the reader — e.g.
> `<fixture-id>.trace.json`, `axe-<fixture-id>.json`, `summary.json` (gate F16: never
> `<fixture-id>.findings.json` for the fixture's own pack — F11 excludes it; that
> filename pattern belongs only among *other* fixtures' padding-eligible artifacts)]
> and the tool that produced each (keyboard-a11y-tester driven trace /
> keyboard-a11y-tester batch-crawl findings / axe-core scan): does this evidence set
> show any interaction defect (focus not reaching or leaving an element as expected, an
> ARIA state changing with no accessible announcement, a keyboard-operability failure)
> and does it show any structural defect (a missing or incorrect ARIA role, landmark,
> label, or heading-order violation) for the component these artifacts describe?

The two-part shape (interaction question + structural question) mirrors the Phase 2.3
precedent deliberately — it's generic enough to point at any fixture's artifact set
without presupposing which specific defect exists (a leading question would let the
reader "answer" from the question's own phrasing, which `<Blind_Reading>` forbids), and
narrow enough to be answerable from filenames and tool types alone.

**Illustrative-only schematic** (generic filenames, not one of this lane's real
fixtures, to show the template's shape without touching any real artifact):

> Based on `widget-x.trace.json` (keyboard-a11y-tester driven trace) and
> `axe-widget-x.json` (axe-core scan): does this evidence set show any interaction
> defect... and does it show any structural defect... for the component these artifacts
> describe?

**A real worked example for one of this lane's 6 chosen fixtures is marked TBD, not
supplied here — stating why rather than fabricating blindness I don't have:** fixture
selection (§2.1) required reading all 6 fixtures' `.metadata.yaml` files, including
their `expected_findings`, in full. I have therefore already seen ground truth for
every fixture in this lane and cannot un-know it — any question I wrote now, even
restricted to filenames and tool types, would risk being shaped by hindsight I can't
verify I've excluded. Per the addendum's own framing: **the real worked-example
question for each of the 6 fixtures must be authored by a fresh agent at pack-
construction time**, one with no prior exposure to this README's fixture-selection
rationale or to any of the six `.metadata.yaml` files. `lane_manifest.yaml` carries a
`TBD` placeholder for each fixture's `adjudication_question` field pending that.

### 9.2 Re-curation gate: AMBIGUOUS rows before freeze (binding, added 2026-08-25 per Phase 2 post-ship review)

If a haiku-run CURATED pack's coverage note carries **any** `AMBIGUOUS` row (the agent
def's own categories: schema unrecognized, fields don't match the extraction recipe,
artifacts conflict, a read was truncated at source, or run provenance is unclear), that
pack is re-curated by re-invoking the same reader agent def at **sonnet**, not
patched or hand-edited. This is not a new escalation path — it's the agent def's own
rule (`<Model_Routing>`: *"Self-escalation, not guessing... Record the item as
AMBIGUOUS... note `re-invoke at sonnet`, then continue"*) made mandatory rather than
advisory for this lane: no pack freezes with an unresolved `AMBIGUOUS` row still in it.
This applies across all 6 fixtures uniformly — it is not tied to a specific fixture the
way the two exercises in §9.3 are, since any fixture's raw artifacts could trigger it
(conflicting axe/trace evidence, an unexpected schema in a real tool-run JSON, etc.).
Sequenced as step 2 in §10's protocol, immediately after the reader's first pass and
before the ground-truth completeness audit — the audit runs against the *final*,
possibly sonnet-re-curated digest, never the haiku draft.

### 9.3 Exercising the two untested Phase 2 receipt cases

The Phase 2.3 worked-example receipt (`context-utilization-phase2/README.md`, "Digest
grading vs the def contract") left two cases from the reader's own Q4 grading design
untested: **(c) glob-partial coverage** (a glob matching more files than get read,
reported as one grouped PARTIAL row) and **(d) "should"-bearing verbatim excerpts**
(axe `help` strings routinely contain "should"; the reader must quote them exactly
rather than treating the word as its own prose). Both are load-bearing correctness
properties of the reader's contract (`.claude/agents/a11y-evidence-reader.md`,
`<Execution>` step 2 and `<What_You_Emit>` respectively) that no prior receipt has
actually forced to fire.

- **Glob-partial coverage → assigned to `tabs-missing-arrow-nav`'s pack construction.**
  The blind reader is handed its own `driven/tabs-missing-arrow-nav.trace.json` path
  (specific, per gate F11 below) PLUS, separately, a glob over the padding corpus —
  `evals/results/keyboard-a11y-tester/findings/*.json` — matching all ~33+ sibling
  fixtures' real batch-crawl files, not a pre-filtered single path. This is also the
  *realistic* shape of blind curation (a human curating the exact file list before the
  reader runs would defeat the point of a blind reader). The completeness audit for this
  fixture must explicitly confirm the coverage note reports this as one grouped
  `PARTIAL` row with an N-matched / read / not-read count, per the agent def's own rule
  ("Glob expansion is inventoried at file granularity... reported as one grouped row"),
  not silently enumerated file-by-file or collapsed to an opaque single entry.
  **Tension with gate F11, resolved here rather than left silent:** the glob matches
  `findings/tabs-missing-arrow-nav.json` too — F11 requires that specific file be
  excluded from THIS fixture's own raw pack (it's the tool's conclusion, not an
  observation). The blind reader cannot know that policy from blind reading alone, so
  pack construction must exclude this fixture's own findings entry from the glob before
  handing it to the reader (or accept the match and mark it NOT READ / out-of-policy in
  the completeness audit, never as evidence backing a must-find) — a checklist item for
  whoever builds this pack, not something to leave as an unstated contradiction between
  two binding rules.
- **"Should"-bearing verbatim excerpt → assigned to `heading-hierarchy-skipped`'s pack
  construction.** axe-core's `heading-order` rule is well known to carry "should" in
  its help text. **Hedging this specific claim rather than asserting it as verified
  fact:** I have not run axe-core in this session to confirm the exact current wording
  pinned at lane setup — the load-bearing requirement is that a genuinely real axe
  `help` string containing "should" reaches the reader (any real rule's help text that
  happens to collide works equally well; `heading-order` is simply the most likely
  candidate given this fixture's real rule hit). The completeness audit must confirm
  the reader quoted the string verbatim, "should" included, inside an `evidence` block
  rather than rephrasing it into its own prose (agent def: *"axe `help` strings
  routinely contain 'should'... quote them exactly as written"*).

Both are the fixtures I already selected on independent evidentiary grounds (§2.1) —
no fixture was added or reshuffled solely to manufacture these test cases.

### 9.4 Must-find keyword overrides (binding, gate F1)

The scorer (`ollama/score_evidence_lane.py`) matches must-find items against explicit
per-item `keywords:` overrides in `lane_manifest.yaml`'s `must_find_keywords`, never
`score_output.py`'s generic branch cascade. Gate F1 proved that cascade cannot
discriminate 5 of this lane's 9 must-finds against a null response — two items on
`interactive-dropdown-focus-bug` shared a byte-identical keyword set (`['focus',
'restored']`) and could never be told apart; `heading-hierarchy-skipped`'s items matched
on the stopword "from"; `file-input-no-labels`' item [3] (a 3.3.2 defect) mis-routed to
live-region keywords via the word "announced". All 9 overrides are hand-authored in the
manifest now, discriminating on each item's actual distinguishing fact (e.g. the
dropdown pair discriminates on the triggering event — "after selecting" vs "after
escape" — since that's what actually differs between the two defects, not the shared
"focus not restored" framing). Calibrated 2026-08-25: a null/no-issues response scores
all 9 False (`score_evidence_lane.py --selftest`'s real-fixture calibration block); spot
checks confirm the positive direction discriminates too (the dropdown pair, given a
response describing only the Escape-key defect, matches item [1] and misses item [0] —
the exact case the gate's F1 finding named).

### 9.5 Prompt assembly order (binding, gate F6 interface — resolved via direct coordination)

Full spec moved to **§5.1** (it governs both local and hosted arms, not just pack
construction, so it lives with the run matrix). Summary: `[critic-protocol ask] +
[fixture source] + [labeled evidence-pack block]` — the runner's own implemented
default, now the lane's binding spec rather than the runner's private choice.

### 9.6 Ruling 8 hardening — question-authorship protocol (binding, gate re-review)

Beyond §9.1's template and §9.4's precondition (a TBD field is data, not a gate — the
manifest's new `adjudication-questions-authored` precondition makes "all 6 authored and
attested" an explicit checkable step), two further requirements from the gate's
re-review:

- **Spawn-prompt recording (auditability, not self-certification).** The fresh
  question-authoring agent's exact spawn prompt must be recorded alongside each
  fixture's `adjudication_question` and `question_source` — not just the agent's own
  claim that it worked blind. A `question_source` that says "authored without
  ground-truth access" is not itself verifiable; the spawn prompt is the artifact that
  lets a later auditor confirm what that agent actually had access to when it wrote the
  question.
- **The practical tension, named rather than glossed over:** the fresh agent must never
  see this README — §3's sourcing table and the fixture-selection rationale throughout
  §2 effectively hand it ground truth (which defect class each fixture has, which
  artifact maps to which must-find). It also must not see any fixture's `.metadata.yaml`
  (§9.1's existing rule). What it *can* see, and all it should be given: a
  mechanically-extracted list of artifact paths + producing tool per fixture, derived
  from `lane_manifest.yaml`'s `raw_source_note` fields (§3's table) — filenames and tool
  types only, stripped of the surrounding rationale prose that would leak intent. Pack
  construction's checklist item is to actually perform that extraction as a separate,
  narrow step, not to hand the fresh agent the manifest file itself (which also carries
  `evidence_class_note` and `must_find_keywords` — both ground-truth-adjacent).

---

## 10. Pack freeze + completeness-audit protocol

**Blocking precondition — RESOLVED 2026-08-25, commit `805c084`.** The reader-def fix
making the full `states` dict for ARIA-state observations exempt from the
`<What_You_Emit>` "excerpts are verbatim, ≤10 lines" cap, emitted as `jq -c` compact
JSON, is now in the committed def (`.claude/agents/a11y-evidence-reader.md`, Phase 2 fix
set, "digest guard all surfaces" — `805c084`). Before the commit it said to "carry the
artifact's full `states` dict verbatim" without exempting that field from the 10-line
cap or specifying compact emission, so a real `states` dict large enough to exceed 10
lines pretty-printed would still have been truncated, contradicting its own
instruction. `lane_manifest.yaml`'s `preconditions:` entry is marked `done: true`
against this commit. **Why this mattered for Phase 3 specifically, not just def
quality (kept for the record):** a reader that silently condensed a `states` dict under
the cap would have produced exactly the failure the Phase 2.3 receipt already caught
once (Obs 1's "condensed" evidence — arrays summarized, keys re-ordered — masked by a
targeted lookup that time, but Phase 3 has no critic doing a targeted lookup per row;
the completeness audit is the only check). Two of this lane's own fixtures involve
ARIA-state observations from keyboard traces (`interactive-dropdown-focus-bug`'s
`aria-expanded`/`aria-haspopup` states, `tabs-missing-arrow-nav`'s `aria-selected`/tab
states) — on either, an uncorrected condensation would have been audited and booked as
`pack-omission` (the evidence "never entered the CURATED pack") when the real cause was
a reader-def defect, silently inflating R1's headline number (plan §9 R1: pack-omission
"*is* R1's number, the measured cost of blind curation") with a bug's cost instead of
curation's real cost.

**New binding checkpoint, same failure family, added 2026-08-25 (critic re-verification
carry-forward) — not yet resolved, applies at first-pack time:** nothing in Phase 2 has
been model-tested past n=1. This lane's first real CURATED digests therefore double as
**instrument calibration data for the reader def itself**, not just pack content. If a
first-pass digest comes back with a condensed `states` dict (despite the fix above) or a
single class label on a genuinely `mixed` evidence-class question (per the reader's
`<Execution>` step 3), that is a **reader-def defect surfacing**, not a fixture-level
pack-omission — fix the def, re-run the reader, and do **not** book it as pack-omission
or freeze it into a pack. This is the exact contamination risk the `states`-dict
precondition above guards against, generalized: the fix landing at n=0-tested doesn't
retire the risk, it just moves the first real test to this lane's own first rows.

1. The blind `a11y-evidence-reader` produces one CURATED digest per fixture, per §9,
   with zero access to `.metadata.yaml` or any ground-truth document (blind-reading
   rule, agent def `<Blind_Reading>`), at haiku tier by default, using this fixture's
   `adjudication_question` from `lane_manifest.yaml` (§9.1) verbatim as the question
   handed to the reader.
2. **Re-curation gate (§9.2):** if the resulting coverage note contains any `AMBIGUOUS`
   row, re-invoke the same reader def at sonnet before proceeding. Step 3's audit runs
   against this final digest, never a haiku draft that still has open `AMBIGUOUS` rows.
3. **A separate process** — not the same blind reader, since this step requires ground
   truth — audits each digest against the fixture's `expected_findings.must_find` list
   *before any model row exists*. **Revised 2026-08-25 per gate F4:** the original
   2-field design (`tool_observable` alone deciding pack-omission-vs-not) conflated "no
   tool could ever see this" with "no tool happened to be run for this fixture" — the
   gate proved this live: 3 of `file-input-no-labels`' 4 must-finds were called
   source-only under the old 2-field test, but items [1]/[2] are AX-observable in
   principle (KAT's own driven session on the sibling `form-validation` fixture proves
   that exact class — `keyboard-a11y-tester/README.md:103`) — only item [3] genuinely
   is source-only. For every must-find item, the audit now records **four** facts,
   committed as `evals/results/context-utilization-phase3/completeness/<fixture_id>.audit.yaml`:
   - `tool_observable` (bool, informational): could **any** real tool run (axe or
     keyboard-a11y-tester) **in principle** surface evidence for this item, on any
     fixture, ever? Genuinely source-only items (e.g. `file-input-no-labels`'s "file
     type restrictions not announced" — no tool observes it) are `false`.
   - `evidence_in_raw_set` (bool, the OPERATIVE field for tool-observable items): does
     THIS fixture's actually-collected raw artifact set contain the run that would show
     this item? An item can be `tool_observable: true` and `evidence_in_raw_set: false`
     simultaneously — the defect class is machine-detectable in principle, but this
     lane's pack construction didn't happen to run that specific tool against this
     specific fixture (ruling 6: this is exactly `file-input-no-labels`' items [1]/[2]
     until the keyboard/AX artifact ruling 6 calls for is actually collected).
   - `in_curated_pack` (bool, only meaningful when `evidence_in_raw_set: true`): does
     this item's evidence actually appear in the generated CURATED digest, checked
     against the raw artifact?
   - `raw_handle`: where in the raw artifact this item's evidence lives (jq path, trace
     step, file:line) — so a human/opus adjudicator can re-check the audit itself.
   The audit file also records `adjudication_question` and `question_source` verbatim
   from the frozen digest (§9.1), so the provenance attestation is checkable alongside
   the completeness numbers rather than trusted from the digest alone. **Every key is
   required — an absent key is a defect in the audit, not a silent default** (gate F5a):
   the scorer raises rather than guessing `tool_observable`/`evidence_in_raw_set`/
   `in_curated_pack` as true or false when a key is missing, because a silent default
   would bias whichever registered prediction reads the partition.
4. **New pre-freeze gate (gate F14, binding) — assert the ESTIMATED-token size, not
   just the measured size, before freezing DUMP.** For every fixture's assembled DUMP
   prompt (§5.1's composition: ask + fixture source + labeled pack block), assert
   `rb.estimate_tokens(assembled_prompt) + 8192 <= 40960` — the exact check the runtime
   guard performs — and record **both** the estimated and measured token counts in the
   manifest (`dump_estimated_tokens`, `dump_measured_tokens` per fixture; a real
   `est/measured` ratio replaces the assumed-from-prose 1.25–1.30 once it exists).
   `ollama/run_evidence_lane.py --dry-run` against a real (non-placeholder) pack computes
   exactly this number — it is the mechanism for this step, not a new tool to build. A
   fixture whose real dump content fails this assertion is a pack-construction problem
   to solve *before* freeze (resize the dump, or accept a smaller uniform target lane-
   wide) — never a reason to freeze anyway and let it surface as a run-time INVALID row.
5. Packs are frozen after the audit **and** this assertion are committed. **No
   regeneration loop**: if the audit finds a curation gap, that gap is data (the
   pack-omission or raw-set-gap number), not a defect to quietly fix by re-running the
   reader — but F14's assertion (step 4) is a *pre-freeze sizing gate*, not part of that
   no-regeneration rule; discovering an oversized dump before freeze and resizing it is
   exactly what step 4 exists to allow, distinct from re-curating content after a model
   row has already been scored against it.
6. At scoring time (see §11), a missed must-find item is classified into one of **four**
   buckets (gate F4), checked in this priority order:
   - `not-tool-observable` if `tool_observable` is false — excluded from the P1/P1b
     dilution comparison, still reported for transparency. No tool run, real or
     hypothetical, was ever going to surface this item.
   - `raw-set-gap` if `tool_observable` is true but `evidence_in_raw_set` is false —
     **also excluded from the P1/P1b dilution comparison**, reported separately. This is
     a lane-collection gap (pack construction didn't run the relevant tool against this
     fixture), not curation's fault and not the model's — counting it into either arm's
     comparison would misattribute the miss.
   - `pack-omission` if `evidence_in_raw_set` is true, condition is CURATED, and
     `in_curated_pack` is false — the evidence was collected but the digest dropped it.
     This is R1's number (plan §9: "the measured cost of blind curation").
   - `model-miss` otherwise — the evidence was available (in the CURATED digest, or by
     construction in DUMP, which always carries the fixture's own full raw output) and
     the model didn't report the item. **DUMP misses on tool-observable,
     raw-set-present items are always `model-miss`, never `pack-omission`** — DUMP
     carries strictly more of the fixture's own collected raw evidence than CURATED, so
     nothing about DUMP's own evidence can be "omitted" by curation.

This audit file does not exist yet for any of the 6 fixtures — building it is
pack-construction work, explicitly out of this task's scope (hard constraint: do not
build packs). `lane_manifest.yaml` declares the planned path for each fixture's audit
file (`completeness_audit_path`) and pack files (`pack_paths`) so the scorer (§11) and
the runner (gate F6, `ollama/run_evidence_lane.py`) have a stable place to look once
they exist.

---

## 11. Scorer + runner

`ollama/score_evidence_lane.py` implements §10's 4-bucket partition logic and the
must-find / FP / INVALID-passthrough scoring described in §5, matching must-find items
against `lane_manifest.yaml`'s explicit per-item `must_find_keywords` (§9.4, gate F1) —
never a generic cascade. `aggregate_by_condition` keys by `(model, condition)` (gate
F5b) with a dilution-eligible `possible` denominator (F5c); `per_item_rows` flattens to
per-item granularity for the plan's mandated flip reporting (F5d); `output_clipped`
flags `done_reason == "length"` rows (F7). Selftest (`--selftest`) now covers 17 checks:
the original partition-logic proof, a malformed-audit case (F5a), the `raw-set-gap`
bucket, per-model aggregation, `output_clipped`, and — the calibration gate F1
specifically asked for — the **real** 9 must-finds against the **real** manifest
keywords scored on a null response (all 9 score False; task report carries the run).
Still a rule-based **candidate detector**, same disclaimed limits as
`ollama/score_output.py` / `score_evalreport.py` — content-adjudication (§5/§6/§7) is a
separate, required human/opus pass.

`ollama/run_evidence_lane.py` (gate F6, owned by a separate runner-builder agent, not
authored by me) executes the local run matrix against `lane_manifest.yaml` as its only
config source. Prompt assembly order confirmed via direct coordination — §9.5.

---

## 12. Ambiguities — dispositions from the gate review's rulings, plus what's still open

Original numbering preserved for traceability; **RESOLVED** items keep their reasoning
for the record rather than being deleted.

1. **Page-shell wrapping — RESOLVED, ruling 1 ACCEPT.** Narrowest-natural-context
   confirmed as designed (§3): a uniform shell would manufacture *more* page-level false
   findings in the DUMP arm specifically — "a hidden confound biasing P3 toward its own
   prediction" (gate review).
2. **`build_fixtures.py`'s hardcoded path — RESOLVED into process, ruling 2 ACCEPT.**
   Moved from README prose into `lane_manifest.yaml`'s `preconditions:` as a named,
   owned, blocking checklist item carrying F10's 41-vs-33 SHIMS constraint (§3).
3. **Fresh re-run vs. reuse — RESOLVED, ruling 3: REUSE.** "Committed KAT driven traces
   *are* real tool output; they satisfy 'where feasible' on the merits." The live risk
   was F11 (`.findings.json` is a conclusion, not an observation), now fixed (§3) — reuse
   is strictly better with that fix in place.
4. **The "should"-collision vehicle — still hedged, ruling 4: ACCEPT the hedge, make it
   mechanical.** Not fully resolved, but no longer just prose: at lane setup, run axe
   once, grep output for `"should"`, record the actual rule id + verbatim string in
   `heading-hierarchy-skipped`'s completeness audit before freeze. If `heading-order`'s
   real wording lacks it, reassign the exercise to whichever real rule's `help` string
   does — never synthesize one (§9.3).
5. **CURATED digest freshness for `interactive-dropdown-focus-bug` — RESOLVED into a
   mechanical guard, ruling 5.** A prose rule alone was "not acceptable" per the gate.
   `lane_manifest.yaml` now carries a `digest_content_hash` field (sha256 of the frozen
   digest) that pack construction must assert differs from the Phase 2.3 receipt's
   digest — the recorded verbatim question + attested no-ground-truth authorship (F3a,
   §9.1) is what makes a wrong-provenance digest detectable in the first place.
6. **`file-input-no-labels`'s mixed evidence class — RESOLVED differently than either
   option I posed, ruling 6: fixture stays, evidence set fixed.** Per gate F4, my "3 of 4
   source-only" claim was itself wrong under the "any tool, in principle" test — only
   item [3] genuinely is. Fix: collect a keyboard/AX artifact for this fixture too (§3) —
   lifts the tool-observable pool from 6 to 8 lane-wide and resolves F9's power question
   (§6.0) directly, which neither of my two originally-posed options would have.
7. **qwen3:32b's declared-*context-window* risk — RESOLVED WITH HARD EVIDENCE, DUMP-cell
   ruling, standardize on 40,960 (§4.1).** Terminology note added on the gate's own flag:
   this item's "ceiling" always meant the model's declared *context-window* limit
   (`/api/tags` `context_length`) — a different sense from gate finding F1's "ceiling
   effect" (a *measurement* ceiling: must-find recall pinned at its maximum regardless of
   input). The two collided in this document's prose; disambiguated here rather than
   left implicit. Branch A (49,152) is dead — server-log-confirmed clamp evidence, not
   just the gate's either-way preference; see §4.1's full arithmetic and the
   `floor(n_ctx/2)+2` replication finding.
8. **Real worked adjudication-question examples — still TBD for all 6 fixtures (§9.1).**
   Unchanged: I authored the template and an illustrative schematic, not real per-fixture
   examples, because I'd already read all 6 fixtures' ground truth for §2's selection
   before this rule existed (added by the same gate review that also produced this
   disposition list). A fresh agent with no exposure to this README must author the real
   questions at pack-construction time.
9. **F2's line citations don't match this document's content at the time of gate
   review — flagged, not dismissed (§4).** Likely a stale-snapshot artifact of concurrent
   editing (this document's second addenda-fold-in pass may have landed after or during
   the gate's read), but F2's substantive requirement (a hard, probe-verified CURATED
   digest cap) was genuinely missing until this fix pass added it. Re-verification should
   confirm against *this* version.
10. **qwen3.6:35b's declared `context_length` — RESOLVED, verified-safe.** Carried
    forward from item 7 as open; the 2026-08-25 ceiling probe checked both models —
    qwen3.6:35b declares 262,144, no clamp — resolving it in the safe direction at both
    40,960 and 49,152 for this model specifically (§4.2).
11. **The glob-partial-coverage exercise (§9.3) collided with gate F11's fix** — the
    exercise's glob over `findings/*.json` matches `tabs-missing-arrow-nav`'s own
    (now-excluded) findings entry. Resolved inline (§9.3: exclude the self-match from
    the glob, or mark it NOT READ / out-of-policy in the audit) rather than left as a
    silent contradiction between two binding rules, but flagging that this is a
    same-session catch, not something the gate reviewed.
12. **F13 (new, gate-confirmed MAJOR, routed elsewhere) — the Phase 0 overflow guard is
    blind to declared `context_length`.** Surfaced by this lane's own §4.1 analysis
    ("the Phase 0.2 client-side estimate gates on the *requested* `num_ctx`, never the
    model's declared ceiling"), confirmed by the gate as a general defect that escapes
    this lane's scope — `run_benchmark.py`'s guard would wave through any request above
    a model's real ceiling as fitting, exactly this lane's original 49,152-vs-qwen3:32b
    situation. Routed to the runner-builder as a Phase 0 fast-follow (`known_risks:` in
    the manifest) — **not fixed in this lane's files, and `ollama/run_benchmark.py` is
    explicitly not touched here.**
13. **F14 (blocking, round-3 gate finding, closed in this pass) — the binding dump spec
    was stated in the wrong units.** §4.1a: the guard gates on estimated tokens
    (chars/3.5), the spec was stated in measured tokens, and the true est/measured
    overestimate on this lane's own probes is 22–30%, not the plan's documented ~7%.
    Restated the spec in estimated terms (13,764 estimated tokens of guard headroom for
    the one fixture measured so far) and added a per-fixture pre-freeze assertion to §10
    step 4. **What remains genuinely open, not resolved by this pass:** whether real DUMP
    content (mostly JSON) tokenizes densely enough to clear the guard at a 15,000-
    measured-token dump is unmeasured for all 6 fixtures — that measurement is
    pack-construction-time work (§10 step 4, `run_evidence_lane.py --dry-run`), not
    something a spec restatement alone can settle. Also not mine: correcting
    `estimate_tokens`'s docstring and the plan's guard-landing finding text is the
    runner-builder's fast-follow, referenced here, not performed.
