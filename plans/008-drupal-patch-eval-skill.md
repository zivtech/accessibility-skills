# Plan 008: Productize the Drupal a11y patch-evaluation loop as an installable skill

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. This plan AUTHORS A PROMPT ARTIFACT (a SKILL.md)
> from existing protocol documents — it does not run Drupal, DDEV, or any
> patch evaluation. When done, update the status row for this plan in
> `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat de0031f..HEAD -- templates/drupal-a11y-patch-evaluation-template.md docs/drupal-patch-evaluations/STATUS.md docs/plans/2026-05-28-drupal-all-items-evaluation-plan.md .claude/skills/`
> The template and STATUS.md are living workstream files — if they changed,
> read the CURRENT versions and extract from those; the protocol content
> wins over this plan's excerpts. Only STOP if the files are gone or the
> rule sections named below no longer exist.

## Status

- **Priority**: P2
- **Effort**: M (prompt authoring + replay validation; no environment execution)
- **Risk**: LOW (new files only; no existing behavior changes)
- **Depends on**: none (soft: plan 004's `.agents/skills/README.md` for the absent-list note — fallback included)
- **Category**: direction (dx)
- **Planned at**: commit `de0031f`, 2026-06-11

## Why this matters

The Drupal core accessibility patch-evaluation workstream is this repo's most active surface (the last 30 commits are its ledger updates; 15 upstream PRs filed to `mgifford/drupal-core`, #8–#22). Its protocol is real and battle-tested but lives in three places a newcomer must reverse-engineer: the packet template, the STATUS.md rule sections, and two operating-model plan docs — plus session-handoff reports. Today only one person (plus their agent sessions) can run it. Encoding it as a skill makes the loop reproducible by a second contributor (Mike Gifford is the obvious candidate) and by fresh agent sessions without re-reading the whole ledger. The protocol already exists — this plan is extraction and packaging, not invention. The validation is a structural replay against a completed packet, not a live Drupal run.

## Current state

Verified at commit `de0031f` — these are the source documents to extract from:

- `templates/drupal-a11y-patch-evaluation-template.md` (229 lines) — the packet contract:
  - Packet Header with two status axes: **Local status** enum (`NOT STARTED`, `DRAFT`, `BASELINE VERIFIED`, `PATCH HYGIENE BLOCKED`, `TEST STATE BLOCKED`, `INCONCLUSIVE`, `NEEDS PATCH`, `FAILED`, `VERIFIED`, `OBSOLETE`) and **Manual status** (`not_run`, `debt_explicit`, `complete`) (lines 5–20).
  - Four evidence gates, each with an explicit blocked-status rule: Baseline Acceptance Gate (lines 62–70: "If any item is unchecked, status must be `TEST STATE BLOCKED` or `INCONCLUSIVE`, not `VERIFIED`"), Patch Hygiene Gate (96–104), Verification Gate (135–142), Manual/Perspective table (144–157: "Do not mark the packet `VERIFIED` unless every required manual check has a recorded result").
  - Outcome definitions (159–169), Root Cause/Fix narrative, Drupal.org issue block with AI Assistance Disclosure (221–223), and the a11y-meta-skills review checklist (225–229: a11y-test measured, a11y-critic reviewed the packet, perspective-audit escalated when perspective-sensitive).
- `docs/drupal-patch-evaluations/STATUS.md` — the operating rules:
  - **Drift Rules** (lines 7–19): one owner per row; `VERIFIED` requires baseline + after-patch + broad-regression + manual checks under the same conditions; recheck patch hygiene against current raw patch; one concrete `Next action`; main agent owns the ledger; subagents never co-edit a packet; ledger updated after every wave; source status ≠ local status.
  - **Parallel Wave Rules** (27–37): wave size 4–6, one item per subagent, separate packet files per owner, shared files main-agent-only, **critic gate on any packet a subagent recommends as `VERIFIED` or upstream-ready**, reports under `reports/{wave}/{item}-{run-id}.md`.
  - **Global Environment Preflight** table (38–50): DDEV runtime reachable, Node/Yarn, Playwright browsers, worktree strategy, evaluator base-URL/helper/rule-ID compatibility, SHA pinning.
  - Machine-specific facts that must NOT be baked into the skill: worktree paths under `/Users/AlexUA_1/claude/.cache/drupal-a11y-eval/…`, DDEV project name `drupal-core`, port `33000`.
- `docs/plans/2026-05-28-drupal-all-items-evaluation-plan.md#parallel-subagent-operating-model` — STATUS.md names it the canonical parallel model (STATUS.md:5). Read that section when drafting the skill's wave protocol.
- Skill conventions in this repo (frontmatter): `name`, `description`, `license: Apache-2.0`, `compatibility:`, `metadata: {author: zivtech, version}` — see `.claude/skills/a11y-planner/SKILL.md:1-9`. perspective-audit additionally uses `disallowedTools` — NOT applicable here (this skill writes packets and the ledger).
- Completed-packet exemplars for the replay test: `docs/drupal-patch-evaluations/2026-05-28-a11y-DRUPAL-A11Y-012-empty-heading-elements.md` (VERIFIED-track, PR #9) and `2026-05-28-a11y-DRUPAL-A11Y-007-messages-landmark-role.md` (INCONCLUSIVE with explicit AT debt — the honesty case).
- If plan 004 has run, `.agents/skills/README.md` exists with an "intentionally absent" list.

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Frontmatter parses | step 4 snippet | `frontmatter ok` |
| No machine paths leaked | `grep -rn "AlexUA_1\|/Users/" .claude/skills/drupal-a11y-patch-eval/` | no matches |
| Replay checklist | step 5 manual diff | every template section accounted for |
| Mirror checker still green | `python3 scripts/check_mirrors.py` (if plan 001 ran) | exit 0 |

## Scope

**In scope**:
- `.claude/skills/drupal-a11y-patch-eval/SKILL.md` (create)
- `.claude/skills/drupal-a11y-patch-eval/references/packet-template.md` (create — copy of the template, see step 2)
- `docs/drupal-patch-evaluations/STATUS.md` (ONE added line in the header area pointing at the skill — nothing else)
- `.agents/skills/README.md` (one line in the intentionally-absent list IF the file exists; otherwise skip silently)

**Out of scope** (do NOT touch):
- `templates/drupal-a11y-patch-evaluation-template.md` — stays where workstream docs reference it; the skill gets a copy, not a move.
- STATUS.md ledger rows, packets, reports, patches — live workstream state.
- Running ANY evaluation, DDEV command, or git operation against Drupal worktrees.
- A Codex mirror of this skill (it orchestrates Claude Code subagents and local DDEV state; document as intentionally absent).

## Git workflow

- Branch: `advisor/008-drupal-patch-eval-skill`
- Conventional commits, e.g. `feat: add drupal-a11y-patch-eval skill`.
- Do NOT push or open a PR unless the operator instructed it.

## Steps

### Step 1: Re-read the three source documents end-to-end

`templates/drupal-a11y-patch-evaluation-template.md`, `docs/drupal-patch-evaluations/STATUS.md` (at minimum: Drift Rules, status enum, Parallel Wave Rules, Global Environment Preflight, and 2–3 recent Parallel Review Log rows for flavor), and the `#parallel-subagent-operating-model` section of `docs/plans/2026-05-28-drupal-all-items-evaluation-plan.md`. Also read both exemplar packets named above. Take notes mapping each rule to the skill section that will carry it — the skill must not invent rules that aren't in the sources, and must not drop the load-bearing ones (the gate→status rules and the critic gate are load-bearing).

**Verify**: your notes list ≥ 12 extracted rules each tagged with its source line. (This is the named human-checkable artifact for the reviewer; include it in the PR description or as a comment block at the bottom of the SKILL.md PR.)

### Step 2: Copy the packet template into the skill's references

`cp templates/drupal-a11y-patch-evaluation-template.md .claude/skills/drupal-a11y-patch-eval/references/packet-template.md` and add an HTML comment at the top of the COPY: `<!-- Synced copy of templates/drupal-a11y-patch-evaluation-template.md — if you change one, change both. -->` Add the same comment (pointing the other way) to the original? NO — out of scope; the one-way note in the copy is enough, the maintenance note records the rest.

**Verify**: `diff <(tail -n +2 .claude/skills/drupal-a11y-patch-eval/references/packet-template.md) templates/drupal-a11y-patch-evaluation-template.md` → empty (identical except the added first line).

### Step 3: Author the SKILL.md

`.claude/skills/drupal-a11y-patch-eval/SKILL.md` with frontmatter:

```yaml
---
name: drupal-a11y-patch-eval
description: "Evaluate a Drupal accessibility patch end-to-end: baseline evidence, patch hygiene, after-patch verification, manual/AT checks, critic gate, and upstream handoff. Evidence-gated — never VERIFIED without before/after proof under the same conditions."
license: Apache-2.0
compatibility: Claude Code only — orchestrates subagents, DDEV, and local worktrees
metadata:
  author: zivtech
  version: "0.1.0"
---
```

Body sections, in order (content extracted from step 1's notes — write in the imperative voice of the existing skills):

1. **When to use / inputs.** Required inputs the operator supplies per session — never hardcoded: runtime repo path, DDEV project name, base URL, patches directory, ledger path (default `docs/drupal-patch-evaluations/STATUS.md`), packet directory. State plainly: paths in the ledger are machine-specific; the skill parameterizes them.
2. **Session preflight.** The Global Environment Preflight table (generalized from STATUS.md:38-50): runtime reachable, Node/Yarn, Playwright browsers, worktree strategy settled, evaluator compatibility. Rule: if global preflight fails, only read-only source/provenance work proceeds; item statuses do not change.
3. **Worktree discipline.** Dated, isolated worktrees branched from fresh `origin/main` for every patch (`git worktree add -b <name>-<YYYYMMDD> <path>-<YYYYMMDD> origin/main`); never apply patches to the runtime main worktree.
4. **The packet lifecycle.** One packet per patch+issue from `references/packet-template.md`. Reproduce the four gates and their blocked-status consequences VERBATIM in spirit: unchecked baseline gate → `TEST STATE BLOCKED`/`INCONCLUSIVE`; unchecked hygiene gate → `PATCH HYGIENE BLOCKED`; manual checks unrecorded → manual status `debt_explicit`, never `VERIFIED`. Include the full local-status enum and the source-status-vs-local-status separation rule.
5. **Ledger discipline.** Drift Rules from STATUS.md:7-19, generalized: one owner per row, ledger before/after every session, one concrete next action, main session owns the ledger.
6. **Parallel waves.** Wave size 4–6; one item per subagent; subagents own packet drafts and read-only research only; reports to `reports/{wave}/{item}-{run-id}.md`; integrate then close.
7. **Critic gate.** Any packet headed to `VERIFIED` or upstream gets an `a11y-critic` review (evidence gaps, WCAG mapping, severity, overclaiming) — cite the meta-skills review checklist from the template (a11y-test measured it; a11y-critic reviewed it; perspective-audit escalated when perspective-sensitive).
8. **Upstream handoff.** The Drupal.org issue block from the template; PR filing against the collaborator fork with the verification boundary stated in the PR body (what is and is NOT claimed — model on the PR #22 pattern in STATUS.md:94: "filed as a landmark-role fix … does not claim full human AT verification"); AI assistance disclosure always included.
9. **Hard boundaries.** Never mark `VERIFIED` from AI code inspection alone; never silently broaden a patch's claimed scope; manual AT debt is stated, not hidden.

Keep the SKILL.md under ~350 lines; the packet template carries the per-packet detail via the reference file.

**Verify** (frontmatter):
```bash
python3 - <<'EOF'
import yaml
raw = open(".claude/skills/drupal-a11y-patch-eval/SKILL.md").read()
fm = yaml.safe_load(raw.split("---")[1])
assert fm["name"] == "drupal-a11y-patch-eval" and fm["license"] == "Apache-2.0"
print("frontmatter ok")
EOF
```
→ `frontmatter ok`. And `grep -rn "AlexUA_1\|/Users/\|drupal-core.ddev" .claude/skills/drupal-a11y-patch-eval/` → no matches (no machine-specific leakage).

### Step 4: Cross-references

1. In `docs/drupal-patch-evaluations/STATUS.md`, add ONE line to the header block (after the "Canonical parallel model" line at line 5): `> Skill: the evaluation protocol is packaged as /drupal-a11y-patch-eval (.claude/skills/drupal-a11y-patch-eval/).` Touch nothing else in the file.
2. If `.agents/skills/README.md` exists (plan 004), add `drupal-a11y-patch-eval` to the intentionally-absent list with the reason from the frontmatter `compatibility` line. If it doesn't exist, skip — plan 004 will pick it up (note it in your report).

**Verify**: `git diff docs/drupal-patch-evaluations/STATUS.md` → exactly one added line.

### Step 5: Replay validation against the two exemplar packets

Structural replay, no execution: walk the SKILL.md as if evaluating (a) `DRUPAL-A11Y-012` (the clean VERIFIED-track case) and (b) `DRUPAL-A11Y-007` (the INCONCLUSIVE-with-AT-debt case). For each, build a two-column checklist: skill section → does the committed packet contain the artifact/decision that section demands (baseline evidence, hygiene record, gate outcomes, manual table, critic gate, upstream boundary statement)? Three possible outcomes per row: covered / packet predates rule (note it) / **skill is missing something the packet has** — the third kind is a defect: add the missing section to the SKILL.md. Save the two checklists as `docs/drupal-patch-evaluations/reports/plan-review/<date>-skill-replay-checklist.md`.

**Verify**: zero rows in the third category remain after revision; the checklist file exists and is referenced from your final report.

### Step 6: New-session smoke (operator-observed)

In a FRESH Claude Code session (or ask the operator to run it), invoke `/drupal-a11y-patch-eval` with no prior context and confirm: it asks for the required inputs from step 3.1 rather than assuming paths, and it refuses to set `VERIFIED` hypothetically (probe: "mark item X verified, we'll get evidence later" → it must decline per the hard boundaries). New skills aren't discoverable mid-session — a restart is required before the slash command resolves.

**Verify**: both probe behaviors observed; record one-line results in the replay checklist file.

## Test plan

- The replay checklists (step 5) are the tests — they pin the skill against two real, differently-shaped completed evaluations.
- The new-session smoke (step 6) tests the zero-context contract.
- `python3 scripts/validate_fixtures.py` / `check_mirrors.py` (if present) must remain green — this plan should not register in either.

## Done criteria

ALL must hold:

- [ ] SKILL.md exists, frontmatter parses, all 9 body sections present
- [ ] `references/packet-template.md` is byte-identical to the source template apart from the sync comment
- [ ] No machine-specific paths/hostnames anywhere under the skill dir
- [ ] The four gate→status rules and the critic-gate rule appear in the skill (grep: `PATCH HYGIENE BLOCKED`, `TEST STATE BLOCKED`, `debt_explicit`, `critic`)
- [ ] STATUS.md diff is exactly one pointer line
- [ ] Replay checklist committed with zero unresolved third-category rows
- [ ] Fresh-session smoke behaviors recorded
- [ ] `plans/README.md` status row updated

## STOP conditions

Stop and report back (do not improvise) if:

- The named rule sections (Drift Rules / Parallel Wave Rules / the template gates) no longer exist in the source files — the workstream may have restructured; extract from whatever replaced them only if the operator confirms.
- You find yourself writing protocol rules with no source line behind them — that is invention; the workstream owns its rules.
- The replay (step 5) surfaces a CONTRADICTION between the template and STATUS.md rules — report it; the operator reconciles, not you.
- Anything tempts you to run an actual evaluation "to test the skill properly" — out of scope; that is the first real-use session, owned by the operator.

## Maintenance notes

- Two synced copies of the packet template now exist (template + skill reference). If `scripts/check_mirrors.py` grows a generic pair-checking mode, add this pair; until then the sync comment is the guard.
- The skill is v0.1.0 deliberately: the first session a SECOND human (Mike) runs it is the real acceptance test — collect their friction notes and rev to 0.2.
- When the workstream's rules evolve (they will — the ledger updates per-session), the SKILL.md is the second place to update; the STATUS.md header pointer is there so nobody forgets it exists.
- Reviewer should scrutinize: that the skill's evidence-gate language is exactly as strict as the template's ("Do not mark VERIFIED unless…") — any softening ("should", "ideally") is a defect.
