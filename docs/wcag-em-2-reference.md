# WCAG-EM 2.0 — Verified Reference

Phase 0 deliverable of [the adoption assessment](wcag-em-2-adoption-assessment.md). Facts below were read directly from the published document text on 2026-07-28, not from secondary sources.

**Provenance:** read from `https://w3c.github.io/wai-wcag-em/` — which the Note's own front matter names as its "Latest editor's draft" URL — after the session's egress allowlist was opened for `www.w3.org` and GitHub Pages. The TR-hosted copy (`https://www.w3.org/TR/wcag-em-2/`) serves a Cloudflare JS challenge to non-browser clients and was not fetched; the editors'-draft page carries the identical Group Note front matter (title, date, this-version URL), so divergence risk is negligible. **Residual checks:** a human-browser glance at the TR copy, and where the 1.0 shortname `https://www.w3.org/TR/WCAG-EM/` now resolves (the Note lists 1.0, `https://www.w3.org/TR/2014/NOTE-WCAG-EM-20140710/`, as "Previous version", so the old shortname likely still serves 1.0 — relevant only to the fixture rubric's URL keyword).

## Identity

- **Title:** WCAG Evaluation Methodology (WCAG-EM) 2.0 (W3C news announced it as "W3C Accessibility Guidelines Evaluation Methodology"; the document title is the former).
- **Status:** W3C **Group Note, 23 July 2026**, Note track — informative; "endorsed by the Accessibility Guidelines Working Group, but is not endorsed by W3C itself nor its Members." Builds on WCAG-EM 1.0 (2014, Eval TF of WCAG WG + ERT WG).
- **This version:** `https://www.w3.org/TR/2026/NOTE-wcag-em-2-20260723/` · **Latest published:** `https://www.w3.org/TR/wcag-em-2/` · **Editors' draft / feedback repo:** `w3c/wai-wcag-em` on GitHub.
- **Editors:** Hidde de Vries (Logius), Jeroen Hulscher (Logius), Steve Faulkner (Tetralogical). Former editors: Eric Velleman, Shadi Abou-Zahra.
- Abstract scope: evaluate how well **digital products** conform to WCAG 2; technology-agnostic; suitable for self-assessment and third-party evaluation. Explicitly does **not** add to or change WCAG 2 requirements.

## Document structure

Introduction (target audience; relation to WCAG 2 conformance claims) → Using this methodology (required expertise; combined expertise; involving users; evaluation tools) → Scope of applicability (principle of product enclosure; product-type considerations; evaluation contexts) → **Evaluation procedure (Steps 1–5)** → Glossary → Background reading.

Each step and sub-step is framed as a numbered **"Methodology Requirement N[.M]"**. Sub-steps use decimal numbering (1.0 used letters):

| Step | Sub-steps |
|---|---|
| 1. Define the evaluation scope | 1.1 scope of the digital product · 1.2 conformance target (A/AA/AAA; "Level AA is the generally accepted and recommended target") · 1.3 accessibility support baseline · 1.4 additional evaluation requirements *(optional)* |
| 2. Explore the target digital product | 2.1 common views · 2.2 essential functionality · 2.3 variety of sample types · 2.4 technologies relied upon (note encourages also recording CMS, design system, frameworks, versions) · 2.5 other relevant samples (accessibility help, settings, contact, auth/financial) |
| 3. Select a representative sample set | 3.1 structured sample set · 3.2 randomly selected sample set · 3.3 complete processes |
| 4. Evaluate the selected sample set | 4.1 check all initial samples (SC · conforming alternate versions · accessibility support · non-interference) · 4.2 check all complete processes · 4.3 compare structured and random sample sets |
| 5. Report the evaluation findings | 5.1 document the outcomes of each step · 5.2 record the evaluation specifics *(optional)* · 5.3 evaluation statement *(optional)* · 5.4 aggregated score *(optional)* · 5.5 machine-readable reports *(optional, new as its own sub-step)* |

Evaluators may return to any preceding step as new information emerges.

## Load-bearing specifics (verbatim-anchored)

1. **Random sample sizing (3.2):** "The number of samples to randomly select is **10% of the structured sample set**" — added *on top* (80 structured → 8 random → 88 total). Must exclude samples already selected (pick a replacement on collision; if no new views exist, the step is complete), span the entire product scope, follow no predictable pattern, and the **selection method must be documented**.
2. **Representativeness check (4.3):** the random set must show no *types of content* and no *evaluation findings* absent from the structured set. If it does, "evaluators need to go back to Step 3" (and possibly adjust Step 2 findings) and the step "is repeated until the structured sample set is adequately representative."
3. **Evaluation basis (4):** each sample is checked against **the five WCAG 2 conformance requirements** at the target level — conformance level, full pages, complete processes, only accessibility-supported ways of using technologies, non-interference — not SC pass/fail alone. Alternate versions are "not considered to be separate samples" — evaluated with the sample as one unit. SC with no relevant content are *satisfied* per WCAG 2 (a report may optionally mark them "not present"). Repeated components (header, nav, search) need not be re-evaluated per occurrence unless they differ.
4. **Complete processes (3.3/4.2):** include the process starting point, the **default sequence** (standard use case: no input errors, no optional selections) and **commonly-accessed, critical branch sequences** (a branch may terminate where it re-enters the default). Record the *actions* needed to move sample-to-sample — "In most cases the web address (URL) will not be sufficient to identify the sample in a complete process." In Step 4.2, evaluate only the content that changes along the process; interaction, form feedback, error messages, and settings/device variations are in scope.
5. **Minimum report contents (5.1):** evaluator name; evaluation commissioner; date; scope + conformance target + baseline + any additional requirements (Step 1 outcomes); technologies relied upon; the three sample lists (structured; random **with selection method**; complete processes); outcomes of 4.1, 4.2, 4.3. Optional: version/identifier, dates of repeat evaluations, common views/functionality/sample-type lists. "Reports should include **at least one example for each conformance requirement and WCAG 2 Success Criterion not met**"; clear issue descriptions, steps to reproduce, severity, and screenshots are encouraged; outcomes may be per-sample or aggregated.
6. **Evaluation specifics (5.2, optional):** archive evaluated samples (note: tools can save the *rendered DOM*, "often different" from initial resources), screenshots, paths/settings/credentials to replicate, names+versions of tools/browsers/AT, and methods used. May need security/privacy precautions.
7. **Evaluation statement (5.3, optional):** allowed only when every non-optional methodology requirement is satisfied, **all evaluated samples satisfy the conformance target**, and the owner commits to maintaining accuracy. Minimum contents: statement date; guidelines title/version/URI; conformance level; product scope; technologies relied upon; baseline. Partial-conformance statements add the non-conforming areas and the reason ("third-party content" or "lack of accessibility support for languages"). Reminder in the text: **"using this methodology alone does not result in WCAG 2 conformance claims"** — sampling can never rule out unidentified errors.
8. **Aggregated scores (5.4, optional and cautioned):** "there is currently no single metric that is known to address the required reliability, accuracy, and practicality. In fact, aggregated scores can be misleading…" Any score used must have its approach documented for transparency and repeatability.
9. **Machine-readable reports (5.5):** EARL "is recommended."
10. **Skipping sampling:** evaluating the entire product is recommended when feasible; skip sampling for products with few views or that can't be split into views — "use the entire product as 'selected sample set'" thereafter.
11. **Sample-set size factors (Step 3 intro):** size, age, complexity (interactivity, generated content, versions/adaptivity), consistency (variety of sample types/functionality/technologies/coding styles), adherence to development processes (formalization, training, tooling, number of authors), required confidence, and **availability of prior evaluation findings** (prior manual/automated test results permit smaller sample sets).

## Glossary (verbatim definitions)

- **view** — "A web page, document, software or view, or an equivalent unit of conformance defined in the accessibility standard being evaluated."
- **sample** — "view that is included in the sample set." **sample set** — "list of samples selected for evaluations." (So the chain is view → sample = a *selected* view → sample set.)
- **digital product** — "coherent collection of one or more related views that together provide common use or functionality" (websites, web apps, e-books, kiosk apps, mobile apps, documents). Products may contain sub-products (a shop area, a blog area) each evaluable as a product.
- **common views** — views relevant to the entire product (home, login, entry points, contact/help/legal, typically linked from header/footer/nav).
- **essential functionality** — "functionality that, if removed, fundamentally changes the use or purpose of the product for users."
- **evaluator** / **evaluation commissioner** — who performs vs. who commissioned the evaluation (commissioner may be owner, developer, procurer, or survey owner).

## Scope-of-applicability notes that matter to this bundle

- **Principle of product enclosure:** scope includes "all views, states and functionality of a digital product, without excluding specific parts" — exclusions conflict with WCAG 2's full-pages/complete-processes requirements or distort results. (Generalizes 1.0's full-pages provision.)
- **Non-URL products:** for native/hybrid apps and hardware-terminal kiosks, "a list of URLs cannot be generated"; samples are identified "with unique screenshots and/or descriptions of the path that lead to the specific sample" (documents: title/filename). Web-testable kiosk interfaces follow the web-application considerations.
- **Third-party content:** points to WCAG 2's Statement of Partial Conformance; evaluators determine whether such content is "regularly monitored and repaired (within two business days)" and whether non-conforming content is clearly identified.
- **Evaluating during development:** the methodology "has been primarily designed for reviewing digital products that are already developed"; early-stage use is possible with adaptation, but such evaluations "can quickly become obsolete" and "should not be used for making statements nor conformance claims about the finalized digital product."
- **Re-running evaluations:** keep a sub-set of prior samples for comparability and replace a sub-set (typically about half) for coverage; sample size/approach usually unchanged unless the product changed significantly.
- **Large-scale surveying** (mass automated evaluation of many products) is explicitly *not* what this methodology is for.
- **Involving users:** "not required… [but] strongly recommended" to involve people with disabilities during evaluation; expert evaluation alone misses barriers.
- **Preliminary review:** WAI "Easy Checks" is positioned as the complementary lightweight pre-pass.

## What this settles from the adoption assessment

All *(verify)* marks in the assessment are resolved except the `/TR/WCAG-EM/` shortname resolution (above). Corrections applied to the assessment: publication date firm (23 July); sub-steps are decimal with a new standalone 5.5; the sample/view/sample-set terminology chain; random-sample parameters and the 4.3 iteration loop; the five-conformance-requirements evaluation basis; and EM 2.0's own caution against aggregated scores.
