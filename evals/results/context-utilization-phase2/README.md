# Context-Utilization Phase 2 — Evidence-Reader Delegation Receipts

Date: 2026-08-25. Branch: `feat/verification-evidence-contract`. Plan: `docs/plans/2026-08-24-context-utilization-plan.md` (Phase 2, tasks 2.1–2.4). Design notes: `docs/plans/2026-08-25-context-utilization-phase2-reader-design-notes.md`.

## What shipped

- **2.1** `.claude/agents/a11y-evidence-reader.md` (14,430 B) — opus-designed, proposal-critic gated (REVISE → all 11 findings applied same session; verdict + dispositions in design notes §6). Three-tier contract split (emit / pass-through-verbatim / never-emit), pre-read inventory coverage note, blind-reading block with verbatim-question provenance, vision mode in the same def, `tools: ["Read", "Grep", "Glob", "Bash"]` allowlist.
- **2.2** Wiring: a11y-workflow SKILL.md (+978 B) + team roster (+229 B). Inject budget defined once: **>8K measured tokens (≈32 KB on disk) → orchestrator spawns the reader**; digest + original paths travel to the consuming critic/planner; the consumer never spawns the reader (depth-1); threshold tunable pending Phase 3 rows.
- **2.3** This worked-example receipt (below).
- **2.4** Repo CLAUDE.md bullet: interactive sessions route heavy reads through `delegate`/`to-file` (routed, never vendored) and over-budget artifact sets through the reader.

## Receipt A — repo-local `tools:` allowlist verification (gate open item #1)

A separate haiku spawn of the registered `a11y-evidence-reader` type was asked to transcribe its visible tool list (probe transcript, 2026-08-25):

- **WebFetch, WebSearch, Agent, Write: all `TOOL-NOT-AVAILABLE` under a positive-control probe.** A follow-up probe (2026-08-25) explicitly instructed the registered repo-local def to *attempt* each of these tools rather than merely report its visible list; all four came back schema-absent — not addressable at all, distinct from "called and rejected." `SendMessage` was likewise absent (its own report had to be recovered from the transcript). `Read`/`Bash` delivered and working. **Confirmed: repo-local `.claude/agents/` frontmatter `tools:` allowlists are honored by this harness — config-enforced at the schema level, not prose-only.** Provenance: probe transcript `c648a303-3902-4c5a-a233-a90ffaded752.jsonl`, project sessions dir, 2026-08-25 (closes design-notes §6 open item 1; disposition in `docs/plans/2026-08-25-context-utilization-phase2-gate-review.md`). **Watch rule: re-check on harness release** — both the allowlist enforcement and the Grep/Glob deferral (below) are build properties, not permanent guarantees. (Bash remains a network-capable path; the def's prose ban covers it and says so.)
- **Caveat (harness-build property, not allowlist-stripping):** the same positive-control probe confirmed `Grep`/`Glob` — which the `tools:` allowlist *grants* — are also `TOOL-NOT-AVAILABLE`. This harness build treats Grep/Glob as deferred tools generally (the main session lacks them natively too); the allowlist is not what's stripping them. Practical consequence: the reader operates with `Read`+`Bash` only. Coverage obligations are unaffected — Execution step 2's file-granularity inventory falls back to Bash `grep`/`ls`/`find` equivalents (now stated explicitly in the def; observed working in the worked example below).

## Receipt B — worked example: reader (haiku) → critic (opus)

**Corpus** (per the gate's Q4 grading design): 6 keyboard-a11y-tester traces + 6 axe baseline-url-scan JSONs (globs), one named-but-missing path (`checkout-form.trace.json`), one oversized artifact (57 KB gemini response JSON), and axe artifacts whose `help` strings contain "should" (the verbatim-excerpt collision class).

**Question (verbatim):** "Which components in this evidence set changed ARIA state without any accessible announcement, and do the axe scans record landmark/region or label violations on the scanned pages?"
**question_source:** orchestrator, task 2.3 worked-example receipt — authored from artifact filenames and tool types only; no fixture metadata, rubrics, or ground-truth files consulted.

### Reader digest (haiku, verbatim from agent transcript)

> **Evidence class**: machine-detectable · **Answerable from artifacts read**: yes
>
> **Obs 1** `aria-state-change-no-announcement-01` — source: keyboard-a11y-tester 0.5.0, `evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json`; handle: `step[1] (step_0002)`. `#dropdown-btn` (button, `aria-haspopup="listbox"`) transitioned `aria-expanded` false→true on Enter; focus did not move; `sr_announcement.live_announcements` empty — no live-region announcement fired.
>
> **Obs 2** `axe-region-violations` — handle: `ours/summary.json, violations_by_rule[] | select(.rule_id == "region")`. 4 pages, 29 nodes, moderate; samples `.l-page__footer`, `.leftArea`.
>
> **Obs 3** `axe-landmark-violations` — handle: `... select(.rule_id == "landmark-unique")`. 3 pages, 4 nodes, moderate; samples `#product-b-nav-bar`, `#product-a-btn`, `#recursos-en-español-btn`.
>
> **Obs 4** `axe-label-violations` — handle: `... select(.rule_id | test("^label"))`. `label` (6 nodes, critical, 1 page — `.form-switch.form-check` checkbox) + `label-title-only` (3 nodes, serious, 2 pages — `#search_input`, `#location-input-nav_input`).
>
> **Absence claim:** no other components across the 6 trace files recorded ARIA state changes without announcements — query returned exactly 1 match.
>
> **Coverage note:** 6 traces READ (jq query, all files) · `checkout-form.trace.json` NOT READ (absent — no file at path) · 5 per-page axe JSONs + summary.json READ (query-scoped to landmark|region|label) · `gemini-bench-popover-no-focus-management-flash-response.json` NOT READ (out of question scope).
>
> **Not claimed:** interaction-mechanism cause; pattern correctness; root cause of missing announcements; WCAG SC mapping; severity.

### Digest grading vs the def contract (honest deviations)

| Q4 case | Exercised? | Outcome |
|---|---|---|
| (a) missing artifact | yes | NOT READ with reason — correct |
| (b) oversized artifact | partially | NOT READ, but reasoned "out of question scope" rather than flagging the 30 KB threshold — honest, wrong vocabulary |
| (c) glob > files read | no | question spanned the whole corpus, so every globbed file was legitimately read; PARTIAL grouped-row form untested — carry to Phase 3 pack construction |
| (d) "should" verbatim excerpt | no | reader quoted summary rows, not per-page `help` strings; collision clause untested |

**Grading gap (recorded, not corrected):** the digest's self-declared evidence class — `machine-detectable` (quoted transcript above) — undercounts the corpus. Obs 1 is an ARIA-state/focus observation from a keyboard-a11y-tester trace, a `name-role-state` concern; the question spanned both that and the axe machine-detectable violations, so the correct classification was `mixed` (name-role-state + machine-detectable). The quoted transcript above is not rewritten — it is what the model actually returned — but this is a known grading gap for Phase 3 pack construction to watch for when grading evidence-class self-declarations.

Further deviations: Obs 1's evidence block **condensed** the raw step (arrays summarized, keys re-ordered) rather than quoting verbatim — exactly the fidelity class the def's verbatim-excerpt rule targets; the consuming critic's targeted lookup (below) is the check that caught/absorbed it. Tools used: Bash + Read only (no Glob — see Receipt A caveat).

### Consuming critic (opus) — findings citing digest handles

**Verification (targeted lookup at the cited handle).** One `jq '.steps[1]'` on `interactive-dropdown-focus-bug.trace.json` (11,107 B; one step read, not the file). Digest was faithful — and under-claimed: raw `sr_announcement` is `{new_phrases: [], live_announcements: [], focus_announcement: null}`, supporting the stronger claim that nothing was announced on any channel. Condensation lost precision but introduced no error. **One material correction to the framing:** raw `ax_name_role_state.states` shows the button correctly wired (`hasPopup: "listbox"`, `controls: "dropdown-list"`, `expanded: true`, `name: "Sort by"`) — so "no announcement of the state change" would overclaim; the defect the step proves is narrower: `focus_moved: false` with no `activedescendant` — the popup opened and nothing moved into it.

**Finding 1 — `dropdown-popup-focus-not-moved-01` (MAJOR; keyboard=HIGH, screen-reader=HIGH).** Rests on `observation_id: aria-state-change-no-announcement-01`, handle `interactive-dropdown-focus-bug.trace.json, step[1] (step_0002)`. WCAG 2.2 SC 4.1.2 (A) + WAI-ARIA APG listbox-button pattern: `aria-expanded` flips false→true on Enter but focus stays on the trigger and no `aria-activedescendant` is set — the pattern is ~80% complete (relationship attributes right, operability half missing). Fix: `listbox.focus()` with roving tabindex, or `aria-activedescendant` on the button updated by Arrow keys; Escape restores focus. Fingerprint marked NOT-recomputed (hashing scheme not in context) — recompute before filing. Calibrated MAJOR not CRITICAL (state exposed on the focused element; correct `aria-controls` wiring mitigates); upgrades to CRITICAL if steps 3+ of the same trace show options unreachable by any key — a one-step lookup to run before filing.

**Finding 2 — label defects (digest-only, deliberately unverified).** Rests on `observation_id: axe-label-violations`, same handle as digest. `label` (6 nodes, critical, unnamed `.form-switch.form-check` toggle) → SC 4.1.2 + 1.3.1 (A), CRITICAL pending DOM verification; `label-title-only` (`#search_input`, `#location-input-nav_input`) → SC 2.4.4/4.1.2 + 3.3.2 (A), MAJOR — the repo's documented title-vs-`aria-label` anti-pattern on primary task-entry controls. `region`/`landmark-unique` NOT promoted (ENHANCEMENT tier — bypass-block friction, not access loss); noted that step_0002's `region.landmark: null` corroborates the axe `region` rule from an independent tool — a cross-link the reader correctly could not make (it extracts, it does not correlate).

**Consumption note (critic's own).** 12 artifacts stayed out of the critic's window; it opened ~1.1 KB of one 11 KB file. One digest field was insufficient: Obs 1's condensed evidence dropped the `ax_name_role_state.states` dict — the field the WCAG mapping turns on. **Without the targeted lookup the critic would have filed a 4.1.3 Status Messages finding, which the raw artifact proves wrong** (state is exposed on the focused element; the real gap is 4.1.2 + APG operability). The digest's phrasing was accurate but invited the misread. NOT-READ rows did not affect confidence (missing file removes nothing; gemini artifact out of scope; the absence claim properly scoped to the 6 queried traces). Finding 2 is flagged digest-only rather than dressed as verified. Reader-contract tweak adopted from this: **for ARIA-state observations, carry the full `states` dict verbatim** (applied to the def same day, see below).

## Routing consequence

The pattern works end-to-end at haiku→opus: the consumer never ingested the corpus, the coverage note carried the missing/oversized artifacts honestly, and the division of labor held (reader reported, critic judged). The receipt's headline lesson: **haiku excerpt condensation is real and it invited a concrete wrong finding (4.1.3 instead of 4.1.2) that the mandatory targeted lookup caught** — the digest is detector output for evidence, not a substitute for the handle; the consumer's per-finding lookup at the cited handle is load-bearing, not optional. One def amendment adopted from the receipt same day: ARIA-state observations must carry the full `states` dict verbatim. Cases (c)/(d) remain untested; Phase 3 pack construction must exercise both (design notes §6).
