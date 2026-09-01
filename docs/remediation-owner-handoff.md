# Remediation Owner Handoff

On a public product with no source access, remediation verification has a hard ceiling: black-box retest. A black-box retest can confirm that a specific interaction now behaves correctly in the live product — it cannot confirm that a source-level regression test exists, runs in CI, or will catch a future reintroduction of the same defect. Crossing from black-box retest into a true source-level regression gate requires specific things from the product owner, not from the testing party. Until they exist, "we added a regression test" is not an available claim, and the engagement should say so plainly rather than approximate it.

## The minimum handoff

A source-level regression gate cannot exist without all ten of the following from the product owner:

| # | Item | Why it's load-bearing |
|---|---|---|
| 1 | **Named owners** | Someone who can authorize and receive the remaining nine items — without a named owner, none of the rest is requestable. |
| 2 | **Repository plus commit** | The exact source location and revision the live product corresponds to — a regression test has to run against *something*. |
| 3 | **Build recipe** | How to produce a running instance from that source — a test cannot execute against source it cannot build. |
| 4 | **Finding-to-component mapping** | Which source file(s) or component(s) each finding traces to — without this, a fix is guesswork even with source access. |
| 5 | **Runnable fixtures** | Test data or scenarios that reproduce the conditions each finding was found under. |
| 6 | **An authorized test environment** | Somewhere the retest is permitted to run repeatedly without violating the product owner's terms of use. |
| 7 | **Existing test locations** | Where current tests (if any) live, so a new regression test extends the existing suite rather than starting a parallel, unmaintained one. |
| 8 | **A route/state inventory** | The set of routes, states, and viewports the regression gate is expected to cover — without it, "covered" is undefined. |
| 9 | **Release-acceptance authority** | Confirmation of who decides whether the regression gate's result blocks a release — a gate nobody is authorized to enforce is a suggestion, not a gate. |
| 10 | **A confirmation channel** | A way to check the other nine against reality as the engagement proceeds — ownership, environments, and test locations drift, and a stale assumption here invalidates the gate silently. |

## What this changes about scoping

This is a **scoping artifact**, not a technical one: it tells a commissioner what a real regression gate costs *before* anyone writes a test, so the choice between "black-box retest only" and "source-level regression gate" is made explicitly rather than discovered partway through an engagement. Naming the gap is itself a deliverable — a plan or report that claims a regression gate is available without confirming these ten items is asserting something no black-box position can support.

## Boundaries

- This document does not itself constitute a regression test, a CI configuration, or a test plan — it is the precondition checklist for one.
- It does not apply to engagements with source access from the start; there, the relevant question is normal test-coverage planning, not this ceiling.
- A partially-met list (for example, owners and a repository but no authorized test environment) does not unlock a partial regression gate — treat any missing item as blocking until it is resolved, and say which items are missing rather than rounding up.
