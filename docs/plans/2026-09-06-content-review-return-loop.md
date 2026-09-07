# Content review return loop — implementation scope

Approved by the user on 2026-09-06 after the human/agent coordination review. The user identified concurrent work in Joyus Docket. This implementation stays in accessibility-skills; Docket's source imports, assignments, decisions, workflow state, browser interface, and accessibility-edition work remain with that project.

## Selected slice

1. Repair the existing content-judgment importer: whole-input validation, incomplete drafts, explicit conflicts and supersession, retry idempotence, independent client/WCAG scopes, and optional unit revision pins.
2. Add a dependency-free offline content-review export/return path. It emits generic draft CSV tasks and a human worklist, blank return fields, source/unit/base-decision pins, and an explicit apply → merge sequence.
3. Wire Node regression tests into CI; mirror references and skill edits. Correct the stale walkthrough pointer and the incorrect claim that every unit ID changes with content.

The initial real pilot needs an actual inventory and participating humans. Software tests and fixture-generated previews are not that pilot and cannot close issue #57.

## Decisions and constraints

| Decision | Reason |
|---|---|
| No Docket code or network writes | The user's active work owns those interfaces; an ordinary CSV boundary is already sufficient to carry draft tasks |
| Use `unit_id`, not a fabricated finding fingerprint | Unratified content units are review questions, not source-adjudicated findings |
| Portable responses remain explicit | A generic tracker answer without source/unit/base-decision pins cannot safely be treated as a ratification |
| Complete legacy unpinned records stay supported and labeled | Repair current failures without silently migrating historical evidence or asserting a missing content binding |
| Incomplete direct JSONL returns remain draft; invalid input refuses before writes | Preserve deferred human work while preventing silent partial imports |
| Corrections require a predecessor decision and reason | Retain history and distinguish reconsideration from concurrent disagreement |
| New wrapper returns require actual observation text and exact snapshot pins | Prevent name-only completion and reuse after content changes under stable IDs |
| Whole snapshot pin in the first wrapper | Conservative, visible invalidation; finer dependency-based reuse requires its own evidence and tests |
| Cooperative lock plus atomic history replacement | Coordinate this CLI's writers without pretending to provide database transactions for unrelated editors |

## Validation and review

The implementation is tested against malformed middle lines, missing decision/date, contradictory reviewers, invalid units/scopes/pins, complete legacy records, client scope separation, retries, reasoned supersession, draft completion/withdrawal, stale source, whole-response refusal, and concurrent return conflicts. The new wrapper's tests exercise the real CLI and builder using temporary synthetic inventories.

Independent critic review found duplicate IDs in the direct merge could apply one decision to two source observations; centralized inventory validation and a no-output-change regression now prevent that. Stale artifact prose that called every row unratified, and ambiguous skill prose that equated ratification with a criterion outcome, were corrected. The final bounded critic verdict was **ACCEPT**.

Local verification on 2026-09-06: **27/27 regression tests** passed via `node --test scripts/test_ratification_import.mjs scripts/test_content_review_loop.mjs`. Node's coverage run reported 97.33% line / 93.50% branch coverage for `ratification-import.mjs` and 100% line / 75% branch coverage for `review-content-judgments.mjs`. These are module-specific figures, not a claim of inventory-builder or repository-wide coverage.

All existing CI command equivalents passed locally: client-reference scan and self-test, Python compile, fixture/registry validation, retained run manifests and their tests, skill lint, scorer smoke, blind guard and self-test, mirror parity and self-test. The staged diff passed Gitleaks and whitespace checks. Remote CI has not run for this branch. A fixture-generated worklist preview has no applied human responses and is explicitly synthetic.

## Human pilot handoff

Once the real inventory and reviewers are named, generate a bundle with the commands in the [return-loop reference](../../.claude/skills/a11y-content-judgment/references/content-review-return-loop.md). Use the existing tracker for assignment and deciding-check ownership. Preserve source observations, human responses, and any contrary reviews separately. Measure handling time alongside clarification, duplicate work, rejected stale/incomplete returns, and observation-quality corrections.

This slice neither promotes the candidate skill nor changes fix-closure attestation, admissibility, or report outcome semantics.
