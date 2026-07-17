# bug-reporting eval suite

Measures the `bug-reporting` skill (issue #3): given a raw accessibility finding
— automated tool output, a manual testing note, or a keyboard-a11y-tester
finding — does the model produce a filable report with the skill's eight
required fields, correct aggregation, verifiable stable IDs, and honest N/A
for data the input genuinely lacks?

## Fixtures (6)

| Fixture | Input format | Difficulty | What it tests |
|---|---|---|---|
| `axe-image-alt-single` | axe-core JSON, 1 rule / 1 node | EASY | All 8 required fields from complete data; stable-ID computation |
| `axe-select-name-dedup` | axe-core JSON, 1 rule / 2 nodes + crawl context | MEDIUM | Dedup into ONE report with an instances table; frequency aggregation; per-instance stable IDs |
| `axe-two-rules-split` | axe-core JSON, 2 rules / 3 nodes | MEDIUM | Inverse-dedup: different rules → separate reports; within-rule node aggregation |
| `kat-focus-appearance` | keyboard-a11y-tester finding JSON | MEDIUM | Non-axe tool mapping; confidence surfacing; duplicate-selector dedup (4 evidence steps, 3 unique elements) |
| `manual-sr-finding-prose` | prose note from manual VoiceOver testing | MEDIUM-HARD | Report from unstructured input; honest N/A for rule ID; environment extracted from prose |
| `sparse-scan-adversarial` | minimal pa11y-style JSON | ADVERSARIAL | Fabrication resistance: no absolute URL, no viewport, no environment — N/A discipline under pressure |

Every fixture is a **triplet**: `fixtures/<id>.md` (the input artifact, sent to
the model verbatim), `fixtures/<id>.metadata.yaml` (machine-checkable
expectations, never sent), `rubrics/<id>.rubric.yaml` (scoring dimensions and
weights, never sent).

## Why there is no blind cut line here

Critic/planner/perspective fixtures embed answer keys below a
`## Accessibility Issues` heading that runners strip. Bug-reporting fixtures
are **inputs, not components with planted bugs** — the `.md` contains only the
raw finding an agent would actually receive, and every expectation lives in
`.metadata.yaml`/`.rubric.yaml`, which never enter a prompt. There is nothing
to strip; `strip_answer_key()` passes these files through unchanged.

## Scoring (`ollama/score_bugreport.py`, rule-based)

```
python3 ollama/score_bugreport.py <response.json> <fixture>.metadata.yaml
```

Checks, all driven by metadata:

1. **Report count** — dedup and split behavior (`expected_report_count`).
2. **Required fields** — the template's labelled rows (URL, XPath, Full DOM
   path, WCAG SC, Rule, Severity, Frequency) plus an HTML snippet section,
   per report.
3. **Key values** — expected URL / WCAG SC / rule ID / severity tokens appear
   (`must_contain`, with alternation lists where two answers are defensible,
   e.g. axe `serious` vs mapped `high`).
4. **Stable IDs** — recomputes `sha256(inputs)[:8]` from metadata-specified
   canonical inputs and requires the `PREFIX-hash` token in the response
   (should-tier: hardest skill behavior, scored but not PASS-gating).
5. **Honest N/A** — fields listed in `na_fields` must read N/A-ish
   (`N/A`, `not recorded`, `not available`, `unknown`, `not provided`) rather
   than carry a value the input never contained. This is the fabrication trap:
   inventing a browser version, OS, screen type, or rule ID the data lacks
   fails the check.
6. **Title pattern** — `(WCAG d.d.d)` in the report title (nice-tier).

Status: **PASS** (all musts, no fabrication), **WARN** (musts pass, should/nice
missed), **FAIL** (any must missed or fabrication detected).

## Running the lane

```
# one fixture, local model
python3 ollama/run_benchmark.py bugreport qwen3:32b axe-image-alt-single

# all fixtures
python3 ollama/run_benchmark.py bugreport-remaining qwen3:32b

# score
python3 ollama/score_bugreport.py /tmp/ollama-bugreport-<fixture>-<model>-response.json \
  evals/suites/bug-reporting/fixtures/<fixture>.metadata.yaml
```

The skill prompt is `.claude/skills/bug-reporting/SKILL.md` (frontmatter
stripped), same loading path as the critic/planner lanes. The lane is
analysis-only and ports to any model family the other lanes support.

## Out of scope (deliberate, from issue #3)

EARL output scoring and the external-organisation email template. Neither has
a consumer in the benchmark yet.
