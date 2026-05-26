# Task 3c — axe-core Audit Plan

## Target
URL: https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-faq/

## Critical Points

1. **Browser**: Firefox, headless, viewport 1280x1800. No full_page screenshots.
2. **axe-core injection**: Use `page.add_script_tag(url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js")` — NOT a local file, NOT fetch().
3. **Audit execution**: `page.evaluate("axe.run(document)")` — returns a dict with `violations`, `passes`, `incomplete`, `inapplicable`.
4. **Wait strategy**: After navigation, wait for `networkidle` then inject. After injection, verify `axe` is defined before running.
5. **Output**: Parse violations for `id`, `impact`, `description`, and `nodes` count. Write to `final_runs/run_1/final_script_log.txt`.
6. **Screenshots**: Before audit and after audit (no full_page). Save to `final_runs/run_1/screenshots/`.
7. **Error handling**: Wrap evaluate() in try/except; log raw result on failure.

## Execution Steps
1. Launch Firefox headless
2. Navigate to URL, wait for networkidle
3. Screenshot: page-initial.png
4. Inject axe-core via add_script_tag
5. Verify axe is available via evaluate
6. Run axe.run(document)
7. Parse and log all violations
8. Screenshot: page-post-audit.png
9. Write log file
10. Print summary to stdout

## Output Format (log file)
- Timestamp
- URL audited
- axe-core version
- Total violation count
- Per violation: id, impact, description, affected node count, node targets
