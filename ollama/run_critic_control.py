#!/usr/bin/env python3
"""Control for the plan-vs-component confound (plan 011 local lane).

The chain runner fed the critic a PLAN ("PLAN UNDER REVIEW: ...") and qwen3
emitted prose instead of the SKILL-mandated | Perspective | Alarm | table 3/3.
This control holds model/SKILL/content constant and changes ONLY the framing:
the critic reviews the COMPONENT directly (as a11y-critic SKILL.md intends).

  - table appears now  -> the no-table result was largely PLAN-FRAMING
  - still prose        -> qwen3 genuinely won't follow the table mandate

Run: OLLAMA_HOST=127.0.0.1:11435 python3 /tmp/run_critic_control.py
"""
import os, sys, glob

ROOT = "/Users/AlexUA_1/claude/a11y-meta-skills"
sys.path.insert(0, os.path.join(ROOT, "ollama"))
sys.path.insert(0, os.path.join(ROOT, "evals", "suites", "chain"))
import ollama_a11y as oa
import score_chain as sc

TARGETS = os.path.join(ROOT, "evals/suites/chain/targets")
OUT = os.path.join(ROOT, "evals/suites/chain/local-qwen3-control")
PILOT = ["modal-broken-focus-trap", "video-tutorial-no-captions", "login-form-clean"]
MODEL = "qwen3:32b"
ZONE = ("\n\n<!--OPERATOR\npeek: false\nreason: |\n  Control: critic reviews the COMPONENT "
        "directly (no plan). Local qwen3 via :11435, no filesystem access.\nOPERATOR-->\n")


def bundle_source(fx):
    d = os.path.join(TARGETS, fx)
    return "\n\n".join(f"=== {os.path.basename(p)} ===\n{open(p).read()}"
                       for p in sorted(glob.glob(os.path.join(d, "*"))) if os.path.isfile(p))


print(f"routing -> {oa.OLLAMA_URL}", flush=True)
summary = []
for fx in PILOT:
    print(f"\n{'='*60}\n{fx}  (critic reviews COMPONENT directly)\n{'='*60}", flush=True)
    src = bundle_source(fx)
    critic = oa.run("critic", src, MODEL)
    d = os.path.join(OUT, fx)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "critic.md"), "w") as f:
        f.write(critic + ZONE)
    alarms = sc.parse_alarms(critic)
    escalated = sorted(p for p, lv in alarms.items() if lv in ("MEDIUM", "HIGH"))
    with open(os.path.join(d, "escalated.txt"), "w") as f:
        f.write("true" if escalated else "false")
    has_pipe_level = any("|" in ln and any(t in ln.upper() for t in ("LOW", "MEDIUM", "HIGH"))
                         for ln in critic.split("\n"))
    print(f"parsed alarms: {alarms or '{}'}", flush=True)
    print(f"escalated: {bool(escalated)} {escalated}", flush=True)
    print(f"pipe-row-with-level present: {has_pipe_level}", flush=True)
    summary.append((fx, alarms, has_pipe_level))

print(f"\n{'#'*60}\nCONTROL SUMMARY (component-input vs the plan-input run)\n{'#'*60}", flush=True)
for fx, alarms, tbl in summary:
    print(f"  {fx:32} table={tbl}  alarms={alarms or '{}'}", flush=True)
