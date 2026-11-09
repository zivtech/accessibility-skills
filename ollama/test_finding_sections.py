#!/usr/bin/env python3
"""Layout coverage for the CLEAN false-finding counter.

The four patterns this counter used until 2026-10-23 passed every test in
test_score_output_contracts.py while recording 1 finding across the 11 CLEAN
receipts that hold 17 at the same severity threshold -- and that 1 came from an
evidence-contract block, not a finding. The gap was in the fixtures, not only
the regex: every sample was written in the one layout the patterns recognised.
Each layout below is transcribed from a real receipt, named in the docstring,
so a future format change breaks a test instead of silently returning zero.

Layout coverage asserts on ``total_detected``, which no severity threshold can
move. ``total`` is asserted separately, in the ``test_minor_*`` tests, so a
later change of threshold cannot be mistaken for a parser regression.
"""

from finding_sections import ALL_SEVERITIES, count_findings
from score_output import count_false_positives

# evidence/receipts/ziv22-blind-ab-2026-10-23/blind/interactive-dropdown-clean-detector.md
# Severity group heading in bold, finding title in the bold slot. This is the
# layout that scored 0 while carrying 4 findings.
BOLD_GROUP_HEADINGS = """# Verdict: REVISE

**Pre-commitment Predictions**:
1.  **Focus/Selection Sync Gap**: Custom dropdowns often update internal state.
2.  **Missing Click-Outside Handling**: Keyboard users may get lost.

**Critical Findings** (blocks access):
1.  **Screen Reader Navigation Feedback Missing**
    - **Evidence**: `src/components/DropdownSelect.tsx:48`.
    - **Fix**: Implement `aria-activedescendant`.

**Major Findings** (significantly degrades experience):
1.  **Missing Click-Outside Handling**
    - **Evidence**: `src/components/DropdownSelect.tsx:10`.
2.  **Listbox Accessible Name**
    - **Evidence**: `src/components/DropdownSelect.tsx:50`.

**Minor Findings** (friction but workaround exists):
- **Conditional Rendering Stability**: The listbox is conditionally rendered.

**What's Missing** (gaps, unhandled edge cases):
- **`aria-activedescendant` implementation**: not bridged to the a11y tree.
- **Focus restoration on click-outside**: no mechanism.
"""

# .../blind/async-retry-recovery-clean-detector.md
# Same grouping, `###` headings instead of bold, and an empty Critical section.
HASH_GROUP_HEADINGS = """# Verdict: ACCEPT

## Findings

### Critical Findings
None. The component implements persistent live regions correctly.

### Major Findings
1. **Missing `aria-busy` during loading state**
   - **Evidence:** `AccountActivityPanel.jsx:24` (loading branch).
   - **Fix:** Add `aria-busy="true"` to the `<section>`.

### Minor Findings
1. **List item context (Payee/Amount)**
   - **Evidence:** `AccountActivityPanel.jsx:48-50`.

### Enhancements
1. **Parent Contract: Button Disabling**
   - **Evidence:** `Expected Behavior` section.

## Multi-Perspective Notes
- **Screen reader user:** Hears section heading, button, and status updates.
- **Keyboard-only user:** Tab order is logical.
"""

# evals/results/context-utilization-phase3/rows-hosted/
#   claude-evidence-lane-button-skip-link-clean-curated-hosted-draw1-opus-response.md
# Claude: severity-prefixed finding heading, no group heading. Finding bodies
# carry top-level bullets that must not be counted as findings themselves.
SEVERITY_PREFIXED_HEADINGS = """# Accessibility Design Review

**VERDICT: REVISE**

## Findings

### MAJOR 1 — Focus indicator measures 2.27:1; WCAG requires 3:1
**Evidence** — `MainLayout.css:42-45`.
- `#0066cc` -> L = **0.13866**
- `#333333` -> L = **0.03310**
- **Confidence: HIGH.** The arithmetic is deterministic.

### MINOR 1 — Skip-link target has no `tabindex="-1"`
- **User group:** keyboard-only users.

### MINOR 2 — No current-page indication, programmatic or visual
- **WCAG:** 2.4.8 Location (AAA).

## Enhancements (best practice not met, no access barrier)
- Consider a visible focus style on the footer links.
"""

# .../claude-evidence-lane-modal-complete-clean-curated-hosted-draw1-opus-response.md
# Claude: severity group heading with deeper sub-headings. The sub-heading is
# the finding; the bullets inside it are its fields.
GROUP_PLUS_SUBHEADINGS = """# Accessibility Design Review

**VERDICT: ACCEPT-WITH-RESERVATIONS**

## Critical Findings (blocks access)
None.

## Major Findings (significantly degrades experience)
### M1 — The focusable-element predicate admits elements that cannot be focused
- **User group:** keyboard-only and screen reader users. Both.
- **WCAG:** 2.1.1 Keyboard and 2.4.3 Focus Order.
- **Confidence: HIGH** on the mechanism.

## Minor Findings (friction, workaround exists)
### M2 — The enumerated focusable set omits several tabbable element types
- **WCAG:** 2.1.1 Keyboard.
### M3 — `id="modal-title"` is hardcoded, so label association collides
- **WCAG:** 4.1.2 Name, Role, Value.

## Enhancements (best practice not met, no access barrier)
### E1 — Consider documenting the focus contract
"""

# The layout the original four patterns were written for.
INLINE_SEVERITY_TAGS = """Verdict: REVISE

Finding #1: Missing form label
Severity: MAJOR
The email input has no associated label.

Finding #2: Low contrast on the submit button
Severity: CRITICAL
"""

SEVERITY_TABLE = """Verdict: REVISE

| Finding | Severity | File |
|---|---|---|
| Missing form label | MAJOR | LoginForm.tsx:14 |
| Low contrast submit | CRITICAL | LoginForm.css:8 |
"""


def test_bold_group_headings_counted():
    """The receipt that scored 0 while raising 4 findings."""
    result = count_findings(BOLD_GROUP_HEADINGS)
    assert result["total_detected"] == 4, result
    assert result["by_severity"]["CRITICAL"] == 1
    assert result["by_severity"]["MAJOR"] == 2
    assert result["by_severity"]["MINOR"] == 1
    # MINOR is detected but below the default threshold.
    assert result["total"] == 3, result


def test_bold_group_excludes_predictions_and_whats_missing():
    """Pre-commitment Predictions and What's Missing are not findings."""
    result = count_findings(BOLD_GROUP_HEADINGS)
    # 2 predictions + 2 What's Missing bullets would push this to 8.
    assert result["total_detected"] == 4


def test_hash_group_headings_counted():
    result = count_findings(HASH_GROUP_HEADINGS)
    assert result["total_detected"] == 2, result
    assert result["by_severity"]["MAJOR"] == 1
    assert result["by_severity"]["MINOR"] == 1
    # "None." under Critical, and Enhancements, contribute nothing.
    assert result["by_severity"]["CRITICAL"] == 0
    assert result["total"] == 1, result


def test_hash_group_excludes_multi_perspective_bullets():
    """Top-level bullets outside a severity section are not findings."""
    assert count_findings(HASH_GROUP_HEADINGS)["total_detected"] == 2


def test_severity_prefixed_headings_counted():
    result = count_findings(SEVERITY_PREFIXED_HEADINGS)
    assert result["total_detected"] == 3, result
    assert result["by_severity"]["MAJOR"] == 1
    assert result["by_severity"]["MINOR"] == 2
    assert result["total"] == 1, result


def test_finding_body_bullets_are_not_separate_findings():
    """A finding's own Evidence/Confidence bullets must not each count."""
    assert count_findings(SEVERITY_PREFIXED_HEADINGS)["total_detected"] == 3


def test_group_plus_subheadings_counted():
    result = count_findings(GROUP_PLUS_SUBHEADINGS)
    assert result["total_detected"] == 3, result
    assert result["by_severity"]["MAJOR"] == 1
    assert result["by_severity"]["MINOR"] == 2
    # E1 sits under Enhancements, not a severity heading.
    assert result["by_severity"]["CRITICAL"] == 0
    assert result["total"] == 1, result


def test_inline_tags_still_counted():
    """The original layout keeps working as a fallback."""
    result = count_findings(INLINE_SEVERITY_TAGS)
    assert result["total"] == 2, result
    assert result["layouts"] == ["inline severity tag"]


def test_severity_table_still_counted():
    result = count_findings(SEVERITY_TABLE)
    assert result["total"] == 2, result


def test_inline_patterns_do_not_stack_on_structured_output():
    """A calibration table restating findings must not double-count them.

    Claude output files a Phase 8 severity-calibration table that repeats each
    finding as a `| ... | MINOR |` row. Adding the inline patterns on top of
    structural counting turned 7 findings into 11.
    """
    text = GROUP_PLUS_SUBHEADINGS + """
## Phase 8 — Realist Check (severity calibration record)

| Finding | Confidence | Refutable | Kind | Severity |
|---|---|---|---|---|
| m1 focusable predicate | HIGH | No | GAP | MAJOR |
| m2 omitted element types | HIGH | No | GAP | MINOR |
| m3 hardcoded id | HIGH | No | GAP | MINOR |
"""
    assert count_findings(text)["total_detected"] == 3


def test_evidence_contract_block_not_counted_as_a_finding():
    """check_evidence_contract counts contracts; this must not count them again.

    button-skip-link-clean's committed receipt scored 1 under the old counter,
    and the 1 came from the contract's `severity: MAJOR` line rather than from
    any of its three findings.
    """
    text = BOLD_GROUP_HEADINGS + """
### A11y Evidence Finding
finding_id: a11y_dropdown_activedescendant
severity: MAJOR
evidence: DropdownSelect.tsx:48 listbox has no active descendant
"""
    assert count_findings(text)["total_detected"] == 4


def test_zero_indent_field_labels_do_not_close_a_bold_section():
    """A bold field label is not a section heading.

    Findings under a bold group heading usually indent their Evidence/Fix
    bullets, but nothing makes them. When they sit at column zero, reading
    "**Evidence**: ..." as a sibling heading closed the section and dropped
    every finding after the first.
    """
    text = """**Major Findings**:
1. **Focus indicator contrast failure**
**Evidence**: MainLayout.css:42
2. **Skip link hiding mechanism fragile**
**Evidence**: MainLayout.css:12

**What's Missing** (gaps, unhandled edge cases):
- No current-page indication.
"""
    result = count_findings(text)
    assert result["total"] == 2, result
    assert result["by_severity"]["MAJOR"] == 2


def test_fenced_code_is_not_scanned():
    text = """**Major Findings**:
1. **Skip link hiding is fragile**
   - **Fix**: use `clip-path`.

```diff
- Severity: CRITICAL
- Finding #9: this is sample code, not a finding
```
"""
    assert count_findings(text)["total_detected"] == 1


def test_clean_accept_with_no_findings_is_zero():
    text = """# Verdict: ACCEPT

## Critical Findings
None.

## Major Findings
None.

## Multi-Perspective Notes
- **Screen reader user:** everything announces correctly.
"""
    assert count_findings(text)["total"] == 0


def test_prose_bait_still_ignored():
    """Regression guard carried over from test_score_output_contracts."""
    text = (
        "This clean component mentions CRITICAL risk only as a hypothetical "
        "example.\nVerdict: ACCEPT"
    )
    assert count_findings(text)["total"] == 0


def test_count_false_positives_exposes_breakdown_and_layouts():
    fp = count_false_positives(BOLD_GROUP_HEADINGS, "REVISE")
    assert fp["structured_findings"] == 3
    assert fp["findings_detected"] == 4
    assert fp["findings_by_severity"]["CRITICAL"] == 1
    assert fp["findings_by_severity"]["MINOR"] == 1
    assert fp["finding_layouts"] == ["severity group + list items"]
    assert fp["wrong_verdict"]


def test_layouts_distinguish_zero_from_unrecognised():
    """A zero with no layouts means nothing was recognised, not nothing found."""
    assert count_findings("Verdict: ACCEPT\nLooks good.")["layouts"] == []
    assert count_findings(BOLD_GROUP_HEADINGS)["layouts"] != []


def test_minor_excluded_from_the_default_total():
    """The default threshold matches the original patterns: no MINOR."""
    result = count_findings(BOLD_GROUP_HEADINGS)
    assert "MINOR" not in result["counted_severities"]
    assert result["by_severity"]["MINOR"] == 1
    assert result["total"] == result["total_detected"] - 1


def test_minor_included_when_the_caller_asks_for_it():
    """The threshold is a default, not a capability."""
    result = count_findings(BOLD_GROUP_HEADINGS, counted_severities=ALL_SEVERITIES)
    assert result["total"] == 4
    assert result["total_detected"] == 4


def test_minor_only_output_scores_zero_but_reports_its_layout():
    """An all-MINOR response is a real zero, not an unrecognised format.

    paired-id-name-columns-clean's receipt is exactly this: two MINOR findings
    and nothing else, so the thresholded total is 0 while the parser plainly
    did read the format. Without `layouts` the two cases look identical.
    """
    text = """# Verdict: ACCEPT

**Minor Findings** (friction but workaround exists):
1. **Column header association is implicit**
2. **No caption on the data table**
"""
    result = count_findings(text)
    assert result["total"] == 0, result
    assert result["total_detected"] == 2
    assert result["layouts"] == ["severity group + list items"]


def test_unstated_severity_counts_toward_the_total():
    """Unstated is not minor; the original `Finding #1:` pattern counted it too."""
    text = """Verdict: REVISE

Finding #1: The email input has no associated label.
Finding #2: The submit button has no accessible name.
"""
    result = count_findings(text)
    assert result["by_severity"]["UNSPECIFIED"] == 2
    assert result["total"] == 2


def test_unknown_severity_in_the_threshold_is_rejected():
    """A typo in a caller's threshold must fail loudly, not silently score zero."""
    try:
        count_findings(BOLD_GROUP_HEADINGS, counted_severities=("MAJOR", "SEVERE"))
    except ValueError as exc:
        assert "SEVERE" in str(exc)
    else:
        raise AssertionError("expected ValueError for an unknown severity level")


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"PASS: {name}")
