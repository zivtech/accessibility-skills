# Example client-standards yardstick: EPA web standards (verified live 2026-09-02)

This is the worked example from the origin run. Copy the shape, not the rules: verify each rule on
the client's live page, quote it verbatim, record the URL and last-updated date, give it an id, and
name the captured fact it fires on.

The engagement owner ruled that the client's own published web standards are a yardstick beside WCAG. Every rule below was fetched from the live page on 2026-09-02 and is
quoted verbatim; the `last updated` date is the page's own. Rule ids are this engagement's, for
citation in `standards.jsonl` and the CSV (`client_rules` / `client_result` / `client_note`). A rule is applied only where the captured row shows the
fact the rule speaks to; it never substitutes for a WCAG outcome.

| Rule id | Standard (page title, last updated) | Verbatim rule | Row types it decides |
|---|---|---|---|
| EPA-LINK-1 | Web Standard: Link Text (2026-07-14) — https://www.epa.gov/web-policies-and-procedures/web-standard-link-text | "Use link text that clearly describes the linked page or page section." | link |
| EPA-LINK-2 | same | "Do not use general link text such as: More info, Learn more, Click here, More, here" | link (generic text) |
| EPA-LINK-3 | same | "Do not use the same link text for different links in the body of your web page." | link (same text, different destinations) |
| EPA-LINK-4 | same | "Do not use the website address (URL) for link text unless you are trying to get your visitor to remember the URL" | link (raw URL text) |
| EPA-LINK-5 | same | "When linking to other file formats, follow this format: Document Title (docx), including the file extension in the link" | link (file) |
| EPA-LINK-6 | same | "When adding a link to content in a different language than your page, include \"(in LANGUAGE)\" in the link." | link (other-language) |
| EPA-FILE-1 | Web Standard: File Links, Formats, and PDF Guidelines (2026-07-14) — https://www.epa.gov/web-policies-and-procedures/web-standard-file-links-formats-and-pdf-guidelines | "All websites must include file extension indicators for non-HTML links. The file type (e.g., pdf, docx) must be displayed next to the link text." | link (file) |
| EPA-HEAD-1 | Web Standard: Headings (2026-06-10) — https://www.epa.gov/web-policies-and-procedures/web-standard-headings | "The page title of all EPA pages is an <h1> element. Only the page title can be <h1>." | title row (h1 count), heading |
| EPA-HEAD-2 | same | "Use <h2> to <h6> in the proper descending order. These headings should be used as you would an outline structure. Any skipping of levels breaks the flow of the page for readers." | heading (level skip) |
| EPA-HEAD-3 | same | "Do not add hyperlinks to headings." | heading |
| EPA-HEAD-4 | same | "A general rule of thumb is between 30-60 characters." (heading length; rule of thumb, not a must) | heading (advisory only) |
| EPA-TITLE-1 | Web Standard: Writing for the Web (2025-11-06) — https://www.epa.gov/web-policies-and-procedures/web-standard-writing-web | "Page titles should be unique and distinct to avoid having the same content on two different pages." | title |
| EPA-TITLE-2 | same | "Do not use words like More, Additional, Other, Related or Further at the start of page titles." | title |
| EPA-IMG-1 | Web Standard: Graphics (Images, photos, infographics) (2025-11-06) — https://www.epa.gov/web-policies-and-procedures/web-standard-graphics-images-photos-infographics | "Decorative photos should use empty alt text. The final code should read (alt=\"\")." | image (decorative) |
| EPA-IMG-2 | same | "Graphics should have alt text or captions because the image adds context to the page and needs an explanation." | image (informative) |
| EPA-IMG-3 | same | "Do not use images that include text." | image (text in image) |
| EPA-IMG-4 | same | "Information conveyed in an infographic should be provided in a text alternative on the same page or in a section 508 compliant pdf." | image (complex) |
| EPA-IMG-5 | same | "Graphics must provide sufficient color contrast for visitors with visual disabilities, and visitors who cannot view the information provided through graphics must have access to equivalent information." | image (informative) |
| EPA-MAP-1 | Web Standard: Maps (2026-05-12) — https://www.epa.gov/web-policies-and-procedures/web-standard-maps | "A description in caption text or alt text of what the map displays." (required element) | image (map) |
| EPA-MAP-2 | same | "A link to equivalent content in text form." (required element) | image (map) |
| EPA-MAP-3 | same | maps must include "A title, that includes the word 'map', located above the map in header tag <h2> – <h4>." | heading (map pages) |
| EPA-WIN-1 | Web Standard: Linking to Related Content via Pop-ups, Overlays, New Browser Tabs/Windows and Same Browser Tabs/Windows (2026-06-22) — https://www.epa.gov/web-policies-and-procedures/web-standard-linking-related-content-pop-ups-overlays-new-browser | "Do not use pop-ups, overlays, new windows or browser tabs unless the content they display is closely related to the content in the existing window" | link (new window) |
| EPA-WIN-2 | same | "When displaying closely related content, if the content opens in a pop-up, overlay, new window or tab, use descriptive text after or nearby the link to warn your visitors" | link (new window) |
| EPA-WIN-3 | same | "Do not force downloading of PDF files. PDFs should open in the browser." | link (file) |
| EPA-EXT-1 | Procedure: External Site Links (2026-07-17) — https://www.epa.gov/web-policies-and-procedures/procedure-external-site-links | "Use the 'Exit EPA' icon to identify external links." / "Any link to a site that is not controlled by EPA is considered an external link." | link (external) — not captured by this inventory (icon presence not recorded); noted, not applied |
| EPA-FORM-1 | Web Standard: Web Forms (2026-08-28) — https://www.epa.gov/web-policies-and-procedures/web-standard-web-forms | "Use title case (initial capital letters) for labels. Never use all caps." | field — no label-presence rule on this page; label presence stays a WCAG 2.4.6 / 1.3.1 / 4.1.2 matter |
| EPA-A11Y-1 | Web Standard: Accessibility (2026-08-28) — https://www.epa.gov/web-policies-and-procedures/web-standard-accessibility | "Meet the standards established for the federal government for Web-based intranet and internet information and applications." (Revised Section 508, E205 Electronic Content → WCAG 2.0 AA by incorporation) | all — the floor; the lane's target is WCAG 2.2 AA |

Pages checked and found to carry no applicable rule sentence: Web Standard: Logos and Icons
(2025-11-06; program-icon approval only), Image Guidance (2026-07-13; editorial image quality only).

## Which standard EPA tests to (verified from the procedure PDF, 2026-09-02)

**Section 508 Testing Procedure**, IT/IM Directive CIO 2130-P-03.1, signed 2022-09-06
(https://www.epa.gov/system/files/documents/2025-02/section_508_testing_procedure.pdf). It names
"A test process aligned with the ICT Testing Baseline" and "EPA's preferred testing protocol, the
Interagency Trusted Tester Process", and lists "WCAG 2.0, Web Content Accessibility Guidelines, W3C
Recommendation" among its references. Rule id **EPA-TEST-1**: EPA's own conformance floor is
Revised Section 508 (WCAG 2.0 AA by incorporation) tested per the ICT Testing Baseline / Trusted
Tester. This lane's target, WCAG 2.2 AA, is stricter; every row that fails here also fails there
except the 2.2-only criteria, which are not in the B3 set. The Data Visualization / GIS
Accessibility Procedure linked from the 508 policies page returned HTTP 404 on 2026-09-02.

## How the pass applies the rules (engagement script `b3-epa-standards-pass.mjs`, not yet generalized)

A rule fires only on a captured fact: the link text itself, the `href` extension, the h1 count, a
flag the builder computed, or an owner-ratified decorative status (EPA-IMG-1 on F3 only). It writes
`standards.jsonl` and the merge renders `client_rules` / `client_result` / `client_note`. Rules with
no captured fact (EPA-HEAD-3 hyperlinked headings, EPA-IMG-3 images of text, EPA-WIN-3 forced PDF
download, EPA-EXT-1 Exit-EPA icon, EPA-MAP-2 text-equivalent link) are listed and not applied.
