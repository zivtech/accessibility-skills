#!/usr/bin/env python3
"""Run a11y skills locally via Ollama.

Usage:
    # Review a component file with a11y-critic
    python3 ollama/ollama_a11y.py critic path/to/component.jsx

    # Review with a specific model
    python3 ollama/ollama_a11y.py critic path/to/component.jsx --model qwen3:32b

    # Plan accessibility for a requirements description
    python3 ollama/ollama_a11y.py planner path/to/requirements.md

    # Review from stdin
    cat component.jsx | python3 ollama/ollama_a11y.py critic -

Supported skills: critic, planner, perspective
Default model: llama3.3:70b (Tier 1)
"""

import argparse
import json
import os
import sys
import time
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3.3:70b"

SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", ".claude", "skills")

SKILL_PROMPTS = {
    "critic": "Review the following component for accessibility design issues. Execute all phases of the investigation protocol.\n\n",
    "planner": "Plan the accessible implementation for the following component or feature. Execute all phases of the planning protocol.\n\n",
    "perspective": "Run the perspective audit on the following component. The escalated perspectives are listed in the input.\n\n",
}

SKILL_REFS = {
    "perspective": [
        "perspective-audit/references/perspectives.md",
        "perspective-audit/references/arrm-perspective-mapping.md",
    ],
}


def load_skill_prompt(skill_name: str) -> str:
    skill_dir_name = "perspective-audit" if skill_name == "perspective" else f"a11y-{skill_name}"
    skill_path = os.path.join(SKILLS_DIR, skill_dir_name, "SKILL.md")
    if not os.path.exists(skill_path):
        print(f"ERROR: Skill file not found: {skill_path}", file=sys.stderr)
        sys.exit(1)

    with open(skill_path) as f:
        content = f.read()

    if content.startswith("---"):
        end = content.index("---", 3)
        content = content[end + 3:].strip()

    for ref_path in SKILL_REFS.get(skill_name, []):
        full_path = os.path.join(SKILLS_DIR, ref_path)
        if os.path.exists(full_path):
            with open(full_path) as f:
                content += "\n\n---\n\n" + f.read()

    return content


def load_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path) as f:
        return f.read()


def check_ollama():
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
        return [m["name"] for m in data.get("models", [])]
    except Exception:
        return None


def run(skill: str, input_text: str, model: str, num_ctx: int = 32768) -> str:
    system_prompt = load_skill_prompt(skill)
    user_prompt = SKILL_PROMPTS[skill] + input_text

    payload = {
        "model": model,
        "system": system_prompt,
        "prompt": user_prompt,
        "stream": False,
        "options": {"num_ctx": num_ctx, "temperature": 0.3},
    }

    print(f"Model: {model}", file=sys.stderr)
    print(f"Skill: a11y-{skill}", file=sys.stderr)
    print(f"Input: {len(input_text)} chars", file=sys.stderr)
    print(f"Context: {num_ctx} tokens", file=sys.stderr)
    print(f"Running...", file=sys.stderr)

    start = time.time()
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(req, timeout=900) as resp:
        data = json.loads(resp.read())

    elapsed = time.time() - start
    response = data.get("response", "")

    tokens_generated = data.get("eval_count", 0)
    print(f"Done in {elapsed:.0f}s ({tokens_generated} tokens, {len(response)} chars)", file=sys.stderr)

    return response


def main():
    parser = argparse.ArgumentParser(
        description="Run a11y skills locally via Ollama",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("skill", choices=["critic", "planner", "perspective"], help="Which a11y skill to run")
    parser.add_argument("input", help="Path to component/requirements file, or - for stdin")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Ollama model (default: {DEFAULT_MODEL})")
    parser.add_argument("--ctx", type=int, default=32768, help="Context window size (default: 32768)")
    parser.add_argument("--json", action="store_true", help="Output as JSON with metadata")
    args = parser.parse_args()

    models = check_ollama()
    if models is None:
        print("ERROR: Ollama not running. Start with: ollama serve", file=sys.stderr)
        sys.exit(1)

    if args.model not in models:
        print(f"ERROR: Model '{args.model}' not available. Installed: {', '.join(models)}", file=sys.stderr)
        sys.exit(1)

    input_text = load_input(args.input)
    if not input_text.strip():
        print("ERROR: Empty input", file=sys.stderr)
        sys.exit(1)

    response = run(args.skill, input_text, args.model, args.ctx)

    if args.json:
        out = {
            "skill": f"a11y-{args.skill}",
            "model": args.model,
            "response": response,
        }
        print(json.dumps(out, indent=2))
    else:
        print(response)


if __name__ == "__main__":
    main()
