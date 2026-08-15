# Fixture: Standards Subscription Platform Evaluation Plan

## Feature Description

Meridian Standards Exchange is a subscription platform where engineers,
inspectors, and compliance officers pay to access technical safety and
construction standards documents — building codes, electrical codes,
structural specifications, and fire-safety bulletins — from a dozen
different issuing bodies. The catalog holds roughly 14,000 documents. Every
document has its own permanent page: title, scope note, adoption history,
and an "Add to Cart" control for the full text, which sits behind the
subscriber paywall.

Today there are two ways a subscriber can land on a given document's page:

- **Browse by Discipline** — a set of category pages showing only the
  roughly 2,600 documents considered currently maintained. Legal asked the
  product team to keep older, superseded editions out of Browse entirely,
  after several engineers complained that citing an outdated edition in a
  permit filing had caused problems for them. That exclusion is intentional
  and has not been revisited since.
- **Search** — a box indexing the title and keywords of all roughly 14,000
  documents, including superseded editions. For performance reasons, the
  search infrastructure, run by a subcontracted vendor, only ever shows a
  subscriber the top 200 matches for a query and stops there — anything
  ranked past that point in a query's matches never reaches the screen.
  Because superseded editions frequently share almost the same title as the
  current replacement ("Bridge Load Rating Manual, 3rd Ed." next to "...4th
  Ed."), a typical search for a popular topic already fills the visible
  matches with current editions before an older one ever ranks high enough
  to show. The documents still exist, still have working URLs, and are
  still purchasable — they simply never rank high enough to reach the
  subscriber once a query has enough current-edition matches to fill what
  the screen will show.

Superseded editions matter in practice: some municipal ordinances still
reference an old edition by name, so an engineer working from one of those
ordinances legitimately needs to find and buy the specific old edition, not
the current one.

## Context

- Meridian's largest customer — a 400-engineer, multi-state civil
  engineering firm — is up for its annual seat-license renewal, and its
  procurement office is requiring a signed accessibility conformance
  statement before signing.
- The sales engineering team already told that customer's procurement
  staff, in an email the accessibility lead was later copied on, that the
  platform "lets a subscriber find any document at least two ways — browse
  and search." Nobody on sales mentioned the search ranking behavior
  described above, or the Browse exclusion, when they said it.
- The customer is separately bringing in its own outside accessibility
  auditor to test the platform independently before the procurement office
  signs. That auditor has not started yet.
- A member of Meridian's legal team, in an offhand comment nobody has
  followed up on, described the individual document page — with its
  "Add to Cart" control for the paywalled full text — as "just a step in
  the purchase flow." No one on the accessibility or product team has
  confirmed or challenged that description.
- Superseded editions remain purchasable and citable; the product team has
  no plan to remove them from the catalog.
- This engagement covers the authenticated subscriber catalog and document
  pages only; Meridian's public marketing site was evaluated separately
  last quarter and is out of scope here.
- Timeline: six weeks before the renewal signature date.
- Team: one accessibility lead, with part-time help from one front-end
  engineer.
- An automated scanner already runs weekly against the platform's roughly
  30 page templates. It has never flagged anything related to the search
  ranking behavior described above or the Browse exclusion, since both are
  business logic decisions rather than markup errors.

## Requirement

Plan the engagement. The plan should say:

- What you would examine, and how, given the situation described above.
- Whether — right now, today — a subscriber can find any given document at
  least two ways, and what you are prepared to say about that.
- What you do with the "just a step in the purchase flow" description of
  the document page before it reaches the outside auditor.
- What you tell the accessibility lead to say back to the sales team about
  the claim already made to the customer's procurement office.
- What, if anything, changes in the product before the renewal date, and
  what instead gets reported as a known, dated limitation.
- What you say to the customer's outside auditor when they arrive to test
  independently.

The plan goes to the accessibility lead, who will use it to brief both the
product team and the customer's procurement contact — the procurement
contact is not a technical reader.
