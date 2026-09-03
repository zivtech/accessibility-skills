# Content Judgment (draft-and-ratify) — Adoption Assessment

> **Status: CANDIDATE skill with an eval lane — PROMOTE-AFTER(critic REVISE folded + user approval), as of 2026-09-02.** The lane (`evals/suites/a11y-content-judgment/`) is calibrated and has first rows; its gate reading is *not met as the rubric stands* — one draw-stable false alarm on a row that WCAG 2.4.4 settles the other way (receipts: `evals/results/content-judgment-2026-09/`). Disposition and bar clauses: `docs/plans/2026-09-02-promotion-candidate-dispositions.md` (v3 addendum).

## What it is

A four-step pipeline for the WCAG criteria a scanner can enumerate but not decide — whether page titles, headings, form labels, link text in context, and image alternatives actually serve the person relying on them (2.4.2, 2.4.6, 2.4.4, 1.1.1), and whether the same destination is identified consistently across pages (3.2.4; 3.2.3 decided deterministically): inventory every such element across a URL list (Playwright, read-only), dedupe shared chrome and attach heuristic flags, have a hosted-tier model draft a per-row `yes | no | unsure` with a rationale that names what the person loses, and hand a named human ratifier a worklist. Origin: one engagement's OpenACR-lane phase where the owner delegated *drafting* to the agent and kept ratification human.

## Gap analysis — what it adds

- The **judgment-shaped middle** of an audit that a11y-test cannot measure and acr-reporting must not invent: rows that become criterion outcomes only through a human signature, with the model's reasons visible beside the machine's flags.
- **Dedupe at engagement scale** (a footer link on 19 pages is judged once, fans out with `view_count`), and the origin run's gotchas encoded in the builder rather than the prompt (URL fragments and query strings are identity; `javascript:` hrefs are not destinations; paired ID/name table columns are not a 3.2.4 case; 3.2.3 is relative order of shared items).
- A **calibration record** discipline: the split (random-row agreement vs `unsure` vs clean-but-`no`) tells a ratifier where to spend the second-reader budget.

## Gap analysis — what it does NOT cover (and what keeps covering it)

- **Interaction, timing, AT behaviour, structure beyond level skips, colour, media, CAPTCHA** — routed to a11y-test / a11y-critic; a request to extend the CSV to those is a scoping error the skill names.
- **Accessible-name computation** — `name` is a DOM approximation recorded with its source; the ratifier verifies in a browser when the approximation decides a row.
- **Outcome-map cells** — the skill never writes one; only a ratified receipt naming `ratified_by`, date, and row id reaches the report contract, and `drafted_by` travels with it.
- **Product and audience context for the judge** — the batch line carries neither (the origin run leaked product through the batch filename); the lane supplies a scenario paragraph per fixture. Filed as a critic finding.
- **Link context in table cells** — the inventory's context is the nearest text block, which for an ID-only cell is empty, so the rubric's paired-column rule is undecidable from the row. Six lane rows are invalid for this; filed as a critic finding.

## Adoption boundary (the ruling)

- **Playwright is a peer dependency of the consuming project or a scratch install, never vendored**; this repo gains no `package.json` (the lane's `build-fixtures.sh` follows the `verify`-skill reproduce-from-scratch pattern).
- **Drafts are detector output behind a mandatory human ratification.** Hosted tier drafts; a local model may pre-sort but is never the `drafted_by` of record — the repo-wide "detector, not verdict authority" rule, confirmed by the lane's qwen3.6:35b row (judged every card-grid link `yes`).
- **No outcome flips, no ACR inputs from the CSV.** acr-reporting must refuse a CSV whose `ratified_by` is blank; the report contract cites the ratification receipt, never the draft.
- **Client web standards are a separate scope** rendered as `client_*` columns and never merged into the WCAG column; the skill ships one worked example and deliberately no generalised rule table until a second client standard exists.
- **Conformance outcome and impact severity stay orthogonal** — the rows carry neither a severity nor an outcome term; a ratified `no` becomes a finding through bug-reporting, not a term through this skill.

## What the lane found about the rubric (2026-09-02)

The rubric's rule for repeated generic link text ("five identical *Learn more* links in a grid are `no` because they are indistinguishable when listed") reasons from 2.4.9 (Link Only, AAA). At the skill's Level AA target the ground is 2.4.4: whether the surrounding text is *programmatically determined* link context (same paragraph, list item, table cell, or F63 when it is not). The lane's card-grid rows happen to fail 2.4.4 (each card's text is a sibling `<p>` outside the link's context) so the rubric arm found them; the same rule made both draws mark a "Learn more" inside a sentence that names its destination `no` — a false alarm WCAG 2.4.4 does not support. Fixing the rule's *reason* (AA context, with the AAA listing concern as a note for the ratifier) is the promotion blocker; the fixtures and scorer are not.

## Reopen / watch triggers

- A second engagement's client web standard → generalise the client-scope matcher into a table.
- A second-reader lane once ≥ 1 more engagement run exists (the rubric is shared; the pass is downstream of the judge).
- Inventory context for `td` links widened to the row → re-validate the six invalid lane rows and lift `invalid`.
- R5 promotion to must-tier needs a positive set larger than six and a false-fire rate under 2 % (receipt in the results directory).
