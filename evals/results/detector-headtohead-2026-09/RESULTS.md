# Detector head-to-head — result (issue #86)

**Publish-safe by construction.** No WAVE report data appears here — no WAVE
item IDs, per-page counts, or category labels (protocol §3;
`docs/wave-adoption-assessment.md` licence clause). Only the decision, the
method, and independently-described WCAG defects. Raw WAVE output and per-page
counts stay in the private engagement record, never in this repo.

**Receipts:** pre-declaration commit `091321a` (2026-09-15 00:41:55 UTC,
committed before any scan; `PRE-DECLARATION.md`); protocol element-level-dedup
amendment `cbeec39`. **Engines:** axe-core 4.13.0, HTML_CodeSniffer 2.6.0
(pa11y 9.1.1), Siteimprove Alfa (rules 0.119.0), WebAIM WAVE API v3.1
(`reporttype=4`). **Viewport:** 1280×800. Playwright 1.62.1.

**Surfaces:** 5 independent EPA systems, each a distinct origin AND
template/CMS per §2 — Drupal 10 (`www.epa.gov/climate-change`), ColdFusion
(`cfpub.epa.gov/roe/`), Envirofacts/nginx (`enviro.epa.gov/`), Oracle APEX
(`ordspub.epa.gov/ords/...`), React SPA (`comptox.epa.gov/dashboard/`). The SPA
rendered fully in both Playwright and the WAVE API.

## Outcome

- **PT-06(a) — Alfa: NOT MET.** Alfa-only A/AA rule classes over axe+htmlcs came
  in **below the ≥3 floor** (same as the one prior run,
  `evals/results/promotion-eval-2026-09/1.1-alfa-overlap/`). No core promotion.
- **PT-07(b) — WAVE: NOT MET on this evidence.** After element-level dedup and
  triage (below), WAVE surfaced **no A/AA defect class that axe missed** on the
  five surfaces. No core promotion.
- Both tools **remain supplemental detector lanes** — unchanged disposition.
  This run *measures* the previously-unmeasured coverage delta and finds the
  unique-core-coverage case **not demonstrated**; it does not diminish WAVE's
  documented value as breadth + aggregate corroboration.

## Why the raw "WAVE finds lots axe misses" count did not survive scrutiny

A naive success-criterion-level overlap suggested a large WAVE-only delta. It
did not hold up, for three independent, verified reasons:

1. **Cross-engine SC-mapping collisions (the decisive one).** axe and WAVE file
   the *same element and defect* under *different* WCAG success-criterion
   numbers (e.g. a form control with no accessible name: axe records it under
   4.1.2, WAVE under 1.1.1/1.3.1/…). An SC-number comparison counts that as
   "unique to WAVE" though both engines flagged the identical element. The
   correct test is **element-level** — did the other engine flag the same
   element under *any* criterion. Verified: an unlabelled search/zip input and a
   page-language defect were each caught by **both** engines, not WAVE alone.
   This is the fix folded into the protocol (§4a, commit `cbeec39`).
2. **Advisory warnings are not failures.** The bulk of the apparent delta was
   WAVE's advisory tier (warnings to check, e.g. "a video is present — verify
   captions"), not confirmed errors — and a large share sat on an injected
   third-party feedback widget, not the sites' own templates.
3. **False positives on live inspection.** The remaining candidate errors,
   inspected in a real browser: "contrast" flagged on **visually-hidden
   (screen-reader-only) text** where contrast does not apply (the tool's own
   contrast data marked these non-failures); "missing alt" on **`aria-hidden`
   decorative icons**; and empty controls that are **hidden (0×0) in the loaded
   state** (a lightbox's prev/next), which axe deliberately skips. One nuanced
   real case remained — a duplicate element `id` breaking a form label — which
   needs human judgment and is not a clean axe miss.

## Human ratification (§5.4)

Reviewed and ratified by **Alex Urevick-Ackelsberg** (alex@zivtech.com),
2026-09-15, against the private evidence record (`RESULTS-PRIVATE.md`,
`packets/` — computed values + screenshots, held privately). The ratification
covers the **negative disposition**: the WAVE-only candidates are false
positives, methodology differences, or one nuanced non-clean case — **no
WAVE-only A/AA true positive that axe misses**. No true positive was confirmed
because none was found; nothing here promotes either tool.

## Deviations / notes for the record

- **Mechanical split enforcement (protocol §4):** this run kept the entire
  pipeline — raw WAVE JSON, analysis, logs — in an **out-of-repo scratchpad**,
  so no WAVE-derived data ever entered the repo tree (a stronger guarantee than
  the gitignore path §4(a) contemplates). The CI grep gate §4(b) was therefore
  not built; it remains a prerequisite for any future run that keeps private
  data on a gitignored path *inside* the repo. A post-run key-leak + WAVE-data
  scan across all run and tracked files came back clean.
- **Method:** uniqueness was computed at the element level per protocol §4a; the
  SC-level overlap is retained privately as a diagnostic only.

## Confirmer / status

Formal status against both bars at run time was
**INCONCLUSIVE-pending-confirmation** (agent run; §5.4 requires a named human).
The ratification above finalizes it to **NOT MET** for both bars.
