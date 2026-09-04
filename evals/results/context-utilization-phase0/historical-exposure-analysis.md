# Historical qwen3:32b critic-suite exposure to OUTPUT-side context clipping (num_ctx=16,384)

**Date:** 2026-08-24
**Scope:** Read-only re-analysis of the 99 committed `qwen3:32b` critic-suite response JSONs (`evals/results/ollama-blind/`, `evals/results/ollama-dehinted/`, `evals/results/ollama-rebaseline/`, 33 fixtures × 3 eras). Perspective-audit files (`ollama-perspective-*`) are excluded — they ran at `num_ctx=32,768`, out of scope.
**Question:** How many of these 99 rows show evidence of *output-side* clipping (generation cut off by hitting the context ceiling), as distinct from the *prompt-side* truncation already confirmed directly by the live probe in this same directory (`README.md`)?

**Headline finding, stated up front:** the mechanical procedure specified for this analysis flags 44–50 of 99 rows as "ceiling-contact." Every independent corroborating check run against those flags — the probe's own ground-truth measurement, structural completeness of the responses, and the sign of the correlation between fixture size and output length — contradicts them. The verdict is **(c) not in evidence**, and the reason the naive count is wrong is itself the most important finding here (see "Why the naive flag is unreliable" below). Numbers for all of this follow.

---

## 1. Method

### 1.1 Anchors (measured, from `README.md` in this directory — verified by re-reading, not re-derived)

| Quantity | Value | Status |
|---|---|---|
| System + `PROMPT_PREFIX` alone, true tokens | **13,853** | measured (qwen3:32b tokenizer, `num_ctx=32768` probe) |
| `button-skip-link-clean` (smallest), true prompt tokens | 14,489 | measured |
| `tabs-missing-arrow-nav` (median), true prompt tokens | 14,649 | measured |
| `multistep-form-error-clearing` (largest), true prompt tokens | 16,447 | measured |
| Historical config | `num_ctx=16,384`, `qwen3:32b` absent from `CRITIC_CTX` map → falls to `CRITIC_CTX_DEFAULT = 16384` | confirmed in `ollama/run_benchmark.py` (git HEAD) |
| Ground-truth prompt-truncation measurement, largest fixture, at `num_ctx=16,384` | server evaluated only **8,194** of the 16,447 true prompt tokens (both draws, deterministic) | measured, this probe |

### 1.2 Stripping logic (ported from `ollama/run_benchmark.py` @ git HEAD, verified against the working file, not re-implemented from memory)

```python
PROMPT_PREFIX = "Review the following React component for accessibility design issues. Execute all phases of the investigation protocol.\n\n"  # 121 chars, confirmed by len()

ANSWER_KEY_RE = re.compile(r"^## Accessibility Issues.*$", re.MULTILINE)

def strip_frontmatter(content):
    if content.startswith("---"):
        end = content.index("---", 3)
        return content[end + 3:].strip()
    return content

def strip_answer_key(content):
    blind = ANSWER_KEY_RE.split(content, maxsplit=1)[0].rstrip() + "\n"
    return blind

# load_fixture() in run_benchmark.py calls strip_answer_key(raw_read) only.
```

Checked directly: **none of the 41 files in `evals/suites/a11y-critic/fixtures/` start with `---`**, so `strip_frontmatter` is a confirmed no-op for every critic fixture — the only stripping that changes fixture byte/char counts is `strip_answer_key` (the blind-protocol answer-key removal). This was verified by scanning all 41 fixture file headers, not assumed.

### 1.3 Calibrating the chars-per-token ratio — and correcting the brief's arithmetic

The task brief's suggested check — `(16,447 − 13,853) = 2,594 tokens for 17,273 raw bytes → 6.66 bytes/token` — **is wrong, and re-deriving it shows why:** it divides the fixture's *raw, unblinded* file bytes (17,273, answer key still included) by the token delta measured on the *blinded* prompt (answer key stripped, `strip_answer_key` applied). Raw and blinded are different texts of different lengths; dividing one by a token count measured on the other overstates the ratio.

The internally-consistent calibration uses the **blinded body** (post-`strip_answer_key`, matching what `load_fixture()` actually sends) against the same token delta:

| Fixture | Raw bytes | Blinded body chars (post-`strip_answer_key`, reproduced here) | True prompt tokens | Δ tokens vs 13,853 baseline | Per-fixture ratio (chars/Δtoken) |
|---|---|---|---|---|---|
| `button-skip-link-clean` | 2,977 | 2,216 | 14,489 | 636 | 3.484 |
| `tabs-missing-arrow-nav` | 5,363 | 3,021 | 14,649 | 796 | 3.795 |
| `multistep-form-error-clearing` | 17,273 | 8,818 | 16,447 | 2,594 | **3.399** |

The largest fixture's own numbers reproduce the README's stated "8,818-char blinded body" exactly, and `8,818 / 2,594 = 3.399` — confirming the README's own "~3.4–3.8 chars/token" characterization, not the brief's 6.66 figure. **The 6.66 number is discarded; it is not a usable calibration point.**

Fitted ratio from the 3 points:
- Simple average of the 3 per-fixture ratios: **3.560 chars/token**
- Pooled (Σchars / Σtokens), used below: **3.491 chars/token**

**Calibration error of the pooled ratio against its own 3 source points** (predicted Δtokens = body_chars / 3.491, vs. actual):

| Fixture | Actual Δtokens | Predicted Δtokens | Error |
|---|---|---|---|
| `button-skip-link-clean` | 636 | 634.8 | −0.2% |
| `tabs-missing-arrow-nav` | 796 | 865.4 | **+8.7%** |
| `multistep-form-error-clearing` | 2,594 | 2,525.9 | −2.6% |

Max absolute error across the 3 calibration points: **8.7%**. This is the basis for treating every `est_*` figure below as **±~10%** — this is the *precision* uncertainty of the ratio itself. It is a separate, smaller issue from the *mechanism* problem described in §3, which is not a percentage error at all.

`est_prompt = 13,853 + stripped_body_chars / 3.491`; `est_budget = 16,384 − est_prompt`. Applied to all 33 fixtures used in the critic-suite corpus (same 33 IDs present in all three eras — verified by diff, zero mismatches).

---

## 2. Per-era table

| Era | Rows | eval_count min / median / p90 / max | Ceiling-contact (tol=100) | Ceiling-contact (tol=300) | Unclosed `<think>` | Any `<think>` at all |
|---|---|---|---|---|---|---|
| `ollama-blind` | 33 | 1,041 / 1,589 / 1,925 / 3,181 | 13 | 17 | 0 | 0 |
| `ollama-dehinted` | 33 | 973 / 1,609 / 2,011 / 2,531 | 14 | 15 | 0 | 0 |
| `ollama-rebaseline` | 33 | 1,092 / 1,776 / 2,162 / 2,373 | 17 | 18 | 0 | 0 |
| **Combined** | **99** | **973 / 1,633 / 2,027 / 3,181** | **44** | **50** | **0** | **0** |

`eval_count` is a **measured** field, read directly from each response JSON (present on all 99/99 rows). `done: true` on all 99/99 rows — no historical row carries an explicit incompleteness flag. Additional structural-completeness check (not in the original instructions, run because it directly bears on "was the response cut off"): triple-backtick code-fence balance is even (properly opened-and-closed) on **99/99** responses — an odd count would be the signature of a response truncated mid code-block.

44 (tol=100) / 50 (tol=300) rows out of 99 satisfy the literal formula `eval_count ≥ est_budget − tolerance`, spanning **17 of 33** fixtures at tol=100 and **19 of 33** at tol=300 (full fixture list in the script output; the low end of that list — `multistep-form-error-clearing`, `modal-complete-clean`, `search-focus-stays-in-input`, `form-field-vs-summary-errors`, `app-focus-order-illogical` — accounts for most of the margin). **Do not read this as "44–50 clipped rows" — see §3.**

---

## 3. Why the naive ceiling-contact flag is unreliable (the load-bearing finding)

The formula `est_budget = num_ctx − est_prompt` is only valid in the regime where `est_prompt < num_ctx` — i.e., where the full prompt actually fits and nothing is dropped before generation starts. The historical-exposure question assumed this regime holds everywhere, but this repo's own probe (in this same directory) directly measured that it does **not** hold for at least one fixture, and the downstream data are consistent with it not holding more broadly:

**Ground-truth check on the most extreme flagged row.** `multistep-form-error-clearing` has the smallest `est_budget` of any fixture (≈5 tokens — the estimated prompt, 16,379 tokens, essentially fills the 16,384 window). By the naive formula this is the single most severe ceiling-contact case in the corpus. But this is the *exact* fixture the live probe measured directly at `num_ctx=16,384`: the server evaluated only **8,194** of the 16,447 true prompt tokens (both draws, deterministic — see `README.md` §"Step 3"). That means the **real** operative generation budget for this fixture was `16,384 − 8,194 ≈ 8,190` tokens, not ≈5. All three historical `eval_count` values for this fixture — 3,181 (blind), 2,278 (dehinted), 2,355 (rebaseline) — sit comfortably inside that real 8,190-token budget, nowhere near it. **The fixture the naive formula flags most severely turns out, on the one occasion we have a direct measurement, to have the most real headroom, not the least** — because Ollama drops prompt content silently rather than encroaching on generation space (this is the same mechanism the probe already documented; the naive per-row formula in the task brief just doesn't model it).

**System-wide correlation check.** If output-side clipping were real and budget-driven, larger/tighter-budget fixtures should show *suppressed* (shorter) output — a positive correlation between `est_budget` and `eval_count`, and a negative correlation between raw fixture size and `eval_count`. The data show the **opposite sign** on both:

- Pearson r(raw fixture bytes, eval_count) across all 99 rows = **+0.508** — bigger fixtures produced *longer* responses, not shorter.
- Pearson r(est_budget, eval_count) across all 99 rows = **−0.441** — smaller nominal budget associated with *longer* output on average, not shorter.

Both signs are consistent with "response length tracks how much the fixture gives the model to comment on," and inconsistent with "response length is capped by remaining context." (`est_budget` and raw bytes are themselves inversely related by construction, so these two correlations are largely the same fact stated twice — reported both because the brief's formula is built on `est_budget` specifically.)

**Manual inspection of every structurally-unusual response ending.** 17 of 99 responses end in a bare non-punctuation character rather than `.`, `?`, or a closing code fence. Every one of the 17 was read in full at the tail: all end on a legitimate word or template field — `trend: new` (a literal field value in the finding template) or `**Open Questions**: None` — not a mid-word cutoff. None show a truncation signature.

Given all four checks point the same direction (ground-truth measurement, correlation sign, structural completeness, manual reading), the naive flag is best understood as identifying "fixtures whose *estimated* prompt size approaches or exceeds `num_ctx`" — a prompt-side risk indicator, which is real and already documented in `README.md` — misapplied here as if it were an output-side signal, which it is not.

---

## 4. The large-fixture rows in detail

The three ≥14.6KB-raw fixtures the probe flagged as plausible prompt-side overflow candidates (`README.md`'s closing paragraph: `app-focus-order-illogical` 14,921B, `dashboard-heading-inconsistency` 14,618B, `multistep-form-error-clearing` 17,273B — the only three at or above 14.6KB raw across all 41 fixtures):

| Fixture | Raw bytes | est_prompt (±~10%) | est_budget (±~10%, naive) | Era | eval_count (measured) | Response chars | Unclosed `<think>` | done |
|---|---|---|---|---|---|---|---|---|
| `multistep-form-error-clearing` | 17,273 | 16,379 | 5 | blind | 3,181 | 4,276 | No | true |
| | | | | dehinted | 2,278 | 4,263 | No | true |
| | | | | rebaseline | 2,355 | 4,543 | No | true |
| `app-focus-order-illogical` | 14,921 | 15,866 | 518 | blind | 2,251 | 5,345 | No | true |
| | | | | dehinted | 1,566 | 3,433 | No | true |
| | | | | rebaseline | 2,373 | 2,497 | No | true |
| `dashboard-heading-inconsistency` | 14,618 | 15,644 | 740 | blind | 1,799 | 4,105 | No | true |
| | | | | dehinted | 1,664 | 4,415 | No | true |
| | | | | rebaseline | 1,673 | 4,198 | No | true |

No anomalies beyond what §3 already covers: all 9 rows are `done: true`, contain no `<think>` tag (open or closed), have balanced code fences, and end on well-formed sentences or template fields. `multistep-form-error-clearing` is the only one of the three with a *directly measured* real budget (≈8,190, from the probe); the other two are estimates only, and their naive `est_budget` (518, 740) should be read with the same §3 skepticism, not as measured ceilings.

---

## 5. Bottom line

**(c) Not in evidence — with a caveat about what wasn't directly measured.**

- The mechanically-specified formula flags **44/99 rows (44%)** at the 100-token tolerance and **50/99 (51%)** at the 300-token tolerance, spanning 17–19 of the 33 distinct fixtures. Reported because the task specified this computation.
- Every corroborating signal available contradicts those flags: 0/99 rows show an unclosed `<think>` block or any `<think>` tag at all; 0/99 show an unbalanced code fence; 99/99 carry `done: true`; all 17 structurally-unusual response endings, read in full, terminate on legitimate content, not mid-word; the sign of the correlation between fixture size/budget and output length runs opposite to what real clipping would produce (r = +0.508 and −0.441, both wrong-signed for the clipping hypothesis); and the one fixture with a *direct, ground-truth* measurement of actual evaluated-prompt-tokens (`multistep-form-error-clearing`, from this directory's own probe) shows the naive formula understating real headroom by roughly **1,600×** (≈5 tokens estimated vs. ≈8,190 tokens real) — precisely because the server truncates the *prompt*, not the *output*, when a fixture overflows the window.
- Net: no row in the 99-row historical qwen3:32b critic-suite corpus shows credible evidence of output-side context clipping. What the naive formula is actually detecting is a subset of fixtures whose *estimated* prompt size is large relative to `num_ctx` — a prompt-side risk category that duplicates, at lower fidelity, what the live probe already established directly for the single largest fixture.

**What this does NOT establish:**
- It does not revisit or weaken the probe's own finding of severe **prompt-side** truncation for `multistep-form-error-clearing` — that finding is a direct measurement and stands independently of this analysis, which is scoped to the output side only.
- Only one fixture (`multistep-form-error-clearing`) has a direct measurement of its actual evaluated-prompt-token count at `num_ctx=16,384`. Generalizing "the same headroom-freeing mechanism likely applies to the other 16–18 flagged fixtures" is an *inference* from the correlation pattern and structural checks, not a per-fixture measurement — those other fixtures' true evaluated-prompt-token counts were never directly probed.
- The chars/token ratio (3.491) carries its own ±8.7%-measured (stated here as ±~10%) calibration error on top of the mechanism issue in §3 — every `est_prompt`/`est_budget` figure in this file is an **estimate**, not a measurement. Only `eval_count`, `done`, the presence/absence of `<think>` tags, code-fence balance, and the three probe anchors (13,853 / 8,194 / 16,447 tokens) are **measurements**.
- This inherits the probe's own version caveat: it characterizes today's Ollama `v0.32.15` behavior; the exact server build the historical rows ran on is not re-verified.
- Effective sample size for the correlation checks is closer to 33 (distinct fixture contents) than 99: per-fixture `eval_count` is fairly stable across the three eras (e.g. `multistep-form-error-clearing`: 3,181 / 2,278 / 2,355), suggesting fixture content — not per-run sampling noise — drives most of the variance the correlations pick up.
- Nothing here bears on the perspective-audit suite (ran at `num_ctx=32,768`, excluded by design) or on any other model/tokenizer.

## 6. Reproduction

Ported stripping logic, calibration, and per-row computation: `analyze_clipping.py` (scratch space, not committed — logic reproduced inline in §1.2–1.3 above for anyone re-deriving this without the script). Full per-row data (est_prompt/est_budget/eval_count/flags for all 99 rows) available on request by re-running the same ported functions against `evals/suites/a11y-critic/fixtures/*.md` and the response JSONs cited above; no new fixture or response files were created or modified to produce this analysis.
