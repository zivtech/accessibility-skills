# Pre-declaration of the PT-06 decision rule (receipt)

The threshold the Alfa measurement was judged against was stated **before the run**, in the spawn instructions the measuring agent received (session 2026-09-02, agent started ~13:36 UTC; `overlap-table.md` was generated at 13:57:10 UTC per its own header). The relevant instruction text, verbatim:

> GOAL: measure whether the Siteimprove Alfa open-source ACT engine detects WCAG 2.2 A/AA defect classes that axe-core + HTML_CodeSniffer (htmlcs via pa11y) miss, on the same public pages. Pre-declared threshold (do not soften it): Alfa is a "threshold candidate" only if it fails ≥3 distinct A/AA rule classes (distinct Alfa rules mapping to A/AA criteria, FAILED outcomes only, not cantTell) that neither axe nor htmlcs flagged on the same page, AND at least one of those is a plausible true positive when you inspect the target. Otherwise "below threshold". Report either outcome plainly.

The same rule appears in the program plan (item 1.1) written before the agent was spawned. What this receipt does **not** establish: that ≥3 was the *right* bar. The rule tested one of the three value propositions in the candidate's JTBD (coverage widening); cross-checking was observed to succeed (`README.md` § Analysis) and EARL-native output was not measured at all. See the dispositions document for the scoped verdict.
