#!/usr/bin/env python3
"""Local (no-API) chain-eval runner — hand-orchestrates the /a11y-workflow chain
through Ollama instead of Claude Code subagents.

WHAT THIS IS / IS NOT
  - IS: an end-to-end exercise of the FIXED instrument (plan 011) on FRESH model
    output — planner -> critic -> (audit if escalated) driven by a local model,
    each stage captured in the I9 pristine format, then scored by score_chain.py.
    Validates that M2 parse_alarms reads a real (non-hand-authored) critic table,
    that the I9 capture/zone format round-trips, and that the scorer integrates.
  - IS NOT: the paid Claude production chain. It does NOT validate I1 staging's
    peek-blocking — a local model only sees piped input, has no filesystem access,
    so peeking is impossible by construction (every stage is peek: false here).
    It also is NOT a measure of Claude's chain quality; qwen3 is a different model.

Usage:
    python3 ollama/run_chain_local.py --model qwen3:32b [fixture ...]
Default fixtures: the 3 pilot fixtures. Output: evals/suites/chain/local-qwen3/<fixture>/
"""
import os, sys, glob, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "evals", "suites", "chain"))
import ollama_a11y as oa
import score_chain as sc

PILOT = ["modal-broken-focus-trap", "video-tutorial-no-captions", "login-form-clean"]
TARGETS = os.path.join(ROOT, "evals", "suites", "chain", "targets")
OUT = os.path.join(ROOT, "evals", "suites", "chain", "local-qwen3")

OPERATOR_ZONE = (
    "\n\n<!--OPERATOR\n"
    "peek: false\n"
    "reason: |\n"
    "  Local {model} run via ollama_a11y.py. The model sees only piped input and has\n"
    "  no filesystem access, so reading the answer key is impossible by construction\n"
    "  (I1 staging is therefore moot, not validated, for this lane).\n"
    "OPERATOR-->\n"
)


def bundle_source(fixture):
    """Concatenate every file in the target dir with filename headers — what the
    scout/planner would survey."""
    d = os.path.join(TARGETS, fixture)
    parts = []
    for p in sorted(glob.glob(os.path.join(d, "*"))):
        if os.path.isfile(p):
            parts.append(f"=== {os.path.basename(p)} ===\n{open(p).read()}")
    return "\n\n".join(parts)


def write(fixture, stem, text):
    d = os.path.join(OUT, fixture)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, stem), "w") as f:
        f.write(text)


def run_fixture(fixture, model):
    print(f"\n{'='*70}\n{fixture}\n{'='*70}", flush=True)
    src = bundle_source(fixture)

    print("[1/3] planner ...", flush=True)
    plan = oa.run("planner", src, model)
    write(fixture, "planner-plan.md", plan)

    print("[2/3] critic (reviews the PLAN) ...", flush=True)
    critic_input = (f"PLAN UNDER REVIEW:\n{plan}\n\n"
                    f"=== SOURCE FILES (for reference) ===\n{src}")
    critic = oa.run("critic", critic_input, model)
    write(fixture, "critic.md", critic + OPERATOR_ZONE.format(model=model))

    alarms = sc.parse_alarms(critic)
    escalated_set = sorted(p for p, lv in alarms.items() if lv in ("MEDIUM", "HIGH"))
    escalated = bool(escalated_set)
    write(fixture, "escalated.txt", "true" if escalated else "false")
    print(f"      parsed alarms: {alarms or '{}'}", flush=True)
    print(f"      escalated: {escalated} {escalated_set}", flush=True)

    if escalated:
        print("[3/3] perspective audit ...", flush=True)
        audit_input = (f"Escalated perspectives (MEDIUM/HIGH): {', '.join(escalated_set)}\n\n"
                       f"=== SOURCE FILES ===\n{src}")
        audit = oa.run("perspective", audit_input, model)
        write(fixture, "audit.md", audit + OPERATOR_ZONE.format(model=model))
    else:
        print("[3/3] no escalation -> audit skipped", flush=True)


def main():
    args = [a for a in sys.argv[1:]]
    model = "qwen3:32b"
    if "--model" in args:
        i = args.index("--model"); model = args[i + 1]; del args[i:i + 2]
    fixtures = args or PILOT

    if oa.check_ollama() is None:
        print("ERROR: Ollama not running.", file=sys.stderr); sys.exit(1)

    for fx in fixtures:
        run_fixture(fx, model)

    print(f"\n{'#'*70}\nCaptures written under {OUT}/<fixture>/\n"
          f"Score each: python3 evals/suites/chain/score_chain.py <fixture> "
          f"{OUT}/<fixture>\n{'#'*70}", flush=True)


if __name__ == "__main__":
    main()
