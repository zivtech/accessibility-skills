# Tools

The toolkit an accessibility investigation runs on: what each tool is pinned to, what evidence it produces, and — the part that matters most — what it cannot tell you.

Everything here is **routed, never vendored**. Each tool is pinned and called from the consuming project; none of their runtimes live in this repository. That is what keeps this a prompt-only repo.

## The stack

| Tool | Pin | Produces |
|---|---|---|
| [Playwright](https://playwright.dev/) | `1.62.1` | Real keyboard events via CDP, browser control, screenshots. The substrate everything else stands on |
| [axe-core](https://github.com/dequelabs/axe-core) | `4.13.0` | Machine-decidable WCAG violations, injected through `@axe-core/playwright` |
| [keyboard-a11y-tester](https://github.com/ezufelt/keyboard-a11y-tester) | release `0.5.0` (`7e852a7`, MIT) | Goal-driven journey audits: per-step trace, evidence-linked findings, reading-order census, focus-indicator measurement |
| [@guidepup/virtual-screen-reader](https://github.com/guidepup/virtual-screen-reader) | `0.32.1` (MIT) | Component-level accessible names, reading order, live-region announcements, asserted in your own test suite |
| [pa11y-ci](https://github.com/pa11y/pa11y-ci) | routed | Sitemap-wide sweeps; adds HTML_CodeSniffer `WCAG2AA` alongside axe |
| [eslint-plugin-jsx-a11y](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y) | routed | Static analysis of JSX/Vue source before anything renders |
| [BackstopJS](https://github.com/garris/BackstopJS) | routed | Visual regression, optional |
| [agent-browser](https://github.com/vercel-labs/agent-browser) | routed | Interactive reconnaissance: ARIA snapshots, reaching a page, verifying one fix |
| Webwright | Claude Code plugin | Python Playwright scripts generated from a prose spec |
| [@openacr/openacr](https://github.com/GSA/openacr) | `0.3.8` (CC0) | Validates and renders the conformance report draft |
| [exceljs](https://github.com/exceljs/exceljs) | `4.4.0` | Client-triage XLSX error workbook |

Licences and dependency-risk analysis for each adopted tool — including the escape hatch if it dies — live in that tool's adoption assessment, linked at the bottom of this page. Only the ones this repo has verified in writing are repeated above.

In-repo scripts that drive them: `references/baseline-url-scan.mjs` (sequential axe sweep over a URL list) and `references/build-error-workbook.mjs`.

## What each tool cannot tell you

This is the half that gets skipped, and skipping it is how a clean scan becomes a false conformance claim.

**axe-core** covers roughly **30–40% of WCAG issue classes**. It is never keyboard-operability evidence and never screen-reader evidence. A clean axe run means "no machine-decidable violations in the rules this version ships" — not "accessible." Rule sets are version-specific and partial by design.

**Static analysis** (`eslint-plugin-jsx-a11y`) reads source, not behaviour. It cannot see anything that depends on runtime state, focus order, or what actually gets announced.

**virtual-screen-reader** drives synthetic interactions through `user-event`, so it is **never keyboard-operability evidence** — it tells you what a screen reader would compute and announce, not whether a person can reach the control. Known blind spots: open shadow DOM, `aria-busy`. Two calibration rules learned the hard way: alerts mounted with content read silent (assert through the persistent-container pattern), and never combine it with fake timers, which wedges the singleton.

**keyboard-a11y-tester** emulates a screen reader; it is not a real one. Its batch-crawl 4.1.3 findings are prompts to run a driven session, not failures.

**Playwright MCP** — do not use for keyboard events. `browser_press_key` is silently dropped for most interactive widgets, which is worse than failing. Use `npx playwright test` or `agent-browser`.

**Every automated lane is a detector, not a verdict authority.** That rule is not specific to local models; it applies to the scanners too.

## Which tool answers which question

| Question | Tool |
|---|---|
| Does this component work for a keyboard user, in CI, forever? | `npx playwright test` with real key presses |
| What machine-decidable violations exist across these 40 URLs? | `baseline-url-scan.mjs` |
| …across this whole sitemap? | `pa11y-ci --sitemap <url> --runner axe --runner htmlcs` |
| Can a keyboard-only or screen-reader user complete this task on a live URL? | `keyboard-a11y-tester` |
| What does a screen reader announce for this component, pre-deploy? | `@guidepup/virtual-screen-reader` |
| What is the ARIA structure here — and did my fix work? | `agent-browser` (snapshot + ref pattern) |
| Did this page change visually? | Playwright screenshots or BackstopJS |
| Can I get a test script from this prose spec? | `/webwright:run` |

Do not run Webwright and agent-browser simultaneously — they contend for the same port.

## The manual layer

No tool in the table above closes the gap. The [ICT Testing Baseline crosswalk](../.claude/skills/a11y-test/references/ict-baseline-crosswalk.yaml) maps all 62 federal web baseline tests to the modes above and lands at **22 covered, 26 partial, 13 not covered, 1 that always passes by upstream design**.

The 13 not-covered rows are the deliverable, not the residue: they name exactly what has to go to manual testing and real assistive technology. An investigation that reports only automated results has not done those 13.

Real-AT automation (`@guidepup/guidepup`, driving actual VoiceOver or NVDA) is **deliberately deferred**, not overlooked. It needs macOS/Windows runners, and it shares a maintainer with virtual-screen-reader — so it is a correlated fallback, not risk diversification. The documented capability floor if that engine ever dies is the manual AT protocol, which is why the manual protocol stays a shipping gate rather than a legacy section.

## Evaluated and not adopted

Recorded so a future reader can tell a decision from an omission.

| Tool | Outcome |
|---|---|
| [Siteimprove Alfa](alfa-scan-adoption-assessment.md) | Negative result. Measured, written up, not adopted; reopen triggers recorded |
| Lighthouse accessibility audits | Measured head-to-head against `baseline-url-scan.mjs` on identical axe-core 4.13.0: **zero Lighthouse-only findings, our mode a strict superset on every page.** It also scored a page 100 while that page carried 4 real axe findings its 66-audit set omits — a false-clean hazard if the score is trusted alone |
| Playwright MCP for keyboard events | Rejected — silently drops key presses |
| Vital-Core scanner runtime | Reporting discipline adopted, [runtime rejected](vital-core-adoption-assessment.md) |

## Version discipline

Pins are exact and re-verified on upgrade, because these tools change what they detect between versions. A finding is only comparable to a prior finding if the engine version is the same — which is why every committed benchmark artifact records the engine version alongside the result, and why an axe-core bump is a re-baseline, not a routine dependency update.

Per-tool adoption assessments — what was adopted, what was deliberately left out, and the escape hatch if the dependency dies — are listed in the [docs index](README.md).
