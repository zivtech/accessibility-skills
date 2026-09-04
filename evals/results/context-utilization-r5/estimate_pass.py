"""R5.2 pre-pass: assemble every production prompt via run_benchmark's own
functions and report the guard's estimate. No server, no re-implementation."""
import os, sys, json
sys.path.insert(0, os.path.abspath("ollama"))
import run_benchmark as rb

SUITES = {}

# critic: system = SKILL.md (frontmatter stripped); prompt = PROMPT_PREFIX + blinded fixture
critic_ids = sorted(f[:-3] for f in os.listdir(rb.FIXTURES_DIR) if f.endswith(".md"))
SUITES["critic"] = (rb.load_system_prompt(),
                    [(i, rb.PROMPT_PREFIX + rb.load_fixture(i)) for i in critic_ids])

# planner (plain) and planner-federal (crosswalk appended to system)
SUITES["planner"] = (rb.load_planner_system_prompt(),
                     [(i, rb.PLANNER_PROMPT_PREFIX + rb.load_fixture(i, rb.PLANNER_FIXTURES_DIR))
                      for i in rb.PLANNER_FIXTURES])
SUITES["planner-federal"] = (rb.load_planner_federal_system_prompt(),
                             [(i, rb.PLANNER_PROMPT_PREFIX + rb.load_fixture(i, rb.PLANNER_FIXTURES_DIR))
                              for i in rb.PLANNER_FIXTURES])

# bugreport
SUITES["bugreport"] = (rb.strip_frontmatter(open(rb.BUGREPORT_SKILL_PATH).read()),
                       [(i, rb.BUGREPORT_PROMPT_PREFIX + rb.load_fixture(i, rb.BUGREPORT_FIXTURES_DIR))
                        for i in rb.BUGREPORT_FIXTURES])

# perspective
persp_ids = sorted(f[:-3] for f in os.listdir(rb.PERSPECTIVE_FIXTURES_DIR)
                   if f.endswith(".md") and not f.endswith(".metadata.md"))
SUITES["perspective"] = (rb.load_perspective_system_prompt(),
                         [(i, rb.build_escalation_prompt(i)) for i in persp_ids])

out = {}
for name, (system, items) in SUITES.items():
    sys_est = rb.estimate_tokens(system)
    rows = sorted(((rb.estimate_tokens(system) + rb.estimate_tokens(p), fid)
                   for fid, p in items), reverse=True)
    out[name] = {
        "n_fixtures": len(rows),
        "system_est": sys_est,
        "system_chars": len(system),
        "min_est": rows[-1][0], "max_est": rows[0][0],
        "largest_fixture": rows[0][1], "smallest_fixture": rows[-1][1],
    }
    print(f"{name:18s} n={len(rows):3d}  sys_est={sys_est:6d}  range={rows[-1][0]}-{rows[0][0]}  "
          f"largest={rows[0][1]}")
json.dump(out, open(sys.argv[1], "w"), indent=2)
