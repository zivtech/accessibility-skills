# Plan 001: Establish a CI verification baseline (compile, YAML, fixtures, scorer smoke tests, mirror drift report)

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat de0031f..HEAD -- ollama/ evals/ .github/ .claude/skills/ .agents/skills/ scripts/`
> If any in-scope file changed since this plan was written, compare the
> "Current state" excerpts against the live code before proceeding; on a
> mismatch, treat it as a STOP condition.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: LOW
- **Depends on**: none
- **Category**: tests
- **Planned at**: commit `de0031f`, 2026-06-11

## Why this matters

This repo's published benchmark numbers (ollama/BENCHMARK.md) are produced by three Python scoring scripts that have **zero tests**, and the only CI is a GitHub Pages deploy (`.github/workflows/pages.yml`, triggered only on `docs/**`). A regression in `score_output.py`, `score_perspective.py`, or `score_planner.py` would silently corrupt every future benchmark number. There is also no check that the 90+ fixture YAML files parse, that fixture triplets are complete, or that the fixture lists hardcoded in two runner scripts match the filesystem. This plan creates the one-command health check every other plan's verification depends on. Plans 002 and 003 modify the scorers and runners — they must not start until this characterization baseline exists.

## Current state

- `.github/workflows/pages.yml` — the ONLY workflow. Deploys `docs/` to GitHub Pages on push to main touching `docs/**`. Do not modify it.
- `ollama/score_output.py` (244 lines) — critic scorer. Entry: `python3 ollama/score_output.py <response.json> <metadata.yaml>`. Prints `Status: PASS` / `Status: FAIL` / `Status: WARN …` on its last line. Branches on `difficulty:` from the metadata: `CLEAN` (lines 147–164), `ADVERSARIAL` (165–201), else HAS-BUGS/FLAWED (202–237).
- `ollama/score_perspective.py` (371 lines) — perspective scorer, same CLI shape. CLEAN branch at lines 271–294, HAS-BUGS at 296–364.
- `ollama/score_planner.py` (142 lines) — planner scorer, same CLI shape. Prints `Status: PASS` if ≥70% of key sections found, else `Status: NEEDS REVIEW` (line 132).
- All three scorers `import yaml` (PyYAML) — the only third-party import in the repo's Python. `ollama/run_cloud_benchmark.py` additionally does a lazy `import anthropic` inside `run_claude()` (line 221) and `import yaml` inside `build_escalation_prompt()` (line 164). No `requirements.txt` exists anywhere.
- Fixture suites and their hardcoded registries:
  - `evals/suites/a11y-critic/fixtures/` — 33 fixtures, each a triplet: `{id}.md`, `{id}.metadata.yaml`, and `../rubrics/{id}.rubric.yaml`.
  - `evals/suites/a11y-planner/fixtures/` — 25 fixtures, same triplet shape.
  - `evals/suites/perspectives/fixtures/` — 25 fixtures, same triplet shape, plus `evals/suites/perspectives/calibration/` (5 calibration pairs: `.md` + `.metadata.yaml`, no rubric).
  - `ollama/run_benchmark.py:54-80` — `ALL_PERSPECTIVE_FIXTURES` (25 ids); `:86-127` — `HAS_BUGS_FIXTURES`/`CLEAN_FIXTURES`/`FLAWED_FIXTURES`/`ADVERSARIAL_FIXTURES` composing `ALL_CRITIC_FIXTURES` (33 ids).
  - `ollama/run_cloud_benchmark.py:101-132` — a SECOND, independently maintained copy of `ALL_CRITIC_FIXTURES` and `ALL_PERSPECTIVE_FIXTURES`. These duplicates can drift from each other and from the filesystem with no alert today.
- Mirror surfaces that are supposed to stay in sync (KNOWN drift today — see plan 004):
  - `.claude/skills/{a11y-critic,a11y-planner,a11y-test,perspective-audit}/SKILL.md` ↔ `.agents/skills/<same>/SKILL.md`. The `.agents/` copy of a11y-test is missing the entire Webwright section; the `.agents/` copy of perspective-audit references a nonexistent `.Codex/` directory (lines 65–66, 159–160).
- Repo conventions: conventional commits (`feat:`, `fix:`, `docs:`, `chore:` — see `git log --oneline`). Python files are standalone scripts, stdlib + PyYAML only, no classes, flat functions, `snake_case`. Match that style in the new scripts.

### Scorer metadata schema facts (needed to author the smoke fixtures)

Confirmed by reading the scorers:

- `score_output.py` reads: `difficulty`, `fixture_id`, `notes`, `expected_findings` as a LIST of `{category: must_find|should_find|must_articulate, items: [{description, wcag}]}`.
- Keyword dispatch in `check_finding()` (`score_output.py:63-85`): a description containing `aria-describedby` yields keywords `["aria-describedby", "describedby"]`; a description containing `live region` or `announced` yields `["aria-live", 'role="alert"', "role='alert'", "live region", "status message", "4.1.3"]`. Use those two description shapes in the smoke fixture so matching is deterministic, never the fallback path.
- `score_perspective.py` reads: `difficulty`, `fixture_id`, `expected_alarm_levels` (map of perspective→LOW/MEDIUM/HIGH), `expected_verdict`, `alternate_verdicts` (CLEAN only), `expected_findings` (same list format). `check_verdict()` (`score_perspective.py:61-69`) is a bare substring scan with BLOCK checked first — **the smoke response text must not contain the letter sequences "block" or "revise" anywhere except the intended verdict**, or the characterization will pin the wrong verdict.
- `score_planner.py` reads: `fixture_id`, and `key_evaluation_criteria` (list of strings) as fallback when `expected_findings.must_have` is absent (`score_planner.py:99-101`). `SECTION_KEYWORDS` (`score_planner.py:32-81`) is keyed by EXACT criterion strings — use exact keys from that dict, e.g. `Focus trap plan (Tab, Shift+Tab behavior)` and `aria-modal="true" and aria-labelledby`.

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Python present | `python3 --version` | Python 3.10+ |
| PyYAML present | `python3 -c "import yaml; print(yaml.__version__)"` | a version prints; if `ModuleNotFoundError`, run `pip3 install pyyaml` |
| Compile check | `python3 -m py_compile ollama/*.py evals/suites/perspectives/*.py` | exit 0, no output |
| Fixture validation | `python3 scripts/validate_fixtures.py` | exit 0, summary lines (created in step 3) |
| Mirror report | `python3 scripts/check_mirrors.py` | exit 0, drift report printed (created in step 4) |
| Smoke tests | `bash scripts/smoke_scorers.sh` | exit 0, `ALL SMOKE TESTS PASSED` (created in step 5) |

All commands run from the repo root: `/Users/AlexUA_1/claude/a11y-meta-skills`.

## Scope

**In scope** (the only files you create or modify):
- `ollama/requirements.txt` (create)
- `scripts/validate_fixtures.py` (create — `scripts/` dir does not exist yet)
- `scripts/check_mirrors.py` (create)
- `scripts/smoke_scorers.sh` (create)
- `evals/suites/smoke/` (create — 8 small files, listed in step 5)
- `.github/workflows/ci.yml` (create)

**Out of scope** (do NOT touch):
- `ollama/score_*.py`, `ollama/run_*.py` — plans 002/003 change them; this plan only *characterizes* them.
- `.github/workflows/pages.yml` — working Pages deploy.
- Any file under `.claude/`, `.agents/`, `.codex/` — plan 004 territory.
- Any existing fixture/rubric/metadata file under `evals/suites/{a11y-critic,a11y-planner,perspectives}/`.
- `README.md`, `CLAUDE.md`, docs — plan 005 territory.

## Git workflow

- Branch: `advisor/001-ci-verification-baseline`
- Conventional commits, one per step, e.g. `test: add scorer smoke fixtures and runner`, `ci: add verification workflow`.
- Do NOT push or open a PR unless the operator instructed it.

## Steps

### Step 1: Create `ollama/requirements.txt`

Exact content:

```
# Third-party deps for the benchmark tooling.
# pyyaml: used by all three score_*.py scripts and build_escalation_prompt()
# anthropic: used only by run_cloud_benchmark.py claude paths (lazy import)
pyyaml>=6.0
anthropic>=0.40
```

**Verify**: `pip3 install -r ollama/requirements.txt --dry-run` → resolves without error (or plain `pip3 install -r ollama/requirements.txt` if dry-run unsupported; exit 0).

### Step 2: Confirm everything compiles today

Run: `python3 -m py_compile ollama/ollama_a11y.py ollama/run_benchmark.py ollama/run_cloud_benchmark.py ollama/score_output.py ollama/score_perspective.py ollama/score_planner.py evals/suites/perspectives/generate_fixtures.py evals/suites/perspectives/strip_bug_comments.py`

**Verify**: exit 0. If any file fails to compile, STOP — that is a pre-existing breakage to report, not to fix here.

### Step 3: Create `scripts/validate_fixtures.py`

A standalone stdlib+PyYAML script, no argparse needed. It must:

1. **YAML parse**: `yaml.safe_load()` every `*.metadata.yaml` and `*.rubric.yaml` under `evals/suites/a11y-critic/`, `evals/suites/a11y-planner/`, `evals/suites/perspectives/` (including `perspectives/calibration/`). Collect failures.
2. **Triplet completeness**: for each suite in (`a11y-critic`, `a11y-planner`, `perspectives`), compare basenames of `fixtures/*.md` vs `fixtures/*.metadata.yaml` vs `rubrics/*.rubric.yaml`. Report any id present in one set but not the others. (Calibration dir: only `.md` ↔ `.metadata.yaml` pairing — no rubrics there.) Skip non-fixture helper files: in `perspectives/`, the `.py` scripts; anything not matching the triplet pattern just gets ignored, not flagged.
3. **Registry coverage**: import the runner modules and compare their hardcoded lists to the filesystem:
   ```python
   sys.path.insert(0, os.path.join(REPO, "ollama"))
   import run_benchmark, run_cloud_benchmark
   ```
   (Safe: both modules only define constants/functions at import; their CLIs run under `__main__`.) Check all four comparisons and report any delta:
   - `run_benchmark.ALL_CRITIC_FIXTURES` vs `evals/suites/a11y-critic/fixtures/*.md` basenames
   - `run_benchmark.ALL_PERSPECTIVE_FIXTURES` vs `evals/suites/perspectives/fixtures/*.md` basenames
   - `run_cloud_benchmark.ALL_CRITIC_FIXTURES` vs `run_benchmark.ALL_CRITIC_FIXTURES` (the two in-code copies)
   - `run_cloud_benchmark.ALL_PERSPECTIVE_FIXTURES` vs `run_benchmark.ALL_PERSPECTIVE_FIXTURES`
4. Exit 1 if any YAML fails to parse or any triplet is incomplete or any registry delta exists; print a per-check summary either way. Exclude `evals/suites/smoke/` from the triplet check (smoke files are response+metadata pairs, not full triplets).

**Verify**: `python3 scripts/validate_fixtures.py` → exit 0 with summary like `YAML: 121 parsed, 0 errors / Triplets: a11y-critic 33 OK, a11y-planner 25 OK, perspectives 25 OK / Registries: 4 checks OK`. If it exits 1, read the report: if it reveals a real pre-existing mismatch (e.g. registry drift), STOP and report the exact delta — do not edit fixture lists to make it pass.

### Step 4: Create `scripts/check_mirrors.py` (report-only in this plan)

For each skill dir present in `.agents/skills/` (`a11y-critic`, `a11y-planner`, `a11y-test`, `perspective-audit`):

1. Compare the set of `## ` headings in `.claude/skills/<name>/SKILL.md` vs `.agents/skills/<name>/SKILL.md`; print headings present in one but not the other.
2. Grep the `.agents/` file for the string `.Codex/` and print any hits (these are broken paths).
3. Print a one-line diff stat (count of differing lines via `difflib.unified_diff`).
4. Also compare `references/` files under both surfaces byte-for-byte and print MATCH/DIFFER per file.
5. **Always `sys.exit(0)`** in this plan, with a final line `MODE: report-only (strict mode enabled by plan 004)`. Implement a `--strict` flag that exits 1 on any `.Codex/` hit or heading-set difference — but do not wire `--strict` into CI yet; plan 004 does that after syncing content.

**Verify**: `python3 scripts/check_mirrors.py` → exit 0; output MUST show (a) a11y-test heading drift including a missing `## Test script generation with Webwright` heading on the `.agents/` side, and (b) 4 `.Codex/` hits in `.agents/skills/perspective-audit/SKILL.md` (lines 65, 66, 159, 160). If it shows neither, your comparison logic is wrong — these drifts are confirmed to exist at commit `de0031f`.

### Step 5: Create smoke fixtures under `evals/suites/smoke/`

Create exactly these 8 files. These pin CURRENT scorer behavior (characterization) — including known quirks. Do not "improve" the scorers to make nicer fixtures possible.

`critic-hasbugs.metadata.yaml`:
```yaml
fixture_id: critic-hasbugs-smoke
difficulty: HAS-BUGS
notes: "Expected verdict: REVISE"
expected_findings:
  - category: must_find
    items:
      - description: "Input missing aria-describedby link to its error message"
        wcag: "WCAG 3.3.1"
      - description: "Error message is not announced to screen readers (no live region)"
        wcag: "WCAG 4.1.3"
```

`critic-hasbugs-response.json` (single line is fine):
```json
{"response": "Phase 1 — Scope. Phase 2 — Findings.\nFinding #1: The email input lacks aria-describedby pointing at the error text. WCAG 3.3.1.\nFinding #2: Add aria-live=\"polite\" so the failure is announced. WCAG 4.1.3.\nVerdict: REVISE"}
```

`critic-clean.metadata.yaml`:
```yaml
fixture_id: critic-clean-smoke
difficulty: CLEAN
notes: "Expected verdict: ACCEPT"
expected_findings: []
```

`critic-clean-response.json`:
```json
{"response": "Phase 1 — Scope. The component uses a native button with a visible label and logical focus order. No accessibility design gaps were identified.\nVerdict: ACCEPT"}
```
(Important: this text must not contain the words REJECT or REVISE anywhere, and contains no `Finding #N:` / `Severity:` patterns — see `score_output.py:101-124`.)

`perspective-hasbugs.metadata.yaml`:
```yaml
fixture_id: perspective-hasbugs-smoke
difficulty: HAS-BUGS
expected_verdict: REVISE
expected_alarm_levels:
  vestibular_motion: HIGH
  auditory_access: LOW
expected_findings:
  - category: must_find
    items:
      - description: "Carousel autoplay ignores prefers-reduced-motion"
        wcag: "2.3.3"
```

`perspective-hasbugs-response.json`:
```json
{"response": "Vestibular & Motion audit: the carousel autoplays and never checks prefers-reduced-motion (WCAG 2.3.3). Route to: Front-End Dev.\nVerdict: REVISE"}
```
(Constraint from `score_perspective.py:61-69`: the response must not contain the substring "block" in any casing, or the scorer's verdict detection returns BLOCK.)

`perspective-clean.metadata.yaml`:
```yaml
fixture_id: perspective-clean-smoke
difficulty: CLEAN
expected_verdict: PASS
expected_alarm_levels:
  vestibular_motion: LOW
  auditory_access: LOW
expected_findings: []
```

`perspective-clean-response.json`:
```json
{"response": "All escalated perspectives at LOW. The page is static text with system fonts and no motion or audio. No findings.\nVerdict: PASS"}
```
(Same constraint: no "block"/"revise" substrings anywhere in the text.)

`planner.metadata.yaml`:
```yaml
fixture_id: planner-smoke
key_evaluation_criteria:
  - "Focus trap plan (Tab, Shift+Tab behavior)"
  - "aria-modal=\"true\" and aria-labelledby"
```

`planner-response.json`:
```json
{"response": "## Focus management\nImplement a focus trap: Tab cycles within the dialog, Shift+Tab reverses.\n## Semantics\nUse role=\"dialog\" with aria-modal=\"true\" and aria-labelledby=\"dialog-title\".\nWCAG 2.1.1, 4.1.2.\n```html\n<dialog aria-modal=\"true\"></dialog>\n```"}
```

### Step 6: Create `scripts/smoke_scorers.sh`

Bash, `set -euo pipefail`, run from repo root. For each case, run the scorer, capture stdout, and `grep -q` the expected lines; on miss, print the full scorer output and exit 1.

| Scorer | Response / metadata | Assert stdout contains |
|--------|--------------------|------------------------|
| `ollama/score_output.py` | `critic-hasbugs-response.json` + `critic-hasbugs.metadata.yaml` | `Must-find issues: 2/2` AND `Status: PASS` |
| `ollama/score_output.py` | `critic-clean-response.json` + `critic-clean.metadata.yaml` | `Verdict correct: YES` AND `Status: PASS` |
| `ollama/score_perspective.py` | `perspective-hasbugs-response.json` + `perspective-hasbugs.metadata.yaml` | `Must-find issues: 1/1` AND `Status: PASS` |
| `ollama/score_perspective.py` | `perspective-clean-response.json` + `perspective-clean.metadata.yaml` | `Verdict: PASS` AND `Status: PASS` |
| `ollama/score_planner.py` | `planner-response.json` + `planner.metadata.yaml` | `Score: 2/2` AND `Status: PASS` |

End with `echo "ALL SMOKE TESTS PASSED"`.

**Verify**: `bash scripts/smoke_scorers.sh` → exit 0, `ALL SMOKE TESTS PASSED`. If any case fails, FIRST suspect your fixture text (keyword dispatch is picky — re-read the schema facts above), not the scorer. The scorers are out of scope to modify.

### Step 7: Create `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [main]
    paths: ['ollama/**', 'evals/**', 'scripts/**', '.claude/**', '.agents/**', '.github/workflows/ci.yml']
  pull_request:
    paths: ['ollama/**', 'evals/**', 'scripts/**', '.claude/**', '.agents/**', '.github/workflows/ci.yml']

permissions:
  contents: read

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r ollama/requirements.txt
      - name: Compile check
        run: python3 -m py_compile ollama/*.py evals/suites/perspectives/*.py
      - name: Validate fixtures and registries
        run: python3 scripts/validate_fixtures.py
      - name: Scorer smoke tests
        run: bash scripts/smoke_scorers.sh
      - name: Mirror drift report (non-blocking)
        run: python3 scripts/check_mirrors.py
```

**Verify**: `python3 -c "import yaml,sys; yaml.safe_load(open('.github/workflows/ci.yml')); print('ci.yml parses')"` → `ci.yml parses`. Then re-run all four local commands (compile, validate, smoke, mirrors) one final time → all exit 0.

## Test plan

The smoke fixtures + `smoke_scorers.sh` ARE the tests this plan adds (characterization tests for 3 untested scripts). `validate_fixtures.py` and `check_mirrors.py` are self-verifying checks; their "test" is the expected output documented in steps 3–4 (known counts: 33/25/25 triplets; known drift: Webwright heading + 4 `.Codex/` hits).

## Done criteria

ALL must hold:

- [ ] `python3 -m py_compile ollama/*.py evals/suites/perspectives/*.py` exits 0
- [ ] `python3 scripts/validate_fixtures.py` exits 0
- [ ] `bash scripts/smoke_scorers.sh` exits 0 and prints `ALL SMOKE TESTS PASSED`
- [ ] `python3 scripts/check_mirrors.py` exits 0 and its output mentions both `Webwright` (heading drift) and `.Codex/` (4 hits)
- [ ] `python3 scripts/check_mirrors.py --strict` exits 1 (strict mode works but is not wired into CI)
- [ ] `.github/workflows/ci.yml` parses as YAML
- [ ] `git status` shows changes ONLY in: `ollama/requirements.txt`, `scripts/`, `evals/suites/smoke/`, `.github/workflows/ci.yml`
- [ ] `plans/README.md` status row updated

## STOP conditions

Stop and report back (do not improvise) if:

- Any scorer behaves differently than the "Scorer metadata schema facts" section describes (e.g. `Status:` line absent, different field names) — the plan's schema notes would be stale.
- Step 3's registry check reveals a pre-existing fixture/registry mismatch — report the exact delta; do not edit `run_benchmark.py` / `run_cloud_benchmark.py` lists.
- A smoke test fails after two fixture-text adjustments — report the scorer output verbatim.
- PyYAML cannot be installed in your environment.

## Maintenance notes

- Plans 002 (scorer fixes) and 003 (runner robustness) will CHANGE behavior that these smoke tests pin. Those plans include updating the smoke expectations — a smoke failure during 002/003 is the system working as intended.
- Plan 004 flips `check_mirrors.py` into `--strict` in CI after syncing the mirrors.
- When adding a new fixture: `validate_fixtures.py` will fail CI until the triplet is complete AND both runners' hardcoded lists include it. That is the point.
- Reviewer should scrutinize: that smoke fixtures exercise the dispatch-table keyword paths (deterministic) rather than the fragile fallback split-words path.
