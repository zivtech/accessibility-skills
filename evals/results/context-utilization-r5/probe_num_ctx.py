"""R5.2 — num_predict=1 probe receipts, per (model x suite), against the
assembled PRODUCTION prompt. Prompt assembly is imported from run_benchmark,
never re-implemented (Phase 0.4 rigor bar). Probes bypass the client-side
guard deliberately: the point is to measure what the guard estimates.
"""
import json, os, sys, time, urllib.request
sys.path.insert(0, os.path.abspath("ollama"))
import run_benchmark as rb

PROBE_CTX = 40960  # generous for every suite here; also qwen3:32b's declared ceiling
MODELS = ["qwen3.6:35b", "qwen3:32b", "gemma4:31b"]
OUT = sys.argv[1]


def suites():
    s = {}
    critic_ids = sorted(f[:-3] for f in os.listdir(rb.FIXTURES_DIR) if f.endswith(".md"))
    s["critic"] = dict(
        system=rb.load_system_prompt(),
        protocol=rb.PROMPT_PREFIX,
        items={i: rb.PROMPT_PREFIX + rb.load_fixture(i) for i in critic_ids})
    s["planner"] = dict(
        system=rb.load_planner_system_prompt(),
        protocol=rb.PLANNER_PROMPT_PREFIX,
        items={i: rb.PLANNER_PROMPT_PREFIX + rb.load_fixture(i, rb.PLANNER_FIXTURES_DIR)
               for i in rb.PLANNER_FIXTURES})
    s["planner-federal"] = dict(
        system=rb.load_planner_federal_system_prompt(),
        protocol=rb.PLANNER_PROMPT_PREFIX,
        items={i: rb.PLANNER_PROMPT_PREFIX + rb.load_fixture(i, rb.PLANNER_FIXTURES_DIR)
               for i in rb.PLANNER_FIXTURES})
    s["bugreport"] = dict(
        system=rb.strip_frontmatter(open(rb.BUGREPORT_SKILL_PATH).read()),
        protocol=rb.BUGREPORT_PROMPT_PREFIX,
        items={i: rb.BUGREPORT_PROMPT_PREFIX + rb.load_fixture(i, rb.BUGREPORT_FIXTURES_DIR)
               for i in rb.BUGREPORT_FIXTURES})
    pids = sorted(f[:-3] for f in os.listdir(rb.PERSPECTIVE_FIXTURES_DIR) if f.endswith(".md"))
    s["perspective"] = dict(
        system=rb.load_perspective_system_prompt(),
        protocol="",
        items={i: rb.build_escalation_prompt(i) for i in pids})
    return s


def probe(model, system, prompt):
    payload = {"model": model, "system": system, "prompt": prompt, "stream": False,
               "options": {"num_ctx": PROBE_CTX, "num_predict": 1, "temperature": 0}}
    req = urllib.request.Request(rb.OLLAMA_URL, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=1800) as r:
        d = json.loads(r.read())
    return {"prompt_eval_count": d.get("prompt_eval_count"),
            "eval_count": d.get("eval_count"),
            "done_reason": d.get("done_reason"),
            "elapsed_seconds": round(time.time() - t0, 1)}


S = suites()
rows = []
for model in MODELS:
    for name, spec in S.items():
        # governing fixture = largest by the guard's own estimator
        largest = max(spec["items"], key=lambda i: rb.estimate_tokens(spec["items"][i]))
        for point, text in (("protocol", spec["protocol"]), (f"largest:{largest}", spec["items"][largest])):
            est = rb.estimate_tokens(spec["system"]) + rb.estimate_tokens(text)
            rec = {"model": model, "suite": name, "point": point, "probe_num_ctx": PROBE_CTX,
                   "estimated_prompt_tokens": est}
            try:
                rec.update(probe(model, spec["system"], text))
                m = rec.get("prompt_eval_count")
                rec["est_over_measured"] = round(est / m, 4) if m else None
            except Exception as e:
                rec["error"] = f"{type(e).__name__}: {e}"
            rows.append(rec)
            print(json.dumps(rec), flush=True)
            json.dump(rows, open(OUT, "w"), indent=2)
print("DONE", len(rows))
