# Provenance

## What was consulted

Only two sources: the blind-author brief at
`.../scratchpad/blind-author-brief.md`, and my own trained knowledge of the
W3C WCAG 2.x Techniques and Failures documents (F-, G-, H-, and ARIA-numbered
techniques) recalled from memory, unaided by lookup.

## What was not opened

No file under `/Users/AlexUA_1/claude` (or anywhere else) was read. No web
search or fetch was performed. No subagent was spawned. No git command was
run. Bash was used only for `mkdir -p` (to create the six fixture
subdirectories) and `ls` (to verify the final file listing).

## Deviations / additions beyond the brief

- **`page-titles-shared` has 6 views, not the general 2–5 guideline.** The
  class list for this fixture requires 3+ pages with the bare-site-name
  defect (F25) plus three distinct clean title patterns (specific phrase,
  long formal, record-detail) — six pages minimum, since a page has exactly
  one `<title>`. I kept all six defective/clean sub-classes rather than
  dropping one to fit the 2–5 range, since the brief says classes may not be
  dropped. All five other fixtures stay within 2–5 views.
- **Real WCAG technique substituted for an initially improvised
  "calibration-only" label.** For the `identification-across-views` "primary
  nav same order across pages" row and the `clean-control` equivalent, I
  used the real sufficient technique for SC 3.2.3 (G61: "Presenting
  repeated components in the same relative order each time they appear")
  once I recalled it, rather than leaving those rows as an improvised
  calibration-only tag — they are unambiguous, so `tier: must` /
  `clause1_evidence: true`. The genuinely ambiguous deterministic-layer rows
  (map zoom controls, the id-linked table construct) stayed
  `calibration-only (repeated construct)`, since no WCAG technique
  specifically addresses excluding those from an inconsistent-identification
  check — that omission is the point being tested.
- **No classes were dropped.** Every defective and clean sub-class listed in
  the brief for all six fixtures is represented by at least one
  `expectations.yaml` row; several fixtures also received one or two
  additional rows within a listed class (e.g. a second descriptive heading
  in `clean-control`) to round out realistic page content, not to introduce
  new classes.
- No other additions beyond what the brief specifies.
