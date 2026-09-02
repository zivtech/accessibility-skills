#!/usr/bin/env python3
"""Validate fixture files and runner registries for the accessibility-skills eval suites.

Checks:
1. YAML parse: all *.metadata.yaml and *.rubric.yaml files parse without error
2. Triplet completeness: each suite's fixture ids are complete across .md / .metadata.yaml / .rubric.yaml
3. Registry coverage: hardcoded fixture lists in runner scripts match the filesystem

Suite discovery is filesystem-derived: every directory under evals/suites/ is a
triplet suite unless listed in NON_TRIPLET_SUITES, and every triplet suite must
map to a runner registry (REGISTRY_LISTS or the inline critic/perspective/
planner checks) — omission is opt-out, never opt-in (#25).

Exit 1 if any check fails; exit 0 if all pass.

Run from repo root:
    python3 scripts/validate_fixtures.py
"""

import os
import sys
import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUITES_DIR = os.path.join(REPO, "evals", "suites")
SMOKE_DIR = os.path.join(SUITES_DIR, "smoke")

# Suite directories that are NOT fixture triplets (.md + .metadata.yaml +
# .rubric.yaml). Everything else under evals/suites/ is validated by default,
# so a new suite is covered unless someone opts it out here (#25: the old
# hardcoded tuples silently skipped acr-reporting for three lanes).
NON_TRIPLET_SUITES = {
    "baseline-scan",       # rule-list scan rig: fixtures/ but no rubrics
    "chain",               # multi-stage chain eval, own scorer + targets
    "smoke",               # scorer smoke responses, not fixtures
    "webwright-benchmark", # task directories, not triplets
}

# Triplet suites whose runner registry is a single hardcoded list in
# ollama/run_benchmark.py. The critic / perspective / planner suites are
# checked against both runners inline in check_registries().
REGISTRY_LISTS = {
    "bug-reporting": "BUGREPORT_FIXTURES",
    "evaluation-report": "EVALREPORT_FIXTURES",
    "a11y-test-operation-evidence": "OPEVIDENCE_FIXTURES",
    "acr-reporting": "ACR_FIXTURES",
}
INLINE_REGISTRY_SUITES = {"a11y-critic", "perspectives", "a11y-planner"}


def triplet_suites():
    """Every directory under evals/suites/ except the explicit non-triplet set."""
    return sorted(
        d for d in os.listdir(SUITES_DIR)
        if os.path.isdir(os.path.join(SUITES_DIR, d)) and d not in NON_TRIPLET_SUITES
    )


def yaml_parse_dir(directory, patterns=(".metadata.yaml", ".rubric.yaml")):
    """Parse all matching YAML files under directory. Returns (count, errors)."""
    errors = []
    count = 0
    if not os.path.isdir(directory):
        return count, errors
    for root, _dirs, files in os.walk(directory):
        for fname in sorted(files):
            if any(fname.endswith(p) for p in patterns):
                path = os.path.join(root, fname)
                count += 1
                try:
                    with open(path) as f:
                        yaml.safe_load(f)
                except Exception as e:
                    errors.append(f"  PARSE ERROR: {path}: {e}")
    return count, errors


def basenames_without_ext(directory, extension):
    """Return set of basenames (without the given extension) for files in directory."""
    if not os.path.isdir(directory):
        return set()
    return {
        f[: -len(extension)]
        for f in os.listdir(directory)
        if f.endswith(extension)
    }


def check_triplets(suite_name, fixtures_dir, rubrics_dir):
    """Compare fixture .md, .metadata.yaml, and .rubric.yaml sets. Returns list of problems."""
    md_ids = basenames_without_ext(fixtures_dir, ".md")
    meta_ids = basenames_without_ext(fixtures_dir, ".metadata.yaml")
    rubric_ids = basenames_without_ext(rubrics_dir, ".rubric.yaml")

    problems = []
    for fid in sorted(md_ids - meta_ids):
        problems.append(f"  {suite_name}: {fid}.md has no .metadata.yaml")
    for fid in sorted(meta_ids - md_ids):
        problems.append(f"  {suite_name}: {fid}.metadata.yaml has no .md")
    for fid in sorted(md_ids - rubric_ids):
        problems.append(f"  {suite_name}: {fid}.md has no .rubric.yaml")
    for fid in sorted(rubric_ids - md_ids):
        problems.append(f"  {suite_name}: {fid}.rubric.yaml has no .md")

    count = len(md_ids & meta_ids & rubric_ids)
    return count, problems


def check_calibration_pairs(calibration_dir):
    """Check .md / .metadata.yaml pairs in calibration dir (no rubrics). Returns problems."""
    md_ids = basenames_without_ext(calibration_dir, ".md")
    meta_ids = basenames_without_ext(calibration_dir, ".metadata.yaml")

    problems = []
    for fid in sorted(md_ids - meta_ids):
        problems.append(f"  perspectives/calibration: {fid}.md has no .metadata.yaml")
    for fid in sorted(meta_ids - md_ids):
        problems.append(f"  perspectives/calibration: {fid}.metadata.yaml has no .md")
    return len(md_ids & meta_ids), problems


def fs_fixture_ids(fixtures_dir):
    """Return sorted list of fixture ids (basenames of .md files) in a directory."""
    if not os.path.isdir(fixtures_dir):
        return []
    return sorted(f[:-3] for f in os.listdir(fixtures_dir) if f.endswith(".md"))


def registry_check_count():
    """3 critic/perspective/planner runner-vs-fs + 3 cross-runner + one per REGISTRY_LISTS suite."""
    mapped = [s for s in triplet_suites() if s not in INLINE_REGISTRY_SUITES]
    return 6 + len(mapped)


def check_registries():
    """Compare hardcoded runner fixture lists against filesystem. Returns list of problems."""
    sys.path.insert(0, os.path.join(REPO, "ollama"))
    import run_benchmark
    import run_cloud_benchmark

    critic_dir = os.path.join(SUITES_DIR, "a11y-critic", "fixtures")
    perspective_dir = os.path.join(SUITES_DIR, "perspectives", "fixtures")
    planner_dir = os.path.join(SUITES_DIR, "a11y-planner", "fixtures")

    fs_critic = set(fs_fixture_ids(critic_dir))
    fs_perspective = set(fs_fixture_ids(perspective_dir))
    fs_planner = set(fs_fixture_ids(planner_dir))
    rb_critic = set(run_benchmark.ALL_CRITIC_FIXTURES)
    rb_perspective = set(run_benchmark.ALL_PERSPECTIVE_FIXTURES)
    rb_planner = set(run_benchmark.PLANNER_FIXTURES)
    rcb_critic = set(run_cloud_benchmark.ALL_CRITIC_FIXTURES)
    rcb_perspective = set(run_cloud_benchmark.ALL_PERSPECTIVE_FIXTURES)

    problems = []

    # run_benchmark vs filesystem
    for fid in sorted(rb_critic - fs_critic):
        problems.append(f"  run_benchmark.ALL_CRITIC_FIXTURES: {fid} not on filesystem")
    for fid in sorted(fs_critic - rb_critic):
        problems.append(f"  run_benchmark.ALL_CRITIC_FIXTURES: filesystem has {fid} not in list")

    for fid in sorted(rb_perspective - fs_perspective):
        problems.append(f"  run_benchmark.ALL_PERSPECTIVE_FIXTURES: {fid} not on filesystem")
    for fid in sorted(fs_perspective - rb_perspective):
        problems.append(f"  run_benchmark.ALL_PERSPECTIVE_FIXTURES: filesystem has {fid} not in list")

    # planner registry vs filesystem
    for fid in sorted(rb_planner - fs_planner):
        problems.append(f"  run_benchmark.PLANNER_FIXTURES: {fid} not on filesystem")
    for fid in sorted(fs_planner - rb_planner):
        problems.append(f"  run_benchmark.PLANNER_FIXTURES: filesystem has {fid} not in list")

    # single-list registries vs filesystem (both directions), one per
    # REGISTRY_LISTS entry; a triplet suite with no mapping is itself an error
    for suite in triplet_suites():
        if suite in INLINE_REGISTRY_SUITES:
            continue
        attr = REGISTRY_LISTS.get(suite)
        if attr is None:
            problems.append(
                f"  {suite}: triplet suite has no registry mapping in "
                "validate_fixtures.REGISTRY_LISTS (add it, or list the suite in NON_TRIPLET_SUITES)"
            )
            continue
        fs_ids = set(fs_fixture_ids(os.path.join(SUITES_DIR, suite, "fixtures")))
        rb_ids = set(getattr(run_benchmark, attr))
        for fid in sorted(rb_ids - fs_ids):
            problems.append(f"  run_benchmark.{attr}: {fid} not on filesystem")
        for fid in sorted(fs_ids - rb_ids):
            problems.append(f"  run_benchmark.{attr}: filesystem has {fid} not in list")

    # run_cloud_benchmark vs run_benchmark (the two in-code copies)
    for fid in sorted(rcb_critic - rb_critic):
        problems.append(f"  run_cloud_benchmark vs run_benchmark critic: {fid} in cloud only")
    for fid in sorted(rb_critic - rcb_critic):
        problems.append(f"  run_cloud_benchmark vs run_benchmark critic: {fid} in local only")

    for fid in sorted(rcb_perspective - rb_perspective):
        problems.append(f"  run_cloud_benchmark vs run_benchmark perspective: {fid} in cloud only")
    for fid in sorted(rb_perspective - rcb_perspective):
        problems.append(f"  run_cloud_benchmark vs run_benchmark perspective: {fid} in local only")

    # planner lists between the two runners ("KEEP IN SYNC" comment is not a
    # check — step 11a drifted here for a day before this guard existed)
    rcb_planner = set(run_cloud_benchmark.PLANNER_FIXTURES)
    for fid in sorted(rcb_planner - rb_planner):
        problems.append(f"  run_cloud_benchmark vs run_benchmark planner: {fid} in cloud only")
    for fid in sorted(rb_planner - rcb_planner):
        problems.append(f"  run_cloud_benchmark vs run_benchmark planner: {fid} in local only")

    return problems


def main():
    errors = []

    # 1. YAML parse: all suites (excluding smoke/)
    total_yaml = 0
    yaml_errors = []
    for suite in sorted(os.listdir(SUITES_DIR)):
        suite_path = os.path.join(SUITES_DIR, suite)
        if suite == "smoke" or not os.path.isdir(suite_path):
            continue
        count, errs = yaml_parse_dir(suite_path)
        total_yaml += count
        yaml_errors.extend(errs)

    print(f"YAML: {total_yaml} parsed, {len(yaml_errors)} errors")
    if yaml_errors:
        for e in yaml_errors:
            print(e)
        errors.extend(yaml_errors)

    # 2. Triplet completeness
    triplet_ok = True
    for suite in triplet_suites():
        fixtures_dir = os.path.join(SUITES_DIR, suite, "fixtures")
        rubrics_dir = os.path.join(SUITES_DIR, suite, "rubrics")
        count, problems = check_triplets(suite, fixtures_dir, rubrics_dir)
        if problems:
            print(f"Triplets: {suite} {count} OK (ISSUES FOUND)")
            for p in problems:
                print(p)
            errors.extend(problems)
            triplet_ok = False
        else:
            print(f"Triplets: {suite} {count} OK")

    # calibration pairs
    calibration_dir = os.path.join(SUITES_DIR, "perspectives", "calibration")
    cal_count, cal_problems = check_calibration_pairs(calibration_dir)
    if cal_problems:
        print(f"Calibration pairs: {cal_count} OK (ISSUES FOUND)")
        for p in cal_problems:
            print(p)
        errors.extend(cal_problems)
    else:
        print(f"Calibration pairs: {cal_count} OK")

    # 3. Registry coverage
    try:
        reg_problems = check_registries()
        if reg_problems:
            print(f"Registries: ISSUES FOUND")
            for p in reg_problems:
                print(p)
            errors.extend(reg_problems)
        else:
            print(f"Registries: {registry_check_count()} checks OK")
    except Exception as e:
        msg = f"  Registry check failed: {e}"
        print(f"Registries: ERROR")
        print(msg)
        errors.append(msg)

    if errors:
        print(f"\nFAIL: {len(errors)} issue(s) found")
        sys.exit(1)
    else:
        print("\nAll checks passed")


if __name__ == "__main__":
    main()
