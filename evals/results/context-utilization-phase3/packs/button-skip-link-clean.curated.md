## Evidence Digest

**def_rev**: 2026-08-26a
**Question (verbatim)**: Based on evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/004-127-0-0-1-8777-button-skip-link-clean-html.json and the tool that produced each (keyboard-a11y-tester driven trace / keyboard-a11y-tester batch-crawl findings / axe-core scan): does this evidence set show any interaction defect (focus not reaching or leaving an element as expected, an ARIA state changing with no accessible announcement, a keyboard-operability failure) and does it show any structural defect (a missing or incorrect ARIA role, landmark, label, or heading-order violation) for the component these artifacts describe?
**question_source**: Phase 3 pack curation — authored by a fresh agent from artifact filenames and tool types only; no fixture metadata, rubrics, ground-truth files, or lane README consulted
**Evidence class**: mixed
- Sub-question A ("interaction defect" — focus reach/leave, ARIA-state-change announcement, keyboard-operability): spans `keyboard-operability` + `focus-order-indicator` + `name-role-state`
- Sub-question B ("structural defect" — role/landmark/label/heading-order): `machine-detectable`

**Answerable from artifacts read**: partially — sub-question A: no (zero admissible artifact provided); sub-question B: partially (one axe-core data point, see below)

### Observations

**1. axe-core scan reports exactly one violation on the scanned page: `page-has-heading-one`, impact "moderate"**
```
observation_id: axe-004-page-has-heading-one
source: axe-core 4.13.0 (batch-scan wrapper; producing script/tool name not stated in artifact) — evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/004-127-0-0-1-8777-button-skip-link-clean-html.json
handle: [artifact path] → .viewports["1280x800"].violations[0]
actual_behavior: Single-page axe scan of http://127.0.0.1:8777/button-skip-link-clean.html, viewport 1280x800, http_status 200, run window 2026-08-26T00:05:58.585Z–00:06:01.857Z. Reports one violation (below), an empty `incomplete` array, `passes_count: 27`, `inapplicable_count: 62`. No other violation entries exist in the array.
wcag_or_apg: not stated in artifact (only axe tags "cat.semantics", "best-practice" are present — no WCAG SC number in this record)
evidence: |
  {"id":"page-has-heading-one","impact":"moderate","help":"Page should contain a level-one heading","help_url":"https://dequeuniversity.com/rules/axe/4.13/page-has-heading-one?application=playwright","tags":["cat.semantics","best-practice"],"node_count":1,"sample_selectors":["html"]}
  {"incomplete":[],"passes_count":27,"inapplicable_count":62}
```
Note: the rule id is `page-has-heading-one` (page lacks any `<h1>`) — a distinct axe rule from `heading-order` (skipped heading levels), one of the four examples the question names under "structural defect." Whether an absent-h1 finding counts toward that category is a mapping judgment left to the consumer.

### Absence claims (queries that returned nothing)

- No violation besides `page-has-heading-one` (no role/landmark/label finding among them) — query `.viewports["1280x800"].violations[] | select(.id != "page-has-heading-one")` on the artifact → empty
- No `heading-order`-rule violation specifically — query `.viewports["1280x800"].violations[] | select(.id == "heading-order")` on the artifact → empty
- No incomplete/manual-review items — query `.viewports["1280x800"].incomplete` on the artifact → `[]`
- No keyboard-a11y-tester artifact (driven trace or batch-crawl findings) exists in the artifact-path set handed to me for this question — the set contains exactly one path (the axe-core scan above); zero paths matching trace/findings-style output. This means sub-question A has **no evidence to read, not evidence of no defect** — the two are not the same claim, and the artifact set cannot distinguish them.

## Coverage Note

| Artifact | Partition | Scope / reason |
|---|---|---|
| evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/004-127-0-0-1-8777-button-skip-link-clean-html.json | READ | full (978 bytes) |
| keyboard-a11y-tester driven trace (tool type named in question, no path given) | NOT READ | out of question scope — question's parenthetical lists this tool, but no artifact path for it was included in the set handed to me |
| keyboard-a11y-tester batch-crawl findings (tool type named in question, no path given) | NOT READ | out of question scope — same reason |

**Not claimed**: This digest does not establish whether the component has any keyboard-operability, focus-order, or ARIA-state-announcement defect — no artifact capable of speaking to those classes (Playwright transcript, keyboard-a11y-tester trace, virtual-screen-reader assertion) was included in the evidence set. Per the a11y-test evidence contract, axe-core is the `machine-detectable` mode only and is not listed as valid evidence for any interaction class. For the structural sub-question, this digest covers only what axe-core's static rule set checks on one viewport of one page; it does not establish absence of structural defects outside axe's detectable rule set (e.g., ARIA states requiring computed-role/AT-output verification), nor does it confirm or rule out a `heading-order` (skip-level) condition specifically.