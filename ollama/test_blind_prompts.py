#!/usr/bin/env python3
"""Regression guard: no benchmark prompt may contain a fixture's answer key.

Added post-003 (2026-07-13) after finding that both runners fed raw fixtures —
including the '## Accessibility Issues (Planted Bugs)' sections — to every lane
that ever ran. Builds real prompt content through BOTH runners for EVERY critic
and perspective fixture and fails if any answer-key marker survives.

Run: python3 ollama/test_blind_prompts.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import run_benchmark as local_runner  # noqa: E402
import run_cloud_benchmark as cloud_runner  # noqa: E402

MARKERS = ("## Accessibility Issues", "Planted Bugs")


def fixture_ids(directory):
    return sorted(f[:-3] for f in os.listdir(directory) if f.endswith(".md"))


def main():
    failures = []
    checks = 0

    for runner, label in ((local_runner, "local"), (cloud_runner, "cloud")):
        # Critic suite: the fixture content each critic prompt embeds.
        for fid in fixture_ids(runner.FIXTURES_DIR):
            content = runner.load_fixture(fid)
            checks += 1
            for marker in MARKERS:
                if marker in content:
                    failures.append(f"{label} critic {fid}: contains {marker!r}")
        # Perspective suite: the full composed user prompt.
        for fid in fixture_ids(runner.PERSPECTIVE_FIXTURES_DIR):
            prompt = runner.build_escalation_prompt(fid)
            checks += 1
            for marker in MARKERS:
                if marker in prompt:
                    failures.append(f"{label} perspective {fid}: contains {marker!r}")

    if failures:
        print(f"FAIL — {len(failures)} leaked prompt(s) of {checks} checked:")
        for f in failures:
            print(f"  {f}")
        sys.exit(1)
    print(f"OK — {checks} prompts checked across both runners; no answer-key markers.")


if __name__ == "__main__":
    main()
