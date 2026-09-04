# WAVE and Siteimprove integration handoff for `accessibility-testing`

Date: 2026-08-28

Status: implementation deferred to a fresh context

Target skill: `accessibility-testing`

Target source repository: `/Users/AlexUA_1/claude/zivtech-claude-skills`

Likely target source: `.claude/skills/accessibility-testing/SKILL.md`

Installed skill inspected for this handoff: `/Users/AlexUA_1/.agents/skills/accessibility-testing/SKILL.md`

## Why this handoff exists

The current `accessibility-testing` skill routes rendered-page checks through axe-core, Pa11y-CI, Playwright keyboard tests, and visual regression. It does not currently define WAVE or Siteimprove as detector lanes. During the authorized EPA product-a retest, a user-supplied WAVE report and a local Siteimprove Alfa Playwright run exposed useful signals that the axe/keyboard evidence alone did not present in the same form.

Add both tools as **supplemental detector lanes**. Do not make either tool a verdict authority, do not merge detector counts into keyboard or VoiceOver outcomes, and do not imply that agreement with WAVE or Siteimprove is a conformance test.

Negative space:

- This work does not replace real-keyboard Playwright testing.
- This work does not provide VoiceOver evidence.
- This work does not establish WCAG, Section 508, or product conformance.
- “Capture all” means preserve every outcome returned by the invoked tool for the observed route/state/viewport. It does not mean that any automated scanner can detect every accessibility defect.
- This handoff does not authorize WAVE credit purchases, account creation, credential use, redistribution of proprietary reports, or a new production service.

## Current repository warning

At handoff time, `/Users/AlexUA_1/claude/zivtech-claude-skills` was on `advisor/008-rename` with existing tracked modifications, including `.claude/skills/accessibility-testing/SKILL.md`. Treat those edits as another owner's work. Start the implementation context by resolving the intended branch and dirty baseline; do not overwrite or revert them.

## WAVE lane to add

### Supported execution modes

Document three explicit modes, in priority order:

1. **Visible browser extension/report observation** for a user-supplied report. Record the exact report URL, evaluated URL, page state, viewport when observable, timestamp, visible WAVE category totals, item-type totals, WAVE version if exposed, and capture limitations. The extension evaluates rendered and dynamic content locally in the browser and does not send page content to the WAVE server.
2. **WAVE subscription API** when the operator supplies an authorized `WAVE_API_KEY`. The key must come from the environment, must never be written to URLs in logs or evidence, and must be redacted from errors. Default to `SKIPPED_CREDENTIAL_REQUIRED` when absent. Respect WAVE's limit of no more than two simultaneous API requests.
3. **Licensed stand-alone API/Testing Engine** when an engagement already provides the licensed runtime. Route to it; do not copy or vendor the WAVE engine into the skill repository.

Official references:

- Browser extension behavior and privacy: <https://wave.webaim.org/extension/>
- API licensing and credits: <https://wave.webaim.org/api/>
- API v3.1 parameters and response contract: <https://wave.webaim.org/api/details>
- Terms governing report/data redistribution: <https://wave.webaim.org/terms>

### API defaults and evidence

For selector-bound evidence, use `reporttype=4`; it returns CSS selectors and contrast data and consumes three credits. `reporttype=3` returns XPath instead. Record:

- requested and final URL;
- HTTP status reported by WAVE;
- viewport width, user agent override, and `evaldelay`;
- WAVE API version and report type;
- credits consumed/remaining without exposing the API key;
- raw response SHA-256 and byte count;
- category, item ID, description, count, and every returned selector/XPath;
- stable local finding fingerprint derived from route identity + viewport + WAVE item ID + target locator;
- `error`, `contrast`, and `alert` as candidate-finding categories;
- `feature`, `structure`, and `aria` as informational observations unless independent review identifies a defect.

Do not republish or sell WAVE reports or WAVE-derived counts/listings without confirming WebAIM permission. An engagement may retain private, access-controlled evidence and independently verify issues, but external reporting should describe the independently validated defect rather than reproduce proprietary WAVE report data by default.

## Siteimprove lane to add

### Supported execution modes

1. **Siteimprove Accessibility Checker browser extension** for user-visible manual investigation of protected or dynamic content.
2. **Siteimprove Accessibility Code Checker / Alfa** for reproducible Playwright evidence in a consuming project. The official integration uses `@siteimprove/alfa-test-utils` plus `@siteimprove/alfa-playwright` and supports Playwright, Puppeteer, Selenium, and Cypress.
3. **Siteimprove platform/API export** only when the engagement supplies the product access and credentials. Missing credentials must produce a skipped/untested lane, never a clean result.

Official references:

- Browser extension behavior: <https://help.siteimprove.com/support/solutions/articles/80000448491>
- Accessibility Code Checker overview: <https://help.siteimprove.com/support/solutions/articles/80001151769-accessibility-code-checker>
- Alfa/Code Checker setup: <https://alfa.siteimprove.com/code-checker/getting-started>
- Package installation: <https://alfa.siteimprove.com/code-checker/getting-started/installation>
- Playwright usage: <https://alfa.siteimprove.com/code-checker/getting-started/usage/playwright>

### Package and evidence contract

Keep the skill repository prompt-only. Document exact-pinned packages for installation in the consuming audit/project; do not add them as dependencies of the skill repository. At this handoff, npm resolved these packages at `0.84.2`:

```bash
npm install --save-dev --save-exact \
  @siteimprove/alfa-test-utils@0.84.2 \
  @siteimprove/alfa-playwright@0.84.2
```

The product-a proof run reported Alfa engine `0.119.0`; record both wrapper and engine versions because they can drift independently. Persist:

- requested/final URL, HTTP status, title, viewport, user agent, load/settle policy, and timestamp;
- every `failed`, `cantTell`, and `passed` outcome without collapsing `cantTell` into pass or fail;
- rule URI, target internal/serialization ID, resolved DOM target descriptor, expectation diagnostics, and bounding box when available;
- raw audit JSON SHA-256 and byte count;
- per-rule totals and per-outcome records;
- WCAG criterion and level separately from detector result;
- an explicit scope classification such as `WCAG_2_2_AA`, `AAA`, `ADVISORY`, or `UNMAPPED`.

The level separation is load-bearing. In the product-a proof, most Siteimprove failures were AAA or advisory rather than WCAG 2.2 AA:

| Rule | Observed failures | Scope |
|---|---:|---|
| SIA-R66 Text has enhanced contrast | 9 | WCAG 1.4.6, AAA |
| SIA-R74 Paragraph font sizes are not absolute | 7 | WCAG 1.4.8, AAA |
| SIA-R73 Paragraphs have sufficient line height | 13 | WCAG 1.4.8, AAA |
| SIA-R113 Target Size (Minimum) | 4 | WCAG 2.5.8, AA candidate |
| SIA-R57 Perceivable text is in a landmark | 2 | WAI-ARIA APG advisory |
| SIA-R111 Target Size (Enhanced) | 7 | WCAG 2.5.5, AAA |

Capture all six rule groups, but only the SIA-R113 outcomes enter the WCAG 2.2 AA candidate queue without a separate scope decision. The four SIA-R113 targets still require independent review because the rule documents assumptions and known false-positive/false-negative boundaries.

## Cross-tool normalization

Add a shared detector receipt shape or documented mapping with these minimum fields:

```yaml
tool:
  name: null
  version: null
  execution_mode: null
observation:
  requested_url: null
  final_url: null
  captured_at: null
  viewport: null
  page_state: null
raw_evidence:
  path: null
  sha256: null
  bytes: null
outcomes:
  - tool_rule_id: null
    tool_result: DETECTED|CANT_TELL|PASS|INFORMATIONAL
    target_locator: null
    target_descriptor: null
    wcag_criteria: []
    wcag_level: A|AA|AAA|ADVISORY|UNMAPPED
    triage: UNREVIEWED|CONFIRMED|DISMISSED|DUPLICATE|OUT_OF_SCOPE
    independent_evidence: []
```

Do not deduplicate by rule name alone. Use route identity, viewport/state, semantic defect class, and target identity. Preserve each tool's original outcome even when multiple tools identify the same candidate. Cross-tool agreement can increase triage priority; it cannot replace target-level verification.

## Tests required in the implementation context

### WAVE adapter/ingest tests

- Parse representative report types 1, 2, 3, and 4.
- Preserve every category/item/selector or XPath returned by the fixture.
- Reject count/detail mismatches and malformed responses.
- Redact API keys from requests, errors, logs, and receipts.
- Produce `SKIPPED_CREDENTIAL_REQUIRED` without an API key.
- Enforce no more than two concurrent subscription API calls.
- Preserve non-success HTTP/API statuses as blocked/tool errors, never PASS.
- Keep `feature`, `structure`, and `aria` informational by default.
- Test report/data redistribution warnings in the documentation/output contract.

### Siteimprove adapter/ingest tests

- Exact-pin and record wrapper plus Alfa engine versions.
- Serialize all failed, `cantTell`, and passed outcomes.
- Resolve text and element targets from serialized Alfa page data without dropping parent context.
- Preserve expectation diagnostics and bounding boxes.
- Map rule URI to criterion/level without promoting AAA or advisory rules into the AA queue.
- Treat `cantTell` as unresolved.
- Fail closed on missing or unreadable raw evidence.

### Reconciliation tests

- Two tools flagging one target produce two source outcomes and one deduplicated candidate after review.
- Similar rule labels on different targets stay separate.
- A clean tool result never overrides a keyboard, VoiceOver, or independently confirmed failure.
- A detector failure never overrides a real-keyboard PASS for a different behavior class.
- Raw-evidence hashes replay without drift.

## product-a proof artifacts available for the later retest

These artifacts are supplemental and currently local to the audit worktree. They are comparison inputs, not immutable golden counts because the live page and engines can change.

WAVE visible-report observation:

- `/Users/AlexUA_1/claude/a11y-audits-epa-interactive-retest/2026-08-24-epa-interactive-retest/evidence/findings/product-a-wave-observation-20260828.json`
- SHA-256: `44493994ab8a7ae999aeb27f7b72a98b8384e10369e56026ec9dec06f68f3576`
- Observed: 3 errors, 27 contrast errors, 28 alerts, 38 features, 49 structural elements, 82 ARIA items, AIM score 5/10.

Siteimprove Alfa Playwright proof:

- Receipt: `/Users/AlexUA_1/claude/a11y-audits-epa-interactive-retest/2026-08-24-epa-interactive-retest/evidence/findings/product-a-siteimprove-alfa-20260828/run-receipt.json`
- Receipt SHA-256: `adaa74a53a043b370a52c935d631b52d74acd7e6067c9fbad102fe8c01e880e1`
- Raw audit: `/Users/AlexUA_1/claude/a11y-audits-epa-interactive-retest/2026-08-24-epa-interactive-retest/evidence/findings/product-a-siteimprove-alfa-20260828/raw-audit.json`
- Raw audit SHA-256: `26dacab2ee28f274ec99848bd9af15d470b215ff24056db9aba4500789d232de`
- Observed: 88 evaluated rules; 6 failing rules; 42 failed outcomes; 3 rules with 67 `cantTell` outcomes; 762 passed outcomes.

Experimental proof runner, not yet an adopted skill artifact:

- `/Users/AlexUA_1/claude/a11y-audits-epa-interactive-retest/2026-08-24-epa-interactive-retest/evidence/harness/siteimprove-playwright-scan.mjs`

Review this runner for generalization rather than copying it blindly. In particular, decide whether full serialized Alfa page data belongs in retained evidence or should be reduced to target-bound outcomes plus a quarantined raw artifact.

## Retest acceptance criteria

After the skill changes are implemented and reviewed in a separate context:

1. Run the WAVE and Siteimprove lanes against the exact product-a Philadelphia route at the documented viewport and page state.
2. Record current versions, route identity, timestamps, hashes, and complete tool-returned outcomes.
3. Compare current categories/rules with the proof artifacts, explaining drift rather than requiring identical live counts.
4. Triage every WAVE error/contrast/alert and every Siteimprove failed/`cantTell` outcome into confirmed, dismissed, duplicate, out-of-scope, or unresolved.
5. Independently verify candidate WCAG 2.2 AA defects at the target level before adding them to the EPA result.
6. Do not rerun the already admitted product-a keyboard PASS/FAIL rows. Detector retesting is a separate lane; only unresolved keyboard rows that gain new target/state mappings should receive targeted keyboard collection.
7. Run `a11y-critic` and `perspective-audit` on the integration and the reconciled results before client reporting.
8. Keep the existing negative-space statement: this is an AI-operated accessibility demonstration, not blind-user usability research, a human-usability claim, or a conformance certification.

## Definition of done for the fresh context

- `accessibility-testing` documents WAVE and Siteimprove as optional supplemental lanes.
- Any reusable adapter or ingest code has fixture tests and secret-redaction tests.
- The skill repository remains prompt-only; proprietary engines and consuming-project dependencies are not vendored.
- WAVE licensing/redistribution constraints are explicit.
- Siteimprove rule level/scope is preserved.
- Evidence schemas preserve raw provenance, `cantTell`, target identity, and hashes.
- The product-a detector retest is completed once, with no broad replay of admitted keyboard outcomes.
- Implementation, review, audit evidence, client reporting, publication, and acceptance remain distinct states.
