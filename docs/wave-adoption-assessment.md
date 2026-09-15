# WebAIM WAVE — Adoption Assessment

**Decision (2026-09-14, user's ruling):** WAVE is offered as an **optional supplemental detector lane** in `a11y-test` — browser-extension observation, subscription API, or a licensed stand-alone engine, always the operator's own credit-metered licence. **Core-stack promotion stays DEFERRED** (ruled 2026-09-03, PT-07 in `docs/plans/2026-09-02-promotion-candidate-dispositions.md`): WAVE's coverage delta over axe has never been measured here, and nothing maker-published exists to route to. This record consolidates the scattered receipts (the PT-07 disposition cell, the 2026-08-28 integration handoff, the `a11y-test` SKILL prose, and the `docs/tools.md` interim row) into one home, the repo's established shape for "we evaluated a tool, here is the boundary."

## What was evaluated

Candidate PT-07 from the engagement-tooling promotion catalogue: "WAVE capture with integrity canary" (`docs/plans/2026-09-02-promotion-candidate-dispositions.md`). During an authorized EPA product retest, a user-supplied WAVE report exposed signals the axe/keyboard evidence did not present in the same form (`docs/plans/2026-08-28-accessibility-testing-wave-siteimprove-handoff.md`). The question was whether to add WAVE as a routed detector lane in `a11y-test`.

Maker-skill survey (`evals/results/promotion-eval-2026-09/memos/1.8-maker-skill-survey.md`, 2026-09-02): WebAIM publishes no client, SDK, CLI, GitHub Action, skill, or MCP server — its GitHub org has 0 public repositories. Two community npm packages exist: `webaim-wave` (published 2019-11-13, ISC licence, unmaintained, 26 downloads/month) and `@afixt/wave-node` (published 2025-06-07, v0.1.0 single release, MIT, 12 downloads/month, no GitHub repo linked from npm metadata). Neither is a "routed, exact-pinned, detector" candidate as-is. skills.sh returned 0 on-topic hits for "wave"/"webaim" against a positive control that confirmed the search path works.

## What was surveyed (and what was NOT measured)

Unlike a coverage measurement, no head-to-head between WAVE and axe was ever run. The maker-skill survey established only that nothing exists to reuse; it did not touch WAVE's detection coverage. **The coverage delta vs axe is unmeasured and remains the open question** — this is reopen trigger (b) below, and a dedicated head-to-head is tracked as issue #86. Until that runs, no coverage number, no ranking, and no promotion claim can be made about WAVE.

## Detector, not verdict authority

WAVE output is detector evidence, not a conformance verdict. In the A11y Evidence Finding Contract (`docs/a11y-evidence-finding-contract.md`), a WAVE detection can merge into a finding's `detected_by` list (fixed vocabulary: `axe-core`, `html_codesniffer`, `alfa`, `wave`) and set `corroboration: corroborated` when a distinct engine agrees on the same WCAG criterion and target — never `confirmed`, a word reserved for the human/AT verification tier. The contract is explicit that no workflow may *require* cross-family corroboration, "which would make the one commercial engine (WAVE) a de facto dependency" — cross-family agreement is a bonus signal when present, never a gate (`docs/a11y-evidence-finding-contract.md`).

## Boundary

Three access modes, in priority order (`docs/plans/2026-08-28-accessibility-testing-wave-siteimprove-handoff.md`):

1. **Browser-extension report observation** for a user-supplied report. The extension evaluates rendered/dynamic content locally and sends nothing to WebAIM. Record report URL, evaluated URL, page state, viewport, timestamp, visible category/item totals, WAVE version if exposed, and capture limitations.
2. **Subscription API** (v3.1) when the operator supplies an authorized `WAVE_API_KEY` from the environment. The key travels in the request URL by WAVE's design, so it must never be recorded — redact it from logs, URLs, evidence files, and errors. Default to `SKIPPED_CREDENTIAL_REQUIRED` when the key is absent, never a clean result. WAVE's API caps concurrency at two simultaneous requests. Use `reporttype=4` for CSS selectors plus contrast data (`reporttype=3` returns XPath instead) — this is load-bearing, not a preference: the evidence contract builds a finding's fingerprint from selector + rule + kind, so a lane with no selector cannot enter the contract or earn a corroboration tag (`docs/a11y-evidence-finding-contract.md`; the same reasoning applies to Alfa's selector-less default output, `docs/alfa-scan-adoption-assessment.md`).
3. **Licensed stand-alone engine** an engagement already provides — route to it; never copy or vendor the WAVE engine into this repository.

Treat `error`, `contrast`, and `alert` as candidate findings; treat `feature`, `structure`, and `aria` as informational unless independent review identifies a defect. This partition follows WAVE's own category semantics: the first three are WAVE's problem/warning categories, the latter three are neutral or positive structural markers rather than defects. An item that cannot be mapped to a WCAG criterion via WebAIM's documented item→SC mapping cannot corroborate — it stays `single`.

## Licence / ToS

Live-verified against <https://wave.webaim.org/api> and <https://wave.webaim.org/terms> (accessed 2026-09-14).

A new registered account gets 100 free credits. Credit cost: 1 credit for a basic scan, 2–3 credits for an advanced scan; bundle pricing runs from $.04/credit down to $.025/credit at volume.

The WAVE terms have **no commercial-vs-non-commercial distinction. WAVE is not non-commercial-restricted.** The operative restriction is: (1) selling or redistributing WAVE reports or WAVE-derived data (error counts, item listings), and (2) modifying, copying, licensing, or creating derivative works from WAVE, without WebAIM's prior permission. This constraint applies to a FOSS/public repo exactly as it does to a client engagement — a public write-up cannot publish WAVE error counts or item listings; only independently verified defects (WCAG success criterion plus description) and the resulting decision may be published.

This is a standing obligation, not a publication-time-only check: the disclaimer is required wherever WAVE evidence appears, not only in a final public write-up (`.claude/skills/a11y-test/SKILL.md`, `docs/tools.md`).

## Reopen / promotion triggers

Verbatim from the PT-07 disposition cell:

- **(a)** WebAIM publishes an official client, SDK, CLI, GitHub Action, skill, or MCP server.
- **(b)** A WAVE licence-holder runs a five-page head-to-head against axe (the Lighthouse comparison in `docs/tools.md` is the template) and finds A/AA defect classes axe misses. **Run 2026-09-15 (issue #86): NOT MET — no promotion** (see below). The runnable protocol — surface independence, pre-declaration, and the WAVE-terms-compliant reporting split — is `docs/plans/2026-09-14-detector-headtohead-protocol.md`.
- **(c)** `@afixt/wave-node` reaches 1.0 with a public repo (today: v0.1.0, MIT, single release 2025-06-07, no repo linked from npm metadata).

**Trigger (b) measured 2026-09-15 (issue #86): NOT MET, no promotion.** A WebAIM-account head-to-head ran WAVE (API `reporttype=4`) against axe on **5 independent EPA surfaces** (Drupal 10, ColdFusion, Envirofacts, Oracle APEX, a React SPA), pre-declaration `091321a` committed before any scan. A naive success-criterion-level overlap suggested a large WAVE-only delta; it **collapsed to no A/AA defect class axe missed** once (1) uniqueness was deduped at the **element level** — axe and WAVE file the same element under different SC numbers, so an SC-number overlap over-counts (an unlabelled form input and a page-language defect were each caught by *both* engines); (2) WAVE's advisory-tier warnings, which are not failures, were set aside; and (3) the remaining candidates were live-inspected and found to be false positives (contrast on screen-reader-only text, missing-alt on `aria-hidden` decorative icons) or a control hidden in the loaded state that axe correctly skips. WAVE stays a supplemental lane; core promotion stays deferred. Full method, receipts, and human ratification: `evals/results/detector-headtohead-2026-09/RESULTS.md`. Per WAVE's terms, no WAVE report data (counts, item listings) is published — only the decision and independently-described WCAG defects. The element-level dedup fix is now in the protocol (§4a).

**Not claimed:** that WAVE finds nothing axe misses in general — the 2026-09-15 run measured five independent EPA surfaces on one day, one version set; it is a "not demonstrated here," not a universal claim.

## Escape hatch and dependency risk

Losing the WAVE lane costs a finding only its corroboration tag, never its validity — the finding stands on its own evidence (`docs/a11y-evidence-finding-contract.md`). Nothing in the bundle depends on WAVE: the contract states no workflow may require cross-family corroboration, precisely so the one commercial engine never becomes a de facto dependency. The operator supplies their own licence or account; the skill repository vendors nothing.

**What this does not claim:**

- No coverage *number* for WAVE against axe is published — WAVE-derived counts stay private per its terms. The 2026-09-15 head-to-head (trigger (b) above) established the *decision* — no A/AA class axe missed on five independent EPA surfaces — not a published number.
- No promotion to the core `a11y-test` stack — core promotion stays DEFERRED (now measured-and-not-demonstrated, 2026-09-15, not merely unmeasured).
- No endorsement of WAVE over Siteimprove Alfa or any other detector — both are optional supplemental lanes, evaluated on separate receipts (see `docs/alfa-scan-adoption-assessment.md`).
