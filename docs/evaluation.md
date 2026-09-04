# Evaluation

This is a prompt-only repository. The skills are text, so the only way to know whether a change helped is to measure it against fixtures. Every number published here traces to a raw artifact committed under `evals/results/`.

## The suites

Counts are fixture `.md` files; each carries a `.metadata.yaml` (ground truth) and a `rubrics/*.rubric.yaml` (scoring).

| Suite | Fixtures | Grades |
|---|--:|---|
| `a11y-critic` | 50 | Component review: does it find the planted defects, and does it stay quiet on clean code |
| `a11y-planner` | 29 | Pre-implementation design plans, including an audit-scope and a declared-508 fixture |
| `perspectives` | 25 | Perspective-audit detection and alarm calibration (plus 5 calibration fixtures) |
| `bug-reporting` | 7 | Finding → filable issue, with fabrication and stable-ID checks |
| `a11y-content-judgment` | 6 | Draft-and-ratify judgments on scanner-undecidable criteria |
| `acr-reporting` | 4 | Evaluation report → OpenACR draft, validated through the pinned CLI |
| `a11y-test-operation-evidence` | 4 | Retest evidence admissibility — over- and under-rejection traps |
| `a11y-test-recipe` | 2 | Is a keyboard test recipe's recorded outcome supported by its own evidence |
| `evaluation-report` | 1 | Aggregating finished findings into the WCAG-EM-shaped report contract |

Four more directories are not fixture suites: `baseline-scan/` (a scan-rig harness), `chain/` (multi-skill chain protocol), `smoke/` (committed scorer smoke cases asserted in CI), and `webwright-benchmark/` (speed and correctness data for the script-generation mode).

Fixtures are tiered — CLEAN, HAS-BUGS, FLAWED, ADVERSARIAL — and registered in `ollama/run_benchmark.py`. That registry is the single source of truth for counts; `scripts/validate_fixtures.py` checks triplet completeness and registry↔filesystem agreement, but it does **not** scan prose, so a stale number in a document will pass CI. Fix prose counts in the same change that adds a fixture.

## Running

```bash
python3 ollama/run_benchmark.py critic-remaining qwen3.6:35b   # un-benchmarked critic fixtures
python3 ollama/run_benchmark.py single <model> <fixture-id>    # one fixture
python3 ollama/run_benchmark.py score-all                      # score critic responses
```

`ollama/run_cloud_benchmark.py` is the hosted equivalent. Full command list and result tables: [ollama/README.md](../ollama/README.md) and [ollama/BENCHMARK.md](../ollama/BENCHMARK.md).

The analysis-only skills also run standalone against a local model, no benchmark harness involved:

```bash
python3 ollama/ollama_a11y.py critic path/to/component.jsx --model qwen3.6:35b
```

`a11y-test` is **not** portable — it needs Playwright, axe-core, and a browser. Only its reference knowledge ports.

## The blind protocol

A fixture embeds its own answer key. The runners cut the file at `## Accessibility Issues` and send only what is above that line, so the answer key never reaches the model.

Leaking is the default state of that mechanism and not leaking is a discipline, which is why the rules below are machine-enforced rather than documented. `ollama/test_blind_prompts.py` builds the real prompt for **every** fixture through **both** runners and fails CI on any violation. Its `--self-test` runs first in CI, perturbing each structural check along the exact dimension it inspects to prove the check still fires.

What it enforces:

1. **No answer-key markers, hint comments, or reassurance text** in any composed prompt. Three separate regressions are behind this: runners that fed raw fixtures including the answer key (fixed 2026-07-13), inline `// BUG:` comments that survived the cut (2026-07-16), and eval-authored reassurance plus verdict-revealing Difficulty/Notes sections in the seven fixtures that had no cut line at all (2026-07-16).
2. **One cut line, spelled exactly `## Accessibility Issues`**, in every fixture of an answer-key-bearing suite — all-or-none. Annotate below the heading, never in it.
3. **Every `## ` heading declared** as visible-to-the-model or eval-side, per suite. Adding a new leak requires editing the allowlist, which is a reviewable act rather than an omission nobody sees.
4. **Every fixture H1 pinned** in [`evals/fixture-title-manifest.yaml`](../evals/fixture-title-manifest.yaml), classified `neutral`, `names-defect`, or `asserts-feature`. Line 1 is above the cut, so the title reaches the model in every lane.

### Known open leaks

The manifest and the heading allowlist declare current leaks rather than pretending they are gone. Two remain, tracked in [#51](https://github.com/zivtech/accessibility-skills/issues/51):

- **Titles.** 52 of 77 fixture H1s name the defect they plant; 6 more assert the feature under test. Measured on the nine maximum-leak critic fixtures: neutralising the title does not move must-find detection for the current recommended local model, which is already at ceiling there. That is a real result and a weak one — a saturated instrument cannot detect an effect.
- **The features section.** 45 of 50 critic fixtures show the model an `## Accessibility Features Present` section above the cut. The title names the defect; this names the non-defects; together they bracket the answer. It is realistic *content* — a developer handing over a component really would say what they handled — but its *function* in the eval is not.

A related finding from the same work, worth knowing before you trust a rubric field: `false_positive_trap` is declared in all 50 critic rubrics and read by **no scorer**. So are `llm_judge`, `hybrid_weights`, and `scoring_method`. Those rubric dimensions do not currently affect any score.

## Adding a fixture

1. Create the triplet: `{kebab-case-id}.md`, `{id}.metadata.yaml`, `rubrics/{id}.rubric.yaml`. Read existing siblings in full first and match their schema, voice, and length — house style is not documented anywhere else.
2. Build BUG and CLEAN variants **together**, not one now and one later. A suite with unmatched pairs measures the wrong thing.
3. Register the id in `ollama/run_benchmark.py` (and `run_cloud_benchmark.py` if the suite runs there).
4. Document planted defects **only** below the cut line — never as inline code comments.
5. Add a row to `evals/fixture-title-manifest.yaml` classifying the H1.
6. Scrutinise the CLEAN half as hard as the BUG half. A BUG fixture with an extra unplanted defect is recoverable; a CLEAN fixture with a real defect punishes correct reviews and is much harder to notice.
7. CLEAN fixtures carry zero real defects and three or more false-positive traps.
8. Run the gates.

```bash
python3 scripts/validate_fixtures.py           # triplets + registry
python3 ollama/test_blind_prompts.py --self-test
python3 ollama/test_blind_prompts.py           # the real gate
bash scripts/smoke_scorers.sh
python3 scripts/check_mirrors.py --strict
```

## Reading a benchmark number

Three rules, each of which was learned by getting it wrong first.

**Single-lane deltas are variance until adjudicated.** Byte-identical prompts at temperature 0.3 flip two or three items between draws. A one-draw difference is noise.

**Local models are detectors, not verdict authorities.** No local model has passed the clean-code verdict bar at any size tested through August 2026. Use them to surface candidate findings; never take a local verdict on clean code as a conclusion.

**Check what a row was assisted by.** Rows dated before 2026-07-13 ran non-blind. Rows before 2026-07-16 saw inline `BUG:` hint comments. Rows before 2026-07-19 were verdict-assisted on CLEAN fixtures. Every affected row is disclosed in [ollama/BENCHMARK.md](../ollama/BENCHMARK.md) rather than silently corrected, because the disclosure is the interesting part.

## Verifying a change

Reproduce the committed evidence-harness recipes from scratch. Do not re-run CI and call it verification — see the `verify` skill.
