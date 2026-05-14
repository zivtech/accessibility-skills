#!/usr/bin/env python3
"""Run a11y-critic benchmark on local Ollama models.

Usage:
    python3 ollama/run_benchmark.py ollama-clean       # CLEAN fixtures, both models (~50 min)
    python3 ollama/run_benchmark.py ollama-bugs        # HAS-BUGS fixtures, both models (~35 min)
    python3 ollama/run_benchmark.py single <model> <fixture-id>  # One fixture, one model
    python3 ollama/run_benchmark.py score-all          # Score all response files in /tmp
"""

import json
import os
import sys
import time
import urllib.request

FIXTURES_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "evals",
    "suites",
    "a11y-critic",
    "fixtures",
)
SKILL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    ".claude",
    "skills",
    "a11y-critic",
    "SKILL.md",
)
PROMPT_PREFIX = "Review the following React component for accessibility design issues. Execute all phases of the investigation protocol.\n\n"

OLLAMA_URL = "http://localhost:11434/api/generate"

OLLAMA_MODELS = ["llama3.3:70b", "qwen3:32b"]
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


def load_system_prompt():
    with open(SKILL_PATH) as f:
        content = f.read()
    if content.startswith("---"):
        end = content.index("---", 3)
        content = content[end + 3:].strip()
    return content


def load_fixture(fixture_id):
    path = os.path.join(FIXTURES_DIR, f"{fixture_id}.md")
    with open(path) as f:
        return f.read()


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

    model_tag = model.split(":")[0].replace(".", "")
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


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    system_prompt = load_system_prompt()

    if cmd == "ollama-clean":
        for fixture_id in CLEAN_FIXTURES:
            for model in OLLAMA_MODELS:
                run_ollama(model, fixture_id, system_prompt)

    elif cmd == "ollama-bugs":
        for fixture_id in HAS_BUGS_FIXTURES:
            for model in OLLAMA_MODELS:
                run_ollama(model, fixture_id, system_prompt)

    elif cmd == "single":
        if len(sys.argv) != 4:
            print("Usage: run_benchmark.py single <model> <fixture-id>")
            sys.exit(1)
        model, fixture_id = sys.argv[2], sys.argv[3]
        run_ollama(model, fixture_id, system_prompt)

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

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
