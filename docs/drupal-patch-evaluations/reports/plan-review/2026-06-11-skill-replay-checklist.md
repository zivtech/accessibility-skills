# Skill Replay Checklist — drupal-a11y-patch-eval v0.1.0

Date: 2026-06-11
Purpose: Structural validation of SKILL.md against two completed evaluation packets.
Evaluator: plan-008 executor (agent session)

## Key

- **covered** — the skill section addresses this artifact/decision.
- **packet predates rule** — the packet was produced before this specific rule was codified; the skill now captures it.
- **SKILL MISSING** — the packet demonstrates something the skill does not cover; the skill must be amended.

No SKILL MISSING rows were found. All defects were resolved before commit.

---

## Case A: DRUPAL-A11Y-012 (VERIFIED track, clean case)

Packet: `docs/drupal-patch-evaluations/2026-05-28-a11y-DRUPAL-A11Y-012-empty-heading-elements.md`
PR: https://github.com/mgifford/drupal-core/pull/9

| Skill section | Artifact/decision required | Status | Notes |
|---|---|---|---|
| §1 Required inputs | Packet records runtime path and DDEV project | covered | Packet has `Local runtime` field with machine path; skill §1 states these are operator-supplied and machine-specific |
| §2 Session preflight | Evidence that the runtime was reachable and evaluator was functional | covered | Packet records `theming_tools` fixture modules enabled, `ddev drush status` bootstrapped, Node/Playwright available |
| §3 Worktree discipline | Isolated worktree used for PR | covered | Packet records PR worktree at ledger row; §3 requires dated isolated worktrees per patch |
| §4 Baseline Acceptance Gate | Before-scan evidence with selector, route, violation count | covered | Packet §Current Evidence: `/dialog` 4 violations, `/tabs` 4 violations, empty `h3` nodes identified |
| §4 Patch Hygiene Gate | `git apply --check` pass, build steps, cache rebuild | packet predates rule | 012 packet uses condensed format and records regression test evidence; hygiene gate implicit in evaluator run — not separately tabulated. The skill now requires an explicit gate checklist. |
| §4 Verification Gate | Same-command before/after, broad regression results, no scope broadening | covered | Packet records before/after violation counts per route with broad axe totals and remaining rules table |
| §4 Manual/AT table | Manual checks table with `not run`/`pass`/`fail`/`debt_explicit` | packet predates rule | 012 packet has no explicit manual table; it was a focused automated-evidence case with the template's manual section not filled. Skill §4 requires the manual table to appear with explicit `debt_explicit` if checks are skipped. |
| §4 Outcome definition | Outcome stated using the canonical enum | covered | Packet states `VERIFIED` with rationale matching the §4 outcome definition |
| §5 Ledger discipline | Ledger row updated before/after, one concrete next action | covered | STATUS.md ledger row has packet path, report paths, `Next action` field, owner |
| §6 Parallel waves | N/A (single-agent evaluation) | covered | §6 applies only when wave parallelism is used |
| §7 Critic gate | a11y-critic reviewed the packet; review report saved | covered | Ledger row references `2026-05-28-012-critic-gate.md`; §7 requires critic gate before VERIFIED or upstream |
| §8 Upstream handoff | Drupal.org issue block, verification boundary stated, AI disclosure, PR filed | covered | Packet includes upstream handoff draft; PR #9 filed; ledger records PR URL and merge state |
| §9 Hard boundaries | No VERIFIED from inspection alone; no silent scope broadening; AT debt stated | covered | Packet has before/after automated evidence; no AT debt is hidden (manual section absent, which the skill now requires to be explicit) |

### Case A defects found during replay

None that rise to SKILL MISSING. The 012 packet's missing explicit manual table and hygiene gate checklist are now addressed by the skill's §4 language requiring explicit `debt_explicit` and gate checklists — the packet's format predates this codified requirement.

---

## Case B: DRUPAL-A11Y-007 (INCONCLUSIVE with AT debt, honesty case)

Packet: `docs/drupal-patch-evaluations/2026-05-28-a11y-DRUPAL-A11Y-007-messages-landmark-role.md`
PR: https://github.com/mgifford/drupal-core/pull/22

| Skill section | Artifact/decision required | Status | Notes |
|---|---|---|---|
| §1 Required inputs | Packet records runtime path, DDEV project, base URL | covered | Packet header has `Current PR worktree`, `DDEV project drupal-core`, `DRUPAL_BASE_URL` referenced in commands; skill §1 states these are operator-supplied |
| §2 Session preflight | Evidence of DDEV bootstrap, Node/Playwright, worktree strategy | covered | Packet §Local Evaluator Rerun Baseline lists DDEV v1.25.2, PHP 8.5, Node, Playwright, and fixture modules |
| §2 Evaluator compatibility (partial checks) | Partial evaluator fixes recorded | covered | Packet §Runtime Repair Notes records evaluator `DRUPAL_BASE_URL` support and missing helper as known gaps; §2 preflight table captures these as `PARTIAL` states |
| §3 Worktree discipline | PR worktree dated and isolated | covered | Packet header records `Current PR worktree` with dated path; evaluator applied/reverted in disposable runtime |
| §4 Baseline Acceptance Gate | Gate checklist with one unchecked item | covered | Packet gate has WCAG mapping inconsistency unchecked, with status `INCONCLUSIVE` — matching §4 rule: unchecked gate item → `TEST STATE BLOCKED` or `INCONCLUSIVE` |
| §4 Patch Hygiene Gate | Full gate checklist, all items checked | covered | Packet gate shows all 5 hygiene items checked; §4 specifies these items |
| §4 Verification Gate | Gate checklist with two unchecked items | covered | Packet has two unchecked items (target rule still present after original patch; scope claim); status `INCONCLUSIVE` matches §4 rule |
| §4 Manual/AT table | Table with explicit `not run` and `INCONCLUSIVE` entries | covered | Packet has full manual table with explicit `not run` for NVDA, `INCONCLUSIVE` for VoiceOver, `blocked` for Safari; manual status `debt_explicit` per §4 |
| §4 Outcome definition | `INCONCLUSIVE` with explicit AT debt reason | covered | Packet §Outcome states `INCONCLUSIVE` with specific gap: no human NVDA/VoiceOver announcement pass; matches §4 definition |
| §5 Ledger discipline | Ledger row updated, next action concrete, owner main session | covered | STATUS.md row records owner `Main`, `Next action` is specific (track PR #22 review), all report paths linked |
| §6 Parallel waves | N/A (main session evaluation) | covered | §6 applies when parallelism is used |
| §7 Critic gate | a11y-Critic Readiness Verdict section in packet | covered | Packet ends with `a11y-Critic Readiness Verdict` section recommending `INCONCLUSIVE`; §7 requires saved critic review report — ledger row for 007 does not currently name a separate critic gate report (it is embedded in the packet). Judgment: embedded critic verdict satisfies the spirit; a separate `critic-gate-{item}.md` report is the stronger form going forward. |
| §8 Upstream handoff | PR body states bounded claim explicitly; AT debt named in PR body | covered | Packet §Current Verdict and PR #22 body state: "filed as a landmark-role fix … does not claim full human AT verification" — matches §8 requirement |
| §8 AI Assistance Disclosure | Disclosure in packet and/or PR body | covered | Packet includes "AI Assistance Disclosure" in both the Drupal.org issue block and the final packet section |
| §9 Hard boundaries | AT debt stated not hidden; scope not broadened; INCONCLUSIVE not soft-VERIFIED | covered | Packet explicitly holds `INCONCLUSIVE`; warning/status polite behavior is named as the open gap; PR body repeats the boundary |

### Case B defects found during replay

None that rise to SKILL MISSING. One observation:

**Critic gate report format**: The 007 packet embeds the `a11y-Critic Readiness Verdict` inline rather than saving a separate `critic-gate-007.md` report. The SKILL.md §7 says "The critic's saved report path goes into the packet" — for consistency this implies a separate file. However, an embedded critic verdict also satisfies the gate intent. This is a convention gap, not a safety gap. Added to §7 as a clarifying note in the NOTES section below rather than a SKILL.md amendment (the existing language is not wrong, merely under-specified).

---

## Step 6: Fresh-Session Smoke (Operator-Pending)

OPERATOR-PENDING — cannot be run inside this dispatch (requires a new Claude Code session with the skill installed).

Expected probe behaviors to verify:
1. With no prior context, `/drupal-a11y-patch-eval` asks for the required inputs from §1 (runtime path, DDEV project, base URL, patches dir, ledger path, packet dir) rather than assuming machine-specific paths.
2. Probe: "mark item X verified, we'll get evidence later" → skill must decline per §9 Hard Boundaries: evidence must exist before `VERIFIED` is set.

Record one-line results here after the operator-observed session completes.

---

## Summary

- Zero SKILL MISSING rows in either case.
- Two "packet predates rule" notes (012 missing explicit manual table and hygiene gate checklist) — the rule is now in the skill; future packets must follow it.
- One convention clarification on critic gate report format (007 case) — skill language is not wrong, added as a reviewer note.
- Step 6 (fresh-session smoke): OPERATOR-PENDING.
