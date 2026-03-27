# A11y-Critic Evaluation Suite: Fixture Inventory

## Complete Fixture List (10 fixtures)

### Interactive Widgets Domain (3 fixtures)

1. **interactive-dropdown-clean** [CLEAN]
   - Files: `interactive-dropdown-clean.md`, `.metadata.yaml`
   - Type: Custom dropdown component
   - Issues: None (baseline for accuracy/false positives)
   - WCAG: 1.3.1, 2.1.1, 2.1.2, 4.1.2
   - APG Pattern: Listbox
   - Code: 150 lines (React + CSS)
   - Status: ✅ Complete

2. **interactive-dropdown-focus-bug** [HAS-BUGS]
   - Files: `interactive-dropdown-focus-bug.md`, `.metadata.yaml`
   - Type: Custom dropdown with incomplete focus management
   - Issues: Focus not restored on selection (MAJOR), focus not restored on Escape (MAJOR)
   - WCAG: 2.1.2
   - APG Pattern: Listbox (incomplete)
   - Code: 120 lines (React)
   - Status: ✅ Complete

3. **modal-complete-clean** [CLEAN]
   - Files: `modal-complete-clean.md`, `.metadata.yaml`
   - Type: Modal dialog component
   - Issues: None (focus trap, focus restoration complete, Escape works)
   - WCAG: 2.1.1, 2.1.2, 2.4.3, 4.1.2
   - APG Pattern: Modal Dialog
   - Code: 200 lines (React + CSS)
   - Status: ✅ Complete

### Form & Validation Domain (2 fixtures)

4. **form-validation-missing-aria-describedby** [HAS-BUGS]
   - Files: `form-validation-missing-aria-describedby.md`, `.metadata.yaml`
   - Type: Login form with validation errors
   - Issues: Errors not associated to fields via aria-describedby (CRITICAL), error summary not announced (MAJOR)
   - WCAG: 1.3.1, 4.1.2, 4.1.3
   - APG Pattern: Form Validation
   - Code: 180 lines (React + CSS)
   - Status: ✅ Complete

5. **loading-state-missing-aria-busy** [HAS-BUGS]
   - Files: `loading-state-missing-aria-busy.md`, `.metadata.yaml`
   - Type: Data loader with visual spinner
   - Issues: No aria-busy (CRITICAL), no aria-live announcement (MAJOR)
   - WCAG: 4.1.3
   - APG Pattern: Live Regions
   - Code: 100 lines (React + CSS)
   - Status: ✅ Complete

### Content & Semantic Structure Domain (2 fixtures)

6. **data-table-missing-scope** [HAS-BUGS]
   - Files: `data-table-missing-scope.md`, `.metadata.yaml`
   - Type: Sales data table
   - Issues: Column headers missing scope="col" (MAJOR), row headers missing scope="row" (MAJOR)
   - WCAG: 1.3.1
   - APG Pattern: Data Table
   - Code: 100 lines (React + CSS)
   - Status: ✅ Complete

7. **heading-hierarchy-skipped** [HAS-BUGS]
   - Files: `heading-hierarchy-skipped.md`, `.metadata.yaml`
   - Type: Blog post article
   - Issues: h1 jumps to h3 skipping h2 (MAJOR), inconsistent h3→h2 (MAJOR)
   - WCAG: 1.3.1
   - APG Pattern: Heading Structure
   - Code: 100 lines (React + CSS)
   - Status: ✅ Complete

### Focus Management & Keyboard Domain (1 fixture)

8. **button-skip-link-clean** [CLEAN]
   - Files: `button-skip-link-clean.md`, `.metadata.yaml`
   - Type: Main layout with skip link
   - Issues: None (skip link functional, landmarks correct, focus indicators visible)
   - WCAG: 2.4.1, 1.3.1
   - APG Pattern: Skip Navigation
   - Code: 150 lines (React + CSS)
   - Status: ✅ Complete

### Dynamic Content & Live Regions Domain (2 fixtures)

9. **search-results-dynamic-clean** [CLEAN]
   - Files: `search-results-dynamic-clean.md`, `.metadata.yaml`
   - Type: Search with dynamic results
   - Issues: None (aria-live, role="status", aria-atomic correct)
   - WCAG: 4.1.3
   - APG Pattern: Live Regions
   - Code: 120 lines (React + CSS)
   - Status: ✅ Complete

10. **tabs-missing-arrow-nav** [HAS-BUGS]
    - Files: `tabs-missing-arrow-nav.md`, `.metadata.yaml`
    - Type: Tabs widget
    - Issues: Arrow key navigation not implemented (MAJOR), active tab not focused after selection (MINOR)
    - WCAG: 2.1.1, 4.1.2
    - APG Pattern: Tabs (incomplete)
    - Code: 140 lines (React + CSS)
    - Status: ✅ Complete

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Fixtures** | 10 |
| **CLEAN Fixtures** | 4 (baseline accuracy tests) |
| **HAS-BUGS Fixtures** | 6 (issue detection tests) |
| **FLAWED Fixtures** | 0 (planned) |
| **ADVERSARIAL Fixtures** | 0 (planned) |
| **Domains Covered** | 5 of 6 (missing: Color/Motion/Sensory) |
| **Total Component Code** | ~1,300 lines |
| **Total Documentation** | ~800 lines (metadata) |
| **WCAG Criteria** | 10+ covered |
| **APG Patterns** | 6 covered |

---

## Difficulty Distribution

- **CLEAN** (4 fixtures): interactive-dropdown-clean, modal-complete-clean, button-skip-link-clean, search-results-dynamic-clean
- **HAS-BUGS** (6 fixtures): interactive-dropdown-focus-bug, form-validation-missing-aria-describedby, loading-state-missing-aria-busy, data-table-missing-scope, heading-hierarchy-skipped, tabs-missing-arrow-nav

## Domain Distribution

| Domain | Fixtures | Count |
|--------|----------|-------|
| Interactive Widgets | dropdown-clean, dropdown-focus-bug, modal-clean | 3 |
| Form & Validation | form-validation-bugs, loading-state-bugs | 2 |
| Content & Semantic Structure | data-table-scope, heading-hierarchy | 2 |
| Focus Management | skip-link-clean | 1 |
| Dynamic Content & Live Regions | search-results-clean, tabs-arrow-nav | 2 |
| Color, Motion, & Sensory | — | 0 |

---

## Rubrics & Baselines

### Rubrics Provided
- ✅ interactive-dropdown-clean.rubric.yaml (CLEAN fixture example)
- ✅ interactive-dropdown-focus-bug.rubric.yaml (HAS-BUGS fixture example)

Template available for remaining 8 fixtures (follow same structure).

### Baselines Available
- ✅ baseline-zero-shot.md (generic review prompt)
- ✅ baseline-few-shot.md (generic + structure + example)

---

## File Checklist

```
fixtures/
  ✅ interactive-dropdown-clean.md (150 lines)
  ✅ interactive-dropdown-clean.metadata.yaml
  ✅ interactive-dropdown-focus-bug.md (120 lines)
  ✅ interactive-dropdown-focus-bug.metadata.yaml
  ✅ modal-complete-clean.md (200 lines)
  ✅ modal-complete-clean.metadata.yaml
  ✅ form-validation-missing-aria-describedby.md (180 lines)
  ✅ form-validation-missing-aria-describedby.metadata.yaml
  ✅ loading-state-missing-aria-busy.md (100 lines)
  ✅ loading-state-missing-aria-busy.metadata.yaml
  ✅ data-table-missing-scope.md (100 lines)
  ✅ data-table-missing-scope.metadata.yaml
  ✅ heading-hierarchy-skipped.md (100 lines)
  ✅ heading-hierarchy-skipped.metadata.yaml
  ✅ button-skip-link-clean.md (150 lines)
  ✅ button-skip-link-clean.metadata.yaml
  ✅ search-results-dynamic-clean.md (120 lines)
  ✅ search-results-dynamic-clean.metadata.yaml
  ✅ tabs-missing-arrow-nav.md (140 lines)
  ✅ tabs-missing-arrow-nav.metadata.yaml

rubrics/
  ✅ interactive-dropdown-clean.rubric.yaml
  ✅ interactive-dropdown-focus-bug.rubric.yaml

baselines/
  ✅ baseline-zero-shot.md
  ✅ baseline-few-shot.md

Documentation/
  ✅ skill-profile.md (11 KB)
  ✅ domain-sampling-strategy.md (14 KB)
  ✅ statistical-design.md (12 KB)
  ✅ eval.yaml (8 KB)
  ✅ README.md (13 KB)
  ✅ BUILD_SUMMARY.md (13 KB)
  ✅ FIXTURE_INVENTORY.md (this file)
```

---

## Extensibility

The suite is designed to expand:
- Add FLAWED fixtures (3-5 more; 3-5 subtle issues each)
- Add ADVERSARIAL fixtures (2-3 more; edge cases, defensible patterns)
- Add Color/Motion/Sensory fixtures (2-3)
- Target: 25-30 total fixtures for full statistical power

For each new fixture, create:
1. `{fixture-name}.md` — component code (real code, 100-200 lines)
2. `{fixture-name}.metadata.yaml` — expected findings, WCAG citations, verdict
3. `{fixture-name}.rubric.yaml` — scoring dimensions (optional, use template)

---

**Last Updated**: 2026-03-09
**Status**: Complete with 10 fixtures; ready for pilot and full evaluation
