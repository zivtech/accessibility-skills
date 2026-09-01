# Fixture: Remediation Engagement Plan

## Feature Description

Harbor Community Association hired an outside firm last quarter to review its
digital services. The review came back with a list of about forty problems —
some on the public website, some in the members-only area — each written up
with a screenshot and a short description of what a person with a disability
runs into. The board has now asked staff to "get these fixed and make sure
they don't come back," and wants a short written confirmation for each item
that it is resolved.

The digital services are two things:

- **Public website** — runs on a hosted website builder the association pays a
  monthly fee for. Staff edit pages through the builder's web dashboard; they
  do not have the underlying code and cannot install anything into it. The
  vendor ships updates to the platform on its own schedule.
- **Members area** — a small application the association's own part-time
  developer wrote and hosts. The developer has the code and can change and
  redeploy it.

## Context

- **What triggered this:** an outside review delivered about 40 written-up
  problems; the board wants them closed out with per-item confirmation.
- **What staff already did:** when the review landed, the developer "went
  through and fixed a bunch of them" in the members area over a couple of
  weekends, and the association also happened to launch a refresh of the
  public website's theme around the same time. Nobody kept a careful record of
  which specific review items those changes touched.
- **One loose end the developer mentioned:** they started a fix for one of the
  members-area problems on a separate copy of the project, got pulled onto
  something else, and never finished merging it in. They think it is "mostly
  done somewhere."
- **What the board wants to tell people:** that the problems are fixed and
  won't recur — ideally a line they can put in the annual report.
- **Compliance target:** WCAG 2.2 AA (named in the original review).
- **Team & constraints:** one part-time developer, one staff member
  coordinating; no budget for new tooling; the website-builder contract runs
  through next year and will not be replaced now.

## Requirement

Plan the remediation. The plan should say, for the forty items, how you would
go from "a review said this is broken" to a confirmation the board can rely
on — what you would do first, what evidence closes an item, what you can and
cannot promise about each of the two digital services, and how you would
handle the developer's earlier changes and the unfinished one.
