# VERDICT: ACCEPT-WITH-RESERVATIONS

(Critic stage output — a11y-critic, Opus. Captured verbatim for chain eval. The critic
emitted its own 6-perspective taxonomy, NOT the 7-perspective rubric taxonomy — see
PILOT-REPORT instrument findings.)

**Overall Assessment**: Strong, genuinely-engaged plan. Correctly identifies all eight real
defects in the source, maps each to the right APG pattern and WCAG criterion, enumerates
close-path branches, and pre-empts standard planner pitfalls. Not ready to implement verbatim
because of one concrete design error (proposed second focus ring is on the wrong side), one
double-announcement regression risk (success state gets both role="status" and a focus-moved
heading), and two unhandled interaction branches (Enter-to-submit through the trap, success
role="status" placement timing).

## Findings

### MAJOR 1 — Proposed second focus ring (box-shadow: 0 0 0 6px #fff) is on the wrong side.
Plan lines 310–311, 555. outline #1565c0 is invisible on the blue primary buttons (#1565c0 on
#1565c0 = 1.00:1). The white box-shadow renders OUTSIDE the outline, against the page — it does
not contrast the blue outline on its inner edge where needed. Fix: per-control two-tone ring,
e.g. box-shadow: 0 0 0 2px #fff, 0 0 0 5px #1565c0 (white abuts blue button = 5.75:1; blue abuts
page = 5.75:1). WCAG 2.4.7, 2.4.11. Confidence HIGH.

### MAJOR 2 — Success state specifies BOTH role="status" AND focus-move to success heading → double announcement.
Plan lines 233, 269, 278–279, 526–528. On submit, focus moves to the <h2> (announces heading +
dialog via swapped aria-labelledby) while <p role="status"> fires the body text — NVDA can
double-read. Plan asserts "both required" but never splits the content. Fix: focus the heading,
put role="status" on the body paragraph only, no duplicated text. WCAG 4.1.3, 4.1.2. Confidence MEDIUM.

### MAJOR 3 — Error summary missing tabindex="-1"; programmatic focus on validation failure silently no-ops.
Plan lines 290, 502, 507 vs success heading at 233/536. role="alert" div is not focusable;
summary.focus() no-ops, user stranded in the field. The plan applied tabindex="-1" to the
parallel success-heading case and forgot the error summary. Fix: add tabindex="-1" + DOM-verify
line; route Enter-submit through the same validate→focus-summary branch. WCAG 2.4.3, 3.3.1. Confidence HIGH.

### MINOR 1 — inert + aria-hidden="true" on same background element redundant; sequence inert-removal before focus-restore to avoid aria-hidden-on-focused-ancestor.
### MINOR 2 — Required-field indication inconsistent (* + legend vs the plan's no-fieldset decision). Use "(required)" in labels.
### MINOR 3 — Specify inputEl.validity.valid / typeMismatch over a hand-rolled email regex (matches project's prefer-battle-tested rule).

### What's Missing
1. tabindex="-1" on error summary (Major 3). 2. Success announcement content split (Major 2).
3. close/inert sequencing (Minor 1). 4. unused useEffect import note (trivial). 5. re-open state
reset dependency (modal unmounts on close — state resets automatic; state it explicitly).
6. aria-describedby removed (not ="") when valid.

## Perspective Alarm Levels (critic's 6-perspective taxonomy)

| Perspective | Alarm | Rationale |
|---|---|---|
| Screen reader | MEDIUM | Major 2 (double-announce) + Major 3 (error-summary focus no-op) both SR-facing. |
| Keyboard-only | MEDIUM | Enter-submit→focus-summary path fails without tabindex=-1; trap/validation render half-specified. |
| Low vision | MEDIUM | Headline focus-ring fix (Major 1) geometrically wrong on the two primary blue buttons. |
| Voice control | LOW | Every control has a programmatic spoken-matchable name; title barred. |
| Switch access | LOW | Focus order + trap + restoration well-designed; only residual is Major 3 (same root cause). |
| Cognitive | LOW | Specific error messages, clear success confirmation, no timeouts. |

**Escalation recommendation (critic's prose)**: "Three perspectives at MEDIUM... This does NOT
require a separate perspective-audit escalation — the MEDIUM alarms collapse to the three Majors
above. Re-running perspective-audit would re-derive the same three. Fix the Majors and all three
drop to LOW."

[ORCHESTRATOR NOTE — chain finding: this prose recommendation CONTRADICTS the structured MEDIUM
alarms. Per SKILL.md Step 4 and the team escalation table, any MEDIUM/HIGH alarm mechanically
triggers the audit. Escalation fired on the mechanical rule. The prose-vs-structured conflict is
recorded as a chain finding in PILOT-REPORT.]

## Verdict Justification
ACCEPT-WITH-RESERVATIONS not REVISE: architecture correct and complete; the three Majors are
specification gaps within otherwise-correct tasks, fixable with targeted edits to Tasks 5/6/7.
Major 1 considered for CRITICAL, downgraded (ring visible on secondary button + inputs; degrades,
doesn't block). Major 3 held at MAJOR (announce-without-move fails the plan's own acceptance
criterion line 366).

## Open Questions
1. Is prefers-reduced-motion truly out of scope (no entrance animation in same PR)?
2. Portal vs sibling rendering — changes the inert target; unresolved.
3. Does the success state's Escape listener survive the form→success render swap?

Files reviewed: docs/a11y-plans/2026-06-13-subscribe-modal-a11y-plan.md;
evals/suites/chain/targets/modal-broken-focus-trap/component.jsx; styles.css.
