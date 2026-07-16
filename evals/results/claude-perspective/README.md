# Claude subagent perspective lane — raw artifacts (2026-07-13)

- Run date: 2026-07-13; mechanism: Claude Code `Agent(subagent_type="general-purpose", model="opus")`, one background subagent per fixture (25 total, parallel), subscription transport — no API key. Prompts composed identically to `run_cloud_benchmark.py`'s `load_perspective_system_prompt()` + `build_escalation_prompt()` (same SKILL.md + references system prompt, same metadata-driven escalation block), with **one deliberate deviation: this lane ran blind.**
- **Blind protocol:** every fixture was truncated at its `## Accessibility Issues` heading before prompting (`re.split(r"^## Accessibility Issues.*$", raw, flags=re.M)[0]`), and each composed prompt was assert-verified to contain neither `Planted` nor the heading. Reason: during setup we found `load_fixture()` in both `ollama/run_benchmark.py` and `ollama/run_cloud_benchmark.py` reads raw fixture files, which embed the full answer key (expected findings, evidence, fixes) — `git log -S` shows truncation logic never existed, so **all previously committed critic/perspective lanes ran non-blind.** Do not compare this lane's numbers 1:1 against those rows. Remediation tracked separately (runner truncation + caveats on published rows + blind re-runs).
- Shape: runner-compatible response JSONs (`response` + `_benchmark` provenance incl. `blind: true`); scored with `python3 ollama/score_perspective.py <json> evals/suites/perspectives/fixtures/<id>.metadata.yaml`. Scorer outputs committed under `scores/`.
- Summary table: `evals/suites/perspectives/RESULTS-claude-opus-subagent.md`; published section: `ollama/BENCHMARK.md` → "Claude subagent lane — perspective".

## Headline

| Layer | Result |
|---|---|
| Pre-003 scorer (as first run) | 20 PASS / 1 WARN / 4 FAIL; must-find 35/37 |
| Post-003 scorer (re-scored after the 2026-07-13 scorer fixes this lane motivated) | **20 PASS / 5 WARN / 0 FAIL; must-find 36/37** |
| Content-adjudicated (receipts below) | **25/25** — every verdict correct, 37/37 must-find coverage (37 items across 20 must-find-bearing fixtures), 0 CRITICAL/MAJOR findings across all 5 CLEAN fixtures |

The committed `scores/` outputs are post-003. The 5 WARNs are all CLEAN fixtures: correct PASS
verdict, 0 CRITICAL/MAJOR — the scorer's WARN flag counts *any* structured findings on a CLEAN
fixture regardless of severity, and these audits raise only ENHANCEMENT/open-question items.

All pre-003 deductions were scorer artifacts, not model errors; each adjudication is verifiable against the committed audit text inside the response JSONs, and the post-003 re-score confirms them:

1. **4 CLEAN "FAIL (verdict BLOCK)" → actual PASS.** `dashboard-text-labels`, `login-form-clean`, `media-player-captions`, `nav-menu-landmarks` each conclude literally `**PASS** — no CRITICAL or MAJOR findings` with a findings-by-severity table showing CRITICAL 0 / MAJOR 0. The audits' verdict lines are formatted `**PASS** — …` (not `Verdict: PASS`), so `detect_verdict()`'s tier-1 regex misses and the tier-2 fallback — a whole-word ladder scan ordered `["BLOCK", "REVISE", "PASS"]` — matches a protocol-boilerplate `BLOCK` token earlier in the document and wins.
2. **1 CLEAN "WARN" → clean at the bar that matters.** `article-page-clean` gives a correct PASS verdict; its 3 structured findings are ENHANCEMENT-level or explicitly "not scored as a violation" open questions (2.4.5 unverifiable from a single component). The repo's CLEAN false-positive bar (0 MAJOR/CRITICAL) is met.
3. **2 must-find keyword misses → content present verbatim.** `custom-select-combobox` (1/2) and `tab-panel-arrow-keys` (1/2): the rubric keywords use single quotes (`role='tablist'`) while the audits write `role="tablist"`; both audits discuss the missing roles exhaustively (26 and 16 mentions respectively, including explicit findings lines). Post-003 quote normalization fixes `custom-select-combobox`; `tab-panel-arrow-keys` remains a rubric artifact — its scoring keyword is the compound string `role='tablist'/role='tab'/role='tabpanel'`, which no prose audit emits verbatim.

The scorer fixes this lane motivated (verdict conclusion-line tier; quote-normalized keyword matching; runner answer-key stripping with the `test_blind_prompts.py` guard) landed 2026-07-13 as post-003 scoring — see `ollama/BENCHMARK.md` → Scoring changelog, including the re-score deltas (gemini lane: unchanged).

## Per-fixture

See `evals/suites/perspectives/RESULTS-claude-opus-subagent.md` for the full table (scorer status, must-find counts, adjudication notes per fixture).

## Run integrity notes

- One first-wave agent (`product-carousel-autoplay`) terminated in 26s with zero tool calls, returning a block of unrelated injected/leaked instructions ("You are a security engineer reviewing a pull request…") instead of its DONE marker. The instructions were not acted on; the agent had written nothing; a hardened retry completed normally. No other agent showed the anomaly (24/25 clean first pass).
- Per-audit usage: ~90–130K subagent tokens, 3–11 minutes; 25 agents ran concurrently in the background.
- The CLEAN escalation block in the harness prompt says "this is a CLEAN baseline. Produce PASS verdict" — the audits did conclude PASS, but demonstrably from analysis (each documents the component's correct patterns in detail and includes ENHANCEMENT-level observations the hint would not supply). The hint is a harness-design artifact shared with all lanes; a stricter blind variant would drop it.
