# accessibility-skills

This repository contains the standalone Accessibility Skills (accessibility-skills) bundle — planner, critic, tester, and perspective auditor — plus cross-model benchmark assets. Claude Code is one supported install/runtime surface; the evals and runners now compare Claude, Codex/OpenAI, local Ollama models, and other hosted model families as peer baselines.

## Dead Output

**What dead looks like in this repo:**
- Accessibility reviews that pattern-match ARIA attributes without testing whether the interaction actually works for the user. A finding that says "missing aria-label" without explaining what a screen reader user would experience is dead.
- Plans that cite WCAG success criteria by number without engaging with the actual user experience they protect. "Violates 4.1.2" is a citation, not a finding.
- Findings rated CRITICAL because the checklist says so, not because a real user would be blocked. Severity must reflect impact on people, not rule weight.
- Eval fixtures that test whether the skill finds the planted bug without testing whether it avoids false alarms on clean code. A critic that flags everything is dead — it just looks thorough.

Three rules:
- **Name it when you see it.** If a review, plan, or finding is dead — checking boxes rather than thinking about the person who'll interact with the UI — say so.
- **Friction is the job.** If the planner's recommendations don't fit the component's actual interaction pattern, push back. If a critique applies a pattern from the APG that doesn't match the use case, say so.
- **Watch for rank erosion.** Accessibility guidance that gets summarized into checklists loses the "why." If the output could be produced by a linter, it's not earning its place as a skill.

## Lifecycle

The critic serves at **two checkpoints** in the accessibility development lifecycle, with role-audit available at two additional points:

```
plan → [role audit: design] → critique plan → [perspective audit] → revise → implement → test → [role audit: code] → critique implementation → [perspective audit] → fix → re-test
```

| Step | Skill | Role |
|------|-------|------|
| 1. Plan | a11y-planner | Design accessibility before coding |
| 1b. Role audit (design) | a11y-role-audit | Review plan from team responsibility lenses (optional) |
| 2. Critique plan | a11y-critic | Review plan for gaps before implementation |
| 2b. Perspective audit | perspective-audit | Deep review of MEDIUM/HIGH alarm perspectives (if escalated) |
| 3. Revise | manual | Address critic findings |
| 4. Implement | executor | Build according to reviewed plan |
| 5. Test | a11y-test | Automated scans + keyboard tests (Playwright); journey audits (keyboard-a11y-tester); component SR assertions (virtual-screen-reader) |
| 5b. Role audit (code) | a11y-role-audit | Review implementation from team responsibility lenses (optional) |
| 6. Critique implementation | a11y-critic | Review design decisions after tests pass |
| 6b. Perspective audit | perspective-audit | Deep review of escalated perspectives (if escalated) |
| 7. Fix | executor | Address findings |
| 8. Re-test | a11y-test | Verify fixes |

The three audit dimensions are orthogonal:
- **a11y-critic**: "Is the accessibility approach sound?" (design quality)
- **perspective-audit**: "Who is blocked?" (access-method perspectives — screen reader, keyboard, low vision...)
- **a11y-role-audit**: "Who on the team owns this?" (ARRM responsibility roles — designer, developer, content author...)

## Skills

| Skill | Type | Command |
|-------|------|---------|
| a11y-workflow | orchestrator | `/a11y-workflow` |
| a11y-planner | planner | `/a11y-planner` |
| a11y-critic | critic | `/a11y-critic` |
| a11y-test | tester | `/a11y-test` |
| perspective-audit | auditor | `/perspective-audit` |
| a11y-role-audit | role auditor | `/a11y-role-audit` |
| bug-reporting | reporter | `/bug-reporting` |
| acr-reporting | ACR serializer | `/acr-reporting` |
| a11y-content-judgment | draft-and-ratify judge | `/a11y-content-judgment` |
| maintain-accessibility-skills | repository maintainer | `/maintain-accessibility-skills` |

`bug-reporting` is a companion skill (contributed by @mgifford, derived from the MIT-licensed [ACCESSIBILITY.md](https://github.com/mgifford/ACCESSIBILITY.md) guide): it converts findings from a11y-test runs or a11y-critic reviews into reproducible bug reports with required fields (URL, XPath, HTML snippet, WCAG SC, rule ID, severity, frequency). It sits after testing/critique in the lifecycle — findings go in, filable issues come out. Analysis-only; eval lane added 2026-07-17 (`evals/suites/bug-reporting/`: 7 fixtures — axe-core/pa11y/keyboard-a11y-tester/manual-prose inputs plus the declared-508 `axe-button-name-federal` added 2026-08-12 — rule-based scorer `ollama/score_bugreport.py` with recomputed stable-ID, fabrication, and manifest-validated `baseline_test` checks; the FILED baseline value is compared, never mere mention — first declared-508 rows 2026-08-12: qwen3.6:35b filed `5.A-ControlName` correctly but FAILed on its documented value-fidelity classes; the qwen3:32b control filed the wrong-but-valid near neighbor `5.C-ControlState` for a NAME defect, the filed-value check's first live catch). First model rows landed in the July 2026 funnel (`evals/results/new-local-models-2026-07/`): qwen3.6:35b 1 PASS / 1 WARN / 4 FAIL — report structure perfect, every failure is value fidelity (dropped exact selectors, 0 recomputed stable IDs verified, two fabrications), the origin of the never-route-generation-without-a-value-check caveat above; laguna-s 0/6 with fabrications on 5, the funnel's worst data fidelity. Its one reference script, `references/build-error-workbook.mjs` (PT-18, 2026-09-03), serializes schema-shaped reports into a client-triage XLSX workbook and `--verify`s a built workbook cell-by-cell against its input — routed `exceljs@4.4.0` peer dependency in the consuming project, never vendored; boundary and receipts in `docs/error-workbook-adoption-assessment.md`.

`acr-reporting` is the report-level companion to `bug-reporting` (finding→issue there; evaluation-report→ACR here): it serializes a **finished audit-scope evaluation** (report contract + evidence-contract findings) into a draft Accessibility Conformance Report in GSA's OpenACR format, validated and rendered via the routed exact-pinned `@openacr/openacr@0.3.8` CLI — never vendored, and **always with `-c`**: bare `validate -f` is schema-shape only (accepts nonexistent criteria) and bare `output` silently renders a criteria-less shell (both Phase 2 discoveries, reproduced; receipts in `docs/openacr-reference.md`). Finish surface is human: acreditor.section508.gov for 2.1-catalog drafts (the editor cannot import the 2.2 catalogs the frozen format itself ships — live skew, watch rule on editor releases), CLI HTML for 2.2. The skill's gates are load-bearing because the official toolchain validates boilerplate: outcome→term mapping with severity strictly orthogonal, the untested gate (`not-evaluated` is AAA-only; untested/cantTell A/AA → INCOMPLETE draft with marker + gap list), catalog A/AA completeness, canonical sample-scoped note forms citing real `finding_id`s, value provenance (never invent contacts/dates/versions; absent `license` renders as CC-BY-4.0 by schema default — surfaced at handoff), and the dual-catalog annex (measured 2.2-only outcomes never dropped). Eval lane added 2026-08-12 (`evals/suites/acr-reporting/`: 4 fixtures — the serialization chain one step downstream of `transit-portal-q3`, orthogonality+annex, untested gate, clean FP control — scorer `ollama/score_acr.py` invokes the pinned CLI and carries the checks it provably lacks; calibrated 9/9 before any row). **Phase 2 gate PASSED same day**: opus subagents 8/8 must-clean across 2 draws on all four fixtures; the A/B baselines FAIL draw-stably with zero term-mapping misses and zero fabrications — bare opus judges correctly, so what the skill carries is the machine contract (schema exactness, component policy, canonical stems), not the judgment; the qwen3.6:35b detector row FAILed at the structural gate (canonical note stems emitted as unquoted colon-bearing scalars — the YAML doesn't parse), so local drafts stay detector output behind the mandatory hosted/human value-and-validate pass (receipts: `evals/results/acr-reporting-phase2/`). Lane B (claims audit of third-party ACRs, a11y-critic adjudicating) and Lane C (drift diffs) are Phases 3–4 of `docs/plans/2026-08-12-openacr-integration-plan.md`; boundary ruling in `docs/openacr-adoption-assessment.md`.

`a11y-content-judgment` is a **candidate** skill (promoted 2026-09-02 from one engagement run; the bar's fixture-before-skill-text order was violated, so the remedy is a blind-authored eval lane): a draft-and-ratify pipeline for the judgment-shaped criteria a scanner cannot decide (2.4.2, 2.4.6, 2.4.4, 1.1.1, 3.2.4; 3.2.3 deterministic) — inventory + builder scripts (playwright peer dep, never vendored), a hosted-tier judge bound to `references/judgment-rubric.md`, a human ratifier; a row is never a criterion outcome until `ratified_by` is filled. Eval lane added 2026-09-02 (`evals/suites/a11y-content-judgment/`: six fixtures blind-authored from W3C technique text and run through the skill's own pipeline — 40 must rows, calibration-tier rows reported never counted, invalid rows disclosed; scorer `ollama/score_content_judgment.py` with contract-priced vs rubric-priced checks; conditions `cj` = rubric as system prompt vs `cj-baseline`). First rows same day (`evals/results/content-judgment-2026-09/`): opus found every planted defective row in every rubric draw and the rubric carries the card-grid link detection bare opus misses (2/7 → 7/7), but one draw-stable false alarm — a "Learn more" inside a sentence naming its destination — traced to the rubric reasoning from 2.4.9 (AAA) at an AA target; the AA restatement proved undecidable from the flattened row context, so rubric v0.3 routes other-sentence context to `unsure` for the human (draw 5 must-clean; capture changes for full decidability are a follow-up PR). Both critic passes (a11y-critic, test-critic) were REVISE and are folded; verdicts verbatim in the results dir. The qwen3.6:35b detector row judged every "Learn more" yes: judge step stays hosted-tier, local = pre-sort only. Boundary ruling: `docs/content-judgment-adoption-assessment.md`.

## Team Workflow

The `/a11y-workflow` skill orchestrates the full lifecycle by spawning specialist agents from the main session (depth-1, no nested delegation).

**Quick start:**
```
/a11y-workflow full src/components/Modal.tsx    # full lifecycle
/a11y-workflow step scout src/components/Modal.tsx  # single step
```

**Model routing** (validated on 8 hard fixtures, 2026-05-19):
- Scout: Haiku (recon only)
- Planner/Critic/Auditor: Opus (judgment-heavy — best-tier verdicts on ADVERSARIAL fixtures)
- Orchestrator: main session (sequencing, not judgment)

**Agents:**
- `a11y-scout` — Haiku, read-only. File discovery and ARIA inventory.
- `a11y-planner` — Opus, no Bash. 9-phase accessibility design.
- `a11y-critic` — Opus, read-only. 8-phase investigation protocol.
- `perspective-audit` — Opus, read-only. 7-perspective deep review (escalation only).
- `a11y-role-auditor` — Opus, read-only. 6-role ARRM-based responsibility review.

See `.claude/teams/a11y-workflow.md` for full team definition and escalation signals.

## Structure

- `.claude/skills/*/SKILL.md` — installable skill definitions
- `.claude/skills/*/references/external-skills-manifest.yaml` — external skill references
- `.claude/agents/*.md` — companion agent prompts
- `.agents/skills/*/SKILL.md` — Codex-compatible skill mirrors
- `.codex/agents/*.toml` — Codex agent definitions for planner/critic
- `roles/` — ARRM-based role definitions and task mapping (see below)
- `docs/` — per-skill documentation and external skills inventory
- `docs/EXTERNAL-SKILLS-INVENTORY.md` — landscape scan of 13 external a11y skills with adoption recommendations
- `templates/` — copied base protocol templates required by the skills
- `evals/suites/` — bundled fixture and rubric assets
- `ollama/` — local model portability layer (see below)

## Working In This Repo

- Use `/maintain-accessibility-skills` for tracked-file hygiene gates, history-rewrite verification, mixed-commit surgery, and recovery of commits made on the local default branch.
- Treat this as a prompt-only repository.
- Keep skill files installable from the repo root.
- Preserve the companion relationship between planner, critic, and perspective-audit.
- Prefer targeted edits over large rewrites.
- The critic serves at two lifecycle points — keep both documented in companion tables.
- Vital-Core adoption is limited to reporting discipline: stable evidence findings, fingerprints, trend language, and benchmark gates. Do not import scanner runtime, generated dashboard state, crawl state, Wappalyzer/ParaCharts vendors, or Lighthouse/security/sustainability engines. See `docs/vital-core-adoption-assessment.md` and `docs/a11y-evidence-finding-contract.md`.
- Audit-scope engagements follow WCAG-EM. The planner's AUDIT-SCOPE MODE, a11y-test's audit sampling discipline (structured + 10% random + representativeness check + complete processes), and `docs/a11y-evaluation-report-contract.md` (whose Appendices A and B carry non-normative serialization examples for `sample_set` and `ratified_receipt` — single-source, so examples only; no validator enforces either until a second instance exists) implement WCAG-EM 2.0 (verified reference: `docs/wcag-em-2-reference.md`; adoption boundary: `docs/wcag-em-2-adoption-assessment.md`). Conformance outcomes and impact severity are orthogonal — report both, never derive one from the other. The full orthogonality register — five further axis pairs and the `claim_boundary` machine mechanism that makes the rule checkable — is in `docs/a11y-orthogonality-register.md`. WCAG-EM citations belong at audit scope only; treat an EM citation in a component-scope review as a finding against the output. The report contract has an eval lane (`evals/suites/evaluation-report/`, added 2026-08-01): the chain fixture `transit-portal-q3` grades aggregation of finished audit evidence into the contract's shape, contract-as-system-prompt vs no-contract baseline, rule-based scorer `ollama/score_evalreport.py`; instrument calibrated, first rows same day (qwen3.6:35b ×2 draws + qwen3:32b control, `evals/results/wcag-em-step11/`): the A/B direction is draw-stable — every baseline draw FAILs on report shape (the outcome map, boundary declaration, and sampling method don't exist without the contract) — but the 35b contract verdict is not (WARN d1 → FAIL d2: draw 2 silently dropped all severity data, the model's known data-fidelity class at must-tier magnitude). Routing consequence: a local contract-condition report is detector output — read it before it leaves the building. The **operation-evidence** lane (`evals/suites/a11y-test-operation-evidence/`, 4 fixtures incl. a mixed package and a clean control) got its rule-based scorer 2026-09-02 (`ollama/score_operation_evidence.py`, over the Structured disposition block in `a11y-test/SKILL.md` — reporting mechanized, rule selection still the model's judgment; 34 smoke canaries incl. an over-flag canary): opus calibration 8/8 must-clean across two draws with baselines failing structurally; first qwen3.6:35b row 2/4 — invented operation ids on op-empty and `BLOCKED`-for-`UNTESTED` on op-dialog, zero fabricated rule ids (`evals/results/opevidence-scorer-2026-09/`). Routing consequence: a local disposition block is a candidate, never a result.
- Declared Revised-Section-508 engagements additionally reference the **ICT Testing Baseline** — the federal test-completeness standard (what minimum tests a 508 conformance test process must include), sitting beside WCAG-EM at audit scope, not on top of it (verified reference: `docs/ict-testing-baseline-reference.md`; test-ID ground truth: `docs/ict-baseline-test-id-manifest.yaml`; adoption boundary: `docs/ict-testing-baseline-adoption-assessment.md`). Same scope rule as EM: baseline citations belong to declared-508 audit scope only — treat a baseline citation in a component-scope review as a finding against the output. Reading traps: baseline text links WCAG 2.2 Understanding articles as reading aids while mapping to 508's WCAG 2.0 A/AA basis (never a 2.2 conformance mapping), and `24.A-Parsing` always passes by upstream design. The bundle's WCAG 2.2 AA default target never lowers to the federal 2.0 floor. Phase 2 wired 2026-08-12 (critic-gated): the planner FEDERAL PROFILE in AUDIT-SCOPE MODE — the conformance floor declaration is the scope gate, and under it the EM `conformance_target` is the floor itself ("Revised Section 508: WCAG 2.0 A/AA + named provisions") while 2.2 AA stays the recommendation layer; the hand-built a11y-test coverage crosswalk (`.claude/skills/a11y-test/references/ict-baseline-crosswalk.yaml` — 62 web tests → execution modes, 22 covered / 26 partial / 13 not-covered / 1 always-passes; the not-covered rows are the deliverable); the optional manifest-validated `baseline_test` finding/bug-report field (17.A–C cite 503.4.x provisions in place of a WCAG SC); and the report contract's optional federal annex (failed rows derive from findings' `baseline_test`, never SC fan-out). The Phase 3 eval lane landed 2026-08-12 (critic-gated, calibrated, no model rows yet): de-hinted federal planner fixture #27 (`test-federal-agency-audit`; conditions `planner-federal` = crosswalk in-prompt vs `planner` = withheld), declared-508 bug-report fixture #7 (`axe-button-name-federal`, valid ID list supplied in-input), and manifest-validated `baseline_test` fidelity checks across the planner/bug-report/critic scorers — fabrications, out-of-scope citations, and trap-marker hits force non-PASS, and the keyword gate is polarity-blind by measurement, so every gate row is detector output (receipts: `evals/results/ict-baseline-phase3/`). Baseline-ID generation may now be routed WITH the value check, never without it. First local rows landed same day (six rows, adjudicated — receipts README): zero fabricated baseline IDs anywhere; the live fabrication risk is invented COUNTS (32b no-crosswalk claimed "54/62 web / 45/57 PDF baseline tests performed" — a documents capability the stack lacks — where 35b hedged an unfilled "N of 62"); the filed-value check's first live catch was 32b filing wrong-but-valid `5.C-ControlState` for a NAME defect; and one trap-marker false-fire on concede-then-refute phrasing was adjudicated correct (instrument-rev candidate). Claude subagent rows (same day): opus 11/11 PASS in both conditions (federal = all 62 IDs cited, exact crosswalk transcription; withheld = honest unfilled "N of 62"), sonnet bugreport WARN with the lane's first-ever 2/2 verified stable IDs — via protocol-from-SKILL.md because the a11y-planner agent-def predated Phase 2 (drift repaired same day: FEDERAL PROFILE synced to both planner agent defs, the critic defs' equivalent Phase 0 + evidence-wording gaps closed, and a marker-based skills-vs-agent-def drift check wired into `scripts/check_mirrors.py` strict CI). Codex/Gemini/Claude-API rows + cloud `planner-federal` condition parity remain open on issue #17.

## Browser Automation Tooling

The a11y-test skill has six execution modes; other a11y skills in this bundle route testing work to the same split:

- **Codified CI keyboard tests, visual regression, axe-core scans, WCAG compliance** → `npx playwright test` with `.spec.js` files. Primary path. All mandatory "real keyboard events, no synthetic events" rules apply.
- **Baseline URL-list scan** (sequential axe-core sweep across a list of URLs → per-page machine-readable evidence plus a summary JSON, no `.spec.js` authoring, not CI-embedded) → `references/baseline-url-scan.mjs` (in-repo reference script, promoted 2026-08-14 from a one-off EPA public-sites harness that ran 40 views; peer deps `playwright` + `@axe-core/playwright`, installed in your own project — never in this repo). Detector output, not a conformance verdict — axe-detectable subset only (roughly 30-40% of WCAG issue classes); never keyboard or screen-reader evidence. Sitemap-wide sweeps route to `pa11y-ci --sitemap <url> --runner axe --runner htmlcs` instead (routed, not vendored). See `docs/baseline-url-scan-adoption-assessment.md`.
- **Interactive agent-driven reconnaissance** (snapshot ARIA structure, navigate a SPA to reach a page under test, verify a single fix, capture annotated screenshots) → `agent-browser` CLI. Uses the snapshot+ref pattern (`@e1`, `@e2`) and calls CDP `Input.dispatchKeyEvent` directly, so real keyboard events are delivered. Verified on both vanilla JS (WAI-ARIA APG disclosure) and React state (react.dev DocSearch Meta+K).
- **Goal-driven journey audits** (live URL + task in plain words → evidence-linked WCAG findings for the keyboard + emulated screen-reader personas) → `keyboard-a11y-tester` (external clone, pinned to release `0.5.0`, MIT). Deterministic Playwright/CDP runner plus an agent-driven `serve`/`step` loop; emits trace/findings/reading-order-census artifacts, is the only mode producing machine evidence for focus-indicator sufficiency, and is the page/journey-level source of live-region announcement evidence (component-level goes to virtual-screen-reader below). Cross-validated against the 33 critic fixtures 2026-07-10 (`evals/results/keyboard-a11y-tester/`). Calibration: batch-crawl 4.1.3 findings are prompts to run a driven session, never failures. Adoption boundary: routed external tool — do not vendor its runner into this repo. See `docs/keyboard-a11y-tester-adoption-assessment.md`.
- **Component/unit screen-reader assertions** (what does a screen reader compute and announce for this component — accessible names, reading order, live-region announcements — asserted in the project's own Vitest/Jest suite or Storybook play functions, pre-deploy, no URL) → `@guidepup/virtual-screen-reader` (npm devDependency, exact-pinned `0.32.1`, MIT). Already the transitive SR engine inside keyboard-a11y-tester; this is the direct component-level lane. Validated in-repo 2026-07-11 (plain jsdom, Vitest 4, real Chromium ESM) and 2026-07-13 (Storybook 10.4.6 addon-vitest lane). Never keyboard-operability evidence — its interactions are synthetic (user-event). Blind spots: open shadow DOM, `aria-busy`. Calibration: mount-with-content alerts read silent (assert via the persistent-container pattern); never combine with fake timers (wedges the singleton). Adoption boundary: routed npm dependency in consuming projects — never vendored. See `docs/virtual-screen-reader-adoption-assessment.md`.
- **Playwright MCP for keyboard events** → do not use. `browser_press_key` calls are silently dropped for most interactive widgets. Use `npx playwright test` or `agent-browser` instead.
- **Test script generation from prose specs** → `/webwright:run` or `/webwright:craft` (Claude Code plugin). LLM generates complete Python Playwright scripts from natural language descriptions. Benchmarked 25/25 on WAI-ARIA APG examples (dialog focus trap, tabs, axe-core injection, menu navigation, ARIA tree inspection). Uses real `page.keyboard.press()` calls (CDP-backed). Claude Code only — not available in Codex CLI; generated `.py` files can be executed from Codex via `python3 script.py`. Do not run simultaneously with agent-browser (port conflicts).

See `.claude/skills/a11y-test/SKILL.md` for the full routing table, decision flowchart, and the interactive reconnaissance quickstart.

## Local Model Portability (Ollama)

The analysis-only skills (critic, planner, perspective-audit) run locally via Ollama with no cloud API. The `ollama/` directory contains the wrapper, benchmark tooling, and full results.

**Recommended model**: `qwen3.6:35b` (23 GB, ollama ≥0.31) — new detector recommendation as of 2026-07-29 (July new-model funnel, `evals/results/new-local-models-2026-07/`): first-ever full critic sweep (68/68 must-find vs the prior champion's 65/68), perspective 36/37, planner 25/25, faster than qwen3:32b. Same routing rule as ever — **detector, not a verdict authority**: Stage 3 ×3-draw CLEAN characterization failed the promotion bar for both 35b and the qwen3:32b same-day control, so no local model's clean-code verdict is a conclusion. Data-fidelity caveat: never route bug-report *generation* to it without a value-checking pass (fabrication-prone on exact selectors/IDs/environment fields). `qwen3:32b` remains the fallback baseline with three lanes of history below. The funnel reopened once on its watch-triggers (2026-08-23, Qwen 3.8 open weights): `qwen3.8:27b` **stopped at Stage 1** — champion-equal detection (15/15 adjudicated) but a stochastic /think stall (0-char response at `done_reason=stop`, retry recovered clean) failed the zero-incompletions gate, plus ADVERSARIAL severity overshoot and ~12 tok/s on the default MTP tag; recommendation unchanged (receipts: `evals/results/new-local-models-2026-08/`).

**Prior baseline**: `qwen3:32b` (18.8 GB) — strongest local model across the three 2026-07 lanes (blind → de-hinted → post-PR-4 unassisted), with calibrated caveats. Detection: critic must-find 67/68 → 65/68 content-adjudicated across consecutive draws — byte-identical prompts flip 2–3 items at temperature 0.3, so treat single-lane deltas as variance until adjudicated; perspective detection 36/37 → 34/37, with exactly one item proven hint-carried (the map-interface-zoom target-size defect, absent in both de-hinted draws) and one first-ever HAS-BUGS FAIL on a byte-identical prompt (checkout-form 1/3 — variance at fixture-FAIL magnitude). False positives: the historical "zero CLEAN false positives" was verdict-assisted — the first unassisted draw (post-PR-4 corpus, 2026-07-19) drew a wrong REVISE on button-skip-link-clean plus structured findings on two more of the four critic CLEAN fixtures, and perspective CLEAN verdicts ran 4/5 → 1/5 → 4/5 wrong across the three draws (media-player-captions wrong in all three, nav-menu-landmarks page-shell over-flagging in all three; no other CLEAN fixture has a stable outcome). Perfect planner scores. Routing rule: qwen3:32b is a **detector, not a verdict authority** — use it to surface candidate findings; never take a single local verdict on clean code as a conclusion (receipts: `evals/results/ollama-rebaseline/README.md`, `evals/results/ollama-dehinted/README.md`, and the disclosures in `ollama/BENCHMARK.md`).

```bash
python3 ollama/ollama_a11y.py critic path/to/component.jsx --model qwen3.6:35b
python3 ollama/ollama_a11y.py planner path/to/requirements.md --model qwen3.6:35b
python3 ollama/ollama_a11y.py perspective path/to/component.jsx --model qwen3.6:35b
```

Benchmarked against the 33 critic fixtures, 25 perspective-audit fixtures, and 25 planner fixtures in full, with cross-platform baselines for Claude API, Claude Code subagents (planner lane, 25/25 PASS), Codex/OpenAI, Gemini (CLI lane, 31/33 critic PASS), and local Ollama models. The planner suite grew to 26 fixtures on 2026-08-01 (`test-hybrid-product-audit`, the de-hinted audit fixture from adoption-plan step 11a — every 25/25 row predates it; first rows same day: qwen3.6:35b 7/11 → 9/11 across two draws (NEEDS REVIEW → PASS at documented item-flip magnitude; both draws pass the central false-coverage trap), and the qwen3:32b control — 11/11 draw-stable on the hinted sibling — scores 3/11 with real absences: the old saturation was fixture-cueing, proven on the same model. Receipts in `evals/results/wcag-em-step11/`). The suite reached 27 on 2026-08-12 (`test-federal-agency-audit`, the de-hinted declared-508 fixture from ICT baseline Phase 3; first rows same day: 35b 10/11 federal-condition PASS vs 9/11 no-crosswalk with an honestly-unfilled coverage count, 32b control 10/11 vs 7/11 with fabricated counts — `evals/results/ict-baseline-phase3/`). Hosted-run raw artifacts are committed under `evals/results/` — every hosted family is a first-class peer row. See `ollama/BENCHMARK.md` for full results and `ollama/README.md` for usage.

a11y-test is NOT portable — it requires Playwright, axe-core, and browser automation. Only reference knowledge ports.

## Canonical Source

This standalone repo was extracted from `zivtech-meta-skills`. If upstream source material changes, sync intentionally rather than drifting silently.
