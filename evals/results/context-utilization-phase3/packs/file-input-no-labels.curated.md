## Evidence Digest

**def_rev**: 2026-08-26a
**Question (verbatim)**: Based on evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/010-127-0-0-1-8777-file-input-no-labels-html.json (axe-core scan), evals/results/context-utilization-phase3/raw/file-input-no-labels-kat-driven/trace.json (keyboard-a11y-tester driven trace), and evals/results/context-utilization-phase3/raw/file-input-no-labels-kat-census/sr-census.json (keyboard-a11y-tester screen-reader reading-order census), and the tool that produced each (keyboard-a11y-tester driven trace / keyboard-a11y-tester batch-crawl findings / keyboard-a11y-tester screen-reader reading-order census / axe-core scan): does this evidence set show any interaction defect (focus not reaching or leaving an element as expected, an ARIA state changing with no accessible announcement, a keyboard-operability failure) and does it show any structural defect (a missing or incorrect ARIA role, landmark, label, or heading-order violation) for the component these artifacts describe?
**question_source**: Phase 3 pack curation — authored by a fresh agent from artifact filenames and tool types only; no fixture metadata, rubrics, ground-truth files, or lane README consulted
**Evidence class**: mixed
- "focus not reaching or leaving an element as expected" → `focus-order-indicator`
- "an ARIA state changing with no accessible announcement" → `name-role-state`
- "a keyboard-operability failure" → `keyboard-operability`
- "a missing or incorrect ARIA role, landmark, label, or heading-order violation" → `machine-detectable` (cross-checked against trace.json's captured role/name for the one element both artifacts share)

**Answerable from artifacts read**: partially — structural sub-question is clearly evidenced; interaction sub-question resolves to absence-of-evidence on 3 of 4 named failure shapes, with one part (full page focus order) outside this trace's scope (see Not claimed).

**Shared evaluation_context** (identical across all observations below; stated in artifacts, not derived): url `http://127.0.0.1:8777/file-input-no-labels.html`; axe viewport key `"1280x800"`; trace `viewport: "desktop"`, `viewport_size: {width:1280,height:800}`. trace.json `test_case_id: "127-0-0-1"` and the axe filename's `127-0-0-1-8777` segment both encode the same host:port as the shared URL.

### Observations

**1. axe-core rule `label` fired (impact: critical)**
```
observation_id: axe-label-missing-input
source: axe-core 4.13.0 (axe_core_version field) — evals/.../axe-batch-2026-08-25/010-127-0-0-1-8777-file-input-no-labels-html.json
handle: axe json, jq path .viewports["1280x800"].violations[0]
actual_behavior: rule "label" fired once, node_count 1, against selector "input".
wcag_or_apg: not stated as an SC number; tags[] include "wcag2a", "wcag412" (verbatim tokens, untranslated)
evidence: |
  {"id":"label","impact":"critical","help":"Form elements must have labels","help_url":"https://dequeuniversity.com/rules/axe/4.13/label?application=playwright","tags":["cat.forms","wcag2a","wcag412","section508","section508.22.n","TTv5","TT5.c","EN-301-549","EN-9.4.1.2","ACT","RGAAv4","RGAA-11.1.1"],"node_count":1,"sample_selectors":["input"]}
```

**2. axe-core rule `landmark-one-main` fired (impact: moderate)**
```
observation_id: axe-landmark-one-main-missing
source: axe-core 4.13.0 — same axe json path
handle: axe json, jq path .viewports["1280x800"].violations[1]
actual_behavior: rule "landmark-one-main" fired once, node_count 1, against selector "html".
wcag_or_apg: not stated in artifact (no wcag2* tag present; tags: ["cat.semantics","best-practice"])
evidence: |
  {"id":"landmark-one-main","impact":"moderate","help":"Document should have one main landmark","help_url":"https://dequeuniversity.com/rules/axe/4.13/landmark-one-main?application=playwright","tags":["cat.semantics","best-practice"],"node_count":1,"sample_selectors":["html"]}
```

**3. axe-core rule `page-has-heading-one` fired (impact: moderate)**
```
observation_id: axe-page-heading-one-missing
source: axe-core 4.13.0 — same axe json path
handle: axe json, jq path .viewports["1280x800"].violations[2]
actual_behavior: rule "page-has-heading-one" fired once, node_count 1, against selector "html".
wcag_or_apg: not stated in artifact (no wcag2* tag present; tags: ["cat.semantics","best-practice"])
evidence: |
  {"id":"page-has-heading-one","impact":"moderate","help":"Page should contain a level-one heading","help_url":"https://dequeuniversity.com/rules/axe/4.13/page-has-heading-one?application=playwright","tags":["cat.semantics","best-practice"],"node_count":1,"sample_selectors":["html"]}
```

**4. axe-core rule `region` fired (impact: moderate)**
```
observation_id: axe-region-content-outside-landmarks
source: axe-core 4.13.0 — same axe json path
handle: axe json, jq path .viewports["1280x800"].violations[3]
actual_behavior: rule "region" fired once, node_count 1, against selector "#root".
wcag_or_apg: not stated in artifact (no wcag2* tag present; tags include "RGAAv4","RGAA-9.2.1")
evidence: |
  {"id":"region","impact":"moderate","help":"All page content should be contained by landmarks","help_url":"https://dequeuniversity.com/rules/axe/4.13/region?application=playwright","tags":["cat.keyboard","best-practice","RGAAv4","RGAA-9.2.1"],"node_count":1,"sample_selectors":["#root"]}
```

**5. Trace's captured role/name for the one element it focuses is not flagged as incorrect by any artifact in this set**
```
observation_id: trace-fileinput-role-name-captured
source: attribution "keyboard-a11y-tester driven trace" per question/dir name ("-kat-driven"); no tool/version field inside trace.json itself — evals/.../file-input-no-labels-kat-driven/trace.json
handle: trace.json, step_id step_0001 and step_0003, jq path .steps[0].ax_name_role_state / .steps[2].ax_name_role_state
actual_behavior: at both step_0001 and step_0003, element "#root > div > input" has ax_name_role_state.name = "Choose File", role = "button"; states identical both visits (see states below). The axe artifact's "label" violation (obs. 1) targets the same selector family ("input") for a missing-label defect, not a role defect; no rule id in the axe violations list matches a role-token rule (aria-allowed-role, aria-valid-attr-value, etc. — id list is ["label","landmark-one-main","page-has-heading-one","region"]).
wcag_or_apg: not stated in artifact
states: {"invalid":"false","focusable":true,"focused":true}
evidence: |
  {"step_id":"step_0001","ax_name_role_state":{"name":"Choose File","role":"button","states":{"invalid":"false","focusable":true,"focused":true}}}
  {"step_id":"step_0003","ax_name_role_state":{"name":"Choose File","role":"button","states":{"invalid":"false","focusable":true,"focused":true}}}
```

**6. step_0001: Tab reaches the file input, focus_moved true, indicator visible**
```
observation_id: trace-step1-tab-reaches-fileinput
source: attribution "keyboard-a11y-tester driven trace" per question/dir name; no tool/version field in file — trace.json
handle: trace.json, step_id step_0001
actual_behavior: keystroke_sent "Tab" → active_element_selector "#root > div > input", focus_moved: true, dom_order_index 12. focus_visible: {visible:true, indicator:"outline", contrast:4.86, contrast_pass:true, aaa_pass:true, area_pass:true}. region: {landmark:null, heading:null}.
wcag_or_apg: not stated in artifact
states: {"invalid":"false","focusable":true,"focused":true}
evidence: |
  {"step_id":"step_0001","keystroke_sent":"Tab","active_element_selector":"#root > div > input","focus_moved":true,"ax_name_role_state":{"name":"Choose File","role":"button","states":{"invalid":"false","focusable":true,"focused":true}}}
```

**7. step_0002: Tab moves active element to `body`, ax role "none", name null**
```
observation_id: trace-step2-tab-reaches-body
source: attribution "keyboard-a11y-tester driven trace" per question/dir name — trace.json
handle: trace.json, step_id step_0002
actual_behavior: keystroke_sent "Tab" → active_element_selector "body", tag "body", dom_order_index -1, ax_name_role_state {name:null, role:"none", states:{}}, focus_moved: true. bounding_box, computed_focus_style, region, focused_region_screenshot, and focus_visible are all null for this step.
wcag_or_apg: not stated in artifact
states: {}
evidence: |
  {"step_id":"step_0002","keystroke_sent":"Tab","active_element_selector":"body","focus_moved":true,"ax_name_role_state":{"name":null,"role":"none","states":{}}}
```

**8. step_0003: Shift+Tab returns focus to the file input, identical AX values to step_0001**
```
observation_id: trace-step3-shifttab-returns-fileinput
source: attribution "keyboard-a11y-tester driven trace" per question/dir name — trace.json
handle: trace.json, step_id step_0003
actual_behavior: keystroke_sent "Shift+Tab" → active_element_selector "#root > div > input" again, focus_moved: true. ax_name_role_state and focus_visible values (contrast 4.86, visible true, indicator "outline") match step_0001 exactly.
wcag_or_apg: not stated in artifact
states: {"invalid":"false","focusable":true,"focused":true}
evidence: |
  {"step_id":"step_0003","keystroke_sent":"Shift+Tab","active_element_selector":"#root > div > input","focus_moved":true,"ax_name_role_state":{"name":"Choose File","role":"button","states":{"invalid":"false","focusable":true,"focused":true}}}
```

**9. sr_announcement differs between two visits to the same, state-unchanged element**
```
observation_id: trace-sr-announcement-step1-vs-step3
source: attribution "keyboard-a11y-tester driven trace" per question/dir name — trace.json
handle: trace.json, jq path .steps[0].sr_announcement and .steps[2].sr_announcement
actual_behavior: step_0001.sr_announcement = {new_phrases:["document"], live_announcements:[], focus_announcement:"document"}. step_0003.sr_announcement (same element, same ax_name_role_state.states, see obs. 5) = {new_phrases:[], live_announcements:[], focus_announcement:null}. live_announcements is [] at all 3 steps (obs. confirmed by jq: [[],[],[]]).
wcag_or_apg: not stated in artifact
evidence: |
  {"step_id":"step_0001","sr_announcement":{"new_phrases":["document"],"live_announcements":[],"focus_announcement":"document"}}
  {"step_id":"step_0003","sr_announcement":{"new_phrases":[],"live_announcements":[],"focus_announcement":null}}
```

**10. Reading-order census records 3 spoken-phrase entries, 2 with null tag/selector**
```
observation_id: census-entries-reading-order
source: attribution "keyboard-a11y-tester screen-reader reading-order census" per question/dir name ("-kat-census"); no tool/version field inside sr-census.json itself — evals/.../file-input-no-labels-kat-census/sr-census.json
handle: sr-census.json, jq path .["http://127.0.0.1:8777/file-input-no-labels.html"].entries[0..2]
actual_behavior: index1: spoken_phrase "document", role "document", tag "body", selector "body". index2: spoken_phrase "Upload file", role "Upload file", tag null, selector null. index3: spoken_phrase "File too large", role "File too large", tag null, selector null. For index2/index3, the "role" field value is identical to that entry's spoken_phrase — a prose string, not a WAI-ARIA role token — and neither entry resolves to a tag or selector. declared_live_regions, declared_broken_aria_refs, declared_alternate_reading_order are all []; truncated: false.
wcag_or_apg: not stated in artifact
evidence: |
  {"index":1,"spoken_phrase":"document","role":"document","tag":"body","selector":"body"}
  {"index":2,"spoken_phrase":"Upload file","role":"Upload file","tag":null,"selector":null}
  {"index":3,"spoken_phrase":"File too large","role":"File too large","tag":null,"selector":null}
  {"declared_live_regions":[],"declared_broken_aria_refs":[],"declared_alternate_reading_order":[],"truncated":false}
```

**11. Every recorded keystroke has focus_moved: true**
```
observation_id: trace-keystrokes-focus-moved-summary
source: attribution "keyboard-a11y-tester driven trace" per question/dir name — trace.json
handle: trace.json, jq path [.steps[].focus_moved]
actual_behavior: keystroke_sent sequence is ["Tab","Tab","Shift+Tab"]; focus_moved is true at every one of the 3 steps. Session goal (stated in artifact): "Choose a file to upload using only the keyboard and review any feedback the page gives" (goals[0].intent).
wcag_or_apg: not stated in artifact
evidence: |
  [true,true,true]
  {"id":"adhoc","intent":"Choose a file to upload using only the keyboard and review any feedback the page gives"}
```

### Absence claims (queries that returned nothing / no matching row)

- No axe violation id in this artifact matches a role-token rule family — query `.viewports["1280x800"].violations[].id` on axe json → `["label","landmark-one-main","page-has-heading-one","region"]`, none role-token-named.
- No live-region announcement is evidenced anywhere in this set — query `.steps[].sr_announcement.live_announcements` on trace.json → `[[],[],[]]`; query `.declared_live_regions` on sr-census.json → `[]`.
- No ARIA state value differs between the two recorded visits to the same element — query `.steps[0].ax_name_role_state.states, .steps[2].ax_name_role_state.states` on trace.json → both `{"invalid":"false","focusable":true,"focused":true}`.
- No step shows an unresponsive keystroke — query `[.steps[].focus_moved]` on trace.json → `[true,true,true]`.
- No `incomplete`/`passes` array entries beyond counts — axe json's `.viewports["1280x800"].incomplete` → `[]`; `.passes` key is absent (only `passes_count: 11` and `inapplicable_count: 76` are present as integers, no corresponding arrays).

## Coverage Note

| Artifact | Partition | Scope / reason |
|---|---|---|
| evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/010-127-0-0-1-8777-file-input-no-labels-html.json | READ | full (2525 bytes) |
| evals/results/context-utilization-phase3/raw/file-input-no-labels-kat-driven/trace.json | READ | full (4798 bytes) |
| evals/results/context-utilization-phase3/raw/file-input-no-labels-kat-census/sr-census.json | READ | full (735 bytes) |

**Not claimed**:
- The question's parenthetical names a 4th tool, "keyboard-a11y-tester batch-crawl findings," but no corresponding artifact path (e.g., a `findings.json`) was supplied among the 3 inputs. This digest makes no claim sourced from batch-crawl findings; none was read, and none was named to inventory.
- Tool/version provenance for trace.json and sr-census.json is not self-declared inside either file (no `tool`/`version` key at top level of either) — the keyboard-a11y-tester attribution rests on directory naming (`-kat-driven`, `-kat-census`) and the question's own labeling, not artifact content. axe-core's version (4.13.0) IS self-declared via `axe_core_version`.
- Whether focus reaching `body` after one Tab (obs. 7), the sr_announcement difference between visits (obs. 9), or the null-selector census entries (obs. 10) constitute a defect is a judgment call this digest does not make — the raw fields are reported; the "as expected" determination in the question's own phrasing is left to the consumer.
- trace.json's 3 steps are a short, goal-driven session (obs. 11's stated goal), not a full-page tab-order sweep — this artifact set cannot establish the total count of focusable elements on the page, only what this session encountered.
- trace.json references screenshot paths (`screenshots/step_0001.png`, `screenshots/step_0003.png`) that were not supplied as artifact paths and were not opened; they are inadmissible for this question's classes regardless, since no `visual-only` sub-question (layout/spacing/color) was asked.
- No SC-number mapping, severity assignment, or conformance verdict is offered — only the literal tag tokens (`wcag2a`, `wcag412`, etc.) axe-core emitted are quoted.