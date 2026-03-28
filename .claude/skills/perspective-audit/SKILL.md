---
name: perspective-audit
description: "Deep accessibility review from 7 access perspectives — activated by escalation from a11y-planner or a11y-critic when one or more perspectives are flagged at MEDIUM or HIGH alarm level."
license: Apache-2.0
compatibility: Designed for Claude Code
metadata:
  author: zivtech
  version: "1.0.0"
disallowedTools:
  - Write
  - Edit
  - NotebookEdit
---

# Perspective Audit

Deep-layer accessibility review for perspectives escalated to MEDIUM or HIGH by the a11y-planner or a11y-critic. This skill reads the JTBD checklists only for the escalated perspectives, applies severity calibration, routes findings by ARRM role, and splits code-level findings from content-level flags.

This is Layer 2 in a hybrid accessibility architecture:
- **Layer 1**: a11y-planner and a11y-critic produce alarm levels (LOW / MEDIUM / HIGH) per perspective as lightweight hints.
- **Layer 2** (this skill): Runs the full JTBD checklist only for perspectives at MEDIUM or HIGH. Perspectives at LOW are not reviewed.

## When to Use

Invoke this skill when:
- a11y-planner or a11y-critic outputs a perspective alarm at **MEDIUM** or **HIGH**
- You need granular, per-perspective findings with WCAG citations and ARRM routing
- A design review surfaces concern about a specific access dimension (motion, contrast, auditory, cognitive) that warrants a dedicated checklist pass

Do not use this skill to review perspectives the planner/critic rated LOW. Evidence over assertion — this skill only fires where the risk signal exists.

## The 7 Perspectives

| # | Perspective | WCAG Criteria (AA) |
|---|---|---|
| 1 | Magnification & Reflow | 1.4.4, 1.4.10, 1.4.12, 1.4.13, 2.4.11 |
| 2 | Environmental Contrast | 1.3.3, 1.4.1, 1.4.3, 1.4.11 |
| 3 | Vestibular & Motion Sensitivity | 2.2.2, 2.3.1, 2.5.4 |
| 4 | Auditory Access | 1.2.1, 1.2.2, 1.2.3, 1.2.5, 1.4.2 |
| 5 | Keyboard & Motor Access | 1.3.4, 2.1.1, 2.1.2, 2.4.1, 2.4.3, 2.4.7, 2.4.13, 2.5.1, 2.5.2, 2.5.3, 2.5.7, 2.5.8 |
| 6 | Screen Reader & Semantic Structure | 1.1.1, 1.3.1, 1.3.2, 2.4.2, 2.4.4, 2.4.6, 3.1.1, 3.1.2, 3.3.1, 3.3.2, 4.1.2, 4.1.3 |
| 7 | Cognitive & Neurodivergent | 1.3.5, 2.2.1, 2.4.5, 3.2.1, 3.2.2, 3.2.3, 3.2.4, 3.2.6, 3.3.3, 3.3.4, 3.3.7, 3.3.8 |

## Severity Calibration

| Severity | When to Apply |
|---|---|
| CRITICAL | Blocks access entirely — keyboard trap, no captions on speech video, CAPTCHA with no alternative |
| MAJOR | Significant barrier for the perspective's user group — contrast below 3:1, motion without prefers-reduced-motion, missing error association |
| MINOR | Degrades experience but workaround exists — suboptimal label text, jargon defined nearby, help location slightly inconsistent |
| ENHANCEMENT | AAA criterion — report but do not escalate to MAJOR/CRITICAL regardless of implementation gap |

## Steps

### Step 1 — Confirm escalated perspectives

Read the planner or critic output to identify which perspectives are flagged MEDIUM or HIGH. List them explicitly before proceeding. If no escalation list is provided, ask: "Which perspectives did the planner or critic flag at MEDIUM or HIGH?"

Do not run checklists for perspectives at LOW.

### Step 2 — Read reference files

Read both reference files at invocation:

1. `.claude/skills/perspective-audit/references/perspectives.md` — Read **only the sections** for escalated perspectives. Do not load sections for LOW-rated perspectives.
2. `.claude/skills/perspective-audit/references/arrm-perspective-mapping.md` — Read in full for finding routing.

### Step 3 — Read the artifact under review

Read all source files relevant to the escalated perspectives. Understand the component structure, markup, CSS, and any JS handling state or interaction before running checklists.

### Step 4 — Run per-perspective checklists

For each escalated perspective:

1. Work through the JTBD checklist from `references/perspectives.md` item by item.
2. For each checklist item:
   - Mark PASS if the implementation satisfies the criterion with evidence (file:line or observed markup).
   - Mark FINDING if not satisfied — generate a finding using the format in Step 5.
   - Mark N/A if the criterion does not apply (e.g., no video present for Auditory Access caption checks).
3. Check all red flags listed for the perspective — any red flag that fires is automatically CRITICAL.
4. Separate code-level findings (enforceable from source) from content-level findings (require human verification).

### Step 5 — Format each finding

Use this format for every finding:

```
**Finding:** [clear description of what is wrong]
**WCAG:** [criterion number and name — e.g., 2.4.7 Focus Visible]
**Perspective:** [which perspective]
**Severity:** CRITICAL | MAJOR | MINOR | ENHANCEMENT
**Route to:** [ARRM primary role] (secondary: [role])
**Evidence:** [file:line citation or observed markup/CSS]
**Fix:** [specific recommended action]
```

Rules:
- Every finding must cite a WCAG criterion. No finding without a citation.
- AAA criteria are always ENHANCEMENT — never escalate them to MAJOR or CRITICAL.
- Content-level findings append: `[Human verification required — cannot be confirmed from source]`
- Code-level findings must include file:line evidence.

### Step 6 — Compile the summary

After all escalated perspectives are reviewed, output the combined summary:

```
## Perspective Audit Summary

**Component/artifact reviewed:** [name]
**Perspectives escalated for deep review:** [list]
**Perspectives at LOW (not reviewed):** [list]

### Findings by Severity

| Severity | Count |
|---|---|
| CRITICAL | N |
| MAJOR | N |
| MINOR | N |
| ENHANCEMENT | N |

### Perspectives That Passed

[List perspectives where all checklist items were PASS or N/A]

### Perspectives With Findings — Grouped by ARRM Role

**Front-End Dev**
- [Finding title] — [Perspective] — [Severity] — [WCAG criterion]

**Visual Design**
- [Finding title] — [Perspective] — [Severity] — [WCAG criterion]

**UX Design**
- [Finding title] — [Perspective] — [Severity] — [WCAG criterion]

**Content Author**
- [Finding title] — [Perspective] — [Severity] — [WCAG criterion]

### Open Questions Requiring Human Verification

[List all content-level findings that cannot be confirmed from source — caption accuracy, transcript completeness, audio description coverage, reading level, alt text quality for editorial images]

### Recommended Next Step

[One of: PASS (no CRITICAL/MAJOR findings), REVISE (MAJOR findings present — address before shipping), BLOCK (CRITICAL findings present — do not ship until resolved)]
```

## Companion Skills

- **a11y-planner**: Layer 1 upstream — produces alarm levels that trigger this skill.
- **a11y-critic**: Layer 1 upstream — produces alarm levels that trigger this skill. Also reviews design decisions post-implementation.
- **a11y-test**: Run after findings are addressed — verifies fixes with automated scans and keyboard tests.

## Reference Files

- `.claude/skills/perspective-audit/references/perspectives.md` — JTBD checklists, red flags, and evidence requirements for all 7 perspectives.
- `.claude/skills/perspective-audit/references/arrm-perspective-mapping.md` — ARRM role routing decision tree and finding output format.
