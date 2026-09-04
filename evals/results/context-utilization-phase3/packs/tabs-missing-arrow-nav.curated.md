## Evidence Digest

**def_rev**: 2026-08-26a
**Question (verbatim)**: Based on evals/results/keyboard-a11y-tester/driven/tabs-missing-arrow-nav.trace.json and the padding corpus evals/results/keyboard-a11y-tester/findings/*.json (~30+ files, with findings/tabs-missing-arrow-nav.json excluded from this fixture's evidence by pack policy), and the tool that produced each (keyboard-a11y-tester driven trace / keyboard-a11y-tester batch-crawl findings / axe-core scan): does this evidence set show any interaction defect (focus not reaching or leaving an element as expected, an ARIA state changing with no accessible announcement, a keyboard-operability failure) and does it show any structural defect (a missing or incorrect ARIA role, landmark, label, or heading-order violation) for the component these artifacts describe?
**question_source**: Phase 3 pack curation — authored by a fresh agent from artifact filenames and tool types only; no fixture metadata, rubrics, ground-truth files, or lane README consulted
**Evidence class**: mixed — "focus not reaching or leaving an element as expected" → `focus-order-indicator`; "an ARIA state changing with no accessible announcement" → `name-role-state`; "a keyboard-operability failure" → `keyboard-operability`; "a missing or incorrect ARIA role, landmark, label, or heading-order violation" → `machine-detectable`
**Answerable from artifacts read**: partially — direct hit for the `focus-order-indicator` sub-question only; the other three sub-questions have no canonically-matching instrument in this evidence set (see Absence claims)

### Observations

**1. Trace: two arrow-key presses on the focused tab do not move focus**
```
observation_id: trace-arrowkeys-no-focus-move
source: keyboard-a11y-tester driven trace (per caller framing; tool name/version not self-declared in file content) — evals/results/keyboard-a11y-tester/driven/tabs-missing-arrow-nav.trace.json
handle: tabs-missing-arrow-nav.trace.json — jq '.steps[]|{step_id,keystroke_sent,active_element_selector,focus_moved}'
actual_behavior: step_0002 (keystroke ArrowRight) and step_0003 (keystroke ArrowLeft) both keep active_element_selector at #tab-overview with focus_moved:false; step_0001 and step_0004 (both keystroke Tab) show focus_moved:true.
wcag_or_apg: not stated in artifact
evidence: |
  {"step_id":"step_0001","keystroke":"Tab","selector":"#tab-overview","focus_moved":true}
  {"step_id":"step_0002","keystroke":"ArrowRight","selector":"#tab-overview","focus_moved":false}
  {"step_id":"step_0003","keystroke":"ArrowLeft","selector":"#tab-overview","focus_moved":false}
  {"step_id":"step_0004","keystroke":"Tab","selector":"body","focus_moved":true}
```

**2. Trace: the focused tab's AX states and SR announcements are unchanged across both arrow-key steps**
```
observation_id: trace-tab-states-and-announcement-stable
source: keyboard-a11y-tester driven trace (per caller framing) — evals/results/keyboard-a11y-tester/driven/tabs-missing-arrow-nav.trace.json
handle: same file — jq '.steps[]|{step_id,states:.ax_name_role_state.states}' / '.steps[]|{step_id,sr_announcement}'
actual_behavior: the states dict for #tab-overview (role "tab", name "Overview") is byte-identical at step_0001–step_0003; sr_announcement.focus_announcement is non-null only at step_0001, null at every later step, and live_announcements is empty at every step.
wcag_or_apg: not stated in artifact
states: |
  {"step_id":"step_0001","states":{"invalid":"false","focusable":true,"focused":true,"selected":true,"controls":"panel-overview"}}
  {"step_id":"step_0002","states":{"invalid":"false","focusable":true,"focused":true,"selected":true,"controls":"panel-overview"}}
  {"step_id":"step_0003","states":{"invalid":"false","focusable":true,"focused":true,"selected":true,"controls":"panel-overview"}}
  {"step_id":"step_0004","states":{}}
evidence: |
  {"step_id":"step_0001","sr_announcement":{"new_phrases":["document","tab, Overview, selected, 1 control, position 1, set size 3"],"live_announcements":[],"focus_announcement":"tab, Overview, selected, 1 control, position 1, set size 3"}}
  {"step_id":"step_0002","sr_announcement":{"new_phrases":[],"live_announcements":[],"focus_announcement":null}}
  {"step_id":"step_0003","sr_announcement":{"new_phrases":[],"live_announcements":[],"focus_announcement":null}}
  {"step_id":"step_0004","sr_announcement":{"new_phrases":[],"live_announcements":[],"focus_announcement":null}}
```

**3. Scope fact: the findings corpus contains no file for the trace's own component**
```
observation_id: findings-corpus-excludes-trace-component
source: caller instruction + directory listing — evals/results/keyboard-a11y-tester/findings/
handle: ls evals/results/keyboard-a11y-tester/findings/*.json (33 matched) vs. the 32 files actually queried
actual_behavior: the glob matches 33 files; findings/tabs-missing-arrow-nav.json (the only filename matching the trace's component) was withheld per caller-stated pack policy and not read. The 32 in-policy files name 32 distinct other components/pages (accordion, app dashboard, async form, breadcrumb nav, modal, pagination, tabs-incomplete-aria-selected, video player, etc.) — none named "tabs-missing-arrow-nav."
wcag_or_apg: not stated in artifact
evidence: |
  findings/tabs-missing-arrow-nav.json  122 bytes  [NOT READ — pack policy]
  findings/tabs-incomplete-aria-selected.json  1707 bytes  [different fixture, READ]
  findings/tabbed-nav-vs-tab-pattern.json  122 bytes  [different fixture, READ]
```

**4. Findings corpus: interaction-defect-shaped rows exist, but in other components**
```
observation_id: findings-corpus-interaction-shaped-rows
source: keyboard-a11y-tester batch-crawl findings (per caller framing; each finding row carries "source":"deterministic") — evals/results/keyboard-a11y-tester/findings/*.json
handle: jq '.findings[]|select(.id=="sr-live-region-silent-desktop" or .id=="positive-tabindex-desktop")' across the 32 in-policy files
actual_behavior: 6 of 29 finding rows are interaction-defect-shaped: sr-live-region-silent-desktop (wcag 4.1.3) in 5 files (async-form-vague-success, form-field-vs-summary-errors, multistep-form-error-clearing, search-focus-stays-in-input, search-results-dynamic-clean); positive-tabindex-desktop (wcag 2.4.3) in 1 file (app-focus-order-illogical). None of the 5 files is the trace's component.
wcag_or_apg: "4.1.3" (sr-live-region-silent-desktop) / "2.4.3" (positive-tabindex-desktop), both verbatim from artifact
evidence: |
  {"src":"async-form-vague-success.json","wcag":"4.1.3","severity":"moderate","summary":"1 declared live region(s) … never produced an announcement during this session: #root > div > div"}
  {"src":"app-focus-order-illogical.json","wcag":"2.4.3","severity":"moderate","summary":"2 element(s) use a positive tabindex, forcing a manual tab order: #root > div > button[tabindex=1], #root > div > button[tabindex=1]"}
```

**5. Findings corpus: structural-defect-shaped rows exist, but in other components and from a different tool than axe-core**
```
observation_id: findings-corpus-structural-shaped-rows
source: keyboard-a11y-tester batch-crawl findings (per caller framing; "source":"deterministic" on every row — not an axe-core rule ID) — evals/results/keyboard-a11y-tester/findings/*.json
handle: jq '.findings[]|select(.id=="sr-heading-skip-desktop" or .id=="missing-accessible-name-desktop" or .id=="no-skip-link-desktop")' across the 32 in-policy files
actual_behavior: 4 of 29 rows are structural-defect-shaped: sr-heading-skip-desktop (wcag 1.3.1) in 2 files (dashboard-heading-inconsistency, heading-hierarchy-skipped); missing-accessible-name-desktop (wcag 4.1.2, severity "serious") in 1 file (tabs-incomplete-aria-selected — a different tabs fixture); no-skip-link-desktop (wcag 2.4.1) in 1 file (pagination-no-nav-landmark). None of these 4 files is the trace's component.
wcag_or_apg: "1.3.1" / "4.1.2" / "2.4.1", verbatim from artifact
evidence: |
  {"src":"heading-hierarchy-skipped.json","wcag":"1.3.1","summary":"1 heading level skip(s) … (jumping past one or more levels): heading, Why Accessibility Matters, level 3"}
  {"src":"tabs-incomplete-aria-selected.json","wcag":"4.1.2","summary":"1 focusable control(s) have no accessible name: tabpanel at #panel-1"}
  {"src":"pagination-no-nav-landmark.json","wcag":"2.4.1","summary":"No \"skip to main content\" style link was found among the first focus stops."}
```

**6. Findings corpus: focus-appearance-weak-desktop is near-ubiquitous but answers neither question clause**
```
observation_id: findings-corpus-focus-appearance-off-clause
source: keyboard-a11y-tester batch-crawl findings — evals/results/keyboard-a11y-tester/findings/*.json
handle: jq '.findings[]|select(.id=="focus-appearance-weak-desktop")' across the 32 in-policy files
actual_behavior: 19 of 32 in-policy files (19 of 29 total finding rows) carry this id, wcag "2.4.13", conformance_level "AAA". It describes focus-indicator area/contrast falling short of the AAA bar, not focus failing to move and not a role/landmark/label/heading defect.
wcag_or_apg: "2.4.13", verbatim from artifact
evidence: |
  "summary": "6 focus stop(s) have a visible indicator that does not meet the AAA Focus Appearance bar (>= 2px-perimeter area and >= 3:1 contrast). Informative only. …"
  "persona_impact": "The focus indicator is present but may be hard to perceive for low-vision users."
```

### Absence claims (queries that returned nothing)

- No step in the trace shows an AX-state change with zero announcement — query `states[i] != states[i-1] and live_announcements==[]` on `tabs-missing-arrow-nav.trace.json` → empty (states never change in this trace; see Obs. 2)
- No incorrect role or missing name is shown for the trace's own focused element — `#tab-overview` reports `role:"tab"`, `name:"Overview"` at every step captured
- No file for the trace's own component (`tabs-missing-arrow-nav`) exists among the 32 in-policy findings files — the one matching filename is the excluded row
- No axe-core artifact of any kind (result file, `summary.json`, or reference to one) is present in this evidence set, despite the question naming "axe-core scan" as a candidate producer
- No virtual-screen-reader assertion output (the SKILL.md contract's canonical `name-role-state` instrument) is present in this evidence set
- No real-keyboard `npx playwright test` transcript (the SKILL.md contract's canonical `keyboard-operability` instrument) is present in this evidence set

## Coverage Note

| Artifact | Partition | Scope / reason |
|---|---|---|
| evals/results/keyboard-a11y-tester/driven/tabs-missing-arrow-nav.trace.json | READ | full (6536 bytes, 4 steps; under 30KB threshold) |
| evals/results/keyboard-a11y-tester/findings/*.json (33 matched) | PARTIAL | 32 read — query-scoped: `jq '.findings[]?.id'` and `jq '.findings\|length'` looped over all 32, plus full `jq '.'` pulled on 6 files for verbatim quotes; 1 not read — findings/tabs-missing-arrow-nav.json, out of question scope (excluded from this fixture's evidence by pack policy per caller instruction) |

**Not claimed**: No conformance verdict, severity, or WCAG-SC mapping for the tabs-missing-arrow-nav component — that judgment is reserved for the consumer. The trace's own `ax_name_role_state`/`sr_announcement` fields are keyboard-a11y-tester's self-reported data, not the canonical `name-role-state` instrument (virtual-screen-reader assertions) per the SKILL.md Verification evidence contract table — neither exists here. No canonical `keyboard-operability` (real-keyboard Playwright transcript) or `machine-detectable` (axe-core) evidence exists in this set at all; the corpus's structural-flavored rows are keyboard-a11y-tester's own deterministic detector output, not axe-core. The findings corpus supplies zero interaction- or structural-flavored rows for the trace's own component — every non-empty row in the 32 in-policy files belongs to one of 32 other, distinct components. Whether "the component these artifacts describe" (singular, as the question frames it) is a coherent description of an evidence set combining one component's trace with 32 unrelated components' findings is left unresolved here — reported as a scope fact, not adjudicated.