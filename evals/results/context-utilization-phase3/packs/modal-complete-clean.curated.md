## Evidence Digest

**def_rev**: 2026-08-26a
**Question (verbatim)**: Based on evals/results/keyboard-a11y-tester/driven/modal-complete-clean.trace.json and the tool that produced each (keyboard-a11y-tester driven trace / keyboard-a11y-tester batch-crawl findings / axe-core scan): does this evidence set show any interaction defect (focus not reaching or leaving an element as expected, an ARIA state changing with no accessible announcement, a keyboard-operability failure) and does it show any structural defect (a missing or incorrect ARIA role, landmark, label, or heading-order violation) for the component these artifacts describe?
**question_source**: Phase 3 pack curation — authored by a fresh agent from artifact filenames and tool types only; no fixture metadata, rubrics, ground-truth files, or lane README consulted
**Evidence class**: mixed — "focus not reaching or leaving an element as expected" = `focus-order-indicator`; "an ARIA state changing with no accessible announcement" = `name-role-state`; "a keyboard-operability failure" = `keyboard-operability`; "missing or incorrect ARIA role, landmark, label, or heading-order violation" = `machine-detectable`
**Answerable from artifacts read**: partially — only 1 of the 3 tool outputs the question names was actually supplied (see Coverage Note)

**evaluation_context** (stated once, verbatim from the artifact's top level, applies to all observations below): `mode:"driven-live"`, `personas:["keyboard","screen-reader"]`, `goals:[{"id":"adhoc","intent":"open the settings modal, then close it, verifying focus management"}]`, `start_url:"http://127.0.0.1:8777/modal-complete-clean.html"`, `viewport:"desktop"`, `viewport_size:{"width":1280,"height":800}`.

**Fields not stated in artifact for any observation below** (omitted per-block rather than repeated 5×): `finding_id`, `baseline_test`, `reproduction_steps` (producing command).

### Observations

**1. [focus-order-indicator] focus_moved is true and a distinct active element is recorded at every one of the 6 steps**
```
observation_id: focus-sequence-full-trace
source: keyboard-a11y-tester (mode "driven-live"; tool version/pin not stated in artifact), evals/results/keyboard-a11y-tester/driven/modal-complete-clean.trace.json
handle: modal-complete-clean.trace.json — jq '.steps[] | {step_id, keystroke_sent, active_element_selector, focus_moved, is_body}'
actual_behavior: focus_moved is true and is_body is false at all 6 steps; active_element_selector differs step-to-step across keystrokes Tab/Enter/Tab/Tab/Tab/Escape, shown below.
wcag_or_apg: not stated in artifact
evidence: |
  {"step_id":"step_0001","keystroke_sent":"Tab","active_element_selector":"#root > div > button"}
  {"step_id":"step_0002","keystroke_sent":"Enter","active_element_selector":"body > div:nth-of-type(2) > div > div:nth-of-type(1) > button"}
  {"step_id":"step_0003","keystroke_sent":"Tab","active_element_selector":"body > div:nth-of-type(2) > div > div:nth-of-type(2) > button"}
  {"step_id":"step_0004","keystroke_sent":"Tab","active_element_selector":"body > div:nth-of-type(2) > div > div:nth-of-type(1) > button"}
  {"step_id":"step_0005","keystroke_sent":"Tab","active_element_selector":"body > div:nth-of-type(2) > div > div:nth-of-type(2) > button"}
  {"step_id":"step_0006","keystroke_sent":"Escape","active_element_selector":"#root > div > button"}
```

**2. [focus-order-indicator] Focus-indicator area_pass/aaa_pass flags differ across two visits to the same two elements within this one trace**
```
observation_id: focus-indicator-area-pass-inconsistent
source: keyboard-a11y-tester (mode "driven-live"), evals/results/keyboard-a11y-tester/driven/modal-complete-clean.trace.json
handle: modal-complete-clean.trace.json — jq '.steps[] | {step_id, active_element_selector, area_pass: .focus_appearance.area_pass, aaa_pass: .focus_appearance.aaa_pass}'
actual_behavior: area_pass/aaa_pass are false at step_0003 and step_0006, true at the other 4. The "Save changes" button (same active_element_selector) is area_pass:false at step_0003 but area_pass:true at step_0005. The "Open settings" button (same selector) is area_pass:true at step_0001 but area_pass:false at step_0006. focus_visible.visible and focus_appearance.contrast_pass are true at all 6 steps.
wcag_or_apg: not stated in artifact
evidence: |
  [{"step_id":"step_0001","active_element_selector":"#root > div > button","area_pass":true,"aaa_pass":true},{"step_id":"step_0002","active_element_selector":"body > div:nth-of-type(2) > div > div:nth-of-type(1) > button","area_pass":true,"aaa_pass":true},{"step_id":"step_0003","active_element_selector":"body > div:nth-of-type(2) > div > div:nth-of-type(2) > button","area_pass":false,"aaa_pass":false},{"step_id":"step_0004","active_element_selector":"body > div:nth-of-type(2) > div > div:nth-of-type(1) > button","area_pass":true,"aaa_pass":true},{"step_id":"step_0005","active_element_selector":"body > div:nth-of-type(2) > div > div:nth-of-type(2) > button","area_pass":true,"aaa_pass":true},{"step_id":"step_0006","active_element_selector":"#root > div > button","area_pass":false,"aaa_pass":false}]
```

**3. [name-role-state — SUBSTITUTION FLAG] ax_name_role_state.states is static across the whole trace; no toggling ARIA state is captured**
```
observation_id: aria-states-static-no-transition
source: keyboard-a11y-tester (mode "driven-live"), evals/results/keyboard-a11y-tester/driven/modal-complete-clean.trace.json — this is the trace tool's own self-reported AX snapshot, NOT output from virtual-screen-reader assertions, the instrument SKILL.md's Verification evidence contract names for the name-role-state class
handle: modal-complete-clean.trace.json — jq '.steps[].ax_name_role_state.states' / jq '.steps[].sr_announcement'
actual_behavior: every step's ax_name_role_state.states dict is identical (query for a differing dict returns []). A whole-file grep for expanded|haspopup|aria- returns no matches. sr_announcement.focus_announcement is non-empty at all 6 steps; the only container-level (non-button) phrase in the whole trace is "dialog, Settings, modal", appearing once, in step_0002's new_phrases.
wcag_or_apg: not stated in artifact
states: {"invalid":"false","focusable":true,"focused":true}
evidence: |
  {"step_id":"step_0002","sr_announcement":{"new_phrases":["dialog, Settings, modal","button, Close dialog"],"live_announcements":[],"focus_announcement":"button, Close dialog"}}
  {"step_id":"step_0006","sr_announcement":{"new_phrases":["button, Open settings"],"live_announcements":[],"focus_announcement":"button, Open settings"}}
```

**4. [keyboard-operability — SUBSTITUTION FLAG] Each recorded keystroke co-occurs with a focus/announcement transition**
```
observation_id: keystroke-focus-pairing
source: keyboard-a11y-tester (mode "driven-live"), evals/results/keyboard-a11y-tester/driven/modal-complete-clean.trace.json — SKILL.md's Verification evidence contract names a real-keyboard `npx playwright test` transcript for keyboard-operability specifically; none was supplied here
handle: modal-complete-clean.trace.json — jq '.steps[] | {step_id, keystroke_sent, focus_moved}'
actual_behavior: keystroke_sent values are Tab (×4), Enter (×1, step_0002), Escape (×1, step_0006); focus_moved is true at all 6. Enter at step_0002 co-occurs with the dialog's only appearance in any new_phrases list; Escape at step_0006 co-occurs with active_element_selector returning to the pre-dialog trigger.
wcag_or_apg: not stated in artifact
evidence: |
  {"step_id":"step_0002","keystroke_sent":"Enter","focus_moved":true,"active_element_selector":"body > div:nth-of-type(2) > div > div:nth-of-type(1) > button"}
  {"step_id":"step_0006","keystroke_sent":"Escape","focus_moved":true,"active_element_selector":"#root > div > button"}
```

**5. [machine-detectable — SUBSTITUTION FLAG] Trace's incidental region/role fields: no landmark ever recorded; no role other than button captured; dialog container never directly focused**
```
observation_id: region-role-incidental-fields
source: keyboard-a11y-tester (mode "driven-live"), evals/results/keyboard-a11y-tester/driven/modal-complete-clean.trace.json — NOT an axe-core artifact; these are the trace tool's own per-step region/role capture, not axe rule-fired/rule-stopped findings
handle: modal-complete-clean.trace.json — jq '.steps[].region.landmark' / jq '.steps[].region.heading' / jq '.steps[].ax_name_role_state.role'
actual_behavior: region.landmark is null at all 6 steps (query for non-null landmarks returns []), including the 4 steps recorded while inside the dialog (heading:"Settings"). region.heading is null at steps 1 and 6, "Settings" (text only, no level) at steps 2-5. ax_name_role_state.role is "button" at all 6 steps (query for non-button roles returns []); the dialog container itself is never the active_element_selector in any step.
wcag_or_apg: not stated in artifact
evidence: |
  [{"step_id":"step_0001","heading":null},{"step_id":"step_0002","heading":"Settings"},{"step_id":"step_0003","heading":"Settings"},{"step_id":"step_0004","heading":"Settings"},{"step_id":"step_0005","heading":"Settings"},{"step_id":"step_0006","heading":null}]
```

### Absence claims (queries that returned nothing)

- No fail/violation/warning/error/defect/issue marker anywhere in the trace — query `grep -oiE '(fail|violat|warn|error|defect|issue)[a-z]*' modal-complete-clean.trace.json` → empty
- No `expanded`, `haspopup`, or `aria-*`-named key/value anywhere in the trace — query `grep -oE '(expanded|haspopup|aria-[a-z]+)' modal-complete-clean.trace.json` → empty
- No step's `ax_name_role_state.states` differs from `{"invalid":"false","focusable":true,"focused":true}` — query `jq -c '[.steps[]|select(.ax_name_role_state.states != {"invalid":"false","focusable":true,"focused":true})]'` → `[]`
- No step's `region.landmark` is non-null — query `jq -c '[.steps[].region.landmark|select(.!=null)]'` → `[]`
- No step's `ax_name_role_state.role` is other than "button" — query `jq -c '[.steps[].ax_name_role_state.role|select(.!="button")]'` → `[]`
- No step shows `focus_moved:false` — query `jq -c '[.steps[]|select(.focus_moved==false)]'` → `[]`

## Coverage Note

| Artifact | Partition | Scope / reason |
|---|---|---|
| evals/results/keyboard-a11y-tester/driven/modal-complete-clean.trace.json (11298 B) | READ | query-scoped: jq over `.personas`,`.goals`,`.mode`,`.start_url`,`.viewport`/`.viewport_size`, and every `.steps[]` field except the 6 `.focused_region_screenshot` path strings' target images (path text read; PNGs never opened — no sub-question here is `visual-only`) |
| evals/results/keyboard-a11y-tester/driven/modal-complete-clean.findings.json (1025 B) | NOT READ | not supplied by caller — sibling to the supplied trace in the same driven-session dir; question names "driven trace" only; content unverified |
| evals/results/keyboard-a11y-tester/findings/modal-complete-clean.json (959 B) | NOT READ | not supplied by caller — candidate match for the question's "batch-crawl findings" clause by directory/filename only; content unverified, cannot confirm it is batch-crawl output |
| evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/020-127-0-0-1-8777-modal-complete-clean-html.json (1411 B) | NOT READ | not supplied by caller — candidate match for the question's "axe-core scan" clause by directory/filename only; content unverified |
| evals/results/keyboard-a11y-tester/README.md (10131 B) | NOT READ | not supplied by caller; lane documentation sitting beside the tool's output directory — blind-reading caution applied, not opened |
| evals/results/keyboard-a11y-tester/harness/pages/modal-complete-clean.html | NOT READ | blind-reading rule — this is the eval fixture's own page source (ground truth relative to the trace, which is a tool's *observation* of this page); located during directory inventory, deliberately not opened |

**Not claimed**: This digest establishes only what `modal-complete-clean.trace.json` contains. It does **not** establish: (1) what the batch-crawl findings or axe-core scan artifacts the question names would show — neither was supplied; same-fixture-named candidates were located by directory listing and left unread. (2) Canonical name-role-state evidence — the states/announcement data here is keyboard-a11y-tester's own self-reported AX snapshot, not `virtual-screen-reader` assertion output. (3) Canonical keyboard-operability evidence — no `npx playwright test` real-keyboard transcript was supplied. (4) Canonical machine-detectable evidence — no axe-core result was read, so no rule-fired/rule-stopped-firing determination for role/landmark/label/heading-order exists in what was read, only incidental region/role fields from the focus walk. (5) Heading order — the trace captures nearest-heading *text* per step, never heading *level*, so a heading-sequence violation cannot be assessed either way. (6) The dialog container's own role/landmark/label — never the directly-focused element in any step; inferable only from one simulated announcement phrase. (7) Anything visual/layout — referenced screenshots not opened. The directory sweep also surfaced ~20 other-model benchmark-response and score files for this same fixture name (`ollama-bench-*`, `gemini-bench-*`, `scores/*.txt`) and Phase-3 pack-curation working files (`context-utilization-phase3/packs/modal-complete-clean.dump.txt` and siblings) — none opened; both categories are ground-truth-/verdict-adjacent to this exact task and out of this role's charter regardless of supply status.