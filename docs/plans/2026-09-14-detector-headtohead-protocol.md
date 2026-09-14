# Detector head-to-head protocol (issue #86)

**Status: protocol only. No adapter built, nothing run.** Specifies how a
future WAVE-vs-axe (and Alfa-vs-axe re-run) head-to-head would be executed,
scored, and reported, so a run can start from a pre-committed method once a
WebAIM account and user-approved surfaces exist. Building the WAVE adapter now,
with no key to exercise it, would be dead code — this document does not do that.

## 1. Pre-declared bars (verbatim)

From `docs/plans/2026-09-02-promotion-candidate-dispositions.md`:

**PT-06, reopen trigger (a):**

> ≥5 *independent* defect-bearing surfaces (not pages from one demo template) yield ≥3 Alfa-only A/AA classes

That sits on top of the original bar it reopens, from
`evals/results/promotion-eval-2026-09/1.1-alfa-overlap/PRE-DECLARATION.md`:

> Alfa is a "threshold candidate" only if it fails ≥3 distinct A/AA rule classes (distinct Alfa rules mapping to A/AA criteria, FAILED outcomes only, not cantTell) that neither axe nor htmlcs flagged on the same page, AND at least one of those is a plausible true positive when you inspect the target.

That run's README records its two Alfa-only findings as "agent-assessed and
need human confirmation" — no live-page verification was done. A re-run
against trigger (a) carries a strictly higher bar: **human-confirmed**, not
agent-assessed, per §5.

**PT-07, reopen trigger (b):**

> a WAVE licence-holder runs a five-page head-to-head against axe (the Lighthouse comparison is the template) and finds A/AA defect classes axe misses

Both bars count **independent surfaces**, not pages, and need ≥1 confirmed
defect, not just a rule-class count. §2 defines "independent surface" so the
count can't be gamed the way the first Alfa run's page count was (its README
carries a reviewer correction on exactly this).

PT-07(b) as quoted above literally says "a five-page head-to-head" — pages,
not surfaces — and names no class-count threshold at all ("finds A/AA
defect classes axe misses," no number). The "independent surfaces, not
pages" upgrade above is this protocol *operationalizing* that trigger as the
harder, non-gameable reading (five independent surfaces, per §2), the same
way it already hardens PT-06(a)'s bar to human-confirmed rather than
agent-assessed (line 24) — it is not what PT-07(b) literally says, and the
dispositions row should be updated to match once a run is actually
scheduled. The missing class-count number is a separate gap this protocol
does **not** fill: picking ≥2 vs. ≥3 vs. some other number for PT-07 is a
promotion-policy decision, out of scope here (see "What this protocol does
not do"). Until that number is pinned, PT-07's operative class-count
threshold **inherits PT-06's ≥3 A/AA-classes as the conservative floor** —
never softer, and never a number invented by whoever runs it. The single
source of truth for whichever number actually governs a run is the §6
pre-declaration file for that run, committed before any tool runs; nobody
picks a number by comparing this doc against the dispositions doc and
choosing the more convenient one.

## 2. Surface independence (operational definition)

A surface is independent **iff** it has (1) a **distinct origin** (different
site/app/hosting boundary, not just a different path on the same deployment)
**and** (2) a **distinct template/CMS/authoring source** (not the same
generator or demo suite with different content). Both must hold, and a surface
does not count toward either bar's number until *both* are shown. **The W3C BAD
"before" site (`w3.org/WAI/demos/bad/before/*`) counts as exactly 1 surface**,
regardless of how many of its pages are sampled — that run's reviewer
correction found pages 3–6 share one template and near-identical SC profiles
("one template sampled four times").

Anchors: `docs/wcag-em-2-reference.md:60-72` requires the sample set to span
"variety of sample types/functionality/technologies/coding styles" (line 71),
and its representativeness check (line 62) exists to catch a structured set
narrower than it looks — the same defect the reviewer correction found here.
`docs/a11y-evaluation-report-contract.md` validator items 1 & 4: item 1
requires every structured sample to carry a `covers` classification (typed by
what it represents, not just enumerated by URL); item 4 requires
`random.items` and `structured` to "share no `id` and no locator value". A
5-surface count means 5 samples disjoint by *both* locator (item 4) and
template classification (item 1) — one URL per template is not five surfaces
under either rule. Any run states, per surface, the evidence for BOTH conditions.

**"Defect-bearing" (pre-declared, so the count can't be assembled after the
fact):** a surface is *defect-bearing* iff it carries **≥1 human-confirmed
A/AA defect**, per the §5 packet, found by **any** engine in the run — not
"an engine flagged something on it" (that would count a raw tool hit, which
is exactly the circularity §5 exists to close). A surface with only
engine-flagged, unconfirmed candidates is not defect-bearing yet, however
plausible the flag looks. This classification is only knowable after §5
runs on that surface's candidates, which is why §6 pre-declares what happens
when the count of qualifying surfaces comes up short: see §6's shortfall
clause.

## 3. Reporting split (REQUIRED by WAVE's terms)

`docs/plans/2026-08-28-accessibility-testing-wave-siteimprove-handoff.md:65`:

> Do not republish or sell WAVE reports or WAVE-derived counts/listings without confirming WebAIM permission. An engagement may retain private, access-controlled evidence and independently verify issues, but external reporting should describe the independently validated defect rather than reproduce proprietary WAVE report data by default.

**PRIVATE** (engagement repo or local only): raw WAVE API/extension JSON,
per-page item counts, category totals, item IDs — anything reproducing or
aggregating WAVE's own output. **PUBLIC** (this repo or any public
assessment): only independently verified defects (SC + plain description of
what a human confirmed) plus the promotion decision — no WAVE item ID, count,
or category label crosses over. **Alternative:** get WebAIM's permission
first via <https://wave.webaim.org/feedback>; absent permission, the split
above is the default.

Same split applies to any engagement URL in this program generally: per-page
evidence private, the aggregate (verified defects + decision) public — WAVE
is one instance of that rule, not a special case.

**WAVE-derived-data boundary.** §4/§6's public artifact carries a per-SC
"WAVE-only" attribution and a confirmed-class tally, which are themselves
1-bit-per-finding facts derived from a WAVE run — read narrowly, "no WAVE
item ID, count, or category label crosses over" above could seem to bar even
that. It doesn't. Boundary, stated explicitly: SC-level, human-confirmed
engine attribution (per §5) and the resulting class tally are **discovery
provenance of an independently validated defect**, not WAVE report data — the
same distinction `docs/plans/2026-08-28-accessibility-testing-wave-siteimprove-handoff.md:65`
draws when it says external reporting should "describe the independently
validated defect rather than reproduce proprietary WAVE report data."
Anything finer-grained than that — item IDs, per-page item counts, WAVE
category labels, WAVE-reported values (contrast ratios, counts) — stays
private under the split above, full stop.

**Classification of every pipeline output, for a WAVE-inclusive run** (all
private by default; nothing here is public unless named so explicitly):

- raw WAVE API/extension JSON — **private**.
- `run-axe-alfa.mjs` / `run-pa11y.mjs` / WAVE-leg normalized output —
  **private** (it still carries per-page, per-item WAVE data before §5
  confirmation strips it down).
- `analyze.mjs` cross-engine output — **private** (its per-page rows include
  WAVE-only cells derived straight from the raw counts).
- `write-overlap-table.mjs` overlap tables — **private** (a table with a WAVE
  column and per-page WAVE-only rows is a WAVE-derived listing, exactly what
  §3's opening rule forbids from crossing over).
- analysis summaries and command/run logs — **private** (command logs can
  carry item IDs and counts in argv or stdout captures).
- §5 human-confirmation packets — **private** as authored (they may reference
  a raw locator before being distilled).
- the **one named public artifact** — a written-for-publication summary whose
  schema contains only §5-confirmed fields: human-measured value, SC,
  failure mechanism/description in plain language, element locator, named
  confirmer, date, plus the SC-level "WAVE-only" attribution and class tally
  permitted by the boundary statement above. Nothing else from the pipeline
  is public.

## 4. Runbook

**Reused unchanged** — `evals/results/promotion-eval-2026-09/1.1-alfa-overlap/project/`:
`run-axe-alfa.mjs` (axe-core; also Alfa if an Alfa re-run is in scope),
`run-pa11y.mjs` (htmlcs), `analyze.mjs` (cross-engine SC normalization +
overlap classification), `write-overlap-table.mjs` (Markdown tables),
`requirements-map.json` (Alfa rule→SC join, only if Alfa is in scope). A
WAVE-inclusive run swaps in the §2 surface list and adds a fourth leg below;
it does not modify these scripts.

**New WAVE leg** (written when a key exists — not part of this task):
`reporttype=4` (selectors + contrast, 3 credits/page, handoff doc line 52);
`WAVE_API_KEY` from ENV only, never in a URL/log/error, redacted on every
write path; **≤2** simultaneous requests (handoff doc line 40); no key → exit
`SKIPPED_CREDENTIAL_REQUIRED` and the other legs still run; item→SC mapping
fetched from WebAIM's documented item reference **at run time**, every run,
**never vendored** (a copied table would itself be WAVE-derived data, same
constraint as §3); raw WAVE JSON goes to the private location only, and the
public artifact gets just the per-surface, per-SC "WAVE-only" classification
after §5, in the shape `analyze.mjs` already produces.

**Mechanical split enforcement (to be built when the run is scheduled, not
now — runs are deferred):** the classification above is only real if nothing
mechanically bypasses it. Two things must exist before any WAVE leg runs:
(a) raw WAVE JSON, `analyze.mjs` output, overlap tables, analysis summaries,
and command logs are written **only** to a gitignored path or the private
engagement repo — never to a path this public repo tracks; (b) a CI grep gate
over tracked files for WAVE item-ID and category patterns (`error|contrast|
alert|feature|structure|aria` as WAVE category tokens, and WAVE's numeric
item-ID scheme), built on the same pattern as `scripts/check_client_refs.py`
(positive+negative self-test, exit 1 on any hit, no allowlist). Reusing
`analyze.mjs`/`write-overlap-table.mjs` unchanged (as this section already
directs) is only safe once (a) and (b) exist — the scripts themselves don't
know which repo they're writing into.

**Sequence:** (1) freeze the surface list per §2 with independence
justification written first (also §6 step 1); (2) run axe+htmlcs(+Alfa) via
the existing scripts, unmodified; (3) run the WAVE leg under the
concurrency/credential rules; (4) extend `analyze.mjs`'s normalization to
classify each surface×SC outcome as engine-only vs ≥2-engine agreement; (5)
run the §5 packet on every engine-only class before it counts; (6) tally
confirmed classes against §2's surface count and §1's bar; (7) apply §3 on
write-up.

## 5. Human-confirmation packet

Per surface, per candidate finding, before it counts toward either bar:

1. **Live inspection record** — page loaded in a real browser at the scan
   viewport, actual computed value checked against the tool's claim (e.g.
   contrast: devtools-read RGB vs. reported ratio) — the check the first Alfa
   run flagged as *not yet done*.
2. **SC + failure mechanism** in one sentence a non-tool-user could verify
   ("the visible label text is not a substring of the accessible name", not
   "rule X fired").
3. **Element locator** — CSS selector or XPath plus a short HTML snippet, at
   `bug-reporting`'s existing granularity.
4. **Confirmer identity and date** — promotes "agent-assessed, needs
   confirmation" to "human-confirmed." The confirmer must be a **named
   human** (never an agent identifier), per the same discipline as
   `ratified_by` in `docs/a11y-evaluation-report-contract.md:257` and PT-06's
   own "human-confirmed, not agent-assessed" line above (§1).
5. **Independence cross-check** — one line confirming no other engine in the
   run flagged the same SC on the same surface, re-verified now, not just
   trusted from runbook step 4.
6. **Frozen-state capture** — a screenshot or saved rendered DOM taken at
   confirmation time, so the packet is re-verifiable later without trusting
   the confirmer's memory of a page that may since have changed; per
   WCAG-EM 5.2 (`docs/wcag-em-2-reference.md:66`), which names archived
   samples, screenshots, and saved rendered DOM as the way to make an
   evaluation specifics record replicable.
7. **Alfa locator derivation** — Alfa's default JSON output carries no
   selector or markup, so for an Alfa-sourced finding the confirmer must
   *derive* item 3's locator by hand from the live page; it does not come
   free from the tool the way it does for axe or WAVE.

A finding missing any of the seven does not count as the "≥1 human-confirmed
true positive" (PT-06) or as evidence WAVE "finds A/AA rule classes that axe
misses" (PT-07).

## 6. Pre-declaration template

Copy the form of `.../1.1-alfa-overlap/PRE-DECLARATION.md`: state the bar,
timestamp it, commit it **before any tool runs**, never adjust after seeing
results.

**Shortfall handling (pre-declared, not decided after the count comes in):**
if, after §5 runs on every candidate, fewer than the committed surface count
qualify as *defect-bearing* (§2's definition), the run reports
**INCONCLUSIVE** against that bar. Surfaces are **not** re-rolled, swapped,
or topped up to reach the number after the fact — that is the optional-
stopping move this protocol exists to close off. Any later attempt at the
same bar must cite the inconclusive run's pre-declaration file and explain
what changed, per the attempt-family accounting below; it does not get to
proceed as if the inconclusive run never happened.

**Attempt-family accounting:** every pre-declaration lists **every prior
attempt at this same bar**, or states plainly that there are none. When a
reopen decision is made, it weighs **all** attempts in the family together —
inconclusive and outright-failed runs included — never just the best-scoring
one. A bar is not "met" because the fifth attempt cleared it while the first
four didn't; the pre-declaration file is where that full history has to live
so a reviewer can see it without reconstructing it from scattered commits.

**Surface count, exact:** the pre-declaration commits an **exact** surface
count *N* (or a narrow named range, e.g. "5, or 6 if one surface is later
disqualified on independence grounds") before any scan — not an open-ended
"≥5." An open floor is a standing invitation to keep adding surfaces until
one clears the bar; a fixed *N* makes the shortfall clause above meaningful.

**Pilot-scan disclosure:** any prior automated scanning of a committed
surface, by any in-scope engine, before that surface was locked into this
pre-declaration, is disclosed here by name — which engine, when, by whom.
Undisclosed pre-scanning of candidate surfaces (curating the list based on
which pages already looked promising) voids the receipt for that run.

**Receipt = commit SHA, not self-reported prose:** the receipt is the
pre-declaration file's own **commit SHA** (from `git log` on the commit that
adds or finalizes it), not "the first output artifact's header timestamp" —
a run's own artifact is self-authored and cannot serve as its own
independent timestamp. Every artifact this run produces (raw engine output,
`analyze.mjs` output, the §5 packets, the final write-up) records that
commit SHA in its header. A verifier checks the commit's ancestry and
timestamp in the repo's own history, not a prose claim inside the artifact.
The same bar, and the same commit-SHA receipt, must also appear wherever the
run is queued (PT-06's rule appeared in the program plan before that agent
was spawned) — a pre-declaration file doesn't count if the tracking doc
states a softer bar or points at a different receipt.

```markdown
# Pre-declaration of the <PT-06(a) | PT-07(b)> decision rule (receipt)
Stated **before the run** (session <date>, started ~<time> UTC; the receipt
is this file's own commit SHA once committed — recorded here after commit,
then copied into every run artifact's header).
Pre-declared threshold (do not soften it): <quote the exact §1 bar under
test, verbatim, plus §2's independence definition, §5's confirmation
requirement, and, for PT-07(b), the pinned class-count threshold per §1's
PT-07 note>.
Surface count committed (exact N, or a named narrow range per §6): <N>.
Surfaces committed, with independence justification per §2: <list, frozen
before any scan>.
Prior attempts at this bar: <list every prior pre-declaration file for this
bar with its outcome, or state "none">.
Pilot-scan disclosure: <name any prior automated scan of a committed surface
by any in-scope engine before it was locked in, or state "none">.
Shortfall handling: if fewer than <N> surfaces qualify as defect-bearing
after §5, this run reports INCONCLUSIVE per §6 — surfaces will not be
re-rolled or topped up.
Report either outcome plainly.
```

## What this protocol does not do

- Build the WAVE API adapter, or run anything — blocked on a WebAIM account
  and the user's choice of surfaces.
- Re-litigate whether ≥3/≥5 is the right bar — §1 quotes them as pre-declared.
- Vendor WAVE's item→SC mapping (§4) or raw report data (§3) into this repo.
