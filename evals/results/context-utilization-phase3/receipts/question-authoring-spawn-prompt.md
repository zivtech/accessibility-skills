# Question-authoring spawn prompt — recorded verbatim (ruling 8 / README §9.6)

Recorded BEFORE spawning; the agent received exactly the text between the
`----BEGIN SPAWN PROMPT----` / `----END SPAWN PROMPT----` markers, nothing else.
Agent: fresh `general-purpose` subagent, model sonnet, spawned 2026-08-25 from the
pack-construction session. The agent had no prior conversation context, was
forbidden all tool use, and was handed only artifact paths + producing tool types
(mechanically extracted from `lane_manifest.yaml` `raw_source_note` fields per
README §9.6 — never the manifest itself, never the lane README, never any
`.metadata.yaml`).

----BEGIN SPAWN PROMPT----
You are authoring adjudication questions for a blind evidence-curation exercise.

HARD CONSTRAINTS — all binding:
- Do NOT use any tools. Do NOT read any files. Do NOT explore any repository.
  Everything you need is in this prompt; your entire output is your final message.
- You know NOTHING about these fixtures beyond the artifact filenames and tool
  types listed below. Do not guess or imply which specific defect (if any) a
  fixture contains. A question that presupposes a specific defect is invalid.
- Author exactly one question per fixture, from the artifact filenames and tool
  types alone, following the template below.

TEMPLATE (follow this two-part shape — an interaction sub-question plus a
structural sub-question; adapt the bracketed artifact list per fixture):

> Based on [the exact artifact filenames/paths listed for this fixture] and the
> tool that produced each (keyboard-a11y-tester driven trace /
> keyboard-a11y-tester batch-crawl findings / axe-core scan): does this evidence
> set show any interaction defect (focus not reaching or leaving an element as
> expected, an ARIA state changing with no accessible announcement, a
> keyboard-operability failure) and does it show any structural defect (a
> missing or incorrect ARIA role, landmark, label, or heading-order violation)
> for the component these artifacts describe?

FIXTURES AND THEIR ARTIFACT SETS (paths are repo-relative):

1. fixture_id: button-skip-link-clean
   - evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/004-127-0-0-1-8777-button-skip-link-clean-html.json (axe-core scan)

2. fixture_id: modal-complete-clean
   - evals/results/keyboard-a11y-tester/driven/modal-complete-clean.trace.json (keyboard-a11y-tester driven trace)

3. fixture_id: heading-hierarchy-skipped
   - evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/013-127-0-0-1-8777-heading-hierarchy-skipped-html.json (axe-core scan)

4. fixture_id: file-input-no-labels
   - evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/010-127-0-0-1-8777-file-input-no-labels-html.json (axe-core scan)
   - evals/results/context-utilization-phase3/raw/file-input-no-labels-kat-driven/trace.json (keyboard-a11y-tester driven trace)

5. fixture_id: tabs-missing-arrow-nav
   - evals/results/keyboard-a11y-tester/driven/tabs-missing-arrow-nav.trace.json (keyboard-a11y-tester driven trace)
   - glob: evals/results/keyboard-a11y-tester/findings/*.json (keyboard-a11y-tester batch-crawl findings corpus, ~30+ files; the file findings/tabs-missing-arrow-nav.json is excluded from this fixture's evidence by pack policy — the question may treat the glob as the padding corpus handed alongside the trace)

6. fixture_id: interactive-dropdown-focus-bug
   - evals/results/keyboard-a11y-tester/driven/interactive-dropdown-focus-bug.trace.json (keyboard-a11y-tester driven trace)

OUTPUT FORMAT — return exactly this YAML structure and nothing else:

```yaml
questions:
  - fixture_id: <id>
    adjudication_question: >
      <the question, one per fixture>
    question_source: "Phase 3 pack curation — authored by a fresh agent from artifact filenames and tool types only; no fixture metadata, rubrics, ground-truth files, or lane README consulted"
```
----END SPAWN PROMPT----

## Correction message (sent to the same running agent before it returned, 2026-08-25)

Reason: after the spawn, lane-setup work added one artifact to
`heading-hierarchy-skipped`'s raw set (a keyboard-a11y-tester screen-reader
reading-order census, collected the same day the axe batch ran). The agent was
sent exactly the text between the markers — still filenames + tool types only.

----BEGIN CORRECTION MESSAGE----
One correction to the artifact lists you were handed — fixture 3
(heading-hierarchy-skipped) has one additional artifact in its evidence set:

3. fixture_id: heading-hierarchy-skipped
   - evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/013-127-0-0-1-8777-heading-hierarchy-skipped-html.json (axe-core scan)
   - evals/results/context-utilization-phase3/raw/heading-hierarchy-skipped-kat-census/sr-census.json (keyboard-a11y-tester screen-reader reading-order census)

Author that fixture's question over both artifacts. All other fixtures'
artifact lists are unchanged. Same constraints as before: no tools, no file
reads, no defect presuppositions. Return the full 6-question YAML as your
final message.
----END CORRECTION MESSAGE----

## Recovery record (2026-08-26, pack-construction pickup session)

The spawning session died on network errors (`API Error: ENOTFOUND`, ~00:24Z)
while question-author was regenerating. Timeline reconstructed from the dead
session's transcript (`b43838df`, events at lines 792/819):

- 00:14:14Z — question-author went idle (`available`) having composed its
  answer from the ORIGINAL spawn prompt (pre-correction artifact lists).
- ~00:15:48Z — the correction message above was sent to the still-running agent.
- 00:18:10Z — question-author reported `failed`: "API Error: Connection lost
  mid-response" — the corrected regeneration never completed.
- 00:24:13Z — the PRE-correction 6-question YAML was delivered as a teammate
  message (6,947 chars, complete and well-formed).

Disposition: the 5 questions for fixtures whose artifact lists were unchanged
by the correction (button-skip-link-clean, modal-complete-clean,
file-input-no-labels, tabs-missing-arrow-nav, interactive-dropdown-focus-bug)
are accepted as authored — they were produced blind under the recorded spawn
prompt. The delivered heading-hierarchy-skipped question is DISCARDED (stale:
cites only the axe artifact, not the census the correction added). That one
fixture is re-authored by a NEW fresh agent under the same §9.6 discipline;
its spawn prompt is recorded verbatim below, before spawning.

## Re-spawn prompt — fixture 3 only (recorded verbatim BEFORE spawning, 2026-08-26)

Agent: fresh `general-purpose` subagent, model sonnet, no prior context, all
tool use forbidden, handed only artifact paths + producing tool types.

----BEGIN RESPAWN PROMPT----
You are authoring an adjudication question for a blind evidence-curation exercise.

HARD CONSTRAINTS — all binding:
- Do NOT use any tools. Do NOT read any files. Do NOT explore any repository.
  Everything you need is in this prompt; your entire output is your final message.
- You know NOTHING about this fixture beyond the artifact filenames and tool
  types listed below. Do not guess or imply which specific defect (if any) the
  fixture contains. A question that presupposes a specific defect is invalid.
- Author exactly one question for the one fixture below, from the artifact
  filenames and tool types alone, following the template below.

TEMPLATE (follow this two-part shape — an interaction sub-question plus a
structural sub-question; adapt the bracketed artifact list per fixture):

> Based on [the exact artifact filenames/paths listed for this fixture] and the
> tool that produced each (keyboard-a11y-tester driven trace /
> keyboard-a11y-tester batch-crawl findings / keyboard-a11y-tester
> screen-reader reading-order census / axe-core scan): does this evidence
> set show any interaction defect (focus not reaching or leaving an element as
> expected, an ARIA state changing with no accessible announcement, a
> keyboard-operability failure) and does it show any structural defect (a
> missing or incorrect ARIA role, landmark, label, or heading-order violation)
> for the component these artifacts describe?

FIXTURE AND ITS ARTIFACT SET (paths are repo-relative):

3. fixture_id: heading-hierarchy-skipped
   - evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/013-127-0-0-1-8777-heading-hierarchy-skipped-html.json (axe-core scan)
   - evals/results/context-utilization-phase3/raw/heading-hierarchy-skipped-kat-census/sr-census.json (keyboard-a11y-tester screen-reader reading-order census)

OUTPUT FORMAT — return exactly this YAML structure and nothing else:

```yaml
questions:
  - fixture_id: heading-hierarchy-skipped
    adjudication_question: >
      <the question>
    question_source: "Phase 3 pack curation — authored by a fresh agent from artifact filenames and tool types only; no fixture metadata, rubrics, ground-truth files, or lane README consulted"
```
----END RESPAWN PROMPT----

## Second correction — file-input-no-labels raw set expanded (2026-08-26, pack construction)

Reason: the §10 ground-truth pass found the collected raw set (axe JSON +
driven trace) carried NO error-present evidence — the trace's states show the
missing `aria-describedby`/`aria-invalid` semantics but nothing shows an error
message exists, so must-find items [1]/[2] would have remained a raw-set gap
despite ruling 6's binding collection order. A screen-reader reading-order
census on the same rendered page (error pre-triggered at mount) captures the
rendered error text ("File too large") as a bare unassociated text node —
completing the evidence pair. The artifact was added to the raw set BEFORE any
pack froze against it; the already-delivered file-input question covers only
the two original artifacts, so the question is re-authored by a NEW fresh
agent over the three-artifact list, same §9.6 discipline. Spawn prompt
recorded verbatim below, before spawning.

----BEGIN FILE-INPUT RESPAWN PROMPT----
You are authoring an adjudication question for a blind evidence-curation exercise.

HARD CONSTRAINTS — all binding:
- Do NOT use any tools. Do NOT read any files. Do NOT explore any repository.
  Everything you need is in this prompt; your entire output is your final message.
- You know NOTHING about this fixture beyond the artifact filenames and tool
  types listed below. Do not guess or imply which specific defect (if any) the
  fixture contains. A question that presupposes a specific defect is invalid.
- Author exactly one question for the one fixture below, from the artifact
  filenames and tool types alone, following the template below.

TEMPLATE (follow this two-part shape — an interaction sub-question plus a
structural sub-question; adapt the bracketed artifact list per fixture):

> Based on [the exact artifact filenames/paths listed for this fixture] and the
> tool that produced each (keyboard-a11y-tester driven trace /
> keyboard-a11y-tester batch-crawl findings / keyboard-a11y-tester
> screen-reader reading-order census / axe-core scan): does this evidence
> set show any interaction defect (focus not reaching or leaving an element as
> expected, an ARIA state changing with no accessible announcement, a
> keyboard-operability failure) and does it show any structural defect (a
> missing or incorrect ARIA role, landmark, label, or heading-order violation)
> for the component these artifacts describe?

FIXTURE AND ITS ARTIFACT SET (paths are repo-relative):

4. fixture_id: file-input-no-labels
   - evals/results/context-utilization-phase3/raw/axe-batch-2026-08-25/010-127-0-0-1-8777-file-input-no-labels-html.json (axe-core scan)
   - evals/results/context-utilization-phase3/raw/file-input-no-labels-kat-driven/trace.json (keyboard-a11y-tester driven trace)
   - evals/results/context-utilization-phase3/raw/file-input-no-labels-kat-census/sr-census.json (keyboard-a11y-tester screen-reader reading-order census)

OUTPUT FORMAT — return exactly this YAML structure and nothing else:

```yaml
questions:
  - fixture_id: file-input-no-labels
    adjudication_question: >
      <the question>
    question_source: "Phase 3 pack curation — authored by a fresh agent from artifact filenames and tool types only; no fixture metadata, rubrics, ground-truth files, or lane README consulted"
```
----END FILE-INPUT RESPAWN PROMPT----

## Delivery record (2026-08-26)

- question-author-2 returned its single-fixture YAML at 16:21:57Z (transcript
  `422c8eb1`): the heading-hierarchy-skipped question cites both artifacts
  (axe JSON + sr-census.json), keeps the two-part template shape, uses the
  exact `question_source` string, and presupposes no defect.
- All 6 questions were filled verbatim into `lane_manifest.yaml`'s
  `question_provenance` blocks (folded-scalar re-wrap only; round-trip
  parse asserted equal to the delivered strings, whitespace-normalized).
- Mechanical validation of the 5 recovered questions before filling: exact
  artifact paths per the spawn prompt (including the tabs glob + F11
  exclusion note), two-part shape, exact source string, no
  defect-presupposition phrasing. `attested_no_ground_truth_access: true`
  set for all 6 — the attestation artifact is this receipt's recorded
  spawn prompts, per README §9.6.
- `digest_content_hash` stays TBD for all 6 (filled at digest freeze,
  ruling 5).
