"""Shared helpers for the score_* scripts. Keep stdlib-only."""
import re

# Gate semantics: this is an ESCALATION/ABORT gate, not a quality bar.
# A fixture "passes" a tier when must-find detection is >= this fraction;
# below it, the escalation runner promotes the fixture to the next tier.
# Headline detection rates in BENCHMARK.md are aggregate found/total counts,
# NOT this pass rate. Do not conflate the two when reporting.
MUST_FIND_ABORT_THRESHOLD = 0.4
PLANNER_SECTION_PASS_THRESHOLD = 0.7


def strip_thinking(text: str) -> tuple[str, bool]:
    """Remove closed <think> blocks. Returns (clean_text, truncated).

    truncated=True means an unclosed <think> remains after stripping —
    the response was cut off mid-chain-of-thought and must not be scored
    as a normal response.
    """
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    truncated = "<think>" in cleaned
    return cleaned, truncated


def detect_verdict(text: str, ladder: list[str]) -> str:
    """Two-tier verdict detection.

    1. Explicit declaration:  'Verdict: REVISE' (with optional markdown).
    2. Fallback: whole-word scan, ladder order (most specific/severe first).
    """
    alternatives = "|".join(re.escape(v) for v in ladder)
    m = re.search(
        rf"(?:#\s*)?(?:\*\*)?Verdict(?:\*\*)?[:\s]+\*?\*?({alternatives})\b",
        text, re.IGNORECASE,
    )
    if m:
        return m.group(1).upper()
    upper = text.upper()
    for v in ladder:
        if re.search(rf"\b{re.escape(v)}\b", upper):
            return v
    return "NONE"


def fallback_keywords(description: str, max_words: int = 4) -> list[str]:
    """Last-resort keyword extraction. Never returns an empty list."""
    words = [w.strip(".,;:()\"'") for w in description.split()[:max_words]]
    filtered = [w for w in words if len(w) > 3]
    return filtered or [w for w in words if w] or [description.strip()[:40]]
