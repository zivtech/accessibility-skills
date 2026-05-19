# Phase 4: Real Component Validation Results

**Date:** 2026-05-19
**Component:** MobileMenu.js (client digital law library, 497 lines)
**Goal:** Validate a11y-workflow end-to-end on a real production component

---

## Workflow Machinery Validation

| Goal | Status | Evidence |
|------|--------|----------|
| `a11y-scout` resolves via `subagent_type` | PASS | Haiku scout ran in ~20s after session restart, produced structured recon |
| Planner writes to `docs/a11y-plans/` | PASS | 1181-line plan at `2026-05-19-mobile-menu-a11y-plan.md` |
| Critic reads plan + source | PASS | Read 7 source files, REVISE verdict with evidence-backed findings |
| Perspective audit triggers on MEDIUM | PASS | Escalated for Screen Reader + Keyboard, produced 4 MAJOR + 3 MINOR |
| End-to-end coherence | PASS | Each agent built on previous, no contradictions, findings accumulated |

## Agent Performance

### Scout (Haiku, ~20s)
- Identified component type: Mobile navigation + embedded bookmark dialog
- APG pattern: Disclosure + Toggle Button + Modal Dialog (corrected from "Menu Button")
- Inventoried 19 ARIA attributes with line numbers
- Flagged 9 areas for reviewer attention
- Output: ~1400 chars (under 1500 budget)

### Planner (Opus, ~10 min)
- Produced 17 implementation tasks across 4 APG patterns
- Correctly identified 2 open product decisions requiring stakeholder input
- Designed focus management plan with 6 focus scenarios
- Added state communication table with 11 state/ARIA mappings
- Included 6 critic review checkpoints
- One design error: blanket focus restoration on menu close (caught by critic)

### Critic (Opus, ~5 min)
- Read plan file + 6 additional source files (chapter.js, chapterMenuNvigation.js, index.js, App.scss)
- Found 1 critical regression (focus restoration races chapter navigation)
- Found 2 major issues (aria-haspopup mismatch, fullscreen double-announcement)
- Resolved 2 open investigations from plan (CSS display:none, error role="alert")
- Perspective alarms: Screen Reader MEDIUM, Keyboard MEDIUM, all others LOW

### Perspective Audit (Opus, ~6 min)
- Reviewed 7 source files including bookContent.js (not read by critic)
- Confirmed critic's findings with additional detail (traced 4-step focus chain)
- Found 1 new MAJOR: dialog renders inside <nav> landmark after plan Task 1
- Proposed concrete fixes: React.createPortal for dialog, CustomEvent.detail for close reason
- Total: 4 MAJOR, 3 MINOR findings

## Finding Accumulation Chain

| Finding | Discovered By | Missed By |
|---------|--------------|-----------|
| Focus restoration races chapter nav | Critic | Planner |
| aria-haspopup on anonymous bookmark | Critic | Planner |
| Fullscreen double-announcement | Critic | Planner |
| Tasks 15/17 already resolved in code | Critic | Planner |
| Dialog inside <nav> landmark | Perspective Audit | Planner, Critic |
| Touch targets need implementation | Perspective Audit | Planner (left as verify) |
| aria-current="page" vs aria-pressed | Perspective Audit | Planner, Critic |

## Model Routing Validation

| Agent | Model | Justified? | Evidence |
|-------|-------|-----------|----------|
| Scout | Haiku | Yes | Recon task, accurate in ~20s, no judgment needed |
| Planner | Opus | Yes | 17-task plan with APG pattern analysis, open decisions surfaced |
| Critic | Opus | Yes | Found regression by tracing cross-file event dispatch |
| Perspective Audit | Opus | Yes | Traced 4-step focus chain across 4 files, found finding critic missed |

## Required Plan Amendments (from Critic + Perspective Audit)

1. **Task 3**: Differentiate close sources — only restore focus on user-initiated close, not chapter-navigation close
2. **Task 10**: Conditional `aria-haspopup` — remove for anonymous users
3. **Task 1 + 4**: React.createPortal for bookmark dialog outside `<nav>` landmark
4. **Task 16**: Promote from verification to implementation (44x44 touch targets)
5. **Task 15**: Retire investigation — CSS `display: none` confirmed
6. **Task 17**: Retire investigation — `role="alert"` confirmed at `index.js:148`
7. **Task 11**: Drop fullscreen status region announcement (aria-pressed sufficient)

## Spot-Check: Cross-File Claims Verified

The critic and perspective auditor made specific claims about code in files they read independently. Three foundation claims were spot-checked against the actual source:

| Claim | Cited Location | Verified? |
|-------|---------------|-----------|
| `closeMobileMenu` dispatched on chapter select | chapter.js:55 | YES — exact line, Defect 24784 comment |
| `role="alert"` on error rendering | index.js:148 | YES — with `position: fixed`, `zIndex: 1050` |
| `display: none` on nav `> ul` per Defect 24791 | App.scss:1360-1363 | YES — exact lines and comment |

## Conclusion

The a11y-workflow team architecture works as designed on a real production component. The sequential scout→planner→critic→perspective-audit chain produced findings that accumulated — each agent caught issues the previous agents missed, and no agent contradicted a previous agent's correct findings. Cross-file claims were spot-checked and confirmed accurate. The perspective audit justified its existence by catching a MAJOR landmark semantics issue (dialog inside `<nav>`) that both planner and critic missed.

## Next Step

**Phase 5: Generalize the team pattern.** Create domain team templates for React and Drupal review workflows. Each domain needs its own benchmark data before model routing can be specified — the a11y benchmarks cannot be assumed to transfer. Alternatively, continue with MobileMenu implementation by amending the plan per the 7 required amendments and running the implement→test→critique cycle.
