# Speed Comparison: Webwright vs agent-browser

**Date:** 2026-05-26
**Machine:** macOS Darwin 25.4.0
**Targets:** WAI-ARIA APG example pages (public, remote)

## Script Execution Time (re-running existing Webwright-generated .py scripts)

| Task | Webwright Script | agent-browser batch | Ratio |
|---|---|---|---|
| Dialog focus trap (8 tabs + Escape + state checks) | 4.4s | 1.4s | 3.1x slower |
| Tabs (click 4 tabs + ArrowRight + state checks) | 4.2s | 2.6s | 1.6x slower |
| Menu (Enter + ArrowDown + End + Escape + state checks) | 3.6s | 1.5s | 2.4x slower |
| **Average** | **4.1s** | **1.8s** | **2.3x slower** |

## Total Webwright Workflow Time (LLM generates script + executes)

Derived from file timestamps: plan.md creation → final_script_log.txt written.
Includes Webwright's explore phase, script generation, iteration, and final execution.

| Task | Total Workflow | Script Execution | LLM Generation |
|---|---|---|---|
| Canary (disclosure toggle) | ~59s | ~4s | ~55s |
| Dialog focus trap | ~132s | ~4s | ~128s |
| Tabs ARIA state | ~68s | ~4s | ~64s |
| axe-core injection | ~33s | ~4s | ~29s |
| Menu keyboard nav | ~66s | ~4s | ~62s |
| ARIA tree inspection | ~36s | ~1s | ~35s |
| **Average** | **~66s** | **~3.5s** | **~62s** |

## What the Numbers Mean

**agent-browser is 2-3x faster for execution** because it uses a persistent Rust daemon with CDP — no Python interpreter startup, no Playwright browser launch overhead per run. Each `batch` call reuses the running Chrome instance.

**Webwright scripts pay ~2s Python + Playwright startup** on every run, plus they launch their own Firefox instance. This overhead is constant regardless of task complexity.

**The real cost is LLM generation time** (~30-130s per task). This is a one-time cost — once the script exists, re-runs are 3.5-4.5s. The agent-browser comparison is against its interactive mode, which also requires an LLM to compose the commands (that time isn't measured here since the commands were pre-written).

## Fair Comparison Notes

- agent-browser commands were pre-composed by the operator. In real use, an LLM would compose them interactively, adding per-command inference latency (~1-3s per command via Claude).
- Webwright's total workflow includes the LLM composing AND executing. The "first run" cost is high, but the script is reusable.
- agent-browser does NOT produce a persistent artifact — session logs exist but aren't re-runnable test scripts.
- Webwright scripts are CI-runnable (with a Python runner) without any LLM at all.

## Apples-to-Apples: Total Time to First Result

| Scenario | Webwright | agent-browser (interactive) |
|---|---|---|
| Simple task (axe-core, ARIA snapshot) | ~30-36s | ~5-10s (2-3 LLM turns + execution) |
| Medium task (tabs, menu) | ~66-68s | ~15-25s (5-8 LLM turns + execution) |
| Complex task (dialog focus trap) | ~132s | ~30-60s (10-15 LLM turns + execution) |
| **Re-run the same test later** | **~4s (no LLM)** | **Must re-compose (LLM again)** |

The breakeven point: if you'll run the test more than ~10 times, Webwright's upfront generation cost amortizes below agent-browser's per-run LLM cost.
