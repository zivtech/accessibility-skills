# WCAG-EM 2.0 Gap Analysis & Adoption Assessment

**Decision:** adopt in three tiers. **Tier 1 (do now, docs only):** refresh the bundle's WCAG-EM references — the methodology was renamed, re-scoped, and republished, and our one fixture that requires it cites the 1.0 identity. **Tier 2 (behind a verify-the-spec gate):** make audit-scope work first-class — an audit mode in the planner protocol, random-sample and complete-process discipline in a11y-test's sampling section, and an evaluation-report contract mirroring the evidence-finding contract. **Tier 3 (defer/watch):** non-web digital products, the WCAG-EM 2 Report Tool, and a site-audit orchestration mode. Nothing in WCAG-EM 2.0 invalidates the component-lifecycle core of this bundle; what it exposes is that our audit-scope layer is half-built — one COMPLEX fixture expects methodology knowledge that no skill file actually teaches.

Assessed 2026-07-27. **Standing caveat:** `www.w3.org` is unreachable from the session that produced this assessment (remote-environment egress allowlist; the TR page also 403s automated fetchers). Every claim below is triangulated from search-result content across independent secondary sources — including a write-up by one of the EM 2.0 editors — plus the WCAG-EM 1.0 structure, which 2.0 is consistently reported to retain. Claims that only the spec text can settle are marked *(verify)* and gate Phase 2. Sources listed at the end.

## What It Is

**WCAG Evaluation Methodology (WCAG-EM) 2.0** — announced by W3C as "W3C Accessibility Guidelines Evaluation Methodology (WCAG-EM) 2.0" — published as a **W3C Group Note on 23 July 2026** (one secondary report says 24 July; pin in Phase 0). First Draft Note 2026-02-05. Editors: Hidde de Vries, Steve Faulkner, Jeroen Hulscher (1.0, 2014, was Shadi Abou-Zahra and Eric Velleman). It is informative guidance, not a normative standard: a technology-agnostic, step-by-step process for evaluating how well a digital product conforms to WCAG 2, usable for self-assessment and third-party evaluation.

The five-step process is retained from 1.0:

1. **Define the evaluation scope** — what is being evaluated, the conformance target (WCAG 2 version and level), and an accessibility support baseline (which AT/browser combinations count).
2. **Explore the target product** — common views, essential functionality, variety of content/view types, technologies relied upon.
3. **Select a representative sample set** — structured selection plus a random sample, including complete processes.
4. **Evaluate the selected sample set** — all samples in all their states, complete processes end-to-end, and a comparison of structured vs. random sample results to check the sample's representativeness.
5. **Report the findings** — documented outcomes per step, optionally an evaluation statement and aggregated score, machine-readable via EARL.

Sub-step naming, the random-sample sizing parameters, and the exact required report fields are 1.0-derived here and *(verify)* for 2.0.

What changed from 1.0:

- **Scope: websites → digital products.** 1.0 ("Website Accessibility Conformance Evaluation Methodology") evaluated websites and web pages. 2.0 also applies to apps, kiosks, documents, and other digital products — aligned with regulators (which have long required apps to be accessible) and with WCAG 3's direction.
- **Terminology.** "Web pages" → **samples** (a sample is a web page, app screen, kiosk step, or other view); "sample of web pages" → **sample set**; "websites" → **digital products**.
- **Editorial.** Readability and clarity work, updated references to related standards and guidance (WCAG 2.2, WCAG2ICT; WCAG2Mobile is in progress at the MATF), new graphics and examples. The core methodology is reported unchanged — "for teams already using WCAG-EM 1, the transition should be relatively smooth."
- **Tooling lag.** The W3C WCAG-EM Report Tool (v3.0.3, updated 2026-07-01) is still WCAG-EM 1-based; W3C plans a WCAG-EM 2 Report Tool "later in 2026."

## Where the Bundle Already Aligns

Honesty first — several EM concepts already exist here, and the plan must not re-invent them:

- **Structured sampling by template group.** `a11y-test` §4 "Scale and Sampling (>15 pages)" and the planner's Phase 8 scale note both do EM Step 3's structured selection in miniature (classify by template, test representatives, document the strategy).
- **Complete processes.** EM requires evaluating complete processes end-to-end. `keyboard-a11y-tester` goal-driven journey audits *are* complete-process evaluation with machine evidence — the bundle has the strongest tool for EM's hardest sample type and never names it in EM terms.
- **Per-SC outcome vocabulary.** `bug-reporting`'s EARL section already documents `passed / failed / cantTell / inapplicable / untested` — exactly the outcome vocabulary an EM-style report aggregates — and already points at the WCAG-EM Report Tool as an EARL producer.
- **Conformance target and AT matrix.** The planner's Phase 1 asks for compliance target (EM 1.b) and supported assistive technologies (an informal accessibility support baseline); `a11y-test` §6 has the SR/browser test matrix.
- **Evaluation-grade reporting discipline.** The evidence-finding contract's stable fingerprints and trend language (`new/persistent/resolved`) serve EM's re-evaluation and consistency goals better than EM itself specifies.
- **The one direct WCAG-EM touchpoint.** `evals/suites/a11y-planner/fixtures/test-multi-page-audit.*` (COMPLEX, VPAT-prep government portal) requires plans to cite WCAG-EM as the sampling/reporting framework, with risk-based sampling and third-party handling.

## Gap Analysis — What EM 2.0 Describes That the Bundle Lacks

1. **Audit-scope planning is expected but never taught.** The multi-page-audit fixture *grades* WCAG-EM knowledge ("a plan that doesn't know the W3C's own evaluation methodology cannot produce a legally defensible VPAT"), and its own scoring predictions say weaker models "will almost certainly miss WCAG-EM" — but the 9-phase planner protocol contains no audit mode, no WCAG-EM mention, and no scope/explore/sample/evaluate/report structure. Today the fixture passes on Opus's training knowledge, which is exactly the "specialist knowledge that structured examples don't supply" failure the rubric predicts for everyone else. A skills repo should carry that knowledge in the skill.
2. **No random sample, no representativeness check.** Our sampling guidance is purely structured. EM Step 3 adds a random sample and Step 4 compares structured vs. random outcomes — the audit-of-the-audit that catches a biased template classification. Nothing in the bundle does this.
3. **No accessibility support baseline as a declared artifact.** We ask which AT to support, but no output declares the baseline the way EM Step 1.c requires — which combinations were tested and which conformance claims are relative to them. Cheap to add to audit-scope outputs; meaningless at component scope.
4. **No evaluation-report layer.** `bug-reporting` is deliberately finding-level (URL, XPath, snippet, SC, rule, severity, frequency). EM Step 5 is report-level: scope statement, conformance target, baseline, sample set with rationale, per-SC outcomes across the sample, optional statement/score. Findings feed such a report; nothing here defines its shape.
5. **Terminology drift.** The fixture calls it "Website Accessibility Conformance Evaluation Methodology" (retired name); the rubric requires URL `https://www.w3.org/TR/WCAG-EM/` *(verify where that shortname now resolves — the 2.0 TR page is `/TR/wcag-em-2/`)*. Once EM 2.0 is common in training data, graded plans will cite either version; the rubric keyword list (`WCAG-EM`, `w3.org/TR/WCAG-EM`) happens to match both, which is the right transition behavior — by luck, not design.
6. **Sample-set language for states.** EM evaluates samples "in all their states." `a11y-test` already scans default/loading/error/expanded variants; the audit-scope guidance should name state coverage as part of what makes a sample "evaluated."

## Gap Analysis — What the Bundle Has That EM Doesn't Cover

Adopting EM must not erode these:

- **Design-phase work.** EM evaluates products that exist. The planner/critic-on-plans half of the lifecycle is out of EM's scope entirely and is this bundle's differentiator.
- **User-impact severity.** EM aggregates SC-level conformance outcomes; it has no severity model. Our CRITICAL/MAJOR/MINOR/ENHANCEMENT is calibrated to real user impact, and CLAUDE.md's rule — severity reflects impact on people, not rule weight — stands. **Conformance outcome and impact severity are orthogonal dimensions: report both, never derive one from the other.** A `failed` outcome on 4.1.2 may be MINOR; a `failed` on 2.1.1 in a checkout process is CRITICAL because the person cannot buy, not because the checklist says so.
- **Evidence discipline.** Fingerprints, trend language, measured-fact vs. design-reasoning tiers, and false-alarm calibration have no EM equivalent. An EM-shaped report from this bundle should be *more* evidence-rigorous than the methodology requires, not less.
- **Component-scope depth.** APG pattern completeness, focus-management coherence, the 7-perspective and 6-role audits — none of this is EM's business, and EM citations must not start appearing in component-scope reviews (see rejects).

## Adoption Matrix

| Surface | Decision | Rationale |
|---|---|---|
| Verified EM 2.0 step/sub-step reference committed to `docs/` | adopt now (Phase 0) | Everything normative below depends on the spec text we could not read from this session. |
| Fixture/rubric identity refresh (`test-multi-page-audit.*`) | adopt now | Retired 1.0 name and stale URL in the one asset that grades EM knowledge; accept either version's citation during transition, bonus (not gate) for 2.0 sample-set/complete-process language. |
| Planner audit-scope mode (EM five-step structure, conformance target, baseline, sample rationale, report skeleton) | adopt (Phase 2) | Converts fixture-graded specialist knowledge into skill content — highest-value change in this plan. |
| Random-sample + structured-vs-random comparison in `a11y-test` sampling | adopt (Phase 2) | The representativeness check is cheap and is the part of EM sampling nobody does informally. Parameters from the spec text, not memory. |
| Name journey audits as complete-process evaluation; route EM Step 4 process samples to `keyboard-a11y-tester` driven sessions | adopt (Phase 2) | Capability already exists; naming it in EM terms makes audit plans routable. |
| `docs/a11y-evaluation-report-contract.md` (scope, target, baseline, sample set, per-SC outcomes via the EARL vocabulary already in `bug-reporting`, statement language, orthogonal impact severity) | adopt (Phase 2) | Mirrors the evidence-finding contract pattern; report-level complement to finding-level bug-reporting. |
| `bug-reporting` change | adapt, minimal | Stays finding-level by charter (mgifford-derived companion). Add one pointer to the report contract + a Report Tool watch note. No scope expansion. |
| Optional `evaluation_context` field on the evidence-finding contract | adapt (Phase 2, optional) | Lets findings carry sample-set membership without making the field ritual for non-audit findings. |
| "Digital product" / "sample" / "sample set" terminology in audit-scope outputs | adapt | Free alignment where it appears; do not rename component-scope concepts. |
| Site-audit orchestration mode in `a11y-workflow` (explore → sample → per-sample fan-out → report) | defer | Plausible, but build it when a real site audit runs through the bundle, not speculatively. |
| WCAG-EM 2 Report Tool / EARL export integration | defer (watch) | Tool doesn't exist yet (planned late 2026); revisit when it ships. |
| Non-web digital products (native mobile, kiosks, documents) | defer, declare boundary | The measurement stack (Playwright, axe-core, jsdom, CDP) is web-only. Audit-scope plans for hybrid products must say which screens the stack cannot measure rather than implying coverage. Watch WCAG2Mobile (MATF). |
| EM citations in component-scope reviews | reject | A component review citing WCAG-EM is checkbox theater — the exact dead-output pattern CLAUDE.md names. EM lives at audit scope only. |
| Replacing impact severity with SC-level outcomes | reject | See gap analysis; orthogonal dimensions. |
| Vendoring Report Tool code or EM text into the repo | reject | Prompt-only repo boundary (same ruling as Vital-Core and keyboard-a11y-tester runners). |

## Plan

Each phase is a single revertible commit; SKILL.md edits mirror to `.agents/skills/`. **Phase 2 is blocked on Phase 0.**

### Phase 0 — Verify against the spec text (the gate)

1. Read `https://www.w3.org/TR/wcag-em-2/` from an environment that can reach it (add `www.w3.org` to this remote environment's network allowlist, or run from local Claude Code), plus the EM 2 changelog.
2. Commit `docs/wcag-em-2-reference.md`: verified title, publication date, step/sub-step map, random-sample parameters, required report fields, definitions (digital product, sample, sample set, accessibility support baseline, complete process), and where `/TR/WCAG-EM/` now resolves. Correct this assessment where the spec contradicts it — the *(verify)* marks above are the checklist.

### Phase 1 — Reference & terminology refresh (docs only, no behavior change)

3. `evals/suites/a11y-planner/fixtures/test-multi-page-audit.md` + `.metadata.yaml` + rubric: current name and URL; rubric explicitly accepts a 1.0 **or** 2.0 citation as the pass signal (training-data lag is real — a 2.0-only gate would fail good plans for years), with 2.0 terminology as bonus evidence, not a gate.
4. `bug-reporting` EARL section: one line noting WCAG-EM 2.0 and the planned EM 2 Report Tool.
5. This doc indexed from `README.md` docs list.

### Phase 2 — Audit-scope methodology wiring

6. **Planner:** add an explicit audit-scope mode to the protocol (trigger: the target is a site/product evaluation, not a component build) structured on the five steps, requiring: conformance target + accessibility support baseline declarations; sample-set rationale (structured + random + complete processes + shared-component leverage); state coverage per sample; the report skeleton from the contract below; and the boundary sentence for anything the web stack can't measure. Risk-based prioritization and third-party handling stay — EM doesn't provide them and the fixture is right to demand them.
7. **`a11y-test` §4 sampling:** add the random sample, the structured-vs-random comparison rule ("divergence means the structured sample was not representative — expand and re-classify"), and complete-process routing to keyboard-a11y-tester driven sessions.
8. **`docs/a11y-evaluation-report-contract.md`:** report-level contract as in the matrix. Findings reference it; it references findings by `finding_id`.
9. Optional `evaluation_context` on the evidence-finding contract; CLAUDE.md routing note if any of the above changes lifecycle wiring.

### Phase 3 — Eval-suite alignment

10. Re-run the multi-page-audit lane after Phase 2 to confirm the protocol now *teaches* what the rubric grades (prediction: sub-Opus tiers should stop missing WCAG-EM once it's in the protocol — that delta is the measure of Phase 2's value).
11. Candidate new fixtures, costed separately: (a) an audit-scope plan for a hybrid web/native product — the trap is claiming axe/Playwright coverage for native screens (false-coverage honesty, in the spirit of the CLEAN-fixture discipline); (b) a chain fixture aggregating a11y-test findings into a contract-shaped evaluation report.

### Phase 4 — Watch items

12. WCAG-EM 2 Report Tool ships (late 2026) → revisit EARL export mapping. WCAG2Mobile advances → revisit the non-web boundary. A real site audit runs through the bundle → revisit the workflow audit mode.

## Risks & Uncertainty

- **Secondary-source basis.** The step-level detail above is consistent across multiple independent sources, one written by an EM 2.0 editor — but no one on this assessment has read the TR text. That is why Phase 2 is gated on Phase 0, and why sub-step claims are marked. Wrongest-plausible-case: a 2.0 structural change we haven't seen (e.g., to sampling or reporting requirements) invalidates part of the Phase 2 design — the phase ordering contains that blast radius.
- **Group Note status.** EM 2.0 is guidance. Procurement and legal contexts (VPATs, EN 301 549 workflows) will keep referencing specific versions on their own schedules; audit-scope outputs should cite the version the engagement requires, not assume 2.0.
- **Rubric transition hazard.** Grading audit plans on "cites WCAG-EM 2.0" too early punishes models with pre-2026 training data for knowing the methodology under its stable name; grading only 1.0 rewards stale citations. Accept-either with 2.0-as-bonus is deliberate.
- **Checklist creep.** The failure mode of adopting an evaluation methodology into a skills bundle is that every output grows a WCAG-EM section. The reject row exists for this; reviewers should treat an EM citation in a component-scope review as a finding against the output.

## What This Does Not Claim

- Not a new capability to test native apps, kiosks, or documents — the boundary is declared, not solved.
- Not a commitment to build the workflow audit mode, new eval lanes, or Report Tool integration on any schedule.
- Not a change to the critic's investigation protocol, the perspective/role audit taxonomies, or the severity scale.
- Not a claim that the bundle was "wrong" pre-EM-2.0: the component lifecycle was never in WCAG-EM's scope, in either version.

## Sources

Direct spec access blocked from this session; basis: [W3C WAI news, 2026-02-05 First Draft Note](https://www.w3.org/WAI/news/2026-02-05/wcag-em-2), [W3C news: Group Note Draft](https://www.w3.org/news/2026/group-note-draft-w3c-accessibility-guidelines-evaluation-methodology-wcag-em-2-0/), [WCAG-EM Overview (WAI)](https://www.w3.org/WAI/test-evaluate/conformance/wcag-em/), [WCAG-EM 2.0 publication history](https://www.w3.org/standards/history/wcag-em-2/), [Hidde de Vries (EM 2.0 editor): "WCAG-EM 2.0 lets you report on accessibility of more than just websites"](https://hidde.blog/wcag-em-apps/), [Centre for Accessibility Australia](https://www.accessibility.org.au/w3c-publishes-wcag-evaluation-methodology-wcag-em-2-0/), [accessibility.chat](https://www.accessibility.chat/articles/wcag-em-20-draft-expands-beyond-websites-to-mobile-apps-and-digital-products), [TR page (unread, for Phase 0)](https://www.w3.org/TR/wcag-em-2/), plus the WCAG-EM 1.0 structure from training knowledge.
