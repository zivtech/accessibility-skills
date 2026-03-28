# External Skills Inventory for a11y-meta-skills

Research conducted 2026-03-28. This document catalogs publicly available Claude Code skills relevant to the **a11y-critic** (post-implementation accessibility design review) and **a11y-planner** (pre-implementation accessibility design specification).

For each skill: what it does, how it differs from our approach, what techniques are worth adopting, and whether it requires external tooling.

---

## Landscape Summary

**13 external a11y skills found** across skills.sh, tessl.io, and GitHub. No external skill implements a planner-critic pair. All are either auditors (scan + report), guideline guardrails (coding standards), or single-criterion analyzers. Our planner-critic architecture is unique in the ecosystem.

**Key gap confirmed:** No external skill separates planning (what to build accessibly) from critique (did we build it accessibly). The closest analogue is AccessLint's `reviewer` agent, which performs multi-step WCAG audits but has no planning counterpart.

**Sources searched:**
- skills.sh (90,352+ skills indexed)
- tessl.io/registry (quality-scored registry with Snyk scanning)
- GitHub search (claude code + accessibility, .claude/skills + a11y)
- VoltAgent/awesome-agent-skills, travisvn/awesome-claude-skills (curated lists)

---

## Tier 1 — High-Value Skills (directly relevant techniques)

### snapsynapse/skill-a11y-audit
- **Source:** [snapsynapse/skill-a11y-audit](https://github.com/snapsynapse/skill-a11y-audit)
- **What it does:** 6-phase audit pipeline: environment discovery → automated scanning (axe-core + Lighthouse) → WCAG 2.1 AA compliance mapping → dynamic manual check guidance → configurable output (markdown/JSON/issues) → issue creation. Version 12, actively maintained.
- **Use for:** Neither directly (auditor, not planner/critic). **Stealable techniques** are the value.
- **Key techniques worth adopting:**
  1. **Dynamic manual check prioritization** — Phase 4 reorders manual testing checklists based on what axe found. If ARIA violations detected → screen reader items prioritized; if no form violations → form testing deprioritized. Our a11y-planner's testing strategy (Phase 8) is static; this adaptive approach is better.
  2. **Template-aware sampling** — `discover.js` classifies pages into template groups and selects representatives for large sites (>15 routes), rather than testing every page. Our skills don't address scale/sampling at all.
  3. **Delta comparison** — `--previous` flag shows fixed/new/changed violations between audit runs. Useful concept for a11y-critic when reviewing incremental work.
  4. **Compliance matrix completeness** — Hardcodes all 50 WCAG 2.1 AA criteria and maps every finding to specific SC. Our critic maps to WCAG but doesn't systematically verify coverage of all 50 criteria.
  5. **CI integration asset** — Ships a GitHub Actions workflow for recurring audits.
- **MCP/API:** Bundled axe-core + puppeteer (auto-installs to `deps/`)
- **Cost:** Free
- **Explicit non-goals:** No code fixes, no PDF audit, no VPAT, no real AT testing — clear scope boundaries we should emulate.

### AccessLint/claude-marketplace
- **Source:** [accesslint/claude-marketplace](https://github.com/accesslint/claude-marketplace)
- **What it does:** Multi-skill a11y toolkit with 4 specialized skills (contrast-checker, link-purpose, use-of-color, refactor) + 1 reviewer agent + companion MCP server for programmatic contrast analysis. The only dedicated accessibility-first Claude Code plugin found.
- **Use for:** Critic reference (reviewer agent performs multi-step WCAG 2.1 audits)
- **Key techniques worth adopting:**
  1. **MCP-based contrast tooling** — `calculate_contrast_ratio`, `analyze_color_pair`, `suggest_accessible_color` as programmatic tools rather than just prompt guidance. Our critic discusses contrast conceptually but can't calculate it. Adding contrast MCP as an optional tool would make color findings evidence-based.
  2. **Single-criterion decomposition** — Separating contrast (1.4.3/1.4.11), link purpose (2.4.4), and use-of-color (1.4.1) into dedicated skills rather than one monolithic review. Our critic handles all criteria in one pass; the decomposed approach catches more per-criterion depth.
  3. **Text-in-UI-component distinction** — Contrast-checker explicitly separates text contrast (4.5:1) from UI component boundary contrast (3:1), with the rule that "text within UI components must meet TEXT requirements." Our critic doesn't make this distinction explicit.
  4. **Refactor skill with style preservation** — The refactor skill fixes a11y issues while explicitly preserving code style and conventions. Useful pattern for executor-stage guidance.
- **MCP/API:** `@accesslint/mcp` npm package (3 tools)
- **Cost:** Free
- **Architecture:** Plugin format (.mcp.json + agents + skills), not standalone SKILL.md

### addyosmani/web-quality-skills — accessibility
- **Source:** [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills)
- **What it does:** WCAG 2.2 reference skill covering POUR principles with code examples. Part of a 6-skill Lighthouse-themed bundle. Author: Addy Osmani (Google Chrome team).
- **Use for:** Both (reference material)
- **Key techniques worth adopting:**
  1. **WCAG 2.2 explicit coverage** — One of only 2 community skills targeting WCAG 2.2 (vs 2.1). Includes 2.4.11/2.4.12 focus appearance criteria. Our skills reference WCAG 2.2 but should verify we cover the 2.2-specific criteria (2.4.11 Focus Not Obscured, 2.4.12 Focus Not Obscured Enhanced, 2.4.13 Focus Appearance, 2.5.7 Dragging Movements, 2.5.8 Target Size, 3.2.6 Consistent Help, 3.3.7 Redundant Entry, 3.3.8 Accessible Authentication, 3.3.9 Accessible Authentication Enhanced).
  2. **Visually-hidden class pattern** — Provides canonical `.visually-hidden` CSS that our planner could reference as a standard pattern.
  3. **Lighthouse score targeting** — Frames a11y as a measurable score (target: 100), which provides a concrete benchmark our testing strategy could reference.
- **MCP/API:** None (guidelines only)
- **Cost:** Free

### meodai/skill.color-expert
- **Source:** [meodai/skill.color-expert](https://github.com/meodai/skill.color-expert)
- **What it does:** Color science specialist with 140+ reference files (286K words). Covers WCAG contrast AND APCA (Advanced Perceptual Contrast Algorithm — the WCAG 3 algorithm). Research data: ~281 trillion hex pairs analyzed, 11.98% pass WCAG AA, only 0.08% pass APCA 90.
- **Use for:** Critic (contrast analysis depth)
- **Key techniques worth adopting:**
  1. **APCA coverage** — The only skill covering the WCAG 3 contrast algorithm alongside WCAG 2.x. Our skills don't mention APCA at all. As WCAG 3 emerges, having APCA awareness is forward-looking.
  2. **OKLCH/OKLAB for accessible palette generation** — Perceptually uniform color spaces for generating compliant palettes. Our visual accessibility plan (Phase 6) mentions contrast ratios but not the color science tools for achieving them.
  3. **Contrast-first color composition** — `apcach` approach where contrast compliance is the starting constraint, not an afterthought. Relevant for our planner's visual accessibility planning.
- **MCP/API:** None (reference files only)
- **Cost:** Free

---

## Tier 2 — Strong Supporting Skills

### ehmo/platform-design-skills — web
- **Source:** [ehmo/platform-design-skills](https://github.com/ehmo/platform-design-skills)
- **What it does:** Cross-platform design rules (web + iOS + Android + macOS + tvOS + visionOS + watchOS). 300+ rules drawing from Apple HIG, Material Design 3, and WCAG 2.2. Accessibility is Section 1 (marked `[CRITICAL]`).
- **Use for:** Both (cross-platform reference)
- **Key techniques worth adopting:**
  1. **Focus indicator area formula** — References the WCAG 2.2 focus indicator area calculation (2.4.11/2.4.12), which our skills mention conceptually but don't provide the formula for.
  2. **Cross-platform awareness** — Our skills are web-only. For teams building React Native or Capacitor apps, platform-specific a11y guidance matters.
- **MCP/API:** None
- **Cost:** Free

### ramzesenok/iOS-Accessibility-Audit-Skill
- **Source:** [ramzesenok/iOS-Accessibility-Audit-Skill](https://github.com/ramzesenok/iOS-Accessibility-Audit-Skill)
- **What it does:** SwiftUI-specific WCAG 2.2 auditor with dual mode: WCAG coverage audit + patch-ready remediation. Priority-grouped output (P0/P1/P2). Ships 6 reference docs. Has WCAG2Mobile interpretation layer.
- **Use for:** Critic reference (output format, evidence model)
- **Key techniques worth adopting:**
  1. **"Needs user verification" flag** — Explicitly marks code-indeterminate items that require manual testing rather than pretending the audit is conclusive. Our critic uses "Open Questions" but this is more precisely scoped.
  2. **Patch-ready snippets per finding** — Each finding includes an embedded code fix, not just a description. Our critic deliberately doesn't fix (read-only), but providing suggested fix snippets alongside findings would be valuable.
  3. **Reference library architecture** — 6 focused reference docs (workflow, checklist, WCAG2Mobile, API examples, remediation guide, manual checklist) loaded in sequence. Our skills are monolithic prompts; decomposing into loadable references could improve focus.
- **MCP/API:** None (source code analysis only)
- **Cost:** Free

### airowe/claude-a11y-skill
- **Source:** [airowe/claude-a11y-skill](https://github.com/airowe/claude-a11y-skill)
- **What it does:** 3-mode web auditor: runtime (axe-core via CDN injection), static (eslint-plugin-jsx-a11y), full (combined). React/Next.js/Vue focus.
- **Use for:** Testing strategy reference
- **Key techniques worth adopting:**
  1. **Static + runtime dual mode** — Running both eslint-plugin-jsx-a11y AND axe-core catches different classes of issues. Our planner's testing strategy mentions axe-core but not jsx-a11y static analysis as a distinct testing layer.
  2. **False positive guidance** — Explicit list of common jsx-a11y false positives (custom `role` props, passthrough ARIA, dynamic content). Our critic's realist check could benefit from a curated false-positive catalog.
  3. **Temporary standalone ESLint config** — Creates `eslint.a11y.mjs` to avoid ESLint 9 flat config compatibility issues, runs, then removes. Practical pattern for our testing strategy.
- **MCP/API:** axe-core (CDN), eslint-plugin-jsx-a11y
- **Cost:** Free

### mindrally/skills — accessibility-a11y
- **Source:** [skills.sh/mindrally/skills/accessibility-a11y](https://skills.sh/mindrally/skills/accessibility-a11y)
- **What it does:** WCAG 2.1 AA coding guidelines. ~1,000 weekly installs. Covers semantic HTML, ARIA patterns, keyboard nav, contrast, focus indicators, forms, reduced-motion/color-scheme.
- **Use for:** Guardrail reference
- **Key techniques worth adopting:**
  1. **`aria-current` coverage** — Explicitly covers `aria-current` for navigation state, which our skills don't mention. Important for SPAs and breadcrumbs.
- **MCP/API:** None
- **Cost:** Free

---

## Tier 3 — Domain-Specific or Narrow Skills

### Hack23/homepage — accessibility-wcag
- **Source:** [github.com/Hack23/homepage](https://github.com/Hack23/homepage)
- **What it does:** Embedded project-specific WCAG 2.1 AA rules with POUR structure. Detailed on time-based media (captions, audio descriptions, transcripts) and adaptable content.
- **Use for:** Content accessibility reference
- **Stealable:** Time-based media coverage (our skills are weak on video/audio a11y).

### jezweb/claude-skills — accessibility
- **Source:** [tessl.io/registry](https://tessl.io/registry/skills/github/jezweb/claude-skills/accessibility)
- **What it does:** Problem-triggered guidance (fires on "focus outline missing", "aria-label required", etc.)
- **Use for:** Trigger pattern reference
- **Stealable:** Symptom-oriented trigger design. Our skills trigger on task intent; adding symptom triggers could improve discoverability.

### supercent-io/skills-template — web-accessibility
- **Source:** [tessl.io/registry](https://tessl.io/registry/skills/github/supercent-io/skills-template/web-accessibility)
- **What it does:** WCAG 2.1 implementation guidelines. 12,654 installs, 88% quality score. Notable eval case: "Patient Intake Form for a Healthcare Portal."
- **Use for:** Eval fixture inspiration
- **Stealable:** Healthcare form as eval scenario — our eval suite lacks domain-specific healthcare/government form fixtures.

### haniakrim21/everything-claude-code — accessibility-wcag
- **Source:** [tessl.io/registry](https://tessl.io/registry/skills/github/haniakrim21/everything-claude-code/accessibility-wcag)
- **What it does:** Brief WCAG 2.2 reference. 95% impact rating on tessl.
- **Use for:** WCAG 2.2 verification
- **Stealable:** Nothing beyond confirming WCAG 2.2 as the standard to target.

### jeremylongshore/claude-code-plugins-plus-skills
- **Source:** [tessl.io/registry](https://tessl.io/registry/skills/github/jeremylongshore/claude-code-plugins-plus-skills/Scanning%20for%20Accessibility%20Issues)
- **What it does:** Plugin-dependent scanner using `a11y-scan` command.
- **Use for:** Architecture reference only
- **Stealable:** Nothing — validation errors in tessl, plugin dependency makes it fragile.

---

## Excluded Skills (evaluated, not relevant)

| Skill | Reason for exclusion |
|-------|---------------------|
| Generic "web quality" bundles without a11y depth | Don't add value beyond our existing coverage |
| Skills targeting only Lighthouse score optimization | Superficial — our skills target design decisions, not score gaming |
| Skills requiring paid services or proprietary APIs | Cost barrier; our skills are self-contained |

---

## Adoption Recommendations

### Incorporate into a11y-critic (prompt enhancements)

| Technique | Source | Priority | Effort |
|-----------|--------|----------|--------|
| Add WCAG 2.2-specific criteria checklist (9 new SC) | addyosmani, ehmo | **High** | Low — add to Phase 3 ARIA audit |
| Add "Needs user verification" flag for code-indeterminate items | ramzesenok | **High** | Low — extend Open Questions section |
| Add false-positive catalog for common jsx-a11y/axe FPs | airowe | **Medium** | Medium — curate list, add to realist check |
| Add text-in-UI-component contrast distinction | AccessLint | **Medium** | Low — add to visual review guidance |
| Add `aria-current` to navigation state checks | mindrally | **Low** | Trivial |
| Add APCA awareness as forward-looking note | meodai | **Low** | Trivial |

### Incorporate into a11y-planner (prompt enhancements)

| Technique | Source | Priority | Effort |
|-----------|--------|----------|--------|
| Add dynamic test prioritization based on risk profile | snapsynapse | **High** | Medium — redesign Phase 8 testing strategy |
| Add WCAG 2.2-specific planning criteria | addyosmani, ehmo | **High** | Low — extend Phases 3-7 |
| Add static analysis (jsx-a11y) as distinct testing layer | airowe | **Medium** | Low — add to Phase 8 |
| Add scale/sampling guidance for large sites | snapsynapse | **Medium** | Medium — new section in Phase 8 |
| Add time-based media planning section | Hack23 | **Medium** | Medium — new content type |
| Add contrast-first color composition approach | meodai | **Low** | Low — add to Phase 6 visual plan |
| Add `.visually-hidden` as canonical pattern reference | addyosmani | **Low** | Trivial |

### Consider as companion tools (not prompt changes)

| Tool | Source | Recommendation |
|------|--------|---------------|
| AccessLint MCP server (contrast calculation) | AccessLint | **Recommend** as optional MCP dependency for a11y-critic |
| axe-core scanning pipeline | snapsynapse, airowe | **Reference** in testing strategy, don't bundle |
| GitHub Actions CI workflow | snapsynapse | **Reference** as integration pattern |

### Do NOT adopt

| Technique | Reason |
|-----------|--------|
| Bundled scanning scripts (scan.js, discover.js) | Our skills are prompt-only; tooling belongs in separate repos |
| Code-fixing/refactoring capability | Our critic is deliberately read-only; fixes go through executor |
| Plugin architecture (.mcp.json) | Adds deployment complexity; our SKILL.md-only approach is simpler |
| iOS/SwiftUI-specific auditing | Out of scope — our skills target web |

---

## Composition Opportunities

### a11y-critic + AccessLint MCP
When reviewing color contrast, the critic could call `analyze_color_pair` for evidence-based findings instead of estimating ratios from hex values in source. This would make contrast findings verifiable.

### a11y-planner + snapsynapse discover pattern
For large-scale projects, the planner's testing strategy could recommend template-group sampling rather than testing every page. Reference snapsynapse's approach without bundling the tooling.

### a11y-critic + airowe dual-mode testing
The critic's testing strategy recommendations could explicitly separate static analysis (build-time, eslint-plugin-jsx-a11y) from runtime analysis (axe-core), noting that each catches different issue classes.
