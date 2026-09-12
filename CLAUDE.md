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

`bug-reporting` (companion, from @mgifford's MIT [ACCESSIBILITY.md](https://github.com/mgifford/ACCESSIBILITY.md)): converts a11y-test/a11y-critic findings into reproducible bug reports with required fields (URL, XPath, HTML snippet, WCAG SC, rule ID, severity, frequency); analysis-only, sits after testing/critique. **Never route bug-report generation to a local model without a value-checking pass** — fabrication-prone on selectors/IDs. Reference script, eval lane, boundary: `docs/error-workbook-adoption-assessment.md`, `evals/results/new-local-models-2026-07/README.md`.

`acr-reporting` (report-level companion to `bug-reporting`): serializes a finished audit-scope evaluation into a **draft** OpenACR-format ACR via the routed exact-pinned `@openacr/openacr@0.3.8` CLI — never vendored, and always run `validate`/`output` **with `-c`** (bare forms silently accept nonexistent criteria / render a criteria-less shell). Output is always a DRAFT for human sign-off. The SKILL enforces the load-bearing gates — severity/term orthogonality, the untested gate, the **unattested-closure gate**, and never inventing metadata. Gate mechanics, receipts, human-verification tier, and eval history: `docs/openacr-reference.md`, `docs/openacr-adoption-assessment.md`, `docs/plans/2026-09-03-human-verification-stage-plan.md`, `evals/results/human-verification-stage/`.

`a11y-content-judgment` (**candidate** skill): draft-and-ratify pipeline for judgment-shaped criteria a scanner can't decide (2.4.2, 2.4.6, 2.4.4, 1.1.1, 3.2.4; 3.2.3 deterministic) — a hosted-tier judge plus a human ratifier. **A row is never a criterion outcome until `ratified_by` is filled**; the judge step stays hosted-tier (local = pre-sort only). Boundary and eval lane: `docs/content-judgment-adoption-assessment.md`, `evals/results/content-judgment-2026-09/`.

## Team Workflow

The `/a11y-workflow` skill orchestrates the full lifecycle by spawning specialist agents from the main session (depth-1, no nested delegation).

**Quick start:**
```
/a11y-workflow full src/components/Modal.tsx    # full lifecycle
/a11y-workflow step scout src/components/Modal.tsx  # single step
```

**Model routing**:
- Scout: Haiku (recon only)
- Reader: Haiku, escalate to Sonnet when interpretation is needed; never Opus
- Planner/Critic/Auditor: Opus (judgment-heavy — best-tier verdicts on ADVERSARIAL fixtures)
- Orchestrator: main session (sequencing, not judgment)

**Agents:**
- `a11y-scout` — Haiku, read-only. File discovery and ARIA inventory.
- `a11y-evidence-reader` — Haiku (Sonnet when interpretation needed; never Opus). Contract-shaped evidence digests.
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
- Navigate SKILL.md files over 30KB by Grep plus section reads (`offset`/`limit`) — whole-file Reads only when the edit is genuinely whole-file. Measured baseline (2026-08 session analysis): whole-file re-reads of these exact files are the single largest context cost in this repo's sessions.
- In interactive sessions, route heavy reads through the installed helpers rather than into the main context: multi-file audits/research via the `delegate` skill (subagent gets its own window), large command output via `to-file` (path + preview, not a dump). Routed, never vendored — these are claude-cost-helpers plugin skills, not repo code. When artifacts exceed the inject budget, spawn the `a11y-evidence-reader` agent for a contract-shaped digest instead of Reading the corpus.
- The critic serves at two lifecycle points — keep both documented in companion tables.
- Vital-Core adoption is limited to reporting discipline: stable evidence findings, fingerprints, trend language, and benchmark gates. Do not import scanner runtime, generated dashboard state, crawl state, Wappalyzer/ParaCharts vendors, or Lighthouse/security/sustainability engines. See `docs/vital-core-adoption-assessment.md` and `docs/a11y-evidence-finding-contract.md`.
- Audit-scope engagements follow WCAG-EM 2.0 (planner AUDIT-SCOPE MODE, a11y-test sampling discipline, `docs/a11y-evaluation-report-contract.md`; reference `docs/wcag-em-2-reference.md`). Conformance outcomes and impact severity are orthogonal — report both, never derive one from the other (register: `docs/a11y-orthogonality-register.md`). **WCAG-EM citations belong at audit scope only; an EM citation in a component-scope review is a finding against the output.** Local audit-report and operation-evidence output is detector output, never a result — read it before it leaves the building (`evals/results/wcag-em-step11/`, `evals/results/opevidence-scorer-2026-09/`).
- Declared Revised-Section-508 engagements additionally reference the **ICT Testing Baseline** (federal test-completeness standard, beside WCAG-EM at audit scope; `docs/ict-testing-baseline-reference.md`, `docs/ict-baseline-test-id-manifest.yaml`). **Baseline citations are declared-508 audit-scope only** — one in a component-scope review is a finding against the output. Reading traps: baseline text links WCAG 2.2 Understanding articles as reading aids while mapping to 508's WCAG 2.0 A/AA basis (never a 2.2 conformance mapping), and `24.A-Parsing` always passes by upstream design; the bundle's WCAG 2.2 AA default target never lowers to the 2.0 floor. Federal profile, coverage crosswalk, `baseline_test` field, and eval lane: `docs/ict-testing-baseline-adoption-assessment.md`, `evals/results/ict-baseline-phase3/` (open parity: issue #17).

## Browser Automation Tooling

The a11y-test skill has six execution modes; other a11y skills in this bundle route testing work to the same split:

- **Codified CI keyboard tests, visual regression, axe-core scans, WCAG compliance** → `npx playwright test` with `.spec.js` files. Primary path. All mandatory "real keyboard events, no synthetic events" rules apply.
- **Baseline URL-list scan** (sequential axe-core sweep across a list of URLs → per-page machine-readable evidence plus a summary JSON, no `.spec.js` authoring, not CI-embedded) → `references/baseline-url-scan.mjs` (in-repo reference script; peer deps `playwright` + `@axe-core/playwright`, installed in your own project — never in this repo). Detector output, not a conformance verdict — axe-detectable subset only (~30-40% of WCAG issue classes); never keyboard or screen-reader evidence. Sitemap-wide sweeps route to `pa11y-ci --sitemap <url> --runner axe --runner htmlcs` instead (routed, not vendored). See `docs/baseline-url-scan-adoption-assessment.md`.
- **Interactive agent-driven reconnaissance** (snapshot ARIA structure, navigate a SPA to reach a page under test, verify a single fix, capture annotated screenshots) → `agent-browser` CLI. Uses the snapshot+ref pattern (`@e1`, `@e2`) and calls CDP `Input.dispatchKeyEvent` directly, so real keyboard events are delivered.
- **Goal-driven journey audits** (live URL + task in plain words → evidence-linked WCAG findings for keyboard + emulated screen-reader personas) → `keyboard-a11y-tester` (external clone, pinned `0.5.0`, MIT). The only mode producing machine evidence for focus-indicator sufficiency, and the page/journey-level source of live-region announcement evidence (component-level → virtual-screen-reader below). Calibration: batch-crawl 4.1.3 findings are prompts to run a driven session, never failures. Routed external tool — do not vendor its runner here. See `docs/keyboard-a11y-tester-adoption-assessment.md`.
- **Component/unit screen-reader assertions** (accessible names, reading order, live-region announcements a component computes — asserted in the project's own Vitest/Jest or Storybook play functions, pre-deploy, no URL) → `@guidepup/virtual-screen-reader` (npm devDependency, exact-pinned `0.32.1`, MIT; the direct component-level lane, also the SR engine inside keyboard-a11y-tester). Never keyboard-operability evidence — interactions are synthetic (user-event). Blind spots: open shadow DOM, `aria-busy`. Calibration: mount-with-content alerts read silent (use the persistent-container pattern); never combine with fake timers (wedges the singleton). Routed npm dependency — never vendored. See `docs/virtual-screen-reader-adoption-assessment.md`.
- **Playwright MCP for keyboard events** → do not use. `browser_press_key` calls are silently dropped for most interactive widgets. Use `npx playwright test` or `agent-browser` instead.
- **Test script generation from prose specs** → `/webwright:run` or `/webwright:craft` (Claude Code plugin). LLM generates complete Python Playwright scripts from natural-language descriptions, using real `page.keyboard.press()` calls (CDP-backed). Claude Code only — not available in Codex CLI; generated `.py` files can be executed from Codex via `python3 script.py`. Do not run simultaneously with agent-browser (port conflicts).

See `.claude/skills/a11y-test/SKILL.md` for the full routing table, decision flowchart, and the interactive reconnaissance quickstart.

## Local Model Portability (Ollama)

The analysis-only skills (critic, planner, perspective-audit) run locally via Ollama with no cloud API. The `ollama/` directory contains the wrapper, benchmark tooling, and full results.

**Recommended model**: `qwen3.6:35b` (23 GB, ollama ≥0.31) — current detector recommendation (best critic/perspective/planner sweep, faster than qwen3:32b). Routing rule — **detector, not a verdict authority**: no local model's clean-code verdict is a conclusion. Never route bug-report *generation* to it without a value-checking pass (fabrication-prone on exact selectors/IDs/environment fields). Funnel history: `evals/results/new-local-models-2026-07/`, `evals/results/new-local-models-2026-08/`.

**Prior baseline / fallback**: `qwen3:32b` (18.8 GB) — same **detector, not a verdict authority** rule; the full three-lane detection and false-positive history (blind → de-hinted → post-PR-4 unassisted) is in `ollama/BENCHMARK.md`, `evals/results/ollama-rebaseline/README.md`, `evals/results/ollama-dehinted/README.md`.

```bash
python3 ollama/ollama_a11y.py critic path/to/component.jsx --model qwen3.6:35b
python3 ollama/ollama_a11y.py planner path/to/requirements.md --model qwen3.6:35b
python3 ollama/ollama_a11y.py perspective path/to/component.jsx --model qwen3.6:35b
```

Benchmarked against the critic, perspective-audit, and planner suites in full, with peer baselines for Claude API, Claude Code subagents, Codex/OpenAI, Gemini, and Ollama; raw artifacts under `evals/results/`. Full results: `ollama/BENCHMARK.md`; usage: `ollama/README.md`.

a11y-test is NOT portable — it requires Playwright, axe-core, and browser automation. Only reference knowledge ports.

## Canonical Source

This standalone repo was extracted from `zivtech-meta-skills`. If upstream source material changes, sync intentionally rather than drifting silently.
