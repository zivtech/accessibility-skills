#!/usr/bin/env python3
"""Run any LOCAL Ollama model as an a11y-critic on the 33-fixture baseline set,
via the repo's validated local path (ollama_a11y.run), blind-cut, retry-on-empty.
Writes one response file per fixture named by MODEL SLUG so several models can be
benchmarked side by side for an ensemble/majority-vote analysis.

Usage: python3 ollama/run_local_critic.py <model> [fixture-id ...]
Output: evals/results/local-critic/<model-slug>/<fixture>.json
Targets a dedicated Ollama on :11435 (run one model at a time — big models swap).
"""
import os
os.environ.setdefault("OLLAMA_HOST", "127.0.0.1:11435")
import sys, json, datetime  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ollama_a11y as oa  # noqa: E402
from run_cloud_benchmark import strip_answer_key  # noqa: E402
from run_gemini_agy_critic import BASELINE_33  # noqa: E402

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BASE)
FIX = os.path.join(REPO, "evals/suites/a11y-critic/fixtures")
MAX_ATTEMPTS = 3


def slug(model):
    return model.replace(":", "-").replace("/", "-").replace(".", "-")


def run_one(fixture, model, out_dir):
    comp = strip_answer_key(open(os.path.join(FIX, fixture + ".md")).read())
    resp, attempts = "", 0
    for attempt in range(1, MAX_ATTEMPTS + 1):
        attempts = attempt
        try:
            resp = oa.run("critic", comp, model) or ""
        except Exception as e:  # noqa: BLE001
            print(f"RETRY {fixture} attempt {attempt}: {type(e).__name__}: {e}", flush=True)
            resp = ""
        if resp.strip():
            break
        print(f"EMPTY {fixture} attempt {attempt} — retrying", flush=True)
    if not resp.strip():
        print(f"FAIL {fixture}: empty after {MAX_ATTEMPTS} attempts", flush=True)
        return
    os.makedirs(out_dir, exist_ok=True)
    json.dump({"response": resp, "model": model, "attempts": attempts,
               "generated_at": datetime.datetime.now(datetime.UTC).isoformat()},
              open(os.path.join(out_dir, fixture + ".json"), "w"), indent=2)
    print(f"OK {fixture} chars={len(resp)} attempts={attempts}", flush=True)


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: run_local_critic.py <model> [fixture-id ...]")
    model = sys.argv[1]
    fixtures = sys.argv[2:] or BASELINE_33
    out_dir = os.path.join(REPO, "evals/results/local-critic", slug(model))
    print(f"{model} local critic -> {out_dir} ({len(fixtures)} fixtures) on {os.environ['OLLAMA_HOST']}", flush=True)
    for f in fixtures:
        run_one(f, model, out_dir)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
