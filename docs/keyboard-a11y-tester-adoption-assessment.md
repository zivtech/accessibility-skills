# keyboard-a11y-tester Gap Analysis & Adoption Assessment

**Decision:** adopt [ezufelt/keyboard-a11y-tester](https://github.com/ezufelt/keyboard-a11y-tester) in two tiers. **Done (2026-07-10):** routed as a fourth execution mode of `a11y-test` — an externally installed tool, like `agent-browser` and Webwright, pinned by commit SHA — after the correctness cross-validation gate was executed and passed. **Next:** elevate its output to critic-trusted hard evidence (Phase 3) and wire it into `drupal-a11y-patch-eval` (Phase 4). The original upstream-maturity gate was recalibrated on author context the same day — see Risks. Do not vendor its runner code into this repo.

Assessed 2026-07-10 at upstream commit `97eb13e`. MIT license, author Everett Zufelt. Hands-on validation of both execution modes performed (commands and results below). Reviewed by proposal-critic 2026-07-10; this revision incorporates its findings.

**Upstream update (2026-07-11):** [PR #7](https://github.com/ezufelt/keyboard-a11y-tester/pull/7) — our 3.3.2 UA-default-name check — was merged the same day it was filed ("Thanks for the contribution - merged"), and upstream immediately began cutting tagged releases (`0.3.0`–`0.5.0`, answering the release-tagging ask), added an OpenSSF Best Practices badge, `--storage-state` authenticated runs, broken-ARIA-reference and focusable-but-AT-invisible checks, and cross-viewport census diffing. **Pin bumped `97eb13e` → release `0.5.0` (`7e852a7`) after re-verify:** suite 28/29 locally vs green on upstream CI — the one local failure is the AAA-informative 2.4.13 pixel measurement (macOS rendering variance, present at both pins, never affects AA pass/fail). The upstream-maturity residuals in Risks are now substantially resolved: tagged releases exist and external contributions are merged responsively.

## What It Is

A keyboard-only + emulated-screen-reader web tester with a two-layer architecture:

- **Deterministic runner** (`scripts/runner.mjs`, ~1,700 lines): Playwright Chromium driven exclusively by real keyboard events (`Input.dispatchKeyEvent`, never `.click()`/`.fill()`), raw CDP accessibility tree as name/role/state ground truth, dual-signal focus-indicator detection (computed style + pixelmatch pixel diff), and `@guidepup/virtual-screen-reader` for announcement emulation, live-region monitoring, and a per-page reading-order census. Fails fast at startup if `:focus-visible` doesn't fire on CDP key events.
- **AI judgment layer**: the invoking agent drives a persistent session (`serve` → `observe`/`step` → `finish` → `stop`) one keystroke at a time, then writes the findings rules can't decide (task completion, logical order, announcement quality, form quality) merged with the deterministic ones.

Two W3C personas run in one pass: keyboard-only "Ade" and screen-reader "Lakshmi" (emulated — spec-compliant ARIA/ACCNAME computation, explicitly not a real-AT replacement, per its own docs). Works against any URL with `--url` + `--goal`; no test file required. Output is evidence-linked findings (`{wcag, persona, conformance_level, confidence, severity, url, locations, persona_impact, evidence[]}`), a per-step `trace.json`, per-stop screenshots, and `screen-reader-census.json` — all written to a temp dir.

**Upstream maturity, measured (2026-07-10):** repository created 2026-07-08 — two days before this assessment. 4 commits total, 1 author, 0 tags, 0 releases, 2 stars, 1 fork. Substantive commits are AI-co-authored, including the CI/test suite added the day of this assessment. The design and documentation quality are unusually high.

**Author context (recalibration, 2026-07-10):** Everett Zufelt is a long-time Drupal contributor with deep, lived accessibility expertise, personally known to us. Author trust rests on years of community work, not on this repo's metrics — so the age signals above are ordinary 0.x dependency hygiene (pin by SHA since no tags exist; expect the API to move; re-verify on upgrade), not a trust question. The phasing below was originally built around repo age as the central fact; it has been recalibrated accordingly.

## Validation Performed (2026-07-10, commit 97eb13e)

```bash
git clone https://github.com/ezufelt/keyboard-a11y-tester && cd keyboard-a11y-tester
npm install && node scripts/setup-check.mjs   # {deps_installed: true, browser_available: true}
# Mode 1 — unattended blind crawl (batch):
node scripts/runner.mjs --url "file://$PWD/test/fixtures/mixed-defects.html" --max-steps 12
node scripts/runner.mjs --url "file://$PWD/test/fixtures/clean.html" --max-steps 12
# Mode 2 — agent-driven session (serve/step loop):
node scripts/runner.mjs serve --url "file://$PWD/test/fixtures/mixed-defects.html" \
  --goal "reach and activate the confirmation button, confirm the live region announces"
node scripts/runner.mjs observe <session>; ... step <session> --press Tab; ... finish; stop
```

- **Blind crawl, mixed-defects.html**: 7 findings per viewport spanning both personas — 4.1.2 missing name (keyboard), 1.1.1 missing alt, 1.3.1 heading skip, 1.3.1 duplicate landmarks, 4.1.2 bare-role control, 4.1.3 silent live region (screen reader), plus a 2.4.13 AAA-informative focus-appearance finding carrying **measured contrast values** (2.34, 5.47).
- **Blind crawl, clean.html**: **0 AA findings** on both viewports; the only emission was the AAA-informative advisory, which is never a fail by design. This is the false-alarm resistance our eval culture requires of our own skills.
- **serve/step session**: verified end-to-end — `observe` → Tab-by-Tab focus stops each reporting CDP AX name/role (the planted unnamed textbox surfaced as an empty name mid-journey), Shift+Tab recovery, and on Enter the emulated screen reader captured `live_announcements: [{priority: "polite", text: "Form submitted successfully"}]`. The driven session correctly emitted 6 findings (not the crawl's 7): the live region announced when actually operated, so the "silent live region" finding did not fire. The goal text guessed the button name wrong ("Show status" vs. actual "Show confirmation") and the observe-decide loop recovered — a concrete demonstration of why the tool's "Tab until the name matches, never a counted sequence" rule is the right discipline.
- The repo self-tests this behavior in CI (`test/defects.spec.js` asserts detection on seeded fixtures; the clean-fixture test asserts zero AA findings; `test/persona-parity.spec.js` asserts the `--persona` contract). Caveat: those fixtures were written by the same (single, AI-assisted) author as the detector — internal consistency, not independent validation. See Phase 2.
- **Cross-validation against our own eval ground truth (Phase 2, executed 2026-07-10):** all 33 a11y-critic fixtures were rendered to live pages and run through KAT — batch crawl on all 33 plus 6 agent-driven sessions. Results: 2/3 deterministically-reachable must-finds caught (the third root-caused to Chromium's intrinsic "Choose File" name — a documented limitation class, not a detector error); **zero false positives outside one pre-disclaimed class** (passive-crawl 4.1.3, which upstream's own docs say requires a driven session); 6/6 driven sessions produced decisive trace evidence for interaction bugs (focus-loss, silent errors, inert arrow keys); and 2 real defects found that our own fixture rubrics don't list. Full agreement record and raw artifacts: [evals/results/keyboard-a11y-tester/](../evals/results/keyboard-a11y-tester/README.md). Headline: KAT's deterministic layer reaches only ~4% of this suite's ground truth — empirical confirmation that it complements rather than replaces the critic.
- **Not validated:** the `/plugin marketplace add` Claude Code install flow (non-interactive session). The standalone clone path is the verified install.

## Gap Analysis — What It Has That We Lack

Ranked by impact on our lifecycle (`plan → critique → implement → test → critique`):

1. **Automated screen-reader evidence.** Our `a11y-test` §6 Screen Reader Test Protocol is a *manual* NVDA/VoiceOver checklist — nothing in our stack can produce machine evidence that a live region never announced (4.1.3), that a control announces as a bare role, or what the reading-order sequence is. axe-core checks that `aria-live` *exists*, not that it *fires*. KAT's live-region monitor and census fill a lane we simply do not have — verified above by capturing an actual polite announcement in response to a real keystroke. Critic Phase 0 currently has no evidence source for announcement behavior.
2. **Focus-indicator measurement.** Our WCAG checklist lists 2.4.7/2.4.13 but the method is "manually check focus indicator contrast." KAT measures: dual-signal presence for 2.4.7 AA, and area + 3:1 contrast for 2.4.13 — reported as AAA-informative, never a fail, which avoids the classic "faint ring reported as missing indicator" false alarm. Our visual-regression lane can detect a focus ring *changed*, not whether it *suffices*.
3. **Goal-driven journey testing against arbitrary URLs.** None of our three modes does "URL + task in plain words → evidence-linked WCAG findings." Codified `.spec.js` requires pre-written per-widget tests; `agent-browser` recon leaves no structured evidence artifact and computes no checks; Webwright generates scripts, it doesn't judge journeys. This is the exact shape needed by discovery audits and by `drupal-a11y-patch-eval`'s before/after evidence requirement.
4. **Deterministic page-level keyboard checks.** Keyboard trap as focus-stall (2.1.2), skip-link presence (2.4.1), context-change-on-focus (3.2.1), positive tabindex (2.4.3), missing accessible name per focus stop (4.1.2) — behavioral checks requiring real key presses, evaluated per stop actually visited. Our 12 APG templates are widget-scoped, not page-journey-scoped; axe covers the static subset only.
5. **Prompt-level disciplines worth adopting regardless of the tool:** (a) "Tab **until** the focused control matches by name/role — never a pre-counted sequence of Tabs" (our agent-browser guidance doesn't state this anti-pattern); (b) AA pass/fail vs AAA informative severity honesty; (c) `persona_impact` in plain language grounded in the W3C WAI user stories.

## Gap Analysis — What We Have That It Lacks (Why This Is Not a Replacement)

- **Lifecycle**: no planner, no code-level critic, no perspective auditor, no orchestration. KAT is testing-only, and only sees the rendered runtime DOM — it cannot catch the `visibility:hidden + :focus-within` catch-22 in source before deploy, or review a plan.
- **Explicit non-goals it declares**: no axe/Lighthouse rule scans, no color-contrast-of-text audits, no real-AT automation. Our axe lane, static-analysis lane (jsx-a11y), and manual AT protocol remain necessary.
- **Coverage we keep**: visual regression baselines, zoom/reflow/text-spacing (1.4.10), text contrast (1.4.3/1.4.11), WCAG 2.2 criteria beyond 2.4.13 (2.5.8 target size, 2.4.11 focus-not-obscured, 3.3.7, 3.3.8), time-based media, SPA/React gotchas, cross-browser (KAT is Chromium-only).
- **Personas**: 2 W3C personas vs our 7-perspective audit model (no magnification/reflow, vestibular, auditory, or cognitive perspective in KAT).
- **Eval rigor**: our 83-fixture, cross-model benchmark discipline; KAT has 4 self-test fixtures graded by their own author (appropriate for a tool's CI, but not independent validation — hence Phase 2 below).

**Overlap to manage:** KAT's `serve`/`step` loop overlaps `agent-browser` recon (both deliver real CDP keyboard events interactively). Differentiator: KAT emits deterministic checks + a committed evidence trace; `agent-browser` is lighter-weight probing with Chrome-profile/auth reuse and arbitrary-domain flexibility. The routing table must disambiguate or agents will pick inconsistently.

## Adoption Matrix

| Surface | Decision | Rationale |
|---|---|---|
| Route as 4th `a11y-test` execution mode (goal-driven journey audit) | adopt now | Fills gaps 1–4 with an installable external tool; same pattern as agent-browser/Webwright; doc-only, one-commit revertible. |
| "Tab until named X, never counted Tabs" rule | adopt now | Correct discipline for *any* interactive keyboard driving, including agent-browser; verified in practice above. |
| AA pass/fail vs AAA informative framing for focus appearance | adopt now | Matches our calibrated-severity culture; prevents 2.4.13 findings masquerading as 2.4.7 failures. |
| Critic Phase 0 consumption of `trace.json` / `deterministic-findings.json` / census as hard evidence | adopt after Phase 2 gate | Would upgrade announcement/focus-indicator claims from "design reasoning" to "measured fact" — which is exactly why it must not happen before the checks themselves are independently validated. A subtly wrong "measured fact" the critic trusts is worse than no automation. |
| Map KAT findings → A11y Evidence Finding Contract | adapt | Their `severity` vocabulary (minor/moderate/serious, axe-style) ≠ our CRITICAL/MAJOR/MINOR/ENHANCEMENT; fingerprint from selector+wcag+check-kind, not their viewport-scoped `id`; `persona` → `perspective_alarms` keys (keyboard→`keyboard_motor`, screen-reader→`screen_reader_semantic`). |
| Persona grounding via W3C WAI user stories | adapt | Reference the user stories in critic/audit impact language; do not reduce our 7 perspectives to 2 personas. |
| Batch blind-crawl as a CI smoke gate on staging URLs | defer | Plausible (their own CI proves it), but belongs to a client-project template, not this bundle's v1 wiring. |
| Scenario `*.test.yaml` library | defer | Useful later for recurring client journeys; no v1 need. |
| Benchmarking KAT's AI-judgment layer across models | defer | Interesting (the judgment layer is model-portable by design) but a new eval lane; prove the routing first. |
| Vendoring runner code into this repo | reject | Prompt-only repo boundary (same ruling as Vital-Core scanner runtime). MIT would permit it; the boundary rule, not license, is the blocker. |
| Replacing `agent-browser`, axe lane, or §6 manual AT protocol | reject | Complementary lanes. KAT's own docs say emulation augments, never replaces, real AT testing. |

## Plan

Phases are ordered by risk tier: cheap-and-reversible documentation first, trust-elevation only behind gates. **Phases 3 and 4 are blocked on Phase 2.** Each phase lands as a single conventional commit so any of it reverts cleanly. Every claim written into a skill file must come from a run we performed, not upstream's README (the two facts below that failed this test in draft — default port and Node floor — are the cautionary examples).

### Phase 1 — Routing & inventory (docs only) — EXECUTED 2026-07-10

1. **Pin the version**: all references adopt commit `97eb13e` (upstream had no tags or releases at adoption; re-verify and re-pin on upgrade, noting its additive-fields compatibility policy). *(2026-07-11: bumped to tagged release `0.5.0` after re-verify — see Upstream update above.)*
2. **`docs/EXTERNAL-SKILLS-INVENTORY.md`**: add Tier 1 entry. Note it postdates the 2026-03-28 scan and is the first true runtime-tester peer found (the scan found only auditors/guardrails/analyzers).
3. **`.claude/skills/a11y-test/SKILL.md`**: add a routing-table row — *"Goal-driven journey audit of a live URL for keyboard + screen-reader personas, with evidence artifacts"* → keyboard-a11y-tester — and a dedicated section mirroring the Webwright section's structure: install (clone + `npm install` as the verified path; plugin-marketplace flow documented only if exercised first), Node ≥ 20 requirement (its `package.json` engines field; upstream README's "≥ 18" is inconsistent — flag it), the serve/step agentic loop with the never-counted-Tabs rule, output artifacts, when NOT to use it (widget CI regression → `.spec.js`; quick probing/authenticated Chrome-profile flows → agent-browser; rule scans → axe), session default port **9333** (`runner.mjs` fallback; README's 9400 is an example flag value), and the Chrome-instance contention caveat (don't run concurrently with agent-browser or Webwright sessions).
4. **`.agents/skills/a11y-test/SKILL.md` mirror**: same content; the clone + CLI path works from Codex (plain Node CLI); plugin install is Claude Code-only.
5. **This repo's `CLAUDE.md`** (`accessibility-skills/CLAUDE.md` only — not the `~/claude` workspace file): extend the Browser Automation Tooling section's routing split with the new mode.

### Phase 2 — Independent correctness cross-validation (the gate) — EXECUTED 2026-07-10, one item open

6. ~~Run against ground truth it did not author~~ **Done:** all 33 a11y-critic fixtures (68 must-finds, 4 CLEAN + 3 ADVERSARIAL false-alarm traps), batch + 6 driven sessions. Agreement record and raw artifacts committed at [evals/results/keyboard-a11y-tester/](../evals/results/keyboard-a11y-tester/README.md).
   **Pass bar verdict: met, with one documented carve-out.** Detection: 2/3 deterministic-scope must-finds caught; the miss is root-caused (UA-intrinsic name on file inputs) and reclassified, not a detector error. False alarms: zero across all check classes except passive-crawl 4.1.3 (3 findings on clean/adversarial pages) — a mode limitation upstream itself documents, carrying low confidence values (0.35–0.4). The carve-out becomes a consumption rule in Phase 3: **batch-mode 4.1.3 findings are never failure evidence, only a prompt to run a driven session.**
7. Formula read-through (2.4.13 area/contrast bar; 4.1.2 bare-role heuristic) against the normative SC text — **downgraded 2026-07-10 from Phase 3 blocker to in-phase diligence, then performed during Phase 3 (model judgment, not human SME).** Result: the 2.4.13 implementation matches the SC's two conditions (indicator area at least that of a 2 CSS-pixel perimeter of the unfocused component; at least 3:1 contrast between focused and unfocused states of the same pixels), and correctly reports as AAA-informative. The bare-role heuristic maps to 4.1.2's programmatically-determinable *name* requirement for interactive controls — consistent with how axe's label/name rules cite 4.1.2, and it behaved correctly in the cross-validation (true positive on the unlabeled tabpanel, no false fires). No discrepancy found.
8. Side product: 2 fixture-rubric gaps found by KAT (unlabeled tabpanel in `tabs-incomplete-aria-selected`, unnamed listbox in `interactive-dropdown-focus-bug`) — add as should-finds to those fixtures.

### Phase 3 — Evidence wiring — EXECUTED 2026-07-10

9. **`a11y-critic` Phase 0**: add KAT artifacts as a recognized hard-evidence tier with a citation format (step id + selector + measured value, e.g. `trace.json step_0003: outline 3px solid, AAA contrast 2.34`), at the same tier as codified Playwright runs. Journey-level verdicts (task completion, logical order) remain judgment-layer claims — cite them only with their supporting trace steps, never as bare "measured facts." Encode the two calibration rules measured in Phase 2: batch-mode 4.1.3 findings are prompts to drive, never failures; and name-presence findings don't cover UA-intrinsic names (a "Choose File" input can still be missing its label).
10. **`docs/a11y-evidence-finding-contract.md`**: add KAT as a `source`, plus the severity/fingerprint/persona mapping table from the adoption matrix above.
11. **`perspective-audit`**: accept KAT-sourced contracts; census/live-region evidence feeds `screen_reader_semantic`, trace/focus evidence feeds `keyboard_motor`.

### Phase 4 — Lifecycle integration — EXECUTED 2026-07-10

12. **Pre-flight for client-facing use (recalibrated 2026-07-10):** the original checkpoint (tagged release / second contributor / 60 days of stability) was calibrated for an unknown author and is withdrawn — the author is known and trusted. What remains is mechanical: re-verify the then-current pin before wiring client deliverables, adopt a tagged release if one exists by then, and keep committed artifacts + the pinned SHA with every delivered finding so evidence stays reproducible regardless of upstream motion.
13. **`.claude/teams/a11y-workflow.md` + orchestrator**: in the test step, route live-URL/journey targets to KAT mode and component/widget targets to `.spec.js` mode; keep both feeding critic Phase 0.
14. **`drupal-a11y-patch-eval`**: use before/after KAT runs (same URL, viewport, goal, same pinned SHA) as same-conditions evidence for keyboard/SR-behavior patches; fingerprints enable `resolved`/`persistent` trend language across the pair.

## Risks & Uncertainty

- **A young (2026-07-08), single-maintainer, zero-release dependency — with a known, trusted author.** The repo metrics alone would counsel heavy caution, and the first version of this assessment did exactly that; the recalibration (2026-07-10, author context from Alex) reduces the residual risks to mechanical ones: no tags to pin (SHA-pin instead), a fast-moving 0.x API (re-verify on upgrade), and the removal-vs-replacement asymmetry — dropping KAT loses the journey-audit capability tier entirely, since we have no in-house equivalent. Routing-not-vendoring keeps removal itself cheap.
- **Correctness now cross-validated on ground truth it did not author** (our 33 fixtures, 2026-07-10) — detection and false-alarm behavior both held, with one documented mode-limitation carve-out. Still open: the human SME check of the 2.4.13 and bare-role formulas against normative SC text (Phase 2 item 7), and the caveat that our judgment-layer sample is 6 sessions driven by one agent, an existence proof rather than a benchmark.
- **CAPTCHA/bot-detection handling is automation-signal spoofing.** On pages where a CAPTCHA is present, the runner suppresses `navigator.webdriver` (page-scoped) so the CAPTCHA can initialize. Pointed at a client's production WAF, that traffic pattern could trip a security review. **Client-facing rule: get explicit client sign-off before running KAT against client production infrastructure; prefer staging.** This belongs in the Phase 1 skill-section text, not just here.
- **Emulated SR fidelity**: guidepup computes what a *spec-compliant* screen reader should announce; real NVDA/JAWS/VoiceOver quirks differ. Our docs must keep KAT SR findings labeled as emulation evidence, distinct from §6 manual AT results.
- **Findings provenance if the dependency is dropped**: any KAT-sourced finding delivered to a client must carry its pinned SHA and committed trace artifacts, so the evidence remains reproducible and defensible even if we later remove the routing (the artifacts stand alone; the tool is only needed to regenerate them).
- **Judgment-layer quality is ours, not theirs**: the deterministic findings are reproducible; journey verdicts are only as good as the driving agent, and we have no measured quality number for that layer (benchmark deferred).

## What This Does Not Claim

- Not a replacement for manual AT testing, real-user testing, axe scanning, or our visual-regression lane.
- Not a commitment to a new cross-model benchmark lane, a CI product, or site monitoring.
- Not an adoption of KAT's code into this repository, and not a change to `a11y-planner` or the critic's investigation protocol beyond Phase 0 evidence intake.
- The 2-persona model does not supersede the 7-perspective audit taxonomy.
- No security/supply-chain audit of `runner.mjs` or `@guidepup/virtual-screen-reader` was performed; that review becomes mandatory if the vendoring decision is ever revisited.
