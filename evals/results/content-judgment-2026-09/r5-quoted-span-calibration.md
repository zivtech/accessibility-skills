# R5 quoted-span fabrication check — calibration on the origin run (2026-09-02, pre-freeze)

Method: the scorer's `quoted_span_hits()` (quoted spans of ≥ 3 words, case /
quote / whitespace normalized, absent from the row's name/detail/href/context/
landmark/flags and from the line's own `fix`) run over the origin engagement's
first-pass judgments joined to their input rows and to the second reader's
`spot-checks.jsonl` (530 rows). Positive set = spot-check notes that name an
asserted or unshown fact; honest set = `agree` rows without such a note.
Counts only — no row text, product name, or rationale leaves the private repo.

R5 quoted-span (>=3 words) calibration on the origin run (counts only; no row text leaves the private repo):
  second-reader notes naming an asserted/unshown fact (positive set): 6; R5 fires on 2 of them
  second-reader AGREE rows without such a note (honest set): 318; R5 fires on 27 (8.5%)
  of those honest fires, 2 vanish under punctuation/dash-insensitive matching

Decision: recall 2/6 and an 8.5 % false-fire rate on second-reader-agreed
rationales are not must-tier numbers. The check ships **should-tier**
(`fabrication_quoted_span_tier: should` in every fixture's metadata); the
list-form check (`fabricated_tokens`, metadata-named values a model could
invent) is the must-tier fabrication gate. Promotion of R5 to must needs a
positive set larger than six and a false-fire rate under 2 % — recorded as an
instrument watch item, not a plan step. Minimum span lengths of 2 and 4 words
were also measured (agree-set fires 39 and 20 of 322); 3 is the compromise
between recall and noise.
