# Webwright Canary Task Plan

## Task
Navigate to the WAI-ARIA APG FAQ disclosure example, find the first disclosure button, record its aria-expanded value, press Enter using Playwright's keyboard API, record the new aria-expanded value, assert they differ, and take before/after screenshots.

## Critical Points

1. **CP1**: Page loads successfully at https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-faq/
2. **CP2**: First disclosure button is located (selector confirmed via exploration)
3. **CP3**: aria-expanded value is read BEFORE keyboard interaction (expected: "false")
4. **CP4**: Button receives keyboard focus before Enter is pressed
5. **CP5**: Enter is dispatched via `locator.press("Enter")` — real CDP keyboard event, NOT synthetic dispatchEvent
6. **CP6**: aria-expanded value is read AFTER keyboard interaction (expected: "true")
7. **CP7**: Assertion passes: before != after
8. **CP8**: Screenshot saved before interaction
9. **CP9**: Screenshot saved after interaction

## Constraints
- Use `locator.press("Enter")` (CDP-backed real keyboard event)
- NO `page.evaluate('element.dispatchEvent(...)')` synthetic events
- Read aria-expanded via `get_attribute("aria-expanded")` before AND after
- Assert values differ

## Execution Phases
1. Explore phase: discover selector for first disclosure button, confirm aria-expanded attribute
2. Final script: instrument with log + screenshots, assert, report
