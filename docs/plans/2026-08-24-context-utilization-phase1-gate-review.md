# Phase 1 Gate Review — proposal-critic disposition record

**Date:** 2026-08-24 · **Reviewer:** proposal-critic subagent (def tier, high effort) · **Scope:** Phase 1 diff (plan §6 tasks 1.1–1.4) as a workflow change. **Verdict: REVISE → all required changes applied same session** (dispositions below), gates re-run green.

## Findings and dispositions

| # | Sev | Finding | Disposition |
|---|---|---|---|
| M1 | Major | `--max-output` documented as a token budget; the tool's own README says `--max-output <chars>` — truncate to N characters. Examples at 2000/500 chars would silently drop snapshot element refs — the silent-truncation class this initiative exists to kill. | **Fixed.** Relabeled to chars in the subsection + Key flags line; examples rescaled to 8000/2000; truncation-risk warning added to the flag description. Upstream `~/claude/CLAUDE.md` "token budget" wording also corrected (separate repo, uncommitted there). |
| M2 | Major | Task 1.4's enforcement premise false for acr-reporting: `check_mirrors.py` `SKILL_NAMES` didn't include it — strict CI green was vacuous for one of the three edited skills. | **Fixed.** `"acr-reporting"` added to `SKILL_NAMES`. Verified in the failing direction: heading perturbation in the `.agents` mirror → exit 1 naming acr-reporting; restored → exit 0, pair byte-identical. Noted: SKILL.md drift = headings/URLs/`.Codex/` paths/references-byte-identity, not body bytes — deliberate, so the intentionally-condensed `a11y-role-audit` Codex mirror (declared in its frontmatter, excluded from `SKILL_NAMES` by design) can pass. |
| M3 | Major | Recipe 1's verification note claimed "no sample scan output is committed" — false: `evals/results/lighthouse-compare-2026-08/ours/` holds five per-URL baseline-url-scan outputs + `summary.json`. A checkably-false negative-existence claim in a file whose job is verification honesty. | **Fixed.** Both recipe-1 jqs re-run verbatim against `ours/002-fire-product-a-gov.json` and `ours/summary.json` (clean, all field names match); note rewritten as real-artifact-verified citing that path. |
| m4 | Minor | bug-reporting one-liner misattributed field provenance ("finding block's already-captured fields (URL, XPath, …)") — the evidence-finding contract has no url/xpath/frequency fields; fabrication-adjacent phrasing. | **Fixed.** Reworded to "the finding entry's captured fields (from the scan/trace input or evidence-contract block)". |
| m5 | Minor | Recipe 3 didn't name the producing tool; repo has two census concepts (keyboard-a11y-tester census vs baseline-url-scan `--census`). | **Fixed.** One clause added naming keyboard-a11y-tester. |
| m6 | Minor | Recipe 1 dies on errored-viewport records (no `violations` key); SKILL.md pointed to a nonexistent "quickstart" section name. | **Fixed.** `.violations[]?`; pointer now names "Interactive reconnaissance with agent-browser". |

## What passed (critic-verified, spot-re-verified here)

R4 byte budget (subsection 980 bytes after fixes, ≤1.5KB cap); spec fidelity to all four task-table items; recipe 2 verified against the committed dropdown trace (both jqs reproduce byte-for-byte); recipe 4 unmistakably documentation-only (prompt-only boundary intact); no contradictions with a11y-critic Phase 0, the evidence contracts, or acr-reporting's procedure; no dead prose.

## Open items (unscored, not Phase 1)

- Does agent-browser print a truncation marker when `--max-output` fires? One live check when the CLI is on PATH shrinks M1's residual blast radius assessment.
- Cross-pointing bug-reporting/acr-reporting one-liners to `evidence-extraction.md` — deferred to Phase 2 wiring (spec said one line each).
