# WCAG-EM 2.0 — Verified Reference

Phase 0 deliverable of [the adoption assessment](wcag-em-2-adoption-assessment.md). Facts below were read directly from the published document text on 2026-07-28, not from secondary sources.

**Provenance — two independent reads on 2026-07-28, agreeing on every shared fact:**

1. **Editors'-draft read (remote session):** `https://w3c.github.io/wai-wcag-em/` — the Note's own designated "Latest editor's draft" URL — after that session's egress allowlist was opened. From that egress, the TR host served a Cloudflare JS challenge to non-browser clients.
2. **TR read (local session):** `https://www.w3.org/TR/wcag-em-2/` and `https://www.w3.org/TR/WCAG-EM/` fetched directly with plain `curl` (HTTP 200, full content — the Cloudflare challenge is egress-dependent, not universal) and byte-compared; the archived 1.0 Note (`/TR/2014/NOTE-WCAG-EM-20140710/`) and the publication-history page fetched for the 1.0 delta and date pinning.

The TR read settles the first read's residual checks: the TR copy matches the editors' draft, and the 1.0-shortname question is answered below. Quotes are short and attributed; the source is © W3C, used under the [W3C Document License](https://www.w3.org/copyright/document-license/).

## Identity

- **Title:** WCAG Evaluation Methodology (WCAG-EM) 2.0 (W3C news announced it as "W3C Accessibility Guidelines Evaluation Methodology"; the document title is the former).
- **Status:** W3C **Group Note, 23 July 2026**, Note track — informative; "endorsed by the Accessibility Guidelines Working Group, but is not endorsed by W3C itself nor its Members." Builds on WCAG-EM 1.0 (2014, Eval TF of WCAG WG + ERT WG).
- **This version:** `https://www.w3.org/TR/2026/NOTE-wcag-em-2-20260723/` · **Latest published:** `https://www.w3.org/TR/wcag-em-2/` · **Editors' draft / feedback repo:** `w3c/wai-wcag-em` on GitHub.
- **Editors:** Hidde de Vries (Logius), Jeroen Hulscher (Logius), Steve Faulkner (Tetralogical). Former editors: Eric Velleman, Shadi Abou-Zahra.
- **History:** `https://www.w3.org/standards/history/wcag-em-2/` — Draft Note 5 February 2026 → Group Note 23 July 2026 (pins the date; the lone "24 July" secondary report was wrong). **Previous version:** `https://www.w3.org/TR/2014/NOTE-WCAG-EM-20140710/` (WCAG-EM 1.0).
- Abstract scope: evaluate how well **digital products** conform to WCAG 2; technology-agnostic; suitable for self-assessment and third-party evaluation. Explicitly does **not** add to or change WCAG 2 requirements.

## Where `/TR/WCAG-EM/` now resolves

Settled 2026-07-28 by the TR read: `https://www.w3.org/TR/WCAG-EM/` returns HTTP 200 with **no redirect** and serves content **byte-identical** to `https://www.w3.org/TR/wcag-em-2/`. The 1.0-era shortname is now an alias of the 2.0 Note (the editors'-draft read's "likely still serves 1.0" guess was wrong); WCAG-EM 1.0 remains reachable only at its dated URI. Consequences: a `w3.org/TR/WCAG-EM` citation is a live pointer to the current methodology but version-ambiguous; the canonical current citation is `/TR/wcag-em-2/` (the Note's own declared latest-published URL); the fixture rubric's URL keyword substring-matches both, which Phase 1 makes deliberate rather than lucky.

## Document structure

Introduction (target audience; relation to WCAG 2 conformance claims) → Using this methodology (required expertise; combined expertise; involving users; evaluation tools) → Scope of applicability (principle of product enclosure; product-type considerations; evaluation contexts) → **Evaluation procedure (Steps 1–5)** → Glossary → Background reading.

Each step and sub-step is framed as a numbered **"Methodology Requirement N[.M]"**. Sub-steps use decimal numbering (1.0 used letters):

| Step | Sub-steps |
|---|---|
| 1. Define the evaluation scope | 1.1 scope of the digital product · 1.2 conformance target (A/AA/AAA; "Level AA is the generally accepted and recommended target") · 1.3 accessibility support baseline · 1.4 additional evaluation requirements *(optional)* |
| 2. Explore the target digital product | 2.1 common views · 2.2 essential functionality · 2.3 variety of sample types · 2.4 technologies relied upon (note encourages also recording CMS, design system, frameworks, versions) · 2.5 other relevant samples (accessibility help, settings, contact, auth/financial) |
| 3. Select a representative sample set | 3.1 structured sample set · 3.2 randomly selected sample set · 3.3 complete processes |
| 4. Evaluate the selected sample set | 4.1 check all initial samples (SC · conforming alternate versions · accessibility support · non-interference) · 4.2 check all complete processes · 4.3 compare structured and random sample sets |
| 5. Report the evaluation findings | 5.1 document the outcomes of each step · 5.2 record the evaluation specifics *(optional)* · 5.3 evaluation statement *(optional)* · 5.4 aggregated score *(optional)* · 5.5 machine-readable reports *(optional)* |

Evaluators may return to any preceding step as new information emerges.

### 1.0 mapping (verified against the archived 1.0 Note)

Every 2.0 sub-step maps 1:1 onto a 1.0 sub-step — letters became decimals, "web pages" became views/samples, and **no sub-step was added or removed** (1.0 already had 2.e "Identify Other Relevant Web Pages", 4.a "Check All Initial Web Pages", and 5.e "Provide Machine-Readable Reports (Optional)"):

| WCAG-EM 2.0 | WCAG-EM 1.0 |
|---|---|
| 1.1 scope of the digital product | 1.a Define the Scope of the Website |
| 1.2 conformance target · 1.3 accessibility support baseline · 1.4 additional requirements | 1.b · 1.c · 1.d (same titles) |
| 2.1 common views | 2.a Identify Common Web Pages of the Website |
| 2.2 essential functionality | 2.b Identify Essential Functionality of the Website |
| 2.3 variety of sample types | 2.c Identify the Variety of Web Page Types |
| 2.4 technologies relied upon | 2.d Identify Web Technologies Relied Upon |
| 2.5 other relevant samples | 2.e Identify Other Relevant Web Pages |
| 3.1 structured sample set · 3.2 randomly selected sample set · 3.3 complete processes | 3.a Include a Structured Sample · 3.b Include a Randomly Selected Sample · 3.c Include Complete Processes |
| 4.1 check all initial samples | 4.a Check All Initial Web Pages |
| 4.2 check all complete processes · 4.3 compare structured and random sample sets | 4.b · 4.c Compare Structured and Random Samples |
| 5.1–5.5 report sub-steps | 5.a–5.e (same five, same optionality) |

## Load-bearing specifics (verbatim-anchored)

1. **Random sample sizing (3.2):** "The number of samples to randomly select is **10% of the structured sample set**" — added *on top* (80 structured → 8 random → 88 total). Must exclude samples already selected (pick a replacement on collision; if no new views exist, the step is complete), span the entire product scope, follow no predictable pattern, and the **selection method must be documented**. **Unchanged from 1.0** — the archived Note uses the identical 10%-of-structured rule with the same 80→8 example and no minimum in either version.
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

Two terms the adoption assessment expected in the glossary are defined elsewhere: **accessibility support baseline** is operational in Methodology Requirement 1.3 (the browsers, assistive technologies, and other user agents the product's features must be accessibility supported for — set with the commissioner, extendable mid-evaluation, narrowable only for closed networks); **complete process** is grounded in WCAG 2.2 conformance requirement 3, with its mechanics (starting point, default sequence, branch sequences) specified in Step 3.3.

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

All *(verify)* marks in the assessment are resolved — including the `/TR/WCAG-EM/` shortname resolution, settled above by the TR read. Corrections applied to the assessment: publication date firm (23 July — dated URI plus history page); sub-steps are decimal and map 1:1 onto 1.0's letters (the editors'-draft read initially called 5.5 "a new standalone sub-step" — wrong, 1.0 had 5.e); the sample/view/sample-set terminology chain; random-sample parameters (1.0-identical) and the 4.3 iteration loop; the five-conformance-requirements evaluation basis; EM 2.0's own caution against aggregated scores; and "accessibility support baseline" / "complete process" being operational definitions rather than glossary terms.

Two provenance notes: the Note has **no changes-from-1.0 appendix** — the 1.0 delta in this document comes from directly comparing the two published Notes, not from a changelog; and the "WCAG-EM 2 Report Tool later in 2026" plan remains a secondary-source claim (WAI announcement, not the spec), correctly attributed as a watch item.
