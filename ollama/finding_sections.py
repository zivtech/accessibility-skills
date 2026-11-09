#!/usr/bin/env python3
"""Count the findings a critic raised, whatever layout it used to group them.

Why this module exists
----------------------
``count_false_positives`` originally matched four patterns that all required the
severity word to sit *inline with the item* -- ``1. **CRITICAL ...``,
``Severity: MAJOR``, or a table cell. Neither the local detector nor the Claude
critic writes that way. Both group findings under a severity *heading* and put
the finding's title in the bold slot, so the counter saw nothing and CLEAN
fixtures reported zero false alarms no matter how many findings were raised.

Four layouts appear in the retained receipts, and only the fourth was counted:

1. Severity group heading + list items (``qwen3.6:35b``, both ``###`` and
   ``**bold**`` heading forms)::

       **Critical Findings** (blocks access):
       1.  **Screen Reader Navigation Feedback Missing**
           - **Evidence**: ...

2. Severity group heading + deeper sub-headings (Claude, ``modal-complete``)::

       ## Major Findings (significantly degrades experience)
       ### M1 - The focusable-element predicate admits ...

3. Severity-prefixed finding heading, no group (Claude, ``button-skip-link``)::

       ## Findings
       ### MAJOR 1 - Focus indicator measures 2.27:1; WCAG requires 3:1

4. Inline severity tags and severity table cells -- the original four patterns,
   kept for formats that really do tag each item.

What counts as a finding
------------------------
A finding is a top-level item under a heading that classifies it by severity.
Deliberately NOT counted, because they are not claims that the artifact is
defective:

- ``Enhancements`` / ``Open Questions`` / ``Multi-Perspective Notes`` sections.
- ``What's Missing`` -- gaps and unstated assumptions, not severity-rated defects.
- ``Pre-commitment Predictions`` -- written before reading the source.
- Nested sub-bullets (``Evidence:``, ``Issue:``, ``Fix:``) of a counted item.
- Fenced code blocks.
- ``A11y Evidence Finding`` contract blocks -- ``check_evidence_contract``
  already counts those, and a contract restates a finding counted above it.

Severity threshold
------------------
MINOR is detected but does not count toward the total by default; see
``DEFAULT_COUNTED_SEVERITIES``. The original patterns matched
CRITICAL/SERIOUS/MAJOR -- and MODERATE in one of the four -- so MINOR was
excluded there too, and keeping it excluded is what makes the published CLEAN
rows comparable *in kind* across 2026-10-23: what changed on that date is which
layouts are visible, not which severities count. A finding whose severity the
critic never stated does count, because unstated is not the same as minor and
the original ``Finding #1:`` pattern counted it as well.

Detection is independent of the threshold, deliberately. ``by_severity`` always
reports every severity found and ``total_detected`` their sum, so a caller that
wants MINOR in the total passes ``counted_severities=ALL_SEVERITIES`` rather
than editing this module. The threshold is a default, not a capability.

Still outstanding
-----------------
``score_perspective.py``'s ``check_false_positives`` holds a byte-identical copy
of the same four patterns and is **not** fixed by this module. It was left alone
because ZIV-24 scoped the CLEAN axis of the ``score_output`` lane and the
perspective lane's published numbers have not been audited; its verdict
vocabulary also differs (``BLOCK``/``REVISE`` rather than ``REJECT``/``REVISE``),
so it is not a drop-in delegation. Any perspective-lane false-positive count is
subject to the same blindness described above.
"""

import re

SEVERITY_LEVELS = ("CRITICAL", "SERIOUS", "MAJOR", "MODERATE", "MINOR")
_SEVERITY_ALT = "|".join(SEVERITY_LEVELS)

# A finding the critic filed without stating a severity.
UNSPECIFIED = "UNSPECIFIED"

# Every bucket a finding can land in, for callers that want MINOR counted.
ALL_SEVERITIES = SEVERITY_LEVELS + (UNSPECIFIED,)

# The default false-alarm threshold: everything a critic called worse than
# MINOR, plus findings it left unclassified.
DEFAULT_COUNTED_SEVERITIES = tuple(
    level for level in ALL_SEVERITIES if level != "MINOR"
)

# "Critical Findings", "Major Findings (significantly degrades experience)".
# The severity word must be immediately followed by "Finding(s)" so a finding
# *title* that happens to start with a severity word cannot be mistaken for a
# group heading.
SEVERITY_GROUP_RE = re.compile(rf"^({_SEVERITY_ALT})\s+FINDINGS?\b", re.IGNORECASE)

# "MAJOR 1 - Focus indicator ...", "CRITICAL: no accessible name".
# The heading is itself the finding.
SEVERITY_ITEM_RE = re.compile(
    rf"^({_SEVERITY_ALT})\b\s*#?\s*\d*\s*[—–:.\-]", re.IGNORECASE
)

# Evidence contracts are counted by check_evidence_contract, not here.
CONTRACT_HEADING_RE = re.compile(r"^A11Y\s+EVIDENCE\s+FINDING", re.IGNORECASE)

HASH_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
BOLD_HEADING_RE = re.compile(r"^\*\*(.+?)\*\*\s*(.*)$")
FENCE_RE = re.compile(r"^\s{0,3}(?:```|~~~)")

# What may follow a bold run for it to still read as a section heading: an
# optional parenthetical and an optional colon, and nothing else.
# "**What's Missing** (gaps, unhandled edge cases):" is a heading.
# "**Evidence**: `DropdownSelect.tsx:48`" is a field label inside a finding,
# and treating it as a heading closed the section its finding belonged to.
HEADING_TAIL_RE = re.compile(r"^\s*(?:\([^)]*\))?\s*:?\s*$")

# Top-level list item: at most one leading space, so the 3-or-4-space
# "- **Evidence**:" sub-bullets of a counted item are excluded.
LIST_ITEM_RE = re.compile(r"^ {0,1}(?:[-*+]|\d+[.)])\s+\S")

# A severity-tagged table row, for findings tabulated under a group heading.
SEVERITY_TABLE_ROW_RE = re.compile(rf"\|\s*\**\s*({_SEVERITY_ALT})\s*\**\s*\|", re.IGNORECASE)

# The original inline patterns, for layouts that tag each item in place.
# Each entry is (pattern, severity_group_index_or_None).
LEGACY_PATTERNS = (
    (re.compile(r"(?:Finding|Issue)\s*#?\d+\s*[:.]", re.IGNORECASE), None),
    (
        re.compile(rf"^\s*\d+[.)]\s+\**({_SEVERITY_ALT})\b", re.IGNORECASE),
        1,
    ),
    (re.compile(rf"\**Severity\**\s*:\s*\**({_SEVERITY_ALT})\b", re.IGNORECASE), 1),
    (SEVERITY_TABLE_ROW_RE, 1),
)

# Bold "headings" carry no level. Treat them as h3: a sibling bold heading then
# closes an open section, and a #### under one would nest inside it.
_BOLD_HEADING_LEVEL = 3


def _classify_heading(line: str) -> tuple[int, str, bool] | None:
    """Return (level, title, is_bold_run) if the line is a heading, else None.

    A leading bold run is reported, but the caller must not treat an arbitrary
    one as a section heading. Documents that structure findings with ``###``
    headings also open field labels with bold runs -- ``**Evidence** - ...``,
    ``**User group:** ...`` -- and reading those as sub-headings counted every
    field of every finding as a separate finding.
    """
    hash_match = HASH_HEADING_RE.match(line)
    if hash_match:
        return len(hash_match.group(1)), hash_match.group(2), False

    # "**Critical Findings**: None. The component meets ..." is still a
    # heading; the trailing prose carries no list items, so it scores zero.
    bold_match = BOLD_HEADING_RE.match(line)
    if bold_match:
        return _BOLD_HEADING_LEVEL, bold_match.group(1), True
    return None


def _is_bold_section_heading(line: str) -> bool:
    """Whether a leading bold run reads as a section heading, not a field label."""
    bold_match = BOLD_HEADING_RE.match(line)
    return bool(bold_match) and bool(HEADING_TAIL_RE.match(bold_match.group(2)))


def _severity_of(title: str) -> str | None:
    group = SEVERITY_GROUP_RE.match(title.strip().lstrip("#* "))
    if group:
        return group.group(1).upper()
    return None


def _severity_item_of(title: str) -> str | None:
    item = SEVERITY_ITEM_RE.match(title.strip().lstrip("#* "))
    if item:
        return item.group(1).upper()
    return None


def count_findings(
    text: str, counted_severities: tuple[str, ...] = DEFAULT_COUNTED_SEVERITIES
) -> dict:
    """Count severity-classified findings in critic output.

    Returns ``{"total": int, "total_detected": int, "by_severity": {LEVEL:
    int}, "counted_severities": (str, ...), "layouts": [str, ...]}``.

    ``total`` applies the severity threshold; ``total_detected`` and
    ``by_severity`` do not, so the threshold is always auditable from the same
    result. ``layouts`` names which of the four layouts actually contributed --
    counting every detection, not just the thresholded ones, so a zero can be
    told apart from a zero that means "this parser did not recognise the
    format".

    The inline-tag patterns are a *fallback*, applied only when the output
    carries no severity headings at all. They are too noisy to add on top of
    structural counting: in a document that already groups its findings, they
    also fire on the Phase 8 severity-calibration table, which restates
    findings counted once already, and on numbered prose in phases that
    critique the evidence rather than the artifact.
    """
    unknown = sorted(set(counted_severities) - set(ALL_SEVERITIES))
    if unknown:
        raise ValueError(
            f"unknown severity level(s) {unknown}; expected a subset of "
            f"{list(ALL_SEVERITIES)}"
        )

    structural: list[tuple[int, str | None, str]] = []
    inline: list[tuple[int, str | None, str]] = []
    seen_lines: set[int] = set()

    # Open severity group section, if any.
    group_severity: str | None = None
    group_level = 0
    group_is_bold = False
    group_saw_subheading = False
    # True while inside the body of a heading that was itself counted as a
    # finding, or inside a block whose contents must not be counted at all.
    in_counted_item = False
    in_contract = False
    in_fence = False
    # True once the output is seen to classify findings by severity heading,
    # whether or not any section turned out to hold a finding.
    has_structure = False

    def record(level: str | None, line_no: int, layout: str, family: int = -1) -> None:
        if line_no in seen_lines:
            return
        seen_lines.add(line_no)
        if family >= 0:
            inline.append((line_no, level, family))
        else:
            structural.append((line_no, level, layout))

    for line_no, line in enumerate(text.splitlines()):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        heading = _classify_heading(line)
        if heading is not None:
            level, title, is_bold = heading
            bare = title.strip().lstrip("#* ")
            severity = _severity_of(bare)
            standalone = _severity_item_of(bare)
            is_contract = bool(CONTRACT_HEADING_RE.match(bare))

            # A bold run only acts as a section boundary when it names a
            # severity group, a severity-prefixed finding, or a contract --
            # or when the open group was itself opened by a bold run, in
            # which case a sibling bold run closes it. Anything else is a
            # field label inside a finding body.
            if is_bold and not (severity or standalone or is_contract):
                if (
                    group_severity is not None
                    and group_is_bold
                    and _is_bold_section_heading(line)
                ):
                    group_severity = None
                    group_saw_subheading = False
                    in_counted_item = False
                    in_contract = False
                    continue
                heading = None

        if heading is not None:
            if is_contract:
                in_contract = True
                in_counted_item = False
                group_severity = None
                continue

            # A heading at or above the open group's level closes it.
            if group_severity is not None and level <= group_level:
                group_severity = None
                group_saw_subheading = False

            if level <= _BOLD_HEADING_LEVEL:
                in_contract = False

            if severity is not None:
                group_severity = severity
                group_level = level
                group_is_bold = is_bold
                group_saw_subheading = False
                in_counted_item = False
                has_structure = True
                continue

            if in_contract:
                in_counted_item = False
                continue

            # "### MAJOR 1 - ..." with no group heading above it: the heading
            # is the finding.
            if standalone is not None and group_severity is None:
                record(standalone, line_no, "severity-prefixed heading")
                in_counted_item = True
                has_structure = True
                continue

            # "### M1 - ..." nested under "## Major Findings": the sub-heading
            # is the finding, and its body's top-level bullets belong to it.
            # Only a real hash heading nests this way; see _classify_heading.
            if group_severity is not None and level > group_level and not is_bold:
                group_saw_subheading = True
                record(group_severity, line_no, "severity group + sub-headings")
                in_counted_item = True
                continue

            in_counted_item = False
            continue

        if in_contract or in_counted_item:
            continue

        if group_severity is None:
            for family, (pattern, severity_index) in enumerate(LEGACY_PATTERNS):
                match = pattern.search(line)
                if match:
                    level_name = (
                        match.group(severity_index).upper() if severity_index else None
                    )
                    record(level_name, line_no, "inline severity tag", family)
                    break
            continue

        # Inside a severity group section, before any sub-heading appeared.
        if group_saw_subheading:
            continue
        if LIST_ITEM_RE.match(line):
            record(group_severity, line_no, "severity group + list items")
        elif SEVERITY_TABLE_ROW_RE.search(line):
            record(group_severity, line_no, "severity group + table")

    if has_structure:
        counted = structural
    else:
        # One finding written as "Finding #1:" on one line and "Severity:
        # MAJOR" on the next matches two of the four inline patterns, and the
        # original counter summed them -- two hits for one finding. The
        # families are alternative spellings of the same thing, so take the
        # most specific one that fired rather than their sum. A document that
        # mixes families for different findings would undercount; none in the
        # corpus does, and summing overcounts every document that does not.
        families = {family for _line_no, _level, family in inline}
        chosen = min(families) if families else None
        counted = [
            (line_no, level, "inline severity tag")
            for line_no, level, family in inline
            if family == chosen
        ]

    by_severity = {level: 0 for level in ALL_SEVERITIES}
    layouts: list[str] = []
    for _line_no, level, layout in counted:
        by_severity[level or UNSPECIFIED] += 1
        if layout not in layouts:
            layouts.append(layout)

    return {
        "total": sum(by_severity[level] for level in counted_severities),
        "total_detected": len(counted),
        "by_severity": by_severity,
        "counted_severities": tuple(counted_severities),
        "layouts": layouts,
    }
