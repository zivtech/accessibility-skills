You are authoring accessibility test fixtures: six small static websites, each planted with documented WCAG failure patterns AND their documented sufficient counterparts, plus an expectations file naming which elements a careful human auditor would judge as failing the person who relies on them. You are deliberately BLIND: you have not seen and must not look for the tool that will later be evaluated on these fixtures. Do not read any file under /Users/AlexUA_1/claude — not skills, not evals, not docs. Do not run web searches. Work only from this brief, your own knowledge of the W3C WCAG techniques named below, and the output directory given at the end. Do not spawn subagents.

## What you are producing

For each fixture id below, a directory `<OUT>/<fixture-id>/` containing:

1. `views.txt` — one line per page: `view_id,product,/path.html` (product = one short lowercase word, identical on every line of a fixture; view_id = short lowercase word). 2–5 views per fixture.
2. The `*.html` pages named in views.txt. Plain HTML5, `lang="en"`, no external assets (no CSS/JS/image files needed — `<img src>` may point at paths that do not exist; that is fine), no inline scripts. Each page 30–90 lines. Realistic content for a **fictional** organisation (invent names; never a real company, agency, government body, product, city agency, or person — no real person names anywhere, including bylines). Use `.example` domains only in any absolute URL. Link hrefs are site-relative paths (`/about.html`); pages linked but not provided are fine.
3. `origin.txt` — a single fictional origin like `https://www.harborline-transit.example`.
4. `scenario.md` — 2–4 sentences, plain prose: what the product is, who its audience is (matters for whether jargon is "audience-standard"), and how many pages were captured. No hints about what is planted.
5. `expectations.yaml` — a list of the elements you planted, defective AND clean, each:

```yaml
- view: hours            # view_id from views.txt
  type: link             # title | heading | link | image | field | ident | nav
  locator:               # enough to find the element unambiguously in that page
    text: "Learn more"   # visible text / accessible name (for images: the alt or "(no alt)"; fields: the label or placeholder; ident: the href path)
    href: "/events.html" # for links/ident when text repeats
    nth: 2               # 1-based, only when text+href still repeat
  expected: "no"         # "no" = fails the person; "yes" = serves the person as-is
  unsure_ok: false       # true (either polarity) only when a careful human could legitimately say "cannot tell from this page alone"
  tier: must             # must = a wrong verdict is a scoring failure; calibration = borderline or convention-dependent, reported but never a failure
  reference: "F84"       # W3C technique/failure id(s) this element reproduces, e.g. "F25", "H30", "G197 + Understanding 3.2.4"; or "calibration-only (<why>)" when no public technique describes it
  polarity: failure      # failure = reproduces the technique's documented failure; sufficient = reproduces its documented sufficient/passing pattern
  clause1_evidence: true # false whenever reference is calibration-only
  loses: ["which page", "same title"]   # 2–5 short phrases; a rationale for a "no" should name at least one of these (what the PERSON loses). Empty list for "yes".
  evidence_contains: ["reserve books online"]  # phrases that MUST appear in the element's own text or its immediately surrounding text for the expected verdict to be decidable (the inventory captures the nearest text block); empty when the element alone decides
  evidence_absent: []    # phrases that must NOT be near the element (e.g. the destination name, for a card-grid "Learn more")
  pattern_group: null    # a short id shared by rows that are the same construct repeated (e.g. "id-links"), else null
  note: "one line for the human reviewer"
```

Every DEFECTIVE class must cite a W3C failure or technique id and reproduce that documented pattern faithfully (read the technique from memory; if unsure of the exact id, say so in `note` and still cite your best id). Every CLEAN row cites the sufficient-technique side (e.g. H30, G91, G197, H37, H44, H65, G131) or "calibration-only".

Unplanted incidental elements (nav links, a footer, an h1) will also be captured by the inventory tool; you do not need to list them — but do not accidentally make them defective. Keep incidental elements clearly fine.

## Fixtures and the class list you must cover

You MAY add classes; you may NOT drop any listed one. Cover each listed class with at least one element; put the clean counterparts in the same page or a sibling page so they are judged side by side.

1. `page-titles-shared` (type: title; SC 2.4.2). Defective: 3+ pages whose `<title>` is the bare site name only (F25). Clean: a page with site name + page-specific phrase; a page with a long formal institutional title (length alone is never a defect); a record-detail page titled "<record id> — <record name> — <site>".
2. `link-purpose-cards` (type: link; SC 2.4.4). Defective: a card grid with five "Learn more" links to five destinations, each card's text NOT naming its destination distinctively (F84 — non-specific link text such as "more"; `evidence_absent` = the destination name); a "Learn more" whose disambiguating text sits in an unrelated part of the page, not near the link (F63); a link whose text is the raw URL (`reference: "calibration-only (Understanding 2.4.4)"`, `clause1_evidence: false`); an icon-only link whose image alt names the icon ("arrow") (F89); a link to a `.pdf` whose text does not indicate the format (`calibration-only (Understanding 2.4.4)`, `clause1_evidence: false`). Clean: "Learn more" inside a paragraph that names the destination in the same sentence (H30 / G91 sufficient — `evidence_contains` = that destination phrase); an icon-only link whose `aria-label` names the destination (ARIA8 / H30); "Annual report (PDF, 2 MB)" (H30 sufficient); a table of 6 records where an ID column links `/records/<id>` and the row's name cell is in the same row — `pattern_group: "id-links"`, expected yes, `reference: "calibration-only (repeated construct)"`, `clause1_evidence: false`, `tier: calibration`.
3. `images-role-routing` (type: image; SC 1.1.1). Defective: alt that is a filename (F30); an `<img>` with no alt attribute at all (F65); an image that is the only content of a link with `alt=""` (F89 — functional image unnamed); an informative gauge/chart image whose alt names the appearance ("gauge") not the information (G94 failure side / F30 — say which in `note`). Clean: a decorative image `alt=""` beside a text label that already says the same thing (H67); an informative image whose alt conveys the data (e.g. "<invented index name> 42, Good") (G94); a complex chart with a short alt AND a `<figcaption>` carrying the data — `unsure_ok: true`, expected yes (G95 — long description adjacent).
4. `headings-fields-labels` (types: heading, field; SC 2.4.6). Defective: a form field labelled by placeholder only (`reference: "H44/G131 sufficient side absent (Understanding 2.4.6)"`, `polarity: failure` — the label disappears on input; do NOT cite F68, which belongs to 1.3.1/4.1.2); headings "Overview" and "Details" above sections whose first sentence shows exactly what specific heading was possible (G130 failure side; `evidence_contains` = that first sentence); an empty `<h2></h2>` (G130 failure side); a heading that is only a number ("24.3") (G130 failure side). Clean: a wrapping `<label>` (H44); an `aria-label`led search field (ARIA14 / H65); a long formal heading (`calibration-only (length)`, `clause1_evidence: false`, `tier: calibration`); on a specialist product (state the audience in scenario.md), a field label that is audience-standard shorthand — INVENT the abbreviation for a fictional specialist domain (do not reuse any real-world assay, index, or database name) — `reference: "calibration-only (audience shorthand)"`, `clause1_evidence: false`, `tier: calibration`, expected yes.
5. `identification-across-views` (type: ident, plus nav; SC 3.2.4 and 3.2.3). Provide 4–5 pages. Defective ident: the same destination linked as "Resources" in the header nav and "Help" in the footer on every page (G197 / Understanding 3.2.4 — inconsistent identification); a version-number link in the header and a "Release notes" link in the footer to the same page. Clean ident: a logo link `<a href="/"><img alt="<Org> home"></a>` plus a text link "Home" to `/` (G197 sufficient); "Contact" in the header and "Contact us" in the footer to `/contact.html` — borderline: expected yes, `unsure_ok: true`, `tier: calibration`, `clause1_evidence: false`. Also plant, for the DETERMINISTIC layer (type `nav` or `ident`, expected yes, note "deterministic"): a page with a table whose ID column and name column both link the same record (should NOT count as inconsistent identification); a map/tool page with two controls marked up as `<a href="javascript:void(0)">Zoom in</a>` (not destinations); a detail page that keeps the primary nav in the same order but adds a sub-navigation; primary nav in the SAME relative order on every page (one page may omit an item but never reorder).
6. `clean-control` — a well-built small site (3 pages, all six types present): descriptive distinct titles, specific headings, labelled fields, links whose purpose is clear from text or immediate context, correct alts (informative with data, decorative empty beside text), consistent identification, same nav order. Include one long formal title and one long formal heading, one INVENTED audience-standard abbreviation on a stated-specialist page (those three: `tier: calibration`, `clause1_evidence: false`), and one "Read more" link inside a sentence that names where it goes (`evidence_contains` = that name). EVERY listed element expected yes; list at least 12; each cites the sufficient technique it reproduces (`polarity: sufficient`).

## Rules
- Fictional everything. `.example` domains. No real orgs, agencies, people. Invent every abbreviation, index name, assay name, and database name you use; never reuse a real one.
- Two shorthand terms per specialist product at most, defined once in scenario.md so a reader can judge them.
- Never write the words "fixture", "planted", "defective", "test", "WCAG", technique ids, or hints into the HTML or scenario.md — only into expectations.yaml.
- Do not make the HTML broken in ways you did not plant (unclosed tags, missing `<main>`): the only defects present should be the ones in expectations.yaml.
- When done, write `<OUT>/PROVENANCE.md`: what you consulted (this brief + your own knowledge only), what you did not open, and the list of classes you added beyond the brief, if any.

Output directory `<OUT>`: /private/tmp/claude-501/-Users-AlexUA-1-claude-accessibility-skills/32d58053-bc70-4b0e-8af1-fc0509383d05/scratchpad/blind-fixtures

Report back only: the fixture ids written, per fixture the count of expected-no and expected-yes rows, and any class you were unsure how to reproduce.
