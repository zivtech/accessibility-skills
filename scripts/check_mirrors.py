#!/usr/bin/env python3
"""Report drift between .claude/skills/ and .agents/skills/ mirror surfaces,
and between skills and their embedded agent-def protocol copies.

Checks per skill directory:
1. Heading set diff (## headings present in one surface but not the other)
2. .Codex/ path hits in the .agents/ file (broken paths)
3. URL set diff (URLs present in one surface but not the other — catches
   over-eager Claude->Codex string rewrites that mangle URLs, e.g.
   zivtech-ai-skills rewritten to the nonexistent zivtech-Codex-skills)
4. Diff stat (count of differing lines)
5. Parity assertion (issue #27): every mirror pair must be byte-identical
   unless PARITY_EXEMPTIONS declares its divergence. Checks 1-3 are a
   drift TIER, not full-text parity — a body-prose edit landing on one
   surface only changes no heading and no URL, so it was invisible to
   --strict. That happened live on 2026-08-25: a CRITICAL a11y-critic
   guard shipped Claude-side only, two byte-identical pairs drifted to 1
   and 10 differing lines, and --strict stayed green. An exemption pins
   both the differing-line COUNT and a fingerprint over the differing
   lines themselves, so a same-size swap of the divergent content fails
   too. The fingerprint ignores context lines and hunk headers, so
   editing shared prose on BOTH surfaces leaves it unchanged.
6. References files: byte-for-byte match

Checks per agent def (skills-vs-agent-def protocol drift):
- Embedded protocol copies (.claude/agents/*.md, .codex/agents/*.toml for
  a11y-planner and a11y-critic): every protocol section marker in the
  canonical SKILL.md — "Phase N — Title:" headings and ALL-CAPS block labels
  (HARD GATES:, AUDIT-SCOPE MODE (WCAG-EM):, FEDERAL PROFILE (...)) — must
  appear in the def. Defs are intentionally condensed, so a full-text mirror
  check would be wrong; a def missing a whole section runs an old protocol
  (the issue #17 failure class: the planner def predated the Phase 2 FEDERAL
  PROFILE and could not execute declared-508 audit planning).
- Thin-wrapper defs (perspective-audit, a11y-role-auditor) load SKILL.md at
  runtime instead of embedding it: verify the reference path is present.

Always exits 0 in report-only mode (default).
Use --strict to exit 1 on any reported drift (heading, .Codex/ path, URL,
parity, references, registry, or agent-def mismatch).
Use --self-test to run the checker's own failing-direction tests (no repo
files read) — it proves parity drift, a same-size content swap, and an
undeclared mirror pair each exit non-zero.

Run from repo root:
    python3 scripts/check_mirrors.py
    python3 scripts/check_mirrors.py --strict
    python3 scripts/check_mirrors.py --self-test
"""

import difflib
import hashlib
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLAUDE_SKILLS = os.path.join(REPO, ".claude", "skills")
AGENTS_SKILLS = os.path.join(REPO, ".agents", "skills")

SKILL_NAMES = ["a11y-critic", "a11y-planner", "a11y-test", "perspective-audit", "bug-reporting", "acr-reporting", "maintain-accessibility-skills", "a11y-content-judgment"]

# Parity manifest (issue #27). Every pair in SKILL_NAMES must be byte-identical
# ACROSS THE WHOLE FILE unless it is declared here. Declaring costs two pinned
# values, both printed by this script when they disagree:
#   diff_lines  — the exact differing-line count (not a ceiling: a drop also
#                 fails, so a sync that removes divergence updates the record)
#   fingerprint — sha256[:16] over the differing lines themselves, so a
#                 same-size swap of the divergent content fails too
# Editing shared prose on BOTH surfaces changes neither value.
PARITY_EXEMPTIONS = {
    "a11y-planner": {
        "diff_lines": 8,
        "fingerprint": "3895fcde18ea0bb9",
        "reason": (
            "Claude/Codex platform terminology, 4 line pairs: the "
            "compatibility: frontmatter value, two oh-my-claudecode/oh-my-Codex "
            "routing bullets, and the 'For Claude:'/'For Codex:' callout. "
            "Pre-existing; recorded in the 2026-08-25 Phase 2 gate review."
        ),
    },
}

# Skill dirs present on BOTH surfaces that are NOT full-text mirror pairs, so
# they are deliberately absent from SKILL_NAMES. Anything else on both surfaces
# and in neither list fails the registry check: parity is opt-out, not opt-in.
NON_MIRROR_PAIRS = {
    "a11y-role-audit": (
        "intentionally condensed Codex mirror, declared in its own frontmatter "
        "(compatibility: 'Codex CLI mirror of .claude/skills/...')"
    ),
}

# Agent defs that EMBED a condensed copy of the skill protocol (drift-prone:
# a new SKILL.md section does not propagate on its own). Not covered:
# a11y-scout (no skill counterpart) and .agents/skills/a11y-role-audit
# (an intentionally condensed Codex mirror, declared in its own frontmatter).
EMBEDDED_AGENT_DEFS = {
    "a11y-planner": [
        os.path.join(".claude", "agents", "a11y-planner.md"),
        os.path.join(".codex", "agents", "a11y-planner.toml"),
    ],
    "a11y-critic": [
        os.path.join(".claude", "agents", "a11y-critic.md"),
        os.path.join(".codex", "agents", "a11y-critic.toml"),
    ],
}

# Agent defs that load the canonical SKILL.md at runtime (drift-free by
# design) — checked only for the presence of the skill reference path.
WRAPPER_AGENT_DEFS = {
    "perspective-audit": os.path.join(".claude", "agents", "perspective-audit.md"),
    "a11y-role-audit": os.path.join(".claude", "agents", "a11y-role-auditor.md"),
}

PHASE_MARKER_RE = re.compile(r"^\s*(Phase \d+ — [^:]+):\s*$")
BLOCK_MARKER_RE = re.compile(r"^\s*([A-Z][A-Z 0-9()-]{4,}(?: \([^)]+\))?)(?: — [^:]*)?:\s*$")
# Generic emphasis labels, and sections a condensed def legitimately drops.
BLOCK_MARKER_DENYLIST = {"IMPORTANT", "WARNING", "CAUTION", "TIP", "TIPS", "EXAMPLE", "EXAMPLES"}


def listdirs(path):
    """Subdirectory names under path (missing path -> empty)."""
    if not os.path.isdir(path):
        return []
    return [n for n in os.listdir(path) if os.path.isdir(os.path.join(path, n))]


def extract_headings(text):
    """Return list of ## headings (stripped) from markdown text."""
    return [
        line.strip()
        for line in text.splitlines()
        if re.match(r"^## ", line)
    ]


def count_codex_hits(text, path):
    """Return list of (line_number, line) for lines containing .Codex/ in text."""
    hits = []
    for i, line in enumerate(text.splitlines(), start=1):
        if ".Codex/" in line:
            hits.append((i, line.strip()))
    return hits


URL_RE = re.compile(r"https?://[^\s)\"'`>\]]+")


def extract_urls(text):
    """Return the set of URLs in text, trailing punctuation stripped."""
    return {url.rstrip(".,;:") for url in URL_RE.findall(text)}


def changed_lines(text_a, text_b):
    """Ordered +/- lines of the unified diff, context and hunk headers excluded.

    Hunk headers carry line numbers, so excluding them keeps the result stable
    under edits made to BOTH surfaces — only one-sided edits change it.
    """
    lines_a = text_a.splitlines(keepends=True)
    lines_b = text_b.splitlines(keepends=True)
    diff = difflib.unified_diff(lines_a, lines_b, fromfile="a", tofile="b", n=0)
    return [
        line.rstrip("\n")
        for line in diff
        if (line.startswith("+") and not line.startswith("+++"))
        or (line.startswith("-") and not line.startswith("---"))
    ]


def diff_stat(text_a, text_b):
    """Return count of differing lines."""
    return len(changed_lines(text_a, text_b))


def parity_fingerprint(changed):
    """sha256[:16] over the differing lines. Drift detection, not a signature."""
    return hashlib.sha256("\n".join(changed).encode("utf-8")).hexdigest()[:16]


def check_parity(skill_name, claude_text, agents_text, exemptions=None):
    """Assert full-text parity for one mirror pair (issue #27).

    Returns (ok, report_lines). Every line names the pair, so a strict-mode
    failure is greppable without reading the surrounding section header.
    """
    exemptions = PARITY_EXEMPTIONS if exemptions is None else exemptions
    changed = changed_lines(claude_text, agents_text)
    count = len(changed)
    fingerprint = parity_fingerprint(changed)
    declared = exemptions.get(skill_name)

    if declared is None:
        if count == 0:
            return True, [f"  Parity [{skill_name}]: byte-identical"]
        return False, [
            f"  PARITY DRIFT [{skill_name}]: {count} differing lines on a pair "
            f"required to be byte-identical",
            f"    Sync the surfaces, or declare the divergence in "
            f"PARITY_EXEMPTIONS with diff_lines: {count}, "
            f"fingerprint: {fingerprint}",
        ] + [f"    {line}" for line in changed[:10]] + (
            [f"    ... {count - 10} more"] if count > 10 else []
        )

    if count != declared["diff_lines"]:
        return False, [
            f"  PARITY DRIFT [{skill_name}]: {count} differing lines, "
            f"declared {declared['diff_lines']}",
            f"    Declared divergence: {declared['reason']}",
            f"    If the change is intended, update PARITY_EXEMPTIONS to "
            f"diff_lines: {count}, fingerprint: {fingerprint}",
        ]

    if fingerprint != declared["fingerprint"]:
        return False, [
            f"  PARITY DRIFT [{skill_name}]: differing-line count matches "
            f"({count}) but the divergent CONTENT changed",
            f"    declared fingerprint {declared['fingerprint']}, "
            f"actual {fingerprint}",
            f"    Declared divergence: {declared['reason']}",
        ]

    return True, [
        f"  Parity [{skill_name}]: {count} differing lines, declared "
        f"(fingerprint {fingerprint})"
    ]


def check_registry(claude_dirs, agents_dirs, skill_names=None, non_mirror=None,
                   exemptions=None):
    """Every skill dir on BOTH surfaces must be declared somewhere.

    Without this, a new mirrored skill left out of SKILL_NAMES is checked by
    nothing at all — the parity guard would be opt-in, which is the same blind
    spot one level up.
    """
    skill_names = SKILL_NAMES if skill_names is None else skill_names
    non_mirror = NON_MIRROR_PAIRS if non_mirror is None else non_mirror
    exemptions = PARITY_EXEMPTIONS if exemptions is None else exemptions

    pairs = set(claude_dirs) & set(agents_dirs)
    declared = set(skill_names) | set(non_mirror)
    undeclared = sorted(pairs - declared)
    stale = sorted(declared - pairs)

    report = ["\n=== mirror registry ==="]
    ok = True
    if undeclared:
        ok = False
        report.append(f"  UNDECLARED mirror pair(s): {len(undeclared)}")
        for name in undeclared:
            report.append(
                f"    - {name}: present on both surfaces but in neither "
                f"SKILL_NAMES nor NON_MIRROR_PAIRS — add it to one"
            )
    if stale:
        ok = False
        report.append(f"  STALE registry entr(ies): {len(stale)}")
        for name in stale:
            report.append(
                f"    - {name}: declared but not a pair on disk — "
                f"remove it or restore the missing surface"
            )
    dead = sorted(set(exemptions) - set(skill_names))
    if dead:
        ok = False
        report.append(f"  DEAD parity exemption(s): {len(dead)}")
        for name in dead:
            report.append(
                f"    - {name}: PARITY_EXEMPTIONS entry for a pair that is not "
                f"parity-checked — the exemption does nothing"
            )
    if ok:
        report.append(
            f"  {len(pairs)} mirror pair(s) on disk, all declared "
            f"({len(pairs & set(skill_names))} parity-checked, "
            f"{len(pairs & set(non_mirror))} declared non-mirror)"
        )
    return ok, report


def check_skill(skill_name, strict_mode):
    """Check mirrors for one skill. Returns has_drift (bool)."""
    claude_skill_file = os.path.join(CLAUDE_SKILLS, skill_name, "SKILL.md")
    agents_skill_file = os.path.join(AGENTS_SKILLS, skill_name, "SKILL.md")

    print(f"\n=== {skill_name} ===")

    has_drift = False

    if not os.path.isfile(claude_skill_file):
        print(f"  MISSING: {claude_skill_file}")
        return True
    if not os.path.isfile(agents_skill_file):
        print(f"  MISSING: {agents_skill_file}")
        return True

    with open(claude_skill_file) as f:
        claude_text = f.read()
    with open(agents_skill_file) as f:
        agents_text = f.read()

    # 1. Heading drift
    claude_headings = set(extract_headings(claude_text))
    agents_headings = set(extract_headings(agents_text))

    only_in_claude = claude_headings - agents_headings
    only_in_agents = agents_headings - claude_headings

    if only_in_claude or only_in_agents:
        has_drift = True
        print(f"  Heading drift detected:")
        for h in sorted(only_in_claude):
            print(f"    - only in .claude/: {h}")
        for h in sorted(only_in_agents):
            print(f"    + only in .agents/: {h}")
    else:
        print(f"  Headings: identical ({len(claude_headings)} headings)")

    # 2. .Codex/ hits in .agents/ file
    codex_hits = count_codex_hits(agents_text, agents_skill_file)
    if codex_hits:
        has_drift = True
        print(f"  .Codex/ hits in .agents/ file: {len(codex_hits)}")
        for lineno, line in codex_hits:
            print(f"    line {lineno}: {line[:100]}")
    else:
        print(f"  .Codex/ hits: none")

    # 3. URL drift between surfaces
    claude_urls = extract_urls(claude_text)
    agents_urls = extract_urls(agents_text)

    only_claude_urls = claude_urls - agents_urls
    only_agents_urls = agents_urls - claude_urls

    if only_claude_urls or only_agents_urls:
        has_drift = True
        print(f"  URL drift detected:")
        for url in sorted(only_claude_urls):
            print(f"    - only in .claude/: {url}")
        for url in sorted(only_agents_urls):
            print(f"    + only in .agents/: {url}")
    else:
        print(f"  URLs: identical ({len(claude_urls)} unique)")

    # 4. Diff stat
    changed = diff_stat(claude_text, agents_text)
    print(f"  Diff stat: {changed} differing lines")

    # 5. Parity assertion (issue #27)
    parity_ok, parity_report = check_parity(skill_name, claude_text, agents_text)
    for line in parity_report:
        print(line)
    if not parity_ok:
        has_drift = True

    # 6. References files
    claude_refs_dir = os.path.join(CLAUDE_SKILLS, skill_name, "references")
    agents_refs_dir = os.path.join(AGENTS_SKILLS, skill_name, "references")

    if os.path.isdir(claude_refs_dir) or os.path.isdir(agents_refs_dir):
        claude_refs = set(os.listdir(claude_refs_dir)) if os.path.isdir(claude_refs_dir) else set()
        agents_refs = set(os.listdir(agents_refs_dir)) if os.path.isdir(agents_refs_dir) else set()
        all_refs = claude_refs | agents_refs

        if not all_refs:
            print(f"  References: no files")
        else:
            for fname in sorted(all_refs):
                claude_ref_path = os.path.join(claude_refs_dir, fname)
                agents_ref_path = os.path.join(agents_refs_dir, fname)
                if fname not in claude_refs:
                    print(f"  References: {fname} — only in .agents/ (MISSING from .claude/)")
                    has_drift = True
                elif fname not in agents_refs:
                    print(f"  References: {fname} — only in .claude/ (MISSING from .agents/)")
                    has_drift = True
                else:
                    with open(claude_ref_path, "rb") as f:
                        claude_bytes = f.read()
                    with open(agents_ref_path, "rb") as f:
                        agents_bytes = f.read()
                    if claude_bytes == agents_bytes:
                        print(f"  References: {fname} — MATCH")
                    else:
                        print(f"  References: {fname} — DIFFER")
                        has_drift = True
    else:
        print(f"  References: no references dir in either surface")

    return has_drift


def extract_protocol_markers(text):
    """Protocol section markers from a SKILL.md: phase headings + CAPS block labels."""
    markers = []
    for line in text.splitlines():
        phase = PHASE_MARKER_RE.match(line)
        if phase:
            markers.append(phase.group(1).strip())
            continue
        block = BLOCK_MARKER_RE.match(line)
        if block:
            label = block.group(1).strip()
            if label not in BLOCK_MARKER_DENYLIST:
                markers.append(label)
    seen = set()
    deduped = []
    for marker in markers:
        if marker not in seen:
            seen.add(marker)
            deduped.append(marker)
    return deduped


def normalize_ws(text):
    """Collapse all whitespace runs so markers match across line-wrap differences."""
    return " ".join(text.split())


def check_agent_defs():
    """Check embedded agent-def protocol copies and thin wrappers. Returns has_drift."""
    has_drift = False

    for skill_name, def_paths in EMBEDDED_AGENT_DEFS.items():
        skill_file = os.path.join(CLAUDE_SKILLS, skill_name, "SKILL.md")
        print(f"\n=== agent defs: {skill_name} ===")

        if not os.path.isfile(skill_file):
            print(f"  MISSING: {skill_file}")
            has_drift = True
            continue
        with open(skill_file) as f:
            markers = extract_protocol_markers(f.read())
        print(f"  Protocol markers in SKILL.md: {len(markers)}")

        for rel_path in def_paths:
            def_file = os.path.join(REPO, rel_path)
            if not os.path.isfile(def_file):
                print(f"  MISSING: {rel_path}")
                has_drift = True
                continue
            with open(def_file) as f:
                def_norm = normalize_ws(f.read())
            missing = [m for m in markers if normalize_ws(m) not in def_norm]
            if missing:
                has_drift = True
                print(f"  {rel_path}: MISSING {len(missing)} protocol section(s):")
                for marker in missing:
                    print(f"    - {marker}")
            else:
                print(f"  {rel_path}: all {len(markers)} protocol sections present")

    for skill_name, rel_path in WRAPPER_AGENT_DEFS.items():
        def_file = os.path.join(REPO, rel_path)
        print(f"\n=== agent defs: {skill_name} (thin wrapper) ===")

        if not os.path.isfile(def_file):
            print(f"  MISSING: {rel_path}")
            has_drift = True
            continue
        expected_ref = f".claude/skills/{skill_name}/SKILL.md"
        with open(def_file) as f:
            def_text = f.read()
        if expected_ref in def_text:
            print(f"  {rel_path}: references {expected_ref}")
        else:
            has_drift = True
            print(f"  {rel_path}: does NOT reference {expected_ref} — wrapper must load the canonical protocol")

    return has_drift


SELF_TEST_BASE = """---
name: demo
compatibility: Claude Code-compatible
---

# Demo Skill

Shared prose line one.
Shared prose line two.

## Protocol

Do the thing.
"""


def self_test():
    """Failing-direction tests for the parity and registry guards (issue #27).

    Hermetic: no repo files are read. Case 2 is the exact regression that went
    undetected on 2026-08-25 — a body-prose line added to one surface only,
    touching no heading and no URL.
    """
    results = []

    def case(name, passed, detail=""):
        results.append((name, passed, detail))

    # 1. Parity-tracked pair, identical -> clean.
    ok, report = check_parity("demo", SELF_TEST_BASE, SELF_TEST_BASE, {})
    case("identical pair passes", ok and "byte-identical" in report[0])

    # 2. Body-prose line on ONE surface only -> fails, names the pair.
    perturbed = SELF_TEST_BASE.replace(
        "Do the thing.", "Do the thing.\nRe-fetch the evidence before filing."
    )
    ok, report = check_parity("demo", perturbed, SELF_TEST_BASE, {})
    body = "\n".join(report)
    case(
        "one-sided body-prose edit fails and names the pair",
        not ok and "PARITY DRIFT [demo]" in body,
    )
    case(
        "no heading/URL drift in that perturbation (the 2026-08-25 blind spot)",
        set(extract_headings(perturbed)) == set(extract_headings(SELF_TEST_BASE))
        and extract_urls(perturbed) == extract_urls(SELF_TEST_BASE),
    )

    # 3. Declared divergence matching its record -> clean.
    codex = SELF_TEST_BASE.replace(
        "compatibility: Claude Code-compatible", "compatibility: Codex-compatible"
    )
    declared_fp = parity_fingerprint(changed_lines(SELF_TEST_BASE, codex))
    manifest = {"demo": {"diff_lines": 2, "fingerprint": declared_fp, "reason": "test"}}
    ok, report = check_parity("demo", SELF_TEST_BASE, codex, manifest)
    case("declared divergence passes", ok and "declared" in report[0])

    # 4. Same differing-line COUNT, different content -> fails on fingerprint.
    swapped = SELF_TEST_BASE.replace("Shared prose line one.", "Something else entirely.")
    ok, report = check_parity("demo", SELF_TEST_BASE, swapped, manifest)
    body = "\n".join(report)
    case(
        "same-size content swap fails on fingerprint",
        not ok
        and "CONTENT changed" in body
        and diff_stat(SELF_TEST_BASE, swapped) == 2,
    )

    # 5. Declared pair drifting further -> fails on count.
    extra = codex.replace("Do the thing.", "Do the thing.\nAnd one more thing.")
    ok, report = check_parity("demo", SELF_TEST_BASE, extra, manifest)
    case("drift beyond the declared count fails", not ok and "declared 2" in "\n".join(report))

    # 6. False-positive control: the same edit on BOTH surfaces stays clean.
    both_a = SELF_TEST_BASE.replace("Do the thing.", "Do the thing.\nNew shared guard.")
    both_b = codex.replace("Do the thing.", "Do the thing.\nNew shared guard.")
    ok, _ = check_parity("demo", both_a, both_b, manifest)
    case("shared-prose edit on both surfaces stays clean", ok)

    # 7. Registry: a pair on both surfaces and in neither list is undeclared.
    ok, report = check_registry(["demo", "extra"], ["demo", "extra"], ["demo"], {})
    case(
        "undeclared mirror pair fails the registry check",
        not ok and "extra" in "\n".join(report),
    )

    # 8. Registry: a declared name with no pair on disk is stale.
    ok, report = check_registry(["demo"], ["demo"], ["demo", "ghost"], {})
    case("stale registry entry fails", not ok and "ghost" in "\n".join(report))

    # 9. Registry: an exemption for a pair nobody parity-checks is dead.
    ok, report = check_registry(
        ["demo"], ["demo"], ["demo"], {},
        {"nowhere": {"diff_lines": 1, "fingerprint": "x", "reason": "test"}},
    )
    case("dead parity exemption fails", not ok and "nowhere" in "\n".join(report))

    print("check_mirrors self-test (issue #27 parity guard)")
    failed = 0
    for name, passed, detail in results:
        print(f"  {'PASS' if passed else 'FAIL'}  {name}{(' — ' + detail) if detail else ''}")
        if not passed:
            failed += 1
    print(f"\n{len(results) - failed}/{len(results)} passed")
    return failed == 0


def main():
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)

    strict_mode = "--strict" in sys.argv

    if strict_mode:
        print("Running in STRICT mode — will exit 1 on any drift")
    else:
        print("Running in report-only mode (use --strict to exit 1 on drift)")

    any_drift = False
    registry_ok, registry_report = check_registry(
        listdirs(CLAUDE_SKILLS), listdirs(AGENTS_SKILLS)
    )
    for line in registry_report:
        print(line)
    if not registry_ok:
        any_drift = True

    for skill_name in SKILL_NAMES:
        drift = check_skill(skill_name, strict_mode)
        if drift:
            any_drift = True

    if check_agent_defs():
        any_drift = True

    print()
    if any_drift:
        print("Drift detected across mirror surfaces (see above)")
    else:
        print("No drift detected — mirrors are in sync")

    print(f"MODE: {'strict' if strict_mode else 'report-only'}")

    if strict_mode and any_drift:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
