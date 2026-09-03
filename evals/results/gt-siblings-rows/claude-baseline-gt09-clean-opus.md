I'll read the specified file and review it.

---

## Verdict: **ACCEPT** — ship as-is

I found no accessibility defect that warrants blocking this component. The semantics, naming, focus, and alternative-access decisions are all correct, and several of them are correct in ways that are commonly gotten wrong.

## Findings

**None at CRITICAL, MAJOR, or MINOR.** No WCAG 2.2 A/AA success criterion is violated by the code as written.

## What I verified (rather than assumed)

| Check | Evidence | Result |
|---|---|---|
| Control semantics — in-page actions are buttons, not links | `map-controls-clean.blind.md:29`, `:33`, `:37` | Correct. `<button type="button">` gives role `button`, Enter+Space activation, no phantom navigation destination. Matches the stated behavior at `:144`. |
| Accessible names (4.1.2, 2.5.3) | `:30-31`, `:34-35`, `:38-39` | Names come from visible text; icons are `aria-hidden`. Visible label ⊆ accessible name, so 2.5.3 Label in Name holds and there is no `aria-label` divergence risk. |
| No spurious `aria-pressed` | `:29`, `:33`, `:37` | Correct. Zoom/reset are momentary actions with no on/off state. Adding `aria-pressed` here would be the defect. |
| Text alternative for the canvas (1.1.1) | `:20`, `:22-26` | Equivalent data reachable by a peer route. Note it's offered to everyone, not gated behind "if you can't use the map." |
| New-tab disclosure (2.4.4, G201) | `:44-47` | Real `<a href>`, real destination, `rel="noopener noreferrer"`, and the new-tab behavior is announced via visually-hidden text rather than sprung. |
| Focus visibility (2.4.7, 1.4.11) | `:97-100`, `:110-113`, `:123-126` | Every interactive element has a 3px `:focus-visible` outline with 2px offset. Critically, **nothing anywhere sets `outline: none`**, so browsers without `:focus-visible` still render a default ring — no gap. |
| Contrast (1.4.3, 1.4.11) | `:90-93` | `#0b5fff` on `#fff` computes to **5.13:1** — passes 4.5:1 for the button text and 3:1 for the border and focus outline. |
| Target size (2.5.8) | `:85-95` | 6px/14px padding + 1px border on ~16px text yields ≥33px height; 12px gap between targets. Comfortably over 24×24. |
| Visually-hidden technique | `:128-138` | Standard clip pattern with `white-space: nowrap` — text stays in the a11y tree and doesn't collapse. |
| Landmark naming | `:14-15` | `<section aria-labelledby>` pointing at the `<h2>` gives a named region. Correct, not redundant. |

## Two things I could not verify from the file (not findings — verification items for the implementer)

1. **`aria-hidden` reaching the SVG** — `:30`, `:34`, `:38`. `aria-hidden="true"` is a *prop on a React component*, not an attribute on a DOM node. If `ZoomInIcon` et al. don't spread unknown props onto their SVG root, the attribute never lands, and any `<title>` inside the icon would then concatenate into the accessible name. The icon source isn't in this file, so I can't confirm it. The button text would still supply a name either way, so this is a name-purity question, not an access blocker.

2. **Reflow at 320px** — `:79-83`. `.map-controls` is `display: flex` with no `flex-wrap: wrap`. At a 320px viewport the panel's content box is ~286px, and three padded icon+text buttons plus two 12px gaps plausibly exceed that, which would mean two-dimensional scrolling (1.4.10). I am explicitly **not** calling this a finding: the icon dimensions appear nowhere in the CSS, so any width arithmetic I do is invented, and flex-shrink plus text wrapping may absorb it entirely. This is where my confidence drops — it's a 30-second check in a browser, not a defect on the page.

## Where a reviewer is likely to raise a false alarm here

I considered and rejected these:

- **"The zoom buttons give no feedback to a screen reader user"** — true but not a defect. The buttons manipulate a visual artifact; the equivalent non-visual access path is the data table at `:23`, which is a peer route rather than a fallback. Bolting a live region onto a canvas a screen reader user isn't reading would be noise, not access.
- **"The map div has no role or label"** — `:20` is a mount point for a third-party library whose output isn't in scope. Flagging it would be reviewing code I wasn't shown.
- **"The link should say it's a PDF"** — a reasonable usability convention, but no WCAG A/AA criterion requires file-format disclosure, and `:145` describes a report, not a download. Not worth a finding.

## One non-accessibility discrepancy

`:143` says the three actions sit **above** the map, but in DOM order `.map-controls` (`:28`) comes *after* `.map-canvas` (`:20`), and no CSS reorders them. Visual and DOM order therefore agree, so 1.3.2 Meaningful Sequence is satisfied and this is not an accessibility defect — but the prose and the code describe different layouts, and one of them is wrong.

## Provenance

Files read:
- `/Users/AlexUA_1/claude/accessibility-skills-gt-fixtures/evals/results/gt-siblings-rows/prompts/map-controls-clean.blind.md`

No other file was read, no search was run, no git command was run, and no skill was invoked. The 5.13:1 contrast figure was computed by hand from the sRGB relative-luminance formula, not measured with a tool.