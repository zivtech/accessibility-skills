# Content draft-judgment rubric

You are drafting per-row accessibility judgments for a human ratifier. Each row is one page title,
heading, link, image, form field, or navigation-identification variant, captured from a live page
with its surrounding context. Your job is to say whether the text a user actually receives does its
job **for the person who relies on it**, not whether it satisfies a checklist.

Output per row: `judgment` (`yes` = useful/meaningful/descriptive as-is; `no` = it fails the person;
`unsure` = you cannot tell from the captured context), `confidence` (`high` / `medium` / `low`),
`rationale` (one sentence, ≤ 25 words, that names what the user would experience), `fix` (a concrete
replacement text or change, ≤ 20 words, or empty when `yes`), and `needs_human` (`true` when
`unsure`, when confidence is `low`, or when a `no` depends on something not in the row, such as
what the destination page actually contains).

## Per criterion

**2.4.2 Page titled.** Does the title identify *this page* and distinguish it from the site's other
pages? A site name alone ("Example.gov") is `no` when the site has more than one page. Site name plus
a page-specific phrase in either order is `yes`. Titles that differ only by an ID string the user
cannot interpret are `unsure` unless the ID is the thing the page is about (a record identifier on a
record detail page is legitimate, but the record *name* should be there too).

**2.4.6 Headings and labels descriptive.** Does the heading tell the reader what the section
contains, so someone scanning by headings can find it? Generic headings ("Overview", "Details",
"More", "Information") are `no` when the section preview shows they could be replaced by something
specific. Empty headings are `no`. A heading that is a data value ("24.3") with no noun is `no`. Do
not judge heading *levels* here; level skips are recorded as a flag for 1.3.1, not for this row.
For form fields: does the label say what to enter? Placeholder-only labels are `no` because the
label disappears on input. (A field with no programmatic label is also a Level A 3.3.2 failure; the row is
filed under 2.4.6 here, so a ratified `no` goes to bug-reporting with 3.3.2 cited.) A wrapping label or `aria-label` that names the field is `yes`.

**2.4.4 Link purpose (in context).** From the link text **plus** the captured surrounding block
(`context`), can the user tell where the link goes or what it does? Judge in context: "Learn more"
inside a paragraph about ozone forecasts is `yes` when that paragraph names the destination — the
paragraph is the link's programmatically determined context (H78; likewise a list item H77, a table
cell with its headers H79, or the heading directly before the link H80). It is `no` only when no such
context names the destination — five "Learn more" links whose card text sits in sibling blocks the
link is not part of (F63), or a bare "Learn more" with nothing around it. That is the Level AA
question. That identical names are indistinguishable when a screen reader lists all links is a
2.4.9 (AAA) concern: put it in the `fix` or a note for the ratifier, never make it the AA verdict.
An empty accessible name is always `no`. A name equal to the raw URL is `no` unless the URL is a
readable domain the user is meant to see. A file link (`file_ext` set) whose name does not indicate
the format is **not** a 2.4.4 failure — no sufficient technique requires a format cue: leave the
`file_<ext>_not_indicated` flag to speak, draft `yes` when the purpose is otherwise clear with the
cue suggested in `fix`, `unsure` when the purpose itself is unclear. Icon-only links with an alt or aria-label that
names the destination are `yes`; with an alt that names the icon ("arrow", "chevron") are `no`.

**1.1.1 Non-text content.** First decide the image's role from its position: inside a link/button
with no other text → **functional** (alt must name the destination/action, not the picture);
decorative (spacer, ornament, an icon next to text that already says the same thing) → alt should be
empty (`alt=""` or `aria-hidden`) and a non-empty alt that repeats adjacent text is `no` as
redundant; informative → alt should convey the *information*, not the *appearance*
("Air quality index gauge showing 42, Good" is `yes`; "gauge" is `no`; "AQI_gauge_v2.png" is `no`).
Complex images (charts, maps, structure diagrams) with a short alt are `unsure` unless the adjacent
text or a figcaption carries the data. A missing `alt` attribute is `no` always. An inline SVG with
no title, no aria-label, and no aria-hidden is `unsure` (it may be decorative, but it will be read
as "image" or skipped depending on the AT).

**3.2.4 Consistent identification.** For rows of type `ident`: the same destination (`href`) is
named differently across pages. Are the variants acceptable (a logo named for the site and a text link "Home"
both go to `/` and users understand both), or would a user think they are different things
("Contact" / "Contact Us" is borderline-`yes`; "Resources" / "Help" for the same page is `no`)?

## Calibration

- A `no` must name what the person loses. "Not descriptive" is not a rationale.
- Do not flag things that are merely not-best-practice. The question is whether the user is
  served.
- Government sites use long formal names legitimately. Length alone is never a `no`.
- When the captured context is clearly truncated or is a whole nav block, that is a capture limit,
  not evidence about the page. Say `unsure`, `needs_human: true`.
- Never invent what a destination page contains. If the judgment hinges on it, `needs_human`.
- Audience-standard shorthand is `yes`. On a specialist product, an abbreviation the audience uses
  daily (a scientific dashboard's assay and pathway abbreviations; an air-quality tool's index name) is a descriptive label at
  Level AA; expansion is a AAA (3.1.4) concern, not this row's. Do not hedge to `unsure` for jargon.
  You can only apply this rule from the product-and-audience note the orchestrator supplies with the
  batch — read it first; a row alone does not tell you who the audience is.
- Judge repeated patterns the same way every time. If a batch holds forty rows of the same
  construct (an ID link beside a name cell), decide the construct once from the rubric and apply it:
  the ID link is `yes` when the row's context names the record, `no` when the row shows only the ID.
  When `context` is empty on an ID link inside `main`, that is the inventory's capture limit for
  table cells (the sibling name cell is not captured), not evidence about the page: `unsure`,
  `needs_human: true`, and say so in the rationale.
  Drifting between `yes`, `no`, and `unsure` on identical rows is the most common first-pass fault.
