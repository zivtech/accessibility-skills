# Content Authoring

## Responsibility

Content authoring ensures that text, media, structure, and language are accessible to all users. This role owns alt text, heading hierarchy, link text, transcripts, captions, plain language, error messages, and the semantic meaning that makes content navigable and understandable.

## Also Known As

Content designer, content strategist, technical writer, editor, information architect, UX writer, communications specialist.

## What This Role Sees

- Whether images have meaningful, non-redundant alt text
- Whether headings form a logical hierarchy that reflects document structure
- Whether link text makes sense out of context (not "click here" or "read more")
- Whether transcripts and captions exist for all media
- Whether plain language is used throughout
- Whether error messages explain what went wrong and how to fix it
- Whether form instructions are clear before users attempt input
- Whether consistent terminology is used across the interface
- Whether page titles are unique and descriptive
- Whether language of page and language changes are identified

## Blind Spots (What This Role Misses)

| Gap | Ask instead |
|-----|-------------|
| Whether HTML implementation matches content intent | Front-End Development |
| Whether the interaction pattern is keyboard-accessible | UX Design |
| Whether color contrast meets minimums | Visual Design |
| Whether the page works with real AT | Testing |

## ARRM Task Ownership

### Primary (42 tasks)

Key areas:
- **Images** — Alt text, decorative image handling, complex image descriptions (1.1.1)
- **Structure** — Headings, page titles, semantic organization (2.4.2, 2.4.6)
- **Links** — Link purpose from text alone, consistent link text (2.4.4, 2.4.9)
- **Forms** — Labels, instructions, error messages (3.3.1, 3.3.2, 3.3.3)
- **Media** — Transcripts, captions, audio descriptions, sign language (1.2.1–1.2.9)
- **Tables** — Headers, captions, summary descriptions (1.3.1)
- **Language** — Plain language, page language, language changes, glossary (3.1.1–3.1.6)

### Secondary (33 tasks)

Supports Front-End Dev on semantic markup, UX Design on consistency, and media player captioning implementation.

### Contributor (10 tasks)

Advises on visual-only information (color, shape, location), dynamic content announcements, and orientation-dependent content.

## Key WCAG Criteria

| SC | Level | What it requires |
|----|-------|-----------------|
| 1.1.1 | A | Non-text content has text alternatives |
| 1.2.1 | A | Audio-only and video-only have alternatives |
| 1.2.2 | A | Captions for prerecorded audio in video |
| 1.2.5 | AA | Audio description for prerecorded video |
| 2.4.2 | A | Page titled |
| 2.4.4 | A | Link purpose from link text (in context) |
| 2.4.6 | AA | Headings and labels are descriptive |
| 3.1.1 | A | Language of page identified |
| 3.1.2 | AA | Language of parts identified |
| 3.3.1 | A | Error identified in text |
| 3.3.2 | A | Labels or instructions provided |

## Review Checklist

When reviewing from this role's perspective, evaluate:

1. **Alt text** — Every informative image has alt text that conveys the same information a sighted user gets. Decorative images have `alt=""`. Complex images (charts, diagrams) have extended descriptions. No "image of" or "photo of" prefixes.
2. **Heading hierarchy** — One `h1` per page, no skipped levels, headings describe their section content, not just style/size.
3. **Link text** — Every link makes sense read in isolation. No "click here," "read more," "learn more" without context. Downloads indicate file type and size.
4. **Media alternatives** — Every video has captions. Every audio has a transcript. Complex video has audio description. Live events have real-time captions.
5. **Plain language** — Content uses the simplest language appropriate for the audience. Jargon is defined on first use. Abbreviations are expanded.
6. **Error messages** — Each error says: what field, what's wrong, and how to fix it. Not just "invalid input."
7. **Form instructions** — Required fields are indicated before the form. Format requirements are stated before input (not just in placeholder). Constraints are visible.
8. **Page titles** — Unique, descriptive, follow a consistent pattern (page name – site name).
9. **Language identification** — `lang` attribute on `<html>` matches content language. Inline language switches marked with `lang` attribute on the containing element.
10. **Consistent terminology** — Same concept uses the same word throughout. No synonym drift (login/sign in/log on for the same action).

## Collaboration Points

| Role | What to share | What to ask them |
|------|---------------|-----------------|
| Front-End Dev | Alt text content, heading outline | "Is my alt text properly rendered by screen readers?" |
| UX Design | Error message copy, form instructions | "Does the interaction flow match the content flow?" |
| Visual Design | Content hierarchy needs | "Does the visual weight match the semantic importance?" |
| Testing | Content samples for AT testing | "Does this alt text make sense when read aloud?" |
| Business Analysis | Plain language requirements | "Does this meet our readability requirements?" |
