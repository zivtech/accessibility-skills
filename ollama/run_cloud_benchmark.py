#!/usr/bin/env python3
"""Run a11y skill benchmarks on cloud models (Claude API + Codex/OpenAI + Gemini CLI).

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
    python3 ollama/run_cloud_benchmark.py codex-planner <tier> <fixture-id>
    python3 ollama/run_cloud_benchmark.py codex-planner-all <tier>

    # Gemini (requires gemini CLI auth; critic suite only — plan 007)
    python3 ollama/run_cloud_benchmark.py gemini <tier> <fixture-id>
    python3 ollama/run_cloud_benchmark.py gemini-all <tier>
    python3 ollama/run_cloud_benchmark.py gemini-escalate
    python3 ollama/run_cloud_benchmark.py gemini-dry-run   # free: prompt sizes + token estimate

    # Score all cloud results
    python3 ollama/run_cloud_benchmark.py score-cloud
    python3 ollama/run_cloud_benchmark.py score-cloud-perspective
    python3 ollama/run_cloud_benchmark.py score-gemini
    python3 ollama/run_cloud_benchmark.py score-codex-planner

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

Gemini tiers (cheapest first):
    flash           Gemini 2.5 Flash
    pro             Gemini 2.5 Pro
"""

import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(BASE_DIR)
RESULTS_DIR = os.environ.get("BENCHMARK_RESULTS_DIR", "/tmp")

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
    # 2026-06-12: ChatGPT-account codex CLI rejects gpt-5.2 (and the CLI
    # default gpt-5.3-codex) with "model is not supported"; gpt-5.5 works.
    # The 5.2 tiers are retained for the historical critic-lane results.
    {"name": "5.2", "model": "gpt-5.2", "effort": None, "label": "GPT-5.2"},
    {"name": "5.2-low", "model": "gpt-5.2", "effort": "low", "label": "GPT-5.2 (low)"},
    {"name": "5.5", "model": "gpt-5.5", "effort": None, "label": "GPT-5.5"},
    {"name": "5.5-low", "model": "gpt-5.5", "effort": "low", "label": "GPT-5.5 (low)"},
]

GEMINI_TIERS = [
    {"name": "flash", "model": "gemini-2.5-flash", "label": "Gemini 2.5 Flash"},
    {"name": "pro", "model": "gemini-2.5-pro", "label": "Gemini 2.5 Pro"},
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

# KEEP IN SYNC with run_benchmark.py (planner constants)
PLANNER_SKILL_PATH = os.path.join(REPO_DIR, ".claude", "skills", "a11y-planner", "SKILL.md")
PLANNER_FIXTURES_DIR = os.path.join(REPO_DIR, "evals", "suites", "a11y-planner", "fixtures")
PLANNER_PROMPT_PREFIX = "Plan the accessible implementation for the following component or feature. Execute all phases of the planning protocol.\n\n"

PLANNER_FIXTURES = [
    "aria-combobox-autocomplete",
    "aria-data-table-sorting",
    "aria-disclosure-widget",
    "aria-modal-form-validation",
    "aria-tab-dynamic-content",
    "keyboard-breadcrumb",
    "keyboard-button-bar",
    "keyboard-menu-dropdown",
    "keyboard-modal-focus-trap",
    "keyboard-roving-tabindex",
    "sr-article-page",
    "sr-form-field-help",
    "sr-notification-system",
    "sr-product-listing",
    "sr-search-results-live",
    "test-data-table",
    "test-form",
    "test-modal",
    "test-multi-page-audit",
    "test-simple-button",
    "visual-animated-transition",
    "visual-dark-mode",
    "visual-data-viz",
    "visual-form-validation",
    "visual-status-colors",
]


import re as _re


def write_json_atomic(path, data):
    """Write JSON to path atomically via a .tmp sibling (safe under Ctrl-C)."""
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)


def validate_fixture_id(fixture_id):
    """Exit with error if fixture_id is not safe kebab-case."""
    if not _re.fullmatch(r"[a-z0-9][a-z0-9-]*", fixture_id):
        sys.exit(f"Invalid fixture id: {fixture_id!r} (expected kebab-case)")


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


def load_planner_system_prompt():
    with open(PLANNER_SKILL_PATH) as f:
        return strip_frontmatter(f.read())


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


def platform_tiers(platform):
    return {"claude": CLAUDE_TIERS, "codex": CODEX_TIERS, "gemini": GEMINI_TIERS}[platform]


def get_tier(platform, tier_name):
    tiers = platform_tiers(platform)
    for t in tiers:
        if t["name"] == tier_name:
            return t
    names = [t["name"] for t in tiers]
    print(f"Unknown tier '{tier_name}'. Available: {', '.join(names)}")
    sys.exit(1)


def output_path(platform, tier_name, fixture_id, skill="critic"):
    prefix = {"claude": "cloud", "codex": "codex", "gemini": "gemini"}[platform]
    tag = tier_name.replace(".", "").replace("-", "")
    skill_tag = f"-{skill}" if skill != "critic" else ""
    return os.path.join(RESULTS_DIR, f"{prefix}-bench{skill_tag}-{fixture_id}-{tag}-response.json")


def result_exists(platform, tier_name, fixture_id, skill="critic"):
    path = output_path(platform, tier_name, fixture_id, skill)
    if not os.path.exists(path):
        return False
    try:
        with open(path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        print(f"WARN: corrupt result file, will re-run: {path}")
        return False
    if data.get("error"):
        return False  # error placeholder from infra failure — re-run, don't skip
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
    try:
        response = client.messages.create(**kwargs)
    except Exception as e:
        elapsed = time.time() - start
        err_msg = f"{type(e).__name__}: {e}"
        print(f"ERROR (infra, not model): {err_msg}")
        write_json_atomic(out, {
            "response": "",
            "done": False,
            "error": err_msg,
            "_benchmark": {
                "platform": "claude",
                "model": tier["model"],
                "tier": tier["name"],
                "fixture_id": fixture_id,
                "skill": skill,
                "elapsed_seconds": round(elapsed, 1),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            },
        })
        return out
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

    write_json_atomic(out, data)

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


# Critic and perspective strings must stay byte-identical to the preamble
# hardcoded before the planner lane landed — changing them invalidates
# comparability with the committed benchmark results.
PREAMBLES = {
    "critic": (
        "You are an accessibility design reviewer. "
        "Analyze ONLY the component provided below — do not read files, "
        "run commands, or use any tools. Output your complete review as text."
    ),
    "perspective": (
        "You are an accessibility design reviewer. "
        "Analyze ONLY the component provided below — do not read files, "
        "run commands, or use any tools. Output your complete review as text."
    ),
    "planner": (
        "You are an accessibility design planner. "
        "Plan ONLY from the requirements provided below — do not read files, "
        "run commands, or use any tools. Output your complete plan document as text."
    ),
}


def run_codex(tier, fixture_id, system_prompt, user_prompt, skill="critic"):
    out = output_path("codex", tier["name"], fixture_id, skill)
    msg_out = os.path.join(RESULTS_DIR, f"codex-msg-{tier['name']}-{fixture_id}-{skill}.txt")

    print(f"\n{'=' * 60}")
    print(f"CODEX | {tier['label']} | {fixture_id} ({skill})")
    print(f"Output: {out}")
    print(f"Started: {time.strftime('%H:%M:%S')}")

    full_prompt = (
        f"{PREAMBLES[skill]}\n\n"
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
    try:
        proc = subprocess.run(
            cmd,
            input=full_prompt,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except Exception as e:
        elapsed = time.time() - start
        err_msg = f"{type(e).__name__}: {e}"
        print(f"ERROR (infra, not model): {err_msg}")
        write_json_atomic(out, {
            "response": "",
            "done": False,
            "error": err_msg,
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
        })
        return out
    elapsed = time.time() - start

    response_text = ""
    if os.path.exists(msg_out):
        with open(msg_out) as f:
            response_text = f.read().strip()
        os.unlink(msg_out)

    if proc.returncode != 0 and not response_text:
        err_msg = f"codex exec failed (rc={proc.returncode})"
        print(f"ERROR (infra, not model): {err_msg}")
        if proc.stderr:
            print(f"STDERR: {proc.stderr[:500]}")
        write_json_atomic(out, {
            "response": "",
            "done": False,
            "error": err_msg,
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
        })
        return out

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

    write_json_atomic(out, data)

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


def run_codex_planner(tier, fixture_id):
    system_prompt = load_planner_system_prompt()
    fixture_content = load_fixture(fixture_id, PLANNER_FIXTURES_DIR)
    user_prompt = PLANNER_PROMPT_PREFIX + fixture_content
    return run_codex(tier, fixture_id, system_prompt, user_prompt, "planner")


# ── Gemini CLI ──────────────────────────────────────────────────────────
# Transport per plan 007 amendment (2026-06-12): the authenticated `gemini`
# CLI, mirroring the codex lane — not the google-genai SDK. Calls run from a
# neutral temp cwd with --skip-trust so the CLI does NOT load this repo's
# .agents skills or workspace context into the model prompt (lane isolation;
# measured CLI harness overhead ~18.7K input tokens/call, recorded per call
# from the JSON stats block).


GEMINI_NEUTRAL_CWD = os.path.join(tempfile.gettempdir(), "gemini-bench-neutral")


def require_gemini_cli():
    if not shutil.which("gemini"):
        sys.exit("gemini CLI not found on PATH — install and authenticate it first.")


def run_gemini(tier, fixture_id, system_prompt, user_prompt, skill="critic"):
    out = output_path("gemini", tier["name"], fixture_id, skill)

    print(f"\n{'=' * 60}")
    print(f"GEMINI | {tier['label']} | {fixture_id} ({skill})")
    print(f"Output: {out}")
    print(f"Started: {time.strftime('%H:%M:%S')}")

    # Preamble adapted for the gemini CLI agent harness: probe runs showed the
    # agent attempting to SAVE the review to a file (blocked, then hallucinated
    # success) instead of answering. The headless contract must be explicit.
    full_prompt = (
        "You are an accessibility design reviewer running HEADLESS with no "
        "filesystem and no tools. Do NOT read files, run commands, create "
        "files, or save anything — file writes are blocked, and a review "
        "saved to a file is a FAILED review. Analyze ONLY the component "
        "provided below. Your final chat response must BE the complete "
        "review document itself, in full — not a summary of it, and not a "
        "statement about where it was saved.\n\n"
        f"## Investigation Protocol\n\n{system_prompt}\n\n"
        f"## Task\n\n{user_prompt}"
    )

    os.makedirs(GEMINI_NEUTRAL_CWD, exist_ok=True)
    cmd = [
        "gemini",
        "-m", tier["model"],
        "-o", "json",
        "--approval-mode", "default",
        "--skip-trust",
        "-p", full_prompt,
    ]

    def error_placeholder(err_msg, elapsed):
        print(f"ERROR (infra, not model): {err_msg}")
        write_json_atomic(out, {
            "response": "",
            "done": False,
            "error": err_msg,
            "_benchmark": {
                "platform": "gemini",
                "model": tier["model"],
                "tier": tier["name"],
                "fixture_id": fixture_id,
                "skill": skill,
                "elapsed_seconds": round(elapsed, 1),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            },
        })

    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=GEMINI_NEUTRAL_CWD,
            capture_output=True,
            text=True,
            timeout=900,
        )
    except Exception as e:
        error_placeholder(f"{type(e).__name__}: {e}", time.time() - start)
        return out
    elapsed = time.time() - start

    response_text = ""
    usage = {}
    if proc.stdout.strip():
        try:
            payload = json.loads(proc.stdout)
            response_text = (payload.get("response") or "").strip()
            models = (payload.get("stats") or {}).get("models") or {}
            if models:
                served_model, mstats = next(iter(models.items()))
                tokens = mstats.get("tokens", {})
                usage = {
                    "served_model": served_model,
                    "input_tokens": tokens.get("input"),
                    "output_tokens": tokens.get("candidates"),
                    "thought_tokens": tokens.get("thoughts"),
                }
        except json.JSONDecodeError:
            pass

    if proc.returncode != 0 and not response_text:
        if proc.stderr:
            print(f"STDERR: {proc.stderr[:500]}")
        error_placeholder(f"gemini CLI failed (rc={proc.returncode})", elapsed)
        return out

    data = {
        "response": response_text,
        "done": True,
        "_benchmark": {
            "platform": "gemini",
            "model": tier["model"],
            "tier": tier["name"],
            "fixture_id": fixture_id,
            "skill": skill,
            "elapsed_seconds": round(elapsed, 1),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            **usage,
        },
    }

    write_json_atomic(out, data)

    print(f"Done: {time.strftime('%H:%M:%S')} ({elapsed:.1f}s, {len(response_text)} chars)")
    return out


def run_gemini_critic(tier, fixture_id):
    system_prompt = load_critic_system_prompt()
    fixture_content = load_fixture(fixture_id)
    user_prompt = CRITIC_PROMPT_PREFIX + fixture_content
    return run_gemini(tier, fixture_id, system_prompt, user_prompt, "critic")


GEMINI_CLI_OVERHEAD_TOKENS = 18700  # measured: CLI harness prompt, neutral cwd


def gemini_dry_run():
    """FREE: print per-fixture prompt sizes + token estimate. No network."""
    system_prompt = load_critic_system_prompt()
    sys_chars = len(system_prompt)
    total_est = 0
    print(f"{'fixture':50s} {'prompt chars':>13s} {'est input tok':>14s}")
    for fid in ALL_CRITIC_FIXTURES:
        user_prompt = CRITIC_PROMPT_PREFIX + load_fixture(fid)
        chars = sys_chars + len(user_prompt)
        est = chars // 4 + GEMINI_CLI_OVERHEAD_TOKENS
        total_est += est
        print(f"{fid:50s} {chars:>13,d} {est:>14,d}")
    print(f"\n{len(ALL_CRITIC_FIXTURES)} fixtures, flash-tier input estimate: ~{total_est:,d} tokens")
    print("(output typically 2-6K tokens/fixture; gemini CLI auth = quota, not per-token billing)")


# ── Scoring ─────────────────────────────────────────────────────────────


def score_cloud_results(skill="critic"):
    if skill == "critic":
        score_script = os.path.join(BASE_DIR, "score_output.py")
        pattern = os.path.join(RESULTS_DIR, "cloud-bench-*-response.json")
        fixtures_dir = FIXTURES_DIR
    else:
        score_script = os.path.join(BASE_DIR, "score_perspective.py")
        pattern = os.path.join(RESULTS_DIR, "cloud-bench-perspective-*-response.json")
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
        pattern = os.path.join(RESULTS_DIR, "codex-bench-*-response.json")
        fixtures_dir = FIXTURES_DIR
    elif skill == "planner":
        score_script = os.path.join(BASE_DIR, "score_planner.py")
        pattern = os.path.join(RESULTS_DIR, "codex-bench-planner-*-response.json")
        fixtures_dir = PLANNER_FIXTURES_DIR
    else:
        score_script = os.path.join(BASE_DIR, "score_perspective.py")
        pattern = os.path.join(RESULTS_DIR, "codex-bench-perspective-*-response.json")
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
        # score_planner.py emits PASS / NEEDS REVIEW; the other scorers
        # emit PASS / FAIL / WARN.
        bucket = results.setdefault(
            tier, {"pass": 0, "fail": 0, "warn": 0, "needs_review": 0}
        )
        if "Status: PASS" in proc.stdout:
            bucket["pass"] += 1
        elif "Status: NEEDS REVIEW" in proc.stdout:
            bucket["needs_review"] += 1
        elif "Status: FAIL" in proc.stdout:
            bucket["fail"] += 1
        elif "Status: WARN" in proc.stdout:
            bucket["warn"] += 1

    return results


def score_gemini_results(skill="critic"):
    if skill != "critic":
        sys.exit("gemini lane supports the critic suite only (plan 007 scope)")
    score_script = os.path.join(BASE_DIR, "score_output.py")
    pattern = os.path.join(RESULTS_DIR, "gemini-bench-*-response.json")
    fixtures_dir = FIXTURES_DIR

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
    """Score all results for a tier; return (failed, not_run, errored).

    errored: result file exists but has a non-empty "error" field (infra failure).
    These are excluded from scorer runs and reported separately.
    """
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
    errored = []
    for fixture_id in all_fixtures:
        out = output_path(platform, tier_name, fixture_id, skill)
        if not os.path.exists(out):
            not_run.append(fixture_id)
            continue
        metadata = os.path.join(fixtures_dir, f"{fixture_id}.metadata.yaml")
        if not os.path.exists(metadata):
            not_run.append(fixture_id)
            continue

        # Check for infra-error placeholder before running scorer
        try:
            with open(out) as f:
                result_data = json.load(f)
            if result_data.get("error"):
                errored.append(fixture_id)
                continue
        except (json.JSONDecodeError, OSError):
            errored.append(fixture_id)
            continue

        proc = subprocess.run(
            [sys.executable, score_script, out, metadata],
            capture_output=True, text=True,
        )
        if "Status: PASS" not in proc.stdout:
            failed.append(fixture_id)

    return failed, not_run, errored


def run_escalation(platform, skill="critic"):
    tiers = platform_tiers(platform)
    all_fixtures = ALL_CRITIC_FIXTURES if skill == "critic" else ALL_PERSPECTIVE_FIXTURES

    if platform == "claude":
        run_fn = run_claude_critic if skill == "critic" else run_claude_perspective
    elif platform == "gemini":
        if skill != "critic":
            sys.exit("gemini lane supports the critic suite only (plan 007 scope)")
        run_fn = run_gemini_critic
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

        failed, not_run, errored = get_failed_fixtures(platform, tier["name"], skill)
        # Only count fixtures that were actually in this tier's scope
        ran_this_tier = [f for f in remaining if f not in not_run]
        passed = len(ran_this_tier) - len([f for f in failed if f in remaining]) - len([f for f in errored if f in remaining])

        tier_results.append({
            "tier": tier["name"],
            "label": tier["label"],
            "ran": len(ran_this_tier),
            "passed": passed,
            "failed": len(failed),
            "errored": len(errored),
            "not_run": len(not_run),
        })

        print(f"\n{'─' * 60}")
        print(f"Tier {tier['label']}: {passed} PASS / {len(failed)} FAIL / {len(errored)} INFRA-ERROR / {len(not_run)} NOT_RUN")

        # Escalate failures, not-run, and infra errors
        remaining = failed + errored + [f for f in not_run if f in remaining]
        if not remaining:
            print(f"\nAll fixtures passed at {tier['label']} tier!")
            break

    print(f"\n{'=' * 60}")
    print(f"ESCALATION SUMMARY ({platform}, {skill})")
    print(f"{'=' * 60}")
    for r in tier_results:
        pct = r["passed"] / max(r["passed"] + r["failed"], 1) * 100
        infra_err_str = f", {r['errored']} infra-error" if r.get("errored") else ""
        print(f"  {r['label']}: ran {r['ran']}, {r['passed']} pass ({pct:.0f}%), {r['failed']} fail{infra_err_str}")

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
        "gemini": {"prefix": "gemini", "tiers": GEMINI_TIERS},
    }

    for platform, info in platforms.items():
        for skill in ["critic", "perspective"]:
            skill_tag = f"-{skill}" if skill != "critic" else ""
            pattern = os.path.join(RESULTS_DIR, f"{info['prefix']}-bench{skill_tag}-*-response.json")
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
        if not os.environ.get("ANTHROPIC_API_KEY"):
            sys.exit("ANTHROPIC_API_KEY is not set — refusing to start a paid run.")
        if len(sys.argv) != 4:
            print("Usage: run_cloud_benchmark.py claude <tier> <fixture-id>")
            sys.exit(1)
        tier = get_tier("claude", sys.argv[2])
        validate_fixture_id(sys.argv[3])
        run_claude_critic(tier, sys.argv[3])

    elif cmd == "claude-perspective":
        if not os.environ.get("ANTHROPIC_API_KEY"):
            sys.exit("ANTHROPIC_API_KEY is not set — refusing to start a paid run.")
        if len(sys.argv) != 4:
            print("Usage: run_cloud_benchmark.py claude-perspective <tier> <fixture-id>")
            sys.exit(1)
        tier = get_tier("claude", sys.argv[2])
        validate_fixture_id(sys.argv[3])
        run_claude_perspective(tier, sys.argv[3])

    elif cmd == "claude-all":
        if not os.environ.get("ANTHROPIC_API_KEY"):
            sys.exit("ANTHROPIC_API_KEY is not set — refusing to start a paid run.")
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
        if not os.environ.get("ANTHROPIC_API_KEY"):
            sys.exit("ANTHROPIC_API_KEY is not set — refusing to start a paid run.")
        skill = "critic"
        if "--skill" in sys.argv:
            skill = sys.argv[sys.argv.index("--skill") + 1]
        run_escalation("claude", skill)

    elif cmd == "codex":
        if len(sys.argv) != 4:
            print("Usage: run_cloud_benchmark.py codex <tier> <fixture-id>")
            sys.exit(1)
        tier = get_tier("codex", sys.argv[2])
        validate_fixture_id(sys.argv[3])
        run_codex_critic(tier, sys.argv[3])

    elif cmd == "codex-perspective":
        if len(sys.argv) != 4:
            print("Usage: run_cloud_benchmark.py codex-perspective <tier> <fixture-id>")
            sys.exit(1)
        tier = get_tier("codex", sys.argv[2])
        validate_fixture_id(sys.argv[3])
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

    elif cmd == "codex-planner":
        if len(sys.argv) != 4:
            print("Usage: run_cloud_benchmark.py codex-planner <tier> <fixture-id>")
            sys.exit(1)
        tier = get_tier("codex", sys.argv[2])
        validate_fixture_id(sys.argv[3])
        run_codex_planner(tier, sys.argv[3])

    elif cmd == "codex-planner-all":
        if len(sys.argv) < 3:
            print("Usage: run_cloud_benchmark.py codex-planner-all <tier>")
            sys.exit(1)
        tier = get_tier("codex", sys.argv[2])
        for i, fid in enumerate(PLANNER_FIXTURES, 1):
            if result_exists("codex", tier["name"], fid, "planner"):
                print(f"[{i}/{len(PLANNER_FIXTURES)}] {fid} — already done, skipping")
                continue
            print(f"\n[{i}/{len(PLANNER_FIXTURES)}]")
            run_codex_planner(tier, fid)

    elif cmd == "gemini":
        require_gemini_cli()
        if len(sys.argv) != 4:
            print("Usage: run_cloud_benchmark.py gemini <tier> <fixture-id>")
            sys.exit(1)
        tier = get_tier("gemini", sys.argv[2])
        validate_fixture_id(sys.argv[3])
        run_gemini_critic(tier, sys.argv[3])

    elif cmd == "gemini-all":
        require_gemini_cli()
        if len(sys.argv) < 3:
            print("Usage: run_cloud_benchmark.py gemini-all <tier>")
            sys.exit(1)
        tier = get_tier("gemini", sys.argv[2])
        for i, fid in enumerate(ALL_CRITIC_FIXTURES, 1):
            if result_exists("gemini", tier["name"], fid, "critic"):
                print(f"[{i}/{len(ALL_CRITIC_FIXTURES)}] {fid} — already done, skipping")
                continue
            print(f"\n[{i}/{len(ALL_CRITIC_FIXTURES)}]")
            run_gemini_critic(tier, fid)

    elif cmd == "gemini-escalate":
        require_gemini_cli()
        run_escalation("gemini", "critic")

    elif cmd == "gemini-dry-run":
        gemini_dry_run()

    elif cmd == "score-gemini":
        score_gemini_results("critic")

    elif cmd == "score-cloud":
        score_cloud_results("critic")

    elif cmd == "score-cloud-perspective":
        score_cloud_results("perspective")

    elif cmd == "score-codex":
        score_codex_results("critic")

    elif cmd == "score-codex-perspective":
        score_codex_results("perspective")

    elif cmd == "score-codex-planner":
        score_codex_results("planner")

    elif cmd == "summary":
        show_summary()

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
