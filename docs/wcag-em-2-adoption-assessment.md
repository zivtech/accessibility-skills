# WCAG-EM 2.0 Gap Analysis & Adoption Assessment

**Decision:** adopt in three tiers. **Tier 1 (do now, docs only):** refresh the bundle's WCAG-EM references — the methodology was renamed, re-scoped, and republished, and our one fixture that requires it cites the 1.0 identity. **Tier 2 (behind a verify-the-spec gate):** make audit-scope work first-class — an audit mode in the planner protocol, random-sample and complete-process discipline in a11y-test's sampling section, and an evaluation-report contract mirroring the evidence-finding contract. **Tier 3 (defer/watch):** non-web digital products, the WCAG-EM 2 Report Tool, and a site-audit orchestration mode. Nothing in WCAG-EM 2.0 invalidates the component-lifecycle core of this bundle; what it exposes is that our audit-scope layer is half-built — one COMPLEX fixture expects methodology knowledge that no skill file actually teaches.

Assessed 2026-07-27 from secondary sources; **Phase 0 executed 2026-07-28, twice in parallel and reconciled**: a remote session read the Note's editors'-draft URL (its egress saw a Cloudflare challenge on the TR host), and a local session read the TR pages directly with plain `curl`, byte-compared the two shortname URLs, and fetched the archived 1.0 Note plus the history page. The two reads agree on every shared fact; every *(verify)* mark is resolved with **no residuals**. Verified facts, verbatim anchors, and both provenance trails live in [`wcag-em-2-reference.md`](wcag-em-2-reference.md); corrections have been applied in place below. Sources listed at the end.

## What It Is

**WCAG Evaluation Methodology (WCAG-EM) 2.0** — announced by W3C as "W3C Accessibility Guidelines Evaluation Methodology (WCAG-EM) 2.0" — published as a **W3C Group Note on 23 July 2026** at `https://www.w3.org/TR/wcag-em-2/` (this-version `/TR/2026/NOTE-wcag-em-2-20260723/`; editors' draft `w3c.github.io/wai-wcag-em/`). First Draft Note 2026-02-05. Editors: Hidde de Vries (Logius), Jeroen Hulscher (Logius), Steve Faulkner (Tetralogical); 1.0 (2014) was Shadi Abou-Zahra and Eric Velleman. It is informative guidance on the Note track — endorsed by the AG WG, not by W3C itself: a technology-agnostic, step-by-step process for evaluating how well a digital product conforms to WCAG 2, usable for self-assessment and third-party evaluation, explicitly adding nothing to WCAG 2's requirements.

The five-step process is retained from 1.0:

1. **Define the evaluation scope** — what is being evaluated, the conformance target (WCAG 2 version and level), and an accessibility support baseline (which AT/browser combinations count).
2. **Explore the target product** — common views, essential functionality, variety of content/view types, technologies relied upon.
3. **Select a representative sample set** — structured selection plus a random sample, including complete processes.
4. **Evaluate the selected sample set** — each sample checked against **all five WCAG 2 conformance requirements** at the target level (conformance level, full pages, complete processes, accessibility-supported technology use, non-interference), complete processes end-to-end, and a comparison of structured vs. random results to check representativeness (Step 4.3: new content types or new findings in the random set send you back to Step 3, repeated until representative).
5. **Report the findings** — Step 5.1's minimum documented outcomes are required; evaluation specifics, an evaluation statement, an aggregated score, and machine-readable reports (EARL recommended, Step 5.5 — 1.0 already had this as 5.e) are optional.

Sub-steps are decimal (1.1–5.5, "Methodology Requirement N.M" framing; 1.0 used letters). The verified step map, the 10%-of-structured random-sample rule, and Step 5.1's minimum report fields are in [`wcag-em-2-reference.md`](wcag-em-2-reference.md).

What changed from 1.0:

- **Scope: websites → digital products.** 1.0 ("Website Accessibility Conformance Evaluation Methodology") evaluated websites and web pages. 2.0 also applies to apps, kiosks, documents, and other digital products — aligned with regulators (which have long required apps to be accessible) and with WCAG 3's direction.
- **Terminology.** The verified chain is **view** (web page, document, software view, "or an equivalent unit of conformance") → **sample** (a view *selected* for evaluation) → **sample set**; "websites" → **digital products** (a "coherent collection of one or more related views"). New framing: the **principle of product enclosure** — scope includes all views, states, and functionality, no exclusions — generalizes 1.0's full-pages provision. Non-URL products (native apps, hardware kiosks) identify samples by screenshots and path descriptions.
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
2. **No random sample, no representativeness check.** Our sampling guidance is purely structured. EM Step 3.2 adds a documented-method random sample sized at **10% of the structured sample set, added on top**, and Step 4.3 is the audit-of-the-audit: if the random set shows content types or findings the structured set missed, the structured sample was not representative — return to Step 3 and repeat until it is. Nothing in the bundle does this.
3. **No accessibility support baseline as a declared artifact.** We ask which AT to support, but no output declares the baseline the way EM Step 1.c requires — which combinations were tested and which conformance claims are relative to them. Cheap to add to audit-scope outputs; meaningless at component scope.
4. **No evaluation-report layer.** `bug-reporting` is deliberately finding-level (URL, XPath, snippet, SC, rule, severity, frequency). EM Step 5 is report-level: scope statement, conformance target, baseline, sample set with rationale, per-SC outcomes across the sample, optional statement/score. Findings feed such a report; nothing here defines its shape.
5. **Terminology drift.** The fixture calls it "Website Accessibility Conformance Evaluation Methodology" (retired name); the rubric requires URL `https://www.w3.org/TR/WCAG-EM/` — settled 2026-07-28: that shortname now serves the 2.0 Note **byte-identically** (a live pointer, but version-ambiguous; the canonical 2.0 URL is `/TR/wcag-em-2/`). Once EM 2.0 is common in training data, graded plans will cite either version; the rubric keyword list (`WCAG-EM`, `w3.org/TR/WCAG-EM`) happens to match both, which is the right transition behavior — by luck, not design.
6. **Sample-set language for states.** EM evaluates samples "in all their states." `a11y-test` already scans default/loading/error/expanded variants; the audit-scope guidance should name state coverage as part of what makes a sample "evaluated."

## Gap Analysis — What the Bundle Has That EM Doesn't Cover

Adopting EM must not erode these:

- **Design-phase work.** EM evaluates products that exist — its own text says it "has been primarily designed for reviewing digital products that are already developed," that early-stage evaluations "can quickly become obsolete," and that they "should not be used for making statements nor conformance claims." The planner/critic-on-plans half of the lifecycle is out of EM's scope entirely and is this bundle's differentiator.
- **User-impact severity.** EM reports conformance outcomes; it has no severity model (its Step 5.1 notes severity in issue descriptions as good practice, nothing more), and its Step 5.4 warns in our own register that aggregated scores "can be misleading and do not provide sufficient context… to understand the actual accessibility of a digital product." Our CRITICAL/MAJOR/MINOR/ENHANCEMENT is calibrated to real user impact, and CLAUDE.md's rule — severity reflects impact on people, not rule weight — stands. **Conformance outcome and impact severity are orthogonal dimensions: report both, never derive one from the other.** A `failed` outcome on 4.1.2 may be MINOR; a `failed` on 2.1.1 in a checkout process is CRITICAL because the person cannot buy, not because the checklist says so.
- **Expert review is not user involvement — and EM says so.** EM 2.0 strongly recommends involving people with disabilities in evaluations; our perspective and role audits are expert-lens simulation, not user research. Audit-scope outputs must present them as such and carry EM's recommendation forward rather than implying the audits satisfy it.
- **Evidence discipline.** Fingerprints, trend language, measured-fact vs. design-reasoning tiers, and false-alarm calibration have no EM equivalent. An EM-shaped report from this bundle should be *more* evidence-rigorous than the methodology requires, not less.
- **Component-scope depth.** APG pattern completeness, focus-management coherence, the 7-perspective and 6-role audits — none of this is EM's business, and EM citations must not start appearing in component-scope reviews (see rejects).

## Adoption Matrix

| Surface | Decision | Rationale |
|---|---|---|
| Verified EM 2.0 step/sub-step reference committed to `docs/` | **executed 2026-07-28** | [`wcag-em-2-reference.md`](wcag-em-2-reference.md) — two parallel reads reconciled: editors'-draft URL (remote session) and the TR text + archived 1.0 Note directly (local session). |
| Fixture/rubric identity refresh (`test-multi-page-audit.*`) | adopt now | Retired 1.0 name and stale URL in the one asset that grades EM knowledge; accept either version's citation during transition, bonus (not gate) for 2.0 sample-set/complete-process language. |
| Planner audit-scope mode (EM five-step structure, conformance target, baseline, sample rationale, report skeleton) | adopt (Phase 2) | Converts fixture-graded specialist knowledge into skill content — highest-value change in this plan. |
| Random-sample + structured-vs-random comparison in `a11y-test` sampling | adopt (Phase 2) | The representativeness check is cheap and is the part of EM sampling nobody does informally. Verified parameters: 10% of the structured set, on top, method documented; Step 4.3 loop until representative. |
| Name journey audits as complete-process evaluation; route EM Step 4 process samples to `keyboard-a11y-tester` driven sessions | adopt (Phase 2) | Capability already exists; naming it in EM terms makes audit plans routable. |
| `docs/a11y-evaluation-report-contract.md` (scope, target, baseline, sample set, per-SC outcomes via the EARL vocabulary already in `bug-reporting`, statement language, orthogonal impact severity) | adopt (Phase 2) | Mirrors the evidence-finding contract pattern; report-level complement to finding-level bug-reporting. |
| `bug-reporting` change | adapt, minimal | Stays finding-level by charter (mgifford-derived companion). Add one pointer to the report contract + a Report Tool watch note. No scope expansion. |
| Optional `evaluation_context` field on the evidence-finding contract | adapt (Phase 2, optional) | Lets findings carry sample-set membership without making the field ritual for non-audit findings. |
| "Digital product" / "sample" / "sample set" terminology in audit-scope outputs | adapt | Free alignment where it appears; do not rename component-scope concepts. |
| Site-audit orchestration mode in `a11y-workflow` (explore → sample → per-sample fan-out → report) | defer | Plausible, but build it when a real site audit runs through the bundle, not speculatively. |
| WCAG-EM 2 Report Tool / EARL export integration | defer (watch) | Tool doesn't exist yet (planned late 2026); revisit when it ships. |
| Non-web digital products (native mobile, kiosks, documents) | defer, declare boundary | The measurement stack (Playwright, axe-core, jsdom, CDP) is web-only, and so are `bug-reporting`'s required URL/XPath fields — EM 2.0 itself says non-URL products identify samples by screenshots and path descriptions instead. Audit-scope plans for hybrid products must say which screens the stack cannot measure rather than implying coverage. Watch WCAG2Mobile (MATF). |
| EM citations in component-scope reviews | reject | A component review citing WCAG-EM is checkbox theater — the exact dead-output pattern CLAUDE.md names. EM lives at audit scope only. |
| Replacing impact severity with SC-level outcomes | reject | See gap analysis; orthogonal dimensions. |
| Vendoring Report Tool code or EM text into the repo | reject | Prompt-only repo boundary (same ruling as Vital-Core and keyboard-a11y-tester runners). |

## Plan

Each phase is a single revertible commit; SKILL.md edits mirror to `.agents/skills/`. **Phase 2 is blocked on Phase 0.**

### Phase 0 — Verify against the spec text (the gate) — EXECUTED 2026-07-28

1. **Done, via two parallel routes that agree.** A remote session read the Note's editors'-draft URL (`w3c.github.io/wai-wcag-em/`) after its egress allowlist was opened — from that egress the TR host served a Cloudflare JS challenge. A local session then fetched `https://www.w3.org/TR/wcag-em-2/` and `https://www.w3.org/TR/WCAG-EM/` directly with plain `curl` (HTTP 200 — the challenge is egress-dependent), byte-compared them, and fetched the archived 1.0 Note and the history page. Either route works for future re-checks depending on network posture.
2. **Done:** [`docs/wcag-em-2-reference.md`](wcag-em-2-reference.md) committed — verified identity, step/sub-step map with the 1:1 1.0 mapping, Methodology Requirement framing, random-sample parameters (1.0-identical), Step 5.1 minimum report fields, statement conditions, glossary, and product-type/context notes. This assessment corrected in place; every *(verify)* mark resolved, **no residuals**: the TR copy matches the editors' draft, `/TR/WCAG-EM/` serves the 2.0 Note byte-identically, and the 1.0 delta is established by direct comparison of the two published Notes (the Note has no changelog appendix).

### Phase 1 — Reference & terminology refresh (docs only, no behavior change)

**Status: completed 2026-07-28.** Fixture, rubric (accept-either with 2.0 as bonus; scoring key renamed in lockstep with its must_have entry), bug-reporting EARL line (both mirrors), and README index landed.

3. `evals/suites/a11y-planner/fixtures/test-multi-page-audit.md` + `.metadata.yaml` + rubric: current name and URL; rubric explicitly accepts a 1.0 **or** 2.0 citation as the pass signal (training-data lag is real — a 2.0-only gate would fail good plans for years), with 2.0 terminology as bonus evidence, not a gate.
4. `bug-reporting` EARL section: one line noting WCAG-EM 2.0 and the planned EM 2 Report Tool.
5. This doc indexed from `README.md` docs list.

### Phase 2 — Audit-scope methodology wiring

**Status: completed 2026-07-28.** AUDIT-SCOPE MODE added to the planner protocol (both mirrors) with the five-step overlay, declarations, and the EM-does-not-supply rules; a11y-test §Scale-and-Sampling gained the random sample, representativeness check, complete-process routing, and state coverage; `docs/a11y-evaluation-report-contract.md` committed; `evaluation_context` added to the evidence-finding contract; CLAUDE.md routing note added. Phase 3 (eval re-run) remains open — it is a benchmark-spend decision.

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

- **Source basis — resolved.** This assessment was first written from secondary sources; Phase 0 (2026-07-28, two parallel reads reconciled) verified it against the published text and the corrections were minor (decimal sub-steps mapping 1:1 to 1.0's letters, the view→sample→sample-set chain, the five-conformance-requirements evaluation basis, the shortname now aliasing 2.0). Network note: the TR host's Cloudflare challenge is egress-dependent — plain `curl` works from unrestricted networks, and the Note's designated editors'-draft URL is the fallback for restricted ones.
- **Group Note status.** EM 2.0 is guidance. Procurement and legal contexts (VPATs, EN 301 549 workflows) will keep referencing specific versions on their own schedules; audit-scope outputs should cite the version the engagement requires, not assume 2.0.
- **Rubric transition hazard.** Grading audit plans on "cites WCAG-EM 2.0" too early punishes models with pre-2026 training data for knowing the methodology under its stable name; grading only 1.0 rewards stale citations. Accept-either with 2.0-as-bonus is deliberate.
- **Checklist creep.** The failure mode of adopting an evaluation methodology into a skills bundle is that every output grows a WCAG-EM section. The reject row exists for this; reviewers should treat an EM citation in a component-scope review as a finding against the output.

## What This Does Not Claim

- Not a new capability to test native apps, kiosks, or documents — the boundary is declared, not solved.
- Not a commitment to build the workflow audit mode, new eval lanes, or Report Tool integration on any schedule.
- Not a change to the critic's investigation protocol, the perspective/role audit taxonomies, or the severity scale.
- Not a claim that the bundle was "wrong" pre-EM-2.0: the component lifecycle was never in WCAG-EM's scope, in either version.

## Sources

**Primary (read in full, 2026-07-28, two parallel reads reconciled):** [WCAG-EM 2.0, W3C Group Note 23 July 2026 — TR copy](https://www.w3.org/TR/wcag-em-2/) (read directly; byte-identical at [/TR/WCAG-EM/](https://www.w3.org/TR/WCAG-EM/)) and the [editors' draft mirror](https://w3c.github.io/wai-wcag-em/) (the route that works behind restrictive egress); [WCAG-EM 1.0 dated Note](https://www.w3.org/TR/2014/NOTE-WCAG-EM-20140710/) (for the verified 1.0 delta); [publication history](https://www.w3.org/standards/history/wcag-em-2/). Verified extract: [`wcag-em-2-reference.md`](wcag-em-2-reference.md).

**Secondary (basis of the 2026-07-27 first draft):** [W3C WAI news, 2026-02-05 First Draft Note](https://www.w3.org/WAI/news/2026-02-05/wcag-em-2), [W3C news: Group Note Draft](https://www.w3.org/news/2026/group-note-draft-w3c-accessibility-guidelines-evaluation-methodology-wcag-em-2-0/), [WCAG-EM Overview (WAI)](https://www.w3.org/WAI/test-evaluate/conformance/wcag-em/), [WCAG-EM 2.0 publication history](https://www.w3.org/standards/history/wcag-em-2/), [Hidde de Vries (EM 2.0 editor): "WCAG-EM 2.0 lets you report on accessibility of more than just websites"](https://hidde.blog/wcag-em-apps/), [Centre for Accessibility Australia](https://www.accessibility.org.au/w3c-publishes-wcag-evaluation-methodology-wcag-em-2-0/), [accessibility.chat](https://www.accessibility.chat/articles/wcag-em-20-draft-expands-beyond-websites-to-mobile-apps-and-digital-products), plus the WCAG-EM 1.0 structure from training knowledge.
