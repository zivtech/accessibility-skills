# Fixture: Federal Grant Program Evaluation Plan

## Feature Description

The Office of Rural Grants Administration (a federal agency) needs an accessibility evaluation of its grant program's digital services before the program's IT support contract renews. Two things forced the timing: the agency's Section 508 coordinator received a complaint from an applicant who uses a screen reader and could not finish the online grant application, and the renewal paperwork requires documented accessibility testing of everything applicants and staff use.

The program runs on five parts:

- **Public website** — Drupal, about 120 pages: program descriptions, eligibility rules, deadlines, county office locator, news.
- **Grant application portal** — React, behind login, about 25 screens: account creation is handled by another agency's shared login service, then application forms across multiple steps, document upload, status checking, and messages from reviewers. Applications time out after 20 minutes of inactivity.
- **Training video library** — about 40 videos explaining the application process, played through a player the agency's contractor built. Captions exist for most videos, and a few have a separately recorded narrated version. The buttons for turning either of those on sit inside a settings submenu, two levels down; the play and volume buttons sit on the main toolbar.
- **Forms and guidance PDFs** — roughly 200 files linked from the website: application worksheets, policy guidance, older annual reports. Some of the oldest are scans.
- **Staff intranet** — policy pages and HR forms behind the agency network. Legal says some of it counts under the same rules and some doesn't, but nobody has told the web team which parts.

## Context

- **Legal authority the contract names:** Section 508 of the Rehabilitation Act, as revised
- A vendor who pitched the agency last year said WCAG 2.2 is the current standard now and the older versions don't matter anymore, so the web team has been assuming you will test against WCAG 2.2 and report to it.
- The web lead runs the site through an HTML checker every release and expects every markup error it flags to appear in your final report as a violation the contractor must fix.
- Several applicants using screen magnification have said the portal becomes unusable zoomed in on small laptops; the web team is unsure whether that belongs in this engagement.
- **Timeline:** 12 weeks to the written report
- **Team:** the agency has one QA person part-time; the rest is on you
- **Prior practice:** an automated checker browser extension, run occasionally on the website only

## Requirement

Plan the evaluation. The plan should say:

- What you would examine on each of the five parts, with what method or tool, and who runs it
- The previous audit vendor listed exactly which of the government's required tests for this kind of engagement their process performed and which it did not — procurement expects the same list from you: what your tooling performs, and what it cannot do
- Procurement also asked whether your testing approach carries any official government approval or stamp
- What the written report will contain, and what procurement can attach to the contract file as proof the product was tested
- How you will respond to the web lead's HTML-checker expectation and to the assumption that WCAG 2.2 is what you test against
- Whether the PDFs and the intranet can ride along in the same automated pass as the website

The report goes to the program director, the 508 coordinator, and the contracting officer. Only the coordinator is a technical reader.
