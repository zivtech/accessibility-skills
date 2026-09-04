## Evidence Digest

**def_rev**: 2026-08-26a
**Question (verbatim)**: Based on evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json and the tool that produced each (keyboard-a11y-tester driven trace / keyboard-a11y-tester batch-crawl findings / axe-core scan): does this evidence set show any interaction defect (focus not reaching or leaving an element as expected, an ARIA state changing with no accessible announcement, a keyboard-operability failure) and does it show any structural defect (a missing or incorrect ARIA role, landmark, label, or heading-order violation) for the component these artifacts describe?
**question_source**: Phase 3 pack curation — authored by a fresh agent from artifact filenames and tool types only; no fixture metadata, rubrics, ground-truth files, or lane README consulted
**Evidence class**: mixed — "focus not reaching/leaving" → `focus-order-indicator`; "ARIA state changing with no announcement" → `name-role-state`; "keyboard-operability failure" → `keyboard-operability`; "structural defect (role/landmark/label/heading-order)" → `machine-detectable`
**Answerable from artifacts read**: partially

**evaluation_context** (stated in artifact, applies to all observations below): `viewport=desktop (1280×800)`, `start_url=http://127.0.0.1:8777/interactive-dropdown-focus-bug.html`, `mode=driven-live`, `personas=["keyboard","screen-reader"]`, `test_case_id=127-0-0-1`, `goals[0].intent="open the sort dropdown, move into the listbox, pick an option, verify focus returns to trigger"`

### Observations

**1. Enter on the trigger button changes captured ARIA state; no announcement recorded**
```
observation_id: expand-state-no-announcement
source: keyboard-a11y-tester (tool/format inferred from directory path and artifact's own `mode` field; version/pin not stated in artifact)
handle: evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json :: step_id=step_0002
actual_behavior: keystroke_sent="Enter", active_element_selector stays "#dropdown-btn", focus_moved:false. States go from step_0001's expanded:false to expanded:true and gain controls:"dropdown-list". sr_announcement.new_phrases is [] and sr_announcement.focus_announcement is null.
wcag_or_apg: not stated in artifact
states: {"invalid":"false","focusable":true,"focused":true,"hasPopup":"listbox","expanded":true,"controls":"dropdown-list","labelledby":{"type":"nodeList","relatedNodes":[{"backendDOMNodeId":14,"text":"Sort by"}]}}
evidence: |
  {"step_id":"step_0002","keystroke_sent":"Enter","active_element_selector":"#dropdown-btn","focus_moved":false,"states":{…},"sr_announcement":{"new_phrases":[],"live_announcements":[],"focus_announcement":null}}
```

**2. Listbox element's captured accessible name is an empty string**
```
observation_id: listbox-empty-accessible-name
source: keyboard-a11y-tester (as above)
handle: evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json :: step_id=step_0003 (also step_0004)
actual_behavior: active_element_selector="#dropdown-list", tag="ul". ax_name_role_state.name = "" (empty string), role="listbox".
wcag_or_apg: not stated in artifact
states: {"focusable":true,"focused":true,"multiselectable":false,"orientation":"vertical","required":false}
evidence: |
  {"step_id":"step_0003","active_element_selector":"#dropdown-list","ax_name_role_state":{"name":"","role":"listbox","states":{…}}}
```

**3. ArrowDown sent while focus is on the listbox produces no recorded change**
```
observation_id: arrowdown-no-observable-effect
source: keyboard-a11y-tester (as above)
handle: evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json :: step_id=step_0004
actual_behavior: keystroke_sent="ArrowDown", active_element_selector stays "#dropdown-list", focus_moved:false. Captured states are identical to step_0003 (no active-descendant or option-level field present). sr_announcement.new_phrases is [] and focus_announcement is null.
wcag_or_apg: not stated in artifact
states: {"focusable":true,"focused":true,"multiselectable":false,"orientation":"vertical","required":false}
evidence: |
  {"step_id":"step_0004","keystroke_sent":"ArrowDown","active_element_selector":"#dropdown-list","focus_moved":false,"states":{…},"sr_announcement":{"new_phrases":[],"live_announcements":[],"focus_announcement":null}}
```

**4. Enter (selection keystroke) moves the active element to `body`**
```
observation_id: focus-to-body-after-select
source: keyboard-a11y-tester (as above)
handle: evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json :: step_id=step_0005
actual_behavior: keystroke_sent="Enter" (per goals[0].intent, sent to "pick an option"). active_element_selector becomes "body", tag="body", focus_moved:true. ax_name_role_state={"name":null,"role":"none","states":{}}. region:null, bounding_box:null, computed_focus_style:null. sr_announcement fields all empty/null. The next recorded step (step_0006) reaches "#dropdown-btn" only via an explicit subsequent Shift+Tab, not automatically from step_0005.
wcag_or_apg: not stated in artifact
states: {}
evidence: |
  {"step_id":"step_0005","keystroke_sent":"Enter","active_element_selector":"body","tag":"body","focus_moved":true,"ax_name_role_state":{"name":null,"role":"none","states":{}},"region":null,"sr_announcement":{"new_phrases":[],"live_announcements":[],"focus_announcement":null}}
```

**5. Returning to the trigger button: visible text changed, accessible name/announcement did not**
```
observation_id: stale-name-after-return-to-trigger
source: keyboard-a11y-tester (as above)
handle: evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json :: step_id=step_0006
actual_behavior: keystroke_sent="Shift+Tab", active_element_selector="#dropdown-btn". text field = "Price: low to high▼" (step_0001's text was "Newest▼"). ax_name_role_state.name = "Sort by" (identical string to step_0001). sr_announcement.focus_announcement = "button, Sort by, not expanded, has popup listbox" — identical string to step_0001's focus_announcement.
wcag_or_apg: not stated in artifact
states: {"invalid":"false","focusable":true,"focused":true,"hasPopup":"listbox","expanded":false,"labelledby":{"type":"nodeList","relatedNodes":[{"backendDOMNodeId":14,"text":"Sort by"}]}}
evidence: |
  {"step_id":"step_0006","keystroke_sent":"Shift+Tab","active_element_selector":"#dropdown-btn","text":"Price: low to high▼","ax_name_role_state":{"name":"Sort by","role":"button","states":{…}},"sr_announcement":{"new_phrases":["button, Sort by, not expanded, has popup listbox"],"focus_announcement":"button, Sort by, not expanded, has popup listbox"}}
```

### Absence claims (queries that returned nothing)

- No `wcag`, `sc`, `finding*`, `severity`, or `impact` key appears anywhere in the trace file — query `grep -o '"wcag[^"]*"\|"sc"\|"finding[^"]*"\|"severity"\|"impact"' interactive-dropdown-focus-bug.trace.json` → empty.
- No landmark or heading is recorded for the focused element's region in any of the 6 steps — query `jq -c '[.steps[] | {step_id, region}]'` → `region:{"landmark":null,"heading":null}` in steps 1–4, 6; `region:null` in step 5 (scoped to the per-step focused-region field, not a page-wide landmark/heading census).

## Coverage Note

| Artifact | Partition | Scope / reason |
|---|---|---|
| evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json | READ | query-scoped: `jq keys`, `jq 'del(.steps)'`, `jq -c '.steps[]'`, per-step `jq -c` field selections (steps 2–6), `grep -o` for wcag/finding/severity/impact keys (11,107 bytes; 6 steps) |
| evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.findings.json | NOT READ | out of question scope — sibling artifact for this same fixture, observed only as a filename+size via `ls` on the parent directory while inventorying the named path; not itself named in the artifact paths handed to me; contents not opened |
| (not provided) keyboard-a11y-tester batch-crawl findings | NOT READ | out of question scope — named by tool-type in the question's parenthetical, but no artifact path for it was supplied to this reader |
| (not provided) axe-core scan | NOT READ | out of question scope — named by tool-type in the question's parenthetical, but no artifact path for it was supplied to this reader |

**Not claimed**: This digest does not establish a machine-detectable/axe-style structural verdict (landmark census, heading-order violation, full ARIA-role validity across the DOM) — no axe-core artifact was provided, and the trace's AX snapshots cover only the six elements that happened to receive focus, not a DOM-wide audit. It does not establish whether keyboard-a11y-tester batch-crawl findings exist for this component — no such artifact was supplied. It does not establish name-role-state conformance via the contract's prescribed instrument (SKILL.md's evidence table names `virtual-screen-reader` assertion output for this class) — the `sr_announcement`/`ax_name_role_state` fields above are the driven-trace tool's own simulated capture, a related but distinct evidence type. It does not establish keyboard-operability via the contract's prescribed `npx playwright test` transcript — this is a `keyboard-a11y-tester` driven-live trace, an adjacent real-keystroke record, not that canonical artifact type. No severity, WCAG/SC mapping, or defect/pass-fail judgment is asserted for any observation above — those are reserved for the consumer.