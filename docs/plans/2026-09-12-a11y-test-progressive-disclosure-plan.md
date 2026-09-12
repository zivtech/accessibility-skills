# Plan: a11y-test SKILL.md progressive disclosure

**Date:** 2026-09-12
**Goal:** Shrink the always-loaded `a11y-test/SKILL.md` (the repo's single largest interactive-session read cost) by moving mode-specific and historical prose to `references/` files loaded on demand, while keeping the load-bearing routing/decision content inline. Behavior-preserving refactor — no rule changes.

## Why

A structural map (2026-09-12) found **~85% of the ~94KB file is movable**: only ~13KB is needed on every invocation (routing table, evidence-class contract, the two detector cautions, context-discipline rule, sequencing table). The rest is per-tool setup, worked examples, dated calibration receipts, and APG templates a session needs only when it enters that mode.

## Constraints (verified)

- `a11y-test` is in the byte-identical **mirror set** (`.claude` ↔ `.agents`) — SKILL.md and every `references/` file must match byte-for-byte.
- `a11y-test` is **not** in the agent-def drift set (no protocol-marker cross-check) and **not** hash-pinned in any run-manifest — so no drift refresh, no manifest refresh.
- Cross-refs are plain-text "see … below", not anchors — every move must rewrite its pointer or the routing table dead-ends.

## Stages

### Stage 1a — DONE (this PR)
Three clean, whole-section, self-contained mode guides → new reference files, pointer stubs left in place, routing cross-refs rewritten:
- `## Test script generation with Webwright` → `references/webwright-testgen.md`
- `## Component screen-reader assertions with virtual-screen-reader` → `references/vsr-testing.md`
- `## 2. Visual Regression Tests (REQUIRED)` → `references/visual-regression-testing.md`

Result: SKILL.md 93,269 → 76,754 chars (17,215 moved). `check_mirrors --strict`, `lint_skills`, `check_client_refs` green; moved content verified verbatim in refs.

### Stage 1b — DONE (this PR)
The APG keyboard-test-patterns block → `references/keyboard-test-patterns.md`. Keep-parent/move-children: `## 1. Keyboard Accessibility Tests` + its MANDATORY real-keyboard-events caution stay inline; the ### children (required method, 12 APG widget templates, SPA patterns, CSS anti-patterns, ARIA supplement) moved (14,501 chars). Fixed 4 APG-template cross-refs — 3 in SKILL.md plus the dangling "below" that Stage 1a left inside `webwright-testgen.md`.

Result: SKILL.md 76,754 → 62,637 chars. Combined Stage 1a+1b: **93,269 → 62,637 (~33% off)**. All validators green.

### Stage 2 — own PR, higher care (deferred; the 6 flagged risks live here)
- Retest classification / operation-evidence admissibility / disposition block → `references/retest-and-admissibility.md`.
- agent-browser recon + keyboard-a11y-tester guide → resolve the **bidirectional keyboard-driving reference** first (keep one canonical copy in the CORE layer; both refs point to it).
- Baseline URL-list scan → carry the **cross-cutting collector-safety rule** with an inline pointer so agent-browser recon still sees it.
- Media/SR protocol, axe-core scanning → resolve **double-booked §-numbers** (make Test Execution Order the single numbering source; convert in-body §N to file-relative names).
- The **A11y Evidence Finding contract** stays inline (or moves only with coordinated edits) — `a11y-critic` Phase 0 and `bug-reporting` depend on it (cross-skill fan-out).
- ICT crosswalk gate: keep the gate sentence and its enforcement bullets physically adjacent.

## Validation gate (every stage)
`check_mirrors.py --strict`, `lint_skills.py`, `check_client_refs.py`, verbatim spot-check of moved content, and a routing-integrity check (no dangling "see … below", every stub links a real ref file).
