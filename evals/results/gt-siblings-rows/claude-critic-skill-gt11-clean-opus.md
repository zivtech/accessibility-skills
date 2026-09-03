I'll start by reading the one file I'm permitted to read.

---

# Fixture review: `paired-id-name-columns-clean.md`

**VERDICT: ACCEPT**

**Overall Assessment**: This is genuinely clean at WCAG 2.2 AA. The table uses correct native semantics with zero ARIA — caption, `thead`/`tbody`, `scope="col"` on all four column headers, and `scope="row"` on the row-identifying Case ID cell — which is precisely the pattern the "td-in-a-loop row header" anti-pattern names as the fix, not the defect. The paired ID/Name links are defensible, though the file's stated *reasoning* for why is weaker than the actual reason (see below). The only real gaps are sub-MINOR: a missing horizontal-scroll wrapper, and an AAA-only link-purpose limitation.

**Pre-commitment Predictions** (made from the title and component type before reading the code):

| # | Predicted | Outcome |
|---|---|---|
| 1 | Case ID cell would be a `<td>` in the loop instead of `<th scope="row">` | **Wrong** — correctly `<th scope="row">` (`:28`) |
| 2 | Adjacent duplicate links to the same href causing H2-style double announcement | **Partly** — duplicates exist but are non-adjacent and header-disambiguated |
| 3 | Bare numeric link text failing link purpose | **Partly** — bare, but covered at AA; fails AAA only |
| 4 | Missing `<caption>` or missing `scope` on column headers | **Wrong** — both present (`:16`, `:19`–`:22`) |
| 5 | Focus indicator killed by an `outline: none` reset | **Wrong** — no reset anywhere; explicit indicator added (`:94`–`:97`) |
| 6 | No `overflow-x` wrapper on a 4-column data table | **Right** — the one that landed |

Four of six predictions were wrong. I did not find the defect I most expected, and I am not going to invent a replacement for it.

## Findings

**Critical Findings**: None.

**Major Findings**: None.

**Minor Findings**

1. **Data table has no horizontal-scroll container.** `.cases-table` is `width: 100%` (`paired-id-name-columns-clean.md:57`–`:60`) inside `.cases-table-container`, which sets padding and a border but no `overflow-x` (`:50`–`:55`). Four columns at `padding: 12px` per side consume ~96px of the 280px available inside the container at a 320px viewport (WCAG 1.4.10 reflow width), leaving ~46px per column — narrower than the unbreakable word "Ridgeway". The table will overflow.
   - WCAG: **1.4.10 Reflow** exempts data tables ("content which requires two-dimensional layout"), so the table's own need to scroll is *not* a failure. The gap is that the overflow escapes to the page rather than being contained, which is a robustness issue rather than a conformance one.
   - Impact: low vision at 400% zoom, and small-viewport users, get page-level horizontal scroll instead of a scrollable region.
   - Fix: `overflow-x: auto` on `.cases-table-container`, plus `tabindex="0"`, `role="region"`, and `aria-labelledby` pointing at the caption — a scrollable region must itself be keyboard-reachable (WCAG 2.1.1), which is the step most implementations skip.
   - Confidence: HIGH on the overflow; MEDIUM on impact, since it depends on the page context this component drops into.

**Enhancements**

- **Link text is uninformative outside table context (AAA only).** The ID link's accessible name is `"4471"` (`:29`). In NVDA's Elements List or the VoiceOver rotor — which strip table context — the user gets a flat list of three bare numbers interleaved with three site names. **SC 2.4.4 Link Purpose (In Context)** is satisfied, but not for the behavioral reason the file gives at `:112`; it is satisfied because the SC's own definition of *programmatically determined link context* explicitly admits "a table header cell for a cell that contains the link." That is a normative citation, not an assumption about how a given screen reader behaves. **SC 2.4.9 Link Purpose (Link Only)** (AAA) does fail. If AAA is ever a target, `aria-label={`Case ${c.id}`}` on the ID link closes it — but only if AAA is actually the target; adding it for AA is over-engineering.
- **Hover-state link contrast sits exactly on the AA line.** `#0b5fff` on the `:hover` background `#f0f0f0` (`:85`–`:87`, `:89`–`:92`) computes to **4.4998:1** against a 4.5:1 requirement — it rounds to a pass and every contrast checker will report 4.5:1. I am flagging the arithmetic, not calling it a violation. Default (`5.13:1`) and zebra (`4.91:1`) states pass comfortably. Darkening to `#0a56e6` would clear all three states with margin. Confidence: HIGH on the numbers, and deliberately rated ENHANCEMENT — a mouse user hovering a row is by definition looking at it, and no keyboard or screen-reader user ever encounters this state.
- **Row header choice encodes the number, not the name.** Only the ID cell is `<th scope="row">` (`:28`), so in table-navigation mode every cell is announced against "4471". A user who came to the table scanning by site name — the exact user the file's claim at `:114` says the Name link serves — gets rows identified by a number they weren't scanning for. HTML permits two `<th scope="row">` cells in a row; promoting the Name cell would announce "4471, Ridgeway Pumping Station, Open". This is a legitimate design choice either way and 1.3.1 is satisfied as written. Raising it as a preference, not a defect.
- **No `<time datetime>` on "Aug 14, 2026"** (`:35`). No WCAG requirement; helps machine consumers.

## What's Missing

Checked for, and correctly absent — the absences are load-bearing, not oversights:

- **No `outline: none`.** The reason `:focus-visible` (`:94`–`:97`) is safe is not that the rule exists, it's that nothing removes the UA default. A browser without `:focus-visible` support still shows an indicator. Many implementations get this backwards.
- **The focus indicator is an `outline`, not a `box-shadow`.** `outline-color` is forced to a system color in Windows High Contrast Mode; `box-shadow` is discarded entirely. This choice survives forced-colors; the common one does not.
- **No `id` attributes anywhere.** If this component renders twice (the mobile+desktop duplicate-DOM anti-pattern), there is nothing to collide. `key={c.id}` is React-internal and never reaches the DOM.
- **No `role="presentation"`**, no `title`-as-accessible-name, no `aria-label` on a wrapper substituting for a visible label, no per-row `aria-live` or `role="alert"` inside the loop, no images needing `alt` decisions. Every item on the April-2026 third-party-audit anti-pattern list is clean.
- **No status color-coding in CSS.** "Open" / "Closed" / "In Progress" (`:34`) are plain text with no `.status-open { color: green }` rule, so there is no 1.4.1 use-of-color exposure. Easy to add badly later; currently correct.
- **Scope boundary — no live region, and none needed.** `cases` is a hardcoded literal (`:7`–`:11`). Nothing updates, so there is no 4.1.3 Status Messages surface. This is a statement about the fixture as given, **not** a claim that the pattern is safe once wired to a fetch or filter — at that point a `role="status"` region and a busy/loading state become mandatory, and the row-count change must be announced.

## Multi-Perspective Notes

- **Screen reader user**: Sound. Two clarifications on the file's own claims. `:110` says a screen reader "announces the column header and the row header together with every cell" — that is true in *table-navigation* mode (JAWS/NVDA `Ctrl+Alt+arrows`, VO `Ctrl+Opt+arrows`), and not true of linear browse-mode reading, where the user hears cell contents in sequence. The conformance conclusion holds; the behavioral claim is broader than reality and shouldn't be restated as unconditional. The genuinely good outcome is that the ID and Name links land under distinct column headers, so the two same-href links are never announced back-to-back with nothing to tell them apart.
- **Keyboard-only user**: DOM order equals visual order; six links, no traps, no JS, no focus management required because nothing opens, closes, or re-renders. The honest trade-off the file's claim at `:114` understates: two links per row doubles the tab cost linearly. At three rows this is invisible; at 200 cases it is 400 tab stops with no in-table bypass mechanism. **2.4.1 Bypass Blocks** does not apply (it scopes to blocks repeated across pages), so this is not a finding — but "neither is redundant" is a claim about semantics, and it does not answer the traversal cost. Worth stating rather than accepting unexamined.
- **Low vision (200%/400% zoom, HCM, magnifier)**: Focus indicator is a 3px outline at 5.13:1 against white — well past the 3:1 non-text minimum (1.4.11) — with `outline-offset: 2px` keeping it clear of the underlined text. Links carry an explicit underline (`:92`), so 1.4.1 is met without relying on the blue. In forced-colors mode the zebra striping and hover backgrounds are discarded but the `1px solid` cell borders (`:69`–`:74`) are forced to a system color, so the grid structure survives — a borderless zebra-only table would not. Target size: the ID link is roughly 34×19 CSS px, under the 24×24 minimum, but **2.5.8** is satisfied via the spacing exception (24px cell padding puts ≥24px between the centers of adjacent link bounding boxes both horizontally and vertically). See Open Questions — this calculation rests on undeclared type metrics.
- **Cognitive**: Caption states the table's purpose and its recency scope (`:16`). Status values are words, not icons or color chips. Dates are unambiguous long-form ("Aug 14, 2026", not "8/14/26" — which reverses meaning across locales). Two entry points into the same record is a genuine cognitive *benefit*: a user who remembers the site name is not forced to translate it into a case number first. No timeouts, no destructive actions, nothing to confirm.

## Verdict Justification

ACCEPT. I found no CRITICAL and no MAJOR findings, so no Realist Check recalibrations were required — nothing needed downgrading because nothing was inflated on the way in.

The thing worth saying plainly: this component is clean because it uses boring, correct HTML and adds no ARIA at all. The row header is a `<th scope="row">` rather than a `<td>` carrying an `aria-label`, the focus indicator is an outline rather than a shadow, the link affordance is an underline rather than a color, and there are no `id` attributes to collide. Each of those is the version that survives a context the author didn't anticipate — a rotor, forced-colors mode, a duplicate render.

Two calibration corrections to the file's own justifications, offered because a right conclusion resting on a wrong reason breaks the next time someone reuses the reasoning:

1. **Claim `:111` reaches the right answer by the wrong route.** It argues the paired links aren't a **3.2.4 Consistent Identification** failure because the ID lookup and the name lookup are "different functionalities." That distinction is doing work it can't bear — both links navigate to `/cases/4471`, and calling that two functionalities is arguable at best. The actual reason 3.2.4 doesn't apply is scope: the criterion governs consistency **across a set of Web pages**, and its associated failure (F31) is about using two different labels for the same function *on different pages*. Two differently-labelled links within a single row are simply outside what 3.2.4 regulates. Same verdict, defensible reason.
2. **Claim `:112` should cite the SC's definition, not screen-reader behavior.** "Table-navigation mode reads the header and the cell together" is mode-dependent and AT-dependent, and it is flatly false in the links-list context where the bare "4471" actually shows up. **2.4.4** is satisfied by its normative definition of programmatically determined link context, which names the table header cell explicitly. Anchor it there.

For an upgrade path: there isn't one — the verdict is already ACCEPT. To move the code from conformant to hardened, the one change with real return is the `overflow-x: auto` wrapper with its keyboard-reachable region, since that is the only item on this list a user can actually be blocked by.

## Open Questions (unscored)

- **Target size (2.5.8) rests on undeclared type metrics.** The CSS sets no `font-size` or `line-height` on the table (`:57`–`:97`), so my ~19px link height and the spacing-exception geometry assume a 16px/1.2 default inherited from the page. A host page setting a smaller base size, or tighter `line-height`, could narrow the vertical margin between rows enough to matter. Confidence MEDIUM; needs a rendered measurement, not source reading. Flagged rather than reported as a finding.
- **Does this component ever render more than a demo-sized list?** The reflow finding and the tab-cost observation both scale with row count, and the fixture ships three rows. At 200 rows the calculus on both changes.
- **Is the data ever loaded asynchronously or filtered?** As given there is nothing to announce. If a search or filter is ever attached, a `role="status"` result-count region and a decision about where focus lands after the update both become required, and neither exists to build on.
- **Is AAA in scope?** If so, 2.4.9 is a real failure on the ID link and needs an `aria-label`. At AA it does not, and adding one would be unnecessary verbosity.

## Provenance

Files read — exactly one:

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt-siblings-rows/prompts/paired-id-name-columns-clean.blind.md` (115 lines, read in full, single `Read` call)

No other file was opened. I ran no `Grep`, no `Glob`, no `Bash`, and no `git` commands; I did not read anything under `evals/suites/`, and I did not access any `*.metadata.yaml` or `*.rubric.yaml`. Contrast ratios were computed by hand from the hex values in the fixture's CSS block using the WCAG 2.x relative-luminance formula, not measured in a browser, and are reported to four decimal places where the result lands near a threshold.