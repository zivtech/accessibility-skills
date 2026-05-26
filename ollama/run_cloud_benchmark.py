#!/usr/bin/env python3
"""Run a11y skill benchmarks on cloud models (Claude API + Codex/OpenAI).

Supports bottom-up escalation: starts with the cheapest tier per platform,
runs all fixtures, scores, and only escalates failed fixtures to the next tier.

Usage:
    # Claude API (requires ANTHROPIC_API_KEY)
    python3 ollama/run_cloud_benchmark.py claude <tier> <fixture-id>
    python3 ollama/run_cloud_benchmark.py claude-all <tier>
    python3 ollama/run_cloud_benchmark.py claude-escalate [--skill critic|perspective]

    # Codex/OpenAI (requires codex CLI auth)
    python3 ollama/run_cloud_benchmark.py codex <tier> <fixture-id>
    python3 ollama/run_cloud_benchmark.py codex-all <tier>
    python3 ollama/run_cloud_benchmark.py codex-escalate [--skill critic|perspective]

    # Score all cloud results
    python3 ollama/run_cloud_benchmark.py score-cloud
    python3 ollama/run_cloud_benchmark.py score-cloud-perspective

    # Show escalation summary
    python3 ollama/run_cloud_benchmark.py summary

Claude tiers (cheapest first):
    haiku           Claude Haiku 4.5 (no thinking)
    sonnet          Claude Sonnet 4.6 (no thinking)
    sonnet-think    Claude Sonnet 4.6 (thinking, 2048 budget)
    opus            Claude Opus 4.7

Codex/OpenAI tiers (cheapest first):
    5.2             GPT-5.2
    5.2-low         GPT-5.2, reasoning_effort=low
    5.5             GPT-5.5
    5.5-low         GPT-5.5, reasoning_effort=low
"""

import glob
import json
import os
import subprocess
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(BASE_DIR)

SKILL_PATH = os.path.join(REPO_DIR, ".claude", "skills", "a11y-critic", "SKILL.md")
FIXTURES_DIR = os.path.join(REPO_DIR, "evals", "suites", "a11y-critic", "fixtures")

PERSPECTIVE_SKILL_PATH = os.path.join(REPO_DIR, ".claude", "skills", "perspective-audit", "SKILL.md")
PERSPECTIVE_FIXTURES_DIR = os.path.join(REPO_DIR, "evals", "suites", "perspectives", "fixtures")
PERSPECTIVE_REFS = [
    os.path.join(REPO_DIR, ".claude", "skills", "perspective-audit", "references", "perspectives.md"),
    os.path.join(REPO_DIR, ".claude", "skills", "perspective-audit", "references", "arrm-perspective-mapping.md"),
]

CRITIC_PROMPT_PREFIX = (
    "Review the following React component for accessibility design issues. "
    "Execute all phases of the investigation protocol.\n\n"
)

CLAUDE_TIERS = [
    {
        "name": "haiku",
        "model": "claude-haiku-4-5-20251001",
        "thinking": None,
        "max_tokens": 8192,
        "label": "Haiku 4.5",
    },
    {
        "name": "sonnet",
        "model": "claude-sonnet-4-6",
        "thinking": None,
        "max_tokens": 8192,
        "label": "Sonnet 4.6",
    },
    {
        "name": "sonnet-think",
        "model": "claude-sonnet-4-6",
        "thinking": {"type": "enabled", "budget_tokens": 2048},
        "max_tokens": 12288,
        "label": "Sonnet 4.6 + thinking",
    },
    {
        "name": "opus",
        "model": "claude-opus-4-7",
        "thinking": None,
        "max_tokens": 8192,
        "label": "Opus 4.7",
    },
]

CODEX_TIERS = [
    {"name": "5.2", "model": "gpt-5.2", "effort": None, "label": "GPT-5.2"},
    {"name": "5.2-low", "model": "gpt-5.2", "effort": "low", "label": "GPT-5.2 (low)"},
    {"name": "5.5", "model": "gpt-5.5", "effort": None, "label": "GPT-5.5"},
    {"name": "5.5-low", "model": "gpt-5.5", "effort": "low", "label": "GPT-5.5 (low)"},
]

ALL_CRITIC_FIXTURES = [
    "button-skip-link-clean", "interactive-dropdown-clean", "modal-complete-clean",
    "search-results-dynamic-clean",
    "form-validation-missing-aria-describedby", "tabs-missing-arrow-nav",
    "toast-notification-no-role", "accordion-no-region-role",
    "breadcrumb-navigation-no-nav-landmark", "checkbox-group-no-fieldset",
    "combobox-autocomplete-no-listbox-role", "data-table-missing-scope",
    "expandable-section-no-button", "file-input-no-labels",
    "heading-hierarchy-skipped", "image-carousel-no-region",
    "infinite-scroll-no-announcement", "interactive-dropdown-focus-bug",
    "loading-state-missing-aria-busy", "megamenu-no-structure",
    "pagination-no-nav-landmark", "popover-no-focus-management",
    "radio-button-group-no-grouping", "tooltip-no-role-no-association",
    "video-player-missing-captions",
    "tabs-incomplete-aria-selected", "multistep-form-error-clearing",
    "dashboard-heading-inconsistency", "app-focus-order-illogical",
    "async-form-vague-success",
    "tabbed-nav-vs-tab-pattern", "form-field-vs-summary-errors",
    "search-focus-stays-in-input",
]

ALL_PERSPECTIVE_FIXTURES = [
    "animated-onboarding-flow", "article-page-clean", "autocomplete-fast-timeout",
    "chat-cognitive-load", "checkout-form-broken-errors", "color-only-status-indicators",
    "custom-select-combobox", "dashboard-text-labels", "data-table-sortable-columns",
    "data-viz-color-encoding", "dense-admin-jargon", "hover-reveal-navigation",
    "image-gallery-small-targets", "infinite-scroll-cognitive", "login-form-clean",
    "map-interface-zoom", "media-player-captions", "modal-broken-focus-trap",
    "multi-column-pricing", "nav-menu-landmarks", "podcast-audio-only",
    "product-carousel-autoplay", "search-results-dynamic-update",
    "tab-panel-arrow-keys", "video-tutorial-no-captions",
]


def strip_frontmatter(content):
    if content.startswith("---"):
        end = content.index("---", 3)
        return content[end + 3:].strip()
    return content


def load_critic_system_prompt():
    with open(SKILL_PATH) as f:
        return strip_frontmatter(f.read())


def load_perspective_system_prompt():
    with open(PERSPECTIVE_SKILL_PATH) as f:
        content = strip_frontmatter(f.read())
    for ref_path in PERSPECTIVE_REFS:
        if os.path.exists(ref_path):
            with open(ref_path) as f:
                content += "\n\n---\n\n" + f.read()
    return content


def load_fixture(fixture_id, fixtures_dir=None):
    d = fixtures_dir or FIXTURES_DIR
    with open(os.path.join(d, f"{fixture_id}.md")) as f:
        return f.read()


def build_escalation_prompt(fixture_id):
    import yaml
    metadata_path = os.path.join(PERSPECTIVE_FIXTURES_DIR, f"{fixture_id}.metadata.yaml")
    with open(metadata_path) as f:
        meta = yaml.safe_load(f)
    alarm_levels = meta.get("expected_alarm_levels", {})
    escalated = [
        f"- {name.replace('_', ' ').title()}: {level}"
        for name, level in alarm_levels.items()
        if level in ("MEDIUM", "HIGH")
    ]
    fixture_content = load_fixture(fixture_id, PERSPECTIVE_FIXTURES_DIR)
    if escalated:
        escalation_block = "## Escalated Perspectives (from a11y-critic)\n\n" + "\n".join(escalated)
    else:
        escalation_block = (
            "## Escalated Perspectives\n\n"
            "All perspectives at LOW — this is a CLEAN baseline. "
            "Produce PASS verdict with no CRITICAL/MAJOR findings."
        )
    return (
        "Run the perspective audit on the following component. "
        "The escalated perspectives are listed below.\n\n"
        f"{escalation_block}\n\n"
        f"## Component Under Review\n\n{fixture_content}"
    )


def get_tier(platform, tier_name):
    tiers = CLAUDE_TIERS if platform == "claude" else CODEX_TIERS
    for t in tiers:
        if t["name"] == tier_name:
            return t
    names = [t["name"] for t in tiers]
    print(f"Unknown tier '{tier_name}'. Available: {', '.join(names)}")
    sys.exit(1)


def output_path(platform, tier_name, fixture_id, skill="critic"):
    prefix = "cloud" if platform == "claude" else "codex"
    tag = tier_name.replace(".", "").replace("-", "")
    skill_tag = f"-{skill}" if skill != "critic" else ""
    return f"/tmp/{prefix}-bench{skill_tag}-{fixture_id}-{tag}-response.json"


def result_exists(platform, tier_name, fixture_id, skill="critic"):
    path = output_path(platform, tier_name, fixture_id, skill)
    if not os.path.exists(path):
        return False
    with open(path) as f:
        data = json.load(f)
    return len(data.get("response", "")) > 100


# ── Claude API ──────────────────────────────────────────────────────────


def run_claude(tier, fixture_id, system_prompt, user_prompt, skill="critic"):
    import anthropic
    client = anthropic.Anthropic()
    out = output_path("claude", tier["name"], fixture_id, skill)

    print(f"\n{'=' * 60}")
    print(f"CLAUDE | {tier['label']} | {fixture_id} ({skill})")
    print(f"Output: {out}")
    print(f"Started: {time.strftime('%H:%M:%S')}")

    kwargs = {
        "model": tier["model"],
        "max_tokens": tier["max_tokens"],
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
        "temperature": 0.3,
    }
    if tier.get("thinking"):
        kwargs["thinking"] = tier["thinking"]
        del kwargs["temperature"]

    start = time.time()
    response = client.messages.create(**kwargs)
    elapsed = time.time() - start

    response_text = ""
    thinking_text = ""
    for block in response.content:
        if block.type == "thinking":
            thinking_text += block.thinking
        elif block.type == "text":
            response_text += block.text

    data = {
        "response": response_text,
        "done": True,
        "thinking": thinking_text if thinking_text else None,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "_benchmark": {
            "platform": "claude",
            "model": tier["model"],
            "tier": tier["name"],
            "fixture_id": fixture_id,
            "skill": skill,
            "elapsed_seconds": round(elapsed, 1),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        },
    }

    with open(out, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Done: {time.strftime('%H:%M:%S')} ({elapsed:.1f}s, {len(response_text)} chars)")
    print(f"Tokens: {response.usage.input_tokens} in / {response.usage.output_tokens} out")
    return out


def run_claude_critic(tier, fixture_id):
    system_prompt = load_critic_system_prompt()
    fixture_content = load_fixture(fixture_id)
    user_prompt = CRITIC_PROMPT_PREFIX + fixture_content
    return run_claude(tier, fixture_id, system_prompt, user_prompt, "critic")


def run_claude_perspective(tier, fixture_id):
    system_prompt = load_perspective_system_prompt()
    user_prompt = build_escalation_prompt(fixture_id)
    return run_claude(tier, fixture_id, system_prompt, user_prompt, "perspective")


# ── Codex/OpenAI ────────────────────────────────────────────────────────


def run_codex(tier, fixture_id, system_prompt, user_prompt, skill="critic"):
    out = output_path("codex", tier["name"], fixture_id, skill)
    msg_out = f"/tmp/codex-msg-{tier['name']}-{fixture_id}-{skill}.txt"

    print(f"\n{'=' * 60}")
    print(f"CODEX | {tier['label']} | {fixture_id} ({skill})")
    print(f"Output: {out}")
    print(f"Started: {time.strftime('%H:%M:%S')}")

    full_prompt = (
        "You are an accessibility design reviewer. "
        "Analyze ONLY the component provided below — do not read files, "
        "run commands, or use any tools. Output your complete review as text.\n\n"
        f"## Investigation Protocol\n\n{system_prompt}\n\n"
        f"## Task\n\n{user_prompt}"
    )

    cmd = [
        "codex", "exec",
        "-m", tier["model"],
        "--sandbox", "read-only",
        "--ephemeral",
        "--ignore-rules",
        "--ignore-user-config",
        "--skip-git-repo-check",
        "-o", msg_out,
    ]
    if tier.get("effort"):
        cmd.extend(["-c", f'model_reasoning_effort="{tier["effort"]}"'])

    start = time.time()
    proc = subprocess.run(
        cmd,
        input=full_prompt,
        capture_output=True,
        text=True,
        timeout=300,
    )
    elapsed = time.time() - start

    response_text = ""
    if os.path.exists(msg_out):
        with open(msg_out) as f:
            response_text = f.read().strip()
        os.unlink(msg_out)

    if proc.returncode != 0 and not response_text:
        print(f"ERROR: codex exec failed (rc={proc.returncode})")
        if proc.stderr:
            print(f"STDERR: {proc.stderr[:500]}")
        return None

    data = {
        "response": response_text,
        "done": True,
        "_benchmark": {
            "platform": "codex",
            "model": tier["model"],
            "tier": tier["name"],
            "fixture_id": fixture_id,
            "skill": skill,
            "effort": tier.get("effort"),
            "elapsed_seconds": round(elapsed, 1),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        },
    }

    with open(out, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Done: {time.strftime('%H:%M:%S')} ({elapsed:.1f}s, {len(response_text)} chars)")
    return out


def run_codex_critic(tier, fixture_id):
    system_prompt = load_critic_system_prompt()
    fixture_content = load_fixture(fixture_id)
    user_prompt = CRITIC_PROMPT_PREFIX + fixture_content
    return run_codex(tier, fixture_id, system_prompt, user_prompt, "critic")


def run_codex_perspective(tier, fixture_id):
    system_prompt = load_perspective_system_prompt()
    user_prompt = build_escalation_prompt(fixture_id)
    return run_codex(tier, fixture_id, system_prompt, user_prompt, "perspective")


# ── Scoring ─────────────────────────────────────────────────────────────


def score_cloud_results(skill="critic"):
    if skill == "critic":
        score_script = os.path.join(BASE_DIR, "score_output.py")
        pattern = "/tmp/cloud-bench-*-response.json"
        fixtures_dir = FIXTURES_DIR
    else:
        score_script = os.path.join(BASE_DIR, "score_perspective.py")
        pattern = "/tmp/cloud-bench-perspective-*-response.json"
        fixtures_dir = PERSPECTIVE_FIXTURES_DIR

    responses = sorted(glob.glob(pattern))
    if not responses:
        print(f"No {skill} response files found matching {pattern}")
        return {}

    results = {}
    for resp in responses:
        with open(resp) as f:
            bench = json.load(f).get("_benchmark", {})
        fixture_id = bench.get("fixture_id", "")
        tier = bench.get("tier", "unknown")
        if not fixture_id:
            continue
        metadata = os.path.join(fixtures_dir, f"{fixture_id}.metadata.yaml")
        if not os.path.exists(metadata):
            continue

        print(f"\n{'=' * 60}")
        print(f"Scoring: {fixture_id} ({tier})")
        print(f"{'=' * 60}")
        proc = subprocess.run(
            [sys.executable, score_script, resp, metadata],
            capture_output=True, text=True,
        )
        print(proc.stdout)
        if "Status: PASS" in proc.stdout:
            results.setdefault(tier, {"pass": 0, "fail": 0, "warn": 0})["pass"] += 1
        elif "Status: FAIL" in proc.stdout:
            results.setdefault(tier, {"pass": 0, "fail": 0, "warn": 0})["fail"] += 1
        elif "Status: WARN" in proc.stdout:
            results.setdefault(tier, {"pass": 0, "fail": 0, "warn": 0})["warn"] += 1

    return results


def score_codex_results(skill="critic"):
    if skill == "critic":
        score_script = os.path.join(BASE_DIR, "score_output.py")
        pattern = "/tmp/codex-bench-*-response.json"
        fixtures_dir = FIXTURES_DIR
    else:
        score_script = os.path.join(BASE_DIR, "score_perspective.py")
        pattern = "/tmp/codex-bench-perspective-*-response.json"
        fixtures_dir = PERSPECTIVE_FIXTURES_DIR

    responses = sorted(glob.glob(pattern))
    if not responses:
        print(f"No {skill} response files found matching {pattern}")
        return {}

    results = {}
    for resp in responses:
        with open(resp) as f:
            bench = json.load(f).get("_benchmark", {})
        fixture_id = bench.get("fixture_id", "")
        tier = bench.get("tier", "unknown")
        if not fixture_id:
            continue
        metadata = os.path.join(fixtures_dir, f"{fixture_id}.metadata.yaml")
        if not os.path.exists(metadata):
            continue

        print(f"\n{'=' * 60}")
        print(f"Scoring: {fixture_id} ({tier})")
        print(f"{'=' * 60}")
        proc = subprocess.run(
            [sys.executable, score_script, resp, metadata],
            capture_output=True, text=True,
        )
        print(proc.stdout)
        if "Status: PASS" in proc.stdout:
            results.setdefault(tier, {"pass": 0, "fail": 0, "warn": 0})["pass"] += 1
        elif "Status: FAIL" in proc.stdout:
            results.setdefault(tier, {"pass": 0, "fail": 0, "warn": 0})["fail"] += 1
        elif "Status: WARN" in proc.stdout:
            results.setdefault(tier, {"pass": 0, "fail": 0, "warn": 0})["warn"] += 1

    return results


# ── Escalation ──────────────────────────────────────────────────────────


def get_failed_fixtures(platform, tier_name, skill="critic"):
    """Score all results for a tier and return fixture IDs that didn't PASS."""
    if skill == "critic":
        score_script = os.path.join(BASE_DIR, "score_output.py")
        fixtures_dir = FIXTURES_DIR
        all_fixtures = ALL_CRITIC_FIXTURES
    else:
        score_script = os.path.join(BASE_DIR, "score_perspective.py")
        fixtures_dir = PERSPECTIVE_FIXTURES_DIR
        all_fixtures = ALL_PERSPECTIVE_FIXTURES

    failed = []
    not_run = []
    for fixture_id in all_fixtures:
        out = output_path(platform, tier_name, fixture_id, skill)
        if not os.path.exists(out):
            not_run.append(fixture_id)
            continue
        metadata = os.path.join(fixtures_dir, f"{fixture_id}.metadata.yaml")
        if not os.path.exists(metadata):
            not_run.append(fixture_id)
            continue

        proc = subprocess.run(
            [sys.executable, score_script, out, metadata],
            capture_output=True, text=True,
        )
        if "Status: PASS" not in proc.stdout:
            failed.append(fixture_id)

    return failed, not_run


def run_escalation(platform, skill="critic"):
    tiers = CLAUDE_TIERS if platform == "claude" else CODEX_TIERS
    all_fixtures = ALL_CRITIC_FIXTURES if skill == "critic" else ALL_PERSPECTIVE_FIXTURES

    if platform == "claude":
        run_fn = run_claude_critic if skill == "critic" else run_claude_perspective
    else:
        run_fn = run_codex_critic if skill == "critic" else run_codex_perspective

    remaining = list(all_fixtures)
    tier_results = []

    for tier in tiers:
        if not remaining:
            break

        print(f"\n{'#' * 60}")
        print(f"# TIER: {tier['label']} — {len(remaining)} fixtures to run")
        print(f"{'#' * 60}")

        for i, fixture_id in enumerate(remaining, 1):
            if result_exists(platform, tier["name"], fixture_id, skill):
                print(f"[{i}/{len(remaining)}] {fixture_id} — already done, skipping")
                continue
            print(f"\n[{i}/{len(remaining)}]")
            run_fn(tier, fixture_id)

        failed, not_run = get_failed_fixtures(platform, tier["name"], skill)
        # Only count fixtures that were actually in this tier's scope
        ran_this_tier = [f for f in remaining if f not in not_run]
        passed = len(ran_this_tier) - len([f for f in failed if f in remaining])

        tier_results.append({
            "tier": tier["name"],
            "label": tier["label"],
            "ran": len(ran_this_tier),
            "passed": passed,
            "failed": len(failed),
            "not_run": len(not_run),
        })

        print(f"\n{'─' * 60}")
        print(f"Tier {tier['label']}: {passed} PASS / {len(failed)} FAIL / {len(not_run)} NOT_RUN")

        # Escalate both failures AND not-run (model didn't exist, API error, etc.)
        remaining = failed + [f for f in not_run if f in remaining]
        if not remaining:
            print(f"\nAll fixtures passed at {tier['label']} tier!")
            break

    print(f"\n{'=' * 60}")
    print(f"ESCALATION SUMMARY ({platform}, {skill})")
    print(f"{'=' * 60}")
    for r in tier_results:
        pct = r["passed"] / max(r["passed"] + r["failed"], 1) * 100
        print(f"  {r['label']}: ran {r['ran']}, {r['passed']} pass ({pct:.0f}%), {r['failed']} fail")

    if remaining:
        print(f"\n  {len(remaining)} fixtures still failing after all tiers:")
        for f in remaining:
            print(f"    - {f}")
    else:
        cheapest = tier_results[0]["label"]
        all_passed_at = next(
            (r["label"] for r in tier_results if r["failed"] == 0),
            "none"
        )
        print(f"\n  Cheapest tier with 100% pass: {all_passed_at}")

    return tier_results


# ── Summary ─────────────────────────────────────────────────────────────


def show_summary():
    platforms = {
        "claude": {"prefix": "cloud", "tiers": CLAUDE_TIERS},
        "codex": {"prefix": "codex", "tiers": CODEX_TIERS},
    }

    for platform, info in platforms.items():
        for skill in ["critic", "perspective"]:
            skill_tag = f"-{skill}" if skill != "critic" else ""
            pattern = f"/tmp/{info['prefix']}-bench{skill_tag}-*-response.json"
            files = glob.glob(pattern)
            if not files:
                continue

            print(f"\n{platform.upper()} {skill.upper()}")
            print(f"{'─' * 40}")

            by_tier = {}
            for f in files:
                with open(f) as fh:
                    bench = json.load(fh).get("_benchmark", {})
                tier = bench.get("tier", "unknown")
                by_tier.setdefault(tier, []).append(bench.get("fixture_id", ""))

            for tier_def in info["tiers"]:
                if tier_def["name"] in by_tier:
                    count = len(by_tier[tier_def["name"]])
                    print(f"  {tier_def['label']}: {count} results")


# ── Main ────────────────────────────────────────────────────────────────


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "claude":
        if len(sys.argv) != 4:
            print("Usage: run_cloud_benchmark.py claude <tier> <fixture-id>")
            sys.exit(1)
        tier = get_tier("claude", sys.argv[2])
        run_claude_critic(tier, sys.argv[3])

    elif cmd == "claude-perspective":
        if len(sys.argv) != 4:
            print("Usage: run_cloud_benchmark.py claude-perspective <tier> <fixture-id>")
            sys.exit(1)
        tier = get_tier("claude", sys.argv[2])
        run_claude_perspective(tier, sys.argv[3])

    elif cmd == "claude-all":
        if len(sys.argv) < 3:
            print("Usage: run_cloud_benchmark.py claude-all <tier> [--skill critic|perspective]")
            sys.exit(1)
        tier = get_tier("claude", sys.argv[2])
        skill = "critic"
        if "--skill" in sys.argv:
            skill = sys.argv[sys.argv.index("--skill") + 1]
        fixtures = ALL_CRITIC_FIXTURES if skill == "critic" else ALL_PERSPECTIVE_FIXTURES
        run_fn = run_claude_critic if skill == "critic" else run_claude_perspective
        for i, fid in enumerate(fixtures, 1):
            if result_exists("claude", tier["name"], fid, skill):
                print(f"[{i}/{len(fixtures)}] {fid} — already done, skipping")
                continue
            print(f"\n[{i}/{len(fixtures)}]")
            run_fn(tier, fid)

    elif cmd == "claude-escalate":
        skill = "critic"
        if "--skill" in sys.argv:
            skill = sys.argv[sys.argv.index("--skill") + 1]
        run_escalation("claude", skill)

    elif cmd == "codex":
        if len(sys.argv) != 4:
            print("Usage: run_cloud_benchmark.py codex <tier> <fixture-id>")
            sys.exit(1)
        tier = get_tier("codex", sys.argv[2])
        run_codex_critic(tier, sys.argv[3])

    elif cmd == "codex-perspective":
        if len(sys.argv) != 4:
            print("Usage: run_cloud_benchmark.py codex-perspective <tier> <fixture-id>")
            sys.exit(1)
        tier = get_tier("codex", sys.argv[2])
        run_codex_perspective(tier, sys.argv[3])

    elif cmd == "codex-all":
        if len(sys.argv) < 3:
            print("Usage: run_cloud_benchmark.py codex-all <tier> [--skill critic|perspective]")
            sys.exit(1)
        tier = get_tier("codex", sys.argv[2])
        skill = "critic"
        if "--skill" in sys.argv:
            skill = sys.argv[sys.argv.index("--skill") + 1]
        fixtures = ALL_CRITIC_FIXTURES if skill == "critic" else ALL_PERSPECTIVE_FIXTURES
        run_fn = run_codex_critic if skill == "critic" else run_codex_perspective
        for i, fid in enumerate(fixtures, 1):
            if result_exists("codex", tier["name"], fid, skill):
                print(f"[{i}/{len(fixtures)}] {fid} — already done, skipping")
                continue
            print(f"\n[{i}/{len(fixtures)}]")
            run_fn(tier, fid)

    elif cmd == "codex-escalate":
        skill = "critic"
        if "--skill" in sys.argv:
            skill = sys.argv[sys.argv.index("--skill") + 1]
        run_escalation("codex", skill)

    elif cmd == "score-cloud":
        score_cloud_results("critic")

    elif cmd == "score-cloud-perspective":
        score_cloud_results("perspective")

    elif cmd == "score-codex":
        score_codex_results("critic")

    elif cmd == "score-codex-perspective":
        score_codex_results("perspective")

    elif cmd == "summary":
        show_summary()

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
