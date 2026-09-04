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

    # Aggregate finished audit evidence into an evaluation report
    python3 ollama/ollama_a11y.py evalreport path/to/evidence.md

Supported skills: critic, planner, perspective, bugreport, evalreport
(evalreport's system prompt is docs/a11y-evaluation-report-contract.md —
the report contract is the skill under test)
Default model: qwen3.6:35b
"""

import argparse
import json
import math
import os
import sys
import time
import urllib.request

# --- Context-overflow guard (context-utilization plan Phase 0.2/0.3, 2026-08-24) ---
# Twin copy in ollama/run_benchmark.py (this file: ollama_a11y.py) — keep both
# in sync by hand; these are standalone scripts, not a shared package.
CHARS_PER_TOKEN_CONSERVATIVE = 3.5  # F15 (gate re-review round 4, 2026-08-25):
# real measured ratio — critic protocol (a11y-critic SKILL.md, frontmatter
# stripped, 60,373 chars) / prompt_eval_count on this lane's own
# num_predict=1 probe corpus (2026-08-25) = 4.23 chars/token (qwen3.6:35b) /
# 4.36 chars/token (qwen3:32b) — supersedes the earlier stale "16,157
# tokens / 3.74 chars/token" figure (wrong on both counts). 3.5 stays
# unchanged, still deliberately below both measured ratios — the safe
# direction — but by more than previously documented; see
# estimate_tokens()'s docstring for what that overestimate is in practice.
RESPONSE_RESERVE = 8192  # thinking models: reasoning tokens share num_ctx


def estimate_tokens(text):
    """Conservative token estimate. CHARS_PER_TOKEN_CONSERVATIVE (3.5) was
    documented as a ~7% overestimate against one earlier measured ratio;
    measured against the context-utilization-phase3 lane's real
    num_predict=1 probes (2026-08-25 — gate F14 part 3, docs/plans/
    2026-08-25-context-utilization-phase3-gate-review.md "Final gate
    ruling") it overestimates by 22-30%, not ~7%: protocol alone, est
    17,480 vs measured 14,276 (qwen3.6:35b) / 13,853 (qwen3:32b) tokens =
    1.224x-1.262x; protocol + tabs-missing-arrow-nav fixture, est 19,004
    vs measured 15,167 / 14,649 = 1.253x-1.297x.

    The asymmetry this creates, stated plainly: a prompt that DOES get
    sent has MORE real headroom than the ~7% figure implies (measured
    margins are looser than believed) — but the guard's pass/fail decision
    runs on this inflated estimate, so it refuses real prompts that would
    have fit more often than a 7%-based mental model predicts (guard
    margins are tighter). CHARS_PER_TOKEN_CONSERVATIVE stays 3.5 — this is
    a documentation-accuracy fix, not a retune. Twin copy: keep in sync
    with run_benchmark.py's estimate_tokens by hand."""
    return math.ceil(len(text) / CHARS_PER_TOKEN_CONSERVATIVE)


def context_overflow(system_text, prompt_text, num_ctx, declared_context_length=None):
    """Client-side primary gate (F6/F7): does estimated prompt + response
    reserve exceed num_ctx? Returns (overflow: bool, estimated_tokens: int).

    F13 fast-follow (gate re-review, 2026-08-25): num_ctx alone is the
    REQUESTED window, not what Ollama will actually allocate. Proven live
    the same day — qwen3:32b requested at 49,152 was silently clamped
    server-side to its declared 40,960, and a 45,176-token prompt lost
    54.7% of itself to truncation while this exact guard, checking only the
    requested value, would have waved it through. declared_context_length
    (fetch_declared_context_length, below) is the model's real ceiling from
    /api/tags; when supplied, the guard compares against
    min(num_ctx, declared_context_length) instead of num_ctx alone — the
    estimate formula and RESPONSE_RESERVE are otherwise unchanged. None
    (the default) preserves the exact old behavior for any caller that
    hasn't been updated to pass it. Twin copy: keep in sync with
    run_benchmark.py's context_overflow by hand."""
    estimated = estimate_tokens((system_text or "") + (prompt_text or ""))
    effective_ctx = num_ctx if declared_context_length is None else min(num_ctx, declared_context_length)
    return estimated + RESPONSE_RESERVE > effective_ctx, estimated


class GuardConfigError(Exception):
    """fetch_declared_context_length's own failures (F13) — /api/tags
    unreachable, or the requested model missing from it, or present but
    carrying no context_length field. Always raised, never silently
    swallowed into a default ceiling."""


_DECLARED_CONTEXT_LENGTH_CACHE = {}  # F13: memoized per model for the process lifetime


def _tag_variants(model):
    """R5 follow-up (2026-08-27): /api/tags ALWAYS reports a tagged name
    ("laguna-xs-2.1:latest"), while callers routinely invoke the bare name
    ("laguna-xs-2.1") and every *_CTX map is keyed on whatever string the
    caller typed. Those are two namespaces, and before this they diverged
    silently: `laguna-xs-2.1` — the exact string with 12 committed critic
    rows AND a CRITIC_CTX entry — raised GuardConfigError, while
    `laguna-xs-2.1:latest` resolved. Try both spellings of the implicit
    ":latest" tag before declaring a model missing. Only ":latest" is
    implied; "qwen3.5:27b" and "qwen3.5:latest" are DIFFERENT models (9.7B
    vs a 27B that is not installed) and are never conflated here."""
    if ":" not in model:
        return [model, model + ":latest"]
    base, _, tag = model.rpartition(":")
    return [model, base] if tag == "latest" else [model]


def _fetch_context_length_from_show(model, show_url):
    """R5 follow-up (2026-08-27): some models list in /api/tags with a null
    details.context_length — gemma4:31b and gemma4:26b do, and both are
    mapped in CRITIC_CTX, so the F13 raise hard-blocked two mapped models
    from running any lane at all. /api/show carries the GGUF metadata the
    tags summary omits, as model_info["<arch>.context_length"].

    This is NOT a fallback guess and NOT a default: verified 2026-08-27 that
    /api/show agrees EXACTLY with /api/tags on every model that reports both
    (qwen3:32b 40960, qwen3.6:35b 262144, llama3.3:70b 131072, and the same
    262144 for gemma4 where tags is null). Same number, fuller source.
    Returns None on any failure so the caller still raises."""
    try:
        req = urllib.request.Request(
            show_url, data=json.dumps({"model": model}).encode(),
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            info = json.loads(resp.read()).get("model_info") or {}
    except Exception:
        return None
    hits = [v for k, v in info.items()
            if k.endswith(".context_length") and isinstance(v, int) and v > 0]
    return min(hits) if hits else None  # min: the safe direction if ever ambiguous


def ctx_for(model, mapping, default):
    """num_ctx lookup that tolerates the implicit-":latest" spelling gap
    (_tag_variants). Without it a map entry written bare misses a tagged
    invocation and the run silently falls to the _DEFAULT."""
    for variant in _tag_variants(model):
        if variant in mapping:
            return mapping[variant]
    return default


def fetch_declared_context_length(model, *, tags_url=None, show_url=None):
    """F13 fast-follow: the model's real context_length ceiling, from
    Ollama's own /api/tags (models[].details.context_length — confirmed
    live, 2026-08-25: qwen3:32b -> 40960, qwen3.6:35b -> 262144). Cached per
    model. Fails loud on any of: /api/tags unreachable, model not listed, or
    listed with no context_length field — never a silent default. Twin copy
    of run_benchmark.py's function of the same name; reuses this file's own
    OLLAMA_TAGS_URL rather than a duplicated host-derivation.

    R5 follow-up (2026-08-27): resolves the implicit ":latest" tag
    (_tag_variants) and falls back to /api/show's GGUF model_info when
    /api/tags reports a null context_length (_fetch_context_length_from_show).
    Still fails loud when neither source has a value — never a silent
    default."""
    if model in _DECLARED_CONTEXT_LENGTH_CACHE:
        return _DECLARED_CONTEXT_LENGTH_CACHE[model]
    url = tags_url or OLLAMA_TAGS_URL
    show = show_url or url.replace("/api/tags", "/api/show")
    try:
        with urllib.request.urlopen(urllib.request.Request(url), timeout=10) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        raise GuardConfigError(f"F13 guard: cannot fetch declared context_length for {model!r} — "
                                f"/api/tags unreachable at {url}: {e}") from e
    listed = {entry.get("name"): entry for entry in data.get("models", [])}
    matched_name = next((v for v in _tag_variants(model) if v in listed), None)
    if matched_name is None:
        raise GuardConfigError(f"F13 guard: model {model!r} not found in /api/tags at {url} "
                                f"(installed: {sorted(n for n in listed if n)})")
    declared = (listed[matched_name].get("details") or {}).get("context_length")
    if declared is None:
        declared = _fetch_context_length_from_show(matched_name, show)
    if declared is None:
        raise GuardConfigError(f"F13 guard: model {model!r} found in /api/tags but neither its "
                                f"details nor /api/show at {show} carry a context_length — "
                                "cannot verify the real ceiling.")
    _DECLARED_CONTEXT_LENGTH_CACHE[model] = declared
    return declared



# Honor the standard OLLAMA_HOST env var so a run can target a specific server,
# e.g. a native Metal server on :11435 vs the CPU-only OrbStack container that
# may hold :11434. Default preserves prior behavior. Accepts "host:port" or URL.
_OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "127.0.0.1:11434").rstrip("/")
if not _OLLAMA_HOST.startswith(("http://", "https://")):
    _OLLAMA_HOST = "http://" + _OLLAMA_HOST
OLLAMA_URL = _OLLAMA_HOST + "/api/generate"
OLLAMA_TAGS_URL = _OLLAMA_HOST + "/api/tags"
DEFAULT_MODEL = "qwen3.6:35b"

SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", ".claude", "skills")
DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")

SKILL_PROMPTS = {
    "critic": "Review the following component for accessibility design issues. Execute all phases of the investigation protocol.\n\n",
    "planner": "Plan the accessible implementation for the following component or feature. Execute all phases of the planning protocol.\n\n",
    "perspective": "Run the perspective audit on the following component. The escalated perspectives are listed in the input.\n\n",
    "bugreport": "Convert the following raw accessibility finding(s) into bug report(s) ready to file as GitHub Issue(s), following the bug-reporting skill exactly. Where the input genuinely lacks a value, follow the skill's guidance on absent data instead of inventing one. Return only the finished report(s) in the skill's Markdown template.\n\n",
    "evalreport": "Aggregate the following finished evaluation evidence into an Accessibility Evaluation Report, following the A11y Evaluation Report Contract exactly. Report only what the evidence contains. Return only the finished report in Markdown.\n\n",
}

# R5.4 (2026-08-27, R5 decision memo §3 last row): the wrapper's flat 32,768
# default is correct for critic/perspective/bugreport/evalreport and WRONG for
# planner -- the a11y-planner protocol alone measures 18,950-19,468 tokens
# (num_predict=1 probes, 2026-08-27), so 32,768 leaves under the 8,192 reserve
# once a real fixture is appended, and the guard here only WARNS (it still
# generates, best effort) rather than refusing as run_benchmark.py does.
#
# HAND-SYNCED with run_benchmark.py's *_CTX_DEFAULT constants per that file's
# standalone-scripts convention (run_benchmark.py:33-34) -- same drift risk the
# twin guard code already carries. If you change one, change the other.
# Probe receipts: evals/results/context-utilization-r5/num-ctx-probe-receipts.md
SKILL_NUM_CTX = {
    "critic": 32768,
    "planner": 40960,
    "perspective": 32768,
    "bugreport": 32768,
    "evalreport": 32768,
}
SKILL_NUM_CTX_DEFAULT = 32768

# Skills whose system prompt is a contract document rather than a SKILL.md
# (prompt-only repo: the contract IS the skill under test).
DOC_SKILLS = {
    "evalreport": "a11y-evaluation-report-contract.md",
}

SKILL_REFS = {
    "perspective": [
        "perspective-audit/references/perspectives.md",
        "perspective-audit/references/arrm-perspective-mapping.md",
    ],
}


def load_skill_prompt(skill_name: str) -> str:
    if skill_name in DOC_SKILLS:
        skill_path = os.path.join(DOCS_DIR, DOC_SKILLS[skill_name])
    else:
        special_dirs = {"perspective": "perspective-audit", "bugreport": "bug-reporting"}
        skill_dir_name = special_dirs.get(skill_name, f"a11y-{skill_name}")
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
        req = urllib.request.Request(OLLAMA_TAGS_URL)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
        return [m["name"] for m in data.get("models", [])]
    except Exception:
        return None


class GuardedResponse(str):
    """A str subclass that also carries whether the client-side
    context-overflow gate (Phase 0.2/0.3) fired for this generation.
    Backward-compatible with existing callers that treat run()'s return
    value as a plain string — ollama/run_chain_local.py and
    ollama/run_critic_control.py both do `x = oa.run(...)` and then use x as
    a string (f-strings, file.write(), regex parsing). GuardedResponse IS a
    str (isinstance, hashing, string methods, json.dumps all behave
    identically), so those callers are unaffected. This file's own main()
    reads the .overflowed attribute on the object run() returns directly to
    decide the exit code."""
    overflowed = False
    declared_context_length = None  # F13: the model's real ceiling, once fetched (see run())


def run(skill: str, input_text: str, model: str, num_ctx: int = None) -> str:
    """Returns the response text as a GuardedResponse (str + .overflowed).
    num_ctx defaults to the skill's entry in SKILL_NUM_CTX when not given.
    overflowed=True means the client-side estimate found the prompt too big
    for num_ctx + RESPONSE_RESERVE — generation still runs (best effort;
    output may be silently front-truncated by Ollama), but the caller should
    surface the failure."""
    # R5.4: num_ctx=None means "size it from the skill" (SKILL_NUM_CTX). An
    # explicit value still wins, so every existing caller that passes one is
    # unaffected; callers that relied on the old flat 32,768 default now get
    # the per-skill value -- which is the fix, not a regression (run_chain_local
    # .py's planner step was the under-budgeted caller).
    if num_ctx is None:
        num_ctx = SKILL_NUM_CTX.get(skill, SKILL_NUM_CTX_DEFAULT)
    system_prompt = load_skill_prompt(skill)
    user_prompt = SKILL_PROMPTS[skill] + input_text

    # F13: fetch before the guard so the guard can clamp to whichever of
    # num_ctx/declared_context_length is smaller, not the requested value alone.
    declared_context_length = fetch_declared_context_length(model)
    overflow, estimated = context_overflow(system_prompt, user_prompt, num_ctx, declared_context_length)

    print(f"Model: {model}", file=sys.stderr)
    print(f"Skill: a11y-{skill}", file=sys.stderr)
    print(f"Input: {len(input_text)} chars", file=sys.stderr)
    # Served prompt size ledger line, every run (context-utilization plan
    # Phase 0 task 0.3): chars + estimated tokens + num_ctx (+ F13: the
    # model's actual declared ceiling, so a requested-vs-declared mismatch
    # is visible even on a row that doesn't overflow).
    prompt_chars = len(system_prompt) + len(user_prompt)
    print(
        f"Prompt: {prompt_chars} chars (~{estimated} estimated tokens) | "
        f"num_ctx: {num_ctx} | declared_context_length: {declared_context_length}",
        file=sys.stderr,
    )

    if overflow:
        effective_ctx = min(num_ctx, declared_context_length)
        print(
            "\n" + "!" * 60 + "\n"
            f"CONTEXT OVERFLOW: estimated {estimated} prompt tokens + "
            f"{RESPONSE_RESERVE} reserve > effective ceiling {effective_ctx} "
            f"(requested num_ctx={num_ctx}, declared_context_length={declared_context_length}) "
            "— output may be silently front-truncated; raise --num-ctx or curate the input\n"
            + "!" * 60,
            file=sys.stderr,
        )

    print(f"Running...", file=sys.stderr)

    payload = {
        "model": model,
        "system": system_prompt,
        "prompt": user_prompt,
        "stream": False,
        "options": {"num_ctx": num_ctx, "temperature": 0.3},
    }

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

    result = GuardedResponse(response)
    result.overflowed = overflow
    result.declared_context_length = declared_context_length  # F13
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Run a11y skills locally via Ollama",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("skill", choices=["critic", "planner", "perspective", "bugreport", "evalreport"], help="Which a11y skill to run")
    parser.add_argument("input", help="Path to component/requirements file, or - for stdin")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Ollama model (default: {DEFAULT_MODEL})")
    parser.add_argument(
        "--ctx", "--num-ctx", dest="ctx", type=int, default=None,
        help="Context window size (default: per-skill, see SKILL_NUM_CTX: "
             "planner=40960, others=32768)",
    )
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

    # Context-overflow guard (Phase 0.2/0.3): output is emitted above either
    # way (best-effort — it may be silently front-truncated); the failure
    # still needs to be surfaced to scripts/CI via the exit code.
    if getattr(response, "overflowed", False):
        sys.exit(2)


if __name__ == "__main__":
    main()
