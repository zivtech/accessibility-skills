# The skills

Twelve skills ship in `.claude/skills/`. Nine are for doing accessibility work; three are for working on this repository.

Each has a Codex-compatible mirror under `.agents/skills/`, kept byte-identical by `scripts/check_mirrors.py --strict` in CI. The one declared exception is `a11y-planner`, whose eight-line Claude/Codex terminology divergence is pinned by count and content fingerprint in the script's `PARITY_EXEMPTIONS`; changing it fails the gate until the record is updated. (`a11y-role-audit` has a Codex mirror too, but a deliberately condensed one, declared as a non-mirror pair.)

---

## Lifecycle skills

### `a11y-planner` — design it before you build it

The pre-implementation design surface. Produces a plan covering semantic structure and landmarks, APG pattern choice, keyboard behaviour and focus management, state communication for assistive technology, visual concerns (contrast, motion, resize), content strategy, and how the result will be tested.

Nine phases: scope and context → semantic structure → interaction pattern → focus management → state communication → visual accessibility → content accessibility → testing strategy → implementation tasks.

**AUDIT-SCOPE MODE** switches it from component design to WCAG-EM evaluation planning: scope declaration, conformance target, accessibility support baseline, sample selection. Under a declared Revised Section 508 engagement, the **FEDERAL PROFILE** additionally gates every ICT Testing Baseline citation behind a conformance floor declaration.

### `a11y-critic` — review the design, twice

Reviews accessibility design decisions at **two** lifecycle points: after planning, to catch gaps before code is written, and after testing, to check that passing automated checks did not hide broken design.

It looks for semantic mismatches between intent and structure, incomplete ARIA pattern implementations, broken focus traps and restoration, missing live regions, low-vision and cognitive friction, and the gaps that pass axe-core while still failing real users.

Eight-phase protocol, evidence-backed severity, and a mandatory multi-perspective pass across screen reader, keyboard-only, low-vision, and cognitive lenses. A finding without evidence of what the user would actually experience is not a finding.

### `a11y-test` — measure it

The measurement layer. Produces the evidence the critic reviews. Six execution modes, routed by what you are actually asking:

| Mode | Use it for |
|---|---|
| `npx playwright test` | Codified CI keyboard tests, axe-core scans, visual regression. **Primary path** |
| `references/baseline-url-scan.mjs` | Sequential axe-core sweep over a URL list; per-page evidence, no spec authoring |
| `agent-browser` | Interactive reconnaissance — snapshot ARIA structure, reach a page, verify one fix |
| `/webwright:run` | Generating complete Python Playwright scripts from prose. Claude Code only |
| `keyboard-a11y-tester` | Goal-driven journey audits of live URLs; the only mode producing focus-indicator sufficiency evidence |
| `@guidepup/virtual-screen-reader` | Component-level screen-reader assertions in your own Vitest/Jest/Storybook suite, pre-deploy, no URL |

**Do not use Playwright MCP for keyboard events** — `browser_press_key` is silently dropped for most interactive widgets.

**The human tier.** Two things no execution mode produces: the fixed-stage confirmation that lets a fix-closure record carry its `attestation` block (what `acr-reporting` admits an improved conformance term on), and the evidence for the 13 ICT baseline rows the stack does not cover. Both come from a named person walking the campaign's planned operation set — never a free walk — and recording `before` / `action` / `expected` / `observed` per operation in a shape the five operation-evidence admissibility rules can read, or the attended-media shape for the alternative-content rows: [`references/human-verification-walkthrough.md`](../.claude/skills/a11y-test/references/human-verification-walkthrough.md). It is the one place a single PASS is the unreliable result: a fixed-stage `supports` needs a second confirmation, a single FAIL sends the item back on its own.

Two boundaries worth stating plainly. A clean axe-core scan is not conformance: it covers roughly 30–40% of WCAG issue classes and is never keyboard or screen-reader evidence. And virtual-screen-reader's interactions are synthetic, so it is never keyboard-operability evidence.

Full tool inventory with pins and blind spots: [tools.md](tools.md). Adoption boundaries and cross-validation records: [baseline-url-scan](baseline-url-scan-adoption-assessment.md), [keyboard-a11y-tester](keyboard-a11y-tester-adoption-assessment.md), [virtual-screen-reader](virtual-screen-reader-adoption-assessment.md).

### `perspective-audit` — who is blocked?

Deep review from seven disability and situational access perspectives. Runs on escalation: when the planner or critic flags a perspective at MEDIUM or HIGH alarm, that perspective gets a focused pass.

- **Magnification & reflow** — zoom, reflow at 320px, target sizing
- **Environmental contrast** — outdoor and low-light use, colour vision deficiency
- **Vestibular & motion** — motion sensitivity, parallax, autoplay
- **Auditory access** — captions, visual alternatives to audio
- **Keyboard & motor** — switch access, voice control, limited dexterity, one-handed use
- **Screen reader & semantic** — NVDA/JAWS/VoiceOver, structure, live regions
- **Cognitive & neurodivergent** — reading level, density, navigational consistency

Each perspective is a Jobs-to-be-Done checklist derived from CivicActions accessibility personas, with ARRM role mapping so findings route to whoever can fix them.

### `a11y-role-audit` — who owns the fix?

The third audit lens, orthogonal to the other two. Reviews an artifact through six ARRM responsibility roles — visual design, UX design, front-end development, content authoring, business analysis, testing — and attributes each finding to the role that owns it.

Available at two points: on a plan (design-time) and on an implementation (code-time). Optional; run it when a finding keeps bouncing between people.

### `bug-reporting` — make it filable

Converts findings from a test run or a review into bug reports a developer can act on without a follow-up conversation. Required fields every time: URL, XPath, HTML snippet, WCAG success criterion, rule ID, severity, frequency.

`references/build-error-workbook.mjs` serializes schema-shaped reports into a verifiable client-triage XLSX workbook (routed `exceljs` peer dependency, never vendored — see the [adoption assessment](error-workbook-adoption-assessment.md)).

Derived from the MIT-licensed [ACCESSIBILITY.md](https://github.com/mgifford/ACCESSIBILITY.md) guide, contributed by @mgifford.

**Routing caveat:** never route bug-report *generation* to a local model without a value-checking pass. The measured failure mode is fabricated exact values — selectors, IDs, environment fields — not missing structure.

### `acr-reporting` — report it

The report-level companion to `bug-reporting`: finding→issue is that skill, evaluation-report→ACR is this one. Serializes a **finished** audit-scope evaluation into a draft Accessibility Conformance Report in GSA's OpenACR format, validated and rendered through the routed exact-pinned `@openacr/openacr` CLI.

Output is always a **draft for human sign-off**, never a final or signed ACR.

Two hard rules, both load-bearing because the official toolchain validates boilerplate rather than substance: never map an untested Level A/AA criterion to any adherence term (`not-evaluated` is AAA-only; an untested A/AA criterion produces an INCOMPLETE draft with a marker and a gap list), and never derive a conformance term from finding severity — the two axes are orthogonal.

Always invoke the CLI with `-c`. Bare `validate -f` checks schema shape only and accepts criteria that do not exist; bare `output` silently renders a criteria-less shell. Both were reproduced here; receipts in [openacr-reference.md](openacr-reference.md).

### `a11y-content-judgment` *(candidate)*

A draft-and-ratify pipeline for the criteria a scanner cannot decide: are titles, headings, labels, link text in context, and image alternatives actually useful to a person (2.4.2, 2.4.6, 2.4.4, 1.1.1), and is identification consistent across pages (3.2.4)?

The agent drafts per-row `yes | no | unsure` with a rationale. A named human ratifies. **Nothing is a criterion outcome until `ratified_by` is filled.**

Candidate status is not a formality — the promotion gate is not met as the rubric stands. See the [adoption assessment](content-judgment-adoption-assessment.md).

### `a11y-workflow` — run the sequence

Orchestrates the lifecycle by spawning specialist agents from the main session at depth 1, with no nested delegation. Claude Code only.

```
/a11y-workflow full src/components/Modal.tsx        # whole lifecycle
/a11y-workflow step scout src/components/Modal.tsx  # one step
```

Model routing, validated on eight hard fixtures: Haiku for the scout (recon only), Opus for planner, critic and auditors (judgment-heavy), and the main session for orchestration, which is sequencing rather than judgment. Team definition in `.claude/teams/a11y-workflow.md`.

---

## Repository-maintenance skills

These operate on this repo rather than on a client's code.

| Skill | For |
|---|---|
| `maintain-accessibility-skills` | Tracked-file hygiene gates, history-rewrite verification, mixed-commit surgery, recovering commits made on the local default branch |
| `verify` | How to verify a change here — reproduce the committed evidence-harness recipes from scratch rather than re-running CI |
| `drupal-a11y-patch-eval` | End-to-end Drupal accessibility patch evaluation: baseline evidence, patch hygiene, after-patch verification, manual and AT checks, critic gate, upstream handoff. Evidence-gated — never VERIFIED without before/after proof under the same conditions |

## Companion agents

`.claude/agents/` carries nine agent prompts. Five back the workflow lane (`a11y-scout`, `a11y-planner`, `a11y-critic`, `perspective-audit`, `a11y-role-auditor`); four maintain the eval suites (`bench-runner`, `bench-reporter`, `bench-reviewer`, `fixture-builder`).

Agent definitions can drift from their SKILL.md source. A marker-based drift check in `scripts/check_mirrors.py --strict` catches it in CI — added after a real instance where the planner agent definition predated a skill change by weeks.

The same script gates full-text parity on the skill mirrors themselves — added after a CRITICAL a11y-critic guard shipped to the Claude surface only on 2026-08-25 and `--strict` stayed green, because a body-prose edit changes no heading and no URL (issue #27). `--self-test` proves that perturbation now fails.
