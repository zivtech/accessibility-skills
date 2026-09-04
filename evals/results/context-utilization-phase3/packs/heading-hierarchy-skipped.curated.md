## Evidence Digest

**def_rev**: 2026-08-26a
**Question (verbatim)**: Based on evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/013-127-0-0-1-8777-heading-hierarchy-skipped-html.json (axe-core scan) and evals/results/context-utilization-phase3/raw/heading-hierarchy-skipped-kat-census/sr-census.json (keyboard-a11y-tester screen-reader reading-order census), and the tool that produced each (keyboard-a11y-tester driven trace / keyboard-a11y-tester batch-crawl findings / keyboard-a11y-tester screen-reader reading-order census / axe-core scan): does this evidence set show any interaction defect (focus not reaching or leaving an element as expected, an ARIA state changing with no accessible announcement, a keyboard-operability failure) and does it show any structural defect (a missing or incorrect ARIA role, landmark, label, or heading-order violation) for the component these artifacts describe?
**question_source**: Phase 3 pack curation — authored by a fresh agent from artifact filenames and tool types only; no fixture metadata, rubrics, ground-truth files, or lane README consulted
**Evidence class**: mixed —
- "focus not reaching or leaving an element as expected" → `focus-order-indicator`
- "ARIA state changing with no accessible announcement" → `name-role-state`
- "keyboard-operability failure" → `keyboard-operability`
- "missing or incorrect ARIA role, landmark, label, or heading-order violation" → `machine-detectable`

**Answerable from artifacts read**: partially — `machine-detectable` sub-question: yes, directly. The three interaction sub-questions (`focus-order-indicator`, `name-role-state`, `keyboard-operability`): no — per `.claude/skills/a11y-test/SKILL.md`'s verification evidence contract, their prescribed instruments are a real-keyboard Playwright transcript, a keyboard-a11y-tester **driven focus trace**, and **virtual-screen-reader** assertion output, respectively. Neither supplied artifact is any of those three.

### Observations

**1. axe-core reports a `heading-order` violation**
```
observation_id: axe-heading-order-violation
source: axe-core 4.13.0 (per artifact's own `axe_core_version` field), evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/013-127-0-0-1-8777-heading-hierarchy-skipped-html.json
handle: artifact path + jq: .viewports."1280x800".violations[] (recipe: references/evidence-extraction.md §1)
actual_behavior: axe-core flags rule "heading-order", impact "moderate", 1 node, sample selector "h3:nth-child(2)". help text (verbatim): "Heading levels should only increase by one."
wcag_or_apg: not stated in artifact (only axe tags cat.semantics/best-practice; no WCAG SC field in this schema)
evidence: |
  $ jq -r '.viewports|to_entries[]|.key as $vp|.value.violations[]?|[$vp,.id,.impact,.node_count,(.sample_selectors[0]//"-")]|@tsv' <axe-file>
  1280x800  heading-order  moderate  1  h3:nth-child(2)
  "help": "Heading levels should only increase by one"
```

**2. axe-core reports a `landmark-one-main` violation**
```
observation_id: axe-landmark-one-main-violation
source: axe-core 4.13.0, same artifact as above
handle: artifact path + jq: .viewports."1280x800".violations[]
actual_behavior: rule "landmark-one-main", impact "moderate", 1 node, sample selector "html". help text (verbatim): "Document should have one main landmark."
wcag_or_apg: not stated in artifact
evidence: |
  1280x800  landmark-one-main  moderate  1  html
  "help": "Document should have one main landmark"
```

**3. axe-core reports a `region` violation**
```
observation_id: axe-region-violation
source: axe-core 4.13.0, same artifact as above
handle: artifact path + jq: .viewports."1280x800".violations[]
actual_behavior: rule "region", impact "moderate", 1 node, sample selector "#root". help text (verbatim): "All page content should be contained by landmarks." Note: this rule's own `tags` array includes "cat.keyboard" alongside "best-practice" — axe's internal rule-taxonomy label, not a record of any keyboard interaction being tested.
wcag_or_apg: not stated in artifact
evidence: |
  1280x800  region  moderate  1  #root
  "help": "All page content should be contained by landmarks"
  "tags": ["cat.keyboard","best-practice","RGAAv4","RGAA-9.2.1"]
```

**4. KAT reading-order census: heading levels skip in document reading order**
```
observation_id: kat-census-heading-level-sequence
source: keyboard-a11y-tester screen-reader reading-order census — tool name/version not self-declared inside the JSON body itself; identification rests on directory name `heading-hierarchy-skipped-kat-census` + file name `sr-census.json` + schema shape (entries keyed by spoken_phrase/role/tag/selector, plus declared_live_regions/declared_broken_aria_refs/declared_alternate_reading_order/truncated fields — matches none of the driven-trace step_id/action schema or batch-crawl finding_id/severity schema), evals/results/context-utilization-phase3/raw/heading-hierarchy-skipped-kat-census/sr-census.json
handle: artifact path + jq: .["http://127.0.0.1:8777/heading-hierarchy-skipped.html"].entries[] | select(.role=="heading")
actual_behavior: the census's reading-order walk lists 7 heading entries with levels, in this order: level 1 (index 3), level 3 (index 4), level 3 (index 8), level 3 (index 12), level 3 (index 24), level 2 (index 25), level 2 (index 29) — no level-2 heading appears between the level-1 and the four level-3 headings. Caveat: axe's violation (#1) cites selector "h3:nth-child(2)" (counts all sibling element types); this census uses ":nth-of-type" (counts only same-tag siblings). Without the raw HTML (not supplied), this digest does not assert the two selectors name the same DOM node.
wcag_or_apg: not stated in artifact
evidence: |
  {"index":3,"spoken_phrase":"heading, Introduction to Web Accessibility, level 1","tag":"h1"}
  {"index":4,"spoken_phrase":"heading, Why Accessibility Matters, level 3","tag":"h3"}
  {"index":8,"spoken_phrase":"heading, WCAG Guidelines, level 3","tag":"h3"}
  {"index":12,"spoken_phrase":"heading, Common Issues, level 3","tag":"h3"}
  {"index":24,"spoken_phrase":"heading, Getting Started, level 3","tag":"h3"}
  {"index":25,"spoken_phrase":"heading, Tools and Resources, level 2","tag":"h2"}
  {"index":29,"spoken_phrase":"heading, Conclusion, level 2","tag":"h2"}
```

**5. KAT reading-order census records zero interactive-role entries**
```
observation_id: kat-census-no-interactive-roles
source: same artifact as observation 4
handle: artifact path + jq: .["..."].entries[] | select(.tag != null) | [.role,.tag]
actual_behavior: across all 33 census entries, the only (role, tag) pairs with a real DOM tag are: document/body, article/article, heading/h1, heading/h2, heading/h3, paragraph/p, list/ul, listitem/li (plus their "end of X" boundary markers). No entry carries an interactive role (button, link, textbox, checkbox, combobox, menuitem, etc.).
wcag_or_apg: not stated in artifact
evidence: |
  document  body
  article   article
  heading   h1
  heading   h2
  heading   h3
  paragraph p
  list      ul
  listitem  li
```

### Absence claims (queries that returned nothing)

- No focus-movement, key-press, or keyboard-action records in either artifact — query `grep -ioE "focus|keydown|keypress|aria-live|tabindex|keyboard"` on both files → axe file matches only the substring "keyboard" inside the `region` rule's own `tags` array value (see obs. 3), not an interaction record; sr-census.json → empty
- No live regions declared/found by the census — query `jq -c '.[...].declared_live_regions'` on sr-census.json → `[]`
- No broken ARIA references declared/found by the census — query `jq -c '.[...].declared_broken_aria_refs'` on sr-census.json → `[]`
- No alternate reading order declared/found by the census — query `jq -c '.[...].declared_alternate_reading_order'` on sr-census.json → `[]`
- No `incomplete` (needs-review) results from axe-core — query `jq '.viewports."1280x800".incomplete'` on the axe file → `[]`

## Coverage Note

| Artifact | Partition | Scope / reason |
|---|---|---|
| evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/013-127-0-0-1-8777-heading-hierarchy-skipped-html.json | READ | full (1,902 bytes) |
| evals/results/context-utilization-phase3/raw/heading-hierarchy-skipped-kat-census/sr-census.json | READ | full (7,086 bytes) |
| evals/results/context-utilization-phase3/raw/heading-hierarchy-skipped-kat-census/session.json | NOT READ | out of question scope — sibling file discovered only via directory listing (472 bytes) while inventorying the named path's directory; not named in the prompt, content never opened. May carry tool/version provenance for observation 4/5's identification; unavailable to this digest. |

**Not claimed**: This digest does not establish presence *or* absence of `keyboard-operability`, `focus-order-indicator`, or `name-role-state` defects for this component — neither supplied artifact is the prescribed instrument for those classes (Playwright keyboard transcript / KAT driven focus trace / virtual-screen-reader assertion output). The census's empty `declared_live_regions`/`declared_broken_aria_refs`/`declared_alternate_reading_order` fields and its zero interactive-role entries are informational, not a substitute for that missing instrumentation — this census walks a page whose captured content has no interactive controls at all, on a URL where no driven interaction was recorded either way. Also not established: WCAG success-criterion mapping (neither artifact states one), whether axe's `h3:nth-child(2)` and the census's `h3:nth-of-type(...)` selectors name the same DOM node, and anything about `session.json`'s contents.