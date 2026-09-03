I'll read the single file I'm permitted to see.

---

# a11y-critic review — `row-action-inconsistent-labels.md`

**VERDICT: REVISE**

**Overall Assessment**: The table's semantics are genuinely good — real `<table>`, `<caption>`, `scope="col"` on every column header, `scope="row"` on the row-identifying cell, native `<a>` for navigation, underlined links, a real `:focus-visible` indicator at adequate contrast. The defect is not in the markup layer at all: the row action's label is a **per-record data field** (`actionLabel`), so one identical function renders as "Edit", "Modify", and "Change details" down a single column. That is a design-coherence failure no automated scanner will ever report, and the fix is a data-model change, not a string change.

---

## Pre-commitment Predictions

Before reading, for "data table with a row-actions column" I predicted:

| # | Prediction | Actual |
|---|---|---|
| 1 | Row-identifying cell rendered as `<td>` instead of `<th scope="row">` | **Wrong** — correct at :29 |
| 2 | Action link labelled only "Edit", ambiguous in a link list | **Partly** — ambiguous, but for a different reason than predicted |
| 3 | Missing `<caption>` / table accessible name | **Wrong** — present at :16 |
| 4 | Icon-only action control with no accessible name | **Wrong** — text labels throughout |
| 5 | No reflow handling at 320px / 200% zoom | **Right** (minor, see below) |
| 6 | Missing or low-contrast focus indicator on the action | **Wrong** — `:focus-visible` at :98–101, ~5.1:1 |

**I was surprised.** Five of six predictions were ARIA/markup-shaped, and the code passes all of them cleanly. The real defect lives in the data (`:8–10`), which is exactly the class of issue a markup-shaped prediction cannot catch. Noted in Synthesis.

---

## Critical Findings

None. No user category is blocked. Every action is reachable by Tab, discoverable in a link list, and correctly named in its table context.

---

## Major Findings

### 1. One function, three different labels — the label is data, not UI

**Evidence**: `row-action-inconsistent-labels.md:8` `actionLabel: 'Edit'`, `:9` `actionLabel: 'Modify'`, `:10` `actionLabel: 'Change details'`, rendered at `:38`:

```jsx
<a href={`/cases/${c.id}/edit`}>{c.actionLabel}</a>
```

The `href` is a single hardcoded template — every row goes to `/cases/{id}/edit`. `:109` confirms the intent: *"the same function every time."* So three labels describe one operation, and the label is carried on the record rather than owned by the Actions column.

**Confidence: HIGH.** The developer cannot refute this with missing context — `:38` proves same-destination, and `:109` states same-function explicitly.

**WCAG**: 3.2.4 Consistent Identification (AA) — *"Components that have the same functionality within a set of Web pages are identified consistently."*

**Scope honesty**: 3.2.4's normative scope is a *set of Web pages*, not a single page, so a pedantic reading says it does not bite here. It bites anyway, and harder than usual, precisely because the label is a data field: the same case record will render "Modify" wherever this data appears — this table, a dashboard widget, a search result, a detail page. The inconsistency is guaranteed to be *cross-page*, not merely within this table. The single-page symptom you can see in this file is the visible edge of a set-wide 3.2.4 failure.

**Who is impacted:**

- **Cognitive (primary)** — "Change details" is not a synonym a user can safely assume. It reads as a *narrower* operation than "Edit" (edit the details, not the case). Every row forces a fresh interpretation and a decision about whether the three words mean three things. This is the WCAG 3.2 Predictable principle failing at its core.
- **Screen reader (secondary)** — Two of the most common SR strategies break. Find-by-text ("Edit") reaches row 1 only. The links-list rotor shows nine links whose action tier reads `Edit / Modify / Change details`, so the list gives no scannable column structure. A user who builds a model from row 1 has it invalidated on row 2.
- **Voice control (secondary, usually missed)** — "Click Edit" works on row 1 and silently does nothing on rows 2 and 3. The user must visually read each row to discover the command before issuing it, which defeats the point of the modality.

**Realist Check** — held at MAJOR, not raised, not lowered:
1. *Worst realistic case*: hesitation, a failed find-by-text, a failed voice command; users recover by arrowing through the table. Friction, not blockage → not CRITICAL.
2. *Groups*: cognitive, screen reader, voice control, plus magnifier users who lose the "same word, same place" scanning anchor.
3. *Detection in production*: **never, silently.** axe-core, Pa11y, and HTML_CS have no rule for label inconsistency across rows. Only manual review or a user report surfaces it. Silent-failure class is why this stays above MINOR.
4. *Proportional?* Yes. It is systematic (all three rows), architectural (it will recur with every new record), and invisible to tooling.

**Fix** — remove the label from the data model; the column owns its label:

```jsx
// Data: no actionLabel field at all
{ id: 4471, name: 'Ridgeway Pumping Station', status: 'Open', lastUpdated: 'Aug 14, 2026' },

// Render:
<td>
  <a href={`/cases/${c.id}/edit`}>
    Edit<span className="visually-hidden"> {c.name}</span>
  </a>
</td>
```

Three properties of this fix matter:

- **Visible word first.** The accessible name becomes "Edit Ridgeway Pumping Station" and the visible label "Edit" is its leading substring — WCAG 2.5.3 Label in Name is satisfied and "click Edit" keeps working for voice control.
- **Hidden qualifier, not a `title` or `aria-label`.** Do not reach for `aria-label="Edit case 4471"` here: it would replace the visible text as the accessible name and re-open the Label-in-Name question; `title` is worse (advisory tooltip, not a reliable accessible name).
- **The `actionLabel` field must be deleted, not defaulted.** Leaving it in place with a default value keeps the failure one CMS edit away.

Deleting the field is the finding. Rewriting three strings to "Edit" fixes this render and leaves the mechanism intact.

---

## Minor Findings

- **Two links per row to the identical destination.** `:30` (`4471`) and `:33` (`Ridgeway Pumping Station`) both target `/cases/{id}`. Nine links for three cases; the SR link list carries six detail links where three would do, and keyboard users take a redundant Tab stop per row. Not a WCAG failure, and linking both the identifier and the title is a defensible design-system convention — flagged as a density cost to make deliberately, not a defect.
- **Table forces two-dimensional scrolling at 320px / 200% zoom.** `:61–64` sets `width: 100%` on a five-column table; `:54–59` gives the container no overflow handling. WCAG 1.4.10 exempts content requiring two-dimensional layout, and a data table is the canonical example — so this is not a 1.4.10 failure, but the *page* scrolls horizontally rather than the table. **If you add the standard fix, add all of it**: a wrapper with `overflow-x: auto` that is not keyboard-focusable is a fresh WCAG 2.1.1 failure, because keyboard-only users cannot scroll a scrollable region they cannot focus. The complete pattern is `tabindex="0"` + `role="region"` + an accessible name (`aria-labelledby` pointing at the caption).

---

## Enhancements

- **Row header is the case ID, not the case name.** `:29–31` makes `4471` the row header, so the Actions cell's programmatically determined context is a bare number. Adding `scope="row"` to the name cell (`:32–34`) as a second row header would give the action link human-readable context for free. HTML permits multiple row headers per row.
- **`:hover` has no `:focus-within` counterpart.** `:89–91` highlights the row for mouse users. Keyboard users get the link outline but lose the row-locating highlight — the affordance that matters most on a wide table. Add `.cases-table tbody tr:focus-within` alongside the `:hover` rule.
- **Touch target height.** Inline link text at default font size is roughly 19px tall. WCAG 2.2 SC 2.5.8 (24×24, AA) is **met** via the spacing exception — vertical row pitch is ~44px and horizontal link centers are far apart — so this is not a finding. It is still small for touch; 2.5.5 (AAA, 44×44) would want padded block-level link targets in the Actions cell.
- **2.4.9 Link Purpose (Link Only, AAA)** is failed by "Change details" and by "4471" standing alone. The Major-finding fix resolves both.

---

## What's Missing

- **Empty state.** `:26–42` renders `<tbody>` with nothing inside when `cases` is empty. Sighted users see an empty box; SR users hear a table with headers and no rows and get no explanation. Data is hardcoded here so this is unexercised, but the component has no empty branch to exercise.
- **A stated rule for who owns action labels.** Nothing in the component or the Expected Behavior (`:104–110`) says the label is fixed. `:109` describes the inconsistency as observed behavior without marking it as a defect. Absent a stated rule, the next feature adds a fourth verb.
- **Any signal tying Status to action availability.** Case 4488 is `Closed` (`:9`) and still offers a full edit link. If closed cases are read-only in reality, that link is a false affordance for every user; if they are editable, nothing here says so. Not assessable from this file — see Open Questions.
- **Verification method for the fix.** Per the DOM-verification rule: a visually-hidden qualifier must be confirmed in the *rendered accessible name* (accessibility tree inspection or a `virtual-screen-reader` spoken-phrase assertion), not by reading the JSX. A `.visually-hidden` class that uses `display:none` computes to no name at all and would look correct in source.

---

## Multi-Perspective Notes

**Screen reader user** — Structure is genuinely good: `<caption>` at `:16` names the table, column headers at `:19–23` and the row header at `:29` mean every cell announces with full context, and reading order matches visual order. The failure is navigational, not structural: find-by-text and rotor scanning both break at the Actions column, and the action tier of the link list reads as three unrelated commands. WCAG 2.4.4 Link Purpose (In Context) **passes** — the definition of programmatically determined link context includes the containing cell and its associated header cells, so "Edit" resolves to "Case ID 4471 → Actions → Edit."

**Keyboard-only user** — No traps, no dynamic content, no focus management required, and correctly none attempted. `:98–101` gives a real 3px `:focus-visible` outline with `outline-offset: 2px`; measured against white it is ~5.1:1 and against the `#f0f0f0` hover row ~4.5:1, both clearing the 3:1 non-text threshold. Tab order follows DOM order follows visual order. The only costs are the redundant per-row Tab stop and the missing `:focus-within` row highlight.

**Low vision (200% zoom, high contrast, magnifier)** — Links are underlined (`:95`), not color-alone, so 1.4.1 is satisfied. Link text at `#0b5fff` measures ~5.1:1 on white and ~4.9:1 on the `#fafafa` zebra rows — both pass 1.4.3. Zebra striping plus a real border grid gives good row tracking under magnification. Two costs: horizontal page scroll at narrow widths (Minor above), and a magnifier user panning to the Actions column has to re-read each label because the word changes — the one place where the Major finding hits this perspective directly.

**Cognitive accessibility** — This is where the component actually fails. Three verbs for one action is a consistency defect at the level users notice, and "Change details" actively suggests a narrower operation than "Edit." Everything else here supports comprehension well: `Status` and `Last updated` are plain text with no color-coding (`:35–36`), the caption states the table's scope, and no timeouts or destructive actions exist to guard.

---

## Clean Bill — verified, not assumed

Stating these explicitly because a sloppier review would flag them:

- Native `<a>` is **correct** for these controls — they navigate to URLs. `<button>` would be wrong.
- Native `<table>` semantics are used; **no** ARIA roles are papering over bad structure.
- `role="presentation"` is **correctly absent** — this is a data table with real `<th>` cells, and adding it would be a defect.
- No `aria-label` on the table is **correct** — `<caption>` at `:16` supplies the accessible name.
- **No** live region, `aria-busy`, or announcement plumbing is needed — nothing on this component is dynamic. Their absence is correct, not a gap.
- **No** focus-management design is needed — no modals, no async CRUD, no in-page anchors, no SPA route changes in scope.
- Row-identifying content is in `<th scope="row">` (`:29`), not `<td>` — the common template-loop anti-pattern is **not** present.
- 2.5.3 Label in Name passes — visible text and accessible name are identical throughout.
- Landmark structure, `<html lang>`, skip links, and heading hierarchy are **page-shell** concerns outside this component's scope and are not counted against it.

---

## Verdict Justification

**REVISE**, not ACCEPT-WITH-RESERVATIONS. The distinction: a reservation is something you ship and watch; this requires a change to the data model before shipping. As long as `actionLabel` (`:8–10`) exists as a per-record field, the inconsistency is not a bug that was fixed — it is a capability the schema grants, and it will recur with the next record, the next import, the next CMS editor.

**REVISE**, not REJECT. The markup is above average for this component class and needs no restructuring. One field deletion, one hardcoded label, one visually-hidden qualifier.

**No severity recalibrations.** The Major finding was tested against all four Realist Check questions and held at MAJOR: it is not CRITICAL (no access loss, no workaround required beyond normal table navigation) and not MINOR (systematic across all rows, architectural in origin, and undetectable by every automated tool in the stack).

**To upgrade to ACCEPT**: delete `actionLabel` from the data model, render a fixed "Edit" with a visually-hidden case-name qualifier, and verify the computed accessible name in the accessibility tree or via a spoken-phrase assertion — not by reading the JSX.

**No test evidence was supplied with this fixture.** Every contrast ratio above is computed from the hex values in the CSS block, and the 2.5.8 spacing-exception analysis is derived from the padding and line-box in `:73–78` rather than from a rendered layout. Those two claims would be stronger measured; neither one carries a finding, so nothing here rests on them.

---

## Open Questions (unscored)

1. **Is a `Closed` case actually editable?** `:9` shows case 4488 as `Closed` with a live edit link. If the backend rejects the edit, the link is a false affordance and this becomes a real finding across all perspectives (cognitive most sharply). Not assessable from this file.
2. **Link contrast on the hover row is exactly at threshold.** `#0b5fff` on `#f0f0f0` (`:90`, `:94`) computes to **4.50:1** against a 4.5:1 requirement. It passes, and I am not filing it — but a margin that thin will fail the moment either value is nudged, and it deserves a measured check rather than my arithmetic.
3. **What does `.visually-hidden` resolve to in this codebase?** My recommended fix depends on the clip-rect pattern. If the project's utility uses `display:none` or `visibility:hidden`, the qualifier contributes no accessible name and the fix silently does nothing. Not verifiable within the blind scope.
4. **Does the Actions column ever carry a genuinely different operation?** If some rows offer "Archive" or "View" rather than an edit, then `actionLabel` has a real job and the finding changes shape — the fix would become a constrained enum plus a per-verb destination, not a fixed string. Nothing in this file suggests it (`:38` hardcodes one destination), but the field's existence hints someone once wanted it.

---

## Provenance

Files read — **one**, in full:

- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt-siblings-rows/prompts/row-action-inconsistent-labels.blind.md` (111 lines, single `Read` call)

No other file was opened. No `Grep`, `Glob`, `Bash`, or `git` command was run at any point in this session. Nothing under `evals/suites/` was accessed; no `*.metadata.yaml` or `*.rubric.yaml` was read; the fixture name was not searched for anywhere in the repo. Blind protocol held.