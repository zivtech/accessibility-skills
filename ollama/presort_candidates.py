#!/usr/bin/env python3
"""Run the accessibility pre-sort detector locally via Ollama.

Standalone CLI: loads the pre-sort system prompt (ollama/presort-prompt.md)
verbatim, sends it plus ONE fixture's COMPONENT markdown to a local Ollama
model, validates the model's JSON candidate list against the schema the
prompt specifies, and writes the validated result to disk. NO Anthropic/
hosted API calls are made anywhere in this file.

Usage:
    python3 ollama/presort_candidates.py <fixture-id>
    python3 ollama/presort_candidates.py <fixture-id> --model qwen3.6:35b
    python3 ollama/presort_candidates.py <fixture-id> --port 11435 --temperature 0.3
    python3 ollama/presort_candidates.py <fixture-id> --out path/to/out.json

Reads ONLY evals/suites/a11y-critic/fixtures/<fixture-id>.md — the sibling
.metadata.yaml / .rubric.yaml files are the answer key for this fixture and
are never opened here.
"""

import argparse
import datetime
import json
import math
import os
import sys
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(BASE_DIR)

PRESORT_PROMPT_PATH = os.path.join(BASE_DIR, "presort-prompt.md")
FIXTURES_DIR = os.path.join(REPO_DIR, "evals", "suites", "a11y-critic", "fixtures")
RESULTS_DIR = os.path.join(REPO_DIR, "evals", "results", "qwen-presort")

# Same conservative estimate approach as ollama_a11y.py's estimate_tokens/
# RESPONSE_RESERVE (see that file for the measured-ratio history) — reused
# here only to size num_ctx generously, not as a hard overflow gate.
CHARS_PER_TOKEN_CONSERVATIVE = 3.5
RESPONSE_RESERVE = 8192
DEFAULT_NUM_CTX = 32768

VALID_SUSPECTED_CLASSES = {
    "name-role-state",
    "keyboard-operability",
    "focus-order-indicator",
    "live-region",
    "semantic-html",
    "contrast-visual",
    "other",
}
VALID_CONFIDENCE = {"high", "medium", "low"}


def estimate_tokens(text):
    return math.ceil(len(text) / CHARS_PER_TOKEN_CONSERVATIVE)


def load_presort_prompt():
    if not os.path.exists(PRESORT_PROMPT_PATH):
        sys.exit(f"ERROR: pre-sort prompt not found: {PRESORT_PROMPT_PATH}")
    with open(PRESORT_PROMPT_PATH) as f:
        return f.read()


def load_fixture_component(fixture_id):
    """Load the fixture's .md component with its in-file answer key stripped.

    Fixture .md files embed their expected findings under an
    '## Accessibility Issues' heading (below a blind cut line). Pre-sort must
    see EXACTLY what the hosted judge sees, so we reuse the runner's canonical
    strip_answer_key() rather than feeding qwen the planted-defect list. Also
    never reads the sibling .metadata.yaml / .rubric.yaml."""
    path = os.path.join(FIXTURES_DIR, f"{fixture_id}.md")
    if not os.path.exists(path):
        sys.exit(
            f"ERROR: fixture component not found: {path}\n"
            f"(expected evals/suites/a11y-critic/fixtures/{fixture_id}.md)"
        )
    with open(path) as f:
        raw = f.read()
    # Reuse the exact blind cut the hosted lane applies (anthropic is imported
    # lazily inside run_cloud_benchmark, so this import has no heavy side effect).
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from run_cloud_benchmark import strip_answer_key
    return strip_answer_key(raw)


def call_ollama(host_port, model, system_prompt, prompt_text, num_ctx, temperature):
    url = f"http://{host_port}/api/generate"
    payload = {
        "model": model,
        "system": system_prompt,
        "prompt": prompt_text,
        "stream": False,
        "options": {"num_ctx": num_ctx, "temperature": temperature},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=900) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        sys.exit(f"ERROR: Ollama request to {url} failed: {type(e).__name__}: {e}")
    return data.get("response", "")


def extract_json_object(response_text):
    """qwen3.6 may emit reasoning outside the JSON object even with
    stream=False (a separate `thinking` field covers most of that, but be
    robust to stray text around the object too). Take the first '{' through
    the last '}' and parse that."""
    start = response_text.find("{")
    end = response_text.rfind("}")
    if start == -1 or end == -1 or end < start:
        sys.exit(
            "ERROR: no JSON object found in model response.\n"
            f"--- raw response ---\n{response_text}"
        )
    candidate_json = response_text[start:end + 1]
    try:
        return json.loads(candidate_json)
    except json.JSONDecodeError as e:
        sys.exit(
            f"ERROR: could not parse JSON object from model response: {e}\n"
            f"--- extracted text ---\n{candidate_json}"
        )


def validate_candidates(parsed):
    """Validate the pre-sort output schema. Returns the validated list of
    candidates on success; exits non-zero printing exactly what failed
    otherwise. An empty candidates list is valid."""
    if not isinstance(parsed, dict):
        sys.exit(f"ERROR: schema validation failed: top-level response is not a JSON object (got {type(parsed).__name__})")

    if "candidates" not in parsed:
        sys.exit("ERROR: schema validation failed: missing top-level key 'candidates'")

    candidates = parsed["candidates"]
    if not isinstance(candidates, list):
        sys.exit(f"ERROR: schema validation failed: 'candidates' is not a list (got {type(candidates).__name__})")

    errors = []
    for i, item in enumerate(candidates):
        prefix = f"candidates[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}: not an object (got {type(item).__name__})")
            continue

        cid = item.get("id")
        if not isinstance(cid, str) or not cid:
            errors.append(f"{prefix}.id: must be a non-empty string (got {cid!r})")

        location_hint = item.get("location_hint")
        if not isinstance(location_hint, str) or not location_hint.strip():
            errors.append(f"{prefix}.location_hint: must be a non-empty string (got {location_hint!r})")

        suspected_class = item.get("suspected_class")
        if suspected_class not in VALID_SUSPECTED_CLASSES:
            errors.append(
                f"{prefix}.suspected_class: must be one of {sorted(VALID_SUSPECTED_CLASSES)} "
                f"(got {suspected_class!r})"
            )

        why = item.get("why")
        if not isinstance(why, str) or not why.strip():
            errors.append(f"{prefix}.why: must be a non-empty string (got {why!r})")

        confidence = item.get("confidence")
        if confidence not in VALID_CONFIDENCE:
            errors.append(
                f"{prefix}.confidence: must be one of {sorted(VALID_CONFIDENCE)} (got {confidence!r})"
            )

    if errors:
        sys.exit("ERROR: schema validation failed:\n" + "\n".join(f"  - {e}" for e in errors))

    return candidates


def default_out_path(fixture_id, model):
    model_tag = model.replace(":", "-")
    return os.path.join(RESULTS_DIR, f"{fixture_id}-{model_tag}.json")


def main():
    parser = argparse.ArgumentParser(
        description="Run the accessibility pre-sort detector locally via Ollama (no hosted API calls).",
    )
    parser.add_argument("fixture_id", help="Fixture id (e.g. tabs-missing-arrow-nav) — reads evals/suites/a11y-critic/fixtures/<fixture-id>.md")
    parser.add_argument("--model", default="qwen3.6:35b", help="Ollama model (default: qwen3.6:35b)")
    parser.add_argument("--port", type=int, default=11435, help="Ollama server port on localhost (default: 11435)")
    parser.add_argument("--temperature", type=float, default=0.3, help="Sampling temperature (default: 0.3)")
    parser.add_argument("--out", default=None, help="Output path (default: evals/results/qwen-presort/<fixture-id>-<model-with-colons-as-dashes>.json)")
    args = parser.parse_args()

    system_prompt = load_presort_prompt()
    fixture_text = load_fixture_component(args.fixture_id)

    num_ctx = max(DEFAULT_NUM_CTX, estimate_tokens(system_prompt + fixture_text) + RESPONSE_RESERVE)

    host_port = f"127.0.0.1:{args.port}"
    raw_response = call_ollama(host_port, args.model, system_prompt, fixture_text, num_ctx, args.temperature)
    parsed = extract_json_object(raw_response)
    candidates = validate_candidates(parsed)

    out_path = args.out or default_out_path(args.fixture_id, args.model)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    result = {
        "fixture": args.fixture_id,
        "model": args.model,
        "port": args.port,
        "temperature": args.temperature,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "num_candidates": len(candidates),
        "candidates": candidates,
    }

    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"fixture={args.fixture_id} model={args.model} num_candidates={len(candidates)} out={out_path}")


if __name__ == "__main__":
    main()
