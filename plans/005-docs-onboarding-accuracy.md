# Plan 005: Make the docs match reality — onboarding prerequisites, command list, counts, and caveats

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat de0031f..HEAD -- README.md CLAUDE.md EVAL-GAPS-PLAN.md ollama/README.md evals/harness/README.md .claude/skills/a11y-workflow/SKILL.md`
> If any in-scope file changed since this plan was written, compare the
> "Current state" excerpts against the live files before proceeding; on a
> mismatch, treat it as a STOP condition.

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none (one soft reference to `ollama/requirements.txt` from plan 001 — fallback included in step 1)
- **Category**: docs
- **Planned at**: commit `de0031f`, 2026-06-11

## Why this matters

This repo is public, installable (`npx skills add zivtech/a11y-meta-skills`), and positions its benchmark story as the credibility anchor. Four verified accuracy gaps undercut that: (1) a fresh contributor following `ollama/README.md` hits `ModuleNotFoundError: No module named 'yaml'` because no Python package install step exists anywhere; (2) the README's Commands section omits `/a11y-workflow` — the one command that drives the whole documented lifecycle; (3) CLAUDE.md says "60 graded fixtures (33 critic, 25 perspective-audit, 2 planner)" — but 25 planner fixtures exist on disk; only 2 were *benchmarked*, and the sentence conflates suite size with benchmark coverage; (4) README's Model Baselines lists `qwen3.5:27b` as a peer baseline without the caveat (documented in BENCHMARK.md:249-254) that its run was stopped at 17/33 due to `/think` stalls. None of these require new measurements — every correction below restates numbers already recorded in BENCHMARK.md/EVAL-GAPS-PLAN.md or facts verified on disk; do not introduce any new metric claims.

## Current state

Verified excerpts at commit `de0031f`:

- `README.md:128-134` Commands section lists exactly four commands (`/a11y-planner`, `/a11y-critic`, `/a11y-test`, `/perspective-audit`); `.claude/skills/a11y-workflow/` exists and CLAUDE.md documents `/a11y-workflow full src/components/Modal.tsx`.
- `README.md:141-144` Model Baselines bullets include: `**Ollama local models** — qwen3:32b, qwen3.5:27b, llama3.3:70b, qwen3.5:latest, and deepseek-r1 probes`.
- `README.md:161-197` Repository Layout code block — has no `teams/` under `.claude/`, no `drupal-patch-evaluations/` under `docs/`, and under `evals/suites/` shows only `webwright-benchmark/` (the `a11y-critic/`, `a11y-planner/`, `perspectives/` suites — the repo's main eval assets — are absent from the diagram).
- `CLAUDE.md` (repo root), in "Local Model Portability (Ollama)": `Benchmarked against 60 graded fixtures (33 critic, 25 perspective-audit, 2 planner) with cross-platform baselines for Claude API, Codex/OpenAI, and local Ollama models.` Disk truth: 33 critic fixtures, 25 perspective fixtures (+5 calibration), 25 planner fixtures of which 2 are benchmarked (EVAL-GAPS-PLAN.md:14 confirms "25 fixtures … 2/25" benchmarked).
- `ollama/README.md:1-30` — intro + Quick Start. Quick Start covers `ollama serve` / `ollama pull` but there is NO `pip install` instruction anywhere in the file; the scorers require PyYAML and the cloud runner requires `anthropic` (`ollama/score_output.py:17`, `run_cloud_benchmark.py:221` lazy import). `ANTHROPIC_API_KEY` is mentioned at `ollama/README.md:137` — env var documented, package install not.
- `EVAL-GAPS-PLAN.md:1-7` — header says `**Purpose**: Historical gap-fill plan …`; the execution-order block at the bottom shows all phases checked complete. No visible completion banner near the top; section headers still read as active work.
- `evals/harness/README.md` — full content is 2 sentences saying the harness "originated in the source monorepo"; it does not point to the runners that actually execute these suites (`ollama/run_benchmark.py`, `ollama/run_cloud_benchmark.py`).
- `.claude/skills/a11y-workflow/SKILL.md:1-4` frontmatter has only `name` + `description`. The other four skills all carry `license: Apache-2.0`, `compatibility: …`, `metadata: {author: zivtech, version: …}` (verified on a11y-critic, a11y-planner, perspective-audit; perspective-audit additionally has `disallowedTools`).
- Style: external-facing README prose is short declarative sentences; keep that register.

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Locate exact lines | `grep -n "<text>" <file>` | line number for each edit target |
| YAML frontmatter check | `python3 - <<'EOF'` … parse frontmatter … `EOF` (given in step 6) | `frontmatter ok` |
| Link/path sanity | `ls <referenced path>` | exists |

## Scope

**In scope**:
- `README.md`, `CLAUDE.md`, `EVAL-GAPS-PLAN.md`, `ollama/README.md`, `evals/harness/README.md`
- `.claude/skills/a11y-workflow/SKILL.md` (frontmatter only)
- `ollama/requirements.txt` (ONLY if plan 001 has not created it — see step 1)

**Out of scope** (do NOT touch):
- `ollama/BENCHMARK.md` — historical record (plan 002 owns its changelog note).
- Any number/percentage not explicitly quoted in this plan — do not "freshen" other metrics; new metric claims require new measured data, which is out of scope.
- `.agents/`, `.codex/` mirrors (plan 004), `docs/drupal-patch-evaluations/**` (active workstream ledger), `docs/*.html` (generated).
- The skill BODY of a11y-workflow — frontmatter only.

## Git workflow

- Branch: `advisor/005-docs-onboarding-accuracy`
- Conventional commits, e.g. `docs: add Python prerequisites to ollama README`.
- Do NOT push or open a PR unless the operator instructed it.

## Steps

### Step 1: Python prerequisites in `ollama/README.md`

Insert a `## Prerequisites` section between the intro paragraph (ends line 3) and `## Quick Start` (line 5):

```markdown
## Prerequisites

- Python 3.10+
- Python packages: `pip3 install -r ollama/requirements.txt` (PyYAML for all
  scorers; `anthropic` only needed for Claude API runs)
- [Ollama](https://ollama.com) installed and serving (`ollama serve`), with at
  least one supported model pulled (see Quick Start)
- For hosted runs only: `ANTHROPIC_API_KEY` exported (Claude) or Codex CLI
  authenticated (OpenAI) — see "Cross-platform baselines" below
```

If `ollama/requirements.txt` does not exist (plan 001 not yet executed), create it with exactly:
```
pyyaml>=6.0
anthropic>=0.40
```

**Verify**: `grep -n "pip3 install -r ollama/requirements.txt" ollama/README.md` → 1 hit; `ls ollama/requirements.txt` → exists.

### Step 2: README Commands + Model Baselines caveat

1. In `README.md`, the Commands section currently reads (lines 128–134):
```markdown
## Commands

- `/a11y-planner` — design accessibility before coding
- `/a11y-critic` — review plans or implementations
- `/a11y-test` — run keyboard, axe-core, and visual regression tests
- `/perspective-audit` — deep review from escalated disability/situational access perspectives
```
Add as the FIRST bullet:
```markdown
- `/a11y-workflow` — orchestrate the full lifecycle (scout → plan → critique → test → critique), Claude Code only
```
2. In the Model Baselines section, change the bullet
`- **Ollama local models** — qwen3:32b, qwen3.5:27b, llama3.3:70b, qwen3.5:latest, and deepseek-r1 probes`
to
`- **Ollama local models** — qwen3:32b, llama3.3:70b, qwen3.5:latest, plus qwen3.5:27b (partial run: stopped 17/33 on /think stalls) and deepseek-r1 probes`
(The 17/33 figure restates `ollama/BENCHMARK.md:249-254`; do not invent different numbers.)

**Verify**: `grep -n "a11y-workflow" README.md` → at least one hit in the Commands section; `grep -n "17/33" README.md` → 1 hit.

### Step 3: README Repository Layout additions

In the layout code block (`README.md:163-197`), make three additions, matching the existing two-space indentation style:

1. Under `.claude/`, after the `skills/` subtree, add:
```text
  teams/                               # a11y-workflow team definition
```
2. Under `docs/`, add:
```text
  drupal-patch-evaluations/            # Drupal core a11y patch evaluation ledger, patches, reports
```
3. Under `evals/  suites/`, before `webwright-benchmark/`, add:
```text
    a11y-critic/                         # 33 critic fixtures + rubrics
    a11y-planner/                        # 25 planner fixtures + rubrics
    perspectives/                        # 25 + 5 calibration perspective fixtures
```

**Verify**: `grep -n "drupal-patch-evaluations/" README.md` → 1 hit inside the layout block; the block still renders as one fenced `text` code block (`grep -c '^```text' README.md` unchanged +0).

### Step 4: Fix the CLAUDE.md fixture-count sentence

Replace (locate with `grep -n "60 graded fixtures" CLAUDE.md`):

`Benchmarked against 60 graded fixtures (33 critic, 25 perspective-audit, 2 planner) with cross-platform baselines for Claude API, Codex/OpenAI, and local Ollama models.`

with:

`Benchmarked against the 33 critic fixtures and 25 perspective-audit fixtures in full, plus 2 of the 25 planner fixtures (planner coverage is a known gap — see EVAL-GAPS-PLAN.md), with cross-platform baselines for Claude API, Codex/OpenAI, and local Ollama models.`

**Verify**: `grep -c "60 graded fixtures" CLAUDE.md` → `0`; `grep -n "2 of the 25 planner" CLAUDE.md` → 1 hit.

### Step 5: Completion banner on EVAL-GAPS-PLAN.md and a useful harness README

1. In `EVAL-GAPS-PLAN.md`, insert directly after the `**Note**:` line (line 5) and before the `---`:
```markdown
> **STATUS: COMPLETE (2026-05-19).** All phases below are done; this document
> is retained as a historical record. Open follow-ons (Gemini baselines,
> planner benchmark expansion) are tracked as direction items in
> `plans/README.md`, not here.
```
2. Replace the full content of `evals/harness/README.md` with:
```markdown
# Eval Harness

There is no standalone harness in this repo. The fixture/rubric suites under
`evals/suites/` are executed by the benchmark runners in `ollama/`:

- `ollama/run_benchmark.py` — local Ollama runs (critic, planner, perspective)
- `ollama/run_cloud_benchmark.py` — hosted Claude / Codex runs with escalation
- `ollama/score_output.py`, `score_perspective.py`, `score_planner.py` — scoring

See `ollama/README.md` for prerequisites and commands, and
`ollama/BENCHMARK.md` for committed results. The original full harness lives
in the upstream `zivtech-meta-skills` monorepo and is not required here.
```

**Verify**: `head -10 EVAL-GAPS-PLAN.md` shows the banner; `grep -n "run_benchmark.py" evals/harness/README.md` → 1 hit; `ls ollama/run_benchmark.py ollama/run_cloud_benchmark.py` → both exist.

### Step 6: a11y-workflow frontmatter parity

In `.claude/skills/a11y-workflow/SKILL.md`, expand the frontmatter from `name` + `description` to match the bundle's standard fields (keep `name` and `description` EXACTLY as they are):

```yaml
license: Apache-2.0
compatibility: Claude Code only — orchestrates Claude Code subagent spawning
metadata:
  author: zivtech
  version: "1.0.0"
```

Do NOT add `disallowedTools` — whether the orchestrator should be write-restricted is an operator decision (it currently may write handoff artifacts); record it in the PR description as an open question.

**Verify**:
```bash
python3 - <<'EOF'
import yaml
raw = open(".claude/skills/a11y-workflow/SKILL.md").read()
fm = yaml.safe_load(raw.split("---")[1])
assert fm["name"] == "a11y-workflow"
assert fm["license"] == "Apache-2.0"
assert fm["metadata"]["version"]
print("frontmatter ok")
EOF
```
→ `frontmatter ok`.

## Test plan

This is a docs plan; the verifications above are grep/parse gates. Additionally run the full plan-001 suite if present (`bash scripts/smoke_scorers.sh`, `python3 scripts/validate_fixtures.py`) to confirm nothing here broke tooling (it must not — no tooling files are in scope except the optional requirements.txt fallback).

## Done criteria

ALL must hold:

- [ ] `grep -c "pip3 install" ollama/README.md` ≥ 1 and `ollama/requirements.txt` exists
- [ ] README Commands section lists `/a11y-workflow`
- [ ] README Model Baselines carries the qwen3.5:27b `17/33` caveat
- [ ] README layout block names `teams/`, `drupal-patch-evaluations/`, and the three eval suites
- [ ] `grep -c "60 graded fixtures" CLAUDE.md` → 0
- [ ] EVAL-GAPS-PLAN.md has the STATUS: COMPLETE banner in its first 10 lines
- [ ] `evals/harness/README.md` points to the `ollama/` runners
- [ ] a11y-workflow frontmatter parses and contains license + metadata.version
- [ ] No numeric claim was added that does not appear verbatim in BENCHMARK.md or EVAL-GAPS-PLAN.md
- [ ] `git status` shows changes only in the in-scope file list
- [ ] `plans/README.md` status row updated

## STOP conditions

Stop and report back (do not improvise) if:

- Any "Current state" excerpt no longer matches the live file (drift since `de0031f`) — especially the CLAUDE.md sentence and README sections.
- You are tempted to update any benchmark number beyond the two quoted restatements (17/33 caveat, 2-of-25 planner) — that requires new measured data and is out of scope.
- `README.md`'s Commands or Layout sections have been restructured so the given anchors don't exist.

## Maintenance notes

- When the planner benchmark expands beyond 2/25 (direction item), CLAUDE.md's sentence from step 4 and EVAL-GAPS-PLAN's banner both need a touch — grep for "2 of the 25 planner".
- When a Gemini baseline lands, README Model Baselines gains a row and the four-document "when artifacts are present" hedge (README:145, BENCHMARK.md:17, EVAL-GAPS-PLAN.md:13, ollama/README.md:49) should collapse to actual results.
- Reviewer should scrutinize: that no new performance claims were introduced — this plan only restates recorded numbers and disk-verifiable facts.
