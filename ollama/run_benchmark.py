#!/usr/bin/env python3
"""Run a11y skill benchmarks on local Ollama models.

Usage:
    python3 ollama/run_benchmark.py ollama-clean       # CLEAN fixtures, all models
    python3 ollama/run_benchmark.py ollama-bugs        # HAS-BUGS fixtures, all models
    python3 ollama/run_benchmark.py single <model> <fixture-id>  # One fixture, one model
    python3 ollama/run_benchmark.py score-all          # Score all response files in /tmp
    python3 ollama/run_benchmark.py perspective <model> <fixture-id>  # Perspective-audit single fixture
    python3 ollama/run_benchmark.py perspective-pilot [model]  # Pilot set of perspective fixtures
"""

import json
import os
import sys
import time
import urllib.request

BASE_DIR = os.path.dirname(__file__)
FIXTURES_DIR = os.path.join(BASE_DIR, "..", "evals", "suites", "a11y-critic", "fixtures")
SKILL_PATH = os.path.join(BASE_DIR, "..", ".claude", "skills", "a11y-critic", "SKILL.md")

PERSPECTIVE_FIXTURES_DIR = os.path.join(BASE_DIR, "..", "evals", "suites", "perspectives", "fixtures")
PERSPECTIVE_SKILL_PATH = os.path.join(BASE_DIR, "..", ".claude", "skills", "perspective-audit", "SKILL.md")
PERSPECTIVE_REFS = [
    os.path.join(BASE_DIR, "..", ".claude", "skills", "perspective-audit", "references", "perspectives.md"),
    os.path.join(BASE_DIR, "..", ".claude", "skills", "perspective-audit", "references", "arrm-perspective-mapping.md"),
]

PLANNER_FIXTURES_DIR = os.path.join(BASE_DIR, "..", "evals", "suites", "a11y-planner", "fixtures")
PLANNER_SKILL_PATH = os.path.join(BASE_DIR, "..", ".claude", "skills", "a11y-planner", "SKILL.md")

PROMPT_PREFIX = "Review the following React component for accessibility design issues. Execute all phases of the investigation protocol.\n\n"
PLANNER_PROMPT_PREFIX = "Plan the accessible implementation for the following component or feature. Execute all phases of the planning protocol.\n\n"

PLANNER_FIXTURES = [
    "aria-modal-form-validation",
    "keyboard-roving-tabindex",
]

PERSPECTIVE_PILOT_FIXTURES = [
    "animated-onboarding-flow",
    "checkout-form-broken-errors",
    "color-only-status-indicators",
    "modal-broken-focus-trap",
    "dense-admin-jargon",
    "login-form-clean",
    "article-page-clean",
]

OLLAMA_URL = "http://localhost:11434/api/generate"

OLLAMA_MODELS = ["llama3.3:70b", "qwen3:32b", "deepseek-r1:70b", "qwen3.5:27b"]
SMALL_MODELS = ["qwen3.5:latest"]  # 6.6 GB — test as lightweight tier
HAS_BUGS_FIXTURES = [
    "form-validation-missing-aria-describedby",
    "tabs-missing-arrow-nav",
    "toast-notification-no-role",
]
CLEAN_FIXTURES = [
    "button-skip-link-clean",
    "interactive-dropdown-clean",
    "modal-complete-clean",
    "search-results-dynamic-clean",
]


def strip_frontmatter(content):
    if content.startswith("---"):
        end = content.index("---", 3)
        return content[end + 3:].strip()
    return content


def load_system_prompt():
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
    path = os.path.join(d, f"{fixture_id}.md")
    with open(path) as f:
        return f.read()


def build_escalation_prompt(fixture_id):
    """Build perspective-audit user prompt with escalation list from fixture metadata."""
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
        escalation_block = "## Escalated Perspectives\n\nAll perspectives at LOW — this is a CLEAN baseline. Produce PASS verdict with no CRITICAL/MAJOR findings."

    return (
        "Run the perspective audit on the following component. "
        "The escalated perspectives are listed below.\n\n"
        f"{escalation_block}\n\n"
        f"## Component Under Review\n\n{fixture_content}"
    )


def run_ollama(model, fixture_id, system_prompt):
    fixture_content = load_fixture(fixture_id)
    prompt = PROMPT_PREFIX + fixture_content

    payload = {
        "model": model,
        "system": system_prompt,
        "prompt": prompt,
        "stream": False,
        "options": {"num_ctx": 16384, "temperature": 0.3},
    }

    model_tag = model.split(":")[0].replace(".", "").replace("-", "")
    out_path = f"/tmp/ollama-bench-{fixture_id}-{model_tag}-response.json"

    print(f"\n{'='*60}")
    print(f"Model: {model} | Fixture: {fixture_id}")
    print(f"Output: {out_path}")
    print(f"Started: {time.strftime('%H:%M:%S')}")

    start = time.time()
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=900) as resp:
        data = json.loads(resp.read())

    elapsed = time.time() - start
    data["_benchmark"] = {
        "model": model,
        "fixture_id": fixture_id,
        "elapsed_seconds": round(elapsed, 1),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)

    resp_len = len(data.get("response", ""))
    print(f"Done: {time.strftime('%H:%M:%S')} ({elapsed:.0f}s, {resp_len} chars)")
    return out_path


def load_planner_system_prompt():
    with open(PLANNER_SKILL_PATH) as f:
        return strip_frontmatter(f.read())


def run_planner(model, fixture_id, system_prompt):
    fixture_content = load_fixture(fixture_id, PLANNER_FIXTURES_DIR)
    prompt = PLANNER_PROMPT_PREFIX + fixture_content

    payload = {
        "model": model,
        "system": system_prompt,
        "prompt": prompt,
        "stream": False,
        "options": {"num_ctx": 32768, "temperature": 0.3},
    }

    model_tag = model.split(":")[0].replace(".", "").replace("-", "")
    out_path = f"/tmp/ollama-planner-{fixture_id}-{model_tag}-response.json"

    print(f"\n{'='*60}")
    print(f"PLANNER | Model: {model} | Fixture: {fixture_id}")
    print(f"Output: {out_path}")
    print(f"Started: {time.strftime('%H:%M:%S')}")

    start = time.time()
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=1200) as resp:
        data = json.loads(resp.read())

    elapsed = time.time() - start
    data["_benchmark"] = {
        "model": model,
        "fixture_id": fixture_id,
        "skill": "a11y-planner",
        "elapsed_seconds": round(elapsed, 1),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)

    resp_len = len(data.get("response", ""))
    print(f"Done: {time.strftime('%H:%M:%S')} ({elapsed:.0f}s, {resp_len} chars)")
    return out_path


def run_perspective(model, fixture_id, system_prompt):
    prompt = build_escalation_prompt(fixture_id)

    payload = {
        "model": model,
        "system": system_prompt,
        "prompt": prompt,
        "stream": False,
        "options": {"num_ctx": 32768, "temperature": 0.3},
    }

    model_tag = model.split(":")[0].replace(".", "").replace("-", "")
    out_path = f"/tmp/ollama-perspective-{fixture_id}-{model_tag}-response.json"

    print(f"\n{'='*60}")
    print(f"PERSPECTIVE | Model: {model} | Fixture: {fixture_id}")
    print(f"Output: {out_path}")
    print(f"Started: {time.strftime('%H:%M:%S')}")

    start = time.time()
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=1200) as resp:
        data = json.loads(resp.read())

    elapsed = time.time() - start
    data["_benchmark"] = {
        "model": model,
        "fixture_id": fixture_id,
        "skill": "perspective-audit",
        "elapsed_seconds": round(elapsed, 1),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)

    resp_len = len(data.get("response", ""))
    print(f"Done: {time.strftime('%H:%M:%S')} ({elapsed:.0f}s, {resp_len} chars)")
    return out_path


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "ollama-clean":
        system_prompt = load_system_prompt()
        for fixture_id in CLEAN_FIXTURES:
            for model in OLLAMA_MODELS:
                run_ollama(model, fixture_id, system_prompt)

    elif cmd == "ollama-bugs":
        system_prompt = load_system_prompt()
        for fixture_id in HAS_BUGS_FIXTURES:
            for model in OLLAMA_MODELS:
                run_ollama(model, fixture_id, system_prompt)

    elif cmd == "single":
        if len(sys.argv) != 4:
            print("Usage: run_benchmark.py single <model> <fixture-id>")
            sys.exit(1)
        model, fixture_id = sys.argv[2], sys.argv[3]
        system_prompt = load_system_prompt()
        run_ollama(model, fixture_id, system_prompt)

    elif cmd == "planner":
        if len(sys.argv) != 4:
            print("Usage: run_benchmark.py planner <model> <fixture-id>")
            sys.exit(1)
        model, fixture_id = sys.argv[2], sys.argv[3]
        system_prompt = load_planner_system_prompt()
        run_planner(model, fixture_id, system_prompt)

    elif cmd == "planner-all":
        model = sys.argv[2] if len(sys.argv) > 2 else None
        models = [model] if model else OLLAMA_MODELS
        system_prompt = load_planner_system_prompt()
        for fixture_id in PLANNER_FIXTURES:
            for m in models:
                run_planner(m, fixture_id, system_prompt)

    elif cmd == "perspective":
        if len(sys.argv) != 4:
            print("Usage: run_benchmark.py perspective <model> <fixture-id>")
            sys.exit(1)
        model, fixture_id = sys.argv[2], sys.argv[3]
        system_prompt = load_perspective_system_prompt()
        run_perspective(model, fixture_id, system_prompt)

    elif cmd == "perspective-pilot":
        model = sys.argv[2] if len(sys.argv) > 2 else "qwen3:32b"
        system_prompt = load_perspective_system_prompt()
        for fixture_id in PERSPECTIVE_PILOT_FIXTURES:
            run_perspective(model, fixture_id, system_prompt)

    elif cmd == "score-all":
        import glob
        import subprocess
        score_script = os.path.join(os.path.dirname(__file__), "score_output.py")
        responses = sorted(glob.glob("/tmp/ollama-bench-*-response.json"))
        responses += sorted(glob.glob("/tmp/ollama-fullproto-*-response.json"))
        for resp in responses:
            basename = os.path.basename(resp)
            parts = basename.replace("ollama-bench-", "").replace("-response.json", "")
            model_tag = parts.split("-")[-1]
            fixture_id = parts.rsplit(f"-{model_tag}", 1)[0]
            metadata = os.path.join(FIXTURES_DIR, f"{fixture_id}.metadata.yaml")
            if os.path.exists(metadata):
                print(f"\n{'='*60}")
                print(f"Scoring: {fixture_id} ({model_tag})")
                print(f"{'='*60}")
                subprocess.run([sys.executable, score_script, resp, metadata])
            else:
                print(f"SKIP: No metadata for {fixture_id}")

    elif cmd == "small-test":
        system_prompt = load_system_prompt()
        for model in SMALL_MODELS:
            for fixture_id in CLEAN_FIXTURES + HAS_BUGS_FIXTURES:
                run_ollama(model, fixture_id, system_prompt)

    elif cmd == "score-perspective":
        import glob
        import subprocess
        score_script = os.path.join(os.path.dirname(__file__), "score_perspective.py")
        if not os.path.exists(score_script):
            print(f"ERROR: {score_script} not found")
            sys.exit(1)
        responses = sorted(glob.glob("/tmp/ollama-perspective-*-response.json"))
        for resp in responses:
            basename = os.path.basename(resp)
            parts = basename.replace("ollama-perspective-", "").replace("-response.json", "")
            model_tag = parts.split("-")[-1]
            fixture_id = parts.rsplit(f"-{model_tag}", 1)[0]
            metadata = os.path.join(PERSPECTIVE_FIXTURES_DIR, f"{fixture_id}.metadata.yaml")
            if os.path.exists(metadata):
                print(f"\n{'='*60}")
                print(f"Scoring perspective: {fixture_id} ({model_tag})")
                print(f"{'='*60}")
                subprocess.run([sys.executable, score_script, resp, metadata])
            else:
                print(f"SKIP: No metadata for {fixture_id}")

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
