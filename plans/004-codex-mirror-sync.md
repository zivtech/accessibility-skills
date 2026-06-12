# Plan 004: Sync the Codex skill mirrors and turn on strict drift checking

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat de0031f..HEAD -- .claude/skills/a11y-test/SKILL.md .agents/skills/ .github/workflows/ci.yml scripts/check_mirrors.py`
> If `.claude/skills/a11y-test/SKILL.md` or the `.agents/` mirrors changed
> since this plan was written, compare the "Current state" excerpts against
> the live files before proceeding; on a mismatch, treat it as a STOP
> condition. (`ci.yml` and `scripts/check_mirrors.py` appearing in the diff
> is EXPECTED — plan 001 creates them.)

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: plans/001-ci-verification-baseline.md (for `scripts/check_mirrors.py` and `ci.yml`; steps 1–3 can land without it, step 4 cannot)
- **Category**: bug
- **Planned at**: commit `de0031f`, 2026-06-11

## Why this matters

This repo ships the same four skills on two surfaces: `.claude/skills/` (Claude Code) and `.agents/skills/` (Codex). The repo's own CLAUDE.md mandate is "sync intentionally rather than drifting silently." Two silent drifts exist today:

1. The Codex `perspective-audit` mirror tells the agent to load its reference checklists from `.Codex/skills/...` — a directory that does not exist (mechanical find-replace artifact). This is a **live runtime failure**: the skill's escalation flow depends on reading those reference files at invocation time.
2. The Codex `a11y-test` mirror is missing the entire Webwright lane (the third browser-automation mode added 2026-05-26): the routing-table row, the decision flowchart, and the 42-line "Test script generation with Webwright" section. It still says "two distinct execution modes" where the Claude surface says three. Webwright *generation* is Claude Code-only, but per this repo's CLAUDE.md, generated `.py` scripts ARE executable from Codex (`python3 script.py`) — so the Codex surface should describe the lane with that adaptation, not omit it.

Plan 001 ships `scripts/check_mirrors.py` in report-only mode precisely because of these known drifts; this plan fixes the content and flips the check to strict so the next drift fails CI instead of festering.

## Current state

Verified at commit `de0031f`:

- `.agents/skills/perspective-audit/SKILL.md` lines 65–66 and 159–160 reference `.Codex/skills/perspective-audit/references/...`. The correct prefix is `.agents/skills/...` — the reference files exist there and are byte-identical to the `.claude/` copies.
- `.claude/skills/a11y-test/SKILL.md` heading map (the source of truth to port from):
  - line 13 `## Browser Tooling Routing (read first)` — contains the 3-row routing table; the Webwright row is at line 21; the decision flowchart block is lines 25–32.
  - line 15: `This skill has three execution modes. Pick the right one before running anything:`
  - line 53 `## Test script generation with Webwright` — section runs through line ~94 (next `##` heading, `## 1. Keyboard Accessibility Tests`, is at line 98).
- `.agents/skills/a11y-test/SKILL.md` line 15 says `This skill has two distinct execution modes…`; it has NO Webwright table row, NO flowchart, NO Webwright section (confirmed by diff: `21d20`, `25,32d23`, `52,94d42`).
- Intentional, KEEP-AS-IS divergences between the surfaces: frontmatter `compatibility:` lines (`Claude Code-compatible` vs `Codex-compatible`) and `.claude/`↔`.agents/` path prefixes in body text.
- `.agents/skills/` contains 4 skills; `a11y-workflow` exists only under `.claude/skills/` (it orchestrates Claude Code subagent spawning, which has no Codex equivalent) — currently undocumented as intentional.
- From plan 001: `scripts/check_mirrors.py` exits 0 always, has a `--strict` flag (exit 1 on any `.Codex/` hit or `##`-heading-set mismatch); `.github/workflows/ci.yml` runs it WITHOUT `--strict`.

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Mirror check (report) | `python3 scripts/check_mirrors.py` | exit 0 |
| Mirror check (strict) | `python3 scripts/check_mirrors.py --strict` | exit 1 BEFORE this plan; exit 0 AFTER step 3 |
| Broken-path scan | `grep -rn '\.Codex/' .agents/` | hits before step 1; empty after |

## Scope

**In scope**:
- `.agents/skills/perspective-audit/SKILL.md` (4 line edits)
- `.agents/skills/a11y-test/SKILL.md` (port Webwright content, adapted)
- `.agents/skills/README.md` (create — mirror policy note)
- `.github/workflows/ci.yml` (one-word change: add `--strict`)

**Out of scope** (do NOT touch):
- ANY file under `.claude/skills/` — the Claude surface is the source of truth and is correct.
- `.codex/agents/*.toml` — separate surface, no findings there.
- `scripts/check_mirrors.py` — strict mode already implemented by plan 001; if its strict semantics don't match this plan's needs, that's a STOP, not a patch-it-here.
- `.claude/agents/*.md` protocol drift (Phase 0) — known, deferred; see plans/README.md.

## Git workflow

- Branch: `advisor/004-codex-mirror-sync`
- Conventional commits, e.g. `fix: correct .Codex reference paths in Codex perspective-audit mirror`.
- Do NOT push or open a PR unless the operator instructed it.

## Steps

### Step 1: Fix the four broken paths in the Codex perspective-audit mirror

In `.agents/skills/perspective-audit/SKILL.md`, replace the string `.Codex/skills/` with `.agents/skills/` on lines 65, 66, 159, 160 (a global replace of that exact string in this one file is safe — verify it produces exactly 4 changes).

**Verify**: `grep -rn '\.Codex/' .agents/` → no output. `ls .agents/skills/perspective-audit/references/` → `arrm-perspective-mapping.md  perspectives.md` (the targets exist).

### Step 2: Port the Webwright lane into the Codex a11y-test mirror, adapted for Codex

All edits in `.agents/skills/a11y-test/SKILL.md`:

1. Change line 15 from `This skill has two distinct execution modes. Pick the right one before running anything:` to `This skill has three execution modes. Pick the right one before running anything:`
2. In the routing table (under `## Browser Tooling Routing (read first)`), add the Webwright row from `.claude/skills/a11y-test/SKILL.md:21`, with the parenthetical changed from `(Claude Code plugin)` to `(generated in Claude Code; run the produced .py from Codex)`.
3. Add the decision flowchart block (`.claude` lines 25–32) after the table, changing the YES line to:
   `YES → /webwright:run in a Claude Code session (one-shot) or /webwright:craft (reusable); execute the generated .py from Codex via python3 <script>.py`
4. Copy the entire `## Test script generation with Webwright` section (`.claude` lines 53–94, ending before `## 1. Keyboard Accessibility Tests`) into the same relative position in the `.agents/` file (i.e., immediately before its `## 1. Keyboard Accessibility Tests` heading... if the `.agents/` file instead places it after the agent-browser section, match the `.claude` ordering: Routing → agent-browser recon → Webwright → numbered test sections). Apply exactly two adaptations to the copied text:
   - In the **Limitations** list, change `Requires Claude Code plugin install — not available in Codex CLI` to `Script GENERATION requires the Claude Code plugin (not available in Codex CLI); generated .py scripts run anywhere Python + Playwright are installed, including from Codex sessions.`
   - Leave every other line verbatim, including the benchmark results line (25/25, 2026-05-26) and the quality-gate list ("The operator must review generated scripts before trusting results") — these are surface-independent facts.

**Verify**: `python3 scripts/check_mirrors.py` → the a11y-test pair now reports identical `##` heading sets (no missing `## Test script generation with Webwright`). `grep -c "three execution modes" .agents/skills/a11y-test/SKILL.md` → `1`.

### Step 3: Document the mirror policy

Create `.agents/skills/README.md`:

```markdown
# Codex skill mirrors

These are Codex-compatible mirrors of `.claude/skills/`. The `.claude/`
surface is the source of truth; edit there first, then sync here.

Intentional divergences (everything else must match):
- frontmatter `compatibility:` line (Codex vs Claude Code)
- path prefixes in body text (`.agents/skills/...` vs `.claude/skills/...`)
- Webwright lane notes: script GENERATION is Claude Code-only; Codex runs the
  generated `.py` scripts.

Intentionally absent from this surface:
- `a11y-workflow` — it orchestrates Claude Code subagent spawning, which has
  no Codex equivalent. On Codex, run the four skills individually in lifecycle
  order: planner → critic → test → perspective-audit (on escalation).

Drift is checked by `scripts/check_mirrors.py --strict` in CI (heading-set
comparison + broken-path scan). If you add a heading to a `.claude` skill,
sync the mirror in the same commit or CI fails.
```

**Verify**: file exists; `python3 scripts/check_mirrors.py` still exits 0 (the README must not confuse the checker — it only compares SKILL.md pairs).

### Step 4: Flip CI to strict

In `.github/workflows/ci.yml`, change the mirror step:

```yaml
      - name: Mirror drift check (strict)
        run: python3 scripts/check_mirrors.py --strict
```

**Verify**: `python3 scripts/check_mirrors.py --strict; echo "exit=$?"` → `exit=0`. Then `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml')); print('ok')"` → `ok`.

## Test plan

- `scripts/check_mirrors.py --strict` is the test; before this plan it must exit 1 (run it first and record that), after steps 1–3 it must exit 0. That before/after flip is the regression demonstration.
- Negative probe: temporarily add a dummy `## Probe` heading to `.agents/skills/a11y-critic/SKILL.md`, confirm `--strict` exits 1, revert the probe, confirm exit 0 again.

## Done criteria

ALL must hold:

- [ ] `grep -rn '\.Codex/' .agents/` → no matches
- [ ] `python3 scripts/check_mirrors.py --strict` exits 0
- [ ] `.agents/skills/a11y-test/SKILL.md` contains the headings `## Test script generation with Webwright` and the text `three execution modes`
- [ ] The two Codex adaptations (generation-vs-execution wording) are present — `grep -c "run the produced .py from Codex\|generated .py scripts run anywhere" .agents/skills/a11y-test/SKILL.md` ≥ 2
- [ ] `.agents/skills/README.md` exists and names `a11y-workflow` as intentionally absent
- [ ] CI workflow runs the mirror check with `--strict`
- [ ] `git status` shows changes only in: `.agents/skills/perspective-audit/SKILL.md`, `.agents/skills/a11y-test/SKILL.md`, `.agents/skills/README.md`, `.github/workflows/ci.yml`
- [ ] `plans/README.md` status row updated

## STOP conditions

Stop and report back (do not improvise) if:

- `scripts/check_mirrors.py` does not exist (plan 001 not executed) — do steps 1–3, skip step 4, and mark this plan BLOCKED-PARTIAL in the index with that note.
- The operator has stated the Codex surface should intentionally exclude Webwright (check `plans/README.md` notes and recent commit messages for such a decision) — then do steps 1, 3, 4 only and report.
- After step 2, `--strict` still fails on the a11y-critic or a11y-planner pairs — those were heading-identical at planning time; if they now differ, new drift appeared since `de0031f`. Report it; do not sync files this plan didn't scope.
- The `.claude/skills/a11y-test/SKILL.md` Webwright section is no longer at lines 53–94 — re-locate by heading; if the heading is gone entirely, STOP.

## Maintenance notes

- Every future edit to a `.claude/skills/*/SKILL.md` heading structure now requires the mirror in the same commit (CI enforces). Body-text drift below heading level is still NOT enforced — flagging that is the report-mode output; review it when touching skills.
- Deferred sibling problem (recorded in plans/README.md): `.claude/agents/*.md` restate skill protocols verbatim and have already drifted (Phase 0 exists in `a11y-critic` SKILL.md:185 but not in `.claude/agents/a11y-critic.md`). Whether to single-source or extend the checker to agent files is a maintainer decision — agent files may need to stay self-contained for spawning.
- Reviewer should scrutinize: the Codex adaptations in step 2 — they must not claim Webwright generation works in Codex (it does not).
