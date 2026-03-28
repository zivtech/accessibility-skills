# Perspective Agents — Skill Profile

## Overview

**Skills Under Test:** a11y-planner (enhanced), a11y-critic (enhanced), a11y-test (enhanced), perspective-audit (new)

**Model:** claude-opus-4-6

**Architecture:** Hybrid with progressive escalation

**Focus:** Whether adding 7 explicit access perspectives improves finding coverage in under-covered dimensions (auditory, vestibular, cognitive, contrast) without regressing in existing-strength dimensions (keyboard, screen reader, ARIA)

## The Hybrid Architecture

### Layer 1 — Lightweight Perspective Hints

The planner and critic include 2-3 line perspective hints in their existing phases. These produce alarm levels (LOW / MEDIUM / HIGH) per perspective at the end of the review:

- **LOW:** This perspective's concerns are minimal for this component
- **MEDIUM:** Some concerns exist; the review should note them but deep audit is optional
- **HIGH:** Significant concerns; deep perspective audit recommended

### Layer 2 — Perspective Audit Companion

The `perspective-audit` skill runs the full JTBD checklist only for perspectives escalated to MEDIUM or HIGH. It reads structured checklists from `references/perspectives.md`, applies severity calibration, routes findings by W3C WAI ARRM role, and separates code-level findings from content-level flags.

## The 7 Perspectives

| # | Perspective | Primary AT/Mechanism | WCAG Criteria (AA) |
|---|---|---|---|
| 1 | Magnification & Reflow | Browser zoom, screen magnifier | 1.4.4, 1.4.10, 1.4.12, 1.4.13, 2.4.11 |
| 2 | Environmental Contrast | High-contrast mode, brightness | 1.3.3, 1.4.1, 1.4.3, 1.4.11 |
| 3 | Vestibular & Motion | prefers-reduced-motion | 2.2.2, 2.3.1, 2.5.4 |
| 4 | Auditory Access | Captions, transcripts, visual alerts | 1.2.1, 1.2.2, 1.2.3, 1.2.5, 1.4.2 |
| 5 | Keyboard & Motor | Keyboard, switch, voice control | 1.3.4, 2.1.1, 2.1.2, 2.4.1, 2.4.3, 2.4.7, 2.4.13, 2.5.1-3, 2.5.7, 2.5.8 |
| 6 | Screen Reader & Semantic | NVDA, JAWS, VoiceOver | 1.1.1, 1.3.1, 1.3.2, 2.4.2, 2.4.4, 2.4.6, 3.1.1-2, 3.3.1-2, 4.1.2-3 |
| 7 | Cognitive & Neurodivergent | Plain language, consistent UI | 1.3.5, 2.2.1, 2.4.5, 3.2.1-4, 3.2.6, 3.3.3-4, 3.3.7-8 |

52 WCAG 2.2 AA criteria covered with one primary owner per criterion.

## Key Differentiators Being Tested

1. **New-dimension coverage:** Auditory, vestibular, cognitive, and contrast findings that the current skills miss or undercover
2. **Structured JTBD approach vs named dimensions:** Does the checklist protocol outperform simply telling the model "also check for X"?
3. **Progressive escalation accuracy:** Do alarm levels correctly identify which perspectives need deep review?
4. **No regression in strength areas:** Keyboard, screen reader, and ARIA review quality maintained
5. **False positive control:** Adding perspectives should not cause over-flagging on clean components

## Output Format

### Planner/Critic Enhanced Output

After the standard review, the enhanced skills append:

```
### Perspective Alarm Levels

| Perspective | Alarm | Rationale |
|---|---|---|
| Magnification & Reflow | LOW | Static content, no hover interactions |
| Environmental Contrast | MEDIUM | Color-coded status indicators present |
| ... | ... | ... |
```

### Perspective Audit Output

```
## Perspective Audit Summary

**Perspectives escalated:** [list]
**Perspectives at LOW (not reviewed):** [list]

### Findings by Severity
| Severity | Count |
|---|---|
| CRITICAL | N |
| ... | ... |

### Perspectives With Findings — Grouped by ARRM Role
...
```

## Anti-Patterns to Avoid

- **Over-escalation:** Flagging all perspectives as HIGH for every component
- **Under-escalation:** Never triggering perspective audit (defeats the purpose)
- **Regression:** Missing keyboard/screen reader issues because focus shifted to new perspectives
- **Manufactured findings:** Inventing vestibular concerns for a static text page
- **Ignoring the N/A case:** A text-only page should mark most Auditory checklist items N/A, not PASS
