#!/usr/bin/env python3
"""Analyze Claude Code session-store JSONL transcripts for context-window use.

Two modes, one script:

  Aggregate (default) — cross-session survey:
      python3 scripts/session_context_report.py <store_dir> [more_dirs...]
  Streams every *.jsonl under the given session-store directories, attributes
  tool_result payload bytes to the producing tool (joined via tool_use_id),
  splits main-window vs subagent-window ingress, decodes PNG headers for a
  rough image-token estimate, flags a11y-related sessions by keyword, ranks
  sessions and single results by size, and reports which files get re-read
  most (with cumulative bytes) across the whole scan.

  Drilldown — single-session detail:
      python3 scripts/session_context_report.py --drill <session.jsonl> [more...]
  Per-session tool composition, Read-target classification (source code vs.
  test artifact vs. docs vs. image file, etc.), the biggest individual Read
  paths, pasted-image count, and a rough compaction-marker count.

WHAT THIS MEASURES, AND HOW MUCH TO TRUST IT
---------------------------------------------
Every number here is derived from *transcript bytes*, not from the tokenizer
that actually ran. Token estimates use:
  - text:   len(bytes) // 4
  - images: min(1600, px // 750) tokens, where px is the pixel count (capped
            at ~1.15MP to match Claude's own downscale) decoded from the PNG
            IHDR header when a block is a base64 PNG; a flat 1100-token
            fallback otherwise (non-PNG, or the header didn't decode).
These are back-of-envelope conversions, good to roughly +/-30%, meant for
*ranking* — which tool, file, or session is biggest — not for budgeting an
actual num_ctx window or citing as a precise cost figure anywhere accuracy
matters. See docs/plans/2026-08-24-context-utilization-plan.md Sec 3 for the
measured baseline this was built to produce, and Sec 6 Phase 0 for the gate
it sits behind.

Manual cross-check (do this by hand once per new store; nothing below can do
it for you — the running harness's own token accounting isn't a file this
script can read, only a live `/usage` readout in that session): open one
session that this script scanned, note its own `/usage` context-token count,
and compare that to this script's byte/token totals for the same session
(rerun aggregate mode against that one store dir, or use --drill on that one
file). The gap between the two bounds this script's real-world error for
your session mix; if it's far outside +/-30%, treat every number below as
ranking-only and re-derive nothing budget-critical from it.

THE INPUT FORMAT IS NOT A CONTRACT
---------------------------------------------
The session-store JSONL (under a harness-managed projects directory, plus
its subagents/*.jsonl children) is a private, versionless, undocumented
implementation detail of the harness that writes it — not a published or
stable format. This script parses today's shape defensively (skips lines
that fail json.loads, tolerates missing keys) but a harness release can
change the shape at any time without notice. A parse failure, or a sudden
drop in matched rows after a harness upgrade, is the *expected* failure
mode here, not a bug in this script — re-derive the field names from a
fresh sample before trusting a changed result. See plan Sec 7 ("Honest
split"): this script is retroactive analysis only; nothing else in the repo
is built on top of it, and the supported forward-looking measurement surface
is the harness's own `/usage`/`/context` output, not this script.

SESSION-LEDGER CONVENTION (plan Sec 6 Phase 0.5)
---------------------------------------------
Audit-scope engagements should end with one run of this script's aggregate
mode against that engagement's own session-store directory, with the printed
per-tool table saved as a text file beside the engagement's other receipts.
This is a manual step: nothing here discovers the right directory or invokes
itself automatically at engagement close.

Requires: Python 3.9+, standard library only. No paths are hardcoded — store
directories and drill targets are always supplied as command-line arguments.

Run from repo root:
    python3 scripts/session_context_report.py ~/.claude/projects/<some-slug>
    python3 scripts/session_context_report.py --drill /path/to/session.jsonl
"""

import argparse
import base64
import binascii
import glob
import heapq
import json
import os
import struct
import sys
from collections import defaultdict

# a11y-relevant tool/skill names this bundle already uses elsewhere in the
# repo (see CLAUDE.md's "Browser Automation Tooling" section) — not client or
# project identifiers, just keyword flags for "was this session doing a11y
# testing work."
A11Y_MARKERS = (
    "playwright", "axe", "keyboard-a11y-tester", "baseline-url-scan",
    "agent-browser", "a11y-test", "pa11y", "virtual-screen-reader",
)

MAX_TOKENS_PER_IMAGE = 1600  # Claude vision cap, ~1.15MP / 750
FALLBACK_IMAGE_TOKENS = 1100  # used when a block isn't a decodable PNG
REPEAT_READ_MIN_COUNT = 4  # F2 threshold: "read >=4x" is what counts as a repeat
IMG_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp")


# ---------------------------------------------------------------------------
# Token/byte estimation helpers (shared; used by aggregate mode)
# ---------------------------------------------------------------------------

def est_text_tokens(nbytes):
    """Rough text-token estimate: chars/4. Ranking-grade only (+/-30%)."""
    return nbytes // 4


def png_dims_from_b64(data_prefix):
    """Decode PNG IHDR width/height from the first bytes of base64 data."""
    try:
        head = data_prefix[:64]
        pad = "=" * ((4 - len(head) % 4) % 4)
        raw = base64.b64decode(head + pad)
    except (binascii.Error, ValueError):
        return None
    if len(raw) < 24 or raw[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    try:
        w, h = struct.unpack(">II", raw[16:24])
    except struct.error:
        return None
    if 0 < w < 20000 and 0 < h < 20000:
        return (w, h)
    return None


def est_image_tokens(source):
    """Estimate vision tokens for one image block; returns (tokens, dims|None)."""
    data = source.get("data", "") if isinstance(source, dict) else ""
    dims = png_dims_from_b64(data) if data else None
    if dims:
        w, h = dims
        px = min(w * h, 1_150_000)  # Claude downscales to <=1.15MP first
        return min(MAX_TOKENS_PER_IMAGE, max(85, px // 750)), dims
    return FALLBACK_IMAGE_TOKENS, None


class Agg:
    """Running total for one (lane, tool) or (file) bucket."""

    __slots__ = ("count", "bytes", "img_count", "img_bytes", "img_tokens")

    def __init__(self):
        self.count = 0
        self.bytes = 0
        self.img_count = 0
        self.img_bytes = 0
        self.img_tokens = 0

    def add(self, nbytes, img_count=0, img_bytes=0, img_tokens=0):
        self.count += 1
        self.bytes += nbytes
        self.img_count += img_count
        self.img_bytes += img_bytes
        self.img_tokens += img_tokens


def content_stats(content):
    """Return (total_bytes, img_count, img_bytes, img_tokens, text_snippet)
    for a tool_result content value (str, list of blocks, or None)."""
    if content is None:
        return 0, 0, 0, 0, ""
    if isinstance(content, str):
        return len(content), 0, 0, 0, content[:100]
    total = imgs = ibytes = itok = 0
    snippet = ""
    if isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                total += len(str(block))
                continue
            btype = block.get("type")
            if btype == "image":
                src = block.get("source", {})
                dlen = len(src.get("data", "")) if isinstance(src, dict) else 0
                tok, _ = est_image_tokens(src)
                imgs += 1
                ibytes += dlen
                itok += tok
                total += dlen
            elif btype in ("text", "tool_result"):
                inner = block.get("text") if btype == "text" else block.get("content")
                b, ic, ib, it, snip = content_stats(inner)
                total += b
                imgs += ic
                ibytes += ib
                itok += it
                if not snippet:
                    snippet = snip
            else:
                total += len(json.dumps(block, default=str))
    return total, imgs, ibytes, itok, snippet


# ---------------------------------------------------------------------------
# Aggregate mode (default): per-tool payload table across many sessions
# ---------------------------------------------------------------------------

def _flag_a11y_markers(text, project, path, session_flags):
    low = text.lower()
    for marker in A11Y_MARKERS:
        if marker in low:
            session_flags[(project, path)].add(marker)


def _process_assistant_block(block, project, eff_lane, path, tools_by_id, stats, session_flags):
    btype = block.get("type")
    if btype == "tool_use":
        tid = block.get("id")
        name = block.get("name", "?")
        raw_input = block.get("input")
        raw_input = raw_input if isinstance(raw_input, dict) else {}
        inp = json.dumps(raw_input, default=str)
        file_path = raw_input.get("file_path") if name == "Read" else None
        if tid:
            tools_by_id[tid] = (name, inp[:160], file_path)
        stats["tool_input"][(project, eff_lane, name)].add(len(inp))
        _flag_a11y_markers(inp, project, path, session_flags)
    elif btype in ("text", "thinking"):
        txt = block.get("text") or block.get("thinking") or ""
        stats["assistant_text"][(project, eff_lane, btype)].add(len(txt))


def _process_user_tool_result(block, project, eff_lane, tools_by_id, stats, top_results):
    """Handle one tool_result block; returns lowercased text for a11y flagging."""
    tid = block.get("tool_use_id")
    name, inp, file_path = tools_by_id.get(tid, ("?unattributed", "", None))
    b, ic, ib, it, snip = content_stats(block.get("content"))
    stats["tool_result"][(project, eff_lane, name)].add(b, ic, ib, it)
    if name == "Read" and file_path:
        stats["read_paths"][file_path].add(b)
    item = (b, project, eff_lane, name, inp[:120], snip[:80], ic)
    if len(top_results) < 40:
        heapq.heappush(top_results, item)
    elif b > top_results[0][0]:
        heapq.heapreplace(top_results, item)
    if ib:
        stats["img_by_tool"][(project, eff_lane, name)].add(b, ic, ib, it)
    return (inp + snip).lower()


def _process_user_message(content, project, eff_lane, path, tools_by_id, stats, top_results, session_flags):
    # NOTE: only the last block processed sets `lowered` for the a11y-marker
    # check below (a multi-block user message doesn't accumulate). Preserved
    # intentionally from the original analyzer so published baseline figures
    # stay reproducible; revisit deliberately, not as a drive-by fix.
    lowered = None
    if isinstance(content, str):
        stats["user_text"][(project, eff_lane, "user")].add(len(content))
        lowered = content.lower()
    for block in content if isinstance(content, list) else []:
        if not isinstance(block, dict):
            continue
        if block.get("type") == "tool_result":
            lowered = _process_user_tool_result(block, project, eff_lane, tools_by_id, stats, top_results)
        elif block.get("type") == "text":
            t = block.get("text", "")
            stats["user_text"][(project, eff_lane, "user")].add(len(t))
            lowered = t.lower()
    if lowered:
        _flag_a11y_markers(lowered, project, path, session_flags)


def scan_file(path, project, is_subagent, tools_by_id, stats, top_results, session_flags):
    """Stream one *.jsonl transcript, updating stats/top_results/session_flags in place."""
    lane = "subagent" if is_subagent else "main"
    with open(path, "r", errors="replace") as fh:
        for line in fh:
            if len(line) < 20:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue  # streaming JSONL can end mid-write; skip, don't crash the scan
            if entry.get("type") == "summary":
                stats["compactions"][(project, path, lane)] += 1
                continue
            msg = entry.get("message")
            if not isinstance(msg, dict):
                continue
            content = msg.get("content")
            sidechain = entry.get("isSidechain", False)
            eff_lane = "subagent" if (is_subagent or sidechain) else "main"
            if msg.get("role") == "assistant" and isinstance(content, list):
                for block in content:
                    if isinstance(block, dict):
                        _process_assistant_block(block, project, eff_lane, path, tools_by_id, stats, session_flags)
            elif msg.get("role") == "user":
                _process_user_message(content, project, eff_lane, path, tools_by_id, stats, top_results, session_flags)
            stats["session_bytes"][(project, path, eff_lane)] += len(line)


def new_stats():
    return {
        "tool_result": defaultdict(Agg),
        "tool_input": defaultdict(Agg),
        "assistant_text": defaultdict(Agg),
        "user_text": defaultdict(Agg),
        "img_by_tool": defaultdict(Agg),
        "read_paths": defaultdict(Agg),
        "session_bytes": defaultdict(int),
        "compactions": defaultdict(int),
    }


def _project_labels(dirs):
    """Map each store dir to a short display label.

    Strips the longest common prefix shared by ALL given dirs' basenames
    (typically harness slug boilerplate repeated across sibling stores) so
    multi-store runs print readable labels. No specific path or username is
    ever hardcoded; with a single dir this is just its basename."""
    names = [os.path.basename(d.rstrip("/")) for d in dirs]
    if len(names) > 1:
        prefix = os.path.commonprefix(names)
        cut = prefix.rfind("-") + 1
        if cut > 0:
            names = [n[cut:] or n for n in names]
    return dict(zip(dirs, names))


def scan_dirs(dirs):
    """Walk every *.jsonl under each store dir; return (stats, top_results, session_flags)."""
    stats = new_stats()
    tools_by_id = {}
    top_results = []
    session_flags = defaultdict(set)
    labels = _project_labels(dirs)
    for d in dirs:
        project = labels[d]
        for path in glob.glob(os.path.join(d, "**", "*.jsonl"), recursive=True):
            is_sub = "/subagents/" in path
            scan_file(path, project, is_sub, tools_by_id, stats, top_results, session_flags)
    return stats, top_results, session_flags


def _merge_lane_tool_rows(agg_map):
    """Collapse a (project, lane, name)-keyed Agg map to (lane, name), summed over projects."""
    merged = defaultdict(Agg)
    for (_project, lane, name), a in agg_map.items():
        m = merged[(lane, name)]
        m.count += a.count
        m.bytes += a.bytes
        m.img_count += a.img_count
        m.img_bytes += a.img_bytes
        m.img_tokens += a.img_tokens
    return sorted(merged.items(), key=lambda kv: -kv[1].bytes)


def _print_tool_result_table(stats, top_n=28):
    print("== TOOL RESULT payloads entering context (all projects) ==")
    print(f"{'lane':9} {'tool':42} {'n':>6} {'MB':>8} {'~Mtok':>7} {'imgs':>5} {'imgMB':>7} {'imgKtok':>8}")
    for (lane, name), a in _merge_lane_tool_rows(stats["tool_result"])[:top_n]:
        text_bytes = a.bytes - a.img_bytes
        mtok = (est_text_tokens(text_bytes) + a.img_tokens) / 1e6
        print(
            f"{lane:9} {name[:42]:42} {a.count:>6} {a.bytes/1e6:>8.1f} {mtok:>7.2f} "
            f"{a.img_count:>5} {a.img_bytes/1e6:>7.1f} {a.img_tokens/1e3:>8.1f}"
        )


def _print_repeat_reads(stats, min_count=REPEAT_READ_MIN_COUNT, top_n=28):
    """F2: which file_paths get re-Read the most, and how many cumulative
    bytes that costs. Keyed by literal file_path, so it spans projects/lanes
    (a file re-read across many sessions is exactly the pattern this
    surfaces)."""
    print(f"\n== Repeat Reads (same file_path Read >= {min_count}x) ==")
    rows = [(fp, a) for fp, a in stats["read_paths"].items() if a.count >= min_count]
    rows.sort(key=lambda kv: -kv[1].bytes)
    total_bytes = sum(a.bytes for _fp, a in rows)
    print(f"{len(rows)} files, {total_bytes/1e6:.1f} MB cumulative")
    for fp, a in rows[:top_n]:
        print(f"  {a.count:>4}x {a.bytes/1e3:>9.0f}KB  {fp[-100:]}")


def _print_assistant_text(stats):
    print("\n== ASSISTANT text/thinking bytes ==")
    for (lane, name), a in _merge_lane_tool_rows(stats["assistant_text"]):
        print(f"{lane:9} {name:12} {a.count:>7} blocks {a.bytes/1e6:>8.1f} MB")


def _rank_sessions(stats):
    per_session = defaultdict(lambda: [0, 0])
    for (project, path, lane), b in stats["session_bytes"].items():
        per_session[(project, path)][0 if lane == "main" else 1] += b
    return per_session


def _print_top_sessions(per_session, session_flags, top_n=15):
    print(f"\n== MAIN-window sessions by size (top {top_n}) ==")
    ranked = sorted(per_session.items(), key=lambda kv: -kv[1][0])[:top_n]
    for (project, path), (mb, sb) in ranked:
        flags = ",".join(sorted(session_flags.get((project, path), []))[:4]) or "-"
        print(
            f"{mb/1e6:>7.1f}MB main {sb/1e6:>7.1f}MB sub  "
            f"{project[:28]:28} {os.path.basename(path)[:20]:20} [{flags}]"
        )


def _print_a11y_summary(per_session, session_flags):
    print("\n== a11y-flagged sessions: aggregate ==")
    fl_main = fl_sub = n_fl = 0
    for key, flags in session_flags.items():
        if flags:
            n_fl += 1
            fl_main += per_session[key][0]
            fl_sub += per_session[key][1]
    print(f"{n_fl} flagged sessions: {fl_main/1e6:.1f} MB main-window, {fl_sub/1e6:.1f} MB subagent")


def _print_top_results(top_results, top_n=25):
    print("\n== TOP single tool results (bytes desc) ==")
    for b, project, lane, name, inp, snip, ic in sorted(top_results, reverse=True)[:top_n]:
        print(f"{b/1e3:>9.0f}KB {lane:8} {name[:34]:34} imgs={ic} | {inp[:90].replace(chr(10), ' ')}")


def _print_compactions(stats):
    print("\n== Compaction summary-lines per project ==")
    comp = defaultdict(int)
    for (project, _path, _lane), n in stats["compactions"].items():
        comp[project] += n
    for project, n in sorted(comp.items(), key=lambda kv: -kv[1]):
        print(f"{n:>5}  {project}")


def run_aggregate(dirs):
    stats, top_results, session_flags = scan_dirs(dirs)
    per_session = _rank_sessions(stats)
    _print_tool_result_table(stats)
    _print_repeat_reads(stats)
    _print_assistant_text(stats)
    _print_top_sessions(per_session, session_flags)
    _print_a11y_summary(per_session, session_flags)
    _print_top_results(top_results)
    _print_compactions(stats)


# ---------------------------------------------------------------------------
# Drilldown mode (--drill): per-session composition detail
# ---------------------------------------------------------------------------

def classify_read(path):
    p = path.lower()
    base = os.path.basename(p)
    if p.endswith(IMG_EXT):
        return "image-file"
    if "axe" in base or "violations" in base:
        return "axe-json"
    if any(k in p for k in ("findings", "trace", "census", "artifacts/", "results/")):
        return "test-artifact"
    if p.endswith((".json", ".jsonl")):
        return "other-json"
    if p.endswith((".spec.js", ".spec.ts", ".test.js", ".mjs")):
        return "test-code"
    if "skill.md" in base or "/skills/" in p or "/agents/" in p:
        return "skill/agent-def"
    if p.endswith((".md", ".yaml", ".yml")):
        return "docs/config"
    return "source-code"


def _track_drill_tool_use(block, tools_by_id):
    if isinstance(block, dict) and block.get("type") == "tool_use":
        tools_by_id[block.get("id")] = (block.get("name", "?"), block.get("input", {}))


def _process_drill_tool_result(block, tools_by_id, per_tool, read_class, read_tops):
    name, inp = tools_by_id.get(block.get("tool_use_id"), ("?", {}))
    raw = json.dumps(block.get("content"), default=str)
    imgs = raw.count('"type": "image"') + raw.count('"type":"image"')
    per_tool[name][0] += len(raw)
    per_tool[name][1] += 1
    per_tool[name][2] += imgs
    if name == "Read" and isinstance(inp, dict):
        fp = inp.get("file_path", "?")
        cls = classify_read(fp)
        read_class[cls][0] += len(raw)
        read_class[cls][1] += 1
        read_tops.append((len(raw), fp))


def _process_drill_user_message(content, tools_by_id, per_tool, read_class, read_tops, pasted_imgs):
    if not isinstance(content, list):
        return
    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") == "image":
            src = block.get("source", {})
            pasted_imgs[0] += 1
            pasted_imgs[1] += len(src.get("data", "")) if isinstance(src, dict) else 0
        elif block.get("type") == "tool_result":
            _process_drill_tool_result(block, tools_by_id, per_tool, read_class, read_tops)


def _is_compact_marker(line):
    return (
        '"isCompactSummary":true' in line
        or '"subtype":"compact_boundary"' in line
        or '"type":"summary"' in line
    )


def drill_scan(path):
    """Parse one session transcript and print its per-tool composition report."""
    try:
        fh = open(path, errors="replace")
    except OSError as exc:
        print(f"!! cannot open {path}: {exc}", file=sys.stderr)
        return

    tools_by_id = {}
    per_tool = defaultdict(lambda: [0, 0, 0])  # bytes, count, imgs
    read_class = defaultdict(lambda: [0, 0])  # bytes, count
    read_tops = []
    pasted_imgs = [0, 0]  # count, bytes
    compact_markers = 0
    turns = 0
    with fh:
        for line in fh:
            if _is_compact_marker(line):
                compact_markers += 1
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = entry.get("message")
            if not isinstance(msg, dict):
                continue
            content = msg.get("content")
            if msg.get("role") == "assistant" and isinstance(content, list):
                for block in content:
                    _track_drill_tool_use(block, tools_by_id)
            elif msg.get("role") == "user":
                turns += 1
                _process_drill_user_message(content, tools_by_id, per_tool, read_class, read_tops, pasted_imgs)

    _print_drill_report(path, turns, compact_markers, pasted_imgs, per_tool, read_class, read_tops)


def _print_drill_report(path, turns, compact_markers, pasted_imgs, per_tool, read_class, read_tops):
    size_mb = os.path.getsize(path) / 1e6
    print(
        f"\n### {os.path.basename(path)}  ({size_mb:.1f}MB file, {turns} user-turns, "
        f"compact-markers={compact_markers}, pasted-images={pasted_imgs[0]} "
        f"({pasted_imgs[1]/1e3:.0f}KB))"
    )
    for name, (b, n, i) in sorted(per_tool.items(), key=lambda kv: -kv[1][0])[:8]:
        print(f"  {name[:40]:40} {b/1e3:>8.0f}KB {n:>5}x imgs={i}")
    if not read_class:
        return
    print("  -- Read targets --")
    for cls, (b, n) in sorted(read_class.items(), key=lambda kv: -kv[1][0]):
        print(f"    {cls:18} {b/1e3:>8.0f}KB {n:>4}x")
    for b, fp in sorted(read_tops, reverse=True)[:5]:
        print(f"    top: {b/1e3:>6.0f}KB {fp[-100:]}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_arg_parser():
    parser = argparse.ArgumentParser(
        prog="session_context_report.py",
        description=(
            "Analyze Claude Code session-store JSONL transcripts for "
            "context-window consumption. See the module docstring for "
            "method, caveats, and the session-ledger convention."
        ),
    )
    parser.add_argument(
        "dirs",
        nargs="*",
        metavar="STORE_DIR",
        help="Session-store directories to scan in aggregate mode (default). Ignored if --drill is given.",
    )
    parser.add_argument(
        "--drill",
        nargs="+",
        metavar="SESSION_JSONL",
        help="Drilldown mode: per-session detail for one or more *.jsonl transcript files.",
    )
    return parser


def main(argv=None):
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    if args.drill:
        for path in args.drill:
            drill_scan(path)
        return 0
    if args.dirs:
        run_aggregate(args.dirs)
        return 0
    parser.print_help(sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
