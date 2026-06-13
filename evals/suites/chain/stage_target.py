#!/usr/bin/env python3
"""I1 (plan 011): stage a chain-eval target into an isolated working dir OUTSIDE the
eval tree, so a judgment subagent given the staged path cannot navigate (`..`) to the
answer key (`rubrics/<id>.chain.yaml`) or the source `*.metadata.yaml`.

This is the PREVENTION layer for the contamination hole the pilot found (the video
critic read the rubric). `detect_peek()` in score_chain.py is the detection backstop.
Mirrors the cloud runner's neutral-cwd isolation pattern.

Usage:
    python3 evals/suites/chain/stage_target.py <fixture-id> [--dest DIR]

Prints the absolute staged path on stdout. Copies ONLY the component/styles/README a
real reviewer would see -- never the rubric or metadata. Default dest:
$TMPDIR/chain-stage/<fixture-id>/ (`..` from there lands in chain-stage/, no answer key).
"""
import os, sys, shutil, tempfile

BASE = os.path.dirname(os.path.abspath(__file__))
TARGETS = os.path.join(BASE, "targets")
EVAL_TREE = os.path.abspath(os.path.join(BASE, "..", ".."))  # .../evals
SAFE_NAMES = ("component.jsx", "component.tsx", "component.js", "styles.css", "README.md")


def stage(fixture_id, dest=None):
    src = os.path.join(TARGETS, fixture_id)
    if not os.path.isdir(src):
        sys.exit(f"target not found: {src}")
    if dest is None:
        # Neutral leaf name: a fixture id can encode its expected verdict (e.g. "...-clean"),
        # so it must NOT appear in the path the agent sees. Stage one fixture at a time.
        dest = os.path.join(tempfile.gettempdir(), "chain-stage", "component")
    dest = os.path.abspath(dest)
    # Guard: never stage inside the eval tree -- that would defeat the isolation.
    if dest.startswith(EVAL_TREE):
        sys.exit(f"refusing to stage inside the eval tree: {dest}")
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    copied = []
    for name in sorted(os.listdir(src)):
        if name in SAFE_NAMES:
            shutil.copy2(os.path.join(src, name), os.path.join(dest, name))
            copied.append(name)
    return dest, copied


def main():
    pos = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not pos:
        print(__doc__)
        sys.exit(1)
    dest = None
    if "--dest" in sys.argv:
        i = sys.argv.index("--dest")
        dest = sys.argv[i + 1] if i + 1 < len(sys.argv) else None
    path, copied = stage(pos[0], dest)
    print(path)
    print(f"# staged {len(copied)} files ({', '.join(copied)}); answer key NOT copied",
          file=sys.stderr)


if __name__ == "__main__":
    main()
