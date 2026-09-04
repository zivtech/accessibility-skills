# Phase 1 Handoff — Context-Utilization Initiative

**Date:** 2026-08-24 · **For:** a fresh session picking up Phase 1. Read this + the plan's §6 Phase 1 table; do **not** re-derive Phase 0 or re-read its receipts wholesale — practice the plan's own discipline (§5 principle 1: handles, not payloads).

## State at handoff

Branch `feat/verification-evidence-contract`, pushed through `8377a3f`. **Phase 0 is COMPLETE** — five themed commits:

| Commit | What |
|---|---|
| `d510218` | Plan + critic review: `docs/plans/2026-08-24-context-utilization-plan.md` (+ `-critic-review.md` with full disposition table) |
| `8aba447` | `scripts/session_context_report.py` — aggregate + `--drill`; resumed-session check verdict: the 45× re-reads are genuine (all-distinct uuids) |
| `44a0d21` | Client-side context-overflow guard in all 6 benchmark lanes + interactive wrapper; per-suite num_ctx maps (behavior-preserving lift); the deliberate `CRITIC_CTX["qwen3:32b"]=32768` fix; `ollama/test_context_guard.py` (26 tests) |
| `af79ece` | Retro-probe + historical-exposure receipts: `evals/results/context-utilization-phase0/` (context token-arrays stripped to length+sha256) |
| `8377a3f` | `ollama/BENCHMARK.md` dated annotation of the qwen3:32b critic history |

**Retro-probe verdict (settled — don't reopen):** annotate, not clear. qwen3:32b's tokenizer is the leanest measured (13,853 system+prefix); one fixture (`multistep-form-error-clearing`, 16,447 tokens vs the historical 16,384 window) ran all three eras with only 8,194 tokens (49.8%) evaluated — the one confirmed asterisk. Output-side clipping **not in evidence** across all 99 historical critic rows. Published aggregates stand.

**CI:** this repo's CI is **pull_request-triggered** — the push alone starts no run. Local CI-equivalent gates all green at handoff (`check_mirrors` no-drift [report-only locally; CI runs strict], `check_client_refs` pass, `validate_fixtures` pass, `lint_skills` pass 17 files/2 surfaces, guard tests 26/26). **Opening a PR is the way to get CI's read** — Alex's call on when.

## Phase 1 — the work (spec: plan §6 Phase 1; per-task executor/model/effort there)

1. **1.1** a11y-test SKILL.md "Evidence consumption" subsection (≤1.5KB in the body — the net context budget of the diff itself is a named review criterion) + new `references/evidence-extraction.md` (jq recipes: axe → [rule, impact, selector, count]; trace → failing steps; census → counts + first divergence; the PreToolUse filter-hook as documented recipe, **never shipped config**); `--max-output` added to all agent-browser examples; screenshots referenced by path, viewed only for visual-class adjudication; long commands write to file. Executor: sonnet subagent drafts.
2. **1.2** CLAUDE.md "Working In This Repo" bullet: SKILL.md files >30KB navigated by Grep + `offset`/`limit` section reads; whole-file Reads only for whole-file edits.
3. **1.3** bug-reporting + acr-reporting: one line each forbidding wholesale evidence-corpus re-reads during serialization.
4. **1.4** Mirror sync `.agents/skills/` for every edited skill — `check_mirrors.py` strict CI enforces (drift tier: headings/URLs/reference bytes, not body prose).

**Gate:** proposal-critic (its def's tier, effort high) reviews the diffs as a workflow change; mirrors green; then commit per theme.

## Watch-outs

- `ollama_a11y.run()` now returns `GuardedResponse` (a `str` subclass carrying `.overflowed`) — `run_chain_local.py` and `run_critic_control.py` depend on plain-str behavior. Do not "simplify" it.
- `check_client_refs.py` bans client identifiers in anything tracked (case-insensitive). It already caught one slip in this initiative's drafting — assume it will catch yours; run it before committing docs.
- While editing the big SKILL.md files, practice 1.2's own rule (Grep-first, section reads) — the F2 baseline says whole-file re-reads of these exact files are the single biggest measured waste.
- Subagents: depth-1 always; returns are digests + paths, never payloads.

## Parked decisions (Alex's, do NOT bundle into Phase 1)

1. **Planner/bug-report/perspective flat num_ctx defaults** are razor-thin against today's real fixtures — the live guard will start refusing those runs as `INVALID`. Raising defaults breaks comparability with historical rows; route through per-model `num_predict=1` probes with their own receipt (plan Phase 0 "guard-landing finding").
2. `BASH_MAX_OUTPUT_LENGTH` / `MAX_MCP_OUTPUT_TOKENS` figures still need the one-line pin receipt.
3. The manual `/usage` cross-check of the analyzer's token estimates (documented in the script docstring).
4. When to open the PR for CI.

## After Phase 1

Phase 2 (evidence-reader agent) is next and Phase 3 formally depends on it (blind pack curation). The plan's decision rules and registered predictions are frozen in the plan doc — don't re-litigate them, execute them.
